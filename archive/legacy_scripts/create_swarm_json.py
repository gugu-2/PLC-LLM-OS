import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: High-Speed Beverage Bottling Line.
Task: Invent a highly complex control scenario for this domain (e.g., PET stretch blow molding pressure curves, isovolumetric filling valve sequencing, and magnetic capping torque verification).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

st_code = """```iec-st
FUNCTION_BLOCK FB_HighSpeedBottlingLine
VAR_INPUT
    bEnable : BOOL; // Master enable for the bottling line
    bEmergencyStop : BOOL; // E-Stop condition (NC)
    rPreBlowPressureCmd : REAL; // Target pre-blow pressure (bar)
    rFinalBlowPressureCmd : REAL; // Target final stretch blow pressure (bar)
    rFillLevelTarget : REAL; // Isovolumetric fill level target (ml)
    rCapTorqueTarget : REAL; // Target magnetic capping torque (Nm)
    nLineSpeed : INT; // Bottles per minute
    bBottlePresentAtBlow : BOOL; // Sensor input
    bBottlePresentAtFill : BOOL; // Sensor input
    bBottlePresentAtCap : BOOL; // Sensor input
    rActualBlowPressure : REAL; // Feedback from pressure transducer
    rActualFillVolume : REAL; // Feedback from flow meter
    rActualCapTorque : REAL; // Feedback from capping servo
END_VAR
VAR_OUTPUT
    bBlowMoldValveOpen : BOOL; // Actuate blow mold valve
    bStretchRodExtend : BOOL; // Actuate stretch rod
    bFillValveOpen : BOOL; // Actuate filling valve
    bCapChuckEngage : BOOL; // Actuate capping chuck
    rCapTorqueCmd : REAL; // Torque command to servo drive
    bSystemFault : BOOL; // Fault flag
    nTotalBottlesProduced : DINT; // Production counter
    sCurrentState : STRING(32); // Human readable state string
END_VAR
VAR
    nStateBlowMolding : INT := 0; // State machine for blow molding
    nStateFilling : INT := 0; // State machine for isovolumetric filling
    nStateCapping : INT := 0; // State machine for capping
    tPreBlowTimer : TON; // Timer for pre-blow phase
    tFinalBlowTimer : TON; // Timer for final blow phase
    tFillDripTimer : TON; // Timer for drip reduction after filling
    bPreBlowDone : BOOL;
    bFinalBlowDone : BOOL;
    bFillComplete : BOOL;
    bCappingComplete : BOOL;
END_VAR

// Main Safety & Enable Check
IF NOT bEnable OR bEmergencyStop THEN
    bBlowMoldValveOpen := FALSE;
    bStretchRodExtend := FALSE;
    bFillValveOpen := FALSE;
    bCapChuckEngage := FALSE;
    rCapTorqueCmd := 0.0;
    bSystemFault := TRUE;
    sCurrentState := 'E-STOP OR DISABLED';
    nStateBlowMolding := 0;
    nStateFilling := 0;
    nStateCapping := 0;
    RETURN;
ELSE
    bSystemFault := FALSE;
END_IF;

// ==========================================
// STAGE 1: PET Stretch Blow Molding
// ==========================================
CASE nStateBlowMolding OF
    0: // Wait for bottle preform
        sCurrentState := 'WAIT_BLOW';
        bBlowMoldValveOpen := FALSE;
        bStretchRodExtend := FALSE;
        IF bBottlePresentAtBlow THEN
            nStateBlowMolding := 10;
        END_IF;

    10: // Pre-blow phase
        sCurrentState := 'PRE_BLOW';
        bStretchRodExtend := TRUE; // Start stretching
        IF rActualBlowPressure < rPreBlowPressureCmd THEN
            bBlowMoldValveOpen := TRUE; // Modulate open (simplified logic)
        ELSE
            bBlowMoldValveOpen := FALSE;
            tPreBlowTimer(IN := TRUE, PT := T#150MS);
            IF tPreBlowTimer.Q THEN
                tPreBlowTimer(IN := FALSE);
                nStateBlowMolding := 20;
            END_IF;
        END_IF;

    20: // Final blow phase
        sCurrentState := 'FINAL_BLOW';
        IF rActualBlowPressure < rFinalBlowPressureCmd THEN
            bBlowMoldValveOpen := TRUE; // Full pressure
        ELSE
            bBlowMoldValveOpen := FALSE;
            tFinalBlowTimer(IN := TRUE, PT := T#250MS);
            IF tFinalBlowTimer.Q THEN
                tFinalBlowTimer(IN := FALSE);
                bStretchRodExtend := FALSE; // Retract rod
                nStateBlowMolding := 30;
            END_IF;
        END_IF;

    30: // Exhaust and transfer
        sCurrentState := 'BLOW_DONE';
        IF NOT bBottlePresentAtBlow THEN
            nStateBlowMolding := 0;
        END_IF;
END_CASE;

// ==========================================
// STAGE 2: Isovolumetric Filling
// ==========================================
CASE nStateFilling OF
    0: // Wait for bottle
        bFillValveOpen := FALSE;
        IF bBottlePresentAtFill THEN
            rActualFillVolume := 0.0; // Reset virtual counter if this were an FB input accumulation
            nStateFilling := 10;
        END_IF;

    10: // Fast fill
        bFillValveOpen := TRUE;
        IF rActualFillVolume >= (rFillLevelTarget * 0.90) THEN // 90% full
            nStateFilling := 20;
        END_IF;

    20: // Fine fill (pulsing / proportional - simplified here as continuous)
        IF rActualFillVolume >= rFillLevelTarget THEN
            bFillValveOpen := FALSE;
            nStateFilling := 30;
        END_IF;

    30: // Settling and Drip Prevention
        tFillDripTimer(IN := TRUE, PT := T#100MS);
        IF tFillDripTimer.Q THEN
            tFillDripTimer(IN := FALSE);
            nStateFilling := 40;
        END_IF;

    40: // Transfer
        IF NOT bBottlePresentAtFill THEN
            nStateFilling := 0;
        END_IF;
END_CASE;

// ==========================================
// STAGE 3: Magnetic Capping Torque Verification
// ==========================================
CASE nStateCapping OF
    0: // Wait for bottle
        bCapChuckEngage := FALSE;
        rCapTorqueCmd := 0.0;
        IF bBottlePresentAtCap THEN
            nStateCapping := 10;
        END_IF;

    10: // Engage and spin
        bCapChuckEngage := TRUE;
        rCapTorqueCmd := rCapTorqueTarget;
        IF rActualCapTorque >= (rCapTorqueTarget * 0.98) THEN
            nStateCapping := 20;
        END_IF;

    20: // Hold and verify
        // Hold torque for brief duration to verify threads
        rCapTorqueCmd := rCapTorqueTarget;
        IF rActualCapTorque <= (rCapTorqueTarget * 1.05) AND rActualCapTorque >= (rCapTorqueTarget * 0.95) THEN
            nTotalBottlesProduced := nTotalBottlesProduced + 1;
            nStateCapping := 30;
        ELSE
            // Torque fault, discard bottle in a real system
            bSystemFault := TRUE;
            nStateCapping := 30;
        END_IF;

    30: // Retract
        bCapChuckEngage := FALSE;
        rCapTorqueCmd := 0.0;
        IF NOT bBottlePresentAtCap THEN
            nStateCapping := 0;
        END_IF;
END_CASE;
END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

print(f"Data saved to {filename}")
