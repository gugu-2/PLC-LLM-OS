# scripts/feedmill_builder/part5_phase2_physics.py
# -*- coding: utf-8 -*-

def get_phase2_block():
    return """(* ====================================================================================================
   PHASE 2: REAL-TIME CYBER-PHYSICAL PROPERTY ESTIMATION & PROCESS OBSERVERS
   ==================================================================================================== *)

(* ----------------------------------------------------------------------------------------------------
   2.1 CULINARY STEAM MASS INJECTION & THERMAL ENTHALPY BALANCE
   ---------------------------------------------------------------------------------------------------- *)
(* Saturated steam mass flow injected through modulating globe valve u_ctrl[2] [%] *)
rSteam_mDot_Actual_kg_s := (u_ctrl[2] / 100.0) * rSteam_mDot_Max_kg_s 
                         * SQRT(MAX(0.20, rSteamHdrPress_Supply_bar) / 2.50);

(* Gravimetric incoming mash feed rate [kg/s] *)
rMash_FlowRate_kg_s := (rFeedRate_SP_tph * 1000.0) / 3600.0;

(* Net moisture uptake condensed onto dry meal [% w/w] *)
IF (rMash_FlowRate_kg_s + rSteam_mDot_Actual_kg_s) > 0.05 THEN
    rMash_MoistUptake_pct := (rSteam_mDot_Actual_kg_s / (rMash_FlowRate_kg_s + rSteam_mDot_Actual_kg_s)) * 100.0;
ELSE
    rMash_MoistUptake_pct := 0.0;
END_IF;

(* Estimated instantaneous conditioned mash moisture content [%] *)
x_state[2] := rRawMashMoist_Inlet_pct + rMash_MoistUptake_pct;

(* Measured conditioner exit mash temperature from voted TMR triplet *)
x_state[1] := rVoted_CondMashTemp_degC;

(* ----------------------------------------------------------------------------------------------------
   2.2 DYNAMIC STARCH GELATINIZATION KINETIC OBSERVER (MODIFIED ARRHENIUS DYNAMICS)
   d(alpha_gel)/dt = k0 * exp(-Ea / (R * T)) * [MAX(0, (w - w_crit)/w_ref)]^beta * (1 + gamma * N) * (1 - alpha)^n
   ---------------------------------------------------------------------------------------------------- *)
(* Thermal Arrhenius exponential term *)
rTempAccum := rGelat_Rgas * (x_state[1] + 273.15);
IF rTempAccum > 100.0 THEN
    rGelat_Rate_dAlpha_dt := rGelat_k0 * EXP(-rGelat_Ea / rTempAccum);
ELSE
    rGelat_Rate_dAlpha_dt := 0.0;
END_IF;

(* Moisture plasticization factor *)
IF x_state[2] > rGelat_Wcrit THEN
    rTempAccum := (x_state[2] - rGelat_Wcrit) / rGelat_Wref;
    (* Exponentiation approximation for beta_w = 1.45 via power expansion *)
    rGelat_Rate_dAlpha_dt := rGelat_Rate_dAlpha_dt * (rTempAccum * SQRT(MAX(0.001, rTempAccum)));
ELSE
    rGelat_Rate_dAlpha_dt := 0.0;
END_IF;

(* Paddle shaft shear rate sensitization *)
rGelat_Rate_dAlpha_dt := rGelat_Rate_dAlpha_dt * (1.0 + rGelat_GammaShear * u_ctrl[3]);

(* Unreacted starch fraction (1.0 - alpha)^1.20 *)
rTempAccum := MAX(0.0, 1.0 - rGelat_State_Alpha);
rGelat_Rate_dAlpha_dt := rGelat_Rate_dAlpha_dt * (rTempAccum * SQRT(SQRT(MAX(0.0001, rTempAccum))));

(* Discrete Euler step integration (Ts = 0.050 s) *)
rGelat_State_Alpha := rGelat_State_Alpha + rGelat_Rate_dAlpha_dt * 0.050;

(* Boundary clamping to physical range [0.0..1.0] *)
IF rGelat_State_Alpha < 0.05 THEN
    rGelat_State_Alpha := 0.05;
ELSIF rGelat_State_Alpha > 0.98 THEN
    rGelat_State_Alpha := 0.98;
END_IF;
x_state[3]               := rGelat_State_Alpha;
rEst_GelatinizationIndex := rGelat_State_Alpha;

(* Real-Time Holmen Pellet Durability Index (PDI) Prediction [%] *)
rEst_PelletDurabilityIndex_PDI := 82.5 + (16.0 * rEst_GelatinizationIndex) 
                                - (0.015 * MAX(0.0, rVoted_PressMotorCurrent_A - 550.0))
                                + (0.50 * (rPress_EffectiveGap_mm - 0.50));
IF rEst_PelletDurabilityIndex_PDI > 99.2 THEN
    rEst_PelletDurabilityIndex_PDI := 99.2;
ELSIF rEst_PelletDurabilityIndex_PDI < 75.0 THEN
    rEst_PelletDurabilityIndex_PDI := 75.0;
END_IF;

(* ----------------------------------------------------------------------------------------------------
   2.3 400 kW RING-DIE PELLET PRESS TRIBOLOGY, ROLLER TRACTION SLIP & SEC ENERGY
   ---------------------------------------------------------------------------------------------------- *)
(* Pellet mill 400 kW main motor state tracking *)
x_state[4] := rVoted_PressMotorCurrent_A;

(* Active 3-Phase Electric Power Consumption [kW] *)
rPress_ActivePower_kW := (1.73205 * rPressMotorVoltage_VT201_V * rVoted_PressMotorCurrent_A 
                         * rPressMotorCosPhi_JT202 * 0.945) / 1000.0;
rCmdMillMotor_kW      := rPress_ActivePower_kW;

(* Effective Shaft Rotational Mechanical Torque [Nm] *)
rTempAccum := 2.0 * 3.1415926 * (MAX(1.0, rDieRing_RPM_ST206_rpm) / 60.0);
rPress_MechanicalTorque_Nm := (rPress_ActivePower_kW * 1000.0) / rTempAccum;

(* Specific Mechanical Energy Consumption (SEC) [kWh/t] *)
rPress_SpecificEnergy_kWh_t := rPress_ActivePower_kW / MAX(1.0, rFeedRate_SP_tph);
rEst_SpecificEnergy_kWh_ton := rPress_SpecificEnergy_kWh_t;

(* Linear Tangential Surface Velocities [m/s] *)
rPress_DieLinearSpeed_m_s    := 3.1415926 * (rPress_DieDiameter_mm / 1000.0) * (rDieRing_RPM_ST206_rpm / 60.0);
rPress_RollerLinearSpeed_m_s := 3.1415926 * (rPress_RollerDiameter_mm / 1000.0) 
                              * ((rRoller1_RPM_ST204_rpm + rRoller2_RPM_ST205_rpm) * 0.5 / 60.0);

(* Dynamic Traction Roller Slip Ratio S_slip in [0.0..1.0] *)
IF rPress_DieLinearSpeed_m_s > 0.10 THEN
    rPress_RollerSlip_Ratio := ABS(rPress_DieLinearSpeed_m_s - rPress_RollerLinearSpeed_m_s) / rPress_DieLinearSpeed_m_s;
ELSE
    rPress_RollerSlip_Ratio := 0.0;
END_IF;
IF rPress_RollerSlip_Ratio > 1.0 THEN rPress_RollerSlip_Ratio := 1.0; END_IF;
rEst_RollerSlipRatio := rPress_RollerSlip_Ratio;

(* Ring Die Surface Pyrometer Temperature State *)
x_state[5] := rDieSurfaceTemp_TE203_degC;

(* Dynamic Ring Die Thermal Expansion Compensation [mm] *)
rPress_DieThermalExp_mm := 1.25E-5 * rPress_DieDiameter_mm * MAX(0.0, rDieSurfaceTemp_TE203_degC - 20.0);

(* Net Effective Roller Extrusion Clearance Gap [mm] *)
rPress_EffectiveGap_mm := ((rRollerGapLVDT_Left_mm + rRollerGapLVDT_Right_mm) * 0.5) - rPress_DieThermalExp_mm;
IF rPress_EffectiveGap_mm < 0.10 THEN rPress_EffectiveGap_mm := 0.10; END_IF;
x_state[6] := rPress_EffectiveGap_mm;

(* Estimated Mechanical Shear Pin Stress [MPa] *)
(* Pin radius r_pin = 0.28 m, shear area A_pin = 2.544E-4 m2 *)
rPress_ShearStress_MPa := ((rPress_MechanicalTorque_Nm / 0.280) / 2.544E-4) / 1.0E6;

(* ----------------------------------------------------------------------------------------------------
   2.4 COUNTERFLOW COOLER PSYCHROMETRICS & CHUNG-PFOST EQUILIBRIUM MOISTURE
   ---------------------------------------------------------------------------------------------------- *)
(* Bed level state from 2oo3 TMR *)
x_state[7] := rVoted_CoolerBedLevel_mm;

(* Instantaneous Pellet Bed Holdup Mass [kg] *)
rCooler_BedHoldupMass_kg := rCooler_BedArea_m2 * (x_state[7] / 1000.0) * rCooler_PelletBulkDensity;

(* Pellet Bed Residence Retention Time [minutes] *)
IF rFeedRate_SP_tph > 0.5 THEN
    rCooler_ResidenceTime_min := rCooler_BedHoldupMass_kg / (rFeedRate_SP_tph * 1000.0 / 60.0);
ELSE
    rCooler_ResidenceTime_min := 0.0;
END_IF;
rEst_CoolerRetentionTime_min := rCooler_ResidenceTime_min;

(* Chung-Pfost Equilibrium Moisture Content (EMC) Calculation [%] *)
rTempAccum := MAX(5.0, MIN(95.0, rCoolerAirInletRH_ME302_pct));
rCooler_EMC_EquilibriumMoist := (1.0 / -rCooler_EMC_ChungPfost_C1) 
                              * LN( -(rGelat_Rgas * (rCoolerAirInletTemp_TE302_degC + rCooler_EMC_ChungPfost_C2) 
                              * LN(rTempAccum / 100.0)) / rCooler_EMC_ChungPfost_C3 );

(* Clamping EMC to physical grain boundaries [9.5%..14.5%] *)
IF rCooler_EMC_EquilibriumMoist < 9.50 THEN
    rCooler_EMC_EquilibriumMoist := 9.50;
ELSIF rCooler_EMC_EquilibriumMoist > 14.50 THEN
    rCooler_EMC_EquilibriumMoist := 14.50;
END_IF;

(* Cooled Pellet Discharge Moisture Equilibrium State x8 [%] *)
IF rCooler_ResidenceTime_min > 1.0 THEN
    x_state[8] := rCooler_EMC_EquilibriumMoist 
                + (x_state[2] - rCooler_EMC_EquilibriumMoist) * EXP(-rCooler_ResidenceTime_min / 3.85);
ELSE
    x_state[8] := x_state[2];
END_IF;
rEst_PelletDischargeMoist_pct := x_state[8];

(* ----------------------------------------------------------------------------------------------------
   2.5 VACUUM COATER CHAMBER DYNAMICS & CAPILLARY PENETRATION ESTIMATOR
   ---------------------------------------------------------------------------------------------------- *)
(* Capillary Penetration Depth Factor driven by atmospheric break differential *)
IF rCoaterVesselPress_PT401_bar < -0.10 THEN
    rCoater_CapillaryPenetration := ABS(rCoaterVesselPress_PT401_bar) / 0.85;
    IF rCoater_CapillaryPenetration > 1.0 THEN rCoater_CapillaryPenetration := 1.0; END_IF;
ELSE
    rCoater_CapillaryPenetration := 0.0;
END_IF;
"""
