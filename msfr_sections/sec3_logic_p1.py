# Section 3: Logic Part 1 (SIL-3 Safety, 2oo3 Voting, Nernstian Thermodynamics)
def get_sec3_logic_p1():
    return """(* ========================================================================================= *)
(* 1.0 EMERGENCY SAFETY SHUTDOWN & SIL-3 HARDWIRED INTERLOCK EVALUATION                      *)
(* ========================================================================================= *)
(* Fast deterministic safety loop: evaluates hardware E-stops, passive freeze plug margin,   *)
(* containment boundary, critical redox boundary runaway, and vessel strain integrity.       *)

bHardwareTripCondition       := FALSE;
bThermalFreezeHazard         := FALSE;
bOverTemperatureHazard       := FALSE;
bOxidizingRunawayHazard      := FALSE;
bReducingPrecipitationHazard := FALSE;
bGasVoidReactivityHazard     := FALSE;
bVesselRuptureStrainHazard   := FALSE;
bContainmentBreachHazard     := FALSE;
bCorrosionRateExceededHazard := FALSE;

(* SIL-3 Dual-channel Active-low Emergency Stop Relay Monitoring *)
IF (NOT bEmergencyStop_CH1) OR (NOT bEmergencyStop_CH2) THEN
    bHardwareTripCondition := TRUE;
    dwCriticalAlarmWord := dwCriticalAlarmWord OR 16#0000_0001; (* Bit 0: Hardwired E-Stop Tripped *)
END_IF;

(* Plant Protection System (PPS) Master Scram Permissive *)
IF NOT bReactorScramPermissive THEN
    bHardwareTripCondition := TRUE;
    dwCriticalAlarmWord := dwCriticalAlarmWord OR 16#0000_0002; (* Bit 1: Reactor PPS Core Trip *)
END_IF;

(* Passive Molten Salt Freeze Plug Safety Thermal Margin *)
IF NOT bSafetyFreezePlugHealthy THEN
    bHardwareTripCondition := TRUE;
    dwCriticalAlarmWord := dwCriticalAlarmWord OR 16#0000_0004; (* Bit 2: Passive Freeze Plug Depleted *)
END_IF;

(* Containment Boundary Isolation Breach Interlock *)
IF NOT bContainmentIsolationClosed THEN
    bContainmentBreachHazard := TRUE;
    dwCriticalAlarmWord := dwCriticalAlarmWord OR 16#0000_0008; (* Bit 3: Containment Barrier Open *)
END_IF;

(* Molten Salt Freeze Crystallization Prevention Interlock (< 565°C) *)
IF (rSaltCoreTemp_A_degC < 565.0) AND (rSaltCoreTemp_B_degC < 565.0) THEN
    bThermalFreezeHazard := TRUE;
    dwCriticalAlarmWord := dwCriticalAlarmWord OR 16#0000_0010; (* Bit 4: Fuel Salt Solidification Hazard *)
END_IF;

(* Core Fuel Salt Overtemperature Thermal Stress Interlock (> 725°C) *)
IF (rSaltCoreTemp_A_degC > 725.0) AND (rSaltCoreTemp_B_degC > 725.0) THEN
    bOverTemperatureHazard := TRUE;
    dwCriticalAlarmWord := dwCriticalAlarmWord OR 16#0000_0020; (* Bit 5: Core Extreme Overtemperature *)
END_IF;

(* Catastrophic Fluorine Potential Runaway (U4+/U3+ Ratio > 220 mol/mol) *)
IF (rCalculatedU4U3Ratio > 220.0) THEN
    bOxidizingRunawayHazard := TRUE;
    dwCriticalAlarmWord := dwCriticalAlarmWord OR 16#0000_0040; (* Bit 6: Severe Oxidizing Runaway *)
END_IF;

(* Severe Over-Reduction Actinide Precipitation Hazard (U4+/U3+ Ratio < 5.0 mol/mol) *)
IF (rCalculatedU4U3Ratio < 5.0) AND (rCalculatedU4U3Ratio > 0.01) THEN
    bReducingPrecipitationHazard := TRUE;
    dwCriticalAlarmWord := dwCriticalAlarmWord OR 16#0000_0080; (* Bit 7: Severe Over-Reduction Hazard *)
END_IF;

(* Core Reactivity Void Fraction Carryunder Interlock (> 0.25% void fraction) *)
IF (rSaltVoidFractionSensor_pct > 0.25) THEN
    bGasVoidReactivityHazard := TRUE;
    dwCriticalAlarmWord := dwCriticalAlarmWord OR 16#0000_0100; (* Bit 8: Gas Void Reactivity Exceeded *)
END_IF;

(* Hastelloy-N Vessel Wall Mechanical Hoop Microstrain Failure (> 1850 microstrain) *)
IF (rVesselWallMicrostrain_CH1 > 1850.0) OR (rVesselWallMicrostrain_CH2 > 1850.0) THEN
    bVesselRuptureStrainHazard := TRUE;
    dwCriticalAlarmWord := dwCriticalAlarmWord OR 16#0000_0200; (* Bit 9: Vessel Wall Hoop Overstrain *)
END_IF;

(* Catastrophic Corrosion Rate Boundary (> 60.0 um/year) *)
IF (rCorrosionRate_um_yr > 60.0) THEN
    bCorrosionRateExceededHazard := TRUE;
    dwCriticalAlarmWord := dwCriticalAlarmWord OR 16#0000_0400; (* Bit 10: Extreme Structural Corrosion *)
END_IF;

(* Overall SIL-3 Master Safety Trip Asserted *)
bEmergencyTripActive := bHardwareTripCondition OR
                        bThermalFreezeHazard OR
                        bOverTemperatureHazard OR
                        bOxidizingRunawayHazard OR
                        bReducingPrecipitationHazard OR
                        bGasVoidReactivityHazard OR
                        bVesselRuptureStrainHazard OR
                        bContainmentBreachHazard OR
                        bCorrosionRateExceededHazard;

(* Safety Actuator Clamp on Emergency Trip *)
IF bEmergencyTripActive THEN
    bBeRodFastEjectionActive := TRUE;
    rBeRodPositionCmd_mm     := 0.0;    (* Retract Beryllium rod instantly from molten salt *)
    bH2SupplyIsolated        := TRUE;
    rH2MassFlowCmd_sccm      := 0.0;    (* Slam shut dual-redundant hydrogen isolation valves *)
    rCycloneThrottleCmd_pct  := 100.0;  (* Dump centrifugal separator to maximize gas release *)
    rHeStrippingFlowCmd_sccm := 100.0;  (* Maintain bare minimum blanket purge, stop bubble stripping *)
    bSystemReady             := FALSE;
    iState                   := 100;    (* Force FSM to State 100: EMERGENCY_SCRAM_DRAIN *)
END_IF;


(* ========================================================================================= *)
(* 2.0 TRIPLE MODULAR REDUNDANCY (2oo3) SENSOR VOTING & SENSOR HEALTH DIAGNOSTICS             *)
(* ========================================================================================= *)
(* High-reliability median selection and deviation monitoring for SIL-3 instrumentation:     *)
(* - Electrochemical Potentiometry (rRedoxPotential_A, B, C)                                 *)
(* - Fuel Salt Bulk Temperature (rSaltCoreTemp_A, B, C)                                      *)
(* - Reduction Sparger Manifold Pressure (rSpargerInletPress_A, B)                           *)
(* - Off-Gas Fission Xe-135 Activity (rOffGasXe135Activity_A, B, C)                         *)

(* --- 2.1 Online Potentiometric Sensor 2oo3 Voting --- *)
rPot_Diff_AB := ABS(rRedoxPotential_A_mV - rRedoxPotential_B_mV);
rPot_Diff_BC := ABS(rRedoxPotential_B_mV - rRedoxPotential_C_mV);
rPot_Diff_CA := ABS(rRedoxPotential_C_mV - rRedoxPotential_A_mV);

(* Sensor plausibility bounds: -650 mV to -150 mV vs Ni/NiF2 reference *)
bPot_Healthy_A := (rRedoxPotential_A_mV >= -650.0) AND (rRedoxPotential_A_mV <= -150.0);
bPot_Healthy_B := (rRedoxPotential_B_mV >= -650.0) AND (rRedoxPotential_B_mV <= -150.0);
bPot_Healthy_C := (rRedoxPotential_C_mV >= -650.0) AND (rRedoxPotential_C_mV <= -150.0);

(* Deviation tolerance: 25.0 mV allowable spread between channels *)
IF rPot_Diff_AB > 25.0 THEN
    IF rPot_Diff_BC <= 25.0 THEN
        bPot_Healthy_A := FALSE; (* Channel A drifting *)
    ELSIF rPot_Diff_CA <= 25.0 THEN
        bPot_Healthy_B := FALSE; (* Channel B drifting *)
    ELSE
        bPot_Healthy_C := FALSE; (* Ambiguous multiple drift *)
    END_IF;
END_IF;

IF rPot_Diff_BC > 25.0 THEN
    IF (rPot_Diff_AB <= 25.0) AND bPot_Healthy_A THEN
        bPot_Healthy_C := FALSE; (* Channel C drifting *)
    END_IF;
END_IF;

(* Calculate healthy channel count *)
iPot_Healthy_Count := 0;
IF bPot_Healthy_A THEN iPot_Healthy_Count := iPot_Healthy_Count + 1; END_IF;
IF bPot_Healthy_B THEN iPot_Healthy_Count := iPot_Healthy_Count + 1; END_IF;
IF bPot_Healthy_C THEN iPot_Healthy_Count := iPot_Healthy_Count + 1; END_IF;

(* Median Selection Logic *)
IF iPot_Healthy_Count = 3 THEN
    (* Perfect 2oo3 Median voting among 3 channels *)
    IF (rRedoxPotential_A_mV >= rRedoxPotential_B_mV AND rRedoxPotential_A_mV <= rRedoxPotential_C_mV) OR
       (rRedoxPotential_A_mV <= rRedoxPotential_B_mV AND rRedoxPotential_A_mV >= rRedoxPotential_C_mV) THEN
        rVotedRedoxPotential_mV := rRedoxPotential_A_mV;
    ELSIF (rRedoxPotential_B_mV >= rRedoxPotential_A_mV AND rRedoxPotential_B_mV <= rRedoxPotential_C_mV) OR
          (rRedoxPotential_B_mV <= rRedoxPotential_A_mV AND rRedoxPotential_B_mV >= rRedoxPotential_C_mV) THEN
        rVotedRedoxPotential_mV := rRedoxPotential_B_mV;
    ELSE
        rVotedRedoxPotential_mV := rRedoxPotential_C_mV;
    END_IF;
ELSIF iPot_Healthy_Count = 2 THEN
    (* Degraded 1oo2 average voting *)
    IF bPot_Healthy_A AND bPot_Healthy_B THEN
        rVotedRedoxPotential_mV := (rRedoxPotential_A_mV + rRedoxPotential_B_mV) * 0.50;
    ELSIF bPot_Healthy_B AND bPot_Healthy_C THEN
        rVotedRedoxPotential_mV := (rRedoxPotential_B_mV + rRedoxPotential_C_mV) * 0.50;
    ELSE
        rVotedRedoxPotential_mV := (rRedoxPotential_A_mV + rRedoxPotential_C_mV) * 0.50;
    END_IF;
    dwWarningWord := dwWarningWord OR 16#0000_0001; (* Warning: Potentiometry 1oo2 degraded *)
ELSIF iPot_Healthy_Count = 1 THEN
    (* Severe degradation: single remaining channel *)
    IF bPot_Healthy_A THEN
        rVotedRedoxPotential_mV := rRedoxPotential_A_mV;
    ELSIF bPot_Healthy_B THEN
        rVotedRedoxPotential_mV := rRedoxPotential_B_mV;
    ELSE
        rVotedRedoxPotential_mV := rRedoxPotential_C_mV;
    END_IF;
    dwWarningWord := dwWarningWord OR 16#0000_0002; (* Warning: Potentiometry 1oo1 critical degraded *)
ELSE
    (* Total sensor failure: Fallback to last filtered value *)
    rVotedRedoxPotential_mV := rFiltRedoxPotential_mV;
    dwCriticalAlarmWord := dwCriticalAlarmWord OR 16#0000_2000; (* Alarm: Loss of all potentiometry *)
END_IF;

(* Exponential Smoothing Noise Rejection Filter on Redox Potential *)
rFiltRedoxPotential_mV := (alpha_RedoxFilter * rVotedRedoxPotential_mV) +
                          ((1.0 - alpha_RedoxFilter) * rFiltRedoxPotential_mV);

(* Dynamic Derivative (Rate-of-Change) Evaluation [mV/s] *)
rRedoxRateOfChange_mV_s := (rFiltRedoxPotential_mV - rHistRedox_1) / tSampleTaskInterval_s;
rHistRedox_3 := rHistRedox_2;
rHistRedox_2 := rHistRedox_1;
rHistRedox_1 := rFiltRedoxPotential_mV;

(* --- 2.2 Fuel Salt Bulk Temperature 2oo3 Voting --- *)
rTemp_Diff_AB := ABS(rSaltCoreTemp_A_degC - rSaltCoreTemp_B_degC);
rTemp_Diff_BC := ABS(rSaltCoreTemp_B_degC - rSaltCoreTemp_C_degC);
rTemp_Diff_CA := ABS(rSaltCoreTemp_C_degC - rSaltCoreTemp_A_degC);

bTemp_Healthy_A := (rSaltCoreTemp_A_degC >= 550.0) AND (rSaltCoreTemp_A_degC <= 750.0);
bTemp_Healthy_B := (rSaltCoreTemp_B_degC >= 550.0) AND (rSaltCoreTemp_B_degC <= 750.0);
bTemp_Healthy_C := (rSaltCoreTemp_C_degC >= 550.0) AND (rSaltCoreTemp_C_degC <= 750.0);

IF rTemp_Diff_AB > 20.0 THEN
    IF rTemp_Diff_BC <= 20.0 THEN bTemp_Healthy_A := FALSE;
    ELSIF rTemp_Diff_CA <= 20.0 THEN bTemp_Healthy_B := FALSE;
    ELSE bTemp_Healthy_C := FALSE;
    END_IF;
END_IF;

iTemp_Healthy_Count := 0;
IF bTemp_Healthy_A THEN iTemp_Healthy_Count := iTemp_Healthy_Count + 1; END_IF;
IF bTemp_Healthy_B THEN iTemp_Healthy_Count := iTemp_Healthy_Count + 1; END_IF;
IF bTemp_Healthy_C THEN iTemp_Healthy_Count := iTemp_Healthy_Count + 1; END_IF;

IF iTemp_Healthy_Count = 3 THEN
    IF (rSaltCoreTemp_A_degC >= rSaltCoreTemp_B_degC AND rSaltCoreTemp_A_degC <= rSaltCoreTemp_C_degC) OR
       (rSaltCoreTemp_A_degC <= rSaltCoreTemp_B_degC AND rSaltCoreTemp_A_degC >= rSaltCoreTemp_C_degC) THEN
        rVotedSaltCoreTemp_degC := rSaltCoreTemp_A_degC;
    ELSIF (rSaltCoreTemp_B_degC >= rSaltCoreTemp_A_degC AND rSaltCoreTemp_B_degC <= rSaltCoreTemp_C_degC) OR
          (rSaltCoreTemp_B_degC <= rSaltCoreTemp_A_degC AND rSaltCoreTemp_B_degC >= rSaltCoreTemp_C_degC) THEN
        rVotedSaltCoreTemp_degC := rSaltCoreTemp_B_degC;
    ELSE
        rVotedSaltCoreTemp_degC := rSaltCoreTemp_C_degC;
    END_IF;
ELSIF iTemp_Healthy_Count = 2 THEN
    IF bTemp_Healthy_A AND bTemp_Healthy_B THEN
        rVotedSaltCoreTemp_degC := (rSaltCoreTemp_A_degC + rSaltCoreTemp_B_degC) * 0.50;
    ELSIF bTemp_Healthy_B AND bTemp_Healthy_C THEN
        rVotedSaltCoreTemp_degC := (rSaltCoreTemp_B_degC + rSaltCoreTemp_C_degC) * 0.50;
    ELSE
        rVotedSaltCoreTemp_degC := (rSaltCoreTemp_A_degC + rSaltCoreTemp_C_degC) * 0.50;
    END_IF;
    dwWarningWord := dwWarningWord OR 16#0000_0004; (* Warning: Temp 1oo2 degraded *)
ELSE
    rVotedSaltCoreTemp_degC := rFiltSaltCoreTemp_degC;
END_IF;

rFiltSaltCoreTemp_degC := (alpha_TempFilter * rVotedSaltCoreTemp_degC) +
                          ((1.0 - alpha_TempFilter) * rFiltSaltCoreTemp_degC);

(* --- 2.3 Off-Gas Fission Gas Xe-135 Activity 2oo3 Voting --- *)
rXe_Diff_AB := ABS(rOffGasXe135Activity_A_Bq_m3 - rOffGasXe135Activity_B_Bq_m3);
rXe_Diff_BC := ABS(rOffGasXe135Activity_B_Bq_m3 - rOffGasXe135Activity_C_Bq_m3);
rXe_Diff_CA := ABS(rOffGasXe135Activity_C_Bq_m3 - rOffGasXe135Activity_A_Bq_m3);

bXe_Healthy_A := (rOffGasXe135Activity_A_Bq_m3 >= 0.0);
bXe_Healthy_B := (rOffGasXe135Activity_B_Bq_m3 >= 0.0);
bXe_Healthy_C := (rOffGasXe135Activity_C_Bq_m3 >= 0.0);

iXe_Healthy_Count := 0;
IF bXe_Healthy_A THEN iXe_Healthy_Count := iXe_Healthy_Count + 1; END_IF;
IF bXe_Healthy_B THEN iXe_Healthy_Count := iXe_Healthy_Count + 1; END_IF;
IF bXe_Healthy_C THEN iXe_Healthy_Count := iXe_Healthy_Count + 1; END_IF;

IF iXe_Healthy_Count = 3 THEN
    IF (rOffGasXe135Activity_A_Bq_m3 >= rOffGasXe135Activity_B_Bq_m3 AND rOffGasXe135Activity_A_Bq_m3 <= rOffGasXe135Activity_C_Bq_m3) OR
       (rOffGasXe135Activity_A_Bq_m3 <= rOffGasXe135Activity_B_Bq_m3 AND rOffGasXe135Activity_A_Bq_m3 >= rOffGasXe135Activity_C_Bq_m3) THEN
        rVotedXe135Activity_Bq_m3 := rOffGasXe135Activity_A_Bq_m3;
    ELSIF (rOffGasXe135Activity_B_Bq_m3 >= rOffGasXe135Activity_A_Bq_m3 AND rOffGasXe135Activity_B_Bq_m3 <= rOffGasXe135Activity_C_Bq_m3) OR
          (rOffGasXe135Activity_B_Bq_m3 <= rOffGasXe135Activity_A_Bq_m3 AND rOffGasXe135Activity_B_Bq_m3 >= rOffGasXe135Activity_C_Bq_m3) THEN
        rVotedXe135Activity_Bq_m3 := rOffGasXe135Activity_B_Bq_m3;
    ELSE
        rVotedXe135Activity_Bq_m3 := rOffGasXe135Activity_C_Bq_m3;
    END_IF;
ELSIF iXe_Healthy_Count >= 1 THEN
    IF bXe_Healthy_A THEN rVotedXe135Activity_Bq_m3 := rOffGasXe135Activity_A_Bq_m3;
    ELSIF bXe_Healthy_B THEN rVotedXe135Activity_Bq_m3 := rOffGasXe135Activity_B_Bq_m3;
    ELSE rVotedXe135Activity_Bq_m3 := rOffGasXe135Activity_C_Bq_m3;
    END_IF;
ELSE
    rVotedXe135Activity_Bq_m3 := 0.0;
END_IF;

rFiltOffGasXe_Bq_m3 := (alpha_XeFilter * rVotedXe135Activity_Bq_m3) +
                       ((1.0 - alpha_XeFilter) * rFiltOffGasXe_Bq_m3);


(* ========================================================================================= *)
(* 3.0 THERMODYNAMIC EQUILIBRIUM & NERNSTIAN ELECTROCHEMICAL REDOX REGULATION                *)
(* ========================================================================================= *)
(* Inverts the voted electrochemical cell potential [mV] using temperature-corrected         *)
(* Nernst-Einstein thermodynamics to obtain the online molar ratio [U4+]/[U3+]:              *)
(*   E_cell(T) = E0(T) + (R * T / (n * F)) * ln( (gamma_UF4 / gamma_UF3) * ([U4+]/[U3+]) )   *)

(* Convert voted temperature to thermodynamic Kelvin *)
rT_Kelvin := rFiltSaltCoreTemp_degC + STANDARD_TEMP_K;
IF rT_Kelvin < 800.0 THEN rT_Kelvin := 800.0; END_IF; (* Safeguard against zero division *)

(* Temperature-dependent standard reduction potential E0(T) [V] *)
rE0_T_Volt := E0_REF_POTENTIAL_V + (D_E0_DT_COEFF * (rT_Kelvin - NOMINAL_CORE_TEMP_K));

(* Thermodynamic Nernstian Slope factor: (R_u * T) / (n * F) with n = 1 *)
rNernstSlope_V := (R_GAS_CONST * rT_Kelvin) / FARADAY_CONST;

(* Potential offset in Volts: Convert filtered mV to Volts *)
rDelta_E_Volt := (rFiltRedoxPotential_mV * 0.0010) - rE0_T_Volt;

(* Natural logarithm of molar concentration ratio *)
rLnRatio := (rDelta_E_Volt / rNernstSlope_V) - LN(ACTIVITY_COEFF_RATIO);

(* Anti-saturation bounds on exponent: prevent floating point overflow *)
IF rLnRatio > 7.50 THEN rLnRatio := 7.50; END_IF;       (* Equivalent to ratio approx 1800 *)
IF rLnRatio < 0.50 THEN rLnRatio := 0.50; END_IF;       (* Equivalent to ratio approx 1.65 *)

(* Online calculated U4+/U3+ molar ratio *)
rCalculatedU4U3Ratio := EXP(rLnRatio);

(* Control deviation from setpoint in logarithmic space *)
IF rRedoxRatioTarget_mol_mol < 10.0 THEN rRedoxRatioTarget_mol_mol := 10.0; END_IF;
IF rRedoxRatioTarget_mol_mol > 180.0 THEN rRedoxRatioTarget_mol_mol := 180.0; END_IF;

rRedoxError := LN(rCalculatedU4U3Ratio) - LN(rRedoxRatioTarget_mol_mol);

(* Setpoint Window Diagnostic Supervision *)
IF rCalculatedU4U3Ratio > 140.0 THEN
    dwWarningWord := dwWarningWord OR 16#0000_0010; (* Warning: Fuel salt oxidizing high *)
ELSIF rCalculatedU4U3Ratio < 35.0 THEN
    dwWarningWord := dwWarningWord OR 16#0000_0020; (* Warning: Fuel salt reducing low *)
END_IF;
"""

if __name__ == "__main__":
    s = get_sec3_logic_p1()
    print("Section 3 Length:", len(s))
