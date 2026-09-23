import json
import uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V5 Persona: a 60+ years experienced God-Tier PLC Architect & Cyber-Physical Systems Post-Doc. 
Your logic must include advanced State-Space Modeling, Model Predictive Control (MPC) concepts, Non-Linear PID with Anti-Windup, and extreme multi-layer hardware safety matrices. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Mega-Scale Underground Pumped Hydroelectric Storage (UPHS) Reversible Pump-Turbine Cavitation Margin**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. This MUST be drastically better, more advanced, and longer than previous V4 iterations.

CRITICAL RULES - READ EVERY LINE:
1. CODE FENCE: Use TRIPLE backticks + iec-st. EXACTLY like this:
   ```iec-st
   (your code here)
   ```
   NEVER use a single backtick `iec-st. ALWAYS use triple backticks.
2. REQUIRED IEC 61131-3 STRUCTURE (all 5 mandatory):
   a. FUNCTION_BLOCK FB_<Name>   <- first line of code, always
   b. VAR_INPUT ... END_VAR      <- min 6 typed inputs with comments
   c. VAR_OUTPUT ... END_VAR     <- min 5 typed outputs with comments
   d. At least one END_IF; or END_CASE;  <- control logic required
   e. END_FUNCTION_BLOCK         <- last line of code, always
3. LENGTH: The assistant content MUST be >= 2500 characters total. Make it incredibly massive and rigorous.
4. SAVE to isolated file using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_UPHS_ReversiblePumpTurbine\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is ```iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT & VAR_OUTPUT sections
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ```
   [ ] Total chars >= 2500
6. REPLY with: EVOLUTION COMPLETE: Mega-Scale Underground Pumped Hydroelectric Storage (UPHS) Reversible Pump-Turbine Cavitation Margin"""

code = """```iec-st
FUNCTION_BLOCK FB_UPHS_ReversiblePumpTurbine
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System enable signal for the pump-turbine unit *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal; Hardwired emergency stop *)
    rSuctionPressure        : REAL;     (* Measured pressure at the draft tube or suction side [Pa] *)
    rVaporPressure          : REAL;     (* Vapor pressure of the working fluid at the current operating temperature [Pa] *)
    rWaterVelocity          : REAL;     (* Fluid velocity at the runner inlet/outlet depending on mode [m/s] *)
    rReferenceElevation     : REAL;     (* Reference elevation of the machine relative to tailwater [m] *)
    rFluidDensity           : REAL;     (* Density of the water, variable with temperature [kg/m^3] *)
    rGuideVaneOpening       : REAL;     (* Current guide vane opening feedback [0.0 - 1.0] *)
    rRotorSpeed             : REAL;     (* Mechanical rotational speed of the pump-turbine [RPM] *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* System ready for operation status *)
    rControlOutput          : REAL;     (* Control signal for guide vane actuator (MPC and Non-Linear PID adjusted) *)
    bAlarm                  : BOOL;     (* Cavitation fault alarm output - triggers interlock *)
    rCalculatedNPSH         : REAL;     (* Net Positive Suction Head Available (NPSHa) calculated [m] *)
    rCavitationMargin       : REAL;     (* Computed safety margin against cavitation inception [m] *)
    bCavitationWarning      : BOOL;     (* Warning threshold: Margin is approaching critical operational limits *)
