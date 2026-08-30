import json
import os
import uuid

prompt = "Invent a highly complex control scenario for a Laser Tube Cutting Machine, including chuck rotary axis interpolation, capacitive height sensor dynamic tracking, and assist gas proportional valve loops. Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

code = """FUNCTION_BLOCK FB_LaserTubeCutter_Core
TITLE = 'Laser Tube Cutting Control Core'
VERSION : '1.0'

VAR_INPUT
    bEnable : BOOL; // System enable
    bStartCut : BOOL; // Start cutting sequence
    rTargetPositionX : REAL; // Linear axis target (mm)
    rTargetAngleC : REAL; // Rotary axis target (deg)
    rFeedRate : REAL; // Cutting feed rate (mm/min)
    rMaterialThickness : REAL; // Tube wall thickness (mm)
    
    // Sensor Inputs
    rCapacitiveHeight : REAL; // Actual standoff distance from nozzle to tube (mm)
    rGasPressureAct : REAL; // Actual assist gas pressure (bar)
    rLaserPowerAct : REAL; // Actual laser power (W)
    
    // Safety & Limits
    bChillerOk : BOOL;
    bGasSupplyOk : BOOL;
    bSafetyGuardsClosed : BOOL;
END_VAR

VAR_OUTPUT
    bReady : BOOL;
    bActive : BOOL;
    bError : BOOL;
    nErrorID : WORD;
    
    // Actuator Commands
    rCmdVelocityX : REAL; // Linear axis command
    rCmdVelocityC : REAL; // Rotary axis command
    rCmdHeightZ : REAL; // Height control Z axis command
    
    // Laser & Gas Commands
    rCmdLaserPower : REAL; // Commanded laser power (W)
    bLaserEmissionOn : BOOL;
    rCmdGasValve : REAL; // Proportional gas valve command (0-10V or 0-100%)
END_VAR

VAR
    // State Machine
    eState : (INIT, IDLE, PIERCE, CUTTING, RETRACT, FAULT);
    
    // Height Control PID
    rHeightSetpoint : REAL := 1.0; // 1mm standoff
    rHeightError : REAL;
    rHeightIntegral : REAL;
    rHeightKp : REAL := 5.5;
    rHeightKi : REAL := 0.2;
    
    // Gas Control PID
    rGasSetpoint : REAL;
    rGasError : REAL;
    rGasIntegral : REAL;
    rGasKp : REAL := 2.0;
    rGasKi : REAL := 0.5;
    
    // Interpolation
    rCurrentX : REAL;
    rCurrentC : REAL;
    rPathLength : REAL;
    
    // Timers
    tPierceTimer : TON;
    tSettleTimer : TON;
END_VAR

// Control Logic
IF NOT bEnable OR NOT bSafetyGuardsClosed OR NOT bChillerOk OR NOT bGasSupplyOk THEN
    eState := FAULT;
    nErrorID := 16#1001;
END_VAR;

CASE eState OF
    INIT:
        bReady := FALSE;
        bActive := FALSE;
        bError := FALSE;
        nErrorID := 0;
        bLaserEmissionOn := FALSE;
        rCmdVelocityX := 0.0;
        rCmdVelocityC := 0.0;
        rCmdHeightZ := 0.0;
        rCmdLaserPower := 0.0;
        rCmdGasValve := 0.0;
        IF bEnable THEN
            eState := IDLE;
        END_IF;
        
    IDLE:
        bReady := TRUE;
        bActive := FALSE;
        IF bStartCut THEN
            bReady := FALSE;
            bActive := TRUE;
            eState := PIERCE;
            tPierceTimer(IN := FALSE); // Reset timer
        END_IF;
        
    PIERCE:
        // Set piercing parameters
        rHeightSetpoint := 2.5; // Higher standoff for piercing
        rCmdLaserPower := 1500.0; // Piercing power
        rGasSetpoint := 3.0; // Low pressure for piercing
        
        bLaserEmissionOn := TRUE;
        
        tPierceTimer(IN := TRUE, PT := T#500MS);
        IF tPierceTimer.Q THEN
            eState := CUTTING;
        END_IF;
        
    CUTTING:
        // Cutting parameters
        rHeightSetpoint := 1.0; // Optimal cutting standoff
        rCmdLaserPower := 3000.0; // Cutting power
        rGasSetpoint := 12.0; // High pressure for cutting
        
        // Chuck and Linear Interpolation (Simplified Outline)
        // Ensure constant surface speed considering rotary axis C and linear X
        rPathLength := SQRT((rTargetPositionX - rCurrentX)*(rTargetPositionX - rCurrentX) + 
                            (rTargetAngleC - rCurrentC)*(rTargetAngleC - rCurrentC)); // Simplified
                            
        IF rPathLength > 0.1 THEN
            rCmdVelocityX := (rTargetPositionX - rCurrentX) / rPathLength * rFeedRate;
            rCmdVelocityC := (rTargetAngleC - rCurrentC) / rPathLength * rFeedRate;
        ELSE
            rCmdVelocityX := 0.0;
            rCmdVelocityC := 0.0;
            eState := RETRACT;
        END_IF;
        
    RETRACT:
        bLaserEmissionOn := FALSE;
        rCmdLaserPower := 0.0;
        rGasSetpoint := 0.0;
        rHeightSetpoint := 10.0; // Retract Z
        
        IF rCapacitiveHeight > 9.5 THEN
            eState := IDLE;
        END_IF;
        
    FAULT:
        bError := TRUE;
        bReady := FALSE;
        bActive := FALSE;
        bLaserEmissionOn := FALSE;
        rCmdLaserPower := 0.0;
        rCmdVelocityX := 0.0;
        rCmdVelocityC := 0.0;
        rCmdGasValve := 0.0;
        rCmdHeightZ := 0.0;
        
        IF NOT bEnable THEN
            bError := FALSE;
            eState := INIT;
        END_IF;
END_CASE;

// Capacitive Height Sensor Dynamic Tracking (PI Control)
rHeightError := rHeightSetpoint - rCapacitiveHeight;
IF bActive THEN
    rHeightIntegral := rHeightIntegral + (rHeightError * 0.01); // Assuming 10ms cycle
    rCmdHeightZ := (rHeightKp * rHeightError) + (rHeightKi * rHeightIntegral);
    
    // Anti-windup
    IF rCmdHeightZ > 100.0 THEN rCmdHeightZ := 100.0; rHeightIntegral := rHeightIntegral - (rHeightError * 0.01); END_IF;
    IF rCmdHeightZ < -100.0 THEN rCmdHeightZ := -100.0; rHeightIntegral := rHeightIntegral - (rHeightError * 0.01); END_IF;
ELSE
    rHeightIntegral := 0.0;
END_IF;

// Assist Gas Proportional Valve Loop (PI Control)
rGasError := rGasSetpoint - rGasPressureAct;
IF bActive THEN
    rGasIntegral := rGasIntegral + (rGasError * 0.01);
    rCmdGasValve := (rGasKp * rGasError) + (rGasKi * rGasIntegral);
    
    // Anti-windup limits 0-100%
    IF rCmdGasValve > 100.0 THEN rCmdGasValve := 100.0; rGasIntegral := rGasIntegral - (rGasError * 0.01); END_IF;
    IF rCmdGasValve < 0.0 THEN rCmdGasValve := 0.0; rGasIntegral := 0.0; END_IF;
ELSE
    rGasIntegral := 0.0;
END_IF;

END_FUNCTION_BLOCK
"""

msg = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": f"```iec-st\n{code}\n```"}
    ]
}

os.makedirs("c:/Users/majip/Downloads/LLM REASEARCH/data", exist_ok=True)
with open("c:/Users/majip/Downloads/LLM REASEARCH/data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(msg) + "\n")

os.makedirs("c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw", exist_ok=True)
file_id = uuid.uuid4().hex[:8]
with open(f"c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_{file_id}.json", "w", encoding="utf-8") as f:
    json.dump(msg, f)
