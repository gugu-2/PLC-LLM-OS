FUNCTION_BLOCK FB_Plastics_InjectionMolding_CavityPressureVPOvershoot
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * ARCHITECTURAL GRADE : Advanced Plastics & High-Performance Polymer Processing (Tier 1 Global Industrial Sector)
 * COMMERCIAL SYSTEM    : 1,600-Ton All-Electric Multi-Cavity Precision Injection Molding Machine
 * CORE SUBSYSTEMS      :
 *   1. In-Mold Cavity Piezoelectric Sensor V/P Switchover Cascade (Velocity-to-Pressure Holding Transfer)
 *      - Sub-millisecond quartz piezoelectric sensor acquisition (Kistler/Priamus dynamic melt front detection)
 *      - Real-time dP/dt rate-of-rise and cavity pressure integral switchover criteria with anti-overshoot dampening
 *   2. Tie-Bar Strain Gauge Dynamic Clamp Tonnage Balancing & Thermal Mold Expansion Compensation
 *      - 4-Channel full-bridge extensometer instrumentation on 220 mm alloy tie-bars (16,000 kN lockup tonnage)
 *      - Active platen parallelism angular tilt compensation (horizontal, vertical, diagonal torsional deflection)
 *      - Closed-loop servo mold height ballscrew adjustment for thermal platen expansion (alpha = 12.0e-6 m/m-K)
 *   3. 8-Zone Ceramic Barrel Heating with Non-Linear Melt Shear Viscosity Feedforward (Cross-WLF Rheology)
 *      - Temperature regulation across Feed, Transition, Metering, and Hot-Runner Nozzle (200 - 380 deg C)
 *      - Dynamic shear rate calculation in screw channel and shear heating energy dissipation feedforward (Q_visc)
 *   4. Servo Toggle Clamp Resolver Synchronization & High-Speed Pneumatic Ejector Array
 *      - 5-Point double toggle kinematic resolver synchronization with S-curve jerk-limited trajectory profiling
 *      - Ultra-sensitive Low-Pressure Mold Protection (LPMP < 5.0 bar platen force) anti-crush safety
 *      - High-speed pulsed pneumatic parts ejector array and Euromap 67 / SPI 3-axis robot take-out handshake
 *
 * GOVERNING STANDARDS  : IEC 61131-3 3rd Ed., ISA-18.2 Alarm Management, EUROMAP 67 / 77, ISO 20430 Safety of IMM
 * TARGET PLATFORMS     : Siemens S7-1500 / Allen-Bradley ControlLogix 5580 / Beckhoff TwinCAT 3 / B&R APC
 * CONTROLLER SCAN TIME : Ts = 1.0 ms (1,000 Hz deterministic servo task cycle)
 * ===================================================================================================================== *)

