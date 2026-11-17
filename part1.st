FUNCTION_BLOCK FB_Steelmaking_HotStripMill_4HighRougher_HydraulicAGC
(*
====================================================================================================
 LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - METALLURGICAL AUTOMATION DIVISION
 REVERSIBLE 4-HIGH HOT STRIP ROUGHING MILL WITH DYNAMIC HYDRAULIC AGC & WORK ROLL BENDING
====================================================================================================
 ARCHITECTURE OVERVIEW:
  This Function Block executes real-time deterministic cyber-physical control for a primary heavy-duty
  reversing 4-High Hot Strip Roughing Mill with attached close-coupled vertical edger, hydraulic Automatic
  Gauge Control (H-AGC), dynamic work roll bending and balancing cylinders, 250-bar ultra-high-pressure
  descaling water headers, and multi-zone optical pyrometer thermal tracking.

 METALLURGICAL & MECHANICAL SYSTEM CHARACTERISTICS:
  - Mill Housing Modulus (Mm): 9,850 kN/mm (Housing stretch stiffness coefficient)
  - Work Roll Diameter / Barrel Length: 1,180 mm / 2,400 mm (Forged high-Cr steel)
  - Backup Roll Diameter / Barrel Length: 1,600 mm / 2,350 mm (Forged alloy steel)
  - Vertical Edger Roll Diameter / Barrel Length: 1,000 mm / 600 mm
  - Maximum Roll Separation Force: 55,000 kN (5,500 metric tons)
  - Hydraulic Screwdown Actuation: Dual differential servo cylinders (stroke 120 mm, diam 850 mm)
  - Main Drive Motors: Twin cycloconverter-fed synchronous motors, 2 x 8,500 kW, 0-40-100 rpm
  - Edger Drive Motor: 2,500 kW AC vector drive, 0-120-250 rpm
  - HP Descaling System: Multi-stage centrifugal pump array delivering 250 bar at 420 m3/h

 CYBER-PHYSICAL MATHEMATICAL RIGOR:
  1. BISRA Gauge-Meter Equation:
     h_exit = S_0 + (F_total - F_0) / M_mill + delta_S_ecc + delta_S_oil + delta_S_therm
     Where S_0 is nominal no-load roll gap, F_total is mill separating force, M_mill is mill modulus,
     delta_S_ecc is roll eccentricity harmonic compensation, delta_S_oil is backup roll oil film compensation,
     and delta_S_therm is dynamic thermal roll expansion expansion compensation.
  2. Sims Hot Rolling Force Theory with Hitchcock's Roll Flattening:
     R' = R * (1 + 16 * (1 - nu^2) / (pi * E) * (F / (W * delta_h)))
     F = (2 / sqrt(3)) * sigma_flow * W * sqrt(R' * delta_h) * Q_p(r, R', h_entry)
  3. Roll Crown & Strip Profile Mechanics:
     Crown_strip = Crown_roll_grind + Crown_thermal + Crown_wear + K_bend * F_bend - K_force * F_total
  4. Discrete State-Space Model (Ts = 0.0005 s / 500 us):
     6 States: x1=Exit gauge error [um], x2=Roll gap dynamic deflection [um],
               x3=Eccentricity error [um], x4=Roll speed mismatch [rpm],
               x5=Slab surface temp gradient [deg C], x6=Differential cylinder tilt [um]
     5 Control Inputs: u1=Operator-side servo [%], u2=Drive-side servo [%],
                       u3=Work roll bending valve [bar], u4=Main drive speed [rpm],
                       u5=High-pressure descaling header [%]
     4 Measured Outputs: y1=Dual load cell rolling force [kN], y2=LVDT cylinder pos [um],
                         y3=Laser optical gauge [um], y4=Dual pyrometer temp [deg C]
     Kalman Innovation Filter: x_hat[k+1] = A * x_hat[k] + B * u[k] + L * (y[k] - C * x_hat[k] - D * u[k])
  5. Receding-Horizon MPC Optimization via 10 Unrolled Projected Gradient Descent (PGD) Iterations:
     Quadratic penalties Q (tracking error), R (servo effort), P (terminal cost), S (slew limits).
     Physical constraints: roll bite skid prevention, roll chatter vibration suppression (120-180 Hz),
     strip crown & wedging minimization, and hydraulic anti-cavitation limits.
  6. 4-Channel 2oo3 Triple Modular Redundancy (TMR) Sensing:
     Channels: Rolling Force, Hydraulic AGC Pressure, Mill Armature Current, Descaling Pressure.
     50 ms debounce persistence timers with bumpless degradation: 2oo3 -> 1oo2 -> 1oo1 -> Trip.
  7. 14-Stage Deterministic Production Finite State Machine (FSM):
     Furnace extract -> Laser verification -> Primary descale -> Edger pass -> Forward entry bite ->
     Dynamic AGC regulation -> Exit pyrometer check -> Reversing table decel -> Gap repositioning ->
     Reverse entry bite -> Secondary descale -> Multi-pass cycling -> Crop shear -> Transfer bar delivery.
  8. ANSI/ISA-18.2 Process Alarm Management & 5x 32-Bit Fieldbus Telemetry Words.
====================================================================================================
*)

