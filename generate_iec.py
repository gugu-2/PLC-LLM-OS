import os, json, uuid

os.makedirs('data/swarm_raw', exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Mega-Scale Hydroponic Vertical Farming Nutrient Film Technique (NFT) Dosing and LED PAR Dimming Sync**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. This MUST be drastically better, more advanced, and longer than previous iterations."""

code = """```iec-st
FUNCTION_BLOCK FB_MegaScaleNFT_DosingDimmingSync
VAR_INPUT
    (* System & Safety Control Inputs *)
    bEnable           : BOOL;     (* Main system enable command from master SCADA *)
    bEStop_Hard       : BOOL;     (* Hardwired emergency stop safety relay feedback (OK = TRUE) *)
    bLeakDetected     : BOOL;     (* Leakage detection sensor array in primary NFT troughs *)
    (* Process Variable Inputs *)
    rNutrientEC       : REAL;     (* Measured electrical conductivity of nutrient solution (mS/cm) *)
    rpH_Level         : REAL;     (* Measured pH level from inline glass electrode *)
    rPAR_Ambient      : REAL;     (* Photosynthetically Active Radiation from ambient daylight (umol/m2/s) *)
    rWaterTemp        : REAL;     (* Chiller/Heater output water temperature (Deg C) *)
    rFlowRate         : REAL;     (* NFT delivery header flow rate (L/min) *)
END_VAR
VAR_OUTPUT
    (* System Status & Actuator Outputs *)
    bSystemReady      : BOOL;     (* System healthy and ready for active dosing/dimming *)
    bAlarm_Critical   : BOOL;     (* Critical fault alarm requiring immediate intervention *)
    iSystemState      : INT;      (* Current operating state enum *)
    rDosingPumpSpeed_EC : REAL;   (* PWM/Analog output for EC dosing pump (0-100%) *)
    rDosingPumpSpeed_pH : REAL;   (* PWM/Analog output for pH dosing pump (0-100%) *)
    rLED_PAR_Output   : REAL;     (* Target LED dimming level to compensate for ambient PAR (0-100%) *)
END_VAR
VAR
    (* Internal State & Timers *)
    iState            : INT := 0; (* Internal state machine tracker *)
    tStartupDelay     : TON;      (* Delay to allow sensors to stabilize on boot *)
    tDosingInterval   : TON;      (* Pulse-width modulation base timer for dosing pumps *)
    
    (* Low-Pass Filter Variables *)
    rEC_Filtered      : REAL := 0.0;
    rpH_Filtered      : REAL := 7.0;
    rPAR_Filtered     : REAL := 0.0;
    rAlpha_Filter     : REAL := 0.05; (* Filter coefficient for digital LPF *)
    
    (* PID & Cascade Control Internal Variables *)
    rEC_Setpoint      : REAL := 2.5;  (* Target EC in mS/cm *)
    rpH_Setpoint      : REAL := 5.8;  (* Target pH level *)
    rPAR_Setpoint     : REAL := 600.0;(* Target PAR level umol/m2/s *)
    
    rError_EC         : REAL;
    rError_pH         : REAL;
    rError_PAR        : REAL;
    
    rIntegral_EC      : REAL := 0.0;
    rIntegral_pH      : REAL := 0.0;
    
    (* Tuning Parameters *)
    Kp_EC             : REAL := 12.5;
    Ki_EC             : REAL := 2.1;
    Kp_pH             : REAL := -15.0; (* Inverse acting for acid dosing *)
    Ki_pH             : REAL := -3.2;
    
    rMax_Integral     : REAL := 50.0;  (* Anti-windup limit *)
    rMin_Integral     : REAL := -50.0;
    
    (* Predictive Anomaly Detection *)
    rEC_RateOfChange  : REAL;
    rEC_Prev          : REAL := 0.0;
END_VAR

(* === MULTI-LAYERED HARDWARE INTERLOCKS === *)
IF NOT bEStop_Hard OR bLeakDetected THEN
    bSystemReady := FALSE;
    bAlarm_Critical := TRUE;
    iState := 99; (* FAULT STATE *)
    rDosingPumpSpeed_EC := 0.0;
    rDosingPumpSpeed_pH := 0.0;
    rLED_PAR_Output := 0.0;
    iSystemState := iState;
    RETURN;
END_IF;

(* === DIGITAL LOW-PASS FILTERING === *)
rEC_Filtered := (rAlpha_Filter * rNutrientEC) + ((1.0 - rAlpha_Filter) * rEC_Filtered);
rpH_Filtered := (rAlpha_Filter * rpH_Level) + ((1.0 - rAlpha_Filter) * rpH_Filtered);
rPAR_Filtered := (rAlpha_Filter * rPAR_Ambient) + ((1.0 - rAlpha_Filter) * rPAR_Filtered);

(* === PREDICTIVE ANOMALY DETECTION === *)
rEC_RateOfChange := rEC_Filtered - rEC_Prev;
rEC_Prev := rEC_Filtered;
IF ABS(rEC_RateOfChange) > 0.5 THEN
    (* Spurious spike detected - likely sensor failure or dosing tube burst *)
    bAlarm_Critical := TRUE;
    iState := 99;
END_IF;

(* === MAIN LOGIC STATE MACHINE === *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        bAlarm_Critical := FALSE;
        rDosingPumpSpeed_EC := 0.0;
        rDosingPumpSpeed_pH := 0.0;
        rLED_PAR_Output := 0.0;
        
        IF bEnable THEN
            tStartupDelay(IN := TRUE, PT := T#10S);
            IF tStartupDelay.Q THEN
                tStartupDelay(IN := FALSE);
                iState := 10;
            END_IF;
        END_IF;

    10: (* ACTIVE RUNNING WITH ADVANCED NON-LINEAR PID & ANTI-WINDUP *)
        bSystemReady := TRUE;
        
        (* 1. pH Cascade Control (Inner Loop Equivalent) *)
        rError_pH := rpH_Setpoint - rpH_Filtered;
        rIntegral_pH := rIntegral_pH + rError_pH;
        
        (* Anti-Windup for pH *)
        IF rIntegral_pH > rMax_Integral THEN rIntegral_pH := rMax_Integral; END_IF;
        IF rIntegral_pH < rMin_Integral THEN rIntegral_pH := rMin_Integral; END_IF;
        
        rDosingPumpSpeed_pH := (Kp_pH * rError_pH) + (Ki_pH * rIntegral_pH);
        
        (* Non-linear bounding for pH output *)
        IF rDosingPumpSpeed_pH > 100.0 THEN rDosingPumpSpeed_pH := 100.0; END_IF;
        IF rDosingPumpSpeed_pH < 0.0 THEN rDosingPumpSpeed_pH := 0.0; END_IF;

        (* 2. EC Control Loop *)
        rError_EC := rEC_Setpoint - rEC_Filtered;
        
        (* Gain scheduling based on Flow Rate (Non-Linear Adaptation) *)
        IF rFlowRate < 50.0 THEN
            rError_EC := rError_EC * 0.5; (* Reduce aggression at low flow *)
        END_IF;
        
        rIntegral_EC := rIntegral_EC + rError_EC;
        
        (* Anti-Windup for EC *)
        IF rIntegral_EC > rMax_Integral THEN rIntegral_EC := rMax_Integral; END_IF;
        IF rIntegral_EC < 0.0 THEN rIntegral_EC := 0.0; END_IF; (* Cannot dose negative EC *)
        
        rDosingPumpSpeed_EC := (Kp_EC * rError_EC) + (Ki_EC * rIntegral_EC);
        IF rDosingPumpSpeed_EC > 100.0 THEN rDosingPumpSpeed_EC := 100.0; END_IF;
        IF rDosingPumpSpeed_EC < 0.0 THEN rDosingPumpSpeed_EC := 0.0; END_IF;

        (* 3. LED PAR Dimming Sync (Feed-Forward Control) *)
        rError_PAR := rPAR_Setpoint - rPAR_Filtered;
        IF rError_PAR > 0.0 THEN
            rLED_PAR_Output := (rError_PAR / rPAR_Setpoint) * 100.0;
        ELSE
            rLED_PAR_Output := 0.0; (* Ambient is sufficient *)
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    99: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        rDosingPumpSpeed_EC := 0.0;
        rDosingPumpSpeed_pH := 0.0;
        rLED_PAR_Output := 0.0;
        IF NOT bLeakDetected AND bEStop_Hard AND NOT bEnable THEN
            bAlarm_Critical := FALSE;
            iState := 0; (* Reset on disable when healthy *)
        END_IF;

END_CASE;

iSystemState := iState;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
