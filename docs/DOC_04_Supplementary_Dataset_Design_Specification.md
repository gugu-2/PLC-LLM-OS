# DOC-04: Supplementary Dataset Design Specification

> **Classification**: Dataset Engineering Design Document  
> **Scope**: 6 new dataset types to complement the existing IEC-ST code corpus  
> **Date**: 2026-11-21  
> **Target**: Complete training data ecosystem for a world-class industrial automation LLM

---

## Context

The 870 existing datasets are **code emission pairs** — a prompt requests a Function Block, the assistant generates raw IEC-ST code. This covers exactly one of the many things an industrial automation LLM needs to do.

This document specifies **6 complementary dataset types** that together form a comprehensive training ecosystem. Each type targets a specific capability gap identified in DOC-01.

---

## Dataset Type 1: Dialogue-Format Explanation & Q&A Pairs

### Capability It Unlocks
The model can answer *engineering questions about PLC code* — not just emit it. Users will ask: "Why did you use a 12th-order state-space model?", "What does state 7 do?", "How do I tune the Q matrix?"

### Format
Multi-turn conversational exchange with engineering depth.

```json
{
  "messages": [
    {
      "role": "user",
      "content": "What is the purpose of the 2oo3 Triple Modular Redundancy (TMR) architecture in a hot strip mill AGC system?"
    },
    {
      "role": "assistant",
      "content": "In a hot-strip mill Automatic Gauge Control (AGC) system, the 2-out-of-3 (2oo3) TMR architecture serves as the primary safety and reliability mechanism for safety-critical sensor channels. Here is the engineering rationale:\n\n## Safety Context\nThe roll gap hydraulic servo valve receives a position command that directly controls strip thickness. A single-point sensor failure — if undetected — will drive the valve to either maximum extension (strip fracture) or full retract (over-roll, die breakage, potential catastrophic fire). In a 1,800 m/min hot-rolling environment, the response window is under 200 milliseconds.\n\n## How 2oo3 Works in This Context\nThree independent load cell channels (ChA, ChB, ChC) measure the same roll force simultaneously. The voting logic:\n1. Computes pairwise deviations: |A−B|, |B−C|, |C−A|\n2. If all three agree within ±0.5 MN: use median vote (most robust estimate)\n3. If one channel diverges beyond threshold AND disagreement persists > 25 ms (discrepancy timer): flag that channel as suspect, degrade to 1oo2 mean voting of the two agreeing channels, raise ISA-18.2 H alarm\n4. If two channels disagree: trip to fail-safe (hydraulic quick-open, roll separation) — this is the 2oo3 safety trip condition\n\n## Why Not 1oo2 or 1oo3?\n- 1oo2: One failure = immediate trip. Unacceptably low availability in a continuous production line running 20+ hours/day\n- 1oo3 (all must agree): One rogue sensor = false trip. Also unacceptable\n- 2oo3: Tolerates one sensor failure without production loss; requires two disagreeing sensors before tripping — this is the IEC 61511 SIL-2 compliant sweet spot\n\n## Practical Tuning\nThe 25 ms discrepancy timer is chosen to be:\n- Longer than normal transient noise (< 5 ms vibration spikes from the mill stand)\n- Shorter than the hydraulic servo response time (> 80 ms) so the system can react before the valve moves significantly"
    },
    {
      "role": "user",
      "content": "What happens to the 2oo3 logic when the mill is decelerating at the tail-out phase? Is there a risk of false trips from the speed-dependent vibration?"
    },
    {
      "role": "assistant",
      "content": "Excellent engineering question. Yes — tail-out deceleration is one of the most challenging conditions for TMR stability, and it must be specifically addressed in the FSM design.\n\n## The Problem\nDuring tail-out (FSM Stage 8: PASS_END_DECELERATION_STRIP_TAIL_TRACK), three physical effects combine to increase load cell noise:\n\n1. **Strip tail whip**: As the strip tail leaves the upstream coiler, tension drops asymmetrically causing a 2–5 Hz oscillatory force signature of ±1.5–3 MN amplitude\n2. **Rolling speed-dependent chatter**: At deceleration rates > 50 m/min/s, the work roll develops periodic chatter marks, exciting the mill housing at 15–45 Hz\n3. **Hydraulic decompression transients**: As roll force drops with the tail, the relief valve cycles, injecting hydraulic pressure oscillations at 8–12 Hz\n\nAll three are real physical signals, not sensor faults. If the TMR discrepancy timer (25 ms) is active during this phase, the 15–45 Hz chatter alone will trigger inter-channel divergence every few milliseconds.\n\n## The Solution: State-Dependent TMR Adaptation\n\nThe correct architecture uses the FSM state to modify TMR behavior:\n\n```iec-st\n(* TMR discrepancy timer adjustment based on FSM state *)\nIF State = STATE_DECELERATION_TAIL_OUT THEN\n    r_TMR_DiscrepancyThreshold := 5.0;    (* MN, relaxed from 0.5 MN *)\n    t_TMR_DiscrepancyTimer := T#100ms;    (* Extended from 25ms *)\n    b_TMR_AlarmSuppressed := TRUE;        (* Suppress H alarm during transient *)\nELSE\n    r_TMR_DiscrepancyThreshold := 0.5;    (* MN, normal *)\n    t_TMR_DiscrepancyTimer := T#25ms;     (* Normal *)\n    b_TMR_AlarmSuppressed := FALSE;\nEND_IF;\n```\n\nThis pattern — **FSM-state-conditional TMR tuning** — is a fundamental architectural requirement that many PLC implementations miss. The discrepancy threshold and timer must be a function of the operating mode, not a fixed value."
    }
  ]
}
```

### Generation Strategy
- Source: Extract specific technical sections from existing code datasets (TMR logic, MPC, FSM transitions)
- Use a "question generation agent" to auto-generate 3–5 questions per code section
- Use a "senior engineer answering agent" to generate expert answers without producing new code
- **Target volume**: 1,500–2,000 Q&A pairs
- **Minimum answer length**: 400 words (enforces depth, not glib responses)

---

## Dataset Type 2: Code Debugging & Fault Diagnosis Chains

### Capability It Unlocks
The model can receive **broken or incomplete PLC code** and identify what is wrong, explain the fault, and produce a corrected version. This is the most common real-world use case for an AI coding assistant.

### Format
3-turn debug chain: broken code presented → diagnosis → corrected code

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Here is a PLC Function Block for a 3,500-ton servo transfer press. The press is experiencing an intermittent force overshoot during the final coining stroke (FSM Stage 6). The overshoot reaches 15% above set point before the loop corrects. Can you identify the problem?\n\n```iec-st\n(* Simplified excerpt *)\nCASE State OF\n  6: (* COINING_FORCE_HOLD *)\n    r_ForceRef := r_CoinForce_SP;\n    r_ForceError := r_ForceRef - r_ForceMeasured_TMR;\n    r_ForceIntegral := r_ForceIntegral + (r_ForceError * r_Ki * r_ScanTime);\n    r_ForcePID_Out := (r_ForceError * r_Kp) + r_ForceIntegral;\n    r_HydroValveCmd := r_ForcePID_Out;\n```"
    },
    {
      "role": "assistant",
      "content": "I can identify **three compounding faults** in this code that together explain the 15% force overshoot.\n\n## Fault 1: No Anti-Windup on the Integral Term (Root Cause of Overshoot)\n\nThe integral `r_ForceIntegral` accumulates unclamped. During the rapid approach phase (Stage 4), the force is far below set point, so `r_ForceError` is large and positive. By the time the press contacts the workpiece at Stage 6, the integral has accumulated a large value — this is classic **integral windup**.\n\nWhen force suddenly rises at contact, the PID output includes this wound-up integral, driving the valve to maximum extension and causing the overshoot before the integrator can drain.\n\n**Fix**: Anti-windup clamp on the integral:\n```iec-st\nr_ForceIntegral := LIMIT(-r_IntegralClamp, r_ForceIntegral + (r_ForceError * r_Ki * r_ScanTime), r_IntegralClamp);\n```\n\n## Fault 2: No Force Rate-of-Change (dF/dt) Derivative Feed-Forward\n\nAt workpiece contact, force rises from 0 to coining force in < 50 ms. A pure P+I controller cannot respond fast enough — by the time the error is measured, the hydraulic column has already overshot.\n\n**Fix**: Add a force derivative term that anticipates the contact transient:\n```iec-st\nr_ForceDerivative := (r_ForceMeasured_TMR - r_ForcePrev) / r_ScanTime;\nr_ForcePID_Out := (r_ForceError * r_Kp) + r_ForceIntegral - (r_ForceDerivative * r_Kd);\nr_ForcePrev := r_ForceMeasured_TMR;\n```\n\n## Fault 3: No Valve Command Rate Limiter (Slew Rate)\n\nThe hydraulic servo valve has a physical slew rate limit (typically 150–300 bar/s). If `r_HydroValveCmd` changes by 100% in one scan cycle, the valve physically cannot follow — the internal valve PID goes into saturation, introducing its own oscillation.\n\n**Fix**: Rate-limit the valve command:\n```iec-st\nr_ValveCmdDelta := LIMIT(-r_ValveMaxSlew_PerScan, r_ForcePID_Out - r_HydroValveCmd, r_ValveMaxSlew_PerScan);\nr_HydroValveCmd := r_HydroValveCmd + r_ValveCmdDelta;\n```"
    },
    {
      "role": "user",
      "content": "Please provide the corrected Stage 6 control logic with all three fixes applied."
    },
    {
      "role": "assistant",
      "content": "```iec-st\n(* Stage 6: COINING_FORCE_HOLD - Corrected with anti-windup, derivative, and slew limiting *)\n6: \n    r_ForceRef := r_CoinForce_SP;\n    r_ForceError := r_ForceRef - r_ForceMeasured_TMR;\n    \n    (* FIX 1: Anti-windup clamped integral *)\n    r_ForceIntegral := LIMIT(\n        -r_IntegralClamp_MN,\n        r_ForceIntegral + (r_ForceError * r_Ki_Force * r_ScanTime_s),\n        r_IntegralClamp_MN\n    );\n    \n    (* FIX 2: Force derivative term for contact transient anticipation *)\n    r_ForceDerivative_MNs := (r_ForceMeasured_TMR - r_ForceMeasured_Prev) / r_ScanTime_s;\n    r_ForceMeasured_Prev := r_ForceMeasured_TMR;\n    \n    (* PID output with all three terms *)\n    r_ForcePID_Raw := (r_ForceError * r_Kp_Force)\n                    + r_ForceIntegral\n                    - (r_ForceDerivative_MNs * r_Kd_Force);\n    \n    (* FIX 3: Valve command slew rate limiter *)\n    r_ValveCmdDelta := LIMIT(\n        -r_ValveMaxSlew_PerScan,\n        r_ForcePID_Raw - r_HydroValveCmd,\n        r_ValveMaxSlew_PerScan\n    );\n    r_HydroValveCmd := r_HydroValveCmd + r_ValveCmdDelta;\n    \n    (* Force hold duration check *)\n    IF r_ForceMeasured_TMR >= (r_CoinForce_SP * 0.98) THEN\n        tCoinHoldTimer(IN := TRUE, PT := t_CoinHoldDuration);\n        IF tCoinHoldTimer.Q THEN\n            State := 7; (* Advance to decompression *)\n            tCoinHoldTimer(IN := FALSE);\n        END_IF;\n    END_IF;\n```"
    }
  ]
}
```

