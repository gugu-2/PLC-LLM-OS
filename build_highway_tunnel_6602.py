import json
import uuid
import os
import subprocess

# Python script to build FB_HighwayTunnel_Ventilation_JetFanFireDeluge
# Highway Tunnel Environmental Ventilation, Fire Deluge & Jet Fan Clusters
# Ultra-Dense, Exhaustive, Mathematically Complete IEC 61131-3 Structured Text

prompt = """Generate a high-density, mathematically rigorous IEC 61131-3 Structured Text FUNCTION_BLOCK FB_HighwayTunnel_Ventilation_JetFanFireDeluge for a Highway Tunnel Environmental Ventilation, Fire Deluge & Jet Fan Clusters system.

The block must control:
1. Discrete State-Space Matrices (A, B, C, D) modeling longitudinal airflow velocity, piston effect from moving vehicles, and smoke spread buoyancy dynamics: x_{k+1} = A*x_k + B*u_k.
2. Receding-Horizon Model Predictive Control (MPC) quadratic cost formulation for reversible ceiling jet fan cluster staging and variable frequency drive (VFD) power minimization.
3. 2oo3 TMR voting logic for CO/NOx gas optical sensors, visibility transmissometers, and linear heat detection cables.
4. Emergency fire mode sequencing: aerodynamic smoke backlayering prevention (Wu & Bakar critical velocity equation), motorized fire damper isolation, and zonal deluge water-mist activation.
5. Pedestrian cross-passage escape route positive overpressure differential protection (Delta P >= 50 Pa) to prevent toxic smoke ingress into evacuation passages.
6. Jet fan high-temperature F400 thermal rating monitoring, motor winding PT100 protection, and automated Variable Message Sign (VMS) evacuation signaling.
7. Multi-stage Finite State Machine (ECO_VENTILATION_NATURAL, TRAFFIC_PEAK_CO_SCRUBBING, VISIBILITY_DEGRADED_FOG_SMOG, EMERGENCY_FIRE_SMOKE_CONTAIN, ZONAL_DELUGE_SUPPRESSION, POST_FIRE_SMOKE_PURGE).
8. ISA-18.2 multi-tiered alarm matrix (HH, H, L, LL, rate-of-rise trips, alarm escalation) and 32-bit packed status words.
"""

st_code_parts = []

