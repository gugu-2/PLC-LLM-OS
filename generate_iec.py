import json, uuid, os

st_code = """FUNCTION_BLOCK FB_WindFarmWakeSteering
VAR_INPUT
    bEnableWakeSteering : BOOL; (* Enable/Disable Wake Steering Optimization *)
    rWindSpeed : REAL; (* Incoming Free-stream Wind Speed (m/s) *)
    rWindDirection : REAL; (* Incoming Wind Direction (degrees) *)
    rActivePowerDemand : REAL; (* Grid Active Power Demand (MW) *)
    rGridFrequency : REAL; (* Grid Frequency (Hz) *)
    rNominalFrequency : REAL := 50.0; (* Nominal Grid Frequency (Hz) *)
    rDroopCoefficient : REAL := 0.04; (* Frequency Droop Coefficient *)
    aTurbineStatus : ARRAY[1..10] OF BOOL; (* Status of each turbine (TRUE=OK) *)
END_VAR

VAR_OUTPUT
    aYawMisalignmentTargets : ARRAY[1..10] OF REAL; (* Target Yaw Misalignment per turbine (degrees) *)
    aPowerCurtailmentTargets : ARRAY[1..10] OF REAL; (* Target Active Power per turbine (MW) *)
    bFrequencyResponseActive : BOOL; (* Droop control active *)
    rTotalFarmPowerTarget : REAL; (* Total Wind Farm Power Target (MW) *)
END_VAR

VAR
    i : INT;
    rFrequencyError : REAL;
    rFrequencyPowerAdjustment : REAL;
    rBaseFarmTarget : REAL;
    aWakeDeflectionCoefficients : ARRAY[1..10, 1..10] OF REAL; (* Simplified interaction matrix *)
    rMaxYawMisalignment : REAL := 25.0; (* Max allowable yaw misalignment (degrees) *)
    rOptimalYaw : REAL;
    rAvailablePowerPerTurbine : REAL := 5.0; (* Assume 5MW nominal per turbine *)
    iActiveTurbines : INT;
END_VAR

(* 1. Calculate Grid Frequency Droop Response *)
rFrequencyError := rNominalFrequency - rGridFrequency;
IF ABS(rFrequencyError) > 0.05 THEN
    bFrequencyResponseActive := TRUE;
    (* P_delta = -(delta_f / (f_nom * Droop)) * P_nom *)
    rFrequencyPowerAdjustment := (rFrequencyError / (rNominalFrequency * rDroopCoefficient)) * (10.0 * rAvailablePowerPerTurbine);
ELSE
    bFrequencyResponseActive := FALSE;
    rFrequencyPowerAdjustment := 0.0;
END_IF;

(* 2. Determine Total Farm Target *)
rBaseFarmTarget := MIN(rActivePowerDemand, 10.0 * rAvailablePowerPerTurbine);
rTotalFarmPowerTarget := LIMIT(0.0, rBaseFarmTarget + rFrequencyPowerAdjustment, 10.0 * rAvailablePowerPerTurbine);

(* 3. Count Active Turbines *)
iActiveTurbines := 0;
FOR i := 1 TO 10 DO
    IF aTurbineStatus[i] THEN
        iActiveTurbines := iActiveTurbines + 1;
    END_IF;
END_FOR;

(* 4. Dispatch Wake Steering and Power *)
IF bEnableWakeSteering AND (iActiveTurbines > 0) THEN
    (* Simplified Wake Steering Logic: Upstream turbines misalign to deflect wake *)
    FOR i := 1 TO 10 DO
        IF aTurbineStatus[i] THEN
            (* Dummy algorithm: Turbines 1-3 are upstream for 270 deg wind *)
            IF (rWindDirection > 250.0 AND rWindDirection < 290.0) AND (i <= 3) THEN
                rOptimalYaw := rMaxYawMisalignment * (1.0 - (rWindSpeed / 25.0)); 
                aYawMisalignmentTargets[i] := LIMIT(-rMaxYawMisalignment, rOptimalYaw, rMaxYawMisalignment);
            ELSE
                aYawMisalignmentTargets[i] := 0.0;
            END_IF;
            
            (* Equal dispatch of power with compensation for wake *)
            aPowerCurtailmentTargets[i] := rTotalFarmPowerTarget / INT_TO_REAL(iActiveTurbines);
        ELSE
            aYawMisalignmentTargets[i] := 0.0;
            aPowerCurtailmentTargets[i] := 0.0;
        END_IF;
    END_FOR;
ELSE
    (* Fallback to normal operation: 0 yaw misalignment, equal dispatch *)
    FOR i := 1 TO 10 DO
        aYawMisalignmentTargets[i] := 0.0;
        IF aTurbineStatus[i] AND (iActiveTurbines > 0) THEN
            aPowerCurtailmentTargets[i] := rTotalFarmPowerTarget / INT_TO_REAL(iActiveTurbines);
        ELSE
            aPowerCurtailmentTargets[i] := 0.0;
        END_IF;
    END_FOR;
END_IF;
END_FUNCTION_BLOCK
"""

prompt = "Invent a highly complex control scenario for Utility-Scale Wind Farm Wake Steering (e.g., yaw misalignment optimization for array efficiency, active power curtailment tracking, and grid frequency droop response). Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": f"```iec-st\n{st_code}\n```"}]}

os.makedirs("c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw", exist_ok=True)
filename = f"c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
print(f"Saved to {filename}")
