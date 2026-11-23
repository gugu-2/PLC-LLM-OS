#!/usr/bin/env python3
"""
lumina/prompt_templates.py — Centralized Prompt Construction & Persona Engine
Reference: DOC-01, DOC-02, DOC-03, DOC-04

Maintains the authoritative V7 Max-Persona (Principal Automation Fellow & Cyber-Physical Systems Chair)
and provides structured prompt builders for:
- Full Function Block Code Generation (Single-Turn with 8 diversity styles)
- Multi-Turn Technical Dialogues (Type 1)
- 3-Turn Fault Diagnosis & Debug Chains (Type 2)
- Incremental Code Modification (Type 3)
- Concept-to-Code Translation (Type 4)
- SIF Functional Safety Scenarios (Type 6)
"""

import random
from typing import Dict, List, Tuple
from .domain_scheduler import DomainScheduler, SECTOR_SYSTEM_CATALOG
from .diversity_injector import generate_diverse_prompt, INSTRUCTION_STYLES

V7_SYSTEM_PERSONA = (
    "You are the Principal Automation Fellow & Cyber-Physical Systems Chair, a 75+ years veteran "
    "of industrial automation, PLC architecture, and heavy commercial manufacturing. "
    "You write mathematically complete, fault-tolerant, production-grade IEC 61131-3 Structured Text. "
    "You never produce placeholders, summaries, or truncated code comments. "
    "Every Function Block contains explicit discrete state-space matrices (A, B, C, D), "
    "Model Predictive Control (MPC) quadratic cost optimization with horizon N >= 10, "
    "2oo3 Triple Modular Redundancy (TMR) voting logic with discrepancy timers, "
    "ISA-18.2 multi-tiered alarm management (HH, H, L, LL, deadband hysteresis), "
    "and a deterministic Finite State Machine (CASE State OF)."
)

def build_code_generation_task(
    sector: str = None,
    system_code: str = None,
    system_desc: str = None,
    style: str = None,
    scheduler: DomainScheduler = None,
    auto_update: bool = False
) -> Dict:
    """Build a complete code generation dataset task prompt."""
    if scheduler and not sector:
        sector, system_code, system_desc = scheduler.select_next_assignment(auto_update=auto_update)
    elif not sector:
        sec = random.choice(list(SECTOR_SYSTEM_CATALOG.keys()))
        system_code, system_desc = random.choice(SECTOR_SYSTEM_CATALOG[sec])
        sector = sec

    fb_name = f"FB_{sector.replace('-', '_').title()}_{system_code}"
    chosen_style, user_prompt = generate_diverse_prompt(sector, system_code, system_desc, fb_name, style=style)

    return {
        "sector": sector,
        "system_code": system_code,
        "system_desc": system_desc,
        "fb_name": fb_name,
        "instruction_style": chosen_style,
        "system_persona": V7_SYSTEM_PERSONA,
        "user_prompt": user_prompt
    }
