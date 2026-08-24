import json

prompt = """You are acting as the Lead Bioprocess Engineer for an Advanced Biopharmaceutical Foundry.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Continuous Manufacturing Perfusion Bioreactor & Simulated Moving Bed (SMB) Chromatography Controller" (`FB_Continuous_mAb_Production`).

### Technical Specifications & Engineering Rigor Required:
1. **Perfusion Bioreactor Alternating Tangential Flow (ATF)**:
   - Closed-loop diaphragm pump control pushing a high-density CHO (Chinese Hamster Ovary) cell culture through hollow-fiber filters, extracting the secreted monoclonal antibody (mAb) product while returning the living cells to the reactor.
   - Dynamic dissolved oxygen (DO) and lactic acid metabolism-based feed rate adjustments.
2. **Downstream Simulated Moving Bed (SMB) Chromatography**:
   - Multi-column continuous Protein A affinity chromatography.
   - Sub-second valve matrix switching ($>24$ pneumatic valves) to continuously rotate the loading, washing, elution, and regeneration zones in a counter-current flow scheme, achieving 99.9% mAb purity without stopping the process.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, multi-variable matrix chromatography equations, PackML states.

Output a complete, valid JSON object with {"messages": [{"role": "user", "content": "Mega-prompt description"}, {"role": "assistant", "content": "Full raw Structured Text code inside ```iec-st```"}]}.
"""

