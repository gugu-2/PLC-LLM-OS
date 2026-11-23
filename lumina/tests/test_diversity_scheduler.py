#!/usr/bin/env python3
"""
Unit and Integration Tests for Lumina Prompt Diversity & Domain Scheduler
========================================================================
Audits and verifies:
1. All 8 instruction styles in lumina/diversity_injector.py
2. Deficit-based sector scheduling in lumina/domain_scheduler.py
3. End-to-end task generation in lumina/prompt_templates.py
"""

import pytest
import itertools
from collections import Counter
from lumina.diversity_injector import INSTRUCTION_STYLES, generate_diverse_prompt
from lumina.domain_scheduler import DomainScheduler, SECTOR_SYSTEM_CATALOG, TARGET_RATIOS
from lumina.prompt_templates import build_code_generation_task, V7_SYSTEM_PERSONA


# ==============================================================================
# 1. Diversity Injector Test Cases (8 Instruction Styles)
# ==============================================================================

def test_instruction_styles_count_and_naming():
    """Verify exact 8 industrial instruction styles are defined."""
    assert len(INSTRUCTION_STYLES) == 8
    expected_styles = {
        "DIRECT_COMMAND",
        "ENGINEERING_BRIEF",
        "PROBLEM_STATEMENT",
        "INCREMENTAL_EXTENSION",
        "CODE_REVIEW",
        "COMPARISON_TASK",
        "FAULT_RECOVERY",
        "COMMISSIONING_QUERY"
    }
    assert set(INSTRUCTION_STYLES) == expected_styles


@pytest.mark.parametrize("style", INSTRUCTION_STYLES)
def test_each_instruction_style_generates_valid_prompt(style):
    """Verify each style produces an exhaustive, well-formed prompt with required industrial parameters."""
    sector = "automotive"
    system_code = "BIW_LaserWeld"
    system_desc = "Robotic Body-in-White Seam & Spot Laser Welding Station"
    fb_name = "FB_Automotive_BIW_LaserWeld"

    chosen_style, prompt = generate_diverse_prompt(sector, system_code, system_desc, fb_name, style=style)

    assert chosen_style == style
    assert isinstance(prompt, str)
    assert len(prompt) >= 500  # Detailed prompt requirements
    assert fb_name in prompt
    assert system_desc in prompt
    assert sector.upper() in prompt or sector in prompt.lower() or sector.replace("_", " ").title() in prompt


def test_instruction_styles_opening_diversity():
    """Verify every style has a unique, non-overlapping opening sentence structure."""
    sector = "electronics"
    system_code = "SMT_DualGantry_PickPlace"
    system_desc = "Dual-Gantry High-Speed SMT Placement Machine (100,000 cph)"
    fb_name = "FB_Electronics_SMT_DualGantry_PickPlace"

    openings = []
    for style in INSTRUCTION_STYLES:
        _, prompt = generate_diverse_prompt(sector, system_code, system_desc, fb_name, style=style)
        first_line = prompt.strip().split("\n")[0]
        openings.append(first_line)

    # All opening lines must be strictly distinct (0% duplication)
    assert len(set(openings)) == len(INSTRUCTION_STYLES)


def test_instruction_styles_pairwise_diversity_jaccard():
    """Verify pairwise lexical diversity (Jaccard similarity < 0.35) between all 8 styles."""
    sector = "heavy_machinery"
    system_code = "ServoPress_2500T"
    system_desc = "2,500-Ton Multi-Axis Servo Stamping Press with Electronic Die Cushion"
    fb_name = "FB_Heavy_Machinery_ServoPress_2500T"

    prompts = {}
    for style in INSTRUCTION_STYLES:
        _, p = generate_diverse_prompt(sector, system_code, system_desc, fb_name, style=style)
        tokens = set(p.lower().replace("\n", " ").split())
        prompts[style] = tokens

    for s1, s2 in itertools.combinations(INSTRUCTION_STYLES, 2):
        toks1 = prompts[s1]
        toks2 = prompts[s2]
        jaccard = len(toks1 & toks2) / len(toks1 | toks2)
        # Pairwise Jaccard similarity must be below 0.35 even with shared domain terms
        assert jaccard < 0.35, f"Styles {s1} and {s2} are too similar (Jaccard: {jaccard:.3f})"


