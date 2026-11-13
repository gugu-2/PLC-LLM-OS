# -*- coding: utf-8 -*-
"""
Generator module for Phase 4: 14-Stage Deterministic Operational Finite State Machine (FSM)
"""

def generate_phase_4():
    lines = []
    lines.append("""(* ============================================================================================== *)
(* PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)                          *)
(* Full Operational Stamping Press Lifecycle: TDC Standby, Deep Draw, BDC Dwell, Decompression   *)
(* ============================================================================================== *)

(* Master Safety Trip Interlock Override *)
IF OUT_TRIP_EMERGENCY_ACTIVE THEN
    nFSM_CurrentState := 999; (* Force immediate transition to Emergency State *)
END_IF;

CASE nFSM_CurrentState OF

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 0: SYSTEM POWER-UP, SENSOR HOMING & PRE-FLIGHT HYDRAULIC CHARGING                   *)
    (* ------------------------------------------------------------------------------------------ *)
    0:
        OUT_BRAKE_RELEASE_SOLENOID := FALSE;
        OUT_CLUTCH_ENGAGE_SOLENOID := FALSE;
        OUT_PART_LIFTER_EXTEND     := FALSE;
        OUT_SAFETY_MUTING_ACTIVE   := FALSE;
        OUT_FAST_DECOMP_VALVE_FL   := FALSE;
        OUT_FAST_DECOMP_VALVE_FR   := FALSE;
        OUT_FAST_DECOMP_VALVE_RL   := FALSE;
        OUT_FAST_DECOMP_VALVE_RR   := FALSE;
        OUT_ANTI_REBOUND_DAMP_L    := 0.000;
        OUT_ANTI_REBOUND_DAMP_R    := 0.000;
        OUT_CUSH_PRE_ACCEL_VALVE   := 0.000;

        fsm_state_timer_ms := fsm_state_timer_ms + 2.000;

        IF (fsm_state_timer_ms > 1000.000) AND DI_EMERGENCY_STOP_HARDWIRE_OK AND (PT_HYD_SUPPLY > 180.000) THEN
            fsm_init_complete  := TRUE;
            fsm_state_timer_ms := 0.000;
            nFSM_PreviousState := 0;
            nFSM_CurrentState  := 10; (* Transition to TDC Standby *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 10: PRESS TOP DEAD CENTER (TDC) HOMED STANDBY                                       *)
    (* ------------------------------------------------------------------------------------------ *)
    10:
        OUT_BRAKE_RELEASE_SOLENOID := FALSE;
        OUT_CLUTCH_ENGAGE_SOLENOID := FALSE;
        OUT_PART_LIFTER_EXTEND     := FALSE;
        OUT_SAFETY_MUTING_ACTIVE   := FALSE;
        OUT_FAST_DECOMP_VALVE_FL   := FALSE;
        OUT_FAST_DECOMP_VALVE_FR   := FALSE;
        OUT_FAST_DECOMP_VALVE_RL   := FALSE;
        OUT_FAST_DECOMP_VALVE_RR   := FALSE;
        OUT_ANTI_REBOUND_DAMP_L    := 0.000;
        OUT_ANTI_REBOUND_DAMP_R    := 0.000;
        OUT_CUSH_PRE_ACCEL_VALVE   := 0.000;
        OUT_STROKE_COMPLETED_PULSE := FALSE;

        fsm_state_timer_ms := fsm_state_timer_ms + 2.000;

        (* Check Cycle Initiation Permissives *)
        IF (ENABLE_AUTO_CYCLE OR REQUEST_SINGLE_STROKE) AND OUT_SAFETY_READY_INTERLOCK
            AND DI_DIE_PROT_PART_SEATED AND (NOT DI_DIE_PROT_DOUBLE_BLANK) THEN
            fsm_state_timer_ms := 0.000;
            fsm_cycle_timer_ms := 0.000;
            nFSM_PreviousState := 10;
            nFSM_CurrentState  := 20; (* Transition to Rapid Approach *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 20: SLIDE RAPID DESCENT APPROACH (CRANK 0 TO 105 DEG)                               *)
    (* ------------------------------------------------------------------------------------------ *)
    20:
        OUT_BRAKE_RELEASE_SOLENOID := TRUE;
        OUT_CLUTCH_ENGAGE_SOLENOID := TRUE;
        OUT_PART_LIFTER_EXTEND     := FALSE;
        OUT_FAST_DECOMP_VALVE_FL   := FALSE;
        OUT_FAST_DECOMP_VALVE_FR   := FALSE;
        OUT_FAST_DECOMP_VALVE_RL   := FALSE;
        OUT_FAST_DECOMP_VALVE_RR   := FALSE;
        OUT_ANTI_REBOUND_DAMP_L    := 0.000;
        OUT_ANTI_REBOUND_DAMP_R    := 0.000;
        OUT_CUSH_PRE_ACCEL_VALVE   := 0.000;

        fsm_state_timer_ms := fsm_state_timer_ms + 2.000;
        fsm_cycle_timer_ms := fsm_cycle_timer_ms + 2.000;

        (* Evaluate Transition to Cushion Pre-Acceleration *)
        IF ENABLE_CUSHION_PRE_ACCELERATION THEN
            IF TMR_CRANK_VOTED_RESULT >= SETPOINT_PRE_ACCEL_ADVANCE_ANGLE THEN
                fsm_state_timer_ms := 0.000;
                nFSM_PreviousState := 20;
                nFSM_CurrentState  := 30; (* Transition to Cushion Pre-Acceleration *)
            END_IF;
        ELSE
            IF TMR_CRANK_VOTED_RESULT >= 125.000 THEN
                fsm_state_timer_ms := 0.000;
                nFSM_PreviousState := 20;
                nFSM_CurrentState  := 40; (* Direct transition to Blank Touch *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 30: DIE CUSHION PRE-ACCELERATION IMPACT VELOCITY MATCHING                           *)
    (* Accelerates cushion downward to match ~85% of ram speed to eliminate sheet tear & impact   *)
    (* ------------------------------------------------------------------------------------------ *)
    30:
        OUT_BRAKE_RELEASE_SOLENOID := TRUE;
        OUT_CLUTCH_ENGAGE_SOLENOID := TRUE;
        OUT_PART_LIFTER_EXTEND     := FALSE;

        fsm_state_timer_ms := fsm_state_timer_ms + 2.000;
        fsm_cycle_timer_ms := fsm_cycle_timer_ms + 2.000;

        (* Compute Pre-Acceleration Downward Boost Command *)
        cush_pre_accel_target_v  := kinematic_velocity_vz * 0.850000;
        OUT_CUSH_PRE_ACCEL_VALVE := (cush_pre_accel_target_v / 500.000) * 100.000;
        IF OUT_CUSH_PRE_ACCEL_VALVE > 90.000 THEN
            OUT_CUSH_PRE_ACCEL_VALVE := 90.000;
        ELSIF OUT_CUSH_PRE_ACCEL_VALVE < 15.000 THEN
            OUT_CUSH_PRE_ACCEL_VALVE := 15.000;
        END_IF;

        (* Detect Blank Impact Touch: Tonnage exceeds blank holder pre-load threshold *)
        IF (OUT_ESTIMATED_TOTAL_TONNAGE > 850.000) OR (TMR_CRANK_VOTED_RESULT >= 130.000) THEN
            OUT_CUSH_PRE_ACCEL_VALVE := 0.000;
            fsm_state_timer_ms := 0.000;
            nFSM_PreviousState := 30;
            nFSM_CurrentState  := 40; (* Transition to Blank Touch Synchronization *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 40: BLANK TOUCH SYNCHRONIZATION & INITIAL CLAMPING                                  *)
    (* ------------------------------------------------------------------------------------------ *)
    40:
        OUT_BRAKE_RELEASE_SOLENOID := TRUE;
        OUT_CLUTCH_ENGAGE_SOLENOID := TRUE;
        OUT_PART_LIFTER_EXTEND     := FALSE;
        OUT_CUSH_PRE_ACCEL_VALVE   := 0.000;

        fsm_state_timer_ms := fsm_state_timer_ms + 2.000;
        fsm_cycle_timer_ms := fsm_cycle_timer_ms + 2.000;

        IF (OUT_ESTIMATED_TOTAL_TONNAGE > 2500.000) OR (TMR_CRANK_VOTED_RESULT >= 138.000) THEN
            fsm_state_timer_ms := 0.000;
            nFSM_PreviousState := 40;
            nFSM_CurrentState  := 50; (* Transition to Deep Draw Forming *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 50: DEEP DRAW FORMING STROKE (CRANK 138 TO 172 DEG)                                 *)
    (* Full 35,000 kN Forming Force with Dynamic Cushion Flow & Blank Holder Resistance          *)
    (* ------------------------------------------------------------------------------------------ *)
    50:
        OUT_BRAKE_RELEASE_SOLENOID := TRUE;
        OUT_CLUTCH_ENGAGE_SOLENOID := TRUE;
        OUT_PART_LIFTER_EXTEND     := FALSE;

        fsm_state_timer_ms := fsm_state_timer_ms + 2.000;
        fsm_cycle_timer_ms := fsm_cycle_timer_ms + 2.000;

        (* Transition to Eccentric Balancing if Tipping Moment exceeds threshold *)
        IF (ABS(overturning_moment_mx) > 250.000) OR (ABS(overturning_moment_my) > 250.000) THEN
            fsm_state_timer_ms := 0.000;
            nFSM_PreviousState := 50;
            nFSM_CurrentState  := 60; (* Transition to Active Eccentric Balancing *)
        ELSIF TMR_CRANK_VOTED_RESULT >= 172.000 THEN
            fsm_state_timer_ms := 0.000;
            nFSM_PreviousState := 50;
            nFSM_CurrentState  := 70; (* Transition to BDC Dwell *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 60: REAL-TIME ECCENTRIC TONNAGE BALANCING & PARALLELISM LEVELING                     *)
    (* ------------------------------------------------------------------------------------------ *)
    60:
        OUT_BRAKE_RELEASE_SOLENOID := TRUE;
        OUT_CLUTCH_ENGAGE_SOLENOID := TRUE;
        OUT_PART_LIFTER_EXTEND     := FALSE;

        fsm_state_timer_ms := fsm_state_timer_ms + 2.000;
        fsm_cycle_timer_ms := fsm_cycle_timer_ms + 2.000;

        IF TMR_CRANK_VOTED_RESULT >= 175.000 THEN
            fsm_state_timer_ms := 0.000;
            nFSM_PreviousState := 60;
            nFSM_CurrentState  := 70; (* Transition to BDC Dwell *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 70: BOTTOM DEAD CENTER (BDC) DWELL & MICRO-STRAIN COINING                           *)
    (* ------------------------------------------------------------------------------------------ *)
    70:
        OUT_BRAKE_RELEASE_SOLENOID := TRUE;
        OUT_CLUTCH_ENGAGE_SOLENOID := TRUE;
        OUT_PART_LIFTER_EXTEND     := FALSE;

        fsm_state_timer_ms := fsm_state_timer_ms + 2.000;
        fsm_cycle_timer_ms := fsm_cycle_timer_ms + 2.000;
        fsm_dwell_timer_ms := fsm_dwell_timer_ms + 2.000;

        (* Latch Peak Pressure at BDC for Decompression Curve Calculation *)
        bdc_latched_pressure := OUT_MEAN_CUSHION_PRESSURE;

        IF (fsm_dwell_timer_ms >= SETPOINT_BDC_DWELL_TIME_MS) OR (TMR_CRANK_VOTED_RESULT >= 183.000) THEN
            fsm_dwell_timer_ms := 0.000;
            fsm_state_timer_ms := 0.000;
            decomp_time_elapsed_ms := 0.000;
            nFSM_PreviousState := 70;
            nFSM_CurrentState  := 80; (* Transition to Controlled Decompression *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 80: CONTROLLED HYDRAULIC DECOMPRESSION (CRANK 183 TO 200 DEG)                       *)
    (* Exponential bleed-off of cushion pressure to prevent cavitation & shockwaves               *)
    (* ------------------------------------------------------------------------------------------ *)
    80:
        OUT_BRAKE_RELEASE_SOLENOID := TRUE;
        OUT_CLUTCH_ENGAGE_SOLENOID := TRUE;
        OUT_PART_LIFTER_EXTEND     := FALSE;

        fsm_state_timer_ms := fsm_state_timer_ms + 2.000;
        fsm_cycle_timer_ms := fsm_cycle_timer_ms + 2.000;
        decomp_time_elapsed_ms := decomp_time_elapsed_ms + 2.000;

        (* Exponential Decompression Profile: P(t) = P_bdc * exp(-t / tau) *)
        IF SETPOINT_DECOMPRESSION_TIME_MS > 5.0 THEN
            decomp_decay_factor := 1.000000 - (decomp_time_elapsed_ms / SETPOINT_DECOMPRESSION_TIME_MS);
            IF decomp_decay_factor < 0.050 THEN
                decomp_decay_factor := 0.050;
            END_IF;
        ELSE
            decomp_decay_factor := 0.050;
        END_IF;

        (* Modulate Fast Decompression Valves *)
        OUT_FAST_DECOMP_VALVE_FL := TRUE;
        OUT_FAST_DECOMP_VALVE_FR := TRUE;
        OUT_FAST_DECOMP_VALVE_RL := TRUE;
        OUT_FAST_DECOMP_VALVE_RR := TRUE;

        IF (decomp_time_elapsed_ms >= SETPOINT_DECOMPRESSION_TIME_MS) OR (OUT_MEAN_CUSHION_PRESSURE < 35.000)
            OR (TMR_CRANK_VOTED_RESULT >= 200.000) THEN
            OUT_FAST_DECOMP_VALVE_FL := FALSE;
            OUT_FAST_DECOMP_VALVE_FR := FALSE;
            OUT_FAST_DECOMP_VALVE_RL := FALSE;
            OUT_FAST_DECOMP_VALVE_RR := FALSE;
            fsm_state_timer_ms := 0.000;
            nFSM_PreviousState := 80;
            nFSM_CurrentState  := 90; (* Transition to Anti-Rebound Active Damping *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 90: ANTI-REBOUND ACTIVE HYDRAULIC DAMPING (CRANK 200 TO 235 DEG)                     *)
    (* Suppresses mechanical rebound, blank flanging distortion & cushion pin bounce             *)
    (* ------------------------------------------------------------------------------------------ *)
    90:
        OUT_BRAKE_RELEASE_SOLENOID := TRUE;
        OUT_CLUTCH_ENGAGE_SOLENOID := TRUE;
        OUT_PART_LIFTER_EXTEND     := FALSE;

        fsm_state_timer_ms := fsm_state_timer_ms + 2.000;
        fsm_cycle_timer_ms := fsm_cycle_timer_ms + 2.000;

        (* Active Hydraulic Counter-Pressure Damping *)
        cush_anti_rebound_damping_effort := (SETPOINT_ANTI_REBOUND_DAMP_GAIN * 0.010)
            * (kinematic_velocity_vz * 0.150000);
        IF cush_anti_rebound_damping_effort > 75.000 THEN
            cush_anti_rebound_damping_effort := 75.000;
        ELSIF cush_anti_rebound_damping_effort < 10.000 THEN
            cush_anti_rebound_damping_effort := 10.000;
        END_IF;

        OUT_ANTI_REBOUND_DAMP_L := cush_anti_rebound_damping_effort;
        OUT_ANTI_REBOUND_DAMP_R := cush_anti_rebound_damping_effort;

        IF TMR_CRANK_VOTED_RESULT >= 235.000 THEN
            OUT_ANTI_REBOUND_DAMP_L := 0.000;
            OUT_ANTI_REBOUND_DAMP_R := 0.000;
            fsm_state_timer_ms := 0.000;
            nFSM_PreviousState := 90;
            nFSM_CurrentState  := 100; (* Transition to Ram Ascent *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 100: SLIDE RAPID ASCENT RETURN (CRANK 235 TO 310 DEG)                                *)
    (* ------------------------------------------------------------------------------------------ *)
    100:
        OUT_BRAKE_RELEASE_SOLENOID := TRUE;
        OUT_CLUTCH_ENGAGE_SOLENOID := TRUE;
        OUT_PART_LIFTER_EXTEND     := FALSE;
        OUT_ANTI_REBOUND_DAMP_L    := 0.000;
        OUT_ANTI_REBOUND_DAMP_R    := 0.000;

        fsm_state_timer_ms := fsm_state_timer_ms + 2.000;
        fsm_cycle_timer_ms := fsm_cycle_timer_ms + 2.000;

        IF TMR_CRANK_VOTED_RESULT >= 310.000 THEN
            fsm_state_timer_ms := 0.000;
            nFSM_PreviousState := 100;
            nFSM_CurrentState  := 110; (* Transition to Part Lift & Unload *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 110: PART LIFT PIN EXTENSION & TRANSFER ROBOT UNLOAD CLEARANCE                      *)
    (* ------------------------------------------------------------------------------------------ *)
    110:
        OUT_BRAKE_RELEASE_SOLENOID := TRUE;
        OUT_CLUTCH_ENGAGE_SOLENOID := TRUE;
        OUT_PART_LIFTER_EXTEND     := TRUE; (* Raise cushion pins to transfer line height *)

        fsm_state_timer_ms := fsm_state_timer_ms + 2.000;
        fsm_cycle_timer_ms := fsm_cycle_timer_ms + 2.000;
        fsm_eject_timer_ms := fsm_eject_timer_ms + 2.000;

        IF (TMR_CRANK_VOTED_RESULT >= 345.000) OR (fsm_eject_timer_ms > 450.000) THEN
            fsm_eject_timer_ms := 0.000;
            fsm_state_timer_ms := 0.000;
            nFSM_PreviousState := 110;
            nFSM_CurrentState  := 120; (* Transition to TDC Deceleration *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 120: TDC DECELERATION SOFT-STOP & CYCLE COMPLETION PULSE                            *)
    (* ------------------------------------------------------------------------------------------ *)
    120:
        OUT_PART_LIFTER_EXTEND     := FALSE;
        OUT_STROKE_COMPLETED_PULSE := TRUE;
        OUT_TOTAL_STROKE_COUNT     := OUT_TOTAL_STROKE_COUNT + 1;
        OUT_CYCLE_TIME_LAST_MS     := fsm_cycle_timer_ms;

        fsm_state_timer_ms := fsm_state_timer_ms + 2.000;

        (* Slide reaches TDC (0 / 360 deg) *)
        IF (TMR_CRANK_VOTED_RESULT >= 358.500) OR (TMR_CRANK_VOTED_RESULT <= 1.500) OR (fsm_state_timer_ms > 350.000) THEN
            OUT_BRAKE_RELEASE_SOLENOID := FALSE; (* Set mechanical brake *)
            OUT_CLUTCH_ENGAGE_SOLENOID := FALSE;
            fsm_state_timer_ms := 0.000;
            fsm_cycle_timer_ms := 0.000;
            nFSM_PreviousState := 120;

            IF ENABLE_AUTO_CYCLE THEN
                nFSM_CurrentState := 20; (* Continue continuous stamping *)
            ELSE
                nFSM_CurrentState := 10; (* Stop and await next single stroke *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 999: CRITICAL EMERGENCY FAST SHUTDOWN & HYDRAULIC DUMP TRIP                         *)
    (* ------------------------------------------------------------------------------------------ *)
    999:
        OUT_BRAKE_RELEASE_SOLENOID := FALSE; (* Immediate Spring-Set Caliper Brake Clamp *)
        OUT_CLUTCH_ENGAGE_SOLENOID := FALSE; (* Disengage Main Flywheel Clutch *)
        OUT_PART_LIFTER_EXTEND     := FALSE;
        OUT_SAFETY_MUTING_ACTIVE   := FALSE;
        OUT_SERVO_RAM_SPEED_REF    := 0.000;
        OUT_SERVO_RAM_TORQUE_LIMIT := 0.000;

        (* Open all fast dump poppets to depressurize 35,000 kN press hydraulics *)
        OUT_FAST_DECOMP_VALVE_FL   := TRUE;
        OUT_FAST_DECOMP_VALVE_FR   := TRUE;
        OUT_FAST_DECOMP_VALVE_RL   := TRUE;
        OUT_FAST_DECOMP_VALVE_RR   := TRUE;
        OUT_CUSH_PRE_ACCEL_VALVE   := 0.000;
        OUT_ANTI_REBOUND_DAMP_L    := 0.000;
        OUT_ANTI_REBOUND_DAMP_R    := 0.000;

        (* Neutralize Proportional Cushion Valves *)
        OUT_CUSH_VALVE_CMD_P1 := 0.000;
        OUT_CUSH_VALVE_CMD_P2 := 0.000;
        OUT_CUSH_VALVE_CMD_P3 := 0.000;
        OUT_CUSH_VALVE_CMD_P4 := 0.000;
        OUT_CUSH_VALVE_CMD_P5 := 0.000;
        OUT_CUSH_VALVE_CMD_P6 := 0.000;
        OUT_CUSH_VALVE_CMD_P7 := 0.000;
        OUT_CUSH_VALVE_CMD_P8 := 0.000;

        fsm_state_timer_ms := fsm_state_timer_ms + 2.000;

        (* Safe Reset Recovery Logic *)
        IF RESET_ALARMS AND DI_EMERGENCY_STOP_HARDWIRE_OK AND (NOT OUT_TRIP_EMERGENCY_ACTIVE) THEN
            OUT_FAST_DECOMP_VALVE_FL := FALSE;
            OUT_FAST_DECOMP_VALVE_FR := FALSE;
            OUT_FAST_DECOMP_VALVE_RL := FALSE;
            OUT_FAST_DECOMP_VALVE_RR := FALSE;
            fsm_state_timer_ms := 0.000;
            nFSM_PreviousState := 999;
            nFSM_CurrentState  := 0; (* Return to System Initialization *)
        END_IF;

END_CASE;

OUT_ACTIVE_FSM_STATE      := nFSM_CurrentState;
OUT_CYCLE_TIME_CURRENT_MS := fsm_cycle_timer_ms;
""")
    return "".join(lines)

print("Phase 4 module loaded.")
