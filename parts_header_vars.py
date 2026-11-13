# parts_header_vars.py

PROMPT_TEXT = """You are assigned to generate ONE production-grade, ultra-dense, mathematically complete IEC 61131-3 Structured Text synthetic training dataset.

### Assignment:
- **Commercial Industry**: Mechanical Engineering & Heavy Machine Tools (Tier 1 Priority Sector)
- **Target Automation System**: Heavy 5-Axis Gantry CNC Milling Center (100 kW, 24,000 rpm Motor Spindle)
  - Dynamic sensorless thermal spindle expansion compensation with multi-node thermal nodal network
  - Multi-axis cross-coupling error decoupling with dual-drive gantry synchronization (electronic line-shafting / yaw compensation) and 5-axis kinematic TCP Jacobian transformation
  - Inertial mass active acceleration vibration damping (AIMD) minimizing tool tip chatter and path contour error during high-jerk directional changes
  - Tool tip deflection observer estimating instantaneous cantilever bending and dynamic spindle nose tilt
- **Function Block Name**: `FB_Machining_5AxisGantry_ThermalSpindleComp_ActiveDamping`

### Quality Directives (V7 Max-Persona Protocol):
1. **Extreme Token & Character Density**: Target 75,000 to 125,000+ characters. Zero placeholders, zero ellipses, every equation and state transition fully coded.
2. **First-Principles Cyber-Physical Formulation**:
   - 10-State discrete state-space formulation (x[k+1] = A*x[k] + B*u[k], y[k] = C*x[k] + D*u[k]) at Ts = 1 ms for 5-axis positions (X, Y, Z, A, C), structural velocities, spindle rotor thermal growth Delta Lz(T), bearing preload variation, cutting force magnitude, and active damping mass displacement.
   - Receding-horizon Model Predictive Control (MPC) with multi-objective quadratic cost functional (Q, R, S, P), projected gradient descent (PGD) with physical actuator box saturation and dynamic slew rate limiters.
   - 2oo3 Triple Modular Redundancy (TMR) voting across critical sensor channels (Linear Encoders X/Y/Z 1A/B/C, Spindle Rotary Encoders 2A/B/C, Spindle Bearing RTD Temp Sensors 3A/B/C, 3-Axis Accelerometers on Spindle Nose 4A/B/C) with discrepancy timers and bumpless degradation.
   - Deterministic 14-stage operational Finite State Machine (CASE nActiveFSMStage OF ... END_CASE) covering chiller pre-cooling, axis homing & laser cal, thermal pre-heat cycle, tool clamp runout verification, adaptive roughing cut, active chatter suppression, precision finish contouring, tool wear probe inspection, spindle orientation lock, ATC tool change sequence, coolant & chip conveyor mgmt, workpiece touch probe check, safe axis retract, and collision emergency brake failsafe.
   - ISA-18.2 multi-tiered alarm hierarchy (Critical, High, Medium, Advisory) with clearance deadbands and bit-packed DWORD status/diagnostic words.
   - Physical engineering units in brackets for all I/O variables: [mm], [um], [m/min], [rpm], [deg C], [N], [m/s2], [bar], [kW], [%].
3. **Parity & Validation**:
   - 100% exact parity: IF/END_IF;, CASE/END_CASE;, FOR/END_FOR;, FUNCTION_BLOCK/END_FUNCTION_BLOCK.
   - Save to isolated JSON file at data/swarm_raw/agent_<uuid>.json with user prompt and assistant response.
   - Run python validate_iec.py data/swarm_raw/agent_<uuid>.json to verify 0 errors.
4. **Completion Message**:
   Reply to the parent agent with: EVOLUTION COMPLETE: Heavy 5-Axis Gantry CNC Milling Center along with system details, character count, and parity audit results."""

