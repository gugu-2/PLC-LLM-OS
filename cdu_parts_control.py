# -*- coding: utf-8 -*-
"""
Control module (Phases 4-6) for FB_DataCenter_LiquidCooling_CDU_DirectToChip
Contains:
  Phase 4: Discrete 8x8 State-Space & Receding-Horizon MPC Action
  Phase 5: Multi-Stage 12-State Finite State Machine (FSM)
  Phase 6: ISA-18.2 Multi-Tier Alarm Engine, Fast Trips, and Diagnostic Word Packing
"""

def get_phase4_mpc():
    return """(* ========================================================================= *)
(* === PHASE 4: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) ACTION ===== *)
(* ========================================================================= *)
(*
   Discrete 8x8 State-Space Representation executed at Ts = 50 ms (0.050 s):
     x[k+1] = A * x[k] + B * u[k] + Bw * w[k]
     y[k]   = C * x[k] + D * u[k]

   State Vector x:
     x[1] = TCS Supply Temperature error [deg C] (Target: 32.0 C)
     x[2] = TCS Return Temperature error [deg C] (Target: 44.0 C)
     x[3] = TCS Loop Differential Pressure error [bar] (Target: 1.80 bar)
     x[4] = TCS Volumetric Flow error [L/min] (Target: 4000.0 L/min)
     x[5] = PHE Plate Core Thermal State [deg C]
     x[6] = Facility Water Return Temperature error [deg C]
     x[7] = Pump Impeller Hydraulic Momentum [rad/s]
     x[8] = Thermal Storage Buffer Core Enthalpy [deg C]

   Control Vector u:
     u[1] = Lead Pump VFD Speed Reference [rpm] (0 - 3500)
     u[2] = Lag Pump VFD Speed Reference [rpm] (0 - 3500)
     u[3] = Primary PHE Modulating Equal-Percentage Valve [%] (0 - 100%)
     u[4] = Secondary TCS 3-Way Fast Bypass Mixing Valve [%] (0 - 100%)

   Disturbance Vector w:
     w[1] = AI Cluster Instantaneous Heat Power Surge [MW]
     w[2] = Facility Chilled Water Supply Temperature Drift [deg C]
*)

(* Initialize matrices once on cold boot *)
IF NOT bMatrices_Initialized THEN
    (* Row 1: Supply Temperature dynamics *)
    mA_Matrix[1,1] := 0.9450; mA_Matrix[1,2] := 0.0120; mA_Matrix[1,3] := -0.0050; mA_Matrix[1,4] := -0.00008;
    mA_Matrix[1,5] := 0.0380; mA_Matrix[1,6] := 0.0000; mA_Matrix[1,7] := -0.0002; mA_Matrix[1,8] := 0.0000;

    (* Row 2: Return Temperature dynamics *)
    mA_Matrix[2,1] := 0.0250; mA_Matrix[2,2] := 0.9200; mA_Matrix[2,3] := -0.0020; mA_Matrix[2,4] := -0.00015;
    mA_Matrix[2,5] := 0.0100; mA_Matrix[2,6] := 0.0000; mA_Matrix[2,7] := -0.0001; mA_Matrix[2,8] := 0.0000;

    (* Row 3: Manifold Differential Pressure dynamics *)
    mA_Matrix[3,1] := 0.0000; mA_Matrix[3,2] := 0.0000; mA_Matrix[3,3] := 0.8850; mA_Matrix[3,4] := 0.00035;
    mA_Matrix[3,5] := 0.0000; mA_Matrix[3,6] := 0.0000; mA_Matrix[3,7] := 0.00185; mA_Matrix[3,8] := 0.0000;

    (* Row 4: Volumetric Flow dynamics *)
    mA_Matrix[4,1] := 0.0000; mA_Matrix[4,2] := 0.0000; mA_Matrix[4,3] := 125.00; mA_Matrix[4,4] := 0.8650;
    mA_Matrix[4,5] := 0.0000; mA_Matrix[4,6] := 0.0000; mA_Matrix[4,7] := 1.4500; mA_Matrix[4,8] := 0.0000;

    (* Row 5: PHE Plate Thermal State *)
    mA_Matrix[5,1] := 0.0420; mA_Matrix[5,2] := 0.0180; mA_Matrix[5,3] := 0.0000; mA_Matrix[5,4] := 0.0000;
    mA_Matrix[5,5] := 0.9150; mA_Matrix[5,6] := 0.0220; mA_Matrix[5,7] := 0.0000; mA_Matrix[5,8] := 0.0000;

    (* Row 6: Facility Return Temperature dynamics *)
    mA_Matrix[6,1] := 0.0000; mA_Matrix[6,2] := 0.0280; mA_Matrix[6,3] := 0.0000; mA_Matrix[6,4] := 0.0000;
    mA_Matrix[6,5] := 0.0450; mA_Matrix[6,6] := 0.9250; mA_Matrix[6,7] := 0.0000; mA_Matrix[6,8] := 0.0000;

    (* Row 7: Pump Impeller Momentum *)
    mA_Matrix[7,1] := 0.0000; mA_Matrix[7,2] := 0.0000; mA_Matrix[7,3] := -0.0150; mA_Matrix[7,4] := -0.0001;
    mA_Matrix[7,5] := 0.0000; mA_Matrix[7,6] := 0.0000; mA_Matrix[7,7] := 0.8500; mA_Matrix[7,8] := 0.0000;

    (* Row 8: Thermal Buffer Storage *)
    mA_Matrix[8,1] := 0.0050; mA_Matrix[8,2] := 0.0000; mA_Matrix[8,3] := 0.0000; mA_Matrix[8,4] := 0.0000;
    mA_Matrix[8,5] := 0.0000; mA_Matrix[8,6] := 0.0000; mA_Matrix[8,7] := 0.0000; mA_Matrix[8,8] := 0.9920;

    (* Matrix B (8x4 Control matrix) *)
    mB_Matrix[1,1] := -0.00012; mB_Matrix[1,2] := -0.00012; mB_Matrix[1,3] := -0.0450; mB_Matrix[1,4] := 0.0380;
    mB_Matrix[2,1] := -0.00018; mB_Matrix[2,2] := -0.00018; mB_Matrix[2,3] := -0.0120; mB_Matrix[2,4] := 0.0050;
    mB_Matrix[3,1] := 0.00062;  mB_Matrix[3,2] := 0.00062;  mB_Matrix[3,3] := 0.0000;  mB_Matrix[3,4] := -0.0015;
    mB_Matrix[4,1] := 0.9500;   mB_Matrix[4,2] := 0.9500;   mB_Matrix[4,3] := 0.0000;  mB_Matrix[4,4] := 0.1200;
    mB_Matrix[5,1] := 0.0000;   mB_Matrix[5,2] := 0.0000;   mB_Matrix[5,3] := -0.0520; mB_Matrix[5,4] := 0.0000;
    mB_Matrix[6,1] := 0.0000;   mB_Matrix[6,2] := 0.0000;   mB_Matrix[6,3] := 0.0480;  mB_Matrix[6,4] := 0.0000;
    mB_Matrix[7,1] := 0.0850;   mB_Matrix[7,2] := 0.0850;   mB_Matrix[7,3] := 0.0000;  mB_Matrix[7,4] := 0.0000;
    mB_Matrix[8,1] := 0.0000;   mB_Matrix[8,2] := 0.0000;   mB_Matrix[8,3] := 0.0000;  mB_Matrix[8,4] := 0.0000;

    (* Matrix Bw (8x2 Disturbance matrix) *)
    mBw_Matrix[1,1] := 0.0150; mBw_Matrix[1,2] := 0.0250;
    mBw_Matrix[2,1] := 0.0850; mBw_Matrix[2,2] := 0.0000;
    mBw_Matrix[3,1] := 0.0000; mBw_Matrix[3,2] := 0.0000;
    mBw_Matrix[4,1] := 0.0000; mBw_Matrix[4,2] := 0.0000;
    mBw_Matrix[5,1] := 0.0200; mBw_Matrix[5,2] := 0.0450;
    mBw_Matrix[6,1] := 0.0150; mBw_Matrix[6,2] := 0.0650;
    mBw_Matrix[7,1] := 0.0000; mBw_Matrix[7,2] := 0.0000;
    mBw_Matrix[8,1] := 0.0000; mBw_Matrix[8,2] := 0.0000;

    (* Matrix C (4x8 Output matrix) *)
    mC_Matrix[1,1] := 1.0; mC_Matrix[1,2] := 0.0; mC_Matrix[1,3] := 0.0; mC_Matrix[1,4] := 0.0;
    mC_Matrix[1,5] := 0.0; mC_Matrix[1,6] := 0.0; mC_Matrix[1,7] := 0.0; mC_Matrix[1,8] := 0.0;

    mC_Matrix[2,1] := 0.0; mC_Matrix[2,2] := 1.0; mC_Matrix[2,3] := 0.0; mC_Matrix[2,4] := 0.0;
    mC_Matrix[2,5] := 0.0; mC_Matrix[2,6] := 0.0; mC_Matrix[2,7] := 0.0; mC_Matrix[2,8] := 0.0;

    mC_Matrix[3,1] := 0.0; mC_Matrix[3,2] := 0.0; mC_Matrix[3,3] := 1.0; mC_Matrix[3,4] := 0.0;
    mC_Matrix[3,5] := 0.0; mC_Matrix[3,6] := 0.0; mC_Matrix[3,7] := 0.0; mC_Matrix[3,8] := 0.0;

    mC_Matrix[4,1] := 0.0; mC_Matrix[4,2] := 0.0; mC_Matrix[4,3] := 0.0; mC_Matrix[4,4] := 1.0;
    mC_Matrix[4,5] := 0.0; mC_Matrix[4,6] := 0.0; mC_Matrix[4,7] := 0.0; mC_Matrix[4,8] := 0.0;

    (* Matrix D (4x4 Direct Feedthrough) *)
    FOR iIndex_i := 1 TO 4 DO
        FOR iIndex_j := 1 TO 4 DO
            mD_Matrix[iIndex_i, iIndex_j] := 0.0;
        END_FOR;
    END_FOR;

    (* MPC Cost Matrices: Q_cost (diagonal state error weights) *)
    FOR iIndex_i := 1 TO 8 DO
        FOR iIndex_j := 1 TO 8 DO
            mQ_cost[iIndex_i, iIndex_j] := 0.0;
            mP_term[iIndex_i, iIndex_j] := 0.0;
        END_FOR;
    END_FOR;
    mQ_cost[1,1] := 850.0;  (* High weight on Supply Temp tracking (32.0 C) *)
    mQ_cost[2,2] := 120.0;  (* Return Temp weight *)
    mQ_cost[3,3] := 1200.0; (* Very high weight on DP tracking (1.80 bar) *)
    mQ_cost[4,4] := 25.0;   (* Flow regulation weight *)
    mQ_cost[5,5] := 40.0;
    mQ_cost[6,6] := 30.0;
    mQ_cost[7,7] := 15.0;
    mQ_cost[8,8] := 50.0;

    (* Riccati terminal cost matrix P_term *)
    mP_term[1,1] := 1450.0;
    mP_term[2,2] := 250.0;
    mP_term[3,3] := 2100.0;
    mP_term[4,4] := 55.0;
    mP_term[5,5] := 80.0;
    mP_term[6,6] := 60.0;
    mP_term[7,7] := 30.0;
    mP_term[8,8] := 110.0;

    (* R_cost (actuator energy and slew effort penalties) *)
    FOR iIndex_i := 1 TO 4 DO
        FOR iIndex_j := 1 TO 4 DO
            mR_cost[iIndex_i, iIndex_j] := 0.0;
            mH_hessian[iIndex_i, iIndex_j] := 0.0;
        END_FOR;
    END_FOR;
    mR_cost[1,1] := 0.085; (* Lead pump VFD effort *)
    mR_cost[2,2] := 0.085; (* Lag pump VFD effort *)
    mR_cost[3,3] := 1.250; (* Primary PHE valve movement penalty *)
    mR_cost[4,4] := 0.650; (* Fast bypass valve movement penalty *)

    (* Hessian approximation H = R + B^T * P * B *)
    mH_hessian[1,1] := mR_cost[1,1] + 0.125;
    mH_hessian[2,2] := mR_cost[2,2] + 0.125;
    mH_hessian[3,3] := mR_cost[3,3] + 2.450;
    mH_hessian[4,4] := mR_cost[4,4] + 1.850;

    bMatrices_Initialized := TRUE;
END_IF;

(* --- Populate Current State Vector x --- *)
aState_x[1] := rVoted_TCS_Supply_Temp_C - 32.0; (* Supply Temp error [deg C] *)
aState_x[2] := rVoted_TCS_Return_Temp_C - 44.0; (* Return Temp error [deg C] *)
aState_x[3] := rVoted_TCS_Loop_Diff_Pressure_bar - 1.80; (* DP error [bar] *)
aState_x[4] := rVoted_TCS_Supply_Flow_Lpm - 4000.0; (* Flow error [L/min] *)
aState_x[5] := (rVoted_TCS_Supply_Temp_C + rVoted_FWS_Facility_Supply_Temp_C) * 0.5 - 22.0;
aState_x[6] := rVoted_FWR_Facility_Return_Temp_C - 24.0;
aState_x[7] := (rCDU_Pump1_VFD_Speed_Cmd_RPM * 0.10472) - 260.0; (* rad/s *)
aState_x[8] := rThermal_Buffer_Tank_Core_Temp_C - 20.0;

(* --- Disturbances w --- *)
aDisturb_w[1] := rIT_Cluster_Thermal_Load_MW - 40.0; (* Load surge deviation *)
aDisturb_w[2] := rVoted_FWS_Facility_Supply_Temp_C - 12.0; (* Chilled water temp deviation *)

(* --- Receding-Horizon Next State Propagation: x[k+1] = A*x + B*u + Bw*w --- *)
FOR iIndex_i := 1 TO 8 DO
    aState_x_next[iIndex_i] := 0.0;
    FOR iIndex_j := 1 TO 8 DO
        aState_x_next[iIndex_i] := aState_x_next[iIndex_i] + (mA_Matrix[iIndex_i, iIndex_j] * aState_x[iIndex_j]);
    END_FOR;
    FOR iIndex_j := 1 TO 4 DO
        aState_x_next[iIndex_i] := aState_x_next[iIndex_i] + (mB_Matrix[iIndex_i, iIndex_j] * aControl_u[iIndex_j]);
    END_FOR;
    FOR iIndex_j := 1 TO 2 DO
        aState_x_next[iIndex_i] := aState_x_next[iIndex_i] + (mBw_Matrix[iIndex_i, iIndex_j] * aDisturb_w[iIndex_j]);
    END_FOR;
END_FOR;

(* --- Quadratic Cost Gradient Vector Evaluation: g = H*u + B^T * Q * x --- *)
aGrad_g[1] := (mH_hessian[1,1] * aControl_u[1]) + (mB_Matrix[1,1] * mQ_cost[1,1] * aState_x[1]) + (mB_Matrix[3,1] * mQ_cost[3,3] * aState_x[3]);
aGrad_g[2] := (mH_hessian[2,2] * aControl_u[2]) + (mB_Matrix[1,2] * mQ_cost[1,1] * aState_x[1]) + (mB_Matrix[3,2] * mQ_cost[3,3] * aState_x[3]);
aGrad_g[3] := (mH_hessian[3,3] * aControl_u[3]) + (mB_Matrix[1,3] * mQ_cost[1,1] * aState_x[1]) + (mB_Matrix[5,3] * mQ_cost[5,5] * aState_x[5]);
aGrad_g[4] := (mH_hessian[4,4] * aControl_u[4]) + (mB_Matrix[1,4] * mQ_cost[1,1] * aState_x[1]) + (mB_Matrix[3,4] * mQ_cost[3,3] * aState_x[3]);

(* Gradient Descent Step: delta_u = -alpha * g *)
aDelta_u[1] := -0.045 * aGrad_g[1];
aDelta_u[2] := -0.045 * aGrad_g[2];
aDelta_u[3] := -0.020 * aGrad_g[3];
aDelta_u[4] := -0.025 * aGrad_g[4];

(* Compute unconstrained optimal control vector *)
aControl_u_opt[1] := aControl_u[1] + aDelta_u[1];
aControl_u_opt[2] := aControl_u[2] + aDelta_u[2];
aControl_u_opt[3] := aControl_u[3] + aDelta_u[3];
aControl_u_opt[4] := aControl_u[4] + aDelta_u[4];
"""

