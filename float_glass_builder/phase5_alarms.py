# phase5_alarms.py for FB_Glass_FloatLine_TinBath_AnnealingLehr_ThicknessCooling

def generate_phase5():
    return """(*
 * =========================================================================================================
 * PHASE 5: ISA-18.2 MULTI-TIERED ALARM ENGINE & BIT-PACKED DIAGNOSTIC STATUS WORDS
 * Multi-tiered alarm matrix with hysteresis deadbands, latching registers, operator reset,
 * and 32-bit bit-packed DWORD telemetry for SCADA / DCS supervisory communication.
 * =========================================================================================================
 *)

(* ---------------------------------------------------------------------------------------------------------
 * 1. ISA-18.2 ALARM MATRIX WITH HYSTERESIS CLEARANCE DEADBANDS
 * --------------------------------------------------------------------------------------------------------- *)
(* --- Laser Optical Thickness Alarms (Deviations in mm vs Recipe Target) --- *)
(* High-High Thickness Deviation (+250 um) *)
IF (rVotedThickness_mm - rRecipeTargetThickness) >= rThickAlarm_HH_Limit THEN
    bAlarm_Thick_HH := TRUE;
ELSIF (rVotedThickness_mm - rRecipeTargetThickness) <= (rThickAlarm_HH_Limit - rThickAlarm_Deadband) THEN
    bAlarm_Thick_HH := FALSE;
END_IF;

(* High Thickness Deviation (+100 um) *)
IF (rVotedThickness_mm - rRecipeTargetThickness) >= rThickAlarm_H_Limit THEN
    bAlarm_Thick_H := TRUE;
ELSIF (rVotedThickness_mm - rRecipeTargetThickness) <= (rThickAlarm_H_Limit - rThickAlarm_Deadband) THEN
    bAlarm_Thick_H := FALSE;
END_IF;

(* Low Thickness Deviation (-100 um) *)
IF (rVotedThickness_mm - rRecipeTargetThickness) <= rThickAlarm_L_Limit THEN
    bAlarm_Thick_L := TRUE;
ELSIF (rVotedThickness_mm - rRecipeTargetThickness) >= (rThickAlarm_L_Limit + rThickAlarm_Deadband) THEN
    bAlarm_Thick_L := FALSE;
END_IF;

(* Low-Low Thickness Deviation (-250 um) *)
IF (rVotedThickness_mm - rRecipeTargetThickness) <= rThickAlarm_LL_Limit THEN
    bAlarm_Thick_LL := TRUE;
ELSIF (rVotedThickness_mm - rRecipeTargetThickness) >= (rThickAlarm_LL_Limit + rThickAlarm_Deadband) THEN
    bAlarm_Thick_LL := FALSE;
END_IF;

(* --- Tin Bath Roof Infrared Pyrometer Alarms (deg C) --- *)
(* High-High Pyrometer (1110 deg C - Silica Arch Thermal Refractory Danger) *)
IF rVotedPyrometer_degC >= rPyroAlarm_HH_Limit THEN
    bAlarm_Pyro_HH := TRUE;
ELSIF rVotedPyrometer_degC <= (rPyroAlarm_HH_Limit - rPyroAlarm_Deadband) THEN
    bAlarm_Pyro_HH := FALSE;
END_IF;

(* High Pyrometer Warning (1075 deg C) *)
IF rVotedPyrometer_degC >= rPyroAlarm_H_Limit THEN
    bAlarm_Pyro_H := TRUE;
ELSIF rVotedPyrometer_degC <= (rPyroAlarm_H_Limit - rPyroAlarm_Deadband) THEN
    bAlarm_Pyro_H := FALSE;
END_IF;

(* Low Pyrometer Warning (1020 deg C - Viscous Retardation) *)
IF rVotedPyrometer_degC <= rPyroAlarm_L_Limit THEN
    bAlarm_Pyro_L := TRUE;
ELSIF rVotedPyrometer_degC >= (rPyroAlarm_L_Limit + rPyroAlarm_Deadband) THEN
    bAlarm_Pyro_L := FALSE;
END_IF;

(* Low-Low Pyrometer (990 deg C - Catastrophic Molten Tin Freezing Risk) *)
IF rVotedPyrometer_degC <= rPyroAlarm_LL_Limit THEN
    bAlarm_Pyro_LL := TRUE;
ELSIF rVotedPyrometer_degC >= (rPyroAlarm_LL_Limit + rPyroAlarm_Deadband) THEN
    bAlarm_Pyro_LL := FALSE;
END_IF;

(* --- Protective Atmosphere Hermetic Pressure Alarms (mbar) --- *)
(* High-High Pressure (1.25 mbar - Casing Mechanical Seal Strain) *)
IF rVotedBathPress_mbar >= rPressAlarm_HH_Limit THEN
    bAlarm_Press_HH := TRUE;
ELSIF rVotedBathPress_mbar <= (rPressAlarm_HH_Limit - rPressAlarm_Deadband) THEN
    bAlarm_Press_HH := FALSE;
END_IF;

(* High Pressure Warning (0.90 mbar) *)
IF rVotedBathPress_mbar >= rPressAlarm_H_Limit THEN
    bAlarm_Press_H := TRUE;
ELSIF rVotedBathPress_mbar <= (rPressAlarm_H_Limit - rPressAlarm_Deadband) THEN
    bAlarm_Press_H := FALSE;
END_IF;

(* Low Pressure Warning (0.20 mbar - Ingress Risk) *)
IF rVotedBathPress_mbar <= rPressAlarm_L_Limit THEN
    bAlarm_Press_L := TRUE;
ELSIF rVotedBathPress_mbar >= (rPressAlarm_L_Limit + rPressAlarm_Deadband) THEN
    bAlarm_Press_L := FALSE;
END_IF;

(* Low-Low Pressure (0.06 mbar - Severe Atmospheric Air Ingress & SnO Formation) *)
IF rVotedBathPress_mbar <= rPressAlarm_LL_Limit THEN
    bAlarm_Press_LL := TRUE;
ELSIF rVotedBathPress_mbar >= (rPressAlarm_LL_Limit + rPressAlarm_Deadband) THEN
    bAlarm_Press_LL := FALSE;
END_IF;

(* --- Lehr Residual Stress Birefringence Alarms (nm/cm) --- *)
(* High-High Residual Stress (45.0 nm/cm - Spontaneous Cross-Belt Break Hazard) *)
IF rVotedLehrStress_nm_cm >= rStressAlarm_HH_Limit THEN
    bAlarm_Stress_HH := TRUE;
ELSIF rVotedLehrStress_nm_cm <= (rStressAlarm_HH_Limit - rStressAlarm_Deadband) THEN
    bAlarm_Stress_HH := FALSE;
END_IF;

(* High Residual Stress Warning (30.0 nm/cm) *)
IF rVotedLehrStress_nm_cm >= rStressAlarm_H_Limit THEN
    bAlarm_Stress_H := TRUE;
ELSIF rVotedLehrStress_nm_cm <= (rStressAlarm_H_Limit - rStressAlarm_Deadband) THEN
    bAlarm_Stress_H := FALSE;
END_IF;

(* --- Gas Chemistry Alarms --- *)
(* Low-Low Hydrogen Scavenger (< 2.5% vol H2) *)
IF rH2_Concentration_Feedback <= rH2_Alarm_LL_Limit THEN
    bAlarm_H2_LowLow := TRUE;
ELSIF rH2_Concentration_Feedback >= (rH2_Alarm_LL_Limit + 0.30) THEN
    bAlarm_H2_LowLow := FALSE;
END_IF;

(* Low Hydrogen Warning (< 3.8% vol H2) *)
IF rH2_Concentration_Feedback <= rH2_Alarm_L_Limit THEN
    bAlarm_H2_Low := TRUE;
ELSIF rH2_Concentration_Feedback >= (rH2_Alarm_L_Limit + 0.30) THEN
    bAlarm_H2_Low := FALSE;
END_IF;

(* High-High Hydrogen Flammability Safety Ceiling (> 8.5% vol H2) *)
IF rH2_Concentration_Feedback >= rH2_Alarm_HH_Limit THEN
    bAlarm_H2_HighHigh := TRUE;
ELSIF rH2_Concentration_Feedback <= (rH2_Alarm_HH_Limit - 0.50) THEN
    bAlarm_H2_HighHigh := FALSE;
END_IF;

(* High-High Oxygen Ingress (> 15 ppm O2) *)
IF rO2_Ppm_Feedback >= rO2_Alarm_HH_Limit THEN
    bAlarm_O2_HighHigh := TRUE;
ELSIF rO2_Ppm_Feedback <= (rO2_Alarm_HH_Limit - 3.0) THEN
    bAlarm_O2_HighHigh := FALSE;
END_IF;

(* --- Hydrodynamic Ribbon Waisting Detection --- *)
IF (rRecipeTargetWidth - rRibbonWidthFeedback) >= rWaistingDefectThreshold_mm THEN
    bAlarm_RibbonWaisting := TRUE;
END_IF;

(* Operator Pushbutton Acknowledgment and Reset *)
IF bAlarmResetPushbutton THEN
    bAlarm_Thick_HH             := FALSE;
    bAlarm_Thick_LL             := FALSE;
    bAlarm_Pyro_HH              := FALSE;
    bAlarm_Pyro_LL              := FALSE;
    bAlarm_Press_HH             := FALSE;
    bAlarm_Press_LL             := FALSE;
    bAlarm_Stress_HH            := FALSE;
    bAlarm_H2_LowLow            := FALSE;
    bAlarm_H2_HighHigh          := FALSE;
    bAlarm_O2_HighHigh          := FALSE;
    bAlarm_TMR_Trip_AllFailed   := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------
 * 2. 32-BIT BIT-PACKED DIAGNOSTIC & ALARM DWORD TELEMETRY
 * --------------------------------------------------------------------------------------------------------- *)
(* --- DWORD 1: ISA-18.2 Process Deviation Alarms (dwAlarmWord1_Process) --- *)
dwAlarmWord1_Process := 16#00000000;
IF bAlarm_Thick_HH             THEN dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#00000001; END_IF;
IF bAlarm_Thick_H              THEN dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#00000002; END_IF;
IF bAlarm_Thick_L              THEN dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#00000004; END_IF;
IF bAlarm_Thick_LL             THEN dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#00000008; END_IF;
IF bAlarm_Pyro_HH              THEN dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#00000010; END_IF;
IF bAlarm_Pyro_H               THEN dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#00000020; END_IF;
IF bAlarm_Pyro_L               THEN dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#00000040; END_IF;
IF bAlarm_Pyro_LL              THEN dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#00000080; END_IF;
IF bAlarm_Press_HH             THEN dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#00000100; END_IF;
IF bAlarm_Press_H              THEN dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#00000200; END_IF;
IF bAlarm_Press_L              THEN dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#00000400; END_IF;
IF bAlarm_Press_LL             THEN dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#00000800; END_IF;
IF bAlarm_Stress_HH            THEN dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#00001000; END_IF;
IF bAlarm_Stress_H             THEN dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#00002000; END_IF;
IF bAlarm_H2_LowLow            THEN dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#00004000; END_IF;
IF bAlarm_H2_Low               THEN dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#00008000; END_IF;
IF bAlarm_H2_HighHigh          THEN dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#00010000; END_IF;
IF bAlarm_O2_HighHigh          THEN dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#00020000; END_IF;
IF bAlarm_RibbonWaisting       THEN dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#00040000; END_IF;

(* --- DWORD 2: Equipment Drives, Top-Rollers & Heaters (dwAlarmWord2_Equipment) --- *)
dwAlarmWord2_Equipment := 16#00000000;
FOR idxRoller := 1 TO 16 DO
    IF arrTopRollerSlipTrip[idxRoller] THEN
        dwAlarmWord2_Equipment := dwAlarmWord2_Equipment OR SHL(DWORD#16#00000001, idxRoller - 1);
    END_IF;
END_FOR;
IF bAlarm_TopRollerCoolingFail THEN dwAlarmWord2_Equipment := dwAlarmWord2_Equipment OR 16#00010000; END_IF;
IF bAlarm_CulletTrapdoorOpen   THEN dwAlarmWord2_Equipment := dwAlarmWord2_Equipment OR 16#00020000; END_IF;

(* --- DWORD 3: Safety Interlocks & TMR Sensor Redundancy Status (dwAlarmWord3_SafetyTMR) --- *)
dwAlarmWord3_SafetyTMR := 16#00000000;
IF NOT bSafetyCircuitHealthy   THEN dwAlarmWord3_SafetyTMR := dwAlarmWord3_SafetyTMR OR 16#00000001; END_IF;
IF bEmergencyStopActive        THEN dwAlarmWord3_SafetyTMR := dwAlarmWord3_SafetyTMR OR 16#00000002; END_IF;
IF bAlarm_TMR_Degraded_Thick   THEN dwAlarmWord3_SafetyTMR := dwAlarmWord3_SafetyTMR OR 16#00000004; END_IF;
IF nThick_VotingMode = 0       THEN dwAlarmWord3_SafetyTMR := dwAlarmWord3_SafetyTMR OR 16#00000008; END_IF;
IF bAlarm_TMR_Degraded_Pyro    THEN dwAlarmWord3_SafetyTMR := dwAlarmWord3_SafetyTMR OR 16#00000010; END_IF;
IF nPyro_VotingMode = 0        THEN dwAlarmWord3_SafetyTMR := dwAlarmWord3_SafetyTMR OR 16#00000020; END_IF;
IF bAlarm_TMR_Degraded_Press   THEN dwAlarmWord3_SafetyTMR := dwAlarmWord3_SafetyTMR OR 16#00000040; END_IF;
IF nPress_VotingMode = 0       THEN dwAlarmWord3_SafetyTMR := dwAlarmWord3_SafetyTMR OR 16#00000080; END_IF;
IF bAlarm_TMR_Degraded_Stress  THEN dwAlarmWord3_SafetyTMR := dwAlarmWord3_SafetyTMR OR 16#00000100; END_IF;
IF nStress_VotingMode = 0      THEN dwAlarmWord3_SafetyTMR := dwAlarmWord3_SafetyTMR OR 16#00000200; END_IF;
IF bSystemDegraded             THEN dwAlarmWord3_SafetyTMR := dwAlarmWord3_SafetyTMR OR 16#00000400; END_IF;
IF bSystemFaultTrip            THEN dwAlarmWord3_SafetyTMR := dwAlarmWord3_SafetyTMR OR 16#00000800; END_IF;

(* --- DWORD 4: Overall System Operational Status (dwStatusWord_System) --- *)
dwStatusWord_System := 16#00000000;
IF bMasterEnable               THEN dwStatusWord_System := dwStatusWord_System OR 16#00000001; END_IF;
IF bAutoModeSelected           THEN dwStatusWord_System := dwStatusWord_System OR 16#00000002; END_IF;
IF bSystemReady                THEN dwStatusWord_System := dwStatusWord_System OR 16#00000004; END_IF;
IF bSystemActive               THEN dwStatusWord_System := dwStatusWord_System OR 16#00000008; END_IF;
IF bSystemDegraded             THEN dwStatusWord_System := dwStatusWord_System OR 16#00000010; END_IF;
IF bSystemFaultTrip            THEN dwStatusWord_System := dwStatusWord_System OR 16#00000020; END_IF;
(* Embed 4-bit operational state code into bits 8..11 *)
dwStatusWord_System := dwStatusWord_System OR SHL(INT_TO_DWORD(nOperationalState AND 16#0F), 8);
IF bCulletDumpGateOpen         THEN dwStatusWord_System := dwStatusWord_System OR 16#00001000; END_IF;
IF nOperationalState = cSTATE_DYNAMIC_PRODUCT_THICKNESS_RECIPE_CHANGE THEN
    dwStatusWord_System := dwStatusWord_System OR 16#00002000;
END_IF;
IF nOperationalState = cSTATE_NOMINAL_CONTINUOUS_FLOAT_PRODUCTION_RUN THEN
    dwStatusWord_System := dwStatusWord_System OR 16#00004000;
END_IF;

END_FUNCTION_BLOCK
"""

if __name__ == "__main__":
    s = generate_phase5()
    print(f"Phase 5 length: {len(s)} chars")
