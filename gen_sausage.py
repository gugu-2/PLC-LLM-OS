import json, uuid, os

os.makedirs('data/swarm_raw', exist_ok=True)
prompt = 'Invent a highly complex control scenario for an Industrial Sausage Stuffer (e.g., vacuum meat emulsion vane pumping, automatic twist casing linking servos, and exact weight portioning feedback). Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.'
code = '''FUNCTION_BLOCK FB_SausageStufferControl
VAR_INPUT
    bEnable : BOOL; // System enable
    bStartFilling : BOOL; // Start filling process
    bCasingLoaded : BOOL; // Casing is loaded and ready
    rTargetWeight_g : REAL := 100.0; // Target portion weight in grams
    rActualWeight_g : REAL; // Current weight from scale
    rVacuumLevel_bar : REAL; // Current vacuum level
    rVanePumpSpeed_RPM : REAL; // Current speed of the vane pump
    bEmergencyStop : BOOL; // Emergency stop signal
END_VAR
VAR_OUTPUT
    bSystemReady : BOOL;
    bFillingActive : BOOL;
    bLinkingActive : BOOL;
    rCmdPumpSpeed_RPM : REAL; // Command speed to the vane pump
    bCmdVacuumPump : BOOL; // Command to turn on vacuum pump
    rCmdTwistServo_Deg : REAL; // Command to twist servo
    bFault : BOOL; // System fault
    nErrorCode : INT; // Error code (0=No Error, 1=EStop, 2=Vacuum Loss, 3=Weight Error)
END_VAR
VAR
    eState : (INIT, READY, VACUUM_BUILDUP, FILLING, LINKING, FAULT) := INIT;
    rWeightError : REAL;
    KP_PUMP : REAL := 2.5; // Proportional gain for pump
    KI_PUMP : REAL := 0.5; // Integral gain for pump
    rIntegralSum : REAL := 0.0;
    rLastWeight_g : REAL := 0.0;
    nTwistCount : INT := 0;
END_VAR

// Emergency Stop Check
IF bEmergencyStop THEN
    eState := FAULT;
    nErrorCode := 1;
END_IF;

// Main State Machine
CASE eState OF
    INIT:
        bSystemReady := FALSE;
        bFillingActive := FALSE;
        bLinkingActive := FALSE;
        rCmdPumpSpeed_RPM := 0.0;
        bCmdVacuumPump := FALSE;
        rCmdTwistServo_Deg := 0.0;
        bFault := FALSE;
        nErrorCode := 0;
        
        IF bEnable THEN
            eState := READY;
        END_IF;
        
    READY:
        bSystemReady := TRUE;
        IF bStartFilling AND bCasingLoaded THEN
            eState := VACUUM_BUILDUP;
        END_IF;
        
    VACUUM_BUILDUP:
        bCmdVacuumPump := TRUE;
        bSystemReady := FALSE;
        
        IF rVacuumLevel_bar <= -0.8 THEN // Target vacuum reached
            eState := FILLING;
            rIntegralSum := 0.0;
            rLastWeight_g := rActualWeight_g;
        ELSIF rVacuumLevel_bar > -0.2 AND bCmdVacuumPump THEN
            // timeout logic
        END_IF;
        
    FILLING:
        bFillingActive := TRUE;
        
        // PI Control for Vane Pump based on target weight trajectory
        rWeightError := rTargetWeight_g - (rActualWeight_g - rLastWeight_g);
        
        IF rWeightError > 0.0 THEN
            rIntegralSum := rIntegralSum + rWeightError;
            // Anti-windup
            IF rIntegralSum > 100.0 THEN rIntegralSum := 100.0; END_IF;
            
            rCmdPumpSpeed_RPM := (KP_PUMP * rWeightError) + (KI_PUMP * rIntegralSum);
            
            // Limit max speed
            IF rCmdPumpSpeed_RPM > 1500.0 THEN rCmdPumpSpeed_RPM := 1500.0; END_IF;
        ELSE
            // Target weight reached
            rCmdPumpSpeed_RPM := 0.0;
            bFillingActive := FALSE;
            eState := LINKING;
        END_IF;
        
    LINKING:
        bLinkingActive := TRUE;
        // Twist servo to link the sausage
        rCmdTwistServo_Deg := rCmdTwistServo_Deg + 360.0; // Full rotation to twist
        nTwistCount := nTwistCount + 1;
        
        // Simulating immediate finish of linking
        bLinkingActive := FALSE;
        rLastWeight_g := rActualWeight_g;
        
        IF bStartFilling THEN
            eState := FILLING; // Continue to next link
        ELSE
            eState := READY;
        END_IF;
        
    FAULT:
        bSystemReady := FALSE;
        bFillingActive := FALSE;
        bLinkingActive := FALSE;
        rCmdPumpSpeed_RPM := 0.0;
        bCmdVacuumPump := FALSE;
        bFault := TRUE;
        
        IF NOT bEmergencyStop AND bEnable = FALSE THEN
            // Reset required
            eState := INIT;
        END_IF;
        
END_CASE;
END_FUNCTION_BLOCK'''
record = {'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': '```iec-st\n' + code + '\n```'}]}
filename = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(record, f, indent=2)
print(f"Written to {filename}")
