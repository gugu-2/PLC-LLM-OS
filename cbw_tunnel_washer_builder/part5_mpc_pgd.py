# cbw_tunnel_washer_builder/part5_mpc_pgd.py
# Receding-Horizon MPC Optimization with Projected Gradient Descent (PGD)

def get_part5_mpc_pgd():
    return """(* ==================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH PROJECTED GRADIENT DESCENT (PGD)                     *)
(* ==================================================================================================== *)

(* -------------------------------------------------------------------------------------------------- *)
(* DYNAMIC REFERENCE TRAJECTORY ADJUSTMENT ACCORDING TO PRODUCTION RECIPE & SOIL INFLUX                *)
(* -------------------------------------------------------------------------------------------------- *)
(* If soil load turbidity is high (> 120 NTU), temporarily elevate main wash temp reference to 88.0 C *)
IF rQT_01_PrewashTurbidity_NTU > 120.0 THEN
    vecX_ref[2] := 88.0;
    vecX_ref[5] := 1.50;    (* Boost alkali concentration target to 1.50 g/L *)
ELSIF rQT_01_PrewashTurbidity_NTU < 40.0 THEN
    vecX_ref[2] := 82.0;    (* Light soil linen: reduce main wash temp to save energy *)
    vecX_ref[5] := 1.05;
ELSE
    vecX_ref[2] := 85.0;    (* Standard heavy healthcare / hospital linen recipe *)
    vecX_ref[5] := 1.25;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* UNROLLED PGD ITERATIVE SOLVER (3 RECURRENT INNER PASSES PER PLC SCAN CYCLE)                        *)
(* -------------------------------------------------------------------------------------------------- *)
(* Initialize optimizer trial vectors with previous converged control solutions *)
FOR k := 1 TO 6 DO
    vecU_target[k] := vecU[k];
END_FOR;

FOR n := 1 TO 3 DO
    (* Gradient Evaluation for Input u[1]: Main Wash Direct Live Steam Valve *)
    (* State sensitivities: x2 (Main Wash Temp) and x1 (Pre-Wash Temp) *)
    vecGrad[1] := (2.0 * matB[2, 1] * matQ[2, 2] * (vecX[2] - vecX_ref[2])) +
                  (2.0 * matR[1, 1] * vecU_target[1]) +
                  (2.0 * matS[1, 1] * (vecU_target[1] - vecU_prev[1]));

    (* Gradient Evaluation for Input u[2]: Bleach Direct Live Steam Valve *)
    (* State sensitivities: x3 (Bleach Temp) *)
    vecGrad[2] := (2.0 * matB[3, 2] * matQ[3, 3] * (vecX[3] - vecX_ref[3])) +
                  (2.0 * matR[2, 2] * vecU_target[2]) +
                  (2.0 * matS[2, 2] * (vecU_target[2] - vecU_prev[2]));

    (* Gradient Evaluation for Input u[3]: Cold Freshwater Makeup Valve *)
    (* State sensitivities: x4 (Rinse Conductivity) and x6 (Heat Exchanger Outlet Temp) *)
    vecGrad[3] := (2.0 * matB[4, 3] * matQ[4, 4] * (vecX[4] - vecX_ref[4])) +
                  (2.0 * matB[6, 3] * matQ[6, 6] * (vecX[6] - vecX_ref[6])) +
                  (2.0 * matR[3, 3] * vecU_target[3]) +
                  (2.0 * matS[3, 3] * (vecU_target[3] - vecU_prev[3]));

    (* Gradient Evaluation for Input u[4]: Counter-Flow Reclaimed Water Recirculation Pump *)
    (* State sensitivities: x1 (Pre-Wash), x4 (Rinse Soil Dilution), x10 (Buffer Level) *)
    vecGrad[4] := (2.0 * matB[1, 4] * matQ[1, 1] * (vecX[1] - vecX_ref[1])) +
                  (2.0 * matB[4, 4] * matQ[4, 4] * (vecX[4] - vecX_ref[4])) +
                  (2.0 * matB[10, 4] * matQ[10, 10] * (vecX[10] - vecX_ref[10])) +
                  (2.0 * matR[4, 4] * vecU_target[4]) +
                  (2.0 * matS[4, 4] * (vecU_target[4] - vecU_prev[4]));

    (* Gradient Evaluation for Input u[5]: Dewatering Hydraulic Ram Extraction Pressure *)
    (* State sensitivities: x7 (Hydraulic Pressure) and x8 (Residual Moisture Reduction) *)
    vecGrad[5] := (2.0 * matB[7, 5] * matQ[7, 7] * (vecX[7] - vecX_ref[7])) +
                  (2.0 * matB[8, 5] * matQ[8, 8] * (vecX[8] - vecX_ref[8])) +
                  (2.0 * matR[5, 5] * vecU_target[5]) +
                  (2.0 * matS[5, 5] * (vecU_target[5] - vecU_prev[5]));

    (* Gradient Evaluation for Input u[6]: Chemical Dosing Manifold Rate *)
    (* State sensitivities: x5 (Alkali Titration) and x9 (Drum Friction Torque) *)
    vecGrad[6] := (2.0 * matB[5, 6] * matQ[5, 5] * (vecX[5] - vecX_ref[5])) +
                  (2.0 * matR[6, 6] * vecU_target[6]) +
                  (2.0 * matS[6, 6] * (vecU_target[6] - vecU_prev[6]));

    (* Projected Gradient Descent Descent Step & Actuator Slew Rate Projection *)
    FOR k := 1 TO 6 DO
        (* Unconstrained Gradient Update *)
        vecU_target[k] := vecU_target[k] - (rPgdStepSize * vecGrad[k]);

        (* Slew Rate Clamping against previous scan control action *)
        rDeltaU := vecU_target[k] - vecU_prev[k];
        IF rDeltaU > vecDeltaU_max[k] THEN
            vecU_target[k] := vecU_prev[k] + vecDeltaU_max[k];
        ELSIF rDeltaU < -vecDeltaU_max[k] THEN
            vecU_target[k] := vecU_prev[k] - vecDeltaU_max[k];
        END_IF;

        (* Box Saturation Projection onto Physical Actuator Hardware Boundaries *)
        vecU_target[k] := LIMIT(vecU_min[k], vecU_target[k], vecU_max[k]);
    END_FOR;
END_FOR;

(* Store Solution for Next Scan Delta Evaluation *)
FOR k := 1 TO 6 DO
    vecU_prev[k] := vecU[k];
END_FOR;
"""
