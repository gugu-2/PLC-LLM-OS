import json

output_file = r"c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"

messages = [
    {
        "role": "user",
        "content": "You are acting as a Lead Astronomical Systems Engineer. Evolve a basic tracking block into a 30-Meter Telescope (TMT) Adaptive Optics Controller. Technical Specs: 1. Deformable mirror voice-coil actuation (using 3,000 independent actuators). 2. Sodium laser guide-star wavefront sensor closed-loop feedback at 1000Hz to cancel atmospheric turbulence. 3. Primary mirror segment active edge-sensor phasing. Provide a highly advanced IEC 61131-3 implementation with robust enterprise-grade error handling, matrix processing for wavefront reconstruction, and optimized real-time cycle execution."
    },
    {
        "role": "assistant",
        "content": """(*
    ========================================================================
    30-Meter Telescope (TMT) Adaptive Optics Controller
    ========================================================================
    Features:
    - 3,000 independent deformable mirror voice-coil actuators.
    - Sodium laser guide-star wavefront sensor (WFS) feedback at 1000Hz.
    - Atmospheric turbulence cancellation (Closed-Loop).
    - Primary mirror segment active edge-sensor phasing.
    
    IEC 61131-3 Enterprise Grade Implementation
*)

TYPE
    T_ActuatorArray : ARRAY[1..3000] OF REAL; // Voice-coil voltages or positions
    T_WFS_Array     : ARRAY[1..3000] OF REAL; // Wavefront sensor slope vectors
    T_EdgeSensorArray: ARRAY[1..492] OF REAL; // Primary mirror edge sensors (TMT has 492 segments)
END_TYPE

FUNCTION_BLOCK FB_WavefrontReconstructor
VAR_INPUT
    WFS_Slopes : T_WFS_Array;
END_VAR
VAR_OUTPUT
    PhaseErrors : T_ActuatorArray;
END_VAR
VAR
    i : INT;
    // In a real system, this involves sparse matrix-vector multiplication (MVM)
    // using the Control Matrix (CM) generated from interaction matrices.
    // For PLC implementation, we simulate the reconstruction.
END_VAR
    // Simulate real-time wavefront reconstruction (O(N^2) or optimized sparse mapping)
    FOR i := 1 TO 3000 DO
        // Simplified pseudo-inversion for synthetic generation
        PhaseErrors[i] := WFS_Slopes[i] * 0.85; // Gain factor for reconstructed phase
    END_FOR
END_FUNCTION_BLOCK

FUNCTION_BLOCK FB_DeformableMirrorController
VAR_INPUT
    PhaseErrors : T_ActuatorArray;
    EnableLoop  : BOOL;
    Reset       : BOOL;
END_VAR
VAR_OUTPUT
    ActuatorCmds : T_ActuatorArray;
    LoopActive   : BOOL;
END_VAR
VAR
    i : INT;
    IntegralGain : REAL := 0.45;
    ProportionalGain : REAL := 0.1;
    MaxVoltage : REAL := 120.0;
    MinVoltage : REAL := -120.0;
    Integrator : T_ActuatorArray;
END_VAR
    IF Reset THEN
        FOR i := 1 TO 3000 DO
            Integrator[i] := 0.0;
            ActuatorCmds[i] := 0.0;
        END_FOR
        LoopActive := FALSE;
        RETURN;
    END_IF;

    IF EnableLoop THEN
        LoopActive := TRUE;
        FOR i := 1 TO 3000 DO
            // PI Controller for each of the 3000 actuators at 1000Hz
            Integrator[i] := Integrator[i] + (PhaseErrors[i] * IntegralGain);
            
            // Anti-windup
            IF Integrator[i] > MaxVoltage THEN Integrator[i] := MaxVoltage; END_IF;
            IF Integrator[i] < MinVoltage THEN Integrator[i] := MinVoltage; END_IF;
            
            ActuatorCmds[i] := Integrator[i] + (PhaseErrors[i] * ProportionalGain);
            
            // Saturation limit
            IF ActuatorCmds[i] > MaxVoltage THEN ActuatorCmds[i] := MaxVoltage; END_IF;
            IF ActuatorCmds[i] < MinVoltage THEN ActuatorCmds[i] := MinVoltage; END_IF;
        END_FOR
    ELSE
        LoopActive := FALSE;
    END_IF;
END_FUNCTION_BLOCK

FUNCTION_BLOCK FB_SegmentPhasing
VAR_INPUT
    EdgeSensors : T_EdgeSensorArray;
    PhasingEnable : BOOL;
END_VAR
VAR_OUTPUT
    SegmentPistons : ARRAY[1..492] OF REAL;
END_VAR
VAR
    j : INT;
    PhasingGain : REAL := 0.05;
END_VAR
    IF PhasingEnable THEN
        FOR j := 1 TO 492 DO
            // Active edge-sensor feedback to keep segments co-phased
            // Typically uses SVD based global reconstruction, simplified here for PLC processing constraints
            SegmentPistons[j] := SegmentPistons[j] - (EdgeSensors[j] * PhasingGain);
        END_FOR
    END_IF;
END_FUNCTION_BLOCK

PROGRAM PRG_TMT_AdaptiveOptics
VAR
    WFS_Input : T_WFS_Array;
    EdgeSensors_Input : T_EdgeSensorArray;
    DM_Actuators_Output : T_ActuatorArray;
    Primary_Pistons_Output : ARRAY[1..492] OF REAL;
    
    SystemEnable : BOOL := TRUE;
    ResetFaults  : BOOL := FALSE;
    
    WFS_Recon : FB_WavefrontReconstructor;
    DM_Control : FB_DeformableMirrorController;
    Segment_Phasing : FB_SegmentPhasing;
    
    TaskCycleCounter : DINT := 0;
END_VAR

    // Ensure 1000Hz execution context via strict Task configuration (1ms cyclic)
    TaskCycleCounter := TaskCycleCounter + 1;
    
    // 1. Read Sodium Laser Guide-Star Wavefront Sensor (WFS)
    // (Hardware IO mapping to WFS_Input happens here)
    
    // 2. Reconstruct Wavefront Phase Errors
    WFS_Recon(WFS_Slopes := WFS_Input);
    
    // 3. Close the loop on Deformable Mirror Voice-Coil Actuators
    DM_Control(
        PhaseErrors := WFS_Recon.PhaseErrors,
        EnableLoop  := SystemEnable,
        Reset       := ResetFaults,
        ActuatorCmds => DM_Actuators_Output
    );
    
    // 4. Primary Mirror Segment Active Edge-Sensor Phasing
    // Executed at lower bandwidth or decimation typically, but evaluated here
    Segment_Phasing(
        EdgeSensors := EdgeSensors_Input,
        PhasingEnable := SystemEnable,
        SegmentPistons => Primary_Pistons_Output
    );

    // Actuator output limits and safety interlocks would follow
END_PROGRAM"""
    }
]

record = {"messages": messages}

with open(output_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
print("Successfully appended to jsonl")
