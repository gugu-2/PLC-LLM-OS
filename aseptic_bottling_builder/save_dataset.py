# Dataset Saver for Food & Beverage Aseptic Bottling
import os
import json
import uuid
import sys
from build import generate_code

def save():
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.

DOMAIN & SPECIFICATION:
- Domain: Food & Beverage Mass Production (Tier 1 Priority Sector)
- System: 60,000 bph Continuous Rotary Aseptic Beverage Bottling Carousel
  - Electromagnetic induction flowmeter dosing valve high-speed electronic camming
  - Vaporized Hydrogen Peroxide (VHP) dry preform sterilization & hot sterile air activation
  - Class 100 / ISO 5 positive-pressure laminar airflow sterile isolator chamber management
  - Automated Clean-In-Place (CIP) caustic/acid sanitization & Steam-In-Place (SIP) thermal lethality (F0) monitoring
- Function Block Name: FB_FoodBev_AsepticBottling_RotaryCarouselSterilization

MANDATORY REQUIREMENTS:
1. Transmitter & Tag Nomenclature:
   Standardized industrial P&ID tags: ST_CAROUSEL_SPEED_RPM_101A/B/C, FT_DOSING_FLOW_MLS_201A/B/C, PT_ISOLATOR_DIFF_PRESS_PA_301A/B/C, AT_VHP_CONC_PPM_401A/B/C, TT_STERILE_ZONE_TEMP_C_501A/B/C, PT_STEAM_BARRIER_PRESS_BAR_601A/B/C, LT_BOTTLE_MENISCUS_MM_701A/B/C, JT_CAPPING_TORQUE_NM_801A/B/C, QT_CIP_CONDUCTIVITY_MSCM_901A/B/C, VT_LAMINAR_AIR_VELOCITY_MS_951A/B/C.
2. 2oo3 Triple Modular Redundancy (TMR):
   Full triplicated voting across carousel rotational speed, dosing flow rate, isolator differential pressure, VHP gas concentration, sterile zone RTD temperature, steam barrier pressure, bottle meniscus fill level, capping torque, CIP fluid conductivity, and laminar velocity with pairwise deviation registers, discrepancy qualification debounce timers, bumpless degradation (2oo3 -> 1oo2 -> single -> trip), and status bitmask packing.
3. Advanced Cyber-Physical Observers & Algorithms:
   - Bigelow thermal lethality F0 integration with trapezoidal rule and z-value temperature dynamics (dF0/dt = 10^((T - 121.11)/10)).
   - VHP gaseous phase equilibrium and Clausius-Clapeyron saturation margin calculation to prevent droplet condensation during dry preform sterilization.
   - Isolator differential pressure dynamic Bernoulli orifice air balance and laminar HEPA face velocity regulator.
   - High-speed electromagnetic induction flowmeter Faraday Law velocity integration with 3-stage electronic cam valve profile (fast open, bulk fill, deceleration taper, anti-drip snifting cutoff).
   - High-speed bottle capping servo torque-angle derivative observer with thread engagement and plastic yield detection.
4. Discrete 8x8 State-Space & Receding-Horizon Model Predictive Control (MPC):
   - Discrete 8x8 state-space propagation (x[k+1] = A x[k] + B u[k], y[k] = C x[k] + D u[k]) at Ts = 2 ms.
   - Receding-horizon quadratic cost functional penalizing angular speed tracking, pitch position deviation, filling volumetric error, VHP concentration drift, isolator differential pressure drop, sterile zone temperature error, bottle meniscus stability, and capping torque error.
   - Projected Gradient Descent (PGD) with physical actuator box saturation and dynamic slew rate limiters.
5. Deterministic 14-Stage Operational Finite State Machine (FSM):
   0: STANDBY_UNINITIALIZED
   1: CIP_PRE_RINSE_AMBIENT_WFI
   2: CIP_CAUSTIC_CIRCULATION_HOT_NAOH
   3: CIP_INTERMEDIATE_RINSE_WFI
   4: CIP_ACID_CIRCULATION_HNO3
   5: CIP_FINAL_RINSE_CONDUCTIVITY_VERIFY
   6: SIP_SUPERHEATED_STEAM_STERILIZATION
   7: STERILE_AIR_COOL_DOWN_LAMINAR_FLOW
   8: VHP_DEHUMIDIFICATION_PRE_CONDITIONING
   9: VHP_GASEOUS_INJECTION_AND_EXPOSURE
   10: HOT_STERILE_AIR_DESORPTION_AERATION
   11: OVERPRESSURE_BARRIER_LOCK_AND_CAM_SYNC
   12: CONTINUOUS_ASEPTIC_PRODUCTION
   13: CONTROLLED_PRODUCTION_RAMPDOWN_PURGE
   14: EMERGENCY_STERILITY_BREACH_ABORT
6. ISA-18.2 Multi-Tiered Alarm Hierarchy:
   - 5-tier alarm hierarchy (HH, H, L, LL, Rate of Change) with clearance deadbands and bit-packed DWORD status/diagnostic words.
7. Extreme Token Density & Code Completeness:
   - Zero summaries, zero placeholders, zero '// ... rest of code'.
   - 100% exact parity: Every IF must have END_IF;, every CASE must have END_CASE;, every FOR must have END_FOR;.
   - Structured Text must be 75,000 to 125,000+ characters of pristine, industrial Structured Text."""

    raw_code = generate_code()
    assistant_content = f"```iec-st\n{raw_code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    agent_id = uuid.uuid4().hex[:8]
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "swarm_raw")
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"agent_{agent_id}.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Dataset successfully written to: {filename}")
    print(f"Assistant content length: {len(assistant_content)} characters")
    return filename

if __name__ == "__main__":
    fn = save()
