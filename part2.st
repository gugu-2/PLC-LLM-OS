(*
====================================================================================================
 PHASE 1: 4-CHANNEL 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSING ARCHITECTURE
====================================================================================================
 METALLURGICAL SAFETY INTEGRITY LEVEL (SIL-3 EQUIVALENT):
  In heavy 4-High hot strip roughing mills, catastrophic failures such as roll breakage, cylinder seal
  blowout, motor stall flashover, or descaling header burst carry massive economic and life-safety risks.
  To ensure absolute fault tolerance, 4 critical cyber-physical loops utilize 2oo3 Triple Modular
  Redundancy (TMR) with hardware-diverse or spatially isolated transducers:
    Channel 1: Total Rolling Force [kN] (3x Hermetically Sealed Load Cell Transducers)
    Channel 2: Main Hydraulic AGC Cylinder Pressure [bar] (3x High-Frequency Piezo Transmitters)
    Channel 3: Main Twin-Drive Motor Armature Current [kA] (3x Hall-Effect & Rogowski Sensors)
    Channel 4: High-Pressure Descaling Header Water Pressure [bar] (3x Piezoresistive Transmitters)

 DEGRADATION HIERARCHY & BUMPLESS FAILOVER MECHANICS:
  - Healthy State (3 valid sensors): Exact median value selection, eliminating sensor outliers.
  - Degraded State 1 (1 failed sensor / persistent 50 ms discrepancy): Bumpless 1oo2 average of remaining 2.
  - Degraded State 2 (2 failed sensors): Fallback to 1oo1 single operational transducer with high-priority warning.
  - Critical Failure State (All 3 sensors invalid): Immediate emergency roll gap opening, reversing table stop,
    and hardware interlock shutdown.
====================================================================================================
*)

(* --- CHANNEL 1: TOTAL ROLLING FORCE 2oo3 TMR EVALUATION --- *)
(* Sensor A validity and range verification [0.0 kN to 60000.0 kN] *)
IF (b_Force_Sensor_Healthy_A AND (r_Force_Sensor_Raw_A >= 0.0) AND (r_Force_Sensor_Raw_A <= 60000.0)) THEN
    b_TMR_Ch1_PairAB_Mismatch := (ABS(r_Force_Sensor_Raw_A - r_Force_Sensor_Raw_B) > r_TMR_Ch1_Tolerance_kN);
    b_TMR_Ch1_PairAC_Mismatch := (ABS(r_Force_Sensor_Raw_A - r_Force_Sensor_Raw_C) > r_TMR_Ch1_Tolerance_kN);
ELSE
    b_TMR_Ch1_PairAB_Mismatch := TRUE;
    b_TMR_Ch1_PairAC_Mismatch := TRUE;
END_IF;

(* Sensor B validity and range verification *)
IF (b_Force_Sensor_Healthy_B AND (r_Force_Sensor_Raw_B >= 0.0) AND (r_Force_Sensor_Raw_B <= 60000.0)) THEN
    b_TMR_Ch1_PairBC_Mismatch := (ABS(r_Force_Sensor_Raw_B - r_Force_Sensor_Raw_C) > r_TMR_Ch1_Tolerance_kN);
ELSE
    b_TMR_Ch1_PairAB_Mismatch := TRUE;
    b_TMR_Ch1_PairBC_Mismatch := TRUE;
END_IF;

(* Sensor C validity check *)
IF (NOT b_Force_Sensor_Healthy_C OR (r_Force_Sensor_Raw_C < 0.0) OR (r_Force_Sensor_Raw_C > 60000.0)) THEN
    b_TMR_Ch1_PairAC_Mismatch := TRUE;
    b_TMR_Ch1_PairBC_Mismatch := TRUE;
END_IF;

(* Channel 1 Persistence Debounce Timers (50.0 ms threshold at Ts = 0.5 ms) *)
IF b_TMR_Ch1_PairAB_Mismatch THEN
    r_TMR_Ch1_Timer_AB_ms := r_TMR_Ch1_Timer_AB_ms + r_Loop_Sample_Time_ms;
    IF (r_TMR_Ch1_Timer_AB_ms > 1000.0) THEN
        r_TMR_Ch1_Timer_AB_ms := 1000.0;
    END_IF;
