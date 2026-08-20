import os
import json
from pathlib import Path

BASE_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data")))
OUTPUT_FILE = BASE_DIR / "evol_instruct_dataset.jsonl"

def append_pair(prompt, code):
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": code}
        ]
    }
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

# ==============================================================================
# SEED 1: SIEMENS SCL MOTOR CONTROL
# ==============================================================================
s1_base_prompt = "Write a Siemens SCL function block for a 3-phase induction motor with direct-on-line starting, forward/reverse rotation, and a run-time hour counter."
s1_base_code = """
FUNCTION_BLOCK "FB_Motor_DOL_Rev"
TITLE = 'DOL Motor Control Forward/Reverse'
AUTHOR : 'Lumina'
FAMILY : 'Drives'
NAME : 'MotDOL'
VERSION : '1.0'

VAR_INPUT
    xCmdStartFwd : BOOL;   // Command to start motor forward
    xCmdStartRev : BOOL;   // Command to start motor reverse
    xCmdStop : BOOL;       // Command to stop motor
    xReset : BOOL;         // Reset runtime counter
    xInterlock : BOOL;     // General interlock (must be TRUE to run)
END_VAR

VAR_OUTPUT
    xCmdOutFwd : BOOL;     // Contactor output forward
    xCmdOutRev : BOOL;     // Contactor output reverse
    xRunning : BOOL;       // Motor is running status
    rRunHours : REAL;      // Run time in hours
END_VAR

VAR
    xRunStateFwd : BOOL;
    xRunStateRev : BOOL;
    fbTimer : TON;
    rSecondCounter : REAL;
END_VAR

BEGIN
    // Safety & Interlock override
    IF NOT xInterlock OR xCmdStop THEN
        xRunStateFwd := FALSE;
        xRunStateRev := FALSE;
    END_IF;

    // Start Forward (Ensure reverse is not active)
    IF xCmdStartFwd AND NOT xRunStateRev AND xInterlock AND NOT xCmdStop THEN
        xRunStateFwd := TRUE;
    END_IF;

    // Start Reverse (Ensure forward is not active)
    IF xCmdStartRev AND NOT xRunStateFwd AND xInterlock AND NOT xCmdStop THEN
        xRunStateRev := TRUE;
    END_IF;

    // Output Mapping
    xCmdOutFwd := xRunStateFwd;
    xCmdOutRev := xRunStateRev;
    xRunning := xRunStateFwd OR xRunStateRev;

    // Runtime calculation (Accumulate seconds, convert to hours)
    fbTimer(IN := xRunning AND NOT fbTimer.Q, PT := T#1s);
    IF fbTimer.Q THEN
        rSecondCounter := rSecondCounter + 1.0;
    END_IF;
    
    rRunHours := rSecondCounter / 3600.0;

    IF xReset THEN
        rSecondCounter := 0.0;
        rRunHours := 0.0;
    END_IF;
END_FUNCTION_BLOCK
"""

s1_m1_prompt = "Take this PLC programming task and make it significantly harder by adding one critical sub-system. Keep the same platform. Original task: Write a Siemens SCL function block for a 3-phase induction motor with direct-on-line starting, forward/reverse rotation, and a run-time hour counter."
s1_m1_code = """
FUNCTION_BLOCK "FB_Motor_DOL_Rev_Thermal"
TITLE = 'DOL Motor Control with Thermal Overload'
AUTHOR : 'Lumina'
VERSION : '2.0'

VAR_INPUT
    xCmdStartFwd : BOOL;
    xCmdStartRev : BOOL;
    xCmdStop : BOOL;
    xReset : BOOL;
    xInterlock : BOOL;
    xThermalOverload : BOOL; // TRUE = Tripped
    xContactorFeedbackFwd : BOOL; // Auxiliary contact feedback
    xContactorFeedbackRev : BOOL;
END_VAR

VAR_OUTPUT
    xCmdOutFwd : BOOL;
    xCmdOutRev : BOOL;
    xRunning : BOOL;
    xFault : BOOL;
    rRunHours : REAL;
END_VAR

VAR
    xRunStateFwd : BOOL;
    xRunStateRev : BOOL;
    fbTimer : TON;
    fbFeedbackTimerFwd : TON;
    fbFeedbackTimerRev : TON;
    rSecondCounter : REAL;
    xFault_Overload : BOOL;
    xFault_Feedback : BOOL;
END_VAR

BEGIN
    // Fault Evaluation
    IF xThermalOverload THEN
        xFault_Overload := TRUE;
    END_IF;
    
    // Contactor Discrepancy (Feedback must arrive within 2 seconds of command)
    fbFeedbackTimerFwd(IN := xRunStateFwd AND NOT xContactorFeedbackFwd, PT := T#2s);
    fbFeedbackTimerRev(IN := xRunStateRev AND NOT xContactorFeedbackRev, PT := T#2s);
    
    IF fbFeedbackTimerFwd.Q OR fbFeedbackTimerRev.Q THEN
        xFault_Feedback := TRUE;
    END_IF;
    
    // Fault Latch
    xFault := xFault_Overload OR xFault_Feedback;
    IF xReset THEN
        xFault_Overload := FALSE;
        xFault_Feedback := FALSE;
    END_IF;

    // Control Logic
    IF NOT xInterlock OR xCmdStop OR xFault THEN
        xRunStateFwd := FALSE;
        xRunStateRev := FALSE;
    END_IF;

    IF xCmdStartFwd AND NOT xRunStateRev AND NOT xFault AND xInterlock THEN
        xRunStateFwd := TRUE;
    END_IF;

    IF xCmdStartRev AND NOT xRunStateFwd AND NOT xFault AND xInterlock THEN
        xRunStateRev := TRUE;
    END_IF;

    xCmdOutFwd := xRunStateFwd;
    xCmdOutRev := xRunStateRev;
    xRunning := xContactorFeedbackFwd OR xContactorFeedbackRev;

    fbTimer(IN := xRunning AND NOT fbTimer.Q, PT := T#1s);
    IF fbTimer.Q THEN
        rSecondCounter := rSecondCounter + 1.0;
    END_IF;
    rRunHours := rSecondCounter / 3600.0;
END_FUNCTION_BLOCK
"""

def main():
    if not OUTPUT_FILE.parent.exists():
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    append_pair(s1_base_prompt, s1_base_code.strip())
    append_pair(s1_m1_prompt, s1_m1_code.strip())
    print("Injected Seed 1 Base and Mutation 1.")

if __name__ == "__main__":
    main()
