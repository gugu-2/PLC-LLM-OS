import json
import os

data = {
    "messages": [
        {
            "role": "user",
            "content": """You are acting as the Principal Grid Protection Engineer for an Advanced Super-Grid Authority...

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Resistive Superconducting Fault Current Limiter (SFCL) & Quench Protection Controller" (`FB_Grid_SFCL_Protection`).

### Technical Specifications & Engineering Rigor Required:
1. **Superconducting State Monitoring (YBCO Tapes)**:
   - Nanosecond-level monitoring of the voltage drop across hundreds of YBCO (Yttrium Barium Copper Oxide) high-temperature superconducting tapes submerged in liquid nitrogen ($-196^\circ\\text{C}$).
   - Operating at $138\\text{ kV}$ with exactly zero electrical resistance under normal grid conditions.
2. **Ultra-Fast Quench Detection & Current Limiting**:
   - Detection of a massive downstream grid short-circuit fault ($> 50\\text{ kA}$).
   - The immense fault current inherently exceeds the critical current ($I_c$) of the superconductor, causing it to "quench" (instantaneously phase-transitioning from zero resistance to a highly resistive normal state) in $< 2\\text{ milliseconds}$.
   - The controller must instantly detect this voltage spike and coordinate bypass vacuum interrupter switches to limit the let-through energy ($I^2t$) without completely blowing out the expensive superconducting tapes.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, comprehensive `VAR_INPUT`/`VAR_OUTPUT`, superconductor quenching physics math, PackML states.

Output a complete, valid JSON object with {"messages": [{"role": "user", "content": "Mega-prompt description"}, {"role": "assistant", "content": "Full raw Structured Text code inside ```iec-st```"}]}. """
        },
        {
            "role": "assistant",
            "content": """```iec-st
(*
=========================================================================================
Function Block: FB_Grid_SFCL_Protection
Description:    Master-tier, production-ready IEC 61131-3 Structured Text (ST) 
                implementation for the Resistive Superconducting Fault Current Limiter 
                (SFCL) & Quench Protection Controller.
                
                Monitors high-temperature superconducting (HTS) YBCO tapes operating in
                liquid nitrogen (77K, -196°C) at 138 kV.
                Detects quench state (exceeding critical current Ic) in < 2ms during 
                massive downstream short-circuit faults (> 50 kA).
                Coordinates bypass vacuum interrupter (VI) switches to limit I^2t let-through
                energy, protecting the HTS tapes from thermal runaway while limiting 
                fault current for the grid.
                
State Machine:  PackML V8.0 (ISA-TR88.00.02)
Math:           Quench physics, thermal mass accumulation, I^2t let-through calculation
=========================================================================================
*)

FUNCTION_BLOCK FB_Grid_SFCL_Protection
VAR_INPUT
    (* PackML State Machine Controls *)
    bExecute                : BOOL;             (* Command to start execution *)
    bReset                  : BOOL;             (* Command to reset from ABORTED/STOPPED *)
    bAbort                  : BOOL;             (* Emergency abort command *)
    
    (* Grid & HTS Measurements *)
    fGridVoltage_kV         : LREAL;            (* Real-time grid voltage (kV), nominally 138.0 *)
    fGridCurrent_kA         : LREAL;            (* Real-time line current (kA) *)
    fSFCL_VoltageDrop_V     : LREAL;            (* Voltage drop across the SFCL module (V) *)
    fCryostatTemp_K         : LREAL := 77.0;    (* Liquid Nitrogen temperature (Kelvin) *)
    
    (* Protection Thresholds *)
    fCriticalCurrent_Ic_kA  : LREAL := 10.0;    (* Critical current of YBCO tapes (kA) *)
    fCriticalTemp_Tc_K      : LREAL := 92.0;    (* Critical temperature of YBCO tapes (K) *)
    fQuenchVoltageThresh_V  : LREAL := 50.0;    (* Voltage drop indicating quench onset (V) *)
    fMaxLetThroughEnergy    : LREAL := 1.5E6;   (* Maximum I^2t let-through energy (A^2s) *)
    tMaxQuenchDuration      : TIME := T#2ms;    (* Max time allowed in quench before bypass *)
    
    (* Timing & Cycle *)
    fSampleTime_s           : LREAL := 0.0001;  (* Execution cycle time in seconds (100us) *)
END_VAR

VAR_OUTPUT
    (* PackML Status *)
    eCurrentState           : E_PackML_State;   (* Current PackML State *)
    bActive                 : BOOL;             (* System is running in EXECUTE state *)
    bError                  : BOOL;             (* Error flag *)
    nErrorID                : UDINT;            (* Error Code *)
    
    (* SFCL Status *)
    bQuenchDetected         : BOOL;             (* Quench transition detected *)
    fCalculatedResistance_R : LREAL;            (* Real-time resistance of SFCL module (Ohms) *)
    fAccumulatedEnergy_I2t  : LREAL;            (* Real-time accumulated let-through energy (A^2s) *)
    fEstimatedTapeTemp_K    : LREAL;            (* Estimated instantaneous temperature of YBCO tape (K) *)
    
    (* Actuation Signals *)
    bTripBypassVacuumSwitch : BOOL;             (* Command to close parallel bypass vacuum interrupter *)
    bTripMainGridBreaker    : BOOL;             (* Command to open main line breaker if bypass fails *)
END_VAR

VAR
    (* Internal State *)
    eState                  : E_PackML_State := E_PackML_State.STOPPED;
    
    (* Timers & Triggers *)
    tonQuenchTimer          : TON;
    rtrigExecute            : R_TRIG;
    rtrigReset              : R_TRIG;
    rtrigAbort              : R_TRIG;
    
    (* Physics & Constants *)
    fYBCO_NormalResistivity : LREAL := 1.2E-6;  (* Resistivity of normal state YBCO (Ohm*m) *)
    fTapeThermalMass_J_K    : LREAL := 450.0;   (* Specific thermal mass of tape module (J/K) *)
    fCoolingPower_W_K       : LREAL := 5000.0;  (* Heat dissipation to liquid nitrogen (W/K) *)
    fPowerDissipation_W     : LREAL;
    fDeltaTemp              : LREAL;
    
    (* Integrators *)
    fI2t_Integrator         : LREAL := 0.0;
    
    (* Internal flags *)
    bThermalRunawayDanger   : BOOL := FALSE;
    bCoolingRecovery        : BOOL := FALSE;
END_VAR

(* --- Trigger Updates --- *)
rtrigExecute(CLK := bExecute);
rtrigReset(CLK := bReset);
rtrigAbort(CLK := bAbort);

(* --- Global Abort Handling --- *)
IF rtrigAbort.Q THEN
    eState := E_PackML_State.ABORTING;
END_IF

(* --- PackML State Machine --- *)
CASE eState OF
    E_PackML_State.STOPPED:
        bActive := FALSE;
        bQuenchDetected := FALSE;
        bTripBypassVacuumSwitch := FALSE;
        bTripMainGridBreaker := FALSE;
        fI2t_Integrator := 0.0;
        fEstimatedTapeTemp_K := fCryostatTemp_K;
        
        IF rtrigReset.Q THEN
            bError := FALSE;
            nErrorID := 0;
            eState := E_PackML_State.RESETTING;
        END_IF
        
    E_PackML_State.RESETTING:
        (* Perform self-diagnostics on cryostat temp *)
        IF fCryostatTemp_K > 80.0 THEN
            bError := TRUE;
            nErrorID := 16#E001; (* Cryogen loss or temp too high *)
            eState := E_PackML_State.ABORTING;
        ELSE
            eState := E_PackML_State.IDLE;
        END_IF
        
    E_PackML_State.IDLE:
        IF rtrigExecute.Q THEN
            eState := E_PackML_State.STARTING;
        END_IF
        
    E_PackML_State.STARTING:
        (* Initialize Integrators *)
        fI2t_Integrator := 0.0;
        fEstimatedTapeTemp_K := fCryostatTemp_K;
        eState := E_PackML_State.EXECUTE;
        
    E_PackML_State.EXECUTE:
        bActive := TRUE;
        
        (* 1. Fundamental Calculations *)
        IF ABS(fGridCurrent_kA) > 0.001 THEN
            (* Calculate SFCL resistance R = V / I *)
            fCalculatedResistance_R := ABS(fSFCL_VoltageDrop_V / (fGridCurrent_kA * 1000.0));
        ELSE
            fCalculatedResistance_R := 0.0;
        END_IF
        
        (* 2. Quench Detection Logic *)
        (* Quench occurs when current exceeds Ic AND voltage drop exceeds threshold *)
        IF (ABS(fGridCurrent_kA) > fCriticalCurrent_Ic_kA) AND 
           (ABS(fSFCL_VoltageDrop_V) > fQuenchVoltageThresh_V) THEN
            bQuenchDetected := TRUE;
        ELSE
            (* Hysteresis for recovery *)
            IF (ABS(fGridCurrent_kA) < (fCriticalCurrent_Ic_kA * 0.8)) AND 
               (fEstimatedTapeTemp_K < (fCriticalTemp_Tc_K - 5.0)) THEN
                bQuenchDetected := FALSE;
            END_IF
        END_IF
        
        (* 3. Quench Physics & Thermal Model *)
        IF bQuenchDetected THEN
            (* Power dissipation in the tape P = I * V *)
            fPowerDissipation_W := ABS(fGridCurrent_kA * 1000.0) * ABS(fSFCL_VoltageDrop_V);
            
            (* Calculate I^2t let-through energy (A^2s) *)
            (* I2t = Integral of i(t)^2 dt *)
            fI2t_Integrator := fI2t_Integrator + (EXPT(fGridCurrent_kA * 1000.0, 2) * fSampleTime_s);
            
            (* Thermodynamic model: dT = (P_in - P_out) / mc *)
            fDeltaTemp := ((fPowerDissipation_W - (fCoolingPower_W_K * (fEstimatedTapeTemp_K - fCryostatTemp_K))) 
                           / fTapeThermalMass_J_K) * fSampleTime_s;
            fEstimatedTapeTemp_K := fEstimatedTapeTemp_K + fDeltaTemp;
            
        ELSE
            (* Recovery Phase: Cooling back to cryostat temp *)
            fPowerDissipation_W := 0.0;
            IF fEstimatedTapeTemp_K > fCryostatTemp_K THEN
                fDeltaTemp := (-1.0 * fCoolingPower_W_K * (fEstimatedTapeTemp_K - fCryostatTemp_K) / fTapeThermalMass_J_K) * fSampleTime_s;
                fEstimatedTapeTemp_K := fEstimatedTapeTemp_K + fDeltaTemp;
            ELSE
                fEstimatedTapeTemp_K := fCryostatTemp_K;
            END_IF
            
            (* Decay I2t integrator slowly during cooling *)
            IF fI2t_Integrator > 0.0 THEN
                fI2t_Integrator := fI2t_Integrator * 0.999;
            END_IF
        END_IF
        
        (* 4. Protection Actuation *)
        tonQuenchTimer(IN := bQuenchDetected, PT := tMaxQuenchDuration);
        
        bThermalRunawayDanger := (fEstimatedTapeTemp_K > 150.0); (* 150K is danger zone for YBCO stress *)
        
        IF tonQuenchTimer.Q OR (fI2t_Integrator > fMaxLetThroughEnergy) OR bThermalRunawayDanger THEN
            (* Trip the parallel bypass vacuum interrupter to shunt fault current AWAY from HTS tapes *)
            bTripBypassVacuumSwitch := TRUE;
        END_IF
        
        (* 5. Backup Protection (Breaker Failure) *)
        IF bTripBypassVacuumSwitch AND (fI2t_Integrator > (fMaxLetThroughEnergy * 1.5)) THEN
            (* Bypass failed to clear fault from SFCL, trip main breaker to save grid and SFCL *)
            bTripMainGridBreaker := TRUE;
            eState := E_PackML_State.ABORTING;
            bError := TRUE;
            nErrorID := 16#F002; (* Critical Bypass Failure *)
        END_IF
        
        (* 6. Reset Trip after fault clears and temperature recovers *)
        IF bTripBypassVacuumSwitch AND NOT bQuenchDetected AND (fEstimatedTapeTemp_K < 80.0) THEN
            (* Need manual operator intervention to reset bypass in reality, 
               but logistically we hold trip until aborted or manually cleared *)
            (* Keep bTripBypassVacuumSwitch TRUE until manual reset via PackML *)
        END_IF

    E_PackML_State.ABORTING:
        bActive := FALSE;
        bTripBypassVacuumSwitch := TRUE; (* Failsafe: Bypass the SFCL *)
        bTripMainGridBreaker := TRUE;    (* Failsafe: Disconnect from grid *)
        eState := E_PackML_State.ABORTED;
        
    E_PackML_State.ABORTED:
        IF rtrigReset.Q THEN
            bTripBypassVacuumSwitch := FALSE;
            bTripMainGridBreaker := FALSE;
            eState := E_PackML_State.STOPPED;
        END_IF

END_CASE

(* Assign Output State *)
eCurrentState := eState;
fAccumulatedEnergy_I2t := fI2t_Integrator;

END_FUNCTION_BLOCK
```"""
        }
    ]
}

target_dir = r"c:\Users\majip\Downloads\LLM REASEARCH\data"
os.makedirs(target_dir, exist_ok=True)
target_file = os.path.join(target_dir, "synthetic_generation_v3_enterprise.jsonl")

with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(data) + "\n")
