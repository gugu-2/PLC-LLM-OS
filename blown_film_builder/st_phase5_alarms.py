# blown_film_builder/st_phase5_alarms.py

def get_phase5_alarms():
    return """(* ==================================================================================================== *)
(* PHASE 5: COORDINATED ACTUATOR COMMAND DISPATCH & 7-LAYER EXTRUDER SPEED BALANCING                   *)
(* Mass Throughput Hydraulics, Layer Ratios, IBC Fan Inverters & Oscillating Haul-Off Nip Drives        *)
(* ==================================================================================================== *)

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 5A: Line Mass Throughput & 7-Layer Co-Extrusion Layer Ratio Command Synthesis              *)
    (* Polymer mass flow Q = rho * 2 * W_layflat * H_thickness * V_line                                 *)
    (* ------------------------------------------------------------------------------------------------ *)
    IF vecU[5] > 5.0 THEN
        (* Continuous Line Total Polymer Mass Rate [kg/h] *)
        rTotalMassThroughput_kgh := (rPolymerDensity_Average_kg_m3 *
                                     (2.0 * rRecipe_LayFlatWidth_mm * 0.001) *
                                     (rRecipe_TargetThickness_um * 0.000001) *
                                     (vecU[5] * 60.0));
    ELSE
        rTotalMassThroughput_kgh := 45.0; (* Minimum Purge Circulation Throughput *)
    END_IF;

    (* Distribute Mass Throughputs to Individual Extruders According to Recipe Layer Percentages *)
    rExtruder_Throughput_A_kgh := rTotalMassThroughput_kgh * (rRecipe_ExtruderRatio_A_pct / 100.0);
    rExtruder_Throughput_B_kgh := rTotalMassThroughput_kgh * (rRecipe_ExtruderRatio_B_pct / 100.0);
    rExtruder_Throughput_C_kgh := rTotalMassThroughput_kgh * (rRecipe_ExtruderRatio_C_pct / 100.0);
    rExtruder_Throughput_D_kgh := rTotalMassThroughput_kgh * (rRecipe_ExtruderRatio_D_pct / 100.0);
    rExtruder_Throughput_E_kgh := rTotalMassThroughput_kgh * (rRecipe_ExtruderRatio_E_pct / 100.0);
    rExtruder_Throughput_F_kgh := rTotalMassThroughput_kgh * (rRecipe_ExtruderRatio_F_pct / 100.0);
    rExtruder_Throughput_G_kgh := rTotalMassThroughput_kgh * (rRecipe_ExtruderRatio_G_pct / 100.0);

    (* Synthesize Screw Speed References [RPM] Incorporating Master MPC Extrusion Trim vecU[4] *)
    IF (eState_Current >= 2) AND (eState_Current <= 11) THEN
        rExtruder_SpeedCmd_A_RPM := LIMIT(0.0, (rExtruder_Throughput_A_kgh / rExtruder_SpecYield_A_kgh_RPM) * (vecU[4] / 68.0), 115.0);
        rExtruder_SpeedCmd_B_RPM := LIMIT(0.0, (rExtruder_Throughput_B_kgh / rExtruder_SpecYield_B_kgh_RPM) * (vecU[4] / 68.0), 115.0);
        rExtruder_SpeedCmd_C_RPM := LIMIT(0.0, (rExtruder_Throughput_C_kgh / rExtruder_SpecYield_C_kgh_RPM) * (vecU[4] / 68.0), 115.0);
        rExtruder_SpeedCmd_D_RPM := LIMIT(0.0, (rExtruder_Throughput_D_kgh / rExtruder_SpecYield_D_kgh_RPM) * (vecU[4] / 68.0), 115.0);
        rExtruder_SpeedCmd_E_RPM := LIMIT(0.0, (rExtruder_Throughput_E_kgh / rExtruder_SpecYield_E_kgh_RPM) * (vecU[4] / 68.0), 115.0);
        rExtruder_SpeedCmd_F_RPM := LIMIT(0.0, (rExtruder_Throughput_F_kgh / rExtruder_SpecYield_F_kgh_RPM) * (vecU[4] / 68.0), 115.0);
        rExtruder_SpeedCmd_G_RPM := LIMIT(0.0, (rExtruder_Throughput_G_kgh / rExtruder_SpecYield_G_kgh_RPM) * (vecU[4] / 68.0), 115.0);
    ELSE
        rExtruder_SpeedCmd_A_RPM := 0.0;
        rExtruder_SpeedCmd_B_RPM := 0.0;
        rExtruder_SpeedCmd_C_RPM := 0.0;
        rExtruder_SpeedCmd_D_RPM := 0.0;
        rExtruder_SpeedCmd_E_RPM := 0.0;
        rExtruder_SpeedCmd_F_RPM := 0.0;
        rExtruder_SpeedCmd_G_RPM := 0.0;
    END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 5B: Commit Inverter Commands for Blowers, Valves & Haul-Off Line Drive                     *)
    (* ------------------------------------------------------------------------------------------------ *)
    rIBC_SupplyBlower_Speed_RPM  := vecU[1];
    rIBC_ExhaustBlower_Speed_RPM := vecU[2];
    rAirRing_BlowerFlowValve_pct := vecU[3];
    rHaulOff_LineSpeed_Cmd_mpm   := vecU[5];

    (* Secondary Lip Chilled Air Modulation Valve (Closed Loop on Supply Temp 10.0 [deg C]) *)
    rAirRing_ChillerTrimValve_pct := LIMIT(10.0, 50.0 + ((rAirRing_SecondaryChilledAirTemp_degC - 10.0) * 4.2), 98.0);

    (* Web Tension Dynamic Nip Closed-Loop Pneumatic Trim *)
    rHaulOff_NipTensionTrim_N := vecX_hat[5] * 0.420;

(* ==================================================================================================== *)
(* PHASE 6: ISA-18.2 MULTI-TIER PROCESS ALARMS, DIAGNOSTICS & 32-BIT BIT-PACKED TELEMETRY                *)
(* High-High, High, Low, Low-Low Trip Engine with Clearance Hysteresis Deadbands & First-Out Latching    *)
(* ==================================================================================================== *)

    (* ------------------------------------------------------------------------------------------------ *)
    (* Alarm Evaluator 1: Circumferential Film Thickness 2-Sigma Gauge Variation [%]                   *)
    (* ------------------------------------------------------------------------------------------------ *)
    IF rProfile_2SigmaThickness_pct >= rTrip_Thickness2Sigma_HH_pct THEN
        dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0001; (* Bit 0: Thickness 2-Sigma High-High Trip *)
    ELSIF rProfile_2SigmaThickness_pct < (rTrip_Thickness2Sigma_HH_pct - rDeadband_Thickness2Sigma_pct) THEN
        dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_0001;
    END_IF;

    IF rProfile_2SigmaThickness_pct >= rTrip_Thickness2Sigma_H_pct THEN
        dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0002; (* Bit 1: Thickness 2-Sigma High Warning *)
    ELSIF rProfile_2SigmaThickness_pct < (rTrip_Thickness2Sigma_H_pct - rDeadband_Thickness2Sigma_pct) THEN
        dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_0002;
    END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Alarm Evaluator 2: IBC Internal Bubble Diameter Transducer [mm]                                 *)
    (* ------------------------------------------------------------------------------------------------ *)
    IF rIBC_Diameter_Voted >= rTrip_Diameter_HH_mm THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0200; (* Bit 9: Diameter High-High Cage Crash Trip *)
        IF dwFirstOutWord = 16#0000_0000 THEN
            dwFirstOutWord := 16#0000_0200;
        END_IF;
    ELSIF rIBC_Diameter_Voted < (rTrip_Diameter_HH_mm - rDeadband_Diameter_mm) THEN
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_0200;
    END_IF;

    IF rIBC_Diameter_Voted >= rTrip_Diameter_H_mm THEN
        dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0004; (* Bit 2: Diameter High Lay-Flat Warning *)
    ELSIF rIBC_Diameter_Voted < (rTrip_Diameter_H_mm - rDeadband_Diameter_mm) THEN
        dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_0004;
    END_IF;

    IF rIBC_Diameter_Voted <= rTrip_Diameter_L_mm THEN
        dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0008; (* Bit 3: Diameter Low Lay-Flat Warning *)
    ELSIF rIBC_Diameter_Voted > (rTrip_Diameter_L_mm + rDeadband_Diameter_mm) THEN
        dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_0008;
    END_IF;

    IF rIBC_Diameter_Voted <= rTrip_Diameter_LL_mm THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0400; (* Bit 10: Diameter Low-Low Deflation Trip *)
        IF dwFirstOutWord = 16#0000_0000 THEN
            dwFirstOutWord := 16#0000_0400;
        END_IF;
    ELSIF rIBC_Diameter_Voted > (rTrip_Diameter_LL_mm + rDeadband_Diameter_mm) THEN
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_0400;
    END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Alarm Evaluator 3: Co-Extrusion Die Exit Total Melt Pressure [bar]                              *)
    (* ------------------------------------------------------------------------------------------------ *)
    IF rMeltPress_Die_Voted >= rTrip_MeltPress_HH_bar THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0020; (* Bit 5: Die Pressure HH Burst Disc Safety Trip *)
        IF dwFirstOutWord = 16#0000_0000 THEN
            dwFirstOutWord := 16#0000_0020;
        END_IF;
    ELSIF rMeltPress_Die_Voted < (rTrip_MeltPress_HH_bar - rDeadband_MeltPress_bar) THEN
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_0020;
    END_IF;

    IF rMeltPress_Die_Voted >= rTrip_MeltPress_H_bar THEN
        dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0010; (* Bit 4: Die Pressure High Screen Blinding Warning *)
    ELSIF rMeltPress_Die_Voted < (rTrip_MeltPress_H_bar - rDeadband_MeltPress_bar) THEN
        dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_0010;
    END_IF;

    IF (rMeltPress_Die_Voted <= rTrip_MeltPress_L_bar) AND (eState_Current >= 3) THEN
        dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0020; (* Bit 5: Die Pressure Low Starvation Warning *)
    ELSIF rMeltPress_Die_Voted > (rTrip_MeltPress_L_bar + rDeadband_MeltPress_bar) THEN
        dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_0020;
    END_IF;

    IF (rMeltPress_Die_Voted <= rTrip_MeltPress_LL_bar) AND (eState_Current >= 3) THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0100; (* Bit 8: Die Pressure Low-Low Melt Disconnect Trip *)
        IF dwFirstOutWord = 16#0000_0000 THEN
            dwFirstOutWord := 16#0000_0100;
        END_IF;
    ELSIF rMeltPress_Die_Voted > (rTrip_MeltPress_LL_bar + rDeadband_MeltPress_bar) THEN
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_0100;
    END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Alarm Evaluator 4: Frost-Line Solidification Height (FLH) [mm]                                   *)
    (* ------------------------------------------------------------------------------------------------ *)
    IF rFLH_Height_Voted >= rTrip_FLH_HH_mm THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#0000_2000; (* Bit 13: FLH High-High Stalk Instability Trip *)
        IF dwFirstOutWord = 16#0000_0000 THEN
            dwFirstOutWord := 16#0000_2000;
        END_IF;
    ELSIF rFLH_Height_Voted < (rTrip_FLH_HH_mm - rDeadband_FLH_mm) THEN
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_2000;
    END_IF;

    IF rFLH_Height_Voted >= rTrip_FLH_H_mm THEN
        dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0040; (* Bit 6: FLH High Insufficient Chilling Warning *)
    ELSIF rFLH_Height_Voted < (rTrip_FLH_H_mm - rDeadband_FLH_mm) THEN
        dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_0040;
    END_IF;

    IF rFLH_Height_Voted <= rTrip_FLH_L_mm THEN
        dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0080; (* Bit 7: FLH Low Premature Freezing Warning *)
    ELSIF rFLH_Height_Voted > (rTrip_FLH_L_mm + rDeadband_FLH_mm) THEN
        dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_0080;
    END_IF;

    IF (rFLH_Height_Voted <= rTrip_FLH_LL_mm) AND (eState_Current >= 3) THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#0000_4000; (* Bit 14: FLH Low-Low Die Freeze-Off Trip *)
        IF dwFirstOutWord = 16#0000_0000 THEN
            dwFirstOutWord := 16#0000_4000;
        END_IF;
    ELSIF rFLH_Height_Voted > (rTrip_FLH_LL_mm + rDeadband_FLH_mm) THEN
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_4000;
    END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Alarm Evaluator 5: Oscillating Haul-Off Web Tension [N]                                          *)
    (* ------------------------------------------------------------------------------------------------ *)
    IF rWebTension_HaulOff_Voted >= rTrip_WebTension_HH_N THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0080; (* Bit 7: Web Tension High-High Tear Trip *)
        IF dwFirstOutWord = 16#0000_0000 THEN
            dwFirstOutWord := 16#0000_0080;
        END_IF;
    ELSIF rWebTension_HaulOff_Voted < (rTrip_WebTension_HH_N - rDeadband_WebTension_N) THEN
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_0080;
    END_IF;

    IF rWebTension_HaulOff_Voted >= rTrip_WebTension_H_N THEN
        dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0100; (* Bit 8: Web Tension High Warning *)
    ELSIF rWebTension_HaulOff_Voted < (rTrip_WebTension_H_N - rDeadband_WebTension_N) THEN
        dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_0100;
    END_IF;

    IF (rWebTension_HaulOff_Voted <= rTrip_WebTension_L_N) AND (eState_Current >= 3) THEN
        dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0200; (* Bit 9: Web Tension Low Slack Warning *)
    ELSIF rWebTension_HaulOff_Voted > (rTrip_WebTension_L_N + rDeadband_WebTension_N) THEN
        dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_0200;
    END_IF;

    IF (rWebTension_HaulOff_Voted <= rTrip_WebTension_LL_N) AND (eState_Current >= 3) THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0040; (* Bit 6: Web Tension Low-Low Web Severance Trip *)
        IF dwFirstOutWord = 16#0000_0000 THEN
            dwFirstOutWord := 16#0000_0040;
        END_IF;
    ELSIF rWebTension_HaulOff_Voted > (rTrip_WebTension_LL_N + rDeadband_WebTension_N) THEN
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_0040;
    END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Alarm Evaluator 6: Co-Extrusion Melt Temperatures [deg C]                                        *)
    (* ------------------------------------------------------------------------------------------------ *)
    IF rBulkMeltTemp_Raw >= rTrip_MeltTemp_HH_degC THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#0000_1000; (* Bit 12: Melt Temp HH EVOH/PA Degradation Trip *)
        IF dwFirstOutWord = 16#0000_0000 THEN
            dwFirstOutWord := 16#0000_1000;
        END_IF;
    ELSIF rBulkMeltTemp_Raw < (rTrip_MeltTemp_HH_degC - rDeadband_MeltTemp_degC) THEN
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_1000;
    END_IF;

    IF rBulkMeltTemp_Raw >= rTrip_MeltTemp_H_degC THEN
        dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0400; (* Bit 10: Melt Temp High Warning *)
    ELSIF rBulkMeltTemp_Raw < (rTrip_MeltTemp_H_degC - rDeadband_MeltTemp_degC) THEN
        dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_0400;
    END_IF;

    IF rBulkMeltTemp_Raw <= rTrip_MeltTemp_L_degC THEN
        dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0800; (* Bit 11: Melt Temp Low Unmelted Gels Warning *)
    ELSIF rBulkMeltTemp_Raw > (rTrip_MeltTemp_L_degC + rDeadband_MeltTemp_degC) THEN
        dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_0800;
    END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Alarm Evaluator 7: IBC Internal Differential Air Pressure [Pa]                                  *)
    (* ------------------------------------------------------------------------------------------------ *)
    IF rIBC_DiffPressure_Sensor_Pa >= rTrip_IBC_DiffPress_HH_Pa THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0800; (* Bit 11: IBC Diff Pressure HH Rupture Trip *)
        IF dwFirstOutWord = 16#0000_0000 THEN
            dwFirstOutWord := 16#0000_0800;
        END_IF;
    ELSIF rIBC_DiffPressure_Sensor_Pa < (rTrip_IBC_DiffPress_HH_Pa - rDeadband_IBC_DiffPress_Pa) THEN
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_0800;
    END_IF;

    IF rIBC_DiffPressure_Sensor_Pa >= rTrip_IBC_DiffPress_H_Pa THEN
        dwAlarmWord2 := dwAlarmWord2 OR 16#0000_1000; (* Bit 12: IBC Diff Pressure High Flutter Warning *)
    ELSIF rIBC_DiffPressure_Sensor_Pa < (rTrip_IBC_DiffPress_H_Pa - rDeadband_IBC_DiffPress_Pa) THEN
        dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_1000;
    END_IF;

    IF (rIBC_DiffPressure_Sensor_Pa <= rTrip_IBC_DiffPress_L_Pa) AND (eState_Current >= 4) THEN
        dwAlarmWord2 := dwAlarmWord2 OR 16#0000_2000; (* Bit 13: IBC Diff Pressure Low Exchange Warning *)
    ELSIF rIBC_DiffPressure_Sensor_Pa > (rTrip_IBC_DiffPress_L_Pa + rDeadband_IBC_DiffPress_Pa) THEN
        dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_2000;
    END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Alarm Evaluator 8: 128-Zone Thermal Expansion Bolt Continuity Diagnostics                        *)
    (* ------------------------------------------------------------------------------------------------ *)
    rTempSum := 0.0;
    FOR zIdx := 0 TO 127 DO
        IF NOT arrBoltZoneHealthy[zIdx] THEN
            rTempSum := rTempSum + 1.0;
        END_IF;
    END_FOR;

    IF rTempSum >= 8.0 THEN
        dwAlarmWord2 := dwAlarmWord2 OR 16#0000_4000; (* Bit 14: Multiple Thermal Bolt Circuit Faults *)
    ELSE
        dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_4000;
    END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Alarm Evaluator 9: TMR Sensor Redundancy Degradation & Hardware Trips                            *)
    (* ------------------------------------------------------------------------------------------------ *)
    IF bDegradedSensorMode THEN
        dwAlarmWord2 := dwAlarmWord2 OR 16#0000_8000; (* Bit 15: Degraded TMR Sensor Redundancy *)
    ELSE
        dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_8000;
    END_IF;

    IF bIBC_Trip THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0002; (* Bit 1: IBC TMR All-Sensor Trip *)
        IF dwFirstOutWord = 16#0000_0000 THEN
            dwFirstOutWord := 16#0000_0002;
        END_IF;
    ELSE
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_0002;
    END_IF;

    IF bFLH_Trip THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0004; (* Bit 2: FLH TMR All-Sensor Trip *)
        IF dwFirstOutWord = 16#0000_0000 THEN
            dwFirstOutWord := 16#0000_0004;
        END_IF;
    ELSE
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_0004;
    END_IF;

    IF bMeltPress_Trip THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0008; (* Bit 3: Melt Pressure TMR All-Sensor Trip *)
        IF dwFirstOutWord = 16#0000_0000 THEN
            dwFirstOutWord := 16#0000_0008;
        END_IF;
    ELSE
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_0008;
    END_IF;

    IF bWebTension_Trip THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0010; (* Bit 4: Web Tension TMR All-Sensor Trip *)
        IF dwFirstOutWord = 16#0000_0000 THEN
            dwFirstOutWord := 16#0000_0010;
        END_IF;
    ELSE
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_0010;
    END_IF;

    IF bEmergencyStop THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0001; (* Bit 0: Emergency Stop Hardwired Interlock Trip *)
        IF dwFirstOutWord = 16#0000_0000 THEN
            dwFirstOutWord := 16#0000_0001;
        END_IF;
    ELSE
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_0001;
    END_IF;

    IF bCriticalTrip THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#0000_8000; (* Bit 15: Critical Safety Trip Interlock Active *)
    ELSE
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_8000;
    END_IF;

    (* Clear Latched First-Out Diagnostic Word on Operator Acknowledge & Fault Removal *)
    IF bResetAlarms AND (dwAlarmWord1 = 16#0000_0000) THEN
        dwFirstOutWord := 16#0000_0000;
    END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 6B: Pack 32-Bit Telemetry Operating Status Registers                                        *)
    (* ------------------------------------------------------------------------------------------------ *)
    dwStatusWord1 := 16#0000_0000;
    IF (eState_Current >= 2) AND (eState_Current <= 11) THEN
        dwStatusWord1 := dwStatusWord1 OR 16#0000_0001; (* Bit 0: Line Running *)
    END_IF;

    IF bAutoMode THEN
        dwStatusWord1 := dwStatusWord1 OR 16#0000_0002; (* Bit 1: Multi-Variable Auto Mode *)
    END_IF;

    IF bInProduction THEN
        dwStatusWord1 := dwStatusWord1 OR 16#0000_0004; (* Bit 2: In-Spec High-Speed Production *)
    END_IF;

    IF bSystemReady THEN
        dwStatusWord1 := dwStatusWord1 OR 16#0000_0008; (* Bit 3: Interlocks Cleared & System Ready *)
    END_IF;

    IF (eState_Current >= 4) AND (eState_Current <= 11) THEN
        dwStatusWord1 := dwStatusWord1 OR 16#0000_0010; (* Bit 4: IBC Closed-Loop Diameter Control Active *)
    END_IF;

    IF (eState_Current >= 8) AND (eState_Current <= 11) THEN
        dwStatusWord1 := dwStatusWord1 OR 16#0000_0020; (* Bit 5: 128 Thermal Bolts Closed Loop Active *)
    END_IF;

    IF eState_Current >= 7 THEN
        dwStatusWord1 := dwStatusWord1 OR 16#0000_0040; (* Bit 6: Rotating Thickness Scanner Synchronized *)
    END_IF;

    IF rRecipe_LineSpeed_mpm > 10.0 THEN
        dwStatusWord1 := dwStatusWord1 OR 16#0000_0080; (* Bit 7: Reversing Haul-Off Tower Oscillating *)
    END_IF;

    (* Encode 14-Stage FSM Current State in Bits 8..15 *)
    dwStatusWord1 := dwStatusWord1 OR SHL(INT_TO_DWORD(eState_Current), 8);

    IF bDegradedSensorMode THEN
        dwStatusWord1 := dwStatusWord1 OR 16#0001_0000; (* Bit 16: TMR Degraded Sensor Operating Mode *)
    END_IF;

    IF bRecipeChangePending THEN
        dwStatusWord1 := dwStatusWord1 OR 16#0002_0000; (* Bit 17: Product Recipe Transition Pending *)
    END_IF;

    IF eState_Current = 11 THEN
        dwStatusWord1 := dwStatusWord1 OR 16#0004_0000; (* Bit 18: Bubble Breathe Instability Damping Mode *)
    END_IF;

    IF eState_Current = 13 THEN
        dwStatusWord1 := dwStatusWord1 OR 16#0008_0000; (* Bit 19: Emergency Abort Latch Active *)
    END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Assemble dwStatusWord2: 7-Layer Co-Extruder & Auxiliary Drive Operating Status                   *)
    (* ------------------------------------------------------------------------------------------------ *)
    dwStatusWord2 := 16#0000_0000;
    IF rExtruder_SpeedCmd_A_RPM > 1.0 THEN dwStatusWord2 := dwStatusWord2 OR 16#0000_0001; END_IF;
    IF rExtruder_SpeedCmd_B_RPM > 1.0 THEN dwStatusWord2 := dwStatusWord2 OR 16#0000_0002; END_IF;
    IF rExtruder_SpeedCmd_C_RPM > 1.0 THEN dwStatusWord2 := dwStatusWord2 OR 16#0000_0004; END_IF;
    IF rExtruder_SpeedCmd_D_RPM > 1.0 THEN dwStatusWord2 := dwStatusWord2 OR 16#0000_0008; END_IF;
    IF rExtruder_SpeedCmd_E_RPM > 1.0 THEN dwStatusWord2 := dwStatusWord2 OR 16#0000_0010; END_IF;
    IF rExtruder_SpeedCmd_F_RPM > 1.0 THEN dwStatusWord2 := dwStatusWord2 OR 16#0000_0020; END_IF;
    IF rExtruder_SpeedCmd_G_RPM > 1.0 THEN dwStatusWord2 := dwStatusWord2 OR 16#0000_0040; END_IF;

    IF rAirRing_ChillerTrimValve_pct > 12.0 THEN dwStatusWord2 := dwStatusWord2 OR 16#0000_0080; END_IF;
    IF rIBC_SupplyBlower_Speed_RPM > 100.0 THEN dwStatusWord2 := dwStatusWord2 OR 16#0000_0100; END_IF;
    IF rIBC_ExhaustBlower_Speed_RPM > 100.0 THEN dwStatusWord2 := dwStatusWord2 OR 16#0000_0200; END_IF;

    IF NOT bIBC_Trip THEN dwStatusWord2 := dwStatusWord2 OR 16#0000_0400; END_IF;
    IF NOT bFLH_Trip THEN dwStatusWord2 := dwStatusWord2 OR 16#0000_0800; END_IF;
    IF NOT bMeltPress_Trip THEN dwStatusWord2 := dwStatusWord2 OR 16#0000_1000; END_IF;
    IF NOT bWebTension_Trip THEN dwStatusWord2 := dwStatusWord2 OR 16#0000_2000; END_IF;

    IF (dwAlarmWord2 AND 16#0000_4000) = 16#0000_0000 THEN
        dwStatusWord2 := dwStatusWord2 OR 16#0000_4000; (* Bit 14: All 128 Thermal Bolts Healthy *)
    END_IF;

    IF bHaulOff_OscillatingDirRev THEN
        dwStatusWord2 := dwStatusWord2 OR 16#0000_8000; (* Bit 15: Haul-Off Direction Reverse (CCW) *)
    END_IF;

END_FUNCTION_BLOCK
"""
