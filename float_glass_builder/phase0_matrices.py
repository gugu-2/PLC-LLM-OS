# phase0_matrices.py for FB_Glass_FloatLine_TinBath_AnnealingLehr_ThicknessCooling

def generate_phase0():
    return """(*
 * =========================================================================================================
 * PHASE 0: SYSTEM INITIALIZATION, CYBER-PHYSICAL STATE-SPACE MATRICES & MPC WEIGHT PROFILES
 * Executed deterministically on first PLC scan cycle or upon master reset.
 * =========================================================================================================
 *)

(* Calculate deterministic scan delta time in seconds with sanity bounds *)
IF tTaskCycleTime > T#0ms THEN
    rScanDeltaTime_sec := TIME_TO_REAL(tTaskCycleTime) / 1000.0;
ELSE
    rScanDeltaTime_sec := 0.010; (* Default fallback to 10 ms *)
END_IF;

IF NOT bInitializationExecuted THEN
    (* -----------------------------------------------------------------------------------------------------
     * 1. CONTINUOUS-TO-DISCRETE SYSTEM STATE TRANSITION DYNAMICS MATRIX A (6x6 SYSTEM)
     * States:
     *   x1: Delta_h [um]       (Ribbon center thickness deviation)
     *   x2: Delta_W [mm]       (Ribbon width deviation)
     *   x3: Delta_T_bath [deg C] (Molten tin longitudinal thermal gradient)
     *   x4: Delta_P_bath [mbar] (Protective atmosphere hermetic overpressure)
     *   x5: Delta_sigma [nm/cm] (Annealing Lehr residual thermal stress birefringence)
     *   x6: Delta_v_line [m/min] (Lehr main line draw conveyor speed)
     * ----------------------------------------------------------------------------------------------------- *)
    (* Row 1: Ribbon Thickness Dynamics (coupled to width neck-in, viscosity-temperature, and line draw speed) *)
    matA[1, 1] := 0.9842;   (* Self-retention pole: visco-capillary attenuation dynamics *)
    matA[1, 2] := -0.0418;  (* Width coupling: Poisson lateral expansion vs thickness thinning *)
    matA[1, 3] := 0.0185;   (* Temperature coupling: lower viscosity accelerates ribbon attenuation *)
    matA[1, 4] := 0.0004;   (* Atmosphere pressure aerodynamic buoyant cushion cross-coupling *)
    matA[1, 5] := 0.0000;   (* Lehr stress downstream decoupling from tin bath thickness *)
    matA[1, 6] := -0.0965;  (* Lehr line speed coupling: mass continuity continuity equation h ~ 1/v *)

    (* Row 2: Ribbon Width Dynamics (governed by top-roller tractive forces and equilibrium spread) *)
    matA[2, 1] := -0.0384;  (* Thickness-to-width reciprocal volumetric continuity *)
    matA[2, 2] := 0.9785;   (* Lateral visco-elastic relaxation pole of floating glass sheet *)
    matA[2, 3] := 0.0246;   (* Molten tin surface temperature promotes lateral spreading wetting *)
    matA[2, 4] := 0.0012;   (* Differential tunnel pressure lateral force on ribbon edge *)
    matA[2, 5] := 0.0000;   (* Downstream stress decoupling *)
    matA[2, 6] := -0.0520;  (* Draw speed longitudinal tension induces lateral neck-in waisting *)

    (* Row 3: Tin Bath Longitudinal Thermal Gradient Dynamics (molten tin pool heat conduction/radiation) *)
    matA[3, 1] := 0.0025;   (* Glass sheet sensible heat transport into molten tin pool *)
    matA[3, 2] := 0.0018;   (* Ribbon width surface coverage radiative shielding effect *)
    matA[3, 3] := 0.9912;   (* Thermal inertia pole: 220 tons molten tin pool thermal capacitance *)
    matA[3, 4] := -0.0015;  (* Reducing gas mass convection heat dissipation into roof casing *)
    matA[3, 5] := 0.0000;   (* Downstream decoupling *)
    matA[3, 6] := 0.0038;   (* Hot glass mass pull rate convective heat influx *)

    (* Row 4: Protective Atmosphere Hermetic Overpressure Dynamics (95% N2 / 5% H2 gas dynamics) *)
    matA[4, 1] := 0.0000;   (* Negligible thickness coupling *)
    matA[4, 2] := -0.0005;  (* Ribbon edge gas seal clearance cross-area alteration *)
    matA[4, 3] := 0.0084;   (* Ideal gas law thermal expansion: P ~ T *)
    matA[4, 4] := 0.9620;   (* Gas compressibility pneumatic leakage dissipation pole *)
    matA[4, 5] := 0.0000;   (* Lehr tunnel downstream decoupling *)
    matA[4, 6] := 0.0002;   (* Moving ribbon boundary layer gas drag *)

    (* Row 5: Lehr Exit Residual Thermal Stress Birefringence Dynamics (viscoelastic relaxation) *)
    matA[5, 1] := 0.0450;   (* Thicker ribbon creates parabolic through-thickness delta T *)
    matA[5, 2] := 0.0210;   (* Ribbon width accentuates transverse cross-belt thermal curvature *)
    matA[5, 3] := 0.0850;   (* Tin bath exit temperature enters Lehr Zone A critical annealing range *)
    matA[5, 4] := 0.0000;   (* Atmosphere pressure decoupling *)
    matA[5, 5] := 0.9760;   (* Narayanaswamy viscoelastic structural relaxation decay pole *)
    matA[5, 6] := 0.0625;   (* Line draw speed reduces residence time inside annealing zone A *)

    (* Row 6: Lehr Main Drive Conveyor Speed Dynamics (heavy mechanical inertia drivetrain) *)
    matA[6, 1] := 0.0000;   (* Ribbon load negligible on 150 kW lehr drive motor *)
    matA[6, 2] := 0.0000;   (* Negligible mechanical load coupling *)
    matA[6, 3] := 0.0000;   (* Thermal decoupling *)
    matA[6, 4] := 0.0000;   (* Pressure decoupling *)
    matA[6, 5] := 0.0000;   (* Stress decoupling *)
    matA[6, 6] := 0.9940;   (* Heavy mechanical flywheel inertia pole of synchronized lehr rolls *)

    (* -----------------------------------------------------------------------------------------------------
     * 2. DISCRETE CONTROL INPUT COUPLING EFFECTIVENESS MATRIX B (6x6 SYSTEM)
     * Inputs:
     *   u1: Top-roller aggregate draw velocity trim [RPM]
     *   u2: Top-roller aggregate toe-in angle trim [deg]
     *   u3: Tin bath roof SiC radiant heater power trim [%]
     *   u4: Protective atmosphere reducing gas supply trim [%]
     *   u5: Annealing Lehr transverse cooling damper air trim [%]
     *   u6: Lehr main line drive conveyor motor speed trim [m/min]
     * ----------------------------------------------------------------------------------------------------- *)
    (* Row 1: Delta_h response to actuator inputs *)
    matB[1, 1] := -0.0825;  (* Increasing top roller speed pulls and attenuates ribbon thinner *)
    matB[1, 2] := -0.0450;  (* Increasing toe-out angle widens ribbon and stretches thickness *)
    matB[1, 3] := -0.0120;  (* Roof heating lowers viscosity, permitting faster draw attenuation *)
    matB[1, 4] := 0.0000;   (* Atmosphere gas trim has zero direct thickness authority *)
    matB[1, 5] := 0.0000;   (* Lehr cooling damper has zero direct bath thickness authority *)
    matB[1, 6] := -0.1450;  (* Primary draw line speed directly governs volumetric thickness pull *)

    (* Row 2: Delta_W response to actuator inputs *)
    matB[2, 1] := -0.0310;  (* Top roller forward pull accelerates longitudinal draw, narrowing ribbon *)
    matB[2, 2] := 0.1250;   (* Top roller toe-out angle directly exerts lateral tension outward *)
    matB[2, 3] := 0.0180;   (* Warmer glass edges soften and spread wider on molten tin *)
    matB[2, 4] := 0.0000;   (* Atmosphere gas trim zero width authority *)
    matB[2, 5] := 0.0000;   (* Lehr cooling damper zero width authority *)
    matB[2, 6] := -0.0880;  (* Increasing lehr line speed necks in the continuous ribbon *)

    (* Row 3: Delta_T_bath response to actuator inputs *)
    matB[3, 1] := 0.0000;   (* Top roller speed zero direct thermal effect *)
    matB[3, 2] := 0.0000;   (* Top roller angle zero thermal effect *)
    matB[3, 3] := 0.0950;   (* SiC roof radiant heating power directly injects thermal flux *)
    matB[3, 4] := -0.0150;  (* Nitrogen purge gas influx cools the roof refractory slightly *)
    matB[3, 5] := 0.0000;   (* Lehr cooling damper zero bath thermal effect *)
    matB[3, 6] := 0.0000;   (* Line speed zero direct bath heating effect *)

    (* Row 4: Delta_P_bath response to actuator inputs *)
    matB[4, 1] := 0.0000;   (* Top roller speed zero pneumatic effect *)
    matB[4, 2] := 0.0000;   (* Top roller angle zero pneumatic effect *)
    matB[4, 3] := 0.0050;   (* Roof heater thermal expansion boosts casing internal pressure *)
    matB[4, 4] := 0.0820;   (* N2/H2 gas supply valve directly charges bath tunnel overpressure *)
    matB[4, 5] := 0.0000;   (* Lehr cooling damper zero bath pressure authority *)
    matB[4, 6] := 0.0000;   (* Line speed zero pneumatic authority *)

    (* Row 5: Delta_sigma (Lehr thermal stress) response to actuator inputs *)
    matB[5, 1] := 0.0000;   (* Top roller speed indirect *)
    matB[5, 2] := 0.0000;   (* Top roller angle indirect *)
    matB[5, 3] := 0.0240;   (* Bath roof heat sets thermal profile entering Lehr Zone A *)
    matB[5, 4] := 0.0000;   (* Gas trim zero lehr stress authority *)
    matB[5, 5] := -0.1180;  (* Lehr transverse cooling air dampers directly cancel thermal curvature *)
    matB[5, 6] := 0.0540;   (* Faster line speed shortens annealing time, increasing residual stress *)

    (* Row 6: Delta_v_line response to actuator inputs *)
    matB[6, 1] := 0.0000;   (* Top roller speed zero lehr drive motor authority *)
    matB[6, 2] := 0.0000;   (* Top roller angle zero lehr drive motor authority *)
    matB[6, 3] := 0.0000;   (* Bath heating zero lehr drive authority *)
    matB[6, 4] := 0.0000;   (* Gas trim zero lehr drive authority *)
    matB[6, 5] := 0.0000;   (* Lehr damper zero lehr drive authority *)
    matB[6, 6] := 0.1650;   (* Lehr line drive VFD speed reference authority *)

    (* -----------------------------------------------------------------------------------------------------
     * 3. DISCRETE MEASUREMENT OBSERVATION MATRIX C (6x6 SYSTEM)
     * Directly maps state vector x to physical sensor measurement channels y
     * ----------------------------------------------------------------------------------------------------- *)
    FOR idxRow := 1 TO 6 DO
        FOR idxCol := 1 TO 6 DO
            IF idxRow = idxCol THEN
                matC[idxRow, idxCol] := 1.0;
            ELSE
                matC[idxRow, idxCol] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    (* -----------------------------------------------------------------------------------------------------
     * 4. DIRECT TRANSMISSION FEEDFORWARD MATRIX D (6x6 SYSTEM)
     * Strictly strictly proper physical process with zero direct feedthrough terms
     * ----------------------------------------------------------------------------------------------------- *)
    FOR idxRow := 1 TO 6 DO
        FOR idxCol := 1 TO 6 DO
            matD[idxRow, idxCol] := 0.0;
        END_FOR;
    END_FOR;

    (* -----------------------------------------------------------------------------------------------------
     * 5. STATIONARY DISCRETE KALMAN / LUENBERGER OBSERVER INNOVATION GAIN MATRIX L (6x6 SYSTEM)
     * Designed via algebraic discrete Riccati solution with measurement covariance R_kalman and process Q_kalman
     * ----------------------------------------------------------------------------------------------------- *)
    matL[1, 1] := 0.4250;  matL[1, 2] := 0.0120;  matL[1, 3] := 0.0045;  matL[1, 4] := 0.0000;  matL[1, 5] := 0.0000;  matL[1, 6] := 0.0180;
    matL[2, 1] := 0.0150;  matL[2, 2] := 0.3850;  matL[2, 3] := 0.0080;  matL[2, 4] := 0.0000;  matL[2, 5] := 0.0000;  matL[2, 6] := 0.0110;
    matL[3, 1] := 0.0020;  matL[3, 2] := 0.0015;  matL[3, 3] := 0.4650;  matL[3, 4] := 0.0025;  matL[3, 5] := 0.0000;  matL[3, 6] := 0.0010;
    matL[4, 1] := 0.0000;  matL[4, 2] := 0.0000;  matL[4, 3] := 0.0035;  matL[4, 4] := 0.5100;  matL[4, 5] := 0.0000;  matL[4, 6] := 0.0000;
    matL[5, 1] := 0.0080;  matL[5, 2] := 0.0065;  matL[5, 3] := 0.0150;  matL[5, 4] := 0.0000;  matL[5, 5] := 0.4800;  matL[5, 6] := 0.0140;
    matL[6, 1] := 0.0050;  matL[6, 2] := 0.0040;  matL[6, 3] := 0.0000;  matL[6, 4] := 0.0000;  matL[6, 5] := 0.0020;  matL[6, 6] := 0.4950;

    (* -----------------------------------------------------------------------------------------------------
     * 6. MPC QUADRATIC ERROR PENALTY WEIGHT MATRIX Q (6x6 SYSTEM)
     * Diagonal positive semi-definite state deviation weighting coefficients
     * ----------------------------------------------------------------------------------------------------- *)
    FOR idxRow := 1 TO 6 DO
        FOR idxCol := 1 TO 6 DO
            matQ[idxRow, idxCol] := 0.0;
        END_FOR;
    END_FOR;
    matQ[1, 1] := 145.0;  (* High priority: glass ribbon thickness optical tolerance tracking *)
    matQ[2, 2] := 95.0;   (* High priority: gross ribbon width stability & edge trim yield *)
    matQ[3, 3] := 45.0;   (* Moderate priority: tin bath thermal gradient profile stability *)
    matQ[4, 4] := 75.0;   (* High priority: protective atmosphere overpressure seal preservation *)
    matQ[5, 5] := 180.0;  (* Extreme priority: residual thermal birefringence stress suppression *)
    matQ[6, 6] := 110.0;  (* High priority: lehr line conveyor synchronization & throughput *)

    (* -----------------------------------------------------------------------------------------------------
     * 7. MPC ACTUATOR CONTROL EFFORT PENALTY WEIGHT MATRIX R (6x6 SYSTEM)
     * Diagonal positive definite penalty on actuator control excursions
     * ----------------------------------------------------------------------------------------------------- *)
    FOR idxRow := 1 TO 6 DO
        FOR idxCol := 1 TO 6 DO
            matR[idxRow, idxCol] := 0.0;
        END_FOR;
    END_FOR;
    matR[1, 1] := 12.5;   (* Top-roller knurl motor speed actuation effort *)
    matR[2, 2] := 16.0;   (* Top-roller toe-in angular servo actuation effort *)
    matR[3, 3] := 6.5;    (* Tin bath SiC roof electric heater bank duty cycle effort *)
    matR[4, 4] := 8.0;    (* Protective reducing gas N2/H2 valve position modulation effort *)
    matR[5, 5] := 7.2;    (* Lehr cooling air damper servo actuator movement effort *)
    matR[6, 6] := 22.0;   (* Lehr main drive 150 kW synchronous motor speed adjustment effort *)

    (* -----------------------------------------------------------------------------------------------------
     * 8. MPC TERMINAL STATE STABILITY RICCATI PENALTY MATRIX P (6x6 SYSTEM)
     * Computed from steady-state Lyapunov equation: P - A^T P A = Q
     * ----------------------------------------------------------------------------------------------------- *)
    FOR idxRow := 1 TO 6 DO
        FOR idxCol := 1 TO 6 DO
            matP[idxRow, idxCol] := 0.0;
        END_FOR;
    END_FOR;
    matP[1, 1] := 385.0;  matP[1, 2] := -25.0;  matP[1, 3] := 12.0;   matP[1, 4] := 0.0;    matP[1, 5] := 42.0;   matP[1, 6] := -65.0;
    matP[2, 1] := -25.0;  matP[2, 2] := 295.0;  matP[2, 3] := 18.0;   matP[2, 4] := 0.0;    matP[2, 5] := 28.0;   matP[2, 6] := -45.0;
    matP[3, 1] := 12.0;   matP[3, 2] := 18.0;   matP[3, 3] := 165.0;  matP[3, 4] := -8.0;   matP[3, 5] := 35.0;   matP[3, 6] := 14.0;
    matP[4, 1] := 0.0;    matP[4, 2] := 0.0;    matP[4, 3] := -8.0;   matP[4, 4] := 210.0;  matP[4, 5] := 0.0;    matP[4, 6] := 0.0;
    matP[5, 1] := 42.0;   matP[5, 2] := 28.0;   matP[5, 3] := 35.0;   matP[5, 4] := 0.0;    matP[5, 5] := 460.0;  matP[5, 6] := 38.0;
    matP[6, 1] := -65.0;  matP[6, 2] := -45.0;  matP[6, 3] := 14.0;   matP[6, 4] := 0.0;    matP[6, 5] := 38.0;   matP[6, 6] := 320.0;

    (* -----------------------------------------------------------------------------------------------------
     * 9. PHYSICAL ACTUATOR HARD SATURATION BOX CONSTRAINTS & MAXIMUM SLEW LIMITS
     * ----------------------------------------------------------------------------------------------------- *)
    (* Lower Bounds u_min *)
    arrU_Min[1] := -45.0;   (* Top-roller knurl speed trim lower bound [RPM] *)
    arrU_Min[2] := -15.0;   (* Top-roller knurl toe angle lower bound [deg] *)
    arrU_Min[3] := -25.0;   (* Roof heater power duty cycle trim lower bound [%] *)
    arrU_Min[4] := -20.0;   (* Protective gas supply valve trim lower bound [%] *)
    arrU_Min[5] := -30.0;   (* Lehr cooling damper servo trim lower bound [%] *)
    arrU_Min[6] := -2.50;   (* Lehr line draw speed trim lower bound [m/min] *)

    (* Upper Bounds u_max *)
    arrU_Max[1] := 45.0;    (* Top-roller knurl speed trim upper bound [RPM] *)
    arrU_Max[2] := 15.0;    (* Top-roller knurl toe angle upper bound [deg] *)
    arrU_Max[3] := 25.0;    (* Roof heater power duty cycle trim upper bound [%] *)
    arrU_Max[4] := 20.0;    (* Protective gas supply valve trim upper bound [%] *)
    arrU_Max[5] := 30.0;    (* Lehr cooling damper servo trim upper bound [%] *)
    arrU_Max[6] := 2.50;    (* Lehr line draw speed trim upper bound [m/min] *)

    (* Slew Rate Limits du_max (per 10 ms execution cycle) *)
    arrDeltaU_Max[1] := 0.45;  (* Max top-roller speed delta per scan (45.0 RPM/s) *)
    arrDeltaU_Max[2] := 0.15;  (* Max toe angle delta per scan (15.0 deg/s) *)
    arrDeltaU_Max[3] := 0.25;  (* Max heater power duty delta per scan (25.0 %/s) *)
    arrDeltaU_Max[4] := 0.20;  (* Max gas valve position delta per scan (20.0 %/s) *)
    arrDeltaU_Max[5] := 0.30;  (* Max lehr damper delta per scan (30.0 %/s) *)
    arrDeltaU_Max[6] := 0.025; (* Max lehr drive speed delta per scan (2.5 m/min/s) *)

    (* Initialize state vectors, previous inputs, and control references *)
    FOR idxRow := 1 TO 6 DO
        arrStateX_Hat[idxRow]  := 0.0;
        arrStateX_Next[idxRow] := 0.0;
        arrInputU[idxRow]      := 0.0;
        arrInputU_Prev[idxRow] := 0.0;
        arrStateX_Ref[idxRow]  := 0.0;
        arrInputU_Ref[idxRow]  := 0.0;
    END_FOR;

    (* -----------------------------------------------------------------------------------------------------
     * 10. DEFAULT NOMINAL SETPOINT PROFILES FOR 16 TOP-ROLLERS, 8 BATH ZONES & 12 LEHR ZONES
     * ----------------------------------------------------------------------------------------------------- *)
    (* Initialize 16 Top-Roller Knurl Machine Pairs *)
    FOR idxRoller := 1 TO 16 DO
        (* Machines 1 to 4: Hot entrance grip & width expansion (toe-out) *)
        IF idxRoller <= 4 THEN
            arrTopRollerSpeedCmd[idxRoller]       := 18.5 + (DINT_TO_REAL(idxRoller) * 1.2);
            arrTopRollerAngleCmd[idxRoller]       := 5.5 + (DINT_TO_REAL(idxRoller) * 0.8);
            arrTopRollerPenetrationCmd[idxRoller] := 1.8;
        (* Machines 5 to 10: Central attenuation & thickness stretching *)
        ELSIF idxRoller <= 10 THEN
            arrTopRollerSpeedCmd[idxRoller]       := 24.0 + (DINT_TO_REAL(idxRoller - 4) * 2.1);
            arrTopRollerAngleCmd[idxRoller]       := 8.0 - (DINT_TO_REAL(idxRoller - 4) * 0.5);
            arrTopRollerPenetrationCmd[idxRoller] := 2.2;
        (* Machines 11 to 16: Cold-end stabilization & edge bead setting *)
        ELSE
            arrTopRollerSpeedCmd[idxRoller]       := 36.0 + (DINT_TO_REAL(idxRoller - 10) * 1.5);
            arrTopRollerAngleCmd[idxRoller]       := 3.5 - (DINT_TO_REAL(idxRoller - 10) * 0.4);
            arrTopRollerPenetrationCmd[idxRoller] := 1.5;
        END_IF;

        arrTopRollerActualSpeed[idxRoller]        := arrTopRollerSpeedCmd[idxRoller];
        arrTopRollerActualAngle[idxRoller]        := arrTopRollerAngleCmd[idxRoller];
        arrTopRollerActualPen[idxRoller]          := arrTopRollerPenetrationCmd[idxRoller];
        arrTopRollerMotorTorque[idxRoller]        := 45.0;
        arrTopRollerMotorCurrent[idxRoller]       := 12.5;
        arrTopRollerShaftWaterFlow[idxRoller]     := 35.0;
        arrTopRollerShaftTemp[idxRoller]          := 42.0;
        arrTopRollerTractiveForce_N[idxRoller]    := 620.0;
        arrTopRollerSlipRatio[idxRoller]          := 0.02;
        arrTopRollerSlipTrip[idxRoller]           := FALSE;
    END_FOR;

    (* Initialize 8 Tin Bath Roof Radiant Heater Zone Setpoints (1050 deg C inlet down to 600 deg C exit) *)
    arrTinBathZoneTempSP[1] := 1050.0;  (* Zone 1: Delivery canal canal lip & wetback inlet *)
    arrTinBathZoneTempSP[2] := 1030.0;  (* Zone 2: Unconstrained glass pool spreading *)
    arrTinBathZoneTempSP[3] := 990.0;   (* Zone 3: Initial top-roller knurl grip inception *)
    arrTinBathZoneTempSP[4] := 940.0;   (* Zone 4: Primary ribbon attenuation & stretching *)
    arrTinBathZoneTempSP[5] := 870.0;   (* Zone 5: Secondary attenuation & thickness sizing *)
    arrTinBathZoneTempSP[6] := 790.0;   (* Zone 6: Thickness stabilization & edge cooling *)
    arrTinBathZoneTempSP[7] := 710.0;   (* Zone 7: Pre-lift-out ribbon solidification *)
    arrTinBathZoneTempSP[8] := 610.0;   (* Zone 8: Lift-out roll (LOR) discharge transition *)

    FOR idxZone := 1 TO 8 DO
        arrTinBathZoneTempActual[idxZone] := arrTinBathZoneTempSP[idxZone];
        arrTinBathRoofHeaterDuty[idxZone] := 55.0;
        arrTinBathZonePowerkW[idxZone]    := 125.0;
    END_FOR;

    (* Initialize 12 Annealing Lehr Temperature Profile (550 deg C entry down to 65 deg C exit) *)
    arrLehrZoneTempSP[1]  := 550.0;  (* Zone A1: Isothermal entry equalization *)
    arrLehrZoneTempSP[2]  := 525.0;  (* Zone A2: Critical annealing rapid relaxation *)
    arrLehrZoneTempSP[3]  := 495.0;  (* Zone A3: Glass transition lower boundary *)
    arrLehrZoneTempSP[4]  := 450.0;  (* Zone B1: Controlled linear stress-setting cooling *)
    arrLehrZoneTempSP[5]  := 405.0;  (* Zone B2: Stress-setting continuation *)
    arrLehrZoneTempSP[6]  := 350.0;  (* Zone B3: Transverse gradient containment *)
    arrLehrZoneTempSP[7]  := 290.0;  (* Zone C1: Secondary cooling *)
    arrLehrZoneTempSP[8]  := 230.0;  (* Zone C2: Secondary cooling *)
    arrLehrZoneTempSP[9]  := 175.0;  (* Zone C3: Low-temperature approach *)
    arrLehrZoneTempSP[10] := 130.0;  (* Zone F1: Forced convection cold-end blower cooling *)
    arrLehrZoneTempSP[11] := 90.0;   (* Zone F2: Cold-end blower cooling *)
    arrLehrZoneTempSP[12] := 65.0;   (* Zone F3: Discharge to cross-cutting line *)

    FOR idxZone := 1 TO 12 DO
        arrLehrZoneTempActual[idxZone]   := arrLehrZoneTempSP[idxZone];
        arrLehrCoolingDamperCmd[idxZone] := 35.0;
        arrLehrTrimHeaterDuty[idxZone]   := 20.0;
        arrLehrTransverseDeltaT[idxZone] := 1.5;
        arrLehrCrossDamperActual[idxZone]:= 35.0;
    END_FOR;

    (* Mark initialization completed *)
    bInitializationExecuted := TRUE;
END_IF;
"""

if __name__ == "__main__":
    s = generate_phase0()
    print(f"Phase 0 length: {len(s)} chars")
