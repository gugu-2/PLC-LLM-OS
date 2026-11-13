FUNCTION_BLOCK FB_Plastics_TwinScrewExtrusion_Compounding_MeltPressure
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * ARCHITECTURAL GRADE : Advanced Plastics, Polymers & High-Performance Compounding (Tier 1 Priority Sector)
 * TARGET SYSTEM       : High-Output Co-Rotating Twin-Screw Extruder (133 mm Screw Diameter, 48:1 L/D Ratio)
 * APPLICATION         : Reinforced Engineering Thermoplastics Compounding (Polyamide 66 + 30% Glass Fiber + Flame Retardant)
 *
 * CORE CYBER-PHYSICAL SUBSYSTEMS INTEGRATED:
 *   1. 12-Zone Barrel Temperature Cascade & Dynamic Non-Linear Shear Heating Decoupling:
 *      - 12 individual barrel zone induction/ceramic band heating zones with closed-loop cooling jackets.
 *      - Feed throat zone 1 water-cooled to prevent premature polymer pellet bridge agglomeration.
 *      - Non-linear viscous dissipation heat generation modeling (Q_visc = tau * gamma_dot = eta * gamma_dot^2).
 *      - Dynamic feedforward decoupling of screw shear power from external heating duty cycles to avoid degradation.
 *   2. Multi-Feeder Gravimetric Loss-in-Weight (LIW) Ratio Cascade:
 *      - Feeder 1: Primary PA66 polymer resin pellets (50 - 1500 kg/h).
 *      - Feeder 2: Toughening elastomer / impact modifier pellets (10 - 250 kg/h).
 *      - Feeder 3: Halogen-free flame retardant powder (10 - 350 kg/h).
 *      - Feeder 4: Color masterbatch / carbon black micro-pellets (1 - 50 kg/h).
 *      - Feeder 5: Downstream twin-screw side-feeder for chopped strand / roving glass fibers (50 - 900 kg/h).
 *   3. Melt Gear Pump Synchronous Speed & Suction Melt Pressure Closed-Loop MPC Regulation:
 *      - Positive displacement melt gear pump (450 cm3/rev) buffering die head against extruder screw surging.
 *      - Receding-horizon Model Predictive Control (MPC) with Projected Gradient Descent (PGD) unrolled solver.
 *      - Decoupling twin-screw drive speed (0 - 600 rpm, 800 kW) from gear pump servo drive (0 - 85 rpm, 110 kW).
 *      - Real-time regulation of suction pressure to 45.0 bar +/- 1.0 bar to guarantee full tooth filling without cavitation.
 *   4. Zone 9 High-Vacuum Volatile Degassing Skid:
 *      - Dual-stage Roots blower and liquid ring vacuum pump skid (-0.95 bar vacuum).
 *      - Entrainment moisture and residual monomer removal with differential pressure trap monitoring.
 *   5. Underwater Strand / Pelletizer System (UWP) & Tempered Water Circulation Loop:
 *      - Variable speed cutter hub (1000 - 4500 rpm) with hydraulic water box clamping against multi-orifice die plate.
 *      - Tempered water circulation loop (60 - 85 deg C) with plate heat exchanger and electrical trim immersion heater.
 *      - Automated 3-way water bypass diverter valve preventing cold freeze-off at die plate start-up.
 *   6. 2oo3 Triple Modular Redundancy (TMR) Sensor Architecture:
 *      - Triplicated Die Melt Pressure transducers (PT-101A/B/C).
 *      - Triplicated Adapter Melt Temperature thermocouples (TT-201A/B/C).
 *      - Triplicated Extruder Screw Drive Torque strain transducers (TT-301A/B/C).
 *      - Triplicated Pelletizer Water Temperature RTDs (TT-401A/B/C).
 *      - Bumpless median voting, pairwise discrepancy timers, and automatic degradation to dual/simplex/observer fallback.
 *   7. Deterministic 14-Stage Operational Finite State Machine (FSM):
 *      - Barrel cold soak pre-heating, equilibrium soak hold, feeder calibration check, screw inching purge,
 *        gravimetric feed ramp, side-feeder glass fiber introduction, vacuum degassing pull, die melt pressure build-up,
 *        gear pump synchronization, underwater pelletizer spin & water box close, continuous compounding production,
 *        die flush & purge compound transition, controlled barrel cooling, and emergency motor torque overload trip.
 *   8. ISA-18.2 Multi-Tier Alarm Management:
 *      - High-High (HH), High (H), Low (L), Low-Low (LL) trip/warn thresholds with deadband hysteresis.
 *      - Bit-packed DWORD diagnostic registers and rupture disc fail-safe overpressure protection.
 *
 * GOVERNING INDUSTRIAL STANDARDS:
 *   - IEC 61131-3 3rd Ed. (Programmable Controllers - Programming Languages)
 *   - ISA-18.2 / IEC 62682 (Management of Alarm Systems for the Process Industries)
 *   - EN 1114-1 (Plastics and Rubber Machines - Safety Requirements for Extruders)
 *   - EUROMAP 27 / 77 (Extruder Interface & Industry 4.0 Protocol)
 *
 * CONTROLLER SCAN EXECUTION:
 *   - Deterministic Cycle Time: Ts = 0.020 s (20.0 ms / 50 Hz cyclic automation task)
 * ===================================================================================================================== *)