ELSE
    r_TMR_Ch1_Timer_AB_ms := 0.0;
END_IF;

IF b_TMR_Ch1_PairBC_Mismatch THEN
    r_TMR_Ch1_Timer_BC_ms := r_TMR_Ch1_Timer_BC_ms + r_Loop_Sample_Time_ms;
    IF (r_TMR_Ch1_Timer_BC_ms > 1000.0) THEN
        r_TMR_Ch1_Timer_BC_ms := 1000.0;
    END_IF;
ELSE
    r_TMR_Ch1_Timer_BC_ms := 0.0;
END_IF;

IF b_TMR_Ch1_PairAC_Mismatch THEN
    r_TMR_Ch1_Timer_AC_ms := r_TMR_Ch1_Timer_AC_ms + r_Loop_Sample_Time_ms;
    IF (r_TMR_Ch1_Timer_AC_ms > 1000.0) THEN
        r_TMR_Ch1_Timer_AC_ms := 1000.0;
    END_IF;
ELSE
    r_TMR_Ch1_Timer_AC_ms := 0.0;
END_IF;

(* Channel 1 Voting State Machine and Degradation *)
IF (b_Force_Sensor_Healthy_A AND b_Force_Sensor_Healthy_B AND b_Force_Sensor_Healthy_C AND
    (r_TMR_Ch1_Timer_AB_ms < r_TMR_Persistence_Limit_ms) AND
    (r_TMR_Ch1_Timer_BC_ms < r_TMR_Persistence_Limit_ms) AND
    (r_TMR_Ch1_Timer_AC_ms < r_TMR_Persistence_Limit_ms)) THEN
    (* Full 2oo3 Median Selection *)
    ui_TMR_Ch1_Health_State := 3;
    IF ((r_Force_Sensor_Raw_A >= r_Force_Sensor_Raw_B AND r_Force_Sensor_Raw_A <= r_Force_Sensor_Raw_C) OR
        (r_Force_Sensor_Raw_A >= r_Force_Sensor_Raw_C AND r_Force_Sensor_Raw_A <= r_Force_Sensor_Raw_B)) THEN
        r_TMR_Ch1_Voted_Value := r_Force_Sensor_Raw_A;
    ELSIF ((r_Force_Sensor_Raw_B >= r_Force_Sensor_Raw_A AND r_Force_Sensor_Raw_B <= r_Force_Sensor_Raw_C) OR
           (r_Force_Sensor_Raw_B >= r_Force_Sensor_Raw_C AND r_Force_Sensor_Raw_B <= r_Force_Sensor_Raw_A)) THEN
        r_TMR_Ch1_Voted_Value := r_Force_Sensor_Raw_B;
    ELSE
        r_TMR_Ch1_Voted_Value := r_Force_Sensor_Raw_C;
    END_IF;
ELSIF (b_Force_Sensor_Healthy_A AND b_Force_Sensor_Healthy_B AND (r_TMR_Ch1_Timer_AB_ms < r_TMR_Persistence_Limit_ms)) THEN
    (* Degraded 1oo2: Sensors A & B healthy *)
    ui_TMR_Ch1_Health_State := 2;
    r_TMR_Ch1_Voted_Value := (r_Force_Sensor_Raw_A + r_Force_Sensor_Raw_B) * 0.5;
ELSIF (b_Force_Sensor_Healthy_B AND b_Force_Sensor_Healthy_C AND (r_TMR_Ch1_Timer_BC_ms < r_TMR_Persistence_Limit_ms)) THEN
    (* Degraded 1oo2: Sensors B & C healthy *)
    ui_TMR_Ch1_Health_State := 2;
    r_TMR_Ch1_Voted_Value := (r_Force_Sensor_Raw_B + r_Force_Sensor_Raw_C) * 0.5;
