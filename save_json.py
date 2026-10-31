import json
import os
import build_full_fadec

def assemble_and_save():
    os.makedirs("data/swarm_raw", exist_ok=True)
    target_path = "data/swarm_raw/agent_6c2019ea.json"

    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 75+ years experienced Principal Automation Fellow & Cyber-Physical Systems Chair writing world-class, ultra-complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced discrete state-space matrices, Model Predictive Control (MPC) quadratic cost approximations, 2oo3 Triple Modular Redundant (TMR) voting with discrepancy timers, ISA-18.2 multi-tiered alarm matrices, and multi-stage finite state machines. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Commercial Aerospace Propulsion: 110,000 lbf High-Bypass Turbofan Jet Engine Dual-Channel FADEC (Channel A / Channel B Cross-Talk) with Active Turbine Clearance Control (HPTCC) & Variable Stator Vanes (VSV)**

Task: Implement the production-grade Function Block `FB_Aerospace_Turbofan_DualChannelFADEC_110klbf` governing:
1. Discrete State-Space Matrices (A, B, C, D) 16x16 state matrix A, 16x8 matrix B, C, D incorporating N1/N2 rotor spool inertia, combustor volume lag, compressor stage pressure ratio, and thermal expansion of the turbine casing: x_{k+1} = A*x_k + B*u_k.
2. Model Predictive Control (MPC) quadratic cost optimization governing fuel flow rate (Wf), Variable Stator Vanes (VSV), and Active Turbine Clearance Control (HPTACC/LPTACC) along the compressor surge margin boundary (Wf / Ps3) to maximize thrust responsiveness while strictly enforcing compressor surge margin and turbine temperature limits.
3. 2oo3 Triple Modular Redundancy (TMR) voting logic on N1 spool pickups, N2 resolvers, Ps3 static pressure transducers, P2 inlet pressure, and an 8-thermocouple dual-element EGT harness with bumpless Channel A / Channel B cross-talk arbitration.
4. Aerodynamic compressor scheduling (VSV / VBV) and Active Turbine Clearance Control (HPTACC / LPTACC) blade tip clearance regulation to 0.25 mm (+/- 0.05 mm) to maximize cruise thermal efficiency and preserve EGT margin.
5. 12-Stage Operational Finite State Machine (PREFLIGHT_BIT_DIAG, ATS_PNEUMATIC_ENGAGE, DRY_MOTORING_CRANK, FUEL_LIGHTOFF_IGNITION, GROUND_IDLE_STABILIZE, TAXI_THRUST_GOVERN, TAKEOFF_RATED_RAMP_110KLBF, CLIMB_THRUST_PACING, CRUISE_ACC_OPTIMIZE, FLIGHT_IDLE_DESCENT_BLEED, THRUST_REVERSER_DEPLOY, EMERGENCY_FLAMEOUT_AUTORELIGHT).
6. ISA-18.2 / DO-178C multi-tiered alarm matrix (N2 overspeed HH trip > 105%, EGT redline breach, compressor stall surge detection, fuel filter impending bypass, dual-channel cross-talk health failure) with bit-packed telemetry DWORDs.

Ensure exhaustive implementation with zero placeholders, full mathematical expansions, and complete variable declarations."""

    st_code = build_full_fadec.generate_full_fadec_code()
    assistant_content = f"```iec-st\n{st_code}\n```"

    data = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            },
            {
                "role": "assistant",
                "content": assistant_content
            }
        ]
    }

    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated and wrote {target_path}")
    print(f"Assistant content character length: {len(assistant_content)}")
    print(f"Assistant content lines count: {len(assistant_content.splitlines())}")

if __name__ == "__main__":
    assemble_and_save()
