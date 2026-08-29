import json, uuid, os

prompt = '''You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Pumped Hydro Energy Storage.
Task: Invent a highly complex control scenario for this domain (e.g., reversible Francis pump-turbine mode transition sequencing, penstock surge tank level mapping, and stator water cooling).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.'''

st_code = '''`iec-st
FUNCTION_BLOCK FB_PumpedHydroControl
VAR_INPUT
    bStartModeTransition : BOOL; (* Initiate mode transition *)
    eTargetMode : INT; (* 0: Standstill, 1: Generate, 2: Pump, 3: Synchronous Condenser *)
    
    (* Penstock and Surge Tank *)
    rUpperResLevel : REAL; (* meters *)
    rLowerResLevel : REAL; (* meters *)
    rSurgeTankLevel : REAL; (* meters *)
    rPenstockPressure : REAL; (* bar *)
    rPenstockFlow : REAL; (* m3/s *)
    
    (* Turbine/Pump parameters *)
    rRotorSpeed : REAL; (* RPM *)
    rGuideVanePosition : REAL; (* 0-100% *)
    bMainInletValveOpen : BOOL;
    bMainInletValveClosed : BOOL;
    
    (* Stator Water Cooling (SWC) *)
    rSWCTempIn : REAL; (* Celsius *)
    rSWCTempOut : REAL; (* Celsius *)
    rSWCFlow : REAL; (* L/min *)
    rSWCConductivity : REAL; (* uS/cm *)
    
    (* Grid constraints *)
    bGridSyncOk : BOOL;
    rActivePower : REAL; (* MW *)
END_VAR

VAR_OUTPUT
    eCurrentMode : INT;
    bTransitionInProgress : BOOL;
    bTransitionComplete : BOOL;
    bTransitionFault : BOOL;
    iErrorCode : INT;
    
    (* Actuator Commands *)
    rGuideVaneCmd : REAL;
    bMainInletValveCmd : BOOL;
    bExcitationEnable : BOOL;
    bSyncBreakerClose : BOOL;
    
    (* SWC Commands *)
    bSWCPumpCmd : BOOL;
    bSWCHeaterCmd : BOOL;
    
    (* Surge Protection *)
    bReliefValveCmd : BOOL;
END_VAR

VAR
    eState : INT; (* Internal state machine *)
    rHeadNet : REAL;
    rSurgeLimitUpper : REAL := 150.0;
    rSurgeLimitLower : REAL := 10.0;
    tTransitionTimer : TON;
    tSWCTimer : TON;
END_VAR

(* Calculate Net Head *)
rHeadNet := rUpperResLevel - rLowerResLevel;

(* Stator Water Cooling Logic *)
IF rSWCTempIn > 45.0 OR rSWCConductivity > 0.5 THEN
    bSWCPumpCmd := TRUE;
    iErrorCode := 101; (* SWC Warning *)
ELSIF rSWCTempIn < 15.0 THEN
    bSWCHeaterCmd := TRUE;
    bSWCPumpCmd := TRUE;
ELSE
    bSWCHeaterCmd := FALSE;
    bSWCPumpCmd := (eCurrentMode > 0);
END_IF;

(* Surge Tank Monitoring *)
IF rSurgeTankLevel > rSurgeLimitUpper OR rPenstockPressure > 50.0 THEN
    bReliefValveCmd := TRUE;
    iErrorCode := 201; (* Surge high *)
    IF eCurrentMode = 1 OR eCurrentMode = 2 THEN
        eTargetMode := 0; (* Emergency shutdown *)
        bStartModeTransition := TRUE;
    END_IF;
ELSE
    bReliefValveCmd := FALSE;
END_IF;

(* Mode Transition State Machine *)
tTransitionTimer(IN := bTransitionInProgress, PT := T#120s);

IF bStartModeTransition AND NOT bTransitionInProgress THEN
    bTransitionInProgress := TRUE;
    bTransitionComplete := FALSE;
    bTransitionFault := FALSE;
    eState := 10; (* Init Transition *)
END_IF;

IF bTransitionInProgress THEN
    CASE eState OF
        10: (* Initialize *)
            IF eCurrentMode = eTargetMode THEN
                bTransitionInProgress := FALSE;
                bTransitionComplete := TRUE;
            ELSE
                IF eCurrentMode = 0 AND eTargetMode = 1 THEN eState := 20; (* To Generate *)
                ELSIF eCurrentMode = 0 AND eTargetMode = 2 THEN eState := 30; (* To Pump *)
                ELSIF eTargetMode = 0 THEN eState := 90; (* To Standstill *)
                ELSE eState := 90; (* Default to shutdown first *)
                END_IF;
            END_IF;
            
        20: (* Generation: Open MIV *)
            bMainInletValveCmd := TRUE;
            IF bMainInletValveOpen THEN
                eState := 21;
            END_IF;
            
        21: (* Generation: Guide Vane to No-Load *)
            rGuideVaneCmd := 15.0; (* 15% opening *)
            IF rRotorSpeed >= 300.0 THEN (* Rated speed *)
                bExcitationEnable := TRUE;
                eState := 22;
            END_IF;
            
        22: (* Generation: Grid Sync *)
            IF bGridSyncOk THEN
                bSyncBreakerClose := TRUE;
                eCurrentMode := 1;
                bTransitionInProgress := FALSE;
                bTransitionComplete := TRUE;
            END_IF;
            
        30: (* Pumping: Start Sequence *)
            (* Assuming variable speed or static frequency converter start *)
            bMainInletValveCmd := TRUE;
            IF bMainInletValveOpen THEN
                eState := 31;
            END_IF;
            
        31: (* Pumping: Motor Start *)
            bExcitationEnable := TRUE;
            IF rRotorSpeed >= 300.0 AND bGridSyncOk THEN
                bSyncBreakerClose := TRUE;
                rGuideVaneCmd := 40.0; (* Optimal pump opening *)
                eCurrentMode := 2;
                bTransitionInProgress := FALSE;
                bTransitionComplete := TRUE;
            END_IF;
            
        90: (* Shutdown Sequence *)
            rGuideVaneCmd := 0.0;
            bSyncBreakerClose := FALSE;
            bExcitationEnable := FALSE;
            IF rRotorSpeed < 10.0 THEN
                bMainInletValveCmd := FALSE;
                IF bMainInletValveClosed THEN
                    eCurrentMode := 0;
                    bTransitionInProgress := FALSE;
                    bTransitionComplete := TRUE;
                END_IF;
            END_IF;
            
    END_CASE;
    
    (* Timeout protection *)
    IF tTransitionTimer.Q THEN
        bTransitionFault := TRUE;
        bTransitionInProgress := FALSE;
        iErrorCode := 301; (* Transition timeout *)
        eState := 90; (* Force shutdown *)
    END_IF;
END_IF;
END_FUNCTION_BLOCK
`'''

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": st_code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
os.makedirs("data/swarm_raw", exist_ok=True)
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
print("Saved to " + filename)