ELSIF (b_Force_Sensor_Healthy_A AND b_Force_Sensor_Healthy_C AND (r_TMR_Ch1_Timer_AC_ms < r_TMR_Persistence_Limit_ms)) THEN
    (* Degraded 1oo2: Sensors A & C healthy *)
    ui_TMR_Ch1_Health_State := 2;
    r_TMR_Ch1_Voted_Value := (r_Force_Sensor_Raw_A + r_Force_Sensor_Raw_C) * 0.5;
ELSIF b_Force_Sensor_Healthy_A THEN
    (* Degraded 1oo1: Only Sensor A healthy *)
    ui_TMR_Ch1_Health_State := 1;
    r_TMR_Ch1_Voted_Value := r_Force_Sensor_Raw_A;
ELSIF b_Force_Sensor_Healthy_B THEN
    (* Degraded 1oo1: Only Sensor B healthy *)
    ui_TMR_Ch1_Health_State := 1;
    r_TMR_Ch1_Voted_Value := r_Force_Sensor_Raw_B;
ELSIF b_Force_Sensor_Healthy_C THEN
    (* Degraded 1oo1: Only Sensor C healthy *)
    ui_TMR_Ch1_Health_State := 1;
    r_TMR_Ch1_Voted_Value := r_Force_Sensor_Raw_C;
ELSE
    (* Complete Channel Failure *)
    ui_TMR_Ch1_Health_State := 0;
    r_TMR_Ch1_Voted_Value := 0.0;
    b_TMR_Critical_Trip_Active := TRUE;
    b_Emergency_Gap_Open_Active := TRUE;
END_IF;
r_Voted_Rolling_Force := r_TMR_Ch1_Voted_Value;

(* --- CHANNEL 2: MAIN HYDRAULIC AGC PRESSURE 2oo3 TMR EVALUATION --- *)
(* Sensor A validity and range verification [0.0 bar to 350.0 bar] *)
IF (b_Press_AGC_Healthy_A AND (r_Press_AGC_Raw_A >= 0.0) AND (r_Press_AGC_Raw_A <= 350.0)) THEN
    b_TMR_Ch2_PairAB_Mismatch := (ABS(r_Press_AGC_Raw_A - r_Press_AGC_Raw_B) > r_TMR_Ch2_Tolerance_bar);
    b_TMR_Ch2_PairAC_Mismatch := (ABS(r_Press_AGC_Raw_A - r_Press_AGC_Raw_C) > r_TMR_Ch2_Tolerance_bar);
ELSE
    b_TMR_Ch2_PairAB_Mismatch := TRUE;
    b_TMR_Ch2_PairAC_Mismatch := TRUE;
END_IF;

(* Sensor B validity and range verification *)
IF (b_Press_AGC_Healthy_B AND (r_Press_AGC_Raw_B >= 0.0) AND (r_Press_AGC_Raw_B <= 350.0)) THEN
    b_TMR_Ch2_PairBC_Mismatch := (ABS(r_Press_AGC_Raw_B - r_Press_AGC_Raw_C) > r_TMR_Ch2_Tolerance_bar);
ELSE
    b_TMR_Ch2_PairAB_Mismatch := TRUE;
    b_TMR_Ch2_PairBC_Mismatch := TRUE;
END_IF;

(* Sensor C validity check *)
IF (NOT b_Press_AGC_Healthy_C OR (r_Press_AGC_Raw_C < 0.0) OR (r_Press_AGC_Raw_C > 350.0)) THEN
    b_TMR_Ch2_PairAC_Mismatch := TRUE;
    b_TMR_Ch2_PairBC_Mismatch := TRUE;
END_IF;

(* Channel 2 Persistence Debounce Timers *)
IF b_TMR_Ch2_PairAB_Mismatch THEN
    r_TMR_Ch2_Timer_AB_ms := r_TMR_Ch2_Timer_AB_ms + r_Loop_Sample_Time_ms;
    IF (r_TMR_Ch2_Timer_AB_ms > 1000.0) THEN
        r_TMR_Ch2_Timer_AB_ms := 1000.0;
    END_IF;
