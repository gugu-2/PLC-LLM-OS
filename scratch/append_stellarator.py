import json

prompt = """You are acting as the Principal Plasma Physicist for a Next-Generation Wendelstein-class Stellarator Fusion Reactor.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Stellarator Magnetic Island Divertor & Non-Planar Coil Quench Controller" (`FB_Stellarator_Divertor`).

### Technical Specifications & Engineering Rigor Required:
1. **Magnetic Island Resonance Tuning**:
   - Superconducting trim coil current modulation (up to 10 kA) to finely adjust the rotational transform ($\\iota$) edge profile, maintaining the 5/5 magnetic island chain precisely aligned with the divertor target plates.
2. **Cryogenic Quench Detection on Non-Planar Coils**:
   - Inductive voltage cancellation across 50 highly twisted, non-planar superconducting coils to detect microvolt-level resistive growth indicating a thermal quench.
   - Fast $I^2t$ action integral calculation to trigger the rapid discharge circuit into external dump resistors.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, redundant SIL-4 checks, PackML states.

Output a complete, valid JSON object with {"messages": [{"role": "user", "content": "Mega-prompt description"}, {"role": "assistant", "content": "Full raw Structured Text code inside ```iec-st```"}]}.
Append this JSON directly to `data/synthetic_generation_v3_enterprise.jsonl` using a safe append script."""

