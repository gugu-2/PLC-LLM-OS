import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: EV Battery Hydrometallurgical Recycling.
Task: Invent a highly complex control scenario for this domain (e.g., lithium leaching acid pH cascades, solvent extraction mixer-settlers, and nickel-cobalt precipitation).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

code = """```iec-st
FUNCTION_BLOCK FB_EV_Battery_Hydro_Recycling
TITLE = 'EV Battery Hydrometallurgical Recycling Control'
VERSION : '1.0'
AUTHOR : 'Lumina Swarm'

VAR_INPUT
    rLeach_Vat_pH              : REAL;   (* Process variable: Current pH in the acid leaching vat *)
    rLeach_Vat_Temp            : REAL;   (* Process variable: Temperature in the leaching vat [degC] *)
    rAcid_Flow_Feed_PV         : REAL;   (* Process variable: Actual acid flow rate into leaching vat [L/min] *)
    bStart_Extraction          : BOOL;   (* Command to start the solvent extraction phase *)
    rSolvent_Ratio             : REAL;   (* Desired ratio of organic to aqueous phase *)
    rMixer_Speed_PV            : REAL;   (* Process variable: Actual speed of the mixer-settler motor [RPM] *)
    rPrecipitation_Vat_Temp    : REAL;   (* Process variable: Temperature in the Ni-Co precipitation vat [degC] *)
    rPrecipitation_pH          : REAL;   (* Process variable: pH in the Ni-Co precipitation vat *)
    rNiCo_Concentration        : REAL;   (* Process variable: Real-time inline measurement of Ni/Co [g/L] *)
    bEmergency_Stop            : BOOL;   (* Global emergency stop interlock *)
    bReset_Alarm               : BOOL;   (* Acknowledge and reset system alarms *)
END_VAR

VAR_OUTPUT
    rAcid_Dosing_Valve_SP      : REAL;   (* Setpoint output: Acid dosing valve position [0.0 - 100.0%] *)
    rMixer_Speed_SP            : REAL;   (* Setpoint output: Mixer-settler motor speed [RPM] *)
    bPhase_Separator_Pump      : BOOL;   (* Command output: Start/stop aqueous phase transfer pump *)
    rAlkali_Dosing_Valve_SP    : REAL;   (* Setpoint output: Alkali (NaOH) dosing valve [0.0 - 100.0%] *)
    rLeach_Heater_Output       : REAL;   (* Setpoint output: Steam valve or electric heater [0.0 - 100.0%] *)
    rPrecip_Heater_Output      : REAL;   (* Setpoint output: Precipitation vat heater [0.0 - 100.0%] *)
    bSystem_Alarm              : BOOL;   (* System wide alarm indicator for HMI / SCADA *)
    iActive_Stage              : INT;    (* Current operational stage: 0=Halt, 1=Leaching, 2=SX, 3=Precipitation *)
END_VAR

VAR
    (* --- Target Setpoints --- *)
    rLeach_pH_SP               : REAL := 1.5;   (* Deep discharge/leach target pH *)
    rLeach_Temp_SP             : REAL := 80.0;  (* Optimal leaching temperature for Li/Co extraction *)
    rPrecip_pH_SP              : REAL := 4.2;   (* Target pH for selective precipitation of transition metals *)
    rPrecip_Temp_SP            : REAL := 60.0;  (* Precipitation temperature target *)
    
    (* --- Control Structures (PID / Timers) --- *)
    fb_Leach_pH_PID            : PID_Compact;   (* Standard IEC PID block for acid leaching *)
    fb_Leach_Temp_PID          : PID_Compact;   (* Standard IEC PID block for leaching heat control *)
    tMixer_Stage_Timer         : TON;           (* Emulsion mixing duration timer *)
    tSettler_Stage_Timer       : TON;           (* Gravity phase separation timer *)
    
    (* --- State Machine & Internal Variables --- *)
    iSX_Step                   : INT := 0;      (* Solvent Extraction internal state machine index *)
    bExtraction_Active         : BOOL := FALSE;
    bPrecipitation_Active      : BOOL := FALSE;
    
    (* --- Safety & Limits --- *)
    rMax_Acid_Valve_Limit      : REAL := 95.0;  (* Avoid fully saturating the dosing valve *)
    rMin_Mixer_Speed_Limit     : REAL := 150.0; (* Minimum required agitation speed *)
    rMax_Mixer_Speed_Limit     : REAL := 850.0; (* Maximum allowable impeller speed to avoid shear degradation *)
    rAlkali_Gain               : REAL := 25.0;  (* Proportional gain for pH neutralization step *)
END_VAR

(* =====================================================================
   MAIN CONTROL EXECUTION
   Domain: EV Battery Hydrometallurgical Recycling
   Processes: Leaching, Solvent Extraction (SX), Precipitation
   ===================================================================== *)

(* 1. GLOBAL EMERGENCY STOP & INTERLOCK CHECK *)
IF bEmergency_Stop THEN
    rAcid_Dosing_Valve_SP   := 0.0;
    rMixer_Speed_SP         := 0.0;
    bPhase_Separator_Pump   := FALSE;
    rAlkali_Dosing_Valve_SP := 0.0;
    rLeach_Heater_Output    := 0.0;
    rPrecip_Heater_Output   := 0.0;
    bSystem_Alarm           := TRUE;
    iActive_Stage           := 0;
    iSX_Step                := 0;
    RETURN; (* Bypass all further control logic safely *)
END_IF;

IF bReset_Alarm AND NOT bEmergency_Stop THEN
    bSystem_Alarm := FALSE;
END_IF;

(* 2. STAGE 1: BLACK MASS ACID LEACHING *)
(* We default to active stage 1 unless subsequent stages assert control *)
IF NOT bExtraction_Active AND NOT bPrecipitation_Active THEN
    iActive_Stage := 1;
END_IF;

(* Leaching pH Control via Cascade (simplified PID call for ST representation) *)
fb_Leach_pH_PID(
    EN := (iActive_Stage = 1),
    SP := rLeach_pH_SP,
    PV := rLeach_Vat_pH,
    Kp := 3.2,
    Tn := 15.0,
    Tv := 0.0,
    ReverseActing := TRUE, (* Acid lowers pH *)
    OUT => rAcid_Dosing_Valve_SP
);

(* Hard limit the dosing valve to prevent overshoot transients *)
IF rAcid_Dosing_Valve_SP > rMax_Acid_Valve_Limit THEN
    rAcid_Dosing_Valve_SP := rMax_Acid_Valve_Limit;
ELSIF rAcid_Dosing_Valve_SP < 0.0 THEN
    rAcid_Dosing_Valve_SP := 0.0;
END_IF;

(* Leaching Temperature Control *)
fb_Leach_Temp_PID(
    EN := (iActive_Stage = 1),
    SP := rLeach_Temp_SP,
    PV := rLeach_Vat_Temp,
    Kp := 5.0,
    Tn := 60.0,
    Tv := 12.0,
    ReverseActing := FALSE,
    OUT => rLeach_Heater_Output
);

(* 3. STAGE 2: SOLVENT EXTRACTION (MIXER-SETTLER) *)
(* Starts conditionally via operator or supervisory sequence command *)
IF bStart_Extraction AND iActive_Stage = 1 THEN
    bExtraction_Active := TRUE;
    iActive_Stage := 2;
END_IF;

IF bExtraction_Active THEN
    CASE iSX_Step OF
        0:  (* Initialization *)
            rMixer_Speed_SP := 0.0;
            bPhase_Separator_Pump := FALSE;
            iSX_Step := 1;
            
        1:  (* Intensive Emulsion Mixing Phase *)
            rMixer_Speed_SP := rMin_Mixer_Speed_Limit + (rSolvent_Ratio * 150.0);
            
            IF rMixer_Speed_SP > rMax_Mixer_Speed_Limit THEN
                rMixer_Speed_SP := rMax_Mixer_Speed_Limit;
            END_IF;
            
            tMixer_Stage_Timer(IN := TRUE, PT := T#45M); (* 45 min residence time *)
            
            IF tMixer_Stage_Timer.Q THEN
                tMixer_Stage_Timer(IN := FALSE);
                rMixer_Speed_SP := 0.0;
                iSX_Step := 2;
            END_IF;
            
        2:  (* Gravity Settling / Phase Separation Phase *)
            tSettler_Stage_Timer(IN := TRUE, PT := T#120M); (* 2 hours for clean organic/aqueous split *)
            
            IF tSettler_Stage_Timer.Q THEN
                tSettler_Stage_Timer(IN := FALSE);
                bPhase_Separator_Pump := TRUE;
                iSX_Step := 3;
            END_IF;
            
        3:  (* Aqueous Transfer to Precipitation Stage *)
            bPhase_Separator_Pump := TRUE;
            
            (* Transition criteria: Adequate transfer based on concentration sensor or low level switch *)
            IF rNiCo_Concentration > 45.0 THEN
                iSX_Step := 0;
                bPhase_Separator_Pump := FALSE;
                bExtraction_Active := FALSE;
                bPrecipitation_Active := TRUE;
            END_IF;
    END_CASE;
END_IF;

(* 4. STAGE 3: NICKEL-COBALT SELECTIVE PRECIPITATION *)
IF bPrecipitation_Active THEN
    iActive_Stage := 3;
    
    (* Proportional Alkali (NaOH) Dosing to reach Precipitation pH *)
    IF rPrecipitation_pH < rPrecip_pH_SP THEN
        rAlkali_Dosing_Valve_SP := (rPrecip_pH_SP - rPrecipitation_pH) * rAlkali_Gain;
    ELSE
        rAlkali_Dosing_Valve_SP := 0.0;
    END_IF;
    
    (* Constrain alkali output *)
    IF rAlkali_Dosing_Valve_SP > 100.0 THEN
        rAlkali_Dosing_Valve_SP := 100.0;
    ELSIF rAlkali_Dosing_Valve_SP < 0.0 THEN
        rAlkali_Dosing_Valve_SP := 0.0;
    END_IF;
    
    (* Simple Proportional Heat Control for Precipitation Kinetics *)
    IF rPrecipitation_Vat_Temp < rPrecip_Temp_SP THEN
        rPrecip_Heater_Output := (rPrecip_Temp_SP - rPrecipitation_Vat_Temp) * 10.0;
        IF rPrecip_Heater_Output > 100.0 THEN rPrecip_Heater_Output := 100.0; END_IF;
    ELSE
        rPrecip_Heater_Output := 0.0;
    END_IF;
    
    (* Precipitation Quality Control Alarms *)
    IF (rPrecipitation_Vat_Temp > rPrecip_Temp_SP + 5.0) OR 
       (rPrecipitation_pH > rPrecip_pH_SP + 0.5) THEN
        bSystem_Alarm := TRUE;
    END_IF;
    
END_IF;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

print(f"Saved to {filename}")
