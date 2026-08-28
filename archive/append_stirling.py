import json

content = """FUNCTION_BLOCK FB_AIP_StirlingEngineController
TITLE = 'Submarine AIP Stirling Engine Controller'
AUTHOR : 'Lumina Elite Synthetic Data Architect'
VERSION : '1.0'
// This FB controls an Air-Independent Propulsion Stirling Engine.
// Incorporates 30 bar LOX/Diesel combustion, Helium thermodynamic cycle tracking,
// and Active Acoustic Signature Dampening.

VAR_INPUT
    bEnable                  : BOOL; // Enable AIP system
    rPowerDemand_kW          : REAL; // Desired power output in kW (0.0 to 300.0 kW)
    rExhaustBackPressure_bar : REAL; // External sea pressure for exhaust
    
    // Sensor Inputs
    rCombustionChamberTemp_C : REAL; // Measured temperature of the combustion chamber
    rCombustionChamberPres_bar: REAL; // Measured pressure of combustion chamber
    rHeliumWorkingTemp_C     : REAL; // Helium hot-side temperature
    rHeliumWorkingPres_bar   : REAL; // Helium mean pressure
    rEngineRPM               : REAL; // Measured RPM of Stirling engine
    rAcousticSensorArray_dB  : ARRAY[1..8] OF REAL; // Acoustic signature feedback from hull mounts
END_VAR

VAR_OUTPUT
    bSystemReady             : BOOL; // System is operational and generating power
    rActualPowerOutput_kW    : REAL; // Estimated current power output
    
    // Actuators
    rLOXValvePosition_Pct    : REAL; // Liquid Oxygen injection valve position (0-100%)
    rDieselValvePosition_Pct : REAL; // Diesel fuel injection valve position (0-100%)
    rHeaterControl_Pct       : REAL; // Pre-heater/Heater control for starting
    
    // Auxiliary Systems
    rActiveDampeningDrive_Pct: ARRAY[1..4] OF REAL; // Active acoustic dampening counter-vibration drives
    bExhaustCompressorRun    : BOOL; // Overboard exhaust compressor enable
    
    // Status/Alarms
    wEngineState             : WORD; // 0=Off, 1=Startup, 2=Running, 3=Shutdown, 4=Fault
    wAlarmWord               : DWORD;
END_VAR

VAR
    // PID Controllers for Combustion
    fbCombustionPresPID : PID_Compact;
    fbCombustionTempPID : PID_Compact;
    
    // Cycle tracking
    rHeThermodynamicEfficiency : REAL;
    
    // Internal States
    eState : INT; // 0=OFF, 1=PURGE, 2=IGNITION, 3=WARMUP, 4=RUN, 5=SHUTDOWN, 6=FAULT
    tStateTimer : TON;
    rTargetPressure : REAL := 30.0; // 30 bar requirement to overcome back-pressure
    
    // Acoustic Filtering
    rAvgAcousticNoise : REAL;
    i : INT;
    rMaxNoiseThreshold : REAL := 65.0; // dB max signature allowed
END_VAR

BEGIN
    // ==============================================================================
    // 1. STATE MACHINE & ENGINE SEQUENCING
    // ==============================================================================
    tStateTimer(IN := (eState = 1) OR (eState = 2) OR (eState = 3), PT := T#10S);
    
    CASE eState OF
        0: // STATE_OFF
            wEngineState := 0;
            bSystemReady := FALSE;
            rLOXValvePosition_Pct := 0.0;
            rDieselValvePosition_Pct := 0.0;
            IF bEnable THEN
                eState := 1;
                tStateTimer(IN := FALSE);
            END_IF;
            
        1: // STATE_PURGE
            wEngineState := 1;
            // Purge combustion chamber
            IF tStateTimer.Q THEN
                eState := 2;
                tStateTimer(IN := FALSE);
            END_IF;
            
        2: // STATE_IGNITION
            wEngineState := 1;
            // Initial fuel and LOX flow
            rLOXValvePosition_Pct := 5.0;
            rDieselValvePosition_Pct := 2.5;
            rHeaterControl_Pct := 100.0;
            IF rCombustionChamberTemp_C > 400.0 THEN
                eState := 3;
                tStateTimer(IN := FALSE);
            END_IF;
            IF tStateTimer.Q THEN // Failed to ignite
                eState := 6;
                wAlarmWord := wAlarmWord OR 16#0001; 
            END_IF;
            
        3: // STATE_WARMUP
            wEngineState := 1;
            rHeaterControl_Pct := 0.0;
            // Ramp up temperature
            IF rHeliumWorkingTemp_C > 650.0 THEN // He hot-side nominal
                eState := 4;
            END_IF;
            
        4: // STATE_RUN
            wEngineState := 2;
            bSystemReady := TRUE;
            
            // Fault condition transitions
            IF NOT bEnable THEN
                eState := 5;
            END_IF;
            IF rCombustionChamberPres_bar > 45.0 THEN // Overpressure
                eState := 6;
                wAlarmWord := wAlarmWord OR 16#0002;
            END_IF;
            
        5: // STATE_SHUTDOWN
            wEngineState := 3;
            bSystemReady := FALSE;
            rLOXValvePosition_Pct := 0.0;
            rDieselValvePosition_Pct := 0.0;
            IF rCombustionChamberTemp_C < 100.0 THEN
                eState := 0;
            END_IF;
            
        6: // STATE_FAULT
            wEngineState := 4;
            bSystemReady := FALSE;
            rLOXValvePosition_Pct := 0.0;
            rDieselValvePosition_Pct := 0.0;
            // Wait for reset (bEnable toggled)
            IF NOT bEnable THEN
                eState := 0;
                wAlarmWord := 0;
            END_IF;
    END_CASE;

    // ==============================================================================
    // 2. COMBUSTION AND PRESSURE CONTROL (30 BAR LOX/DIESEL)
    // ==============================================================================
    // The combustion chamber must maintain 30 bar to naturally exhaust against deep sea pressure
    // The Diesel-to-LOX ratio is maintained stoichiometrically (approx 1:3.5 by mass depending on exact density)
    
    IF eState = 4 THEN
        // Pressure Control to overcome exhaust back-pressure
        rTargetPressure := MAX(IN1:=30.0, IN2:=rExhaustBackPressure_bar + 5.0);
        
        fbCombustionPresPID(
            Setpoint := rTargetPressure,
            Input := rCombustionChamberPres_bar,
            Kp := 2.5,
            Ti := T#2S,
            Td := T#500MS
        );
        
        fbCombustionTempPID(
            Setpoint := 850.0 + (rPowerDemand_kW * 0.5), // Scale temp with power demand
            Input := rCombustionChamberTemp_C,
            Kp := 1.2,
            Ti := T#5S
        );
        
        // Output from PIDs governs total mass flow. We split it for stoichiometric combustion.
        // Assuming Output range is 0.0 to 100.0%
        rLOXValvePosition_Pct := LIMIT(MN:=0.0, IN:=(fbCombustionPresPID.Output + fbCombustionTempPID.Output) * 0.78, MX:=100.0);
        rDieselValvePosition_Pct := LIMIT(MN:=0.0, IN:=(fbCombustionPresPID.Output + fbCombustionTempPID.Output) * 0.22, MX:=100.0);
        
        // Exhaust compressor logic - turn on if back-pressure is higher than combustion pressure
        IF rExhaustBackPressure_bar > rCombustionChamberPres_bar THEN
            bExhaustCompressorRun := TRUE;
        ELSE
            bExhaustCompressorRun := FALSE;
        END_IF;
    ELSE
        bExhaustCompressorRun := FALSE;
    END_IF;

    // ==============================================================================
    // 3. HELIUM THERMODYNAMIC CYCLE TRACKING
    // ==============================================================================
    // Ideal Stirling Cycle Efficiency = 1 - (Tc/Th)
    // We approximate Tc to ambient seawater temp (~10C) = 283K. Th is He hot-side temp in Kelvin.
    rHeThermodynamicEfficiency := 1.0 - (283.15 / (rHeliumWorkingTemp_C + 273.15));
    
    // Actual power estimation based on RPM, mean He pressure, and engine displacement constants (C_engine=0.045)
    rActualPowerOutput_kW := (rEngineRPM / 60.0) * rHeliumWorkingPres_bar * 0.045 * rHeThermodynamicEfficiency * 100.0;
    
    // ==============================================================================
    // 4. ACOUSTIC SIGNATURE DAMPENING ARRAYS
    // ==============================================================================
    // Read acoustic sensor array and apply active noise cancellation (ANC) to vibration mounts
    rAvgAcousticNoise := 0.0;
    FOR i := 1 TO 8 DO
        rAvgAcousticNoise := rAvgAcousticNoise + rAcousticSensorArray_dB[i];
    END_FOR;
    rAvgAcousticNoise := rAvgAcousticNoise / 8.0;
    
    IF rAvgAcousticNoise > rMaxNoiseThreshold THEN
        wAlarmWord := wAlarmWord OR 16#0004; // High signature alarm
    ELSE
        wAlarmWord := wAlarmWord AND 16#FFFB; // Clear alarm
    END_IF;

    // Simple phase-shifted active dampening control based on engine RPM (fundamental frequency)
    // In a real system, this involves complex DSP algorithms. We simulate the drive outputs.
    // 1 Hz = 60 RPM. 
    FOR i := 1 TO 4 DO
        IF eState = 4 THEN
            // Modulate dampening drive based on RPM harmonic and overall noise level
            rActiveDampeningDrive_Pct[i] := LIMIT(MN:=0.0, IN:=(rAvgAcousticNoise / rMaxNoiseThreshold) * 50.0 + (INT_TO_REAL(i) * 5.0), MX:=100.0);
        ELSE
            rActiveDampeningDrive_Pct[i] := 0.0;
        END_IF;
    END_FOR;

END_FUNCTION_BLOCK
"""

json_obj = {
    "messages": [
        {
            "role": "user",
            "content": "You are acting as a Lead Marine Engineer. Evolve a basic power block into a Submarine AIP (Air-Independent Propulsion) Stirling Engine Controller. Technical Specs: 1. Liquid Oxygen (LOX) and Diesel combustion at 30 bar pressure to overcome exhaust back-pressure. 2. Helium working fluid thermodynamic cycle tracking. 3. Acoustic signature dampening arrays."
        },
        {
            "role": "assistant",
            "content": content
        }
    ]
}

with open("c:/Users/majip/Downloads/LLM REASEARCH/Local_Ollama_Evol_Pipeline/seeds/tier1_enterprise_grade/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(json_obj) + "\n")

print("Appended successfully.")