st_code_parts.append("""FUNCTION_BLOCK FB_HighwayTunnel_Ventilation_JetFanFireDeluge
VAR_INPUT
    (* === TUNNEL AERODYNAMIC & LONGITUDINAL AIRFLOW SIGNALS === *)
    rTunnel_Longitudinal_AirVelocity_m_s: REAL;  (* Ultrasonic anemometer longitudinal velocity [-10.0..+10.0 m/s] *)
    rTunnel_Portal_Barometric_Delta_P_Pa: REAL;  (* Differential barometric wind pressure across portals [-150..+150 Pa] *)
    rTunnel_Portal_Ambient_Temp_degC    : REAL;  (* Outside portal ambient dry-bulb air temperature [deg C] *)
    rTunnel_Interior_Air_Temp_degC      : REAL;  (* Mid-tunnel ceiling interior air temperature [deg C] *)

    (* === TRAFFIC FLOW, SPEED & PISTON EFFECT MONITORING === *)
    rTraffic_Vehicle_Flow_Rate_veh_h    : REAL;  (* Upstream inductive loop vehicle count [0..4500 veh/h] *)
    rTraffic_Average_Speed_km_h         : REAL;  (* Dual-loop transit velocity measurement [0.0..120.0 km/h] *)
    rTraffic_Heavy_Truck_Percentage_Pct : REAL;  (* Percentage of heavy commercial transport vehicles [0..100 %] *)

    (* === 2oo3 TMR CO GAS OPTICAL SENSORS (0..300 ppm) === *)
    rCO_Gas_Concentration_ppm_ChA       : REAL;  (* NDIR optical Carbon Monoxide sensor Channel A [ppm] *)
    rCO_Gas_Concentration_ppm_ChB       : REAL;  (* NDIR optical Carbon Monoxide sensor Channel B [ppm] *)
    rCO_Gas_Concentration_ppm_ChC       : REAL;  (* NDIR optical Carbon Monoxide sensor Channel C [ppm] *)
    rNOx_Gas_Concentration_ppm          : REAL;  (* Nitrogen Oxides chemiluminescence sensor [0.0..50.0 ppm] *)

    (* === 2oo3 TMR VISIBILITY TRANSMISSOMETERS (0..0.05 1/m) === *)
    rVisibility_Extinction_Coeff_k_m1_ChA:REAL;  (* Optical opacity extinction coefficient Channel A [1/m] *)
    rVisibility_Extinction_Coeff_k_m1_ChB:REAL;  (* Optical opacity extinction coefficient Channel B [1/m] *)
    rVisibility_Extinction_Coeff_k_m1_ChC:REAL;  (* Optical opacity extinction coefficient Channel C [1/m] *)

    (* === 2oo3 TMR LINEAR HEAT DETECTION FIBRE-OPTIC CABLE === *)
    rLinear_Heat_Detect_Zone1_Temp_ChA  : REAL;  (* Fibre-optic distributed heat temperature Zone 1 Ch A [deg C] *)
    rLinear_Heat_Detect_Zone1_Temp_ChB  : REAL;  (* Fibre-optic distributed heat temperature Zone 1 Ch B [deg C] *)
    rLinear_Heat_Detect_Zone1_Temp_ChC  : REAL;  (* Fibre-optic distributed heat temperature Zone 1 Ch C [deg C] *)
    rFire_Estimated_Heat_Release_Rate_MW: REAL;  (* Estimated fire convective power release Q_dot [0..150 MW] *)

    (* === ESCAPE CROSS-PASSAGE & SAFETY DOORS === *)
    rCrossPassage_Overpressure_Delta_P_Pa:REAL;  (* Cross-passage differential pressure relative to tunnel bore [Pa] *)
    bCrossPassage_Fire_Door_Open_Switch : BOOL;  (* Escape route fire barrier door status [-] *)

    (* === FIRE DELUGE & SMOKE DAMPER FEEDBACKS === *)
    bDeluge_Pumps_Running_Feedback      : BOOL;  (* High-pressure water-mist deluge pump running feedback [-] *)
    rDeluge_Manifold_Pressure_bar       : REAL;  (* Zonal deluge water delivery manifold pressure [bar] *)
    bSmoke_Damper_Open_Limit_Switch     : BOOL;  (* Ceiling smoke extraction damper full open limit [-] *)

    (* === JET FAN MOTOR THERMAL & VIBRATION HEALTH === *)
    rJetFan_Motor_Max_Winding_T_degC    : REAL;  (* Ceiling jet fan motor stator PT100 temperature [deg C] *)
    rJetFan_Vibration_Velocity_mm_s     : REAL;  (* Jet fan housing radial vibration RMS velocity [mm/s] *)

    (* === SCADA AUTOMATION & SAFETY PERMISSIVES === *)
    bFire_Emergency_Manual_PB           : BOOL;  (* Highway emergency tunnel fire alarm pull-station [-] *)
    bSupervisory_Auto_Enable            : BOOL;  (* SCADA automated environmental run permissive [-] *)
    bManual_Mode_Select                 : BOOL;  (* Maintenance technician manual jog override select [-] *)
    nManual_JetFan_Cluster_Cmd          : INT;   (* Manual jet fan stage count setpoint [0..12] *)
    bReset_Alarms_PB                    : BOOL;  (* Master alarm acknowledgement and reset pushbutton [-] *)
    tScan_Cycle_Time_ms                 : REAL;  (* Automation task execution period [ms] *)
END_VAR

VAR_OUTPUT
    (* === ACTUATOR DISPATCH COMMANDS === *)
    nJetFan_Active_Forward_Clusters     : INT;   (* Count of energized ceiling jet fan pairs blowing forward [0..12] *)
    nJetFan_Active_Reverse_Clusters     : INT;   (* Count of energized ceiling jet fan pairs blowing reverse [0..12] *)
    rJetFan_VFD_Speed_Ref_Pct           : REAL;  (* Speed reference for modulating lead jet fan cluster [30.0..100.0 %] *)
    bZonal_Deluge_WaterMist_Valve_Cmd   : BOOL;  (* High-pressure zonal deluge water-mist solenoid valve [-] *)
    bSmoke_Extraction_Damper_Open_Cmd   : BOOL;  (* Overhead motorized smoke extraction damper actuator [-] *)
    bPortal_Closure_Traffic_Gate_Cmd    : BOOL;  (* Tunnel portal automated entrance vehicle barrier gate [-] *)
    bCrossPassage_Pressurization_Fan_Cmd: BOOL;  (* Egress cross-passage positive overpressure fan command [-] *)
    bVMS_Evacuation_Display_Sign_Cmd    : BOOL;  (* Automated tunnel portal Variable Message Sign evacuation text [-] *)

    (* === AERODYNAMIC & ENVIRONMENTAL METRICS === *)
    rCritical_Anti_Backlayering_Vel_m_s : REAL;  (* Wu & Bakar critical velocity to prevent smoke backlayering [m/s] *)
    rAirflow_Piston_Effect_Thrust_N     : REAL;  (* Net aerodynamic vehicle draft thrust force [N] *)
    rNet_Tunnel_Pressure_Drop_Pa        : REAL;  (* Total longitudinal tunnel aerodynamic head loss [Pa] *)

    (* === 2oo3 TMR VOTED PROCESS VALUES === *)
    rCO_Concentration_Voted_ppm         : REAL;  (* 2oo3 TMR voted Carbon Monoxide concentration [ppm] *)
    rVisibility_Extinction_Voted_k_m1   : REAL;  (* 2oo3 TMR voted optical extinction coefficient [1/m] *)
    rHeat_Detect_Zone1_Voted_degC       : REAL;  (* 2oo3 TMR voted linear heat temperature [deg C] *)

    (* === SEQUENCER, SAFETY & DIAGNOSTIC PACKETS === *)
    eCurrent_State                      : INT;   (* FSM State: 1=ECO, 2=PEAK_CO, 3=SMOG, 4=SMOKE_CONTAIN, 5=DELUGE, 6=PURGE *)
    bTunnel_Fire_Confirmed              : BOOL;  (* Confirmed fire incident latch [-] *)
    bSmoke_Backlayering_Risk            : BOOL;  (* Airspeed below critical velocity during fire [-] *)
    bCrossPassage_Depressurized_Warning : BOOL;  (* Cross-passage differential pressure below 50 Pa [-] *)
    dwAlarm_Word_Critical               : DWORD; (* ISA-18.2 Priority 1 / Emergency Fire Trips *)
    dwAlarm_Word_Warning                : DWORD; (* ISA-18.2 Priority 2 / Environmental Warnings & TMR *)
    dwTunnel_Status_Word                : DWORD; (* Tunnel operational status, gate status, and fan telemetry *)
END_VAR

VAR
    (* === 2oo3 TRIPLE MODULAR REDUNDANCY INTERNAL VOTING STRUCTURES === *)
    (* Carbon Monoxide Optical Sensors *)
    bCO_Discrepancy_AB                  : BOOL;
    bCO_Discrepancy_BC                  : BOOL;
    bCO_Discrepancy_CA                  : BOOL;
    rCO_Discrepancy_Timer_s             : REAL;
    bCO_Sensor_A_Fault                  : BOOL;
    bCO_Sensor_B_Fault                  : BOOL;
    bCO_Sensor_C_Fault                  : BOOL;

    (* Visibility Transmissometers *)
    bVis_Discrepancy_AB                 : BOOL;
    bVis_Discrepancy_BC                 : BOOL;
    bVis_Discrepancy_CA                 : BOOL;
    rVis_Discrepancy_Timer_s            : REAL;
    bVis_Sensor_A_Fault                 : BOOL;
    bVis_Sensor_B_Fault                 : BOOL;
    bVis_Sensor_C_Fault                 : BOOL;

    (* Linear Heat Detection Cable *)
    bHeat_Discrepancy_AB                : BOOL;
    bHeat_Discrepancy_BC                : BOOL;
    bHeat_Discrepancy_CA                : BOOL;
    rHeat_Discrepancy_Timer_s           : REAL;
    bHeat_Sensor_A_Fault                : BOOL;
    bHeat_Sensor_B_Fault                : BOOL;
    bHeat_Sensor_C_Fault                : BOOL;

    (* === STATE-SPACE MATRICES FOR 5-STATE DYNAMICS (x[k+1] = A*x[k] + B*u[k]) === *)
    (* State Vector:
       x[0] = Longitudinal air velocity tracking error Delta v_air [m/s]
       x[1] = CO gas concentration deviation Delta C_CO [ppm]
       x[2] = Smoke optical opacity / extinction deviation Delta k_vis [1/m]
       x[3] = Vehicle piston effect aerodynamic pressure Delta P_piston [Pa]
       x[4] = Thermal buoyancy stack pressure difference Delta P_buoyancy [Pa]
    *)
    x_state                             : ARRAY[0..4] OF REAL;
    x_state_next                        : ARRAY[0..4] OF REAL;
    x_state_horizon2                    : ARRAY[0..4] OF REAL;
    x_state_horizon3                    : ARRAY[0..4] OF REAL;
    x_setpoint                          : ARRAY[0..4] OF REAL;
    x_error                             : ARRAY[0..4] OF REAL;

    (* Control Vector:
       u[0] = Forward jet fan cluster aerodynamic thrust command Delta F_fwd [N]
       u[1] = Reverse jet fan cluster aerodynamic thrust command Delta F_rev [N]
       u[2] = Overhead smoke extraction damper flow capacity Delta u_damper [%]
       u[3] = Portal ventilation fan fine trim Delta u_portal [%]
    *)
    u_control                           : ARRAY[0..3] OF REAL;
    u_control_prev                      : ARRAY[0..3] OF REAL;
    u_rate_limit                        : ARRAY[0..3] OF REAL;

    (* 5x5 State Matrix A *)
    A_mat                               : ARRAY[0..4, 0..4] OF REAL;
    (* 5x4 Input Coupling Matrix B *)
    B_mat                               : ARRAY[0..4, 0..3] OF REAL;
    (* 5x5 Measurement Matrix C *)
    C_mat                               : ARRAY[0..4, 0..4] OF REAL;

    (* === RECEDING-HORIZON MPC COST MATRICES & OPTIMIZATION INTERNAL BUFFERS === *)
    Q_diag                              : ARRAY[0..4] OF REAL; (* State deviation penalties *)
    R_diag                              : ARRAY[0..3] OF REAL; (* Control effort rate penalties *)
    P_diag                              : ARRAY[0..4] OF REAL; (* Terminal state penalties *)
    Hessian_diag                        : ARRAY[0..3] OF REAL; (* Approximate Hessian diagonal *)
    Gradient_vec                        : ARRAY[0..3] OF REAL; (* Real-time cost gradient vector *)
    u_opt_step                          : ARRAY[0..3] OF REAL; (* Projected Newton/gradient step *)
    rMPC_Step_Size_Alpha                : REAL;
    i_mpc_iter                          : INT;
    n_mpc_max_iter                      : INT;

    (* === AERODYNAMIC MODEL & TUNNEL GEOMETRY CONSTANTS === *)
    rTunnel_Cross_Section_Area_m2       : REAL;  (* Tunnel bore hydraulic cross section (e.g. 72.0 m2) *)
    rTunnel_Hydraulic_Diameter_m        : REAL;  (* Hydraulic diameter D_h = 4*A/P (e.g. 8.5 m) *)
    rTunnel_Length_m                    : REAL;  (* Tunnel tube bore length (e.g. 2400.0 m) *)
    rAir_Density_kg_m3                  : REAL;  (* Ambient dry air density (1.205 kg/m3) *)
    rWall_Friction_Factor_lambda        : REAL;  (* Darcy-Weisbach wall friction factor lambda (0.022) *)
    rVehicle_Drag_Coeff_Cd_Car          : REAL;  (* Passenger vehicle drag coefficient (0.35) *)
    rVehicle_Drag_Coeff_Cd_Truck        : REAL;  (* Heavy goods vehicle drag coefficient (0.85) *)
    rSingle_JetFan_Thrust_N             : REAL;  (* Aerodynamic thrust per jet fan unit at 100% (850 N) *)

    (* === WU & BAKAR CRITICAL VELOCITY CALCULATOR === *)
    rDimensionless_Heat_Release_Q_star  : REAL;
    rFroude_Number_Factor               : REAL;
    rTarget_Longitudinal_Airspeed_m_s   : REAL;

    (* === FINITE STATE MACHINE SEQUENCING TIMERS & THRESHOLDS === *)
    rState_Dwell_Timer_s                : REAL;
    rFan_Staging_Deadtime_Timer_s       : REAL;
    rDeluge_Suppression_Timer_s         : REAL;
    rPost_Fire_Purge_Timer_s            : REAL;

    (* === ISA-18.2 ALARM ENGINE DEADZONE & TIMING BUFFERS === *)
    rCO_High_Alarm_Timer_s              : REAL;
    rCO_HighHigh_Trip_Timer_s           : REAL;
    rVis_Low_Alarm_Timer_s              : REAL;
    rHeat_Rate_Of_Rise_degC_min         : REAL;
    rPrevious_Heat_Detect_Temp_degC     : REAL;
    rFire_Confirmed_Timer_s             : REAL;
    rBacklayering_Alarm_Timer_s         : REAL;
    rCrossPassage_Low_P_Timer_s         : REAL;
    rJetFan_Motor_Hot_Timer_s           : REAL;

    (* Loop iteration counters *)
    i_loop                              : INT;
    j_loop                              : INT;
    k_loop                              : INT;
END_VAR
""")

