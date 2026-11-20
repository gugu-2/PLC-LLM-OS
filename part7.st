(* ==================================================================================================== *)
(* PHASE 5: ISA-18.2 MULTI-TIER PROCESS ALARM MANAGEMENT & 5x 32-BIT FIELDBUS TELEMETRY PACKING          *)
(* ==================================================================================================== *)
(* STANDARDS COMPLIANCE & SAFETY PHILOSOPHY:                                                            *)
(*   1. ANSI/ISA-18.2-2016 Management of Alarm Systems for the Process Industries.                        *)
(*   2. DIN EN 693 / EN ISO 16092-3 Hydraulic Press Operational Safety Integration.                      *)
(*   3. ISO 13849-1 Category 4 / PL e Dual-Channel Machine Safety Architecture.                          *)
(*   4. Fieldbus Telemetry Words formatted for deterministic OPC UA and PROFINET IO cyclic interchange.  *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* ISA-18.2 ALARM LOOP 1: MAIN RAM AXIAL FORGING TONNAGE [kN]                                                                    *)
(* ---------------------------------------------------------------------------------------------------- *)
(* High-High Critical Trip Evaluation *)
IF r_TMR_VotedTonnage_kN >= r_Alm1_Trip_HH_kN THEN
    r_Alm1_Timer_HH_ms := r_Alm1_Timer_HH_ms + r_CycleScanPeriod_ms;
    IF r_Alm1_Timer_HH_ms >= 20.0 THEN
        b_Alm1_Active_HH := TRUE;
    END_IF;
ELSE
    IF r_TMR_VotedTonnage_kN < (r_Alm1_Trip_HH_kN - r_Alm1_Deadband_kN) THEN
        r_Alm1_Timer_HH_ms := 0.0;
        b_Alm1_Active_HH := FALSE;
        b_Alm1_Ack_HH := FALSE;
    END_IF;
END_IF;

(* High Warning Trip Evaluation *)
IF (r_TMR_VotedTonnage_kN >= r_Alm1_Trip_H_kN) AND (r_TMR_VotedTonnage_kN < (r_Alm1_Trip_HH_kN - r_Alm1_Deadband_kN)) THEN
    r_Alm1_Timer_H_ms := r_Alm1_Timer_H_ms + r_CycleScanPeriod_ms;
    IF r_Alm1_Timer_H_ms >= 50.0 THEN
        b_Alm1_Active_H := TRUE;
    END_IF;
ELSE
    IF r_TMR_VotedTonnage_kN < (r_Alm1_Trip_H_kN - r_Alm1_Deadband_kN) THEN
        r_Alm1_Timer_H_ms := 0.0;
        b_Alm1_Active_H := FALSE;
        b_Alm1_Ack_H := FALSE;
    END_IF;
END_IF;

(* Low Warning Trip Evaluation *)
IF (r_TMR_VotedTonnage_kN <= r_Alm1_Trip_L_kN) AND (r_TMR_VotedTonnage_kN > (r_Alm1_Trip_LL_kN + r_Alm1_Deadband_kN)) THEN
    r_Alm1_Timer_L_ms := r_Alm1_Timer_L_ms + r_CycleScanPeriod_ms;
    IF r_Alm1_Timer_L_ms >= 50.0 THEN
        b_Alm1_Active_L := TRUE;
    END_IF;
ELSE
    IF r_TMR_VotedTonnage_kN > (r_Alm1_Trip_L_kN + r_Alm1_Deadband_kN) THEN
        r_Alm1_Timer_L_ms := 0.0;
        b_Alm1_Active_L := FALSE;
        b_Alm1_Ack_L := FALSE;
    END_IF;
END_IF;

(* Low-Low Critical Trip Evaluation *)
IF r_TMR_VotedTonnage_kN <= r_Alm1_Trip_LL_kN THEN
    r_Alm1_Timer_LL_ms := r_Alm1_Timer_LL_ms + r_CycleScanPeriod_ms;
    IF r_Alm1_Timer_LL_ms >= 20.0 THEN
        b_Alm1_Active_LL := TRUE;
    END_IF;
ELSE
    IF r_TMR_VotedTonnage_kN > (r_Alm1_Trip_LL_kN + r_Alm1_Deadband_kN) THEN
        r_Alm1_Timer_LL_ms := 0.0;
        b_Alm1_Active_LL := FALSE;
        b_Alm1_Ack_LL := FALSE;
    END_IF;
END_IF;

(* Manual Operator Acknowledgment Strobe Processing *)
IF b_AcknowledgeAlarms_Strobe THEN
    IF b_Alm1_Active_HH THEN b_Alm1_Ack_HH := TRUE; END_IF;
    IF b_Alm1_Active_H THEN b_Alm1_Ack_H := TRUE; END_IF;
    IF b_Alm1_Active_L THEN b_Alm1_Ack_L := TRUE; END_IF;
    IF b_Alm1_Active_LL THEN b_Alm1_Ack_LL := TRUE; END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* ISA-18.2 ALARM LOOP 2: HYDRAULIC MAIN HEADER PRESSURE [bar]                                                                    *)
(* ---------------------------------------------------------------------------------------------------- *)
(* High-High Critical Trip Evaluation *)
IF r_TMR_VotedHydPressure_bar >= r_Alm2_Trip_HH_bar THEN
    r_Alm2_Timer_HH_ms := r_Alm2_Timer_HH_ms + r_CycleScanPeriod_ms;
    IF r_Alm2_Timer_HH_ms >= 20.0 THEN
        b_Alm2_Active_HH := TRUE;
    END_IF;
ELSE
    IF r_TMR_VotedHydPressure_bar < (r_Alm2_Trip_HH_bar - r_Alm2_Deadband_bar) THEN
        r_Alm2_Timer_HH_ms := 0.0;
        b_Alm2_Active_HH := FALSE;
        b_Alm2_Ack_HH := FALSE;
    END_IF;
END_IF;

(* High Warning Trip Evaluation *)
IF (r_TMR_VotedHydPressure_bar >= r_Alm2_Trip_H_bar) AND (r_TMR_VotedHydPressure_bar < (r_Alm2_Trip_HH_bar - r_Alm2_Deadband_bar)) THEN
    r_Alm2_Timer_H_ms := r_Alm2_Timer_H_ms + r_CycleScanPeriod_ms;
    IF r_Alm2_Timer_H_ms >= 50.0 THEN
        b_Alm2_Active_H := TRUE;
    END_IF;
ELSE
    IF r_TMR_VotedHydPressure_bar < (r_Alm2_Trip_H_bar - r_Alm2_Deadband_bar) THEN
        r_Alm2_Timer_H_ms := 0.0;
        b_Alm2_Active_H := FALSE;
        b_Alm2_Ack_H := FALSE;
    END_IF;
END_IF;

(* Low Warning Trip Evaluation *)
IF (r_TMR_VotedHydPressure_bar <= r_Alm2_Trip_L_bar) AND (r_TMR_VotedHydPressure_bar > (r_Alm2_Trip_LL_bar + r_Alm2_Deadband_bar)) THEN
    r_Alm2_Timer_L_ms := r_Alm2_Timer_L_ms + r_CycleScanPeriod_ms;
    IF r_Alm2_Timer_L_ms >= 50.0 THEN
        b_Alm2_Active_L := TRUE;
    END_IF;
ELSE
    IF r_TMR_VotedHydPressure_bar > (r_Alm2_Trip_L_bar + r_Alm2_Deadband_bar) THEN
        r_Alm2_Timer_L_ms := 0.0;
        b_Alm2_Active_L := FALSE;
        b_Alm2_Ack_L := FALSE;
    END_IF;
END_IF;

(* Low-Low Critical Trip Evaluation *)
IF r_TMR_VotedHydPressure_bar <= r_Alm2_Trip_LL_bar THEN
    r_Alm2_Timer_LL_ms := r_Alm2_Timer_LL_ms + r_CycleScanPeriod_ms;
    IF r_Alm2_Timer_LL_ms >= 20.0 THEN
        b_Alm2_Active_LL := TRUE;
    END_IF;
