# ldpe_reactor_builder/st_phase1_tmr.py

def get_phase1_tmr():
    return """(* ============================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE WITH DISCREPANCY TIMERS       *)
(* 4 INSTRUMENTATION CLUSTERS:                                                                    *)
(*   CLUSTER 1: 4,000-BAR PIEZORESISTIVE QUARTZ TRANSDUCERS (PRESS_SENSORS 1, 2, 3) [bar]          *)
(*   CLUSTER 2: THICK-WALLED MULTI-JUNCTION TYPE K THERMOCOUPLES (TEMP_SENSORS 1, 2, 3) [deg C]   *)
(*   CLUSTER 3: CORIOLIS MASS FLOWMETERS FOR PEROXIDE DOSING (PEROXIDE_FLOW 1, 2, 3) [kg/h]        *)
(*   CLUSTER 4: TUBE WALL HIGH-FREQUENCY ACOUSTIC EMISSION PRECURSORS (ACOUSTIC 1, 2, 3) [dB]     *)
(* ============================================================================================== *)

(* ---------------------------------------------------------------------------------------------- *)
(* CLUSTER 1: REACTOR INLET OPERATING PRESSURE (2oo3 VOTING ACROSS QUARTZ TRANSDUCERS)           *)
(* ---------------------------------------------------------------------------------------------- *)
(* Range Validation Check: 0.0 to 4200.0 bar *)
IF rPress_Transducer_1_bar < 0.0 OR rPress_Transducer_1_bar > 4200.0 THEN
    bFault_Press_Ch1 := TRUE;
    rHealth_Press_Ch1_pct := 0.0;
END_IF;

IF rPress_Transducer_2_bar < 0.0 OR rPress_Transducer_2_bar > 4200.0 THEN
    bFault_Press_Ch2 := TRUE;
    rHealth_Press_Ch2_pct := 0.0;
END_IF;

IF rPress_Transducer_3_bar < 0.0 OR rPress_Transducer_3_bar > 4200.0 THEN
    bFault_Press_Ch3 := TRUE;
    rHealth_Press_Ch3_pct := 0.0;
END_IF;

(* Pairwise Delta Evaluation *)
rTempCalc1 := ABS(rPress_Transducer_1_bar - rPress_Transducer_2_bar); (* Delta 1-2 *)
rTempCalc2 := ABS(rPress_Transducer_2_bar - rPress_Transducer_3_bar); (* Delta 2-3 *)
rTempCalc3 := ABS(rPress_Transducer_3_bar - rPress_Transducer_1_bar); (* Delta 3-1 *)

(* Discrepancy Timer Accumulation *)
IF (rTempCalc1 > rTMR_Press_Tol_bar) OR (rTempCalc2 > rTMR_Press_Tol_bar) OR (rTempCalc3 > rTMR_Press_Tol_bar) THEN
    tTMR_Press_DiscTimer_s := tTMR_Press_DiscTimer_s + tScanCycleTime_s;
    IF tTMR_Press_DiscTimer_s >= tTMR_Press_TripDelay_s THEN
        (* Identify the Deviating Channel *)
        IF (rTempCalc1 > rTMR_Press_Tol_bar) AND (rTempCalc3 > rTMR_Press_Tol_bar) THEN
            bFault_Press_Ch1 := TRUE;
            rHealth_Press_Ch1_pct := 15.0;
        ELSIF (rTempCalc1 > rTMR_Press_Tol_bar) AND (rTempCalc2 > rTMR_Press_Tol_bar) THEN
            bFault_Press_Ch2 := TRUE;
            rHealth_Press_Ch2_pct := 15.0;
        ELSIF (rTempCalc2 > rTMR_Press_Tol_bar) AND (rTempCalc3 > rTMR_Press_Tol_bar) THEN
            bFault_Press_Ch3 := TRUE;
            rHealth_Press_Ch3_pct := 15.0;
        END_IF;
    END_IF;
ELSE
    IF tTMR_Press_DiscTimer_s > 0.0 THEN
        tTMR_Press_DiscTimer_s := tTMR_Press_DiscTimer_s - (tScanCycleTime_s * 2.0);
        IF tTMR_Press_DiscTimer_s < 0.0 THEN
            tTMR_Press_DiscTimer_s := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Pressure Voting & Degradation Logic *)
IF (NOT bFault_Press_Ch1) AND (NOT bFault_Press_Ch2) AND (NOT bFault_Press_Ch3) THEN
    (* 3 Channels Healthy: True Mid-Value (Median) Selection *)
    IF (rPress_Transducer_1_bar >= rPress_Transducer_2_bar AND rPress_Transducer_1_bar <= rPress_Transducer_3_bar) OR
       (rPress_Transducer_1_bar >= rPress_Transducer_3_bar AND rPress_Transducer_1_bar <= rPress_Transducer_2_bar) THEN
        rTempCalc4 := rPress_Transducer_1_bar;
    ELSIF (rPress_Transducer_2_bar >= rPress_Transducer_1_bar AND rPress_Transducer_2_bar <= rPress_Transducer_3_bar) OR
          (rPress_Transducer_2_bar >= rPress_Transducer_3_bar AND rPress_Transducer_2_bar <= rPress_Transducer_1_bar) THEN
        rTempCalc4 := rPress_Transducer_2_bar;
    ELSE
        rTempCalc4 := rPress_Transducer_3_bar;
    END_IF;
    rHealth_Press_Ch1_pct := 100.0;
    rHealth_Press_Ch2_pct := 100.0;
    rHealth_Press_Ch3_pct := 100.0;
ELSIF bFault_Press_Ch1 AND (NOT bFault_Press_Ch2) AND (NOT bFault_Press_Ch3) THEN
    (* Ch1 Fault: Degraded 1oo2 High-Select Conservative for Overpressure *)
    IF rPress_Transducer_2_bar > rPress_Transducer_3_bar THEN
        rTempCalc4 := rPress_Transducer_2_bar;
    ELSE
        rTempCalc4 := rPress_Transducer_3_bar;
    END_IF;
    rHealth_Press_Ch2_pct := 85.0;
    rHealth_Press_Ch3_pct := 85.0;
ELSIF bFault_Press_Ch2 AND (NOT bFault_Press_Ch1) AND (NOT bFault_Press_Ch3) THEN
    (* Ch2 Fault: Degraded 1oo2 High-Select Conservative *)
    IF rPress_Transducer_1_bar > rPress_Transducer_3_bar THEN
        rTempCalc4 := rPress_Transducer_1_bar;
    ELSE
        rTempCalc4 := rPress_Transducer_3_bar;
    END_IF;
    rHealth_Press_Ch1_pct := 85.0;
    rHealth_Press_Ch3_pct := 85.0;
ELSIF bFault_Press_Ch3 AND (NOT bFault_Press_Ch1) AND (NOT bFault_Press_Ch2) THEN
    (* Ch3 Fault: Degraded 1oo2 High-Select Conservative *)
    IF rPress_Transducer_1_bar > rPress_Transducer_2_bar THEN
        rTempCalc4 := rPress_Transducer_1_bar;
    ELSE
        rTempCalc4 := rPress_Transducer_2_bar;
    END_IF;
    rHealth_Press_Ch1_pct := 85.0;
    rHealth_Press_Ch2_pct := 85.0;
ELSIF (NOT bFault_Press_Ch1) AND bFault_Press_Ch2 AND bFault_Press_Ch3 THEN
    (* Single Channel Ch1 Surviving *)
    rTempCalc4 := rPress_Transducer_1_bar;
    rHealth_Press_Ch1_pct := 40.0;
ELSIF (NOT bFault_Press_Ch2) AND bFault_Press_Ch1 AND bFault_Press_Ch3 THEN
    (* Single Channel Ch2 Surviving *)
    rTempCalc4 := rPress_Transducer_2_bar;
    rHealth_Press_Ch2_pct := 40.0;
ELSIF (NOT bFault_Press_Ch3) AND bFault_Press_Ch1 AND bFault_Press_Ch2 THEN
    (* Single Channel Ch3 Surviving *)
    rTempCalc4 := rPress_Transducer_3_bar;
    rHealth_Press_Ch3_pct := 40.0;
ELSE
    (* All Channels Faulty: Fallback to State-Space Prediction *)
    rTempCalc4 := vecX_Est[iState_Pinlet];
END_IF;

(* Bumpless Transfer Low-Pass Filter on Pressure *)
rVoted_ReactorPressure_bar := rVoted_ReactorPressure_bar + 0.45 * (rTempCalc4 - rVoted_ReactorPressure_bar);

(* Real-Time Pressure Derivative Calculation (dP/dt in bar/s) *)
IF tScanCycleTime_s > 0.0001 THEN
    rFast_dP_dt_bar_s := (rVoted_ReactorPressure_bar - rVoted_Press_Prev_bar) / tScanCycleTime_s;
    rEst_RateOfPressureRise_bar_s := rFast_dP_dt_bar_s;
END_IF;
rVoted_Press_Prev_bar := rVoted_ReactorPressure_bar;


(* ---------------------------------------------------------------------------------------------- *)
(* CLUSTER 2: REACTION PEAK EXOTHERM TEMPERATURE (2oo3 VOTING ACROSS TYPE K THERMOCOUPLES)       *)
(* ---------------------------------------------------------------------------------------------- *)
(* Range Validation Check: 0.0 to 450.0 deg C *)
IF rTemp_Thermocouple_1_degC < 0.0 OR rTemp_Thermocouple_1_degC > 450.0 THEN
    bFault_Temp_Ch1 := TRUE;
    rHealth_Temp_Ch1_pct := 0.0;
END_IF;

IF rTemp_Thermocouple_2_degC < 0.0 OR rTemp_Thermocouple_2_degC > 450.0 THEN
    bFault_Temp_Ch2 := TRUE;
    rHealth_Temp_Ch2_pct := 0.0;
END_IF;

IF rTemp_Thermocouple_3_degC < 0.0 OR rTemp_Thermocouple_3_degC > 450.0 THEN
    bFault_Temp_Ch3 := TRUE;
    rHealth_Temp_Ch3_pct := 0.0;
END_IF;

(* Pairwise Delta Evaluation *)
rTempCalc1 := ABS(rTemp_Thermocouple_1_degC - rTemp_Thermocouple_2_degC);
rTempCalc2 := ABS(rTemp_Thermocouple_2_degC - rTemp_Thermocouple_3_degC);
rTempCalc3 := ABS(rTemp_Thermocouple_3_degC - rTemp_Thermocouple_1_degC);

IF (rTempCalc1 > rTMR_Temp_Tol_degC) OR (rTempCalc2 > rTMR_Temp_Tol_degC) OR (rTempCalc3 > rTMR_Temp_Tol_degC) THEN
    tTMR_Temp_DiscTimer_s := tTMR_Temp_DiscTimer_s + tScanCycleTime_s;
    IF tTMR_Temp_DiscTimer_s >= tTMR_Temp_TripDelay_s THEN
        IF (rTempCalc1 > rTMR_Temp_Tol_degC) AND (rTempCalc3 > rTMR_Temp_Tol_degC) THEN
            bFault_Temp_Ch1 := TRUE;
            rHealth_Temp_Ch1_pct := 15.0;
        ELSIF (rTempCalc1 > rTMR_Temp_Tol_degC) AND (rTempCalc2 > rTMR_Temp_Tol_degC) THEN
            bFault_Temp_Ch2 := TRUE;
            rHealth_Temp_Ch2_pct := 15.0;
        ELSIF (rTempCalc2 > rTMR_Temp_Tol_degC) AND (rTempCalc3 > rTMR_Temp_Tol_degC) THEN
            bFault_Temp_Ch3 := TRUE;
            rHealth_Temp_Ch3_pct := 15.0;
        END_IF;
    END_IF;
ELSE
    IF tTMR_Temp_DiscTimer_s > 0.0 THEN
        tTMR_Temp_DiscTimer_s := tTMR_Temp_DiscTimer_s - (tScanCycleTime_s * 2.0);
        IF tTMR_Temp_DiscTimer_s < 0.0 THEN
            tTMR_Temp_DiscTimer_s := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Temperature Voting & Degradation Logic *)
IF (NOT bFault_Temp_Ch1) AND (NOT bFault_Temp_Ch2) AND (NOT bFault_Temp_Ch3) THEN
    (* 3 Channels Healthy: Median Selection *)
    IF (rTemp_Thermocouple_1_degC >= rTemp_Thermocouple_2_degC AND rTemp_Thermocouple_1_degC <= rTemp_Thermocouple_3_degC) OR
       (rTemp_Thermocouple_1_degC >= rTemp_Thermocouple_3_degC AND rTemp_Thermocouple_1_degC <= rTemp_Thermocouple_2_degC) THEN
        rTempCalc4 := rTemp_Thermocouple_1_degC;
    ELSIF (rTemp_Thermocouple_2_degC >= rTemp_Thermocouple_1_degC AND rTemp_Thermocouple_2_degC <= rTemp_Thermocouple_3_degC) OR
          (rTemp_Thermocouple_2_degC >= rTemp_Thermocouple_3_degC AND rTemp_Thermocouple_2_degC <= rTemp_Thermocouple_1_degC) THEN
        rTempCalc4 := rTemp_Thermocouple_2_degC;
    ELSE
        rTempCalc4 := rTemp_Thermocouple_3_degC;
    END_IF;
    rHealth_Temp_Ch1_pct := 100.0;
    rHealth_Temp_Ch2_pct := 100.0;
    rHealth_Temp_Ch3_pct := 100.0;
ELSIF bFault_Temp_Ch1 AND (NOT bFault_Temp_Ch2) AND (NOT bFault_Temp_Ch3) THEN
    (* Ch1 Fault: Degraded 1oo2 High-Select Conservative for Runaway Exotherm *)
    IF rTemp_Thermocouple_2_degC > rTemp_Thermocouple_3_degC THEN
        rTempCalc4 := rTemp_Thermocouple_2_degC;
    ELSE
        rTempCalc4 := rTemp_Thermocouple_3_degC;
    END_IF;
    rHealth_Temp_Ch2_pct := 85.0;
    rHealth_Temp_Ch3_pct := 85.0;
ELSIF bFault_Temp_Ch2 AND (NOT bFault_Temp_Ch1) AND (NOT bFault_Temp_Ch3) THEN
    IF rTemp_Thermocouple_1_degC > rTemp_Thermocouple_3_degC THEN
        rTempCalc4 := rTemp_Thermocouple_1_degC;
    ELSE
        rTempCalc4 := rTemp_Thermocouple_3_degC;
    END_IF;
    rHealth_Temp_Ch1_pct := 85.0;
    rHealth_Temp_Ch3_pct := 85.0;
ELSIF bFault_Temp_Ch3 AND (NOT bFault_Temp_Ch1) AND (NOT bFault_Temp_Ch2) THEN
    IF rTemp_Thermocouple_1_degC > rTemp_Thermocouple_2_degC THEN
        rTempCalc4 := rTemp_Thermocouple_1_degC;
    ELSE
        rTempCalc4 := rTemp_Thermocouple_2_degC;
    END_IF;
    rHealth_Temp_Ch1_pct := 85.0;
    rHealth_Temp_Ch2_pct := 85.0;
ELSIF (NOT bFault_Temp_Ch1) AND bFault_Temp_Ch2 AND bFault_Temp_Ch3 THEN
    rTempCalc4 := rTemp_Thermocouple_1_degC;
    rHealth_Temp_Ch1_pct := 40.0;
ELSIF (NOT bFault_Temp_Ch2) AND bFault_Temp_Ch1 AND bFault_Temp_Ch3 THEN
    rTempCalc4 := rTemp_Thermocouple_2_degC;
    rHealth_Temp_Ch2_pct := 40.0;
ELSIF (NOT bFault_Temp_Ch3) AND bFault_Temp_Ch1 AND bFault_Temp_Ch2 THEN
    rTempCalc4 := rTemp_Thermocouple_3_degC;
    rHealth_Temp_Ch3_pct := 40.0;
ELSE
    rTempCalc4 := vecX_Est[iState_Tpeak];
END_IF;

(* Bumpless Transfer Low-Pass Filter on Peak Temperature *)
rVoted_PeakTemperature_degC := rVoted_PeakTemperature_degC + 0.35 * (rTempCalc4 - rVoted_PeakTemperature_degC);

(* Real-Time Temperature Derivative Calculation (dT/dt in K/s) *)
IF tScanCycleTime_s > 0.0001 THEN
    rFast_dT_dt_K_s := (rVoted_PeakTemperature_degC - rVoted_Temp_Prev_degC) / tScanCycleTime_s;
    rEst_RateOfTempRise_K_s := rFast_dT_dt_K_s;
END_IF;
rVoted_Temp_Prev_degC := rVoted_PeakTemperature_degC;


(* ---------------------------------------------------------------------------------------------- *)
(* CLUSTER 3: OPTICAL ABSORPTION CORIOLIS PEROXIDE DOSING FLOWMETERS [kg/h]                       *)
(* ---------------------------------------------------------------------------------------------- *)
(* Range Validation Check: 0.0 to 120.0 kg/h *)
IF rPeroxide_FlowMeter_1_kgh < 0.0 OR rPeroxide_FlowMeter_1_kgh > 120.0 THEN
    bFault_Flow_Ch1 := TRUE;
    rHealth_Flow_Ch1_pct := 0.0;
END_IF;

IF rPeroxide_FlowMeter_2_kgh < 0.0 OR rPeroxide_FlowMeter_2_kgh > 120.0 THEN
    bFault_Flow_Ch2 := TRUE;
    rHealth_Flow_Ch2_pct := 0.0;
END_IF;

IF rPeroxide_FlowMeter_3_kgh < 0.0 OR rPeroxide_FlowMeter_3_kgh > 120.0 THEN
    bFault_Flow_Ch3 := TRUE;
    rHealth_Flow_Ch3_pct := 0.0;
END_IF;

rTempCalc1 := ABS(rPeroxide_FlowMeter_1_kgh - rPeroxide_FlowMeter_2_kgh);
rTempCalc2 := ABS(rPeroxide_FlowMeter_2_kgh - rPeroxide_FlowMeter_3_kgh);
rTempCalc3 := ABS(rPeroxide_FlowMeter_3_kgh - rPeroxide_FlowMeter_1_kgh);

IF (rTempCalc1 > rTMR_Flow_Tol_kgh) OR (rTempCalc2 > rTMR_Flow_Tol_kgh) OR (rTempCalc3 > rTMR_Flow_Tol_kgh) THEN
    tTMR_Flow_DiscTimer_s := tTMR_Flow_DiscTimer_s + tScanCycleTime_s;
    IF tTMR_Flow_DiscTimer_s >= tTMR_Flow_TripDelay_s THEN
        IF (rTempCalc1 > rTMR_Flow_Tol_kgh) AND (rTempCalc3 > rTMR_Flow_Tol_kgh) THEN
            bFault_Flow_Ch1 := TRUE;
            rHealth_Flow_Ch1_pct := 20.0;
        ELSIF (rTempCalc1 > rTMR_Flow_Tol_kgh) AND (rTempCalc2 > rTMR_Flow_Tol_kgh) THEN
            bFault_Flow_Ch2 := TRUE;
            rHealth_Flow_Ch2_pct := 20.0;
        ELSIF (rTempCalc2 > rTMR_Flow_Tol_kgh) AND (rTempCalc3 > rTMR_Flow_Tol_kgh) THEN
            bFault_Flow_Ch3 := TRUE;
            rHealth_Flow_Ch3_pct := 20.0;
        END_IF;
    END_IF;
ELSE
    IF tTMR_Flow_DiscTimer_s > 0.0 THEN
        tTMR_Flow_DiscTimer_s := tTMR_Flow_DiscTimer_s - (tScanCycleTime_s * 2.0);
        IF tTMR_Flow_DiscTimer_s < 0.0 THEN
            tTMR_Flow_DiscTimer_s := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Flowmeter Mid-Value / Average Selection *)
IF (NOT bFault_Flow_Ch1) AND (NOT bFault_Flow_Ch2) AND (NOT bFault_Flow_Ch3) THEN
    IF (rPeroxide_FlowMeter_1_kgh >= rPeroxide_FlowMeter_2_kgh AND rPeroxide_FlowMeter_1_kgh <= rPeroxide_FlowMeter_3_kgh) OR
       (rPeroxide_FlowMeter_1_kgh >= rPeroxide_FlowMeter_3_kgh AND rPeroxide_FlowMeter_1_kgh <= rPeroxide_FlowMeter_2_kgh) THEN
        rTempCalc4 := rPeroxide_FlowMeter_1_kgh;
    ELSIF (rPeroxide_FlowMeter_2_kgh >= rPeroxide_FlowMeter_1_kgh AND rPeroxide_FlowMeter_2_kgh <= rPeroxide_FlowMeter_3_kgh) OR
          (rPeroxide_FlowMeter_2_kgh >= rPeroxide_FlowMeter_3_kgh AND rPeroxide_FlowMeter_2_kgh <= rPeroxide_FlowMeter_1_kgh) THEN
        rTempCalc4 := rPeroxide_FlowMeter_2_kgh;
    ELSE
        rTempCalc4 := rPeroxide_FlowMeter_3_kgh;
    END_IF;
    rHealth_Flow_Ch1_pct := 100.0;
    rHealth_Flow_Ch2_pct := 100.0;
    rHealth_Flow_Ch3_pct := 100.0;
ELSIF bFault_Flow_Ch1 AND (NOT bFault_Flow_Ch2) AND (NOT bFault_Flow_Ch3) THEN
    rTempCalc4 := 0.5 * (rPeroxide_FlowMeter_2_kgh + rPeroxide_FlowMeter_3_kgh);
    rHealth_Flow_Ch2_pct := 90.0;
    rHealth_Flow_Ch3_pct := 90.0;
ELSIF bFault_Flow_Ch2 AND (NOT bFault_Flow_Ch1) AND (NOT bFault_Flow_Ch3) THEN
    rTempCalc4 := 0.5 * (rPeroxide_FlowMeter_1_kgh + rPeroxide_FlowMeter_3_kgh);
    rHealth_Flow_Ch1_pct := 90.0;
    rHealth_Flow_Ch3_pct := 90.0;
ELSIF bFault_Flow_Ch3 AND (NOT bFault_Flow_Ch1) AND (NOT bFault_Flow_Ch2) THEN
    rTempCalc4 := 0.5 * (rPeroxide_FlowMeter_1_kgh + rPeroxide_FlowMeter_2_kgh);
    rHealth_Flow_Ch1_pct := 90.0;
    rHealth_Flow_Ch2_pct := 90.0;
ELSIF (NOT bFault_Flow_Ch1) AND bFault_Flow_Ch2 AND bFault_Flow_Ch3 THEN
    rTempCalc4 := rPeroxide_FlowMeter_1_kgh;
    rHealth_Flow_Ch1_pct := 45.0;
ELSIF (NOT bFault_Flow_Ch2) AND bFault_Flow_Ch1 AND bFault_Flow_Ch3 THEN
    rTempCalc4 := rPeroxide_FlowMeter_2_kgh;
    rHealth_Flow_Ch2_pct := 45.0;
ELSIF (NOT bFault_Flow_Ch3) AND bFault_Flow_Ch1 AND bFault_Flow_Ch2 THEN
    rTempCalc4 := rPeroxide_FlowMeter_3_kgh;
    rHealth_Flow_Ch3_pct := 45.0;
ELSE
    rTempCalc4 := 48.0; (* Conservative Default Feed Rate *)
END_IF;

rVoted_PeroxideFlow_kgh := rVoted_PeroxideFlow_kgh + 0.30 * (rTempCalc4 - rVoted_PeroxideFlow_kgh);


(* ---------------------------------------------------------------------------------------------- *)
(* CLUSTER 4: TUBE WALL ACOUSTIC EMISSION DECOMPOSITION PRECURSOR TRANSDUCERS [dB]               *)
(* ---------------------------------------------------------------------------------------------- *)
IF rAcoustic_Emission_1_dB < 0.0 OR rAcoustic_Emission_1_dB > 140.0 THEN
    bFault_Acoustic_Ch1 := TRUE;
    rHealth_Acoustic_Ch1_pct := 0.0;
END_IF;

IF rAcoustic_Emission_2_dB < 0.0 OR rAcoustic_Emission_2_dB > 140.0 THEN
    bFault_Acoustic_Ch2 := TRUE;
    rHealth_Acoustic_Ch2_pct := 0.0;
END_IF;

IF rAcoustic_Emission_3_dB < 0.0 OR rAcoustic_Emission_3_dB > 140.0 THEN
    bFault_Acoustic_Ch3 := TRUE;
    rHealth_Acoustic_Ch3_pct := 0.0;
END_IF;

rTempCalc1 := ABS(rAcoustic_Emission_1_dB - rAcoustic_Emission_2_dB);
rTempCalc2 := ABS(rAcoustic_Emission_2_dB - rAcoustic_Emission_3_dB);
rTempCalc3 := ABS(rAcoustic_Emission_3_dB - rAcoustic_Emission_1_dB);

IF (rTempCalc1 > rTMR_Acoustic_Tol_dB) OR (rTempCalc2 > rTMR_Acoustic_Tol_dB) OR (rTempCalc3 > rTMR_Acoustic_Tol_dB) THEN
    tTMR_Acoustic_DiscTimer_s := tTMR_Acoustic_DiscTimer_s + tScanCycleTime_s;
    IF tTMR_Acoustic_DiscTimer_s >= tTMR_Acoustic_TripDelay_s THEN
        IF (rTempCalc1 > rTMR_Acoustic_Tol_dB) AND (rTempCalc3 > rTMR_Acoustic_Tol_dB) THEN
            bFault_Acoustic_Ch1 := TRUE;
            rHealth_Acoustic_Ch1_pct := 10.0;
        ELSIF (rTempCalc1 > rTMR_Acoustic_Tol_dB) AND (rTempCalc2 > rTMR_Acoustic_Tol_dB) THEN
            bFault_Acoustic_Ch2 := TRUE;
            rHealth_Acoustic_Ch2_pct := 10.0;
        ELSIF (rTempCalc2 > rTMR_Acoustic_Tol_dB) AND (rTempCalc3 > rTMR_Acoustic_Tol_dB) THEN
            bFault_Acoustic_Ch3 := TRUE;
            rHealth_Acoustic_Ch3_pct := 10.0;
        END_IF;
    END_IF;
ELSE
    IF tTMR_Acoustic_DiscTimer_s > 0.0 THEN
        tTMR_Acoustic_DiscTimer_s := tTMR_Acoustic_DiscTimer_s - (tScanCycleTime_s * 2.0);
        IF tTMR_Acoustic_DiscTimer_s < 0.0 THEN
            tTMR_Acoustic_DiscTimer_s := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Acoustic Precursor Selection (Max-Select Conservative for Explosive Crack Precursors) *)
IF (NOT bFault_Acoustic_Ch1) AND (NOT bFault_Acoustic_Ch2) AND (NOT bFault_Acoustic_Ch3) THEN
    IF (rAcoustic_Emission_1_dB >= rAcoustic_Emission_2_dB AND rAcoustic_Emission_1_dB <= rAcoustic_Emission_3_dB) OR
       (rAcoustic_Emission_1_dB >= rAcoustic_Emission_3_dB AND rAcoustic_Emission_1_dB <= rAcoustic_Emission_2_dB) THEN
        rTempCalc4 := rAcoustic_Emission_1_dB;
    ELSIF (rAcoustic_Emission_2_dB >= rAcoustic_Emission_1_dB AND rAcoustic_Emission_2_dB <= rAcoustic_Emission_3_dB) OR
          (rAcoustic_Emission_2_dB >= rAcoustic_Emission_3_dB AND rAcoustic_Emission_2_dB <= rAcoustic_Emission_1_dB) THEN
        rTempCalc4 := rAcoustic_Emission_2_dB;
    ELSE
        rTempCalc4 := rAcoustic_Emission_3_dB;
    END_IF;
    rHealth_Acoustic_Ch1_pct := 100.0;
    rHealth_Acoustic_Ch2_pct := 100.0;
    rHealth_Acoustic_Ch3_pct := 100.0;
ELSIF bFault_Acoustic_Ch1 AND (NOT bFault_Acoustic_Ch2) AND (NOT bFault_Acoustic_Ch3) THEN
    IF rAcoustic_Emission_2_dB > rAcoustic_Emission_3_dB THEN
        rTempCalc4 := rAcoustic_Emission_2_dB;
    ELSE
        rTempCalc4 := rAcoustic_Emission_3_dB;
    END_IF;
    rHealth_Acoustic_Ch2_pct := 80.0;
    rHealth_Acoustic_Ch3_pct := 80.0;
ELSIF bFault_Acoustic_Ch2 AND (NOT bFault_Acoustic_Ch1) AND (NOT bFault_Acoustic_Ch3) THEN
    IF rAcoustic_Emission_1_dB > rAcoustic_Emission_3_dB THEN
        rTempCalc4 := rAcoustic_Emission_1_dB;
    ELSE
        rTempCalc4 := rAcoustic_Emission_3_dB;
    END_IF;
    rHealth_Acoustic_Ch1_pct := 80.0;
    rHealth_Acoustic_Ch3_pct := 80.0;
ELSIF bFault_Acoustic_Ch3 AND (NOT bFault_Acoustic_Ch1) AND (NOT bFault_Acoustic_Ch2) THEN
    IF rAcoustic_Emission_1_dB > rAcoustic_Emission_2_dB THEN
        rTempCalc4 := rAcoustic_Emission_1_dB;
    ELSE
        rTempCalc4 := rAcoustic_Emission_2_dB;
    END_IF;
    rHealth_Acoustic_Ch1_pct := 80.0;
    rHealth_Acoustic_Ch2_pct := 80.0;
ELSIF (NOT bFault_Acoustic_Ch1) AND bFault_Acoustic_Ch2 AND bFault_Acoustic_Ch3 THEN
    rTempCalc4 := rAcoustic_Emission_1_dB;
    rHealth_Acoustic_Ch1_pct := 35.0;
ELSIF (NOT bFault_Acoustic_Ch2) AND bFault_Acoustic_Ch1 AND bFault_Acoustic_Ch3 THEN
    rTempCalc4 := rAcoustic_Emission_2_dB;
    rHealth_Acoustic_Ch2_pct := 35.0;
ELSIF (NOT bFault_Acoustic_Ch3) AND bFault_Acoustic_Ch1 AND bFault_Acoustic_Ch2 THEN
    rTempCalc4 := rAcoustic_Emission_3_dB;
    rHealth_Acoustic_Ch3_pct := 35.0;
ELSE
    rTempCalc4 := 45.0; (* Conservative Default Background Noise *)
END_IF;

rVoted_AcousticEmission_dB := rVoted_AcousticEmission_dB + 0.50 * (rTempCalc4 - rVoted_AcousticEmission_dB);

(* Overall TMR Health Reliability Metric Across All 12 Transducers *)
rTMR_Health_Overall_pct := (
    rHealth_Press_Ch1_pct + rHealth_Press_Ch2_pct + rHealth_Press_Ch3_pct +
    rHealth_Temp_Ch1_pct  + rHealth_Temp_Ch2_pct  + rHealth_Temp_Ch3_pct  +
    rHealth_Flow_Ch1_pct  + rHealth_Flow_Ch2_pct  + rHealth_Flow_Ch3_pct  +
    rHealth_Acoustic_Ch1_pct + rHealth_Acoustic_Ch2_pct + rHealth_Acoustic_Ch3_pct
) / 12.0;

bTMR_DiscrepancyAlarm := bFault_Press_Ch1 OR bFault_Press_Ch2 OR bFault_Press_Ch3 OR
                         bFault_Temp_Ch1  OR bFault_Temp_Ch2  OR bFault_Temp_Ch3  OR
                         bFault_Flow_Ch1  OR bFault_Flow_Ch2  OR bFault_Flow_Ch3  OR
                         bFault_Acoustic_Ch1 OR bFault_Acoustic_Ch2 OR bFault_Acoustic_Ch3;
"""