VAR_INPUT
    (* --- 2oo3 TMR Triplicated Sensor Inputs: Die Head Melt Pressure PT-101 --- *)
    rDieMeltPres_SensA_In        : REAL;    (* Die Melt Pressure Transducer Channel A (Diaphragm Piezo) [bar] *)
    rDieMeltPres_SensB_In        : REAL;    (* Die Melt Pressure Transducer Channel B (Diaphragm Piezo) [bar] *)
    rDieMeltPres_SensC_In        : REAL;    (* Die Melt Pressure Transducer Channel C (Diaphragm Piezo) [bar] *)

    (* --- 2oo3 TMR Triplicated Sensor Inputs: Adapter Polymer Melt Temperature TT-201 --- *)
    rMeltTemp_SensA_In           : REAL;    (* Adapter Melt Temperature Thermocouple Channel A (Immersion Probe) [°C] *)
    rMeltTemp_SensB_In           : REAL;    (* Adapter Melt Temperature Thermocouple Channel B (Immersion Probe) [°C] *)
    rMeltTemp_SensC_In           : REAL;    (* Adapter Melt Temperature Thermocouple Channel C (Immersion Probe) [°C] *)

    (* --- 2oo3 TMR Triplicated Sensor Inputs: Extruder Drive Shaft Torque TT-301 --- *)
    rScrewTorque_SensA_In        : REAL;    (* Main Extruder Drive Shaft Torque Transducer Channel A [Nm] *)
    rScrewTorque_SensB_In        : REAL;    (* Main Extruder Drive Shaft Torque Transducer Channel B [Nm] *)
    rScrewTorque_SensC_In        : REAL;    (* Main Extruder Drive Shaft Torque Transducer Channel C [Nm] *)

    (* --- 2oo3 TMR Triplicated Sensor Inputs: Pelletizer Water Loop Temperature TT-401 --- *)
    rPelletWaterTemp_SensA_In    : REAL;    (* Pelletizer Supply Water Temperature RTD Channel A [°C] *)
    rPelletWaterTemp_SensB_In    : REAL;    (* Pelletizer Supply Water Temperature RTD Channel B [°C] *)
    rPelletWaterTemp_SensC_In    : REAL;    (* Pelletizer Supply Water Temperature RTD Channel C [°C] *)

    (* --- 12-Zone Barrel Temperature RTD Feedbacks (Zones 1 through 12) --- *)
    rZoneTemp_Act_Z01_In         : REAL;    (* Barrel Zone 01 (Feed Throat Section) Temperature [°C] *)
    rZoneTemp_Act_Z02_In         : REAL;    (* Barrel Zone 02 (Solids Conveying Section) Temperature [°C] *)
    rZoneTemp_Act_Z03_In         : REAL;    (* Barrel Zone 03 (Primary Plasticizing / Kneading) Temperature [°C] *)
    rZoneTemp_Act_Z04_In         : REAL;    (* Barrel Zone 04 (Melt Homogenization Section) Temperature [°C] *)
    rZoneTemp_Act_Z05_In         : REAL;    (* Barrel Zone 05 (Side-Feeder Glass Port) Temperature [°C] *)
    rZoneTemp_Act_Z06_In         : REAL;    (* Barrel Zone 06 (Filler Dispersive Mixing) Temperature [°C] *)
    rZoneTemp_Act_Z07_In         : REAL;    (* Barrel Zone 07 (Thermal Conditioning Section) Temperature [°C] *)
    rZoneTemp_Act_Z08_In         : REAL;    (* Barrel Zone 08 (Atmospheric Vent Section) Temperature [°C] *)
    rZoneTemp_Act_Z09_In         : REAL;    (* Barrel Zone 09 (Vacuum Degassing Chamber) Temperature [°C] *)
    rZoneTemp_Act_Z10_In         : REAL;    (* Barrel Zone 10 (Pumping & Metering Section) Temperature [°C] *)
    rZoneTemp_Act_Z11_In         : REAL;    (* Barrel Zone 11 (Screen Changer Entrance) Temperature [°C] *)
    rZoneTemp_Act_Z12_In         : REAL;    (* Barrel Zone 12 (Gear Pump Adapter Transition) Temperature [°C] *)

    (* --- 12-Zone Barrel Temperature Recipe Setpoints (Zones 1 through 12) --- *)
    rZoneTemp_SP_Z01_In          : REAL;    (* Recipe Target Temperature Setpoint Barrel Zone 01 [°C] *)
    rZoneTemp_SP_Z02_In          : REAL;    (* Recipe Target Temperature Setpoint Barrel Zone 02 [°C] *)
    rZoneTemp_SP_Z03_In          : REAL;    (* Recipe Target Temperature Setpoint Barrel Zone 03 [°C] *)
    rZoneTemp_SP_Z04_In          : REAL;    (* Recipe Target Temperature Setpoint Barrel Zone 04 [°C] *)
    rZoneTemp_SP_Z05_In          : REAL;    (* Recipe Target Temperature Setpoint Barrel Zone 05 [°C] *)
    rZoneTemp_SP_Z06_In          : REAL;    (* Recipe Target Temperature Setpoint Barrel Zone 06 [°C] *)
    rZoneTemp_SP_Z07_In          : REAL;    (* Recipe Target Temperature Setpoint Barrel Zone 07 [°C] *)
    rZoneTemp_SP_Z08_In          : REAL;    (* Recipe Target Temperature Setpoint Barrel Zone 08 [°C] *)
    rZoneTemp_SP_Z09_In          : REAL;    (* Recipe Target Temperature Setpoint Barrel Zone 09 [°C] *)
    rZoneTemp_SP_Z10_In          : REAL;    (* Recipe Target Temperature Setpoint Barrel Zone 10 [°C] *)
    rZoneTemp_SP_Z11_In          : REAL;    (* Recipe Target Temperature Setpoint Barrel Zone 11 [°C] *)
    rZoneTemp_SP_Z12_In          : REAL;    (* Recipe Target Temperature Setpoint Barrel Zone 12 [°C] *)

    (* --- Melt Gear Pump Flange Pressures --- *)
    rGearPump_SuctPres_In        : REAL;    (* Melt Gear Pump Suction Housing Pressure PT-102 [bar] *)
    rGearPump_DischPres_In       : REAL;    (* Melt Gear Pump Discharge Delivery Pressure PT-103 [bar] *)

    (* --- Drive Motion & Mechanical Feedbacks --- *)
    rScrewSpeed_Act_In           : REAL;    (* Extruder Screw Drive Shaft Tachometer Feedback [rpm] *)
    rScrewMotor_Current_In       : REAL;    (* Main Extruder AC Inverter RMS Stator Current [A] *)
    rGearPumpSpeed_Act_In        : REAL;    (* Melt Gear Pump Servo Resolver Actual Speed [rpm] *)
    rGearPump_Torque_In          : REAL;    (* Melt Gear Pump Servo Shaft Actual Torque [Nm] *)

    (* --- Gravimetric Loss-in-Weight (LIW) Feeders Actual Mass Flow Rates --- *)
    rFeeder_ActFlow_01_In        : REAL;    (* Feeder 01 Primary Resin Pellet Mass Flow Rate [kg/h] *)
    rFeeder_ActFlow_02_In        : REAL;    (* Feeder 02 Impact Modifier Elastomer Mass Flow Rate [kg/h] *)
    rFeeder_ActFlow_03_In        : REAL;    (* Feeder 03 Flame Retardant Powder Mass Flow Rate [kg/h] *)
    rFeeder_ActFlow_04_In        : REAL;    (* Feeder 04 Color Masterbatch Pellet Mass Flow Rate [kg/h] *)
    rFeeder_ActFlow_05_In        : REAL;    (* Feeder 05 Glass Fiber Side-Feeder Mass Flow Rate [kg/h] *)

    (* --- Gravimetric Loss-in-Weight (LIW) Feeders Target Recipe Mass Flow Rates --- *)
    rFeeder_SP_Flow_01_In        : REAL;    (* Recipe Setpoint Mass Flow Rate Feeder 01 [kg/h] *)
    rFeeder_SP_Flow_02_In        : REAL;    (* Recipe Setpoint Mass Flow Rate Feeder 02 [kg/h] *)
    rFeeder_SP_Flow_03_In        : REAL;    (* Recipe Setpoint Mass Flow Rate Feeder 03 [kg/h] *)
    rFeeder_SP_Flow_04_In        : REAL;    (* Recipe Setpoint Mass Flow Rate Feeder 04 [kg/h] *)
    rFeeder_SP_Flow_05_In        : REAL;    (* Recipe Setpoint Mass Flow Rate Feeder 05 [kg/h] *)

    (* --- Auxiliary Process Sensors & Vacuum System --- *)
    rVacuumPres_FB_In            : REAL;    (* Barrel Zone 09 Vacuum Port Absolute Pressure [bar] *)
    rPelletCutter_Speed_FB_In    : REAL;    (* Underwater Pelletizer Cutter Hub Actual Speed [rpm] *)
    rPelletWater_Flow_FB_In      : REAL;    (* Pelletizer Water Circulation Volumetric Flow Rate [m3/h] *)
    rPelletWater_Pres_FB_In      : REAL;    (* Pelletizer Water Box Chamber Manifold Pressure [bar] *)

    (* --- Safety Interlocks & Discrete Plant Signals --- *)
    bRuptureDisc_Intact_In       : BOOL;    (* Rupture Disc Safety Sensor Loop (Fail-Safe True = Intact) [BOOL] *)
    bSafetyLine_Healthy_In       : BOOL;    (* Master Emergency Stop Safety Line Relay Closed [BOOL] *)
    bMasterEnable_In             : BOOL;    (* Master Supervisory Automation Run Enable Command [BOOL] *)
    bAutoMode_Cmd_In             : BOOL;    (* Operator Automatic Production Sequence Start Request [BOOL] *)
    bAlarmReset_Cmd_In           : BOOL;    (* Operator Master Alarm Acknowledge & Reset Command [BOOL] *)
    bPurgeMode_Cmd_In            : BOOL;    (* Extruder Purging & Material Transition Cycle Request [BOOL] *)
    bControlledStop_Cmd_In       : BOOL;    (* Operator Controlled Ramp-Down & Thermal Hold Request [BOOL] *)
