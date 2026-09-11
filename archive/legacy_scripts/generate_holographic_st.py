import json, uuid
import os

user_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Holographic Foil Embossing Machine.
Task: Invent a highly complex control scenario for this domain (e.g., heated nip roller pressure micro-adjustments, holographic shim seam registration, and unwinder tension isolation).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

assistant_response = """```iec-st
FUNCTION_BLOCK FB_HoloFoilEmbosser_AdvancedCtrl
TITLE = 'Holographic Foil Embossing Machine - High-Precision Seam & Pressure Control'
VERSION : '2.5'

VAR_INPUT
    bEnable                 : BOOL;   (* Enable the embossing control loop *)
    bReset                  : BOOL;   (* Acknowledge and reset faults *)
    lrLineSpeedMaster       : LREAL;  (* Master machine speed [m/min] *)
    lrTargetTension         : LREAL;  (* Desired unwinder tension [N] *)
    lrActualTension         : LREAL;  (* Measured tension from load cells [N] *)
    lrTargetNipPressure     : LREAL;  (* Target nip roller pressure [bar] *)
    lrActualNipPressure     : LREAL;  (* Actual nip pressure [bar] *)
    lrTargetNipTemp         : LREAL;  (* Target nip roller temperature [°C] *)
    lrActualNipTemp         : LREAL;  (* Measured nip roller temperature [°C] *)
    diShimSeamPosition      : DINT;   (* Encoder counts for shim seam position *)
    diFoilRegisterMark      : DINT;   (* High-speed latch position of foil register mark *)
    lrShimCircumference     : LREAL;  (* Circumference of the holographic shim [mm] *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;   (* System is ready and within tolerances *)
    bFault                  : BOOL;   (* General fault indicator *)
    iFaultCode              : INT;    (* Specific fault code *)
    lrUnwinderTorqueRef     : LREAL;  (* Torque reference for unwinder drive [%] *)
    lrNipPressureValveCmd   : LREAL;  (* Command to proportional pressure valve [0-10V] *)
    bNipHeaterEnable        : BOOL;   (* Enable signal for SSR heating elements *)
    lrWebGuideCorrection    : LREAL;  (* Correction value for lateral web guide [mm] *)
    bPhaseSyncActive        : BOOL;   (* Seam and foil mark are phase synchronized *)
END_VAR

VAR
    // Internal States
    iState                  : INT := 0; // State machine step
    
    // PI Controller Variables - Tension
    lrTensionError          : LREAL;
    lrTensionIntegral       : LREAL;
    lrKp_Tension            : LREAL := 0.85;
    lrKi_Tension            : LREAL := 0.15;
    
    // PID Controller Variables - Temperature
    lrTempError             : LREAL;
    lrTempIntegral          : LREAL;
    lrTempDerivative        : LREAL;
    lrTempLastError         : LREAL;
    lrKp_Temp               : LREAL := 2.5;
    lrKi_Temp               : LREAL := 0.05;
    lrKd_Temp               : LREAL := 0.8;
    
    // Seam Registration Variables
    lrRegisterError         : LREAL;
    lrRegisterTolerance     : LREAL := 0.05; (* 50 microns *)
    lrPhaseCorrection       : LREAL;
    diExpectedMarkPos       : DINT;
    
    // Pressure Micro-adjustments
    lrPressureError         : LREAL;
    lrPressureGain          : LREAL := 0.5;
    lrThermalExpComp        : LREAL; // Compensation for roller thermal expansion
    
    // Timers
    tHeaterPulseTimer       : TON;
    tFaultTimer             : TON;
    
    // Constants
    lrMAX_TORQUE            : LREAL := 100.0;
    lrMAX_VALVE_V           : LREAL := 10.0;
    lrMAX_TEMP              : LREAL := 250.0;
END_VAR

(* -----------------------------------------------------------------------------
   HOLOGRAPHIC FOIL EMBOSSING - MAIN CONTROL ROUTINE
   ----------------------------------------------------------------------------- *)

// Fault Reset
IF bReset THEN
    bFault := FALSE;
    iFaultCode := 0;
    iState := 0;
END_IF;

// Over-Temperature Protection
IF lrActualNipTemp > lrMAX_TEMP THEN
    bFault := TRUE;
    iFaultCode := 101; // OTP Fault
    bNipHeaterEnable := FALSE;
    bSystemReady := FALSE;
    RETURN;
END_IF;

IF NOT bEnable THEN
    lrUnwinderTorqueRef := 0.0;
    lrNipPressureValveCmd := 0.0;
    bNipHeaterEnable := FALSE;
    bSystemReady := FALSE;
    iState := 0;
    RETURN;
END_IF;

// 1. TENSION CONTROL (Unwinder Isolation)
lrTensionError := lrTargetTension - lrActualTension;
lrTensionIntegral := lrTensionIntegral + (lrTensionError * 0.01); // Assuming 10ms task
// Anti-windup
IF lrTensionIntegral > 50.0 THEN lrTensionIntegral := 50.0; END_IF;
IF lrTensionIntegral < -50.0 THEN lrTensionIntegral := -50.0; END_IF;

lrUnwinderTorqueRef := (lrKp_Tension * lrTensionError) + (lrKi_Tension * lrTensionIntegral);
// Feedforward based on line speed
lrUnwinderTorqueRef := lrUnwinderTorqueRef + (lrLineSpeedMaster * 0.2);
IF lrUnwinderTorqueRef > lrMAX_TORQUE THEN lrUnwinderTorqueRef := lrMAX_TORQUE; END_IF;
IF lrUnwinderTorqueRef < 0.0 THEN lrUnwinderTorqueRef := 0.0; END_IF;

// 2. TEMPERATURE CONTROL (Heated Nip Roller)
lrTempError := lrTargetNipTemp - lrActualNipTemp;
lrTempIntegral := lrTempIntegral + (lrTempError * 0.01);
lrTempDerivative := (lrTempError - lrTempLastError) / 0.01;
lrTempLastError := lrTempError;

// PWM Logic for Heater SSR
tHeaterPulseTimer(IN := NOT tHeaterPulseTimer.Q, PT := T#1S);
IF (lrKp_Temp * lrTempError + lrKi_Temp * lrTempIntegral + lrKd_Temp * lrTempDerivative) > 50.0 THEN
    bNipHeaterEnable := TRUE;
ELSE
    bNipHeaterEnable := FALSE;
END_IF;

// 3. NIP PRESSURE MICRO-ADJUSTMENTS
// Thermal expansion compensation: roller swells 0.005 bar equiv per degree over 100C
IF lrActualNipTemp > 100.0 THEN
    lrThermalExpComp := (lrActualNipTemp - 100.0) * 0.005;
ELSE
    lrThermalExpComp := 0.0;
END_IF;

lrPressureError := lrTargetNipPressure - lrActualNipPressure - lrThermalExpComp;
lrNipPressureValveCmd := lrTargetNipPressure * 0.8 + (lrPressureError * lrPressureGain);
IF lrNipPressureValveCmd > lrMAX_VALVE_V THEN lrNipPressureValveCmd := lrMAX_VALVE_V; END_IF;
IF lrNipPressureValveCmd < 0.0 THEN lrNipPressureValveCmd := 0.0; END_IF;

// 4. HOLOGRAPHIC SHIM SEAM REGISTRATION
// Calculate theoretical register mark position
// Modulo arithmetic for continuous rotation
diExpectedMarkPos := diShimSeamPosition MOD LREAL_TO_DINT(lrShimCircumference * 1000.0); // assuming 1000 cnts/mm

// Calculate error (shortest path)
lrRegisterError := DINT_TO_LREAL(diFoilRegisterMark - diExpectedMarkPos) / 1000.0;
IF lrRegisterError > (lrShimCircumference / 2.0) THEN
    lrRegisterError := lrRegisterError - lrShimCircumference;
ELSIF lrRegisterError < -(lrShimCircumference / 2.0) THEN
    lrRegisterError := lrRegisterError + lrShimCircumference;
END_IF;

IF ABS(lrRegisterError) < lrRegisterTolerance THEN
    bPhaseSyncActive := TRUE;
    lrPhaseCorrection := 0.0;
ELSE
    bPhaseSyncActive := FALSE;
    // P-control for phase correction mapped to web guide
    lrPhaseCorrection := lrRegisterError * 0.2; 
END_IF;
lrWebGuideCorrection := lrPhaseCorrection;

// System Ready Evaluation
IF ABS(lrTensionError) < 2.0 AND ABS(lrTempError) < 5.0 AND ABS(lrPressureError) < 0.2 AND bPhaseSyncActive THEN
    bSystemReady := TRUE;
ELSE
    bSystemReady := FALSE;
END_IF;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": user_prompt}, {"role": "assistant", "content": assistant_response}]}

os.makedirs("data/swarm_raw", exist_ok=True)
os.makedirs("data", exist_ok=True)

with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f)

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")
