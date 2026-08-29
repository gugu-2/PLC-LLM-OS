import json
import uuid
import os

workspace_dir = r"c:\Users\majip\Downloads\LLM REASEARCH"
swarm_dir = os.path.join(workspace_dir, "data", "swarm_raw")
os.makedirs(swarm_dir, exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: High-Voltage Static Synchronous Compensator (STATCOM).
Task: Invent a highly complex control scenario for this domain (e.g., grid voltage droop curves, IGBT cascaded H-bridge switching, and capacitor voltage balancing).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

st_code = """```iec-st
FUNCTION_BLOCK FB_STATCOM_HighVoltageControl
TITLE = 'STATCOM Cascaded H-Bridge Control'
VERSION : '1.0'

VAR_INPUT
    bEnable                 : BOOL;   (* Enable STATCOM Control *)
    bFaultReset             : BOOL;   (* Reset Faults *)
    rGridVoltage_PU         : REAL;   (* Per Unit Grid Voltage *)
    rReferenceVoltage_PU    : REAL;   (* Per Unit Reference Voltage *)
    rActivePowerTarget_MW   : REAL;   (* Target Active Power (for loss compensation) *)
    rDroopGain              : REAL;   (* Droop characteristic gain (pu/MVAR) *)
    rCapacitorVoltage_V     : ARRAY[1..12] OF REAL; (* Sub-module capacitor voltages *)
    rGridCurrent_A          : REAL;   (* Measured Grid Current *)
    rPhaseAngle_Rad         : REAL;   (* Grid Phase Angle from PLL *)
    rDcLinkVoltageRef_V     : REAL;   (* Reference DC link voltage for balancing *)
END_VAR

VAR_OUTPUT
    bActive                 : BOOL;   (* STATCOM is active *)
    bFault                  : BOOL;   (* Fault state active *)
    wFaultCode              : WORD;   (* Fault code *)
    rReactivePowerOutput    : REAL;   (* Actual Reactive Power Output (MVAR) *)
    rModulationIndex        : REAL;   (* Modulation Index for PWM *)
    rPhaseShift             : REAL;   (* Phase shift angle for inverter *)
    bGatePulses             : ARRAY[1..48] OF BOOL; (* IGBT Gate Pulses for 12 sub-modules (4 IGBTs each) *)
END_VAR

VAR
    i                       : INT;
    rErrorVoltage           : REAL;
    rReactivePowerDemand    : REAL;
    rTotalCapVoltage        : REAL;
    rCapVoltageAvg          : REAL;
    rVoltageBalancingKp     : REAL := 0.05;
    rVoltageBalancingKi     : REAL := 0.01;
    rVoltageBalancingInt    : ARRAY[1..12] OF REAL;
    rSubModuleDutyCycle     : ARRAY[1..12] OF REAL;
    rPI_ControllerInt       : REAL;
    rPI_ControllerKp        : REAL := 2.5;
    rPI_ControllerKi        : REAL := 10.0;
    rSamplingTime           : REAL := 0.0001; (* 100 microseconds *)
    bCapacitorOverVoltage   : BOOL;
    bCapacitorUnderVoltage  : BOOL;
    rMaxCapVoltageLimit     : REAL := 1200.0; (* 1200V max per SM *)
    rMinCapVoltageLimit     : REAL := 700.0;  (* 700V min per SM *)
    rCarrierWave            : REAL;
    rTimeAccumulator        : REAL;
END_VAR

(* Fault Reset logic *)
IF bFaultReset THEN
    bFault := FALSE;
    wFaultCode := 16#0000;
END_IF;

(* Main Execution Condition *)
IF NOT bEnable THEN
    bActive := FALSE;
    rPI_ControllerInt := 0.0;
    FOR i := 1 TO 12 DO
        rVoltageBalancingInt[i] := 0.0;
        bGatePulses[(i-1)*4 + 1] := FALSE;
        bGatePulses[(i-1)*4 + 2] := FALSE;
        bGatePulses[(i-1)*4 + 3] := FALSE;
        bGatePulses[(i-1)*4 + 4] := FALSE;
    END_FOR;
    RETURN;
END_IF;

bActive := TRUE;

(* 1. Grid Voltage Droop Control *)
(* Calculate error between reference and actual grid voltage *)
rErrorVoltage := rReferenceVoltage_PU - rGridVoltage_PU;

(* Droop control to determine reactive power demand *)
rReactivePowerDemand := (rErrorVoltage / rDroopGain);

(* Limit Reactive Power Demand to safe operating bounds (-100 to 100 MVAR) *)
IF rReactivePowerDemand > 100.0 THEN
    rReactivePowerDemand := 100.0;
ELSIF rReactivePowerDemand < -100.0 THEN
    rReactivePowerDemand := -100.0;
END_IF;

(* 2. Sub-module Capacitor Voltage Balancing and Monitoring *)
rTotalCapVoltage := 0.0;
bCapacitorOverVoltage := FALSE;
bCapacitorUnderVoltage := FALSE;

FOR i := 1 TO 12 DO
    rTotalCapVoltage := rTotalCapVoltage + rCapacitorVoltage_V[i];
    
    (* Fault checks *)
    IF rCapacitorVoltage_V[i] > rMaxCapVoltageLimit THEN
        bCapacitorOverVoltage := TRUE;
    END_IF;
    
    IF rCapacitorVoltage_V[i] < rMinCapVoltageLimit THEN
        bCapacitorUnderVoltage := TRUE;
    END_IF;
END_FOR;

rCapVoltageAvg := rTotalCapVoltage / 12.0;

IF bCapacitorOverVoltage THEN
    bFault := TRUE;
    wFaultCode := 16#0001; (* Overvoltage fault *)
    bActive := FALSE;
    RETURN;
END_IF;

IF bCapacitorUnderVoltage THEN
    bFault := TRUE;
    wFaultCode := 16#0002; (* Undervoltage fault *)
    bActive := FALSE;
    RETURN;
END_IF;

(* 3. Modulation Index and Phase Shift calculation *)
(* PI Controller for reactive current / voltage error *)
rPI_ControllerInt := rPI_ControllerInt + (rErrorVoltage * rSamplingTime * rPI_ControllerKi);

(* Anti-windup for PI *)
IF rPI_ControllerInt > 1.0 THEN
    rPI_ControllerInt := 1.0;
ELSIF rPI_ControllerInt < -1.0 THEN
    rPI_ControllerInt := -1.0;
END_IF;

rModulationIndex := (rErrorVoltage * rPI_ControllerKp) + rPI_ControllerInt;
IF rModulationIndex > 1.0 THEN
    rModulationIndex := 1.0;
ELSIF rModulationIndex < 0.0 THEN
    rModulationIndex := 0.0;
END_IF;

rPhaseShift := 0.1 * rActivePowerTarget_MW; (* Simplified phase shift for active power losses *)

(* 4. Cascaded H-Bridge Switching (Phase-Shifted Carrier PWM) *)
rTimeAccumulator := rTimeAccumulator + rSamplingTime;
IF rTimeAccumulator >= (1.0 / 50.0) THEN
    rTimeAccumulator := 0.0;
END_IF;

FOR i := 1 TO 12 DO
    (* Voltage balancing PI per sub-module *)
    rVoltageBalancingInt[i] := rVoltageBalancingInt[i] + ((rCapVoltageAvg - rCapacitorVoltage_V[i]) * rSamplingTime * rVoltageBalancingKi);
    rSubModuleDutyCycle[i] := rModulationIndex + ((rCapVoltageAvg - rCapacitorVoltage_V[i]) * rVoltageBalancingKp) + rVoltageBalancingInt[i];
    
    (* Carrier generation with phase shifting for harmonic reduction *)
    rCarrierWave := SIN(2.0 * 3.14159 * 50.0 * rTimeAccumulator + (i * 3.14159 / 12.0));
    
    (* PWM Comparison logic for 4 IGBTs in H-Bridge *)
    IF rSubModuleDutyCycle[i] > rCarrierWave THEN
        bGatePulses[(i-1)*4 + 1] := TRUE;  (* S1 *)
        bGatePulses[(i-1)*4 + 4] := TRUE;  (* S4 *)
        bGatePulses[(i-1)*4 + 2] := FALSE; (* S2 *)
        bGatePulses[(i-1)*4 + 3] := FALSE; (* S3 *)
    ELSE
        bGatePulses[(i-1)*4 + 1] := FALSE; 
        bGatePulses[(i-1)*4 + 4] := FALSE;
        bGatePulses[(i-1)*4 + 2] := TRUE;
        bGatePulses[(i-1)*4 + 3] := TRUE;
    END_IF;
END_FOR;

rReactivePowerOutput := rReactivePowerDemand;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

filename = f"agent_{uuid.uuid4().hex[:8]}.json"
file_path = os.path.join(swarm_dir, filename)
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

print(f"Success: {file_path}")