def get_phase5_fsm():
    return """(* ========================================================================= *)
(* === PHASE 5: MULTI-STAGE CASE FINITE STATE MACHINE (FSM) ================ *)
(* ========================================================================= *)
(*
   12 Discrete Operational States:
     State 0:  CDU_STANDBY_OFFLINE
     State 1:  COOLANT_DE_AERATION_CIRCULATION
     State 2:  FACILITY_LOOP_PHE_PRECOOL
     State 3:  PRIMARY_SECONDARY_SYNC
     State 4:  NORMAL_AI_WORKLOAD_TRACKING_40MW
     State 5:  PUMP_AUTO_LEAD_LAG_FAILOVER
     State 6:  CHEMICAL_DOSING_AND_FILTRATION
     State 7:  PEAK_DEMAND_VFD_BOOST
     State 8:  FACILITY_OUTAGE_THERMAL_BUFFER_RIDE
     State 9:  CONTROLLED_DRAIN_AND_FLUSH
     State 10: LEAK_ZONE_EMERGENCY_ISOLATION
     State 11: EMERGENCY_ESTOP_CDU_TRIP
*)

tState_Dwell_Timer_Sec := tState_Dwell_Timer_Sec + 0.050;

CASE nFSM_State OF

    0: (* CDU_STANDBY_OFFLINE *)
        rTarget_Lead_RPM   := 0.0;
        rTarget_Lag_RPM    := 0.0;
        rTarget_Valve_Pct  := 0.0;
        rTarget_Bypass_Pct := 100.0;
        bTCS_Fast_Isolation_Valve_Trip      := FALSE;
        bThermal_Buffer_Discharge_Valve_Cmd := FALSE;
        bChemical_Dosing_Pump_Cmd           := FALSE;
        bDeaerator_Vacuum_Vent_Solenoid     := FALSE;
        bAI_Cluster_Emergency_Thermal_Throttling_Req := FALSE;

        IF bCDU_System_Enable AND bEmergencyStop_Circuit_NC THEN
            nFSM_PreviousState := nFSM_State;
            nFSM_State := 1; (* Transition to De-Aeration Circulation *)
            tState_Dwell_Timer_Sec := 0.0;
        END_IF;

    1: (* COOLANT_DE_AERATION_CIRCULATION *)
        (* Run lead pump at low speed (1200 rpm) to dislodge micro-bubbles *)
        rTarget_Lead_RPM   := 1200.0;
        rTarget_Lag_RPM    := 0.0;
        rTarget_Valve_Pct  := 10.0;
        rTarget_Bypass_Pct := 80.0;
        bDeaerator_Vacuum_Vent_Solenoid := TRUE;

        tDeaeration_Cycle_Sec := tDeaeration_Cycle_Sec + 0.050;
        IF (tDeaeration_Cycle_Sec > 30.0) AND (rVoted_Dissolved_Oxygen_ppb < 25.0) THEN
            bDeaerator_Vacuum_Vent_Solenoid := FALSE;
            nFSM_PreviousState := nFSM_State;
            nFSM_State := 2; (* Transition to Facility Pre-Cool *)
            tState_Dwell_Timer_Sec := 0.0;
        END_IF;

    2: (* FACILITY_LOOP_PHE_PRECOOL *)
        (* Modulate PHE facility valve to chill titanium plates before heavy loop load *)
        rTarget_Lead_RPM   := 1800.0;
        rTarget_Lag_RPM    := 0.0;
        rTarget_Valve_Pct  := 45.0;
        rTarget_Bypass_Pct := 50.0;

        IF (rVoted_TCS_Supply_Temp_C <= 33.0) AND (tState_Dwell_Timer_Sec > 15.0) THEN
            nFSM_PreviousState := nFSM_State;
            nFSM_State := 3; (* Transition to Primary/Secondary Sync *)
            tState_Dwell_Timer_Sec := 0.0;
        END_IF;

    3: (* PRIMARY_SECONDARY_SYNC *)
        (* Synchronize thermal balance and ramp pump to operating baseline 2600 rpm *)
        rTarget_Lead_RPM   := 2600.0;
        rTarget_Lag_RPM    := 0.0;
        rTarget_Valve_Pct  := 55.0;
        rTarget_Bypass_Pct := 20.0;

        IF (ABS(rVoted_TCS_Loop_Diff_Pressure_bar - 1.80) <= 0.15) AND 
           (ABS(rVoted_TCS_Supply_Temp_C - 32.0) <= 0.8) AND 
           (tState_Dwell_Timer_Sec > 10.0) THEN
            nFSM_PreviousState := nFSM_State;
            nFSM_State := 4; (* Transition to Normal AI Workload Tracking *)
            tState_Dwell_Timer_Sec := 0.0;
        END_IF;

    4: (* NORMAL_AI_WORKLOAD_TRACKING_40MW *)
        (* Full MPC Closed-Loop Active: dynamic lead pump RPM and PHE modulating valve *)
        rTarget_Lead_RPM := aControl_u_opt[1];
        IF (rTarget_Lead_RPM < 1500.0) THEN rTarget_Lead_RPM := 1500.0; END_IF;
        IF (rTarget_Lead_RPM > 3200.0) THEN rTarget_Lead_RPM := 3200.0; END_IF;

        rTarget_Lag_RPM    := 0.0; (* Lag pump on hot standby *)
        rTarget_Valve_Pct  := aControl_u_opt[3];
        IF (rTarget_Valve_Pct < 5.0)   THEN rTarget_Valve_Pct := 5.0;   END_IF;
        IF (rTarget_Valve_Pct > 100.0) THEN rTarget_Valve_Pct := 100.0; END_IF;

        rTarget_Bypass_Pct := aControl_u_opt[4];
        IF (rTarget_Bypass_Pct < 0.0)  THEN rTarget_Bypass_Pct := 0.0;  END_IF;
        IF (rTarget_Bypass_Pct > 50.0) THEN rTarget_Bypass_Pct := 50.0; END_IF;

        bThermal_Buffer_Discharge_Valve_Cmd := FALSE;
        bTCS_Fast_Isolation_Valve_Trip      := FALSE;

        (* Interlock: Peak IT Load Boost Trigger (> 38 MW or DP deficit) *)
        IF (rIT_Cluster_Thermal_Load_MW > 38.0) OR (rVoted_TCS_Loop_Diff_Pressure_bar < 1.60) THEN
            nFSM_PreviousState := nFSM_State;
            nFSM_State := 7; (* Transition to Peak Demand VFD Boost *)
            tState_Dwell_Timer_Sec := 0.0;
        (* Interlock: Lead Pump Fault / Cavitation Trip -> Auto Failover *)
        ELSIF bCavitation_Trip_Latched OR (ZT_CDU_PUMP1_VFD_RPM_301A < 800.0 AND rTarget_Lead_RPM > 2000.0) THEN
            nFSM_PreviousState := nFSM_State;
            nFSM_State := 5; (* Transition to Lead-Lag Failover *)
            tState_Dwell_Timer_Sec := 0.0;
        (* Interlock: Chemical inhibitor top-up required *)
        ELSIF (rVoted_Dissolved_Oxygen_ppb > 20.0) OR (rVoted_Glycol_Concentration_Pct < 23.5) THEN
            nFSM_PreviousState := nFSM_State;
            nFSM_State := 6; (* Transition to Chemical Dosing *)
            tState_Dwell_Timer_Sec := 0.0;
        (* Interlock: Facility Chiller Plant Outage -> Engage Thermal Buffer *)
        ELSIF (rVoted_FWS_Facility_Flow_m3h < 25.0) OR (rVoted_FWS_Facility_Supply_Temp_C > 26.0) THEN
            nFSM_PreviousState := nFSM_State;
            nFSM_State := 8; (* Transition to Thermal Buffer Ride-Through *)
            tState_Dwell_Timer_Sec := 0.0;
        END_IF;

    5: (* PUMP_AUTO_LEAD_LAG_FAILOVER *)
        (* Bumpless Transfer: Spin up lag pump (Pump 2) to 2800 rpm while ramping down lead *)
        tFailover_Ramp_Timer_Sec := tFailover_Ramp_Timer_Sec + 0.050;
        rTarget_Lead_RPM := 0.0;
        rTarget_Lag_RPM  := 2850.0;
        rTarget_Valve_Pct := 65.0;

        IF (tFailover_Ramp_Timer_Sec > 3.0) AND (ZT_CDU_PUMP2_VFD_RPM_302A > 2600.0) THEN
            bLeadPump_Active := 2; (* Switch lead index to pump 2 *)
            tFailover_Ramp_Timer_Sec := 0.0;
            nFSM_PreviousState := nFSM_State;
            nFSM_State := 4; (* Return to Normal Tracking under Pump 2 *)
            tState_Dwell_Timer_Sec := 0.0;
        END_IF;

    6: (* CHEMICAL_DOSING_AND_FILTRATION *)
        (* Modulate dosing pump to inject corrosion inhibitor until DO drops *)
        rTarget_Lead_RPM  := 2400.0;
        rTarget_Lag_RPM   := 0.0;
        rTarget_Valve_Pct := 50.0;
        bChemical_Dosing_Pump_Cmd := TRUE;

        tChemical_Dosing_Pulse_Sec := tChemical_Dosing_Pulse_Sec + 0.050;
        IF (tChemical_Dosing_Pulse_Sec > 20.0) OR (rVoted_Dissolved_Oxygen_ppb < 15.0) THEN
            bChemical_Dosing_Pump_Cmd := FALSE;
            tChemical_Dosing_Pulse_Sec := 0.0;
            nFSM_PreviousState := nFSM_State;
            nFSM_State := 4; (* Return to Normal Tracking *)
            tState_Dwell_Timer_Sec := 0.0;
        END_IF;

    7: (* PEAK_DEMAND_VFD_BOOST *)
        (* Both Lead and Lag pumps active simultaneously to deliver up to 4,800 L/min *)
        rTarget_Lead_RPM   := 3300.0;
        rTarget_Lag_RPM    := 2200.0;
        rTarget_Valve_Pct  := 95.0;
        rTarget_Bypass_Pct := 0.0;

        IF (rIT_Cluster_Thermal_Load_MW <= 36.0) AND (rVoted_TCS_Loop_Diff_Pressure_bar >= 1.80) AND (tState_Dwell_Timer_Sec > 30.0) THEN
            nFSM_PreviousState := nFSM_State;
            nFSM_State := 4; (* Return to single lead pump normal tracking *)
            tState_Dwell_Timer_Sec := 0.0;
        END_IF;

    8: (* FACILITY_OUTAGE_THERMAL_BUFFER_RIDE *)
        (* Chiller power lost: Open 120,000L cold buffer reservoir valve to absorb 40 MW *)
        bThermal_Buffer_Discharge_Valve_Cmd := TRUE;
        rTarget_Lead_RPM   := 2900.0;
        rTarget_Lag_RPM    := 0.0;
        rTarget_Valve_Pct  := 0.0; (* Chiller loop isolated *)
        rTarget_Bypass_Pct := 0.0;

        (* Assert IT cluster throttling request if remaining autonomy drops below 30s *)
        IF (rThermal_Buffer_RideThrough_Sec_Remaining < 30.0) THEN
            bAI_Cluster_Emergency_Thermal_Throttling_Req := TRUE;
        END_IF;

        (* If facility chilled water is restored, recharge and return to normal *)
        IF (rVoted_FWS_Facility_Flow_m3h > 150.0) AND (rVoted_FWS_Facility_Supply_Temp_C < 16.0) THEN
            bThermal_Buffer_Discharge_Valve_Cmd := FALSE;
            bAI_Cluster_Emergency_Thermal_Throttling_Req := FALSE;
            nFSM_PreviousState := nFSM_State;
            nFSM_State := 4;
            tState_Dwell_Timer_Sec := 0.0;
        END_IF;

    9: (* CONTROLLED_DRAIN_AND_FLUSH *)
        (* Controlled shutdown and loop drainage *)
        rTarget_Lead_RPM   := 500.0;
        rTarget_Lag_RPM    := 0.0;
        rTarget_Valve_Pct  := 0.0;
        rTarget_Bypass_Pct := 100.0;
        bThermal_Buffer_Discharge_Valve_Cmd := FALSE;

        IF (tState_Dwell_Timer_Sec > 60.0) THEN
            nFSM_PreviousState := nFSM_State;
            nFSM_State := 0; (* Standby Offline *)
            tState_Dwell_Timer_Sec := 0.0;
        END_IF;

    10: (* LEAK_ZONE_EMERGENCY_ISOLATION *)
        (* Catastrophic Coolant Breach: Trip isolation valves < 100 ms and stop pumps *)
        rTarget_Lead_RPM   := 0.0;
        rTarget_Lag_RPM    := 0.0;
        rTarget_Valve_Pct  := 0.0;
        rTarget_Bypass_Pct := 0.0;
        bTCS_Fast_Isolation_Valve_Trip := TRUE;
        bAI_Cluster_Emergency_Thermal_Throttling_Req := TRUE;

        IF bMaster_Alarm_Reset AND (rVoted_Leak_Rope_Resistance_Ohm > 700.0) THEN
            bTCS_Fast_Isolation_Valve_Trip := FALSE;
            bAI_Cluster_Emergency_Thermal_Throttling_Req := FALSE;
            nFSM_PreviousState := nFSM_State;
            nFSM_State := 0; (* Offline Standby awaiting operator inspection *)
            tState_Dwell_Timer_Sec := 0.0;
        END_IF;

    11: (* EMERGENCY_ESTOP_CDU_TRIP *)
        (* Hardware E-Stop open: Hard shutdown of all actuators *)
        rTarget_Lead_RPM   := 0.0;
        rTarget_Lag_RPM    := 0.0;
        rTarget_Valve_Pct  := 0.0;
        rTarget_Bypass_Pct := 0.0;
        bTCS_Fast_Isolation_Valve_Trip      := TRUE;
        bThermal_Buffer_Discharge_Valve_Cmd := FALSE;
        bChemical_Dosing_Pump_Cmd           := FALSE;
        bDeaerator_Vacuum_Vent_Solenoid     := FALSE;
        bAI_Cluster_Emergency_Thermal_Throttling_Req := TRUE;

        IF bEmergencyStop_Circuit_NC AND bMaster_Alarm_Reset THEN
            bTCS_Fast_Isolation_Valve_Trip := FALSE;
            bAI_Cluster_Emergency_Thermal_Throttling_Req := FALSE;
            nFSM_PreviousState := nFSM_State;
            nFSM_State := 0;
            tState_Dwell_Timer_Sec := 0.0;
        END_IF;

END_CASE;

(* --- Priority Interlocks Overriding FSM State --- *)
IF NOT bEmergencyStop_Circuit_NC THEN
    nFSM_State := 11; (* Direct jump to E-Stop Trip *)
ELSIF bLeak_Fast_Trip_Latched OR (rVoted_Leak_Rope_Resistance_Ohm < 150.0) THEN
    nFSM_State := 10; (* Direct jump to Leak Isolation Trip *)
END_IF;

(* Update state diagnostic output registers *)
wCDU_FSM_Current_State  := INT_TO_WORD(nFSM_State);
wCDU_FSM_Previous_State := INT_TO_WORD(nFSM_PreviousState);

(* --- Slew Rate Limiter for Actuators (Pumps: max 250 rpm/s, Valves: max 15 %/s) --- *)
rRamp_Rate_RPM_per_Sec := 250.0 * 0.050; (* 12.5 rpm per 50 ms cycle *)
IF (rCDU_Pump1_VFD_Speed_Cmd_RPM < rTarget_Lead_RPM) THEN
    rCDU_Pump1_VFD_Speed_Cmd_RPM := rCDU_Pump1_VFD_Speed_Cmd_RPM + rRamp_Rate_RPM_per_Sec;
    IF (rCDU_Pump1_VFD_Speed_Cmd_RPM > rTarget_Lead_RPM) THEN rCDU_Pump1_VFD_Speed_Cmd_RPM := rTarget_Lead_RPM; END_IF;
ELSIF (rCDU_Pump1_VFD_Speed_Cmd_RPM > rTarget_Lead_RPM) THEN
    rCDU_Pump1_VFD_Speed_Cmd_RPM := rCDU_Pump1_VFD_Speed_Cmd_RPM - rRamp_Rate_RPM_per_Sec;
    IF (rCDU_Pump1_VFD_Speed_Cmd_RPM < rTarget_Lead_RPM) THEN rCDU_Pump1_VFD_Speed_Cmd_RPM := rTarget_Lead_RPM; END_IF;
END_IF;

IF (rCDU_Pump2_VFD_Speed_Cmd_RPM < rTarget_Lag_RPM) THEN
    rCDU_Pump2_VFD_Speed_Cmd_RPM := rCDU_Pump2_VFD_Speed_Cmd_RPM + rRamp_Rate_RPM_per_Sec;
    IF (rCDU_Pump2_VFD_Speed_Cmd_RPM > rTarget_Lag_RPM) THEN rCDU_Pump2_VFD_Speed_Cmd_RPM := rTarget_Lag_RPM; END_IF;
ELSIF (rCDU_Pump2_VFD_Speed_Cmd_RPM > rTarget_Lag_RPM) THEN
    rCDU_Pump2_VFD_Speed_Cmd_RPM := rCDU_Pump2_VFD_Speed_Cmd_RPM - rRamp_Rate_RPM_per_Sec;
    IF (rCDU_Pump2_VFD_Speed_Cmd_RPM < rTarget_Lag_RPM) THEN rCDU_Pump2_VFD_Speed_Cmd_RPM := rTarget_Lag_RPM; END_IF;
END_IF;

(* Valve slew rate: 0.75% per 50 ms *)
IF (rPHE_Facility_Modulating_Valve_Cmd_Pct < rTarget_Valve_Pct) THEN
    rPHE_Facility_Modulating_Valve_Cmd_Pct := rPHE_Facility_Modulating_Valve_Cmd_Pct + 0.75;
    IF (rPHE_Facility_Modulating_Valve_Cmd_Pct > rTarget_Valve_Pct) THEN rPHE_Facility_Modulating_Valve_Cmd_Pct := rTarget_Valve_Pct; END_IF;
ELSIF (rPHE_Facility_Modulating_Valve_Cmd_Pct > rTarget_Valve_Pct) THEN
    rPHE_Facility_Modulating_Valve_Cmd_Pct := rPHE_Facility_Modulating_Valve_Cmd_Pct - 0.75;
    IF (rPHE_Facility_Modulating_Valve_Cmd_Pct < rTarget_Valve_Pct) THEN rPHE_Facility_Modulating_Valve_Cmd_Pct := rTarget_Valve_Pct; END_IF;
END_IF;

IF (rPHE_Bypass_3Way_Valve_Cmd_Pct < rTarget_Bypass_Pct) THEN
    rPHE_Bypass_3Way_Valve_Cmd_Pct := rPHE_Bypass_3Way_Valve_Cmd_Pct + 1.25;
    IF (rPHE_Bypass_3Way_Valve_Cmd_Pct > rTarget_Bypass_Pct) THEN rPHE_Bypass_3Way_Valve_Cmd_Pct := rTarget_Bypass_Pct; END_IF;
ELSIF (rPHE_Bypass_3Way_Valve_Cmd_Pct > rTarget_Bypass_Pct) THEN
    rPHE_Bypass_3Way_Valve_Cmd_Pct := rPHE_Bypass_3Way_Valve_Cmd_Pct - 1.25;
    IF (rPHE_Bypass_3Way_Valve_Cmd_Pct < rTarget_Bypass_Pct) THEN rPHE_Bypass_3Way_Valve_Cmd_Pct := rTarget_Bypass_Pct; END_IF;
END_IF;
"""

