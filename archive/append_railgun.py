import json
import os

prompt = """You are acting as the Principal Pulsed Power Controls Engineer for a Next-Generation Space Launch System.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "High-Energy Electromagnetic Railgun & Capacitor Bank Sequential Discharge Controller" (`FB_Railgun_LaunchSystem`).

### Technical Specifications & Engineering Rigor Required:
1. **Pulsed Power Capacitor Bank Discharge**:
   - Nanosecond-synchronized cascading trigger logic for 50 individual pulsed-power modules (PPMs), discharging $100\\text{ MJ}$ of stored capacitive energy.
   - Real-time $di/dt$ current shaping ($> 5\\text{ Mega-amps}$) to maintain a constant Lorentz force on the sliding armature without causing catastrophic plasma arcing or rail melting.
2. **Armature Velocity & Lorentz Force Tracking**:
   - Back-EMF tracking and localized B-dot magnetic field probes to compute the exact position and velocity of the projectile (accelerating to Mach 7) in real-time, feeding forward to the next stator section.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, multi-physics Maxwell's equations integration, PackML states."""

st_code = """```iec-st
(*
===================================================================================================
    FB_Railgun_LaunchSystem
    -----------------------------------------------------------------------------------------------
    Description:
    High-Energy Electromagnetic Railgun & Capacitor Bank Sequential Discharge Controller.
    Manages nanosecond-synchronized cascading trigger logic for 50 pulsed-power modules (PPMs).
    Total Energy: 100 MJ. Target Velocity: Mach 7. Peak Current: > 5 MA.
    
    PackML State Machine compliance for system management.
    Multi-physics integration: Back-EMF tracking, B-dot field probes for positional telemetry.
===================================================================================================
*)

TYPE E_PackML_State :
(
    eSTATE_IDLE             := 0,
    eSTATE_STARTING         := 1,
    eSTATE_EXECUTE          := 2,
    eSTATE_COMPLETING       := 3,
    eSTATE_COMPLETE         := 4,
    eSTATE_HOLDING          := 5,
    eSTATE_HELD             := 6,
    eSTATE_UNHOLDING        := 7,
    eSTATE_SUSPENDING       := 8,
    eSTATE_SUSPENDED        := 9,
    eSTATE_UNSUSPENDING     := 10,
    eSTATE_STOPPING         := 11,
    eSTATE_STOPPED          := 12,
    eSTATE_ABORTING         := 13,
    eSTATE_ABORTED          := 14,
    eSTATE_CLEARING         := 15
);
END_TYPE

TYPE ST_PulsedPowerModule :
STRUCT
    ChargeVoltage       : LREAL;   (* kV *)
    Capacitance         : LREAL;   (* Farads *)
    DischargeState      : BOOL;
    DischargeTimeNs     : LREAL;   (* Trigger time offset in nanoseconds *)
    CurrentFeedback     : LREAL;   (* Mega-amps *)
    Temp                : LREAL;   (* Kelvin *)
    Inductance          : LREAL;   (* Henry, localized parasitic *)
    Resistance          : LREAL;   (* Ohms *)
END_STRUCT
END_TYPE

TYPE ST_ArmatureTelemetry :
STRUCT
    Position            : LREAL;   (* meters *)
    Velocity            : LREAL;   (* m/s *)
    Acceleration        : LREAL;   (* m/s^2 *)
    BackEMF             : LREAL;   (* V *)
    BDotMagneticFlux    : LREAL;   (* Tesla/s *)
    EstimatedLorentz    : LREAL;   (* Newtons *)
END_STRUCT
END_TYPE

FUNCTION_BLOCK FB_Railgun_LaunchSystem
VAR_INPUT
    bStartCommand       : BOOL;
    bAbortCommand       : BOOL;
    bClearCommand       : BOOL;
    fTargetVelocity     : LREAL := 2382.0; (* Mach 7 in m/s at STP *)
    fTargetForce        : LREAL := 1.5E7;  (* 15 MN Target Lorentz Force *)
END_VAR

VAR_OUTPUT
    eCurrentState       : E_PackML_State := eSTATE_STOPPED;
    bReadyToLaunch      : BOOL;
    fProjectileVel      : LREAL;
    fTotalSystemCurrent : LREAL;
    fTotalEnergyJ       : LREAL;
    bCriticalFault      : BOOL;
    nActiveModules      : INT;
END_VAR

VAR
    (* Arrays for PPM and Sensors *)
    aPPMs               : ARRAY[1..50] OF ST_PulsedPowerModule;
    aBDotProbes         : ARRAY[1..50] OF LREAL; (* Array of B-Dot readings *)
    
    (* Kinematics & Electromagnetics *)
    stArmature          : ST_ArmatureTelemetry;
    fRailInductanceGrad : LREAL := 0.5E-6; (* dL/dx in H/m *)
    fRailMass           : LREAL := 15.0;   (* Projectile mass in kg *)
    fMu0                : LREAL := 1.25663706E-6; (* Permeability of free space *)
    
    (* Control Timing *)
    nCurrentModuleIdx   : INT := 1;
    fElapsedLaunchTime  : LREAL; (* seconds from trigger *)
    fDeltaT             : LREAL := 1.0E-9; (* 1 nanosecond integration step *)
    
    (* Diagnostics *)
    i                   : INT;
    fTotalCapacitance   : LREAL;
    fCalculatedDiDt     : LREAL;
END_VAR

(* 
    ========================================================================
    STATE MACHINE LOGIC (PackML)
    ======================================================================== 
*)
IF bAbortCommand THEN
    eCurrentState := eSTATE_ABORTING;
END_IF

CASE eCurrentState OF

    eSTATE_STOPPED:
        bReadyToLaunch := FALSE;
        IF bClearCommand THEN
            eCurrentState := eSTATE_CLEARING;
        END_IF
        
    eSTATE_CLEARING:
        (* Reset telemetry and module states *)
        stArmature.Position := 0.0;
        stArmature.Velocity := 0.0;
        stArmature.Acceleration := 0.0;
        fTotalSystemCurrent := 0.0;
        nCurrentModuleIdx := 1;
        bCriticalFault := FALSE;
        
        FOR i := 1 TO 50 DO
            aPPMs[i].DischargeState := FALSE;
            aPPMs[i].CurrentFeedback := 0.0;
        END_FOR
        
        eCurrentState := eSTATE_IDLE;
        
    eSTATE_IDLE:
        bReadyToLaunch := TRUE;
        IF bStartCommand AND NOT bCriticalFault THEN
            eCurrentState := eSTATE_STARTING;
        END_IF
        
    eSTATE_STARTING:
        bReadyToLaunch := FALSE;
        (* Initialize pre-launch validations *)
        fTotalEnergyJ := 0.0;
        FOR i := 1 TO 50 DO
            (* E = 1/2 C V^2 *)
            fTotalEnergyJ := fTotalEnergyJ + (0.5 * aPPMs[i].Capacitance * (aPPMs[i].ChargeVoltage * 1.0E3) * (aPPMs[i].ChargeVoltage * 1.0E3));
        END_FOR
        
        IF fTotalEnergyJ < 9.5E7 THEN (* Ensure ~100MJ is available *)
            bCriticalFault := TRUE;
            eCurrentState := eSTATE_ABORTING;
        ELSE
            eCurrentState := eSTATE_EXECUTE;
        END_IF
        
    eSTATE_EXECUTE:
        (* Sub-nanosecond resolution execution block *)
        fElapsedLaunchTime := fElapsedLaunchTime + fDeltaT;
        
        (* 1. B-Dot Probe Feedback & Telemetry Fusion *)
        (* Map discrete B-dot sensor voltages to localized magnetic flux variation *)
        stArmature.BDotMagneticFlux := aBDotProbes[nCurrentModuleIdx]; 
        
        (* 2. Back-EMF Calculation: V_emf = (dL/dx) * I * v *)
        stArmature.BackEMF := fRailInductanceGrad * (fTotalSystemCurrent * 1.0E6) * stArmature.Velocity;
        
        (* 3. Lorentz Force Calculation: F = 1/2 * (dL/dx) * I^2 *)
        stArmature.EstimatedLorentz := 0.5 * fRailInductanceGrad * (fTotalSystemCurrent * 1.0E6) * (fTotalSystemCurrent * 1.0E6);
        
        (* 4. Kinematics Update (F = ma) *)
        stArmature.Acceleration := stArmature.EstimatedLorentz / fRailMass;
        stArmature.Velocity := stArmature.Velocity + (stArmature.Acceleration * fDeltaT);
        stArmature.Position := stArmature.Position + (stArmature.Velocity * fDeltaT);
        
        fProjectileVel := stArmature.Velocity;
        
        (* 5. Sequential Cascading Trigger Logic & Current Shaping *)
        IF stArmature.Velocity >= fTargetVelocity OR stArmature.Position >= 10.0 THEN
            (* 10 meter barrel reached or target velocity achieved *)
            eCurrentState := eSTATE_COMPLETING;
        ELSE
            (* Trigger next PPM module based on armature position to maintain continuous forward momentum *)
            (* Assuming each module covers 0.2 meters of the rail length *)
            IF (stArmature.Position >= (INT_TO_LREAL(nCurrentModuleIdx) * 0.2)) AND (nCurrentModuleIdx <= 50) THEN
                
                (* di/dt limitation control: active shaping *)
                fCalculatedDiDt := (aPPMs[nCurrentModuleIdx].ChargeVoltage * 1000.0 - stArmature.BackEMF) / MAX(aPPMs[nCurrentModuleIdx].Inductance, 1.0E-9);
                
                (* Safety limits against plasma arcing: di/dt < 100 kA/us = 1E11 A/s *)
                IF fCalculatedDiDt > 1.0E11 THEN
                    (* Suppress next stage trigger until current stabilizes *)
                    aPPMs[nCurrentModuleIdx].DischargeState := FALSE;
                ELSE
                    aPPMs[nCurrentModuleIdx].DischargeState := TRUE;
                    aPPMs[nCurrentModuleIdx].CurrentFeedback := 5.0; (* Simulated MA response *)
                    nCurrentModuleIdx := nCurrentModuleIdx + 1;
                END_IF
            END_IF
        END_IF
        
        (* Aggregate total instantaneous rail current *)
        fTotalSystemCurrent := 0.0;
        nActiveModules := 0;
        FOR i := 1 TO 50 DO
            IF aPPMs[i].DischargeState THEN
                fTotalSystemCurrent := fTotalSystemCurrent + aPPMs[i].CurrentFeedback;
                nActiveModules := nActiveModules + 1;
            END_IF
        END_FOR
        
        IF fTotalSystemCurrent > 6.0 THEN (* Hard ceiling at 6 Mega-amps *)
            bCriticalFault := TRUE;
            eCurrentState := eSTATE_ABORTING;
        END_IF
        
    eSTATE_COMPLETING:
        (* Ensure complete shutoff of un-triggered banks *)
        FOR i := 1 TO 50 DO
            aPPMs[i].DischargeState := FALSE;
        END_FOR
        fTotalSystemCurrent := 0.0;
        eCurrentState := eSTATE_COMPLETE;
        
    eSTATE_COMPLETE:
        IF NOT bStartCommand THEN
            eCurrentState := eSTATE_STOPPED;
        END_IF
        
    eSTATE_ABORTING:
        (* Immediate Crowbar Circuit Dump *)
        FOR i := 1 TO 50 DO
            aPPMs[i].DischargeState := FALSE;
        END_FOR
        fTotalSystemCurrent := 0.0;
        eCurrentState := eSTATE_ABORTED;
        
    eSTATE_ABORTED:
        IF bClearCommand THEN
            eCurrentState := eSTATE_CLEARING;
        END_IF

END_CASE;
```"""

msg = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

os.makedirs('data', exist_ok=True)
with open('data/synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(msg) + '\n')
print("Successfully generated and appended to data/synthetic_generation_v3_enterprise.jsonl")
