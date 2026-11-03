# build_biw_hemming.py
# Generates FB_Automotive_BIW_RoboticRollerHemming_Sealer in full mathematical detail
import uuid
import json
import re

USER_PROMPT = """You are generating a SINGLE ultra-dense IEC 61131-3 Structured Text dataset for the **Automotive Body-in-White (BIW)** industry.

**Domain**: Automotive Robotic BIW High-Speed Roller Hemming & Multi-Axis Sealer Dispensing Cell with 3D Optical Vision Part Offset Compensation.

**Function Block Name**: `FB_Automotive_BIW_RoboticRollerHemming_Sealer`

**Engineering Context**:
- Automotive closure assembly line (doors, hoods, tailgates) with twin 6-axis articulated hemming robots (Fanuc / Kuka 210 kg payload)
- High-speed 3-step roller hemming process (pre-hemming at 45°, intermediate hemming at 75°, final hemming at 90° flat)
- Multi-component mastic sealant bead dispensing (viscosity 80,000 mPa.s) with continuous volumetric encoder tracking
- Robot force-torque sensor (ATI 6-axis F/T transducer) maintaining constant hemming roller normal contact force (1,800 N ±50 N)
- Perceptron / Coherix 3D optical laser triangulation sensors verifying door flange gap, flushness, and roll-in tolerance (±0.2 mm)
- Vacuum suction gripper tooling table with servo-electric locating pin clamps and part seating proximity sensors
- ISO 10218-2 collaborative safety zone monitoring with dynamic robot envelope limiting (SafeMove / Dual Check Safety)

**Required Mathematical Rigor** (ALL must be explicitly coded with complete equations and matrix constants):
1. **Discrete State-Space Matrix Model** for hemming roller normal contact force & robot TCP tracking error:
   - State vector x = [roller_force_normal_N, flange_crease_depth_mm, sealer_bead_height_mm, tcp_path_offset_um]
   - Full numerical matrices A (4×4) and B (4×3 robot force offset / pump servo commands)
   - Dynamic propagation: x_{k+1} = A*x_k + B*u_k evaluated at 4ms deterministic fieldbus loop
2. **Model Predictive Control (MPC) Quadratic Cost Approximation**:
   - Roller normal force regulation across sheet metal curvature variations
   - Q matrix (4×4 force/crease error penalty) and R matrix (3×3 robot TCP slew penalty)
   - Terminal cost matrix P (4×4)
3. **2oo3 (Two-out-of-Three) Triple Modular Redundant (TMR) Voting**:
   - 3 optical laser triangulation sensors verifying door outer-to-inner hem roll-in
   - Discrepancy validation (0.15 mm) with automated optical air wipe purge cycle
4. **ISA-18.2 Multi-Tiered Alarm Ladder**:
   - Roller normal contact force: HH (2,250 N panel crushing trip), H (2,050 N), L (1,450 N loose hem warn), LL (1,100 N disengaged abort)
   - Sealer dispense pressure: HH (220 bar), H (185 bar), LL (45 bar air bubble fault)
   - Robot F/T sensor overload: HH (3,000 N emergency stop)
5. **Multi-Stage Finite State Machine (FSM)**:
   - States: CELL_IDLE (0) -> INNER_OUTER_PANEL_DOCK (10) -> VACUUM_CLAMP_ENGAGE (20) -> 3D_VISION_ALIGN_OFFSETS (30) -> MASTIC_SEALER_DISPENSE (40) -> FLANGE_PRE_HEM_45DEG (50) -> INTERMEDIATE_HEM_75DEG (60) -> FINAL_FLAT_HEM_90DEG (70) -> GAP_FLUSH_OPTICAL_AUDIT (80) -> PART_UNCLAMP_EJECT (90) -> ROLLER_FORCE_OVERLOAD_TRIP (99)

**Output Format**:
- Code fenced with TRIPLE backticks and `iec-st`: ` ```iec-st `
- First line: `FUNCTION_BLOCK FB_Automotive_BIW_RoboticRollerHemming_Sealer`
- Last line: `END_FUNCTION_BLOCK`
- Minimum length: 45,000 to 75,000+ characters of deeply engineered Structured Text.

Save output to `data/swarm_raw/agent_<uuid>.json` and reply: `EVOLUTION COMPLETE: Automotive BIW Robotic Roller Hemming Sealer`"""

