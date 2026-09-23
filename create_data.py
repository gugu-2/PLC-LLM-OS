import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V5 Persona: a 60+ years experienced God-Tier PLC Architect & Cyber-Physical Systems Post-Doc. 
Your logic must include advanced State-Space Modeling, Model Predictive Control (MPC) concepts, Non-Linear PID with Anti-Windup, and extreme multi-layer hardware safety matrices. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Mega-Scale Particle Accelerator Radio Frequency Quadrupole (RFQ) Cavity Tuning and Beam Emittance**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Accelerator_RFQTuning\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Mega-Scale Particle Accelerator Radio Frequency Quadrupole (RFQ) Cavity Tuning and Beam Emittance"""

code = """```iec-st
FUNCTION_BLOCK FB_MegaScale_RFQ_CavityTuning_EmittanceControl
VAR_INPUT
    (* Safety and Enable Signals *)
    bSystemEnable           : BOOL;     (* Main activation signal for the RFQ control matrix *)
    bEmergencyStop          : BOOL;     (* Ultra-fast hardwired SIL-4 safety interlock OK signal *)
    bBeamPermitSignal       : BOOL;     (* Multi-facility beam permit signal (BPS) *)
    bCoolingSystemOK        : BOOL;     (* Cryogenic and water cooling systems nominal *)
    bVacuumStatusOK         : BOOL;     (* Ultra-high vacuum (UHV) sensors confirm operating pressure *)
    bRfAmplifierReady       : BOOL;     (* Klystron/Solid-state RF amplifier readiness status *)
    
    (* Process Variables (Sensors) *)
    rCavityResonanceFreq    : REAL;     (* Measured cavity resonance frequency [MHz] *)
    rForwardRfPower         : REAL;     (* Forward RF power to the cavity [kW] *)
    rReflectedRfPower       : REAL;     (* Reflected RF power from the cavity [kW] *)
    rCavityWallTempMain     : REAL;     (* Main cavity wall temperature (PT100) [deg C] *)
    rVaneVoltageProbe1      : REAL;     (* Measured voltage at vane 1 pickup [kV] *)
    rVaneVoltageProbe2      : REAL;     (* Measured voltage at vane 2 pickup [kV] *)
    rBeamCurrentInput       : REAL;     (* Input beam current measured by ACCT [mA] *)
    rBeamCurrentOutput      : REAL;     (* Output beam current measured by FCT [mA] *)
    
    (* Setpoints and Configuration *)
    rTargetFrequency        : REAL;     (* Target operating frequency for the RFQ [MHz] *)
    rTargetVaneVoltage      : REAL;     (* Desired vane voltage profile [kV] *)
    rTunerPositionLimits    : REAL;     (* Absolute physical limits for mechanical tuners [mm] *)
END_VAR

VAR_OUTPUT
    (* Status and Diagnostics *)
    bSystemReady            : BOOL;     (* Control system initialized and tracking targets *)
    bBeamInjectionPermit    : BOOL;     (* Signal to ion source / LEBT to inject beam *)
    bCriticalAlarm          : BOOL;     (* Indicates a catastrophic failure requiring abort *)
    iOperationState         : INT;      (* Current state machine step enumeration *)
    
    (* Control Signals (Actuators) *)
    rMotorTuner1Position    : REAL;     (* Commanded position for main resonance tuner [mm] *)
    rMotorTuner2Position    : REAL;     (* Commanded position for symmetry/tilt tuner [mm] *)
    rRfDriveAmplitude       : REAL;     (* LLRF amplitude drive setpoint [0-100%] *)
    rRfDrivePhase           : REAL;     (* LLRF phase drive setpoint [degrees] *)
    rCoolingValvePosition   : REAL;     (* Cooling water proportional valve position [0-100%] *)
    
    (* Telemetry *)
    rCalculatedEmittance    : REAL;     (* Real-time estimated beam emittance [pi mm mrad] *)
    rFieldFlatnessError     : REAL;     (* Calculated error in longitudinal field flatness [%] *)
END_VAR

VAR
    (* Internal State Variables *)
    iState                  : INT := 0; (* Main State Machine: 0=Init, 10=Standby, 20=Tune, 30=RF_On, 40=Beam_On, 99=Fault *)
    tStateTimer             : TON;
    tFaultTimer             : TON;
    
    (* Non-Linear PID with Anti-Windup (Tuner Control) *)
    rTunerKp                : REAL := 125.5;
    rTunerKi                : REAL := 18.2;
    rTunerKd                : REAL := 4.5;
    rTunerIntegral          : REAL := 0.0;
    rTunerPrevError         : REAL := 0.0;
    rFreqError              : REAL;
    rDerivative             : REAL;
    rPidOutput              : REAL;
    
    (* Model Predictive Control (MPC) Matrices (Simplified State-Space) *)
    rStateMatrixA_11        : REAL := 0.985;
    rStateMatrixA_12        : REAL := 0.015;
    rInputMatrixB_1         : REAL := 0.042;
    rPredictedState         : REAL;
    
    (* Safety and Fault Tracking *)
    bReflectedPowerHigh     : BOOL;
    bVoltageImbalance       : BOOL;
    
    (* Physical Constants *)
    C_SPEED_OF_LIGHT        : REAL := 299792458.0; (* m/s *)
END_VAR

(* =========================================================================
   === MAIN CONTROL LOGIC: MEGASCALE RFQ TUNING AND EMITTANCE MANAGEMENT ===
   ========================================================================= *)

(* 1. SIL-4 Hardware Safety Matrix & Interlocks *)
IF NOT bEmergencyStop OR NOT bCoolingSystemOK OR NOT bVacuumStatusOK THEN
    (* Immediate catastrophic abort *)
    bSystemReady := FALSE;
    bBeamInjectionPermit := FALSE;
    bCriticalAlarm := TRUE;
    rRfDriveAmplitude := 0.0;
    rMotorTuner1Position := 0.0;
    rMotorTuner2Position := 0.0;
    iState := 99; (* Transition to Hard Fault State *)
    RETURN;
END_IF;

(* 2. Reflected Power and Voltage Symmetry Protection *)
bReflectedPowerHigh := (rReflectedRfPower > (0.15 * rForwardRfPower));
bVoltageImbalance := (ABS(rVaneVoltageProbe1 - rVaneVoltageProbe2) > (0.05 * rTargetVaneVoltage));

IF bReflectedPowerHigh OR bVoltageImbalance THEN
    tFaultTimer(IN := TRUE, PT := T#50MS);
    IF tFaultTimer.Q THEN
        bCriticalAlarm := TRUE;
        bBeamInjectionPermit := FALSE;
        rRfDriveAmplitude := 0.0;
        iState := 99;
    END_IF;
ELSE
    tFaultTimer(IN := FALSE);
    bCriticalAlarm := FALSE;
END_IF;

(* 3. Emittance and Field Flatness Estimation (Telemetry) *)
(* Emittance growth is modeled based on transmission efficiency and field asymmetry *)
IF rBeamCurrentInput > 0.0 THEN
    rCalculatedEmittance := 0.25 * (1.0 + (1.0 - (rBeamCurrentOutput / rBeamCurrentInput))) * (1.0 + ABS(rVaneVoltageProbe1 - rVaneVoltageProbe2)/rTargetVaneVoltage);
ELSE
    rCalculatedEmittance := 0.0;
END_IF;
rFieldFlatnessError := ((rVaneVoltageProbe1 + rVaneVoltageProbe2) / 2.0) - rTargetVaneVoltage;

(* 4. State-Space MPC and State Machine Operations *)
CASE iState OF
    0: (* INITIALIZATION / COLD START *)
        bSystemReady := FALSE;
        bBeamInjectionPermit := FALSE;
        rMotorTuner1Position := 0.0;
        rMotorTuner2Position := 0.0;
        rRfDriveAmplitude := 0.0;
        
        IF bSystemEnable AND bRfAmplifierReady THEN
            iState := 10;
        END_IF;
        
    10: (* STANDBY / THERMAL STABILIZATION *)
        (* Engage cooling proportional control based on cavity wall temperature *)
        rCoolingValvePosition := (rCavityWallTempMain - 20.0) * 5.0; 
        IF rCoolingValvePosition > 100.0 THEN rCoolingValvePosition := 100.0; END_IF;
        IF rCoolingValvePosition < 0.0 THEN rCoolingValvePosition := 0.0; END_IF;
        
        tStateTimer(IN := TRUE, PT := T#10S);
        IF tStateTimer.Q THEN
            tStateTimer(IN := FALSE);
            iState := 20;
        END_IF;
        
    20: (* RESONANCE TUNING (NON-LINEAR PID WITH ANTI-WINDUP) *)
        rFreqError := rTargetFrequency - rCavityResonanceFreq;
        
        (* Proportional term with non-linear scheduling near resonance *)
        IF ABS(rFreqError) < 0.05 THEN
            rPidOutput := (rTunerKp * 0.5) * rFreqError;
        ELSE
            rPidOutput := rTunerKp * rFreqError;
        END_IF;
        
        (* Integral term with clamping (Anti-Windup) *)
        rTunerIntegral := rTunerIntegral + (rFreqError * 0.01); (* Assuming 10ms cycle *)
        IF rTunerIntegral > 10.0 THEN rTunerIntegral := 10.0; END_IF;
        IF rTunerIntegral < -10.0 THEN rTunerIntegral := -10.0; END_IF;
        rPidOutput := rPidOutput + (rTunerKi * rTunerIntegral);
        
        (* Derivative term *)
        rDerivative := (rFreqError - rTunerPrevError) / 0.01;
        rPidOutput := rPidOutput + (rTunerKd * rDerivative);
        rTunerPrevError := rFreqError;
        
        (* Apply output to tuner motors *)
        rMotorTuner1Position := rPidOutput;
        rMotorTuner2Position := rPidOutput * -0.5; (* Opposing tuner for symmetry control *)
        
        (* Limit mechanical travel *)
        IF rMotorTuner1Position > rTunerPositionLimits THEN rMotorTuner1Position := rTunerPositionLimits; END_IF;
        IF rMotorTuner1Position < -rTunerPositionLimits THEN rMotorTuner1Position := -rTunerPositionLimits; END_IF;
        
        IF ABS(rFreqError) < 0.01 THEN
            tStateTimer(IN := TRUE, PT := T#3S);
            IF tStateTimer.Q THEN
                tStateTimer(IN := FALSE);
                iState := 30;
            END_IF;
        ELSE
            tStateTimer(IN := FALSE);
        END_IF;
        
    30: (* RF POWER RAMP-UP (STATE-SPACE PREDICTION) *)
        bSystemReady := TRUE;
        
        (* Simple MPC prediction for RF Amplitude based on voltage error *)
        rPredictedState := (rStateMatrixA_11 * rVaneVoltageProbe1) + (rInputMatrixB_1 * rRfDriveAmplitude);
        IF rPredictedState < rTargetVaneVoltage THEN
            rRfDriveAmplitude := rRfDriveAmplitude + 1.5; (* Ramp rate *)
        ELSE
            rRfDriveAmplitude := rRfDriveAmplitude - 0.5;
        END_IF;
        
        IF rRfDriveAmplitude > 100.0 THEN rRfDriveAmplitude := 100.0; END_IF;
        
        IF ABS(rVaneVoltageProbe1 - rTargetVaneVoltage) < (0.01 * rTargetVaneVoltage) THEN
            IF bBeamPermitSignal THEN
                iState := 40;
            END_IF;
        END_IF;
        
    40: (* BEAM ON (ACTIVE BEAM LOADING COMPENSATION) *)
        bBeamInjectionPermit := TRUE;
        
        (* Feedforward compensation for beam loading based on input current *)
        rRfDriveAmplitude := rRfDriveAmplitude + (rBeamCurrentInput * 0.05);
        IF rRfDriveAmplitude > 100.0 THEN rRfDriveAmplitude := 100.0; END_IF;
        
        IF NOT bBeamPermitSignal OR NOT bSystemEnable THEN
            bBeamInjectionPermit := FALSE;
            iState := 30;
        END_IF;
        
    99: (* HARD FAULT / LATCH *)
        bSystemReady := FALSE;
        bBeamInjectionPermit := FALSE;
        rRfDriveAmplitude := 0.0;
        
        (* Require manual reset via bSystemEnable cycle *)
        IF NOT bSystemEnable AND NOT bEmergencyStop THEN
            iState := 0;
        END_IF;
        
    ELSE
        iState := 99; (* Unhandled state fallthrough to fault *)
END_CASE;

iOperationState := iState;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}, f, ensure_ascii=False)
print(f"Saved to {filename}")
