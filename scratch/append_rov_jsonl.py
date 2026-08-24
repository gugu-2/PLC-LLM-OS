import json
import sys

prompt = """You are acting as the Chief Robotics Engineer for a Deep-Ocean Biology Institute.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Abyssal Hydrothermal Vent Extremophile Harvesting ROV & Biomass Chemostat Controller" (`FB_Hydrothermal_ROV`).

### Technical Specifications & Engineering Rigor Required:
1. **Supercritical Fluid Sampling**:
   - Closed-loop robotic manipulator control to precisely insert titanium sampling wands into 400°C "black smoker" hydrothermal vents emitting supercritical water at 300 bar of pressure.
   - Isobaric sample isolation chambers maintaining the extreme pressure and temperature gradient while ascending to the surface, preventing extremophile cell lysis.
2. **Plume Tracking & Thruster Station-Keeping**:
   - Multi-beam sonar and dissolved hydrogen sulfide (H2S) concentration gradient tracking to autonomously navigate blindly through the opaque mineral plume.
   - 6-DOF vectored thrust station-keeping countering chaotic thermal updrafts (> 2 m/s) to keep the ROV perfectly hovering.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, comprehensive `VAR_INPUT`/`VAR_OUTPUT`, PackML states."""

response = """```iec-st
(*
=================================================================================================
    FB_Hydrothermal_ROV
    Description: Abyssal Hydrothermal Vent Extremophile Harvesting ROV & Biomass Chemostat
    Institute:   Deep-Ocean Biology Institute
    Author:      Chief Robotics Engineer
    Standard:    IEC 61131-3 Structured Text (ST)
    Version:     1.0.0
=================================================================================================
*)
FUNCTION_BLOCK FB_Hydrothermal_ROV
VAR_INPUT
    bEnable                 : BOOL;   // System enable
    bStartMission           : BOOL;   // Trigger to commence the mission
    bAbort                  : BOOL;   // Emergency abort
    bAscent                 : BOOL;   // Surface command
    
    // Telemetry & Sensor Data
    fDepth_m                : LREAL;  // Current depth (m)
    fAmbientTemp_C          : LREAL;  // Ambient water temperature (C)
    fAmbientPress_bar       : LREAL;  // Ambient pressure (bar)
    fVentTemp_C             : LREAL;  // IR/Thermocouple vent temp (C)
    fH2S_Concentration_ppm  : LREAL;  // Dissolved H2S gradient
    
    // Sonar & Spatial 
    aSonarPointClouds       : ARRAY[0..255] OF LREAL; // Multibeam raw returns
    fUpdraftVel_ms          : LREAL;  // Measured thermal updraft velocity (m/s)
    
    // ROV Kinematics (6-DOF Position & Orientation)
    stROVPose               : ST_Pose_6DOF;  // X, Y, Z, Roll, Pitch, Yaw
    stTargetPose            : ST_Pose_6DOF;
END_VAR

VAR_OUTPUT
    // State Machine (PackML-inspired)
    eState                  : E_ROV_State;
    bSamplingActive         : BOOL;
    bStationKeepingActive   : BOOL;
    bIsobaricSecure         : BOOL;
    
    // Thruster Commands (6-DOF Vectored Thrust)
    aThrusterPower          : ARRAY[1..6] OF LREAL; // -100.0 to 100.0 %
    
    // Manipulator Commands
    fArmExtension_mm        : LREAL;
    fArmAngle_deg           : LREAL;
    bWandValveOpen          : BOOL;
    
    // Subsystem Alarms
    bCriticalTempAlarm      : BOOL;
    bIsobaricSealFailed     : BOOL;
    bLossOfNavigation       : BOOL;
END_VAR

VAR
    // PID Controllers
    fbHoverPID_Z            : FB_PID_Advanced;
    fbHoverPID_X            : FB_PID_Advanced;
    fbHoverPID_Y            : FB_PID_Advanced;
    fbAttitudePID_R         : FB_PID_Advanced;
    fbAttitudePID_P         : FB_PID_Advanced;
    fbAttitudePID_Y         : FB_PID_Advanced;
    
    // Plume Tracking Algorithm
    fbPlumeTracker          : FB_GradientDescentNav;
    
    // Isobaric Chamber Management
    fChamberPress_bar       : LREAL;
    fChamberTemp_C          : LREAL;
    fbChamberThermalControl : FB_PID_Advanced;
    
    // Timers
    tSamplingTimer          : TON;
    tGradientSample         : TON;
    
    // Internal States
    bVentLocated            : BOOL;
    bHoverStable            : BOOL;
    fDistToTarget_m         : LREAL;
    
    // Constants
    cMaxSafeTemp            : LREAL := 450.0; // Max wand temp C
    cTargetSampleVol_mL     : LREAL := 500.0;
    cIsobaricTargetPress    : LREAL := 300.0;
END_VAR

// ===========================================================================
// MAIN CONTROL EXECUTION
// ===========================================================================

// 1. Safety Interlocks & Abort Checking
IF bAbort OR fVentTemp_C > cMaxSafeTemp THEN
    eState := E_ROV_State.ABORTING;
END_IF

// 2. PackML State Machine
CASE eState OF
    
    E_ROV_State.IDLE:
        bSamplingActive := FALSE;
        bStationKeepingActive := FALSE;
        aThrusterPower[1] := 0.0;
        // Zero out other thrusters...
        IF bEnable AND bStartMission THEN
            eState := E_ROV_State.PLUME_SEARCH;
        END_IF
        
    E_ROV_State.PLUME_SEARCH:
        // Blind Navigation via H2S Gradient & Multi-beam Sonar
        tGradientSample(IN := TRUE, PT := T#1S);
        IF tGradientSample.Q THEN
            fbPlumeTracker(
                fCurrentConcentration := fH2S_Concentration_ppm,
                aSonarData := aSonarPointClouds,
                stSuggestedVector => stTargetPose
            );
            tGradientSample(IN := FALSE);
        END_IF
        
        // Check if vent is within manipulator range (e.g. 1.5m, Temp > 350C)
        fDistToTarget_m := SQRT(EXPT(stTargetPose.X - stROVPose.X, 2) + EXPT(stTargetPose.Y - stROVPose.Y, 2));
        IF fDistToTarget_m < 1.5 AND fVentTemp_C > 350.0 THEN
            bVentLocated := TRUE;
            eState := E_ROV_State.STATION_KEEPING;
        END_IF
        
    E_ROV_State.STATION_KEEPING:
        bStationKeepingActive := TRUE;
        
        // 6-DOF Station Keeping countering chaotic thermal updrafts (>2 m/s)
        // Z-axis PID specifically compensates for fUpdraftVel_ms (feed-forward)
        fbHoverPID_Z(
            fSetpoint := stTargetPose.Z,
            fActual   := stROVPose.Z,
            fFeedForward := (fUpdraftVel_ms * 15.0), // Thrust compensation factor
            fKp := 4.5, fKi := 1.2, fKd := 0.8,
            fOutput => aThrusterPower[1] // Vertical Thrusters
        );
        
        // X/Y and Attitude PIDs (Simplified representation)
        fbHoverPID_X(fSetpoint:=stTargetPose.X, fActual:=stROVPose.X, fOutput=>aThrusterPower[2]);
        fbHoverPID_Y(fSetpoint:=stTargetPose.Y, fActual:=stROVPose.Y, fOutput=>aThrusterPower[3]);
        fbAttitudePID_R(fSetpoint:=stTargetPose.Roll, fActual:=stROVPose.Roll, fOutput=>aThrusterPower[4]);
        fbAttitudePID_P(fSetpoint:=stTargetPose.Pitch, fActual:=stROVPose.Pitch, fOutput=>aThrusterPower[5]);
        fbAttitudePID_Y(fSetpoint:=stTargetPose.Yaw, fActual:=stROVPose.Yaw, fOutput=>aThrusterPower[6]);
        
        // Determine stability threshold
        bHoverStable := (ABS(stTargetPose.Z - stROVPose.Z) < 0.05) AND 
                        (ABS(stTargetPose.X - stROVPose.X) < 0.1);
                        
        IF bHoverStable THEN
            eState := E_ROV_State.SAMPLING;
        END_IF
        
    E_ROV_State.SAMPLING:
        bSamplingActive := TRUE;
        
        // Maintain hovering while sampling
        // (Call PIDs here as well...)
        
        // Manipulator logic for supercritical water insertion
        fArmExtension_mm := 1200.0; // Extend wand into vent
        fArmAngle_deg := -15.5;
        
        tSamplingTimer(IN := TRUE, PT := T#15S); // Time required to fill 500mL at 300 bar
        
        IF fVentTemp_C >= 380.0 AND fAmbientPress_bar > 290.0 THEN
            bWandValveOpen := TRUE; // Intake supercritical fluid
        END_IF
        
        IF tSamplingTimer.Q THEN
            bWandValveOpen := FALSE;
            fArmExtension_mm := 0.0; // Retract wand
            tSamplingTimer(IN := FALSE);
            eState := E_ROV_State.ISOBARIC_ISOLATION;
        END_IF
        
    E_ROV_State.ISOBARIC_ISOLATION:
        bSamplingActive := FALSE;
        
        // Lock pressure chamber to maintain 300 bar and gradient temperature
        fChamberPress_bar := cIsobaricTargetPress;
        bIsobaricSecure := TRUE;
        
        // Thermal control for the chemostat during ascent
        fbChamberThermalControl(
            fSetpoint := 400.0, // Extremophile target
            fActual   := fChamberTemp_C,
            fOutput   => (* Heater PWM *) // Dummy mapping for example
        );
        
        IF bIsobaricSecure AND bAscent THEN
            eState := E_ROV_State.ASCENDING;
        END_IF
        
    E_ROV_State.ASCENDING:
        // Command vertical thrusters for slow ascent, maintaining chamber integrity
        aThrusterPower[1] := -25.0; // Positive buoyancy or upward thrust
        
        IF fDepth_m < 5.0 THEN
            eState := E_ROV_State.COMPLETED;
        END_IF
        
    E_ROV_State.COMPLETED:
        aThrusterPower[1] := 0.0;
        
    E_ROV_State.ABORTING:
        bSamplingActive := FALSE;
        bWandValveOpen := FALSE;
        fArmExtension_mm := 0.0;
        // Emergency blow ballast / max ascent thrust
        aThrusterPower[1] := -100.0;
        
END_CASE

// 3. Subsystem Alarms
bCriticalTempAlarm := fVentTemp_C > cMaxSafeTemp;
bIsobaricSealFailed := bIsobaricSecure AND (fChamberPress_bar < (cIsobaricTargetPress - 10.0));
bLossOfNavigation := (aSonarPointClouds[0] = 0.0) AND (fH2S_Concentration_ppm = 0.0);

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {
            "role": "user",
            "content": prompt
        },
        {
            "role": "assistant",
            "content": response
        }
    ]
}

out_file = r"C:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"
with open(out_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(record, ensure_ascii=False) + "\n")

print("Appended successfully.")
