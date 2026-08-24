import json
import os

target_file = r"C:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"

user_prompt = """You are acting as the Lead Grid Architect for a Trans-Continental Super-Grid Project.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Multi-Terminal High-Voltage Direct Current (HVDC) Subsea Interconnector & Fast DC Breaker Controller" (`FB_MT_HVDC_Interconnector`).

### Technical Specifications & Engineering Rigor Required:
1. **Voltage Margin Control & Droop Allocation**:
   - Master-slave transitionless control across 4 offshore wind converter stations and 2 onshore grid nodes.
   - DC voltage ($V_{dc} = \pm 525\text{ kV}$) droop control ensuring instantaneous active power ($P$) balancing if the primary voltage-regulating onshore terminal trips offline.
2. **Hybrid Fast DC Circuit Breakers**:
   - Ultra-fast fault detection ($di/dt > 5\text{ kA/ms}$) via distributed Rogowski coils.
   - Millisecond-sequencing of the hybrid breaker: transferring current from the ultra-fast mechanical disconnect switch into the solid-state IGBT commutation path, and finally into the Metal-Oxide Varistor (MOV) energy absorber to clear the DC subsea cable fault in $<3\text{ ms}$.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, multi-terminal power flow matrices, PackML states.

Output a complete, valid JSON object with {"messages": [{"role": "user", "content": "Mega-prompt description"}, {"role": "assistant", "content": "Full raw Structured Text code inside ```iec-st```"}]}."""