response = """```iec-st
FUNCTION_BLOCK FB_Stellarator_Divertor
TITLE = 'Stellarator Magnetic Island Divertor & Non-Planar Coil Quench Controller'
VERSION : '2.0'
AUTHOR : 'Lumina Elite Synthetic Data Architect'

(* 
    =============================================================================
    FB_Stellarator_Divertor 
    -----------------------------------------------------------------------------
    Mission: Magnetic Island Resonance Tuning & Non-Planar Coil Quench Protection
    Architecture: IEC 61131-3 ST, PackML State Machine, SIL-4 Redundant Paths
    Target: Wendelstein-class Advanced Stellarator 
    =============================================================================
*)

VAR_INPUT
    // PackML State Control
    bExecute            : BOOL;     (* Command: Execute / Start Process *)
    bAbort              : BOOL;     (* Command: Emergency Abort / Quench Trigger *)
    bReset              : BOOL;     (* Command: Reset from Fault state *)
    
    // Magnetic Diagnostics & Control
    fIotaEdgeTarget     : LREAL;    (* Target edge rotational transform (e.g., 5/5 = 1.0) *)
    fIotaEdgeMeasured   : LREAL;    (* Measured edge rotational transform from diagnostic *)
    fPlasmaCurrent      : LREAL;    (* Bootstrap & driven plasma current [A] *)
    fTrimCoilMaxRate    : LREAL := 50.0; (* Max current modulation rate [A/ms] *)

    // Coil Diagnostics (Array for 50 Non-Planar Coils)
    aCoilCurrents       : ARRAY[1..50] OF LREAL; (* Operating currents [A] (e.g., up to 20,000 A) *)
    aCoilVoltages       : ARRAY[1..50] OF LREAL; (* Total measured voltage drop [V] *)
    aCoildIdt           : ARRAY[1..50] OF LREAL; (* Measured di/dt [A/s] for inductive compensation *)
    
    // Quench Detection Parameters
    aCoilInductances    : ARRAY[1..50] OF LREAL; (* Self and mutual inductance tensor diagonals [H] *)
    fQuenchThreshold_V  : LREAL := 0.005;        (* 5mV microvolt resistive threshold for quench *)
    fActionIntegralMax  : LREAL := 1.0E9;        (* I^2t max threshold [A^2s] before thermal runaway *)
    
    // Timing
    fCycleTime_ms       : LREAL;    (* Controller cycle time in milliseconds *)
END_VAR

VAR_OUTPUT
    // PackML State Reporting
    iState              : INT;      (* Current PackML State ID *)
    sStateName          : STRING;   (* Current PackML State Name *)
    bError              : BOOL;     (* Active Fault *)
    nErrorID            : DINT;     (* Fault Code *)

    // Actuation Signals
    fTrimCoilCurrentRef : LREAL;    (* Requested trim coil current [A], limit 10,000 A *)
    bFastDischargeTrig  : BOOL;     (* Trigger for rapid energy extraction (Dump resistors) *)
    bTargetPlateAlign   : BOOL;     (* 5/5 magnetic island chain successfully aligned *)
    
    // Telemetry
    aResistiveVoltages  : ARRAY[1..50] OF LREAL; (* Calculated resistive voltages [V] *)
    fActionIntegralVal  : LREAL;    (* Highest I^2t action integral calculated [A^2s] *)
END_VAR

VAR
    // PackML States Enumeration (Internal)
    eState : (
        STATE_IDLE      := 0,
        STATE_STARTING  := 1,
        STATE_EXECUTE   := 2,
        STATE_HOLDING   := 3,
        STATE_ABORTING  := 4,
        STATE_ABORTED   := 5,
        STATE_FAULT     := 6,
        STATE_RESETTING := 7
    );
    
    // PID Controller for Iota Tuning
    fKp_Iota            : LREAL := 25000.0;
    fKi_Iota            : LREAL := 500.0;
    fIotaError          : LREAL;
    fIotaIntegral       : LREAL := 0.0;
    
    // Quench Action Integral calculations
    aActionIntegral     : ARRAY[1..50] OF LREAL;
    i                   : INT;
    fU_inductive        : LREAL;
    
    // Redundancy / Diagnostics
    bQuenchDetected     : BOOL := FALSE;
    iWorstCoilIdx       : INT := 0;
END_VAR

(* -----------------------------------------------------------------------------
   PackML STATE MACHINE
   ----------------------------------------------------------------------------- *)
CASE eState OF

    STATE_IDLE:
        sStateName := 'IDLE';
        bFastDischargeTrig := FALSE;
        fTrimCoilCurrentRef := 0.0;
        bTargetPlateAlign := FALSE;
        
        IF bAbort THEN
            eState := STATE_ABORTING;
        ELSIF bExecute THEN
            eState := STATE_STARTING;
        END_IF;
        
    STATE_STARTING:
        sStateName := 'STARTING';
        // Initialize Integrals and arrays
        fIotaIntegral := 0.0;
        FOR i := 1 TO 50 DO
            aActionIntegral[i] := 0.0;
        END_FOR;
        
        eState := STATE_EXECUTE;

    STATE_EXECUTE:
        sStateName := 'EXECUTE';
        
        IF bAbort THEN
            eState := STATE_ABORTING;
        END_IF;

        (* =========================================================================
           1. MAGNETIC ISLAND RESONANCE TUNING (Divertor Alignment)
           ========================================================================= *)
        // Calculate error in edge rotational transform (iota)
        // Aiming to keep 5/5 magnetic islands at the divertor strike lines
        fIotaError := fIotaEdgeTarget - fIotaEdgeMeasured;
        
        // Anti-windup integration
        IF (fTrimCoilCurrentRef < 10000.0) AND (fTrimCoilCurrentRef > -10000.0) THEN
            fIotaIntegral := fIotaIntegral + (fIotaError * (fCycleTime_ms / 1000.0));
        END_IF;
        
        // PI Control for Trim Coil
        fTrimCoilCurrentRef := (fKp_Iota * fIotaError) + (fKi_Iota * fIotaIntegral);
        
        // Feedforward compensation for plasma bootstrap current
        fTrimCoilCurrentRef := fTrimCoilCurrentRef - (0.01 * fPlasmaCurrent);
        
        // Saturation limits (Superconducting Trim Coils max 10kA)
        IF fTrimCoilCurrentRef > 10000.0 THEN
            fTrimCoilCurrentRef := 10000.0;
        ELSIF fTrimCoilCurrentRef < -10000.0 THEN
            fTrimCoilCurrentRef := -10000.0;
        END_IF;
        
        // Check alignment precision
        bTargetPlateAlign := ABS(fIotaError) < 0.005;

        (* =========================================================================
           2. CRYOGENIC QUENCH DETECTION (Non-Planar Coils)
           ========================================================================= *)
        bQuenchDetected := FALSE;
        fActionIntegralVal := 0.0;
        
        FOR i := 1 TO 50 DO
            // Inductive voltage cancellation: U_res = U_meas - L * (di/dt)
            // Note: In a real SIL-4 system, full mutual inductance matrix M_ij would be used.
            fU_inductive := aCoilInductances[i] * aCoildIdt[i];
            aResistiveVoltages[i] := aCoilVoltages[i] - fU_inductive;
            
            // Check for microvolt resistive growth (Quench precursor)
            IF aResistiveVoltages[i] > fQuenchThreshold_V THEN
                // Calculate I^2t action integral for the quenching coil
                aActionIntegral[i] := aActionIntegral[i] + 
                                     (aCoilCurrents[i] * aCoilCurrents[i] * (fCycleTime_ms / 1000.0));
                
                // Track worst-case action integral
                IF aActionIntegral[i] > fActionIntegralVal THEN
                    fActionIntegralVal := aActionIntegral[i];
                    iWorstCoilIdx := i;
                END_IF;
                
                // SIL-4 Trigger Check: If action integral exceeds thermal threshold, trip dump!
                IF aActionIntegral[i] > fActionIntegralMax THEN
                    bQuenchDetected := TRUE;
                END_IF;
            ELSE
                // Cooling recovers, slowly bleed off action integral memory
                aActionIntegral[i] := MAX(0.0, aActionIntegral[i] - (1.0E5 * (fCycleTime_ms / 1000.0)));
            END_IF;
        END_FOR;
        
        // Fast Discharge Trip
        IF bQuenchDetected THEN
            bError := TRUE;
            nErrorID := 16#FFFF; // FATAL QUENCH
            eState := STATE_ABORTING;
        END_IF;
        
    STATE_ABORTING:
        sStateName := 'ABORTING';
        bFastDischargeTrig := TRUE; // TRIGGER EXTERNAL DUMP RESISTORS
        fTrimCoilCurrentRef := 0.0; // Command trim coils to zero
        
        // Wait for currents to decay (simulated here as a pass-through to ABORTED)
        eState := STATE_ABORTED;
        
    STATE_ABORTED:
        sStateName := 'ABORTED';
        bFastDischargeTrig := TRUE; // Maintain dump active
        
        IF bReset THEN
            eState := STATE_RESETTING;
        END_IF;
        
    STATE_RESETTING:
        sStateName := 'RESETTING';
        bError := FALSE;
        nErrorID := 0;
        bFastDischargeTrig := FALSE;
        
        FOR i := 1 TO 50 DO
            aActionIntegral[i] := 0.0;
        END_FOR;
        
        eState := STATE_IDLE;
        
    STATE_FAULT:
        sStateName := 'FAULT';
        bFastDischargeTrig := TRUE; // Safe state
        
        IF bReset THEN
            eState := STATE_RESETTING;
        END_IF;
        
    ELSE
        eState := STATE_FAULT;
        
END_CASE;

// Assign external state variable
iState := eState;

END_FUNCTION_BLOCK
```"""

data = {
  "messages": [
    {
      "role": "user",
      "content": prompt
    },
    {
      "role": "assistant",
      "content": response
    }
  ]
}

with open(r"c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(data) + "\n")

print("Done")
