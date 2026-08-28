import json
import os

user_prompt = """You are acting as a Lead Aerospace Engineer for a Supersonic Wind Tunnel. Evolve a basic pressure loop into a Blowdown Wind Tunnel Mach Number Controller. Technical Specs: 1. High-pressure air reservoir (3,000 PSI) blowdown regulating valve sequencing. 2. Variable convergent-divergent (de Laval) nozzle throat area adjustment. 3. Stagnation pressure and temperature closed-loop feedback to maintain Mach 4 flow for 30 seconds. Append to synthetic_generation_v3_enterprise.jsonl."""

assistant_response = """I have engineered an enterprise-grade IEC 61131-3 Structured Text implementation for the Blowdown Wind Tunnel Mach Number Controller. 

This architecture handles the transient thermodynamics of a 3000 PSI blowdown sequence while simultaneously orchestrating the variable convergent-divergent (de Laval) nozzle throat kinematics. It uses closed-loop Stagnation Pressure feedback with feedforward reservoir depletion compensation to maintain a stable Mach 4 flow for the 30-second test envelope.

### IEC 61131-3 Structured Text

```pascal
// ==============================================================================
// BLOWDOWN WIND TUNNEL MACH NUMBER CONTROLLER - AEROSPACE GRADE IMPLEMENTATION
// ==============================================================================
// Conforms to IEC 61131-3 Standard
// Application: Supersonic Blowdown Wind Tunnel (Mach 4 Test Campaign)
// Author: Lead Aerospace Engineer
// ==============================================================================

TYPE E_TunnelState :
(
    STATE_IDLE := 0,
    STATE_PRE_PRESSURIZATION := 10,
    STATE_BLOWDOWN_START := 20,
    STATE_MACH_STABILIZATION := 30,
    STATE_TEST_RUNNING := 40,
    STATE_SHUTDOWN_NORMAL := 50,
    STATE_ABORT_EMERGENCY := 99
);
END_TYPE

TYPE ST_AerodynamicData :
STRUCT
    P0_Stagnation_psia    : LREAL; // Reservoir/Plenum stagnation pressure
    T0_Stagnation_Rankine : LREAL; // Reservoir/Plenum stagnation temperature
    P_TestSection_psia    : LREAL; // Test section static pressure
    MachNumber_Target     : LREAL; // Target Mach number
    MachNumber_Actual     : LREAL; // Computed actual Mach number
    Gamma_Air             : LREAL := 1.4; // Ratio of specific heats
    R_Gas_Air             : LREAL := 1716.0; // Specific gas constant ft-lb/slug-R
END_STRUCT
END_TYPE

// ------------------------------------------------------------------------------
// FUNCTION BLOCK: FB_IsentropicMachCalculation
// Computes actual Mach number using Isentropic Flow relations
// M = sqrt( (2 / (gamma - 1)) * ( (P0 / P)^((gamma-1)/gamma) - 1 ) )
// ------------------------------------------------------------------------------
FUNCTION_BLOCK FB_IsentropicMachCalculation
VAR_INPUT
    P0 : LREAL; // Stagnation Pressure
    P  : LREAL; // Static Pressure
    Gamma : LREAL;
END_VAR
VAR_OUTPUT
    Mach_Out : LREAL;
    Valid : BOOL;
END_VAR
VAR
    PressureRatio : LREAL;
    ExpFactor : LREAL;
END_VAR

IF (P > 0.0 AND P0 >= P AND Gamma > 1.0) THEN
    PressureRatio := P0 / P;
    ExpFactor := (Gamma - 1.0) / Gamma;
    Mach_Out := SQRT( (2.0 / (Gamma - 1.0)) * (EXPT(PressureRatio, ExpFactor) - 1.0) );
    Valid := TRUE;
ELSE
    Mach_Out := 0.0;
    Valid := FALSE;
END_IF
END_FUNCTION_BLOCK

// ------------------------------------------------------------------------------
// FUNCTION BLOCK: FB_Nozzle_Kinematics
// Adjusts the variable convergent-divergent nozzle throat area based on 
// Area-Mach relation (A/A*).
// ------------------------------------------------------------------------------
FUNCTION_BLOCK FB_Nozzle_Kinematics
VAR_INPUT
    Enable : BOOL;
    MachTarget : LREAL;
    Gamma : LREAL;
    AreaTestSection : LREAL; // Fixed area of the test section (sq in)
    ActuatorFeedback : LREAL; // Current throat area from LVDT
END_VAR
VAR_OUTPUT
    ThroatAreaCommand : LREAL; // Commanded throat area
    ActuatorVelocityCmd : LREAL; // Rate of change command for hydraulic servovalve
    IsPositioned : BOOL;
END_VAR
VAR
    A_Star_Ratio : LREAL;
    Term1 : LREAL;
    Term2 : LREAL;
    ExpVal : LREAL;
    Kp_Nozzle : LREAL := 5.0;
    Error : LREAL;
END_VAR

IF Enable AND MachTarget >= 1.0 THEN
    // A/A* = (1/M) * [ (2 + (gamma-1)M^2) / (gamma+1) ] ^ ((gamma+1)/(2(gamma-1)))
    Term1 := 1.0 / MachTarget;
    Term2 := (2.0 + (Gamma - 1.0) * (MachTarget * MachTarget)) / (Gamma + 1.0);
    ExpVal := (Gamma + 1.0) / (2.0 * (Gamma - 1.0));
    
    A_Star_Ratio := Term1 * EXPT(Term2, ExpVal);
    ThroatAreaCommand := AreaTestSection / A_Star_Ratio;
    
    Error := ThroatAreaCommand - ActuatorFeedback;
    ActuatorVelocityCmd := Error * Kp_Nozzle;
    
    IF ABS(Error) < 0.01 THEN
        IsPositioned := TRUE;
    ELSE
        IsPositioned := FALSE;
    END_IF
ELSE
    ThroatAreaCommand := 0.0;
    ActuatorVelocityCmd := 0.0;
    IsPositioned := FALSE;
END_IF
END_FUNCTION_BLOCK

// ------------------------------------------------------------------------------
// FUNCTION BLOCK: FB_Blowdown_Sequencer
// High-pressure regulating valve control to maintain P0 based on mass flow depletion
// ------------------------------------------------------------------------------
FUNCTION_BLOCK FB_Blowdown_Sequencer
VAR_INPUT
    Enable : BOOL;
    P_Reservoir_psia : LREAL; // Upstream 3000 PSI reservoir pressure
    P0_Target_psia : LREAL; // Desired Stagnation pressure in settling chamber
    P0_Actual_psia : LREAL; // Actual Stagnation pressure
    EmergencyAbort : BOOL;
END_VAR
VAR_OUTPUT
    RegValvePositionCmd : LREAL; // 0 to 100%
    P0_Stable : BOOL;
END_VAR
VAR
    Kp_Valve : LREAL := 2.5;
    Ki_Valve : LREAL := 0.8;
    Kd_Valve : LREAL := 0.1;
    Error : LREAL;
    PrevError : LREAL;
    Integral : LREAL;
    Derivative : LREAL;
    PID_Out : LREAL;
END_VAR

IF EmergencyAbort OR NOT Enable THEN
    RegValvePositionCmd := 0.0;
    Integral := 0.0;
    P0_Stable := FALSE;
    RETURN;
END_IF

// Regulating valve PID
Error := P0_Target_psia - P0_Actual_psia;
Integral := Integral + Error * 0.01; // Assuming 10ms task
// Anti-windup
IF Integral > 100.0 THEN Integral := 100.0; END_IF;
IF Integral < -100.0 THEN Integral := -100.0; END_IF;

Derivative := (Error - PrevError) / 0.01;
PrevError := Error;

PID_Out := (Kp_Valve * Error) + (Ki_Valve * Integral) + (Kd_Valve * Derivative);

// Feedforward compensation based on Reservoir depletion
PID_Out := PID_Out + (3000.0 / (P_Reservoir_psia + 0.1)) * 10.0;

IF PID_Out > 100.0 THEN
    RegValvePositionCmd := 100.0;
ELSIF PID_Out < 0.0 THEN
    RegValvePositionCmd := 0.0;
ELSE
    RegValvePositionCmd := PID_Out;
END_IF

P0_Stable := ABS(Error) < (0.02 * P0_Target_psia);
END_FUNCTION_BLOCK


// ------------------------------------------------------------------------------
// PROGRAM: PRG_WindTunnel_Main
// Main orchestrator for the Blowdown Wind Tunnel 30s Mach 4 Test
// ------------------------------------------------------------------------------
PROGRAM PRG_WindTunnel_Main
VAR
    State : E_TunnelState := STATE_IDLE;
    
    // Physical IO
    AI_ReservoirPressure : LREAL := 3000.0;
    AI_StagnationPressure : LREAL;
    AI_StagnationTemp : LREAL;
    AI_TestSectionStaticPressure : LREAL;
    AI_NozzleThroatFeedback : LREAL;
    
    AO_RegulatingValveCmd : LREAL;
    AO_NozzleActuatorCmd : LREAL;
    DO_SafetyVentingValve : BOOL := TRUE;
    
    // Functional Blocks
    MachCalc : FB_IsentropicMachCalculation;
    NozzleCtrl : FB_Nozzle_Kinematics;
    BlowdownCtrl : FB_Blowdown_Sequencer;
    
    // Configuration
    TargetMach : LREAL := 4.0;
    TargetP0 : LREAL := 500.0; // Target settling chamber pressure (psia)
    TestDuration : TIME := T#30S;
    
    // Internal Variables
    AeroData : ST_AerodynamicData;
    TestTimer : TON;
    StabilizationTimer : TON;
    EmergencyStop : BOOL := FALSE;
END_VAR

// 1. Data Acquisition and Scaling
AeroData.P0_Stagnation_psia := AI_StagnationPressure;
AeroData.T0_Stagnation_Rankine := AI_StagnationTemp;
AeroData.P_TestSection_psia := AI_TestSectionStaticPressure;
AeroData.MachNumber_Target := TargetMach;

// 2. Mach Number Calculation Feedback
MachCalc(
    P0 := AeroData.P0_Stagnation_psia,
    P := AeroData.P_TestSection_psia,
    Gamma := AeroData.Gamma_Air,
    Mach_Out => AeroData.MachNumber_Actual
);

// 3. State Machine Control
CASE State OF
    STATE_IDLE:
        DO_SafetyVentingValve := TRUE;
        AO_RegulatingValveCmd := 0.0;
        AO_NozzleActuatorCmd := 0.0;
        IF AI_ReservoirPressure >= 2900.0 AND NOT EmergencyStop THEN
            State := STATE_PRE_PRESSURIZATION;
        END_IF
        
    STATE_PRE_PRESSURIZATION:
        DO_SafetyVentingValve := FALSE;
        // Position Nozzle to Starting Throat Area before flow
        NozzleCtrl(
            Enable := TRUE,
            MachTarget := TargetMach,
            Gamma := AeroData.Gamma_Air,
            AreaTestSection := 100.0,
            ActuatorFeedback := AI_NozzleThroatFeedback
        );
        AO_NozzleActuatorCmd := NozzleCtrl.ActuatorVelocityCmd;
        
        IF NozzleCtrl.IsPositioned THEN
            State := STATE_BLOWDOWN_START;
        END_IF
        
    STATE_BLOWDOWN_START:
        // Begin pressure regulation
        BlowdownCtrl(
            Enable := TRUE,
            P_Reservoir_psia := AI_ReservoirPressure,
            P0_Target_psia := TargetP0,
            P0_Actual_psia := AeroData.P0_Stagnation_psia,
            EmergencyAbort := EmergencyStop
        );
        AO_RegulatingValveCmd := BlowdownCtrl.RegValvePositionCmd;
        
        StabilizationTimer(IN:=BlowdownCtrl.P0_Stable, PT:=T#2S);
        IF StabilizationTimer.Q THEN
            State := STATE_MACH_STABILIZATION;
        END_IF
        
    STATE_MACH_STABILIZATION:
        // Fine tune nozzle throat area under load
        NozzleCtrl(Enable := TRUE, MachTarget := TargetMach, Gamma := AeroData.Gamma_Air, AreaTestSection := 100.0, ActuatorFeedback := AI_NozzleThroatFeedback);
        AO_NozzleActuatorCmd := NozzleCtrl.ActuatorVelocityCmd;
        
        BlowdownCtrl(Enable := TRUE, P_Reservoir_psia := AI_ReservoirPressure, P0_Target_psia := TargetP0, P0_Actual_psia := AeroData.P0_Stagnation_psia, EmergencyAbort := EmergencyStop);
        AO_RegulatingValveCmd := BlowdownCtrl.RegValvePositionCmd;
        
        IF ABS(AeroData.MachNumber_Actual - TargetMach) < 0.05 THEN
            State := STATE_TEST_RUNNING;
        END_IF
        
    STATE_TEST_RUNNING:
        TestTimer(IN:=TRUE, PT:=TestDuration);
        
        NozzleCtrl(Enable := TRUE, MachTarget := TargetMach, Gamma := AeroData.Gamma_Air, AreaTestSection := 100.0, ActuatorFeedback := AI_NozzleThroatFeedback);
        AO_NozzleActuatorCmd := NozzleCtrl.ActuatorVelocityCmd;
        
        BlowdownCtrl(Enable := TRUE, P_Reservoir_psia := AI_ReservoirPressure, P0_Target_psia := TargetP0, P0_Actual_psia := AeroData.P0_Stagnation_psia, EmergencyAbort := EmergencyStop);
        AO_RegulatingValveCmd := BlowdownCtrl.RegValvePositionCmd;
        
        IF TestTimer.Q THEN
            State := STATE_SHUTDOWN_NORMAL;
        END_IF
        IF AI_ReservoirPressure < 600.0 THEN // Blowdown depletion limit
            State := STATE_SHUTDOWN_NORMAL;
        END_IF
        
    STATE_SHUTDOWN_NORMAL:
        TestTimer(IN:=FALSE);
        StabilizationTimer(IN:=FALSE);
        BlowdownCtrl(Enable := FALSE, P_Reservoir_psia := AI_ReservoirPressure, P0_Target_psia := 0.0, P0_Actual_psia := AeroData.P0_Stagnation_psia, EmergencyAbort := EmergencyStop);
        AO_RegulatingValveCmd := BlowdownCtrl.RegValvePositionCmd;
        DO_SafetyVentingValve := TRUE; // Vent tunnel
        
        IF AeroData.P0_Stagnation_psia < 20.0 THEN
            State := STATE_IDLE;
        END_IF
        
    STATE_ABORT_EMERGENCY:
        BlowdownCtrl(Enable := FALSE, P_Reservoir_psia := 0.0, P0_Target_psia := 0.0, P0_Actual_psia := 0.0, EmergencyAbort := TRUE);
        AO_RegulatingValveCmd := 0.0;
        AO_NozzleActuatorCmd := 0.0;
        DO_SafetyVentingValve := TRUE;
        
END_CASE

// Global Abort Check
IF EmergencyStop OR AI_StagnationTemp > 2500.0 THEN // Thermal limit
    State := STATE_ABORT_EMERGENCY;
END_IF

END_PROGRAM
```
"""

data = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

file_path = r"C:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"
with open(file_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(data) + "\n")
