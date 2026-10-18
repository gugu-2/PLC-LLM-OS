# builder.py - Generates FB_SOFC_TriGeneration_AnodeRecycleReformer
import json
import uuid
import re
import os

PROMPT_TEXT = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices ($A, B, C, D$), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Industrial Multi-Stack Solid Oxide Fuel Cell (SOFC) Microgrid Co-Generation: Dynamic Anode Gas Recirculation Ejector Entrainment Ratio, In-Situ Internal Methane Steam Reforming Endothermic Thermal Gradient Smoothing, and Electrochemical Impedance Spectroscopy (EIS) Carbon Coking Degradation Mitigation**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_SOFC_TriGeneration_AnodeRecycleReformer
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [A], [Nm3/h], [bar], [mol/mol], [deg C], [mOhm*cm2], [V], [%])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 55,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE.
5. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_SOFC_TriGeneration_AnodeRecycleReformer
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Industrial Multi-Stack Solid Oxide Fuel Cell (SOFC) Microgrid Co-Generation: Dynamic Anode Gas Recirculation Ejector Entrainment Ratio, In-Situ Internal Methane Steam Reforming Endothermic Thermal Gradient Smoothing, and Electrochemical Impedance Spectroscopy (EIS) Carbon Coking Degradation Mitigation"""

print(f"Prompt length: {len(PROMPT_TEXT)}")
