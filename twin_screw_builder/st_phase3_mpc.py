(* =====================================================================================================================
 * PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) & NON-LINEAR SHEAR DECOUPLING
 * Horizon: Np = 5 steps | Optimization: 6 Unrolled Projected Gradient Descent (PGD) Iterations
 * Controlled Variables: Melt Pump Suction Pressure (45.0 bar), Die Pressure (75.0 bar), Melt Temp (275.0 °C)
 * Manipulated Variables: Extruder Screw Drive Speed [rpm] & Melt Gear Pump Servo Speed [rpm]
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * STEP 3.1: MULTI-STEP RECURSIVE HORIZON PREDICTION BUFFER INITIALIZATION (Np = 5 steps)
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Initialize Horizon Step 1 from Current Plant Estimated State Vector *)
FOR idx_i := 1 TO 16 DO
    x_horiz[1, idx_i] := x_state[idx_i];
END_FOR;

(* Initialize Candidate Actuator Speed References from Previous Commands *)
rCand_ScrewSpeed := rPrev_ScrewSpeed_Cmd;
rCand_PumpSpeed  := rPrev_PumpSpeed_Cmd;

(* Clamp Candidate Speeds to Absolute Mechanical Machine Boundaries *)
IF rCand_ScrewSpeed < 0.0 THEN
    rCand_ScrewSpeed := 0.0;
ELSIF rCand_ScrewSpeed > MAX_RATED_SCREW_SPEED THEN
    rCand_ScrewSpeed := MAX_RATED_SCREW_SPEED;
END_IF;

IF rCand_PumpSpeed < 0.0 THEN
    rCand_PumpSpeed := 0.0;
