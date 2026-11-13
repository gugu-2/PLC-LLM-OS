# cmp_polisher_builder/part1_decl.py

def get_part1():
    return """FUNCTION_BLOCK FB_Semiconductor_CMP_300mm_WaferPolishing
(*
========================================================================================================================
  LUMINA AI CYBER-PHYSICAL SYSTEMS & ADVANCED INDUSTRIAL AUTOMATION ARCHITECTURE GROUP
  CRITICAL SEMICONDUCTOR SILICON FABRICATION REFERENCE IMPLEMENTATION — SYNTHETIC DATASET ENGINE V7
  
  SYSTEM DESIGNATION : 300MM SILICON WAFER CHEMICAL MECHANICAL PLANARIZATION (CMP) ADVANCED POLISHING STATION
  PROCESS PLATFORM   : DUAL-PLATEN ROTARY CMP TOOL WITH 5-ZONE INDEPENDENT AIR/MEMBRANE CARRIER HEAD & RETAINING RING
  ENDPOINT SUBSYSTEM : DUAL-MODE IN-LINE OPTICAL REFLECTANCE SPECTROMETRY & EDDY CURRENT COPPER THICKNESS SENSING (< 20 Å)
  PAD CONDITIONING   : RECIPROCATING DIAMOND CONDITIONING DISC SWEEP WITH REAL-TIME ACOUSTIC EMISSION WEAR MONITORING
  SLURRY DELIVERY    : MULTI-CHANNEL COLLOIDAL SILICA/ALUMINA SLURRY WITH IN-LINE PH, REDOX (ORP), AND TEMP REGULATION
  SAFETY INTEGRITY   : IEC 61508 / IEC 61511 SIL-2/SIL-3 REDUNDANT CARRIER VACUUM INTERLOCK & OVER-TORQUE E-STOP
  APPLICABLE NORMS   : SEMI S2-0715 (ENVIRONMENTAL, HEALTH & SAFETY GUIDELINES FOR SEMICONDUCTOR MANUFACTURING EQUIPMENT),
                       SEMI S8-0915 (SAFETY GUIDELINES FOR ERGONOMICS ENGINEERING), SEMI E10 (EQUIPMENT RELIABILITY),
                       SEMI E30 (GENERIC MODEL FOR COMMUNICATIONS AND CONTROL OF MANUFACTURING EQUIPMENT - GEM),
                       SEMI E58 (AUTOMATED WAFER HANDLING), ISA-18.2 / IEC 62682 (MANAGEMENT OF ALARM SYSTEMS),
                       DIN EN ISO 13849-1 (SAFETY OF MACHINERY - SAFETY-RELATED PARTS OF CONTROL SYSTEMS).
  AUTHOR             : 75+ YEARS VETERAN PRINCIPAL AUTOMATION FELLOW & CYBER-PHYSICAL SYSTEMS CHAIR
========================================================================================================================

  THEORETICAL & CYBER-PHYSICAL CHEMICAL MECHANICAL PLANARIZATION FOUNDATIONS:
  ----------------------------------------------------------------------------------------------------------------------
  1. PRESTONIAN MATERIAL REMOVAL RATE (MRR) & BOUNDARY LUBRICATION KINETICS:
     - In chemical mechanical planarization of sub-10nm advanced CMOS logic and 3D NAND copper interconnect structures,
       wafer surface topology planarization is governed macroscopically by Preston's Law:
           MRR(r, theta) = K_p(T, pH, zeta) * P(r, theta) * V_rel(r, theta)
       where:
           MRR      = Instantaneous local copper / dielectric film removal rate [Angstrom/min]
           K_p      = Modified Prestonian coefficient representing chemical tribochemical synergy [m^2 / N]
           P        = Local normal downforce pressure exerted by the flexible membrane carrier zone [psi] (N/m^2)
           V_rel    = Instantaneous relative sliding linear velocity between polishing pad and wafer [m/s]
     - Slurry Hydrodynamics and Lubrication Regimes (Modified Stribeck CMP Curve):
       The Sommerfeld number characterizes the fluid lubrication regime between wafer and polyurethane pad:
           So = (mu_slurry * V_rel) / (P_mean * h_pad_roughness)
       At high downforce and low kinematic velocity (So < 10^-6), contact occurs in the boundary lubrication regime,
       where direct contact between diamond-dressed pad asperities and copper wafer micro-peaks drives mechanical abrasion.
       At nominal production operating setpoints (So ~ 10^-5 to 10^-4), planarization operates in the mixed / partial
       hydrodynamic regime, where a sub-micron slurry liquid boundary film (thickness h_0 ~ 15 to 45 um) separates
       the wafer from the bulk pad matrix, transporting abrasive nanoparticles into contact zones.
     - Chemical Complexation Kinetics:
       Copper planarization relies on a dynamic oxidation-passivation-abrasion equilibrium:
         Step a: Slurry hydrogen peroxide (H2O2) rapidly oxidizes native Cu to Cu+ and Cu2+ cuprous/cupric oxides:
                 2 Cu + H2O2 -> Cu2O + H2O ; Cu2O + H2O2 -> 2 CuO + H2O
         Step b: Organic corrosion inhibitor Benzotriazole (BTA) reacts with copper oxides to form an insoluble,
                 highly protective Cu-BTA polymeric passivation film over low-lying pattern trenches:
                 n Cu+ + n BTA -> [Cu(I)-BTA]_n (passivation layer, thickness ~ 20 to 50 Angstrom)
         Step c: Elevated wafer micro-features experience high localized contact downforce P_local >> P_nominal,
                 causing abrasive silica nanoparticles (30 to 80 nm mean diameter) to abrade the fragile Cu-BTA film.
         Step d: Exposed copper micro-hills dissolve rapidly under organic complexing acids (e.g. citric or glycine),
                 achieving global planarization with minimal pattern dishing and oxide erosion.

  2. 5-ZONE CONCENTRIC CARRIER HEAD MECHANICS & EDGE ROLL-OFF (ERO) SUPPRESSION:
     - The 300mm wafer carrier head utilizes a multi-chamber pneumatic bladder with 5 independent concentric pressure zones:
       * Zone 1: Center membrane chamber           (Radius: 0 to 40 mm)
       * Zone 2: Inner-middle membrane chamber     (Radius: 40 to 80 mm)
       * Zone 3: Middle membrane chamber           (Radius: 80 to 115 mm)
       * Zone 4: Outer-middle membrane chamber     (Radius: 115 to 140 mm)
       * Zone 5: Edge membrane chamber             (Radius: 140 to 150 mm)
       * Retaining Ring (RR): Floating ceramic/polymer ring concentric with Zone 5 (Radius: 150 to 180 mm)
     - Edge Roll-Off (ERO) Dynamic Compensation:
       As the flexible polyurethane pad passes under the leading edge of the wafer, pad compression creates a dynamic
       wave-front ("pad rebounding phenomenon"). Without compensation, excessive edge pressure produces catastrophic
       edge roll-off (severe over-polishing within the outer 3 mm exclusion margin).
       The Retaining Ring exerts independent pneumatic downforce P_RR to pre-compress the incoming pad asperities,
       flattening the pad profile before it enters Zone 5. The carrier algorithm dynamically modulates the Retaining
       Ring to Zone 5 pressure ratio:
           Ratio_RR_Z5 = P_RR / P_Zone5 (Nominal: 1.15 to 1.35)
       Real-time closed-loop tuning maintains Within-Wafer Non-Uniformity (WIWNU) 1-sigma < 1.25% across all 5 zones.

  3. DUAL-MODE IN-LINE ENDPOINT DETECTION (EPD) TO SUB-20 ÅNGSTRÖM PRECISION:
     - Optical Reflectance Spectrometry:
       * A broadband xenon flash lamp or multi-wavelength spectrometer (400 to 850 nm) interrogates the wafer through
         a transparent quartz window hermetically embedded in the rotating platen once per revolution.
       * Thin-film optical interference creates constructive and destructive spectral fringes as the dielectric or
         remaining copper thickness thins. Reflectance intensity R(lambda, t) oscillates according to:
             2 * n_film * d(t) * cos(theta_refr) = m * lambda
       * As copper reaches full clearance and reveals the underlying high-reflectance tantalum/ruthenium barrier layer,
         the broadband optical reflectance signal exhibits a sharp step-change inflection point.
     - In-Situ High-Frequency Eddy Current Sensor:
       * Integrated inside the platen body beneath the pad, an electromagnetic probe coil excited at 2 to 10 MHz
         induces circular eddy currents in the conductive copper interconnect film.
       * The back-EMF and coil impedance shift Delta-Z = Delta-R + j*omega*Delta-L correlate strictly with copper sheet
         conductance:
             G_sheet = sigma_Cu * t_Cu  [Siemens]
       * Eddy current thickness sensing is completely impervious to opaque chemical slurry films and operates
         continuously throughout bulk polish down to 150 Angstrom residual copper thickness.
     - Dual-Sensor Fusion EPD Trigger:
       * Bulk Stage: High-speed Eddy Current tracking governs bulk polish down to t_residual = 350 Å.
       * Soft-Landing Stage: Optical spectrometry locks onto the interference slope dR/dt to identify initial barrier
         breakthrough and initiates soft-landing over-polish (< 20 Å precision) before barrier metal punch-through.

  4. PAD SURFACE DIAMOND CONDITIONER DYNAMICS & ACOUSTIC EMISSION MONITORING:
     - Polishing pad pores (microporous polyurethane, e.g. IC1000 with sub-pad) clog with abraded copper complexes
       and crushed silica abrasive particles during polishing ("pad glazing"), reducing friction coefficient and MRR.
     - An electroplated CVD diamond conditioning disc (diameter 100 mm) oscillates across the platen radius in a
       controlled sinusoidal or constant-velocity sweep profile:
           r_cond(t) = R_inner + A_sweep * [ 0.5 - 0.5 * cos(omega_sweep * t) ]
     - The conditioning disc downforce F_cond (typically 6.0 to 12.0 lbf) and rotation speed omega_cond (90 to 110 rpm)
       dress the pad, restoring the asperity height distribution and pad surface roughness (Ra ~ 4.5 to 7.0 um).
     - Acoustic Emission (AE) Piezoelectric Sensors (Bandwidth: 100 kHz to 1.0 MHz):
       Mounted on the conditioning arm spindle, AE sensors capture elastic stress waves generated by diamond micro-cutting
       and pad asperity fracture. The Root-Mean-Square (RMS) AE signal amplitude:
           V_AE_RMS = sqrt( (1/T_w) * integral_0^Tw V_AE(t)^2 dt )
       AE signal drop indicates diamond grit loss, pad wear-out, or hydroplaning, triggering automatic pad re-dressing
       or pad lifecycle replacement interlocks.

  5. 8-STATE DISCRETE CYBER-PHYSICAL STATE-SPACE FORMULATION (Ts = 0.005 s / 5 ms):
     - Discrete Time State Equation:
           x[k+1] = A * x[k] + B * u[k] + E * d[k]
           y[k]   = C * x[k] + D * u[k]
     - State Vector x (8x1):
         x[1]: Platen Rotational Angular Velocity                     [rpm]
         x[2]: Wafer Carrier Rotational Angular Velocity              [rpm]
         x[3]: Weighted Multi-Zone Membrane Downforce Pressure        [psi]
         x[4]: Remaining Wafer Copper/Interconnect Film Thickness     [Angstrom]
         x[5]: Polyurethane Polishing Pad Surface Bulk Temperature    [deg C]
         x[6]: Interfacial CMP Friction Torque at Platen Spindle      [Nm]
         x[7]: Active Slurry Chemical Volumetric Delivery Flow Rate   [mL/min]
         x[8]: Pad Diamond Conditioning Cut Rate (PCR)                [um/h]
     - Manipulated Input Vector u (8x1):
         u[1]: Platen Direct-Drive Motor Torque Command               [%] (0.0 to 100.0%)
         u[2]: Carrier Direct-Drive Motor Torque Command              [%] (0.0 to 100.0%)
         u[3]: Multi-Zone Membrane Master Pressure Regulator Command  [%] (0.0 to 100.0%)
         u[4]: Retaining Ring Downforce Pneumatic Regulator Command   [%] (0.0 to 100.0%)
         u[5]: Slurry Peristaltic Metering Pump Speed Command         [%] (0.0 to 100.0%)
         u[6]: Conditioner Disc Downforce Cylinder Pressure Command   [%] (0.0 to 100.0%)
         u[7]: Conditioner Arm Radial Sweep Servo Velocity Command    [%] (0.0 to 100.0%)
         u[8]: High-Pressure De-Ionized Water (DIW) Rinse Flush Valve [%] (0.0 to 100.0%)
     - Disturbance Input Vector d (4x1):
         d[1]: Incoming Wafer Initial Copper Layer Thickness Drift    [Angstrom]
         d[2]: Slurry Supply Header Temperature Variance              [deg C]
         d[3]: Bulk Slurry Chemical pH Deviation from Target (3.0)   [pH units]
         d[4]: Pad Glaze / Diamond Grit Wear State Index              [dimensionless, 0.0 to 1.0]

  6. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) ARCHITECTURE:
     - Prediction Horizon N_p = 5 steps (25 ms look-ahead), Control Horizon N_u = 3 steps.
     - Multi-Objective Quadratic Cost Functional:
           J = sum_{i=1}^{Np} (x[k+i] - x_ref)' * Q * (x[k+i] - x_ref)
             + sum_{j=0}^{Nu-1} (u[k+j] - u_ref)' * R * (u[k+j] - u_ref)
             + sum_{j=0}^{Nu-1} delta_u[k+j]' * S * delta_u[k+j]
             + (x[k+Np] - x_ref)' * P * (x[k+Np] - x_ref)
     - Projected Gradient Descent (PGD) with physical box saturation [u_min, u_max] and dynamic slew-rate limiters.
*)
VAR_INPUT
    (* ============================================================================================== *)
    (* MASTER SYSTEM ENABLES, RUN COMMANDS & SIL-3 SAFETY SIGNALS                                     *)
    (* ============================================================================================== *)
    bSystemEnable                       : BOOL;     (* Master Tool Enable / 480VAC Main Contactor Permissive *)
    bProductionRunCmd                   : BOOL;     (* Production Cycle Start Command from Host SECS/GEM Interface *)
    bEmergencyStop                      : BOOL;     (* Hardwired SIL-3 Safety Circuit Status (1=Healthy, 0=Tripped) *)
    bAlarmAcknowledge                   : BOOL;     (* Operator Alarm Acknowledge Pushbutton / HMI Trigger *)
    bAlarmReset                         : BOOL;     (* Master Alarm Reset Pushbutton / HMI Trigger *)
    bRecipeStartCmd                     : BOOL;     (* Wafer Process Recipe Execution Trigger *)
    nActiveRecipeID                     : INT;      (* Active Wafer Polishing Recipe ID (1=Bulk Cu, 2=Barrier, 3=Oxide) *)
    
    (* ============================================================================================== *)
    (* WAFER CARRIER MECHANICS & ROBOTIC TRANSFER SIGNALS                                             *)
    (* ============================================================================================== *)
    bWaferPresent_LoadCup               : BOOL;     (* Optical Sensor: 300mm Silicon Wafer Present in Load Cup *)
    bWaferChucked_Carrier               : BOOL;     (* Capacitive Sensor: Wafer Confirmed Sealed on Carrier Head Membrane *)
    rCarrierVacuum_kPa                  : REAL;     (* Carrier Chucking Vacuum Level [-101.3 to 0.0 kPa] *)
    rCarrierZAxisPosition_mm            : REAL;     (* Carrier Head Vertical Z-Axis Height Above Pad [mm] *)
    rCarrierZAxisVelocity_mmps          : REAL;     (* Carrier Head Vertical Z-Axis Descent/Lift Velocity [mm/s] *)
    rCarrierHeadAngle_deg               : REAL;     (* Carrier Head Gimbal / Tilt Angle [deg] *)
    
    (* ============================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANT (TMR) PRIMARY INSTRUMENTATION CHANNELS                           *)
    (* ============================================================================================== *)
    (* In-Line Spectrometric Optical Reflectance Intensity [%] *)
    rOptReflectance_A_pct               : REAL;     (* Spectrometric Optical Reflectance Channel A [%] *)
    rOptReflectance_B_pct               : REAL;     (* Spectrometric Optical Reflectance Channel B [%] *)
    rOptReflectance_C_pct               : REAL;     (* Spectrometric Optical Reflectance Channel C [%] *)
    
    (* In-Situ High-Frequency Eddy Current Copper Film Thickness [Angstrom] *)
    rEddyCurrent_Thick_A_Angstrom       : REAL;     (* Eddy Current Film Thickness Probe Channel A [Angstrom] *)
    rEddyCurrent_Thick_B_Angstrom       : REAL;     (* Eddy Current Film Thickness Probe Channel B [Angstrom] *)
    rEddyCurrent_Thick_C_Angstrom       : REAL;     (* Eddy Current Film Thickness Probe Channel C [Angstrom] *)
    
    (* Platen Direct-Drive Reaction Torque Load Cells [Nm] *)
    rPlatenTorque_A_Nm                  : REAL;     (* Platen Reaction Torque Load Cell Channel A [Nm] *)
    rPlatenTorque_B_Nm                  : REAL;     (* Platen Reaction Torque Load Cell Channel B [Nm] *)
    rPlatenTorque_C_Nm                  : REAL;     (* Platen Reaction Torque Load Cell Channel C [Nm] *)
    
    (* Wafer Carrier Membrane Zone 1 (Center) Pressure Transducers [psi] *)
    rZone1_Press_A_psi                  : REAL;     (* Zone 1 Center Membrane Pressure Transducer Channel A [psi] *)
    rZone1_Press_B_psi                  : REAL;     (* Zone 1 Center Membrane Pressure Transducer Channel B [psi] *)
    rZone1_Press_C_psi                  : REAL;     (* Zone 1 Center Membrane Pressure Transducer Channel C [psi] *)
    
    (* Polishing Pad Surface Non-Contact Infrared Pyrometers [deg C] *)
    rPadIRTemp_A_degC                   : REAL;     (* Pad Surface Infrared Optical Pyrometer Channel A [deg C] *)
    rPadIRTemp_B_degC                   : REAL;     (* Pad Surface Infrared Optical Pyrometer Channel B [deg C] *)
    rPadIRTemp_C_degC                   : REAL;     (* Pad Surface Infrared Optical Pyrometer Channel C [deg C] *)
    
    (* ============================================================================================== *)
    (* MULTI-ZONE MEMBRANE PRESSURE & KINEMATIC PROCESS SENSORS                                       *)
    (* ============================================================================================== *)
    rZonePress_PV_01_psi                : REAL;     (* Zone 1 (Center: 0-40mm) Actual Membrane Downforce [psi] *)
    rZonePress_PV_02_psi                : REAL;     (* Zone 2 (Inner-Mid: 40-80mm) Actual Membrane Downforce [psi] *)
    rZonePress_PV_03_psi                : REAL;     (* Zone 3 (Mid: 80-115mm) Actual Membrane Downforce [psi] *)
    rZonePress_PV_04_psi                : REAL;     (* Zone 4 (Outer-Mid: 115-140mm) Actual Membrane Downforce [psi] *)
    rZonePress_PV_05_psi                : REAL;     (* Zone 5 (Edge: 140-150mm) Actual Membrane Downforce [psi] *)
    rRetainingRingPress_PV_psi          : REAL;     (* Retaining Ring Downforce Actual Pressure [psi] *)
    rPlatenSpeed_PV_rpm                 : REAL;     (* Main Direct-Drive Platen Rotational Speed Feedback [rpm] *)
    rCarrierSpeed_PV_rpm                : REAL;     (* Wafer Carrier Direct-Drive Spindle Rotational Speed [rpm] *)
    rCarrierSweepPosition_mm            : REAL;     (* Carrier Radial Sweep Arm Horizontal Coordinate [mm] *)
    
    (* ============================================================================================== *)
    (* CHEMICAL SLURRY & PAD CONDITIONER PROCESS FEEDBACK                                             *)
    (* ============================================================================================== *)
    rSlurryFlow_PV_mLpm                 : REAL;     (* Active Chemical Slurry Volumetric Flow Rate [mL/min] *)
    rSlurryTemp_PV_degC                 : REAL;     (* In-Line Slurry Delivery Temperature [deg C] *)
    rSlurryPH_PV_pH                     : REAL;     (* Chemical Slurry Real-Time Acidity/Alkalinity [pH units] *)
    rSlurryORP_PV_mV                    : REAL;     (* Chemical Slurry Oxidation-Reduction Potential [mV] *)
    rSlurrySupplyPressure_bar           : REAL;     (* Slurry Recirculation Loop Header Supply Pressure [bar] *)
    rCondArmPosition_mm                 : REAL;     (* Diamond Conditioner Sweep Arm Radial Position [mm] *)
    rCondSpeed_PV_rpm                   : REAL;     (* Diamond Conditioner Spindle Rotational Speed [rpm] *)
    rCondDownforce_PV_lbf               : REAL;     (* Diamond Conditioner Pneumatic Cylinder Downforce [lbf] *)
    rCondAcousticEmission_RMS_mV        : REAL;     (* Conditioner Acoustic Emission Piezo Sensor Signal [mV] *)
    
    (* ============================================================================================== *)
    (* CLEANROOM FACILITY & UTILITIES TELEMETRY                                                       *)
    (* ============================================================================================== *)
    rDIW_SupplyPressure_bar             : REAL;     (* Ultra-Pure De-Ionized Water (DIW) Header Pressure [bar] *)
    rPneumaticSupplyPressure_bar        : REAL;     (* Clean Dry Air (CDA) Facility Header Pressure [bar] *)
    rExhaustNegativePressure_Pa         : REAL;     (* CMP Enclosure Scrubber Acid Exhaust Draft [-Pa] *)
    rCleanroomAmbientTemp_degC          : REAL;     (* Fab Bay Sub-Class 1 Cleanroom Ambient Temp [deg C] *)
END_VAR
VAR_OUTPUT
    (* ============================================================================================== *)
    (* MASTER SYSTEM STATUS & PRODUCTION SUPERVISORY FLAGS                                           *)
    (* ============================================================================================== *)
    bSystemReady                        : BOOL;     (* CMP Station Pre-Conditioned, Interlocks Clear, Ready *)
    bProductionActive                   : BOOL;     (* Active Automated Wafer Polishing Cycle in Progress *)
    bEmergencyTripActive                : BOOL;     (* SIL-3 Safety Circuit Interlock or Wafer Slip Tripped *)
    nOperationalState                   : INT;      (* Current CMP Production Finite State Machine State Code (0-14) *)
    bWaferPolishedComplete              : BOOL;     (* Target Film Thickness & Over-Polish Completed Successfully *)
    bEndpointDetected                   : BOOL;     (* In-Line Optical & Eddy Current Endpoint Triggered *)
    
    (* ============================================================================================== *)
    (* 2oo3 TMR VALIDATED SENSOR VALUES & PROCESS ESTIMATES                                           *)
    (* ============================================================================================== *)
    rVotedOpticalReflectance_pct        : REAL;     (* 2oo3 TMR Validated Optical Reflectance Intensity [%] *)
    rVotedFilmThickness_Angstrom        : REAL;     (* 2oo3 TMR Validated Copper Film Thickness [Angstrom] *)
    rVotedPlatenTorque_Nm               : REAL;     (* 2oo3 TMR Validated Platen Drive Friction Torque [Nm] *)
    rVotedPadTemp_degC                  : REAL;     (* 2oo3 TMR Validated Polyurethane Pad Surface Temp [deg C] *)
    rVotedZone1Press_psi                : REAL;     (* 2oo3 TMR Validated Carrier Center Membrane Pressure [psi] *)
    rComputedMRR_AngstromPerMin         : REAL;     (* Real-Time Prestonian Instantaneous Removal Rate [Angstrom/min] *)
    rWIWNU_OneSigma_pct                 : REAL;     (* Within-Wafer Non-Uniformity 1-Sigma Metric [%] *)
    rEstimatedRemainingTime_s           : REAL;     (* Real-Time Estimated Seconds to Target Endpoint [s] *)
    
    (* ============================================================================================== *)
    (* MOTION ACTUATOR & SPINDLE SPEED/TORQUE COMMANDS                                                *)
    (* ============================================================================================== *)
    rPlatenMotorTorqueCmd_pct           : REAL;     (* Platen Direct-Drive Motor Torque Command [%] *)
    rPlatenSpeedSetpoint_rpm            : REAL;     (* Platen Direct-Drive Closed-Loop Speed Setpoint [rpm] *)
    rCarrierMotorTorqueCmd_pct          : REAL;     (* Wafer Carrier Motor Torque Command [%] *)
    rCarrierSpeedSetpoint_rpm           : REAL;     (* Wafer Carrier Closed-Loop Speed Setpoint [rpm] *)
    rCarrierZAxisDriveCmd_pct           : REAL;     (* Carrier Vertical Z-Axis Servo Drive Command [%] *)
    rCarrierSweepVelocityCmd_mmps       : REAL;     (* Carrier Radial Sweep Arm Horizontal Velocity [mm/s] *)
    
    (* ============================================================================================== *)
    (* 5-ZONE MEMBRANE PRESSURE & RETAINING RING PNEUMATIC COMMANDS                                   *)
    (* ============================================================================================== *)
    rZonePressCmd_01_psi                : REAL;     (* Zone 1 Center Membrane Proportional Pressure Command [psi] *)
    rZonePressCmd_02_psi                : REAL;     (* Zone 2 Inner-Mid Membrane Proportional Pressure Command [psi] *)
    rZonePressCmd_03_psi                : REAL;     (* Zone 3 Mid Membrane Proportional Pressure Command [psi] *)
    rZonePressCmd_04_psi                : REAL;     (* Zone 4 Outer-Mid Membrane Proportional Pressure Command [psi] *)
    rZonePressCmd_05_psi                : REAL;     (* Zone 5 Edge Membrane Proportional Pressure Command [psi] *)
    rRetainingRingPressCmd_psi          : REAL;     (* Retaining Ring Pneumatic Chamber Pressure Command [psi] *)
    bCarrierVacuumSolenoidCmd           : BOOL;     (* Carrier Wafer Chucking Vacuum Isolation Valve Solenoid *)
    
    (* ============================================================================================== *)
    (* CHEMICAL SLURRY & DE-IONIZED WATER ACTUATOR COMMANDS                                           *)
    (* ============================================================================================== *)
    rSlurryPumpFlowCmd_mLpm             : REAL;     (* Slurry Peristaltic Metering Pump Volumetric Command [mL/min] *)
    rSlurryArmSweepAngleCmd_deg         : REAL;     (* Slurry Delivery Arm Radial Swing Angle Command [deg] *)
    bSlurryDeliveryValveCmd             : BOOL;     (* Slurry Injector Nozzle Pneumatic Pinch Valve Command *)
    bDIW_FlushValveCmd                  : BOOL;     (* De-Ionized Water High-Volume Platen Flush Valve *)
    bHighPressurePadRinseCmd            : BOOL;     (* Pad Conditioner High-Pressure DIW Jet Spray Solenoid *)
    
    (* ============================================================================================== *)
    (* DIAMOND CONDITIONER ACTUATOR COMMANDS                                                          *)
    (* ============================================================================================== *)
    rCondHeadSpeedCmd_rpm               : REAL;     (* Diamond Conditioner Head Spindle Speed Setpoint [rpm] *)
    rCondDownforceCmd_lbf               : REAL;     (* Conditioner Head Pneumatic Cylinder Downforce [lbf] *)
    rCondSweepVelocityCmd_mmps          : REAL;     (* Conditioner Radial Arm Oscillation Velocity Command [mm/s] *)
    bCondArmInService                   : BOOL;     (* Conditioner Arm Positioned Over Platen Status Flag *)
    
    (* ============================================================================================== *)
    (* BIT-PACKED STATUS WORDS & ISA-18.2 ALARM GROUPS                                               *)
    (* ============================================================================================== *)
    dwCMP_StatusWord                    : DWORD;    (* 32-Bit CMP Machine Operational Status Bitmask *)
    dwCMP_DiagnosticWord                : DWORD;    (* 32-Bit Hardware Safety & Sensor Health Bitmask *)
    bAlarmGroup_CriticalEStop           : BOOL;     (* Priority 1 Critical E-Stop or Safety Door Open Tripped *)
    bAlarmGroup_WaferSlipLoss           : BOOL;     (* Priority 1 Wafer Slippage / Vacuum Loss During Polish *)
    bAlarmGroup_OverTorque              : BOOL;     (* Priority 2 Platen/Carrier Spindle Over-Torque Hazard *)
    bAlarmGroup_SlurryDeliveryFault     : BOOL;     (* Priority 2 Chemical Slurry Low Flow / pH Excursion *)
    bAlarmGroup_ConditionerFault        : BOOL;     (* Priority 2 Pad Conditioner Diamond Loss / Acoustic Emission *)
    bAlarmGroup_ThermalExcursion        : BOOL;     (* Priority 2 Pad Surface Over-Temperature Trip *)
    bAlarmGroup_TMR_SensorDiscrepancy   : BOOL;     (* Priority 3 TMR Triplicate Sensor Divergence Warning *)
END_VAR
VAR
    (* ============================================================================================== *)
    (* CONSTANTS & SYSTEM TIMING DEFINITIONS                                                          *)
    (* ============================================================================================== *)
    T_CYCLE_SEC                         : REAL := 0.005;    (* Discrete Real-Time PLC Scan Interval Ts = 5 ms [s] *)
    NUM_STATES                          : INT := 8;         (* Cyber-Physical Dynamic State Dimension *)
    NUM_INPUTS                          : INT := 8;         (* Manipulated Actuator Command Dimension *)
    NUM_DISTURBANCES                    : INT := 4;         (* External Disturbance Input Dimension *)
    HORIZON_NP                          : INT := 5;         (* Receding-Horizon Prediction Horizon Steps *)
    HORIZON_NU                          : INT := 3;         (* Receding-Horizon Control Horizon Steps *)
    
    (* ============================================================================================== *)
    (* DISCRETE STATE-SPACE MATRICES & LUENBERGER OBSERVER                                            *)
    (* x[k+1] = A * x[k] + B * u[k] + E * d[k]                                                        *)
    (* y[k]   = C * x[k] + D * u[k]                                                                   *)
    (* ============================================================================================== *)
    a_mat                               : ARRAY[1..8, 1..8] OF REAL;    (* State Transition Matrix A (8x8) *)
    b_mat                               : ARRAY[1..8, 1..8] OF REAL;    (* Input Coupling Matrix B (8x8) *)
    c_mat                               : ARRAY[1..8, 1..8] OF REAL;    (* State Output Matrix C (8x8) *)
    d_mat                               : ARRAY[1..8, 1..8] OF REAL;    (* Direct Feedthrough Matrix D (8x8) *)
    e_mat                               : ARRAY[1..8, 1..4] OF REAL;    (* Disturbance Coupling Matrix E (8x4) *)
    l_observer_gain                     : ARRAY[1..8] OF REAL;          (* Luenberger Observer Innovation Gain Vector *)
    
    x_state                             : ARRAY[1..8] OF REAL;          (* Estimated Cyber-Physical State x[k] *)
    x_next                              : ARRAY[1..8] OF REAL;          (* State Propagation Vector x[k+1] *)
    y_meas                              : ARRAY[1..8] OF REAL;          (* Process Measurement Vector y[k] *)
    y_pred                              : ARRAY[1..8] OF REAL;          (* Predicted Measurement Vector y_hat[k] *)
    u_ctrl                              : ARRAY[1..8] OF REAL;          (* Manipulated Control Input Vector u[k] *)
    d_dist                              : ARRAY[1..4] OF REAL;          (* External Disturbance Estimate Vector *)
    x_ref                               : ARRAY[1..8] OF REAL;          (* Reference State Setpoint Trajectory *)
    u_ref                               : ARRAY[1..8] OF REAL;          (* Nominal Equilibrium Actuator Command *)
    u_prev                              : ARRAY[1..8] OF REAL;          (* Previous Cycle Actuator Command u[k-1] *)
    
    (* ============================================================================================== *)
    (* MODEL PREDICTIVE CONTROL (MPC) COST MATRICES & PGD OPTIMIZATION                                *)
    (* ============================================================================================== *)
    q_diag                              : ARRAY[1..8] OF REAL;          (* State Tracking Penalty Diagonal Q *)
    r_diag                              : ARRAY[1..8] OF REAL;          (* Actuator Effort Penalty Diagonal R *)
    s_diag                              : ARRAY[1..8] OF REAL;          (* Actuator Slew Rate Penalty Diagonal S *)
    p_diag                              : ARRAY[1..8] OF REAL;          (* Terminal State Penalty Diagonal P *)
    u_box_min                           : ARRAY[1..8] OF REAL;          (* Actuator Physical Lower Bound Box Saturation *)
    u_box_max                           : ARRAY[1..8] OF REAL;          (* Actuator Physical Upper Bound Box Saturation *)
    du_slew_max                         : ARRAY[1..8] OF REAL;          (* Maximum Allowable Actuator Rate of Change *)
    
    u_mpc_traj                          : ARRAY[1..5, 1..8] OF REAL;    (* Receding Horizon Control Candidate Trajectory *)
    grad_u                              : ARRAY[1..8] OF REAL;          (* Projected Gradient Descent Gradient Vector *)
    u_tentative                         : ARRAY[1..8] OF REAL;          (* Candidate Actuator Command Update *)
    rMpcAlphaStep                       : REAL := 0.045;                (* PGD Optimization Gradient Step Length *)
    rTotalCostFunctional                : REAL;                         (* Accumulated Quadratic MPC Cost J *)
    
    (* ============================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) STRUCTURES & FAULT ISOLATION                              *)
    (* ============================================================================================== *)
    (* Spectrometric Optical Reflectance TMR Channels *)
    rOpt_Delta_AB                       : REAL;     (* |Reflectance A - Reflectance B| [%] *)
    rOpt_Delta_BC                       : REAL;     (* |Reflectance B - Reflectance C| [%] *)
    rOpt_Delta_CA                       : REAL;     (* |Reflectance C - Reflectance A| [%] *)
    rOpt_DiscrepancyLimit_pct           : REAL := 4.5;      (* Permissible Optical Deviation Threshold [%] *)
    rOpt_DiscrepancyTimer_s             : REAL := 0.0;      (* Cumulative Optical Discrepancy Integrator [s] *)
    bOpt_ChannelA_Valid                 : BOOL := TRUE;     (* Channel A Optical Sensor Health Flag *)
    bOpt_ChannelB_Valid                 : BOOL := TRUE;     (* Channel B Optical Sensor Health Flag *)
    bOpt_ChannelC_Valid                 : BOOL := TRUE;     (* Channel C Optical Sensor Health Flag *)
    nOpt_DegradedVotingMode             : INT := 3;         (* 3=2oo3 TMR, 2=1oo2 Average, 1=Single, 0=Fail-Safe *)
    
    (* Eddy Current Film Thickness TMR Channels *)
    rEddy_Delta_AB                      : REAL;     (* |Eddy A - Eddy B| [Angstrom] *)
    rEddy_Delta_BC                      : REAL;     (* |Eddy B - Eddy C| [Angstrom] *)
    rEddy_Delta_CA                      : REAL;     (* |Eddy C - Eddy A| [Angstrom] *)
    rEddy_DiscrepancyLimit_Angstrom     : REAL := 120.0;    (* Permissible Eddy Thickness Deviation [Angstrom] *)
    rEddy_DiscrepancyTimer_s            : REAL := 0.0;      (* Cumulative Eddy Discrepancy Integrator [s] *)
    bEddy_ChannelA_Valid                : BOOL := TRUE;     (* Channel A Eddy Sensor Health Flag *)
    bEddy_ChannelB_Valid                : BOOL := TRUE;     (* Channel B Eddy Sensor Health Flag *)
    bEddy_ChannelC_Valid                : BOOL := TRUE;     (* Channel C Eddy Sensor Health Flag *)
    nEddy_DegradedVotingMode            : INT := 3;         (* 3=2oo3 TMR, 2=1oo2 Average, 1=Single, 0=Fail-Safe *)
    
    (* Platen Drive Reaction Torque TMR Channels *)
    rTorq_Delta_AB                      : REAL;     (* |Torque A - Torque B| [Nm] *)
    rTorq_Delta_BC                      : REAL;     (* |Torque B - Torque C| [Nm] *)
    rTorq_Delta_CA                      : REAL;     (* |Torque C - Torque A| [Nm] *)
    rTorq_DiscrepancyLimit_Nm           : REAL := 8.5;      (* Permissible Torque Deviation Margin [Nm] *)
    rTorq_DiscrepancyTimer_s            : REAL := 0.0;      (* Cumulative Torque Discrepancy Integrator [s] *)
    bTorq_ChannelA_Valid                : BOOL := TRUE;     (* Channel A Torque Load Cell Health Flag *)
    bTorq_ChannelB_Valid                : BOOL := TRUE;     (* Channel B Torque Load Cell Health Flag *)
    bTorq_ChannelC_Valid                : BOOL := TRUE;     (* Channel C Torque Load Cell Health Flag *)
    nTorq_DegradedVotingMode            : INT := 3;         (* 3=2oo3 TMR, 2=1oo2 Average, 1=Single, 0=Fail-Safe *)
    
    (* Membrane Zone 1 Pressure Transducer TMR Channels *)
    rZ1P_Delta_AB                       : REAL;     (* |Zone 1 Press A - Press B| [psi] *)
    rZ1P_Delta_BC                       : REAL;     (* |Zone 1 Press B - Press C| [psi] *)
    rZ1P_Delta_CA                       : REAL;     (* |Zone 1 Press C - Press A| [psi] *)
    rZ1P_DiscrepancyLimit_psi           : REAL := 0.25;     (* Permissible Pressure Transducer Deviation [psi] *)
    rZ1P_DiscrepancyTimer_s             : REAL := 0.0;      (* Cumulative Zone 1 Discrepancy Integrator [s] *)
    bZ1P_ChannelA_Valid                 : BOOL := TRUE;     (* Channel A Zone 1 Transducer Health Flag *)
    bZ1P_ChannelB_Valid                 : BOOL := TRUE;     (* Channel B Zone 1 Transducer Health Flag *)
    bZ1P_ChannelC_Valid                 : BOOL := TRUE;     (* Channel C Zone 1 Transducer Health Flag *)
    nZ1P_DegradedVotingMode             : INT := 3;         (* 3=2oo3 TMR, 2=1oo2 Average, 1=Single, 0=Fail-Safe *)
    
    (* Polishing Pad Surface Infrared Pyrometer TMR Channels *)
    rPadT_Delta_AB                      : REAL;     (* |Pad Temp A - Pad Temp B| [deg C] *)
    rPadT_Delta_BC                      : REAL;     (* |Pad Temp B - Pad Temp C| [deg C] *)
    rPadT_Delta_CA                      : REAL;     (* |Pad Temp C - Pad Temp A| [deg C] *)
    rPadT_DiscrepancyLimit_degC         : REAL := 2.2;      (* Permissible Pad Pyrometer Deviation [deg C] *)
    rPadT_DiscrepancyTimer_s            : REAL := 0.0;      (* Cumulative Pad Pyrometer Discrepancy Integrator [s] *)
    bPadT_ChannelA_Valid                : BOOL := TRUE;     (* Channel A Pad Pyrometer Health Flag *)
    bPadT_ChannelB_Valid                : BOOL := TRUE;     (* Channel B Pad Pyrometer Health Flag *)
    bPadT_ChannelC_Valid                : BOOL := TRUE;     (* Channel C Pad Pyrometer Health Flag *)
    nPadT_DegradedVotingMode            : INT := 3;         (* 3=2oo3 TMR, 2=1oo2 Average, 1=Single, 0=Fail-Safe *)
    
    (* Discrepancy Persistence Threshold *)
    rDiscrepancyPersistLimit_s          : REAL := 0.350;    (* Persistent Divergence Time Prior to Channel Trip [s] *)
    
    (* ============================================================================================== *)
    (* 5-ZONE CARRIER HEAD CLOSED-LOOP PROFILE VARIABLES                                              *)
    (* ============================================================================================== *)
    rZoneTarget_01_psi                  : REAL := 2.80;     (* Zone 1 Recipe Downforce Setpoint [psi] *)
    rZoneTarget_02_psi                  : REAL := 2.85;     (* Zone 2 Recipe Downforce Setpoint [psi] *)
    rZoneTarget_03_psi                  : REAL := 2.90;     (* Zone 3 Recipe Downforce Setpoint [psi] *)
    rZoneTarget_04_psi                  : REAL := 2.95;     (* Zone 4 Recipe Downforce Setpoint [psi] *)
    rZoneTarget_05_psi                  : REAL := 3.10;     (* Zone 5 Recipe Downforce Setpoint [psi] *)
    rRetainingRingTarget_psi            : REAL := 3.85;     (* Retaining Ring Recipe Downforce Setpoint [psi] *)
    
    rZoneError_01_psi                   : REAL;             (* Zone 1 Tracking Error [psi] *)
    rZoneError_02_psi                   : REAL;             (* Zone 2 Tracking Error [psi] *)
    rZoneError_03_psi                   : REAL;             (* Zone 3 Tracking Error [psi] *)
    rZoneError_04_psi                   : REAL;             (* Zone 4 Tracking Error [psi] *)
    rZoneError_05_psi                   : REAL;             (* Zone 5 Tracking Error [psi] *)
    rRetainingRingError_psi             : REAL;             (* Retaining Ring Tracking Error [psi] *)
    
    rZoneInt_01_psi                     : REAL := 0.0;      (* Zone 1 Anti-Windup Error Integrator [psi*s] *)
    rZoneInt_02_psi                     : REAL := 0.0;      (* Zone 2 Anti-Windup Error Integrator [psi*s] *)
    rZoneInt_03_psi                     : REAL := 0.0;      (* Zone 3 Anti-Windup Error Integrator [psi*s] *)
    rZoneInt_04_psi                     : REAL := 0.0;      (* Zone 4 Anti-Windup Error Integrator [psi*s] *)
    rZoneInt_05_psi                     : REAL := 0.0;      (* Zone 5 Anti-Windup Error Integrator [psi*s] *)
    rRetainingRingInt_psi               : REAL := 0.0;      (* Retaining Ring Anti-Windup Integrator [psi*s] *)
    
    rKp_ZonePressure                    : REAL := 1.25;     (* Zone Pressure Proportional Gain [1/psi] *)
    rKi_ZonePressure                    : REAL := 0.45;     (* Zone Pressure Integral Gain [1/(psi*s)] *)
    rEdgeRollOffFactor                  : REAL := 0.18;     (* Edge Roll-Off (ERO) Dynamic Tuning Factor *)
    
    (* Prestonian Relative Velocity & Radial Distribution *)
    rRadialPos_Zone1_m                  : REAL := 0.020;    (* Zone 1 Effective Center Radius [m] *)
    rRadialPos_Zone2_m                  : REAL := 0.060;    (* Zone 2 Effective Radius [m] *)
    rRadialPos_Zone3_m                  : REAL := 0.098;    (* Zone 3 Effective Radius [m] *)
    rRadialPos_Zone4_m                  : REAL := 0.128;    (* Zone 4 Effective Radius [m] *)
    rRadialPos_Zone5_m                  : REAL := 0.146;    (* Zone 5 Effective Outer Edge Radius [m] *)
    rPlatenTrackRadius_m                : REAL := 0.380;    (* Carrier Spindle Offset from Platen Center [m] *)
    rPrestonCoeff_Kp                    : REAL := 3.42E-7;  (* Tribochemical Preston Removal Coefficient [m^2/N] *)
    
    (* ============================================================================================== *)
    (* IN-LINE ENDPOINT DETECTION (EPD) ALGORITHM VARIABLES                                           *)
    (* ============================================================================================== *)
    rEpdThresholdThickness_Angstrom     : REAL := 220.0;    (* Eddy Current Soft-Landing Transition Threshold [Angstrom] *)
    rEpdFinalTargetThickness_Angstrom   : REAL := 45.0;     (* Target Interconnect Barrier Clearance Level [Angstrom] *)
    rEpdOpticalInflectionSlope          : REAL := -0.85;    (* Spectral Reflectance Breakthrough Slope [dRefl/dt] *)
    rFilteredThickness_Angstrom         : REAL := 8500.0;   (* 1st-Order Low-Pass Filtered Copper Thickness [Angstrom] *)
    rThicknessRateOfChange_Aps          : REAL := 0.0;      (* Instantaneous Copper Removal Rate d(Thick)/dt [Angstrom/s] *)
    rPrevThickness_Angstrom             : REAL := 8500.0;   (* Prior PLC Scan Thickness Sample [Angstrom] *)
    rFilteredOpticalReflectance         : REAL := 78.5;     (* Low-Pass Filtered Optical Reflectance [%] *)
    rOpticalSlope_pctps                 : REAL := 0.0;      (* Reflectance Rate of Change d(Refl)/dt [%/s] *)
    rPrevOpticalReflectance             : REAL := 78.5;     (* Prior PLC Scan Optical Sample [%] *)
    bOpticalEndpointLatched             : BOOL := FALSE;    (* Optical Breakthrough Inflection Verified Flag *)
    bEddyCurrentEndpointLatched         : BOOL := FALSE;    (* Eddy Current Threshold Cleared Flag *)
    rOverpolishTimer_s                  : REAL := 0.0;      (* Soft-Landing Controlled Over-Polish Integrator [s] *)
    rRecipeOverpolishTarget_s           : REAL := 4.25;     (* Recipe Soft-Landing Fixed Over-Polish Duration [s] *)
    
    (* ============================================================================================== *)
    (* CHEMICAL SLURRY & PAD CONDITIONER CASCADE CONTROLLERS                                          *)
    (* ============================================================================================== *)
    rSlurryFlowTarget_mLpm              : REAL := 250.0;    (* Recipe Slurry Flow Rate Setpoint [mL/min] *)
    rSlurryFlowError_mLpm               : REAL;             (* Slurry Delivery Flow Tracking Error [mL/min] *)
    rSlurryFlowInt_mLpm                 : REAL := 0.0;      (* Slurry Flow Error Integrator [mL/min*s] *)
    rKp_SlurryPump                      : REAL := 0.16;     (* Peristaltic Pump Proportional Gain *)
    rKi_SlurryPump                      : REAL := 0.08;     (* Peristaltic Pump Integral Gain *)
    
    (* Conditioner Sweep Profile Generator *)
    rCondSweepInnerLimit_mm             : REAL := 120.0;    (* Conditioner Inner Platen Sweep Radius [mm] *)
    rCondSweepOuterLimit_mm             : REAL := 480.0;    (* Conditioner Outer Platen Sweep Radius [mm] *)
    rCondSweepFrequency_Hz              : REAL := 0.18;     (* Sinusoidal Reciprocating Sweep Frequency [Hz] *)
    rCondSweepPhase_rad                 : REAL := 0.0;      (* Conditioner Harmonic Phase Angle [rad] *)
    rCondNominalDownforce_lbf           : REAL := 8.5;      (* Conditioner Target Downforce Load [lbf] *)
    rCondNominalSpeed_rpm               : REAL := 105.0;    (* Conditioner Spindle Speed Setpoint [rpm] *)
    rCondDownforceError_lbf             : REAL;             (* Conditioner Downforce Error [lbf] *)
    rCondDownforceInt_lbf               : REAL := 0.0;      (* Downforce Error Integrator [lbf*s] *)
    
    (* Acoustic Emission (AE) Signal Processing *)
    rCondAcousticRMS_Filtered_mV        : REAL := 45.0;     (* Filtered Acoustic Emission RMS Level [mV] *)
    rPadGlazeIndex                      : REAL := 0.05;     (* Pad Glazing Metric (0.0=Fresh Texturized, 1.0=Glazed) *)
    rDiamondWearAccumulator             : REAL := 0.0;      (* Cumulative Diamond Asperity Wear Metric *)
    
    (* ============================================================================================== *)
    (* DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)                                   *)
    (* ============================================================================================== *)
    nFsmCurrentState                    : INT := 0;         (* Active Operational State Index (0 to 14) *)
    nFsmPreviousState                   : INT := 0;         (* Previous Operational State Index *)
    rStateTimer_s                       : REAL := 0.0;      (* Active State Elapsed Timer [s] *)
    rStateTimeout_s                     : REAL := 120.0;    (* State Abort Maximum Permitted Dwell [s] *)
    bStateFirstScan                     : BOOL := TRUE;     (* One-Shot Rising Edge Transition Marker *)
    
    (* FSM State Code Encodings *)
    STATE_CMP_IDLE_STANDBY              : INT := 0;         (* Standby Ready, Vacuum Off, Arms Parked *)
    STATE_CMP_WAFER_LOAD_CUP_HANDSHAKE  : INT := 1;         (* Load Cup Transfer & Carrier Vacuum Chucking *)
    STATE_CMP_PLATEN_SWEEP_AND_DESCENT  : INT := 2;         (* Platen Spin-Up, Carrier Sweeps Over Platen *)
    STATE_CMP_LOW_PRESSURE_TOUCHDOWN    : INT := 3;         (* Touch-Down, Slurry Pre-Wet, Low Downforce *)
    STATE_CMP_MULTI_ZONE_BULK_RAMP      : INT := 4;         (* Multi-Zone Pressure Ramp, Bulk Cu Removal *)
    STATE_CMP_STEADY_STATE_POLISH       : INT := 5;         (* Steady-State MPC Polish, Eddy Current Mon *)
    STATE_CMP_OPTICAL_EPD_LOCK          : INT := 6;         (* Optical Reflectance EPD Lock, Barrier Crossing *)
    STATE_CMP_SOFT_LANDING_OVERPOLISH   : INT := 7;         (* Reduced Downforce Soft Landing Over-Polish *)
    STATE_CMP_DIW_HIGH_PRESSURE_FLUSH   : INT := 8;         (* DIW Flush, Stop Slurry, Pad Rinse *)
    STATE_CMP_CARRIER_VACUUM_DECHUCK    : INT := 9;         (* Carrier High Lift, Vacuum Unclamp & Blow-Off *)
    STATE_CMP_UNLOAD_CUP_TRANSFER       : INT := 10;        (* Carrier Sweeps to Unload Cup, Hands Wafer Off *)
    STATE_CMP_IN_SITU_PAD_CONDITIONING  : INT := 11;        (* Post-Polish Pad Diamond Conditioning Sweep *)
    STATE_CMP_POST_CONDITION_AE_AUDIT   : INT := 12;        (* Acoustic Emission Pad Texture & PCR Check *)
    STATE_CMP_RECIPE_STEP_TRANSITION    : INT := 13;        (* Multi-Step Interconnect Layer Transition *)
    STATE_CMP_EMERGENCY_TRIP_VAC_LOSS   : INT := 14;        (* Emergency Vacuum Loss / Wafer Slip Retract *)
    
    (* ============================================================================================== *)
    (* ISA-18.2 MULTI-TIER ALARM TRIP SETPOINTS, DEADBANDS & TIMERS                                   *)
    (* ============================================================================================== *)
    (* Pad Temperature Alarms *)
    rPadTemp_Limit_HH_degC              : REAL := 65.0;     (* High-High Critical Pad Overtemp Trip [deg C] *)
    rPadTemp_Limit_H_degC               : REAL := 55.0;     (* High Pad Temperature Warning [deg C] *)
    rPadTemp_Deadband_degC              : REAL := 3.0;      (* Alarm Clearing Hysteresis [deg C] *)
    bAlarmPadTemp_HH                    : BOOL := FALSE;    (* Pad Temp High-High Latched Alarm *)
    bAlarmPadTemp_H                     : BOOL := FALSE;    (* Pad Temp High Latched Alarm *)
    
    (* Platen Spindle Torque Alarms *)
    rPlatenTorque_Limit_HH_Nm           : REAL := 195.0;    (* High-High Platen Mechanical Stall Trip [Nm] *)
    rPlatenTorque_Limit_H_Nm            : REAL := 160.0;    (* High Platen Friction Warning [Nm] *)
    rPlatenTorque_Deadband_Nm           : REAL := 8.0;      (* Torque Alarm Hysteresis [Nm] *)
    bAlarmPlatenTorque_HH               : BOOL := FALSE;    (* Platen Torque High-High Latched Alarm *)
    bAlarmPlatenTorque_H                : BOOL := FALSE;    (* Platen Torque High Latched Alarm *)
    
    (* Carrier Chucking Vacuum Alarms *)
    rCarrierVac_Limit_LL_kPa            : REAL := -35.0;    (* Low-Low Critical Wafer Chucking Loss [-kPa] *)
    rCarrierVac_Limit_L_kPa             : REAL := -55.0;    (* Low Chucking Vacuum Warning [-kPa] *)
    rCarrierVac_Deadband_kPa            : REAL := 5.0;      (* Vacuum Alarm Hysteresis [kPa] *)
    bAlarmCarrierVac_LL                 : BOOL := FALSE;    (* Carrier Vacuum Low-Low Latched Trip *)
    bAlarmCarrierVac_L                  : BOOL := FALSE;    (* Carrier Vacuum Low Latched Warning *)
    
    (* Slurry Delivery Alarms *)
    rSlurryFlow_Limit_LL_mLpm           : REAL := 120.0;    (* Low-Low Chemical Slurry Starvation Trip [mL/min] *)
    rSlurryFlow_Limit_L_mLpm            : REAL := 180.0;    (* Low Slurry Flow Warning [mL/min] *)
    rSlurryPH_Limit_HH                  : REAL := 4.2;      (* High-High Slurry Acidity Breakdown [pH] *)
    rSlurryPH_Limit_LL                  : REAL := 2.2;      (* Low-Low Slurry Acidic Overdose [pH] *)
    bAlarmSlurryFlow_LL                 : BOOL := FALSE;    (* Slurry Flow Low-Low Latched Trip *)
    bAlarmSlurryPH_Excursion            : BOOL := FALSE;    (* Slurry pH Out-of-Tolerance Alarm *)
    
    (* Diamond Conditioner Alarms *)
    rCondAE_Limit_LL_mV                 : REAL := 12.0;     (* Low-Low AE Signal: Diamond Disc Loss / Glaze [mV] *)
    rCondAE_Limit_HH_mV                 : REAL := 95.0;     (* High-High AE Signal: Disc Fracture / Pad Gouge [mV] *)
    bAlarmConditioner_AE_Fault          : BOOL := FALSE;    (* Conditioner Acoustic Emission Trip *)
    
    (* Loop Counters & Scratch Variables *)
    i_idx                               : INT;              (* General Loop Iterator *)
    j_idx                               : INT;              (* Secondary Loop Iterator *)
    k_idx                               : INT;              (* Third Loop Iterator *)
    rTempSum                            : REAL;             (* Floating Point Accumulator *)
    rTempVelRel                         : REAL;             (* Relative Sliding Velocity Scratch [m/s] *)
    rTempPressAvg                       : REAL;             (* Average Membrane Pressure Scratch [psi] *)
END_VAR
"""
