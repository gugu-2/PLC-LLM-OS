# cmp_polisher_builder/part3_tmr_observer.py

def get_part3():
    return """(*
========================================================================================================================
  PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS
  COVERS 5 PRIMARY INSTRUMENTATION CHANNELS WITH BUMPLESS DEGRADATION
========================================================================================================================
*)
(* ------------------------------------------------------------------------------------------------------------------ *)
(* 1. SPECTROMETRIC OPTICAL REFLECTANCE INTENSITY VOTING [%]                                                          *)
(* ------------------------------------------------------------------------------------------------------------------ *)
rOpt_Delta_AB := ABS(rOptReflectance_A_pct - rOptReflectance_B_pct);
rOpt_Delta_BC := ABS(rOptReflectance_B_pct - rOptReflectance_C_pct);
rOpt_Delta_CA := ABS(rOptReflectance_C_pct - rOptReflectance_A_pct);

IF (rOpt_Delta_AB > rOpt_DiscrepancyLimit_pct) OR (rOpt_Delta_BC > rOpt_DiscrepancyLimit_pct) OR (rOpt_Delta_CA > rOpt_DiscrepancyLimit_pct) THEN
    rOpt_DiscrepancyTimer_s := rOpt_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rOpt_DiscrepancyTimer_s >= rDiscrepancyPersistLimit_s THEN
        (* Channel Fault Isolation *)
        IF (rOpt_Delta_AB > rOpt_DiscrepancyLimit_pct) AND (rOpt_Delta_CA > rOpt_DiscrepancyLimit_pct) THEN
            bOpt_ChannelA_Valid := FALSE;   (* Channel A is deviant from both B and C *)
        ELSIF (rOpt_Delta_AB > rOpt_DiscrepancyLimit_pct) AND (rOpt_Delta_BC > rOpt_DiscrepancyLimit_pct) THEN
            bOpt_ChannelB_Valid := FALSE;   (* Channel B is deviant from both A and C *)
        ELSIF (rOpt_Delta_BC > rOpt_DiscrepancyLimit_pct) AND (rOpt_Delta_CA > rOpt_DiscrepancyLimit_pct) THEN
            bOpt_ChannelC_Valid := FALSE;   (* Channel C is deviant from both A and B *)
        END_IF;
    END_IF;
ELSE
    rOpt_DiscrepancyTimer_s := MAX(0.0, rOpt_DiscrepancyTimer_s - T_CYCLE_SEC * 0.5);
END_IF;

(* Evaluate Voting Mode and Compute Output *)
IF bOpt_ChannelA_Valid AND bOpt_ChannelB_Valid AND bOpt_ChannelC_Valid THEN
    nOpt_DegradedVotingMode := 3;   (* Full 2oo3 TMR Median Voting *)
    IF (rOptReflectance_A_pct >= rOptReflectance_B_pct AND rOptReflectance_A_pct <= rOptReflectance_C_pct) OR 
       (rOptReflectance_A_pct <= rOptReflectance_B_pct AND rOptReflectance_A_pct >= rOptReflectance_C_pct) THEN
        rVotedOpticalReflectance_pct := rOptReflectance_A_pct;
    ELSIF (rOptReflectance_B_pct >= rOptReflectance_A_pct AND rOptReflectance_B_pct <= rOptReflectance_C_pct) OR 
          (rOptReflectance_B_pct <= rOptReflectance_A_pct AND rOptReflectance_B_pct >= rOptReflectance_C_pct) THEN
        rVotedOpticalReflectance_pct := rOptReflectance_B_pct;
    ELSE
        rVotedOpticalReflectance_pct := rOptReflectance_C_pct;
    END_IF;
ELSIF bOpt_ChannelA_Valid AND bOpt_ChannelB_Valid THEN
    nOpt_DegradedVotingMode := 2;   (* 1oo2 Degraded Average AB *)
    rVotedOpticalReflectance_pct := (rOptReflectance_A_pct + rOptReflectance_B_pct) * 0.5;
ELSIF bOpt_ChannelB_Valid AND bOpt_ChannelC_Valid THEN
    nOpt_DegradedVotingMode := 2;   (* 1oo2 Degraded Average BC *)
    rVotedOpticalReflectance_pct := (rOptReflectance_B_pct + rOptReflectance_C_pct) * 0.5;
ELSIF bOpt_ChannelA_Valid AND bOpt_ChannelC_Valid THEN
    nOpt_DegradedVotingMode := 2;   (* 1oo2 Degraded Average AC *)
    rVotedOpticalReflectance_pct := (rOptReflectance_A_pct + rOptReflectance_C_pct) * 0.5;
ELSIF bOpt_ChannelA_Valid THEN
    nOpt_DegradedVotingMode := 1;   (* Single Remaining Channel A *)
    rVotedOpticalReflectance_pct := rOptReflectance_A_pct;
ELSIF bOpt_ChannelB_Valid THEN
    nOpt_DegradedVotingMode := 1;   (* Single Remaining Channel B *)
    rVotedOpticalReflectance_pct := rOptReflectance_B_pct;
ELSIF bOpt_ChannelC_Valid THEN
    nOpt_DegradedVotingMode := 1;   (* Single Remaining Channel C *)
    rVotedOpticalReflectance_pct := rOptReflectance_C_pct;
ELSE
    nOpt_DegradedVotingMode := 0;   (* Total Sensor Failure: Safe Default *)
    rVotedOpticalReflectance_pct := 0.0;
END_IF;

(* ------------------------------------------------------------------------------------------------------------------ *)
(* 2. IN-SITU HIGH-FREQUENCY EDDY CURRENT FILM THICKNESS VOTING [Angstrom]                                            *)
(* ------------------------------------------------------------------------------------------------------------------ *)
rEddy_Delta_AB := ABS(rEddyCurrent_Thick_A_Angstrom - rEddyCurrent_Thick_B_Angstrom);
rEddy_Delta_BC := ABS(rEddyCurrent_Thick_B_Angstrom - rEddyCurrent_Thick_C_Angstrom);
rEddy_Delta_CA := ABS(rEddyCurrent_Thick_C_Angstrom - rEddyCurrent_Thick_A_Angstrom);

IF (rEddy_Delta_AB > rEddy_DiscrepancyLimit_Angstrom) OR (rEddy_Delta_BC > rEddy_DiscrepancyLimit_Angstrom) OR (rEddy_Delta_CA > rEddy_DiscrepancyLimit_Angstrom) THEN
    rEddy_DiscrepancyTimer_s := rEddy_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rEddy_DiscrepancyTimer_s >= rDiscrepancyPersistLimit_s THEN
        IF (rEddy_Delta_AB > rEddy_DiscrepancyLimit_Angstrom) AND (rEddy_Delta_CA > rEddy_DiscrepancyLimit_Angstrom) THEN
            bEddy_ChannelA_Valid := FALSE;
        ELSIF (rEddy_Delta_AB > rEddy_DiscrepancyLimit_Angstrom) AND (rEddy_Delta_BC > rEddy_DiscrepancyLimit_Angstrom) THEN
            bEddy_ChannelB_Valid := FALSE;
        ELSIF (rEddy_Delta_BC > rEddy_DiscrepancyLimit_Angstrom) AND (rEddy_Delta_CA > rEddy_DiscrepancyLimit_Angstrom) THEN
            bEddy_ChannelC_Valid := FALSE;
        END_IF;
    END_IF;
ELSE
    rEddy_DiscrepancyTimer_s := MAX(0.0, rEddy_DiscrepancyTimer_s - T_CYCLE_SEC * 0.5);
END_IF;

IF bEddy_ChannelA_Valid AND bEddy_ChannelB_Valid AND bEddy_ChannelC_Valid THEN
    nEddy_DegradedVotingMode := 3;
    IF (rEddyCurrent_Thick_A_Angstrom >= rEddyCurrent_Thick_B_Angstrom AND rEddyCurrent_Thick_A_Angstrom <= rEddyCurrent_Thick_C_Angstrom) OR 
       (rEddyCurrent_Thick_A_Angstrom <= rEddyCurrent_Thick_B_Angstrom AND rEddyCurrent_Thick_A_Angstrom >= rEddyCurrent_Thick_C_Angstrom) THEN
        rVotedFilmThickness_Angstrom := rEddyCurrent_Thick_A_Angstrom;
    ELSIF (rEddyCurrent_Thick_B_Angstrom >= rEddyCurrent_Thick_A_Angstrom AND rEddyCurrent_Thick_B_Angstrom <= rEddyCurrent_Thick_C_Angstrom) OR 
          (rEddyCurrent_Thick_B_Angstrom <= rEddyCurrent_Thick_A_Angstrom AND rEddyCurrent_Thick_B_Angstrom >= rEddyCurrent_Thick_C_Angstrom) THEN
        rVotedFilmThickness_Angstrom := rEddyCurrent_Thick_B_Angstrom;
    ELSE
        rVotedFilmThickness_Angstrom := rEddyCurrent_Thick_C_Angstrom;
    END_IF;
ELSIF bEddy_ChannelA_Valid AND bEddy_ChannelB_Valid THEN
    nEddy_DegradedVotingMode := 2;
    rVotedFilmThickness_Angstrom := (rEddyCurrent_Thick_A_Angstrom + rEddyCurrent_Thick_B_Angstrom) * 0.5;
ELSIF bEddy_ChannelB_Valid AND bEddy_ChannelC_Valid THEN
    nEddy_DegradedVotingMode := 2;
    rVotedFilmThickness_Angstrom := (rEddyCurrent_Thick_B_Angstrom + rEddyCurrent_Thick_C_Angstrom) * 0.5;
ELSIF bEddy_ChannelA_Valid AND bEddy_ChannelC_Valid THEN
    nEddy_DegradedVotingMode := 2;
    rVotedFilmThickness_Angstrom := (rEddyCurrent_Thick_A_Angstrom + rEddyCurrent_Thick_C_Angstrom) * 0.5;
ELSIF bEddy_ChannelA_Valid THEN
    nEddy_DegradedVotingMode := 1;
    rVotedFilmThickness_Angstrom := rEddyCurrent_Thick_A_Angstrom;
ELSIF bEddy_ChannelB_Valid THEN
    nEddy_DegradedVotingMode := 1;
    rVotedFilmThickness_Angstrom := rEddyCurrent_Thick_B_Angstrom;
ELSIF bEddy_ChannelC_Valid THEN
    nEddy_DegradedVotingMode := 1;
    rVotedFilmThickness_Angstrom := rEddyCurrent_Thick_C_Angstrom;
ELSE
    nEddy_DegradedVotingMode := 0;
    rVotedFilmThickness_Angstrom := 0.0;
END_IF;

(* ------------------------------------------------------------------------------------------------------------------ *)
(* 3. PLATEN DIRECT-DRIVE REACTION TORQUE LOAD CELLS VOTING [Nm]                                                      *)
(* ------------------------------------------------------------------------------------------------------------------ *)
rTorq_Delta_AB := ABS(rPlatenTorque_A_Nm - rPlatenTorque_B_Nm);
rTorq_Delta_BC := ABS(rPlatenTorque_B_Nm - rPlatenTorque_C_Nm);
rTorq_Delta_CA := ABS(rPlatenTorque_C_Nm - rPlatenTorque_A_Nm);

IF (rTorq_Delta_AB > rTorq_DiscrepancyLimit_Nm) OR (rTorq_Delta_BC > rTorq_DiscrepancyLimit_Nm) OR (rTorq_Delta_CA > rTorq_DiscrepancyLimit_Nm) THEN
    rTorq_DiscrepancyTimer_s := rTorq_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rTorq_DiscrepancyTimer_s >= rDiscrepancyPersistLimit_s THEN
        IF (rTorq_Delta_AB > rTorq_DiscrepancyLimit_Nm) AND (rTorq_Delta_CA > rTorq_DiscrepancyLimit_Nm) THEN
            bTorq_ChannelA_Valid := FALSE;
        ELSIF (rTorq_Delta_AB > rTorq_DiscrepancyLimit_Nm) AND (rTorq_Delta_BC > rTorq_DiscrepancyLimit_Nm) THEN
            bTorq_ChannelB_Valid := FALSE;
        ELSIF (rTorq_Delta_BC > rTorq_DiscrepancyLimit_Nm) AND (rTorq_Delta_CA > rTorq_DiscrepancyLimit_Nm) THEN
            bTorq_ChannelC_Valid := FALSE;
        END_IF;
    END_IF;
ELSE
    rTorq_DiscrepancyTimer_s := MAX(0.0, rTorq_DiscrepancyTimer_s - T_CYCLE_SEC * 0.5);
END_IF;

IF bTorq_ChannelA_Valid AND bTorq_ChannelB_Valid AND bTorq_ChannelC_Valid THEN
    nTorq_DegradedVotingMode := 3;
    IF (rPlatenTorque_A_Nm >= rPlatenTorque_B_Nm AND rPlatenTorque_A_Nm <= rPlatenTorque_C_Nm) OR 
       (rPlatenTorque_A_Nm <= rPlatenTorque_B_Nm AND rPlatenTorque_A_Nm >= rPlatenTorque_C_Nm) THEN
        rVotedPlatenTorque_Nm := rPlatenTorque_A_Nm;
    ELSIF (rPlatenTorque_B_Nm >= rPlatenTorque_A_Nm AND rPlatenTorque_B_Nm <= rPlatenTorque_C_Nm) OR 
          (rPlatenTorque_B_Nm <= rPlatenTorque_A_Nm AND rPlatenTorque_B_Nm >= rPlatenTorque_C_Nm) THEN
        rVotedPlatenTorque_Nm := rPlatenTorque_B_Nm;
    ELSE
        rVotedPlatenTorque_Nm := rPlatenTorque_C_Nm;
    END_IF;
ELSIF bTorq_ChannelA_Valid AND bTorq_ChannelB_Valid THEN
    nTorq_DegradedVotingMode := 2;
    rVotedPlatenTorque_Nm := (rPlatenTorque_A_Nm + rPlatenTorque_B_Nm) * 0.5;
ELSIF bTorq_ChannelB_Valid AND bTorq_ChannelC_Valid THEN
    nTorq_DegradedVotingMode := 2;
    rVotedPlatenTorque_Nm := (rPlatenTorque_B_Nm + rPlatenTorque_C_Nm) * 0.5;
ELSIF bTorq_ChannelA_Valid AND bTorq_ChannelC_Valid THEN
    nTorq_DegradedVotingMode := 2;
    rVotedPlatenTorque_Nm := (rPlatenTorque_A_Nm + rPlatenTorque_C_Nm) * 0.5;
ELSIF bTorq_ChannelA_Valid THEN
    nTorq_DegradedVotingMode := 1;
    rVotedPlatenTorque_Nm := rPlatenTorque_A_Nm;
ELSIF bTorq_ChannelB_Valid THEN
    nTorq_DegradedVotingMode := 1;
    rVotedPlatenTorque_Nm := rPlatenTorque_B_Nm;
ELSIF bTorq_ChannelC_Valid THEN
    nTorq_DegradedVotingMode := 1;
    rVotedPlatenTorque_Nm := rPlatenTorque_C_Nm;
ELSE
    nTorq_DegradedVotingMode := 0;
    rVotedPlatenTorque_Nm := 0.0;
END_IF;

(* ------------------------------------------------------------------------------------------------------------------ *)
(* 4. WAFER CARRIER MEMBRANE ZONE 1 (CENTER) PRESSURE TRANSDUCERS VOTING [psi]                                        *)
(* ------------------------------------------------------------------------------------------------------------------ *)
rZ1P_Delta_AB := ABS(rZone1_Press_A_psi - rZone1_Press_B_psi);
rZ1P_Delta_BC := ABS(rZone1_Press_B_psi - rZone1_Press_C_psi);
rZ1P_Delta_CA := ABS(rZone1_Press_C_psi - rZone1_Press_A_psi);

IF (rZ1P_Delta_AB > rZ1P_DiscrepancyLimit_psi) OR (rZ1P_Delta_BC > rZ1P_DiscrepancyLimit_psi) OR (rZ1P_Delta_CA > rZ1P_DiscrepancyLimit_psi) THEN
    rZ1P_DiscrepancyTimer_s := rZ1P_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rZ1P_DiscrepancyTimer_s >= rDiscrepancyPersistLimit_s THEN
        IF (rZ1P_Delta_AB > rZ1P_DiscrepancyLimit_psi) AND (rZ1P_Delta_CA > rZ1P_DiscrepancyLimit_psi) THEN
            bZ1P_ChannelA_Valid := FALSE;
        ELSIF (rZ1P_Delta_AB > rZ1P_DiscrepancyLimit_psi) AND (rZ1P_Delta_BC > rZ1P_DiscrepancyLimit_psi) THEN
            bZ1P_ChannelB_Valid := FALSE;
        ELSIF (rZ1P_Delta_BC > rZ1P_DiscrepancyLimit_psi) AND (rZ1P_Delta_CA > rZ1P_DiscrepancyLimit_psi) THEN
            bZ1P_ChannelC_Valid := FALSE;
        END_IF;
    END_IF;
ELSE
    rZ1P_DiscrepancyTimer_s := MAX(0.0, rZ1P_DiscrepancyTimer_s - T_CYCLE_SEC * 0.5);
END_IF;

IF bZ1P_ChannelA_Valid AND bZ1P_ChannelB_Valid AND bZ1P_ChannelC_Valid THEN
    nZ1P_DegradedVotingMode := 3;
    IF (rZone1_Press_A_psi >= rZone1_Press_B_psi AND rZone1_Press_A_psi <= rZone1_Press_C_psi) OR 
       (rZone1_Press_A_psi <= rZone1_Press_B_psi AND rZone1_Press_A_psi >= rZone1_Press_C_psi) THEN
        rVotedZone1Press_psi := rZone1_Press_A_psi;
    ELSIF (rZone1_Press_B_psi >= rZone1_Press_A_psi AND rZone1_Press_B_psi <= rZone1_Press_C_psi) OR 
          (rZone1_Press_B_psi <= rZone1_Press_A_psi AND rZone1_Press_B_psi >= rZone1_Press_C_psi) THEN
        rVotedZone1Press_psi := rZone1_Press_B_psi;
    ELSE
        rVotedZone1Press_psi := rZone1_Press_C_psi;
    END_IF;
ELSIF bZ1P_ChannelA_Valid AND bZ1P_ChannelB_Valid THEN
    nZ1P_DegradedVotingMode := 2;
    rVotedZone1Press_psi := (rZone1_Press_A_psi + rZone1_Press_B_psi) * 0.5;
ELSIF bZ1P_ChannelB_Valid AND bZ1P_ChannelC_Valid THEN
    nZ1P_DegradedVotingMode := 2;
    rVotedZone1Press_psi := (rZone1_Press_B_psi + rZone1_Press_C_psi) * 0.5;
ELSIF bZ1P_ChannelA_Valid AND bZ1P_ChannelC_Valid THEN
    nZ1P_DegradedVotingMode := 2;
    rVotedZone1Press_psi := (rZone1_Press_A_psi + rZone1_Press_C_psi) * 0.5;
ELSIF bZ1P_ChannelA_Valid THEN
    nZ1P_DegradedVotingMode := 1;
    rVotedZone1Press_psi := rZone1_Press_A_psi;
ELSIF bZ1P_ChannelB_Valid THEN
    nZ1P_DegradedVotingMode := 1;
    rVotedZone1Press_psi := rZone1_Press_B_psi;
ELSIF bZ1P_ChannelC_Valid THEN
    nZ1P_DegradedVotingMode := 1;
    rVotedZone1Press_psi := rZone1_Press_C_psi;
ELSE
    nZ1P_DegradedVotingMode := 0;
    rVotedZone1Press_psi := 0.0;
END_IF;

(* ------------------------------------------------------------------------------------------------------------------ *)
(* 5. POLISHING PAD SURFACE NON-CONTACT INFRARED PYROMETERS VOTING [deg C]                                            *)
(* ------------------------------------------------------------------------------------------------------------------ *)
rPadT_Delta_AB := ABS(rPadIRTemp_A_degC - rPadIRTemp_B_degC);
rPadT_Delta_BC := ABS(rPadIRTemp_B_degC - rPadIRTemp_C_degC);
rPadT_Delta_CA := ABS(rPadIRTemp_C_degC - rPadIRTemp_A_degC);

IF (rPadT_Delta_AB > rPadT_DiscrepancyLimit_degC) OR (rPadT_Delta_BC > rPadT_DiscrepancyLimit_degC) OR (rPadT_Delta_CA > rPadT_DiscrepancyLimit_degC) THEN
    rPadT_DiscrepancyTimer_s := rPadT_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rPadT_DiscrepancyTimer_s >= rDiscrepancyPersistLimit_s THEN
        IF (rPadT_Delta_AB > rPadT_DiscrepancyLimit_degC) AND (rPadT_Delta_CA > rPadT_DiscrepancyLimit_degC) THEN
            bPadT_ChannelA_Valid := FALSE;
        ELSIF (rPadT_Delta_AB > rPadT_DiscrepancyLimit_degC) AND (rPadT_Delta_BC > rPadT_DiscrepancyLimit_degC) THEN
            bPadT_ChannelB_Valid := FALSE;
        ELSIF (rPadT_Delta_BC > rPadT_DiscrepancyLimit_degC) AND (rPadT_Delta_CA > rPadT_DiscrepancyLimit_degC) THEN
            bPadT_ChannelC_Valid := FALSE;
        END_IF;
    END_IF;
ELSE
    rPadT_DiscrepancyTimer_s := MAX(0.0, rPadT_DiscrepancyTimer_s - T_CYCLE_SEC * 0.5);
END_IF;

IF bPadT_ChannelA_Valid AND bPadT_ChannelB_Valid AND bPadT_ChannelC_Valid THEN
    nPadT_DegradedVotingMode := 3;
    IF (rPadIRTemp_A_degC >= rPadIRTemp_B_degC AND rPadIRTemp_A_degC <= rPadIRTemp_C_degC) OR 
       (rPadIRTemp_A_degC <= rPadIRTemp_B_degC AND rPadIRTemp_A_degC >= rPadIRTemp_C_degC) THEN
        rVotedPadTemp_degC := rPadIRTemp_A_degC;
    ELSIF (rPadIRTemp_B_degC >= rPadIRTemp_A_degC AND rPadIRTemp_B_degC <= rPadIRTemp_C_degC) OR 
          (rPadIRTemp_B_degC <= rPadIRTemp_A_degC AND rPadIRTemp_B_degC >= rPadIRTemp_C_degC) THEN
        rVotedPadTemp_degC := rPadIRTemp_B_degC;
    ELSE
        rVotedPadTemp_degC := rPadIRTemp_C_degC;
    END_IF;
ELSIF bPadT_ChannelA_Valid AND bPadT_ChannelB_Valid THEN
    nPadT_DegradedVotingMode := 2;
    rVotedPadTemp_degC := (rPadIRTemp_A_degC + rPadIRTemp_B_degC) * 0.5;
ELSIF bPadT_ChannelB_Valid AND bPadT_ChannelC_Valid THEN
    nPadT_DegradedVotingMode := 2;
    rVotedPadTemp_degC := (rPadIRTemp_B_degC + rPadIRTemp_C_degC) * 0.5;
ELSIF bPadT_ChannelA_Valid AND bPadT_ChannelC_Valid THEN
    nPadT_DegradedVotingMode := 2;
    rVotedPadTemp_degC := (rPadIRTemp_A_degC + rPadIRTemp_C_degC) * 0.5;
ELSIF bPadT_ChannelA_Valid THEN
    nPadT_DegradedVotingMode := 1;
    rVotedPadTemp_degC := rPadIRTemp_A_degC;
ELSIF bPadT_ChannelB_Valid THEN
    nPadT_DegradedVotingMode := 1;
    rVotedPadTemp_degC := rPadIRTemp_B_degC;
ELSIF bPadT_ChannelC_Valid THEN
    nPadT_DegradedVotingMode := 1;
    rVotedPadTemp_degC := rPadIRTemp_C_degC;
ELSE
    nPadT_DegradedVotingMode := 0;
    rVotedPadTemp_degC := 22.0;
END_IF;

(*
========================================================================================================================
  PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & LUENBERGER OBSERVER
  x[k+1] = A * x[k] + B * u[k] + E * d[k]
  y[k]   = C * x[k] + D * u[k]
========================================================================================================================
*)
(* 1. Assemble Filtered Measurement Vector y_meas (8x1) *)
y_meas[1] := rPlatenSpeed_PV_rpm;
y_meas[2] := rCarrierSpeed_PV_rpm;
y_meas[3] := (rVotedZone1Press_psi + rZonePress_PV_02_psi + rZonePress_PV_03_psi + rZonePress_PV_04_psi + rZonePress_PV_05_psi) * 0.20;
y_meas[4] := rVotedFilmThickness_Angstrom;
y_meas[5] := rVotedPadTemp_degC;
y_meas[6] := rVotedPlatenTorque_Nm;
y_meas[7] := rSlurryFlow_PV_mLpm;
y_meas[8] := rCondAcousticRMS_Filtered_mV * 0.411;  (* Pad cut rate correlation from acoustic emission *)

(* 2. Assemble External Disturbance Vector d_dist (4x1) *)
d_dist[1] := 0.0;                                       (* Nominal incoming batch thickness offset *)
d_dist[2] := rSlurryTemp_PV_degC - 20.0;                (* Slurry supply temperature deviation *)
d_dist[3] := rSlurryPH_PV_pH - 3.0;                     (* Acidic slurry pH deviation *)
d_dist[4] := rPadGlazeIndex;                            (* Real-time pad glazing factor *)

(* 3. Compute State Model Propagation: x_next = A * x_state + B * u_ctrl + E * d_dist *)
FOR i_idx := 1 TO 8 DO
    rTempSum := 0.0;
    (* State transition coupling: A * x *)
    FOR j_idx := 1 TO 8 DO
        rTempSum := rTempSum + a_mat[i_idx, j_idx] * x_state[j_idx];
    END_FOR;
    (* Manipulated actuator coupling: B * u *)
    FOR j_idx := 1 TO 8 DO
        rTempSum := rTempSum + b_mat[i_idx, j_idx] * u_ctrl[j_idx];
    END_FOR;
    (* Disturbance coupling: E * d *)
    FOR k_idx := 1 TO 4 DO
        rTempSum := rTempSum + e_mat[i_idx, k_idx] * d_dist[k_idx];
    END_FOR;
    x_next[i_idx] := rTempSum;
END_FOR;

(* 4. Compute Predicted Outputs: y_pred = C * x_state *)
FOR i_idx := 1 TO 8 DO
    rTempSum := 0.0;
    FOR j_idx := 1 TO 8 DO
        rTempSum := rTempSum + c_mat[i_idx, j_idx] * x_state[j_idx];
    END_FOR;
    y_pred[i_idx] := rTempSum;
END_FOR;

(* 5. Apply Luenberger Observer Innovation: x_state = x_next + L * (y_meas - y_pred) *)
FOR i_idx := 1 TO 8 DO
    x_state[i_idx] := x_next[i_idx] + l_observer_gain[i_idx] * (y_meas[i_idx] - y_pred[i_idx]);
END_FOR;

(* State Physical Boundary Clamping *)
x_state[1] := MAX(0.0, MIN(180.0, x_state[1]));             (* Platen speed limit [rpm] *)
x_state[2] := MAX(0.0, MIN(180.0, x_state[2]));             (* Carrier speed limit [rpm] *)
x_state[3] := MAX(0.0, MIN(8.5, x_state[3]));               (* Membrane pressure limit [psi] *)
x_state[4] := MAX(0.0, MIN(25000.0, x_state[4]));           (* Film thickness limit [Angstrom] *)
x_state[5] := MAX(15.0, MIN(85.0, x_state[5]));             (* Pad surface temp limit [deg C] *)
x_state[6] := MAX(0.0, MIN(250.0, x_state[6]));             (* Platen torque limit [Nm] *)
x_state[7] := MAX(0.0, MIN(500.0, x_state[7]));             (* Slurry flow limit [mL/min] *)
x_state[8] := MAX(0.0, MIN(45.0, x_state[8]));              (* Conditioner cut rate [um/h] *)

(* 6. Cyber-Physical Prestonian Instantaneous Material Removal Rate (MRR) Integration *)
(* Relative linear velocity calculation at carrier midpoint *)
(* omega_p = Platen rad/s, omega_c = Carrier rad/s *)
rTempVelRel := SQRT( (x_state[1] * 0.1047198 * rPlatenTrackRadius_m) * (x_state[1] * 0.1047198 * rPlatenTrackRadius_m)
                   + (x_state[2] * 0.1047198 * rRadialPos_Zone3_m) * (x_state[2] * 0.1047198 * rRadialPos_Zone3_m) );
(* Preston's Law: MRR = K_p * P * V_rel *)
(* P [Pa] = psi * 6894.76, MRR [Angstrom/min] = MRR [m/s] * 1.0E10 * 60 *)
rTempPressAvg := x_state[3] * 6894.76;
rComputedMRR_AngstromPerMin := rPrestonCoeff_Kp * rTempPressAvg * rTempVelRel * 6.0E11;

(* Low-pass filter for copper film thickness and rate of change d(Thick)/dt *)
rFilteredThickness_Angstrom := rFilteredThickness_Angstrom * 0.92 + x_state[4] * 0.08;
rThicknessRateOfChange_Aps := (rPrevThickness_Angstrom - rFilteredThickness_Angstrom) / T_CYCLE_SEC;
rPrevThickness_Angstrom := rFilteredThickness_Angstrom;

(* Low-pass filter for optical reflectance and slope d(Refl)/dt *)
rFilteredOpticalReflectance := rFilteredOpticalReflectance * 0.90 + rVotedOpticalReflectance_pct * 0.10;
rOpticalSlope_pctps := (rFilteredOpticalReflectance - rPrevOpticalReflectance) / T_CYCLE_SEC;
rPrevOpticalReflectance := rFilteredOpticalReflectance;

(* Estimated seconds to target endpoint based on current MRR *)
IF rComputedMRR_AngstromPerMin > 100.0 THEN
    rEstimatedRemainingTime_s := MAX(0.0, (x_state[4] - rEpdFinalTargetThickness_Angstrom) / (rComputedMRR_AngstromPerMin / 60.0));
ELSE
    rEstimatedRemainingTime_s := 999.0;
END_IF;

(* Compute Within-Wafer Non-Uniformity (WIWNU) 1-Sigma [%] across 5 zones *)
rTempSum := (rZonePress_PV_01_psi + rZonePress_PV_02_psi + rZonePress_PV_03_psi + rZonePress_PV_04_psi + rZonePress_PV_05_psi) * 0.20;
IF rTempSum > 0.5 THEN
    rWIWNU_OneSigma_pct := (SQRT( ( (rZonePress_PV_01_psi - rTempSum)*(rZonePress_PV_01_psi - rTempSum)
                                   + (rZonePress_PV_02_psi - rTempSum)*(rZonePress_PV_02_psi - rTempSum)
                                   + (rZonePress_PV_03_psi - rTempSum)*(rZonePress_PV_03_psi - rTempSum)
                                   + (rZonePress_PV_04_psi - rTempSum)*(rZonePress_PV_04_psi - rTempSum)
                                   + (rZonePress_PV_05_psi - rTempSum)*(rZonePress_PV_05_psi - rTempSum) ) * 0.20 ) / rTempSum) * 100.0;
ELSE
    rWIWNU_OneSigma_pct := 0.0;
END_IF;
"""
