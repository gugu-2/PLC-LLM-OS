import json, uuid, os
os.makedirs('data/swarm_raw', exist_ok=True)
record = {'messages': [{'role': 'user', 'content': 'Design a complex control scenario for a Utility-Scale Biogas Upgrading Plant (membrane separation CO2 stripping, amine scrubbing solvent regeneration, and biomethane grid injection pressure) in Structured Text.'}, {'role': 'assistant', 'content': '''```iec-st
FUNCTION_BLOCK FB_BiogasUpgradingPlantControl
VAR_INPUT
    bEnable                 : BOOL;   (* Enable overall plant control *)
    bEmergencyStop          : BOOL;   (* Plant emergency stop *)
    rRawGasFlowRate         : REAL;   (* Raw biogas inlet flow rate [Nm3/h] *)
    rRawGasCH4              : REAL;   (* Raw biogas CH4 concentration [%] *)
    rRawGasCO2              : REAL;   (* Raw biogas CO2 concentration [%] *)
    rAmineSolventLevel      : REAL;   (* Level of amine solvent in regenerator [%] *)
    rAmineTemperature       : REAL;   (* Temperature of amine solvent [degC] *)
    rMembranePressure       : REAL;   (* Feed pressure to membrane separation [bar] *)
    rGridPressure           : REAL;   (* Biomethane grid injection pressure [bar] *)
    rTargetGridPressure     : REAL;   (* Target grid injection pressure [bar] *)
    rBiomethaneQualityCH4   : REAL;   (* Output biomethane CH4 concentration [%] *)
END_VAR

VAR_OUTPUT
    bInletCompressorCmd     : BOOL;   (* Command to start inlet compressor *)
    rInletCompressorSpeed   : REAL;   (* Speed setpoint for inlet compressor [%] *)
    bAminePumpCmd           : BOOL;   (* Command to start amine circulation pump *)
    rAminePumpSpeed         : REAL;   (* Speed setpoint for amine circulation pump [%] *)
    bAmineHeaterCmd         : BOOL;   (* Command to activate amine regeneration heater *)
    rAmineHeaterPower       : REAL;   (* Power setpoint for amine regeneration heater [%] *)
    bMembraneValveCmd       : BOOL;   (* Command to open membrane feed valve *)
    rGridInjectionValvePos  : REAL;   (* Position setpoint for grid injection control valve [%] *)
    bFlareValveCmd          : BOOL;   (* Command to send off-spec gas to flare *)
    bSystemReady            : BOOL;   (* Plant is ready and operating normally *)
    bAlarmActive            : BOOL;   (* General alarm active *)
    iAlarmCode              : INT;    (* Active alarm code *)
END_VAR

VAR
    (* Internal state variables *)
    nState                  : INT := 0; (* State machine step: 0=Init, 1=Startup, 2=Running, 3=Shutdown, 4=Fault *)
    tStartupTimer           : TON;
    tPurgeTimer             : TON;
    tStabilizationTimer     : TON;
    
    (* PI Controllers *)
    rKpCompressor           : REAL := 2.5;
    rKiCompressor           : REAL := 0.5;
    rCompressorError        : REAL;
    rCompressorIntegral     : REAL;
    
    rKpAmineHeater          : REAL := 5.0;
    rKiAmineHeater          : REAL := 1.2;
    rAmineHeaterError       : REAL;
    rAmineHeaterIntegral    : REAL;
    
    rKpGridValve            : REAL := 1.5;
    rKiGridValve            : REAL := 0.3;
    rGridValveError         : REAL;
    rGridValveIntegral      : REAL;
    
    (* Constants *)
    rMinAmineTemp           : REAL := 105.0; (* Minimum temp for amine regeneration [degC] *)
    rMaxAmineTemp           : REAL := 125.0; (* Maximum temp for amine regeneration [degC] *)
    rMinGridQualityCH4      : REAL := 97.0;  (* Minimum required CH4 quality for grid [%] *)
    rMaxMembranePress       : REAL := 16.0;  (* Maximum safe membrane pressure [bar] *)
    
    tCycleTime              : REAL := 0.1; (* Control loop cycle time [s] *)
END_VAR

(* EMERGENCY STOP HANDLING *)
IF bEmergencyStop THEN
    nState := 4;
    iAlarmCode := 99;
END_IF;

(* STATE MACHINE *)
CASE nState OF
    0: (* INIT *)
        bInletCompressorCmd := FALSE;
        rInletCompressorSpeed := 0.0;
        bAminePumpCmd := FALSE;
        rAminePumpSpeed := 0.0;
        bAmineHeaterCmd := FALSE;
        rAmineHeaterPower := 0.0;
        bMembraneValveCmd := FALSE;
        rGridInjectionValvePos := 0.0;
        bFlareValveCmd := FALSE;
        bSystemReady := FALSE;
        bAlarmActive := FALSE;
        iAlarmCode := 0;
        
        IF bEnable AND NOT bEmergencyStop THEN
            nState := 1;
            tStartupTimer(IN := FALSE);
        END_IF;
        
    1: (* STARTUP *)
        bSystemReady := FALSE;
        bAminePumpCmd := TRUE;
        rAminePumpSpeed := 50.0;
        
        IF rAmineTemperature < rMinAmineTemp THEN
            bAmineHeaterCmd := TRUE;
            rAmineHeaterPower := 100.0;
        ELSE
            bInletCompressorCmd := TRUE;
            rInletCompressorSpeed := 20.0;
            tStartupTimer(IN := TRUE, PT := T#30s);
            
            IF tStartupTimer.Q THEN
                bMembraneValveCmd := TRUE;
                nState := 2;
                tStabilizationTimer(IN := FALSE);
            END_IF;
        END_IF;
        
    2: (* RUNNING *)
        bSystemReady := TRUE;
        
        rCompressorError := rRawGasFlowRate - 500.0;
        IF rMembranePressure > rMaxMembranePress THEN
            rCompressorError := -50.0;
        END_IF;
        rCompressorIntegral := rCompressorIntegral + (rCompressorError * tCycleTime);
        IF rCompressorIntegral > 100.0 THEN rCompressorIntegral := 100.0; END_IF;
        IF rCompressorIntegral < 0.0 THEN rCompressorIntegral := 0.0; END_IF;
        rInletCompressorSpeed := (rKpCompressor * rCompressorError) + (rKiCompressor * rCompressorIntegral);
        IF rInletCompressorSpeed > 100.0 THEN rInletCompressorSpeed := 100.0; END_IF;
        IF rInletCompressorSpeed < 20.0 THEN rInletCompressorSpeed := 20.0; END_IF;
        
        rAmineHeaterError := ((rMinAmineTemp + rMaxAmineTemp) / 2.0) - rAmineTemperature;
        rAmineHeaterIntegral := rAmineHeaterIntegral + (rAmineHeaterError * tCycleTime);
        IF rAmineHeaterIntegral > 100.0 THEN rAmineHeaterIntegral := 100.0; END_IF;
        IF rAmineHeaterIntegral < 0.0 THEN rAmineHeaterIntegral := 0.0; END_IF;
        rAmineHeaterPower := (rKpAmineHeater * rAmineHeaterError) + (rKiAmineHeater * rAmineHeaterIntegral);
        IF rAmineHeaterPower > 100.0 THEN rAmineHeaterPower := 100.0; END_IF;
        IF rAmineHeaterPower < 0.0 THEN rAmineHeaterPower := 0.0; END_IF;
        
        tStabilizationTimer(IN := TRUE, PT := T#60s);
        IF tStabilizationTimer.Q THEN
            IF rBiomethaneQualityCH4 >= rMinGridQualityCH4 THEN
                bFlareValveCmd := FALSE;
                rGridValveError := rTargetGridPressure - rGridPressure;
                rGridValveIntegral := rGridValveIntegral + (rGridValveError * tCycleTime);
                IF rGridValveIntegral > 100.0 THEN rGridValveIntegral := 100.0; END_IF;
                IF rGridValveIntegral < 0.0 THEN rGridValveIntegral := 0.0; END_IF;
                rGridInjectionValvePos := (rKpGridValve * rGridValveError) + (rKiGridValve * rGridValveIntegral);
                IF rGridInjectionValvePos > 100.0 THEN rGridInjectionValvePos := 100.0; END_IF;
                IF rGridInjectionValvePos < 0.0 THEN rGridInjectionValvePos := 0.0; END_IF;
            ELSE
                bFlareValveCmd := TRUE;
                rGridInjectionValvePos := 0.0;
            END_IF;
        END_IF;
        
        IF NOT bEnable THEN
            nState := 3;
            tPurgeTimer(IN := FALSE);
        END_IF;
        
    3: (* SHUTDOWN *)
        bSystemReady := FALSE;
        bInletCompressorCmd := FALSE;
        rInletCompressorSpeed := 0.0;
        rGridInjectionValvePos := 0.0;
        bFlareValveCmd := TRUE;
        bAmineHeaterCmd := FALSE;
        rAmineHeaterPower := 0.0;
        
        tPurgeTimer(IN := TRUE, PT := T#120s);
        IF tPurgeTimer.Q THEN
            bAminePumpCmd := FALSE;
            rAminePumpSpeed := 0.0;
            bMembraneValveCmd := FALSE;
            bFlareValveCmd := FALSE;
            nState := 0;
        END_IF;
        
    4: (* FAULT *)
        bSystemReady := FALSE;
        bAlarmActive := TRUE;
        bInletCompressorCmd := FALSE;
        rInletCompressorSpeed := 0.0;
        bAminePumpCmd := FALSE;
        rAminePumpSpeed := 0.0;
        bAmineHeaterCmd := FALSE;
        rAmineHeaterPower := 0.0;
        bMembraneValveCmd := FALSE;
        rGridInjectionValvePos := 0.0;
        bFlareValveCmd := TRUE;
        
        IF NOT bEmergencyStop AND bEnable = FALSE THEN
            nState := 0;
        END_IF;
        
END_CASE;
END_FUNCTION_BLOCK
```'''}]}
with open(f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json', 'w', encoding='utf-8') as f:
    json.dump(record, f)