HEADER_COMMENT = """FUNCTION_BLOCK FB_Machining_5AxisGantry_ThermalSpindleComp_ActiveDamping
(*
========================================================================================================================
  LUMINA AI CYBER-PHYSICAL SYSTEMS & ADVANCED INDUSTRIAL AUTOMATION ARCHITECTURE GROUP
  HEAVY MACHINE TOOLS & 5-AXIS CNC GANTRY MACHINING CENTERS REFERENCE IMPLEMENTATION — SYNTHETIC DATASET ENGINE V7
  
  SYSTEM DESIGNATION   : HEAVY 5-AXIS GANTRY CNC MILLING CENTER WITH HIGH-SPEED MOTOR SPINDLE & ACTIVE CHATTER DAMPING
  SPINDLE ARCHITECTURE : 100 kW BUILT-IN SYNCHRONOUS MOTOR SPINDLE (24,000 RPM, HSK-A100 / HSK-E63 TAPER INTERFACE)
  THERMAL COMPENSATION : SENSORLESS MULTI-NODE THERMAL EXPANSION OBSERVER & DYNAMIC ROTOR Z-AXIS OFFSET INJECTION
  AXIS SYNCHRONIZATION : DUAL-DRIVE GANTRY LINE-SHAFT DECOUPLING & 5-AXIS KINEMATIC TOOL CENTER POINT (TCP) JACOBIAN
  VIBRATION DAMPING    : VOICE-COIL ACTIVE INERTIAL MASS ACCELERATION DAMPING (AIMD) & SPINDLE SPEED VARIATION (SSV)
  SAFETY INTEGRITY     : ISO 13849-1 PL e / IEC 62061 SIL-3 CERTIFIED MACHINE TOOL SAFETY ARCHITECTURE
  APPLICABLE STANDARDS : ISO 230-1 / ISO 230-2 (TEST CODE FOR MACHINE TOOLS - ACCURACY & REPEATABILITY),
                         ISO 230-3 (THERMAL EFFECTS DETERMINATION ON MACHINE TOOLS),
                         ISO 10791 (TEST CONDITIONS FOR MACHINING CENTERS),
                         ISO 1940-1 (MECHANICAL VIBRATION - BALANCE QUALITY REQUIREMENTS OF ROTORS),
                         DIN EN 12417 (MACHINE TOOLS - SAFETY - MACHINING CENTERS),
                         ISA-18.2 / IEC 62682 (MANAGEMENT OF ALARM SYSTEMS FOR THE PROCESS INDUSTRIES).
  AUTHOR               : 75+ YEARS VETERAN PRINCIPAL AUTOMATION FELLOW & CYBER-PHYSICAL SYSTEMS CHAIR
========================================================================================================================

  THEORETICAL & CYBER-PHYSICAL DYNAMICS OF HEAVY 5-AXIS GANTRY MACHINING:
  ----------------------------------------------------------------------------------------------------------------------
  1. MULTI-NODE LUMPED THERMAL PARAMETER NETWORK & ROTOR AXIAL GROWTH (ISO 230-3):
     - High-speed 100 kW synchronous motor spindles subject to substantial internal heat generation sources:
       a) Stator Joule copper losses: P_cu = 3 * R_s(T) * I_s^2 [W]
       b) Stator core magnetic hysteresis and eddy current iron losses: P_fe = K_h * f_e + K_e * f_e^2 [W]
       c) Hybrid ceramic angular contact bearing viscous shear and friction torque: P_brg = M_brg * omega_m [W]
          where M_brg = f0 * (v_lub * omega_m)^(2/3) * d_m^3 * 10^-7 + f1 * P1 * d_m [N*m] (per Palmgren formulation)
       d) Cutting process heat conduction through tool holder taper: Q_cut = eta_cut * F_c * v_c [W]
     - Closed-loop glycol chiller jacket heat extraction:
          Q_chiller = m_dot_cool * C_p_glycol * (T_chiller_out - T_chiller_in) [W]
     - Multi-node differential heat balance equations across 6 thermal state domains:
          Node 1: Spindle Rotor Core & Shaft
          Node 2: Stator Winding & Stator Iron Core
          Node 3: Front Tandem Hybrid Ceramic Bearing Pack (Fixed Datum)
          Node 4: Rear Floating Hybrid Ceramic Bearing Pack
          Node 5: Cast Iron Spindle Housing Carrier & Z-Axis Ram
          Node 6: Liquid Cooling Glycol Boundary Layer
     - Resultant cumulative axial thermal growth along tool axis Z:
          Delta_L_z(t) = alpha_shaft * Integral[T_rotor(z) - T_0] dz + alpha_brg * L_brg * [T_front - T_0]
                         - alpha_ram * L_ram * [T_housing - T_0] - K_centrif * omega_m^2  [um]
       where the centrifugal term (- K_centrif * omega_m^2) accounts for Poisson contraction of the spinning shaft
       and radial dilation of bearing rings under high centrifugal loads.
     - Dynamic bearing preload variation:
          Delta_F_pre(t) = K_dT * [T_inner_ring - T_outer_ring] + K_omega * omega_m [N]
       Excessive differential thermal expansion between inner and outer bearing rings leads to thermal runaway
       and catastrophic seizure if not dynamically counter-regulated.

  2. DUAL-DRIVE GANTRY CROSS-COUPLING DECOUPLING & 5-AXIS KINEMATIC TOOL CENTER POINT (TCP):
     - Gantry bridge structure of width W_gantry [m] driven symmetrically by twin linear permanent magnet synchronous
       motors (X1 Master, X2 Slave). Asymmetric cutting forces and mass carriage travel induce bridge yaw rotation:
          e_yaw(t) = X1_scale(t) - X2_scale(t)  [mm]
          phi_yaw(t) = e_yaw(t) / W_gantry      [rad]
     - Dynamic cross-coupling decoupling control incorporates electronic line-shafting:
          F_yaw_correction = K_p_yaw * e_yaw + K_d_yaw * (de_yaw / dt) + K_i_yaw * Integral[e_yaw dt]  [N]
     - 5-Axis Forward Kinematics (Trunnion Table Topology A-C Axes):
       Let tool vector in spindle reference frame be p_tool = [0, 0, -L_tool]^T.
       Under trunnion tilt angle A (around X-axis) and rotary table angle C (around Z-axis):
          R_C(C) = [ cos(C) -sin(C) 0 ; sin(C) cos(C) 0 ; 0 0 1 ]
          R_A(A) = [ 1 0 0 ; 0 cos(A) -sin(A) ; 0 sin(A) cos(A) ]
          p_tcp(t) = p_gantry(t) + R_C(C) * R_A(A) * [p_tool + delta_deflection(t) + delta_thermal(t)]
       The Jacobian matrix J(q) relates joint velocity space to tool center point Cartesian velocities:
          v_tcp = J(q) * dq/dt
       Thermal and deflection compensation offsets are projected inversely through J^-1(q) into drive setpoints.

  3. REGENERATIVE CHATTER VIBRATION & ACTIVE INERTIAL MASS ACCELERATION DAMPING (AIMD):
     - Self-excited regenerative chatter in end-milling occurs when dynamic cutting force excites structural modes:
          F_c(t) = K_t * a_p * [h_0 - (x_struct(t) - x_struct(t - tau_tooth))]  [N]
       where K_t is the specific cutting energy [N/mm2], a_p is axial depth of cut [mm], h_0 is nominal uncut chip
       thickness [mm], and tau_tooth = 60 / (N_flutes * omega_rpm) is the tooth passing period [s].
     - When phase shift between inner and outer modulated surfaces creates positive regenerative feedback, vibration
       grows exponentially, producing acoustic screaming, severe surface scallops, and cutter chipping.
     - Dual-Pronged Cyber-Physical Active Suppression:
       a) Active Inertial Mass Actuators (AIMD): Linear voice-coil / piezo proof-mass actuators mounted directly on the
          spindle ram housing inject anti-phase dynamic counter-forces:
             F_damp_x(t) = - K_v_aimd * v_struct_x(t) - K_a_aimd * a_struct_x(t)  [N]
             F_damp_y(t) = - K_v_aimd * v_struct_y(t) - K_a_aimd * a_struct_y(t)  [N]
       b) Continuous Spindle Speed Variation (SSV): Sinusoidal modulation of spindle rotational velocity:
             omega(t) = omega_0 * [1 + S_amp * sin(2 * pi * f_mod * t)]  [rpm]
          disrupts the fixed phase delay tau_tooth, tearing down the regenerative feedback resonance loop.

  4. HIGH-SPEED TOOL TIP CANTILEVER DEFLECTION OBSERVER:
     - Slender endmills subjected to high radial cutting loads experience dynamic elastic bending:
          delta_cantilever(t) = (F_radial * L_overhang^3) / (3 * E_carbide * I_tool)  [um]
          where I_tool = (pi * D_tool^4) / 64 [m4], E_carbide = 600 GPa.
     - Spindle nose structural compliance adds rotational tilt theta_nose:
          delta_total(t) = delta_cantilever(t) + theta_nose * L_overhang  [um]
     - The real-time observer reconstructs instantaneous cutting force components (F_cx, F_cy, F_cz) from high-speed
       spindle inverter torque current I_sq and triaxial nose accelerometers, injecting micro-compensations directly
       into the CNC cross-coupling trajectory setpoint buffer at 1 kHz!
*)
"""

