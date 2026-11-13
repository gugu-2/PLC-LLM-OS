# brewery_builder/part5_phase2_state_space.py

def get_part5():
    return """(* ============================================================================================== *)
(* PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & PROCESS OBSERVERS            *)
(* ============================================================================================== *)

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 2.1: SYNTHESIZE PROCESS MEASUREMENT VECTOR y_meas[k] FROM 2oo3 TMR SENSORS                *)
(* ---------------------------------------------------------------------------------------------- *)
vecY_meas[1] := fVotedGrainBedDP;     (* Observed Bed Differential Pressure [mbar] *)
vecY_meas[2] := fVotedWortTurbidity;  (* Observed Vorlauf Turbidity [EBC] *)
vecY_meas[3] := fVotedRunoffFlow;     (* Observed Lauter Runoff Flow [hL/h] *)
vecY_meas[4] := fVotedKettleTemp;     (* Observed Kettle Boiling Temp [deg C] *)

(* Evaporation Rate [ %/h ] Synthesis via Thermal Energy Balance *)
IF (fVotedKettleTemp >= 99.0) AND (fVotedCalandriaSteamP > 0.5) THEN
    (* Evaporation Rate = (Thermal Power Input - Wall Heat Losses) / (Wort Mass * Enthalpy of Vap) *)
    fTempScalar := (fCalandriaSurfaceArea * fCleanCalandriaHeatTransferU * fCalandriaFoulingFactor *
                   MAX(0.5, (120.0 + (fVotedCalandriaSteamP * 12.5)) - fVotedKettleTemp) / 1000.0) - 180.0; (* Net kW *)
    vecY_meas[5] := MAX(0.0, (fTempScalar * 3600.0 / (fBatchVolumeTarget * 104.8 * fWaterLatentHeatVap)) * 100.0);
ELSE
    vecY_meas[5] := 0.0;
END_IF;

(* Residual Volatile DMS Concentration [ppb] Synthesis via Kinetic Observer Tracking *)
vecY_meas[6] := vecX_hat[6]; (* Retain Kalman updated state as measurement baseline *)

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 2.2: COMPUTE ESTIMATED MEASUREMENTS y_est[k] = C * x_hat[k] + D * u[k]                    *)
(* ---------------------------------------------------------------------------------------------- *)
FOR idxRow := 1 TO 6 DO
    fTempSum := 0.0;
    FOR idxCol := 1 TO 6 DO
        fTempSum := fTempSum + (matC[idxRow, idxCol] * vecX_hat[idxCol]);
    END_FOR;
    FOR idxInput := 1 TO 5 DO
        fTempSum := fTempSum + (matD[idxRow, idxInput] * vecU_active[idxInput]);
    END_FOR;
    vecY_est[idxRow] := fTempSum;
    (* Innovation Residual: y_innov = y_meas - y_est *)
    vecY_innov[idxRow] := vecY_meas[idxRow] - vecY_est[idxRow];
END_FOR;

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 2.3: COMPUTE STATE PROPAGATION x_hat[k+1] = A * x_hat[k] + B * u[k] + L * y_innov[k]     *)
(* ---------------------------------------------------------------------------------------------- *)
FOR idxRow := 1 TO 6 DO
    fTempSum := 0.0;
    (* Plant Dynamics Contribution: A * x_hat *)
    FOR idxCol := 1 TO 6 DO
        fTempSum := fTempSum + (matA[idxRow, idxCol] * vecX_hat[idxCol]);
    END_FOR;
    (* Actuation Driving Force Contribution: B * u *)
    FOR idxInput := 1 TO 5 DO
        fTempSum := fTempSum + (matB[idxRow, idxInput] * vecU_active[idxInput]);
    END_FOR;
    (* Kalman Innovation Correction Contribution: L * y_innov *)
    FOR idxCol := 1 TO 6 DO
        fTempSum := fTempSum + (matL[idxRow, idxCol] * vecY_innov[idxCol]);
    END_FOR;
    vecX_hat_next[idxRow] := fTempSum;
END_FOR;

(* Apply Cyber-Physical Physical Feasibility Clamping on Estimated States *)
IF vecX_hat_next[1] < 0.0 THEN vecX_hat_next[1] := 0.0; END_IF;      (* Delta P cannot be negative *)
IF vecX_hat_next[2] < 0.0 THEN vecX_hat_next[2] := 0.0; END_IF;      (* Turbidity cannot be negative *)
IF vecX_hat_next[3] < 0.0 THEN vecX_hat_next[3] := 0.0; END_IF;      (* Runoff flow cannot be negative *)
IF vecX_hat_next[4] < 5.0 THEN vecX_hat_next[4] := 5.0; END_IF;      (* Temp lower bound *)
IF vecX_hat_next[4] > 115.0 THEN vecX_hat_next[4] := 115.0; END_IF;  (* Temp upper bound *)
IF vecX_hat_next[5] < 0.0 THEN vecX_hat_next[5] := 0.0; END_IF;      (* Evaporation rate cannot be negative *)
IF vecX_hat_next[5] > 20.0 THEN vecX_hat_next[5] := 20.0; END_IF;    (* Evaporation rate upper bound *)
IF vecX_hat_next[6] < 0.0 THEN vecX_hat_next[6] := 0.0; END_IF;      (* DMS concentration cannot be negative *)

(* Advance State Vector Registers *)
FOR idxRow := 1 TO 6 DO
    vecX_hat_prev[idxRow] := vecX_hat[idxRow];
    vecX_hat[idxRow] := vecX_hat_next[idxRow];
END_FOR;

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 2.4: FIRST-PRINCIPLES BREWHOUSE ADVANCED CYBER-PHYSICAL OBSERVERS                         *)
(* ---------------------------------------------------------------------------------------------- *)

(* 1. Darcy Law Grain Bed Dynamic Permeability Estimation *)
(* Darcy Formula: Q [m3/s] = (K [m2] * Area [m2] / (mu [Pa*s] * L [m])) * DeltaP [Pa] *)
(* Solving for K: K = (Q_m3_s * mu * L) / (Area * DeltaP_Pa) *)
IF (vecX_hat[1] > 2.0) AND (vecX_hat[3] > 15.0) THEN
    (* Convert Flow from hL/h to m3/s: 1 hL = 0.1 m3, 1 h = 3600 s => / 36000.0 *)
    fTempScalar := (vecX_hat[3] / 36000.0); (* Flow in m3/s *)
    (* Convert Delta P from mbar to Pa: 1 mbar = 100 Pa *)
    fPermeabilityDarcyRaw := (fTempScalar * fWortDynamicViscosity * fGrainBedNominalHeight) /
                             (fLauterTunArea * MAX(100.0, vecX_hat[1] * 100.0));
    (* 1st-Order Low-Pass Digital Filter on Permeability (Time Constant tau = 2.0 s) *)
    fPermeabilityFiltered := fPermeabilityFiltered + (0.050 * (fPermeabilityDarcyRaw - fPermeabilityFiltered));
ELSE
    (* Fallback nominal permeability for virgin settled malt bed *)
    fPermeabilityFiltered := 1.25E-10;
END_IF;
fEstimatedGrainBedPermeability := fPermeabilityFiltered;

(* 2. Grain Bed Hydraulic Choking & Differential Pressure Rate of Change Detector *)
fDiffPressureRateOfChange := (fVotedGrainBedDP - fPrevVotedDP) / MAX(0.010, fCycleDeltaTimeSec);
fPrevVotedDP := fVotedGrainBedDP;

(* Detect Rapid Bed Compression / Choking: High d(DP)/dt combined with Collapsing Permeability *)
IF (fDiffPressureRateOfChange > 2.80) AND (fVotedGrainBedDP > 32.0) THEN
    bBedChokeDetected := TRUE;
ELSIF fVotedGrainBedDP < 25.0 THEN
    bBedChokeDetected := FALSE;
END_IF;

(* 3. Calandria Shell-and-Tube Heat Exchanger Dynamic Fouling Observer *)
IF (fVotedCalandriaSteamP > 0.8) AND (fVotedKettleTemp > 80.0) THEN
    (* Saturated Steam Temperature T_sat = 100.0 + 13.5 * P_steam^0.82 *)
    fTempScalar := 100.0 + (13.5 * SQRT(MAX(0.0, fVotedCalandriaSteamP))); (* Approx T_sat [deg C] *)
    (* Heat Transfer Duty Q = M_wort * Cp * dT/dt + Evap_loss *)
    fCalandriaCleanDutyWatts := fCalandriaSurfaceArea * fCleanCalandriaHeatTransferU * MAX(1.0, fTempScalar - fVotedKettleTemp);
    (* Observed Heat Transfer Duty from Rate of Temperature Rise & Boiling *)
    fCalandriaActualDutyWatts := (fBatchVolumeTarget * 104.8 * fWortSpecificHeatCp * 1000.0 *
                                 MAX(0.0, (vecX_hat[4] - vecX_hat_prev[4]) / fCycleDeltaTimeSec)) +
                                 (vecX_hat[5] * fBatchVolumeTarget * 104.8 * fWaterLatentHeatVap * 1000.0 / 3600.0);
    IF fCalandriaCleanDutyWatts > 10000.0 THEN
        fCalandriaFoulingFactor := fCalandriaActualDutyWatts / fCalandriaCleanDutyWatts;
        (* Bounds Clamping on Fouling Ratio *)
        IF fCalandriaFoulingFactor > 1.20 THEN fCalandriaFoulingFactor := 1.20; END_IF;
        IF fCalandriaFoulingFactor < 0.35 THEN fCalandriaFoulingFactor := 0.35; END_IF;
    END_IF;
ELSE
    fCalandriaFoulingFactor := 1.0;
END_IF;

IF fCalandriaFoulingFactor < 0.65 THEN
    bCalandriaFoulingAlarm := TRUE;
ELSE
    bCalandriaFoulingAlarm := FALSE;
END_IF;

(* 4. S-Methylmethionine (SMM) Precursor Cleavage & Volatile DMS Desorption Kinetics *)
(* Arrhenius Equation for SMM Thermal Cleavage: k_smm = A * exp(-Ea / (R * T_K)) *)
IF vecX_hat[4] > 70.0 THEN
    fTempScalar := vecX_hat[4] + 273.15; (* Convert to Kelvin *)
    (* Taylor Series / Numerical Approximation for exp(-Ea / (R * T)) *)
    fTempScalar := -fArrheniusActivationEnergySMM / (fUniversalGasConstantR * fTempScalar);
    IF fTempScalar < -35.0 THEN fTempScalar := -35.0; END_IF;
    (* Numerical exponential expansion *)
    fSMM_CleavageRateCoeff := fArrheniusPreExponentialA * EXP(fTempScalar);
    IF fSMM_CleavageRateCoeff > 0.0050 THEN fSMM_CleavageRateCoeff := 0.0050; END_IF;
ELSE
    fSMM_CleavageRateCoeff := 0.0;
END_IF;

(* DMS Volatilization Stripping Rate Proportional to Continuous Boil Evaporation Rate *)
fDMS_StrippingRateCoeff := 0.00028 * vecX_hat[5];

(* SMM Pool Depletion: d[SMM]/dt = - k_smm * [SMM] *)
fSMM_Concentration := MAX(0.0, fSMM_Concentration - (fSMM_CleavageRateCoeff * fSMM_Concentration * fCycleDeltaTimeSec));

(* DMS Residual Concentration Update: d[DMS]/dt = k_smm * [SMM] - k_vol * [DMS] *)
vecX_hat[6] := MAX(0.0, vecX_hat[6] + ((fSMM_CleavageRateCoeff * fSMM_Concentration -
                                       fDMS_StrippingRateCoeff * vecX_hat[6]) * fCycleDeltaTimeSec));
fEstimatedResidualDMS := vecX_hat[6];
"""