ELSE
    r_TMR_Ch2_Timer_AB_ms := 0.0;
END_IF;

IF b_TMR_Ch2_PairBC_Mismatch THEN
    r_TMR_Ch2_Timer_BC_ms := r_TMR_Ch2_Timer_BC_ms + r_Loop_Sample_Time_ms;
    IF (r_TMR_Ch2_Timer_BC_ms > 1000.0) THEN
        r_TMR_Ch2_Timer_BC_ms := 1000.0;
    END_IF;
ELSE
    r_TMR_Ch2_Timer_BC_ms := 0.0;
END_IF;

IF b_TMR_Ch2_PairAC_Mismatch THEN
    r_TMR_Ch2_Timer_AC_ms := r_TMR_Ch2_Timer_AC_ms + r_Loop_Sample_Time_ms;
    IF (r_TMR_Ch2_Timer_AC_ms > 1000.0) THEN
        r_TMR_Ch2_Timer_AC_ms := 1000.0;
    END_IF;
ELSE
    r_TMR_Ch2_Timer_AC_ms := 0.0;
END_IF;

(* Channel 2 Voting Logic *)
IF (b_Press_AGC_Healthy_A AND b_Press_AGC_Healthy_B AND b_Press_AGC_Healthy_C AND
    (r_TMR_Ch2_Timer_AB_ms < r_TMR_Persistence_Limit_ms) AND
    (r_TMR_Ch2_Timer_BC_ms < r_TMR_Persistence_Limit_ms) AND
    (r_TMR_Ch2_Timer_AC_ms < r_TMR_Persistence_Limit_ms)) THEN
    ui_TMR_Ch2_Health_State := 3;
    IF ((r_Press_AGC_Raw_A >= r_Press_AGC_Raw_B AND r_Press_AGC_Raw_A <= r_Press_AGC_Raw_C) OR
        (r_Press_AGC_Raw_A >= r_Press_AGC_Raw_C AND r_Press_AGC_Raw_A <= r_Press_AGC_Raw_B)) THEN
        r_TMR_Ch2_Voted_Value := r_Press_AGC_Raw_A;
    ELSIF ((r_Press_AGC_Raw_B >= r_Press_AGC_Raw_A AND r_Press_AGC_Raw_B <= r_Press_AGC_Raw_C) OR
           (r_Press_AGC_Raw_B >= r_Press_AGC_Raw_C AND r_Press_AGC_Raw_B <= r_Press_AGC_Raw_A)) THEN
        r_TMR_Ch2_Voted_Value := r_Press_AGC_Raw_B;
    ELSE
        r_TMR_Ch2_Voted_Value := r_Press_AGC_Raw_C;
    END_IF;
ELSIF (b_Press_AGC_Healthy_A AND b_Press_AGC_Healthy_B AND (r_TMR_Ch2_Timer_AB_ms < r_TMR_Persistence_Limit_ms)) THEN
    ui_TMR_Ch2_Health_State := 2;
    r_TMR_Ch2_Voted_Value := (r_Press_AGC_Raw_A + r_Press_AGC_Raw_B) * 0.5;
ELSIF (b_Press_AGC_Healthy_B AND b_Press_AGC_Healthy_C AND (r_TMR_Ch2_Timer_BC_ms < r_TMR_Persistence_Limit_ms)) THEN
    ui_TMR_Ch2_Health_State := 2;
    r_TMR_Ch2_Voted_Value := (r_Press_AGC_Raw_B + r_Press_AGC_Raw_C) * 0.5;
ELSIF (b_Press_AGC_Healthy_A AND b_Press_AGC_Healthy_C AND (r_TMR_Ch2_Timer_AC_ms < r_TMR_Persistence_Limit_ms)) THEN
    ui_TMR_Ch2_Health_State := 2;
    r_TMR_Ch2_Voted_Value := (r_Press_AGC_Raw_A + r_Press_AGC_Raw_C) * 0.5;