VAR_INPUT_BLOCK = """VAR_INPUT
    (* ============================================================================================== *)
    (* MASTER CNC CONTROL ENABLES, HARDWARE INTERLOCKS & SAFETY SIGNALS                             *)
    (* ============================================================================================== *)
    bSystemEnable                       : BOOL;     (* Master CNC Gantry System Hardware Enable Permissive *)
    bMachineAutoMode                    : BOOL;     (* Automatic Cycle Execution Mode Active (G-Code Program Run) *)
    bSpindleDriveEnable                 : BOOL;     (* 100 kW Motor Spindle Power Stage Inverter Enable *)
    bActiveDampingEnable                : BOOL;     (* Active Inertial Mass Vibration Damping Actuator Enable *)
    bThermalCompEnable                  : BOOL;     (* Real-Time Thermal Expansion Compensation Offset Enable *)
    bEmergencyStopLoop                  : BOOL;     (* Hardwired SIL-3 Safety Chain (1=Healthy, 0=Emergency Trip) *)
    bAlarmAcknowledge                   : BOOL;     (* HMI Operator Alarm Acknowledgment Strobe *)
    bAlarmReset                         : BOOL;     (* HMI Operator Master Alarm Fault Reset Strobe *)
    
    (* ============================================================================================== *)
    (* CNC INTERPOLATOR COMMANDED TRAJECTORIES & TOOL DATA WITH PHYSICAL UNITS                       *)
    (* ============================================================================================== *)
    rCmdPos_X_mm                        : REAL;     (* Commanded Tool Center Point X-Axis Position [mm] *)
    rCmdPos_Y_mm                        : REAL;     (* Commanded Crossbeam Travel Y-Axis Position [mm] *)
    rCmdPos_Z_mm                        : REAL;     (* Commanded Ram Height Z-Axis Position [mm] *)
    rCmdPos_A_deg                       : REAL;     (* Commanded Trunnion Table A-Axis Tilt Angle [deg] *)
    rCmdPos_C_deg                       : REAL;     (* Commanded Rotary Table C-Axis Orientation [deg] *)
    rCmdFeedrate_mmin                   : REAL;     (* Programmed Cutting Contour Tangential Feedrate [m/min] *)
    rCmdSpindleSpeed_rpm                : REAL;     (* Programmed S-Code Spindle Rotational Speed [rpm] *)
    rCmdSpindlePower_kW                 : REAL;     (* Spindle Motor Instantaneous Electrical Power [kW] *)
    rToolLength_mm                      : REAL;     (* Tool Gage Protrusion Length from Spindle Nose Datum [mm] *)
    rToolDiameter_mm                    : REAL;     (* Active Milling Cutter Nominal Cutting Diameter [mm] *)
    nToolFluteCount                     : INT;      (* Active Cutter Flute / Insert Tooth Quantity [-] *)
    rToolOverhangRatio                  : REAL;     (* Dynamic Aspect Ratio L/D of Tool Assembly [-] *)
    rWorkpieceHardness_HB               : REAL;     (* Workpiece Raw Stock Brinell Hardness Value [HB] *)
    rAmbientTemp_degC                   : REAL;     (* Ambient Machine Enclosure Hall Air Temperature [deg C] *)
    rChillerInletTemp_degC              : REAL;     (* Spindle Closed-Loop Cooling Glycol Supply Temp [deg C] *)
    rChillerCoolantFlow_lmin            : REAL;     (* Spindle Jacket Glycol Coolant Volumetric Flow Rate [l/min] *)
    rHydraulicClampPressure_bar         : REAL;     (* HSK Hydraulic Collet Tool Gripping Line Pressure [bar] *)
    rThroughSpindleCoolant_bar          : REAL;     (* High-Pressure Through-Spindle Coolant (TSC) Pressure [bar] *)
    rChipConveyorMotorLoad_pct          : REAL;     (* Dual Swarf Extraction Screw Motor Electrical Load [%] *)
    bTouchProbeDeflected                : BOOL;     (* Renishaw 3D Workpiece Optical Touch Probe Contact Trigger *)
    bLaserToolSetterBeamBreak           : BOOL;     (* Blum Non-Contact Laser Tool Setter Optical Occlusion *)
    
    (* ============================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANT (TMR) SENSOR CHANNELS                                           *)
    (* ============================================================================================== *)
    (* Optical Linear Scales X-Axis (Gantry Dual-Drive Master X1 / Slave X2) *)
    rLinearScale_X_ChA_mm               : REAL;     (* Gantry X-Axis Optical Linear Absolute Scale Channel A [mm] *)
    rLinearScale_X_ChB_mm               : REAL;     (* Gantry X-Axis Optical Linear Absolute Scale Channel B [mm] *)
    rLinearScale_X_ChC_mm               : REAL;     (* Gantry X-Axis Optical Linear Absolute Scale Channel C [mm] *)
    
    (* Optical Linear Scales Y-Axis (Crossbeam Carriage Travel) *)
    rLinearScale_Y_ChA_mm               : REAL;     (* Crossbeam Y-Axis Optical Linear Scale Channel A [mm] *)
    rLinearScale_Y_ChB_mm               : REAL;     (* Crossbeam Y-Axis Optical Linear Scale Channel B [mm] *)
    rLinearScale_Y_ChC_mm               : REAL;     (* Crossbeam Y-Axis Optical Linear Scale Channel C [mm] *)
    
    (* Optical Linear Scales Z-Axis (Vertical Ram Quill Travel) *)
    rLinearScale_Z_ChA_mm               : REAL;     (* Ram Z-Axis Optical Linear Absolute Scale Channel A [mm] *)
    rLinearScale_Z_ChB_mm               : REAL;     (* Ram Z-Axis Optical Linear Absolute Scale Channel B [mm] *)
    rLinearScale_Z_ChC_mm               : REAL;     (* Ram Z-Axis Optical Linear Absolute Scale Channel C [mm] *)
    
    (* Spindle High-Resolution Magnetic Ring Rotary Encoders *)
    rSpindleRotSpeed_ChA_rpm            : REAL;     (* Spindle Magnetic Ring Rotary Encoder Speed Channel A [rpm] *)
    rSpindleRotSpeed_ChB_rpm            : REAL;     (* Spindle Magnetic Ring Rotary Encoder Speed Channel B [rpm] *)
    rSpindleRotSpeed_ChC_rpm            : REAL;     (* Spindle Magnetic Ring Rotary Encoder Speed Channel C [rpm] *)
    rSpindleRotAngle_ChA_deg            : REAL;     (* Spindle Rotor Electrical/Mechanical Angle Channel A [deg] *)
    rSpindleRotAngle_ChB_deg            : REAL;     (* Spindle Rotor Electrical/Mechanical Angle Channel B [deg] *)
    rSpindleRotAngle_ChC_deg            : REAL;     (* Spindle Rotor Electrical/Mechanical Angle Channel C [deg] *)
    
    (* Spindle Bearing RTD Pt100 Temperature Sensors *)
    rFrontBearingTemp_ChA_degC          : REAL;     (* Front Hybrid Ceramic Bearing Pack Outer Ring RTD A [deg C] *)
    rFrontBearingTemp_ChB_degC          : REAL;     (* Front Hybrid Ceramic Bearing Pack Outer Ring RTD B [deg C] *)
    rFrontBearingTemp_ChC_degC          : REAL;     (* Front Hybrid Ceramic Bearing Pack Outer Ring RTD C [deg C] *)
    rRearBearingTemp_ChA_degC           : REAL;     (* Rear Floating Hybrid Bearing Outer Ring RTD A [deg C] *)
    rRearBearingTemp_ChB_degC           : REAL;     (* Rear Floating Hybrid Bearing Outer Ring RTD B [deg C] *)
    rRearBearingTemp_ChC_degC           : REAL;     (* Rear Floating Hybrid Bearing Outer Ring RTD C [deg C] *)
    rSpindleStatorTemp_ChA_degC         : REAL;     (* Synchronous Motor Stator Core RTD Channel A [deg C] *)
    rSpindleStatorTemp_ChB_degC         : REAL;     (* Synchronous Motor Stator Core RTD Channel B [deg C] *)
    rSpindleStatorTemp_ChC_degC         : REAL;     (* Synchronous Motor Stator Core RTD Channel C [deg C] *)
    
    (* Spindle Nose 3-Axis Piezo Accelerometers *)
    rSpindleAccel_X_ChA_ms2             : REAL;     (* Spindle Nose Triaxial Piezo Accelerometer X Channel A [m/s2] *)
    rSpindleAccel_X_ChB_ms2             : REAL;     (* Spindle Nose Triaxial Piezo Accelerometer X Channel B [m/s2] *)
    rSpindleAccel_X_ChC_ms2             : REAL;     (* Spindle Nose Triaxial Piezo Accelerometer X Channel C [m/s2] *)
    rSpindleAccel_Y_ChA_ms2             : REAL;     (* Spindle Nose Triaxial Piezo Accelerometer Y Channel A [m/s2] *)
    rSpindleAccel_Y_ChB_ms2             : REAL;     (* Spindle Nose Triaxial Piezo Accelerometer Y Channel B [m/s2] *)
    rSpindleAccel_Y_ChC_ms2             : REAL;     (* Spindle Nose Triaxial Piezo Accelerometer Y Channel C [m/s2] *)
    rSpindleAccel_Z_ChA_ms2             : REAL;     (* Spindle Nose Triaxial Piezo Accelerometer Z Channel A [m/s2] *)
    rSpindleAccel_Z_ChB_ms2             : REAL;     (* Spindle Nose Triaxial Piezo Accelerometer Z Channel B [m/s2] *)
    rSpindleAccel_Z_ChC_ms2             : REAL;     (* Spindle Nose Triaxial Piezo Accelerometer Z Channel C [m/s2] *)
    
    (* Spindle Motor Electrical Inverter Sensing *)
    rSpindleCurrent_Iu_A                : REAL;     (* Spindle Inverter Phase U Stator Current Feedback [A] *)
    rSpindleCurrent_Iv_A                : REAL;     (* Spindle Inverter Phase V Stator Current Feedback [A] *)
    rSpindleCurrent_Iw_A                : REAL;     (* Spindle Inverter Phase W Stator Current Feedback [A] *)
    rSpindleDCLinkVoltage_V             : REAL;     (* Spindle Inverter DC Bus Intermediate Voltage [V] *)
END_VAR
"""

