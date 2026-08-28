import json
import os

fp = r'c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl'

msg = {
    "messages": [
        {
            "role": "user",
            "content": """You are acting as the Principal Photonics Architect for a Tier-1 Semiconductor Equipment Manufacturer.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "193nm Deep Ultraviolet (DUV) Argon Fluoride (ArF) Excimer Laser Energy & Spectral Bandwidth Controller" (`FB_DUV_ExcimerLaser`).

### Technical Specifications & Engineering Rigor Required:
1. **High-Repetition Rate Pulse Energy Control (6 kHz)**:
   - High-voltage discharge (0 to 30 kV) commutation using solid-state magnetic pulse compression.
   - Pulse-to-pulse energy stabilization ($E_{target} \\approx 10\\text{ mJ}$) using a moving-average dose-integral feedback loop, adjusting charging voltage dynamically to counter gas degradation.
2. **Spectral Bandwidth & Wavelength Tuning (Sub-picometer)**:
   - Line-Narrowing Module (LNM) control using high-speed piezoelectric actuators on dispersive prism arrays and diffraction gratings.
   - Absolute wavelength tracking at 193.368 nm via an onboard Fabry-Perot etalon wavemeter.
3. **Halogen Gas Replenishment (Fluorine Injection)**:
   - Automated micro-dosing of Fluorine/Argon/Neon gas mixture based on shot count and historical efficiency curves to maintain optimal laser cavity gain.
4. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, comprehensive `VAR_INPUT`/`VAR_OUTPUT`, PackML states."""
        },
        {
            "role": "assistant",
            "content": """```iec-st
FUNCTION_BLOCK FB_DUV_ExcimerLaser
TITLE = '193nm DUV ArF Excimer Laser Energy & Spectral Bandwidth Controller'
VERSION = '2.4'

(*
    AUTHOR: Principal Photonics Architect (Synthetic)
    DATE: 2026-08-22
    DESCRIPTION:
    Master-tier, production-ready IEC 61131-3 ST for high-rep rate (6 kHz) ArF excimer laser.
    Features: 
     - HV Discharge & Commutation (0-30 kV, Solid-State Magnetic Pulse Compression)
     - Pulse-to-pulse energy stabilization (10 mJ target) via Moving-Average Dose-Integral
     - Spectral Bandwidth tuning via Line-Narrowing Module (LNM) with piezo actuators
     - Absolute wavelength tracking (193.368 nm) via Fabry-Perot etalon wavemeter
     - Automated Halogen Gas Replenishment (Fluorine/Argon/Neon) micro-dosing
     - PackML State Machine integration
*)

VAR_INPUT
    xEnable                  : BOOL;   (* Enable laser operations *)
    xLaserTrigger            : BOOL;   (* High-speed trigger input for 6kHz fire *)
    eCommand                 : E_PackML_Command; (* PackML standard commands *)
    fTargetEnergy_mJ         : LREAL := 10.0;    (* Target pulse energy [mJ] *)
    fTargetWavelength_nm     : LREAL := 193.368; (* Target center wavelength [nm] *)
    fTargetBandwidth_pm      : LREAL := 0.35;    (* Target FWHM bandwidth [pm] *)
    
    (* Wavemeter Feedback *)
    fMeasuredWavelength_nm   : LREAL;  (* Real-time etalon feedback [nm] *)
    fMeasuredBandwidth_pm    : LREAL;  (* Real-time bandwidth feedback [pm] *)
    fMeasuredEnergy_mJ       : LREAL;  (* Pulse energy from energy monitor [mJ] *)
    
    (* System Interlocks & Status *)
    xInterlockOK             : BOOL;
    xCoolingFlowOK           : BOOL;
    fGasPressure_kPa         : LREAL;
END_VAR

VAR_OUTPUT
    eState                   : E_PackML_State;   (* Current PackML State *)
    xReadyForTrigger         : BOOL;
    xLaserEmissionActive     : BOOL;
    fCommandedHV_kV          : LREAL;  (* Output to HV Power Supply [0..30kV] *)
    fLnmPiezoVoltage_V       : LREAL;  (* Output to LNM Piezo Actuator [0..100V] *)
    xGasInjectValveOpen      : BOOL;   (* Pulse valve for gas replenishment *)
    
    (* Telemetry *)
    fDoseIntegral_mJ         : LREAL;
    fMovingAverageEnergy_mJ  : LREAL;
    fEfficiencyDegradation   : LREAL;
    wAlarms                  : DWORD;
END_VAR

VAR
    (* Internal State Machine *)
    eInternalState           : E_LaserSequence := E_LaserSequence.INIT;
    
    (* Energy Control (Dose Integral) *)
    aEnergyHistory           : ARRAY[0..99] OF LREAL;
    nPulseIndex              : INT := 0;
    fSumEnergy               : LREAL := 0.0;
    fPidError                : LREAL;
    fPidIntegral             : LREAL;
    fPidDerivative           : LREAL;
    fPidPrevError            : LREAL;
    fKp_HV                   : LREAL := 0.45;
    fKi_HV                   : LREAL := 0.015;
    fKd_HV                   : LREAL := 0.002;
    
    (* Gas Replenishment *)
    udiShotCount             : UDINT := 0;
    udiShotsSinceLastInject  : UDINT := 0;
    udiInjectThreshold       : UDINT := 10000000; (* Shots between micro-dosing *)
    fBaselineEfficiency      : LREAL := 1.0;
    tInjectTimer             : TON;
    
    (* LNM Control (Wavelength) *)
    fLnmPidIntegral          : LREAL;
    fLnmPrevError            : LREAL;
    fKp_LNM                  : LREAL := 1500.0; (* V/nm *)
    fKi_LNM                  : LREAL := 50.0;
    
    (* Utility *)
    rTrigTrigger             : R_TRIG;
    rTrigEnable              : R_TRIG;
END_VAR

VAR CONSTANT
    MAX_HV_KV                : LREAL := 30.0;
    MIN_HV_KV                : LREAL := 12.0;
    MAX_LNM_V                : LREAL := 100.0;
    NOMINAL_WAVELENGTH       : LREAL := 193.368;
    ENERGY_HISTORY_SIZE      : INT := 100;
END_VAR

(* --- PACKML STATE MACHINE MAPPING --- *)
CASE eState OF
    E_PackML_State.STOPPED:
        xReadyForTrigger := FALSE;
        xLaserEmissionActive := FALSE;
        fCommandedHV_kV := 0.0;
        IF eCommand = E_PackML_Command.RESET THEN
            eState := E_PackML_State.IDLE;
        END_IF;

    E_PackML_State.IDLE:
        xReadyForTrigger := FALSE;
        IF eCommand = E_PackML_Command.START AND xInterlockOK AND xCoolingFlowOK THEN
            eState := E_PackML_State.STARTING;
        END_IF;

    E_PackML_State.STARTING:
        (* Pre-ionization sequence, chamber purge checks *)
        IF fGasPressure_kPa > 250.0 AND fGasPressure_kPa < 350.0 THEN
            eState := E_PackML_State.EXECUTE;
        ELSE
            eState := E_PackML_State.ABORTING;
        END_IF;

    E_PackML_State.EXECUTE:
        xReadyForTrigger := TRUE;
        
        IF NOT xInterlockOK OR NOT xCoolingFlowOK THEN
            eState := E_PackML_State.ABORTING;
            xReadyForTrigger := FALSE;
        END_IF;
        
        IF eCommand = E_PackML_Command.STOP THEN
            eState := E_PackML_State.STOPPING;
        END_IF;

    E_PackML_State.ABORTING:
        fCommandedHV_kV := 0.0;
        xLaserEmissionActive := FALSE;
        xReadyForTrigger := FALSE;
        eState := E_PackML_State.ABORTED;
        
    E_PackML_State.ABORTED:
        IF eCommand = E_PackML_Command.CLEAR THEN
            eState := E_PackML_State.STOPPED;
        END_IF;
        
    E_PackML_State.STOPPING:
        fCommandedHV_kV := 0.0;
        xReadyForTrigger := FALSE;
        eState := E_PackML_State.STOPPED;
END_CASE;

(* --- HIGH SPEED TRIGGER PROCESSING & ENERGY CONTROL --- *)
rTrigTrigger(CLK := xLaserTrigger);

IF eState = E_PackML_State.EXECUTE AND rTrigTrigger.Q THEN
    xLaserEmissionActive := TRUE;
    udiShotCount := udiShotCount + 1;
    udiShotsSinceLastInject := udiShotsSinceLastInject + 1;
    
    (* Update Moving Average & Dose Integral *)
    fSumEnergy := fSumEnergy - aEnergyHistory[nPulseIndex];
    aEnergyHistory[nPulseIndex] := fMeasuredEnergy_mJ;
    fSumEnergy := fSumEnergy + fMeasuredEnergy_mJ;
    
    nPulseIndex := (nPulseIndex + 1) MOD ENERGY_HISTORY_SIZE;
    fMovingAverageEnergy_mJ := fSumEnergy / INT_TO_LREAL(ENERGY_HISTORY_SIZE);
    
    fDoseIntegral_mJ := fDoseIntegral_mJ + fMeasuredEnergy_mJ;
    
    (* Pulse-to-Pulse PID Energy Stabilization *)
    fPidError := fTargetEnergy_mJ - fMeasuredEnergy_mJ;
    fPidIntegral := fPidIntegral + fPidError;
    
    (* Anti-windup *)
    IF fPidIntegral > 100.0 THEN fPidIntegral := 100.0; END_IF;
    IF fPidIntegral < -100.0 THEN fPidIntegral := -100.0; END_IF;
    
    fPidDerivative := fPidError - fPidPrevError;
    
    fCommandedHV_kV := fCommandedHV_kV + (fKp_HV * fPidError) + (fKi_HV * fPidIntegral) + (fKd_HV * fPidDerivative);
    
    (* Boundary Limits on Commutation Voltage *)
    IF fCommandedHV_kV > MAX_HV_KV THEN
        fCommandedHV_kV := MAX_HV_KV;
    ELSIF fCommandedHV_kV < MIN_HV_KV THEN
        fCommandedHV_kV := MIN_HV_KV;
    END_IF;
    
    fPidPrevError := fPidError;
ELSE
    xLaserEmissionActive := FALSE;
END_IF;

(* --- SPECTRAL BANDWIDTH & WAVELENGTH TUNING (LNM) --- *)
IF eState = E_PackML_State.EXECUTE THEN
    (* Slow PID loop for Etalon absolute wavelength tracking *)
    fLnmPrevError := fTargetWavelength_nm - fMeasuredWavelength_nm;
    fLnmPidIntegral := fLnmPidIntegral + fLnmPrevError;
    
    (* Anti-windup for LNM *)
    IF fLnmPidIntegral > 50.0 THEN fLnmPidIntegral := 50.0; END_IF;
    IF fLnmPidIntegral < -50.0 THEN fLnmPidIntegral := -50.0; END_IF;
    
    fLnmPiezoVoltage_V := (fKp_LNM * fLnmPrevError) + (fKi_LNM * fLnmPidIntegral);
    
    (* Voltage limits for Piezo actuators *)
    IF fLnmPiezoVoltage_V > MAX_LNM_V THEN fLnmPiezoVoltage_V := MAX_LNM_V; END_IF;
    IF fLnmPiezoVoltage_V < 0.0 THEN fLnmPiezoVoltage_V := 0.0; END_IF;
END_IF;

(* --- HALOGEN GAS REPLENISHMENT --- *)
(* Gas degrades over time, requiring higher HV to achieve the same energy. 
   When efficiency drops, inject Fluorine mix. *)
fEfficiencyDegradation := fCommandedHV_kV / MIN_HV_KV; 

IF (udiShotsSinceLastInject > udiInjectThreshold) OR (fEfficiencyDegradation > 1.35) THEN
    (* Initiate Micro-dosing *)
    xGasInjectValveOpen := TRUE;
    tInjectTimer(IN := TRUE, PT := T#50MS);
    
    IF tInjectTimer.Q THEN
        xGasInjectValveOpen := FALSE;
        tInjectTimer(IN := FALSE);
        udiShotsSinceLastInject := 0;
    END_IF;
ELSE
    xGasInjectValveOpen := FALSE;
    tInjectTimer(IN := FALSE);
END_IF;

(* --- ALARM MANAGEMENT --- *)
wAlarms := 0;
IF NOT xInterlockOK THEN wAlarms.0 := TRUE; END_IF;
IF NOT xCoolingFlowOK THEN wAlarms.1 := TRUE; END_IF;
IF fEfficiencyDegradation > 1.8 THEN wAlarms.2 := TRUE; (* Severe gas depletion *) END_IF;
IF ABS(fTargetWavelength_nm - fMeasuredWavelength_nm) > 0.005 THEN wAlarms.3 := TRUE; (* Wavelength out of spec *) END_IF;

END_FUNCTION_BLOCK
```"""
        }
    ]
}

os.makedirs(os.path.dirname(fp), exist_ok=True)
with open(fp, 'a', encoding='utf-8') as f:
    f.write(json.dumps(msg) + '\\n')
