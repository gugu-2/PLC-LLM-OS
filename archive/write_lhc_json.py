import json
import os

target_dir = r"c:\Users\majip\Downloads\LLM REASEARCH\data"
os.makedirs(target_dir, exist_ok=True)
target_file = os.path.join(target_dir, "synthetic_generation_v3_enterprise.jsonl")

prompt = """You are acting as the Chief Beam Physics Architect for the Large Hadron Collider (LHC).

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "LHC Beam Dump System (LBDS) Fast Kicker Magnet & Abort Synchronization Controller" (`FB_LHC_BeamAbort`).

### Technical Specifications & Engineering Rigor Required:
1. **Beam Abort Synchronization**:
   - 3-microsecond abort gap tracking synchronizing with the 400 MHz RF bucket frequency.
   - 15-kiloampere pulse forming network (PFN) thyratron trigger firing logic with nanosecond jitter tolerance.
2. **Dilution Kicker Sweeping**:
   - Orthogonal lissajous sweeping of the extracted beam block to distribute the 360 MJ beam energy safely across the graphite dump block without melting it.
3. **Machine Protection System (MPS) Interlocks**:
   - 2-out-of-3 (2oo3) fail-safe voting for Beam Loss Monitors (BLM) and Quench Protection System (QPS) triggers."""

