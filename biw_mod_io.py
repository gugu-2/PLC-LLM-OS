# -*- coding: utf-8 -*-
"""
Module: biw_mod_io.py
Generates the comprehensive IEC 61131-3 Function Block Header, VAR_INPUT, and VAR_OUTPUT blocks
for FB_Automotive_BIW_GeoFraming_MultiRobotWelding.
"""

def get_header_and_io() -> str:
    lines = [
        "FUNCTION_BLOCK FB_Automotive_BIW_GeoFraming_MultiRobotWelding",
        "(*",
        " ====================================================================================================",
        "  LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - ULTRA-RIGOROUS SYNTHETIC DATASET V7 MAX-PERSONA",
        "  DOMAIN: AUTOMOTIVE BODY-IN-WHITE (BIW) MANUFACTURING (INDUSTRY RANK #1 - HIGHEST GLOBAL PLC DEMAND)",
        "  SYSTEM: HIGH-SPEED AUTOMOTIVE FLEXIBLE BIW GEO-FRAMING STATION: 14-ROBOT COORDINATED MULTI-SPOT &",
        "          LASER SEAM WELDING JIG (45.0 s CYCLE TIME, 0.05 mm STRUCTURAL BODY FRAMING TOLERANCE),",
        "          MULTI-MODEL ROLLER SKID CONVEYOR LIFTER PACING (PAYLOAD 1,850 kg), DYNAMIC SERVO WELDING GUN",
        "          ADAPTIVE RESISTANCE & EXPULSION FEEDBACK (14.5 kA WELD CURRENT, 4.5 kN TIP FORCE), PNEUMATIC",
        "          CLAMP SEQUENCE MONITORING WITH INDUCTIVE DUAL-CHANNEL DISCREPANCY, AND ISO 13849 PL e /",
        "          IEC 62061 SIL-3 SAFETY LIGHT CURTAIN ZONE MUTING INTERLOCKS.",
        " ====================================================================================================",
        "  APPLICABLE INDUSTRIAL CODES, NORMS, AND ARCHITECTURAL STANDARDS:",
        "   - ISO 13849-1 / IEC 62061: Functional safety of machinery (Category 4, PL e, SIL-3 safety circuits).",
        "   - ISO 12100: Safety of machinery - General principles for design, risk assessment and risk reduction.",
        "   - AWS D8.1M / D8.9M: Recommended practices for automotive weld quality evaluation & test procedures.",
        "   - ISO 14373 / ISO 18278: Resistance welding - Procedure for spot welding of low carbon and high strength steels.",
        "   - ISO 15609-4 / ISO 15614-11: Specification and qualification of welding procedures for laser beam welding.",
        "   - ISA-18.2 / IEC 62682: Management of alarm systems for process and industrial automation industries.",
        "   - IEC 61131-3 3rd Edition: Programmable controllers - Programming languages (Structured Text ST).",
        " ====================================================================================================",
        "  CYBER-PHYSICAL CORE SUBSYSTEM ARCHITECTURE:",
        "   1. MULTI-MODEL ROLLER SKID FRICTION CONVEYOR & 4-CORNER SYNCHRONOUS LIFTER:",
        "      - Paced transport of 1,850 kg vehicle underbody + 650 kg rigid palletized skid (2,500 kg total payload).",
        "      - Friction roller drive with dual-frequency variable speed vector inverter (0.0 to 1.5 m/s).",
        "      - Heavy-duty hydraulic/servo 4-corner eccentric lifter table lifting body 650.0 mm into framing datum.",
        "      - Laser position encoder triplets (ZT_SKID_LIFTER_POS_101A/B/C) with 0.5 mm discrepancy tolerance.",
        "   2. RIGID GEO-FRAMING SIDE GATE CLAMPING TOWERS & WEDGE-PIN DOCKING JIG:",
        "      - Left and Right structural framing side gates (3,500 kg each) docking into precision NC locating datum.",
        "      - 4-point heavy pneumatic wedge-pin locks establishing rigid framing geometric envelope (0.05 mm limit).",
        "      - Dual inductive proximity switches per clamp cylinder (ZT_CLAMP_CYLINDER_RETRACT/ADVANCE 302/303).",
        "      - Mechanical compliance & elastic tower rebound observer under high-speed multi-robot weld forces.",
        "   3. 14-ROBOT COORDINATED INTERFERENCE ZONE KINEMATIC SYNCHRONIZATION:",
        "      - 8 Spot Welding Robots (R01..R08) with 7th-axis integrated servo welding guns (MFDC 1,000 Hz inverters).",
        "      - 2 Laser Seam Brazing Robots (R09..R10) for continuous roof seam joining (4.8 kW Nd:YAG / Fiber laser).",
        "      - 4 Respot & Underbody Reinforcement Robots (R11..R14) operating in dense cross-axis collision zones.",
        "      - 14x14 dynamic cross-axis mutual exclusion zone interlock matrix preventing mechanical robot collisions.",
        "   4. ADAPTIVE RESISTANCE SPOT WELDING & EXPULSION SPATTER FEEDBACK OBSERVER:",
        "      - Dynamic sheet contact resistance curve tracking R(t) = V(t) / I(t) at 2 ms resolution.",
        "      - Real-time Joulean energy integration: Q(t) = Integral(I^2 * R * dt) [kJ].",
        "      - High-speed negative dR/dt derivative spike and piezoelectric tip force dip detection for expulsion spatter.",
        "      - Closed-loop adaptive current scaling and dynamic tip squeeze force regulation to suppress spatter.",
        "   5. CONTINUOUS ROOF SEAM LASER BRAZING OPTICAL TRACKING CONTROLLER:",
        "      - High-frequency optical laser triangulation seam tracker (OPT_LASER_SEAM_TRACKER_501A/B/C) at 0.04 mm limit.",
        "      - Coordinated laser power modulation (0.0 to 5.0 kW) and cold wire feed velocity pacing (0.0 to 4.0 m/min).",
        "   6. TRIPLE MODULAR REDUNDANCY (2oo3 TMR) TRANSDUCER VOTING & HEALTH SUITE:",
        "      - 11 critical sensor triplets with configurable discrepancy debounce timers and bumpless auto-degradation.",
        "   7. 8x8 DISCRETE MULTIVARIABLE STATE-SPACE PROPAGATION & RECEDING-HORIZON MPC:",
        "      - Full 8x8 state-space formulation at 2 ms cycle time modeling electrical, thermal, and mechanical dynamics.",
        "      - Receding-horizon MPC with projected gradient descent quadratic cost optimization.",
        "   8. 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) & ISA-18.2 ALARM ENGINE:",
        "      - Deterministic sequencing from skid ingress, pin lift, clamping, 14-robot welding, brazing, to exit.",
        "      - 5-tier alarm hierarchy (HI_HI, HI, LO, LO_LO, ROC) packed into 4 industrial diagnostic status words.",
        " ====================================================================================================",
        "*)"
    ]

    # VAR_INPUT
    lines.append("VAR_INPUT")
    lines.append("    (* =========================================================================================== *)")
    lines.append("    (* 1.0 SUPERVISORY COMMANDS, MASTER PERMISSIVES & SYSTEM TIMING                                *)")
    lines.append("    (* =========================================================================================== *)")
    lines.append("    bMasterEnable                       : BOOL := FALSE;        (* Master station enable permissive *)")
    lines.append("    bSafetyCircuitOK                    : BOOL := FALSE;        (* Category 4 / PL e safety circuit status *)")
    lines.append("    bAlarmReset                         : BOOL := FALSE;        (* Operator alarm acknowledge and reset pulse *)")
    lines.append("    bAutoCycleStart                     : BOOL := FALSE;        (* Supervisory automatic cycle start trigger *)")
    lines.append("    bManualMode                         : BOOL := FALSE;        (* Manual maintenance jog and override mode *)")
    lines.append("    iVehicleModelID                     : INT  := 1;            (* Active vehicle variant: 1=Sedan, 2=SUV, 3=EV *)")
    lines.append("    rCycleTime_s                        : REAL := 0.002;        (* PLC deterministic task scan period [s] *)")
    lines.append("")

    lines.append("    (* =========================================================================================== *)")
    lines.append("    (* 2.0 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR TRANSMITTER TRIPLETS                        *)")
    lines.append("    (* =========================================================================================== *)")
    lines.append("    (* 4-Corner Geo-Lifter Table Laser Distance Position Transmitters [mm] *)")
    lines.append("    ZT_SKID_LIFTER_POS_101A             : REAL := 0.0;          (* Skid Lifter Table Height Sensor Ch A [mm] *)")
    lines.append("    ZT_SKID_LIFTER_POS_101B             : REAL := 0.0;          (* Skid Lifter Table Height Sensor Ch B [mm] *)")
    lines.append("    ZT_SKID_LIFTER_POS_101C             : REAL := 0.0;          (* Skid Lifter Table Height Sensor Ch C [mm] *)")
    lines.append("")
    lines.append("    (* Heavy Roller Friction Conveyor Linear Velocity Radar/Encoders [m/s] *)")
    lines.append("    ST_ROLLER_CONVEYOR_VEL_102A         : REAL := 0.0;          (* Roller Conveyor Skid Velocity Ch A [m/s] *)")
    lines.append("    ST_ROLLER_CONVEYOR_VEL_102B         : REAL := 0.0;          (* Roller Conveyor Skid Velocity Ch B [m/s] *)")
    lines.append("    ST_ROLLER_CONVEYOR_VEL_102C         : REAL := 0.0;          (* Roller Conveyor Skid Velocity Ch C [m/s] *)")
    lines.append("")
    lines.append("    (* Primary MFDC Inverter Servo Weld Gun Current Rogowski Toroids [kA] *)")
    lines.append("    IT_SERVO_GUN_WELD_CURRENT_201A      : REAL := 0.0;          (* Primary Servo Gun Weld Current Ch A [kA] *)")
    lines.append("    IT_SERVO_GUN_WELD_CURRENT_201B      : REAL := 0.0;          (* Primary Servo Gun Weld Current Ch B [kA] *)")
    lines.append("    IT_SERVO_GUN_WELD_CURRENT_201C      : REAL := 0.0;          (* Primary Servo Gun Weld Current Ch C [kA] *)")
    lines.append("")
    lines.append("    (* Servo Gun Piezoelectric Dynamic Tip Force Transducers [kN] *)")
    lines.append("    WT_SERVO_GUN_TIP_FORCE_202A         : REAL := 0.0;          (* Servo Gun Dynamic Squeeze Force Ch A [kN] *)")
    lines.append("    WT_SERVO_GUN_TIP_FORCE_202B         : REAL := 0.0;          (* Servo Gun Dynamic Squeeze Force Ch B [kN] *)")
    lines.append("    WT_SERVO_GUN_TIP_FORCE_202C         : REAL := 0.0;          (* Servo Gun Dynamic Squeeze Force Ch C [kN] *)")
    lines.append("")
    lines.append("    (* Main Framing Pneumatic Header Pressure Transmitters [bar] *)")
    lines.append("    PT_PNEUMATIC_CLAMP_HEADER_301A      : REAL := 6.5;          (* Pneumatic Supply Header Pressure Ch A [bar] *)")
    lines.append("    PT_PNEUMATIC_CLAMP_HEADER_301B      : REAL := 6.5;          (* Pneumatic Supply Header Pressure Ch B [bar] *)")
    lines.append("    PT_PNEUMATIC_CLAMP_HEADER_301C      : REAL := 6.5;          (* Pneumatic Supply Header Pressure Ch C [bar] *)")
    lines.append("")
    lines.append("    (* Gate Clamp Cylinders Retracted Inductive Proximity Sensors [BOOL] *)")
    lines.append("    ZT_CLAMP_CYLINDER_RETRACT_302A      : BOOL := TRUE;         (* Framing Clamp Retract Inductive Ch A [BOOL] *)")
    lines.append("    ZT_CLAMP_CYLINDER_RETRACT_302B      : BOOL := TRUE;         (* Framing Clamp Retract Inductive Ch B [BOOL] *)")
    lines.append("    ZT_CLAMP_CYLINDER_RETRACT_302C      : BOOL := TRUE;         (* Framing Clamp Retract Inductive Ch C [BOOL] *)")
    lines.append("")
    lines.append("    (* Gate Clamp Cylinders Advanced / Locked Inductive Proximity Sensors [BOOL] *)")
    lines.append("    ZT_CLAMP_CYLINDER_ADVANCE_303A      : BOOL := FALSE;        (* Framing Clamp Advance Inductive Ch A [BOOL] *)")
    lines.append("    ZT_CLAMP_CYLINDER_ADVANCE_303B      : BOOL := FALSE;        (* Framing Clamp Advance Inductive Ch B [BOOL] *)")
    lines.append("    ZT_CLAMP_CYLINDER_ADVANCE_303C      : BOOL := FALSE;        (* Framing Clamp Advance Inductive Ch C [BOOL] *)")
    lines.append("")
    lines.append("    (* Zone 1 Perimeter Safety Light Curtain Dual OSSD Channels [BOOL] *)")
    lines.append("    OPT_LIGHT_CURTAIN_ZONE1_401A        : BOOL := TRUE;         (* Safety Light Curtain Zone 1 OSSD1 Ch A [BOOL] *)")
    lines.append("    OPT_LIGHT_CURTAIN_ZONE1_401B        : BOOL := TRUE;         (* Safety Light Curtain Zone 1 OSSD2 Ch B [BOOL] *)")
    lines.append("    OPT_LIGHT_CURTAIN_ZONE1_401C        : BOOL := TRUE;         (* Safety Light Curtain Zone 1 Auxiliary Ch C [BOOL] *)")
    lines.append("")
    lines.append("    (* Optical Roof Laser Seam Tracking Joint Gap Transmitters [mm] *)")
    lines.append("    OPT_LASER_SEAM_TRACKER_501A         : REAL := 0.0;          (* Optical Laser Seam Joint Gap Ch A [mm] *)")
    lines.append("    OPT_LASER_SEAM_TRACKER_501B         : REAL := 0.0;          (* Optical Laser Seam Joint Gap Ch B [mm] *)")
    lines.append("    OPT_LASER_SEAM_TRACKER_501C         : REAL := 0.0;          (* Optical Laser Seam Joint Gap Ch C [mm] *)")
    lines.append("")
    lines.append("    (* MFDC Inverter Transformer Cooling Water Temperature Transmitters [deg C] *)")
    lines.append("    TT_TRANSFORMER_WATER_COOL_601A      : REAL := 22.5;         (* Weld Transformer Water Cool Temp Ch A [deg C] *)")
    lines.append("    TT_TRANSFORMER_WATER_COOL_601B      : REAL := 22.5;         (* Weld Transformer Water Cool Temp Ch B [deg C] *)")
    lines.append("    TT_TRANSFORMER_WATER_COOL_601C      : REAL := 22.5;         (* Weld Transformer Water Cool Temp Ch C [deg C] *)")
    lines.append("")
    lines.append("    (* Servo Gun Secondary Water Circuit Flow Rate Transmitters [L/min] *)")
    lines.append("    FT_COOLING_WATER_FLOW_602A          : REAL := 15.0;         (* Servo Gun Cooling Water Flow Ch A [L/min] *)")
    lines.append("    FT_COOLING_WATER_FLOW_602B          : REAL := 15.0;         (* Servo Gun Cooling Water Flow Ch B [L/min] *)")
    lines.append("    FT_COOLING_WATER_FLOW_602C          : REAL := 15.0;         (* Servo Gun Cooling Water Flow Ch C [L/min] *)")
    lines.append("")

    lines.append("    (* =========================================================================================== *)")
    lines.append("    (* 3.0 PROCESS PARAMETERS, SETPOINTS & RECIPE BOUNDS                                           *)")
    lines.append("    (* =========================================================================================== *)")
    lines.append("    rWeldCurrentSetpoint_kA             : REAL := 14.5;         (* Target MFDC Spot Weld Current [kA] *)")
    lines.append("    rWeldTipForceSetpoint_kN            : REAL := 4.5;          (* Target Servo Tip Squeeze Force [kN] *)")
    lines.append("    rWeldSqueezeTime_ms                 : REAL := 120.0;        (* Pre-weld Mechanical Squeeze Duration [ms] *)")
    lines.append("    rWeldCurrentTime_ms                 : REAL := 240.0;        (* Active MFDC Inverter Current Duration [ms] *)")
    lines.append("    rWeldHoldTime_ms                    : REAL := 140.0;        (* Post-weld Solidification Hold Duration [ms] *)")
    lines.append("    rLaserPowerSetpoint_kW              : REAL := 4.8;          (* Continuous Roof Laser Brazing Power [kW] *)")
    lines.append("    rLaserWireFeedRate_mpm              : REAL := 3.2;          (* Laser Brazing Cold-Wire Feed Velocity [m/min] *)")
    lines.append("    rLaserBrazingLength_mm              : REAL := 1450.0;       (* Total Roof Seam Brazing Seam Length [mm] *)")
    lines.append("    rLifterTargetHeight_mm              : REAL := 650.0;        (* Geo-Framing Station Working Height [mm] *)")
    lines.append("    rLifterLowerHeight_mm               : REAL := 0.0;          (* Skid Roller Conveyor Ingress/Egress Height [mm] *)")
    lines.append("    rConveyorSpeedSetpoint_mps          : REAL := 0.85;         (* Paced Roller Skid Conveyor Speed [m/s] *)")
    lines.append("    rPneumaticHeaderPressureMin_bar     : REAL := 5.8;          (* Minimum Clamp Header Pressure Trip Limit [bar] *)")
    lines.append("    rCoolingWaterFlowMin_Lpm            : REAL := 12.0;         (* Minimum Gun Cooling Water Flow Interlock [L/min] *)")
    lines.append("    rTransformerTempMax_degC            : REAL := 55.0;         (* Maximum Weld Transformer Overheat Limit [deg C] *)")
    lines.append("")

    lines.append("    (* =========================================================================================== *)")
    lines.append("    (* 4.0 14 INDUSTRIAL ROBOT HANDSHAKE, HOME, AND INTERFERENCE SIGNALS                           *)")
    lines.append("    (* =========================================================================================== *)")
    for i in range(1, 15):
        r_id = f"{i:02d}"
        role = "Spot Weld" if i <= 8 else ("Laser Brazing" if i <= 10 else "Respot Underbody")
        lines.append(f"    bRobot{r_id}_InHomePos                  : BOOL := TRUE;         (* Robot {r_id} ({role}) Safe Home Position [BOOL] *)")
        lines.append(f"    bRobot{r_id}_WeldComplete               : BOOL := FALSE;        (* Robot {r_id} ({role}) Cycle Complete [BOOL] *)")
        lines.append(f"    bRobot{r_id}_InterferenceClear          : BOOL := TRUE;         (* Robot {r_id} ({role}) Zone Clear Flag [BOOL] *)")
    lines.append("    wRobotCollisionZoneOccupied         : WORD := 16#0000;      (* Real-Time Hardware Interference Zone Bitmask *)")
    lines.append("    bSkidPresentAtEntry                 : BOOL := FALSE;        (* Entry Optical Skid Ingress Photoeye [BOOL] *)")
    lines.append("    bSkidPresentAtExit                  : BOOL := FALSE;        (* Exit Optical Skid Clear Photoeye [BOOL] *)")
    lines.append("END_VAR")
    lines.append("")

    # VAR_OUTPUT
    lines.append("VAR_OUTPUT")
    lines.append("    (* =========================================================================================== *)")
    lines.append("    (* 1.0 ACTUATOR DRIVES, SERVO CONTROLLERS & PROCESS INTERFACE COMMANDS                         *)")
    lines.append("    (* =========================================================================================== *)")
    lines.append("    bLifterMotorRun                     : BOOL;                 (* Geo-Lifter Table Servo VFD Run Command *)")
    lines.append("    bLifterMotorDirectionUp             : BOOL;                 (* Geo-Lifter VFD Direction Command (TRUE=UP) *)")
    lines.append("    rLifterSpeedCommand_pct             : REAL;                 (* Geo-Lifter VFD Speed Frequency Command [%] *)")
    lines.append("    bConveyorMotorRun                   : BOOL;                 (* Paced Roller Skid Conveyor Drive Run Command *)")
    lines.append("    rConveyorSpeedCommand_mps           : REAL;                 (* Paced Roller Skid Conveyor Speed Command [m/s] *)")
    lines.append("    bClampCylinderAdvanceCmd            : BOOL;                 (* Framing Side Gate Clamps Advance Solenoid *)")
    lines.append("    bClampCylinderRetractCmd            : BOOL;                 (* Framing Side Gate Clamps Retract Solenoid *)")
    lines.append("    bGateLockPinsEngageCmd              : BOOL;                 (* Side Gate NC Precision Wedge Pins Lock Solenoid *)")
    lines.append("    bPneumaticHeaderDumpValveCmd        : BOOL;                 (* Fail-Safe Pneumatic Emergency Quick-Dump Valve *)")
    lines.append("    bServoGunElectrodeCloseCmd          : BOOL;                 (* Integrated 7th-Axis Servo Gun Electrode Close *)")
    lines.append("    rServoGunForceCommand_kN            : REAL;                 (* Dynamic Servo Gun Tip Force Command [kN] *)")
    lines.append("    bMFDCWeldTimerEnableCmd             : BOOL;                 (* Medium Frequency Inverter Weld Timer Fire Enable *)")
    lines.append("    rMFDCCurrentCommand_kA              : REAL;                 (* MFDC Inverter Adaptive Weld Current Command [kA] *)")
    lines.append("    bLaserBrazingEnableCmd              : BOOL;                 (* Optical Laser Beam Generator Emission Enable *)")
    lines.append("    rLaserPowerCommand_kW               : REAL;                 (* Continuous Modulated Laser Power Command [kW] *)")
    lines.append("    rLaserWireFeedCommand_mpm           : REAL;                 (* Laser Brazing Wire Feed Drive Speed [m/min] *)")
    lines.append("    bCoolingWaterBoosterPumpCmd         : BOOL;                 (* Secondary Cooling Water Booster Pump Contactor *)")
    lines.append("")

    lines.append("    (* =========================================================================================== *)")
    lines.append("    (* 2.0 14 ROBOT COORDINATED PERMISSIVES & SYNCHRONOUS OVERRIDE COMMANDS                        *)")
    lines.append("    (* =========================================================================================== *)")
    lines.append("    wRobotWeldPermitWord                : WORD;                 (* 14-Robot Master Welding Permissive Bitmask *)")
    lines.append("    wRobotInterferenceZoneRelease       : WORD;                 (* 14-Robot Mutually Exclusive Zone Release Bitmask *)")
    lines.append("    rRobotFeedrateOverride_pct          : REAL;                 (* Synchronized Kinematic Feedrate Scaling [%] *)")
    lines.append("")

    lines.append("    (* =========================================================================================== *)")
    lines.append("    (* 3.0 STATION PROCESS STATUS, METROLOGY & WELD QUALITY ASSESSMENT                             *)")
    lines.append("    (* =========================================================================================== *)")
    lines.append("    iCurrentState                       : INT;                  (* Current Active FSM State Code [10..999] *)")
    lines.append("    bStationInCycle                     : BOOL;                 (* Geo-Framing Station Cycle In Progress *)")
    lines.append("    bCycleComplete                      : BOOL;                 (* Geo-Framing 45.0 s Total Cycle Complete Pulse *)")
    lines.append("    rCurrentCycleElapsed_s              : REAL;                 (* Current Station Cycle Elapsed Timer [s] *)")
    lines.append("    rGeometricAlignmentError_mm         : REAL;                 (* Structural Body Framing Geometric Deviation [mm] *)")
    lines.append("    bExpulsionSpatterDetected           : BOOL;                 (* Real-Time Dynamic Resistance Expulsion Spatter Latched *)")
    lines.append("    rDynamicSheetResistance_mOhm        : REAL;                 (* Real-Time Sheet Contact & Bulk Resistance [mOhm] *)")
    lines.append("    rNuggetJouleanEnergy_kJ             : REAL;                 (* Total Spot Weld Joulean Heat Energy Input [kJ] *)")
    lines.append("    rEstimatedNuggetDiameter_mm         : REAL;                 (* AWS D8.1M Conformal Weld Nugget Size Estimate [mm] *)")
    lines.append("    bWeldingQualityPass                 : BOOL;                 (* Comprehensive Multi-Spot Weld Quality Flag *)")
    lines.append("    bLaserSeamQualityPass               : BOOL;                 (* Roof Seam Laser Brazing Continuous Quality Flag *)")
    lines.append("    bSafetyZoneTripped                  : BOOL;                 (* Safety Light Curtain Perimeter Violation Latched *)")
    lines.append("    bEmergencyHaltActive                : BOOL;                 (* ISO 13849 Category 4 / SIL-3 Emergency Stop Active *)")
    lines.append("")

    lines.append("    (* =========================================================================================== *)")
    lines.append("    (* 4.0 ISA-18.2 DIAGNOSTIC STATUS WORDS                                                        *)")
    lines.append("    (* =========================================================================================== *)")
    lines.append("    wDiagnosticWord01_Sensors           : WORD;                 (* Diagnostic Word 01: Sensor TMR Health & Discrepancies *)")
    lines.append("    wDiagnosticWord02_Actuators         : WORD;                 (* Diagnostic Word 02: Drives, Clamps & Tooling Alarms *)")
    lines.append("    wDiagnosticWord03_Quality           : WORD;                 (* Diagnostic Word 03: Weld Expulsion & Geometry Alarms *)")
    lines.append("    wDiagnosticWord04_SafetyFSM         : WORD;                 (* Diagnostic Word 04: Safety Interlocks & FSM States *)")
    lines.append("END_VAR")

    return "\n".join(lines)
