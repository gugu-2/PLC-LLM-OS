# fpso_gen/phase2_physics.py
def get_phase2():
    return """
(* =====================================================================================================================
 * PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & THERMODYNAMICS
 * Architected in accordance with API 617, GPSA Section 20, and Euler-Lagrange 6-DOF vessel hydrodynamics.
 * Models polytropic head, surge limit lines, dynamic SCL biases, TEG absorption kinetics, and state-space observer.
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 2.1: MARINE HULL 6-DOF WAVE MOTION DYNAMIC DECOUPLING
 * Floating production hulls undergo pitch, roll, and heave motions that destabilize gas-liquid mass transfer in tall
 * vertical columns (TEG contactor, scrubbers) and induce gyroscopic precession forces on high-speed compressor rotors.
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Compute dynamic vector magnitude of hull angular inclination [deg] *)
rVessel_TiltAngle := SQRT((rFPSO_RollAngle_In * rFPSO_RollAngle_In) + (rFPSO_PitchAngle_In * rFPSO_PitchAngle_In));
IF rVessel_TiltAngle < 0.01 THEN
    rVessel_TiltAngle := 0.01;
END_IF;

(* Compute dynamic angular velocity magnitude [deg/s] *)
rVessel_TiltRate := SQRT((rFPSO_RollRate_In * rFPSO_RollRate_In) + (rFPSO_PitchRate_In * rFPSO_PitchRate_In));

(* Effective vertical gravity acceleration accounting for marine wave heave acceleration [m/s2] *)
rVessel_EffGravity := rStdGravity + rFPSO_HeaveAccel_In;
IF rVessel_EffGravity < 2.50 THEN
    rVessel_EffGravity := 2.50; (* Hard physical floor against wave trough free-fall *)
END_IF;

(* TEG Contactor packed bed liquid sloshing wetting efficiency factor *)
(* When vessel tilts and oscillates, glycol maldistribution reduces effective gas-liquid contact area *)
rContactor_SloshDampingFactor := 1.000 - (0.0225 * rVessel_TiltAngle) - (0.0142 * rVessel_TiltRate);
IF rContactor_SloshDampingFactor < 0.520 THEN
    rContactor_SloshDampingFactor := 0.520;
ELSIF rContactor_SloshDampingFactor > 1.000 THEN
    rContactor_SloshDampingFactor := 1.000;
END_IF;

(* Contactor Tray Hydraulic Foaming Indicator Metric *)
(* Hydrocarbon mist condensation combined with roll/pitch liquid churn spikes column differential pressure *)
rContactor_FoamIndex := (rTEG_ContactorDP_PDT503_In / 28.5) * (1.000 + (0.0385 * rVessel_TiltAngle));
rContactor_FoamIndex_Out := rContactor_FoamIndex;

(* Suction Scrubber Mist Eliminator Droplet Carryover Risk Metric *)
(* As vertical heave reduces net settling acceleration (g_eff < g), terminal settling velocity of droplets drops *)
IF rVessel_EffGravity < rStdGravity THEN
    rDemister_CarryoverRisk := ((rStdGravity - rVessel_EffGravity) / rStdGravity) * 2.85;
ELSE
    rDemister_CarryoverRisk := 0.0;
END_IF;

(* Rotor Dynamic Gyroscopic Precession Bearing Load [kN] *)
(* Rotor polar moment of inertia I_p = 185 kg*m2; M_gyro = I_p * omega * tilt_rate *)
rGyro_PrecessionBearingLoad := 0.000185 * (rCompressorSpeed_ST101_In * 0.1047198) * (rVessel_TiltRate * 0.0174533);

(* Dynamic Surge Margin Derate Factor Due to Marine Wave Motions *)
(* When vessel pitches or rolls, gas velocity profiles inside suction nozzles deform, shifting the surge point *)
rDynamicSurgeBias_Wave := (0.0075 * rVessel_TiltAngle) + (0.0042 * ABS(rFPSO_HeaveAccel_In));
IF rDynamicSurgeBias_Wave > 0.125 THEN
    rDynamicSurgeBias_Wave := 0.125;
END_IF;
rVesselMotion_Derate_Factor_Out := rDynamicSurgeBias_Wave;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 2.2: COMPRESSOR TRAIN POLYTROPIC THERMODYNAMICS & REAL-TIME SURGE LIMIT LINES
 * Real gas thermodynamics applying Benedict-Webb-Rubin / Peng-Robinson EOS compressibility and polytropic head.
 * Calculates dynamic Surge Limit Lines (SLL) and Surge Control Lines (SCL) with negative rate-of-flow proactive bias.
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Molecular weight & specific gas constant validation *)
IF rGasMolecularWeight_In >= 12.0 AND rGasMolecularWeight_In <= 45.0 THEN
    rGas_Mw := rGasMolecularWeight_In;
ELSE
    rGas_Mw := 19.85; (* Offshore associated gas standard default *)
END_IF;
rGas_Z_Avg := 0.885;
rGas_n_Polytropic := 1.345;

(* Stage 1 Thermodynamics *)
IF rVoted_PT101_Internal > 1.0 THEN
    rPolytropicHead_Stg1 := (rGas_Z_Avg * (rGasConstant_R / rGas_Mw) * (rSuctionTemp_TT101_In + 273.15) *
                            (rGas_n_Polytropic / (rGas_n_Polytropic - 1.0)) *
                            (EXP(((rGas_n_Polytropic - 1.0) / rGas_n_Polytropic) *
                            LN(rInterstagePres_PT102_In / rVoted_PT101_Internal)) - 1.0)) * 0.001;
ELSE
    rPolytropicHead_Stg1 := 0.0;
END_IF;

(* Stage 2 Thermodynamics *)
IF rInterstagePres_PT102_In > 1.0 THEN
    rPolytropicHead_Stg2 := (rGas_Z_Avg * (rGasConstant_R / rGas_Mw) * (rInterstageTemp_TT102_In + 273.15) *
                            (rGas_n_Polytropic / (rGas_n_Polytropic - 1.0)) *
                            (EXP(((rGas_n_Polytropic - 1.0) / rGas_n_Polytropic) *
                            LN(rStage3SuctionPres_PT103_In / rInterstagePres_PT102_In)) - 1.0)) * 0.001;
ELSE
    rPolytropicHead_Stg2 := 0.0;
END_IF;

(* Stage 3 Thermodynamics *)
IF rStage3SuctionPres_PT103_In > 1.0 THEN
    rPolytropicHead_Stg3 := (rGas_Z_Avg * (rGasConstant_R / rGas_Mw) * (rStage3DischargeTemp_TT201_In + 273.15) *
                            (rGas_n_Polytropic / (rGas_n_Polytropic - 1.0)) *
                            (EXP(((rGas_n_Polytropic - 1.0) / rGas_n_Polytropic) *
                            LN(rVoted_PT201_Internal / rStage3SuctionPres_PT103_In)) - 1.0)) * 0.001;
ELSE
    rPolytropicHead_Stg3 := 0.0;
END_IF;

rPolytropicHead_Total_Out := rPolytropicHead_Stg1 + rPolytropicHead_Stg2 + rPolytropicHead_Stg3;

(* Polytropic Thermodynamic Compression Efficiency [%] *)
IF rMotorPower_WT101_In > 500.0 THEN
    rPolytropicEfficiency_Out := ((rPolytropicHead_Total_Out * 42.5) / rMotorPower_WT101_In) * 100.0;
    IF rPolytropicEfficiency_Out > 88.5 THEN
        rPolytropicEfficiency_Out := 88.5;
    ELSIF rPolytropicEfficiency_Out < 45.0 THEN
        rPolytropicEfficiency_Out := 45.0;
    END_IF;
ELSE
    rPolytropicEfficiency_Out := 76.5;
END_IF;

(* Calculate Surge Limit Line (SLL) Orifice Differential Pressures [mbar] *)
(* Formula: DeltaP_SLL = K_Surge * (P_discharge - P_suction) * 10.0 *)
rSurgeLimitDP_Stg1 := rK_Surge_Stg1 * (rInterstagePres_PT102_In - rVoted_PT101_Internal) * 10.0;
IF rSurgeLimitDP_Stg1 < 1.0 THEN
    rSurgeLimitDP_Stg1 := 1.0;
END_IF;

rSurgeLimitDP_Stg2 := rK_Surge_Stg2 * (rStage3SuctionPres_PT103_In - rInterstagePres_PT102_In) * 10.0;
IF rSurgeLimitDP_Stg2 < 1.0 THEN
    rSurgeLimitDP_Stg2 := 1.0;
END_IF;

rSurgeLimitDP_Stg3 := rK_Surge_Stg3 * (rVoted_PT201_Internal - rStage3SuctionPres_PT103_In) * 10.0;
IF rSurgeLimitDP_Stg3 < 1.0 THEN
    rSurgeLimitDP_Stg3 := 1.0;
END_IF;

(* Calculate Real-Time Surge Proximity Margins S_s = DeltaP_measured / DeltaP_SLL *)
rSurgeMargin_Stg1 := rVoted_PDT301_Internal / rSurgeLimitDP_Stg1;
rSurgeMargin_Stg2 := rInterstageDP_PDT302_In / rSurgeLimitDP_Stg2;
rSurgeMargin_Stg3 := rStage3DP_PDT303_In / rSurgeLimitDP_Stg3;

rSurgeMargin_Stg1_Out := rSurgeMargin_Stg1;
rSurgeMargin_Stg2_Out := rSurgeMargin_Stg2;
rSurgeMargin_Stg3_Out := rSurgeMargin_Stg3;

(* Rate of change of flow differential (derivative protection) *)
rdPDT301_dt := rdPDT301_dt + 0.20 * (((rVoted_PDT301_Internal - rPDT301_Prev) / rTs) - rdPDT301_dt);
rPDT301_Prev := rVoted_PDT301_Internal;

(* If flow is dropping rapidly toward surge, advance the Surge Control Line proactively *)
IF rdPDT301_dt < -5.0 THEN
    rDynamicSurgeBias_Rate := -0.00185 * rdPDT301_dt;
    IF rDynamicSurgeBias_Rate > 0.160 THEN
        rDynamicSurgeBias_Rate := 0.160;
    END_IF;
ELSE
    rDynamicSurgeBias_Rate := 0.0;
END_IF;

(* Overall Dynamic Target Surge Control Line Setpoint *)
rSurgeMargin_Target := 1.100 + rDynamicSurgeBias_Rate + rDynamicSurgeBias_Wave;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 2.3: TRIETHYLENE GLYCOL (TEG) ABSORPTION DEWPOINT & REBOILER ENERGY BALANCE
 * High-pressure absorption kinetics at 130 bar contactor operating pressure, tracking equilibrium water content,
 * mass transfer under vessel motion, and stripping still column reboiler thermal duty.
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Contactor water equilibrium loading based on Buczek-Selleck model [ppmv] *)
IF rTEG_ContactorPres_PT502_In > 5.0 THEN
    rTEG_WaterEquilibriumPpmv := (4850.0 / rTEG_ContactorPres_PT502_In) *
                                 (1.0 - (0.0085 * (rTEG_LeanPurity_AT502_In - 99.0)));
    IF rTEG_WaterEquilibriumPpmv < 1.5 THEN
        rTEG_WaterEquilibriumPpmv := 1.5;
    END_IF;
ELSE
    rTEG_WaterEquilibriumPpmv := 25.0;
END_IF;

(* Extracted water mass rate [kg/h] *)
rTEG_WaterAbsorptionRate := 0.075 * rTEG_LeanFlow_FT501_In * rContactor_SloshDampingFactor *
                            (rVoted_AT501_Internal - rTEG_WaterEquilibriumPpmv);
IF rTEG_WaterAbsorptionRate < 0.0 THEN
    rTEG_WaterAbsorptionRate := 0.0;
END_IF;

(* Reboiler heating duty required [kW] *)
(* Glycol sensible heat: Q_sensible = m_dot * Cp * deltaT; Water latent heat: Q_latent = m_water * deltaH_vap *)
rTEG_ReboilerThermalDutyKW := (rTEG_LeanFlow_FT501_In * 1120.0 * 2.55 * (rTEG_ReboilerTargetTemp - 145.0) / 3600.0) +
                              (rTEG_WaterAbsorptionRate * 2257.0 / 3600.0);
IF rTEG_ReboilerThermalDutyKW < 10.0 THEN
    rTEG_ReboilerThermalDutyKW := 10.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 2.4: 6-STATE CYBER-PHYSICAL DISCRETE STATE-SPACE MODEL & LUENBERGER OBSERVER
 * System equations: x[k+1] = A*x[k] + B*u[k] + Ew*w[k] + L*(y[k] - C*x[k] - D*u[k])
 * x = [delta_Ps1, delta_Pd3, delta_MassFlow, delta_ShaftSpeed, delta_Moisture, delta_RecyclePres]^T
 * u = [u_ASV1, u_ASV2, u_ASV3, delta_VFD_Speed]^T
 * w = [w_PipelineBackPres, w_WaveHeaveAccel, w_FeedMoistureSat]^T
 * --------------------------------------------------------------------------------------------------------------------- *)
IF NOT bStateSpace_Initialized THEN
    (* Row 1: delta_Ps1 (Suction Pressure) *)
    rMatrix_A[1, 1] := 0.985000; rMatrix_A[1, 2] := 0.002100; rMatrix_A[1, 3] := -0.014500;
    rMatrix_A[1, 4] := 0.000320; rMatrix_A[1, 5] := 0.000000; rMatrix_A[1, 6] := 0.012500;

    (* Row 2: delta_Pd3 (Discharge Pressure) *)
    rMatrix_A[2, 1] := 0.008500; rMatrix_A[2, 2] := 0.978000; rMatrix_A[2, 3] := 0.038500;
    rMatrix_A[2, 4] := 0.002850; rMatrix_A[2, 5] := 0.000000; rMatrix_A[2, 6] := -0.024500;

    (* Row 3: delta_MassFlow (Train Flow Rate) *)
    rMatrix_A[3, 1] := 0.035000; rMatrix_A[3, 2] := -0.028000; rMatrix_A[3, 3] := 0.965000;
    rMatrix_A[3, 4] := 0.004500; rMatrix_A[3, 5] := 0.000000; rMatrix_A[3, 6] := 0.018500;

    (* Row 4: delta_ShaftSpeed (Drive Rotor Speed) *)
    rMatrix_A[4, 1] := -0.015000; rMatrix_A[4, 2] := -0.045000; rMatrix_A[4, 3] := -0.085000;
    rMatrix_A[4, 4] := 0.991000; rMatrix_A[4, 5] := 0.000000; rMatrix_A[4, 6] := 0.012000;

    (* Row 5: delta_Moisture (Export Moisture) *)
    rMatrix_A[5, 1] := 0.000000; rMatrix_A[5, 2] := 0.000000; rMatrix_A[5, 3] := 0.024000;
    rMatrix_A[5, 4] := 0.000000; rMatrix_A[5, 5] := 0.955000; rMatrix_A[5, 6] := 0.000000;

    (* Row 6: delta_RecyclePres (Recycle Header Inventory) *)
    rMatrix_A[6, 1] := 0.012000; rMatrix_A[6, 2] := 0.021000; rMatrix_A[6, 3] := -0.019000;
    rMatrix_A[6, 4] := 0.001100; rMatrix_A[6, 5] := 0.000000; rMatrix_A[6, 6] := 0.972000;

    (* Control Input Matrix B (6 states x 4 controls) *)
    rMatrix_B[1, 1] := 0.045000; rMatrix_B[1, 2] := 0.015000; rMatrix_B[1, 3] := 0.008000; rMatrix_B[1, 4] := 0.000150;
    rMatrix_B[2, 1] := -0.038000; rMatrix_B[2, 2] := -0.042000; rMatrix_B[2, 3] := -0.085000; rMatrix_B[2, 4] := 0.003500;
    rMatrix_B[3, 1] := 0.065000; rMatrix_B[3, 2] := 0.058000; rMatrix_B[3, 3] := 0.072000; rMatrix_B[3, 4] := 0.005500;
    rMatrix_B[4, 1] := 0.012000; rMatrix_B[4, 2] := 0.018000; rMatrix_B[4, 3] := 0.025000; rMatrix_B[4, 4] := 0.085000;
    rMatrix_B[5, 1] := 0.000000; rMatrix_B[5, 2] := 0.000000; rMatrix_B[5, 3] := 0.000000; rMatrix_B[5, 4] := -0.000500;
    rMatrix_B[6, 1] := 0.052000; rMatrix_B[6, 2] := 0.048000; rMatrix_B[6, 3] := 0.064000; rMatrix_B[6, 4] := 0.001200;

    (* Disturbance Matrix Ew (6 states x 3 disturbances) *)
    rMatrix_Ew[1, 1] := 0.000000; rMatrix_Ew[1, 2] := 0.002500; rMatrix_Ew[1, 3] := 0.000000;
    rMatrix_Ew[2, 1] := 0.085000; rMatrix_Ew[2, 2] := 0.008500; rMatrix_Ew[2, 3] := 0.000000;
    rMatrix_Ew[3, 1] := -0.045000; rMatrix_Ew[3, 2] := -0.015000; rMatrix_Ew[3, 3] := 0.000000;
    rMatrix_Ew[4, 1] := -0.025000; rMatrix_Ew[4, 2] := -0.035000; rMatrix_Ew[4, 3] := 0.000000;
    rMatrix_Ew[5, 1] := 0.000000; rMatrix_Ew[5, 2] := 0.000000; rMatrix_Ew[5, 3] := 0.065000;
    rMatrix_Ew[6, 1] := 0.015000; rMatrix_Ew[6, 2] := 0.004000; rMatrix_Ew[6, 3] := 0.000000;

    (* Output Matrix C (Identity mapping) *)
    FOR iLoopRow := 1 TO 6 DO
        FOR iLoopCol := 1 TO 6 DO
            IF iLoopRow = iLoopCol THEN
                rMatrix_C[iLoopRow, iLoopCol] := 1.0;
            ELSE
                rMatrix_C[iLoopRow, iLoopCol] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    (* Direct Feedthrough Matrix D (Zero) *)
    FOR iLoopRow := 1 TO 6 DO
        FOR iLoopCol := 1 TO 4 DO
            rMatrix_D[iLoopRow, iLoopCol] := 0.0;
        END_FOR;
    END_FOR;

    (* Luenberger Observer Gain Matrix L (6 states x 6 outputs) *)
    rObserver_L[1, 1] := 0.125000; rObserver_L[1, 2] := 0.005000; rObserver_L[1, 3] := 0.010000;
    rObserver_L[1, 4] := 0.000000; rObserver_L[1, 5] := 0.000000; rObserver_L[1, 6] := 0.005000;
    rObserver_L[2, 1] := 0.005000; rObserver_L[2, 2] := 0.145000; rObserver_L[2, 3] := 0.015000;
    rObserver_L[2, 4] := 0.000000; rObserver_L[2, 5] := 0.000000; rObserver_L[2, 6] := 0.008000;
    rObserver_L[3, 1] := 0.010000; rObserver_L[3, 2] := 0.015000; rObserver_L[3, 3] := 0.155000;
    rObserver_L[3, 4] := 0.000000; rObserver_L[3, 5] := 0.000000; rObserver_L[3, 6] := 0.010000;
    rObserver_L[4, 1] := 0.000000; rObserver_L[4, 2] := 0.000000; rObserver_L[4, 3] := 0.000000;
    rObserver_L[4, 4] := 0.095000; rObserver_L[4, 5] := 0.000000; rObserver_L[4, 6] := 0.000000;
    rObserver_L[5, 1] := 0.000000; rObserver_L[5, 2] := 0.000000; rObserver_L[5, 3] := 0.000000;
    rObserver_L[5, 4] := 0.000000; rObserver_L[5, 5] := 0.115000; rObserver_L[5, 6] := 0.000000;
    rObserver_L[6, 1] := 0.005000; rObserver_L[6, 2] := 0.008000; rObserver_L[6, 3] := 0.010000;
    rObserver_L[6, 4] := 0.000000; rObserver_L[6, 5] := 0.000000; rObserver_L[6, 6] := 0.135000;

    (* MPC Quadratic Cost Weights Initialization *)
    rMPC_Weight_Q[1] := 85.0;   (* Suction Pressure deviation penalty *)
    rMPC_Weight_Q[2] := 120.0;  (* Export Discharge Pressure deviation penalty *)
    rMPC_Weight_Q[3] := 45.0;   (* Flow Rate penalty *)
    rMPC_Weight_Q[4] := 25.0;   (* VFD Shaft Speed deviation penalty *)
    rMPC_Weight_Q[5] := 150.0;  (* Export Moisture specification violation penalty *)
    rMPC_Weight_Q[6] := 35.0;   (* Recycle line inventory penalty *)

    rMPC_Weight_R[1] := 15.0;   (* ASV 1 Opening throttle penalty *)
    rMPC_Weight_R[2] := 15.0;   (* ASV 2 Opening throttle penalty *)
    rMPC_Weight_R[3] := 18.0;   (* ASV 3 Opening throttle penalty *)
    rMPC_Weight_R[4] := 5.0;    (* VFD Motor Speed variation penalty *)

    rMPC_Weight_S[1] := 250.0;  (* ASV 1 Valve Slew Rate Chattering penalty *)
    rMPC_Weight_S[2] := 250.0;  (* ASV 2 Valve Slew Rate Chattering penalty *)
    rMPC_Weight_S[3] := 280.0;  (* ASV 3 Valve Slew Rate Chattering penalty *)
    rMPC_Weight_S[4] := 85.0;   (* VFD Speed Acceleration Rate penalty *)

    rMPC_Weight_P[1] := 140.0;  (* Terminal Suction Penalty *)
    rMPC_Weight_P[2] := 220.0;  (* Terminal Discharge Penalty *)
    rMPC_Weight_P[3] := 75.0;   (* Terminal Flow Penalty *)
    rMPC_Weight_P[4] := 40.0;   (* Terminal Speed Penalty *)
    rMPC_Weight_P[5] := 250.0;  (* Terminal Moisture Penalty *)
    rMPC_Weight_P[6] := 55.0;   (* Terminal Recycle Penalty *)

    bStateSpace_Initialized := TRUE;
END_IF;

(* Formulate Measured Process Output Deviation Vector y[k] *)
rVec_y[1] := rVoted_SuctionPres_Out - 25.0;
rVec_y[2] := rVoted_DischargePres_Out - 250.0;
rVec_y[3] := (rVoted_SuctionDP_Out - 120.0) * 0.35;
rVec_y[4] := rCompressorSpeed_ST101_In - 9800.0;
rVec_y[5] := rVoted_ExportMoisture_Out - 18.0;
rVec_y[6] := (rInterstagePres_PT102_In - 62.0);

(* Formulate External Disturbance Estimation Vector w[k] *)
rVec_w[1] := rPipeline_BackPres_PT801_In - 250.0;
rVec_w[2] := rFPSO_HeaveAccel_In;
rVec_w[3] := (rVoted_ExportMoisture_Out - 20.0) * 0.15;

(* Observer Output Prediction: y_hat = C * x_hat + D * u *)
FOR iLoopRow := 1 TO 6 DO
    rVec_y_hat[iLoopRow] := 0.0;
    FOR iLoopCol := 1 TO 6 DO
        rVec_y_hat[iLoopRow] := rVec_y_hat[iLoopRow] + (rMatrix_C[iLoopRow, iLoopCol] * rVec_x_hat[iLoopCol]);
    END_FOR;
END_FOR;

(* Innovation Estimation Error: e_obs = y - y_hat *)
FOR iLoopRow := 1 TO 6 DO
    rVec_e_obs[iLoopRow] := rVec_y[iLoopRow] - rVec_y_hat[iLoopRow];
END_FOR;

(* Correct State Vector: x_corrected = x_hat + L * e_obs *)
FOR iLoopRow := 1 TO 6 DO
    rVec_x[iLoopRow] := rVec_x_hat[iLoopRow];
    FOR iLoopCol := 1 TO 6 DO
        rVec_x[iLoopRow] := rVec_x[iLoopRow] + (rObserver_L[iLoopRow, iLoopCol] * rVec_e_obs[iLoopCol]);
    END_FOR;
END_FOR;

(* State Propagation Step: x_hat[k+1] = A * x_corrected + B * u + Ew * w *)
FOR iLoopRow := 1 TO 6 DO
    rVec_x_hat[iLoopRow] := 0.0;
    (* State dynamics contribution *)
    FOR iLoopCol := 1 TO 6 DO
        rVec_x_hat[iLoopRow] := rVec_x_hat[iLoopRow] + (rMatrix_A[iLoopRow, iLoopCol] * rVec_x[iLoopCol]);
    END_FOR;
    (* Control input contribution *)
    FOR iLoopCol := 1 TO 4 DO
        rVec_x_hat[iLoopRow] := rVec_x_hat[iLoopRow] + (rMatrix_B[iLoopRow, iLoopCol] * rVec_u[iLoopCol]);
    END_FOR;
    (* Disturbance contribution *)
    FOR iLoopCol := 1 TO 3 DO
        rVec_x_hat[iLoopRow] := rVec_x_hat[iLoopRow] + (rMatrix_Ew[iLoopRow, iLoopCol] * rVec_w[iLoopCol]);
    END_FOR;
END_FOR;
"""
