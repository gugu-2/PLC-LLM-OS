# subsea_boosting_builder/st_phase5_alarms.py

def get_phase5_alarms():
    return """(* ==================================================================================================== *)
(* PHASE 5: ISA-18.2 MULTI-TIERED ALARM ENGINE & 32-BIT BIT-PACKED STATUS WORDS                          *)
(* Alarm Trip Evaluation, Deadband Hysteresis, On-Delay Debouncing, First-Out Incident Latch,            *)
(* and Comprehensive DWORD Telemetry Packaging.                                                         *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* 5.1: Process Alarm Trip Evaluation & Debounce Timers                                                 *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Suction Pressure Low-Low (LL) Trip *)
IF rVotedSuctionPress_bar <= rSuctionPress_LL_Trip_bar THEN
    tTimer_SuctionPress_LL_s := tTimer_SuctionPress_LL_s + rCycleTime_s;
    IF tTimer_SuctionPress_LL_s >= 0.200 THEN
        bAlarm_SuctionPress_LL := TRUE;
        IF NOT bFirstOutLatched THEN
            nFirstOutAlarmIndex := 1;
            bFirstOutLatched := TRUE;
        END_IF;
    END_IF;
ELSIF rVotedSuctionPress_bar > (rSuctionPress_LL_Trip_bar + rSuctionPress_Hysteresis_bar) THEN
    tTimer_SuctionPress_LL_s := 0.0;
    bAlarm_SuctionPress_LL := FALSE;
END_IF;

(* Suction Pressure Low (L) Warning *)
IF rVotedSuctionPress_bar <= rSuctionPress_L_Warn_bar THEN
    tTimer_SuctionPress_L_s := tTimer_SuctionPress_L_s + rCycleTime_s;
    IF tTimer_SuctionPress_L_s >= 0.350 THEN
        bAlarm_SuctionPress_L := TRUE;
    END_IF;
ELSIF rVotedSuctionPress_bar > (rSuctionPress_L_Warn_bar + rSuctionPress_Hysteresis_bar) THEN
    tTimer_SuctionPress_L_s := 0.0;
    bAlarm_SuctionPress_L := FALSE;
END_IF;

(* Suction Pressure High (H) Warning *)
IF rVotedSuctionPress_bar >= rSuctionPress_H_Warn_bar THEN
    tTimer_SuctionPress_H_s := tTimer_SuctionPress_H_s + rCycleTime_s;
    IF tTimer_SuctionPress_H_s >= 0.350 THEN
        bAlarm_SuctionPress_H := TRUE;
    END_IF;
ELSIF rVotedSuctionPress_bar < (rSuctionPress_H_Warn_bar - rSuctionPress_Hysteresis_bar) THEN
    tTimer_SuctionPress_H_s := 0.0;
    bAlarm_SuctionPress_H := FALSE;
END_IF;

(* Suction Pressure High-High (HH) Trip *)
IF rVotedSuctionPress_bar >= rSuctionPress_HH_Trip_bar THEN
    tTimer_SuctionPress_HH_s := tTimer_SuctionPress_HH_s + rCycleTime_s;
    IF tTimer_SuctionPress_HH_s >= 0.200 THEN
        bAlarm_SuctionPress_HH := TRUE;
        IF NOT bFirstOutLatched THEN
            nFirstOutAlarmIndex := 2;
            bFirstOutLatched := TRUE;
        END_IF;
    END_IF;
ELSIF rVotedSuctionPress_bar < (rSuctionPress_HH_Trip_bar - rSuctionPress_Hysteresis_bar) THEN
    tTimer_SuctionPress_HH_s := 0.0;
    bAlarm_SuctionPress_HH := FALSE;
END_IF;

(* Discharge Pressure Low-Low (LL) Trip *)
IF rVotedDischargePress_bar <= rDischargePress_LL_Trip_bar THEN
    tTimer_DischargePress_LL_s := tTimer_DischargePress_LL_s + rCycleTime_s;
    IF tTimer_DischargePress_LL_s >= 0.250 THEN
        bAlarm_DischargePress_LL := TRUE;
        IF NOT bFirstOutLatched THEN
            nFirstOutAlarmIndex := 3;
            bFirstOutLatched := TRUE;
        END_IF;
    END_IF;
ELSIF rVotedDischargePress_bar > (rDischargePress_LL_Trip_bar + rDischargePress_Hysteresis_bar) THEN
    tTimer_DischargePress_LL_s := 0.0;
    bAlarm_DischargePress_LL := FALSE;
END_IF;

(* Discharge Pressure Low (L) Warning *)
IF rVotedDischargePress_bar <= rDischargePress_L_Warn_bar THEN
    tTimer_DischargePress_L_s := tTimer_DischargePress_L_s + rCycleTime_s;
    IF tTimer_DischargePress_L_s >= 0.400 THEN
        bAlarm_DischargePress_L := TRUE;
    END_IF;
ELSIF rVotedDischargePress_bar > (rDischargePress_L_Warn_bar + rDischargePress_Hysteresis_bar) THEN
    tTimer_DischargePress_L_s := 0.0;
    bAlarm_DischargePress_L := FALSE;
END_IF;

(* Discharge Pressure High (H) Warning *)
IF rVotedDischargePress_bar >= rDischargePress_H_Warn_bar THEN
    tTimer_DischargePress_H_s := tTimer_DischargePress_H_s + rCycleTime_s;
    IF tTimer_DischargePress_H_s >= 0.400 THEN
        bAlarm_DischargePress_H := TRUE;
    END_IF;
ELSIF rVotedDischargePress_bar < (rDischargePress_H_Warn_bar - rDischargePress_Hysteresis_bar) THEN
    tTimer_DischargePress_H_s := 0.0;
    bAlarm_DischargePress_H := FALSE;
END_IF;

(* Discharge Pressure High-High (HH) Trip *)
IF rVotedDischargePress_bar >= rDischargePress_HH_Trip_bar THEN
    tTimer_DischargePress_HH_s := tTimer_DischargePress_HH_s + rCycleTime_s;
    IF tTimer_DischargePress_HH_s >= 0.150 THEN
        bAlarm_DischargePress_HH := TRUE;
        IF NOT bFirstOutLatched THEN
            nFirstOutAlarmIndex := 4;
            bFirstOutLatched := TRUE;
        END_IF;
    END_IF;
ELSIF rVotedDischargePress_bar < (rDischargePress_HH_Trip_bar - rDischargePress_Hysteresis_bar) THEN
    tTimer_DischargePress_HH_s := 0.0;
    bAlarm_DischargePress_HH := FALSE;
END_IF;

(* Twin-Screw Differential Pressure High (H) Warning *)
IF rTwinScrewDifferentialPress_bar >= rDiffPress_H_Warn_bar THEN
    tTimer_DiffPress_H_s := tTimer_DiffPress_H_s + rCycleTime_s;
    IF tTimer_DiffPress_H_s >= 0.350 THEN
        bAlarm_DiffPress_H := TRUE;
    END_IF;
ELSIF rTwinScrewDifferentialPress_bar < (rDiffPress_H_Warn_bar - 1.5) THEN
    tTimer_DiffPress_H_s := 0.0;
    bAlarm_DiffPress_H := FALSE;
END_IF;

(* Twin-Screw Differential Pressure High-High (HH) Trip *)
IF rTwinScrewDifferentialPress_bar >= rDiffPress_HH_Trip_bar THEN
    tTimer_DiffPress_HH_s := tTimer_DiffPress_HH_s + rCycleTime_s;
    IF tTimer_DiffPress_HH_s >= 0.200 THEN
        bAlarm_DiffPress_HH := TRUE;
        IF NOT bFirstOutLatched THEN
            nFirstOutAlarmIndex := 5;
            bFirstOutLatched := TRUE;
        END_IF;
    END_IF;
ELSIF rTwinScrewDifferentialPress_bar < (rDiffPress_HH_Trip_bar - 1.5) THEN
    tTimer_DiffPress_HH_s := 0.0;
    bAlarm_DiffPress_HH := FALSE;
END_IF;

(* Gas Volume Fraction (GVF) High (H) Warning *)
IF rVotedGVF_pct >= rGVF_H_Warn_pct THEN
    tTimer_GVF_H_s := tTimer_GVF_H_s + rCycleTime_s;
    IF tTimer_GVF_H_s >= 0.400 THEN
        bAlarm_GVF_H := TRUE;
    END_IF;
ELSIF rVotedGVF_pct < (rGVF_H_Warn_pct - 1.5) THEN
    tTimer_GVF_H_s := 0.0;
    bAlarm_GVF_H := FALSE;
END_IF;

(* Gas Volume Fraction (GVF) High-High (HH) Trip *)
IF rVotedGVF_pct >= rGVF_HH_Trip_pct THEN
    tTimer_GVF_HH_s := tTimer_GVF_HH_s + rCycleTime_s;
    IF tTimer_GVF_HH_s >= 0.300 THEN
        bAlarm_GVF_HH := TRUE;
        IF NOT bFirstOutLatched THEN
            nFirstOutAlarmIndex := 6;
            bFirstOutLatched := TRUE;
        END_IF;
    END_IF;
ELSIF rVotedGVF_pct < (rGVF_HH_Trip_pct - 1.5) THEN
    tTimer_GVF_HH_s := 0.0;
    bAlarm_GVF_HH := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 5.2: Mechanical, Seal & Thermodynamic Alarm Evaluations                                              *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Barrier Fluid Seal DP Low-Low (LL) Trip *)
IF rVotedSealDP_bar <= rSealDP_LL_Trip_bar THEN
    tTimer_SealDP_LL_s := tTimer_SealDP_LL_s + rCycleTime_s;
    IF tTimer_SealDP_LL_s >= 0.150 THEN
        bAlarm_SealDP_LL := TRUE;
        IF NOT bFirstOutLatched THEN
            nFirstOutAlarmIndex := 7;
            bFirstOutLatched := TRUE;
        END_IF;
    END_IF;
ELSIF rVotedSealDP_bar > (rSealDP_LL_Trip_bar + 1.0) THEN
    tTimer_SealDP_LL_s := 0.0;
    bAlarm_SealDP_LL := FALSE;
END_IF;

(* Barrier Fluid Seal DP Low (L) Warning *)
IF rVotedSealDP_bar <= rSealDP_L_Warn_bar THEN
    tTimer_SealDP_L_s := tTimer_SealDP_L_s + rCycleTime_s;
    IF tTimer_SealDP_L_s >= 0.300 THEN
        bAlarm_SealDP_L := TRUE;
    END_IF;
ELSIF rVotedSealDP_bar > (rSealDP_L_Warn_bar + 1.0) THEN
    tTimer_SealDP_L_s := 0.0;
    bAlarm_SealDP_L := FALSE;
END_IF;

(* Barrier Fluid Seal DP High (H) Warning *)
IF rVotedSealDP_bar >= rSealDP_H_Warn_bar THEN
    tTimer_SealDP_H_s := tTimer_SealDP_H_s + rCycleTime_s;
    IF tTimer_SealDP_H_s >= 0.350 THEN
        bAlarm_SealDP_H := TRUE;
    END_IF;
ELSIF rVotedSealDP_bar < (rSealDP_H_Warn_bar - 1.0) THEN
    tTimer_SealDP_H_s := 0.0;
    bAlarm_SealDP_H := FALSE;
END_IF;

(* Barrier Fluid Seal DP High-High (HH) Trip *)
IF rVotedSealDP_bar >= rSealDP_HH_Trip_bar THEN
    tTimer_SealDP_HH_s := tTimer_SealDP_HH_s + rCycleTime_s;
    IF tTimer_SealDP_HH_s >= 0.200 THEN
        bAlarm_SealDP_HH := TRUE;
        IF NOT bFirstOutLatched THEN
            nFirstOutAlarmIndex := 8;
            bFirstOutLatched := TRUE;
        END_IF;
    END_IF;
ELSIF rVotedSealDP_bar < (rSealDP_HH_Trip_bar - 1.0) THEN
    tTimer_SealDP_HH_s := 0.0;
    bAlarm_SealDP_HH := FALSE;
END_IF;

(* Barrier Fluid Leak Rate High (H) Warning *)
IF rBarrierFluidLeakRate_mLmin >= rBarrierLeak_H_Warn_mLmin THEN
    tTimer_BarrierLeak_H_s := tTimer_BarrierLeak_H_s + rCycleTime_s;
    IF tTimer_BarrierLeak_H_s >= 1.0 THEN
        bAlarm_BarrierLeak_H := TRUE;
    END_IF;
ELSIF rBarrierFluidLeakRate_mLmin < (rBarrierLeak_H_Warn_mLmin - 0.5) THEN
    tTimer_BarrierLeak_H_s := 0.0;
    bAlarm_BarrierLeak_H := FALSE;
END_IF;

(* Barrier Fluid Leak Rate High-High (HH) Trip *)
IF rBarrierFluidLeakRate_mLmin >= rBarrierLeak_HH_Trip_mLmin THEN
    tTimer_BarrierLeak_HH_s := tTimer_BarrierLeak_HH_s + rCycleTime_s;
    IF tTimer_BarrierLeak_HH_s >= 0.500 THEN
        bAlarm_BarrierLeak_HH := TRUE;
        IF NOT bFirstOutLatched THEN
            nFirstOutAlarmIndex := 9;
            bFirstOutLatched := TRUE;
        END_IF;
    END_IF;
ELSIF rBarrierFluidLeakRate_mLmin < (rBarrierLeak_HH_Trip_mLmin - 1.0) THEN
    tTimer_BarrierLeak_HH_s := 0.0;
    bAlarm_BarrierLeak_HH := FALSE;
END_IF;

(* Differential Thermal Expansion High (H) Warning *)
IF rDifferentialGrowth_um >= rThermalGrowth_H_Warn_um THEN
    tTimer_ThermalGrowth_H_s := tTimer_ThermalGrowth_H_s + rCycleTime_s;
    IF tTimer_ThermalGrowth_H_s >= 0.500 THEN
        bAlarm_ThermalGrowth_H := TRUE;
    END_IF;
ELSIF rDifferentialGrowth_um < (rThermalGrowth_H_Warn_um - 3.0) THEN
    tTimer_ThermalGrowth_H_s := 0.0;
    bAlarm_ThermalGrowth_H := FALSE;
END_IF;

(* Differential Thermal Expansion High-High (HH) Trip *)
IF rDifferentialGrowth_um >= rThermalGrowth_HH_Trip_um THEN
    tTimer_ThermalGrowth_HH_s := tTimer_ThermalGrowth_HH_s + rCycleTime_s;
    IF tTimer_ThermalGrowth_HH_s >= 0.250 THEN
        bAlarm_ThermalGrowth_HH := TRUE;
        IF NOT bFirstOutLatched THEN
            nFirstOutAlarmIndex := 10;
            bFirstOutLatched := TRUE;
        END_IF;
    END_IF;
ELSIF rDifferentialGrowth_um < (rThermalGrowth_HH_Trip_um - 3.0) THEN
    tTimer_ThermalGrowth_HH_s := 0.0;
    bAlarm_ThermalGrowth_HH := FALSE;
END_IF;

(* Cartridge Radial Vibration RMS High (H) Warning *)
IF (rPumpRadialVibration_DE_RMS_mps2 >= rVibration_H_Warn_mps2) OR
   (rPumpRadialVibration_NDE_RMS_mps2 >= rVibration_H_Warn_mps2) THEN
    tTimer_Vibration_H_s := tTimer_Vibration_H_s + rCycleTime_s;
    IF tTimer_Vibration_H_s >= 0.350 THEN
        bAlarm_Vibration_H := TRUE;
    END_IF;
ELSIF (rPumpRadialVibration_DE_RMS_mps2 < (rVibration_H_Warn_mps2 - 0.4)) AND
      (rPumpRadialVibration_NDE_RMS_mps2 < (rVibration_H_Warn_mps2 - 0.4)) THEN
    tTimer_Vibration_H_s := 0.0;
    bAlarm_Vibration_H := FALSE;
END_IF;

(* Cartridge Radial Vibration RMS High-High (HH) Trip *)
IF (rPumpRadialVibration_DE_RMS_mps2 >= rVibration_HH_Trip_mps2) OR
   (rPumpRadialVibration_NDE_RMS_mps2 >= rVibration_HH_Trip_mps2) THEN
    tTimer_Vibration_HH_s := tTimer_Vibration_HH_s + rCycleTime_s;
    IF tTimer_Vibration_HH_s >= 0.150 THEN
        bAlarm_Vibration_HH := TRUE;
        IF NOT bFirstOutLatched THEN
            nFirstOutAlarmIndex := 11;
            bFirstOutLatched := TRUE;
        END_IF;
    END_IF;
ELSIF (rPumpRadialVibration_DE_RMS_mps2 < (rVibration_HH_Trip_mps2 - 0.5)) AND
      (rPumpRadialVibration_NDE_RMS_mps2 < (rVibration_HH_Trip_mps2 - 0.5)) THEN
    tTimer_Vibration_HH_s := 0.0;
    bAlarm_Vibration_HH := FALSE;
END_IF;

(* Subsea Motor Stator Winding High (H) Warning *)
IF rMotorStatorWindingTemp_degC >= rMotorStatorTemp_H_Warn_degC THEN
    tTimer_MotorStatorTemp_H_s := tTimer_MotorStatorTemp_H_s + rCycleTime_s;
    IF tTimer_MotorStatorTemp_H_s >= 1.0 THEN
        bAlarm_MotorStatorTemp_H := TRUE;
    END_IF;
ELSIF rMotorStatorWindingTemp_degC < (rMotorStatorTemp_H_Warn_degC - 3.0) THEN
    tTimer_MotorStatorTemp_H_s := 0.0;
    bAlarm_MotorStatorTemp_H := FALSE;
END_IF;

(* Subsea Motor Stator Winding High-High (HH) Trip *)
IF rMotorStatorWindingTemp_degC >= rMotorStatorTemp_HH_Trip_degC THEN
    tTimer_MotorStatorTemp_HH_s := tTimer_MotorStatorTemp_HH_s + rCycleTime_s;
    IF tTimer_MotorStatorTemp_HH_s >= 0.500 THEN
        bAlarm_MotorStatorTemp_HH := TRUE;
        IF NOT bFirstOutLatched THEN
            nFirstOutAlarmIndex := 12;
            bFirstOutLatched := TRUE;
        END_IF;
    END_IF;
ELSIF rMotorStatorWindingTemp_degC < (rMotorStatorTemp_HH_Trip_degC - 3.0) THEN
    tTimer_MotorStatorTemp_HH_s := 0.0;
    bAlarm_MotorStatorTemp_HH := FALSE;
END_IF;

(* Hydrate Subcooling Margin Low (L) Warning *)
IF rHydrateSubcoolingMargin_degC <= rHydrateMargin_L_Warn_degC THEN
    tTimer_HydrateMargin_L_s := tTimer_HydrateMargin_L_s + rCycleTime_s;
    IF tTimer_HydrateMargin_L_s >= 0.500 THEN
        bAlarm_HydrateMargin_L := TRUE;
    END_IF;
ELSIF rHydrateSubcoolingMargin_degC > (rHydrateMargin_L_Warn_degC + 1.0) THEN
    tTimer_HydrateMargin_L_s := 0.0;
    bAlarm_HydrateMargin_L := FALSE;
END_IF;

(* Hydrate Subcooling Margin Low-Low (LL) Trip *)
IF rHydrateSubcoolingMargin_degC <= rHydrateMargin_LL_Trip_degC THEN
    tTimer_HydrateMargin_LL_s := tTimer_HydrateMargin_LL_s + rCycleTime_s;
    IF tTimer_HydrateMargin_LL_s >= 0.300 THEN
        bAlarm_HydrateMargin_LL := TRUE;
        IF NOT bFirstOutLatched THEN
            nFirstOutAlarmIndex := 13;
            bFirstOutLatched := TRUE;
        END_IF;
    END_IF;
ELSIF rHydrateSubcoolingMargin_degC > (rHydrateMargin_LL_Trip_degC + 1.0) THEN
    tTimer_HydrateMargin_LL_s := 0.0;
    bAlarm_HydrateMargin_LL := FALSE;
END_IF;

(* Master Reset of First-Out Incident Latch *)
IF bReset THEN
    bFirstOutLatched := FALSE;
    nFirstOutAlarmIndex := 0;
END_IF;

(* Summary Status Booleans *)
bStationWarning := bAlarm_SuctionPress_L OR bAlarm_SuctionPress_H OR
                   bAlarm_DischargePress_L OR bAlarm_DischargePress_H OR
                   bAlarm_DiffPress_H OR bAlarm_GVF_H OR
                   bAlarm_SealDP_L OR bAlarm_SealDP_H OR
                   bAlarm_BarrierLeak_H OR bAlarm_ThermalGrowth_H OR
                   bAlarm_Vibration_H OR bAlarm_MotorStatorTemp_H OR
                   bAlarm_HydrateMargin_L OR bClearanceWarning OR
                   (nSuction_VotingMode < 3) OR (nDischarge_VotingMode < 3) OR
                   (nGVF_VotingMode < 3) OR (nSealDP_VotingMode < 3);

(* ---------------------------------------------------------------------------------------------------- *)
(* 5.3: 32-Bit Bit-Packed DWORD Telemetry Construction                                                  *)
(* ---------------------------------------------------------------------------------------------------- *)
(* dwAlarmWord1: Multiphase Process Alarms *)
dwAlarmWord1 := 16#00000000;
IF bAlarm_SuctionPress_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF;
IF bAlarm_SuctionPress_L  THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF;
IF bAlarm_SuctionPress_H  THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF;
IF bAlarm_SuctionPress_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF;
IF bAlarm_DischargePress_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF;
IF bAlarm_DischargePress_L  THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF;
IF bAlarm_DischargePress_H  THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF;
IF bAlarm_DischargePress_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF;
IF bAlarm_DiffPress_H THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; END_IF;
IF bAlarm_DiffPress_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; END_IF;
IF bAlarm_GVF_H THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000400; END_IF;
IF bAlarm_GVF_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000800; END_IF;
IF bGasSlugDetected THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00001000; END_IF;
IF bLiquidSlugDetected THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00002000; END_IF;
IF bAlarm_HydrateMargin_L THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00004000; END_IF;
IF bAlarm_HydrateMargin_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00008000; END_IF;
IF rSurgeProximityMargin_pct < 20.0 THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00010000; END_IF;
IF rMixtureAcousticSonicSpeed_mps < 60.0 THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00020000; END_IF;

(* dwAlarmWord2: Mechanical, Seal & Dynamic Clearance Alarms *)
dwAlarmWord2 := 16#00000000;
IF bAlarm_SealDP_LL THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF;
IF bAlarm_SealDP_L  THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF;
IF bAlarm_SealDP_H  THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF;
IF bAlarm_SealDP_HH THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF;
IF bAlarm_BarrierLeak_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF;
IF bAlarm_BarrierLeak_HH THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF;
IF bBarrierAccumulatorLowVolume THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF;
IF bAlarm_ThermalGrowth_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; END_IF;
IF bAlarm_ThermalGrowth_HH THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; END_IF;
IF bClearanceWarning THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; END_IF;
IF bClearanceCriticalTrip THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000400; END_IF;
IF bAlarm_Vibration_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000800; END_IF;
IF bAlarm_Vibration_HH THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00001000; END_IF;
IF bAlarm_MotorStatorTemp_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00002000; END_IF;
IF bAlarm_MotorStatorTemp_HH THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00004000; END_IF;
IF rPumpThrustBearingDisplacement_um > 50.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00008000; END_IF;

(* dwStatusWord1: Operating Modes & Permissives *)
dwStatusWord1 := 16#00000000;
dwStatusWord1 := dwStatusWord1 OR INT_TO_DWORD(nFSM_CurrentState AND 16#000F);
IF bStationReady THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF;
IF bStationRunning THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF;
IF bStationTripped THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF;
IF bStationWarning THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF;
IF bAutoMode THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF;
IF bProductionPermissive THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF;
IF rMotorVFD_SpeedFeedback_RPM > 100.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF;
IF rKickbackValvePosition_Feedback_pct < 5.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF;
IF rChokeTrimPosition_Feedback_pct > 10.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF;
IF rMEG_ValvePosition_Feedback_pct > 10.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF;
IF rMistCoolingRecycleDemand_pct > 5.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF;
IF NOT bBarrierAccumulatorLowVolume THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF;
IF bFirstOutLatched THEN dwStatusWord1 := dwStatusWord1 OR 16#00010000; END_IF;

(* dwStatusWord2: 2oo3 TMR Health & Subsea Diagnostics *)
dwStatusWord2 := 16#00000000;
IF bSuction_ChA_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000001; END_IF;
IF bSuction_ChB_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000002; END_IF;
IF bSuction_ChC_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000004; END_IF;
IF nSuction_VotingMode = 0 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000008; END_IF;
IF bDischarge_ChA_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000010; END_IF;
IF bDischarge_ChB_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000020; END_IF;
IF bDischarge_ChC_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000040; END_IF;
IF nDischarge_VotingMode = 0 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000080; END_IF;
IF bGVF_ChA_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF;
IF bGVF_ChB_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000200; END_IF;
IF bGVF_ChC_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000400; END_IF;
IF nGVF_VotingMode = 0 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000800; END_IF;
IF bSealDP_ChA_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00001000; END_IF;
IF bSealDP_ChB_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00002000; END_IF;
IF bSealDP_ChC_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00004000; END_IF;
IF nSealDP_VotingMode = 0 THEN dwStatusWord2 := dwStatusWord2 OR 16#00008000; END_IF;
dwStatusWord2 := dwStatusWord2 OR 16#00010000; (* Subsea Umbilical Link Telemetry OK *)
dwStatusWord2 := dwStatusWord2 OR 16#00020000; (* Topside Modbus TCP/IP Master Heartbeat OK *)

END_FUNCTION_BLOCK
"""
