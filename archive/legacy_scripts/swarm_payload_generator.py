import json, uuid, os

os.makedirs('data/swarm_raw', exist_ok=True)
os.makedirs('data', exist_ok=True)

st_code = """```iec-st
FUNCTION_BLOCK FB_GeothermalBinaryCycleControl
TITLE = 'Geothermal Binary Cycle Power Plant Control'
VERSION : '2.1'
AUTHOR : 'Lumina Elite Synthetic Data Architect'

VAR_INPUT
    (* Physical Analog Inputs *)
    rProductionWellPress      : REAL; (* Bar *)
    rProductionWellTemp       : REAL; (* Deg C *)
    rBrineFlowRate            : REAL; (* kg/s *)
    rVaporizerLevel           : REAL; (* % *)
    rORCTurbineSpeed          : REAL; (* RPM *)
    rGridFrequency            : REAL; (* Hz *)
    rReinjectionWellLevel     : REAL; (* meters *)
    
    (* Physical Digital Inputs *)
    xGridSyncEnable           : BOOL; 
    xEmergencyStop            : BOOL;
    xPump1Ready               : BOOL;
    xPump2Ready               : BOOL;
    xPump3Ready               : BOOL;
    
    (* Setpoints *)
    rTargetTurbineSpeed       : REAL := 3000.0; (* RPM *)
    rTargetVaporizerLevel     : REAL := 50.0;   (* % *)
    rMaxBrinePressure         : REAL := 25.0;   (* Bar *)
END_VAR

VAR_OUTPUT
    (* Analog Outputs *)
    rWellheadThrottlePos      : REAL; (* 0-100% *)
    rORCTurbineGovernorVal    : REAL; (* 0-100% *)
    
    (* Digital Outputs *)
    xReinjectionPump1Cmd      : BOOL;
    xReinjectionPump2Cmd      : BOOL;
    xReinjectionPump3Cmd      : BOOL;
    xGridBreakerClose         : BOOL;
    xSystemAlarm              : BOOL;
    xTripTurbine              : BOOL;
END_VAR

VAR
    (* Internal State *)
    eState                    : INT := 0; (* 0:Stop, 1:Warmup, 2:RampUp, 3:Sync, 4:Run, 5:Trip *)
    
    (* PIDs and Controllers *)
    fbWellheadPID             : PID; 
    fbTurbineSpeedPID         : PID;
    fbVaporizerLevelPID       : PID;
    
    (* Timers *)
    tonWarmup                 : TON;
    tonSyncDelay              : TON;
    tonPumpStageDelay         : TON;
    
    (* Internal Variables *)
    rSpeedError               : REAL;
    rLevelError               : REAL;
    rFreqError                : REAL;
    iActivePumps              : INT := 0;
    xPumpStageUpReq           : BOOL;
    xPumpStageDnReq           : BOOL;
    rTotalReinjectFlow        : REAL;
END_VAR

(* 
   ================================================================================
   STATE MACHINE & SAFETY OVERRIDES
   ================================================================================
*)
IF xEmergencyStop THEN
    eState := 5; (* Trip *)
    xTripTurbine := TRUE;
    xSystemAlarm := TRUE;
END_IF;

CASE eState OF
    0: (* STOP STATE *)
        rWellheadThrottlePos := 0.0;
        rORCTurbineGovernorVal := 0.0;
        xReinjectionPump1Cmd := FALSE;
        xReinjectionPump2Cmd := FALSE;
        xReinjectionPump3Cmd := FALSE;
        xGridBreakerClose := FALSE;
        iActivePumps := 0;
        
        IF NOT xEmergencyStop AND rProductionWellTemp > 120.0 THEN
            eState := 1; (* Move to Warmup *)
        END_IF;

    1: (* WARMUP STATE *)
        (* Crack open wellhead to warm up vaporizer *)
        fbWellheadPID(EN:=TRUE, SP:=15.0, PV:=rProductionWellPress, KP:=1.2, KI:=0.5, KD:=0.1);
        rWellheadThrottlePos := fbWellheadPID.OUT;
        
        tonWarmup(IN:= (rVaporizerLevel > 20.0 AND rProductionWellTemp > 140.0), PT:=T#5M);
        
        IF tonWarmup.Q THEN
            eState := 2;
        END_IF;

    2: (* RAMP UP STATE *)
        (* Control Vaporizer Level by manipulating Brine Flow (Wellhead) *)
        fbVaporizerLevelPID(EN:=TRUE, SP:=rTargetVaporizerLevel, PV:=rVaporizerLevel, KP:=2.0, KI:=1.1, KD:=0.0);
        rWellheadThrottlePos := fbVaporizerLevelPID.OUT;
        
        (* Ramp Turbine Speed *)
        fbTurbineSpeedPID(EN:=TRUE, SP:=rTargetTurbineSpeed, PV:=rORCTurbineSpeed, KP:=5.0, KI:=2.5, KD:=0.5);
        rORCTurbineGovernorVal := fbTurbineSpeedPID.OUT;
        
        IF ABS(rORCTurbineSpeed - rTargetTurbineSpeed) < 10.0 THEN
            eState := 3;
        END_IF;

    3: (* SYNC STATE *)
        rFreqError := rGridFrequency - (rORCTurbineSpeed / 60.0);
        (* Fine-tune governor for phase matching *)
        IF ABS(rFreqError) < 0.05 AND xGridSyncEnable THEN
            tonSyncDelay(IN:=TRUE, PT:=T#2S);
            IF tonSyncDelay.Q THEN
                xGridBreakerClose := TRUE;
                eState := 4;
            END_IF;
        ELSE
            tonSyncDelay(IN:=FALSE);
            xGridBreakerClose := FALSE;
        END_IF;
        
    4: (* RUN STATE - NORMAL OPERATION *)
        (* Wellhead throttling to maintain maximum efficient extraction pressure *)
        fbWellheadPID(EN:=TRUE, SP:=rMaxBrinePressure - 2.0, PV:=rProductionWellPress, KP:=1.5, KI:=0.8, KD:=0.2);
        rWellheadThrottlePos := fbWellheadPID.OUT;
        
        (* Reinjection Pump Cascade Logic *)
        (* Evaluate staging based on well level and brine flow *)
        xPumpStageUpReq := (rReinjectionWellLevel > 80.0 OR rBrineFlowRate > 150.0) AND (iActivePumps < 3);
        xPumpStageDnReq := (rReinjectionWellLevel < 30.0 AND rBrineFlowRate < 50.0) AND (iActivePumps > 0);
        
        tonPumpStageDelay(IN:= (xPumpStageUpReq OR xPumpStageDnReq), PT:=T#10S);
        
        IF tonPumpStageDelay.Q THEN
            IF xPumpStageUpReq THEN
                iActivePumps := iActivePumps + 1;
            ELSIF xPumpStageDnReq THEN
                iActivePumps := iActivePumps - 1;
            END_IF;
        END_IF;
        
        (* Apply pump staging outputs *)
        xReinjectionPump1Cmd := (iActivePumps >= 1) AND xPump1Ready;
        xReinjectionPump2Cmd := (iActivePumps >= 2) AND xPump2Ready;
        xReinjectionPump3Cmd := (iActivePumps >= 3) AND xPump3Ready;
        
        (* Fallback Safety - Trip condition *)
        IF rORCTurbineSpeed > 3300.0 OR rProductionWellPress > 30.0 THEN
            eState := 5;
        END_IF;
        
    5: (* TRIP STATE *)
        rWellheadThrottlePos := 0.0;
        rORCTurbineGovernorVal := 0.0;
        xGridBreakerClose := FALSE;
        xTripTurbine := TRUE;
        
        IF NOT xEmergencyStop AND rORCTurbineSpeed < 100.0 THEN
            xTripTurbine := FALSE;
            eState := 0; (* Ready for restart *)
        END_IF;
END_CASE;

END_FUNCTION_BLOCK
```"""

prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\nYour specific domain is: Geothermal Binary Cycle Power Plant.\nTask: Invent a highly complex control scenario for this domain (e.g., organic Rankine fluid turbine speed matching, production wellhead throttling, and reinjection pump staging cascades)."
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": st_code}]}

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=4)
    
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
    
print(f"Saved to {filename} and appended to jsonl")
