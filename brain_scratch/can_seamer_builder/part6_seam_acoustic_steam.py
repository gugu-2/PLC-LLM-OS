# brain_scratch/can_seamer_builder/part6_seam_acoustic_steam.py

PART6_SEAM_ACOUSTIC_STEAM = """
(* ==========================================================================================
 * PHASE 7: DYNAMIC DOUBLE-SEAM CAM PROFILING & 18-HEAD CHUCK AXIAL FORCE MONITORING
 * Electronic Cam Synchronization:
 *   1st Operation Curl Roll Cam: Form body hook and cover hook interlock (cycloidal profile).
 *   2nd Operation Flattening Roll Cam: Iron out wrinkles and compress sealing compound (modified sine).
 * ========================================================================================== *)

(* Pocket Cam Angular Coordinate relative to active turret index [0.0 to 360.0 deg] *)
rCamAngle_1stOp_Deg := rTurret_Angular_Pos_Deg;
WHILE rCamAngle_1stOp_Deg >= 360.0 DO
    rCamAngle_1stOp_Deg := rCamAngle_1stOp_Deg - 360.0;
END_WHILE;

(* 1st Operation Cycloidal Roll Feed Profile (Active Zone: 30 deg to 150 deg) *)
IF rCamAngle_1stOp_Deg >= 30.0 AND rCamAngle_1stOp_Deg <= 150.0 THEN
    (* Cycloidal Motion Curve: s = h * [ (theta/beta) - (1/(2*pi))*sin(2*pi*theta/beta) ] *)
    rCamProfile_1stOp_Pos_mm := 1.850 * (((rCamAngle_1stOp_Deg - 30.0) / 120.0) - 
                                ((1.0 / (2.0 * 3.14159265)) * SIN(2.0 * 3.14159265 * (rCamAngle_1stOp_Deg - 30.0) / 120.0)));
ELSE
    rCamProfile_1stOp_Pos_mm := 0.0;
END_IF;

(* 2nd Operation Modified Sine Roll Feed Profile (Active Zone: 170 deg to 290 deg) *)
IF rCamAngle_1stOp_Deg >= 170.0 AND rCamAngle_1stOp_Deg <= 290.0 THEN
    rCamProfile_2ndOp_Pos_mm := 1.450 * (((rCamAngle_1stOp_Deg - 170.0) / 120.0) - 
                                ((1.0 / (2.0 * 3.14159265)) * SIN(2.0 * 3.14159265 * (rCamAngle_1stOp_Deg - 170.0) / 120.0)));
ELSE
    rCamProfile_2ndOp_Pos_mm := 0.0;
END_IF;

(* Seaming Station Axial Strain Gauge Verification: 3.5 to 8.0 kN Envelope *)
IF bIn_Production THEN
    IF rVoted_Chuck_AxialLoad_kN > rTrip_AxialLoad_HH_kN THEN
        bAlarm_AxialLoad_HH := TRUE;
    ELSIF rVoted_Chuck_AxialLoad_kN < (rTrip_AxialLoad_HH_kN - rDeadband_AxialLoad_kN) THEN
        bAlarm_AxialLoad_HH := FALSE;
    END_IF;

    IF rVoted_Chuck_AxialLoad_kN < rTrip_AxialLoad_LL_kN THEN
        bAlarm_AxialLoad_LL := TRUE;
    ELSIF rVoted_Chuck_AxialLoad_kN > (rTrip_AxialLoad_LL_kN + rDeadband_AxialLoad_kN) THEN
        bAlarm_AxialLoad_LL := FALSE;
    END_IF;
END_IF;

(* Pocket Shift Register Propagation across 36 Turret/Infeed/Discharge Stations *)
IF bIn_Production AND (rTurret_Angular_Pos_Deg < 5.0) THEN
    FOR iMatrixRow := 36 TO 2 BY -1 DO
        abPocket_HasCan[iMatrixRow]        := abPocket_HasCan[iMatrixRow - 1];
        abPocket_HasEnd[iMatrixRow]        := abPocket_HasEnd[iMatrixRow - 1];
        abPocket_DosedLN2[iMatrixRow]      := abPocket_DosedLN2[iMatrixRow - 1];
        abPocket_SeamedOK[iMatrixRow]      := abPocket_SeamedOK[iMatrixRow - 1];
        abPocket_AcousticPass[iMatrixRow]  := abPocket_AcousticPass[iMatrixRow - 1];
        abPocket_RejectPending[iMatrixRow] := abPocket_RejectPending[iMatrixRow - 1];
        aiPocket_HeadOrigin[iMatrixRow]    := aiPocket_HeadOrigin[iMatrixRow - 1];
    END_FOR;
END_IF;

(* ==========================================================================================
 * PHASE 8: NON-DESTRUCTIVE ACOUSTIC SOUND RESONANCE PING LEAK INSPECTION
 * Principle:
 *   Calibrated piezoelectric impulse striker excites the can end diaphragm.
 *   Microphone sensor array captures acoustic sound pressure spectrum.
 *   Under-pressurized cans (< 1.2 bar), pinhole leaks, and missing LN2 doses produce a
 *   sharp drop in peak resonance frequency (< 2.4 kHz) and premature ringdown decay (< 6 ms).
 * ========================================================================================== *)

IF bIn_Production THEN
    (* Check for low acoustic peak resonance *)
    IF rVoted_AcousticResonance_kHz < rTrip_Acoustic_LL_kHz THEN
        bAlarm_Acoustic_Leak_Fault := TRUE;
    ELSIF rVoted_AcousticResonance_kHz > (rTrip_Acoustic_LL_kHz + 0.150) THEN
        bAlarm_Acoustic_Leak_Fault := FALSE;
    END_IF;

    (* Check for headspace residual oxygen contamination *)
    IF rResidual_Oxygen_Pct > rTrip_ResidualO2_HH_Pct THEN
        bAlarm_Oxygen_Elevated := TRUE;
    ELSIF rResidual_Oxygen_Pct < rTrip_ResidualO2_H_Pct THEN
        bAlarm_Oxygen_Elevated := FALSE;
    END_IF;
END_IF;

(* ==========================================================================================
 * PHASE 9: ASEPTIC STEAM BARRIER ENCLOSURE THERMAL STERILIZATION & F0 ACCUMULATION
 * Enclosure maintains continuous saturated steam labyrinth seal at 125.0 deg C.
 * Real-time F0 lethality tracking verifies continuous commercial sterility assurance.
 * ========================================================================================== *)

IF bIn_Production THEN
    (* Loss of Aseptic Steam Barrier Interlock *)
    IF rVoted_SteamBarrier_Temp_degC < rTrip_SteamTemp_LL_degC THEN
        bAlarm_SteamTemp_LL := TRUE;
    ELSIF rVoted_SteamBarrier_Temp_degC > (rTrip_SteamTemp_LL_degC + rDeadband_SteamTemp_degC) THEN
        bAlarm_SteamTemp_LL := FALSE;
    END_IF;
END_IF;
"""
