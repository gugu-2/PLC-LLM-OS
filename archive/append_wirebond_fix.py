import json

prompt = """You are acting as a Lead Mechatronics Engineer for a Semiconductor OSAT (Outsourced Semiconductor Assembly and Test) facility. I have a basic motion and PID controller block in IEC 61131-3. Please evolve this into a comprehensive High-Speed Wire Bonding Machine Controller function block using Structured Text. It must include:
1. Ultrasonic transducer impedance tracking and power control for gold-wire ball bonding.
2. Capillary tip Z-axis touchdown force sensing in the milligram range to prevent pad damage.
3. Voice-coil X-Y stage micro-stepping control capable of sustaining 20 bonds per second.
The controller needs a high-speed state machine that executes the complete bonding cycle (Spark/Ball Formation, Descent, First Bond, Looping, Second Bond, Tail Breaking) within a 50ms window. Provide enterprise-grade IEC 61131-3 Structured Text."""

response = """```pascal
(*
=============================================================================
FUNCTION BLOCK: FB_WireBonder_HighSpeed
DESCRIPTION:  High-speed Gold-wire Ball Bonding Controller for Semiconductor OSAT.
              Executes one complete bond cycle in <= 50ms (20 bonds/sec).
              Features: Voice-coil XY tracking, mg-resolution Z-force sensing, 
              and Ultrasonic (US) impedance tracking for bond quality.
AUTHOR:       Lead Mechatronics Engineer
VERSION:      2.0.1 (Enterprise Edition)
=============================================================================
*)

TYPE E_BondingState :
(
    BOND_INIT               := 0,
    BOND_EFO_SPARK          := 10, // Electronic Flame Off (Ball Formation)
    BOND_Z_DESCENT_FAST     := 20, // Fast approach to safe height
    BOND_Z_SEARCH           := 30, // Search speed until Touchdown
    BOND_BALL_BOND          := 40, // First bond (Pad) - US + Force + Temp
    BOND_REVERSE_MOTION     := 50, // Reverse motion for kink
    BOND_LOOP_TRAJECTORY    := 60, // XY-Z coordinated looping
    BOND_STITCH_BOND        := 70, // Second bond (Leadframe) - US + Force
    BOND_TAIL_BREAK         := 80, // Clamp close and Z up to tear wire
    BOND_MOVE_NEXT          := 90, // XY move to next die pad
    BOND_ERROR              := 999
) DINT;
END_TYPE

FUNCTION_BLOCK FB_WireBonder_HighSpeed
VAR_INPUT
    bEnable                 : BOOL;               // System enable
    bStartCycle             : BOOL;               // Trigger bond cycle
    
    // Voice-Coil XY Stage Feedback (Resolution: 0.1 um)
    lrActPosX_um            : LREAL; 
    lrActPosY_um            : LREAL;
    
    // Z-Axis Capillary Feedback (Resolution: 0.1 um)
    lrActPosZ_um            : LREAL;
    
    // Milligram Force Sensor (Z-Axis Load Cell or VCM Current estimation)
    lrTouchdownForce_mg     : LREAL; 
    
    // Ultrasonic Transducer Feedback
    lrUSImpedance_Ohms      : LREAL;              // Tracked during bonding (PLL feedback)
    
    // Target Coordinates
    lrTargetPadX_um         : LREAL;
    lrTargetPadY_um         : LREAL;
    lrTargetLeadX_um        : LREAL;
    lrTargetLeadY_um        : LREAL;
END_VAR

VAR_OUTPUT
    eState                  : E_BondingState;
    bCycleComplete          : BOOL;
    bError                  : BOOL;
    udiBondCounter          : UDINT;
    
    // Motion Commands
    lrCmdPosX_um            : LREAL;
    lrCmdPosY_um            : LREAL;
    lrCmdPosZ_um            : LREAL;
    
    // Actuator Commands
    lrCmdForceZ_mg          : LREAL;              // Force override for Z VCM
    lrUSPowerCmd_W          : LREAL;              // Ultrasonic Power Command
    bEFO_Trigger            : BOOL;               // Electronic Flame-Off Spark
    bWireClampOpen          : BOOL;               // TRUE = Open (feeding), FALSE = Closed (tearing)
END_VAR

VAR
    rtStart                 : R_TRIG;
    tStateTimer             : TON;
    tCycleTimer             : TON;
    
    // Internal Variables
    lrSearchHeight_um       : LREAL := 50.0;      // Height above pad to start search speed
    lrSafeHeight_um         : LREAL := 500.0;     // Safe Z traverse height
    lrTargetForce_mg        : LREAL;
    lrImpedancePhaseRef     : LREAL;              // Reference for Impedance PLL
    
    // Limits & Tunings
    c_MaxBondForce_mg       : LREAL := 15000.0;   // 15g max force
    c_TouchdownThresh_mg    : LREAL := 500.0;     // 0.5g touchdown detection
    c_OptimumImpedance_Ohms : LREAL := 50.0;      // Optimal acoustic match
    
    // Cycle Time Tracking
    lrLastCycleTime_ms      : LREAL;
    rtCycleDone             : R_TRIG;
END_VAR

BEGIN
    // Initialization & Triggers
    rtStart(CLK := bStartCycle);
    
    // Cycle Timeout Watchdog (50ms limit for 20Hz operation)
    tCycleTimer(IN := (eState > BOND_INIT AND eState < BOND_MOVE_NEXT), PT := T#60ms);
    IF tCycleTimer.Q THEN
        eState := BOND_ERROR;
    END_IF;

    // Fast State Machine execution (Expected cyclic interrupt: 10us - 50us)
    CASE eState OF
        
        BOND_INIT:
            bCycleComplete := FALSE;
            bError := FALSE;
            bWireClampOpen := TRUE;
            lrCmdPosZ_um := lrSafeHeight_um;
            lrCmdForceZ_mg := 0.0;
            lrUSPowerCmd_W := 0.0;
            bEFO_Trigger := FALSE;
            
            IF bEnable AND rtStart.Q THEN
                // Move XY to First Pad
                lrCmdPosX_um := lrTargetPadX_um;
                lrCmdPosY_um := lrTargetPadY_um;
                eState := BOND_EFO_SPARK;
            END_IF;

        BOND_EFO_SPARK:
            // High voltage spark to melt gold wire tail into a free-air ball
            bEFO_Trigger := TRUE;
            tStateTimer(IN := TRUE, PT := T#1ms);
            IF tStateTimer.Q THEN
                bEFO_Trigger := FALSE;
                tStateTimer(IN := FALSE);
                eState := BOND_Z_DESCENT_FAST;
            END_IF;

        BOND_Z_DESCENT_FAST:
            // Voice-coil fast approach
            lrCmdPosZ_um := lrSearchHeight_um;
            
            // Check position window
            IF ABS(lrActPosZ_um - lrSearchHeight_um) < 5.0 THEN
                eState := BOND_Z_SEARCH;
            END_IF;

        BOND_Z_SEARCH:
            // Constant low-velocity descent until force transient (touchdown)
            lrCmdPosZ_um := lrCmdPosZ_um - 1.0; // Decrement per scan (velocity profile)
            
            IF lrTouchdownForce_mg >= c_TouchdownThresh_mg THEN
                // Touchdown registered (milligram precision)
                eState := BOND_BALL_BOND;
            END_IF;

        BOND_BALL_BOND:
            // Apply specific Force and Ultrasonic Energy to form intermetallic bond
            lrCmdForceZ_mg := 8000.0; // 8 grams force
            
            // Impedance tracking: Adjust US Power based on transducer impedance shifts 
            // as the gold ball deforms and bonds to the aluminum pad
            IF lrUSImpedance_Ohms > (c_OptimumImpedance_Ohms * 1.2) THEN
                lrUSPowerCmd_W := 1.5; // Boost power if impedance rises (hardening)
            ELSE
                lrUSPowerCmd_W := 0.8; // Nominal power
            END_IF;
            
            tStateTimer(IN := TRUE, PT := T#8ms); // Extremely brief bond time
            IF tStateTimer.Q THEN
                lrUSPowerCmd_W := 0.0;
                lrCmdForceZ_mg := 0.0;
                tStateTimer(IN := FALSE);
                eState := BOND_REVERSE_MOTION;
            END_IF;

        BOND_REVERSE_MOTION:
            // Move Z up and slightly back to form the kink above the ball
            lrCmdPosZ_um := lrActPosZ_um + 150.0;
            lrCmdPosX_um := lrActPosX_um - 20.0; 
            
            IF ABS(lrActPosZ_um - lrCmdPosZ_um) < 5.0 THEN
                eState := BOND_LOOP_TRAJECTORY;
            END_IF;

        BOND_LOOP_TRAJECTORY:
            // Spline trajectory to Leadframe (Stitch Bond)
            // Coordinated X, Y, Z moves
            lrCmdPosX_um := lrTargetLeadX_um;
            lrCmdPosY_um := lrTargetLeadY_um;
            lrCmdPosZ_um := lrSearchHeight_um; 
            
            // Wait until XY settled over Leadframe
            IF ABS(lrActPosX_um - lrTargetLeadX_um) < 2.0 AND 
               ABS(lrActPosY_um - lrTargetLeadY_um) < 2.0 AND
               ABS(lrActPosZ_um - lrSearchHeight_um) < 5.0 THEN
                eState := BOND_STITCH_BOND;
            END_IF;

        BOND_STITCH_BOND:
            // Touchdown onto leadframe and perform stitch/wedge bond
            // Requires higher force, different US profile
            lrCmdForceZ_mg := 12000.0; // 12 grams
            lrUSPowerCmd_W := 1.2;
            
            tStateTimer(IN := TRUE, PT := T#6ms);
            IF tStateTimer.Q THEN
                lrUSPowerCmd_W := 0.0;
                lrCmdForceZ_mg := 0.0;
                tStateTimer(IN := FALSE);
                eState := BOND_TAIL_BREAK;
            END_IF;

        BOND_TAIL_BREAK:
            // Close clamp to grip wire, move Z up to tear wire at the stitch heel
            bWireClampOpen := FALSE; 
            lrCmdPosZ_um := lrSafeHeight_um;
            
            IF ABS(lrActPosZ_um - lrSafeHeight_um) < 10.0 THEN
                bWireClampOpen := TRUE; // Open clamp for next EFO tail
                udiBondCounter := udiBondCounter + 1;
                bCycleComplete := TRUE;
                eState := BOND_INIT; // Ready for next trigger
            END_IF;

        BOND_ERROR:
            // Halt sequence, retract Z, disable Ultrasonics
            lrUSPowerCmd_W := 0.0;
            lrCmdForceZ_mg := 0.0;
            lrCmdPosZ_um := lrSafeHeight_um;
            bError := TRUE;
            
            IF NOT bStartCycle THEN // Acknowledge error
                eState := BOND_INIT;
            END_IF;
            
    END_CASE;

END_FUNCTION_BLOCK
```"""

obj = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response}
    ]
}

with open(r'c:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\seeds\tier1_enterprise_grade\synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(obj, ensure_ascii=False) + '\n')

print("Append successful.")
