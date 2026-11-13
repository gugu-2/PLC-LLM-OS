# desal_builder/part3_tmr_voting.py
# Phase 1: 2oo3 Triple Modular Redundant Sensor Voting Suite

def get_part3_tmr_voting():
    return """
(* ====================================================================================================
   PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & FAULT-TOLERANT DEGRADATION ENGINE
   IEC 61508 / IEC 61511 SIL-2/3 Instrumentation Validation Suite
   Channels Supervised:
     1. PT-101 (A/B/C): Raw Seawater Intake Pressure [bar]
     2. PT-201 (A/B/C): High-Pressure Membrane Feed Header Pressure [bar]
     3. AT-301 (A/B/C): Combined Permeate Conductivity Analyzer [uS/cm]
     4. FT-401 (A/B/C): Isobaric ERD HP Brine Reject Flow [m3/h]
     5. AT-102 (A/B/C): Feed Dechlorination ORP Redox Analyzer [mV] (Polyamide Oxidation Guard)
     6. PT-501 (A/B/C): ERD PX Booster Pump Discharge Pressure [bar]
   ==================================================================================================== *)

(* ----------------------------------------------------------------------------------------------------
   CHANNEL GROUP 1: PT-101 RAW SEAWATER INTAKE PRESSURE [bar]
   Range: 0.0 to 10.0 [bar], Discrepancy Deviation Limit: 0.60 [bar], Debounce: 2.0 [s]
   ---------------------------------------------------------------------------------------------------- *)
(* Raw Range Checking (NAMUR NE-43 Compliance: 3.8 mA to 20.5 mA equivalent) *)
bHealthy_PT101A := (rPT_101A_IntakePressure_bar >= 0.10) AND (rPT_101A_IntakePressure_bar <= 9.50);
bHealthy_PT101B := (rPT_101B_IntakePressure_bar >= 0.10) AND (rPT_101B_IntakePressure_bar <= 9.50);
bHealthy_PT101C := (rPT_101C_IntakePressure_bar >= 0.10) AND (rPT_101C_IntakePressure_bar <= 9.50);

(* Pairwise Deviation Timers *)
IF ABS(rPT_101A_IntakePressure_bar - rPT_101B_IntakePressure_bar) > 0.60 THEN
    rTimer_PT101_AB_sec := rTimer_PT101_AB_sec + rCycleTime_sec;
ELSE
    rTimer_PT101_AB_sec := MAX(0.0, rTimer_PT101_AB_sec - (rCycleTime_sec * 2.0));
END_IF;

IF ABS(rPT_101B_IntakePressure_bar - rPT_101C_IntakePressure_bar) > 0.60 THEN
    rTimer_PT101_BC_sec := rTimer_PT101_BC_sec + rCycleTime_sec;
ELSE
    rTimer_PT101_BC_sec := MAX(0.0, rTimer_PT101_BC_sec - (rCycleTime_sec * 2.0));
END_IF;

IF ABS(rPT_101C_IntakePressure_bar - rPT_101A_IntakePressure_bar) > 0.60 THEN
    rTimer_PT101_CA_sec := rTimer_PT101_CA_sec + rCycleTime_sec;
ELSE
    rTimer_PT101_CA_sec := MAX(0.0, rTimer_PT101_CA_sec - (rCycleTime_sec * 2.0));
END_IF;

(* Identify Channel Discrepancies and Invalidate Discordant Transmitter *)
IF (rTimer_PT101_AB_sec >= 2.0) AND (rTimer_PT101_CA_sec >= 2.0) THEN
    bHealthy_PT101A := FALSE;
END_IF;
IF (rTimer_PT101_AB_sec >= 2.0) AND (rTimer_PT101_BC_sec >= 2.0) THEN
    bHealthy_PT101B := FALSE;
END_IF;
IF (rTimer_PT101_BC_sec >= 2.0) AND (rTimer_PT101_CA_sec >= 2.0) THEN
    bHealthy_PT101C := FALSE;
END_IF;

(* 2oo3 Voting Execution with Bumpless Degradation *)
IF bHealthy_PT101A AND bHealthy_PT101B AND bHealthy_PT101C THEN
    (* Full Triple Modular Healthy: Hardware Median Selection *)
    rVoted_PT101_IntakePress_bar := MAX(MIN(rPT_101A_IntakePressure_bar, rPT_101B_IntakePressure_bar),
                                        MIN(MAX(rPT_101A_IntakePressure_bar, rPT_101B_IntakePressure_bar), rPT_101C_IntakePressure_bar));
    bDiscrepancy_PT101 := FALSE;
    bDegraded_PT101 := FALSE;
ELSIF bHealthy_PT101A AND bHealthy_PT101B THEN
    rVoted_PT101_IntakePress_bar := (rPT_101A_IntakePressure_bar + rPT_101B_IntakePressure_bar) * 0.5;
    bDiscrepancy_PT101 := TRUE;
    bDegraded_PT101 := TRUE;
ELSIF bHealthy_PT101B AND bHealthy_PT101C THEN
    rVoted_PT101_IntakePress_bar := (rPT_101B_IntakePressure_bar + rPT_101C_IntakePressure_bar) * 0.5;
    bDiscrepancy_PT101 := TRUE;
    bDegraded_PT101 := TRUE;
ELSIF bHealthy_PT101C AND bHealthy_PT101A THEN
    rVoted_PT101_IntakePress_bar := (rPT_101C_IntakePressure_bar + rPT_101A_IntakePressure_bar) * 0.5;
    bDiscrepancy_PT101 := TRUE;
    bDegraded_PT101 := TRUE;
ELSIF bHealthy_PT101A THEN
    rVoted_PT101_IntakePress_bar := rPT_101A_IntakePressure_bar;
    bDiscrepancy_PT101 := TRUE;
    bDegraded_PT101 := TRUE;
ELSIF bHealthy_PT101B THEN
    rVoted_PT101_IntakePress_bar := rPT_101B_IntakePressure_bar;
    bDiscrepancy_PT101 := TRUE;
    bDegraded_PT101 := TRUE;
ELSIF bHealthy_PT101C THEN
    rVoted_PT101_IntakePress_bar := rPT_101C_IntakePressure_bar;
    bDiscrepancy_PT101 := TRUE;
    bDegraded_PT101 := TRUE;
ELSE
    (* All Three Channels Failed: Retain Previous Valid Sample & Assert Failure *)
    rVoted_PT101_IntakePress_bar := rVoted_PT101_Prev;
    bDiscrepancy_PT101 := TRUE;
    bDegraded_PT101 := TRUE;
END_IF;

(* Rate of Change Filter (Bumpless Protection: Max 1.0 bar/s) *)
rVoted_PT101_IntakePress_bar := rVoted_PT101_Prev + LIMIT(-0.010, rVoted_PT101_IntakePress_bar - rVoted_PT101_Prev, 0.010);
rVoted_PT101_Prev := rVoted_PT101_IntakePress_bar;

(* ----------------------------------------------------------------------------------------------------
   CHANNEL GROUP 2: PT-201 HIGH-PRESSURE MEMBRANE FEED HEADER PRESSURE [bar]
   Range: 0.0 to 100.0 [bar], Discrepancy Deviation Limit: 2.50 [bar], Debounce: 1.5 [s]
   ---------------------------------------------------------------------------------------------------- *)
bHealthy_PT201A := (rPT_201A_HpFeedPressure_bar >= 0.50) AND (rPT_201A_HpFeedPressure_bar <= 98.0);
bHealthy_PT201B := (rPT_201B_HpFeedPressure_bar >= 0.50) AND (rPT_201B_HpFeedPressure_bar <= 98.0);
bHealthy_PT201C := (rPT_201C_HpFeedPressure_bar >= 0.50) AND (rPT_201C_HpFeedPressure_bar <= 98.0);

IF ABS(rPT_201A_HpFeedPressure_bar - rPT_201B_HpFeedPressure_bar) > 2.50 THEN
    rTimer_PT201_AB_sec := rTimer_PT201_AB_sec + rCycleTime_sec;
ELSE
    rTimer_PT201_AB_sec := MAX(0.0, rTimer_PT201_AB_sec - (rCycleTime_sec * 2.0));
END_IF;

IF ABS(rPT_201B_HpFeedPressure_bar - rPT_201C_HpFeedPressure_bar) > 2.50 THEN
    rTimer_PT201_BC_sec := rTimer_PT201_BC_sec + rCycleTime_sec;
ELSE
    rTimer_PT201_BC_sec := MAX(0.0, rTimer_PT201_BC_sec - (rCycleTime_sec * 2.0));
END_IF;

IF ABS(rPT_201C_HpFeedPressure_bar - rPT_201A_HpFeedPressure_bar) > 2.50 THEN
    rTimer_PT201_CA_sec := rTimer_PT201_CA_sec + rCycleTime_sec;
ELSE
    rTimer_PT201_CA_sec := MAX(0.0, rTimer_PT201_CA_sec - (rCycleTime_sec * 2.0));
END_IF;

IF (rTimer_PT201_AB_sec >= 1.5) AND (rTimer_PT201_CA_sec >= 1.5) THEN
    bHealthy_PT201A := FALSE;
END_IF;
IF (rTimer_PT201_AB_sec >= 1.5) AND (rTimer_PT201_BC_sec >= 1.5) THEN
    bHealthy_PT201B := FALSE;
END_IF;
IF (rTimer_PT201_BC_sec >= 1.5) AND (rTimer_PT201_CA_sec >= 1.5) THEN
    bHealthy_PT201C := FALSE;
END_IF;

IF bHealthy_PT201A AND bHealthy_PT201B AND bHealthy_PT201C THEN
    rVoted_PT201_HpFeedPress_bar := MAX(MIN(rPT_201A_HpFeedPressure_bar, rPT_201B_HpFeedPressure_bar),
                                        MIN(MAX(rPT_201A_HpFeedPressure_bar, rPT_201B_HpFeedPressure_bar), rPT_201C_HpFeedPressure_bar));
    bDiscrepancy_PT201 := FALSE;
    bDegraded_PT201 := FALSE;
ELSIF bHealthy_PT201A AND bHealthy_PT201B THEN
    rVoted_PT201_HpFeedPress_bar := (rPT_201A_HpFeedPressure_bar + rPT_201B_HpFeedPressure_bar) * 0.5;
    bDiscrepancy_PT201 := TRUE;
    bDegraded_PT201 := TRUE;
ELSIF bHealthy_PT201B AND bHealthy_PT201C THEN
    rVoted_PT201_HpFeedPress_bar := (rPT_201B_HpFeedPressure_bar + rPT_201C_HpFeedPressure_bar) * 0.5;
    bDiscrepancy_PT201 := TRUE;
    bDegraded_PT201 := TRUE;
ELSIF bHealthy_PT201C AND bHealthy_PT201A THEN
    rVoted_PT201_HpFeedPress_bar := (rPT_201C_HpFeedPressure_bar + rPT_201A_HpFeedPressure_bar) * 0.5;
    bDiscrepancy_PT201 := TRUE;
    bDegraded_PT201 := TRUE;
ELSIF bHealthy_PT201A THEN
    rVoted_PT201_HpFeedPress_bar := rPT_201A_HpFeedPressure_bar;
    bDiscrepancy_PT201 := TRUE;
    bDegraded_PT201 := TRUE;
ELSIF bHealthy_PT201B THEN
    rVoted_PT201_HpFeedPress_bar := rPT_201B_HpFeedPressure_bar;
    bDiscrepancy_PT201 := TRUE;
    bDegraded_PT201 := TRUE;
ELSIF bHealthy_PT201C THEN
    rVoted_PT201_HpFeedPress_bar := rPT_201C_HpFeedPressure_bar;
    bDiscrepancy_PT201 := TRUE;
    bDegraded_PT201 := TRUE;
ELSE
    rVoted_PT201_HpFeedPress_bar := rVoted_PT201_Prev;
    bDiscrepancy_PT201 := TRUE;
    bDegraded_PT201 := TRUE;
END_IF;

(* Bumpless Slew Limiter: Max 2.5 bar/s *)
rVoted_PT201_HpFeedPress_bar := rVoted_PT201_Prev + LIMIT(-0.025, rVoted_PT201_HpFeedPress_bar - rVoted_PT201_Prev, 0.025);
rVoted_PT201_Prev := rVoted_PT201_HpFeedPress_bar;

(* ----------------------------------------------------------------------------------------------------
   CHANNEL GROUP 3: AT-301 COMBINED PERMEATE PRODUCT CONDUCTIVITY [uS/cm]
   Range: 0.0 to 2000.0 [uS/cm], Discrepancy Deviation Limit: 35.0 [uS/cm], Debounce: 3.0 [s]
   ---------------------------------------------------------------------------------------------------- *)
bHealthy_AT301A := (rAT_301A_PermConductivity_uS >= 5.0) AND (rAT_301A_PermConductivity_uS <= 1950.0);
bHealthy_AT301B := (rAT_301B_PermConductivity_uS >= 5.0) AND (rAT_301B_PermConductivity_uS <= 1950.0);
bHealthy_AT301C := (rAT_301C_PermConductivity_uS >= 5.0) AND (rAT_301C_PermConductivity_uS <= 1950.0);

IF ABS(rAT_301A_PermConductivity_uS - rAT_301B_PermConductivity_uS) > 35.0 THEN
    rTimer_AT301_AB_sec := rTimer_AT301_AB_sec + rCycleTime_sec;
ELSE
    rTimer_AT301_AB_sec := MAX(0.0, rTimer_AT301_AB_sec - (rCycleTime_sec * 2.0));
END_IF;

IF ABS(rAT_301B_PermConductivity_uS - rAT_301C_PermConductivity_uS) > 35.0 THEN
    rTimer_AT301_BC_sec := rTimer_AT301_BC_sec + rCycleTime_sec;
ELSE
    rTimer_AT301_BC_sec := MAX(0.0, rTimer_AT301_BC_sec - (rCycleTime_sec * 2.0));
END_IF;

IF ABS(rAT_301C_PermConductivity_uS - rAT_301A_PermConductivity_uS) > 35.0 THEN
    rTimer_AT301_CA_sec := rTimer_AT301_CA_sec + rCycleTime_sec;
ELSE
    rTimer_AT301_CA_sec := MAX(0.0, rTimer_AT301_CA_sec - (rCycleTime_sec * 2.0));
END_IF;

IF (rTimer_AT301_AB_sec >= 3.0) AND (rTimer_AT301_CA_sec >= 3.0) THEN
    bHealthy_AT301A := FALSE;
END_IF;
IF (rTimer_AT301_AB_sec >= 3.0) AND (rTimer_AT301_BC_sec >= 3.0) THEN
    bHealthy_AT301B := FALSE;
END_IF;
IF (rTimer_AT301_BC_sec >= 3.0) AND (rTimer_AT301_CA_sec >= 3.0) THEN
    bHealthy_AT301C := FALSE;
END_IF;

IF bHealthy_AT301A AND bHealthy_AT301B AND bHealthy_AT301C THEN
    rVoted_AT301_PermConduct_uS := MAX(MIN(rAT_301A_PermConductivity_uS, rAT_301B_PermConductivity_uS),
                                       MIN(MAX(rAT_301A_PermConductivity_uS, rAT_301B_PermConductivity_uS), rAT_301C_PermConductivity_uS));
    bDiscrepancy_AT301 := FALSE;
    bDegraded_AT301 := FALSE;
ELSIF bHealthy_AT301A AND bHealthy_AT301B THEN
    rVoted_AT301_PermConduct_uS := (rAT_301A_PermConductivity_uS + rAT_301B_PermConductivity_uS) * 0.5;
    bDiscrepancy_AT301 := TRUE;
    bDegraded_AT301 := TRUE;
ELSIF bHealthy_AT301B AND bHealthy_AT301C THEN
    rVoted_AT301_PermConduct_uS := (rAT_301B_PermConductivity_uS + rAT_301C_PermConductivity_uS) * 0.5;
    bDiscrepancy_AT301 := TRUE;
    bDegraded_AT301 := TRUE;
ELSIF bHealthy_AT301C AND bHealthy_AT301A THEN
    rVoted_AT301_PermConduct_uS := (rAT_301C_PermConductivity_uS + rAT_301A_PermConductivity_uS) * 0.5;
    bDiscrepancy_AT301 := TRUE;
    bDegraded_AT301 := TRUE;
ELSIF bHealthy_AT301A THEN
    rVoted_AT301_PermConduct_uS := rAT_301A_PermConductivity_uS;
    bDiscrepancy_AT301 := TRUE;
    bDegraded_AT301 := TRUE;
ELSIF bHealthy_AT301B THEN
    rVoted_AT301_PermConduct_uS := rAT_301B_PermConductivity_uS;
    bDiscrepancy_AT301 := TRUE;
    bDegraded_AT301 := TRUE;
ELSIF bHealthy_AT301C THEN
    rVoted_AT301_PermConduct_uS := rAT_301C_PermConductivity_uS;
    bDiscrepancy_AT301 := TRUE;
    bDegraded_AT301 := TRUE;
ELSE
    rVoted_AT301_PermConduct_uS := rVoted_AT301_Prev;
    bDiscrepancy_AT301 := TRUE;
    bDegraded_AT301 := TRUE;
END_IF;

(* Rate of Change Filter: Max 10.0 uS/cm/s *)
rVoted_AT301_PermConduct_uS := rVoted_AT301_Prev + LIMIT(-0.10, rVoted_AT301_PermConduct_uS - rVoted_AT301_Prev, 0.10);
rVoted_AT301_Prev := rVoted_AT301_PermConduct_uS;

(* ----------------------------------------------------------------------------------------------------
   CHANNEL GROUP 4: FT-401 ISOBARIC ERD HP BRINE REJECT FLOW [m3/h]
   Range: 0.0 to 5000.0 [m3/h], Discrepancy Deviation Limit: 120.0 [m3/h], Debounce: 2.0 [s]
   ---------------------------------------------------------------------------------------------------- *)
bHealthy_FT401A := (rFT_401A_ErdBrineFlow_m3h >= 10.0) AND (rFT_401A_ErdBrineFlow_m3h <= 4800.0);
bHealthy_FT401B := (rFT_401B_ErdBrineFlow_m3h >= 10.0) AND (rFT_401B_ErdBrineFlow_m3h <= 4800.0);
bHealthy_FT401C := (rFT_401C_ErdBrineFlow_m3h >= 10.0) AND (rFT_401C_ErdBrineFlow_m3h <= 4800.0);

IF ABS(rFT_401A_ErdBrineFlow_m3h - rFT_401B_ErdBrineFlow_m3h) > 120.0 THEN
    rTimer_FT401_AB_sec := rTimer_FT401_AB_sec + rCycleTime_sec;
ELSE
    rTimer_FT401_AB_sec := MAX(0.0, rTimer_FT401_AB_sec - (rCycleTime_sec * 2.0));
END_IF;

IF ABS(rFT_401B_ErdBrineFlow_m3h - rFT_401C_ErdBrineFlow_m3h) > 120.0 THEN
    rTimer_FT401_BC_sec := rTimer_FT401_BC_sec + rCycleTime_sec;
ELSE
    rTimer_FT401_BC_sec := MAX(0.0, rTimer_FT401_BC_sec - (rCycleTime_sec * 2.0));
END_IF;

IF ABS(rFT_401C_ErdBrineFlow_m3h - rFT_401A_ErdBrineFlow_m3h) > 120.0 THEN
    rTimer_FT401_CA_sec := rTimer_FT401_CA_sec + rCycleTime_sec;
ELSE
    rTimer_FT401_CA_sec := MAX(0.0, rTimer_FT401_CA_sec - (rCycleTime_sec * 2.0));
END_IF;

IF (rTimer_FT401_AB_sec >= 2.0) AND (rTimer_FT401_CA_sec >= 2.0) THEN
    bHealthy_FT401A := FALSE;
END_IF;
IF (rTimer_FT401_AB_sec >= 2.0) AND (rTimer_FT401_BC_sec >= 2.0) THEN
    bHealthy_FT401B := FALSE;
END_IF;
IF (rTimer_FT401_BC_sec >= 2.0) AND (rTimer_FT401_CA_sec >= 2.0) THEN
    bHealthy_FT401C := FALSE;
END_IF;

IF bHealthy_FT401A AND bHealthy_FT401B AND bHealthy_FT401C THEN
    rVoted_FT401_ErdBrineFlow_m3h := MAX(MIN(rFT_401A_ErdBrineFlow_m3h, rFT_401B_ErdBrineFlow_m3h),
                                         MIN(MAX(rFT_401A_ErdBrineFlow_m3h, rFT_401B_ErdBrineFlow_m3h), rFT_401C_ErdBrineFlow_m3h));
    bDiscrepancy_FT401 := FALSE;
    bDegraded_FT401 := FALSE;
ELSIF bHealthy_FT401A AND bHealthy_FT401B THEN
    rVoted_FT401_ErdBrineFlow_m3h := (rFT_401A_ErdBrineFlow_m3h + rFT_401B_ErdBrineFlow_m3h) * 0.5;
    bDiscrepancy_FT401 := TRUE;
    bDegraded_FT401 := TRUE;
ELSIF bHealthy_FT401B AND bHealthy_FT401C THEN
    rVoted_FT401_ErdBrineFlow_m3h := (rFT_401B_ErdBrineFlow_m3h + rFT_401C_ErdBrineFlow_m3h) * 0.5;
    bDiscrepancy_FT401 := TRUE;
    bDegraded_FT401 := TRUE;
ELSIF bHealthy_FT401C AND bHealthy_FT401A THEN
    rVoted_FT401_ErdBrineFlow_m3h := (rFT_401C_ErdBrineFlow_m3h + rFT_401A_ErdBrineFlow_m3h) * 0.5;
    bDiscrepancy_FT401 := TRUE;
    bDegraded_FT401 := TRUE;
ELSIF bHealthy_FT401A THEN
    rVoted_FT401_ErdBrineFlow_m3h := rFT_401A_ErdBrineFlow_m3h;
    bDiscrepancy_FT401 := TRUE;
    bDegraded_FT401 := TRUE;
ELSIF bHealthy_FT401B THEN
    rVoted_FT401_ErdBrineFlow_m3h := rFT_401B_ErdBrineFlow_m3h;
    bDiscrepancy_FT401 := TRUE;
    bDegraded_FT401 := TRUE;
ELSIF bHealthy_FT401C THEN
    rVoted_FT401_ErdBrineFlow_m3h := rFT_401C_ErdBrineFlow_m3h;
    bDiscrepancy_FT401 := TRUE;
    bDegraded_FT401 := TRUE;
ELSE
    rVoted_FT401_ErdBrineFlow_m3h := rVoted_FT401_Prev;
    bDiscrepancy_FT401 := TRUE;
    bDegraded_FT401 := TRUE;
END_IF;

(* Rate Filter: Max 50.0 m3/h/s *)
rVoted_FT401_ErdBrineFlow_m3h := rVoted_FT401_Prev + LIMIT(-0.50, rVoted_FT401_ErdBrineFlow_m3h - rVoted_FT401_Prev, 0.50);
rVoted_FT401_Prev := rVoted_FT401_ErdBrineFlow_m3h;

(* ----------------------------------------------------------------------------------------------------
   CHANNEL GROUP 5: AT-102 FEED DECHLORINATION REDOX ORP ANALYZER [mV]
   Range: -200.0 to +800.0 [mV], Discrepancy Deviation Limit: 30.0 [mV], Debounce: 1.0 [s]
   CRITICAL MEMBRANE OXIDATION SAFETY INTERLOCK (FREE CHLORINE DESTROYS POLYAMIDE SKIN)
   ---------------------------------------------------------------------------------------------------- *)
bHealthy_AT102A := (rAT_102A_FeedOrp_mV >= -180.0) AND (rAT_102A_FeedOrp_mV <= 750.0);
bHealthy_AT102B := (rAT_102B_FeedOrp_mV >= -180.0) AND (rAT_102B_FeedOrp_mV <= 750.0);
bHealthy_AT102C := (rAT_102C_FeedOrp_mV >= -180.0) AND (rAT_102C_FeedOrp_mV <= 750.0);

IF ABS(rAT_102A_FeedOrp_mV - rAT_102B_FeedOrp_mV) > 30.0 THEN
    rTimer_AT102_AB_sec := rTimer_AT102_AB_sec + rCycleTime_sec;
ELSE
    rTimer_AT102_AB_sec := MAX(0.0, rTimer_AT102_AB_sec - (rCycleTime_sec * 2.0));
END_IF;

IF ABS(rAT_102B_FeedOrp_mV - rAT_102C_FeedOrp_mV) > 30.0 THEN
    rTimer_AT102_BC_sec := rTimer_AT102_BC_sec + rCycleTime_sec;
ELSE
    rTimer_AT102_BC_sec := MAX(0.0, rTimer_AT102_BC_sec - (rCycleTime_sec * 2.0));
END_IF;

IF ABS(rAT_102C_FeedOrp_mV - rAT_102A_FeedOrp_mV) > 30.0 THEN
    rTimer_AT102_CA_sec := rTimer_AT102_CA_sec + rCycleTime_sec;
ELSE
    rTimer_AT102_CA_sec := MAX(0.0, rTimer_AT102_CA_sec - (rCycleTime_sec * 2.0));
END_IF;

IF (rTimer_AT102_AB_sec >= 1.0) AND (rTimer_AT102_CA_sec >= 1.0) THEN
    bHealthy_AT102A := FALSE;
END_IF;
IF (rTimer_AT102_AB_sec >= 1.0) AND (rTimer_AT102_BC_sec >= 1.0) THEN
    bHealthy_AT102B := FALSE;
END_IF;
IF (rTimer_AT102_BC_sec >= 1.0) AND (rTimer_AT102_CA_sec >= 1.0) THEN
    bHealthy_AT102C := FALSE;
END_IF;

(* For ORP Safety: When degraded, conservative selection takes the HIGHEST redox reading to prevent oxidizer sneak *)
IF bHealthy_AT102A AND bHealthy_AT102B AND bHealthy_AT102C THEN
    rVoted_AT102_FeedOrp_mV := MAX(MIN(rAT_102A_FeedOrp_mV, rAT_102B_FeedOrp_mV),
                                   MIN(MAX(rAT_102A_FeedOrp_mV, rAT_102B_FeedOrp_mV), rAT_102C_FeedOrp_mV));
    bDiscrepancy_AT102 := FALSE;
    bDegraded_AT102 := FALSE;
ELSIF bHealthy_AT102A AND bHealthy_AT102B THEN
    rVoted_AT102_FeedOrp_mV := MAX(rAT_102A_FeedOrp_mV, rAT_102B_FeedOrp_mV);
    bDiscrepancy_AT102 := TRUE;
    bDegraded_AT102 := TRUE;
ELSIF bHealthy_AT102B AND bHealthy_AT102C THEN
    rVoted_AT102_FeedOrp_mV := MAX(rAT_102B_FeedOrp_mV, rAT_102C_FeedOrp_mV);
    bDiscrepancy_AT102 := TRUE;
    bDegraded_AT102 := TRUE;
ELSIF bHealthy_AT102C AND bHealthy_AT102A THEN
    rVoted_AT102_FeedOrp_mV := MAX(rAT_102C_FeedOrp_mV, rAT_102A_FeedOrp_mV);
    bDiscrepancy_AT102 := TRUE;
    bDegraded_AT102 := TRUE;
ELSIF bHealthy_AT102A THEN
    rVoted_AT102_FeedOrp_mV := rAT_102A_FeedOrp_mV;
    bDiscrepancy_AT102 := TRUE;
    bDegraded_AT102 := TRUE;
ELSIF bHealthy_AT102B THEN
    rVoted_AT102_FeedOrp_mV := rAT_102B_FeedOrp_mV;
    bDiscrepancy_AT102 := TRUE;
    bDegraded_AT102 := TRUE;
ELSIF bHealthy_AT102C THEN
    rVoted_AT102_FeedOrp_mV := rAT_102C_FeedOrp_mV;
    bDiscrepancy_AT102 := TRUE;
    bDegraded_AT102 := TRUE;
ELSE
    rVoted_AT102_FeedOrp_mV := 350.0; (* Failsafe trip injection if all 3 ORP sensors fail *)
    bDiscrepancy_AT102 := TRUE;
    bDegraded_AT102 := TRUE;
END_IF;

(* Rate Filter: Max 15.0 mV/s *)
rVoted_AT102_FeedOrp_mV := rVoted_AT102_Prev + LIMIT(-0.15, rVoted_AT102_FeedOrp_mV - rVoted_AT102_Prev, 0.15);
rVoted_AT102_Prev := rVoted_AT102_FeedOrp_mV;

(* ----------------------------------------------------------------------------------------------------
   CHANNEL GROUP 6: PT-501 ERD PX BOOSTER PUMP DISCHARGE PRESSURE [bar]
   Range: 0.0 to 100.0 [bar], Discrepancy Deviation Limit: 2.00 [bar], Debounce: 1.5 [s]
   ---------------------------------------------------------------------------------------------------- *)
bHealthy_PT501A := (rPT_501A_PxDischargePress_bar >= 0.50) AND (rPT_501A_PxDischargePress_bar <= 98.0);
bHealthy_PT501B := (rPT_501B_PxDischargePress_bar >= 0.50) AND (rPT_501B_PxDischargePress_bar <= 98.0);
bHealthy_PT501C := (rPT_501C_PxDischargePress_bar >= 0.50) AND (rPT_501C_PxDischargePress_bar <= 98.0);

IF ABS(rPT_501A_PxDischargePress_bar - rPT_501B_PxDischargePress_bar) > 2.00 THEN
    rTimer_PT501_AB_sec := rTimer_PT501_AB_sec + rCycleTime_sec;
ELSE
    rTimer_PT501_AB_sec := MAX(0.0, rTimer_PT501_AB_sec - (rCycleTime_sec * 2.0));
END_IF;

IF ABS(rPT_501B_PxDischargePress_bar - rPT_501C_PxDischargePress_bar) > 2.00 THEN
    rTimer_PT501_BC_sec := rTimer_PT501_BC_sec + rCycleTime_sec;
ELSE
    rTimer_PT501_BC_sec := MAX(0.0, rTimer_PT501_BC_sec - (rCycleTime_sec * 2.0));
END_IF;

IF ABS(rPT_501C_PxDischargePress_bar - rPT_501A_PxDischargePress_bar) > 2.00 THEN
    rTimer_PT501_CA_sec := rTimer_PT501_CA_sec + rCycleTime_sec;
ELSE
    rTimer_PT501_CA_sec := MAX(0.0, rTimer_PT501_CA_sec - (rCycleTime_sec * 2.0));
END_IF;

IF (rTimer_PT501_AB_sec >= 1.5) AND (rTimer_PT501_CA_sec >= 1.5) THEN
    bHealthy_PT501A := FALSE;
END_IF;
IF (rTimer_PT501_AB_sec >= 1.5) AND (rTimer_PT501_BC_sec >= 1.5) THEN
    bHealthy_PT501B := FALSE;
END_IF;
IF (rTimer_PT501_BC_sec >= 1.5) AND (rTimer_PT501_CA_sec >= 1.5) THEN
    bHealthy_PT501C := FALSE;
END_IF;

IF bHealthy_PT501A AND bHealthy_PT501B AND bHealthy_PT501C THEN
    rVoted_PT501_PxDischPress_bar := MAX(MIN(rPT_501A_PxDischargePress_bar, rPT_501B_PxDischargePress_bar),
                                         MIN(MAX(rPT_501A_PxDischargePress_bar, rPT_501B_PxDischargePress_bar), rPT_501C_PxDischargePress_bar));
    bDiscrepancy_PT501 := FALSE;
    bDegraded_PT501 := FALSE;
ELSIF bHealthy_PT501A AND bHealthy_PT501B THEN
    rVoted_PT501_PxDischPress_bar := (rPT_501A_PxDischargePress_bar + rPT_501B_PxDischargePress_bar) * 0.5;
    bDiscrepancy_PT501 := TRUE;
    bDegraded_PT501 := TRUE;
ELSIF bHealthy_PT501B AND bHealthy_PT501C THEN
    rVoted_PT501_PxDischPress_bar := (rPT_501B_PxDischargePress_bar + rPT_501C_PxDischargePress_bar) * 0.5;
    bDiscrepancy_PT501 := TRUE;
    bDegraded_PT501 := TRUE;
ELSIF bHealthy_PT501C AND bHealthy_PT501A THEN
    rVoted_PT501_PxDischPress_bar := (rPT_501C_PxDischargePress_bar + rPT_501A_PxDischargePress_bar) * 0.5;
    bDiscrepancy_PT501 := TRUE;
    bDegraded_PT501 := TRUE;
ELSIF bHealthy_PT501A THEN
    rVoted_PT501_PxDischPress_bar := rPT_501A_PxDischargePress_bar;
    bDiscrepancy_PT501 := TRUE;
    bDegraded_PT501 := TRUE;
ELSIF bHealthy_PT501B THEN
    rVoted_PT501_PxDischPress_bar := rPT_501B_PxDischargePress_bar;
    bDiscrepancy_PT501 := TRUE;
    bDegraded_PT501 := TRUE;
ELSIF bHealthy_PT501C THEN
    rVoted_PT501_PxDischPress_bar := rPT_501C_PxDischargePress_bar;
    bDiscrepancy_PT501 := TRUE;
    bDegraded_PT501 := TRUE;
ELSE
    rVoted_PT501_PxDischPress_bar := rVoted_PT501_Prev;
    bDiscrepancy_PT501 := TRUE;
    bDegraded_PT501 := TRUE;
END_IF;

(* Rate Filter: Max 2.0 bar/s *)
rVoted_PT501_PxDischPress_bar := rVoted_PT501_Prev + LIMIT(-0.020, rVoted_PT501_PxDischPress_bar - rVoted_PT501_Prev, 0.020);
rVoted_PT501_Prev := rVoted_PT501_PxDischPress_bar;
"""
