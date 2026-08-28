import json, uuid, os

st_code = """```iec-st
FUNCTION_BLOCK FB_DAC_MultiStage_Controller
TITLE = 'Carbon Capture Direct Air Capture System Controller'
VERSION : '2.1'
AUTHOR : 'Lumina Elite Synthetic Data Architect'

VAR_INPUT
    bSystemEnable : BOOL; // Main system enable flag
    bEmergencyStop : BOOL; // Safety interlock, active low
    
    // Ambient and Air Handling Inputs
    rAmbientTemp : REAL; // Ambient temperature [C]
    rAirflowRate : REAL; // Measured intake airflow [m3/s]
    rInletCO2Conc : REAL; // Inlet CO2 concentration [ppm]
    rOutletCO2Conc : REAL; // Outlet CO2 concentration [ppm]
    
    // Thermal Sorbent Regeneration Inputs
    rSorbentTemp : REAL; // Sorbent bed temperature [C]
    rDesorptionPressure : REAL; // Vacuum/Pressure in desorption chamber [bar]
    
    // Multi-stage Compression Inputs
    rCompStage1_Pressure : REAL; // Stage 1 Discharge Pressure [bar]
    rCompStage2_Pressure : REAL; // Stage 2 Discharge Pressure [bar]
    rCompStage3_Pressure : REAL; // Stage 3 Discharge Pressure [bar]
    rLiquefactionTemp : REAL; // Cryogenic cooler temp [C]
    
    // Utility Inputs
    bSteamAvailable : BOOL;
    bCoolingWaterAvailable : BOOL;
END_VAR

VAR_OUTPUT
    // Fan Array Outputs
    rFanSpeedSetpoint : REAL; // 0-100% speed command for VFDs
    bFanArrayEnable : BOOL;
    
    // Regeneration Outputs
    bSteamValveOpen : BOOL; // Open steam injection for amine heating
    rVacuumPumpSpeed : REAL; // Speed command for vacuum recovery
    
    // Compressor Outputs
    bCompressor1_Run : BOOL;
    bCompressor2_Run : BOOL;
    bCompressor3_Run : BOOL;
    rCryoChillerSetPoint : REAL; // Temp setpoint for cryogenic stage
    
    // System Status
    iCurrentState : INT; // 0:Off, 1:Adsorb, 2:PreHeat, 3:Desorb, 4:Cool, 99:Fault
    rCalculatedCaptureRate : REAL; // kg/hr CO2 captured
    bSystemFault : BOOL;
    sFaultCode : STRING[32];
END_VAR

VAR
    // Internal State Machine
    eState : (STATE_OFF, STATE_ADSORPTION, STATE_PREHEAT, STATE_DESORPTION, STATE_COMPRESSION, STATE_COOLING, STATE_FAULT);
    
    // Timers
    tAdsorptionTimer : TON;
    tDesorptionTimer : TON;
    tCoolingTimer : TON;
    
    // PID Controllers (Simulated representation)
    rFanPID_Integral : REAL := 0.0;
    rTempPID_Integral : REAL := 0.0;
    
    // Internal calculations
    rDeltaCO2 : REAL;
    rCaptureEfficiency : REAL;
    
    // Constants
    c_rMaxAdsorptionTime : TIME := T#120M;
    c_rMaxDesorptionTime : TIME := T#45M;
    c_rTargetDesorbTemp : REAL := 95.0; // C for amine regeneration
    c_rCryoTargetTemp : REAL := -35.0; // C for CO2 liquefaction
END_VAR

// -----------------------------------------------------------------------------
// MAIN CONTROL LOGIC
// -----------------------------------------------------------------------------

// 1. Safety and Interlocks
IF NOT bEmergencyStop THEN
    eState := STATE_FAULT;
    sFaultCode := 'E-STOP ACTIVATED';
    bSystemFault := TRUE;
ELSIF NOT bCoolingWaterAvailable OR NOT bSteamAvailable THEN
    eState := STATE_FAULT;
    sFaultCode := 'UTILITY LOSS';
    bSystemFault := TRUE;
END_IF;

// 2. State Machine Evaluation
CASE eState OF
    
    STATE_OFF:
        bSystemFault := FALSE;
        sFaultCode := 'OK';
        bFanArrayEnable := FALSE;
        bSteamValveOpen := FALSE;
        rFanSpeedSetpoint := 0.0;
        bCompressor1_Run := FALSE;
        bCompressor2_Run := FALSE;
        bCompressor3_Run := FALSE;
        
        IF bSystemEnable THEN
            eState := STATE_ADSORPTION;
        END_IF;
        
    STATE_ADSORPTION:
        // Activate Massive Air Handling Fan Arrays
        bFanArrayEnable := TRUE;
        
        // Simple PI Control for Fan Speed based on CO2 capture efficiency
        rDeltaCO2 := rInletCO2Conc - rOutletCO2Conc;
        IF rDeltaCO2 < 100.0 THEN // Sorbent saturating, push more air or prepare to switch
            rFanSpeedSetpoint := 100.0;
        ELSE
            rFanSpeedSetpoint := 75.0; // Cruise speed
        END_IF;
        
        // Timer for adsorption cycle
        tAdsorptionTimer(IN := TRUE, PT := c_rMaxAdsorptionTime);
        
        // Transition condition: Timer done or sorbent saturated
        IF tAdsorptionTimer.Q OR (rDeltaCO2 < 20.0 AND tAdsorptionTimer.ET > T#30M) THEN
            tAdsorptionTimer(IN := FALSE); // Reset timer
            bFanArrayEnable := FALSE;
            rFanSpeedSetpoint := 0.0;
            eState := STATE_PREHEAT;
        END_IF;
        
    STATE_PREHEAT:
        // Amine sorbent regeneration thermal cycling starts
        bSteamValveOpen := TRUE;
        
        IF rSorbentTemp >= c_rTargetDesorbTemp THEN
            eState := STATE_DESORPTION;
        END_IF;
        
    STATE_DESORPTION:
        // Hold temperature and pull vacuum to extract CO2
        bSteamValveOpen := (rSorbentTemp < c_rTargetDesorbTemp + 2.0); // Simple thermostat logic
        rVacuumPumpSpeed := 90.0;
        
        tDesorptionTimer(IN := TRUE, PT := c_rMaxDesorptionTime);
        
        // Multi-stage cryogenic CO2 compression engages once pressure builds
        IF rDesorptionPressure > 0.5 THEN
            eState := STATE_COMPRESSION;
        END_IF;
        
        IF tDesorptionTimer.Q THEN
            tDesorptionTimer(IN := FALSE);
            bSteamValveOpen := FALSE;
            rVacuumPumpSpeed := 0.0;
            eState := STATE_COOLING;
        END_IF;
        
    STATE_COMPRESSION:
        // Multi-Stage CO2 Compression Logic
        bCompressor1_Run := TRUE;
        
        IF rCompStage1_Pressure > 5.0 THEN
            bCompressor2_Run := TRUE;
        END_IF;
        
        IF rCompStage2_Pressure > 20.0 THEN
            bCompressor3_Run := TRUE;
        END_IF;
        
        rCryoChillerSetPoint := c_rCryoTargetTemp;
        
        // Return to desorption monitoring
        eState := STATE_DESORPTION;
        
    STATE_COOLING:
        // Cool down the sorbent bed before next adsorption phase
        // Requires cooling water circulation (abstracted to time delay here)
        tCoolingTimer(IN := TRUE, PT := T#15M);
        
        IF tCoolingTimer.Q THEN
            tCoolingTimer(IN := FALSE);
            IF bSystemEnable THEN
                eState := STATE_ADSORPTION;
            ELSE
                eState := STATE_OFF;
            END_IF;
        END_IF;
        
    STATE_FAULT:
        // Safe state enforcement
        bFanArrayEnable := FALSE;
        bSteamValveOpen := FALSE;
        rFanSpeedSetpoint := 0.0;
        bCompressor1_Run := FALSE;
        bCompressor2_Run := FALSE;
        bCompressor3_Run := FALSE;
        rVacuumPumpSpeed := 0.0;
        
        IF NOT bEmergencyStop AND bCoolingWaterAvailable AND bSteamAvailable AND NOT bSystemEnable THEN
            // Reset fault if conditions clear and system is disabled
            eState := STATE_OFF;
        END_IF;
        
    ELSE
        eState := STATE_FAULT;
        sFaultCode := 'INVALID STATE';
END_CASE;

// Map internal state to output
iCurrentState := eState;

// Simple calculation for UI/SCADA tracking
IF bFanArrayEnable THEN
    rCalculatedCaptureRate := rAirflowRate * (rDeltaCO2 / 1000000.0) * 1.225 * 3600.0; // Approximate kg/hr
ELSE
    rCalculatedCaptureRate := 0.0;
END_IF;

END_FUNCTION_BLOCK
```"""

user_prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\\nYour specific domain is: Carbon Capture Direct Air Capture (DAC).\\nTask: Invent a highly complex control scenario for this domain (e.g., amine sorbent regeneration thermal cycling, multi-stage cryogenic CO2 compression, and massive air handling fan arrays).\\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

record = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": st_code}
    ]
}

# 1. Swarm directory file
os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

# 2. Append to jsonl
os.makedirs("data", exist_ok=True)
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