# Phase 0: System Initialization & Discrete Model Calibration
st_code_parts.append("""
(* ============================================================================== *)
(* PHASE 0: SYSTEM INITIALIZATION & DISCRETE STATE-SPACE MATRIX CALIBRATION       *)
(* ============================================================================== *)
IF A_mat[0, 0] = 0.0 THEN
    (* Sampled continuous-to-discrete system matrix at Ts = 50.0 ms *)
    (* State 0: Delta v_air (Longitudinal air velocity tracking error [m/s]) *)
    A_mat[0, 0] := 0.9850; A_mat[0, 1] := 0.0000;  A_mat[0, 2] := 0.0000;  A_mat[0, 3] := 0.0120; A_mat[0, 4] := 0.0085;
    (* State 1: Delta C_CO (CO gas concentration deviation [ppm]) *)
    A_mat[1, 0] := -0.0450; A_mat[1, 1] := 0.9620; A_mat[1, 2] := 0.0050;  A_mat[1, 3] := 0.0000; A_mat[1, 4] := 0.0000;
    (* State 2: Delta k_vis (Smoke opacity / extinction deviation [1/m]) *)
    A_mat[2, 0] := -0.0080; A_mat[2, 1] := 0.0005; A_mat[2, 2] := 0.9700;  A_mat[2, 3] := 0.0000; A_mat[2, 4] := 0.0000;
    (* State 3: Delta P_piston (Vehicle piston effect aerodynamic pressure [Pa]) *)
    A_mat[3, 0] := -0.0150; A_mat[3, 1] := 0.0000; A_mat[3, 2] := 0.0000;  A_mat[3, 3] := 0.9400; A_mat[3, 4] := 0.0000;
    (* State 4: Delta P_buoyancy (Thermal buoyancy stack pressure difference [Pa]) *)
    A_mat[4, 0] := 0.0000;  A_mat[4, 1] := 0.0000; A_mat[4, 2] := 0.0000;  A_mat[4, 3] := 0.0000; A_mat[4, 4] := 0.9780;

    (* Input Coupling Matrix B (Affecting states via u_fwd, u_rev, u_damper, u_portal) *)
    B_mat[0, 0] := 0.0240;  B_mat[0, 1] := -0.0240; B_mat[0, 2] := 0.0050; B_mat[0, 3] := 0.0120;
    B_mat[1, 0] := -0.0180; B_mat[1, 1] := 0.0180;  B_mat[1, 2] := -0.0350; B_mat[1, 3] := -0.0220;
    B_mat[2, 0] := -0.0040; B_mat[2, 1] := 0.0040;  B_mat[2, 2] := -0.0120; B_mat[2, 3] := -0.0060;
    B_mat[3, 0] := 0.0000;  B_mat[3, 1] := 0.0000;  B_mat[3, 2] := 0.0000; B_mat[3, 3] := 0.0000;
    B_mat[4, 0] := 0.0000;  B_mat[4, 1] := 0.0000;  B_mat[4, 2] := -0.0080; B_mat[4, 3] := 0.0000;

    (* Observation Matrix C *)
    FOR i_loop := 0 TO 4 DO
        FOR j_loop := 0 TO 4 DO
            IF i_loop = j_loop THEN
                C_mat[i_loop, j_loop] := 1.0;
            ELSE
                C_mat[i_loop, j_loop] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    (* MPC Quadratic Cost Diagonal Weights *)
    Q_diag[0] := 50.0;  (* Velocity tracking penalty (critical for anti-backlayering) *)
    Q_diag[1] := 35.0;  (* CO concentration penalty *)
    Q_diag[2] := 45.0;  (* Visibility extinction penalty *)
    Q_diag[3] := 15.0;  (* Piston pressure stability penalty *)
    Q_diag[4] := 20.0;  (* Buoyancy pressure penalty *)

    R_diag[0] := 1.2;   (* Forward jet fan power rate penalty *)
    R_diag[1] := 1.2;   (* Reverse jet fan power rate penalty *)
    R_diag[2] := 2.5;   (* Extraction damper stroke rate penalty *)
    R_diag[3] := 1.8;   (* Portal fan trim rate penalty *)

    P_diag[0] := 80.0;  (* Terminal penalties *)
    P_diag[1] := 55.0;
    P_diag[2] := 70.0;
    P_diag[3] := 25.0;
    P_diag[4] := 30.0;

    (* Slew rate limitations per PLC scan [units / scan] *)
    u_rate_limit[0] := 500.0; (* Jet fan thrust rate max 500 N per scan *)
    u_rate_limit[1] := 500.0;
    u_rate_limit[2] := 2.50;  (* Damper stroke max 2.5% per scan *)
    u_rate_limit[3] := 2.00;

    rMPC_Step_Size_Alpha := 0.125;
    n_mpc_max_iter := 5;

    (* Tunnel Bore Geometry & Physical Constants *)
    rTunnel_Cross_Section_Area_m2 := 72.0; (* Twin-lane highway tunnel *)
    rTunnel_Hydraulic_Diameter_m := 8.50;
    rTunnel_Length_m := 2400.0;
    rAir_Density_kg_m3 := 1.205;
    rWall_Friction_Factor_lambda := 0.022;
    rVehicle_Drag_Coeff_Cd_Car := 0.35;
    rVehicle_Drag_Coeff_Cd_Truck := 0.85;
    rSingle_JetFan_Thrust_N := 850.0;

    (* Initial Default State *)
    eCurrent_State := 1; (* ECO_VENTILATION_NATURAL *)
    bTunnel_Fire_Confirmed := FALSE;
    bSmoke_Backlayering_Risk := FALSE;
    bCrossPassage_Depressurized_Warning := FALSE;
    rPrevious_Heat_Detect_Temp_degC := 25.0;
END_IF;
""")