VAR_OUTPUT_BLOCK = """VAR_OUTPUT
    (* ============================================================================================== *)
    (* MASTER MACHINE STATUS, FSM PHASES & SAFETY TRIPS                                              *)
    (* ============================================================================================== *)
    bMachiningCenterReady               : BOOL;     (* 5-Axis Gantry Milling Center Master Permissive Ready *)
    bCollisionStopActive                : BOOL;     (* SIL-3 Collision Impact Rapid Brake Stop Latched *)
    nActiveFSMStage                     : INT;      (* Current 14-Stage Master FSM Operational Stage (0 to 13) *)
    sActiveFSMStageName                 : STRING(64); (* Descriptive String of Active FSM Operational State *)
    
    (* ============================================================================================== *)
    (* 2oo3 TMR VOTED SENSOR SIGNALS & FILTERED VALUES                                               *)
    (* ============================================================================================== *)
    rVotedPos_X_mm                      : REAL;     (* 2oo3 TMR Voted True Gantry Position X [mm] *)
    rVotedPos_Y_mm                      : REAL;     (* 2oo3 TMR Voted True Crossbeam Position Y [mm] *)
    rVotedPos_Z_mm                      : REAL;     (* 2oo3 TMR Voted True Ram Height Position Z [mm] *)
    rVotedSpindleSpeed_rpm              : REAL;     (* 2oo3 TMR Voted Spindle Rotational Speed [rpm] *)
    rVotedSpindleAngle_deg              : REAL;     (* 2oo3 TMR Voted Spindle Rotor Angular Orientation [deg] *)
    rVotedFrontBearingTemp_degC         : REAL;     (* 2oo3 TMR Voted Front Hybrid Ceramic Bearing Temp [deg C] *)
    rVotedRearBearingTemp_degC          : REAL;     (* 2oo3 TMR Voted Rear Hybrid Bearing Temp [deg C] *)
    rVotedStatorTemp_degC               : REAL;     (* 2oo3 TMR Voted Synchronous Motor Stator Core Temp [deg C] *)
    rVotedSpindleAccel_X_ms2            : REAL;     (* 2oo3 TMR Voted Spindle Nose Acceleration X-Axis [m/s2] *)
    rVotedSpindleAccel_Y_ms2            : REAL;     (* 2oo3 TMR Voted Spindle Nose Acceleration Y-Axis [m/s2] *)
    rVotedSpindleAccel_Z_ms2            : REAL;     (* 2oo3 TMR Voted Spindle Nose Acceleration Z-Axis [m/s2] *)
    
    (* ============================================================================================== *)
    (* CYBER-PHYSICAL OBSERVERS, DEFLECTIONS & THERMAL GROWTH                                         *)
    (* ============================================================================================== *)
    rThermalGrowth_Z_um                 : REAL;     (* Multi-Node Observer Spindle Shaft Elongation Delta Lz [um] *)
    rThermalTilt_A_urad                 : REAL;     (* Spindle Nose Thermal Angular Pitch Tilt around A-Axis [urad] *)
    rThermalTilt_C_urad                 : REAL;     (* Spindle Nose Thermal Angular Yaw Tilt around C-Axis [urad] *)
    rBearingPreloadDelta_N              : REAL;     (* Thermally Induced Bearing Preload Force Dynamic Variation [N] *)
    rCuttingForce_Magnitude_N           : REAL;     (* Reconstructed Total Cutting Force Vector Magnitude [N] *)
    rCuttingForce_Fx_N                  : REAL;     (* Resolved Dynamic Cutting Force Component X-Axis [N] *)
    rCuttingForce_Fy_N                  : REAL;     (* Resolved Dynamic Cutting Force Component Y-Axis [N] *)
    rCuttingForce_Fz_N                  : REAL;     (* Resolved Dynamic Cutting Force Component Z-Axis [N] *)
    rToolTipDeflection_um               : REAL;     (* Real-Time Cantilever Dynamic Tool Tip Deflection [um] *)
    rGantryCrossCouplingYaw_um          : REAL;     (* Gantry Dual-Drive Linear Scale Skew Yaw Differential [um] *)
    rPeakChatterAmplitude_ms2           : REAL;     (* Real-Time Peak Chatter Vibration Acceleration Amplitude [m/s2] *)
    rDominantChatterFreq_Hz             : REAL;     (* Identified Dominant Chatter Modal Resonant Frequency [Hz] *)
    
    (* ============================================================================================== *)
    (* ACTUATOR COMMANDS & DYNAMIC REAL-TIME OFFSETS                                                  *)
    (* ============================================================================================== *)
    rActiveDampForceCmd_X_N             : REAL;     (* AIMD Linear Voice-Coil Actuator Force Command X [N] *)
    rActiveDampForceCmd_Y_N             : REAL;     (* AIMD Linear Voice-Coil Actuator Force Command Y [N] *)
    rActiveDampForceCmd_Z_N             : REAL;     (* AIMD High-Force Piezo Stack Dynamic Force Command Z [N] *)
    rThermalCompOffset_Z_um             : REAL;     (* Real-Time Additive Z-Axis Interpolator Position Offset [um] *)
    rDeflectionCompOffset_X_um          : REAL;     (* Real-Time Tool Deflection Additive Offset X-Axis [um] *)
    rDeflectionCompOffset_Y_um          : REAL;     (* Real-Time Tool Deflection Additive Offset Y-Axis [um] *)
    rAdaptiveFeedOverride_pct           : REAL;     (* Dynamic Chatter-Suppressed Feedrate Override Multiplier [%] *)
    rModulatedSpindleSpeed_rpm          : REAL;     (* SSV Continuous Sinusoidally Modulated Spindle Speed [rpm] *)
    rChillerValveDemand_pct             : REAL;     (* Spindle Jacket Cooling Chiller Proportional Flow Demand [%] *)
    bToolClampSolenoidCmd               : BOOL;     (* HSK Collet Hydraulic Clamping (1=Clamped, 0=Unclamped) *)
    bThroughSpindleCoolantCmd           : BOOL;     (* High-Pressure TSC Boost Pump Contactor Enable Command *)
    bChipConveyorRunCmd                 : BOOL;     (* Swarf Chip Conveyor Forward Motor Run Command *)
    bSpindlePurgeAirCmd                 : BOOL;     (* Spindle Labyrinth Positive Air Barrier Purge Solenoid *)
    
    (* ============================================================================================== *)
    (* BIT-PACKED STATUS WORDS & ISA-18.2 ALARM GROUPS                                               *)
    (* ============================================================================================== *)
    dwMotionStatusWord                  : DWORD;    (* 32-Bit Gantry Axis & Decoupling Controller Status Bitmask *)
    dwSpindleStatusWord                 : DWORD;    (* 32-Bit 100 kW Motor Spindle & Thermal Observer Status *)
    dwDampingStatusWord                 : DWORD;    (* 32-Bit Active Damping & MPC Chatter Controller Status *)
    dwAlarmStatus_P1_Critical           : DWORD;    (* 32-Bit ISA-18.2 Priority 1 Failsafe / Crash Alarm Bitmask *)
    dwAlarmStatus_P2_High               : DWORD;    (* 32-Bit ISA-18.2 Priority 2 Heavy Thermal & Process Trip Bitmask *)
    dwAlarmStatus_P3_Medium             : DWORD;    (* 32-Bit ISA-18.2 Priority 3 Warning & Discrepancy Bitmask *)
    dwAlarmStatus_P4_Advisory           : DWORD;    (* 32-Bit ISA-18.2 Priority 4 Wear & Maintenance Advisory Bitmask *)
    bAlarm_SpindleBearingOverheat       : BOOL;     (* High-High Spindle Ceramic Bearing Thermal Protection Trip *)
    bAlarm_ExcessiveChatterVibration    : BOOL;     (* High-High Regenerative Chatter Instability Trip *)
    bAlarm_CollisionImpactTripped       : BOOL;     (* Extreme Deceleration Crash Impact Failsafe Trip *)
    bAlarm_ToolClampingDefect           : BOOL;     (* HSK Collet Grip Force Transducer Failure Trip *)
    bAlarm_ChillerCoolingLoss           : BOOL;     (* Spindle Cooling Jacket Flow Failure / Over-Temperature *)
END_VAR
"""

