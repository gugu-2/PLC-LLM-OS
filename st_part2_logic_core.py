# st_part2_logic_core.py

def get_logic_core():
    return """
(* ========================================================================================= *)
(* === MAIN LOGIC EXECUTION BODY                                                         === *)
(* ========================================================================================= *)

(* Update global continuous execution timer *)
rGlobalProcessRuntime_s := rGlobalProcessRuntime_s + rCycleTime_s;

(* ========================================================================================= *)
(* SEGMENT 1: SYSTEM INITIALIZATION & STATE-SPACE MATRIX POPULATION                          *)
(* ========================================================================================= *)
IF NOT bInitialized THEN
    (* Continuous Plant Matrix A (4x4) - Derived from thermal-fluid perturbation at 1,800 deg C *)
    (* dx1/dt: Cavity Refractory Temp dynamics *)
    aA_Cont[1, 1] := -0.0425;  (* Self-radiation & conduction dissipation *)
    aA_Cont[1, 2] :=  0.0085;  (* Radiative exchange with quartz window *)
    aA_Cont[1, 3] := -0.0150;  (* Endothermic reaction heat sink *)
    aA_Cont[1, 4] :=  0.0000;

    (* dx2/dt: Quartz Window Temp dynamics *)
    aA_Cont[2, 1] :=  0.0120;  (* Radiative absorption from 1,800 C cavity *)
    aA_Cont[2, 2] := -0.0850;  (* Convective cooling from argon sweep & ambient *)
    aA_Cont[2, 3] :=  0.0000;
    aA_Cont[2, 4] :=  0.0000;

    (* dx3/dt: Zinc Vapor Core Density dynamics *)
    aA_Cont[3, 1] :=  0.0650;  (* Thermochemical vaporization kinetics *)
    aA_Cont[3, 2] :=  0.0000;
    aA_Cont[3, 3] := -0.1450;  (* Convective outflow towards quench zone *)
    aA_Cont[3, 4] :=  0.0000;

    (* dx4/dt: Quench Boundary Layer Temp dynamics *)
    aA_Cont[4, 1] :=  0.0000;
    aA_Cont[4, 2] :=  0.0000;
    aA_Cont[4, 3] :=  0.0350;  (* Hot vapor entrainment heat flux *)
    aA_Cont[4, 4] := -0.3200;  (* High-speed supersonic argon chilling *)

    (* Continuous Input Matrix B (4x3) *)
    (* Inputs: u1 = Attenuator [%], u2 = Quench Flow [%], u3 = Window Sweep [%] *)
    aB_Cont[1, 1] :=  0.8500;  (* Attenuator modulates concentrated solar flux *)
    aB_Cont[1, 2] :=  0.0000;
    aB_Cont[1, 3] := -0.0040;  (* Slight sweep gas cooling penetration *)

    aB_Cont[2, 1] :=  0.1500;  (* Transmitted solar flux absorption *)
    aB_Cont[2, 2] :=  0.0000;
    aB_Cont[2, 3] := -0.6200;  (* Vortex sweep gas convection cooling *)

    aB_Cont[3, 1] :=  0.0550;  (* Thermal dissociation drive *)
    aB_Cont[3, 2] := -0.0250;  (* Dilution by quench flow *)
    aB_Cont[3, 3] := -0.0100;  (* Sweep gas displacement *)

    aB_Cont[4, 1] :=  0.0000;
    aB_Cont[4, 2] := -1.4500;  (* Direct supersonic quench cooling *)
    aB_Cont[4, 3] :=  0.0000;

    (* Continuous Disturbance Matrix Bd (4x3) *)
    (* Disturbances: d1 = DNI [W/m2], d2 = ZnO Feed [kg/h], d3 = Wind [m/s] *)
    aBd_Cont[1, 1] :=  0.00185; (* Solar DNI direct solar flux input *)
    aBd_Cont[1, 2] := -0.12500; (* Endothermic powder sensible & reaction load *)
    aBd_Cont[1, 3] := -0.00500; (* External shell wind dissipation *)

    aBd_Cont[2, 1] :=  0.00035; (* DNI direct absorption in quartz *)
    aBd_Cont[2, 2] :=  0.00000;
    aBd_Cont[2, 3] := -0.01200; (* External window convective wind cooling *)

    aBd_Cont[3, 1] :=  0.00010;
    aBd_Cont[3, 2] :=  0.28500; (* Direct reactant mass addition *)
    aBd_Cont[3, 3] :=  0.00000;

    aBd_Cont[4, 1] :=  0.00000;
    aBd_Cont[4, 2] :=  0.01500;
    aBd_Cont[4, 3] := -0.00200;

    (* Output Matrix C (4x4) - Identity mapping *)
    aC_Cont[1, 1] := 1.0; aC_Cont[1, 2] := 0.0; aC_Cont[1, 3] := 0.0; aC_Cont[1, 4] := 0.0;
    aC_Cont[2, 1] := 0.0; aC_Cont[2, 2] := 1.0; aC_Cont[2, 3] := 0.0; aC_Cont[2, 4] := 0.0;
    aC_Cont[3, 1] := 0.0; aC_Cont[3, 2] := 0.0; aC_Cont[3, 3] := 1.0; aC_Cont[3, 4] := 0.0;
    aC_Cont[4, 1] := 0.0; aC_Cont[4, 2] := 0.0; aC_Cont[4, 3] := 0.0; aC_Cont[4, 4] := 1.0;

    (* Discretization using 1st-Order Euler Approximation: Ad = I + A*dt, Bd = B*dt *)
    aA_Disc[1, 1] := 1.0 + aA_Cont[1, 1] * rCycleTime_s;
    aA_Disc[1, 2] := aA_Cont[1, 2] * rCycleTime_s;
    aA_Disc[1, 3] := aA_Cont[1, 3] * rCycleTime_s;
    aA_Disc[1, 4] := aA_Cont[1, 4] * rCycleTime_s;

    aA_Disc[2, 1] := aA_Cont[2, 1] * rCycleTime_s;
    aA_Disc[2, 2] := 1.0 + aA_Cont[2, 2] * rCycleTime_s;
    aA_Disc[2, 3] := aA_Cont[2, 3] * rCycleTime_s;
    aA_Disc[2, 4] := aA_Cont[2, 4] * rCycleTime_s;

    aA_Disc[3, 1] := aA_Cont[3, 1] * rCycleTime_s;
    aA_Disc[3, 2] := aA_Cont[3, 2] * rCycleTime_s;
    aA_Disc[3, 3] := 1.0 + aA_Cont[3, 3] * rCycleTime_s;
    aA_Disc[3, 4] := aA_Cont[3, 4] * rCycleTime_s;

    aA_Disc[4, 1] := aA_Cont[4, 1] * rCycleTime_s;
    aA_Disc[4, 2] := aA_Cont[4, 2] * rCycleTime_s;
    aA_Disc[4, 3] := aA_Cont[4, 3] * rCycleTime_s;
    aA_Disc[4, 4] := 1.0 + aA_Cont[4, 4] * rCycleTime_s;

    aB_Disc[1, 1] := aB_Cont[1, 1] * rCycleTime_s;
    aB_Disc[1, 2] := aB_Cont[1, 2] * rCycleTime_s;
    aB_Disc[1, 3] := aB_Cont[1, 3] * rCycleTime_s;
    aB_Disc[2, 1] := aB_Cont[2, 1] * rCycleTime_s;
    aB_Disc[2, 2] := aB_Cont[2, 2] * rCycleTime_s;
    aB_Disc[2, 3] := aB_Cont[2, 3] * rCycleTime_s;
    aB_Disc[3, 1] := aB_Cont[3, 1] * rCycleTime_s;
    aB_Disc[3, 2] := aB_Cont[3, 2] * rCycleTime_s;
    aB_Disc[3, 3] := aB_Cont[3, 3] * rCycleTime_s;
    aB_Disc[4, 1] := aB_Cont[4, 1] * rCycleTime_s;
    aB_Disc[4, 2] := aB_Cont[4, 2] * rCycleTime_s;
    aB_Disc[4, 3] := aB_Cont[4, 3] * rCycleTime_s;

    aBd_Disc[1, 1] := aBd_Cont[1, 1] * rCycleTime_s;
    aBd_Disc[1, 2] := aBd_Cont[1, 2] * rCycleTime_s;
    aBd_Disc[1, 3] := aBd_Cont[1, 3] * rCycleTime_s;
    aBd_Disc[2, 1] := aBd_Cont[2, 1] * rCycleTime_s;
    aBd_Disc[2, 2] := aBd_Cont[2, 2] * rCycleTime_s;
    aBd_Disc[2, 3] := aBd_Cont[2, 3] * rCycleTime_s;
    aBd_Disc[3, 1] := aBd_Cont[3, 1] * rCycleTime_s;
    aBd_Disc[3, 2] := aBd_Cont[3, 2] * rCycleTime_s;
    aBd_Disc[3, 3] := aBd_Cont[3, 3] * rCycleTime_s;
    aBd_Disc[4, 1] := aBd_Cont[4, 1] * rCycleTime_s;
    aBd_Disc[4, 2] := aBd_Cont[4, 2] * rCycleTime_s;
    aBd_Disc[4, 3] := aBd_Cont[4, 3] * rCycleTime_s;

    (* Observer Gain Matrix L (4x4) *)
    aL_Obs[1, 1] := 0.350; aL_Obs[1, 2] := 0.010; aL_Obs[1, 3] := 0.005; aL_Obs[1, 4] := 0.000;
    aL_Obs[2, 1] := 0.015; aL_Obs[2, 2] := 0.420; aL_Obs[2, 3] := 0.000; aL_Obs[2, 4] := 0.000;
    aL_Obs[3, 1] := 0.020; aL_Obs[3, 2] := 0.000; aL_Obs[3, 3] := 0.550; aL_Obs[3, 4] := 0.010;
    aL_Obs[4, 1] := 0.000; aL_Obs[4, 2] := 0.000; aL_Obs[4, 3] := 0.015; aL_Obs[4, 4] := 0.650;

    (* MPC Quadratic Weights: State Tracking Penalty Q *)
    aQ_Weight[1, 1] := 25.0;  (* Cavity temp deviation penalty *)
    aQ_Weight[2, 2] := 45.0;  (* Quartz window temp critical penalty *)
    aQ_Weight[3, 3] := 15.0;  (* Zinc vapor density penalty *)
    aQ_Weight[4, 4] := 30.0;  (* Quench boundary layer temp penalty *)

    (* MPC Control Slew Penalty R *)
    aR_Weight[1, 1] := 5.0;   (* Attenuator mechanical wear penalty *)
    aR_Weight[2, 2] := 1.2;   (* Quench argon consumption penalty *)
    aR_Weight[3, 3] := 2.0;   (* Window sweep argon consumption penalty *)

    (* Actuator Hard Saturation Bounds *)
    aU_Min[1] := 0.0;   aU_Max[1] := 100.0;  (* Attenuator [%] *)
    aU_Min[2] := 15.0;  aU_Max[2] := 100.0;  (* Quench Flow Min 15% to prevent back-flow *)
    aU_Min[3] := 20.0;  aU_Max[3] := 100.0;  (* Window Sweep Min 20% to prevent deposition *)

    aDeltaU_Min[1] := -15.0; aDeltaU_Max[1] := 15.0;
    aDeltaU_Min[2] := -20.0; aDeltaU_Max[2] := 20.0;
    aDeltaU_Min[3] := -10.0; aDeltaU_Max[3] := 10.0;

    (* Setpoint Vector y_ref *)
    aY_Setpoint[1] := 1800.0; (* Cavity Temp: 1,800.0 deg C *)
    aY_Setpoint[2] := 680.0;  (* Window Temp limit: 680.0 deg C (safe below 950 C) *)
    aY_Setpoint[3] := 18.5;   (* Target core Zn vapor density [g/m3] *)
    aY_Setpoint[4] := 350.0;  (* Quench boundary layer temp: 350.0 deg C *)

    bInitialized := TRUE;
END_IF;

(* ========================================================================================= *)
(* SEGMENT 2: HARDWIRED SAFETY INTERLOCKS & TRIP SUPERVISION                                 *)
(* ========================================================================================= *)
IF NOT bEmergencyStop THEN
    (* Immediate Fail-Safe Trip Trigger *)
    bReactorOperational := FALSE;
    bFastOpticalShutterClose := TRUE;
    bHeliostatDefocusCommand := TRUE;
    rZnO_FeederSpeedCmd_pct := 0.0;
    rApertureAttenuatorPosition_pct := 0.0;
    
    (* Maximally boost protective inert sweeps during emergency shutdown *)
    rWindowPurgeValveCmd_pct := 100.0;
    rQuenchCurtainValveCmd_pct := 100.0;

    IF NOT bFirstOutRecorded THEN
        dwAlarmWordFirstOut := 16#00000001; (* Bit 0: Emergency Stop Trip *)
        bFirstOutRecorded := TRUE;
        tFirstOutTimestamp_s := rGlobalProcessRuntime_s;
    END_IF;

    iState := 100; (* Jump directly to EMERGENCY_DEFOCUS state *)
END_IF;

(* ========================================================================================= *)
(* SEGMENT 3: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING ENGINES                            *)
(* ========================================================================================= *)
(* Group 1: Cavity Receiver Optical Pyrometers (A, B, C) *)
(* Range check: 0.0 deg C to 2200.0 deg C *)
bCavityTemp_A_Healthy := (rCavityPyrometerTemp_A_degC >= 0.0) AND (rCavityPyrometerTemp_A_degC <= 2200.0);
bCavityTemp_B_Healthy := (rCavityPyrometerTemp_B_degC >= 0.0) AND (rCavityPyrometerTemp_B_degC <= 2200.0);
bCavityTemp_C_Healthy := (rCavityPyrometerTemp_C_degC >= 0.0) AND (rCavityPyrometerTemp_C_degC <= 2200.0);

IF bCavityTemp_A_Healthy AND bCavityTemp_B_Healthy AND bCavityTemp_C_Healthy THEN
    (* All 3 channels healthy: Median Select Voting *)
    IF (rCavityPyrometerTemp_A_degC >= rCavityPyrometerTemp_B_degC) AND (rCavityPyrometerTemp_A_degC <= rCavityPyrometerTemp_C_degC) OR
       (rCavityPyrometerTemp_A_degC >= rCavityPyrometerTemp_C_degC) AND (rCavityPyrometerTemp_A_degC <= rCavityPyrometerTemp_B_degC) THEN
        rVotedCavityTemp_degC := rCavityPyrometerTemp_A_degC;
    ELSIF (rCavityPyrometerTemp_B_degC >= rCavityPyrometerTemp_A_degC) AND (rCavityPyrometerTemp_B_degC <= rCavityPyrometerTemp_C_degC) OR
          (rCavityPyrometerTemp_B_degC >= rCavityPyrometerTemp_C_degC) AND (rCavityPyrometerTemp_B_degC <= rCavityPyrometerTemp_A_degC) THEN
        rVotedCavityTemp_degC := rCavityPyrometerTemp_B_degC;
    ELSE
        rVotedCavityTemp_degC := rCavityPyrometerTemp_C_degC;
    END_IF;

    (* Discrepancy Detection: Check if any single channel deviates by > 65 deg C from median *)
    IF (ABS(rCavityPyrometerTemp_A_degC - rVotedCavityTemp_degC) > 65.0) OR
       (ABS(rCavityPyrometerTemp_B_degC - rVotedCavityTemp_degC) > 65.0) OR
       (ABS(rCavityPyrometerTemp_C_degC - rVotedCavityTemp_degC) > 65.0) THEN
        rCavityTemp_DiscrepancyTimer_s := rCavityTemp_DiscrepancyTimer_s + rCycleTime_s;
    ELSE
        rCavityTemp_DiscrepancyTimer_s := 0.0;
    END_IF;
ELSIF bCavityTemp_A_Healthy AND bCavityTemp_B_Healthy THEN
    (* Degraded 1oo2: Average of A and B *)
    rVotedCavityTemp_degC := (rCavityPyrometerTemp_A_degC + rCavityPyrometerTemp_B_degC) * 0.5;
ELSIF bCavityTemp_A_Healthy AND bCavityTemp_C_Healthy THEN
    rVotedCavityTemp_degC := (rCavityPyrometerTemp_A_degC + rCavityPyrometerTemp_C_degC) * 0.5;
ELSIF bCavityTemp_B_Healthy AND bCavityTemp_C_Healthy THEN
    rVotedCavityTemp_degC := (rCavityPyrometerTemp_B_degC + rCavityPyrometerTemp_C_degC) * 0.5;
ELSIF bCavityTemp_A_Healthy THEN
    rVotedCavityTemp_degC := rCavityPyrometerTemp_A_degC;
ELSIF bCavityTemp_B_Healthy THEN
    rVotedCavityTemp_degC := rCavityPyrometerTemp_B_degC;
ELSIF bCavityTemp_C_Healthy THEN
    rVotedCavityTemp_degC := rCavityPyrometerTemp_C_degC;
ELSE
    (* Complete TMR Sensor Failure -> Immediate Trip *)
    bReactorOperational := FALSE;
    bFastOpticalShutterClose := TRUE;
    bHeliostatDefocusCommand := TRUE;
    IF NOT bFirstOutRecorded THEN
        dwAlarmWordFirstOut := 16#00000002; (* Bit 1: Cavity Pyrometer TMR Complete Loss *)
        bFirstOutRecorded := TRUE;
    END_IF;
END_IF;

(* Group 2: Aperture Incident Solar Calorimeter Flux Radiometers (A, B, C) *)
bSolarFlux_A_Healthy := (rApertureIncidentFlux_A_kW_m2 >= 0.0) AND (rApertureIncidentFlux_A_kW_m2 <= 5000.0);
bSolarFlux_B_Healthy := (rApertureIncidentFlux_B_kW_m2 >= 0.0) AND (rApertureIncidentFlux_B_kW_m2 <= 5000.0);
bSolarFlux_C_Healthy := (rApertureIncidentFlux_C_kW_m2 >= 0.0) AND (rApertureIncidentFlux_C_kW_m2 <= 5000.0);

IF bSolarFlux_A_Healthy AND bSolarFlux_B_Healthy AND bSolarFlux_C_Healthy THEN
    IF (rApertureIncidentFlux_A_kW_m2 >= rApertureIncidentFlux_B_kW_m2) AND (rApertureIncidentFlux_A_kW_m2 <= rApertureIncidentFlux_C_kW_m2) OR
       (rApertureIncidentFlux_A_kW_m2 >= rApertureIncidentFlux_C_kW_m2) AND (rApertureIncidentFlux_A_kW_m2 <= rApertureIncidentFlux_B_kW_m2) THEN
        rVotedSolarFlux_kW_m2 := rApertureIncidentFlux_A_kW_m2;
    ELSIF (rApertureIncidentFlux_B_kW_m2 >= rApertureIncidentFlux_A_kW_m2) AND (rApertureIncidentFlux_B_kW_m2 <= rApertureIncidentFlux_C_kW_m2) OR
          (rApertureIncidentFlux_B_kW_m2 >= rApertureIncidentFlux_C_kW_m2) AND (rApertureIncidentFlux_B_kW_m2 <= rApertureIncidentFlux_A_kW_m2) THEN
        rVotedSolarFlux_kW_m2 := rApertureIncidentFlux_B_kW_m2;
    ELSE
        rVotedSolarFlux_kW_m2 := rApertureIncidentFlux_C_kW_m2;
    END_IF;
ELSIF bSolarFlux_A_Healthy AND bSolarFlux_B_Healthy THEN
    rVotedSolarFlux_kW_m2 := (rApertureIncidentFlux_A_kW_m2 + rApertureIncidentFlux_B_kW_m2) * 0.5;
ELSIF bSolarFlux_A_Healthy AND bSolarFlux_C_Healthy THEN
    rVotedSolarFlux_kW_m2 := (rApertureIncidentFlux_A_kW_m2 + rApertureIncidentFlux_C_kW_m2) * 0.5;
ELSIF bSolarFlux_B_Healthy AND bSolarFlux_C_Healthy THEN
    rVotedSolarFlux_kW_m2 := (rApertureIncidentFlux_B_kW_m2 + rApertureIncidentFlux_C_kW_m2) * 0.5;
ELSE
    rVotedSolarFlux_kW_m2 := 0.0;
END_IF;

(* Group 3: Fused Quartz Aperture Window IR Thermopiles (A, B, C) *)
(* Quartz window uses HIGH-SELECT voting for conservative thermal protection *)
bWindowTemp_A_Healthy := (rQuartzWindowTemp_A_degC >= 0.0) AND (rQuartzWindowTemp_A_degC <= 1400.0);
bWindowTemp_B_Healthy := (rQuartzWindowTemp_B_degC >= 0.0) AND (rQuartzWindowTemp_B_degC <= 1400.0);
bWindowTemp_C_Healthy := (rQuartzWindowTemp_C_degC >= 0.0) AND (rQuartzWindowTemp_C_degC <= 1400.0);

IF bWindowTemp_A_Healthy AND bWindowTemp_B_Healthy AND bWindowTemp_C_Healthy THEN
    (* Select maximum temperature to prevent localized hotspot breach *)
    rVotedWindowTemp_degC := rQuartzWindowTemp_A_degC;
    IF rQuartzWindowTemp_B_degC > rVotedWindowTemp_degC THEN rVotedWindowTemp_degC := rQuartzWindowTemp_B_degC; END_IF;
    IF rQuartzWindowTemp_C_degC > rVotedWindowTemp_degC THEN rVotedWindowTemp_degC := rQuartzWindowTemp_C_degC; END_IF;
ELSIF bWindowTemp_A_Healthy AND bWindowTemp_B_Healthy THEN
    IF rQuartzWindowTemp_A_degC > rQuartzWindowTemp_B_degC THEN rVotedWindowTemp_degC := rQuartzWindowTemp_A_degC; ELSE rVotedWindowTemp_degC := rQuartzWindowTemp_B_degC; END_IF;
ELSIF bWindowTemp_A_Healthy THEN
    rVotedWindowTemp_degC := rQuartzWindowTemp_A_degC;
ELSIF bWindowTemp_B_Healthy THEN
    rVotedWindowTemp_degC := rQuartzWindowTemp_B_degC;
ELSIF bWindowTemp_C_Healthy THEN
    rVotedWindowTemp_degC := rQuartzWindowTemp_C_degC;
ELSE
    rVotedWindowTemp_degC := 999.0; (* Fail-safe trip high *)
END_IF;

(* Group 4: Quench Nozzle Inlet Pressure Transmitters *)
bQuenchPress_A_Healthy := (rQuenchNozzleInletPress_bar >= 0.0) AND (rQuenchNozzleInletPress_bar <= 30.0);
bQuenchPress_B_Healthy := (rQuenchNozzleInletPress_bar >= 0.0) AND (rQuenchNozzleInletPress_bar <= 30.0);
bQuenchPress_C_Healthy := (rQuenchNozzleInletPress_bar >= 0.0) AND (rQuenchNozzleInletPress_bar <= 30.0);

rVotedQuenchPress_bar := rQuenchNozzleInletPress_bar;

(* ========================================================================================= *)
(* SEGMENT 4: SIGNAL CONDITIONING, CERAMIC REFRACTORY STRESS & QUARTZ TRANSMISSIVITY        *)
(* ========================================================================================= *)
(* SiC Refractory Cavity Radial Temperature Gradient & von Mises Stress *)
(* Fourier's Law conduction across cylindrical shell: q_cond = -k * dT/dr *)
rCavityRadialTempDiff_degC := (rVotedCavityTemp_degC - 350.0) * (rCavityWallThickness_m / 0.15);
IF rCavityRadialTempDiff_degC < 0.0 THEN rCavityRadialTempDiff_degC := 0.0; END_IF;

(* Thermo-mechanical hoop stress: sigma_theta = E * alpha * DeltaT / (2 * (1 - nu)) *)
rCavityHoopStress_MPa := (rSiC_YoungsModulus_GPa * 1000.0 * rSiC_ThermalExpansion_perK * rCavityRadialTempDiff_degC) / (2.0 * (1.0 - rSiC_PoissonsRatio));

(* Von Mises Stress taking into account fiber optic measured microstrain *)
rCavityVonMisesStress_MPa := SQRT(rCavityHoopStress_MPa * rCavityHoopStress_MPa + (rCavityCeramicStrain_microstrain * 0.001 * rSiC_YoungsModulus_GPa) * (rCavityCeramicStrain_microstrain * 0.001 * rSiC_YoungsModulus_GPa));
rCeramicRefractoryStress_MPa := rCavityVonMisesStress_MPa;

(* Fused Quartz Window Transmissivity Degradation & Cristobalite Phase Transformation *)
(* Nucleation Rate of beta-Cristobalite accelerates exponentially at T > 950 deg C *)
IF rVotedWindowTemp_degC > 950.0 THEN
    rCristobaliteNucleationRate := 1.25E-04 * EXP((rVotedWindowTemp_degC - 950.0) / 45.0);
    rCristobaliteCumulativeIntegral := rCristobaliteCumulativeIntegral + rCristobaliteNucleationRate * rCycleTime_s;
ELSE
    rCristobaliteNucleationRate := 0.0;
END_IF;

IF rCristobaliteCumulativeIntegral > 100.0 THEN rCristobaliteCumulativeIntegral := 100.0; END_IF;
rQuartzDevitrificationRisk_pct := rCristobaliteCumulativeIntegral;

(* ========================================================================================= *)
(* SEGMENT 5: NON-STOICHIOMETRIC REDOX KINETIC OBSERVER (ZnO_1-delta)                        *)
(* ========================================================================================= *)
(* Temperature in Kelvin: T_K = T_C + 273.15 *)
(* Standard Gibbs Free Energy: Delta G(T) = Delta H - T * Delta S *)
(* Delta H = 461,300 J/mol, Delta S = 288.5 J/(mol K) *)
rThermodynamicAffinity_kJ_mol := (rStdEnthalpy_kJ_mol * 1000.0 - (rVotedCavityTemp_degC + 273.15) * rStdEntropy_J_molK) / 1000.0;

(* Equilibrium Constant Kp(T) = exp(-Delta G / (R * T)) *)
IF (rVotedCavityTemp_degC + 273.15) > 1000.0 THEN
    rEquilibriumConstant_Kp := EXP(- (rThermodynamicAffinity_kJ_mol * 1000.0) / (rGasConstant_R * (rVotedCavityTemp_degC + 273.15)));
ELSE
    rEquilibriumConstant_Kp := 1.0E-12;
END_IF;

(* Oxygen non-stoichiometry parameter delta in ZnO_1-delta *)
(* Defect relation: delta is proportional to Kp^(1/3) *)
IF rEquilibriumConstant_Kp > 1.0E-09 THEN
    rDelta_NonStoichiometry := 0.0055 * (rEquilibriumConstant_Kp ** 0.3333);
ELSE
    rDelta_NonStoichiometry := 0.00001;
END_IF;
IF rDelta_NonStoichiometry > 0.085 THEN rDelta_NonStoichiometry := 0.085; END_IF;

(* Arrhenius Heterogeneous Dissociation Rate Constant k(T) = k0 * (1 + 25*delta) * exp(-Ea / (R*T)) *)
IF (rVotedCavityTemp_degC + 273.15) > 1200.0 THEN
    rDissociationReactionRate_mol_s := (rZnO_FeedRate_kg_h / 81.38 / 3.6) * 
                                       (rArrheniusPreExp_k0 * (1.0 + 25.0 * rDelta_NonStoichiometry) * EXP(- rActivationEnergy_Ea / (rGasConstant_R * (rVotedCavityTemp_degC + 273.15))));
    IF rDissociationReactionRate_mol_s > 85.0 THEN rDissociationReactionRate_mol_s := 85.0; END_IF;
ELSE
    rDissociationReactionRate_mol_s := 0.0;
END_IF;

(* Estimated Zinc Vapor Yield and Conversion Efficiency *)
rEstimatedZnVaporYield_mol_s := rDissociationReactionRate_mol_s;
IF rZnO_FeedRate_kg_h > 1.0 THEN
    rEstimatedDissociationRate_pct := (rEstimatedZnVaporYield_mol_s * 81.38 * 3.6 / rZnO_FeedRate_kg_h) * 100.0;
    IF rEstimatedDissociationRate_pct > 100.0 THEN rEstimatedDissociationRate_pct := 100.0; END_IF;
ELSE
    rEstimatedDissociationRate_pct := 0.0;
END_IF;

(* ========================================================================================= *)
(* SEGMENT 6: AERODYNAMIC QUENCH GAS CURTAIN DYNAMICS & RECOMBINATION SUPPRESSION            *)
(* ========================================================================================= *)
(* Momentum flux ratio J = (rho_quench * v_quench^2) / (rho_core * v_core^2) *)
(* With argon carrier gas density ~ 1.78 kg/m3 and core velocity ~ 12 m/s *)
rQuenchCurtainMomentumRatio_J := (1.78 * rQuenchGasCurtainVelocity_m_s * rQuenchGasCurtainVelocity_m_s) / (0.45 * 144.0);
IF rQuenchCurtainMomentumRatio_J < 0.1 THEN rQuenchCurtainMomentumRatio_J := 0.1; END_IF;

(* Shock-chilling cooling rate: dT/dt = v_gas * (Delta T / Delta x_nozzle) *)
(* Delta x_nozzle = 0.012 m (12 mm nozzle shear zone) *)
rQuenchCoolingRate_K_s := rQuenchGasCurtainVelocity_m_s * ((rVotedCavityTemp_degC - 350.0) / 0.012);

(* Clausius-Clapeyron Zinc Saturation Vapor Pressure: ln(P_sat / P_0) = -Delta H_vap / R * (1/T - 1/T_boil) *)
(* Delta H_vap = 115.3 kJ/mol, T_boil = 1180.0 K (907 deg C) *)
IF (aX_Est[4] + 273.15) > 400.0 THEN
    rZincSaturationPress_bar := 1.01325 * EXP(- (115300.0 / rGasConstant_R) * ((1.0 / (aX_Est[4] + 273.15)) - (1.0 / 1180.0)));
ELSE
    rZincSaturationPress_bar := 1.0E-07;
END_IF;

(* Supersaturation ratio S = P_Zn / P_sat *)
IF rZincSaturationPress_bar > 1.0E-06 THEN
    rZincSupersaturationRatio_S := (rEstimatedZnVaporYield_mol_s * 0.08314 * (aX_Est[4] + 273.15) / (rQuenchGasCurtainFlow_Nm3_h * 0.000277 + 0.001)) / rZincSaturationPress_bar;
ELSE
    rZincSupersaturationRatio_S := 1000.0;
END_IF;
IF rZincSupersaturationRatio_S < 1.0 THEN rZincSupersaturationRatio_S := 1.0; END_IF;

(* ========================================================================================= *)
(* SEGMENT 7: HIGH-TEMPERATURE QUARTZ WINDOW PROTECTIVE GAS SWEEPING DYNAMICS                *)
(* ========================================================================================= *)
(* Annular vortex swirl number Sw = G_phi / (R * G_x) *)
(* High swirl creates centrifugal force repelling micronized particles away from window *)
IF rWindowSweepGasFlow_Nm3_h > 50.0 THEN
    rWindowSweepBarrierEfficiency := 0.985 + 0.010 * (rWindowSweepGasFlow_Nm3_h / 500.0);
ELSE
    rWindowSweepBarrierEfficiency := 0.650;
END_IF;

(* Particle Stokes Number Stk = rho_p * d_p^2 * v_sweep / (18 * mu * D_hydraulic) *)
(* With ZnO particle density = 5610 kg/m3, d_p = 1.5 um, mu_argon = 5.5E-5 Pa.s, D = 0.8 m *)
rParticleStokesNumber_Stk := (5610.0 * 2.25E-12 * (rWindowSweepGasFlow_Nm3_h * 0.277 / 0.50)) / (18.0 * 5.5E-05 * 0.8);
IF rParticleStokesNumber_Stk > 0.05 THEN
    (* Stokes number exceeds aerodynamic deflection threshold -> Dust deposition imminent *)
    wSystemWarningWord := wSystemWarningWord OR 16#0004;
END_IF;
"""

print("Logic Core module ready.")