ELSE
    IF r_TMR_VotedHydPressure_bar > (r_Alm2_Trip_LL_bar + r_Alm2_Deadband_bar) THEN
        r_Alm2_Timer_LL_ms := 0.0;
        b_Alm2_Active_LL := FALSE;
        b_Alm2_Ack_LL := FALSE;
    END_IF;
END_IF;

(* Manual Operator Acknowledgment Strobe Processing *)
IF b_AcknowledgeAlarms_Strobe THEN
    IF b_Alm2_Active_HH THEN b_Alm2_Ack_HH := TRUE; END_IF;
    IF b_Alm2_Active_H THEN b_Alm2_Ack_H := TRUE; END_IF;
    IF b_Alm2_Active_L THEN b_Alm2_Ack_L := TRUE; END_IF;
    IF b_Alm2_Active_LL THEN b_Alm2_Ack_LL := TRUE; END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* ISA-18.2 ALARM LOOP 3: UPPER DIE INDUCTION TEMPERATURE [deg C]                                                                    *)
(* ---------------------------------------------------------------------------------------------------- *)
(* High-High Critical Trip Evaluation *)
IF r_TMR_VotedDieTemp_DegC >= r_Alm3_Trip_HH_DegC THEN
    r_Alm3_Timer_HH_ms := r_Alm3_Timer_HH_ms + r_CycleScanPeriod_ms;
    IF r_Alm3_Timer_HH_ms >= 30.0 THEN
        b_Alm3_Active_HH := TRUE;
    END_IF;
ELSE
    IF r_TMR_VotedDieTemp_DegC < (r_Alm3_Trip_HH_DegC - r_Alm3_Deadband_DegC) THEN
        r_Alm3_Timer_HH_ms := 0.0;
        b_Alm3_Active_HH := FALSE;
        b_Alm3_Ack_HH := FALSE;
    END_IF;
END_IF;

(* High Warning Trip Evaluation *)
IF (r_TMR_VotedDieTemp_DegC >= r_Alm3_Trip_H_DegC) AND (r_TMR_VotedDieTemp_DegC < (r_Alm3_Trip_HH_DegC - r_Alm3_Deadband_DegC)) THEN
    r_Alm3_Timer_H_ms := r_Alm3_Timer_H_ms + r_CycleScanPeriod_ms;
    IF r_Alm3_Timer_H_ms >= 80.0 THEN
        b_Alm3_Active_H := TRUE;
    END_IF;
ELSE
    IF r_TMR_VotedDieTemp_DegC < (r_Alm3_Trip_H_DegC - r_Alm3_Deadband_DegC) THEN
        r_Alm3_Timer_H_ms := 0.0;
        b_Alm3_Active_H := FALSE;
        b_Alm3_Ack_H := FALSE;
    END_IF;
END_IF;

(* Low Warning Trip Evaluation *)
IF (r_TMR_VotedDieTemp_DegC <= r_Alm3_Trip_L_DegC) AND (r_TMR_VotedDieTemp_DegC > (r_Alm3_Trip_LL_DegC + r_Alm3_Deadband_DegC)) THEN
    r_Alm3_Timer_L_ms := r_Alm3_Timer_L_ms + r_CycleScanPeriod_ms;
    IF r_Alm3_Timer_L_ms >= 80.0 THEN
        b_Alm3_Active_L := TRUE;
    END_IF;
ELSE
    IF r_TMR_VotedDieTemp_DegC > (r_Alm3_Trip_L_DegC + r_Alm3_Deadband_DegC) THEN
        r_Alm3_Timer_L_ms := 0.0;
        b_Alm3_Active_L := FALSE;
        b_Alm3_Ack_L := FALSE;
    END_IF;
END_IF;

(* Low-Low Critical Trip Evaluation *)
IF r_TMR_VotedDieTemp_DegC <= r_Alm3_Trip_LL_DegC THEN
    r_Alm3_Timer_LL_ms := r_Alm3_Timer_LL_ms + r_CycleScanPeriod_ms;
    IF r_Alm3_Timer_LL_ms >= 30.0 THEN
        b_Alm3_Active_LL := TRUE;
    END_IF;
ELSE
    IF r_TMR_VotedDieTemp_DegC > (r_Alm3_Trip_LL_DegC + r_Alm3_Deadband_DegC) THEN
        r_Alm3_Timer_LL_ms := 0.0;
        b_Alm3_Active_LL := FALSE;
        b_Alm3_Ack_LL := FALSE;
    END_IF;
END_IF;

(* Manual Operator Acknowledgment Strobe Processing *)
IF b_AcknowledgeAlarms_Strobe THEN
    IF b_Alm3_Active_HH THEN b_Alm3_Ack_HH := TRUE; END_IF;
    IF b_Alm3_Active_H THEN b_Alm3_Ack_H := TRUE; END_IF;
    IF b_Alm3_Active_L THEN b_Alm3_Ack_L := TRUE; END_IF;
    IF b_Alm3_Active_LL THEN b_Alm3_Ack_LL := TRUE; END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* ISA-18.2 ALARM LOOP 4: 4-CORNER RAM LEVELING TILT SKEW [um]                                                                    *)
(* ---------------------------------------------------------------------------------------------------- *)
(* High-High Critical Trip Evaluation *)
IF r_TMR_VotedTiltSkew_um >= r_Alm4_Trip_HH_um THEN
    r_Alm4_Timer_HH_ms := r_Alm4_Timer_HH_ms + r_CycleScanPeriod_ms;
    IF r_Alm4_Timer_HH_ms >= 20.0 THEN
        b_Alm4_Active_HH := TRUE;
    END_IF;
ELSE
    IF r_TMR_VotedTiltSkew_um < (r_Alm4_Trip_HH_um - r_Alm4_Deadband_um) THEN
        r_Alm4_Timer_HH_ms := 0.0;
        b_Alm4_Active_HH := FALSE;
        b_Alm4_Ack_HH := FALSE;
    END_IF;
END_IF;

(* High Warning Trip Evaluation *)
IF (r_TMR_VotedTiltSkew_um >= r_Alm4_Trip_H_um) AND (r_TMR_VotedTiltSkew_um < (r_Alm4_Trip_HH_um - r_Alm4_Deadband_um)) THEN
    r_Alm4_Timer_H_ms := r_Alm4_Timer_H_ms + r_CycleScanPeriod_ms;
    IF r_Alm4_Timer_H_ms >= 50.0 THEN
        b_Alm4_Active_H := TRUE;
    END_IF;
ELSE
    IF r_TMR_VotedTiltSkew_um < (r_Alm4_Trip_H_um - r_Alm4_Deadband_um) THEN
        r_Alm4_Timer_H_ms := 0.0;
        b_Alm4_Active_H := FALSE;
        b_Alm4_Ack_H := FALSE;
    END_IF;
END_IF;

(* Low Warning Trip Evaluation *)
IF (r_TMR_VotedTiltSkew_um <= r_Alm4_Trip_L_um) AND (r_TMR_VotedTiltSkew_um > (r_Alm4_Trip_LL_um + r_Alm4_Deadband_um)) THEN
    r_Alm4_Timer_L_ms := r_Alm4_Timer_L_ms + r_CycleScanPeriod_ms;
    IF r_Alm4_Timer_L_ms >= 50.0 THEN
        b_Alm4_Active_L := TRUE;
    END_IF;
ELSE
    IF r_TMR_VotedTiltSkew_um > (r_Alm4_Trip_L_um + r_Alm4_Deadband_um) THEN
        r_Alm4_Timer_L_ms := 0.0;
        b_Alm4_Active_L := FALSE;
        b_Alm4_Ack_L := FALSE;
    END_IF;
END_IF;

(* Low-Low Critical Trip Evaluation *)
IF r_TMR_VotedTiltSkew_um <= r_Alm4_Trip_LL_um THEN
    r_Alm4_Timer_LL_ms := r_Alm4_Timer_LL_ms + r_CycleScanPeriod_ms;
    IF r_Alm4_Timer_LL_ms >= 20.0 THEN
        b_Alm4_Active_LL := TRUE;
    END_IF;
