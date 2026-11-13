# hpdc_megacasting_builder/build_st_phase2_state_space.py

def get_phase2_state_space():
    return """(* =====================================================================================================================
 * PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & HYDRODYNAMICS
 * Ts = 1.0 ms deterministic execution of Kalman observer innovation, fluid kinematics, and structural platen tilt
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * 1. KINEMATIC VELOCITY & ACCELERATION DERIVATION WITH DIGITAL BUTTERWORTH FILTERING
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Optical scale backward difference raw velocity in m/s (dx in mm / dt in ms = m/s) *)
rRawVelocity := (rTMR_ENC301_Voted - rPlungerPos_Prev) / 1.0;

(* 2nd-Order Low-Pass Butterworth Filter (Cutoff fc = 120 Hz at 1 kHz sampling rate) *)
(* Difference equation: y[k] = b0*x[k] + b1*x[k-1] + b2*x[k-2] - a1*y[k-1] - a2*y[k-2] *)
rFiltVelocity := (0.09131 * rRawVelocity) + (0.18262 * rFiltVel_z1) + (0.09131 * rFiltVel_z2)
                 + (0.98238 * rFiltVel_z1) - (0.27400 * rFiltVel_z2);

(* Dynamic Slew Clamping to Prevent Mathematical Spikes During Transition *)
IF rFiltVelocity > 12.0 THEN
    rFiltVelocity := 12.0;
ELSIF rFiltVelocity < -2.0 THEN
    rFiltVelocity := -2.0;
END_IF;

(* Acceleration Derivative in m/s^2 *)
rRawAcceleration := (rFiltVelocity - rFiltVel_z1) * 1000.0;

(* Update Filter Historical Delay Registers *)
rFiltVel_z2 := rFiltVel_z1;
rFiltVel_z1 := rFiltVelocity;
rPlungerPos_Prev2 := rPlungerPos_Prev;
rPlungerPos_Prev := rTMR_ENC301_Voted;

(* Track Peak Fast-Shot Injection Velocity *)
IF (iFSM_CurrentState = 5) AND (rFiltVelocity > rPeakVelocityRecorded) THEN
    rPeakVelocityRecorded := rFiltVelocity;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2. HYDROSTATIC FORCE CONVERSIONS & SPECIFIC METAL CASTING PRESSURE
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Forward Head Thrust: F_head = P_head [bar] * 1e5 [N/m2] * Area [m2] / 1000 [N/kN] *)
rForce_Head_kN := (rTMR_PT101_Voted * 100.0) * rCylHead_Area_m2;

(* Opposing Rod Chamber Thrust *)
rForce_Rod_kN := (rTMR_PT201_Voted * 100.0) * rCylRod_Area_m2;

(* Net Mechanical Injection Thrust Force *)
rForce_Net_kN := rForce_Head_kN - rForce_Rod_kN;

(* Effective Hydrostatic Specific Metal Pressure on Molten Alloy in Shot Sleeve / Die Cavity *)
IF rPlunger_Area_m2 > 0.001 THEN
    rSpecificMetalPres_bar := (rForce_Net_kN / rPlunger_Area_m2) / 100.0;
ELSE
    rSpecificMetalPres_bar := 0.0;
END_IF;

(* Track Peak Intensification Pressure in Phase 3 / Phase 6 *)
IF (iFSM_CurrentState = 6) OR (iFSM_CurrentState = 7) THEN
    IF rSpecificMetalPres_bar > rPeakIntensPresRecorded THEN
        rPeakIntensPresRecorded := rSpecificMetalPres_bar;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 3. GATING FLUID MECHANICS & CONTINUITY EQUATIONS
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Ingate molten aluminum velocity: v_gate = (A_plunger / A_ingate) * v_plunger *)
IF rIngate_Area_m2 > 0.0001 THEN
    rIngate_Velocity_ms := (rPlunger_Area_m2 / rIngate_Area_m2) * rFiltVelocity;
ELSE
    rIngate_Velocity_ms := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 4. TIE-BAR STRUCTURAL STRAIN & DYNAMIC PLATEN TILT DEFLECTION
 * --------------------------------------------------------------------------------------------------------------------- *)
rTieBar_AvgStrain := (rTieBar_Strain_Col1_In + rTieBar_Strain_Col2_In + rTieBar_Strain_Col3_In + rTieBar_Strain_Col4_In) * 0.25;

rTieBar_MaxEccentricity := ABS(rTieBar_Strain_Col1_In - rTieBar_AvgStrain);
IF ABS(rTieBar_Strain_Col2_In - rTieBar_AvgStrain) > rTieBar_MaxEccentricity THEN
    rTieBar_MaxEccentricity := ABS(rTieBar_Strain_Col2_In - rTieBar_AvgStrain);
END_IF;
IF ABS(rTieBar_Strain_Col3_In - rTieBar_AvgStrain) > rTieBar_MaxEccentricity THEN
    rTieBar_MaxEccentricity := ABS(rTieBar_Strain_Col3_In - rTieBar_AvgStrain);
END_IF;
IF ABS(rTieBar_Strain_Col4_In - rTieBar_AvgStrain) > rTieBar_MaxEccentricity THEN
    rTieBar_MaxEccentricity := ABS(rTieBar_Strain_Col4_In - rTieBar_AvgStrain);
END_IF;

(* Set Platen Deflection Skew Interlock if Strain Eccentricity Exceeds 8.5% of Mean Strain *)
IF (rTieBar_AvgStrain > 200.0) AND (rTieBar_MaxEccentricity > (rTieBar_AvgStrain * 0.085)) THEN
    bTieBar_TonnageImbalance := TRUE;
    bAlarm_TieBar_Eccentricity := TRUE;
ELSE
    bTieBar_TonnageImbalance := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 5. ASSEMBLE SENSOR MEASUREMENT VECTOR y[k] (6 CHANNELS)
 * --------------------------------------------------------------------------------------------------------------------- *)
rVec_y_Measured[1] := rTMR_ENC301_Voted; (* Plunger Position [mm] *)
rVec_y_Measured[2] := rFiltVelocity;     (* Plunger Velocity [m/s] *)
rVec_y_Measured[3] := rTMR_PT101_Voted;  (* Head Pressure [bar] *)
rVec_y_Measured[4] := rTMR_PT201_Voted;  (* Rod Pressure [bar] *)
rVec_y_Measured[5] := rTMR_VPT401_Voted; (* Cavity Vacuum [mbar] *)
rVec_y_Measured[6] := (rDieTemp_Zone01_Fixed_In + rDieTemp_Zone02_Fixed_In + rDieTemp_Zone03_Fixed_In
                       + rDieTemp_Zone07_Moving_In + rDieTemp_Zone08_Moving_In) * 0.2; (* Die Surface Steel Temp [deg C] *)

(* ---------------------------------------------------------------------------------------------------------------------
 * 6. ESTIMATE OBSERVATION OUTPUT: y_hat = C * x_State + D * u_Control
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR iRow_Idx := 1 TO 6 DO
    rMatMul_Sum := 0.0;
    FOR iInner_Idx := 1 TO 8 DO
        rMatMul_Sum := rMatMul_Sum + (rMatrix_C[iRow_Idx, iInner_Idx] * rVec_x_State[iInner_Idx]);
    END_FOR;
    FOR iInner_Idx := 1 TO 6 DO
        rMatMul_Sum := rMatMul_Sum + (rMatrix_D[iRow_Idx, iInner_Idx] * rVec_u_Control[iInner_Idx]);
    END_FOR;
    rVec_y_Estimated[iRow_Idx] := rMatMul_Sum;
    rVec_y_Residual[iRow_Idx] := rVec_y_Measured[iRow_Idx] - rVec_y_Estimated[iRow_Idx];
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * 7. KALMAN FILTER INNOVATION UPDATE: x_hat = x_State + K * residual
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR iRow_Idx := 1 TO 8 DO
    rMatMul_Sum := 0.0;
    FOR iInner_Idx := 1 TO 6 DO
        rMatMul_Sum := rMatMul_Sum + (rMatrix_K_Kalman[iRow_Idx, iInner_Idx] * rVec_y_Residual[iInner_Idx]);
    END_FOR;
    rVec_x_Corrected[iRow_Idx] := rVec_x_State[iRow_Idx] + rMatMul_Sum;
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * 8. EXOGENOUS DISTURBANCE ESTIMATION
 * --------------------------------------------------------------------------------------------------------------------- *)
(* w1: Molten alloy viscosity / flow friction estimated from velocity and pressure residuals *)
rVec_w_Disturbance[1] := (0.015 * rVec_y_Residual[3]) - (0.085 * rVec_y_Residual[2]);
(* w2: Mold thermal fatigue / cavity boundary resistance *)
rVec_w_Disturbance[2] := 0.005 * rVec_y_Residual[5];
(* w3: Hydraulic supply pump pressure ripple *)
rVec_w_Disturbance[3] := 0.025 * rVec_y_Residual[4];

(* ---------------------------------------------------------------------------------------------------------------------
 * 9. DISCRETE STATE PROPAGATION: x[k+1] = A * x_hat + B * u + Ew * w
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR iRow_Idx := 1 TO 8 DO
    rMatMul_Sum := 0.0;
    (* State transition contribution *)
    FOR iInner_Idx := 1 TO 8 DO
        rMatMul_Sum := rMatMul_Sum + (rMatrix_A[iRow_Idx, iInner_Idx] * rVec_x_Corrected[iInner_Idx]);
    END_FOR;
    (* Actuator input contribution *)
    FOR iInner_Idx := 1 TO 6 DO
        rMatMul_Sum := rMatMul_Sum + (rMatrix_B[iRow_Idx, iInner_Idx] * rVec_u_Control[iInner_Idx]);
    END_FOR;
    (* Disturbance contribution *)
    FOR iInner_Idx := 1 TO 3 DO
        rMatMul_Sum := rMatMul_Sum + (rMatrix_Ew[iRow_Idx, iInner_Idx] * rVec_w_Disturbance[iInner_Idx]);
    END_FOR;
    rVec_x_Next[iRow_Idx] := rMatMul_Sum;
END_FOR;

(* Apply Physical Bound Constraints to State Variables to Guarantee Numerical Stability *)
IF rVec_x_Next[1] < 0.0 THEN rVec_x_Next[1] := 0.0; END_IF;
IF rVec_x_Next[1] > 1300.0 THEN rVec_x_Next[1] := 1300.0; END_IF;
IF rVec_x_Next[2] < -2.0 THEN rVec_x_Next[2] := -2.0; END_IF;
IF rVec_x_Next[2] > 12.0 THEN rVec_x_Next[2] := 12.0; END_IF;
IF rVec_x_Next[3] < 0.0 THEN rVec_x_Next[3] := 0.0; END_IF;
IF rVec_x_Next[3] > 400.0 THEN rVec_x_Next[3] := 400.0; END_IF;
IF rVec_x_Next[4] < 0.0 THEN rVec_x_Next[4] := 0.0; END_IF;
IF rVec_x_Next[4] > 350.0 THEN rVec_x_Next[4] := 350.0; END_IF;
IF rVec_x_Next[5] < 0.0 THEN rVec_x_Next[5] := 0.0; END_IF;
IF rVec_x_Next[5] > 950.0 THEN rVec_x_Next[5] := 950.0; END_IF;
IF rVec_x_Next[6] < 0.0 THEN rVec_x_Next[6] := 0.0; END_IF;
IF rVec_x_Next[6] > 1050.0 THEN rVec_x_Next[6] := 1050.0; END_IF;

(* Commit Propagated Prediction to Active State Vector *)
FOR iRow_Idx := 1 TO 8 DO
    rVec_x_State[iRow_Idx] := rVec_x_Next[iRow_Idx];
END_FOR;
"""