ELSIF rCand_PumpSpeed > MAX_RATED_GEARPUMP_SPEED THEN
    rCand_PumpSpeed := MAX_RATED_GEARPUMP_SPEED;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * STEP 3.2: UNROLLED PROJECTED GRADIENT DESCENT (PGD) OPTIMIZATION SOLVER (6 ITERATIONS)
 * Evaluates Quadratic Cost Functional J and Computes Analytical Gradient Direction
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR idx_m := 1 TO 6 DO
    (* Predict Receding State Trajectory across Np = 5 Steps under Candidate Actuator Commands *)
    FOR idx_k := 1 TO 4 DO
        FOR idx_i := 1 TO 16 DO
            rCalc_Sum := 0.0;
            FOR idx_j := 1 TO 16 DO
                rCalc_Sum := rCalc_Sum + (A_mat[idx_i, idx_j] * x_horiz[idx_k, idx_j]);
            END_FOR;
            (* Apply Candidate Speed Inputs u[13] and u[14] *)
            rCalc_Sum := rCalc_Sum + (B_mat[idx_i, 13] * rCand_ScrewSpeed);
            rCalc_Sum := rCalc_Sum + (B_mat[idx_i, 14] * rCand_PumpSpeed);
            (* Include existing thermal heating commands u[1..12] *)
            FOR idx_j := 1 TO 12 DO
                rCalc_Sum := rCalc_Sum + (B_mat[idx_i, idx_j] * u_input[idx_j]);
            END_FOR;
            x_horiz[idx_k + 1, idx_i] := rCalc_Sum;
        END_FOR;
    END_FOR;

    (* Evaluate Analytical Cost Gradients w.r.t Screw Speed (u_13) and Gear Pump Speed (u_14) *)
    (* dJ/d(u_13) and dJ/d(u_14) accumulated over prediction horizon Np = 5 *)
    rGrad_ScrewSpeed := 0.0;
    rGrad_PumpSpeed  := 0.0;

    FOR idx_k := 2 TO 5 DO
        (* Suction Pressure Tracking Error: e_suct = x_horiz[k, 16] - SP_Suct *)
        rCalc_TempA := x_horiz[idx_k, 16] - rMPC_SP_SuctPres;
        (* Die Pressure Tracking Error: e_die = x_horiz[k, 14] - SP_Die *)
        rCalc_TempB := x_horiz[idx_k, 14] - rMPC_SP_DiePres;
        (* Melt Temp Tracking Error: e_temp = x_horiz[k, 13] - SP_MeltTemp *)
        rCalc_TempC := x_horiz[idx_k, 13] - rMPC_SP_MeltTemp;

        (* Gradient Contribution from Suction Pressure (B[16, 13] > 0, B[16, 14] < 0) *)
        rGrad_ScrewSpeed := rGrad_ScrewSpeed + (2.0 * rMPC_Weight_SuctPres * rCalc_TempA * B_mat[16, 13]);
        rGrad_PumpSpeed  := rGrad_PumpSpeed  + (2.0 * rMPC_Weight_SuctPres * rCalc_TempA * B_mat[16, 14]);

        (* Gradient Contribution from Die Pressure (B[14, 14] > 0) *)
        rGrad_PumpSpeed  := rGrad_PumpSpeed  + (2.0 * rMPC_Weight_DiePres * rCalc_TempB * B_mat[14, 14]);

        (* Gradient Contribution from Polymer Melt Temperature (B[13, 13] > 0 via shear heating) *)
        rGrad_ScrewSpeed := rGrad_ScrewSpeed + (2.0 * rMPC_Weight_MeltTemp * rCalc_TempC * B_mat[13, 13]);

        (* Barrier Penalty for Shaft Torque Overload: Max(0, x_horiz[k, 15] - MAX_TORQUE) *)
        IF x_horiz[idx_k, 15] > (0.90 * MAX_RATED_SCREW_TORQUE) THEN
            rCalc_TempD := x_horiz[idx_k, 15] - (0.90 * MAX_RATED_SCREW_TORQUE);
            rGrad_ScrewSpeed := rGrad_ScrewSpeed + (2.0 * rMPC_Weight_TorqueLimit * rCalc_TempD * B_mat[15, 13]);
        END_IF;
    END_FOR;

    (* Add Regularization Slew Suppression Gradient Penalties *)
    rGrad_ScrewSpeed := rGrad_ScrewSpeed + (2.0 * rMPC_Weight_DeltaScrewSpeed * (rCand_ScrewSpeed - rPrev_ScrewSpeed_Cmd));
    rGrad_PumpSpeed  := rGrad_PumpSpeed  + (2.0 * rMPC_Weight_DeltaPumpSpeed  * (rCand_PumpSpeed  - rPrev_PumpSpeed_Cmd));

    (* Apply Gradient Descent Step Update: u = u - alpha * grad *)
    rCand_ScrewSpeed := rCand_ScrewSpeed - (rMPC_Alpha_Step * rGrad_ScrewSpeed);
    rCand_PumpSpeed  := rCand_PumpSpeed  - (rMPC_Alpha_Step * rGrad_PumpSpeed);

    (* Projection 1: Mechanical Box Bound Actuator Saturation Constraints *)
    IF rCand_ScrewSpeed < 0.0 THEN
        rCand_ScrewSpeed := 0.0;
    ELSIF rCand_ScrewSpeed > MAX_RATED_SCREW_SPEED THEN
        rCand_ScrewSpeed := MAX_RATED_SCREW_SPEED;
    END_IF;

    IF rCand_PumpSpeed < 0.0 THEN
        rCand_PumpSpeed := 0.0;
    ELSIF rCand_PumpSpeed > MAX_RATED_GEARPUMP_SPEED THEN
        rCand_PumpSpeed := MAX_RATED_GEARPUMP_SPEED;
    END_IF;
END_FOR;

(* Assign Converged PGD Optimization Results *)
rOptimal_ScrewSpeed_Cmd := rCand_ScrewSpeed;
rOptimal_PumpSpeed_Cmd  := rCand_PumpSpeed;

(* Diagnostic MPC Objective Cost Functional Computation *)
rCalc_TempA := x_state[16] - rMPC_SP_SuctPres;
rMPC_CostSuctPres_Out := rMPC_Weight_SuctPres * (rCalc_TempA * rCalc_TempA);
rMPC_PredMeltPres_Out := x_horiz[5, 14];

