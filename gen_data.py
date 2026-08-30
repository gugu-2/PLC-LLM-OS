import json, uuid, os

record = {
    "messages": [
        {
            "role": "user", 
            "content": "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\nYour specific domain is: CNC Wire Electrical Discharge Machining (EDM).\nTask: Invent a highly complex control scenario for this domain (e.g., deionized water dielectric conductivity, continuous wire tension unspooling, and spark gap voltage optimization).\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."
        }, 
        {
            "role": "assistant", 
            "content": """```iec-st
FUNCTION_BLOCK FB_WireEDM_ProcessController
VAR_INPUT
    rTargetSparkGapVoltage      : REAL;   (* Setpoint for spark gap voltage [V] *)
    rActualSparkGapVoltage      : REAL;   (* Feedback from gap sensor [V] *)
    rTargetWireTension          : REAL;   (* Setpoint for wire tension [N] *)
    rActualWireTension          : REAL;   (* Feedback from tension load cell [N] *)
    rTargetConductivity         : REAL;   (* Setpoint for dielectric conductivity [uS/cm] *)
    rActualConductivity         : REAL;   (* Feedback from conductivity sensor [uS/cm] *)
    rWireSpeed                  : REAL;   (* Current wire unspooling speed [m/min] *)
    bSystemEnable               : BOOL;   (* Master process enable *)
    bEmergencyStop              : BOOL;   (* Safety interlock *)
    rKp_Tension                 : REAL := 1.5;
    rKi_Tension                 : REAL := 0.5;
    rKd_Tension                 : REAL := 0.1;
    rKp_Conductivity            : REAL := 2.0;
    rKi_Conductivity            : REAL := 0.8;
END_VAR

VAR_OUTPUT
    rGeneratorPWMOutput         : REAL;   (* 0-100% PWM for spark generator power *)
    rUnspoolMotorTorqueCmd      : REAL;   (* Torque command to wire spool motor [Nm] *)
    rResinPumpSpeedCmd          : REAL;   (* Speed command to deionization resin pump [RPM] *)
    bWireBreakDetected          : BOOL;   (* Flag indicating sudden drop in tension *)
    bConductivityAlarm          : BOOL;   (* Flag indicating dielectric quality out of bounds *)
    bShortCircuitDetected       : BOOL;   (* Flag indicating electrode touching workpiece *)
    iMachineState               : INT;    (* 0=Idle, 1=Running, 2=Fault *)
END_VAR

VAR
    rTensionError               : REAL;
    rTensionErrorIntegral       : REAL;
    rTensionErrorPrev           : REAL;
    rTensionDerivative          : REAL;
    
    rCondError                  : REAL;
    rCondErrorIntegral          : REAL;
    
    rGapVoltageError            : REAL;
    
    rTensionTolerance           : REAL := 0.2; (* [N] *)
    rCondAlarmThreshold         : REAL := 50.0; (* [uS/cm] max limit *)
    rShortCircuitThreshold      : REAL := 5.0; (* [V] *)
    rWireBreakThreshold         : REAL := 1.0; (* [N] *)
    
    tCycleTime                  : REAL := 0.01; (* 10ms execution cycle *)
    
    rMaxTorque                  : REAL := 10.0; (* [Nm] *)
    rMaxPumpSpeed               : REAL := 3000.0; (* [RPM] *)
    
    bInitDone                   : BOOL := FALSE;
END_VAR

(* Initialization Block *)
IF NOT bInitDone THEN
    rTensionErrorIntegral := 0.0;
    rTensionErrorPrev := 0.0;
    rCondErrorIntegral := 0.0;
    bInitDone := TRUE;
END_IF

(* Safety and State Management *)
IF bEmergencyStop THEN
    rGeneratorPWMOutput := 0.0;
    rUnspoolMotorTorqueCmd := 0.0;
    rResinPumpSpeedCmd := 0.0;
    iMachineState := 2;
    RETURN;
ELSIF NOT bSystemEnable THEN
    rGeneratorPWMOutput := 0.0;
    rUnspoolMotorTorqueCmd := 0.0;
    rResinPumpSpeedCmd := 0.0;
    iMachineState := 0;
    RETURN;
ELSE
    iMachineState := 1;
END_IF

(* -------------------------------------------------------------
   1. Wire Tension Control (PID)
   ------------------------------------------------------------- *)
(* Detect Wire Break *)
IF rActualWireTension < rWireBreakThreshold AND rWireSpeed > 0.0 THEN
    bWireBreakDetected := TRUE;
    rUnspoolMotorTorqueCmd := 0.0;
    iMachineState := 2;
ELSE
    bWireBreakDetected := FALSE;
    
    rTensionError := rTargetWireTension - rActualWireTension;
    rTensionErrorIntegral := rTensionErrorIntegral + (rTensionError * tCycleTime);
    
    (* Anti-windup for Tension Integral *)
    IF rTensionErrorIntegral > 20.0 THEN
        rTensionErrorIntegral := 20.0;
    ELSIF rTensionErrorIntegral < -20.0 THEN
        rTensionErrorIntegral := -20.0;
    END_IF
    
    rTensionDerivative := (rTensionError - rTensionErrorPrev) / tCycleTime;
    
    rUnspoolMotorTorqueCmd := (rKp_Tension * rTensionError) + 
                              (rKi_Tension * rTensionErrorIntegral) + 
                              (rKd_Tension * rTensionDerivative);
                              
    rTensionErrorPrev := rTensionError;
    
    (* Output clamping *)
    IF rUnspoolMotorTorqueCmd > rMaxTorque THEN
        rUnspoolMotorTorqueCmd := rMaxTorque;
    ELSIF rUnspoolMotorTorqueCmd < 0.0 THEN
        rUnspoolMotorTorqueCmd := 0.0;
    END_IF
END_IF

(* -------------------------------------------------------------
   2. Dielectric Conductivity Control (PI)
   ------------------------------------------------------------- *)
(* If conductivity is too high, pump water through DI resin *)
rCondError := rActualConductivity - rTargetConductivity;

IF rCondError > 0.0 THEN
    rCondErrorIntegral := rCondErrorIntegral + (rCondError * tCycleTime);
ELSE
    (* Optional: Decay integral if we are below target to prevent windup *)
    rCondErrorIntegral := rCondErrorIntegral * 0.99;
END_IF

rResinPumpSpeedCmd := (rKp_Conductivity * rCondError) + (rKi_Conductivity * rCondErrorIntegral);

IF rResinPumpSpeedCmd > rMaxPumpSpeed THEN
    rResinPumpSpeedCmd := rMaxPumpSpeed;
ELSIF rResinPumpSpeedCmd < 0.0 THEN
    rResinPumpSpeedCmd := 0.0;
END_IF

IF rActualConductivity > rCondAlarmThreshold THEN
    bConductivityAlarm := TRUE;
ELSE
    bConductivityAlarm := FALSE;
END_IF

(* -------------------------------------------------------------
   3. Spark Gap Voltage Optimization
   ------------------------------------------------------------- *)
(* Maintain gap by regulating PWM power based on voltage deviation.
   In a real EDM, the feed rate is also adjusted, but here we adjust generator power. *)
   
IF rActualSparkGapVoltage < rShortCircuitThreshold THEN
    bShortCircuitDetected := TRUE;
    (* Immediately cut power to prevent wire melting *)
    rGeneratorPWMOutput := 0.0;
ELSE
    bShortCircuitDetected := FALSE;
    
    rGapVoltageError := rActualSparkGapVoltage - rTargetSparkGapVoltage;
    
    (* If gap voltage is higher than target, gap is too large -> increase power.
       If gap voltage is lower than target, gap is too small -> decrease power.
       Simple proportional relationship for this implementation. *)
       
    rGeneratorPWMOutput := 50.0 + (rGapVoltageError * 2.5); (* 50% base duty cycle *)
    
    IF rGeneratorPWMOutput > 100.0 THEN
        rGeneratorPWMOutput := 100.0;
    ELSIF rGeneratorPWMOutput < 10.0 THEN
        rGeneratorPWMOutput := 10.0; (* Maintain minimum pilot spark *)
    END_IF
END_IF

(* Critical Fault Handling *)
IF bWireBreakDetected OR bShortCircuitDetected THEN
    iMachineState := 2;
END_IF

END_FUNCTION_BLOCK
```"""
        }
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f)

# System instruction append
os.makedirs("data", exist_ok=True)
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
