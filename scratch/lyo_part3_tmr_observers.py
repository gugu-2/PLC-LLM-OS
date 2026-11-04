# Module 3: Phase 1 (Init), Phase 2 (2oo3 TMR Voting), Phase 3 (Cyber-Physical Observers)
def get_part3():
    return '''(* ==========================================================================================
 * PHASE 1: COLD INITIALIZATION, WATCHDOG CHECKS & SUPERVISORY PERMISSIVES
 * ========================================================================================== *)
(* Scan cycle delta time sanity bounding [0.005 s to 0.100 s] *)
IF rDeltaTime_s <= 0.005 THEN
    rDeltaTime_s := 0.020; (* Default to standard 20 ms industrial cyclic task *)
ELSIF rDeltaTime_s >= 0.100 THEN
    rDeltaTime_s := 0.100; (* Clamp maximum execution step to prevent numeric instability *)
END_IF;

(* First-Scan Cold Initialization of Model Matrices, Observers, PID and Baselines *)
IF NOT bInitialized THEN
    (* 1. Initialize Discrete State Transition Matrix matA (8x8) for Ts = 0.020 s *)
    (* x1: T_oil_sup [deg C] *)
    matA[1,1] := 0.9880; matA[1,2] := 0.0090; matA[1,3] := 0.0000; matA[1,4] := 0.0000;
    matA[1,5] := 0.0000; matA[1,6] := 0.0015; matA[1,7] := 0.0000; matA[1,8] := 0.0000;
    (* x2: T_oil_ret [deg C] *)
    matA[2,1] := 0.0120; matA[2,2] := 0.9810; matA[2,3] := 0.0000; matA[2,4] := 0.0000;
    matA[2,5] := -0.0035; matA[2,6] := 0.0085; matA[2,7] := 0.0000; matA[2,8] := 0.0000;
    (* x3: h_ice_cond [mm] *)
    matA[3,1] := 0.0000; matA[3,2] := 0.0000; matA[3,3] := 0.9998; matA[3,4] := 0.0000;
    matA[3,5] := 0.0042; matA[3,6] := 0.0000; matA[3,7] := 0.0000; matA[3,8] := 0.0000;
    (* x4: P_diff_cp [mbar] *)
    matA[4,1] := 0.0000; matA[4,2] := 0.0000; matA[4,3] := 0.0000; matA[4,4] := 0.9850;
    matA[4,5] := 0.0180; matA[4,6] := 0.0005; matA[4,7] := -0.0002; matA[4,8] := 0.0000;
    (* x5: v_sub_front [mm/h] *)
    matA[5,1] := 0.0010; matA[5,2] := 0.0000; matA[5,3] := 0.0000; matA[5,4] := 0.0085;
    matA[5,5] := 0.9760; matA[5,6] := 0.0065; matA[5,7] := 0.0000; matA[5,8] := 0.0000;
    (* x6: T_prod_core [deg C] *)
    matA[6,1] := 0.0075; matA[6,2] := 0.0020; matA[6,3] := 0.0000; matA[6,4] := 0.0000;
    matA[6,5] := -0.0125; matA[6,6] := 0.9890; matA[6,7] := 0.0000; matA[6,8] := 0.0000;
    (* x7: m_dot_n2 [sccm] *)
    matA[7,1] := 0.0000; matA[7,2] := 0.0000; matA[7,3] := 0.0000; matA[7,4] := -0.0050;
    matA[7,5] := 0.0000; matA[7,6] := 0.0000; matA[7,7] := 0.9500; matA[7,8] := 0.0000;
    (* x8: P_hyd_ram [bar] *)
    matA[8,1] := 0.0000; matA[8,2] := 0.0000; matA[8,3] := 0.0000; matA[8,4] := 0.0000;
    matA[8,5] := 0.0000; matA[8,6] := 0.0000; matA[8,7] := 0.0000; matA[8,8] := 0.9800;

    (* 2. Initialize Discrete Input Coupling Matrix matB (8x6) *)
    (* Inputs: u1=Thermal net, u2=N2 bleed, u3=Vac throttle, u4=Refrig comp, u5=Hot gas defrost, u6=Hyd pressure *)
    matB[1,1] :=  0.0350; matB[1,2] :=  0.0000; matB[1,3] :=  0.0000; matB[1,4] :=  0.0000; matB[1,5] :=  0.0000; matB[1,6] :=  0.0000;
    matB[2,1] :=  0.0180; matB[2,2] :=  0.0000; matB[2,3] :=  0.0000; matB[2,4] :=  0.0000; matB[2,5] :=  0.0000; matB[2,6] :=  0.0000;
    matB[3,1] :=  0.0000; matB[3,2] :=  0.0000; matB[3,3] :=  0.0000; matB[3,4] :=  0.0005; matB[3,5] := -0.0080; matB[3,6] :=  0.0000;
    matB[4,1] :=  0.0002; matB[4,2] := -0.0015; matB[4,3] :=  0.0008; matB[4,4] := -0.0004; matB[4,5] :=  0.0000; matB[4,6] :=  0.0000;
    matB[5,1] :=  0.0012; matB[5,2] :=  0.0005; matB[5,3] := -0.0003; matB[5,4] :=  0.0000; matB[5,5] :=  0.0000; matB[5,6] :=  0.0000;
    matB[6,1] :=  0.0008; matB[6,2] :=  0.0001; matB[6,3] := -0.0002; matB[6,4] :=  0.0000; matB[6,5] :=  0.0000; matB[6,6] :=  0.0000;
    matB[7,1] :=  0.0000; matB[7,2] :=  0.4500; matB[7,3] := -0.0500; matB[7,4] :=  0.0000; matB[7,5] :=  0.0000; matB[7,6] :=  0.0000;
    matB[8,1] :=  0.0000; matB[8,2] :=  0.0000; matB[8,3] :=  0.0000; matB[8,4] :=  0.0000; matB[8,5] :=  0.0000; matB[8,6] :=  0.8500;

    (* 3. Initialize Measurement Matrix matC (8x8) and Feedthrough matD (8x6) *)
    FOR iLoopI := 1 TO 8 DO
        FOR iLoopJ := 1 TO 8 DO
            IF iLoopI = iLoopJ THEN
                matC[iLoopI, iLoopJ] := 1.0;
            ELSE
                matC[iLoopI, iLoopJ] := 0.0;
            END_IF;
        END_FOR;
        FOR iLoopK := 1 TO 6 DO
            matD[iLoopI, iLoopK] := 0.0;
        END_FOR;
    END_FOR;

    (* 4. Initialize Model Predictive Control (MPC) Penalty Matrices Q (8x8), R (6x6), P (8x8) *)
    FOR iLoopI := 1 TO 8 DO
        FOR iLoopJ := 1 TO 8 DO
            matQ[iLoopI, iLoopJ] := 0.0;
            matP[iLoopI, iLoopJ] := 0.0;
        END_FOR;
    END_FOR;
    (* Diagonal State Tracking Error Penalties *)
    matQ[1,1] :=  8.5;  (* Silicone oil supply temperature tracking penalty *)
    matQ[2,2] :=  4.0;  (* Silicone oil return temperature penalty *)
    matQ[3,3] :=  1.5;  (* Condenser ice layer accumulation penalty *)
    matQ[4,4] := 25.0;  (* Comparative pressure differential penalty *)
    matQ[5,5] := 10.0;  (* Sublimation front velocity stability penalty *)
    matQ[6,6] := 50.0;  (* Product vial core temperature overshoot penalty (CRITICAL TO AVOID MELT COLLAPSE) *)
    matQ[7,7] :=  0.8;  (* Nitrogen mass flow stability penalty *)
    matQ[8,8] := 12.0;  (* Hydraulic stoppering ram pressure penalty *)

    (* Terminal Lyapunov Cost Matrix P = 2.5 * Q *)
    FOR iLoopI := 1 TO 8 DO
        matP[iLoopI, iLoopI] := matQ[iLoopI, iLoopI] * 2.5;
    END_FOR;

    (* Actuation Effort Penalty Matrix R (6x6) *)
    FOR iLoopI := 1 TO 6 DO
        FOR iLoopJ := 1 TO 6 DO
            matR[iLoopI, iLoopJ] := 0.0;
        END_FOR;
    END_FOR;
    matR[1,1] := 0.20;  (* Shelf heating/cooling thermal slew penalty *)
    matR[2,2] := 0.65;  (* Sterile N2 micro-bleed throttling cost penalty *)
    matR[3,3] := 0.15;  (* Vacuum butterfly valve modulation penalty *)
    matR[4,4] := 0.40;  (* Refrigeration compressor power penalty *)
    matR[5,5] := 0.50;  (* Hot gas bypass defrost duty penalty *)
    matR[6,6] := 0.35;  (* Hydraulic proportional relief throttling penalty *)

    (* Actuator Hard Saturation Constraints *)
    u_min[1] := -100.0; u_max[1] := 100.0; (* Thermal fluid duty [%] *)
    u_min[2] :=    0.0; u_max[2] := 100.0; (* N2 bleed valve [%] *)
    u_min[3] :=    0.0; u_max[3] := 100.0; (* Vacuum butterfly [%] *)
    u_min[4] :=    0.0; u_max[4] := 100.0; (* Refrig compressor capacity [%] *)
    u_min[5] :=    0.0; u_max[5] := 100.0; (* Defrost valve [%] *)
    u_min[6] :=    0.0; u_max[6] := 100.0; (* Hydraulic relief valve [%] *)

    (* 5. Initialize Luenberger / Kalman Observer Correction Gains *)
    rKalmanGain[1] := 0.15;
    rKalmanGain[2] := 0.12;
    rKalmanGain[3] := 0.05;
    rKalmanGain[4] := 0.22;
    rKalmanGain[5] := 0.18;
    rKalmanGain[6] := 0.25;
    rKalmanGain[7] := 0.10;
    rKalmanGain[8] := 0.20;

    (* 6. Initialize Pikal Sublimation Kinetics Physical Constants *)
    rPikal_CakeResistance_R0        := 1.250;   (* Base cake membrane resistance [cm2*h*mbar/g] *)
    rPikal_CakeResistance_A1        := 16.50;   (* Linear resistance increase coefficient *)
    rPikal_CakeResistance_A2        := 0.120;   (* Non-linear curvature coefficient *)
    rPikal_VialHeatTransferCoeff_Kv := 0.00042; (* Vial heat transfer Kv [cal/(s*cm2*K)] *)
    rPikal_LatentHeatSublimation_kJ := 2835.0;  (* Latent heat of sublimation of pure ice [kJ/kg] *)
    rPikal_TotalIceMass_kg          := 360.0;   (* Total ice inventory in 40 m2 chamber batch [kg] *)
    rPikal_CumulativeSublimated_kg  := 0.0;
    rPikal_CakeDryThickness_mm      := 0.0;

    (* 7. Initialize Comparative Pressure & MTM Parameters *)
    rComp_RawRatio           := 1.0;
    rComp_FilteredRatio      := 1.0;
    rComp_RatioSlope_per_s   := 0.0;
    rComp_RatioFilterCoeff   := 0.05; (* Alpha for EMA filtering *)
    tComp_ConvergenceTimer_s := 0.0;
    bComp_EndpointMet        := FALSE;
    bMTM_Active              := FALSE;
    tMTM_Timer_s             := 0.0;
    rMTM_Interval_Timer_s    := 0.0;

    (* 8. Initialize Steam-in-Place (SIP) Parameters *)
    rSIP_BaseTemp_degC       := 121.11; (* Reference sterilization datum [deg C] *)
    rSIP_Z_Value_degC        := 10.00;  (* Inactivation Z-value [deg C] *)
    rSIP_AccumulatedF0_min   := 0.0;
    bSIP_SterilizationValid  := FALSE;

    (* 9. Initialize Hydraulic Stoppering Mechanics *)
    rHyd_PistonArea_cm2      := 380.13; (* Effective bore area of hydraulic ram cylinder [cm2] *)
    rHyd_CalculatedForce_kN  := 0.0;
    rHyd_CalculatedTonnage_ton := 0.0;
    rHyd_CompactionStrain_pct:= 0.0;
    tHyd_TonnageHoldTimer_s  := 0.0;
    bHyd_TargetTonnageReached:= FALSE;

    (* 10. Initialize Condenser Ice Parameters *)
    rCond_IceDensity_kg_m3   := 917.0;  (* Crystalline ice density [kg/m3] *)
    rCond_SurfaceArea_m2     := 80.0;   (* Condenser internal tube coil surface area [m2] *)
    rCond_IceMass_kg         := 0.0;
    rCond_IceThickness_mm    := 0.0;

    (* 11. Initialize PID Controller Parameters *)
    rPID_Shelf_Kp            := 2.80;
    rPID_Shelf_Ki            := 0.045;
    rPID_Shelf_Kd            := 4.20;
    rPID_Shelf_Integral      := 0.0;
    rPID_Shelf_PrevError     := 0.0;

    rPID_Vac_Kp              := 185.0;
    rPID_Vac_Ki              := 12.5;
    rPID_Vac_Kd              := 15.0;
    rPID_Vac_Integral        := 0.0;
    rPID_Vac_PrevError       := 0.0;

    (* 12. Initialize ISA-18.2 Alarm Trip Thresholds *)
    rAlarm_VacLoss_HH_Trip   := 0.400;  (* Primary drying high-high vacuum loss trip [mbar] *)
    rAlarm_VacLoss_H_Trip    := 0.250;  (* Primary drying high vacuum warning [mbar] *)
    rAlarm_Vac_Deadband      := 0.020;  (* Vacuum deadband [mbar] *)
    rAlarm_Product_HH_Trip   := -30.0;  (* Product eutectic collapse trip [deg C] *)
    rAlarm_Product_H_Trip    := -33.0;  (* Product warning high [deg C] *)
    rAlarm_Product_Deadband  := 1.0;    (* Product deadband [deg C] *)
    rAlarm_CondTemp_HH_Trip  := -45.0;  (* Condenser overheat trip [deg C] *)
    rAlarm_CondTemp_H_Trip   := -60.0;  (* Condenser warning high [deg C] *)
    rAlarm_CondTemp_Deadband := 2.0;    (* Condenser deadband [deg C] *)
    rAlarm_ShelfSpread_H_Trip:= 1.2;    (* Shelf thermal spread warning [deg C] *)
    rAlarm_ShelfSpread_Deadband := 0.2; (* Shelf spread deadband [deg C] *)
    rAlarm_HydPress_HH_Trip  := 235.0;  (* Hydraulic overpressure slam trip [bar] *)
    rAlarm_HydPress_H_Trip   := 210.0;  (* Hydraulic high warning [bar] *)
    rAlarm_HydPress_Deadband := 5.0;    (* Hydraulic deadband [bar] *)
    rAlarm_SIP_Temp_LL_Trip  := 120.0;  (* Pure steam under-temperature trip [deg C] *)
    rAlarm_SIP_Temp_Deadband := 0.5;    (* SIP deadband [deg C] *)

    (* 13. Initialize Slew Rates *)
    rShelfHeater_SlewRate_pct_s  := 5.0;  (* Max 5.0% per sec *)
    rShelfCooling_SlewRate_pct_s := 8.0;  (* Max 8.0% per sec *)
    rN2Bleed_SlewRate_pct_s      := 25.0; (* Max 25.0% per sec *)
    rMpcStepSize                 := 0.015;

    (* Initial FSM State: IDLE_STERILE_HOLD *)
    iState             := 1;
    iPrevState         := 1;
    tStateTimer_s      := 0.0;
    tTotalBatchTimer_s := 0.0;
    bStateFirstScan    := TRUE;
    bCycleComplete     := FALSE;
    bPrimaryDryingComplete   := FALSE;
    bSecondaryDryingComplete := FALSE;
    bStopperingComplete      := FALSE;
    bSterilizationComplete   := FALSE;

    bInitialized := TRUE;
END_IF;

(* Master Hardware Emergency Stop & System Enable Check *)
IF NOT bEmergencyStop OR NOT bEnable THEN
    IF iState <> 1 THEN
        iPrevState := iState;
        iState := 1; (* Abort immediately to Safe Sterile Hold *)
        tStateTimer_s := 0.0;
        bStateFirstScan := TRUE;
    END_IF;
END_IF;

(* Master Fault & Alarm Reset Logic *)
IF bReset THEN
    bTMR1_FaultA := FALSE; bTMR1_FaultB := FALSE; bTMR1_FaultC := FALSE;
    tTMR1_TimerA := 0.0;   tTMR1_TimerB := 0.0;   tTMR1_TimerC := 0.0;
    bTMR2_FaultA := FALSE; bTMR2_FaultB := FALSE; bTMR2_FaultC := FALSE;
    tTMR2_TimerA := 0.0;   tTMR2_TimerB := 0.0;   tTMR2_TimerC := 0.0;
    bTMR3_FaultA := FALSE; bTMR3_FaultB := FALSE; bTMR3_FaultC := FALSE;
    tTMR3_TimerA := 0.0;   tTMR3_TimerB := 0.0;   tTMR3_TimerC := 0.0;
    bTMR4_FaultA := FALSE; bTMR4_FaultB := FALSE; bTMR4_FaultC := FALSE;
    tTMR4_TimerA := 0.0;   tTMR4_TimerB := 0.0;   tTMR4_TimerC := 0.0;
    bTMR5_FaultA := FALSE; bTMR5_FaultB := FALSE; bTMR5_FaultC := FALSE;
    tTMR5_TimerA := 0.0;   tTMR5_TimerB := 0.0;   tTMR5_TimerC := 0.0;
    bTMR6_FaultA := FALSE; bTMR6_FaultB := FALSE; bTMR6_FaultC := FALSE;
    tTMR6_TimerA := 0.0;   tTMR6_TimerB := 0.0;   tTMR6_TimerC := 0.0;
    tAlarmTimer_VacLossHH    := 0.0;
    tAlarmTimer_ProductHH    := 0.0;
    tAlarmTimer_CondTempHH   := 0.0;
    tAlarmTimer_ShelfSpreadH := 0.0;
    tAlarmTimer_HydPressHH   := 0.0;
    tAlarmTimer_SIP_TempLL   := 0.0;
    dwISAAlarm_Critical := 16#00000000;
    dwISAAlarm_Warning  := 16#00000000;
    dwISAAlarm_Advisory := 16#00000000;
    bAlarm_AnyCritical  := FALSE;
    bAlarm_AnyWarning   := FALSE;
END_IF;


(* ==========================================================================================
 * PHASE 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY TIMERS
 * ========================================================================================== *)

(* ------------------------------------------------------------------------------------------
 * TMR Group 1: Shelf Product Vial Core Temperature RTDs [deg C] (TE101A, TE101B, TE101C)
 * ------------------------------------------------------------------------------------------ *)
rTMR1_DiffAB := ABS(rTemp_Product_TE101A - rTemp_Product_TE101B);
rTMR1_DiffBC := ABS(rTemp_Product_TE101B - rTemp_Product_TE101C);
rTMR1_DiffCA := ABS(rTemp_Product_TE101C - rTemp_Product_TE101A);

(* Discrepancy Debounce Timers (Tolerance: 1.5 deg C, Hold: 3.0 s) *)
IF (rTMR1_DiffAB > 1.5) AND (rTMR1_DiffCA > 1.5) THEN
    tTMR1_TimerA := tTMR1_TimerA + rDeltaTime_s;
    IF tTMR1_TimerA >= 3.0 THEN
        bTMR1_FaultA := TRUE;
    END_IF;
ELSE
    tTMR1_TimerA := 0.0;
END_IF;

IF (rTMR1_DiffAB > 1.5) AND (rTMR1_DiffBC > 1.5) THEN
    tTMR1_TimerB := tTMR1_TimerB + rDeltaTime_s;
    IF tTMR1_TimerB >= 3.0 THEN
        bTMR1_FaultB := TRUE;
    END_IF;
ELSE
    tTMR1_TimerB := 0.0;
END_IF;

IF (rTMR1_DiffBC > 1.5) AND (rTMR1_DiffCA > 1.5) THEN
    tTMR1_TimerC := tTMR1_TimerC + rDeltaTime_s;
    IF tTMR1_TimerC >= 3.0 THEN
        bTMR1_FaultC := TRUE;
    END_IF;
ELSE
    tTMR1_TimerC := 0.0;
END_IF;

(* Median & Degraded Fallback Voting Logic *)
IF NOT bTMR1_FaultA AND NOT bTMR1_FaultB AND NOT bTMR1_FaultC THEN
    (* Full TMR Health: Median of 3 *)
    IF (rTemp_Product_TE101A >= rTemp_Product_TE101B AND rTemp_Product_TE101A <= rTemp_Product_TE101C) OR
       (rTemp_Product_TE101A <= rTemp_Product_TE101B AND rTemp_Product_TE101A >= rTemp_Product_TE101C) THEN
        rTMR1_VotedVal := rTemp_Product_TE101A;
    ELSIF (rTemp_Product_TE101B >= rTemp_Product_TE101A AND rTemp_Product_TE101B <= rTemp_Product_TE101C) OR
          (rTemp_Product_TE101B <= rTemp_Product_TE101A AND rTemp_Product_TE101B >= rTemp_Product_TE101C) THEN
        rTMR1_VotedVal := rTemp_Product_TE101B;
    ELSE
        rTMR1_VotedVal := rTemp_Product_TE101C;
    END_IF;
    iTMR1_HealthGrade := 3;
ELSIF bTMR1_FaultA AND NOT bTMR1_FaultB AND NOT bTMR1_FaultC THEN
    rTMR1_VotedVal := (rTemp_Product_TE101B + rTemp_Product_TE101C) * 0.5;
    iTMR1_HealthGrade := 2;
ELSIF bTMR1_FaultB AND NOT bTMR1_FaultA AND NOT bTMR1_FaultC THEN
    rTMR1_VotedVal := (rTemp_Product_TE101A + rTemp_Product_TE101C) * 0.5;
    iTMR1_HealthGrade := 2;
ELSIF bTMR1_FaultC AND NOT bTMR1_FaultA AND NOT bTMR1_FaultB THEN
    rTMR1_VotedVal := (rTemp_Product_TE101A + rTemp_Product_TE101B) * 0.5;
    iTMR1_HealthGrade := 2;
ELSIF NOT bTMR1_FaultA AND bTMR1_FaultB AND bTMR1_FaultC THEN
    rTMR1_VotedVal := rTemp_Product_TE101A;
    iTMR1_HealthGrade := 1;
ELSIF NOT bTMR1_FaultB AND bTMR1_FaultA AND bTMR1_FaultC THEN
    rTMR1_VotedVal := rTemp_Product_TE101B;
    iTMR1_HealthGrade := 1;
ELSIF NOT bTMR1_FaultC AND bTMR1_FaultA AND bTMR1_FaultB THEN
    rTMR1_VotedVal := rTemp_Product_TE101C;
    iTMR1_HealthGrade := 1;
ELSE
    rTMR1_VotedVal := rTemp_Product_TE101A;
    iTMR1_HealthGrade := 0; (* All Sensors Tripped *)
END_IF;

(* ------------------------------------------------------------------------------------------
 * TMR Group 2: Chamber Absolute Capacitance Manometers [mbar] (PT201A, PT201B, PT201C)
 * ------------------------------------------------------------------------------------------ *)
rTMR2_DiffAB := ABS(rPress_Chamber_Baratron_PT201A - rPress_Chamber_Baratron_PT201B);
rTMR2_DiffBC := ABS(rPress_Chamber_Baratron_PT201B - rPress_Chamber_Baratron_PT201C);
rTMR2_DiffCA := ABS(rPress_Chamber_Baratron_PT201C - rPress_Chamber_Baratron_PT201A);

IF (rTMR2_DiffAB > 0.015) AND (rTMR2_DiffCA > 0.015) THEN
    tTMR2_TimerA := tTMR2_TimerA + rDeltaTime_s;
    IF tTMR2_TimerA >= 3.0 THEN
        bTMR2_FaultA := TRUE;
    END_IF;
ELSE
    tTMR2_TimerA := 0.0;
END_IF;

IF (rTMR2_DiffAB > 0.015) AND (rTMR2_DiffBC > 0.015) THEN
    tTMR2_TimerB := tTMR2_TimerB + rDeltaTime_s;
    IF tTMR2_TimerB >= 3.0 THEN
        bTMR2_FaultB := TRUE;
    END_IF;
ELSE
    tTMR2_TimerB := 0.0;
END_IF;

IF (rTMR2_DiffBC > 0.015) AND (rTMR2_DiffCA > 0.015) THEN
    tTMR2_TimerC := tTMR2_TimerC + rDeltaTime_s;
    IF tTMR2_TimerC >= 3.0 THEN
        bTMR2_FaultC := TRUE;
    END_IF;
ELSE
    tTMR2_TimerC := 0.0;
END_IF;

IF NOT bTMR2_FaultA AND NOT bTMR2_FaultB AND NOT bTMR2_FaultC THEN
    IF (rPress_Chamber_Baratron_PT201A >= rPress_Chamber_Baratron_PT201B AND rPress_Chamber_Baratron_PT201A <= rPress_Chamber_Baratron_PT201C) OR
       (rPress_Chamber_Baratron_PT201A <= rPress_Chamber_Baratron_PT201B AND rPress_Chamber_Baratron_PT201A >= rPress_Chamber_Baratron_PT201C) THEN
        rTMR2_VotedVal := rPress_Chamber_Baratron_PT201A;
    ELSIF (rPress_Chamber_Baratron_PT201B >= rPress_Chamber_Baratron_PT201A AND rPress_Chamber_Baratron_PT201B <= rPress_Chamber_Baratron_PT201C) OR
          (rPress_Chamber_Baratron_PT201B <= rPress_Chamber_Baratron_PT201A AND rPress_Chamber_Baratron_PT201B >= rPress_Chamber_Baratron_PT201C) THEN
        rTMR2_VotedVal := rPress_Chamber_Baratron_PT201B;
    ELSE
        rTMR2_VotedVal := rPress_Chamber_Baratron_PT201C;
    END_IF;
    iTMR2_HealthGrade := 3;
ELSIF bTMR2_FaultA AND NOT bTMR2_FaultB AND NOT bTMR2_FaultC THEN
    rTMR2_VotedVal := (rPress_Chamber_Baratron_PT201B + rPress_Chamber_Baratron_PT201C) * 0.5;
    iTMR2_HealthGrade := 2;
ELSIF bTMR2_FaultB AND NOT bTMR2_FaultA AND NOT bTMR2_FaultC THEN
    rTMR2_VotedVal := (rPress_Chamber_Baratron_PT201A + rPress_Chamber_Baratron_PT201C) * 0.5;
    iTMR2_HealthGrade := 2;
ELSIF bTMR2_FaultC AND NOT bTMR2_FaultA AND NOT bTMR2_FaultB THEN
    rTMR2_VotedVal := (rPress_Chamber_Baratron_PT201A + rPress_Chamber_Baratron_PT201B) * 0.5;
    iTMR2_HealthGrade := 2;
ELSIF NOT bTMR2_FaultA AND bTMR2_FaultB AND bTMR2_FaultC THEN
    rTMR2_VotedVal := rPress_Chamber_Baratron_PT201A;
    iTMR2_HealthGrade := 1;
ELSIF NOT bTMR2_FaultB AND bTMR2_FaultA AND bTMR2_FaultC THEN
    rTMR2_VotedVal := rPress_Chamber_Baratron_PT201B;
    iTMR2_HealthGrade := 1;
ELSIF NOT bTMR2_FaultC AND bTMR2_FaultA AND bTMR2_FaultB THEN
    rTMR2_VotedVal := rPress_Chamber_Baratron_PT201C;
    iTMR2_HealthGrade := 1;
ELSE
    rTMR2_VotedVal := rPress_Chamber_Baratron_PT201A;
    iTMR2_HealthGrade := 0;
END_IF;

(* ------------------------------------------------------------------------------------------
 * TMR Group 3: Condenser Suction Pressure Transmitters [bar] (PT301A, PT301B, PT301C)
 * ------------------------------------------------------------------------------------------ *)
rTMR3_DiffAB := ABS(rPress_Suction_PT301A - rPress_Suction_PT301B);
rTMR3_DiffBC := ABS(rPress_Suction_PT301B - rPress_Suction_PT301C);
rTMR3_DiffCA := ABS(rPress_Suction_PT301C - rPress_Suction_PT301A);

IF (rTMR3_DiffAB > 0.8) AND (rTMR3_DiffCA > 0.8) THEN
    tTMR3_TimerA := tTMR3_TimerA + rDeltaTime_s;
    IF tTMR3_TimerA >= 3.0 THEN
        bTMR3_FaultA := TRUE;
    END_IF;
ELSE
    tTMR3_TimerA := 0.0;
END_IF;

IF (rTMR3_DiffAB > 0.8) AND (rTMR3_DiffBC > 0.8) THEN
    tTMR3_TimerB := tTMR3_TimerB + rDeltaTime_s;
    IF tTMR3_TimerB >= 3.0 THEN
        bTMR3_FaultB := TRUE;
    END_IF;
ELSE
    tTMR3_TimerB := 0.0;
END_IF;

IF (rTMR3_DiffBC > 0.8) AND (rTMR3_DiffCA > 0.8) THEN
    tTMR3_TimerC := tTMR3_TimerC + rDeltaTime_s;
    IF tTMR3_TimerC >= 3.0 THEN
        bTMR3_FaultC := TRUE;
    END_IF;
ELSE
    tTMR3_TimerC := 0.0;
END_IF;

IF NOT bTMR3_FaultA AND NOT bTMR3_FaultB AND NOT bTMR3_FaultC THEN
    IF (rPress_Suction_PT301A >= rPress_Suction_PT301B AND rPress_Suction_PT301A <= rPress_Suction_PT301C) OR
       (rPress_Suction_PT301A <= rPress_Suction_PT301B AND rPress_Suction_PT301A >= rPress_Suction_PT301C) THEN
        rTMR3_VotedVal := rPress_Suction_PT301A;
    ELSIF (rPress_Suction_PT301B >= rPress_Suction_PT301A AND rPress_Suction_PT301B <= rPress_Suction_PT301C) OR
          (rPress_Suction_PT301B <= rPress_Suction_PT301A AND rPress_Suction_PT301B >= rPress_Suction_PT301C) THEN
        rTMR3_VotedVal := rPress_Suction_PT301B;
    ELSE
        rTMR3_VotedVal := rPress_Suction_PT301C;
    END_IF;
    iTMR3_HealthGrade := 3;
ELSIF bTMR3_FaultA AND NOT bTMR3_FaultB AND NOT bTMR3_FaultC THEN
    rTMR3_VotedVal := (rPress_Suction_PT301B + rPress_Suction_PT301C) * 0.5;
    iTMR3_HealthGrade := 2;
ELSIF bTMR3_FaultB AND NOT bTMR3_FaultA AND NOT bTMR3_FaultC THEN
    rTMR3_VotedVal := (rPress_Suction_PT301A + rPress_Suction_PT301C) * 0.5;
    iTMR3_HealthGrade := 2;
ELSIF bTMR3_FaultC AND NOT bTMR3_FaultA AND NOT bTMR3_FaultB THEN
    rTMR3_VotedVal := (rPress_Suction_PT301A + rPress_Suction_PT301B) * 0.5;
    iTMR3_HealthGrade := 2;
ELSIF NOT bTMR3_FaultA AND bTMR3_FaultB AND bTMR3_FaultC THEN
    rTMR3_VotedVal := rPress_Suction_PT301A;
    iTMR3_HealthGrade := 1;
ELSIF NOT bTMR3_FaultB AND bTMR3_FaultA AND bTMR3_FaultC THEN
    rTMR3_VotedVal := rPress_Suction_PT301B;
    iTMR3_HealthGrade := 1;
ELSIF NOT bTMR3_FaultC AND bTMR3_FaultA AND bTMR3_FaultB THEN
    rTMR3_VotedVal := rPress_Suction_PT301C;
    iTMR3_HealthGrade := 1;
ELSE
    rTMR3_VotedVal := rPress_Suction_PT301A;
    iTMR3_HealthGrade := 0;
END_IF;

(* ------------------------------------------------------------------------------------------
 * TMR Group 4: Shelf Silicone Oil Supply Temperature Probes [deg C] (TE401A, TE401B, TE401C)
 * ------------------------------------------------------------------------------------------ *)
rTMR4_DiffAB := ABS(rTemp_OilSupply_TE401A - rTemp_OilSupply_TE401B);
rTMR4_DiffBC := ABS(rTemp_OilSupply_TE401B - rTemp_OilSupply_TE401C);
rTMR4_DiffCA := ABS(rTemp_OilSupply_TE401C - rTemp_OilSupply_TE401A);

IF (rTMR4_DiffAB > 1.0) AND (rTMR4_DiffCA > 1.0) THEN
    tTMR4_TimerA := tTMR4_TimerA + rDeltaTime_s;
    IF tTMR4_TimerA >= 3.0 THEN
        bTMR4_FaultA := TRUE;
    END_IF;
ELSE
    tTMR4_TimerA := 0.0;
END_IF;

IF (rTMR4_DiffAB > 1.0) AND (rTMR4_DiffBC > 1.0) THEN
    tTMR4_TimerB := tTMR4_TimerB + rDeltaTime_s;
    IF tTMR4_TimerB >= 3.0 THEN
        bTMR4_FaultB := TRUE;
    END_IF;
ELSE
    tTMR4_TimerB := 0.0;
END_IF;

IF (rTMR4_DiffBC > 1.0) AND (rTMR4_DiffCA > 1.0) THEN
    tTMR4_TimerC := tTMR4_TimerC + rDeltaTime_s;
    IF tTMR4_TimerC >= 3.0 THEN
        bTMR4_FaultC := TRUE;
    END_IF;
ELSE
    tTMR4_TimerC := 0.0;
END_IF;

IF NOT bTMR4_FaultA AND NOT bTMR4_FaultB AND NOT bTMR4_FaultC THEN
    IF (rTemp_OilSupply_TE401A >= rTemp_OilSupply_TE401B AND rTemp_OilSupply_TE401A <= rTemp_OilSupply_TE401C) OR
       (rTemp_OilSupply_TE401A <= rTemp_OilSupply_TE401B AND rTemp_OilSupply_TE401A >= rTemp_OilSupply_TE401C) THEN
        rTMR4_VotedVal := rTemp_OilSupply_TE401A;
    ELSIF (rTemp_OilSupply_TE401B >= rTemp_OilSupply_TE401A AND rTemp_OilSupply_TE401B <= rTemp_OilSupply_TE401C) OR
          (rTemp_OilSupply_TE401B <= rTemp_OilSupply_TE401A AND rTemp_OilSupply_TE401B >= rTemp_OilSupply_TE401C) THEN
        rTMR4_VotedVal := rTemp_OilSupply_TE401B;
    ELSE
        rTMR4_VotedVal := rTemp_OilSupply_TE401C;
    END_IF;
    iTMR4_HealthGrade := 3;
ELSIF bTMR4_FaultA AND NOT bTMR4_FaultB AND NOT bTMR4_FaultC THEN
    rTMR4_VotedVal := (rTemp_OilSupply_TE401B + rTemp_OilSupply_TE401C) * 0.5;
    iTMR4_HealthGrade := 2;
ELSIF bTMR4_FaultB AND NOT bTMR4_FaultA AND NOT bTMR4_FaultC THEN
    rTMR4_VotedVal := (rTemp_OilSupply_TE401A + rTemp_OilSupply_TE401C) * 0.5;
    iTMR4_HealthGrade := 2;
ELSIF bTMR4_FaultC AND NOT bTMR4_FaultA AND NOT bTMR4_FaultB THEN
    rTMR4_VotedVal := (rTemp_OilSupply_TE401A + rTemp_OilSupply_TE401B) * 0.5;
    iTMR4_HealthGrade := 2;
ELSIF NOT bTMR4_FaultA AND bTMR4_FaultB AND bTMR4_FaultC THEN
    rTMR4_VotedVal := rTemp_OilSupply_TE401A;
    iTMR4_HealthGrade := 1;
ELSIF NOT bTMR4_FaultB AND bTMR4_FaultA AND bTMR4_FaultC THEN
    rTMR4_VotedVal := rTemp_OilSupply_TE401B;
    iTMR4_HealthGrade := 1;
ELSIF NOT bTMR4_FaultC AND bTMR4_FaultA AND bTMR4_FaultB THEN
    rTMR4_VotedVal := rTemp_OilSupply_TE401C;
    iTMR4_HealthGrade := 1;
ELSE
    rTMR4_VotedVal := rTemp_OilSupply_TE401A;
    iTMR4_HealthGrade := 0;
END_IF;

(* ------------------------------------------------------------------------------------------
 * TMR Group 5: Chamber Thermal Conductivity Pirani Gauges [mbar] (PT501A, PT501B, PT501C)
 * ------------------------------------------------------------------------------------------ *)
rTMR5_DiffAB := ABS(rPress_Chamber_Pirani_PT501A - rPress_Chamber_Pirani_PT501B);
rTMR5_DiffBC := ABS(rPress_Chamber_Pirani_PT501B - rPress_Chamber_Pirani_PT501C);
rTMR5_DiffCA := ABS(rPress_Chamber_Pirani_PT501C - rPress_Chamber_Pirani_PT501A);

IF (rTMR5_DiffAB > 0.025) AND (rTMR5_DiffCA > 0.025) THEN
    tTMR5_TimerA := tTMR5_TimerA + rDeltaTime_s;
    IF tTMR5_TimerA >= 3.0 THEN
        bTMR5_FaultA := TRUE;
    END_IF;
ELSE
    tTMR5_TimerA := 0.0;
END_IF;

IF (rTMR5_DiffAB > 0.025) AND (rTMR5_DiffBC > 0.025) THEN
    tTMR5_TimerB := tTMR5_TimerB + rDeltaTime_s;
    IF tTMR5_TimerB >= 3.0 THEN
        bTMR5_FaultB := TRUE;
    END_IF;
ELSE
    tTMR5_TimerB := 0.0;
END_IF;

IF (rTMR5_DiffBC > 0.025) AND (rTMR5_DiffCA > 0.025) THEN
    tTMR5_TimerC := tTMR5_TimerC + rDeltaTime_s;
    IF tTMR5_TimerC >= 3.0 THEN
        bTMR5_FaultC := TRUE;
    END_IF;
ELSE
    tTMR5_TimerC := 0.0;
END_IF;

IF NOT bTMR5_FaultA AND NOT bTMR5_FaultB AND NOT bTMR5_FaultC THEN
    IF (rPress_Chamber_Pirani_PT501A >= rPress_Chamber_Pirani_PT501B AND rPress_Chamber_Pirani_PT501A <= rPress_Chamber_Pirani_PT501C) OR
       (rPress_Chamber_Pirani_PT501A <= rPress_Chamber_Pirani_PT501B AND rPress_Chamber_Pirani_PT501A >= rPress_Chamber_Pirani_PT501C) THEN
        rTMR5_VotedVal := rPress_Chamber_Pirani_PT501A;
    ELSIF (rPress_Chamber_Pirani_PT501B >= rPress_Chamber_Pirani_PT501A AND rPress_Chamber_Pirani_PT501B <= rPress_Chamber_Pirani_PT501C) OR
          (rPress_Chamber_Pirani_PT501B <= rPress_Chamber_Pirani_PT501A AND rPress_Chamber_Pirani_PT501B >= rPress_Chamber_Pirani_PT501C) THEN
        rTMR5_VotedVal := rPress_Chamber_Pirani_PT501B;
    ELSE
        rTMR5_VotedVal := rPress_Chamber_Pirani_PT501C;
    END_IF;
    iTMR5_HealthGrade := 3;
ELSIF bTMR5_FaultA AND NOT bTMR5_FaultB AND NOT bTMR5_FaultC THEN
    rTMR5_VotedVal := (rPress_Chamber_Pirani_PT501B + rPress_Chamber_Pirani_PT501C) * 0.5;
    iTMR5_HealthGrade := 2;
ELSIF bTMR5_FaultB AND NOT bTMR5_FaultA AND NOT bTMR5_FaultC THEN
    rTMR5_VotedVal := (rPress_Chamber_Pirani_PT501A + rPress_Chamber_Pirani_PT501C) * 0.5;
    iTMR5_HealthGrade := 2;
ELSIF bTMR5_FaultC AND NOT bTMR5_FaultA AND NOT bTMR5_FaultB THEN
    rTMR5_VotedVal := (rPress_Chamber_Pirani_PT501A + rPress_Chamber_Pirani_PT501B) * 0.5;
    iTMR5_HealthGrade := 2;
ELSIF NOT bTMR5_FaultA AND bTMR5_FaultB AND bTMR5_FaultC THEN
    rTMR5_VotedVal := rPress_Chamber_Pirani_PT501A;
    iTMR5_HealthGrade := 1;
ELSIF NOT bTMR5_FaultB AND bTMR5_FaultA AND bTMR5_FaultC THEN
    rTMR5_VotedVal := rPress_Chamber_Pirani_PT501B;
    iTMR5_HealthGrade := 1;
ELSIF NOT bTMR5_FaultC AND bTMR5_FaultA AND bTMR5_FaultB THEN
    rTMR5_VotedVal := rPress_Chamber_Pirani_PT501C;
    iTMR5_HealthGrade := 1;
ELSE
    rTMR5_VotedVal := rPress_Chamber_Pirani_PT501A;
    iTMR5_HealthGrade := 0;
END_IF;

(* ------------------------------------------------------------------------------------------
 * TMR Group 6: Hydraulic Stoppering Cylinder Pressure Transducers [bar] (PT601A, PT601B, PT601C)
 * ------------------------------------------------------------------------------------------ *)
rTMR6_DiffAB := ABS(rPress_Hydraulic_PT601A - rPress_Hydraulic_PT601B);
rTMR6_DiffBC := ABS(rPress_Hydraulic_PT601B - rPress_Hydraulic_PT601C);
rTMR6_DiffCA := ABS(rPress_Hydraulic_PT601C - rPress_Hydraulic_PT601A);

IF (rTMR6_DiffAB > 6.0) AND (rTMR6_DiffCA > 6.0) THEN
    tTMR6_TimerA := tTMR6_TimerA + rDeltaTime_s;
    IF tTMR6_TimerA >= 3.0 THEN
        bTMR6_FaultA := TRUE;
    END_IF;
ELSE
    tTMR6_TimerA := 0.0;
END_IF;

IF (rTMR6_DiffAB > 6.0) AND (rTMR6_DiffBC > 6.0) THEN
    tTMR6_TimerB := tTMR6_TimerB + rDeltaTime_s;
    IF tTMR6_TimerB >= 3.0 THEN
        bTMR6_FaultB := TRUE;
    END_IF;
ELSE
    tTMR6_TimerB := 0.0;
END_IF;

IF (rTMR6_DiffBC > 6.0) AND (rTMR6_DiffCA > 6.0) THEN
    tTMR6_TimerC := tTMR6_TimerC + rDeltaTime_s;
    IF tTMR6_TimerC >= 3.0 THEN
        bTMR6_FaultC := TRUE;
    END_IF;
ELSE
    tTMR6_TimerC := 0.0;
END_IF;

IF NOT bTMR6_FaultA AND NOT bTMR6_FaultB AND NOT bTMR6_FaultC THEN
    IF (rPress_Hydraulic_PT601A >= rPress_Hydraulic_PT601B AND rPress_Hydraulic_PT601A <= rPress_Hydraulic_PT601C) OR
       (rPress_Hydraulic_PT601A <= rPress_Hydraulic_PT601B AND rPress_Hydraulic_PT601A >= rPress_Hydraulic_PT601C) THEN
        rTMR6_VotedVal := rPress_Hydraulic_PT601A;
    ELSIF (rPress_Hydraulic_PT601B >= rPress_Hydraulic_PT601A AND rPress_Hydraulic_PT601B <= rPress_Hydraulic_PT601C) OR
          (rPress_Hydraulic_PT601B <= rPress_Hydraulic_PT601A AND rPress_Hydraulic_PT601B >= rPress_Hydraulic_PT601C) THEN
        rTMR6_VotedVal := rPress_Hydraulic_PT601B;
    ELSE
        rTMR6_VotedVal := rPress_Hydraulic_PT601C;
    END_IF;
    iTMR6_HealthGrade := 3;
ELSIF bTMR6_FaultA AND NOT bTMR6_FaultB AND NOT bTMR6_FaultC THEN
    rTMR6_VotedVal := (rPress_Hydraulic_PT601B + rPress_Hydraulic_PT601C) * 0.5;
    iTMR6_HealthGrade := 2;
ELSIF bTMR6_FaultB AND NOT bTMR6_FaultA AND NOT bTMR6_FaultC THEN
    rTMR6_VotedVal := (rPress_Hydraulic_PT601A + rPress_Hydraulic_PT601C) * 0.5;
    iTMR6_HealthGrade := 2;
ELSIF bTMR6_FaultC AND NOT bTMR6_FaultA AND NOT bTMR6_FaultB THEN
    rTMR6_VotedVal := (rPress_Hydraulic_PT601A + rPress_Hydraulic_PT601B) * 0.5;
    iTMR6_HealthGrade := 2;
ELSIF NOT bTMR6_FaultA AND bTMR6_FaultB AND bTMR6_FaultC THEN
    rTMR6_VotedVal := rPress_Hydraulic_PT601A;
    iTMR6_HealthGrade := 1;
ELSIF NOT bTMR6_FaultB AND bTMR6_FaultA AND bTMR6_FaultC THEN
    rTMR6_VotedVal := rPress_Hydraulic_PT601B;
    iTMR6_HealthGrade := 1;
ELSIF NOT bTMR6_FaultC AND bTMR6_FaultA AND bTMR6_FaultB THEN
    rTMR6_VotedVal := rPress_Hydraulic_PT601C;
    iTMR6_HealthGrade := 1;
ELSE
    rTMR6_VotedVal := rPress_Hydraulic_PT601A;
    iTMR6_HealthGrade := 0;
END_IF;


(* ==========================================================================================
 * PHASE 3: CYBER-PHYSICAL OBSERVERS & DETAILED PHYSICAL FORMULATIONS
 * ========================================================================================== *)

(* ------------------------------------------------------------------------------------------
 * 1. Pikal Sublimation Kinetics & Dynamic Cake Resistance Observer
 * ------------------------------------------------------------------------------------------ *)
(* Product Ice Interface Temperature Estimation based on Heat Conduction & Vapor Sublimation Balance *)
rPikal_IceInterfaceTemp_degC := rTMR1_VotedVal - 1.20; (* Nominal core to interface delta *)

(* Clausius-Clapeyron Pure Ice Saturation Vapor Pressure Formulation [mbar] *)
(* P_sat(T) = 10^(24.01849 - 6144.96 / (T_ice + 273.15)) / 100.0 [converted from Pa to mbar] *)
IF (rPikal_IceInterfaceTemp_degC > -60.0) AND (rPikal_IceInterfaceTemp_degC < 0.0) THEN
    rPikal_SatIcePressure_mbar := EXPT(10.0, (24.01849 - (6144.96 / (rPikal_IceInterfaceTemp_degC + 273.15)))) / 100.0;
ELSE
    rPikal_SatIcePressure_mbar := 0.010;
END_IF;

(* Dynamic Dry Cake Mass Transfer Resistance Formulation Rp = R0 + (A1 * L_dry) / (1 + A2 * L_dry) *)
rPikal_DryCakeResistance_Rp := rPikal_CakeResistance_R0 + 
    ((rPikal_CakeResistance_A1 * rPikal_CakeDryThickness_mm) / (1.0 + (rPikal_CakeResistance_A2 * rPikal_CakeDryThickness_mm)));

(* Sublimation Vapor Mass Flux J_sub [kg/(m2*s)] *)
IF (rPikal_SatIcePressure_mbar > rTMR2_VotedVal) AND (rPikal_DryCakeResistance_Rp > 0.1) THEN
    (* 1 cm2*h*mbar/g = 36000 kg/(m2*s*mbar) conversion factor *)
    rPikal_SublimationFlux_kg_m2_s := ((rPikal_SatIcePressure_mbar - rTMR2_VotedVal) / rPikal_DryCakeResistance_Rp) * 0.0002778;
ELSE
    rPikal_SublimationFlux_kg_m2_s := 0.0;
END_IF;

(* Sublimation Front Recession Velocity v_sub [mm/h] *)
(* v_sub = (J_sub / rho_ice) * 3.6e6 *)
rPikal_SublimationVelocity_mm_h := (rPikal_SublimationFlux_kg_m2_s / 917.0) * 3600000.0;

(* Instantaneous Chamber Total Sublimation Mass Flow Rate [kg/h] across 40 m2 shelf loading *)
(* Assuming 40 m2 shelf area with 85% active vial packing = 34.0 m2 sublimation cross-section *)
rObs_SublimationRate_kgh := rPikal_SublimationFlux_kg_m2_s * 34.0 * 3600.0;

(* Cumulative Sublimation Mass Integration & Dry Layer Propagation *)
IF (iState = 6) OR (iState = 7) THEN
    rPikal_CumulativeSublimated_kg := rPikal_CumulativeSublimated_kg + (rObs_SublimationRate_kgh * (rDeltaTime_s / 3600.0));
    rPikal_CakeDryThickness_mm := rPikal_CakeDryThickness_mm + (rPikal_SublimationVelocity_mm_h * (rDeltaTime_s / 3600.0));
    IF rPikal_CakeDryThickness_mm > 22.0 THEN
        rPikal_CakeDryThickness_mm := 22.0; (* Full cake thickness reached *)
    END_IF;
END_IF;

rObs_DryLayerThickness_mm        := rPikal_CakeDryThickness_mm;
rObs_ProductIceInterfaceTemp_degC := rPikal_IceInterfaceTemp_degC;

(* ------------------------------------------------------------------------------------------
 * 2. Comparative Pressure Ratio (Pirani / Baratron) Observer & End-Point Convergence
 * ------------------------------------------------------------------------------------------ *)
IF rTMR2_VotedVal >= 0.005 THEN
    rComp_RawRatio := rTMR5_VotedVal / rTMR2_VotedVal;
ELSE
    rComp_RawRatio := 1.0;
END_IF;

(* First-Order Exponential Smoothing Filter on Comparative Ratio *)
rComp_FilteredRatio := rComp_FilteredRatio + (rComp_RatioFilterCoeff * (rComp_RawRatio - rComp_FilteredRatio));

(* Numerical Derivative of Comparative Ratio d(R_cp)/dt *)
rComp_RatioSlope_per_s := (rComp_RawRatio - rComp_FilteredRatio) / (rDeltaTime_s + 0.0001);

rObs_CompPressureRatio := rComp_FilteredRatio;

(* End-Point Convergence Detection (Primary Sublimation Completion Criterion):
 * When bulk ice is depleted, water vapor partial pressure collapses.
 * Chamber atmosphere transitions to pure Nitrogen bleed gas.
 * Pirani calibration aligns with Baratron: R_cp converges to 1.00 +/- 0.04. *)
IF (iState = 6) OR (iState = 7) THEN
    IF (rComp_FilteredRatio <= 1.08) AND (rComp_FilteredRatio >= 0.94) AND (ABS(rComp_RatioSlope_per_s) < 0.002) THEN
        tComp_ConvergenceTimer_s := tComp_ConvergenceTimer_s + rDeltaTime_s;
        IF tComp_ConvergenceTimer_s >= 1800.0 THEN (* 30 minutes continuous stability *)
            bComp_EndpointMet := TRUE;
        END_IF;
    ELSE
        IF tComp_ConvergenceTimer_s > 0.0 THEN
            tComp_ConvergenceTimer_s := tComp_ConvergenceTimer_s - (rDeltaTime_s * 0.5); (* Soft decay on transient spike *)
        END_IF;
    END_IF;
ELSE
    tComp_ConvergenceTimer_s := 0.0;
    bComp_EndpointMet := FALSE;
END_IF;

(* ------------------------------------------------------------------------------------------
 * 3. Manometric Temperature Measurement (MTM) / Pressure Rise Test (PRT) Observer
 * ------------------------------------------------------------------------------------------ *)
(* Periodic Triggering Every 3600 s During Primary Drying *)
IF (iState = 6) THEN
    rMTM_Interval_Timer_s := rMTM_Interval_Timer_s + rDeltaTime_s;
    IF (rMTM_Interval_Timer_s >= 3600.0) AND NOT bMTM_Active AND (tStateTimer_s > 1800.0) THEN
        bMTM_Active := TRUE;
        tMTM_Timer_s := 0.0;
        rMTM_StartPress_mbar := rTMR2_VotedVal;
        rMTM_Interval_Timer_s := 0.0;
    END_IF;
END_IF;

IF bMTM_Active THEN
    tMTM_Timer_s := tMTM_Timer_s + rDeltaTime_s;
    (* Close Isolation Butterfly for 15 seconds *)
    bCmd_IsolationValve_Close := TRUE;
    bCmd_IsolationValve_Open  := FALSE;

    IF tMTM_Timer_s >= 15.0 THEN
        rMTM_EndPress_mbar := rTMR2_VotedVal;
        rMTM_RateOfRise_mbar_s := (rMTM_EndPress_mbar - rMTM_StartPress_mbar) / 15.0;
        
        (* Extrapolated Equilibrium Vapor Pressure *)
        rMTM_EquilibriumVaporPress_mbar := rMTM_EndPress_mbar + (rMTM_RateOfRise_mbar_s * 8.5);

        (* Inverse Clausius-Clapeyron to deduce ice front temperature *)
        IF rMTM_EquilibriumVaporPress_mbar > 0.020 THEN
            rMTM_CalculatedIceTemp_degC := -6144.96 / ((LOG(rMTM_EquilibriumVaporPress_mbar * 100.0) / 2.302585) - 24.01849) - 273.15;
        ELSE
            rMTM_CalculatedIceTemp_degC := -50.0;
        END_IF;

        (* Terminate MTM Test & Re-Open Butterfly *)
        bMTM_Active := FALSE;
        tMTM_Timer_s := 0.0;
        bCmd_IsolationValve_Close := FALSE;
        bCmd_IsolationValve_Open  := TRUE;
    END_IF;
END_IF;

(* ------------------------------------------------------------------------------------------
 * 4. Steam-in-Place (SIP) F0 Thermal Lethality Integration
 * ------------------------------------------------------------------------------------------ *)
(* Sterilization F0 calculation based on Lowest Condensate Drain RTD (TE_Drain) *)
IF (iState = 12) AND (rTemp_SIP_DrainTrap_degC >= 100.0) THEN
    (* Instantaneous Lethality Rate L = 10^((T_drain - 121.11) / 10.0) *)
    rSIP_LethalityRate_per_min := EXPT(10.0, ((rTemp_SIP_DrainTrap_degC - rSIP_BaseTemp_degC) / rSIP_Z_Value_degC));
    rSIP_AccumulatedF0_min := rSIP_AccumulatedF0_min + (rSIP_LethalityRate_per_min * (rDeltaTime_s / 60.0));
    
    IF rSIP_AccumulatedF0_min >= rRecipe_SIP_MinF0_min THEN
        bSIP_SterilizationValid := TRUE;
    END_IF;
ELSE
    rSIP_LethalityRate_per_min := 0.0;
    IF (iState <> 12) AND (iState <> 1) THEN
        rSIP_AccumulatedF0_min := 0.0;
        bSIP_SterilizationValid := FALSE;
    END_IF;
END_IF;
rObs_CalculatedF0_min := rSIP_AccumulatedF0_min;

(* ------------------------------------------------------------------------------------------
 * 5. 16-Zone Shelf Thermal Uniformity Observer
 * ------------------------------------------------------------------------------------------ *)
rShelf_MinTemp_degC := rTemp_Shelf_Zones[1];
rShelf_MaxTemp_degC := rTemp_Shelf_Zones[1];
rTempSum            := 0.0;
iShelf_ColdestZoneIndex := 1;
iShelf_HottestZoneIndex := 1;

FOR iLoopI := 1 TO 16 DO
    rTempSum := rTempSum + rTemp_Shelf_Zones[iLoopI];
    IF rTemp_Shelf_Zones[iLoopI] < rShelf_MinTemp_degC THEN
        rShelf_MinTemp_degC := rTemp_Shelf_Zones[iLoopI];
        iShelf_ColdestZoneIndex := iLoopI;
    END_IF;
    IF rTemp_Shelf_Zones[iLoopI] > rShelf_MaxTemp_degC THEN
        rShelf_MaxTemp_degC := rTemp_Shelf_Zones[iLoopI];
        iShelf_HottestZoneIndex := iLoopI;
    END_IF;
END_FOR;

rShelf_AvgTemp_degC := rTempSum / 16.0;
rShelf_Spread_degC  := rShelf_MaxTemp_degC - rShelf_MinTemp_degC;
rObs_ShelfTempUniformity_degC := rShelf_Spread_degC;

(* ------------------------------------------------------------------------------------------
 * 6. Hydraulic Stoppering Tonnage & Compaction Mechanics Observer
 * ------------------------------------------------------------------------------------------ *)
(* Force F [kN] = P [bar] * 100 kPa/bar * Area [cm2] * 1e-4 m2/cm2 = P * Area * 0.01 *)
rHyd_CalculatedForce_kN := rTMR6_VotedVal * rHyd_PistonArea_cm2 * 0.010;

(* Tonnage [metric tons] = Force [kN] / 9.80665 *)
rHyd_CalculatedTonnage_ton := rHyd_CalculatedForce_kN / 9.80665;
rObs_StopperingTonnage_ton  := rHyd_CalculatedTonnage_ton;

(* Stopper Seating Displacement *)
IF rPos_StopperingRam_mm >= 100.0 THEN
    rHyd_VialDeflection_mm := rPos_StopperingRam_mm - 100.0;
ELSE
    rHyd_VialDeflection_mm := 0.0;
END_IF;

(* ------------------------------------------------------------------------------------------
 * 7. Condenser Ice Deposition & Thermal Balance Observer
 * ------------------------------------------------------------------------------------------ *)
(* Cumulative Ice Mass Deposited on 80 m2 Condenser Coil *)
rCond_IceMass_kg := rPikal_CumulativeSublimated_kg;

(* Average Ice Thickness h_ice [mm] = (Mass / (rho_ice * Area)) * 1000 *)
IF (rCond_IceDensity_kg_m3 > 100.0) AND (rCond_SurfaceArea_m2 > 10.0) THEN
    rCond_IceThickness_mm := (rCond_IceMass_kg / (rCond_IceDensity_kg_m3 * rCond_SurfaceArea_m2)) * 1000.0;
ELSE
    rCond_IceThickness_mm := 0.0;
END_IF;
rObs_CondenserIceThickness_mm := rCond_IceThickness_mm;

(* Instantaneous Sublimation Condensation Refrigeration Heat Load [kW] *)
(* Q_dot = (m_dot_sub [kg/h] / 3600) * 2835 kJ/kg *)
rCond_RefrigDuty_kW := (rObs_SublimationRate_kgh / 3600.0) * rPikal_LatentHeatSublimation_kJ;
'''

if __name__ == "__main__":
    print(f"Part 3 length: {len(get_part3())} characters")
