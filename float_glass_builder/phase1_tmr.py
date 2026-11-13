# phase1_tmr.py for FB_Glass_FloatLine_TinBath_AnnealingLehr_ThicknessCooling

def generate_phase1():
    return """(*
 * =========================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DYNAMIC DISCREPANCY TIMERS
 * Comprehensive voting, fault isolation, and bumpless degradation across 4 critical sensor triples:
 *   1. Non-Contact Laser Optical Scanning Thickness Gauges (Thick1, Thick2, Thick3) [mm]
 *   2. Tin Bath Multi-Wavelength Optical Infrared Pyrometers (Pyro1, Pyro2, Pyro3) [deg C]
 *   3. Tin Bath Hermetic Protective Atmosphere Pressure Transmitters (Press1, Press2, Press3) [mbar]
 *   4. Lehr Cold-End Polarimetric Optical Stress Birefringence Transducers (Stress1, Stress2, Stress3) [nm/cm]
 * =========================================================================================================
 *)

(* ---------------------------------------------------------------------------------------------------------
 * 1. LASER OPTICAL SCANNING THICKNESS GAUGES 2oo3 TMR ENGINE
 * Nominal range: 1.50 mm to 22.00 mm. Discrepancy threshold: 0.080 mm (80 um).
 * --------------------------------------------------------------------------------------------------------- *)
(* Physical range validation *)
IF rLaserThick_Sensor1 < 1.00 OR rLaserThick_Sensor1 > 25.00 THEN
    bThick_Ch1_Valid := FALSE;
END_IF;
IF rLaserThick_Sensor2 < 1.00 OR rLaserThick_Sensor2 > 25.00 THEN
    bThick_Ch2_Valid := FALSE;
END_IF;
IF rLaserThick_Sensor3 < 1.00 OR rLaserThick_Sensor3 > 25.00 THEN
    bThick_Ch3_Valid := FALSE;
END_IF;

(* Calculate absolute inter-channel pairwise discrepancies *)
rDiff_Thick_12 := ABS(rLaserThick_Sensor1 - rLaserThick_Sensor2);
rDiff_Thick_23 := ABS(rLaserThick_Sensor2 - rLaserThick_Sensor3);
rDiff_Thick_13 := ABS(rLaserThick_Sensor1 - rLaserThick_Sensor3);

(* Pair 1-2 Discrepancy Integration Timer *)
IF rDiff_Thick_12 > rThick_DiscrepancyLimit_mm AND bThick_Ch1_Valid AND bThick_Ch2_Valid THEN
    rTimer_Thick_12 := rTimer_Thick_12 + rScanDeltaTime_sec;
ELSE
    rTimer_Thick_12 := MAX(0.0, rTimer_Thick_12 - (rScanDeltaTime_sec * 0.5));
END_IF;

(* Pair 2-3 Discrepancy Integration Timer *)
IF rDiff_Thick_23 > rThick_DiscrepancyLimit_mm AND bThick_Ch2_Valid AND bThick_Ch3_Valid THEN
    rTimer_Thick_23 := rTimer_Thick_23 + rScanDeltaTime_sec;
ELSE
    rTimer_Thick_23 := MAX(0.0, rTimer_Thick_23 - (rScanDeltaTime_sec * 0.5));
END_IF;

(* Pair 1-3 Discrepancy Integration Timer *)
IF rDiff_Thick_13 > rThick_DiscrepancyLimit_mm AND bThick_Ch1_Valid AND bThick_Ch3_Valid THEN
    rTimer_Thick_13 := rTimer_Thick_13 + rScanDeltaTime_sec;
ELSE
    rTimer_Thick_13 := MAX(0.0, rTimer_Thick_13 - (rScanDeltaTime_sec * 0.5));
END_IF;

(* Fault Isolation Logic: identify aberrant channel based on dual-pair timer expiration *)
IF rTimer_Thick_12 >= rThick_TimerLimit_sec AND rTimer_Thick_13 >= rThick_TimerLimit_sec THEN
    bThick_Ch1_Valid := FALSE; (* Channel 1 is the divergent outlier *)
END_IF;

IF rTimer_Thick_12 >= rThick_TimerLimit_sec AND rTimer_Thick_23 >= rThick_TimerLimit_sec THEN
    bThick_Ch2_Valid := FALSE; (* Channel 2 is the divergent outlier *)
END_IF;

IF rTimer_Thick_13 >= rThick_TimerLimit_sec AND rTimer_Thick_23 >= rThick_TimerLimit_sec THEN
    bThick_Ch3_Valid := FALSE; (* Channel 3 is the divergent outlier *)
END_IF;

(* Re-evaluate healthy channel count *)
nThick_HealthyChannels := 0;
IF bThick_Ch1_Valid THEN
    nThick_HealthyChannels := nThick_HealthyChannels + 1;
END_IF;
IF bThick_Ch2_Valid THEN
    nThick_HealthyChannels := nThick_HealthyChannels + 1;
END_IF;
IF bThick_Ch3_Valid THEN
    nThick_HealthyChannels := nThick_HealthyChannels + 1;
END_IF;

(* Execute Bumpless Voted Synthesis Based on Healthy Topology *)
IF nThick_HealthyChannels = 3 THEN
    (* Full 2oo3 TMR: Median Signal Selection *)
    nThick_VotingMode := 3;
    bAlarm_TMR_Degraded_Thick := FALSE;
    IF (rLaserThick_Sensor1 >= rLaserThick_Sensor2 AND rLaserThick_Sensor1 <= rLaserThick_Sensor3) OR
       (rLaserThick_Sensor1 >= rLaserThick_Sensor3 AND rLaserThick_Sensor1 <= rLaserThick_Sensor2) THEN
        rVotedThickness_mm := rLaserThick_Sensor1;
    ELSIF (rLaserThick_Sensor2 >= rLaserThick_Sensor1 AND rLaserThick_Sensor2 <= rLaserThick_Sensor3) OR
          (rLaserThick_Sensor2 >= rLaserThick_Sensor3 AND rLaserThick_Sensor2 <= rLaserThick_Sensor1) THEN
        rVotedThickness_mm := rLaserThick_Sensor2;
    ELSE
        rVotedThickness_mm := rLaserThick_Sensor3;
    END_IF;

ELSIF nThick_HealthyChannels = 2 THEN
    (* 1oo2 Degraded Mode: Arithmetic Mean of Remaining Valid Sensors *)
    nThick_VotingMode := 2;
    bAlarm_TMR_Degraded_Thick := TRUE;
    IF bThick_Ch1_Valid AND bThick_Ch2_Valid THEN
        rVotedThickness_mm := (rLaserThick_Sensor1 + rLaserThick_Sensor2) * 0.50;
    ELSIF bThick_Ch2_Valid AND bThick_Ch3_Valid THEN
        rVotedThickness_mm := (rLaserThick_Sensor2 + rLaserThick_Sensor3) * 0.50;
    ELSE
        rVotedThickness_mm := (rLaserThick_Sensor1 + rLaserThick_Sensor3) * 0.50;
    END_IF;

ELSIF nThick_HealthyChannels = 1 THEN
    (* 1oo1 Simplex Failover Mode: Single Surviving Sensor *)
    nThick_VotingMode := 1;
    bAlarm_TMR_Degraded_Thick := TRUE;
    IF bThick_Ch1_Valid THEN
        rVotedThickness_mm := rLaserThick_Sensor1;
    ELSIF bThick_Ch2_Valid THEN
        rVotedThickness_mm := rLaserThick_Sensor2;
    ELSE
        rVotedThickness_mm := rLaserThick_Sensor3;
    END_IF;

ELSE
    (* Zero Valid Channels: Critical Sensor Loss - Maintain Last Sane Estimate or Recipe Target *)
    nThick_VotingMode := 0;
    bAlarm_TMR_Degraded_Thick := TRUE;
    bAlarm_TMR_Trip_AllFailed := TRUE;
    IF rVotedThickness_mm < 1.00 OR rVotedThickness_mm > 25.00 THEN
        rVotedThickness_mm := rRecipeTargetThickness;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------
 * 2. TIN BATH ROOF MULTI-WAVELENGTH INFRARED PYROMETERS 2oo3 TMR ENGINE
 * Nominal range: 900.0 to 1150.0 deg C. Discrepancy threshold: 12.0 deg C.
 * --------------------------------------------------------------------------------------------------------- *)
(* Physical range validation *)
IF rPyrometer_Bath_Zone1 < 800.0 OR rPyrometer_Bath_Zone1 > 1250.0 THEN
    bPyro_Ch1_Valid := FALSE;
END_IF;
IF rPyrometer_Bath_Zone2 < 800.0 OR rPyrometer_Bath_Zone2 > 1250.0 THEN
    bPyro_Ch2_Valid := FALSE;
END_IF;
IF rPyrometer_Bath_Zone3 < 800.0 OR rPyrometer_Bath_Zone3 > 1250.0 THEN
    bPyro_Ch3_Valid := FALSE;
END_IF;

(* Inter-channel pairwise discrepancies *)
rDiff_Pyro_12 := ABS(rPyrometer_Bath_Zone1 - rPyrometer_Bath_Zone2);
rDiff_Pyro_23 := ABS(rPyrometer_Bath_Zone2 - rPyrometer_Bath_Zone3);
rDiff_Pyro_13 := ABS(rPyrometer_Bath_Zone1 - rPyrometer_Bath_Zone3);

(* Pair 1-2 Timer *)
IF rDiff_Pyro_12 > rPyro_DiscrepancyLimit_degC AND bPyro_Ch1_Valid AND bPyro_Ch2_Valid THEN
    rTimer_Pyro_12 := rTimer_Pyro_12 + rScanDeltaTime_sec;
ELSE
    rTimer_Pyro_12 := MAX(0.0, rTimer_Pyro_12 - (rScanDeltaTime_sec * 0.5));
END_IF;

(* Pair 2-3 Timer *)
IF rDiff_Pyro_23 > rPyro_DiscrepancyLimit_degC AND bPyro_Ch2_Valid AND bPyro_Ch3_Valid THEN
    rTimer_Pyro_23 := rTimer_Pyro_23 + rScanDeltaTime_sec;
ELSE
    rTimer_Pyro_23 := MAX(0.0, rTimer_Pyro_23 - (rScanDeltaTime_sec * 0.5));
END_IF;

(* Pair 1-3 Timer *)
IF rDiff_Pyro_13 > rPyro_DiscrepancyLimit_degC AND bPyro_Ch1_Valid AND bPyro_Ch3_Valid THEN
    rTimer_Pyro_13 := rTimer_Pyro_13 + rScanDeltaTime_sec;
ELSE
    rTimer_Pyro_13 := MAX(0.0, rTimer_Pyro_13 - (rScanDeltaTime_sec * 0.5));
END_IF;

(* Pyrometer fault isolation *)
IF rTimer_Pyro_12 >= rPyro_TimerLimit_sec AND rTimer_Pyro_13 >= rPyro_TimerLimit_sec THEN
    bPyro_Ch1_Valid := FALSE;
END_IF;

IF rTimer_Pyro_12 >= rPyro_TimerLimit_sec AND rTimer_Pyro_23 >= rPyro_TimerLimit_sec THEN
    bPyro_Ch2_Valid := FALSE;
END_IF;

IF rTimer_Pyro_13 >= rPyro_TimerLimit_sec AND rTimer_Pyro_23 >= rPyro_TimerLimit_sec THEN
    bPyro_Ch3_Valid := FALSE;
END_IF;

(* Count healthy pyrometers *)
nPyro_HealthyChannels := 0;
IF bPyro_Ch1_Valid THEN
    nPyro_HealthyChannels := nPyro_HealthyChannels + 1;
END_IF;
IF bPyro_Ch2_Valid THEN
    nPyro_HealthyChannels := nPyro_HealthyChannels + 1;
END_IF;
IF bPyro_Ch3_Valid THEN
    nPyro_HealthyChannels := nPyro_HealthyChannels + 1;
END_IF;

(* Pyrometer Voted Output Synthesis *)
IF nPyro_HealthyChannels = 3 THEN
    nPyro_VotingMode := 3;
    bAlarm_TMR_Degraded_Pyro := FALSE;
    IF (rPyrometer_Bath_Zone1 >= rPyrometer_Bath_Zone2 AND rPyrometer_Bath_Zone1 <= rPyrometer_Bath_Zone3) OR
       (rPyrometer_Bath_Zone1 >= rPyrometer_Bath_Zone3 AND rPyrometer_Bath_Zone1 <= rPyrometer_Bath_Zone2) THEN
        rVotedPyrometer_degC := rPyrometer_Bath_Zone1;
    ELSIF (rPyrometer_Bath_Zone2 >= rPyrometer_Bath_Zone1 AND rPyrometer_Bath_Zone2 <= rPyrometer_Bath_Zone3) OR
          (rPyrometer_Bath_Zone2 >= rPyrometer_Bath_Zone3 AND rPyrometer_Bath_Zone2 <= rPyrometer_Bath_Zone1) THEN
        rVotedPyrometer_degC := rPyrometer_Bath_Zone2;
    ELSE
        rVotedPyrometer_degC := rPyrometer_Bath_Zone3;
    END_IF;

ELSIF nPyro_HealthyChannels = 2 THEN
    nPyro_VotingMode := 2;
    bAlarm_TMR_Degraded_Pyro := TRUE;
    IF bPyro_Ch1_Valid AND bPyro_Ch2_Valid THEN
        rVotedPyrometer_degC := (rPyrometer_Bath_Zone1 + rPyrometer_Bath_Zone2) * 0.50;
    ELSIF bPyro_Ch2_Valid AND bPyro_Ch3_Valid THEN
        rVotedPyrometer_degC := (rPyrometer_Bath_Zone2 + rPyrometer_Bath_Zone3) * 0.50;
    ELSE
        rVotedPyrometer_degC := (rPyrometer_Bath_Zone1 + rPyrometer_Bath_Zone3) * 0.50;
    END_IF;

ELSIF nPyro_HealthyChannels = 1 THEN
    nPyro_VotingMode := 1;
    bAlarm_TMR_Degraded_Pyro := TRUE;
    IF bPyro_Ch1_Valid THEN
        rVotedPyrometer_degC := rPyrometer_Bath_Zone1;
    ELSIF bPyro_Ch2_Valid THEN
        rVotedPyrometer_degC := rPyrometer_Bath_Zone2;
    ELSE
        rVotedPyrometer_degC := rPyrometer_Bath_Zone3;
    END_IF;

ELSE
    nPyro_VotingMode := 0;
    bAlarm_TMR_Degraded_Pyro := TRUE;
    bAlarm_TMR_Trip_AllFailed := TRUE;
    IF rVotedPyrometer_degC < 800.0 OR rVotedPyrometer_degC > 1250.0 THEN
        rVotedPyrometer_degC := rRecipeTargetTinBathInletTemp;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------
 * 3. TIN BATH PROTECTIVE ATMOSPHERE PRESSURE TRANSMITTERS 2oo3 TMR ENGINE
 * Nominal range: +0.20 to +1.20 mbar. Discrepancy threshold: 0.12 mbar.
 * --------------------------------------------------------------------------------------------------------- *)
(* Physical range validation *)
IF rBathPress_Sensor1 < -0.50 OR rBathPress_Sensor1 > 3.00 THEN
    bPress_Ch1_Valid := FALSE;
END_IF;
IF rBathPress_Sensor2 < -0.50 OR rBathPress_Sensor2 > 3.00 THEN
    bPress_Ch2_Valid := FALSE;
END_IF;
IF rBathPress_Sensor3 < -0.50 OR rBathPress_Sensor3 > 3.00 THEN
    bPress_Ch3_Valid := FALSE;
END_IF;

(* Pressure pairwise discrepancies *)
rDiff_Press_12 := ABS(rBathPress_Sensor1 - rBathPress_Sensor2);
rDiff_Press_23 := ABS(rBathPress_Sensor2 - rBathPress_Sensor3);
rDiff_Press_13 := ABS(rBathPress_Sensor1 - rBathPress_Sensor3);

(* Pressure discrepancy timers *)
IF rDiff_Press_12 > rPress_DiscrepancyLimit_mbar AND bPress_Ch1_Valid AND bPress_Ch2_Valid THEN
    rTimer_Press_12 := rTimer_Press_12 + rScanDeltaTime_sec;
ELSE
    rTimer_Press_12 := MAX(0.0, rTimer_Press_12 - (rScanDeltaTime_sec * 0.5));
END_IF;

IF rDiff_Press_23 > rPress_DiscrepancyLimit_mbar AND bPress_Ch2_Valid AND bPress_Ch3_Valid THEN
    rTimer_Press_23 := rTimer_Press_23 + rScanDeltaTime_sec;
ELSE
    rTimer_Press_23 := MAX(0.0, rTimer_Press_23 - (rScanDeltaTime_sec * 0.5));
END_IF;

IF rDiff_Press_13 > rPress_DiscrepancyLimit_mbar AND bPress_Ch1_Valid AND bPress_Ch3_Valid THEN
    rTimer_Press_13 := rTimer_Press_13 + rScanDeltaTime_sec;
ELSE
    rTimer_Press_13 := MAX(0.0, rTimer_Press_13 - (rScanDeltaTime_sec * 0.5));
END_IF;

(* Pressure transmitter fault isolation *)
IF rTimer_Press_12 >= rPress_TimerLimit_sec AND rTimer_Press_13 >= rPress_TimerLimit_sec THEN
    bPress_Ch1_Valid := FALSE;
END_IF;

IF rTimer_Press_12 >= rPress_TimerLimit_sec AND rTimer_Press_23 >= rPress_TimerLimit_sec THEN
    bPress_Ch2_Valid := FALSE;
END_IF;

IF rTimer_Press_13 >= rPress_TimerLimit_sec AND rTimer_Press_23 >= rPress_TimerLimit_sec THEN
    bPress_Ch3_Valid := FALSE;
END_IF;

(* Count healthy pressure channels *)
nPress_HealthyChannels := 0;
IF bPress_Ch1_Valid THEN
    nPress_HealthyChannels := nPress_HealthyChannels + 1;
END_IF;
IF bPress_Ch2_Valid THEN
    nPress_HealthyChannels := nPress_HealthyChannels + 1;
END_IF;
IF bPress_Ch3_Valid THEN
    nPress_HealthyChannels := nPress_HealthyChannels + 1;
END_IF;

(* Pressure Voted Output Synthesis *)
IF nPress_HealthyChannels = 3 THEN
    nPress_VotingMode := 3;
    bAlarm_TMR_Degraded_Press := FALSE;
    IF (rBathPress_Sensor1 >= rBathPress_Sensor2 AND rBathPress_Sensor1 <= rBathPress_Sensor3) OR
       (rBathPress_Sensor1 >= rBathPress_Sensor3 AND rBathPress_Sensor1 <= rBathPress_Sensor2) THEN
        rVotedBathPress_mbar := rBathPress_Sensor1;
    ELSIF (rBathPress_Sensor2 >= rBathPress_Sensor1 AND rBathPress_Sensor2 <= rBathPress_Sensor3) OR
          (rBathPress_Sensor2 >= rBathPress_Sensor3 AND rBathPress_Sensor2 <= rBathPress_Sensor1) THEN
        rVotedBathPress_mbar := rBathPress_Sensor2;
    ELSE
        rVotedBathPress_mbar := rBathPress_Sensor3;
    END_IF;

ELSIF nPress_HealthyChannels = 2 THEN
    nPress_VotingMode := 2;
    bAlarm_TMR_Degraded_Press := TRUE;
    IF bPress_Ch1_Valid AND bPress_Ch2_Valid THEN
        rVotedBathPress_mbar := (rBathPress_Sensor1 + rBathPress_Sensor2) * 0.50;
    ELSIF bPress_Ch2_Valid AND bPress_Ch3_Valid THEN
        rVotedBathPress_mbar := (rBathPress_Sensor2 + rBathPress_Sensor3) * 0.50;
    ELSE
        rVotedBathPress_mbar := (rBathPress_Sensor1 + rBathPress_Sensor3) * 0.50;
    END_IF;

ELSIF nPress_HealthyChannels = 1 THEN
    nPress_VotingMode := 1;
    bAlarm_TMR_Degraded_Press := TRUE;
    IF bPress_Ch1_Valid THEN
        rVotedBathPress_mbar := rBathPress_Sensor1;
    ELSIF bPress_Ch2_Valid THEN
        rVotedBathPress_mbar := rBathPress_Sensor2;
    ELSE
        rVotedBathPress_mbar := rBathPress_Sensor3;
    END_IF;

ELSE
    nPress_VotingMode := 0;
    bAlarm_TMR_Degraded_Press := TRUE;
    bAlarm_TMR_Trip_AllFailed := TRUE;
    IF rVotedBathPress_mbar < -0.50 OR rVotedBathPress_mbar > 3.00 THEN
        rVotedBathPress_mbar := 0.45; (* Safe default positive overpressure bias *)
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------
 * 4. LEHR EXIT POLARIMETRIC OPTICAL STRESS BIREFRINGENCE SENSORS 2oo3 TMR ENGINE
 * Nominal range: 0.0 to 35.0 nm/cm. Discrepancy threshold: 6.0 nm/cm.
 * --------------------------------------------------------------------------------------------------------- *)
(* Physical range validation *)
IF rLehrStress_Sensor1 < -20.0 OR rLehrStress_Sensor1 > 100.0 THEN
    bStress_Ch1_Valid := FALSE;
END_IF;
IF rLehrStress_Sensor2 < -20.0 OR rLehrStress_Sensor2 > 100.0 THEN
    bStress_Ch2_Valid := FALSE;
END_IF;
IF rLehrStress_Sensor3 < -20.0 OR rLehrStress_Sensor3 > 100.0 THEN
    bStress_Ch3_Valid := FALSE;
END_IF;

(* Stress pairwise discrepancies *)
rDiff_Stress_12 := ABS(rLehrStress_Sensor1 - rLehrStress_Sensor2);
rDiff_Stress_23 := ABS(rLehrStress_Sensor2 - rLehrStress_Sensor3);
rDiff_Stress_13 := ABS(rLehrStress_Sensor1 - rLehrStress_Sensor3);

(* Stress discrepancy timers *)
IF rDiff_Stress_12 > rStress_DiscrepancyLimit_nm AND bStress_Ch1_Valid AND bStress_Ch2_Valid THEN
    rTimer_Stress_12 := rTimer_Stress_12 + rScanDeltaTime_sec;
ELSE
    rTimer_Stress_12 := MAX(0.0, rTimer_Stress_12 - (rScanDeltaTime_sec * 0.5));
END_IF;

IF rDiff_Stress_23 > rStress_DiscrepancyLimit_nm AND bStress_Ch2_Valid AND bStress_Ch3_Valid THEN
    rTimer_Stress_23 := rTimer_Stress_23 + rScanDeltaTime_sec;
ELSE
    rTimer_Stress_23 := MAX(0.0, rTimer_Stress_23 - (rScanDeltaTime_sec * 0.5));
END_IF;

IF rDiff_Stress_13 > rStress_DiscrepancyLimit_nm AND bStress_Ch1_Valid AND bStress_Ch3_Valid THEN
    rTimer_Stress_13 := rTimer_Stress_13 + rScanDeltaTime_sec;
ELSE
    rTimer_Stress_13 := MAX(0.0, rTimer_Stress_13 - (rScanDeltaTime_sec * 0.5));
END_IF;

(* Stress sensor fault isolation *)
IF rTimer_Stress_12 >= rStress_TimerLimit_sec AND rTimer_Stress_13 >= rStress_TimerLimit_sec THEN
    bStress_Ch1_Valid := FALSE;
END_IF;

IF rTimer_Stress_12 >= rStress_TimerLimit_sec AND rTimer_Stress_23 >= rStress_TimerLimit_sec THEN
    bStress_Ch2_Valid := FALSE;
END_IF;

IF rTimer_Stress_13 >= rStress_TimerLimit_sec AND rTimer_Stress_23 >= rStress_TimerLimit_sec THEN
    bStress_Ch3_Valid := FALSE;
END_IF;

(* Count healthy stress channels *)
nStress_HealthyChannels := 0;
IF bStress_Ch1_Valid THEN
    nStress_HealthyChannels := nStress_HealthyChannels + 1;
END_IF;
IF bStress_Ch2_Valid THEN
    nStress_HealthyChannels := nStress_HealthyChannels + 1;
END_IF;
IF bStress_Ch3_Valid THEN
    nStress_HealthyChannels := nStress_HealthyChannels + 1;
END_IF;

(* Stress Voted Output Synthesis *)
IF nStress_HealthyChannels = 3 THEN
    nStress_VotingMode := 3;
    bAlarm_TMR_Degraded_Stress := FALSE;
    IF (rLehrStress_Sensor1 >= rLehrStress_Sensor2 AND rLehrStress_Sensor1 <= rLehrStress_Sensor3) OR
       (rLehrStress_Sensor1 >= rLehrStress_Sensor3 AND rLehrStress_Sensor1 <= rLehrStress_Sensor2) THEN
        rVotedLehrStress_nm_cm := rLehrStress_Sensor1;
    ELSIF (rLehrStress_Sensor2 >= rLehrStress_Sensor1 AND rLehrStress_Sensor2 <= rLehrStress_Sensor3) OR
          (rLehrStress_Sensor2 >= rLehrStress_Sensor3 AND rLehrStress_Sensor2 <= rLehrStress_Sensor1) THEN
        rVotedLehrStress_nm_cm := rLehrStress_Sensor2;
    ELSE
        rVotedLehrStress_nm_cm := rLehrStress_Sensor3;
    END_IF;

ELSIF nStress_HealthyChannels = 2 THEN
    nStress_VotingMode := 2;
    bAlarm_TMR_Degraded_Stress := TRUE;
    IF bStress_Ch1_Valid AND bStress_Ch2_Valid THEN
        rVotedLehrStress_nm_cm := (rLehrStress_Sensor1 + rLehrStress_Sensor2) * 0.50;
    ELSIF bStress_Ch2_Valid AND bStress_Ch3_Valid THEN
        rVotedLehrStress_nm_cm := (rLehrStress_Sensor2 + rLehrStress_Sensor3) * 0.50;
    ELSE
        rVotedLehrStress_nm_cm := (rLehrStress_Sensor1 + rLehrStress_Sensor3) * 0.50;
    END_IF;

ELSIF nStress_HealthyChannels = 1 THEN
    nStress_VotingMode := 1;
    bAlarm_TMR_Degraded_Stress := TRUE;
    IF bStress_Ch1_Valid THEN
        rVotedLehrStress_nm_cm := rLehrStress_Sensor1;
    ELSIF bStress_Ch2_Valid THEN
        rVotedLehrStress_nm_cm := rLehrStress_Sensor2;
    ELSE
        rVotedLehrStress_nm_cm := rLehrStress_Sensor3;
    END_IF;

ELSE
    nStress_VotingMode := 0;
    bAlarm_TMR_Degraded_Stress := TRUE;
    bAlarm_TMR_Trip_AllFailed := TRUE;
    IF rVotedLehrStress_nm_cm < -20.0 OR rVotedLehrStress_nm_cm > 100.0 THEN
        rVotedLehrStress_nm_cm := 12.0; (* Safe fallback estimate *)
    END_IF;
END_IF;

(* Overall System Degradation Flag *)
IF nThick_VotingMode < 3 OR nPyro_VotingMode < 3 OR nPress_VotingMode < 3 OR nStress_VotingMode < 3 THEN
    bSystemDegraded := TRUE;
ELSE
    bSystemDegraded := FALSE;
END_IF;
"""

if __name__ == "__main__":
    s = generate_phase1()
    print(f"Phase 1 length: {len(s)} chars")
