# Part 2: Phases 1, 2, 3
import os

code_part2 = '''
(* ==================================================================================================== *)
(* === PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & INTEGRITY ENGINE               === *)
(* ==================================================================================================== *)

(* 1.1 Sensor Bank 1: Main Resin Loss-in-Weight Gravimetric Feeder 101A/B/C *)
bMainFeeder_A_Ok := (WT_GRAVIMETRIC_FEEDER_MAIN_101A >= 0.0) AND (WT_GRAVIMETRIC_FEEDER_MAIN_101A <= 3200.0);
bMainFeeder_B_Ok := (WT_GRAVIMETRIC_FEEDER_MAIN_101B >= 0.0) AND (WT_GRAVIMETRIC_FEEDER_MAIN_101B <= 3200.0);
bMainFeeder_C_Ok := (WT_GRAVIMETRIC_FEEDER_MAIN_101C >= 0.0) AND (WT_GRAVIMETRIC_FEEDER_MAIN_101C <= 3200.0);
iMainFeeder_HealthyCount := 0;
IF bMainFeeder_A_Ok THEN iMainFeeder_HealthyCount := iMainFeeder_HealthyCount + 1; END_IF;
IF bMainFeeder_B_Ok THEN iMainFeeder_HealthyCount := iMainFeeder_HealthyCount + 1; END_IF;
IF bMainFeeder_C_Ok THEN iMainFeeder_HealthyCount := iMainFeeder_HealthyCount + 1; END_IF;
rMainFeeder_Diff_AB := ABS(WT_GRAVIMETRIC_FEEDER_MAIN_101A - WT_GRAVIMETRIC_FEEDER_MAIN_101B);
rMainFeeder_Diff_BC := ABS(WT_GRAVIMETRIC_FEEDER_MAIN_101B - WT_GRAVIMETRIC_FEEDER_MAIN_101C);
rMainFeeder_Diff_CA := ABS(WT_GRAVIMETRIC_FEEDER_MAIN_101C - WT_GRAVIMETRIC_FEEDER_MAIN_101A);
IF iMainFeeder_HealthyCount = 3 THEN
    IF (WT_GRAVIMETRIC_FEEDER_MAIN_101A >= WT_GRAVIMETRIC_FEEDER_MAIN_101B AND WT_GRAVIMETRIC_FEEDER_MAIN_101A <= WT_GRAVIMETRIC_FEEDER_MAIN_101C) OR
       (WT_GRAVIMETRIC_FEEDER_MAIN_101A >= WT_GRAVIMETRIC_FEEDER_MAIN_101C AND WT_GRAVIMETRIC_FEEDER_MAIN_101A <= WT_GRAVIMETRIC_FEEDER_MAIN_101B) THEN
        rMainFeeder_Voted_kgh := WT_GRAVIMETRIC_FEEDER_MAIN_101A;
    ELSIF (WT_GRAVIMETRIC_FEEDER_MAIN_101B >= WT_GRAVIMETRIC_FEEDER_MAIN_101A AND WT_GRAVIMETRIC_FEEDER_MAIN_101B <= WT_GRAVIMETRIC_FEEDER_MAIN_101C) OR
          (WT_GRAVIMETRIC_FEEDER_MAIN_101B >= WT_GRAVIMETRIC_FEEDER_MAIN_101C AND WT_GRAVIMETRIC_FEEDER_MAIN_101B <= WT_GRAVIMETRIC_FEEDER_MAIN_101A) THEN
        rMainFeeder_Voted_kgh := WT_GRAVIMETRIC_FEEDER_MAIN_101B;
    ELSE
        rMainFeeder_Voted_kgh := WT_GRAVIMETRIC_FEEDER_MAIN_101C;
    END_IF;
    IF (rMainFeeder_Diff_AB > 25.0) OR (rMainFeeder_Diff_BC > 25.0) OR (rMainFeeder_Diff_CA > 25.0) THEN
        tMainFeeder_DiscrepancyTimer(IN := TRUE, PT := T#500MS);
    ELSE
        tMainFeeder_DiscrepancyTimer(IN := FALSE);
    END_IF;
ELSIF iMainFeeder_HealthyCount = 2 THEN
    IF bMainFeeder_A_Ok AND bMainFeeder_B_Ok THEN
        rMainFeeder_Voted_kgh := (WT_GRAVIMETRIC_FEEDER_MAIN_101A + WT_GRAVIMETRIC_FEEDER_MAIN_101B) * 0.5;
    ELSIF bMainFeeder_B_Ok AND bMainFeeder_C_Ok THEN
        rMainFeeder_Voted_kgh := (WT_GRAVIMETRIC_FEEDER_MAIN_101B + WT_GRAVIMETRIC_FEEDER_MAIN_101C) * 0.5;
    ELSE
        rMainFeeder_Voted_kgh := (WT_GRAVIMETRIC_FEEDER_MAIN_101A + WT_GRAVIMETRIC_FEEDER_MAIN_101C) * 0.5;
    END_IF;
    tMainFeeder_DiscrepancyTimer(IN := TRUE, PT := T#500MS);
ELSIF iMainFeeder_HealthyCount = 1 THEN
    IF bMainFeeder_A_Ok THEN rMainFeeder_Voted_kgh := WT_GRAVIMETRIC_FEEDER_MAIN_101A;
    ELSIF bMainFeeder_B_Ok THEN rMainFeeder_Voted_kgh := WT_GRAVIMETRIC_FEEDER_MAIN_101B;
    ELSE rMainFeeder_Voted_kgh := WT_GRAVIMETRIC_FEEDER_MAIN_101C; END_IF;
    tMainFeeder_DiscrepancyTimer(IN := TRUE, PT := T#500MS);
ELSE
    rMainFeeder_Voted_kgh := 0.0;
    bMainFeeder_DiscrepancyFault := TRUE;
END_IF;
bMainFeeder_DiscrepancyFault := tMainFeeder_DiscrepancyTimer.Q;

(* 1.2 Sensor Bank 2: Side Stuffer Gravimetric Feeder 102A/B/C *)
bSideFeeder_A_Ok := (WT_GRAVIMETRIC_FEEDER_SIDE_102A >= 0.0) AND (WT_GRAVIMETRIC_FEEDER_SIDE_102A <= 300.0);
bSideFeeder_B_Ok := (WT_GRAVIMETRIC_FEEDER_SIDE_102B >= 0.0) AND (WT_GRAVIMETRIC_FEEDER_SIDE_102B <= 300.0);
bSideFeeder_C_Ok := (WT_GRAVIMETRIC_FEEDER_SIDE_102C >= 0.0) AND (WT_GRAVIMETRIC_FEEDER_SIDE_102C <= 300.0);
iSideFeeder_HealthyCount := 0;
IF bSideFeeder_A_Ok THEN iSideFeeder_HealthyCount := iSideFeeder_HealthyCount + 1; END_IF;
IF bSideFeeder_B_Ok THEN iSideFeeder_HealthyCount := iSideFeeder_HealthyCount + 1; END_IF;
IF bSideFeeder_C_Ok THEN iSideFeeder_HealthyCount := iSideFeeder_HealthyCount + 1; END_IF;
rSideFeeder_Diff_AB := ABS(WT_GRAVIMETRIC_FEEDER_SIDE_102A - WT_GRAVIMETRIC_FEEDER_SIDE_102B);
rSideFeeder_Diff_BC := ABS(WT_GRAVIMETRIC_FEEDER_SIDE_102B - WT_GRAVIMETRIC_FEEDER_SIDE_102C);
rSideFeeder_Diff_CA := ABS(WT_GRAVIMETRIC_FEEDER_SIDE_102C - WT_GRAVIMETRIC_FEEDER_SIDE_102A);
IF iSideFeeder_HealthyCount = 3 THEN
    IF (WT_GRAVIMETRIC_FEEDER_SIDE_102A >= WT_GRAVIMETRIC_FEEDER_SIDE_102B AND WT_GRAVIMETRIC_FEEDER_SIDE_102A <= WT_GRAVIMETRIC_FEEDER_SIDE_102C) OR
       (WT_GRAVIMETRIC_FEEDER_SIDE_102A >= WT_GRAVIMETRIC_FEEDER_SIDE_102C AND WT_GRAVIMETRIC_FEEDER_SIDE_102A <= WT_GRAVIMETRIC_FEEDER_SIDE_102B) THEN
        rSideFeeder_Voted_kgh := WT_GRAVIMETRIC_FEEDER_SIDE_102A;
    ELSIF (WT_GRAVIMETRIC_FEEDER_SIDE_102B >= WT_GRAVIMETRIC_FEEDER_SIDE_102A AND WT_GRAVIMETRIC_FEEDER_SIDE_102B <= WT_GRAVIMETRIC_FEEDER_SIDE_102C) OR
          (WT_GRAVIMETRIC_FEEDER_SIDE_102B >= WT_GRAVIMETRIC_FEEDER_SIDE_102C AND WT_GRAVIMETRIC_FEEDER_SIDE_102B <= WT_GRAVIMETRIC_FEEDER_SIDE_102A) THEN
        rSideFeeder_Voted_kgh := WT_GRAVIMETRIC_FEEDER_SIDE_102B;
    ELSE
        rSideFeeder_Voted_kgh := WT_GRAVIMETRIC_FEEDER_SIDE_102C;
    END_IF;
    IF (rSideFeeder_Diff_AB > 5.0) OR (rSideFeeder_Diff_BC > 5.0) OR (rSideFeeder_Diff_CA > 5.0) THEN
        tSideFeeder_DiscrepancyTimer(IN := TRUE, PT := T#500MS);
    ELSE
        tSideFeeder_DiscrepancyTimer(IN := FALSE);
    END_IF;
ELSIF iSideFeeder_HealthyCount = 2 THEN
    IF bSideFeeder_A_Ok AND bSideFeeder_B_Ok THEN
        rSideFeeder_Voted_kgh := (WT_GRAVIMETRIC_FEEDER_SIDE_102A + WT_GRAVIMETRIC_FEEDER_SIDE_102B) * 0.5;
    ELSIF bSideFeeder_B_Ok AND bSideFeeder_C_Ok THEN
        rSideFeeder_Voted_kgh := (WT_GRAVIMETRIC_FEEDER_SIDE_102B + WT_GRAVIMETRIC_FEEDER_SIDE_102C) * 0.5;
    ELSE
        rSideFeeder_Voted_kgh := (WT_GRAVIMETRIC_FEEDER_SIDE_102A + WT_GRAVIMETRIC_FEEDER_SIDE_102C) * 0.5;
    END_IF;
    tSideFeeder_DiscrepancyTimer(IN := TRUE, PT := T#500MS);
ELSIF iSideFeeder_HealthyCount = 1 THEN
    IF bSideFeeder_A_Ok THEN rSideFeeder_Voted_kgh := WT_GRAVIMETRIC_FEEDER_SIDE_102A;
    ELSIF bSideFeeder_B_Ok THEN rSideFeeder_Voted_kgh := WT_GRAVIMETRIC_FEEDER_SIDE_102B;
    ELSE rSideFeeder_Voted_kgh := WT_GRAVIMETRIC_FEEDER_SIDE_102C; END_IF;
    tSideFeeder_DiscrepancyTimer(IN := TRUE, PT := T#500MS);
ELSE
    rSideFeeder_Voted_kgh := 0.0;
    bSideFeeder_DiscrepancyFault := TRUE;
END_IF;
bSideFeeder_DiscrepancyFault := tSideFeeder_DiscrepancyTimer.Q;

(* 1.3 Sensor Bank 3: Liquid Peroxide Coriolis Mass Flow Meter 201A/B/C *)
bPeroxide_A_Ok := (FT_PEROXIDE_LIQUID_201A >= 0.0) AND (FT_PEROXIDE_LIQUID_201A <= 35.0);
bPeroxide_B_Ok := (FT_PEROXIDE_LIQUID_201B >= 0.0) AND (FT_PEROXIDE_LIQUID_201B <= 35.0);
bPeroxide_C_Ok := (FT_PEROXIDE_LIQUID_201C >= 0.0) AND (FT_PEROXIDE_LIQUID_201C <= 35.0);
iPeroxide_HealthyCount := 0;
IF bPeroxide_A_Ok THEN iPeroxide_HealthyCount := iPeroxide_HealthyCount + 1; END_IF;
IF bPeroxide_B_Ok THEN iPeroxide_HealthyCount := iPeroxide_HealthyCount + 1; END_IF;
IF bPeroxide_C_Ok THEN iPeroxide_HealthyCount := iPeroxide_HealthyCount + 1; END_IF;
rPeroxide_Diff_AB := ABS(FT_PEROXIDE_LIQUID_201A - FT_PEROXIDE_LIQUID_201B);
rPeroxide_Diff_BC := ABS(FT_PEROXIDE_LIQUID_201B - FT_PEROXIDE_LIQUID_201C);
rPeroxide_Diff_CA := ABS(FT_PEROXIDE_LIQUID_201C - FT_PEROXIDE_LIQUID_201A);
IF iPeroxide_HealthyCount = 3 THEN
    IF (FT_PEROXIDE_LIQUID_201A >= FT_PEROXIDE_LIQUID_201B AND FT_PEROXIDE_LIQUID_201A <= FT_PEROXIDE_LIQUID_201C) OR
       (FT_PEROXIDE_LIQUID_201A >= FT_PEROXIDE_LIQUID_201C AND FT_PEROXIDE_LIQUID_201A <= FT_PEROXIDE_LIQUID_201B) THEN
        rPeroxide_Voted_kgh := FT_PEROXIDE_LIQUID_201A;
    ELSIF (FT_PEROXIDE_LIQUID_201B >= FT_PEROXIDE_LIQUID_201A AND FT_PEROXIDE_LIQUID_201B <= FT_PEROXIDE_LIQUID_201C) OR
          (FT_PEROXIDE_LIQUID_201B >= FT_PEROXIDE_LIQUID_201C AND FT_PEROXIDE_LIQUID_201B <= FT_PEROXIDE_LIQUID_201A) THEN
        rPeroxide_Voted_kgh := FT_PEROXIDE_LIQUID_201B;
    ELSE
        rPeroxide_Voted_kgh := FT_PEROXIDE_LIQUID_201C;
    END_IF;
    IF (rPeroxide_Diff_AB > 0.40) OR (rPeroxide_Diff_BC > 0.40) OR (rPeroxide_Diff_CA > 0.40) THEN
        tPeroxide_DiscrepancyTimer(IN := TRUE, PT := T#200MS);
    ELSE
        tPeroxide_DiscrepancyTimer(IN := FALSE);
    END_IF;
ELSIF iPeroxide_HealthyCount = 2 THEN
    IF bPeroxide_A_Ok AND bPeroxide_B_Ok THEN
        rPeroxide_Voted_kgh := (FT_PEROXIDE_LIQUID_201A + FT_PEROXIDE_LIQUID_201B) * 0.5;
    ELSIF bPeroxide_B_Ok AND bPeroxide_C_Ok THEN
        rPeroxide_Voted_kgh := (FT_PEROXIDE_LIQUID_201B + FT_PEROXIDE_LIQUID_201C) * 0.5;
    ELSE
        rPeroxide_Voted_kgh := (FT_PEROXIDE_LIQUID_201A + FT_PEROXIDE_LIQUID_201C) * 0.5;
    END_IF;
    tPeroxide_DiscrepancyTimer(IN := TRUE, PT := T#200MS);
ELSIF iPeroxide_HealthyCount = 1 THEN
    IF bPeroxide_A_Ok THEN rPeroxide_Voted_kgh := FT_PEROXIDE_LIQUID_201A;
    ELSIF bPeroxide_B_Ok THEN rPeroxide_Voted_kgh := FT_PEROXIDE_LIQUID_201B;
    ELSE rPeroxide_Voted_kgh := FT_PEROXIDE_LIQUID_201C; END_IF;
    tPeroxide_DiscrepancyTimer(IN := TRUE, PT := T#200MS);
ELSE
    rPeroxide_Voted_kgh := 0.0;
    bPeroxide_DiscrepancyFault := TRUE;
END_IF;
bPeroxide_DiscrepancyFault := tPeroxide_DiscrepancyTimer.Q;

(* 1.4 Sensor Bank 4: Barrel Zone 5 Melting Melt Pressure 301A/B/C *)
bZone5Press_A_Ok := (PT_BARREL_ZONE5_MELT_301A >= 0.0) AND (PT_BARREL_ZONE5_MELT_301A <= 220.0);
bZone5Press_B_Ok := (PT_BARREL_ZONE5_MELT_301B >= 0.0) AND (PT_BARREL_ZONE5_MELT_301B <= 220.0);
bZone5Press_C_Ok := (PT_BARREL_ZONE5_MELT_301C >= 0.0) AND (PT_BARREL_ZONE5_MELT_301C <= 220.0);
iZone5Press_HealthyCount := 0;
IF bZone5Press_A_Ok THEN iZone5Press_HealthyCount := iZone5Press_HealthyCount + 1; END_IF;
IF bZone5Press_B_Ok THEN iZone5Press_HealthyCount := iZone5Press_HealthyCount + 1; END_IF;
IF bZone5Press_C_Ok THEN iZone5Press_HealthyCount := iZone5Press_HealthyCount + 1; END_IF;
rZone5Press_Diff_AB := ABS(PT_BARREL_ZONE5_MELT_301A - PT_BARREL_ZONE5_MELT_301B);
rZone5Press_Diff_BC := ABS(PT_BARREL_ZONE5_MELT_301B - PT_BARREL_ZONE5_MELT_301C);
rZone5Press_Diff_CA := ABS(PT_BARREL_ZONE5_MELT_301C - PT_BARREL_ZONE5_MELT_301A);
IF iZone5Press_HealthyCount = 3 THEN
    IF (PT_BARREL_ZONE5_MELT_301A >= PT_BARREL_ZONE5_MELT_301B AND PT_BARREL_ZONE5_MELT_301A <= PT_BARREL_ZONE5_MELT_301C) OR
       (PT_BARREL_ZONE5_MELT_301A >= PT_BARREL_ZONE5_MELT_301C AND PT_BARREL_ZONE5_MELT_301A <= PT_BARREL_ZONE5_MELT_301B) THEN
        rZone5Press_Voted_bar := PT_BARREL_ZONE5_MELT_301A;
    ELSIF (PT_BARREL_ZONE5_MELT_301B >= PT_BARREL_ZONE5_MELT_301A AND PT_BARREL_ZONE5_MELT_301B <= PT_BARREL_ZONE5_MELT_301C) OR
          (PT_BARREL_ZONE5_MELT_301B >= PT_BARREL_ZONE5_MELT_301C AND PT_BARREL_ZONE5_MELT_301B <= PT_BARREL_ZONE5_MELT_301A) THEN
        rZone5Press_Voted_bar := PT_BARREL_ZONE5_MELT_301B;
    ELSE
        rZone5Press_Voted_bar := PT_BARREL_ZONE5_MELT_301C;
    END_IF;
    IF (rZone5Press_Diff_AB > 6.0) OR (rZone5Press_Diff_BC > 6.0) OR (rZone5Press_Diff_CA > 6.0) THEN
        tZone5Press_DiscrepancyTimer(IN := TRUE, PT := T#300MS);
    ELSE
        tZone5Press_DiscrepancyTimer(IN := FALSE);
    END_IF;
ELSIF iZone5Press_HealthyCount = 2 THEN
    IF bZone5Press_A_Ok AND bZone5Press_B_Ok THEN
        rZone5Press_Voted_bar := (PT_BARREL_ZONE5_MELT_301A + PT_BARREL_ZONE5_MELT_301B) * 0.5;
    ELSIF bZone5Press_B_Ok AND bZone5Press_C_Ok THEN
        rZone5Press_Voted_bar := (PT_BARREL_ZONE5_MELT_301B + PT_BARREL_ZONE5_MELT_301C) * 0.5;
    ELSE
        rZone5Press_Voted_bar := (PT_BARREL_ZONE5_MELT_301A + PT_BARREL_ZONE5_MELT_301C) * 0.5;
    END_IF;
    tZone5Press_DiscrepancyTimer(IN := TRUE, PT := T#300MS);
ELSIF iZone5Press_HealthyCount = 1 THEN
    IF bZone5Press_A_Ok THEN rZone5Press_Voted_bar := PT_BARREL_ZONE5_MELT_301A;
    ELSIF bZone5Press_B_Ok THEN rZone5Press_Voted_bar := PT_BARREL_ZONE5_MELT_301B;
    ELSE rZone5Press_Voted_bar := PT_BARREL_ZONE5_MELT_301C; END_IF;
    tZone5Press_DiscrepancyTimer(IN := TRUE, PT := T#300MS);
ELSE
    rZone5Press_Voted_bar := 0.0;
    bZone5Press_DiscrepancyFault := TRUE;
END_IF;
bZone5Press_DiscrepancyFault := tZone5Press_DiscrepancyTimer.Q;

(* 1.5 Sensor Bank 5: Die Inlet / Gear Pump Suction Melt Pressure 401A/B/C (3.0 bar Trip Tol) *)
bDieInlet_A_Ok := (PT_DIE_INLET_PRESSURE_401A >= 0.0) AND (PT_DIE_INLET_PRESSURE_401A <= 120.0);
bDieInlet_B_Ok := (PT_DIE_INLET_PRESSURE_401B >= 0.0) AND (PT_DIE_INLET_PRESSURE_401B <= 120.0);
bDieInlet_C_Ok := (PT_DIE_INLET_PRESSURE_401C >= 0.0) AND (PT_DIE_INLET_PRESSURE_401C <= 120.0);
iDieInlet_HealthyCount := 0;
IF bDieInlet_A_Ok THEN iDieInlet_HealthyCount := iDieInlet_HealthyCount + 1; END_IF;
IF bDieInlet_B_Ok THEN iDieInlet_HealthyCount := iDieInlet_HealthyCount + 1; END_IF;
IF bDieInlet_C_Ok THEN iDieInlet_HealthyCount := iDieInlet_HealthyCount + 1; END_IF;
rDieInlet_Diff_AB := ABS(PT_DIE_INLET_PRESSURE_401A - PT_DIE_INLET_PRESSURE_401B);
rDieInlet_Diff_BC := ABS(PT_DIE_INLET_PRESSURE_401B - PT_DIE_INLET_PRESSURE_401C);
rDieInlet_Diff_CA := ABS(PT_DIE_INLET_PRESSURE_401C - PT_DIE_INLET_PRESSURE_401A);
IF iDieInlet_HealthyCount = 3 THEN
    IF (PT_DIE_INLET_PRESSURE_401A >= PT_DIE_INLET_PRESSURE_401B AND PT_DIE_INLET_PRESSURE_401A <= PT_DIE_INLET_PRESSURE_401C) OR
       (PT_DIE_INLET_PRESSURE_401A >= PT_DIE_INLET_PRESSURE_401C AND PT_DIE_INLET_PRESSURE_401A <= PT_DIE_INLET_PRESSURE_401B) THEN
        rDieInlet_Voted_bar := PT_DIE_INLET_PRESSURE_401A;
    ELSIF (PT_DIE_INLET_PRESSURE_401B >= PT_DIE_INLET_PRESSURE_401A AND PT_DIE_INLET_PRESSURE_401B <= PT_DIE_INLET_PRESSURE_401C) OR
          (PT_DIE_INLET_PRESSURE_401B >= PT_DIE_INLET_PRESSURE_401C AND PT_DIE_INLET_PRESSURE_401B <= PT_DIE_INLET_PRESSURE_401A) THEN
        rDieInlet_Voted_bar := PT_DIE_INLET_PRESSURE_401B;
    ELSE
        rDieInlet_Voted_bar := PT_DIE_INLET_PRESSURE_401C;
    END_IF;
    IF (rDieInlet_Diff_AB > 3.0) OR (rDieInlet_Diff_BC > 3.0) OR (rDieInlet_Diff_CA > 3.0) THEN
        tDieInlet_DiscrepancyTimer(IN := TRUE, PT := T#250MS);
    ELSE
        tDieInlet_DiscrepancyTimer(IN := FALSE);
    END_IF;
ELSIF iDieInlet_HealthyCount = 2 THEN
    IF bDieInlet_A_Ok AND bDieInlet_B_Ok THEN
        rDieInlet_Voted_bar := (PT_DIE_INLET_PRESSURE_401A + PT_DIE_INLET_PRESSURE_401B) * 0.5;
        IF rDieInlet_Diff_AB > 3.0 THEN tDieInlet_DiscrepancyTimer(IN := TRUE, PT := T#250MS); ELSE tDieInlet_DiscrepancyTimer(IN := FALSE); END_IF;
    ELSIF bDieInlet_B_Ok AND bDieInlet_C_Ok THEN
        rDieInlet_Voted_bar := (PT_DIE_INLET_PRESSURE_401B + PT_DIE_INLET_PRESSURE_401C) * 0.5;
        IF rDieInlet_Diff_BC > 3.0 THEN tDieInlet_DiscrepancyTimer(IN := TRUE, PT := T#250MS); ELSE tDieInlet_DiscrepancyTimer(IN := FALSE); END_IF;
    ELSE
        rDieInlet_Voted_bar := (PT_DIE_INLET_PRESSURE_401A + PT_DIE_INLET_PRESSURE_401C) * 0.5;
        IF rDieInlet_Diff_CA > 3.0 THEN tDieInlet_DiscrepancyTimer(IN := TRUE, PT := T#250MS); ELSE tDieInlet_DiscrepancyTimer(IN := FALSE); END_IF;
    END_IF;
ELSIF iDieInlet_HealthyCount = 1 THEN
    IF bDieInlet_A_Ok THEN rDieInlet_Voted_bar := PT_DIE_INLET_PRESSURE_401A;
    ELSIF bDieInlet_B_Ok THEN rDieInlet_Voted_bar := PT_DIE_INLET_PRESSURE_401B;
    ELSE rDieInlet_Voted_bar := PT_DIE_INLET_PRESSURE_401C; END_IF;
    tDieInlet_DiscrepancyTimer(IN := TRUE, PT := T#250MS);
ELSE
    rDieInlet_Voted_bar := 0.0;
    bDieInlet_DiscrepancyFault := TRUE;
END_IF;
bDieInlet_DiscrepancyFault := tDieInlet_DiscrepancyTimer.Q;
rGearPumpSuction_Voted_bar := rDieInlet_Voted_bar;

(* 1.6 Sensor Bank 6: True Melt Immersion Optical Pyrometer 501A/B/C *)
bPyro_A_Ok := (TT_MELT_TRUE_PYRO_501A >= 50.0) AND (TT_MELT_TRUE_PYRO_501A <= 350.0);
bPyro_B_Ok := (TT_MELT_TRUE_PYRO_501B >= 50.0) AND (TT_MELT_TRUE_PYRO_501B <= 350.0);
bPyro_C_Ok := (TT_MELT_TRUE_PYRO_501C >= 50.0) AND (TT_MELT_TRUE_PYRO_501C <= 350.0);
iPyro_HealthyCount := 0;
IF bPyro_A_Ok THEN iPyro_HealthyCount := iPyro_HealthyCount + 1; END_IF;
IF bPyro_B_Ok THEN iPyro_HealthyCount := iPyro_HealthyCount + 1; END_IF;
IF bPyro_C_Ok THEN iPyro_HealthyCount := iPyro_HealthyCount + 1; END_IF;
rPyro_Diff_AB := ABS(TT_MELT_TRUE_PYRO_501A - TT_MELT_TRUE_PYRO_501B);
rPyro_Diff_BC := ABS(TT_MELT_TRUE_PYRO_501B - TT_MELT_TRUE_PYRO_501C);
rPyro_Diff_CA := ABS(TT_MELT_TRUE_PYRO_501C - TT_MELT_TRUE_PYRO_501A);
IF iPyro_HealthyCount = 3 THEN
    IF (TT_MELT_TRUE_PYRO_501A >= TT_MELT_TRUE_PYRO_501B AND TT_MELT_TRUE_PYRO_501A <= TT_MELT_TRUE_PYRO_501C) OR
       (TT_MELT_TRUE_PYRO_501A >= TT_MELT_TRUE_PYRO_501C AND TT_MELT_TRUE_PYRO_501A <= TT_MELT_TRUE_PYRO_501B) THEN
        rPyro_Voted_degC := TT_MELT_TRUE_PYRO_501A;
    ELSIF (TT_MELT_TRUE_PYRO_501B >= TT_MELT_TRUE_PYRO_501A AND TT_MELT_TRUE_PYRO_501B <= TT_MELT_TRUE_PYRO_501C) OR
          (TT_MELT_TRUE_PYRO_501B >= TT_MELT_TRUE_PYRO_501C AND TT_MELT_TRUE_PYRO_501B <= TT_MELT_TRUE_PYRO_501A) THEN
        rPyro_Voted_degC := TT_MELT_TRUE_PYRO_501B;
    ELSE
        rPyro_Voted_degC := TT_MELT_TRUE_PYRO_501C;
    END_IF;
    IF (rPyro_Diff_AB > 4.0) OR (rPyro_Diff_BC > 4.0) OR (rPyro_Diff_CA > 4.0) THEN
        tPyro_DiscrepancyTimer(IN := TRUE, PT := T#400MS);
    ELSE
        tPyro_DiscrepancyTimer(IN := FALSE);
    END_IF;
ELSIF iPyro_HealthyCount = 2 THEN
    IF bPyro_A_Ok AND bPyro_B_Ok THEN
        rPyro_Voted_degC := (TT_MELT_TRUE_PYRO_501A + TT_MELT_TRUE_PYRO_501B) * 0.5;
    ELSIF bPyro_B_Ok AND bPyro_C_Ok THEN
        rPyro_Voted_degC := (TT_MELT_TRUE_PYRO_501B + TT_MELT_TRUE_PYRO_501C) * 0.5;
    ELSE
        rPyro_Voted_degC := (TT_MELT_TRUE_PYRO_501A + TT_MELT_TRUE_PYRO_501C) * 0.5;
    END_IF;
    tPyro_DiscrepancyTimer(IN := TRUE, PT := T#400MS);
ELSIF iPyro_HealthyCount = 1 THEN
    IF bPyro_A_Ok THEN rPyro_Voted_degC := TT_MELT_TRUE_PYRO_501A;
    ELSIF bPyro_B_Ok THEN rPyro_Voted_degC := TT_MELT_TRUE_PYRO_501B;
    ELSE rPyro_Voted_degC := TT_MELT_TRUE_PYRO_501C; END_IF;
    tPyro_DiscrepancyTimer(IN := TRUE, PT := T#400MS);
ELSE
    rPyro_Voted_degC := 200.0;
    bPyro_DiscrepancyFault := TRUE;
END_IF;
bPyro_DiscrepancyFault := tPyro_DiscrepancyTimer.Q;
rTrueMeltTemp_Voted_degC := rPyro_Voted_degC;

(* 1.7 Sensor Bank 7: Slit-Die Rheometer Multi-Tap Differential Pressure 601A/B/C (1.2 bar Threshold) *)
bSlitDP_A_Ok := (VISC_SLIT_DIE_RHEOMETER_601A >= 0.0) AND (VISC_SLIT_DIE_RHEOMETER_601A <= 180.0);
bSlitDP_B_Ok := (VISC_SLIT_DIE_RHEOMETER_601B >= 0.0) AND (VISC_SLIT_DIE_RHEOMETER_601B <= 180.0);
bSlitDP_C_Ok := (VISC_SLIT_DIE_RHEOMETER_601C >= 0.0) AND (VISC_SLIT_DIE_RHEOMETER_601C <= 180.0);
iSlitDP_HealthyCount := 0;
IF bSlitDP_A_Ok THEN iSlitDP_HealthyCount := iSlitDP_HealthyCount + 1; END_IF;
IF bSlitDP_B_Ok THEN iSlitDP_HealthyCount := iSlitDP_HealthyCount + 1; END_IF;
IF bSlitDP_C_Ok THEN iSlitDP_HealthyCount := iSlitDP_HealthyCount + 1; END_IF;
rSlitDP_Diff_AB := ABS(VISC_SLIT_DIE_RHEOMETER_601A - VISC_SLIT_DIE_RHEOMETER_601B);
rSlitDP_Diff_BC := ABS(VISC_SLIT_DIE_RHEOMETER_601B - VISC_SLIT_DIE_RHEOMETER_601C);
rSlitDP_Diff_CA := ABS(VISC_SLIT_DIE_RHEOMETER_601C - VISC_SLIT_DIE_RHEOMETER_601A);
IF iSlitDP_HealthyCount = 3 THEN
    IF (VISC_SLIT_DIE_RHEOMETER_601A >= VISC_SLIT_DIE_RHEOMETER_601B AND VISC_SLIT_DIE_RHEOMETER_601A <= VISC_SLIT_DIE_RHEOMETER_601C) OR
       (VISC_SLIT_DIE_RHEOMETER_601A >= VISC_SLIT_DIE_RHEOMETER_601C AND VISC_SLIT_DIE_RHEOMETER_601A <= VISC_SLIT_DIE_RHEOMETER_601B) THEN
        rSlitDP_Voted_bar := VISC_SLIT_DIE_RHEOMETER_601A;
    ELSIF (VISC_SLIT_DIE_RHEOMETER_601B >= VISC_SLIT_DIE_RHEOMETER_601A AND VISC_SLIT_DIE_RHEOMETER_601B <= VISC_SLIT_DIE_RHEOMETER_601C) OR
          (VISC_SLIT_DIE_RHEOMETER_601B >= VISC_SLIT_DIE_RHEOMETER_601C AND VISC_SLIT_DIE_RHEOMETER_601B <= VISC_SLIT_DIE_RHEOMETER_601A) THEN
        rSlitDP_Voted_bar := VISC_SLIT_DIE_RHEOMETER_601B;
    ELSE
        rSlitDP_Voted_bar := VISC_SLIT_DIE_RHEOMETER_601C;
    END_IF;
    IF (rSlitDP_Diff_AB > 1.2) OR (rSlitDP_Diff_BC > 1.2) OR (rSlitDP_Diff_CA > 1.2) THEN
        tSlitDP_DiscrepancyTimer(IN := TRUE, PT := T#200MS);
    ELSE
        tSlitDP_DiscrepancyTimer(IN := FALSE);
    END_IF;
ELSIF iSlitDP_HealthyCount = 2 THEN
    IF bSlitDP_A_Ok AND bSlitDP_B_Ok THEN
        rSlitDP_Voted_bar := (VISC_SLIT_DIE_RHEOMETER_601A + VISC_SLIT_DIE_RHEOMETER_601B) * 0.5;
        IF rSlitDP_Diff_AB > 1.2 THEN tSlitDP_DiscrepancyTimer(IN := TRUE, PT := T#200MS); ELSE tSlitDP_DiscrepancyTimer(IN := FALSE); END_IF;
    ELSIF bSlitDP_B_Ok AND bSlitDP_C_Ok THEN
        rSlitDP_Voted_bar := (VISC_SLIT_DIE_RHEOMETER_601B + VISC_SLIT_DIE_RHEOMETER_601C) * 0.5;
        IF rSlitDP_Diff_BC > 1.2 THEN tSlitDP_DiscrepancyTimer(IN := TRUE, PT := T#200MS); ELSE tSlitDP_DiscrepancyTimer(IN := FALSE); END_IF;
    ELSE
        rSlitDP_Voted_bar := (VISC_SLIT_DIE_RHEOMETER_601A + VISC_SLIT_DIE_RHEOMETER_601C) * 0.5;
        IF rSlitDP_Diff_CA > 1.2 THEN tSlitDP_DiscrepancyTimer(IN := TRUE, PT := T#200MS); ELSE tSlitDP_DiscrepancyTimer(IN := FALSE); END_IF;
    END_IF;
ELSIF iSlitDP_HealthyCount = 1 THEN
    IF bSlitDP_A_Ok THEN rSlitDP_Voted_bar := VISC_SLIT_DIE_RHEOMETER_601A;
    ELSIF bSlitDP_B_Ok THEN rSlitDP_Voted_bar := VISC_SLIT_DIE_RHEOMETER_601B;
    ELSE rSlitDP_Voted_bar := VISC_SLIT_DIE_RHEOMETER_601C; END_IF;
    tSlitDP_DiscrepancyTimer(IN := TRUE, PT := T#200MS);
ELSE
    rSlitDP_Voted_bar := 0.0;
    bSlitDP_DiscrepancyFault := TRUE;
END_IF;
bSlitDP_DiscrepancyFault := tSlitDP_DiscrepancyTimer.Q;

(* 1.8 Sensor Bank 8: Twin-Screw Motor Speed 701A/B/C *)
bScrewSpeed_A_Ok := (ST_SCREW_MOTOR_SPEED_701A >= 0.0) AND (ST_SCREW_MOTOR_SPEED_701A <= 1400.0);
bScrewSpeed_B_Ok := (ST_SCREW_MOTOR_SPEED_701B >= 0.0) AND (ST_SCREW_MOTOR_SPEED_701B <= 1400.0);
bScrewSpeed_C_Ok := (ST_SCREW_MOTOR_SPEED_701C >= 0.0) AND (ST_SCREW_MOTOR_SPEED_701C <= 1400.0);
iScrewSpeed_HealthyCount := 0;
IF bScrewSpeed_A_Ok THEN iScrewSpeed_HealthyCount := iScrewSpeed_HealthyCount + 1; END_IF;
IF bScrewSpeed_B_Ok THEN iScrewSpeed_HealthyCount := iScrewSpeed_HealthyCount + 1; END_IF;
IF bScrewSpeed_C_Ok THEN iScrewSpeed_HealthyCount := iScrewSpeed_HealthyCount + 1; END_IF;
rScrewSpeed_Diff_AB := ABS(ST_SCREW_MOTOR_SPEED_701A - ST_SCREW_MOTOR_SPEED_701B);
rScrewSpeed_Diff_BC := ABS(ST_SCREW_MOTOR_SPEED_701B - ST_SCREW_MOTOR_SPEED_701C);
rScrewSpeed_Diff_CA := ABS(ST_SCREW_MOTOR_SPEED_701C - ST_SCREW_MOTOR_SPEED_701A);
IF iScrewSpeed_HealthyCount = 3 THEN
    IF (ST_SCREW_MOTOR_SPEED_701A >= ST_SCREW_MOTOR_SPEED_701B AND ST_SCREW_MOTOR_SPEED_701A <= ST_SCREW_MOTOR_SPEED_701C) OR
       (ST_SCREW_MOTOR_SPEED_701A >= ST_SCREW_MOTOR_SPEED_701C AND ST_SCREW_MOTOR_SPEED_701A <= ST_SCREW_MOTOR_SPEED_701B) THEN
        rScrewSpeed_Voted_rpm := ST_SCREW_MOTOR_SPEED_701A;
    ELSIF (ST_SCREW_MOTOR_SPEED_701B >= ST_SCREW_MOTOR_SPEED_701A AND ST_SCREW_MOTOR_SPEED_701B <= ST_SCREW_MOTOR_SPEED_701C) OR
          (ST_SCREW_MOTOR_SPEED_701B >= ST_SCREW_MOTOR_SPEED_701C AND ST_SCREW_MOTOR_SPEED_701B <= ST_SCREW_MOTOR_SPEED_701A) THEN
        rScrewSpeed_Voted_rpm := ST_SCREW_MOTOR_SPEED_701B;
    ELSE
        rScrewSpeed_Voted_rpm := ST_SCREW_MOTOR_SPEED_701C;
    END_IF;
    IF (rScrewSpeed_Diff_AB > 8.0) OR (rScrewSpeed_Diff_BC > 8.0) OR (rScrewSpeed_Diff_CA > 8.0) THEN
        tScrewSpeed_DiscrepancyTimer(IN := TRUE, PT := T#150MS);
    ELSE
        tScrewSpeed_DiscrepancyTimer(IN := FALSE);
    END_IF;
ELSIF iScrewSpeed_HealthyCount = 2 THEN
    IF bScrewSpeed_A_Ok AND bScrewSpeed_B_Ok THEN
        rScrewSpeed_Voted_rpm := (ST_SCREW_MOTOR_SPEED_701A + ST_SCREW_MOTOR_SPEED_701B) * 0.5;
    ELSIF bScrewSpeed_B_Ok AND bScrewSpeed_C_Ok THEN
        rScrewSpeed_Voted_rpm := (ST_SCREW_MOTOR_SPEED_701B + ST_SCREW_MOTOR_SPEED_701C) * 0.5;
    ELSE
        rScrewSpeed_Voted_rpm := (ST_SCREW_MOTOR_SPEED_701A + ST_SCREW_MOTOR_SPEED_701C) * 0.5;
    END_IF;
    tScrewSpeed_DiscrepancyTimer(IN := TRUE, PT := T#150MS);
ELSIF iScrewSpeed_HealthyCount = 1 THEN
    IF bScrewSpeed_A_Ok THEN rScrewSpeed_Voted_rpm := ST_SCREW_MOTOR_SPEED_701A;
    ELSIF bScrewSpeed_B_Ok THEN rScrewSpeed_Voted_rpm := ST_SCREW_MOTOR_SPEED_701B;
    ELSE rScrewSpeed_Voted_rpm := ST_SCREW_MOTOR_SPEED_701C; END_IF;
    tScrewSpeed_DiscrepancyTimer(IN := TRUE, PT := T#150MS);
ELSE
    rScrewSpeed_Voted_rpm := 0.0;
    bScrewSpeed_DiscrepancyFault := TRUE;
END_IF;
bScrewSpeed_DiscrepancyFault := tScrewSpeed_DiscrepancyTimer.Q;

(* 1.9 Pack Sensor Health Bitmask *)
dwSensorHealthMask := 16#00000000;
IF bMainFeeder_A_Ok THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00000001; END_IF;
IF bMainFeeder_B_Ok THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00000002; END_IF;
IF bMainFeeder_C_Ok THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00000004; END_IF;
IF bSideFeeder_A_Ok THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00000008; END_IF;
IF bSideFeeder_B_Ok THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00000010; END_IF;
IF bSideFeeder_C_Ok THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00000020; END_IF;
IF bPeroxide_A_Ok   THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00000040; END_IF;
IF bPeroxide_B_Ok   THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00000080; END_IF;
IF bPeroxide_C_Ok   THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00000100; END_IF;
IF bDieInlet_A_Ok   THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00000200; END_IF;
IF bDieInlet_B_Ok   THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00000400; END_IF;
IF bDieInlet_C_Ok   THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00000800; END_IF;
IF bPyro_A_Ok       THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00001000; END_IF;
IF bPyro_B_Ok       THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00002000; END_IF;
IF bPyro_C_Ok       THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00004000; END_IF;
IF bSlitDP_A_Ok     THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00008000; END_IF;
IF bSlitDP_B_Ok     THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00010000; END_IF;
IF bSlitDP_C_Ok     THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00020000; END_IF;
IF bScrewSpeed_A_Ok THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00040000; END_IF;
IF bScrewSpeed_B_Ok THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00080000; END_IF;
IF bScrewSpeed_C_Ok THEN dwSensorHealthMask := dwSensorHealthMask OR 16#00100000; END_IF;

(* ==================================================================================================== *)
(* === PHASE 2: IN-LINE SLIT-DIE RHEOMETER TRUE SHEAR VISCOSITY & CROSS-WLF OBSERVER                === *)
(* ==================================================================================================== *)

(* 2.1 Slit-Die Geometry & Real-Time Melt Density Calculation *)
rMeltDensity_Actual := (c_rPolymerDensity_Melt0 / (1.0 + (c_rThermalExpansionBeta * (rTrueMeltTemp_Voted_degC - 200.0)))) *
                       (1.0 + (c_rCompressibilityBetaP * rTargetDiePressure_bar));
IF rMeltDensity_Actual < 600.0 THEN rMeltDensity_Actual := 600.0; END_IF;
IF rMeltDensity_Actual > 850.0 THEN rMeltDensity_Actual := 850.0; END_IF;

rSlitCrossSectionArea_m2 := (rSlitDieWidth_mm * 0.001) * (rSlitDieGap_mm * 0.001);
rSlitChannelVolume_m3 := rSlitCrossSectionArea_m2 * (rSlitDieLength_mm * 0.001);

IF (rMainFeeder_Voted_kgh + rSideFeeder_Voted_kgh) > 10.0 THEN
    rVolumetricThroughput_m3s := (rMainFeeder_Voted_kgh + rSideFeeder_Voted_kgh) / (rMeltDensity_Actual * 3600.0);
ELSE
    rVolumetricThroughput_m3s := 0.000001;
END_IF;

(* 2.2 Apparent Shear Rate & Wall Shear Stress *)
IF (rSlitDieWidth_mm > 1.0) AND (rSlitDieGap_mm > 0.1) THEN
    rSlitApparentShearRate_invs := (6.0 * rVolumetricThroughput_m3s) /
                                   ((rSlitDieWidth_mm * 0.001) * (rSlitDieGap_mm * 0.001) * (rSlitDieGap_mm * 0.001));
ELSE
    rSlitApparentShearRate_invs := 10.0;
END_IF;
IF rSlitApparentShearRate_invs < 0.1 THEN rSlitApparentShearRate_invs := 0.1; END_IF;

IF rSlitDieLength_mm > 5.0 THEN
    rSlitWallShearStress_Pa := ((rSlitDieGap_mm * 0.001) * (rSlitDP_Voted_bar * 100000.0)) / (2.0 * (rSlitDieLength_mm * 0.001));
ELSE
    rSlitWallShearStress_Pa := 1000.0;
END_IF;
rSlitDieShearStress_kPa := rSlitWallShearStress_Pa * 0.001;

(* 2.3 Weissenberg-Rabinowitsch Shear Rate Correction *)
rTempCalc_A := EXPT(c_rCross_Lambda0 * rSlitApparentShearRate_invs, 1.0 - c_rCross_PowerIndex_n);
rNonNewtonianIndex_neff := 1.0 - (((1.0 - c_rCross_PowerIndex_n) * rTempCalc_A) / (1.0 + rTempCalc_A));
IF rNonNewtonianIndex_neff < 0.15 THEN rNonNewtonianIndex_neff := 0.15; END_IF;
IF rNonNewtonianIndex_neff > 0.95 THEN rNonNewtonianIndex_neff := 0.95; END_IF;

rRabinowitschFactor_b := ((2.0 * rNonNewtonianIndex_neff) + 1.0) / (3.0 * rNonNewtonianIndex_neff);
rSlitTrueWallShearRate_invs := rSlitApparentShearRate_invs * rRabinowitschFactor_b;
rSlitDieShearRate_invs := rSlitTrueWallShearRate_invs;

IF rSlitTrueWallShearRate_invs > 0.01 THEN
    rDynamicViscosity_Pas := rSlitWallShearStress_Pa / rSlitTrueWallShearRate_invs;
ELSE
    rDynamicViscosity_Pas := 1000.0;
END_IF;
IF rDynamicViscosity_Pas < 10.0 THEN rDynamicViscosity_Pas := 10.0; END_IF;
IF rDynamicViscosity_Pas > 15000.0 THEN rDynamicViscosity_Pas := 15000.0; END_IF;
rObservedViscosity_Pas := rDynamicViscosity_Pas;

(* 2.4 Cross-WLF Theoretical Viscosity Model Formulation *)
rAbsoluteMeltTemp_K := rTrueMeltTemp_Voted_degC + 273.15;
rTempCalc_B := rAbsoluteMeltTemp_K - c_rCross_Tstar;
IF (c_rCross_A2 + rTempCalc_B) > 1.0 THEN
    rWLF_ShiftFactor_aT := EXP((-1.0 * c_rCross_A1 * rTempCalc_B) / (c_rCross_A2 + rTempCalc_B));
ELSE
    rWLF_ShiftFactor_aT := 1.0;
END_IF;

rZeroShearViscosity_Eta0 := c_rCross_D1 * rWLF_ShiftFactor_aT * EXP(c_rCompressibilityBetaP * rTargetDiePressure_bar);
IF rZeroShearViscosity_Eta0 < 100.0 THEN rZeroShearViscosity_Eta0 := 100.0; END_IF;
IF rZeroShearViscosity_Eta0 > 500000.0 THEN rZeroShearViscosity_Eta0 := 500000.0; END_IF;

rTempCalc_C := EXPT(c_rCross_Lambda0 * rSlitTrueWallShearRate_invs, 1.0 - c_rCross_PowerIndex_n);
rCrossModelViscosity_Pas := rZeroShearViscosity_Eta0 / (1.0 + rTempCalc_C);
rViscosityModelResidual_Pas := rDynamicViscosity_Pas - rCrossModelViscosity_Pas;

(* 2.5 In-Line Melt Flow Index (MFI) Observer *)
rStandardMFI_ShearViscosity_Pas := rZeroShearViscosity_Eta0 / (1.0 + EXPT(c_rCross_Lambda0 * 32.5, 1.0 - c_rCross_PowerIndex_n));
IF rStandardMFI_ShearViscosity_Pas > 10.0 THEN
    rCalculatedMFI_Online := 142000.0 * EXPT(rStandardMFI_ShearViscosity_Pas, -1.58);
ELSE
    rCalculatedMFI_Online := rTargetMFI_g10min;
END_IF;
IF rCalculatedMFI_Online < 0.1 THEN rCalculatedMFI_Online := 0.1; END_IF;
IF rCalculatedMFI_Online > 120.0 THEN rCalculatedMFI_Online := 120.0; END_IF;
rEstimatedMFI_g10min := rCalculatedMFI_Online;

IF rTargetMFI_g10min > 0.05 THEN
    rMFI_TrackingError_pct := ((rCalculatedMFI_Online - rTargetMFI_g10min) / rTargetMFI_g10min) * 100.0;
ELSE
    rMFI_TrackingError_pct := 0.0;
END_IF;

(* ==================================================================================================== *)
(* === PHASE 3: FREE-RADICAL GRAFTING REACTION KINETICS & TWIN-SCREW VISCOUS DISSIPATION ENGINE      === *)
(* ==================================================================================================== *)

(* 3.1 Arrhenius Free-Radical Thermal Decomposition Kinetics *)
(* Thermal decay rate: kd = A0 * exp(-Ea / (R * T)) [1/s] *)
IF rAbsoluteMeltTemp_K > 350.0 THEN
    rPeroxideDecayConstant_kd := c_rArrhenius_A0 * EXP(-1.0 * c_rArrhenius_Ea / (c_rGasConstant_R * rAbsoluteMeltTemp_K));
ELSE
    rPeroxideDecayConstant_kd := 0.0001;
END_IF;

IF rPeroxideDecayConstant_kd > 0.000001 THEN
    rPeroxideHalfLife_s := 0.693147 / rPeroxideDecayConstant_kd;
ELSE
    rPeroxideHalfLife_s := 999.0;
END_IF;

(* Mean residence time in reactive grafting zone (Zones 6 through 8 = 32% of active channel volume) *)
IF (rMainFeeder_Voted_kgh + rSideFeeder_Voted_kgh) > 10.0 THEN
    rReactiveZoneTransitTime_s := (c_rScrewChannelNetVolume_m3 * 0.32 * rMeltDensity_Actual * 3600.0) /
                                  (rMainFeeder_Voted_kgh + rSideFeeder_Voted_kgh);
ELSE
    rReactiveZoneTransitTime_s := 45.0;
END_IF;
IF rReactiveZoneTransitTime_s < 2.0 THEN rReactiveZoneTransitTime_s := 2.0; END_IF;
IF rReactiveZoneTransitTime_s > 180.0 THEN rReactiveZoneTransitTime_s := 180.0; END_IF;
rResinResidenceTime_s := rReactiveZoneTransitTime_s / 0.32;

(* Undecomposed residual peroxide fraction: X_res = exp(-kd * t_transit) *)
rPeroxideResidualFraction := EXP(-1.0 * rPeroxideDecayConstant_kd * rReactiveZoneTransitTime_s);
rPeroxideConversionYield := 1.0 - rPeroxideResidualFraction;

(* Primary radical generation flux: Ri = 2 * f * kd * [Peroxide] [mol/(m3*s)] *)
IF (rMainFeeder_Voted_kgh + rSideFeeder_Voted_kgh) > 10.0 THEN
    rPrimaryRadicalFlux_mol_m3s := (2.0 * c_rRadicalEfficiency_f * rPeroxideDecayConstant_kd *
                                   (rPeroxide_Voted_kgh / 3600.0) * 1000.0) /
                                   (c_rPeroxideMolarMass * (rVolumetricThroughput_m3s + 0.000001));
ELSE
    rPrimaryRadicalFlux_mol_m3s := 0.0;
END_IF;

(* 3.2 Monomer Grafting vs. Beta-Scission Degradation Kinetics *)
IF (rMainFeeder_Voted_kgh + rSideFeeder_Voted_kgh) > 10.0 THEN
    rTempCalc_A := (rSideFeeder_Voted_kgh / (rMainFeeder_Voted_kgh + rSideFeeder_Voted_kgh)) * 100.0;
ELSE
    rTempCalc_A := 0.0;
END_IF;

(* Grafting conversion yield: alpha_g = alpha_max * (K_g * [M] * sqrt(Ri) / (1 + K_t * [M])) * (1 - exp(-t/tau)) *)
IF rPrimaryRadicalFlux_mol_m3s > 0.00001 THEN
    rGraftingReactionRate_mol_m3s := 1.85 * rTempCalc_A * SQRT(rPrimaryRadicalFlux_mol_m3s) / (1.0 + (0.42 * rTempCalc_A));
    rCalculatedGraftingConversion := 92.5 * (rGraftingReactionRate_mol_m3s / (rGraftingReactionRate_mol_m3s + 0.15)) *
                                     (1.0 - EXP(-1.0 * rReactiveZoneTransitTime_s / 6.5));
ELSE
    rGraftingReactionRate_mol_m3s := 0.0;
    rCalculatedGraftingConversion := 0.0;
END_IF;
IF rCalculatedGraftingConversion < 0.0 THEN rCalculatedGraftingConversion := 0.0; END_IF;
IF rCalculatedGraftingConversion > 98.5 THEN rCalculatedGraftingConversion := 98.5; END_IF;
rGraftingConversion_pct := rCalculatedGraftingConversion;

(* Beta-scission degradation factor: reduces average molecular weight and increases MFI *)
rBetaScissionChainDegradationFactor := 0.00085 * rPrimaryRadicalFlux_mol_m3s * rReactiveZoneTransitTime_s;

(* 3.3 Twin-Screw Shear Dynamics & Viscous Dissipation Heat Generation *)
(* Flight clearance shear rate: gamma_dot_clear = pi * D * N / delta *)
rScrewClearanceShearRate_invs := (3.141592 * c_rScrewDiameter_m * (rScrewSpeed_Voted_rpm / 60.0)) / c_rFlightClearance_m;
(* Channel shear rate: gamma_dot_chan = pi * D * N / h *)
rScrewChannelShearRate_invs := (3.141592 * c_rScrewDiameter_m * (rScrewSpeed_Voted_rpm / 60.0)) / c_rChannelDepth_m;

(* Channel degree of fill calculation: theta_fill = Q / (Q_drag_max) *)
IF rScrewSpeed_Voted_rpm > 1.0 THEN
    rChannelFillDegree_Fraction := (rVolumetricThroughput_m3s) /
                                   (c_rScrewFlightStarts * c_rScrewFlightPitch_m * 3.141592 * c_rScrewDiameter_m *
                                    c_rChannelDepth_m * (rScrewSpeed_Voted_rpm / 60.0) * 0.5);
ELSE
    rChannelFillDegree_Fraction := 1.0;
END_IF;
IF rChannelFillDegree_Fraction < 0.05 THEN rChannelFillDegree_Fraction := 0.05; END_IF;
IF rChannelFillDegree_Fraction > 1.00 THEN rChannelFillDegree_Fraction := 1.00; END_IF;
rDegreeOfFill_pct := rChannelFillDegree_Fraction * 100.0;

(* Viscous thermal dissipation power in clearance and channel [kW] *)
rTempCalc_B := (c_rCross_D1 * rWLF_ShiftFactor_aT) / (1.0 + EXPT(c_rCross_Lambda0 * rScrewClearanceShearRate_invs, 1.0 - c_rCross_PowerIndex_n));
rViscousHeatFlux_Clearance_kW := (rTempCalc_B * rScrewClearanceShearRate_invs * rScrewClearanceShearRate_invs *
                                 (3.141592 * c_rScrewDiameter_m * c_rFlightClearance_m * c_rScrewLength_m * 0.08)) * 0.001;

rTempCalc_C := (c_rCross_D1 * rWLF_ShiftFactor_aT) / (1.0 + EXPT(c_rCross_Lambda0 * rScrewChannelShearRate_invs, 1.0 - c_rCross_PowerIndex_n));
rViscousHeatFlux_Channel_kW := (rTempCalc_C * rScrewChannelShearRate_invs * rScrewChannelShearRate_invs *
                               (c_rScrewChannelNetVolume_m3 * rChannelFillDegree_Fraction)) * 0.001;

rTotalViscousDissipation_kW := rViscousHeatFlux_Clearance_kW + rViscousHeatFlux_Channel_kW;

(* Mechanical shaft drive power & Specific Mechanical Energy (SME) *)
(* Rated motor torque: 12,000 Nm. Power = 2 * pi * N * Torque / 60,000 [kW] *)
rTheoreticalMechanicalPower_kW := (2.0 * 3.141592 * (rScrewSpeed_Voted_rpm / 60.0) *
                                  ((rScrewMotorTorque_pct * 0.01) * 12000.0)) * 0.001;

IF (rMainFeeder_Voted_kgh + rSideFeeder_Voted_kgh) > 10.0 THEN
    rSpecificMechanicalEnergy_kWh_t := rTheoreticalMechanicalPower_kW /
                                       ((rMainFeeder_Voted_kgh + rSideFeeder_Voted_kgh) * 0.001);
ELSE
    rSpecificMechanicalEnergy_kWh_t := 0.0;
END_IF;
rCalculatedSME_kWh_ton := rSpecificMechanicalEnergy_kWh_t;
'''

with open('scratch/code_part2.st', 'w', encoding='utf-8') as f:
    f.write(code_part2)
print("Part 2 written, len =", len(code_part2))
