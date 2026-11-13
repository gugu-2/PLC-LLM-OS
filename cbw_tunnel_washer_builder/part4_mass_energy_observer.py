# cbw_tunnel_washer_builder/part4_mass_energy_observer.py
# First-Principles Cyber-Physical Mass & Energy Balances & State Observer

def get_part4_mass_energy_observer():
    return """(* ==================================================================================================== *)
(* PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL MASS & ENERGY BALANCES & STATE-SPACE OBSERVER               *)
(* ==================================================================================================== *)

(* -------------------------------------------------------------------------------------------------- *)
(* EXOGENOUS DISTURBANCE VECTOR COLLATION                                                             *)
(* -------------------------------------------------------------------------------------------------- *)
vecDist[1] := rWT_01_BatchDryLinenMass_kg / 1.75;           (* Linen Mass Ingestion Rate [kg/min] *)
vecDist[2] := rIncomingColdWaterTemp_degC;                  (* Raw Freshwater Supply Temp [deg C] *)
vecDist[3] := rPT_801_SteamHeaderPress_bar;                 (* Live Steam Supply Header Pressure [bar] *)
vecDist[4] := rQT_01_PrewashTurbidity_NTU;                  (* Optical Soil Turbidity Influx [NTU] *)
vecDist[5] := rAmbientLaundryRoomTemp_degC;                 (* Laundry Facility Ambient Air Temp [deg C] *)
vecDist[6] := rTT_302_HydraulicOilTemp_degC;                (* Dewatering HPU Hydraulic Oil Temp [deg C] *)

(* -------------------------------------------------------------------------------------------------- *)
(* COUNTER-FLOW WATER & THERMAL ENERGY RECLAMATION DYNAMICS                                            *)
(* -------------------------------------------------------------------------------------------------- *)
(* Specific heat capacity of wash liquor Cp = 4.186 [kJ/(kg*K)], density rho = 1,000 [kg/m3]          *)
(* Heat transfer rate in clean water preheat exchanger: Q_rec = m_dot * Cp * Delta_T                 *)
IF rVotedFreshwaterFlow_m3h > 0.1 THEN
    (* Mass flow rate in kg/s = Flow [m3/h] * 1000 / 3600 *)
    rScratchSum := (rVotedFreshwaterFlow_m3h * 1000.0) / 3600.0;
    
    (* Temperature differential across clean water side of plate heat exchanger *)
    IF rVotedExchangerEffluent_degC > rIncomingColdWaterTemp_degC THEN
        rThermalEnergyReclaimed_kW := rScratchSum * 4.186 * (rVotedExchangerEffluent_degC - rIncomingColdWaterTemp_degC);
    ELSE
        rThermalEnergyReclaimed_kW := 0.0;
    END_IF;
ELSE
    rThermalEnergyReclaimed_kW := 0.0;
END_IF;

(* Cumulative Thermal & Water Consumption Integrators *)
rAccumulatedFreshwater_m3 := rAccumulatedFreshwater_m3 + (rVotedFreshwaterFlow_m3h * (rDeltaTime_s / 3600.0));
rAccumulatedReclaimedHeat_MJ := rAccumulatedReclaimedHeat_MJ + (rThermalEnergyReclaimed_kW * (rDeltaTime_s / 1000.0));

(* Real-Time Live Steam Mass Flow Estimation from Valve Position and Header Pressure *)
(* Saturated steam at 6.0 bar has latent heat h_fg = 2066 kJ/kg *)
IF rPT_801_SteamHeaderPress_bar > 2.0 THEN
    rScratchSum := (rMainWashSteamValveCmd_pct * 0.01 * 0.180 * SQRT(MAX(0.1, rPT_801_SteamHeaderPress_bar))) +
                   (rBleachSteamValveCmd_pct * 0.01 * 0.095 * SQRT(MAX(0.1, rPT_801_SteamHeaderPress_bar)));
    rAccumulatedLiveSteam_kg := rAccumulatedLiveSteam_kg + (rScratchSum * rDeltaTime_s);
END_IF;

(* Specific Key Performance Indicators (KPIs) per kg of Linen Processed *)
IF rAccumulatedLinenProcessed_kg > 10.0 THEN
    (* Specific Water Consumption in Liters per kg dry linen *)
    rSpecificWaterConsumption_L := (rAccumulatedFreshwater_m3 * 1000.0) / rAccumulatedLinenProcessed_kg;
    
    (* Specific Energy Consumption in kWh per kg dry linen (Thermal + Estimated Electric) *)
    rSpecificEnergyConsumption_kWh := ((rAccumulatedLiveSteam_kg * 0.625) - (rAccumulatedReclaimedHeat_MJ / 3.6)) / rAccumulatedLinenProcessed_kg;
    IF rSpecificEnergyConsumption_kWh < 0.15 THEN
        rSpecificEnergyConsumption_kWh := 0.15;
    END_IF;
ELSE
    rSpecificWaterConsumption_L := 6.5;
    rSpecificEnergyConsumption_kWh := 0.45;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* SENSOR MEASUREMENT VECTOR PACKING FOR OBSERVER INNOVATION (8 CHANNELS)                              *)
(* -------------------------------------------------------------------------------------------------- *)
vecY_meas[1] := rVotedMainWashTemp_degC;                    (* Main Wash Temperature TT-101 [deg C] *)
vecY_meas[2] := rVotedRinseConductivity_mS;                 (* Rinse Zone Conductivity AT-201 [mS/cm] *)
vecY_meas[3] := rVotedPressPressure_bar;                    (* Dewatering Press Pressure PT-301 [bar] *)
vecY_meas[4] := rVotedFreshwaterFlow_m3h;                   (* Cold Freshwater Makeup Flow FT-401 [m3/h] *)
vecY_meas[5] := rVotedDrumTorque_Nm;                        (* Drum Motor Drive Torque ST-501 [N*m] *)
vecY_meas[6] := rVotedExchangerEffluent_degC;               (* Heat Exchanger Effluent TT-701 [deg C] *)
vecY_meas[7] := vecX[8];                                    (* Residual Moisture (Virtual Output) [%] *)
vecY_meas[8] := rLT_901_PressRecoveryTankLvl_pct;           (* Press Water Tank Level LT-901 [%] *)

(* Current Actuator Command Vector Packing *)
vecU[1] := rMainWashSteamValveCmd_pct;
vecU[2] := rBleachSteamValveCmd_pct;
vecU[3] := rFreshwaterMakeupValveCmd_pct;
vecU[4] := rCounterFlowRecircPumpCmd_pct;
vecU[5] := rPressHydraulicServoCmd_bar;
vecU[6] := (rAlkaliDosingPumpCmd_ml + rDetergentDosingPumpCmd_ml) * 0.1;

(* -------------------------------------------------------------------------------------------------- *)
(* OUTPUT ESTIMATION: y_est = C * x + D * u                                                           *)
(* -------------------------------------------------------------------------------------------------- *)
FOR i := 1 TO 8 DO
    rScratchSum := 0.0;
    FOR j := 1 TO 10 DO
        rScratchSum := rScratchSum + (matC[i, j] * vecX[j]);
    END_FOR;
    FOR k := 1 TO 6 DO
        rScratchSum := rScratchSum + (matD[i, k] * vecU[k]);
    END_FOR;
    vecY_est[i] := rScratchSum;
    vecInnovation[i] := vecY_meas[i] - vecY_est[i];
END_FOR;

(* -------------------------------------------------------------------------------------------------- *)
(* OBSERVER STATE PROPAGATION & INNOVATION UPDATE: x[k+1] = A * x[k] + B * u[k] + L * Innovation     *)
(* -------------------------------------------------------------------------------------------------- *)
FOR i := 1 TO 10 DO
    rScratchSum := 0.0;
    
    (* Dynamic Propagation from System Matrix A *)
    FOR j := 1 TO 10 DO
        rScratchSum := rScratchSum + (matA[i, j] * vecX[j]);
    END_FOR;
    
    (* Control Input Influx from Input Matrix B *)
    FOR k := 1 TO 6 DO
        rScratchSum := rScratchSum + (matB[i, k] * vecU[k]);
    END_FOR;
    
    (* Luenberger Observer Innovation Correction from Gain Matrix L *)
    FOR m := 1 TO 8 DO
        rScratchSum := rScratchSum + (matL[i, m] * vecInnovation[m]);
    END_FOR;
    
    vecX_next[i] := rScratchSum;
END_FOR;

(* Physical Clamping of Propagated State Estimates *)
vecX_next[1]  := LIMIT(10.0, vecX_next[1], 95.0);          (* Pre-Wash Temperature Bounds [deg C] *)
vecX_next[2]  := LIMIT(15.0, vecX_next[2], 98.0);          (* Main Wash Core Temperature Bounds [deg C] *)
vecX_next[3]  := LIMIT(15.0, vecX_next[3], 95.0);          (* Bleach Zone Temperature Bounds [deg C] *)
vecX_next[4]  := LIMIT(0.01, vecX_next[4], 8.00);          (* Rinse Water Conductivity Bounds [mS/cm] *)
vecX_next[5]  := LIMIT(0.00, vecX_next[5], 10.0);          (* Active Alkali Concentration [g/L] *)
vecX_next[6]  := LIMIT(10.0, vecX_next[6], 85.0);          (* Heat Exchanger Preheated Outlet [deg C] *)
vecX_next[7]  := LIMIT(0.00, vecX_next[7], 55.0);          (* Hydraulic Extraction Pressure [bar] *)
vecX_next[8]  := LIMIT(42.0, vecX_next[8], 280.0);         (* Linen Cake Moisture Retention [%] *)
vecX_next[9]  := LIMIT(100.0, vecX_next[9], 5500.0);       (* Drum Geared Drive Torque Load [N*m] *)
vecX_next[10] := LIMIT(0.00, vecX_next[10], 100.0);        (* Press Water Recovery Buffer Level [%] *)

(* Update State Vector for Next Execution Scan *)
FOR i := 1 TO 10 DO
    vecX[i] := vecX_next[i];
END_FOR;

(* Surface State Estimates to Output Interface *)
rEstimatedCakeMoisture_pct := vecX[8];
"""
