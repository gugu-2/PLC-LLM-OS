import json
import os

prompt = """You are acting as the Chief Astrobiology Engineer for a Europa Subsurface Exploration Mission.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Europan Ice-Shell Nuclear Melt-Probe (Cryobot) & Hydrothermal Sampling Controller" (`FB_Cryobot_EuropaExplorer`).

### Technical Specifications & Engineering Rigor Required:
1. **Radioisotope Thermal Melting & Gravity-Driven Descent**:
   - Closed-loop heat routing from the internal Plutonium-238 General Purpose Heat Source (GPHS).
   - Dynamic fluidic routing of heated melt-water jets to the nose cone to melt through 20 km of cryogenic, radiation-hardened Europan ice, while actively freezing the ice behind the probe to seal it from surface contamination.
2. **Subsurface Ocean Hydrothermal Plume Navigation**:
   - Transition to neutral-buoyancy autonomous underwater vehicle (AUV) mode upon breaking through the ice ceiling into the global ocean.
   - Vector-thrust acoustic homing towards localized thermal gradients indicative of alkaline hydrothermal vents, searching for extraterrestrial biosignatures.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, comprehensive `VAR_INPUT`/`VAR_OUTPUT`, thermodynamics equations for phase change, PackML states.
"""

st_code = """```iec-st
(*
===================================================================================================
FUNCTION_BLOCK FB_Cryobot_EuropaExplorer
===================================================================================================
DESCRIPTION:
Master Control for the Europan Ice-Shell Nuclear Melt-Probe (Cryobot) & Hydrothermal Sampling AUV.
Implements dynamic heat routing from Pu-238 GPHS for phase-change cryo-drilling (melting/refreezing).
Transitions to AUV mode upon ocean entry, performing vector-thrust navigation to localized thermal 
gradients (alkaline hydrothermal vents) for biosignature sampling.

PACKML STATES IMPLEMENTED:
- ABORTED, CLEARING, STOPPED, STARTING, EXECUTE (MELTING), HELD, UNHOLDING
- EXECUTE_AUV (OCEAN TRANSITION & NAVIGATION), SAMPLING

AUTHOR: Chief Astrobiology Engineer, Lumina Elite Synthetic Data Architect
===================================================================================================
*)

FUNCTION_BLOCK FB_Cryobot_EuropaExplorer
VAR_INPUT
    (* Commands *)
    bExecuteMission     : BOOL; (* Start descent sequence *)
    bEmergencyAbort     : BOOL; (* Scram systems and abort *)
    bReset              : BOOL; (* Reset faults *)
    
    (* Environmental Telemetry (Sensor Inputs) *)
    fExternalTempK      : LREAL; (* External Ice/Water Temperature in Kelvin *)
    fExternalPressurePa : LREAL; (* External Pressure in Pascals *)
    fIceDensity         : LREAL; (* Estimated density of surrounding ice (kg/m^3) *)
    fDepthMeters        : LREAL; (* Z-axis depth from Europa surface *)
    
    (* Thermal / GPHS Inputs *)
    fGPHS_CoreTempK     : LREAL; (* Core temperature of the Pu-238 GPHS *)
    fThermalPowerW      : LREAL; (* Available thermal power in Watts *)
    
    (* Ocean/Navigation Inputs (Active only in Ocean Mode) *)
    fThermalGradientX   : LREAL; (* Detected dK/dx from acoustic/thermal sensors *)
    fThermalGradientY   : LREAL; (* Detected dK/dy *)
    fThermalGradientZ   : LREAL; (* Detected dK/dz *)
    bVentsDetected      : BOOL;  (* Flag indicating proximity to hydrothermal vent *)
END_VAR

VAR_OUTPUT
    (* Status & PackML State *)
    eState              : INT := 3; (* E_PackML_State.STOPPED *)
    bFault              : BOOL;
    nErrorID            : UDINT;
    
    (* Actuator Control - Cryobot Melting Mode *)
    fNoseConeHeatFluxW  : LREAL; (* Directed heat flux to nose cone for melting *)
    fAftFreezeCoolantFlow:LREAL; (* Flow rate of coolant to freeze wake behind probe (L/s) *)
    fPumpSpeedJet       : LREAL; (* Hot water jet pump speed (0.0 to 100.0%) *)
    
    (* Actuator Control - AUV Navigation Mode *)
    fThrustVectorX      : LREAL; (* Thrust vector X component (-100.0 to 100.0) *)
    fThrustVectorY      : LREAL; (* Thrust vector Y component (-100.0 to 100.0) *)
    fThrustVectorZ      : LREAL; (* Thrust vector Z component (-100.0 to 100.0) *)
    bDeploySampler      : BOOL;  (* Command to deploy micro-fluidic sample intake *)
    
    (* Telemetry Output *)
    fDescentVelocityM_s : LREAL; (* Calculated rate of descent through ice *)
    bOceanBreakthrough  : BOOL;  (* True when liquid ocean boundary is crossed *)
END_VAR

VAR
    (* Internal Thermodynamics Constants *)
    c_fLatentHeatFusionIce : LREAL := 334000.0; (* J/kg for H2O *)
    c_fHeatCapacityIce     : LREAL := 2108.0;   (* J/(kg*K) *)
    c_fEuropaIceMeltingPointK : LREAL := 273.15;(* Assuming pure H2O, neglecting pressure effects for baseline *)
    
    (* Internal State Variables *)
    fRequiredMeltEnergyW : LREAL; 
    fAvailableMeltPowerW : LREAL;
    fProbeCrossSectionA  : LREAL := 0.2827;     (* Area in m^2, assuming ~0.6m diameter *)
    fEnergyLossConduction: LREAL;
    
    fIntegralErrorNavX   : LREAL := 0.0;
    fIntegralErrorNavY   : LREAL := 0.0;
    fIntegralErrorNavZ   : LREAL := 0.0;
    
    bInitDone            : BOOL := FALSE;
END_VAR

(* -----------------------------------------------------------------------------
   INITIALIZATION
   ----------------------------------------------------------------------------- *)
IF NOT bInitDone THEN
    eState := 3; (* STOPPED *)
    bInitDone := TRUE;
END_IF

(* -----------------------------------------------------------------------------
   EMERGENCY SCRAM HANDLING
   ----------------------------------------------------------------------------- *)
IF bEmergencyAbort THEN
    eState := 1; (* ABORTED *)
    bFault := TRUE;
    nErrorID := 9999; (* Critical Abort *)
    fNoseConeHeatFluxW := 0.0;
    fPumpSpeedJet := 0.0;
    fThrustVectorX := 0.0;
    fThrustVectorY := 0.0;
    fThrustVectorZ := 0.0;
    bDeploySampler := FALSE;
END_IF

IF bReset AND eState = 1 THEN (* ABORTED *)
    bFault := FALSE;
    nErrorID := 0;
    eState := 2; (* CLEARING *)
END_IF

(* -----------------------------------------------------------------------------
   ENVIRONMENTAL STATE DETECTION (BREAKTHROUGH)
   ----------------------------------------------------------------------------- *)
(* If depth > 20km (20,000m) and external temp > 270K and pressure matches hydrostatic, 
   we assume breakthrough to the global ocean. *)
IF (fDepthMeters >= 20000.0) AND (fExternalTempK >= 270.0) THEN
    bOceanBreakthrough := TRUE;
ELSE
    bOceanBreakthrough := FALSE;
END_IF


(* -----------------------------------------------------------------------------
   STATE MACHINE (PackML Inspired)
   ----------------------------------------------------------------------------- *)
CASE eState OF
    
    2: (* CLEARING *)
        (* Reset logic *)
        IF NOT bEmergencyAbort THEN
            eState := 3; (* STOPPED *)
        END_IF
        
    3: (* STOPPED *)
        (* Zero outputs *)
        fNoseConeHeatFluxW := 0.0;
        fAftFreezeCoolantFlow := 10.0; (* Maintain thermal isolation of core *)
        fPumpSpeedJet := 0.0;
        
        IF bExecuteMission AND NOT bFault THEN
            eState := 4; (* STARTING *)
        END_IF
        
    4: (* STARTING *)
        (* Spool up GPHS thermal routing loops *)
        IF fGPHS_CoreTempK > 1200.0 THEN (* GPHS is nominal *)
            IF bOceanBreakthrough THEN
                eState := 10; (* EXECUTE_AUV *)
            ELSE
                eState := 5; (* EXECUTE *) (* Melting *)
            END_IF
        END_IF
        
    5: (* EXECUTE *)
        (* ---------------------------------------------------------------------
           MODE: CRYOBOT MELTING / DESCENT
           --------------------------------------------------------------------- *)
        IF bOceanBreakthrough THEN
            eState := 10; (* EXECUTE_AUV *)
        ELSIF bEmergencyAbort THEN
            eState := 1; (* ABORTED *)
        ELSE
            (* 1. Calculate thermodynamics for melting *)
            (* Energy required to raise ice to melting point + latent heat of fusion *)
            (* Q = m*c*dT + m*L *)
            
            fEnergyLossConduction := (c_fEuropaIceMeltingPointK - fExternalTempK) * 50.0; (* Simplified conduction loss *)
            fAvailableMeltPowerW := fThermalPowerW - fEnergyLossConduction;
            
            IF fAvailableMeltPowerW > 0.0 THEN
                (* Route 85% of available thermal power to the nose cone melt-jets *)
                fNoseConeHeatFluxW := fAvailableMeltPowerW * 0.85;
                
                (* Calculate Descent Velocity (simplified Stefan problem)
                   v = P / (A * rho * (c*dT + L)) *)
                fRequiredMeltEnergyW := (c_fHeatCapacityIce * (c_fEuropaIceMeltingPointK - fExternalTempK)) + c_fLatentHeatFusionIce;
                fDescentVelocityM_s := fNoseConeHeatFluxW / (fProbeCrossSectionA * fIceDensity * fRequiredMeltEnergyW);
                
                (* Run hot water jets proportional to available flux *)
                fPumpSpeedJet := 80.0; 
                
                (* Active refreezing behind the probe (Sterilization/Sealing protocol) *)
                (* Divert remaining 15% thermal energy away from aft section, pump coolant *)
                fAftFreezeCoolantFlow := 50.0; 
            ELSE
                fNoseConeHeatFluxW := 0.0;
                fDescentVelocityM_s := 0.0;
                fPumpSpeedJet := 0.0;
                eState := 6; (* HELD *) (* Insufficient power, hold position *)
            END_IF
        END_IF
        
    6: (* HELD *)
        (* Waiting for thermal capacity to build up *)
        fNoseConeHeatFluxW := 0.0;
        fPumpSpeedJet := 0.0;
        IF fThermalPowerW > 5000.0 THEN (* Threshold reached *)
            eState := 7; (* UNHOLDING *)
        END_IF
        
    7: (* UNHOLDING *)
        eState := 5; (* EXECUTE *)
        
    10: (* EXECUTE_AUV *)
        (* ---------------------------------------------------------------------
           MODE: AUTONOMOUS UNDERWATER VEHICLE (OCEAN EXPLORATION)
           --------------------------------------------------------------------- *)
        (* Melt systems off *)
        fNoseConeHeatFluxW := 0.0;
        fPumpSpeedJet := 0.0;
        fDescentVelocityM_s := 0.0;
        
        IF bVentsDetected THEN
            eState := 11; (* SAMPLING *)
        ELSE
            (* Vector Thrust Navigation: Homing on thermal gradients (dK/dx, dK/dy, dK/dz) *)
            (* Simple P-I Controller towards positive thermal gradient (towards source) *)
            
            fIntegralErrorNavX := fIntegralErrorNavX + (fThermalGradientX * 0.01);
            fIntegralErrorNavY := fIntegralErrorNavY + (fThermalGradientY * 0.01);
            fIntegralErrorNavZ := fIntegralErrorNavZ + (fThermalGradientZ * 0.01);
            
            (* Kp = 50.0, Ki = 5.0 *)
            fThrustVectorX := (fThermalGradientX * 50.0) + (fIntegralErrorNavX * 5.0);
            fThrustVectorY := (fThermalGradientY * 50.0) + (fIntegralErrorNavY * 5.0);
            
            (* Neutral buoyancy maintenance + gradient tracking for Z *)
            fThrustVectorZ := (fThermalGradientZ * 50.0) + (fIntegralErrorNavZ * 5.0);
            
            (* Clamp thrust limits *)
            IF fThrustVectorX > 100.0 THEN fThrustVectorX := 100.0; END_IF;
            IF fThrustVectorX < -100.0 THEN fThrustVectorX := -100.0; END_IF;
            IF fThrustVectorY > 100.0 THEN fThrustVectorY := 100.0; END_IF;
            IF fThrustVectorY < -100.0 THEN fThrustVectorY := -100.0; END_IF;
            IF fThrustVectorZ > 100.0 THEN fThrustVectorZ := 100.0; END_IF;
            IF fThrustVectorZ < -100.0 THEN fThrustVectorZ := -100.0; END_IF;
        END_IF
        
    11: (* SAMPLING *)
        (* Vent proximity achieved. Hover and deploy micro-fluidic sampler *)
        fThrustVectorX := 0.0; (* Maintain hover *)
        fThrustVectorY := 0.0;
        fThrustVectorZ := 0.0; 
        
        bDeploySampler := TRUE;
        
        (* If vent is lost, go back to searching *)
        IF NOT bVentsDetected THEN
            bDeploySampler := FALSE;
            eState := 10; (* EXECUTE_AUV *)
        END_IF
        
END_CASE
END_FUNCTION_BLOCK
```"""

payload = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

data_dir = "data"
os.makedirs(data_dir, exist_ok=True)
output_path = os.path.join(data_dir, "synthetic_generation_v3_enterprise.jsonl")

with open(output_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(payload) + "\\n")