def test_invalid_instruction_style_raises_error():
    """Verify passing an unrecognized style name raises ValueError."""
    with pytest.raises(ValueError, match="Invalid instruction style"):
        generate_diverse_prompt("automotive", "TEST", "Test System", "FB_Test", style="NON_EXISTENT_STYLE")


def test_diversity_injector_random_selection():
    """Verify that omitting style triggers random selection among all 8 styles."""
    sector = "plastics"
    system_code = "InjectionMolding_1200T_CavityPress"
    system_desc = "1,200-Ton Multi-Cavity Injection Molding Machine"
    fb_name = "FB_Plastics_InjectionMolding"

    sampled_styles = set()
    for _ in range(50):
        s, _ = generate_diverse_prompt(sector, system_code, system_desc, fb_name)
        sampled_styles.add(s)

    # Over 50 random calls, all or nearly all styles should be sampled
    assert len(sampled_styles) >= 6


# ==============================================================================
# 2. Domain Scheduler Test Cases (7 Target Sectors & Quotas)
# ==============================================================================

def test_catalog_and_target_ratios_integrity():
    """Verify that 7 target sectors are defined and quotas sum to exactly 1.0 (100%)."""
    assert len(TARGET_RATIOS) == 7
    assert pytest.approx(sum(TARGET_RATIOS.values()), abs=1e-6) == 1.0

    # Ensure every target sector exists in catalog with non-empty systems
    for sector, quota in TARGET_RATIOS.items():
        assert sector in SECTOR_SYSTEM_CATALOG
        assert len(SECTOR_SYSTEM_CATALOG[sector]) >= 3
        assert quota > 0.0

    expected_quotas = {
        "automotive": 0.25,
        "heavy_machinery": 0.20,
        "electronics": 0.15,
        "semiconductor": 0.15,
        "plastics": 0.10,
        "foodbev": 0.10,
        "steelmaking": 0.05
    }
    for sec, exp_q in expected_quotas.items():
        assert TARGET_RATIOS[sec] == exp_q


def test_scheduler_cold_start():
    """Verify scheduler defaults to highest priority sector when counts are 0."""
    scheduler = DomainScheduler()
    sec, code, desc = scheduler.select_next_assignment()
    assert sec == "automotive"
    assert any(code == c for c, _ in SECTOR_SYSTEM_CATALOG["automotive"])


def test_scheduler_quota_balancing_convergence_n1000():
    """Verify scheduler converges to target quotas with near zero deviation over 1000 steps."""
    scheduler = DomainScheduler()
    history = []
    N = 1000

    for _ in range(N):
        sec, _, _ = scheduler.select_next_assignment()
        scheduler.update_count(sec)
        history.append(sec)

    counts = Counter(history)
    for sector, target_pct in TARGET_RATIOS.items():
        actual_pct = counts[sector] / N
        deviation = abs(actual_pct - target_pct)
        # For N=1000, deviation should be exactly 0.0 due to integer cycle of 20
        assert deviation < 0.005, f"Sector {sector} deviated: actual={actual_pct}, target={target_pct}"


def test_scheduler_exact_quantum_n20():
    """Verify that every 20-step quantum perfectly satisfies integer allocations."""
    scheduler = DomainScheduler()
    for _ in range(20):
        sec, _, _ = scheduler.select_next_assignment()
        scheduler.update_count(sec)

    # 20 * ratios: auto=5, heavy=4, elec=3, semi=3, plastic=2, food=2, steel=1
    expected_counts = {
        "automotive": 5,
        "heavy_machinery": 4,
        "electronics": 3,
        "semiconductor": 3,
        "plastics": 2,
        "foodbev": 2,
        "steelmaking": 1
    }
    assert scheduler.counts == expected_counts


def test_scheduler_rebalancing_from_skewed_state():
    """Verify scheduler prioritizes deficit sectors when initialized with skewed counts."""
    # Automotive is over-represented (50 samples, while others are 0)
    skewed_counts = {
        "automotive": 50,
        "heavy_machinery": 0,
        "electronics": 0,
        "semiconductor": 0,
        "plastics": 0,
        "foodbev": 0,
        "steelmaking": 0
    }
    scheduler = DomainScheduler(current_sector_counts=skewed_counts.copy())

    # Run 150 tasks (total will reach 200)
    for _ in range(150):
        sec, _, _ = scheduler.select_next_assignment()
        scheduler.update_count(sec)

    # At total = 200, automotive target is 200 * 0.25 = 50, which was already satisfied.
    # Therefore, 0 new automotive tasks should have been selected!
    assert scheduler.counts["automotive"] == 50
    assert scheduler.counts["heavy_machinery"] == 40  # 20% of 200
    assert scheduler.counts["electronics"] == 30      # 15% of 200
    assert scheduler.counts["semiconductor"] == 30    # 15% of 200
    assert scheduler.counts["plastics"] == 20         # 10% of 200
    assert scheduler.counts["foodbev"] == 20          # 10% of 200
    assert scheduler.counts["steelmaking"] == 10      # 5% of 200


