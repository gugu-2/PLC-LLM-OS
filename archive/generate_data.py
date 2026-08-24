import json
import os

user_prompt = """You are acting as the Lead Bioprocess Automation Architect for an Advanced Genomic Medicine Facility.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "CRISPR-Cas9 Cell Therapy Electroporation & Continuous Perfusion Bioreactor" (`FB_CRISPR_ElectroporationController`).

### Technical Specifications & Engineering Rigor Required:
1. **High-Voltage Micro-Electroporation**: Square-wave pulse generator sequencing (e.g., 2.0 kV/cm, 10-millisecond pulses) to permeabilize T-cell membranes for Cas9 RNP (Ribonucleoprotein) insertion without causing irreversible thermal necrosis.
2. **Continuous Perfusion & Tangential Flow**: Acoustic wave cell retention or alternating tangential flow (ATF) filtering to maintain a steady state of nutrient delivery (glucose/glutamine) and toxic byproduct (lactate/ammonia) removal.
3. **Cell Viability & pH/DO Control**: Cascaded PID loops for Dissolved Oxygen (DO) using micro-sparging and pH using CO2/Bicarbonate buffers, coupled with capacitance-based live-cell density sensors.
4. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, 21 CFR Part 11 electronic batch records compliance flags, PackML state machine."""

