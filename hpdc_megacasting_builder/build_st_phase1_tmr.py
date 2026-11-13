# hpdc_megacasting_builder/build_st_phase1_tmr.py

def get_phase1_tmr():
    return """(* =====================================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DYNAMIC DISCREPANCY TIMERS
 * Millisecond-by-millisecond cross-channel verification across 7 critical safety and closed-loop process channels:
 *   1. Injection Cylinder Head Hydraulic Pressure PT-101A/B/C [bar]
 *   2. Injection Cylinder Rod Hydraulic Pressure PT-201A/B/C [bar]
 *   3. Plunger Optical Linear Absolute Scale ENC-301A/B/C [mm]
 *   4. Cavity Vacuum Absolute Transducers VPT-401A/B/C [mbar]
 *   5. Hydraulic Accumulator High-Pressure Transducers PT-501A/B/C [bar]
 *   6. Main Clamping Force Load Cells LC-601A/B/C [kN]
 *   7. Shot Sleeve Melt Pouring Thermocouples TT-701A/B/C [deg C]
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL 1: PT-101 INJECTION CYLINDER HEAD PRESSURE (TMR VOTING & FAULT DEGRADATION)
 * --------------------------------------------------------------------------------------------------------------------- *)
rTMR_PT101_DevAB := ABS(rCylHeadPres_PT101A_In - rCylHeadPres_PT101B_In);
rTMR_PT101_DevBC := ABS(rCylHeadPres_PT101B_In - rCylHeadPres_PT101C_In);
rTMR_PT101_DevCA := ABS(rCylHeadPres_PT101C_In - rCylHeadPres_PT101A_In);

(* Sensor A Discrepancy Timer Evaluation *)
IF (rTMR_PT101_DevAB > rTMR_Tol_Pres_PT101) AND (rTMR_PT101_DevCA > rTMR_Tol_Pres_PT101) THEN
    rTMR_PT101_TimerA := rTMR_PT101_TimerA + 1.0;
    IF rTMR_PT101_TimerA >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_PT101_HealthyA := FALSE;
    END_IF;
ELSE
    IF rTMR_PT101_TimerA > 0.0 THEN
        rTMR_PT101_TimerA := rTMR_PT101_TimerA - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_PT101_HealthyA := TRUE;
        rTMR_PT101_TimerA := 0.0;
    END_IF;
END_IF;

(* Sensor B Discrepancy Timer Evaluation *)
IF (rTMR_PT101_DevAB > rTMR_Tol_Pres_PT101) AND (rTMR_PT101_DevBC > rTMR_Tol_Pres_PT101) THEN
    rTMR_PT101_TimerB := rTMR_PT101_TimerB + 1.0;
    IF rTMR_PT101_TimerB >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_PT101_HealthyB := FALSE;
    END_IF;
ELSE
    IF rTMR_PT101_TimerB > 0.0 THEN
        rTMR_PT101_TimerB := rTMR_PT101_TimerB - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_PT101_HealthyB := TRUE;
        rTMR_PT101_TimerB := 0.0;
    END_IF;
END_IF;

(* Sensor C Discrepancy Timer Evaluation *)
IF (rTMR_PT101_DevBC > rTMR_Tol_Pres_PT101) AND (rTMR_PT101_DevCA > rTMR_Tol_Pres_PT101) THEN
    rTMR_PT101_TimerC := rTMR_PT101_TimerC + 1.0;
    IF rTMR_PT101_TimerC >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_PT101_HealthyC := FALSE;
    END_IF;
ELSE
    IF rTMR_PT101_TimerC > 0.0 THEN
        rTMR_PT101_TimerC := rTMR_PT101_TimerC - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_PT101_HealthyC := TRUE;
        rTMR_PT101_TimerC := 0.0;
    END_IF;
END_IF;

(* Voted Calculation with Bumpless Degradation *)
IF bTMR_PT101_HealthyA AND bTMR_PT101_HealthyB AND bTMR_PT101_HealthyC THEN
    iTMR_PT101_DegradeMode := 3; (* 2oo3 Healthy *)
    IF ((rCylHeadPres_PT101A_In >= rCylHeadPres_PT101B_In) AND (rCylHeadPres_PT101A_In <= rCylHeadPres_PT101C_In)) OR
       ((rCylHeadPres_PT101A_In <= rCylHeadPres_PT101B_In) AND (rCylHeadPres_PT101A_In >= rCylHeadPres_PT101C_In)) THEN
        rTMR_PT101_Voted := rCylHeadPres_PT101A_In;
    ELSIF ((rCylHeadPres_PT101B_In >= rCylHeadPres_PT101A_In) AND (rCylHeadPres_PT101B_In <= rCylHeadPres_PT101C_In)) OR
          ((rCylHeadPres_PT101B_In <= rCylHeadPres_PT101A_In) AND (rCylHeadPres_PT101B_In >= rCylHeadPres_PT101C_In)) THEN
        rTMR_PT101_Voted := rCylHeadPres_PT101B_In;
    ELSE
        rTMR_PT101_Voted := rCylHeadPres_PT101C_In;
    END_IF;
ELSIF bTMR_PT101_HealthyA AND bTMR_PT101_HealthyB THEN
    iTMR_PT101_DegradeMode := 2; (* 1oo2 Degraded *)
    rTMR_PT101_Voted := (rCylHeadPres_PT101A_In + rCylHeadPres_PT101B_In) * 0.5;
ELSIF bTMR_PT101_HealthyB AND bTMR_PT101_HealthyC THEN
    iTMR_PT101_DegradeMode := 2;
    rTMR_PT101_Voted := (rCylHeadPres_PT101B_In + rCylHeadPres_PT101C_In) * 0.5;
ELSIF bTMR_PT101_HealthyA AND bTMR_PT101_HealthyC THEN
    iTMR_PT101_DegradeMode := 2;
    rTMR_PT101_Voted := (rCylHeadPres_PT101A_In + rCylHeadPres_PT101C_In) * 0.5;
ELSIF bTMR_PT101_HealthyA THEN
    iTMR_PT101_DegradeMode := 1; (* Single Sensor Failover *)
    rTMR_PT101_Voted := rCylHeadPres_PT101A_In;
ELSIF bTMR_PT101_HealthyB THEN
    iTMR_PT101_DegradeMode := 1;
    rTMR_PT101_Voted := rCylHeadPres_PT101B_In;
ELSIF bTMR_PT101_HealthyC THEN
    iTMR_PT101_DegradeMode := 1;
    rTMR_PT101_Voted := rCylHeadPres_PT101C_In;
ELSE
    iTMR_PT101_DegradeMode := 0; (* Complete Channel Failure *)
    bAlarm_TMR_MajorDegrade := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL 2: PT-201 INJECTION CYLINDER ROD PRESSURE (TMR VOTING & FAULT DEGRADATION)
 * --------------------------------------------------------------------------------------------------------------------- *)
rTMR_PT201_DevAB := ABS(rCylRodPres_PT201A_In - rCylRodPres_PT201B_In);
rTMR_PT201_DevBC := ABS(rCylRodPres_PT201B_In - rCylRodPres_PT201C_In);
rTMR_PT201_DevCA := ABS(rCylRodPres_PT201C_In - rCylRodPres_PT201A_In);

IF (rTMR_PT201_DevAB > rTMR_Tol_Pres_PT201) AND (rTMR_PT201_DevCA > rTMR_Tol_Pres_PT201) THEN
    rTMR_PT201_TimerA := rTMR_PT201_TimerA + 1.0;
    IF rTMR_PT201_TimerA >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_PT201_HealthyA := FALSE;
    END_IF;
ELSE
    IF rTMR_PT201_TimerA > 0.0 THEN
        rTMR_PT201_TimerA := rTMR_PT201_TimerA - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_PT201_HealthyA := TRUE;
        rTMR_PT201_TimerA := 0.0;
    END_IF;
END_IF;

IF (rTMR_PT201_DevAB > rTMR_Tol_Pres_PT201) AND (rTMR_PT201_DevBC > rTMR_Tol_Pres_PT201) THEN
    rTMR_PT201_TimerB := rTMR_PT201_TimerB + 1.0;
    IF rTMR_PT201_TimerB >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_PT201_HealthyB := FALSE;
    END_IF;
ELSE
    IF rTMR_PT201_TimerB > 0.0 THEN
        rTMR_PT201_TimerB := rTMR_PT201_TimerB - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_PT201_HealthyB := TRUE;
        rTMR_PT201_TimerB := 0.0;
    END_IF;
END_IF;

IF (rTMR_PT201_DevBC > rTMR_Tol_Pres_PT201) AND (rTMR_PT201_DevCA > rTMR_Tol_Pres_PT201) THEN
    rTMR_PT201_TimerC := rTMR_PT201_TimerC + 1.0;
    IF rTMR_PT201_TimerC >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_PT201_HealthyC := FALSE;
    END_IF;
ELSE
    IF rTMR_PT201_TimerC > 0.0 THEN
        rTMR_PT201_TimerC := rTMR_PT201_TimerC - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_PT201_HealthyC := TRUE;
        rTMR_PT201_TimerC := 0.0;
    END_IF;
END_IF;

IF bTMR_PT201_HealthyA AND bTMR_PT201_HealthyB AND bTMR_PT201_HealthyC THEN
    iTMR_PT201_DegradeMode := 3;
    IF ((rCylRodPres_PT201A_In >= rCylRodPres_PT201B_In) AND (rCylRodPres_PT201A_In <= rCylRodPres_PT201C_In)) OR
       ((rCylRodPres_PT201A_In <= rCylRodPres_PT201B_In) AND (rCylRodPres_PT201A_In >= rCylRodPres_PT201C_In)) THEN
        rTMR_PT201_Voted := rCylRodPres_PT201A_In;
    ELSIF ((rCylRodPres_PT201B_In >= rCylRodPres_PT201A_In) AND (rCylRodPres_PT201B_In <= rCylRodPres_PT201C_In)) OR
          ((rCylRodPres_PT201B_In <= rCylRodPres_PT201A_In) AND (rCylRodPres_PT201B_In >= rCylRodPres_PT201C_In)) THEN
        rTMR_PT201_Voted := rCylRodPres_PT201B_In;
    ELSE
        rTMR_PT201_Voted := rCylRodPres_PT201C_In;
    END_IF;
ELSIF bTMR_PT201_HealthyA AND bTMR_PT201_HealthyB THEN
    iTMR_PT201_DegradeMode := 2;
    rTMR_PT201_Voted := (rCylRodPres_PT201A_In + rCylRodPres_PT201B_In) * 0.5;
ELSIF bTMR_PT201_HealthyB AND bTMR_PT201_HealthyC THEN
    iTMR_PT201_DegradeMode := 2;
    rTMR_PT201_Voted := (rCylRodPres_PT201B_In + rCylRodPres_PT201C_In) * 0.5;
ELSIF bTMR_PT201_HealthyA AND bTMR_PT201_HealthyC THEN
    iTMR_PT201_DegradeMode := 2;
    rTMR_PT201_Voted := (rCylRodPres_PT201A_In + rCylRodPres_PT201C_In) * 0.5;
ELSIF bTMR_PT201_HealthyA THEN
    iTMR_PT201_DegradeMode := 1;
    rTMR_PT201_Voted := rCylRodPres_PT201A_In;
ELSIF bTMR_PT201_HealthyB THEN
    iTMR_PT201_DegradeMode := 1;
    rTMR_PT201_Voted := rCylRodPres_PT201B_In;
ELSIF bTMR_PT201_HealthyC THEN
    iTMR_PT201_DegradeMode := 1;
    rTMR_PT201_Voted := rCylRodPres_PT201C_In;
ELSE
    iTMR_PT201_DegradeMode := 0;
    bAlarm_TMR_MajorDegrade := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL 3: ENC-301 PLUNGER LINEAR ABSOLUTE OPTICAL SCALE (TMR VOTING & FAULT DEGRADATION)
 * --------------------------------------------------------------------------------------------------------------------- *)
rTMR_ENC301_DevAB := ABS(rPlungerPos_ENC301A_In - rPlungerPos_ENC301B_In);
rTMR_ENC301_DevBC := ABS(rPlungerPos_ENC301B_In - rPlungerPos_ENC301C_In);
rTMR_ENC301_DevCA := ABS(rPlungerPos_ENC301C_In - rPlungerPos_ENC301A_In);

IF (rTMR_ENC301_DevAB > rTMR_Tol_Pos_ENC301) AND (rTMR_ENC301_DevCA > rTMR_Tol_Pos_ENC301) THEN
    rTMR_ENC301_TimerA := rTMR_ENC301_TimerA + 1.0;
    IF rTMR_ENC301_TimerA >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_ENC301_HealthyA := FALSE;
    END_IF;
ELSE
    IF rTMR_ENC301_TimerA > 0.0 THEN
        rTMR_ENC301_TimerA := rTMR_ENC301_TimerA - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_ENC301_HealthyA := TRUE;
        rTMR_ENC301_TimerA := 0.0;
    END_IF;
END_IF;

IF (rTMR_ENC301_DevAB > rTMR_Tol_Pos_ENC301) AND (rTMR_ENC301_DevBC > rTMR_Tol_Pos_ENC301) THEN
    rTMR_ENC301_TimerB := rTMR_ENC301_TimerB + 1.0;
    IF rTMR_ENC301_TimerB >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_ENC301_HealthyB := FALSE;
    END_IF;
ELSE
    IF rTMR_ENC301_TimerB > 0.0 THEN
        rTMR_ENC301_TimerB := rTMR_ENC301_TimerB - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_ENC301_HealthyB := TRUE;
        rTMR_ENC301_TimerB := 0.0;
    END_IF;
END_IF;

IF (rTMR_ENC301_DevBC > rTMR_Tol_Pos_ENC301) AND (rTMR_ENC301_DevCA > rTMR_Tol_Pos_ENC301) THEN
    rTMR_ENC301_TimerC := rTMR_ENC301_TimerC + 1.0;
    IF rTMR_ENC301_TimerC >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_ENC301_HealthyC := FALSE;
    END_IF;
ELSE
    IF rTMR_ENC301_TimerC > 0.0 THEN
        rTMR_ENC301_TimerC := rTMR_ENC301_TimerC - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_ENC301_HealthyC := TRUE;
        rTMR_ENC301_TimerC := 0.0;
    END_IF;
END_IF;

IF bTMR_ENC301_HealthyA AND bTMR_ENC301_HealthyB AND bTMR_ENC301_HealthyC THEN
    iTMR_ENC301_DegradeMode := 3;
    IF ((rPlungerPos_ENC301A_In >= rPlungerPos_ENC301B_In) AND (rPlungerPos_ENC301A_In <= rPlungerPos_ENC301C_In)) OR
       ((rPlungerPos_ENC301A_In <= rPlungerPos_ENC301B_In) AND (rPlungerPos_ENC301A_In >= rPlungerPos_ENC301C_In)) THEN
        rTMR_ENC301_Voted := rPlungerPos_ENC301A_In;
    ELSIF ((rPlungerPos_ENC301B_In >= rPlungerPos_ENC301A_In) AND (rPlungerPos_ENC301B_In <= rPlungerPos_ENC301C_In)) OR
          ((rPlungerPos_ENC301B_In <= rPlungerPos_ENC301A_In) AND (rPlungerPos_ENC301B_In >= rPlungerPos_ENC301C_In)) THEN
        rTMR_ENC301_Voted := rPlungerPos_ENC301B_In;
    ELSE
        rTMR_ENC301_Voted := rPlungerPos_ENC301C_In;
    END_IF;
ELSIF bTMR_ENC301_HealthyA AND bTMR_ENC301_HealthyB THEN
    iTMR_ENC301_DegradeMode := 2;
    rTMR_ENC301_Voted := (rPlungerPos_ENC301A_In + rPlungerPos_ENC301B_In) * 0.5;
ELSIF bTMR_ENC301_HealthyB AND bTMR_ENC301_HealthyC THEN
    iTMR_ENC301_DegradeMode := 2;
    rTMR_ENC301_Voted := (rPlungerPos_ENC301B_In + rPlungerPos_ENC301C_In) * 0.5;
ELSIF bTMR_ENC301_HealthyA AND bTMR_ENC301_HealthyC THEN
    iTMR_ENC301_DegradeMode := 2;
    rTMR_ENC301_Voted := (rPlungerPos_ENC301A_In + rPlungerPos_ENC301C_In) * 0.5;
ELSIF bTMR_ENC301_HealthyA THEN
    iTMR_ENC301_DegradeMode := 1;
    rTMR_ENC301_Voted := rPlungerPos_ENC301A_In;
ELSIF bTMR_ENC301_HealthyB THEN
    iTMR_ENC301_DegradeMode := 1;
    rTMR_ENC301_Voted := rPlungerPos_ENC301B_In;
ELSIF bTMR_ENC301_HealthyC THEN
    iTMR_ENC301_DegradeMode := 1;
    rTMR_ENC301_Voted := rPlungerPos_ENC301C_In;
ELSE
    iTMR_ENC301_DegradeMode := 0;
    bAlarm_TMR_MajorDegrade := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL 4: VPT-401 CAVITY VACUUM TRANSDUCERS (TMR VOTING & FAULT DEGRADATION)
 * --------------------------------------------------------------------------------------------------------------------- *)
rTMR_VPT401_DevAB := ABS(rCavityVac_VPT401A_In - rCavityVac_VPT401B_In);
rTMR_VPT401_DevBC := ABS(rCavityVac_VPT401B_In - rCavityVac_VPT401C_In);
rTMR_VPT401_DevCA := ABS(rCavityVac_VPT401C_In - rCavityVac_VPT401A_In);

IF (rTMR_VPT401_DevAB > rTMR_Tol_Vac_VPT401) AND (rTMR_VPT401_DevCA > rTMR_Tol_Vac_VPT401) THEN
    rTMR_VPT401_TimerA := rTMR_VPT401_TimerA + 1.0;
    IF rTMR_VPT401_TimerA >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_VPT401_HealthyA := FALSE;
    END_IF;
ELSE
    IF rTMR_VPT401_TimerA > 0.0 THEN
        rTMR_VPT401_TimerA := rTMR_VPT401_TimerA - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_VPT401_HealthyA := TRUE;
        rTMR_VPT401_TimerA := 0.0;
    END_IF;
END_IF;

IF (rTMR_VPT401_DevAB > rTMR_Tol_Vac_VPT401) AND (rTMR_VPT401_DevBC > rTMR_Tol_Vac_VPT401) THEN
    rTMR_VPT401_TimerB := rTMR_VPT401_TimerB + 1.0;
    IF rTMR_VPT401_TimerB >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_VPT401_HealthyB := FALSE;
    END_IF;
ELSE
    IF rTMR_VPT401_TimerB > 0.0 THEN
        rTMR_VPT401_TimerB := rTMR_VPT401_TimerB - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_VPT401_HealthyB := TRUE;
        rTMR_VPT401_TimerB := 0.0;
    END_IF;
END_IF;

IF (rTMR_VPT401_DevBC > rTMR_Tol_Vac_VPT401) AND (rTMR_VPT401_DevCA > rTMR_Tol_Vac_VPT401) THEN
    rTMR_VPT401_TimerC := rTMR_VPT401_TimerC + 1.0;
    IF rTMR_VPT401_TimerC >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_VPT401_HealthyC := FALSE;
    END_IF;
ELSE
    IF rTMR_VPT401_TimerC > 0.0 THEN
        rTMR_VPT401_TimerC := rTMR_VPT401_TimerC - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_VPT401_HealthyC := TRUE;
        rTMR_VPT401_TimerC := 0.0;
    END_IF;
END_IF;

IF bTMR_VPT401_HealthyA AND bTMR_VPT401_HealthyB AND bTMR_VPT401_HealthyC THEN
    iTMR_VPT401_DegradeMode := 3;
    IF ((rCavityVac_VPT401A_In >= rCavityVac_VPT401B_In) AND (rCavityVac_VPT401A_In <= rCavityVac_VPT401C_In)) OR
       ((rCavityVac_VPT401A_In <= rCavityVac_VPT401B_In) AND (rCavityVac_VPT401A_In >= rCavityVac_VPT401C_In)) THEN
        rTMR_VPT401_Voted := rCavityVac_VPT401A_In;
    ELSIF ((rCavityVac_VPT401B_In >= rCavityVac_VPT401A_In) AND (rCavityVac_VPT401B_In <= rCavityVac_VPT401C_In)) OR
          ((rCavityVac_VPT401B_In <= rCavityVac_VPT401A_In) AND (rCavityVac_VPT401B_In >= rCavityVac_VPT401C_In)) THEN
        rTMR_VPT401_Voted := rCavityVac_VPT401B_In;
    ELSE
        rTMR_VPT401_Voted := rCavityVac_VPT401C_In;
    END_IF;
ELSIF bTMR_VPT401_HealthyA AND bTMR_VPT401_HealthyB THEN
    iTMR_VPT401_DegradeMode := 2;
    rTMR_VPT401_Voted := (rCavityVac_VPT401A_In + rCavityVac_VPT401B_In) * 0.5;
ELSIF bTMR_VPT401_HealthyB AND bTMR_VPT401_HealthyC THEN
    iTMR_VPT401_DegradeMode := 2;
    rTMR_VPT401_Voted := (rCavityVac_VPT401B_In + rCavityVac_VPT401C_In) * 0.5;
ELSIF bTMR_VPT401_HealthyA AND bTMR_VPT401_HealthyC THEN
    iTMR_VPT401_DegradeMode := 2;
    rTMR_VPT401_Voted := (rCavityVac_VPT401A_In + rCavityVac_VPT401C_In) * 0.5;
ELSIF bTMR_VPT401_HealthyA THEN
    iTMR_VPT401_DegradeMode := 1;
    rTMR_VPT401_Voted := rCavityVac_VPT401A_In;
ELSIF bTMR_VPT401_HealthyB THEN
    iTMR_VPT401_DegradeMode := 1;
    rTMR_VPT401_Voted := rCavityVac_VPT401B_In;
ELSIF bTMR_VPT401_HealthyC THEN
    iTMR_VPT401_DegradeMode := 1;
    rTMR_VPT401_Voted := rCavityVac_VPT401C_In;
ELSE
    iTMR_VPT401_DegradeMode := 0;
    bAlarm_TMR_MajorDegrade := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL 5: PT-501 HYDRAULIC ACCUMULATOR PRESSURE (TMR VOTING & FAULT DEGRADATION)
 * --------------------------------------------------------------------------------------------------------------------- *)
rTMR_PT501_DevAB := ABS(rAccumPres_PT501A_In - rAccumPres_PT501B_In);
rTMR_PT501_DevBC := ABS(rAccumPres_PT501B_In - rAccumPres_PT501C_In);
rTMR_PT501_DevCA := ABS(rAccumPres_PT501C_In - rAccumPres_PT501A_In);

IF (rTMR_PT501_DevAB > rTMR_Tol_Accum_PT501) AND (rTMR_PT501_DevCA > rTMR_Tol_Accum_PT501) THEN
    rTMR_PT501_TimerA := rTMR_PT501_TimerA + 1.0;
    IF rTMR_PT501_TimerA >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_PT501_HealthyA := FALSE;
    END_IF;
ELSE
    IF rTMR_PT501_TimerA > 0.0 THEN
        rTMR_PT501_TimerA := rTMR_PT501_TimerA - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_PT501_HealthyA := TRUE;
        rTMR_PT501_TimerA := 0.0;
    END_IF;
END_IF;

IF (rTMR_PT501_DevAB > rTMR_Tol_Accum_PT501) AND (rTMR_PT501_DevBC > rTMR_Tol_Accum_PT501) THEN
    rTMR_PT501_TimerB := rTMR_PT501_TimerB + 1.0;
    IF rTMR_PT501_TimerB >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_PT501_HealthyB := FALSE;
    END_IF;
ELSE
    IF rTMR_PT501_TimerB > 0.0 THEN
        rTMR_PT501_TimerB := rTMR_PT501_TimerB - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_PT501_HealthyB := TRUE;
        rTMR_PT501_TimerB := 0.0;
    END_IF;
END_IF;

IF (rTMR_PT501_DevBC > rTMR_Tol_Accum_PT501) AND (rTMR_PT501_DevCA > rTMR_Tol_Accum_PT501) THEN
    rTMR_PT501_TimerC := rTMR_PT501_TimerC + 1.0;
    IF rTMR_PT501_TimerC >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_PT501_HealthyC := FALSE;
    END_IF;
ELSE
    IF rTMR_PT501_TimerC > 0.0 THEN
        rTMR_PT501_TimerC := rTMR_PT501_TimerC - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_PT501_HealthyC := TRUE;
        rTMR_PT501_TimerC := 0.0;
    END_IF;
END_IF;

IF bTMR_PT501_HealthyA AND bTMR_PT501_HealthyB AND bTMR_PT501_HealthyC THEN
    iTMR_PT501_DegradeMode := 3;
    IF ((rAccumPres_PT501A_In >= rAccumPres_PT501B_In) AND (rAccumPres_PT501A_In <= rAccumPres_PT501C_In)) OR
       ((rAccumPres_PT501A_In <= rAccumPres_PT501B_In) AND (rAccumPres_PT501A_In >= rAccumPres_PT501C_In)) THEN
        rTMR_PT501_Voted := rAccumPres_PT501A_In;
    ELSIF ((rAccumPres_PT501B_In >= rAccumPres_PT501A_In) AND (rAccumPres_PT501B_In <= rAccumPres_PT501C_In)) OR
          ((rAccumPres_PT501B_In <= rAccumPres_PT501A_In) AND (rAccumPres_PT501B_In >= rAccumPres_PT501C_In)) THEN
        rTMR_PT501_Voted := rAccumPres_PT501B_In;
    ELSE
        rTMR_PT501_Voted := rAccumPres_PT501C_In;
    END_IF;
ELSIF bTMR_PT501_HealthyA AND bTMR_PT501_HealthyB THEN
    iTMR_PT501_DegradeMode := 2;
    rTMR_PT501_Voted := (rAccumPres_PT501A_In + rAccumPres_PT501B_In) * 0.5;
ELSIF bTMR_PT501_HealthyB AND bTMR_PT501_HealthyC THEN
    iTMR_PT501_DegradeMode := 2;
    rTMR_PT501_Voted := (rAccumPres_PT501B_In + rAccumPres_PT501C_In) * 0.5;
ELSIF bTMR_PT501_HealthyA AND bTMR_PT501_HealthyC THEN
    iTMR_PT501_DegradeMode := 2;
    rTMR_PT501_Voted := (rAccumPres_PT501A_In + rAccumPres_PT501C_In) * 0.5;
ELSIF bTMR_PT501_HealthyA THEN
    iTMR_PT501_DegradeMode := 1;
    rTMR_PT501_Voted := rAccumPres_PT501A_In;
ELSIF bTMR_PT501_HealthyB THEN
    iTMR_PT501_DegradeMode := 1;
    rTMR_PT501_Voted := rAccumPres_PT501B_In;
ELSIF bTMR_PT501_HealthyC THEN
    iTMR_PT501_DegradeMode := 1;
    rTMR_PT501_Voted := rAccumPres_PT501C_In;
ELSE
    iTMR_PT501_DegradeMode := 0;
    bAlarm_TMR_MajorDegrade := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL 6: LC-601 MAIN CLAMPING TONNAGE LOAD CELLS (TMR VOTING & FAULT DEGRADATION)
 * --------------------------------------------------------------------------------------------------------------------- *)
rTMR_LC601_DevAB := ABS(rClampForce_LC601A_In - rClampForce_LC601B_In);
rTMR_LC601_DevBC := ABS(rClampForce_LC601B_In - rClampForce_LC601C_In);
rTMR_LC601_DevCA := ABS(rClampForce_LC601C_In - rClampForce_LC601A_In);

IF (rTMR_LC601_DevAB > rTMR_Tol_Clamp_LC601) AND (rTMR_LC601_DevCA > rTMR_Tol_Clamp_LC601) THEN
    rTMR_LC601_TimerA := rTMR_LC601_TimerA + 1.0;
    IF rTMR_LC601_TimerA >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_LC601_HealthyA := FALSE;
    END_IF;
ELSE
    IF rTMR_LC601_TimerA > 0.0 THEN
        rTMR_LC601_TimerA := rTMR_LC601_TimerA - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_LC601_HealthyA := TRUE;
        rTMR_LC601_TimerA := 0.0;
    END_IF;
END_IF;

IF (rTMR_LC601_DevAB > rTMR_Tol_Clamp_LC601) AND (rTMR_LC601_DevBC > rTMR_Tol_Clamp_LC601) THEN
    rTMR_LC601_TimerB := rTMR_LC601_TimerB + 1.0;
    IF rTMR_LC601_TimerB >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_LC601_HealthyB := FALSE;
    END_IF;
ELSE
    IF rTMR_LC601_TimerB > 0.0 THEN
        rTMR_LC601_TimerB := rTMR_LC601_TimerB - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_LC601_HealthyB := TRUE;
        rTMR_LC601_TimerB := 0.0;
    END_IF;
END_IF;

IF (rTMR_LC601_DevBC > rTMR_Tol_Clamp_LC601) AND (rTMR_LC601_DevCA > rTMR_Tol_Clamp_LC601) THEN
    rTMR_LC601_TimerC := rTMR_LC601_TimerC + 1.0;
    IF rTMR_LC601_TimerC >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_LC601_HealthyC := FALSE;
    END_IF;
ELSE
    IF rTMR_LC601_TimerC > 0.0 THEN
        rTMR_LC601_TimerC := rTMR_LC601_TimerC - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_LC601_HealthyC := TRUE;
        rTMR_LC601_TimerC := 0.0;
    END_IF;
END_IF;

IF bTMR_LC601_HealthyA AND bTMR_LC601_HealthyB AND bTMR_LC601_HealthyC THEN
    iTMR_LC601_DegradeMode := 3;
    IF ((rClampForce_LC601A_In >= rClampForce_LC601B_In) AND (rClampForce_LC601A_In <= rClampForce_LC601C_In)) OR
       ((rClampForce_LC601A_In <= rClampForce_LC601B_In) AND (rClampForce_LC601A_In >= rClampForce_LC601C_In)) THEN
        rTMR_LC601_Voted := rClampForce_LC601A_In;
    ELSIF ((rClampForce_LC601B_In >= rClampForce_LC601A_In) AND (rClampForce_LC601B_In <= rClampForce_LC601C_In)) OR
          ((rClampForce_LC601B_In <= rClampForce_LC601A_In) AND (rClampForce_LC601B_In >= rClampForce_LC601C_In)) THEN
        rTMR_LC601_Voted := rClampForce_LC601B_In;
    ELSE
        rTMR_LC601_Voted := rClampForce_LC601C_In;
    END_IF;
ELSIF bTMR_LC601_HealthyA AND bTMR_LC601_HealthyB THEN
    iTMR_LC601_DegradeMode := 2;
    rTMR_LC601_Voted := (rClampForce_LC601A_In + rClampForce_LC601B_In) * 0.5;
ELSIF bTMR_LC601_HealthyB AND bTMR_LC601_HealthyC THEN
    iTMR_LC601_DegradeMode := 2;
    rTMR_LC601_Voted := (rClampForce_LC601B_In + rClampForce_LC601C_In) * 0.5;
ELSIF bTMR_LC601_HealthyA AND bTMR_LC601_HealthyC THEN
    iTMR_LC601_DegradeMode := 2;
    rTMR_LC601_Voted := (rClampForce_LC601A_In + rClampForce_LC601C_In) * 0.5;
ELSIF bTMR_LC601_HealthyA THEN
    iTMR_LC601_DegradeMode := 1;
    rTMR_LC601_Voted := rClampForce_LC601A_In;
ELSIF bTMR_LC601_HealthyB THEN
    iTMR_LC601_DegradeMode := 1;
    rTMR_LC601_Voted := rClampForce_LC601B_In;
ELSIF bTMR_LC601_HealthyC THEN
    iTMR_LC601_DegradeMode := 1;
    rTMR_LC601_Voted := rClampForce_LC601C_In;
ELSE
    iTMR_LC601_DegradeMode := 0;
    bAlarm_TMR_MajorDegrade := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL 7: TT-701 SHOT SLEEVE MELT THERMOCOUPLES (TMR VOTING & FAULT DEGRADATION)
 * --------------------------------------------------------------------------------------------------------------------- *)
rTMR_TT701_DevAB := ABS(rSleeveTemp_TT701A_In - rSleeveTemp_TT701B_In);
rTMR_TT701_DevBC := ABS(rSleeveTemp_TT701B_In - rSleeveTemp_TT701C_In);
rTMR_TT701_DevCA := ABS(rSleeveTemp_TT701C_In - rSleeveTemp_TT701A_In);

IF (rTMR_TT701_DevAB > rTMR_Tol_Temp_TT701) AND (rTMR_TT701_DevCA > rTMR_Tol_Temp_TT701) THEN
    rTMR_TT701_TimerA := rTMR_TT701_TimerA + 1.0;
    IF rTMR_TT701_TimerA >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_TT701_HealthyA := FALSE;
    END_IF;
ELSE
    IF rTMR_TT701_TimerA > 0.0 THEN
        rTMR_TT701_TimerA := rTMR_TT701_TimerA - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_TT701_HealthyA := TRUE;
        rTMR_TT701_TimerA := 0.0;
    END_IF;
END_IF;

IF (rTMR_TT701_DevAB > rTMR_Tol_Temp_TT701) AND (rTMR_TT701_DevBC > rTMR_Tol_Temp_TT701) THEN
    rTMR_TT701_TimerB := rTMR_TT701_TimerB + 1.0;
    IF rTMR_TT701_TimerB >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_TT701_HealthyB := FALSE;
    END_IF;
ELSE
    IF rTMR_TT701_TimerB > 0.0 THEN
        rTMR_TT701_TimerB := rTMR_TT701_TimerB - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_TT701_HealthyB := TRUE;
        rTMR_TT701_TimerB := 0.0;
    END_IF;
END_IF;

IF (rTMR_TT701_DevBC > rTMR_Tol_Temp_TT701) AND (rTMR_TT701_DevCA > rTMR_Tol_Temp_TT701) THEN
    rTMR_TT701_TimerC := rTMR_TT701_TimerC + 1.0;
    IF rTMR_TT701_TimerC >= rTMR_Discrepancy_Limit_ms THEN
        bTMR_TT701_HealthyC := FALSE;
    END_IF;
ELSE
    IF rTMR_TT701_TimerC > 0.0 THEN
        rTMR_TT701_TimerC := rTMR_TT701_TimerC - 0.5;
    END_IF;
    IF bCmd_Reset_Alarms_In THEN
        bTMR_TT701_HealthyC := TRUE;
        rTMR_TT701_TimerC := 0.0;
    END_IF;
END_IF;

IF bTMR_TT701_HealthyA AND bTMR_TT701_HealthyB AND bTMR_TT701_HealthyC THEN
    iTMR_TT701_DegradeMode := 3;
    IF ((rSleeveTemp_TT701A_In >= rSleeveTemp_TT701B_In) AND (rSleeveTemp_TT701A_In <= rSleeveTemp_TT701C_In)) OR
       ((rSleeveTemp_TT701A_In <= rSleeveTemp_TT701B_In) AND (rSleeveTemp_TT701A_In >= rSleeveTemp_TT701C_In)) THEN
        rTMR_TT701_Voted := rSleeveTemp_TT701A_In;
    ELSIF ((rSleeveTemp_TT701B_In >= rSleeveTemp_TT701A_In) AND (rSleeveTemp_TT701B_In <= rSleeveTemp_TT701C_In)) OR
          ((rSleeveTemp_TT701B_In <= rSleeveTemp_TT701A_In) AND (rSleeveTemp_TT701B_In >= rSleeveTemp_TT701C_In)) THEN
        rTMR_TT701_Voted := rSleeveTemp_TT701B_In;
    ELSE
        rTMR_TT701_Voted := rSleeveTemp_TT701C_In;
    END_IF;
ELSIF bTMR_TT701_HealthyA AND bTMR_TT701_HealthyB THEN
    iTMR_TT701_DegradeMode := 2;
    rTMR_TT701_Voted := (rSleeveTemp_TT701A_In + rSleeveTemp_TT701B_In) * 0.5;
ELSIF bTMR_TT701_HealthyB AND bTMR_TT701_HealthyC THEN
    iTMR_TT701_DegradeMode := 2;
    rTMR_TT701_Voted := (rSleeveTemp_TT701B_In + rSleeveTemp_TT701C_In) * 0.5;
ELSIF bTMR_TT701_HealthyA AND bTMR_TT701_HealthyC THEN
    iTMR_TT701_DegradeMode := 2;
    rTMR_TT701_Voted := (rSleeveTemp_TT701A_In + rSleeveTemp_TT701C_In) * 0.5;
ELSIF bTMR_TT701_HealthyA THEN
    iTMR_TT701_DegradeMode := 1;
    rTMR_TT701_Voted := rSleeveTemp_TT701A_In;
ELSIF bTMR_TT701_HealthyB THEN
    iTMR_TT701_DegradeMode := 1;
    rTMR_TT701_Voted := rSleeveTemp_TT701B_In;
ELSIF bTMR_TT701_HealthyC THEN
    iTMR_TT701_DegradeMode := 1;
    rTMR_TT701_Voted := rSleeveTemp_TT701C_In;
ELSE
    iTMR_TT701_DegradeMode := 0;
    bAlarm_TMR_MajorDegrade := TRUE;
END_IF;
"""
