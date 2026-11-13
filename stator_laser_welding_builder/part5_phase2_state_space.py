# stator_laser_welding_builder/part5_phase2_state_space.py

def get_phase2_state_space():
    return """(*
====================================================================================================
PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION (Ts = 2.0 [ms])
State Propagation: x_pred[k+1] = A * x[k] + B * u[k] + Ew * w[k]
Output Estimation: y_est[k]    = C * x_pred[k] + D * u[k]
Observer Update:   x_est[k+1]  = x_pred[k+1] + Ke * (y_meas[k] - y_est[k])
====================================================================================================
*)

(* -------------------------------------------------------------------------------------------------
   STEP 2.1: NON-LINEAR THERMOPHYSICAL CALCULATIONS & ABSORPTIVITY DYNAMICS
   ------------------------------------------------------------------------------------------------- *)
(* 2.1.1: Dynamic Optical Absorptivity as a function of Copper Temperature & Keyhole Trapping *)
IF arrX_State[1] < rCu_MeltingPoint_degC THEN
    (* Solid State: Fresnel reflectivity dominates at 1070 nm fiber laser wavelength *)
    rDynamicCopperAbsorptivity := (1.0 - rCu_SolidReflectivity) + (0.000085 * MAX(0.0, arrX_State[1] - 25.0));
ELSE
    (* Liquid / Vapor Keyhole State: Multi-reflection photon trapping inside capillary *)
    rTemp_Scalar1 := MIN(1.0, MAX(0.0, (arrX_State[1] - rCu_MeltingPoint_degC) / (rCu_VaporizationPoint_degC - rCu_MeltingPoint_degC)));
    rDynamicCopperAbsorptivity := (1.0 - rCu_LiquidReflectivity) + (0.280 * rTemp_Scalar1) + (0.185 * MIN(1.0, arrX_State[4] / 2.50));
END_IF;

(* 2.1.2: Thermocapillary Marangoni Convection Velocity at Melt Pool Boundary *)
(* dGamma/dT of Molten Copper = -0.32 x 10^-3 [N/(m-K)], Dynamic Viscosity mu = 4.0 x 10^-3 [Pa-s] *)
IF arrX_State[1] > rCu_MeltingPoint_degC THEN
    rMarangoniFlowVelocity_m_s := (0.320 / 4.0) * (arrX_State[1] - arrX_State[2]) * 0.001;
    rMarangoniFlowVelocity_m_s := MIN(4.50, MAX(0.0, rMarangoniFlowVelocity_m_s));
ELSE
    rMarangoniFlowVelocity_m_s := 0.0;
END_IF;

(* 2.1.3: Vapor Plume Recoil Pressure Balance Inside Keyhole *)
IF arrX_State[1] > 1850.0 THEN
    (* Clausius-Clapeyron Vapor Recoil Approximation *)
    rTemp_Scalar2 := (arrX_State[1] - 1850.0) / 712.0;
    rKeyholeRecoilPressure_bar := 0.54 * EXP(MIN(4.50, 2.85 * rTemp_Scalar2));
ELSE
    rKeyholeRecoilPressure_bar := 0.0;
END_IF;

(* 2.1.4: Real-Time Pyrometer Cooling Velocity dT/dt *)
rCoolingRate_dTdt_degC_s := (rMeltPool_Voted_degC - rPreviousMeltPoolTemp_degC) / rScanTime_s;
rPreviousMeltPoolTemp_degC := rMeltPool_Voted_degC;

(* 2.1.5: Stator Winding Slot Liner Aramid Paper (Nomex/PAI) Thermal Accumulation *)
(* Heat conduction down 42 mm copper hairpin shank to slot insulation opening *)
rTemp_Scalar1 := (arrX_State[3] - rSlotLiner_ThermalAccum_degC) * 0.0035;
rSlotLiner_ThermalAccum_degC := rSlotLiner_ThermalAccum_degC + (rTemp_Scalar1 * rScanTime_s) - ((rSlotLiner_ThermalAccum_degC - 25.0) * 0.00085 * rScanTime_s);
rEst_ThermalInsulMargin_degC := rTrip_InsulationTemp_HH_degC - rSlotLiner_ThermalAccum_degC;

(* -------------------------------------------------------------------------------------------------
   STEP 2.2: ASSEMBLE INPUT & DISTURBANCE VECTORS
   ------------------------------------------------------------------------------------------------- *)
(* Control Inputs: u = [P_laser, f_wobble, tau_chuck, Q_gas] *)
arrU_Control[1] := rLaserPower_Cmd_kW;
arrU_Control[2] := rLaserWobble_Freq_Cmd_Hz;
arrU_Control[3] := rChuck_ActualTorque_Nm;
arrU_Control[4] := rShieldGas_Flow_Cmd_Lmin;

(* Physical Disturbances: w = [delta_gap, delta_height, delta_reflectivity] *)
arrW_Disturbance[1] := rGap_Voted_mm;
arrW_Disturbance[2] := rHeight_Voted_mm;
arrW_Disturbance[3] := (1.0 - rDynamicCopperAbsorptivity) - rCu_SolidReflectivity;

(* Sensor Measurements: y_meas = [T_pyro, P_mon, Q_gas, theta_pos, omega_spd, P_hyd] *)
arrY_Measurement[1] := rMeltPool_Voted_degC;
arrY_Measurement[2] := rLaserPwr_Voted_kW;
arrY_Measurement[3] := rShieldGas_Voted_Lmin;
arrY_Measurement[4] := rChuck_ActualPosition_deg;
arrY_Measurement[5] := rChuck_ActualVelocity_deg_s;
arrY_Measurement[6] := rHydClamp_Voted_bar;

(* -------------------------------------------------------------------------------------------------
   STEP 2.3: UNROLLED STATE PREDICTION (x_pred = A * x + B * u + Ew * w)
   ------------------------------------------------------------------------------------------------- *)
(* State 1: Molten Copper Weld Pool Core Temperature T_pool [deg C] *)
arrX_Predicted[1] := (arrA_Matrix[1, 1] * arrX_State[1]) +
                     (arrA_Matrix[1, 2] * arrX_State[2]) +
                     (arrA_Matrix[1, 3] * arrX_State[3]) +
                     (arrA_Matrix[1, 4] * arrX_State[4]) +
                     (arrA_Matrix[1, 5] * arrX_State[5]) +
                     (arrA_Matrix[1, 6] * arrX_State[6]) +
                     (arrA_Matrix[1, 7] * arrX_State[7]) +
                     (arrA_Matrix[1, 8] * arrX_State[8]) +
                     (arrB_Matrix[1, 1] * arrU_Control[1]) +
                     (arrB_Matrix[1, 2] * arrU_Control[2]) +
                     (arrB_Matrix[1, 3] * arrU_Control[3]) +
                     (arrB_Matrix[1, 4] * arrU_Control[4]) +
                     (arrEw_Matrix[1, 1] * arrW_Disturbance[1]) +
                     (arrEw_Matrix[1, 2] * arrW_Disturbance[2]) +
                     (arrEw_Matrix[1, 3] * arrW_Disturbance[3]);

(* State 2: Copper Heat-Affected Zone (HAZ) Temperature T_haz [deg C] *)
arrX_Predicted[2] := (arrA_Matrix[2, 1] * arrX_State[1]) +
                     (arrA_Matrix[2, 2] * arrX_State[2]) +
                     (arrA_Matrix[2, 3] * arrX_State[3]) +
                     (arrA_Matrix[2, 4] * arrX_State[4]) +
                     (arrA_Matrix[2, 5] * arrX_State[5]) +
                     (arrA_Matrix[2, 6] * arrX_State[6]) +
                     (arrA_Matrix[2, 7] * arrX_State[7]) +
                     (arrA_Matrix[2, 8] * arrX_State[8]) +
                     (arrB_Matrix[2, 1] * arrU_Control[1]) +
                     (arrB_Matrix[2, 2] * arrU_Control[2]) +
                     (arrB_Matrix[2, 3] * arrU_Control[3]) +
                     (arrB_Matrix[2, 4] * arrU_Control[4]) +
                     (arrEw_Matrix[2, 1] * arrW_Disturbance[1]) +
                     (arrEw_Matrix[2, 2] * arrW_Disturbance[2]) +
                     (arrEw_Matrix[2, 3] * arrW_Disturbance[3]);

(* State 3: Copper Hairpin Pin-Tip Bulk Temperature T_pin [deg C] *)
arrX_Predicted[3] := (arrA_Matrix[3, 1] * arrX_State[1]) +
                     (arrA_Matrix[3, 2] * arrX_State[2]) +
                     (arrA_Matrix[3, 3] * arrX_State[3]) +
                     (arrA_Matrix[3, 4] * arrX_State[4]) +
                     (arrA_Matrix[3, 5] * arrX_State[5]) +
                     (arrA_Matrix[3, 6] * arrX_State[6]) +
                     (arrA_Matrix[3, 7] * arrX_State[7]) +
                     (arrA_Matrix[3, 8] * arrX_State[8]) +
                     (arrB_Matrix[3, 1] * arrU_Control[1]) +
                     (arrB_Matrix[3, 2] * arrU_Control[2]) +
                     (arrB_Matrix[3, 3] * arrU_Control[3]) +
                     (arrB_Matrix[3, 4] * arrU_Control[4]) +
                     (arrEw_Matrix[3, 1] * arrW_Disturbance[1]) +
                     (arrEw_Matrix[3, 2] * arrW_Disturbance[2]) +
                     (arrEw_Matrix[3, 3] * arrW_Disturbance[3]);

(* State 4: Keyhole Vapor Capillary Depth h_keyhole [mm] *)
arrX_Predicted[4] := (arrA_Matrix[4, 1] * arrX_State[1]) +
                     (arrA_Matrix[4, 2] * arrX_State[2]) +
                     (arrA_Matrix[4, 3] * arrX_State[3]) +
                     (arrA_Matrix[4, 4] * arrX_State[4]) +
                     (arrA_Matrix[4, 5] * arrX_State[5]) +
                     (arrA_Matrix[4, 6] * arrX_State[6]) +
                     (arrA_Matrix[4, 7] * arrX_State[7]) +
                     (arrA_Matrix[4, 8] * arrX_State[8]) +
                     (arrB_Matrix[4, 1] * arrU_Control[1]) +
                     (arrB_Matrix[4, 2] * arrU_Control[2]) +
                     (arrB_Matrix[4, 3] * arrU_Control[3]) +
                     (arrB_Matrix[4, 4] * arrU_Control[4]) +
                     (arrEw_Matrix[4, 1] * arrW_Disturbance[1]) +
                     (arrEw_Matrix[4, 2] * arrW_Disturbance[2]) +
                     (arrEw_Matrix[4, 3] * arrW_Disturbance[3]);

(* State 5: Weld Nugget Molten Pool Volume V_nugget [mm3] *)
arrX_Predicted[5] := (arrA_Matrix[5, 1] * arrX_State[1]) +
                     (arrA_Matrix[5, 2] * arrX_State[2]) +
                     (arrA_Matrix[5, 3] * arrX_State[3]) +
                     (arrA_Matrix[5, 4] * arrX_State[4]) +
                     (arrA_Matrix[5, 5] * arrX_State[5]) +
                     (arrA_Matrix[5, 6] * arrX_State[6]) +
                     (arrA_Matrix[5, 7] * arrX_State[7]) +
                     (arrA_Matrix[5, 8] * arrX_State[8]) +
                     (arrB_Matrix[5, 1] * arrU_Control[1]) +
                     (arrB_Matrix[5, 2] * arrU_Control[2]) +
                     (arrB_Matrix[5, 3] * arrU_Control[3]) +
                     (arrB_Matrix[5, 4] * arrU_Control[4]) +
                     (arrEw_Matrix[5, 1] * arrW_Disturbance[1]) +
                     (arrEw_Matrix[5, 2] * arrW_Disturbance[2]) +
                     (arrEw_Matrix[5, 3] * arrW_Disturbance[3]);

(* State 6: Rotary Chuck Angular Position Error Delta_theta [mrad] *)
arrX_Predicted[6] := (arrA_Matrix[6, 1] * arrX_State[1]) +
                     (arrA_Matrix[6, 2] * arrX_State[2]) +
                     (arrA_Matrix[6, 3] * arrX_State[3]) +
                     (arrA_Matrix[6, 4] * arrX_State[4]) +
                     (arrA_Matrix[6, 5] * arrX_State[5]) +
                     (arrA_Matrix[6, 6] * arrX_State[6]) +
                     (arrA_Matrix[6, 7] * arrX_State[7]) +
                     (arrA_Matrix[6, 8] * arrX_State[8]) +
                     (arrB_Matrix[6, 1] * arrU_Control[1]) +
                     (arrB_Matrix[6, 2] * arrU_Control[2]) +
                     (arrB_Matrix[6, 3] * arrU_Control[3]) +
                     (arrB_Matrix[6, 4] * arrU_Control[4]) +
                     (arrEw_Matrix[6, 1] * arrW_Disturbance[1]) +
                     (arrEw_Matrix[6, 2] * arrW_Disturbance[2]) +
                     (arrEw_Matrix[6, 3] * arrW_Disturbance[3]);

(* State 7: Direct-Drive Motor Speed omega_chuck [rad/s] *)
arrX_Predicted[7] := (arrA_Matrix[7, 1] * arrX_State[1]) +
                     (arrA_Matrix[7, 2] * arrX_State[2]) +
                     (arrA_Matrix[7, 3] * arrX_State[3]) +
                     (arrA_Matrix[7, 4] * arrX_State[4]) +
                     (arrA_Matrix[7, 5] * arrX_State[5]) +
                     (arrA_Matrix[7, 6] * arrX_State[6]) +
                     (arrA_Matrix[7, 7] * arrX_State[7]) +
                     (arrA_Matrix[7, 8] * arrX_State[8]) +
                     (arrB_Matrix[7, 1] * arrU_Control[1]) +
                     (arrB_Matrix[7, 2] * arrU_Control[2]) +
                     (arrB_Matrix[7, 3] * arrU_Control[3]) +
                     (arrB_Matrix[7, 4] * arrU_Control[4]) +
                     (arrEw_Matrix[7, 1] * arrW_Disturbance[1]) +
                     (arrEw_Matrix[7, 2] * arrW_Disturbance[2]) +
                     (arrEw_Matrix[7, 3] * arrW_Disturbance[3]);

(* State 8: Shielding Gas Nitrogen Concentration C_N2 [%] *)
arrX_Predicted[8] := (arrA_Matrix[8, 1] * arrX_State[1]) +
                     (arrA_Matrix[8, 2] * arrX_State[2]) +
                     (arrA_Matrix[8, 3] * arrX_State[3]) +
                     (arrA_Matrix[8, 4] * arrX_State[4]) +
                     (arrA_Matrix[8, 5] * arrX_State[5]) +
                     (arrA_Matrix[8, 6] * arrX_State[6]) +
                     (arrA_Matrix[8, 7] * arrX_State[7]) +
                     (arrA_Matrix[8, 8] * arrX_State[8]) +
                     (arrB_Matrix[8, 1] * arrU_Control[1]) +
                     (arrB_Matrix[8, 2] * arrU_Control[2]) +
                     (arrB_Matrix[8, 3] * arrU_Control[3]) +
                     (arrB_Matrix[8, 4] * arrU_Control[4]) +
                     (arrEw_Matrix[8, 1] * arrW_Disturbance[1]) +
                     (arrEw_Matrix[8, 2] * arrW_Disturbance[2]) +
                     (arrEw_Matrix[8, 3] * arrW_Disturbance[3]);

(* Physical Lower-Bound Clamping of Predicted States *)
arrX_Predicted[1] := MAX(25.0, arrX_Predicted[1]);
arrX_Predicted[2] := MAX(25.0, arrX_Predicted[2]);
arrX_Predicted[3] := MAX(25.0, arrX_Predicted[3]);
arrX_Predicted[4] := MAX(0.0, arrX_Predicted[4]);
arrX_Predicted[5] := MAX(0.0, arrX_Predicted[5]);
arrX_Predicted[8] := MIN(100.0, MAX(0.0, arrX_Predicted[8]));

(* -------------------------------------------------------------------------------------------------
   STEP 2.4: UNROLLED OUTPUT ESTIMATION (y_est = C * x_pred + D * u)
   ------------------------------------------------------------------------------------------------- *)
arrY_Estimated[1] := (arrC_Matrix[1, 1] * arrX_Predicted[1]) +
                     (arrC_Matrix[1, 2] * arrX_Predicted[2]) +
                     (arrC_Matrix[1, 3] * arrX_Predicted[3]) +
                     (arrC_Matrix[1, 4] * arrX_Predicted[4]) +
                     (arrC_Matrix[1, 5] * arrX_Predicted[5]) +
                     (arrC_Matrix[1, 6] * arrX_Predicted[6]) +
                     (arrC_Matrix[1, 7] * arrX_Predicted[7]) +
                     (arrC_Matrix[1, 8] * arrX_Predicted[8]) +
                     (arrD_Matrix[1, 1] * arrU_Control[1]) +
                     (arrD_Matrix[1, 2] * arrU_Control[2]) +
                     (arrD_Matrix[1, 3] * arrU_Control[3]) +
                     (arrD_Matrix[1, 4] * arrU_Control[4]);

arrY_Estimated[2] := (arrC_Matrix[2, 1] * arrX_Predicted[1]) +
                     (arrC_Matrix[2, 2] * arrX_Predicted[2]) +
                     (arrC_Matrix[2, 3] * arrX_Predicted[3]) +
                     (arrC_Matrix[2, 4] * arrX_Predicted[4]) +
                     (arrC_Matrix[2, 5] * arrX_Predicted[5]) +
                     (arrC_Matrix[2, 6] * arrX_Predicted[6]) +
                     (arrC_Matrix[2, 7] * arrX_Predicted[7]) +
                     (arrC_Matrix[2, 8] * arrX_Predicted[8]) +
                     (arrD_Matrix[2, 1] * arrU_Control[1]) +
                     (arrD_Matrix[2, 2] * arrU_Control[2]) +
                     (arrD_Matrix[2, 3] * arrU_Control[3]) +
                     (arrD_Matrix[2, 4] * arrU_Control[4]);

arrY_Estimated[3] := (arrC_Matrix[3, 1] * arrX_Predicted[1]) +
                     (arrC_Matrix[3, 2] * arrX_Predicted[2]) +
                     (arrC_Matrix[3, 3] * arrX_Predicted[3]) +
                     (arrC_Matrix[3, 4] * arrX_Predicted[4]) +
                     (arrC_Matrix[3, 5] * arrX_Predicted[5]) +
                     (arrC_Matrix[3, 6] * arrX_Predicted[6]) +
                     (arrC_Matrix[3, 7] * arrX_Predicted[7]) +
                     (arrC_Matrix[3, 8] * arrX_Predicted[8]) +
                     (arrD_Matrix[3, 1] * arrU_Control[1]) +
                     (arrD_Matrix[3, 2] * arrU_Control[2]) +
                     (arrD_Matrix[3, 3] * arrU_Control[3]) +
                     (arrD_Matrix[3, 4] * arrU_Control[4]);

arrY_Estimated[4] := (arrC_Matrix[4, 1] * arrX_Predicted[1]) +
                     (arrC_Matrix[4, 2] * arrX_Predicted[2]) +
                     (arrC_Matrix[4, 3] * arrX_Predicted[3]) +
                     (arrC_Matrix[4, 4] * arrX_Predicted[4]) +
                     (arrC_Matrix[4, 5] * arrX_Predicted[5]) +
                     (arrC_Matrix[4, 6] * arrX_Predicted[6]) +
                     (arrC_Matrix[4, 7] * arrX_Predicted[7]) +
                     (arrC_Matrix[4, 8] * arrX_Predicted[8]) +
                     (arrD_Matrix[4, 1] * arrU_Control[1]) +
                     (arrD_Matrix[4, 2] * arrU_Control[2]) +
                     (arrD_Matrix[4, 3] * arrU_Control[3]) +
                     (arrD_Matrix[4, 4] * arrU_Control[4]);

arrY_Estimated[5] := (arrC_Matrix[5, 1] * arrX_Predicted[1]) +
                     (arrC_Matrix[5, 2] * arrX_Predicted[2]) +
                     (arrC_Matrix[5, 3] * arrX_Predicted[3]) +
                     (arrC_Matrix[5, 4] * arrX_Predicted[4]) +
                     (arrC_Matrix[5, 5] * arrX_Predicted[5]) +
                     (arrC_Matrix[5, 6] * arrX_Predicted[6]) +
                     (arrC_Matrix[5, 7] * arrX_Predicted[7]) +
                     (arrC_Matrix[5, 8] * arrX_Predicted[8]) +
                     (arrD_Matrix[5, 1] * arrU_Control[1]) +
                     (arrD_Matrix[5, 2] * arrU_Control[2]) +
                     (arrD_Matrix[5, 3] * arrU_Control[3]) +
                     (arrD_Matrix[5, 4] * arrU_Control[4]);

arrY_Estimated[6] := (arrC_Matrix[6, 1] * arrX_Predicted[1]) +
                     (arrC_Matrix[6, 2] * arrX_Predicted[2]) +
                     (arrC_Matrix[6, 3] * arrX_Predicted[3]) +
                     (arrC_Matrix[6, 4] * arrX_Predicted[4]) +
                     (arrC_Matrix[6, 5] * arrX_Predicted[5]) +
                     (arrC_Matrix[6, 6] * arrX_Predicted[6]) +
                     (arrC_Matrix[6, 7] * arrX_Predicted[7]) +
                     (arrC_Matrix[6, 8] * arrX_Predicted[8]) +
                     (arrD_Matrix[6, 1] * arrU_Control[1]) +
                     (arrD_Matrix[6, 2] * arrU_Control[2]) +
                     (arrD_Matrix[6, 3] * arrU_Control[3]) +
                     (arrD_Matrix[6, 4] * arrU_Control[4]);

(* -------------------------------------------------------------------------------------------------
   STEP 2.5: MEASUREMENT INNOVATION RESIDUALS (e = y_meas - y_est)
   ------------------------------------------------------------------------------------------------- *)
arrY_Innovation[1] := arrY_Measurement[1] - arrY_Estimated[1];
arrY_Innovation[2] := arrY_Measurement[2] - arrY_Estimated[2];
arrY_Innovation[3] := arrY_Measurement[3] - arrY_Estimated[3];
arrY_Innovation[4] := arrY_Measurement[4] - arrY_Estimated[4];
arrY_Innovation[5] := arrY_Measurement[5] - arrY_Estimated[5];
arrY_Innovation[6] := arrY_Measurement[6] - arrY_Estimated[6];

(* -------------------------------------------------------------------------------------------------
   STEP 2.6: LUENBERGER OBSERVER CLOSED-LOOP CORRECTION (x_est = x_pred + Ke * e)
   ------------------------------------------------------------------------------------------------- *)
arrX_Estimated[1] := arrX_Predicted[1] +
                     (arrKe_Matrix[1, 1] * arrY_Innovation[1]) +
                     (arrKe_Matrix[1, 2] * arrY_Innovation[2]) +
                     (arrKe_Matrix[1, 3] * arrY_Innovation[3]) +
                     (arrKe_Matrix[1, 4] * arrY_Innovation[4]) +
                     (arrKe_Matrix[1, 5] * arrY_Innovation[5]) +
                     (arrKe_Matrix[1, 6] * arrY_Innovation[6]);

arrX_Estimated[2] := arrX_Predicted[2] +
                     (arrKe_Matrix[2, 1] * arrY_Innovation[1]) +
                     (arrKe_Matrix[2, 2] * arrY_Innovation[2]) +
                     (arrKe_Matrix[2, 3] * arrY_Innovation[3]) +
                     (arrKe_Matrix[2, 4] * arrY_Innovation[4]) +
                     (arrKe_Matrix[2, 5] * arrY_Innovation[5]) +
                     (arrKe_Matrix[2, 6] * arrY_Innovation[6]);

arrX_Estimated[3] := arrX_Predicted[3] +
                     (arrKe_Matrix[3, 1] * arrY_Innovation[1]) +
                     (arrKe_Matrix[3, 2] * arrY_Innovation[2]) +
                     (arrKe_Matrix[3, 3] * arrY_Innovation[3]) +
                     (arrKe_Matrix[3, 4] * arrY_Innovation[4]) +
                     (arrKe_Matrix[3, 5] * arrY_Innovation[5]) +
                     (arrKe_Matrix[3, 6] * arrY_Innovation[6]);

arrX_Estimated[4] := arrX_Predicted[4] +
                     (arrKe_Matrix[4, 1] * arrY_Innovation[1]) +
                     (arrKe_Matrix[4, 2] * arrY_Innovation[2]) +
                     (arrKe_Matrix[4, 3] * arrY_Innovation[3]) +
                     (arrKe_Matrix[4, 4] * arrY_Innovation[4]) +
                     (arrKe_Matrix[4, 5] * arrY_Innovation[5]) +
                     (arrKe_Matrix[4, 6] * arrY_Innovation[6]);

arrX_Estimated[5] := arrX_Predicted[5] +
                     (arrKe_Matrix[5, 1] * arrY_Innovation[1]) +
                     (arrKe_Matrix[5, 2] * arrY_Innovation[2]) +
                     (arrKe_Matrix[5, 3] * arrY_Innovation[3]) +
                     (arrKe_Matrix[5, 4] * arrY_Innovation[4]) +
                     (arrKe_Matrix[5, 5] * arrY_Innovation[5]) +
                     (arrKe_Matrix[5, 6] * arrY_Innovation[6]);

arrX_Estimated[6] := arrX_Predicted[6] +
                     (arrKe_Matrix[6, 1] * arrY_Innovation[1]) +
                     (arrKe_Matrix[6, 2] * arrY_Innovation[2]) +
                     (arrKe_Matrix[6, 3] * arrY_Innovation[3]) +
                     (arrKe_Matrix[6, 4] * arrY_Innovation[4]) +
                     (arrKe_Matrix[6, 5] * arrY_Innovation[5]) +
                     (arrKe_Matrix[6, 6] * arrY_Innovation[6]);

arrX_Estimated[7] := arrX_Predicted[7] +
                     (arrKe_Matrix[7, 1] * arrY_Innovation[1]) +
                     (arrKe_Matrix[7, 2] * arrY_Innovation[2]) +
                     (arrKe_Matrix[7, 3] * arrY_Innovation[3]) +
                     (arrKe_Matrix[7, 4] * arrY_Innovation[4]) +
                     (arrKe_Matrix[7, 5] * arrY_Innovation[5]) +
                     (arrKe_Matrix[7, 6] * arrY_Innovation[6]);

arrX_Estimated[8] := arrX_Predicted[8] +
                     (arrKe_Matrix[8, 1] * arrY_Innovation[1]) +
                     (arrKe_Matrix[8, 2] * arrY_Innovation[2]) +
                     (arrKe_Matrix[8, 3] * arrY_Innovation[3]) +
                     (arrKe_Matrix[8, 4] * arrY_Innovation[4]) +
                     (arrKe_Matrix[8, 5] * arrY_Innovation[5]) +
                     (arrKe_Matrix[8, 6] * arrY_Innovation[6]);

(* -------------------------------------------------------------------------------------------------
   STEP 2.7: OBSERVER STATE COMMIT & CYBER-PHYSICAL SYNTHESIS
   ------------------------------------------------------------------------------------------------- *)
FOR iIndex_Loop1 := 1 TO 8 DO
    arrX_State[iIndex_Loop1] := arrX_Estimated[iIndex_Loop1];
END_FOR;

(* Assign Cyber-Physical Observable Outputs *)
rEst_MeltPool_Volume_mm3 := MAX(0.0, arrX_State[5]);
rEst_Keyhole_Depth_mm    := MAX(0.0, arrX_State[4]);

(* Empirical 4-Wire Kelvin Joint Resistance Model from Nugget Volume & Penetration *)
IF arrX_State[5] > 0.50 THEN
    rEst_JointResistance_uOhm := 1.45 + (1.20 / (arrX_State[5] * 0.40)) + (0.15 * MAX(0.0, 2.20 - arrX_State[4]));
ELSE
    rEst_JointResistance_uOhm := 9.99; (* Unfused Pin Pair *)
END_IF;
"""
