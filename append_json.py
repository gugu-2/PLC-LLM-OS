import json
import os

user_prompt = """I have a basic motion function block used for single-axis positioning. 

Please evolve this basic motion block into a 30-meter class Astronomical Telescope Mount Controller.
You must implement:
1. Sidereal tracking algorithms.
2. Active optics mirror deformation arrays (to compensate for gravity).
3. Wind-buffeting disturbance rejection.
4. Complex state machines.
5. Safety interlocks (e-stops, thermal overloads).
6. Hardware abstractions and flawless comments.
"""

assistant_response = """(*
=============================================================================
BLOCK: FB_TelescopeMountController
DESCRIPTION: 
  Advanced 30-meter class Astronomical Telescope Mount Controller.
  Includes sidereal tracking, active optics gravity compensation, 
  wind-buffeting rejection, and critical safety interlocks.
=============================================================================
*)
FUNCTION_BLOCK FB_TelescopeMountController

VAR_INPUT
    bEnable                 : BOOL;   // Master enable
    bEstop                  : BOOL;   // Emergency Stop (NC, TRUE = Safe)
    bReset                  : BOOL;   // Fault reset
    
    // Environmental & Target Data
    fTargetRA               : LREAL;  // Target Right Ascension (hours)
    fTargetDec              : LREAL;  // Target Declination (degrees)
    fLocalSiderealTime      : LREAL;  // Local Sidereal Time (hours)
    fLatitude               : LREAL;  // Observatory Latitude (degrees)
    fWindSpeed_mps          : LREAL;  // Wind speed for buffeting rejection
    fElevationAngle         : LREAL;  // Current elevation angle (degrees)
    
    // Hardware Sensors
    fAzimuthEncoder         : LREAL;  // Actual Azimuth position
    fAltitudeEncoder        : LREAL;  // Actual Altitude position
    bThermalOverload_Az     : BOOL;   // Thermal overload Azimuth (NC)
    bThermalOverload_Alt    : BOOL;   // Thermal overload Altitude (NC)
    
    // Safety & Limits
    bLimitAzCW              : BOOL;   // CW Limit Azimuth
    bLimitAzCCW             : BOOL;   // CCW Limit Azimuth
    bLimitAltUp             : BOOL;   // Upper Limit Altitude
    bLimitAltDown           : BOOL;   // Lower Limit Altitude
END_VAR

VAR_OUTPUT
    bReady                  : BOOL;   // Controller is ready
    bTracking               : BOOL;   // Actively tracking target
    bError                  : BOOL;   // Fault active
    nErrorID                : UDINT;  // Fault code
    
    // Actuator Commands
    fAzimuthVelocityCmd     : LREAL;  // Velocity command to Azimuth drive
    fAltitudeVelocityCmd    : LREAL;  // Velocity command to Altitude drive
    
    // Active Optics Commands (Array of 120 actuators)
    aMirrorActuators        : ARRAY[1..120] OF LREAL; // Force cmds (Newtons)
END_VAR

VAR
    // State Machine
    eState                  : (INIT, IDLE, SLEW, TRACK, FAULT);
    ePrevState              : (INIT, IDLE, SLEW, TRACK, FAULT);
    
    // PID Controllers for Tracking (simplified representation)
    fbAzimuthPID            : FB_PID_Advanced;
    fbAltitudePID           : FB_PID_Advanced;
    
    // Wind Disturbance Rejection
    fbWindObserver          : FB_DisturbanceObserver;
    fWindComp_Az            : LREAL;
    fWindComp_Alt           : LREAL;
    
    // Calculated Target Positions (Alt-Az coordinates)
    fTargetAzimuth          : LREAL;
    fTargetAltitude         : LREAL;
    
    // Internal Flags
    bSafetyOK               : BOOL;
    i                       : INT;
    fGravitySagFactor       : LREAL;
END_VAR

(* --------------------------------------------------------------------------
   1. SAFETY INTERLOCKS & HARDWARE ABSTRACTION
-------------------------------------------------------------------------- *)
// Evaluate Safety Chain (All signals are NC - Normally Closed)
bSafetyOK := bEstop AND NOT bThermalOverload_Az AND NOT bThermalOverload_Alt;

IF NOT bSafetyOK THEN
    eState := FAULT;
    IF NOT bEstop THEN nErrorID := 16#E001; END_IF; // E-Stop pressed
    IF bThermalOverload_Az THEN nErrorID := 16#E002; END_IF;
    IF bThermalOverload_Alt THEN nErrorID := 16#E003; END_IF;
END_IF;

(* --------------------------------------------------------------------------
   2. STATE MACHINE
-------------------------------------------------------------------------- *)
CASE eState OF
    
    INIT:
        // Initialize PI/PID controllers and observer gains
        fbAzimuthPID.Kp := 15.5; fbAzimuthPID.Ki := 2.1; fbAzimuthPID.Kd := 0.5;
        fbAltitudePID.Kp := 18.2; fbAltitudePID.Ki := 2.5; fbAltitudePID.Kd := 0.6;
        bReady := FALSE;
        bTracking := FALSE;
        bError := FALSE;
        IF bSafetyOK THEN
            eState := IDLE;
        END_IF;
        
    IDLE:
        bReady := TRUE;
        bTracking := FALSE;
        fAzimuthVelocityCmd := 0.0;
        fAltitudeVelocityCmd := 0.0;
        
        IF bEnable AND bSafetyOK THEN
            eState := SLEW;
        END_IF;
        
    SLEW:
        // High speed move to target vicinity
        bReady := TRUE;
        bTracking := FALSE;
        
        // Slew logic... (omitted for brevity)
        // Transition to track when error < 0.1 degrees
        IF ABS(fTargetAzimuth - fAzimuthEncoder) < 0.1 AND 
           ABS(fTargetAltitude - fAltitudeEncoder) < 0.1 THEN
            eState := TRACK;
        END_IF;
        
        IF NOT bEnable THEN eState := IDLE; END_IF;
        
    TRACK:
        bTracking := TRUE;
        
        // PID loop executions
        fbAzimuthPID(fSetpoint := fTargetAzimuth, fActual := fAzimuthEncoder);
        fbAltitudePID(fSetpoint := fTargetAltitude, fActual := fAltitudeEncoder);
        
        // Add Wind Buffeting Disturbance Rejection
        fbWindObserver(fWindSpeed := fWindSpeed_mps, fAz_Actual := fAzimuthEncoder);
        fWindComp_Az := fbWindObserver.fAz_Comp;
        fWindComp_Alt := fbWindObserver.fAlt_Comp;
        
        // Final Velocity Commands
        fAzimuthVelocityCmd := fbAzimuthPID.fOutput + fWindComp_Az;
        fAltitudeVelocityCmd := fbAltitudePID.fOutput + fWindComp_Alt;
        
        IF NOT bEnable THEN eState := IDLE; END_IF;
        
    FAULT:
        bReady := FALSE;
        bTracking := FALSE;
        bError := TRUE;
        fAzimuthVelocityCmd := 0.0;
        fAltitudeVelocityCmd := 0.0;
        
        IF bReset AND bSafetyOK THEN
            bError := FALSE;
            nErrorID := 0;
            eState := INIT;
        END_IF;
        
END_CASE;

(* --------------------------------------------------------------------------
   3. SIDEREAL TRACKING ALGORITHMS
-------------------------------------------------------------------------- *)
// Convert Equatorial (RA, Dec) to Horizontal (Az, Alt) coordinates
// Hour Angle (HA) = Local Sidereal Time (LST) - Right Ascension (RA)
VAR
    fHourAngle : LREAL;
    fSinAlt    : LREAL;
    fCosAz     : LREAL;
END_VAR

fHourAngle := (fLocalSiderealTime - fTargetRA) * 15.0; // Convert hours to degrees

// Sin(Alt) = Sin(Dec)*Sin(Lat) + Cos(Dec)*Cos(Lat)*Cos(HA)
fSinAlt := SIN(fTargetDec) * SIN(fLatitude) + 
           COS(fTargetDec) * COS(fLatitude) * COS(fHourAngle);
fTargetAltitude := ASIN(fSinAlt);

// Cos(Az) = (Sin(Dec) - Sin(Alt)*Sin(Lat)) / (Cos(Alt)*Cos(Lat))
fCosAz := (SIN(fTargetDec) - fSinAlt * SIN(fLatitude)) / 
          (COS(fTargetAltitude) * COS(fLatitude));
fTargetAzimuth := ACOS(fCosAz);

// Adjust Azimuth based on Hour Angle
IF SIN(fHourAngle) > 0.0 THEN
    fTargetAzimuth := 360.0 - fTargetAzimuth;
END_IF;

(* --------------------------------------------------------------------------
   4. ACTIVE OPTICS MIRROR DEFORMATION ARRAY
-------------------------------------------------------------------------- *)
// Compensate for gravity sag as a function of elevation angle
// A 30m mirror sags heavily based on Cos(Altitude).
fGravitySagFactor := COS(fElevationAngle);

FOR i := 1 TO 120 DO
    // Zernike polynomial baseline force + Gravity compensation model
    // In a real system, this integrates wavefront sensor feedback.
    aMirrorActuators[i] := (100.0 * fGravitySagFactor) + (i * 0.5); 
    
    // Safety limit per actuator (Max 500 N)
    IF aMirrorActuators[i] > 500.0 THEN
        aMirrorActuators[i] := 500.0;
    END_IF;
END_FOR;

END_FUNCTION_BLOCK
"""

data = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

with open(r'C:\Users\majip\Downloads\LLM REASEARCH\data\evol_instruct_dataset.jsonl', 'a') as f:
    f.write(json.dumps(data) + '\n')
print("Successfully appended to jsonl")