# Phase 1: 2oo3 TMR Voting Logic
st_code_parts.append("""
(* ============================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY     *)
(* ============================================================================== *)

(* --- SUB-PHASE 1A: CO GAS NDIR SENSOR 2oo3 VOTING --- *)
bCO_Discrepancy_AB := ABS(rCO_Gas_Concentration_ppm_ChA - rCO_Gas_Concentration_ppm_ChB) > 15.0;
bCO_Discrepancy_BC := ABS(rCO_Gas_Concentration_ppm_ChB - rCO_Gas_Concentration_ppm_ChC) > 15.0;
bCO_Discrepancy_CA := ABS(rCO_Gas_Concentration_ppm_ChC - rCO_Gas_Concentration_ppm_ChA) > 15.0;

IF bCO_Discrepancy_AB OR bCO_Discrepancy_BC OR bCO_Discrepancy_CA THEN
    rCO_Discrepancy_Timer_s := rCO_Discrepancy_Timer_s + (tScan_Cycle_Time_ms / 1000.0);
ELSE
    rCO_Discrepancy_Timer_s := MAX(0.0, rCO_Discrepancy_Timer_s - (tScan_Cycle_Time_ms / 500.0));
END_IF;

IF NOT bCO_Discrepancy_AB AND NOT bCO_Discrepancy_CA THEN
    rCO_Concentration_Voted_ppm := (rCO_Gas_Concentration_ppm_ChA + rCO_Gas_Concentration_ppm_ChB + rCO_Gas_Concentration_ppm_ChC) / 3.0;
    bCO_Sensor_A_Fault := FALSE;
    bCO_Sensor_B_Fault := FALSE;
    bCO_Sensor_C_Fault := FALSE;
ELSIF bCO_Discrepancy_AB AND NOT bCO_Discrepancy_BC THEN
    rCO_Concentration_Voted_ppm := (rCO_Gas_Concentration_ppm_ChB + rCO_Gas_Concentration_ppm_ChC) / 2.0;
    bCO_Sensor_A_Fault := (rCO_Discrepancy_Timer_s > 3.0);
ELSIF bCO_Discrepancy_BC AND NOT bCO_Discrepancy_CA THEN
    rCO_Concentration_Voted_ppm := (rCO_Gas_Concentration_ppm_ChA + rCO_Gas_Concentration_ppm_ChC) / 2.0;
    bCO_Sensor_B_Fault := (rCO_Discrepancy_Timer_s > 3.0);
ELSIF bCO_Discrepancy_CA AND NOT bCO_Discrepancy_AB THEN
    rCO_Concentration_Voted_ppm := (rCO_Gas_Concentration_ppm_ChA + rCO_Gas_Concentration_ppm_ChB) / 2.0;
    bCO_Sensor_C_Fault := (rCO_Discrepancy_Timer_s > 3.0);
ELSE
    IF (rCO_Gas_Concentration_ppm_ChA >= rCO_Gas_Concentration_ppm_ChB AND rCO_Gas_Concentration_ppm_ChA <= rCO_Gas_Concentration_ppm_ChC) OR
       (rCO_Gas_Concentration_ppm_ChA <= rCO_Gas_Concentration_ppm_ChB AND rCO_Gas_Concentration_ppm_ChA >= rCO_Gas_Concentration_ppm_ChC) THEN
        rCO_Concentration_Voted_ppm := rCO_Gas_Concentration_ppm_ChA;
    ELSIF (rCO_Gas_Concentration_ppm_ChB >= rCO_Gas_Concentration_ppm_ChA AND rCO_Gas_Concentration_ppm_ChB <= rCO_Gas_Concentration_ppm_ChC) OR
          (rCO_Gas_Concentration_ppm_ChB <= rCO_Gas_Concentration_ppm_ChA AND rCO_Gas_Concentration_ppm_ChB >= rCO_Gas_Concentration_ppm_ChC) THEN
        rCO_Concentration_Voted_ppm := rCO_Gas_Concentration_ppm_ChB;
    ELSE
        rCO_Concentration_Voted_ppm := rCO_Gas_Concentration_ppm_ChC;
    END_IF;
END_IF;

(* --- SUB-PHASE 1B: VISIBILITY TRANSMISSOMETER 2oo3 VOTING --- *)
bVis_Discrepancy_AB := ABS(rVisibility_Extinction_Coeff_k_m1_ChA - rVisibility_Extinction_Coeff_k_m1_ChB) > 0.0035;
bVis_Discrepancy_BC := ABS(rVisibility_Extinction_Coeff_k_m1_ChB - rVisibility_Extinction_Coeff_k_m1_ChC) > 0.0035;
bVis_Discrepancy_CA := ABS(rVisibility_Extinction_Coeff_k_m1_ChC - rVisibility_Extinction_Coeff_k_m1_ChA) > 0.0035;

IF bVis_Discrepancy_AB OR bVis_Discrepancy_BC OR bVis_Discrepancy_CA THEN
    rVis_Discrepancy_Timer_s := rVis_Discrepancy_Timer_s + (tScan_Cycle_Time_ms / 1000.0);
ELSE
    rVis_Discrepancy_Timer_s := MAX(0.0, rVis_Discrepancy_Timer_s - (tScan_Cycle_Time_ms / 500.0));
END_IF;

IF NOT bVis_Discrepancy_AB AND NOT bVis_Discrepancy_CA THEN
    rVisibility_Extinction_Voted_k_m1 := (rVisibility_Extinction_Coeff_k_m1_ChA + rVisibility_Extinction_Coeff_k_m1_ChB + rVisibility_Extinction_Coeff_k_m1_ChC) / 3.0;
    bVis_Sensor_A_Fault := FALSE;
    bVis_Sensor_B_Fault := FALSE;
    bVis_Sensor_C_Fault := FALSE;
ELSIF bVis_Discrepancy_AB AND NOT bVis_Discrepancy_BC THEN
    rVisibility_Extinction_Voted_k_m1 := (rVisibility_Extinction_Coeff_k_m1_ChB + rVisibility_Extinction_Coeff_k_m1_ChC) / 2.0;
    bVis_Sensor_A_Fault := (rVis_Discrepancy_Timer_s > 3.0);
ELSIF bVis_Discrepancy_BC AND NOT bVis_Discrepancy_CA THEN
    rVisibility_Extinction_Voted_k_m1 := (rVisibility_Extinction_Coeff_k_m1_ChA + rVisibility_Extinction_Coeff_k_m1_ChC) / 2.0;
    bVis_Sensor_B_Fault := (rVis_Discrepancy_Timer_s > 3.0);
ELSIF bVis_Discrepancy_CA AND NOT bVis_Discrepancy_AB THEN
    rVisibility_Extinction_Voted_k_m1 := (rVisibility_Extinction_Coeff_k_m1_ChA + rVisibility_Extinction_Coeff_k_m1_ChB) / 2.0;
    bVis_Sensor_C_Fault := (rVis_Discrepancy_Timer_s > 3.0);
ELSE
    IF (rVisibility_Extinction_Coeff_k_m1_ChA >= rVisibility_Extinction_Coeff_k_m1_ChB AND rVisibility_Extinction_Coeff_k_m1_ChA <= rVisibility_Extinction_Coeff_k_m1_ChC) OR
       (rVisibility_Extinction_Coeff_k_m1_ChA <= rVisibility_Extinction_Coeff_k_m1_ChB AND rVisibility_Extinction_Coeff_k_m1_ChA >= rVisibility_Extinction_Coeff_k_m1_ChC) THEN
        rVisibility_Extinction_Voted_k_m1 := rVisibility_Extinction_Coeff_k_m1_ChA;
    ELSIF (rVisibility_Extinction_Coeff_k_m1_ChB >= rVisibility_Extinction_Coeff_k_m1_ChA AND rVisibility_Extinction_Coeff_k_m1_ChB <= rVisibility_Extinction_Coeff_k_m1_ChC) OR
          (rVisibility_Extinction_Coeff_k_m1_ChB <= rVisibility_Extinction_Coeff_k_m1_ChA AND rVisibility_Extinction_Coeff_k_m1_ChB >= rVisibility_Extinction_Coeff_k_m1_ChC) THEN
        rVisibility_Extinction_Voted_k_m1 := rVisibility_Extinction_Coeff_k_m1_ChB;
    ELSE
        rVisibility_Extinction_Voted_k_m1 := rVisibility_Extinction_Coeff_k_m1_ChC;
    END_IF;
END_IF;

(* --- SUB-PHASE 1C: LINEAR HEAT DETECTION CABLE 2oo3 VOTING --- *)
bHeat_Discrepancy_AB := ABS(rLinear_Heat_Detect_Zone1_Temp_ChA - rLinear_Heat_Detect_Zone1_Temp_ChB) > 8.0;
bHeat_Discrepancy_BC := ABS(rLinear_Heat_Detect_Zone1_Temp_ChB - rLinear_Heat_Detect_Zone1_Temp_ChC) > 8.0;
bHeat_Discrepancy_CA := ABS(rLinear_Heat_Detect_Zone1_Temp_ChC - rLinear_Heat_Detect_Zone1_Temp_ChA) > 8.0;

IF bHeat_Discrepancy_AB OR bHeat_Discrepancy_BC OR bHeat_Discrepancy_CA THEN
    rHeat_Discrepancy_Timer_s := rHeat_Discrepancy_Timer_s + (tScan_Cycle_Time_ms / 1000.0);
ELSE
    rHeat_Discrepancy_Timer_s := MAX(0.0, rHeat_Discrepancy_Timer_s - (tScan_Cycle_Time_ms / 500.0));
END_IF;

(* Safety Critical Fire Voting: Take Maximum Pair to Ensure Fast Thermal Alarm Response *)
IF (rLinear_Heat_Detect_Zone1_Temp_ChA >= rLinear_Heat_Detect_Zone1_Temp_ChB AND rLinear_Heat_Detect_Zone1_Temp_ChB >= rLinear_Heat_Detect_Zone1_Temp_ChC) OR
   (rLinear_Heat_Detect_Zone1_Temp_ChB >= rLinear_Heat_Detect_Zone1_Temp_ChA AND rLinear_Heat_Detect_Zone1_Temp_ChA >= rLinear_Heat_Detect_Zone1_Temp_ChC) THEN
    rHeat_Detect_Zone1_Voted_degC := (rLinear_Heat_Detect_Zone1_Temp_ChA + rLinear_Heat_Detect_Zone1_Temp_ChB) / 2.0;
ELSIF (rLinear_Heat_Detect_Zone1_Temp_ChB >= rLinear_Heat_Detect_Zone1_Temp_ChC AND rLinear_Heat_Detect_Zone1_Temp_ChC >= rLinear_Heat_Detect_Zone1_Temp_ChA) OR
      (rLinear_Heat_Detect_Zone1_Temp_ChC >= rLinear_Heat_Detect_Zone1_Temp_ChB AND rLinear_Heat_Detect_Zone1_Temp_ChB >= rLinear_Heat_Detect_Zone1_Temp_ChA) THEN
    rHeat_Detect_Zone1_Voted_degC := (rLinear_Heat_Detect_Zone1_Temp_ChB + rLinear_Heat_Detect_Zone1_Temp_ChC) / 2.0;
ELSE
    rHeat_Detect_Zone1_Voted_degC := (rLinear_Heat_Detect_Zone1_Temp_ChA + rLinear_Heat_Detect_Zone1_Temp_ChC) / 2.0;
END_IF;

(* Rate-of-Rise calculation [deg C / min] *)
rHeat_Rate_Of_Rise_degC_min := (rHeat_Detect_Zone1_Voted_degC - rPrevious_Heat_Detect_Temp_degC) * (60000.0 / tScan_Cycle_Time_ms);
rPrevious_Heat_Detect_Temp_degC := rHeat_Detect_Zone1_Voted_degC;
""")