ELSIF b_Press_AGC_Healthy_A THEN
    ui_TMR_Ch2_Health_State := 1;
    r_TMR_Ch2_Voted_Value := r_Press_AGC_Raw_A;
ELSIF b_Press_AGC_Healthy_B THEN
    ui_TMR_Ch2_Health_State := 1;
    r_TMR_Ch2_Voted_Value := r_Press_AGC_Raw_B;
ELSIF b_Press_AGC_Healthy_C THEN
    ui_TMR_Ch2_Health_State := 1;
    r_TMR_Ch2_Voted_Value := r_Press_AGC_Raw_C;
ELSE
    ui_TMR_Ch2_Health_State := 0;
    r_TMR_Ch2_Voted_Value := 0.0;
    b_TMR_Critical_Trip_Active := TRUE;
    b_Emergency_Gap_Open_Active := TRUE;
END_IF;
r_Voted_Hydraulic_AGC_Pressure := r_TMR_Ch2_Voted_Value;

(* --- CHANNEL 3: MAIN MOTOR ARMATURE CURRENT 2oo3 TMR EVALUATION --- *)
(* Sensor A validity and range verification [0.0 kA to 6.0 kA] *)
IF (b_Curr_Motor_Healthy_A AND (r_Curr_Motor_Raw_A >= 0.0) AND (r_Curr_Motor_Raw_A <= 6.0)) THEN
    b_TMR_Ch3_PairAB_Mismatch := (ABS(r_Curr_Motor_Raw_A - r_Curr_Motor_Raw_B) > r_TMR_Ch3_Tolerance_kA);
    b_TMR_Ch3_PairAC_Mismatch := (ABS(r_Curr_Motor_Raw_A - r_Curr_Motor_Raw_C) > r_TMR_Ch3_Tolerance_kA);
ELSE
    b_TMR_Ch3_PairAB_Mismatch := TRUE;
    b_TMR_Ch3_PairAC_Mismatch := TRUE;
END_IF;

(* Sensor B validity and range verification *)
IF (b_Curr_Motor_Healthy_B AND (r_Curr_Motor_Raw_B >= 0.0) AND (r_Curr_Motor_Raw_B <= 6.0)) THEN
    b_TMR_Ch3_PairBC_Mismatch := (ABS(r_Curr_Motor_Raw_B - r_Curr_Motor_Raw_C) > r_TMR_Ch3_Tolerance_kA);
ELSE
    b_TMR_Ch3_PairAB_Mismatch := TRUE;
    b_TMR_Ch3_PairBC_Mismatch := TRUE;
END_IF;

(* Sensor C validity check *)
IF (NOT b_Curr_Motor_Healthy_C OR (r_Curr_Motor_Raw_C < 0.0) OR (r_Curr_Motor_Raw_C > 6.0)) THEN
    b_TMR_Ch3_PairAC_Mismatch := TRUE;
    b_TMR_Ch3_PairBC_Mismatch := TRUE;
END_IF;

(* Channel 3 Persistence Debounce Timers *)
IF b_TMR_Ch3_PairAB_Mismatch THEN
    r_TMR_Ch3_Timer_AB_ms := r_TMR_Ch3_Timer_AB_ms + r_Loop_Sample_Time_ms;
    IF (r_TMR_Ch3_Timer_AB_ms > 1000.0) THEN
        r_TMR_Ch3_Timer_AB_ms := 1000.0;
    END_IF;
ELSE
    r_TMR_Ch3_Timer_AB_ms := 0.0;
END_IF;

IF b_TMR_Ch3_PairBC_Mismatch THEN
    r_TMR_Ch3_Timer_BC_ms := r_TMR_Ch3_Timer_BC_ms + r_Loop_Sample_Time_ms;
    IF (r_TMR_Ch3_Timer_BC_ms > 1000.0) THEN
        r_TMR_Ch3_Timer_BC_ms := 1000.0;
    END_IF;
ELSE
    r_TMR_Ch3_Timer_BC_ms := 0.0;
