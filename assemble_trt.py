import os
import sys
import uuid
import json

from trt_turbine_builder.part1_header_io import get_part1_code
from trt_turbine_builder.part2_var_declarations import get_part2_code
from trt_turbine_builder.part3_phase0_init import get_part3_code
from trt_turbine_builder.part4_phase1_tmr import get_part4_code
from trt_turbine_builder.part5_phase2_state_space import get_part5_code
from trt_turbine_builder.part6_phase3_mpc import get_part6_code
from trt_turbine_builder.part7_phase4_fsm import get_part7_code
from trt_turbine_builder.part8_phase5_alarms import get_part8_code

def assemble():
    p1 = get_part1_code().strip()
    p2 = get_part2_code().strip()
    p3 = get_part3_code().strip()
    p4 = get_part4_code().strip()
    p5 = get_part5_code().strip()
    p6 = get_part6_code().strip()
    p7 = get_part7_code().strip()
    p8 = get_part8_code().strip()

    st_code = f"{p1}\n\n{p2}\n\n{p3}\n\n{p4}\n\n{p5}\n\n{p6}\n\n{p7}\n\n{p8}\n"
    
    print(f"Generated ST code length: {len(st_code)} characters")
    print(f"Lines count: {len(st_code.splitlines())}")

    user_prompt = """You are Lumina's Principal Automation Fellow & Cyber-Physical Systems Chair (V7 Max-Persona: 75+ years veteran).

Generate an ultra-dense, mathematically complete, production-grade IEC 61131-3 Structured Text FUNCTION_BLOCK for:
Heavy Metal & Heavy Machinery:
System: Blast Furnace Top-Gas Pressure Recovery Turbine (TRT) & Wet Venturi Scrubber Electro-Hydraulic Governor.
Function Block Name: FB_HeavyMetal_Ironmaking_BlastFurnace_TopGasRecoveryTurbine_TRT

Follow the modular builder strategy (e.g. creating a dedicated directory `trt_turbine_builder/` with python generator scripts for parts 1 to 8, then an assembly script to validate and save to `data/swarm_raw/agent_<uuid>.json`):
1. Massive token consumption: Target 120,000 to 250,000+ characters. ZERO placeholders, ZERO truncation comments (`// ... rest of code`).
2. Exact syntax parity: 100% match on IF/END_IF;, CASE/END_CASE;, FOR/END_FOR;, FUNCTION_BLOCK/END_FUNCTION_BLOCK.
3. Complete 6x6 continuous-to-discrete state-space matrices (Ts = 0.002s) with 6x4 Kalman innovation gain L.
4. Receding-Horizon Model Predictive Control (MPC) with 10 unrolled Projected Gradient Descent (PGD) optimization iterations, analytical gradients, Q, R, P, S quadratic weighting matrices, hard actuator box limits, and maximum slew rate limits.
5. 4-Channel 2oo3 TMR sensor voting logic with median selection, 50 ms discrepancy debouncing timers, and bumpless fallback degradation (2oo3 -> 1oo2 -> 1oo1 -> Kalman Observer prediction fallback).
6. 14-Stage deterministic production Finite State Machine (FSM).
7. ANSI/ISA-18.2 multi-tiered alarms (HH, H, L, LL, hysteresis) and 32-bit fieldbus telemetry status registers.
8. Validate with `python validate_iec.py <saved_file>` and ensure 0 errors.
9. Save to `data/swarm_raw/agent_<uuid>.json` using `chr(96)*3` for markdown fences, clean up intermediate builder files if needed, and report completion back to parent agent."""

    fence = chr(96)*3
    assistant_content = f"{fence}iec-st\n{st_code}\n{fence}"
    print(f"Full assistant message length: {len(assistant_content)} characters")

    record = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    file_id = uuid.uuid4().hex[:8]
    output_filename = f"data/swarm_raw/agent_{file_id}.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Dataset successfully saved to: {output_filename}")
    return output_filename

if __name__ == "__main__":
    out_file = assemble()