VAR_INPUT
    (* ========================================================================================== *)
    (* SECTION 1: MASTER SYSTEM CONTROL & OPERATIONAL COMMANDS                                    *)
    (* ========================================================================================== *)
    b_Enable_System                 : BOOL := FALSE;       (* Master mill control block enable command [bool] *)
    b_Safety_Interlocks_OK          : BOOL := FALSE;       (* Plant safety fence and E-stop circuit healthy [bool] *)
    b_Auto_Sequence_Start           : BOOL := FALSE;       (* Automatic rolling multi-pass sequence trigger [bool] *)
    b_Sequence_Hold_Command         : BOOL := FALSE;       (* Hold current rolling pass at safe position [bool] *)
    b_Sequence_Abort_Command        : BOOL := FALSE;       (* Abort multi-pass sequence and reverse slab [bool] *)
    b_Alarm_Master_Acknowledge      : BOOL := FALSE;       (* Acknowledge active ISA-18.2 process alarms [bool] *)
    b_Alarm_Reset_Command           : BOOL := FALSE;       (* Reset latched alarms and trip registers [bool] *)
    b_Manual_Jog_Fwd_Command        : BOOL := FALSE;       (* Manual jog forward table and rolls [bool] *)
    b_Manual_Jog_Rev_Command        : BOOL := FALSE;       (* Manual jog reverse table and rolls [bool] *)
    b_Roll_Gap_Calibration_Request  : BOOL := FALSE;       (* Trigger automated kissing roll zero calibration [bool] *)

    (* ========================================================================================== *)
    (* SECTION 2: SLAB METALLURGICAL TRACKING & PRODUCTION RECIPE                                 *)
    (* ========================================================================================== *)
    di_Slab_Identification_Number   : DINT := 10001;       (* Production schedule tracking slab ID [id] *)
    ui_Steel_Grade_Code             : UINT := 1045;        (* Metallurgical grade designation AISI/SAE [code] *)
    r_Nominal_Incoming_Thickness    : REAL := 250.0;       (* Raw slab thickness from reheating furnace [mm] *)
    r_Nominal_Incoming_Width        : REAL := 1500.0;      (* Raw slab width from reheating furnace [mm] *)
    r_Nominal_Incoming_Length       : REAL := 10500.0;     (* Raw slab cut length before roughing [mm] *)
    r_Target_Transfer_Bar_Thickness : REAL := 32.0;        (* Target transfer bar thickness for finishing mill [mm] *)
    r_Target_Transfer_Bar_Width     : REAL := 1450.0;      (* Target transfer bar width after edging [mm] *)
    r_Steel_Carbon_Content_Pct      : REAL := 0.18;        (* Carbon content for flow stress calculation [%] *)
    r_Steel_Manganese_Content_Pct   : REAL := 1.45;        (* Manganese alloy content [%] *)
    r_Steel_Silicon_Content_Pct     : REAL := 0.25;        (* Silicon alloy content [%] *)
    r_Target_Furnace_Extract_Temp   : REAL := 1250.0;      (* Minimum target extraction temperature [deg C] *)
    r_Minimum_Finishing_Entry_Temp  : REAL := 1040.0;      (* Critical low thermal abort limit [deg C] *)
    ui_Total_Scheduled_Rolling_Passes: UINT := 5;          (* Total number of roughing reduction passes (3, 5, 7) [passes] *)

    (* ========================================================================================== *)
    (* SECTION 3: 4-CHANNEL 2oo3 REDUNDANT PROCESS SENSOR ARRAYS                                  *)
    (* ========================================================================================== *)
    (* Channel 1: Total Rolling Force Sensors (3x Load Cells) *)
    r_Force_Sensor_Raw_A            : REAL := 0.0;         (* Mill stand roll force load cell transducer A [kN] *)
    r_Force_Sensor_Raw_B            : REAL := 0.0;         (* Mill stand roll force load cell transducer B [kN] *)
    r_Force_Sensor_Raw_C            : REAL := 0.0;         (* Mill stand roll force load cell transducer C [kN] *)
    b_Force_Sensor_Healthy_A        : BOOL := TRUE;        (* Load cell channel A electrical health bit [bool] *)
    b_Force_Sensor_Healthy_B        : BOOL := TRUE;        (* Load cell channel B electrical health bit [bool] *)
    b_Force_Sensor_Healthy_C        : BOOL := TRUE;        (* Load cell channel C electrical health bit [bool] *)

    (* Channel 2: Main Hydraulic AGC Cylinder Pressure Sensors (3x Piezo Transmitters) *)
    r_Press_AGC_Raw_A               : REAL := 210.0;       (* Hydraulic AGC servo cylinder pressure A [bar] *)
    r_Press_AGC_Raw_B               : REAL := 210.0;       (* Hydraulic AGC servo cylinder pressure B [bar] *)
    r_Press_AGC_Raw_C               : REAL := 210.0;       (* Hydraulic AGC servo cylinder pressure C [bar] *)
    b_Press_AGC_Healthy_A           : BOOL := TRUE;        (* Hydraulic AGC pressure transmitter A health [bool] *)
    b_Press_AGC_Healthy_B           : BOOL := TRUE;        (* Hydraulic AGC pressure transmitter B health [bool] *)
    b_Press_AGC_Healthy_C           : BOOL := TRUE;        (* Hydraulic AGC pressure transmitter C health [bool] *)

    (* Channel 3: Mill Motor Armature Current Transducers (3x Rogowski / Hall Array) *)
    r_Curr_Motor_Raw_A              : REAL := 1.2;         (* Main twin drive motor armature current A [kA] *)
    r_Curr_Motor_Raw_B              : REAL := 1.2;         (* Main twin drive motor armature current B [kA] *)
    r_Curr_Motor_Raw_C              : REAL := 1.2;         (* Main twin drive motor armature current C [kA] *)
    b_Curr_Motor_Healthy_A          : BOOL := TRUE;        (* Motor current transducer A health [bool] *)
    b_Curr_Motor_Healthy_B          : BOOL := TRUE;        (* Motor current transducer B health [bool] *)
    b_Curr_Motor_Healthy_C          : BOOL := TRUE;        (* Motor current transducer C health [bool] *)

    (* Channel 4: High-Pressure Descaling Header Water Pressure (3x Heavy Duty Pressure Transmitters) *)
    r_Press_Desc_Raw_A              : REAL := 245.0;       (* HP descaling pump header manifold pressure A [bar] *)
    r_Press_Desc_Raw_B              : REAL := 245.0;       (* HP descaling pump header manifold pressure B [bar] *)
    r_Press_Desc_Raw_C              : REAL := 245.0;       (* HP descaling pump header manifold pressure C [bar] *)
    b_Press_Desc_Healthy_A          : BOOL := TRUE;        (* Descaling pressure transmitter A health [bool] *)
    b_Press_Desc_Healthy_B          : BOOL := TRUE;        (* Descaling pressure transmitter B health [bool] *)
    b_Press_Desc_Healthy_C          : BOOL := TRUE;        (* Descaling pressure transmitter C health [bool] *)

    (* ========================================================================================== *)
    (* SECTION 4: HIGH-PRECISION ACTUATOR FEEDBACKS & OPTICAL GAUGING                             *)
    (* ========================================================================================== *)
    r_LVDT_Pos_Operator_Side        : REAL := 65000.0;     (* OS hydraulic cylinder position feedback [um] *)
    r_LVDT_Pos_Drive_Side           : REAL := 65000.0;     (* DS hydraulic cylinder position feedback [um] *)
    r_WorkRoll_Bending_Press_OS     : REAL := 125.0;       (* OS roll bending cylinder actual pressure [bar] *)
    r_WorkRoll_Bending_Press_DS     : REAL := 125.0;       (* DS roll bending cylinder actual pressure [bar] *)
    r_Edger_Gap_Actual_Position     : REAL := 1480.0;      (* Vertical edger roll opening position [mm] *)
    r_Edger_Rolling_Force_Actual    : REAL := 2800.0;      (* Edger stand width reduction separating force [kN] *)
    r_Laser_Gauge_Exit_Thickness    : REAL := 65.0;        (* High-speed laser optical gauge exit thickness [mm] *)
    r_Laser_Gauge_Exit_Width        : REAL := 1475.0;      (* Optical width gauge actual measurement [mm] *)
    r_Laser_Gauge_Measurement_Valid : BOOL := TRUE;        (* Optical thickness gauge valid reading flag [bool] *)
    r_Pyrometer_Entry_Top_Temp      : REAL := 1220.0;      (* Dual-wavelength entry pyrometer top surface [deg C] *)
    r_Pyrometer_Entry_Bottom_Temp   : REAL := 1210.0;      (* Dual-wavelength entry pyrometer bottom surface [deg C] *)
    r_Pyrometer_Exit_Top_Temp       : REAL := 1180.0;      (* Exit optical pyrometer top surface [deg C] *)
    r_Pyrometer_Exit_Bottom_Temp    : REAL := 1170.0;      (* Exit optical pyrometer bottom surface [deg C] *)
    r_Main_Motor_Actual_Speed_Top   : REAL := 0.0;         (* Top work roll drive motor resolver speed [rpm] *)
    r_Main_Motor_Actual_Speed_Bot   : REAL := 0.0;         (* Bottom work roll drive motor resolver speed [rpm] *)
    r_Edger_Motor_Actual_Speed      : REAL := 0.0;         (* Edger motor resolver speed [rpm] *)
    r_Entry_Table_Actual_Speed      : REAL := 0.0;         (* Infeed reversing roller table actual speed [m/s] *)
    r_Exit_Table_Actual_Speed       : REAL := 0.0;         (* Delivery reversing roller table actual speed [m/s] *)
    r_Mill_Housing_Vibration_RMS    : REAL := 1.25;        (* Accelerometer vibration signal on mill chock [mm/s] *)
    r_Chatter_Spectral_Peak_160Hz   : REAL := 0.15;        (* 3rd octave torsional mill chatter spectral power [g] *)
    r_Hydraulic_Fluid_Supply_Temp   : REAL := 42.5;        (* Servo valve hydraulic reservoir oil temperature [deg C] *)
    r_Descaling_Header_Flow_Rate    : REAL := 385.0;       (* HP descaling header water volumetric flow [m3/h] *)
    b_Crop_Shear_Knife_Home_Pos     : BOOL := TRUE;        (* Flying crop shear home limit switch confirmed [bool] *)
    b_Crop_Shear_Ready_For_Cut      : BOOL := TRUE;        (* Crop shear hydraulic flywheel clutch armed [bool] *)