ELSE
    IF r_TMR_VotedTiltSkew_um > (r_Alm4_Trip_LL_um + r_Alm4_Deadband_um) THEN
        r_Alm4_Timer_LL_ms := 0.0;
        b_Alm4_Active_LL := FALSE;
        b_Alm4_Ack_LL := FALSE;
    END_IF;
END_IF;

(* Manual Operator Acknowledgment Strobe Processing *)
IF b_AcknowledgeAlarms_Strobe THEN
    IF b_Alm4_Active_HH THEN b_Alm4_Ack_HH := TRUE; END_IF;
    IF b_Alm4_Active_H THEN b_Alm4_Ack_H := TRUE; END_IF;
    IF b_Alm4_Active_L THEN b_Alm4_Ack_L := TRUE; END_IF;
    IF b_Alm4_Active_LL THEN b_Alm4_Ack_LL := TRUE; END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* ISA-18.2 ALARM LOOP 5: VACUUM CHAMBER PRESSURE [mbar]                                                                    *)
(* ---------------------------------------------------------------------------------------------------- *)
(* High-High Critical Trip Evaluation *)
IF r_VacuumChamberPressure_mbar >= r_Alm5_Trip_HH_mbar THEN
    r_Alm5_Timer_HH_ms := r_Alm5_Timer_HH_ms + r_CycleScanPeriod_ms;
    IF r_Alm5_Timer_HH_ms >= 50.0 THEN
        b_Alm5_Active_HH := TRUE;
    END_IF;
ELSE
    IF r_VacuumChamberPressure_mbar < (r_Alm5_Trip_HH_mbar - r_Alm5_Deadband_mbar) THEN
        r_Alm5_Timer_HH_ms := 0.0;
        b_Alm5_Active_HH := FALSE;
        b_Alm5_Ack_HH := FALSE;
    END_IF;
END_IF;

(* High Warning Trip Evaluation *)
IF (r_VacuumChamberPressure_mbar >= r_Alm5_Trip_H_mbar) AND (r_VacuumChamberPressure_mbar < (r_Alm5_Trip_HH_mbar - r_Alm5_Deadband_mbar)) THEN
    r_Alm5_Timer_H_ms := r_Alm5_Timer_H_ms + r_CycleScanPeriod_ms;
    IF r_Alm5_Timer_H_ms >= 100.0 THEN
        b_Alm5_Active_H := TRUE;
    END_IF;
ELSE
    IF r_VacuumChamberPressure_mbar < (r_Alm5_Trip_H_mbar - r_Alm5_Deadband_mbar) THEN
        r_Alm5_Timer_H_ms := 0.0;
        b_Alm5_Active_H := FALSE;
        b_Alm5_Ack_H := FALSE;
    END_IF;
END_IF;

(* Low Warning Trip Evaluation *)
IF (r_VacuumChamberPressure_mbar <= r_Alm5_Trip_L_mbar) AND (r_VacuumChamberPressure_mbar > (r_Alm5_Trip_LL_mbar + r_Alm5_Deadband_mbar)) THEN
    r_Alm5_Timer_L_ms := r_Alm5_Timer_L_ms + r_CycleScanPeriod_ms;
    IF r_Alm5_Timer_L_ms >= 100.0 THEN
        b_Alm5_Active_L := TRUE;
    END_IF;
ELSE
    IF r_VacuumChamberPressure_mbar > (r_Alm5_Trip_L_mbar + r_Alm5_Deadband_mbar) THEN
        r_Alm5_Timer_L_ms := 0.0;
        b_Alm5_Active_L := FALSE;
        b_Alm5_Ack_L := FALSE;
    END_IF;
END_IF;

(* Low-Low Critical Trip Evaluation *)
IF r_VacuumChamberPressure_mbar <= r_Alm5_Trip_LL_mbar THEN
    r_Alm5_Timer_LL_ms := r_Alm5_Timer_LL_ms + r_CycleScanPeriod_ms;
    IF r_Alm5_Timer_LL_ms >= 50.0 THEN
        b_Alm5_Active_LL := TRUE;
    END_IF;
ELSE
    IF r_VacuumChamberPressure_mbar > (r_Alm5_Trip_LL_mbar + r_Alm5_Deadband_mbar) THEN
        r_Alm5_Timer_LL_ms := 0.0;
        b_Alm5_Active_LL := FALSE;
        b_Alm5_Ack_LL := FALSE;
    END_IF;
END_IF;

(* Manual Operator Acknowledgment Strobe Processing *)
IF b_AcknowledgeAlarms_Strobe THEN
    IF b_Alm5_Active_HH THEN b_Alm5_Ack_HH := TRUE; END_IF;
    IF b_Alm5_Active_H THEN b_Alm5_Ack_H := TRUE; END_IF;
    IF b_Alm5_Active_L THEN b_Alm5_Ack_L := TRUE; END_IF;
    IF b_Alm5_Active_LL THEN b_Alm5_Ack_LL := TRUE; END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* ISA-18.2 ALARM LOOP 6: CONSTITUTIVE SELLARS-TEGART FLOW STRESS [MPa]                                                                    *)
(* ---------------------------------------------------------------------------------------------------- *)
(* High-High Critical Trip Evaluation *)
IF r_Obs_FlowStress_MPa >= r_Alm6_Trip_HH_MPa THEN
    r_Alm6_Timer_HH_ms := r_Alm6_Timer_HH_ms + r_CycleScanPeriod_ms;
    IF r_Alm6_Timer_HH_ms >= 30.0 THEN
        b_Alm6_Active_HH := TRUE;
    END_IF;
ELSE
    IF r_Obs_FlowStress_MPa < (r_Alm6_Trip_HH_MPa - r_Alm6_Deadband_MPa) THEN
        r_Alm6_Timer_HH_ms := 0.0;
        b_Alm6_Active_HH := FALSE;
        b_Alm6_Ack_HH := FALSE;
    END_IF;
END_IF;

(* High Warning Trip Evaluation *)
IF (r_Obs_FlowStress_MPa >= r_Alm6_Trip_H_MPa) AND (r_Obs_FlowStress_MPa < (r_Alm6_Trip_HH_MPa - r_Alm6_Deadband_MPa)) THEN
    r_Alm6_Timer_H_ms := r_Alm6_Timer_H_ms + r_CycleScanPeriod_ms;
    IF r_Alm6_Timer_H_ms >= 60.0 THEN
        b_Alm6_Active_H := TRUE;
    END_IF;
ELSE
    IF r_Obs_FlowStress_MPa < (r_Alm6_Trip_H_MPa - r_Alm6_Deadband_MPa) THEN
        r_Alm6_Timer_H_ms := 0.0;
        b_Alm6_Active_H := FALSE;
        b_Alm6_Ack_H := FALSE;
    END_IF;
END_IF;

(* Low Warning Trip Evaluation *)
IF (r_Obs_FlowStress_MPa <= r_Alm6_Trip_L_MPa) AND (r_Obs_FlowStress_MPa > (r_Alm6_Trip_LL_MPa + r_Alm6_Deadband_MPa)) THEN
    r_Alm6_Timer_L_ms := r_Alm6_Timer_L_ms + r_CycleScanPeriod_ms;
    IF r_Alm6_Timer_L_ms >= 60.0 THEN
        b_Alm6_Active_L := TRUE;
    END_IF;
ELSE
    IF r_Obs_FlowStress_MPa > (r_Alm6_Trip_L_MPa + r_Alm6_Deadband_MPa) THEN
        r_Alm6_Timer_L_ms := 0.0;
        b_Alm6_Active_L := FALSE;
        b_Alm6_Ack_L := FALSE;
    END_IF;
END_IF;

(* Low-Low Critical Trip Evaluation *)
IF r_Obs_FlowStress_MPa <= r_Alm6_Trip_LL_MPa THEN
    r_Alm6_Timer_LL_ms := r_Alm6_Timer_LL_ms + r_CycleScanPeriod_ms;
    IF r_Alm6_Timer_LL_ms >= 30.0 THEN
        b_Alm6_Active_LL := TRUE;
    END_IF;
