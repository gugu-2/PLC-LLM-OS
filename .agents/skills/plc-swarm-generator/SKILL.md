---
name: plc-swarm-generator
description: Orchestrates concurrent multi-agent swarms (6 to 8 subagents) to generate ultra-dense, mathematically rigorous IEC 61131-3 Structured Text synthetic datasets.
---

# PLC Synthetic Data Swarm Skill

Use this skill when the user asks to generate synthetic datasets, start the swarm data loop, or run high-token concurrent subagents.

---

## 1. Domain Catalog (Rotate Across 8 Subagents)

When launching an 8-agent swarm wave, assign each agent one of these diverse domains:

1. **Nuclear Fusion**: Tokamak Tungsten Divertor Steady-State Detached Radiative Plasma Regime (`FB_FusionTokamak_Divertor_DetachedPlasmaFeedback`)
2. **Cryogenics**: Cryogenic Liquid Helium (4.2K to 1.8K) Superfluid Transition Cryostat (`FB_CryoHelium_SuperfluidHeII_LambdaTransition`)
3. **Deep-Sea**: 8,000-Meter Abyssal Research Seabed Coring Rig Active Heave Compensation (`FB_AbyssalCoring_DrillString_HeaveCompensator`)
4. **Biopharma**: Continuous Biopharmaceutical Downstream Tangential Flow Ultrafiltration & Diafiltration (`FB_Biopharma_ContinuousTFF_UltrafiltrationBufferSync`)
5. **Solar Thermal**: 1,800°C High-Flux Solar-Thermal Zinc Oxide (ZnO) Thermochemical Water-Splitting Reactor (`FB_SolarThermal_ZnO_ThermochemicalWaterSplitting`)
6. **Hydrogen Clean Energy**: 70-Bar High-Pressure PEM Electrolysis Hydrogen Dewatering & Temperature Swing Adsorption (`FB_HydrogenPEM_Dewatering_TSA_DesiccantCycle`)
7. **Aerospace Mobility**: Autonomous eVTOL Multi-Rotor Distributed Electric Propulsion (DEP) Tilt-Wing Transition (`FB_eVTOL_DEP_TiltWing_AeroTransitionSync`)
8. **Heavy Metallurgy**: 150-Ton Industrial AC Electric Arc Furnace (EAF) Dynamic Foaming Slag Optimization (`FB_EAF_FoamingSlag_MicrowaveRadar_CarbonInject`)

---

## 2. Subagent Invocation Template

Launch all 8 subagents in a single turn using `invoke_subagent`:

```json
{
  "TypeName": "SyntheticDataEvolverV3",
  "Role": "<Domain Architect Title>",
  "Model": "inherit",
  "Prompt": "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.\nYou possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.\nYou are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.\n\n**Your assigned domain is: <Domain Full Title and Scope>**\n\nCRITICAL RULES:\n1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).\n2. STRUCTURE:\n   a. First line: FUNCTION_BLOCK FB_<Name>\n   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units)\n   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)\n   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)\n   e. Multi-stage CASE machine with END_CASE;\n   f. Last line: END_FUNCTION_BLOCK\n3. LENGTH: Assistant content MUST be >= 3500 characters total (target 45,000 to 85,000+ chars).\n4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE.\n5. SAVE using this exact Python:\n   import json, uuid\n   prompt = \"\"\"<copy this exact user prompt here>\"\"\"\n   code = \"\"\"```iec-st\nFUNCTION_BLOCK FB_<Name>\n//...\nEND_FUNCTION_BLOCK\n```\"\"\"\n   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}\n   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:\n       json.dump(record, f, ensure_ascii=False)\n6. REPLY with: EVOLUTION COMPLETE: <Domain Full Title>"
}
```

---

## 3. Wave Completion & Looping
1. When all subagents respond with `EVOLUTION COMPLETE`, run verification:
   `python verify_dataset.py` or `python validate_iec.py`
2. If loop is enabled (*"never stop loop"*), spawn the next wave of 8 subagents immediately.
3. Save paths are always in `data/swarm_raw/agent_<uuid>.json`.