def generate_st_code():
    sections = []
    
    # Header
    sections.append('''FUNCTION_BLOCK FB_Automotive_BIW_RoboticRollerHemming_Sealer
(*
====================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - ULTRA-HIGH FIDELITY IEC 61131-3 ST DATASET
  SYSTEM SPECIFICATION: CPS-AUT-BIW-HEM-SEAL-CELL-04 (REV 9.4)
  DOMAIN: AUTOMOTIVE BODY-IN-WHITE (BIW) CLOSURE MANUFACTURING
  CELL ASSET:
    Dual-Arm High-Speed Roller Hemming & Multi-Axis Mastic Sealer Dispensing Cell with 
    3D Optical Laser Triangulation Part Offset Compensation & Active Compliance Force Control.

  ARCHITECTURAL & KINEMATIC INTEGRATION:
    - Closure Line: Side Passenger Doors, Tailgate Liftgates, and Engine Hood Closures.
    - Sheet Metal Specifications:
        * Outer Skin Blank: 0.70 mm BH210 Bake-Hardened Steel / 6111-T4 Aluminum Alloy.
        * Inner Frame Blank: 0.80 mm CR4 Mild Deep-Drawing Carbon Steel / 5182-O Aluminum.
        * Nominal Total Flange Pack Thickness: 1.50 mm.
        * Target Final Flattened Hem Thickness: 2.15 mm +/- 0.08 mm (Elongation < 18%).
    - Articulated Manipulators:
        * Twin KUKA KR210 R2700 / FANUC M-900iB/280L Heavy-Duty Articulated Robots.
        * ISO 10218-2 Collaborative Safety Architecture with SafeMove / Dual Check Safety (DCS).
    - End-Effector Tooling:
        * Triple-Roller Hemming Tool Head:
            - Step 1: Pre-Hemming Wheel (45 deg angle, diameter 120 mm, CrV tool steel 62 HRC).
            - Step 2: Intermediate Hemming Wheel (75 deg angle, diameter 120 mm).
            - Step 3: Final Flat Hemming Wheel (90 deg flat roller, diameter 150 mm).
        * Integrated ATI Omega160 IP67 6-Axis Force-Torque (F/T) Transducer at Robot Wrist.
        * Optical Laser Triangulation Scanners: 3x Perceptron Helix / Coherix Predator 3D profilometers.
        * Adhesive Extrusion Head: SCA Schuler / Scheugenpflug servo-electric positive displacement
          piston dispenser delivering high-viscosity structural mastic (80,000 mPa.s).
    - Fixturing Bed:
        * 18-point multi-zone vacuum suction tooling nest (-75 kPa Festo venturi generators).
        * 6x Tunkers SZK servo-electric retractable shot-pin toggle clamps.
        * Balluff inductive seating confirmation sensors with micron-level contact repeatability.

  CYBER-PHYSICAL MATHEMATICAL METHODOLOGIES CODED:
    1. Triple Modular Redundancy (2oo3 TMR) Voting with Pairwise Discrepancy Timers & Lens Air-Purge.
    2. 2nd-Order Digital Butterworth Low-Pass Filtering & Dynamic Gravity Tare Vector Compensation.
    3. Non-Newtonian Temperature-Dependent Fluid Rheology & Volumetric Bead Deposition Control.
    4. Sheet Metal Elastic-Plastic Flange Bending Moments & Contact Pressure Mechanics.
    5. Discrete State-Space Dynamic Model (4x4 A, 4x3 B, 4x4 C, 4x3 D) at 4ms Cycle Time.
    6. Luenberger Observer / Discrete Kalman State Innovation Observer.
    7. Receding-Horizon Model Predictive Control (MPC) with Unrolled Quadratic Cost Optimization.
    8. 11-State Sequential Finite State Machine with Micro-Interpolation & Path Tracking.
    9. ISA-18.2 Multi-Tiered Alarm Matrix (HH, H, L, LL, Deadbands, Diagnostic Word Bitfields).
====================================================================================================
*)
VAR_INPUT
    (* ========================================================================================= *)
    (* 1. CELL MASTER SAFETY, PERMIT & SEQUENCE CONTROL SIGNALS                                  *)
    (* ========================================================================================= *)
    b_EnableCell                    : BOOL;     (* Master cell automatic cycle enable permission signal [-] *)
    b_EmergencyStop_OK              : BOOL;     (* Dual-channel hardware safety circuit status ISO 13849-1 PLe [-] *)
    b_SafetyGate_Closed             : BOOL;     (* Perimeter safety interlocking fence and light curtain status [-] *)
    b_PartLoaded_DockTrigger        : BOOL;     (* Upstream overhead gantry fixture part presence trigger [-] *)
    b_AirWipePurge_Ack              : BOOL;     (* Feedback confirmation from optical window air purge valve [-] *)
    b_AlarmReset                    : BOOL;     (* Operator panel master fault latch acknowledge and reset [-] *)

    (* ========================================================================================= *)
    (* 2. ATI 6-AXIS WRIST FORCE / TORQUE TRANSDUCER SIGNALS (ETHERCAT IRT 4.0 MS)               *)
    (* ========================================================================================= *)
    r_HemmingRoller_Force_Fx_Raw    : REAL;     (* Tangential friction force component along tool path [N] *)
    r_HemmingRoller_Force_Fy_Raw    : REAL;     (* Lateral side-load force component normal to flange path [N] *)
    r_HemmingRoller_Force_Fz_Raw    : REAL;     (* Primary normal contact hemming pressing force [N] *)
    r_HemmingRoller_Torque_Mx_Raw   : REAL;     (* Roller head lateral camber overturning torque [N.m] *)
    r_HemmingRoller_Torque_My_Raw   : REAL;     (* Roller head pitch bending torque in feed direction [N.m] *)
    r_HemmingRoller_Torque_Mz_Raw   : REAL;     (* Roller head axial yaw torsion torque around normal [N.m] *)

    (* ========================================================================================= *)
    (* 3. 3D OPTICAL LASER TRIANGULATION SENSORS (TMR 2oo3 ROLL-IN, GAP, FLUSHNESS)             *)
    (* ========================================================================================= *)
    r_LaserSensor_A_RollIn_mm       : REAL;     (* Perceptron 3D laser scanner Channel A flange roll-in depth [mm] *)
    r_LaserSensor_B_RollIn_mm       : REAL;     (* Perceptron 3D laser scanner Channel B flange roll-in depth [mm] *)
    r_LaserSensor_C_RollIn_mm       : REAL;     (* Perceptron 3D laser scanner Channel C flange roll-in depth [mm] *)
    r_LaserSensor_FlangeGap_mm      : REAL;     (* Coherix optical gap distance between inner/outer panels [mm] *)
    r_LaserSensor_Flushness_mm      : REAL;     (* Coherix outer skin flushness offset relative to body datum [mm] *)

    (* ========================================================================================= *)
    (* 4. VOLUMETRIC MASTIC SEALER DISPENSING SENSOR SIGNALS                                     *)
    (* ========================================================================================= *)
    r_SealerDispense_Pressure_bar   : REAL;     (* Nozzle manifold dynamic fluid injection pressure [bar] *)
    r_SealerDispense_FlowRate_ccps  : REAL;     (* High-resolution positive displacement gear flow meter [cm3/s] *)
    r_SealerDispense_Temp_degC      : REAL;     (* Heated delivery hose temperature probe at nozzle tip [deg C] *)
    r_MasticViscosity_mPas          : REAL;     (* Inline rheometer measured dynamic fluid viscosity [mPa.s] *)

    (* ========================================================================================= *)
    (* 5. ROBOT KINEMATICS, TOOLING NEST & INCOMING BLANK PARAMETERS                             *)
    (* ========================================================================================= *)
    r_RobotTCP_ActualVelocity_mmps  : REAL;     (* Tool Center Point (TCP) measured feed trajectory velocity [mm/s] *)
    r_RobotTCP_HemmingAngle_deg     : REAL;     (* Wrist tilt orientation angle relative to flange normal [deg] *)
    r_VacuumTooling_Level_kPa       : REAL;     (* Tooling nest vacuum manifold vacuum pressure level [kPa] *)
    r_SheetMetal_Thickness_Outer_mm : REAL;     (* Measured outer skin blank sheet thickness gauge [mm] *)
    r_SheetMetal_Thickness_Inner_mm : REAL;     (* Measured inner door frame sheet thickness gauge [mm] *)
END_VAR
VAR_OUTPUT
    (* ========================================================================================= *)
    (* 1. CELL MASTER STATUS & INTERLOCK SIGNALS                                                 *)
    (* ========================================================================================= *)
    b_CellReady                     : BOOL;     (* Hemming & sealer cell idle and ready for execution [-] *)
    b_HemmingCycleActive            : BOOL;     (* Roller hemming or dispensing sequence actively running [-] *)
    b_HemmingCycleComplete          : BOOL;     (* Part hemming and sealing cycle successfully finished [-] *)
    b_PartUnclamp_Permit            : BOOL;     (* Safe interlock permit to release vacuum and clamps for unloader [-] *)
    b_EmergencyStop_Active          : BOOL;     (* Cell safety shutdown active due to hardware E-stop or overload [-] *)
    i_CurrentFSM_State              : INT;      (* Active Finite State Machine state enumeration index [-] *)

    (* ========================================================================================= *)
    (* 2. ROBOT CONTROLLER TRAJECTORY & FORCE COMPENSATION OFFSETS                               *)
    (* ========================================================================================= *)
    r_RobotTCP_Offset_Normal_mm     : REAL;     (* Real-time normal path offset command to robot controller [mm] *)
    r_RobotTCP_Offset_Lateral_mm    : REAL;     (* Real-time lateral path offset command to robot controller [mm] *)
    r_RobotTCP_TargetVelocity_mmps  : REAL;     (* Dynamically modulated robot traverse feedrate command [mm/s] *)

    (* ========================================================================================= *)
    (* 3. MASTIC SEALER DISPENSE ACTUATION COMMANDS                                              *)
    (* ========================================================================================= *)
    r_SealerPump_FlowCmd_ccps       : REAL;     (* Electric servo piston extruder volumetric flow setpoint [cm3/s] *)
    r_SealerPump_SpeedCmd_RPM       : REAL;     (* Dispenser servo motor rotational speed setpoint [rev/min] *)
    b_SealerNozzle_Open             : BOOL;     (* Pneumatic high-pressure snuff-back needle valve solenoid [-] *)

    (* ========================================================================================= *)
    (* 4. TOOLING BED & SENSOR AUXILIARY ACTUATOR COMMANDS                                       *)
    (* ========================================================================================= *)
    b_VacuumGripper_Command         : BOOL;     (* Multi-zone vacuum venturi generator energization solenoid [-] *)
    b_ServoClamps_EngageCmd         : BOOL;     (* Tooling nest motorized toggle shot-pin clamp engage command [-] *)
    b_LaserWindow_AirWipeBlow_Cmd   : BOOL;     (* Solenoid valve pulse for optical laser lens purge air blast [-] *)

    (* ========================================================================================= *)
    (* 5. ESTIMATED CYBER-PHYSICAL STATES & TMR CONSENSUS VALUES                                 *)
    (* ========================================================================================= *)
    r_Voted_RollIn_mm               : REAL;     (* 2oo3 TMR consensus outer-to-inner hem roll-in measurement [mm] *)
    r_Estimated_FlangeCrease_mm     : REAL;     (* State-space observer estimated sheet metal crease depth [mm] *)
    r_Estimated_SealerBeadHeight_mm : REAL;     (* State-space observer estimated compressed sealer bead height [mm] *)

    (* ========================================================================================= *)
    (* 6. ISA-18.2 ALARM & DIAGNOSTIC PACKED REGISTERS                                           *)
    (* ========================================================================================= *)
    w_CellStatusWord                : WORD;     (* Packed cell operating mode and state word bitfield [-] *)
    w_ISA_AlarmWord_1               : DWORD;    (* ISA-18.2 Multi-tiered process warning and trip alarms DWORD #1 [-] *)
    w_ISA_AlarmWord_2               : DWORD;    (* ISA-18.2 Sensor discrepancy and diagnostic alarms DWORD #2 [-] *)
END_VAR
VAR
    (* ========================================================================================= *)
    (* 1. SYSTEM TIMING, SCAN CONSTANTS & HEARTBEAT ENGINE                                       *)
    (* ========================================================================================= *)
    b_FirstScan                     : BOOL := TRUE;
    r_DeltaT_Sec                    : REAL := 0.004;    (* Deterministic fieldbus cycle period: 4.0 milliseconds [s] *)
    dw_HeartbeatCycleCount          : DWORD := 0;
    r_CycleTimer_Sec                : REAL := 0.0;
    r_StateDwellTimer_Sec           : REAL := 0.0;

    (* ========================================================================================= *)
    (* 2. BUTTERWORTH 2ND-ORDER DIGITAL LOW-PASS FILTER APPLIED TO 6-AXIS F/T TRANSDUCER         *)
    (* Filter Cutoff = 25.0 Hz @ Sampling Frequency = 250.0 Hz (T_s = 4.0 ms)                    *)
    (* ========================================================================================= *)
    r_Filt_b0                       : REAL := 0.067455;
    r_Filt_b1                       : REAL := 0.134911;
    r_Filt_b2                       : REAL := 0.067455;
    r_Filt_a1                       : REAL := -1.142981;
    r_Filt_a2                       : REAL := 0.412802;

    r_Raw_Fx_z1                     : REAL := 0.0;
    r_Raw_Fx_z2                     : REAL := 0.0;
    r_Filt_Fx_z1                    : REAL := 0.0;
    r_Filt_Fx_z2                    : REAL := 0.0;
    r_Filt_Fx                       : REAL := 0.0;

    r_Raw_Fy_z1                     : REAL := 0.0;
    r_Raw_Fy_z2                     : REAL := 0.0;
    r_Filt_Fy_z1                    : REAL := 0.0;
    r_Filt_Fy_z2                    : REAL := 0.0;
    r_Filt_Fy                       : REAL := 0.0;

    r_Raw_Fz_z1                     : REAL := 0.0;
    r_Raw_Fz_z2                     : REAL := 0.0;
    r_Filt_Fz_z1                    : REAL := 0.0;
    r_Filt_Fz_z2                    : REAL := 0.0;
    r_Filt_Fz                       : REAL := 0.0;

    r_Raw_Mx_z1                     : REAL := 0.0;
    r_Raw_Mx_z2                     : REAL := 0.0;
    r_Filt_Mx_z1                    : REAL := 0.0;
    r_Filt_Mx_z2                    : REAL := 0.0;
    r_Filt_Mx                       : REAL := 0.0;

    r_Raw_My_z1                     : REAL := 0.0;
    r_Raw_My_z2                     : REAL := 0.0;
    r_Filt_My_z1                    : REAL := 0.0;
    r_Filt_My_z2                    : REAL := 0.0;
    r_Filt_My                       : REAL := 0.0;

    r_Raw_Mz_z1                     : REAL := 0.0;
    r_Raw_Mz_z2                     : REAL := 0.0;
    r_Filt_Mz_z1                    : REAL := 0.0;
    r_Filt_Mz_z2                    : REAL := 0.0;
    r_Filt_Mz                       : REAL := 0.0;

    r_ResultantForce_N              : REAL := 0.0;
    r_ResultantTorque_Nm            : REAL := 0.0;

    (* Tool Center Point dynamic gravity tare parameters *)
    r_ToolMass_kg                   : REAL := 18.5;     (* Mass of triple-roller hemming end-effector [kg] *)
    r_GravityAccel_mpss             : REAL := 9.80665;  (* Gravitational acceleration [m/s2] *)
    r_ToolGravity_Fz_Tare_N         : REAL := 0.0;
    r_HemmingContactForce_Fz_Net_N  : REAL := 0.0;

    (* ========================================================================================= *)
    (* 3. TRIPLE MODULAR REDUNDANCY (2oo3 TMR) OPTICAL LASER VOTING ENGINE                       *)
    (* ========================================================================================= *)
    r_TMR_Discrepancy_Limit_mm      : REAL := 0.150;    (* Discrepancy threshold between sensors [mm] *)
    r_Diff_AB_mm                    : REAL := 0.0;
    r_Diff_BC_mm                    : REAL := 0.0;
    r_Diff_CA_mm                    : REAL := 0.0;

    b_SensorA_Valid                 : BOOL := TRUE;
    b_SensorB_Valid                 : BOOL := TRUE;
    b_SensorC_Valid                 : BOOL := TRUE;

    r_DiscTimer_AB_Sec              : REAL := 0.0;
    r_DiscTimer_BC_Sec              : REAL := 0.0;
    r_DiscTimer_CA_Sec              : REAL := 0.0;
    r_DiscTripDelay_Sec             : REAL := 0.800;    (* Discrepancy qualification persistence [s] *)

    b_Discrepancy_AB_Tripped        : BOOL := FALSE;
    b_Discrepancy_BC_Tripped        : BOOL := FALSE;
    b_Discrepancy_CA_Tripped        : BOOL := FALSE;

    b_TMR_Degraded_2oo2             : BOOL := FALSE;
    b_TMR_CriticalFault_Trip        : BOOL := FALSE;
    i_TMR_HealthState               : INT := 3;         (* 3: All 3 healthy, 2: 2oo2 degraded, 1: 1oo1, 0: Fault *)

    (* Optical air-wipe lens purge sequencer *)
    b_AirWipePurge_Active           : BOOL := FALSE;
    r_AirWipeDuration_Sec           : REAL := 0.500;    (* 500 ms blow-off pulse [s] *)
    r_AirWipeTimer_Sec              : REAL := 0.0;
    i_AirWipePurgeCounter           : INT := 0;

    (* ========================================================================================= *)
    (* 4. NON-NEWTONIAN MASTIC SEALER DISPENSING RHEOLOGY & FLUID MECHANICS                      *)
    (* ========================================================================================= *)
    r_NominalViscosity_mPas         : REAL := 80000.0;  (* Baseline dynamic viscosity at 25.0 deg C [mPa.s] *)
    r_NominalTemp_degC              : REAL := 25.0;
    r_TempViscosityCoeff_Beta       : REAL := 0.0385;   (* Arrhenius viscosity temperature coefficient [1/deg C] *)
    r_CorrectedViscosity_mPas       : REAL := 80000.0;
    r_DispenseNozzleDiameter_mm     : REAL := 3.20;     (* Circular extrusion orifice diameter [mm] *)
    r_DispenseHoseLength_m          : REAL := 4.50;     (* Flexible high-pressure heated hose length [m] *)
    r_DispenseHoseDiameter_mm       : REAL := 12.70;    (* Internal diameter of delivery hose [mm] *)

    r_TargetBeadWidth_mm            : REAL := 6.50;     (* Specified uncompressed mastic bead width [mm] *)
    r_TargetBeadHeight_mm           : REAL := 3.20;     (* Specified uncompressed mastic bead height [mm] *)
    r_TargetBeadArea_mm2            : REAL := 0.0;      (* Cross-sectional bead area [mm2] *)
    r_TargetDispenseFlow_ccps       : REAL := 0.0;      (* Theoretical required flow rate [cm3/s] *)
    r_PistonDispenserPivoting_cc    : REAL := 125.0;    (* Dispenser cylinder stroke volume [cm3] *)
    r_PistonDriveRatio_RPM_per_ccps : REAL := 18.75;    (* Motor speed per unit volumetric flow [RPM/(cm3/s)] *)

    r_FluidFrictionLoss_bar         : REAL := 0.0;      (* Hagen-Poiseuille calculated pressure drop [bar] *)
    r_FluidCompressibilityModulus   : REAL := 18500.0;  (* Bulk modulus of mastic adhesive [bar] *)
    r_DispensePressureError_bar     : REAL := 0.0;

    (* ========================================================================================= *)
    (* 5. SHEET METAL PLASTIC BENDING MECHANICS & SPRINGBACK PREDICTOR                           *)
    (* ========================================================================================= *)
    r_OuterSkin_Yield_MPa           : REAL := 210.0;    (* BH210 bake-hardened yield strength [MPa] *)
    r_InnerFrame_Yield_MPa          : REAL := 160.0;    (* CR4 mild steel yield strength [MPa] *)
    r_YoungsModulus_Steel_MPa       : REAL := 205000.0; (* Elastic modulus of carbon steel [MPa] *)
    r_PoissonsRatio_Steel           : REAL := 0.30;
    r_FlangeHeight_mm               : REAL := 10.50;    (* Standing flange height before hem [mm] *)
    r_FlangeCurvatureRadius_mm      : REAL := 1200.0;   (* Door styling character feature curvature [mm] *)

    r_TotalPackThickness_mm         : REAL := 1.50;
    r_TargetHemThickness_mm         : REAL := 2.15;
    r_SpringbackAngle_deg           : REAL := 0.0;
    r_PreHemForce_Setpoint_N        : REAL := 1400.0;   (* Pre-hemming target normal force (45 deg) [N] *)
    r_IntermediateForce_Setpoint_N  : REAL := 1650.0;   (* Intermediate target normal force (75 deg) [N] *)
    r_FinalHemForce_Setpoint_N      : REAL := 1800.0;   (* Final flat hemming target normal force (90 deg) [N] *)
    r_ActiveForce_Setpoint_N        : REAL := 1800.0;   (* Dynamically selected force setpoint [N] *)

    (* ========================================================================================= *)
    (* 6. DISCRETE STATE-SPACE MODEL & KALMAN OBSERVER MATRICES (4x4, 4x3)                       *)
    (* State Vector: x = [ x0: Force_Tracking_Error [N]                                          *)
    (*                     x1: Flange_Crease_Depth [mm]                                          *)
    (*                     x2: Sealer_Bead_Height [mm]                                           *)
    (*                     x3: Robot_TCP_Path_Offset [um] ]                                      *)
    (* Input Vector: u = [ u0: TCP_Normal_Correction [um]                                        *)
    (*                     u1: TCP_Traverse_Speed_Trim [mm/s]                                    *)
    (*                     u2: Sealer_Flow_Trim [cm3/s] ]                                        *)
    (* ========================================================================================= *)
    a_x                             : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];
    a_x_next                        : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];
    a_x_hat                         : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];
    a_u                             : ARRAY[0..2] OF REAL := [0.0, 0.0, 0.0];
    a_y_meas                        : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];
    a_y_est                         : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];
    a_innov                         : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];

    (* Numerical System Dynamics Matrix A (4x4) *)
    mat_A                           : ARRAY[0..3, 0..3] OF REAL := [
        [0.884500, -12.450000,   0.000000,  1.842000],
        [0.000150,   0.942000,   0.012500, -0.003500],
        [-0.000080, -0.052000,   0.815000,  0.000200],
        [0.004200,   0.000000,   0.000000,  0.765000]
    ];

    (* Numerical Actuation Input Matrix B (4x3) *)
    mat_B                           : ARRAY[0..3, 0..2] OF REAL := [
        [2.854000, -0.421000,  0.000000],
        [0.008400,  0.001200,  0.015000],
        [-0.003200, -0.008500,  0.142000],
        [0.952000,  0.025000,  0.000000]
    ];

    (* Numerical Measurement Output Matrix C (4x4) *)
    mat_C                           : ARRAY[0..3, 0..3] OF REAL := [
        [1.000000,  0.000000,  0.000000,  0.000000],
        [0.000000,  1.000000,  0.000000,  0.000000],
        [0.000000,  0.000000,  1.000000,  0.000000],
        [0.000000,  0.000000,  0.000000,  1.000000]
    ];

    (* Discrete Observer Kalman Gain Matrix L (4x4) *)
    mat_L                           : ARRAY[0..3, 0..3] OF REAL := [
        [0.185000, -0.250000,  0.000000,  0.045000],
        [0.000250,  0.220000,  0.005000, -0.001200],
        [-0.000150, -0.015000,  0.195000,  0.000100],
        [0.008500,  0.000000,  0.000000,  0.165000]
    ];

    (* ========================================================================================= *)
    (* 7. MODEL PREDICTIVE CONTROL (MPC) QUADRATIC COST APPROXIMATION MATRICES                   *)
    (* ========================================================================================= *)
    (* State Tracking Penalty Matrix Q (4x4) *)
    mat_Q                           : ARRAY[0..3, 0..3] OF REAL := [
        [0.015000,    0.000000,    0.000000,   0.000000],
        [0.000000,  450.000000,    0.000000,   0.000000],
        [0.000000,    0.000000,  280.000000,   0.000000],
        [0.000000,    0.000000,    0.000000,   0.080000]
    ];

    (* Actuator Slew Effort Penalty Matrix R (3x3) *)
    mat_R                           : ARRAY[0..2, 0..2] OF REAL := [
        [1.250000,  0.000000,  0.000000],
        [0.000000,  0.650000,  0.000000],
        [0.000000,  0.000000,  0.850000]
    ];

    (* Terminal Algebraic Riccati Cost Matrix P (4x4) *)
    mat_P                           : ARRAY[0..3, 0..3] OF REAL := [
        [0.085000,    0.000000,    0.000000,   0.000000],
        [0.000000, 1250.000000,    0.000000,   0.000000],
        [0.000000,    0.000000,  850.000000,   0.000000],
        [0.000000,    0.000000,    0.000000,   0.350000]
    ];

    (* MPC Horizon Buffers (Prediction Horizon Np = 4 stages) *)
    a_x_pred_stage1                 : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];
    a_x_pred_stage2                 : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];
    a_x_pred_stage3                 : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];
    a_x_pred_stage4                 : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];

    a_u_opt_stage0                  : ARRAY[0..2] OF REAL := [0.0, 0.0, 0.0];
    a_u_opt_stage1                  : ARRAY[0..2] OF REAL := [0.0, 0.0, 0.0];
    a_u_opt_stage2                  : ARRAY[0..2] OF REAL := [0.0, 0.0, 0.0];
    a_u_opt_stage3                  : ARRAY[0..2] OF REAL := [0.0, 0.0, 0.0];

    r_MPC_StageCost0                : REAL := 0.0;
    r_MPC_StageCost1                : REAL := 0.0;
    r_MPC_StageCost2                : REAL := 0.0;
    r_MPC_StageCost3                : REAL := 0.0;
    r_MPC_TerminalCost              : REAL := 0.0;
    r_MPC_TotalPredictedCost        : REAL := 0.0;

    (* MPC Gradient and Hessian Precomputed Inversion Components *)
    a_grad_u                        : ARRAY[0..2] OF REAL := [0.0, 0.0, 0.0];
    mat_H_inv                       : ARRAY[0..2, 0..2] OF REAL := [
        [0.428571,  0.015240, -0.008450],
        [0.015240,  0.892857, -0.012500],
        [-0.008450, -0.012500,  0.740741]
    ];

    (* Actuator Hard Saturation Bounds *)
    r_Limit_Max_NormalOffset_mm     : REAL := 1.500;
    r_Limit_Min_NormalOffset_mm     : REAL := -1.500;
    r_Limit_Max_SpeedTrim_mmps      : REAL := 35.0;
    r_Limit_Min_SpeedTrim_mmps      : REAL := -35.0;
    r_Limit_Max_FlowTrim_ccps       : REAL := 2.50;
    r_Limit_Min_FlowTrim_ccps       : REAL := -2.50;

    (* Slew rate filters *)
    r_NormalOffset_Cmd_Filtered_mm  : REAL := 0.0;
    r_SpeedTrim_Cmd_Filtered_mmps   : REAL := 0.0;
    r_FlowTrim_Cmd_Filtered_ccps    : REAL := 0.0;

    (* ========================================================================================= *)
    (* 8. FINITE STATE MACHINE (FSM) CONSTANTS & LOCAL TIMERS                                    *)
    (* ========================================================================================= *)
    STATE_CELL_IDLE                 : INT := 0;
    STATE_INNER_OUTER_PANEL_DOCK    : INT := 10;
    STATE_VACUUM_CLAMP_ENGAGE       : INT := 20;
    STATE_3D_VISION_ALIGN_OFFSETS   : INT := 30;
    STATE_MASTIC_SEALER_DISPENSE    : INT := 40;
    STATE_FLANGE_PRE_HEM_45DEG      : INT := 50;
    STATE_INTERMEDIATE_HEM_75DEG    : INT := 60;
    STATE_FINAL_FLAT_HEM_90DEG      : INT := 70;
    STATE_GAP_FLUSH_OPTICAL_AUDIT   : INT := 80;
    STATE_PART_UNCLAMP_EJECT        : INT := 90;
    STATE_ROLLER_FORCE_OVERLOAD_TRIP: INT := 99;

    i_NextFSM_State                 : INT := 0;
    b_StateFirstCycle               : BOOL := TRUE;
    r_StateTimer_Sec                : REAL := 0.0;
    r_StateTimeout_Sec              : REAL := 60.0;
    b_StateTimeout_Flag             : BOOL := FALSE;

    (* Process Trajectory Variables *)
    r_HemmingPathProgress_Percent   : REAL := 0.0;
    r_NominalPathSpeed_mmps         : REAL := 180.0;    (* Nominal robot traverse speed [mm/s] *)
    r_TotalPathLength_mm            : REAL := 3450.0;   (* Total perimeter hem contour length [mm] *)
    r_InterpolatedDistance_mm       : REAL := 0.0;

    (* Fixture status verification *)
    b_VacuumSensors_AllOK           : BOOL := FALSE;
    b_ServoClamps_AllLocked         : BOOL := FALSE;
    b_VisionOffsets_Computed        : BOOL := FALSE;
    r_Vision_OffsetX_mm             : REAL := 0.0;
    r_Vision_OffsetY_mm             : REAL := 0.0;
    r_Vision_OffsetZ_mm             : REAL := 0.0;
    r_Vision_OffsetYaw_deg          : REAL := 0.0;

    (* ========================================================================================= *)
    (* 9. ISA-18.2 MULTI-TIERED ALARM THRESHOLDS, DEADBANDS & TIMERS                             *)
    (* ========================================================================================= *)
    (* Normal Hemming Force Trip Points [N] *)
    r_Force_HH_Trip_N               : REAL := 2250.0;   (* High-High panel crushing trip [N] *)
    r_Force_H_Warn_N                : REAL := 2050.0;   (* High warning [N] *)
    r_Force_L_Warn_N                : REAL := 1450.0;   (* Low warning loose hem [N] *)
    r_Force_LL_Trip_N               : REAL := 1100.0;   (* Low-Low disengaged roller abort [N] *)
    r_Force_Deadband_N              : REAL := 25.0;     (* Hysteresis deadband [N] *)

    (* Sealer Injection Pressure Trip Points [bar] *)
    r_Press_HH_Trip_bar             : REAL := 220.0;    (* High-High blocked nozzle trip [bar] *)
    r_Press_H_Warn_bar              : REAL := 185.0;    (* High warning [bar] *)
    r_Press_LL_Trip_bar             : REAL := 45.0;     (* Low-Low air bubble starvation trip [bar] *)
    r_Press_Deadband_bar            : REAL := 5.0;      (* Hysteresis deadband [bar] *)

    (* ATI 6-Axis Resultant Force Crash Trip [N] *)
    r_Force_Resultant_HH_Crash_N    : REAL := 3000.0;   (* Severe robot wrist collision trip [N] *)
    r_Torque_Resultant_HH_Crash_Nm  : REAL := 150.0;    (* Severe robot wrist moment trip [N.m] *)

    (* Vacuum Level Threshold [kPa] *)
    r_Vacuum_LL_Fault_kPa           : REAL := -65.0;    (* Minimum vacuum holding safety limit [kPa] *)

    (* Optical Flange Gap & Flushness Quality Limits [mm] *)
    r_FlangeGap_Max_mm              : REAL := 1.80;
    r_FlangeGap_Min_mm              : REAL := 0.40;
    r_Flushness_Max_mm              : REAL := 0.80;
    r_Flushness_Min_mm              : REAL := -0.80;

    (* Alarm Delay Qualification Timers [s] *)
    r_AlarmTimer_Force_HH           : REAL := 0.0;
    r_AlarmTimer_Force_H            : REAL := 0.0;
    r_AlarmTimer_Force_L            : REAL := 0.0;
    r_AlarmTimer_Force_LL           : REAL := 0.0;
    r_AlarmTimer_Press_HH           : REAL := 0.0;
    r_AlarmTimer_Press_H            : REAL := 0.0;
    r_AlarmTimer_Press_LL           : REAL := 0.0;
    r_AlarmTimer_Crash_HH           : REAL := 0.0;
    r_AlarmTimer_Vacuum_LL          : REAL := 0.0;

    r_QualDelay_Trip_Sec            : REAL := 0.020;    (* 20 ms fast trip qualification [s] *)
    r_QualDelay_Warn_Sec            : REAL := 0.080;    (* 80 ms warning qualification [s] *)

    (* Latched Alarm Status Bits *)
    b_AlarmLatched_Force_HH         : BOOL := FALSE;
    b_AlarmLatched_Force_H          : BOOL := FALSE;
    b_AlarmLatched_Force_L          : BOOL := FALSE;
    b_AlarmLatched_Force_LL         : BOOL := FALSE;
    b_AlarmLatched_Press_HH         : BOOL := FALSE;
    b_AlarmLatched_Press_H          : BOOL := FALSE;
    b_AlarmLatched_Press_LL         : BOOL := FALSE;
    b_AlarmLatched_Crash_HH         : BOOL := FALSE;
    b_AlarmLatched_Vacuum_LL        : BOOL := FALSE;
    b_AlarmLatched_TMR_Trip         : BOOL := FALSE;
    b_AlarmLatched_GapFlush_Fault   : BOOL := FALSE;

    (* Loop index counters *)
    idx_i                           : INT := 0;
    idx_j                           : INT := 0;
    idx_k                           : INT := 0;
    r_SumAcc                        : REAL := 0.0;
    r_AuxVar1                       : REAL := 0.0;
    r_AuxVar2                       : REAL := 0.0;
END_VAR
''')
    
    # Body starts
    sections.append('''
(* ============================================================================================= *)
(* SECTION 1: MASTER SAFETY VERIFICATION, CYCLE INITIALIZATION & HEARTBEAT ENGINE                *)
(* ============================================================================================= *)
dw_HeartbeatCycleCount := dw_HeartbeatCycleCount + 1;
r_CycleTimer_Sec := r_CycleTimer_Sec + r_DeltaT_Sec;

IF b_FirstScan THEN
    b_FirstScan := FALSE;
    i_CurrentFSM_State := STATE_CELL_IDLE;
    i_NextFSM_State := STATE_CELL_IDLE;
    b_StateFirstCycle := TRUE;
    r_StateTimer_Sec := 0.0;

    (* Initialize State-Space Estimation Buffers *)
    a_x[0] := 0.0;
    a_x[1] := 0.0;
    a_x[2] := 0.0;
    a_x[3] := 0.0;

    a_x_hat[0] := 0.0;
    a_x_hat[1] := 0.0;
    a_x_hat[2] := 0.0;
    a_x_hat[3] := 0.0;

    a_u[0] := 0.0;
    a_u[1] := 0.0;
    a_u[2] := 0.0;

    (* Initialize 2nd-Order Filter Past Buffers *)
    r_Raw_Fx_z1 := r_HemmingRoller_Force_Fx_Raw;
    r_Raw_Fx_z2 := r_HemmingRoller_Force_Fx_Raw;
    r_Filt_Fx_z1 := r_HemmingRoller_Force_Fx_Raw;
    r_Filt_Fx_z2 := r_HemmingRoller_Force_Fx_Raw;
    r_Filt_Fx := r_HemmingRoller_Force_Fx_Raw;

    r_Raw_Fy_z1 := r_HemmingRoller_Force_Fy_Raw;
    r_Raw_Fy_z2 := r_HemmingRoller_Force_Fy_Raw;
    r_Filt_Fy_z1 := r_HemmingRoller_Force_Fy_Raw;
    r_Filt_Fy_z2 := r_HemmingRoller_Force_Fy_Raw;
    r_Filt_Fy := r_HemmingRoller_Force_Fy_Raw;

    r_Raw_Fz_z1 := r_HemmingRoller_Force_Fz_Raw;
    r_Raw_Fz_z2 := r_HemmingRoller_Force_Fz_Raw;
    r_Filt_Fz_z1 := r_HemmingRoller_Force_Fz_Raw;
    r_Filt_Fz_z2 := r_HemmingRoller_Force_Fz_Raw;
    r_Filt_Fz := r_HemmingRoller_Force_Fz_Raw;

    r_Raw_Mx_z1 := r_HemmingRoller_Torque_Mx_Raw;
    r_Raw_Mx_z2 := r_HemmingRoller_Torque_Mx_Raw;
    r_Filt_Mx_z1 := r_HemmingRoller_Torque_Mx_Raw;
    r_Filt_Mx_z2 := r_HemmingRoller_Torque_Mx_Raw;
    r_Filt_Mx := r_HemmingRoller_Torque_Mx_Raw;

    r_Raw_My_z1 := r_HemmingRoller_Torque_My_Raw;
    r_Raw_My_z2 := r_HemmingRoller_Torque_My_Raw;
    r_Filt_My_z1 := r_HemmingRoller_Torque_My_Raw;
    r_Filt_My_z2 := r_HemmingRoller_Torque_My_Raw;
    r_Filt_My := r_HemmingRoller_Torque_My_Raw;

    r_Raw_Mz_z1 := r_HemmingRoller_Torque_Mz_Raw;
    r_Raw_Mz_z2 := r_HemmingRoller_Torque_Mz_Raw;
    r_Filt_Mz_z1 := r_HemmingRoller_Torque_Mz_Raw;
    r_Filt_Mz_z2 := r_HemmingRoller_Torque_Mz_Raw;
    r_Filt_Mz := r_HemmingRoller_Torque_Mz_Raw;
END_IF;

(* Master Safety Circuit Interlocking *)
IF NOT b_EmergencyStop_OK OR NOT b_SafetyGate_Closed THEN
    b_EmergencyStop_Active := TRUE;
    b_CellReady := FALSE;
    b_HemmingCycleActive := FALSE;
    b_SealerNozzle_Open := FALSE;
    r_SealerPump_FlowCmd_ccps := 0.0;
    r_SealerPump_SpeedCmd_RPM := 0.0;
    r_RobotTCP_TargetVelocity_mmps := 0.0;
    r_RobotTCP_Offset_Normal_mm := 0.0;
    r_RobotTCP_Offset_Lateral_mm := 0.0;
    i_CurrentFSM_State := STATE_ROLLER_FORCE_OVERLOAD_TRIP;
END_IF;
''')

    # Section 2: 2oo3 TMR Laser Voting Engine
    sections.append('''
(* ============================================================================================= *)
(* SECTION 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) OPTICAL LASER VOTING ENGINE                   *)
(* ============================================================================================= *)
(* Compute Pairwise Absolute Differences Between Triangulation Sensors A, B, and C *)
r_Diff_AB_mm := ABS(r_LaserSensor_A_RollIn_mm - r_LaserSensor_B_RollIn_mm);
r_Diff_BC_mm := ABS(r_LaserSensor_B_RollIn_mm - r_LaserSensor_C_RollIn_mm);
r_Diff_CA_mm := ABS(r_LaserSensor_C_RollIn_mm - r_LaserSensor_A_RollIn_mm);

(* Discrepancy Debounce Timers *)
IF r_Diff_AB_mm > r_TMR_Discrepancy_Limit_mm THEN
    r_DiscTimer_AB_Sec := r_DiscTimer_AB_Sec + r_DeltaT_Sec;
    IF r_DiscTimer_AB_Sec >= r_DiscTripDelay_Sec THEN
        b_Discrepancy_AB_Tripped := TRUE;
    END_IF;
ELSE
    r_DiscTimer_AB_Sec := 0.0;
    b_Discrepancy_AB_Tripped := FALSE;
END_IF;

IF r_Diff_BC_mm > r_TMR_Discrepancy_Limit_mm THEN
    r_DiscTimer_BC_Sec := r_DiscTimer_BC_Sec + r_DeltaT_Sec;
    IF r_DiscTimer_BC_Sec >= r_DiscTripDelay_Sec THEN
        b_Discrepancy_BC_Tripped := TRUE;
    END_IF;
ELSE
    r_DiscTimer_BC_Sec := 0.0;
    b_Discrepancy_BC_Tripped := FALSE;
END_IF;

IF r_Diff_CA_mm > r_TMR_Discrepancy_Limit_mm THEN
    r_DiscTimer_CA_Sec := r_DiscTimer_CA_Sec + r_DeltaT_Sec;
    IF r_DiscTimer_CA_Sec >= r_DiscTripDelay_Sec THEN
        b_Discrepancy_CA_Tripped := TRUE;
    END_IF;
ELSE
    r_DiscTimer_CA_Sec := 0.0;
    b_Discrepancy_CA_Tripped := FALSE;
END_IF;

(* 2oo3 Voting & Fault Isolation Logic *)
IF NOT b_Discrepancy_AB_Tripped AND NOT b_Discrepancy_BC_Tripped AND NOT b_Discrepancy_CA_Tripped THEN
    (* All Three Sensors Healthy: Full 3-Channel Tri-Voter Average *)
    b_SensorA_Valid := TRUE;
    b_SensorB_Valid := TRUE;
    b_SensorC_Valid := TRUE;
    b_TMR_Degraded_2oo2 := FALSE;
    b_TMR_CriticalFault_Trip := FALSE;
    i_TMR_HealthState := 3;
    r_Voted_RollIn_mm := (r_LaserSensor_A_RollIn_mm + r_LaserSensor_B_RollIn_mm + r_LaserSensor_C_RollIn_mm) / 3.0;

ELSIF b_Discrepancy_AB_Tripped AND b_Discrepancy_CA_Tripped AND NOT b_Discrepancy_BC_Tripped THEN
    (* Sensor A Diverged: Degraded 2oo2 Average of B and C *)
    b_SensorA_Valid := FALSE;
    b_SensorB_Valid := TRUE;
    b_SensorC_Valid := TRUE;
    b_TMR_Degraded_2oo2 := TRUE;
    b_TMR_CriticalFault_Trip := FALSE;
    i_TMR_HealthState := 2;
    r_Voted_RollIn_mm := (r_LaserSensor_B_RollIn_mm + r_LaserSensor_C_RollIn_mm) * 0.500;

    (* Trigger Optical Air Wipe Window Purge Cycle *)
    IF NOT b_AirWipePurge_Active THEN
        b_AirWipePurge_Active := TRUE;
        r_AirWipeTimer_Sec := 0.0;
        i_AirWipePurgeCounter := i_AirWipePurgeCounter + 1;
    END_IF;

ELSIF b_Discrepancy_AB_Tripped AND b_Discrepancy_BC_Tripped AND NOT b_Discrepancy_CA_Tripped THEN
    (* Sensor B Diverged: Degraded 2oo2 Average of A and C *)
    b_SensorA_Valid := TRUE;
    b_SensorB_Valid := FALSE;
    b_SensorC_Valid := TRUE;
    b_TMR_Degraded_2oo2 := TRUE;
    b_TMR_CriticalFault_Trip := FALSE;
    i_TMR_HealthState := 2;
    r_Voted_RollIn_mm := (r_LaserSensor_A_RollIn_mm + r_LaserSensor_C_RollIn_mm) * 0.500;

    IF NOT b_AirWipePurge_Active THEN
        b_AirWipePurge_Active := TRUE;
        r_AirWipeTimer_Sec := 0.0;
        i_AirWipePurgeCounter := i_AirWipePurgeCounter + 1;
    END_IF;

ELSIF b_Discrepancy_BC_Tripped AND b_Discrepancy_CA_Tripped AND NOT b_Discrepancy_AB_Tripped THEN
    (* Sensor C Diverged: Degraded 2oo2 Average of A and B *)
    b_SensorA_Valid := TRUE;
    b_SensorB_Valid := TRUE;
    b_SensorC_Valid := FALSE;
    b_TMR_Degraded_2oo2 := TRUE;
    b_TMR_CriticalFault_Trip := FALSE;
    i_TMR_HealthState := 2;
    r_Voted_RollIn_mm := (r_LaserSensor_A_RollIn_mm + r_LaserSensor_B_RollIn_mm) * 0.500;

    IF NOT b_AirWipePurge_Active THEN
        b_AirWipePurge_Active := TRUE;
        r_AirWipeTimer_Sec := 0.0;
        i_AirWipePurgeCounter := i_AirWipePurgeCounter + 1;
    END_IF;

ELSE
    (* Multiple Sensor Divergence: Critical TMR Failure (All Channels Disagree) *)
    b_SensorA_Valid := FALSE;
    b_SensorB_Valid := FALSE;
    b_SensorC_Valid := FALSE;
    b_TMR_Degraded_2oo2 := FALSE;
    b_TMR_CriticalFault_Trip := TRUE;
    i_TMR_HealthState := 0;
    b_AlarmLatched_TMR_Trip := TRUE;
    (* Hold last valid roll-in reading without updating *)
END_IF;

(* Automatic Optical Lens Air-Wipe Purge Sequencer *)
IF b_AirWipePurge_Active THEN
    b_LaserWindow_AirWipeBlow_Cmd := TRUE;
    r_AirWipeTimer_Sec := r_AirWipeTimer_Sec + r_DeltaT_Sec;
    IF r_AirWipeTimer_Sec >= r_AirWipeDuration_Sec THEN
        b_LaserWindow_AirWipeBlow_Cmd := FALSE;
        IF b_AirWipePurge_Ack THEN
            b_AirWipePurge_Active := FALSE;
            r_AirWipeTimer_Sec := 0.0;
        END_IF;
    END_IF;
ELSE
    b_LaserWindow_AirWipeBlow_Cmd := FALSE;
END_IF;
''')

    # Section 3: 6-Axis Butterworth Digital Filtering & Dynamic Gravity Tare
    sections.append('''
(* ============================================================================================= *)
(* SECTION 3: 6-AXIS F/T BUTTERWORTH DIGITAL FILTERING & DYNAMIC GRAVITY TARE ENGINE             *)
(* ============================================================================================= *)
(* Channel Fx 2nd-Order Low-Pass Filter *)
r_Filt_Fx := (r_Filt_b0 * r_HemmingRoller_Force_Fx_Raw)
           + (r_Filt_b1 * r_Raw_Fx_z1)
           + (r_Filt_b2 * r_Raw_Fx_z2)
           - (r_Filt_a1 * r_Filt_Fx_z1)
           - (r_Filt_a2 * r_Filt_Fx_z2);
r_Raw_Fx_z2 := r_Raw_Fx_z1;
r_Raw_Fx_z1 := r_HemmingRoller_Force_Fx_Raw;
r_Filt_Fx_z2 := r_Filt_Fx_z1;
r_Filt_Fx_z1 := r_Filt_Fx;

(* Channel Fy 2nd-Order Low-Pass Filter *)
r_Filt_Fy := (r_Filt_b0 * r_HemmingRoller_Force_Fy_Raw)
           + (r_Filt_b1 * r_Raw_Fy_z1)
           + (r_Filt_b2 * r_Raw_Fy_z2)
           - (r_Filt_a1 * r_Filt_Fy_z1)
           - (r_Filt_a2 * r_Filt_Fy_z2);
r_Raw_Fy_z2 := r_Raw_Fy_z1;
r_Raw_Fy_z1 := r_HemmingRoller_Force_Fy_Raw;
r_Filt_Fy_z2 := r_Filt_Fy_z1;
r_Filt_Fy_z1 := r_Filt_Fy;

(* Channel Fz 2nd-Order Low-Pass Filter *)
r_Filt_Fz := (r_Filt_b0 * r_HemmingRoller_Force_Fz_Raw)
           + (r_Filt_b1 * r_Raw_Fz_z1)
           + (r_Filt_b2 * r_Raw_Fz_z2)
           - (r_Filt_a1 * r_Filt_Fz_z1)
           - (r_Filt_a2 * r_Filt_Fz_z2);
r_Raw_Fz_z2 := r_Raw_Fz_z1;
r_Raw_Fz_z1 := r_HemmingRoller_Force_Fz_Raw;
r_Filt_Fz_z2 := r_Filt_Fz_z1;
r_Filt_Fz_z1 := r_Filt_Fz;

(* Channel Mx 2nd-Order Low-Pass Filter *)
r_Filt_Mx := (r_Filt_b0 * r_HemmingRoller_Torque_Mx_Raw)
           + (r_Filt_b1 * r_Raw_Mx_z1)
           + (r_Filt_b2 * r_Raw_Mx_z2)
           - (r_Filt_a1 * r_Filt_Mx_z1)
           - (r_Filt_a2 * r_Filt_Mx_z2);
r_Raw_Mx_z2 := r_Raw_Mx_z1;
r_Raw_Mx_z1 := r_HemmingRoller_Torque_Mx_Raw;
r_Filt_Mx_z2 := r_Filt_Mx_z1;
r_Filt_Mx_z1 := r_Filt_Mx;

(* Channel My 2nd-Order Low-Pass Filter *)
r_Filt_My := (r_Filt_b0 * r_HemmingRoller_Torque_My_Raw)
           + (r_Filt_b1 * r_Raw_My_z1)
           + (r_Filt_b2 * r_Raw_My_z2)
           - (r_Filt_a1 * r_Filt_My_z1)
           - (r_Filt_a2 * r_Filt_My_z2);
r_Raw_My_z2 := r_Raw_My_z1;
r_Raw_My_z1 := r_HemmingRoller_Torque_My_Raw;
r_Filt_My_z2 := r_Filt_My_z1;
r_Filt_My_z1 := r_Filt_My;

(* Channel Mz 2nd-Order Low-Pass Filter *)
r_Filt_Mz := (r_Filt_b0 * r_HemmingRoller_Torque_Mz_Raw)
           + (r_Filt_b1 * r_Raw_Mz_z1)
           + (r_Filt_b2 * r_Raw_Mz_z2)
           - (r_Filt_a1 * r_Filt_Mz_z1)
           - (r_Filt_a2 * r_Filt_Mz_z2);
r_Raw_Mz_z2 := r_Raw_Mz_z1;
r_Raw_Mz_z1 := r_HemmingRoller_Torque_Mz_Raw;
r_Filt_Mz_z2 := r_Filt_Mz_z1;
r_Filt_Mz_z1 := r_Filt_Mz;

(* Compute Euclidean Resultant Force and Resultant Torque *)
r_ResultantForce_N := SQRT((r_Filt_Fx * r_Filt_Fx) + (r_Filt_Fy * r_Filt_Fy) + (r_Filt_Fz * r_Filt_Fz));
r_ResultantTorque_Nm := SQRT((r_Filt_Mx * r_Filt_Mx) + (r_Filt_My * r_Filt_My) + (r_Filt_Mz * r_Filt_Mz));

(* Dynamic Tool Mass Gravity Tare Compensation as Function of Wrist Tilt Angle *)
(* Theta in Radians = Deg * (PI / 180.0) *)
r_AuxVar1 := r_RobotTCP_HemmingAngle_deg * 0.0174532925;
r_ToolGravity_Fz_Tare_N := r_ToolMass_kg * r_GravityAccel_mpss * COS(r_AuxVar1);

(* True Net Normal Contact Pressing Force on Sheet Flange *)
r_HemmingContactForce_Fz_Net_N := r_Filt_Fz - r_ToolGravity_Fz_Tare_N;
''')

    # Section 4: Mastic Adhesive Rheology, Temperature Correction & Hagen-Poiseuille Dispense Engine
    sections.append('''
(* ============================================================================================= *)
(* SECTION 4: NON-NEWTONIAN MASTIC DISPENSING RHEOLOGY & FLUID MECHANICS ENGINE                  *)
(* ============================================================================================= *)
(* Temperature-Dependent Viscosity Correction (Arrhenius Exponential Law) *)
r_AuxVar2 := r_TempViscosityCoeff_Beta * (r_NominalTemp_degC - r_SealerDispense_Temp_degC);
(* Bounded exponential expansion to prevent numerical overflow: exp(u) ~ 1 + u + 0.5*u^2 + ... *)
IF r_AuxVar2 > 1.50 THEN
    r_AuxVar2 := 1.50;
ELSIF r_AuxVar2 < -1.50 THEN
    r_AuxVar2 := -1.50;
END_IF;

r_CorrectedViscosity_mPas := r_NominalViscosity_mPas * (1.0 + r_AuxVar2 + (0.50 * r_AuxVar2 * r_AuxVar2));

(* Compute Required Cross-Sectional Area of Extruded Mastic Bead (Semi-Elliptic Cross Section) *)
(* Area = (PI / 4.0) * Width * Height *)
r_TargetBeadArea_mm2 := 0.785398 * r_TargetBeadWidth_mm * r_TargetBeadHeight_mm;

(* Continuous Synchronous Volumetric Flow Command: Flow [cm3/s] = Area [mm2] * Velocity [mm/s] / 1000.0 *)
IF b_SealerNozzle_Open AND (r_RobotTCP_ActualVelocity_mmps > 5.0) THEN
    r_TargetDispenseFlow_ccps := (r_TargetBeadArea_mm2 * r_RobotTCP_ActualVelocity_mmps) / 1000.0;
ELSE
    r_TargetDispenseFlow_ccps := 0.0;
END_IF;

(* Hagen-Poiseuille Viscous Pressure Drop Calculation in Delivery Hose *)
(* DeltaP [Pa] = (128 * mu * L * Q) / (PI * D^4) *)
(* Converted to Bar: 1 bar = 100,000 Pa *)
r_AuxVar1 := r_DispenseHoseDiameter_mm / 1000.0; (* Diameter in meters *)
r_AuxVar2 := r_AuxVar1 * r_AuxVar1 * r_AuxVar1 * r_AuxVar1; (* D^4 *)
IF r_AuxVar2 > 1.0E-9 THEN
    r_FluidFrictionLoss_bar := (128.0 * (r_CorrectedViscosity_mPas * 0.001) * r_DispenseHoseLength_m * (r_TargetDispenseFlow_ccps * 1.0E-6))
                             / (3.14159265 * r_AuxVar2 * 100000.0);
ELSE
    r_FluidFrictionLoss_bar := 0.0;
END_IF;

(* Dispense Pressure Error & Extruder Motor Speed Calculation *)
r_DispensePressureError_bar := r_SealerDispense_Pressure_bar - (r_FluidFrictionLoss_bar + 95.0);
r_SealerPump_FlowCmd_ccps := r_TargetDispenseFlow_ccps + a_u[2]; (* Add MPC flow trim *)

(* Clamp Volumetric Flow Setpoint *)
IF r_SealerPump_FlowCmd_ccps < 0.0 THEN
    r_SealerPump_FlowCmd_ccps := 0.0;
ELSIF r_SealerPump_FlowCmd_ccps > 18.0 THEN
    r_SealerPump_FlowCmd_ccps := 18.0;
END_IF;

(* Servo Extruder Motor Speed Output (RPM) *)
r_SealerPump_SpeedCmd_RPM := r_SealerPump_FlowCmd_ccps * r_PistonDriveRatio_RPM_per_ccps;
''')

    # Section 5: Sheet Metal Elastic-Plastic Flange Bending Mechanics & Force Profiling
    sections.append('''
(* ============================================================================================= *)
(* SECTION 5: SHEET METAL PLASTIC BENDING MECHANICS & FORCE SETPOINT ENGINE                      *)
(* ============================================================================================= *)
(* Calculate Total Flange Sheet Stack Thickness *)
r_TotalPackThickness_mm := r_SheetMetal_Thickness_Outer_mm + r_SheetMetal_Thickness_Inner_mm;

(* Elastic Springback Estimation for Plastic Hemming *)
(* Theta_sb = 3 * (sigma_y / E) * (R_bend / t) *)
r_AuxVar1 := (r_OuterSkin_Yield_MPa / r_YoungsModulus_Steel_MPa) * (r_FlangeCurvatureRadius_mm / r_TotalPackThickness_mm);
r_SpringbackAngle_deg := 3.0 * r_AuxVar1 * 57.29578; (* Convert to degrees *)

(* Dynamic Force Setpoints Scaled by Incoming Sheet Thickness Deviation *)
(* Nominal Pack = 1.50 mm *)
r_AuxVar2 := r_TotalPackThickness_mm / 1.500;
IF r_AuxVar2 < 0.70 THEN
    r_AuxVar2 := 0.70;
ELSIF r_AuxVar2 > 1.40 THEN
    r_AuxVar2 := 1.40;
END_IF;

r_PreHemForce_Setpoint_N := 1400.0 * r_AuxVar2;
r_IntermediateForce_Setpoint_N := 1650.0 * r_AuxVar2;
r_FinalHemForce_Setpoint_N := 1800.0 * r_AuxVar2;

(* Select Active Normal Force Target Based on Active FSM Hemming Stage *)
CASE i_CurrentFSM_State OF
    STATE_FLANGE_PRE_HEM_45DEG:
        r_ActiveForce_Setpoint_N := r_PreHemForce_Setpoint_N;
    STATE_INTERMEDIATE_HEM_75DEG:
        r_ActiveForce_Setpoint_N := r_IntermediateForce_Setpoint_N;
    STATE_FINAL_FLAT_HEM_90DEG:
        r_ActiveForce_Setpoint_N := r_FinalHemForce_Setpoint_N;
ELSE
    r_ActiveForce_Setpoint_N := 0.0;
END_CASE;
''')

    # Section 6: Discrete State-Space Model & Kalman Observer
    sections.append('''
(* ============================================================================================= *)
(* SECTION 6: DISCRETE STATE-SPACE MODEL (x[k+1] = A*x[k] + B*u[k]) & KALMAN OBSERVER             *)
(* ============================================================================================= *)
(* Assign Sensor Measurements to y_meas Vector *)
a_y_meas[0] := r_HemmingContactForce_Fz_Net_N - r_ActiveForce_Setpoint_N; (* Force Error [N] *)
a_y_meas[1] := r_Voted_RollIn_mm;                                         (* Flange Roll-In [mm] *)
a_y_meas[2] := r_TargetBeadHeight_mm - (r_DispensePressureError_bar * 0.015); (* Bead Height [mm] *)
a_y_meas[3] := (r_LaserSensor_FlangeGap_mm - 1.00) * 1000.0;              (* Trajectory Gap [um] *)

(* Compute Estimated Output y_est = C * x_hat *)
FOR idx_i := 0 TO 3 DO
    r_SumAcc := 0.0;
    FOR idx_j := 0 TO 3 DO
        r_SumAcc := r_SumAcc + (mat_C[idx_i, idx_j] * a_x_hat[idx_j]);
    END_FOR;
    a_y_est[idx_i] := r_SumAcc;
    (* Innovation Vector: innov = y_meas - y_est *)
    a_innov[idx_i] := a_y_meas[idx_i] - a_y_est[idx_i];
END_FOR;

(* State-Space Dynamic Update with Kalman Innovation:                                            *)
(* x_hat[k+1] = A * x_hat[k] + B * u[k] + L * innov[k]                                          *)
FOR idx_i := 0 TO 3 DO
    r_SumAcc := 0.0;
    (* Matrix A * x_hat contribution *)
    FOR idx_j := 0 TO 3 DO
        r_SumAcc := r_SumAcc + (mat_A[idx_i, idx_j] * a_x_hat[idx_j]);
    END_FOR;
    (* Matrix B * u contribution *)
    FOR idx_k := 0 TO 2 DO
        r_SumAcc := r_SumAcc + (mat_B[idx_i, idx_k] * a_u[idx_k]);
    END_FOR;
    (* Matrix L * innov contribution *)
    FOR idx_j := 0 TO 3 DO
        r_SumAcc := r_SumAcc + (mat_L[idx_i, idx_j] * a_innov[idx_j]);
    END_FOR;
    a_x_next[idx_i] := r_SumAcc;
END_FOR;

(* Transfer Next State to Active State Buffers *)
FOR idx_i := 0 TO 3 DO
    a_x[idx_i] := a_x_next[idx_i];
    a_x_hat[idx_i] := a_x_next[idx_i];
END_FOR;

(* Assign Cyber-Physical Estimated States to Outputs *)
r_Estimated_FlangeCrease_mm := a_x_hat[1];
r_Estimated_SealerBeadHeight_mm := a_x_hat[2];
''')

    # Section 7: Model Predictive Control Receding Horizon Engine
    sections.append('''
(* ============================================================================================= *)
(* SECTION 7: MODEL PREDICTIVE CONTROL (MPC) RECEDING-HORIZON QUADRATIC OPTIMIZATION ENGINE      *)
(* ============================================================================================= *)
(* Stage 1 Forward State Prediction: x_pred_1 = A * x + B * u0 *)
FOR idx_i := 0 TO 3 DO
    r_SumAcc := 0.0;
    FOR idx_j := 0 TO 3 DO
        r_SumAcc := r_SumAcc + (mat_A[idx_i, idx_j] * a_x[idx_j]);
    END_FOR;
    FOR idx_k := 0 TO 2 DO
        r_SumAcc := r_SumAcc + (mat_B[idx_i, idx_k] * a_u[idx_k]);
    END_FOR;
    a_x_pred_stage1[idx_i] := r_SumAcc;
END_FOR;

(* Stage 2 Forward State Prediction: x_pred_2 = A * x_pred_1 + B * u1 *)
FOR idx_i := 0 TO 3 DO
    r_SumAcc := 0.0;
    FOR idx_j := 0 TO 3 DO
        r_SumAcc := r_SumAcc + (mat_A[idx_i, idx_j] * a_x_pred_stage1[idx_j]);
    END_FOR;
    FOR idx_k := 0 TO 2 DO
        r_SumAcc := r_SumAcc + (mat_B[idx_i, idx_k] * a_u[idx_k]);
    END_FOR;
    a_x_pred_stage2[idx_i] := r_SumAcc;
END_FOR;

(* Stage 3 Forward State Prediction: x_pred_3 = A * x_pred_2 + B * u2 *)
FOR idx_i := 0 TO 3 DO
    r_SumAcc := 0.0;
    FOR idx_j := 0 TO 3 DO
        r_SumAcc := r_SumAcc + (mat_A[idx_i, idx_j] * a_x_pred_stage2[idx_j]);
    END_FOR;
    FOR idx_k := 0 TO 2 DO
        r_SumAcc := r_SumAcc + (mat_B[idx_i, idx_k] * a_u[idx_k]);
    END_FOR;
    a_x_pred_stage3[idx_i] := r_SumAcc;
END_FOR;

(* Stage 4 Forward State Prediction: x_pred_4 = A * x_pred_3 + B * u3 *)
FOR idx_i := 0 TO 3 DO
    r_SumAcc := 0.0;
    FOR idx_j := 0 TO 3 DO
        r_SumAcc := r_SumAcc + (mat_A[idx_i, idx_j] * a_x_pred_stage3[idx_j]);
    END_FOR;
    FOR idx_k := 0 TO 2 DO
        r_SumAcc := r_SumAcc + (mat_B[idx_i, idx_k] * a_u[idx_k]);
    END_FOR;
    a_x_pred_stage4[idx_i] := r_SumAcc;
END_FOR;

(* Compute Stage Costs: J_stage = x_pred^T * Q * x_pred + u^T * R * u *)
r_MPC_StageCost0 := 0.0;
FOR idx_i := 0 TO 3 DO
    r_MPC_StageCost0 := r_MPC_StageCost0 + (a_x_pred_stage1[idx_i] * mat_Q[idx_i, idx_i] * a_x_pred_stage1[idx_i]);
END_FOR;
FOR idx_k := 0 TO 2 DO
    r_MPC_StageCost0 := r_MPC_StageCost0 + (a_u[idx_k] * mat_R[idx_k, idx_k] * a_u[idx_k]);
END_FOR;

r_MPC_StageCost1 := 0.0;
FOR idx_i := 0 TO 3 DO
    r_MPC_StageCost1 := r_MPC_StageCost1 + (a_x_pred_stage2[idx_i] * mat_Q[idx_i, idx_i] * a_x_pred_stage2[idx_i]);
END_FOR;
FOR idx_k := 0 TO 2 DO
    r_MPC_StageCost1 := r_MPC_StageCost1 + (a_u[idx_k] * mat_R[idx_k, idx_k] * a_u[idx_k]);
END_FOR;

r_MPC_StageCost2 := 0.0;
FOR idx_i := 0 TO 3 DO
    r_MPC_StageCost2 := r_MPC_StageCost2 + (a_x_pred_stage3[idx_i] * mat_Q[idx_i, idx_i] * a_x_pred_stage3[idx_i]);
END_FOR;
FOR idx_k := 0 TO 2 DO
    r_MPC_StageCost2 := r_MPC_StageCost2 + (a_u[idx_k] * mat_R[idx_k, idx_k] * a_u[idx_k]);
END_FOR;

r_MPC_StageCost3 := 0.0;
FOR idx_i := 0 TO 3 DO
    r_MPC_StageCost3 := r_MPC_StageCost3 + (a_x_pred_stage4[idx_i] * mat_Q[idx_i, idx_i] * a_x_pred_stage4[idx_i]);
END_FOR;
FOR idx_k := 0 TO 2 DO
    r_MPC_StageCost3 := r_MPC_StageCost3 + (a_u[idx_k] * mat_R[idx_k, idx_k] * a_u[idx_k]);
END_FOR;

(* Terminal Cost: J_term = x_pred_4^T * P * x_pred_4 *)
r_MPC_TerminalCost := 0.0;
FOR idx_i := 0 TO 3 DO
    r_MPC_TerminalCost := r_MPC_TerminalCost + (a_x_pred_stage4[idx_i] * mat_P[idx_i, idx_i] * a_x_pred_stage4[idx_i]);
END_FOR;

r_MPC_TotalPredictedCost := r_MPC_StageCost0 + r_MPC_StageCost1 + r_MPC_StageCost2 + r_MPC_StageCost3 + r_MPC_TerminalCost;

(* Compute Control Gradient Vector: grad_u = B^T * Q * x_pred_1 + R * u *)
FOR idx_k := 0 TO 2 DO
    r_SumAcc := 0.0;
    FOR idx_i := 0 TO 3 DO
        r_SumAcc := r_SumAcc + (mat_B[idx_i, idx_k] * mat_Q[idx_i, idx_i] * a_x_pred_stage1[idx_i]);
    END_FOR;
    r_SumAcc := r_SumAcc + (mat_R[idx_k, idx_k] * a_u[idx_k]);
    a_grad_u[idx_k] := r_SumAcc;
END_FOR;

(* Receding Horizon Optimal Actuator Correction: Delta_u = - H_inv * grad_u *)
FOR idx_i := 0 TO 2 DO
    r_SumAcc := 0.0;
    FOR idx_j := 0 TO 2 DO
        r_SumAcc := r_SumAcc + (mat_H_inv[idx_i, idx_j] * a_grad_u[idx_j]);
    END_FOR;
    a_u[idx_i] := a_u[idx_i] - (0.350 * r_SumAcc); (* Damped step size *)
END_FOR;

(* Enforce Hard Actuator Saturation Constraints *)
(* u[0]: Robot TCP Normal Correction in micrometers [-1500 um to +1500 um] *)
IF a_u[0] > (r_Limit_Max_NormalOffset_mm * 1000.0) THEN
    a_u[0] := r_Limit_Max_NormalOffset_mm * 1000.0;
ELSIF a_u[0] < (r_Limit_Min_NormalOffset_mm * 1000.0) THEN
    a_u[0] := r_Limit_Min_NormalOffset_mm * 1000.0;
END_IF;

(* u[1]: Robot Speed Trim in mm/s [-35 mm/s to +35 mm/s] *)
IF a_u[1] > r_Limit_Max_SpeedTrim_mmps THEN
    a_u[1] := r_Limit_Max_SpeedTrim_mmps;
ELSIF a_u[1] < r_Limit_Min_SpeedTrim_mmps THEN
    a_u[1] := r_Limit_Min_SpeedTrim_mmps;
END_IF;

(* u[2]: Sealer Dispense Flow Trim in cm3/s [-2.50 to +2.50 cm3/s] *)
IF a_u[2] > r_Limit_Max_FlowTrim_ccps THEN
    a_u[2] := r_Limit_Max_FlowTrim_ccps;
ELSIF a_u[2] < r_Limit_Min_FlowTrim_ccps THEN
    a_u[2] := r_Limit_Min_FlowTrim_ccps;
END_IF;

(* Slew Rate Filter on Actuator Outputs to Avoid Robot Resonant Excitation *)
r_NormalOffset_Cmd_Filtered_mm := r_NormalOffset_Cmd_Filtered_mm + (0.125 * ((a_u[0] * 0.001) - r_NormalOffset_Cmd_Filtered_mm));
r_SpeedTrim_Cmd_Filtered_mmps := r_SpeedTrim_Cmd_Filtered_mmps + (0.125 * (a_u[1] - r_SpeedTrim_Cmd_Filtered_mmps));

(* Assign Output Offset Commands *)
r_RobotTCP_Offset_Normal_mm := r_NormalOffset_Cmd_Filtered_mm;
r_RobotTCP_Offset_Lateral_mm := (r_LaserSensor_FlangeGap_mm - 1.00) * 0.350; (* Lateral centering offset *)

(* Modulated Robot Traverse Speed Command *)
IF b_HemmingCycleActive THEN
    r_RobotTCP_TargetVelocity_mmps := r_NominalPathSpeed_mmps + r_SpeedTrim_Cmd_Filtered_mmps;
    IF r_RobotTCP_TargetVelocity_mmps < 40.0 THEN
        r_RobotTCP_TargetVelocity_mmps := 40.0;
    ELSIF r_RobotTCP_TargetVelocity_mmps > 300.0 THEN
        r_RobotTCP_TargetVelocity_mmps := 300.0;
    END_IF;
ELSE
    r_RobotTCP_TargetVelocity_mmps := 0.0;
END_IF;
''')

    # Section 8: Multi-Stage Finite State Machine
    sections.append('''
(* ============================================================================================= *)
(* SECTION 8: MULTI-STAGE SEQUENTIAL FINITE STATE MACHINE (FSM) ENGINE                           *)
(* ============================================================================================= *)
IF b_StateFirstCycle THEN
    b_StateFirstCycle := FALSE;
    r_StateTimer_Sec := 0.0;
    r_StateDwellTimer_Sec := 0.0;
ELSE
    r_StateTimer_Sec := r_StateTimer_Sec + r_DeltaT_Sec;
    r_StateDwellTimer_Sec := r_StateDwellTimer_Sec + r_DeltaT_Sec;
END_IF;

CASE i_CurrentFSM_State OF

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 0: CELL IDLE - AWAITING PRODUCTION AUTHORIZATION & PART DOCKING                     *)
    (* ----------------------------------------------------------------------------------------- *)
    STATE_CELL_IDLE:
        b_CellReady := TRUE;
        b_HemmingCycleActive := FALSE;
        b_HemmingCycleComplete := FALSE;
        b_PartUnclamp_Permit := FALSE;
        b_VacuumGripper_Command := FALSE;
        b_ServoClamps_EngageCmd := FALSE;
        b_SealerNozzle_Open := FALSE;
        r_HemmingPathProgress_Percent := 0.0;
        r_InterpolatedDistance_mm := 0.0;
        b_VisionOffsets_Computed := FALSE;

        IF b_EnableCell AND b_EmergencyStop_OK AND b_SafetyGate_Closed AND b_PartLoaded_DockTrigger THEN
            i_NextFSM_State := STATE_INNER_OUTER_PANEL_DOCK;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 10: INNER & OUTER CLOSURE PANEL DOCKING ON FIXTURE NEST                             *)
    (* ----------------------------------------------------------------------------------------- *)
    STATE_INNER_OUTER_PANEL_DOCK:
        b_CellReady := FALSE;
        b_HemmingCycleActive := TRUE;
        b_HemmingCycleComplete := FALSE;
        b_VacuumGripper_Command := TRUE; (* Start vacuum generator pull-down *)

        (* Dwell for Overhead Gantry Drop Confirmation (1.200 Seconds) *)
        IF r_StateTimer_Sec >= 1.200 THEN
            IF r_VacuumTooling_Level_kPa <= -40.0 THEN
                i_NextFSM_State := STATE_VACUUM_CLAMP_ENGAGE;
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 20: VACUUM SUCTION BED ENGAGE & MOTORIZED LOCATING PIN CLAMP LOCK                   *)
    (* ----------------------------------------------------------------------------------------- *)
    STATE_VACUUM_CLAMP_ENGAGE:
        b_VacuumGripper_Command := TRUE;
        b_ServoClamps_EngageCmd := TRUE; (* Lock motorized shot pins *)

        (* Verify Full Vacuum Saturation (Below -70.0 kPa) & Clamp Dwell *)
        IF (r_VacuumTooling_Level_kPa <= -70.0) AND (r_StateTimer_Sec >= 1.500) THEN
            b_VacuumSensors_AllOK := TRUE;
            b_ServoClamps_AllLocked := TRUE;
            i_NextFSM_State := STATE_3D_VISION_ALIGN_OFFSETS;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 30: 3D OPTICAL VISION SCANNING & PART FIXTURING OFFSET COMPENSATION                *)
    (* ----------------------------------------------------------------------------------------- *)
    STATE_3D_VISION_ALIGN_OFFSETS:
        (* Scan Panel Flange Edge Contour with Perceptron 3D Laser *)
        IF r_StateTimer_Sec >= 0.800 THEN
            (* Compute Part Fixturing Spatial Translation & Rotation Offsets *)
            r_Vision_OffsetX_mm := (r_LaserSensor_FlangeGap_mm - 1.05) * 0.450;
            r_Vision_OffsetY_mm := (r_LaserSensor_Flushness_mm - 0.10) * 0.350;
            r_Vision_OffsetZ_mm := (r_Voted_RollIn_mm - 1.85) * 0.500;
            b_VisionOffsets_Computed := TRUE;

            IF b_VisionOffsets_Computed THEN
                i_NextFSM_State := STATE_MASTIC_SEALER_DISPENSE;
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 40: VOLUMETRIC HIGH-PRESSURE MASTIC SEALER BEAD DISPENSING                          *)
    (* ----------------------------------------------------------------------------------------- *)
    STATE_MASTIC_SEALER_DISPENSE:
        b_SealerNozzle_Open := TRUE;
        r_InterpolatedDistance_mm := r_InterpolatedDistance_mm + (r_RobotTCP_ActualVelocity_mmps * r_DeltaT_Sec);
        r_HemmingPathProgress_Percent := (r_InterpolatedDistance_mm / r_TotalPathLength_mm) * 100.0;

        (* Check Dispensing Path Complete *)
        IF (r_HemmingPathProgress_Percent >= 100.0) OR (r_StateTimer_Sec >= 25.0) THEN
            b_SealerNozzle_Open := FALSE;
            r_SealerPump_FlowCmd_ccps := 0.0;
            r_SealerPump_SpeedCmd_RPM := 0.0;
            r_InterpolatedDistance_mm := 0.0;
            r_HemmingPathProgress_Percent := 0.0;
            i_NextFSM_State := STATE_FLANGE_PRE_HEM_45DEG;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 50: HIGH-SPEED ROLLER PRE-HEMMING PASS (45 DEGREE ROLLER HEAD)                      *)
    (* ----------------------------------------------------------------------------------------- *)
    STATE_FLANGE_PRE_HEM_45DEG:
        b_SealerNozzle_Open := FALSE;
        r_InterpolatedDistance_mm := r_InterpolatedDistance_mm + (r_RobotTCP_ActualVelocity_mmps * r_DeltaT_Sec);
        r_HemmingPathProgress_Percent := (r_InterpolatedDistance_mm / r_TotalPathLength_mm) * 100.0;

        (* Check 45 Degree Pre-Hemming Contour Completed *)
        IF (r_HemmingPathProgress_Percent >= 100.0) OR (r_StateTimer_Sec >= 24.0) THEN
            r_InterpolatedDistance_mm := 0.0;
            r_HemmingPathProgress_Percent := 0.0;
            i_NextFSM_State := STATE_INTERMEDIATE_HEM_75DEG;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 60: ROLLER INTERMEDIATE HEMMING PASS (75 DEGREE ROLLER HEAD)                        *)
    (* ----------------------------------------------------------------------------------------- *)
    STATE_INTERMEDIATE_HEM_75DEG:
        r_InterpolatedDistance_mm := r_InterpolatedDistance_mm + (r_RobotTCP_ActualVelocity_mmps * r_DeltaT_Sec);
        r_HemmingPathProgress_Percent := (r_InterpolatedDistance_mm / r_TotalPathLength_mm) * 100.0;

        (* Check 75 Degree Intermediate Hemming Contour Completed *)
        IF (r_HemmingPathProgress_Percent >= 100.0) OR (r_StateTimer_Sec >= 24.0) THEN
            r_InterpolatedDistance_mm := 0.0;
            r_HemmingPathProgress_Percent := 0.0;
            i_NextFSM_State := STATE_FINAL_FLAT_HEM_90DEG;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 70: FINAL FLAT ROLLER HEMMING PASS (90 DEGREE FLAT ROLLER HEAD)                     *)
    (* ----------------------------------------------------------------------------------------- *)
    STATE_FINAL_FLAT_HEM_90DEG:
        r_InterpolatedDistance_mm := r_InterpolatedDistance_mm + (r_RobotTCP_ActualVelocity_mmps * r_DeltaT_Sec);
        r_HemmingPathProgress_Percent := (r_InterpolatedDistance_mm / r_TotalPathLength_mm) * 100.0;

        (* Check 90 Degree Flat Hemming Contour Completed *)
        IF (r_HemmingPathProgress_Percent >= 100.0) OR (r_StateTimer_Sec >= 24.0) THEN
            r_InterpolatedDistance_mm := 0.0;
            r_HemmingPathProgress_Percent := 0.0;
            i_NextFSM_State := STATE_GAP_FLUSH_OPTICAL_AUDIT;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 80: POST-PROCESS 3D LASER OPTICAL GAP & FLUSHNESS QUALITY AUDIT                     *)
    (* ----------------------------------------------------------------------------------------- *)
    STATE_GAP_FLUSH_OPTICAL_AUDIT:
        r_RobotTCP_TargetVelocity_mmps := 0.0;
        r_RobotTCP_Offset_Normal_mm := 0.0;
        r_RobotTCP_Offset_Lateral_mm := 0.0;

        IF r_StateTimer_Sec >= 1.500 THEN
            (* Verify Hemmed Flange Dimensional Quality Acceptance Criteria *)
            IF (r_LaserSensor_FlangeGap_mm <= r_FlangeGap_Max_mm) AND 
               (r_LaserSensor_FlangeGap_mm >= r_FlangeGap_Min_mm) AND 
               (r_LaserSensor_Flushness_mm <= r_Flushness_Max_mm) AND 
               (r_LaserSensor_Flushness_mm >= r_Flushness_Min_mm) THEN
                b_AlarmLatched_GapFlush_Fault := FALSE;
                i_NextFSM_State := STATE_PART_UNCLAMP_EJECT;
            ELSE
                b_AlarmLatched_GapFlush_Fault := TRUE;
                i_NextFSM_State := STATE_PART_UNCLAMP_EJECT;
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 90: VACUUM DISSIPATION, SERVO CLAMP RETRACT & UNLOAD PERMIT                         *)
    (* ----------------------------------------------------------------------------------------- *)
    STATE_PART_UNCLAMP_EJECT:
        b_VacuumGripper_Command := FALSE; (* Turn off vacuum, engage blow-off release *)
        b_ServoClamps_EngageCmd := FALSE; (* Retract shot-pin clamps *)
        b_HemmingCycleActive := FALSE;

        IF r_StateTimer_Sec >= 1.500 THEN
            b_PartUnclamp_Permit := TRUE;
            b_HemmingCycleComplete := TRUE;
            (* Return to Idle Upon Part Extraction by Unloading Robot *)
            IF NOT b_PartLoaded_DockTrigger THEN
                i_NextFSM_State := STATE_CELL_IDLE;
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 99: ROLLER FORCE OVERLOAD / CRASH EMERGENCY SHUTDOWN TRIP                           *)
    (* ----------------------------------------------------------------------------------------- *)
    STATE_ROLLER_FORCE_OVERLOAD_TRIP:
        b_EmergencyStop_Active := TRUE;
        b_CellReady := FALSE;
        b_HemmingCycleActive := FALSE;
        b_HemmingCycleComplete := FALSE;
        b_PartUnclamp_Permit := FALSE;
        b_SealerNozzle_Open := FALSE;
        r_SealerPump_FlowCmd_ccps := 0.0;
        r_SealerPump_SpeedCmd_RPM := 0.0;
        r_RobotTCP_TargetVelocity_mmps := 0.0;
        r_RobotTCP_Offset_Normal_mm := 0.0;
        r_RobotTCP_Offset_Lateral_mm := 0.0;

        (* Reset Sequence Upon Safety OK & Alarm Acknowledgment *)
        IF b_AlarmReset AND b_EmergencyStop_OK AND b_SafetyGate_Closed AND 
           NOT b_AlarmLatched_Crash_HH AND NOT b_AlarmLatched_Force_HH THEN
            b_EmergencyStop_Active := FALSE;
            i_NextFSM_State := STATE_CELL_IDLE;
        END_IF;

ELSE
    i_CurrentFSM_State := STATE_CELL_IDLE;
    i_NextFSM_State := STATE_CELL_IDLE;
END_CASE;

(* FSM Transition Update *)
IF i_NextFSM_State <> i_CurrentFSM_State THEN
    i_CurrentFSM_State := i_NextFSM_State;
    b_StateFirstCycle := TRUE;
END_IF;
''')

    # Section 9: ISA-18.2 Multi-Tiered Alarm Matrix & Diagnostic Registers
    sections.append('''
(* ============================================================================================= *)
(* SECTION 9: ISA-18.2 MULTI-TIERED ALARM LADDER & DIAGNOSTIC WORD BITFIELD PACKING              *)
(* ============================================================================================= *)
(* 1. Hemming Roller Normal Pressing Force Monitoring *)
(* Level HH (Trip Limit = 2250.0 N) *)
IF r_HemmingContactForce_Fz_Net_N >= r_Force_HH_Trip_N THEN
    r_AlarmTimer_Force_HH := r_AlarmTimer_Force_HH + r_DeltaT_Sec;
    IF r_AlarmTimer_Force_HH >= r_QualDelay_Trip_Sec THEN
        b_AlarmLatched_Force_HH := TRUE;
        i_NextFSM_State := STATE_ROLLER_FORCE_OVERLOAD_TRIP;
    END_IF;
ELSIF r_HemmingContactForce_Fz_Net_N <= (r_Force_HH_Trip_N - r_Force_Deadband_N) THEN
    r_AlarmTimer_Force_HH := 0.0;
    IF b_AlarmReset THEN
        b_AlarmLatched_Force_HH := FALSE;
    END_IF;
END_IF;

(* Level H (Warning Limit = 2050.0 N) *)
IF r_HemmingContactForce_Fz_Net_N >= r_Force_H_Warn_N THEN
    r_AlarmTimer_Force_H := r_AlarmTimer_Force_H + r_DeltaT_Sec;
    IF r_AlarmTimer_Force_H >= r_QualDelay_Warn_Sec THEN
        b_AlarmLatched_Force_H := TRUE;
    END_IF;
ELSIF r_HemmingContactForce_Fz_Net_N <= (r_Force_H_Warn_N - r_Force_Deadband_N) THEN
    r_AlarmTimer_Force_H := 0.0;
    IF b_AlarmReset THEN
        b_AlarmLatched_Force_H := FALSE;
    END_IF;
END_IF;

(* Level L (Warning Limit = 1450.0 N) - Evaluated Only During Active Hemming Pass *)
IF b_HemmingCycleActive AND (i_CurrentFSM_State >= STATE_FLANGE_PRE_HEM_45DEG) AND (i_CurrentFSM_State <= STATE_FINAL_FLAT_HEM_90DEG) THEN
    IF r_HemmingContactForce_Fz_Net_N <= r_Force_L_Warn_N THEN
        r_AlarmTimer_Force_L := r_AlarmTimer_Force_L + r_DeltaT_Sec;
        IF r_AlarmTimer_Force_L >= r_QualDelay_Warn_Sec THEN
            b_AlarmLatched_Force_L := TRUE;
        END_IF;
    ELSIF r_HemmingContactForce_Fz_Net_N >= (r_Force_L_Warn_N + r_Force_Deadband_N) THEN
        r_AlarmTimer_Force_L := 0.0;
        IF b_AlarmReset THEN
            b_AlarmLatched_Force_L := FALSE;
        END_IF;
    END_IF;

    (* Level LL (Disengaged Abort Limit = 1100.0 N) *)
    IF r_HemmingContactForce_Fz_Net_N <= r_Force_LL_Trip_N THEN
        r_AlarmTimer_Force_LL := r_AlarmTimer_Force_LL + r_DeltaT_Sec;
        IF r_AlarmTimer_Force_LL >= r_QualDelay_Trip_Sec THEN
            b_AlarmLatched_Force_LL := TRUE;
            i_NextFSM_State := STATE_ROLLER_FORCE_OVERLOAD_TRIP;
        END_IF;
    ELSIF r_HemmingContactForce_Fz_Net_N >= (r_Force_LL_Trip_N + r_Force_Deadband_N) THEN
        r_AlarmTimer_Force_LL := 0.0;
        IF b_AlarmReset THEN
            b_AlarmLatched_Force_LL := FALSE;
        END_IF;
    END_IF;
ELSE
    r_AlarmTimer_Force_L := 0.0;
    r_AlarmTimer_Force_LL := 0.0;
END_IF;

(* 2. Sealer Injection Manifold Pressure Monitoring *)
(* Level HH (Blocked Nozzle Trip = 220.0 bar) *)
IF r_SealerDispense_Pressure_bar >= r_Press_HH_Trip_bar THEN
    r_AlarmTimer_Press_HH := r_AlarmTimer_Press_HH + r_DeltaT_Sec;
    IF r_AlarmTimer_Press_HH >= r_QualDelay_Trip_Sec THEN
        b_AlarmLatched_Press_HH := TRUE;
        b_SealerNozzle_Open := FALSE;
    END_IF;
ELSIF r_SealerDispense_Pressure_bar <= (r_Press_HH_Trip_bar - r_Press_Deadband_bar) THEN
    r_AlarmTimer_Press_HH := 0.0;
    IF b_AlarmReset THEN
        b_AlarmLatched_Press_HH := FALSE;
    END_IF;
END_IF;

(* Level H (Warning Limit = 185.0 bar) *)
IF r_SealerDispense_Pressure_bar >= r_Press_H_Warn_bar THEN
    r_AlarmTimer_Press_H := r_AlarmTimer_Press_H + r_DeltaT_Sec;
    IF r_AlarmTimer_Press_H >= r_QualDelay_Warn_Sec THEN
        b_AlarmLatched_Press_H := TRUE;
    END_IF;
ELSIF r_SealerDispense_Pressure_bar <= (r_Press_H_Warn_bar - r_Press_Deadband_bar) THEN
    r_AlarmTimer_Press_H := 0.0;
    IF b_AlarmReset THEN
        b_AlarmLatched_Press_H := FALSE;
    END_IF;
END_IF;

(* Level LL (Starvation / Air Bubble Fault = 45.0 bar during active dispensing) *)
IF b_SealerNozzle_Open AND (r_StateTimer_Sec >= 0.500) THEN
    IF r_SealerDispense_Pressure_bar <= r_Press_LL_Trip_bar THEN
        r_AlarmTimer_Press_LL := r_AlarmTimer_Press_LL + r_DeltaT_Sec;
        IF r_AlarmTimer_Press_LL >= r_QualDelay_Trip_Sec THEN
            b_AlarmLatched_Press_LL := TRUE;
        END_IF;
    ELSIF r_SealerDispense_Pressure_bar >= (r_Press_LL_Trip_bar + r_Press_Deadband_bar) THEN
        r_AlarmTimer_Press_LL := 0.0;
        IF b_AlarmReset THEN
            b_AlarmLatched_Press_LL := FALSE;
        END_IF;
    END_IF;
ELSE
    r_AlarmTimer_Press_LL := 0.0;
END_IF;

(* 3. ATI 6-Axis Resultant Force/Torque Crash Monitoring *)
IF (r_ResultantForce_N >= r_Force_Resultant_HH_Crash_N) OR (r_ResultantTorque_Nm >= r_Torque_Resultant_HH_Crash_Nm) THEN
    r_AlarmTimer_Crash_HH := r_AlarmTimer_Crash_HH + r_DeltaT_Sec;
    IF r_AlarmTimer_Crash_HH >= r_QualDelay_Trip_Sec THEN
        b_AlarmLatched_Crash_HH := TRUE;
        i_NextFSM_State := STATE_ROLLER_FORCE_OVERLOAD_TRIP;
    END_IF;
ELSE
    r_AlarmTimer_Crash_HH := 0.0;
    IF b_AlarmReset THEN
        b_AlarmLatched_Crash_HH := FALSE;
    END_IF;
END_IF;

(* 4. Tooling Nest Vacuum Level Holding Fault *)
IF b_VacuumGripper_Command AND (r_StateTimer_Sec >= 1.000) THEN
    IF r_VacuumTooling_Level_kPa > r_Vacuum_LL_Fault_kPa THEN
        r_AlarmTimer_Vacuum_LL := r_AlarmTimer_Vacuum_LL + r_DeltaT_Sec;
        IF r_AlarmTimer_Vacuum_LL >= r_QualDelay_Trip_Sec THEN
            b_AlarmLatched_Vacuum_LL := TRUE;
        END_IF;
    ELSE
        r_AlarmTimer_Vacuum_LL := 0.0;
        IF b_AlarmReset THEN
            b_AlarmLatched_Vacuum_LL := FALSE;
        END_IF;
    END_IF;
ELSE
    r_AlarmTimer_Vacuum_LL := 0.0;
END_IF;

(* Reset TMR Discrepancy Latch on Master Alarm Reset *)
IF b_AlarmReset THEN
    b_AlarmLatched_TMR_Trip := FALSE;
    b_AlarmLatched_GapFlush_Fault := FALSE;
END_IF;

(* ============================================================================================= *)
(* BITFIELD PACKING: CELL STATUS WORD & ISA-18.2 ALARM WORDS                                      *)
(* ============================================================================================= *)
(* Cell Status Word (16-bit register) *)
w_CellStatusWord := 16#0000;
IF b_CellReady THEN
    w_CellStatusWord := w_CellStatusWord OR 16#0001;
END_IF;
IF b_HemmingCycleActive THEN
    w_CellStatusWord := w_CellStatusWord OR 16#0002;
END_IF;
IF b_HemmingCycleComplete THEN
    w_CellStatusWord := w_CellStatusWord OR 16#0004;
END_IF;
IF b_PartUnclamp_Permit THEN
    w_CellStatusWord := w_CellStatusWord OR 16#0008;
END_IF;
IF b_VacuumGripper_Command THEN
    w_CellStatusWord := w_CellStatusWord OR 16#0010;
END_IF;
IF b_ServoClamps_EngageCmd THEN
    w_CellStatusWord := w_CellStatusWord OR 16#0020;
END_IF;
IF b_SealerNozzle_Open THEN
    w_CellStatusWord := w_CellStatusWord OR 16#0040;
END_IF;
IF b_EmergencyStop_Active THEN
    w_CellStatusWord := w_CellStatusWord OR 16#0080;
END_IF;
IF b_TMR_Degraded_2oo2 THEN
    w_CellStatusWord := w_CellStatusWord OR 16#0100;
END_IF;
IF b_AirWipePurge_Active THEN
    w_CellStatusWord := w_CellStatusWord OR 16#0200;
END_IF;

(* ISA-18.2 Alarm Word #1 (Process Operational Warnings and Trips) *)
w_ISA_AlarmWord_1 := 16#00000000;
IF b_AlarmLatched_Force_HH THEN
    w_ISA_AlarmWord_1 := w_ISA_AlarmWord_1 OR 16#00000001;
END_IF;
IF b_AlarmLatched_Force_H THEN
    w_ISA_AlarmWord_1 := w_ISA_AlarmWord_1 OR 16#00000002;
END_IF;
IF b_AlarmLatched_Force_L THEN
    w_ISA_AlarmWord_1 := w_ISA_AlarmWord_1 OR 16#00000004;
END_IF;
IF b_AlarmLatched_Force_LL THEN
    w_ISA_AlarmWord_1 := w_ISA_AlarmWord_1 OR 16#00000008;
END_IF;
IF b_AlarmLatched_Press_HH THEN
    w_ISA_AlarmWord_1 := w_ISA_AlarmWord_1 OR 16#00000010;
END_IF;
IF b_AlarmLatched_Press_H THEN
    w_ISA_AlarmWord_1 := w_ISA_AlarmWord_1 OR 16#00000020;
END_IF;
IF b_AlarmLatched_Press_LL THEN
    w_ISA_AlarmWord_1 := w_ISA_AlarmWord_1 OR 16#00000040;
END_IF;
IF b_AlarmLatched_Crash_HH THEN
    w_ISA_AlarmWord_1 := w_ISA_AlarmWord_1 OR 16#00000080;
END_IF;
IF b_AlarmLatched_Vacuum_LL THEN
    w_ISA_AlarmWord_1 := w_ISA_AlarmWord_1 OR 16#00000100;
END_IF;

(* ISA-18.2 Alarm Word #2 (Hardware Discrepancies, Quality & Sensor Diagnostics) *)
w_ISA_AlarmWord_2 := 16#00000000;
IF b_AlarmLatched_TMR_Trip THEN
    w_ISA_AlarmWord_2 := w_ISA_AlarmWord_2 OR 16#00000001;
END_IF;
IF b_Discrepancy_AB_Tripped THEN
    w_ISA_AlarmWord_2 := w_ISA_AlarmWord_2 OR 16#00000002;
END_IF;
IF b_Discrepancy_BC_Tripped THEN
    w_ISA_AlarmWord_2 := w_ISA_AlarmWord_2 OR 16#00000004;
END_IF;
IF b_Discrepancy_CA_Tripped THEN
    w_ISA_AlarmWord_2 := w_ISA_AlarmWord_2 OR 16#00000008;
END_IF;
IF b_AlarmLatched_GapFlush_Fault THEN
    w_ISA_AlarmWord_2 := w_ISA_AlarmWord_2 OR 16#00000010;
END_IF;
IF NOT b_SensorA_Valid THEN
    w_ISA_AlarmWord_2 := w_ISA_AlarmWord_2 OR 16#00000020;
END_IF;
IF NOT b_SensorB_Valid THEN
    w_ISA_AlarmWord_2 := w_ISA_AlarmWord_2 OR 16#00000040;
END_IF;
IF NOT b_SensorC_Valid THEN
    w_ISA_AlarmWord_2 := w_ISA_AlarmWord_2 OR 16#00000080;
END_IF;

END_FUNCTION_BLOCK
''')

    return "".join(sections)

