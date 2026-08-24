import json
import os

path = r"c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"
os.makedirs(os.path.dirname(path), exist_ok=True)

data = {
    "messages": [
        {
            "role": "user",
            "content": "You are the Chief Materials Scientist for an Advanced Synthetic Gemstone & Semiconductor Lab. I need a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for a Microwave Plasma Chemical Vapor Deposition (MPCVD) Monocrystalline Diamond Growth Controller. The FB should be named `FB_MPCVD_DiamondGrowth`.\n\nIt must handle:\n1. Microwave Plasma Resonance: Continuous auto-tuning of a 915 MHz, 100 kW microwave generator using a 3-stub tuner to maintain a perfectly spherical, high-density hydrogen/methane plasma ball hovering exactly 2 mm above the diamond seed plates.\n2. Growth Chemistry & Defect Minimization: Mass flow control of the precise CH4/H2 ratio (< 5% methane) and trace nitrogen doping to control the nitrogen-vacancy (NV) center density for quantum computing applications.\n3. Substrate Temperature Control: Dual-color optical pyrometry maintaining the substrate temperature exactly at 950°C via backside helium jet cooling.\n4. Framework: Strict IEC 61131-3 ST, LREAL datatypes, comprehensive VAR_INPUT/VAR_OUTPUT, and PackML state management."
        },
        {
            "role": "assistant",
            "content": """```iec-st
TYPE E_PackML_State : 
(
    ePackML_Undefined := 0,
    ePackML_Clearing := 1,
    ePackML_Stopped := 2,
    ePackML_Starting := 3,
    ePackML_Idle := 4,
    ePackML_Suspended := 5,
    ePackML_Execute := 6,
    ePackML_Stopping := 7,
    ePackML_Aborting := 8,
    ePackML_Aborted := 9,
    ePackML_Holding := 10,
    ePackML_Held := 11,
    ePackML_Unholding := 12,
    ePackML_Suspending := 13,
    ePackML_Unsuspending := 14,
    ePackML_Resetting := 15,
    ePackML_Completing := 16,
    ePackML_Complete := 17
) DINT;
END_TYPE

FUNCTION_BLOCK FB_PID
VAR_INPUT
    rSetpoint        : LREAL;
    rProcessVariable : LREAL;
    rKp              : LREAL := 1.0;
    rKi              : LREAL := 0.1;
    rKd              : LREAL := 0.01;
END_VAR
VAR_OUTPUT
    rOutput          : LREAL;
END_VAR
VAR
    rIntegral        : LREAL;
    rPrevError       : LREAL;
    rError           : LREAL;
    rDerivative      : LREAL;
END_VAR
(* Simplified PID Implementation *)
rError := rSetpoint - rProcessVariable;
rIntegral := rIntegral + rError;
rDerivative := rError - rPrevError;
rOutput := (rKp * rError) + (rKi * rIntegral) + (rKd * rDerivative);
rPrevError := rError;
IF rOutput > 100.0 THEN rOutput := 100.0; END_IF
IF rOutput < 0.0 THEN rOutput := 0.0; END_IF
END_FUNCTION_BLOCK

FUNCTION_BLOCK FB_3StubTuner
VAR_INPUT
    lrForwardPower   : LREAL;
    lrReflectedPower : LREAL;
END_VAR
VAR_OUTPUT
    lrPos1           : LREAL;
    lrPos2           : LREAL;
    lrPos3           : LREAL;
END_VAR
(* Auto-tuning stubs to minimize Reflected Power *)
lrPos1 := 50.0 - (lrReflectedPower * 0.1);
lrPos2 := 30.0 + (lrReflectedPower * 0.2);
lrPos3 := 10.0 + (lrReflectedPower * 0.05);
END_FUNCTION_BLOCK

FUNCTION_BLOCK FB_MPCVD_DiamondGrowth
VAR_INPUT
    bEnable                : BOOL;   (* Enable MPCVD System *)
    bStartGrowth           : BOOL;   (* Transition from Idle to Growth *)
    bStopGrowth            : BOOL;   (* Abort/Stop Growth *)
    bEmergencyStop         : BOOL;   (* E-Stop triggers Immediate Purge and RF Kill *)
    
    // Sensor Feedback
    lrForwardPower_kW      : LREAL;  (* MW Generator Forward Power Feedback (0-100 kW) *)
    lrReflectedPower_kW    : LREAL;  (* MW Generator Reflected Power Feedback (0-100 kW) *)
    lrPlasmaHeight_mm      : LREAL;  (* Optical feedback of plasma centroid height *)
    
    lrSubstrateTemp_C      : LREAL;  (* Dual-color pyrometer temperature feedback *)
    lrChamberPressure_Torr : LREAL;  (* Chamber pressure *)
    
    lrH2_MassFlow_sccm     : LREAL;  (* Hydrogen flow feedback *)
    lrCH4_MassFlow_sccm    : LREAL;  (* Methane flow feedback *)
    lrN2_MassFlow_sccm     : LREAL;  (* Nitrogen flow feedback *)
    
    // Setpoints
    lrTargetMethaneRatio   : LREAL := 0.04;  (* Ratio of CH4 to H2 (< 0.05) *)
    lrTargetTemp_C         : LREAL := 950.0; (* Substrate Temp via backside He cooling *)
    lrTargetPlasmaHeight_mm: LREAL := 2.0;   (* Plasma height above seed *)
    lrTargetPressure_Torr  : LREAL := 120.0; (* Reactor pressure *)
    lrTargetN2_Doping_ppm  : LREAL := 1.5;   (* For NV center generation *)
END_VAR

VAR_OUTPUT
    ePackML_State          : E_PackML_State;
    
    // Control Outputs
    lrMicrowavePowerCmd_kW : LREAL; 
    lrStub1_Position_mm    : LREAL;
    lrStub2_Position_mm    : LREAL;
    lrStub3_Position_mm    : LREAL;
    
    lrH2_ValveCmd_pct      : LREAL;
    lrCH4_ValveCmd_pct     : LREAL;
    lrN2_ValveCmd_pct      : LREAL;
    
    lrHeCoolingValveCmd_pct: LREAL; (* Backside He jet cooling for temp control *)
    lrVacuumValveCmd_pct   : LREAL; (* Chamber pressure control *)
    
    bSystemReady           : BOOL;
    bGrowthActive          : BOOL;
    bError                 : BOOL;
    sErrorMsg              : STRING(255);
END_VAR

VAR
    // Internal PIDs and Control
    fbTempPID              : FB_PID;
    fbPressurePID          : FB_PID;
    fbPlasmaHeightPID      : FB_PID;
    fbAutoTuner            : FB_3StubTuner; 
    
    // State Machine
    iState                 : INT := 0; 
    
    // Timers
    tonIgnitionTimer       : TON;
    
    // Calculated Internal Variables
    lrCurrentMethaneRatio  : LREAL;
END_VAR

(* =========================================================================
   EMERGENCY STOP & SAFETY INTERLOCKS
   ========================================================================= *)
IF bEmergencyStop THEN
    iState := 0;
    ePackML_State := ePackML_Aborted;
    lrMicrowavePowerCmd_kW := 0.0;
    lrH2_ValveCmd_pct := 0.0;
    lrCH4_ValveCmd_pct := 0.0;
    lrN2_ValveCmd_pct := 0.0;
    lrHeCoolingValveCmd_pct := 100.0; // Max backside cooling on abort to protect substrate
    lrVacuumValveCmd_pct := 100.0;    // Evacuate chamber immediately
    bError := TRUE;
    sErrorMsg := 'EMERGENCY STOP TRIGGERED. RF KILLED. CHAMBER PURGING.';
    bGrowthActive := FALSE;
    RETURN;
END_IF

(* =========================================================================
   MPCVD PACKML STATE MACHINE
   ========================================================================= *)
CASE iState OF
    0: (* RESET / STOPPED *)
        bSystemReady := FALSE;
        bGrowthActive := FALSE;
        lrMicrowavePowerCmd_kW := 0.0;
        IF bEnable AND NOT bError THEN
            iState := 1;
            ePackML_State := ePackML_Idle;
        END_IF
        
    1: (* IDLE *)
        bSystemReady := TRUE;
        lrH2_ValveCmd_pct := 0.0;
        lrCH4_ValveCmd_pct := 0.0;
        lrN2_ValveCmd_pct := 0.0;
        lrVacuumValveCmd_pct := 0.0;
        
        IF bStartGrowth THEN
            iState := 2;
            ePackML_State := ePackML_Starting;
            bSystemReady := FALSE;
        END_IF
        
    2: (* PUMP DOWN & PURGE *)
        lrVacuumValveCmd_pct := 100.0;
        lrH2_ValveCmd_pct := 5.0; // Small purge flow of Hydrogen
        
        IF lrChamberPressure_Torr < 0.1 THEN
            iState := 3;
            tonIgnitionTimer(IN := FALSE);
        END_IF
        
    3: (* H2 PLASMA IGNITION & PRESSURE BUILD *)
        fbPressurePID(
            rSetpoint := 20.0, // Initial strike pressure
            rProcessVariable := lrChamberPressure_Torr,
            rOutput => lrVacuumValveCmd_pct
        );
        
        lrH2_ValveCmd_pct := 50.0; 
        lrMicrowavePowerCmd_kW := 12.5; // Strike power for 915 MHz generator
        
        fbAutoTuner(
            lrForwardPower := lrForwardPower_kW,
            lrReflectedPower := lrReflectedPower_kW,
            lrPos1 => lrStub1_Position_mm,
            lrPos2 => lrStub2_Position_mm,
            lrPos3 => lrStub3_Position_mm
        );
        
        tonIgnitionTimer(IN := TRUE, PT := T#10S);
        IF tonIgnitionTimer.Q THEN
            IF lrReflectedPower_kW < 2.0 AND lrPlasmaHeight_mm > 0.0 THEN
                iState := 4;
            ELSE
                bError := TRUE;
                sErrorMsg := 'Plasma Ignition Failed. High Reflected Power or No Plasma Detected.';
                iState := 0;
            END_IF
        END_IF
        
    4: (* TEMPERATURE & PRESSURE STABILIZATION *)
        ePackML_State := ePackML_Execute;
        
        fbPressurePID(
            rSetpoint := lrTargetPressure_Torr,
            rProcessVariable := lrChamberPressure_Torr,
            rOutput => lrVacuumValveCmd_pct
        );
        
        fbPlasmaHeightPID(
            rSetpoint := lrTargetPlasmaHeight_mm,
            rProcessVariable := lrPlasmaHeight_mm,
            rOutput => lrMicrowavePowerCmd_kW
        );
        
        fbAutoTuner(
            lrForwardPower := lrForwardPower_kW,
            lrReflectedPower := lrReflectedPower_kW,
            lrPos1 => lrStub1_Position_mm,
            lrPos2 => lrStub2_Position_mm,
            lrPos3 => lrStub3_Position_mm
        );
        
        fbTempPID(
            rSetpoint := lrTargetTemp_C,
            rProcessVariable := lrSubstrateTemp_C,
            rKp := 2.5,
            rKi := 0.2,
            rOutput => lrHeCoolingValveCmd_pct
        );
        
        IF ABS(lrSubstrateTemp_C - lrTargetTemp_C) < 1.0 AND ABS(lrChamberPressure_Torr - lrTargetPressure_Torr) < 2.0 THEN
            iState := 5; 
            bGrowthActive := TRUE;
        END_IF
        
    5: (* MONOCRYSTALLINE DIAMOND GROWTH *)
        ePackML_State := ePackML_Execute;
        
        fbPlasmaHeightPID(
            rSetpoint := lrTargetPlasmaHeight_mm,
            rProcessVariable := lrPlasmaHeight_mm,
            rOutput => lrMicrowavePowerCmd_kW
        );
        fbAutoTuner(
            lrForwardPower := lrForwardPower_kW,
            lrReflectedPower := lrReflectedPower_kW,
            lrPos1 => lrStub1_Position_mm,
            lrPos2 => lrStub2_Position_mm,
            lrPos3 => lrStub3_Position_mm
        );
        fbTempPID(
            rSetpoint := lrTargetTemp_C,
            rProcessVariable := lrSubstrateTemp_C,
            rOutput => lrHeCoolingValveCmd_pct
        );
        fbPressurePID(
            rSetpoint := lrTargetPressure_Torr,
            rProcessVariable := lrChamberPressure_Torr,
            rOutput => lrVacuumValveCmd_pct
        );
        
        lrH2_ValveCmd_pct := 85.0;
        IF lrTargetMethaneRatio > 0.045 THEN 
            lrTargetMethaneRatio := 0.045; 
        END_IF
        
        lrCH4_ValveCmd_pct := lrH2_ValveCmd_pct * lrTargetMethaneRatio; 
        lrN2_ValveCmd_pct := (lrTargetN2_Doping_ppm / 1000.0) * 100.0; 
        
        IF bStopGrowth THEN
            iState := 6;
            bGrowthActive := FALSE;
        END_IF
        
    6: (* COOL DOWN & SHUTDOWN SEQUENCE *)
        ePackML_State := ePackML_Completing;
        lrCH4_ValveCmd_pct := 0.0;
        lrN2_ValveCmd_pct := 0.0;
        
        lrMicrowavePowerCmd_kW := lrMicrowavePowerCmd_kW - 0.05;
        IF lrMicrowavePowerCmd_kW <= 0.0 THEN
            lrMicrowavePowerCmd_kW := 0.0;
        END_IF
        
        IF lrSubstrateTemp_C < 100.0 THEN
            lrHeCoolingValveCmd_pct := 0.0;
            lrH2_ValveCmd_pct := 0.0;
            lrVacuumValveCmd_pct := 100.0;
            
            IF lrChamberPressure_Torr < 0.1 THEN
                iState := 1;
                ePackML_State := ePackML_Complete;
            END_IF
        END_IF
END_CASE
```"""
        }
    ]
}

with open(path, "a", encoding="utf-8") as f:
    f.write(json.dumps(data) + "\n")
