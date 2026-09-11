import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Semiconductor PECVD (Plasma Enhanced Chemical Vapor Deposition) System.
Task: Invent a highly complex control scenario for this domain (e.g., RF generator automatic impedance matching, silane/nitrous oxide mass flow controller (MFC) ratio, and chamber capacitance tuning).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

st_code = """```iec-st
FUNCTION_BLOCK FB_PECVD_Process_Control
TITLE = 'Semiconductor PECVD Advanced Control System'
VERSION : '2.1'
AUTHOR : 'Lumina Elite Data Architect'

VAR_INPUT
    bStartProcess : BOOL; // Start deposition process
    bEmergencyStop : BOOL; // System E-Stop
    rTargetChamberPressure : REAL; // Target pressure in mTorr (e.g., 2000)
    rActualChamberPressure : REAL; // Feedback from capacitance manometer
    rTargetTemperature : REAL; // Heater setpoint in Celsius (e.g., 400)
    rActualTemperature : REAL; // Feedback from thermocouple
    rTargetRFPower : REAL; // Target RF Power in Watts (e.g., 600)
    rForwardRFPower : REAL; // Actual forward power from generator
    rReflectedRFPower : REAL; // Reflected power to calculate VSWR
    rSilane_MFC_Setpoint : REAL; // SiH4 Mass Flow Controller Target (sccm)
    rSilane_MFC_Feedback : REAL; // SiH4 Actual Flow
    rNitrous_MFC_Setpoint : REAL; // N2O Mass Flow Controller Target (sccm)
    rNitrous_MFC_Feedback : REAL; // N2O Actual Flow
    rLoadCapacitorPos : REAL; // Matching network load cap (0-100%)
    rTuneCapacitorPos : REAL; // Matching network tune cap (0-100%)
END_VAR

VAR_OUTPUT
    bProcessActive : BOOL;
    bSystemFault : BOOL;
    nFaultCode : INT;
    rThrottleValvePos : REAL; // Chamber pressure control (0-100%)
    rRFGeneratorCmd : REAL; // Command to RF generator (Watts)
    rLoadCapacitorCmd : REAL; // Command to load cap motor
    rTuneCapacitorCmd : REAL; // Command to tune cap motor
    rSilane_MFC_Cmd : REAL; // Command to SiH4 MFC
    rNitrous_MFC_Cmd : REAL; // Command to N2O MFC
    bHeaterEnable : BOOL;
END_VAR

VAR
    // State machine steps
    nProcessState : INT := 0; // 0=IDLE, 1=PUMP_DOWN, 2=HEAT, 3=STABILIZE_GAS, 4=STRIKE_PLASMA, 5=DEPOSITION, 6=PURGE, 7=VENT
    
    // PID for Pressure
    rPressureError : REAL;
    rPressureIntegral : REAL := 0.0;
    rPressureKp : REAL := 0.05;
    rPressureKi : REAL := 0.01;
    
    // Auto-match network algorithm parameters
    rPhaseError : REAL;
    rMagError : REAL;
    rMatchDeadband : REAL := 2.0; // Watts
    
    // Timers
    tDepositionTimer : TON;
    tGasStabilizeTimer : TON;
    tPurgeTimer : TON;
    
    // Constants
    rMaxReflectedPower : REAL := 50.0; // Max allowed reflected power before fault
    rRatio_SiH4_N2O : REAL := 0.0; // Calculated gas ratio
END_VAR

// =========================================================================
// Main Control Logic
// =========================================================================

IF bEmergencyStop THEN
    bProcessActive := FALSE;
    bSystemFault := TRUE;
    nFaultCode := 999;
    nProcessState := 0;
    rThrottleValvePos := 100.0; // Open valve to pump down fully
    rRFGeneratorCmd := 0.0;
    rSilane_MFC_Cmd := 0.0;
    rNitrous_MFC_Cmd := 0.0;
    bHeaterEnable := FALSE;
    RETURN;
END_IF;

CASE nProcessState OF
    0: // IDLE
        bProcessActive := FALSE;
        rRFGeneratorCmd := 0.0;
        rSilane_MFC_Cmd := 0.0;
        rNitrous_MFC_Cmd := 0.0;
        bHeaterEnable := FALSE;
        IF bStartProcess AND NOT bSystemFault THEN
            nProcessState := 1;
            bProcessActive := TRUE;
        END_IF;
        
    1: // PUMP_DOWN
        rThrottleValvePos := 100.0; // Max open
        IF rActualChamberPressure < 10.0 THEN // Base pressure reached
            nProcessState := 2;
        END_IF;
        
    2: // HEAT
        bHeaterEnable := TRUE;
        IF (rActualTemperature >= rTargetTemperature - 5.0) AND (rActualTemperature <= rTargetTemperature + 5.0) THEN
            nProcessState := 3;
            tGasStabilizeTimer(IN:=FALSE); // Reset timer
        END_IF;
        
    3: // STABILIZE_GAS
        rSilane_MFC_Cmd := rSilane_MFC_Setpoint;
        rNitrous_MFC_Cmd := rNitrous_MFC_Setpoint;
        
        // Pressure Control PID
        rPressureError := rTargetChamberPressure - rActualChamberPressure;
        rPressureIntegral := rPressureIntegral + (rPressureError * 0.1);
        IF rPressureIntegral > 100.0 THEN rPressureIntegral := 100.0; END_IF;
        IF rPressureIntegral < 0.0 THEN rPressureIntegral := 0.0; END_IF;
        
        // Throttle valve acts inversely to pressure error (if pressure too high, open valve more)
        rThrottleValvePos := 50.0 - (rPressureError * rPressureKp) - rPressureKi * rPressureIntegral;
        IF rThrottleValvePos > 100.0 THEN rThrottleValvePos := 100.0; END_IF;
        IF rThrottleValvePos < 0.0 THEN rThrottleValvePos := 0.0; END_IF;
        
        tGasStabilizeTimer(IN:=TRUE, PT:=T#15S);
        IF tGasStabilizeTimer.Q THEN
            nProcessState := 4;
        END_IF;
        
    4: // STRIKE_PLASMA
        rRFGeneratorCmd := rTargetRFPower;
        
        // Initial match network positions
        rLoadCapacitorCmd := 45.0; 
        rTuneCapacitorCmd := 55.0;
        
        IF (rForwardRFPower > rTargetRFPower * 0.9) AND (rReflectedRFPower < 20.0) THEN
            nProcessState := 5;
            tDepositionTimer(IN:=FALSE);
        END_IF;
        
    5: // DEPOSITION & AUTO-MATCH
        rRFGeneratorCmd := rTargetRFPower;
        tDepositionTimer(IN:=TRUE, PT:=T#120S); // e.g., 2 minute deposition
        
        // Advanced Auto-Impedance Matching Algorithm
        // simplified logic assuming ReflectedPower correlates to mismatch
        IF rReflectedRFPower > rMatchDeadband THEN
            IF rReflectedRFPower > rMaxReflectedPower THEN
                // Fault condition
                bSystemFault := TRUE;
                nFaultCode := 101; // High Reflected Power Fault
                nProcessState := 6; // Go to purge
            ELSE
                // Adjust tune and load capacitors to minimize reflected power
                rTuneCapacitorCmd := rTuneCapacitorPos - (rReflectedRFPower * 0.01);
                rLoadCapacitorCmd := rLoadCapacitorPos + (rReflectedRFPower * 0.01);
                
                // Clamp
                IF rTuneCapacitorCmd > 100.0 THEN rTuneCapacitorCmd := 100.0; END_IF;
                IF rTuneCapacitorCmd < 0.0 THEN rTuneCapacitorCmd := 0.0; END_IF;
                IF rLoadCapacitorCmd > 100.0 THEN rLoadCapacitorCmd := 100.0; END_IF;
                IF rLoadCapacitorCmd < 0.0 THEN rLoadCapacitorCmd := 0.0; END_IF;
            END_IF;
        END_IF;
        
        IF tDepositionTimer.Q THEN
            nProcessState := 6;
            tPurgeTimer(IN:=FALSE);
        END_IF;
        
    6: // PURGE
        rRFGeneratorCmd := 0.0; // RF off
        rSilane_MFC_Cmd := 0.0; // Reactive gas off
        rNitrous_MFC_Cmd := 0.0;
        rThrottleValvePos := 100.0; 
        
        tPurgeTimer(IN:=TRUE, PT:=T#30S);
        IF tPurgeTimer.Q THEN
            nProcessState := 0; // Back to idle
            bProcessActive := FALSE;
        END_IF;
        
    ELSE
        nProcessState := 0;
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
print(f"Success! Saved to {filename}")
