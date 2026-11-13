# steel_dri_builder/part5_phase2_state_space.py
"""
Part 5: Phase 2 - First-Principles Cyber-Physical State-Space Estimation & Luenberger Observer
"""

def get_phase2_state_space():
    return """(* ==================================================================================================== *)
(* PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & LUENBERGER OBSERVER                *)
(* ==================================================================================================== *)

(* 2.1 Assemble Robustly Voted Process Measurement Vector y_Meas[1..6] *)
y_Meas[1] := rPV_BustleTemp_Voted;
y_Meas[2] := rPV_TopGasH2CO_Voted;
y_Meas[3] := rPV_ShaftDP_Voted;
y_Meas[4] := rPV_TopGasCO2_Voted;
y_Meas[5] := rPV_DRITemp_Voted;
y_Meas[6] := x_State[8]; (* Feeder linear mass extraction rate [t/h] *)

(* 2.2 Calculate Observer Measurement Predictions: y_Hat = C * x_Hat + D * u_Prev *)
FOR idx_i := 1 TO 6 DO
    rTempSum := 0.0;
    FOR idx_j := 1 TO 8 DO
        rTempSum := rTempSum + (matC[idx_i, idx_j] * x_Hat[idx_j]);
    END_FOR;
    FOR idx_k := 1 TO 6 DO
        rTempSum := rTempSum + (matD[idx_i, idx_k] * u_Prev[idx_k]);
    END_FOR;
    y_Hat[idx_i] := rTempSum;
END_FOR;

(* 2.3 Calculate Innovation Residual Vector: y_Innov = y_Meas - y_Hat *)
FOR idx_i := 1 TO 6 DO
    y_Innov[idx_i] := y_Meas[idx_i] - y_Hat[idx_i];
END_FOR;

(* 2.4 Luenberger Observer State Correction: x_Corr = x_Pred + L * y_Innov *)
FOR idx_i := 1 TO 8 DO
    rTempSum := 0.0;
    FOR idx_j := 1 TO 6 DO
        rTempSum := rTempSum + (matL[idx_i, idx_j] * y_Innov[idx_j]);
    END_FOR;
    x_Corr[idx_i] := x_Pred[idx_i] + rTempSum;
END_FOR;

(* 2.5 Cyber-Physical Non-Linear Gas-Solid Kinetics & Carburization Augmentation *)
(* Arrhenius reduction rate constant for H2 and CO: k = k0 * exp(-Ea / (R*T)) *)
(* Iron reduction velocity: Fe2O3 -> Fe3O4 -> FeO -> Fe *)
(* Net reaction velocity v_red [mol/(m3*s)] *)
rPV_Estimated_ReductionReactionRate := 0.000215 * EXP((x_Corr[1] - 850.0) / 125.0) * (x_Corr[4] / 2.50) * (1.0 - (x_Corr[2] / 100.0));
IF rPV_Estimated_ReductionReactionRate < 0.005 THEN
    rPV_Estimated_ReductionReactionRate := 0.005;
ELSIF rPV_Estimated_ReductionReactionRate > 0.450 THEN
    rPV_Estimated_ReductionReactionRate := 0.450;
END_IF;

(* Endothermic Hydrogen Enthalpy Cooling vs Exothermic Syngas Heat of Reduction *)
(* Delta H: H2 reduction absorbs +25 kJ/mol; CO reduction releases -17 kJ/mol *)
(* Internal Reduction Bed Core Temperature Estimation *)
rPV_Estimated_InternalThermalBed := x_Corr[1] - (x_Corr[4] * 18.5) + ((100.0 - x_Corr[2]) * 0.45) - 35.0;
IF rPV_Estimated_InternalThermalBed < 650.0 THEN
    rPV_Estimated_InternalThermalBed := 650.0;
ELSIF rPV_Estimated_InternalThermalBed > 1100.0 THEN
    rPV_Estimated_InternalThermalBed := 1100.0;
END_IF;

(* Burden Sintering & Sticking Propensity (Clusters form if Temp > 920 C and Metallization > 92%) *)
IF (x_Corr[1] > 940.0) AND (x_Corr[2] > 93.5) AND (x_Corr[3] > 68.0) THEN
    bClusterStickingWarning := TRUE;
ELSE
    IF x_Corr[3] < 62.0 THEN
        bClusterStickingWarning := FALSE;
    END_IF;
END_IF;

(* Apply Physical State Bounds to Filtered Observer Vector x_Hat *)
x_Hat[1] := x_Corr[1]; (* Bustle Gas Temp [deg C] *)
IF x_Hat[1] < 200.0 THEN x_Hat[1] := 200.0; ELSIF x_Hat[1] > 1200.0 THEN x_Hat[1] := 1200.0; END_IF;

x_Hat[2] := x_Corr[2] + (rPV_Estimated_ReductionReactionRate * 12.5 * rTs_Seconds); (* Metallization [% Fe] *)
IF x_Hat[2] < 10.0 THEN x_Hat[2] := 10.0; ELSIF x_Hat[2] > 99.8 THEN x_Hat[2] := 99.8; END_IF;

x_Hat[3] := x_Corr[3]; (* Shaft DP [kPa] *)
IF x_Hat[3] < 5.0 THEN x_Hat[3] := 5.0; ELSIF x_Hat[3] > 115.0 THEN x_Hat[3] := 115.0; END_IF;

x_Hat[4] := x_Corr[4]; (* Top Gas H2/CO Ratio [ratio] *)
IF x_Hat[4] < 0.5 THEN x_Hat[4] := 0.5; ELSIF x_Hat[4] > 8.0 THEN x_Hat[4] := 8.0; END_IF;

x_Hat[5] := x_Corr[5]; (* Top Gas CO2 [% vol] *)
IF x_Hat[5] < 1.0 THEN x_Hat[5] := 1.0; ELSIF x_Hat[5] > 32.0 THEN x_Hat[5] := 32.0; END_IF;

x_Hat[6] := x_Corr[6]; (* Discharged DRI Carbon [wt% C] *)
IF x_Hat[6] < 0.1 THEN x_Hat[6] := 0.1; ELSIF x_Hat[6] > 5.0 THEN x_Hat[6] := 5.0; END_IF;

x_Hat[7] := x_Corr[7]; (* Cooling Gas Discharge Temp [deg C] *)
IF x_Hat[7] < 25.0 THEN x_Hat[7] := 25.0; ELSIF x_Hat[7] > 850.0 THEN x_Hat[7] := 850.0; END_IF;

x_Hat[8] := x_Corr[8]; (* Feeder Extraction Rate [t/h] *)
IF x_Hat[8] < 0.0 THEN x_Hat[8] := 0.0; ELSIF x_Hat[8] > 280.0 THEN x_Hat[8] := 280.0; END_IF;

(* 2.6 Dynamic State-Space Time Propagation: x_Pred[k+1] = A * x_Hat[k] + B * u_Act[k] *)
FOR idx_i := 1 TO 8 DO
    rTempSum := 0.0;
    FOR idx_j := 1 TO 8 DO
        rTempSum := rTempSum + (matA[idx_i, idx_j] * x_Hat[idx_j]);
    END_FOR;
    FOR idx_k := 1 TO 6 DO
        rTempSum := rTempSum + (matB[idx_i, idx_k] * u_Act[idx_k]);
    END_FOR;
    x_Pred[idx_i] := rTempSum;
END_FOR;

(* 2.7 Emulated Cyber-Physical Reactor Evolution: x_State[k+1] = A * x_State[k] + B * u_Act[k] *)
FOR idx_i := 1 TO 8 DO
    rTempSum := 0.0;
    FOR idx_j := 1 TO 8 DO
        rTempSum := rTempSum + (matA[idx_i, idx_j] * x_State[idx_j]);
    END_FOR;
    FOR idx_k := 1 TO 6 DO
        rTempSum := rTempSum + (matB[idx_i, idx_k] * u_Act[idx_k]);
    END_FOR;
    x_State[idx_i] := rTempSum;
END_FOR;

(* 2.8 Export State Estimations to Output Interfaces *)
rPV_Estimated_Metallization := x_Hat[2];
rPV_Estimated_Carbon := x_Hat[6];
rPV_Estimated_DescendVelocity := (x_Hat[8] / 150.0) * 2.85;

(* 2.9 Rolling History Buffers & Moving Average Smoothing (Size 16) *)
arrHist_Metallization[iHistIndex] := x_Hat[2];
arrHist_ShaftDP[iHistIndex] := x_Hat[3];
iHistIndex := iHistIndex + 1;
IF iHistIndex > 16 THEN
    iHistIndex := 1;
END_IF;

rTempSum := 0.0;
FOR idx_k := 1 TO 16 DO
    rTempSum := rTempSum + arrHist_Metallization[idx_k];
END_FOR;
rFilter_Metallization_SMA := rTempSum / 16.0;

rTempSum := 0.0;
FOR idx_k := 1 TO 16 DO
    rTempSum := rTempSum + arrHist_ShaftDP[idx_k];
END_FOR;
rFilter_ShaftDP_SMA := rTempSum / 16.0;
"""
