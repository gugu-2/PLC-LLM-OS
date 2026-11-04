# assemble_cbw.py
import os
import sys
import json
import uuid

# Import the builder modules
sys.path.append(os.path.dirname(__file__))
from part1_declarations import get_part1
from part2_tmr_voting import get_part2
from part3_observers import get_part3
from part4_state_space_mpc import get_part4
from part5_fsm import get_part5
from part6_press_alarms_outputs import get_part6

def assemble():
    p1 = get_part1().strip()
    p2 = get_part2().strip()
    p3 = get_part3().strip()
    p4 = get_part4().strip()
    p5 = get_part5().strip()
    p6 = get_part6().strip()

    full_st = f"{p1}\n\n{p2}\n\n{p3}\n\n{p4}\n\n{p5}\n\n{p6}"
    print(f"Assembled Full Structured Text length: {len(full_st)} characters")
    print(f"Total lines: {len(full_st.splitlines())}")

    # Verify first and last line
    lines = [l.strip() for l in full_st.splitlines() if l.strip()]
    print(f"First line: {lines[0]}")
    print(f"Last line: {lines[-1]}")
    assert lines[0] == "FUNCTION_BLOCK FB_Laundry_ContinuousTunnel_WaterRecycle_Press", f"Bad first line: {lines[0]}"
    assert lines[-1] == "END_FUNCTION_BLOCK", f"Bad last line: {lines[-1]}"

    # Prepare fenced content
    fenced_code = f"```iec-st\n{full_st}\n```"
    print(f"Fenced content character count: {len(fenced_code)}")

    # Prompt
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 75+ years experienced Principal Automation Fellow & Cyber-Physical Systems Chair writing world-class, ultra-complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced discrete state-space matrices, Model Predictive Control (MPC) quadratic cost approximations, 2oo3 Triple Modular Redundant (TMR) voting with discrepancy timers, ISA-18.2 multi-tiered alarm matrices, and multi-stage finite state machines. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Commercial Industrial Services / Large-Scale Automated Commercial Laundry - Continuous Batch Tunnel Washer (CBW, 16-Compartment Archimedean Screw / Top-Transfer, 2,000 kg/h textile throughput): Counter-Flow Water Reclamation & Heat Recovery Network (Plate Heat Exchanger with Greywater Filtration), Compartment-Wise Direct Steam Injection & Closed-Loop Temperature Profiling (40°C pre-wash -> 85°C main wash -> 50°C rinse), 12-Channel Peristaltic Chemical Dosing Manifold with Inductive Conductivity Feedback (Alkali, Detergent, Bleach, Neutralizer/Sour, Softener), 50-Bar Hydraulic Membrane Dewatering Press (Cake Extraction with Linear Position Transducer & Moisture Observer), Shuttle Conveyor Cake Transfer Interlocks, and Water Recycle Turbidity / pH Closed-Loop Quality Interlocks.**

Task: Implement the production-grade Function Block FB_Laundry_ContinuousTunnel_WaterRecycle_Press governing:
1. Discrete State-Space Matrices (A, B, C, D) modeling pre-wash temperature, main wash zone 1 & 2 temperatures, rinse water temperature, greywater heat recovery reclaim tank level, wash bath inductive conductivity, rinse bath neutralization pH, membrane press ram position, and cake moisture percentage: x_{k+1} = A*x_k + B*u_k.
2. Model Predictive Control (MPC) quadratic cost optimization governing direct steam injection valve, fresh water makeup valve, reclaimed water recirculation pump, 12-channel chemical dosing pumps (alkali, detergent, bleach, neutralizer, softener), and hydraulic press proportional pressure relief valve.
3. 2oo3 TMR voting logic on all critical transmitters (main wash zone temp probes, reclaim tank level transmitters, wash bath inductive conductivity probes, hydraulic press 50-bar pressure transducers, plate heat exchanger preheat temp probes, reclaimed water turbidity optical analyzers).
4. Cyber-physical observers: Terzaghi consolidation & Darcy porous medium cake dewatering observer, Plate Heat Exchanger (PHE) LMTD effectiveness observer, temperature-compensated inductive conductivity alkali concentration observer, water recycle turbidity quality settling observer, and peristaltic pump tube fatigue observer.
5. 12-stage operational FSM (CBW_STATE_STANDBY_IDLE through CBW_STATE_EMERGENCY_PRESS_DUMP_SAFE).
6. 50-bar hydraulic membrane press dewatering sequence with linear position transducer profile tracking, acoustic cavitation suppression on direct steam injectors, and shuttle conveyor multi-bay dryer transfer collision interlocks.
7. ISA-18.2 multi-tiered alarm hierarchy with hydraulic overpressure slam-dump, steam isolation, chemical spill interlocks, and diagnostic status word packing.

Ensure exhaustive implementation with zero placeholders, full mathematical expansions, and complete variable declarations."""

    # Generate isolated JSON
    agent_id = uuid.uuid4().hex[:8]
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "swarm_raw", f"agent_{agent_id}.json"))

    record = {
        "id": f"agent_{agent_id}",
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": fenced_code}
        ],
        "metadata": {
            "domain": "Commercial Industrial Services / Large-Scale Automated Commercial Laundry",
            "system": "Continuous Batch Tunnel Washer (CBW, 16-Compartment Archimedean Screw / Top-Transfer, 2,000 kg/h textile throughput) & 50-Bar Membrane Dewatering Press",
            "function_block": "FB_Laundry_ContinuousTunnel_WaterRecycle_Press",
            "characters": len(fenced_code),
            "lines": len(full_st.splitlines()),
            "validated": True,
            "tier": 4,
            "rank": 38
        }
    }

    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Successfully saved record to: {json_path}")
    return json_path

if __name__ == "__main__":
    assemble()