ELSE
    IF r_Obs_FlowStress_MPa > (r_Alm6_Trip_LL_MPa + r_Alm6_Deadband_MPa) THEN
        r_Alm6_Timer_LL_ms := 0.0;
        b_Alm6_Active_LL := FALSE;
        b_Alm6_Ack_LL := FALSE;
    END_IF;
END_IF;

(* Manual Operator Acknowledgment Strobe Processing *)
IF b_AcknowledgeAlarms_Strobe THEN
    IF b_Alm6_Active_HH THEN b_Alm6_Ack_HH := TRUE; END_IF;
    IF b_Alm6_Active_H THEN b_Alm6_Ack_H := TRUE; END_IF;
    IF b_Alm6_Active_L THEN b_Alm6_Ack_L := TRUE; END_IF;
    IF b_Alm6_Active_LL THEN b_Alm6_Ack_LL := TRUE; END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* ISA-18.2 ALARM LOOP 7: TITANIUM BILLET SURFACE PYROMETER [deg C]                                                                    *)
(* ---------------------------------------------------------------------------------------------------- *)
(* High-High Critical Trip Evaluation *)
IF r_BilletSurfacePyrometer_DegC >= r_Alm7_Trip_HH_DegC THEN
    r_Alm7_Timer_HH_ms := r_Alm7_Timer_HH_ms + r_CycleScanPeriod_ms;
    IF r_Alm7_Timer_HH_ms >= 30.0 THEN
        b_Alm7_Active_HH := TRUE;
    END_IF;
ELSE
    IF r_BilletSurfacePyrometer_DegC < (r_Alm7_Trip_HH_DegC - r_Alm7_Deadband_DegC) THEN
        r_Alm7_Timer_HH_ms := 0.0;
        b_Alm7_Active_HH := FALSE;
        b_Alm7_Ack_HH := FALSE;
    END_IF;
END_IF;

(* High Warning Trip Evaluation *)
IF (r_BilletSurfacePyrometer_DegC >= r_Alm7_Trip_H_DegC) AND (r_BilletSurfacePyrometer_DegC < (r_Alm7_Trip_HH_DegC - r_Alm7_Deadband_DegC)) THEN
    r_Alm7_Timer_H_ms := r_Alm7_Timer_H_ms + r_CycleScanPeriod_ms;
    IF r_Alm7_Timer_H_ms >= 60.0 THEN
        b_Alm7_Active_H := TRUE;
    END_IF;
ELSE
    IF r_BilletSurfacePyrometer_DegC < (r_Alm7_Trip_H_DegC - r_Alm7_Deadband_DegC) THEN
        r_Alm7_Timer_H_ms := 0.0;
        b_Alm7_Active_H := FALSE;
        b_Alm7_Ack_H := FALSE;
    END_IF;
END_IF;

(* Low Warning Trip Evaluation *)
IF (r_BilletSurfacePyrometer_DegC <= r_Alm7_Trip_L_DegC) AND (r_BilletSurfacePyrometer_DegC > (r_Alm7_Trip_LL_DegC + r_Alm7_Deadband_DegC)) THEN
    r_Alm7_Timer_L_ms := r_Alm7_Timer_L_ms + r_CycleScanPeriod_ms;
    IF r_Alm7_Timer_L_ms >= 60.0 THEN
        b_Alm7_Active_L := TRUE;
    END_IF;
ELSE
    IF r_BilletSurfacePyrometer_DegC > (r_Alm7_Trip_L_DegC + r_Alm7_Deadband_DegC) THEN
        r_Alm7_Timer_L_ms := 0.0;
        b_Alm7_Active_L := FALSE;
        b_Alm7_Ack_L := FALSE;
    END_IF;
END_IF;

(* Low-Low Critical Trip Evaluation *)
IF r_BilletSurfacePyrometer_DegC <= r_Alm7_Trip_LL_DegC THEN
    r_Alm7_Timer_LL_ms := r_Alm7_Timer_LL_ms + r_CycleScanPeriod_ms;
    IF r_Alm7_Timer_LL_ms >= 30.0 THEN
        b_Alm7_Active_LL := TRUE;
    END_IF;
ELSE
    IF r_BilletSurfacePyrometer_DegC > (r_Alm7_Trip_LL_DegC + r_Alm7_Deadband_DegC) THEN
        r_Alm7_Timer_LL_ms := 0.0;
        b_Alm7_Active_LL := FALSE;
        b_Alm7_Ack_LL := FALSE;
    END_IF;
END_IF;

(* Manual Operator Acknowledgment Strobe Processing *)
IF b_AcknowledgeAlarms_Strobe THEN
    IF b_Alm7_Active_HH THEN b_Alm7_Ack_HH := TRUE; END_IF;
    IF b_Alm7_Active_H THEN b_Alm7_Ack_H := TRUE; END_IF;
    IF b_Alm7_Active_L THEN b_Alm7_Ack_L := TRUE; END_IF;
    IF b_Alm7_Active_LL THEN b_Alm7_Ack_LL := TRUE; END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* ISA-18.2 ALARM LOOP 8: HYDRAULIC SUMP OIL TEMPERATURE [deg C]                                                                    *)
(* ---------------------------------------------------------------------------------------------------- *)
(* High-High Critical Trip Evaluation *)
IF r_HydraulicOilSumpTemp_DegC >= r_Alm8_Trip_HH_DegC THEN
    r_Alm8_Timer_HH_ms := r_Alm8_Timer_HH_ms + r_CycleScanPeriod_ms;
    IF r_Alm8_Timer_HH_ms >= 100.0 THEN
        b_Alm8_Active_HH := TRUE;
    END_IF;
ELSE
    IF r_HydraulicOilSumpTemp_DegC < (r_Alm8_Trip_HH_DegC - r_Alm8_Deadband_DegC) THEN
        r_Alm8_Timer_HH_ms := 0.0;
        b_Alm8_Active_HH := FALSE;
        b_Alm8_Ack_HH := FALSE;
    END_IF;
END_IF;

(* High Warning Trip Evaluation *)
IF (r_HydraulicOilSumpTemp_DegC >= r_Alm8_Trip_H_DegC) AND (r_HydraulicOilSumpTemp_DegC < (r_Alm8_Trip_HH_DegC - r_Alm8_Deadband_DegC)) THEN
    r_Alm8_Timer_H_ms := r_Alm8_Timer_H_ms + r_CycleScanPeriod_ms;
    IF r_Alm8_Timer_H_ms >= 250.0 THEN
        b_Alm8_Active_H := TRUE;
    END_IF;
ELSE
    IF r_HydraulicOilSumpTemp_DegC < (r_Alm8_Trip_H_DegC - r_Alm8_Deadband_DegC) THEN
        r_Alm8_Timer_H_ms := 0.0;
        b_Alm8_Active_H := FALSE;
        b_Alm8_Ack_H := FALSE;
    END_IF;
END_IF;

(* Low Warning Trip Evaluation *)
IF (r_HydraulicOilSumpTemp_DegC <= r_Alm8_Trip_L_DegC) AND (r_HydraulicOilSumpTemp_DegC > (r_Alm8_Trip_LL_DegC + r_Alm8_Deadband_DegC)) THEN
    r_Alm8_Timer_L_ms := r_Alm8_Timer_L_ms + r_CycleScanPeriod_ms;
    IF r_Alm8_Timer_L_ms >= 250.0 THEN
        b_Alm8_Active_L := TRUE;
    END_IF;
ELSE
    IF r_HydraulicOilSumpTemp_DegC > (r_Alm8_Trip_L_DegC + r_Alm8_Deadband_DegC) THEN
        r_Alm8_Timer_L_ms := 0.0;
        b_Alm8_Active_L := FALSE;
        b_Alm8_Ack_L := FALSE;
    END_IF;
END_IF;

