import json

prompt = """You are acting as the Lead Mechatronics Engineer for an Advanced High-Speed Logistics Hub.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Magnetic Levitation (Maglev) Planar Motor Multi-Shuttle Sorting Matrix Controller" (`FB_PlanarMaglev_Sorter`).

### Technical Specifications & Engineering Rigor Required:
1. **2D Planar Motor Stator Tile Array & Halbach Array Movers**:
   - Electromagnetic field orientation across a matrix of 1000+ stator tiles to levitate and propel hundreds of individual passive mover shuttles simultaneously.
   - Dynamic 6-DOF force/torque vector calculation (Lorentz force) for each shuttle, resolving X, Y, Z translation and Pitch, Roll, Yaw rotation for cornering and collision avoidance.
2. **High-Speed Anti-Slosh Payload Dynamics**:
   - Adaptive jerk limiting ($100\text{ m/s}^3$) and feedforward input shaping (Zero Vibration Derivative - ZVD) applied to each mover's trajectory to prevent liquid splashing or fragile goods damage during $5\text{ G}$ accelerations.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, comprehensive `VAR_INPUT`/`VAR_OUTPUT`, matrix equations for multi-agent swarm scheduling, PackML states.

Output a complete, valid JSON object with {"messages": [{"role": "user", "content": "Mega-prompt description"}, {"role": "assistant", "content": "Full raw Structured Text code inside ```iec-st```"}]}.
Append this JSON directly to `data/synthetic_generation_v3_enterprise.jsonl` using a safe append script."""

