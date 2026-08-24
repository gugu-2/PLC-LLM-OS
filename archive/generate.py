import json
import os

prompt = """You are acting as the Lead Oceanic Robotics Engineer for a Deep-Sea Mining Consortium.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Abyssal Polymetallic Nodule Harvester & Benthic Plume Mitigation Controller" (`FB_OceanMining_Harvester`).

### Technical Specifications & Engineering Rigor Required:
1. **Coanda-Effect Hydraulic Nodule Collection**:
   - Precise closed-loop control of internal water jets generating a low-pressure Coanda-effect lifting force, sucking up potato-sized Manganese/Cobalt nodules from the sediment (4,500m depth) without physically scraping the delicate abyssal seafloor.
2. **Benthic Plume Recirculation & Mitigation**:
   - Real-time acoustic Doppler turbidity monitoring of the sediment exhaust plume.
   - Active cyclonic separation within the crawler to strip out ultra-fine sediment particles, injecting them back into the seafloor trench at zero velocity rather than blasting them into the mid-water column.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, hydrodynamic mass-flow matrices, PackML states.
"""

st_code = """```iec-st
(* ==============================================================================
   Function Block: FB_OceanMining_Harvester
   Description:    Master controller for Abyssal Polymetallic Nodule Harvester
                   and Benthic Plume Mitigation System (Depth: 4,500m).
                   Integrates Coanda-effect lifting, cyclonic particle separation,
                   and ISA-88/PackML state machine.
   Standard:       IEC 61131-3 Structured Text (ST)
   Author:         Lead Oceanic Robotics Engineer
   ============================================================================== *)

TYPE E_PackML_State :
(
    eSTATE_UNDEFINED   := 0,
    eSTATE_CLEARED     := 1,
    eSTATE_STOPPED     := 2,
    eSTATE_STARTING    := 3,
    eSTATE_IDLE        := 4,
    eSTATE_SUSPENDED   := 5,
    eSTATE_EXECUTE     := 6,
    eSTATE_STOPPING    := 7,
    eSTATE_ABORTING    := 8,
    eSTATE_ABORTED     := 9,
    eSTATE_HOLDING     := 10,
    eSTATE_HELD        := 11,
    eSTATE_UNHOLDING   := 12,
    eSTATE_SUSPENDING  := 13,
    eSTATE_RESUMING    := 14,
    eSTATE_RESETTING   := 15,
    eSTATE_COMPLETING  := 16,
    eSTATE_COMPLETE    := 17
);
END_TYPE

TYPE ST_Harvester_Telemetry :
STRUCT
    fAmbientPressure_Bar    : LREAL; (* Nominally 450 Bar at 4500m *)
    fSeafloorDistance_mm    : LREAL;
    fNoduleMassFlow_kg_s    : LREAL;
    fCoandaJetPressure_kPa  : LREAL;
    fPlumeTurbidity_NTU     : LREAL;
    fInjectionVelocity_m_s  : LREAL;
END_STRUCT
END_TYPE

TYPE ST_Coanda_Matrix :
STRUCT
    fA : ARRAY[1..3, 1..3] OF LREAL; (* Hydrodynamic mass-flow coefficients *)
    fB : ARRAY[1..3] OF LREAL;       (* Lift vector *)
END_STRUCT
END_TYPE

FUNCTION_BLOCK FB_OceanMining_Harvester
VAR_INPUT
    bEnable                 : BOOL;
    bStart                  : BOOL;
    bStop                   : BOOL;
    bAbort                  : BOOL;
    
    stTelemetry             : ST_Harvester_Telemetry;
    fTargetNoduleFlow_kg_s  : LREAL := 15.0; 
    fMaxPermissibleNTU      : LREAL := 50.0; (* Plume limit *)
END_VAR

VAR_OUTPUT
    eCurrentState           : E_PackML_State := eSTATE_STOPPED;
    
    (* Coanda Lift Actuators *)
    fJetPumpCommand_RPM     : LREAL;
    fApertureValveOpen_Pct  : LREAL;
    
    (* Plume Mitigation Actuators *)
    fCyclonicSepRPM         : LREAL;
    fInjectionPumpRPM       : LREAL;
    
    bAlarmPlumeCritical     : BOOL;
    bAlarmLossOfLift        : BOOL;
END_VAR

VAR
    (* Internal PID Controllers *)
    fbCoandaLiftPID         : FB_PID;
    fbPlumeTurbidityPID     : FB_PID;
    fbInjectionVelocityPID  : FB_PID;
    
    (* Matrices *)
    stHydroMatrix           : ST_Coanda_Matrix;
    
    (* Internal State *)
    fCalculatedLift_N       : LREAL;
    fPredictedPlumeVol_m3   : LREAL;
    
    bInitializationComplete : BOOL := FALSE;
END_VAR

(* --- Matrix Initialization --- *)
IF NOT bInitializationComplete THEN
    stHydroMatrix.fA[1,1] := 1.045; stHydroMatrix.fA[1,2] := -0.012; stHydroMatrix.fA[1,3] := 0.005;
    stHydroMatrix.fA[2,1] := 0.022; stHydroMatrix.fA[2,2] :=  1.103; stHydroMatrix.fA[2,3] := -0.015;
    stHydroMatrix.fA[3,1] := 0.001; stHydroMatrix.fA[3,2] := -0.008; stHydroMatrix.fA[3,3] :=  0.998;
    bInitializationComplete := TRUE;
END_IF

(* --- PackML State Machine Evaluation --- *)
IF bAbort THEN
    eCurrentState := eSTATE_ABORTING;
ELSIF bStop AND eCurrentState <> eSTATE_ABORTING AND eCurrentState <> eSTATE_ABORTED THEN
    eCurrentState := eSTATE_STOPPING;
END_IF

CASE eCurrentState OF
    eSTATE_STOPPED:
        fJetPumpCommand_RPM := 0.0;
        fApertureValveOpen_Pct := 0.0;
        fCyclonicSepRPM := 0.0;
        fInjectionPumpRPM := 0.0;
        
        IF bStart THEN
            eCurrentState := eSTATE_STARTING;
        END_IF
        
    eSTATE_STARTING:
        (* Spool up cyclonic separator first to prevent initial plume blowout *)
        fCyclonicSepRPM := fCyclonicSepRPM + 15.0;
        IF fCyclonicSepRPM >= 3500.0 THEN
            eCurrentState := eSTATE_EXECUTE;
        END_IF
        
    eSTATE_EXECUTE:
        (* ---------------------------------------------------------
           1. Coanda-Effect Hydraulic Nodule Collection
           --------------------------------------------------------- *)
        (* Closed-loop lift control based on mass flow and altitude *)
        fbCoandaLiftPID(
            fSetpoint := fTargetNoduleFlow_kg_s,
            fProcessValue := stTelemetry.fNoduleMassFlow_kg_s,
            fKp := 4.2, fKi := 1.1, fKd := 0.5
        );
        
        (* Hydrodynamic compensation using pressure and distance *)
        fCalculatedLift_N := fbCoandaLiftPID.fOutput * stHydroMatrix.fA[1,1] + 
                             (stTelemetry.fAmbientPressure_Bar * stHydroMatrix.fA[1,2]);
                             
        fJetPumpCommand_RPM := LIMIT(0.0, fCalculatedLift_N * 12.5, 8000.0);
        
        (* Adjust aperture to maintain Coanda profile without seafloor contact *)
        IF stTelemetry.fSeafloorDistance_mm < 150.0 THEN
            fApertureValveOpen_Pct := LIMIT(0.0, fApertureValveOpen_Pct - 1.0, 100.0);
        ELSIF stTelemetry.fSeafloorDistance_mm > 250.0 THEN
            fApertureValveOpen_Pct := LIMIT(0.0, fApertureValveOpen_Pct + 0.5, 100.0);
        END_IF

        (* ---------------------------------------------------------
           2. Benthic Plume Recirculation & Mitigation
           --------------------------------------------------------- *)
        (* Acoustic Doppler turbidity monitoring loop *)
        fbPlumeTurbidityPID(
            fSetpoint := fMaxPermissibleNTU * 0.8, (* Target 20% margin below max *)
            fProcessValue := stTelemetry.fPlumeTurbidity_NTU,
            fKp := 8.5, fKi := 2.0, fKd := 1.2
        );
        
        (* Modulate cyclonic separation intensity *)
        fCyclonicSepRPM := LIMIT(3500.0, 3500.0 + (fbPlumeTurbidityPID.fOutput * 50.0), 9000.0);
        
        (* Inject sediment back into trench at ZERO relative velocity *)
        (* Control injection pump to match crawler speed vector (simplified to velocity offset here) *)
        fbInjectionVelocityPID(
            fSetpoint := 0.0, (* Zero absolute velocity relative to sediment *)
            fProcessValue := stTelemetry.fInjectionVelocity_m_s,
            fKp := 10.0, fKi := 5.0, fKd := 0.0
        );
        fInjectionPumpRPM := LIMIT(0.0, fInjectionPumpRPM + fbInjectionVelocityPID.fOutput, 5000.0);
        
        (* Alarms *)
        bAlarmPlumeCritical := stTelemetry.fPlumeTurbidity_NTU > fMaxPermissibleNTU;
        bAlarmLossOfLift := (stTelemetry.fNoduleMassFlow_kg_s < 1.0) AND (fJetPumpCommand_RPM > 6000.0);
        
        IF bAlarmPlumeCritical THEN
            eCurrentState := eSTATE_HOLDING;
        END_IF

    eSTATE_HOLDING:
        (* Halt collection, maintain mitigation *)
        fJetPumpCommand_RPM := 0.0;
        fApertureValveOpen_Pct := 0.0;
        
        IF stTelemetry.fPlumeTurbidity_NTU < (fMaxPermissibleNTU * 0.5) THEN
            eCurrentState := eSTATE_UNHOLDING;
        END_IF
        
    eSTATE_UNHOLDING:
        eCurrentState := eSTATE_EXECUTE;

    eSTATE_STOPPING:
        fJetPumpCommand_RPM := 0.0;
        fCyclonicSepRPM := fCyclonicSepRPM - 20.0;
        fInjectionPumpRPM := fInjectionPumpRPM - 20.0;
        IF fCyclonicSepRPM <= 0.0 AND fInjectionPumpRPM <= 0.0 THEN
            eCurrentState := eSTATE_STOPPED;
        END_IF
        
    eSTATE_ABORTING:
        fJetPumpCommand_RPM := 0.0;
        fApertureValveOpen_Pct := 0.0;
        fCyclonicSepRPM := 0.0;
        fInjectionPumpRPM := 0.0;
        eCurrentState := eSTATE_ABORTED;
        
    eSTATE_ABORTED:
        IF NOT bAbort THEN
            eCurrentState := eSTATE_CLEARED;
        END_IF
        
    eSTATE_CLEARED:
        eCurrentState := eSTATE_STOPPED;
        
    ELSE
        eCurrentState := eSTATE_UNDEFINED;
END_CASE
```"""

json_obj = {
    'messages': [
        {'role': 'user', 'content': prompt},
        {'role': 'assistant', 'content': st_code}
    ]
}

os.makedirs('data', exist_ok=True)
with open('data/synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(json_obj) + '\\n')
print('Successfully appended to jsonl')
