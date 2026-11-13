# fccu_builder/part6_phase5_actuators_and_phase6_alarms_telemetry.py

def get_part6_phase5_actuators_and_phase6_alarms_telemetry():
    lines = []
    lines.append("""(*
========================================================================================================================
  PHASE 5: ACTUATOR SLEW RATE LIMITING, MECHANICAL SATURATION & SAFETY PRIORITY ARBITRATION
========================================================================================================================
*)
(* ---------------------------------------------------------------------------------------------------------------------
   5.1 Actuator Priority Arbitration & Slew Rate Limiting
   Priority 1: SIL-3 Slide Valve Anti-Reversal Fast Deflagration Interlock (<50 ms closure)
   Priority 2: SIL-3 Master Emergency Stop / Plant Trip
   Priority 3: Normal Rate-Limited Tracking towards Target Setpoints
   --------------------------------------------------------------------------------------------------------------------- *)

(* 1. Regenerated Catalyst Slide Valve (RCSV) Position [%] *)
IF bAntiReversalLockActive OR bEmergencyTripActive THEN
    (* Instantaneous SIL-3 Fast Emergency Cutoff *)
    rActuator_RCSV_Pos_pct := 0.0;
ELSE
    IF (rActuator_RCSV_Target_pct - rActuator_RCSV_Pos_pct) > (rSlewRate_RCSV_pct_s * rTs_sec) THEN
        rActuator_RCSV_Pos_pct := rActuator_RCSV_Pos_pct + (rSlewRate_RCSV_pct_s * rTs_sec);
    ELSIF (rActuator_RCSV_Target_pct - rActuator_RCSV_Pos_pct) < (-rSlewRate_RCSV_pct_s * rTs_sec) THEN
        rActuator_RCSV_Pos_pct := rActuator_RCSV_Pos_pct - (rSlewRate_RCSV_pct_s * rTs_sec);
    ELSE
        rActuator_RCSV_Pos_pct := rActuator_RCSV_Target_pct;
    END_IF;
END_IF;
IF rActuator_RCSV_Pos_pct < 0.0 THEN
    rActuator_RCSV_Pos_pct := 0.0;
ELSIF rActuator_RCSV_Pos_pct > 100.0 THEN
    rActuator_RCSV_Pos_pct := 100.0;
END_IF;

(* 2. Spent Catalyst Slide Valve (SCSV) Position [%] *)
IF bAntiReversalLockActive OR bEmergencyTripActive THEN
    (* Instantaneous SIL-3 Fast Emergency Cutoff *)
    rActuator_SCSV_Pos_pct := 0.0;
ELSE
    IF (rActuator_SCSV_Target_pct - rActuator_SCSV_Pos_pct) > (rSlewRate_SCSV_pct_s * rTs_sec) THEN
        rActuator_SCSV_Pos_pct := rActuator_SCSV_Pos_pct + (rSlewRate_SCSV_pct_s * rTs_sec);
    ELSIF (rActuator_SCSV_Target_pct - rActuator_SCSV_Pos_pct) < (-rSlewRate_SCSV_pct_s * rTs_sec) THEN
        rActuator_SCSV_Pos_pct := rActuator_SCSV_Pos_pct - (rSlewRate_SCSV_pct_s * rTs_sec);
    ELSE
        rActuator_SCSV_Pos_pct := rActuator_SCSV_Target_pct;
    END_IF;
END_IF;
IF rActuator_SCSV_Pos_pct < 0.0 THEN
    rActuator_SCSV_Pos_pct := 0.0;
ELSIF rActuator_SCSV_Pos_pct > 100.0 THEN
    rActuator_SCSV_Pos_pct := 100.0;
END_IF;

(* 3. Combustion Air Blower VFD / Guide Vane Command [%] *)
IF (rActuator_AirBlower_Target_pct - rActuator_AirBlower_pct) > (rSlewRate_AirBlower_pct_s * rTs_sec) THEN
    rActuator_AirBlower_pct := rActuator_AirBlower_pct + (rSlewRate_AirBlower_pct_s * rTs_sec);
ELSIF (rActuator_AirBlower_Target_pct - rActuator_AirBlower_pct) < (-rSlewRate_AirBlower_pct_s * rTs_sec) THEN
    rActuator_AirBlower_pct := rActuator_AirBlower_pct - (rSlewRate_AirBlower_pct_s * rTs_sec);
ELSE
    rActuator_AirBlower_pct := rActuator_AirBlower_Target_pct;
END_IF;
IF rActuator_AirBlower_pct < 10.0 THEN
    rActuator_AirBlower_pct := 10.0; (* Minimum preservation purge velocity *)
ELSIF rActuator_AirBlower_pct > 100.0 THEN
    rActuator_AirBlower_pct := 100.0;
END_IF;

(* 4. Auxiliary Torch Oil Injection Fuel Valve Command [%] *)
IF bEmergencyTripActive OR NOT bTorchOilPermissive THEN
    rActuator_TorchOil_pct := 0.0;
ELSE
    IF (rActuator_TorchOil_Target_pct - rActuator_TorchOil_pct) > (rSlewRate_TorchOil_pct_s * rTs_sec) THEN
        rActuator_TorchOil_pct := rActuator_TorchOil_pct + (rSlewRate_TorchOil_pct_s * rTs_sec);
    ELSIF (rActuator_TorchOil_Target_pct - rActuator_TorchOil_pct) < (-rSlewRate_TorchOil_pct_s * rTs_sec) THEN
        rActuator_TorchOil_pct := rActuator_TorchOil_pct - (rSlewRate_TorchOil_pct_s * rTs_sec);
    ELSE
        rActuator_TorchOil_pct := rActuator_TorchOil_Target_pct;
    END_IF;
END_IF;
IF rActuator_TorchOil_pct < 0.0 THEN
    rActuator_TorchOil_pct := 0.0;
ELSIF rActuator_TorchOil_pct > 100.0 THEN
    rActuator_TorchOil_pct := 100.0;
END_IF;

(* 5. Riser Lift Steam Control Valve Command [%] *)
IF bAntiReversalLockActive THEN
    (* Full emergency steam blanket sweep *)
    rActuator_LiftSteam_pct := 100.0;
ELSE
    IF (rActuator_LiftSteam_Target_pct - rActuator_LiftSteam_pct) > (rSlewRate_LiftSteam_pct_s * rTs_sec) THEN
        rActuator_LiftSteam_pct := rActuator_LiftSteam_pct + (rSlewRate_LiftSteam_pct_s * rTs_sec);
    ELSIF (rActuator_LiftSteam_Target_pct - rActuator_LiftSteam_pct) < (-rSlewRate_LiftSteam_pct_s * rTs_sec) THEN
        rActuator_LiftSteam_pct := rActuator_LiftSteam_pct - (rSlewRate_LiftSteam_pct_s * rTs_sec);
    ELSE
        rActuator_LiftSteam_pct := rActuator_LiftSteam_Target_pct;
    END_IF;
END_IF;
IF rActuator_LiftSteam_pct < 15.0 THEN
    rActuator_LiftSteam_pct := 15.0; (* Minimum warming purge *)
ELSIF rActuator_LiftSteam_pct > 100.0 THEN
    rActuator_LiftSteam_pct := 100.0;
END_IF;

(* 6. Flue Gas Double-Disc Slide Valve Backpressure Command [%] *)
IF (rActuator_FlueGasValve_Target_pct - rActuator_FlueGasValve_pct) > (rSlewRate_FlueGasValve_pct_s * rTs_sec) THEN
    rActuator_FlueGasValve_pct := rActuator_FlueGasValve_pct + (rSlewRate_FlueGasValve_pct_s * rTs_sec);
ELSIF (rActuator_FlueGasValve_Target_pct - rActuator_FlueGasValve_pct) < (-rSlewRate_FlueGasValve_pct_s * rTs_sec) THEN
    rActuator_FlueGasValve_pct := rActuator_FlueGasValve_pct - (rSlewRate_FlueGasValve_pct_s * rTs_sec);
ELSE
    rActuator_FlueGasValve_pct := rActuator_FlueGasValve_Target_pct;
END_IF;
IF rActuator_FlueGasValve_pct < 10.0 THEN
    rActuator_FlueGasValve_pct := 10.0;
ELSIF rActuator_FlueGasValve_pct > 100.0 THEN
    rActuator_FlueGasValve_pct := 100.0;
END_IF;

(* 7. Regenerator Dilute Phase Quench Water Emergency Valve [%] *)
IF (rActuator_QuenchWater_Target_pct - rActuator_QuenchWater_pct) > (rSlewRate_QuenchWater_pct_s * rTs_sec) THEN
    rActuator_QuenchWater_pct := rActuator_QuenchWater_pct + (rSlewRate_QuenchWater_pct_s * rTs_sec);
ELSIF (rActuator_QuenchWater_Target_pct - rActuator_QuenchWater_pct) < (-rSlewRate_QuenchWater_pct_s * rTs_sec) THEN
    rActuator_QuenchWater_pct := rActuator_QuenchWater_pct - (rSlewRate_QuenchWater_pct_s * rTs_sec);
ELSE
    rActuator_QuenchWater_pct := rActuator_QuenchWater_Target_pct;
END_IF;
IF rActuator_QuenchWater_pct < 0.0 THEN
    rActuator_QuenchWater_pct := 0.0;
ELSIF rActuator_QuenchWater_pct > 100.0 THEN
    rActuator_QuenchWater_pct := 100.0;
END_IF;

(* 8. Main Hydrocarbon Feed Safety Emergency Cutoff Valve [%] *)
IF bEmergencyTripActive OR bAntiReversalLockActive OR NOT bFeedCutPermissive THEN
    rActuator_FeedCutoff_pct := 0.0;
ELSE
    rActuator_FeedCutoff_pct := rActuator_FeedCutoff_Target_pct;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
   5.2 Update Historical Actuator Vector u_prev and u_cmd for Continuous Discrete Simulation
   --------------------------------------------------------------------------------------------------------------------- *)
u_prev[1] := rActuator_RCSV_Pos_pct;
u_prev[2] := rActuator_SCSV_Pos_pct;
u_prev[3] := rActuator_AirBlower_pct;
u_prev[4] := rActuator_TorchOil_pct;
u_prev[5] := rActuator_LiftSteam_pct;
u_prev[6] := rActuator_FlueGasValve_pct;

u_cmd[1] := rActuator_RCSV_Pos_pct;
u_cmd[2] := rActuator_SCSV_Pos_pct;
u_cmd[3] := rActuator_AirBlower_pct;
u_cmd[4] := rActuator_TorchOil_pct;
u_cmd[5] := rActuator_LiftSteam_pct;
u_cmd[6] := rActuator_FlueGasValve_pct;


(*
========================================================================================================================
  PHASE 6: ISA-18.2 MULTI-TIER PROCESS ALARMS, REVERSE FLOW INTERLOCK & 32-BIT TELEMETRY
========================================================================================================================
*)
(* ---------------------------------------------------------------------------------------------------------------------
   6.1 ISA-18.2 Process Alarm Engine with Deadband Hysteresis & Delay Timers
   --------------------------------------------------------------------------------------------------------------------- *)
(* 1. Riser Outlet Temperature Alarms (rVoted_RiserTemp_degC) *)
(* High-High Trip (HH) *)
IF rVoted_RiserTemp_degC >= rAlarm_RiserTemp_HH_degC THEN
    rTimer_Alarm_RiserTemp_HH_sec := rTimer_Alarm_RiserTemp_HH_sec + rTs_sec;
    IF rTimer_Alarm_RiserTemp_HH_sec >= 0.500 THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; (* Bit 0 *)
        IF dwFirstOutWord = 16#00000000 THEN dwFirstOutWord := 16#00000003; END_IF;
    END_IF;
ELSIF rVoted_RiserTemp_degC <= (rAlarm_RiserTemp_HH_degC - rHyst_RiserTemp_degC) THEN
    rTimer_Alarm_RiserTemp_HH_sec := 0.0;
    dwAlarmWord1 := dwAlarmWord1 AND 16#FFFFFFFE;
END_IF;

(* High Warning (H) *)
IF rVoted_RiserTemp_degC >= rAlarm_RiserTemp_H_degC THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; (* Bit 0 *)
ELSIF rVoted_RiserTemp_degC <= (rAlarm_RiserTemp_H_degC - rHyst_RiserTemp_degC) THEN
    dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFFFFE;
END_IF;

(* Low Warning (L) *)
IF (rVoted_RiserTemp_degC <= rAlarm_RiserTemp_L_degC) AND (eState >= 6) THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; (* Bit 1 *)
ELSIF rVoted_RiserTemp_degC >= (rAlarm_RiserTemp_L_degC + rHyst_RiserTemp_degC) THEN
    dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFFFFD;
END_IF;

(* Low-Low Trip (LL) - Cold Catalyst Slump Hazard *)
IF (rVoted_RiserTemp_degC <= rAlarm_RiserTemp_LL_degC) AND (eState >= 6) THEN
    rTimer_Alarm_RiserTemp_LL_sec := rTimer_Alarm_RiserTemp_LL_sec + rTs_sec;
    IF rTimer_Alarm_RiserTemp_LL_sec >= 1.000 THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; (* Bit 1 *)
        IF dwFirstOutWord = 16#00000000 THEN dwFirstOutWord := 16#00000004; END_IF;
    END_IF;
ELSIF rVoted_RiserTemp_degC >= (rAlarm_RiserTemp_LL_degC + rHyst_RiserTemp_degC) THEN
    rTimer_Alarm_RiserTemp_LL_sec := 0.0;
    dwAlarmWord1 := dwAlarmWord1 AND 16#FFFFFFFD;
END_IF;

(* 2. Riser Top Differential Pressure Alarms (rPDT_RISER_TOTAL_kPa) *)
(* High-High Trip (HH) - Choking / Solid Bed Slumping *)
IF rPDT_RISER_TOTAL_kPa >= rAlarm_RiserDP_HH_kPa THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; (* Bit 2 *)
ELSIF rPDT_RISER_TOTAL_kPa <= (rAlarm_RiserDP_HH_kPa - rHyst_RiserDP_kPa) THEN
    dwAlarmWord1 := dwAlarmWord1 AND 16#FFFFFFFB;
END_IF;

(* High Warning (H) *)
IF rPDT_RISER_TOTAL_kPa >= rAlarm_RiserDP_H_kPa THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; (* Bit 2 *)
ELSIF rPDT_RISER_TOTAL_kPa <= (rAlarm_RiserDP_H_kPa - rHyst_RiserDP_kPa) THEN
    dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFFFFB;
END_IF;

(* Low Warning (L) *)
IF (rPDT_RISER_TOTAL_kPa <= rAlarm_RiserDP_L_kPa) AND (eState >= 6) THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; (* Bit 3 *)
ELSIF rPDT_RISER_TOTAL_kPa >= (rAlarm_RiserDP_L_kPa + rHyst_RiserDP_kPa) THEN
    dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFFFF7;
END_IF;

(* Low-Low Trip (LL) - Loss of Solids Lift *)
IF (rPDT_RISER_TOTAL_kPa <= rAlarm_RiserDP_LL_kPa) AND (eState >= 6) THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; (* Bit 3 *)
ELSIF rPDT_RISER_TOTAL_kPa >= (rAlarm_RiserDP_LL_kPa + rHyst_RiserDP_kPa) THEN
    dwAlarmWord1 := dwAlarmWord1 AND 16#FFFFFFF7;
END_IF;

(* 3. Regenerator Dense Bed Temperature Alarms (rVoted_RegenBedTemp_degC) *)
(* High-High Trip (HH) - Refractory Thermal Breakdown *)
IF rVoted_RegenBedTemp_degC >= rAlarm_RegenBed_HH_degC THEN
    rTimer_Alarm_RegenBed_HH_sec := rTimer_Alarm_RegenBed_HH_sec + rTs_sec;
    IF rTimer_Alarm_RegenBed_HH_sec >= 0.500 THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; (* Bit 4 *)
        IF dwFirstOutWord = 16#00000000 THEN dwFirstOutWord := 16#00000005; END_IF;
    END_IF;
ELSIF rVoted_RegenBedTemp_degC <= (rAlarm_RegenBed_HH_degC - rHyst_RegenBed_degC) THEN
    rTimer_Alarm_RegenBed_HH_sec := 0.0;
    dwAlarmWord1 := dwAlarmWord1 AND 16#FFFFFFEF;
END_IF;

(* High Warning (H) *)
IF rVoted_RegenBedTemp_degC >= rAlarm_RegenBed_H_degC THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; (* Bit 4 *)
ELSIF rVoted_RegenBedTemp_degC <= (rAlarm_RegenBed_H_degC - rHyst_RegenBed_degC) THEN
    dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFFFEF;
END_IF;

(* Low Warning (L) *)
IF (rVoted_RegenBedTemp_degC <= rAlarm_RegenBed_L_degC) AND (eState >= 3) THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; (* Bit 5 *)
ELSIF rVoted_RegenBedTemp_degC >= (rAlarm_RegenBed_L_degC + rHyst_RegenBed_degC) THEN
    dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFFFDF;
END_IF;

(* Low-Low Trip (LL) - Loss of Catalyst Bed Combustion *)
IF (rVoted_RegenBedTemp_degC <= rAlarm_RegenBed_LL_degC) AND (eState >= 3) THEN
    rTimer_Alarm_RegenBed_LL_sec := rTimer_Alarm_RegenBed_LL_sec + rTs_sec;
    IF rTimer_Alarm_RegenBed_LL_sec >= 2.000 THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; (* Bit 5 *)
    END_IF;
ELSIF rVoted_RegenBedTemp_degC >= (rAlarm_RegenBed_LL_degC + rHyst_RegenBed_degC) THEN
    rTimer_Alarm_RegenBed_LL_sec := 0.0;
    dwAlarmWord1 := dwAlarmWord1 AND 16#FFFFFFDF;
END_IF;

(* 4. Spent Catalyst Slide Valve DP Alarms (rVoted_SCSV_dP_kPa) *)
(* Low-Low SIL-3 Anti-Reversal Deflagration Fast Trip (LL) *)
IF (rVoted_SCSV_dP_kPa <= rAlarm_SlideValveDP_LL_kPa) AND (eState >= 4) THEN
    rTimer_Alarm_SCSV_LL_sec := rTimer_Alarm_SCSV_LL_sec + rTs_sec;
    IF rTimer_Alarm_SCSV_LL_sec >= 0.050 THEN (* <50 ms fast interlock threshold *)
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; (* Bit 6 *)
        IF dwFirstOutWord = 16#00000000 THEN dwFirstOutWord := 16#00000001; END_IF;
    END_IF;
ELSIF rVoted_SCSV_dP_kPa >= (rAlarm_SlideValveDP_LL_kPa + rHyst_SlideValveDP_kPa) THEN
    rTimer_Alarm_SCSV_LL_sec := 0.0;
    dwAlarmWord1 := dwAlarmWord1 AND 16#FFFFFFBF;
END_IF;

(* Low Pre-Alarm Warning (L) *)
IF (rVoted_SCSV_dP_kPa <= rAlarm_SlideValveDP_L_kPa) AND (eState >= 4) THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; (* Bit 6 *)
ELSIF rVoted_SCSV_dP_kPa >= (rAlarm_SlideValveDP_L_kPa + rHyst_SlideValveDP_kPa) THEN
    dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFFFBF;
END_IF;

(* High Warning (H) *)
IF rVoted_SCSV_dP_kPa >= rAlarm_SlideValveDP_H_kPa THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; (* Bit 7 *)
ELSIF rVoted_SCSV_dP_kPa <= (rAlarm_SlideValveDP_H_kPa - rHyst_SlideValveDP_kPa) THEN
    dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFFF7F;
END_IF;

(* 5. Regenerated Catalyst Slide Valve DP Alarms (rVoted_RCSV_dP_kPa) *)
(* Low-Low SIL-3 Anti-Reversal Deflagration Fast Trip (LL) *)
IF (rVoted_RCSV_dP_kPa <= rAlarm_SlideValveDP_LL_kPa) AND (eState >= 4) THEN
    rTimer_Alarm_RCSV_LL_sec := rTimer_Alarm_RCSV_LL_sec + rTs_sec;
    IF rTimer_Alarm_RCSV_LL_sec >= 0.050 THEN (* <50 ms fast interlock threshold *)
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; (* Bit 7 *)
        IF dwFirstOutWord = 16#00000000 THEN dwFirstOutWord := 16#00000001; END_IF;
    END_IF;
ELSIF rVoted_RCSV_dP_kPa >= (rAlarm_SlideValveDP_LL_kPa + rHyst_SlideValveDP_kPa) THEN
    rTimer_Alarm_RCSV_LL_sec := 0.0;
    dwAlarmWord1 := dwAlarmWord1 AND 16#FFFFFF7F;
END_IF;

(* Low Pre-Alarm Warning (L) *)
IF (rVoted_RCSV_dP_kPa <= rAlarm_SlideValveDP_L_kPa) AND (eState >= 4) THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; (* Bit 8 *)
ELSIF rVoted_RCSV_dP_kPa >= (rAlarm_SlideValveDP_L_kPa + rHyst_SlideValveDP_kPa) THEN
    dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFFEFF;
END_IF;

(* High Warning (H) *)
IF rVoted_RCSV_dP_kPa >= rAlarm_SlideValveDP_H_kPa THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; (* Bit 9 *)
ELSIF rVoted_RCSV_dP_kPa <= (rAlarm_SlideValveDP_H_kPa - rHyst_SlideValveDP_kPa) THEN
    dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFFDFF;
END_IF;

(* 6. Flue Gas Excess Oxygen Alarms (rVoted_FlueGasO2_pct) *)
(* High-High Trip (HH) - Potential Dilute Phase Flammability Envelope *)
IF (rVoted_FlueGasO2_pct >= rAlarm_FlueGasO2_HH_pct) AND (eState >= 2) THEN
    rTimer_Alarm_FlueGasO2_HH_sec := rTimer_Alarm_FlueGasO2_HH_sec + rTs_sec;
    IF rTimer_Alarm_FlueGasO2_HH_sec >= 1.000 THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; (* Bit 8 *)
        IF dwFirstOutWord = 16#00000000 THEN dwFirstOutWord := 16#00000007; END_IF;
    END_IF;
ELSIF rVoted_FlueGasO2_pct <= (rAlarm_FlueGasO2_HH_pct - rHyst_FlueGasO2_pct) THEN
    rTimer_Alarm_FlueGasO2_HH_sec := 0.0;
    dwAlarmWord1 := dwAlarmWord1 AND 16#FFFFFEFF;
END_IF;

(* High Warning (H) *)
IF (rVoted_FlueGasO2_pct >= rAlarm_FlueGasO2_H_pct) AND (eState >= 2) THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000400; (* Bit 10 *)
ELSIF rVoted_FlueGasO2_pct <= (rAlarm_FlueGasO2_H_pct - rHyst_FlueGasO2_pct) THEN
    dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFFBFF;
END_IF;

(* Low Warning (L) *)
IF (rVoted_FlueGasO2_pct <= rAlarm_FlueGasO2_L_pct) AND (eState >= 3) THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000800; (* Bit 11 *)
ELSIF rVoted_FlueGasO2_pct >= (rAlarm_FlueGasO2_L_pct + rHyst_FlueGasO2_pct) THEN
    dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFF7FF;
END_IF;

(* Low-Low Trip (LL) - Incomplete Combustion & CO Runaway Hazard *)
IF (rVoted_FlueGasO2_pct <= rAlarm_FlueGasO2_LL_pct) AND (eState >= 3) THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; (* Bit 9 *)
ELSIF rVoted_FlueGasO2_pct >= (rAlarm_FlueGasO2_LL_pct + rHyst_FlueGasO2_pct) THEN
    dwAlarmWord1 := dwAlarmWord1 AND 16#FFFFFDFF;
END_IF;

(* 7. Flue Gas Carbon Monoxide Alarms (rAT_CO_FLUEGAS_ppmv) *)
(* High-High Trip (HH) *)
IF (rAT_CO_FLUEGAS_ppmv >= rAlarm_FlueGasCO_HH_ppmv) AND (eState >= 3) THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000400; (* Bit 10 *)
ELSIF rAT_CO_FLUEGAS_ppmv <= (rAlarm_FlueGasCO_HH_ppmv - rHyst_FlueGasCO_ppmv) THEN
    dwAlarmWord1 := dwAlarmWord1 AND 16#FFFFFBFF;
END_IF;

(* High Warning (H) *)
IF (rAT_CO_FLUEGAS_ppmv >= rAlarm_FlueGasCO_H_ppmv) AND (eState >= 3) THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00001000; (* Bit 12 *)
ELSIF rAT_CO_FLUEGAS_ppmv <= (rAlarm_FlueGasCO_H_ppmv - rHyst_FlueGasCO_ppmv) THEN
    dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFEFFF;
END_IF;

(* 8. Regenerator Cyclone Dilute Phase Afterburning Alarms (rAfterburnDeltaT_degC) *)
(* High-High Extreme Thermal Quench Trip (HH) *)
IF rAfterburnDeltaT_degC >= rAlarm_Afterburn_HH_degC THEN
    rTimer_Alarm_Afterburn_HH_sec := rTimer_Alarm_Afterburn_HH_sec + rTs_sec;
    IF rTimer_Alarm_Afterburn_HH_sec >= 0.300 THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000800; (* Bit 11 *)
        IF dwFirstOutWord = 16#00000000 THEN dwFirstOutWord := 16#00000006; END_IF;
    END_IF;
ELSIF rAfterburnDeltaT_degC <= (rAlarm_Afterburn_HH_degC - rHyst_Afterburn_degC) THEN
    rTimer_Alarm_Afterburn_HH_sec := 0.0;
    dwAlarmWord1 := dwAlarmWord1 AND 16#FFFFF7FF;
END_IF;

(* High Advisory Warning (H) *)
IF rAfterburnDeltaT_degC >= rAlarm_Afterburn_H_degC THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00002000; (* Bit 13 *)
ELSIF rAfterburnDeltaT_degC <= (rAlarm_Afterburn_H_degC - rHyst_Afterburn_degC) THEN
    dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFDFFF;
END_IF;

(* 9. Hardware & Plant Permissive Diagnostic Faults in dwAlarmWord1 *)
IF bEmergencyStop THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00001000; (* Bit 12: Emergency Stop Pressed *)
    IF dwFirstOutWord = 16#00000000 THEN dwFirstOutWord := 16#00000002; END_IF;
ELSE
    dwAlarmWord1 := dwAlarmWord1 AND 16#FFFFEFFF;
END_IF;

IF bAirBlowerTripFeedback THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00002000; (* Bit 13: Air Blower Tripped *)
    IF dwFirstOutWord = 16#00000000 THEN dwFirstOutWord := 16#00000005; END_IF;
ELSE
    dwAlarmWord1 := dwAlarmWord1 AND 16#FFFFDFFF;
END_IF;

IF NOT bSlideValveHydraulicOk THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00004000; (* Bit 14: Slide Valve Hydraulic Power Unit Fault *)
    IF dwFirstOutWord = 16#00000000 THEN dwFirstOutWord := 16#00000008; END_IF;
ELSE
    dwAlarmWord1 := dwAlarmWord1 AND 16#FFFFBFFF;
END_IF;

(* 10. TMR Sensor Channel Discordance Diagnostics in dwAlarmWord2 *)
IF bDiscrep_TT101_AB OR bDiscrep_TT101_BC OR bDiscrep_TT101_AC THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00010000; (* Bit 16: TT101 Riser Temp Discordance *)
ELSE
    dwAlarmWord2 := dwAlarmWord2 AND 16#FFFEFFFF;
END_IF;

IF bDiscrep_TT201_AB OR bDiscrep_TT201_BC OR bDiscrep_TT201_AC THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00020000; (* Bit 17: TT201 Regen Bed Temp Discordance *)
ELSE
    dwAlarmWord2 := dwAlarmWord2 AND 16#FFFDFFFF;
END_IF;

IF bDiscrep_PDT301_AB OR bDiscrep_PDT301_BC OR bDiscrep_PDT301_AC THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00040000; (* Bit 18: PDT301 Spent Slide Valve DP Discordance *)
ELSE
    dwAlarmWord2 := dwAlarmWord2 AND 16#FFFBFFFF;
END_IF;

IF bDiscrep_PDT401_AB OR bDiscrep_PDT401_BC OR bDiscrep_PDT401_AC THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00080000; (* Bit 19: PDT401 Regen Slide Valve DP Discordance *)
ELSE
    dwAlarmWord2 := dwAlarmWord2 AND 16#FFF7FFFF;
END_IF;

IF bDiscrep_AT501_AB OR bDiscrep_AT501_BC OR bDiscrep_AT501_AC THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00100000; (* Bit 20: AT501 Flue Gas O2 Analyzer Discordance *)
ELSE
    dwAlarmWord2 := dwAlarmWord2 AND 16#FFEFFFFF;
END_IF;

(* Reset Master Safety Alarm Latch on Operator Request *)
IF bAlarmReset AND NOT bEmergencyStop AND NOT bAirBlowerTripFeedback AND bSlideValveHydraulicOk THEN
    IF (rVoted_SCSV_dP_kPa >= 35.0) AND (rVoted_RCSV_dP_kPa >= 35.0) THEN
        dwAlarmWord1 := 16#00000000;
        dwFirstOutWord := 16#00000000;
        bEmergencyTripActive := FALSE;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
   6.2 Bit-Packed Telemetry Words (ISA-18.2 / IEC 61131-3 Compliant)
   --------------------------------------------------------------------------------------------------------------------- *)
(* Status Word 1: Operational Modes, States & Interlocks *)
dwStatusWord1 := 16#00000000;
IF bSystemEnable            THEN dwStatusWord1 := dwStatusWord1 OR 16#00000001; END_IF; (* Bit 0 *)
IF bProductionActive        THEN dwStatusWord1 := dwStatusWord1 OR 16#00000002; END_IF; (* Bit 1 *)
IF bSystemReady             THEN dwStatusWord1 := dwStatusWord1 OR 16#00000004; END_IF; (* Bit 2 *)
IF bEmergencyTripActive     THEN dwStatusWord1 := dwStatusWord1 OR 16#00000008; END_IF; (* Bit 3 *)
IF bAntiReversalLockActive  THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF; (* Bit 4 *)
IF bAfterburnQuenchActive   THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF; (* Bit 5 *)
IF bBlowerSurgeAlert        THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF; (* Bit 6 *)
IF bTorchOilActive          THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF; (* Bit 7 *)

(* Pack FSM State Code [0..13] into Bits 8..11 *)
dwStatusWord1 := dwStatusWord1 OR SHL(INT_TO_DWORD(eState AND 16#0F), 8);

IF bAutoModeRequest         THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF; (* Bit 12 *)
IF bFeedCutPermissive       THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF; (* Bit 13 *)
IF bSlideValveHydraulicOk   THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF; (* Bit 14 *)
IF bStateStepPermissive     THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF; (* Bit 15 *)

IF bChannelFault_TT101A OR bChannelFault_TT101B OR bChannelFault_TT101C THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00010000; (* Bit 16: TT101 Channel Faulted *)
END_IF;
IF bChannelFault_TT201A OR bChannelFault_TT201B OR bChannelFault_TT201C THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00020000; (* Bit 17: TT201 Channel Faulted *)
END_IF;
IF bChannelFault_PDT301A OR bChannelFault_PDT301B OR bChannelFault_PDT301C THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00040000; (* Bit 18: PDT301 Channel Faulted *)
END_IF;
IF bChannelFault_PDT401A OR bChannelFault_PDT401B OR bChannelFault_PDT401C THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00080000; (* Bit 19: PDT401 Channel Faulted *)
END_IF;
IF bChannelFault_AT501A OR bChannelFault_AT501B OR bChannelFault_AT501C THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00100000; (* Bit 20: AT501 Channel Faulted *)
END_IF;

(* Status Word 2: Cyber-Physical Observer Convergence & Subsystem Health *)
dwStatusWord2 := 16#00000000;
(* Observer State Estimation Convergence Healthy *)
IF (ABS(y_innov[1]) < 6.5) AND (ABS(y_innov[4]) < 4.5) AND (ABS(y_innov[5]) < 4.5) THEN
    dwStatusWord2 := dwStatusWord2 OR 16#00000001; (* Bit 0 *)
END_IF;
(* Receding Horizon MPC Optimization Convergence *)
IF rMPC_OptimizationError < 15.0 THEN
    dwStatusWord2 := dwStatusWord2 OR 16#00000002; (* Bit 1 *)
END_IF;
(* Slide Valve Operating Differential Pressure Margin Healthy (> 5 kPa above 35 kPa) *)
IF rSlideValveMinMargin_kPa >= 5.0 THEN
    dwStatusWord2 := dwStatusWord2 OR 16#00000004; (* Bit 2 *)
END_IF;
(* Regenerator Dense Bed Level Adequate for Catalyst Circulation *)
IF (rLT_REGEN_STAGE1_m >= 3.0) AND (rLT_REGEN_STAGE2_m >= 2.5) THEN
    dwStatusWord2 := dwStatusWord2 OR 16#00000008; (* Bit 3 *)
END_IF;
(* Spent Catalyst Stripper Bed Level Equilibrium *)
IF (rLT_STRIPPER_BED_m >= 3.0) AND (rLT_STRIPPER_BED_m <= 7.0) THEN
    dwStatusWord2 := dwStatusWord2 OR 16#00000010; (* Bit 4 *)
END_IF;
(* Catalyst-to-Oil Ratio Operating in Optimal Range (5.5 - 9.5 wt/wt) *)
IF (rCatalystToOilRatio_wt >= 5.5) AND (rCatalystToOilRatio_wt <= 9.5) THEN
    dwStatusWord2 := dwStatusWord2 OR 16#00000020; (* Bit 5 *)
END_IF;
(* Flue Gas CO within Industrial Refining Environmental Limit (< 400 ppmv) *)
IF rObs_CO_ppmv <= 400.0 THEN
    dwStatusWord2 := dwStatusWord2 OR 16#00000040; (* Bit 6 *)
END_IF;
(* Combustion Air Blower Operating Safely Outside Surge Envelope *)
IF NOT bBlowerSurgeAlert THEN
    dwStatusWord2 := dwStatusWord2 OR 16#00000080; (* Bit 7 *)
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
   6.3 Function Block Execution Statistics & Output Assignment Finalization
   --------------------------------------------------------------------------------------------------------------------- *)
nOperationalState := eState;
nScanCount        := nScanCount + 1;

END_FUNCTION_BLOCK
""")
    return "\n".join(lines)