### Generation Strategy
- Take existing complete Function Blocks, deliberately introduce the 5 most common PLC bugs:
  1. Missing anti-windup → integral windup
  2. Missing derivative clamping → derivative kick
  3. No slew rate limiter → valve saturation
  4. Missing state entry guard → state re-entry on every scan
  5. No timeout guard on FSM state → deadlock on sensor failure
- Generate diagnosis turn using a "senior controls engineer" agent
- **Target volume**: 800–1,000 debug chains

---

## Dataset Type 3: Incremental Modification Tasks

### Capability It Unlocks
The model receives an **existing Function Block** and a modification request, and produces the updated code. This mirrors the most common real-world usage of an AI code assistant.

### Format

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Here is an existing IEC-ST Function Block for a 128-cavity PET preform injection molding machine:\n\n[EXISTING CODE HERE — 50,000 chars]\n\nTask: Extend this Function Block to add a 5-tier cavity pressure imbalance detection system using the existing 128-channel piezoelectric cavity pressure sensors. When pressure imbalance exceeds ±12% of mean cavity pressure, trigger a graduated response: (1) log to alarm buffer, (2) adjust melt temperature setpoint by ±0.5°C/cycle, (3) adjust injection velocity profile by ±2%, (4) if imbalance persists > 50 cycles: initiate hot runner gate balancing sequence, (5) if still unresolved after 100 cycles: schedule planned maintenance flag and reduce shot count to 96 cavities."
    },
    {
      "role": "assistant",
      "content": "I'll extend the Function Block with a 5-tier cavity pressure imbalance detection and correction system. Here are the new additions:\n\n[MODIFIED/EXTENDED CODE — adds only new logic without repeating unchanged sections]\n```iec-st\n(* === SECTION ADDITION: 5-TIER CAVITY PRESSURE IMBALANCE DETECTION === *)\n(* Insert after existing cavity pressure measurement block, before hot-runner PID *)\n\n(* Step 1: Compute mean and imbalance across all 128 cavities *)\nr_CavityPressure_Mean := 0.0;\nFOR i := 1 TO 128 DO\n    r_CavityPressure_Mean := r_CavityPressure_Mean + r_CavityPressure_arr[i];\nEND_FOR;\nr_CavityPressure_Mean := r_CavityPressure_Mean / 128.0;\n...\n```"
    }
  ]
}
```

### Generation Strategy
- Use pairs from existing corpus: take FB_A as the "base" and FB_B from the same sector as the "target"
- Extract the difference in features between the two (e.g., B has 128-cavity monitoring, A does not)
- Construct a modification request that describes the delta
- The answer shows only the new code additions (not the full repeated block)
- **Target volume**: 500–800 modification pairs

---

## Dataset Type 4: Concept-to-Code Translation (Knowledge Bridging)

### Capability It Unlocks
The model can translate **engineering theory into code**. A user provides a mathematical control concept ("I want a deadbeat observer for my casting machine"), and the model explains it and implements it.

### Format

```json
{
  "messages": [
    {
      "role": "user",
      "content": "What is Automatic Flatness Control (AFC) in cold strip rolling, and how is it typically implemented in PLC code using a segmented coolant spray bar?"
    },
    {
      "role": "assistant",
      "content": "## Automatic Flatness Control (AFC) in Cold Strip Rolling\n\n### Physical Principle\n[Engineering explanation — 300 words minimum]\n\n### PLC Implementation Strategy\n[Architecture decision rationale — 200 words]\n\n### Core IEC-ST Implementation\n```iec-st\n(* Complete AFC implementation for 40-zone spray bar *)\n...\n```"
    }
  ]
}
```

### Source Generation
- Extract technical concepts from existing code comments and variable names
- Generate "what is X and how do you implement it" questions for each concept
- Write comprehensive answers that explain theory first, then implement code
- **Target volume**: 600–800 concept-code pairs

---

## Dataset Type 5: Text Corpora for Language Modeling (Domain Pre-Training)

### Capability It Unlocks
Improves the model's understanding of industrial automation engineering language, terminology, standards, and reasoning patterns — independent of code generation.

### Corpus Sources (Actual Obtainable Data)

| Source | Data Type | Volume | Availability |
|---|---|---|---|
| IEC 61131-3 standard public summaries | Technical prose | ~100K tokens | Public |
| ISA-18.2 alarm management guidelines | Technical prose | ~150K tokens | ISA membership |
| IEC 61511 functional safety SIL methodology | Technical prose | ~200K tokens | Public summary |
| Wikipedia: Industrial control systems, PLC, SCADA | Encyclopedic | ~500K tokens | CC-BY-SA |
| OpenAutomation wiki pages | Technical reference | ~200K tokens | Public |
| Machine builder manuals (Siemens SINUMERIK, Beckhoff TwinCAT) | Technical/operational | ~1M tokens | Public |
| Academic papers: industrial control, MPC, process control (arXiv) | Research | ~2M tokens | Open Access |
| tc-open GitHub repository code comments | Code prose | ~100K tokens | MIT License |
| Automation Forums (PLCopen, Automation.com) | Discussion | ~300K tokens | Public |

### Processing Pipeline
```python
# For each source:
# 1. Extract plain text
# 2. Remove boilerplate (headers, footers, navigation)
# 3. Filter for minimum quality (> 100 words, English, technical content)
# 4. Deduplicate using MinHash LSH (threshold = 0.85 Jaccard)
# 5. Format as plain text chunks (512–2048 tokens per chunk)
```

**Target volume**: 5–10 million tokens of domain text

---

## Dataset Type 6: Safety & Functional Safety Scenario Dataset

### Capability It Unlocks
The model understands **industrial safety requirements** and can generate code that explicitly addresses SIL levels, safety function definitions, proof test intervals, and emergency shutdown logic.

### Format: Scenario-Based Safety Engineering

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Design a Safety Instrumented Function (SIF) for high-high pressure protection on a hydraulic forging press main cylinder. The SIF must achieve SIL-2 per IEC 61511. The process demand rate is 0.1 per year, the allowed PFDavg is < 0.001 (10^-3). Include proof test interval recommendations and partial stroke testing for the hydraulic dump valve."
    },
    {
      "role": "assistant",
      "content": "## SIF Design: High-High Hydraulic Pressure Protection (SIL-2)\n\n### Safety Requirement Specification (SRS)\n- **Safety Function**: De-energize hydraulic dump valve (SDV-001) on cylinder pressure ≥ P_HH\n- **Safe State**: SDV-001 open, cylinder pressure returns to atmospheric via accumulator vent\n- **SIL Target**: SIL-2 (PFDavg < 1×10⁻³)\n- **Process Demand Rate (λD)**: 0.1 per year (1 demand per 10 years)\n\n### Architecture Selection (IEC 61511 Table D.3)\n[Full SIL verification, 1oo2D architecture justification]\n\n### IEC-ST Safety Function Implementation\n```iec-st\n(* SIF: High-High Hydraulic Pressure — SIL-2 Certified Logic *)\nFUNCTION_BLOCK SIF_HH_HydraulicPressure_SIL2\n...\n```"
    }
  ]
}
```

**Target volume**: 200–300 SIF design scenarios across the 7 manufacturing sectors

---

## Summary: Complete Dataset Ecosystem

| Dataset Type | Format | Capability Unlocked | Target Volume | Priority |
|---|---|---|---|---|
| Existing code corpus (remediated) | Single-turn code emission | Generate IEC-ST Function Blocks | ~620 | Done |
| Type 1: Q&A Explanation Pairs | Multi-turn dialogue | Answer engineering questions | 1,500–2,000 | P0 |
| Type 2: Debug Chains | 3-turn diagnosis + fix | Debug and fix broken code | 800–1,000 | P0 |
| Type 3: Incremental Modification | 2-turn extension | Extend existing code | 500–800 | P1 |
| Type 4: Concept-to-Code | 2-turn theory+code | Bridge theory to implementation | 600–800 | P1 |
| Type 5: Domain Text Corpora | Raw text pre-training | Domain language & reasoning | 5–10M tokens | P1 |
| Type 6: Safety Scenarios | Multi-turn SIF design | Functional safety engineering | 200–300 | P2 |
