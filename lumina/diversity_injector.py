#!/usr/bin/env python3
"""
lumina/diversity_injector.py — Prompt Diversity & Instruction Style Injector
Reference: DOC-01, DOC-02, DOC-03

Solves the prompt template homogeneity problem (where 46.7% of datasets opened with the identical phrasing).
Rotates between 8 distinct real-world industrial prompt framing styles:
1. DIRECT_COMMAND: Precise technical imperative
2. ENGINEERING_BRIEF: Formal physical plant specification
3. PROBLEM_STATEMENT: Plant symptom / troubleshooting scenario
4. INCREMENTAL_EXTENSION: Extending an existing machine stub
5. CODE_REVIEW: Reviewing and refactoring sub-optimal code
6. COMPARISON_TASK: Comparing two control strategies and implementing the superior one
7. FAULT_RECOVERY: Fail-safe behavior and fault escalation
8. COMMISSIONING_QUERY: Cold-start to full production commissioning sequence
"""

import random
from typing import Dict, List, Tuple

INSTRUCTION_STYLES = [
    "DIRECT_COMMAND",
    "ENGINEERING_BRIEF",
    "PROBLEM_STATEMENT",
    "INCREMENTAL_EXTENSION",
    "CODE_REVIEW",
    "COMPARISON_TASK",
    "FAULT_RECOVERY",
    "COMMISSIONING_QUERY"
]