END_IF;

IF b_TMR_Ch3_PairAC_Mismatch THEN
    r_TMR_Ch3_Timer_AC_ms := r_TMR_Ch3_Timer_AC_ms + r_Loop_Sample_Time_ms;
    IF (r_TMR_Ch3_Timer_AC_ms > 1000.0) THEN
        r_TMR_Ch3_Timer_AC_ms := 1000.0;
    END_IF;
ELSE
    r_TMR_Ch3_Timer_AC_ms := 0.0;
END_IF;

(* Channel 3 Voting Logic *)
IF (b_Curr_Motor_Healthy_A AND b_Curr_Motor_Healthy_B AND b_Curr_Motor_Healthy_C AND
    (r_TMR_Ch3_Timer_AB_ms < r_TMR_Persistence_Limit_ms) AND
    (r_TMR_Ch3_Timer_BC_ms < r_TMR_Persistence_Limit_ms) AND
    (r_TMR_Ch3_Timer_AC_ms < r_TMR_Persistence_Limit_ms)) THEN
    ui_TMR_Ch3_Health_State := 3;
    IF ((r_Curr_Motor_Raw_A >= r_Curr_Motor_Raw_B AND r_Curr_Motor_Raw_A <= r_Curr_Motor_Raw_C) OR
        (r_Curr_Motor_Raw_A >= r_Curr_Motor_Raw_C AND r_Curr_Motor_Raw_A <= r_Curr_Motor_Raw_B)) THEN
        r_TMR_Ch3_Voted_Value := r_Curr_Motor_Raw_A;
    ELSIF ((r_Curr_Motor_Raw_B >= r_Curr_Motor_Raw_A AND r_Curr_Motor_Raw_B <= r_Curr_Motor_Raw_C) OR
           (r_Curr_Motor_Raw_B >= r_Curr_Motor_Raw_C AND r_Curr_Motor_Raw_B <= r_Curr_Motor_Raw_A)) THEN
        r_TMR_Ch3_Voted_Value := r_Curr_Motor_Raw_B;
    ELSE
        r_TMR_Ch3_Voted_Value := r_Curr_Motor_Raw_C;
    END_IF;
ELSIF (b_Curr_Motor_Healthy_A AND b_Curr_Motor_Healthy_B AND (r_TMR_Ch3_Timer_AB_ms < r_TMR_Persistence_Limit_ms)) THEN
    ui_TMR_Ch3_Health_State := 2;
    r_TMR_Ch3_Voted_Value := (r_Curr_Motor_Raw_A + r_Curr_Motor_Raw_B) * 0.5;
ELSIF (b_Curr_Motor_Healthy_B AND b_Curr_Motor_Healthy_C AND (r_TMR_Ch3_Timer_BC_ms < r_TMR_Persistence_Limit_ms)) THEN
    ui_TMR_Ch3_Health_State := 2;
    r_TMR_Ch3_Voted_Value := (r_Curr_Motor_Raw_B + r_Curr_Motor_Raw_C) * 0.5;
ELSIF (b_Curr_Motor_Healthy_A AND b_Curr_Motor_Healthy_C AND (r_TMR_Ch3_Timer_AC_ms < r_TMR_Persistence_Limit_ms)) THEN
    ui_TMR_Ch3_Health_State := 2;
    r_TMR_Ch3_Voted_Value := (r_Curr_Motor_Raw_A + r_Curr_Motor_Raw_C) * 0.5;
ELSIF b_Curr_Motor_Healthy_A THEN
    ui_TMR_Ch3_Health_State := 1;
    r_TMR_Ch3_Voted_Value := r_Curr_Motor_Raw_A;
ELSIF b_Curr_Motor_Healthy_B THEN
    ui_TMR_Ch3_Health_State := 1;
    r_TMR_Ch3_Voted_Value := r_Curr_Motor_Raw_B;
ELSIF b_Curr_Motor_Healthy_C THEN
    ui_TMR_Ch3_Health_State := 1;
    r_TMR_Ch3_Voted_Value := r_Curr_Motor_Raw_C;
