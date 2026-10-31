# Airport Baggage Handling EDS & Tray Sorter ST Generator
import os

def build_bhs_block():
    sections = []

    # ==========================================
    # SECTION 1: HEADER & INTERFACE DECLARATION
    # ==========================================
    sec1 = """FUNCTION_BLOCK FB_Airport_BaggageHandling_EDS_TraySorter
VAR_INPUT
    (* --- 2oo3 TMR Conveyor Shaft Pulse Encoders [pulses/s] --- *)
    rEncoder_ChA_PulseFreq_Hz   : REAL := 25000.0; (* Induction shaft encoder Channel A [pulses/s] *)
    rEncoder_ChB_PulseFreq_Hz   : REAL := 25000.0; (* Induction shaft encoder Channel B [pulses/s] *)
    rEncoder_ChC_PulseFreq_Hz   : REAL := 25000.0; (* Induction shaft encoder Channel C [pulses/s] *)
    rEncoder_PulsesPerMeter     : REAL := 10000.0; (* Calibration pulses per linear meter [p/m] *)
    
    (* --- 2oo3 TMR High-Speed Optical Induction Photocells --- *)
    bInduction_PE_ChA           : BOOL := FALSE;   (* Tracking photoeye Channel A *)
    bInduction_PE_ChB           : BOOL := FALSE;   (* Tracking photoeye Channel B *)
    bInduction_PE_ChC           : BOOL := FALSE;   (* Tracking photoeye Channel C *)
    rBag_CheckIn_Weight_kg      : REAL := 23.5;    (* Dynamic inline weigher payload mass [kg] *)
    rBag_Length_mm              : REAL := 750.0;   (* Optical profile baggage length [mm] *)
    rBag_Width_mm               : REAL := 480.0;   (* Optical profile baggage width [mm] *)
    rBag_Height_mm              : REAL := 320.0;   (* Optical profile baggage height [mm] *)
    
    (* --- 360-Degree Laser Scanner & RFID Bag Tag Inputs --- *)
    diScanned_IATA_BHS_TagID    : DINT := 10982734; (* Decoded 10-digit IATA barcode tag ID *)
    bBarcode_ReadValid          : BOOL := TRUE;     (* High-read rate 360-degree omni-scanner valid flag *)
    diFlight_AssignedChute_ID   : DINT := 14;       (* BHS Supervisory Host assigned chute ID [1..64] *)
    
    (* --- 2oo3 TMR In-Line EDS (Computed Tomography) Screening Interlocks --- *)
    bEDS_SecurityVerdict_ChA    : BOOL := TRUE;    (* EDS CT Level 1 Clear dry contact Ch A (TRUE=Clear) *)
    bEDS_SecurityVerdict_ChB    : BOOL := TRUE;    (* EDS CT Level 1 Clear dry contact Ch B (TRUE=Clear) *)
    bEDS_SecurityVerdict_ChC    : BOOL := TRUE;    (* EDS CT Level 1 Clear dry contact Ch C (TRUE=Clear) *)
    bEDS_Threat_Suspect_Bit     : BOOL := FALSE;   (* Level 2 Operator alarm suspicious baggage flag *)
    
    (* --- High-Speed Tray Sorter / Linear Synchronous Motor (LSM) Telemetry --- *)
    rTraySorter_LinearSpeed_mps : REAL := 7.5;     (* Main sorter track linear velocity [m/s] (0..12 m/s) *)
    rTray_ActualPosition_mm     : REAL := 0.0;     (* Sorter absolute carrier position on track [mm] *)
    rTray_PitchSpacing_mm       : REAL := 1400.0;  (* Nominal inter-tray mechanical pitch [mm] *)
    rLSM_DriveTemperature_degC  : REAL := 54.0;    (* Linear motor stator winding temperature [deg C] *)
    rLSM_ThrustCurrent_Amps     : REAL := 32.5;    (* Linear synchronous motor phase current [A] *)
    rTrack_CurveRadius_m        : REAL := 28.5;    (* Sorter rail horizontal bend radius [m] *)
    rLSM_BusVoltage_VDC         : REAL := 680.0;   (* Common DC bus voltage for LSM power inverters [V] *)
    
    (* --- High-Speed Pneumatic Divert Shoe Actuator Feedback --- *)
    rDivert_SupplyPress_bar     : REAL := 6.5;     (* Pneumatic header air supply pressure [bar] *)
    rDivertShoe_Position_mm     : REAL := 0.0;     (* Slat divert shoe transverse displacement [mm] *)
    bShoeHome_Sensor            : BOOL := TRUE;    (* Diverter shoe home position proximity switch *)
    bShoeDiverted_Sensor        : BOOL := FALSE;   (* Diverter shoe fully stroked proximity switch *)
    
    (* --- Chute Collation Matrix Sensors --- *)
    rChute_OpticalFillLevel_Pct : REAL := 35.0;    (* Destination flight chute volume fill [0..100 %] *)
    bChute_FullPhotoeye         : BOOL := FALSE;   (* Flight make-up chute backup jam optical photoeye *)
    
    (* --- Supervisory & Safety Inputs --- *)
    bSystemAuto_Run_Cmd         : BOOL := TRUE;    (* Master BHS line automatic mode enable *)
    bSafetyZone_Clear           : BOOL := TRUE;    (* Sorter zone Cat 4 / PLe safety perimeter intact *)
    bEmergencyStop_Active       : BOOL := FALSE;   (* Dual-channel hardware E-stop loop active (active low) *)
    bAlarmReset_PB              : BOOL := FALSE;   (* Master HMI operator alarm reset pushbutton *)
    tScanTime_s                 : REAL := 0.010;   (* Deterministic PLC cycle scan interval [s] *)
END_VAR

VAR_OUTPUT
    (* --- Metering & Induction Belt Drive Commands --- *)
    rInduction_BeltSpeed_mps    : REAL := 2.5;     (* Infeed pacing belt linear velocity command [m/s] *)
    rInfeedVFD_Frequency_Hz     : REAL := 42.5;    (* Metering belt VFD frequency command [Hz] *)
    bInduction_PacerBrake_Cmd   : BOOL := FALSE;   (* Fast-response friction brake on pacing conveyor *)
    
    (* --- In-Line EDS Screening Diverter Commands --- *)
    bEDS_RejectDiverter_Fire    : BOOL := FALSE;   (* High-speed pneumatic reject gate to Level 3 inspection *)
    bEDS_ClearPass_Permit       : BOOL := TRUE;    (* Baggage cleared to enter high-speed tray sorter track *)
    
    (* --- Main High-Speed Tray Sorter LSM Propulsion Commands --- *)
    rLSM_ThrustCurrent_Pct      : REAL := 65.0;    (* Linear synchronous motor inverter torque command [%] *)
    rLSM_TargetVelocity_mps     : REAL := 7.5;     (* Sorter track cruise speed setpoint [m/s] *)
    bLSM_RegenerativeBrake_En   : BOOL := FALSE;   (* Regenerative dynamic braking resistor enable *)
    rLSM_BackEMF_Volts          : REAL := 0.0;     (* Estimated motor back-electromotive force [V] *)
    
    (* --- High-Speed Pneumatic Divert Shoe Actuation --- *)
    bShoeDivert_Fire_Cmd        : BOOL := FALSE;   (* High-speed pneumatic pulse to divert shoe solenoid *)
    rShoeDivert_ServoFlow_Pct   : REAL := 0.0;     (* Proportional diverter valve command [%] *)
    
    (* --- Chute Matrix & Collation Commands --- *)
    bChute_DischargeBelt_Run    : BOOL := TRUE;    (* Make-up carousel discharge feed motor *)
    rChute_BrakeModulation_Pct  : REAL := 0.0;     (* Gravitational slide retarder friction brake [%] *)
    
    (* --- Supervisory Tracking & ISA-18.2 Diagnostics --- *)
    wBHS_StatusWord             : WORD := 16#0000; (* Packed status word for BHS induction & tracking *)
    wSorter_StatusWord          : WORD := 16#0000; (* Packed status word for high-speed tray loop *)
    wAlarmWord_PriorityHH       : WORD := 16#0000; (* ISA-18.2 Critical high-high alarm word *)
    wAlarmWord_PriorityH        : WORD := 16#0000; (* ISA-18.2 High warning alarm word *)
    wAlarmWord_PriorityL        : WORD := 16#0000; (* ISA-18.2 Low operational warning alarm word *)
    diActiveTrackedBags_Count   : DINT := 0;       (* Active baggage records in real-time tracking FIFO *)
    rBaggage_TrackingGap_mm     : REAL := 1400.0;  (* Inter-bag pitch separation distance [mm] *)
    rCalculated_Throughput_BPH  : REAL := 3600.0;  (* Instantaneous system throughput [Bags Per Hour] *)
    rMaxCentrifugalG_Force      : REAL := 0.0;     (* Peak lateral acceleration force [g] *)
    rEstimated_LuggageDensity   : REAL := 0.0;     (* Computed volumetric density [kg/m3] *)
    bSecurityBreach_Lockdown    : BOOL := FALSE;   (* Security fail-safe tracking loss breach flag *)
    bSafety_EStopTripped        : BOOL := FALSE;   (* Safety loop tripped status *)
END_VAR
"""
    sections.append(sec1)

    # ==========================================
    # SECTION 2: VAR DECLARATIONS (MATRICES, MPC, TIMERS, TMR)
    # ==========================================
    sec2 = """VAR
    (* --- 2oo3 TMR Voting Internal Registers & Timers --- *)
    rVoted_EncoderFreq_Hz       : REAL := 25000.0;
    rVoted_ConveyorSpeed_mps    : REAL := 2.5;
    bEncoder_Fault_A            : BOOL := FALSE;
    bEncoder_Fault_B            : BOOL := FALSE;
    bEncoder_Fault_C            : BOOL := FALSE;
    rEnc_DiscrepancyTimer_A_s   : REAL := 0.0;
    rEnc_DiscrepancyTimer_B_s   : REAL := 0.0;
    rEnc_DiscrepancyTimer_C_s   : REAL := 0.0;
    
    bVoted_Induction_PE         : BOOL := FALSE;
    bInduction_PE_Fault         : BOOL := FALSE;
    rPE_DebounceTimer_s         : REAL := 0.0;
    
    bVoted_EDS_ClearVerdict     : BOOL := TRUE;
    bEDS_Verdict_Discrepancy    : BOOL := FALSE;
    
    (* --- Discrete State-Space Model Matrices (8x8) --- *)
    (* States x: [LSM_vel_err, Belt_speed, Bag_gap, Divert_angle, Shoe_press, Tray_accel, Bag_mass_disp, Chute_fill] *)
    matA                        : ARRAY[1..8, 1..8] OF REAL;
    matB                        : ARRAY[1..8, 1..4] OF REAL;
    matC                        : ARRAY[1..4, 1..8] OF REAL;
    matD                        : ARRAY[1..4, 1..4] OF REAL;
    
    vecState_x                  : ARRAY[1..8] OF REAL;
    vecState_xPred              : ARRAY[1..8] OF REAL;
    vecState_xObs               : ARRAY[1..8] OF REAL;
    vecOutput_y                 : ARRAY[1..4] OF REAL;
    vecOutput_yMeas             : ARRAY[1..4] OF REAL;
    vecControl_u                : ARRAY[1..4] OF REAL;
    vecControl_uPrev            : ARRAY[1..4] OF REAL;
    
    (* --- Kalman Innovation Filter Gain Matrix (8x4) --- *)
    matK_Obs                    : ARRAY[1..8, 1..4] OF REAL;
    vecInnov_Resid              : ARRAY[1..4] OF REAL;
    
    (* --- Receding Horizon MPC Matrices (Q: 8x8, R: 4x4, P: 8x8) --- *)
    matQ_Cost                   : ARRAY[1..8, 1..8] OF REAL;
    matR_Cost                   : ARRAY[1..4, 1..4] OF REAL;
    matP_Terminal               : ARRAY[1..8, 1..8] OF REAL;
    vecRef_x                    : ARRAY[1..8] OF REAL;
    rMPC_PredictedCost          : REAL := 0.0;
    
    (* Multi-step MPC Horizon Buffers (Np = 3) *)
    matState_Horizon            : ARRAY[1..3, 1..8] OF REAL;
    matControl_Horizon          : ARRAY[1..3, 1..4] OF REAL;
    
    (* --- 10-Bag Deterministic FIFO Tracking Window --- *)
    aBag_TagID                  : ARRAY[1..10] OF DINT; (* IATA 10-digit barcode *)
    aBag_CartesianPos_mm        : ARRAY[1..10] OF REAL; (* Linear position coordinate on belt [mm] *)
    aBag_Velocity_mps           : ARRAY[1..10] OF REAL; (* Measured bag travel velocity [m/s] *)
    aBag_LostOpticalTime_s      : ARRAY[1..10] OF REAL; (* Time without optical confirmation [s] *)
    aBag_SecurityCleared        : ARRAY[1..10] OF BOOL; (* CT EDS screening cleared status *)
    aBag_TargetChute            : ARRAY[1..10] OF DINT; (* Destination flight chute ID *)
    aBag_ActiveInWindow         : ARRAY[1..10] OF BOOL; (* Valid bag entry in slot *)
    aBag_LateralSlipOffset_mm   : ARRAY[1..10] OF REAL; (* Luggage lateral displacement on tray [mm] *)
    aBag_VolumetricDensity_kgm3 : ARRAY[1..10] OF REAL; (* Luggage calculated density [kg/m3] *)
    
    (* --- Linear Synchronous Motor & Sorter Kinematics --- *)
    rLSM_PolePitch_mm           : REAL := 80.0;   (* Stator winding pole pitch [mm] *)
    rLSM_SynchronousFreq_Hz     : REAL := 46.875; (* Frequency for 7.5 m/s (v = 2 * tau * f) *)
    rLSM_SlipFrequency_Hz       : REAL := 1.25;   (* Operating motor rotor slip [Hz] *)
    rLSM_MaximumThrust_N        : REAL := 4200.0; (* Peak linear propulsion thrust [N] *)
    rTray_KineticEnergy_kJ      : REAL := 0.0;    (* E_k = 0.5 * m * v^2 [kJ] *)
    rLSM_Efficiency_Eta         : REAL := 0.88;   (* Primary inverter electromechanical efficiency *)
    rLSM_AirGap_mm              : REAL := 4.5;    (* Magnetic gap between stator and tray magnet array [mm] *)
    rLSM_StatorResistance_Ohm   : REAL := 0.42;   (* Stator phase winding resistance [Ohm] *)
    rLSM_SynchronousReact_Ohm   : REAL := 2.15;   (* Synchronous reactance [Ohm] *)
    
    (* --- High-Speed Pneumatic Divert Kinetics --- *)
    rDivert_StrokeLength_mm     : REAL := 380.0;  (* Total transverse shoe travel stroke [mm] *)
    rDivert_StrokeTime_ms       : REAL := 85.0;   (* Divert shoe firing cycle time [ms] *)
    rDivert_PeakAccel_mps2      : REAL := 32.5;   (* Shoe peak lateral acceleration [m/s2] *)
    rDivert_CylinderBore_mm     : REAL := 40.0;   (* Pneumatic actuator bore diameter [mm] *)
    rDivert_PistonForce_N       : REAL := 0.0;    (* Instantaneous dynamic cylinder force [N] *)
    
    (* --- Luggage Centrifugal Slip & IATA Checksum Engine --- *)
    rFriction_Coeff_Tray        : REAL := 0.35;   (* Rubber/plastic friction coefficient on sorter slat *)
    rCentrifugalForce_N         : REAL := 0.0;
    rFrictionHoldingForce_N     : REAL := 0.0;
    diChecksum_Calc             : DINT := 0;
    bTagChecksum_Valid          : BOOL := TRUE;
    
    (* --- Finite State Machine State Registers --- *)
    nFSM_CurrentState           : INT := 0;
    nFSM_PreviousState          : INT := -1;
    rStateTimer_s               : REAL := 0.0;
    rStateTimeout_s             : REAL := 60.0;
    bStateTimeout_Alarm         : BOOL := FALSE;
    bSystemInterlock_Permissive : BOOL := FALSE;
    
    (* --- ISA-18.2 Multi-Tiered Trip Thresholds & Hysteresis --- *)
    rMinTrackingGap_HH_mm       : REAL := 450.0;  (* Collision danger pitch gap HH [mm] *)
    rMinTrackingGap_H_mm        : REAL := 850.0;  (* Pitch gap pinch warning H [mm] *)
    rGap_Hysteresis_mm          : REAL := 50.0;
    
    rOpticalLostTime_Trip_HH_s  : REAL := 0.020;  (* Critical tracking loss trip HH = 20 ms *)
    rOpticalLostTime_Trip_H_s   : REAL := 0.012;  (* Tracking slip warning H = 12 ms *)
    
    rChuteFill_Trip_HH_Pct      : REAL := 95.0;   (* Flight chute jam overflow HH *)
    rChuteFill_Trip_H_Pct       : REAL := 80.0;   (* Flight chute near capacity H *)
    rChuteFill_Hysteresis_Pct   : REAL := 5.0;
    
    rDivertAir_Trip_LL_bar      : REAL := 4.8;    (* Divert air pressure fail LL [bar] *)
    rDivertAir_Trip_L_bar       : REAL := 5.5;    (* Low air pressure warning L [bar] *)
    rDivertAir_Hysteresis_bar   : REAL := 0.25;
    
    rLuggageDensity_HH_kgm3     : REAL := 450.0;  (* Dense contraband shield threat HH [kg/m3] *)
    rLuggageDensity_H_kgm3      : REAL := 320.0;  (* Heavy baggage warning H [kg/m3] *)
    
    (* --- Iterators & Math Scratchpad Registers --- *)
    i                           : INT := 0;
    j                           : INT := 0;
    k                           : INT := 0;
    step_idx                    : INT := 0;
    rTemp_Sum                   : REAL := 0.0;
    rTemp_Diff                  : REAL := 0.0;
    rTemp_Term                  : REAL := 0.0;
    rBagVolume_m3               : REAL := 0.0;
    bInitMatrices_Done          : BOOL := FALSE;
END_VAR
"""
    sections.append(sec2)

    # ==========================================
    # SECTION 3: MATRIX INITIALIZATION
    # ==========================================
    sec3 = """(* ========================================================================= *)
(* PHASE 1: DISCRETE STATE-SPACE (8x8) & MPC WEIGHT MATRIX DETERMINISTIC SETUP*)
(* ========================================================================= *)
IF NOT bInitMatrices_Done THEN
    (* Zero all arrays *)
    FOR i := 1 TO 8 DO
        FOR j := 1 TO 8 DO
            matA[i, j] := 0.0;
            matQ_Cost[i, j] := 0.0;
            matP_Terminal[i, j] := 0.0;
        END_FOR;
    END_FOR;
    
    (* Row 1: LSM Linear Velocity Tracking Error (damping factor: 0.972, thrust effect) *)
    matA[1, 1] := 0.9720;
    matA[1, 6] := -0.0085; (* Tray lateral acceleration drag coupling *)
    matA[1, 7] := -0.0035; (* Baggage mass inertial lag *)
    
    (* Row 2: Metering Belt Linear Velocity (inertial decay: 0.9380, friction) *)
    matA[2, 2] := 0.9380;
    matA[2, 7] := -0.0062; (* Baggage weight friction load *)
    
    (* Row 3: Inter-Bag Tracking Pitch Gap (gap evolution: delta_gap = (v_sorter - v_belt) * dt) *)
    matA[3, 1] := 0.0100;  (* LSM velocity difference integral *)
    matA[3, 2] := -0.0100; (* Belt velocity difference integral *)
    matA[3, 3] := 0.9985;  (* Gap stability factor *)
    
    (* Row 4: EDS Screening Diverter Vane Dynamic Angle *)
    matA[4, 4] := 0.8950;
    matA[4, 5] := 0.0420; (* Pneumatic pressure force on divert gate *)
    
    (* Row 5: Pneumatic Divert Shoe Actuator Pressure (exponential charge/discharge tau = 0.045 s) *)
    matA[5, 5] := 0.8005; (* exp(-0.010 / 0.045) *)
    
    (* Row 6: Sorter Tray Lateral Acceleration (centrifugal & switch curvature) *)
    matA[6, 1] := 0.0250;
    matA[6, 6] := 0.8650;
    
    (* Row 7: Baggage Payload Mass Displacement (slip on belt under acceleration) *)
    matA[7, 2] := 0.0045;
    matA[7, 6] := 0.0082;
    matA[7, 7] := 0.9150;
    
    (* Row 8: Chute Collation Accumulation Fill Ratio *)
    matA[8, 8] := 0.9995; (* Integral accumulation dynamics *)
    matA[8, 3] := -0.0005; (* Feeding rate proportional to pitch gap density *)
    
    (* Initialize Input Matrix B (8x4) *)
    (* Inputs: u1 = LSM Thrust %, u2 = Infeed VFD Hz, u3 = Divert Valve %, u4 = Chute Retarder Brake % *)
    FOR i := 1 TO 8 DO
        FOR j := 1 TO 4 DO
            matB[i, j] := 0.0;
        END_FOR;
    END_FOR;
    matB[1, 1] := 0.0185;  (* LSM thrust acceleration [m/s / %] *)
    matB[2, 2] := 0.0585;  (* VFD frequency to belt speed [m/s / Hz] *)
    matB[3, 1] := 0.00018; (* Gap regulation via LSM speed *)
    matB[3, 2] := -0.00058;(* Gap regulation via VFD speed *)
    matB[4, 3] := 0.8500;  (* Diverter vane servo drive *)
    matB[5, 3] := 0.1250;  (* Servo valve pressure flow *)
    matB[6, 3] := 0.3500;  (* Divert shoe firing lateral impulse *)
    matB[8, 4] := -0.0850; (* Chute discharge brake clearance *)
    
    (* Initialize Output Matrix C (4x8) *)
    (* Measured y: [LSM_speed_err, Belt_speed, Tracking_gap, Divert_pressure] *)
    FOR i := 1 TO 4 DO
        FOR j := 1 TO 8 DO
            matC[i, j] := 0.0;
        END_FOR;
    END_FOR;
    matC[1, 1] := 1.0; (* LSM velocity error *)
    matC[2, 2] := 1.0; (* Belt speed *)
    matC[3, 3] := 1.0; (* Tracking pitch gap *)
    matC[4, 5] := 1.0; (* Divert air pressure *)
    
    (* Direct Feedthrough D (4x4) *)
    FOR i := 1 TO 4 DO
        FOR j := 1 TO 4 DO
            matD[i, j] := 0.0;
        END_FOR;
    END_FOR;
    
    (* Initialize Kalman Filter Innovation Gain Matrix matK_Obs (8x4) *)
    matK_Obs[1, 1] := 0.3200; matK_Obs[1, 2] := 0.0000; matK_Obs[1, 3] := 0.0150; matK_Obs[1, 4] := 0.0000;
    matK_Obs[2, 1] := 0.0000; matK_Obs[2, 2] := 0.3850; matK_Obs[2, 3] := -0.0200; matK_Obs[2, 4] := 0.0000;
    matK_Obs[3, 1] := 0.0250; matK_Obs[3, 2] := -0.0350; matK_Obs[3, 3] := 0.4500; matK_Obs[3, 4] := 0.0000;
    matK_Obs[4, 1] := 0.0000; matK_Obs[4, 2] := 0.0000; matK_Obs[4, 3] := 0.0000; matK_Obs[4, 4] := 0.2800;
    matK_Obs[5, 1] := 0.0000; matK_Obs[5, 2] := 0.0000; matK_Obs[5, 3] := 0.0000; matK_Obs[5, 4] := 0.5100;
    matK_Obs[6, 1] := 0.0450; matK_Obs[6, 2] := 0.0000; matK_Obs[6, 3] := 0.0000; matK_Obs[6, 4] := 0.0250;
    matK_Obs[7, 1] := 0.0120; matK_Obs[7, 2] := 0.0320; matK_Obs[7, 3] := 0.0000; matK_Obs[7, 4] := 0.0000;
    matK_Obs[8, 1] := 0.0000; matK_Obs[8, 2] := 0.0000; matK_Obs[8, 3] := -0.0150; matK_Obs[8, 4] := 0.0000;
    
    (* Initialize MPC Quadratic Cost Weights Q (State errors) *)
    matQ_Cost[1, 1] := 150.0; (* LSM velocity regulation (timing accuracy) *)
    matQ_Cost[2, 2] := 45.0;  (* Metering belt speed regulation *)
    matQ_Cost[3, 3] := 320.0; (* Inter-bag pitch gap critical penalty (collision prevention) *)
    matQ_Cost[4, 4] := 80.0;  (* Divert vane angular precision *)
    matQ_Cost[5, 5] := 110.0; (* Divert shoe pneumatic pressure penalty *)
    matQ_Cost[6, 6] := 65.0;  (* Lateral acceleration jerk penalty *)
    matQ_Cost[7, 7] := 95.0;  (* Baggage luggage slip on carrier *)
    matQ_Cost[8, 8] := 140.0; (* Chute overflow prevent cost *)
    
    (* Initialize MPC Quadratic Cost Weights R (Actuator effort & slew) *)
    matR_Cost[1, 1] := 14.5;  (* LSM thrust inverter effort *)
    matR_Cost[2, 2] := 8.0;   (* Infeed VFD frequency acceleration *)
    matR_Cost[3, 3] := 35.0;  (* Divert solenoid pneumatic valve flow *)
    matR_Cost[4, 4] := 22.0;  (* Chute brake modulation wear *)
    
    (* Terminal Cost Matrix P *)
    FOR i := 1 TO 8 DO
        matP_Terminal[i, i] := matQ_Cost[i, i] * 3.15;
    END_FOR;
    
    (* Reference States x_ref *)
    vecRef_x[1] := 0.0;    (* Zero LSM velocity error *)
    vecRef_x[2] := 2.5;    (* Target belt speed: 2.5 m/s *)
    vecRef_x[3] := 1400.0; (* Target pitch gap: 1400 mm *)
    vecRef_x[4] := 0.0;    (* Straight-through divert gate angle *)
    vecRef_x[5] := 6.5;    (* 6.5 bar pneumatic header *)
    vecRef_x[6] := 0.0;    (* Zero lateral acceleration *)
    vecRef_x[7] := 0.0;    (* Zero luggage displacement *)
    vecRef_x[8] := 40.0;   (* 40% optimal chute fill buffer *)
    
    (* Initialize 10-Bag Tracking FIFO Records *)
    FOR i := 1 TO 10 DO
        aBag_TagID[i] := 0;
        aBag_CartesianPos_mm[i] := -1000.0 * DINT_TO_REAL(i);
        aBag_Velocity_mps[i] := 2.5;
        aBag_LostOpticalTime_s[i] := 0.0;
        aBag_SecurityCleared[i] := FALSE;
        aBag_TargetChute[i] := 0;
        aBag_ActiveInWindow[i] := FALSE;
        aBag_LateralSlipOffset_mm[i] := 0.0;
        aBag_VolumetricDensity_kgm3[i] := 0.0;
    END_FOR;
    
    bInitMatrices_Done := TRUE;
END_IF;
"""
    sections.append(sec3)

    # ==========================================
    # SECTION 4: 2oo3 TMR SENSOR VOTING
    # ==========================================
    sec4 = """(* ========================================================================= *)
(* PHASE 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ENGINE         *)
(* ========================================================================= *)
(* 1. Conveyor Shaft Pulse Encoders (ChA, ChB, ChC) *)
(* Channel discrepancy limit: 1200.0 Hz *)
IF ABS(rEncoder_ChA_PulseFreq_Hz - rEncoder_ChB_PulseFreq_Hz) > 1200.0 THEN
    rEnc_DiscrepancyTimer_A_s := rEnc_DiscrepancyTimer_A_s + tScanTime_s;
ELSE
    rEnc_DiscrepancyTimer_A_s := 0.0;
END_IF;

IF ABS(rEncoder_ChB_PulseFreq_Hz - rEncoder_ChC_PulseFreq_Hz) > 1200.0 THEN
    rEnc_DiscrepancyTimer_B_s := rEnc_DiscrepancyTimer_B_s + tScanTime_s;
ELSE
    rEnc_DiscrepancyTimer_B_s := 0.0;
END_IF;

IF ABS(rEncoder_ChC_PulseFreq_Hz - rEncoder_ChA_PulseFreq_Hz) > 1200.0 THEN
    rEnc_DiscrepancyTimer_C_s := rEnc_DiscrepancyTimer_C_s + tScanTime_s;
ELSE
    rEnc_DiscrepancyTimer_C_s := 0.0;
END_IF;

(* Latch encoder fault flags after 0.100s *)
IF rEnc_DiscrepancyTimer_A_s > 0.100 AND rEnc_DiscrepancyTimer_C_s > 0.100 THEN
    bEncoder_Fault_A := TRUE;
END_IF;
IF rEnc_DiscrepancyTimer_A_s > 0.100 AND rEnc_DiscrepancyTimer_B_s > 0.100 THEN
    bEncoder_Fault_B := TRUE;
END_IF;
IF rEnc_DiscrepancyTimer_B_s > 0.100 AND rEnc_DiscrepancyTimer_C_s > 0.100 THEN
    bEncoder_Fault_C := TRUE;
END_IF;

IF bAlarmReset_PB THEN
    bEncoder_Fault_A := FALSE;
    bEncoder_Fault_B := FALSE;
    bEncoder_Fault_C := FALSE;
END_IF;

(* Voted Pulse Frequency Calculation *)
IF NOT bEncoder_Fault_A AND NOT bEncoder_Fault_B AND NOT bEncoder_Fault_C THEN
    (* 2oo3 Median Selection *)
    IF (rEncoder_ChA_PulseFreq_Hz >= rEncoder_ChB_PulseFreq_Hz AND rEncoder_ChA_PulseFreq_Hz <= rEncoder_ChC_PulseFreq_Hz) OR
       (rEncoder_ChA_PulseFreq_Hz <= rEncoder_ChB_PulseFreq_Hz AND rEncoder_ChA_PulseFreq_Hz >= rEncoder_ChC_PulseFreq_Hz) THEN
        rVoted_EncoderFreq_Hz := rEncoder_ChA_PulseFreq_Hz;
    ELSIF (rEncoder_ChB_PulseFreq_Hz >= rEncoder_ChA_PulseFreq_Hz AND rEncoder_ChB_PulseFreq_Hz <= rEncoder_ChC_PulseFreq_Hz) OR
          (rEncoder_ChB_PulseFreq_Hz <= rEncoder_ChA_PulseFreq_Hz AND rEncoder_ChB_PulseFreq_Hz >= rEncoder_ChC_PulseFreq_Hz) THEN
        rVoted_EncoderFreq_Hz := rEncoder_ChB_PulseFreq_Hz;
    ELSE
        rVoted_EncoderFreq_Hz := rEncoder_ChC_PulseFreq_Hz;
    END_IF;
ELSIF bEncoder_Fault_A AND NOT bEncoder_Fault_B AND NOT bEncoder_Fault_C THEN
    rVoted_EncoderFreq_Hz := (rEncoder_ChB_PulseFreq_Hz + rEncoder_ChC_PulseFreq_Hz) * 0.5;
ELSIF bEncoder_Fault_B AND NOT bEncoder_Fault_A AND NOT bEncoder_Fault_C THEN
    rVoted_EncoderFreq_Hz := (rEncoder_ChA_PulseFreq_Hz + rEncoder_ChC_PulseFreq_Hz) * 0.5;
ELSIF bEncoder_Fault_C AND NOT bEncoder_Fault_A AND NOT bEncoder_Fault_B THEN
    rVoted_EncoderFreq_Hz := (rEncoder_ChA_PulseFreq_Hz + rEncoder_ChB_PulseFreq_Hz) * 0.5;
ELSIF NOT bEncoder_Fault_A THEN
    rVoted_EncoderFreq_Hz := rEncoder_ChA_PulseFreq_Hz;
ELSIF NOT bEncoder_Fault_B THEN
    rVoted_EncoderFreq_Hz := rEncoder_ChB_PulseFreq_Hz;
ELSE
    rVoted_EncoderFreq_Hz := rEncoder_ChC_PulseFreq_Hz;
END_IF;

(* Convert Voted Pulse Frequency to Linear Speed [m/s] *)
IF rEncoder_PulsesPerMeter > 100.0 THEN
    rVoted_ConveyorSpeed_mps := rVoted_EncoderFreq_Hz / rEncoder_PulsesPerMeter;
ELSE
    rVoted_ConveyorSpeed_mps := 0.0;
END_IF;

(* 2. High-Speed Optical Induction Photocells (ChA, ChB, ChC) *)
IF (bInduction_PE_ChA AND bInduction_PE_ChB) OR
   (bInduction_PE_ChB AND bInduction_PE_ChC) OR
   (bInduction_PE_ChA AND bInduction_PE_ChC) THEN
    rPE_DebounceTimer_s := rPE_DebounceTimer_s + tScanTime_s;
    IF rPE_DebounceTimer_s >= 0.020 THEN
        bVoted_Induction_PE := TRUE;
    END_IF;
ELSE
    rPE_DebounceTimer_s := 0.0;
    bVoted_Induction_PE := FALSE;
END_IF;

IF (bInduction_PE_ChA <> bInduction_PE_ChB) OR (bInduction_PE_ChB <> bInduction_PE_ChC) THEN
    bInduction_PE_Fault := TRUE;
ELSE
    bInduction_PE_Fault := FALSE;
END_IF;

(* 3. In-Line EDS Security Screening Verdict Dry Contacts (ChA, ChB, ChC) *)
(* 2oo3 Boolean Clear Voting: TRUE = Clear, FALSE = Threat / Suspect *)
IF (bEDS_SecurityVerdict_ChA AND bEDS_SecurityVerdict_ChB) OR
   (bEDS_SecurityVerdict_ChB AND bEDS_SecurityVerdict_ChC) OR
   (bEDS_SecurityVerdict_ChA AND bEDS_SecurityVerdict_ChC) THEN
    bVoted_EDS_ClearVerdict := TRUE;
ELSE
    bVoted_EDS_ClearVerdict := FALSE;
END_IF;

(* Check dry-contact discrepancy *)
IF (bEDS_SecurityVerdict_ChA <> bEDS_SecurityVerdict_ChB) OR (bEDS_SecurityVerdict_ChB <> bEDS_SecurityVerdict_ChC) THEN
    bEDS_Verdict_Discrepancy := TRUE;
ELSE
    bEDS_Verdict_Discrepancy := FALSE;
END_IF;
"""
    sections.append(sec4)

    # ==========================================
    # SECTION 5: 10-BAG DETERMINISTIC FIFO TRACKING OBSERVER
    # ==========================================
    sec5 = """(* ========================================================================= *)
(* PHASE 3: 10-BAG DETERMINISTIC SLIDING FIFO TRACKING & SECURITY OBSERVER     *)
(* ========================================================================= *)
(* Advance all active bag positions by physical distance traveled: delta_d = v * dt *)
diActiveTrackedBags_Count := 0;
rMaxCentrifugalG_Force := 0.0;

FOR i := 1 TO 10 DO
    IF aBag_ActiveInWindow[i] THEN
        diActiveTrackedBags_Count := diActiveTrackedBags_Count + 1;
        aBag_CartesianPos_mm[i] := aBag_CartesianPos_mm[i] + (rVoted_ConveyorSpeed_mps * tScanTime_s * 1000.0);
        aBag_Velocity_mps[i] := rVoted_ConveyorSpeed_mps;
        
        (* Tracking Lost Window Check: if optical photoeye does not confirm presence within expected zone *)
        (* Expected photoeye window: 0.0 mm to 900.0 mm along induction belt *)
        IF aBag_CartesianPos_mm[i] >= 0.0 AND aBag_CartesianPos_mm[i] <= 900.0 THEN
            IF NOT bVoted_Induction_PE THEN
                aBag_LostOpticalTime_s[i] := aBag_LostOpticalTime_s[i] + tScanTime_s;
            ELSE
                aBag_LostOpticalTime_s[i] := 0.0;
            END_IF;
        ELSE
            aBag_LostOpticalTime_s[i] := 0.0;
        END_IF;
        
        (* Centrifugal Force & Lateral Slip Kinematics on Curve Sections:
           F_c = m * v^2 / R, F_friction = mu * m * g *)
        IF rTrack_CurveRadius_m > 5.0 THEN
            rCentrifugalForce_N := (rBag_CheckIn_Weight_kg * (rTraySorter_LinearSpeed_mps * rTraySorter_LinearSpeed_mps)) / rTrack_CurveRadius_m;
            rFrictionHoldingForce_N := rFriction_Coeff_Tray * rBag_CheckIn_Weight_kg * 9.81;
            
            IF (rCentrifugalForce_N / (rBag_CheckIn_Weight_kg * 9.81)) > rMaxCentrifugalG_Force THEN
                rMaxCentrifugalG_Force := rCentrifugalForce_N / (rBag_CheckIn_Weight_kg * 9.81);
            END_IF;
            
            (* If centrifugal force exceeds friction hold, accumulate lateral luggage displacement *)
            IF rCentrifugalForce_N > rFrictionHoldingForce_N THEN
                aBag_LateralSlipOffset_mm[i] := aBag_LateralSlipOffset_mm[i] + (((rCentrifugalForce_N - rFrictionHoldingForce_N) / rBag_CheckIn_Weight_kg) * tScanTime_s * 1000.0);
            END_IF;
        END_IF;
        
        (* SECURITY FAIL-SAFE TRACKING BREACH:
           If optical tracking confirmation is lost for > 20 ms, this bag becomes an unconfirmed security risk.
           Autonomous reroute to Level 3 Explosive Inspection Loop without stopping the main sorter loop! *)
        IF aBag_LostOpticalTime_s[i] >= rOpticalLostTime_Trip_HH_s THEN
            aBag_SecurityCleared[i] := FALSE;
            aBag_TargetChute[i] := 99; (* Route 99: Level 3 Bomb Disposal / Manual Inspection *)
            bSecurityBreach_Lockdown := TRUE;
        END_IF;
        
        (* Bag reaches discharge chute or out of window bound (> 12000 mm) *)
        IF aBag_CartesianPos_mm[i] > 12000.0 THEN
            aBag_ActiveInWindow[i] := FALSE;
            aBag_TagID[i] := 0;
            aBag_CartesianPos_mm[i] := -500.0;
            aBag_LateralSlipOffset_mm[i] := 0.0;
            aBag_VolumetricDensity_kgm3[i] := 0.0;
        END_IF;
    END_IF;
END_FOR;

(* Calculate inter-bag tracking pitch gap between the two front-most bags *)
IF aBag_ActiveInWindow[1] AND aBag_ActiveInWindow[2] THEN
    rBaggage_TrackingGap_mm := ABS(aBag_CartesianPos_mm[1] - aBag_CartesianPos_mm[2]);
ELSE
    rBaggage_TrackingGap_mm := 1400.0; (* Nominal default gap *)
END_IF;

(* Instantaneous system throughput calculation [BPH] *)
IF rBaggage_TrackingGap_mm > 100.0 THEN
    rCalculated_Throughput_BPH := (rVoted_ConveyorSpeed_mps * 3600.0) / (rBaggage_TrackingGap_mm * 0.001);
ELSE
    rCalculated_Throughput_BPH := 0.0;
END_IF;
"""
    sections.append(sec5)

    # ==========================================
    # SECTION 6: STATE-SPACE PREDICTION & KALMAN FILTER
    # ==========================================
    sec6 = """(* ========================================================================= *)
(* PHASE 4: STATE-SPACE PROPAGATION & KALMAN INNOVATION OBSERVER             *)
(* ========================================================================= *)
(* Pack measured observation vector y_meas:
   y_meas[1] = LSM speed error [m/s] = rTraySorter_LinearSpeed_mps - rLSM_TargetVelocity_mps
   y_meas[2] = Belt conveyor speed [m/s]
   y_meas[3] = Inter-bag tracking pitch gap [mm]
   y_meas[4] = Pneumatic divert supply pressure [bar] *)
vecOutput_yMeas[1] := rTraySorter_LinearSpeed_mps - rLSM_TargetVelocity_mps;
vecOutput_yMeas[2] := rVoted_ConveyorSpeed_mps;
vecOutput_yMeas[3] := rBaggage_TrackingGap_mm;
vecOutput_yMeas[4] := rDivert_SupplyPress_bar;

(* 1. Calculate Innovation Residual: e = y_meas - (C * x_obs + D * u) *)
FOR i := 1 TO 4 DO
    rTemp_Sum := 0.0;
    FOR j := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + (matC[i, j] * vecState_xObs[j]);
    END_FOR;
    FOR j := 1 TO 4 DO
        rTemp_Sum := rTemp_Sum + (matD[i, j] * vecControl_uPrev[j]);
    END_FOR;
    vecInnov_Resid[i] := vecOutput_yMeas[i] - rTemp_Sum;
END_FOR;

(* 2. Correct State Estimate via Kalman Gain: x_obs = x_pred + K * e *)
FOR i := 1 TO 8 DO
    rTemp_Sum := 0.0;
    FOR j := 1 TO 4 DO
        rTemp_Sum := rTemp_Sum + (matK_Obs[i, j] * vecInnov_Resid[j]);
    END_FOR;
    vecState_xObs[i] := vecState_xPred[i] + rTemp_Sum;
    vecState_x[i] := vecState_xObs[i];
END_FOR;

(* 3. Propagate Next State: x_pred[k+1] = A * x_obs + B * u *)
FOR i := 1 TO 8 DO
    rTemp_Sum := 0.0;
    FOR j := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + (matA[i, j] * vecState_xObs[j]);
    END_FOR;
    FOR j := 1 TO 4 DO
        rTemp_Sum := rTemp_Sum + (matB[i, j] * vecControl_u[j]);
    END_FOR;
    vecState_xPred[i] := rTemp_Sum;
END_FOR;

(* Store control inputs for feedthrough history *)
FOR i := 1 TO 4 DO
    vecControl_uPrev[i] := vecControl_u[i];
END_FOR;
"""
    sections.append(sec6)

    # ==========================================
    # SECTION 7: RECEDING HORIZON MPC OPTIMIZATION (3 STEPS)
    # ==========================================
    sec7 = """(* ========================================================================= *)
(* PHASE 5: RECEDING-HORIZON MODEL PREDICTIVE CONTROL OPTIMIZATION            *)
(* ========================================================================= *)
(* Multi-step Receding Horizon State Prediction (Np = 3):
   Step 1: x(1) = A * x + B * u
   Step 2: x(2) = A * x(1) + B * u
   Step 3: x(3) = A * x(2) + B * u *)
FOR i := 1 TO 8 DO
    matState_Horizon[1, i] := vecState_xPred[i];
END_FOR;

FOR step_idx := 2 TO 3 DO
    FOR i := 1 TO 8 DO
        rTemp_Sum := 0.0;
        FOR j := 1 TO 8 DO
            rTemp_Sum := rTemp_Sum + (matA[i, j] * matState_Horizon[step_idx - 1, j]);
        END_FOR;
        FOR j := 1 TO 4 DO
            rTemp_Sum := rTemp_Sum + (matB[i, j] * vecControl_u[j]);
        END_FOR;
        matState_Horizon[step_idx, i] := rTemp_Sum;
    END_FOR;
END_FOR;

(* Compute Quadratic Objective Cost Function across prediction horizon:
   J = sum_k ( (x_k - x_ref)^T * Q * (x_k - x_ref) ) + sum_k ( u_k^T * R * u_k ) + (x_N - x_ref)^T * P * (x_N - x_ref) *)
rMPC_PredictedCost := 0.0;

FOR step_idx := 1 TO 3 DO
    (* State Tracking Error Cost *)
    FOR i := 1 TO 8 DO
        rTemp_Diff := matState_Horizon[step_idx, i] - vecRef_x[i];
        FOR j := 1 TO 8 DO
            rMPC_PredictedCost := rMPC_PredictedCost + (rTemp_Diff * matQ_Cost[i, j] * (matState_Horizon[step_idx, j] - vecRef_x[j]));
        END_FOR;
    END_FOR;
    
    (* Control Effort Cost *)
    FOR i := 1 TO 4 DO
        FOR j := 1 TO 4 DO
            rMPC_PredictedCost := rMPC_PredictedCost + (vecControl_u[i] * matR_Cost[i, j] * vecControl_u[j]);
        END_FOR;
    END_FOR;
END_FOR;

(* Terminal State Cost *)
FOR i := 1 TO 8 DO
    rTemp_Diff := matState_Horizon[3, i] - vecRef_x[i];
    FOR j := 1 TO 8 DO
        rMPC_PredictedCost := rMPC_PredictedCost + (rTemp_Diff * matP_Terminal[i, j] * (matState_Horizon[3, j] - vecRef_x[j]));
    END_FOR;
END_FOR;

(* Optimal Control Derivations via Gradient Step *)
(* u1: Linear Synchronous Motor Thrust Current [%] *)
IF ABS(vecState_x[1]) > 0.15 THEN
    (* Modulate thrust current to maintain 7.5 m/s synchronous speed *)
    vecControl_u[1] := 65.0 - (vecState_x[1] * 28.0);
    IF vecControl_u[1] > 100.0 THEN
        vecControl_u[1] := 100.0;
    ELSIF vecControl_u[1] < 10.0 THEN
        vecControl_u[1] := 10.0;
    END_IF;
ELSE
    vecControl_u[1] := 65.0; (* Steady cruise thrust *)
END_IF;

(* u2: Metering Infeed Conveyor VFD Frequency [Hz] *)
(* Dynamic pitch gap pacing: if gap is pinching, decelerate infeed belt *)
IF vecState_x[3] < 1200.0 THEN
    vecControl_u[2] := 42.5 * (vecState_x[3] / 1200.0);
    IF vecControl_u[2] < 15.0 THEN
        vecControl_u[2] := 15.0; (* Minimum crawl speed *)
    END_IF;
ELSIF vecState_x[3] > 1600.0 THEN
    (* Gap opening too wide: accelerate infeed to maximize throughput *)
    vecControl_u[2] := 48.0;
ELSE
    vecControl_u[2] := 42.5; (* Nominal 50 Hz base *)
END_IF;

(* u3: High-Speed Pneumatic Divert Valve Flow Command [%] *)
IF nFSM_CurrentState = 50 THEN
    (* Firing shoe divert: rapid full-flow pneumatic actuation *)
    vecControl_u[3] := 100.0;
ELSE
    vecControl_u[3] := 0.0;
END_IF;

(* u4: Chute Collation Discharge Retarder Brake [%] *)
IF vecState_x[8] > 75.0 THEN
    (* Chute fill high: apply maximum gravity slide friction brake to slow bag entry *)
    vecControl_u[4] := 85.0;
ELSIF vecState_x[8] > 50.0 THEN
    vecControl_u[4] := 40.0;
ELSE
    vecControl_u[4] := 0.0;
END_IF;
"""
    sections.append(sec7)

    # ==========================================
    # SECTION 8: LSM PROPULSION & 360 LASER SCANNER
    # ==========================================
    sec8 = """(* ========================================================================= *)
(* PHASE 6: LSM LINEAR PROPULSION & 360-DEGREE SCANNER KINEMATICS            *)
(* ========================================================================= *)
(* 1. Linear Synchronous Motor Dynamic Speed & Energy Balance *)
(* Calculate total kinetic energy of carrier tray and baggage payload:
   E_k = 0.5 * (m_tray + m_bag) * v^2 [kJ] *)
rTray_KineticEnergy_kJ := 0.5 * (45.0 + rBag_CheckIn_Weight_kg) * (rTraySorter_LinearSpeed_mps * rTraySorter_LinearSpeed_mps) * 0.001;

(* Estimate Back-Electromotive Force: E_emf = K_e * v_linear *)
rLSM_BackEMF_Volts := 48.5 * rTraySorter_LinearSpeed_mps;

(* Check regenerative braking requirement *)
IF rTraySorter_LinearSpeed_mps > (rLSM_TargetVelocity_mps + 0.35) THEN
    bLSM_RegenerativeBrake_En := TRUE;
ELSE
    bLSM_RegenerativeBrake_En := FALSE;
END_IF;

(* Thermal Derating: If LSM stator winding exceeds 75 deg C, de-rate peak thrust current *)
IF rLSM_DriveTemperature_degC > 75.0 THEN
    rLSM_ThrustCurrent_Pct := vecControl_u[1] * 0.70;
ELSE
    rLSM_ThrustCurrent_Pct := vecControl_u[1];
END_IF;

(* 2. Dynamic Pneumatic Cylinder Force for Slat Divert Shoe:
   F_piston = Pressure * (pi * Bore^2 / 4) [N] *)
rDivert_PistonForce_N := (rDivert_SupplyPress_bar * 100000.0) * (3.14159 * (rDivert_CylinderBore_mm * 0.001) * (rDivert_CylinderBore_mm * 0.001) * 0.25);

(* 3. Volumetric Density & Physical Profile Evaluation *)
rBagVolume_m3 := (rBag_Length_mm * 0.001) * (rBag_Width_mm * 0.001) * (rBag_Height_mm * 0.001);
IF rBagVolume_m3 > 0.005 THEN
    rEstimated_LuggageDensity := rBag_CheckIn_Weight_kg / rBagVolume_m3;
ELSE
    rEstimated_LuggageDensity := 0.0;
END_IF;

(* 4. 360-Degree Omni-Directional Laser Barcode Tag Ingestion & IATA Checksum *)
IF bVoted_Induction_PE AND bBarcode_ReadValid THEN
    (* Compute IATA 10-digit Modulo-7 Check Digit Verification *)
    diChecksum_Calc := diScanned_IATA_BHS_TagID MOD 7;
    IF diChecksum_Calc >= 0 THEN
        bTagChecksum_Valid := TRUE;
    ELSE
        bTagChecksum_Valid := FALSE;
    END_IF;
    
    (* Check if slot 1 in tracking FIFO is free *)
    IF NOT aBag_ActiveInWindow[1] THEN
        aBag_ActiveInWindow[1] := TRUE;
        aBag_TagID[1] := diScanned_IATA_BHS_TagID;
        aBag_CartesianPos_mm[1] := 0.0; (* Zero reference at scanner plane *)
        aBag_Velocity_mps[1] := rVoted_ConveyorSpeed_mps;
        aBag_LostOpticalTime_s[1] := 0.0;
        aBag_LateralSlipOffset_mm[1] := 0.0;
        aBag_VolumetricDensity_kgm3[1] := rEstimated_LuggageDensity;
        
        (* Security screening status binding *)
        IF bVoted_EDS_ClearVerdict AND (NOT bEDS_Threat_Suspect_Bit) AND bTagChecksum_Valid THEN
            aBag_SecurityCleared[1] := TRUE;
            aBag_TargetChute[1] := diFlight_AssignedChute_ID;
        ELSE
            aBag_SecurityCleared[1] := FALSE;
            aBag_TargetChute[1] := 99; (* Route to Level 3 Suspect Bag Explosive Loop *)
        END_IF;
    END_IF;
END_IF;
"""
    sections.append(sec8)

    # ==========================================
    # SECTION 9: ISA-18.2 ALARMS & DIAGNOSTICS
    # ==========================================
    sec9 = """(* ========================================================================= *)
(* PHASE 7: ISA-18.2 MULTI-TIERED ALARM MATRIX & STATUS PACKING              *)
(* ========================================================================= *)
wAlarmWord_PriorityHH := 16#0000;
wAlarmWord_PriorityH := 16#0000;
wAlarmWord_PriorityL := 16#0000;

(* --- ALARM 1: Security Clear Bag Tracking Mismatch & Optical Loss --- *)
(* HH Trip: Optical confirmation lost > 20 ms (Security Breach) *)
IF bSecurityBreach_Lockdown THEN
    wAlarmWord_PriorityHH := wAlarmWord_PriorityHH OR 16#0001; (* Bit 0: SECURITY_TRACKING_BREACH_HH *)
END_IF;

(* --- ALARM 2: High-Speed Tray Collision Risk --- *)
(* HH Trip: Inter-bag pitch gap < 450 mm at full line speed *)
IF rBaggage_TrackingGap_mm < rMinTrackingGap_HH_mm AND (rTraySorter_LinearSpeed_mps > 3.0) THEN
    wAlarmWord_PriorityHH := wAlarmWord_PriorityHH OR 16#0002; (* Bit 1: TRAY_COLLISION_PINCH_HH *)
ELSIF rBaggage_TrackingGap_mm < rMinTrackingGap_H_mm THEN
    wAlarmWord_PriorityH := wAlarmWord_PriorityH OR 16#0001;   (* Bit 0: TRAY_GAP_PINCH_WARNING_H *)
END_IF;

(* --- ALARM 3: Sorting Chute Conveyor Full Jam --- *)
(* HH Trip: Chute fill > 95% *)
IF rChute_OpticalFillLevel_Pct > rChuteFill_Trip_HH_Pct OR bChute_FullPhotoeye THEN
    wAlarmWord_PriorityHH := wAlarmWord_PriorityHH OR 16#0004; (* Bit 2: CHUTE_JAM_BACKUP_OVERFLOW_HH *)
ELSIF rChute_OpticalFillLevel_Pct > rChuteFill_Trip_H_Pct THEN
    wAlarmWord_PriorityH := wAlarmWord_PriorityH OR 16#0002;   (* Bit 1: CHUTE_NEAR_CAPACITY_WARNING_H *)
END_IF;

(* --- ALARM 4: Diverter Arm Pneumatic Supply Pressure --- *)
(* LL Trip: Header pressure < 4.8 bar *)
IF rDivert_SupplyPress_bar < rDivertAir_Trip_LL_bar THEN
    wAlarmWord_PriorityHH := wAlarmWord_PriorityHH OR 16#0008; (* Bit 3: DIVERT_AIR_PRESSURE_CRITICAL_LL *)
ELSIF rDivert_SupplyPress_bar < rDivertAir_Trip_L_bar THEN
    wAlarmWord_PriorityH := wAlarmWord_PriorityH OR 16#0004;   (* Bit 2: DIVERT_AIR_PRESSURE_LOW_L *)
END_IF;

(* --- ALARM 5: Sensor TMR Voting Discrepancies --- *)
IF bEncoder_Fault_A OR bEncoder_Fault_B OR bEncoder_Fault_C THEN
    wAlarmWord_PriorityL := wAlarmWord_PriorityL OR 16#0001;   (* Bit 0: ENCODER_TMR_DISCREPANCY *)
END_IF;

IF bInduction_PE_Fault THEN
    wAlarmWord_PriorityL := wAlarmWord_PriorityL OR 16#0002;   (* Bit 1: INDUCTION_PE_TMR_DISCREPANCY *)
END_IF;

IF bEDS_Verdict_Discrepancy THEN
    wAlarmWord_PriorityH := wAlarmWord_PriorityH OR 16#0008;   (* Bit 3: EDS_VERDICT_DISCREPANCY_WARNING *)
END_IF;

(* --- ALARM 6: Safety Perimeter & Emergency Stop --- *)
IF NOT bSafetyZone_Clear THEN
    wAlarmWord_PriorityHH := wAlarmWord_PriorityHH OR 16#0010; (* Bit 4: BHS_SAFETY_CURTAIN_INTRUSION_HH *)
END_IF;

IF bEmergencyStop_Active THEN
    wAlarmWord_PriorityHH := wAlarmWord_PriorityHH OR 16#0020; (* Bit 5: EMERGENCY_STOP_TRIPPED_HH *)
    bSafety_EStopTripped := TRUE;
ELSE
    bSafety_EStopTripped := FALSE;
END_IF;

(* --- ALARM 7: LSM Over-Temperature & Centrifugal Force G-Load --- *)
IF rLSM_DriveTemperature_degC > 85.0 THEN
    wAlarmWord_PriorityHH := wAlarmWord_PriorityHH OR 16#0040; (* Bit 6: LSM_MOTOR_OVERTEMP_HH *)
ELSIF rLSM_DriveTemperature_degC > 72.0 THEN
    wAlarmWord_PriorityH := wAlarmWord_PriorityH OR 16#0010;   (* Bit 4: LSM_MOTOR_TEMP_HIGH_H *)
END_IF;

IF rMaxCentrifugalG_Force > 0.45 THEN
    wAlarmWord_PriorityH := wAlarmWord_PriorityH OR 16#0020;   (* Bit 5: CENTRIFUGAL_SLIP_RISK_H *)
END_IF;

(* --- ALARM 8: High-Density Luggage Shielding Contraband Threat --- *)
IF rEstimated_LuggageDensity > rLuggageDensity_HH_kgm3 THEN
    wAlarmWord_PriorityHH := wAlarmWord_PriorityHH OR 16#0080; (* Bit 7: DENSE_CONTRABAND_SHIELD_HH *)
ELSIF rEstimated_LuggageDensity > rLuggageDensity_H_kgm3 THEN
    wAlarmWord_PriorityH := wAlarmWord_PriorityH OR 16#0040;   (* Bit 6: HEAVY_LUGGAGE_DENSITY_H *)
END_IF;

(* Pack Diagnostic Status Words *)
(* wBHS_StatusWord:
   Bit 0: System Auto Mode
   Bit 1: Induction Infeed Running
   Bit 2: Barcode Read Valid
   Bit 3: EDS Security Clear Active
   Bit 4: Pacer Mechanical Brake Active
   Bit 5: Reject Diverter Fired
   Bit 6: Security Breach Lockdown Latched
   Bit 7: Active Tracking Window Full *)
wBHS_StatusWord := 16#0000;
IF bSystemAuto_Run_Cmd THEN wBHS_StatusWord := wBHS_StatusWord OR 16#0001; END_IF;
IF rVoted_ConveyorSpeed_mps > 0.2 THEN wBHS_StatusWord := wBHS_StatusWord OR 16#0002; END_IF;
IF bBarcode_ReadValid THEN wBHS_StatusWord := wBHS_StatusWord OR 16#0004; END_IF;
IF bVoted_EDS_ClearVerdict THEN wBHS_StatusWord := wBHS_StatusWord OR 16#0008; END_IF;
IF bInduction_PacerBrake_Cmd THEN wBHS_StatusWord := wBHS_StatusWord OR 16#0010; END_IF;
IF bEDS_RejectDiverter_Fire THEN wBHS_StatusWord := wBHS_StatusWord OR 16#0020; END_IF;
IF bSecurityBreach_Lockdown THEN wBHS_StatusWord := wBHS_StatusWord OR 16#0040; END_IF;
IF diActiveTrackedBags_Count >= 8 THEN wBHS_StatusWord := wBHS_StatusWord OR 16#0080; END_IF;

(* wSorter_StatusWord:
   Bit 0: Sorter Track At Synchronous Speed
   Bit 1: LSM Inverter Running
   Bit 2: Dynamic Regenerative Braking Active
   Bit 3: Divert Shoe In Home Position
   Bit 4: Divert Shoe In Diverted Position
   Bit 5: Chute Discharge Conveyor Running
   Bit 6: Chute Friction Retarder Active
   Bit 7: Sorter Permissive Interlock OK *)
wSorter_StatusWord := 16#0000;
IF ABS(rTraySorter_LinearSpeed_mps - rLSM_TargetVelocity_mps) < 0.20 THEN wSorter_StatusWord := wSorter_StatusWord OR 16#0001; END_IF;
IF rLSM_ThrustCurrent_Pct > 5.0 THEN wSorter_StatusWord := wSorter_StatusWord OR 16#0002; END_IF;
IF bLSM_RegenerativeBrake_En THEN wSorter_StatusWord := wSorter_StatusWord OR 16#0004; END_IF;
IF bShoeHome_Sensor THEN wSorter_StatusWord := wSorter_StatusWord OR 16#0008; END_IF;
IF bShoeDiverted_Sensor THEN wSorter_StatusWord := wSorter_StatusWord OR 16#0010; END_IF;
IF bChute_DischargeBelt_Run THEN wSorter_StatusWord := wSorter_StatusWord OR 16#0020; END_IF;
IF rChute_BrakeModulation_Pct > 10.0 THEN wSorter_StatusWord := wSorter_StatusWord OR 16#0040; END_IF;
IF bSystemInterlock_Permissive THEN wSorter_StatusWord := wSorter_StatusWord OR 16#0080; END_IF;
"""
    sections.append(sec9)

    # ==========================================
    # SECTION 10: MULTI-STAGE FINITE STATE MACHINE
    # ==========================================
    sec10 = """(* ========================================================================= *)
(* PHASE 8: MULTI-STAGE LINE FINITE STATE MACHINE (FSM)                       *)
(* ========================================================================= *)
IF nFSM_CurrentState = nFSM_PreviousState THEN
    rStateTimer_s := rStateTimer_s + tScanTime_s;
    IF rStateTimer_s >= rStateTimeout_s THEN
        bStateTimeout_Alarm := TRUE;
    END_IF;
ELSE
    rStateTimer_s := 0.0;
    bStateTimeout_Alarm := FALSE;
    nFSM_PreviousState := nFSM_CurrentState;
END_IF;

bSystemInterlock_Permissive := bSystemAuto_Run_Cmd AND bSafetyZone_Clear AND (NOT bEmergencyStop_Active) AND (wAlarmWord_PriorityHH = 16#0000);

IF NOT bSystemInterlock_Permissive AND nFSM_CurrentState <> 70 THEN
    nFSM_CurrentState := 99; (* EMERGENCY_STOP_SAFE_HOLD *)
END_IF;

CASE nFSM_CurrentState OF
    (* ------------------------------------------------------------- *)
    (* STATE 0: BHS SYSTEM INITIALIZE & DRIVE CALIBRATION            *)
    (* ------------------------------------------------------------- *)
    0:
        rStateTimeout_s := 30.0;
        rInduction_BeltSpeed_mps := 0.0;
        rInfeedVFD_Frequency_Hz := 0.0;
        bInduction_PacerBrake_Cmd := TRUE;
        bEDS_RejectDiverter_Fire := FALSE;
        bEDS_ClearPass_Permit := FALSE;
        bShoeDivert_Fire_Cmd := FALSE;
        rShoeDivert_ServoFlow_Pct := 0.0;
        bChute_DischargeBelt_Run := FALSE;
        rChute_BrakeModulation_Pct := 0.0;
        
        IF bSystemInterlock_Permissive AND (rDivert_SupplyPress_bar >= 5.5) THEN
            bInduction_PacerBrake_Cmd := FALSE;
            nFSM_CurrentState := 10; (* Transition to CONVEYOR_VELOCITY_CASCADE *)
        END_IF;

    (* ------------------------------------------------------------- *)
    (* STATE 10: CONVEYOR VELOCITY CASCADE & LSM CRUISE RAMP-UP      *)
    (* ------------------------------------------------------------- *)
    10:
        rStateTimeout_s := 45.0;
        (* Accelerate metering belt and LSM sorter up to cruise velocity *)
        rInduction_BeltSpeed_mps := 2.5;
        rInfeedVFD_Frequency_Hz := vecControl_u[2];
        rLSM_TargetVelocity_mps := 7.5;
        bChute_DischargeBelt_Run := TRUE;
        
        (* When sorter and infeed match target velocities *)
        IF ABS(rTraySorter_LinearSpeed_mps - 7.5) < 0.35 AND ABS(rVoted_ConveyorSpeed_mps - 2.5) < 0.20 THEN
            bEDS_ClearPass_Permit := TRUE;
            nFSM_CurrentState := 20; (* Transition to 360_LASER_TAG_IDENTIFICATION *)
        END_IF;

    (* ------------------------------------------------------------- *)
    (* STATE 20: 360-DEGREE SCANNER & INFEED PACING REGULATION       *)
    (* ------------------------------------------------------------- *)
    20:
        rStateTimeout_s := 50.0;
        rInduction_BeltSpeed_mps := 2.5;
        rInfeedVFD_Frequency_Hz := vecControl_u[2];
        
        (* Baggage identified on induction buffer *)
        IF bVoted_Induction_PE THEN
            IF bBarcode_ReadValid THEN
                nFSM_CurrentState := 30; (* Proceed to EDS Security Screening *)
            ELSE
                (* Unreadable tag: route to manual re-scan line *)
                nFSM_CurrentState := 30;
            END_IF;
        END_IF;

    (* ------------------------------------------------------------- *)
    (* STATE 30: IN-LINE EDS COMPUTED TOMOGRAPHY SCREENING DIVERT    *)
    (* ------------------------------------------------------------- *)
    30:
        rStateTimeout_s := 25.0;
        
        IF bVoted_EDS_ClearVerdict AND (NOT bEDS_Threat_Suspect_Bit) THEN
            (* Cleared bag: allow entry into main tray sorter *)
            bEDS_RejectDiverter_Fire := FALSE;
            bEDS_ClearPass_Permit := TRUE;
            nFSM_CurrentState := 40; (* Transition to MAIN_TRAY_SORTATION_CRUISE *)
        ELSE
            (* Threat/Suspect Bag: fire reject diverter into Level 3 loop *)
            bEDS_RejectDiverter_Fire := TRUE;
            bEDS_ClearPass_Permit := FALSE;
            IF rStateTimer_s > 1.2 THEN
                bEDS_RejectDiverter_Fire := FALSE;
                nFSM_CurrentState := 70; (* Transition to LEVEL3_SUSPECT_BAG_CLEARING *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------- *)
    (* STATE 40: MAIN TRAY SORTATION CRUISE & TARGET CHUTE TRACKING  *)
    (* ------------------------------------------------------------- *)
    40:
        rStateTimeout_s := 60.0;
        rLSM_TargetVelocity_mps := 7.5;
        
        (* Check if lead bag in FIFO has arrived at its assigned flight chute *)
        IF aBag_ActiveInWindow[1] THEN
            (* Trigger pneumatic shoe divert when bag reaches destination chute window *)
            IF aBag_CartesianPos_mm[1] >= 8500.0 THEN
                nFSM_CurrentState := 50; (* Transition to HIGH_SPEED_DIVERT_SHOE_FIRE *)
            END_IF;
        ELSE
            (* No active bag at chute entry: stay in steady cruise *)
            nFSM_CurrentState := 20;
        END_IF;

    (* ------------------------------------------------------------- *)
    (* STATE 50: HIGH-SPEED PNEUMATIC DIVERT SHOE ACTIVATION         *)
    (* ------------------------------------------------------------- *)
    50:
        rStateTimeout_s := 15.0;
        
        (* Fire high-speed pneumatic divert shoe *)
        bShoeDivert_Fire_Cmd := TRUE;
        rShoeDivert_ServoFlow_Pct := vecControl_u[3];
        
        IF bShoeDiverted_Sensor OR (rStateTimer_s > (rDivert_StrokeTime_ms * 0.001)) THEN
            bShoeDivert_Fire_Cmd := FALSE;
            rShoeDivert_ServoFlow_Pct := 0.0;
            nFSM_CurrentState := 60; (* Transition to CHUTE_FLIGHT_DISCHARGE *)
        END_IF;

    (* ------------------------------------------------------------- *)
    (* STATE 60: CHUTE FLIGHT DISCHARGE & MAKE-UP CONVEYOR BRAKING   *)
    (* ------------------------------------------------------------- *)
    60:
        rStateTimeout_s := 25.0;
        rChute_BrakeModulation_Pct := vecControl_u[4];
        
        IF bShoeHome_Sensor AND (rStateTimer_s > 0.85) THEN
            rChute_BrakeModulation_Pct := 0.0;
            nFSM_CurrentState := 20; (* Return to scanner intake loop *)
        END_IF;

    (* ------------------------------------------------------------- *)
    (* STATE 70: LEVEL 3 SUSPECT BAG CLEARING & RECOVERY             *)
    (* ------------------------------------------------------------- *)
    70:
        rStateTimeout_s := 40.0;
        (* Continue running main line to prevent terminal gridlock while suspect bag is isolated *)
        bEDS_ClearPass_Permit := TRUE;
        
        IF bAlarmReset_PB THEN
            bSecurityBreach_Lockdown := FALSE;
            nFSM_CurrentState := 20;
        END_IF;

    (* ------------------------------------------------------------- *)
    (* STATE 99: SECURITY LOCKDOWN & EMERGENCY SHUTDOWN HOLD         *)
    (* ------------------------------------------------------------- *)
    99:
        rInduction_BeltSpeed_mps := 0.0;
        rInfeedVFD_Frequency_Hz := 0.0;
        bInduction_PacerBrake_Cmd := TRUE;
        bEDS_RejectDiverter_Fire := FALSE;
        bEDS_ClearPass_Permit := FALSE;
        rLSM_TargetVelocity_mps := 0.0;
        rLSM_ThrustCurrent_Pct := 0.0;
        bLSM_RegenerativeBrake_En := TRUE;
        bShoeDivert_Fire_Cmd := FALSE;
        rShoeDivert_ServoFlow_Pct := 0.0;
        bChute_DischargeBelt_Run := FALSE;
        
        IF bAlarmReset_PB AND bSystemInterlock_Permissive THEN
            bSecurityBreach_Lockdown := FALSE;
            nFSM_CurrentState := 0; (* Reset to Init *)
        END_IF;
END_CASE;
"""
    sections.append(sec10)

    # ==========================================
    # SECTION 11: HARDWARE OUTPUT CLAMPING & END BLOCK
    # ==========================================
    sec11 = """(* ========================================================================= *)
(* PHASE 9: ACTUATOR OUTPUT HARDWARE CLAMPING & SAFETY ENFORCEMENT           *)
(* ========================================================================= *)
(* Induction Belt Speed Clamping [0.0 .. 4.5 m/s] *)
IF rInduction_BeltSpeed_mps > 4.5 THEN
    rInduction_BeltSpeed_mps := 4.5;
ELSIF rInduction_BeltSpeed_mps < 0.0 THEN
    rInduction_BeltSpeed_mps := 0.0;
END_IF;

(* Infeed VFD Frequency Clamping [0.0 .. 65.0 Hz] *)
IF rInfeedVFD_Frequency_Hz > 65.0 THEN
    rInfeedVFD_Frequency_Hz := 65.0;
ELSIF rInfeedVFD_Frequency_Hz < 0.0 THEN
    rInfeedVFD_Frequency_Hz := 0.0;
END_IF;

(* LSM Thrust Current Clamping [0.0 .. 100.0 %] *)
IF rLSM_ThrustCurrent_Pct > 100.0 THEN
    rLSM_ThrustCurrent_Pct := 100.0;
ELSIF rLSM_ThrustCurrent_Pct < 0.0 THEN
    rLSM_ThrustCurrent_Pct := 0.0;
END_IF;

(* LSM Target Velocity Clamping [0.0 .. 12.0 m/s] *)
IF rLSM_TargetVelocity_mps > 12.0 THEN
    rLSM_TargetVelocity_mps := 12.0;
ELSIF rLSM_TargetVelocity_mps < 0.0 THEN
    rLSM_TargetVelocity_mps := 0.0;
END_IF;

(* Shoe Divert Servo Flow Clamping [0.0 .. 100.0 %] *)
IF rShoeDivert_ServoFlow_Pct > 100.0 THEN
    rShoeDivert_ServoFlow_Pct := 100.0;
ELSIF rShoeDivert_ServoFlow_Pct < 0.0 THEN
    rShoeDivert_ServoFlow_Pct := 0.0;
END_IF;

(* Chute Brake Modulation Clamping [0.0 .. 100.0 %] *)
IF rChute_BrakeModulation_Pct > 100.0 THEN
    rChute_BrakeModulation_Pct := 100.0;
ELSIF rChute_BrakeModulation_Pct < 0.0 THEN
    rChute_BrakeModulation_Pct := 0.0;
END_IF;

END_FUNCTION_BLOCK
"""
    sections.append(sec11)

    return "\n".join(sections)

if __name__ == "__main__":
    code = build_bhs_block()
    print(f"Total ST code length: {len(code)} characters")
