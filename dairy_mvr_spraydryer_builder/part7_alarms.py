# dairy_mvr_spraydryer_builder/part7_alarms.py
# Lumina Cyber-Physical Systems Chair - V7 Max-Persona
# Part 7: Phase 5 ISA-18.2 Multi-Tier Alarms, First-Out Latched Trips & 32-Bit Telemetry

def get_part7_alarms():
    return """(* === PHASE 5: ISA-18.2 MULTI-TIER ALARMS & 32-BIT BIT-PACKED STATUS WORDS === *)

(* ------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.1: FAST NFPA 68/69 DEFLAGRATION DETECTION & HRD CHEMICAL BARRIER ACTUATION (<10 ms)   *)
(* ------------------------------------------------------------------------------------------------- *)
IF rPT_901_ChamberPressure_Pa >= rHH_ChamberPressure_Pa THEN
    bAlarm_ChamberPressure_HH      := TRUE;
    bHRD_ExplosionCannonsFire      := TRUE;
    bExplosionIsolationValvesClose := TRUE;
    bFireDelugeActive              := TRUE;
    eState                         := 13;
ELSIF (rPT_901_ChamberPressure_Pa < (rHH_ChamberPressure_Pa - 50.0)) AND (NOT bHRD_ExplosionCannonsFire) THEN
    bAlarm_ChamberPressure_HH      := FALSE;
END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.2: CALANDRIA 1ST EFFECT SUMP LEVEL 4-TIER ALARMS WITH DEADBAND HYSTERESIS             *)
(* ------------------------------------------------------------------------------------------------- *)
(* Low-Low Critical Dryout Trip (LL: 350.0 mm) *)
IF rVoted_CalandriaLevel_mm <= rLL_CalandriaLevel_mm THEN
    bAlarm_CalandriaLevel_LL := TRUE;
ELSIF rVoted_CalandriaLevel_mm >= (rLL_CalandriaLevel_mm + rDB_CalandriaLevel_mm) THEN
    bAlarm_CalandriaLevel_LL := FALSE;
END_IF;

(* Low Advisory Pre-Alarm (L: 600.0 mm) *)
IF rVoted_CalandriaLevel_mm <= rL_CalandriaLevel_mm THEN
    bAlarm_CalandriaLevel_L := TRUE;
ELSIF rVoted_CalandriaLevel_mm >= (rL_CalandriaLevel_mm + rDB_CalandriaLevel_mm) THEN
    bAlarm_CalandriaLevel_L := FALSE;
END_IF;

(* High Advisory Pre-Alarm (H: 2200.0 mm) *)
IF rVoted_CalandriaLevel_mm >= rH_CalandriaLevel_mm THEN
    bAlarm_CalandriaLevel_H := TRUE;
ELSIF rVoted_CalandriaLevel_mm <= (rH_CalandriaLevel_mm - rDB_CalandriaLevel_mm) THEN
    bAlarm_CalandriaLevel_H := FALSE;
END_IF;

(* High-High Vapor Duct Carryover Trip (HH: 2650.0 mm) *)
IF rVoted_CalandriaLevel_mm >= rHH_CalandriaLevel_mm THEN
    bAlarm_CalandriaLevel_HH := TRUE;
ELSIF rVoted_CalandriaLevel_mm <= (rHH_CalandriaLevel_mm - rDB_CalandriaLevel_mm) THEN
    bAlarm_CalandriaLevel_HH := FALSE;
END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.3: IN-LINE CONCENTRATE BRIX SOLIDS 4-TIER ALARMS WITH DEADBAND HYSTERESIS             *)
(* ------------------------------------------------------------------------------------------------- *)
(* Low-Low Water Dilution Severe Trip (LL: 12.0 % TS) *)
IF rVoted_SolidsBrix_pct <= rLL_SolidsBrix_pct THEN
    bAlarm_SolidsBrix_LL := TRUE;
ELSIF rVoted_SolidsBrix_pct >= (rLL_SolidsBrix_pct + rDB_SolidsBrix_pct) THEN
    bAlarm_SolidsBrix_LL := FALSE;
END_IF;

(* Low Divert Advisory Alert (L: 44.0 % TS) *)
IF rVoted_SolidsBrix_pct <= rL_SolidsBrix_pct THEN
    bAlarm_SolidsBrix_L := TRUE;
ELSIF rVoted_SolidsBrix_pct >= (rL_SolidsBrix_pct + rDB_SolidsBrix_pct) THEN
    bAlarm_SolidsBrix_L := FALSE;
END_IF;

(* High Viscosity Warning Alert (H: 52.5 % TS) *)
IF rVoted_SolidsBrix_pct >= rH_SolidsBrix_pct THEN
    bAlarm_SolidsBrix_H := TRUE;
ELSIF rVoted_SolidsBrix_pct <= (rH_SolidsBrix_pct - rDB_SolidsBrix_pct) THEN
    bAlarm_SolidsBrix_H := FALSE;
END_IF;

(* High-High Tube Plugging Risk Trip (HH: 55.0 % TS) *)
IF rVoted_SolidsBrix_pct >= rHH_SolidsBrix_pct THEN
    bAlarm_SolidsBrix_HH := TRUE;
ELSIF rVoted_SolidsBrix_pct <= (rHH_SolidsBrix_pct - rDB_SolidsBrix_pct) THEN
    bAlarm_SolidsBrix_HH := FALSE;
END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.4: MVR TURBO COMPRESSOR DIFFERENTIAL PRESSURE 4-TIER ALARMS                           *)
(* ------------------------------------------------------------------------------------------------- *)
(* Low-Low Stall / Loss of Vapor Trip (LL: 8.0 kPa) *)
IF rVoted_MvrDiffPress_kPa <= rLL_MvrDiffPress_kPa THEN
    bAlarm_MvrDiffPress_LL := TRUE;
ELSIF rVoted_MvrDiffPress_kPa >= (rLL_MvrDiffPress_kPa + rDB_MvrDiffPress_kPa) THEN
    bAlarm_MvrDiffPress_LL := FALSE;
END_IF;

(* Low Differential Pressure Warning (L: 18.0 kPa) *)
IF rVoted_MvrDiffPress_kPa <= rL_MvrDiffPress_kPa THEN
    bAlarm_MvrDiffPress_L := TRUE;
ELSIF rVoted_MvrDiffPress_kPa >= (rL_MvrDiffPress_kPa + rDB_MvrDiffPress_kPa) THEN
    bAlarm_MvrDiffPress_L := FALSE;
END_IF;

(* High Differential Pressure Warning (H: 55.0 kPa) *)
IF rVoted_MvrDiffPress_kPa >= rH_MvrDiffPress_kPa THEN
    bAlarm_MvrDiffPress_H := TRUE;
ELSIF rVoted_MvrDiffPress_kPa <= (rH_MvrDiffPress_kPa - rDB_MvrDiffPress_kPa) THEN
    bAlarm_MvrDiffPress_H := FALSE;
END_IF;

(* High-High Overpressure Impeller Trip (HH: 68.0 kPa) *)
IF rVoted_MvrDiffPress_kPa >= rHH_MvrDiffPress_kPa THEN
    bAlarm_MvrDiffPress_HH := TRUE;
ELSIF rVoted_MvrDiffPress_kPa <= (rHH_MvrDiffPress_kPa - rDB_MvrDiffPress_kPa) THEN
    bAlarm_MvrDiffPress_HH := FALSE;
END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.5: SPRAY DRYER EXHAUST AIR TEMPERATURE 3-TIER ALARMS                                  *)
(* ------------------------------------------------------------------------------------------------- *)
(* Low Condensation Advisory Warning (L: 78.0 deg C) *)
IF rVoted_ExhaustTemp_degC <= rL_ExhaustTemp_degC THEN
    bAlarm_ExhaustTemp_L := TRUE;
ELSIF rVoted_ExhaustTemp_degC >= (rL_ExhaustTemp_degC + rDB_ExhaustTemp_degC) THEN
    bAlarm_ExhaustTemp_L := FALSE;
END_IF;

(* High Powder Scorching Warning (H: 96.0 deg C) *)
IF rVoted_ExhaustTemp_degC >= rH_ExhaustTemp_degC THEN
    bAlarm_ExhaustTemp_H := TRUE;
ELSIF rVoted_ExhaustTemp_degC <= (rH_ExhaustTemp_degC - rDB_ExhaustTemp_degC) THEN
    bAlarm_ExhaustTemp_H := FALSE;
END_IF;

(* High-High Flash Fire Ignition Trip (HH: 105.0 deg C) *)
IF rVoted_ExhaustTemp_degC >= rHH_ExhaustTemp_degC THEN
    bAlarm_ExhaustTemp_HH := TRUE;
ELSIF rVoted_ExhaustTemp_degC <= (rHH_ExhaustTemp_degC - rDB_ExhaustTemp_degC) THEN
    bAlarm_ExhaustTemp_HH := FALSE;
END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.6: CYCLONE & BAGHOUSE INFRARED SPARK DETECTORS 2-TIER ALARMS                         *)
(* ------------------------------------------------------------------------------------------------- *)
(* High Spark Low Infrared Advisory (H: 12.0 counts/s) *)
IF rVoted_SparkDetector_cps >= rH_SparkDetector_cps THEN
    bAlarm_Spark_H := TRUE;
ELSIF rVoted_SparkDetector_cps <= (rH_SparkDetector_cps - rDB_SparkDetector_cps) THEN
    bAlarm_Spark_H := FALSE;
END_IF;

(* High-High Confirmed Fire Trigger (HH: 30.0 counts/s) *)
IF rVoted_SparkDetector_cps >= rHH_SparkDetector_cps THEN
    bAlarm_Spark_HH := TRUE;
ELSIF rVoted_SparkDetector_cps <= (rHH_SparkDetector_cps - rDB_SparkDetector_cps) THEN
    bAlarm_Spark_HH := FALSE;
END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.7: DRYING CHAMBER INLET HOT AIR TEMPERATURE 3-TIER ALARMS                             *)
(* ------------------------------------------------------------------------------------------------- *)
(* Low Thermal Delivery Advisory (L: 170.0 deg C) *)
IF rVoted_InletAirTemp_degC <= rL_InletAirTemp_degC THEN
    bAlarm_InletAirTemp_L := TRUE;
ELSIF rVoted_InletAirTemp_degC >= (rL_InletAirTemp_degC + rDB_InletAirTemp_degC) THEN
    bAlarm_InletAirTemp_L := FALSE;
END_IF;

(* High Thermal Warning (H: 215.0 deg C) *)
IF rVoted_InletAirTemp_degC >= rH_InletAirTemp_degC THEN
    bAlarm_InletAirTemp_H := TRUE;
ELSIF rVoted_InletAirTemp_degC <= (rH_InletAirTemp_degC - rDB_InletAirTemp_degC) THEN
    bAlarm_InletAirTemp_H := FALSE;
END_IF;

(* High-High Burner Emergency Trip (HH: 235.0 deg C) *)
IF rVoted_InletAirTemp_degC >= rHH_InletAirTemp_degC THEN
    bAlarm_InletAirTemp_HH := TRUE;
ELSIF rVoted_InletAirTemp_degC <= (rHH_InletAirTemp_degC - rDB_InletAirTemp_degC) THEN
    bAlarm_InletAirTemp_HH := FALSE;
END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.8: FINAL MILK POWDER RESIDUAL MOISTURE 4-TIER ALARMS                                  *)
(* ------------------------------------------------------------------------------------------------- *)
(* Low-Low Over-Drying Thermal Degradation Trip (LL: 2.20 % w/w) *)
IF rVoted_PowderMoisture_pct <= rLL_PowderMoisture_pct THEN
    bAlarm_PowderMoisture_LL := TRUE;
ELSIF rVoted_PowderMoisture_pct >= (rLL_PowderMoisture_pct + rDB_PowderMoisture_pct) THEN
    bAlarm_PowderMoisture_LL := FALSE;
END_IF;

(* Low Moisture Target Departure Alert (L: 3.20 % w/w) *)
IF rVoted_PowderMoisture_pct <= rL_PowderMoisture_pct THEN
    bAlarm_PowderMoisture_L := TRUE;
ELSIF rVoted_PowderMoisture_pct >= (rL_PowderMoisture_pct + rDB_PowderMoisture_pct) THEN
    bAlarm_PowderMoisture_L := FALSE;
END_IF;

(* High Moisture Caking Warning Alert (H: 4.30 % w/w) *)
IF rVoted_PowderMoisture_pct >= rH_PowderMoisture_pct THEN
    bAlarm_PowderMoisture_H := TRUE;
ELSIF rVoted_PowderMoisture_pct <= (rH_PowderMoisture_pct - rDB_PowderMoisture_pct) THEN
    bAlarm_PowderMoisture_H := FALSE;
END_IF;

(* High-High Out-of-Spec Divert Trip (HH: 5.20 % w/w) *)
IF rVoted_PowderMoisture_pct >= rHH_PowderMoisture_pct THEN
    bAlarm_PowderMoisture_HH := TRUE;
ELSIF rVoted_PowderMoisture_pct <= (rHH_PowderMoisture_pct - rDB_PowderMoisture_pct) THEN
    bAlarm_PowderMoisture_HH := FALSE;
END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.9: MECHANICAL & AERODYNAMIC AUXILIARY SAFETY ALARMS                                   *)
(* ------------------------------------------------------------------------------------------------- *)
(* MVR Compressor Bearing Severe Vibration High-High Trip (HH: 6.50 mm/s) *)
IF rVT_903_CompressorVibration_mms >= rHH_CompressorVibe_mms THEN
    bAlarm_CompressorVibe_HH := TRUE;
ELSIF rVT_903_CompressorVibration_mms <= (rHH_CompressorVibe_mms - rDB_CompressorVibe_mms) THEN
    bAlarm_CompressorVibe_HH := FALSE;
END_IF;

(* MVR Compressor Aerodynamic Surge Margin Low Advisory (Threshold: 15.0%) *)
IF rSurgeMargin_pct < 15.0 THEN
    bAlarm_SurgeMargin_Low := TRUE;
ELSIF rSurgeMargin_pct > 20.0 THEN
    bAlarm_SurgeMargin_Low := FALSE;
END_IF;

(* Evaporator Falling Film Recirculation Velocity Low-Low Dry Tube Trip (LL: 0.50 m/s) *)
IF rVoted_RecircVelocity_ms < 0.50 THEN
    bAlarm_RecircVelocity_LL := TRUE;
ELSIF rVoted_RecircVelocity_ms > 0.80 THEN
    bAlarm_RecircVelocity_LL := FALSE;
END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.10: ROOT-CAUSE FIRST-OUT LATCHING EMERGENCY TRIP LOGIC                                *)
(* Evaluates all critical safety trip conditions in strict deterministic priority order.              *)
(* Latches the first initiator bit into dwFirstOutWord and locks out until manual reset.             *)
(* ------------------------------------------------------------------------------------------------- *)
IF NOT bFirstOutLatched THEN
    IF NOT bEmergencyStop THEN
        dwFirstOutWord    := 16#00000001; (* Bit 0: Emergency Stop Hardwired Safety Relay Tripped *)
        bFirstOutLatched  := TRUE;
    ELSIF bAlarm_Spark_HH THEN
        dwFirstOutWord    := 16#00000002; (* Bit 1: Cyclone / Baghouse Optical Spark Fire Detected *)
        bFirstOutLatched  := TRUE;
    ELSIF bAlarm_ChamberPressure_HH THEN
        dwFirstOutWord    := 16#00000004; (* Bit 2: NFPA 68 Chamber High-High Deflagration Pressure *)
        bFirstOutLatched  := TRUE;
    ELSIF bAlarm_ExhaustTemp_HH THEN
        dwFirstOutWord    := 16#00000008; (* Bit 3: Exhaust Air High-High Flash Fire Ignition Trip *)
        bFirstOutLatched  := TRUE;
    ELSIF bAlarm_InletAirTemp_HH THEN
        dwFirstOutWord    := 16#00000010; (* Bit 4: Chamber Inlet Air High-High Burner Shutdown Trip *)
        bFirstOutLatched  := TRUE;
    ELSIF bAlarm_CalandriaLevel_HH THEN
        dwFirstOutWord    := 16#00000020; (* Bit 5: Calandria Sump Level High-High Carryover Trip *)
        bFirstOutLatched  := TRUE;
    ELSIF bAlarm_CalandriaLevel_LL THEN
        dwFirstOutWord    := 16#00000040; (* Bit 6: Calandria Sump Level Low-Low Dry Tube Burnout Trip *)
        bFirstOutLatched  := TRUE;
    ELSIF bAlarm_CompressorVibe_HH THEN
        dwFirstOutWord    := 16#00000080; (* Bit 7: MVR Centrifugal Turbo High-High Severe Vibration *)
        bFirstOutLatched  := TRUE;
    ELSIF bAlarm_MvrDiffPress_HH THEN
        dwFirstOutWord    := 16#00000100; (* Bit 8: MVR Compressor Differential Pressure High-High *)
        bFirstOutLatched  := TRUE;
    ELSIF bAlarm_MvrDiffPress_LL THEN
        dwFirstOutWord    := 16#00000200; (* Bit 9: MVR Compressor Differential Pressure Low-Low *)
        bFirstOutLatched  := TRUE;
    ELSIF bAlarm_SolidsBrix_HH THEN
        dwFirstOutWord    := 16#00000400; (* Bit 10: Concentrated Solids High-High Tube Plugging Trip *)
        bFirstOutLatched  := TRUE;
    ELSIF bAlarm_PowderMoisture_HH THEN
        dwFirstOutWord    := 16#00000800; (* Bit 11: Final Powder Moisture High-High Out-of-Spec Divert *)
        bFirstOutLatched  := TRUE;
    ELSIF bAlarm_RecircVelocity_LL THEN
        dwFirstOutWord    := 16#00001000; (* Bit 12: Falling Film Recirculation Velocity Low-Low Trip *)
        bFirstOutLatched  := TRUE;
    ELSIF bFireDelugeManualTrigger THEN
        dwFirstOutWord    := 16#00002000; (* Bit 13: Manual Emergency Fire Deluge Pushbutton Actuated *)
        bFirstOutLatched  := TRUE;
    ELSIF (nDegradedMode_LT101 = 3) OR (nDegradedMode_DT201 = 3) OR (nDegradedMode_PDT301 = 3) OR
          (nDegradedMode_TT401 = 3) OR (nDegradedMode_IRT501 = 3) THEN
        dwFirstOutWord    := 16#00004000; (* Bit 14: TMR Critical Sensor Group Triple Channel Fail *)
        bFirstOutLatched  := TRUE;
    END_IF;
END_IF;

(* Operator Latching Trip Reset Permissive Check *)
IF bResetTrips AND bAcknowledgeFault AND bEmergencyStop AND (NOT bFireDelugeManualTrigger) AND (rVoted_SparkDetector_cps < rH_SparkDetector_cps) THEN
    dwFirstOutWord            := 16#00000000;
    bFirstOutLatched          := FALSE;
    bEmergencyShutdownTripped := FALSE;
END_IF;

(* Master Process Trip Flag Integration *)
bEmergencyShutdownTripped := bFirstOutLatched OR (NOT bEmergencyStop) OR (eState = 12) OR (eState = 13);

(* ------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.11: QUALITY SPECIFICATIONS & SYSTEM HEALTH SUPERVISION                                *)
(* ------------------------------------------------------------------------------------------------- *)
(* Commercial Milk Concentrate Solids Target Quality Window (48.0 to 52.5% TS) *)
bConcentrateOnSpec := (rVoted_SolidsBrix_pct >= 48.0) AND (rVoted_SolidsBrix_pct <= 52.5);

(* Finished Agglomerated Milk Powder Target Moisture Specification (3.40 to 4.20% w/w) *)
bPowderMoistureOnSpec := (rVoted_PowderMoisture_pct >= 3.40) AND (rVoted_PowderMoisture_pct <= 4.20);

(* Overall Cyber-Physical System Healthy Permissive Interlock *)
bSystemHealthy := bEnableSystem AND
                  bEmergencyStop AND
                  (NOT bEmergencyShutdownTripped) AND
                  (nDegradedMode_LT101 < 3) AND
                  (nDegradedMode_DT201 < 3) AND
                  (nDegradedMode_PDT301 < 3) AND
                  (nDegradedMode_TT401 < 3) AND
                  (nDegradedMode_IRT501 < 3);

(* Active 14-Stage FSM State Telemetry Pointer *)
nActiveState := eState;

(* ------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.12: BIT-PACKED 32-BIT TELEMETRY DWORD 1 (OPERATIONAL STATUS & ACTUATORS)              *)
(* ------------------------------------------------------------------------------------------------- *)
dwStatusWord1 := 16#00000000;

IF bEnableSystem THEN dwStatusWord1 := dwStatusWord1 OR 16#00000001; END_IF;
IF bEmergencyStop THEN dwStatusWord1 := dwStatusWord1 OR 16#00000002; END_IF;
IF (eState >= 4) AND (eState <= 9) THEN dwStatusWord1 := dwStatusWord1 OR 16#00000004; END_IF;
IF eState = 1 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000008; END_IF;
IF eState = 2 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF;
IF eState >= 3 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF;
IF rSPD_MvrCompressor_rpm > 500.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF;
IF rCV_BurnerGasModulation_pct > 5.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF;
IF rCV_AtomizerNozzlePress_bar > 50.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF;
IF rCV_FluidBedSupplyFan_pct > 10.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF;
IF rCV_DensePhaseConveyAir_pct > 10.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF;
IF bConcentrateOnSpec THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF;
IF bPowderMoistureOnSpec THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF;
IF rCV_SlurryDivertValve_pct > 50.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF;
IF bAntiSurgeActive THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF;
IF bExplosionSuppressionArm THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF;
IF bHRD_ExplosionCannonsFire THEN dwStatusWord1 := dwStatusWord1 OR 16#00010000; END_IF;
IF bFireDelugeActive THEN dwStatusWord1 := dwStatusWord1 OR 16#00020000; END_IF;
IF bExplosionIsolationValvesClose THEN dwStatusWord1 := dwStatusWord1 OR 16#00040000; END_IF;
IF bEmergencyShutdownTripped THEN dwStatusWord1 := dwStatusWord1 OR 16#00080000; END_IF;
IF bSystemHealthy THEN dwStatusWord1 := dwStatusWord1 OR 16#00100000; END_IF;
IF bBaghouseShakerEnable THEN dwStatusWord1 := dwStatusWord1 OR 16#00200000; END_IF;
IF bFluidBedVibratorRunPermissive THEN dwStatusWord1 := dwStatusWord1 OR 16#00400000; END_IF;
IF bPowderSifterHealthy THEN dwStatusWord1 := dwStatusWord1 OR 16#00800000; END_IF;

(* Encode Active FSM State into Bits 24..27 *)
CASE eState OF
    0:  dwStatusWord1 := dwStatusWord1 OR 16#00000000;
    1:  dwStatusWord1 := dwStatusWord1 OR 16#01000000;
    2:  dwStatusWord1 := dwStatusWord1 OR 16#02000000;
    3:  dwStatusWord1 := dwStatusWord1 OR 16#03000000;
    4:  dwStatusWord1 := dwStatusWord1 OR 16#04000000;
    5:  dwStatusWord1 := dwStatusWord1 OR 16#05000000;
    6:  dwStatusWord1 := dwStatusWord1 OR 16#06000000;
    7:  dwStatusWord1 := dwStatusWord1 OR 16#07000000;
    8:  dwStatusWord1 := dwStatusWord1 OR 16#08000000;
    9:  dwStatusWord1 := dwStatusWord1 OR 16#09000000;
    10: dwStatusWord1 := dwStatusWord1 OR 16#0A000000;
    11: dwStatusWord1 := dwStatusWord1 OR 16#0B000000;
    12: dwStatusWord1 := dwStatusWord1 OR 16#0C000000;
    13: dwStatusWord1 := dwStatusWord1 OR 16#0D000000;
ELSE
    dwStatusWord1 := dwStatusWord1 OR 16#0F000000;
END_CASE;

(* Bit 31: Heartbeat Toggle Bit (Toggles every 50 execution cycles = 1.0 s) *)
IF (nCycleCounter MOD 50) < 25 THEN
    dwStatusWord1 := dwStatusWord1 OR 16#80000000;
END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.13: BIT-PACKED 32-BIT TELEMETRY DWORD 2 (TMR SENSOR HEALTH & SUBSYSTEM PERMISSIVES)   *)
(* ------------------------------------------------------------------------------------------------- *)
dwStatusWord2 := 16#00000000;

(* TMR Sensor Channel Health Bits (Bits 0..23) *)
dwStatusWord2 := dwStatusWord2 OR (WORD_TO_DWORD(wTmrHealth_LT101 AND 16#0007));
dwStatusWord2 := dwStatusWord2 OR SHL(WORD_TO_DWORD(wTmrHealth_DT201 AND 16#0007), 3);
dwStatusWord2 := dwStatusWord2 OR SHL(WORD_TO_DWORD(wTmrHealth_PDT301 AND 16#0007), 6);
dwStatusWord2 := dwStatusWord2 OR SHL(WORD_TO_DWORD(wTmrHealth_TT401 AND 16#0007), 9);
dwStatusWord2 := dwStatusWord2 OR SHL(WORD_TO_DWORD(wTmrHealth_IRT501 AND 16#0007), 12);
dwStatusWord2 := dwStatusWord2 OR SHL(WORD_TO_DWORD(wTmrHealth_TT601 AND 16#0007), 15);
dwStatusWord2 := dwStatusWord2 OR SHL(WORD_TO_DWORD(wTmrHealth_MT701 AND 16#0007), 18);
dwStatusWord2 := dwStatusWord2 OR SHL(WORD_TO_DWORD(wTmrHealth_FT801 AND 16#0007), 21);

(* Auxiliary Subsystem Permissives & Latches (Bits 24..31) *)
IF bBaghouseShakerEnable THEN dwStatusWord2 := dwStatusWord2 OR 16#01000000; END_IF;
IF bFluidBedVibratorRunPermissive THEN dwStatusWord2 := dwStatusWord2 OR 16#02000000; END_IF;
IF bPowderSifterHealthy THEN dwStatusWord2 := dwStatusWord2 OR 16#04000000; END_IF;
IF bFirstOutLatched THEN dwStatusWord2 := dwStatusWord2 OR 16#08000000; END_IF;
IF bInitialized THEN dwStatusWord2 := dwStatusWord2 OR 16#10000000; END_IF;
IF bConcentrateDivertManual THEN dwStatusWord2 := dwStatusWord2 OR 16#20000000; END_IF;
IF bCipVerificationRequest THEN dwStatusWord2 := dwStatusWord2 OR 16#40000000; END_IF;
IF bWaterBalanceRequest THEN dwStatusWord2 := dwStatusWord2 OR 16#80000000; END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.14: BIT-PACKED 32-BIT TELEMETRY DWORD 3 (EVAPORATOR & MVR PROCESS ALARMS)            *)
(* ------------------------------------------------------------------------------------------------- *)
dwAlarmWord1 := 16#00000000;

IF bAlarm_CalandriaLevel_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF;
IF bAlarm_CalandriaLevel_L  THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF;
IF bAlarm_CalandriaLevel_H  THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF;
IF bAlarm_CalandriaLevel_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF;
IF bAlarm_SolidsBrix_LL     THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF;
IF bAlarm_SolidsBrix_L      THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF;
IF bAlarm_SolidsBrix_H      THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF;
IF bAlarm_SolidsBrix_HH     THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF;
IF bAlarm_MvrDiffPress_LL   THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; END_IF;
IF bAlarm_MvrDiffPress_L    THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; END_IF;
IF bAlarm_MvrDiffPress_H    THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000400; END_IF;
IF bAlarm_MvrDiffPress_HH   THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000800; END_IF;
IF bAlarm_SurgeMargin_Low   THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00001000; END_IF;
IF bAlarm_CompressorVibe_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00002000; END_IF;
IF bAlarm_RecircVelocity_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00004000; END_IF;

(* TMR Sensor Channel Single/Dual Degraded Alarms (Bits 16..23) *)
IF nDegradedMode_LT101 > 0 THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00010000; END_IF;
IF nDegradedMode_DT201 > 0 THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00020000; END_IF;
IF nDegradedMode_PDT301 > 0 THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00040000; END_IF;
IF nDegradedMode_TT401 > 0 THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00080000; END_IF;
IF nDegradedMode_IRT501 > 0 THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00100000; END_IF;
IF nDegradedMode_TT601 > 0 THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00200000; END_IF;
IF nDegradedMode_MT701 > 0 THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00400000; END_IF;
IF nDegradedMode_FT801 > 0 THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00800000; END_IF;

(* Auxiliary Evaporator Diagnostic Alarms (Bits 24..31) *)
IF rQT_905_CipConductivity_mScm > 5.0 THEN dwAlarmWord1 := dwAlarmWord1 OR 16#01000000; END_IF;
IF rPT_906_LiveSteamHeader_bar < 2.5 THEN dwAlarmWord1 := dwAlarmWord1 OR 16#02000000; END_IF;
IF (rFT_904_MilkFeedFlow_kgh < 10000.0) AND (eState >= 4) THEN dwAlarmWord1 := dwAlarmWord1 OR 16#04000000; END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.15: BIT-PACKED 32-BIT TELEMETRY DWORD 4 (SPRAY DRYER, BURNER & NFPA ALARMS)           *)
(* ------------------------------------------------------------------------------------------------- *)
dwAlarmWord2 := 16#00000000;

IF bAlarm_ExhaustTemp_L      THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF;
IF bAlarm_ExhaustTemp_H      THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF;
IF bAlarm_ExhaustTemp_HH     THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF;
IF bAlarm_Spark_H            THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF;
IF bAlarm_Spark_HH           THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF;
IF bAlarm_InletAirTemp_L     THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF;
IF bAlarm_InletAirTemp_H     THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF;
IF bAlarm_InletAirTemp_HH    THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; END_IF;
IF bAlarm_PowderMoisture_LL  THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; END_IF;
IF bAlarm_PowderMoisture_L   THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; END_IF;
IF bAlarm_PowderMoisture_H   THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000400; END_IF;
IF bAlarm_PowderMoisture_HH  THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000800; END_IF;
IF bAlarm_ChamberPressure_HH THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00001000; END_IF;
IF NOT bEmergencyStop        THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00002000; END_IF;
IF bFireDelugeManualTrigger  THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00004000; END_IF;
IF NOT bPowderSifterHealthy  THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00008000; END_IF;
IF NOT bBaghouseShakerEnable THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00010000; END_IF;
IF NOT bFluidBedVibratorRunPermissive THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00020000; END_IF;

(* Additional Spray Dryer Environmental & Mechanical Diagnostics *)
IF rPT_901_ChamberPressure_Pa > -20.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00040000; END_IF; (* Loss of Vacuum Draft *)
IF rPT_901_ChamberPressure_Pa < -250.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00080000; END_IF; (* Excessive Draft Vacuum *)
IF rTT_908_FluidBedZone1Temp_degC > 88.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00100000; END_IF; (* Fluid Bed Zone 1 High Temp *)
IF rTT_909_FluidBedZone2Temp_degC > 28.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00200000; END_IF; (* Fluid Bed Zone 2 Chilling Warm *)
IF rAT_910_BurnerCombustionO2_pct < 1.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00400000; END_IF; (* Incomplete Combustion Warning *)
IF (rPT_907_AtomizerFeedPress_bar < 130.0) AND (eState = 7) THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00800000; END_IF; (* Slurry Feed Pressure Low *)

(* ------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.16: ACTUATOR SLEW DYNAMIC MEMORY UPDATE FOR NEXT EXECUTION CYCLE                     *)
(* ------------------------------------------------------------------------------------------------- *)
vec_uPrev[1] := rCV_FeedRateValve_pct;
vec_uPrev[2] := rSPD_MvrCompressor_rpm;
vec_uPrev[3] := rCV_SteamInjectionValve_pct;
vec_uPrev[4] := rCV_AtomizerNozzlePress_bar;
vec_uPrev[5] := rCV_BurnerGasModulation_pct;
vec_uPrev[6] := rCV_ExhaustDamper_pct;

END_FUNCTION_BLOCK"""