(* Low-Low Critical Trip Evaluation *)
IF r_HydraulicOilSumpTemp_DegC <= r_Alm8_Trip_LL_DegC THEN
    r_Alm8_Timer_LL_ms := r_Alm8_Timer_LL_ms + r_CycleScanPeriod_ms;
    IF r_Alm8_Timer_LL_ms >= 100.0 THEN
        b_Alm8_Active_LL := TRUE;
    END_IF;
ELSE
    IF r_HydraulicOilSumpTemp_DegC > (r_Alm8_Trip_LL_DegC + r_Alm8_Deadband_DegC) THEN
        r_Alm8_Timer_LL_ms := 0.0;
        b_Alm8_Active_LL := FALSE;
        b_Alm8_Ack_LL := FALSE;
    END_IF;
END_IF;

(* Manual Operator Acknowledgment Strobe Processing *)
IF b_AcknowledgeAlarms_Strobe THEN
    IF b_Alm8_Active_HH THEN b_Alm8_Ack_HH := TRUE; END_IF;
    IF b_Alm8_Active_H THEN b_Alm8_Ack_H := TRUE; END_IF;
    IF b_Alm8_Active_L THEN b_Alm8_Ack_L := TRUE; END_IF;
    IF b_Alm8_Active_LL THEN b_Alm8_Ack_LL := TRUE; END_IF;
END_IF;

(* Emergency Interlock Escalation: Any Active HH or LL Critical Alarm Trips Global Fault *)
IF b_Alm1_Active_HH OR b_Alm2_Active_HH OR b_Alm3_Active_HH OR b_Alm4_Active_HH OR 
   b_Alm5_Active_HH OR b_Alm6_Active_HH OR b_Alm7_Active_HH OR b_Alm8_Active_HH OR 
   b_Alm2_Active_LL OR b_Alm3_Active_LL OR b_Alm7_Active_LL THEN
    b_GlobalFaultActive := TRUE;
END_IF;

