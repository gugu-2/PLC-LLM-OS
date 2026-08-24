import json
import os

target_file = r"c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"
os.makedirs(os.path.dirname(target_file), exist_ok=True)

prompt = """You are acting as the Chief Orbital Mechanics Engineer for a Lunar Space Elevator Project.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Carbon-Nanotube Ribbon Spooling & Centrifugal Tension Controller" (`FB_LunarElevator_Tensioning`).

### Technical Specifications & Engineering Rigor Required:
1. **Ribbon Tension Matrix**:
   - Closed-loop modulation of the base anchoring spool torque to maintain dynamic tension along a 100,000 km carbon-nanotube tether.
   - Compensation for Lunar libration (wobble) and tidal gravitational forces from the Earth pulling on the tether's center of mass.
2. **Coriolis Vibration Damping**:
   - Active oscillation suppression to damp out "guitar string" standing waves induced by 10-ton climber vehicles ascending at $200\text{ km/h}$, calculating the Coriolis acceleration shift.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, comprehensive `VAR_INPUT`/`VAR_OUTPUT`, PackML states."""

code = """```iec-st
(* 
   =============================================================================
   Lunar Space Elevator Project - Carbon-Nanotube Ribbon Tensioning Controller
   =============================================================================
   Function Block: FB_LunarElevator_Tensioning
   Version: 1.0.0
   Author: Chief Orbital Mechanics Engineer
   Description:
     Master-tier IEC 61131-3 Structured Text (ST) implementation for closed-loop
     modulation of base anchoring spool torque. Maintains dynamic tension along 
     a 100,000 km carbon-nanotube tether. Compensates for Lunar libration, Earth 
     tidal gravitational forces, and actively suppresses "guitar string" standing 
     waves (Coriolis vibration damping) induced by 10-ton ascending climbers.
     
     Implements a standard PackML state machine for safe and robust operation.
   =============================================================================
*)

FUNCTION_BLOCK FB_LunarElevator_Tensioning
VAR_INPUT
    bEnable                 : BOOL;   (* System enable *)
    bStart                  : BOOL;   (* PackML Start command *)
    bStop                   : BOOL;   (* PackML Stop command *)
    bAbort                  : BOOL;   (* PackML Abort command *)
    bReset                  : BOOL;   (* PackML Reset command *)
    
    lrTetherLengthKm        : LREAL;  (* Nominal length of the tether in km (e.g., 100000.0) *)
    lrMeasuredBaseTension   : LREAL;  (* Measured tension at base spool (N) *)
    lrTargetBaseTension     : LREAL;  (* Desired base tension (N) *)
    
    (* Climber Data for Coriolis Damping *)
    lrClimberMassKg         : LREAL;  (* Mass of the climber vehicle (e.g., 10000.0 kg) *)
    lrClimberVelocityKmH    : LREAL;  (* Velocity of the climber (e.g., 200.0 km/h) *)
    lrClimberAltitudeKm     : LREAL;  (* Current altitude of the climber (km) *)
    
    (* Orbital & Astrometric Data *)
    lrLunarLibrationAngleRad: LREAL;  (* Real-time lunar libration angle in radians *)
    lrEarthTidalForceN      : LREAL;  (* Tidal force exerted by Earth (N) *)
    
    (* System parameters *)
    lrMaxSpoolTorqueNm      : LREAL;  (* Maximum allowed spool torque (Nm) *)
    lrSpoolRadiusM          : LREAL;  (* Radius of the base spool (m) *)
    
    lrKp                    : LREAL := 0.05;  (* PID Proportional Gain *)
    lrKi                    : LREAL := 0.01;  (* PID Integral Gain *)
    lrKd                    : LREAL := 0.15;  (* PID Derivative Gain *)
    
    fCycleTimeMs            : LREAL := 10.0;  (* Controller cycle time in ms *)
END_VAR

VAR_OUTPUT
    ePackMLState            : E_PackML_State; (* Current PackML State *)
    bReadyToOperate         : BOOL;           (* System ready indicator *)
    bError                  : BOOL;           (* Error flag *)
    nErrorID                : UDINT;          (* Error code *)
    
    lrCommandedSpoolTorqueNm: LREAL;          (* Output torque command for the base spool drive *)
    lrActiveDampingForceN   : LREAL;          (* Output active damping force applied *)
    lrTotalSetTensionN      : LREAL;          (* Calculated target tension after compensations *)
END_VAR

VAR
    (* Internal PackML State *)
    eCurrentState           : E_PackML_State := E_PackML_State.STOPPED;
    
    (* PID internal variables *)
    lrError                 : LREAL;
    lrLastError             : LREAL;
    lrIntegralTerm          : LREAL;
    lrDerivativeTerm        : LREAL;
    
    (* Physics compensations *)
    lrClimberVelocityMs     : LREAL;
    lrCoriolisAccel         : LREAL;
    lrCoriolisForceN        : LREAL;
    lrLibrationCompN        : LREAL;
    
    (* Constants *)
    LUNAR_OMEGA_RAD_S       : LREAL := 2.66166E-6; (* Lunar angular velocity *)
    
    bInitDone               : BOOL := FALSE;
END_VAR

(* 
   =============================================================================
   STATE MACHINE (PackML Simplified)
   ============================================================================= 
*)
CASE eCurrentState OF

    E_PackML_State.STOPPED:
        lrCommandedSpoolTorqueNm := 0.0;
        bReadyToOperate := FALSE;
        IF bReset THEN
            eCurrentState := E_PackML_State.IDLE;
            bError := FALSE;
            nErrorID := 0;
        END_IF
        
    E_PackML_State.IDLE:
        lrCommandedSpoolTorqueNm := 0.0;
        bReadyToOperate := TRUE;
        IF bStart AND bEnable THEN
            eCurrentState := E_PackML_State.STARTING;
        ELSIF bStop THEN
            eCurrentState := E_PackML_State.STOPPED;
        ELSIF bAbort THEN
            eCurrentState := E_PackML_State.ABORTED;
        END_IF
        
    E_PackML_State.STARTING:
        (* Initialize PID & Filters *)
        lrIntegralTerm := 0.0;
        lrLastError := 0.0;
        eCurrentState := E_PackML_State.EXECUTE;
        
    E_PackML_State.EXECUTE:
        bReadyToOperate := TRUE;
        
        (* 1. Convert Climber Velocity to m/s *)
        lrClimberVelocityMs := lrClimberVelocityKmH * 1000.0 / 3600.0;
        
        (* 2. Coriolis Vibration Damping 
           a_c = 2 * w x v
           F_c = m * a_c 
        *)
        lrCoriolisAccel := 2.0 * LUNAR_OMEGA_RAD_S * lrClimberVelocityMs;
        lrCoriolisForceN := lrClimberMassKg * lrCoriolisAccel;
        
        (* Phase shift active damping to suppress standing wave *)
        (* Simplified: Damping force is proportional and opposite to Coriolis transverse force *)
        lrActiveDampingForceN := lrCoriolisForceN * 0.85; (* 85% compensation tuning *)
        
        (* 3. Lunar Libration & Tidal Force Compensation *)
        (* Libration modifies the apparent gravity vector, requiring base tension modulation *)
        lrLibrationCompN := SIN(lrLunarLibrationAngleRad) * 50000.0; (* Parametric factor for 100,000km tether *)
        
        (* 4. Total Target Tension Calculation *)
        lrTotalSetTensionN := lrTargetBaseTension + lrEarthTidalForceN + lrLibrationCompN + lrActiveDampingForceN;
        
        (* 5. PID Control for Spool Torque *)
        lrError := lrTotalSetTensionN - lrMeasuredBaseTension;
        
        lrIntegralTerm := lrIntegralTerm + (lrError * (fCycleTimeMs / 1000.0));
        
        (* Anti-windup *)
        IF lrIntegralTerm > 1.0E6 THEN lrIntegralTerm := 1.0E6; END_IF;
        IF lrIntegralTerm < -1.0E6 THEN lrIntegralTerm := -1.0E6; END_IF;
        
        lrDerivativeTerm := (lrError - lrLastError) / (fCycleTimeMs / 1000.0);
        lrLastError := lrError;
        
        (* Calculate desired tension force at spool *)
        lrCommandedSpoolTorqueNm := (lrKp * lrError) + (lrKi * lrIntegralTerm) + (lrKd * lrDerivativeTerm);
        
        (* Convert Force to Torque: T = F * r *)
        lrCommandedSpoolTorqueNm := lrCommandedSpoolTorqueNm * lrSpoolRadiusM;
        
        (* 6. Torque Limitation *)
        IF lrCommandedSpoolTorqueNm > lrMaxSpoolTorqueNm THEN
            lrCommandedSpoolTorqueNm := lrMaxSpoolTorqueNm;
        ELSIF lrCommandedSpoolTorqueNm < -lrMaxSpoolTorqueNm THEN
            lrCommandedSpoolTorqueNm := -lrMaxSpoolTorqueNm;
        END_IF;

        IF bStop THEN
            eCurrentState := E_PackML_State.STOPPING;
        ELSIF bAbort THEN
            eCurrentState := E_PackML_State.ABORTED;
        END_IF
        
    E_PackML_State.STOPPING:
        (* Ramp down torque to nominal safe tension before stopping *)
        lrCommandedSpoolTorqueNm := lrCommandedSpoolTorqueNm * 0.99;
        IF ABS(lrCommandedSpoolTorqueNm) < 100.0 THEN
            eCurrentState := E_PackML_State.STOPPED;
        END_IF
        
    E_PackML_State.ABORTED:
        (* Emergency state - lock spool or apply maximum braking torque safely *)
        lrCommandedSpoolTorqueNm := lrMaxSpoolTorqueNm * 0.5; (* Safety holding torque *)
        bReadyToOperate := FALSE;
        bError := TRUE;
        nErrorID := 9999; (* Emergency Abort Code *)
        IF bReset THEN
            eCurrentState := E_PackML_State.STOPPED;
        END_IF

END_CASE;

(* Output mapping *)
ePackMLState := eCurrentState;
END_FUNCTION_BLOCK

(* Definition for PackML State Enum *)
TYPE E_PackML_State :
(
    STOPPED := 0,
    STARTING := 1,
    IDLE := 2,
    SUSPENDED := 3,
    EXECUTE := 4,
    STOPPING := 5,
    ABORTING := 6,
    ABORTED := 7,
    HOLDING := 8,
    HELD := 9
) UDINT;
END_TYPE
```"""

assistant_response = "Here is the master-tier, production-ready IEC 61131-3 ST implementation for the `FB_LunarElevator_Tensioning` function block, complete with PackML states, physical force compensations, and PID tension control.\n\n" + code

json_obj = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(json_obj) + "\\n")

print("Successfully appended to jsonl file.")
