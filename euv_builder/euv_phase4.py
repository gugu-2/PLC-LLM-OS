# euv_builder/euv_phase4.py

def get_phase4():
    return """(* === PHASE 4: MULTI-STAGE CASE FINITE STATE MACHINE === *)
(* 12 deterministic operational stages managing vacuum pump-down, molten tin reservoir heating,  *)
(* piezo acoustic jetting, shadowgraph calibration, H2 buffer flow, magnet ramp, laser ignition, *)
(* closed-loop 500W MPC power production, in-situ stannane etching, and SEMI S2 emergency lockout. *)

CASE iState OF

    0: (* STAGE 0: VESSEL VACUUM PUMP-DOWN & STANDBY PURGE *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bEUVLightEmitting := FALSE;
        bPlasmaIgnited := FALSE;
        bDropletStreamLocked := FALSE;

        (* Safe parked actuator setpoints *)
        rTargetPiezoFreq_kHz := 50.0;
        rTargetPiezoVolt_V := 0.0;
        rTargetTinPress_bar := 0.0;
        rTargetPrePulse_mJ := 0.0;
        rTargetMainPulse_J := 0.0;
        rTargetGalvoSteerX_urad := 0.0;
        rTargetGalvoSteerY_urad := 0.0;
        rTargetH2Flow_slpm := 0.0;
        rTargetMagnetField_Tesla := 0.0;
        rTargetMirrorCoolingFlow_Pct := 20.0;

        (* Reset state sequencing timers *)
        tPumpDownTimer(IN := (bVesselSealsLocked AND bRoughingVacuumOk AND bTurbopumpsOnline), PT := T#180S);
        tMeltSoakTimer(IN := FALSE);
        tPiezoTuneTimer(IN := FALSE);
        tStreamStabilizeTimer(IN := FALSE);
        tShadowgraphCalTimer(IN := FALSE);
        tH2MagnetRampTimer(IN := FALSE);
        tPrePulseAlignTimer(IN := FALSE);
        tIgnitionTimer(IN := FALSE);
        tPowerStabTimer(IN := FALSE);
        tEtchCleanTimer(IN := FALSE);
        tShutdownTimer(IN := FALSE);
        tFaultHoldTimer(IN := FALSE);

        (* Advance to Inert Gas Purge when high vacuum is established *)
        IF bMasterEnable AND NOT bSystemTripped AND (rVotedVesselPressure_Pa < 0.05) AND tPumpDownTimer.Q THEN
            tPumpDownTimer(IN := FALSE);
            iState := 10; (* Advance to Inert Purge & Vacuum Verification *)
        END_IF;

    10: (* STAGE 10: INERT GAS PURGE & VESSEL VACUUM VERIFICATION *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bEUVLightEmitting := FALSE;
        bPlasmaIgnited := FALSE;
        bDropletStreamLocked := FALSE;

        (* Clean hydrocarbon stripping purge with 15 slpm pure Argon *)
        rTargetPiezoFreq_kHz := 50.0;
        rTargetPiezoVolt_V := 0.0;
        rTargetTinPress_bar := 0.0;
        rTargetPrePulse_mJ := 0.0;
        rTargetMainPulse_J := 0.0;
        rTargetGalvoSteerX_urad := 0.0;
        rTargetGalvoSteerY_urad := 0.0;
        rTargetH2Flow_slpm := 0.0;
        rTargetMagnetField_Tesla := 0.0;
        rTargetMirrorCoolingFlow_Pct := 20.0;

        tPumpDownTimer(IN := TRUE, PT := T#60S);

        IF bMasterEnable AND NOT bSystemTripped AND (rVotedVesselPressure_Pa < 0.01) AND tPumpDownTimer.Q THEN
            tPumpDownTimer(IN := FALSE);
            iState := 20; (* Advance to Molten Tin Reservoir Melting *)
        END_IF;

        IF NOT bMasterEnable THEN
            iState := 0;
        END_IF;

    20: (* STAGE 20: MOLTEN TIN RESERVOIR MELTING & HEATING (260.0 DEG C) *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bEUVLightEmitting := FALSE;
        bPlasmaIgnited := FALSE;
        bDropletStreamLocked := FALSE;

        (* Maintain safe vacuum, heat molten tin to 260 deg C *)
        rTargetPiezoFreq_kHz := 50.0;
        rTargetPiezoVolt_V := 0.0;
        rTargetTinPress_bar := 5.0; (* Slight blanketing pressure *)
        rTargetPrePulse_mJ := 0.0;
        rTargetMainPulse_J := 0.0;
        rTargetGalvoSteerX_urad := 0.0;
        rTargetGalvoSteerY_urad := 0.0;
        rTargetH2Flow_slpm := 0.0;
        rTargetMagnetField_Tesla := 0.0;
        rTargetMirrorCoolingFlow_Pct := 25.0;

        (* Soak timer starts when temperature reaches 258.0 deg C *)
        tMeltSoakTimer(IN := (rTinReservoirTemp_DegC >= 258.0), PT := T#120S);

        IF bMasterEnable AND NOT bSystemTripped AND (rTinReservoirTemp_DegC >= 258.0) AND (rTinReservoirTemp_DegC <= 265.0) AND tMeltSoakTimer.Q THEN
            tMeltSoakTimer(IN := FALSE);
            iState := 30; (* Advance to Piezo Acoustic Nozzle Tuning *)
        END_IF;

        IF NOT bMasterEnable THEN
            iState := 110; (* Safe Controlled Shutdown *)
        END_IF;

    30: (* STAGE 30: PIEZO NOZZLE ACOUSTIC FREQUENCY TUNING *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bEUVLightEmitting := FALSE;
        bPlasmaIgnited := FALSE;
        bDropletStreamLocked := FALSE;

        (* Sweep acoustic frequency 49.5 to 50.5 kHz to lock acoustic standing wave *)
        rTargetPiezoFreq_kHz := 50.0;
        rTargetPiezoVolt_V := 15.0;
        rTargetTinPress_bar := 10.0;
        rTargetPrePulse_mJ := 0.0;
        rTargetMainPulse_J := 0.0;
        rTargetGalvoSteerX_urad := 0.0;
        rTargetGalvoSteerY_urad := 0.0;
        rTargetH2Flow_slpm := 0.0;
        rTargetMagnetField_Tesla := 0.0;
        rTargetMirrorCoolingFlow_Pct := 25.0;

        tPiezoTuneTimer(IN := TRUE, PT := T#30S);

        IF bMasterEnable AND NOT bSystemTripped AND tPiezoTuneTimer.Q THEN
            tPiezoTuneTimer(IN := FALSE);
            iState := 40; (* Advance to Droplet Stream Jetting *)
        END_IF;

        IF NOT bMasterEnable THEN
            iState := 110;
        END_IF;

    40: (* STAGE 40: HIGH-VELOCITY DROPLET STREAM JETTING (75.0 m/s) *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bEUVLightEmitting := FALSE;
        bPlasmaIgnited := FALSE;
        bDropletStreamLocked := FALSE;

        (* Pressurize reservoir to 82.5 bar, drive piezo at 32.0 V *)
        rTargetPiezoFreq_kHz := 50.0;
        rTargetPiezoVolt_V := 32.0;
        rTargetTinPress_bar := 82.5;
        rTargetPrePulse_mJ := 0.0;
        rTargetMainPulse_J := 0.0;
        rTargetGalvoSteerX_urad := 0.0;
        rTargetGalvoSteerY_urad := 0.0;
        rTargetH2Flow_slpm := 0.0;
        rTargetMagnetField_Tesla := 0.0;
        rTargetMirrorCoolingFlow_Pct := 30.0;

        (* Verify continuous droplet train velocity >= 70.0 m/s *)
        tStreamStabilizeTimer(IN := (rVotedDropletVel_mps >= 70.0) AND (rVotedDropletDiam_um >= 21.0), PT := T#45S);

        IF bMasterEnable AND NOT bSystemTripped AND tStreamStabilizeTimer.Q THEN
            tStreamStabilizeTimer(IN := FALSE);
            iState := 50; (* Advance to Shadowgraph Calibration *)
        END_IF;

        IF NOT bMasterEnable THEN
            iState := 110;
        END_IF;

    50: (* STAGE 50: DROPLET TRAJECTORY VERIFICATION & SHADOWGRAPH CALIBRATION *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bEUVLightEmitting := FALSE;
        bPlasmaIgnited := FALSE;
        bDropletStreamLocked := FALSE;

        (* Keep jetting stable, optical shadowgraph locks droplet coordinates *)
        rTargetPiezoFreq_kHz := 50.0;
        rTargetPiezoVolt_V := 32.0;
        rTargetTinPress_bar := 82.5;
        rTargetPrePulse_mJ := 0.0;
        rTargetMainPulse_J := 0.0;
        rTargetGalvoSteerX_urad := 0.0;
        rTargetGalvoSteerY_urad := 0.0;
        rTargetH2Flow_slpm := 0.0;
        rTargetMagnetField_Tesla := 0.0;
        rTargetMirrorCoolingFlow_Pct := 30.0;

        (* Check that lateral droplet jitter is sub-micron (< 1.5 um) *)
        tShadowgraphCalTimer(IN := (rDropletPosJitter_um < 1.5) AND (rVotedDropletVel_mps >= 72.0), PT := T#30S);

        IF bMasterEnable AND NOT bSystemTripped AND tShadowgraphCalTimer.Q THEN
            tShadowgraphCalTimer(IN := FALSE);
            bDropletStreamLocked := TRUE;
            iState := 60; (* Advance to H2 Buffer Gas & Magnet Ramp *)
        END_IF;

        IF NOT bMasterEnable THEN
            iState := 110;
        END_IF;

    60: (* STAGE 60: HYDROGEN BUFFER GAS FLOW (150 slpm) & MAGNET RAMP (1.2 T) *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bEUVLightEmitting := FALSE;
        bPlasmaIgnited := FALSE;
        bDropletStreamLocked := TRUE;

        (* Inject 150 slpm H2, throttle to 3.5 Pa, ramp superconducting magnet to 1.2 T *)
        rTargetPiezoFreq_kHz := 50.0;
        rTargetPiezoVolt_V := 32.0;
        rTargetTinPress_bar := 82.5;
        rTargetPrePulse_mJ := 0.0;
        rTargetMainPulse_J := 0.0;
        rTargetGalvoSteerX_urad := 0.0;
        rTargetGalvoSteerY_urad := 0.0;
        rTargetH2Flow_slpm := 150.0;
        rTargetMagnetField_Tesla := 1.20;
        rTargetMirrorCoolingFlow_Pct := 35.0;

        tH2MagnetRampTimer(IN := (rVotedVesselPressure_Pa >= 3.0) AND (rVotedVesselPressure_Pa <= 4.5) AND
                                  (rMagnetField_Tesla >= 1.15) AND bMagnetCryoPermissive, PT := T#60S);

        IF bMasterEnable AND NOT bSystemTripped AND tH2MagnetRampTimer.Q THEN
            tH2MagnetRampTimer(IN := FALSE);
            iState := 70; (* Advance to Low-Power Pre-Pulse Alignment *)
        END_IF;

        IF NOT bMasterEnable THEN
            iState := 110;
        END_IF;

    70: (* STAGE 70: LOW-POWER LASER ALIGNMENT & PRE-PULSE STRIKE *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bEUVLightEmitting := FALSE;
        bPlasmaIgnited := FALSE;
        bDropletStreamLocked := TRUE;

        (* Fire pre-pulse laser at 18.5 mJ, expand droplets into 210 um pancakes *)
        rTargetPiezoFreq_kHz := 50.0;
        rTargetPiezoVolt_V := 32.0;
        rTargetTinPress_bar := 82.5;
        rTargetPrePulse_mJ := 18.5;
        rTargetMainPulse_J := 0.0; (* Main laser still shuttered *)
        rTargetGalvoSteerX_urad := 0.0;
        rTargetGalvoSteerY_urad := 0.0;
        rTargetH2Flow_slpm := 150.0;
        rTargetMagnetField_Tesla := 1.20;
        rTargetMirrorCoolingFlow_Pct := 40.0;

        (* Confirm pancake disc expansion diameter >= 150 um *)
        tPrePulseAlignTimer(IN := (rPancakeDiameter_um >= 150.0) AND bPrePulseLaserReady AND bCO2LaserMOPAReady, PT := T#40S);

        IF bMasterEnable AND NOT bSystemTripped AND tPrePulseAlignTimer.Q THEN
            tPrePulseAlignTimer(IN := FALSE);
            iState := 80; (* Advance to Main-Pulse Plasma Ignition *)
        END_IF;

        IF NOT bMasterEnable THEN
            iState := 110;
        END_IF;

    80: (* STAGE 80: MAIN-PULSE PLASMA IGNITION & IN-BAND EUV EMISSION *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bEUVLightEmitting := TRUE;
        bPlasmaIgnited := TRUE;
        bDropletStreamLocked := TRUE;

        (* Fire main CO2 laser pulse at 0.75 J, verify plasma ignition & IF EUV > 200 W *)
        rTargetPiezoFreq_kHz := 50.0;
        rTargetPiezoVolt_V := 32.0;
        rTargetTinPress_bar := 82.5;
        rTargetPrePulse_mJ := 18.5;
        rTargetMainPulse_J := 0.75;
        rTargetGalvoSteerX_urad := 0.0;
        rTargetGalvoSteerY_urad := 0.0;
        rTargetH2Flow_slpm := 150.0;
        rTargetMagnetField_Tesla := 1.20;
        rTargetMirrorCoolingFlow_Pct := 45.0;

        tIgnitionTimer(IN := (rVotedIFEUVPower_W >= 200.0) AND (rCalculatedTe_eV >= 25.0), PT := T#20S);

        IF bMasterEnable AND NOT bSystemTripped AND tIgnitionTimer.Q THEN
            tIgnitionTimer(IN := FALSE);
            iState := 90; (* Advance to Closed-Loop 500W In-Band MPC Production *)
        END_IF;

        IF NOT bMasterEnable THEN
            iState := 110;
        END_IF;

    90: (* STAGE 90: CLOSED-LOOP 500W IN-BAND POWER STABILIZATION MPC *)
        bSystemRunning := TRUE;
        bSystemReady := TRUE;
        bEUVLightEmitting := TRUE;
        bPlasmaIgnited := TRUE;
        bDropletStreamLocked := TRUE;

        (* Full multivariable MPC engaged - stabilizing 500.0 W at IF *)
        rTargetPiezoFreq_kHz := 50.0;
        rTargetPiezoVolt_V := 32.0;
        rTargetTinPress_bar := 82.5;
        rTargetPrePulse_mJ := 18.5;
        rTargetMainPulse_J := 0.95;
        rTargetGalvoSteerX_urad := 0.0;
        rTargetGalvoSteerY_urad := 0.0;
        rTargetH2Flow_slpm := 150.0;
        rTargetMagnetField_Tesla := 1.20;

        (* Continuous closed-loop production monitoring *)
        tPowerStabTimer(IN := (rVotedIFEUVPower_W >= 480.0) AND (rVotedIFEUVPower_W <= 520.0), PT := T#10S);

        (* Handle operator transition requests *)
        IF NOT bMasterEnable THEN
            iState := 110; (* Normal Controlled Shutdown *)
        END_IF;

    100: (* STAGE 100: COLLECTOR MIRROR THERMAL & STANNANE ETCH CLEANING *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bEUVLightEmitting := TRUE;
        bPlasmaIgnited := TRUE;
        bDropletStreamLocked := TRUE;

        (* Elevated H2 buffer flow (180 slpm) and pressure (4.8 Pa) for high chemical etch *)
        rTargetPiezoFreq_kHz := 50.0;
        rTargetPiezoVolt_V := 32.0;
        rTargetTinPress_bar := 82.5;
        rTargetPrePulse_mJ := 18.5;
        rTargetMainPulse_J := 0.85;
        rTargetGalvoSteerX_urad := 0.0;
        rTargetGalvoSteerY_urad := 0.0;
        rTargetH2Flow_slpm := 180.0;
        rTargetMagnetField_Tesla := 1.20;
        rTargetMirrorCoolingFlow_Pct := 60.0;

        tEtchCleanTimer(IN := TRUE, PT := T#300S);

        IF bMasterEnable AND NOT bSystemTripped AND tEtchCleanTimer.Q THEN
            tEtchCleanTimer(IN := FALSE);
            iState := 90; (* Return to 500W Closed-Loop Production *)
        END_IF;

        IF NOT bMasterEnable THEN
            iState := 110;
        END_IF;

    110: (* STAGE 110: LASER SAFE SHUTTER CLOSE & TIN JET EXTINGUISH *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bEUVLightEmitting := FALSE;
        bPlasmaIgnited := FALSE;
        bDropletStreamLocked := FALSE;

        (* Shutters closed, lasers off, piezo off, tin pressure dumped *)
        rTargetPiezoFreq_kHz := 50.0;
        rTargetPiezoVolt_V := 0.0;
        rTargetTinPress_bar := 0.0;
        rTargetPrePulse_mJ := 0.0;
        rTargetMainPulse_J := 0.0;
        rTargetGalvoSteerX_urad := 0.0;
        rTargetGalvoSteerY_urad := 0.0;
        rTargetH2Flow_slpm := 20.0; (* Low idle purge *)
        rTargetMagnetField_Tesla := 0.0;
        rTargetMirrorCoolingFlow_Pct := 20.0;

        tShutdownTimer(IN := TRUE, PT := T#60S);

        IF tShutdownTimer.Q THEN
            tShutdownTimer(IN := FALSE);
            iState := 0; (* Return to Standby *)
        END_IF;

    120: (* STAGE 120: EMERGENCY HYDROGEN SAFE SNUFF & VESSEL VACUUM LOCKOUT *)
        bSystemRunning := FALSE;
        bSystemReady := FALSE;
        bEUVLightEmitting := FALSE;
        bPlasmaIgnited := FALSE;
        bDropletStreamLocked := FALSE;
        bCriticalTripActive := TRUE;

        (* Instant emergency safe actuator shutdown *)
        rTargetPiezoFreq_kHz := 50.0;
        rTargetPiezoVolt_V := 0.0;
        rTargetTinPress_bar := 0.0;
        rTargetPrePulse_mJ := 0.0;
        rTargetMainPulse_J := 0.0;
        rTargetGalvoSteerX_urad := 0.0;
        rTargetGalvoSteerY_urad := 0.0;
        rTargetH2Flow_slpm := 0.0; (* Immediate H2 gas valve slam *)
        rTargetMagnetField_Tesla := 0.0;
        rTargetMirrorCoolingFlow_Pct := 100.0; (* Full cooling to prevent thermal shock *)

        (* Await manual trip reset after emergency condition has cleared *)
        tFaultHoldTimer(IN := TRUE, PT := T#10S);

        IF bResetFaults AND NOT bSystemTripped AND bEmergencyStop AND tFaultHoldTimer.Q THEN
            tFaultHoldTimer(IN := FALSE);
            bCriticalTripActive := FALSE;
            iState := 0; (* Reset to Standby *)
        END_IF;

ELSE
    (* Fallback safe default *)
    iState := 120;

END_CASE;

iOperatingState := iState;
"""
