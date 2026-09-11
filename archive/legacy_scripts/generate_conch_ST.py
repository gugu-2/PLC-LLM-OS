import os, json, uuid

os.makedirs('data/swarm_raw', exist_ok=True)
prompt = "Write a highly complex Structured Text control scenario for an Industrial Chocolate Conching Machine, including motor shear viscosity torque feedback, automated cocoa butter dosing profiles, and volatile acid stripping ventilation."
code = """```iec-st
FUNCTION_BLOCK FB_Conching_Process_Control
VAR_INPUT
    bStartProcess : BOOL; // Start process flag
    bEmergencyStop : BOOL; // Emergency stop
    rMotorTorqueFeedback : REAL; // Current motor torque (Nm) representing viscosity
    rTemperatureProcess : REAL; // Process temperature (deg C)
    rTargetViscosity : REAL; // Target viscosity metric
    rTimeElapsed_Hours : REAL; // Process time elapsed in hours
    bVentilationFlowOk : BOOL; // True if exhaust air flow is OK
END_VAR

VAR_OUTPUT
    rMainMotorSpeedCmd : REAL; // Main agitator motor speed (RPM)
    rHeaterPowerCmd : REAL; // Heating element power (0.0 to 100.0%)
    rCoolingValveCmd : REAL; // Cooling water valve position (0.0 to 100.0%)
    rButterDosingRate : REAL; // Cocoa butter dosing rate (L/hr)
    bVentilationFanCmd : BOOL; // Ventilation fan command
    rAcidStrippingDamperCmd : REAL; // Damper position for volatile extraction (0.0 to 100.0%)
    bProcessComplete : BOOL; // Process complete flag
    eState : INT; // Current state
END_VAR

VAR
    rPID_Integral : REAL := 0.0;
    rPID_LastError : REAL := 0.0;
    rKp : REAL := 2.5;
    rKi : REAL := 0.1;
    rKd : REAL := 0.05;
    rTempSetPoint : REAL := 60.0; // Phase dependent target temperature
    
    // Conching Phases
    STATE_IDLE : INT := 0;
    STATE_DRY_CONCHING : INT := 1;
    STATE_PASTY_CONCHING : INT := 2;
    STATE_LIQUID_CONCHING : INT := 3;
    STATE_COOLING : INT := 4;
    STATE_DONE : INT := 5;
    STATE_ERROR : INT := 99;
END_VAR

// Main State Machine Logic
IF bEmergencyStop THEN
    eState := STATE_ERROR;
    rMainMotorSpeedCmd := 0.0;
    rHeaterPowerCmd := 0.0;
    rCoolingValveCmd := 100.0;
    rButterDosingRate := 0.0;
    bVentilationFanCmd := TRUE;
    rAcidStrippingDamperCmd := 100.0;
    bProcessComplete := FALSE;
    RETURN;
END_IF;

CASE eState OF
    STATE_IDLE:
        rMainMotorSpeedCmd := 0.0;
        rHeaterPowerCmd := 0.0;
        rCoolingValveCmd := 0.0;
        rButterDosingRate := 0.0;
        bVentilationFanCmd := FALSE;
        rAcidStrippingDamperCmd := 0.0;
        IF bStartProcess THEN
            eState := STATE_DRY_CONCHING;
        END_IF;
        
    STATE_DRY_CONCHING:
        // Phase 1: Dry conching (0 to 6 hours)
        // High torque, high friction, extracting moisture and volatile acids.
        rTempSetPoint := 65.0; // Moderate heat
        rMainMotorSpeedCmd := 30.0; // Low speed high torque
        
        // Venting is critical here for acid stripping
        bVentilationFanCmd := TRUE;
        rAcidStrippingDamperCmd := 100.0;
        rButterDosingRate := 0.0;
        
        IF rTimeElapsed_Hours > 6.0 THEN
            eState := STATE_PASTY_CONCHING;
        END_IF;
        
    STATE_PASTY_CONCHING:
        // Phase 2: Pasty conching (6 to 18 hours)
        // Viscosity starts dropping. Start adding some cocoa butter.
        rTempSetPoint := 75.0; // Higher heat
        
        // Dynamic speed based on torque
        IF rMotorTorqueFeedback > 500.0 THEN
            rMainMotorSpeedCmd := 40.0;
        ELSE
            rMainMotorSpeedCmd := 60.0;
        END_IF;
        
        // Moderate ventilation
        bVentilationFanCmd := TRUE;
        rAcidStrippingDamperCmd := 50.0;
        
        // Dose butter if torque is too high (viscosity reducing profile)
        IF rMotorTorqueFeedback > 600.0 THEN
            rButterDosingRate := 15.0;
        ELSE
            rButterDosingRate := 5.0;
        END_IF;
        
        IF rTimeElapsed_Hours > 18.0 THEN
            eState := STATE_LIQUID_CONCHING;
        END_IF;
        
    STATE_LIQUID_CONCHING:
        // Phase 3: Liquid conching (18 to 22 hours)
        // Final viscosity adjustment and flavor development
        rTempSetPoint := 60.0; 
        rMainMotorSpeedCmd := 80.0; // High speed
        
        // Butter dosing controlled by PID based on Target Viscosity vs Torque
        rButterDosingRate := (rMotorTorqueFeedback - rTargetViscosity) * 0.1;
        IF rButterDosingRate < 0.0 THEN rButterDosingRate := 0.0; END_IF;
        IF rButterDosingRate > 30.0 THEN rButterDosingRate := 30.0; END_IF;
        
        bVentilationFanCmd := FALSE;
        rAcidStrippingDamperCmd := 10.0;
        
        IF rTimeElapsed_Hours > 22.0 THEN
            eState := STATE_COOLING;
        END_IF;
        
    STATE_COOLING:
        rTempSetPoint := 45.0;
        rMainMotorSpeedCmd := 20.0;
        rButterDosingRate := 0.0;
        bVentilationFanCmd := FALSE;
        rAcidStrippingDamperCmd := 0.0;
        
        IF rTemperatureProcess <= 46.0 THEN
            eState := STATE_DONE;
        END_IF;
        
    STATE_DONE:
        rMainMotorSpeedCmd := 0.0;
        rHeaterPowerCmd := 0.0;
        rCoolingValveCmd := 0.0;
        bProcessComplete := TRUE;
        
    STATE_ERROR:
        // Safety fallback
        rMainMotorSpeedCmd := 0.0;
        rHeaterPowerCmd := 0.0;
        rCoolingValveCmd := 100.0;
        
END_CASE;

// Temperature PID Control
IF eState <> STATE_ERROR AND eState <> STATE_IDLE AND eState <> STATE_DONE THEN
    VAR
        rError : REAL;
        rDerivative : REAL;
        rOutput : REAL;
    END_VAR
    rError := rTempSetPoint - rTemperatureProcess;
    rPID_Integral := rPID_Integral + (rError * 0.1); // Assuming 100ms cycle time
    // Anti-windup
    IF rPID_Integral > 100.0 THEN rPID_Integral := 100.0; END_IF;
    IF rPID_Integral < -100.0 THEN rPID_Integral := -100.0; END_IF;
    
    rDerivative := (rError - rPID_LastError) / 0.1;
    rOutput := (rKp * rError) + (rKi * rPID_Integral) + (rKd * rDerivative);
    
    IF rOutput > 0.0 THEN
        rHeaterPowerCmd := rOutput;
        rCoolingValveCmd := 0.0;
    ELSE
        rHeaterPowerCmd := 0.0;
        rCoolingValveCmd := ABS(rOutput);
    END_IF;
    
    // Bounds
    IF rHeaterPowerCmd > 100.0 THEN rHeaterPowerCmd := 100.0; END_IF;
    IF rCoolingValveCmd > 100.0 THEN rCoolingValveCmd := 100.0; END_IF;
    
    rPID_LastError := rError;
END_IF;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=4)
print(filename)
