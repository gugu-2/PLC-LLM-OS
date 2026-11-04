# scripts/feedmill_builder/part7_phase4_fsm.py
# -*- coding: utf-8 -*-

def get_phase4_block():
    return """(* ====================================================================================================
   PHASE 4: 12-STAGE DETERMINISTIC OPERATIONAL FINITE STATE MACHINE (FSM)
   ==================================================================================================== *)

(* State Scan Transition Bookkeeping *)
IF nFsm_CurrentState <> nFsm_PreviousState THEN
    bFsm_StateFirstScan     := TRUE;
    rFsm_StateTimeElapsed_s := 0.0;
    nFsm_PreviousState      := nFsm_CurrentState;
ELSE
    bFsm_StateFirstScan     := FALSE;
    rFsm_StateTimeElapsed_s := rFsm_StateTimeElapsed_s + 0.050;
END_IF;

(* Master Hardware Safety Permissive Evaluation *)
bFsm_InterlockTripped := NOT bEmergStop_Circuit_OK 
                      OR NOT bDieDoor_Closed_DI208 
                      OR NOT bShearPin_Intact_DI207;

(* Immediate Emergency Overload Interlock Override *)
IF bFsm_InterlockTripped AND nFsm_CurrentState <> 11 AND nFsm_CurrentState <> 0 THEN
    nFsm_CurrentState := 11; (* Direct transfer to Emergency Overload Bypass State *)
END_IF;

CASE nFsm_CurrentState OF

    (* ------------------------------------------------------------------------------------------------
       STATE 0: COLD IDLE STANDBY & HARDWARE SAFETY VERIFICATION
       ------------------------------------------------------------------------------------------------ *)
    0:
        bSysRunning            := FALSE;
        bSysFault              := FALSE;
        bEmergencyBypassActive := FALSE;
        bCmdBypassFlap_Divert  := TRUE;  (* Divert flap in safe reject position during standby *)
        
        (* Actuators Commanded to Zero / Standby *)
        u_ctrl[1] := 0.0;    (* Feeder Screw Off *)
        u_ctrl[2] := 0.0;    (* Steam Valve Closed *)
        u_ctrl[3] := 0.0;    (* Conditioner Agitator Off *)
        u_ctrl[4] := 0.0;    (* Hydraulic Gap fully retracted *)
        u_ctrl[5] := 0.0;    (* Cooler Discharge Off *)
        u_ctrl[6] := 30.0;   (* Cooler Fan Minimum *)

        bCmdCoaterVacuumPump    := FALSE;
        bCmdCoaterFatSprayValve := FALSE;
        bCmdCoaterEnzymeValve   := FALSE;
        bCmdCoaterVentValve     := TRUE;  (* Chamber at atmospheric pressure *)
        bCmdCoaterDischargeGate := FALSE;

        (* Transition to State 1 on System Start Command & Valid Safety Circuits *)
        IF bEnable AND bReset AND NOT bFsm_InterlockTripped THEN
            nFsm_ShearPinTripLatch  := FALSE;
            nFsm_DieChokeFaultLatch := FALSE;
            nFsm_CurrentState       := 1;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 1: STEAM HEADER CONDENSATE PURGE & PRESSURE EQUILIBRATION
       ------------------------------------------------------------------------------------------------ *)
    1:
        bSysRunning            := TRUE;
        bCmdBypassFlap_Divert  := TRUE;

        (* Saturated Steam Purge Action: Crack steam valve 12% to purge condensate traps *)
        u_ctrl[1] := 0.0;
        u_ctrl[2] := 12.0;   (* Condensate warm-up bleed *)
        u_ctrl[3] := 0.0;
        u_ctrl[4] := 0.0;
        u_ctrl[5] := 0.0;
        u_ctrl[6] := 30.0;

        (* Permissive Check: Steam header reaches 2.2 bar and purge duration elapsed *)
        IF rFsm_StateTimeElapsed_s >= tFsm_SteamPurgeTime_s THEN
            IF rSteamHdrPress_Supply_bar >= 2.20 THEN
                nFsm_CurrentState := 2; (* Advance to Conditioner Preheat *)
            END_IF;
        END_IF;

        IF NOT bEnable THEN nFsm_CurrentState := 10; END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 2: DUAL-SHAFT CONDITIONER CYLINDER PREHEAT
       ------------------------------------------------------------------------------------------------ *)
    2:
        bSysRunning            := TRUE;
        bCmdBypassFlap_Divert  := TRUE;

        (* Agitator starts at slow speed to distribute steam heat evenly throughout empty barrel *)
        u_ctrl[1] := 0.0;
        u_ctrl[2] := 25.0;   (* 25% Steam to warm stainless barrel jacket *)
        u_ctrl[3] := 180.0;  (* 180 RPM Agitator Speed *)
        u_ctrl[4] := 0.0;
        u_ctrl[5] := 0.0;
        u_ctrl[6] := 30.0;

        (* Advance when conditioner discharge temp rises above 65 deg C and timer elapsed *)
        IF rFsm_StateTimeElapsed_s >= tFsm_PreheatTime_s AND rVoted_CondMashTemp_degC >= 65.0 THEN
            nFsm_CurrentState := 3; (* Advance to Cooler Exhaust Fan Start *)
        END_IF;

        IF NOT bEnable THEN nFsm_CurrentState := 10; END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 3: COUNTERFLOW COOLER EXHAUST FAN START & AIRFLOW ESTABLISHMENT
       ------------------------------------------------------------------------------------------------ *)
    3:
        bSysRunning            := TRUE;
        bCmdBypassFlap_Divert  := TRUE;

        (* Start cooler exhaust centrifugal fan to establish counterflow draft *)
        u_ctrl[1] := 0.0;
        u_ctrl[2] := 15.0;   (* Maintain conditioner warmth *)
        u_ctrl[3] := 180.0;
        u_ctrl[4] := 0.0;
        u_ctrl[5] := 0.0;
        u_ctrl[6] := 65.0;   (* 65% Fan Speed *)

        IF rFsm_StateTimeElapsed_s >= 15.0 THEN
            nFsm_CurrentState := 4; (* Advance to 400 kW Pellet Mill Main Motor Start *)
        END_IF;

        IF NOT bEnable THEN nFsm_CurrentState := 10; END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 4: PELLET MILL 400 kW MAIN DRIVE STAR-DELTA / SOFT-START RAMP
       ------------------------------------------------------------------------------------------------ *)
    4:
        bSysRunning            := TRUE;
        bCmdBypassFlap_Divert  := TRUE;

        (* Position hydraulic gap rams to initial safe clearance gap (1.20 mm) *)
        u_ctrl[1] := 0.0;
        u_ctrl[2] := 15.0;
        u_ctrl[3] := 200.0;
        u_ctrl[4] := 45.0;   (* 45% hydraulic servo sets initial 1.20 mm gap *)
        u_ctrl[5] := 0.0;
        u_ctrl[6] := 65.0;

        (* Verify main motor transitions from start to idle running speed *)
        IF rFsm_StateTimeElapsed_s >= tFsm_MillStarDelta_s THEN
            (* Check idle motor current: expected between 160 A and 260 A at no load *)
            IF rVoted_PressMotorCurrent_A >= 150.0 AND rVoted_PressMotorCurrent_A <= 280.0 THEN
                nFsm_CurrentState := 5; (* Advance to Feeder Screw Ramp Initial *)
            ELSIF rFsm_StateTimeElapsed_s >= 25.0 THEN
                (* Motor failed to accelerate or belt disconnect *)
                bSysFault         := TRUE;
                nFsm_CurrentState := 11;
            END_IF;
        END_IF;

        IF NOT bEnable THEN nFsm_CurrentState := 10; END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 5: FEEDER SCREW INITIAL RAMP & DRY MEAL INTRODUCTION
       ------------------------------------------------------------------------------------------------ *)
    5:
        bSysRunning            := TRUE;
        bCmdBypassFlap_Divert  := TRUE; (* Keep reject flap OPEN to dump initial cold meal *)

        (* Feeder starts at 15% rated speed (4.5 t/h) to fill conditioner paddles *)
        u_ctrl[1] := 27.0;   (* 27 RPM = 15% of 180 RPM *)
        u_ctrl[2] := 35.0;   (* Steam increases to heat incoming meal *)
        u_ctrl[3] := 260.0;  (* 260 RPM Agitator *)
        u_ctrl[4] := 45.0;
        u_ctrl[5] := 0.0;
        u_ctrl[6] := 65.0;

        IF rFsm_StateTimeElapsed_s >= tFsm_FeederInitialRamp_s THEN
            nFsm_CurrentState := 6; (* Advance to Hydrothermal Conditioning Equilibration *)
        END_IF;

        IF NOT bEnable THEN nFsm_CurrentState := 10; END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 6: HYDROTHERMAL CONDITIONING EQUILIBRATION & GELATINIZATION RAMP
       ------------------------------------------------------------------------------------------------ *)
    6:
        bSysRunning            := TRUE;
        bCmdBypassFlap_Divert  := TRUE; (* Still diverting until pasteurization temp achieved *)

        (* Modulate steam to drive mash temperature toward 88 deg C target *)
        u_ctrl[1] := 45.0;   (* Feeder increases to 25% (7.5 t/h) *)
        IF rVoted_CondMashTemp_degC < 85.0 THEN
            u_ctrl[2] := 60.0;
        ELSE
            u_ctrl[2] := 48.0;
        END_IF;
        u_ctrl[3] := 320.0;  (* Increase paddle shear *)
        u_ctrl[4] := 45.0;
        u_ctrl[5] := 0.0;
        u_ctrl[6] := 70.0;

        (* Permissive to switch mash into die: Temp >= 85 deg C and Gelatinization >= 0.35 *)
        IF (rVoted_CondMashTemp_degC >= 85.0 AND rEst_GelatinizationIndex >= 0.35) 
            OR (rFsm_StateTimeElapsed_s >= tFsm_CondEquilibration_s AND rVoted_CondMashTemp_degC >= 80.0) THEN
            nFsm_CurrentState := 7; (* Advance to Pellet Mill Feed Introduction *)
        END_IF;

        IF NOT bEnable THEN nFsm_CurrentState := 10; END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 7: PELLET MILL FEED INTRODUCTION & HYDRAULIC ROLLER GAP ENGAGEMENT
       ------------------------------------------------------------------------------------------------ *)
    7:
        bSysRunning            := TRUE;
        bCmdBypassFlap_Divert  := FALSE; (* CLOSE REJECT FLAP: Hot mash directed into Pellet Mill Die! *)

        (* Transition hydraulic gap servo from 1.20 mm to working clearance 0.70 mm *)
        u_ctrl[1] := 65.0;   (* Feeder increases to 36% (10.8 t/h) *)
        u_ctrl[2] := 52.0;   (* Steady steam injection *)
        u_ctrl[3] := 350.0;
        u_ctrl[4] := 58.0;   (* Close gap toward 0.70 mm *)
        u_ctrl[5] := 0.0;
        u_ctrl[6] := 75.0;

        (* Check motor current response: current must rise above 350 A indicating extrusion begun *)
        IF rVoted_PressMotorCurrent_A >= 350.0 AND rFsm_StateTimeElapsed_s >= 20.0 THEN
            nFsm_CurrentState := 8; (* Advance to Full Steady-State Production Pelleting *)
        ELSIF rFsm_StateTimeElapsed_s >= 45.0 THEN
            (* Timeout with low current: feed bridge in chute *)
            bSysFault         := TRUE;
            nFsm_CurrentState := 10;
        END_IF;

        IF NOT bEnable THEN nFsm_CurrentState := 10; END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 8: FULL STEADY-STATE PRODUCTION PELLETING (RECEDING-HORIZON MPC ACTIVE)
       ------------------------------------------------------------------------------------------------ *)
    8:
        bSysRunning            := TRUE;
        bCmdBypassFlap_Divert  := FALSE;

        (* Feeder setpoint scales with operator rFeedRate_SP_tph (up to 30 t/h = 180 RPM) *)
        IF NOT bAutoMode THEN
            (* Manual Baseline Actuator Trajectory *)
            u_ctrl[1] := (rFeedRate_SP_tph / 30.0) * 180.0;
            u_ctrl[2] := 65.0;
            u_ctrl[3] := 380.0;
            u_ctrl[4] := 62.0;
        END_IF;
        (* If bAutoMode, u_ctrl is dynamically optimized via Receding-Horizon MPC in Phase 3! *)

        (* Counterflow Cooler Bed Level Regulation *)
        IF rVoted_CoolerBedLevel_mm >= 750.0 THEN
            (* Modulate reciprocating discharge grid to maintain 950 mm target bed depth *)
            u_ctrl[5] := 35.0 + ((rVoted_CoolerBedLevel_mm - 950.0) * 0.08);
            IF u_ctrl[5] > 100.0 THEN u_ctrl[5] := 100.0; END_IF;
            IF u_ctrl[5] < 10.0 THEN u_ctrl[5] := 10.0; END_IF;
        ELSE
            u_ctrl[5] := 0.0; (* Hold grid closed to build proper retention bed *)
        END_IF;
        u_ctrl[6] := 85.0; (* High cooling air draft *)

        (* Check Vacuum Coater Batch Initiation Trigger *)
        IF bCoaterCycleStartCmd AND rCoaterBatchWeight_WT401_kg >= 480.0 THEN
            nFsm_CurrentState := 9; (* Advance to Vacuum Coater Batch Execution *)
        END_IF;

        (* Controlled Normal Shutdown Transition *)
        IF NOT bEnable OR NOT bPelletMillStartCmd THEN
            nFsm_CurrentState := 10;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 9: VACUUM FAT & POST-PELLET LIQUID ENZYME BATCH COATING CYCLE
       ------------------------------------------------------------------------------------------------ *)
    9:
        bSysRunning            := TRUE;
        bCmdBypassFlap_Divert  := FALSE;
        (* Pelleting press continues running in background while coater executes cyclic batch *)

        (* Step 9.1: Evacuate Chamber to -0.85 bar (0 to 18 s) *)
        IF rFsm_StateTimeElapsed_s < 18.0 THEN
            bCmdCoaterVacuumPump    := TRUE;
            bCmdCoaterFatSprayValve := FALSE;
            bCmdCoaterEnzymeValve   := FALSE;
            bCmdCoaterVentValve     := FALSE; (* Close atmospheric vent *)
            bCmdCoaterDischargeGate := FALSE;

        (* Step 9.2: Heated Liquid Fat High-Pressure Injection Pulse (18 to 32 s) *)
        ELSIF rFsm_StateTimeElapsed_s >= 18.0 AND rFsm_StateTimeElapsed_s < 32.0 THEN
            bCmdCoaterVacuumPump    := FALSE; (* Vacuum held *)
            bCmdCoaterFatSprayValve := TRUE;  (* Atomize fat spray over tumbling pellets *)
            bCmdCoaterEnzymeValve   := FALSE;
            bCmdCoaterVentValve     := FALSE;
            bCmdCoaterDischargeGate := FALSE;

        (* Step 9.3: Liquid Micro-Enzyme Injection Spray (32 to 42 s) *)
        ELSIF rFsm_StateTimeElapsed_s >= 32.0 AND rFsm_StateTimeElapsed_s < 42.0 THEN
            bCmdCoaterVacuumPump    := FALSE;
            bCmdCoaterFatSprayValve := FALSE;
            bCmdCoaterEnzymeValve   := TRUE;  (* High-precision enzyme metering *)
            bCmdCoaterVentValve     := FALSE;
            bCmdCoaterDischargeGate := FALSE;

        (* Step 9.4: Atmospheric Break & Capillary Penetration Soak (42 to 55 s) *)
        ELSIF rFsm_StateTimeElapsed_s >= 42.0 AND rFsm_StateTimeElapsed_s < 55.0 THEN
            bCmdCoaterVacuumPump    := FALSE;
            bCmdCoaterFatSprayValve := FALSE;
            bCmdCoaterEnzymeValve   := FALSE;
            bCmdCoaterVentValve     := TRUE;  (* Open atmospheric vent: air forces fat into pellet core *)
            bCmdCoaterDischargeGate := FALSE;

        (* Step 9.5: Bottom Pneumatic Slide Gate Discharge (55 to 68 s) *)
        ELSIF rFsm_StateTimeElapsed_s >= 55.0 AND rFsm_StateTimeElapsed_s < 68.0 THEN
            bCmdCoaterVacuumPump    := FALSE;
            bCmdCoaterFatSprayValve := FALSE;
            bCmdCoaterEnzymeValve   := FALSE;
            bCmdCoaterVentValve     := TRUE;
            bCmdCoaterDischargeGate := TRUE;  (* Evacuate 500 kg batch to finished product bin *)

        (* Step 9.6: Batch Complete, Return to Steady Pelleting *)
        ELSE
            bCmdCoaterDischargeGate := FALSE;
            nFsm_CurrentState       := 8; (* Return to State 8 *)
        END_IF;

        IF NOT bEnable THEN nFsm_CurrentState := 10; END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 10: CONTROLLED DIE FLUSH & NORMAL SEQUENCE SHUTDOWN
       ------------------------------------------------------------------------------------------------ *)
    10:
        bSysRunning            := TRUE;
        bCmdBypassFlap_Divert  := TRUE; (* Divert reject flap *)

        (* Feeder screw stopped, dry flush meal cleans out die, steam valve closed *)
        u_ctrl[1] := 0.0;    (* Feeder STOP *)
        u_ctrl[2] := 0.0;    (* Steam CLOSED *)
        u_ctrl[3] := 200.0;  (* Conditioner clears remaining holdup *)
        u_ctrl[4] := 40.0;   (* Retract rollers to 1.50 mm *)
        u_ctrl[5] := 50.0;   (* Empty cooler bed *)
        u_ctrl[6] := 60.0;

        (* Verify mill current drops back to idle (< 220 A) indicating die empty *)
        IF rFsm_StateTimeElapsed_s >= tFsm_FlushShutdown_s AND rVoted_PressMotorCurrent_A <= 220.0 THEN
            (* Mill empty, safe to stop main drive *)
            nFsm_CurrentState := 0; (* Return to Cold Idle Standby *)
        ELSIF rFsm_StateTimeElapsed_s >= 120.0 THEN
            nFsm_CurrentState := 0; (* Forced shutdown timeout *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 11: EMERGENCY OVERLOAD BYPASS & DIE CHOKE LOCKOUT
       ------------------------------------------------------------------------------------------------ *)
    11:
        bSysRunning            := FALSE;
        bSysFault              := TRUE;
        bEmergencyBypassActive := TRUE;
        bCmdBypassFlap_Divert  := TRUE; (* OPEN BYPASS FLAP IMMEDIATELY (within 150 ms) *)

        (* Trip all feeding & heating actuators instantly *)
        u_ctrl[1] := 0.0;    (* Immediate Feeder Screw Trip *)
        u_ctrl[2] := 0.0;    (* Fast Steam Shut-off *)
        u_ctrl[3] := 0.0;    (* Stop Agitator *)
        u_ctrl[4] := 0.0;    (* Retract Roller Hydraulic Rams to Maximum Clearance (2.50 mm) *)
        u_ctrl[5] := 0.0;    (* Stop Cooler Discharge *)
        u_ctrl[6] := 30.0;

        bCmdCoaterVacuumPump    := FALSE;
        bCmdCoaterFatSprayValve := FALSE;
        bCmdCoaterEnzymeValve   := FALSE;
        bCmdCoaterVentValve     := TRUE;  (* Vent vacuum chamber *)
        bCmdCoaterDischargeGate := FALSE;

        (* Latch Fault until operator physical reset *)
        IF bReset AND NOT bFsm_InterlockTripped THEN
            nFsm_ShearPinTripLatch  := FALSE;
            nFsm_DieChokeFaultLatch := FALSE;
            nFsm_CurrentState       := 0; (* Return to Standby *)
        END_IF;

ELSE
    nFsm_CurrentState := 0;
END_CASE;

nFsmState_Active := nFsm_CurrentState;
"""