VAR_INPUT
    (* --- 2oo3 TMR Sensor Channels: In-Mold Piezoelectric Cavity Pressure --- *)
    rCavityPres_TransA_In        : REAL;    (* Cavity Pressure Transducer Channel A (Piezoelectric Quartz Gate Pin) [bar] *)
    rCavityPres_TransB_In        : REAL;    (* Cavity Pressure Transducer Channel B (Piezoelectric Quartz Gate Pin) [bar] *)
    rCavityPres_TransC_In        : REAL;    (* Cavity Pressure Transducer Channel C (Piezoelectric Quartz Gate Pin) [bar] *)

    (* --- 2oo3 TMR Sensor Channels: Nozzle Melt Injection Pressure --- *)
    rMeltPres_NozzleA_In         : REAL;    (* Nozzle Melt Pressure Sensor Channel A (Extruder Tip Diaphragm) [bar] *)
    rMeltPres_NozzleB_In         : REAL;    (* Nozzle Melt Pressure Sensor Channel B (Extruder Tip Diaphragm) [bar] *)
    rMeltPres_NozzleC_In         : REAL;    (* Nozzle Melt Pressure Sensor Channel C (Extruder Tip Diaphragm) [bar] *)

    (* --- 2oo3 TMR Sensor Channels: Injection Screw Axial Position --- *)
    rScrewPos_LinearEncA_In      : REAL;    (* Screw Axial Position Absolute Optical Scale Channel A [mm] *)
    rScrewPos_LinearEncB_In      : REAL;    (* Screw Axial Position Absolute Optical Scale Channel B [mm] *)
    rScrewPos_LinearEncC_In      : REAL;    (* Screw Axial Position Absolute Optical Scale Channel C [mm] *)

    (* --- 2oo3 TMR Sensor Channels: Extruder Bulk Melt Temperature --- *)
    rMeltTemp_ThermocoupleA_In   : REAL;    (* Extruder Tip Melt Thermocouple Channel A (Mineral Insulated Type-J) [deg C] *)
    rMeltTemp_ThermocoupleB_In   : REAL;    (* Extruder Tip Melt Thermocouple Channel B (Mineral Insulated Type-J) [deg C] *)
    rMeltTemp_ThermocoupleC_In   : REAL;    (* Extruder Tip Melt Thermocouple Channel C (Mineral Insulated Type-J) [deg C] *)

    (* --- 4-Channel Tie-Bar Extensometer Strain Gauges (Platen Balancing) --- *)
    rTieBar_Strain_CH1_In        : REAL;    (* Tie-Bar 1 Top-Operator Strain Extensometer [um] *)
    rTieBar_Strain_CH2_In        : REAL;    (* Tie-Bar 2 Top-NonOperator Strain Extensometer [um] *)
    rTieBar_Strain_CH3_In        : REAL;    (* Tie-Bar 3 Bottom-Operator Strain Extensometer [um] *)
    rTieBar_Strain_CH4_In        : REAL;    (* Tie-Bar 4 Bottom-NonOperator Strain Extensometer [um] *)

    (* --- 8-Zone Ceramic Barrel Heating Temperatures --- *)
    rBarrelTemp_Zone1_Feed_In    : REAL;    (* Barrel Zone 1 Feed Throat Ceramic Band Temperature [deg C] *)
    rBarrelTemp_Zone2_Rear_In    : REAL;    (* Barrel Zone 2 Rear Compression Band Temperature [deg C] *)
    rBarrelTemp_Zone3_MidRear_In : REAL;    (* Barrel Zone 3 Middle-Rear Plasticizing Temperature [deg C] *)
    rBarrelTemp_Zone4_Middle_In  : REAL;    (* Barrel Zone 4 Middle Plasticizing Temperature [deg C] *)
    rBarrelTemp_Zone5_MidFront_In: REAL;    (* Barrel Zone 5 Middle-Front Homogenizing Temperature [deg C] *)
    rBarrelTemp_Zone6_Front_In   : REAL;    (* Barrel Zone 6 Front Metering Temperature [deg C] *)
    rBarrelTemp_Zone7_Adapter_In : REAL;    (* Barrel Zone 7 Nozzle Adapter Body Temperature [deg C] *)
    rBarrelTemp_Zone8_Nozzle_In  : REAL;    (* Barrel Zone 8 High-Speed Injection Nozzle Tip Temperature [deg C] *)

    (* --- Auxiliary Process Transducers & Cooling Utilities --- *)
    rHydraulic_BackPres_In       : REAL;    (* Proportional Back-Pressure Hydraulic/Servo Sensor [bar] *)
    rMoldWater_InletTemp_In      : REAL;    (* Mold Cooling Water Supply Manifold Temperature [deg C] *)
    rMoldWater_FlowRate_In       : REAL;    (* Mold Cooling Water Total Volumetric Flow Rate [l/min] *)
    rPlaten_MetalTemp_In         : REAL;    (* Moving Platen Core Structural Steel Temperature [deg C] *)
    rMoldCavity_CoreTemp_In      : REAL;    (* Mold Fixed Core Cavity Surface Thermocouple [deg C] *)

    (* --- Supervisory Commands & Recipe Setpoints --- *)
    bCmd_CycleStart_In           : BOOL;    (* Master Automatic Molding Cycle Start Command [bool] *)
    bCmd_EmergencyStop_In        : BOOL;    (* Master Hardwired Emergency Stop E-Stop Interlock [bool] *)
    bCmd_ManualPurge_In          : BOOL;    (* Manual High-Speed Screw Purge / Decontamination Command [bool] *)
    bCmd_ResetAlarms_In          : BOOL;    (* Master Alarm Reset and Latch Acknowledge Command [bool] *)
    rRecipe_ShotVolume_In        : REAL;    (* Target Shot Dosing Volumetric Stroke Setpoint [mm] *)
    rRecipe_InjSpeed_Max_In      : REAL;    (* Maximum Primary Stage Injection Velocity Setpoint [mm/s] *)
    rRecipe_CavityVPOvershoot_In : REAL;    (* In-Mold Cavity Pressure V/P Switchover Setpoint [bar] *)
    rRecipe_HoldPressure_In      : REAL;    (* Target Stage 1 Packing & Holding Pressure Setpoint [bar] *)
    rRecipe_HoldTime_In          : REAL;    (* Total Multi-Stage Holding Pressure Duration Setpoint [s] *)
    rRecipe_CoolingTime_In       : REAL;    (* In-Mold Solidification Cooling Duration Setpoint [s] *)
    rRecipe_ClampTonnage_In      : REAL;    (* Clamping Force Lockup Target Tonnage Setpoint [kN] *)
    rRecipe_BackPressure_In      : REAL;    (* Dosing Plasticizing Target Melt Back Pressure [bar] *)
    rRecipe_ScrewRPM_In          : REAL;    (* Dosing Extruder Screw Rotational Velocity Setpoint [RPM] *)

    (* --- Machine Safety Interlocks & Euromap 67 Robot Interface --- *)
    bSafetyGate_FrontClosed_In   : BOOL;    (* Operator Front Safety Enclosure Interlock Closed [bool] *)
    bSafetyGate_RearClosed_In    : BOOL;    (* Non-Operator Rear Safety Door Interlock Closed [bool] *)
    bRobot_PermissiveToClose_In  : BOOL;    (* Euromap 67 Robot Home / Permissive to Close Mold [bool] *)
    bRobot_PartStrippedConfirm_In: BOOL;    (* Euromap 67 Vacuum Grip Confirmation Part Removed [bool] *)
    bOptical_PartDropVerified_In : BOOL;    (* Mold Freefall Optical Light Curtain Part Ejection Detection [bool] *)
    bPneumatics_AirPressureOK_In : BOOL;    (* Pneumatics Main Air Supply Pressure OK (> 6.0 bar) [bool] *)