assistant_response = """```iec-st
(*
======================================================================================
FUNCTION_BLOCK FB_MT_HVDC_Interconnector
DESCRIPTION:
    Master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation
    for a Multi-Terminal High-Voltage Direct Current (HVDC) Subsea Interconnector
    and Fast DC Breaker Controller.

    Core Capabilities:
    1. Voltage Margin Control & Droop Allocation for 6 terminals (4 offshore, 2 onshore).
    2. Master-slave transitionless control with Vdc droop balancing (Vdc = ± 525 kV).
    3. Ultra-fast fault detection (di/dt > 5 kA/ms) via distributed Rogowski coils.
    4. Millisecond-sequencing of Hybrid Fast DC Circuit Breakers (< 3 ms clear time).
    5. PackML state machine architecture.

AUTHOR: Lumina Elite Synthetic Data Architect (Lead Grid Architect)
VERSION: 3.0.0
======================================================================================
*)

TYPE E_PackML_State :
(
    eSTATE_UNDEFINED     := 0,
    eSTATE_IDLE          := 1,
    eSTATE_STARTING      := 2,
    eSTATE_EXECUTE       := 3,
    eSTATE_COMPLETING    := 4,
    eSTATE_COMPLETE      := 5,
    eSTATE_HOLDING       := 6,
    eSTATE_HELD          := 7,
    eSTATE_UNHOLDING     := 8,
    eSTATE_SUSPENDING    := 9,
    eSTATE_SUSPENDED     := 10,
    eSTATE_UNSUSPENDING  := 11,
    eSTATE_STOPPING      := 12,
    eSTATE_STOPPED       := 13,
    eSTATE_ABORTING      := 14,
    eSTATE_ABORTED       := 15,
    eSTATE_CLEARING      := 16
);
END_TYPE

TYPE E_Terminal_Role :
(
    eROLE_SLAVE_P_CTRL       := 0, (* Active Power Control *)
    eROLE_MASTER_VDC_CTRL    := 1, (* Primary DC Voltage Control *)
    eROLE_DROOP_VDC_CTRL     := 2  (* Droop DC Voltage Control *)
);
END_TYPE

TYPE E_Breaker_State :
(
    eBRK_CLOSED              := 0,
    eBRK_COMMUTATING_IGBT    := 1,
    eBRK_UFD_OPENING         := 2,
    eBRK_MOV_ABSORBING       := 3,
    eBRK_OPEN                := 4,
    eBRK_FAILED              := 99
);
END_TYPE

TYPE ST_Terminal_Data :
STRUCT
    Role                : E_Terminal_Role;
    IsOnline            : BOOL;
    Vdc_Meas_kV         : LREAL; (* Measured DC Voltage [kV] *)
    P_Meas_MW           : LREAL; (* Measured Active Power [MW] *)
    P_Ref_MW            : LREAL; (* Active Power Reference [MW] *)
    Vdc_Ref_kV          : LREAL; (* DC Voltage Reference [kV] *)
    Droop_kV_per_MW     : LREAL; (* Droop coefficient [kV/MW] *)
    di_dt_kA_per_ms     : LREAL; (* Rate of change of current [kA/ms] *)
    BreakerState        : E_Breaker_State;
    BreakerTripCmd      : BOOL;
    FaultDetected       : BOOL;
    FaultClearTimer_ms  : LREAL;
END_STRUCT
END_TYPE

FUNCTION_BLOCK FB_MT_HVDC_Interconnector
VAR_INPUT
    bEnable             : BOOL;
    bAbort              : BOOL;
    bClear              : BOOL;
    bTripOverride       : BOOL;
    
    aTerminals_In       : ARRAY[1..6] OF ST_Terminal_Data; (* T1-T4 Offshore, T5-T6 Onshore *)
END_VAR

VAR_OUTPUT
    eState              : E_PackML_State;
    aTerminals_Out      : ARRAY[1..6] OF ST_Terminal_Data;
    bSystemFault        : BOOL;
    bPrimaryMasterLoss  : BOOL;
    rTotalSystemPower   : LREAL;
END_VAR

VAR
    i                   : INT;
    rNominalVdc_kV      : LREAL := 525.0;
    rFaultThreshold_kA  : LREAL := 5.0; (* 5 kA/ms *)
    rMaxClearTime_ms    : LREAL := 3.0; (* 3 ms max clearing time *)
    
    dtCycleTime         : LREAL := 0.1; (* 100 microseconds cycle time *)
    bMasterActive       : BOOL;
    iActiveMasterIdx    : INT;
END_VAR

(* ============================================================================== *)
(* PACKML STATE MACHINE IMPLEMENTATION                                            *)
(* ============================================================================== *)
IF bAbort THEN
    eState := eSTATE_ABORTING;
END_IF

CASE eState OF
    eSTATE_UNDEFINED, eSTATE_IDLE:
        IF bEnable THEN
            eState := eSTATE_STARTING;
        END_IF
        
    eSTATE_STARTING:
        (* Initialize terminal parameters *)
        FOR i := 1 TO 6 DO
            aTerminals_Out[i] := aTerminals_In[i];
            aTerminals_Out[i].BreakerState := eBRK_CLOSED;
            aTerminals_Out[i].FaultDetected := FALSE;
            aTerminals_Out[i].BreakerTripCmd := FALSE;
            aTerminals_Out[i].FaultClearTimer_ms := 0.0;
        END_FOR
        bSystemFault := FALSE;
        eState := eSTATE_EXECUTE;
        
    eSTATE_EXECUTE:
        IF NOT bEnable THEN
            eState := eSTATE_STOPPING;
        ELSE
            (* 1. Read Inputs & Master Synchronization *)
            FOR i := 1 TO 6 DO
                aTerminals_Out[i].Vdc_Meas_kV := aTerminals_In[i].Vdc_Meas_kV;
                aTerminals_Out[i].P_Meas_MW := aTerminals_In[i].P_Meas_MW;
                aTerminals_Out[i].di_dt_kA_per_ms := aTerminals_In[i].di_dt_kA_per_ms;
                aTerminals_Out[i].IsOnline := aTerminals_In[i].IsOnline;
            END_FOR

            (* 2. Voltage Margin Control & Droop Allocation *)
            bMasterActive := FALSE;
            iActiveMasterIdx := 0;
            
            (* Identify if primary master (usually Onshore T5) is online *)
            FOR i := 1 TO 6 DO
                IF aTerminals_Out[i].Role = eROLE_MASTER_VDC_CTRL AND aTerminals_Out[i].IsOnline AND NOT aTerminals_Out[i].FaultDetected THEN
                    bMasterActive := TRUE;
                    iActiveMasterIdx := i;
                    EXIT;
                END_IF
            END_FOR
            
            bPrimaryMasterLoss := NOT bMasterActive;
            
            (* Transitionless Control: If master is lost, switch droop controllers to balance power *)
            IF bPrimaryMasterLoss THEN
                FOR i := 1 TO 6 DO
                    IF aTerminals_Out[i].Role = eROLE_DROOP_VDC_CTRL AND aTerminals_Out[i].IsOnline THEN
                        (* Apply P-Vdc droop characteristic to regulate system voltage *)
                        aTerminals_Out[i].P_Ref_MW := aTerminals_Out[i].P_Meas_MW + 
                            (rNominalVdc_kV - aTerminals_Out[i].Vdc_Meas_kV) / aTerminals_Out[i].Droop_kV_per_MW;
                    END_IF
                END_FOR
            END_IF

            (* 3. Hybrid Fast DC Circuit Breaker Sequencing *)
            FOR i := 1 TO 6 DO
                (* Fault Detection via Rogowski Coils (di/dt) *)
                IF ABS(aTerminals_Out[i].di_dt_kA_per_ms) > rFaultThreshold_kA OR bTripOverride THEN
                    aTerminals_Out[i].FaultDetected := TRUE;
                    aTerminals_Out[i].BreakerTripCmd := TRUE;
                    bSystemFault := TRUE;
                END_IF
                
                (* Breaker State Machine (Millisecond Sequencing) *)
                IF aTerminals_Out[i].BreakerTripCmd THEN
                    aTerminals_Out[i].FaultClearTimer_ms := aTerminals_Out[i].FaultClearTimer_ms + dtCycleTime;
                    
                    CASE aTerminals_Out[i].BreakerState OF
                        eBRK_CLOSED:
                            (* Step 1: Transfer current to solid-state IGBT commutation path (t < 0.2 ms) *)
                            IF aTerminals_Out[i].FaultClearTimer_ms >= 0.2 THEN
                                aTerminals_Out[i].BreakerState := eBRK_COMMUTATING_IGBT;
                            END_IF
                            
                        eBRK_COMMUTATING_IGBT:
                            (* Step 2: Open ultra-fast mechanical disconnect switch (UFD) (0.2 ms < t < 2.0 ms) *)
                            IF aTerminals_Out[i].FaultClearTimer_ms >= 2.0 THEN
                                aTerminals_Out[i].BreakerState := eBRK_UFD_OPENING;
                            END_IF
                            
                        eBRK_UFD_OPENING:
                            (* Step 3: Block IGBTs, force current into MOV energy absorber (2.0 ms < t < 2.5 ms) *)
                            IF aTerminals_Out[i].FaultClearTimer_ms >= 2.5 THEN
                                aTerminals_Out[i].BreakerState := eBRK_MOV_ABSORBING;
                            END_IF
                            
                        eBRK_MOV_ABSORBING:
                            (* Step 4: Residual energy absorbed, fault cleared (t < 3.0 ms) *)
                            IF aTerminals_Out[i].FaultClearTimer_ms >= rMaxClearTime_ms THEN
                                aTerminals_Out[i].BreakerState := eBRK_OPEN;
                            END_IF
                            
                        eBRK_OPEN:
                            (* Subsea cable isolated *)
                            aTerminals_Out[i].IsOnline := FALSE;
                    END_CASE
                END_IF
            END_FOR
            
            (* 4. Telemetry and System Aggregation *)
            rTotalSystemPower := 0.0;
            FOR i := 1 TO 6 DO
                IF aTerminals_Out[i].IsOnline THEN
                    rTotalSystemPower := rTotalSystemPower + aTerminals_Out[i].P_Meas_MW;
                END_IF
            END_FOR
            
        END_IF
        
    eSTATE_STOPPING:
        (* Safely power down terminals *)
        FOR i := 1 TO 6 DO
            aTerminals_Out[i].P_Ref_MW := 0.0;
        END_FOR
        eState := eSTATE_STOPPED;
        
    eSTATE_STOPPED:
        IF bClear THEN
            eState := eSTATE_CLEARING;
        END_IF
        
    eSTATE_ABORTING:
        (* Immediate multi-terminal shutdown *)
        FOR i := 1 TO 6 DO
            aTerminals_Out[i].BreakerTripCmd := TRUE;
            aTerminals_Out[i].P_Ref_MW := 0.0;
        END_FOR
        eState := eSTATE_ABORTED;
        
    eSTATE_ABORTED:
        IF bClear THEN
            eState := eSTATE_CLEARING;
        END_IF
        
    eSTATE_CLEARING:
        bSystemFault := FALSE;
        eState := eSTATE_IDLE;
        
END_CASE
END_FUNCTION_BLOCK
```"""

obj = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(obj) + "\n")

print("Appended successfully.")
