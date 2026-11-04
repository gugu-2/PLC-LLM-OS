# parts_water_rec_7.py - PHASE 4: DETERMINISTIC 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)

def get_phase4_fsm():
    code = []
    code.append("""(* =====================================================================================================================
 * PHASE 4: DETERMINISTIC 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
 * Controls complete life-cycle orchestration across all unit operations: line purge, MABR chemostat startup,
 * UF continuous filtration and air-scour CEB sequences, RO high-pressure soft ramps with ERD synchronization,
 * continuous steady-state desalination, membrane clean-in-place, off-spec diversion, and emergency rupture lockout.
 * ===================================================================================================================== *)

(* State Scan Timing Integration *)
tFSM_StateTimer_Sec := tFSM_StateTimer_Sec + rPar_SampleTime_Sec;
tFSM_SubPhaseTimer_Sec := tFSM_SubPhaseTimer_Sec + rPar_SampleTime_Sec;
tUF_Filtration_Run_Timer_Sec := tUF_Filtration_Run_Timer_Sec + rPar_SampleTime_Sec;

(* Master Hardware Safety Trip Interlock *)
IF bCmd_Emergency_Stop OR (dwAlarmWord_Critical_Trip <> 16#0000_0000) THEN
    iFSM_State := 11; (* Direct Unconditional Transition to EMERGENCY_RUPTURE_LOCKOUT *)
    bTrip_Plant_Lockout := TRUE;
END_IF;

CASE iFSM_State OF

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 0: PLANT WETTING & LINE PURGE
     * De-aeration of headers, low-pressure wetting of hollow-fiber membranes, pipeline venting, and leak checks.
     * ----------------------------------------------------------------------------------------------------------------- *)
    0:
        iPlantFSM_State_Active := 0;
        dwStatus_Word_Plant := 16#0000_0001; (* State 0 Active Mask *)

        CASE iFSM_SubPhase OF
            0: (* Sub-Phase 0: Header Venting & Static Fill *)
                rCmd_MABR_LumenAir_Valve_Pct     := 10.0;
                rCmd_MABR_InternalRecycle_RPM    := 200.0;
                rCmd_UF_PermeateSuction_VFD_Pct  := 0.0;
                rCmd_UF_AirScour_Valve_Pct       := 0.0;
                rCmd_UF_NaOCl_Dosing_Pump_Pct    := 0.0;
                rCmd_UF_CitricAcid_Dosing_Pct    := 0.0;
                rCmd_RO_HP_FeedPump_VFD_Pct      := 0.0;
                rCmd_RO_ERD_BoosterPump_VFD_Pct  := 0.0;
                rCmd_RO_BrineReject_Throttle_Pct := 100.0; (* Fully open to prevent overpressure *)
                rCmd_RO_Antiscalant_Dosing_Pct   := 0.0;
                rCmd_Permeate_Diversion_Valve_Pct:= 100.0; (* Divert to drain/basin *)
                rCmd_UV_Reactor_Power_Pct        := 30.0;  (* Standby idle *)

                IF tFSM_SubPhaseTimer_Sec > 30.0 THEN
                    iFSM_SubPhase := 1;
                    tFSM_SubPhaseTimer_Sec := 0.0;
                END_IF;

            1: (* Sub-Phase 1: Low-Pressure Hydraulic Line Purge *)
                rCmd_MABR_InternalRecycle_RPM    := 400.0;
                rCmd_UF_PermeateSuction_VFD_Pct  := 15.0;
                rCmd_RO_BrineReject_Throttle_Pct := 90.0;

                IF (tFSM_SubPhaseTimer_Sec > 60.0) AND bCmd_Plant_Enable THEN
                    iFSM_State := 1; (* Advance to MABR Low-Flow Inoculation *)
                    iFSM_SubPhase := 0;
                    tFSM_StateTimer_Sec := 0.0;
                    tFSM_SubPhaseTimer_Sec := 0.0;
                END_IF;
        END_CASE;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 1: MABR LOW-FLOW INOCULATION & BIOFILM ACCLIMATION
     * Introduction of seeded activated sludge, bubbleless oxygen diffusion ramp, and initial biofilm attachment.
     * ----------------------------------------------------------------------------------------------------------------- *)
    1:
        iPlantFSM_State_Active := 1;
        dwStatus_Word_Plant := 16#0000_0002;

        rCmd_MABR_LumenAir_Valve_Pct     := 25.0;
        rCmd_MABR_InternalRecycle_RPM    := 650.0;
        rCmd_UF_PermeateSuction_VFD_Pct  := 20.0;
        rCmd_UF_AirScour_Valve_Pct       := 0.0;
        rCmd_UF_NaOCl_Dosing_Pump_Pct    := 0.0;
        rCmd_UF_CitricAcid_Dosing_Pct    := 0.0;
        rCmd_RO_HP_FeedPump_VFD_Pct      := 0.0;
        rCmd_RO_ERD_BoosterPump_VFD_Pct  := 0.0;
        rCmd_RO_BrineReject_Throttle_Pct := 80.0;
        rCmd_RO_Antiscalant_Dosing_Pct   := 0.0;
        rCmd_Permeate_Diversion_Valve_Pct:= 100.0;
        rCmd_UV_Reactor_Power_Pct        := 35.0;

        (* Transition Guard: Biofilm growth initiated and DO stabilized in bulk liquid *)
        IF (tFSM_StateTimer_Sec > 120.0) AND (rObs_MABR_Biofilm_Thickness_um >= 65.0) AND (rVoted_MABR_DO >= 0.10) THEN
            iFSM_State := 2; (* Advance to Continuous MABR Nitrification/Denitrification Chemostat *)
            iFSM_SubPhase := 0;
            tFSM_StateTimer_Sec := 0.0;
            tFSM_SubPhaseTimer_Sec := 0.0;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 2: CONTINUOUS MABR NITRIFICATION/DENITRIFICATION CHEMOSTAT
     * Full simultaneous nitrification/denitrification (SND) chemostat operation with active MPC lumen oxygen modulation.
     * ----------------------------------------------------------------------------------------------------------------- *)
    2:
        iPlantFSM_State_Active := 2;
        dwStatus_Word_Plant := 16#0000_0004;

        (* Modulate MABR actuators using MPC optimized outputs *)
        rCmd_MABR_LumenAir_Valve_Pct     := u_opt[1];
        rCmd_MABR_InternalRecycle_RPM    := u_opt[2];
        rCmd_UF_PermeateSuction_VFD_Pct  := 35.0;
        rCmd_UF_AirScour_Valve_Pct       := 0.0;
        rCmd_UF_NaOCl_Dosing_Pump_Pct    := 0.0;
        rCmd_UF_CitricAcid_Dosing_Pct    := 0.0;
        rCmd_RO_HP_FeedPump_VFD_Pct      := 0.0;
        rCmd_RO_ERD_BoosterPump_VFD_Pct  := 0.0;
        rCmd_RO_BrineReject_Throttle_Pct := 75.0;
        rCmd_RO_Antiscalant_Dosing_Pct   := 0.0;
        rCmd_Permeate_Diversion_Valve_Pct:= 100.0;
        rCmd_UV_Reactor_Power_Pct        := 40.0;

        (* Transition Guard: MABR effluent total nitrogen in compliance and secondary liquor stabilized *)
        IF (tFSM_StateTimer_Sec > 60.0) AND (rObs_MABR_Total_Nitrogen_mg_L < 15.0) THEN
            iFSM_State := 3; (* Advance to UF Filtration Forward Flow *)
            iFSM_SubPhase := 0;
            tFSM_StateTimer_Sec := 0.0;
            tFSM_SubPhaseTimer_Sec := 0.0;
            tUF_Filtration_Run_Timer_Sec := 0.0;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 3: UF FILTRATION FORWARD FLOW
     * Continuous submerged UF forward suction permeation with automated TMP monitoring and flux maintenance.
     * ----------------------------------------------------------------------------------------------------------------- *)
    3:
        iPlantFSM_State_Active := 3;
        dwStatus_Word_Plant := 16#0000_0008;

        rCmd_MABR_LumenAir_Valve_Pct     := u_opt[1];
        rCmd_MABR_InternalRecycle_RPM    := u_opt[2];
        rCmd_UF_PermeateSuction_VFD_Pct  := u_opt[3];
        rCmd_UF_AirScour_Valve_Pct       := 0.0;
        rCmd_UF_NaOCl_Dosing_Pump_Pct    := 0.0;
        rCmd_UF_CitricAcid_Dosing_Pct    := 0.0;
        rCmd_RO_HP_FeedPump_VFD_Pct      := 0.0;
        rCmd_RO_ERD_BoosterPump_VFD_Pct  := 0.0;
        rCmd_RO_BrineReject_Throttle_Pct := 60.0;
        rCmd_RO_Antiscalant_Dosing_Pct   := 0.0;
        rCmd_Permeate_Diversion_Valve_Pct:= 100.0;
        rCmd_UV_Reactor_Power_Pct        := 45.0;

        (* Check for Periodic Air-Scour or Backwash Triggers *)
        IF bCmd_Force_UF_Backwash OR (rVoted_UF_TMP > 0.55) OR (tUF_Filtration_Run_Timer_Sec >= tUF_Filtration_Cycle_Limit_Sec) THEN
            iFSM_State := 4; (* Transition to UF Air-Scour & Fast Water Flush *)
            iFSM_SubPhase := 0;
            tFSM_StateTimer_Sec := 0.0;
            tFSM_SubPhaseTimer_Sec := 0.0;
        ELSIF (tFSM_StateTimer_Sec > 90.0) AND (rVoted_UF_Turb < 0.10) AND (rAIT_FEED_SDI15_505 < 3.20) THEN
            iFSM_State := 6; (* Advance to RO HP Soft Ramp & ERD Synchronization *)
            iFSM_SubPhase := 0;
            tFSM_StateTimer_Sec := 0.0;
            tFSM_SubPhaseTimer_Sec := 0.0;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 4: UF AIR-SCOUR & FAST WATER FLUSH
     * Suction stopped, cyclic coarse bubble aeration scour applied to shake off foulant cake layer, followed by drain flush.
     * ----------------------------------------------------------------------------------------------------------------- *)
    4:
        iPlantFSM_State_Active := 4;
        dwStatus_Word_Plant := 16#0000_0010;

        rCmd_MABR_LumenAir_Valve_Pct     := u_opt[1];
        rCmd_MABR_InternalRecycle_RPM    := u_opt[2];
        rCmd_UF_PermeateSuction_VFD_Pct  := 0.0; (* Suction paused *)
        rCmd_UF_AirScour_Valve_Pct       := 85.0;(* High-rate coarse bubble aeration scour *)
        rCmd_UF_NaOCl_Dosing_Pump_Pct    := 0.0;
        rCmd_UF_CitricAcid_Dosing_Pct    := 0.0;
        rCmd_RO_HP_FeedPump_VFD_Pct      := 0.0;
        rCmd_RO_ERD_BoosterPump_VFD_Pct  := 0.0;
        rCmd_RO_BrineReject_Throttle_Pct := 50.0;
        rCmd_RO_Antiscalant_Dosing_Pct   := 0.0;
        rCmd_Permeate_Diversion_Valve_Pct:= 100.0;
        rCmd_UV_Reactor_Power_Pct        := 35.0;

        (* 45-Second Air Scour Relaxation Cycle *)
        IF tFSM_StateTimer_Sec > 45.0 THEN
            rUF_Cake_Resistance_Accum := rUF_Cake_Resistance_Accum * 0.45; (* 55% cake detachment credit *)
            tUF_Filtration_Run_Timer_Sec := 0.0;

            IF rVoted_UF_TMP > 0.60 THEN
                iFSM_State := 5; (* Heavy fouling remains -> Advance to Chemically Enhanced Backwash *)
            ELSE
                iFSM_State := 3; (* Return to Normal Forward Filtration *)
            END_IF;
            iFSM_SubPhase := 0;
            tFSM_StateTimer_Sec := 0.0;
            tFSM_SubPhaseTimer_Sec := 0.0;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 5: UF CHEMICALLY ENHANCED BACKWASH (CEB)
     * Reverse hydraulic pulse with NaOCl (organic foulant dissolution) and Citric Acid (inorganic scaling descaling).
     * ----------------------------------------------------------------------------------------------------------------- *)
    5:
        iPlantFSM_State_Active := 5;
        dwStatus_Word_Plant := 16#0000_0020;

        rCmd_MABR_LumenAir_Valve_Pct     := u_opt[1];
        rCmd_MABR_InternalRecycle_RPM    := u_opt[2];
        rCmd_UF_PermeateSuction_VFD_Pct  := 0.0;
        rCmd_RO_HP_FeedPump_VFD_Pct      := 0.0;
        rCmd_RO_ERD_BoosterPump_VFD_Pct  := 0.0;
        rCmd_RO_BrineReject_Throttle_Pct := 40.0;
        rCmd_RO_Antiscalant_Dosing_Pct   := 0.0;
        rCmd_Permeate_Diversion_Valve_Pct:= 100.0;
        rCmd_UV_Reactor_Power_Pct        := 30.0;

        CASE iFSM_SubPhase OF
            0: (* Chemical Injection Phase: NaOCl Hypochlorite Dosing *)
                rCmd_UF_AirScour_Valve_Pct     := 20.0;
                rCmd_UF_NaOCl_Dosing_Pump_Pct  := 65.0;
                rCmd_UF_CitricAcid_Dosing_Pct  := 0.0;

                IF tFSM_SubPhaseTimer_Sec > 30.0 THEN
                    iFSM_SubPhase := 1;
                    tFSM_SubPhaseTimer_Sec := 0.0;
                END_IF;

            1: (* Chemical Static Soak Phase *)
                rCmd_UF_AirScour_Valve_Pct     := 0.0;
                rCmd_UF_NaOCl_Dosing_Pump_Pct  := 0.0;
                rCmd_UF_CitricAcid_Dosing_Pct  := 0.0;

                IF tFSM_SubPhaseTimer_Sec > 60.0 THEN
                    iFSM_SubPhase := 2;
                    tFSM_SubPhaseTimer_Sec := 0.0;
                END_IF;

            2: (* Citric Acid Descaling Injection Phase *)
                rCmd_UF_AirScour_Valve_Pct     := 15.0;
                rCmd_UF_NaOCl_Dosing_Pump_Pct  := 0.0;
                rCmd_UF_CitricAcid_Dosing_Pct  := 55.0;

                IF tFSM_SubPhaseTimer_Sec > 30.0 THEN
                    iFSM_SubPhase := 3;
                    tFSM_SubPhaseTimer_Sec := 0.0;
                END_IF;

            3: (* Final Forward Displacement Rinse *)
                rCmd_UF_AirScour_Valve_Pct     := 50.0;
                rCmd_UF_NaOCl_Dosing_Pump_Pct  := 0.0;
                rCmd_UF_CitricAcid_Dosing_Pct  := 0.0;

                IF tFSM_SubPhaseTimer_Sec > 45.0 THEN
                    rUF_Cake_Resistance_Accum := 2.0E11; (* Clean baseline restored *)
                    tUF_Filtration_Run_Timer_Sec := 0.0;
                    iFSM_State := 3; (* Return to Forward Filtration *)
                    iFSM_SubPhase := 0;
                    tFSM_StateTimer_Sec := 0.0;
                    tFSM_SubPhaseTimer_Sec := 0.0;
                END_IF;
        END_CASE;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 6: RO HIGH-PRESSURE SOFT RAMP & ERD SYNCHRONIZATION
     * Controlled acceleration of 65-bar HP feed pump (slew <= 1.2%/s), ERD ceramic rotor spin-up, and isobaric balance.
     * ----------------------------------------------------------------------------------------------------------------- *)
    6:
        iPlantFSM_State_Active := 6;
        dwStatus_Word_Plant := 16#0000_0040;

        rCmd_MABR_LumenAir_Valve_Pct     := u_opt[1];
        rCmd_MABR_InternalRecycle_RPM    := u_opt[2];
        rCmd_UF_PermeateSuction_VFD_Pct  := u_opt[3];
        rCmd_UF_AirScour_Valve_Pct       := 0.0;
        rCmd_UF_NaOCl_Dosing_Pump_Pct    := 0.0;
        rCmd_UF_CitricAcid_Dosing_Pct    := 0.0;
        rCmd_Permeate_Diversion_Valve_Pct:= 100.0; (* Hold permeate on divert during ramp *)
        rCmd_UV_Reactor_Power_Pct        := 60.0;

        CASE iFSM_SubPhase OF
            0: (* Sub-Phase 0: Antiscalant Priming & Low-Pressure Feed Boost *)
                rCmd_RO_Antiscalant_Dosing_Pct   := 45.0;
                rCmd_RO_BrineReject_Throttle_Pct := 40.0;
                rCmd_RO_ERD_BoosterPump_VFD_Pct  := 25.0;
                rCmd_RO_HP_FeedPump_VFD_Pct      := 15.0;

                IF (tFSM_SubPhaseTimer_Sec > 20.0) AND (rST_ERD_ROTOR_RPM_504 > 250.0) THEN
                    iFSM_SubPhase := 1;
                    tFSM_SubPhaseTimer_Sec := 0.0;
                END_IF;

            1: (* Sub-Phase 1: Linear Slew Acceleration to 65 bar Operating Target *)
                rCmd_RO_Antiscalant_Dosing_Pct   := 55.0;
                rCmd_RO_BrineReject_Throttle_Pct := 28.0;
                rCmd_RO_ERD_BoosterPump_VFD_Pct  := u_opt[6];
                rCmd_RO_HP_FeedPump_VFD_Pct      := u_opt[5];

                IF (tFSM_SubPhaseTimer_Sec > 40.0) AND (rVoted_RO_HP_Feed >= 60.0) AND (rObs_ERD_Hydraulic_Recovery_Eff > 88.0) THEN
                    iFSM_State := 7; (* Advance to Steady-State RO Desalination *)
                    iFSM_SubPhase := 0;
                    tFSM_StateTimer_Sec := 0.0;
                    tFSM_SubPhaseTimer_Sec := 0.0;
                END_IF;
        END_CASE;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 7: STEADY-STATE RO DESALINATION & PERMEATE BLENDING
     * Continuous dual-stage high-recovery (85%) seawater/brackish reverse osmosis with isobaric ERD energy exchange.
     * ----------------------------------------------------------------------------------------------------------------- *)
    7:
        iPlantFSM_State_Active := 7;
        dwStatus_Word_Plant := 16#0000_0080;

        (* Modulate all unit operations under optimal closed-loop MPC control *)
        rCmd_MABR_LumenAir_Valve_Pct     := u_opt[1];
        rCmd_MABR_InternalRecycle_RPM    := u_opt[2];
        rCmd_UF_PermeateSuction_VFD_Pct  := u_opt[3];
        rCmd_UF_AirScour_Valve_Pct       := 0.0;
        rCmd_UF_NaOCl_Dosing_Pump_Pct    := 0.0;
        rCmd_UF_CitricAcid_Dosing_Pct    := 0.0;
        rCmd_RO_HP_FeedPump_VFD_Pct      := u_opt[5];
        rCmd_RO_ERD_BoosterPump_VFD_Pct  := u_opt[6];
        rCmd_RO_BrineReject_Throttle_Pct := u_opt[7];
        rCmd_RO_Antiscalant_Dosing_Pct   := u_opt[8];
        rCmd_UV_Reactor_Power_Pct        := 85.0;

        (* High-Purity Permeate Quality Interlock *)
        IF (rVoted_RO_Cond < 45.0) AND (rObs_UV_Delivered_Dose_mJ_cm2 >= rSP_UV_Dose_Target) THEN
            rCmd_Permeate_Diversion_Valve_Pct := 0.0; (* Forward to Reclamation Product Water Header *)
            bWarning_Quality_OffSpec := FALSE;
        ELSE
            rCmd_Permeate_Diversion_Valve_Pct := 100.0; (* Divert off-spec water *)
            bWarning_Quality_OffSpec := TRUE;
        END_IF;

        (* CIP and Service Request Transitions *)
        IF bCmd_Force_RO_CIP OR (tRO_CIP_Accumulated_Hours > 720.0) THEN
            iFSM_State := 8; (* Transition to Membrane Clean-in-Place *)
            iFSM_SubPhase := 0;
            tFSM_StateTimer_Sec := 0.0;
            tFSM_SubPhaseTimer_Sec := 0.0;
        ELSIF NOT bCmd_Plant_Enable THEN
            iFSM_State := 9; (* Normal Shutdown: Transition to Permeate Flush & Hold *)
            iFSM_SubPhase := 0;
            tFSM_StateTimer_Sec := 0.0;
            tFSM_SubPhaseTimer_Sec := 0.0;
        ELSIF (rVoted_RO_Cond >= 75.0) OR (rObs_UV_Delivered_Dose_mJ_cm2 < 30.0) THEN
            iFSM_State := 10; (* Water Quality Violation: Transition to Automated Diversion Hold *)
            iFSM_SubPhase := 0;
            tFSM_StateTimer_Sec := 0.0;
            tFSM_SubPhaseTimer_Sec := 0.0;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 8: MEMBRANE CLEAN-IN-PLACE (CIP) RECIRCULATION
     * High-temperature alkaline wash (organic foulants) followed by low-pH acid wash (inorganic scaling).
     * ----------------------------------------------------------------------------------------------------------------- *)
    8:
        iPlantFSM_State_Active := 8;
        dwStatus_Word_Plant := 16#0000_0100;

        rCmd_MABR_LumenAir_Valve_Pct     := 20.0;
        rCmd_MABR_InternalRecycle_RPM    := 300.0;
        rCmd_UF_PermeateSuction_VFD_Pct  := 0.0;
        rCmd_UF_AirScour_Valve_Pct       := 0.0;
        rCmd_UF_NaOCl_Dosing_Pump_Pct    := 0.0;
        rCmd_UF_CitricAcid_Dosing_Pct    := 0.0;
        rCmd_RO_HP_FeedPump_VFD_Pct      := 0.0;  (* HP Pump OFF during CIP *)
        rCmd_RO_ERD_BoosterPump_VFD_Pct  := 0.0;
        rCmd_RO_BrineReject_Throttle_Pct := 100.0;
        rCmd_RO_Antiscalant_Dosing_Pct   := 0.0;
        rCmd_Permeate_Diversion_Valve_Pct:= 100.0;
        rCmd_UV_Reactor_Power_Pct        := 30.0;

        CASE iFSM_SubPhase OF
            0: (* Permeate Displacement Pre-Rinse *)
                IF tFSM_SubPhaseTimer_Sec > 30.0 THEN
                    iFSM_SubPhase := 1;
                    tFSM_SubPhaseTimer_Sec := 0.0;
                END_IF;

            1: (* High-pH Alkaline Recirculation *)
                IF tFSM_SubPhaseTimer_Sec > 60.0 THEN
                    iFSM_SubPhase := 2;
                    tFSM_SubPhaseTimer_Sec := 0.0;
                END_IF;

            2: (* Low-pH Acid Descaling Recirculation *)
                IF tFSM_SubPhaseTimer_Sec > 60.0 THEN
                    iFSM_SubPhase := 3;
                    tFSM_SubPhaseTimer_Sec := 0.0;
                END_IF;

            3: (* Final Permeate Rinse & Neutralization *)
                IF tFSM_SubPhaseTimer_Sec > 45.0 THEN
                    tRO_CIP_Accumulated_Hours := 0.0;
                    iFSM_State := 9; (* Advance to Preservation Hold / Flush *)
                    iFSM_SubPhase := 0;
                    tFSM_StateTimer_Sec := 0.0;
                    tFSM_SubPhaseTimer_Sec := 0.0;
                END_IF;
        END_CASE;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 9: RO PERMEATE FLUSH & PRESERVATION HOLD
     * Low-pressure displacement of high-salinity brine using pure permeate to prevent osmotic shock and scaling.
     * ----------------------------------------------------------------------------------------------------------------- *)
    9:
        iPlantFSM_State_Active := 9;
        dwStatus_Word_Plant := 16#0000_0200;

        rCmd_MABR_LumenAir_Valve_Pct     := 15.0;
        rCmd_MABR_InternalRecycle_RPM    := 250.0;
        rCmd_UF_PermeateSuction_VFD_Pct  := 0.0;
        rCmd_UF_AirScour_Valve_Pct       := 0.0;
        rCmd_UF_NaOCl_Dosing_Pump_Pct    := 0.0;
        rCmd_UF_CitricAcid_Dosing_Pct    := 0.0;
        rCmd_RO_HP_FeedPump_VFD_Pct      := 0.0;
        rCmd_RO_ERD_BoosterPump_VFD_Pct  := 0.0;
        rCmd_RO_BrineReject_Throttle_Pct := 100.0;
        rCmd_RO_Antiscalant_Dosing_Pct   := 0.0;
        rCmd_Permeate_Diversion_Valve_Pct:= 100.0;
        rCmd_UV_Reactor_Power_Pct        := 30.0;

        IF (tFSM_StateTimer_Sec > 60.0) AND bCmd_Plant_Enable THEN
            iFSM_State := 0; (* Ready for Warm Restart *)
            iFSM_SubPhase := 0;
            tFSM_StateTimer_Sec := 0.0;
            tFSM_SubPhaseTimer_Sec := 0.0;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 10: EFFLUENT WATER QUALITY VIOLATION DIVERSION
     * Immediate sub-500 ms diversion of product water upon salinity breach or UV disinfection dose loss.
     * ----------------------------------------------------------------------------------------------------------------- *)
    10:
        iPlantFSM_State_Active := 10;
        dwStatus_Word_Plant := 16#0000_0400;

        rCmd_Permeate_Diversion_Valve_Pct := 100.0; (* 100% Divert Active *)
        bWarning_Quality_OffSpec := TRUE;

        (* Maintain unit trains running in recycle / throttled mode *)
        rCmd_MABR_LumenAir_Valve_Pct     := u_opt[1];
        rCmd_MABR_InternalRecycle_RPM    := u_opt[2];
        rCmd_UF_PermeateSuction_VFD_Pct  := 25.0;
        rCmd_RO_HP_FeedPump_VFD_Pct      := 45.0;
        rCmd_RO_ERD_BoosterPump_VFD_Pct  := 20.0;
        rCmd_RO_BrineReject_Throttle_Pct := 35.0;
        rCmd_RO_Antiscalant_Dosing_Pct   := 60.0;
        rCmd_UV_Reactor_Power_Pct        := 100.0; (* Boost UV lamps to maximum *)

        (* Return to production if water quality re-stabilizes *)
        IF (rVoted_RO_Cond < 40.0) AND (rObs_UV_Delivered_Dose_mJ_cm2 >= rSP_UV_Dose_Target) AND (tFSM_StateTimer_Sec > 30.0) THEN
            iFSM_State := 7; (* Return to Steady-State Desalination *)
            iFSM_SubPhase := 0;
            tFSM_StateTimer_Sec := 0.0;
            tFSM_SubPhaseTimer_Sec := 0.0;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 11: EMERGENCY HIGH-PRESSURE RUPTURE LOCKOUT
     * Immediate trip of HP feed pumps, rapid depressurization dump valve actuation, and hard plant lockout.
     * ----------------------------------------------------------------------------------------------------------------- *)
    11:
        iPlantFSM_State_Active := 11;
        dwStatus_Word_Plant := 16#0000_0800;

        (* Fail-Safe Zero-Energy State for All High-Pressure Machinery *)
        rCmd_RO_HP_FeedPump_VFD_Pct      := 0.0;
        rCmd_RO_ERD_BoosterPump_VFD_Pct  := 0.0;
        rCmd_RO_BrineReject_Throttle_Pct := 100.0; (* Immediate Depressurization *)
        rCmd_RO_Antiscalant_Dosing_Pct   := 0.0;
        rCmd_UF_PermeateSuction_VFD_Pct  := 0.0;
        rCmd_UF_AirScour_Valve_Pct       := 0.0;
        rCmd_UF_NaOCl_Dosing_Pump_Pct    := 0.0;
        rCmd_UF_CitricAcid_Dosing_Pct    := 0.0;
        rCmd_MABR_LumenAir_Valve_Pct     := 0.0;
        rCmd_MABR_InternalRecycle_RPM    := 0.0;
        rCmd_Permeate_Diversion_Valve_Pct:= 100.0;
        rCmd_UV_Reactor_Power_Pct        := 30.0;

        bTrip_Plant_Lockout := TRUE;

        (* Operator Reset Permissive Interlock *)
        IF bCmd_Reset_Alarms AND (NOT bCmd_Emergency_Stop) AND (rVoted_RO_HP_Feed < 5.0) THEN
            dwAlarmWord_Critical_Trip := 16#0000_0000;
            bTrip_Plant_Lockout := FALSE;
            iFSM_State := 0; (* Reset to Plant Wetting *)
            iFSM_SubPhase := 0;
            tFSM_StateTimer_Sec := 0.0;
            tFSM_SubPhaseTimer_Sec := 0.0;
        END_IF;

END_CASE;
\n""")
    return "".join(code)
