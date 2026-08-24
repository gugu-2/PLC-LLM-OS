import json
import os

os.makedirs('data', exist_ok=True)

prompt = """You are acting as the Lead Astrodynamics Engineer for an Orbital Habitat Megaproject.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Centripetal Artificial Gravity Space Station Hub & Spoke Spin Controller" (`FB_SpaceStation_ArtificialGravity`).

### Technical Specifications & Engineering Rigor Required:
1. **Centripetal Spin-Rate Regulation**:
   - Closed-loop modulation of tangential Control Moment Gyroscopes (CMGs) to maintain a massive 500-meter diameter rotating torus at exactly $1.89\\text{ RPM}$, generating $1.0\\text{ G}$ at the outer rim.
2. **Dynamic Mass Balancing & Wobble Suppression**:
   - Real-time calculation of shifting centers of mass (e.g., as crew and massive fluid supplies move around the torus).
   - Automated pumping of water ballast between 36 circumferential trimming tanks to instantly kill any induced nutation or wobble (preventing the Dzhanibekov effect).
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, comprehensive rigid-body inertia tensor matrices, PackML states."""

code = """```iec-st
(****************************************************************************************
* FUNCTION_BLOCK FB_SpaceStation_ArtificialGravity
* 
* DESCRIPTION:
*   Centripetal Artificial Gravity Space Station Hub & Spoke Spin Controller.
*   Regulates tangential Control Moment Gyroscopes (CMGs) to maintain exactly 
*   1.89 RPM for a 500-meter diameter rotating torus (producing 1.0 G at the rim).
*   Manages dynamic mass balancing and wobble suppression by modulating ballast 
*   pumps across 36 circumferential trimming tanks to prevent nutation.
*   
* STANDARDS/COMPLIANCE:
*   - IEC 61131-3 Structured Text
*   - ISA-TR88.00.02 (PackML) State Model
*   - IEEE 754 Double Precision (LREAL) rigid body dynamics
*
* AUTHOR: Lead Astrodynamics Engineer
* DATE: 2026-08-22
****************************************************************************************)

TYPE E_PackML_State :
(
    eSTATE_IDLE := 1,
    eSTATE_STARTING := 2,
    eSTATE_EXECUTE := 3,
    eSTATE_COMPLETING := 4,
    eSTATE_COMPLETE := 5,
    eSTATE_HOLDING := 6,
    eSTATE_HELD := 7,
    eSTATE_UNHOLDING := 8,
    eSTATE_SUSPENDING := 9,
    eSTATE_SUSPENDED := 10,
    eSTATE_UNSUSPENDING := 11,
    eSTATE_STOPPING := 12,
    eSTATE_STOPPED := 13,
    eSTATE_ABORTING := 14,
    eSTATE_ABORTED := 15,
    eSTATE_CLEARING := 16
);
END_TYPE

TYPE ST_Vector3D :
STRUCT
    X : LREAL;
    Y : LREAL;
    Z : LREAL;
END_STRUCT
END_TYPE

TYPE ST_InertiaTensor :
STRUCT
    Ixx : LREAL;
    Iyy : LREAL;
    Izz : LREAL;
    Ixy : LREAL;
    Ixz : LREAL;
    Iyz : LREAL;
END_STRUCT
END_TYPE

TYPE ST_CMG_Command :
STRUCT
    TorqueDemandX : LREAL;
    TorqueDemandY : LREAL;
    TorqueDemandZ : LREAL;
    GimbalRate    : LREAL;
END_STRUCT
END_TYPE

FUNCTION_BLOCK FB_SpaceStation_ArtificialGravity
VAR_INPUT
    bStart                  : BOOL; // PackML Command
    bStop                   : BOOL; // PackML Command
    bAbort                  : BOOL; // PackML Command
    bClear                  : BOOL; // PackML Command
    
    // Sensor Inputs
    fCurrentSpinRateRPM     : LREAL; // Measured via Star Trackers and Ring Laser Gyros
    stMeasuredWobbleVector  : ST_Vector3D; // Accelerometer & IMU nutation inputs
    fCurrentRadiusRim       : LREAL := 250.0; // Torus Radius in meters
    stCurrentInertiaTensor  : ST_InertiaTensor; // Real-time updated inertia matrix based on cargo
    
    // System Parameters
    fTargetGravityG         : LREAL := 1.0; // Desired simulated gravity at the rim
    fMaxPumpRate            : LREAL := 500.0; // kg/s max flow between trimming tanks
END_VAR

VAR_OUTPUT
    eCurrentState           : E_PackML_State := eSTATE_IDLE;
    fTargetSpinRateRPM      : LREAL;
    stCMGCommand            : ST_CMG_Command;
    aBallastPumpCmd         : ARRAY[1..36] OF LREAL; // Commanded mass flow rate for 36 tanks (kg/s)
    bGravityEstablished     : BOOL;
    bNutationCritical       : BOOL;
END_VAR

VAR
    // Internal States
    fGravitationalConst     : LREAL := 9.80665;
    fSpinErrorRPM           : LREAL;
    fSpinIntegral           : LREAL := 0.0;
    
    // PID Gains for Spin Control
    Kp_Spin                 : LREAL := 1.5e6;
    Ki_Spin                 : LREAL := 0.5e5;
    Kd_Spin                 : LREAL := 2.5e6;
    fSpinDerivative         : LREAL;
    fLastSpinErrorRPM       : LREAL;
    
    // Wobble Suppression Matrix
    aTankAnglesRad          : ARRAY[1..36] OF LREAL;
    i                       : INT;
    fNutationMagnitude      : LREAL;
    
    // Time management
    fbTonExecuteTimer       : TON;
    tCycleTime              : LREAL := 0.01; // 10ms cycle
END_VAR

// -----------------------------------------------------------------------------
// INITIALIZATION
// -----------------------------------------------------------------------------
IF eCurrentState = eSTATE_IDLE THEN
    // Pre-calculate tank angular positions (36 tanks = 10 degrees apart)
    FOR i := 1 TO 36 DO
        aTankAnglesRad[i] := (INT_TO_LREAL(i - 1) * 10.0) * (3.14159265359 / 180.0);
    END_FOR;
END_IF;

// -----------------------------------------------------------------------------
// PACKML STATE MACHINE
// -----------------------------------------------------------------------------
IF bAbort THEN
    eCurrentState := eSTATE_ABORTING;
END_IF;

CASE eCurrentState OF

    eSTATE_IDLE:
        bGravityEstablished := FALSE;
        stCMGCommand.TorqueDemandX := 0.0;
        stCMGCommand.TorqueDemandY := 0.0;
        stCMGCommand.TorqueDemandZ := 0.0;
        FOR i := 1 TO 36 DO
            aBallastPumpCmd[i] := 0.0;
        END_FOR;
        
        IF bStart THEN
            eCurrentState := eSTATE_STARTING;
        END_IF;

    eSTATE_STARTING:
        // Calculate Target RPM based on desired G-force and Radius
        // a = (v^2)/r = w^2 * r
        // w = sqrt(a/r) [rad/s]
        // RPM = (w * 60) / (2 * PI)
        IF fCurrentRadiusRim > 0.0 THEN
            fTargetSpinRateRPM := (SQRT((fTargetGravityG * fGravitationalConst) / fCurrentRadiusRim) * 60.0) / (2.0 * 3.14159265359);
        ELSE
            fTargetSpinRateRPM := 0.0;
        END_IF;
        
        eCurrentState := eSTATE_EXECUTE;

    eSTATE_EXECUTE:
        IF bStop THEN
            eCurrentState := eSTATE_STOPPING;
        END_IF;
        
        // ---------------------------------------------------------------------
        // 1. CENTRIPETAL SPIN-RATE REGULATION (Main Z-Axis Rotation)
        // ---------------------------------------------------------------------
        fSpinErrorRPM := fTargetSpinRateRPM - fCurrentSpinRateRPM;
        
        // Anti-windup for integral
        IF ABS(fSpinErrorRPM) < 0.5 THEN
            fSpinIntegral := fSpinIntegral + (fSpinErrorRPM * tCycleTime);
        END_IF;
        
        fSpinDerivative := (fSpinErrorRPM - fLastSpinErrorRPM) / tCycleTime;
        fLastSpinErrorRPM := fSpinErrorRPM;
        
        // Apply Z-axis Torque via CMGs (simplified Z-axis dominant)
        stCMGCommand.TorqueDemandZ := (Kp_Spin * fSpinErrorRPM) + (Ki_Spin * fSpinIntegral) + (Kd_Spin * fSpinDerivative);
        
        // Determine if target gravity is established (within 0.5% tolerance)
        IF ABS(fSpinErrorRPM) < (fTargetSpinRateRPM * 0.005) THEN
            bGravityEstablished := TRUE;
        ELSE
            bGravityEstablished := FALSE;
        END_IF;

        // ---------------------------------------------------------------------
        // 2. DYNAMIC MASS BALANCING & WOBBLE SUPPRESSION
        // ---------------------------------------------------------------------
        // Calculate nutation magnitude on the non-spin axes (X and Y)
        fNutationMagnitude := SQRT((stMeasuredWobbleVector.X * stMeasuredWobbleVector.X) + 
                                   (stMeasuredWobbleVector.Y * stMeasuredWobbleVector.Y));
                                   
        IF fNutationMagnitude > 0.5 THEN // Threshold for critical wobble (e.g. m/s^2 accel)
            bNutationCritical := TRUE;
        ELSE
            bNutationCritical := FALSE;
        END_IF;
        
        // Calculate required cross-product torque for Active Nutation Control
        // Mapping required correction vector to 36 ballast tanks
        // Assuming X-Y plane represents the torus plane.
        // If station wobbles towards +X, we must pump ballast towards -X.
        
        FOR i := 1 TO 36 DO
            // Compute the corrective flow rate based on tank angular position
            // Projection of the wobble vector onto the tank's angle
            // Negative sign: pump mass away from the heavy side
            aBallastPumpCmd[i] := -1.0 * (
                (stMeasuredWobbleVector.X * COS(aTankAnglesRad[i])) + 
                (stMeasuredWobbleVector.Y * SIN(aTankAnglesRad[i]))
            ) * 100.0; // Gain multiplier
            
            // Saturation limits for pumps
            IF aBallastPumpCmd[i] > fMaxPumpRate THEN
                aBallastPumpCmd[i] := fMaxPumpRate;
            ELSIF aBallastPumpCmd[i] < -fMaxPumpRate THEN
                aBallastPumpCmd[i] := -fMaxPumpRate;
            END_IF;
        END_FOR;
        
        // Supplement with CMG gyroscopic stiffness on X/Y axes
        stCMGCommand.TorqueDemandX := -1.0 * stMeasuredWobbleVector.Y * stCurrentInertiaTensor.Ixx * fCurrentSpinRateRPM;
        stCMGCommand.TorqueDemandY := stMeasuredWobbleVector.X * stCurrentInertiaTensor.Iyy * fCurrentSpinRateRPM;

    eSTATE_STOPPING:
        fTargetSpinRateRPM := 0.0;
        stCMGCommand.TorqueDemandZ := -Kp_Spin * fCurrentSpinRateRPM; // Aggressive braking
        bGravityEstablished := FALSE;
        
        IF fCurrentSpinRateRPM < 0.01 THEN
            eCurrentState := eSTATE_STOPPED;
        END_IF;

    eSTATE_STOPPED:
        stCMGCommand.TorqueDemandZ := 0.0;
        FOR i := 1 TO 36 DO
            aBallastPumpCmd[i] := 0.0;
        END_FOR;
        IF bClear THEN
            eCurrentState := eSTATE_IDLE;
        END_IF;

    eSTATE_ABORTING:
        // Emergency stop - maximum braking, all pumps halt
        stCMGCommand.TorqueDemandX := 0.0;
        stCMGCommand.TorqueDemandY := 0.0;
        stCMGCommand.TorqueDemandZ := -5.0e7; // Max braking torque
        FOR i := 1 TO 36 DO
            aBallastPumpCmd[i] := 0.0;
        END_FOR;
        eCurrentState := eSTATE_ABORTED;

    eSTATE_ABORTED:
        IF bClear THEN
            eCurrentState := eSTATE_CLEARING;
        END_IF;

    eSTATE_CLEARING:
        eCurrentState := eSTATE_IDLE;

END_CASE;
END_FUNCTION_BLOCK
```"""

message_data = {
    'messages': [
        {'role': 'user', 'content': prompt},
        {'role': 'assistant', 'content': code}
    ]
}

with open('data/synthetic_generation_v3_enterprise.jsonl', 'a') as f:
    f.write(json.dumps(message_data) + '\\n')