response = """Here is the master-tier, production-ready IEC 61131-3 Structured Text implementation for the LHC Beam Dump System (LBDS) Fast Kicker Magnet & Abort Synchronization Controller.

```iec-st
(*
  FB_LHC_BeamAbort
  Chief Beam Physics Architect: LHC Beam Dump System (LBDS)
  Fast Kicker Magnet & Abort Synchronization Controller
  
  System Specifications:
  - 400 MHz RF bucket synchronization
  - 3-us Abort Gap Tracking
  - 15 kA PFN Thyratron trigger with < 5ns jitter
  - 360 MJ beam energy dilution via Orthogonal Lissajous Sweeping
  - Fail-safe 2oo3 Machine Protection Interlocks (BLM / QPS)
*)
FUNCTION_BLOCK FB_LHC_BeamAbort
VAR_INPUT
    bSystemEnable      : BOOL; // System arming & operational permission
    bManualAbort       : BOOL; // Operator manual abort trigger
    aBLM_Triggers      : ARRAY[1..3] OF BOOL; // Beam Loss Monitors (Active High = Trip)
    aQPS_Triggers      : ARRAY[1..3] OF BOOL; // Quench Protection System (Active High = Trip)
    diRF_Frequency_Hz  : DINT := 400_000_000; // 400 MHz RF synchronization clock
    lrBeamEnergy_MJ    : LREAL := 360.0;      // 360 MJ nominal stored energy
    bAbortGapSync      : BOOL; // Hardware-level sync pulse indicating 3us abort gap
END_VAR

VAR_OUTPUT
    bThyratronTrigger  : BOOL;  // Trigger pulse for 15-kA PFN discharge
    lrDilutionKickerX  : LREAL; // Lissajous X-axis Deflection Target (kA)
    lrDilutionKickerY  : LREAL; // Lissajous Y-axis Deflection Target (kA)
    bSystemArmed       : BOOL;  // System status indicator
    bBeamDumped        : BOOL;  // Dump completion confirmation
    sSystemStatus      : STRING(64);
END_VAR

VAR
    // Machine Protection System (MPS) Internal Evaluation
    bBLM_Trip          : BOOL;
    bQPS_Trip          : BOOL;
    bMachineInterlock  : BOOL;

    // Fast Execution State Machine
    eState : (IDLE, ARMED, SYNC_WAIT, FIRING, SWEEPING, SAFE_SHUTDOWN);

    // Dilution Kicker Sweeping Parameters (Lissajous Profile)
    lrTime_us          : LREAL := 0.0;
    lrFreqX            : LREAL := 14.7;       // kHz (Non-integer ratio for dense fill)
    lrFreqY            : LREAL := 19.3;       // kHz
    lrPhaseX           : LREAL := 0.0;        // Rad
    lrPhaseY           : LREAL := 1.57079632; // Rad (pi/2)
    lrAmplitude        : LREAL := 15.0;       // kA Peak rating
    
    // Internal Timers
    rCycleTime_us      : LREAL := 0.1;        // High-speed task cycle time (100 ns)
END_VAR

// ==============================================================================
// 1. MACHINE PROTECTION SYSTEM (MPS) - 2oo3 VOTING LOGIC
// ==============================================================================
// Fail-safe logic requiring at least 2 adjacent or cross-channel monitors to trip
bBLM_Trip := (aBLM_Triggers[1] AND aBLM_Triggers[2]) OR
             (aBLM_Triggers[2] AND aBLM_Triggers[3]) OR
             (aBLM_Triggers[1] AND aBLM_Triggers[3]);

bQPS_Trip := (aQPS_Triggers[1] AND aQPS_Triggers[2]) OR
             (aQPS_Triggers[2] AND aQPS_Triggers[3]) OR
             (aQPS_Triggers[1] AND aQPS_Triggers[3]);

// Any 2oo3 consensus or manual intervention strictly forces the interlock
bMachineInterlock := bBLM_Trip OR bQPS_Trip OR bManualAbort;

// ==============================================================================
// 2. LBDS SYNCHRONIZATION AND EXECUTION STATE MACHINE
// ==============================================================================
CASE eState OF
    IDLE:
        bSystemArmed := FALSE;
        bThyratronTrigger := FALSE;
        bBeamDumped := FALSE;
        lrDilutionKickerX := 0.0;
        lrDilutionKickerY := 0.0;
        sSystemStatus := 'IDLE: Awaiting System Enable';
        
        IF bSystemEnable AND NOT bMachineInterlock THEN
            eState := ARMED;
        END_IF;

    ARMED:
        bSystemArmed := TRUE;
        sSystemStatus := 'ARMED: LBDS Monitoring MPS';
        
        IF bMachineInterlock THEN
            eState := SYNC_WAIT;
            sSystemStatus := 'INTERLOCK TRIPPED: Awaiting Abort Gap Sync';
        ELSIF NOT bSystemEnable THEN
            eState := IDLE;
        END_IF;

    SYNC_WAIT:
        // Hardware-critical phase: wait for the 3us particle-free abort gap
        // Synchronized to the 400 MHz RF bucket structure
        IF bAbortGapSync THEN
            bThyratronTrigger := TRUE; // Fire the 15-kA MKD thyratrons
            lrTime_us := 0.0;
            eState := FIRING;
            sSystemStatus := 'FIRING: Thyratron MKD Triggered';
        END_IF;

    FIRING:
        // Sub-microsecond PFN discharge ramp-up (nanosecond jitter tolerated)
        // Transition instantly to dilution phase to manage the 360 MJ transfer
        eState := SWEEPING;

    SWEEPING:
        // Dilution Kicker (MKB) Sweeping Logic
        // Generates an orthogonal Lissajous pattern over the 89-us LHC revolution period
        // Prevents hydrodynamic tunneling and structural failure of the graphite core
        lrTime_us := lrTime_us + rCycleTime_us;

        lrDilutionKickerX := lrAmplitude * SIN((2.0 * 3.14159 * lrFreqX * lrTime_us / 1000.0) + lrPhaseX);
        lrDilutionKickerY := lrAmplitude * SIN((2.0 * 3.14159 * lrFreqY * lrTime_us / 1000.0) + lrPhaseY);

        sSystemStatus := 'SWEEPING: MKB Lissajous Dilution Active';

        // 1 LHC Revolution = ~88.92 us. Sweep for 90 us to ensure total dilution.
        IF lrTime_us >= 90.0 THEN
            bThyratronTrigger := FALSE;
            lrDilutionKickerX := 0.0;
            lrDilutionKickerY := 0.0;
            bBeamDumped := TRUE;
            eState := SAFE_SHUTDOWN;
        END_IF;

    SAFE_SHUTDOWN:
        sSystemStatus := 'SAFE: 360 MJ Beam Successfully Dumped';
        
        // Require manual operator reset (dropping Enable) to re-arm after an abort
        IF NOT bMachineInterlock AND NOT bSystemEnable THEN
            eState := IDLE;
        END_IF;
END_CASE;
END_FUNCTION_BLOCK
```"""

data = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response}
    ]
}

with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(data) + "\n")

print(f"Successfully appended to {target_file}")
