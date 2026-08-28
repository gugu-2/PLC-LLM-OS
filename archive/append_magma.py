import json

mega_prompt = """You are acting as the Principal Geohazards Robotics Engineer for a Magma Chamber Exploration Initiative.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Volcanic Magma Chamber Submersible Drone & Tungsten Tether Controller" (`FB_MagmaDrone_Explorer`).

### Technical Specifications & Engineering Rigor Required:
1. **Molten Silicate Buoyancy & Thermal Management**:
   - Active buoyancy compensation within a liquid basalt/rhyolite magma chamber ($1,200^\circ\text{C}$, massive viscosity gradients up to $10^6\text{ Pa}\cdot\text{s}$).
   - Internal Phase Change Material (PCM) melting rate tracking and thermoelectric generator (TEG) harvesting off the hull thermal gradient to power internal logic.
2. **Tungsten Tether Tensioning & Signal Multiplexing**:
   - Surface winch control maintaining constant tension on a $3\text{ km}$ braided Tungsten-Rhenium tether to prevent slack loops in the convecting magma flow.
   - Acoustic/seismic pulse telemetry encoding since standard electromagnetic radio waves cannot penetrate the conductive molten rock.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, fluid dynamics matrices for non-Newtonian flow, PackML states.

Output a complete, valid JSON object with {"messages": [{"role": "user", "content": "Mega-prompt description"}, {"role": "assistant", "content": "Full raw Structured Text code inside ```iec-st```"}]}.
"""