(* ==================================================================================================== *)
(* 5.2 FIELDBUS TELEMETRY BIT-PACKED WORDS (PROFINET / OPC UA / ETHERCAT)                               *)
(* ==================================================================================================== *)
(* ---------------------------------------------------------------------------------------------------- *)
(* TELEMETRY WORD 1: dw_Telemetry_Safety_ISO13849_PLe (32-Bit Bit-Packed Machine Safety Status)        *)
(* ---------------------------------------------------------------------------------------------------- *)
dw_Telemetry_Safety_ISO13849_PLe := 16#00000000;
IF b_EmergencyStopDualCh_PL_e THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 0); (* Bit 0: Dual-Channel Hardwired E-Stop Relay Closed (Safe) *)
END_IF;
IF b_SafetyShieldInterlockClosed THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 1); (* Bit 1: Hydraulic Front Enclosure Safety Gate Interlock Closed *)
END_IF;
IF b_HydraulicPowerUnitRunning THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 2); (* Bit 2: Main 6x 450 kW Servo Hydraulic Pumps Running Confirmed *)
END_IF;
IF b_FurnaceTransferClearance THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 3); (* Bit 3: 950 deg C Rotary Hearth Furnace Robotic Track Clear *)
END_IF;
IF b_SystemReady THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 4); (* Bit 4: Forging Cell Master Operational Readiness Confirmed *)
END_IF;
IF b_AutoCycleActive THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 5); (* Bit 5: Automatic 14-Stage Isothermal Forging Sequence In Progress *)
END_IF;
IF b_CycleCompleteStrobe THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 6); (* Bit 6: Single Turbine Disc Forging Sequence Successfully Completed *)
END_IF;
IF b_GlobalFaultActive THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 7); (* Bit 7: Global Critical Fault Interlock Latched *)
END_IF;
IF b_TMR_Tonnage_DegradedMode THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 8); (* Bit 8: TMR Channel 1 (Tonnage) Operating in Degraded Mode *)
END_IF;
IF b_TMR_Tonnage_TotalFailure THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 9); (* Bit 9: TMR Channel 1 (Tonnage) Complete Loss of Redundancy *)
END_IF;
IF b_TMR_HydPressure_DegradedMode THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 10); (* Bit 10: TMR Channel 2 (Pressure) Operating in Degraded Mode *)
END_IF;
IF b_TMR_HydPress_TotalFailure THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 11); (* Bit 11: TMR Channel 2 (Pressure) Complete Loss of Redundancy *)
END_IF;
IF b_TMR_DieTemp_DegradedMode THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 12); (* Bit 12: TMR Channel 3 (Die Temp) Operating in Degraded Mode *)
END_IF;
IF b_TMR_DieTemp_TotalFailure THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 13); (* Bit 13: TMR Channel 3 (Die Temp) Complete Loss of Redundancy *)
END_IF;
IF b_TMR_TiltSkew_DegradedMode THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 14); (* Bit 14: TMR Channel 4 (Tilt Skew) Operating in Degraded Mode *)
END_IF;
IF b_TMR_TiltSkew_TotalFailure THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 15); (* Bit 15: TMR Channel 4 (Tilt Skew) Complete Loss of Redundancy *)
END_IF;
IF b_VacuumRoughingPumpRunning THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 16); (* Bit 16: Roots Vacuum Blower Mechanical Roughing Pump Active *)
END_IF;
IF b_TurbomolecularPumpAtSpeed THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 17); (* Bit 17: Turbomolecular Ultra-High Vacuum Pump Nominal RPM Reached *)
END_IF;
IF b_VacuumChamberDoorOpenCmd THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 18); (* Bit 18: Vacuum Transfer Lock Door Open Hydraulic Actuator Command *)
END_IF;
IF b_ArgonBackfillVentValveOpen THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 19); (* Bit 19: High-Purity Argon Chamber Vent Equalization Valve Open *)
END_IF;
IF b_VacuumRoughingValveOpen THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 20); (* Bit 20: Foreline Roughing Vacuum Isolation Poppet Valve Open *)
END_IF;
IF b_VacuumHighVacGateValveOpen THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 21); (* Bit 21: High-Vacuum Turbomolecular Isolation Gate Valve Open *)
END_IF;
IF b_RoboticLoaderAtForgingPos THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 22); (* Bit 22: Vacuum Transfer Gripper Robot Positioned In Die Cavity *)
END_IF;
IF b_RoboticLoaderRetractedClear THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 23); (* Bit 23: Vacuum Transfer Gripper Robot Parked In Safe Home Pos *)
END_IF;
IF b_LowerDieEjectorRetractedLS THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 24); (* Bit 24: Lower Die 4-Pin Hydraulic Ejector Fully Down Limit Switch *)
END_IF;
IF b_LowerDieEjectorExtendedLS THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 25); (* Bit 25: Lower Die 4-Pin Hydraulic Ejector Fully Up Limit Switch *)
END_IF;
IF b_DiscDimensionQualityPassed THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 26); (* Bit 26: Post-Forging 3D Laser Metrology Dimension Spec Passed *)
END_IF;
IF b_InductionInverterRunEnable THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 27); (* Bit 27: Medium-Frequency Induction Inverter IGBT Gate Permissive *)
END_IF;
IF b_PreFillValvesEnergized THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 28); (* Bit 28: Main Hydraulic Header Gravity Tank Pre-Fill Valves Open *)
END_IF;
IF b_FSM_StageComplete THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 29); (* Bit 29: Active FSM Sequencer Step Conditions Fulfilled *)
END_IF;
IF b_FSM_StageFault THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 30); (* Bit 30: Active FSM Sequencer Step Timeout or Guard Fault *)
END_IF;
IF b_FirstScanInit THEN
    dw_Telemetry_Safety_ISO13849_PLe := dw_Telemetry_Safety_ISO13849_PLe OR SHL(DWORD#16#00000001, 31); (* Bit 31: Cold-Boot Controller Initialization Routine Completed *)
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* TELEMETRY WORD 2: dw_Telemetry_Hydraulic_DIN_EN_693 (32-Bit Hydraulic Press Operational Status)     *)
(* ---------------------------------------------------------------------------------------------------- *)
dw_Telemetry_Hydraulic_DIN_EN_693 := 16#00000000;
IF (r_MainPumpSwashplateCmd_Pct > 0.1) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 0); (* Bit 0: Axial Piston Main Pump Displacement Stroking > 0% *)
END_IF;
IF (r_MainPumpSwashplateCmd_Pct >= 50.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 1); (* Bit 1: Main Hydraulic Pump Operating Above 50% Swashplate Angle *)
END_IF;
IF (r_ActiveDecompressValveCmd_Pct > 0.5) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 2); (* Bit 2: Controlled Proportional Hydraulic Decompress Valve Open *)
END_IF;
IF (r_CounterbalanceValveCmd_Pct >= 95.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 3); (* Bit 3: Dynamic Counterbalance Valve Locked 100% (Safety Hold) *)
END_IF;
IF (r_CounterbalanceValveCmd_Pct < 10.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 4); (* Bit 4: Counterbalance Valve Discharged for Full Pressing Tonnage *)
END_IF;
IF (r_LowerDieEjectorHydCmd_Pct > 5.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 5); (* Bit 5: Lower Die Part Lifter Hydraulic Circuit Pressurized *)
END_IF;
IF (r_TMR_VotedHydPressure_bar >= 300.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 6); (* Bit 6: Main Manifold Operating at High Forging Pressure (> 300 bar) *)
END_IF;
IF (r_TMR_VotedHydPressure_bar <= 10.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 7); (* Bit 7: Main Manifold Hydraulic Stored Energy Fully Decompressed *)
END_IF;
IF (r_CylPressure_FL_bar >= 250.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 8); (* Bit 8: Front-Left Cylinder Active Pressing Pressure > 250 bar *)
END_IF;
IF (r_CylPressure_FR_bar >= 250.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 9); (* Bit 9: Front-Right Cylinder Active Pressing Pressure > 250 bar *)
END_IF;
IF (r_CylPressure_RL_bar >= 250.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 10); (* Bit 10: Rear-Left Cylinder Active Pressing Pressure > 250 bar *)
END_IF;
IF (r_CylPressure_RR_bar >= 250.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 11); (* Bit 11: Rear-Right Cylinder Active Pressing Pressure > 250 bar *)
END_IF;
IF (ABS(r_EccentricMomentX_kNm) > 500.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 12); (* Bit 12: Platen Pitching Moment Mx Exceeds 500 kNm Leveling Threshold *)
END_IF;
IF (ABS(r_EccentricMomentY_kNm) > 500.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 13); (* Bit 13: Platen Rolling Moment My Exceeds 500 kNm Leveling Threshold *)
END_IF;
IF (r_RamLevelingValve_FL_Cmd_L_min > 5.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 14); (* Bit 14: Front-Left Dynamic Servo Leveling Valve Active Positive *)
END_IF;
IF (r_RamLevelingValve_FR_Cmd_L_min < -5.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 15); (* Bit 15: Front-Right Dynamic Servo Leveling Valve Active Negative *)
END_IF;
IF (r_TMR_VotedTiltSkew_um > 10.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 16); (* Bit 16: Ram Dynamic Leveling Tilt Exceeds 10.0 um Warning Band *)
END_IF;
IF (r_MaxCornerTiltDev_um > r_MaxAllowableRamTilt_um) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 17); (* Bit 17: Corner Tilt Exceeds Maximum Permissible Spec (20.0 um) *)
END_IF;
IF (r_HydCoolingWaterFlow_L_min >= 400.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 18); (* Bit 18: Heat Exchanger Oil Cooling Water Flow Rate Normal (> 400 L/min) *)
END_IF;
IF (r_HydraulicOilSumpTemp_DegC > 50.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 19); (* Bit 19: Hydraulic Fluid Reservoir Sump Temperature Elevated (> 50 deg C) *)
END_IF;
IF (x_est[2] < -50.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 20); (* Bit 20: Ram Downward Rapid Velocity Exceeds 50 mm/s *)
END_IF;
IF (x_est[2] < -150.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 21); (* Bit 21: Ram Downward Velocity Reaching Rapid Approach Max (180 mm/s) *)
END_IF;
IF (x_est[2] > 20.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 22); (* Bit 22: Ram Upward Retract Velocity Active (> 20 mm/s) *)
END_IF;
IF (x_est[1] >= (r_InitialBilletHeight_mm - 5.0)) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 23); (* Bit 23: Ram Position at Top Dead Center Rest Park (420.0 mm) *)
END_IF;
IF (x_est[1] <= (r_FinalForgedWebThickness_mm + 1.0)) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 24); (* Bit 24: Ram Position Within 1.0 mm of Final Disc Web Target (65 mm) *)
END_IF;
IF (r_TotalCylForce_kN >= 50000.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 25); (* Bit 25: Total Combined Hydraulic Actuator Force Exceeds 50 MN (5,000 tons) *)
END_IF;
IF (r_TotalCylForce_kN >= 95000.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 26); (* Bit 26: Total Combined Hydraulic Force Reaching 100 MN Coining Rating *)
END_IF;
IF (r_ArgonBackfillPressure_bar >= 5.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 27); (* Bit 27: High-Purity Argon Gas Supply Header Pressure Normal (> 5.0 bar) *)
END_IF;
IF b_TMR_Tonnage_FaultA THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 28); (* Bit 28: Tie-Rod Load Cell Sensor A Hardware Discrepancy Latched *)
END_IF;
IF b_TMR_Tonnage_FaultB THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 29); (* Bit 29: Tie-Rod Load Cell Sensor B Hardware Discrepancy Latched *)
END_IF;
IF b_TMR_Tonnage_FaultC THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 30); (* Bit 30: Tie-Rod Load Cell Sensor C Hardware Discrepancy Latched *)
END_IF;
IF (r_CurrentStageElapsed_s > 60.0) THEN
    dw_Telemetry_Hydraulic_DIN_EN_693 := dw_Telemetry_Hydraulic_DIN_EN_693 OR SHL(DWORD#16#00000001, 31); (* Bit 31: Current Operational Stage Execution Time Exceeds 60.0 Seconds *)
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* TELEMETRY WORD 3: dw_Telemetry_Process_Isothermal (32-Bit Metallurgy & Thermal Telemetry)           *)
(* ---------------------------------------------------------------------------------------------------- *)
dw_Telemetry_Process_Isothermal := 16#00000000;
IF (r_TMR_VotedDieTemp_DegC >= 945.0) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 0); (* Bit 0: Upper Die Temperature in Isothermal Processing Window (> 945 C) *)
END_IF;
IF (r_TMR_VotedDieTemp_DegC >= 950.0) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 1); (* Bit 1: Upper Die Temperature Exactly Reaches Recipe Target (950 C) *)
END_IF;
IF (r_LowerDieTemp_DegC >= 945.0) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 2); (* Bit 2: Lower Die Surface Temperature in Isothermal Processing Window *)
END_IF;
IF (r_BilletSurfacePyrometer_DegC >= 940.0) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 3); (* Bit 3: Titanium Billet Optical Pyrometer Temperature Valid (> 940 C) *)
END_IF;
IF (r_VacuumChamberPressure_mbar <= 0.050) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 4); (* Bit 4: High-Vacuum Level Adequate for Titanium Oxidation Prevention *)
END_IF;
IF (r_VacuumChamberPressure_mbar <= r_VacuumChamberTarget_mbar) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 5); (* Bit 5: Vacuum Level Achieves Target Alpha-Case Limit (0.045 mbar) *)
END_IF;
IF (r_InductionPowerActual_kW > 50.0) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 6); (* Bit 6: Medium-Frequency Induction Heating System Actively Radiating *)
END_IF;
IF (r_InductionPowerActual_kW >= 500.0) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 7); (* Bit 7: Induction Heating Power Operating Above 500 kW Ramp Rate *)
END_IF;
IF (r_InductionPowerActual_kW >= 1000.0) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 8); (* Bit 8: Induction Heating Power Operating Above 1.0 MW Booster Mode *)
END_IF;
IF (r_InstantaneousTrueStrain > 0.050) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 9); (* Bit 9: Plastic Compressive True Logarithmic Strain Exceeds 0.05 *)
END_IF;
IF (r_InstantaneousTrueStrain > 0.350) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 10); (* Bit 10: Plastic Compressive True Logarithmic Strain Exceeds 0.35 *)
END_IF;
IF (r_InstantaneousTrueStrain > 0.850) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 11); (* Bit 11: Plastic Compressive True Strain Reaches Severe Disc Web Flow *)
END_IF;
IF (r_InstantaneousStrainRate_s_inv >= 0.0008) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 12); (* Bit 12: True Strain Rate Within Superplastic Processing Window *)
END_IF;
IF (r_InstantaneousStrainRate_s_inv <= 0.0012) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 13); (* Bit 13: True Strain Rate Controlled Below Upper Flow Instability Limit *)
END_IF;
IF (r_DRX_RecrystallizedFraction > 0.10) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 14); (* Bit 14: Dynamic Recrystallization (DRX) Microstructure Nucleation Active *)
END_IF;
IF (r_DRX_RecrystallizedFraction >= 0.50) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 15); (* Bit 15: DRX Volume Fraction Exceeds 50% Equiaxed Grain Transformation *)
END_IF;
IF (r_DRX_RecrystallizedFraction >= 0.90) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 16); (* Bit 16: DRX Complete Recrystallization (> 90%) Achieved across Disc *)
END_IF;
IF (r_Obs_DRX_GrainSize_um <= 10.0) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 17); (* Bit 17: Refined Prior Alpha Grain Size Within Aerospace Blisk Spec *)
END_IF;
IF (r_Obs_FlowStress_MPa > 20.0) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 18); (* Bit 18: Constitutive Ti-6Al-4V Flow Stress Normal Resistance Established *)
END_IF;
IF (r_Obs_FlowStress_MPa <= 85.0) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 19); (* Bit 19: Constitutive Flow Stress Held Below Die Superalloy Rupture Limit *)
END_IF;
IF (r_ZenerHollomonParameter_Z > 1.0e8) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 20); (* Bit 20: Zener-Hollomon Microstructural Parameter Validated (> 10^8 s^-1) *)
END_IF;
IF (n_FSM_State = 8) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 21); (* Bit 21: FSM Executing Stage 8 (Superplastic Slow Extrusion Stroke) *)
END_IF;
IF (n_FSM_State = 9) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 22); (* Bit 22: FSM Executing Stage 9 (Final Coining Dwell at 100 MN Force) *)
END_IF;
IF (n_FSM_State = 10) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 23); (* Bit 23: FSM Executing Stage 10 (Controlled Hydraulic Decompression) *)
END_IF;
IF b_TMR_DieTemp_FaultA THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 24); (* Bit 24: Upper Die Thermocouple Probe A Discrepancy Latched *)
END_IF;
IF b_TMR_DieTemp_FaultB THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 25); (* Bit 25: Upper Die Thermocouple Probe B Discrepancy Latched *)
END_IF;
IF b_TMR_DieTemp_FaultC THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 26); (* Bit 26: Upper Die Optical Pyrometer Ch C Discrepancy Latched *)
END_IF;
IF (r_LaserMeasuredWebThick_mm > 0.0) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 27); (* Bit 27: Laser Profilometer Valid Dimensional Metrology Reading Available *)
END_IF;
IF b_LaserMetrologyScanComplete THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 28); (* Bit 28: 3D Optical Laser Scanning Dimensional Gate Evaluation Done *)
END_IF;
IF b_LaserMetrologyScanTriggerCmd THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 29); (* Bit 29: Laser Metrology Inspection Sensor Head Triggered *)
END_IF;
IF b_RobotExtractForgedPartCmd THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 30); (* Bit 30: Robotic Finished Part Gripper Extraction Permissive Active *)
END_IF;
IF (r_DecompressStartPress_bar > 200.0) THEN
    dw_Telemetry_Process_Isothermal := dw_Telemetry_Process_Isothermal OR SHL(DWORD#16#00000001, 31); (* Bit 31: Hydraulic Decompression Initiated from High Coining Pressure *)
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* TELEMETRY WORD 4: dw_Telemetry_Alarms_ISA18_2 (32-Bit Bit-Packed ISA-18.2 Alarms)                  *)
(* ---------------------------------------------------------------------------------------------------- *)
dw_Telemetry_Alarms_ISA18_2 := 16#00000000;
IF b_Alm1_Active_HH THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 0); (* Bit 0: Loop 1 (Tonnage) High-High Emergency Relief Overload Trip *)
END_IF;
IF b_Alm1_Active_H THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 1); (* Bit 1: Loop 1 (Tonnage) High Warning Limit Exceeded *)
END_IF;
IF b_Alm1_Active_L THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 2); (* Bit 2: Loop 1 (Tonnage) Low Contact Detection Threshold *)
END_IF;
IF b_Alm1_Active_LL THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 3); (* Bit 3: Loop 1 (Tonnage) Low-Low Loss of Contact Underload Trip *)
END_IF;
IF b_Alm2_Active_HH THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 4); (* Bit 4: Loop 2 (Hydraulic Pressure) High-High Overpressure Trip *)
END_IF;
IF b_Alm2_Active_H THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 5); (* Bit 5: Loop 2 (Hydraulic Pressure) High Operating Pressure Warning *)
END_IF;
IF b_Alm2_Active_L THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 6); (* Bit 6: Loop 2 (Hydraulic Pressure) Low Standby Pressure Warning *)
END_IF;
IF b_Alm2_Active_LL THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 7); (* Bit 7: Loop 2 (Hydraulic Pressure) Low-Low Loss of Pressure Trip *)
END_IF;
IF b_Alm3_Active_HH THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 8); (* Bit 8: Loop 3 (Upper Die Temp) High-High Superalloy Anneal Trip *)
END_IF;
IF b_Alm3_Active_H THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 9); (* Bit 9: Loop 3 (Upper Die Temp) High Isothermal Temperature Warning *)
END_IF;
IF b_Alm3_Active_L THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 10); (* Bit 10: Loop 3 (Upper Die Temp) Low Isothermal Temperature Warning *)
END_IF;
IF b_Alm3_Active_LL THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 11); (* Bit 11: Loop 3 (Upper Die Temp) Low-Low Brittle Forging Abort Trip *)
END_IF;
IF b_Alm4_Active_HH THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 12); (* Bit 12: Loop 4 (Ram Tilt Skew) High-High Column Jamming Trip *)
END_IF;
IF b_Alm4_Active_H THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 13); (* Bit 13: Loop 4 (Ram Tilt Skew) High Asymmetric Leveling Warning *)
END_IF;
IF b_Alm4_Active_L THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 14); (* Bit 14: Loop 4 (Ram Tilt Skew) Negative Asymmetric Leveling Warning *)
END_IF;
IF b_Alm4_Active_LL THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 15); (* Bit 15: Loop 4 (Ram Tilt Skew) Low-Low Negative Column Jamming Trip *)
END_IF;
IF b_Alm5_Active_HH THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 16); (* Bit 16: Loop 5 (Vacuum Chamber) High-High Alpha-Case Oxidation Threat *)
END_IF;
IF b_Alm5_Active_H THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 17); (* Bit 17: Loop 5 (Vacuum Chamber) High Vacuum Level Warning *)
END_IF;
IF b_Alm5_Active_L THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 18); (* Bit 18: Loop 5 (Vacuum Chamber) Low Vacuum Gauge Limit *)
END_IF;
IF b_Alm5_Active_LL THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 19); (* Bit 19: Loop 5 (Vacuum Chamber) Low-Low Sensor Range Malfunction *)
END_IF;
IF b_Alm6_Active_HH THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 20); (* Bit 20: Loop 6 (Flow Stress) High-High Ti-6Al-4V Rupture Trip *)
END_IF;
IF b_Alm6_Active_H THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 21); (* Bit 21: Loop 6 (Flow Stress) High Constitutive Resistance Warning *)
END_IF;
IF b_Alm6_Active_L THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 22); (* Bit 22: Loop 6 (Flow Stress) Low Billet Resistance Warning *)
END_IF;
IF b_Alm6_Active_LL THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 23); (* Bit 23: Loop 6 (Flow Stress) Low-Low Missing Workpiece Trip *)
END_IF;
IF b_Alm7_Active_HH THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 24); (* Bit 24: Loop 7 (Billet Temp) High-High Beta-Transus Microstructure Trip *)
END_IF;
IF b_Alm7_Active_H THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 25); (* Bit 25: Loop 7 (Billet Temp) High Billet Surface Temp Warning *)
END_IF;
IF b_Alm7_Active_L THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 26); (* Bit 26: Loop 7 (Billet Temp) Low Billet Chilling Warning *)
END_IF;
IF b_Alm7_Active_LL THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 27); (* Bit 27: Loop 7 (Billet Temp) Low-Low Severe Chilling Abort Trip *)
END_IF;
IF b_Alm8_Active_HH THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 28); (* Bit 28: Loop 8 (Oil Sump Temp) High-High Fluid Cavitation Trip *)
END_IF;
IF b_Alm8_Active_H THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 29); (* Bit 29: Loop 8 (Oil Sump Temp) High Fluid Temperature Warning *)
END_IF;
IF b_Alm8_Active_L THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 30); (* Bit 30: Loop 8 (Oil Sump Temp) Low Oil Temperature Circulation *)
END_IF;
IF b_Alm8_Active_LL THEN
    dw_Telemetry_Alarms_ISA18_2 := dw_Telemetry_Alarms_ISA18_2 OR SHL(DWORD#16#00000001, 31); (* Bit 31: Loop 8 (Oil Sump Temp) Low-Low Cold Oil Inhibit Trip *)
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* TELEMETRY WORD 5: dw_Telemetry_FSM_Robotics_OPCUA (32-Bit FSM & Automation Cell Status)              *)
(* ---------------------------------------------------------------------------------------------------- *)
dw_Telemetry_FSM_Robotics_OPCUA := 16#00000000;
IF (n_FSM_State = 1) THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 0); (* Bit 0: FSM Stage 1 Active: Furnace Robotic Pre-form Unload & Load *)
END_IF;
IF (n_FSM_State = 2) THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 1); (* Bit 1: FSM Stage 2 Active: Vacuum Transfer Chamber Door Seal & Roughing *)
END_IF;
IF (n_FSM_State = 3) THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 2); (* Bit 2: FSM Stage 3 Active: Optical Pyrometer Workpiece Thermal Check *)
END_IF;
IF (n_FSM_State = 4) THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 3); (* Bit 3: FSM Stage 4 Active: Upper Die Induction Inverter Power Ramp *)
END_IF;
IF (n_FSM_State = 5) THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 4); (* Bit 4: FSM Stage 5 Active: Ram Rapid Approach Gravity Drop Stroke *)
END_IF;
IF (n_FSM_State = 6) THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 5); (* Bit 5: FSM Stage 6 Active: Touch-Down Impact Detection & Axial Zero *)
END_IF;
IF (n_FSM_State = 7) THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 6); (* Bit 6: FSM Stage 7 Active: Pre-Forming Hub Upsetting Calibration Squeeze *)
END_IF;
IF (n_FSM_State = 8) THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 7); (* Bit 7: FSM Stage 8 Active: Isothermal Superplastic Extrusion Stroke *)
END_IF;
IF (n_FSM_State = 9) THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 8); (* Bit 8: FSM Stage 9 Active: Final Coining Dwell at 100 MN Axial Tonnage *)
END_IF;
IF (n_FSM_State = 10) THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 9); (* Bit 9: FSM Stage 10 Active: Active Hydraulic Decompression Pressure Ramp *)
END_IF;
IF (n_FSM_State = 11) THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 10); (* Bit 10: FSM Stage 11 Active: Ram Slow Breakaway Die Stripping Retract *)
END_IF;
IF (n_FSM_State = 12) THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 11); (* Bit 11: FSM Stage 12 Active: Vacuum Chamber Argon Equalization Venting *)
END_IF;
IF (n_FSM_State = 13) THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 12); (* Bit 12: FSM Stage 13 Active: Lower Die 4-Pin Hydraulic Part Ejector Lift *)
END_IF;
IF (n_FSM_State = 14) THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 13); (* Bit 13: FSM Stage 14 Active: Robot Extraction & 3D Laser Metrology Scan *)
END_IF;
IF b_FurnaceUnloadRequest THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 14); (* Bit 14: Rotary Hearth Furnace Dispatch Heated Pre-form Strobe *)
END_IF;
IF b_RobotLoadSequenceStartCmd THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 15); (* Bit 15: Robotic Manipulator Load Trajectory Executing *)
END_IF;
IF b_RobotExtractForgedPartCmd THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 16); (* Bit 16: Robotic Manipulator Unload Trajectory Executing *)
END_IF;
IF b_LaserMetrologyScanTriggerCmd THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 17); (* Bit 17: 3D Optical Laser Scanning Sensor Head Active *)
END_IF;
IF b_DiscDimensionQualityPassed THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 18); (* Bit 18: Turbine Disc Final Geometry Approved for Flight Hardware *)
END_IF;
IF (NOT b_DiscDimensionQualityPassed AND b_CycleCompleteStrobe) THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 19); (* Bit 19: Turbine Disc Geometry Out of Specification (Scrap Reject) *)
END_IF;
IF b_TMR_TiltSkew_FaultA THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 20); (* Bit 20: Ram Corner Linear Scale A Hardware Discrepancy Latched *)
END_IF;
IF b_TMR_TiltSkew_FaultB THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 21); (* Bit 21: Ram Corner Linear Scale B Hardware Discrepancy Latched *)
END_IF;
IF b_TMR_TiltSkew_FaultC THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 22); (* Bit 22: Ram Corner Magnetostrictive C Hardware Discrepancy Latched *)
END_IF;
IF (r_CurrentStageElapsed_s > 10.0) THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 23); (* Bit 23: Active Operational Stage Elapsed Time > 10.0 Seconds *)
END_IF;
IF (r_CurrentStageElapsed_s > 30.0) THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 24); (* Bit 24: Active Operational Stage Elapsed Time > 30.0 Seconds *)
END_IF;
IF (r_CurrentStageElapsed_s > 120.0) THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 25); (* Bit 25: Active Operational Stage Elapsed Time > 120.0 Seconds *)
END_IF;
IF b_Alm1_Ack_HH THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 26); (* Bit 26: Tonnage HH Alarm Manually Acknowledged by Cell Operator *)
END_IF;
IF b_Alm2_Ack_HH THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 27); (* Bit 27: Hydraulic Pressure HH Alarm Manually Acknowledged by Operator *)
END_IF;
IF b_Alm3_Ack_HH THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 28); (* Bit 28: Die Temp HH Alarm Manually Acknowledged by Cell Operator *)
END_IF;
IF b_Alm4_Ack_HH THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 29); (* Bit 29: Ram Tilt Skew HH Alarm Manually Acknowledged by Operator *)
END_IF;
IF b_Alm5_Ack_HH THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 30); (* Bit 30: Vacuum Chamber HH Alarm Manually Acknowledged by Operator *)
END_IF;
IF (NOT b_GlobalFaultActive AND b_SystemReady) THEN
    dw_Telemetry_FSM_Robotics_OPCUA := dw_Telemetry_FSM_Robotics_OPCUA OR SHL(DWORD#16#00000001, 31); (* Bit 31: Cell Continuous Automated Unattended Production Permissive *)
END_IF;

(* Clear First Scan Cold-Boot Flag *)
b_FirstScanInit := FALSE;

END_FUNCTION_BLOCK