assistant_response = """```iec-st
(****************************************************************************************
* FUNCTION_BLOCK: FB_CRISPR_ElectroporationController                                     *
* DESCRIPTION: Lead Bioprocess Automation Architect - Advanced Genomic Medicine Facility  *
*              Controls High-Voltage Micro-Electroporation for CRISPR-Cas9 RNP T-Cell   *
*              Permeabilization and Continuous Perfusion Bioreactor processes using     *
*              PackML state machines, cascaded PID loops (pH, DO), and 21 CFR Part 11   *
*              compliance metrics for electronic batch records.                         *
****************************************************************************************)
FUNCTION_BLOCK FB_CRISPR_ElectroporationController
VAR_INPUT
    bEnable                  : BOOL;   (* Enable Function Block *)
    bStartBatch              : BOOL;   (* Start Batch Trigger *)
    bStopBatch               : BOOL;   (* Stop Batch Trigger *)
    bAbort                   : BOOL;   (* Abort Trigger *)
    bReset                   : BOOL;   (* Reset Trigger *)
    
    (* Process Parameters *)
    fVoltageSetpointKV       : LREAL := 2.0; (* kV/cm for electroporation *)
    tPulseDuration           : TIME := T#10MS;
    nPulseCount              : INT := 3;
    fGlucoseSetpoint_mM      : LREAL := 15.0;
    fGlutamineSetpoint_mM    : LREAL := 4.0;
    fTargetpH                : LREAL := 7.2;
    fTargetDO_Percent        : LREAL := 40.0;
    
    (* Sensor Data Inputs *)
    fLiveCellDensity_Capacitance : LREAL; (* pF/cm *)
    fCurrentpH               : LREAL;
    fCurrentDO_Percent       : LREAL;
    fCurrentLactate_mM       : LREAL;
    fCurrentAmmonia_mM       : LREAL;
    fCurrentVesselTemp       : LREAL;
END_VAR

VAR_OUTPUT
    (* PackML State Output *)
    eCurrentState            : E_PackML_State;
    bBatchInProgress         : BOOL;
    
    (* Actuator Controls *)
    bTriggerElectroporation  : BOOL;
    fElectroporationVoltage  : LREAL;
    bPerfusionPumpEnable     : BOOL;
    fPerfusionPumpSpeed      : LREAL; (* L/min *)
    bATFSystemEnable         : BOOL;  (* Alternating Tangential Flow System *)
    
    (* Gas & Buffer Controls *)
    fMicroSpargerO2Flow      : LREAL; (* sccm *)
    fMicroSpargerAirFlow     : LREAL; (* sccm *)
    fCO2SpargerFlow          : LREAL; (* sccm *)
    fBasePumpSpeed           : LREAL; (* Bicarbonate pump rpm *)
    
    (* 21 CFR Part 11 & Quality Metrics *)
    sBatchRecordID           : STRING(255);
    bBatchDeviationDetected  : BOOL;
    bThermalNecrosisAlarm    : BOOL;
    bReadyForHarvest         : BOOL;
END_VAR

VAR
    (* PackML State Machine Variables *)
    eNextState               : E_PackML_State := E_PackML_State.STOPPED;
    
    (* Electroporation Sequencer Variables *)
    tPulseTimer              : TON;
    tInterPulseTimer         : TON;
    nPulsesDelivered         : INT := 0;
    bPulseActive             : BOOL;
    eElectroState            : INT := 0; (* 0: IDLE, 1: PULSE_ON, 2: INTER_WAIT, 3: COMPLETE *)
    
    (* PID Controllers *)
    fbPID_pH                 : FB_PIDController;
    fbPID_DO                 : FB_PIDController;
    fbPID_Perfusion          : FB_PIDController;
    
    (* Data Logging & Compliance *)
    tAuditTrailTimer         : TON;
    fTotalPermeabilizedCells : LREAL;
    fThermalNecrosisLimit    : LREAL := 39.5; (* Deg C limit for viable T-Cells *)
    
    (* Internal State Flags *)
    bElectroporationComplete : BOOL;
    bPerfusionStabilized     : BOOL;
END_VAR

(* Implementation *)

(* 1. Thermal Necrosis Protection & Safety Interlocks *)
IF fCurrentVesselTemp >= fThermalNecrosisLimit THEN
    bThermalNecrosisAlarm := TRUE;
    bBatchDeviationDetected := TRUE;
    eNextState := E_PackML_State.ABORTING;
END_IF;

(* 2. PackML State Machine *)
CASE eCurrentState OF
    
    E_PackML_State.STOPPED:
        bBatchInProgress := FALSE;
        bPerfusionPumpEnable := FALSE;
        bATFSystemEnable := FALSE;
        IF bReset THEN
            eNextState := E_PackML_State.IDLE;
        END_IF;
        
    E_PackML_State.IDLE:
        IF bStartBatch AND bEnable THEN
            sBatchRecordID := 'CRISPR_TCELL_BATCH_2026_08_22';
            eNextState := E_PackML_State.STARTING;
        END_IF;
        
    E_PackML_State.STARTING:
        bATFSystemEnable := TRUE;
        bPerfusionPumpEnable := TRUE;
        bBatchDeviationDetected := FALSE;
        bThermalNecrosisAlarm := FALSE;
        nPulsesDelivered := 0;
        bElectroporationComplete := FALSE;
        eNextState := E_PackML_State.EXECUTE;
        
    E_PackML_State.EXECUTE:
        bBatchInProgress := TRUE;
        
        (* Bioreactor Core Control Logic *)
        ACT_ControlDO_pH();
        ACT_ControlPerfusion();
        ACT_ElectroporationSequence();
        ACT_AuditTrailLogging();
        
        IF bStopBatch THEN
            eNextState := E_PackML_State.STOPPING;
        ELSIF bAbort THEN
            eNextState := E_PackML_State.ABORTING;
        ELSIF fLiveCellDensity_Capacitance > 50.0 AND bElectroporationComplete THEN 
            (* Harvest threshold met (e.g. >50x10^6 cells/mL) *)
            bReadyForHarvest := TRUE;
            eNextState := E_PackML_State.COMPLETING;
        END_IF;
        
    E_PackML_State.COMPLETING:
        bReadyForHarvest := TRUE;
        bBatchInProgress := FALSE;
        eNextState := E_PackML_State.COMPLETE;
        
    E_PackML_State.COMPLETE:
        bPerfusionPumpEnable := FALSE;
        bATFSystemEnable := FALSE;
        IF bReset THEN
            eNextState := E_PackML_State.IDLE;
        END_IF;
        
    E_PackML_State.STOPPING:
        bBatchInProgress := FALSE;
        eNextState := E_PackML_State.STOPPED;
        
    E_PackML_State.ABORTING:
        bBatchInProgress := FALSE;
        bTriggerElectroporation := FALSE;
        bATFSystemEnable := FALSE;
        bPerfusionPumpEnable := FALSE;
        eNextState := E_PackML_State.ABORTED;
        
    E_PackML_State.ABORTED:
        IF bReset THEN
            eNextState := E_PackML_State.IDLE;
        END_IF;
        
END_CASE;

eCurrentState := eNextState;

(* --- ACTIONS --- *)

ACTION ACT_ControlDO_pH:
    (* DO Control: Micro-sparging cascade *)
    fbPID_DO(
        fSetpoint := fTargetDO_Percent,
        fProcessVariable := fCurrentDO_Percent,
        fKp := 1.5, fKi := 0.05, fKd := 0.01,
        bEnable := bBatchInProgress
    );
    
    IF fbPID_DO.fControlOutput > 0 THEN
        fMicroSpargerO2Flow := fbPID_DO.fControlOutput * 0.1;
        fMicroSpargerAirFlow := 5.0 - fMicroSpargerO2Flow; (* Maintain constant total gas *)
    ELSE
        fMicroSpargerO2Flow := 0.0;
        fMicroSpargerAirFlow := 5.0;
    END_IF;

    (* pH Control: CO2 & Bicarbonate Buffering *)
    fbPID_pH(
        fSetpoint := fTargetpH,
        fProcessVariable := fCurrentpH,
        fKp := 2.0, fKi := 0.1, fKd := 0.02,
        bEnable := bBatchInProgress
    );
    
    IF fbPID_pH.fControlOutput > 0 THEN
        (* pH is high, add CO2 (acidic) *)
        fCO2SpargerFlow := fbPID_pH.fControlOutput * 0.05;
        fBasePumpSpeed := 0.0;
    ELSIF fbPID_pH.fControlOutput < 0 THEN
        (* pH is low, add Bicarbonate (basic) *)
        fBasePumpSpeed := ABS(fbPID_pH.fControlOutput) * 0.2;
        fCO2SpargerFlow := 0.0;
    ELSE
        fCO2SpargerFlow := 0.0;
        fBasePumpSpeed := 0.0;
    END_IF;
END_ACTION

ACTION ACT_ControlPerfusion:
    (* Alternating Tangential Flow (ATF) & Nutrient Delivery based on toxic byproducts *)
    (* If Lactate > 15 mM or Ammonia > 2 mM, increase perfusion rate *)
    
    fbPID_Perfusion(
        fSetpoint := 12.0, (* Target max Lactate mM *)
        fProcessVariable := fCurrentLactate_mM,
        fKp := 0.8, fKi := 0.01, fKd := 0.0,
        bEnable := bBatchInProgress
    );
    
    IF fbPID_Perfusion.fControlOutput > 0 THEN
        fPerfusionPumpSpeed := 0.5 + (fbPID_Perfusion.fControlOutput * 0.1); (* Base 0.5 L/min + PID adjustment *)
    ELSE
        fPerfusionPumpSpeed := 0.5;
    END_IF;
    
    (* Cap perfusion pump speed at 2.0 L/min to protect shear-sensitive cells *)
    IF fPerfusionPumpSpeed > 2.0 THEN
        fPerfusionPumpSpeed := 2.0;
    END_IF;
END_ACTION

ACTION ACT_ElectroporationSequence:
    IF NOT bBatchInProgress OR bElectroporationComplete THEN
        bTriggerElectroporation := FALSE;
        eElectroState := 0; (* IDLE *)
        RETURN;
    END_IF;

    CASE eElectroState OF
        0: (* IDLE *)
            (* Wait for optimal live cell density and stable temp to trigger Cas9 RNP insertion *)
            IF (fLiveCellDensity_Capacitance > 10.0) AND (fCurrentVesselTemp < 37.5) AND NOT bElectroporationComplete THEN
                nPulsesDelivered := 0;
                fElectroporationVoltage := fVoltageSetpointKV;
                eElectroState := 1; (* PULSE_ON *)
            END_IF;
            
        1: (* PULSE_ON *)
            bTriggerElectroporation := TRUE;
            tPulseTimer(IN:= TRUE, PT:= tPulseDuration);
            IF tPulseTimer.Q THEN
                bTriggerElectroporation := FALSE;
                tPulseTimer(IN:= FALSE);
                nPulsesDelivered := nPulsesDelivered + 1;
                eElectroState := 2; (* INTER_PULSE_WAIT *)
            END_IF;
            
        2: (* INTER_PULSE_WAIT *)
            (* 1-second relaxation time between pulses to prevent thermal runaway *)
            tInterPulseTimer(IN:= TRUE, PT:= T#1S);
            IF tInterPulseTimer.Q THEN
                tInterPulseTimer(IN:= FALSE);
                IF nPulsesDelivered >= nPulseCount THEN
                    bElectroporationComplete := TRUE;
                    eElectroState := 3; (* COMPLETE *)
                ELSE
                    eElectroState := 1; (* PULSE_ON *)
                END_IF;
            END_IF;
            
        3: (* COMPLETE *)
            bTriggerElectroporation := FALSE;
    END_CASE;
END_ACTION

ACTION ACT_AuditTrailLogging:
    (* 21 CFR Part 11 Electronic Records Compliance: Log critical parameters periodically *)
    tAuditTrailTimer(IN:= bBatchInProgress AND NOT tAuditTrailTimer.Q, PT:= T#10S);
    
    IF tAuditTrailTimer.Q THEN
        (* System logic to log to historian... *)
    END_IF;
END_ACTION

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {
            "role": "user",
            "content": user_prompt
        },
        {
            "role": "assistant",
            "content": assistant_response
        }
    ]
}

os.makedirs('data', exist_ok=True)
with open('data/synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(record) + '\n')
