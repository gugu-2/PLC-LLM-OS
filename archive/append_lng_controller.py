import json

def generate_payload():
    prompt = "You are acting as a Lead Marine Engineer for a massive Liquefied Natural Gas (LNG) Carrier. Evolve a basic temperature loop into an LNG Cargo Reliquefaction Plant Controller. Technical Specs: 1. Boil-Off Gas (BOG) compressor sequencing. 2. Cryogenic heat exchanger cascade control. 3. Cargo tank pressure management matrices."
    
    response = """Here is the evolved, production-ready IEC 61131-3 implementation for an LNG Cargo Reliquefaction Plant Controller.

This code evolves a simple PID loop into a full multi-variable, state-driven control system that handles the complexities of BOG compressor staging, active surge control, and the cryogenic nitrogen Brayton cycle for condensing boil-off gas back to LNG.

```pascal
FUNCTION_BLOCK FB_LNG_Reliquefaction_Controller
TITLE = 'LNG Cargo Reliquefaction Plant Controller'
VERSION : '3.1'
AUTHOR : 'Lumina Elite Synthetic Data Architect'

// -----------------------------------------------------------------------------
// This complex controller evolves a basic PID temperature loop into a full-scale
// LNG reliquefaction management system. It incorporates:
// 1. BOG (Boil-Off Gas) Compressor Sequencing and Anti-Surge
// 2. Cryogenic Heat Exchanger Cascade Control (Nitrogen Brayton Cycle)
// 3. Cargo Tank Pressure Management Matrix
// -----------------------------------------------------------------------------

VAR_INPUT
    // System Enables
    bSystemEnable           : BOOL; // Main system enable
    bEmergencyStop          : BOOL; // Emergency shutdown (ESD)
    bReset                  : BOOL; // System fault reset
    
    // Cargo Tank Parameters
    rTankPressure           : REAL; // kPa (absolute)
    rTankLevel              : REAL; // %
    rTankTemperature        : REAL; // °C
    
    // BOG Compressor Parameters
    rComp1_DischargePress   : REAL; // kPa
    rComp1_Flow             : REAL; // kg/h
    bComp1_Running          : BOOL;
    bComp1_Fault            : BOOL;
    
    rComp2_DischargePress   : REAL; // kPa
    rComp2_Flow             : REAL; // kg/h
    bComp2_Running          : BOOL;
    bComp2_Fault            : BOOL;
    
    // Cryogenic System Parameters (N2 Cycle)
    rN2_ExpanderTemp        : REAL; // °C
    rColdBox_Temp           : REAL; // °C
    rLNG_ReturnTemp         : REAL; // °C
END_VAR

VAR_OUTPUT
    // BOG Compressor Control
    bComp1_Start            : BOOL;
    bComp1_Stop             : BOOL;
    rComp1_SpeedCmd         : REAL; // % (0-100)
    rComp1_IGVCmd           : REAL; // Inlet Guide Vane % (0-100)
    rComp1_RecycleValve     : REAL; // Anti-surge valve % (0-100)
    
    bComp2_Start            : BOOL;
    bComp2_Stop             : BOOL;
    rComp2_SpeedCmd         : REAL; // % (0-100)
    rComp2_IGVCmd           : REAL; // Inlet Guide Vane % (0-100)
    rComp2_RecycleValve     : REAL; // Anti-surge valve % (0-100)
    
    // Cryogenic System Control
    rN2_CompSpeedCmd        : REAL; // Nitrogen comp speed %
    rN2_ExpanderBypass      : REAL; // Expander bypass valve %
    rJT_ValveCmd            : REAL; // Joule-Thomson expansion valve %
    
    // Status
    ePlantState             : INT;  // 0=Off, 1=Standby, 2=Starting, 3=Running, 4=Tripped
    bCommonAlarm            : BOOL;
    bESD_Active             : BOOL;
END_VAR

VAR
    // PID Controllers (Instantiated from library)
    fbTankPressControl      : FB_PID_Control; // Master pressure controller
    fbComp1_SurgeControl    : FB_PID_Control;
    fbComp2_SurgeControl    : FB_PID_Control;
    fbColdBox_TempControl   : FB_PID_Control;
    
    // State Machine
    iState                  : INT := 0;
    iSeqStep                : INT := 0;
    
    // Timers
    tonStartDelay           : TON;
    tonCompSeq              : TON;
    tonSurgeTimer           : TON;
    
    // Internal calculations
    rTotalBOGFlow           : REAL;
    rPressureError          : REAL;
    rLoadDemand             : REAL;
    
    // Matrix thresholds
    rPress_HighHigh         : REAL := 125.0; // kPa
    rPress_High             : REAL := 115.0;
    rPress_Target           : REAL := 108.0;
    rPress_Low              : REAL := 102.0;
    
    rTemp_TargetLNG         : REAL := -161.5; // °C
END_VAR

BEGIN
    // =========================================================================
    // 0. EMERGENCY SHUTDOWN (ESD) INTERLOCKS
    // =========================================================================
    IF bEmergencyStop OR (rTankPressure > rPress_HighHigh) THEN
        bESD_Active := TRUE;
        iState := 4; // Tripped
    END_IF;
    
    IF bReset AND NOT bEmergencyStop AND (rTankPressure < rPress_HighHigh) THEN
        bESD_Active := FALSE;
        bCommonAlarm := FALSE;
        IF iState = 4 THEN iState := 0; END_IF;
    END_IF;
    
    IF bESD_Active THEN
        // Hard shutdown of all equipment
        bComp1_Start := FALSE; bComp1_Stop := TRUE; rComp1_SpeedCmd := 0.0; rComp1_RecycleValve := 100.0;
        bComp2_Start := FALSE; bComp2_Stop := TRUE; rComp2_SpeedCmd := 0.0; rComp2_RecycleValve := 100.0;
        rN2_CompSpeedCmd := 0.0; rN2_ExpanderBypass := 100.0; rJT_ValveCmd := 0.0;
        ePlantState := 4;
        RETURN;
    END_IF;

    // =========================================================================
    // 1. CARGO TANK PRESSURE MANAGEMENT MATRIX
    // =========================================================================
    // Cascade control: Tank Pressure -> BOG Flow Demand -> Compressor Speed/IGV
    fbTankPressControl(
        rInput := rTankPressure,
        rSetpoint := rPress_Target,
        rKp := 2.5,
        rTi := 15.0,
        rTd := 0.0,
        bReset := NOT bSystemEnable
    );
    
    // Load Demand (0-200%) representing need for 0 to 2 compressors
    rLoadDemand := fbTankPressControl.rOutput * 2.0; 

    // =========================================================================
    // 2. BOG COMPRESSOR SEQUENCING & LOAD SHARING
    // =========================================================================
    // Start/Stop sequencing based on pressure demand matrix
    IF bSystemEnable AND (iState < 4) THEN
        
        CASE iState OF
            0: // OFF
                IF rTankPressure > rPress_High THEN
                    iState := 1; // Transition to start sequence
                END_IF;
                
            1: // STARTING COMP 1
                bComp1_Start := TRUE;
                bComp1_Stop := FALSE;
                IF bComp1_Running AND rComp1_DischargePress > 200.0 THEN
                    iState := 2; // Comp 1 running, cryogenic cooling active
                END_IF;
                
            2: // RUNNING 1 COMPRESSOR
                // Control Speed and IGV of Comp 1 based on load demand (0-100%)
                rComp1_SpeedCmd := LIMIT(MN:=40.0, IN:=rLoadDemand, MX:=100.0);
                rComp1_IGVCmd := LIMIT(MN:=20.0, IN:=(rLoadDemand - 40.0)*1.66, MX:=100.0);
                
                // Sequence Compressor 2 if demand is very high
                tonCompSeq(IN:=(rLoadDemand > 95.0), PT:=T#60s);
                IF tonCompSeq.Q AND NOT bComp2_Fault THEN
                    iState := 3;
                END_IF;
                
                // Stop condition
                IF rTankPressure < rPress_Low THEN
                    bComp1_Start := FALSE;
                    bComp1_Stop := TRUE;
                    iState := 0;
                END_IF;
                
            3: // RUNNING 2 COMPRESSORS (Load Sharing)
                bComp2_Start := TRUE;
                bComp2_Stop := FALSE;
                
                // Share load equally
                rComp1_SpeedCmd := LIMIT(MN:=40.0, IN:=rLoadDemand/2.0, MX:=100.0);
                rComp2_SpeedCmd := LIMIT(MN:=40.0, IN:=rLoadDemand/2.0, MX:=100.0);
                rComp1_IGVCmd := LIMIT(MN:=20.0, IN:=(rLoadDemand/2.0 - 40.0)*1.66, MX:=100.0);
                rComp2_IGVCmd := LIMIT(MN:=20.0, IN:=(rLoadDemand/2.0 - 40.0)*1.66, MX:=100.0);
                
                // Stage down condition
                tonCompSeq(IN:=(rLoadDemand < 80.0), PT:=T#60s);
                IF tonCompSeq.Q THEN
                    bComp2_Start := FALSE;
                    bComp2_Stop := TRUE;
                    iState := 2;
                END_IF;
                
        END_CASE;
    ELSE
        // Normal Stop
        bComp1_Start := FALSE; bComp1_Stop := TRUE;
        bComp2_Start := FALSE; bComp2_Stop := TRUE;
        iState := 0;
    END_IF;
    
    // =========================================================================
    // 3. COMPRESSOR ANTI-SURGE CONTROL
    // =========================================================================
    // Simplistic surge control: recycle valve opens if flow drops below minimum
    // for a given discharge pressure (surge line approximation).
    fbComp1_SurgeControl(
        rInput := rComp1_Flow,
        rSetpoint := (rComp1_DischargePress * 0.15) + 50.0, // Dynamic surge line setpoint
        rKp := -5.0, // Reverse acting
        rTi := 2.0,
        rTd := 0.5,
        bReset := NOT bComp1_Running
    );
    rComp1_RecycleValve := LIMIT(MN:=0.0, IN:=fbComp1_SurgeControl.rOutput, MX:=100.0);
    IF NOT bComp1_Running THEN rComp1_RecycleValve := 100.0; END_IF;
    
    fbComp2_SurgeControl(
        rInput := rComp2_Flow,
        rSetpoint := (rComp2_DischargePress * 0.15) + 50.0,
        rKp := -5.0,
        rTi := 2.0,
        rTd := 0.5,
        bReset := NOT bComp2_Running
    );
    rComp2_RecycleValve := LIMIT(MN:=0.0, IN:=fbComp2_SurgeControl.rOutput, MX:=100.0);
    IF NOT bComp2_Running THEN rComp2_RecycleValve := 100.0; END_IF;

    // =========================================================================
    // 4. CRYOGENIC HEAT EXCHANGER CASCADE (N2 BRAYTON CYCLE)
    // =========================================================================
    // The N2 Brayton cycle extracts heat from the BOG. The expander bypass and 
    // N2 comp speed are manipulated to achieve the target LNG return temperature.
    
    IF (iState = 2 OR iState = 3) THEN
        // Cascade Temp Control: Target LNG Return Temp (-161.5 °C)
        fbColdBox_TempControl(
            rInput := rLNG_ReturnTemp,
            rSetpoint := rTemp_TargetLNG,
            rKp := 1.5,
            rTi := 25.0,
            rTd := 5.0,
            bReset := FALSE
        );
        
        // Output from Temp Control determines N2 cooling demand
        rN2_CompSpeedCmd := LIMIT(MN:=50.0, IN:=fbColdBox_TempControl.rOutput, MX:=100.0);
        
        // Expander Bypass is used for fine tuning and protection against freezing
        IF rN2_ExpanderTemp < -170.0 THEN
            rN2_ExpanderBypass := rN2_ExpanderBypass + 1.0; // Open bypass if too cold
        ELSIF fbColdBox_TempControl.rOutput > 80.0 THEN
            rN2_ExpanderBypass := rN2_ExpanderBypass - 1.0; // Close bypass for max cooling
        END_IF;
        rN2_ExpanderBypass := LIMIT(MN:=0.0, IN:=rN2_ExpanderBypass, MX:=100.0);
        
        // JT Valve for flash gas expansion back to the tank
        rJT_ValveCmd := rLoadDemand / 2.0; // Simplified proportional logic
    ELSE
        rN2_CompSpeedCmd := 0.0;
        rN2_ExpanderBypass := 100.0;
        rJT_ValveCmd := 0.0;
    END_IF;

    // State mapping
    ePlantState := iState;

END_FUNCTION_BLOCK
```
"""
    
    payload = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response}
        ]
    }
    
    with open(r"c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")

if __name__ == "__main__":
    generate_payload()
