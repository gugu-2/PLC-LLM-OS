# gen_part7.py

part7 = """(* ==================================================================================================== *)
(* PHASE 5: ISA-18.2 MULTI-TIER PROCESS ALARMS, DIAGNOSTICS & 32-BIT BIT-PACKED TELEMETRY               *)
(* Alarms: 4-Tier Matrix (HH, H, L, LL) with Clearance Hysteresis Deadbands                              *)
(* Features: First-Out Latching Architecture, 32-Bit Packed Status, Diagnostic & Alarm Words             *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* Tier 1: Cell Differential Pressure Alarms [mbar] (Catholyte minus Anolyte)                           *)
(* HH = 6.0 mbar (Membrane Rupture), H = 3.0 mbar, L = -3.0 mbar, LL = -6.0 mbar (Reverse Pinch)       *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rPDT_Cell_DP_Voted >= rDP_HH_Limit_mbar THEN
    bAlarm_DP_HH := TRUE;
ELSIF rPDT_Cell_DP_Voted <= (rDP_HH_Limit_mbar - rDP_Deadband_mbar) THEN
    bAlarm_DP_HH := FALSE;
END_IF;

IF rPDT_Cell_DP_Voted >= rDP_H_Limit_mbar THEN
    bAlarm_DP_H := TRUE;
ELSIF rPDT_Cell_DP_Voted <= (rDP_H_Limit_mbar - rDP_Deadband_mbar) THEN
    bAlarm_DP_H := FALSE;
END_IF;

IF rPDT_Cell_DP_Voted <= rDP_L_Limit_mbar THEN
    bAlarm_DP_L := TRUE;
ELSIF rPDT_Cell_DP_Voted >= (rDP_L_Limit_mbar + rDP_Deadband_mbar) THEN
    bAlarm_DP_L := FALSE;
END_IF;

IF rPDT_Cell_DP_Voted <= rDP_LL_Limit_mbar THEN
    bAlarm_DP_LL := TRUE;
ELSIF rPDT_Cell_DP_Voted >= (rDP_LL_Limit_mbar + rDP_Deadband_mbar) THEN
    bAlarm_DP_LL := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Tier 2: Chlorine Header Pressure Alarms [bar]                                                        *)
(* HH = 0.60 bar (Overpressure Trip), H = 0.40 bar, L = 0.05 bar, LL = -0.02 bar (Vacuum Ingress Trip)  *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rPT_Cl2_Header_Voted >= rP_Cl2_HH_Limit_bar THEN
    bAlarm_P_Cl2_HH := TRUE;
ELSIF rPT_Cl2_Header_Voted <= (rP_Cl2_HH_Limit_bar - rP_Cl2_Deadband_bar) THEN
    bAlarm_P_Cl2_HH := FALSE;
END_IF;

IF rPT_Cl2_Header_Voted >= rP_Cl2_H_Limit_bar THEN
    bAlarm_P_Cl2_H := TRUE;
ELSIF rPT_Cl2_Header_Voted <= (rP_Cl2_H_Limit_bar - rP_Cl2_Deadband_bar) THEN
    bAlarm_P_Cl2_H := FALSE;
END_IF;

IF rPT_Cl2_Header_Voted <= rP_Cl2_L_Limit_bar THEN
    bAlarm_P_Cl2_L := TRUE;
ELSIF rPT_Cl2_Header_Voted >= (rP_Cl2_L_Limit_bar + rP_Cl2_Deadband_bar) THEN
    bAlarm_P_Cl2_L := FALSE;
END_IF;

IF rPT_Cl2_Header_Voted <= rP_Cl2_LL_Limit_bar THEN
    bAlarm_P_Cl2_LL := TRUE;
ELSIF rPT_Cl2_Header_Voted >= (rP_Cl2_LL_Limit_bar + rP_Cl2_Deadband_bar) THEN
    bAlarm_P_Cl2_LL := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Tier 3: Hydrogen Header Pressure Alarms [bar]                                                        *)
(* HH = 0.62 bar, H = 0.42 bar, L = 0.06 bar, LL = -0.01 bar (Air Ingress Detonation Hazard)           *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rPT_H2_Header_Voted >= rP_H2_HH_Limit_bar THEN
    bAlarm_P_H2_HH := TRUE;
ELSIF rPT_H2_Header_Voted <= (rP_H2_HH_Limit_bar - rP_H2_Deadband_bar) THEN
    bAlarm_P_H2_HH := FALSE;
END_IF;

IF rPT_H2_Header_Voted >= rP_H2_H_Limit_bar THEN
    bAlarm_P_H2_H := TRUE;
ELSIF rPT_H2_Header_Voted <= (rP_H2_H_Limit_bar - rP_H2_Deadband_bar) THEN
    bAlarm_P_H2_H := FALSE;
END_IF;

IF rPT_H2_Header_Voted <= rP_H2_L_Limit_bar THEN
    bAlarm_P_H2_L := TRUE;
ELSIF rPT_H2_Header_Voted >= (rP_H2_L_Limit_bar + rP_H2_Deadband_bar) THEN
    bAlarm_P_H2_L := FALSE;
END_IF;

IF rPT_H2_Header_Voted <= rP_H2_LL_Limit_bar THEN
    bAlarm_P_H2_LL := TRUE;
ELSIF rPT_H2_Header_Voted >= (rP_H2_LL_Limit_bar + rP_H2_Deadband_bar) THEN
    bAlarm_P_H2_LL := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Tier 4: Inline Hydrogen-in-Chlorine Gas Purity Alarms [% vol]                                        *)
(* HH = 1.20 % vol (Immediate Emergency Scrubber Trip), H = 0.60 % vol (High Advisory Warning)         *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rAT_H2_in_Cl2_Voted >= rH2_in_Cl2_HH_Limit_pct THEN
    bAlarm_H2_in_Cl2_HH := TRUE;
ELSIF rAT_H2_in_Cl2_Voted <= (rH2_in_Cl2_HH_Limit_pct - rH2_in_Cl2_Deadband_pct) THEN
    bAlarm_H2_in_Cl2_HH := FALSE;
END_IF;

IF rAT_H2_in_Cl2_Voted >= rH2_in_Cl2_H_Limit_pct THEN
    bAlarm_H2_in_Cl2_H := TRUE;
ELSIF rAT_H2_in_Cl2_Voted <= (rH2_in_Cl2_H_Limit_pct - rH2_in_Cl2_Deadband_pct) THEN
    bAlarm_H2_in_Cl2_H := FALSE;
END_IF;

IF rAT_H2_in_Cl2_Voted <= rH2_in_Cl2_L_Limit_pct THEN
    bAlarm_H2_in_Cl2_L := TRUE;
ELSIF rAT_H2_in_Cl2_Voted >= (rH2_in_Cl2_L_Limit_pct + rH2_in_Cl2_Deadband_pct) THEN
    bAlarm_H2_in_Cl2_L := FALSE;
END_IF;

IF rAT_H2_in_Cl2_Voted <= rH2_in_Cl2_LL_Limit_pct THEN
    bAlarm_H2_in_Cl2_LL := TRUE;
ELSIF rAT_H2_in_Cl2_Voted >= (rH2_in_Cl2_LL_Limit_pct + rH2_in_Cl2_Deadband_pct) THEN
    bAlarm_H2_in_Cl2_LL := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Tier 5: Anolyte Depleted Brine Concentration Alarms [g/L]                                            *)
(* LL = 175.0 g/L (Severe O2 Evolution / DSA Coating Destruction), L = 190.0 g/L, H = 225.0, HH = 240.0 *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rAT_Anolyte_NaCl_Voted >= rBrine_HH_Limit_gL THEN
    bAlarm_Brine_HH := TRUE;
ELSIF rAT_Anolyte_NaCl_Voted <= (rBrine_HH_Limit_gL - rBrine_Deadband_gL) THEN
    bAlarm_Brine_HH := FALSE;
END_IF;

IF rAT_Anolyte_NaCl_Voted >= rBrine_H_Limit_gL THEN
    bAlarm_Brine_H := TRUE;
ELSIF rAT_Anolyte_NaCl_Voted <= (rBrine_H_Limit_gL - rBrine_Deadband_gL) THEN
    bAlarm_Brine_H := FALSE;
END_IF;

IF rAT_Anolyte_NaCl_Voted <= rBrine_L_Limit_gL THEN
    bAlarm_Brine_L := TRUE;
ELSIF rAT_Anolyte_NaCl_Voted >= (rBrine_L_Limit_gL + rBrine_Deadband_gL) THEN
    bAlarm_Brine_L := FALSE;
END_IF;

IF rAT_Anolyte_NaCl_Voted <= rBrine_LL_Limit_gL THEN
    bAlarm_Brine_LL := TRUE;
ELSIF rAT_Anolyte_NaCl_Voted >= (rBrine_LL_Limit_gL + rBrine_Deadband_gL) THEN
    bAlarm_Brine_LL := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Tier 6: Catholyte Caustic Soda Concentration Alarms [wt%]                                            *)
(* HH = 36.0 wt% (Precipitation / Membrane Damage), H = 34.5 wt%, L = 31.0 wt%, LL = 28.0 wt%           *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rAT_Catholyte_NaOH_Voted >= rCaustic_HH_Limit_pct THEN
    bAlarm_Caustic_HH := TRUE;
ELSIF rAT_Catholyte_NaOH_Voted <= (rCaustic_HH_Limit_pct - rCaustic_Deadband_pct) THEN
    bAlarm_Caustic_HH := FALSE;
END_IF;

IF rAT_Catholyte_NaOH_Voted >= rCaustic_H_Limit_pct THEN
    bAlarm_Caustic_H := TRUE;
ELSIF rAT_Catholyte_NaOH_Voted <= (rCaustic_H_Limit_pct - rCaustic_Deadband_pct) THEN
    bAlarm_Caustic_H := FALSE;
END_IF;

IF rAT_Catholyte_NaOH_Voted <= rCaustic_L_Limit_pct THEN
    bAlarm_Caustic_L := TRUE;
ELSIF rAT_Catholyte_NaOH_Voted >= (rCaustic_L_Limit_pct + rCaustic_Deadband_pct) THEN
    bAlarm_Caustic_L := FALSE;
END_IF;

IF rAT_Catholyte_NaOH_Voted <= rCaustic_LL_Limit_pct THEN
    bAlarm_Caustic_LL := TRUE;
ELSIF rAT_Catholyte_NaOH_Voted >= (rCaustic_LL_Limit_pct + rCaustic_Deadband_pct) THEN
    bAlarm_Caustic_LL := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Tier 7: Electrolyzer Cell Stack Temperature Alarms [deg C]                                           *)
(* HH = 93.0 deg C (Boiling Hazard), H = 90.0 deg C, L = 80.0 deg C, LL = 70.0 deg C                   *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rCell_Temperature_degC >= rTemp_HH_Limit_degC THEN
    bAlarm_Temp_HH := TRUE;
ELSIF rCell_Temperature_degC <= (rTemp_HH_Limit_degC - rTemp_Deadband_degC) THEN
    bAlarm_Temp_HH := FALSE;
END_IF;

IF rCell_Temperature_degC >= rTemp_H_Limit_degC THEN
    bAlarm_Temp_H := TRUE;
ELSIF rCell_Temperature_degC <= (rTemp_H_Limit_degC - rTemp_Deadband_degC) THEN
    bAlarm_Temp_H := FALSE;
END_IF;

IF rCell_Temperature_degC <= rTemp_L_Limit_degC THEN
    bAlarm_Temp_L := TRUE;
ELSIF rCell_Temperature_degC >= (rTemp_L_Limit_degC + rTemp_Deadband_degC) THEN
    bAlarm_Temp_L := FALSE;
END_IF;

IF rCell_Temperature_degC <= rTemp_LL_Limit_degC THEN
    bAlarm_Temp_LL := TRUE;
ELSIF rCell_Temperature_degC >= (rTemp_LL_Limit_degC + rTemp_Deadband_degC) THEN
    bAlarm_Temp_LL := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Tier 8: Single-Cell Polarization Voltage Alarms [V]                                                  *)
(* HH = 3.55 V (Passivation / Membrane Blistering), H = 3.35 V, L = 2.85 V, LL = 2.10 V (Short Circuit) *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rCell_AverageVoltage_V >= rVolt_HH_Limit_V THEN
    bAlarm_Volt_HH := TRUE;
ELSIF rCell_AverageVoltage_V <= (rVolt_HH_Limit_V - rVolt_Deadband_V) THEN
    bAlarm_Volt_HH := FALSE;
END_IF;

IF rCell_AverageVoltage_V >= rVolt_H_Limit_V THEN
    bAlarm_Volt_H := TRUE;
ELSIF rCell_AverageVoltage_V <= (rVolt_H_Limit_V - rVolt_Deadband_V) THEN
    bAlarm_Volt_H := FALSE;
END_IF;

IF rCell_AverageVoltage_V <= rVolt_L_Limit_V THEN
    bAlarm_Volt_L := TRUE;
ELSIF rCell_AverageVoltage_V >= (rVolt_L_Limit_V + rVolt_Deadband_V) THEN
    bAlarm_Volt_L := FALSE;
END_IF;

IF rCell_AverageVoltage_V <= rVolt_LL_Limit_V THEN
    bAlarm_Volt_LL := TRUE;
ELSIF rCell_AverageVoltage_V >= (rVolt_LL_Limit_V + rVolt_Deadband_V) THEN
    bAlarm_Volt_LL := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* First-Out Latching Diagnostic Architecture                                                           *)
(* Freezes and Preserves the First Hardware Fault Triggering an Emergency Plant Trip                   *)
(* ---------------------------------------------------------------------------------------------------- *)
IF NOT bFirstOutLatched THEN
    IF bAlarm_DP_HH THEN
        dwFirstOutCapturedCode := 16#00000001; (* Code 1: Cell Differential Pressure High-High *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_DP_LL THEN
        dwFirstOutCapturedCode := 16#00000002; (* Code 2: Cell Differential Pressure Low-Low *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_P_Cl2_HH THEN
        dwFirstOutCapturedCode := 16#00000004; (* Code 4: Chlorine Header Overpressure HH *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_P_Cl2_LL THEN
        dwFirstOutCapturedCode := 16#00000008; (* Code 8: Chlorine Header Vacuum Ingress LL *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_P_H2_HH THEN
        dwFirstOutCapturedCode := 16#00000010; (* Code 16: Hydrogen Header Overpressure HH *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_P_H2_LL THEN
        dwFirstOutCapturedCode := 16#00000020; (* Code 32: Hydrogen Header Vacuum Ingress LL *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_H2_in_Cl2_HH THEN
        dwFirstOutCapturedCode := 16#00000040; (* Code 64: H2 in Cl2 Detonation Risk HH *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_Brine_LL THEN
        dwFirstOutCapturedCode := 16#00000080; (* Code 128: Brine Concentration Under-Saturation LL *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_Caustic_HH THEN
        dwFirstOutCapturedCode := 16#00000100; (* Code 256: Caustic High Precipitation HH *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_Temp_HH THEN
        dwFirstOutCapturedCode := 16#00000200; (* Code 512: Cell Temperature Boiling HH *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_Volt_HH THEN
        dwFirstOutCapturedCode := 16#00000400; (* Code 1024: Cell Voltage High Passivation HH *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_Volt_LL THEN
        dwFirstOutCapturedCode := 16#00000800; (* Code 2048: Cell Voltage Low Short Circuit LL *)
        bFirstOutLatched := TRUE;
    ELSIF bPDT_Cell_DP_Trip THEN
        dwFirstOutCapturedCode := 16#00001000; (* Code 4096: Cell DP Complete TMR Sensor Failure *)
        bFirstOutLatched := TRUE;
    ELSIF bEmergencyStop THEN
        dwFirstOutCapturedCode := 16#00010000; (* Code 65536: Master Emergency Stop Pushbutton *)
        bFirstOutLatched := TRUE;
    END_IF;
END_IF;

(* Clear First-Out Latch on Authorized Operator Reset *)
IF bFaultReset AND bAlarmAck THEN
    IF NOT bAlarm_DP_HH AND NOT bAlarm_DP_LL AND NOT bAlarm_P_Cl2_HH AND NOT bAlarm_P_Cl2_LL AND
       NOT bAlarm_P_H2_HH AND NOT bAlarm_P_H2_LL AND NOT bAlarm_H2_in_Cl2_HH AND NOT bEmergencyStop THEN
        bFirstOutLatched := FALSE;
        dwFirstOutCapturedCode := 16#00000000;
    END_IF;
END_IF;

dwFirstOutWord := dwFirstOutCapturedCode;

(* ---------------------------------------------------------------------------------------------------- *)
(* Assemble 32-Bit Bit-Packed Telemetry & Diagnostic Status Words                                       *)
(* ---------------------------------------------------------------------------------------------------- *)
(* 1. Status Word 1: Operational States, Interlocks & Actuator Discretes *)
dwStatusWord1 := 16#00000000;
dwStatusWord1 := dwStatusWord1 OR INT_TO_DWORD(eState); (* Bits 0..3: Active State *)
IF bEnable THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF; (* Bit 4: Enable *)
IF bAutoCycleStart THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF; (* Bit 5: Auto Start *)
IF bRectifierOnlineFeedback THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF; (* Bit 6: Rectifier Online *)
IF bAnolyteRecircPumpRunning THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF; (* Bit 7: Anolyte Pump *)
IF bCausticRecircPumpRunning THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF; (* Bit 8: Caustic Pump *)
IF bValve_EmergencyScrubberVent THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF; (* Bit 9: Scrubber Vent *)
IF bValve_EmergencyH2VentStack THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF; (* Bit 10: H2 Vent *)
IF bValve_N2_AnolytePurge THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF; (* Bit 11: N2 Anolyte Purge *)
IF bValve_N2_CatholytePurge THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF; (* Bit 12: N2 Catholyte Purge *)
IF bRectifier_TripInterlock THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF; (* Bit 13: Rectifier Interlock *)
IF bElectrolyzerIsolateValves THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF; (* Bit 14: Skid Isolate *)
IF bBrinePreheaterSteamValve THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF; (* Bit 15: Steam Preheater *)
IF bCausticCoolerWaterValve THEN dwStatusWord1 := dwStatusWord1 OR 16#00010000; END_IF; (* Bit 16: Caustic Cooler *)
IF bMpcManualOverride THEN dwStatusWord1 := dwStatusWord1 OR 16#00020000; END_IF; (* Bit 17: MPC Manual *)
IF bNitrogenPurgePermissive THEN dwStatusWord1 := dwStatusWord1 OR 16#00040000; END_IF; (* Bit 18: N2 Permissive *)
IF bChlorineAbsorptionReady THEN dwStatusWord1 := dwStatusWord1 OR 16#00080000; END_IF; (* Bit 19: Scrubber Ready *)
IF bHydrogenVentStackReady THEN dwStatusWord1 := dwStatusWord1 OR 16#00100000; END_IF; (* Bit 20: Flare Ready *)
IF bDeminWaterSupplyPermissive THEN dwStatusWord1 := dwStatusWord1 OR 16#00200000; END_IF; (* Bit 21: Demin Ready *)

(* 2. Status Word 2: 2oo3 TMR Sensor Health, Degraded Modes & Cyber-Physical Diagnostics *)
dwStatusWord2 := 16#00000000;
IF bPDT_Cell_DP_HealthA THEN dwStatusWord2 := dwStatusWord2 OR 16#00000001; END_IF; (* Bit 0: DP 1A Health *)
IF bPDT_Cell_DP_HealthB THEN dwStatusWord2 := dwStatusWord2 OR 16#00000002; END_IF; (* Bit 1: DP 1B Health *)
IF bPDT_Cell_DP_HealthC THEN dwStatusWord2 := dwStatusWord2 OR 16#00000004; END_IF; (* Bit 2: DP 1C Health *)
IF bPDT_Cell_DP_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000008; END_IF; (* Bit 3: DP Degraded 2oo2 *)
IF bPDT_Cell_DP_SingleFallback THEN dwStatusWord2 := dwStatusWord2 OR 16#00000010; END_IF; (* Bit 4: DP Single Fallback *)
IF bPT_Cl2_Header_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000020; END_IF; (* Bit 5: Cl2 Degraded *)
IF bPT_Cl2_Header_SingleFallback THEN dwStatusWord2 := dwStatusWord2 OR 16#00000040; END_IF; (* Bit 6: Cl2 Fallback *)
IF bPT_H2_Header_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000080; END_IF; (* Bit 7: H2 Degraded *)
IF bPT_H2_Header_SingleFallback THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF; (* Bit 8: H2 Fallback *)
IF bAT_H2_in_Cl2_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000200; END_IF; (* Bit 9: Photometer Degraded *)
IF bAT_H2_in_Cl2_SingleFallback THEN dwStatusWord2 := dwStatusWord2 OR 16#00000400; END_IF; (* Bit 10: Photometer Fallback *)
IF bAT_Anolyte_NaCl_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000800; END_IF; (* Bit 11: Brine Degraded *)
IF bAT_Catholyte_NaOH_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00001000; END_IF; (* Bit 12: Caustic Degraded *)
IF ABS(vecInnov[0]) < 1.00 AND ABS(vecInnov[1]) < 0.020 THEN dwStatusWord2 := dwStatusWord2 OR 16#00002000; END_IF; (* Bit 13: Observer Converged *)
IF rMpc_CostFunction_Val < 500.0 THEN dwStatusWord2 := dwStatusWord2 OR 16#00004000; END_IF; (* Bit 14: MPC Converged *)

(* 3. Alarm Word 1: ISA-18.2 Critical Emergency Trips & Safety Interlocks (HH/LL) *)
dwAlarmWord1 := 16#00000000;
IF bAlarm_DP_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF; (* Bit 0: DP HH Trip *)
IF bAlarm_DP_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF; (* Bit 1: DP LL Trip *)
IF bAlarm_P_Cl2_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF; (* Bit 2: Cl2 HH Trip *)
IF bAlarm_P_Cl2_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF; (* Bit 3: Cl2 LL Trip *)
IF bAlarm_P_H2_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF; (* Bit 4: H2 HH Trip *)
IF bAlarm_P_H2_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF; (* Bit 5: H2 LL Trip *)
IF bAlarm_H2_in_Cl2_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF; (* Bit 6: H2 in Cl2 HH Trip *)
IF bAlarm_Brine_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF; (* Bit 7: Brine LL Trip *)
IF bAlarm_Caustic_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; END_IF; (* Bit 8: Caustic HH Trip *)
IF bAlarm_Temp_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; END_IF; (* Bit 9: Temp HH Trip *)
IF bAlarm_Volt_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000400; END_IF; (* Bit 10: Volt HH Trip *)
IF bAlarm_Volt_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000800; END_IF; (* Bit 11: Volt LL Trip *)
IF bPDT_Cell_DP_Trip THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00001000; END_IF; (* Bit 12: DP TMR Sensor Trip *)
IF bPT_Cl2_Header_Trip THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00002000; END_IF; (* Bit 13: Cl2 TMR Sensor Trip *)
IF bPT_H2_Header_Trip THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00004000; END_IF; (* Bit 14: H2 TMR Sensor Trip *)
IF bAT_H2_in_Cl2_Trip THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00008000; END_IF; (* Bit 15: Photometer Sensor Trip *)
IF bEmergencyStop THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00010000; END_IF; (* Bit 16: E-Stop Trip *)

(* 4. Alarm Word 2: ISA-18.2 Warning Deviations & Sensor Discrepancies (H/L) *)
dwAlarmWord2 := 16#00000000;
IF bAlarm_DP_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF; (* Bit 0: DP High Warning *)
IF bAlarm_DP_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF; (* Bit 1: DP Low Warning *)
IF bAlarm_P_Cl2_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF; (* Bit 2: Cl2 High Warning *)
IF bAlarm_P_Cl2_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF; (* Bit 3: Cl2 Low Warning *)
IF bAlarm_P_H2_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF; (* Bit 4: H2 High Warning *)
IF bAlarm_P_H2_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF; (* Bit 5: H2 Low Warning *)
IF bAlarm_H2_in_Cl2_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF; (* Bit 6: H2 in Cl2 Warning *)
IF bAlarm_Brine_HH THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; END_IF; (* Bit 7: Brine High-High *)
IF bAlarm_Brine_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; END_IF; (* Bit 8: Brine High Advisory *)
IF bAlarm_Brine_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; END_IF; (* Bit 9: Brine Low Warning *)
IF bAlarm_Caustic_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000400; END_IF; (* Bit 10: Caustic High Warning *)
IF bAlarm_Caustic_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000800; END_IF; (* Bit 11: Caustic Low Warning *)
IF bAlarm_Caustic_LL THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00001000; END_IF; (* Bit 12: Caustic Low-Low *)
IF bAlarm_Temp_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00002000; END_IF; (* Bit 13: Temp High Warning *)
IF bAlarm_Temp_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00004000; END_IF; (* Bit 14: Temp Low Warning *)
IF bAlarm_Volt_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00008000; END_IF; (* Bit 15: Volt High Warning *)
IF bAlarm_Volt_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00010000; END_IF; (* Bit 16: Volt Low Advisory *)
IF rPDT_Cell_DP_Disc_AB_ms > 200.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00020000; END_IF; (* Bit 17: DP AB Discrepancy *)
IF rPDT_Cell_DP_Disc_BC_ms > 200.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00040000; END_IF; (* Bit 18: DP BC Discrepancy *)
IF rPDT_Cell_DP_Disc_CA_ms > 200.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00080000; END_IF; (* Bit 19: DP CA Discrepancy *)

(* Cyclic Execution Scan Counter Increment *)
iCycleCounter := iCycleCounter + 1;

END_FUNCTION_BLOCK
"""

with open("dataset_parts/part7_alarms.txt", "w", encoding="utf-8") as f:
    f.write(part7)

print("Part 7 written successfully.")
