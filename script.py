import json
import uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: High-Frequency Linear Sorting Conveyor.
Task: Invent a highly complex control scenario for this domain (e.g., cross-belt shoe sorter timing, barcode induction gap optimization, and overflow recirculation logic).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

st_code = """```iec-st
FUNCTION_BLOCK FB_HighFreqLinearSorter
(*
    ========================================================================
    High-Frequency Linear Sorting Conveyor - Cross-Belt Shoe Sorter Control
    ========================================================================
    Description:
    This block manages high-speed parcel tracking, induction gap optimization,
    and overflow recirculation for a cross-belt shoe sorter. Utilizing 
    encoder pulses (Master Clock) and continuous barcode inputs, it tracks 
    packages along the primary conveyor belt and calculates the precise timing 
    to fire the divert mechanism.
    
    Features:
    - Barcode Induction Gap Optimization
    - Cross-belt shoe sorter divert timing
    - Overflow / Recirculation tracking logic
    ========================================================================
*)
VAR_INPUT
    xEnable            : BOOL; // Enable the sorting functionality
    xMasterClock       : BOOL; // Master encoder clock pulse for position tracking
    rBeltSpeedMs       : REAL; // Current primary belt speed in meters per second
    iBarcodeScanID     : DINT; // Scanned package identifier (0 = No Read/Invalid)
    rInductionGapMm    : REAL; // Current measured gap between consecutive packages (mm)
    xOverflowFull      : BOOL; // Indicates if the overflow/recirculation lane is full
END_VAR

VAR_OUTPUT
    xInductEnable      : BOOL; // Command to activate the induction belt for merge
    xShoeDivertCmd     : BOOL; // Command to fire the divert shoe mechanism
    xRecirculate       : BOOL; // Command to divert to recirculation lane
    rCalculatedDelayMs : REAL; // Calculated divert delay time in milliseconds (Diagnostics)
    iErrorID           : INT;  // Error code (0 = OK, 1 = FIFO Full, 2 = Overflow blocked, 3 = Gap violation)
END_VAR

VAR
    aTrackingFifo      : ARRAY[0..255] OF DINT; // FIFO for package tracking IDs
    aPositionFifo      : ARRAY[0..255] OF REAL; // FIFO for package entry positions
    iHeadIndex         : INT := 0; // FIFO Head pointer
    iTailIndex         : INT := 0; // FIFO Tail pointer
    
    rShoeDivertPosMm   : REAL := 15000.0; // Configured physical distance to primary divert (mm)
    rMinGapMm          : REAL := 250.0;   // Minimum acceptable gap for induction (mm)
    rPulseDistanceMm   : REAL := 10.0;    // Belt travel distance per encoder pulse (mm)
    
    rCurrentPositionMm : REAL := 0.0;     // Absolute tracking position accumulator
    xPrevClock         : BOOL;            // Edge detection auxiliary flag for encoder
    
    // Internal Timers & Triggers
    fbDivertPulse      : TON;             // Ensures shoe divert stays active long enough
    xDivertActive      : BOOL := FALSE;
END_VAR

// Step 1: Process Encoder Clock for Position Tracking
// Using a simple edge detection on the master encoder clock to accumulate distance.
IF xMasterClock AND NOT xPrevClock THEN
    rCurrentPositionMm := rCurrentPositionMm + rPulseDistanceMm;
    
    // Check if the oldest package in the FIFO has reached the divert location
    IF iHeadIndex <> iTailIndex THEN
        IF (rCurrentPositionMm - aPositionFifo[iTailIndex]) >= rShoeDivertPosMm THEN
            // Trigger the divert mechanism
            xDivertActive := TRUE;
            
            // Advance tail pointer (dequeue)
            iTailIndex := (iTailIndex + 1) MOD 256;
        END_IF
    END_IF
END_IF
xPrevClock := xMasterClock;

// Keep divert output high for a specific duration (e.g., 50ms) using a timer
fbDivertPulse(IN := xDivertActive, PT := T#50ms);
IF fbDivertPulse.Q THEN
    xDivertActive := FALSE; // Reset trigger after pulse duration
END_IF
xShoeDivertCmd := xDivertActive;

// Step 2: Main Operational Logic
IF xEnable THEN
    
    iErrorID := 0; // Clear errors
    
    // Evaluate induction gap optimization
    IF rInductionGapMm >= rMinGapMm THEN
        
        // Evaluate valid barcode
        IF iBarcodeScanID > 0 THEN
            
            // Validate FIFO capacity
            IF ((iHeadIndex + 1) MOD 256) <> iTailIndex THEN
                // Enqueue the new package ID and current position
                aTrackingFifo[iHeadIndex] := iBarcodeScanID;
                aPositionFifo[iHeadIndex] := rCurrentPositionMm;
                iHeadIndex := (iHeadIndex + 1) MOD 256;
                
                // Allow induction onto the main sorter
                xInductEnable := TRUE;
                xRecirculate := FALSE;
                
                // Calculate theoretical time until divert (Diagnostics)
                IF rBeltSpeedMs > 0.0 THEN
                    rCalculatedDelayMs := (rShoeDivertPosMm / (rBeltSpeedMs * 1000.0)) * 1000.0;
                END_IF
            ELSE
                iErrorID := 1; // Critical Error: Tracking FIFO Full
                xInductEnable := FALSE;
            END_IF
            
        ELSE
            // Invalid barcode read, package must be recirculated
            IF NOT xOverflowFull THEN
                xRecirculate := TRUE;
                xInductEnable := TRUE; // Induct, but flag for recirculation lane
            ELSE
                // Recirculation lane is blocked, stop induction to prevent jam
                xInductEnable := FALSE;
                xRecirculate := FALSE;
                iErrorID := 2; // Error: Overflow blocked, cannot recirculate
            END_IF
        END_IF
        
    ELSE
        // Minimum gap violated, hold induction
        xInductEnable := FALSE;
        xRecirculate := FALSE;
        iErrorID := 3; // Error: Gap violation
    END_IF
    
ELSE
    // Sorter disabled, safe state
    xInductEnable := FALSE;
    xShoeDivertCmd := FALSE;
    xRecirculate := FALSE;
    xDivertActive := FALSE;
    iErrorID := 0;
END_IF
END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

# 1. Append to data/synthetic_generation_v3_enterprise.jsonl in tier1_enterprise_grade directory
enterprise_path = r"C:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\seeds\tier1_enterprise_grade\synthetic_generation_v3_enterprise.jsonl"
os.makedirs(os.path.dirname(enterprise_path), exist_ok=True)
with open(enterprise_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")

# 2. Save JSON payload to a uniquely named file in data/swarm_raw/
# The directory is C:\Users\majip\Downloads\LLM REASEARCH\data\swarm_raw\
swarm_dir = r"C:\Users\majip\Downloads\LLM REASEARCH\data\swarm_raw"
os.makedirs(swarm_dir, exist_ok=True)
file_id = uuid.uuid4().hex[:8]
swarm_path = os.path.join(swarm_dir, f"agent_{file_id}.json")

with open(swarm_path, "w", encoding="utf-8") as f:
    json.dump(record, f)

print(f"Success! Swarm payload written to {swarm_path} and enterprise jsonl appended.")
