# -*- coding: utf-8 -*-
"""
Generator for Phase 3: Discrete State-Space Propagation
"""

def generate_statespace_st():
    lines = []
    lines.append("(* ==================================================================================================================== *)")
    lines.append("(* PHASE 3: DISCRETE STATE-SPACE MODEL PROPAGATION (x[k+1] = A*x[k] + B*u[k], y = C*x[k] + D*u[k])                    *)")
    lines.append("(* ==================================================================================================================== *)")
    lines.append("")
    
    lines.append("""(* 3.1 Mapping Real-Time Validated Telemetry & Observers into State Vector x[1..16] *)
x[1]  := rVoted_CargoTankPress_mbar - 1040.0;                    (* Cargo Tank 1 Vapor Pressure Deviation [mbar] *)
x[2]  := (rComp_SuctionPress_PT202_bar * 1000.0) - 1035.0;      (* Compressor Suction Manifold Pressure Deviation [mbar] *)
x[3]  := rObs_BOG_GenerationRate_kgh - 4150.0;                   (* Natural + Forced Boil-Off Mass Rate Deviation [kg/h] *)
x[4]  := rVoted_CompSuctionTemp_degC - (-140.0);                 (* Compressor Suction Temperature Deviation [deg C] *)
x[5]  := rComp_Stage1DischPress_PT203_bar - 2.85;                (* Compressor Stage 1 Intermediate Pressure Deviation [bar] *)
x[6]  := rComp_SuctionFlow_FT201_kgh - 3800.0;                   (* Compressor Mass Throughput Delivery Deviation [kg/h] *)
x[7]  := rCmd_Comp_AntiSurgeValve_pct * 12.5;                    (* Anti-Surge Recycle Mass Flow Deviation [kg/h] *)
x[8]  := (20.0 - rObs_Comp_SurgeMargin_pct) * 0.05;              (* Compressor Surge Line Proximity Deviation Index [dim] *)
x[9]  := rRecondenser_Press_PT501_bar - 5.50;                    (* Recondenser Column Pressure Deviation [bar] *)
x[10] := rRecondenser_Level_LT501_pct - 50.0;                    (* Recondenser Sump Cryogenic Condensate Level Deviation [%] *)
x[11] := (rLNG_SpraySupplyFlow_FT502_m3h * 445.0) - 1500.0;      (* Subcooled LNG Spray Inflow Mass Deviation [kg/h] *)
x[12] := rHP_PumpDischargePress_PT602_bar - 315.0;               (* HP Submerged Fuel Pump Discharge Pressure Deviation [bar] *)
x[13] := rPCHE_GasOutletTemp_TT603_degC - 45.0;                  (* PCHE Supercritical Delivery Temperature Deviation [deg C] *)
x[14] := rVoted_MEGI_HeaderPress_bar - 300.0;                    (* ME-GI 300 Bar Fuel Header Pressure Deviation [bar] *)
x[15] := rObs_AccumulatorGasMass_kg - 480.0;                     (* Buffer Bottle Stored Gas Inventory Deviation [kg] *)
x[16] := rCmd_GCU_PeakingVentValve_pct * 45.0;                   (* Gas Combustion Unit Thermal Energy Influx [kW] *)

(* Load Previous Scan Manipulated Vector into u[1..8] *)
u[1] := u_prev[1]; (* IGV Angle [%] *)
u[2] := u_prev[2]; (* Anti-Surge Valve [%] *)
u[3] := u_prev[3]; (* Subcooled Spray Valve [%] *)
u[4] := u_prev[4]; (* HP Pump VFD Speed [%] *)
u[5] := u_prev[5]; (* ME-GI Master PCV [%] *)
u[6] := u_prev[6]; (* PCHE Glycol Valve [%] *)
u[7] := u_prev[7]; (* GCU Peaking Vent [%] *)
u[8] := u_prev[8]; (* Tank Suction Throttle [%] *)

(* 3.2 Discrete State Propagation: x_{next} = A * x + B * u *)
FOR i := 1 TO 16 DO
    rSumAx := 0.0;
    FOR j := 1 TO 16 DO
        rSumAx := rSumAx + (A[i, j] * x[j]);
    END_FOR;
    
    rSumBu := 0.0;
    FOR k := 1 TO 8 DO
        rSumBu := rSumBu + (B[i, k] * u[k]);
    END_FOR;
    
    x_next[i] := rSumAx + rSumBu;
END_FOR;

(* 3.3 Predicted Process Output Vector: y = C * x + D * u *)
FOR m := 1 TO 8 DO
    rSumCx := 0.0;
    FOR j := 1 TO 16 DO
        rSumCx := rSumCx + (C[m, j] * x[j]);
    END_FOR;
    
    rSumDu := 0.0;
    FOR k := 1 TO 8 DO
        rSumDu := rSumDu + (D[m, k] * u[k]);
    END_FOR;
    
    y[m] := rSumCx + rSumDu;
END_FOR;
""")
    return "\n".join(lines)

print("Part 5 state-space propagation generator written.")
