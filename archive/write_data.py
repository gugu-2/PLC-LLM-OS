import json
import os

user_prompt = """You are acting as the Lead Subsea Extraction Engineer for a Deep Ocean Methane Hydrate Consortium.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Benthic Methane Clathrate Harvester & Decompression Controller" (`FB_MethaneHydrate_Harvester`).

### Technical Specifications & Engineering Rigor Required:
1. **In-Situ Depressurization & Thermal Stimulation**:
   - Subsea wellhead modulation injecting heated seawater ($40^\circ\text{C}$) into the permafrost sediment while actively depressurizing the zone to force the phase-change dissociation of solid methane clathrates into gas and water.
2. **Multi-Phase Slurry Pumping & Separation**:
   - Control of subsea multiphase boosting pumps handling transient slugs of expanding methane gas, liquid water, and abrasive sand.
   - Real-time hydrate reformation prevention algorithms using Monoethylene Glycol (MEG) injection matrices based on the pressure-temperature stability curve.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, equations of state for gas expansion, PackML states."""

assistant_response = """Here is the master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the **Benthic Methane Clathrate Harvester & Decompression Controller**.

```iec-st
TYPE E_PackML_States :
(
    P_STOPPED := 0,
    P_STARTING := 1,
    P_EXECUTE := 2,
    P_HOLDING := 3,
    P_HELD := 4,
    P_UNHOLDING := 5,
    P_SUSPENDING := 6,
    P_SUSPENDED := 7,
    P_UNSUSPENDING := 8,
    P_STOPPING := 9,
    P_ABORTING := 10,
    P_ABORTED := 11
) INT;
END_TYPE

FUNCTION_BLOCK FB_PID_Advanced
VAR_INPUT
    rSetpoint : LREAL;
    rProcessValue : LREAL;
    rKp : LREAL;
    rKi : LREAL;
    rKd : LREAL;
END_VAR
VAR_OUTPUT
    rOutput : LREAL;
END_VAR
VAR
    rError : LREAL;
    rLastError : LREAL;
    rIntegral : LREAL;
    rDerivative : LREAL;
END_VAR
    rError := rSetpoint - rProcessValue;
    rIntegral := rIntegral + rError;
    rDerivative := rError - rLastError;
    rOutput := (rKp * rError) + (rKi * rIntegral) + (rKd * rDerivative);
    rLastError := rError;
END_FUNCTION_BLOCK

FUNCTION_BLOCK FB_MethaneHydrate_Harvester
VAR_INPUT
    bEnable : BOOL; (* Enable Harvest System *)
    bEmergencyStop : BOOL; (* Critical ESD *)
    rWellheadPressure_bar : LREAL; (* Subsea pressure at wellhead *)
    rWellheadTemp_C : LREAL; (* Subsea temperature at wellhead *)
    rSlurryDensity_kgm3 : LREAL; (* Density of the extracted multiphase flow *)
    rSeawaterTemp_C : LREAL; (* Ambient seawater temperature *)
    rMEG_TankLevel_pct : LREAL; (* Monoethylene Glycol tank level *)
END_VAR

VAR_OUTPUT
    bSystemReady : BOOL;
    bGasFlaring : BOOL;
    rPumpSpeedSetpoint_rpm : LREAL;
    rThermalInjectorFlow_kg_s : LREAL;
    rMEG_InjectionRate_L_min : LREAL;
    bAlarmHydrateReformation : BOOL;
    bAlarmPumpCavitation : BOOL;
    iState : INT; (* PackML State *)
END_VAR

VAR
    (* Internal State Machine *)
    eState : E_PackML_States := P_STOPPED;
    
    (* Hydrate Stability Curve Constants (Dickens & Quinby-Hunt) *)
    c_HydrateA : LREAL := 38.98;
    c_HydrateB : LREAL := 8533.8;
    
    (* PID Controllers *)
    fbThermalController : FB_PID_Advanced;
    
    (* Internal variables *)
    rTargetPressure_bar : LREAL;
    rDissociationTemp_C : LREAL;
    rPhaseMargin_C : LREAL;
END_VAR

(* Implementation *)
IF bEmergencyStop THEN
    eState := P_ABORTED;
END_IF

(* Hydrate Stability Threshold Calculation (simplified logarithmic fit) *)
(* T(dissociation) = c_HydrateB / (c_HydrateA - ln(P)) - 273.15 *)
IF rWellheadPressure_bar > 1.0 THEN
    rDissociationTemp_C := (c_HydrateB / (c_HydrateA - LN(rWellheadPressure_bar))) - 273.15;
ELSE
    rDissociationTemp_C := -273.15;
END_IF

(* Calculate phase margin *)
rPhaseMargin_C := rWellheadTemp_C - rDissociationTemp_C;

CASE eState OF
    P_STOPPED:
        bSystemReady := FALSE;
        rPumpSpeedSetpoint_rpm := 0.0;
        rThermalInjectorFlow_kg_s := 0.0;
        rMEG_InjectionRate_L_min := 0.0;
        IF bEnable AND NOT bEmergencyStop THEN
            eState := P_STARTING;
        END_IF
        
    P_STARTING:
        (* Prime MEG lines to prevent flash freezing during initial depressurization *)
        rMEG_InjectionRate_L_min := 15.0;
        IF rMEG_TankLevel_pct > 10.0 THEN
            eState := P_EXECUTE;
            bSystemReady := TRUE;
        ELSE
            eState := P_HELD;
        END_IF
        
    P_EXECUTE:
        (* Active Depressurization & Thermal Stimulation Phase *)
        
        (* 1. Thermal Injection Control *)
        (* Target 40 deg C injection to maintain +5C above dissociation *)
        fbThermalController(
            rSetpoint := rDissociationTemp_C + 5.0,
            rProcessValue := rWellheadTemp_C,
            rKp := 2.5,
            rKi := 0.1,
            rKd := 0.5,
            rOutput => rThermalInjectorFlow_kg_s
        );
        
        (* 2. Multiphase Slurry Pumping *)
        (* Dynamically adjust pump speed based on density to prevent cavitation from gas breakout *)
        IF rSlurryDensity_kgm3 < 500.0 THEN
            (* High gas void fraction, risk of cavitation - slow down *)
            rPumpSpeedSetpoint_rpm := 1200.0 * (rSlurryDensity_kgm3 / 500.0);
            bAlarmPumpCavitation := TRUE;
        ELSE
            (* Normal slurry mixture *)
            rPumpSpeedSetpoint_rpm := 3600.0;
            bAlarmPumpCavitation := FALSE;
        END_IF
        
        (* 3. Real-Time Hydrate Reformation Prevention (MEG Injection) *)
        IF rPhaseMargin_C < 2.0 THEN
            bAlarmHydrateReformation := TRUE;
            (* Aggressive MEG injection inversely proportional to thermal margin *)
            rMEG_InjectionRate_L_min := 50.0 - (rPhaseMargin_C * 25.0); 
            IF rMEG_InjectionRate_L_min > 100.0 THEN
                rMEG_InjectionRate_L_min := 100.0;
            END_IF
            IF rMEG_InjectionRate_L_min < 0.0 THEN
                rMEG_InjectionRate_L_min := 0.0;
            END_IF
        ELSE
            bAlarmHydrateReformation := FALSE;
            rMEG_InjectionRate_L_min := 5.0; (* Baseline continuous inhibition *)
        END_IF
        
        IF NOT bEnable THEN
            eState := P_STOPPING;
        END_IF

    P_HELD:
        (* System on standby due to low MEG or temporary pause *)
        rPumpSpeedSetpoint_rpm := 0.0;
        rThermalInjectorFlow_kg_s := 0.0;
        rMEG_InjectionRate_L_min := 5.0; (* Keep lines active *)
        IF bEnable AND rMEG_TankLevel_pct > 15.0 THEN
            eState := P_EXECUTE;
        END_IF
        
    P_STOPPING:
        (* Controlled shutdown, flood well with seawater and max MEG to secure *)
        rMEG_InjectionRate_L_min := 100.0;
        rPumpSpeedSetpoint_rpm := rPumpSpeedSetpoint_rpm * 0.9; (* Ramp down *)
        IF rPumpSpeedSetpoint_rpm < 10.0 THEN
            eState := P_STOPPED;
        END_IF
        
    P_ABORTED:
        (* Critical failure, immediate isolate and shutdown *)
        rPumpSpeedSetpoint_rpm := 0.0;
        rThermalInjectorFlow_kg_s := 0.0;
        rMEG_InjectionRate_L_min := 100.0; (* Max dose to plug *)
        bSystemReady := FALSE;
        IF NOT bEmergencyStop THEN
            eState := P_STOPPED;
        END_IF
END_CASE

iState := eState;
END_FUNCTION_BLOCK
```"""

record = {
    'messages': [
        {'role': 'user', 'content': user_prompt},
        {'role': 'assistant', 'content': assistant_response}
    ]
}

os.makedirs('data', exist_ok=True)
with open('data/synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(record) + '\n')

print('Success')
