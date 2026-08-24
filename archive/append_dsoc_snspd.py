import json
import os

data = {
    "messages": [
        {
            "role": "user",
            "content": """You are acting as the Principal Photonics Engineer for a Deep Space Network (DSN) ground station.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Deep Space Optical Communications (DSOC) Superconducting Nanowire Single-Photon Detector (SNSPD) Array Controller" (`FB_DSOC_PhotonReceiver`).

### Technical Specifications & Engineering Rigor Required:
1. **SNSPD Cryogenic Array Bias & Readout**:
   - Dynamic DC current biasing of a 64-pixel Niobium Nitride (NbN) nanowire array operating at 0.8 Kelvin, keeping it just below the superconducting critical current (Ic).
   - Ultra-fast Time-to-Digital Converter (TDC) integration capturing individual photon arrival times with < 50 picosecond jitter from a spacecraft orbiting Mars.
2. **Pulse Position Modulation (PPM) Demodulation**:
   - Decoding the 16-ary PPM optical signal by synchronizing the local ground clock with the incoming photon stream, correcting for massive Doppler shifts (> 10 GHz) due to relative planetary motion.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, orbital Doppler math, PackML states.

Output a complete, valid IEC 61131-3 ST implementation inside ```iec-st```."""
        },
        {
            "role": "assistant",
            "content": """Here is the complete, master-tier IEC 61131-3 Structured Text implementation for the DSOC SNSPD Array Controller.

### Architecture Overview
1. **Cryogenic Control & Biasing**: Maintains the 64-pixel NbN array at $0.8\\text{ K}$ and dynamically biases each pixel to $95\\%$ of its dynamic critical current ($I_c$).
2. **Doppler-Compensated Clock Recovery**: Real-time adjustment of the slot clock based on the relativistic Doppler shift resulting from Mars-Earth relative velocity.
3. **16-ary PPM Demodulation**: High-speed, parallel evaluation of photon arrival times against shifted time-slots, with continuous jitter tracking ($<50\\text{ ps}$).
4. **PackML State Machine**: Robust control flow for standard industrial automation integration.

```iec-st
(****************************************************************************************
* POU      : FB_DSOC_PhotonReceiver
* TYPE     : FUNCTION_BLOCK
* AUTHOR   : Principal Photonics Engineer, DSN
* DOMAIN   : Deep Space Optical Communications (DSOC) - Ground Station
* DESC     : Controls a 64-pixel NbN SNSPD array, biases nanowires, compensates 
*            Mars-Earth Doppler shift, and demodulates 16-ary PPM photon streams.
*****************************************************************************************)

TYPE E_PackML_State :
(
    eIDLE := 0,
    eSTARTING := 1,
    eEXECUTE := 2,
    eCOMPLETING := 3,
    eCOMPLETE := 4,
    eHOLDING := 5,
    eHELD := 6,
    eUNHOLDING := 7,
    eSUSPENDING := 8,
    eSUSPENDED := 9,
    eUNSUSPENDING := 10,
    eSTOPPING := 11,
    eSTOPPED := 12,
    eABORTING := 13,
    eABORTED := 14,
    eCLEARING := 15
) DINT;
END_TYPE

TYPE ST_SNSPD_Pixel :
STRUCT
    fCriticalCurrent_uA : LREAL := 15.0;  (* Superconducting critical current Ic *)
    fBiasCurrent_uA     : LREAL;          (* Commanded DC bias *)
    bAvalancheDetected  : BOOL;           (* Photon absorption event trigger *)
    fArrivalTime_ps     : LREAL;          (* Precise TDC arrival time *)
    bQuenched           : BOOL;           (* True if wire latched to resistive state *)
    nHotSpotCount       : LINT;           (* Total photon hits *)
END_STRUCT
END_TYPE

TYPE ST_DSOC_Telemetry :
STRUCT
    fDopplerShift_GHz   : LREAL;          (* Relativistic Doppler shift *)
    fSpacecraftRange_km : LREAL;          (* Calculated range approximation *)
    fAverageJitter_ps   : LREAL;          (* Timing jitter across array *)
    nTotalPhotons       : LINT;           (* Lifetime array counts *)
    nDemodulatedSymbols : LINT;           (* Valid 16-PPM symbols decoded *)
    fArrayMeanTemp_K    : LREAL;          (* Monitored cryo-stage temp *)
    bLinkLock           : BOOL;           (* True if clock sync is established *)
END_STRUCT
END_TYPE

FUNCTION_BLOCK FB_DSOC_PhotonReceiver
VAR_INPUT
    eCommand                : E_PackML_State; (* PackML Command from Superior *)
    fBaseOpticalFreq_THz    : LREAL := 193.1; (* Standard DSOC 1550nm carrier *)
    fSpacecraftVelocity_kms : LREAL;          (* Relative line-of-sight velocity (positive = receding) *)
    fSpacecraftRange_km     : LREAL;          (* Ephemeris-derived distance *)
    aTdcArrivals_ps         : ARRAY[0..63] OF LREAL; (* Fast TDC buffers *)
    aAvalancheTrigger       : ARRAY[0..63] OF BOOL;  (* TDC valid triggers *)
    fColdStageTemp_K        : LREAL;          (* Feedback from cryocooler *)
    fSymbolRate_MHz         : LREAL := 10.0;  (* Baseline symbol rate without Doppler *)
END_VAR

VAR_OUTPUT
    eState                  : E_PackML_State := eIDLE;
    aDemodulatedSymbols     : ARRAY[0..1023] OF BYTE;
    nSymbolsAvailable       : INT;
    stTelemetry             : ST_DSOC_Telemetry;
    aBiasOutputs_uA         : ARRAY[0..63] OF LREAL;
    bSystemFault            : BOOL;
    sFaultMsg               : STRING(255);
END_VAR

VAR
    (* Array & Physics State *)
    aPixels                 : ARRAY[0..63] OF ST_SNSPD_Pixel;
    i                       : INT;
    j                       : INT;
    
    (* Physics Constants *)
    C_LIGHT_KM_S            : LREAL := 299792.458; 
    C_TARGET_TEMP_K         : LREAL := 0.8;
    C_TEMP_TOLERANCE_K      : LREAL := 0.05;
    C_BIAS_MARGIN           : LREAL := 0.95; (* Bias at 95% of Ic *)
    
    (* Synchronization & PPM Demodulation *)
    fDopplerFactor          : LREAL;
    fAdjustedSymbolRate_MHz : LREAL;
    fSymbolDuration_ps      : LREAL;
    fSlotDuration_ps        : LREAL;
    nPPM_Order              : INT := 16;
    
    aSlotPhotonCounts       : ARRAY[0..15] OF INT;
    nMaxPhotons             : INT;
    nWinningSlot            : INT;
    fSlotBoundary_ps        : LREAL;
    
    (* Jitter and Analytics *)
    fArrivalOffset_ps       : LREAL;
    fCumulativeJitter       : LREAL;
    nJitterSamples          : LINT;
    
    bInitDone               : BOOL;
END_VAR

(* ========================================================================= *)
(* 1. PACKML STATE MACHINE IMPLEMENTATION                                    *)
(* ========================================================================= *)
CASE eState OF

    eIDLE:
        bSystemFault := FALSE;
        sFaultMsg := '';
        stTelemetry.bLinkLock := FALSE;
        
        IF eCommand = eSTARTING THEN
            eState := eSTARTING;
        END_IF;

    eSTARTING:
        (* Initialize Pixel Array *)
        IF NOT bInitDone THEN
            FOR i := 0 TO 63 DO
                aPixels[i].fCriticalCurrent_uA := 15.0; 
                aPixels[i].fBiasCurrent_uA := 0.0;
                aPixels[i].bQuenched := FALSE;
            END_FOR;
            bInitDone := TRUE;
        END_IF;
        
        (* Ramp up bias currents if temperature is stable *)
        IF ABS(fColdStageTemp_K - C_TARGET_TEMP_K) <= C_TEMP_TOLERANCE_K THEN
            FOR i := 0 TO 63 DO
                (* Dynamically scale Ic based on actual temp drift using BCS theory approx *)
                aPixels[i].fCriticalCurrent_uA := 15.0 * SQRT(1.0 - (fColdStageTemp_K / 9.3) * (fColdStageTemp_K / 9.3)); 
                
                (* Gently ramp bias to 95% of operational Ic *)
                IF aPixels[i].fBiasCurrent_uA < (aPixels[i].fCriticalCurrent_uA * C_BIAS_MARGIN) THEN
                    aPixels[i].fBiasCurrent_uA := aPixels[i].fBiasCurrent_uA + 0.1; 
                END_IF;
                
                aBiasOutputs_uA[i] := aPixels[i].fBiasCurrent_uA;
            END_FOR;
            
            IF aPixels[0].fBiasCurrent_uA >= (aPixels[0].fCriticalCurrent_uA * C_BIAS_MARGIN) THEN
                eState := eEXECUTE;
            END_IF;
        ELSE
            bSystemFault := TRUE;
            sFaultMsg := 'CRYO FAULT: SNSPD array temperature out of superconducting limits.';
            eState := eABORTING;
        END_IF;

    eEXECUTE:
        (* Handle State Transitions *)
        IF eCommand = eSTOPPING THEN
            eState := eSTOPPING;
        ELSIF eCommand = eHOLDING THEN
            eState := eHOLDING;
        END_IF;

        (* ========================================================================= *)
        (* 2. RELATIVISTIC DOPPLER COMPENSATION                                      *)
        (* ========================================================================= *)
        (* Calculate Relativistic Doppler factor for relative velocities *)
        (* f_recv = f_src * SQRT((c - v)/(c + v)) *)
        fDopplerFactor := SQRT((C_LIGHT_KM_S - fSpacecraftVelocity_kms) / (C_LIGHT_KM_S + fSpacecraftVelocity_kms));
        
        (* Calculate optical frequency shift for telemetry (>10 GHz offset typical for Mars) *)
        stTelemetry.fDopplerShift_GHz := (fBaseOpticalFreq_THz * 1000.0) * (1.0 - fDopplerFactor);
        
        (* Adjust ground clock symbol rate & slot durations *)
        fAdjustedSymbolRate_MHz := fSymbolRate_MHz * fDopplerFactor;
        
        (* 1 MHz = 1e6 Hz -> Period in ps = 1e12 / (Rate * 1e6) = 1e6 / Rate *)
        fSymbolDuration_ps := 1000000.0 / fAdjustedSymbolRate_MHz; 
        fSlotDuration_ps := fSymbolDuration_ps / INT_TO_LREAL(nPPM_Order);

        (* ========================================================================= *)
        (* 3. 16-ARY PULSE POSITION MODULATION (PPM) DEMODULATION                    *)
        (* ========================================================================= *)
        nSymbolsAvailable := 0;
        (* In ST, initializing an array dynamically usually involves a loop unless MEMSET is supported *)
        FOR j := 0 TO 15 DO
            aSlotPhotonCounts[j] := 0;
        END_FOR;
        
        (* Read raw TDC data and map to array pixels *)
        FOR i := 0 TO 63 DO
            IF aAvalancheTrigger[i] AND NOT aPixels[i].bQuenched THEN
                aPixels[i].bAvalancheDetected := TRUE;
                aPixels[i].fArrivalTime_ps := aTdcArrivals_ps[i];
                aPixels[i].nHotSpotCount := aPixels[i].nHotSpotCount + 1;
                stTelemetry.nTotalPhotons := stTelemetry.nTotalPhotons + 1;
                
                (* Compute which PPM slot this photon falls into *)
                (* Modulo operation over the symbol duration to find offset within symbol *)
                fArrivalOffset_ps := aPixels[i].fArrivalTime_ps - (DINT_TO_LREAL(LREAL_TO_DINT(aPixels[i].fArrivalTime_ps / fSymbolDuration_ps)) * fSymbolDuration_ps);
                
                (* Determine slot index (0 to 15) *)
                j := LREAL_TO_INT(fArrivalOffset_ps / fSlotDuration_ps);
                
                IF j >= 0 AND j < nPPM_Order THEN
                    aSlotPhotonCounts[j] := aSlotPhotonCounts[j] + 1;
                    
                    (* Calculate jitter relative to center of the expected slot *)
                    fSlotBoundary_ps := (INT_TO_LREAL(j) * fSlotDuration_ps) + (fSlotDuration_ps / 2.0);
                    fCumulativeJitter := fCumulativeJitter + ABS(fArrivalOffset_ps - fSlotBoundary_ps);
                    nJitterSamples := nJitterSamples + 1;
                END_IF;
                
                (* Active quenching/reset simulation: reset trigger *)
                aAvalancheTrigger[i] := FALSE;
            END_IF;
        END_FOR;
        
        (* Maximum Likelihood Sequence Detection (MLSD) for 16-PPM Symbol *)
        nMaxPhotons := 0;
        nWinningSlot := -1;
        FOR j := 0 TO 15 DO
            IF aSlotPhotonCounts[j] > nMaxPhotons THEN
                nMaxPhotons := aSlotPhotonCounts[j];
                nWinningSlot := j;
            END_IF;
        END_FOR;
        
        (* If enough coincident photons detect the pulse, decode symbol *)
        IF nMaxPhotons >= 4 THEN (* Minimum coincidence threshold across 64 pixels *)
            IF nSymbolsAvailable < 1024 THEN
                aDemodulatedSymbols[nSymbolsAvailable] := INT_TO_BYTE(nWinningSlot);
                nSymbolsAvailable := nSymbolsAvailable + 1;
                stTelemetry.nDemodulatedSymbols := stTelemetry.nDemodulatedSymbols + 1;
                stTelemetry.bLinkLock := TRUE;
            END_IF;
        ELSE
            stTelemetry.bLinkLock := FALSE; (* Signal fade or blockage *)
        END_IF;

        (* Telemetry Update *)
        IF nJitterSamples > 0 THEN
            stTelemetry.fAverageJitter_ps := fCumulativeJitter / LINT_TO_LREAL(nJitterSamples);
            
            (* Jitter fault threshold (< 50ps required for link viability) *)
            IF stTelemetry.fAverageJitter_ps > 50.0 THEN
                sFaultMsg := 'WARNING: Timing jitter exceeds 50ps threshold. Check PLL lock.';
            END_IF;
        END_IF;
        
        stTelemetry.fArrayMeanTemp_K := fColdStageTemp_K;
        stTelemetry.fSpacecraftRange_km := fSpacecraftRange_km;

    eSTOPPING:
        (* Safely ramp down SNSPD bias to zero *)
        FOR i := 0 TO 63 DO
            IF aPixels[i].fBiasCurrent_uA > 0.1 THEN
                aPixels[i].fBiasCurrent_uA := aPixels[i].fBiasCurrent_uA - 0.1;
            ELSE
                aPixels[i].fBiasCurrent_uA := 0.0;
            END_IF;
            aBiasOutputs_uA[i] := aPixels[i].fBiasCurrent_uA;
        END_FOR;
        
        IF aPixels[0].fBiasCurrent_uA = 0.0 THEN
            eState := eSTOPPED;
        END_IF;
        
    eSTOPPED:
        IF eCommand = eIDLE THEN
            eState := eIDLE;
        END_IF;

    eABORTING:
        (* Immediate quenching and protection *)
        FOR i := 0 TO 63 DO
            aPixels[i].fBiasCurrent_uA := 0.0;
            aBiasOutputs_uA[i] := 0.0;
        END_FOR;
        eState := eABORTED;
        
    eABORTED:
        IF eCommand = eCLEARING THEN
            eState := eCLEARING;
        END_IF;
        
    eCLEARING:
        bSystemFault := FALSE;
        sFaultMsg := '';
        eState := eIDLE;
        
    ELSE
        (* Handle undefined states or unhandled PackML transitions gracefully *)
        eState := eIDLE;
        
END_CASE;
END_FUNCTION_BLOCK
```"""
        }
    ]
}

os.makedirs('data', exist_ok=True)
with open('data/synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(data) + '\\n')
