# -*- coding: utf-8 -*-
"""
Module: aseptic_retort_builder/mod_cyberphysical.py
Implements Phase 2: First-Principles Cyber-Physical Thermodynamics, Dalton Overpressure,
Bigelow/Arrhenius Microbial Lethality Kinetics (F0), Cook Value (C0), Rotary Drum Kinematics,
Cooling Water Cascade Enthalpy Balance, and Discrete 6x6 State-Space Propagation.
"""

def generate_cyberphysical():
    return '''(* =====================================================================================================================
 * PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & THERMODYNAMICS
 * Cyber-Physical Modeling Components:
 *   1. Multiphase Saturated Steam-Air Vapor Equilibrium (Magnus-Tetens Formulation)
 *   2. Dalton's Law of Partial Pressures in Free Chamber Volume & Hermetic Container Headspace
 *   3. Container Wall Net Mechanical Stress Differential DeltaP = Pcan - Pretort (Burst vs Buckling)
 *   4. Bigelow / Arrhenius Clostridium botulinum Lethality Kinetics Integral (F0, z=10.0 deg C, Tref=121.11 deg C)
 *   5. Nutritional & Texture Cook Quality Degradation Kinetics Integral (C0, z=33.1 deg C, Tref=100.0 deg C)
 *   6. Continuous Rotary Drum Agitation Kinematics, Dwell Time & Production Throughput (1,200 cans/min)
 *   7. Multi-Zone Recirculating Cooling Water Cascade Heat Transfer Enthalpy Balance
 *   8. Discrete State-Space System Propagation: x[k+1] = A*x[k] + B*u[k], y[k] = C*x[k] + D*u[k]
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SUB-SECTION 2.1: SATURATED STEAM VAPOR PRESSURE & DALTON PARTIAL AIR OVERPRESSURE
 * Magnus-Tetens Equation for Saturated Steam Vapor Pressure:
 *   Psat(T) = 0.0061121 * EXP((17.502 * T) / (240.97 + T)) * 10.0 [bar absolute]
 * Evaluated across retort chamber and internal container product cold-spot core.
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Vessel Chamber Steam Saturation Pressure from Voted RTD Temperature *)
rTempCalc1 := (17.5020 * rVoted_Temp_degC) / (240.970 + rVoted_Temp_degC);
rAntoine_Pv_sat_bar := 0.0061121 * EXP(rTempCalc1) * 10.0;

(* Boundary Clamping of Saturated Vapor Pressure *)
IF rAntoine_Pv_sat_bar < 0.0234 THEN
    rAntoine_Pv_sat_bar := 0.0234; (* 20.0 deg C minimum physical datum *)
ELSIF rAntoine_Pv_sat_bar > 4.7580 THEN
    rAntoine_Pv_sat_bar := 4.7580; (* 150.0 deg C upper mechanical threshold *)
END_IF;

(* Dalton's Law: Retort Total Chamber Pressure P_total = P_steam_sat + P_air_overpressure *)
IF rVoted_Press_bar > rAntoine_Pv_sat_bar THEN
    rDalton_Pair_bar := rVoted_Press_bar - rAntoine_Pv_sat_bar;
ELSE
    rDalton_Pair_bar := 0.0; (* Retort operating at pure saturated steam equilibrium *)
END_IF;

(* Container Cold-Spot Product Core Vapor Pressure from State-Space Estimated Core Temp *)
rTempCalc2 := (17.5020 * rX_State[2]) / (240.970 + rX_State[2]);
rAntoine_Pcan_sat_bar := 0.0061121 * EXP(rTempCalc2) * 10.0;

IF rAntoine_Pcan_sat_bar < 0.0234 THEN
    rAntoine_Pcan_sat_bar := 0.0234;
ELSIF rAntoine_Pcan_sat_bar > 4.7580 THEN
    rAntoine_Pcan_sat_bar := 4.7580;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUB-SECTION 2.2: CONTAINER HEADSPACE AIR EXPANSION & NET WALL DIFFERENTIAL STRESS
 * Hermetically sealed multi-layer pouch / rigid tinplate container mechanics:
 *   Pcan(t) = Psat(Tcore) + Pair,headspace(t)
 *   Pair,headspace(t) = P0_seam * (Tcore_K / T0_K) * (V0_headspace / V(t))
 *   DeltaP(t) = Pcan(t) - Pretort(t)
 * Safe operating envelope to prevent pouch seal bursting or can panelling: -0.12 <= DeltaP <= +0.12 bar.
 * --------------------------------------------------------------------------------------------------------------------- *)
rTempCalc3 := (rX_State[2] + rKelvinOffset) / (20.0 + rKelvinOffset);

(* Partial pressure of enclosed air assuming 0.88 bar initial seamer closing pressure *)
rDalton_Pcan_air_bar := 0.880 * rTempCalc3 * (1.0 + (0.0125 * (rX_State[2] - 20.0) / 100.0));

(* Total Theoretical Container Internal Pressure *)
rTotalEstimatedPcan_bar := rAntoine_Pcan_sat_bar + rDalton_Pcan_air_bar;

(* Container Wall Net Stress Differential: DeltaP = Pcan - Pretort *)
rContainerDeltaP_bar := rVoted_PouchPress_bar - rVoted_Press_bar;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUB-SECTION 2.3: MICROBIAL INACTIVATION LETHALITY (BIGELOW / ARRHENIUS KINETICS)
 * Clostridium botulinum Spore Thermal Inactivation Kinetics:
 *   Instantaneous Lethality Rate: L(Tcore) = 10^((Tcore - Tref) / z) [min/min]
 *   Reference Temperature: Tref = 121.11 deg C (250 deg F); Thermal Sensitivity: z = 10.0 deg C
 *   Accumulated Thermal Lethality: F0 = INTEGRAL_0^t L(Tcore(tau)) dtau [min]
 * FDA 21 CFR Part 113 Legal Mandate: Minimum Sterility Standard F0 >= 6.0 minutes.
 * --------------------------------------------------------------------------------------------------------------------- *)
IF rX_State[2] > 90.0 THEN
    rTempCalc1 := (rX_State[2] - cBigelow_Tref_degC) / cBigelow_z_degC;
    (* Numerical evaluation of 10^(x) via natural exponential: 10^x = EXP(x * ln(10)) *)
    rInstantaneousLethalityRate_L := EXP(rTempCalc1 * 2.302585092994046);
ELSE
    rInstantaneousLethalityRate_L := 0.0; (* Sub-lethal baseline below 90 deg C *)
END_IF;

(* Numerical Trapezoidal / Euler Quadrature Integration of Lethality F0 *)
IF (iFSM_CurrentState >= 3) AND (iFSM_CurrentState <= 9) THEN
    rIntegratedF0_min := rIntegratedF0_min + (rInstantaneousLethalityRate_L * (rTs_s / 60.0));
ELSIF iFSM_CurrentState = 0 THEN
    rIntegratedF0_min := 0.0;
END_IF;

IF rIntegratedF0_min >= rSet_TargetF0_min THEN
    bTargetF0Reached := TRUE;
ELSE
    bTargetF0Reached := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUB-SECTION 2.4: NUTRITIONAL & SENSORY QUALITY RETENTION COOK VALUE C0
 * Thermal Cooking Degradation Index (Thiamine, Chlorophyll, Texture):
 *   Cook Degradation Rate: Lc(Tcore) = 10^((Tcore - 100.0) / 33.1) [min/min]
 *   Cook Reference: Tref_cook = 100.0 deg C; Cook Sensitivity: z_cook = 33.1 deg C
 *   Accumulated Cook Value: C0 = INTEGRAL_0^t Lc(Tcore(tau)) dtau [min]
 * Target: Maximize F0 while minimizing C0 to preserve fresh sensory attributes and nutritional vitamins.
 * --------------------------------------------------------------------------------------------------------------------- *)
IF rX_State[2] > 60.0 THEN
    rTempCalc2 := (rX_State[2] - cCook_Tref_degC) / cCook_z_degC;
    rInstantaneousCookRate_C := EXP(rTempCalc2 * 2.302585092994046);
ELSE
    rInstantaneousCookRate_C := 0.0;
END_IF;

IF (iFSM_CurrentState >= 3) AND (iFSM_CurrentState <= 9) THEN
    rIntegratedC0_min := rIntegratedC0_min + (rInstantaneousCookRate_C * (rTs_s / 60.0));
ELSIF iFSM_CurrentState = 0 THEN
    rIntegratedC0_min := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUB-SECTION 2.5: CONTINUOUS ROTARY DRUM KINEMATICS & THROUGHPUT REGULATION
 * Continuous Retort Spiral Rotor Helical Drum Mechanics:
 *   Total Helix Turns = DrumLength / HelixPitch = 12.5 m / 0.085 m = 147.05 revolutions
 *   Container Transit Residence Dwell Time: tau_dwell = Total Turns / Rotor_RPM [min]
 *   Production Container Throughput: Throughput = Rotor_RPM * SlotsPerRev = Rotor_RPM * 48 [cans/min]
 * At nominal 25.0 RPM: Throughput = 25.0 * 48 = 1,200 cans/min; Dwell Time = 147.05 / 25 = 5.88 min.
 * --------------------------------------------------------------------------------------------------------------------- *)
IF rRotaryDrumSpeed_RPM > 0.50 THEN
    rCalculatedDwellTime_min := (cDrumLength_m / cHelixPitch_m) / rRotaryDrumSpeed_RPM;
    rEstimatedThroughput_cpm := rRotaryDrumSpeed_RPM * cSlotsPerRevolution;
ELSE
    rCalculatedDwellTime_min := 999.0; (* Drum stationary / in dwell hold *)
    rEstimatedThroughput_cpm := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUB-SECTION 2.6: MULTI-ZONE COOLING WATER CASCADE HEAT BALANCE
 * Enthalpy Extraction Rate of Recirculated Water Spray:
 *   Q_cooling = m_dot_water * Cp * (T_drain - T_supply) [kW]
 * --------------------------------------------------------------------------------------------------------------------- *)
IF rCoolingWaterFlow_m3h > 0.10 THEN
    rCoolingThermalPower_kW := (rCoolingWaterFlow_m3h * 1000.0 / 3600.0) * cWaterSpecificHeat_kJkgK * (rCoolingWaterDrainTemp_degC - rCoolingWaterSupplyTemp_degC);
    IF rCoolingThermalPower_kW < 0.0 THEN
        rCoolingThermalPower_kW := 0.0;
    END_IF;
ELSE
    rCoolingThermalPower_kW := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUB-SECTION 2.7: DISCRETE 6x6 STATE-SPACE PROPAGATION (x[k+1] = A*x[k] + B*u[k])
 * Real-time Observer State Propagation and Sensor Innovation Blending
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Blend sensor feedback innovations into current state estimation *)
rX_State[1] := (rX_State[1] * 0.70) + (rVoted_Temp_degC * 0.30);
rX_State[3] := (rX_State[3] * 0.75) + (rVoted_Press_bar * 0.25);
rX_State[4] := (rX_State[4] * 0.80) + (rVoted_PouchPress_bar * 0.20);
rX_State[5] := rIntegratedF0_min;
rX_State[6] := rIntegratedC0_min;

(* Compute x[k+1] = A * x[k] + B * u[k] *)
FOR iIdx1 := 1 TO 6 DO
    rTempSum := 0.0;
    (* A * x[k] dot product *)
    FOR iIdx2 := 1 TO 6 DO
        rTempSum := rTempSum + (rA[iIdx1, iIdx2] * rX_State[iIdx2]);
    END_FOR;
    (* B * u[k] dot product *)
    FOR iIdx3 := 1 TO 5 DO
        rTempSum := rTempSum + (rB[iIdx1, iIdx3] * rU_ControlPrev[iIdx3]);
    END_FOR;
    rX_StateNext[iIdx1] := rTempSum;
END_FOR;

(* Forward state vector propagation for next execution cycle *)
FOR iIdx1 := 1 TO 6 DO
    rX_State[iIdx1] := rX_StateNext[iIdx1];
END_FOR;

(* Re-synchronize integrator states *)
rX_State[5] := rIntegratedF0_min;
rX_State[6] := rIntegratedC0_min;

(* Output Observation Vector: y[k] = C * x[k] + D * u[k] *)
FOR iIdx1 := 1 TO 6 DO
    rTempSum := 0.0;
    FOR iIdx2 := 1 TO 6 DO
        rTempSum := rTempSum + (rC[iIdx1, iIdx2] * rX_State[iIdx2]);
    END_FOR;
    FOR iIdx3 := 1 TO 5 DO
        rTempSum := rTempSum + (rD[iIdx1, iIdx3] * rU_ControlPrev[iIdx3]);
    END_FOR;
    rY_Output[iIdx1] := rTempSum;
END_FOR;

(* Direct Physical Assignment to Block Outputs *)
rEst_ChamberTemp_degC         := rY_Output[1];
rEst_CanCoreTemp_degC         := rY_Output[2];
rEst_ChamberPress_bar         := rY_Output[3];
rEst_PouchInternalPress_bar   := rY_Output[4];
rEst_ContainerDeltaP_bar      := rY_Output[5];
rCalc_AccumulatedF0_min       := rIntegratedF0_min;
rCalc_AccumulatedC0_min       := rIntegratedC0_min;
rCalc_TransitDwellTime_min    := rCalculatedDwellTime_min;
rCalc_ContainerThroughput_cpm := rEstimatedThroughput_cpm;'''