(* ---------------------------------------------------------------------------------------------------------------------
 * STEP 3.3: DYNAMIC ACCELERATION / DECELERATION SLEW RATE LIMITERS
 * Protects Extruder Helical Reduction Gearbox and Melt Pump Ceramic Bearings
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Extruder Screw Drive Slew Limiter (Max 12.0 rpm/s -> 0.24 rpm per 20 ms scan) *)
rCalc_TempA := rMaxScrewSpeedSlew * T_SAMPLE;
rCalc_TempB := rOptimal_ScrewSpeed_Cmd - rPrev_ScrewSpeed_Cmd;
IF rCalc_TempB > rCalc_TempA THEN
    rScrewSpeed_Cmd_Out := rPrev_ScrewSpeed_Cmd + rCalc_TempA;
ELSIF rCalc_TempB < -rCalc_TempA THEN
    rScrewSpeed_Cmd_Out := rPrev_ScrewSpeed_Cmd - rCalc_TempA;
ELSE
    rScrewSpeed_Cmd_Out := rOptimal_ScrewSpeed_Cmd;
END_IF;
rPrev_ScrewSpeed_Cmd := rScrewSpeed_Cmd_Out;

(* Melt Gear Pump Drive Slew Limiter (Max 4.5 rpm/s -> 0.09 rpm per 20 ms scan) *)
rCalc_TempA := rMaxPumpSpeedSlew * T_SAMPLE;
rCalc_TempB := rOptimal_PumpSpeed_Cmd - rPrev_PumpSpeed_Cmd;
IF rCalc_TempB > rCalc_TempA THEN
    rGearPumpSpeed_Cmd_Out := rPrev_PumpSpeed_Cmd + rCalc_TempA;
ELSIF rCalc_TempB < -rCalc_TempA THEN
    rGearPumpSpeed_Cmd_Out := rPrev_PumpSpeed_Cmd - rCalc_TempA;
ELSE
    rGearPumpSpeed_Cmd_Out := rOptimal_PumpSpeed_Cmd;
END_IF;
rPrev_PumpSpeed_Cmd := rGearPumpSpeed_Cmd_Out;

(* ---------------------------------------------------------------------------------------------------------------------
 * STEP 3.4: BARREL ZONE DYNAMIC VISCOUS SHEAR DECOUPLING FEEDFORWARD
 * Distributes Mechanical Dissipation Power across Kneading/Mixing Zones to Prevent Thermal Runaway
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Zone Shear Heating Distribution Factors:
 * Zone 01: 0.00 | Zone 02: 0.02 | Zone 03: 0.28 (Kneading) | Zone 04: 0.18
 * Zone 05: 0.04 | Zone 06: 0.26 (Dispersive) | Zone 07: 0.08 | Zone 08: 0.02
 * Zone 09: 0.02 | Zone 10: 0.08 | Zone 11: 0.02 | Zone 12: 0.00 *)
rDecoupledShearCorrection[1]  := 0.0;
rDecoupledShearCorrection[2]  := 0.02 * rOnline_ShearHeatingPowerKW * 0.45;
rDecoupledShearCorrection[3]  := 0.28 * rOnline_ShearHeatingPowerKW * 0.45;
rDecoupledShearCorrection[4]  := 0.18 * rOnline_ShearHeatingPowerKW * 0.45;
rDecoupledShearCorrection[5]  := 0.04 * rOnline_ShearHeatingPowerKW * 0.45;
rDecoupledShearCorrection[6]  := 0.26 * rOnline_ShearHeatingPowerKW * 0.45;
rDecoupledShearCorrection[7]  := 0.08 * rOnline_ShearHeatingPowerKW * 0.45;
rDecoupledShearCorrection[8]  := 0.02 * rOnline_ShearHeatingPowerKW * 0.45;
rDecoupledShearCorrection[9]  := 0.02 * rOnline_ShearHeatingPowerKW * 0.45;
rDecoupledShearCorrection[10] := 0.08 * rOnline_ShearHeatingPowerKW * 0.45;
rDecoupledShearCorrection[11] := 0.02 * rOnline_ShearHeatingPowerKW * 0.45;
rDecoupledShearCorrection[12] := 0.0;

