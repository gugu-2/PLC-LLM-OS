# mine_vod_fan_builder/st_phase3_state_space.py

def get_phase3_state_space():
    return """(* ==================================================================================================== *)
(* PHASE 3: DISCRETE STATE-SPACE PROPAGATION & LUENBERGER OBSERVER INNOVATION                           *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 3.1: Assembly of Normalized Physical Input Vector u[k]                                     *)
(* ---------------------------------------------------------------------------------------------------- *)
IF bLeadFanSelect THEN
    arrU_vector[1] := rFan2_BladePitchCmd_deg;
    arrU_vector[2] := rFan2_VFD_SpeedCmd_RPM;
ELSE
    arrU_vector[1] := rFan1_BladePitchCmd_deg;
    arrU_vector[2] := rFan1_VFD_SpeedCmd_RPM;
END_IF;

(* Average Louver Position Across 24 Underground Branches *)
rTempSum := 0.0;
FOR iLoopIdx := 1 TO 24 DO
    rTempSum := rTempSum + arrLouverCmd_pct[iLoopIdx];
END_FOR;
arrU_vector[3] := rTempSum / 24.0;

(* Average Auxiliary Booster Fan Pressure Differential [kPa] *)
rTempSum := 0.0;
FOR iLoopIdx := 1 TO 24 DO
    rTempSum := rTempSum + (arrAuxBoosterFanCmd_pct[iLoopIdx] * 0.018); (* 100% = 1.8 kPa boost *)
END_FOR;
arrU_vector[4] := rTempSum / 24.0;

arrU_vector[5] := rIntakeCollarHeaterValveCmd_pct;
arrU_vector[6] := rPostBlastFumeInitialMass_kg * 0.125; (* Source rate equivalent *)

(* ---------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 3.2: Assembly of Measured Process Output Vector y_meas[k]                                  *)
(* ---------------------------------------------------------------------------------------------------- *)
arrY_meas[1] := rDP_Voted;
arrY_meas[2] := rAirVel_Voted;
arrY_meas[3] := rFanStallMargin_pct;
arrY_meas[4] := rBladeTipTurbulenceRMS_Pa;
arrY_meas[5] := rToxicGas_Voted;
arrY_meas[6] := rShaftBottomBaroPressure_kPa - rSurfaceBaroPressure_kPa;

(* ---------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 3.3: Output Estimation y_hat[k] = C * x_hat[k] + D * u[k]                                  *)
(* ---------------------------------------------------------------------------------------------------- *)
FOR iLoopIdx := 1 TO 6 DO
    rTempSum := 0.0;
    FOR jLoopIdx := 1 TO 6 DO
        rTempSum := rTempSum + (arrC[iLoopIdx, jLoopIdx] * arrX_hat[jLoopIdx]) + (arrD[iLoopIdx, jLoopIdx] * arrU_vector[jLoopIdx]);
    END_FOR;
    arrY_hat[iLoopIdx] := rTempSum;
    (* Innovation Residual Error *)
    arrY_err[iLoopIdx] := arrY_meas[iLoopIdx] - arrY_hat[iLoopIdx];
END_FOR;

(* ---------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 3.4: Dynamic State Observer Innovation Update x_pred[k+1] = A*x_hat + B*u + L*y_err         *)
(* ---------------------------------------------------------------------------------------------------- *)
FOR iLoopIdx := 1 TO 6 DO
    rTempSum := 0.0;
    (* Matrix A * x_hat Term *)
    FOR jLoopIdx := 1 TO 6 DO
        rTempSum := rTempSum + (arrA[iLoopIdx, jLoopIdx] * arrX_hat[jLoopIdx]);
    END_FOR;
    (* Matrix B * u Term *)
    FOR jLoopIdx := 1 TO 6 DO
        rTempSum := rTempSum + (arrB[iLoopIdx, jLoopIdx] * arrU_vector[jLoopIdx]);
    END_FOR;
    (* Luenberger Innovation Feedback Matrix L * y_err Term *)
    FOR jLoopIdx := 1 TO 6 DO
        rTempSum := rTempSum + (arrL[iLoopIdx, jLoopIdx] * arrY_err[jLoopIdx]);
    END_FOR;
    arrX_pred[iLoopIdx] := rTempSum;
END_FOR;

(* State Bounding & Numerical Safeguard Protection *)
IF arrX_pred[1] < 0.2 THEN arrX_pred[1] := 0.2; ELSIF arrX_pred[1] > 9.5 THEN arrX_pred[1] := 9.5; END_IF;
IF arrX_pred[2] < 20.0 THEN arrX_pred[2] := 20.0; ELSIF arrX_pred[2] > 650.0 THEN arrX_pred[2] := 650.0; END_IF;
IF arrX_pred[3] < -25.0 THEN arrX_pred[3] := -25.0; ELSIF arrX_pred[3] > 120.0 THEN arrX_pred[3] := 120.0; END_IF;
IF arrX_pred[4] < 5.0 THEN arrX_pred[4] := 5.0; ELSIF arrX_pred[4] > 450.0 THEN arrX_pred[4] := 450.0; END_IF;
IF arrX_pred[5] < 0.0 THEN arrX_pred[5] := 0.0; ELSIF arrX_pred[5] > 350.0 THEN arrX_pred[5] := 350.0; END_IF;
IF arrX_pred[6] < 10.0 THEN arrX_pred[6] := 10.0; ELSIF arrX_pred[6] > 55.0 THEN arrX_pred[6] := 55.0; END_IF;

(* Advance Estimated State Vector for Next Cycle *)
FOR iLoopIdx := 1 TO 6 DO
    arrX_hat[iLoopIdx] := arrX_pred[iLoopIdx];
END_FOR;
"""