# Phase 2: Aerodynamics, Traffic Piston Effect & Critical Backlayering
st_code_parts.append("""
(* ============================================================================== *)
(* PHASE 2: TRAFFIC PISTON EFFECT & WU & BAKAR CRITICAL VELOCITY MODEL            *)
(* ============================================================================== *)

(* --- SUB-PHASE 2A: TRAFFIC PISTON EFFECT AERODYNAMIC THRUST --- *)
IF rTraffic_Average_Speed_km_h > 5.0 THEN
    rAirflow_Piston_Effect_Thrust_N := (rTraffic_Vehicle_Flow_Rate_veh_h / 3600.0) * (rTunnel_Length_m / (rTraffic_Average_Speed_km_h / 3.6)) *
        0.5 * rAir_Density_kg_m3 *
        (((1.0 - (rTraffic_Heavy_Truck_Percentage_Pct / 100.0)) * 0.85) + ((rTraffic_Heavy_Truck_Percentage_Pct / 100.0) * 6.5)) *
        ((rTraffic_Average_Speed_km_h / 3.6) - rTunnel_Longitudinal_AirVelocity_m_s) *
        ABS((rTraffic_Average_Speed_km_h / 3.6) - rTunnel_Longitudinal_AirVelocity_m_s);
ELSE
    rAirflow_Piston_Effect_Thrust_N := 0.0;
END_IF;

(* Tunnel Longitudinal Aerodynamic Head Loss (Darcy-Weisbach) *)
rNet_Tunnel_Pressure_Drop_Pa := rWall_Friction_Factor_lambda * (rTunnel_Length_m / rTunnel_Hydraulic_Diameter_m) *
    0.5 * rAir_Density_kg_m3 * rTunnel_Longitudinal_AirVelocity_m_s * ABS(rTunnel_Longitudinal_AirVelocity_m_s);

(* --- SUB-PHASE 2B: WU & BAKAR CRITICAL ANTI-BACKLAYERING VELOCITY --- *)
IF rFire_Estimated_Heat_Release_Rate_MW > 0.5 THEN
    rDimensionless_Heat_Release_Q_star := (rFire_Estimated_Heat_Release_Rate_MW * 1000000.0) /
        (rAir_Density_kg_m3 * 1005.0 * (rTunnel_Portal_Ambient_Temp_degC + 273.15) * 3.132 * 210.5);

    IF rDimensionless_Heat_Release_Q_star <= 0.20 THEN
        rCritical_Anti_Backlayering_Vel_m_s := 0.40 * EXP(0.3333 * LN(MAX(0.001, rDimensionless_Heat_Release_Q_star / 0.20))) *
            SQRT(9.81 * rTunnel_Hydraulic_Diameter_m);
    ELSE
        rCritical_Anti_Backlayering_Vel_m_s := 0.40 * SQRT(9.81 * rTunnel_Hydraulic_Diameter_m);
    END_IF;
    rCritical_Anti_Backlayering_Vel_m_s := MAX(2.20, MIN(3.80, rCritical_Anti_Backlayering_Vel_m_s));
ELSE
    rCritical_Anti_Backlayering_Vel_m_s := 2.50; (* Standard baseline design velocity *)
END_IF;

(* Backlayering Risk Evaluation during Confirmed Fire *)
IF bTunnel_Fire_Confirmed AND (rTunnel_Longitudinal_AirVelocity_m_s < (rCritical_Anti_Backlayering_Vel_m_s - 0.25)) THEN
    bSmoke_Backlayering_Risk := TRUE;
ELSE
    bSmoke_Backlayering_Risk := FALSE;
END_IF;

(* --- SUB-PHASE 2C: ESCAPE CROSS-PASSAGE OVERPRESSURE EVALUATION --- *)
(* Safe cross-passage evacuation requires Delta P >= 50.0 Pa relative to incident bore *)
IF bCrossPassage_Pressurization_Fan_Cmd AND (rCrossPassage_Overpressure_Delta_P_Pa < 50.0) THEN
    bCrossPassage_Depressurized_Warning := TRUE;
ELSE
    bCrossPassage_Depressurized_Warning := FALSE;
END_IF;
""")

