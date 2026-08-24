import os
import json

os.makedirs('data', exist_ok=True)

prompt = """You are acting as the Chief Aerodynamics Facility Engineer for an Advanced Aerospace Test Center.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Mach 10 Hypersonic Blowdown Wind Tunnel & Plasma Arc-Heater Controller" (`FB_Hypersonic_WindTunnel`).

### Technical Specifications & Engineering Rigor Required:
1. **High-Pressure Blowdown Sequencing**:
   - Ultra-fast acting hydraulically actuated regulating valves to maintain exactly $200\\text{ bar}$ stagnation pressure ($P_0$) in the settling chamber for a 5-second test window, drawing from a $300\\text{ bar}$ tank farm.
2. **Plasma Arc-Heater Power Modulation**:
   - Closed-loop MW-class DC arc heater current control to rapidly heat the incoming air to $4,000\\text{ K}$, preventing the air from liquefying as it expands through the converging-diverging nozzle to Mach 10.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, comprehensive `VAR_INPUT`/`VAR_OUTPUT`, thermodynamics equations for isentropic expansion, PackML states.

Output a complete, valid JSON object with {"messages": [{"role": "user", "content": "Mega-prompt description"}, {"role": "assistant", "content": "Full raw Structured Text code inside ```iec-st```"}]}."""

