import json
import uuid
import os

code_st = \"\"\"FUNCTION_BLOCK FB_FrancisTurbineAdvancedControl
TITLE = 'Hydroelectric Dam Francis Turbine Control - Wicket Gate, Cavitation & Sync'
VERSION : '2.0'
AUTHOR : 'Lumina AI Cloud Swarm'

VAR_INPUT
    rPenstockPressure       : REAL; (* Penstock water pressure in kPa *)
    rTailwaterElevation     : REAL; (* Tailwater elevation in meters *)
    rTurbineSpeed           : REAL; (* Current turbine rotational speed in RPM *)
    rActivePower            : REAL; (* Output active power in MW *)
    rReactivePower          : REAL; (* Output reactive power in MVAR *)
    rGridVoltage            : REAL; (* Grid network voltage in kV *)
    rGridFrequency          : REAL; (* Grid network frequency in Hz *)
    rGeneratorVoltage       : REAL; (* Generator terminal voltage in kV *)
    rGeneratorFrequency     : REAL; (* Generator electrical frequency in Hz *)
    rPhaseAngleDiff         : REAL; (* Phase angle difference between grid and gen in degrees *)
    rAcousticSensor1        : REAL; (* Acoustic emission sensor 1 in dB - Draft tube *)
    rAcousticSensor2        : REAL; (* Acoustic emission sensor 2 in dB - Spiral case *)
    rAcousticSensor3        : REAL; (* Acoustic emission sensor 3 in dB - Runner *)
    bGridSyncEnable         : BOOL; (* Command to initiate grid synchronization *)
    bLoadRejectionCmd       : BOOL; (* Command indicating sudden load rejection *)
    bEmergencyStop          : BOOL; (* Emergency shutdown command *)
    bAcknowledgeAlarms      : BOOL; (* Operator alarm acknowledgment *)
END_VAR

VAR_OUTPUT
    rWicketGatePositionSet  : REAL; (* Commanded wicket gate guide vane position 0-100% *)
    rExcitationVoltageSet   : REAL; (* Commanded AVR excitation voltage setpoint in V *)
    bGeneratorBreakerClose  : BOOL; (* Command to close the main generator circuit breaker *)
    bAlarmCavitation        : BOOL; (* High acoustic noise / cavitation detected alarm *)
    bAlarmOverspeed         : BOOL; (* Turbine overspeed critical alarm *)
    bAlarmSyncFailed        : BOOL; (* Synchronization sequence timeout/failure alarm *)
    iStateSync              : INT;  (* Current step in synchronization state machine *)
END_VAR

VAR
    rSpeedSetpoint          : REAL := 150.0; (* Nominal turbine speed in RPM *)
    rWicketGateMax          : REAL := 100.0; (* Maximum gate opening % *)
    rWicketGateMin          : REAL := 0.0;   (* Minimum gate opening % *)
    rCavitationThreshold    : REAL := 85.0;  (* Acoustic emission threshold for cavitation dB *)
    
    tCavitationTimer        : TON;
    tSyncTimeoutTimer       : TON;
    tBreakerCloseTimer      : TON;
    
    rVoltageTolerance       : REAL := 0.5;   (* kV tolerance for sync *)
    rFreqTolerance          : REAL := 0.05;  (* Hz tolerance for sync *)
    rPhaseTolerance         : REAL := 3.0;   (* Degrees tolerance for sync *)
    
    rKp_Speed               : REAL := 3.2;   (* Proportional gain for speed governor *)
    rKi_Speed               : REAL := 0.8;   (* Integral gain for speed governor *)
    rKd_Speed               : REAL := 0.1;   (* Derivative gain for speed governor *)
    rSpeedError             : REAL;
    rSpeedErrorPrev         : REAL;
    rSpeedIntegral          : REAL;
    rSpeedDerivative        : REAL;
    
    bSyncReady              : BOOL;
    rNetHead                : REAL;
END_VAR

(*========================================================================
   1. EMERGENCY AND CRITICAL PROTECTIONS
========================================================================*)
IF bEmergencyStop THEN
    rWicketGatePositionSet := 0.0; (* Slam gates closed *)
    bGeneratorBreakerClose := FALSE;
    rExcitationVoltageSet  := 0.0;
    iStateSync := 0;
    rSpeedIntegral := 0.0;
    bAlarmOverspeed := FALSE;
    bAlarmCavitation := FALSE;
    bAlarmSyncFailed := FALSE;
    RETURN; (* Halt further processing *)
END_IF;

IF bAcknowledgeAlarms THEN
    bAlarmCavitation := FALSE;
    bAlarmOverspeed := FALSE;
    bAlarmSyncFailed := FALSE;
END_IF;

(* Overspeed Protection *)
IF rTurbineSpeed > (rSpeedSetpoint * 1.15) THEN
    bAlarmOverspeed := TRUE;
    rWicketGatePositionSet := 0.0; (* Fast closure to prevent runaway *)
    bGeneratorBreakerClose := FALSE;
    RETURN;
END_IF;

(* Load Rejection Handling *)
IF bLoadRejectionCmd THEN
    bGeneratorBreakerClose := FALSE;
    rWicketGatePositionSet := 5.0; (* Speed-no-load position roughly *)
    iStateSync := 0;
END_IF;

(*========================================================================
   2. RUNNER CAVITATION ACOUSTIC MONITORING
========================================================================*)
(* Calculate net head roughly based on pressure and tailwater *)
rNetHead := (rPenstockPressure * 0.10197) - rTailwaterElevation; 