def generate_diverse_prompt(
    sector: str,
    system_code: str,
    system_desc: str,
    fb_name: str,
    style: str = None
) -> Tuple[str, str]:
    """
    Constructs a diverse user prompt for the given system.
    Returns: (style_name, prompt_text)
    """
    if style is not None and style not in INSTRUCTION_STYLES:
        raise ValueError(f"Invalid instruction style '{style}'. Must be one of {INSTRUCTION_STYLES}")
    chosen_style = style or random.choice(INSTRUCTION_STYLES)

    if chosen_style == "DIRECT_COMMAND":
        prompt = (
            f"You are a Principal Automation Fellow and Chair of Cyber-Physical Systems. "
            f"Develop a complete, production-ready IEC 61131-3 Function Block named `{fb_name}` for: {system_desc} ({sector.upper()} sector).\n\n"
            f"Strict engineering mandates:\n"
            f"1. Implement a complete discrete state-space model ($x_{{k+1}} = A x_k + B u_k$) with fully populated matrices.\n"
            f"2. Incorporate Model Predictive Control (MPC) quadratic cost optimization with prediction horizon $N \\ge 10$.\n"
            f"3. Implement 2oo3 (Two-out-of-Three) Triple Modular Redundancy (TMR) sensor voting with timed discrepancy mitigation.\n"
            f"4. Provide ISA-18.2 multi-tiered alarm management (HH, H, L, LL, rate-of-change, deadband hysteresis).\n"
            f"5. Design a multi-stage Finite State Machine (`CASE State OF`) covering startup, active synchronization, fault degradation, and safe stop.\n"
            f"Output purely valid IEC 61131-3 Structured Text framed in ```iec-st ... ``` without placeholders or summaries."
        )

    elif chosen_style == "ENGINEERING_BRIEF":
        prompt = (
            f"### Engineering Plant Specification: {system_desc}\n"
            f"**Target Sector**: {sector.replace('_', ' ').title()}\n"
            f"**Control Unit**: Beckhoff TwinCAT 3 / CODESYS 3.5 Runtime\n\n"
            f"We are engineering the automation controller for a new commercial line. We require a comprehensive Function Block `{fb_name}` that controls this equipment.\n"
            f"The specification requires:\n"
            f"- Rigorous 2oo3 voting across redundant process transmitters with bumpless channel degradation.\n"
            f"- Linear discrete-time state-space dynamics embedded directly into scan-time execution.\n"
            f"- Model Predictive Control algorithm computing optimal actuator commands.\n"
            f"- Full ISA-18.2 alarm prioritization.\n"
            f"- State machine governing all operating states.\n\n"
            f"Please deliver the complete, un-truncated Structured Text source code."
        )

    elif chosen_style == "PROBLEM_STATEMENT":
        prompt = (
            f"Our manufacturing plant operates a {system_desc} in the {sector} division. "
            f"During recent production runs, the existing legacy control loops caused process oscillation, sensor disagreement trips, and product quality variances. "
            f"To resolve these failures permanently, architect and deliver a brand-new, robust Function Block `{fb_name}` that incorporates:\n"
            f"- 2oo3 majority voting to eliminate single-sensor false trips.\n"
            f"- State-space model prediction and MPC regulation to damp out harmonic transients.\n"
            f"- Comprehensive FSM states with explicit entry/exit transitions.\n"
            f"- Multi-tiered ISA-18.2 alarms with deadbands.\n"
            f"Provide the complete IEC-ST code block."
        )

    elif chosen_style == "INCREMENTAL_EXTENSION":
        prompt = (
            f"In our {sector} facility, we need to upgrade the automation logic for {system_desc}. "
            f"The basic I/O definitions are in place, but we need the complete advanced cyber-physical control logic implemented in Function Block `{fb_name}`.\n\n"
            f"Build the full Function Block from the ground up, ensuring it includes:\n"
            f"- Full VAR, VAR_INPUT, VAR_OUTPUT declarations with bracketed physical engineering units.\n"
            f"- Triple modular redundant (2oo3) sensor validation.\n"
            f"- Discrete state-space matrices ($A, B, C, D$) and MPC solver.\n"
            f"- Complete multi-state sequencing FSM and ISA-18.2 alarm buffers.\n"
            f"Render the entire production-grade code in ```iec-st```."
        )

    elif chosen_style == "CODE_REVIEW":
        prompt = (
            f"Act as a Principal Automation Fellow reviewing control architectures for: {system_desc} ({sector}). "
            f"Previous attempts at this Function Block lacked mathematical depth, had no state-space representation, and omitted redundancy. "
            f"Write the definitive, industry-standard implementation of `{fb_name}` that sets the benchmark for cyber-physical reliability:\n"
            f"- Exact discrete state-space formulation with physical coefficients.\n"
            f"- Model Predictive Control horizon optimization ($N \\ge 10$).\n"
            f"- Fault-tolerant 2oo3 voter with discrepancy tracking.\n"
            f"- ISA-18.2 alarm thresholds and complete state transition logic.\n"
            f"Output complete code without truncation."
        )

    elif chosen_style == "COMPARISON_TASK":
        prompt = (
            f"For controlling {system_desc} in high-throughput {sector} manufacturing, traditional single-loop PID controllers suffer from phase lag and lack anticipatory feed-forward. "
            f"We are implementing a discrete State-Space Model Predictive Control (MPC) approach with 2oo3 TMR voting.\n"
            f"Generate the full Function Block `{fb_name}` that proves this advanced architecture:\n"
            f"- Fully parameterized state matrices ($A, B, C, D$).\n"
            f"- Constrained quadratic cost MPC minimization.\n"
            f"- Redundant sensor voting with mismatch timers.\n"
            f"- ISA-18.2 alarm hierarchy and deterministic finite state machine.\n"
            f"Provide the full IEC 61131-3 Structured Text."
        )

    elif chosen_style == "FAULT_RECOVERY":
        prompt = (
            f"Functional safety and uninterrupted operation are critical for our {system_desc} ({sector}). "
            f"We require a resilient controller Function Block `{fb_name}` that guarantees safety and bumpless fault recovery:\n"
            f"- Sensor failures: 2oo3 TMR majority voting with discrepancy detection and automatic 1oo2 failover.\n"
            f"- Actuator saturation: MPC cost function with penalty weights and rate limits.\n"
            f"- Emergency states: Deterministic FSM handling degraded modes, controlled braking, and safe interlocks.\n"
            f"- Alarms: ISA-18.2 compliant priority escalation (Warning, High, High-High emergency trip).\n"
            f"Deliver the complete Structured Text code."
        )

    else:  # COMMISSIONING_QUERY
        prompt = (
            f"We are commissioning a greenfield {system_desc} installation in our {sector} plant. "
            f"To support cold-commissioning through full-rate production, generate the master Function Block `{fb_name}`.\n"
            f"The controller must implement:\n"
            f"1. FSM sequencing across: Initialization, Calibration, Pre-heat/Pressurization, Production Run, Ramp-Down, and Faulted.\n"
            f"2. Triple Modular Redundant sensor verification.\n"
            f"3. Discrete state-space dynamics and MPC compensation.\n"
            f"4. ISA-18.2 alarm limits with hysteresis.\n"
            f"Format as a complete, un-truncated ```iec-st``` code block."
        )

    return chosen_style, prompt