END_VAR

VAR_OUTPUT
    (* ========================================================================================== *)
    (* SECTION 1: MASTER ACTUATOR CONTROL SIGNALS                                                 *)
    (* ========================================================================================== *)
    r_Screwdown_Servo_Valve_OS      : REAL := 0.0;         (* Operator-side hydraulic servo valve command [%] *)
    r_Screwdown_Servo_Valve_DS      : REAL := 0.0;         (* Drive-side hydraulic servo valve command [%] *)
    r_WorkRoll_Bending_Servo_Valve  : REAL := 0.0;         (* Work roll positive/negative bending valve [bar] *)
    r_Main_Drive_Speed_Reference_Top: REAL := 0.0;         (* Top work roll drive speed reference [rpm] *)
    r_Main_Drive_Speed_Reference_Bot: REAL := 0.0;         (* Bottom work roll drive speed reference [rpm] *)
    r_Main_Drive_Torque_Limit_Top   : REAL := 1250.0;      (* Top drive motor active torque limit [kNm] *)
    r_Main_Drive_Torque_Limit_Bot   : REAL := 1250.0;      (* Bottom drive motor active torque limit [kNm] *)
    r_Edger_Drive_Speed_Reference   : REAL := 0.0;         (* Vertical edger motor speed reference [rpm] *)
    r_Edger_Hydraulic_Gap_Command   : REAL := 1480.0;      (* Vertical edger roll gap servo positioning [mm] *)
    r_Entry_Table_Speed_Reference   : REAL := 0.0;         (* Infeed reversing table VFD speed command [m/s] *)
    r_Exit_Table_Speed_Reference    : REAL := 0.0;         (* Delivery reversing table VFD speed command [m/s] *)
    r_HP_Descaling_Valve_Top_Cmd    : REAL := 0.0;         (* Top descaling header pneumatic valve command [%] *)
    r_HP_Descaling_Valve_Bottom_Cmd : REAL := 0.0;         (* Bottom descaling header valve command [%] *)
    b_Crop_Shear_Cut_Initiate_Trigger: BOOL := FALSE;      (* Crop shear flying cut solenoid trigger [bool] *)

    (* ========================================================================================== *)
    (* SECTION 2: ESTIMATED CYBER-PHYSICAL STATES & METROLOGY                                     *)
    (* ========================================================================================== *)
    r_Voted_Rolling_Force           : REAL := 0.0;         (* 2oo3 TMR consolidated mill separating force [kN] *)
    r_Voted_Hydraulic_AGC_Pressure  : REAL := 0.0;         (* 2oo3 TMR consolidated hydraulic AGC pressure [bar] *)
    r_Voted_Mill_Armature_Current   : REAL := 0.0;         (* 2oo3 TMR consolidated motor current [kA] *)
    r_Voted_Descaling_Water_Pressure: REAL := 0.0;         (* 2oo3 TMR consolidated descaling pressure [bar] *)
    r_Estimated_Exit_Gauge_Error    : REAL := 0.0;         (* State x1: Exit thickness deviation from target [um] *)
    r_Estimated_Mill_Deflection     : REAL := 0.0;         (* State x2: Housing & roll elastic deflection [um] *)
    r_Estimated_Roll_Eccentricity   : REAL := 0.0;         (* State x3: Roll eccentricity harmonic disturbance [um] *)
    r_Estimated_Roll_Speed_Mismatch : REAL := 0.0;         (* State x4: Top vs bottom roll circumferential slip [rpm] *)
    r_Estimated_Thermal_Gradient    : REAL := 0.0;         (* State x5: Slab cross-thickness thermal gradient [deg C] *)
    r_Estimated_Cylinder_Tilt       : REAL := 0.0;         (* State x6: Operator vs drive side differential tilt [um] *)
    r_BISRA_Gauge_Meter_Thickness   : REAL := 0.0;         (* True instantaneous thickness via BISRA equation [mm] *)
    r_Calculated_Strip_Crown        : REAL := 0.0;         (* Calculated centerline vs edge strip crown [um] *)
    r_Calculated_Strip_Wedge        : REAL := 0.0;         (* Calculated operator vs drive side strip wedge [um] *)
    r_Dynamic_Forward_Slip          : REAL := 0.0;         (* Calculated rolling forward slip factor [ratio] *)
    r_Roll_Contact_Arc_Length       : REAL := 0.0;         (* Projected length of roll bite contact arc [mm] *)

    (* ========================================================================================== *)
    (* SECTION 3: FINITE STATE MACHINE & TELEMETRY REGISTERS                                      *)
    (* ========================================================================================== *)
    ui_Active_FSM_Stage             : UINT := 0;           (* Current 14-stage roughing sequence stage [stage] *)
    ui_Current_Rolling_Pass         : UINT := 0;           (* Current active rolling pass number (1 to 7) [pass] *)
    b_Mill_In_Bite_Flag             : BOOL := FALSE;       (* Hot slab currently engaged in roll bite [bool] *)
    b_Mill_Reversing_Direction_Rev  : BOOL := FALSE;       (* False=Forward pass (1,3,5), True=Reverse pass (2,4) [bool] *)
    b_Pass_Complete_Strobe          : BOOL := FALSE;       (* Strobe on successful single pass completion [bool] *)
    b_Slab_Sequence_Complete_Strobe : BOOL := FALSE;       (* Strobe when slab reduced to transfer bar [bool] *)
    b_Emergency_Gap_Open_Active     : BOOL := FALSE;       (* Emergency rapid hydraulic roll gap opening [bool] *)
    b_TMR_Channel_Degraded_Alarm    : BOOL := FALSE;       (* Any 2oo3 sensing channel degraded to 1oo2/1oo1 [bool] *)
    b_TMR_Critical_Trip_Active      : BOOL := FALSE;       (* Severe 2oo3 multi-sensor failure emergency trip [bool] *)
    b_ISA_Alarm_HH_Active           : BOOL := FALSE;       (* Any ISA-18.2 High-High critical trip active [bool] *)
    b_ISA_Alarm_H_Active            : BOOL := FALSE;       (* Any ISA-18.2 High priority warning active [bool] *)
    b_ISA_Alarm_L_Active            : BOOL := FALSE;       (* Any ISA-18.2 Low priority warning active [bool] *)
    b_ISA_Alarm_LL_Active           : BOOL := FALSE;       (* Any ISA-18.2 Low-Low critical trip active [bool] *)
    dw_Status_Word_1                : DWORD := 16#00000000;(* Mill operational status word 1 [dword] *)
    dw_Status_Word_2                : DWORD := 16#00000000;(* Actuator and sequence status word 2 [dword] *)
    dw_Alarm_Word_1                 : DWORD := 16#00000000;(* ISA-18.2 process alarms word 1 [dword] *)
    dw_Alarm_Word_2                 : DWORD := 16#00000000;(* Hardware, safety & TMR alarms word 2 [dword] *)
    dw_Quality_Word_1               : DWORD := 16#00000000;(* Transfer bar metallurgical quality word [dword] *)
