import json, uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V5 Persona: a 60+ years experienced God-Tier PLC Architect & Cyber-Physical Systems Post-Doc. 
Your logic must include advanced State-Space Modeling, Model Predictive Control (MPC) concepts, Non-Linear PID with Anti-Windup, and extreme multi-layer hardware safety matrices. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Mega-Scale Superconducting Magnetic Energy Storage (SMES) Cryocooler and Power Conversion System (PCS)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. This MUST be drastically better, more advanced, and longer than previous V4 iterations.

CRITICAL RULES - READ EVERY LINE:
1. CODE FENCE: Use TRIPLE backticks + iec-st. EXACTLY like this:
   ```iec-st
   (your code here)
   ```
   NEVER use a single backtick `iec-st. ALWAYS use triple backticks.
2. REQUIRED IEC 61131-3 STRUCTURE (all 5 mandatory):
   a. FUNCTION_BLOCK FB_<Name>   <- first line of code, always
   b. VAR_INPUT ... END_VAR      <- min 6 typed inputs with comments
   c. VAR_OUTPUT ... END_VAR     <- min 5 typed outputs with comments
   d. At least one END_IF; or END_CASE;  <- control logic required
   e. END_FUNCTION_BLOCK         <- last line of code, always
3. LENGTH: The assistant content MUST be >= 2500 characters total. Make it incredibly massive and rigorous.
4. SAVE to isolated file using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st\nFUNCTION_BLOCK FB_SMES_CryocoolerPCS\n//...\nEND_FUNCTION_BLOCK\n```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is ```iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT & VAR_OUTPUT sections
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ```
   [ ] Total chars >= 2500