IF (rAcousticSensor1 > rCavitationThreshold) OR 
   (rAcousticSensor2 > rCavitationThreshold) OR 
   (rAcousticSensor3 > rCavitationThreshold) THEN
    tCavitationTimer(IN := TRUE, PT := T#5S);
ELSE
    tCavitationTimer(IN := FALSE, PT := T#5S);
END_IF;

IF tCavitationTimer.Q THEN
    bAlarmCavitation := TRUE;
    (* Automatic mitigation: Reduce gate opening slightly to exit cavitation zone *)
    rWicketGatePositionSet := LIMIT(rWicketGateMin, rWicketGatePositionSet - 2.5, rWicketGateMax);
END_IF;

(*========================================================================
   3. WICKET GATE GUIDE VANE POSITIONING (PID SPEED GOVERNOR)
========================================================================*)
rSpeedError := rSpeedSetpoint - rTurbineSpeed;

IF NOT bEmergencyStop AND NOT bAlarmCavitation AND NOT bLoadRejectionCmd THEN
    (* Integral term with anti-windup *)
    rSpeedIntegral := rSpeedIntegral + (rSpeedError * 0.1); (* Assumes 100ms task cycle *)
    rSpeedIntegral := LIMIT(-30.0, rSpeedIntegral, 30.0);
    
    (* Derivative term *)
    rSpeedDerivative := (rSpeedError - rSpeedErrorPrev) / 0.1;
    rSpeedErrorPrev := rSpeedError;
    
    (* PID Output *)
    rWicketGatePositionSet := (rKp_Speed * rSpeedError) + (rKi_Speed * rSpeedIntegral) + (rKd_Speed * rSpeedDerivative);
    
    (* Output limitation *)
    rWicketGatePositionSet := LIMIT(rWicketGateMin, rWicketGatePositionSet, rWicketGateMax);
END_IF;

(*========================================================================
   4. GENERATOR GRID SYNCHRONIZATION
========================================================================*)
tSyncTimeoutTimer(IN := (iStateSync > 0 AND iStateSync < 4), PT := T#120S);

IF tSyncTimeoutTimer.Q THEN
    bAlarmSyncFailed := TRUE;
    iStateSync := 0;
END_IF;

CASE iStateSync OF
    0: (* Standby / Unsynchronized *)
        bGeneratorBreakerClose := FALSE;
        IF bGridSyncEnable AND (rTurbineSpeed > (rSpeedSetpoint * 0.95)) AND NOT bAlarmSyncFailed THEN
            iStateSync := 1;
        END_IF;
        
    1: (* Voltage Matching Phase *)
        (* Adjust AVR excitation to match grid voltage *)
        IF rGeneratorVoltage < (rGridVoltage - rVoltageTolerance) THEN
            rExcitationVoltageSet := rExcitationVoltageSet + 1.0;
        ELSIF rGeneratorVoltage > (rGridVoltage + rVoltageTolerance) THEN
            rExcitationVoltageSet := rExcitationVoltageSet - 1.0;
        ELSE
            iStateSync := 2; (* Voltage matched *)
        END_IF;
        
    2: (* Frequency & Phase Angle Matching Phase *)
        (* Adjust speed setpoint slightly to match frequency and bring phase angle to zero *)
        IF rGeneratorFrequency < (rGridFrequency - rFreqTolerance) THEN
            rSpeedSetpoint := rSpeedSetpoint + 0.1;
        ELSIF rGeneratorFrequency > (rGridFrequency + rFreqTolerance) THEN
            rSpeedSetpoint := rSpeedSetpoint - 0.1;
        END_IF;
        
        IF (ABS(rGridFrequency - rGeneratorFrequency) <= rFreqTolerance) AND 
           (ABS(rPhaseAngleDiff) <= rPhaseTolerance) AND 
           (ABS(rGridVoltage - rGeneratorVoltage) <= rVoltageTolerance) THEN
            
            tBreakerCloseTimer(IN := TRUE, PT := T#1S);
            IF tBreakerCloseTimer.Q THEN
                iStateSync := 3;
                tBreakerCloseTimer(IN := FALSE);
            END_IF;
        ELSE
            tBreakerCloseTimer(IN := FALSE, PT := T#1S);
        END_IF;
        
    3: (* Issue Breaker Close Command *)
        bGeneratorBreakerClose := TRUE;
        iStateSync := 4;
        
    4: (* Synchronized and Online *)
        IF NOT bGridSyncEnable OR bLoadRejectionCmd THEN
            bGeneratorBreakerClose := FALSE;
            iStateSync := 0;
        END_IF;
END_CASE;
END_FUNCTION_BLOCK\"\"\"

prompt = \"You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data. Your specific domain is: Hydroelectric Dam Francis Turbine. Task: Invent a highly complex control scenario for this domain (e.g., wicket gate guide vane positioning, runner cavitation acoustic monitoring, and generator grid synchronization). Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.\"

record = {
    \"messages\": [
        {\"role\": \"user\", \"content\": prompt},
        {\"role\": \"assistant\", \"content\": f\"`iec-st\\n{code_st}\\n`\"}
    ]
}

os.makedirs(\"data/swarm_raw\", exist_ok=True)
filename = f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\"
with open(filename, \"w\", encoding=\"utf-8\") as f:
    json.dump(record, f, indent=2)

os.makedirs(\"data\", exist_ok=True)
with open(\"data/synthetic_generation_v3_enterprise.jsonl\", \"a\", encoding=\"utf-8\") as f:
    f.write(json.dumps(record) + \"\\n\")

print(filename)
