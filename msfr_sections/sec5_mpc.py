# Section 5: Multivariable State-Space Model & Real-Time MPC Engine
def get_sec5_mpc():
    return """(* ========================================================================================= *)
(* 7.0 6-STATE MULTIVARIABLE STATE-SPACE DISCRETE MODEL & REAL-TIME MPC OPTIMIZATION         *)
(* ========================================================================================= *)
(* Multivariable cyber-physical governor:                                                    *)
(*   x[k+1] = A * x[k] + B * u[k]                                                           *)
(*   y[k]   = C * x[k] + D * u[k]                                                           *)
(* Solves an embedded quadratic cost function via projected gradient descent with Hessian    *)
(* preconditioning and actuator saturation constraints:                                      *)
(*   min J = (x_pred - x_ref)^T * Q * (x_pred - x_ref)                                       *)
(*         + (u - u_ref)^T * R * (u - u_ref) + delta_u^T * S * delta_u                       *)

(* First-Scan State-Space Model Matrix Population (T_s = 0.200 s) *)
IF NOT bMatricesInitialized THEN
    (* Discrete Transition Matrix A (6x6) *)
    A_mat[1,1] := 0.9820; A_mat[1,2] := 0.0005; A_mat[1,3] := 0.0000; A_mat[1,4] := 0.0012; A_mat[1,5] := 0.0000;  A_mat[1,6] := 0.0045;
    A_mat[2,1] := 0.0125; A_mat[2,2] := 0.9950; A_mat[2,3] := 0.0000; A_mat[2,4] := 0.0000; A_mat[2,5] := 0.0000;  A_mat[2,6] := 0.0250;
    A_mat[3,1] := 0.0000; A_mat[3,2] := 0.0000; A_mat[3,3] := 0.9200; A_mat[3,4] := 0.0000; A_mat[3,5] := 0.0150;  A_mat[3,6] := 0.0000;
    A_mat[4,1] := 0.0020; A_mat[4,2] := 0.0000; A_mat[4,3] := 0.0000; A_mat[4,4] := 0.9980; A_mat[4,5] := 0.0000;  A_mat[4,6] := 0.0000;
    A_mat[5,1] := 0.0000; A_mat[5,2] := 0.0000; A_mat[5,3] := 0.0000; A_mat[5,4] := 0.0000; A_mat[5,5] := 0.8500;  A_mat[5,6] := 0.0000;
    A_mat[6,1] := 0.0850; A_mat[6,2] := 0.0150; A_mat[6,3] := 0.0000; A_mat[6,4] := 0.0000; A_mat[6,5] := 0.0000;  A_mat[6,6] := 0.9650;

    (* Input Coupling Matrix B (6x4) *)
    (* Inputs: u1=Be rod [mm], u2=H2 flow [sccm], u3=He stripping [sccm], u4=Cyclone throttle [%] *)
    B_mat[1,1] := -0.00420; B_mat[1,2] := -0.00085; B_mat[1,3] := 0.00005;  B_mat[1,4] := 0.00000;
    B_mat[2,1] := -0.00150; B_mat[2,2] := -0.00030; B_mat[2,3] := 0.00000;  B_mat[2,4] := 0.00000;
    B_mat[3,1] := 0.00000;  B_mat[3,2] := 0.00000;  B_mat[3,3] := -0.00065; B_mat[3,4] := -0.00015;
    B_mat[4,1] := 0.00080;  B_mat[4,2] := 0.00000;  B_mat[4,3] := 0.00000;  B_mat[4,4] := 0.00000;
    B_mat[5,1] := 0.00000;  B_mat[5,2] := 0.00002;  B_mat[5,3] := 0.00008;  B_mat[5,4] := -0.00250;
    B_mat[6,1] := -0.00350; B_mat[6,2] := -0.00075; B_mat[6,3] := 0.00000;  B_mat[6,4] := 0.00000;

    (* Output Observation Matrix C (4x6 Identity Selection) *)
    FOR iRow := 1 TO 4 DO
        FOR iCol := 1 TO 6 DO
            IF iRow = iCol THEN
                C_mat[iRow, iCol] := 1.0;
            ELSE
                C_mat[iRow, iCol] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    (* Direct Feedthrough Matrix D (4x4 Zero) *)
    FOR iRow := 1 TO 4 DO
        FOR iCol := 1 TO 4 DO
            D_mat[iRow, iCol] := 0.0;
        END_FOR;
    END_FOR;

    (* Diagonal State Penalty Weights Q (6 states) *)
    Q_diag[1] := 120.0;     (* Heavy penalty on Redox Ratio tracking error *)
    Q_diag[2] := 5.0;       (* Penalty on leached chromium accumulation *)
    Q_diag[3] := 45.0;      (* Strong penalty on residual Xe-135 noble gas inventory *)
    Q_diag[4] := 1.5;       (* Minor penalty on Beryllium rod consumption *)
    Q_diag[5] := 250.0;     (* Extreme penalty on core gas void fraction *)
    Q_diag[6] := 80.0;      (* High penalty on structural alloy corrosion current *)

    (* Diagonal Control Action Weights R (4 actuators) *)
    R_diag[1] := 0.025;     (* Beryllium rod movement cost *)
    R_diag[2] := 0.050;     (* Hydrogen sparger gas consumption cost *)
    R_diag[3] := 0.010;     (* Helium stripping flow cost *)
    R_diag[4] := 0.080;     (* Cyclone throttle movement cost *)

    (* Diagonal Slew Rate (Delta-U) Suppression Weights S (4 actuators) *)
    S_diag[1] := 0.850;     (* Suppress aggressive Be rod mechanical oscillations *)
    S_diag[2] := 0.450;     (* Smooth hydrogen flow controller transients *)
    S_diag[3] := 0.150;     (* Smooth helium bubble injection transitions *)
    S_diag[4] := 0.650;     (* Prevent violent cyclone throttle hunting *)

    (* Actuator Hard Saturation Limits *)
    u_min[1] := 0.0;    u_max[1] := BE_ROD_MAX_STROKE_MM;   (* Be rod: 0 to 250 mm *)
    u_min[2] := 0.0;    u_max[2] := 1200.0;                 (* H2 flow: 0 to 1200 sccm *)
    u_min[3] := 200.0;  u_max[3] := 5000.0;                 (* He stripping: 200 to 5000 sccm *)
    u_min[4] := 15.0;   u_max[4] := 95.0;                   (* Cyclone throttle: 15 to 95 % *)

    (* Maximum Permissible Slew Rate per Execution Scan (0.2 s) *)
    delta_u_max[1] := 2.50;     (* Max 12.5 mm/s Be rod drive speed *)
    delta_u_max[2] := 25.0;     (* Max 125 sccm/s H2 MFC ramping *)
    delta_u_max[3] := 100.0;    (* Max 500 sccm/s He MFC ramping *)
    delta_u_max[4] := 5.0;      (* Max 25 %/s cyclone valve stroking *)

    (* Diagonal Hessian Approximations: H_m approx 2 * (sum_n B[n,m]^2 * Q[n] + R[m] + S[m]) *)
    FOR iCol := 1 TO 4 DO
        rTempSum := 0.0;
        FOR iRow := 1 TO 6 DO
            rTempSum := rTempSum + (B_mat[iRow, iCol] * B_mat[iRow, iCol] * Q_diag[iRow]);
        END_FOR;
        rWorkVal1 := 2.0 * (rTempSum + R_diag[iCol] + S_diag[iCol]);
        IF rWorkVal1 > 0.001 THEN
            inv_Hessian_diag[iCol] := 1.0 / rWorkVal1;
        ELSE
            inv_Hessian_diag[iCol] := 1.0;
        END_IF;
    END_FOR;

    bMatricesInitialized := TRUE;
END_IF;

(* Assemble Real-Time Current State Vector x_state *)
x_state[1] := rRedoxError;
x_state[2] := rDissolvedChromium_ppm;
x_state[3] := rFiltOffGasXe_Bq_m3 * 1.0e-10; (* Scaled dimensionless activity *)
x_state[4] := rCumulativeBerylliumBurn_grams * 0.010;
x_state[5] := rCalculatedVoidFraction_pct;
x_state[6] := rI_corr_uA_cm2;

(* Assemble State Setpoint Reference Vector x_ref *)
x_ref[1] := 0.0;        (* Target redox ratio error is zero (ln(ratio) = ln(target)) *)
x_ref[2] := 10.0;       (* Baseline background chromium limit [ppm] *)
x_ref[3] := 0.0;        (* Target residual Xenon activity in salt is zero *)
x_ref[4] := 0.0;        (* Minimize cumulative beryllium consumption *)
x_ref[5] := 0.025;      (* Target optimal bubbly flow void fraction: 0.025% *)
x_ref[6] := 0.250;      (* Target ultra-low corrosion current: 0.25 uA/cm2 *)

(* Actuator Baseline Reference Vector u_ref *)
u_ref[1] := 15.0;       (* Baseline shallow Be rod immersion [mm] *)
u_ref[2] := 150.0;      (* Baseline H2 trimming flow [sccm] *)
u_ref[3] := 1500.0;     (* Nominal He bubble stripping flow [sccm] *)
u_ref[4] := 65.0;       (* Nominal cyclone throttle position [%] *)

(* Forward One-Step State Prediction: x_pred = A * x_state + B * u_ctrl *)
FOR iRow := 1 TO 6 DO
    rTempSum := 0.0;
    FOR iCol := 1 TO 6 DO
        rTempSum := rTempSum + (A_mat[iRow, iCol] * x_state[iCol]);
    END_FOR;
    FOR iCol := 1 TO 4 DO
        rTempSum := rTempSum + (B_mat[iRow, iCol] * u_ctrl[iCol]);
    END_FOR;
    x_pred[iRow] := rTempSum;
    x_error[iRow] := x_pred[iRow] - x_ref[iRow];
END_FOR;

(* Projected Gradient Descent Optimization: 3 Unrolled Iterations per Scan *)
FOR iGradIter := 1 TO 3 DO
    (* Compute Analytical Gradient: grad_J[m] = dJ/du[m] *)
    FOR iCol := 1 TO 4 DO
        rTempSum := 0.0;
        FOR iRow := 1 TO 6 DO
            rTempSum := rTempSum + (2.0 * B_mat[iRow, iCol] * Q_diag[iRow] * x_error[iRow]);
        END_FOR;
        rTempSum := rTempSum + (2.0 * R_diag[iCol] * (u_ctrl[iCol] - u_ref[iCol]));
        rTempSum := rTempSum + (2.0 * S_diag[iCol] * (u_ctrl[iCol] - u_prev[iCol]));
        grad_J[iCol] := rTempSum;
    END_FOR;

    (* Update Control Actions: du = - alpha * inv_H * grad_J *)
    FOR iCol := 1 TO 4 DO
        delta_u[iCol] := - rStepSize * inv_Hessian_diag[iCol] * grad_J[iCol];
        
        (* Apply Slew Rate Bounds *)
        IF delta_u[iCol] > delta_u_max[iCol] THEN
            delta_u[iCol] := delta_u_max[iCol];
        ELSIF delta_u[iCol] < -delta_u_max[iCol] THEN
            delta_u[iCol] := -delta_u_max[iCol];
        END_IF;
        
        (* Integrate Control Action *)
        u_ctrl[iCol] := u_ctrl[iCol] + delta_u[iCol];
        
        (* Enforce Hard Actuator Saturation Constraints *)
        IF u_ctrl[iCol] > u_max[iCol] THEN
            u_ctrl[iCol] := u_max[iCol];
        ELSIF u_ctrl[iCol] < u_min[iCol] THEN
            u_ctrl[iCol] := u_min[iCol];
        END_IF;
    END_FOR;
END_FOR;

(* Store previous control inputs for next scan derivative evaluation *)
FOR iCol := 1 TO 4 DO
    u_prev[iCol] := u_ctrl[iCol];
END_FOR;

(* Assign MPC Computed Targets to Actuator Outputs *)
rBeImmersionTarget_mm := u_ctrl[1];
rH2FlowTarget_sccm    := u_ctrl[2];
"""

if __name__ == "__main__":
    s = get_sec5_mpc()
    print("Section 5 Length:", len(s))
