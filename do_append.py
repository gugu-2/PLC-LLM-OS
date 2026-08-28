import subprocess
import json

prompt = """Write an IEC 61131-3 Structured Text FUNCTION_BLOCK for an Extreme Ultraviolet Lithography (EUVL) dose and focus control system in a semiconductor wafer fab. It must handle multi-axis piezo stage positioning, laser-produced plasma (LPP) droplet generator synchronization, CO2 laser pulse timing, dose integration across multiple exposure fields, and real-time reticle thermal expansion compensation. Include complex state machines, error handling for dose deviation and focus loss, and extensive variable declarations with physical I/O mappings."""

code = """```iec-st
FUNCTION_BLOCK FB_EUVL_DoseFocusControl
TITLE = 'Extreme Ultraviolet Lithography Dose and Focus Control'
VERSION : '2.1'
AUTHOR : 'Lumina AI Cloud Swarm'

VAR_INPUT
    bEnableSystem         : BOOL;  // Enable EUVL control system
    bStartExposure        : BOOL;  // Trigger exposure sequence
    bEmergencyStop        : BOOL;  // Hardware E-Stop
    
    // Wafer Stage Telemetry
    rStageX_nm            : REAL;  // X position in nanometers
    rStageY_nm            : REAL;  // Y position in nanometers
    rStageZ_nm            : REAL;  // Z position (focus) in nanometers
    rStageRx_urad         : REAL;  // Pitch in microradians
    rStageRy_urad         : REAL;  // Roll in microradians
    rStageRz_urad         : REAL;  // Yaw in microradians
    
    // Laser Produced Plasma (LPP) Source
    rTinDropletFreq_Hz    : REAL;  // Tin droplet generator frequency
    bDropletDetected      : BOOL;  // Droplet passing trigger zone
    
    // EUV Sensors
    rPlasmaEUVYield_mJ    : REAL;  // Energy per pulse measured at intermediate focus
    rReticleTemp_C        : REAL;  // Reticle temperature for thermal expansion compensation
    
    // Recipe Parameters
    rTargetDose_mJ_cm2    : REAL;  // Target dose for current layer
    rExposureDuration_ms  : REAL;  // Target exposure time per field
    rTargetFocus_nm       : REAL;  // Target Z position
    
    // Tolerances
    rDoseErrorLimit_pct   : REAL := 1.5; // Max allowable dose error percentage
    rFocusErrorLimit_nm   : REAL := 5.0; // Max allowable focus error in nm
END_VAR

VAR_OUTPUT
    bSystemReady          : BOOL;
    bExposing             : BOOL;
    bExposureComplete     : BOOL;
    bFaultActive          : BOOL;
    iFaultCode            : INT;
    
    // CO2 Laser Drive
    bLaserFireCommand     : BOOL;  // Fire main CO2 laser pulse
    rLaserPower_pct       : REAL;  // Output power level (0-100%)
    
    // Stage Corrections (Piezo Drive)
    rStageZ_Correction_nm : REAL;
    
    // Dose Metrics
    rAccumulatedDose_mJ   : REAL;
    rDoseError_pct        : REAL;
END_VAR

VAR
    // State Machine
    eState : INT := 0; // 0:INIT, 1:IDLE, 2:STAGE_SETTLE, 3:DROPLET_SYNC, 4:EXPOSURE_ACTIVE, 5:FAULT
    ePrevState : INT;
    
    // Internal calculations
    rThermalExpansionCoef : REAL := 0.000023; // ppm/C for ULE glass
    rBaseReticleTemp_C    : REAL := 22.0;
    rZShiftThermal_nm     : REAL;
    
    rCurrentFocusError_nm : REAL;
    rMovingAvgYield_mJ    : REAL;
    rYieldBuffer          : ARRAY[0..9] OF REAL;
    iBufferIndex          : INT := 0;
    
    // Timers
    tExposureTimer        : TON;
    tDropletSyncTimeout   : TON;
    tStageSettleTimer     : TON;
    
    // Laser sync logic
    rCalculatedDelay_us   : REAL;
    bLaserArmed           : BOOL;
END_VAR

// ==============================================================================
// Implementation
// ==============================================================================

// Handle Emergency Stop
IF bEmergencyStop THEN
    eState := 5; // FAULT
    iFaultCode := 9999; // E-STOP
    bExposing := FALSE;
    bLaserFireCommand := FALSE;
    bLaserArmed := FALSE;
END_IF;

// Thermal Expansion Compensation for Reticle (Focus Shift)
// Shift focus based on reticle heating during exposure
rZShiftThermal_nm := (rReticleTemp_C - rBaseReticleTemp_C) * rThermalExpansionCoef * 1000.0;

// Focus Error Calculation
rCurrentFocusError_nm := (rTargetFocus_nm + rZShiftThermal_nm) - rStageZ_nm;

// State Machine
CASE eState OF

    0: // INIT
        bSystemReady := FALSE;
        bExposing := FALSE;
        bExposureComplete := FALSE;
        bFaultActive := FALSE;
        iFaultCode := 0;
        rAccumulatedDose_mJ := 0.0;
        rDoseError_pct := 0.0;
        rStageZ_Correction_nm := 0.0;
        rLaserPower_pct := 0.0;
        
        IF bEnableSystem THEN
            eState := 1; // IDLE
        END_IF;

    1: // IDLE
        bSystemReady := TRUE;
        bExposureComplete := FALSE;
        
        IF bStartExposure AND NOT bEmergencyStop THEN
            bSystemReady := FALSE;
            rAccumulatedDose_mJ := 0.0;
            eState := 2; // STAGE_SETTLE
        END_IF;
        
        IF NOT bEnableSystem THEN
            eState := 0; // INIT
        END_IF;

    2: // STAGE_SETTLE
        // Calculate required Z correction
        rStageZ_Correction_nm := rCurrentFocusError_nm;
        
        // Timer to wait for piezo stage to settle
        tStageSettleTimer(IN := TRUE, PT := T#50MS);
        
        IF tStageSettleTimer.Q THEN
            tStageSettleTimer(IN := FALSE); // Reset
            IF ABS(rCurrentFocusError_nm) <= rFocusErrorLimit_nm THEN
                eState := 3; // DROPLET_SYNC
            ELSE
                eState := 5; // FAULT
                iFaultCode := 1001; // Focus settle timeout/error
            END_IF;
        END_IF;

    3: // DROPLET_SYNC
        // Sync CO2 laser firing with tin droplet generator
        tDropletSyncTimeout(IN := TRUE, PT := T#10MS);
        
        IF bDropletDetected THEN
            tDropletSyncTimeout(IN := FALSE);
            bLaserArmed := TRUE;
            eState := 4; // EXPOSURE_ACTIVE
        ELSIF tDropletSyncTimeout.Q THEN
            tDropletSyncTimeout(IN := FALSE);
            eState := 5; // FAULT
            iFaultCode := 2001; // Droplet sync timeout
        END_IF;

    4: // EXPOSURE_ACTIVE
        bExposing := TRUE;
        
        // Active focus tracking
        rStageZ_Correction_nm := rCurrentFocusError_nm;
        IF ABS(rCurrentFocusError_nm) > (rFocusErrorLimit_nm * 1.5) THEN
            eState := 5; // FAULT
            iFaultCode := 1002; // Dynamic focus loss
        END_IF;
        
        // Laser firing logic
        IF bLaserArmed AND bDropletDetected THEN
            bLaserFireCommand := TRUE; // Pulse laser
            
            // Integrate Dose
            rAccumulatedDose_mJ := rAccumulatedDose_mJ + rPlasmaEUVYield_mJ;
            
            // Moving average for laser power modulation
            rYieldBuffer[iBufferIndex] := rPlasmaEUVYield_mJ;
            iBufferIndex := (iBufferIndex + 1) MOD 10;
            
            // Check dose trajectory
            rDoseError_pct := ((rTargetDose_mJ_cm2 - rAccumulatedDose_mJ) / rTargetDose_mJ_cm2) * 100.0;
            
            // Modulate laser power for next pulse based on yield
            IF rPlasmaEUVYield_mJ < 1.0 THEN // Low yield threshold
                 rLaserPower_pct := rLaserPower_pct + 5.0;
                 IF rLaserPower_pct > 100.0 THEN rLaserPower_pct := 100.0; END_IF;
            ELSE
                 rLaserPower_pct := rLaserPower_pct - 1.0;
                 IF rLaserPower_pct < 10.0 THEN rLaserPower_pct := 10.0; END_IF;
            END_IF;
            
            bLaserArmed := FALSE; // Wait for next droplet
        ELSE
            bLaserFireCommand := FALSE;
        END_IF;
        
        // Check if exposure is complete
        IF rAccumulatedDose_mJ >= rTargetDose_mJ_cm2 THEN
            bExposing := FALSE;
            bLaserFireCommand := FALSE;
            bExposureComplete := TRUE;
            eState := 1; // IDLE
        END_IF;
        
        // Safety timeout
        // Wait, TYPE CONVERSION
        tExposureTimer(IN := bExposing, PT := T#2S);
        IF tExposureTimer.Q THEN
            tExposureTimer(IN := FALSE);
            eState := 5; // FAULT
            iFaultCode := 3001; // Exposure time overrun
        END_IF;

    5: // FAULT
        bFaultActive := TRUE;
        bSystemReady := FALSE;
        bExposing := FALSE;
        bLaserFireCommand := FALSE;
        rLaserPower_pct := 0.0;
        
        // Require system disable/enable to clear fault
        IF NOT bEnableSystem THEN
            bFaultActive := FALSE;
            eState := 0; // INIT
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

payload = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

json_str = json.dumps(payload)
subprocess.run(['python', 'pipeline/tools/safe_append.py', json_str, 'data/synthetic_generation_v3_enterprise.jsonl'])