st_code = """```iec-st
FUNCTION_BLOCK FB_PlanarMaglev_Sorter
(* 
   Magnetic Levitation (Maglev) Planar Motor Multi-Shuttle Sorting Matrix Controller
   Features:
   - 2D Planar Motor Stator Tile Array & Halbach Array Movers (6-DOF Force/Torque calculation)
   - High-Speed Anti-Slosh Payload Dynamics (ZVD input shaping, Adaptive jerk limiting)
   - PackML state machine for matrix operations
   - Collision avoidance and swarm scheduling
*)

VAR_INPUT
    bEnable          : BOOL; (* Enable Matrix Controller *)
    bStart           : BOOL; (* Start sorting operation *)
    bStop            : BOOL; (* Stop sorting operation *)
    bAbort           : BOOL; (* Abort operations - Emergency Stop *)
    bClear           : BOOL; (* Clear faults and reset *)
    fMaxAccel        : LREAL := 49.05; (* Max Acceleration (m/s^2), 5G *)
    fMaxJerk         : LREAL := 100.0; (* Adaptive Jerk Limiting (m/s^3) *)
    nNumMovers       : UINT; (* Number of active movers (0 to MAX_MOVERS) *)
    fPayloadFreqHz   : LREAL; (* Payload natural frequency for ZVD shaper (Hz) *)
    fPayloadDamping  : LREAL; (* Payload damping ratio (zeta) *)
END_VAR

VAR_OUTPUT
    ePackMLState     : E_PackML_States := ePackML_Stopped; (* Current PackML State *)
    bMatrixReady     : BOOL; (* Stator matrix energized and ready *)
    bFault           : BOOL; (* Fault present *)
    nErrorID         : UDINT; (* Fault code *)
    fTotalPowerkW    : LREAL; (* Total power consumption of the matrix *)
END_VAR

VAR_IN_OUT
    aMovers          : ARRAY[1..MAX_MOVERS] OF ST_MoverState; (* State data for all active movers *)
    aStatorTiles     : ARRAY[1..MAX_TILES_X, 1..MAX_TILES_Y] OF ST_StatorTile; (* Stator tile array *)
    aTrajectories    : ARRAY[1..MAX_MOVERS] OF ST_TrajectoryPlan; (* Planned paths for movers *)
END_VAR

VAR CONSTANT
    MAX_MOVERS       : UINT := 250;
    MAX_TILES_X      : UINT := 40;
    MAX_TILES_Y      : UINT := 25;
    MU_0             : LREAL := 1.2566370614E-6; (* Vacuum permeability *)
    LORENTZ_CONST    : LREAL := 0.85; (* Simplification constant for stator field *)
END_VAR

VAR
    i, j, k          : UINT;
    fTimePeriod      : LREAL := 0.001; (* 1ms Task cycle *)
    
    (* PackML Variables *)
    eCommand         : E_PackML_Commands;
    
    (* Anti-Slosh ZVD Shaper variables *)
    fOmega_n         : LREAL;
    fK_ZVD           : LREAL;
    fT_d             : LREAL;
    fA1, fA2, fA3    : LREAL;
    fT1, fT2, fT3    : LREAL;
    
    (* Kinematics and Dynamics *)
    fForceVec        : ARRAY[1..6] OF LREAL; (* Fx, Fy, Fz, Tx, Ty, Tz *)
    fTargetPos       : ARRAY[1..3] OF LREAL;
    fCurrentPos      : ARRAY[1..3] OF LREAL;
    fPosError        : ARRAY[1..3] OF LREAL;
    
    (* Collision Avoidance *)
    fDistSq          : LREAL;
    fMinSafeDistSq   : LREAL := 0.04; (* 200mm squared safe distance *)
    
    (* Temporary variables for calculations *)
    fBx, fBy, fBz    : LREAL;
    fCurrent         : LREAL;
    fTemp            : LREAL;
END_VAR

(* 
   ========================================================================================
   PackML State Machine Implementation
   ======================================================================================== 
*)
IF bAbort THEN
    ePackMLState := ePackML_Aborted;
    bMatrixReady := FALSE;
ELSIF bStop THEN
    IF ePackMLState = ePackML_Execute OR ePackMLState = ePackML_Starting THEN
        ePackMLState := ePackML_Stopping;
    END_IF;
END_IF;

CASE ePackMLState OF
    ePackML_Stopped:
        IF bClear THEN
            bFault := FALSE;
            nErrorID := 0;
            ePackMLState := ePackML_Clearing;
        ELSIF bStart AND NOT bFault THEN
            ePackMLState := ePackML_Starting;
        END_IF;

    ePackML_Clearing:
        bFault := FALSE;
        nErrorID := 0;
        ePackMLState := ePackML_Stopped;
        
    ePackML_Starting:
        (* Energize Stator Matrix, check diagnostics *)
        bMatrixReady := TRUE;
        
        (* Calculate ZVD Input Shaper coefficients based on payload frequency *)
        IF fPayloadFreqHz > 0.0 THEN
            fOmega_n := 2.0 * 3.1415926535 * fPayloadFreqHz;
            fK_ZVD := EXP(-(fPayloadDamping * 3.1415926535) / SQRT(1.0 - fPayloadDamping*fPayloadDamping));
            fT_d := 3.1415926535 / (fOmega_n * SQRT(1.0 - fPayloadDamping*fPayloadDamping));
            
            fA1 := 1.0 / (1.0 + 2.0*fK_ZVD + fK_ZVD*fK_ZVD);
            fA2 := (2.0 * fK_ZVD) / (1.0 + 2.0*fK_ZVD + fK_ZVD*fK_ZVD);
            fA3 := (fK_ZVD * fK_ZVD) / (1.0 + 2.0*fK_ZVD + fK_ZVD*fK_ZVD);
            
            fT1 := 0.0;
            fT2 := fT_d;
            fT3 := 2.0 * fT_d;
        ELSE
            (* Disable ZVD if frequency is zero *)
            fA1 := 1.0; fA2 := 0.0; fA3 := 0.0;
        END_IF;
        
        ePackMLState := ePackML_Execute;

    ePackML_Execute:
        IF NOT bEnable THEN
            ePackMLState := ePackML_Holding;
        END_IF;
        
        (* Main Execute Loop for Mover Matrix *)
        fTotalPowerkW := 0.0;
        
        FOR i := 1 TO nNumMovers DO
            IF aMovers[i].bActive THEN
                
                (* 1. Anti-Slosh Payload Dynamics (ZVD Shaping on Target Position) *)
                (* ZVD requires convolving the impulse sequence with the desired trajectory *)
                (* Simplification: Apply moving average or pre-computed ZVD delayed inputs *)
                aMovers[i].fTargetX_Shaped := fA1 * aTrajectories[i].fTargetX + 
                                              fA2 * aMovers[i].fDelayQueueX[1] + 
                                              fA3 * aMovers[i].fDelayQueueX[2];
                                              
                aMovers[i].fTargetY_Shaped := fA1 * aTrajectories[i].fTargetY + 
                                              fA2 * aMovers[i].fDelayQueueY[1] + 
                                              fA3 * aMovers[i].fDelayQueueY[2];
                
                (* Shift delay queues (simplified indexing for ZVD periods) *)
                aMovers[i].fDelayQueueX[2] := aMovers[i].fDelayQueueX[1];
                aMovers[i].fDelayQueueX[1] := aTrajectories[i].fTargetX;
                aMovers[i].fDelayQueueY[2] := aMovers[i].fDelayQueueY[1];
                aMovers[i].fDelayQueueY[1] := aTrajectories[i].fTargetY;

                (* 2. Swarm Collision Avoidance (Repulsive Force Fields) *)
                FOR j := 1 TO nNumMovers DO
                    IF i <> j AND aMovers[j].bActive THEN
                        fDistSq := EXPT(aMovers[i].fCurrentX - aMovers[j].fCurrentX, 2.0) + 
                                   EXPT(aMovers[i].fCurrentY - aMovers[j].fCurrentY, 2.0);
                                   
                        IF fDistSq < fMinSafeDistSq AND fDistSq > 0.0001 THEN
                            (* Apply repulsive vector modifier to trajectory to skirt collision *)
                            fTemp := fMinSafeDistSq / fDistSq;
                            aMovers[i].fTargetX_Shaped := aMovers[i].fTargetX_Shaped + (aMovers[i].fCurrentX - aMovers[j].fCurrentX) * fTemp * 0.1;
                            aMovers[i].fTargetY_Shaped := aMovers[i].fTargetY_Shaped + (aMovers[i].fCurrentY - aMovers[j].fCurrentY) * fTemp * 0.1;
                        END_IF;
                    END_IF;
                END_FOR;
                
                (* 3. Adaptive Jerk Limiting Profile Generation *)
                (* Limit delta acceleration to fMaxJerk *)
                fPosError[1] := aMovers[i].fTargetX_Shaped - aMovers[i].fCurrentX;
                fPosError[2] := aMovers[i].fTargetY_Shaped - aMovers[i].fCurrentY;
                fPosError[3] := 0.015; (* Target Z levitation height (15mm) *)
                
                (* Basic PID with Jerk clamping for kinematics *)
                aMovers[i].fReqVelX := LIMIT(-10.0, fPosError[1] * aMovers[i].fKp, 10.0);
                aMovers[i].fReqVelY := LIMIT(-10.0, fPosError[2] * aMovers[i].fKp, 10.0);
                
                (* Calculate required accelerations with Jerk limits *)
                aMovers[i].fReqAccelX := LIMIT(-fMaxAccel, (aMovers[i].fReqVelX - aMovers[i].fCurrentVelX) / fTimePeriod, fMaxAccel);
                aMovers[i].fReqAccelY := LIMIT(-fMaxAccel, (aMovers[i].fReqVelY - aMovers[i].fCurrentVelY) / fTimePeriod, fMaxAccel);
                
                IF ABS(aMovers[i].fReqAccelX - aMovers[i].fLastAccelX) / fTimePeriod > fMaxJerk THEN
                    IF aMovers[i].fReqAccelX > aMovers[i].fLastAccelX THEN
                        aMovers[i].fReqAccelX := aMovers[i].fLastAccelX + (fMaxJerk * fTimePeriod);
                    ELSE
                        aMovers[i].fReqAccelX := aMovers[i].fLastAccelX - (fMaxJerk * fTimePeriod);
                    END_IF;
                END_IF;
                aMovers[i].fLastAccelX := aMovers[i].fReqAccelX;
                
                (* 4. 6-DOF Lorentz Force/Torque Vector Calculation *)
                (* F = I * (L x B)  - simplified for planar Halbach arrays *)
                (* Calculate required Lorentz forces for X, Y propulsion and Z levitation *)
                fForceVec[1] := aMovers[i].fMass * aMovers[i].fReqAccelX; (* Fx *)
                fForceVec[2] := aMovers[i].fMass * aMovers[i].fReqAccelY; (* Fy *)
                fForceVec[3] := (aMovers[i].fMass * 9.81) + ((0.015 - aMovers[i].fCurrentZ) * aMovers[i].fKz); (* Fz Levitation *)
                
                (* Pitch/Roll torque to counteract acceleration tipping (cornering) *)
                fForceVec[4] := -fForceVec[2] * aMovers[i].fCG_Height; (* Tx - Roll *)
                fForceVec[5] := fForceVec[1] * aMovers[i].fCG_Height;  (* Ty - Pitch *)
                fForceVec[6] := 0.0; (* Tz - Yaw (assume locked to grid unless turning explicitly) *)
                
                (* 5. Map Forces to Stator Matrix Currents *)
                (* Determine which stator tiles the mover is currently over *)
                k := LREAL_TO_UINT(aMovers[i].fCurrentX / 0.1); (* Assuming 100mm tiles *)
                j := LREAL_TO_UINT(aMovers[i].fCurrentY / 0.1);
                
                k := LIMIT(1, k, MAX_TILES_X);
                j := LIMIT(1, j, MAX_TILES_Y);
                
                (* Inject required current vector into Stator Matrix DQs *)
                (* Pseudo-inverse mapping of force to coil currents *)
                fCurrent := SQRT(EXPT(fForceVec[1], 2) + EXPT(fForceVec[2], 2) + EXPT(fForceVec[3], 2)) / LORENTZ_CONST;
                
                aStatorTiles[k, j].fCommandedCurrentU := fCurrent * SIN(aMovers[i].fPhaseAngle);
                aStatorTiles[k, j].fCommandedCurrentV := fCurrent * SIN(aMovers[i].fPhaseAngle + 2.0944); (* +120 deg *)
                aStatorTiles[k, j].fCommandedCurrentW := fCurrent * SIN(aMovers[i].fPhaseAngle + 4.1888); (* +240 deg *)
                
                (* Sum power for monitoring *)
                fTotalPowerkW := fTotalPowerkW + (EXPT(fCurrent, 2) * aStatorTiles[k, j].fCoilResistance) / 1000.0;
                
            END_IF;
        END_FOR;

    ePackML_Holding:
        IF bEnable THEN
            ePackMLState := ePackML_Execute;
        END_IF;

    ePackML_Stopping:
        bMatrixReady := FALSE;
        ePackMLState := ePackML_Stopped;

    ePackML_Aborted:
        bMatrixReady := FALSE;
        (* Dump all stator currents immediately for E-Stop (drop to landing pads) *)
        FOR i := 1 TO MAX_TILES_X DO
            FOR j := 1 TO MAX_TILES_Y DO
                aStatorTiles[i, j].fCommandedCurrentU := 0.0;
                aStatorTiles[i, j].fCommandedCurrentV := 0.0;
                aStatorTiles[i, j].fCommandedCurrentW := 0.0;
            END_FOR;
        END_FOR;
        IF bClear THEN
            ePackMLState := ePackML_Clearing;
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

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")

print("Successfully appended to data/synthetic_generation_v3_enterprise.jsonl")

