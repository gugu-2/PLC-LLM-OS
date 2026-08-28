import os
import json

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = "Invent a highly complex control scenario for High-Speed Rail CBTC Signaling domain (moving block train separation). Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

code = """```iec-st
FUNCTION_BLOCK FB_CBTC_MovingBlock_Controller
TITLE = 'High-Speed Rail Moving Block Separation Controller'
VERSION : '2.1'
AUTHOR : 'Lumina AI Swarm'

VAR_INPUT
    Enable : BOOL; // System enable
    TrainID : DINT; // Unique train identifier
    CurrentSpeed_Kmh : REAL; // Current train speed in km/h
    CurrentPosition_m : REAL; // Current train position in meters from reference point
    PrecedingTrainPosition_m : REAL; // Position of the preceding train in meters
    PrecedingTrainSpeed_Kmh : REAL; // Speed of the preceding train
    TrackGrade_Percent : REAL; // Track gradient
    TrackAdhesionFactor : REAL; // Track adhesion factor (0.0 to 1.0)
    MaxLineSpeed_Kmh : REAL; // Maximum allowable line speed
    CommunicationValid : BOOL; // Valid VOBC communication status
END_VAR

VAR_OUTPUT
    TargetSpeed_Kmh : REAL; // Calculated target speed for traction control
    BrakeCommand : BOOL; // Emergency brake intervention command
    ServiceBrakeEffort : REAL; // Requested service brake effort (0.0 - 1.0)
    SafeDistance_m : REAL; // Calculated safe braking distance
    MovementAuthority_m : REAL; // Granted movement authority limit
    Alarm_Proximity : BOOL; // Proximity warning alarm
    SystemFault : BOOL; // System fault indicator
END_VAR

VAR
    ReactionTime_s : REAL := 2.5; // System reaction time (VOBC + delays)
    SafetyMargin_m : REAL := 50.0; // Absolute safety margin
    DecelerationRate_ms2 : REAL := 0.8; // Nominal service deceleration
    EmergencyDeceleration_ms2 : REAL := 1.2; // Emergency deceleration
    Speed_ms : REAL;
    PrecedingSpeed_ms : REAL;
    StoppingDistance_m : REAL;
    PrecedingStoppingDistance_m : REAL;
    RelativeDistance_m : REAL;
    EffectiveDeceleration_ms2 : REAL;
    GradeEffect_ms2 : REAL;
    Gravity : REAL := 9.81;
END_VAR

// Implementation Details
IF NOT Enable OR NOT CommunicationValid THEN
    TargetSpeed_Kmh := 0.0;
    BrakeCommand := TRUE; // Fail-safe emergency brake
    ServiceBrakeEffort := 1.0;
    MovementAuthority_m := CurrentPosition_m;
    SystemFault := NOT CommunicationValid;
    RETURN;
END_IF;

SystemFault := FALSE;
BrakeCommand := FALSE;

// Convert speeds to m/s for calculations
Speed_ms := CurrentSpeed_Kmh / 3.6;
PrecedingSpeed_ms := PrecedingTrainSpeed_Kmh / 3.6;

// Calculate grade effect on braking (positive grade aids braking, negative hinders)
GradeEffect_ms2 := Gravity * (TrackGrade_Percent / 100.0);

// Determine effective emergency deceleration factoring adhesion and grade
EffectiveDeceleration_ms2 := (EmergencyDeceleration_ms2 * TrackAdhesionFactor) + GradeEffect_ms2;
IF EffectiveDeceleration_ms2 < 0.3 THEN
    EffectiveDeceleration_ms2 := 0.3; // Minimum guaranteed deceleration
END_IF;

// Calculate minimum stopping distance for ego train
StoppingDistance_m := (Speed_ms * Speed_ms) / (2.0 * EffectiveDeceleration_ms2) + (Speed_ms * ReactionTime_s);

// Calculate Movement Authority limit
MovementAuthority_m := PrecedingTrainPosition_m - SafetyMargin_m;

// Calculate actual relative distance
RelativeDistance_m := MovementAuthority_m - CurrentPosition_m;

// Determine safe separation
SafeDistance_m := StoppingDistance_m + SafetyMargin_m;

// Control Logic
IF RelativeDistance_m <= SafeDistance_m THEN
    Alarm_Proximity := TRUE;
    
    // Calculate required service brake effort
    IF RelativeDistance_m <= (StoppingDistance_m * 0.8) THEN
        BrakeCommand := TRUE; // Emergency brake
        ServiceBrakeEffort := 1.0;
        TargetSpeed_Kmh := 0.0;
    ELSE
        // Modulate service brake
        ServiceBrakeEffort := 1.0 - ((RelativeDistance_m - (StoppingDistance_m * 0.8)) / (SafeDistance_m - (StoppingDistance_m * 0.8)));
        IF ServiceBrakeEffort > 1.0 THEN ServiceBrakeEffort := 1.0; END_IF;
        IF ServiceBrakeEffort < 0.0 THEN ServiceBrakeEffort := 0.0; END_IF;
        TargetSpeed_Kmh := CurrentSpeed_Kmh * 0.5; // Request speed reduction
    END_IF;
ELSE
    Alarm_Proximity := FALSE;
    ServiceBrakeEffort := 0.0;
    IF CurrentSpeed_Kmh < MaxLineSpeed_Kmh THEN
        TargetSpeed_Kmh := MaxLineSpeed_Kmh;
    ELSE
        TargetSpeed_Kmh := CurrentSpeed_Kmh;
    END_IF;
END_IF;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open("data/swarm_raw/agent_rail_cbtc.json", "w", encoding="utf-8") as f:
    json.dump(record, f)