# Phase 3: Discrete State-Space & 3-Horizon MPC
st_code_parts.append("""
(* ============================================================================== *)
(* PHASE 3: DISCRETE STATE-SPACE PREDICTION & 3-HORIZON RECEDING MPC OPTIMIZER    *)
(* ============================================================================== *)

(* Determine dynamic target longitudinal airspeed setpoint based on operating condition *)
IF bTunnel_Fire_Confirmed THEN
    rTarget_Longitudinal_Airspeed_m_s := rCritical_Anti_Backlayering_Vel_m_s;
ELSIF rCO_Concentration_Voted_ppm > 45.0 THEN
    rTarget_Longitudinal_Airspeed_m_s := 3.0;
ELSIF rVisibility_Extinction_Voted_k_m1 > 0.005 THEN
    rTarget_Longitudinal_Airspeed_m_s := 2.5;
ELSE
    rTarget_Longitudinal_Airspeed_m_s := 1.2; (* Eco-ventilation baseline *)
END_IF;

x_state[0] := rTunnel_Longitudinal_AirVelocity_m_s - rTarget_Longitudinal_Airspeed_m_s;
x_state[1] := rCO_Concentration_Voted_ppm - 25.0;
x_state[2] := (rVisibility_Extinction_Voted_k_m1 - 0.003) * 1000.0;
x_state[3] := (rAirflow_Piston_Effect_Thrust_N / rTunnel_Cross_Section_Area_m2) - 15.0;
x_state[4] := rTunnel_Portal_Barometric_Delta_P_Pa;

x_setpoint[0] := 0.0;
x_setpoint[1] := 0.0;
x_setpoint[2] := 0.0;
x_setpoint[3] := 0.0;
x_setpoint[4] := 0.0;

FOR i_loop := 0 TO 4 DO
    x_error[i_loop] := x_state[i_loop] - x_setpoint[i_loop];
END_FOR;

(* Horizon 1 State Prediction: x_next = A * x + B * u *)
FOR i_loop := 0 TO 4 DO
    x_state_next[i_loop] := 0.0;
    FOR j_loop := 0 TO 4 DO
        x_state_next[i_loop] := x_state_next[i_loop] + (A_mat[i_loop, j_loop] * x_state[j_loop]);
    END_FOR;
    FOR k_loop := 0 TO 3 DO
        x_state_next[i_loop] := x_state_next[i_loop] + (B_mat[i_loop, k_loop] * u_control[k_loop]);
    END_FOR;
END_FOR;

(* Horizon 2 State Prediction: x_horizon2 = A * x_next + B * u *)
FOR i_loop := 0 TO 4 DO
    x_state_horizon2[i_loop] := 0.0;
    FOR j_loop := 0 TO 4 DO
        x_state_horizon2[i_loop] := x_state_horizon2[i_loop] + (A_mat[i_loop, j_loop] * x_state_next[j_loop]);
    END_FOR;
    FOR k_loop := 0 TO 3 DO
        x_state_horizon2[i_loop] := x_state_horizon2[i_loop] + (B_mat[i_loop, k_loop] * u_control[k_loop]);
    END_FOR;
END_FOR;

(* Horizon 3 State Prediction: x_horizon3 = A * x_horizon2 + B * u *)
FOR i_loop := 0 TO 4 DO
    x_state_horizon3[i_loop] := 0.0;
    FOR j_loop := 0 TO 4 DO
        x_state_horizon3[i_loop] := x_state_horizon3[i_loop] + (A_mat[i_loop, j_loop] * x_state_horizon2[j_loop]);
    END_FOR;
    FOR k_loop := 0 TO 3 DO
        x_state_horizon3[i_loop] := x_state_horizon3[i_loop] + (B_mat[i_loop, k_loop] * u_control[k_loop]);
    END_FOR;
END_FOR;

(* --- 3-HORIZON RECEDING HORIZON QUADRATIC GRADIENT DESCENT --- *)
(* Cost Function: J = sum_{h=1}^3 (x_h)^T * Q * (x_h) + (u)^T * R * (u) + (x_3)^T * P * (x_3) *)
FOR k_loop := 0 TO 3 DO
    Gradient_vec[k_loop] := 2.0 * R_diag[k_loop] * u_control[k_loop];

    (* Horizon 1 Contribution *)
    FOR i_loop := 0 TO 4 DO
        Gradient_vec[k_loop] := Gradient_vec[k_loop] +
            (2.0 * B_mat[i_loop, k_loop] * Q_diag[i_loop] * x_state_next[i_loop]);
    END_FOR;

    (* Horizon 2 Contribution with discounted factor gamma=0.85 *)
    FOR i_loop := 0 TO 4 DO
        Gradient_vec[k_loop] := Gradient_vec[k_loop] +
            (1.70 * B_mat[i_loop, k_loop] * Q_diag[i_loop] * x_state_horizon2[i_loop]);
    END_FOR;

    (* Horizon 3 Terminal Contribution with terminal weight P *)
    FOR i_loop := 0 TO 4 DO
        Gradient_vec[k_loop] := Gradient_vec[k_loop] +
            (1.445 * B_mat[i_loop, k_loop] * (Q_diag[i_loop] + P_diag[i_loop]) * x_state_horizon3[i_loop]);
    END_FOR;

    (* Approximate Hessian diagonal element: H_mm = 2 * R[m] + 2 * sum_i( B[i, m]^2 * (Q[i] + P[i]) ) *)
    Hessian_diag[k_loop] := 2.0 * R_diag[k_loop];
    FOR i_loop := 0 TO 4 DO
        Hessian_diag[k_loop] := Hessian_diag[k_loop] +
            (2.0 * B_mat[i_loop, k_loop] * B_mat[i_loop, k_loop] * (Q_diag[i_loop] + (0.5 * P_diag[i_loop])));
    END_FOR;

    (* Projected Newton-Raphson step *)
    IF Hessian_diag[k_loop] > 0.001 THEN
        u_opt_step[k_loop] := - Gradient_vec[k_loop] / Hessian_diag[k_loop];
    ELSE
        u_opt_step[k_loop] := - rMPC_Step_Size_Alpha * Gradient_vec[k_loop];
    END_IF;
END_FOR;

(* Perform MPC multi-iteration optimization with slew rate and boundary constraints *)
FOR i_mpc_iter := 1 TO n_mpc_max_iter DO
    FOR k_loop := 0 TO 3 DO
        u_opt_step[k_loop] := MAX(-u_rate_limit[k_loop], MIN(u_rate_limit[k_loop], u_opt_step[k_loop]));
        u_control[k_loop] := u_control[k_loop] + (rMPC_Step_Size_Alpha * u_opt_step[k_loop]);

        (* Actuator limits *)
        IF k_loop = 0 THEN
            (* Forward Jet Fan total thrust: 0 to 10200 N (12 pairs x 850 N) *)
            u_control[k_loop] := MAX(0.0, MIN(10200.0, u_control[k_loop]));
        ELSIF k_loop = 1 THEN
            (* Reverse Jet Fan thrust: 0 to 10200 N *)
            u_control[k_loop] := MAX(0.0, MIN(10200.0, u_control[k_loop]));
        ELSIF k_loop = 2 THEN
            (* Extraction damper capacity: 0 to 100% *)
            u_control[k_loop] := MAX(0.0, MIN(100.0, u_control[k_loop]));
        ELSIF k_loop = 3 THEN
            (* Portal fan trim: 0 to 100% *)
            u_control[k_loop] := MAX(0.0, MIN(100.0, u_control[k_loop]));
        END_IF;
    END_FOR;
END_FOR;
""")

# Phase 4: Jet Fan Staging & VFD Modulating Control
st_code_parts.append("""
(* ============================================================================== *)
(* PHASE 4: REVERSIBLE JET FAN CLUSTER STAGING, VMS & CROSS-PASSAGE FANS          *)
(* ============================================================================== *)

(* Staging deadtime timer to prevent cyclic contactor wear (minimum 15s between steps) *)
rFan_Staging_Deadtime_Timer_s := rFan_Staging_Deadtime_Timer_s + (tScan_Cycle_Time_ms / 1000.0);

IF eCurrent_State = 4 OR eCurrent_State = 5 THEN
    (* Emergency Fire Mode: Maximum forward thrust to purge smoke in traffic direction *)
    nJetFan_Active_Forward_Clusters := 12;
    nJetFan_Active_Reverse_Clusters := 0;
    rJetFan_VFD_Speed_Ref_Pct := 100.0;
    bSmoke_Extraction_Damper_Open_Cmd := TRUE;
    bPortal_Closure_Traffic_Gate_Cmd := TRUE;
    bCrossPassage_Pressurization_Fan_Cmd := TRUE;
    bVMS_Evacuation_Display_Sign_Cmd := TRUE;
ELSIF eCurrent_State = 6 THEN
    (* Post-fire purge: High extraction with 8 forward clusters *)
    nJetFan_Active_Forward_Clusters := 8;
    nJetFan_Active_Reverse_Clusters := 0;
    rJetFan_VFD_Speed_Ref_Pct := 85.0;
    bSmoke_Extraction_Damper_Open_Cmd := TRUE;
    bPortal_Closure_Traffic_Gate_Cmd := TRUE;
    bCrossPassage_Pressurization_Fan_Cmd := TRUE;
    bVMS_Evacuation_Display_Sign_Cmd := TRUE;
ELSE
    (* Normal / Peak Traffic Regulation: Stage forward jet fan clusters based on MPC thrust *)
    IF rFan_Staging_Deadtime_Timer_s >= 15.0 THEN
        nJetFan_Active_Forward_Clusters := REAL_TO_INT(u_control[0] / rSingle_JetFan_Thrust_N);
        nJetFan_Active_Forward_Clusters := MAX(0, MIN(12, nJetFan_Active_Forward_Clusters));
        nJetFan_Active_Reverse_Clusters := 0;
        rFan_Staging_Deadtime_Timer_s := 0.0;
    END_IF;

    (* Fine VFD speed trimming on lead fan bank (Bays 1-2) *)
    IF nJetFan_Active_Forward_Clusters > 0 THEN
        rJetFan_VFD_Speed_Ref_Pct := 50.0 + ((u_control[0] - (INT_TO_REAL(nJetFan_Active_Forward_Clusters) * rSingle_JetFan_Thrust_N)) /
                                            rSingle_JetFan_Thrust_N) * 50.0;
        rJetFan_VFD_Speed_Ref_Pct := MAX(35.0, MIN(100.0, rJetFan_VFD_Speed_Ref_Pct));
    ELSE
        rJetFan_VFD_Speed_Ref_Pct := 0.0;
    END_IF;

    bSmoke_Extraction_Damper_Open_Cmd := (u_control[2] > 20.0);
    bPortal_Closure_Traffic_Gate_Cmd := FALSE;
    bCrossPassage_Pressurization_Fan_Cmd := FALSE;
    bVMS_Evacuation_Display_Sign_Cmd := FALSE;
END_IF;

(* Manual Engineering Mode Handler *)
IF bManual_Mode_Select THEN
    nJetFan_Active_Forward_Clusters := MAX(0, MIN(12, nManual_JetFan_Cluster_Cmd));
    nJetFan_Active_Reverse_Clusters := 0;
    rJetFan_VFD_Speed_Ref_Pct := 75.0;
END_IF;
""")

