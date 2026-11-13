# blown_film_builder/st_phase2_observers.py

def get_phase2_observers():
    return """(* ==================================================================================================== *)
(* PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & LUENBERGER OBSERVER                *)
(* High-Fidelity 6-State Estimation with 128-Zone Circumferential Statistical Quality Control (SQC)      *)
(* ==================================================================================================== *)

    (* -------------------------------------------------------------------------------------------- *)
    (* Step 2A: 128-Sector Rotating Thickness Profile Statistical Metrology & Noise Filtering       *)
    (* -------------------------------------------------------------------------------------------- *)
    rMeanSum := 0.0;
    rProfile_MaxPeak_um := -1.0E6;
    rProfile_MinTrough_um := 1.0E6;

    FOR zIdx := 0 TO 127 DO
        (* First-order discrete low-pass spatial recursive filter: alpha = 0.15 *)
        arrFilteredProfile_um[zIdx] := (0.850 * arrFilteredProfile_um[zIdx]) + (0.150 * arrThicknessProfile_Raw_um[zIdx]);
        rMeanSum := rMeanSum + arrFilteredProfile_um[zIdx];

        (* Track Extreme Circumferential Peaks and Troughs *)
        IF arrFilteredProfile_um[zIdx] > rProfile_MaxPeak_um THEN
            rProfile_MaxPeak_um := arrFilteredProfile_um[zIdx];
        END_IF;

        IF arrFilteredProfile_um[zIdx] < rProfile_MinTrough_um THEN
            rProfile_MinTrough_um := arrFilteredProfile_um[zIdx];
        END_IF;
    END_FOR;

    rProfile_AverageThickness_um := rMeanSum / 128.0;

    (* Compute Sample Variance & 2-Sigma Gauge Deviation Percentage *)
    rVarianceSum := 0.0;
    FOR zIdx := 0 TO 127 DO
        rTempDiff := arrFilteredProfile_um[zIdx] - rProfile_AverageThickness_um;
        rVarianceSum := rVarianceSum + (rTempDiff * rTempDiff);
    END_FOR;

    (* Safe Numerical Square Root (Newton-Raphson 3-Step Iteration for IEC Compatibility) *)
    rStdDev := rVarianceSum / 128.0;
    IF rStdDev > 0.0001 THEN
        (* Seed Initial Guess *)
        rTempStep := 0.5 * (rStdDev + 1.0);
        (* 3 Unrolled Newton-Raphson Iterations: x_{n+1} = 0.5 * (x_n + S / x_n) *)
        rTempStep := 0.5 * (rTempStep + (rStdDev / rTempStep));
        rTempStep := 0.5 * (rTempStep + (rStdDev / rTempStep));
        rTempStep := 0.5 * (rTempStep + (rStdDev / rTempStep));
        rStdDev := rTempStep;
    ELSE
        rStdDev := 0.0;
    END_IF;

    IF rProfile_AverageThickness_um > 1.0 THEN
        rProfile_2SigmaThickness_pct := (2.0 * rStdDev / rProfile_AverageThickness_um) * 100.0;
    ELSE
        rProfile_2SigmaThickness_pct := 0.0;
    END_IF;

    (* -------------------------------------------------------------------------------------------- *)
    (* Step 2B: Co-Extrusion 7-Layer Bulk Tooling Melt Temperature Synthesis                        *)
    (* -------------------------------------------------------------------------------------------- *)
    rBulkMeltTemp_Raw := (rExtruder_MeltTemp_A_degC +
                          rExtruder_MeltTemp_B_degC +
                          rExtruder_MeltTemp_C_degC +
                          rExtruder_MeltTemp_D_degC +
                          rExtruder_MeltTemp_E_degC +
                          rExtruder_MeltTemp_F_degC +
                          rExtruder_MeltTemp_G_degC) / 7.0;

    (* -------------------------------------------------------------------------------------------- *)
    (* Step 2C: Assemble Process Innovation Measurement Vector y_meas (6 States)                     *)
    (* -------------------------------------------------------------------------------------------- *)
    (* y[0]: 2-Sigma Gauge Deviation Error from Baseline Target (3.0% Industrial Benchmark) *)
    vecY_meas[0] := rProfile_2SigmaThickness_pct - 3.0;

    (* y[1]: Bubble Diameter Deviation from Kinematic Lay-Flat Nominal: D_nominal = 2 * W_layflat / PI *)
    vecY_meas[1] := rIBC_Diameter_Voted - (rRecipe_LayFlatWidth_mm * 0.63661977);

    (* y[2]: IBC Air Differential Pressure Deviation from Recipe Setpoint *)
    vecY_meas[2] := rIBC_DiffPressure_Sensor_Pa - rRecipe_IBC_DiffPress_Target_Pa;

    (* y[3]: Frost-Line Solidification Height Deviation from Recipe Target *)
    vecY_meas[3] := rFLH_Height_Voted - rRecipe_TargetFLH_mm;

    (* y[4]: Bulk Melt Temperature Deviation from Co-Extrusion Die Tooling Target *)
    vecY_meas[4] := rBulkMeltTemp_Raw - rRecipe_DieTemp_Target_degC;

    (* y[5]: Oscillating Haul-Off Web Tension Deviation from Recipe Target *)
    vecY_meas[5] := rWebTension_HaulOff_Voted - rRecipe_WebTension_N;

    (* -------------------------------------------------------------------------------------------- *)
    (* Step 2D: Compute Estimated Measurement Vector y_hat = C * x_hat + D * u                       *)
    (* -------------------------------------------------------------------------------------------- *)
    FOR iIdx := 0 TO 5 DO
        rTempSum := 0.0;
        FOR jIdx := 0 TO 5 DO
            rTempSum := rTempSum + (matC[iIdx, jIdx] * vecX_hat[jIdx]);
        END_FOR;
        FOR mIdx := 0 TO 5 DO
            rTempSum := rTempSum + (matD[iIdx, mIdx] * (vecU[mIdx] - vecU_target[mIdx]));
        END_FOR;
        vecY_hat[iIdx] := rTempSum;
    END_FOR;

    (* -------------------------------------------------------------------------------------------- *)
    (* Step 2E: State Observer Correction & Propagation: x_hat[k+1] = A*x_hat + B*u + L*(y - y_hat) *)
    (* -------------------------------------------------------------------------------------------- *)
    FOR iIdx := 0 TO 5 DO
        rTempSum := 0.0;
        (* State Transition Contribution: A * x_hat *)
        FOR jIdx := 0 TO 5 DO
            rTempSum := rTempSum + (matA[iIdx, jIdx] * vecX_hat[jIdx]);
        END_FOR;

        (* Control Actuator Contribution: B * (u - u_target) *)
        FOR mIdx := 0 TO 5 DO
            rTempSum := rTempSum + (matB[iIdx, mIdx] * (vecU[mIdx] - vecU_target[mIdx]));
        END_FOR;

        (* Innovation Feedback Correction: L * (y_meas - y_hat) *)
        FOR jIdx := 0 TO 5 DO
            rTempSum := rTempSum + (matL[iIdx, jIdx] * (vecY_meas[jIdx] - vecY_hat[jIdx]));
        END_FOR;

        vecX_hat[iIdx] := rTempSum;
    END_FOR;

    (* -------------------------------------------------------------------------------------------- *)
    (* Step 2F: Update Function Block Process Value Physical Output Estimates                      *)
    (* -------------------------------------------------------------------------------------------- *)
    rEstimated_ThicknessDev_um   := vecX_hat[0];
    rEstimated_BubbleDiameter_mm := (rRecipe_LayFlatWidth_mm * 0.63661977) + vecX_hat[1];
    rEstimated_IBC_DiffPress_Pa  := rRecipe_IBC_DiffPress_Target_Pa + vecX_hat[2];
    rEstimated_FLH_mm            := rRecipe_TargetFLH_mm + vecX_hat[3];
    rEstimated_MeltTemp_degC     := rRecipe_DieTemp_Target_degC + vecX_hat[4];
    rEstimated_WebTension_N      := rRecipe_WebTension_N + vecX_hat[5];
"""