END_VAR

VAR_OUTPUT
    (* --- Primary Drive Speed Actuator References --- *)
    rScrewSpeed_Cmd_Out          : REAL;    (* Extruder Screw Drive Master Speed Reference Command [rpm] *)
    rGearPumpSpeed_Cmd_Out       : REAL;    (* Melt Gear Pump Master Speed Reference Command [rpm] *)
    rSideFeederSpeed_Cmd_Out     : REAL;    (* Glass Fiber Side-Feeder Drive Speed Command [rpm] *)
    rPelletCutterSpeed_Cmd_Out   : REAL;    (* Underwater Pelletizer Cutter Motor Speed Command [rpm] *)

    (* --- 12-Zone Barrel Electric Heater PWM Duty Cycle Demands --- *)
    rZoneHeat_Cmd_Z01_Out        : REAL;    (* Zone 01 Barrel Heating Duty Cycle Demand (Feed Throat) [%] *)
    rZoneHeat_Cmd_Z02_Out        : REAL;    (* Zone 02 Barrel Heating Duty Cycle Demand (Solids Conveying) [%] *)
    rZoneHeat_Cmd_Z03_Out        : REAL;    (* Zone 03 Barrel Heating Duty Cycle Demand (Kneading/Melting) [%] *)
    rZoneHeat_Cmd_Z04_Out        : REAL;    (* Zone 04 Barrel Heating Duty Cycle Demand (Homogenization) [%] *)
    rZoneHeat_Cmd_Z05_Out        : REAL;    (* Zone 05 Barrel Heating Duty Cycle Demand (Glass Fiber Port) [%] *)
    rZoneHeat_Cmd_Z06_Out        : REAL;    (* Zone 06 Barrel Heating Duty Cycle Demand (Dispersive Mixing) [%] *)
    rZoneHeat_Cmd_Z07_Out        : REAL;    (* Zone 07 Barrel Heating Duty Cycle Demand (Conditioning) [%] *)
    rZoneHeat_Cmd_Z08_Out        : REAL;    (* Zone 08 Barrel Heating Duty Cycle Demand (Vent Section) [%] *)
    rZoneHeat_Cmd_Z09_Out        : REAL;    (* Zone 09 Barrel Heating Duty Cycle Demand (Vacuum Chamber) [%] *)
    rZoneHeat_Cmd_Z10_Out        : REAL;    (* Zone 10 Barrel Heating Duty Cycle Demand (Melt Pumping) [%] *)
    rZoneHeat_Cmd_Z11_Out        : REAL;    (* Zone 11 Barrel Heating Duty Cycle Demand (Screen Changer) [%] *)
    rZoneHeat_Cmd_Z12_Out        : REAL;    (* Zone 12 Barrel Heating Duty Cycle Demand (Adapter Flange) [%] *)

    (* --- 12-Zone Barrel Cooling Jacket Solenoid Valve Actuations --- *)
    bZoneCool_Cmd_Z01_Out        : BOOL;    (* Zone 01 Cooling Water Solenoid Valve Command [BOOL] *)
    bZoneCool_Cmd_Z02_Out        : BOOL;    (* Zone 02 Cooling Water Solenoid Valve Command [BOOL] *)
    bZoneCool_Cmd_Z03_Out        : BOOL;    (* Zone 03 Cooling Water Solenoid Valve Command [BOOL] *)
    bZoneCool_Cmd_Z04_Out        : BOOL;    (* Zone 04 Cooling Water Solenoid Valve Command [BOOL] *)
    bZoneCool_Cmd_Z05_Out        : BOOL;    (* Zone 05 Cooling Water Solenoid Valve Command [BOOL] *)
    bZoneCool_Cmd_Z06_Out        : BOOL;    (* Zone 06 Cooling Water Solenoid Valve Command [BOOL] *)
    bZoneCool_Cmd_Z07_Out        : BOOL;    (* Zone 07 Cooling Water Solenoid Valve Command [BOOL] *)
    bZoneCool_Cmd_Z08_Out        : BOOL;    (* Zone 08 Cooling Water Solenoid Valve Command [BOOL] *)
    bZoneCool_Cmd_Z09_Out        : BOOL;    (* Zone 09 Cooling Water Solenoid Valve Command [BOOL] *)
    bZoneCool_Cmd_Z10_Out        : BOOL;    (* Zone 10 Cooling Water Solenoid Valve Command [BOOL] *)
    bZoneCool_Cmd_Z11_Out        : BOOL;    (* Zone 11 Cooling Water Solenoid Valve Command [BOOL] *)
    bZoneCool_Cmd_Z12_Out        : BOOL;    (* Zone 12 Cooling Water Solenoid Valve Command [BOOL] *)

    (* --- Gravimetric Loss-in-Weight Feeders Master Mass Flow Commands --- *)
    rFeeder_CmdFlow_01_Out       : REAL;    (* LIW Feeder 01 Master Mass Flow Setpoint [kg/h] *)
    rFeeder_CmdFlow_02_Out       : REAL;    (* LIW Feeder 02 Master Mass Flow Setpoint [kg/h] *)
    rFeeder_CmdFlow_03_Out       : REAL;    (* LIW Feeder 03 Master Mass Flow Setpoint [kg/h] *)
    rFeeder_CmdFlow_04_Out       : REAL;    (* LIW Feeder 04 Master Mass Flow Setpoint [kg/h] *)
    rFeeder_CmdFlow_05_Out       : REAL;    (* LIW Feeder 05 Master Mass Flow Setpoint [kg/h] *)

    (* --- Auxiliary Process Equipment Controls --- *)
    bVacuumPump_Run_Out          : BOOL;    (* Vacuum Degassing Skid Roots & Liquid Ring Blower Run [BOOL] *)
    rVacuumThrottle_Cmd_Out      : REAL;    (* Vacuum Degassing Modulating Throttle Valve Demand [%] *)
    bWaterBox_Clamp_Out          : BOOL;    (* Underwater Pelletizer Hydraulic Water Box Clamp Solenoid [BOOL] *)
    bWaterBox_Diverter_Out       : BOOL;    (* Water Box 3-Way Diverter Valve (True = Process, False = Bypass) [BOOL] *)
    bWaterCircPump_Run_Out       : BOOL;    (* Pelletizer Tempered Water Loop Circulation Pump Run [BOOL] *)
    rWaterTrimHeat_Cmd_Out       : REAL;    (* Pelletizer Water Temperature Immersion Trim Heater Demand [%] *)
    bDieFastDump_Valve_Out       : BOOL;    (* Emergency Fast Die Depressurization Bypass Dump Valve [BOOL] *)

    (* --- 2oo3 TMR Validated Physical Process Signals --- *)
    rVoted_DieMeltPres_Out       : REAL;    (* 2oo3 TMR Voted Die Head Melt Pressure [bar] *)
    rVoted_MeltTemp_Out          : REAL;    (* 2oo3 TMR Voted Adapter Melt Temperature [°C] *)
    rVoted_ScrewTorque_Out       : REAL;    (* 2oo3 TMR Voted Extruder Screw Drive Shaft Torque [Nm] *)
    rVoted_PelletWaterTemp_Out   : REAL;    (* 2oo3 TMR Voted Pelletizer Water Loop Temperature [°C] *)

    (* --- Real-Time Cyber-Physical Compounding Metrics --- *)
    rTotalThroughput_Out         : REAL;    (* Total Compounding Output Mass Throughput [kg/h] *)
    rSpecificMechEnergy_Out      : REAL;    (* Specific Mechanical Energy (SME) Input [kWh/kg] *)
    rApparentViscosity_Out       : REAL;    (* Polymer Melt Dynamic Apparent Shear Viscosity [Pa*s] *)
    rShearHeatPower_Out          : REAL;    (* Viscous Dissipation Mechanical Heat Generation [kW] *)
    rDegreeOfFill_Out            : REAL;    (* Estimated Screw Channel Volumetric Degree of Fill [%] *)

    (* --- Finite State Machine Execution Tracking --- *)
    uiExtruderFSM_State_Out      : UINT;    (* Extruder Production Finite State Machine State ID [0..14] *)
    uiExtruderFSM_SubState_Out   : UINT;    (* Extruder Production Finite State Machine Sub-Phase ID [0..10] *)

    (* --- ISA-18.2 Bit-Packed Status & Diagnostic Registers --- *)
    dwExtruderStatusWord_01_Out  : DWORD;   (* Bit-Packed Extruder Operating Modes & Sequence Flags [DWORD] *)
    dwExtruderStatusWord_02_Out  : DWORD;   (* Bit-Packed Equipment Ready, Interlock & Drive Status [DWORD] *)
    dwExtruderStatusWord_03_Out  : DWORD;   (* Bit-Packed TMR Sensor Integrity & Channel Health States [DWORD] *)

    (* --- ISA-18.2 Bit-Packed Alarm & Trip Registers --- *)
    dwExtruderAlarmWord_01_Out   : DWORD;   (* Bit-Packed Priority 1 Critical Protective Safety Trips [DWORD] *)
    dwExtruderAlarmWord_02_Out   : DWORD;   (* Bit-Packed Priority 2 Process Out-of-Tolerance Warnings [DWORD] *)
    dwExtruderAlarmWord_03_Out   : DWORD;   (* Bit-Packed Priority 3 Hardware & Maintenance Advisory Alarms [DWORD] *)

    (* --- Model Predictive Control Performance Diagnostics --- *)
    rMPC_CostSuctPres_Out        : REAL;    (* MPC Objective Quadratic Loss on Suction Pressure [REAL] *)
    rMPC_PredMeltPres_Out        : REAL;    (* MPC Model-Predicted Future Die Melt Pressure [bar] *)
    bExtruderReady_Out           : BOOL;    (* Compounding Extrusion Line Interlocks Satisfied & Ready [BOOL] *)
    bTripInterlocked_Out         : BOOL;    (* Master Safety Trip Latched (Operator Reset Required) [BOOL] *)
END_VAR
