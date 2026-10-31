import json
import os
import sys
from generate_agent_dataset import assemble_all
from validate_iec import validate_json_file

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 75+ years experienced Principal Automation Fellow & Cyber-Physical Systems Chair writing world-class, ultra-complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced discrete state-space matrices, Model Predictive Control (MPC) quadratic cost approximations, 2oo3 Triple Modular Redundant (TMR) voting with discrepancy timers, ISA-18.2 multi-tiered alarm matrices, and multi-stage finite state machines. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Commercial Power & Renewable Energy: 15 MW Offshore Wind Turbine Individual Pitch Control (IPC) & Active Yaw System with Nacelle LiDAR Inflow Wind Feed-Forward**

Task: Implement the production-grade Function Block `FB_WindTurbine_Offshore15MW_PitchYaw_LiDAR` governing:
1. 15 MW Direct-Drive Permanent Magnet Synchronous Generator (PMSG) with medium-voltage full-scale back-to-back 4-quadrant converter.
2. Individual Pitch Control (IPC): Independent electrohydraulic / electromechanical pitch actuators for each of the 3 rotor blades (118 m blade length, rotor diameter > 240 m) performing multiblade coordinate Coleman transformation (d-q axis decomposition) to cancel 1P asymmetric aerodynamic thrust tilt and yaw bending moments on the main bearing.
3. Nacelle-mounted continuous-wave pulsed LiDAR wind preview: measuring inflow horizontal wind velocity, wind shear gradient, and incoming gust front 2.5 seconds (50–200 m) upstream, feeding forward pitch angle offsets before the wind gust impacts the rotor.
4. Active yaw drive system: 8 synchronized yaw motors with hydraulic brake calipers regulating nacelle yaw alignment into the mean wind vector while counteracting gyroscopic precessional torque.
5. Active tower damping: fore-aft and side-to-side tower top accelerometer feedback modulating collective pitch and generator torque to suppress offshore floating spar/jacket structure hydrodynamic resonance.
6. Discrete State-Space Model (16x16 state matrix A, 16x8 B, 8x16 C, 8x8 D) incorporating blade aeroelastic bending modes, drivetrain torsional compliance, generator electromagnetic torque, and floating foundation hydrodynamic pitching dynamics.
7. Receding-horizon MPC for joint generator torque and pitch rate optimization (Region II partial load power maximization vs Region III full load aerodynamic power shedding at rated 15 MW).
8. 2oo3 Triple Modular Redundancy (TMR) voting across blade root optical strain sensors, nacelle LiDAR velocity channels, tower accelerometers, and generator speed encoders.
9. 12-Stage Operational FSM (Grid Tie Synchronization, Brake Release & Idling Spin-Up, Region I Cut-In Feather Ramp, Region II Maximum Aerodynamic Cp Tracking, Region II.5 Transition Smoothing, Region III Constant Power Pitch Regulation, IPC Asymmetric Load Mitigation Active, LiDAR Wind Gust Feed-Forward Suppression, Storm High-Wind Hysteresis Cut-Out, Fast Pitch Feather Aerodynamic Braking, Mechanical Caliper Lock, Grid Fault Ride-Through FRT / Standby).
10. ISA-18.2 multi-tiered alarm matrix (Rotor overspeed HH trip > 115%, blade pitch discrepancy, generator bearing overtemp, tower vibration resonance trip, grid loss islanding trip) with bit-packed telemetry DWORDs.

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st.
2. EXACT AST PARITY: Every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;, every WHILE has END_WHILE;.
3. First line: FUNCTION_BLOCK FB_WindTurbine_Offshore15MW_PitchYaw_LiDAR, Last line: END_FUNCTION_BLOCK.
4. Total length >= 55,000 characters (zero placeholders, zero truncation comments)."""

st_code = assemble_all()
assistant_content = f"```iec-st\n{st_code}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

target_file = "data/swarm_raw/agent_8d1042ab.json"
os.makedirs(os.path.dirname(target_file), exist_ok=True)

with open(target_file, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Dataset successfully written to {target_file}")
print(f"Assistant content character count: {len(assistant_content)}")

# Now run validation directly
errs = validate_json_file(target_file)
if errs:
    print("VALIDATION FAILED with errors:")
    for e in errs:
        print(" -", e)
    sys.exit(1)
else:
    print("ALL VALIDATION CHECKS PASSED PERFECTLY!")
    sys.exit(0)
