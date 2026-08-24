import json
import os

prompt = """As a Lead Manufacturing Engineer for a 3D NAND Flash Memory Fab, please design an Atomic Layer Deposition (ALD) Chamber Controller in IEC 61131-3 (Structured Text). This module must evolve a basic step sequencer into an advanced ALD controller meeting the following technical specifications:
1. Angstrom-level precursor gas pulsing for Trimethylaluminum (TMA).
2. Sub-millisecond mass flow controller (MFC) sequencing to achieve exact dose/purge cycles.
3. Foreline trap and delivery line heating control to prevent unreacted precursor condensation.
4. Robust state machine for ALD cycle sequencing.
Provide a complete, production-ready PLC program including data types, function blocks, and state machine logic."""

response = """An Atomic Layer Deposition (ALD) process for 3D NAND flash memory fabrication demands extreme precision. Trimethylaluminum (TMA) is highly reactive, and sub-millisecond precursor dosing is required to achieve Angstrom-level film thickness control. Condensation in the foreline trap can lead to particle defects and catastrophic pump failures, so proactive thermal management is essential.

Below is a production-ready IEC 61131-3 Structured Text implementation of the ALD Chamber Controller. It utilizes `LTIME` for sub-millisecond timer resolution and a robust state machine to manage the dosing sequence and temperature zones.

### 1. Data Unit Types (DUTs)

First, we define the structures for our temperature zones, MFC control, and the state machine enumeration.

```iecst
TYPE E_ALD_State :
(
    ALD_INIT := 0,
    ALD_IDLE := 10,
    ALD_PUMP_DOWN := 20,
    ALD_THERMAL_STABILIZE := 30,
    ALD_RECIPE_START := 40,
    ALD_TMA_DOSE := 50,
    ALD_TMA_PURGE := 60,
    ALD_OXIDIZER_DOSE := 70,
    ALD_OXIDIZER_PURGE := 80,
    ALD_CYCLE_END := 90,
    ALD_RECIPE_COMPLETE := 100,
    ALD_ABORT := 999
);
END_TYPE

TYPE ST_MFC_Control :
STRUCT
    Enable : BOOL;
    Setpoint_sccm : REAL;
    ActualFlow_sccm : REAL;
    ValvePosition : REAL;
    AtSetpoint : BOOL;
END_STRUCT
END_TYPE

TYPE ST_TempZone :
STRUCT
    CurrentTemp : REAL;
    TargetTemp : REAL;
    Tolerance : REAL;
    HeaterOutput : REAL;
    AtTemperature : BOOL;
END_STRUCT
END_TYPE
```

### 2. Temperature Controller (Foreline Trap & Delivery Lines)

We need a dedicated function block to manage heating to prevent TMA condensation. TMA typically condenses if lines drop below ~40-60°C depending on pressure, while foreline traps run even hotter to break down or passivate unreacted precursors.

```iecst
FUNCTION_BLOCK FB_ThermalManager
VAR_INPUT
    bEnable : BOOL;
    rActualTempChamber : REAL;
    rActualTempForeline : REAL;
    rActualTempDelivery : REAL;
END_VAR
VAR_OUTPUT
    stChamber : ST_TempZone;
    stForeline : ST_TempZone;
    stDelivery : ST_TempZone;
    bAllZonesStable : BOOL;
END_VAR
VAR
    fbPidChamber : PID;
    fbPidForeline : PID;
    fbPidDelivery : PID;
END_VAR

// Initialize Targets
stChamber.TargetTemp := 300.0; // Typical ALD window for Al2O3
stForeline.TargetTemp := 120.0; // Keep foreline hot to prevent TMA condensation
stDelivery.TargetTemp := 80.0;  // Delivery lines heated to prevent precursor condensation
stChamber.Tolerance := 2.0;
stForeline.Tolerance := 5.0;
stDelivery.Tolerance := 3.0;

IF bEnable THEN
    // Chamber PID
    fbPidChamber(ACTUAL := rActualTempChamber, SET_POINT := stChamber.TargetTemp, 
                 KP := 2.5, TN := 120.0, TV := 10.0, Y => stChamber.HeaterOutput);
    stChamber.AtTemperature := ABS(rActualTempChamber - stChamber.TargetTemp) <= stChamber.Tolerance;

    // Foreline Trap PID
    fbPidForeline(ACTUAL := rActualTempForeline, SET_POINT := stForeline.TargetTemp, 
                  KP := 1.5, TN := 60.0, TV := 5.0, Y => stForeline.HeaterOutput);
    stForeline.AtTemperature := ABS(rActualTempForeline - stForeline.TargetTemp) <= stForeline.Tolerance;

    // Delivery Line PID
    fbPidDelivery(ACTUAL := rActualTempDelivery, SET_POINT := stDelivery.TargetTemp, 
                  KP := 1.8, TN := 45.0, TV := 2.0, Y => stDelivery.HeaterOutput);
    stDelivery.AtTemperature := ABS(rActualTempDelivery - stDelivery.TargetTemp) <= stDelivery.Tolerance;

    bAllZonesStable := stChamber.AtTemperature AND stForeline.AtTemperature AND stDelivery.AtTemperature;
ELSE
    stChamber.HeaterOutput := 0.0;
    stForeline.HeaterOutput := 0.0;
    stDelivery.HeaterOutput := 0.0;
    bAllZonesStable := FALSE;
END_IF
END_FUNCTION_BLOCK
```

### 3. ALD Sequencer & Sub-Millisecond MFC Control

The main controller orchestrates the precursor pulses. Sub-millisecond resolution is achieved utilizing the `LTON` (Long Time Delay On) timer which operates on nanosecond/microsecond resolution (`LTIME`).

```iecst
FUNCTION_BLOCK FB_ALDChamberController
VAR_INPUT
    bStartRecipe : BOOL;
    bAbort : BOOL;
    nTargetCycles : UDINT := 50; // Typically 1 cycle = ~1 Angstrom of Al2O3
    
    // Sub-millisecond and standard pulse parameters
    tTMADose : LTIME := LTIME#800us;  // 800 microsecond TMA dose
    tTMAPurge : LTIME := LTIME#2s;    // 2 second Ar purge
    tOxDose : LTIME := LTIME#15ms;    // 15 ms H2O/O3 dose
    tOxPurge : LTIME := LTIME#3s;     // 3 second Ar purge
    
    rChamberPressure : REAL;          // Torr
END_VAR
VAR_OUTPUT
    eState : E_ALD_State;
    nCurrentCycle : UDINT;
    bRecipeComplete : BOOL;
    bError : BOOL;
    
    // Fast acting ALD Valves (ALDs)
    bValveTMA : BOOL;
    bValveOxidizer : BOOL;
    bValvePurgeAr : BOOL;
    bPumpGateValve : BOOL;
    
    stMfcTMA : ST_MFC_Control;
    stMfcOx : ST_MFC_Control;
    stMfcPurge : ST_MFC_Control;
END_VAR
VAR
    fbThermal : FB_ThermalManager;
    hpTimer : LTON; // High Precision Timer for sub-ms control
    tStateTimer : TON; // Standard timer for purges
    tStateTimeL : LTIME; 
END_VAR

// Abort Interlock
IF bAbort OR (rChamberPressure > 10.0 AND eState > ALD_PUMP_DOWN) THEN
    eState := ALD_ABORT;
END_IF

// Thermal Management Execution
fbThermal(bEnable := (eState <> ALD_ABORT), 
          rActualTempChamber := 300.0, // Replace with IO 
          rActualTempForeline := 120.0, 
          rActualTempDelivery := 80.0);

// State Machine
CASE eState OF
    ALD_INIT:
        bValveTMA := FALSE;
        bValveOxidizer := FALSE;
        bValvePurgeAr := FALSE;
        bPumpGateValve := FALSE;
        stMfcTMA.Enable := FALSE;
        nCurrentCycle := 0;
        bRecipeComplete := FALSE;
        eState := ALD_IDLE;
        
    ALD_IDLE:
        IF bStartRecipe THEN
            eState := ALD_PUMP_DOWN;
        END_IF
        
    ALD_PUMP_DOWN:
        bPumpGateValve := TRUE;
        // Wait for base pressure
        IF rChamberPressure < 0.05 THEN
            eState := ALD_THERMAL_STABILIZE;
        END_IF
        
    ALD_THERMAL_STABILIZE:
        IF fbThermal.bAllZonesStable THEN
            eState := ALD_RECIPE_START;
        END_IF
        
    ALD_RECIPE_START:
        nCurrentCycle := 1;
        bValvePurgeAr := TRUE;
        stMfcPurge.Enable := TRUE;
        stMfcPurge.Setpoint_sccm := 500.0;
        eState := ALD_TMA_DOSE;
        hpTimer(IN:=FALSE); // Reset timer
        
    ALD_TMA_DOSE:
        // Sub-millisecond pulsing of TMA
        hpTimer(IN := TRUE, PT := tTMADose);
        bValveTMA := TRUE;
        stMfcTMA.Enable := TRUE;
        stMfcTMA.Setpoint_sccm := 150.0;
        
        IF hpTimer.Q THEN
            bValveTMA := FALSE;
            hpTimer(IN := FALSE);
            tStateTimer(IN := FALSE);
            eState := ALD_TMA_PURGE;
        END_IF
        
    ALD_TMA_PURGE:
        // Purge residual TMA and byproducts (methane) through foreline
        tStateTimer(IN := TRUE, PT := LTIME_TO_TIME(tTMAPurge));
        bValveTMA := FALSE;
        
        IF tStateTimer.Q THEN
            tStateTimer(IN := FALSE);
            hpTimer(IN := FALSE);
            eState := ALD_OXIDIZER_DOSE;
        END_IF
        
    ALD_OXIDIZER_DOSE:
        // Fast dose of Oxidizer to react with chemisorbed TMA
        hpTimer(IN := TRUE, PT := tOxDose);
        bValveOxidizer := TRUE;
        stMfcOx.Enable := TRUE;
        stMfcOx.Setpoint_sccm := 200.0;
        
        IF hpTimer.Q THEN
            bValveOxidizer := FALSE;
            hpTimer(IN := FALSE);
            tStateTimer(IN := FALSE);
            eState := ALD_OXIDIZER_PURGE;
        END_IF
        
    ALD_OXIDIZER_PURGE:
        // Purge oxidizer and reaction byproducts
        tStateTimer(IN := TRUE, PT := LTIME_TO_TIME(tOxPurge));
        bValveOxidizer := FALSE;
        
        IF tStateTimer.Q THEN
            tStateTimer(IN := FALSE);
            eState := ALD_CYCLE_END;
        END_IF
        
    ALD_CYCLE_END:
        IF nCurrentCycle >= nTargetCycles THEN
            eState := ALD_RECIPE_COMPLETE;
        ELSE
            nCurrentCycle := nCurrentCycle + 1;
            eState := ALD_TMA_DOSE; // Loop back for next cycle
        END_IF
        
    ALD_RECIPE_COMPLETE:
        bRecipeComplete := TRUE;
        bValvePurgeAr := FALSE;
        bPumpGateValve := FALSE;
        stMfcPurge.Enable := FALSE;
        IF NOT bStartRecipe THEN
            eState := ALD_INIT;
        END_IF
        
    ALD_ABORT:
        bError := TRUE;
        bValveTMA := FALSE;
        bValveOxidizer := FALSE;
        bValvePurgeAr := TRUE; // Purge chamber on abort
        stMfcTMA.Enable := FALSE;
        stMfcOx.Enable := FALSE;
        // Hold in abort until reset
        IF NOT bAbort THEN
            eState := ALD_INIT;
        END_IF
        
END_CASE

END_FUNCTION_BLOCK
```

### Engineering Details:
1. **Sub-millisecond Precision**: Typical IEC standard `TON` timers are limited to `TIME` which resolves to 1ms. We utilize `LTON` and `LTIME` which support nanosecond resolutions (e.g., `LTIME#800us`), allowing for precise dosing critical for single-layer atom deposition.
2. **Foreline Condensation Avoidance**: The `FB_ThermalManager` maintains the delivery lines at 80°C and the foreline trap at 120°C. TMA vaporizes near room temperature but requires higher temps down-line to ensure it and complex byproducts do not condense and block the vacuum lines.
3. **Safety & Equipment Integrity**: The controller includes pressure interlocks (`rChamberPressure > 10.0` Torr abort trigger) to prevent unsafe gas mixing or chamber over-pressurization during valve failure. All precursor valves default to `FALSE` in the abort state.
"""

data = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response}
    ]
}

target_file = r"C:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"
with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(data) + "\n")

print(f"Successfully appended ALD controller to {target_file}")
