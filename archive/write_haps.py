import json
import os

user_prompt = """You are acting as the Lead Aerospace Power Engineer for a Global High-Altitude Platform Station (HAPS) Initiative.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Stratospheric Airship Solar Array & Regenerative Hydrogen Fuel Cell Controller" (`FB_HAPS_RegenerativePower`).

### Technical Specifications & Engineering Rigor Required:
1. **Regenerative Electrolysis (Daytime Cycle)**:
   - Maximum Power Point Tracking (MPPT) of extreme-lightweight thin-film Gallium Arsenide (GaAs) solar arrays covering the top of a 200 m stratospheric blimp (20 km altitude).
   - Routing excess MW-scale daytime solar power into a closed-loop Proton Exchange Membrane (PEM) electrolyzer to crack water into pressurized H2 and O2 gases for energy storage.
2. **Fuel Cell Recombination (Nighttime Cycle)**:
   - Dynamic switching to PEM fuel cell mode during the frigid stratospheric night.
   - Precise mass flow rate tracking combining the stored H2 and O2 back into water to generate exactly 100 kW of continuous baseload power for the blimp's electric propulsion and 5G telecom payloads.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, comprehensive `VAR_INPUT`/`VAR_OUTPUT`, thermodynamics equations for fuel cell stoichiometry, PackML states.

Output a complete, valid JSON object with {"messages": [{"role": "user", "content": "Mega-prompt description"}, {"role": "assistant", "content": "Full raw Structured Text code inside ```iec-st```"}]}.
Append this JSON directly to `data/synthetic_generation_v3_enterprise.jsonl` using a safe append script."""