END_VAR

VAR_OUTPUT
    (* --- Servo Actuator Analog Output Commands --- *)
    rServo_InjVelocity_Cmd_Out   : REAL;    (* Closed-Loop Injection Servo Velocity Command [mm/s] *)
    rServo_HoldPressure_Cmd_Out  : REAL;    (* Closed-Loop Holding / Packing Pressure Command [bar] *)
    rServo_ScrewRPM_Cmd_Out      : REAL;    (* Plasticizing Extruder Screw Drive Velocity Command [RPM] *)
    rServo_BackPressure_Cmd_Out  : REAL;    (* Closed-Loop Melt Dosing Back-Pressure Command [bar] *)
    rServo_ClampTonnage_Cmd_Out  : REAL;    (* Servo Toggle Clamping Force Command [kN] *)
    rServo_ClampVelocity_Cmd_Out : REAL;    (* Servo Toggle Moving Platen Traverse Velocity Command [mm/s] *)
    rServo_EjectorStroke_Cmd_Out : REAL;    (* High-Speed Servo/Hydraulic Ejector Plate Position Command [mm] *)
    rServo_MoldHeight_Delta_Out  : REAL;    (* Mold Height Adjustment Gear Motor Closed-Loop Trim [mm] *)

    (* --- 8-Zone Barrel Ceramic Band PWM Duty Cycle Outputs --- *)
    rHeaterDuty_Zone1_Out        : REAL;    (* Zone 1 Feed Throat Solid State Relay PWM Duty Cycle [%] *)
    rHeaterDuty_Zone2_Out        : REAL;    (* Zone 2 Rear Compression SSR PWM Duty Cycle [%] *)
    rHeaterDuty_Zone3_Out        : REAL;    (* Zone 3 Middle-Rear Plasticizing SSR PWM Duty Cycle [%] *)
    rHeaterDuty_Zone4_Out        : REAL;    (* Zone 4 Middle Plasticizing SSR PWM Duty Cycle [%] *)
    rHeaterDuty_Zone5_Out        : REAL;    (* Zone 5 Middle-Front Homogenizing SSR PWM Duty Cycle [%] *)
    rHeaterDuty_Zone6_Out        : REAL;    (* Zone 6 Front Metering SSR PWM Duty Cycle [%] *)
    rHeaterDuty_Zone7_Out        : REAL;    (* Zone 7 Nozzle Adapter Body SSR PWM Duty Cycle [%] *)
    rHeaterDuty_Zone8_Out        : REAL;    (* Zone 8 Injection Nozzle Tip SSR PWM Duty Cycle [%] *)

    (* --- Digital Pneumatic Actuation & Interlock Signals --- *)
    bPneumatic_CorePull1_Fwd_Out : BOOL;    (* Mold Hydraulic/Pneumatic Side Core Puller 1 Advance [bool] *)
    bPneumatic_CorePull2_Fwd_Out : BOOL;    (* Mold Hydraulic/Pneumatic Side Core Puller 2 Advance [bool] *)
    bPneumatic_AirEjectBlast_Out : BOOL;    (* High-Pressure Mold Air Poppet Valve Part Stripping Pulse [bool] *)
    bRobot_PermissiveToEnter_Out : BOOL;    (* Euromap 67 Signal: Mold Fully Open, Robot Enter Safe [bool] *)
    bRobot_CycleComplete_Out     : BOOL;    (* Euromap 67 Signal: Injection Cycle Finished Pulse [bool] *)
    bMachine_CycleActive_Out     : BOOL;    (* Machine Auto Molding Sequence Active Status [bool] *)
    bTrip_EmergencyLockout_Out   : BOOL;    (* Master Critical Safety Emergency Lockout Trip [bool] *)

    (* --- Process Analytics & V/P Cascade Metrics --- *)
    rMeltViscosity_Shear_Out     : REAL;    (* Real-Time Estimated Polymer Shear Melt Viscosity [Pa.s] *)
    rCavity_PeakOvershoot_Out    : REAL;    (* Peak Dynamic In-Mold Cavity Pressure Overshoot [bar] *)
    rCycle_ActualTime_Out        : REAL;    (* Total Running Time of Active Production Cycle [s] *)
    rPlaten_ParallelismTilt_Out  : REAL;    (* Calculated Moving Platen Angular Deflection Tilt [um] *)

    (* --- 32-Bit Bit-Packed Diagnostic Status and Alarm Words --- *)
    dwStatusWord_Machine_Out     : DWORD;   (* 32-Bit Operating FSM State, Safety, and Sequence Flags *)
    dwStatusWord_TMR_Out         : DWORD;   (* 32-Bit 2oo3 TMR Sensor Redundancy & Health Status *)
    dwAlarmWord_Trip_Out         : DWORD;   (* 32-Bit Critical ISA-18.2 Process Trips (Immediate Lockout) *)
    dwAlarmWord_Warning_Out      : DWORD;   (* 32-Bit High/Low Process Warnings & Discrepancies *)
    dwDiagnosticWord_MPC_Out     : DWORD;   (* 32-Bit Receding-Horizon MPC Optimization Status Flags *)
END_VAR
