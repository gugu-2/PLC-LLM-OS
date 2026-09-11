import json, uuid, os

prompt = "Generate a highly complex, production-ready IEC 61131-3 Structured Text (ST) FUNCTION_BLOCK for an Ultra-Class Mining Dump Truck. Focus on diesel-electric wheel motor traction control, dynamic retarder grid cooling, and payload weigh-scale averaging. Include complete VAR declarations and physical I/O."

code = """```iec-st
FUNCTION_BLOCK FB_UltraClass_MiningTruck_Control
TITLE = 'Ultra-Class Mining Dump Truck Core Control'
VERSION : '1.0'
AUTHOR  : 'Lumina Elite Synthetic Data Architect'

VAR_INPUT
    // Engine & Powertrain Inputs
    rDieselEngineSpeed        : REAL; // Engine RPM (0.0 - 2500.0)
    rThrottleCommand          : REAL; // Operator throttle command 0.0 to 100.0 %
    rBrakePedal               : REAL; // Service brake pedal 0.0 to 100.0 %
    rRetarderLever            : REAL; // Dynamic retarder lever 0.0 to 100.0 %
    
    // Wheel Motor Feedbacks
    rWheelSpeedLeft           : REAL; // Left wheel motor speed (RPM)
    rWheelSpeedRight          : REAL; // Right wheel motor speed (RPM)
    rMotorTempLeft            : REAL; // Left traction motor temperature (deg C)
    rMotorTempRight           : REAL; // Right traction motor temperature (deg C)
    
    // Suspension / Payload Sensors
    rStrutPressureFL          : REAL; // Front-Left suspension strut pressure (kPa)
    rStrutPressureFR          : REAL; // Front-Right suspension strut pressure (kPa)
    rStrutPressureRL          : REAL; // Rear-Left suspension strut pressure (kPa)
    rStrutPressureRR          : REAL; // Rear-Right suspension strut pressure (kPa)
    rInclinometerPitch        : REAL; // Vehicle pitch angle (degrees)
    rInclinometerRoll         : REAL; // Vehicle roll angle (degrees)
    
    // Retarder Grid System
    rGridTemp1                : REAL; // Retarder grid bank 1 temperature (deg C)
    rGridTemp2                : REAL; // Retarder grid bank 2 temperature (deg C)
    
    // Operator Controls
    bPayloadDumpSwitch        : BOOL; // Bed dump command
    bTractionControlBypass    : BOOL; // Override traction control limits
END_VAR

VAR_OUTPUT
    // Motor Control Commands
    rTractionTorqueCmdLeft    : REAL; // Torque command to left inverter (N-m)
    rTractionTorqueCmdRight   : REAL; // Torque command to right inverter (N-m)
    rRetarderEffortCmd        : REAL; // Blended retarder effort to grid choppers 0.0 to 100.0 %
    
    // Cooling Systems
    rBlowerFanSpeedCmd        : REAL; // Grid cooling blower fan command 0.0 to 100.0 %
    rMotorCoolingFanCmd       : REAL; // Traction motor cooling fan command 0.0 to 100.0 %
    
    // Powertrain & VIMS (Vital Information Management System)
    rEngineFuelDemand         : REAL; // Fuel injection demand to Engine ECU 0.0 to 100.0 %
    rEstimatedPayload         : REAL; // Filtered payload estimation (Tonnes)
    
    // Alarms and Warnings
    bGridOverTempAlarm        : BOOL; // Retarder grid temperature critical
    bTractionSlipAlarm        : BOOL; // Wheel slip condition active
    bMotorOverTempAlarm       : BOOL; // Traction motor temperature critical
END_VAR

VAR
    // Internal calculations
    rAverageSpeed             : REAL;
    rSlipRatioLeft            : REAL;
    rSlipRatioRight           : REAL;
    rMaxSlipAllowed           : REAL := 0.12; // 12% slip limit for optimal traction
    rTorqueLimitSlip          : REAL;
    
    // Payload estimation variables
    rFilterWeightFront        : REAL;
    rFilterWeightRear         : REAL;
    rRawPayloadTotal          : REAL;
    iPayloadFilterIndex       : INT := 0;
    arPayloadHistory          : ARRAY[0..99] OF REAL; // Moving average window (100 samples)
    rPayloadSum               : REAL := 0.0;
    bFilterInitialized        : BOOL := FALSE;
    i                         : INT;
    
    // Grid Cooling & Thermal Derating
    rMaxGridTemp              : REAL;
    rGridTempThreshold        : REAL := 680.0; // Max allowed temp before reducing retarder effort
    rGridTempCritical         : REAL := 800.0;
    rBlowerKp                 : REAL := 0.65;
    rRetarderDerateFactor     : REAL := 1.0;
    
    // Constants
    cEmptyVehicleWeight       : REAL := 160000.0; // 160 Tonnes tare weight
    cMaxTorqueLimit           : REAL := 25000.0;  // 25kNm per wheel motor
END_VAR

// ==============================================================================
// 1. PAYLOAD ESTIMATION & WEIGH-SCALE AVERAGING
// ==============================================================================
// Dynamic weight estimation compensating for vehicle pitch and roll.
// Uses a 100-sample moving average filter to smooth pressure spikes during haulage.

// Calculate dynamic weight distribution based on strut pressures and inclinometer
rFilterWeightFront := (rStrutPressureFL + rStrutPressureFR) * 0.42 * COS(rInclinometerPitch * 3.14159 / 180.0) * COS(rInclinometerRoll * 3.14159 / 180.0);
rFilterWeightRear  := (rStrutPressureRL + rStrutPressureRR) * 0.58 * COS(rInclinometerPitch * 3.14159 / 180.0) * COS(rInclinometerRoll * 3.14159 / 180.0);
rRawPayloadTotal   := rFilterWeightFront + rFilterWeightRear - cEmptyVehicleWeight; 

// Initialize filter array on first scan
IF NOT bFilterInitialized THEN
    FOR i := 0 TO 99 DO
        arPayloadHistory[i] := rRawPayloadTotal;
        rPayloadSum := rPayloadSum + rRawPayloadTotal;
    END_FOR;
    bFilterInitialized := TRUE;
ELSE
    // Moving Average Filter execution
    rPayloadSum := rPayloadSum - arPayloadHistory[iPayloadFilterIndex] + rRawPayloadTotal;
    arPayloadHistory[iPayloadFilterIndex] := rRawPayloadTotal;
    iPayloadFilterIndex := (iPayloadFilterIndex + 1) MOD 100;
END_IF;

rEstimatedPayload := rPayloadSum / 100.0;
// Zero clamp to prevent negative payload readings on bounce
IF rEstimatedPayload < 0.0 THEN
    rEstimatedPayload := 0.0;
END_IF;

// ==============================================================================
// 2. DIESEL-ELECTRIC TRACTION CONTROL & WHEEL SLIP REGULATION
// ==============================================================================
rAverageSpeed := (rWheelSpeedLeft + rWheelSpeedRight) / 2.0;

// Base fuel demand tied to throttle and engine governing (simplified)
rEngineFuelDemand := rThrottleCommand; 

// Calculate independent wheel slip ratios if vehicle is moving
IF rAverageSpeed > 5.0 THEN
    rSlipRatioLeft := (rWheelSpeedLeft - rAverageSpeed) / rAverageSpeed;
    rSlipRatioRight := (rWheelSpeedRight - rAverageSpeed) / rAverageSpeed;
ELSE
    rSlipRatioLeft := 0.0;
    rSlipRatioRight := 0.0;
END_IF;

// Evaluate Slip Conditions
bTractionSlipAlarm := (rSlipRatioLeft > rMaxSlipAllowed) OR (rSlipRatioRight > rMaxSlipAllowed);

// Dynamic Torque Derating for Traction Control
IF bTractionSlipAlarm AND NOT bTractionControlBypass THEN
    // Proportional torque reduction based on worst-case slip
    rTorqueLimitSlip := 1.0 - ((MAX(rSlipRatioLeft, rSlipRatioRight) - rMaxSlipAllowed) * 2.5);
    IF rTorqueLimitSlip < 0.2 THEN
        rTorqueLimitSlip := 0.2; // Minimum 20% torque retention to prevent stalling
    END_IF;
ELSE
    rTorqueLimitSlip := 1.0;
END_IF;

// Apply Torque Commands with Slip Limits
rTractionTorqueCmdLeft := (rThrottleCommand / 100.0) * cMaxTorqueLimit * rTorqueLimitSlip;
rTractionTorqueCmdRight := (rThrottleCommand / 100.0) * cMaxTorqueLimit * rTorqueLimitSlip;

// ==============================================================================
// 3. DYNAMIC RETARDER GRID COOLING & BRAKE BLENDING
// ==============================================================================
// Find highest grid temperature
IF rGridTemp1 > rGridTemp2 THEN
    rMaxGridTemp := rGridTemp1;
ELSE
    rMaxGridTemp := rGridTemp2;
END_IF;

// Grid Cooling Blower PI Control (Simplified to P-only for synthetic model)
IF rMaxGridTemp > 200.0 THEN
    rBlowerFanSpeedCmd := (rMaxGridTemp - 200.0) * rBlowerKp;
ELSE
    rBlowerFanSpeedCmd := 0.0;
END_IF;

IF rBlowerFanSpeedCmd > 100.0 THEN
    rBlowerFanSpeedCmd := 100.0;
END_IF;

// Thermal Derating of Retarder Grid
bGridOverTempAlarm := rMaxGridTemp > rGridTempThreshold;
IF rMaxGridTemp > rGridTempCritical THEN
    rRetarderDerateFactor := 0.0; // Shut down dynamic braking, force mechanical brakes
ELSIF bGridOverTempAlarm THEN
    // Linear derate from threshold to critical
    rRetarderDerateFactor := 1.0 - ((rMaxGridTemp - rGridTempThreshold) / (rGridTempCritical - rGridTempThreshold));
ELSE
    rRetarderDerateFactor := 1.0;
END_IF;

// Final Retarder Effort blending operator commands with thermal protection
rRetarderEffortCmd := (rRetarderLever + (rBrakePedal * 0.5)) * rRetarderDerateFactor;
IF rRetarderEffortCmd > 100.0 THEN
    rRetarderEffortCmd := 100.0;
END_IF;

// Motor Cooling Management
bMotorOverTempAlarm := (rMotorTempLeft > 180.0) OR (rMotorTempRight > 180.0);
IF bMotorOverTempAlarm OR (rTractionTorqueCmdLeft > cMaxTorqueLimit * 0.8) THEN
    rMotorCoolingFanCmd := 100.0;
ELSIF rAverageSpeed > 10.0 THEN
    rMotorCoolingFanCmd := 50.0;
ELSE
    rMotorCoolingFanCmd := 20.0; // Idle cooling
END_IF;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
out_dir = r"c:\Users\majip\Downloads\LLM REASEARCH\data\swarm_raw"
os.makedirs(out_dir, exist_ok=True)
with open(os.path.join(out_dir, f"agent_{uuid.uuid4().hex[:8]}.json"), "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
