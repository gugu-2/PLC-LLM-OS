import json, uuid, os

prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\nYour specific domain is: Flue Gas Desulfurization (FGD) System.\nTask: Invent a highly complex control scenario for this domain (e.g., limestone slurry density loops, absorber spray header sequencing, and gypsum dewatering hydrocyclones).\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

iec_st_code = """FUNCTION_BLOCK FB_FGD_System_Control
VAR_INPUT
    rFlueGasInletFlow       : REAL; (* kg/s *)
    rFlueGasInletSO2        : REAL; (* ppm *)
    rFlueGasOutletSO2       : REAL; (* ppm *)
    rAbsorberLevel          : REAL; (* % *)
    rAbsorberpH             : REAL; (* pH *)
    rSlurryDensity          : REAL; (* kg/m3 *)
    bStartCommand           : BOOL;
    bEmergencyStop          : BOOL;
END_VAR

VAR_OUTPUT
    rLimestoneFeedRate      : REAL; (* kg/h *)
    bSprayHeader1_Cmd       : BOOL;
    bSprayHeader2_Cmd       : BOOL;
    bSprayHeader3_Cmd       : BOOL;
    bSprayHeader4_Cmd       : BOOL;
    bOxidationBlower_Cmd    : BOOL;
    bHydrocycloneFeedPump   : BOOL;
    rHydrocycloneValve      : REAL; (* % *)
    bSystemReady            : BOOL;
    bAlarm                  : BOOL;
    iAlarmCode              : INT;
END_VAR

VAR
    rTargetSO2              : REAL := 50.0; (* ppm *)
    rTargetpH               : REAL := 5.5;
    rTargetDensity          : REAL := 1150.0; (* kg/m3 *)
    
    (* PI Controller variables for pH (Limestone Feed) *)
    rError_pH               : REAL;
    rIntegral_pH            : REAL;
    Kp_pH                   : REAL := 120.0;
    Ki_pH                   : REAL := 5.0;
    
    (* Density control for hydrocyclones *)
    rError_Density          : REAL;
    
    (* State machine variables *)
    iState                  : INT := 0;
    tSprayTimer             : TIME := T#0s;
    bHeadersActive          : BOOL := FALSE;
END_VAR

(*
    FLUE GAS DESULFURIZATION (FGD) COMPLEX CONTROL ALGORITHM
    - pH-based limestone slurry feed control
    - Staged spray header activation based on SO2 load
    - Gypsum dewatering density management
*)

IF bEmergencyStop THEN
    iState := 99;
END_IF;

CASE iState OF
    0: (* Standby *)
        rLimestoneFeedRate := 0.0;
        bSprayHeader1_Cmd := FALSE;
        bSprayHeader2_Cmd := FALSE;
        bSprayHeader3_Cmd := FALSE;
        bSprayHeader4_Cmd := FALSE;
        bOxidationBlower_Cmd := FALSE;
        bHydrocycloneFeedPump := FALSE;
        bSystemReady := TRUE;
        bAlarm := FALSE;
        iAlarmCode := 0;
        
        IF bStartCommand THEN
            iState := 10;
            bSystemReady := FALSE;
        END_IF;
        
    10: (* Startup Sequence: Start Oxidation Blowers *)
        bOxidationBlower_Cmd := TRUE;
        (* Assume blowers reach operating state instantly for this block *)
        iState := 20;
        
    20: (* Startup Sequence: Initialize Base Spray Headers *)
        bSprayHeader1_Cmd := TRUE;
        bSprayHeader2_Cmd := TRUE;
        iState := 30;
        
    30: (* Continuous Control Loop *)
        (* 1. Limestone Feed Control (pH Loop) *)
        rError_pH := rTargetpH - rAbsorberpH;
        rIntegral_pH := rIntegral_pH + (rError_pH * 0.1); (* Assuming 100ms task rate *)
        
        (* Anti-windup *)
        IF rIntegral_pH > 5000.0 THEN rIntegral_pH := 5000.0; END_IF;
        IF rIntegral_pH < -1000.0 THEN rIntegral_pH := -1000.0; END_IF;
        
        rLimestoneFeedRate := (Kp_pH * rError_pH) + (Ki_pH * rIntegral_pH);
        IF rLimestoneFeedRate < 0.0 THEN rLimestoneFeedRate := 0.0; END_IF;
        IF rLimestoneFeedRate > 10000.0 THEN rLimestoneFeedRate := 10000.0; END_IF;
        
        (* 2. Spray Header Sequencing (SO2 Load Management) *)
        IF rFlueGasOutletSO2 > (rTargetSO2 * 1.2) THEN
            bSprayHeader3_Cmd := TRUE;
            IF rFlueGasOutletSO2 > (rTargetSO2 * 1.5) THEN
                bSprayHeader4_Cmd := TRUE;
            END_IF;
        ELSIF rFlueGasOutletSO2 < (rTargetSO2 * 0.8) THEN
            bSprayHeader4_Cmd := FALSE;
            IF rFlueGasOutletSO2 < (rTargetSO2 * 0.5) THEN
                bSprayHeader3_Cmd := FALSE;
            END_IF;
        END_IF;
        
        (* 3. Gypsum Dewatering (Density Control Loop) *)
        rError_Density := rSlurryDensity - rTargetDensity;
        IF rError_Density > 20.0 THEN
            bHydrocycloneFeedPump := TRUE;
            rHydrocycloneValve := 50.0 + (rError_Density * 0.5);
            IF rHydrocycloneValve > 100.0 THEN rHydrocycloneValve := 100.0; END_IF;
        ELSIF rError_Density < -10.0 THEN
            rHydrocycloneValve := 0.0;
            bHydrocycloneFeedPump := FALSE;
        END_IF;
        
        (* 4. Alarm Monitoring *)
        IF rAbsorberLevel > 85.0 THEN
            bAlarm := TRUE;
            iAlarmCode := 101; (* High Level Alarm *)
        ELSIF rAbsorberLevel < 15.0 THEN
            bAlarm := TRUE;
            iAlarmCode := 102; (* Low Level Alarm *)
        END_IF;
        
    99: (* Emergency Shutdown Sequence *)
        rLimestoneFeedRate := 0.0;
        bSprayHeader1_Cmd := FALSE;
        bSprayHeader2_Cmd := FALSE;
        bSprayHeader3_Cmd := FALSE;
        bSprayHeader4_Cmd := FALSE;
        bOxidationBlower_Cmd := FALSE;
        bHydrocycloneFeedPump := FALSE;
        rHydrocycloneValve := 0.0;
        bAlarm := TRUE;
        iAlarmCode := 999;
        
        IF NOT bEmergencyStop AND NOT bStartCommand THEN
            iState := 0;
        END_IF;
END_CASE;
END_FUNCTION_BLOCK
"""

response_content = f"```iec-st\n{iec_st_code}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response_content}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
file_path = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

print(file_path)
