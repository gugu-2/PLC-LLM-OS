import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = "Write a highly complex control scenario for a Continuous Metal Coil Coating Line in IEC 61131-3 Structured Text. Include chemical pre-treatment spray headers, precision reverse-roll coater applicator gaps, and catenary oven web sag tensioning. It must be a deterministic FUNCTION_BLOCK with complete VAR declarations and physical I/O."
code = """
FUNCTION_BLOCK FB_CoilCoatingLineControl
VAR_INPUT
    bEnableLine : BOOL; // Master enable
    rLineSpeedCmd_mpm : REAL; // Line speed command in meters per minute
    rCoilWidth_mm : REAL; // Width of the metal coil
    rCoilThickness_mm : REAL; // Thickness of the metal coil
    
    // Chemical Pre-Treatment
    rSprayHeader1PressFbk_bar : REAL;
    rSprayHeader2PressFbk_bar : REAL;
    rTankTempFbk_degC : REAL;
    
    // Reverse-Roll Coater
    rApplicatorGapFbk_um : REAL; // Applicator roll gap feedback in micrometers
    rPanLevelFbk_pct : REAL; // Coating pan level feedback
    rViscosityFbk_cP : REAL; // Coating viscosity feedback
    
    // Catenary Oven
    rWebTensionFbk_N : REAL; // Web tension feedback
    rOvenZone1TempFbk_degC : REAL;
    rOvenZone2TempFbk_degC : REAL;
    rOvenZone3TempFbk_degC : REAL;
    rSagDistanceFbk_mm : REAL; // Web sag measured by laser distance sensor
END_VAR

VAR_OUTPUT
    // Chemical Pre-Treatment
    rSprayHeader1PumpSpdRef_pct : REAL;
    rSprayHeader2PumpSpdRef_pct : REAL;
    rHeaterValveCmd_pct : REAL;
    
    // Reverse-Roll Coater
    rApplicatorGapCmd_um : REAL;
    rPanPumpSpdRef_pct : REAL;
    
    // Catenary Oven
    rTensionMotorTrqRef_Nm : REAL;
    rOvenZone1HeaterCmd_pct : REAL;
    rOvenZone2HeaterCmd_pct : REAL;
    rOvenZone3HeaterCmd_pct : REAL;
    
    // Status
    bSystemReady : BOOL;
    bAlarmActive : BOOL;
    iErrorCode : INT;
END_VAR

VAR
    // Internal States and PID Controllers
    rTargetSprayPress_bar : REAL;
    rTargetApplicatorGap_um : REAL;
    rTargetSagDistance_mm : REAL;
    
    rPressError1 : REAL;
    rPressError2 : REAL;
    rGapError : REAL;
    rSagError : REAL;
    rTensionIntegral : REAL := 0.0;
    
    // Constants
    cKp_Press : REAL := 2.5;
    cKp_Gap : REAL := 0.8;
    cKp_Sag : REAL := 1.2;
    cKi_Sag : REAL := 0.05;
    cMaxTensionTrq_Nm : REAL := 500.0;
    cMinSag_mm : REAL := 150.0;
    cMaxSag_mm : REAL := 800.0;
END_VAR

// -----------------------------------------------------------------------------
// Continuous Metal Coil Coating Line Control Algorithm
// -----------------------------------------------------------------------------

IF NOT bEnableLine THEN
    rSprayHeader1PumpSpdRef_pct := 0.0;
    rSprayHeader2PumpSpdRef_pct := 0.0;
    rHeaterValveCmd_pct := 0.0;
    rApplicatorGapCmd_um := 0.0;
    rPanPumpSpdRef_pct := 0.0;
    rTensionMotorTrqRef_Nm := 0.0;
    rOvenZone1HeaterCmd_pct := 0.0;
    rOvenZone2HeaterCmd_pct := 0.0;
    rOvenZone3HeaterCmd_pct := 0.0;
    bSystemReady := FALSE;
    bAlarmActive := FALSE;
    iErrorCode := 0;
    rTensionIntegral := 0.0;
    RETURN;
END_IF;

bSystemReady := TRUE;
bAlarmActive := FALSE;
iErrorCode := 0;

// 1. Chemical Pre-Treatment Control
rTargetSprayPress_bar := 1.5 + (rLineSpeedCmd_mpm * 0.02) + (rCoilWidth_mm * 0.001);

rPressError1 := rTargetSprayPress_bar - rSprayHeader1PressFbk_bar;
rSprayHeader1PumpSpdRef_pct := rSprayHeader1PumpSpdRef_pct + (rPressError1 * cKp_Press);
IF rSprayHeader1PumpSpdRef_pct > 100.0 THEN rSprayHeader1PumpSpdRef_pct := 100.0; END_IF;
IF rSprayHeader1PumpSpdRef_pct < 0.0 THEN rSprayHeader1PumpSpdRef_pct := 0.0; END_IF;

rPressError2 := rTargetSprayPress_bar - rSprayHeader2PressFbk_bar;
rSprayHeader2PumpSpdRef_pct := rSprayHeader2PumpSpdRef_pct + (rPressError2 * cKp_Press);
IF rSprayHeader2PumpSpdRef_pct > 100.0 THEN rSprayHeader2PumpSpdRef_pct := 100.0; END_IF;
IF rSprayHeader2PumpSpdRef_pct < 0.0 THEN rSprayHeader2PumpSpdRef_pct := 0.0; END_IF;

// Tank Temperature Control (Simple Proportional)
rHeaterValveCmd_pct := (65.0 - rTankTempFbk_degC) * 5.0;
IF rHeaterValveCmd_pct > 100.0 THEN rHeaterValveCmd_pct := 100.0; END_IF;
IF rHeaterValveCmd_pct < 0.0 THEN rHeaterValveCmd_pct := 0.0; END_IF;

// 2. Precision Reverse-Roll Coater Applicator Gap Control
rTargetApplicatorGap_um := 25.0 + (rViscosityFbk_cP * 0.1) - (rLineSpeedCmd_mpm * 0.05);
IF rTargetApplicatorGap_um < 10.0 THEN rTargetApplicatorGap_um := 10.0; END_IF;

rGapError := rTargetApplicatorGap_um - rApplicatorGapFbk_um;
rApplicatorGapCmd_um := rApplicatorGapFbk_um + (rGapError * cKp_Gap);

// Pan Level Control
rPanPumpSpdRef_pct := (50.0 - rPanLevelFbk_pct) * 2.0;
IF rPanPumpSpdRef_pct > 100.0 THEN rPanPumpSpdRef_pct := 100.0; END_IF;
IF rPanPumpSpdRef_pct < 0.0 THEN rPanPumpSpdRef_pct := 0.0; END_IF;

// 3. Catenary Oven Web Sag Tensioning
rTargetSagDistance_mm := 400.0 - (rLineSpeedCmd_mpm * 0.5);
IF rTargetSagDistance_mm < cMinSag_mm THEN rTargetSagDistance_mm := cMinSag_mm; END_IF;

rSagError := rSagDistanceFbk_mm - rTargetSagDistance_mm;
rTensionIntegral := rTensionIntegral + (rSagError * cKi_Sag);

// Anti-windup
IF rTensionIntegral > cMaxTensionTrq_Nm THEN rTensionIntegral := cMaxTensionTrq_Nm; END_IF;
IF rTensionIntegral < 0.0 THEN rTensionIntegral := 0.0; END_IF;

rTensionMotorTrqRef_Nm := (rSagError * cKp_Sag) + rTensionIntegral;
IF rTensionMotorTrqRef_Nm > cMaxTensionTrq_Nm THEN rTensionMotorTrqRef_Nm := cMaxTensionTrq_Nm; END_IF;
IF rTensionMotorTrqRef_Nm < 0.0 THEN rTensionMotorTrqRef_Nm := 0.0; END_IF;

// Oven Temperature Control (Simple Profile Tracking)
rOvenZone1HeaterCmd_pct := (150.0 - rOvenZone1TempFbk_degC) * 2.5;
IF rOvenZone1HeaterCmd_pct > 100.0 THEN rOvenZone1HeaterCmd_pct := 100.0; END_IF;
IF rOvenZone1HeaterCmd_pct < 0.0 THEN rOvenZone1HeaterCmd_pct := 0.0; END_IF;

rOvenZone2HeaterCmd_pct := (250.0 - rOvenZone2TempFbk_degC) * 2.5;
IF rOvenZone2HeaterCmd_pct > 100.0 THEN rOvenZone2HeaterCmd_pct := 100.0; END_IF;
IF rOvenZone2HeaterCmd_pct < 0.0 THEN rOvenZone2HeaterCmd_pct := 0.0; END_IF;

rOvenZone3HeaterCmd_pct := (300.0 - rOvenZone3TempFbk_degC) * 2.5;
IF rOvenZone3HeaterCmd_pct > 100.0 THEN rOvenZone3HeaterCmd_pct := 100.0; END_IF;
IF rOvenZone3HeaterCmd_pct < 0.0 THEN rOvenZone3HeaterCmd_pct := 0.0; END_IF;

// Safety Checks
IF rSagDistanceFbk_mm > cMaxSag_mm THEN
    bAlarmActive := TRUE;
    iErrorCode := 1001; // Web sag exceeded critical limit
END_IF;

IF rTankTempFbk_degC > 80.0 THEN
    bAlarmActive := TRUE;
    iErrorCode := 1002; // Over-temperature pre-treatment tank
END_IF;

END_FUNCTION_BLOCK
"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": f"```iec-st\n{code}\n```"}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f)
