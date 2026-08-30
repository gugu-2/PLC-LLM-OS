import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Geothermal Flash Steam Power Plant.
Task: Invent a highly complex control scenario for this domain (e.g., brine reinjection well pressure mapping, Non-Condensable Gas (NCG) extraction loops, and steam turbine bypass control).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.
"""

st_code = """```iec-st
FUNCTION_BLOCK FB_Geothermal_Flash_Steam_Control
TITLE = 'Geothermal Flash Steam Power Plant Advanced Control System'
VERSION : '1.0'
AUTHOR : 'Lumina Elite Synthetic Data Architect'

VAR_INPUT
    // Steam Turbine & Bypass
    rTurbineInletPress_bar    : REAL; // Pressure at turbine inlet
    rTurbineSpeed_rpm         : REAL; // Turbine shaft speed
    rGridDemand_MW            : REAL; // Grid power demand
    bTurbineTrip              : BOOL; // Emergency trip signal
    
    // NCG Extraction Loop
    rCondenserPress_mbar      : REAL; // Condenser vacuum pressure
    rNCGTemperature_C         : REAL; // Temperature of NCG mixture
    rCoolingWaterFlow_kgps    : REAL; // Cooling water flow rate
    
    // Brine Reinjection
    rFlashSeparatorLevel_m    : REAL; // Brine level in flash separator
    rReinjectionWellPress_bar : REAL; // Downhole pressure of reinjection well
    rBrineFlowRate_tph        : REAL; // Brine mass flow to reinjection
    bSeismicActivityDetected  : BOOL; // Interlock for induced seismicity
END_VAR

VAR_OUTPUT
    // Turbine Bypass Control
    rTurbineBypassValve_pct   : REAL; // Opening of turbine bypass to condenser
    rTurbineThrottleValve_pct : REAL; // Main throttle valve position
    
    // NCG System
    rEjectorSteamValve_pct    : REAL; // Motive steam valve to NCG ejectors
    bVacuumPumpStart          : BOOL; // Liquid ring vacuum pump start command
    
    // Brine Reinjection Control
    rBrineReinjectionValve_pct: REAL; // Control valve for brine injection
    bReinjectionPumpStart     : BOOL; // Reinjection booster pump
    bEmergencyDumpValve       : BOOL; // Dump to silencer/pond
    
    // System Status
    bSystemAlarm              : BOOL;
    wAlarmCode                : WORD;
END_VAR

VAR
    // PID Controllers (Internal representations)
    fbTurbineSpeedPID         : FB_PID;
    fbBypassPressPID          : FB_PID;
    fbCondenserVacPID         : FB_PID;
    fbBrineLevelPID           : FB_PID;
    
    // Internal state variables
    rSetpointSpeed_rpm        : REAL := 3000.0;
    rSetpointVacuum_mbar      : REAL := 80.0;
    rSetpointBrineLevel_m     : REAL := 2.5;
    rMaxReinjectionPress      : REAL := 45.0; // bar
    
    // Timers
    tonPumpDelay              : TON;
    tonTripDelay              : TON;
    
    // Constants
    c_rNominalInletPress      : REAL := 10.5; // bar
END_VAR

(* 
   ========================================================================
   1. Turbine Speed and Bypass Control (Steam Management)
   ========================================================================
*)
IF bTurbineTrip THEN
    rTurbineThrottleValve_pct := 0.0;
    // Fast-acting bypass to protect upstream piping and prevent safety valve lift
    fbBypassPressPID.rSetPoint := c_rNominalInletPress;
    fbBypassPressPID.rProcessValue := rTurbineInletPress_bar;
    fbBypassPressPID(bEnable := TRUE);
    rTurbineBypassValve_pct := fbBypassPressPID.rOutput;
    
    wAlarmCode := 16#A001; // Turbine Trip
    bSystemAlarm := TRUE;
ELSE
    // Normal operation: control turbine speed/load
    fbTurbineSpeedPID.rSetPoint := rSetpointSpeed_rpm;
    fbTurbineSpeedPID.rProcessValue := rTurbineSpeed_rpm;
    fbTurbineSpeedPID(bEnable := TRUE);
    rTurbineThrottleValve_pct := fbTurbineSpeedPID.rOutput;
    
    // Bypass is closed during normal operation unless overpressure occurs
    IF rTurbineInletPress_bar > (c_rNominalInletPress * 1.05) THEN
        rTurbineBypassValve_pct := (rTurbineInletPress_bar - (c_rNominalInletPress * 1.05)) * 10.0;
        IF rTurbineBypassValve_pct > 100.0 THEN rTurbineBypassValve_pct := 100.0; END_IF;
    ELSE
        rTurbineBypassValve_pct := 0.0;
    END_IF;
END_IF;

(* 
   ========================================================================
   2. Non-Condensable Gas (NCG) Extraction Control
   ========================================================================
   NCGs severely degrade condenser vacuum. Dual system: Steam ejectors + LRVP.
*)
fbCondenserVacPID.rSetPoint := rSetpointVacuum_mbar;
fbCondenserVacPID.rProcessValue := rCondenserPress_mbar;
fbCondenserVacPID(bEnable := TRUE);

// Stage 1: Steam ejectors handle baseline NCG load
rEjectorSteamValve_pct := fbCondenserVacPID.rOutput * 0.8;

// Stage 2: Liquid Ring Vacuum Pump (LRVP) starts if pressure > 100 mbar 
// or high cooling water temp reduces condensation efficiency
IF rCondenserPress_mbar > 100.0 OR rNCGTemperature_C > 40.0 THEN
    bVacuumPumpStart := TRUE;
    wAlarmCode := 16#B002; // High Condenser Pressure
ELSE
    bVacuumPumpStart := FALSE;
END_IF;

(* 
   ========================================================================
   3. Brine Reinjection Control (Silica Scaling & Pressure Limits)
   ========================================================================
   Flash separator level must be maintained. Brine must be reinjected at 
   high pressure, but limited by seismic triggers.
*)

fbBrineLevelPID.rSetPoint := rSetpointBrineLevel_m;
fbBrineLevelPID.rProcessValue := rFlashSeparatorLevel_m;
fbBrineLevelPID(bEnable := TRUE);

tonPumpDelay(IN := (fbBrineLevelPID.rOutput > 10.0), PT := T#5S);

IF tonPumpDelay.Q THEN
    bReinjectionPumpStart := TRUE;
ELSE
    bReinjectionPumpStart := FALSE;
END_IF;

// Seismic Interlock Override
IF bSeismicActivityDetected OR (rReinjectionWellPress_bar > rMaxReinjectionPress) THEN
    // Close injection valve to prevent induced seismicity or over-pressurization
    rBrineReinjectionValve_pct := 0.0;
    bReinjectionPumpStart := FALSE;
    bEmergencyDumpValve := TRUE; // Dump brine to thermal pond
    
    bSystemAlarm := TRUE;
    wAlarmCode := 16#C003; // Seismic / High Reinjection Pressure Trip
ELSE
    bEmergencyDumpValve := FALSE;
    rBrineReinjectionValve_pct := fbBrineLevelPID.rOutput;
END_IF;

END_FUNCTION_BLOCK
```"""

# The instructions in the prompt specify appending to data/synthetic_generation_v3_enterprise.jsonl but the user payload requests data/swarm_raw/agent_{uuid}.json. I will do both.

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": st_code}]}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")
    
print(f"Created file: {filename} and appended to jsonl")
