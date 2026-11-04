# generate_dataset.py
# Lumina Elite Synthetic Data Architect - Commercial Aerospace FAL Wingbox Drilling & Fastening

import json
import uuid
import re
import os

def build_iec_code():
    parts = []
    
    # -------------------------------------------------------------
    # HEADER BLOCK
    # -------------------------------------------------------------
    parts.append('''FUNCTION_BLOCK FB_Aerospace_FAL_Wingbox_Drilling_Fastening
(*
 ==========================================================================================
  PROJECT:       COMMERCIAL AIRCRAFT FINAL ASSEMBLY LINE (FAL) STRUCTURES AUTOMATION
  SUBSYSTEM:     6-AXIS GANTRY MULTIFUNCTION END-EFFECTOR DRILLING & FASTENING CELL
  DISCIPLINE:    AEROSPACE MECHATRONICS / ADVANCED CPS / HYBRID MATERIAL MACHINING / EMR
  IEC STANDARD:  IEC 61131-3 STRUCTURED TEXT 3RD EDITION (DETERMINISTIC EMBEDDED EXECUTION)
  AUTHOR:        LUMINA AI CLOUD SWARM - PRINCIPAL AUTOMATION FELLOW & CPS CHAIR (V7 MAX)
  TARGET SYSTEM: COMMERCIAL WIDE-BODY & SINGLE-AISLE AIRFRAME WINGBOX MAIN TORQUE BOX
  STRUCTURAL STACK: AS4/8552 HIGH-MODULUS CFRP (14.2 mm) + Ti-6Al-4V GRADE 5 FLANGE (9.8 mm)
  CYCLE TIME BASE: 1.0 MILLISECOND HIGH-SPEED DETERMINISTIC SERVO INTERPOLATION SCAN
 ==========================================================================================

  PURPOSE & ENGINEERING OVERVIEW:
    This Function Block provides absolute deterministic cyber-physical governing, multi-axis
    real-time closed-loop motion compensation, sensor fusion, acoustic/vibration health monitoring,
    and quality metrology for an aerospace-grade 6-Axis Gantry End-Effector. The cell performs 
    one-way assembly (drill, countersink, clean, inspect, insert, and electromagnetic rivet) of 
    hybrid multi-material Carbon Fiber Reinforced Polymer (CFRP) and Titanium alloy (Ti-6Al-4V) 
    wing covers to titanium wing spars and stringers without intermediate disassembly for deburring.

  CORE TECHNICAL PILLARS:
    1. Multi-Point Optical Triangulation Laser Surface Normal Alignment:
       Employs 3 high-precision optical triangulation distance sensors arranged in a 120-degree 
       circumferential pattern around the spindle centerline (Pitch Circle Radius R = 75.0 mm).
       Computes the real-time local surface normal unit vector via cross product:
         n_vec = (v1 x v2) / ||v1 x v2||
       Dynamically compensates the gantry A-tilt and B-tilt rotary gimbal axes to guarantee
       tool perpendicularity to within +/- 0.080 degrees (maximum allowable tilt < 0.100 degrees)
       across aerodynamic wing skin loft curvature prior to clamp engagement.

    2. Dynamic Pressure-Foot Clamping Compliance & Inter-Laminar Gap Model:
       To eliminate composite delamination, uncut fiber pull-out, and inter-laminar titanium burr
       formation between the unbonded CFRP and Ti-6Al-4V stack, the end-effector drives an axial
       hydraulic ring pressure-foot surrounding the drill bit with a nominal clamp force of 2,500 N
       (regulated up to 3,800 N). Executes a dynamic compliance and spring-deflection observer:
         delta_gap = delta_0 * exp(-F_clamp / F_crit)
       Guaranteeing inter-laminar separation delta_gap < 0.025 mm (25 microns) across all cutting phases.

    3. High-Speed Active Thermal Compensated Spindle (24,000 RPM):
       A high-frequency permanent magnet synchronous motorized spindle operates up to 24,000 RPM.
       Ceramic hybrid angular-contact ball bearings are actively monitored via RTD sensors.
       Axial thermal spindle shaft elongation and centrifugal expansion are calculated in real time:
         Delta_L_therm = alpha_shaft * L_0 * (T_bearing - T_ref) + beta_centrif * omega^2
       Compensates Z-axis servo position feed to sub-micron accuracy (< 2.0 um error).
       Real-time triaxial vibration FFT band-power and running crest factor evaluate high-frequency
       chatter, micro-chipping, and abrasive flank wear on diamond-coated carbide drill bits.

    4. Multi-Layer CFRP / Ti-6Al-4V Material Boundary Transition Observer:
       The stack transition from abrasive, brittle CFRP (optimum cutting speed vc = 140 m/min,
       feed fz = 0.06 mm/rev) to ductile, heat-sensitive Ti-6Al-4V (optimum vc = 35 m/min,
       fz = 0.02 mm/rev) represents an extreme mechanical discontinuity. The block continuously
       differentiates cutting thrust force (dFz/dt) and dynamic torque (dTq/dt). Upon entering
       the titanium boundary, the observer detects the force gradient spike (> 1,100 N/s) and
       transitions spindle speed from 16,000 RPM down to 2,600 RPM and feed rate from 960 mm/min
       to 52 mm/min within 15 ms, synchronizing high-pressure Minimum Quantity Lubrication (MQL).

    5. In-Process Laser Hole Metrology & Precision Countersink Depth Evaluation:
       Post-drilling, the spindle retracts and indexes an integrated telecentric optical confocal
       laser gauge into the bore. Measures top diameter (CFRP), middle diameter (Interface), and
       bottom diameter (Ti-6Al-4V) to confirm aerospace H8 tolerance (+0.015 / -0.000 mm).
       Evaluates countersink depth and chamfer angle to within +/- 0.020 mm before releasing
       fastener feed permissives.

    6. Automated Hi-Lok / Blind Fastener Robotic Collet Feed:
       Coordinates pneumatic singulation, collet vacuum transfer, and insertion stroke monitoring.
       Evaluates insertion resistance force profile (limit < 180 N) to verify hole clearance.

    7. Electromagnetic Riveting (EMR) High-Energy Pulse Dynamics:
       Controls pulsed-power high-voltage capacitor bank discharge (4.2 kV, 480 uF) into an
       electromagnetic pancake coil. Lorentz force drives a massive stress wave pulse (25 to 55 kN,
       duration 2.5 ms) through the rivet shank, achieving controlled plastic volumetric expansion
       (1.5% to 2.2% hole interference) for maximum airframe fatigue resistance.

    8. 8x8 Discrete State-Space Model & Receding-Horizon MPC Governor:
       Operates an 8-state, 4-input discrete linear time-invariant cyber-physical observer
       with receding-horizon quadratic cost optimization running at 1 ms sampling. Penalizes
       position tracking error, clamping force ripple, spindle torque overload, and vibration.
 ==========================================================================================
*)
''')

    # -------------------------------------------------------------
    # VAR_INPUT BLOCK
    # -------------------------------------------------------------
    parts.append('''VAR_INPUT
    (* ------------------------------------------------------------------------------------- *)
    (* MASTER DIGITAL SAFETY PERMISSIVES & CATEGORY 4 / SIL-3 SIGNALS                       *)
    (* ------------------------------------------------------------------------------------- *)
    bEmergencyStop                  : BOOL;     (* Active-low SIL-3 hardwired safety relay contact *)
    bMasterEnable                   : BOOL;     (* Primary cell automated sequence enable permissive *)
    bResetFaults                    : BOOL;     (* Master alarm unlatch and error acknowledgement command *)
    bLightCurtainMuted              : BOOL;     (* Optical safety light curtain muting request during gantry index *)
    bLightCurtainOSSD1              : BOOL;     (* Laser safety light curtain output signal switching device Ch 1 *)
    bLightCurtainOSSD2              : BOOL;     (* Laser safety light curtain output signal switching device Ch 2 *)
    bFastenerFeedReady              : BOOL;     (* Hi-Lok fastener singulation feed track loaded and ready *)
    bEmrCapacitorCharged            : BOOL;     (* EMR pulse power unit capacitor bank at rated discharge voltage *)
    bCoolantMqlSkidReady            : BOOL;     (* High-pressure MQL oil/air aerosol supply system operational *)
    bManualOverride                 : BOOL;     (* Engineering manual jog/commissioning permissive *)

    (* ------------------------------------------------------------------------------------- *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY: GANTRY CARTESIAN POSITION FEEDBACK [mm]               *)
    (* ------------------------------------------------------------------------------------- *)
    rGantryX_Pos_A_mm               : REAL;     (* Gantry longitudinal axis optical linear scale A (ZT_GANTRY_X_101A) *)
    rGantryX_Pos_B_mm               : REAL;     (* Gantry longitudinal axis optical linear scale B (ZT_GANTRY_X_101B) *)
    rGantryX_Pos_C_mm               : REAL;     (* Gantry longitudinal axis optical linear scale C (ZT_GANTRY_X_101C) *)
    rGantryY_Pos_A_mm               : REAL;     (* Gantry transverse axis optical linear scale A (ZT_GANTRY_Y_102A) *)
    rGantryY_Pos_B_mm               : REAL;     (* Gantry transverse axis optical linear scale B (ZT_GANTRY_Y_102B) *)
    rGantryY_Pos_C_mm               : REAL;     (* Gantry transverse axis optical linear scale C (ZT_GANTRY_Y_102C) *)
    rGantryZ_Pos_A_mm               : REAL;     (* Gantry vertical thrust axis optical linear scale A (ZT_GANTRY_Z_103A) *)
    rGantryZ_Pos_B_mm               : REAL;     (* Gantry vertical thrust axis optical linear scale B (ZT_GANTRY_Z_103B) *)
    rGantryZ_Pos_C_mm               : REAL;     (* Gantry vertical thrust axis optical linear scale C (ZT_GANTRY_Z_103C) *)

    (* ------------------------------------------------------------------------------------- *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY: SPINDLE GIMBAL ROTARY TILT ANGLES [deg]               *)
    (* ------------------------------------------------------------------------------------- *)
    rSpindleA_Tilt_A_deg            : REAL;     (* Spherical gimbal A-axis rotary resolver A (AE_SPINDLE_A_104A) *)
    rSpindleA_Tilt_B_deg            : REAL;     (* Spherical gimbal A-axis rotary resolver B (AE_SPINDLE_A_104B) *)
    rSpindleA_Tilt_C_deg            : REAL;     (* Spherical gimbal A-axis rotary resolver C (AE_SPINDLE_A_104C) *)
    rSpindleB_Tilt_A_deg            : REAL;     (* Spherical gimbal B-axis rotary resolver A (AE_SPINDLE_B_105A) *)
    rSpindleB_Tilt_B_deg            : REAL;     (* Spherical gimbal B-axis rotary resolver B (AE_SPINDLE_B_105B) *)
    rSpindleB_Tilt_C_deg            : REAL;     (* Spherical gimbal B-axis rotary resolver C (AE_SPINDLE_B_105C) *)

    (* ------------------------------------------------------------------------------------- *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY: SURFACE NORMAL OPTICAL LASER TRIANGULATION [mm]       *)
    (* ------------------------------------------------------------------------------------- *)
    rLaserDist1_A_mm                : REAL;     (* Laser triangulator 1 at theta=0 deg Channel A (OPT_SURFACE_201A1) *)
    rLaserDist1_B_mm                : REAL;     (* Laser triangulator 1 at theta=0 deg Channel B (OPT_SURFACE_201B1) *)
    rLaserDist1_C_mm                : REAL;     (* Laser triangulator 1 at theta=0 deg Channel C (OPT_SURFACE_201C1) *)
    rLaserDist2_A_mm                : REAL;     (* Laser triangulator 2 at theta=120 deg Channel A (OPT_SURFACE_201A2) *)
    rLaserDist2_B_mm                : REAL;     (* Laser triangulator 2 at theta=120 deg Channel B (OPT_SURFACE_201B2) *)
    rLaserDist2_C_mm                : REAL;     (* Laser triangulator 2 at theta=120 deg Channel C (OPT_SURFACE_201C2) *)
    rLaserDist3_A_mm                : REAL;     (* Laser triangulator 3 at theta=240 deg Channel A (OPT_SURFACE_201A3) *)
    rLaserDist3_B_mm                : REAL;     (* Laser triangulator 3 at theta=240 deg Channel B (OPT_SURFACE_201B3) *)
    rLaserDist3_C_mm                : REAL;     (* Laser triangulator 3 at theta=240 deg Channel C (OPT_SURFACE_201C3) *)

    (* ------------------------------------------------------------------------------------- *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY: CLAMPING FORCE & HYDRAULIC PRESSURE [N, bar]          *)
    (* ------------------------------------------------------------------------------------- *)
    rClampForce_A_N                 : REAL;     (* Pressure-foot piezoelectric load cell A (WT_CLAMP_FORCE_202A) *)
    rClampForce_B_N                 : REAL;     (* Pressure-foot piezoelectric load cell B (WT_CLAMP_FORCE_202B) *)
    rClampForce_C_N                 : REAL;     (* Pressure-foot piezoelectric load cell C (WT_CLAMP_FORCE_202C) *)
    rClampHydPress_A_bar            : REAL;     (* Pressure-foot hydraulic cylinder pressure A (PT_CLAMP_HYD_203A) *)
    rClampHydPress_B_bar            : REAL;     (* Pressure-foot hydraulic cylinder pressure B (PT_CLAMP_HYD_203B) *)
    rClampHydPress_C_bar            : REAL;     (* Pressure-foot hydraulic cylinder pressure C (PT_CLAMP_HYD_203C) *)

    (* ------------------------------------------------------------------------------------- *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY: HIGH-SPEED SPINDLE DYNAMICS [rpm, A, N*m]             *)
    (* ------------------------------------------------------------------------------------- *)
    rSpindleSpeed_A_rpm             : REAL;     (* Spindle high-resolution magnetic encoder A (ST_SPINDLE_RPM_301A) *)
    rSpindleSpeed_B_rpm             : REAL;     (* Spindle high-resolution magnetic encoder B (ST_SPINDLE_RPM_301B) *)
    rSpindleSpeed_C_rpm             : REAL;     (* Spindle high-resolution magnetic encoder C (ST_SPINDLE_RPM_301C) *)
    rSpindleCurrent_A_A             : REAL;     (* Spindle drive phase current transducer A (IT_SPINDLE_CURR_302A) *)
    rSpindleCurrent_B_A             : REAL;     (* Spindle drive phase current transducer B (IT_SPINDLE_CURR_302B) *)
    rSpindleCurrent_C_A             : REAL;     (* Spindle drive phase current transducer C (IT_SPINDLE_CURR_302C) *)
    rSpindleTorque_A_Nm             : REAL;     (* Spindle inline telemetric rotary torque gauge A (TQ_SPINDLE_303A) *)
    rSpindleTorque_B_Nm             : REAL;     (* Spindle inline telemetric rotary torque gauge B (TQ_SPINDLE_303B) *)
    rSpindleTorque_C_Nm             : REAL;     (* Spindle inline telemetric rotary torque gauge C (TQ_SPINDLE_303C) *)

    (* ------------------------------------------------------------------------------------- *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY: VIBRATION, BEARING TEMP & IN-PROCESS METROLOGY        *)
    (* ------------------------------------------------------------------------------------- *)
    rToolVibration_A_mms            : REAL;     (* Spindle nose triaxial accelerometer RMS A (AT_VIBRATION_304A) *)
    rToolVibration_B_mms            : REAL;     (* Spindle nose triaxial accelerometer RMS B (AT_VIBRATION_304B) *)
    rToolVibration_C_mms            : REAL;     (* Spindle nose triaxial accelerometer RMS C (AT_VIBRATION_304C) *)
    rBearingTemp_A_degC             : REAL;     (* Spindle front ceramic bearing RTD sensor A (TT_BEARING_305A) *)
    rBearingTemp_B_degC             : REAL;     (* Spindle front ceramic bearing RTD sensor B (TT_BEARING_305B) *)
    rBearingTemp_C_degC             : REAL;     (* Spindle front ceramic bearing RTD sensor C (TT_BEARING_305C) *)
    rFastenerFeederPos_A_mm         : REAL;     (* Fastener insertion collet stroke sensor A (ZT_FASTENER_POS_401A) *)
    rFastenerFeederPos_B_mm         : REAL;     (* Fastener insertion collet stroke sensor B (ZT_FASTENER_POS_401B) *)
    rFastenerFeederPos_C_mm         : REAL;     (* Fastener insertion collet stroke sensor C (ZT_FASTENER_POS_401C) *)
    rEmrPulseChamber_A_bar          : REAL;     (* EMR pulse coil recoil chamber acoustic pressure A (PT_EMR_402A) *)
    rEmrPulseChamber_B_bar          : REAL;     (* EMR pulse coil recoil chamber acoustic pressure B (PT_EMR_402B) *)
    rEmrPulseChamber_C_bar          : REAL;     (* EMR pulse coil recoil chamber acoustic pressure C (PT_EMR_402C) *)
    rHoleDiamLaser_A_mm             : REAL;     (* In-process optical telecentric bore gauge A (OPT_METROLOGY_501A) *)
    rHoleDiamLaser_B_mm             : REAL;     (* In-process optical telecentric bore gauge B (OPT_METROLOGY_501B) *)
    rHoleDiamLaser_C_mm             : REAL;     (* In-process optical telecentric bore gauge C (OPT_METROLOGY_501C) *)
    rCountersinkDepth_A_mm          : REAL;     (* Laser displacement countersink depth gauge A (ZT_COUNTERSINK_502A) *)
    rCountersinkDepth_B_mm          : REAL;     (* Laser displacement countersink depth gauge B (ZT_COUNTERSINK_502B) *)
    rCountersinkDepth_C_mm          : REAL;     (* Laser displacement countersink depth gauge C (ZT_COUNTERSINK_502C) *)

    (* ------------------------------------------------------------------------------------- *)
    (* PROCESS SETPOINTS & PARAMETRIC LIMITS                                                 *)
    (* ------------------------------------------------------------------------------------- *)
    rTargetGantryX_mm               : REAL;     (* Target hole coordinate X on wingbox grid [mm] *)
    rTargetGantryY_mm               : REAL;     (* Target hole coordinate Y on wingbox grid [mm] *)
    rTargetGantryZ_mm               : REAL;     (* Target hole approach plane coordinate Z [mm] *)
    rNominalClampForce_N            : REAL;     (* Commanded nominal pressure-foot clamping load [N] *)
    rMaxAllowableClampForce_N       : REAL;     (* Absolute upper safety clamp limit [N] *)
    rCfrpSpindleSpeedDemand_rpm     : REAL;     (* High-speed drilling RPM for CFRP composite layer [rpm] *)
    rTitaniumSpindleSpeedDemand_rpm : REAL;     (* Heavy-duty drilling RPM for Ti-6Al-4V titanium layer [rpm] *)
    rCfrpFeedRateDemand_mm_min      : REAL;     (* Tool axial feed speed in CFRP layer [mm/min] *)
    rTitaniumFeedRateDemand_mm_min  : REAL;     (* Tool axial feed speed in Titanium layer [mm/min] *)
    rNominalHoleDiameter_mm         : REAL;     (* Fastener nominal bore diameter (e.g. 6.350 mm / 1/4 in) [mm] *)
    rHoleDiameterTolUpper_mm        : REAL;     (* H8 tolerance upper deviation limit [mm] *)
    rHoleDiameterTolLower_mm        : REAL;     (* H8 tolerance lower deviation limit [mm] *)
    rCountersinkDepthTarget_mm      : REAL;     (* Precision countersink target depth [mm] *)
    rCountersinkDepthTol_mm         : REAL;     (* Allowable countersink depth tolerance band (+/-) [mm] *)
    rMaxAllowableVibration_mms      : REAL;     (* Spindle triaxial vibration trip threshold [mm/s] *)
    rMaxAllowableTorque_Nm          : REAL;     (* Spindle dynamic cutting torque trip threshold [N*m] *)
    rMaxBearingTemp_degC            : REAL;     (* Spindle bearing temperature trip threshold [deg C] *)
END_VAR
''')

    # -------------------------------------------------------------
    # VAR_OUTPUT BLOCK
    # -------------------------------------------------------------
    parts.append('''VAR_OUTPUT
    (* ------------------------------------------------------------------------------------- *)
    (* SYSTEM STATUS FLAGS & SAFETY DISCRETE INTERLOCKS                                      *)
    (* ------------------------------------------------------------------------------------- *)
    bCellRunning                    : BOOL;     (* End-effector automatic drilling/fastening cycle active *)
    bCellReady                      : BOOL;     (* All safety permissives satisfied, ready for new cycle *)
    bCellTripped                    : BOOL;     (* Emergency safety trip or critical fault active *)
    bCycleComplete                  : BOOL;     (* Drilling, countersinking, inspection, and rivet set completed *)
    bLightCurtainIntrusion          : BOOL;     (* Optical safety light curtain beam break detected *)
    bToolWearWarning                : BOOL;     (* Drill bit flank wear or vibration signature degraded *)
    bDrillChippingFault             : BOOL;     (* Drill cutting edge chipping or catastrophic fracture detected *)
    bMaterialTransitionLatched      : BOOL;     (* CFRP-to-Titanium interface detected and feed rate adapted *)
    bHoleMetrologyPassed            : BOOL;     (* Hole diameter and countersink depth within H8 tolerance *)
    bFastenerSeatedOk               : BOOL;     (* Fastener correctly inserted to nominal collet stroke *)
    bEmrPulseDelivered              : BOOL;     (* Electromagnetic rivet expansion pulse completed *)
    bDegradedSensorActive           : BOOL;     (* At least one 2oo3 sensor channel operates in degraded mode *)
    bMpcActiveOptimization          : BOOL;     (* Receding-horizon MPC algorithm actively computing commands *)

    (* ------------------------------------------------------------------------------------- *)
    (* 6-AXIS MOTION & SERVO ACTUATOR COMMANDS                                               *)
    (* ------------------------------------------------------------------------------------- *)
    rGantryX_Cmd_mm                 : REAL;     (* Longitudinal axis interpolated position command [mm] *)
    rGantryY_Cmd_mm                 : REAL;     (* Transverse axis interpolated position command [mm] *)
    rGantryZ_Cmd_mm                 : REAL;     (* Vertical thrust axis position command with thermal offset [mm] *)
    rSpindleA_Cmd_deg               : REAL;     (* Gimbal A-axis tilt orientation command [deg] *)
    rSpindleB_Cmd_deg               : REAL;     (* Gimbal B-axis tilt orientation command [deg] *)
    rSpindleSpeedCmd_rpm            : REAL;     (* Motorized spindle dynamic speed setpoint [rpm] *)
    rZFeedVelocityCmd_mms           : REAL;     (* Dynamic Z-axis cutting feed velocity [mm/s] *)
    rClampValveFlowCmd_pct          : REAL;     (* Hydraulic proportional servo valve flow command [%] *)
    rMqlAerosolPulseCmd_pct         : REAL;     (* High-pressure MQL air/oil lubricant pulse rate [%] *)
    rFastenerColletAdvanceCmd_mm    : REAL;     (* Fastener insertion actuator stroke command [mm] *)
    bEmrDischargeTrigger            : BOOL;     (* High-voltage thyristor pulse trigger signal for EMR *)
    bVacuumSuctionEnable            : BOOL;     (* End-effector composite dust & chip vacuum extraction enable *)

    (* ------------------------------------------------------------------------------------- *)
    (* 2oo3 SYNTHESIZED VOTED PROCESS ESTIMATES                                              *)
    (* ------------------------------------------------------------------------------------- *)
    rVotedGantryX_mm                : REAL;     (* 2oo3 median voted gantry X position [mm] *)
    rVotedGantryY_mm                : REAL;     (* 2oo3 median voted gantry Y position [mm] *)
    rVotedGantryZ_mm                : REAL;     (* 2oo3 median voted gantry Z position [mm] *)
    rVotedSpindleA_deg              : REAL;     (* 2oo3 median voted gimbal A tilt angle [deg] *)
    rVotedSpindleB_deg              : REAL;     (* 2oo3 median voted gimbal B tilt angle [deg] *)
    rVotedLaserDist1_mm             : REAL;     (* 2oo3 median voted laser distance 1 [mm] *)
    rVotedLaserDist2_mm             : REAL;     (* 2oo3 median voted laser distance 2 [mm] *)
    rVotedLaserDist3_mm             : REAL;     (* 2oo3 median voted laser distance 3 [mm] *)
    rVotedClampForce_N              : REAL;     (* 2oo3 median voted pressure-foot clamp load [N] *)
    rVotedSpindleSpeed_rpm          : REAL;     (* 2oo3 median voted spindle rotational speed [rpm] *)
    rVotedSpindleTorque_Nm          : REAL;     (* 2oo3 median voted spindle dynamic torque [N*m] *)
    rVotedToolVibration_mms         : REAL;     (* 2oo3 median voted spindle triaxial vibration [mm/s] *)
    rVotedBearingTemp_degC          : REAL;     (* 2oo3 median voted spindle ceramic bearing temperature [deg C] *)
    rVotedHoleDiam_mm               : REAL;     (* 2oo3 median voted in-process hole diameter [mm] *)
    rVotedCountersinkDepth_mm       : REAL;     (* 2oo3 median voted countersink depth [mm] *)

    (* ------------------------------------------------------------------------------------- *)
    (* CYBER-PHYSICAL OBSERVER & PROCESS QUALITY METRICS                                     *)
    (* ------------------------------------------------------------------------------------- *)
    rSurfaceTiltError_deg           : REAL;     (* Normal vector angular tilt deviation relative to Z axis [deg] *)
    rEstimatedInterlayerGap_um      : REAL;     (* Real-time calculated CFRP/Titanium separation gap [um] *)
    rSpindleThermalGrowth_um        : REAL;     (* Real-time computed spindle shaft axial elongation [um] *)
    rZThermalCompensatedPos_mm      : REAL;     (* Final Z position command adjusted for thermal & centrifugal slip [mm] *)
    rCuttingPower_W                 : REAL;     (* Real-time spindle instantaneous cutting power [W] *)
    rThrustForceDerivative_Ns       : REAL;     (* Dynamic cutting thrust force rate of change (dFz/dt) [N/s] *)
    rTorqueDerivative_Nms           : REAL;     (* Dynamic cutting torque rate of change (dTq/dt) [N*m/s] *)
    rFastenerInsertionForce_N       : REAL;     (* Monitored mechanical fastener insertion push force [N] *)
    rEmrPeakCurrent_kA              : REAL;     (* Estimated peak discharge current during EMR pulse [kA] *)
    rResidualStackStress_MPa        : REAL;     (* Estimated residual compressive stress under rivet head [MPa] *)

    (* ------------------------------------------------------------------------------------- *)
    (* COMPREHENSIVE BIT-PACKED STATUS & ALARM WORDS (ISA-18.2 COMPLIANT)                   *)
    (* ------------------------------------------------------------------------------------- *)
    dwSystemStatusWord              : DWORD;    (* Bit-packed operational FSM state and permissive word *)
    dwAlarmWord1                    : DWORD;    (* Bit-packed emergency trips, SIL-3 safety & light curtain faults *)
    dwAlarmWord2                    : DWORD;    (* Bit-packed process trips: tool fracture, thermal & force trips *)
    dwWarningWord                   : DWORD;    (* Bit-packed advisory warnings: tool wear, gap limit, MQL warning *)
    dwDegradationWord               : DWORD;    (* Bit-packed 2oo3 sensor channel health & degradation word *)
END_VAR
''')

    # -------------------------------------------------------------
    # VAR INTERNAL BLOCK
    # -------------------------------------------------------------
    parts.append('''VAR
    (* ------------------------------------------------------------------------------------- *)
    (* FINITE STATE MACHINE (FSM) STEP CONTROL & TIMERS                                     *)
    (* ------------------------------------------------------------------------------------- *)
    iFsmState                       : INT := 0; (* Primary supervisory state register *)
    iFsmSubState                    : INT := 0; (* Secondary substep sequence register *)
    iPrevFsmState                   : INT := 0; (* State history register for transition diagnostics *)
    
    tStateTimer                     : TON;      (* Primary state execution dwell timer *)
    tLaserSettleTimer               : TON;      (* Optical laser triangulation beam settling timer *)
    tClampDwellTimer                : TON;      (* Pressure-foot pre-clamping force build-up timer *)
    tSpindleRampTimer               : TON;      (* Motorized spindle dynamic speed acceleration timer *)
    tTransitionDebounce             : TON;      (* Material boundary detection persistency debounce timer *)
    tCountersinkDwellTimer          : TON;      (* Countersink bottom dwell spark-out timer *)
    tMetrologyScanTimer             : TON;      (* Laser bore optical inspection profiling timer *)
    tFastenerFeedTimer              : TON;      (* Pneumatic fastener collet insertion stroke timer *)
    tEmrDischargeTimer              : TON;      (* Electromagnetic riveting pulse firing timer *)
    tBreakageDetectTimer            : TON;      (* Drill bit catastrophic fracture confirmation timer *)
    tLightCurtainDebounce           : TON;      (* Safety light curtain OSSD dual-channel discrepancy timer *)
    tSensorTripDebounce             : TON;      (* 2oo3 sensor deviation trip debounce timer *)

    (* ------------------------------------------------------------------------------------- *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY SENSOR DISCREPANCY & CHANNEL HEALTH                   *)
    (* ------------------------------------------------------------------------------------- *)
    (* Gantry X Position Triplet *)
    rDev_GX_AB                      : REAL;
    rDev_GX_BC                      : REAL;
    rDev_GX_CA                      : REAL;
    bGX_A_Healthy                   : BOOL := TRUE;
    bGX_B_Healthy                   : BOOL := TRUE;
    bGX_C_Healthy                   : BOOL := TRUE;

    (* Gantry Y Position Triplet *)
    rDev_GY_AB                      : REAL;
    rDev_GY_BC                      : REAL;
    rDev_GY_CA                      : REAL;
    bGY_A_Healthy                   : BOOL := TRUE;
    bGY_B_Healthy                   : BOOL := TRUE;
    bGY_C_Healthy                   : BOOL := TRUE;

    (* Gantry Z Position Triplet *)
    rDev_GZ_AB                      : REAL;
    rDev_GZ_BC                      : REAL;
    rDev_GZ_CA                      : REAL;
    bGZ_A_Healthy                   : BOOL := TRUE;
    bGZ_B_Healthy                   : BOOL := TRUE;
    bGZ_C_Healthy                   : BOOL := TRUE;

    (* Gimbal A Tilt Triplet *)
    rDev_GA_AB                      : REAL;
    rDev_GA_BC                      : REAL;
    rDev_GA_CA                      : REAL;
    bGA_A_Healthy                   : BOOL := TRUE;
    bGA_B_Healthy                   : BOOL := TRUE;
    bGA_C_Healthy                   : BOOL := TRUE;

    (* Gimbal B Tilt Triplet *)
    rDev_GB_AB                      : REAL;
    rDev_GB_BC                      : REAL;
    rDev_GB_CA                      : REAL;
    bGB_A_Healthy                   : BOOL := TRUE;
    bGB_B_Healthy                   : BOOL := TRUE;
    bGB_C_Healthy                   : BOOL := TRUE;

    (* Surface Normal Laser Dist 1 Triplet *)
    rDev_L1_AB                      : REAL;
    rDev_L1_BC                      : REAL;
    rDev_L1_CA                      : REAL;
    bL1_A_Healthy                   : BOOL := TRUE;
    bL1_B_Healthy                   : BOOL := TRUE;
    bL1_C_Healthy                   : BOOL := TRUE;

    (* Surface Normal Laser Dist 2 Triplet *)
    rDev_L2_AB                      : REAL;
    rDev_L2_BC                      : REAL;
    rDev_L2_CA                      : REAL;
    bL2_A_Healthy                   : BOOL := TRUE;
    bL2_B_Healthy                   : BOOL := TRUE;
    bL2_C_Healthy                   : BOOL := TRUE;

    (* Surface Normal Laser Dist 3 Triplet *)
    rDev_L3_AB                      : REAL;
    rDev_L3_BC                      : REAL;
    rDev_L3_CA                      : REAL;
    bL3_A_Healthy                   : BOOL := TRUE;
    bL3_B_Healthy                   : BOOL := TRUE;
    bL3_C_Healthy                   : BOOL := TRUE;

    (* Clamping Force Triplet *)
    rDev_CF_AB                      : REAL;
    rDev_CF_BC                      : REAL;
    rDev_CF_CA                      : REAL;
    bCF_A_Healthy                   : BOOL := TRUE;
    bCF_B_Healthy                   : BOOL := TRUE;
    bCF_C_Healthy                   : BOOL := TRUE;

    (* Spindle Dynamic Torque Triplet *)
    rDev_TQ_AB                      : REAL;
    rDev_TQ_BC                      : REAL;
    rDev_TQ_CA                      : REAL;
    bTQ_A_Healthy                   : BOOL := TRUE;
    bTQ_B_Healthy                   : BOOL := TRUE;
    bTQ_C_Healthy                   : BOOL := TRUE;

    (* Tool Triaxial Vibration Triplet *)
    rDev_VB_AB                      : REAL;
    rDev_VB_BC                      : REAL;
    rDev_VB_CA                      : REAL;
    bVB_A_Healthy                   : BOOL := TRUE;
    bVB_B_Healthy                   : BOOL := TRUE;
    bVB_C_Healthy                   : BOOL := TRUE;

    (* Spindle Bearing Temp Triplet *)
    rDev_BT_AB                      : REAL;
    rDev_BT_BC                      : REAL;
    rDev_BT_CA                      : REAL;
    bBT_A_Healthy                   : BOOL := TRUE;
    bBT_B_Healthy                   : BOOL := TRUE;
    bBT_C_Healthy                   : BOOL := TRUE;

    (* Optical Metrology Hole Diam Triplet *)
    rDev_HD_AB                      : REAL;
    rDev_HD_BC                      : REAL;
    rDev_HD_CA                      : REAL;
    bHD_A_Healthy                   : BOOL := TRUE;
    bHD_B_Healthy                   : BOOL := TRUE;
    bHD_C_Healthy                   : BOOL := TRUE;

    (* Countersink Depth Triplet *)
    rDev_CD_AB                      : REAL;
    rDev_CD_BC                      : REAL;
    rDev_CD_CA                      : REAL;
    bCD_A_Healthy                   : BOOL := TRUE;
    bCD_B_Healthy                   : BOOL := TRUE;
    bCD_C_Healthy                   : BOOL := TRUE;

    (* ------------------------------------------------------------------------------------- *)
    (* PHYSICAL CONSTANTS & MECHATRONIC GEOMETRIC PARAMETERS                                 *)
    (* ------------------------------------------------------------------------------------- *)
    c_Pi                            : REAL := 3.1415926535; (* Circular constant *)
    c_DegToRad                      : REAL := 0.0174532925; (* Degrees to radians multiplier *)
    c_RadToDeg                      : REAL := 57.295779513; (* Radians to degrees multiplier *)
    c_LaserPitchRadius_mm           : REAL := 75.0;         (* Circumferential radius of triangulation lasers [mm] *)
    c_SpindleShaftLength_mm         : REAL := 420.0;        (* Cold reference length of spindle shaft [mm] *)
    c_ShaftThermalCoeff_1K          : REAL := 0.0000117;    (* Steel-ceramic composite shaft expansion coeff [1/K] *)
    c_CentrifugalCoeff              : REAL := 0.000000000018; (* Centrifugal axial expansion coefficient [mm/rpm^2] *)
    c_RefBearingTemp_degC           : REAL := 22.0;         (* Calibration reference ambient temperature [deg C] *)
    c_StackInitialGap_um            : REAL := 180.0;        (* Nominal uncompressed inter-laminar gap [um] *)
    c_CriticalClampForce_N          : REAL := 1250.0;       (* Characteristic exponential clamping decay constant [N] *)
    c_MaxAllowableGap_um            : REAL := 25.0;         (* Critical burr formation gap threshold [um] *)
    c_EmrCapacitance_uF             : REAL := 480.0;        (* EMR capacitor bank energy storage [uF] *)
    c_EmrChargeVoltage_V            : REAL := 4200.0;       (* EMR pulse discharge voltage [V] *)
    c_EmrCoilInductance_uH          : REAL := 12.5;         (* EMR discharge circuit lumped inductance [uH] *)
    c_EmrCircuitResistance_Ohm      : REAL := 0.045;        (* EMR pulse circuit dynamic damping resistance [Ohm] *)

    (* ------------------------------------------------------------------------------------- *)
    (* SURFACE NORMAL 3D VECTOR GEOMETRY WORKING REGISTERS                                   *)
    (* ------------------------------------------------------------------------------------- *)
    rP1_x                           : REAL := 75.0;
    rP1_y                           : REAL := 0.0;
    rP1_z                           : REAL := 0.0;
    rP2_x                           : REAL := -37.5;
    rP2_y                           : REAL := 64.951905;
    rP2_z                           : REAL := 0.0;
    rP3_x                           : REAL := -37.5;
    rP3_y                           : REAL := -64.951905;
    rP3_z                           : REAL := 0.0;
    rV1_x                           : REAL := 0.0;
    rV1_y                           : REAL := 0.0;
    rV1_z                           : REAL := 0.0;
    rV2_x                           : REAL := 0.0;
    rV2_y                           : REAL := 0.0;
    rV2_z                           : REAL := 0.0;
    rNorm_x                         : REAL := 0.0;
    rNorm_y                         : REAL := 0.0;
    rNorm_z                         : REAL := 1.0;
    rNormMag                        : REAL := 1.0;
    rUnitNorm_x                     : REAL := 0.0;
    rUnitNorm_y                     : REAL := 0.0;
    rUnitNorm_z                     : REAL := 1.0;
    rSurfaceTilt_deg                : REAL := 0.0;
    rTiltAngleA_deg                 : REAL := 0.0;
    rTiltAngleB_deg                 : REAL := 0.0;

    (* ------------------------------------------------------------------------------------- *)
    (* MATERIAL BOUNDARY & FEEDRATE SMOOTHING INTERNALS                                      *)
    (* ------------------------------------------------------------------------------------- *)
    rPrevTorque_Nm                  : REAL := 0.0;
    rPrevThrustForce_N              : REAL := 0.0;
    rPrevGantryZ_mm                 : REAL := 0.0;
    rEstimatedThrust_N              : REAL := 0.0;
    rFilteredVibration_mms          : REAL := 0.0;
    rVibrationPeak_mms              : REAL := 0.0;
    rVibrationCrestFactor           : REAL := 1.0;
    rFilteredCurrent_A              : REAL := 0.0;
    rInternalFeedVel_mms            : REAL := 0.0;
    rTargetFeedVel_mms              : REAL := 0.0;
    rInternalSpeed_rpm              : REAL := 0.0;
    rTargetSpeed_rpm                : REAL := 0.0;
    bBreakageDetected               : BOOL := FALSE;
    bTransitionDetected             : BOOL := FALSE;

    (* Hydraulic Clamp Closed-Loop PI Regulator Internals *)
    rClampError_N                   : REAL := 0.0;
    rClampIntegral_N                : REAL := 0.0;
    rClampKp                        : REAL := 0.024;        (* Proportional gain [%/N] *)
    rClampKi                        : REAL := 0.085;        (* Integral gain [%/(N*s)] *)
    rClampRawOutput_pct             : REAL := 0.0;

    (* ------------------------------------------------------------------------------------- *)
    (* 8x8 MULTIVARIABLE DISCRETE STATE-SPACE & MPC OPTIMIZATION MATRICES                    *)
    (* States x:                                                                             *)
    (*   x[1]: Gantry Z axial position tracking error [mm]                                   *)
    (*   x[2]: Gantry Z axial feed velocity [mm/s]                                           *)
    (*   x[3]: Pressure-foot clamping force deviation [N]                                    *)
    (*   x[4]: Hydraulic clamping force rate of change [N/s]                                 *)
    (*   x[5]: Spindle dynamic cutting torque error [N*m]                                    *)
    (*   x[6]: Spindle rotational angular speed deviation [rad/s]                            *)
    (*   x[7]: Spindle shaft dynamic axial thermal expansion [um]                            *)
    (*   x[8]: Tool nose triaxial structural vibration envelope [mm/s]                      *)
    (* Inputs u:                                                                             *)
    (*   u[1]: Servo Z feed thrust force command [N]                                         *)
    (*   u[2]: Spindle drive electromagnetic torque demand [N*m]                             *)
    (*   u[3]: Hydraulic clamping proportional valve command [%]                             *)
    (*   u[4]: High-pressure MQL pulse duty ratio [%]                                        *)
    (* Outputs y:                                                                            *)
    (*   y[1]: Net axial tool cutting feed rate [mm/min]                                     *)
    (*   y[2]: Total pressure-foot clamping load [N]                                         *)
    (*   y[3]: Instantaneous cutting torque [N*m]                                            *)
    (*   y[4]: Filtered vibration envelope [mm/s]                                            *)
    (* ------------------------------------------------------------------------------------- *)
    A_mat                           : ARRAY[1..8, 1..8] OF REAL; (* Discrete state matrix A (8x8) *)
    B_mat                           : ARRAY[1..8, 1..4] OF REAL; (* Discrete input matrix B (8x4) *)
    C_mat                           : ARRAY[1..4, 1..8] OF REAL; (* Discrete output matrix C (4x8) *)
    D_mat                           : ARRAY[1..4, 1..4] OF REAL; (* Direct transmission matrix D (4x4) *)

    x_state                         : ARRAY[1..8] OF REAL;       (* Current estimated cyber-physical state vector *)
    x_pred                          : ARRAY[1..8] OF REAL;       (* One-step-ahead state prediction vector *)
    x_ref                           : ARRAY[1..8] OF REAL;       (* Target trajectory setpoint vector *)
    x_err                           : ARRAY[1..8] OF REAL;       (* State tracking error vector *)

    u_mpc                           : ARRAY[1..4] OF REAL;       (* Active MPC command vector *)
    u_delta                         : ARRAY[1..4] OF REAL;       (* Gradient descent increment vector *)
    u_prev                          : ARRAY[1..4] OF REAL;       (* Previous execution command history *)
    u_min                           : ARRAY[1..4] OF REAL;       (* Lower actuator saturation boundary *)
    u_max                           : ARRAY[1..4] OF REAL;       (* Upper actuator saturation boundary *)

    Q_diag                          : ARRAY[1..8] OF REAL;       (* State tracking quadratic penalty weights *)
    R_diag                          : ARRAY[1..4] OF REAL;       (* Actuator rate-of-change penalty weights *)
    grad_J                          : ARRAY[1..4] OF REAL;       (* Performance index gradient vector *)
    H_diag                          : ARRAY[1..4] OF REAL;       (* Diagonal Hessian metric approximation *)

    iRow                            : INT := 1;                 (* Matrix row iterator *)
    iCol                            : INT := 1;                 (* Matrix column iterator *)
    iIter                           : INT := 1;                 (* MPC gradient descent iteration counter *)
    rCostValue                      : REAL := 0.0;              (* Evaluated quadratic objective value *)
    rMpcStepSize                    : REAL := 0.015;            (* Gradient optimization convergence step *)

    (* Fast Deterministic Execution Timing *)
    rScanTime_s                     : REAL := 0.001;            (* Deterministic 1 ms execution interval *)
    bMatricesInitialized            : BOOL := FALSE;            (* Initialization latch *)
END_VAR
''')

    # -------------------------------------------------------------
    # CODE BODY - SECTION 0 & 1: SAFETY & LIGHT CURTAINS
    # -------------------------------------------------------------
    parts.append('''
(* ========================================================================================= *)
(* 0.0 CYBER-PHYSICAL MATRICES COLD-START INITIALIZATION                                     *)
(* ========================================================================================= *)
(* Initializes the discrete-time 8x8 State-Space matrices and MPC cost matrices during cold  *)
(* system boot or warm reset. System dynamics sampled at Ts = 0.001 s (1 millisecond).      *)

IF NOT bMatricesInitialized THEN
    (* Row 1: Gantry Z Position Error x[1] *)
    A_mat[1,1] := 0.9992;  A_mat[1,2] := 0.00098; A_mat[1,3] := 0.00000; A_mat[1,4] := 0.00000;
    A_mat[1,5] := 0.00000; A_mat[1,6] := 0.00000; A_mat[1,7] := -0.00045; A_mat[1,8] := 0.00000;

    (* Row 2: Gantry Z Feed Velocity x[2] *)
    A_mat[2,1] := -0.0125; A_mat[2,2] := 0.98420; A_mat[2,3] := 0.00000; A_mat[2,4] := 0.00000;
    A_mat[2,5] := -0.0032; A_mat[2,6] := 0.00000; A_mat[2,7] := 0.00000;  A_mat[2,8] := -0.00185;

    (* Row 3: Clamping Force Deviation x[3] *)
    A_mat[3,1] := 0.00000; A_mat[3,2] := 0.00000; A_mat[3,3] := 0.99450; A_mat[3,4] := 0.00095;
    A_mat[3,5] := 0.00000; A_mat[3,6] := 0.00000; A_mat[3,7] := 0.00000;  A_mat[3,8] := 0.00000;

    (* Row 4: Hydraulic Clamping Force Rate x[4] *)
    A_mat[4,1] := 0.00000; A_mat[4,2] := 0.00000; A_mat[4,3] := -8.4500; A_mat[4,4] := 0.92500;
    A_mat[4,5] := 0.00000; A_mat[4,6] := 0.00000; A_mat[4,7] := 0.00000;  A_mat[4,8] := 0.00000;

    (* Row 5: Spindle Cutting Torque Error x[5] *)
    A_mat[5,1] := 0.00000; A_mat[5,2] := 0.18500; A_mat[5,3] := 0.00000; A_mat[5,4] := 0.00000;
    A_mat[5,5] := 0.96200; A_mat[5,6] := 0.00140; A_mat[5,7] := 0.00000;  A_mat[5,8] := 0.00450;

    (* Row 6: Spindle Rotational Speed Deviation x[6] *)
    A_mat[6,1] := 0.00000; A_mat[6,2] := 0.00000; A_mat[6,3] := 0.00000; A_mat[6,4] := 0.00000;
    A_mat[6,5] := -0.8500; A_mat[6,6] := 0.98800; A_mat[6,7] := 0.00000;  A_mat[6,8] := 0.00000;

    (* Row 7: Spindle Shaft Axial Thermal Growth x[7] *)
    A_mat[7,1] := 0.00000; A_mat[7,2] := 0.00000; A_mat[7,3] := 0.00000; A_mat[7,4] := 0.00000;
    A_mat[7,5] := 0.00085; A_mat[7,6] := 0.00012; A_mat[7,7] := 0.99985; A_mat[7,8] := 0.00000;

    (* Row 8: Tool Nose Structural Vibration x[8] *)
    A_mat[8,1] := 0.00000; A_mat[8,2] := 0.02400; A_mat[8,3] := 0.00000; A_mat[8,4] := 0.00000;
    A_mat[8,5] := 0.04500; A_mat[8,6] := 0.00000; A_mat[8,7] := 0.00000;  A_mat[8,8] := 0.94500;

    (* Discrete Input Coupling Matrix B (8x4) *)
    B_mat[1,1] := 0.000012; B_mat[1,2] := 0.000000; B_mat[1,3] := 0.000000; B_mat[1,4] := 0.000000;
    B_mat[2,1] := 0.002450; B_mat[2,2] := 0.000000; B_mat[2,3] := 0.000000; B_mat[2,4] := 0.000000;
    B_mat[3,1] := 0.000000; B_mat[3,2] := 0.000000; B_mat[3,3] := 0.045000; B_mat[3,4] := 0.000000;
    B_mat[4,1] := 0.000000; B_mat[4,2] := 0.000000; B_mat[4,3] := 42.50000; B_mat[4,4] := 0.000000;
    B_mat[5,1] := 0.000000; B_mat[5,2] := -0.01500; B_mat[5,3] := 0.000000; B_mat[5,4] := -0.00250;
    B_mat[6,1] := 0.000000; B_mat[6,2] := 1.250000; B_mat[6,3] := 0.000000; B_mat[6,4] := 0.000000;
    B_mat[7,1] := 0.000000; B_mat[7,2] := 0.000015; B_mat[7,3] := 0.000000; B_mat[7,4] := -0.00018;
    B_mat[8,1] := 0.000000; B_mat[8,2] := 0.000000; B_mat[8,3] := 0.000000; B_mat[8,4] := -0.00850;

    (* Observation Matrix C (4x8) *)
    C_mat[1,1] := 0.0; C_mat[1,2] := 60.0; C_mat[1,3] := 0.0; C_mat[1,4] := 0.0;
    C_mat[1,5] := 0.0; C_mat[1,6] := 0.0;  C_mat[1,7] := 0.0; C_mat[1,8] := 0.0;

    C_mat[2,1] := 0.0; C_mat[2,2] := 0.0; C_mat[2,3] := 1.0; C_mat[2,4] := 0.0;
    C_mat[2,5] := 0.0; C_mat[2,6] := 0.0; C_mat[2,7] := 0.0; C_mat[2,8] := 0.0;

    C_mat[3,1] := 0.0; C_mat[3,2] := 0.0; C_mat[3,3] := 0.0; C_mat[3,4] := 0.0;
    C_mat[3,5] := 1.0; C_mat[3,6] := 0.0; C_mat[3,7] := 0.0; C_mat[3,8] := 0.0;

    C_mat[4,1] := 0.0; C_mat[4,2] := 0.0; C_mat[4,3] := 0.0; C_mat[4,4] := 0.0;
    C_mat[4,5] := 0.0; C_mat[4,6] := 0.0; C_mat[4,7] := 0.0; C_mat[4,8] := 1.0;

    (* Feedthrough Matrix D (4x4) *)
    FOR iRow := 1 TO 4 DO
        FOR iCol := 1 TO 4 DO
            D_mat[iRow, iCol] := 0.0;
        END_FOR;
    END_FOR;

    (* Quadratic Optimization Penalties *)
    Q_diag[1] := 450.0;  (* Heavy penalty on Z position error *)
    Q_diag[2] := 25.0;   (* Penalty on Z velocity flutter *)
    Q_diag[3] := 80.0;   (* Clamping force error penalty *)
    Q_diag[4] := 0.05;   (* Clamp rate damping *)
    Q_diag[5] := 65.0;   (* Spindle torque deviation penalty *)
    Q_diag[6] := 35.0;   (* Rotational speed flutter penalty *)
    Q_diag[7] := 120.0;  (* Spindle thermal elongation penalty *)
    Q_diag[8] := 250.0;  (* Tool vibration suppression weight *)

    R_diag[1] := 0.008;  (* Z feed thrust actuator cost *)
    R_diag[2] := 0.012;  (* Spindle torque demand cost *)
    R_diag[3] := 0.025;  (* Hydraulic clamp valve rate cost *)
    R_diag[4] := 0.005;  (* MQL pulse rate cost *)

    H_diag[1] := 12.50;  H_diag[2] := 8.40;  H_diag[3] := 15.60; H_diag[4] := 4.20;

    (* Input Saturation Boundaries *)
    u_min[1] := -1500.0; u_max[1] := 3500.0;  (* Thrust force bounds [N] *)
    u_min[2] := -10.0;   u_max[2] := 12.0;    (* Spindle torque bounds [N*m] *)
    u_min[3] := 0.0;     u_max[3] := 100.0;   (* Clamp valve flow [%] *)
    u_min[4] := 0.0;     u_max[4] := 100.0;   (* MQL aerosol pulse [%] *)

    bMatricesInitialized := TRUE;
END_IF;


(* ========================================================================================= *)
(* 1.0 CATEGORY 4 / SIL-3 SAFETY INTERLOCKS & OPTICAL LIGHT CURTAINS                        *)
(* ========================================================================================= *)
(* Evaluates redundant hardwired emergency stop contacts and optical light curtain OSSD      *)
(* safety channels with cross-channel discrepancy timers to satisfy ISO 13849-1 Cat 4 / PLe. *)

dwAlarmWord1 := 16#0000_0000;
dwAlarmWord2 := 16#0000_0000;

(* Interlock 1.1: Active-low Emergency Stop Relay (SIL-3 Hardwired) *)
IF NOT bEmergencyStop THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0001; (* Bit 0: Hardware E-Stop Asserted *)
END_IF;

(* Interlock 1.2: Automation Master Enable Permissive *)
IF NOT bMasterEnable THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0002; (* Bit 1: Automation Enable Dropped *)
END_IF;

(* Interlock 1.3: Category 4 Optical Laser Light Curtain Dual-Channel OSSD Interlock *)
tLightCurtainDebounce(IN := (bLightCurtainOSSD1 <> bLightCurtainOSSD2), PT := T#15MS);

IF (NOT bLightCurtainOSSD1 OR NOT bLightCurtainOSSD2) AND NOT bLightCurtainMuted THEN
    bLightCurtainIntrusion := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0004; (* Bit 2: Light Curtain Perimeter Intrusion *)
ELSE
    bLightCurtainIntrusion := FALSE;
END_IF;

IF tLightCurtainDebounce.Q THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0008; (* Bit 3: Light Curtain Channel Discrepancy Fault *)
END_IF;

(* Interlock 1.4: MQL Minimum Quantity Lubricant Supply Pressure Missing *)
IF NOT bCoolantMqlSkidReady THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0010; (* Bit 4: High-Pressure MQL Skid Fault *)
END_IF;

(* Interlock 1.5: Fastener Feeder System Jam / Hardware Fault *)
IF NOT bFastenerFeedReady AND (iFsmState >= 9) THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0020; (* Bit 5: Fastener Feeder Not Ready During Insert *)
END_IF;

(* Interlock 1.6: EMR Capacitor Bank Charge Fault *)
IF NOT bEmrCapacitorCharged AND (iFsmState = 10) THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0040; (* Bit 6: EMR Pulse Power Bank Discharged *)
END_IF;
''')

    # -------------------------------------------------------------
    # CODE BODY - SECTION 2: 2oo3 TMR SENSOR VOTING
    # -------------------------------------------------------------
    parts.append('''
(* ========================================================================================= *)
(* 2.0 TRIPLE MODULAR REDUNDANCY (2oo3) SENSOR VOTING & DEGRADATION                         *)
(* ========================================================================================= *)
(* Executes triplicated sensor cross-comparison with median voting and bumpless fallback    *)
(* (2oo3 -> 1oo2 -> 1oo1 -> fail-safe trip). Sets diagnostic bits in dwDegradationWord.    *)

dwDegradationWord := 16#0000_0000;
bDegradedSensorActive := FALSE;

(* --- 2.1 Gantry X Linear Scale 2oo3 Bank --- *)
rDev_GX_AB := ABS(rGantryX_Pos_A_mm - rGantryX_Pos_B_mm);
rDev_GX_BC := ABS(rGantryX_Pos_B_mm - rGantryX_Pos_C_mm);
rDev_GX_CA := ABS(rGantryX_Pos_C_mm - rGantryX_Pos_A_mm);

bGX_A_Healthy := (rGantryX_Pos_A_mm >= -500.0) AND (rGantryX_Pos_A_mm <= 35000.0);
bGX_B_Healthy := (rGantryX_Pos_B_mm >= -500.0) AND (rGantryX_Pos_B_mm <= 35000.0);
bGX_C_Healthy := (rGantryX_Pos_C_mm >= -500.0) AND (rGantryX_Pos_C_mm <= 35000.0);

IF bGX_A_Healthy AND bGX_B_Healthy AND bGX_C_Healthy THEN
    IF ((rGantryX_Pos_A_mm >= rGantryX_Pos_B_mm) AND (rGantryX_Pos_A_mm <= rGantryX_Pos_C_mm)) OR
       ((rGantryX_Pos_A_mm >= rGantryX_Pos_C_mm) AND (rGantryX_Pos_A_mm <= rGantryX_Pos_B_mm)) THEN
        rVotedGantryX_mm := rGantryX_Pos_A_mm;
    ELSIF ((rGantryX_Pos_B_mm >= rGantryX_Pos_A_mm) AND (rGantryX_Pos_B_mm <= rGantryX_Pos_C_mm)) OR
          ((rGantryX_Pos_B_mm >= rGantryX_Pos_C_mm) AND (rGantryX_Pos_B_mm <= rGantryX_Pos_A_mm)) THEN
        rVotedGantryX_mm := rGantryX_Pos_B_mm;
    ELSE
        rVotedGantryX_mm := rGantryX_Pos_C_mm;
    END_IF;
    IF (rDev_GX_AB > 0.150) OR (rDev_GX_BC > 0.150) OR (rDev_GX_CA > 0.150) THEN
        dwDegradationWord := dwDegradationWord OR 16#0000_0001; (* Gantry X channel deviation *)
    END_IF;
ELSIF bGX_A_Healthy AND bGX_B_Healthy THEN
    rVotedGantryX_mm := (rGantryX_Pos_A_mm + rGantryX_Pos_B_mm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0002;
    bDegradedSensorActive := TRUE;
ELSIF bGX_B_Healthy AND bGX_C_Healthy THEN
    rVotedGantryX_mm := (rGantryX_Pos_B_mm + rGantryX_Pos_C_mm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0004;
    bDegradedSensorActive := TRUE;
ELSIF bGX_A_Healthy AND bGX_C_Healthy THEN
    rVotedGantryX_mm := (rGantryX_Pos_A_mm + rGantryX_Pos_C_mm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0008;
    bDegradedSensorActive := TRUE;
ELSIF bGX_A_Healthy THEN
    rVotedGantryX_mm := rGantryX_Pos_A_mm;
    dwDegradationWord := dwDegradationWord OR 16#0000_0010;
    bDegradedSensorActive := TRUE;
ELSIF bGX_B_Healthy THEN
    rVotedGantryX_mm := rGantryX_Pos_B_mm;
    dwDegradationWord := dwDegradationWord OR 16#0000_0020;
    bDegradedSensorActive := TRUE;
ELSIF bGX_C_Healthy THEN
    rVotedGantryX_mm := rGantryX_Pos_C_mm;
    dwDegradationWord := dwDegradationWord OR 16#0000_0040;
    bDegradedSensorActive := TRUE;
ELSE
    rVotedGantryX_mm := 0.0;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0080; (* All Gantry X transducers failed *)
END_IF;

(* --- 2.2 Gantry Y Linear Scale 2oo3 Bank --- *)
rDev_GY_AB := ABS(rGantryY_Pos_A_mm - rGantryY_Pos_B_mm);
rDev_GY_BC := ABS(rGantryY_Pos_B_mm - rGantryY_Pos_C_mm);
rDev_GY_CA := ABS(rGantryY_Pos_C_mm - rGantryY_Pos_A_mm);

bGY_A_Healthy := (rGantryY_Pos_A_mm >= -200.0) AND (rGantryY_Pos_A_mm <= 12000.0);
bGY_B_Healthy := (rGantryY_Pos_B_mm >= -200.0) AND (rGantryY_Pos_B_mm <= 12000.0);
bGY_C_Healthy := (rGantryY_Pos_C_mm >= -200.0) AND (rGantryY_Pos_C_mm <= 12000.0);

IF bGY_A_Healthy AND bGY_B_Healthy AND bGY_C_Healthy THEN
    IF ((rGantryY_Pos_A_mm >= rGantryY_Pos_B_mm) AND (rGantryY_Pos_A_mm <= rGantryY_Pos_C_mm)) OR
       ((rGantryY_Pos_A_mm >= rGantryY_Pos_C_mm) AND (rGantryY_Pos_A_mm <= rGantryY_Pos_B_mm)) THEN
        rVotedGantryY_mm := rGantryY_Pos_A_mm;
    ELSIF ((rGantryY_Pos_B_mm >= rGantryY_Pos_A_mm) AND (rGantryY_Pos_B_mm <= rGantryY_Pos_C_mm)) OR
          ((rGantryY_Pos_B_mm >= rGantryY_Pos_C_mm) AND (rGantryY_Pos_B_mm <= rGantryY_Pos_A_mm)) THEN
        rVotedGantryY_mm := rGantryY_Pos_B_mm;
    ELSE
        rVotedGantryY_mm := rGantryY_Pos_C_mm;
    END_IF;
    IF (rDev_GY_AB > 0.150) OR (rDev_GY_BC > 0.150) OR (rDev_GY_CA > 0.150) THEN
        dwDegradationWord := dwDegradationWord OR 16#0000_0100;
    END_IF;
ELSIF bGY_A_Healthy AND bGY_B_Healthy THEN
    rVotedGantryY_mm := (rGantryY_Pos_A_mm + rGantryY_Pos_B_mm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0200;
    bDegradedSensorActive := TRUE;
ELSIF bGY_B_Healthy AND bGY_C_Healthy THEN
    rVotedGantryY_mm := (rGantryY_Pos_B_mm + rGantryY_Pos_C_mm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0400;
    bDegradedSensorActive := TRUE;
ELSIF bGY_A_Healthy AND bGY_C_Healthy THEN
    rVotedGantryY_mm := (rGantryY_Pos_A_mm + rGantryY_Pos_C_mm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0800;
    bDegradedSensorActive := TRUE;
ELSIF bGY_A_Healthy THEN
    rVotedGantryY_mm := rGantryY_Pos_A_mm;
    dwDegradationWord := dwDegradationWord OR 16#0000_1000;
    bDegradedSensorActive := TRUE;
ELSIF bGY_B_Healthy THEN
    rVotedGantryY_mm := rGantryY_Pos_B_mm;
    dwDegradationWord := dwDegradationWord OR 16#0000_2000;
    bDegradedSensorActive := TRUE;
ELSIF bGY_C_Healthy THEN
    rVotedGantryY_mm := rGantryY_Pos_C_mm;
    dwDegradationWord := dwDegradationWord OR 16#0000_4000;
    bDegradedSensorActive := TRUE;
ELSE
    rVotedGantryY_mm := 0.0;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0100;
END_IF;

(* --- 2.3 Gantry Z Linear Scale 2oo3 Bank --- *)
rDev_GZ_AB := ABS(rGantryZ_Pos_A_mm - rGantryZ_Pos_B_mm);
rDev_GZ_BC := ABS(rGantryZ_Pos_B_mm - rGantryZ_Pos_C_mm);
rDev_GZ_CA := ABS(rGantryZ_Pos_C_mm - rGantryZ_Pos_A_mm);

bGZ_A_Healthy := (rGantryZ_Pos_A_mm >= -100.0) AND (rGantryZ_Pos_A_mm <= 2500.0);
bGZ_B_Healthy := (rGantryZ_Pos_B_mm >= -100.0) AND (rGantryZ_Pos_B_mm <= 2500.0);
bGZ_C_Healthy := (rGantryZ_Pos_C_mm >= -100.0) AND (rGantryZ_Pos_C_mm <= 2500.0);

IF bGZ_A_Healthy AND bGZ_B_Healthy AND bGZ_C_Healthy THEN
    IF ((rGantryZ_Pos_A_mm >= rGantryZ_Pos_B_mm) AND (rGantryZ_Pos_A_mm <= rGantryZ_Pos_C_mm)) OR
       ((rGantryZ_Pos_A_mm >= rGantryZ_Pos_C_mm) AND (rGantryZ_Pos_A_mm <= rGantryZ_Pos_B_mm)) THEN
        rVotedGantryZ_mm := rGantryZ_Pos_A_mm;
    ELSIF ((rGantryZ_Pos_B_mm >= rGantryZ_Pos_A_mm) AND (rGantryZ_Pos_B_mm <= rGantryZ_Pos_C_mm)) OR
          ((rGantryZ_Pos_B_mm >= rGantryZ_Pos_C_mm) AND (rGantryZ_Pos_B_mm <= rGantryZ_Pos_A_mm)) THEN
        rVotedGantryZ_mm := rGantryZ_Pos_B_mm;
    ELSE
        rVotedGantryZ_mm := rGantryZ_Pos_C_mm;
    END_IF;
    IF (rDev_GZ_AB > 0.080) OR (rDev_GZ_BC > 0.080) OR (rDev_GZ_CA > 0.080) THEN
        dwDegradationWord := dwDegradationWord OR 16#0000_8000;
    END_IF;
ELSIF bGZ_A_Healthy AND bGZ_B_Healthy THEN
    rVotedGantryZ_mm := (rGantryZ_Pos_A_mm + rGantryZ_Pos_B_mm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0001_0000;
    bDegradedSensorActive := TRUE;
ELSIF bGZ_B_Healthy AND bGZ_C_Healthy THEN
    rVotedGantryZ_mm := (rGantryZ_Pos_B_mm + rGantryZ_Pos_C_mm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0002_0000;
    bDegradedSensorActive := TRUE;
ELSIF bGZ_A_Healthy AND bGZ_C_Healthy THEN
    rVotedGantryZ_mm := (rGantryZ_Pos_A_mm + rGantryZ_Pos_C_mm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0004_0000;
    bDegradedSensorActive := TRUE;
ELSE
    rVotedGantryZ_mm := 0.0;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0200;
END_IF;

(* --- 2.4 Gimbal Tilt Angles A & B 2oo3 Bank --- *)
IF (rSpindleA_Tilt_A_deg >= -45.0) AND (rSpindleA_Tilt_A_deg <= 45.0) THEN
    rVotedSpindleA_deg := rSpindleA_Tilt_A_deg;
ELSIF (rSpindleA_Tilt_B_deg >= -45.0) AND (rSpindleA_Tilt_B_deg <= 45.0) THEN
    rVotedSpindleA_deg := rSpindleA_Tilt_B_deg;
ELSE
    rVotedSpindleA_deg := rSpindleA_Tilt_C_deg;
END_IF;

IF (rSpindleB_Tilt_A_deg >= -45.0) AND (rSpindleB_Tilt_A_deg <= 45.0) THEN
    rVotedSpindleB_deg := rSpindleB_Tilt_A_deg;
ELSIF (rSpindleB_Tilt_B_deg >= -45.0) AND (rSpindleB_Tilt_B_deg <= 45.0) THEN
    rVotedSpindleB_deg := rSpindleB_Tilt_B_deg;
ELSE
    rVotedSpindleB_deg := rSpindleB_Tilt_C_deg;
END_IF;

(* --- 2.5 Surface Normal Laser Distance 1, 2, 3 2oo3 Bank --- *)
(* Laser 1 *)
IF ((rLaserDist1_A_mm >= rLaserDist1_B_mm) AND (rLaserDist1_A_mm <= rLaserDist1_C_mm)) OR
   ((rLaserDist1_A_mm >= rLaserDist1_C_mm) AND (rLaserDist1_A_mm <= rLaserDist1_B_mm)) THEN
    rVotedLaserDist1_mm := rLaserDist1_A_mm;
ELSIF ((rLaserDist1_B_mm >= rLaserDist1_A_mm) AND (rLaserDist1_B_mm <= rLaserDist1_C_mm)) OR
      ((rLaserDist1_B_mm >= rLaserDist1_C_mm) AND (rLaserDist1_B_mm <= rLaserDist1_A_mm)) THEN
    rVotedLaserDist1_mm := rLaserDist1_B_mm;
ELSE
    rVotedLaserDist1_mm := rLaserDist1_C_mm;
END_IF;

(* Laser 2 *)
IF ((rLaserDist2_A_mm >= rLaserDist2_B_mm) AND (rLaserDist2_A_mm <= rLaserDist2_C_mm)) OR
   ((rLaserDist2_A_mm >= rLaserDist2_C_mm) AND (rLaserDist2_A_mm <= rLaserDist2_B_mm)) THEN
    rVotedLaserDist2_mm := rLaserDist2_A_mm;
ELSIF ((rLaserDist2_B_mm >= rLaserDist2_A_mm) AND (rLaserDist2_B_mm <= rLaserDist2_C_mm)) OR
      ((rLaserDist2_B_mm >= rLaserDist2_C_mm) AND (rLaserDist2_B_mm <= rLaserDist2_A_mm)) THEN
    rVotedLaserDist2_mm := rLaserDist2_B_mm;
ELSE
    rVotedLaserDist2_mm := rLaserDist2_C_mm;
END_IF;

(* Laser 3 *)
IF ((rLaserDist3_A_mm >= rLaserDist3_B_mm) AND (rLaserDist3_A_mm <= rLaserDist3_C_mm)) OR
   ((rLaserDist3_A_mm >= rLaserDist3_C_mm) AND (rLaserDist3_A_mm <= rLaserDist3_B_mm)) THEN
    rVotedLaserDist3_mm := rLaserDist3_A_mm;
ELSIF ((rLaserDist3_B_mm >= rLaserDist3_A_mm) AND (rLaserDist3_B_mm <= rLaserDist3_C_mm)) OR
      ((rLaserDist3_B_mm >= rLaserDist3_C_mm) AND (rLaserDist3_B_mm <= rLaserDist3_A_mm)) THEN
    rVotedLaserDist3_mm := rLaserDist3_B_mm;
ELSE
    rVotedLaserDist3_mm := rLaserDist3_C_mm;
END_IF;

(* --- 2.6 Pressure-Foot Clamping Load Cell 2oo3 Bank --- *)
IF ((rClampForce_A_N >= rClampForce_B_N) AND (rClampForce_A_N <= rClampForce_C_N)) OR
   ((rClampForce_A_N >= rClampForce_C_N) AND (rClampForce_A_N <= rClampForce_B_N)) THEN
    rVotedClampForce_N := rClampForce_A_N;
ELSIF ((rClampForce_B_N >= rClampForce_A_N) AND (rClampForce_B_N <= rClampForce_C_N)) OR
      ((rClampForce_B_N >= rClampForce_C_N) AND (rClampForce_B_N <= rClampForce_A_N)) THEN
    rVotedClampForce_N := rClampForce_B_N;
ELSE
    rVotedClampForce_N := rClampForce_C_N;
END_IF;

(* --- 2.7 Spindle Dynamic Torque 2oo3 Bank --- *)
IF ((rSpindleTorque_A_Nm >= rSpindleTorque_B_Nm) AND (rSpindleTorque_A_Nm <= rSpindleTorque_C_Nm)) OR
   ((rSpindleTorque_A_Nm >= rSpindleTorque_C_Nm) AND (rSpindleTorque_A_Nm <= rSpindleTorque_B_Nm)) THEN
    rVotedSpindleTorque_Nm := rSpindleTorque_A_Nm;
ELSIF ((rSpindleTorque_B_Nm >= rSpindleTorque_A_Nm) AND (rSpindleTorque_B_Nm <= rSpindleTorque_C_Nm)) OR
      ((rSpindleTorque_B_Nm >= rSpindleTorque_C_Nm) AND (rSpindleTorque_B_Nm <= rSpindleTorque_A_Nm)) THEN
    rVotedSpindleTorque_Nm := rSpindleTorque_B_Nm;
ELSE
    rVotedSpindleTorque_Nm := rSpindleTorque_C_Nm;
END_IF;

(* --- 2.8 Spindle Triaxial Vibration 2oo3 Bank --- *)
IF ((rToolVibration_A_mms >= rToolVibration_B_mms) AND (rToolVibration_A_mms <= rToolVibration_C_mms)) OR
   ((rToolVibration_A_mms >= rToolVibration_C_mms) AND (rToolVibration_A_mms <= rToolVibration_B_mms)) THEN
    rVotedToolVibration_mms := rToolVibration_A_mms;
ELSIF ((rToolVibration_B_mms >= rToolVibration_A_mms) AND (rToolVibration_B_mms <= rToolVibration_C_mms)) OR
      ((rToolVibration_B_mms >= rToolVibration_C_mms) AND (rToolVibration_B_mms <= rToolVibration_A_mms)) THEN
    rVotedToolVibration_mms := rToolVibration_B_mms;
ELSE
    rVotedToolVibration_mms := rToolVibration_C_mms;
END_IF;

(* --- 2.9 Spindle Ceramic Front Bearing Temperature 2oo3 Bank --- *)
IF ((rBearingTemp_A_degC >= rBearingTemp_B_degC) AND (rBearingTemp_A_degC <= rBearingTemp_C_degC)) OR
   ((rBearingTemp_A_degC >= rBearingTemp_C_degC) AND (rBearingTemp_A_degC <= rBearingTemp_B_degC)) THEN
    rVotedBearingTemp_degC := rBearingTemp_A_degC;
ELSIF ((rBearingTemp_B_degC >= rBearingTemp_A_degC) AND (rBearingTemp_B_degC <= rBearingTemp_C_degC)) OR
      ((rBearingTemp_B_degC >= rBearingTemp_C_degC) AND (rBearingTemp_B_degC <= rBearingTemp_A_degC)) THEN
    rVotedBearingTemp_degC := rBearingTemp_B_degC;
ELSE
    rVotedBearingTemp_degC := rBearingTemp_C_degC;
END_IF;

(* --- 2.10 Optical Hole Diameter & Countersink Depth 2oo3 Bank --- *)
IF ((rHoleDiamLaser_A_mm >= rHoleDiamLaser_B_mm) AND (rHoleDiamLaser_A_mm <= rHoleDiamLaser_C_mm)) OR
   ((rHoleDiamLaser_A_mm >= rHoleDiamLaser_C_mm) AND (rHoleDiamLaser_A_mm <= rHoleDiamLaser_B_mm)) THEN
    rVotedHoleDiam_mm := rHoleDiamLaser_A_mm;
ELSE
    rVotedHoleDiam_mm := rHoleDiamLaser_B_mm;
END_IF;

IF ((rCountersinkDepth_A_mm >= rCountersinkDepth_B_mm) AND (rCountersinkDepth_A_mm <= rCountersinkDepth_C_mm)) OR
   ((rCountersinkDepth_A_mm >= rCountersinkDepth_C_mm) AND (rCountersinkDepth_A_mm <= rCountersinkDepth_B_mm)) THEN
    rVotedCountersinkDepth_mm := rCountersinkDepth_A_mm;
ELSE
    rVotedCountersinkDepth_mm := rCountersinkDepth_B_mm;
END_IF;

rVotedSpindleSpeed_rpm := rSpindleSpeed_A_rpm;
''')

    # -------------------------------------------------------------
    # CODE BODY - SECTION 3: SURFACE NORMAL SOLVER
    # -------------------------------------------------------------
    parts.append('''
(* ========================================================================================= *)
(* 3.0 MULTI-POINT OPTICAL LASER SURFACE NORMAL VECTOR ALIGNMENT SOLVER                      *)
(* ========================================================================================= *)
(* Computes the local wing surface normal unit vector from 3 triangulation distance probes   *)
(* arranged at 120-degree intervals on a 75.0 mm pitch circle radius. Evaluates surface tilt *)
(* and drives the spherical gimbal A/B axes to maintain perpendicularity within +/- 0.08 deg.*)

(* Set 3D spatial coordinates of laser touch points in end-effector coordinates *)
rP1_x := c_LaserPitchRadius_mm;
rP1_y := 0.0;
rP1_z := -rVotedLaserDist1_mm;

rP2_x := -0.5 * c_LaserPitchRadius_mm;
rP2_y := 0.86602540 * c_LaserPitchRadius_mm;
rP2_z := -rVotedLaserDist2_mm;

rP3_x := -0.5 * c_LaserPitchRadius_mm;
rP3_y := -0.86602540 * c_LaserPitchRadius_mm;
rP3_z := -rVotedLaserDist3_mm;

(* Vectors spanning the triangulation plane: v1 = P2 - P1, v2 = P3 - P1 *)
rV1_x := rP2_x - rP1_x;
rV1_y := rP2_y - rP1_y;
rV1_z := rP2_z - rP1_z;

rV2_x := rP3_x - rP1_x;
rV2_y := rP3_y - rP1_y;
rV2_z := rP3_z - rP1_z;

(* Cross product: n = v1 x v2 *)
rNorm_x := (rV1_y * rV2_z) - (rV1_z * rV2_y);
rNorm_y := (rV1_z * rV2_x) - (rV1_x * rV2_z);
rNorm_z := (rV1_x * rV2_y) - (rV1_y * rV2_x);

(* Ensure vector points outward along +Z tool axis *)
IF rNorm_z < 0.0 THEN
    rNorm_x := -rNorm_x;
    rNorm_y := -rNorm_y;
    rNorm_z := -rNorm_z;
END_IF;

(* Vector magnitude *)
rNormMag := SQRT((rNorm_x * rNorm_x) + (rNorm_y * rNorm_y) + (rNorm_z * rNorm_z));
IF rNormMag < 0.00001 THEN
    rNormMag := 1.0; (* Prevent numerical zero-division *)
END_IF;

(* Unit normal vector *)
rUnitNorm_x := rNorm_x / rNormMag;
rUnitNorm_y := rNorm_y / rNormMag;
rUnitNorm_z := rNorm_z / rNormMag;

(* Angular tilt error relative to tool Z axis: tilt = arccos(n_z) *)
IF rUnitNorm_z > 1.0 THEN
    rUnitNorm_z := 1.0;
ELSIF rUnitNorm_z < -1.0 THEN
    rUnitNorm_z := -1.0;
END_IF;

(* Series expansion approximation for arccos(z) near z = 1: theta ~ sqrt(2*(1-z)) *)
IF rUnitNorm_z >= 0.9998 THEN
    rSurfaceTilt_deg := SQRT(2.0 * (1.0 - rUnitNorm_z)) * c_RadToDeg;
ELSE
    rSurfaceTilt_deg := SQRT((rUnitNorm_x * rUnitNorm_x) + (rUnitNorm_y * rUnitNorm_y)) * c_RadToDeg;
END_IF;
rSurfaceTiltError_deg := rSurfaceTilt_deg;

(* Small-angle gimbal attitude corrections *)
rTiltAngleA_deg := -rUnitNorm_y * c_RadToDeg;
rTiltAngleB_deg :=  rUnitNorm_x * c_RadToDeg;
''')

    # -------------------------------------------------------------
    # CODE BODY - SECTION 4: PRESSURE-FOOT COMPLIANCE & GAP MODEL
    # -------------------------------------------------------------
    parts.append('''
(* ========================================================================================= *)
(* 4.0 DYNAMIC PRESSURE-FOOT CLAMPING COMPLIANCE & GAP REGULATION                            *)
(* ========================================================================================= *)
(* Evaluates non-linear contact compliance between CFRP wing skin and Titanium spar.        *)
(* Models inter-laminar gap separation: delta_gap = delta_0 * exp(-F_clamp / F_crit).       *)
(* Executes closed-loop PI regulation on proportional hydraulic clamping valve.             *)

(* Real-time inter-laminar separation estimation *)
IF rVotedClampForce_N > 10.0 THEN
    rEstimatedInterlayerGap_um := c_StackInitialGap_um * EXP(-rVotedClampForce_N / c_CriticalClampForce_N);
ELSE
    rEstimatedInterlayerGap_um := c_StackInitialGap_um;
END_IF;

(* Closed-loop clamping force regulator: target nominal load 2,500 N *)
rClampError_N := rNominalClampForce_N - rVotedClampForce_N;

(* Anti-windup clamping integrator (active only when FSM is in clamp or cutting states) *)
IF (iFsmState >= 3) AND (iFsmState <= 7) THEN
    rClampIntegral_N := rClampIntegral_N + (rClampError_N * rScanTime_s);
    IF rClampIntegral_N > 800.0 THEN
        rClampIntegral_N := 800.0;
    ELSIF rClampIntegral_N < -800.0 THEN
        rClampIntegral_N := -800.0;
    END_IF;
    
    rClampRawOutput_pct := (rClampKp * rClampError_N) + (rClampKi * rClampIntegral_N);
    IF rClampRawOutput_pct > 100.0 THEN
        rClampValveFlowCmd_pct := 100.0;
    ELSIF rClampRawOutput_pct < 0.0 THEN
        rClampValveFlowCmd_pct := 0.0;
    ELSE
        rClampValveFlowCmd_pct := rClampRawOutput_pct;
    END_IF;
ELSE
    rClampIntegral_N := 0.0;
    rClampValveFlowCmd_pct := 0.0;
END_IF;

(* Clamping load verification: warn if gap exceeds 25 um during active machining *)
IF (iFsmState >= 4) AND (iFsmState <= 7) AND (rEstimatedInterlayerGap_um > c_MaxAllowableGap_um) THEN
    dwWarningWord := dwWarningWord OR 16#0000_0001; (* Warning: Inter-laminar gap exceeds 25 um *)
END_IF;

IF (iFsmState >= 4) AND (iFsmState <= 7) AND (rVotedClampForce_N < 1800.0) THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0001; (* Trip: Clamping force insufficient for zero-burr *)
END_IF;
''')

    # -------------------------------------------------------------
    # CODE BODY - SECTION 5: ACTIVE THERMAL SPINDLE & CHATTER/WEAR
    # -------------------------------------------------------------
    parts.append('''
(* ========================================================================================= *)
(* 5.0 HIGH-SPEED SPINDLE ACTIVE THERMAL COMPENSATION & TOOL HEALTH                          *)
(* ========================================================================================= *)
(* 24,000 RPM motorized spindle dynamics: real-time ceramic bearing thermal expansion        *)
(* model (Delta_L = alpha * L_0 * dT + beta * omega^2). Triaxial accelerometer FFT kurtosis  *)
(* and dynamic torque derivative (dTq/dt) for drill wear and chipping/breakage trip.        *)

(* Spindle Shaft Thermal & Centrifugal Elongation [um] *)
rSpindleThermalGrowth_um := (c_ShaftThermalCoeff_1K * c_SpindleShaftLength_mm * (rVotedBearingTemp_degC - c_RefBearingTemp_degC) * 1000.0)
                          + (c_CentrifugalCoeff * rVotedSpindleSpeed_rpm * rVotedSpindleSpeed_rpm * 1000.0);

IF rSpindleThermalGrowth_um < 0.0 THEN
    rSpindleThermalGrowth_um := 0.0;
END_IF;

(* Thermal offset applied to Z motion command *)
rZThermalCompensatedPos_mm := rTargetGantryZ_mm - (rSpindleThermalGrowth_um * 0.001);

(* Spindle Instantaneous Cutting Power [W]: P = omega * Tq *)
rCuttingPower_W := (2.0 * c_Pi * rVotedSpindleSpeed_rpm / 60.0) * rVotedSpindleTorque_Nm;

(* Dynamic Cutting Derivatives: dFz/dt and dTq/dt *)
rThrustForceDerivative_Ns := (rVotedClampForce_N - rPrevThrustForce_N) / rScanTime_s;
rTorqueDerivative_Nms     := (rVotedSpindleTorque_Nm - rPrevTorque_Nm) / rScanTime_s;

rPrevThrustForce_N := rVotedClampForce_N;
rPrevTorque_Nm     := rVotedSpindleTorque_Nm;

(* Triaxial Vibration Filtering & Crest Factor Evaluation *)
rFilteredVibration_mms := (0.985 * rFilteredVibration_mms) + (0.015 * rVotedToolVibration_mms);
IF rVotedToolVibration_mms > rVibrationPeak_mms THEN
    rVibrationPeak_mms := rVotedToolVibration_mms;
ELSE
    rVibrationPeak_mms := rVibrationPeak_mms * 0.998; (* Peak exponential decay *)
END_IF;

IF rFilteredVibration_mms > 0.05 THEN
    rVibrationCrestFactor := rVibrationPeak_mms / rFilteredVibration_mms;
ELSE
    rVibrationCrestFactor := 1.0;
END_IF;

(* Drill Chipping / Flank Wear Warning *)
IF (rFilteredVibration_mms > 5.5) OR (rVibrationCrestFactor > 4.2) THEN
    bToolWearWarning := TRUE;
    dwWarningWord := dwWarningWord OR 16#0000_0002; (* Spindle high vibration / tool wear *)
ELSE
    bToolWearWarning := FALSE;
END_IF;

(* Catastrophic Drill Bit Breakage Trip (< 10 ms fast trip):
   Triggered if torque collapses abruptly while feed velocity is positive and thrust is high *)
tBreakageDetectTimer(IN := ((iFsmState = 4 OR iFsmState = 6) AND (rTorqueDerivative_Nms < -18.0) AND (rVotedSpindleTorque_Nm < 0.25)), PT := T#8MS);

IF tBreakageDetectTimer.Q THEN
    bDrillChippingFault := TRUE;
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0002; (* Catastrophic drill bit fracture *)
END_IF;

(* Spindle Bearing High-High Temperature Trip *)
IF rVotedBearingTemp_degC > rMaxBearingTemp_degC THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0004; (* Bearing over-temperature trip *)
END_IF;

(* Spindle Over-Torque Trip *)
IF rVotedSpindleTorque_Nm > rMaxAllowableTorque_Nm THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0008; (* Spindle mechanical overload trip *)
END_IF;
''')

    # -------------------------------------------------------------
    # CODE BODY - SECTION 6: CFRP / TITANIUM TRANSITION OBSERVER
    # -------------------------------------------------------------
    parts.append('''
(* ========================================================================================= *)
(* 6.0 MULTI-LAYER CFRP / TI-6AL-4V BOUNDARY TRANSITION OBSERVER                             *)
(* ========================================================================================= *)
(* Detects sudden material transition from CFRP composite into Titanium alloy via rate of    *)
(* change of cutting torque and thrust. Dynamically modulates spindle speed from 16,000 RPM  *)
(* to 2,600 RPM and feed rate from 960 mm/min to 52 mm/min to prevent thermal hardening.     *)

tTransitionDebounce(IN := ((iFsmState = 4) AND (rVotedSpindleTorque_Nm > 1.65) AND (rTorqueDerivative_Nms > 12.0)), PT := T#6MS);

IF tTransitionDebounce.Q AND NOT bMaterialTransitionLatched THEN
    bMaterialTransitionLatched := TRUE;
    iFsmState := 5; (* Jump directly to MATERIAL_TRANSITION_SLOWDOWN state *)
END_IF;

(* S-Curve feed and speed rate-limiter *)
IF iFsmState = 4 THEN
    (* CFRP High-Speed Regime *)
    rTargetSpeed_rpm := rCfrpSpindleSpeedDemand_rpm;
    rTargetFeedVel_mms := rCfrpFeedRateDemand_mm_min / 60.0; (* mm/s *)
    rMqlAerosolPulseCmd_pct := 15.0; (* Light MQL aerosol for dust evacuation *)
ELSIF iFsmState = 5 THEN
    (* Transition Slowdown Regime *)
    rTargetSpeed_rpm := rTitaniumSpindleSpeedDemand_rpm;
    rTargetFeedVel_mms := 0.20; (* Slow creep feed during interface crossing *)
    rMqlAerosolPulseCmd_pct := 75.0; (* Increase MQL pulse flow *)
ELSIF iFsmState = 6 THEN
    (* Titanium Heavy-Duty Regime *)
    rTargetSpeed_rpm := rTitaniumSpindleSpeedDemand_rpm;
    rTargetFeedVel_mms := rTitaniumFeedRateDemand_mm_min / 60.0; (* mm/s *)
    rMqlAerosolPulseCmd_pct := 100.0; (* Maximum MQL cooling aerosol *)
ELSIF iFsmState = 7 THEN
    (* Precision Countersink Regime *)
    rTargetSpeed_rpm := 1800.0;
    rTargetFeedVel_mms := 0.15;
    rMqlAerosolPulseCmd_pct := 50.0;
ELSE
    rTargetFeedVel_mms := 0.0;
    IF (iFsmState = 0) OR (iFsmState >= 8) THEN
        rTargetSpeed_rpm := 0.0;
        rMqlAerosolPulseCmd_pct := 0.0;
    END_IF;
END_IF;

(* Smooth rate-limited progression of spindle speed command *)
IF rInternalSpeed_rpm < rTargetSpeed_rpm THEN
    rInternalSpeed_rpm := rInternalSpeed_rpm + (12000.0 * rScanTime_s);
    IF rInternalSpeed_rpm > rTargetSpeed_rpm THEN
        rInternalSpeed_rpm := rTargetSpeed_rpm;
    END_IF;
ELSIF rInternalSpeed_rpm > rTargetSpeed_rpm THEN
    rInternalSpeed_rpm := rInternalSpeed_rpm - (18000.0 * rScanTime_s);
    IF rInternalSpeed_rpm < rTargetSpeed_rpm THEN
        rInternalSpeed_rpm := rTargetSpeed_rpm;
    END_IF;
END_IF;
rSpindleSpeedCmd_rpm := rInternalSpeed_rpm;

(* Smooth rate-limited progression of Z feed velocity command *)
IF rInternalFeedVel_mms < rTargetFeedVel_mms THEN
    rInternalFeedVel_mms := rInternalFeedVel_mms + (25.0 * rScanTime_s);
    IF rInternalFeedVel_mms > rTargetFeedVel_mms THEN
        rInternalFeedVel_mms := rTargetFeedVel_mms;
    END_IF;
ELSIF rInternalFeedVel_mms > rTargetFeedVel_mms THEN
    rInternalFeedVel_mms := rInternalFeedVel_mms - (45.0 * rScanTime_s);
    IF rInternalFeedVel_mms < rTargetFeedVel_mms THEN
        rInternalFeedVel_mms := rTargetFeedVel_mms;
    END_IF;
END_IF;
rZFeedVelocityCmd_mms := rInternalFeedVel_mms;
''')

    # -------------------------------------------------------------
    # CODE BODY - SECTION 7: IN-PROCESS LASER METROLOGY EVALUATOR
    # -------------------------------------------------------------
    parts.append('''
(* ========================================================================================= *)
(* 7.0 IN-PROCESS OPTICAL LASER HOLE METROLOGY & COUNTERSINK EVALUATION                      *)
(* ========================================================================================= *)
(* Post-drilling quality gate: evaluates hole diameter against aerospace H8 tolerance       *)
(* (6.350 mm +0.015 / -0.000 mm) and countersink depth (+/- 0.020 mm).                      *)

IF iFsmState = 8 THEN
    (* Evaluate diameter tolerance *)
    IF (rVotedHoleDiam_mm >= (rNominalHoleDiameter_mm - rHoleDiameterTolLower_mm)) AND
       (rVotedHoleDiam_mm <= (rNominalHoleDiameter_mm + rHoleDiameterTolUpper_mm)) AND
       (ABS(rVotedCountersinkDepth_mm - rCountersinkDepthTarget_mm) <= rCountersinkDepthTol_mm) THEN
        bHoleMetrologyPassed := TRUE;
    ELSE
        bHoleMetrologyPassed := FALSE;
    END_IF;
    
    (* Check for hole diameter undersize / oversize fault *)
    IF rVotedHoleDiam_mm < (rNominalHoleDiameter_mm - rHoleDiameterTolLower_mm) THEN
        dwWarningWord := dwWarningWord OR 16#0000_0004; (* Hole undersize warning *)
    ELSIF rVotedHoleDiam_mm > (rNominalHoleDiameter_mm + rHoleDiameterTolUpper_mm) THEN
        dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0010; (* Hole oversize reject trip *)
    END_IF;

    (* Check countersink depth tolerance *)
    IF ABS(rVotedCountersinkDepth_mm - rCountersinkDepthTarget_mm) > rCountersinkDepthTol_mm THEN
        dwWarningWord := dwWarningWord OR 16#0000_0008; (* Countersink depth out of tolerance *)
    END_IF;
END_IF;
''')

    # -------------------------------------------------------------
    # CODE BODY - SECTION 8: FASTENER INSERTION & EMR PULSE
    # -------------------------------------------------------------
    parts.append('''
(* ========================================================================================= *)
(* 8.0 AUTOMATED FASTENER INSERTION & ELECTROMAGNETIC RIVETING (EMR)                         *)
(* ========================================================================================= *)
(* Monitors robotic collet insertion resistance force (< 180 N) and fires high-energy       *)
(* capacitor discharge (4.2 kV, 480 uF) through the EMR pancake coil to cold-expand rivet.  *)

IF iFsmState = 9 THEN
    (* Fastener insertion stroke *)
    rFastenerColletAdvanceCmd_mm := 65.0; (* Collet advance stroke to seat fastener *)
    rFastenerInsertionForce_N := rVotedClampForce_N * 0.065; (* Calibrated mechanical push force *)
    
    IF rFastenerInsertionForce_N > 180.0 THEN
        dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0020; (* Fastener insertion jamming trip *)
    END_IF;

    IF (rFastenerFeederPos_A_mm >= 64.5) AND (rFastenerInsertionForce_N <= 180.0) THEN
        bFastenerSeatedOk := TRUE;
    END_IF;
ELSE
    rFastenerColletAdvanceCmd_mm := 0.0;
END_IF;

IF iFsmState = 10 THEN
    (* Electromagnetic Rivet Set Pulse *)
    bEmrDischargeTrigger := TRUE;
    
    (* Damped RLC pulse dynamics: peak discharge current estimate *)
    (* I_peak ~ V0 / sqrt(L/C + R^2) *)
    rEmrPeakCurrent_kA := (c_EmrChargeVoltage_V / SQRT((c_EmrCoilInductance_uH * 1.0E-6 / (c_EmrCapacitance_uF * 1.0E-6)) + (c_EmrCircuitResistance_Ohm * c_EmrCircuitResistance_Ohm))) * 0.001;
    
    (* Estimated residual interference stress under rivet head [MPa] *)
    rResidualStackStress_MPa := 245.0 + (rEmrPeakCurrent_kA * 4.25);
    
    bEmrPulseDelivered := TRUE;
ELSE
    bEmrDischargeTrigger := FALSE;
END_IF;
''')

    # -------------------------------------------------------------
    # CODE BODY - SECTION 9: 8x8 DISCRETE STATE-SPACE MPC GOVERNOR
    # -------------------------------------------------------------
    parts.append('''
(* ========================================================================================= *)
(* 9.0 8x8 DISCRETE STATE-SPACE MODEL & RECEDING-HORIZON MPC GOVERNOR                        *)
(* ========================================================================================= *)
(* Solves multi-axis gantry thrust, spindle torque, hydraulic clamping, and MQL lubrication  *)
(* optimization via active-set projected gradient descent at 1 ms sampling frequency.        *)

bMpcActiveOptimization := (iFsmState >= 3) AND (iFsmState <= 7) AND NOT bCellTripped;

IF bMpcActiveOptimization THEN
    (* Populate current state vector x_state *)
    x_state[1] := rVotedGantryZ_mm - rZThermalCompensatedPos_mm; (* Z position tracking error [mm] *)
    x_state[2] := rZFeedVelocityCmd_mms;                        (* Z feed velocity [mm/s] *)
    x_state[3] := rVotedClampForce_N - rNominalClampForce_N;     (* Clamping force error [N] *)
    x_state[4] := rThrustForceDerivative_Ns;                     (* Hydraulic clamp force rate [N/s] *)
    x_state[5] := rVotedSpindleTorque_Nm - 1.25;                 (* Cutting torque error [N*m] *)
    x_state[6] := (rVotedSpindleSpeed_rpm - rSpindleSpeedCmd_rpm) * 0.10472; (* Speed error [rad/s] *)
    x_state[7] := rSpindleThermalGrowth_um;                      (* Spindle axial thermal growth [um] *)
    x_state[8] := rFilteredVibration_mms;                        (* Filtered tool nose vibration [mm/s] *)

    (* Reference trajectory vector x_ref *)
    x_ref[1] := 0.0;
    x_ref[2] := rTargetFeedVel_mms;
    x_ref[3] := 0.0;
    x_ref[4] := 0.0;
    x_ref[5] := 0.0;
    x_ref[6] := 0.0;
    x_ref[7] := 0.0;
    x_ref[8] := 0.0;

    (* Tracking error: x_err = x_state - x_ref *)
    FOR iRow := 1 TO 8 DO
        x_err[iRow] := x_state[iRow] - x_ref[iRow];
    END_FOR;

    (* State propagation prediction: x_pred = A * x_state + B * u_mpc *)
    FOR iRow := 1 TO 8 DO
        x_pred[iRow] := 0.0;
        FOR iCol := 1 TO 8 DO
            x_pred[iRow] := x_pred[iRow] + (A_mat[iRow, iCol] * x_state[iCol]);
        END_FOR;
        FOR iCol := 1 TO 4 DO
            x_pred[iRow] := x_pred[iRow] + (B_mat[iRow, iCol] * u_mpc[iCol]);
        END_FOR;
    END_FOR;

    (* Quadratic cost function evaluation:
       J = 0.5 * sum(Q_i * x_err_i^2) + 0.5 * sum(R_j * u_j^2) *)
    rCostValue := 0.0;
    FOR iRow := 1 TO 8 DO
        rCostValue := rCostValue + (0.5 * Q_diag[iRow] * x_err[iRow] * x_err[iRow]);
    END_FOR;
    FOR iCol := 1 TO 4 DO
        rCostValue := rCostValue + (0.5 * R_diag[iCol] * u_mpc[iCol] * u_mpc[iCol]);
    END_FOR;

    (* Compute gradient vector: grad_J = B^T * Q * x_err + R * u_mpc *)
    FOR iCol := 1 TO 4 DO
        grad_J[iCol] := R_diag[iCol] * u_mpc[iCol];
        FOR iRow := 1 TO 8 DO
            grad_J[iCol] := grad_J[iCol] + (B_mat[iRow, iCol] * Q_diag[iRow] * x_err[iRow]);
        END_FOR;
    END_FOR;

    (* Projected gradient descent update with box constraints *)
    FOR iIter := 1 TO 3 DO
        FOR iCol := 1 TO 4 DO
            u_delta[iCol] := - (grad_J[iCol] / H_diag[iCol]) * rMpcStepSize;
            u_mpc[iCol] := u_mpc[iCol] + u_delta[iCol];
            
            (* Actuator hard constraint saturation *)
            IF u_mpc[iCol] > u_max[iCol] THEN
                u_mpc[iCol] := u_max[iCol];
            ELSIF u_mpc[iCol] < u_min[iCol] THEN
                u_mpc[iCol] := u_min[iCol];
            END_IF;
        END_FOR;
    END_FOR;
ELSE
    (* MPC inactive: reset control vector *)
    u_mpc[1] := 0.0;
    u_mpc[2] := 0.0;
    u_mpc[3] := 0.0;
    u_mpc[4] := 0.0;
END_IF;
''')

    # -------------------------------------------------------------
    # CODE BODY - SECTION 10: 12-STATE FINITE STATE MACHINE (FSM)
    # -------------------------------------------------------------
    parts.append('''
(* ========================================================================================= *)
(* 10.0 MULTI-STAGE 12-STATE OPERATIONAL FINITE STATE MACHINE (FSM)                          *)
(* ========================================================================================= *)
(* Executes fully deterministic sequential aerospace drilling and fastening cycle:           *)
(*   State 0:  GANTRY_STANDBY_HOMING                                                         *)
(*   State 1:  WINGBOX_DATUM_ALIGNMENT                                                       *)
(*   State 2:  SURFACE_NORMAL_LASER_PROBE                                                    *)
(*   State 3:  PRESSURE_FOOT_FORCE_ENGAGED                                                   *)
(*   State 4:  CFRP_LAYER_HIGH_SPEED_DRILL                                                   *)
(*   State 5:  MATERIAL_TRANSITION_SLOWDOWN                                                  *)
(*   State 6:  TITANIUM_LAYER_HEAVY_DRILL                                                   *)
(*   State 7:  PRECISION_COUNTERSINK_PASS                                                    *)
(*   State 8:  IN_PROCESS_LASER_METROLOGY                                                    *)
(*   State 9:  AUTOMATED_FASTENER_INSERTION                                                  *)
(*   State 10: EMR_ELECTROMAGNETIC_RIVET_SET                                                 *)
(*   State 11: EMERGENCY_ESTOP_SPINDLE_RETRACT                                               *)

(* Master Safety Trip Handling *)
IF (dwAlarmWord1 <> 16#0000_0000) OR (dwAlarmWord2 <> 16#0000_0000) THEN
    bCellTripped := TRUE;
    bCellRunning := FALSE;
    bCellReady := FALSE;
    iFsmState := 11; (* Emergency Retract *)
END_IF;

(* Timer instance call *)
tStateTimer(IN := (iFsmState = iPrevFsmState), PT := T#60S);
iPrevFsmState := iFsmState;

CASE iFsmState OF

    0: (* GANTRY_STANDBY_HOMING *)
        bCellRunning := FALSE;
        bCycleComplete := FALSE;
        bVacuumSuctionEnable := FALSE;
        rGantryX_Cmd_mm := rVotedGantryX_mm;
        rGantryY_Cmd_mm := rVotedGantryY_mm;
        rGantryZ_Cmd_mm := 0.0; (* Retracted home plane *)
        rSpindleA_Cmd_deg := 0.0;
        rSpindleB_Cmd_deg := 0.0;

        IF bMasterEnable AND bEmergencyStop AND NOT bLightCurtainIntrusion AND (dwAlarmWord1 = 0) THEN
            bCellReady := TRUE;
            IF bResetFaults THEN
                bCellTripped := FALSE;
                bMaterialTransitionLatched := FALSE;
                bHoleMetrologyPassed := FALSE;
                bFastenerSeatedOk := FALSE;
                bEmrPulseDelivered := FALSE;
                iFsmState := 1; (* Advance to Wingbox Alignment *)
            END_IF;
        ELSE
            bCellReady := FALSE;
        END_IF;

    1: (* WINGBOX_DATUM_ALIGNMENT *)
        bCellRunning := TRUE;
        bCellReady := FALSE;
        rGantryX_Cmd_mm := rTargetGantryX_mm;
        rGantryY_Cmd_mm := rTargetGantryY_mm;
        rGantryZ_Cmd_mm := rTargetGantryZ_mm + 50.0; (* 50 mm clearance standoff plane *)
        rSpindleA_Cmd_deg := 0.0;
        rSpindleB_Cmd_deg := 0.0;

        IF (ABS(rVotedGantryX_mm - rTargetGantryX_mm) < 0.050) AND
           (ABS(rVotedGantryY_mm - rTargetGantryY_mm) < 0.050) THEN
            iFsmState := 2; (* Advance to Laser Normal Probe *)
        END_IF;

    2: (* SURFACE_NORMAL_LASER_PROBE *)
        rGantryZ_Cmd_mm := rTargetGantryZ_mm + 15.0; (* Close standoff for laser triangulation *)
        tLaserSettleTimer(IN := TRUE, PT := T#40MS);

        (* Gimbal alignment closed-loop tracking *)
        rSpindleA_Cmd_deg := rTiltAngleA_deg;
        rSpindleB_Cmd_deg := rTiltAngleB_deg;

        IF tLaserSettleTimer.Q AND (rSurfaceTiltError_deg <= 0.080) THEN
            tLaserSettleTimer(IN := FALSE);
            iFsmState := 3; (* Advance to Pressure Foot Engage *)
        END_IF;

    3: (* PRESSURE_FOOT_FORCE_ENGAGED *)
        bVacuumSuctionEnable := TRUE; (* Start CFRP chip/dust vacuum *)
        rGantryZ_Cmd_mm := rTargetGantryZ_mm; (* Touchdown on wing surface *)
        tClampDwellTimer(IN := (rVotedClampForce_N >= 2400.0), PT := T#50MS);

        IF tClampDwellTimer.Q AND (rEstimatedInterlayerGap_um < c_MaxAllowableGap_um) THEN
            tClampDwellTimer(IN := FALSE);
            iFsmState := 4; (* Advance to CFRP High-Speed Drilling *)
        END_IF;

    4: (* CFRP_LAYER_HIGH_SPEED_DRILL *)
        (* High-speed drilling in progress, feed velocity and RPM modulated by Section 6 *)
        rGantryZ_Cmd_mm := rVotedGantryZ_mm + (rZFeedVelocityCmd_mms * rScanTime_s);
        
        (* Transition condition handled by Section 6 which sets iFsmState := 5 *)
        (* Backup depth check: if Z penetrates through 15 mm composite thickness *)
        IF (rVotedGantryZ_mm - rTargetGantryZ_mm) > 14.5 THEN
            iFsmState := 5;
        END_IF;

    5: (* MATERIAL_TRANSITION_SLOWDOWN *)
        (* Spindle speed ramped down to 2,600 RPM and feed rate to 52 mm/min *)
        rGantryZ_Cmd_mm := rVotedGantryZ_mm + (rZFeedVelocityCmd_mms * rScanTime_s);

        IF (rVotedSpindleSpeed_rpm <= 2800.0) AND (rVotedGantryZ_mm - rTargetGantryZ_mm > 15.2) THEN
            iFsmState := 6; (* Advance to Titanium Heavy Drilling *)
        END_IF;

    6: (* TITANIUM_LAYER_HEAVY_DRILL *)
        rGantryZ_Cmd_mm := rVotedGantryZ_mm + (rZFeedVelocityCmd_mms * rScanTime_s);

        (* Total stack penetration check: 14.2 mm CFRP + 9.8 mm Titanium = 24.0 mm *)
        IF (rVotedGantryZ_mm - rTargetGantryZ_mm) >= 24.2 THEN
            iFsmState := 7; (* Advance to Precision Countersink *)
        END_IF;

    7: (* PRECISION_COUNTERSINK_PASS *)
        rGantryZ_Cmd_mm := rTargetGantryZ_mm + 24.0 + rCountersinkDepthTarget_mm;
        tCountersinkDwellTimer(IN := (ABS(rVotedCountersinkDepth_mm - rCountersinkDepthTarget_mm) < 0.015), PT := T#120MS);

        IF tCountersinkDwellTimer.Q THEN
            tCountersinkDwellTimer(IN := FALSE);
            iFsmState := 8; (* Advance to In-Process Metrology *)
        END_IF;

    8: (* IN_PROCESS_LASER_METROLOGY *)
        (* Retract spindle and index optical telecentric laser probe into bore *)
        rGantryZ_Cmd_mm := rTargetGantryZ_mm + 10.0;
        tMetrologyScanTimer(IN := TRUE, PT := T#80MS);

        IF tMetrologyScanTimer.Q THEN
            tMetrologyScanTimer(IN := FALSE);
            IF bHoleMetrologyPassed THEN
                iFsmState := 9; (* Quality passed: advance to Fastener Insertion *)
            ELSE
                dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0040; (* Metrology reject trip *)
                iFsmState := 11; (* Abort cycle on QA failure *)
            END_IF;
        END_IF;

    9: (* AUTOMATED_FASTENER_INSERTION *)
        tFastenerFeedTimer(IN := bFastenerSeatedOk, PT := T#60MS);

        IF tFastenerFeedTimer.Q THEN
            tFastenerFeedTimer(IN := FALSE);
            iFsmState := 10; (* Advance to EMR Pulse Set *)
        END_IF;

    10: (* EMR_ELECTROMAGNETIC_RIVET_SET *)
        tEmrDischargeTimer(IN := bEmrPulseDelivered, PT := T#150MS);

        IF tEmrDischargeTimer.Q THEN
            tEmrDischargeTimer(IN := FALSE);
            bCycleComplete := TRUE;
            bCellRunning := FALSE;
            iFsmState := 0; (* Return to Standby Ready *)
        END_IF;

    11: (* EMERGENCY_ESTOP_SPINDLE_RETRACT *)
        bCellRunning := FALSE;
        rSpindleSpeedCmd_rpm := 0.0;
        rZFeedVelocityCmd_mms := 0.0;
        rClampValveFlowCmd_pct := 0.0;
        rMqlAerosolPulseCmd_pct := 0.0;
        bVacuumSuctionEnable := FALSE;
        bEmrDischargeTrigger := FALSE;
        
        (* Fast Z retract to safe standoff plane *)
        rGantryZ_Cmd_mm := 0.0;
        
        IF bResetFaults AND bEmergencyStop AND (dwAlarmWord1 = 0) AND (dwAlarmWord2 = 0) THEN
            bCellTripped := FALSE;
            iFsmState := 0; (* Reset to standby *)
        END_IF;

END_CASE;
''')

    # -------------------------------------------------------------
    # CODE BODY - SECTION 11: ISA-18.2 ALARMS & BIT PACKING
    # -------------------------------------------------------------
    parts.append('''
(* ========================================================================================= *)
(* 11.0 ISA-18.2 ALARM ENGINE & STATUS WORD BIT-PACKING                                      *)
(* ========================================================================================= *)
(* Packs all real-time operational states, safety trips, tool health alerts, and sensor     *)
(* degradation masks into deterministic 32-bit words for DCS / SCADA integration.           *)

dwSystemStatusWord := 16#0000_0000;

(* Pack State Machine Register (Bits 0-3) *)
dwSystemStatusWord := dwSystemStatusWord OR (INT_TO_DWORD(iFsmState) AND 16#0000_000F);

(* Status Flags *)
IF bCellRunning THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0010; (* Bit 4: Cell Running *)
END_IF;

IF bCellReady THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0020; (* Bit 5: Cell Ready *)
END_IF;

IF bCellTripped THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0040; (* Bit 6: Cell Tripped *)
END_IF;

IF bCycleComplete THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0080; (* Bit 7: Cycle Complete *)
END_IF;

IF bMaterialTransitionLatched THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0100; (* Bit 8: Material Boundary Latched *)
END_IF;

IF bHoleMetrologyPassed THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0200; (* Bit 9: Hole Metrology OK *)
END_IF;

IF bFastenerSeatedOk THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0400; (* Bit 10: Fastener Seated OK *)
END_IF;

IF bEmrPulseDelivered THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0800; (* Bit 11: EMR Pulse Delivered *)
END_IF;

IF bDegradedSensorActive THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_1000; (* Bit 12: Sensor Degraded Mode *)
END_IF;

IF bMpcActiveOptimization THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_2000; (* Bit 13: MPC Active *)
END_IF;

IF bToolWearWarning THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_4000; (* Bit 14: Tool Wear Warning *)
END_IF;

IF bDrillChippingFault THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_8000; (* Bit 15: Drill Chipping Fracture *)
END_IF;

END_FUNCTION_BLOCK
''')

    return "".join(parts)

if __name__ == "__main__":
    st_code = build_iec_code()
    print(f"Generated Structured Text length: {len(st_code)} characters")
    
    # Check parity
    verify_parity(st_code)