6. REPLY with: EVOLUTION COMPLETE: Mega-Scale Superconducting Magnetic Energy Storage (SMES) Cryocooler and Power Conversion System (PCS)"""

code = """```iec-st
FUNCTION_BLOCK FB_SMES_Cryocooler_PCS_Control
VAR_INPUT
    (* Master control and safety interlocks *)
    bEnable                 : BOOL;     (* Master system enable command from SCADA *)
    bEmergencyStop          : BOOL;     (* Hardware E-Stop (Active Low) / Safety Relay OK *)
    bQuenchDetect           : BOOL;     (* Hardwired quench detection signal (Active High) from fiber optics *)
    
    (* Cryogenic system sensor inputs *)
    rCoilCurrent            : REAL;     (* Measured SMES coil operating current [A] *)
    rCoilTemperature        : REAL;     (* Measured superconducting coil temperature [K] *)
    rHeBathLevel            : REAL;     (* Liquid Helium bath level [%] *)
    rCryocoolerPressure     : REAL;     (* Helium gas compressor return pressure [bar] *)
    
    (* Electrical grid and PCS measurements *)
    rGridVoltage            : REAL;     (* Main AC grid voltage RMS [V] *)
    rGridFrequency          : REAL;     (* Main AC grid frequency [Hz] *)
    rPowerDemand            : REAL;     (* Power dispatch demand from grid operator [MW] *)
    rDCBusVoltage           : REAL;     (* Intermediate DC link voltage of PCS [V] *)
END_VAR

VAR_OUTPUT
    (* Status and mode indications *)
    bSystemReady            : BOOL;     (* PCS and Cryocooler are nominal and ready for dispatch *)
    bPCS_Enable             : BOOL;     (* Enable signal to PCS IGBT gating unit *)
    
    (* Actuator commands *)
    rPCSActivePowerCmd      : REAL;     (* Real power command to PCS [MW] *)
    rPCSReactivePowerCmd    : REAL;     (* Reactive power command to PCS [MVAR] *)
    rCryocoolerFlowCmd      : REAL;     (* Command to Helium compressor bypass valve [0-100%] *)
    rHeaterCmd              : REAL;     (* Command to cryogenic dump heater for quench mitigation [0-100%] *)
    
    (* Alarms and diagnostics *)
    bQuenchAlarm            : BOOL;     (* Critical quench protection activated *)
    bGridFaultAlarm         : BOOL;     (* Grid voltage/frequency out of bounds *)
    bThermalWarning         : BOOL;     (* Impending thermal boundary approach *)
END_VAR

VAR
    (* State Machine & Timing *)
    iState                  : INT := 0; (* Main state machine tracker *)
    tStartupDelay           : TON;      (* Delay for cryogenic stabilization *)
    tGridFaultTimer         : TON;      (* Ride-through timer for grid voltage dips *)
    tWatchdog               : TON;      (* Execution watchdog timer *)
    
    (* Non-Linear PID Controller Variables (Power Dispatch) *)
    rCurrentError           : REAL;
    rIntegralTerm           : REAL := 0.0;
    rDerivativeTerm         : REAL := 0.0;
    rLastCurrentError       : REAL := 0.0;
    
    (* Tuning Parameters (Adaptive Base) *)
    rKp                     : REAL := 2.50;
    rKi                     : REAL := 0.15;
    rKd                     : REAL := 0.05;
    rWindupLimit            : REAL := 150.0;
    
    (* Model Predictive Control (MPC) Thermal Variables *)
    rThermalCapacity        : REAL := 8500.0;  (* Specific heat capacity of the cold mass [J/K] *)
    rThermalResistance      : REAL := 0.015;   (* Equivalent thermal resistance to cryocooler [K/W] *)
    rEstimatedHeatLoad      : REAL;            (* AC loss heat generation estimate [W] *)
    rPredictedTempHorizon   : REAL;            (* N-step ahead predicted temperature [K] *)
    rMaxFlowCmd             : REAL := 100.0;
    rMinFlowCmd             : REAL := 15.0;
    
    (* State-Space Electrical Model Variables (Observer) *)
    rEstimatedDCLinkVolts   : REAL;
    rObserverGain           : REAL := 0.02;
END_VAR

(* === MAIN LOGIC === *)

(* -------------------------------------------------------------------------
   LAYER 1: EXTREME HARDWARE SAFETY & QUENCH PROTECTION MATRIX
   ------------------------------------------------------------------------- *)
IF NOT bEmergencyStop THEN
    (* Immediate system-wide safe state *)
    bSystemReady := FALSE;
    bPCS_Enable := FALSE;
    rPCSActivePowerCmd := 0.0;
    rPCSReactivePowerCmd := 0.0;
    rCryocoolerFlowCmd := rMaxFlowCmd; (* Maximize cooling to prevent boil-off *)
    rHeaterCmd := 0.0;
    bQuenchAlarm := FALSE;
    iState := 0;
    RETURN;
END_IF;

IF bQuenchDetect OR (rCoilTemperature > 6.8) OR (rHeBathLevel < 10.0) THEN
    (* Quench state requires immediate energy dump and PCS isolation *)
    bQuenchAlarm := TRUE;
    bPCS_Enable := FALSE;
    rPCSActivePowerCmd := 0.0;
    rPCSReactivePowerCmd := 0.0;
    rHeaterCmd := 100.0;               (* Fully activate dump resistors *)
    rCryocoolerFlowCmd := rMaxFlowCmd; (* Attempt to salvage remaining cold mass *)
    bSystemReady := FALSE;
    iState := 999;                     (* Latched Critical Fault State *)
    RETURN;
END_IF;

(* -------------------------------------------------------------------------
   LAYER 2: STATE-SPACE PREDICTIVE MODELING & CONTROL EXECUTION
   ------------------------------------------------------------------------- *)
CASE iState OF
    0: (* STATE: IDLE & SELF-DIAGNOSTICS *)
        bSystemReady := FALSE;
        rPCSActivePowerCmd := 0.0;
        rPCSReactivePowerCmd := 0.0;
        rCryocoolerFlowCmd := rMinFlowCmd;
        rHeaterCmd := 0.0;
        bPCS_Enable := FALSE;
        bQuenchAlarm := FALSE;
        bGridFaultAlarm := FALSE;
        bThermalWarning := FALSE;
        
        (* Reset integrators and observers *)
        rIntegralTerm := 0.0;
        rLastCurrentError := 0.0;
        
        IF bEnable AND (rCoilTemperature < 4.5) AND (rCryocoolerPressure > 12.0) THEN
            iState := 10;
        END_IF;

    10: (* STATE: CRYOCOOLER PRE-CONDITIONING (MPC THERMAL MANAGEMENT) *)
        (* Estimate AC losses based on current magnitude (I^2 * R_ac_equivalent) *)
        rEstimatedHeatLoad := (rCoilCurrent * rCoilCurrent) * 0.000025; 
        
        (* N-step ahead thermal prediction based on simple Euler integration *)
        rPredictedTempHorizon := rCoilTemperature + ((rEstimatedHeatLoad - (rCoilTemperature / rThermalResistance)) / rThermalCapacity) * 5.0; 
        
        IF rPredictedTempHorizon > 5.5 THEN
            bThermalWarning := TRUE;
            rCryocoolerFlowCmd := rMaxFlowCmd;
        ELSIF rPredictedTempHorizon > 4.8 THEN
            bThermalWarning := FALSE;
            rCryocoolerFlowCmd := rMaxFlowCmd * 0.75;
        ELSE
            bThermalWarning := FALSE;
            rCryocoolerFlowCmd := rMinFlowCmd * 2.0;
        END_IF;
        
        tStartupDelay(IN := TRUE, PT := T#15S);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* STATE: PCS SYNCHRONIZATION AND ACTIVE POWER DISPATCH *)
        bSystemReady := TRUE;
        
        (* Fault-Ride-Through (FRT) Grid Monitoring *)
        IF (rGridVoltage < 0.85 * 33000.0) OR (rGridVoltage > 1.15 * 33000.0) OR 
           (rGridFrequency < 49.0) OR (rGridFrequency > 51.0) THEN
            
            tGridFaultTimer(IN := TRUE, PT := T#0.25S); (* 250ms FRT limit *)
            IF tGridFaultTimer.Q THEN
                bGridFaultAlarm := TRUE;
                bPCS_Enable := FALSE;
                rPCSActivePowerCmd := 0.0;
                rPCSReactivePowerCmd := 0.0;
                iState := 30; (* Transition to Islanding / Fault state *)
            END_IF;
        ELSE
            tGridFaultTimer(IN := FALSE);
            bGridFaultAlarm := FALSE;
            bPCS_Enable := TRUE;
            
            (* State-Space Voltage Observer for DC Link *)
            rEstimatedDCLinkVolts := rEstimatedDCLinkVolts + rObserverGain * (rDCBusVoltage - rEstimatedDCLinkVolts);
            
            (* Non-Linear PID with Anti-Windup for Power Tracking *)
            rCurrentError := rPowerDemand - (rGridVoltage * rCoilCurrent * 0.000001732); (* Approx MW output for 3-phase *)
            
            (* Gain Scheduling based on error magnitude *)
            IF ABS(rCurrentError) > 10.0 THEN
                rKp := 4.0;
            ELSE
                rKp := 2.5;
            END_IF;
            
            rIntegralTerm := rIntegralTerm + (rCurrentError * rKi);
            (* Anti-Windup Limit *)
            IF rIntegralTerm > rWindupLimit THEN
                rIntegralTerm := rWindupLimit;
            ELSIF rIntegralTerm < -rWindupLimit THEN
                rIntegralTerm := -rWindupLimit;
            END_IF;
            
            rDerivativeTerm := (rCurrentError - rLastCurrentError) * rKd;
            rPCSActivePowerCmd := (rCurrentError * rKp) + rIntegralTerm + rDerivativeTerm;
            
            (* Output Saturation & Curtailment based on DC bus stability *)
            IF rEstimatedDCLinkVolts < 800.0 THEN
                rPCSActivePowerCmd := rPCSActivePowerCmd * 0.5; (* Derate if DC link sags *)
            END_IF;
            
            IF rPCSActivePowerCmd > 200.0 THEN
                rPCSActivePowerCmd := 200.0;
            ELSIF rPCSActivePowerCmd < -200.0 THEN
                rPCSActivePowerCmd := -200.0;
            END_IF;
            
            (* Provide reactive power support proportional to voltage sag/swell *)
            rPCSReactivePowerCmd := (33000.0 - rGridVoltage) * 0.05;
            
            rLastCurrentError := rCurrentError;
            
            (* Feed-forward thermal management during high ramp rates *)
            IF ABS(rPCSActivePowerCmd) > 100.0 THEN
                rCryocoolerFlowCmd := rMaxFlowCmd;
            ELSE
                rCryocoolerFlowCmd := rMinFlowCmd * 3.0;
            END_IF;
            
            (* Transition out if Enable dropped *)
            IF NOT bEnable THEN
                iState := 0;
            END_IF;
        END_IF;

    30: (* STATE: GRID FAULT RIDE-THROUGH (ISOLATION) *)
        bSystemReady := FALSE;
        rPCSActivePowerCmd := 0.0; (* Stop active pulsing *)
        
        (* Provide maximal reactive power support to grid during fault *)
        rPCSReactivePowerCmd := 100.0; 
        
        IF rGridVoltage >= 0.9 * 33000.0 AND rGridVoltage <= 1.1 * 33000.0 THEN
            iState := 10; (* Recover grid normal -> return to pre-conditioning *)
        END_IF;

    999: (* STATE: LATCHED QUENCH / CRITICAL FAULT *)
        (* System requires external hardware reset via SCADA and local key switch *)
        bQuenchAlarm := TRUE;
        rHeaterCmd := 100.0;
        bPCS_Enable := FALSE;
        bSystemReady := FALSE;
        rPCSActivePowerCmd := 0.0;
        rPCSReactivePowerCmd := 0.0;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
