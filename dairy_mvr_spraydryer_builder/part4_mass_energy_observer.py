# dairy_mvr_spraydryer_builder/part4_mass_energy_observer.py
# Lumina Cyber-Physical Systems Chair - V7 Max-Persona
# Part 4: Phase 2 - First-Principles Cyber-Physical Modeling, Thermodynamics & Luenberger State Estimation

def get_part4_mass_energy_observer():
    return """(* === PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL MODELING & LUENBERGER OBSERVER === *)

(* ------------------------------------------------------------------------------------------------- *)
(* CONSTRUCT MEASURED OUTPUT VECTOR Y_MEAS[1..6] FROM 2oo3 TMR VOTED SENSORS                        *)
(* ------------------------------------------------------------------------------------------------- *)
vec_yMeas[1] := rVoted_CalandriaLevel_mm * 0.001;   (* Convert Level mm -> m Liquid Sump Column *)
vec_yMeas[2] := rVoted_SolidsBrix_pct;              (* Calandria Concentrated Milk Solids [% TS] *)
vec_yMeas[3] := rVoted_MvrDiffPress_kPa;            (* MVR Turbo-Compressor Boost Pressure [kPa] *)
vec_yMeas[4] := rVoted_InletAirTemp_degC;           (* Drying Tower Inlet Hot Air Temperature [deg C] *)
vec_yMeas[5] := rExhaustAirRelHumidity_pct;         (* Drying Tower Exhaust Air Relative Humidity [% RH] *)
vec_yMeas[6] := rVoted_PowderMoisture_pct;          (* Final Milk Powder Moisture Content [% w/w] *)

(* ------------------------------------------------------------------------------------------------- *)
(* NON-LINEAR BOILING POINT ELEVATION (BPE) DYNAMIC COMPENSATION                                     *)
(* Empirical multi-component milk solute elevation equation (lactose, casein, whey, mineral salts)  *)
(* BPE(TS) = 0.0512 * TS + 0.00164 * TS^2 - 0.000012 * TS^3 [deg C]                                 *)
(* ------------------------------------------------------------------------------------------------- *)
rEstimated_BPE_degC := (0.051200 * vec_xEst[2]) + 
                       (0.001640 * vec_xEst[2] * vec_xEst[2]) - 
                       (0.000012 * vec_xEst[2] * vec_xEst[2] * vec_xEst[2]);

(* BPE physical saturation clamp [0.0..8.5 deg C] *)
IF rEstimated_BPE_degC < 0.0 THEN
    rEstimated_BPE_degC := 0.0;
ELSIF rEstimated_BPE_degC > 8.50 THEN
    rEstimated_BPE_degC := 8.50;
END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* MVR TURBO-COMPRESSOR THERMODYNAMICS & SURGE MARGIN COORDINATED DECOUPLING                         *)
(* Computes vapor mass flow, suction volumetric throughput, surge limit line (SLL) & surge margin   *)
(* ------------------------------------------------------------------------------------------------- *)
(* Evaporator water evaporation mass rate: m_evap = m_feed * (1 - TS_in / TS_out) [kg/h] *)
IF vec_xEst[2] > rFeedConcentration_pct THEN
    rEvaporationRate_kgh := rFT_904_MilkFeedFlow_kgh * (1.000 - (rFeedConcentration_pct / vec_xEst[2]));
ELSE
    rEvaporationRate_kgh := 0.0;
END_IF;

(* Calandria vapor volumetric suction flow rate: Q = m_dot_evap * v_vapor [m3/s] *)
(* At 62.4 deg C saturation, specific volume v_g ~ 7.42 [m3/kg] *)
rCompressorActualFlow_m3s := (rEvaporationRate_kgh / 3600.0) * 7.420;

(* Dynamic Surge Limit Line (SLL) volumetric flow threshold based on compressor characteristic *)
rCompressorSurgeLimitFlow_m3s := 0.780 * SQRT(MAX(1.0, rVoted_MvrDiffPress_kPa));

(* Active Surge Margin calculation: SM = (Q_actual - Q_surge) / Q_actual * 100% *)
IF rCompressorActualFlow_m3s > 0.100 THEN
    rSurgeMargin_pct := ((rCompressorActualFlow_m3s - rCompressorSurgeLimitFlow_m3s) / rCompressorActualFlow_m3s) * 100.0;
ELSE
    rSurgeMargin_pct := -10.0;
END_IF;

(* Coordinated Fast Anti-Surge Override Valve Controller *)
IF rSurgeMargin_pct < 12.0 THEN
    bAntiSurgeActive := TRUE;
    (* Rapidly modulate bypass recycle valve to inject discharge vapor back to suction *)
    rAntiSurgePidOutput := (12.0 - rSurgeMargin_pct) * 8.50;
    IF rAntiSurgePidOutput > 100.0 THEN
        rAntiSurgePidOutput := 100.0;
    ELSIF rAntiSurgePidOutput < 0.0 THEN
        rAntiSurgePidOutput := 0.0;
    END_IF;
    rCV_AntiSurgeBypassValve_pct := rAntiSurgePidOutput;
ELSE
    bAntiSurgeActive := FALSE;
    rAntiSurgePidOutput := 0.0;
    rCV_AntiSurgeBypassValve_pct := 0.0;
END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* SPRAY TOWER DROPLET ATOMIZATION & DRYING KINETICS ESTIMATION                                      *)
(* Droplet Sauter Mean Diameter (SMD D[3,2]) based on high-pressure swirl nozzle hydrodynamic laws   *)
(* D32 = C_atom * (mu_slurry^0.2) / (P_atom^0.4) [microns]                                          *)
(* ------------------------------------------------------------------------------------------------- *)
IF rCV_AtomizerNozzlePress_bar > 10.0 THEN
    rDropletSauterMeanDiam_um := 480.0 / (SQRT(rCV_AtomizerNozzlePress_bar));
ELSE
    rDropletSauterMeanDiam_um := 120.0;
END_IF;

(* Real-time Finished Dry Milk Powder Production Rate [kg/h] *)
IF vec_xEst[2] > 10.0 THEN
    rPowderTowerThroughput_kgh := (rFT_904_MilkFeedFlow_kgh * (rFeedConcentration_pct / 100.0)) / 
                                  MAX(0.50, (1.000 - (vec_xEst[7] / 100.0)));
ELSE
    rPowderTowerThroughput_kgh := 0.0;
END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* LUENBERGER OBSERVER EXECUTION: COMPUTATION OF ESTIMATED MEASUREMENTS Y_EST[1..6]                  *)
(* yEst = C * xEst + D * uCmd                                                                        *)
(* ------------------------------------------------------------------------------------------------- *)
FOR i := 1 TO 6 DO
    rSum := 0.0;
    FOR j := 1 TO 8 DO
        rSum := rSum + (matC[i, j] * vec_xEst[j]);
    END_FOR;
    FOR m := 1 TO 6 DO
        rSum := rSum + (matD[i, m] * vec_uCmd[m]);
    END_FOR;
    vec_yEst[i] := rSum;
END_FOR;

(* ------------------------------------------------------------------------------------------------- *)
(* INNOVATION RESIDUAL CALCULATION: INNOV[1..6] = Y_MEAS[1..6] - Y_EST[1..6]                         *)
(* ------------------------------------------------------------------------------------------------- *)
FOR i := 1 TO 6 DO
    vec_Innov[i] := vec_yMeas[i] - vec_yEst[i];
END_FOR;

(* ------------------------------------------------------------------------------------------------- *)
(* LUENBERGER OBSERVER STATE PROPAGATION & CORRECTION UPDATE                                         *)
(* xPred = A * xEst + B * uCmd + L * Innov                                                           *)
(* ------------------------------------------------------------------------------------------------- *)
FOR i := 1 TO 8 DO
    rSum := 0.0;
    (* State transition contribution *)
    FOR j := 1 TO 8 DO
        rSum := rSum + (matA[i, j] * vec_xEst[j]);
    END_FOR;
    (* Control input contribution *)
    FOR m := 1 TO 6 DO
        rSum := rSum + (matB[i, m] * vec_uCmd[m]);
    END_FOR;
    (* Measurement innovation correction contribution *)
    FOR j := 1 TO 6 DO
        rSum := rSum + (matL[i, j] * vec_Innov[j]);
    END_FOR;
    vec_xPred[i] := rSum;
END_FOR;

(* Latch propagated state into active cyber-physical state estimate *)
FOR i := 1 TO 8 DO
    vec_xEst[i] := vec_xPred[i];
END_FOR;

(* Physical Non-Negativity Bounds Clamping on Estimated States *)
IF vec_xEst[1] < 0.050 THEN vec_xEst[1] := 0.050; END_IF; (* Min level 0.05 m *)
IF vec_xEst[2] < 5.000 THEN vec_xEst[2] := 5.000; END_IF; (* Min solids 5.0% TS *)
IF vec_xEst[3] < 0.000 THEN vec_xEst[3] := 0.000; END_IF; (* Min DP 0.0 kPa *)
IF vec_xEst[4] < 20.00 THEN vec_xEst[4] := 20.00; END_IF; (* Min suction temp 20 deg C *)
IF vec_xEst[5] < 20.00 THEN vec_xEst[5] := 20.00; END_IF; (* Min inlet temp 20 deg C *)
IF vec_xEst[6] < 2.000 THEN vec_xEst[6] := 2.000; END_IF; (* Min RH 2% *)
IF vec_xEst[7] < 0.500 THEN vec_xEst[7] := 0.500; END_IF; (* Min moisture 0.5% *)
IF vec_xEst[8] < 0.100 THEN vec_xEst[8] := 0.100; END_IF; (* Min recirc velocity 0.1 m/s *)
"""
