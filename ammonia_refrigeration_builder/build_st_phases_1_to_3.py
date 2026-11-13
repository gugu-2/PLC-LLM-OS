# ammonia_refrigeration_builder/build_st_phases_1_to_3.py

def get_phases_1_to_3():
    return """(* ==================================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY FAULT ISOLATION                          *)
(* ==================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.1: 2oo3 VOTING - SUCTION HEADER PRESSURE (PT-101A/B/C) [bar]                                                      *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* Compute Median Value across 3 Analog Transmitters *)
rTMR_Suction_Median := MAX(MIN(PT_SUCTION_HDR_101A, PT_SUCTION_HDR_101B),
                           MIN(MAX(PT_SUCTION_HDR_101A, PT_SUCTION_HDR_101B), PT_SUCTION_HDR_101C));

(* Compute Absolute Deviations from Median *)
rTMR_Suction_DevA := ABS(PT_SUCTION_HDR_101A - rTMR_Suction_Median);
rTMR_Suction_DevB := ABS(PT_SUCTION_HDR_101B - rTMR_Suction_Median);
rTMR_Suction_DevC := ABS(PT_SUCTION_HDR_101C - rTMR_Suction_Median);

(* Channel A Discrepancy Accumulation Timer *)
IF rTMR_Suction_DevA > rDiscLimit_Suction_bar THEN
    rTMR_Suction_TimerA := rTMR_Suction_TimerA + rCycleTime_dt_sec;
    IF rTMR_Suction_TimerA >= rTMR_DiscrepancyTripTime_sec THEN
        bTMR_Suction_HealthyA := FALSE;
    END_IF;
ELSE
    rTMR_Suction_TimerA := MAX(0.0, rTMR_Suction_TimerA - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN
        bTMR_Suction_HealthyA := TRUE;
    END_IF;
END_IF;

(* Channel B Discrepancy Accumulation Timer *)
IF rTMR_Suction_DevB > rDiscLimit_Suction_bar THEN
    rTMR_Suction_TimerB := rTMR_Suction_TimerB + rCycleTime_dt_sec;
    IF rTMR_Suction_TimerB >= rTMR_DiscrepancyTripTime_sec THEN
        bTMR_Suction_HealthyB := FALSE;
    END_IF;
ELSE
    rTMR_Suction_TimerB := MAX(0.0, rTMR_Suction_TimerB - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN
        bTMR_Suction_HealthyB := TRUE;
    END_IF;
END_IF;

(* Channel C Discrepancy Accumulation Timer *)
IF rTMR_Suction_DevC > rDiscLimit_Suction_bar THEN
    rTMR_Suction_TimerC := rTMR_Suction_TimerC + rCycleTime_dt_sec;
    IF rTMR_Suction_TimerC >= rTMR_DiscrepancyTripTime_sec THEN
        bTMR_Suction_HealthyC := FALSE;
    END_IF;
ELSE
    rTMR_Suction_TimerC := MAX(0.0, rTMR_Suction_TimerC - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN
        bTMR_Suction_HealthyC := TRUE;
    END_IF;
END_IF;

(* Bumpless Degradation Voting Strategy *)
IF bTMR_Suction_HealthyA AND bTMR_Suction_HealthyB AND bTMR_Suction_HealthyC THEN
    rVoted_SuctionPressure_bar := rTMR_Suction_Median;
ELSIF bTMR_Suction_HealthyA AND bTMR_Suction_HealthyB THEN
    rVoted_SuctionPressure_bar := (PT_SUCTION_HDR_101A + PT_SUCTION_HDR_101B) * 0.50;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000001;
ELSIF bTMR_Suction_HealthyB AND bTMR_Suction_HealthyC THEN
    rVoted_SuctionPressure_bar := (PT_SUCTION_HDR_101B + PT_SUCTION_HDR_101C) * 0.50;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000001;
ELSIF bTMR_Suction_HealthyA AND bTMR_Suction_HealthyC THEN
    rVoted_SuctionPressure_bar := (PT_SUCTION_HDR_101A + PT_SUCTION_HDR_101C) * 0.50;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000001;
ELSIF bTMR_Suction_HealthyA THEN
    rVoted_SuctionPressure_bar := PT_SUCTION_HDR_101A;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000002;
ELSIF bTMR_Suction_HealthyB THEN
    rVoted_SuctionPressure_bar := PT_SUCTION_HDR_101B;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000002;
ELSIF bTMR_Suction_HealthyC THEN
    rVoted_SuctionPressure_bar := PT_SUCTION_HDR_101C;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000002;
ELSE
    rVoted_SuctionPressure_bar := rSet_SuctionPressure_Target_bar; (* Safe Fallback Target *)
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000001;   (* Trip on 3-Channel Loss *)
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.2: 2oo3 VOTING - COMPRESSOR DISCHARGE TEMPERATURE (TT-201A/B/C) [deg C]                                           *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rTMR_DischTemp_Median := MAX(MIN(TT_DISCHARGE_HDR_201A, TT_DISCHARGE_HDR_201B),
                             MIN(MAX(TT_DISCHARGE_HDR_201A, TT_DISCHARGE_HDR_201B), TT_DISCHARGE_HDR_201C));

rTMR_DischTemp_DevA := ABS(TT_DISCHARGE_HDR_201A - rTMR_DischTemp_Median);
rTMR_DischTemp_DevB := ABS(TT_DISCHARGE_HDR_201B - rTMR_DischTemp_Median);
rTMR_DischTemp_DevC := ABS(TT_DISCHARGE_HDR_201C - rTMR_DischTemp_Median);

IF rTMR_DischTemp_DevA > rDiscLimit_DischTemp_degC THEN
    rTMR_DischTemp_TimerA := rTMR_DischTemp_TimerA + rCycleTime_dt_sec;
    IF rTMR_DischTemp_TimerA >= rTMR_DiscrepancyTripTime_sec THEN
        bTMR_DischTemp_HealthyA := FALSE;
    END_IF;
ELSE
    rTMR_DischTemp_TimerA := MAX(0.0, rTMR_DischTemp_TimerA - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN
        bTMR_DischTemp_HealthyA := TRUE;
    END_IF;
END_IF;

IF rTMR_DischTemp_DevB > rDiscLimit_DischTemp_degC THEN
    rTMR_DischTemp_TimerB := rTMR_DischTemp_TimerB + rCycleTime_dt_sec;
    IF rTMR_DischTemp_TimerB >= rTMR_DiscrepancyTripTime_sec THEN
        bTMR_DischTemp_HealthyB := FALSE;
    END_IF;
ELSE
    rTMR_DischTemp_TimerB := MAX(0.0, rTMR_DischTemp_TimerB - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN
        bTMR_DischTemp_HealthyB := TRUE;
    END_IF;
END_IF;

IF rTMR_DischTemp_DevC > rDiscLimit_DischTemp_degC THEN
    rTMR_DischTemp_TimerC := rTMR_DischTemp_TimerC + rCycleTime_dt_sec;
    IF rTMR_DischTemp_TimerC >= rTMR_DiscrepancyTripTime_sec THEN
        bTMR_DischTemp_HealthyC := FALSE;
    END_IF;
ELSE
    rTMR_DischTemp_TimerC := MAX(0.0, rTMR_DischTemp_TimerC - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN
        bTMR_DischTemp_HealthyC := TRUE;
    END_IF;
END_IF;

IF bTMR_DischTemp_HealthyA AND bTMR_DischTemp_HealthyB AND bTMR_DischTemp_HealthyC THEN
    rVoted_DischargeTemp_degC := rTMR_DischTemp_Median;
ELSIF bTMR_DischTemp_HealthyA AND bTMR_DischTemp_HealthyB THEN
    rVoted_DischargeTemp_degC := (TT_DISCHARGE_HDR_201A + TT_DISCHARGE_HDR_201B) * 0.50;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000004;
ELSIF bTMR_DischTemp_HealthyB AND bTMR_DischTemp_HealthyC THEN
    rVoted_DischargeTemp_degC := (TT_DISCHARGE_HDR_201B + TT_DISCHARGE_HDR_201C) * 0.50;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000004;
ELSIF bTMR_DischTemp_HealthyA AND bTMR_DischTemp_HealthyC THEN
    rVoted_DischargeTemp_degC := (TT_DISCHARGE_HDR_201A + TT_DISCHARGE_HDR_201C) * 0.50;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000004;
ELSIF bTMR_DischTemp_HealthyA THEN
    rVoted_DischargeTemp_degC := TT_DISCHARGE_HDR_201A;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000008;
ELSIF bTMR_DischTemp_HealthyB THEN
    rVoted_DischargeTemp_degC := TT_DISCHARGE_HDR_201B;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000008;
ELSIF bTMR_DischTemp_HealthyC THEN
    rVoted_DischargeTemp_degC := TT_DISCHARGE_HDR_201C;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000008;
ELSE
    rVoted_DischargeTemp_degC := 95.0; (* Conservative High Safe Fallback *)
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000002;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.3: 2oo3 VOTING - OIL DIFFERENTIAL PRESSURE (PDT-301A/B/C) [bar]                                                    *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rTMR_OilDP_Median := MAX(MIN(PDT_OIL_DIFF_301A, PDT_OIL_DIFF_301B),
                         MIN(MAX(PDT_OIL_DIFF_301A, PDT_OIL_DIFF_301B), PDT_OIL_DIFF_301C));

rTMR_OilDP_DevA := ABS(PDT_OIL_DIFF_301A - rTMR_OilDP_Median);
rTMR_OilDP_DevB := ABS(PDT_OIL_DIFF_301B - rTMR_OilDP_Median);
rTMR_OilDP_DevC := ABS(PDT_OIL_DIFF_301C - rTMR_OilDP_Median);

IF rTMR_OilDP_DevA > rDiscLimit_OilDP_bar THEN
    rTMR_OilDP_TimerA := rTMR_OilDP_TimerA + rCycleTime_dt_sec;
    IF rTMR_OilDP_TimerA >= rTMR_DiscrepancyTripTime_sec THEN
        bTMR_OilDP_HealthyA := FALSE;
    END_IF;
ELSE
    rTMR_OilDP_TimerA := MAX(0.0, rTMR_OilDP_TimerA - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN
        bTMR_OilDP_HealthyA := TRUE;
    END_IF;
END_IF;

IF rTMR_OilDP_DevB > rDiscLimit_OilDP_bar THEN
    rTMR_OilDP_TimerB := rTMR_OilDP_TimerB + rCycleTime_dt_sec;
    IF rTMR_OilDP_TimerB >= rTMR_DiscrepancyTripTime_sec THEN
        bTMR_OilDP_HealthyB := FALSE;
    END_IF;
ELSE
    rTMR_OilDP_TimerB := MAX(0.0, rTMR_OilDP_TimerB - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN
        bTMR_OilDP_HealthyB := TRUE;
    END_IF;
END_IF;

IF rTMR_OilDP_DevC > rDiscLimit_OilDP_bar THEN
    rTMR_OilDP_TimerC := rTMR_OilDP_TimerC + rCycleTime_dt_sec;
    IF rTMR_OilDP_TimerC >= rTMR_DiscrepancyTripTime_sec THEN
        bTMR_OilDP_HealthyC := FALSE;
    END_IF;
ELSE
    rTMR_OilDP_TimerC := MAX(0.0, rTMR_OilDP_TimerC - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN
        bTMR_OilDP_HealthyC := TRUE;
    END_IF;
END_IF;

IF bTMR_OilDP_HealthyA AND bTMR_OilDP_HealthyB AND bTMR_OilDP_HealthyC THEN
    rVoted_OilDiffPressure_bar := rTMR_OilDP_Median;
ELSIF bTMR_OilDP_HealthyA AND bTMR_OilDP_HealthyB THEN
    rVoted_OilDiffPressure_bar := (PDT_OIL_DIFF_301A + PDT_OIL_DIFF_301B) * 0.50;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000010;
ELSIF bTMR_OilDP_HealthyB AND bTMR_OilDP_HealthyC THEN
    rVoted_OilDiffPressure_bar := (PDT_OIL_DIFF_301B + PDT_OIL_DIFF_301C) * 0.50;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000010;
ELSIF bTMR_OilDP_HealthyA AND bTMR_OilDP_HealthyC THEN
    rVoted_OilDiffPressure_bar := (PDT_OIL_DIFF_301A + PDT_OIL_DIFF_301C) * 0.50;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000010;
ELSIF bTMR_OilDP_HealthyA THEN
    rVoted_OilDiffPressure_bar := PDT_OIL_DIFF_301A;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000020;
ELSIF bTMR_OilDP_HealthyB THEN
    rVoted_OilDiffPressure_bar := PDT_OIL_DIFF_301B;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000020;
ELSIF bTMR_OilDP_HealthyC THEN
    rVoted_OilDiffPressure_bar := PDT_OIL_DIFF_301C;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000020;
ELSE
    rVoted_OilDiffPressure_bar := 0.0; (* Loss of Lube Oil Protection *)
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000004;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.4: 2oo3 VOTING - AMMONIA AMBIENT GAS DETECTORS (AT-401A/B/C) [ppm]                                                 *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rTMR_AmbientNH3_Median := MAX(MIN(AT_NH3_AMBIENT_401A, AT_NH3_AMBIENT_401B),
                              MIN(MAX(AT_NH3_AMBIENT_401A, AT_NH3_AMBIENT_401B), AT_NH3_AMBIENT_401C));

rTMR_AmbientNH3_DevA := ABS(AT_NH3_AMBIENT_401A - rTMR_AmbientNH3_Median);
rTMR_AmbientNH3_DevB := ABS(AT_NH3_AMBIENT_401B - rTMR_AmbientNH3_Median);
rTMR_AmbientNH3_DevC := ABS(AT_NH3_AMBIENT_401C - rTMR_AmbientNH3_Median);

IF rTMR_AmbientNH3_DevA > rDiscLimit_AmbientNH3_ppm THEN
    rTMR_AmbientNH3_TimerA := rTMR_AmbientNH3_TimerA + rCycleTime_dt_sec;
    IF rTMR_AmbientNH3_TimerA >= rTMR_DiscrepancyTripTime_sec THEN
        bTMR_AmbientNH3_HealthyA := FALSE;
    END_IF;
ELSE
    rTMR_AmbientNH3_TimerA := MAX(0.0, rTMR_AmbientNH3_TimerA - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN
        bTMR_AmbientNH3_HealthyA := TRUE;
    END_IF;
END_IF;

IF rTMR_AmbientNH3_DevB > rDiscLimit_AmbientNH3_ppm THEN
    rTMR_AmbientNH3_TimerB := rTMR_AmbientNH3_TimerB + rCycleTime_dt_sec;
    IF rTMR_AmbientNH3_TimerB >= rTMR_DiscrepancyTripTime_sec THEN
        bTMR_AmbientNH3_HealthyB := FALSE;
    END_IF;
ELSE
    rTMR_AmbientNH3_TimerB := MAX(0.0, rTMR_AmbientNH3_TimerB - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN
        bTMR_AmbientNH3_HealthyB := TRUE;
    END_IF;
END_IF;

IF rTMR_AmbientNH3_DevC > rDiscLimit_AmbientNH3_ppm THEN
    rTMR_AmbientNH3_TimerC := rTMR_AmbientNH3_TimerC + rCycleTime_dt_sec;
    IF rTMR_AmbientNH3_TimerC >= rTMR_DiscrepancyTripTime_sec THEN
        bTMR_AmbientNH3_HealthyC := FALSE;
    END_IF;
ELSE
    rTMR_AmbientNH3_TimerC := MAX(0.0, rTMR_AmbientNH3_TimerC - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN
        bTMR_AmbientNH3_HealthyC := TRUE;
    END_IF;
END_IF;

(* For Toxic Life Safety, take the Maximum of Healthy Channels for conservative fail-safe detection *)
IF bTMR_AmbientNH3_HealthyA AND bTMR_AmbientNH3_HealthyB AND bTMR_AmbientNH3_HealthyC THEN
    rVoted_AmbientNH3_ppm := MAX(rTMR_AmbientNH3_Median,
                                 (AT_NH3_AMBIENT_401A + AT_NH3_AMBIENT_401B + AT_NH3_AMBIENT_401C) / 3.0);
ELSIF bTMR_AmbientNH3_HealthyA AND bTMR_AmbientNH3_HealthyB THEN
    rVoted_AmbientNH3_ppm := MAX(AT_NH3_AMBIENT_401A, AT_NH3_AMBIENT_401B);
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000040;
ELSIF bTMR_AmbientNH3_HealthyB AND bTMR_AmbientNH3_HealthyC THEN
    rVoted_AmbientNH3_ppm := MAX(AT_NH3_AMBIENT_401B, AT_NH3_AMBIENT_401C);
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000040;
ELSIF bTMR_AmbientNH3_HealthyA AND bTMR_AmbientNH3_HealthyC THEN
    rVoted_AmbientNH3_ppm := MAX(AT_NH3_AMBIENT_401A, AT_NH3_AMBIENT_401C);
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000040;
ELSIF bTMR_AmbientNH3_HealthyA THEN
    rVoted_AmbientNH3_ppm := AT_NH3_AMBIENT_401A;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000080;
ELSIF bTMR_AmbientNH3_HealthyB THEN
    rVoted_AmbientNH3_ppm := AT_NH3_AMBIENT_401B;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000080;
ELSIF bTMR_AmbientNH3_HealthyC THEN
    rVoted_AmbientNH3_ppm := AT_NH3_AMBIENT_401C;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000080;
ELSE
    rVoted_AmbientNH3_ppm := 500.0; (* Trigger Immediate Scrubber on 3-Channel Sensor Failure *)
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000008;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.5: 2oo3 VOTING - ECONOMIZER INTERMEDIATE PRESSURE (PT-501A/B/C) [bar]                                              *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rTMR_EcoPres_Median := MAX(MIN(PT_ECONOMIZER_501A, PT_ECONOMIZER_501B),
                           MIN(MAX(PT_ECONOMIZER_501A, PT_ECONOMIZER_501B), PT_ECONOMIZER_501C));
rTMR_EcoPres_DevA := ABS(PT_ECONOMIZER_501A - rTMR_EcoPres_Median);
rTMR_EcoPres_DevB := ABS(PT_ECONOMIZER_501B - rTMR_EcoPres_Median);
rTMR_EcoPres_DevC := ABS(PT_ECONOMIZER_501C - rTMR_EcoPres_Median);

IF rTMR_EcoPres_DevA > rDiscLimit_EcoPres_bar THEN
    rTMR_EcoPres_TimerA := rTMR_EcoPres_TimerA + rCycleTime_dt_sec;
    IF rTMR_EcoPres_TimerA >= rTMR_DiscrepancyTripTime_sec THEN bTMR_EcoPres_HealthyA := FALSE; END_IF;
ELSE
    rTMR_EcoPres_TimerA := MAX(0.0, rTMR_EcoPres_TimerA - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN bTMR_EcoPres_HealthyA := TRUE; END_IF;
END_IF;

IF rTMR_EcoPres_DevB > rDiscLimit_EcoPres_bar THEN
    rTMR_EcoPres_TimerB := rTMR_EcoPres_TimerB + rCycleTime_dt_sec;
    IF rTMR_EcoPres_TimerB >= rTMR_DiscrepancyTripTime_sec THEN bTMR_EcoPres_HealthyB := FALSE; END_IF;
ELSE
    rTMR_EcoPres_TimerB := MAX(0.0, rTMR_EcoPres_TimerB - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN bTMR_EcoPres_HealthyB := TRUE; END_IF;
END_IF;

IF rTMR_EcoPres_DevC > rDiscLimit_EcoPres_bar THEN
    rTMR_EcoPres_TimerC := rTMR_EcoPres_TimerC + rCycleTime_dt_sec;
    IF rTMR_EcoPres_TimerC >= rTMR_DiscrepancyTripTime_sec THEN bTMR_EcoPres_HealthyC := FALSE; END_IF;
ELSE
    rTMR_EcoPres_TimerC := MAX(0.0, rTMR_EcoPres_TimerC - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN bTMR_EcoPres_HealthyC := TRUE; END_IF;
END_IF;

IF bTMR_EcoPres_HealthyA AND bTMR_EcoPres_HealthyB AND bTMR_EcoPres_HealthyC THEN
    rVoted_EconomizerPressure_bar := rTMR_EcoPres_Median;
ELSIF bTMR_EcoPres_HealthyA AND bTMR_EcoPres_HealthyB THEN
    rVoted_EconomizerPressure_bar := (PT_ECONOMIZER_501A + PT_ECONOMIZER_501B) * 0.50;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000100;
ELSIF bTMR_EcoPres_HealthyB AND bTMR_EcoPres_HealthyC THEN
    rVoted_EconomizerPressure_bar := (PT_ECONOMIZER_501B + PT_ECONOMIZER_501C) * 0.50;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000100;
ELSIF bTMR_EcoPres_HealthyA AND bTMR_EcoPres_HealthyC THEN
    rVoted_EconomizerPressure_bar := (PT_ECONOMIZER_501A + PT_ECONOMIZER_501C) * 0.50;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000100;
ELSE
    rVoted_EconomizerPressure_bar := rTMR_EcoPres_Median;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000200;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.6: 2oo3 VOTING - CONDENSER DISCHARGE PRESSURE (PT-601A/B/C) [bar]                                                  *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rTMR_CondPres_Median := MAX(MIN(PT_CONDENSER_DISCH_601A, PT_CONDENSER_DISCH_601B),
                            MIN(MAX(PT_CONDENSER_DISCH_601A, PT_CONDENSER_DISCH_601B), PT_CONDENSER_DISCH_601C));
rTMR_CondPres_DevA := ABS(PT_CONDENSER_DISCH_601A - rTMR_CondPres_Median);
rTMR_CondPres_DevB := ABS(PT_CONDENSER_DISCH_601B - rTMR_CondPres_Median);
rTMR_CondPres_DevC := ABS(PT_CONDENSER_DISCH_601C - rTMR_CondPres_Median);

IF rTMR_CondPres_DevA > rDiscLimit_CondPres_bar THEN
    rTMR_CondPres_TimerA := rTMR_CondPres_TimerA + rCycleTime_dt_sec;
    IF rTMR_CondPres_TimerA >= rTMR_DiscrepancyTripTime_sec THEN bTMR_CondPres_HealthyA := FALSE; END_IF;
ELSE
    rTMR_CondPres_TimerA := MAX(0.0, rTMR_CondPres_TimerA - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN bTMR_CondPres_HealthyA := TRUE; END_IF;
END_IF;

IF rTMR_CondPres_DevB > rDiscLimit_CondPres_bar THEN
    rTMR_CondPres_TimerB := rTMR_CondPres_TimerB + rCycleTime_dt_sec;
    IF rTMR_CondPres_TimerB >= rTMR_DiscrepancyTripTime_sec THEN bTMR_CondPres_HealthyB := FALSE; END_IF;
ELSE
    rTMR_CondPres_TimerB := MAX(0.0, rTMR_CondPres_TimerB - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN bTMR_CondPres_HealthyB := TRUE; END_IF;
END_IF;

IF rTMR_CondPres_DevC > rDiscLimit_CondPres_bar THEN
    rTMR_CondPres_TimerC := rTMR_CondPres_TimerC + rCycleTime_dt_sec;
    IF rTMR_CondPres_TimerC >= rTMR_DiscrepancyTripTime_sec THEN bTMR_CondPres_HealthyC := FALSE; END_IF;
ELSE
    rTMR_CondPres_TimerC := MAX(0.0, rTMR_CondPres_TimerC - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN bTMR_CondPres_HealthyC := TRUE; END_IF;
END_IF;

IF bTMR_CondPres_HealthyA AND bTMR_CondPres_HealthyB AND bTMR_CondPres_HealthyC THEN
    rVoted_CondenserPressure_bar := rTMR_CondPres_Median;
ELSIF bTMR_CondPres_HealthyA AND bTMR_CondPres_HealthyB THEN
    rVoted_CondenserPressure_bar := (PT_CONDENSER_DISCH_601A + PT_CONDENSER_DISCH_601B) * 0.50;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000400;
ELSIF bTMR_CondPres_HealthyB AND bTMR_CondPres_HealthyC THEN
    rVoted_CondenserPressure_bar := (PT_CONDENSER_DISCH_601B + PT_CONDENSER_DISCH_601C) * 0.50;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000400;
ELSIF bTMR_CondPres_HealthyA AND bTMR_CondPres_HealthyC THEN
    rVoted_CondenserPressure_bar := (PT_CONDENSER_DISCH_601A + PT_CONDENSER_DISCH_601C) * 0.50;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000400;
ELSIF bTMR_CondPres_HealthyA THEN
    rVoted_CondenserPressure_bar := PT_CONDENSER_DISCH_601A;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000800;
ELSIF bTMR_CondPres_HealthyB THEN
    rVoted_CondenserPressure_bar := PT_CONDENSER_DISCH_601B;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000800;
ELSIF bTMR_CondPres_HealthyC THEN
    rVoted_CondenserPressure_bar := PT_CONDENSER_DISCH_601C;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00000800;
ELSE
    rVoted_CondenserPressure_bar := 12.0; (* Safe Condensing Fallback *)
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000010;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.7: 2oo3 VOTING - AMBIENT PSYCHROMETRIC WET-BULB TEMPERATURE (TT-602A/B/C) [deg C]                                 *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rTMR_WetBulb_Median := MAX(MIN(TT_AMBIENT_WETBULB_602A, TT_AMBIENT_WETBULB_602B),
                           MIN(MAX(TT_AMBIENT_WETBULB_602A, TT_AMBIENT_WETBULB_602B), TT_AMBIENT_WETBULB_602C));
rTMR_WetBulb_DevA := ABS(TT_AMBIENT_WETBULB_602A - rTMR_WetBulb_Median);
rTMR_WetBulb_DevB := ABS(TT_AMBIENT_WETBULB_602B - rTMR_WetBulb_Median);
rTMR_WetBulb_DevC := ABS(TT_AMBIENT_WETBULB_602C - rTMR_WetBulb_Median);

IF rTMR_WetBulb_DevA > rDiscLimit_WetBulb_degC THEN
    rTMR_WetBulb_TimerA := rTMR_WetBulb_TimerA + rCycleTime_dt_sec;
    IF rTMR_WetBulb_TimerA >= rTMR_DiscrepancyTripTime_sec THEN bTMR_WetBulb_HealthyA := FALSE; END_IF;
ELSE
    rTMR_WetBulb_TimerA := MAX(0.0, rTMR_WetBulb_TimerA - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN bTMR_WetBulb_HealthyA := TRUE; END_IF;
END_IF;

IF rTMR_WetBulb_DevB > rDiscLimit_WetBulb_degC THEN
    rTMR_WetBulb_TimerB := rTMR_WetBulb_TimerB + rCycleTime_dt_sec;
    IF rTMR_WetBulb_TimerB >= rTMR_DiscrepancyTripTime_sec THEN bTMR_WetBulb_HealthyB := FALSE; END_IF;
ELSE
    rTMR_WetBulb_TimerB := MAX(0.0, rTMR_WetBulb_TimerB - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN bTMR_WetBulb_HealthyB := TRUE; END_IF;
END_IF;

IF rTMR_WetBulb_DevC > rDiscLimit_WetBulb_degC THEN
    rTMR_WetBulb_TimerC := rTMR_WetBulb_TimerC + rCycleTime_dt_sec;
    IF rTMR_WetBulb_TimerC >= rTMR_DiscrepancyTripTime_sec THEN bTMR_WetBulb_HealthyC := FALSE; END_IF;
ELSE
    rTMR_WetBulb_TimerC := MAX(0.0, rTMR_WetBulb_TimerC - (rCycleTime_dt_sec * 2.0));
    IF bAcknowledgeFaultReset THEN bTMR_WetBulb_HealthyC := TRUE; END_IF;
END_IF;

IF bTMR_WetBulb_HealthyA AND bTMR_WetBulb_HealthyB AND bTMR_WetBulb_HealthyC THEN
    rVoted_WetBulbTemp_degC := rTMR_WetBulb_Median;
ELSIF bTMR_WetBulb_HealthyA AND bTMR_WetBulb_HealthyB THEN
    rVoted_WetBulbTemp_degC := (TT_AMBIENT_WETBULB_602A + TT_AMBIENT_WETBULB_602B) * 0.50;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00001000;
ELSIF bTMR_WetBulb_HealthyB AND bTMR_WetBulb_HealthyC THEN
    rVoted_WetBulbTemp_degC := (TT_AMBIENT_WETBULB_602B + TT_AMBIENT_WETBULB_602C) * 0.50;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00001000;
ELSIF bTMR_WetBulb_HealthyA AND bTMR_WetBulb_HealthyC THEN
    rVoted_WetBulbTemp_degC := (TT_AMBIENT_WETBULB_602A + TT_AMBIENT_WETBULB_602C) * 0.50;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00001000;
ELSE
    rVoted_WetBulbTemp_degC := 20.0; (* Design Default Wet-Bulb *)
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#00002000;
END_IF;

(* ==================================================================================================================== *)
(* PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE OBSERVER & THERMODYNAMIC ENGINE                                  *)
(* ==================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 2.1: REAL-TIME ANHYDROUS AMMONIA (R717) SATURATION & CYCLE THERMODYNAMICS                                           *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* Polynomial approximation for R717 Saturation Temperature: Tsat_suct [deg C] vs Suction Pressure [bar abs] *)
rSuctionSatPressure_abs_bar := MAX(0.50, rVoted_SuctionPressure_bar);
rCalc_SuctionSaturationTemp_degC := -53.250 + (17.820 * rSuctionSatPressure_abs_bar) 
                                   - (2.150 * rSuctionSatPressure_abs_bar * rSuctionSatPressure_abs_bar)
                                   + (0.142 * rSuctionSatPressure_abs_bar * rSuctionSatPressure_abs_bar * rSuctionSatPressure_abs_bar);

(* Computed Suction Superheat [K] *)
rCalc_SuctionSuperheat_K := MAX(0.0, TT_SUCTION_ACCUMULATOR_GAS - rCalc_SuctionSaturationTemp_degC);

(* Polynomial approximation for R717 Condensing Saturation Temperature: Tsat_cond [deg C] vs Discharge Pressure [bar] *)
rCondSatPressure_abs_bar := MAX(5.00, rVoted_CondenserPressure_bar);
rCalc_CondensingSaturationTemp_degC := -15.400 + (5.120 * rCondSatPressure_abs_bar)
                                      - (0.125 * rCondSatPressure_abs_bar * rCondSatPressure_abs_bar)
                                      + (0.0018 * rCondSatPressure_abs_bar * rCondSatPressure_abs_bar * rCondSatPressure_abs_bar);

(* Operating Compression Ratio & Ideal Built-In Volume Ratio Vi *)
rCompPressureRatio := rCondSatPressure_abs_bar / rSuctionSatPressure_abs_bar;
(* Vi = (P_cond / P_suct) ^ (1 / 1.31) -> Vi = (rCompPressureRatio) ^ 0.763 *)
rOptimumVi_Ratio := 0.763 * rCompPressureRatio + 0.35; (* Linear approximation around nominal design operating point *)
rOptimumVi_Ratio := LIMIT(2.20, rOptimumVi_Ratio, 5.00);

(* Ideal Gas Suction Vapor Density [kg/m3] *)
rSuctionVaporDensity_kg_m3 := (rSuctionSatPressure_abs_bar * 100.0) / 
                              (rNH3_GasGasConstant_R * (TT_SUCTION_ACCUMULATOR_GAS + 273.15));
rSuctionVaporDensity_kg_m3 := LIMIT(0.50, rSuctionVaporDensity_kg_m3, 5.00);

(* Total Rack Swept Volume Displacement [m3/h] *)
rCompressorTotalFlow_m3_h := (1250.0 * (rComp1_SlideValve_Feedback * 0.01) * (rComp1_VFD_ActualSpeed_Hz / 50.0));
IF bComp2_RunningFeedback THEN
    rCompressorTotalFlow_m3_h := rCompressorTotalFlow_m3_h + (1650.0 * (rComp2_SlideValve_Feedback * 0.01));
END_IF;
IF bComp3_RunningFeedback THEN
    rCompressorTotalFlow_m3_h := rCompressorTotalFlow_m3_h + (1650.0 * (rComp3_SlideValve_Feedback * 0.01));
END_IF;

(* Ammonia Mass Flow Rate [kg/s] *)
rRefrigerantMassFlow_kg_s := (rCompressorTotalFlow_m3_h / 3600.0) * rSuctionVaporDensity_kg_m3 * rIsentropicEfficiency_eta;

(* Estimated Thermal Capacity [kW] and Tonnage [TR] *)
rCalc_TotalThermalCapacity_kW := rRefrigerantMassFlow_kg_s * rNH3_LatentHeat_hfg_kJ_kg;
rRefrigerationTonnage_TR := rCalc_TotalThermalCapacity_kW / 3.51685;

(* Estimated Total Compressor Electrical Power Draw [kW] *)
rCompressorNetPower_kW := (rRefrigerantMassFlow_kg_s * rNH3_GasGasConstant_R * (TT_SUCTION_ACCUMULATOR_GAS + 273.15) * 
                           (rNH3_IsentropicExponent_k / (rNH3_IsentropicExponent_k - 1.0)) * 
                           ((rCompPressureRatio * 0.2366) + 0.05)) / (rIsentropicEfficiency_eta * rMechanicalEfficiency_eta);
rCalc_TotalElectricalPower_kW := MAX(45.0, rCompressorNetPower_kW);

(* Real-Time Coefficient of Performance (COP) & Specific Power [kW/TR] *)
rCalc_CoefficientOfPerformance_COP := rCalc_TotalThermalCapacity_kW / MAX(1.0, rCalc_TotalElectricalPower_kW);
rCalc_SpecificPower_kW_per_TR := 3.51685 / MAX(0.10, rCalc_CoefficientOfPerformance_COP);

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 2.2: KALMAN OBSERVER INNOVATION UPDATE & DISCRETE STATE RECONSTRUCTION                                               *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* Formulate Measurement Vector y_meas *)
vecY_meas[1] := rVoted_SuctionPressure_bar;
vecY_meas[2] := 1420.0 + (rCalc_SuctionSuperheat_K * 2.50); (* Enthalpy kJ/kg *)
vecY_meas[3] := rVoted_CondenserPressure_bar;
vecY_meas[4] := rVoted_DischargeTemp_degC;
vecY_meas[5] := TT_OIL_SEPARATOR_SUMP;
vecY_meas[6] := rVoted_EconomizerPressure_bar;
vecY_meas[7] := TT_CONDENSER_SUMP_WATER;
vecY_meas[8] := rCalc_SuctionSuperheat_K;

(* Predict Measurement Output y_pred = C * vecX *)
FOR idxRow := 1 TO 8 DO
    rTempSum := 0.0;
    FOR idxCol := 1 TO 8 DO
        rTempSum := rTempSum + (matC[idxRow, idxCol] * vecX[idxCol]);
    END_FOR;
    vecY_pred[idxRow] := rTempSum;
    vecY_innov[idxRow] := vecY_meas[idxRow] - vecY_pred[idxRow];
END_FOR;

(* Correct States with Observer Kalman Innovation: vecX_hat = vecX + K * vecY_innov *)
FOR idxRow := 1 TO 8 DO
    rTempSum := 0.0;
    FOR idxCol := 1 TO 8 DO
        rTempSum := rTempSum + (matK[idxRow, idxCol] * vecY_innov[idxCol]);
    END_FOR;
    vecX_hat[idxRow] := vecX[idxRow] + rTempSum;
END_FOR;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 2.3: DISCRETE STATE PROPAGATION: vecX_next = A * vecX_hat + B * vecU + Ew * vecW                                      *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* Disturbance Vector Assignment *)
vecW[1] := rVoted_WetBulbTemp_degC - 18.0; (* Wet-bulb deviation from 18 deg C design *)
vecW[2] := (rVoted_SuctionPressure_bar - rSet_SuctionPressure_Target_bar) * 120.0; (* Thermal load disturbance *)
IF iFSM_State = FSM_STATE_DEFROST_HOT_GAS_FEED THEN
    vecW[3] := 0.45; (* 0.45 kg/s hot gas diverted *)
ELSE
    vecW[3] := 0.0;
END_IF;

(* Propagate Internal Dynamics *)
FOR idxRow := 1 TO 8 DO
    rTempSum := 0.0;
    (* State transition contribution *)
    FOR idxCol := 1 TO 8 DO
        rTempSum := rTempSum + (matA[idxRow, idxCol] * vecX_hat[idxCol]);
    END_FOR;
    (* Control input contribution *)
    FOR idxCol := 1 TO 6 DO
        rTempSum := rTempSum + (matB[idxRow, idxCol] * vecU[idxCol]);
    END_FOR;
    (* Exogenous disturbance contribution *)
    FOR idxCol := 1 TO 3 DO
        rTempSum := rTempSum + (matEw[idxRow, idxCol] * vecW[idxCol]);
    END_FOR;
    vecX_next[idxRow] := rTempSum;
END_FOR;

(* Update State Vector for Next Cycle *)
FOR idxRow := 1 TO 8 DO
    vecX[idxRow] := vecX_next[idxRow];
END_FOR;

(* ==================================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION WITH PROJECTED GRADIENT DESCENT (PGD)         *)
(* ==================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 3.1: DYNAMIC REFERENCE TARGET ASSIGNMENT                                                                             *)
(* -------------------------------------------------------------------------------------------------------------------- *)
vecR[1] := rSet_SuctionPressure_Target_bar;
vecR[2] := 1425.0; (* Target Enthalpy kJ/kg *)

(* Dynamic Floating Head Target: Track Wet-Bulb + Approach with Safety Floor *)
rTargetFloatingCondTemp := rVoted_WetBulbTemp_degC + rSet_FloatingHead_Approach_degC;
(* Invert polynomial to estimate target condensing pressure *)
rCalc_FloatingHeadTarget_bar := 0.0035 * (rTargetFloatingCondTemp * rTargetFloatingCondTemp) + 
                                (0.285 * rTargetFloatingCondTemp) + 5.20;
rCalc_FloatingHeadTarget_bar := LIMIT(rSet_MinDischargePressure_bar, rCalc_FloatingHeadTarget_bar, rSet_MaxDischargePressure_bar);
vecR[3] := rCalc_FloatingHeadTarget_bar;

vecR[4] := 80.0;                      (* Target Discharge Gas Temp: 80.0 deg C *)
vecR[5] := rSet_TargetOilTemp_degC;   (* Target Oil Sump Temp: 48.0 deg C *)
(* Optimum Economizer Pressure: Geometric Mean P_eco = sqrt(P_s * P_d) *)
vecR[6] := SQRT(MAX(1.0, vecR[1] * vecR[3]));
vecR[7] := rVoted_WetBulbTemp_degC + 2.0; (* Condenser basin target *)
vecR[8] := 4.0;                       (* Target Suction Superheat: 4.0 K *)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 3.2: PROJECTED GRADIENT DESCENT (PGD) MULTI-ITERATION SOLVER                                                         *)
(* Quadratic Cost: J = (x[k+1]-r)^T Q (x[k+1]-r) + u^T R u + Delta_u^T S Delta_u + x_N^T P x_N                          *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* Initialize Optimization Actuator Vector to Current Commands *)
FOR idxRow := 1 TO 6 DO
    vecU_opt[idxRow] := vecU[idxRow];
END_FOR;

(* Execute 6 PGD Iteration Cycles *)
FOR iPgdIteration := 1 TO 6 DO
    (* Step A: Predict 1-step Ahead State from Candidate u_opt *)
    FOR idxRow := 1 TO 8 DO
        rTempSum := 0.0;
        FOR idxCol := 1 TO 8 DO
            rTempSum := rTempSum + (matA[idxRow, idxCol] * vecX[idxCol]);
        END_FOR;
        FOR idxCol := 1 TO 6 DO
            rTempSum := rTempSum + (matB[idxRow, idxCol] * vecU_opt[idxCol]);
        END_FOR;
        FOR idxCol := 1 TO 3 DO
            rTempSum := rTempSum + (matEw[idxRow, idxCol] * vecW[idxCol]);
        END_FOR;
        vecX_next[idxRow] := rTempSum;
    END_FOR;

    (* Step B: Compute Cost Gradient Grad_J = 2*B^T * Q * (x_next - r) + 2*R * u_opt + 2*S * (u_opt - u_prev) *)
    FOR idxCol := 1 TO 6 DO
        rTempSum := 0.0;
        (* State Error Backpropagation through B^T * Q *)
        FOR idxRow := 1 TO 8 DO
            rTempSum := rTempSum + (matB[idxRow, idxCol] * matQ[idxRow, idxRow] * (vecX_next[idxRow] - vecR[idxRow]));
        END_FOR;
        rTempSum := 2.0 * rTempSum;

        (* Actuator Effort Penalty Gradient *)
        rTempSum := rTempSum + (2.0 * matR[idxCol, idxCol] * vecU_opt[idxCol]);

        (* Slew Rate Penalty Gradient *)
        rTempSum := rTempSum + (2.0 * matS[idxCol, idxCol] * (vecU_opt[idxCol] - vecU_prev[idxCol]));

        vecGradJ[idxCol] := rTempSum;
    END_FOR;

    (* Step C: Descend Along Negative Gradient with Projection & Slew Clamping *)
    FOR idxCol := 1 TO 6 DO
        rGradStep := vecU_opt[idxCol] - (rMpcStepSize_alpha * vecGradJ[idxCol]);

        (* Physical Saturation Box Bounds [vecU_min .. vecU_max] *)
        rGradStep := LIMIT(vecU_min[idxCol], rGradStep, vecU_max[idxCol]);

        (* Dynamic Slew Rate Clamping *)
        rSlewLimit_dt := vecSlew_max[idxCol] * rCycleTime_dt_sec * 10.0;
        rDeltaU_Clamped := LIMIT(-rSlewLimit_dt, (rGradStep - vecU_prev[idxCol]), rSlewLimit_dt);
        vecU_opt[idxCol] := vecU_prev[idxCol] + rDeltaU_Clamped;
    END_FOR;
END_FOR;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 3.3: UPDATE CONTROLS & STORE PREVIOUS CYCLE VECTOR                                                                   *)
(* -------------------------------------------------------------------------------------------------------------------- *)
FOR idxRow := 1 TO 6 DO
    vecDeltaU[idxRow] := vecU_opt[idxRow] - vecU[idxRow];
    vecU_prev[idxRow] := vecU[idxRow];
    vecU[idxRow] := vecU_opt[idxRow];
END_FOR;
"""
