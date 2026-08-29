import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Concentrated Solar Power (CSP) Parabolic Trough.
Task: Invent a highly complex control scenario for this domain (e.g., Synthetic Oil Heat Transfer Fluid (HTF) mass flow balancing, precise solar tracking actuator kinematics, and steam generator thermal cascades).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

response = """```iec-st
FUNCTION_BLOCK FB_CSP_Parabolic_Trough_Controller
TITLE = 'Concentrated Solar Power (CSP) Parabolic Trough Advanced Controller'
VERSION : '2.1'
AUTHOR : 'Lumina AI Cloud Swarm'

VAR_INPUT
    rSunAzimuth_deg         : REAL;   // Current solar azimuth angle in degrees
    rSunElevation_deg       : REAL;   // Current solar elevation angle in degrees
    rDNI_W_m2               : REAL;   // Direct Normal Irradiance (W/m^2)
    rWindSpeed_m_s          : REAL;   // Wind speed (m/s)
    rInletTemp_HTF_C        : REAL;   // Inlet Heat Transfer Fluid temperature (Celsius)
    rOutletTemp_HTF_C       : REAL;   // Outlet Heat Transfer Fluid temperature (Celsius)
    rPressure_HTF_bar       : REAL;   // HTF system pressure (bar)
    rFlowRate_HTF_kg_s      : REAL;   // Current HTF mass flow rate (kg/s)
    bSystemEnable           : BOOL;   // Global system enable flag
    bEmergencyStow          : BOOL;   // Emergency stow command (e.g., high wind, alarm)
    rTargetOutletTemp_C     : REAL;   // Target HTF outlet temperature (Celsius)
END_VAR

VAR_OUTPUT
    rTargetTrackingAngle_deg: REAL;   // Target angle for the parabolic trough actuators
    rTrackingSpeed_deg_s    : REAL;   // Kinematic speed for the actuator movement
    rPumpSpeed_RPM          : REAL;   // HTF pump speed command (RPM)
    rTargetFlowRate_kg_s    : REAL;   // Calculated optimal HTF mass flow rate
    bValveBypass_Open       : BOOL;   // Steam generator bypass valve command
    bTrackingActive         : BOOL;   // Indicates if active tracking is engaged
    bStowed                 : BOOL;   // Indicates if trough is in safe stow position
    wAlarmWord              : WORD;   // System alarms and diagnostics
END_VAR

VAR
    rTrackingError_deg      : REAL;   // Internal tracking error calculation
    rTempError_C            : REAL;   // Internal temperature error
    rTempErrorIntegral      : REAL;   // Integral part of temperature PID
    rTempErrorDerivative    : REAL;   // Derivative part of temperature PID
    rPrevTempError_C        : REAL;   // Previous temperature error for PID
    rDeltaTime_s            : REAL := 0.1; // Execution cycle time (100ms)
    
    rKp_Flow                : REAL := 2.5;
    rKi_Flow                : REAL := 0.05;
    rKd_Flow                : REAL := 0.1;
    
    rMaxFlowRate_kg_s       : REAL := 150.0;
    rMinFlowRate_kg_s       : REAL := 15.0;
    rStowAngle_deg          : REAL := -90.0;
    
    timerDefocus            : TON;    // Timer for temporary defocusing during high DNI transients
END_VAR

// Control Logic Implementation
IF NOT bSystemEnable OR bEmergencyStow OR rWindSpeed_m_s > 15.0 THEN
    // Safe mode / Emergency stow
    bTrackingActive := FALSE;
    rTargetTrackingAngle_deg := rStowAngle_deg;
    rTrackingSpeed_deg_s := 2.0; // Fast movement to stow
    rTargetFlowRate_kg_s := rMinFlowRate_kg_s;
    bValveBypass_Open := TRUE;
    
    IF ABS(rTargetTrackingAngle_deg - rStowAngle_deg) < 1.0 THEN
        bStowed := TRUE;
    ELSE
        bStowed := FALSE;
    END_IF;
    
    // Reset PID
    rTempErrorIntegral := 0.0;
    rPrevTempError_C := 0.0;
    
    wAlarmWord := 16#0001; // Set stow alarm bit
    
ELSE
    // Normal Operation Mode
    bStowed := FALSE;
    bValveBypass_Open := FALSE;
    wAlarmWord := 16#0000;
    
    // 1. Solar Tracking Kinematics
    IF rSunElevation_deg > 5.0 THEN
        bTrackingActive := TRUE;
        // Simplified incidence angle calculation for North-South aligned trough
        rTargetTrackingAngle_deg := ATAN(TAN(rSunElevation_deg * 3.14159 / 180.0) / COS(rSunAzimuth_deg * 3.14159 / 180.0)) * 180.0 / 3.14159;
        rTrackingSpeed_deg_s := 0.1; // Slow precise tracking
    ELSE
        // Sun below operational horizon
        bTrackingActive := FALSE;
        rTargetTrackingAngle_deg := rStowAngle_deg;
        rTrackingSpeed_deg_s := 1.0;
    END_IF;
    
    // 2. High DNI Defocusing Logic (Avoid HTF degradation)
    timerDefocus(IN := (rDNI_W_m2 > 1100.0 AND rOutletTemp_HTF_C > 395.0), PT := T#10s);
    IF timerDefocus.Q THEN
        // Introduce artificial tracking error to shed thermal load
        rTargetTrackingAngle_deg := rTargetTrackingAngle_deg + 3.0; 
        wAlarmWord.1 := 1; // High thermal load warning bit
    END_IF;

    // 3. HTF Mass Flow Balancing (PID Control for Outlet Temperature)
    rTempError_C := rOutletTemp_HTF_C - rTargetOutletTemp_C;
    
    // Anti-windup for integral term
    IF (rTargetFlowRate_kg_s < rMaxFlowRate_kg_s AND rTargetFlowRate_kg_s > rMinFlowRate_kg_s) THEN
        rTempErrorIntegral := rTempErrorIntegral + (rTempError_C * rDeltaTime_s);
    END_IF;
    
    rTempErrorDerivative := (rTempError_C - rPrevTempError_C) / rDeltaTime_s;
    rPrevTempError_C := rTempError_C;
    
    // Calculate new target flow rate based on error (Inverted response: higher temp -> higher flow)
    rTargetFlowRate_kg_s := (rKp_Flow * rTempError_C) + (rKi_Flow * rTempErrorIntegral) + (rKd_Flow * rTempErrorDerivative) + rFlowRate_HTF_kg_s;
    
    // Limit flow rate output
    IF rTargetFlowRate_kg_s > rMaxFlowRate_kg_s THEN
        rTargetFlowRate_kg_s := rMaxFlowRate_kg_s;
    ELSIF rTargetFlowRate_kg_s < rMinFlowRate_kg_s THEN
        rTargetFlowRate_kg_s := rMinFlowRate_kg_s;
    END_IF;
    
    // Convert target mass flow to Pump RPM (assuming linear correlation for simulation)
    rPumpSpeed_RPM := (rTargetFlowRate_kg_s / rMaxFlowRate_kg_s) * 3000.0;
    
    // Thermal cascade steam generator checks
    IF rInletTemp_HTF_C < 250.0 THEN
        // If return temp from steam generator is too low, slow down flow slightly to maintain boiler pressure
        rTargetFlowRate_kg_s := rTargetFlowRate_kg_s * 0.9;
        wAlarmWord.2 := 1; // Cold return warning
    END_IF;

END_IF;

END_FUNCTION_BLOCK
```"""

os.makedirs('data/swarm_raw', exist_ok=True)
record = {'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': response}]}
file_path = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(record, f, indent=2)
print(f'Wrote to {file_path}')