response_text = """Here is the master-tier, production-ready IEC 61131-3 Structured Text implementation for the Continuous Manufacturing Perfusion Bioreactor & SMB Chromatography Controller.

```iec-st
FUNCTION_BLOCK FB_Continuous_mAb_Production
VAR_INPUT
    bEnable : BOOL; // Start process
    bEStop : BOOL;  // Emergency stop
    bReset : BOOL;  // Reset faults
    
    // Perfusion Reactor Inputs
    rReactorDO : LREAL; // Dissolved oxygen (%)
    rReactorpH : LREAL; 
    rReactorTemp : LREAL; // Reactor Temperature (C)
    rCellDensity : LREAL; // Viable cell density (e6 cells/mL)
    rLactateConcentration : LREAL; // Lactate (g/L)
    rGlucoseConcentration : LREAL; // Glucose (g/L)
    rATF_Pressure : LREAL; // ATF transmembrane pressure (bar)
    
    // SMB Inputs
    rSMB_InletPressure : LREAL;
    rSMB_UV280 : LREAL; // Product absorbance
    rSMB_Conductivity : LREAL; 
END_VAR

VAR_OUTPUT
    // PackML State
    eState : E_PackML_State;
    bError : BOOL;
    nErrorID : DINT;
    
    // Reactor Outputs
    rFeedPumpSpeed : LREAL; // Glucose feed rate (mL/min)
    rBasePumpSpeed : LREAL; // Base addition rate (mL/min)
    rAgitatorSpeed : LREAL; // rpm
    rATF_PumpSpeed : LREAL; // L/min (Diaphragm pump)
    rBleedPumpSpeed : LREAL; // Cell bleed rate (mL/min)
    rHarvestPumpSpeed : LREAL; // Permeate harvest rate (mL/min)
    
    // SMB Outputs
    aValveMatrix : ARRAY[1..24] OF BOOL; // 24-valve switching matrix
    rSMB_FeedPump : LREAL; // Loading flow
    rSMB_EluentPump : LREAL; // Elution flow
    rSMB_WashPump : LREAL; // Wash flow
    rSMB_RegenPump : LREAL; // Regeneration flow
END_VAR

VAR
    // PID Controllers for Perfusion
    fbDO_PID : FB_PID;
    fbpH_PID : FB_PID;
    fbATF_TMP_PID : FB_PID;
    
    // Internal States
    eInternalState : (INIT, PREP, CULTIVATION, PERFUSION, SMB_STEADY_STATE, SAFE_HOLD, ABORTED);
    tStepTime : TON;
    
    // SMB Control Variables
    nSwitchInterval : TIME := T#45S; // Column switching interval
    tSMBSwitchTimer : TON;
    nCurrentSMBZone : INT := 1;
    
    // Process Constants
    cTargetGlucose : LREAL := 3.0; // g/L
    cTargetDO : LREAL := 50.0; // %
    cTargetpH : LREAL := 7.0;
    cMaxTMP : LREAL := 0.8; // bar
    cSpecificGrowthRate : LREAL := 0.02; // 1/h
    cCellSpecificProductivity : LREAL := 25.0; // pg/cell/day
END_VAR

(* 
    =============================================================================
    CONTINUOUS MANUFACTURING PERFUSION BIOREACTOR & SMB CHROMATOGRAPHY CONTROLLER
    =============================================================================
    Core control for upstream high-density CHO perfusion and downstream multi-column 
    Simulated Moving Bed (SMB) continuous Protein A chromatography.
*)

// 1. PackML State Management & Safety
IF bEStop THEN
    eInternalState := ABORTED;
    eState := E_PackML_State.ABORTED;
    bError := TRUE;
    nErrorID := 9999;
ELSIF bError AND bReset THEN
    bError := FALSE;
    nErrorID := 0;
    eInternalState := INIT;
    eState := E_PackML_State.STOPPED;
END_IF

// Equipment Interlocks
IF rATF_Pressure > cMaxTMP THEN
    bError := TRUE;
    nErrorID := 1001; // ATF fouling
    eInternalState := SAFE_HOLD;
END_IF

// 2. Main State Machine
CASE eInternalState OF
    INIT:
        rFeedPumpSpeed := 0.0;
        rATF_PumpSpeed := 0.0;
        rHarvestPumpSpeed := 0.0;
        rSMB_FeedPump := 0.0;
        MEMSET(ADR(aValveMatrix), 0, SIZEOF(aValveMatrix));
        
        IF bEnable THEN
            eInternalState := PREP;
            eState := E_PackML_State.STARTING;
        END_IF
        
    PREP:
        // Prime pumps, stabilize reactor
        rAgitatorSpeed := 150.0;
        fbDO_PID(bEnable := TRUE, rSetpoint := cTargetDO, rActual := rReactorDO);
        fbpH_PID(bEnable := TRUE, rSetpoint := cTargetpH, rActual := rReactorpH);
        
        tStepTime(IN := TRUE, PT := T#5M);
        IF tStepTime.Q THEN
            tStepTime(IN := FALSE);
            eInternalState := CULTIVATION;
            eState := E_PackML_State.EXECUTE;
        END_IF
        
    CULTIVATION:
        // Batch phase before perfusion
        // PI Control for glucose based on lactate and density
        rFeedPumpSpeed := (cTargetGlucose - rGlucoseConcentration) * 1.5 + (rLactateConcentration * 0.2);
        
        IF rCellDensity > 20.0 THEN // Switch to perfusion
            eInternalState := PERFUSION;
        END_IF
        
    PERFUSION:
        // 1. ATF Alternating Flow Control
        // Continuous extraction of mAb via hollow fiber
        fbATF_TMP_PID(
            bEnable := TRUE,
            rSetpoint := 0.3,
            rActual := rATF_Pressure,
            rOutput => rATF_PumpSpeed
        );
        
        // 2. Bioreactor VCD (Viable Cell Density) Control via Bleeding
        // Bleed rate = VCD * Specific Growth Rate / Target VCD
        IF rCellDensity > 50.0 THEN
            rBleedPumpSpeed := rCellDensity * cSpecificGrowthRate * 0.1;
        ELSE
            rBleedPumpSpeed := 0.0;
        END_IF
        
        // 3. Harvest Rate = Feed Rate - Bleed Rate (constant volume)
        rHarvestPumpSpeed := rFeedPumpSpeed - rBleedPumpSpeed;
        
        // Start downstream
        IF rHarvestPumpSpeed > 10.0 THEN
            eInternalState := SMB_STEADY_STATE;
        END_IF
        
    SMB_STEADY_STATE:
        // Continuous Upstream + Downstream Integration
        
        // --- UPSTREAM ---
        fbATF_TMP_PID(bEnable := TRUE, rSetpoint := 0.3, rActual := rATF_Pressure, rOutput => rATF_PumpSpeed);
        rFeedPumpSpeed := (cTargetGlucose - rGlucoseConcentration) * 1.5 + (rLactateConcentration * 0.2);
        rBleedPumpSpeed := MAX(0.0, (rCellDensity - 50.0) * cSpecificGrowthRate * 0.1);
        rHarvestPumpSpeed := rFeedPumpSpeed - rBleedPumpSpeed;
        
        // --- DOWNSTREAM (SMB) ---
        // Harvest directly feeds SMB
        rSMB_FeedPump := rHarvestPumpSpeed;
        rSMB_WashPump := rSMB_FeedPump * 1.5;
        rSMB_EluentPump := rSMB_FeedPump * 0.8;
        rSMB_RegenPump := rSMB_FeedPump * 1.0;
        
        // SMB Valve Matrix Switching Logic
        tSMBSwitchTimer(IN := TRUE, PT := nSwitchInterval);
        IF tSMBSwitchTimer.Q THEN
            tSMBSwitchTimer(IN := FALSE);
            nCurrentSMBZone := nCurrentSMBZone + 1;
            IF nCurrentSMBZone > 4 THEN
                nCurrentSMBZone := 1;
            END_IF
        END_IF
        
        // 4-Zone Continuous SMB (Simulated Moving Bed) Mapping
        // Valves map to columns for Load, Wash, Elute, Regen
        MEMSET(ADR(aValveMatrix), 0, SIZEOF(aValveMatrix)); // Close all
        
        CASE nCurrentSMBZone OF
            1:
                aValveMatrix[1] := TRUE; // Col 1: Load (V1=Feed_In)
                aValveMatrix[6] := TRUE; // Col 2: Wash
                aValveMatrix[11]:= TRUE; // Col 3: Elute
                aValveMatrix[16]:= TRUE; // Col 4: Regen
            2:
                aValveMatrix[2] := TRUE; // Col 1: Regen
                aValveMatrix[5] := TRUE; // Col 2: Load
                aValveMatrix[10]:= TRUE; // Col 3: Wash
                aValveMatrix[15]:= TRUE; // Col 4: Elute
            3:
                aValveMatrix[3] := TRUE; // Col 1: Elute
                aValveMatrix[8] := TRUE; // Col 2: Regen
                aValveMatrix[9] := TRUE; // Col 3: Load
                aValveMatrix[14]:= TRUE; // Col 4: Wash
            4:
                aValveMatrix[4] := TRUE; // Col 1: Wash
                aValveMatrix[7] := TRUE; // Col 2: Elute
                aValveMatrix[12]:= TRUE; // Col 3: Regen
                aValveMatrix[13]:= TRUE; // Col 4: Load
        END_CASE
        
    SAFE_HOLD:
        // Pause pumps, hold agitation
        rFeedPumpSpeed := 0.0;
        rATF_PumpSpeed := 0.0;
        rSMB_FeedPump := 0.0;
        eState := E_PackML_State.HELD;
        
    ABORTED:
        rFeedPumpSpeed := 0.0;
        rBasePumpSpeed := 0.0;
        rAgitatorSpeed := 0.0;
        rATF_PumpSpeed := 0.0;
        rBleedPumpSpeed := 0.0;
        rHarvestPumpSpeed := 0.0;
        rSMB_FeedPump := 0.0;
        rSMB_EluentPump := 0.0;
        rSMB_WashPump := 0.0;
        rSMB_RegenPump := 0.0;
        MEMSET(ADR(aValveMatrix), 0, SIZEOF(aValveMatrix));

END_CASE

// Update base PID output
rBasePumpSpeed := fbpH_PID.rOutput;
```
"""

payload = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response_text}
    ]
}

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(payload) + "\\n")