(* ---------------------------------------------------------------------------------------------------------------------
 * STEP 3.5: 12-ZONE BARREL TEMPERATURE INDIVIDUAL SPLIT-RANGE PID & PWM GENERATION
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Initialize Standard Tuning Gains per Zone if not already configured *)
rPID_Zone_Kp[1]  := 4.2;  rPID_Zone_Tn[1]  := 180.0; rPID_Zone_Tv[1]  := 28.0;
rPID_Zone_Kp[2]  := 5.0;  rPID_Zone_Tn[2]  := 160.0; rPID_Zone_Tv[2]  := 32.0;
rPID_Zone_Kp[3]  := 6.5;  rPID_Zone_Tn[3]  := 140.0; rPID_Zone_Tv[3]  := 38.0;
rPID_Zone_Kp[4]  := 5.8;  rPID_Zone_Tn[4]  := 150.0; rPID_Zone_Tv[4]  := 35.0;
rPID_Zone_Kp[5]  := 4.8;  rPID_Zone_Tn[5]  := 170.0; rPID_Zone_Tv[5]  := 30.0;
rPID_Zone_Kp[6]  := 6.2;  rPID_Zone_Tn[6]  := 145.0; rPID_Zone_Tv[6]  := 36.0;
rPID_Zone_Kp[7]  := 5.5;  rPID_Zone_Tn[7]  := 155.0; rPID_Zone_Tv[7]  := 34.0;
rPID_Zone_Kp[8]  := 5.2;  rPID_Zone_Tn[8]  := 165.0; rPID_Zone_Tv[8]  := 31.0;
rPID_Zone_Kp[9]  := 5.0;  rPID_Zone_Tn[9]  := 160.0; rPID_Zone_Tv[9]  := 32.0;
rPID_Zone_Kp[10] := 5.6;  rPID_Zone_Tn[10] := 150.0; rPID_Zone_Tv[10] := 33.0;
rPID_Zone_Kp[11] := 5.8;  rPID_Zone_Tn[11] := 145.0; rPID_Zone_Tv[11] := 34.0;
rPID_Zone_Kp[12] := 6.0;  rPID_Zone_Tn[12] := 140.0; rPID_Zone_Tv[12] := 35.0;