# Phase 5: Multi-Stage FSM
st_code_parts.append("""
(* ============================================================================== *)
(* PHASE 5: MULTI-STAGE FINITE STATE MACHINE (FSM) CONTROL SEQUENCER              *)
(* ============================================================================== *)

(* Fire Detection Logic: Manual Pull Station OR Linear Heat >= 68 C OR Rate-of-Rise >= 12 C/min *)
IF bFire_Emergency_Manual_PB OR (rHeat_Detect_Zone1_Voted_degC >= 68.0) OR (rHeat_Rate_Of_Rise_degC_min >= 12.0) THEN
    rFire_Confirmed_Timer_s := rFire_Confirmed_Timer_s + (tScan_Cycle_Time_ms / 1000.0);
    IF rFire_Confirmed_Timer_s >= 0.50 THEN
        bTunnel_Fire_Confirmed := TRUE;
        IF eCurrent_State < 4 THEN
            eCurrent_State := 4; (* Direct emergency escalation to EMERGENCY_FIRE_SMOKE_CONTAIN *)
            rState_Dwell_Timer_s := 0.0;
        END_IF;
    END_IF;
ELSE
    rFire_Confirmed_Timer_s := 0.0;
END_IF;

CASE eCurrent_State OF
    1: (* STATE_ECO_VENTILATION_NATURAL *)
        (* Rely on natural barometric draught and vehicle piston effect; jet fans idling *)
        bZonal_Deluge_WaterMist_Valve_Cmd := FALSE;
        rState_Dwell_Timer_s := rState_Dwell_Timer_s + (tScan_Cycle_Time_ms / 1000.0);

        (* Transition Criteria: CO rises > 30 ppm OR Visibility degrades k > 0.005 1/m *)
        IF rCO_Concentration_Voted_ppm >= 30.0 THEN
            eCurrent_State := 2; (* Advance to TRAFFIC_PEAK_CO_SCRUBBING *)
            rState_Dwell_Timer_s := 0.0;
        ELSIF rVisibility_Extinction_Voted_k_m1 >= 0.005 THEN
            eCurrent_State := 3; (* Advance to VISIBILITY_DEGRADED_FOG_SMOG *)
            rState_Dwell_Timer_s := 0.0;
        END_IF;

    2: (* STATE_TRAFFIC_PEAK_CO_SCRUBBING *)
        (* Stage jet fan clusters to dilute and flush CO emissions below 25 ppm *)
        bZonal_Deluge_WaterMist_Valve_Cmd := FALSE;
        rState_Dwell_Timer_s := rState_Dwell_Timer_s + (tScan_Cycle_Time_ms / 1000.0);

        (* Transition Criteria: CO normalized < 18 ppm for 30 seconds *)
        IF (rCO_Concentration_Voted_ppm <= 18.0) AND (rState_Dwell_Timer_s >= 30.0) THEN
            eCurrent_State := 1; (* Return to ECO mode *)
            rState_Dwell_Timer_s := 0.0;
        ELSIF rVisibility_Extinction_Voted_k_m1 >= 0.008 THEN
            eCurrent_State := 3; (* Transition to visibility scrubbing *)
            rState_Dwell_Timer_s := 0.0;
        END_IF;

    3: (* STATE_VISIBILITY_DEGRADED_FOG_SMOG *)
        (* Exhaust particulate haze/fog using combination of jet fans and ceiling extraction *)
        bZonal_Deluge_WaterMist_Valve_Cmd := FALSE;
        rState_Dwell_Timer_s := rState_Dwell_Timer_s + (tScan_Cycle_Time_ms / 1000.0);

        (* Transition Criteria: Visibility restored k <= 0.003 for 45 seconds *)
        IF (rVisibility_Extinction_Voted_k_m1 <= 0.003) AND (rState_Dwell_Timer_s >= 45.0) THEN
            eCurrent_State := 1; (* Return to ECO mode *)
            rState_Dwell_Timer_s := 0.0;
        END_IF;

    4: (* STATE_EMERGENCY_FIRE_SMOKE_CONTAIN *)
        (* Establish critical anti-backlayering longitudinal velocity (v_crit), lower portal gate *)
        bZonal_Deluge_WaterMist_Valve_Cmd := FALSE;
        rState_Dwell_Timer_s := rState_Dwell_Timer_s + (tScan_Cycle_Time_ms / 1000.0);

        (* Transition Criteria: Critical airflow established (v_air >= v_crit) and dwell >= 45s *)
        (* Escalate to zonal water-mist deluge if heat release rate > 15 MW or heat temp > 85 C *)
        IF (rFire_Estimated_Heat_Release_Rate_MW >= 15.0 OR rHeat_Detect_Zone1_Voted_degC >= 85.0) AND (rState_Dwell_Timer_s >= 30.0) THEN
            eCurrent_State := 5; (* Advance to ZONAL_DELUGE_SUPPRESSION *)
            rState_Dwell_Timer_s := 0.0;
            rDeluge_Suppression_Timer_s := 0.0;
        END_IF;

    5: (* STATE_ZONAL_DELUGE_SUPPRESSION *)
        (* Trigger high-pressure water-mist deluge zone to suppress fire load *)
        bZonal_Deluge_WaterMist_Valve_Cmd := TRUE;
        rState_Dwell_Timer_s := rState_Dwell_Timer_s + (tScan_Cycle_Time_ms / 1000.0);
        rDeluge_Suppression_Timer_s := rDeluge_Suppression_Timer_s + (tScan_Cycle_Time_ms / 1000.0);

        (* Transition Criteria: Deluge discharged for 120s and heat temp drops < 55 C *)
        IF (rDeluge_Suppression_Timer_s >= 120.0) AND (rHeat_Detect_Zone1_Voted_degC < 55.0) THEN
            bZonal_Deluge_WaterMist_Valve_Cmd := FALSE;
            eCurrent_State := 6; (* Advance to POST_FIRE_SMOKE_PURGE *)
            rState_Dwell_Timer_s := 0.0;
            rPost_Fire_Purge_Timer_s := 0.0;
        END_IF;

    6: (* STATE_POST_FIRE_SMOKE_PURGE *)
        (* Full smoke evacuation and toxic gas clearing following suppression *)
        bZonal_Deluge_WaterMist_Valve_Cmd := FALSE;
        rState_Dwell_Timer_s := rState_Dwell_Timer_s + (tScan_Cycle_Time_ms / 1000.0);
        rPost_Fire_Purge_Timer_s := rPost_Fire_Purge_Timer_s + (tScan_Cycle_Time_ms / 1000.0);

        (* Transition Criteria: Operator reset PB pressed, CO < 20 ppm, heat < 35 C, purge >= 300s *)
        IF bReset_Alarms_PB AND (rCO_Concentration_Voted_ppm < 20.0) AND (rHeat_Detect_Zone1_Voted_degC < 35.0) AND
           (rPost_Fire_Purge_Timer_s >= 300.0) THEN
            bTunnel_Fire_Confirmed := FALSE;
            eCurrent_State := 1; (* Return to ECO mode *)
            rState_Dwell_Timer_s := 0.0;
        END_IF;

    ELSE
        eCurrent_State := 1;
END_CASE;
""")

