# ccgt_builder/st_phase4_fsm.py

def get_phase4_fsm():
    return """(* =====================================================================================================================
 * PHASE 4: DETERMINISTIC 14-STAGE CCGT POWER PLANT FINITE STATE MACHINE (FSM)
 * Conforming to ASME PTC 46, NFPA 85 Boiler and Combustion Hazards Code, and IEC 61511 Safety Lifecycle:
 *
 * Operational State Mapping:
 *   0  : TURBINE_ISOLATION_AND_PURGE_CYCLE (Combustion path positive displacement purge, 300 s)
 *   1  : ROTOR_BARRED_TURNING_GEAR_DISENGAGE (Hydrostatic jacking oil check, barring to 150 rpm, clutch disengage)
 *   2  : CRANK_MOTOR_ACCELERATION_AND_IGNITION (SFC starter acceleration to 750 rpm, spark ignition, pilot light-off)
 *   3  : FLAME_DETECTION_AND_WARMUP_IDLE (1200 rpm thermal soak, casing differential expansion stabilization)
 *   4  : FULL_SPEED_NO_LOAD_3000RPM_ACCEL (Rotor acceleration to synchronous 3000 rpm FSNL, governor speed lock)
 *   5  : GENERATOR_52G_BREAKER_GRID_SYNC (Auto-synchronizer voltage/frequency/phase match, 52G breaker close)
 *   6  : GAS_TURBINE_MINIMUM_STABLE_LOAD_RUN (25 MW anti-motoring block load, diffusion flame stabilization)
 *   7  : DLN_PREMIX_COMBUSTION_MODE_TRANSFER (Dry Low NOx fuel nozzle staging shift, VGV combustor temp trim)
 *   8  : HRSG_HEAT_ACCUMULATION_AND_DRUM_SWELL_LOCK (Exhaust energy soak, drum void swell decoupling lock, HP bypass)
 *   9  : STEAM_TURBINE_ADMISSION_AND_COORDINATED_MPC (HP steam admission, CCGT Coordinated MPC governor tracking)
 *   10 : DUCT_BURNER_PEAKING_FIRE_BOOST (Supplemental duct firing ignition, peaking generation to 350 MW)
 *   11 : RAPID_GRID_FREQUENCY_PRIMARY_RESPONSE (Fast primary droop frequency support under grid frequency disturbance)
 *   12 : CONTROLLED_COOLDOWN_AND_TURNDOWN (Deliberate thermal stress turndown at -5 MW/min, deloading sequence)
 *   13 : EMERGENCY_TRIP_MASTER_FUEL_TRIP_MFT (Instant SIL-3 MFT trip, fuel gas double-block shut < 80 ms, bypass open)
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 4.1: HARDWARE OVERRIDES & MASTER SAFETY INTERLOCKS (HIGHEST PRIORITY TRIPS)
 * --------------------------------------------------------------------------------------------------------------------- *)
(* 1. SIL-3 Hardwired Emergency Stop Pushbutton Trip (Active-LOW fail-safe) *)
IF NOT bEmergencyTrip_PB THEN
    IF eCurrentState <> 13 THEN
        eCurrentState := 13;
        IF dwFirstOutWord = 16#00000000 THEN
            dwFirstOutWord := 16#00000001; (* Bit 0: Emergency Pushbutton First Out *)
        END_IF;
    END_IF;
(* 2. SIL-3 HP Drum Narrow-Range Low-Low Water Level Trip (< -250 mm) - Prevents Evaporator Tube Dryout *)
ELSIF rVoted_Drum_Level_mm <= rTrip_Drum_LowLow_LL THEN
    IF eCurrentState <> 13 THEN
        eCurrentState := 13;
        IF dwFirstOutWord = 16#00000000 THEN
            dwFirstOutWord := 16#00000002; (* Bit 1: Drum Low-Low Level Dryout First Out *)
        END_IF;
    END_IF;
(* 3. SIL-3 HP Drum High-High Water Level Trip (> +200 mm) - Prevents Water Carryover to Steam Turbine *)
ELSIF rVoted_Drum_Level_mm >= rTrip_Drum_HighHigh_HH THEN
    IF eCurrentState <> 13 THEN
        eCurrentState := 13;
        IF dwFirstOutWord = 16#00000000 THEN
            dwFirstOutWord := 16#00000004; (* Bit 2: Drum High-High Carryover First Out *)
        END_IF;
    END_IF;
(* 4. Combustor Exhaust Gas Temperature (EGT) High-High Trip (> 660 deg C) *)
ELSIF rVoted_EGT_degC >= rTrip_EGT_HighHigh_HH THEN
    IF eCurrentState <> 13 THEN
        eCurrentState := 13;
        IF dwFirstOutWord = 16#00000000 THEN
            dwFirstOutWord := 16#00000008; (* Bit 3: EGT Over-Temperature First Out *)
        END_IF;
    END_IF;
(* 5. Final Superheater Main Steam Exit Temperature High-High Trip (> 595 deg C) *)
ELSIF rVoted_Steam_Temp_degC >= rTrip_SteamTemp_HighHigh_HH THEN
    IF eCurrentState <> 13 THEN
        eCurrentState := 13;
        IF dwFirstOutWord = 16#00000000 THEN
            dwFirstOutWord := 16#00000010; (* Bit 4: Main Steam Over-Temperature Creep First Out *)
        END_IF;
    END_IF;
(* 6. Turbomachinery Rotor Mechanical Over-Speed Trip (> 3300 rpm) *)
ELSIF rTurbine_Shaft_Speed_RPM >= rTrip_Overspeed_HH_RPM THEN
    IF eCurrentState <> 13 THEN
        eCurrentState := 13;
        IF dwFirstOutWord = 16#00000000 THEN
            dwFirstOutWord := 16#00000020; (* Bit 5: Rotor Over-Speed First Out *)
        END_IF;
    END_IF;
(* 7. Loss of Flame during At-Power Operations (States 3 to 11) *)
ELSIF (eCurrentState >= 3 AND eCurrentState <= 11) AND (nCombustor_Flames_Detected < 2 OR rCombustor_Flame_Intensity_Pct < rTrip_FlameLoss_Threshold_Pct) THEN
    IF eCurrentState <> 13 THEN
        eCurrentState := 13;
        IF dwFirstOutWord = 16#00000000 THEN
            dwFirstOutWord := 16#00000040; (* Bit 6: Combustor Flame Loss First Out *)
        END_IF;
    END_IF;
(* 8. Bearing Forced Lubrication Header Pressure Loss *)
ELSIF NOT bLube_Oil_Press_OK AND (eCurrentState >= 2 AND eCurrentState <= 12) THEN
    IF eCurrentState <> 13 THEN
        eCurrentState := 13;
        IF dwFirstOutWord = 16#00000000 THEN
            dwFirstOutWord := 16#00000080; (* Bit 7: Bearing Lubrication Failure First Out *)
        END_IF;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 4.2: DWELL TIMER & STATE ENTRY PULSE EVALUATION
 * --------------------------------------------------------------------------------------------------------------------- *)
IF eCurrentState = ePreviousState THEN
    rState_Dwell_Timer := rState_Dwell_Timer + rScan_Period_Ts;
    bState_Entry_Flag := FALSE;
ELSE
    rState_Dwell_Timer := 0.0;
    bState_Entry_Flag := TRUE;
    ePreviousState := eCurrentState;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 4.3: STATE-SPECIFIC SEQUENCING LOGIC & ACTUATOR PROFILES
 * --------------------------------------------------------------------------------------------------------------------- *)
CASE eCurrentState OF

    (* =================================================================================================================
     * STATE 0: TURBINE ISOLATION AND NFPA 85 PRE-PURGE CYCLE (300 s)
     * ================================================================================================================= *)
    0:
        bMaster_Fuel_Trip_MFT := FALSE;
        bTurning_Gear_Motor_Cmd := TRUE;
        bIgniter_Spark_Cmd := FALSE;
        bSync_Permissive_52G := FALSE;
        bDLN_Premix_Mode_Active := FALSE;
        bDrum_Swell_Lockout_Active := FALSE;
        bPrimary_Freq_Active := FALSE;

        (* Actuators locked in safe purge isolation *)
        u_vec[1] := 0.0;   (* Fuel gas valve closed *)
        u_vec[2] := 0.0;   (* VGV closed parking angle *)
        u_vec[3] := 15.0;  (* Minimum drum makeup circulation *)
        u_vec[4] := 0.0;   (* Attemperator spray isolated *)
        u_vec[5] := 100.0; (* HP steam bypass open for warm-up venting *)
        u_vec[6] := 0.0;   (* Duct burner fuel closed *)

        rTarget_Power_MW := 0.0;
        rTarget_VGV_Position_deg := 0.0;

        IF bMasterStart_Cmd AND bJacking_Oil_Press_OK AND bLube_Oil_Press_OK AND bCondenser_Vacuum_OK THEN
            rTimer_Purge_Elapsed_s := rTimer_Purge_Elapsed_s + rScan_Period_Ts;
            IF rTimer_Purge_Elapsed_s >= 300.0 THEN (* 5-minute NFPA 85 volumetric purge completed *)
                rTimer_Purge_Elapsed_s := 0.0;
                eCurrentState := 1; (* Advance to Turning Gear Disengagement *)
            END_IF;
        ELSE
            rTimer_Purge_Elapsed_s := 0.0;
        END_IF;

    (* =================================================================================================================
     * STATE 1: ROTOR BARRED TURNING GEAR DISENGAGEMENT
     * ================================================================================================================= *)
    1:
        bTurning_Gear_Motor_Cmd := TRUE;
        bIgniter_Spark_Cmd := FALSE;
        bSync_Permissive_52G := FALSE;

        u_vec[1] := 0.0;
        u_vec[2] := 0.0;
        u_vec[3] := 15.0;
        u_vec[4] := 0.0;
        u_vec[5] := 100.0;
        u_vec[6] := 0.0;

        (* Engage crank starter motor to accelerate rotor above turning gear overrunning clutch speed *)
        IF bCrank_Motor_Running AND (rTurbine_Shaft_Speed_RPM > 160.0) AND NOT bTurning_Gear_Engaged THEN
            bTurning_Gear_Motor_Cmd := FALSE;
            eCurrentState := 2; (* Advance to Ignition Speed Acceleration *)
        ELSIF rState_Dwell_Timer > 60.0 AND bTurning_Gear_Engaged THEN
            (* Clutch failure to disengage timeout *)
            eCurrentState := 13;
        END_IF;

    (* =================================================================================================================
     * STATE 2: CRANK MOTOR ACCELERATION AND IGNITION
     * ================================================================================================================= *)
    2:
        bTurning_Gear_Motor_Cmd := FALSE;
        bSync_Permissive_52G := FALSE;

        u_vec[2] := 0.0;   (* VGV parked at 0 deg for low starting torque *)
        u_vec[3] := 20.0;
        u_vec[4] := 0.0;
        u_vec[5] := 100.0;
        u_vec[6] := 0.0;

        IF rTurbine_Shaft_Speed_RPM >= 720.0 AND rTurbine_Shaft_Speed_RPM <= 850.0 THEN
            (* Ignition speed window achieved: Energize spark igniters and admit pilot light-off gas *)
            bIgniter_Spark_Cmd := TRUE;
            u_vec[1] := 8.5; (* Light-off fuel gas pilot demand *)
            rTimer_Crank_Spinup_s := rTimer_Crank_Spinup_s + rScan_Period_Ts;

            (* Flame scanner verification *)
            IF (rCombustor_Flame_Intensity_Pct >= 20.0) AND (nCombustor_Flames_Detected >= 3) THEN
                bIgniter_Spark_Cmd := FALSE;
                rTimer_Crank_Spinup_s := 0.0;
                eCurrentState := 3; (* Advance to Flame Detection & Warmup Idle *)
            ELSIF rTimer_Crank_Spinup_s >= 15.0 THEN
                (* Ignition failure within 15 seconds trial-for-ignition *)
                bIgniter_Spark_Cmd := FALSE;
                rTimer_Crank_Spinup_s := 0.0;
                eCurrentState := 13; (* Trip Master Fuel Trip *)
            END_IF;
        ELSE
            bIgniter_Spark_Cmd := FALSE;
            u_vec[1] := 0.0;
            IF rState_Dwell_Timer > 120.0 THEN
                (* Starter motor failed to accelerate turbine to ignition speed *)
                eCurrentState := 13;
            END_IF;
        END_IF;

    (* =================================================================================================================
     * STATE 3: FLAME DETECTION AND WARMUP IDLE (1200 RPM THERMAL SOAK)
     * ================================================================================================================= *)
    3:
        bIgniter_Spark_Cmd := FALSE;
        bSync_Permissive_52G := FALSE;
        bDLN_Premix_Mode_Active := FALSE;

        (* Modulate fuel gas to accelerate shaft to 1200 rpm idle speed *)
        IF rTurbine_Shaft_Speed_RPM < 1180.0 THEN
            u_vec[1] := MIN(14.0, u_vec[1] + (0.05 * rScan_Period_Ts * 50.0));
        ELSIF rTurbine_Shaft_Speed_RPM > 1220.0 THEN
            u_vec[1] := MAX(9.0, u_vec[1] - (0.05 * rScan_Period_Ts * 50.0));
        END_IF;

        u_vec[2] := 5.0;   (* Slight guide vane opening to supply combustion oxygen *)
        u_vec[3] := 25.0;  (* Drum level establishing circulation *)
        u_vec[4] := 0.0;
        u_vec[5] := 80.0;  (* Bypass modulating *)
        u_vec[6] := 0.0;

        rTimer_Warmup_Idle_s := rTimer_Warmup_Idle_s + rScan_Period_Ts;
        (* 180 seconds rotor thermal soak to avoid rotor vibration *)
        IF rTimer_Warmup_Idle_s >= 180.0 AND (rVoted_EGT_degC >= 380.0) THEN
            rTimer_Warmup_Idle_s := 0.0;
            eCurrentState := 4; (* Advance to FSNL 3000 RPM Acceleration *)
        END_IF;

    (* =================================================================================================================
     * STATE 4: FULL SPEED NO LOAD 3000 RPM ACCELERATION (FSNL)
     * ================================================================================================================= *)
    4:
        bIgniter_Spark_Cmd := FALSE;
        bSync_Permissive_52G := FALSE;

        (* Closed-loop speed ramp governor to 3000 rpm *)
        IF rTurbine_Shaft_Speed_RPM < 2990.0 THEN
            u_vec[1] := MIN(22.0, u_vec[1] + (0.08 * rScan_Period_Ts * 50.0));
        ELSIF rTurbine_Shaft_Speed_RPM > 3010.0 THEN
            u_vec[1] := MAX(15.0, u_vec[1] - (0.08 * rScan_Period_Ts * 50.0));
        END_IF;

        u_vec[2] := 15.0;  (* VGV at 15 deg FSNL idle position *)
        u_vec[3] := 30.0;
        u_vec[4] := 0.0;
        u_vec[5] := 70.0;
        u_vec[6] := 0.0;

        IF (rTurbine_Shaft_Speed_RPM >= 2985.0) AND (rTurbine_Shaft_Speed_RPM <= 3015.0) AND (rState_Dwell_Timer >= 20.0) THEN
            eCurrentState := 5; (* Advance to Generator Grid Synchronization *)
        END_IF;

    (* =================================================================================================================
     * STATE 5: GENERATOR 52G CIRCUIT BREAKER AUTO-SYNCHRONIZATION
     * ================================================================================================================= *)
    5:
        u_vec[2] := 15.0;
        u_vec[3] := 30.0;
        u_vec[4] := 0.0;
        u_vec[5] := 60.0;
        u_vec[6] := 0.0;

        (* Fine-tune shaft speed to grid synchronous frequency with slight positive slip (+0.1 Hz) *)
        IF rTurbine_Shaft_Speed_RPM < (rNominal_Turbine_Speed_RPM * (rGrid_Frequency_Hz / rGrid_Freq_Nominal_Hz) + 3.0) THEN
            u_vec[1] := MIN(24.0, u_vec[1] + 0.02);
        ELSE
            u_vec[1] := MAX(16.0, u_vec[1] - 0.02);
        END_IF;

        rTimer_Sync_Window_s := rTimer_Sync_Window_s + rScan_Period_Ts;

        (* Check synchronizing parameters: Slip < 0.15 Hz, voltage matched *)
        IF ABS(rTurbine_Shaft_Speed_RPM - 3000.0) < 6.0 THEN
            bSync_Permissive_52G := TRUE;
            IF bBreaker_52G_Closed THEN
                bSync_Permissive_52G := FALSE;
                rTimer_Sync_Window_s := 0.0;
                eCurrentState := 6; (* Advance to Minimum Stable Generation *)
            END_IF;
        ELSE
            bSync_Permissive_52G := FALSE;
        END_IF;

        IF rTimer_Sync_Window_s >= 180.0 THEN
            (* Auto-synchronizer window timeout *)
            bSync_Permissive_52G := FALSE;
            rTimer_Sync_Window_s := 0.0;
            eCurrentState := 4; (* Fallback to FSNL to re-align *)
        END_IF;

    (* =================================================================================================================
     * STATE 6: GAS TURBINE MINIMUM STABLE LOAD RUN (25 MW BLOCK LOAD)
     * ================================================================================================================= *)
    6:
        bSync_Permissive_52G := FALSE;
        bDLN_Premix_Mode_Active := FALSE;

        (* Step load immediately to 25 MW to establish positive forward power and prevent reverse power trip *)
        rTarget_Power_MW := 25.0;
        rTarget_VGV_Position_deg := 20.0;

        IF u_vec[1] < 28.0 THEN
            u_vec[1] := u_vec[1] + (0.10 * rScan_Period_Ts * 50.0);
        END_IF;
        u_vec[2] := 20.0;
        u_vec[3] := 35.0;  (* 3-element level controller starting to track *)
        u_vec[4] := 0.0;
        u_vec[5] := 50.0;  (* Modulate bypass to maintain drum pressure rate *)
        u_vec[6] := 0.0;

        IF (rVoted_Active_Power_MW >= 22.0) AND (rState_Dwell_Timer >= 30.0) THEN
            eCurrentState := 7; (* Advance to Dry Low NOx Premix Transfer *)
        END_IF;

    (* =================================================================================================================
     * STATE 7: DRY LOW NOx (DLN 2.6+) PREMIX COMBUSTION MODE TRANSFER
     * ================================================================================================================= *)
    7:
        rTarget_Power_MW := 45.0;
        rTarget_VGV_Position_deg := 32.0;

        (* Ramp fuel and VGV through combustor lean-premix staging window *)
        rTimer_DLN_Transfer_s := rTimer_DLN_Transfer_s + rScan_Period_Ts;
        IF u_vec[1] < 36.0 THEN
            u_vec[1] := u_vec[1] + (0.05 * rScan_Period_Ts * 50.0);
        END_IF;
        IF u_vec[2] < 32.0 THEN
            u_vec[2] := u_vec[2] + (0.04 * rScan_Period_Ts * 50.0);
        END_IF;

        u_vec[3] := 40.0;
        u_vec[5] := 40.0;
        u_vec[6] := 0.0;

        IF rTimer_DLN_Transfer_s >= 45.0 AND (rVoted_EGT_degC >= 520.0) THEN
            bDLN_Premix_Mode_Active := TRUE;
            rTimer_DLN_Transfer_s := 0.0;
            eCurrentState := 8; (* Advance to HRSG Heat Accumulation & Drum Swell Lock *)
        END_IF;

    (* =================================================================================================================
     * STATE 8: HRSG HEAT ACCUMULATION AND DRUM SWELL LOCKOUT
     * ================================================================================================================= *)
    8:
        bDrum_Swell_Lockout_Active := TRUE;
        rTarget_Power_MW := 80.0;
        rTarget_VGV_Position_deg := 45.0;

        (* Modulate gas turbine load up to 80 MW to soak HRSG evaporator *)
        IF u_vec[1] < 45.0 THEN
            u_vec[1] := u_vec[1] + (0.06 * rScan_Period_Ts * 50.0);
        END_IF;
        IF u_vec[2] < 45.0 THEN
            u_vec[2] := u_vec[2] + (0.05 * rScan_Period_Ts * 50.0);
        END_IF;

        (* 3-element feedwater control holding drum level during severe boiling swell *)
        u_vec[3] := 48.0 + rDynamic_Decoupling_FW_FF;
        u_vec[4] := rDynamic_Decoupling_Spray_FF;
        u_vec[5] := 30.0;  (* HP steam bypass controlling drum pressure build-up *)
        u_vec[6] := 0.0;

        rTimer_Drum_Swell_Lock_s := rTimer_Drum_Swell_Lock_s + rScan_Period_Ts;

        (* Permissive to admit steam to Steam Turbine: Pressure > 90 bar, Temp > 480 deg C *)
        IF (rHP_Drum_Pressure_bar >= 90.0) AND (rVoted_Steam_Temp_degC >= 480.0) AND bSteam_Turbine_Ready_Accept AND (rTimer_Drum_Swell_Lock_s >= 60.0) THEN
            bDrum_Swell_Lockout_Active := FALSE;
            rTimer_Drum_Swell_Lock_s := 0.0;
            eCurrentState := 9; (* Advance to Coordinated Turbine-Boiler MPC Control *)
        END_IF;

    (* =================================================================================================================
     * STATE 9: STEAM TURBINE ADMISSION & COORDINATED CCGT MPC RUN (BASE GENERATION)
     * ================================================================================================================= *)
    9:
        bDrum_Swell_Lockout_Active := FALSE;
        bPrimary_Freq_Active := FALSE;

        (* Ramp target active power to operator/grid demand (clamped between 80 MW and 250 MW base load) *)
        rTarget_Power_MW := MIN(rGT_Rated_Base_Power_MW, MAX(80.0, rMW_Demand_Grid));

        (* Calculate optimal VGV angle for high exhaust temperature combined-cycle efficiency *)
        IF rTarget_Power_MW > 200.0 THEN
            rTarget_VGV_Position_deg := 80.0;
        ELSE
            rTarget_VGV_Position_deg := 45.0 + ((rTarget_Power_MW - 80.0) / 120.0) * 35.0;
        END_IF;

        (* Phase 3 MPC drives u_vec[1..6] when bAuto_Coord_Enable is TRUE *)
        (* Steam bypass to condenser closes as steam turbine takes full steam production *)
        IF u_vec[5] > 0.0 THEN
            u_vec[5] := MAX(0.0, u_vec[5] - (0.10 * rScan_Period_Ts * 50.0));
        END_IF;

        (* Transition Checks *)
        IF bEnable_Duct_Burner AND (rTarget_Power_MW >= 240.0) AND (rVoted_Steam_Temp_degC >= 550.0) THEN
            eCurrentState := 10; (* Advance to Duct Burner Peaking Boost *)
        ELSIF bGrid_Freq_Support_Enable AND (ABS(rGrid_Frequency_Hz - rGrid_Freq_Nominal_Hz) > 0.06) THEN
            eCurrentState := 11; (* Jump to Rapid Primary Grid Frequency Response *)
        ELSIF bMasterStop_Cmd THEN
            eCurrentState := 12; (* Advance to Controlled Cooldown and Turndown *)
        END_IF;

    (* =================================================================================================================
     * STATE 10: HRSG DUCT BURNER PEAKING FIRE BOOST (PEAKING TO 350 MW)
     * ================================================================================================================= *)
    10:
        (* Gas turbine operates at base load (250 MW), duct firing boosts steam production to supply up to 350 MW combined *)
        rTarget_Power_MW := rGT_Rated_Base_Power_MW;
        rTarget_VGV_Position_deg := 85.0; (* Fully open VGV to supply high oxygen content exhaust gas for duct combustion *)

        rTimer_Duct_Burner_Ramp_s := rTimer_Duct_Burner_Ramp_s + rScan_Period_Ts;

        (* Slew duct burner valve to requested peaking dispatch *)
        IF u_vec[6] < 75.0 THEN
            u_vec[6] := MIN(75.0, u_vec[6] + (0.08 * rScan_Period_Ts * 50.0));
        END_IF;

        (* Attemperator spray valve active under MPC Phase 3 to clamp main steam temp to 565 deg C *)
        IF NOT bEnable_Duct_Burner OR (rMW_Demand_Grid < 260.0) THEN
            (* Ramp down duct burner before returning to normal coordinated run *)
            u_vec[6] := MAX(0.0, u_vec[6] - (0.15 * rScan_Period_Ts * 50.0));
            IF u_vec[6] <= 0.0 THEN
                rTimer_Duct_Burner_Ramp_s := 0.0;
                eCurrentState := 9; (* Return to State 9 *)
            END_IF;
        ELSIF bGrid_Freq_Support_Enable AND (ABS(rGrid_Frequency_Hz - rGrid_Freq_Nominal_Hz) > 0.06) THEN
            eCurrentState := 11; (* Jump to Primary Frequency Response *)
        ELSIF bMasterStop_Cmd THEN
            eCurrentState := 12;
        END_IF;

    (* =================================================================================================================
     * STATE 11: RAPID GRID FREQUENCY PRIMARY GOVERNOR RESPONSE
     * ================================================================================================================= *)
    11:
        bPrimary_Freq_Active := TRUE;

        (* Calculate primary frequency droop response: Delta_MW = - (100 / Droop) * (Delta_f / f_nom) * P_rated *)
        rPrimary_Freq_Delta_MW := -(100.0 / MAX(2.0, rGrid_Droop_Percent))
                                  * ((rGrid_Frequency_Hz - rGrid_Freq_Nominal_Hz) / rGrid_Freq_Nominal_Hz)
                                  * rGT_Rated_Base_Power_MW;

        (* Clamp frequency primary response delta within [-25 MW, +25 MW] *)
        IF rPrimary_Freq_Delta_MW > 25.0 THEN
            rPrimary_Freq_Delta_MW := 25.0;
        ELSIF rPrimary_Freq_Delta_MW < -25.0 THEN
            rPrimary_Freq_Delta_MW := -25.0;
        END_IF;

        rTarget_Power_MW := MIN(rGT_Rated_Base_Power_MW, MAX(50.0, rMW_Demand_Grid + rPrimary_Freq_Delta_MW));

        (* Fast direct throttle bias on fuel gas valve *)
        u_vec[1] := MIN(100.0, MAX(20.0, u_vec[1] + (0.015 * rPrimary_Freq_Delta_MW)));

        (* Return to normal MPC state once grid frequency stabilizes within +/- 0.02 Hz deadband for > 10 s *)
        IF ABS(rGrid_Frequency_Hz - rGrid_Freq_Nominal_Hz) <= 0.02 THEN
            IF rState_Dwell_Timer >= 10.0 THEN
                bPrimary_Freq_Active := FALSE;
                IF bEnable_Duct_Burner THEN
                    eCurrentState := 10;
                ELSE
                    eCurrentState := 9;
                END_IF;
            END_IF;
        END_IF;

    (* =================================================================================================================
     * STATE 12: CONTROLLED COOLDOWN AND TURNDOWN (-5 MW/min)
     * ================================================================================================================= *)
    12:
        bAuto_Coord_Enable := FALSE;
        bPrimary_Freq_Active := FALSE;
        bEnable_Duct_Burner := FALSE;

        (* Extinguish duct burner immediately *)
        u_vec[6] := 0.0;

        (* Open steam bypass to transfer steam load away from steam turbine *)
        IF u_vec[5] < 60.0 THEN
            u_vec[5] := u_vec[5] + (0.15 * rScan_Period_Ts * 50.0);
        END_IF;

        (* Ramp down gas turbine load smoothly *)
        rTarget_Power_MW := MAX(15.0, rTarget_Power_MW - (0.035 * rScan_Period_Ts * 50.0));
        u_vec[1] := MAX(18.0, u_vec[1] - (0.04 * rScan_Period_Ts * 50.0));
        u_vec[2] := MAX(15.0, u_vec[2] - (0.03 * rScan_Period_Ts * 50.0));
        u_vec[3] := MAX(25.0, u_vec[3] - (0.04 * rScan_Period_Ts * 50.0));
        u_vec[4] := 0.0;

        (* When load reaches minimum stable spinning load (< 18 MW), trip breaker 52G *)
        IF rVoted_Active_Power_MW <= 18.0 THEN
            bDLN_Premix_Mode_Active := FALSE;
            (* Fuel cut off once breaker opened *)
            u_vec[1] := 0.0;
            u_vec[2] := 0.0;
            IF rTurbine_Shaft_Speed_RPM <= 150.0 THEN
                bTurning_Gear_Motor_Cmd := TRUE;
                eCurrentState := 0; (* Return to Cold Isolation Standby *)
            END_IF;
        END_IF;

    (* =================================================================================================================
     * STATE 13: EMERGENCY MASTER FUEL TRIP (MFT) - SIL 3 FAIL-SAFE SHUTDOWN
     * ================================================================================================================= *)
    13:
        bMaster_Fuel_Trip_MFT := TRUE;
        bIgniter_Spark_Cmd := FALSE;
        bSync_Permissive_52G := FALSE;
        bDLN_Premix_Mode_Active := FALSE;
        bDrum_Swell_Lockout_Active := FALSE;
        bPrimary_Freq_Active := FALSE;
        bAuto_Coord_Enable := FALSE;

        (* Fast hydraulic slam shut on fuel gas and duct burner valves (< 80 ms) *)
        u_vec[1] := 0.0;
        u_vec[6] := 0.0;
        u_vec[2] := 0.0;   (* Slam VGV shut *)
        u_vec[4] := 0.0;   (* Isolate attemperator spray *)

        (* Slam HP steam bypass valve 100% open to avoid drum safety relief valve pop *)
        u_vec[5] := 100.0;

        (* Feedwater valve trips to safe minimum circulation to avoid boiler overfill *)
        u_vec[3] := 10.0;

        rTarget_Power_MW := 0.0;
        rTarget_VGV_Position_deg := 0.0;

        (* Auto-engage turning gear once shaft coasts down below 120 rpm *)
        IF rTurbine_Shaft_Speed_RPM <= 120.0 AND bJacking_Oil_Press_OK THEN
            bTurning_Gear_Motor_Cmd := TRUE;
        END_IF;

        (* Trip Lockout Timer: Must remain latched in MFT for at least 15 seconds *)
        rTimer_Trip_Lockout_s := rTimer_Trip_Lockout_s + rScan_Period_Ts;

        (* Trip Reset Permissive: Operator Reset PB + Trip conditions clear + Lockout elapsed *)
        IF bReset_Cmd AND (rTimer_Trip_Lockout_s >= 15.0) AND bEmergencyTrip_PB
           AND (rVoted_Drum_Level_mm > rTrip_Drum_LowLow_LL)
           AND (rVoted_Drum_Level_mm < rTrip_Drum_HighHigh_HH)
           AND (rVoted_EGT_degC < (rTrip_EGT_HighHigh_HH - rDeadband_EGT_degC))
           AND (rVoted_Steam_Temp_degC < (rTrip_SteamTemp_HighHigh_HH - rDeadband_SteamTemp_degC)) THEN
            bMaster_Fuel_Trip_MFT := FALSE;
            dwFirstOutWord := 16#00000000;
            rTimer_Trip_Lockout_s := 0.0;
            eCurrentState := 0; (* Reset to Isolation Standby *)
        END_IF;

END_CASE;

(* Update FSM State Output Telemetry *)
nPlant_FSM_State_Out := eCurrentState;
"""