VAR_BLOCK = """VAR
    (* ============================================================================================== *)
    (* TIME CYCLES & DISCRETE CONTROLLER SAMPLING TIME                                               *)
    (* ============================================================================================== *)
    T_CYCLE_SEC                         : REAL := 0.001;    (* Fast High-Speed CNC Scan Interval Ts = 1 ms [s] *)
    bInitDone                           : BOOL := FALSE;    (* First-Scan State-Space Matrix Initialization *)
    
    (* ============================================================================================== *)
    (* PHYSICAL MACHINE TOOL MECHANICAL & THERMAL SPECIFICATIONS                                     *)
    (* ============================================================================================== *)
    GANTRY_SPAN_WIDTH_M                 : REAL := 3.200;    (* Gantry Bridge Twin Rail Spacing W_gantry [m] *)
    GANTRY_BRIDGE_MASS_KG               : REAL := 18500.0;  (* Total Moving Gantry Cast Iron Structure Mass [kg] *)
    RAM_QUILL_MASS_KG                   : REAL := 2400.0;   (* Vertical Z-Axis Ram Structural Mass [kg] *)
    SPINDLE_ROTOR_MASS_KG               : REAL := 68.5;     (* High-Speed Synchronous Motor Rotor Mass [kg] *)
    SPINDLE_NOM_POWER_KW                : REAL := 100.0;    (* Continuous S1 Spindle Drive Rating [kW] *)
    SPINDLE_MAX_SPEED_RPM               : REAL := 24000.0;  (* Maximum Permissible Spindle Angular Speed [rpm] *)
    SPINDLE_POLE_PAIRS                  : INT := 2;         (* 4-Pole Synchronous Motor Configuration *)
    SPINDLE_PM_FLUX_WB                  : REAL := 0.185;    (* Rotor Permanent Magnet Flux Linkage psi_f [Wb] *)
    SPINDLE_STATOR_RES_OHM              : REAL := 0.038;    (* Stator Phase Winding Resistance at 20 deg C [Ohm] *)
    BEARING_PITCH_DIAMETER_M            : REAL := 0.110;    (* Hybrid Ceramic Bearing Mean Diameter d_m [m] *)
    BEARING_CONTACT_ANGLE_RAD           : REAL := 0.2618;   (* Angular Contact Angle alpha_0 = 15 deg [rad] *)
    BEARING_NOM_PRELOAD_N               : REAL := 2200.0;   (* Calibrated Assembly Axial Preload Force [N] *)
    
    (* Thermal Expansion Coefficients & Nodal Network Properties *)
    ALPHA_STEEL_SHAFT_PER_K             : REAL := 1.15E-5;  (* High-Alloy Spindle Steel Exp Coeff [1/K] *)
    ALPHA_CERAMIC_BRG_PER_K             : REAL := 3.20E-6;  (* Silicon Nitride Si3N4 Ball Exp Coeff [1/K] *)
    ALPHA_CAST_IRON_PER_K               : REAL := 1.05E-5;  (* Meehanite Cast Iron Housing Exp Coeff [1/K] *)
    ALPHA_ALU_TOOL_PER_K                : REAL := 2.30E-5;  (* Tool Extension Structural Sleeve Exp Coeff [1/K] *)
    ROTOR_ACTIVE_LENGTH_M               : REAL := 0.650;    (* Spindle Rotor Thermal Effective Length [m] *)
    RAM_EFFECTIVE_LENGTH_M              : REAL := 1.200;    (* Z-Axis Ram Thermal Reference Length [m] *)
    TOOL_CARBIDE_YOUNGS_MOD_PA          : REAL := 6.0E11;   (* Solid Tungsten Carbide Elastic Modulus [Pa] *)
    
    (* Multi-Node Thermal Heat Capacity & Thermal Conductance Matrices *)
    C_TH_ROTOR_J_K                      : REAL := 32000.0;  (* Thermal Capacity Rotor Assembly [J/K] *)
    C_TH_STATOR_J_K                     : REAL := 48000.0;  (* Thermal Capacity Stator Core & Copper [J/K] *)
    C_TH_FRONT_BRG_J_K                  : REAL := 8500.0;   (* Thermal Capacity Front Bearing Pack [J/K] *)
    C_TH_REAR_BRG_J_K                   : REAL := 6200.0;   (* Thermal Capacity Rear Floating Bearing [J/K] *)
    C_TH_HOUSING_J_K                    : REAL := 125000.0; (* Thermal Capacity Spindle Ram Housing [J/K] *)
    G_TH_ROTOR_TO_FRONT_W_K             : REAL := 42.0;     (* Thermal Conductance Rotor to Front Bearings [W/K] *)
    G_TH_ROTOR_TO_REAR_W_K              : REAL := 28.0;     (* Thermal Conductance Rotor to Rear Bearings [W/K] *)
    G_TH_STATOR_TO_CHILLER_W_K          : REAL := 380.0;    (* Thermal Conductance Stator to Chiller Jacket [W/K] *)
    G_TH_FRONT_TO_HOUSING_W_K           : REAL := 85.0;     (* Thermal Conductance Front Bearing to Housing [W/K] *)
    G_TH_REAR_TO_HOUSING_W_K            : REAL := 65.0;     (* Thermal Conductance Rear Bearing to Housing [W/K] *)
    G_TH_HOUSING_TO_AIR_W_K             : REAL := 45.0;     (* Thermal Conductance Housing to Ambient Air [W/K] *)
    K_CENTRIFUGAL_CONTRACTION_UM        : REAL := 2.5E-9;   (* Rotor Centrifugal Shrinkage Coeff [um/(rpm^2)] *)
    K_BEARING_PRELOAD_TEMP_N_K          : REAL := 48.5;     (* Differential Temp Preload Gradient [N/K] *)
    K_BEARING_PRELOAD_SPEED_N_RPM       : REAL := 0.042;    (* Centrifugal Dilation Preload Gradient [N/rpm] *)
    
    (* ============================================================================================== *)
    (* DISCRETE STATE-SPACE MODEL MATRICES & VECTORS (10 STATES, 6 CONTROLS)                          *)
    (* x[k+1] = A * x[k] + B * u[k]                                                                   *)
    (* y[k]   = C * x[k] + D * u[k]                                                                   *)
    (* State Vector x:                                                                                *)
    (*  x[1]: Gantry X-Axis TCP Position Error                  [um]                                  *)
    (*  x[2]: Crossbeam Y-Axis TCP Position Error              [um]                                  *)
    (*  x[3]: Ram Z-Axis TCP Position Error                    [um]                                  *)
    (*  x[4]: Structural Modal Vibration Velocity X-Axis        [mm/s]                                *)
    (*  x[5]: Structural Modal Vibration Velocity Y-Axis        [mm/s]                                *)
    (*  x[6]: Structural Modal Vibration Velocity Z-Axis        [mm/s]                                *)
    (*  x[7]: Spindle Rotor Axial Thermal Expansion Delta Lz    [um]                                  *)
    (*  x[8]: Front Bearing Dynamic Preload Variation           [N]                                   *)
    (*  x[9]: Reconstructed Dynamic Cutting Force Vector        [N]                                   *)
    (*  x[10]: Active Inertial Damper Proof-Mass Position       [mm]                                  *)
    (* Control Vector u:                                                                              *)
    (*  u[1]: Active Damper Force Demand X-Axis                 [N]                                   *)
    (*  u[2]: Active Damper Force Demand Y-Axis                 [N]                                   *)
    (*  u[3]: Active Piezo Force Demand Z-Axis                  [N]                                   *)
    (*  u[4]: Dynamic Thermal Offset Compensation Delta Z       [um]                                  *)
    (*  u[5]: Dynamic Feedrate Override Attenuation Factor      [%]                                   *)
    (*  u[6]: Spindle Chiller Proportional Valve Flow Demand    [%]                                   *)
    (* ============================================================================================== *)
    a_mat                               : ARRAY[1..10, 1..10] OF REAL;  (* State Transition Matrix A (10x10) *)
    b_mat                               : ARRAY[1..10, 1..6] OF REAL;   (* Input Coupling Matrix B (10x6) *)
    c_mat                               : ARRAY[1..10, 1..10] OF REAL;  (* State Measurement Matrix C (10x10) *)
    d_mat                               : ARRAY[1..10, 1..6] OF REAL;   (* Feedthrough Matrix D (10x6) *)
    k_obs                               : ARRAY[1..10] OF REAL;         (* Luenberger Observer Correction Gains *)
    
    x_state                             : ARRAY[1..10] OF REAL;         (* Estimated System State Vector x[k] *)
    x_next                              : ARRAY[1..10] OF REAL;         (* Propagated State Vector x[k+1] *)
    y_meas                              : ARRAY[1..10] OF REAL;         (* Measured / Filtered Observation Vector *)
    y_pred                              : ARRAY[1..10] OF REAL;         (* Model Predicted Output Vector *)
    u_ctrl                              : ARRAY[1..6] OF REAL;          (* Computed Actuator Control Vector u[k] *)
    x_ref                               : ARRAY[1..10] OF REAL;         (* Desired Target State Trajectory *)
    u_ref                               : ARRAY[1..6] OF REAL;          (* Nominal Equilibrium Actuator Command *)
    u_prev                              : ARRAY[1..6] OF REAL;          (* Previous Step Actuator Command u[k-1] *)
    
    (* ============================================================================================== *)
    (* MODEL PREDICTIVE CONTROL (MPC) COST MATRICES & PROJECTION BOUNDS                               *)
    (* ============================================================================================== *)
    q_diag                              : ARRAY[1..10] OF REAL;         (* State Error Quadratic Penalty Diagonal Q *)
    r_diag                              : ARRAY[1..6] OF REAL;          (* Control Effort Quadratic Penalty Diagonal R *)
    s_diag                              : ARRAY[1..6] OF REAL;          (* Actuator Slew Rate Penalty Diagonal S *)
    p_diag                              : ARRAY[1..10] OF REAL;         (* Terminal State Error Quadratic Penalty P *)
    u_box_min                           : ARRAY[1..6] OF REAL;          (* Actuator Physical Lower Bound Box Saturation *)
    u_box_max                           : ARRAY[1..6] OF REAL;          (* Actuator Physical Upper Bound Box Saturation *)
    du_slew_max                         : ARRAY[1..6] OF REAL;          (* Max Allowable Actuator Slew [units/scan] *)
    
    u_mpc_traj                          : ARRAY[1..5, 1..6] OF REAL;    (* Receding Prediction Horizon Actuator Matrix *)
    grad_u                              : ARRAY[1..6] OF REAL;          (* Projected Gradient Vector *)
    u_tentative                         : ARRAY[1..6] OF REAL;          (* Intermediate PGD Optimization Candidate *)
    rMpcStepSize                        : REAL := 0.035;                (* PGD Optimization Gradient Descent Step *)
    rPredictedCost                      : REAL;                         (* Cumulative Quadratic MPC Cost Value *)
    
    (* ============================================================================================== *)
    (* 2oo3 TMR VOTING VARIABLES ACROSS 11 SENSOR CHANNELS                                           *)
    (* ============================================================================================== *)
    (* Triplet 1: Linear Scale X *)
    rX_Delta_AB : REAL; rX_Delta_BC : REAL; rX_Delta_CA : REAL;
    rX_DiscLimit_mm : REAL := 0.025; rX_DiscTimer_s : REAL := 0.0;
    bX_ChA_Valid : BOOL := TRUE; bX_ChB_Valid : BOOL := TRUE; bX_ChC_Valid : BOOL := TRUE;
    nX_VotingMode : INT := 3; rX_Filt_mm : REAL := 0.0;
    
    (* Triplet 2: Linear Scale Y *)
    rY_Delta_AB : REAL; rY_Delta_BC : REAL; rY_Delta_CA : REAL;
    rY_DiscLimit_mm : REAL := 0.025; rY_DiscTimer_s : REAL := 0.0;
    bY_ChA_Valid : BOOL := TRUE; bY_ChB_Valid : BOOL := TRUE; bY_ChC_Valid : BOOL := TRUE;
    nY_VotingMode : INT := 3; rY_Filt_mm : REAL := 0.0;
    
    (* Triplet 3: Linear Scale Z *)
    rZ_Delta_AB : REAL; rZ_Delta_BC : REAL; rZ_Delta_CA : REAL;
    rZ_DiscLimit_mm : REAL := 0.020; rZ_DiscTimer_s : REAL := 0.0;
    bZ_ChA_Valid : BOOL := TRUE; bZ_ChB_Valid : BOOL := TRUE; bZ_ChC_Valid : BOOL := TRUE;
    nZ_VotingMode : INT := 3; rZ_Filt_mm : REAL := 0.0;
    
    (* Triplet 4: Spindle Rotary Speed *)
    rSpd_Delta_AB : REAL; rSpd_Delta_BC : REAL; rSpd_Delta_CA : REAL;
    rSpd_DiscLimit_rpm : REAL := 45.0; rSpd_DiscTimer_s : REAL := 0.0;
    bSpd_ChA_Valid : BOOL := TRUE; bSpd_ChB_Valid : BOOL := TRUE; bSpd_ChC_Valid : BOOL := TRUE;
    nSpd_VotingMode : INT := 3; rSpd_Filt_rpm : REAL := 0.0;
    
    (* Triplet 5: Spindle Rotary Angle *)
    rAng_Delta_AB : REAL; rAng_Delta_BC : REAL; rAng_Delta_CA : REAL;
    rAng_DiscLimit_deg : REAL := 0.50; rAng_DiscTimer_s : REAL := 0.0;
    bAng_ChA_Valid : BOOL := TRUE; bAng_ChB_Valid : BOOL := TRUE; bAng_ChC_Valid : BOOL := TRUE;
    nAng_VotingMode : INT := 3; rAng_Filt_deg : REAL := 0.0;
    
    (* Triplet 6: Front Bearing Temperature *)
    rTF_Delta_AB : REAL; rTF_Delta_BC : REAL; rTF_Delta_CA : REAL;
    rTF_DiscLimit_degC : REAL := 4.0; rTF_DiscTimer_s : REAL := 0.0;
    bTF_ChA_Valid : BOOL := TRUE; bTF_ChB_Valid : BOOL := TRUE; bTF_ChC_Valid : BOOL := TRUE;
    nTF_VotingMode : INT := 3; rTF_Filt_degC : REAL := 22.0;
    
    (* Triplet 7: Rear Bearing Temperature *)
    rTR_Delta_AB : REAL; rTR_Delta_BC : REAL; rTR_Delta_CA : REAL;
    rTR_DiscLimit_degC : REAL := 4.0; rTR_DiscTimer_s : REAL := 0.0;
    bTR_ChA_Valid : BOOL := TRUE; bTR_ChB_Valid : BOOL := TRUE; bTR_ChC_Valid : BOOL := TRUE;
    nTR_VotingMode : INT := 3; rTR_Filt_degC : REAL := 22.0;
    
    (* Triplet 8: Stator Winding Temperature *)
    rTS_Delta_AB : REAL; rTS_Delta_BC : REAL; rTS_Delta_CA : REAL;
    rTS_DiscLimit_degC : REAL := 6.0; rTS_DiscTimer_s : REAL := 0.0;
    bTS_ChA_Valid : BOOL := TRUE; bTS_ChB_Valid : BOOL := TRUE; bTS_ChC_Valid : BOOL := TRUE;
    nTS_VotingMode : INT := 3; rTS_Filt_degC : REAL := 22.0;
    
    (* Triplet 9: Spindle Nose Accel X *)
    rAX_Delta_AB : REAL; rAX_Delta_BC : REAL; rAX_Delta_CA : REAL;
    rAX_DiscLimit_ms2 : REAL := 2.5; rAX_DiscTimer_s : REAL := 0.0;
    bAX_ChA_Valid : BOOL := TRUE; bAX_ChB_Valid : BOOL := TRUE; bAX_ChC_Valid : BOOL := TRUE;
    nAX_VotingMode : INT := 3; rAX_Filt_ms2 : REAL := 0.0;
    
    (* Triplet 10: Spindle Nose Accel Y *)
    rAY_Delta_AB : REAL; rAY_Delta_BC : REAL; rAY_Delta_CA : REAL;
    rAY_DiscLimit_ms2 : REAL := 2.5; rAY_DiscTimer_s : REAL := 0.0;
    bAY_ChA_Valid : BOOL := TRUE; bAY_ChB_Valid : BOOL := TRUE; bAY_ChC_Valid : BOOL := TRUE;
    nAY_VotingMode : INT := 3; rAY_Filt_ms2 : REAL := 0.0;
    
    (* Triplet 11: Spindle Nose Accel Z *)
    rAZ_Delta_AB : REAL; rAZ_Delta_BC : REAL; rAZ_Delta_CA : REAL;
    rAZ_DiscLimit_ms2 : REAL := 2.5; rAZ_DiscTimer_s : REAL := 0.0;
    bAZ_ChA_Valid : BOOL := TRUE; bAZ_ChB_Valid : BOOL := TRUE; bAZ_ChC_Valid : BOOL := TRUE;
    nAZ_VotingMode : INT := 3; rAZ_Filt_ms2 : REAL := 0.0;
    
    (* TMR Discrepancy Fault Integration Constants *)
    T_DISCREPANCY_FAULT_SEC             : REAL := 0.080;   (* 80 ms Continuous Mismatch Triggers Isolation [s] *)
    TMR_FILTER_ALPHA                    : REAL := 0.150;   (* First-Order Low-Pass Filter Smoothing Weight *)
    
    (* ============================================================================================== *)
    (* CYBER-PHYSICAL INTERNAL STATE VARIABLES & OBSERVER RECONSTRUCTION                             *)
    (* ============================================================================================== *)
    (* Multi-Node Thermal Network States *)
    rNodeTemp_Rotor_degC                : REAL := 22.0;    (* Thermal State Node 1: Rotor Shaft Core [deg C] *)
    rNodeTemp_Stator_degC               : REAL := 22.0;    (* Thermal State Node 2: Stator Winding [deg C] *)
    rNodeTemp_FrontBrg_degC             : REAL := 22.0;    (* Thermal State Node 3: Front Bearing Pack [deg C] *)
    rNodeTemp_RearBrg_degC              : REAL := 22.0;    (* Thermal State Node 4: Rear Bearing Pack [deg C] *)
    rNodeTemp_Housing_degC              : REAL := 22.0;    (* Thermal State Node 5: Ram Housing Structure [deg C] *)
    rRefDatumTemp_degC                  : REAL := 20.0;    (* Standard Calibration Reference Temperature [deg C] *)
    
    (* Heat Loss Powers *)
    rHeatLoss_StatorJoule_W             : REAL := 0.0;     (* Stator Copper I^2*R Dissipation [W] *)
    rHeatLoss_StatorIron_W              : REAL := 0.0;     (* Stator Core Magnetic Hysteresis / Eddy Loss [W] *)
    rHeatLoss_BearingFront_W            : REAL := 0.0;     (* Front Bearing Viscous Friction Loss [W] *)
    rHeatLoss_BearingRear_W             : REAL := 0.0;     (* Rear Bearing Viscous Friction Loss [W] *)
    rHeatRemoval_Chiller_W              : REAL := 0.0;     (* Glycol Jacket Extracted Heat Energy [W] *)
    
    (* Cutting Force & Tool Tip Deflection *)
    rMotorTorque_EM_Nm                  : REAL := 0.0;     (* Spindle Motor Electromagnetic Torque [Nm] *)
    rMotorTorque_Loss_Nm                : REAL := 0.0;     (* Bearing Windage & Seal Friction Torque [Nm] *)
    rTangentialCutForce_N               : REAL := 0.0;     (* Tangential Cutting Force Component [N] *)
    rRadialCutForce_N                   : REAL := 0.0;     (* Radial Cutting Force Component [N] *)
    rAxialCutForce_N                    : REAL := 0.0;     (* Axial Cutting Force Component [N] *)
    rToolCantileverInertia_m4           : REAL := 1.0E-10; (* Area Moment of Inertia of Cylindrical Tool [m4] *)
    rToolOverhang_m                     : REAL := 0.120;   (* Tool Flute Effective Cantilever Overhang [m] *)
    rSpindleNoseTiltAngle_X_rad         : REAL := 0.0;     (* Nose Structural Bending Rotation around X [rad] *)
    rSpindleNoseTiltAngle_Y_rad         : REAL := 0.0;     (* Nose Structural Bending Rotation around Y [rad] *)
    
    (* Dual-Drive Gantry Yaw Decoupling *)
    rGantryYaw_SkewError_mm             : REAL := 0.0;     (* Raw Differential Distance X1 - X2 [mm] *)
    rGantryYaw_SkewVel_mms              : REAL := 0.0;     (* Derivative of Skew Difference [mm/s] *)
    rGantryYaw_SkewIntegral_mms         : REAL := 0.0;     (* Integrated Skew Error [mm*s] *)
    rGantryYaw_PrevSkew_mm              : REAL := 0.0;     (* Previous Step Skew Error [mm] *)
    rKp_Yaw                             : REAL := 45000.0; (* Proportional Yaw Correction Gain [N/mm] *)
    rKd_Yaw                             : REAL := 850.0;   (* Derivative Yaw Dampening Gain [N/(mm/s)] *)
    rKi_Yaw                             : REAL := 2200.0;  (* Integral Yaw Restoring Gain [N/(mm*s)] *)
    rGantryYawRestoringForce_N          : REAL := 0.0;     (* Differential Cross-Coupling Restoring Force [N] *)
    
    (* 5-Axis Forward Kinematics Jacobian *)
    rAngle_A_rad                        : REAL := 0.0;     (* Trunnion Table A-Axis Angle in Radians [rad] *)
    rAngle_C_rad                        : REAL := 0.0;     (* Rotary Table C-Axis Angle in Radians [rad] *)
    rRotMat_A11 : REAL; rRotMat_A12 : REAL; rRotMat_A13 : REAL;
    rRotMat_A21 : REAL; rRotMat_A22 : REAL; rRotMat_A23 : REAL;
    rRotMat_A31 : REAL; rRotMat_A32 : REAL; rRotMat_A33 : REAL;
    rRotMat_C11 : REAL; rRotMat_C12 : REAL; rRotMat_C13 : REAL;
    rRotMat_C21 : REAL; rRotMat_C22 : REAL; rRotMat_C23 : REAL;
    rRotMat_C31 : REAL; rRotMat_C32 : REAL; rRotMat_C33 : REAL;
    rToolVector_X_mm                    : REAL := 0.0;     (* Dynamic Tool Tip Orientation Vector X [mm] *)
    rToolVector_Y_mm                    : REAL := 0.0;     (* Dynamic Tool Tip Orientation Vector Y [mm] *)
    rToolVector_Z_mm                    : REAL := 0.0;     (* Dynamic Tool Tip Orientation Vector Z [mm] *)
    
    (* Spindle Speed Variation (SSV) & Chatter Suppression *)
    rSSV_ModulationPhase_rad            : REAL := 0.0;     (* Sinusoidal Modulation Phase Integrator [rad] *)
    rSSV_AmplitudeFactor                : REAL := 0.085;   (* Speed Modulation Depth Ratio (+/- 8.5%) *)
    rSSV_ModulationFreq_Hz              : REAL := 2.50;    (* Modulation Oscillation Frequency [Hz] *)
    rChatterPeakSpectrum_ms2            : REAL := 0.0;     (* Filtered Spectral Acceleration Peak [m/s2] *)
    bChatterActiveCondition             : BOOL := FALSE;   (* Regenerative Chatter Threshold Exceeded Flag *)
    
    (* ============================================================================================== *)
    (* DETERMINISTIC 14-STAGE FINITE STATE MACHINE (FSM) TIMERS & REGISTERS                           *)
    (* ============================================================================================== *)
    nPrevFSMStage                       : INT := -1;       (* Previous Cycle FSM State Code *)
    rStageDwellTimer_s                  : REAL := 0.0;     (* Active State Elapsed Dwell Timer [s] *)
    rStageTargetDwell_s                 : REAL := 0.0;     (* Active State Required Dwell Timeout [s] *)
    bStateInitStrobe                    : BOOL := TRUE;    (* One-Shot Pulse on State Entry *)
    nWarmupSubStep                      : INT := 0;        (* Thermal Preheating Ramp Index (0 to 4) *)
    rWarmupRampSpeed_rpm                : REAL := 0.0;     (* Preheating Target Speed Command [rpm] *)
    rLaserCalRefZ_mm                    : REAL := 0.0;     (* Laser Baseline Reference Tool Position Z [mm] *)
    rMeasuredRunout_um                  : REAL := 0.0;     (* Measured Tool Assembly Radial Runout [um] *)
    rTouchProbeRecorded_X_mm            : REAL := 0.0;     (* Touch Probe Latched Workpiece Datum X [mm] *)
    rTouchProbeRecorded_Y_mm            : REAL := 0.0;     (* Touch Probe Latched Workpiece Datum Y [mm] *)
    rTouchProbeRecorded_Z_mm            : REAL := 0.0;     (* Touch Probe Latched Workpiece Datum Z [mm] *)
    nATC_SubStep                        : INT := 0;        (* Automatic Tool Changer Sequencer Step *)
    
    (* ============================================================================================== *)
    (* ISA-18.2 ALARM PARAMETERS, HYSTERESIS DEADBANDS & TRIP REGISTERS                              *)
    (* ============================================================================================== *)
    (* Bearing Temperature Limits *)
    TEMP_BRG_HH_TRIP_DEGC               : REAL := 75.0;    (* Priority 2 Front Bearing High-High Trip [deg C] *)
    TEMP_BRG_H_WARN_DEGC                : REAL := 62.0;    (* Priority 3 Front Bearing High Warning [deg C] *)
    TEMP_STATOR_HH_TRIP_DEGC            : REAL := 110.0;   (* Priority 2 Stator Winding High-High Trip [deg C] *)
    TEMP_STATOR_H_WARN_DEGC             : REAL := 95.0;    (* Priority 3 Stator Winding High Warning [deg C] *)
    TEMP_HYSTERESIS_DEGC                : REAL := 3.0;     (* Temperature Alarm Reset Clearance Band [deg C] *)
    
    (* Dynamic Vibration & Chatter Limits *)
    VIB_COLLISION_CRASH_MS2             : REAL := 120.0;   (* Priority 1 Spindle Collision Impact Trip [m/s2] *)
    VIB_CHATTER_HH_TRIP_MS2             : REAL := 15.0;    (* Priority 2 Excessive Chatter Vibration Trip [m/s2] *)
    VIB_CHATTER_H_WARN_MS2              : REAL := 4.5;     (* Priority 3 Chatter Onset Detection Warning [m/s2] *)
    VIB_HYSTERESIS_MS2                  : REAL := 1.0;     (* Vibration Alarm Reset Clearance Band [m/s2] *)
    
    (* Tool Clamping & Process Pressures *)
    PRESSURE_CLAMP_MIN_BAR              : REAL := 45.0;    (* Priority 1 Minimum Safe Collet Grip Pressure [bar] *)
    PRESSURE_TSC_MIN_BAR                : REAL := 20.0;    (* Priority 3 Minimum Through-Coolant Pressure [bar] *)
    CHILLER_FLOW_MIN_LMIN               : REAL := 4.5;     (* Priority 2 Minimum Coolant Chiller Flow [l/min] *)
    
    (* Inverter Electrical Thresholds *)
    SPINDLE_CURRENT_MAX_A               : REAL := 220.0;   (* Priority 1 Instantaneous Stator Over-Current [A] *)
    DCLINK_VOLTAGE_MAX_V                : REAL := 780.0;   (* Priority 1 DC Bus Over-Voltage Limit [V] *)
    DCLINK_VOLTAGE_MIN_V                : REAL := 480.0;   (* Priority 1 DC Bus Under-Voltage Limit [V] *)
    
    (* Alarm Delay Integrators *)
    rAlarmTimer_BrgOverheat_s           : REAL := 0.0;
    rAlarmTimer_Chatter_s               : REAL := 0.0;
    rAlarmTimer_ChillerLoss_s           : REAL := 0.0;
    rAlarmTimer_ClampLoss_s             : REAL := 0.0;
    
    (* Loop Iterators *)
    idx_i                               : INT := 1;
    idx_j                               : INT := 1;
    idx_k                               : INT := 1;
    idx_m                               : INT := 1;
    rTempSum                            : REAL := 0.0;
END_VAR
"""
