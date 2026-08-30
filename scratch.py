import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Rotary Autoclave Sterilizer (Food/Pharma).
Task: Invent a highly complex control scenario for this domain (e.g., F0 lethality value calculation loops, steam-air mixture overpressure, and rotary basket agitation profiling).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

st_code = """```iec-st
FUNCTION_BLOCK FB_RotaryAutoclaveSterilizer
VAR_INPUT
    bStartCycle       : BOOL; (* Initiate sterilization cycle *)
    bStopCycle        : BOOL; (* Abort cycle *)
    bEmergencyStop    : BOOL; (* E-stop activated *)
    
    rChamberTemp      : REAL; (* Current chamber temperature [°C] *)
    rCoreTemp         : REAL; (* Product core temperature [°C] *)
    rChamberPressure  : REAL; (* Chamber pressure [bar] *)
    rBasketRpmFeed    : REAL; (* Basket rotation speed feedback [RPM] *)
    
    rTargetF0         : REAL := 15.0; (* Target F0 value [min] *)
    rSterilTemp       : REAL := 121.1; (* Target sterilization temp [°C] *)
    rCoolingTemp      : REAL := 40.0; (* Target cooling temp [°C] *)
    rTargetOverpressure : REAL := 2.5; (* Target overpressure during holding [bar] *)
    rMaxBasketRpm     : REAL := 10.0; (* Max agitation speed [RPM] *)
END_VAR

VAR_OUTPUT
    eState            : DINT; (* Current cycle phase *)
    bSteamValve       : BOOL; (* Steam inlet valve *)
    bWaterValve       : BOOL; (* Cooling water inlet valve *)
    bVentValve        : BOOL; (* Exhaust/vent valve *)
    bAirValve         : BOOL; (* Compressed air inlet valve for overpressure *)
    rBasketRpmCmd     : REAL; (* Basket rotation command [RPM] *)
    rAccumulatedF0    : REAL; (* Calculated F0 lethality [min] *)
    bCycleComplete    : BOOL; (* Cycle finished successfully *)
    bAlarm            : BOOL; (* Active alarm *)
    iAlarmCode        : INT;  (* Specific alarm code *)
END_VAR

VAR
    rtStart           : R_TRIG;
    ftTempHold        : F_TRIG;
    rZValue           : REAL := 10.0; (* Z-value for F0 calc [°C] *)
    rRefTemp          : REAL := 121.1; (* Reference temp for F0 calc [°C] *)
    tScanTime         : REAL := 0.1; (* Block execution scan time [s] *)
    rDeltaF0          : REAL;
    
    tHoldTimer        : TON;
    tCoolTimer        : TON;
    
    rPID_TempError    : REAL;
    rPID_TempIntegral : REAL;
    rPID_TempOutput   : REAL;
    
    rPID_PressError   : REAL;
    rPID_PressIntegral: REAL;
    rPID_PressOutput  : REAL;
END_VAR

(* Implementation *)
rtStart(CLK := bStartCycle);

IF bEmergencyStop THEN
    eState := 99; (* ABORTED *)
    bAlarm := TRUE;
    iAlarmCode := 999;
END_IF;

IF bStopCycle THEN
    eState := 99; (* ABORTED *)
END_IF;

CASE eState OF
    0: (* IDLE *)
        bSteamValve := FALSE;
        bWaterValve := FALSE;
        bVentValve := TRUE;
        bAirValve := FALSE;
        rBasketRpmCmd := 0.0;
        bCycleComplete := FALSE;
        rAccumulatedF0 := 0.0;
        
        IF rtStart.Q AND NOT bEmergencyStop THEN
            eState := 10; (* HEATING *)
            bVentValve := FALSE;
        END_IF;
        
    10: (* HEATING *)
        (* Agitation *)
        rBasketRpmCmd := rMaxBasketRpm * 0.5;
        
        (* Heat up *)
        bSteamValve := TRUE;
        bVentValve := (rChamberPressure > 1.2); (* Basic air purging *)
        
        IF rChamberTemp >= rSterilTemp AND rCoreTemp >= (rSterilTemp - 0.5) THEN
            eState := 20; (* HOLDING *)
            rPID_TempIntegral := 0.0;
            rPID_PressIntegral := 0.0;
        END_IF;
        
    20: (* HOLDING *)
        (* F0 Calculation (Trapezoidal integration over scan time) *)
        rDeltaF0 := (10.0 ** ((rCoreTemp - rRefTemp) / rZValue)) * (tScanTime / 60.0);
        rAccumulatedF0 := rAccumulatedF0 + rDeltaF0;
        
        (* Temp PID simplified control *)
        rPID_TempError := rSterilTemp - rChamberTemp;
        bSteamValve := rPID_TempError > 0.0;
        
        (* Overpressure PID simplified control *)
        rPID_PressError := rTargetOverpressure - rChamberPressure;
        bAirValve := rPID_PressError > 0.0;
        bVentValve := rPID_PressError < -0.1;
        
        (* Agitation profile *)
        rBasketRpmCmd := rMaxBasketRpm;
        
        IF rAccumulatedF0 >= rTargetF0 THEN
            eState := 30; (* COOLING *)
            bSteamValve := FALSE;
        END_IF;
        
    30: (* COOLING *)
        bWaterValve := TRUE;
        (* Maintain overpressure during initial cooling to prevent packaging rupture *)
        rPID_PressError := (rTargetOverpressure - 0.5) - rChamberPressure;
        bAirValve := rPID_PressError > 0.0;
        
        rBasketRpmCmd := rMaxBasketRpm * 0.2;
        
        IF rCoreTemp <= rCoolingTemp THEN
            bWaterValve := FALSE;
            bAirValve := FALSE;
            eState := 40; (* DEPRESSURIZING *)
        END_IF;
        
    40: (* DEPRESSURIZING *)
        bVentValve := TRUE;
        rBasketRpmCmd := 0.0;
        
        IF rChamberPressure <= 1.05 THEN
            eState := 50; (* COMPLETE *)
        END_IF;
        
    50: (* COMPLETE *)
        bCycleComplete := TRUE;
        bVentValve := TRUE;
        IF NOT bStartCycle THEN
            eState := 0; (* IDLE *)
        END_IF;
        
    99: (* ABORTED *)
        bSteamValve := FALSE;
        bWaterValve := TRUE; (* Cooling down safely *)
        bAirValve := FALSE;
        bVentValve := TRUE;
        rBasketRpmCmd := 0.0;
        
        IF rChamberPressure <= 1.05 AND rChamberTemp <= 60.0 THEN
            bWaterValve := FALSE;
            IF NOT bEmergencyStop AND NOT bStopCycle THEN
                eState := 0;
            END_IF;
        END_IF;
END_CASE;
END_FUNCTION_BLOCK
```"""

record = {'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': st_code}]}
os.makedirs('data/swarm_raw', exist_ok=True)
with open(f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json', 'w', encoding='utf-8') as f:
    json.dump(record, f)