ELSE
    ui_TMR_Ch3_Health_State := 0;
    r_TMR_Ch3_Voted_Value := 0.0;
    b_TMR_Critical_Trip_Active := TRUE;
    b_Emergency_Gap_Open_Active := TRUE;
END_IF;
r_Voted_Mill_Armature_Current := r_TMR_Ch3_Voted_Value;

(* --- CHANNEL 4: HIGH-PRESSURE DESCALING WATER PRESSURE 2oo3 TMR EVALUATION --- *)
(* Sensor A validity and range verification [0.0 bar to 350.0 bar] *)
IF (b_Press_Desc_Healthy_A AND (r_Press_Desc_Raw_A >= 0.0) AND (r_Press_Desc_Raw_A <= 350.0)) THEN
    b_TMR_Ch4_PairAB_Mismatch := (ABS(r_Press_Desc_Raw_A - r_Press_Desc_Raw_B) > r_TMR_Ch4_Tolerance_bar);
    b_TMR_Ch4_PairAC_Mismatch := (ABS(r_Press_Desc_Raw_A - r_Press_Desc_Raw_C) > r_TMR_Ch4_Tolerance_bar);
ELSE
    b_TMR_Ch4_PairAB_Mismatch := TRUE;
    b_TMR_Ch4_PairAC_Mismatch := TRUE;
END_IF;

(* Sensor B validity and range verification *)
IF (b_Press_Desc_Healthy_B AND (r_Press_Desc_Raw_B >= 0.0) AND (r_Press_Desc_Raw_B <= 350.0)) THEN
    b_TMR_Ch4_PairBC_Mismatch := (ABS(r_Press_Desc_Raw_B - r_Press_Desc_Raw_C) > r_TMR_Ch4_Tolerance_bar);
ELSE
    b_TMR_Ch4_PairAB_Mismatch := TRUE;
    b_TMR_Ch4_PairBC_Mismatch := TRUE;
END_IF;

(* Sensor C validity check *)
IF (NOT b_Press_Desc_Healthy_C OR (r_Press_Desc_Raw_C < 0.0) OR (r_Press_Desc_Raw_C > 350.0)) THEN
    b_TMR_Ch4_PairAC_Mismatch := TRUE;
    b_TMR_Ch4_PairBC_Mismatch := TRUE;
END_IF;

(* Channel 4 Persistence Debounce Timers *)
IF b_TMR_Ch4_PairAB_Mismatch THEN
    r_TMR_Ch4_Timer_AB_ms := r_TMR_Ch4_Timer_AB_ms + r_Loop_Sample_Time_ms;
    IF (r_TMR_Ch4_Timer_AB_ms > 1000.0) THEN
        r_TMR_Ch4_Timer_AB_ms := 1000.0;
    END_IF;
ELSE
    r_TMR_Ch4_Timer_AB_ms := 0.0;
END_IF;

IF b_TMR_Ch4_PairBC_Mismatch THEN
    r_TMR_Ch4_Timer_BC_ms := r_TMR_Ch4_Timer_BC_ms + r_Loop_Sample_Time_ms;
    IF (r_TMR_Ch4_Timer_BC_ms > 1000.0) THEN
        r_TMR_Ch4_Timer_BC_ms := 1000.0;
    END_IF;
ELSE
    r_TMR_Ch4_Timer_BC_ms := 0.0;
END_IF;

IF b_TMR_Ch4_PairAC_Mismatch THEN
    r_TMR_Ch4_Timer_AC_ms := r_TMR_Ch4_Timer_AC_ms + r_Loop_Sample_Time_ms;
    IF (r_TMR_Ch4_Timer_AC_ms > 1000.0) THEN
        r_TMR_Ch4_Timer_AC_ms := 1000.0;
    END_IF;
ELSE
    r_TMR_Ch4_Timer_AC_ms := 0.0;
END_IF;

