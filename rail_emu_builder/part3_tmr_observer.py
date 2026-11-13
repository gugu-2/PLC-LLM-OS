# rail_emu_builder/part3_tmr_observer.py

def get_part3():
    return '''(* ============================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) PRIMARY SENSOR VOTING WITH DISCREPANCY TIMERS   *)
(* SIL-4 Compliant Hardware Fault Tolerant Median Selection & Degraded Degradation States         *)
(* ============================================================================================== *)

(* ---------------------------------------------------------------------------------------------- *)
(* Channel 1: Train Longitudinal True Ground Velocity (Radar vs Wheel Tachos)                     *)
(* ---------------------------------------------------------------------------------------------- *)
rSpeed_Delta_AB := ABS(rDopplerRadarSpeed_kmh - rWheelTachoSpeed_W1_kmh);
rSpeed_Delta_BC := ABS(rWheelTachoSpeed_W1_kmh - rWheelTachoSpeed_W2_kmh);
rSpeed_Delta_CA := ABS(rWheelTachoSpeed_W2_kmh - rDopplerRadarSpeed_kmh);

IF (rSpeed_Delta_AB > rSpeed_DiscrepancyLimit_kmh) OR (rSpeed_Delta_CA > rSpeed_DiscrepancyLimit_kmh) THEN
    rSpeed_DiscrepancyTimer_s := rSpeed_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rSpeed_DiscrepancyTimer_s > 0.350 THEN
        IF (rSpeed_Delta_AB > rSpeed_DiscrepancyLimit_kmh) AND (rSpeed_Delta_CA > rSpeed_DiscrepancyLimit_kmh) THEN
            bSpeed_ChannelA_Valid := FALSE; (* Doppler Radar Outlier Discrepancy *)
        ELSIF (rSpeed_Delta_AB > rSpeed_DiscrepancyLimit_kmh) AND (rSpeed_Delta_BC > rSpeed_DiscrepancyLimit_kmh) THEN
            bSpeed_ChannelB_Valid := FALSE; (* Wheel Tacho 1 Outlier Discrepancy *)
        ELSIF (rSpeed_Delta_CA > rSpeed_DiscrepancyLimit_kmh) AND (rSpeed_Delta_BC > rSpeed_DiscrepancyLimit_kmh) THEN
            bSpeed_ChannelC_Valid := FALSE; (* Wheel Tacho 2 Outlier Discrepancy *)
        END_IF;
    END_IF;
ELSE
    rSpeed_DiscrepancyTimer_s := MAX(0.0, rSpeed_DiscrepancyTimer_s - (T_CYCLE_SEC * 0.5));
END_IF;

IF bSpeed_ChannelA_Valid AND bSpeed_ChannelB_Valid AND bSpeed_ChannelC_Valid THEN
    nSpeed_DegradedVotingMode := 3;
    (* 2oo3 Median Voting *)
    IF (rDopplerRadarSpeed_kmh >= rWheelTachoSpeed_W1_kmh AND rDopplerRadarSpeed_kmh <= rWheelTachoSpeed_W2_kmh) OR
       (rDopplerRadarSpeed_kmh <= rWheelTachoSpeed_W1_kmh AND rDopplerRadarSpeed_kmh >= rWheelTachoSpeed_W2_kmh) THEN
        rVotedTrainSpeed_kmh := rDopplerRadarSpeed_kmh;
    ELSIF (rWheelTachoSpeed_W1_kmh >= rDopplerRadarSpeed_kmh AND rWheelTachoSpeed_W1_kmh <= rWheelTachoSpeed_W2_kmh) OR
          (rWheelTachoSpeed_W1_kmh <= rDopplerRadarSpeed_kmh AND rWheelTachoSpeed_W1_kmh >= rWheelTachoSpeed_W2_kmh) THEN
        rVotedTrainSpeed_kmh := rWheelTachoSpeed_W1_kmh;
    ELSE
        rVotedTrainSpeed_kmh := rWheelTachoSpeed_W2_kmh;
    END_IF;
ELSIF bSpeed_ChannelA_Valid AND bSpeed_ChannelB_Valid THEN
    nSpeed_DegradedVotingMode := 2;
    rVotedTrainSpeed_kmh := (rDopplerRadarSpeed_kmh + rWheelTachoSpeed_W1_kmh) * 0.5;
ELSIF bSpeed_ChannelB_Valid AND bSpeed_ChannelC_Valid THEN
    nSpeed_DegradedVotingMode := 2;
    rVotedTrainSpeed_kmh := (rWheelTachoSpeed_W1_kmh + rWheelTachoSpeed_W2_kmh) * 0.5;
ELSIF bSpeed_ChannelA_Valid AND bSpeed_ChannelC_Valid THEN
    nSpeed_DegradedVotingMode := 2;
    rVotedTrainSpeed_kmh := (rDopplerRadarSpeed_kmh + rWheelTachoSpeed_W2_kmh) * 0.5;
ELSIF bSpeed_ChannelA_Valid THEN
    nSpeed_DegradedVotingMode := 1;
    rVotedTrainSpeed_kmh := rDopplerRadarSpeed_kmh;
ELSIF bSpeed_ChannelB_Valid THEN
    nSpeed_DegradedVotingMode := 1;
    rVotedTrainSpeed_kmh := rWheelTachoSpeed_W1_kmh;
ELSIF bSpeed_ChannelC_Valid THEN
    nSpeed_DegradedVotingMode := 1;
    rVotedTrainSpeed_kmh := rWheelTachoSpeed_W2_kmh;
ELSE
    nSpeed_DegradedVotingMode := 0;
    rVotedTrainSpeed_kmh := 0.0; (* SIL-4 Fail-Safe Fallback *)
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* Channel 2: Bogie Leading Axle 1 Speed Sensors Triplet [rpm]                                    *)
(* ---------------------------------------------------------------------------------------------- *)
rAxle1_Delta_AB := ABS(rAxleSpeed_A1_ChA_rpm - rAxleSpeed_A1_ChB_rpm);
rAxle1_Delta_BC := ABS(rAxleSpeed_A1_ChB_rpm - rAxleSpeed_A1_ChC_rpm);
rAxle1_Delta_CA := ABS(rAxleSpeed_A1_ChC_rpm - rAxleSpeed_A1_ChA_rpm);

IF (rAxle1_Delta_AB > rAxle1_DiscrepancyLimit_rpm) OR (rAxle1_Delta_CA > rAxle1_DiscrepancyLimit_rpm) THEN
    rAxle1_DiscrepancyTimer_s := rAxle1_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rAxle1_DiscrepancyTimer_s > 0.250 THEN
        IF (rAxle1_Delta_AB > rAxle1_DiscrepancyLimit_rpm) AND (rAxle1_Delta_CA > rAxle1_DiscrepancyLimit_rpm) THEN
            bAxle1_ChannelA_Valid := FALSE;
        ELSIF (rAxle1_Delta_AB > rAxle1_DiscrepancyLimit_rpm) AND (rAxle1_Delta_BC > rAxle1_DiscrepancyLimit_rpm) THEN
            bAxle1_ChannelB_Valid := FALSE;
        ELSIF (rAxle1_Delta_CA > rAxle1_DiscrepancyLimit_rpm) AND (rAxle1_Delta_BC > rAxle1_DiscrepancyLimit_rpm) THEN
            bAxle1_ChannelC_Valid := FALSE;
        END_IF;
    END_IF;
ELSE
    rAxle1_DiscrepancyTimer_s := MAX(0.0, rAxle1_DiscrepancyTimer_s - (T_CYCLE_SEC * 0.5));
END_IF;

IF bAxle1_ChannelA_Valid AND bAxle1_ChannelB_Valid AND bAxle1_ChannelC_Valid THEN
    nAxle1_DegradedVotingMode := 3;
    IF (rAxleSpeed_A1_ChA_rpm >= rAxleSpeed_A1_ChB_rpm AND rAxleSpeed_A1_ChA_rpm <= rAxleSpeed_A1_ChC_rpm) OR
       (rAxleSpeed_A1_ChA_rpm <= rAxleSpeed_A1_ChB_rpm AND rAxleSpeed_A1_ChA_rpm >= rAxleSpeed_A1_ChC_rpm) THEN
        rVotedAxleSpeed_A1_rpm := rAxleSpeed_A1_ChA_rpm;
    ELSIF (rAxleSpeed_A1_ChB_rpm >= rAxleSpeed_A1_ChA_rpm AND rAxleSpeed_A1_ChB_rpm <= rAxleSpeed_A1_ChC_rpm) OR
          (rAxleSpeed_A1_ChB_rpm <= rAxleSpeed_A1_ChA_rpm AND rAxleSpeed_A1_ChB_rpm >= rAxleSpeed_A1_ChC_rpm) THEN
        rVotedAxleSpeed_A1_rpm := rAxleSpeed_A1_ChB_rpm;
    ELSE
        rVotedAxleSpeed_A1_rpm := rAxleSpeed_A1_ChC_rpm;
    END_IF;
ELSIF bAxle1_ChannelA_Valid AND bAxle1_ChannelB_Valid THEN
    nAxle1_DegradedVotingMode := 2;
    rVotedAxleSpeed_A1_rpm := (rAxleSpeed_A1_ChA_rpm + rAxleSpeed_A1_ChB_rpm) * 0.5;
ELSIF bAxle1_ChannelB_Valid AND bAxle1_ChannelC_Valid THEN
    nAxle1_DegradedVotingMode := 2;
    rVotedAxleSpeed_A1_rpm := (rAxleSpeed_A1_ChB_rpm + rAxleSpeed_A1_ChC_rpm) * 0.5;
ELSIF bAxle1_ChannelA_Valid AND bAxle1_ChannelC_Valid THEN
    nAxle1_DegradedVotingMode := 2;
    rVotedAxleSpeed_A1_rpm := (rAxleSpeed_A1_ChA_rpm + rAxleSpeed_A1_ChC_rpm) * 0.5;
ELSIF bAxle1_ChannelA_Valid THEN
    nAxle1_DegradedVotingMode := 1;
    rVotedAxleSpeed_A1_rpm := rAxleSpeed_A1_ChA_rpm;
ELSIF bAxle1_ChannelB_Valid THEN
    nAxle1_DegradedVotingMode := 1;
    rVotedAxleSpeed_A1_rpm := rAxleSpeed_A1_ChB_rpm;
ELSIF bAxle1_ChannelC_Valid THEN
    nAxle1_DegradedVotingMode := 1;
    rVotedAxleSpeed_A1_rpm := rAxleSpeed_A1_ChC_rpm;
ELSE
    nAxle1_DegradedVotingMode := 0;
    rVotedAxleSpeed_A1_rpm := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* Channel 3: Bogie Trailing Axle 2 Speed Sensors Triplet [rpm]                                   *)
(* ---------------------------------------------------------------------------------------------- *)
rAxle2_Delta_AB := ABS(rAxleSpeed_A2_ChA_rpm - rAxleSpeed_A2_ChB_rpm);
rAxle2_Delta_BC := ABS(rAxleSpeed_A2_ChB_rpm - rAxleSpeed_A2_ChC_rpm);
rAxle2_Delta_CA := ABS(rAxleSpeed_A2_ChC_rpm - rAxleSpeed_A2_ChA_rpm);

IF (rAxle2_Delta_AB > rAxle2_DiscrepancyLimit_rpm) OR (rAxle2_Delta_CA > rAxle2_DiscrepancyLimit_rpm) THEN
    rAxle2_DiscrepancyTimer_s := rAxle2_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rAxle2_DiscrepancyTimer_s > 0.250 THEN
        IF (rAxle2_Delta_AB > rAxle2_DiscrepancyLimit_rpm) AND (rAxle2_Delta_CA > rAxle2_DiscrepancyLimit_rpm) THEN
            bAxle2_ChannelA_Valid := FALSE;
        ELSIF (rAxle2_Delta_AB > rAxle2_DiscrepancyLimit_rpm) AND (rAxle2_Delta_BC > rAxle2_DiscrepancyLimit_rpm) THEN
            bAxle2_ChannelB_Valid := FALSE;
        ELSIF (rAxle2_Delta_CA > rAxle2_DiscrepancyLimit_rpm) AND (rAxle2_Delta_BC > rAxle2_DiscrepancyLimit_rpm) THEN
            bAxle2_ChannelC_Valid := FALSE;
        END_IF;
    END_IF;
ELSE
    rAxle2_DiscrepancyTimer_s := MAX(0.0, rAxle2_DiscrepancyTimer_s - (T_CYCLE_SEC * 0.5));
END_IF;

IF bAxle2_ChannelA_Valid AND bAxle2_ChannelB_Valid AND bAxle2_ChannelC_Valid THEN
    nAxle2_DegradedVotingMode := 3;
    IF (rAxleSpeed_A2_ChA_rpm >= rAxleSpeed_A2_ChB_rpm AND rAxleSpeed_A2_ChA_rpm <= rAxleSpeed_A2_ChC_rpm) OR
       (rAxleSpeed_A2_ChA_rpm <= rAxleSpeed_A2_ChB_rpm AND rAxleSpeed_A2_ChA_rpm >= rAxleSpeed_A2_ChC_rpm) THEN
        rVotedAxleSpeed_A2_rpm := rAxleSpeed_A2_ChA_rpm;
    ELSIF (rAxleSpeed_A2_ChB_rpm >= rAxleSpeed_A2_ChA_rpm AND rAxleSpeed_A2_ChB_rpm <= rAxleSpeed_A2_ChC_rpm) OR
          (rAxleSpeed_A2_ChB_rpm <= rAxleSpeed_A2_ChA_rpm AND rAxleSpeed_A2_ChB_rpm >= rAxleSpeed_A2_ChC_rpm) THEN
        rVotedAxleSpeed_A2_rpm := rAxleSpeed_A2_ChB_rpm;
    ELSE
        rVotedAxleSpeed_A2_rpm := rAxleSpeed_A2_ChC_rpm;
    END_IF;
ELSIF bAxle2_ChannelA_Valid AND bAxle2_ChannelB_Valid THEN
    nAxle2_DegradedVotingMode := 2;
    rVotedAxleSpeed_A2_rpm := (rAxleSpeed_A2_ChA_rpm + rAxleSpeed_A2_ChB_rpm) * 0.5;
ELSIF bAxle2_ChannelB_Valid AND bAxle2_ChannelC_Valid THEN
    nAxle2_DegradedVotingMode := 2;
    rVotedAxleSpeed_A2_rpm := (rAxleSpeed_A2_ChB_rpm + rAxleSpeed_A2_ChC_rpm) * 0.5;
ELSIF bAxle2_ChannelA_Valid AND bAxle2_ChannelC_Valid THEN
    nAxle2_DegradedVotingMode := 2;
    rVotedAxleSpeed_A2_rpm := (rAxleSpeed_A2_ChA_rpm + rAxleSpeed_A2_ChC_rpm) * 0.5;
ELSIF bAxle2_ChannelA_Valid THEN
    nAxle2_DegradedVotingMode := 1;
    rVotedAxleSpeed_A2_rpm := rAxleSpeed_A2_ChA_rpm;
ELSIF bAxle2_ChannelB_Valid THEN
    nAxle2_DegradedVotingMode := 1;
    rVotedAxleSpeed_A2_rpm := rAxleSpeed_A2_ChB_rpm;
ELSIF bAxle2_ChannelC_Valid THEN
    nAxle2_DegradedVotingMode := 1;
    rVotedAxleSpeed_A2_rpm := rAxleSpeed_A2_ChC_rpm;
ELSE
    nAxle2_DegradedVotingMode := 0;
    rVotedAxleSpeed_A2_rpm := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* Channel 4: Pantograph Catenary Dynamic Contact Force Load Cells [N]                            *)
(* ---------------------------------------------------------------------------------------------- *)
rPanto_Delta_AB := ABS(rPantoContactForce_ChA_N - rPantoContactForce_ChB_N);
rPanto_Delta_BC := ABS(rPantoContactForce_ChB_N - rPantoContactForce_ChC_N);
rPanto_Delta_CA := ABS(rPantoContactForce_ChC_N - rPantoContactForce_ChA_N);

IF (rPanto_Delta_AB > rPanto_DiscrepancyLimit_N) OR (rPanto_Delta_CA > rPanto_DiscrepancyLimit_N) THEN
    rPanto_DiscrepancyTimer_s := rPanto_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rPanto_DiscrepancyTimer_s > 0.200 THEN
        IF (rPanto_Delta_AB > rPanto_DiscrepancyLimit_N) AND (rPanto_Delta_CA > rPanto_DiscrepancyLimit_N) THEN
            bPanto_ChannelA_Valid := FALSE;
        ELSIF (rPanto_Delta_AB > rPanto_DiscrepancyLimit_N) AND (rPanto_Delta_BC > rPanto_DiscrepancyLimit_N) THEN
            bPanto_ChannelB_Valid := FALSE;
        ELSIF (rPanto_Delta_CA > rPanto_DiscrepancyLimit_N) AND (rPanto_Delta_BC > rPanto_DiscrepancyLimit_N) THEN
            bPanto_ChannelC_Valid := FALSE;
        END_IF;
    END_IF;
ELSE
    rPanto_DiscrepancyTimer_s := MAX(0.0, rPanto_DiscrepancyTimer_s - (T_CYCLE_SEC * 0.5));
END_IF;

IF bPanto_ChannelA_Valid AND bPanto_ChannelB_Valid AND bPanto_ChannelC_Valid THEN
    nPanto_DegradedVotingMode := 3;
    IF (rPantoContactForce_ChA_N >= rPantoContactForce_ChB_N AND rPantoContactForce_ChA_N <= rPantoContactForce_ChC_N) OR
       (rPantoContactForce_ChA_N <= rPantoContactForce_ChB_N AND rPantoContactForce_ChA_N >= rPantoContactForce_ChC_N) THEN
        rVotedPantoForce_N := rPantoContactForce_ChA_N;
    ELSIF (rPantoContactForce_ChB_N >= rPantoContactForce_ChA_N AND rPantoContactForce_ChB_N <= rPantoContactForce_ChC_N) OR
          (rPantoContactForce_ChB_N <= rPantoContactForce_ChA_N AND rPantoContactForce_ChB_N >= rPantoContactForce_ChC_N) THEN
        rVotedPantoForce_N := rPantoContactForce_ChB_N;
    ELSE
        rVotedPantoForce_N := rPantoContactForce_ChC_N;
    END_IF;
ELSIF bPanto_ChannelA_Valid AND bPanto_ChannelB_Valid THEN
    nPanto_DegradedVotingMode := 2;
    rVotedPantoForce_N := (rPantoContactForce_ChA_N + rPantoContactForce_ChB_N) * 0.5;
ELSIF bPanto_ChannelB_Valid AND bPanto_ChannelC_Valid THEN
    nPanto_DegradedVotingMode := 2;
    rVotedPantoForce_N := (rPantoContactForce_ChB_N + rPantoContactForce_ChC_N) * 0.5;
ELSIF bPanto_ChannelA_Valid AND bPanto_ChannelC_Valid THEN
    nPanto_DegradedVotingMode := 2;
    rVotedPantoForce_N := (rPantoContactForce_ChA_N + rPantoContactForce_ChC_N) * 0.5;
ELSIF bPanto_ChannelA_Valid THEN
    nPanto_DegradedVotingMode := 1;
    rVotedPantoForce_N := rPantoContactForce_ChA_N;
ELSIF bPanto_ChannelB_Valid THEN
    nPanto_DegradedVotingMode := 1;
    rVotedPantoForce_N := rPantoContactForce_ChB_N;
ELSIF bPanto_ChannelC_Valid THEN
    nPanto_DegradedVotingMode := 1;
    rVotedPantoForce_N := rPantoContactForce_ChC_N;
ELSE
    nPanto_DegradedVotingMode := 0;
    rVotedPantoForce_N := 145.0; (* Fallback nominal contact force *)
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* Channel 5: DC Link Intermediate Bus Differential Voltage Probes [V]                            *)
(* ---------------------------------------------------------------------------------------------- *)
rDCLink_Delta_AB := ABS(rDCLinkVoltage_ChA_V - rDCLinkVoltage_ChB_V);
rDCLink_Delta_BC := ABS(rDCLinkVoltage_ChB_V - rDCLinkVoltage_ChC_V);
rDCLink_Delta_CA := ABS(rDCLinkVoltage_ChC_V - rDCLinkVoltage_ChA_V);

IF (rDCLink_Delta_AB > rDCLink_DiscrepancyLimit_V) OR (rDCLink_Delta_CA > rDCLink_DiscrepancyLimit_V) THEN
    rDCLink_DiscrepancyTimer_s := rDCLink_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rDCLink_DiscrepancyTimer_s > 0.150 THEN
        IF (rDCLink_Delta_AB > rDCLink_DiscrepancyLimit_V) AND (rDCLink_Delta_CA > rDCLink_DiscrepancyLimit_V) THEN
            bDCLink_ChannelA_Valid := FALSE;
        ELSIF (rDCLink_Delta_AB > rDCLink_DiscrepancyLimit_V) AND (rDCLink_Delta_BC > rDCLink_DiscrepancyLimit_V) THEN
            bDCLink_ChannelB_Valid := FALSE;
        ELSIF (rDCLink_Delta_CA > rDCLink_DiscrepancyLimit_V) AND (rDCLink_Delta_BC > rDCLink_DiscrepancyLimit_V) THEN
            bDCLink_ChannelC_Valid := FALSE;
        END_IF;
    END_IF;
ELSE
    rDCLink_DiscrepancyTimer_s := MAX(0.0, rDCLink_DiscrepancyTimer_s - (T_CYCLE_SEC * 0.5));
END_IF;

IF bDCLink_ChannelA_Valid AND bDCLink_ChannelB_Valid AND bDCLink_ChannelC_Valid THEN
    nDCLink_DegradedVotingMode := 3;
    IF (rDCLinkVoltage_ChA_V >= rDCLinkVoltage_ChB_V AND rDCLinkVoltage_ChA_V <= rDCLinkVoltage_ChC_V) OR
       (rDCLinkVoltage_ChA_V <= rDCLinkVoltage_ChB_V AND rDCLinkVoltage_ChA_V >= rDCLinkVoltage_ChC_V) THEN
        rVotedDCLinkVoltage_V := rDCLinkVoltage_ChA_V;
    ELSIF (rDCLinkVoltage_ChB_V >= rDCLinkVoltage_ChA_V AND rDCLinkVoltage_ChB_V <= rDCLinkVoltage_ChC_V) OR
          (rDCLinkVoltage_ChB_V <= rDCLinkVoltage_ChA_V AND rDCLinkVoltage_ChB_V >= rDCLinkVoltage_ChC_V) THEN
        rVotedDCLinkVoltage_V := rDCLinkVoltage_ChB_V;
    ELSE
        rVotedDCLinkVoltage_V := rDCLinkVoltage_ChC_V;
    END_IF;
ELSIF bDCLink_ChannelA_Valid AND bDCLink_ChannelB_Valid THEN
    nDCLink_DegradedVotingMode := 2;
    rVotedDCLinkVoltage_V := (rDCLinkVoltage_ChA_V + rDCLinkVoltage_ChB_V) * 0.5;
ELSIF bDCLink_ChannelB_Valid AND bDCLink_ChannelC_Valid THEN
    nDCLink_DegradedVotingMode := 2;
    rVotedDCLinkVoltage_V := (rDCLinkVoltage_ChB_V + rDCLinkVoltage_ChC_V) * 0.5;
ELSIF bDCLink_ChannelA_Valid AND bDCLink_ChannelC_Valid THEN
    nDCLink_DegradedVotingMode := 2;
    rVotedDCLinkVoltage_V := (rDCLinkVoltage_ChA_V + rDCLinkVoltage_ChC_V) * 0.5;
ELSIF bDCLink_ChannelA_Valid THEN
    nDCLink_DegradedVotingMode := 1;
    rVotedDCLinkVoltage_V := rDCLinkVoltage_ChA_V;
ELSIF bDCLink_ChannelB_Valid THEN
    nDCLink_DegradedVotingMode := 1;
    rVotedDCLinkVoltage_V := rDCLinkVoltage_ChB_V;
ELSIF bDCLink_ChannelC_Valid THEN
    nDCLink_DegradedVotingMode := 1;
    rVotedDCLinkVoltage_V := rDCLinkVoltage_ChC_V;
ELSE
    nDCLink_DegradedVotingMode := 0;
    rVotedDCLinkVoltage_V := 3000.0;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* Channel 6: Bogie Brake Cylinder Pneumatic Pressure Transducers [bar]                           *)
(* ---------------------------------------------------------------------------------------------- *)
rBrakeCyl_Delta_AB := ABS(rBrakeCylinderPressure_ChA_bar - rBrakeCylinderPressure_ChB_bar);
rBrakeCyl_Delta_BC := ABS(rBrakeCylinderPressure_ChB_bar - rBrakeCylinderPressure_ChC_bar);
rBrakeCyl_Delta_CA := ABS(rBrakeCylinderPressure_ChC_bar - rBrakeCylinderPressure_ChA_bar);

IF (rBrakeCyl_Delta_AB > rBrakeCyl_DiscrepancyLimit_bar) OR (rBrakeCyl_Delta_CA > rBrakeCyl_DiscrepancyLimit_bar) THEN
    rBrakeCyl_DiscrepancyTimer_s := rBrakeCyl_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rBrakeCyl_DiscrepancyTimer_s > 0.200 THEN
        IF (rBrakeCyl_Delta_AB > rBrakeCyl_DiscrepancyLimit_bar) AND (rBrakeCyl_Delta_CA > rBrakeCyl_DiscrepancyLimit_bar) THEN
            bBrakeCyl_ChannelA_Valid := FALSE;
        ELSIF (rBrakeCyl_Delta_AB > rBrakeCyl_DiscrepancyLimit_bar) AND (rBrakeCyl_Delta_BC > rBrakeCyl_DiscrepancyLimit_bar) THEN
            bBrakeCyl_ChannelB_Valid := FALSE;
        ELSIF (rBrakeCyl_Delta_CA > rBrakeCyl_DiscrepancyLimit_bar) AND (rBrakeCyl_Delta_BC > rBrakeCyl_DiscrepancyLimit_bar) THEN
            bBrakeCyl_ChannelC_Valid := FALSE;
        END_IF;
    END_IF;
ELSE
    rBrakeCyl_DiscrepancyTimer_s := MAX(0.0, rBrakeCyl_DiscrepancyTimer_s - (T_CYCLE_SEC * 0.5));
END_IF;

IF bBrakeCyl_ChannelA_Valid AND bBrakeCyl_ChannelB_Valid AND bBrakeCyl_ChannelC_Valid THEN
    nBrakeCyl_DegradedVotingMode := 3;
    IF (rBrakeCylinderPressure_ChA_bar >= rBrakeCylinderPressure_ChB_bar AND rBrakeCylinderPressure_ChA_bar <= rBrakeCylinderPressure_ChC_bar) OR
       (rBrakeCylinderPressure_ChA_bar <= rBrakeCylinderPressure_ChB_bar AND rBrakeCylinderPressure_ChA_bar >= rBrakeCylinderPressure_ChC_bar) THEN
        rVotedBrakeCylPressure_bar := rBrakeCylinderPressure_ChA_bar;
    ELSIF (rBrakeCylinderPressure_ChB_bar >= rBrakeCylinderPressure_ChA_bar AND rBrakeCylinderPressure_ChB_bar <= rBrakeCylinderPressure_ChC_bar) OR
          (rBrakeCylinderPressure_ChB_bar <= rBrakeCylinderPressure_ChA_bar AND rBrakeCylinderPressure_ChB_bar >= rBrakeCylinderPressure_ChC_bar) THEN
        rVotedBrakeCylPressure_bar := rBrakeCylinderPressure_ChB_bar;
    ELSE
        rVotedBrakeCylPressure_bar := rBrakeCylinderPressure_ChC_bar;
    END_IF;
ELSIF bBrakeCyl_ChannelA_Valid AND bBrakeCyl_ChannelB_Valid THEN
    nBrakeCyl_DegradedVotingMode := 2;
    rVotedBrakeCylPressure_bar := (rBrakeCylinderPressure_ChA_bar + rBrakeCylinderPressure_ChB_bar) * 0.5;
ELSIF bBrakeCyl_ChannelB_Valid AND bBrakeCyl_ChannelC_Valid THEN
    nBrakeCyl_DegradedVotingMode := 2;
    rVotedBrakeCylPressure_bar := (rBrakeCylinderPressure_ChB_bar + rBrakeCylinderPressure_ChC_bar) * 0.5;
ELSIF bBrakeCyl_ChannelA_Valid AND bBrakeCyl_ChannelC_Valid THEN
    nBrakeCyl_DegradedVotingMode := 2;
    rVotedBrakeCylPressure_bar := (rBrakeCylinderPressure_ChA_bar + rBrakeCylinderPressure_ChC_bar) * 0.5;
ELSIF bBrakeCyl_ChannelA_Valid THEN
    nBrakeCyl_DegradedVotingMode := 1;
    rVotedBrakeCylPressure_bar := rBrakeCylinderPressure_ChA_bar;
ELSIF bBrakeCyl_ChannelB_Valid THEN
    nBrakeCyl_DegradedVotingMode := 1;
    rVotedBrakeCylPressure_bar := rBrakeCylinderPressure_ChB_bar;
ELSIF bBrakeCyl_ChannelC_Valid THEN
    nBrakeCyl_DegradedVotingMode := 1;
    rVotedBrakeCylPressure_bar := rBrakeCylinderPressure_ChC_bar;
ELSE
    nBrakeCyl_DegradedVotingMode := 0;
    rVotedBrakeCylPressure_bar := 0.0;
END_IF;

(* ============================================================================================== *)
(* PHASE 2: CURTIUS-KNIFFLER NON-LINEAR RAIL-WHEEL ADHESION OBSERVER & MICRO-SLIP ESTIMATION      *)
(* UIC 541-05 & EN 15595 Compliant Tangential Friction & Dynamic Creep Surface Observer            *)
(* ============================================================================================== *)

(* 1. Velocity and Acceleration Transformations into SI Units *)
rTrainSpeed_ms := rVotedTrainSpeed_kmh / 3.6;
rAxle1_LinearVelocity_ms := (rVotedAxleSpeed_A1_rpm * 2.0 * 3.14159265 / 60.0) * WHEEL_RADIUS_NOM_M;
rAxle2_LinearVelocity_ms := (rVotedAxleSpeed_A2_rpm * 2.0 * 3.14159265 / 60.0) * WHEEL_RADIUS_NOM_M;

rTrainAcceleration_ms2 := (rVotedTrainSpeed_kmh - rPrevTrainSpeed_kmh) / (3.6 * T_CYCLE_SEC);
rPrevTrainSpeed_kmh := rVotedTrainSpeed_kmh;

rAxle1_AngularDecel_rads2 := -((rVotedAxleSpeed_A1_rpm - rPrevAxleSpeed_A1_rpm) * 2.0 * 3.14159265 / (60.0 * T_CYCLE_SEC));
rPrevAxleSpeed_A1_rpm := rVotedAxleSpeed_A1_rpm;
rAxle1_LinearDecel_ms2 := rAxle1_AngularDecel_rads2 * WHEEL_RADIUS_NOM_M;

rAxle2_AngularDecel_rads2 := -((rVotedAxleSpeed_A2_rpm - rPrevAxleSpeed_A2_rpm) * 2.0 * 3.14159265 / (60.0 * T_CYCLE_SEC));
rPrevAxleSpeed_A2_rpm := rVotedAxleSpeed_A2_rpm;
rAxle2_LinearDecel_ms2 := rAxle2_AngularDecel_rads2 * WHEEL_RADIUS_NOM_M;

(* 2. Slip/Skid Velocity & Non-Dimensional Slip Ratio Calculation *)
rAxle1_SlipVelocity_ms := rAxle1_LinearVelocity_ms - rTrainSpeed_ms;
rAxle2_SlipVelocity_ms := rAxle2_LinearVelocity_ms - rTrainSpeed_ms;

IF bBrakingEnableCmd OR (rDriverBrakeNotch_pct > 1.0) THEN
    (* Braking Skid Ratio: (v_train - v_wheel) / v_train *)
    IF rTrainSpeed_ms > 0.5 THEN
        rAxle1_SlipRatio := (rTrainSpeed_ms - rAxle1_LinearVelocity_ms) / rTrainSpeed_ms;
        rAxle2_SlipRatio := (rTrainSpeed_ms - rAxle2_LinearVelocity_ms) / rTrainSpeed_ms;
    ELSE
        rAxle1_SlipRatio := 0.0;
        rAxle2_SlipRatio := 0.0;
    END_IF;
ELSE
    (* Motoring Slip Ratio: (v_wheel - v_train) / max(v_wheel, v_train) *)
    IF rAxle1_LinearVelocity_ms > 0.5 THEN
        rAxle1_SlipRatio := rAxle1_SlipVelocity_ms / MAX(rAxle1_LinearVelocity_ms, rTrainSpeed_ms);
    ELSE
        rAxle1_SlipRatio := 0.0;
    END_IF;
    IF rAxle2_LinearVelocity_ms > 0.5 THEN
        rAxle2_SlipRatio := rAxle2_SlipVelocity_ms / MAX(rAxle2_LinearVelocity_ms, rTrainSpeed_ms);
    ELSE
        rAxle2_SlipRatio := 0.0;
    END_IF;
END_IF;

rEstimatedWheelSlip_A1_pct := rAxle1_SlipRatio * 100.0;
rEstimatedWheelSlip_A2_pct := rAxle2_SlipRatio * 100.0;

(* 3. Curtius-Kniffler Theoretical Adhesion Ceiling *)
rTheoreticalAdhesionLimit := (rCurtius_c1 / (rVotedTrainSpeed_kmh + rCurtius_c2)) + rCurtius_c3;
(* Account for track condition railhead contamination factor d_dist[4] (1.0=Dry, 0.0=Contaminated) *)
rTheoreticalAdhesionLimit := rTheoreticalAdhesionLimit * (0.35 + (0.65 * MAX(0.0, MIN(1.0, d_dist[4]))));

(* 4. Transmitted Tractive / Braking Force & Instantaneous Friction Coefficient *)
IF rAxle1_DynamicLoad_kN > 10.0 THEN
    rScratchAccum := (ABS(rTractionTorqueCommand_kNm) * GEAR_RATIO) / WHEEL_RADIUS_NOM_M;
    rObservedAdhesionRaw := rScratchAccum / rAxle1_DynamicLoad_kN;
    rObservedAdhesionRaw := MIN(rObservedAdhesionRaw, rTheoreticalAdhesionLimit * 1.25);
ELSE
    rObservedAdhesionRaw := 0.15;
END_IF;

(* Recursive Low-Pass Filter on Observed Adhesion *)
rObservedAdhesionCoeff := (1.0 - rAdhesionFilterCoeff) * rObservedAdhesionCoeff + (rAdhesionFilterCoeff * rObservedAdhesionRaw);

(* 5. Micro-Slip Numerical Gradient dMu / ds Evaluation *)
rScratchDiff := rAxle1_SlipRatio - rSlipRatio_Prev_A1;
IF ABS(rScratchDiff) > 0.0001 THEN
    rAdhesionGradient_dMu_ds_A1 := (rObservedAdhesionCoeff - rAdhesion_Prev_A1) / rScratchDiff;
ELSE
    rAdhesionGradient_dMu_ds_A1 := 0.0;
END_IF;
rSlipRatio_Prev_A1 := rAxle1_SlipRatio;
rAdhesion_Prev_A1 := rObservedAdhesionCoeff;
'''
