# desal_builder/part6_fsm_logic.py
# Phase 4: Deterministic 14-Stage Production, CIP & Emergency Depressurization FSM

def get_part6_fsm_logic():
    return """
(* ====================================================================================================
   PHASE 4: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)
   Deterministic Sequencing Architecture for 50,000 m3/day SWRO Industrial Desalination Train:
     State 0:  STATE_0_STANDBY                 - System Idle, Lockouts Verified, Permissives Polled
     State 1:  STATE_1_LP_FEED_PRIME           - LP Intake Pump Running, Air Venting & Deaeration
     State 2:  STATE_2_CHEM_PRECONDITION       - SBS Dechlorination (ORP < 180 mV) & Antiscalant Dosing
     State 3:  STATE_3_LP_FLUSH_HEADER_EQ      - Low Pressure Membrane Purge & Rack Hydrostatic Fill
     State 4:  STATE_4_HP_SOFT_RAMP            - High Pressure Pump Controlled VFD Acceleration (0.5 bar/s)
     State 5:  STATE_5_ERD_WHEEL_ENGAGE        - Isobaric Ceramic Rotor PX Spin-up & Brine Pressurization
     State 6:  STATE_6_ERD_BOOSTER_SYNC        - PX Booster VFD Ramp to Balance Manifold Differential Head
     State 7:  STATE_7_PERMEATE_PRODUCTION     - Steady Production, Permeate Forwarding, Active MPC Optimization
     State 8:  STATE_8_SALINITY_FLUX_TRIM      - Salinity Surge & Temperature Drop Trim, Recovery Clamping
     State 9:  STATE_9_ANTISCALANT_AUTOTUNE    - Real-Time Stiff & Davis Scaling Index Chemical Dosage Modulator
     State 10: STATE_10_SCHEDULED_LP_PERM_FLUSH- Controlled Shutdown LP Permeate Displacement Flush (1.5 Volume)
     State 11: STATE_11_CIP_ACID_CLEAN_SOAK    - Acid Cleaning Loop (pH 2.0 - 2.5) for Carbonate/Iron Scale
     State 12: STATE_12_CIP_CAUSTIC_DISINFECT  - Alkaline Cleaning Loop (pH 11.0 - 11.5) for Biofilm & Organics
     State 13: STATE_13_FAST_EMERGENCY_DEPRESS - Hard Safety Fast Emergency Depressurization (FED: 75 -> 5 bar)
   ==================================================================================================== *)

(* Master State Timer Increment *)
rFsmTimer_sec := rFsmTimer_sec + rCycleTime_sec;
rFsmStepTimer_sec := rFsmStepTimer_sec + rCycleTime_sec;
rFsmStateElapsedTime_sec := rFsmTimer_sec;

(* Emergency Fast Depressurization Preemption Guard *)
IF bEmergencyDepressurize OR bCriticalTripActive THEN
    IF nFsmState <> 13 THEN
        nFsmNextState := 13;
        nFsmState := 13;
        rFsmTimer_sec := 0.0;
        bStateFirstScan := TRUE;
    END_IF;
END_IF;

CASE nFsmState OF

    (* ------------------------------------------------------------------------------------------------
       STATE 0: STANDBY & PRE-FLIGHT VERIFICATION
       ------------------------------------------------------------------------------------------------ *)
    0:
        sFsmStateName := 'STATE_0_STANDBY';
        bSystemRunning := FALSE;
        bSequenceComplete := FALSE;
        bPermeateOffSpecDiverted := FALSE;
        bCipCycleActive := FALSE;

        (* Actuators Inactive & Safe Isolated *)
        rHppVfdSpeedReference_Hz   := 0.0;
        rPxBpVfdSpeedReference_Hz  := 0.0;
        rBrineThrottleValveCmd_pct := 100.0; (* Full open to prevent accidental pressure traps *)
        rSbsDosingPumpStroke_pct   := 0.0;
        rAntiscalantDosingStroke_pct := 0.0;
        rPermeateDivertValveCmd_pct := 100.0; (* Divert open on standby *)
        rLpPermeateFlushPumpCmd_pct := 0.0;
        rCipCirculationPumpCmd_pct := 0.0;

        (* Motorized Valve Positions *)
        bOpenLpFeedInletValve          := FALSE;
        bOpenHpFeedHeaderValve         := FALSE;
        bOpenErdHpBrineValve           := FALSE;
        bOpenErdLpSeawaterValve        := FALSE;
        bOpenFastDepressurizeDumpValve := FALSE;
        bOpenPermeateProductValve      := FALSE;
        bOpenCipSuctionValve           := FALSE;
        bOpenCipReturnValve            := FALSE;

        (* State Transitions *)
        IF bEnable AND bStartCommand AND NOT bCriticalTripActive THEN
            nFsmNextState := 1;
            nFsmState := 1;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        ELSIF bCipInitiate AND NOT bCriticalTripActive THEN
            IF bCipTypeCaustic THEN
                nFsmNextState := 12;
                nFsmState := 12;
            ELSE
                nFsmNextState := 11;
                nFsmState := 11;
            END_IF;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 1: LOW PRESSURE INTAKE PRIMING & DEAERATION
       Opens intake valves, energizes LP feed pumps, and purges entrapped air from cartridge filters.
       ------------------------------------------------------------------------------------------------ *)
    1:
        sFsmStateName := 'STATE_1_LP_FEED_PRIME';
        bSystemRunning := FALSE;
        bSequenceComplete := FALSE;

        bOpenLpFeedInletValve          := TRUE;
        bOpenHpFeedHeaderValve         := FALSE;
        bOpenErdHpBrineValve           := FALSE;
        bOpenErdLpSeawaterValve        := TRUE;
        bOpenFastDepressurizeDumpValve := FALSE;
        bOpenPermeateProductValve      := FALSE;

        rHppVfdSpeedReference_Hz   := 0.0;
        rPxBpVfdSpeedReference_Hz  := 0.0;
        rBrineThrottleValveCmd_pct := 100.0;
        rPermeateDivertValveCmd_pct := 100.0;
        rLpPermeateFlushPumpCmd_pct := 0.0;

        (* State Transition Guards *)
        IF bStopCommand THEN
            nFsmNextState := 0;
            nFsmState := 0;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        ELSIF (rFsmTimer_sec >= 45.0) AND (rVoted_PT101_IntakePress_bar >= 2.50) 
              AND (rCartridgeFilterDp_bar <= 0.85) THEN
            (* Cartridge filters flooded and intake head established *)
            nFsmNextState := 2;
            nFsmState := 2;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        ELSIF rFsmTimer_sec >= 180.0 THEN
            (* Priming Timeout Failure *)
            dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; (* Low Intake Pressure Timeout Trip *)
            nFsmNextState := 13;
            nFsmState := 13;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 2: CHEMICAL PRE-CONDITIONING (DECHLORINATION & ANTISCALANT)
       Meters Sodium Bisulfite (SBS) to scavenge free chlorine (ORP < 180 mV) and starts Antiscalant.
       ------------------------------------------------------------------------------------------------ *)
    2:
        sFsmStateName := 'STATE_2_CHEM_PRECONDITION';
        bOpenLpFeedInletValve   := TRUE;
        bOpenErdLpSeawaterValve := TRUE;

        (* Proportional SBS Dosing based on Voted ORP Reading *)
        IF rVoted_AT102_FeedOrp_mV > 220.0 THEN
            rSbsDosingPumpStroke_pct := 75.0;
        ELSIF rVoted_AT102_FeedOrp_mV > 180.0 THEN
            rSbsDosingPumpStroke_pct := 55.0;
        ELSE
            rSbsDosingPumpStroke_pct := 35.0;
        END_IF;

        (* Stoichiometric Baseline Antiscalant Dosing (~2.5 ppm target) *)
        rAntiscalantDosingStroke_pct := 40.0;

        (* State Transition Guards *)
        IF bStopCommand THEN
            nFsmNextState := 0;
            nFsmState := 0;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        ELSIF (rFsmTimer_sec >= 30.0) AND (rVoted_AT102_FeedOrp_mV <= 185.0) 
              AND (rSbsDayTankLevel_pct >= 15.0) AND (rAntiscalantDayTankLevel_pct >= 15.0) THEN
            (* Chlorine safely neutralized and antiscalant active *)
            nFsmNextState := 3;
            nFsmState := 3;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        ELSIF rFsmTimer_sec >= 120.0 THEN
            (* Dechlorination Failure Timeout: High ORP will destroy polyamide membranes *)
            dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; (* ORP Neutralization Timeout Trip *)
            nFsmNextState := 13;
            nFsmState := 13;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 3: LOW PRESSURE MEMBRANE FLUSH & HEADER EQUALIZATION
       Displaces stagnant water, equalizes rack headers, verifies seal integrity.
       ------------------------------------------------------------------------------------------------ *)
    3:
        sFsmStateName := 'STATE_3_LP_FLUSH_HEADER_EQ';
        bOpenLpFeedInletValve   := TRUE;
        bOpenHpFeedHeaderValve  := TRUE;
        bOpenErdHpBrineValve    := TRUE;
        bOpenErdLpSeawaterValve := TRUE;
        bOpenPermeateProductValve := FALSE;
        rPermeateDivertValveCmd_pct := 100.0;
        rBrineThrottleValveCmd_pct  := 100.0;

        IF bStopCommand THEN
            nFsmNextState := 0;
            nFsmState := 0;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        ELSIF rFsmTimer_sec >= 60.0 THEN
            (* Flush complete, racks filled with fresh de-chlorinated seawater *)
            nFsmNextState := 4;
            nFsmState := 4;
            rFsmTimer_sec := 0.0;
            rHppRampTarget_Hz := 30.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 4: HIGH PRESSURE PUMP SOFT RAMP-UP
       Accelerates HPP VFD at controlled rate (max 0.5 bar/s) to prevent telescoping damage.
       ------------------------------------------------------------------------------------------------ *)
    4:
        sFsmStateName := 'STATE_4_HP_SOFT_RAMP';
        bOpenLpFeedInletValve   := TRUE;
        bOpenHpFeedHeaderValve  := TRUE;
        bOpenErdHpBrineValve    := TRUE;
        bOpenErdLpSeawaterValve := TRUE;

        (* Controlled Frequency Ramp-up *)
        IF rHppVfdSpeedReference_Hz < 48.50 THEN
            rHppVfdSpeedReference_Hz := rHppVfdSpeedReference_Hz + (0.50 * rCycleTime_sec);
        ELSE
            rHppVfdSpeedReference_Hz := 48.50;
        END_IF;

        (* Progressive Throttling of Brine Valve to build backpressure *)
        IF rBrineThrottleValveCmd_pct > 65.0 THEN
            rBrineThrottleValveCmd_pct := rBrineThrottleValveCmd_pct - (1.0 * rCycleTime_sec);
        ELSE
            rBrineThrottleValveCmd_pct := 65.0;
        END_IF;

        (* State Transition Guards *)
        IF bStopCommand THEN
            nFsmNextState := 10;
            nFsmState := 10;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        ELSIF (rVoted_PT201_HpFeedPress_bar >= 58.0) AND (rFsmTimer_sec >= 45.0) THEN
            (* Operating pressure threshold reached -> engage isobaric ERD rotor *)
            nFsmNextState := 5;
            nFsmState := 5;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        ELSIF rFsmTimer_sec >= 180.0 THEN
            (* Soft Ramp Failure: Target pressure not achieved *)
            dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; (* HPP Soft Ramp Timeout Trip *)
            nFsmNextState := 13;
            nFsmState := 13;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 5: ERD ISOBARIC CERAMIC ROTOR ENGAGEMENT
       Allows high-pressure brine to rotate PX ceramic rotor, transferring energy to low-pressure feed.
       ------------------------------------------------------------------------------------------------ *)
    5:
        sFsmStateName := 'STATE_5_ERD_WHEEL_ENGAGE';
        bOpenErdHpBrineValve    := TRUE;
        bOpenErdLpSeawaterValve := TRUE;

        (* Hold HPP at stable base load *)
        rHppVfdSpeedReference_Hz := 48.50;

        (* Modulate Brine Valve to stabilize ERD Differential Pressure *)
        IF (rVoted_PT201_HpFeedPress_bar - rVoted_PT501_PxDischPress_bar) > 4.0 THEN
            rBrineThrottleValveCmd_pct := rBrineThrottleValveCmd_pct + (0.5 * rCycleTime_sec);
        ELSIF (rVoted_PT201_HpFeedPress_bar - rVoted_PT501_PxDischPress_bar) < 1.5 THEN
            rBrineThrottleValveCmd_pct := rBrineThrottleValveCmd_pct - (0.5 * rCycleTime_sec);
        END_IF;

        (* State Transition Guards *)
        IF bStopCommand THEN
            nFsmNextState := 10;
            nFsmState := 10;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        ELSIF (rFsmTimer_sec >= 30.0) AND (rVoted_FT401_ErdBrineFlow_m3h >= 1200.0) 
              AND (rObservedErdEnergyRecovery_pct >= 90.0) THEN
            (* ERD rotor stabilized with balanced hydrodynamic flow *)
            nFsmNextState := 6;
            nFsmState := 6;
            rFsmTimer_sec := 0.0;
            rPxBpRampTarget_Hz := 30.0;
            bStateFirstScan := TRUE;
        ELSIF rFsmTimer_sec >= 120.0 THEN
            (* ERD Rotor Stall / Differential Pressure Anomaly *)
            dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; (* ERD Engagement Timeout Trip *)
            nFsmNextState := 13;
            nFsmState := 13;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 6: ERD BOOSTER PUMP SYNCHRONIZATION
       Ramps PX Booster Pump to equalize ERD pressurized feed with HPP discharge manifold.
       ------------------------------------------------------------------------------------------------ *)
    6:
        sFsmStateName := 'STATE_6_ERD_BOOSTER_SYNC';
        
        (* Ramp Booster VFD *)
        IF rPxBpVfdSpeedReference_Hz < 42.0 THEN
            rPxBpVfdSpeedReference_Hz := rPxBpVfdSpeedReference_Hz + (1.0 * rCycleTime_sec);
        ELSE
            rPxBpVfdSpeedReference_Hz := 42.0;
        END_IF;

        (* Fine Manifold Balance Trim *)
        IF ABS(rVoted_PT201_HpFeedPress_bar - rVoted_PT501_PxDischPress_bar) < 0.60 THEN
            (* Headers synchronized *)
            IF rFsmTimer_sec >= 20.0 THEN
                nFsmNextState := 7;
                nFsmState := 7;
                rFsmTimer_sec := 0.0;
                bStateFirstScan := TRUE;
            END_IF;
        END_IF;

        IF bStopCommand THEN
            nFsmNextState := 10;
            nFsmState := 10;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        ELSIF rFsmTimer_sec >= 90.0 THEN
            (* Booster synchronization timeout *)
            dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; (* Booster Sync Timeout Trip *)
            nFsmNextState := 13;
            nFsmState := 13;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 7: CONTINUOUS PERMEATE PRODUCTION (MPC ACTIVE OPTIMIZATION)
       Full steady state operation. MPC calculates optimal pump speeds to minimize SEC.
       ------------------------------------------------------------------------------------------------ *)
    7:
        sFsmStateName := 'STATE_7_PERMEATE_PRODUCTION';
        bSystemRunning := TRUE;
        bSequenceComplete := TRUE;

        bOpenLpFeedInletValve   := TRUE;
        bOpenHpFeedHeaderValve  := TRUE;
        bOpenErdHpBrineValve    := TRUE;
        bOpenErdLpSeawaterValve := TRUE;

        (* Permeate Quality Interlock: Product vs. Divert Valve *)
        IF rVoted_AT301_PermConduct_uS <= rMaxPermeateConductivity_uS THEN
            bOpenPermeateProductValve   := TRUE;
            rPermeateDivertValveCmd_pct := 0.0;
            bPermeateOffSpecDiverted    := FALSE;
        ELSE
            (* High conductivity: divert to outfall drain *)
            bOpenPermeateProductValve   := FALSE;
            rPermeateDivertValveCmd_pct := 100.0;
            bPermeateOffSpecDiverted    := TRUE;
        END_IF;

        (* Pass Optimal Control Commands from Phase 3 MPC Solver *)
        rHppVfdSpeedReference_Hz     := u_mpc_opt[1];
        rPxBpVfdSpeedReference_Hz    := u_mpc_opt[2];
        rBrineThrottleValveCmd_pct   := u_mpc_opt[3];
        rAntiscalantDosingStroke_pct := u_mpc_opt[4];
        rSbsDosingPumpStroke_pct     := u_mpc_opt[5];

        (* State Transitions *)
        IF bStopCommand THEN
            nFsmNextState := 10;
            nFsmState := 10;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        ELSIF (rObservedRecoveryRatio_pct > 44.5) OR (rRawSeawaterTds_ppm > 42000.0) THEN
            (* Salinity surge requires active trimming *)
            nFsmNextState := 8;
            nFsmState := 8;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        ELSIF rObservedScalingIndex_Lsi > 0.35 THEN
            (* Scaling risk requires autotuning *)
            nFsmNextState := 9;
            nFsmState := 9;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 8: SALINITY SURGE & FLUX RECOVERY TRIMMING
       Opens brine throttle, trims recovery down to 39.0% to prevent membrane crystallization.
       ------------------------------------------------------------------------------------------------ *)
    8:
        sFsmStateName := 'STATE_8_SALINITY_FLUX_TRIM';
        bSystemRunning := TRUE;

        (* Lower recovery target to relieve osmotic pressure *)
        IF rBrineThrottleValveCmd_pct < 78.0 THEN
            rBrineThrottleValveCmd_pct := rBrineThrottleValveCmd_pct + (0.8 * rCycleTime_sec);
        END_IF;

        (* Trim HPP slightly higher to overcome elevated osmotic pressure *)
        IF (rObservedPermeateFlow_m3h < rTargetPermeateFlow_m3h * 0.95) AND (rHppVfdSpeedReference_Hz < 56.0) THEN
            rHppVfdSpeedReference_Hz := rHppVfdSpeedReference_Hz + (0.2 * rCycleTime_sec);
        END_IF;

        (* Transition back to steady production once salinity stabilizes *)
        IF (rObservedRecoveryRatio_pct <= 42.0) AND (rRawSeawaterTds_ppm <= 39000.0) AND (rFsmTimer_sec >= 60.0) THEN
            nFsmNextState := 7;
            nFsmState := 7;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        ELSIF bStopCommand THEN
            nFsmNextState := 10;
            nFsmState := 10;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 9: DYNAMIC ANTISCALANT AUTO-TUNE (S&DSI STABILIZATION)
       Calculates real-time stoichiometric antiscalant requirement and ramps chemical stroke.
       ------------------------------------------------------------------------------------------------ *)
    9:
        sFsmStateName := 'STATE_9_ANTISCALANT_AUTOTUNE';
        bSystemRunning := TRUE;

        (* Modulate antiscalant stroke proportional to supersaturation index *)
        rAntiscalantDosingStroke_pct := LIMIT(40.0, 50.0 + (rObservedScalingIndex_Lsi * 45.0), 95.0);

        IF (rObservedScalingIndex_Lsi <= 0.15) AND (rFsmTimer_sec >= 90.0) THEN
            nFsmNextState := 7;
            nFsmState := 7;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        ELSIF bStopCommand THEN
            nFsmNextState := 10;
            nFsmState := 10;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 10: SCHEDULED LOW PRESSURE PERMEATE FLUSH (NORMAL SHUTDOWN)
       Isolates HPP and PX, runs LP permeate flush pump to purge brine from membrane elements.
       ------------------------------------------------------------------------------------------------ *)
    10:
        sFsmStateName := 'STATE_10_SCHEDULED_LP_PERM_FLUSH';
        bSystemRunning := FALSE;
        bSequenceComplete := FALSE;

        (* Ramp down high pressure pumps safely *)
        rHppVfdSpeedReference_Hz  := 0.0;
        rPxBpVfdSpeedReference_Hz := 0.0;
        rSbsDosingPumpStroke_pct  := 0.0;
        rAntiscalantDosingStroke_pct := 0.0;
        bOpenPermeateProductValve := FALSE;
        rPermeateDivertValveCmd_pct := 100.0;
        rBrineThrottleValveCmd_pct  := 100.0;

        (* Engage LP Permeate Flush Pump *)
        rLpPermeateFlushPumpCmd_pct := 85.0;

        (* Flush Duration: 180 seconds to replace complete train hydraulic volume *)
        IF rFsmTimer_sec >= 180.0 THEN
            rLpPermeateFlushPumpCmd_pct := 0.0;
            bOpenLpFeedInletValve       := FALSE;
            bOpenHpFeedHeaderValve      := FALSE;
            bOpenErdHpBrineValve        := FALSE;
            bOpenErdLpSeawaterValve     := FALSE;
            nFsmNextState := 0;
            nFsmState := 0;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 11: MEMBRANE CIP ACID CLEANING SOAK (pH 2.0 - 2.5)
       Dissolves inorganic carbonate, iron oxide and mineral scale using Citric/HCl recirculation.
       ------------------------------------------------------------------------------------------------ *)
    11:
        sFsmStateName := 'STATE_11_CIP_ACID_CLEAN_SOAK';
        bSystemRunning := FALSE;
        bCipCycleActive := TRUE;

        bOpenCipSuctionValve := TRUE;
        bOpenCipReturnValve  := TRUE;
        bOpenLpFeedInletValve := FALSE;
        bOpenHpFeedHeaderValve := FALSE;
        bOpenErdHpBrineValve := FALSE;
        bOpenPermeateProductValve := FALSE;
        rPermeateDivertValveCmd_pct := 100.0;

        (* CIP Sub-Step Sequencer *)
        IF rFsmTimer_sec < 600.0 THEN
            (* Sub-Step 1: Low-flow displacement and wetting (10 min) *)
            rCipCirculationPumpCmd_pct := 35.0;
        ELSIF rFsmTimer_sec < 2400.0 THEN
            (* Sub-Step 2: High-flow turbulent recirculation (30 min) *)
            rCipCirculationPumpCmd_pct := 80.0;
        ELSIF rFsmTimer_sec < 4200.0 THEN
            (* Sub-Step 3: Static Chemical Soak (30 min) *)
            rCipCirculationPumpCmd_pct := 0.0;
        ELSE
            (* Sub-Step 4: Permeate Neutralization Rinse (15 min) *)
            bOpenCipSuctionValve := FALSE;
            bOpenCipReturnValve := FALSE;
            rLpPermeateFlushPumpCmd_pct := 75.0;
            IF rFsmTimer_sec >= 5100.0 THEN
                rLpPermeateFlushPumpCmd_pct := 0.0;
                bCipCycleActive := FALSE;
                nFsmNextState := 0;
                nFsmState := 0;
                rFsmTimer_sec := 0.0;
                bStateFirstScan := TRUE;
            END_IF;
        END_IF;

        IF bStopCommand THEN
            nFsmNextState := 0;
            nFsmState := 0;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 12: MEMBRANE CIP CAUSTIC / ALKALINE DISINFECTION SOAK (pH 11.0 - 11.5)
       Hydrolyzes and dissolves organic foulants, extracellular polysaccharides, and biofilms.
       ------------------------------------------------------------------------------------------------ *)
    12:
        sFsmStateName := 'STATE_12_CIP_CAUSTIC_DISINFECT';
        bSystemRunning := FALSE;
        bCipCycleActive := TRUE;

        bOpenCipSuctionValve := TRUE;
        bOpenCipReturnValve  := TRUE;
        bOpenLpFeedInletValve := FALSE;
        bOpenHpFeedHeaderValve := FALSE;
        bOpenErdHpBrineValve := FALSE;
        bOpenPermeateProductValve := FALSE;
        rPermeateDivertValveCmd_pct := 100.0;

        IF rFsmTimer_sec < 600.0 THEN
            (* Sub-Step 1: Low-flow displacement (10 min) *)
            rCipCirculationPumpCmd_pct := 40.0;
        ELSIF rFsmTimer_sec < 3000.0 THEN
            (* Sub-Step 2: Heated alkaline recirculation (40 min, 35-40 C) *)
            rCipCirculationPumpCmd_pct := 85.0;
        ELSIF rFsmTimer_sec < 5400.0 THEN
            (* Sub-Step 3: Extended deep chemical soak (40 min) *)
            rCipCirculationPumpCmd_pct := 0.0;
        ELSE
            (* Sub-Step 4: Final demineralized water rinse (20 min) *)
            bOpenCipSuctionValve := FALSE;
            bOpenCipReturnValve := FALSE;
            rLpPermeateFlushPumpCmd_pct := 85.0;
            IF rFsmTimer_sec >= 6600.0 THEN
                rLpPermeateFlushPumpCmd_pct := 0.0;
                bCipCycleActive := FALSE;
                nFsmNextState := 0;
                nFsmState := 0;
                rFsmTimer_sec := 0.0;
                bStateFirstScan := TRUE;
            END_IF;
        END_IF;

        IF bStopCommand THEN
            nFsmNextState := 0;
            nFsmState := 0;
            rFsmTimer_sec := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 13: FAST EMERGENCY DEPRESSURIZATION (FED TRIP)
       Hard trip lockout state. Snaps open emergency dump valves to depressurize train to < 5 bar in < 4 s.
       ------------------------------------------------------------------------------------------------ *)
    13:
        sFsmStateName := 'STATE_13_FAST_EMERGENCY_DEPRESS';
        bSystemRunning := FALSE;
        bSequenceComplete := FALSE;

        (* Instantaneous Motor Trips *)
        rHppVfdSpeedReference_Hz  := 0.0;
        rPxBpVfdSpeedReference_Hz := 0.0;
        rSbsDosingPumpStroke_pct  := 0.0;
        rAntiscalantDosingStroke_pct := 0.0;
        rLpPermeateFlushPumpCmd_pct := 0.0;
        rCipCirculationPumpCmd_pct  := 0.0;

        (* Snap open emergency dump and bypass valves *)
        bOpenFastDepressurizeDumpValve := TRUE;
        rBrineThrottleValveCmd_pct     := 100.0;
        rPermeateDivertValveCmd_pct    := 100.0;
        bOpenPermeateProductValve      := FALSE;

        (* Isolate high pressure headers *)
        bOpenLpFeedInletValve          := FALSE;
        bOpenHpFeedHeaderValve         := FALSE;
        bOpenErdHpBrineValve           := FALSE;
        bOpenErdLpSeawaterValve        := FALSE;

        (* Trip Reset Handler *)
        IF bResetFault AND NOT bCriticalTripActive AND NOT bEmergencyDepressurize THEN
            IF rVoted_PT201_HpFeedPress_bar <= 5.0 THEN
                bOpenFastDepressurizeDumpValve := FALSE;
                dwTripWord := 16#00000000;
                nFsmNextState := 0;
                nFsmState := 0;
                rFsmTimer_sec := 0.0;
                bStateFirstScan := TRUE;
            END_IF;
        END_IF;

    ELSE
        (* Failsafe unknown state catch *)
        nFsmNextState := 13;
        nFsmState := 13;
        rFsmTimer_sec := 0.0;
END_CASE;

(* Update Output Registers *)
nFsmCurrentState := nFsmState;
"""
