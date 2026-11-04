# Remaining sections of FB_Chemical_CryoASU_DoubleColumn_AntiSurge
import json, uuid, re, os, sys

def get_phases_2_to_7():
    return """
(* ===================================================================================================================
 * PHASE 2: CRYOGENIC THERMODYNAMICS, PENG-ROBINSON VLE, MAC AERODYNAMICS & SAFETY KINETICS
 * =================================================================================================================== *)
rTotalPlantUptime_s := rTotalPlantUptime_s + c_rTs;

(* 1. Cryogenic Peng-Robinson Equation of State Equilibrium (N2, Ar, O2) *)
rReducedTemp := (rVoted_CondenserTemp_degC + 273.15) / c_rTc_N2_K;
rAlphaPR := (1.0 + (0.37464 + (1.54226 * c_rOmega_N2) - (0.26992 * c_rOmega_N2 * c_rOmega_N2)) * (1.0 - SQRT(MAX(0.01, rReducedTemp)))) * (1.0 + (0.37464 + (1.54226 * c_rOmega_N2) - (0.26992 * c_rOmega_N2 * c_rOmega_N2)) * (1.0 - SQRT(MAX(0.01, rReducedTemp))));
rAntoinePvap := EXP(8.95 - (650.0 / MAX(10.0, (rVoted_CondenserTemp_degC + 273.15 - 3.5))));
rCalculated_PengRobinson_K_N2 := rAntoinePvap / MAX(0.5, rVoted_LP_Pressure_bar);

rReducedTemp := (rVoted_CondenserTemp_degC + 273.15) / c_rTc_Ar_K;
rAntoinePvap := EXP(9.25 - (800.0 / MAX(10.0, (rVoted_CondenserTemp_degC + 273.15 - 5.0))));
rCalculated_PengRobinson_K_Ar := rAntoinePvap / MAX(0.5, rVoted_LP_Pressure_bar);

rReducedTemp := (rVoted_CondenserTemp_degC + 273.15) / c_rTc_O2_K;
rAntoinePvap := EXP(9.15 - (750.0 / MAX(10.0, (rVoted_CondenserTemp_degC + 273.15 - 4.5))));
rCalculated_PengRobinson_K_O2 := rAntoinePvap / MAX(0.5, rVoted_LP_Pressure_bar);

(* 2. 45 MW Centrifugal MAC Aerodynamic Dynamic Anti-Surge & Head-Flow Coordinates *)
rGasHeadVenturi_bar := rVoted_MAC_VenturiDP_mbar * 0.001;
rSurgeLimitDP_bar := c_rMAC_SurgeOffset_b0 + (c_rMAC_SurgeSlope_Ksll * rVoted_MAC_VenturiDP_mbar);
rSurgeControlDP_bar := rSurgeLimitDP_bar * (1.0 + (rTarget_AntiSurgeMargin_pct / 100.0));

IF (rVoted_MAC_DischargePress_bar - 1.013) > 0.5 THEN
    rCalculated_SurgeMargin_pct := ((rVoted_MAC_VenturiDP_mbar - ((rVoted_MAC_DischargePress_bar - c_rMAC_SurgeOffset_b0) / MAX(0.001, c_rMAC_SurgeSlope_Ksll))) / MAX(1.0, rVoted_MAC_VenturiDP_mbar)) * 100.0;
ELSE
    rCalculated_SurgeMargin_pct := 15.0;
END_IF;

rCalculated_SurgeMargin_pct := MAX(-20.0, MIN(50.0, rCalculated_SurgeMargin_pct));
rROC_SurgeMargin_pct_s := (rCalculated_SurgeMargin_pct - rPrev_SurgeMargin_pct) / c_rTs;
rPrev_SurgeMargin_pct := rCalculated_SurgeMargin_pct;

rROC_MAC_DischargePress_bar_s := (rVoted_MAC_DischargePress_bar - rPrev_MAC_DischargePress_bar) / c_rTs;
rPrev_MAC_DischargePress_bar := rVoted_MAC_DischargePress_bar;

(* 3. Cryogenic Turbo-Expander (85,000 RPM) Isentropic Refrigeration *)
IF (rVoted_HP_Pressure_bar > 1.2) AND (rVoted_LP_Pressure_bar > 0.5) THEN
    rTheoreticalDeltaT_Expander := (rVoted_MAC_DischargeTemp_degC + 273.15) * (1.0 - (1.0 / MAX(1.1, (rVoted_HP_Pressure_bar / rVoted_LP_Pressure_bar)))**(0.2857));
    rActualDeltaT_Expander := rTheoreticalDeltaT_Expander * c_rExpander_DesignEfficiency;
    rCalculated_ExpanderEfficiency_pct := c_rExpander_DesignEfficiency * 100.0;
    rThermalPowerExpander_kW := (rVoted_Expander_RPM / 82500.0) * 1850.0;
ELSE
    rCalculated_ExpanderEfficiency_pct := 0.0;
    rThermalPowerExpander_kW := 0.0;
END_IF;

(* 4. Main Condenser-Reboiler Thermosiphon Natural Circulation & Acetylene Mass Balance *)
rDeltaH_Reboiler_kW := (c_rReboiler_CoreArea_m2 * c_rReboiler_HeatTransferU_W_m2K * 1.65) * 0.001;
rCalculated_LOX_EvaporationRate_kgh := (rDeltaH_Reboiler_kW / c_rLatentHeatO2_kJ_kg) * 3600.0;
rCalculated_ThermosiphonFlowRate_m3h := 0.65 * 0.45 * SQRT(2.0 * 9.80665 * c_rReboiler_CoreHeight_m * ((c_rDensityLOX_kg_m3 - 420.0) / c_rDensityLOX_kg_m3)) * 3600.0;

(* Modeled Acetylene Accumulation Rate [ppm/h] *)
rCalculated_AcetyleneAccumulationRate_ppmh := (((rVoted_MAC_Flow_m3h * 1.25 * 0.00000002) - (rCmd_LOX_ContinuousPurge_pct * 0.01 * 5000.0 * rVoted_Acetylene_ppm * 0.000001)) / c_rReboiler_LOX_SumpVolume_m3) * 3600.0;

(* 5. Overall Specific Power Consumption [kWh / Nm3 O2] *)
rCompressorWork_kW := 42500.0 * (rVoted_MAC_Flow_m3h / 185000.0) * (rVoted_MAC_DischargePress_bar / 6.20);
rNetProductOxygen_Nm3h := MAX(1000.0, rVoted_GOX_Flow_Nm3h);
rCalculated_SpecificPower_kWh_Nm3O2 := (rCompressorWork_kW - rThermalPowerExpander_kW) / rNetProductOxygen_Nm3h;

(* ===================================================================================================================
 * PHASE 3: 8x8 MULTIVARIABLE DISCRETE STATE-SPACE PROPAGATION
 * =================================================================================================================== *)
vecX[1] := rVoted_MAC_DischargePress_bar - rTarget_MAC_DischargePress_bar;
vecX[2] := rVoted_MAC_Flow_m3h - rTarget_MAC_InletAirFlow_m3h;
vecX[3] := rVoted_HP_Pressure_bar - rTarget_HP_ColumnPress_bar;
vecX[4] := rVoted_LP_Pressure_bar - rTarget_LP_ColumnPress_bar;
vecX[5] := rVoted_LOX_Level_pct - rTarget_LOX_Level_pct;
vecX[6] := rVoted_Acetylene_ppm - 0.0;
vecX[7] := rVoted_Argon_O2_pct - rTarget_ArgonPurity_O2_pct;
vecX[8] := rVoted_Expander_RPM - rTarget_ExpanderSpeed_RPM;

(* Compute Projected Next State Vector x[k+1] = matA * x[k] + matB * u[k] *)
FOR iLoop := 1 TO 8 DO
    rTempSum := 0.0;
    FOR jLoop := 1 TO 8 DO
        rTempSum := rTempSum + (matA[iLoop, jLoop] * vecX[jLoop]);
    END_FOR;
    FOR kLoop := 1 TO 5 DO
        rTempSum := rTempSum + (matB[iLoop, kLoop] * vecU[kLoop]);
    END_FOR;
    vecX_next[iLoop] := rTempSum;
END_FOR;

(* Compute Synthetic Output Observation y[k] = matC * x[k] + matD * u[k] *)
FOR iLoop := 1 TO 8 DO
    rTempSum := 0.0;
    FOR jLoop := 1 TO 8 DO
        rTempSum := rTempSum + (matC[iLoop, jLoop] * vecX[jLoop]);
    END_FOR;
    FOR kLoop := 1 TO 5 DO
        rTempSum := rTempSum + (matD[iLoop, kLoop] * vecU[kLoop]);
    END_FOR;
    vecY[iLoop] := rTempSum;
END_FOR;

(* ===================================================================================================================
 * PHASE 4: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION
 * =================================================================================================================== *)
rMPC_ObjectiveCost_J := 0.0;
FOR iLoop := 1 TO 8 DO
    rMPC_ObjectiveCost_J := rMPC_ObjectiveCost_J + (arrQ_Weight[iLoop] * (vecX[iLoop] - vecX_ref[iLoop]) * (vecX[iLoop] - vecX_ref[iLoop]));
    rMPC_ObjectiveCost_J := rMPC_ObjectiveCost_J + (arrP_TerminalWeight[iLoop] * (vecX_next[iLoop] - vecX_ref[iLoop]) * (vecX_next[iLoop] - vecX_ref[iLoop]));
END_FOR;
FOR jLoop := 1 TO 5 DO
    rMPC_ObjectiveCost_J := rMPC_ObjectiveCost_J + (arrR_Weight[jLoop] * vecU[jLoop] * vecU[jLoop]);
    rMPC_ObjectiveCost_J := rMPC_ObjectiveCost_J + (arrS_Weight[jLoop] * (vecU[jLoop] - vecU_prev[jLoop]) * (vecU[jLoop] - vecU_prev[jLoop]));
END_FOR;

IF bAutoMode AND NOT bCompressorSurgeTrip AND NOT bHydrocarbonExplosionHazardTrip AND NOT bEmergencyDepressActive THEN
    (* 3 Iterations of Projected Gradient Descent (PGD) *)
    FOR iPGD_Iter := 1 TO 3 DO
        FOR kLoop := 1 TO 5 DO
            rGradientElement := (2.0 * arrR_Weight[kLoop] * vecU[kLoop]) + (2.0 * arrS_Weight[kLoop] * (vecU[kLoop] - vecU_prev[kLoop]));
            FOR iLoop := 1 TO 8 DO
                rGradientElement := rGradientElement + (2.0 * arrP_TerminalWeight[iLoop] * (vecX_next[iLoop] - vecX_ref[iLoop]) * matB[iLoop, kLoop]);
            END_FOR;
            vecGradU[kLoop] := rGradientElement;
            rActuatorCandidate := vecU[kLoop] - (c_rPGD_StepSize * vecGradU[kLoop]);
            rActuatorCandidate := MAX(arrU_Min[kLoop], MIN(arrU_Max[kLoop], rActuatorCandidate));
            vecU[kLoop] := rActuatorCandidate;
        END_FOR;
    END_FOR;

    (* Aerodynamic Dynamic Surge Margin Rapid Feedforward Pulse *)
    IF rCalculated_SurgeMargin_pct < rTarget_AntiSurgeMargin_pct THEN
        bAntiSurgeActive := TRUE;
        vecU[1] := vecU[1] + (3.50 * (rTarget_AntiSurgeMargin_pct - rCalculated_SurgeMargin_pct));
        IF rROC_SurgeMargin_pct_s < -2.0 THEN
            vecU[1] := vecU[1] + (-1.50 * rROC_SurgeMargin_pct_s);
        END_IF;
    ELSE
        bAntiSurgeActive := FALSE;
    END_IF;

    (* Reboiler Hydrocarbon Acetylene Safety Feedforward Purge Boost *)
    IF rVoted_Acetylene_ppm > 0.040 THEN
        vecU[4] := vecU[4] + (125.0 * (rVoted_Acetylene_ppm - 0.040));
    END_IF;

    (* Slew Rate Clamping & Actuator Constraint Enforcement *)
    FOR jLoop := 1 TO 5 DO
        vecDeltaU[jLoop] := vecU[jLoop] - vecU_prev[jLoop];
        IF vecDeltaU[jLoop] > arrDeltaU_Max[jLoop] THEN
            vecU[jLoop] := vecU_prev[jLoop] + arrDeltaU_Max[jLoop];
        ELSIF vecDeltaU[jLoop] < -arrDeltaU_Max[jLoop] THEN
            vecU[jLoop] := vecU_prev[jLoop] - arrDeltaU_Max[jLoop];
        END_IF;
        vecU[jLoop] := MAX(arrU_Min[jLoop], MIN(arrU_Max[jLoop], vecU[jLoop]));
        vecU_prev[jLoop] := vecU[jLoop];
    END_FOR;
END_IF;

(* ===================================================================================================================
 * PHASE 5: 12-STAGE DETERMINISTIC PLANT OPERATIONAL FINITE STATE MACHINE (FSM)
 * =================================================================================================================== *)
rStateTimer_s := rStateTimer_s + c_rTs;

(* Emergency Interlock Override Check *)
IF NOT bEmergencyStop_NC OR bEmergencyDepressCommand THEN
    iFSM_State := 12; (* EMERGENCY_DEPRESSURIZATION *)
END_IF;

CASE iFSM_State OF
    1: (* State 1: COLD_BOX_WARM_PURGE *)
        bReady := FALSE;
        bBusy := TRUE;
        bUnitInSteadyState := FALSE;
        bCmd_ColdBoxWarmPurgeVent := TRUE;
        bCmd_MolecularSieveSwitchover := FALSE;
        bCmd_FastRecycleOpenTrip := FALSE;
        bCmd_LOX_EmergencyDumpValve := FALSE;
        rCmd_MAC_AntiSurgeValve_pct := 100.0;
        rCmd_MAC_IGV_Position_pct := 0.0;
        rCmd_Expander_Nozzle_pct := 0.0;
        rCmd_Expander_BrakeBlower_pct := 0.0;
        rCmd_LOX_ContinuousPurge_pct := 100.0;
        rCmd_ArgonSideDrawValve_pct := 0.0;
        rCmd_RichLiquidAirFeedValve_pct := 0.0;
        rCmd_PureLiquidN2RefluxValve_pct := 0.0;
        rCmd_GOX_DeliveryValve_pct := 0.0;
        rCmd_GAN_DeliveryValve_pct := 0.0;
        rWarmPurgeTimer_s := rWarmPurgeTimer_s + c_rTs;

        IF bEnable AND bColdBoxWarmPurgePermissive AND (rWarmPurgeTimer_s >= 60.0) THEN
            rWarmPurgeTimer_s := 0.0;
            rStateTimer_s := 0.0;
            iFSM_State := 2; (* Advance to MOLECULAR_SIEVE_DRYING *)
        END_IF;

    2: (* State 2: MOLECULAR_SIEVE_DRYING *)
        bReady := FALSE;
        bBusy := TRUE;
        bUnitInSteadyState := FALSE;
        bCmd_ColdBoxWarmPurgeVent := FALSE;
        bCmd_MolecularSieveSwitchover := TRUE;
        rCmd_MAC_AntiSurgeValve_pct := 100.0;
        rCmd_MAC_IGV_Position_pct := 15.0;
        rCmd_Expander_Nozzle_pct := 0.0;
        rCmd_LOX_ContinuousPurge_pct := 20.0;
        rMolSieveDryTimer_s := rMolSieveDryTimer_s + c_rTs;

        IF bMolSieveDryingPermissive AND (rMolSieveDryTimer_s >= 45.0) THEN
            rMolSieveDryTimer_s := 0.0;
            rStateTimer_s := 0.0;
            iFSM_State := 3; (* Advance to MAC_STARTUP_ANTISURGE_LOCK *)
        END_IF;

    3: (* State 3: MAC_STARTUP_ANTISURGE_LOCK *)
        bReady := FALSE;
        bBusy := TRUE;
        bUnitInSteadyState := FALSE;
        rCmd_MAC_AntiSurgeValve_pct := 100.0;
        rCmd_MAC_IGV_Position_pct := 25.0;
        rCmd_Expander_Nozzle_pct := 0.0;
        rMAC_SpinupTimer_s := rMAC_SpinupTimer_s + c_rTs;

        IF bCompressorStartPermissive AND (rVoted_MAC_DischargePress_bar >= 5.20) AND (rMAC_SpinupTimer_s >= 30.0) THEN
            rMAC_SpinupTimer_s := 0.0;
            rStateTimer_s := 0.0;
            iFSM_State := 4; (* Advance to EXPANDER_CHILLDOWN_START *)
        END_IF;

    4: (* State 4: EXPANDER_CHILLDOWN_START *)
        bReady := FALSE;
        bBusy := TRUE;
        bUnitInSteadyState := FALSE;
        rCmd_MAC_AntiSurgeValve_pct := 65.0;
        rCmd_MAC_IGV_Position_pct := 40.0;
        rCmd_Expander_Nozzle_pct := 30.0;
        rCmd_Expander_BrakeBlower_pct := 25.0;
        rExpanderChilldownTimer_s := rExpanderChilldownTimer_s + c_rTs;

        IF bExpanderStartPermissive AND (rVoted_Expander_RPM >= 40000.0) AND (rExpanderChilldownTimer_s >= 40.0) THEN
            rExpanderChilldownTimer_s := 0.0;
            rStateTimer_s := 0.0;
            iFSM_State := 5; (* Advance to LIQUID_AIR_ACCUMULATION *)
        END_IF;

    5: (* State 5: LIQUID_AIR_ACCUMULATION *)
        bReady := FALSE;
        bBusy := TRUE;
        bUnitInSteadyState := FALSE;
        rCmd_MAC_AntiSurgeValve_pct := 35.0;
        rCmd_MAC_IGV_Position_pct := 55.0;
        rCmd_Expander_Nozzle_pct := 55.0;
        rCmd_Expander_BrakeBlower_pct := 45.0;
        rLiquefactionTimer_s := rLiquefactionTimer_s + c_rTs;

        IF (rVoted_HP_SumpLevel_pct >= 40.0) AND (rLiquefactionTimer_s >= 50.0) THEN
            rLiquefactionTimer_s := 0.0;
            rStateTimer_s := 0.0;
            iFSM_State := 6; (* Advance to HP_LP_COLUMN_PRESSURIZATION *)
        END_IF;

    6: (* State 6: HP_LP_COLUMN_PRESSURIZATION *)
        bReady := FALSE;
        bBusy := TRUE;
        bUnitInSteadyState := FALSE;
        rCmd_MAC_AntiSurgeValve_pct := 15.0;
        rCmd_MAC_IGV_Position_pct := 68.0;
        rCmd_Expander_Nozzle_pct := 65.0;
        rCmd_RichLiquidAirFeedValve_pct := 35.0;
        rCmd_PureLiquidN2RefluxValve_pct := 25.0;
        rColumnPressurizeTimer_s := rColumnPressurizeTimer_s + c_rTs;

        IF (rVoted_HP_Pressure_bar >= 5.60) AND (rVoted_LP_Pressure_bar >= 1.35) AND (rColumnPressurizeTimer_s >= 35.0) THEN
            rColumnPressurizeTimer_s := 0.0;
            rStateTimer_s := 0.0;
            iFSM_State := 7; (* Advance to CONDENSER_REBOILER_THERMOSIPHON *)
        END_IF;

    7: (* State 7: CONDENSER_REBOILER_THERMOSIPHON *)
        bReady := FALSE;
        bBusy := TRUE;
        bUnitInSteadyState := FALSE;
        rCmd_MAC_AntiSurgeValve_pct := 5.0;
        rCmd_MAC_IGV_Position_pct := 72.0;
        rCmd_Expander_Nozzle_pct := 58.0;
        rCmd_RichLiquidAirFeedValve_pct := 52.0;
        rCmd_PureLiquidN2RefluxValve_pct := 48.0;
        rCmd_LOX_ContinuousPurge_pct := 3.5;
        rThermosiphonPrimeTimer_s := rThermosiphonPrimeTimer_s + c_rTs;

        IF (rVoted_LOX_Level_pct >= 55.0) AND (rCalculated_ThermosiphonFlowRate_m3h >= 250.0) AND (rThermosiphonPrimeTimer_s >= 40.0) THEN
            rThermosiphonPrimeTimer_s := 0.0;
            rStateTimer_s := 0.0;
            iFSM_State := 8; (* Advance to STEADY_STATE_O2_N2_SEPARATION *)
        END_IF;

    8: (* State 8: STEADY_STATE_O2_N2_SEPARATION *)
        bReady := TRUE;
        bBusy := FALSE;
        bUnitInSteadyState := TRUE;
        rCmd_MAC_AntiSurgeValve_pct := vecU[1];
        rCmd_MAC_IGV_Position_pct := vecU[2];
        rCmd_Expander_Nozzle_pct := vecU[3];
        rCmd_LOX_ContinuousPurge_pct := vecU[4];
        rCmd_ArgonSideDrawValve_pct := vecU[5];
        rCmd_RichLiquidAirFeedValve_pct := 62.0;
        rCmd_PureLiquidN2RefluxValve_pct := 58.0;
        rCmd_GOX_DeliveryValve_pct := 75.0;
        rCmd_GAN_DeliveryValve_pct := 85.0;

        IF bArgonDrawPermissive AND (rVoted_LOX_Level_pct >= 60.0) THEN
            rStateTimer_s := 0.0;
            iFSM_State := 9; (* Advance to ARGON_COLUMN_COOLING_DRAW *)
        ELSIF rVoted_Acetylene_ppm > 0.045 THEN
            rStateTimer_s := 0.0;
            iFSM_State := 10; (* Advance to LOX_SAFETY_PURGE_RAMP *)
        END_IF;

    9: (* State 9: ARGON_COLUMN_COOLING_DRAW *)
        bReady := TRUE;
        bBusy := FALSE;
        bUnitInSteadyState := TRUE;
        rCmd_MAC_AntiSurgeValve_pct := vecU[1];
        rCmd_MAC_IGV_Position_pct := vecU[2];
        rCmd_Expander_Nozzle_pct := vecU[3];
        rCmd_LOX_ContinuousPurge_pct := vecU[4];
        rCmd_ArgonSideDrawValve_pct := vecU[5];
        rArgonCommissionTimer_s := rArgonCommissionTimer_s + c_rTs;

        IF rVoted_Acetylene_ppm > 0.045 THEN
            rArgonCommissionTimer_s := 0.0;
            rStateTimer_s := 0.0;
            iFSM_State := 10; (* Advance to LOX_SAFETY_PURGE_RAMP *)
        END_IF;

    10: (* State 10: LOX_SAFETY_PURGE_RAMP *)
        bReady := TRUE;
        bBusy := TRUE;
        bUnitInSteadyState := FALSE;
        rCmd_LOX_ContinuousPurge_pct := 15.0;
        rCmd_MAC_AntiSurgeValve_pct := vecU[1];
        rCmd_MAC_IGV_Position_pct := vecU[2];
        rCmd_Expander_Nozzle_pct := vecU[3];
        rCmd_ArgonSideDrawValve_pct := vecU[5] * 0.80;
        rLOX_PurgeRampTimer_s := rLOX_PurgeRampTimer_s + c_rTs;

        IF (rVoted_Acetylene_ppm <= 0.020) AND (rLOX_PurgeRampTimer_s >= 30.0) THEN
            rLOX_PurgeRampTimer_s := 0.0;
            rStateTimer_s := 0.0;
            iFSM_State := 8; (* Return to STEADY_STATE_O2_N2_SEPARATION *)
        END_IF;

    11: (* State 11: CRYOGENIC_DRAIN_DRAIN *)
        bReady := FALSE;
        bBusy := TRUE;
        bUnitInSteadyState := FALSE;
        rCmd_MAC_AntiSurgeValve_pct := 100.0;
        rCmd_MAC_IGV_Position_pct := 15.0;
        rCmd_Expander_Nozzle_pct := 0.0;
        rCmd_LOX_ContinuousPurge_pct := 100.0;
        rCmd_RichLiquidAirFeedValve_pct := 100.0;
        rDrainTimer_s := rDrainTimer_s + c_rTs;

        IF (rVoted_LOX_Level_pct <= 5.0) AND (rVoted_HP_SumpLevel_pct <= 5.0) THEN
            rDrainTimer_s := 0.0;
            rStateTimer_s := 0.0;
            iFSM_State := 1; (* Return to COLD_BOX_WARM_PURGE *)
        END_IF;

    12: (* State 12: EMERGENCY_DEPRESSURIZATION *)
        bReady := FALSE;
        bBusy := FALSE;
        bUnitInSteadyState := FALSE;
        bEmergencyDepressActive := TRUE;
        bCmd_FastRecycleOpenTrip := TRUE;
        rCmd_MAC_AntiSurgeValve_pct := 100.0;
        rCmd_MAC_IGV_Position_pct := 0.0;
        rCmd_Expander_Nozzle_pct := 0.0;
        rCmd_Expander_BrakeBlower_pct := 100.0;
        bCmd_LOX_EmergencyDumpValve := TRUE;
        rCmd_LOX_ContinuousPurge_pct := 100.0;
        rCmd_ArgonSideDrawValve_pct := 0.0;
        rCmd_RichLiquidAirFeedValve_pct := 0.0;
        rCmd_PureLiquidN2RefluxValve_pct := 0.0;
        rCmd_GOX_DeliveryValve_pct := 0.0;
        rCmd_GAN_DeliveryValve_pct := 0.0;
        rEmergencyDepressTimer_s := rEmergencyDepressTimer_s + c_rTs;

        IF bResetFault AND bEmergencyStop_NC AND NOT bEmergencyDepressCommand THEN
            bEmergencyDepressActive := FALSE;
            bCompressorSurgeTrip := FALSE;
            bHydrocarbonExplosionHazardTrip := FALSE;
            bExpanderOverspeedTrip := FALSE;
            bCmd_FastRecycleOpenTrip := FALSE;
            bCmd_LOX_EmergencyDumpValve := FALSE;
            rEmergencyDepressTimer_s := 0.0;
            rStateTimer_s := 0.0;
            iFSM_State := 1; (* Reset to COLD_BOX_WARM_PURGE *)
        END_IF;
END_CASE;

nActiveFSM_State := iFSM_State;

(* ===================================================================================================================
 * PHASE 6: ISA-18.2 MULTI-TIER PROCESS ALARM ENGINE & DIAGNOSTIC WORD BIT-PACKING
 * =================================================================================================================== *)
(* 1. Main Air Compressor Discharge Pressure Alarm Ladder *)
IF rVoted_MAC_DischargePress_bar >= c_rMAC_Press_Trip_HI_HI THEN
    bAlarm_MAC_Press_HI_HI := TRUE;
    bCompressorSurgeTrip := TRUE;
    iFSM_State := 12;
ELSIF rVoted_MAC_DischargePress_bar <= (c_rMAC_Press_Trip_HI_HI - c_rMAC_Press_Deadband) THEN
    bAlarm_MAC_Press_HI_HI := FALSE;
END_IF;

IF rVoted_MAC_DischargePress_bar >= c_rMAC_Press_Alarm_HI THEN
    bAlarm_MAC_Press_HI := TRUE;
ELSIF rVoted_MAC_DischargePress_bar <= (c_rMAC_Press_Alarm_HI - c_rMAC_Press_Deadband) THEN
    bAlarm_MAC_Press_HI := FALSE;
END_IF;

IF rVoted_MAC_DischargePress_bar <= c_rMAC_Press_Alarm_LO THEN
    bAlarm_MAC_Press_LO := TRUE;
ELSIF rVoted_MAC_DischargePress_bar >= (c_rMAC_Press_Alarm_LO + c_rMAC_Press_Deadband) THEN
    bAlarm_MAC_Press_LO := FALSE;
END_IF;

IF rVoted_MAC_DischargePress_bar <= c_rMAC_Press_Trip_LO_LO THEN
    bAlarm_MAC_Press_LO_LO := TRUE;
    iFSM_State := 12;
ELSIF rVoted_MAC_DischargePress_bar >= (c_rMAC_Press_Trip_LO_LO + c_rMAC_Press_Deadband) THEN
    bAlarm_MAC_Press_LO_LO := FALSE;
END_IF;

(* 2. Aerodynamic Surge Safety Margin Alarm Ladder *)
IF rCalculated_SurgeMargin_pct <= c_rSurge_Trip_LO_LO THEN
    bAlarm_SurgeMargin_LO_LO := TRUE;
    bCompressorSurgeTrip := TRUE;
    iFSM_State := 12;
ELSIF rCalculated_SurgeMargin_pct >= (c_rSurge_Trip_LO_LO + c_rSurge_Deadband) THEN
    bAlarm_SurgeMargin_LO_LO := FALSE;
END_IF;

IF rCalculated_SurgeMargin_pct <= c_rSurge_Alarm_LO THEN
    bAlarm_SurgeMargin_LO := TRUE;
ELSIF rCalculated_SurgeMargin_pct >= (c_rSurge_Alarm_LO + c_rSurge_Deadband) THEN
    bAlarm_SurgeMargin_LO := FALSE;
END_IF;

IF rROC_SurgeMargin_pct_s <= c_rSurge_ROC_Limit THEN
    bAlarm_SurgeMargin_ROC := TRUE;
ELSE
    bAlarm_SurgeMargin_ROC := FALSE;
END_IF;

(* 3. Reboiler Hydrocarbon Acetylene Explosion Trip Ladder *)
IF rVoted_Acetylene_ppm >= c_rAcetylene_Trip_HI_HI THEN
    bAlarm_Acetylene_HI_HI := TRUE;
    bHydrocarbonExplosionHazardTrip := TRUE;
    bCmd_LOX_EmergencyDumpValve := TRUE;
    iFSM_State := 12;
ELSIF rVoted_Acetylene_ppm <= (c_rAcetylene_Trip_HI_HI - c_rAcetylene_Deadband) THEN
    bAlarm_Acetylene_HI_HI := FALSE;
END_IF;

IF rVoted_Acetylene_ppm >= c_rAcetylene_Alarm_HI THEN
    bAlarm_Acetylene_HI := TRUE;
ELSIF rVoted_Acetylene_ppm <= (c_rAcetylene_Alarm_HI - c_rAcetylene_Deadband) THEN
    bAlarm_Acetylene_HI := FALSE;
END_IF;

(* 4. Main Reboiler LOX Level Alarm Ladder *)
IF rVoted_LOX_Level_pct >= c_rLOX_Level_Trip_HI_HI THEN
    bAlarm_LOX_Level_HI_HI := TRUE;
ELSIF rVoted_LOX_Level_pct <= (c_rLOX_Level_Trip_HI_HI - c_rLOX_Level_Deadband) THEN
    bAlarm_LOX_Level_HI_HI := FALSE;
END_IF;

IF rVoted_LOX_Level_pct >= c_rLOX_Level_Alarm_HI THEN
    bAlarm_LOX_Level_HI := TRUE;
ELSIF rVoted_LOX_Level_pct <= (c_rLOX_Level_Alarm_HI - c_rLOX_Level_Deadband) THEN
    bAlarm_LOX_Level_HI := FALSE;
END_IF;

IF rVoted_LOX_Level_pct <= c_rLOX_Level_Alarm_LO THEN
    bAlarm_LOX_Level_LO := TRUE;
ELSIF rVoted_LOX_Level_pct >= (c_rLOX_Level_Alarm_LO + c_rLOX_Level_Deadband) THEN
    bAlarm_LOX_Level_LO := FALSE;
END_IF;

IF rVoted_LOX_Level_pct <= c_rLOX_Level_Trip_LO_LO THEN
    bAlarm_LOX_Level_LO_LO := TRUE;
    bHydrocarbonExplosionHazardTrip := TRUE;
    iFSM_State := 12;
ELSIF rVoted_LOX_Level_pct >= (c_rLOX_Level_Trip_LO_LO + c_rLOX_Level_Deadband) THEN
    bAlarm_LOX_Level_LO_LO := FALSE;
END_IF;

(* 5. Cryogenic Turbo-Expander Rotational Overspeed Trip *)
IF rVoted_Expander_RPM >= c_rExpander_Trip_HI_HI THEN
    bAlarm_Expander_Speed_HI_HI := TRUE;
    bExpanderOverspeedTrip := TRUE;
    rCmd_Expander_Nozzle_pct := 0.0;
    rCmd_Expander_BrakeBlower_pct := 100.0;
ELSIF rVoted_Expander_RPM <= (c_rExpander_Trip_HI_HI - c_rExpander_Deadband) THEN
    bAlarm_Expander_Speed_HI_HI := FALSE;
END_IF;

IF rVoted_Expander_RPM >= c_rExpander_Alarm_HI THEN
    bAlarm_Expander_Speed_HI := TRUE;
ELSIF rVoted_Expander_RPM <= (c_rExpander_Alarm_HI - c_rExpander_Deadband) THEN
    bAlarm_Expander_Speed_HI := FALSE;
END_IF;

IF rVoted_TotalHydrocarbon_ppm >= 0.80 THEN
    bAlarm_TotalHydrocarbon_HI := TRUE;
ELSIF rVoted_TotalHydrocarbon_ppm <= 0.65 THEN
    bAlarm_TotalHydrocarbon_HI := FALSE;
END_IF;

(* Pack wDiagnosticWord01: FSM State & Operation Status *)
wDiagnosticWord01 := INT_TO_WORD(iFSM_State);
IF bAutoMode THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0100; END_IF;
IF bReady THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0200; END_IF;
IF bBusy THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0400; END_IF;
IF bUnitInSteadyState THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0800; END_IF;
IF bAntiSurgeActive THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#1000; END_IF;
IF bDegradedSensorModeActive THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#2000; END_IF;
IF bEmergencyDepressActive THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#4000; END_IF;

(* Pack wDiagnosticWord02: 2oo3 TMR Sensor Health & Isolation Flags *)
wDiagnosticWord02 := 16#0000;
IF bIso_Press_MAC_A OR bIso_Press_MAC_B OR bIso_Press_MAC_C THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0001; END_IF;
IF bIso_Flow_MAC_A OR bIso_Flow_MAC_B OR bIso_Flow_MAC_C THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0002; END_IF;
IF bIso_Press_HP_A OR bIso_Press_HP_B OR bIso_Press_HP_C THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0004; END_IF;
IF bIso_Press_LP_A OR bIso_Press_LP_B OR bIso_Press_LP_C THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0008; END_IF;
IF bIso_Temp_Bath_A OR bIso_Temp_Bath_B OR bIso_Temp_Bath_C THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0010; END_IF;
IF bIso_Level_LOX_A OR bIso_Level_LOX_B OR bIso_Level_LOX_C THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0020; END_IF;
IF bIso_Acetylene_A OR bIso_Acetylene_B OR bIso_Acetylene_C THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0040; END_IF;
IF bIso_Argon_O2_A OR bIso_Argon_O2_B OR bIso_Argon_O2_C THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0080; END_IF;
IF bIso_Expander_RPM_A OR bIso_Expander_RPM_B OR bIso_Expander_RPM_C THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0100; END_IF;
IF bIso_Expander_Nozzle_A OR bIso_Expander_Nozzle_B OR bIso_Expander_Nozzle_C THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0200; END_IF;
IF bIso_Flow_GOX_A OR bIso_Flow_GOX_B OR bIso_Flow_GOX_C THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0400; END_IF;
IF bIso_Flow_GAN_A OR bIso_Flow_GAN_B OR bIso_Flow_GAN_C THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0800; END_IF;
IF bIso_Venturi_DP_A OR bIso_Venturi_DP_B OR bIso_Venturi_DP_C THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#1000; END_IF;
IF bIso_Temp_Discharge_A OR bIso_Temp_Discharge_B OR bIso_Temp_Discharge_C THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#2000; END_IF;
IF bIso_Level_HPSump_A OR bIso_Level_HPSump_B OR bIso_Level_HPSump_C THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#4000; END_IF;
IF bIso_TotalHydrocarbon_A OR bIso_TotalHydrocarbon_B OR bIso_TotalHydrocarbon_C THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#8000; END_IF;

(* Pack wDiagnosticWord03: ISA-18.2 Process Advisory Alarms *)
wDiagnosticWord03 := 16#0000;
IF bAlarm_MAC_Press_HI THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0001; END_IF;
IF bAlarm_MAC_Press_LO THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0002; END_IF;
IF bAlarm_SurgeMargin_LO THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0004; END_IF;
IF bAlarm_SurgeMargin_ROC THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0008; END_IF;
IF bAlarm_Acetylene_HI THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0010; END_IF;
IF bAlarm_LOX_Level_HI THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0020; END_IF;
IF bAlarm_LOX_Level_LO THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0040; END_IF;
IF bAlarm_Expander_Speed_HI THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0080; END_IF;
IF bAlarm_TotalHydrocarbon_HI THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0100; END_IF;
IF bAlarm_TMR_ChannelDivergent THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0200; END_IF;

(* Pack wDiagnosticWord04: ISA-18.2 Critical Redline Trips *)
wDiagnosticWord04 := 16#0000;
IF bAlarm_MAC_Press_HI_HI THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0001; END_IF;
IF bAlarm_MAC_Press_LO_LO THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0002; END_IF;
IF bAlarm_SurgeMargin_LO_LO THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0004; END_IF;
IF bAlarm_Acetylene_HI_HI THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0008; END_IF;
IF bAlarm_LOX_Level_HI_HI THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0010; END_IF;
IF bAlarm_LOX_Level_LO_LO THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0020; END_IF;
IF bAlarm_Expander_Speed_HI_HI THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0040; END_IF;
IF bCompressorSurgeTrip THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0080; END_IF;
IF bHydrocarbonExplosionHazardTrip THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0100; END_IF;
IF bExpanderOverspeedTrip THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0200; END_IF;
IF bEmergencyDepressActive THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0400; END_IF;
IF NOT bEmergencyStop_NC THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0800; END_IF;

(* ===================================================================================================================
 * PHASE 7: ACTUATOR COMMAND CLAMPING & FINAL OUTPUT DISPATCH
 * =================================================================================================================== *)
(* Clamp Final Actuator Commands to Certified Physical Envelopes *)
rCmd_MAC_AntiSurgeValve_pct := MAX(0.0, MIN(100.0, rCmd_MAC_AntiSurgeValve_pct));
rCmd_MAC_IGV_Position_pct := MAX(0.0, MIN(100.0, rCmd_MAC_IGV_Position_pct));
rCmd_Expander_Nozzle_pct := MAX(0.0, MIN(100.0, rCmd_Expander_Nozzle_pct));
rCmd_Expander_BrakeBlower_pct := MAX(0.0, MIN(100.0, rCmd_Expander_BrakeBlower_pct));
rCmd_LOX_ContinuousPurge_pct := MAX(0.5, MIN(100.0, rCmd_LOX_ContinuousPurge_pct));
rCmd_ArgonSideDrawValve_pct := MAX(0.0, MIN(100.0, rCmd_ArgonSideDrawValve_pct));
rCmd_RichLiquidAirFeedValve_pct := MAX(0.0, MIN(100.0, rCmd_RichLiquidAirFeedValve_pct));
rCmd_PureLiquidN2RefluxValve_pct := MAX(0.0, MIN(100.0, rCmd_PureLiquidN2RefluxValve_pct));
rCmd_GOX_DeliveryValve_pct := MAX(0.0, MIN(100.0, rCmd_GOX_DeliveryValve_pct));
rCmd_GAN_DeliveryValve_pct := MAX(0.0, MIN(100.0, rCmd_GAN_DeliveryValve_pct));

END_FUNCTION_BLOCK
"""

print("Phase 2-7 ready.")