assistant_content = """```iec-st
FUNCTION_BLOCK FB_MagmaDrone_Explorer
VAR_INPUT
    // PackML State Machine Inputs
    bExecute            : BOOL;
    bAbort              : BOOL;
    bStop               : BOOL;
    bReset              : BOOL;

    // Environmental Sensors (High-T Tolerant)
    fHullTemp_C         : LREAL;  // Surface temp, up to 1250.0 C
    fInternalTemp_C     : LREAL;  // Payload temp, target < 85.0 C
    fMagmaPressure_Pa   : LREAL;  // Ambient hydrostatic pressure
    fAcousticRX_Hz      : LREAL;  // Incoming seismic telemetry signal frequency
    fTetherTension_N    : LREAL;  // Current measured tension on the W-Re tether
    
    // Viscosity & Flow
    fStrainRate_1s      : LREAL;  // Measured shear strain rate from external rheometer
END_VAR

VAR_OUTPUT
    // PackML States
    iState              : INT;    // 0=Stopped, 1=Starting, 2=Execute, 3=Aborting, 4=Aborted
    
    // Winch & Tether Control
    fWinchTorqueCmd_Nm  : LREAL;  // Commanded winch torque for constant tension
    bPulseTxCmd         : BOOL;   // Seismic pulse transmitter actuation
    fAcousticTx_Hz      : LREAL;  // Outgoing telemetry frequency
    
    // Thermal & Buoyancy
    fCoolantFlow_Lpm    : LREAL;  // Active cooling loop flow rate
    fBuoyancyCmd_L      : LREAL;  // Target displacement volume for buoyancy
    fTEG_Harvesting_W   : LREAL;  // Estimated thermoelectric power generation
    
    // Status Flags
    bThermalWarning     : BOOL;
    bTensionWarning     : BOOL;
    bPCM_Depleted       : BOOL;
END_VAR

VAR
    // PackML State Constants
    STATE_IDLE          : INT := 0;
    STATE_STARTING      : INT := 1;
    STATE_EXECUTE       : INT := 2;
    STATE_STOPPING      : INT := 3;
    STATE_STOPPED       : INT := 4;
    STATE_ABORTING      : INT := 5;
    STATE_ABORTED       : INT := 6;
    STATE_HOLDING       : INT := 7;
    STATE_HELD          : INT := 8;

    // Internal Variables for Rheology (Non-Newtonian power-law fluid)
    fConsistencyK       : LREAL := 150000.0; // Consistency index (Pa s^n) for Basaltic/Rhyolitic melt
    fFlowBehavior_n     : LREAL := 0.45;     // Shear-thinning index (dimensionless)
    fDynamicViscosity   : LREAL;             // Calculated apparent viscosity
    
    // Tether Control (Constant Tension)
    fTargetTension_N    : LREAL := 15000.0;  // 15 kN base tension for 3km W-Re tether
    fTensionError       : LREAL;
    fTensionIntegral    : LREAL;
    Kp_Tension          : LREAL := 0.25;
    Ki_Tension          : LREAL := 0.05;
    
    // Thermal & PCM (Phase Change Material) Management
    fPCM_Mass_kg        : LREAL := 250.0;    // Initial mass of PCM (e.g., Lithium Nitrate trihydrate)
    fPCM_LatentHeat_Jkg : LREAL := 280000.0; 
    fPCM_MeltedFraction : LREAL := 0.0;
    fThermalGradient    : LREAL;
    
    // TEG Constants
    fTEG_Seebeck_V_K    : LREAL := 0.005;    // Effective Seebeck coefficient array
    fTEG_InternalRes    : LREAL := 2.5;      // Ohms
    
    // Telemetry Buffer
    nTelemStep          : INT := 0;
    nPulseTimer         : DINT := 0;
END_VAR

// -----------------------------------------------------------------------------
// PackML State Machine Evaluation
// -----------------------------------------------------------------------------
IF bAbort THEN
    iState := STATE_ABORTING;
ELSIF bStop THEN
    iState := STATE_STOPPING;
END_IF;

CASE iState OF
    STATE_IDLE:
        IF bExecute THEN
            iState := STATE_STARTING;
        END_IF;
        
    STATE_STARTING:
        // Initialize regulators and PCM status
        fTensionIntegral := 0.0;
        bThermalWarning := FALSE;
        bTensionWarning := FALSE;
        iState := STATE_EXECUTE;
        
    STATE_EXECUTE:
        // Main operational state, processed below
        ;
        
    STATE_STOPPING:
        fWinchTorqueCmd_Nm := 5000.0; // Maintain base holding torque
        fCoolantFlow_Lpm := 10.0;     // Minimum cooling
        iState := STATE_STOPPED;
        
    STATE_STOPPED:
        IF bReset THEN
            iState := STATE_IDLE;
        END_IF;
        
    STATE_ABORTING:
        // Emergency ascent, max buoyancy, emergency tension
        fWinchTorqueCmd_Nm := 25000.0; // Max pull
        fBuoyancyCmd_L := 100.0;       // Max displacement
        fCoolantFlow_Lpm := 100.0;     // Max cooling
        iState := STATE_ABORTED;
        
    STATE_ABORTED:
        IF bReset THEN
            iState := STATE_IDLE;
        END_IF;
        
    ELSE
        iState := STATE_IDLE;
END_CASE;

// -----------------------------------------------------------------------------
// Core Subsystems (Only Active in EXECUTE)
// -----------------------------------------------------------------------------
IF iState = STATE_EXECUTE THEN
    
    // ---------------------------------------------------------
    // 1. Non-Newtonian Rheology & Viscosity Estimation
    // ---------------------------------------------------------
    // Power-law fluid: Apparent Viscosity = K * (StrainRate)^(n-1)
    // Avoid division by zero
    IF fStrainRate_1s > 0.001 THEN
        fDynamicViscosity := fConsistencyK * EXPT(fStrainRate_1s, (fFlowBehavior_n - 1.0));
    ELSE
        fDynamicViscosity := 1000000.0; // Cap at 10^6 Pa-s for ultra-low shear
    END_IF;

    // Adjust buoyancy dynamically based on local magma density/viscosity
    // Higher viscosity requires more forceful displacement to achieve vertical translation
    fBuoyancyCmd_L := 50.0 + (fDynamicViscosity * 0.00005); 

    // ---------------------------------------------------------
    // 2. Thermal Management & TEG Power Harvesting
    // ---------------------------------------------------------
    fThermalGradient := fHullTemp_C - fInternalTemp_C;
    
    // Estimate power from TEG: P = (V^2) / R = (S * dT)^2 / R
    IF fThermalGradient > 0.0 THEN
        fTEG_Harvesting_W := EXPT((fTEG_Seebeck_V_K * fThermalGradient), 2.0) / fTEG_InternalRes;
    ELSE
        fTEG_Harvesting_W := 0.0;
    END_IF;
    
    // Active cooling based on internal temp
    IF fInternalTemp_C > 70.0 THEN
        fCoolantFlow_Lpm := 80.0; // Max flow
        bThermalWarning := TRUE;
        
        // Accumulate PCM melting
        // Very simplified: assuming excess heat fluxes into the PCM
        fPCM_MeltedFraction := fPCM_MeltedFraction + 0.0001; 
    ELSIF fInternalTemp_C > 50.0 THEN
        fCoolantFlow_Lpm := 40.0 + (fInternalTemp_C - 50.0) * 2.0; // Proportional
        bThermalWarning := FALSE;
    ELSE
        fCoolantFlow_Lpm := 10.0; // Base flow
        bThermalWarning := FALSE;
    END_IF;
    
    IF fPCM_MeltedFraction >= 0.95 THEN
        bPCM_Depleted := TRUE;
        // If PCM depleted, we must abort to save payload
        iState := STATE_ABORTING;
    END_IF;

    // ---------------------------------------------------------
    // 3. Tether Tensioning (Winch Control PI Loop)
    // ---------------------------------------------------------
    // The winch must maintain tension to prevent slack in the 3km W-Re tether
    // despite powerful convective magma currents acting on the hull.
    fTensionError := fTargetTension_N - fTetherTension_N;
    fTensionIntegral := fTensionIntegral + (fTensionError * 0.01); // Assuming 10ms task
    
    // Anti-windup
    IF fTensionIntegral > 5000.0 THEN fTensionIntegral := 5000.0; END_IF;
    IF fTensionIntegral < -5000.0 THEN fTensionIntegral := -5000.0; END_IF;
    
    fWinchTorqueCmd_Nm := (fTensionError * Kp_Tension) + (fTensionIntegral * Ki_Tension);
    
    // Base holding torque (approx radius * target tension)
    fWinchTorqueCmd_Nm := fWinchTorqueCmd_Nm + (0.5 * fTargetTension_N); 
    
    IF ABS(fTensionError) > 3000.0 THEN
        bTensionWarning := TRUE;
    ELSE
        bTensionWarning := FALSE;
    END_IF;

    // ---------------------------------------------------------
    // 4. Acoustic / Seismic Telemetry Encoding
    // ---------------------------------------------------------
    // Encode drone state via low-frequency seismic pulses (10Hz - 50Hz)
    // EM waves don't propagate in conductive melt, use acoustic pulses.
    nPulseTimer := nPulseTimer + 1;
    IF nPulseTimer > 100 THEN // Every 1 second
        nPulseTimer := 0;
        nTelemStep := nTelemStep + 1;
        IF nTelemStep > 3 THEN nTelemStep := 0; END_IF;
        
        bPulseTxCmd := TRUE;
        
        // Multiplexing
        CASE nTelemStep OF
            0: fAcousticTx_Hz := 20.0; // Sync pulse
            1: fAcousticTx_Hz := 25.0 + (fHullTemp_C * 0.01); // Temp data
            2: fAcousticTx_Hz := 30.0 + (fPCM_MeltedFraction * 10.0); // PCM data
            3: fAcousticTx_Hz := 35.0 + (fDynamicViscosity * 0.00001); // Rheology data
        END_CASE;
    ELSE
        bPulseTxCmd := FALSE;
    END_IF;

END_IF;
END_FUNCTION_BLOCK
```"""

payload = {
    "messages": [
        {"role": "user", "content": mega_prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

file_path = r"c:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\data\synthetic_generation_v3_enterprise.jsonl"
with open(file_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(payload) + "\n")
print("Appended successfully.")