def get_phase6_alarms():
    return """(* ========================================================================= *)
(* === PHASE 6: ISA-18.2 ALARMS, FAST TRIPS & DIAGNOSTIC WORD PACKING ===== *)
(* ========================================================================= *)
(*
   ISA-18.2 Compliant Multi-Tier Alarm Matrix:
     - Priority 1 (Critical Safety Trips): dwISA_Alarm_Word_1_Critical
     - Priority 2 (Process Warnings):      dwISA_Alarm_Word_2_Warning
     - TMR Degradation Status:             dwTMR_Discrepancy_Word
     - Automation Status Word:             wAutomationStatusWord
*)

(* --- 1. Rate of Change (ROC) Calculations --- *)
rROC_DP_bar_per_s := (rVoted_TCS_Loop_Diff_Pressure_bar - rPrev_Voted_DP) / 0.050;
rROC_SupplyTemp_degC_per_s := (rVoted_TCS_Supply_Temp_C - rPrev_Voted_SupplyTemp) / 0.050;
rROC_LeakResistance_Ohm_per_s := (rVoted_Leak_Rope_Resistance_Ohm - rPrev_Voted_LeakResistance) / 0.050;

rPrev_Voted_DP := rVoted_TCS_Loop_Diff_Pressure_bar;
rPrev_Voted_SupplyTemp := rVoted_TCS_Supply_Temp_C;
rPrev_Voted_LeakResistance := rVoted_Leak_Rope_Resistance_Ohm;

(* --- 2. Sub-100 ms Leak Detection & Fast Trip Interlock --- *)
IF (rVoted_Leak_Rope_Resistance_Ohm < 150.0) OR (rROC_LeakResistance_Ohm_per_s < -500.0) THEN
    tLeak_Trip_Debounce_Time := tLeak_Trip_Debounce_Time + 0.050;
    IF (tLeak_Trip_Debounce_Time >= 0.050) THEN (* 1 cycle latency = 50 ms *)
        bLeak_Fast_Trip_Latched := TRUE;
        bTCS_Fast_Isolation_Valve_Trip := TRUE;
    END_IF;
ELSE
    tLeak_Trip_Debounce_Time := 0.0;
END_IF;

IF bMaster_Alarm_Reset THEN
    bLeak_Fast_Trip_Latched := FALSE;
    bCavitation_Trip_Latched := FALSE;
END_IF;

(* --- 3. Pump Cavitation Detection (Low Suction Pressure vs Vapor Pressure) --- *)
IF (rVoted_TCS_Return_Pressure_bar < 0.85) AND (rCDU_Pump1_VFD_Speed_Cmd_RPM > 1800.0) THEN
    tCavitation_Debounce_Time := tCavitation_Debounce_Time + 0.050;
    IF (tCavitation_Debounce_Time > 0.200) THEN
        bCavitation_Trip_Latched := TRUE;
    END_IF;
ELSE
    tCavitation_Debounce_Time := 0.0;
END_IF;

(* --- 4. Evaluate Priority 1 Critical Alarms (dwISA_Alarm_Word_1_Critical) --- *)
dwISA_Alarm_Word_1_Critical := 16#00000000;

(* Bit 0: Leak Fast Trip Actuated *)
IF bLeak_Fast_Trip_Latched THEN dwISA_Alarm_Word_1_Critical := dwISA_Alarm_Word_1_Critical OR 16#00000001; END_IF;

(* Bit 1: TCS Supply Temp HI_HI (> 36.0 deg C) *)
IF (rVoted_TCS_Supply_Temp_C > 36.0) THEN dwISA_Alarm_Word_1_Critical := dwISA_Alarm_Word_1_Critical OR 16#00000002; END_IF;

(* Bit 2: TCS Loop Differential Pressure HI_HI (> 2.40 bar) *)
IF (rVoted_TCS_Loop_Diff_Pressure_bar > 2.40) THEN dwISA_Alarm_Word_1_Critical := dwISA_Alarm_Word_1_Critical OR 16#00000004; END_IF;

(* Bit 3: TCS Loop Differential Pressure LO_LO (< 1.20 bar) *)
IF (rVoted_TCS_Loop_Diff_Pressure_bar < 1.20) THEN dwISA_Alarm_Word_1_Critical := dwISA_Alarm_Word_1_Critical OR 16#00000008; END_IF;

(* Bit 4: GPU Silicon Junction Temp HI_HI (> 88.0 deg C) -> Trigger Throttling *)
IF (rObserved_GPU_Junction_Temp_C > 88.0) OR (rAI_Server_Rack_Hotspot_Max_Temp_C > 88.0) THEN
    dwISA_Alarm_Word_1_Critical := dwISA_Alarm_Word_1_Critical OR 16#00000010;
    bAI_Cluster_Emergency_Thermal_Throttling_Req := TRUE;
END_IF;

(* Bit 5: Thermal Buffer Reservoir Level LO_LO (< 40.0%) *)
IF (rVoted_Buffer_Tank_Level_Pct < 40.0) THEN dwISA_Alarm_Word_1_Critical := dwISA_Alarm_Word_1_Critical OR 16#00000020; END_IF;

(* Bit 6: Facility Chilled Water Total Flow Loss (< 20.0 m3/h) *)
IF (rVoted_FWS_Facility_Flow_m3h < 20.0) AND (nFSM_State = 4) THEN dwISA_Alarm_Word_1_Critical := dwISA_Alarm_Word_1_Critical OR 16#00000040; END_IF;

(* Bit 7: Hardware Emergency Stop Circuit Open *)
IF NOT bEmergencyStop_Circuit_NC THEN dwISA_Alarm_Word_1_Critical := dwISA_Alarm_Word_1_Critical OR 16#00000080; END_IF;

(* Bit 8: Pump Cavitation / Suction Depressurization Latched *)
IF bCavitation_Trip_Latched THEN dwISA_Alarm_Word_1_Critical := dwISA_Alarm_Word_1_Critical OR 16#00000100; END_IF;

(* Bit 9: TCS Return Temp HI_HI (> 52.0 deg C) *)
IF (rVoted_TCS_Return_Temp_C > 52.0) THEN dwISA_Alarm_Word_1_Critical := dwISA_Alarm_Word_1_Critical OR 16#00000200; END_IF;

(* Bit 10: Thermal Storage Buffer Autonomy Exhausted (< 15 s) *)
IF (rThermal_Buffer_RideThrough_Sec_Remaining < 15.0) AND (nFSM_State = 8) THEN
    dwISA_Alarm_Word_1_Critical := dwISA_Alarm_Word_1_Critical OR 16#00000400;
END_IF;

(* --- 5. Evaluate Priority 2 Warning Alarms (dwISA_Alarm_Word_2_Warning) --- *)
dwISA_Alarm_Word_2_Warning := 16#00000000;

(* Bit 0: Leak Sensing Rope Pre-Alarm (Resistance < 500.0 Ohm) *)
IF (rVoted_Leak_Rope_Resistance_Ohm < 500.0) THEN dwISA_Alarm_Word_2_Warning := dwISA_Alarm_Word_2_Warning OR 16#00000001; END_IF;

(* Bit 1: TCS Supply Temp HI (> 34.0 deg C) *)
IF (rVoted_TCS_Supply_Temp_C > 34.0) THEN dwISA_Alarm_Word_2_Warning := dwISA_Alarm_Word_2_Warning OR 16#00000002; END_IF;

(* Bit 2: TCS Supply Temp LO (< 30.0 deg C) *)
IF (rVoted_TCS_Supply_Temp_C < 30.0) THEN dwISA_Alarm_Word_2_Warning := dwISA_Alarm_Word_2_Warning OR 16#00000004; END_IF;

(* Bit 3: TCS Loop Differential Pressure HI (> 2.10 bar) *)
IF (rVoted_TCS_Loop_Diff_Pressure_bar > 2.10) THEN dwISA_Alarm_Word_2_Warning := dwISA_Alarm_Word_2_Warning OR 16#00000008; END_IF;

(* Bit 4: TCS Loop Differential Pressure LO (< 1.50 bar) *)
IF (rVoted_TCS_Loop_Diff_Pressure_bar < 1.50) THEN dwISA_Alarm_Word_2_Warning := dwISA_Alarm_Word_2_Warning OR 16#00000010; END_IF;

(* Bit 5: Propylene Glycol Concentration Deviation (< 22.0% or > 28.0%) *)
IF (rVoted_Glycol_Concentration_Pct < 22.0) OR (rVoted_Glycol_Concentration_Pct > 28.0) THEN
    dwISA_Alarm_Word_2_Warning := dwISA_Alarm_Word_2_Warning OR 16#00000020;
END_IF;

(* Bit 6: Coolant Dissolved Oxygen HI (> 20.0 ppb - Corrosion Risk) *)
IF (rVoted_Dissolved_Oxygen_ppb > 20.0) THEN dwISA_Alarm_Word_2_Warning := dwISA_Alarm_Word_2_Warning OR 16#00000040; END_IF;

(* Bit 7: Plate Heat Exchanger Micro-Fouling Resistance Warning (> 0.008 m2*K/kW) *)
IF (rPHE_Fouling_Resistance_m2K_kW > 0.008) THEN dwISA_Alarm_Word_2_Warning := dwISA_Alarm_Word_2_Warning OR 16#00000080; END_IF;

(* Bit 8: Rate of Change Warning: Rapid DP Drop (> 0.20 bar/s) *)
IF (rROC_DP_bar_per_s < -0.20) THEN dwISA_Alarm_Word_2_Warning := dwISA_Alarm_Word_2_Warning OR 16#00000100; END_IF;

(* Bit 9: Thermal Buffer Tank Temperature High in Standby (> 32.0 deg C) *)
IF (rThermal_Buffer_Tank_Core_Temp_C > 32.0) THEN dwISA_Alarm_Word_2_Warning := dwISA_Alarm_Word_2_Warning OR 16#00000200; END_IF;

(* Bit 10: TMR Sensor Triplet Degraded to Dual or Single Channel *)
IF (dwTMR_Discrepancy_Word <> 16#00000000) THEN dwISA_Alarm_Word_2_Warning := dwISA_Alarm_Word_2_Warning OR 16#00000400; END_IF;

(* --- 6. Pack Automation Status Word (wAutomationStatusWord) --- *)
wAutomationStatusWord := 16#0000;
IF bCDU_System_Enable                             THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0001; END_IF;
IF (nFSM_State = 4)                               THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0002; END_IF;
IF (rCDU_Pump1_VFD_Speed_Cmd_RPM > 100.0)         THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0004; END_IF;
IF (rCDU_Pump2_VFD_Speed_Cmd_RPM > 100.0)         THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0008; END_IF;
IF bThermal_Buffer_Discharge_Valve_Cmd            THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0010; END_IF;
IF bDeaerator_Vacuum_Vent_Solenoid                THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0020; END_IF;
IF bChemical_Dosing_Pump_Cmd                      THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0040; END_IF;
IF (dwTMR_Discrepancy_Word = 16#00000000)         THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0080; END_IF;
IF (rVoted_FWS_Facility_Flow_m3h > 50.0)          THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0100; END_IF;
IF bMatrices_Initialized                          THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0200; END_IF;
IF bEmergencyStop_Circuit_NC                      THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0400; END_IF;
IF bAI_Cluster_Emergency_Thermal_Throttling_Req   THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0800; END_IF;

END_FUNCTION_BLOCK
"""

print("Control module (Phases 4-6) configured.")