END_VAR

VAR
    (* ========================================================================================== *)
    (* SECTION 1: DISCRETE STATE-SPACE MATRICES & VECTORS (Ts = 0.0005 s / 500 us)               *)
    (* ========================================================================================== *)
    (* System Transition Matrix A [6x6] *)
    r_A_11 : REAL := 0.985420; r_A_12 : REAL := 0.042150; r_A_13 : REAL := 0.015820; r_A_14 : REAL := -0.003410; r_A_15 : REAL := -0.018420; r_A_16 : REAL := 0.006210;
    r_A_21 : REAL := 0.012540; r_A_22 : REAL := 0.942180; r_A_23 : REAL := 0.086430; r_A_24 : REAL := -0.008920; r_A_25 : REAL := -0.004120; r_A_26 : REAL := 0.021580;
    r_A_31 : REAL := -0.001850; r_A_32 : REAL := -0.015420; r_A_33 : REAL := 0.892540; r_A_34 : REAL := 0.024510; r_A_35 : REAL := 0.000000; r_A_36 : REAL := -0.004520;
    r_A_41 : REAL := 0.004820; r_A_42 : REAL := -0.006850; r_A_43 : REAL := 0.005210; r_A_44 : REAL := 0.965420; r_A_45 : REAL := 0.008450; r_A_46 : REAL := 0.001250;
    r_A_51 : REAL := 0.001250; r_A_52 : REAL := 0.000850; r_A_53 : REAL := 0.000000; r_A_54 : REAL := 0.002140; r_A_55 : REAL := 0.994250; r_A_56 : REAL := 0.000420;
    r_A_61 : REAL := 0.008450; r_A_62 : REAL := 0.014520; r_A_63 : REAL := -0.005820; r_A_64 : REAL := 0.001840; r_A_65 : REAL := 0.000210; r_A_66 : REAL := 0.952140;

    (* Input Coupling Matrix B [6x5] *)
    r_B_11 : REAL := -0.125420; r_B_12 : REAL := -0.125420; r_B_13 : REAL := 0.018540; r_B_14 : REAL := -0.045210; r_B_15 : REAL := 0.008420;
    r_B_21 : REAL := 0.285420;  r_B_22 : REAL := 0.285420;  r_B_23 : REAL := -0.042510; r_B_24 : REAL := 0.015240;  r_B_25 : REAL := -0.005210;
    r_B_31 : REAL := 0.005420;  r_B_32 : REAL := 0.005420;  r_B_33 : REAL := 0.001250;  r_B_34 : REAL := 0.038450;  r_B_35 : REAL := 0.000000;
    r_B_41 : REAL := -0.014520; r_B_42 : REAL := -0.014520; r_B_43 : REAL := 0.000850;  r_B_44 : REAL := 0.254180;  r_B_45 : REAL := -0.002150;
    r_B_51 : REAL := -0.002150; r_B_52 : REAL := -0.002150; r_B_53 : REAL := 0.000000;  r_B_54 : REAL := -0.008420; r_B_55 : REAL := -0.342150;
    r_B_61 : REAL := 0.185420;  r_B_62 : REAL := -0.185420; r_B_63 : REAL := 0.024510;  r_B_64 : REAL := 0.000000;  r_B_65 : REAL := 0.000000;

    (* Output Mapping Matrix C [4x6] *)
    r_C_11 : REAL := 45.250000; r_C_12 : REAL := 125.420000; r_C_13 : REAL := 8.520000;  r_C_14 : REAL := 1.850000;   r_C_15 : REAL := -4.250000; r_C_16 : REAL := 12.450000;
    r_C_21 : REAL := 0.852000;  r_C_22 : REAL := 1.000000;   r_C_23 : REAL := 0.254000;  r_C_24 : REAL := 0.000000;   r_C_25 : REAL := 0.012500;  r_C_26 : REAL := 0.500000;
    r_C_31 : REAL := 1.000000;  r_C_32 : REAL := 0.154000;   r_C_33 : REAL := 0.985000;  r_C_34 : REAL := -0.025000;  r_C_35 : REAL := -0.085000; r_C_36 : REAL := 0.000000;
    r_C_41 : REAL := -0.045000; r_C_42 : REAL := -0.012000;  r_C_43 : REAL := 0.000000;  r_C_44 : REAL := 0.085000;   r_C_45 : REAL := 1.000000;  r_C_46 : REAL := -0.024000;

    (* Direct Feedthrough Matrix D [4x5] *)
    r_D_11 : REAL := 15.420000; r_D_12 : REAL := 15.420000; r_D_13 : REAL := 2.850000;  r_D_14 : REAL := 0.450000;  r_D_15 : REAL := -1.250000;
    r_D_21 : REAL := 0.452000;  r_D_22 : REAL := 0.452000;  r_D_23 : REAL := 0.000000;  r_D_24 : REAL := 0.000000;  r_D_25 : REAL := 0.000000;
    r_D_31 : REAL := 0.000000;  r_D_32 : REAL := 0.000000;  r_D_33 : REAL := 0.000000;  r_D_34 : REAL := 0.000000;  r_D_35 : REAL := 0.000000;
    r_D_41 : REAL := 0.000000;  r_D_42 : REAL := 0.000000;  r_D_43 : REAL := 0.000000;  r_D_44 : REAL := 0.000000;  r_D_45 : REAL := -0.852000;

    (* Discrete Kalman Innovation Gain Matrix L [6x4] *)
    r_L_11 : REAL := 0.000452; r_L_12 : REAL := 0.024510; r_L_13 : REAL := 0.185420; r_L_14 : REAL := -0.000852;
    r_L_21 : REAL := 0.001854; r_L_22 : REAL := 0.142580; r_L_23 : REAL := 0.045210; r_L_24 : REAL := -0.000412;
    r_L_31 : REAL := 0.000125; r_L_32 : REAL := 0.008450; r_L_33 : REAL := 0.254180; r_L_34 : REAL := 0.000000;
    r_L_41 : REAL := 0.000285; r_L_42 : REAL := -0.002150; r_L_43 : REAL := -0.008520; r_L_44 : REAL := 0.015420;
    r_L_51 : REAL := -0.000085; r_L_52 : REAL := 0.000420; r_L_53 : REAL := -0.014520; r_L_54 : REAL := 0.195420;
    r_L_61 : REAL := 0.000625; r_L_62 : REAL := 0.045210; r_L_63 : REAL := 0.000000; r_L_64 : REAL := -0.000542;

    (* State Vector Registers *)
    r_x_hat_1 : REAL := 0.0; (* Exit slab thickness gauge error [um] *)
    r_x_hat_2 : REAL := 0.0; (* Mill stand roll gap dynamic deflection [um] *)
    r_x_hat_3 : REAL := 0.0; (* Roll eccentricity harmonic error [um] *)
    r_x_hat_4 : REAL := 0.0; (* Main drive roll speed mismatch [rpm] *)
    r_x_hat_5 : REAL := 0.0; (* Slab surface temperature gradient error [deg C] *)
    r_x_hat_6 : REAL := 0.0; (* Hydraulic screwdown differential cylinder tilt [um] *)

    r_x_pred_1 : REAL := 0.0; r_x_pred_2 : REAL := 0.0; r_x_pred_3 : REAL := 0.0;
    r_x_pred_4 : REAL := 0.0; r_x_pred_5 : REAL := 0.0; r_x_pred_6 : REAL := 0.0;

    r_y_pred_1 : REAL := 0.0; r_y_pred_2 : REAL := 0.0; r_y_pred_3 : REAL := 0.0; r_y_pred_4 : REAL := 0.0;
    r_innov_1  : REAL := 0.0; r_innov_2  : REAL := 0.0; r_innov_3  : REAL := 0.0; r_innov_4  : REAL := 0.0;

    (* Control Input Vector Registers *)
    r_u_cmd_1 : REAL := 0.0; (* Operator-side hydraulic servo [%] *)
    r_u_cmd_2 : REAL := 0.0; (* Drive-side hydraulic servo [%] *)
    r_u_cmd_3 : REAL := 0.0; (* Work roll bending valve [bar] *)
    r_u_cmd_4 : REAL := 0.0; (* Main drive twin-motor speed [rpm] *)
    r_u_cmd_5 : REAL := 0.0; (* High-pressure descaling header [%] *)

    r_u_prev_1 : REAL := 0.0; r_u_prev_2 : REAL := 0.0; r_u_prev_3 : REAL := 0.0;
    r_u_prev_4 : REAL := 0.0; r_u_prev_5 : REAL := 0.0;

    (* ========================================================================================== *)
    (* SECTION 2: MODEL PREDICTIVE CONTROL (MPC) PARAMETERS & PGD OPTIMIZATION                    *)
    (* ========================================================================================== *)
    (* State Penalty Diagonal Matrix Q [6x6] *)
    r_Q_diag_1 : REAL := 25.0;  (* Gauge tracking penalty *)
    r_Q_diag_2 : REAL := 15.0;  (* Mill deflection penalty *)
    r_Q_diag_3 : REAL := 40.0;  (* Roll eccentricity suppression penalty *)
    r_Q_diag_4 : REAL := 30.0;  (* Speed mismatch / chatter penalty *)
    r_Q_diag_5 : REAL := 8.0;   (* Thermal gradient uniformity penalty *)
    r_Q_diag_6 : REAL := 50.0;  (* Cylinder differential tilt / wedge penalty *)

    (* Actuator Penalty Diagonal Matrix R [5x5] *)
    r_R_diag_1 : REAL := 1.2;   (* OS servo energy *)
    r_R_diag_2 : REAL := 1.2;   (* DS servo energy *)
    r_R_diag_3 : REAL := 0.8;   (* Bending pressure energy *)
    r_R_diag_4 : REAL := 0.5;   (* Main drive speed energy *)
    r_R_diag_5 : REAL := 0.3;   (* Descaling water energy *)

    (* Actuator Slew Rate Penalty Diagonal Matrix S [5x5] *)
    r_S_diag_1 : REAL := 4.5;   (* OS servo slew penalty *)
    r_S_diag_2 : REAL := 4.5;   (* DS servo slew penalty *)
    r_S_diag_3 : REAL := 2.5;   (* Bending slew penalty *)
    r_S_diag_4 : REAL := 1.5;   (* Drive speed slew penalty *)
    r_S_diag_5 : REAL := 0.5;   (* Descale valve slew penalty *)

    (* Terminal State Penalty Diagonal Matrix P [6x6] *)
    r_P_diag_1 : REAL := 35.0; r_P_diag_2 : REAL := 20.0; r_P_diag_3 : REAL := 60.0;
    r_P_diag_4 : REAL := 45.0; r_P_diag_5 : REAL := 12.0; r_P_diag_6 : REAL := 75.0;

    (* PGD Step Size and Slew Bounds *)
    r_PGD_Alpha_Step         : REAL := 0.045;  (* Gradient step size *)
    r_Max_Servo_Slew_Rate    : REAL := 250.0;  (* Max hydraulic servo change [%/s] *)
    r_Max_Bending_Slew_Rate  : REAL := 120.0;  (* Max roll bending change [bar/s] *)
    r_Max_Speed_Slew_Rate    : REAL := 25.0;   (* Max main motor acceleration [rpm/s] *)
    r_Max_Desc_Slew_Rate     : REAL := 100.0;  (* Max descaling valve change [%/s] *)
    r_Max_Allowable_Tilt     : REAL := 450.0;  (* Maximum hydraulic cylinder differential tilt [um] *)
    r_Anti_Cavitation_Min_P  : REAL := 15.0;   (* Minimum hydraulic backpressure to prevent cavitation [bar] *)

    (* Gradient Vector Variables for 10 Unrolled PGD Iterations *)
    r_grad_1 : REAL := 0.0; r_grad_2 : REAL := 0.0; r_grad_3 : REAL := 0.0;
    r_grad_4 : REAL := 0.0; r_grad_5 : REAL := 0.0;
    r_u_cand_1 : REAL := 0.0; r_u_cand_2 : REAL := 0.0; r_u_cand_3 : REAL := 0.0;
    r_u_cand_4 : REAL := 0.0; r_u_cand_5 : REAL := 0.0;
    r_delta_u_1 : REAL := 0.0; r_delta_u_2 : REAL := 0.0; r_delta_u_3 : REAL := 0.0;
    r_delta_u_4 : REAL := 0.0; r_delta_u_5 : REAL := 0.0;
    r_mpc_cost_total : REAL := 0.0;

    (* ========================================================================================== *)
    (* SECTION 3: 4-CHANNEL 2oo3 TMR VOTING VARIABLES & DEBOUNCE TIMERS                           *)
    (* ========================================================================================== *)
    (* Channel 1: Rolling Force 2oo3 TMR *)
    b_TMR_Ch1_PairAB_Mismatch  : BOOL := FALSE;
    b_TMR_Ch1_PairBC_Mismatch  : BOOL := FALSE;
    b_TMR_Ch1_PairAC_Mismatch  : BOOL := FALSE;
    r_TMR_Ch1_Timer_AB_ms      : REAL := 0.0;
    r_TMR_Ch1_Timer_BC_ms      : REAL := 0.0;
    r_TMR_Ch1_Timer_AC_ms      : REAL := 0.0;
    ui_TMR_Ch1_Health_State    : UINT := 3; (* 3=2oo3 healthy, 2=1oo2 degraded, 1=1oo1 single, 0=Failed *)
    r_TMR_Ch1_Voted_Value      : REAL := 0.0;
    r_TMR_Ch1_Tolerance_kN     : REAL := 850.0; (* Max allowable discrepancy between force sensors [kN] *)

    (* Channel 2: Hydraulic AGC Pressure 2oo3 TMR *)
    b_TMR_Ch2_PairAB_Mismatch  : BOOL := FALSE;
    b_TMR_Ch2_PairBC_Mismatch  : BOOL := FALSE;
    b_TMR_Ch2_PairAC_Mismatch  : BOOL := FALSE;
    r_TMR_Ch2_Timer_AB_ms      : REAL := 0.0;
    r_TMR_Ch2_Timer_BC_ms      : REAL := 0.0;
    r_TMR_Ch2_Timer_AC_ms      : REAL := 0.0;
    ui_TMR_Ch2_Health_State    : UINT := 3;
    r_TMR_Ch2_Voted_Value      : REAL := 0.0;
    r_TMR_Ch2_Tolerance_bar    : REAL := 18.0; (* Max allowable discrepancy in AGC pressure [bar] *)

    (* Channel 3: Motor Armature Current 2oo3 TMR *)
    b_TMR_Ch3_PairAB_Mismatch  : BOOL := FALSE;
    b_TMR_Ch3_PairBC_Mismatch  : BOOL := FALSE;
    b_TMR_Ch3_PairAC_Mismatch  : BOOL := FALSE;
    r_TMR_Ch3_Timer_AB_ms      : REAL := 0.0;
    r_TMR_Ch3_Timer_BC_ms      : REAL := 0.0;
    r_TMR_Ch3_Timer_AC_ms      : REAL := 0.0;
    ui_TMR_Ch3_Health_State    : UINT := 3;
    r_TMR_Ch3_Voted_Value      : REAL := 0.0;
    r_TMR_Ch3_Tolerance_kA     : REAL := 0.35; (* Max allowable discrepancy in motor current [kA] *)

    (* Channel 4: Descaling Pressure 2oo3 TMR *)
    b_TMR_Ch4_PairAB_Mismatch  : BOOL := FALSE;
    b_TMR_Ch4_PairBC_Mismatch  : BOOL := FALSE;
    b_TMR_Ch4_PairAC_Mismatch  : BOOL := FALSE;
    r_TMR_Ch4_Timer_AB_ms      : REAL := 0.0;
    r_TMR_Ch4_Timer_BC_ms      : REAL := 0.0;
    r_TMR_Ch4_Timer_AC_ms      : REAL := 0.0;
    ui_TMR_Ch4_Health_State    : UINT := 3;
    r_TMR_Ch4_Voted_Value      : REAL := 0.0;
    r_TMR_Ch4_Tolerance_bar    : REAL := 22.0; (* Max allowable discrepancy in descaling pressure [bar] *)

    r_TMR_Persistence_Limit_ms : REAL := 50.0; (* Debounce timer threshold [ms] *)
    r_Loop_Sample_Time_ms      : REAL := 0.5;  (* Loop sample period 500 us = 0.5 ms *)

    (* ========================================================================================== *)
    (* SECTION 4: PRODUCTION FINITE STATE MACHINE (FSM) VARIABLES                                 *)
    (* ========================================================================================== *)
    ui_FSM_State_Current       : UINT := 0;
    ui_FSM_State_Next          : UINT := 0;
    ui_FSM_SubState            : UINT := 0;
    r_FSM_Stage_Timer_s        : REAL := 0.0;
    r_Slab_Bite_Timer_s        : REAL := 0.0;
    r_Slab_In_Mill_Length_m    : REAL := 0.0;
    r_Calculated_Rolling_Speed : REAL := 0.0;
    r_Target_Gap_Pass_1        : REAL := 195.0; (* Pass 1 nominal roll gap [mm] *)
    r_Target_Gap_Pass_2        : REAL := 142.0; (* Pass 2 nominal roll gap [mm] *)
    r_Target_Gap_Pass_3        : REAL := 95.0;  (* Pass 3 nominal roll gap [mm] *)
    r_Target_Gap_Pass_4        : REAL := 58.0;  (* Pass 4 nominal roll gap [mm] *)
    r_Target_Gap_Pass_5        : REAL := 32.0;  (* Pass 5 nominal roll gap [mm] *)
    r_Target_Gap_Pass_6        : REAL := 24.0;  (* Pass 6 optional [mm] *)
    r_Target_Gap_Pass_7        : REAL := 18.0;  (* Pass 7 optional [mm] *)
    r_Edger_Width_Pass_1       : REAL := 1485.0;(* Pass 1 edger target width [mm] *)
    r_Edger_Width_Pass_2       : REAL := 1475.0;(* Pass 2 edger target width [mm] *)
    r_Edger_Width_Pass_3       : REAL := 1465.0;(* Pass 3 edger target width [mm] *)
    r_Edger_Width_Pass_4       : REAL := 1455.0;(* Pass 4 edger target width [mm] *)
    r_Edger_Width_Pass_5       : REAL := 1450.0;(* Pass 5 edger target width [mm] *)
    r_Bite_Force_Threshold_kN  : REAL := 2500.0;(* Rolling force threshold indicating strip in bite [kN] *)
    r_Tail_Out_Force_Threshold : REAL := 1200.0;(* Rolling force threshold indicating strip tail out [kN] *)
    b_Forward_Direction_Latched: BOOL := TRUE;
    r_Reversing_Decel_Distance : REAL := 0.0;
    b_Crop_Shear_Executed_Head : BOOL := FALSE;
    b_Crop_Shear_Executed_Tail : BOOL := FALSE;

    (* ========================================================================================== *)
    (* SECTION 5: ANSI/ISA-18.2 ALARM ENGINE REGISTERS (8 MONITORED ANALOG LOOPS)                 *)
    (* ========================================================================================== *)
    (* Loop 1: Total Rolling Force [kN] *)
    r_Trip_Force_HH            : REAL := 52000.0; (* High-High rolling force trip [kN] *)
    r_Trip_Force_H             : REAL := 46000.0; (* High warning rolling force [kN] *)
    r_Trip_Force_L             : REAL := 2200.0;  (* Low warning rolling force during bite [kN] *)
    r_Trip_Force_LL            : REAL := 800.0;   (* Low-Low lost bite trip [kN] *)
    r_Deadband_Force_kN        : REAL := 500.0;   (* Force hysteresis deadband [kN] *)
    b_Alarm_Force_HH_Latched   : BOOL := FALSE;
    b_Alarm_Force_H_Active     : BOOL := FALSE;
    b_Alarm_Force_L_Active     : BOOL := FALSE;
    b_Alarm_Force_LL_Latched   : BOOL := FALSE;
    r_Timer_Force_HH_ms        : REAL := 0.0;
    r_Timer_Force_LL_ms        : REAL := 0.0;

    (* Loop 2: Hydraulic AGC Pressure [bar] *)
    r_Trip_Press_AGC_HH        : REAL := 285.0;   (* High-High relief valve blowoff risk [bar] *)
    r_Trip_Press_AGC_H         : REAL := 260.0;   (* High pressure warning [bar] *)
    r_Trip_Press_AGC_L         : REAL := 45.0;    (* Low pressure warning [bar] *)
    r_Trip_Press_AGC_LL        : REAL := 18.0;    (* Low-Low cavitation collapse trip [bar] *)
    r_Deadband_Press_bar       : REAL := 4.0;     (* Hydraulic pressure deadband [bar] *)
    b_Alarm_Press_AGC_HH_Latched: BOOL := FALSE;
    b_Alarm_Press_AGC_H_Active : BOOL := FALSE;
    b_Alarm_Press_AGC_L_Active : BOOL := FALSE;
    b_Alarm_Press_AGC_LL_Latched: BOOL := FALSE;
    r_Timer_Press_AGC_HH_ms    : REAL := 0.0;
    r_Timer_Press_AGC_LL_ms    : REAL := 0.0;

    (* Loop 3: Slab Exit Temperature [deg C] *)
    r_Trip_Temp_HH             : REAL := 1320.0;  (* High-High scale burning [deg C] *)
    r_Trip_Temp_H              : REAL := 1280.0;  (* High temperature warning [deg C] *)
    r_Trip_Temp_L              : REAL := 1020.0;  (* Low temperature rolling resistance warning [deg C] *)
    r_Trip_Temp_LL             : REAL := 960.0;   (* Low-Low cold slab roll break risk trip [deg C] *)
    r_Deadband_Temp_degC       : REAL := 15.0;    (* Temperature deadband [deg C] *)
    b_Alarm_Temp_HH_Latched    : BOOL := FALSE;
    b_Alarm_Temp_H_Active      : BOOL := FALSE;
    b_Alarm_Temp_L_Active      : BOOL := FALSE;
    b_Alarm_Temp_LL_Latched    : BOOL := FALSE;
    r_Timer_Temp_HH_ms         : REAL := 0.0;
    r_Timer_Temp_LL_ms         : REAL := 0.0;

    (* Loop 4: Main Drive Motor Armature Current [kA] *)
    r_Trip_Current_HH          : REAL := 4.8;     (* High-High motor stall overcurrent trip [kA] *)
    r_Trip_Current_H           : REAL := 4.0;     (* High motor thermal overload warning [kA] *)
    r_Trip_Current_L           : REAL := 0.25;    (* Low motor current underbite [kA] *)
    r_Trip_Current_LL          : REAL := 0.05;    (* Low-Low coupling disconnect trip [kA] *)
    r_Deadband_Current_kA      : REAL := 0.15;    (* Armature current deadband [kA] *)
    b_Alarm_Current_HH_Latched : BOOL := FALSE;
    b_Alarm_Current_H_Active   : BOOL := FALSE;
    b_Alarm_Current_L_Active   : BOOL := FALSE;
    b_Alarm_Current_LL_Latched : BOOL := FALSE;
    r_Timer_Current_HH_ms      : REAL := 0.0;
    r_Timer_Current_LL_ms      : REAL := 0.0;

    (* Loop 5: Work Roll Bending Pressure [bar] *)
    r_Trip_Bending_HH          : REAL := 290.0;   (* High-High roll bending seal burst trip [bar] *)
    r_Trip_Bending_H           : REAL := 250.0;   (* High bending pressure warning [bar] *)
    r_Trip_Bending_L           : REAL := 25.0;    (* Low bending pressure warning [bar] *)
    r_Trip_Bending_LL          : REAL := 8.0;     (* Low-Low roll balancing lost trip [bar] *)
    r_Deadband_Bending_bar     : REAL := 5.0;     (* Bending pressure deadband [bar] *)
    b_Alarm_Bending_HH_Latched : BOOL := FALSE;
    b_Alarm_Bending_H_Active   : BOOL := FALSE;
    b_Alarm_Bending_L_Active   : BOOL := FALSE;
    b_Alarm_Bending_LL_Latched : BOOL := FALSE;
    r_Timer_Bending_HH_ms      : REAL := 0.0;
    r_Timer_Bending_LL_ms      : REAL := 0.0;

    (* Loop 6: Descaling Header Pressure [bar] *)
    r_Trip_Desc_HH             : REAL := 295.0;   (* High-High header nozzle overpressure [bar] *)
    r_Trip_Desc_H              : REAL := 275.0;   (* High descaling pressure warning [bar] *)
    r_Trip_Desc_L              : REAL := 210.0;   (* Low descaling pressure warning [bar] *)
    r_Trip_Desc_LL             : REAL := 160.0;   (* Low-Low descaling pump cavitation trip [bar] *)
    r_Deadband_Desc_bar        : REAL := 8.0;     (* Descaling pressure deadband [bar] *)
    b_Alarm_Desc_HH_Latched    : BOOL := FALSE;
    b_Alarm_Desc_H_Active      : BOOL := FALSE;
    b_Alarm_Desc_L_Active      : BOOL := FALSE;
    b_Alarm_Desc_LL_Latched    : BOOL := FALSE;
    r_Timer_Desc_HH_ms         : REAL := 0.0;
    r_Timer_Desc_LL_ms         : REAL := 0.0;

    (* Loop 7: Roll Gap Differential Tilt Error [um] *)
    r_Trip_Tilt_HH             : REAL := 550.0;   (* High-High dangerous strip wedging trip [um] *)
    r_Trip_Tilt_H              : REAL := 350.0;   (* High tilt asymmetry warning [um] *)
    r_Trip_Tilt_L              : REAL := -350.0;  (* Low tilt asymmetry warning [um] *)
    r_Trip_Tilt_LL             : REAL := -550.0;  (* Low-Low dangerous reverse wedging trip [um] *)
    r_Deadband_Tilt_um         : REAL := 30.0;    (* Tilt deadband [um] *)
    b_Alarm_Tilt_HH_Latched    : BOOL := FALSE;
    b_Alarm_Tilt_H_Active      : BOOL := FALSE;
    b_Alarm_Tilt_L_Active      : BOOL := FALSE;
    b_Alarm_Tilt_LL_Latched    : BOOL := FALSE;
    r_Timer_Tilt_HH_ms         : REAL := 0.0;
    r_Timer_Tilt_LL_ms         : REAL := 0.0;

    (* Loop 8: Mill Stand Vibration / Roll Chatter Spectral Power [g] *)
    r_Trip_Chatter_HH          : REAL := 0.65;    (* High-High 3rd octave destructive chatter trip [g] *)
    r_Trip_Chatter_H           : REAL := 0.40;    (* High chatter harmonic resonance warning [g] *)
    r_Trip_Chatter_L           : REAL := 0.08;    (* Low sensor threshold [g] *)
    r_Trip_Chatter_LL          : REAL := 0.01;    (* Low-Low sensor disconnect [g] *)
    r_Deadband_Chatter_g       : REAL := 0.03;    (* Chatter deadband [g] *)
    b_Alarm_Chatter_HH_Latched : BOOL := FALSE;
    b_Alarm_Chatter_H_Active   : BOOL := FALSE;
    b_Alarm_Chatter_L_Active   : BOOL := FALSE;
    b_Alarm_Chatter_LL_Latched : BOOL := FALSE;
    r_Timer_Chatter_HH_ms      : REAL := 0.0;
    r_Timer_Chatter_LL_ms      : REAL := 0.0;

    (* First-Out Sequence Latching *)
    ui_First_Out_Alarm_Code    : UINT := 0;
    r_First_Out_Timestamp_ms   : REAL := 0.0;
    r_Master_Cycle_Counter     : REAL := 0.0;

    (* Mechanical Constants & Physics Auxiliary Registers *)
    r_Mill_Modulus_Constant_Mm : REAL := 9850.0;  (* Mill housing modulus [kN/mm] *)
    r_Nominal_NoLoad_Gap_S0    : REAL := 65.0;    (* Base mechanical zero datum [mm] *)
    r_WorkRoll_Radius_Nominal  : REAL := 590.0;   (* Work roll radius [mm] *)
    r_BackupRoll_Radius_Nominal: REAL := 800.0;   (* Backup roll radius [mm] *)
    r_Youngs_Modulus_Rolls     : REAL := 210000.0;(* Steel elastic modulus [MPa] *)
    r_Poissons_Ratio_Rolls     : REAL := 0.29;    (* Steel Poisson ratio *)
    r_Friction_Coefficient_Bite: REAL := 0.32;    (* Hot steel/roll friction coefficient *)
    r_Yield_Strength_Flow_Hot  : REAL := 85.0;    (* High temperature steel yield stress [MPa] *)
    r_Thermal_Expansion_Coeff  : REAL := 0.000012;(* Roll thermal expansion [1/deg C] *)
    r_Roll_Heating_DeltaT      : REAL := 35.0;    (* Average roll thermal equilibrium delta [deg C] *)
    r_Calculated_R_Prime       : REAL := 590.0;   (* Hitchcock flattened roll radius [mm] *)
    r_Neutral_Bite_Angle_rad   : REAL := 0.085;   (* Roll bite neutral point angle [rad] *)
    r_Forward_Slip_Ratio       : REAL := 0.042;   (* Forward slip ratio [(v_strip - v_roll)/v_roll] *)
    r_Sims_Qp_Factor           : REAL := 1.38;    (* Sims hot rolling geometric friction factor *)
    r_Calculated_Rolling_Torque: REAL := 0.0;     (* Calculated rolling spindle torque [kNm] *)
    r_Calculated_Motor_Power_kW: REAL := 0.0;     (* Instantaneous mechanical power consumed [kW] *)
END_VAR
