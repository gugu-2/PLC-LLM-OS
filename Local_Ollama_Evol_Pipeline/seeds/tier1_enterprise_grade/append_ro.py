import json

prompt = """You are acting as a Lead Process Engineer for a massive Desalination Plant. Evolve a basic pressure loop into a Reverse Osmosis (RO) High-Pressure Controller. Technical Specs: 1. Energy Recovery Device (ERD) pressure exchange synchronization. 2. Isobaric chamber valve sequencing to prevent water hammer. 3. Trans-membrane pressure (TMP) monitoring to detect membrane fouling."""

assistant_response = """As a Lead Process Engineer, the transition from a simple PID pressure loop to a comprehensive Reverse Osmosis (RO) High-Pressure Controller is one of the most critical upgrades for a massive desalination plant. We're moving from basic feedback control to a multivariable, predictive, and state-machine-driven architecture. 

The three primary challenges we must address are:
1. **ERD Synchronization**: The Energy Recovery Device (like an isobaric PX or DWEER) recycles up to 98% of the brine pressure. The high-pressure pump (HPP) and ERD booster pump must work in tandem to maintain constant membrane feed pressure despite ERD chamber switching dynamics.
2. **Valve Sequencing (Water Hammer Prevention)**: Rapid transitions in the isobaric chambers can cause destructive transients (water hammer). Precise overlapping of active/inactive chamber valves is required.
3. **TMP Monitoring**: Trans-Membrane Pressure (TMP) must be continuously calculated and normalized to detect early signs of scaling or bio-fouling, triggering preventative alarms or CIP (Clean-In-Place) sequences.

Here is the Enterprise-Grade IEC 61131-3 Structured Text implementation for this complex controller.

### IEC 61131-3 Structured Text Implementation

```iecst
(* 
   =============================================================================
   FUNCTION BLOCK: FB_RO_HighPressureController
   DESCRIPTION: 
     Advanced controller for Reverse Osmosis High-Pressure Loop integrating:
     - HPP (High Pressure Pump) and Booster Pump VFD PID control.
     - ERD (Energy Recovery Device) Isobaric Chamber Sequencing.
     - TMP (Trans-Membrane Pressure) Monitoring & Fouling Detection.
     - Water hammer prevention through ramp-rate limiting and valve overlap.
   ============================================================================= 
*)

FUNCTION_BLOCK FB_RO_HighPressureController
VAR_INPUT
    // Enable & Setpoints
    bEnable                 : BOOL;      // Controller Enable
    rFeedPressSetpoint      : REAL;      // Target RO Feed Pressure (bar)
    rMaxRampRate            : REAL;      // Maximum pressure ramp rate (bar/sec)
    
    // Process Inputs (Sensors)
    rSensFeedPress          : REAL;      // Actual RO Feed Pressure (bar)
    rSensBrinePress         : REAL;      // Brine Pressure leaving RO (bar)
    rSensPermeatePress      : REAL;      // Permeate (Product) Pressure (bar)
    rSensFeedFlow           : REAL;      // Total Feed Flow (m3/h)
    rSensTemperature        : REAL;      // Feed Water Temp (Celsius)
    
    // ERD Valve Status (Isobaric Chambers A & B)
    bValveA_InletOpened     : BOOL;
    bValveA_InletClosed     : BOOL;
    bValveB_InletOpened     : BOOL;
    bValveB_InletClosed     : BOOL;
    
    // System Parameters
    rBaselineTMP            : REAL;      // Clean membrane TMP (bar)
    rMaxTMP_Deviation       : REAL;      // Alarm threshold for fouling (bar)
END_VAR

VAR_OUTPUT
    // Pump VFD Control Signals (0.0 - 100.0 %)
    rVfdHighPressurePump    : REAL;      
    rVfdBoosterPump         : REAL;      
    
    // ERD Valve Control Signals
    bCmdValveA_Inlet        : BOOL;
    bCmdValveB_Inlet        : BOOL;
    
    // Alarms and Status
    bAlrmWaterHammerRisk    : BOOL;
    bAlrmMembraneFouling    : BOOL;
    bAlrmPressureDeviation  : BOOL;
    rCurrentTMP             : REAL;      // Calculated Normalized TMP
    iState                  : INT;       // 0:Off, 1:RampUp, 2:SyncERD, 3:Steady
END_VAR

VAR
    // PID Instances
    pidHPP                  : FB_PID_Advanced; 
    pidBooster              : FB_PID_Advanced;
    
    // State Management & Timers
    tonValveOverlap         : TON;       // Timer for valve overlap sequencing
    rInternalSetpoint       : REAL;      // Ramp-limited internal setpoint
    rPrevFeedPress          : REAL;      // For dP/dt calculation (hammer check)
    
    // Sequencing State Machine
    eErdState               : INT;       // 0:INIT, 1:CHAMBER_A_ACTIVE, 2:TRANSITION_A_TO_B, 3:CHAMBER_B_ACTIVE, 4:TRANSITION_B_TO_A
    
    // Internal calculations
    rDeltaPress             : REAL;
    rTempCorrection         : REAL;
END_VAR

(* =======================================================================
   1. PRESSURE RAMPING & SETPOINT GENERATION
   ======================================================================= *)
IF NOT bEnable THEN
    rInternalSetpoint := 0.0;
    rVfdHighPressurePump := 0.0;
    rVfdBoosterPump := 0.0;
    bCmdValveA_Inlet := FALSE;
    bCmdValveB_Inlet := FALSE;
    iState := 0;
    eErdState := 0;
    RETURN;
END_IF;

// Ramp the internal setpoint to prevent sudden shocks to the membranes
IF rInternalSetpoint < rFeedPressSetpoint THEN
    rInternalSetpoint := rInternalSetpoint + (rMaxRampRate * 0.01); // Assuming 10ms cycle
    IF rInternalSetpoint > rFeedPressSetpoint THEN
        rInternalSetpoint := rFeedPressSetpoint;
    END_IF;
ELSIF rInternalSetpoint > rFeedPressSetpoint THEN
    rInternalSetpoint := rInternalSetpoint - (rMaxRampRate * 0.01);
    IF rInternalSetpoint < rFeedPressSetpoint THEN
        rInternalSetpoint := rFeedPressSetpoint;
    END_IF;
END_IF;

(* =======================================================================
   2. HPP AND BOOSTER PUMP PID CONTROL
   ======================================================================= *)
// High Pressure Pump PID handles the bulk pressure requirement (Primary)
pidHPP.SetPoint := rInternalSetpoint;
pidHPP.ProcessVariable := rSensFeedPress;
pidHPP.Kp := 2.5; 
pidHPP.Ki := 0.8;
pidHPP.Kd := 0.1;
pidHPP();
rVfdHighPressurePump := pidHPP.Output;

// Booster Pump PID handles the pressure deficit after the ERD (Secondary/Trim)
// The target for booster is to match the HPP output pressure to ensure smooth mixing
pidBooster.SetPoint := rSensFeedPress; 
pidBooster.ProcessVariable := rSensBrinePress; // ERD input is roughly Brine pressure
pidBooster.Kp := 1.5;
pidBooster.Ki := 1.2; // Faster integral to catch ERD switching dips
pidBooster.Kd := 0.05;
pidBooster();
rVfdBoosterPump := pidBooster.Output;

(* =======================================================================
   3. ISOBARIC CHAMBER VALVE SEQUENCING (WATER HAMMER PREVENTION)
   ======================================================================= *)
// Calculate Rate of Change of Pressure (dP/dt)
rDeltaPress := rSensFeedPress - rPrevFeedPress;
rPrevFeedPress := rSensFeedPress;

// Trigger Water Hammer Risk Alarm if dP/dt is excessively high
IF ABS(rDeltaPress) > (rMaxRampRate * 1.5 * 0.01) THEN
    bAlrmWaterHammerRisk := TRUE;
ELSE
    bAlrmWaterHammerRisk := FALSE;
END_IF;

// ERD Sequencing State Machine
CASE eErdState OF
    0: (* INIT *)
        bCmdValveA_Inlet := TRUE;
        bCmdValveB_Inlet := FALSE;
        IF bValveA_InletOpened AND (rSensFeedPress > 10.0) THEN
            eErdState := 1;
        END_IF;

    1: (* CHAMBER_A_ACTIVE *)
        // Based on volumetric timing or piston stroke sensors (simulated as time here)
        tonValveOverlap(IN := TRUE, PT := T#5s);
        IF tonValveOverlap.Q THEN
            eErdState := 2;
            tonValveOverlap(IN := FALSE); // Reset timer
        END_IF;

    2: (* TRANSITION_A_TO_B *)
        // Open Valve B BEFORE closing Valve A (Make-Before-Break)
        bCmdValveB_Inlet := TRUE;
        IF bValveB_InletOpened THEN
            bCmdValveA_Inlet := FALSE; // Safe to close A
            eErdState := 3;
        END_IF;

    3: (* CHAMBER_B_ACTIVE *)
        tonValveOverlap(IN := TRUE, PT := T#5s);
        IF tonValveOverlap.Q THEN
            eErdState := 4;
            tonValveOverlap(IN := FALSE);
        END_IF;

    4: (* TRANSITION_B_TO_A *)
        // Open Valve A BEFORE closing Valve B
        bCmdValveA_Inlet := TRUE;
        IF bValveA_InletOpened THEN
            bCmdValveB_Inlet := FALSE;
            eErdState := 1;
        END_IF;
END_CASE;

(* =======================================================================
   4. TMP (TRANS-MEMBRANE PRESSURE) MONITORING
   ======================================================================= *)
// TMP = [ (FeedPress + BrinePress)/2 ] - PermeatePress
rCurrentTMP := ((rSensFeedPress + rSensBrinePress) / 2.0) - rSensPermeatePress;

// Temperature Normalization (viscosity of water changes with temperature)
// Baseline typically 25C. Correction factor ~3% per degree C.
rTempCorrection := EXP(2640.0 * (1.0/(rSensTemperature + 273.15) - 1.0/298.15));
rCurrentTMP := rCurrentTMP * rTempCorrection;

// Fouling Detection (Check deviation from Baseline)
IF (rCurrentTMP - rBaselineTMP) > rMaxTMP_Deviation THEN
    bAlrmMembraneFouling := TRUE;
ELSE
    bAlrmMembraneFouling := FALSE;
END_IF;

// Feed Pressure Deviation Alarm
IF (ABS(rSensFeedPress - rInternalSetpoint) > (rFeedPressSetpoint * 0.10)) AND (rInternalSetpoint = rFeedPressSetpoint) THEN
    bAlrmPressureDeviation := TRUE;
ELSE
    bAlrmPressureDeviation := FALSE;
END_IF;

// Determine Overall Controller State
IF rInternalSetpoint < rFeedPressSetpoint THEN
    iState := 1; // Ramp Up
ELSIF (rInternalSetpoint = rFeedPressSetpoint) AND NOT bAlrmPressureDeviation THEN
    iState := 3; // Steady State
ELSE
    iState := 2; // Stabilizing / ERD Sync active
END_IF;

END_FUNCTION_BLOCK
```

### Engineering Design Notes:
1. **Ramp Rate Limitation**: The `rMaxRampRate` ensures the HPP does not shock the membrane, which can cause compaction or mechanical failure of the membrane leaves.
2. **Dual-PID Architecture**: The system uses two PIDs. The HPP dictates total mass flow and initial pressure, while the Booster Pump acts as a trim controller matching its output pressure to the HPP output to minimize the mixing pressure differential.
3. **Make-Before-Break Valve Logic**: Water is virtually incompressible. Closing a valve before opening the next causes a massive pressure spike (Water Hammer). The `TRANSITION` states ensure the incoming chamber's valve is fully open before the outgoing chamber's valve is commanded closed.
4. **TMP Normalization**: Raw TMP is highly susceptible to feed water temperature variations. We employ an Arrhenius-based viscosity correction formula to normalize TMP to a standard 25°C, ensuring that winter/summer temperature swings do not trigger false fouling alarms."""

with open('c:\\Users\\majip\\Downloads\\LLM REASEARCH\\Local_Ollama_Evol_Pipeline\\seeds\\tier1_enterprise_grade\\synthetic_generation_v3_enterprise.jsonl', 'a') as f:
    f.write(json.dumps({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": assistant_response}]}) + '\\n')