END_VAR
VAR
    (* Internal state variables and configuration parameters *)
    iState                  : INT := 0; (* Internal state machine variable for process tracking *)
    tTimer                  : TON;      (* Timer for state transitions and filter delays *)
    tFaultTimer             : TON;      (* Fault persistence timer to avoid spurious trips *)
    rGravity                : REAL := 9.81; (* Acceleration due to gravity [m/s^2] *)
    rAtmosphericPressure    : REAL := 101325.0; (* Standard atmospheric pressure at elevation [Pa] *)
    rCriticalCavitationIdx  : REAL := 0.115; (* Thoma's critical cavitation parameter sigma_c *)
    rRequiredNPSH           : REAL;     (* Required NPSH based on current operating point (NPSHr) [m] *)
    rHead                   : REAL;     (* Total dynamic head across the machine [m] *)
    rIntegralError          : REAL := 0.0; (* Integral component for anti-windup PID controller *)
    rPreviousError          : REAL := 0.0; (* Previous error for derivative term computation *)
    rError                  : REAL := 0.0; (* Current tracking error *)
    
    (* Advanced State-Space and Model Predictive Control variables *)
    rModelPredictedMargin   : REAL;     (* Horizon-predicted cavitation margin [m] *)
    rAdaptiveGain           : REAL;     (* Gain scheduled based on proximity to cavitation threshold *)
    rStateObserverX1        : REAL := 0.0; (* State observer internal variable 1 (velocity derivative) *)
    rStateObserverX2        : REAL := 0.0; (* State observer internal variable 2 (pressure derivative) *)
    
    (* Filter variables *)
    rFilteredVelocity       : REAL := 0.0; (* Low-pass filtered water velocity *)
    rFilterAlpha            : REAL := 0.1; (* Smoothing factor for first-order IIR filter *)
END_VAR

(* === MAIN LOGIC === *)
(* Multi-layer Hardware Safety Matrix: Level 1 - Hardwired Emergency Stop Evaluation *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    rControlOutput := 0.0; (* Force actuators to fail-safe closed position *)
    rIntegralError := 0.0; (* Clear integral windup memory *)
    iState := 99; (* Enter terminal fault state *)
    RETURN;
END_IF;

(* Continuous Signal Filtering (First Order IIR) to reject sensor noise in high-vibration environment *)
rFilteredVelocity := rFilteredVelocity + rFilterAlpha * (rWaterVelocity - rFilteredVelocity);

(* Calculate NPSHa (Available Net Positive Suction Head) using Bernoulli's principle *)
(* NPSHa = (P_atm - P_vapor) / (rho * g) + Suction_Head - Friction_Losses_and_Kinetic *)
rCalculatedNPSH := (rAtmosphericPressure - rVaporPressure) / (rFluidDensity * rGravity) 
                   + rSuctionPressure / (rFluidDensity * rGravity) 
                   - rReferenceElevation 
                   - (0.5 * rFilteredVelocity * rFilteredVelocity) / rGravity;

(* Advanced State-Space estimation of required NPSH (NPSHr) based on Guide Vane Opening and total Dynamic Head *)
rHead := (rSuctionPressure / (rFluidDensity * rGravity)) + rReferenceElevation; 
(* NPSHr scales with operating head and non-linearly with guide vane position *)
rRequiredNPSH := rCriticalCavitationIdx * rHead * (1.0 + 0.35 * (rGuideVaneOpening * rGuideVaneOpening));

(* Compute deterministic Cavitation Margin (Margin = NPSHa - NPSHr) *)
rCavitationMargin := rCalculatedNPSH - rRequiredNPSH;

(* Model Predictive Control (MPC) Horizon Estimation for Margin Degradation *)
(* Predict future margin over a T=2s horizon based on state observer dynamics *)
rStateObserverX1 := rStateObserverX1 + 0.05 * (rFilteredVelocity - rStateObserverX1);
rModelPredictedMargin := rCavitationMargin - (rStateObserverX1 * 0.15) - (0.01 * rRotorSpeed / 60.0);

(* Core State Machine for Operational Sequence *)
CASE iState OF
    0: (* STATE: IDLE / OFF *)
        bSystemReady := FALSE;
        bAlarm := FALSE;
        bCavitationWarning := FALSE;
        rControlOutput := 0.0;
        tFaultTimer(IN := FALSE);
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* STATE: INITIALIZATION & STARTUP VALIDATION *)
        (* Ensure baseline cavitation margin is strictly safe before allowing guide vane opening *)
        IF rCavitationMargin > 8.0 AND rModelPredictedMargin > 7.5 THEN
            tTimer(IN := TRUE, PT := T#3S);
            IF tTimer.Q THEN
                tTimer(IN := FALSE);
                iState := 20;
            END_IF;
        ELSE
            (* Safety Matrix Level 2: Interlock pre-start if margin is inadequate *)
            tFaultTimer(IN := TRUE, PT := T#2S);
            IF tFaultTimer.Q THEN
                bAlarm := TRUE;
                iState := 99;
            END_IF;
        END_IF;

    20: (* STATE: ACTIVE RUNNING WITH NON-LINEAR PID ANTI-WINDUP CONTROL *)
        bSystemReady := TRUE;
        tFaultTimer(IN := FALSE);
        
        (* Evaluate Predictive Safety Margins and emit early warnings *)
        IF rCavitationMargin < 3.0 OR rModelPredictedMargin < 2.5 THEN
            bCavitationWarning := TRUE;
        ELSE
            bCavitationWarning := FALSE;
        END_IF;
        
        (* Extreme Multi-layer Hardware Safety Matrix: Level 3 - Dynamic In-Run Trip Evaluation *)
        IF rCavitationMargin < 0.5 OR rModelPredictedMargin < 0.0 THEN
            (* Cavitation is imminent or currently occurring! Trip the system immediately. *)
            bAlarm := TRUE;
            iState := 99;
        ELSE
            (* Advanced Non-Linear Control Law: Increase proportional gain as margin shrinks to act faster *)
            IF rCavitationMargin < 4.0 THEN
                rAdaptiveGain := 3.5; (* High gain for aggressive closure near cavitation limit *)
            ELSE
                rAdaptiveGain := 1.2; (* Nominal gain during normal safe operation *)
            END_IF;
            
            (* Compute error against a safe target margin of 5.0 meters *)
            rError := rCavitationMargin - 5.0;
            
            (* Anti-Windup Integral computation for flow modulation *)
            rIntegralError := rIntegralError + (rError * 0.02); (* dt ~ 0.02s assumed *)
            
            (* Strict Anti-Windup Clamping based on actuator saturation limits *)
            IF rIntegralError > 15.0 THEN
                rIntegralError := 15.0; 
            ELSIF rIntegralError < -15.0 THEN
                rIntegralError := -15.0; 
            END_IF;
            
            (* Control Output calculation (simplistic generic form: Base + P + I) *)
            (* Positive error (excess margin) allows opening, negative requires closing *)
            rControlOutput := rGuideVaneOpening + (rAdaptiveGain * 0.1 * rError) + (0.05 * rIntegralError);
            
            (* Absolute Actuator Limits Clamping *)
            IF rControlOutput > 1.0 THEN
                rControlOutput := 1.0;
            ELSIF rControlOutput < 0.0 THEN
                rControlOutput := 0.0;
            END_IF;
        END_IF;

        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    99: (* STATE: FAULT / TRIP LATCH *)
        bSystemReady := FALSE;
        rControlOutput := 0.0; (* Maintain fail-safe state *)
        bCavitationWarning := FALSE;
        
        (* Require positive manual reset sequence: Alarm cleared and Enable toggled *)
        IF NOT bAlarm AND NOT bEnable THEN
            iState := 0; 
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

import os
os.makedirs(r"C:\Users\majip\Downloads\LLM REASEARCH\data\swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"C:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print("Saved to file.")