def save_dataset():
    st_code = generate_st_code()
    
    # Validation checks
    assert st_code.startswith("FUNCTION_BLOCK FB_Automotive_BIW_RoboticRollerHemming_Sealer"), "First line invalid"
    assert st_code.strip().endswith("END_FUNCTION_BLOCK"), "Last line invalid"
    
    code_no_comments = re.sub(r'\(\*[\s\S]*?\*\)', '', st_code)
    ifs = len(re.findall(r'\bIF\b', code_no_comments))
    end_ifs = len(re.findall(r'\bEND_IF\b', code_no_comments))
    assert ifs == end_ifs, f"IF ({ifs}) != END_IF ({end_ifs})"
    
    cases = len(re.findall(r'\bCASE\b', code_no_comments))
    end_cases = len(re.findall(r'\bEND_CASE\b', code_no_comments))
    assert cases == end_cases, f"CASE ({cases}) != END_CASE ({end_cases})"
    
    fors = len(re.findall(r'\bFOR\b', code_no_comments))
    end_fors = len(re.findall(r'\bEND_FOR\b', code_no_comments))
    assert fors == end_fors, f"FOR ({fors}) != END_FOR ({end_fors})"
    
    # Exact code block formatting
    code_fenced = f"```iec-st\n{st_code}\n```"
    
    record = {
        "messages": [
            {"role": "user", "content": USER_PROMPT},
            {"role": "assistant", "content": code_fenced}
        ]
    }
    
    agent_id = uuid.uuid4().hex[:8]
    filename = f"data/swarm_raw/agent_{agent_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully validated and saved dataset to {filename}")
    print(f"Character count of ST code: {len(st_code)}")
    print(f"Total assistant message character count: {len(code_fenced)}")
    return filename

if __name__ == '__main__':
    save_dataset()