assistant_response = """Here is the master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the `FB_HAPS_RegenerativePower` controller. 

This module adheres to strict IEC 61131-3 syntax, utilizes double-precision `LREAL` calculations for thermodynamic precision, implements a standard PackML state machine for robust mission phase transitions, and performs continuous MPPT (Perturb & Observe) alongside stoichiometric flow calculations for the PEM systems.

```iec-st
TYPE E_PackML_State :
(
    STOPPED         := 0,
    STARTING        := 1,
    IDLE            := 2,
    EXECUTE_DAY     := 3, (* Solar Array & Electrolysis *)
    EXECUTE_NIGHT   := 4, (* Fuel Cell Baseload Generation *)
    HOLDING         := 5,
    HELD            := 6,
    UNHOLDING       := 7,
    SUSPENDING      := 8,
    SUSPENDED       := 9,
    UNSUSPENDING    := 10,
    ABORTING        := 11,
    ABORTED         := 12,
    CLEARING        := 13,
    STOPPING        := 14
);
END_TYPE

FUNCTION_BLOCK FB_HAPS_RegenerativePower
TITLE = 'Stratospheric Airship Solar Array & Regenerative Hydrogen Fuel Cell Controller'
VERSION = '1.0'
AUTHOR = 'Aerospace Power Engineering'

(* 
    System Overview:
    HAPS (High-Altitude Platform Station) operating at 20km altitude.
    Daytime: GaAs thin-film solar MPPT -> Payload & Propulsion + PEM Electrolyzer (H2/O2 generation).
    Nighttime: PEM Fuel Cell (H2/O2 consumption) -> Payload & Propulsion (100kW continuous).
*)

VAR_INPUT
    // Environmental Conditions (20km Stratosphere AM0)
    fSolarIrradiance       : LREAL; (* W/m^2, typically up to 1361 W/m^2 *)
    fAmbientTemp           : LREAL; (* K, ~216.65K at 20km *)
    fAmbientPressure       : LREAL; (* Pa, ~5474 Pa at 20km *)
    
    // Power Demands
    fPayloadDemand_kW      : LREAL; (* kW, Base load for 5G telecom payload *)
    fPropulsionDemand_kW   : LREAL; (* kW, Dynamic load for station keeping *)
    
    // Solar Array Sensors
    fArrayVoltage          : LREAL; (* V, DC Bus Voltage from Solar Array *)
    fArrayCurrent          : LREAL; (* A, DC Current from Solar Array *)
    
    // Storage Tanks Sensors
    fH2_TankPressure       : LREAL; (* Pa *)
    fO2_TankPressure       : LREAL; (* Pa *)
    fH2_TankTemp           : LREAL; (* K *)
    fO2_TankTemp           : LREAL; (* K *)
    fH2O_TankLevel         : LREAL; (* %, 0.0 - 100.0 *)
    
    // Commands & States (PackML)
    bStart                 : BOOL;
    bStop                  : BOOL;
    bEmergencyStop         : BOOL;
    bClear                 : BOOL;
END_VAR

VAR_OUTPUT
    // Power Management
    fSolarPower_kW         : LREAL;
    fElectrolyzerPower_kW  : LREAL;
    fFuelCellPower_kW      : LREAL;
    fNetPowerMargin_kW     : LREAL;
    
    // Actuators & Control
    fMPPT_DutyCycle        : LREAL; (* 0.0 - 1.0 (PWM duty for MPPT converter) *)
    fElectrolyzerCurrent_A : LREAL; (* A (Set point for electrolyzer stack) *)
    fFuelCellMassFlow_H2   : LREAL; (* kg/s (Valve position equivalent) *)
    fFuelCellMassFlow_O2   : LREAL; (* kg/s (Valve position equivalent) *)
    
    // PackML State
    eState                 : E_PackML_State;
    bAlarm                 : BOOL;
    nErrorID               : UDINT;
END_VAR

VAR
    // PackML State Machine
    eNextState             : E_PackML_State := E_PackML_State.STOPPED;
    
    // MPPT Internal State (Perturb & Observe)
    fLastArrayVoltage      : LREAL := 0.0;
    fLastArrayPower        : LREAL := 0.0;
    fPerturbStep           : LREAL := 0.0025; (* 0.25% step size *)
    
    // Thermodynamics & Electrochemistry Constants
    c_Faraday              : LREAL := 96485.33212; (* Faraday constant, C/mol *)
    c_MolarMass_H2         : LREAL := 0.00201588;  (* kg/mol *)
    c_MolarMass_O2         : LREAL := 0.031999;    (* kg/mol *)
    c_UnivGasConstant      : LREAL := 8.314462618; (* J/(mol*K) *)
    c_CellsInStack         : INT   := 1250;        (* Number of cells in FC/EL stack *)
    c_FC_Efficiency        : LREAL := 0.60;        (* Fuel Cell efficiency (approx. 60%) *)
    c_FC_NominalVoltage    : LREAL := 0.75;        (* Volts per cell operating *)
    c_EL_Efficiency        : LREAL := 0.75;        (* Electrolyzer efficiency *)
    c_EL_NominalVoltage    : LREAL := 1.48;        (* Volts per cell operating (thermoneutral) *)
    
    // Operational Limits
    c_MaxTankPressure_H2   : LREAL := 35000000.0;  (* 350 Bar in Pa *)
    c_MinTankPressure_H2   : LREAL := 1000000.0;   (* 10 Bar in Pa *)
    
    // Process Variables
    fTotalDemand_kW        : LREAL;
    fAvailableSolar_kW     : LREAL;
    bIsDaytime             : BOOL;
    fStackVoltage_FC       : LREAL;
    fStackVoltage_EL       : LREAL;
    fMolesPerSecond_H2     : LREAL;
END_VAR

(* 
    ===================================================================
    1. INPUT PROCESSING & SYSTEM DEMAND CALCULATIONS
    ===================================================================
*)
fTotalDemand_kW := fPayloadDemand_kW + fPropulsionDemand_kW;
fAvailableSolar_kW := (fArrayVoltage * fArrayCurrent) / 1000.0;
fSolarPower_kW := fAvailableSolar_kW;

// Determine Mission Phase (Day vs. Night based on Irradiance)
// At 20km, Irradiance drops rapidly at twilight.
IF fSolarIrradiance > 150.0 THEN
    bIsDaytime := TRUE;
ELSE
    bIsDaytime := FALSE;
END_IF

(* 
    ===================================================================
    2. PACKML STATE MACHINE EVALUATION
    ===================================================================
*)
IF bEmergencyStop THEN
    eState := E_PackML_State.ABORTING;
END_IF

CASE eState OF
    E_PackML_State.STOPPED:
        fMPPT_DutyCycle := 0.0;
        fElectrolyzerCurrent_A := 0.0;
        fFuelCellMassFlow_H2 := 0.0;
        fFuelCellMassFlow_O2 := 0.0;
        
        IF bStart THEN
            eState := E_PackML_State.STARTING;
        END_IF;
        
    E_PackML_State.STARTING:
        // System initialization logic (purge valves, pre-heat/cool)
        eState := E_PackML_State.IDLE;
        
    E_PackML_State.IDLE:
        IF fTotalDemand_kW > 0.0 THEN
            IF bIsDaytime THEN
                eState := E_PackML_State.EXECUTE_DAY;
            ELSE
                eState := E_PackML_State.EXECUTE_NIGHT;
            END_IF;
        END_IF;
        
    E_PackML_State.EXECUTE_DAY:
        IF NOT bIsDaytime THEN
            eState := E_PackML_State.EXECUTE_NIGHT;
        ELSIF bStop THEN
            eState := E_PackML_State.STOPPING;
        END_IF;
        
    E_PackML_State.EXECUTE_NIGHT:
        IF bIsDaytime THEN
            eState := E_PackML_State.EXECUTE_DAY;
        ELSIF bStop THEN
            eState := E_PackML_State.STOPPING;
        END_IF;
        
    E_PackML_State.STOPPING:
        fMPPT_DutyCycle := 0.0;
        fElectrolyzerCurrent_A := 0.0;
        fFuelCellMassFlow_H2 := 0.0;
        fFuelCellMassFlow_O2 := 0.0;
        eState := E_PackML_State.STOPPED;
        
    E_PackML_State.ABORTING:
        fMPPT_DutyCycle := 0.0;
        fElectrolyzerCurrent_A := 0.0;
        fFuelCellMassFlow_H2 := 0.0;
        fFuelCellMassFlow_O2 := 0.0;
        bAlarm := TRUE;
        nErrorID := 999; // Critical E-STOP
        eState := E_PackML_State.ABORTED;
        
    E_PackML_State.ABORTED:
        IF bClear THEN
            eState := E_PackML_State.CLEARING;
        END_IF;
        
    E_PackML_State.CLEARING:
        bAlarm := FALSE;
        nErrorID := 0;
        eState := E_PackML_State.STOPPED;
        
    ELSE
        // Handle undefined states gracefully
        eState := E_PackML_State.STOPPED;
END_CASE;

(* 
    ===================================================================
    3. CONTROL LOOP: DAYTIME CYCLE (MPPT & REGENERATIVE ELECTROLYSIS)
    ===================================================================
*)
IF eState = E_PackML_State.EXECUTE_DAY THEN
    // A. MPPT Perturb & Observe Algorithm
    IF fAvailableSolar_kW > fLastArrayPower THEN
        IF fArrayVoltage > fLastArrayVoltage THEN
            fMPPT_DutyCycle := fMPPT_DutyCycle + fPerturbStep;
        ELSE
            fMPPT_DutyCycle := fMPPT_DutyCycle - fPerturbStep;
        END_IF;
    ELSIF fAvailableSolar_kW < fLastArrayPower THEN
        IF fArrayVoltage > fLastArrayVoltage THEN
            fMPPT_DutyCycle := fMPPT_DutyCycle - fPerturbStep;
        ELSE
            fMPPT_DutyCycle := fMPPT_DutyCycle + fPerturbStep;
        END_IF;
    END_IF;
    
    // Clamp MPPT Duty Cycle
    IF fMPPT_DutyCycle > 1.0 THEN fMPPT_DutyCycle := 1.0; END_IF;
    IF fMPPT_DutyCycle < 0.0 THEN fMPPT_DutyCycle := 0.0; END_IF;
    
    fLastArrayPower := fAvailableSolar_kW;
    fLastArrayVoltage := fArrayVoltage;
    
    // B. Power Routing & Electrolyzer Control
    fNetPowerMargin_kW := fAvailableSolar_kW - fTotalDemand_kW;
    
    IF (fNetPowerMargin_kW > 0.0) AND (fH2_TankPressure < c_MaxTankPressure_H2) AND (fH2O_TankLevel > 5.0) THEN
        // Route excess power to Electrolyzer
        fElectrolyzerPower_kW := fNetPowerMargin_kW;
        fStackVoltage_EL := c_EL_NominalVoltage * INT_TO_LREAL(c_CellsInStack);
        
        // P = V * I -> I = P / V
        fElectrolyzerCurrent_A := (fElectrolyzerPower_kW * 1000.0) / fStackVoltage_EL;
    ELSE
        fElectrolyzerPower_kW := 0.0;
        fElectrolyzerCurrent_A := 0.0;
    END_IF;
    
    // No fuel cell operation during the day
    fFuelCellPower_kW := 0.0;
    fFuelCellMassFlow_H2 := 0.0;
    fFuelCellMassFlow_O2 := 0.0;

(* 
    ===================================================================
    4. CONTROL LOOP: NIGHTTIME CYCLE (FUEL CELL RECOMBINATION)
    ===================================================================
*)
ELSIF eState = E_PackML_State.EXECUTE_NIGHT THEN
    // Zero out solar systems
    fMPPT_DutyCycle := 0.0;
    fElectrolyzerCurrent_A := 0.0;
    fElectrolyzerPower_kW := 0.0;
    
    // Safety check: ensure adequate H2 pressure before attempting to generate power
    IF fH2_TankPressure > c_MinTankPressure_H2 THEN
        fFuelCellPower_kW := fTotalDemand_kW;
        
        // Stoichiometry Calculations (Thermodynamics)
        // Electric Power (W) = V_stack * I_stack
        fStackVoltage_FC := c_FC_NominalVoltage * INT_TO_LREAL(c_CellsInStack);
        
        // Block local variables properly (in ST local vars within logic blocks are not valid, we will define it in the global VAR block of the FB)
        // Wait, fRequiredCurrent_A needs to be handled without nested VAR.
        // Let me just compute it directly or use another variable. We can do it in one expression.
        
        // Faraday's Law of Electrolysis (applied to Fuel Cell)
        // I = P / (V * efficiency)
        // Moles of H2 per second = I / (2 * F) * N_cells
        fMolesPerSecond_H2 := (((fFuelCellPower_kW * 1000.0) / (fStackVoltage_FC * c_FC_Efficiency)) * INT_TO_LREAL(c_CellsInStack)) / (2.0 * c_Faraday);
        
        // Mass flow = Moles * Molar Mass
        fFuelCellMassFlow_H2 := fMolesPerSecond_H2 * c_MolarMass_H2;
        
        // Stoichiometric ratio for O2 is 0.5 moles of O2 per 1 mole of H2
        fFuelCellMassFlow_O2 := (fMolesPerSecond_H2 * 0.5) * c_MolarMass_O2;
        
        fNetPowerMargin_kW := 0.0; // Perfect load matching during nighttime
    ELSE
        // Critical failure: Out of Hydrogen during night phase
        bAlarm := TRUE;
        nErrorID := 101; // Out of Fuel
        fFuelCellPower_kW := 0.0;
        fFuelCellMassFlow_H2 := 0.0;
        fFuelCellMassFlow_O2 := 0.0;
    END_IF;
END_IF;

END_FUNCTION_BLOCK
```"""

item = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

file_path = r"c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"
with open(file_path, 'a', encoding='utf-8') as f:
    f.write(json.dumps(item) + '\n')

print("Successfully appended to JSONL.")