def test_scheduler_system_selection_diversity():
    """Verify that multiple distinct systems are chosen within a sector."""
    scheduler = DomainScheduler()
    # Force heavy_machinery by setting other counts high
    heavy_systems = set()
    for _ in range(30):
        sec, code, _ = scheduler.select_next_assignment()
        if sec == "automotive":
            heavy_systems.add(code)
        scheduler.update_count(sec)

    assert len(heavy_systems) > 1


# ==============================================================================
# 3. Prompt Templates Integration Test Cases
# ==============================================================================

def test_v7_persona_text():
    """Verify V7 persona includes all mandated Principal Fellow directives."""
    assert "Principal Automation Fellow & Cyber-Physical Systems Chair" in V7_SYSTEM_PERSONA
    assert "75+ years veteran" in V7_SYSTEM_PERSONA
    assert "Model Predictive Control" in V7_SYSTEM_PERSONA
    assert "2oo3 Triple Modular Redundancy" in V7_SYSTEM_PERSONA
    assert "ISA-18.2" in V7_SYSTEM_PERSONA
    assert "discrete state-space matrices" in V7_SYSTEM_PERSONA


def test_build_code_generation_task_structure():
    """Verify build_code_generation_task returns fully populated task dictionary."""
    task = build_code_generation_task(
        sector="semiconductor",
        system_code="Cleanroom_HEPA_FFU_Control",
        system_desc="ISO Class 3 Semiconductor Cleanroom HVAC FFU Pressure Cascading",
        style="ENGINEERING_BRIEF"
    )

    required_keys = [
        "sector",
        "system_code",
        "system_desc",
        "fb_name",
        "instruction_style",
        "system_persona",
        "user_prompt"
    ]
    for key in required_keys:
        assert key in task
        assert isinstance(task[key], str)
        assert len(task[key]) > 0

    assert task["instruction_style"] == "ENGINEERING_BRIEF"
    assert task["fb_name"] == "FB_Semiconductor_Cleanroom_HEPA_FFU_Control"
    assert task["system_persona"] == V7_SYSTEM_PERSONA
    assert task["fb_name"] in task["user_prompt"]


def test_build_code_generation_task_with_scheduler():
    """Verify build_code_generation_task integrates with DomainScheduler."""
    scheduler = DomainScheduler()
    task = build_code_generation_task(scheduler=scheduler)

    assert task["sector"] in TARGET_RATIOS
    assert task["system_code"] is not None
    assert task["instruction_style"] in INSTRUCTION_STYLES
    assert task["fb_name"].startswith("FB_")


def test_scheduler_auto_update_and_deficits():
    """Verify auto_update parameter automatically increments sector count and deficit tracking."""
    scheduler = DomainScheduler()
    deficits_init = scheduler.get_deficits()
    assert deficits_init["automotive"] == 0.25

    sec1, _, _ = scheduler.select_next_assignment(auto_update=True)
    assert sec1 == "automotive"
    assert scheduler.counts["automotive"] == 1
    assert scheduler.counts["heavy_machinery"] == 0

    dist = scheduler.get_distribution()
    assert dist["automotive"] == 1.0

    # Next assignment must pick highest deficit (heavy machinery with deficit 0.20)
    sec2, _, _ = scheduler.select_next_assignment(auto_update=True)
    assert sec2 == "heavy_machinery"
    assert scheduler.counts["heavy_machinery"] == 1


def test_build_code_generation_task_auto_update():
    """Verify build_code_generation_task propagates auto_update to scheduler."""
    scheduler = DomainScheduler()
    t1 = build_code_generation_task(scheduler=scheduler, auto_update=True)
    t2 = build_code_generation_task(scheduler=scheduler, auto_update=True)

    assert t1["sector"] == "automotive"
    assert t2["sector"] == "heavy_machinery"
    assert sum(scheduler.counts.values()) == 2