(* Execute 12-Zone Cascaded Loop Calculations *)
FOR idx_z := 1 TO 12 DO
    (* Map Zone Input Temperatures and Setpoints *)
    CASE idx_z OF
        1:  rPID_Zone_Err[1]  := rZoneTemp_SP_Z01_In - rZoneTemp_Act_Z01_In;
        2:  rPID_Zone_Err[2]  := rZoneTemp_SP_Z02_In - rZoneTemp_Act_Z02_In;
        3:  rPID_Zone_Err[3]  := rZoneTemp_SP_Z03_In - rZoneTemp_Act_Z03_In;
        4:  rPID_Zone_Err[4]  := rZoneTemp_SP_Z04_In - rZoneTemp_Act_Z04_In;
        5:  rPID_Zone_Err[5]  := rZoneTemp_SP_Z05_In - rZoneTemp_Act_Z05_In;
        6:  rPID_Zone_Err[6]  := rZoneTemp_SP_Z06_In - rZoneTemp_Act_Z06_In;
        7:  rPID_Zone_Err[7]  := rZoneTemp_SP_Z07_In - rZoneTemp_Act_Z07_In;
        8:  rPID_Zone_Err[8]  := rZoneTemp_SP_Z08_In - rZoneTemp_Act_Z08_In;
        9:  rPID_Zone_Err[9]  := rZoneTemp_SP_Z09_In - rZoneTemp_Act_Z09_In;
        10: rPID_Zone_Err[10] := rZoneTemp_SP_Z10_In - rZoneTemp_Act_Z10_In;
        11: rPID_Zone_Err[11] := rZoneTemp_SP_Z11_In - rZoneTemp_Act_Z11_In;
        12: rPID_Zone_Err[12] := rZoneTemp_SP_Z12_In - rZoneTemp_Act_Z12_In;
    END_CASE;

    (* Anti-Windup Trapezoidal Integral Accumulator *)
    IF rPID_Zone_Tn[idx_z] > 1.0 THEN
        rPID_Zone_Integ[idx_z] := rPID_Zone_Integ[idx_z] +
            ((rPID_Zone_Kp[idx_z] / rPID_Zone_Tn[idx_z]) * 0.5 * (rPID_Zone_Err[idx_z] + rPID_Zone_PrevErr[idx_z]) * T_SAMPLE);
    END_IF;

    (* Clamp Integral Accumulator to [-100.0% .. +100.0%] *)
    IF rPID_Zone_Integ[idx_z] > 100.0 THEN
        rPID_Zone_Integ[idx_z] := 100.0;
    ELSIF rPID_Zone_Integ[idx_z] < -100.0 THEN
        rPID_Zone_Integ[idx_z] := -100.0;
    END_IF;

    (* Derivative Rate of Error Change *)
    IF T_SAMPLE > 0.001 THEN
        rCalc_TempA := (rPID_Zone_Kp[idx_z] * rPID_Zone_Tv[idx_z]) * (rPID_Zone_Err[idx_z] - rPID_Zone_PrevErr[idx_z]) / T_SAMPLE;
    ELSE
        rCalc_TempA := 0.0;
    END_IF;
    rPID_Zone_PrevErr[idx_z] := rPID_Zone_Err[idx_z];

    (* Sum PID Terms and Subtract Viscous Shear Heating Feedforward Compensation *)
    rPID_Zone_RawOut[idx_z] := (rPID_Zone_Kp[idx_z] * rPID_Zone_Err[idx_z]) +
                               rPID_Zone_Integ[idx_z] +
                               rCalc_TempA -
                               rDecoupledShearCorrection[idx_z];

    (* Split-Range Heating vs Solenoid Cooling Decision *)
    IF rPID_Zone_RawOut[idx_z] >= 0.0 THEN
        (* Heating Demand [%]: 0.0 to 100.0% *)
        rCalc_TempB := rPID_Zone_RawOut[idx_z];
        IF rCalc_TempB > 100.0 THEN
            rCalc_TempB := 100.0;
        END_IF;
        rCalc_TempC := 0.0; (* No cooling *)
    ELSE
        (* Cooling Demand [%]: 0.0 to 100.0% with 2.0% Neutral Deadband *)
        rCalc_TempB := 0.0; (* No heating *)
        rCalc_TempC := -rPID_Zone_RawOut[idx_z];
        IF rCalc_TempC < 2.0 THEN
            rCalc_TempC := 0.0;
        ELSIF rCalc_TempC > 100.0 THEN
            rCalc_TempC := 100.0;
        END_IF;
    END_IF;

    (* Time-Proportioned PWM Generator for Electric Heater Bands (Cycle = 4.0 s) *)
    rPWM_Zone_HeatAccum[idx_z] := rPWM_Zone_HeatAccum[idx_z] + T_SAMPLE;
    IF rPWM_Zone_HeatAccum[idx_z] >= rPWM_Zone_CyclePeriod THEN
        rPWM_Zone_HeatAccum[idx_z] := 0.0;
    END_IF;

    (* Time-Proportioned PWM Generator for Water Cooling Solenoids (Cycle = 4.0 s) *)
    rPWM_Zone_CoolAccum[idx_z] := rPWM_Zone_CoolAccum[idx_z] + T_SAMPLE;
    IF rPWM_Zone_CoolAccum[idx_z] >= rPWM_Zone_CyclePeriod THEN
        rPWM_Zone_CoolAccum[idx_z] := 0.0;
    END_IF;

    (* Map Calculated Heating and Cooling Commands to Physical Hardware Outputs *)
    CASE idx_z OF
        1:
            rZoneHeat_Cmd_Z01_Out := rCalc_TempB;
            bZoneCool_Cmd_Z01_Out := (rPWM_Zone_CoolAccum[1] < (rCalc_TempC * 0.01 * rPWM_Zone_CyclePeriod)) AND (rCalc_TempC > 5.0);
        2:
            rZoneHeat_Cmd_Z02_Out := rCalc_TempB;
            bZoneCool_Cmd_Z02_Out := (rPWM_Zone_CoolAccum[2] < (rCalc_TempC * 0.01 * rPWM_Zone_CyclePeriod)) AND (rCalc_TempC > 5.0);
        3:
            rZoneHeat_Cmd_Z03_Out := rCalc_TempB;
            bZoneCool_Cmd_Z03_Out := (rPWM_Zone_CoolAccum[3] < (rCalc_TempC * 0.01 * rPWM_Zone_CyclePeriod)) AND (rCalc_TempC > 5.0);
        4:
            rZoneHeat_Cmd_Z04_Out := rCalc_TempB;
            bZoneCool_Cmd_Z04_Out := (rPWM_Zone_CoolAccum[4] < (rCalc_TempC * 0.01 * rPWM_Zone_CyclePeriod)) AND (rCalc_TempC > 5.0);
        5:
            rZoneHeat_Cmd_Z05_Out := rCalc_TempB;
            bZoneCool_Cmd_Z05_Out := (rPWM_Zone_CoolAccum[5] < (rCalc_TempC * 0.01 * rPWM_Zone_CyclePeriod)) AND (rCalc_TempC > 5.0);
        6:
            rZoneHeat_Cmd_Z06_Out := rCalc_TempB;
            bZoneCool_Cmd_Z06_Out := (rPWM_Zone_CoolAccum[6] < (rCalc_TempC * 0.01 * rPWM_Zone_CyclePeriod)) AND (rCalc_TempC > 5.0);
        7:
            rZoneHeat_Cmd_Z07_Out := rCalc_TempB;
            bZoneCool_Cmd_Z07_Out := (rPWM_Zone_CoolAccum[7] < (rCalc_TempC * 0.01 * rPWM_Zone_CyclePeriod)) AND (rCalc_TempC > 5.0);
        8:
            rZoneHeat_Cmd_Z08_Out := rCalc_TempB;
            bZoneCool_Cmd_Z08_Out := (rPWM_Zone_CoolAccum[8] < (rCalc_TempC * 0.01 * rPWM_Zone_CyclePeriod)) AND (rCalc_TempC > 5.0);
        9:
            rZoneHeat_Cmd_Z09_Out := rCalc_TempB;
            bZoneCool_Cmd_Z09_Out := (rPWM_Zone_CoolAccum[9] < (rCalc_TempC * 0.01 * rPWM_Zone_CyclePeriod)) AND (rCalc_TempC > 5.0);
        10:
            rZoneHeat_Cmd_Z10_Out := rCalc_TempB;
            bZoneCool_Cmd_Z10_Out := (rPWM_Zone_CoolAccum[10] < (rCalc_TempC * 0.01 * rPWM_Zone_CyclePeriod)) AND (rCalc_TempC > 5.0);
        11:
            rZoneHeat_Cmd_Z11_Out := rCalc_TempB;
            bZoneCool_Cmd_Z11_Out := (rPWM_Zone_CoolAccum[11] < (rCalc_TempC * 0.01 * rPWM_Zone_CyclePeriod)) AND (rCalc_TempC > 5.0);
        12:
            rZoneHeat_Cmd_Z12_Out := rCalc_TempB;
            bZoneCool_Cmd_Z12_Out := (rPWM_Zone_CoolAccum[12] < (rCalc_TempC * 0.01 * rPWM_Zone_CyclePeriod)) AND (rCalc_TempC > 5.0);
    END_CASE;
END_FOR;
