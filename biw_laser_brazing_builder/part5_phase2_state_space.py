# biw_laser_brazing_builder/part5_phase2_state_space.py
"""
Part 5: Phase 2 - First-Principles Cyber-Physical State-Space Observer & Dynamic Decoupling
Function Block: FB_Automotive_BIW_LaserBrazing_StructuralAdhesive
"""

def get_phase2_state_space():
    return """(* ============================================================================================== *)
(* PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & DYNAMIC DECOUPLING            *)
(* State Equations:                                                                               *)
(*   y_est[k]   = C * x_hat[k] + D * u[k]                                                         *)
(*   innov[k]   = y_meas[k] - y_est[k]                                                            *)
(*   x_hat[k]   = x_hat[k] + L * innov[k]   (Kalman / Luenberger Innovation Correction)           *)
(*   x_pred[k+1]= A * x_hat[k] + B * u[k]   (One-Step Ahead A-Priori State Propagation)           *)
(* ============================================================================================== *)

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 2.1: ESTIMATE OUTPUT VECTOR y_est [1..6] VIA MATRICES C [6x8] AND D [6x6]                 *)
(* ---------------------------------------------------------------------------------------------- *)
(* y_est[1]: Melt Pool Temperature Estimate [deg C] *)
a_y_est[1] := (a_C[1, 1] * a_x[1]) + (a_C[1, 2] * a_x[2]) + (a_C[1, 3] * a_x[3]) + (a_C[1, 4] * a_x[4])
            + (a_C[1, 5] * a_x[5]) + (a_C[1, 6] * a_x[6]) + (a_C[1, 7] * a_x[7]) + (a_C[1, 8] * a_x[8])
            + (a_D[1, 1] * a_u[1]) + (a_D[1, 2] * a_u[2]) + (a_D[1, 3] * a_u[3]) + (a_D[1, 4] * a_u[4])
            + (a_D[1, 5] * a_u[5]) + (a_D[1, 6] * a_u[6]);

(* y_est[2]: CuSi3 Wire Feed Speed Estimate [mm/s] *)
a_y_est[2] := (a_C[2, 1] * a_x[1]) + (a_C[2, 2] * a_x[2]) + (a_C[2, 3] * a_x[3]) + (a_C[2, 4] * a_x[4])
            + (a_C[2, 5] * a_x[5]) + (a_C[2, 6] * a_x[6]) + (a_C[2, 7] * a_x[7]) + (a_C[2, 8] * a_x[8])
            + (a_D[2, 1] * a_u[1]) + (a_D[2, 2] * a_u[2]) + (a_D[2, 3] * a_u[3]) + (a_D[2, 4] * a_u[4])
            + (a_D[2, 5] * a_u[5]) + (a_D[2, 6] * a_u[6]);

(* y_est[3]: Lateral Seam Tracking Offset Estimate [um] *)
a_y_est[3] := (a_C[3, 1] * a_x[1]) + (a_C[3, 2] * a_x[2]) + (a_C[3, 3] * a_x[3]) + (a_C[3, 4] * a_x[4])
            + (a_C[3, 5] * a_x[5]) + (a_C[3, 6] * a_x[6]) + (a_C[3, 7] * a_x[7]) + (a_C[3, 8] * a_x[8])
            + (a_D[3, 1] * a_u[1]) + (a_D[3, 2] * a_u[2]) + (a_D[3, 3] * a_u[3]) + (a_D[3, 4] * a_u[4])
            + (a_D[3, 5] * a_u[5]) + (a_D[3, 6] * a_u[6]);

(* y_est[4]: Structural Adhesive Manifold Line Pressure Estimate [bar] *)
a_y_est[4] := (a_C[4, 1] * a_x[1]) + (a_C[4, 2] * a_x[2]) + (a_C[4, 3] * a_x[3]) + (a_C[4, 4] * a_x[4])
            + (a_C[4, 5] * a_x[5]) + (a_C[4, 6] * a_x[6]) + (a_C[4, 7] * a_x[7]) + (a_C[4, 8] * a_x[8])
            + (a_D[4, 1] * a_u[1]) + (a_D[4, 2] * a_u[2]) + (a_D[4, 3] * a_u[3]) + (a_D[4, 4] * a_u[4])
            + (a_D[4, 5] * a_u[5]) + (a_D[4, 6] * a_u[6]);

(* y_est[5]: Volumetric Flux Estimate [mL/s] *)
a_y_est[5] := (a_C[5, 1] * a_x[1]) + (a_C[5, 2] * a_x[2]) + (a_C[5, 3] * a_x[3]) + (a_C[5, 4] * a_x[4])
            + (a_C[5, 5] * a_x[5]) + (a_C[5, 6] * a_x[6]) + (a_C[5, 7] * a_x[7]) + (a_C[5, 8] * a_x[8])
            + (a_D[5, 1] * a_u[1]) + (a_D[5, 2] * a_u[2]) + (a_D[5, 3] * a_u[3]) + (a_D[5, 4] * a_u[4])
            + (a_D[5, 5] * a_u[5]) + (a_D[5, 6] * a_u[6]);

(* y_est[6]: Framing Geo-Clamp Reaction Force Estimate [N] *)
a_y_est[6] := (a_C[6, 1] * a_x[1]) + (a_C[6, 2] * a_x[2]) + (a_C[6, 3] * a_x[3]) + (a_C[6, 4] * a_x[4])
            + (a_C[6, 5] * a_x[5]) + (a_C[6, 6] * a_x[6]) + (a_C[6, 7] * a_x[7]) + (a_C[6, 8] * a_x[8])
            + (a_D[6, 1] * a_u[1]) + (a_D[6, 2] * a_u[2]) + (a_D[6, 3] * a_u[3]) + (a_D[6, 4] * a_u[4])
            + (a_D[6, 5] * a_u[5]) + (a_D[6, 6] * a_u[6]);


(* ---------------------------------------------------------------------------------------------- *)
(* STEP 2.2: CALCULATE LUENBERGER INNOVATION ERROR RESIDUALS a_innov [1..6]                        *)
(* ---------------------------------------------------------------------------------------------- *)
FOR j := 1 TO 6 DO
    a_innov[j] := a_y_meas[j] - a_y_est[j];
END_FOR;


(* ---------------------------------------------------------------------------------------------- *)
(* STEP 2.3: LUENBERGER / KALMAN STATE CORRECTION UPDATE (x_hat := x_hat + L * innov)             *)
(* ---------------------------------------------------------------------------------------------- *)
a_x[1] := a_x[1] + (a_L[1, 1] * a_innov[1]) + (a_L[1, 2] * a_innov[2]) + (a_L[1, 3] * a_innov[3])
                 + (a_L[1, 4] * a_innov[4]) + (a_L[1, 5] * a_innov[5]) + (a_L[1, 6] * a_innov[6]);

a_x[2] := a_x[2] + (a_L[2, 1] * a_innov[1]) + (a_L[2, 2] * a_innov[2]) + (a_L[2, 3] * a_innov[3])
                 + (a_L[2, 4] * a_innov[4]) + (a_L[2, 5] * a_innov[5]) + (a_L[2, 6] * a_innov[6]);

a_x[3] := a_x[3] + (a_L[3, 1] * a_innov[1]) + (a_L[3, 2] * a_innov[2]) + (a_L[3, 3] * a_innov[3])
                 + (a_L[3, 4] * a_innov[4]) + (a_L[3, 5] * a_innov[5]) + (a_L[3, 6] * a_innov[6]);

a_x[4] := a_x[4] + (a_L[4, 1] * a_innov[1]) + (a_L[4, 2] * a_innov[2]) + (a_L[4, 3] * a_innov[3])
                 + (a_L[4, 4] * a_innov[4]) + (a_L[4, 5] * a_innov[5]) + (a_L[4, 6] * a_innov[6]);

a_x[5] := a_x[5] + (a_L[5, 1] * a_innov[1]) + (a_L[5, 2] * a_innov[2]) + (a_L[5, 3] * a_innov[3])
                 + (a_L[5, 4] * a_innov[4]) + (a_L[5, 5] * a_innov[5]) + (a_L[5, 6] * a_innov[6]);

a_x[6] := a_x[6] + (a_L[6, 1] * a_innov[1]) + (a_L[6, 2] * a_innov[2]) + (a_L[6, 3] * a_innov[3])
                 + (a_L[6, 4] * a_innov[4]) + (a_L[6, 5] * a_innov[5]) + (a_L[6, 6] * a_innov[6]);

a_x[7] := a_x[7] + (a_L[7, 1] * a_innov[1]) + (a_L[7, 2] * a_innov[2]) + (a_L[7, 3] * a_innov[3])
                 + (a_L[7, 4] * a_innov[4]) + (a_L[7, 5] * a_innov[5]) + (a_L[7, 6] * a_innov[6]);

a_x[8] := a_x[8] + (a_L[8, 1] * a_innov[1]) + (a_L[8, 2] * a_innov[2]) + (a_L[8, 3] * a_innov[3])
                 + (a_L[8, 4] * a_innov[4]) + (a_L[8, 5] * a_innov[5]) + (a_L[8, 6] * a_innov[6]);


(* ---------------------------------------------------------------------------------------------- *)
(* STEP 2.4: DYNAMIC MULTI-PHYSICS DECOUPLING COMPUTATIONS                                        *)
(* ---------------------------------------------------------------------------------------------- *)
(* 2.4.1: Laser Brazing Thermal Enthalpy & Wire Feed Anti-Stubbing Decoupling                     *)
(* Mass flow rate of wire: m_dot = rho * A_wire * v_wire                                          *)
(* Required optical power: P_wire = m_dot * (c_p * (T_liq - 25) + Delta_H_f) / eta_opt            *)
rTheoreticalWireMeltPower := (rCuSi3_Density * 1.0E-6) * rCuSi3_WireArea * a_x[2] 
                           * (rCuSi3_SpecificHeat * (rCuSi3_LiquidusTemp - 25.0) + rCuSi3_LatentHeatFusion) 
                           / rLaserAbsorptivity;

(* Feedforward Decoupled Laser Power Command (Accounting for travel speed line energy) *)
IF rRobotContourSpeed > 5.0 THEN
    rDecoupledLaserPower := (rTheoreticalWireMeltPower + 1200.0) * (rRobotContourSpeed / rRobotSpeedNominal);
ELSE
    rDecoupledLaserPower := 800.0; (* Pre-heat standby power *)
END_IF;

(* Anti-Stubbing Wire Speed Clamping: Wire cannot outrun laser melt capacity *)
IF a_x[1] < rCuSi3_SolidusTemp THEN
    (* Cold substrate: Suppress wire feed to prevent mechanical stubbing *)
    rDecoupledWireSpeed := a_x[2] * 0.40;
ELSE
    rDecoupledWireSpeed := a_x_ref[2] * (rRobotContourSpeed / rRobotSpeedNominal);
END_IF;

(* 2.4.2: High-Viscosity Structural Epoxy Dispense Decoupling                                     *)
(* Target volumetric flux: V_dot [mL/s] = Target Bead Area [mm2] * Robot Path Velocity [mm/s] / 1000 *)
rAdh_VolumetricFluxTarget := (rAdh_TargetBeadArea * rRobotContourSpeed) / 1000.0;

(* Dispenser Servo Gear Pump Decoupled RPM: N_pump [rpm] = (V_dot [mL/s] * 60) / (Disp [mL/rev]) *)
IF rAdh_VolumetricFluxTarget > 0.05 THEN
    rDecoupledAdhPumpSpeed := (rAdh_VolumetricFluxTarget * 60.0) / (rAdh_PumpDisplacementPerRev * 1000.0);
    (* Dynamic Lead-Lag Hose Compliance Compensation: High pressure drop in long flexible lines requires *)
    (* an advance velocity boost during robot acceleration, and reverse decompression at deceleration *)
    IF a_du[6] > 0.10 THEN
        rDecoupledAdhPumpSpeed := rDecoupledAdhPumpSpeed * 1.15; (* 15% dynamic acceleration lead boost *)
    ELSIF a_du[6] < -0.10 THEN
        rDecoupledAdhPumpSpeed := rDecoupledAdhPumpSpeed * 0.82; (* 18% dynamic deceleration anti-balloon cut *)
    END_IF;
ELSE
    rDecoupledAdhPumpSpeed := 0.0;
END_IF;


(* ---------------------------------------------------------------------------------------------- *)
(* STEP 2.5: ONE-STEP AHEAD STATE PROPAGATION x_pred[k+1] = A * x[k] + B * u[k]                    *)
(* Completely unrolled 8x8 A matrix and 8x6 B matrix products                                     *)
(* ---------------------------------------------------------------------------------------------- *)
(* State 1: Melt Pool Temperature [deg C] *)
a_x_pred[1] := (a_A[1, 1] * a_x[1]) + (a_A[1, 2] * a_x[2]) + (a_A[1, 3] * a_x[3]) + (a_A[1, 4] * a_x[4])
             + (a_A[1, 5] * a_x[5]) + (a_A[1, 6] * a_x[6]) + (a_A[1, 7] * a_x[7]) + (a_A[1, 8] * a_x[8])
             + (a_B[1, 1] * a_u[1]) + (a_B[1, 2] * a_u[2]) + (a_B[1, 3] * a_u[3]) + (a_B[1, 4] * a_u[4])
             + (a_B[1, 5] * a_u[5]) + (a_B[1, 6] * a_u[6]);

(* State 2: CuSi3 Wire Feed Velocity [mm/s] *)
a_x_pred[2] := (a_A[2, 1] * a_x[1]) + (a_A[2, 2] * a_x[2]) + (a_A[2, 3] * a_x[3]) + (a_A[2, 4] * a_x[4])
             + (a_A[2, 5] * a_x[5]) + (a_A[2, 6] * a_x[6]) + (a_A[2, 7] * a_x[7]) + (a_A[2, 8] * a_x[8])
             + (a_B[2, 1] * a_u[1]) + (a_B[2, 2] * a_u[2]) + (a_B[2, 3] * a_u[3]) + (a_B[2, 4] * a_u[4])
             + (a_B[2, 5] * a_u[5]) + (a_B[2, 6] * a_u[6]);

(* State 3: Seam Lateral Deviation [um] *)
a_x_pred[3] := (a_A[3, 1] * a_x[1]) + (a_A[3, 2] * a_x[2]) + (a_A[3, 3] * a_x[3]) + (a_A[3, 4] * a_x[4])
             + (a_A[3, 5] * a_x[5]) + (a_A[3, 6] * a_x[6]) + (a_A[3, 7] * a_x[7]) + (a_A[3, 8] * a_x[8])
             + (a_B[3, 1] * a_u[1]) + (a_B[3, 2] * a_u[2]) + (a_B[3, 3] * a_u[3]) + (a_B[3, 4] * a_u[4])
             + (a_B[3, 5] * a_u[5]) + (a_B[3, 6] * a_u[6]);

(* State 4: Adhesive Dynamic Line Pressure [bar] *)
a_x_pred[4] := (a_A[4, 1] * a_x[1]) + (a_A[4, 2] * a_x[2]) + (a_A[4, 3] * a_x[3]) + (a_A[4, 4] * a_x[4])
             + (a_A[4, 5] * a_x[5]) + (a_A[4, 6] * a_x[6]) + (a_A[4, 7] * a_x[7]) + (a_A[4, 8] * a_x[8])
             + (a_B[4, 1] * a_u[1]) + (a_B[4, 2] * a_u[2]) + (a_B[4, 3] * a_u[3]) + (a_B[4, 4] * a_u[4])
             + (a_B[4, 5] * a_u[5]) + (a_B[4, 6] * a_u[6]);

(* State 5: Adhesive Volumetric Flux [mL/s] *)
a_x_pred[5] := (a_A[5, 1] * a_x[1]) + (a_A[5, 2] * a_x[2]) + (a_A[5, 3] * a_x[3]) + (a_A[5, 4] * a_x[4])
             + (a_A[5, 5] * a_x[5]) + (a_A[5, 6] * a_x[6]) + (a_A[5, 7] * a_x[7]) + (a_A[5, 8] * a_x[8])
             + (a_B[5, 1] * a_u[1]) + (a_B[5, 2] * a_u[2]) + (a_B[5, 3] * a_u[3]) + (a_B[5, 4] * a_u[4])
             + (a_B[5, 5] * a_u[5]) + (a_B[5, 6] * a_u[6]);

(* State 6: Dispensed Adhesive Bead Area [mm2] *)
a_x_pred[6] := (a_A[6, 1] * a_x[1]) + (a_A[6, 2] * a_x[2]) + (a_A[6, 3] * a_x[3]) + (a_A[6, 4] * a_x[4])
             + (a_A[6, 5] * a_x[5]) + (a_A[6, 6] * a_x[6]) + (a_A[6, 7] * a_x[7]) + (a_A[6, 8] * a_x[8])
             + (a_B[6, 1] * a_u[1]) + (a_B[6, 2] * a_u[2]) + (a_B[6, 3] * a_u[3]) + (a_B[6, 4] * a_u[4])
             + (a_B[6, 5] * a_u[5]) + (a_B[6, 6] * a_u[6]);

(* State 7: Roof Panel Thermal Buckling [um] *)
a_x_pred[7] := (a_A[7, 1] * a_x[1]) + (a_A[7, 2] * a_x[2]) + (a_A[7, 3] * a_x[3]) + (a_A[7, 4] * a_x[4])
             + (a_A[7, 5] * a_x[5]) + (a_A[7, 6] * a_x[6]) + (a_A[7, 7] * a_x[7]) + (a_A[7, 8] * a_x[8])
             + (a_B[7, 1] * a_u[1]) + (a_B[7, 2] * a_u[2]) + (a_B[7, 3] * a_u[3]) + (a_B[7, 4] * a_u[4])
             + (a_B[7, 5] * a_u[5]) + (a_B[7, 6] * a_u[6]);

(* State 8: Framing Clamp Differential Force [N] *)
a_x_pred[8] := (a_A[8, 1] * a_x[1]) + (a_A[8, 2] * a_x[2]) + (a_A[8, 3] * a_x[3]) + (a_A[8, 4] * a_x[4])
             + (a_A[8, 5] * a_x[5]) + (a_A[8, 6] * a_x[6]) + (a_A[8, 7] * a_x[7]) + (a_A[8, 8] * a_x[8])
             + (a_B[8, 1] * a_u[1]) + (a_B[8, 2] * a_u[2]) + (a_B[8, 3] * a_u[3]) + (a_B[8, 4] * a_u[4])
             + (a_B[8, 5] * a_u[5]) + (a_B[8, 6] * a_u[6]);
"""
