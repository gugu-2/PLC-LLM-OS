import json
import uuid
import os

prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data. Your specific domain is: Municipal UV Disinfection System. Task: Invent a highly complex control scenario for this domain (e.g., water transmittance profiling, quartz sleeve automatic wiper sequencing, and lamp ballast output regulation). Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

iec_st_code = """FUNCTION_BLOCK FB_UV_Disinfection_Controller
VAR_INPUT
    bEnableSystem : BOOL; (* Master enable *)
    rFlowRate_m3_h : REAL; (* Current influent flow rate *)
    rUVT_Percent : REAL; (* UV Transmittance 0.0 to 100.0% *)
    rTargetDose_mJ_cm2 : REAL; (* Desired target dose *)
    bWiperFault : BOOL; (* Input from wiper mechanism fault *)
    bLampFault : ARRAY[1..8] OF BOOL; (* Lamp fault inputs *)
    rWaterTemp_C : REAL; (* Water temperature *)
END_VAR

VAR_OUTPUT
    bSystemRunning : BOOL; (* Overall system running state *)
    rCalculatedDose : REAL; (* Real-time calculated dose *)
    rRequiredPower_kW : REAL; (* Required ballast power *)
    bLampEnable : ARRAY[1..8] OF BOOL; (* Enable signals for lamps *)
    rBallastOutput_Pct : ARRAY[1..8] OF REAL; (* Analog output to ballasts 50-100% *)
    bTriggerWipers : BOOL; (* Command to start wiper cycle *)
    bAlarmWiper : BOOL; (* Wiper alarm indicator *)
    bAlarmLowDose : BOOL; (* Low dose alarm indicator *)
END_VAR

VAR
    i : INT;
    rFlowFactor : REAL;
    rUVTFactor : REAL;
    rIntensity : REAL;
    tWiperTimer : TON;
    tWiperCycle : TIME := T#4H; (* Default wipe interval *)
    rMinBallastOut : REAL := 50.0;
    rMaxBallastOut : REAL := 100.0;
    rDoseMargin : REAL := 1.1; (* 10% safety margin *)
END_VAR

(* Calculate expected intensity based on UVT *)
rUVTFactor := EXPT(10.0, (rUVT_Percent - 100.0) / 10.0);
rIntensity := rRequiredPower_kW * rUVTFactor; (* Simplified model *)

(* Flow factor based on residence time *)
IF rFlowRate_m3_h > 0.0 THEN
    rFlowFactor := 1000.0 / rFlowRate_m3_h; 
ELSE
    rFlowFactor := 0.0;
END_IF;

(* Dose calculation *)
rCalculatedDose := rIntensity * rFlowFactor;

(* Ballast regulation loop *)
IF bEnableSystem THEN
    bSystemRunning := TRUE;
    
    (* Check dose and adjust power *)
    IF rCalculatedDose < (rTargetDose_mJ_cm2 * rDoseMargin) THEN
        rRequiredPower_kW := rRequiredPower_kW + 0.5;
    ELSIF rCalculatedDose > (rTargetDose_mJ_cm2 * 1.5) THEN
        rRequiredPower_kW := rRequiredPower_kW - 0.2;
    END_IF;
    
    (* Distribute power to lamps *)
    FOR i := 1 TO 8 DO
        IF NOT bLampFault[i] THEN
            bLampEnable[i] := TRUE;
            rBallastOutput_Pct[i] := rRequiredPower_kW / 8.0 * 100.0;
            
            IF rBallastOutput_Pct[i] > rMaxBallastOut THEN
                rBallastOutput_Pct[i] := rMaxBallastOut;
            ELSIF rBallastOutput_Pct[i] < rMinBallastOut THEN
                rBallastOutput_Pct[i] := rMinBallastOut;
            END_IF;
        ELSE
            bLampEnable[i] := FALSE;
            rBallastOutput_Pct[i] := 0.0;
        END_IF;
    END_FOR;
ELSE
    bSystemRunning := FALSE;
    FOR i := 1 TO 8 DO
        bLampEnable[i] := FALSE;
        rBallastOutput_Pct[i] := 0.0;
    END_FOR;
END_IF;

(* Wiper Sequence *)
tWiperTimer(IN := bSystemRunning AND NOT bTriggerWipers, PT := tWiperCycle);
IF tWiperTimer.Q THEN
    bTriggerWipers := TRUE;
END_IF;

IF bWiperFault THEN
    bAlarmWiper := TRUE;
    bTriggerWipers := FALSE;
END_IF;

(* Alarms *)
bAlarmLowDose := rCalculatedDose < rTargetDose_mJ_cm2;

END_FUNCTION_BLOCK
"""

content = f"```iec-st\n{iec_st_code}\n```"
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": content}]}

os.makedirs("C:/Users/majip/Downloads/LLM REASEARCH/gugu-2/PLC-LLM-OS/data/swarm_raw", exist_ok=True)
filename = f"C:/Users/majip/Downloads/LLM REASEARCH/gugu-2/PLC-LLM-OS/data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f)

# Also append to the data/synthetic_generation_v3_enterprise.jsonl file as requested in Agent System Instructions
jsonl_file = "C:/Users/majip/Downloads/LLM REASEARCH/gugu-2/PLC-LLM-OS/data/synthetic_generation_v3_enterprise.jsonl"
os.makedirs(os.path.dirname(jsonl_file), exist_ok=True)
with open(jsonl_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")

print(f"EVOLUTION COMPLETE: Municipal UV Disinfection System")
