# hpdc_megacasting_builder/build_st_phase5_thermal_die.py

def get_phase5_thermal_die():
    return """(* =====================================================================================================================
 * PHASE 5: MULTI-ZONE THERMAL DIE BALANCING & PULSED IN-MOLD SOLIDIFICATION SUBSYSTEM
 * 12-Zone Pressurized Water/Thermal Oil Temperature Regulation with Anti-Windup PID and PWM Duty Output
 * Fixed Die Half (Zones 1-6) and Moving Die Half (Zones 7-12)
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * 1. MAP SENSOR INPUTS TO INTERNAL MULTI-ZONE ARRAY
 * --------------------------------------------------------------------------------------------------------------------- *)
rDieTemp_Current[1]  := rDieTemp_Zone01_Fixed_In;
rDieTemp_Current[2]  := rDieTemp_Zone02_Fixed_In;
rDieTemp_Current[3]  := rDieTemp_Zone03_Fixed_In;
rDieTemp_Current[4]  := rDieTemp_Zone04_Fixed_In;
rDieTemp_Current[5]  := rDieTemp_Zone05_Fixed_In;
rDieTemp_Current[6]  := rDieTemp_Zone06_Fixed_In;
rDieTemp_Current[7]  := rDieTemp_Zone07_Moving_In;
rDieTemp_Current[8]  := rDieTemp_Zone08_Moving_In;
rDieTemp_Current[9]  := rDieTemp_Zone09_Moving_In;
rDieTemp_Current[10] := rDieTemp_Zone10_Moving_In;
rDieTemp_Current[11] := rDieTemp_Zone11_Moving_In;
rDieTemp_Current[12] := rDieTemp_Zone12_Moving_In;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2. INDEPENDENT PID REGULATION FOR 12 THERMAL ZONES
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR iZone_Loop := 1 TO 12 DO

    (* Temperature Error Calculation: Positive Error Indicates Overheating (Cooling Required) *)
    rDieTemp_Error[iZone_Loop] := rDieTemp_Current[iZone_Loop] - rDieTemp_Setpoint[iZone_Loop];

    (* Rate of Temperature Change (Derivative) in deg C / second *)
    rDieTemp_Derivative[iZone_Loop] := (rDieTemp_Current[iZone_Loop] - rDieTemp_Prev[iZone_Loop]) * 1000.0;

    (* Anti-Windup Integral Error Accumulator *)
    IF ABS(rDieTemp_Error[iZone_Loop]) < 25.0 THEN
        rDieTemp_Integral[iZone_Loop] := rDieTemp_Integral[iZone_Loop] + (rDieTemp_Error[iZone_Loop] * 0.001);
        (* Clamp Integral Accumulation *)
        IF rDieTemp_Integral[iZone_Loop] > 80.0 THEN
            rDieTemp_Integral[iZone_Loop] := 80.0;
        ELSIF rDieTemp_Integral[iZone_Loop] < -80.0 THEN
            rDieTemp_Integral[iZone_Loop] := -80.0;
        END_IF;
    ELSE
        (* Reset Integral Outside Active Proportional Band *)
        rDieTemp_Integral[iZone_Loop] := 0.0;
    END_IF;

    (* PID Cooling Demand Computation (Duty Cycle %) *)
    rDieCooling_DutyCycle[iZone_Loop] := (rPID_Kp[iZone_Loop] * rDieTemp_Error[iZone_Loop])
                                       + (rPID_Ki[iZone_Loop] * rDieTemp_Integral[iZone_Loop])
                                       + (rPID_Kd[iZone_Loop] * rDieTemp_Derivative[iZone_Loop]);

    (* Actuator Hard Saturation Bounds (0% to 100%) *)
    IF rDieCooling_DutyCycle[iZone_Loop] < 0.0 THEN
        rDieCooling_DutyCycle[iZone_Loop] := 0.0;
    ELSIF rDieCooling_DutyCycle[iZone_Loop] > 100.0 THEN
        rDieCooling_DutyCycle[iZone_Loop] := 100.0;
    END_IF;

    (* Computed Thermal Energy Extraction Rate: Q = m_dot * Cp * delta_T [kW] *)
    rDieHeatExtracted_kW[iZone_Loop] := (rDieCooling_DutyCycle[iZone_Loop] / 100.0) * 1.85 * 4.184 * 18.0;

    (* Store Current Temperature for Next Derivative Scan *)
    rDieTemp_Prev[iZone_Loop] := rDieTemp_Current[iZone_Loop];

END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * 3. 1,000 ms BASE PULSE-WIDTH MODULATION (PWM) SOLENOID VALVE DRIVER
 * --------------------------------------------------------------------------------------------------------------------- *)
iPWM_CycleCounter_ms := iPWM_CycleCounter_ms + 1;
IF iPWM_CycleCounter_ms >= 1000 THEN
    iPWM_CycleCounter_ms := 0;
END_IF;

(* Zone 1 PWM Output *)
IF iPWM_CycleCounter_ms < REAL_TO_INT(rDieCooling_DutyCycle[1] * 10.0) THEN
    rDieCooling_PWM_Zone01_Out := 100.0;
ELSE
    rDieCooling_PWM_Zone01_Out := 0.0;
END_IF;

(* Zone 2 PWM Output *)
IF iPWM_CycleCounter_ms < REAL_TO_INT(rDieCooling_DutyCycle[2] * 10.0) THEN
    rDieCooling_PWM_Zone02_Out := 100.0;
ELSE
    rDieCooling_PWM_Zone02_Out := 0.0;
END_IF;

(* Zone 3 PWM Output *)
IF iPWM_CycleCounter_ms < REAL_TO_INT(rDieCooling_DutyCycle[3] * 10.0) THEN
    rDieCooling_PWM_Zone03_Out := 100.0;
ELSE
    rDieCooling_PWM_Zone03_Out := 0.0;
END_IF;

(* Zone 4 PWM Output *)
IF iPWM_CycleCounter_ms < REAL_TO_INT(rDieCooling_DutyCycle[4] * 10.0) THEN
    rDieCooling_PWM_Zone04_Out := 100.0;
ELSE
    rDieCooling_PWM_Zone04_Out := 0.0;
END_IF;

(* Zone 5 PWM Output *)
IF iPWM_CycleCounter_ms < REAL_TO_INT(rDieCooling_DutyCycle[5] * 10.0) THEN
    rDieCooling_PWM_Zone05_Out := 100.0;
ELSE
    rDieCooling_PWM_Zone05_Out := 0.0;
END_IF;

(* Zone 6 PWM Output *)
IF iPWM_CycleCounter_ms < REAL_TO_INT(rDieCooling_DutyCycle[6] * 10.0) THEN
    rDieCooling_PWM_Zone06_Out := 100.0;
ELSE
    rDieCooling_PWM_Zone06_Out := 0.0;
END_IF;

(* Zone 7 PWM Output *)
IF iPWM_CycleCounter_ms < REAL_TO_INT(rDieCooling_DutyCycle[7] * 10.0) THEN
    rDieCooling_PWM_Zone07_Out := 100.0;
ELSE
    rDieCooling_PWM_Zone07_Out := 0.0;
END_IF;

(* Zone 8 PWM Output *)
IF iPWM_CycleCounter_ms < REAL_TO_INT(rDieCooling_DutyCycle[8] * 10.0) THEN
    rDieCooling_PWM_Zone08_Out := 100.0;
ELSE
    rDieCooling_PWM_Zone08_Out := 0.0;
END_IF;

(* Zone 9 PWM Output *)
IF iPWM_CycleCounter_ms < REAL_TO_INT(rDieCooling_DutyCycle[9] * 10.0) THEN
    rDieCooling_PWM_Zone09_Out := 100.0;
ELSE
    rDieCooling_PWM_Zone09_Out := 0.0;
END_IF;

(* Zone 10 PWM Output *)
IF iPWM_CycleCounter_ms < REAL_TO_INT(rDieCooling_DutyCycle[10] * 10.0) THEN
    rDieCooling_PWM_Zone10_Out := 100.0;
ELSE
    rDieCooling_PWM_Zone10_Out := 0.0;
END_IF;

(* Zone 11 PWM Output *)
IF iPWM_CycleCounter_ms < REAL_TO_INT(rDieCooling_DutyCycle[11] * 10.0) THEN
    rDieCooling_PWM_Zone11_Out := 100.0;
ELSE
    rDieCooling_PWM_Zone11_Out := 0.0;
END_IF;

(* Zone 12 PWM Output *)
IF iPWM_CycleCounter_ms < REAL_TO_INT(rDieCooling_DutyCycle[12] * 10.0) THEN
    rDieCooling_PWM_Zone12_Out := 100.0;
ELSE
    rDieCooling_PWM_Zone12_Out := 0.0;
END_IF;
"""
