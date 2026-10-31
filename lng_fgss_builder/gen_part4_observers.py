# -*- coding: utf-8 -*-
"""
Generator for Phase 2: Cyber-Physical Thermodynamic Observers & Peng-Robinson EOS
"""

def generate_observers_st():
    lines = []
    lines.append("(* ==================================================================================================================== *)")
    lines.append("(* PHASE 2: CYBER-PHYSICAL THERMODYNAMIC OBSERVERS & PENG-ROBINSON REAL GAS EQUATION OF STATE                          *)")
    lines.append("(* ==================================================================================================================== *)")
    lines.append("")
    
    # 2.1 Peng-Robinson EOS for Supercritical Methane Fuel Gas
    lines.append("""(* 2.1 Peng-Robinson Equation of State: Supercritical Methane at ME-GI Supply Header (300 Bar, 45 Deg C) *)
rPR_Temp_Kelvin := rPCHE_GasOutletTemp_TT603_degC + 273.15;
IF rPR_Temp_Kelvin < 150.0 THEN
    rPR_Temp_Kelvin := 318.15; (* 45.0 deg C fallback default *)
END_IF;

rPR_Press_kPa := rVoted_MEGI_HeaderPress_bar * 100.0; (* bar to kPa *)
IF rPR_Press_kPa < 1000.0 THEN
    rPR_Press_kPa := 30000.0; (* 300.0 bar default *)
END_IF;

(* Reduced Temperature Tr and Pitzer Acentric Function m(omega) *)
rPR_Tr := rPR_Temp_Kelvin / c_rMethane_CritTemp_K;
rPR_m_factor := 0.37464 + (1.54226 * c_rMethane_AcentricFactor_omega) - (0.26992 * c_rMethane_AcentricFactor_omega * c_rMethane_AcentricFactor_omega);

(* Alpha Function: alpha = [1 + m*(1 - sqrt(Tr))]^2 *)
IF rPR_Tr > 0.01 THEN
    rPR_alpha := (1.0 + rPR_m_factor * (1.0 - SQRT(rPR_Tr))) * (1.0 + rPR_m_factor * (1.0 - SQRT(rPR_Tr)));
ELSE
    rPR_alpha := 1.0;
END_IF;

(* Dimensional EOS Attraction 'a' and Repulsion Co-Volume 'b' Parameters *)
(* a = 0.45724 * (R_u * Tc)^2 / Pc * alpha *)
rPR_a := 0.45724 * (8.31446 * c_rMethane_CritTemp_K * 8.31446 * c_rMethane_CritTemp_K) / (c_rMethane_CritPress_bar * 100.0) * rPR_alpha;
(* b = 0.07780 * (R_u * Tc) / Pc *)
rPR_b := 0.07780 * (8.31446 * c_rMethane_CritTemp_K) / (c_rMethane_CritPress_bar * 100.0);

(* Dimensionless Peng-Robinson Parameters A and B *)
rPR_A_dim := (rPR_a * rPR_Press_kPa) / (8.31446 * rPR_Temp_Kelvin * 8.31446 * rPR_Temp_Kelvin);
rPR_B_dim := (rPR_b * rPR_Press_kPa) / (8.31446 * rPR_Temp_Kelvin);

(* Newton-Raphson Iterative Solution for Compressibility Factor Z in Supercritical Dense Vapor Region *)
(* Cubic: f(Z) = Z^3 - (1 - B)*Z^2 + (A - 3*B^2 - 2*B)*Z - (A*B - B^2 - B^3) = 0 *)
rPR_Z_compressibility := 0.8850; (* Initial seed for supercritical dense gas *)
FOR iter := 1 TO 5 DO
    rPR_Z_compressibility := rPR_Z_compressibility - 
        ( (rPR_Z_compressibility * rPR_Z_compressibility * rPR_Z_compressibility)
        - ((1.0 - rPR_B_dim) * rPR_Z_compressibility * rPR_Z_compressibility)
        + ((rPR_A_dim - (3.0 * rPR_B_dim * rPR_B_dim) - (2.0 * rPR_B_dim)) * rPR_Z_compressibility)
        - ((rPR_A_dim * rPR_B_dim) - (rPR_B_dim * rPR_B_dim) - (rPR_B_dim * rPR_B_dim * rPR_B_dim)) )
        /
        LIMIT(0.10, 
            (3.0 * rPR_Z_compressibility * rPR_Z_compressibility)
            - (2.0 * (1.0 - rPR_B_dim) * rPR_Z_compressibility)
            + (rPR_A_dim - (3.0 * rPR_B_dim * rPR_B_dim) - (2.0 * rPR_B_dim)),
            50.0);
END_FOR;
rPR_Z_compressibility := LIMIT(0.35, rPR_Z_compressibility, 1.45);

(* Real Supercritical Gas Density: rho = (P * M) / (Z * R_u * T) [kg/m3] *)
rObs_MEGI_FuelGasDensity_kgm3 := (rPR_Press_kPa * c_rMethane_MolarMass_kgkmol) / 
                                  LIMIT(100.0, rPR_Z_compressibility * 8.31446 * rPR_Temp_Kelvin, 200000.0);
rObs_MEGI_FuelGasDensity_kgm3 := LIMIT(40.0, rObs_MEGI_FuelGasDensity_kgm3, 280.0);

(* 300 Bar Fuel Gas Accumulator Buffer Bottle Stored Inventory Mass [kg] *)
rObs_AccumulatorGasMass_kg := c_rAccumulatorVolume_m3 * rObs_MEGI_FuelGasDensity_kgm3;
""")

    # 2.2 Cargo Tank Boil-Off Mass Generation Observer
    lines.append("""(* 2.2 Cargo Tank Thermodynamic Boil-Off Gas (BOG) Mass Generation Observer *)
(* Natural boil-off baseline ~0.10 %/day: 4250 kg/h for 174,000 m3 vessel *)
(* Dynamic boil-off rate accounting for tank pressure rate of change and ambient seawater temperature *)
rObs_BOG_GenerationRate_kgh := 4150.0 
    + ((rVoted_CargoTankPress_mbar - 1040.0) * 18.5)
    + ((rAmbientSeaWaterTemp_degC - 20.0) * 35.0);
rObs_BOG_GenerationRate_kgh := LIMIT(1500.0, rObs_BOG_GenerationRate_kgh, 9500.0);
""")

    # 2.3 Compressor Aerodynamic & Anti-Surge Distance Observer
    lines.append("""(* 2.3 Cryogenic Centrifugal Compressor Aerodynamic Observer & Anti-Surge Margin *)
rComp_PressRatio := rComp_Stage2DischPress_PT204_bar / LIMIT(0.50, rComp_SuctionPress_PT202_bar, 5.0);
rComp_PressRatio := LIMIT(1.10, rComp_PressRatio, 8.50);

(* Polytropic Compression Head: H_p = (n / (n-1)) * Z * R * T1 * [ (P2/P1)^((n-1)/n) - 1 ] [kJ/kg] *)
rComp_PolytropicHead_calc := (c_rPolytropicExponent_n / (c_rPolytropicExponent_n - 1.0))
                           * 0.985 (* Suction compressibility *)
                           * c_rGasConstant_R_kJkgK
                           * (rVoted_CompSuctionTemp_degC + 273.15)
                           * (EXPT(rComp_PressRatio, (c_rPolytropicExponent_n - 1.0) / c_rPolytropicExponent_n) - 1.0);
rObs_Comp_PolytropicHead_kJkg := LIMIT(10.0, rComp_PolytropicHead_calc, 350.0);

(* Compressor Shaft Thermodynamic Power [kW] *)
rComp_ShaftPower_calc := (rComp_SuctionFlow_FT201_kgh / 3600.0) * rObs_Comp_PolytropicHead_kJkg / c_rPolytropicEfficiency;
rObs_Comp_ShaftPower_kW := LIMIT(20.0, rComp_ShaftPower_calc, 1850.0);

(* Surge Flow Threshold as a Function of Pressure Ratio: Q_surge = Q0 + k*(PR - 1) [kg/h] *)
rComp_SurgeFlowThreshold_kgh := 950.0 + (540.0 * (rComp_PressRatio - 1.0));
rComp_SurgeSafetyLine_kgh := rComp_SurgeFlowThreshold_kgh * 1.15; (* 15% Safety Margin Surge Control Line *)

(* Proximity to Surge Line [%]: Distance = (ActualFlow - SurgeThreshold) / SurgeThreshold * 100 *)
rComp_SurgeMargin_DeltaFlow := rComp_SuctionFlow_FT201_kgh - rComp_SurgeFlowThreshold_kgh;
rObs_Comp_SurgeMargin_pct := (rComp_SurgeMargin_DeltaFlow / LIMIT(100.0, rComp_SurgeFlowThreshold_kgh, 10000.0)) * 100.0;
rObs_Comp_SurgeMargin_pct := LIMIT(-20.0, rObs_Comp_SurgeMargin_pct, 100.0);
""")

    # 2.4 Direct-Contact Spray Recondenser Mass & Energy Balance
    lines.append("""(* 2.4 Direct-Contact Spray Recondenser Column Condensation Observer *)
(* Saturation Temperature at Recondenser Operating Pressure (approx -138.5 C at 5.5 bar abs) *)
rRecondenser_SatTemp_degC := -161.5 + (15.5 * LN(LIMIT(1.0, rRecondenser_Press_PT501_bar, 10.0)));
rRecondenser_Subcooling_DeltaT := rRecondenser_SatTemp_degC - rLNG_SprayTemp_TT504_degC;
IF rRecondenser_Subcooling_DeltaT < 2.0 THEN
    rRecondenser_Subcooling_DeltaT := 2.0;
END_IF;

(* Effective Latent Heat Absorption [kJ/kg] *)
rRecondenser_LatentHeat_eff := c_rLNG_LatentHeatVap_kJkg + (c_rLNG_LiquidCp_kJkgK * rRecondenser_Subcooling_DeltaT);

(* Real-Time Vapor Condensation Rate: m_cond = (m_spray * Cp_liq * DeltaT) / h_fg [kg/h] *)
rRecondenser_VaporCondRate_calc := (rLNG_SpraySupplyFlow_FT502_m3h * c_rLNG_LiquidDensity_kgm3)
                                  * c_rLNG_LiquidCp_kJkgK
                                  * rRecondenser_Subcooling_DeltaT
                                  / LIMIT(100.0, c_rLNG_LatentHeatVap_kJkg, 1000.0);
rObs_Recondenser_CondRate_kgh := LIMIT(0.0, rRecondenser_VaporCondRate_calc, 8500.0);

(* Eco-Friendly Methane Boil-Off Captured Rate Avoided From Atmosphere [kg/h] *)
rObs_MethaneEmissionAvoided_kgh := rObs_Recondenser_CondRate_kgh;
""")

    # 2.5 HP Cryogenic Submerged Fuel Pumps & PCHE Vaporizer Observer
    lines.append("""(* 2.5 High-Pressure Cryogenic Submerged Fuel Sendout Pump Hydraulic Observer *)
rHPPump_DeltaPress_calc := rHP_PumpDischargePress_PT602_bar - rHP_PumpSuctionPress_PT601_bar;
rObs_HPPump_DeltaPress_bar := LIMIT(0.0, rHPPump_DeltaPress_calc, 380.0);

(* Instantaneous Hydraulic Fluid Power: W_hyd = DeltaP * VolFlow [kW] *)
rHPPump_HydraulicPower_calc := (rObs_HPPump_DeltaPress_bar * 100.0) 
                              * ((rMEGI_FuelGasDemandFlow_kgh / LIMIT(100.0, c_rLNG_LiquidDensity_kgm3, 600.0)) / 3600.0);
rObs_HPPump_HydraulicPower_kW := LIMIT(0.0, rHPPump_HydraulicPower_calc, 450.0);
""")
    return "\n".join(lines)

print("Part 4 thermodynamic observers code generator written.")
