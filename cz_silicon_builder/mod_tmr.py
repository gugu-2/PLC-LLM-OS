# cz_silicon_builder/mod_tmr.py
# -*- coding: utf-8 -*-

def generate_tmr():
    return """(* ==========================================================================================
   PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS
   ==========================================================================================
   Provides robust fault tolerance and bumpless degradation for 4 critical sensor triplets:
     1. Triplicated Melt Meniscus Optical Pyrometers [deg C]
     2. Triplicated High-Speed CCD Camera Diameter Channels [mm]
     3. Triplicated Seed Suspension Load Cell Weight Transducers [kg]
     4. Triplicated Main Graphite Resistance Heater Thermocouple Arrays [deg C]
   Implements 200 ms persistence filtering before trip to reject high-temperature optical glare,
   sparks, and RF electromagnetic noise from thyristor power bursts.
   ========================================================================================== *)

(* ------------------------------------------------------------------------------------------
   1. TRIPLET 1: MELT MENISCUS OPTICAL PYROMETERS [deg C]
   ------------------------------------------------------------------------------------------ *)
(* Pairwise absolute difference computation *)
rPyro_DiffAB := ABS(rPyrometer_Meniscus_ChA - rPyrometer_Meniscus_ChB);
rPyro_DiffBC := ABS(rPyrometer_Meniscus_ChB - rPyrometer_Meniscus_ChC);
rPyro_DiffCA := ABS(rPyrometer_Meniscus_ChC - rPyrometer_Meniscus_ChA);

(* Discrepancy detection with out-of-range gross electrical plausibility check *)
ton_PyroA_Discrep(
    IN := ((rPyro_DiffAB > rPyro_DevLimit_degC) AND (rPyro_DiffCA > rPyro_DevLimit_degC))
          OR (rPyrometer_Meniscus_ChA < 20.0) OR (rPyrometer_Meniscus_ChA > 1650.0),
    PT := tDiscrepancyPersistence
);
bPyro_FltA := ton_PyroA_Discrep.Q;

ton_PyroB_Discrep(
    IN := ((rPyro_DiffAB > rPyro_DevLimit_degC) AND (rPyro_DiffBC > rPyro_DevLimit_degC))
          OR (rPyrometer_Meniscus_ChB < 20.0) OR (rPyrometer_Meniscus_ChB > 1650.0),
    PT := tDiscrepancyPersistence
);
bPyro_FltB := ton_PyroB_Discrep.Q;

ton_PyroC_Discrep(
    IN := ((rPyro_DiffBC > rPyro_DevLimit_degC) AND (rPyro_DiffCA > rPyro_DevLimit_degC))
          OR (rPyrometer_Meniscus_ChC < 20.0) OR (rPyrometer_Meniscus_ChC > 1650.0),
    PT := tDiscrepancyPersistence
);
bPyro_FltC := ton_PyroC_Discrep.Q;

(* 2oo3 Voting & Degradation Logic *)
IF (NOT bPyro_FltA) AND (NOT bPyro_FltB) AND (NOT bPyro_FltC) THEN
    (* All 3 channels healthy: True mathematical median selection *)
    IF ((rPyrometer_Meniscus_ChA >= rPyrometer_Meniscus_ChB) AND (rPyrometer_Meniscus_ChA <= rPyrometer_Meniscus_ChC))
       OR ((rPyrometer_Meniscus_ChA >= rPyrometer_Meniscus_ChC) AND (rPyrometer_Meniscus_ChA <= rPyrometer_Meniscus_ChB)) THEN
        rVotedMeniscusTemp := rPyrometer_Meniscus_ChA;
    ELSIF ((rPyrometer_Meniscus_ChB >= rPyrometer_Meniscus_ChA) AND (rPyrometer_Meniscus_ChB <= rPyrometer_Meniscus_ChC))
          OR ((rPyrometer_Meniscus_ChB >= rPyrometer_Meniscus_ChC) AND (rPyrometer_Meniscus_ChB <= rPyrometer_Meniscus_ChA)) THEN
        rVotedMeniscusTemp := rPyrometer_Meniscus_ChB;
    ELSE
        rVotedMeniscusTemp := rPyrometer_Meniscus_ChC;
    END_IF;
    bPyro_DegradedMode := FALSE;
    bPyro_CriticalFailSafe := FALSE;
ELSIF bPyro_FltA AND (NOT bPyro_FltB) AND (NOT bPyro_FltC) THEN
    (* Channel A faulted: Degraded average of channels B and C *)
    rVotedMeniscusTemp := (rPyrometer_Meniscus_ChB + rPyrometer_Meniscus_ChC) * 0.50;
    bPyro_DegradedMode := TRUE;
    bPyro_CriticalFailSafe := FALSE;
ELSIF bPyro_FltB AND (NOT bPyro_FltA) AND (NOT bPyro_FltC) THEN
    (* Channel B faulted: Degraded average of channels A and C *)
    rVotedMeniscusTemp := (rPyrometer_Meniscus_ChA + rPyrometer_Meniscus_ChC) * 0.50;
    bPyro_DegradedMode := TRUE;
    bPyro_CriticalFailSafe := FALSE;
ELSIF bPyro_FltC AND (NOT bPyro_FltA) AND (NOT bPyro_FltB) THEN
    (* Channel C faulted: Degraded average of channels A and B *)
    rVotedMeniscusTemp := (rPyrometer_Meniscus_ChA + rPyrometer_Meniscus_ChB) * 0.50;
    bPyro_DegradedMode := TRUE;
    bPyro_CriticalFailSafe := FALSE;
ELSE
    (* Multiple failures (2 or 3 channels down): Hold last known valid reading *)
    rVotedMeniscusTemp := rLastValidVotedMeniscusTemp;
    bPyro_DegradedMode := TRUE;
    bPyro_CriticalFailSafe := TRUE;
END_IF;

IF NOT bPyro_CriticalFailSafe THEN
    rLastValidVotedMeniscusTemp := rVotedMeniscusTemp;
END_IF;


(* ------------------------------------------------------------------------------------------
   2. TRIPLET 2: HIGH-SPEED CCD CAMERA DIAMETER METROLOGY CHANNELS [mm]
   ------------------------------------------------------------------------------------------ *)
rCCD_DiffAB := ABS(rCCD_Diameter_ChA - rCCD_Diameter_ChB);
rCCD_DiffBC := ABS(rCCD_Diameter_ChB - rCCD_Diameter_ChC);
rCCD_DiffCA := ABS(rCCD_Diameter_ChC - rCCD_Diameter_ChA);

ton_CCDA_Discrep(
    IN := ((rCCD_DiffAB > rCCD_DevLimit_mm) AND (rCCD_DiffCA > rCCD_DevLimit_mm))
          OR (rCCD_Diameter_ChA < 0.0) OR (rCCD_Diameter_ChA > 450.0),
    PT := tDiscrepancyPersistence
);
bCCD_FltA := ton_CCDA_Discrep.Q;

ton_CCDB_Discrep(
    IN := ((rCCD_DiffAB > rCCD_DevLimit_mm) AND (rCCD_DiffBC > rCCD_DevLimit_mm))
          OR (rCCD_Diameter_ChB < 0.0) OR (rCCD_Diameter_ChB > 450.0),
    PT := tDiscrepancyPersistence
);
bCCD_FltB := ton_CCDB_Discrep.Q;

ton_CCDC_Discrep(
    IN := ((rCCD_DiffBC > rCCD_DevLimit_mm) AND (rCCD_DiffCA > rCCD_DevLimit_mm))
          OR (rCCD_Diameter_ChC < 0.0) OR (rCCD_Diameter_ChC > 450.0),
    PT := tDiscrepancyPersistence
);
bCCD_FltC := ton_CCDC_Discrep.Q;

IF (NOT bCCD_FltA) AND (NOT bCCD_FltB) AND (NOT bCCD_FltC) THEN
    (* All 3 channels healthy: Median selection *)
    IF ((rCCD_Diameter_ChA >= rCCD_Diameter_ChB) AND (rCCD_Diameter_ChA <= rCCD_Diameter_ChC))
       OR ((rCCD_Diameter_ChA >= rCCD_Diameter_ChC) AND (rCCD_Diameter_ChA <= rCCD_Diameter_ChB)) THEN
        rVotedIngotDiameter := rCCD_Diameter_ChA;
    ELSIF ((rCCD_Diameter_ChB >= rCCD_Diameter_ChA) AND (rCCD_Diameter_ChB <= rCCD_Diameter_ChC))
          OR ((rCCD_Diameter_ChB >= rCCD_Diameter_ChC) AND (rCCD_Diameter_ChB <= rCCD_Diameter_ChA)) THEN
        rVotedIngotDiameter := rCCD_Diameter_ChB;
    ELSE
        rVotedIngotDiameter := rCCD_Diameter_ChC;
    END_IF;
    bCCD_DegradedMode := FALSE;
    bCCD_CriticalFailSafe := FALSE;
ELSIF bCCD_FltA AND (NOT bCCD_FltB) AND (NOT bCCD_FltC) THEN
    rVotedIngotDiameter := (rCCD_Diameter_ChB + rCCD_Diameter_ChC) * 0.50;
    bCCD_DegradedMode := TRUE;
    bCCD_CriticalFailSafe := FALSE;
ELSIF bCCD_FltB AND (NOT bCCD_FltA) AND (NOT bCCD_FltC) THEN
    rVotedIngotDiameter := (rCCD_Diameter_ChA + rCCD_Diameter_ChC) * 0.50;
    bCCD_DegradedMode := TRUE;
    bCCD_CriticalFailSafe := FALSE;
ELSIF bCCD_FltC AND (NOT bCCD_FltA) AND (NOT bCCD_FltB) THEN
    rVotedIngotDiameter := (rCCD_Diameter_ChA + rCCD_Diameter_ChB) * 0.50;
    bCCD_DegradedMode := TRUE;
    bCCD_CriticalFailSafe := FALSE;
ELSE
    rVotedIngotDiameter := rLastValidVotedIngotDiameter;
    bCCD_DegradedMode := TRUE;
    bCCD_CriticalFailSafe := TRUE;
END_IF;

IF NOT bCCD_CriticalFailSafe THEN
    rLastValidVotedIngotDiameter := rVotedIngotDiameter;
END_IF;


(* ------------------------------------------------------------------------------------------
   3. TRIPLET 3: SEED SUSPENSION LOAD CELL WEIGHT TRANSDUCERS [kg]
   ------------------------------------------------------------------------------------------ *)
rLoadCell_DiffAB := ABS(rLoadCell_Weight_ChA - rLoadCell_Weight_ChB);
rLoadCell_DiffBC := ABS(rLoadCell_Weight_ChB - rLoadCell_Weight_ChC);
rLoadCell_DiffCA := ABS(rLoadCell_Weight_ChC - rLoadCell_Weight_ChA);

ton_LoadCellA_Discrep(
    IN := ((rLoadCell_DiffAB > rLoadCell_DevLimit_kg) AND (rLoadCell_DiffCA > rLoadCell_DevLimit_kg))
          OR (rLoadCell_Weight_ChA < -2.0) OR (rLoadCell_Weight_ChA > 500.0),
    PT := tDiscrepancyPersistence
);
bLoadCell_FltA := ton_LoadCellA_Discrep.Q;

ton_LoadCellB_Discrep(
    IN := ((rLoadCell_DiffAB > rLoadCell_DevLimit_kg) AND (rLoadCell_DiffBC > rLoadCell_DevLimit_kg))
          OR (rLoadCell_Weight_ChB < -2.0) OR (rLoadCell_Weight_ChB > 500.0),
    PT := tDiscrepancyPersistence
);
bLoadCell_FltB := ton_LoadCellB_Discrep.Q;

ton_LoadCellC_Discrep(
    IN := ((rLoadCell_DiffBC > rLoadCell_DevLimit_kg) AND (rLoadCell_DiffCA > rLoadCell_DevLimit_kg))
          OR (rLoadCell_Weight_ChC < -2.0) OR (rLoadCell_Weight_ChC > 500.0),
    PT := tDiscrepancyPersistence
);
bLoadCell_FltC := ton_LoadCellC_Discrep.Q;

IF (NOT bLoadCell_FltA) AND (NOT bLoadCell_FltB) AND (NOT bLoadCell_FltC) THEN
    (* All 3 channels healthy: Median selection *)
    IF ((rLoadCell_Weight_ChA >= rLoadCell_Weight_ChB) AND (rLoadCell_Weight_ChA <= rLoadCell_Weight_ChC))
       OR ((rLoadCell_Weight_ChA >= rLoadCell_Weight_ChC) AND (rLoadCell_Weight_ChA <= rLoadCell_Weight_ChB)) THEN
        rVotedCrystalWeight := rLoadCell_Weight_ChA;
    ELSIF ((rLoadCell_Weight_ChB >= rLoadCell_Weight_ChA) AND (rLoadCell_Weight_ChB <= rLoadCell_Weight_ChC))
          OR ((rLoadCell_Weight_ChB >= rLoadCell_Weight_ChC) AND (rLoadCell_Weight_ChB <= rLoadCell_Weight_ChA)) THEN
        rVotedCrystalWeight := rLoadCell_Weight_ChB;
    ELSE
        rVotedCrystalWeight := rLoadCell_Weight_ChC;
    END_IF;
    bLoadCell_DegradedMode := FALSE;
    bLoadCell_CriticalFailSafe := FALSE;
ELSIF bLoadCell_FltA AND (NOT bLoadCell_FltB) AND (NOT bLoadCell_FltC) THEN
    rVotedCrystalWeight := (rLoadCell_Weight_ChB + rLoadCell_Weight_ChC) * 0.50;
    bLoadCell_DegradedMode := TRUE;
    bLoadCell_CriticalFailSafe := FALSE;
ELSIF bLoadCell_FltB AND (NOT bLoadCell_FltA) AND (NOT bLoadCell_FltC) THEN
    rVotedCrystalWeight := (rLoadCell_Weight_ChA + rLoadCell_Weight_ChC) * 0.50;
    bLoadCell_DegradedMode := TRUE;
    bLoadCell_CriticalFailSafe := FALSE;
ELSIF bLoadCell_FltC AND (NOT bLoadCell_FltA) AND (NOT bLoadCell_FltB) THEN
    rVotedCrystalWeight := (rLoadCell_Weight_ChA + rLoadCell_Weight_ChB) * 0.50;
    bLoadCell_DegradedMode := TRUE;
    bLoadCell_CriticalFailSafe := FALSE;
ELSE
    rVotedCrystalWeight := rLastValidVotedCrystalWeight;
    bLoadCell_DegradedMode := TRUE;
    bLoadCell_CriticalFailSafe := TRUE;
END_IF;

IF NOT bLoadCell_CriticalFailSafe THEN
    rLastValidVotedCrystalWeight := rVotedCrystalWeight;
END_IF;


(* ------------------------------------------------------------------------------------------
   4. TRIPLET 4: MAIN GRAPHITE RESISTANCE HEATER THERMOCOUPLE ARRAYS [deg C]
   ------------------------------------------------------------------------------------------ *)
rHeater_DiffAB := ABS(rHeater_TC_ChA - rHeater_TC_ChB);
rHeater_DiffBC := ABS(rHeater_TC_ChB - rHeater_TC_ChC);
rHeater_DiffCA := ABS(rHeater_TC_ChC - rHeater_TC_ChA);

ton_HeaterA_Discrep(
    IN := ((rHeater_DiffAB > rHeater_DevLimit_degC) AND (rHeater_DiffCA > rHeater_DevLimit_degC))
          OR (rHeater_TC_ChA < 20.0) OR (rHeater_TC_ChA > 2000.0),
    PT := tDiscrepancyPersistence
);
bHeater_FltA := ton_HeaterA_Discrep.Q;

ton_HeaterB_Discrep(
    IN := ((rHeater_DiffAB > rHeater_DevLimit_degC) AND (rHeater_DiffBC > rHeater_DevLimit_degC))
          OR (rHeater_TC_ChB < 20.0) OR (rHeater_TC_ChB > 2000.0),
    PT := tDiscrepancyPersistence
);
bHeater_FltB := ton_HeaterB_Discrep.Q;

ton_HeaterC_Discrep(
    IN := ((rHeater_DiffBC > rHeater_DevLimit_degC) AND (rHeater_DiffCA > rHeater_DevLimit_degC))
          OR (rHeater_TC_ChC < 20.0) OR (rHeater_TC_ChC > 2000.0),
    PT := tDiscrepancyPersistence
);
bHeater_FltC := ton_HeaterC_Discrep.Q;

IF (NOT bHeater_FltA) AND (NOT bHeater_FltB) AND (NOT bHeater_FltC) THEN
    (* All 3 channels healthy: Median selection *)
    IF ((rHeater_TC_ChA >= rHeater_TC_ChB) AND (rHeater_TC_ChA <= rHeater_TC_ChC))
       OR ((rHeater_TC_ChA >= rHeater_TC_ChC) AND (rHeater_TC_ChA <= rHeater_TC_ChB)) THEN
        rVotedHeaterTemp := rHeater_TC_ChA;
    ELSIF ((rHeater_TC_ChB >= rHeater_TC_ChA) AND (rHeater_TC_ChB <= rHeater_TC_ChC))
          OR ((rHeater_TC_ChB >= rHeater_TC_ChC) AND (rHeater_TC_ChB <= rHeater_TC_ChA)) THEN
        rVotedHeaterTemp := rHeater_TC_ChB;
    ELSE
        rVotedHeaterTemp := rHeater_TC_ChC;
    END_IF;
    bHeater_DegradedMode := FALSE;
    bHeater_CriticalFailSafe := FALSE;
ELSIF bHeater_FltA AND (NOT bHeater_FltB) AND (NOT bHeater_FltC) THEN
    rVotedHeaterTemp := (rHeater_TC_ChB + rHeater_TC_ChC) * 0.50;
    bHeater_DegradedMode := TRUE;
    bHeater_CriticalFailSafe := FALSE;
ELSIF bHeater_FltB AND (NOT bHeater_FltA) AND (NOT bHeater_FltC) THEN
    rVotedHeaterTemp := (rHeater_TC_ChA + rHeater_TC_ChC) * 0.50;
    bHeater_DegradedMode := TRUE;
    bHeater_CriticalFailSafe := FALSE;
ELSIF bHeater_FltC AND (NOT bHeater_FltA) AND (NOT bHeater_FltB) THEN
    rVotedHeaterTemp := (rHeater_TC_ChA + rHeater_TC_ChB) * 0.50;
    bHeater_DegradedMode := TRUE;
    bHeater_CriticalFailSafe := FALSE;
ELSE
    rVotedHeaterTemp := rLastValidVotedHeaterTemp;
    bHeater_DegradedMode := TRUE;
    bHeater_CriticalFailSafe := TRUE;
END_IF;

IF NOT bHeater_CriticalFailSafe THEN
    rLastValidVotedHeaterTemp := rVotedHeaterTemp;
END_IF;"""
