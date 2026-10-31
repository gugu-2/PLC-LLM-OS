# cz_builder/cz_phase1.py

def get_phase1():
    return """(* === PHASE 1: 2oo3 TMR SENSOR VOTING === *)
(* Implements deterministic 3-channel median voting, pairwise discrepancy checks,          *)
(* bumpless failover to 1oo2 averaging, and individual sensor degradation latching.        *)

(* 1.1 Melt Surface Two-Color Optical Pyrometer 2oo3 Voting (Tolerance: 6.0 deg C) *)
bMeltTemp_Dev_1_2 := ABS(rMeltTempPyrometer_DegC_Ch1 - rMeltTempPyrometer_DegC_Ch2) > 6.0;
bMeltTemp_Dev_2_3 := ABS(rMeltTempPyrometer_DegC_Ch2 - rMeltTempPyrometer_DegC_Ch3) > 6.0;
bMeltTemp_Dev_1_3 := ABS(rMeltTempPyrometer_DegC_Ch1 - rMeltTempPyrometer_DegC_Ch3) > 6.0;

IF bMeltTemp_Dev_1_2 AND bMeltTemp_Dev_1_3 THEN
    bMeltTemp_Ch1_Fault := TRUE;
END_IF;
IF bMeltTemp_Dev_1_2 AND bMeltTemp_Dev_2_3 THEN
    bMeltTemp_Ch2_Fault := TRUE;
END_IF;
IF bMeltTemp_Dev_1_3 AND bMeltTemp_Dev_2_3 THEN
    bMeltTemp_Ch3_Fault := TRUE;
END_IF;

bMeltTemp_Degraded_1oo2 := bMeltTemp_Ch1_Fault OR bMeltTemp_Ch2_Fault OR bMeltTemp_Ch3_Fault;

IF NOT bMeltTemp_Degraded_1oo2 THEN
    (* Healthy 3-channel median selection *)
    IF (rMeltTempPyrometer_DegC_Ch1 >= rMeltTempPyrometer_DegC_Ch2 AND rMeltTempPyrometer_DegC_Ch1 <= rMeltTempPyrometer_DegC_Ch3) OR
       (rMeltTempPyrometer_DegC_Ch1 <= rMeltTempPyrometer_DegC_Ch2 AND rMeltTempPyrometer_DegC_Ch1 >= rMeltTempPyrometer_DegC_Ch3) THEN
        rVotedMeltTemp_DegC := rMeltTempPyrometer_DegC_Ch1;
    ELSIF (rMeltTempPyrometer_DegC_Ch2 >= rMeltTempPyrometer_DegC_Ch1 AND rMeltTempPyrometer_DegC_Ch2 <= rMeltTempPyrometer_DegC_Ch3) OR
          (rMeltTempPyrometer_DegC_Ch2 <= rMeltTempPyrometer_DegC_Ch1 AND rMeltTempPyrometer_DegC_Ch2 >= rMeltTempPyrometer_DegC_Ch3) THEN
        rVotedMeltTemp_DegC := rMeltTempPyrometer_DegC_Ch2;
    ELSE
        rVotedMeltTemp_DegC := rMeltTempPyrometer_DegC_Ch3;
    END_IF;
ELSIF bMeltTemp_Ch1_Fault AND NOT bMeltTemp_Ch2_Fault AND NOT bMeltTemp_Ch3_Fault THEN
    rVotedMeltTemp_DegC := (rMeltTempPyrometer_DegC_Ch2 + rMeltTempPyrometer_DegC_Ch3) * 0.5;
ELSIF bMeltTemp_Ch2_Fault AND NOT bMeltTemp_Ch1_Fault AND NOT bMeltTemp_Ch3_Fault THEN
    rVotedMeltTemp_DegC := (rMeltTempPyrometer_DegC_Ch1 + rMeltTempPyrometer_DegC_Ch3) * 0.5;
ELSIF bMeltTemp_Ch3_Fault AND NOT bMeltTemp_Ch1_Fault AND NOT bMeltTemp_Ch2_Fault THEN
    rVotedMeltTemp_DegC := (rMeltTempPyrometer_DegC_Ch1 + rMeltTempPyrometer_DegC_Ch2) * 0.5;
ELSE
    (* Multiple pyrometer faults: latch surviving channel or safe physical model estimate *)
    IF NOT bMeltTemp_Ch1_Fault THEN
        rVotedMeltTemp_DegC := rMeltTempPyrometer_DegC_Ch1;
    ELSIF NOT bMeltTemp_Ch2_Fault THEN
        rVotedMeltTemp_DegC := rMeltTempPyrometer_DegC_Ch2;
    ELSE
        rVotedMeltTemp_DegC := rMeltTempPyrometer_DegC_Ch3;
    END_IF;
    dwWarningWord := dwWarningWord OR 16#0000_0001; (* Multiple pyrometer faults degraded *)
END_IF;

(* 1.2 Optical CCD Meniscus Ring Diameter 2oo3 Voting (Tolerance: 1.5 mm) *)
bMeniscusDiam_Dev_1_2 := ABS(rMeniscusDiameter_mm_Ch1 - rMeniscusDiameter_mm_Ch2) > 1.5;
bMeniscusDiam_Dev_2_3 := ABS(rMeniscusDiameter_mm_Ch2 - rMeniscusDiameter_mm_Ch3) > 1.5;
bMeniscusDiam_Dev_1_3 := ABS(rMeniscusDiameter_mm_Ch1 - rMeniscusDiameter_mm_Ch3) > 1.5;

IF bMeniscusDiam_Dev_1_2 AND bMeniscusDiam_Dev_1_3 THEN
    bMeniscusDiam_Ch1_Fault := TRUE;
END_IF;
IF bMeniscusDiam_Dev_1_2 AND bMeniscusDiam_Dev_2_3 THEN
    bMeniscusDiam_Ch2_Fault := TRUE;
END_IF;
IF bMeniscusDiam_Dev_1_3 AND bMeniscusDiam_Dev_2_3 THEN
    bMeniscusDiam_Ch3_Fault := TRUE;
END_IF;

bMeniscusDiam_Degraded_1oo2 := bMeniscusDiam_Ch1_Fault OR bMeniscusDiam_Ch2_Fault OR bMeniscusDiam_Ch3_Fault;

IF NOT bMeniscusDiam_Degraded_1oo2 THEN
    IF (rMeniscusDiameter_mm_Ch1 >= rMeniscusDiameter_mm_Ch2 AND rMeniscusDiameter_mm_Ch1 <= rMeniscusDiameter_mm_Ch3) OR
       (rMeniscusDiameter_mm_Ch1 <= rMeniscusDiameter_mm_Ch2 AND rMeniscusDiameter_mm_Ch1 >= rMeniscusDiameter_mm_Ch3) THEN
        rVotedMeniscusDiam_mm := rMeniscusDiameter_mm_Ch1;
    ELSIF (rMeniscusDiameter_mm_Ch2 >= rMeniscusDiameter_mm_Ch1 AND rMeniscusDiameter_mm_Ch2 <= rMeniscusDiameter_mm_Ch3) OR
          (rMeniscusDiameter_mm_Ch2 <= rMeniscusDiameter_mm_Ch1 AND rMeniscusDiameter_mm_Ch2 >= rMeniscusDiameter_mm_Ch3) THEN
        rVotedMeniscusDiam_mm := rMeniscusDiameter_mm_Ch2;
    ELSE
        rVotedMeniscusDiam_mm := rMeniscusDiameter_mm_Ch3;
    END_IF;
ELSIF bMeniscusDiam_Ch1_Fault AND NOT bMeniscusDiam_Ch2_Fault AND NOT bMeniscusDiam_Ch3_Fault THEN
    rVotedMeniscusDiam_mm := (rMeniscusDiameter_mm_Ch2 + rMeniscusDiameter_mm_Ch3) * 0.5;
ELSIF bMeniscusDiam_Ch2_Fault AND NOT bMeniscusDiam_Ch1_Fault AND NOT bMeniscusDiam_Ch3_Fault THEN
    rVotedMeniscusDiam_mm := (rMeniscusDiameter_mm_Ch1 + rMeniscusDiameter_mm_Ch3) * 0.5;
ELSIF bMeniscusDiam_Ch3_Fault AND NOT bMeniscusDiam_Ch1_Fault AND NOT bMeniscusDiam_Ch2_Fault THEN
    rVotedMeniscusDiam_mm := (rMeniscusDiameter_mm_Ch1 + rMeniscusDiameter_mm_Ch2) * 0.5;
ELSE
    IF NOT bMeniscusDiam_Ch1_Fault THEN
        rVotedMeniscusDiam_mm := rMeniscusDiameter_mm_Ch1;
    ELSIF NOT bMeniscusDiam_Ch2_Fault THEN
        rVotedMeniscusDiam_mm := rMeniscusDiameter_mm_Ch2;
    ELSE
        rVotedMeniscusDiam_mm := rMeniscusDiameter_mm_Ch3;
    END_IF;
    dwWarningWord := dwWarningWord OR 16#0000_0002; (* Multiple meniscus camera faults degraded *)
END_IF;

(* 1.3 Chamber Vacuum Capacitance Manometer 2oo3 Voting (Tolerance: 2.0 mbar) *)
bChamberPress_Dev_1_2 := ABS(rChamberPressure_mbar_Ch1 - rChamberPressure_mbar_Ch2) > 2.0;
bChamberPress_Dev_2_3 := ABS(rChamberPressure_mbar_Ch2 - rChamberPressure_mbar_Ch3) > 2.0;
bChamberPress_Dev_1_3 := ABS(rChamberPressure_mbar_Ch1 - rChamberPressure_mbar_Ch3) > 2.0;

IF bChamberPress_Dev_1_2 AND bChamberPress_Dev_1_3 THEN
    bChamberPress_Ch1_Fault := TRUE;
END_IF;
IF bChamberPress_Dev_1_2 AND bChamberPress_Dev_2_3 THEN
    bChamberPress_Ch2_Fault := TRUE;
END_IF;
IF bChamberPress_Dev_1_3 AND bChamberPress_Dev_2_3 THEN
    bChamberPress_Ch3_Fault := TRUE;
END_IF;

bChamberPress_Degraded_1oo2 := bChamberPress_Ch1_Fault OR bChamberPress_Ch2_Fault OR bChamberPress_Ch3_Fault;

IF NOT bChamberPress_Degraded_1oo2 THEN
    IF (rChamberPressure_mbar_Ch1 >= rChamberPressure_mbar_Ch2 AND rChamberPressure_mbar_Ch1 <= rChamberPressure_mbar_Ch3) OR
       (rChamberPressure_mbar_Ch1 <= rChamberPressure_mbar_Ch2 AND rChamberPressure_mbar_Ch1 >= rChamberPressure_mbar_Ch3) THEN
        rVotedChamberPress_mbar := rChamberPressure_mbar_Ch1;
    ELSIF (rChamberPressure_mbar_Ch2 >= rChamberPressure_mbar_Ch1 AND rChamberPressure_mbar_Ch2 <= rChamberPressure_mbar_Ch3) OR
          (rChamberPressure_mbar_Ch2 <= rChamberPressure_mbar_Ch1 AND rChamberPressure_mbar_Ch2 >= rChamberPressure_mbar_Ch3) THEN
        rVotedChamberPress_mbar := rChamberPressure_mbar_Ch2;
    ELSE
        rVotedChamberPress_mbar := rChamberPressure_mbar_Ch3;
    END_IF;
ELSIF bChamberPress_Ch1_Fault AND NOT bChamberPress_Ch2_Fault AND NOT bChamberPress_Ch3_Fault THEN
    rVotedChamberPress_mbar := (rChamberPressure_mbar_Ch2 + rChamberPressure_mbar_Ch3) * 0.5;
ELSIF bChamberPress_Ch2_Fault AND NOT bChamberPress_Ch1_Fault AND NOT bChamberPress_Ch3_Fault THEN
    rVotedChamberPress_mbar := (rChamberPressure_mbar_Ch1 + rChamberPressure_mbar_Ch3) * 0.5;
ELSIF bChamberPress_Ch3_Fault AND NOT bChamberPress_Ch1_Fault AND NOT bChamberPress_Ch2_Fault THEN
    rVotedChamberPress_mbar := (rChamberPressure_mbar_Ch1 + rChamberPressure_mbar_Ch2) * 0.5;
ELSE
    IF NOT bChamberPress_Ch1_Fault THEN
        rVotedChamberPress_mbar := rChamberPressure_mbar_Ch1;
    ELSIF NOT bChamberPress_Ch2_Fault THEN
        rVotedChamberPress_mbar := rChamberPressure_mbar_Ch2;
    ELSE
        rVotedChamberPress_mbar := rChamberPressure_mbar_Ch3;
    END_IF;
    dwWarningWord := dwWarningWord OR 16#0000_0004; (* Multiple pressure manometer faults degraded *)
END_IF;

(* 1.4 Melt Surface Level Laser Triangulation 2oo3 Voting (Tolerance: 0.8 mm) *)
bMeltLevel_Dev_1_2 := ABS(rMeltLevelLaser_mm_Ch1 - rMeltLevelLaser_mm_Ch2) > 0.8;
bMeltLevel_Dev_2_3 := ABS(rMeltLevelLaser_mm_Ch2 - rMeltLevelLaser_mm_Ch3) > 0.8;
bMeltLevel_Dev_1_3 := ABS(rMeltLevelLaser_mm_Ch1 - rMeltLevelLaser_mm_Ch3) > 0.8;

IF bMeltLevel_Dev_1_2 AND bMeltLevel_Dev_1_3 THEN
    bMeltLevel_Ch1_Fault := TRUE;
END_IF;
IF bMeltLevel_Dev_1_2 AND bMeltLevel_Dev_2_3 THEN
    bMeltLevel_Ch2_Fault := TRUE;
END_IF;
IF bMeltLevel_Dev_1_3 AND bMeltLevel_Dev_2_3 THEN
    bMeltLevel_Ch3_Fault := TRUE;
END_IF;

bMeltLevel_Degraded_1oo2 := bMeltLevel_Ch1_Fault OR bMeltLevel_Ch2_Fault OR bMeltLevel_Ch3_Fault;

IF NOT bMeltLevel_Degraded_1oo2 THEN
    IF (rMeltLevelLaser_mm_Ch1 >= rMeltLevelLaser_mm_Ch2 AND rMeltLevelLaser_mm_Ch1 <= rMeltLevelLaser_mm_Ch3) OR
       (rMeltLevelLaser_mm_Ch1 <= rMeltLevelLaser_mm_Ch2 AND rMeltLevelLaser_mm_Ch1 >= rMeltLevelLaser_mm_Ch3) THEN
        rVotedMeltLevel_mm := rMeltLevelLaser_mm_Ch1;
    ELSIF (rMeltLevelLaser_mm_Ch2 >= rMeltLevelLaser_mm_Ch1 AND rMeltLevelLaser_mm_Ch2 <= rMeltLevelLaser_mm_Ch3) OR
          (rMeltLevelLaser_mm_Ch2 <= rMeltLevelLaser_mm_Ch1 AND rMeltLevelLaser_mm_Ch2 >= rMeltLevelLaser_mm_Ch3) THEN
        rVotedMeltLevel_mm := rMeltLevelLaser_mm_Ch2;
    ELSE
        rVotedMeltLevel_mm := rMeltLevelLaser_mm_Ch3;
    END_IF;
ELSIF bMeltLevel_Ch1_Fault AND NOT bMeltLevel_Ch2_Fault AND NOT bMeltLevel_Ch3_Fault THEN
    rVotedMeltLevel_mm := (rMeltLevelLaser_mm_Ch2 + rMeltLevelLaser_mm_Ch3) * 0.5;
ELSIF bMeltLevel_Ch2_Fault AND NOT bMeltLevel_Ch1_Fault AND NOT bMeltLevel_Ch3_Fault THEN
    rVotedMeltLevel_mm := (rMeltLevelLaser_mm_Ch1 + rMeltLevelLaser_mm_Ch3) * 0.5;
ELSIF bMeltLevel_Ch3_Fault AND NOT bMeltLevel_Ch1_Fault AND NOT bMeltLevel_Ch2_Fault THEN
    rVotedMeltLevel_mm := (rMeltLevelLaser_mm_Ch1 + rMeltLevelLaser_mm_Ch2) * 0.5;
ELSE
    IF NOT bMeltLevel_Ch1_Fault THEN
        rVotedMeltLevel_mm := rMeltLevelLaser_mm_Ch1;
    ELSIF NOT bMeltLevel_Ch2_Fault THEN
        rVotedMeltLevel_mm := rMeltLevelLaser_mm_Ch2;
    ELSE
        rVotedMeltLevel_mm := rMeltLevelLaser_mm_Ch3;
    END_IF;
    dwWarningWord := dwWarningWord OR 16#0000_0008; (* Multiple melt laser level faults degraded *)
END_IF;

(* 1.5 Crucible Graphite Susceptor Type B Thermocouple 2oo3 Voting (Tolerance: 15.0 deg C) *)
bCrucibleTemp_Dev_1_2 := ABS(rCrucibleWallTemp_DegC_Ch1 - rCrucibleWallTemp_DegC_Ch2) > 15.0;
bCrucibleTemp_Dev_2_3 := ABS(rCrucibleWallTemp_DegC_Ch2 - rCrucibleWallTemp_DegC_Ch3) > 15.0;
bCrucibleTemp_Dev_1_3 := ABS(rCrucibleWallTemp_DegC_Ch1 - rCrucibleWallTemp_DegC_Ch3) > 15.0;

IF bCrucibleTemp_Dev_1_2 AND bCrucibleTemp_Dev_1_3 THEN
    bCrucibleTemp_Ch1_Fault := TRUE;
END_IF;
IF bCrucibleTemp_Dev_1_2 AND bCrucibleTemp_Dev_2_3 THEN
    bCrucibleTemp_Ch2_Fault := TRUE;
END_IF;
IF bCrucibleTemp_Dev_1_3 AND bCrucibleTemp_Dev_2_3 THEN
    bCrucibleTemp_Ch3_Fault := TRUE;
END_IF;

bCrucibleTemp_Degraded_1oo2 := bCrucibleTemp_Ch1_Fault OR bCrucibleTemp_Ch2_Fault OR bCrucibleTemp_Ch3_Fault;

IF NOT bCrucibleTemp_Degraded_1oo2 THEN
    IF (rCrucibleWallTemp_DegC_Ch1 >= rCrucibleWallTemp_DegC_Ch2 AND rCrucibleWallTemp_DegC_Ch1 <= rCrucibleWallTemp_DegC_Ch3) OR
       (rCrucibleWallTemp_DegC_Ch1 <= rCrucibleWallTemp_DegC_Ch2 AND rCrucibleWallTemp_DegC_Ch1 >= rCrucibleWallTemp_DegC_Ch3) THEN
        rVotedCrucibleTemp_DegC := rCrucibleWallTemp_DegC_Ch1;
    ELSIF (rCrucibleWallTemp_DegC_Ch2 >= rCrucibleWallTemp_DegC_Ch1 AND rCrucibleWallTemp_DegC_Ch2 <= rCrucibleWallTemp_DegC_Ch3) OR
          (rCrucibleWallTemp_DegC_Ch2 <= rCrucibleWallTemp_DegC_Ch1 AND rCrucibleWallTemp_DegC_Ch2 >= rCrucibleWallTemp_DegC_Ch3) THEN
        rVotedCrucibleTemp_DegC := rCrucibleWallTemp_DegC_Ch2;
    ELSE
        rVotedCrucibleTemp_DegC := rCrucibleWallTemp_DegC_Ch3;
    END_IF;
ELSIF bCrucibleTemp_Ch1_Fault AND NOT bCrucibleTemp_Ch2_Fault AND NOT bCrucibleTemp_Ch3_Fault THEN
    rVotedCrucibleTemp_DegC := (rCrucibleWallTemp_DegC_Ch2 + rCrucibleWallTemp_DegC_Ch3) * 0.5;
ELSIF bCrucibleTemp_Ch2_Fault AND NOT bCrucibleTemp_Ch1_Fault AND NOT bCrucibleTemp_Ch3_Fault THEN
    rVotedCrucibleTemp_DegC := (rCrucibleWallTemp_DegC_Ch1 + rCrucibleWallTemp_DegC_Ch3) * 0.5;
ELSIF bCrucibleTemp_Ch3_Fault AND NOT bCrucibleTemp_Ch1_Fault AND NOT bCrucibleTemp_Ch2_Fault THEN
    rVotedCrucibleTemp_DegC := (rCrucibleWallTemp_DegC_Ch1 + rCrucibleWallTemp_DegC_Ch2) * 0.5;
ELSE
    IF NOT bCrucibleTemp_Ch1_Fault THEN
        rVotedCrucibleTemp_DegC := rCrucibleWallTemp_DegC_Ch1;
    ELSIF NOT bCrucibleTemp_Ch2_Fault THEN
        rVotedCrucibleTemp_DegC := rCrucibleWallTemp_DegC_Ch2;
    ELSE
        rVotedCrucibleTemp_DegC := rCrucibleWallTemp_DegC_Ch3;
    END_IF;
    dwWarningWord := dwWarningWord OR 16#0000_0010; (* Multiple crucible thermocouple faults degraded *)
END_IF;

(* 1.6 Overall Degraded Sensor Evaluation *)
bAnySensorDegraded := bMeltTemp_Degraded_1oo2 OR bMeniscusDiam_Degraded_1oo2 OR
                      bChamberPress_Degraded_1oo2 OR bMeltLevel_Degraded_1oo2 OR
                      bCrucibleTemp_Degraded_1oo2;

bDegradedSensorMode := bAnySensorDegraded;
"""
