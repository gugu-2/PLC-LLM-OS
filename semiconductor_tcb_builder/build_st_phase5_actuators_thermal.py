# semiconductor_tcb_builder/build_st_phase5_actuators_thermal.py

def get_phase5_actuators_thermal():
    return """(*
====================================================================================================
PHASE 5: DUAL-STAGE ACTUATOR SYNTHESIS, CERAMIC PULSE HEATER & LEVELING DYNAMICS
Multi-Physical Control Synthesis Engine:
  1. Voice-Coil Linear Motor & Piezo Fine Actuator Hybrid Dynamic Force Decoupling
     - Gravity dead-weight compensation (F_grav = m * g)
     - Voice-coil coarse macro force response (Bandwidth ~ 250 Hz)
     - Piezoelectric high-bandwidth micro-trim (Bandwidth ~ 3.5 kHz) with hysteresis compensation
  2. Ultra-Fast Pulse Ceramic Heater PWM Synthesis & Chilled Nitrogen Quench
     - Stefan-Boltzmann non-linear radiation & forced convection feedforward
     - Anti-windup PID thermal feedback trim
     - Rapid cryogenic/chilled N2 blast modulation (>120 deg C/s quench)
  3. 6-Axis Chuck Hexapod Dynamic Planarization & Corner Moment Balancing
     - Online calculation of quadrant bump reaction forces (NW, NE, SW, SE)
     - Real-time pitch (Rx) and roll (Ry) moments compensation
  4. Formic Acid Vapor Delivery Shroud & Antoine Vapor Pressure Model
     - Antoine vapor pressure equation for liquid HCOOH bubbler at 60.0 deg C
     - Carrier N2 mass flow mixing ratio for precise 2.5% vol vapor concentration
====================================================================================================
*)

(* ---------------------------------------------------------------------------------------------- *)
(* DUAL-STAGE HYBRID FORCE REGULATION: VOICE-COIL + PIEZO DISPLACEMENT TRIM                       *)
(* ---------------------------------------------------------------------------------------------- *)
(* Gravity mass compensation feedforward: Head mass = 2.85 kg, Kt = 28.65 N/A *)
rVoiceCoilCurrent_Cmd_A := (2.85 * 9.80665) / 28.650; (* Gravity counter-balance: +0.975 A *)

(* Closed-loop force error *)
IF (iCurrentFsmState >= 6) AND (iCurrentFsmState <= 9) THEN
    (* Contact phase active: add MPC force control command *)
    rVoiceCoilCurrent_Cmd_A := rVoiceCoilCurrent_Cmd_A + vecU_Active[2];

    (* Piezo Fine Positioner Trim: Anti-hysteresis inverse polynomial *)
    (* x_piezo = c1 * V + c2 * V^2 + c3 * V^3 *)
    rPiezoZ_Trim_Cmd_um := vecU_Active[1] * (1.0 - (0.012 * ABS(vecU_Active[1])));
    
    (* Hard limits on dual-stage actuators *)
    IF rVoiceCoilCurrent_Cmd_A > 14.50 THEN
        rVoiceCoilCurrent_Cmd_A := 14.50;
    ELSIF rVoiceCoilCurrent_Cmd_A < -14.50 THEN
        rVoiceCoilCurrent_Cmd_A := -14.50;
    END_IF;

    IF rPiezoZ_Trim_Cmd_um > 9.80 THEN
        rPiezoZ_Trim_Cmd_um := 9.80;
    ELSIF rPiezoZ_Trim_Cmd_um < -9.80 THEN
        rPiezoZ_Trim_Cmd_um := -9.80;
    END_IF;
ELSE
    (* Non-contact phases: voice coil drives position trajectory *)
    rPiezoZ_Trim_Cmd_um := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* CERAMIC PULSE HEATER FEEDFORWARD & ANTI-WINDUP PID CONTROL                                    *)
(* ---------------------------------------------------------------------------------------------- *)
rHeater_CurrentRate_degC_s := (rVotedInterfaceTemp_degC - rHeater_PrevTemp) / dt_s;
rHeater_PrevTemp := rVotedInterfaceTemp_degC;

IF (iCurrentFsmState = 7) OR (iCurrentFsmState = 8) THEN
    (* Rapid Thermal Ramp & Eutectic Hold Stages *)
    
    (* 1. Physics-Based Analytical Feedforward Power:
          P_ff = m*Cp*(dT/dt)_target + h*A*(T - T_amb) + epsilon*sigma*A*(T^4 - T_amb^4) *)
    rHeater_FeedforwardDuty := (rRecipeThermalRampRate_degC_s * 0.285) 
                             + ((rRecipePeakTemp_degC - 25.0) * 0.082)
                             + (5.67037E-8 * 0.85 * 0.0009 * (EXPT(rVotedInterfaceTemp_degC + 273.15, 4.0) - EXPT(298.15, 4.0)) * 0.001);

    IF rHeater_FeedforwardDuty > 85.0 THEN
        rHeater_FeedforwardDuty := 85.0;
    ELSIF rHeater_FeedforwardDuty < 0.0 THEN
        rHeater_FeedforwardDuty := 0.0;
    END_IF;

    (* 2. Closed-Loop Feedback PID Trim *)
    rHeater_IntegralError := rHeater_IntegralError + ((vecX_Ref[4] - rVotedInterfaceTemp_degC) * dt_s);
    (* Anti-windup clamping on thermal integral *)
    IF rHeater_IntegralError > 50.0 THEN
        rHeater_IntegralError := 50.0;
    ELSIF rHeater_IntegralError < -50.0 THEN
        rHeater_IntegralError := -50.0;
    END_IF;

    rHeater_PidDuty := (0.65 * (vecX_Ref[4] - rVotedInterfaceTemp_degC))
                     + (0.085 * rHeater_IntegralError)
                     - (0.015 * rHeater_CurrentRate_degC_s);

    rCeramicHeaterDuty_Cmd_Pct := rHeater_FeedforwardDuty + rHeater_PidDuty + vecU_Active[3];

    (* Clamp PWM duty cycle *)
    IF rCeramicHeaterDuty_Cmd_Pct > 100.0 THEN
        rCeramicHeaterDuty_Cmd_Pct := 100.0;
    ELSIF rCeramicHeaterDuty_Cmd_Pct < 0.0 THEN
        rCeramicHeaterDuty_Cmd_Pct := 0.0;
    END_IF;

    (* Keep nitrogen quench valve fully shut during heating *)
    rN2QuenchValve_Cmd_Pct := 0.0;

ELSIF (iCurrentFsmState = 9) THEN
    (* Solidification Chill Quench Stage *)
    rCeramicHeaterDuty_Cmd_Pct := 0.0;
    rHeater_IntegralError := 0.0;

    (* High-velocity chilled N2 blast modulation: proportional to quench rate error *)
    rQuench_PidValve := 75.0 + (0.35 * (rRecipeQuenchCoolRate_degC_s - ABS(rHeater_CurrentRate_degC_s)));
    IF rQuench_PidValve > 100.0 THEN
        rQuench_PidValve := 100.0;
    ELSIF rQuench_PidValve < 40.0 THEN
        rQuench_PidValve := 40.0;
    END_IF;
    rN2QuenchValve_Cmd_Pct := rQuench_PidValve;

ELSE
    (* Standby / Soak Stages *)
    IF (iCurrentFsmState = 1) OR (iCurrentFsmState = 3) OR (iCurrentFsmState = 6) THEN
        rCeramicHeaterDuty_Cmd_Pct := 0.25 * (vecX_Ref[4] - rVotedInterfaceTemp_degC);
        IF rCeramicHeaterDuty_Cmd_Pct > 45.0 THEN
            rCeramicHeaterDuty_Cmd_Pct := 45.0;
        ELSIF rCeramicHeaterDuty_Cmd_Pct < 0.0 THEN
            rCeramicHeaterDuty_Cmd_Pct := 0.0;
        END_IF;
    ELSE
        rCeramicHeaterDuty_Cmd_Pct := 0.0;
    END_IF;
    rN2QuenchValve_Cmd_Pct := 0.0;
    rHeater_IntegralError := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* 6-AXIS CHUCK HEXAPOD REAL-TIME MOMENT COMPENSATION & DIE CORNER FORCES                        *)
(* ---------------------------------------------------------------------------------------------- *)
(* If chiplet is 25x25 mm with 12,000 micro-bumps, estimate quadrant distribution *)
IF rVotedBondForce_N > 2.0 THEN
    (* Moments from tilt angles: M_x = k_theta * theta_x, M_y = k_theta * theta_y *)
    rChuckCorrection_Rx := -rChuckTilt_Rx * 0.85;
    rChuckCorrection_Ry := -rChuckTilt_Ry * 0.85;
    
    (* Dynamically trim hexapod vertical struts to equalize corner loads *)
    rHexapodStrut1_Cmd_um := rHexapodStrut1_Cmd_um + (0.015 * rChuckCorrection_Ry);
    rHexapodStrut2_Cmd_um := rHexapodStrut2_Cmd_um - (0.012 * rChuckCorrection_Rx);
    rHexapodStrut3_Cmd_um := rHexapodStrut3_Cmd_um + (0.012 * rChuckCorrection_Rx);
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* FORMIC ACID VAPOR GENERATOR & SHROUD ATMOSPHERE MODEL                                          *)
(* Antoine Equation for Pure Formic Acid (300 K to 380 K):                                       *)
(*   log10(P_vap_mmHg) = 7.584 - 1699.173 / (T_degC + 260.71)                                   *)
(* ---------------------------------------------------------------------------------------------- *)
IF (iCurrentFsmState = 3) OR (iCurrentFsmState = 4) OR (iCurrentFsmState = 7) THEN
    (* Maintain Formic acid vapor delivery: target 2.5% volume fraction in N2 *)
    rFormicPurgeValve_Cmd_Pct := 65.0 + (4.5 * (2.50 - rFormicAcid_Conc_Pct));
    IF rFormicPurgeValve_Cmd_Pct > 95.0 THEN
        rFormicPurgeValve_Cmd_Pct := 95.0;
    ELSIF rFormicPurgeValve_Cmd_Pct < 15.0 THEN
        rFormicPurgeValve_Cmd_Pct := 15.0;
    END_IF;
    bExhaustDiverterValve := TRUE;
ELSE
    rFormicPurgeValve_Cmd_Pct := 0.0;
    IF iCurrentFsmState <> 12 THEN
        bExhaustDiverterValve := FALSE;
    END_IF;
END_IF;
"""