# Phase 6: ISA-18.2 Alarms and Status Word Packing
st_code_parts.append("""
(* ============================================================================== *)
(* PHASE 6: ISA-18.2 ALARM ENGINE & STATUS WORD BITFIELD PACKING                  *)
(* ============================================================================== *)

(* Clear working alarm flags before re-evaluation *)
dwAlarm_Word_Critical := 16#00000000;
dwAlarm_Word_Warning  := 16#00000000;
dwTunnel_Status_Word  := 16#00000000;

(* Alarm 1: Confirmed Tunnel Fire Incident (High-High Priority 1) *)
IF bTunnel_Fire_Confirmed THEN
    dwAlarm_Word_Critical := dwAlarm_Word_Critical OR 16#00000001; (* Bit 0: Fire Emergency *)
END_IF;

(* Alarm 2: Smoke Backlayering Hazard Trip *)
IF bSmoke_Backlayering_Risk THEN
    rBacklayering_Alarm_Timer_s := rBacklayering_Alarm_Timer_s + (tScan_Cycle_Time_ms / 1000.0);
    IF rBacklayering_Alarm_Timer_s >= 5.0 THEN
        dwAlarm_Word_Critical := dwAlarm_Word_Critical OR 16#00000002; (* Bit 1: Backlayering Critical *)
    END_IF;
ELSE
    rBacklayering_Alarm_Timer_s := 0.0;
END_IF;

(* Alarm 3: Carbon Monoxide (CO) Multi-Tiered Alarms *)
IF rCO_Concentration_Voted_ppm >= 100.0 THEN
    rCO_HighHigh_Trip_Timer_s := rCO_HighHigh_Trip_Timer_s + (tScan_Cycle_Time_ms / 1000.0);
    IF rCO_HighHigh_Trip_Timer_s >= 10.0 THEN
        dwAlarm_Word_Critical := dwAlarm_Word_Critical OR 16#00000004; (* Bit 2: CO High-High *)
    END_IF;
ELSIF rCO_Concentration_Voted_ppm >= 50.0 THEN
    rCO_High_Alarm_Timer_s := rCO_High_Alarm_Timer_s + (tScan_Cycle_Time_ms / 1000.0);
    IF rCO_High_Alarm_Timer_s >= 20.0 THEN
        dwAlarm_Word_Warning := dwAlarm_Word_Warning OR 16#00000001; (* Bit 0: CO High Warning *)
    END_IF;
ELSE
    rCO_HighHigh_Trip_Timer_s := 0.0;
    rCO_High_Alarm_Timer_s := 0.0;
END_IF;

(* Alarm 4: Visibility Low Degradation (k > 0.012 1/m) *)
IF rVisibility_Extinction_Voted_k_m1 >= 0.012 THEN
    rVis_Low_Alarm_Timer_s := rVis_Low_Alarm_Timer_s + (tScan_Cycle_Time_ms / 1000.0);
    IF rVis_Low_Alarm_Timer_s >= 15.0 THEN
        dwAlarm_Word_Warning := dwAlarm_Word_Warning OR 16#00000002; (* Bit 1: Visibility Low *)
    END_IF;
ELSE
    rVis_Low_Alarm_Timer_s := 0.0;
END_IF;

(* Alarm 5: Zonal Deluge Pump Feedback Discrepancy *)
IF bZonal_Deluge_WaterMist_Valve_Cmd AND NOT bDeluge_Pumps_Running_Feedback THEN
    dwAlarm_Word_Critical := dwAlarm_Word_Critical OR 16#00000008; (* Bit 3: Deluge Failure *)
END_IF;

(* Alarm 6: Cross-Passage Depressurization Warning (< 50 Pa) *)
IF bCrossPassage_Depressurized_Warning THEN
    rCrossPassage_Low_P_Timer_s := rCrossPassage_Low_P_Timer_s + (tScan_Cycle_Time_ms / 1000.0);
    IF rCrossPassage_Low_P_Timer_s >= 10.0 THEN
        dwAlarm_Word_Warning := dwAlarm_Word_Warning OR 16#00000004; (* Bit 2: Cross Passage Lost *)
    END_IF;
ELSE
    rCrossPassage_Low_P_Timer_s := 0.0;
END_IF;

(* Alarm 7: Jet Fan Motor Winding Over-Temperature (PT100 >= 140 C) *)
IF rJetFan_Motor_Max_Winding_T_degC >= 140.0 THEN
    rJetFan_Motor_Hot_Timer_s := rJetFan_Motor_Hot_Timer_s + (tScan_Cycle_Time_ms / 1000.0);
    IF rJetFan_Motor_Hot_Timer_s >= 5.0 THEN
        dwAlarm_Word_Warning := dwAlarm_Word_Warning OR 16#00000008; (* Bit 3: Fan Winding Hot *)
    END_IF;
ELSE
    rJetFan_Motor_Hot_Timer_s := 0.0;
END_IF;

(* Alarm 8: TMR Sensor Discrepancy Warnings *)
IF bCO_Sensor_A_Fault OR bCO_Sensor_B_Fault OR bCO_Sensor_C_Fault THEN
    dwAlarm_Word_Warning := dwAlarm_Word_Warning OR 16#00000010; (* Bit 4: CO Sensor TMR *)
END_IF;

IF bVis_Sensor_A_Fault OR bVis_Sensor_B_Fault OR bVis_Sensor_C_Fault THEN
    dwAlarm_Word_Warning := dwAlarm_Word_Warning OR 16#00000020; (* Bit 5: Visibility TMR *)
END_IF;

IF bHeat_Sensor_A_Fault OR bHeat_Sensor_B_Fault OR bHeat_Sensor_C_Fault THEN
    dwAlarm_Word_Warning := dwAlarm_Word_Warning OR 16#00000040; (* Bit 6: Heat Cable TMR *)
END_IF;

(* Pack Tunnel Status Word *)
IF bTunnel_Fire_Confirmed THEN
    dwTunnel_Status_Word := dwTunnel_Status_Word OR 16#00000001; (* Bit 0: Fire Mode *)
END_IF;

IF bPortal_Closure_Traffic_Gate_Cmd THEN
    dwTunnel_Status_Word := dwTunnel_Status_Word OR 16#00000002; (* Bit 1: Portals Closed *)
END_IF;

IF bZonal_Deluge_WaterMist_Valve_Cmd THEN
    dwTunnel_Status_Word := dwTunnel_Status_Word OR 16#00000004; (* Bit 2: Deluge Active *)
END_IF;

IF bSmoke_Extraction_Damper_Open_Cmd THEN
    dwTunnel_Status_Word := dwTunnel_Status_Word OR 16#00000008; (* Bit 3: Extraction Damper Open *)
END_IF;

IF bCrossPassage_Pressurization_Fan_Cmd THEN
    dwTunnel_Status_Word := dwTunnel_Status_Word OR 16#00000010; (* Bit 4: Cross Passage Fan Run *)
END_IF;

IF bSupervisory_Auto_Enable THEN
    dwTunnel_Status_Word := dwTunnel_Status_Word OR 16#00000020; (* Bit 5: Auto Supervisory Permissive *)
END_IF;

(* Pack State Code into Status Word Bits 8..11 *)
dwTunnel_Status_Word := dwTunnel_Status_Word OR SHL(INT_TO_DWORD(eCurrent_State), 8);

(* Pack Active Jet Fan Forward Count into Status Word Bits 16..20 *)
dwTunnel_Status_Word := dwTunnel_Status_Word OR SHL(INT_TO_DWORD(nJetFan_Active_Forward_Clusters), 16);
""")

# Closing
st_code_parts.append("""
END_FUNCTION_BLOCK
""")

full_st_code = "".join(st_code_parts)

print(f"Generated ST character count: {len(full_st_code)}")

dataset_record = {
    "messages": [
        {
            "role": "user",
            "content": prompt
        },
        {
            "role": "assistant",
            "content": f"```iec-st\n{full_st_code}```"
        }
    ]
}

target_file = "data/swarm_raw/agent_6602b831.json"
os.makedirs("data/swarm_raw", exist_ok=True)

with open(target_file, "w", encoding="utf-8") as f:
    json.dump(dataset_record, f, indent=2, ensure_ascii=False)

print(f"File saved to {target_file}")
print(f"Assistant content character count: {len(dataset_record['messages'][1]['content'])}")

# Run validation
proc = subprocess.run(["python", "validate_iec.py", target_file], capture_output=True, text=True)
print("Validator Output:")
print(proc.stdout)
if proc.stderr:
    print("Validator Errors:", proc.stderr)

if "ALL VALIDATION CHECKS PASSED PERFECTLY!" in proc.stdout:
    print("VALIDATION SUCCEEDED!")
else:
    print("VALIDATION FAILED!")