st_code = """```iec-st
(*
  =============================================================================
  FB_Hypersonic_WindTunnel
  =============================================================================
  Description:
    Mach 10 Hypersonic Blowdown Wind Tunnel & Plasma Arc-Heater Controller
  
  Features:
    - PackML State Machine (Idle, Starting, Execute, Completing, Aborted)
    - High-Pressure Blowdown Sequencing (300 bar -> 200 bar stagnation pressure)
    - Plasma Arc-Heater Power Modulation (MW-class DC arc heater to 4,000 K)
    - Isentropic Expansion calculations to verify Mach 10 conditions
    
  Standards:
    - IEC 61131-3 Structured Text
    - LREAL variables for high precision control
  =============================================================================
*)
FUNCTION_BLOCK FB_Hypersonic_WindTunnel
VAR_INPUT
    bEnable               : BOOL;           (* Master enable *)
    bStart                : BOOL;           (* Start test sequence *)
    bAbort                : BOOL;           (* Emergency abort *)
    
    // Sensor Inputs
    fStagnationPressure   : LREAL;          (* P0 - Settling chamber pressure [bar] *)
    fStagnationTemp       : LREAL;          (* T0 - Settling chamber temperature [K] *)
    fTankPressure         : LREAL;          (* Storage tank pressure [bar] *)
    fTestSectionStaticP   : LREAL;          (* P - Test section static pressure [bar] *)
    fTestSectionStaticT   : LREAL;          (* T - Test section static temperature [K] *)
    
    // Settings
    fTargetStagPressure   : LREAL := 200.0; (* Desired P0 [bar] *)
    fTargetStagTemp       : LREAL := 4000.0;(* Desired T0 [K] *)
    tTestDuration         : TIME := T#5S;   (* Blowdown test duration *)
END_VAR

VAR_OUTPUT
    // Actuator Commands
    fValvePositionCmd     : LREAL;          (* Hydraulic regulator valve [0.0 - 100.0%] *)
    fArcHeaterPowerCmd    : LREAL;          (* Arc heater current command [0.0 - 100.0 MW equivalent] *)
    
    // Status
    iPackMLState          : INT;            (* Current PackML State *)
    bTestActive           : BOOL;           (* Indicates test window is active *)
    bTestComplete         : BOOL;           (* Indicates successful completion *)
    
    // Calculated Metrics
    fCalculatedMach       : LREAL;          (* Calculated Mach number in test section *)
    fCalculatedVelocity   : LREAL;          (* Calculated velocity [m/s] *)
END_VAR

VAR
    // PackML State Constants
    STATE_STOPPED         : INT := 1;
    STATE_STARTING        : INT := 2;
    STATE_IDLE            : INT := 3;
    STATE_EXECUTE         : INT := 4;
    STATE_COMPLETING      : INT := 5;
    STATE_COMPLETE        : INT := 6;
    STATE_ABORTING        : INT := 7;
    STATE_ABORTED         : INT := 8;
    
    // State Machine Variables
    CurrentState          : INT := 1;
    SequenceTimer         : TON;            (* Timer for the 5-second blowdown test *)
    
    // PID Controllers
    PressurePID           : FB_PID;         (* Standard PID block for valve *)
    TempPID               : FB_PID;         (* Standard PID block for heater *)
    
    // Thermodynamics Constants
    Gamma                 : LREAL := 1.4;   (* Ratio of specific heats for Air *)
    R_Specific            : LREAL := 287.05;(* Specific gas constant for Air [J/(kg*K)] *)
    
    // Intermediate Calculations
    fPressureRatio        : LREAL;
    fSpeedOfSound         : LREAL;
END_VAR

(* --- State Machine Execution --- *)
IF bAbort THEN
    CurrentState := STATE_ABORTING;
END_IF;

CASE CurrentState OF
    STATE_STOPPED:
        iPackMLState := STATE_STOPPED;
        fValvePositionCmd := 0.0;
        fArcHeaterPowerCmd := 0.0;
        bTestActive := FALSE;
        bTestComplete := FALSE;
        
        IF bEnable THEN
            CurrentState := STATE_IDLE;
        END_IF;
        
    STATE_IDLE:
        iPackMLState := STATE_IDLE;
        IF NOT bEnable THEN
            CurrentState := STATE_STOPPED;
        ELSIF bStart AND (fTankPressure >= fTargetStagPressure) THEN
            CurrentState := STATE_STARTING;
        END_IF;
        
    STATE_STARTING:
        iPackMLState := STATE_STARTING;
        
        // Pre-heat / Pre-pressurize sequence
        TempPID(
            fSetpoint := fTargetStagTemp,
            fProcessVar := fStagnationTemp,
            fKp := 0.5, fKi := 0.1, fKd := 0.01,
            fOutput => fArcHeaterPowerCmd
        );
        
        PressurePID(
            fSetpoint := fTargetStagPressure,
            fProcessVar := fStagnationPressure,
            fKp := 2.5, fKi := 0.5, fKd := 0.05,
            fOutput => fValvePositionCmd
        );
        
        // Wait for Stabilization
        IF (ABS(fStagnationPressure - fTargetStagPressure) < 5.0) AND 
           (ABS(fStagnationTemp - fTargetStagTemp) < 50.0) THEN
            SequenceTimer(IN := FALSE); // Reset timer
            CurrentState := STATE_EXECUTE;
        END_IF;
        
    STATE_EXECUTE:
        iPackMLState := STATE_EXECUTE;
        bTestActive := TRUE;
        
        // Maintain Continuous Pressure and Temp Control
        PressurePID(
            fSetpoint := fTargetStagPressure,
            fProcessVar := fStagnationPressure,
            fKp := 2.5, fKi := 0.5, fKd := 0.05,
            fOutput => fValvePositionCmd
        );
        
        TempPID(
            fSetpoint := fTargetStagTemp,
            fProcessVar := fStagnationTemp,
            fKp := 0.5, fKi := 0.1, fKd := 0.01,
            fOutput => fArcHeaterPowerCmd
        );
        
        // Execute the 5-second blowdown test
        SequenceTimer(IN := TRUE, PT := tTestDuration);
        IF SequenceTimer.Q THEN
            CurrentState := STATE_COMPLETING;
        END_IF;
        
        // Thermodynamics Calculations
        // Isentropic Expansion Relation: M = sqrt( 2/(Gamma-1) * ( (P0/P)^((Gamma-1)/Gamma) - 1 ) )
        IF fTestSectionStaticP > 0.0 THEN
            fPressureRatio := fStagnationPressure / fTestSectionStaticP;
            fCalculatedMach := SQRT( (2.0 / (Gamma - 1.0)) * 
                               (EXPT(fPressureRatio, ((Gamma - 1.0)/Gamma)) - 1.0) );
        ELSE
            fCalculatedMach := 0.0;
        END_IF;
        
        // Velocity (V = M * a) where a = sqrt(Gamma * R * T)
        fSpeedOfSound := SQRT(Gamma * R_Specific * fTestSectionStaticT);
        fCalculatedVelocity := fCalculatedMach * fSpeedOfSound;
        
    STATE_COMPLETING:
        iPackMLState := STATE_COMPLETING;
        bTestActive := FALSE;
        
        // Safely ramp down systems
        fValvePositionCmd := fValvePositionCmd - 10.0; // Fast close
        fArcHeaterPowerCmd := 0.0;                     // Cut power
        
        IF fValvePositionCmd <= 0.0 THEN
            fValvePositionCmd := 0.0;
            CurrentState := STATE_COMPLETE;
        END_IF;
        
    STATE_COMPLETE:
        iPackMLState := STATE_COMPLETE;
        bTestComplete := TRUE;
        
        IF NOT bStart THEN
            CurrentState := STATE_IDLE;
        END_IF;
        
    STATE_ABORTING:
        iPackMLState := STATE_ABORTING;
        bTestActive := FALSE;
        
        // Emergency Shutdown: Immediately dump pressure and isolate heater
        fValvePositionCmd := 0.0;
        fArcHeaterPowerCmd := 0.0;
        
        CurrentState := STATE_ABORTED;
        
    STATE_ABORTED:
        iPackMLState := STATE_ABORTED;
        IF NOT bAbort AND NOT bStart THEN
            CurrentState := STATE_STOPPED;
        END_IF;
        
END_CASE;
END_FUNCTION_BLOCK

(*
  =============================================================================
  FB_PID
  =============================================================================
  Description:
    Standard PID Controller implementation.
  =============================================================================
*)
FUNCTION_BLOCK FB_PID
VAR_INPUT
    fSetpoint     : LREAL;
    fProcessVar   : LREAL;
    fKp           : LREAL;
    fKi           : LREAL;
    fKd           : LREAL;
END_VAR
VAR_OUTPUT
    fOutput       : LREAL;
END_VAR
VAR
    fError        : LREAL;
    fPrevError    : LREAL;
    fIntegral     : LREAL;
    fDerivative   : LREAL;
    fCycleTime    : LREAL := 0.01; (* 10ms standard assumed scan cycle *)
END_VAR

    fError := fSetpoint - fProcessVar;
    fIntegral := fIntegral + (fError * fCycleTime);
    fDerivative := (fError - fPrevError) / fCycleTime;
    
    fOutput := (fKp * fError) + (fKi * fIntegral) + (fKd * fDerivative);
    
    // Clamp output to 0-100% boundary limit
    IF fOutput > 100.0 THEN fOutput := 100.0; END_IF;
    IF fOutput < 0.0 THEN fOutput := 0.0; END_IF;
    
    fPrevError := fError;
END_FUNCTION_BLOCK
```"""

payload = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(payload) + "\\n")
print("Successfully appended to JSONL")
