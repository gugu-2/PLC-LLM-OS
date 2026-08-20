import json
import os

lines = [
    {
        "messages": [
            {"role": "user", "content": "Write an Allen-Bradley ST program for an automotive paint shop conveyor with RFID skid tracking, color change block valves, and oven bake temperature profiling."},
            {"role": "assistant", "content": "Here is the Base Code:\n```structured-text\nPROGRAM PaintShopBase\nVAR\n    RFID_SkidID : DINT;\n    TargetColor : INT;\n    Valve_Red, Valve_Blue, Valve_White, Valve_Solvent : BOOL;\n    OvenTemp_Zone1 : REAL;\n    Heater_Zone1 : REAL;\nEND_VAR\n\nIF RFID_SkidID > 0 THEN\n    TargetColor := DINT_TO_INT(RFID_SkidID MOD 3) + 1;\n    Valve_Red := (TargetColor = 1);\n    Valve_Blue := (TargetColor = 2);\n    Valve_White := (TargetColor = 3);\nELSE\n    Valve_Red := FALSE;\n    Valve_Blue := FALSE;\n    Valve_White := FALSE;\nEND_IF;\n\nIF OvenTemp_Zone1 < 120.0 THEN\n    Heater_Zone1 := 100.0;\nELSE\n    Heater_Zone1 := 0.0;\nEND_IF;\nEND_PROGRAM\n```"}
        ]
    },
    {
        "messages": [
            {"role": "user", "content": "Write an Allen-Bradley ST program for an automotive paint shop conveyor with RFID skid tracking, color change block valves, and oven bake temperature profiling. Make the task significantly harder by adding one critical sub-system: a robotic bell applicator purge and solvent recovery sequence."},
            {"role": "assistant", "content": "Here is Mutation 1 (Add Depth):\n```structured-text\nPROGRAM PaintShopMut1\nVAR\n    RFID_SkidID : DINT;\n    TargetColor : INT;\n    Valve_Red, Valve_Blue, Valve_White, Valve_Solvent : BOOL;\n    OvenTemp_Zone1, Heater_Zone1 : REAL;\n    \n    PurgeActive : BOOL;\n    PurgeTimer : TON;\n    RecoveryPump : BOOL;\nEND_VAR\n\nIF RFID_SkidID > 0 THEN\n    PurgeActive := TRUE;\nEND_IF;\n\nPurgeTimer(IN := PurgeActive, PT := T#5s);\nIF PurgeActive THEN\n    Valve_Solvent := TRUE;\n    RecoveryPump := TRUE;\n    Valve_Red := FALSE; Valve_Blue := FALSE; Valve_White := FALSE;\n    IF PurgeTimer.Q THEN\n        PurgeActive := FALSE;\n        Valve_Solvent := FALSE;\n        RecoveryPump := FALSE;\n    END_IF;\nELSE\n    TargetColor := DINT_TO_INT(RFID_SkidID MOD 3) + 1;\n    Valve_Red := (TargetColor = 1);\n    Valve_Blue := (TargetColor = 2);\n    Valve_White := (TargetColor = 3);\nEND_IF;\n\nHeater_Zone1 := SEL(OvenTemp_Zone1 < 120.0, 0.0, 100.0);\nEND_PROGRAM\n```"}
        ]
    },
    {
        "messages": [
            {"role": "user", "content": "Write an Allen-Bradley ST program for an automotive paint shop conveyor with RFID skid tracking, color change block valves, oven bake temperature profiling, and a robotic bell applicator purge and solvent recovery sequence. Additionally, include industrial communication (Ethernet/IP mapping) and comprehensive fault diagnostics for the entire system."},
            {"role": "assistant", "content": "Here is Mutation 2 (Add Breadth):\n```structured-text\nPROGRAM PaintShopMut2\nVAR\n    EIP_Status : DINT;\n    EIP_CommFault : BOOL;\n    RFID_SkidID : DINT;\n    TargetColor : INT;\n    Valve_Red, Valve_Solvent : BOOL;\n    OvenTemp_Zone1, Heater_Zone1 : REAL;\n    Fault_OvenTempHigh, Fault_PurgeTimeout, SystemFault : BOOL;\n    AlarmCode : INT;\n    PurgeActive : BOOL;\n    PurgeTimer : TON;\nEND_VAR\n\nIF OvenTemp_Zone1 > 180.0 THEN\n    Fault_OvenTempHigh := TRUE;\n    AlarmCode := 101;\nEND_IF;\n\nEIP_CommFault := (EIP_Status <> 16#0000);\nIF EIP_CommFault THEN\n    SystemFault := TRUE;\n    AlarmCode := 999;\nEND_IF;\n\nIF NOT SystemFault AND NOT Fault_OvenTempHigh THEN\n    IF RFID_SkidID > 0 THEN PurgeActive := TRUE; END_IF;\n    PurgeTimer(IN := PurgeActive, PT := T#5s);\n    IF PurgeActive THEN\n        Valve_Solvent := TRUE;\n        IF PurgeTimer.Q THEN PurgeActive := FALSE; END_IF;\n    END_IF;\n    Heater_Zone1 := SEL(OvenTemp_Zone1 < 120.0, 0.0, 100.0);\nELSE\n    Valve_Red := FALSE;\n    Valve_Solvent := FALSE;\n    Heater_Zone1 := 0.0;\n    PurgeActive := FALSE;\nEND_IF;\nEND_PROGRAM\n```"}
        ]
    },
    {
        "messages": [
            {"role": "user", "content": "Write an Allen-Bradley ST program for an automotive paint shop conveyor with RFID skid tracking, color change block valves, oven bake temperature profiling, a robotic bell applicator purge sequence, Ethernet/IP mapping, and fault diagnostics. Furthermore, implement IEC 62443 cybersecurity access levels, PLC redundancy failover logic, and SCADA integration tags."},
            {"role": "assistant", "content": "Here is Mutation 3 (Add Reasoning):\n```structured-text\nPROGRAM PaintShopMut3\nVAR\n    SCADA_Heartbeat : DINT;\n    Sec_AccessLevel : INT;\n    Auth_Token : DINT;\n    PLC_IsPrimary : BOOL;\n    FailoverTrigger : BOOL;\n    RFID_SkidID : DINT;\n    SystemFault : BOOL;\n    Valve_Red : BOOL;\n    OvenTemp_Zone1, Heater_Zone1 : REAL;\nEND_VAR\n\nIF Auth_Token = 16#ABCD AND Sec_AccessLevel >= 2 THEN\n    // Authorized parameter changes allowed\nEND_IF;\n\nIF SCADA_Heartbeat = 0 OR SystemFault THEN\n    FailoverTrigger := TRUE;\nEND_IF;\n\nIF PLC_IsPrimary AND NOT FailoverTrigger THEN\n    Heater_Zone1 := SEL(OvenTemp_Zone1 < 120.0, 0.0, 100.0);\n    IF RFID_SkidID > 0 THEN Valve_Red := TRUE; END_IF;\nELSE\n    Heater_Zone1 := 0.0;\n    Valve_Red := FALSE;\nEND_IF;\nEND_PROGRAM\n```"}
        ]
    },
    {
        "messages": [
            {"role": "user", "content": "Write an Allen-Bradley ST program for an automotive paint shop conveyor with RFID skid tracking, color change block valves, oven bake temperature profiling, a robotic bell applicator purge sequence, Ethernet/IP mapping, fault diagnostics, cybersecurity access levels, failover logic, and SCADA integration tags. Ensure the program is robust against adversarial conditions by adding sensor drift detection algorithms, Hardware-in-the-Loop (HIL) digital twin synchronization hooks, and a pre-production self-test routine."},
            {"role": "assistant", "content": "Here is Mutation 4 (Add Adversarial):\n```structured-text\nPROGRAM PaintShopMut4\nVAR\n    PLC_IsPrimary : BOOL;\n    SystemFault : BOOL;\n    OvenTemp_Sensor1, OvenTemp_Sensor2 : REAL;\n    Drift_Alarm : BOOL;\n    HIL_Mode : BOOL;\n    HIL_SimTemp : REAL;\n    SelfTest_Active : BOOL;\n    SelfTest_Step : INT;\n    Heater_Zone1 : REAL;\nEND_VAR\n\nIF ABS(OvenTemp_Sensor1 - OvenTemp_Sensor2) > 5.0 THEN\n    Drift_Alarm := TRUE;\n    SystemFault := TRUE;\nEND_IF;\n\nIF HIL_Mode THEN\n    OvenTemp_Sensor1 := HIL_SimTemp;\n    OvenTemp_Sensor2 := HIL_SimTemp;\nEND_IF;\n\nIF SelfTest_Active THEN\n    CASE SelfTest_Step OF\n        0:\n            Heater_Zone1 := 0.0;\n            SelfTest_Step := 1;\n        1:\n            IF OvenTemp_Sensor1 < 50.0 THEN SelfTest_Step := 2; END_IF;\n        2:\n            SelfTest_Active := FALSE;\n    END_CASE;\nELSIF PLC_IsPrimary AND NOT SystemFault THEN\n    Heater_Zone1 := SEL(OvenTemp_Sensor1 < 120.0, 0.0, 100.0);\nELSE\n    Heater_Zone1 := 0.0;\nEND_IF;\nEND_PROGRAM\n```"}
        ]
    }
]

os.makedirs(r'C:\Users\majip\Downloads\LLM REASEARCH\data\swarm_outputs', exist_ok=True)
with open(r'C:\Users\majip\Downloads\LLM REASEARCH\data\swarm_outputs\seed_142.jsonl', 'w', encoding='utf-8') as f:
    for line in lines:
        f.write(json.dumps(line) + '\n')
