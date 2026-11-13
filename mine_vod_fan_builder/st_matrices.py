# mine_vod_fan_builder/st_matrices.py

def get_matrices_init():
    code = """(* ==================================================================================================== *)
(* PHASE 0: ONE-SHOT CYBER-PHYSICAL STATE-SPACE ALLOCATION & PARAMETER INITIALIZATION                   *)
(* ==================================================================================================== *)
IF NOT bStateSpaceInitialized THEN
    (* ------------------------------------------------------------------------------------------------ *)
    (* Discrete State Transition Matrix A (6x6) for Ts = 50 ms Execution Cycle                          *)
    (* x1: Fan DP [kPa], x2: Airway Mass Flow [kg/s], x3: Stall Margin [%],                              *)
    (* x4: Blade Tip Turb [Pa RMS], x5: Heading Toxic Gas [ppm], x6: Shaft Baro DP [kPa]                *)
    (* ------------------------------------------------------------------------------------------------ *)
    arrA[1, 1] := 0.942500; arrA[1, 2] := 0.003150; arrA[1, 3] := -0.001250; arrA[1, 4] := 0.000420; arrA[1, 5] := 0.000000; arrA[1, 6] := 0.015200;
    arrA[2, 1] := 0.085000; arrA[2, 2] := 0.965400; arrA[2, 3] := 0.012400; arrA[2, 4] := -0.001850; arrA[2, 5] := 0.000000; arrA[2, 6] := -0.042500;
    arrA[3, 1] := -0.038500; arrA[3, 2] := 0.045200; arrA[3, 3] := 0.912500; arrA[3, 4] := -0.085400; arrA[3, 5] := 0.000000; arrA[3, 6] := 0.008500;
    arrA[4, 1] := 0.012500; arrA[4, 2] := -0.021500; arrA[4, 3] := -0.095000; arrA[4, 4] := 0.885000; arrA[4, 5] := 0.000000; arrA[4, 6] := 0.002400;
    arrA[5, 1] := 0.000000; arrA[5, 2] := -0.052400; arrA[5, 3] := 0.000000; arrA[5, 4] := 0.000000; arrA[5, 5] := 0.985000; arrA[5, 6] := 0.000000;
    arrA[6, 1] := 0.004500; arrA[6, 2] := -0.008500; arrA[6, 3] := 0.001100; arrA[6, 4] := 0.000000; arrA[6, 5] := 0.000000; arrA[6, 6] := 0.992000;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Discrete Input Coupling Matrix B (6x6)                                                           *)
    (* u1: Blade Pitch [deg], u2: Fan VFD Speed [RPM], u3: Louver Mean [%],                             *)
    (* u4: Booster Fan [kPa], u5: Collar Thermal [kW], u6: Work-Heading Gas Generation [mg/s]           *)
    (* ------------------------------------------------------------------------------------------------ *)
    arrB[1, 1] := 0.058500; arrB[1, 2] := 0.004850; arrB[1, 3] := -0.024500; arrB[1, 4] := 0.012500; arrB[1, 5] := 0.000450; arrB[1, 6] := 0.000000;
    arrB[2, 1] := 0.082500; arrB[2, 2] := 0.018200; arrB[2, 3] := 0.095400; arrB[2, 4] := 0.038500; arrB[2, 5] := -0.001250; arrB[2, 6] := 0.000000;
    arrB[3, 1] := -0.045000; arrB[3, 2] := 0.008500; arrB[3, 3] := 0.125000; arrB[3, 4] := 0.015200; arrB[3, 5] := 0.000000; arrB[3, 6] := 0.000000;
    arrB[4, 1] := 0.035000; arrB[4, 2] := -0.004200; arrB[4, 3] := -0.075000; arrB[4, 4] := -0.008500; arrB[4, 5] := 0.000000; arrB[4, 6] := 0.000000;
    arrB[5, 1] := -0.018500; arrB[5, 2] := -0.006500; arrB[5, 3] := -0.085000; arrB[5, 4] := -0.024500; arrB[5, 5] := 0.000000; arrB[5, 6] := 0.042500;
    arrB[6, 1] := 0.002500; arrB[6, 2] := 0.000850; arrB[6, 3] := -0.012400; arrB[6, 4] := -0.004500; arrB[6, 5] := 0.003500; arrB[6, 6] := 0.000000;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Discrete Measurement Output Matrix C (6x6)                                                       *)
    (* y1: Measured Fan DP, y2: Exhaust Air Velocity, y3: Calculated Stall Margin,                      *)
    (* y4: Dynamic Blade Tip Turb, y5: Borehole Toxic Gas, y6: Shaft Hydrostatic DP                     *)
    (* ------------------------------------------------------------------------------------------------ *)
    arrC[1, 1] := 1.000000; arrC[1, 2] := 0.000000; arrC[1, 3] := 0.000000; arrC[1, 4] := 0.000000; arrC[1, 5] := 0.000000; arrC[1, 6] := 0.000000;
    arrC[2, 1] := 0.000000; arrC[2, 2] := 0.075400; arrC[2, 3] := 0.000000; arrC[2, 4] := 0.000000; arrC[2, 5] := 0.000000; arrC[2, 6] := 0.000000;
    arrC[3, 1] := 0.000000; arrC[3, 2] := 0.000000; arrC[3, 3] := 1.000000; arrC[3, 4] := 0.000000; arrC[3, 5] := 0.000000; arrC[3, 6] := 0.000000;
    arrC[4, 1] := 0.000000; arrC[4, 2] := 0.000000; arrC[4, 3] := 0.000000; arrC[4, 4] := 1.000000; arrC[4, 5] := 0.000000; arrC[4, 6] := 0.000000;
    arrC[5, 1] := 0.000000; arrC[5, 2] := 0.000000; arrC[5, 3] := 0.000000; arrC[5, 4] := 0.000000; arrC[5, 5] := 1.000000; arrC[5, 6] := 0.000000;
    arrC[6, 1] := 0.000000; arrC[6, 2] := 0.000000; arrC[6, 3] := 0.000000; arrC[6, 4] := 0.000000; arrC[6, 5] := 0.000000; arrC[6, 6] := 1.000000;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Discrete Direct Feedthrough Matrix D (6x6) - Strictly Zero Direct Feedthrough                    *)
    (* ------------------------------------------------------------------------------------------------ *)
    arrD[1, 1] := 0.0; arrD[1, 2] := 0.0; arrD[1, 3] := 0.0; arrD[1, 4] := 0.0; arrD[1, 5] := 0.0; arrD[1, 6] := 0.0;
    arrD[2, 1] := 0.0; arrD[2, 2] := 0.0; arrD[2, 3] := 0.0; arrD[2, 4] := 0.0; arrD[2, 5] := 0.0; arrD[2, 6] := 0.0;
    arrD[3, 1] := 0.0; arrD[3, 2] := 0.0; arrD[3, 3] := 0.0; arrD[3, 4] := 0.0; arrD[3, 5] := 0.0; arrD[3, 6] := 0.0;
    arrD[4, 1] := 0.0; arrD[4, 2] := 0.0; arrD[4, 3] := 0.0; arrD[4, 4] := 0.0; arrD[4, 5] := 0.0; arrD[4, 6] := 0.0;
    arrD[5, 1] := 0.0; arrD[5, 2] := 0.0; arrD[5, 3] := 0.0; arrD[5, 4] := 0.0; arrD[5, 5] := 0.0; arrD[5, 6] := 0.0;
    arrD[6, 1] := 0.0; arrD[6, 2] := 0.0; arrD[6, 3] := 0.0; arrD[6, 4] := 0.0; arrD[6, 5] := 0.0; arrD[6, 6] := 0.0;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Luenberger State Observer Innovation Feedback Gain Matrix L (6x6)                                *)
    (* Designed via pole placement for deadbeat / fast error decay (spectral radius < 0.45)             *)
    (* ------------------------------------------------------------------------------------------------ *)
    arrL[1, 1] := 0.285000; arrL[1, 2] := 0.012500; arrL[1, 3] := -0.004200; arrL[1, 4] := 0.001850; arrL[1, 5] := 0.000000; arrL[1, 6] := 0.045000;
    arrL[2, 1] := 0.045000; arrL[2, 2] := 0.315000; arrL[2, 3] := 0.018500; arrL[2, 4] := -0.005400; arrL[2, 5] := 0.000000; arrL[2, 6] := -0.012400;
    arrL[3, 1] := -0.024500; arrL[3, 2] := 0.038500; arrL[3, 3] := 0.385000; arrL[3, 4] := -0.042500; arrL[3, 5] := 0.000000; arrL[3, 6] := 0.004500;
    arrL[4, 1] := 0.008500; arrL[4, 2] := -0.014500; arrL[4, 3] := -0.045000; arrL[4, 4] := 0.412000; arrL[4, 5] := 0.000000; arrL[4, 6] := 0.001200;
    arrL[5, 1] := 0.000000; arrL[5, 2] := -0.028500; arrL[5, 3] := 0.000000; arrL[5, 4] := 0.000000; arrL[5, 5] := 0.345000; arrL[5, 6] := 0.000000;
    arrL[6, 1] := 0.012500; arrL[6, 2] := -0.004500; arrL[6, 3] := 0.002500; arrL[6, 4] := 0.000000; arrL[6, 5] := 0.000000; arrL[6, 6] := 0.295000;

    (* ------------------------------------------------------------------------------------------------ *)
    (* MPC Quadratic Penalty Weights (State Q, Actuator Energy R, Slew S, Terminal P)                   *)
    (* ------------------------------------------------------------------------------------------------ *)
    arrQ_weights[1] := 45.0;  (* x1: Fan DP tracking penalty *)
    arrQ_weights[2] := 65.0;  (* x2: Total Airway Mass Flow regulatory compliance penalty *)
    arrQ_weights[3] := 185.0; (* x3: Stall margin safety barrier base penalty *)
    arrQ_weights[4] := 75.0;  (* x4: Blade tip dynamic turbulence penalty *)
    arrQ_weights[5] := 120.0; (* x5: Heading toxic gas clearance penalty *)
    arrQ_weights[6] := 35.0;  (* x6: Subterranean differential barometric pressure penalty *)

    arrR_weights[1] := 18.0; (* u1: Blade pitch servo actuator energy penalty *)
    arrR_weights[2] := 28.0; (* u2: 3.5 MW Fan VFD electrical power penalty *)
    arrR_weights[3] := 12.0; (* u3: Underground branch louver damper modulation penalty *)
    arrR_weights[4] := 15.0; (* u4: Auxiliary booster fan power consumption penalty *)
    arrR_weights[5] := 8.5;  (* u5: Surface intake collar heating thermal duty penalty *)
    arrR_weights[6] := 5.0;  (* u6: Work-heading production intensity penalty *)

    arrS_weights[1] := 45.0; (* u1: Blade pitch mechanical slew rate penalty *)
    arrS_weights[2] := 85.0; (* u2: 3.5 MW motor torque acceleration slew penalty *)
    arrS_weights[3] := 25.0; (* u3: Branch louver gear motor movement slew penalty *)
    arrS_weights[4] := 30.0; (* u4: Auxiliary booster fan acceleration slew penalty *)
    arrS_weights[5] := 10.0; (* u5: Thermal coil modulating valve slew penalty *)
    arrS_weights[6] := 2.0;  (* u6: Production activity change rate penalty *)

    arrP_weights[1] := 95.0;  (* Terminal cost state x1 *)
    arrP_weights[2] := 135.0; (* Terminal cost state x2 *)
    arrP_weights[3] := 420.0; (* Terminal cost state x3 (Stall safety terminal dominance) *)
    arrP_weights[4] := 160.0; (* Terminal cost state x4 *)
    arrP_weights[5] := 260.0; (* Terminal cost state x5 *)
    arrP_weights[6] := 70.0;  (* Terminal cost state x6 *)

    (* Actuator Physical Saturation and Slew Constraints *)
    arrU_min[1] := -12.0; arrU_max[1] := 38.0; arrDeltaU_max[1] := 0.125; (* Pitch: -12 to +38 deg, 2.5 deg/s *)
    arrU_min[2] := 350.0; arrU_max[2] := 1050.0; arrDeltaU_max[2] := 4.5; (* VFD Speed: 350 to 1050 RPM, 90 RPM/s *)
    arrU_min[3] := 5.0; arrU_max[3] := 100.0; arrDeltaU_max[3] := 0.25; (* Louvers: 5% to 100%, 5 %/s *)
    arrU_min[4] := 0.0; arrU_max[4] := 1.8; arrDeltaU_max[4] := 0.045; (* Boosters: 0 to 1.8 kPa, 0.9 kPa/s *)
    arrU_min[5] := 0.0; arrU_max[5] := 100.0; arrDeltaU_max[5] := 0.50; (* Heating Valve: 0 to 100%, 10 %/s *)
    arrU_min[6] := 0.0; arrU_max[6] := 1000.0; arrDeltaU_max[6] := 50.0; (* Emission source rate: 0..1000 mg/s *)

    (* Engineering Unit Scaling and Offsets for State Vector *)
    arrX_scale[1] := 1.0; arrX_bias[1] := 0.0; (* Fan DP [kPa] *)
    arrX_scale[2] := 1.0; arrX_bias[2] := 0.0; (* Airway Mass Flow [kg/s] *)
    arrX_scale[3] := 1.0; arrX_bias[3] := 0.0; (* Stall Margin [%] *)
    arrX_scale[4] := 1.0; arrX_bias[4] := 0.0; (* Blade Tip Turbulence [Pa RMS] *)
    arrX_scale[5] := 1.0; arrX_bias[5] := 0.0; (* Heading Toxic Gas [ppm] *)
    arrX_scale[6] := 1.0; arrX_bias[6] := 0.0; (* Shaft Barometric DP [kPa] *)

    (* Initial Observer State Vector Seed *)
    arrX_hat[1] := 3.5;
    arrX_hat[2] := 285.0;
    arrX_hat[3] := 32.5;
    arrX_hat[4] := 45.0;
    arrX_hat[5] := 12.0;
    arrX_hat[6] := 30.0;

    (* ------------------------------------------------------------------------------------------------ *)
    (* 24 Underground Automated Branch Louvers Physical Parameter Map                                   *)
    (* Levels 400 m to 2,400 m, Crosscuts, Ramps, Extraction Stopes, and Refuge Chambers                *)
    (* ------------------------------------------------------------------------------------------------ *)
    arrBranchResistance_Base[1] := 0.0245; arrBranchCrossSection_m2[1] := 22.5; arrBranchRegulatoryFlowMin_m3s[1] := 18.0; (* L01 - 400m Level Shaft Station *)
    arrBranchResistance_Base[2] := 0.0312; arrBranchCrossSection_m2[2] := 20.0; arrBranchRegulatoryFlowMin_m3s[2] := 15.0; (* L02 - 600m Exploration Drift *)
    arrBranchResistance_Base[3] := 0.0185; arrBranchCrossSection_m2[3] := 26.0; arrBranchRegulatoryFlowMin_m3s[3] := 22.0; (* L03 - 800m Main Haulage Ramp North *)
    arrBranchResistance_Base[4] := 0.0195; arrBranchCrossSection_m2[4] := 26.0; arrBranchRegulatoryFlowMin_m3s[4] := 22.0; (* L04 - 800m Main Haulage Ramp South *)
    arrBranchResistance_Base[5] := 0.0425; arrBranchCrossSection_m2[5] := 18.5; arrBranchRegulatoryFlowMin_m3s[5] := 14.0; (* L05 - 1000m Primary Crusher Station *)
    arrBranchResistance_Base[6] := 0.0380; arrBranchCrossSection_m2[6] := 19.0; arrBranchRegulatoryFlowMin_m3s[6] := 12.0; (* L06 - 1000m Ore Pass Dumping Point *)
    arrBranchResistance_Base[7] := 0.0275; arrBranchCrossSection_m2[7] := 24.0; arrBranchRegulatoryFlowMin_m3s[7] := 20.0; (* L07 - 1200m Sub-level Caving Stope 1 *)
    arrBranchResistance_Base[8] := 0.0290; arrBranchCrossSection_m2[8] := 24.0; arrBranchRegulatoryFlowMin_m3s[8] := 20.0; (* L08 - 1200m Sub-level Caving Stope 2 *)
    arrBranchResistance_Base[9] := 0.0345; arrBranchCrossSection_m2[9] := 21.0; arrBranchRegulatoryFlowMin_m3s[9] := 16.0; (* L09 - 1400m Drill Jumbo Heading West *)
    arrBranchResistance_Base[10] := 0.0360; arrBranchCrossSection_m2[10] := 21.0; arrBranchRegulatoryFlowMin_m3s[10] := 16.0; (* L10 - 1400m Drill Jumbo Heading East *)
    arrBranchResistance_Base[11] := 0.0520; arrBranchCrossSection_m2[11] := 16.0; arrBranchRegulatoryFlowMin_m3s[11] := 8.0;  (* L11 - 1500m Explosives Magazine Safe *)
    arrBranchResistance_Base[12] := 0.0650; arrBranchCrossSection_m2[12] := 14.5; arrBranchRegulatoryFlowMin_m3s[12] := 6.0;  (* L12 - 1600m Permanent Refuge Chamber A *)
    arrBranchResistance_Base[13] := 0.0220; arrBranchCrossSection_m2[13] := 25.0; arrBranchRegulatoryFlowMin_m3s[13] := 24.0; (* L13 - 1700m Heavy LHD Haulage Level *)
    arrBranchResistance_Base[14] := 0.0235; arrBranchCrossSection_m2[14] := 25.0; arrBranchRegulatoryFlowMin_m3s[14] := 24.0; (* L14 - 1700m Electric Truck Loop *)
    arrBranchResistance_Base[15] := 0.0410; arrBranchCrossSection_m2[15] := 18.0; arrBranchRegulatoryFlowMin_m3s[15] := 15.0; (* L15 - 1800m Workshop & Maintenance Bay *)
    arrBranchResistance_Base[16] := 0.0385; arrBranchCrossSection_m2[16] := 19.5; arrBranchRegulatoryFlowMin_m3s[16] := 14.0; (* L16 - 1900m Electrical Substation Drift *)
    arrBranchResistance_Base[17] := 0.0265; arrBranchCrossSection_m2[17] := 23.5; arrBranchRegulatoryFlowMin_m3s[17] := 22.0; (* L17 - 2000m Deep Stope Extraction Alpha *)
    arrBranchResistance_Base[18] := 0.0280; arrBranchCrossSection_m2[18] := 23.5; arrBranchRegulatoryFlowMin_m3s[18] := 22.0; (* L18 - 2000m Deep Stope Extraction Beta *)
    arrBranchResistance_Base[19] := 0.0325; arrBranchCrossSection_m2[19] := 21.5; arrBranchRegulatoryFlowMin_m3s[19] := 18.0; (* L19 - 2100m Ramp Decline Development *)
    arrBranchResistance_Base[20] := 0.0350; arrBranchCrossSection_m2[20] := 21.0; arrBranchRegulatoryFlowMin_m3s[20] := 18.0; (* L20 - 2200m Deep Borehole Drainage Sump *)
    arrBranchResistance_Base[21] := 0.0680; arrBranchCrossSection_m2[21] := 14.0; arrBranchRegulatoryFlowMin_m3s[21] := 6.0;  (* L21 - 2200m Permanent Refuge Chamber B *)
    arrBranchResistance_Base[22] := 0.0295; arrBranchCrossSection_m2[22] := 22.0; arrBranchRegulatoryFlowMin_m3s[22] := 20.0; (* L22 - 2300m Ore Body Delineation Drift *)
    arrBranchResistance_Base[23] := 0.0330; arrBranchCrossSection_m2[23] := 20.5; arrBranchRegulatoryFlowMin_m3s[23] := 19.0; (* L23 - 2400m Bottom Shaft Station Sump *)
    arrBranchResistance_Base[24] := 0.0365; arrBranchCrossSection_m2[24] := 20.0; arrBranchRegulatoryFlowMin_m3s[24] := 18.0; (* L24 - 2400m Deep Horizon Active Blast Heading *)

    bStateSpaceInitialized := TRUE;
END_IF;
"""
    return code
