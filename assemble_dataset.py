# assemble_dataset.py
import sys
import json
import os
import subprocess

sys.path.append("tubular_gen")

from part1_header_io import header_io_text
from part2_vars import vars_text
from part3_tmr_kinetics import tmr_kinetics_text
from part4_mpc import mpc_text
from part5_fsm import fsm_text
from part6_dump_alarms import dump_alarms_text

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 75+ years experienced Principal Automation Fellow & Cyber-Physical Systems Chair writing world-class, ultra-complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced discrete state-space matrices, Model Predictive Control (MPC) quadratic cost approximations, 2oo3 Triple Modular Redundant (TMR) voting with discrepancy timers, ISA-18.2 multi-tiered alarm matrices, and multi-stage finite state machines. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Commercial Petrochemicals & Polymers: Continuous Ultra-High-Pressure (3,000 Bar) Ethylene Polymerization Tubular Reactor (LDPE/EVA) with Multi-Zone Peroxide Dosing & Emergency Fast Depressurization SIL-3**

Task: Implement the production-grade Function Block FB_Petrochem_EthylenePolymerization_3000Bar_Tubular governing:
1. Ultra-high-pressure continuous tubular reactor (Length 1,500 m to 2,500 m, inner diameter 40–60 mm, operating pressures 2,200 to 3,200 bar, process temperatures 160 to 320 deg C).
2. Multi-stage hyper-compressor (plunger reciprocating compressor delivering ethylene monomer at 3,000 bar) with vibration crosshead monitoring and cylinder packing leakage detection.
3. Multi-zone initiator dosing: 4 independent organic peroxide injection points along the tube length with micro-metering intensifier pumps controlling free-radical polymerization rate, peak temperature profiles, and monomer conversion (25–35% per pass).
4. High-pressure water jackets: counter-current pressurized hot water cooling/heating zones controlling reaction exotherm and preventing runaway decomposition of ethylene into carbon and methane.
5. High-Pressure Let-Down Valve (HPLDV): precision electrohydraulic needle valve dynamically modulating backpressure (3,000 bar down to 250 bar into High-Pressure Separator HPS) with acoustic shockwave attenuation.
6. Decomposition detection & Emergency Dump System (EDS): high-speed piezo-quartz pressure sensors detecting explosive decomposition pressure rise rate (dP/dt > 1,500 bar/s); actuating 4 hydraulic dump valves opening to flare/catch tank in < 50 ms (SIL-3 safety instrumented function).
7. Discrete State-Space Model (16x16 state matrix A, 16x8 B, C, D) incorporating radical initiation kinetics, propagation exotherm, non-Newtonian polymer melt rheology, and axial tube heat conduction.
8. Receding-horizon MPC for multivariable control of initiator dosing rates, jacket water temperatures, and let-down valve position to maximize polymer yield while maintaining molecular weight distribution (MFI).
9. 2oo3 Triple Modular Redundancy (TMR) voting across tubular reactor strain-gauge pressure transmitters, peak temperature thermocouples, and hyper-compressor discharge pressure sensors with bumpless degradation.
10. 12-Stage Operational FSM (Inert Gas Leak Test & Hydraulic Pressure Pre-Load, Ethylene Gas Flush & Recycle Line Pre-Cool, Hyper-Compressor Staged Ramp-Up to 2,000 Bar, Hot Water Jacket Thermal Preheat, Initiator Peroxide Zone 1 Dosing Cut-In, Reaction Exotherm Light-Off & Zone Staging, Full-Rate Steady-State 3,000 Bar Polymerization, Molecular Weight Regulator (CTA) Trimming, Transition to EVA Co-Monomer Feed, Controlled Reactor Rinse & Flush Run-Down, Inactive Recycle Gas Sweeping, Emergency Decomposition SIL-3 Fast Dump Flare).
11. ISA-18.2 multi-tiered alarm matrix (Pressure decomposition dP/dt HH trip, tube skin temperature runaway HH, let-down valve cavitation warning, hyper-compressor packing leak, flare interlock) with bit-packed telemetry DWORDs.

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st.
2. EXACT AST PARITY: Every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;, every WHILE has END_WHILE;.
3. First line: FUNCTION_BLOCK FB_Petrochem_EthylenePolymerization_3000Bar_Tubular, Last line: END_FUNCTION_BLOCK.
4. Total length >= 55,000 characters (zero placeholders, zero truncation comments)."""

st_body = header_io_text.strip() + "\n\n" + \
          vars_text.strip() + "\n\n" + \
          tmr_kinetics_text.strip() + "\n\n" + \
          mpc_text.strip() + "\n\n" + \
          fsm_text.strip() + "\n\n" + \
          dump_alarms_text.strip()

assistant_content = f"```iec-st\n{st_body}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

target_file = "data/swarm_raw/agent_3d8109bf.json"
os.makedirs("data/swarm_raw", exist_ok=True)
with open(target_file, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Successfully generated and wrote {target_file}")
print(f"Assistant Content Length: {len(assistant_content)} characters")
print(f"Total Lines: {len(assistant_content.splitlines())}")

# Run validation
cmd = [sys.executable, "validate_iec.py", target_file]
res = subprocess.run(cmd, capture_output=True, text=True)
print("Validation Output:\n", res.stdout)
if res.stderr:
    print("Validation Errors:\n", res.stderr)
if res.returncode == 0:
    print(">>> VALIDATION TEST PASSED 100%! <<<")
else:
    print(f">>> VALIDATION FAILED WITH EXIT CODE {res.returncode} <<<")
    sys.exit(res.returncode)
