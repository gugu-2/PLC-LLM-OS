import json
import os
import uuid

record = {
    "messages": [
        {
            "role": "user",
            "content": "Invent a highly complex control scenario for this domain (e.g., fractional distillation of liquid nitrogen/oxygen, turbo-expander efficiency mapping, and argon side-draw cascade control).\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."
        },
        {
            "role": "assistant",
            "content": "```iec-st\nFUNCTION_BLOCK FB_ASU_DistillationControl\nVAR_INPUT\n    rFeedTemp           : REAL; (* Main air feed temperature (K) *)\n    rFeedPress          : REAL; (* Main air feed pressure (bar) *)\n    rMainExchangerEff   : REAL; (* Heat exchanger efficiency (0-1) *)\n    rArgonDrawFlow      : REAL; (* Argon side-draw flow rate (kg/h) *)\n    bTurboTrip          : BOOL; (* Turbo-expander trip signal *)\n    bStartSequence      : BOOL;\n    bEmergencyStop      : BOOL;\nEND_VAR\nVAR_OUTPUT\n    rN2ProductFlow      : REAL;\n    rO2ProductFlow      : REAL;\n    rTurboSpeedCmd      : REAL;\n    rReboilerHeaterCmd  : REAL;\n    rRefluxValveCmd     : REAL;\n    bSystemStable       : BOOL;\n    bAlarmHighPress     : BOOL;\n    bAlarmLowTemp       : BOOL;\nEND_VAR\nVAR\n    eState              : DINT;\n    rInternalTemp       : REAL := 298.15;\n    rColumnPress        : REAL := 1.0;\n    rArgonPurity        : REAL := 0.0;\n    rLiquidLevel        : REAL := 0.0;\n    TimerStartup        : TON;\n    rTurboTargetSpeed   : REAL := 0.0;\nEND_VAR\n\n(* Main State Machine for Cryogenic Air Separation *)\nIF bEmergencyStop OR bTurboTrip THEN\n    eState := 5; (* SAFE_SHUTDOWN *)\nEND_IF;\n\nCASE eState OF\n    0: (* INIT *)\n        rN2ProductFlow := 0.0;\n        rO2ProductFlow := 0.0;\n        rTurboSpeedCmd := 0.0;\n        rReboilerHeaterCmd := 0.0;\n        rRefluxValveCmd := 0.0;\n        bSystemStable := FALSE;\n        IF bStartSequence THEN\n            eState := 1; (* STARTUP *)\n        END_IF;\n\n    1: (* STARTUP *)\n        rTurboTargetSpeed := 15000.0; (* RPM *)\n        TimerStartup(IN:=TRUE, PT:=T#5M);\n        IF TimerStartup.Q THEN\n            eState := 2; (* COOLING *)\n            TimerStartup(IN:=FALSE);\n        END_IF;\n\n    2: (* COOLING *)\n        rInternalTemp := rInternalTemp - (rMainExchangerEff * 2.5);\n        IF rInternalTemp < 90.0 THEN\n            bAlarmLowTemp := TRUE;\n        END_IF;\n        \n        IF rInternalTemp <= 100.0 THEN\n            eState := 3; (* DISTILLATION *)\n        END_IF;\n\n    3: (* DISTILLATION *)\n        rColumnPress := rFeedPress * 0.85;\n        IF rColumnPress > 6.5 THEN\n            bAlarmHighPress := TRUE;\n        END_IF;\n        \n        rN2ProductFlow := rFeedPress * 100.0 * (100.0 / rInternalTemp);\n        rO2ProductFlow := rFeedPress * 20.0 * (150.0 / rInternalTemp);\n        rReboilerHeaterCmd := 45.5; \n        \n        IF rArgonDrawFlow > 10.0 THEN\n            rArgonPurity := 98.5;\n        END_IF;\n        \n        IF ABS(rN2ProductFlow - 500.0) < 50.0 THEN\n            eState := 4; (* STABILIZATION *)\n        END_IF;\n\n    4: (* STABILIZATION *)\n        bSystemStable := TRUE;\n        IF rInternalTemp > 110.0 THEN\n            bSystemStable := FALSE;\n            eState := 3; (* DISTILLATION *)\n        END_IF;\n\n    5: (* SAFE_SHUTDOWN *)\n        rTurboSpeedCmd := 0.0;\n        rRefluxValveCmd := 0.0;\n        rReboilerHeaterCmd := 0.0;\n        bSystemStable := FALSE;\n        IF NOT bEmergencyStop AND NOT bTurboTrip THEN\n            eState := 0;\n        END_IF;\nEND_CASE;\nEND_FUNCTION_BLOCK\n```"
        }
    ]
}

os.makedirs('data/swarm_raw', exist_ok=True)

with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f)

with open('data/synthetic_generation_v3_enterprise.jsonl', 'a') as f:
    f.write(json.dumps(record) + '\n')