(* Channel 4 Voting Logic *)
IF (b_Press_Desc_Healthy_A AND b_Press_Desc_Healthy_B AND b_Press_Desc_Healthy_C AND
    (r_TMR_Ch4_Timer_AB_ms < r_TMR_Persistence_Limit_ms) AND
    (r_TMR_Ch4_Timer_BC_ms < r_TMR_Persistence_Limit_ms) AND
    (r_TMR_Ch4_Timer_AC_ms < r_TMR_Persistence_Limit_ms)) THEN
    ui_TMR_Ch4_Health_State := 3;
    IF ((r_Press_Desc_Raw_A >= r_Press_Desc_Raw_B AND r_Press_Desc_Raw_A <= r_Press_Desc_Raw_C) OR
        (r_Press_Desc_Raw_A >= r_Press_Desc_Raw_C AND r_Press_Desc_Raw_A <= r_Press_Desc_Raw_B)) THEN
        r_TMR_Ch4_Voted_Value := r_Press_Desc_Raw_A;
    ELSIF ((r_Press_Desc_Raw_B >= r_Press_Desc_Raw_A AND r_Press_Desc_Raw_B <= r_Press_Desc_Raw_C) OR
           (r_Press_Desc_Raw_B >= r_Press_Desc_Raw_C AND r_Press_Desc_Raw_B <= r_Press_Desc_Raw_A)) THEN
        r_TMR_Ch4_Voted_Value := r_Press_Desc_Raw_B;
    ELSE
        r_TMR_Ch4_Voted_Value := r_Press_Desc_Raw_C;
    END_IF;
ELSIF (b_Press_Desc_Healthy_A AND b_Press_Desc_Healthy_B AND (r_TMR_Ch4_Timer_AB_ms < r_TMR_Persistence_Limit_ms)) THEN
    ui_TMR_Ch4_Health_State := 2;
    r_TMR_Ch4_Voted_Value := (r_Press_Desc_Raw_A + r_Press_Desc_Raw_B) * 0.5;
ELSIF (b_Press_Desc_Healthy_B AND b_Press_Desc_Healthy_C AND (r_TMR_Ch4_Timer_BC_ms < r_TMR_Persistence_Limit_ms)) THEN
    ui_TMR_Ch4_Health_State := 2;
    r_TMR_Ch4_Voted_Value := (r_Press_Desc_Raw_B + r_Press_Desc_Raw_C) * 0.5;
ELSIF (b_Press_Desc_Healthy_A AND b_Press_Desc_Healthy_C AND (r_TMR_Ch4_Timer_AC_ms < r_TMR_Persistence_Limit_ms)) THEN
    ui_TMR_Ch4_Health_State := 2;
    r_TMR_Ch4_Voted_Value := (r_Press_Desc_Raw_A + r_Press_Desc_Raw_C) * 0.5;
ELSIF b_Press_Desc_Healthy_A THEN
    ui_TMR_Ch4_Health_State := 1;
    r_TMR_Ch4_Voted_Value := r_Press_Desc_Raw_A;
ELSIF b_Press_Desc_Healthy_B THEN
    ui_TMR_Ch4_Health_State := 1;
    r_TMR_Ch4_Voted_Value := r_Press_Desc_Raw_B;
ELSIF b_Press_Desc_Healthy_C THEN
    ui_TMR_Ch4_Health_State := 1;
    r_TMR_Ch4_Voted_Value := r_Press_Desc_Raw_C;
ELSE
    ui_TMR_Ch4_Health_State := 0;
    r_TMR_Ch4_Voted_Value := 0.0;
    b_TMR_Critical_Trip_Active := TRUE;
END_IF;
r_Voted_Descaling_Water_Pressure := r_TMR_Ch4_Voted_Value;

(* Consolidated TMR Degradation Alarm Flag *)
b_TMR_Channel_Degraded_Alarm := (ui_TMR_Ch1_Health_State < 3) OR
                                (ui_TMR_Ch2_Health_State < 3) OR
                                (ui_TMR_Ch3_Health_State < 3) OR
                                (ui_TMR_Ch4_Health_State < 3);
