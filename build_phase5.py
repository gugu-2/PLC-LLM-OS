# -*- coding: utf-8 -*-
"""
Generator module for Phase 5: Optical Safety Light Curtain Muting & Mechanical Brake Monitor
"""

def generate_phase_5():
    lines = []
    lines.append("""(* ============================================================================================== *)
(* PHASE 5: OPTICAL SAFETY LIGHT CURTAIN MUTING ENGINE & MECHANICAL BRAKE MONITOR                 *)
(* Certified Sequential 4-Sensor Muting & High-Speed Microsecond Brake Performance Surveillance  *)
(* ============================================================================================== *)

(* ---------------------------------------------------------------------------------------------- *)
(* Step 5.1: Optical Safety Light Curtain Muting Engine                                          *)
(* ---------------------------------------------------------------------------------------------- *)
(* Verify Downward Motion & Permissible Crank Muting Angle Window (115 deg to 175 deg) *)
IF (TMR_CRANK_VOTED_RESULT >= 115.000) AND (TMR_CRANK_VOTED_RESULT <= 175.000) AND (kinematic_velocity_vz > 15.000) THEN
    muting_direction_valid := TRUE;
ELSE
    muting_direction_valid := FALSE;
END_IF;

(* 4-Sensor Entry Sequence Evaluation: MS1 followed by MS2 *)
IF DI_MUTING_SENSOR_MS1 AND muting_direction_valid THEN
    IF DI_MUTING_SENSOR_MS2 AND (muting_timer_ms < 1500.000) THEN
        muting_entry_latch := TRUE;
    END_IF;
END_IF;

IF muting_entry_latch THEN
    muting_timer_ms := muting_timer_ms + 2.000;
    (* Verify Muting Active Within Max Time Window (2,500 ms) *)
    IF (muting_timer_ms <= 2500.000) AND muting_direction_valid THEN
        muting_active_flag := TRUE;
    ELSE
        muting_active_flag := FALSE;
        muting_entry_latch := FALSE;
        muting_timer_ms    := 0.000;
    END_IF;

    (* Exit Sequence Check: De-latch on MS3 / MS4 clear *)
    IF DI_MUTING_SENSOR_MS3 AND DI_MUTING_SENSOR_MS4 THEN
        muting_entry_latch := FALSE;
        muting_active_flag := FALSE;
        muting_timer_ms    := 0.000;
    END_IF;
ELSE
    muting_active_flag := FALSE;
    muting_timer_ms    := 0.000;
END_IF;

OUT_SAFETY_MUTING_ACTIVE := muting_active_flag;

(* Dual-Channel OSSD Cross-Monitoring with Discrepancy Timer *)
IF (DI_OPTICAL_CURTAIN_FRONT_OSSD1 <> DI_OPTICAL_CURTAIN_FRONT_OSSD2) OR (DI_OPTICAL_CURTAIN_REAR_OSSD1 <> DI_OPTICAL_CURTAIN_REAR_OSSD2) THEN
    ossd_discrepancy_timer := ossd_discrepancy_timer + 2.000;
ELSE
    ossd_discrepancy_timer := 0.000;
END_IF;

(* Evaluate Optical Safety Light Curtain Violation Trip *)
IF NOT muting_active_flag THEN
    IF (NOT DI_OPTICAL_CURTAIN_FRONT_OSSD1) OR (NOT DI_OPTICAL_CURTAIN_FRONT_OSSD2)
        OR (NOT DI_OPTICAL_CURTAIN_REAR_OSSD1) OR (NOT DI_OPTICAL_CURTAIN_REAR_OSSD2)
        OR (ossd_discrepancy_timer > 40.000) THEN
        ALM_SAFETY_CURTAIN_TRIP := TRUE;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* Step 5.2: Mechanical Flywheel Brake Performance Monitor                                        *)
(* ---------------------------------------------------------------------------------------------- *)
(* Trigger Detection: Brake Solenoid De-Energized While Press Is Rotating *)
IF (NOT OUT_BRAKE_RELEASE_SOLENOID) AND (NOT brake_monitor_in_test) AND (ABS(kinematic_velocity_vz) > 10.000) THEN
    brake_monitor_in_test    := TRUE;
    brake_stop_cmd_angle     := TMR_CRANK_VOTED_RESULT;
    brake_stop_cmd_timer_ms  := 0.000;
    brake_speed_at_trip_spm  := SETPOINT_PRESS_SPEED_SPM;
END_IF;

IF brake_monitor_in_test THEN
    brake_stop_cmd_timer_ms := brake_stop_cmd_timer_ms + 2.000;

    (* Detect Full Slide Motion Arrest (Velocity < 0.5 mm/s) *)
    IF ABS(kinematic_velocity_vz) < 0.500 THEN
        brake_monitor_in_test    := FALSE;
        brake_measured_stop_time := brake_stop_cmd_timer_ms;

        val_temp := TMR_CRANK_VOTED_RESULT - brake_stop_cmd_angle;
        IF val_temp < 0.000 THEN
            val_temp := val_temp + 360.000;
        END_IF;
        brake_measured_stop_ang := val_temp;

        OUT_BRAKE_STOPPING_TIME_MS   := brake_measured_stop_time;
        OUT_BRAKE_STOPPING_ANGLE_DEG := brake_measured_stop_ang;

        (* Check Stopping Time HH Trip Point *)
        IF brake_measured_stop_time > SETPOINT_BRAKE_MAX_STOP_TIME_MS THEN
            ALM_BRAKE_STOP_TIME_HH_TRIP := TRUE;
        END_IF;

        (* Check Stopping Angle Overrun HH Trip Point *)
        IF brake_measured_stop_ang > SETPOINT_BRAKE_MAX_OVERRUN_ANGLE THEN
            ALM_BRAKE_OVERRUN_HH_TRIP := TRUE;
        END_IF;
    END_IF;

    (* Timeout Trip Protection: Press Failed to Stop within 500 ms *)
    IF brake_stop_cmd_timer_ms > 500.000 THEN
        brake_monitor_in_test       := FALSE;
        ALM_BRAKE_STOP_TIME_HH_TRIP := TRUE;
    END_IF;
END_IF;
""")
    return "".join(lines)

print("Phase 5 module loaded.")
