# DOC-04: Structural & Task-Specific Dataset Engineering Specification

**Classification**: Training Data Architecture Specification & Dataset Design Document  
**System**: Lumina Cyber-Physical Multi-Modal Training Ecosystem  
**Target Scope**: 6 Supplementary Dataset Archetypes Complementing the IEC-ST Code Corpus  
**Author**: Lumina Engineering Review Board & Principal Automation Fellow  
**Date**: November 23, 2026  
**Status**: APPROVED & OPERATIONAL SPECIFICATION  
**Companion Docs**: DOC-01 (Pathology), DOC-02 (Architecture), DOC-03 (Fine-Tuning), DOC-05 (Pipeline Guide)

---

## 1. Executive Summary: The Need for Multi-Modal Data Diversity

The 870 original datasets in `data/swarm_raw/` represent a single data format: **single-turn code emission pairs** (a system specification prompt followed by a monolithic Function Block). As demonstrated in DOC-01, training an LLM exclusively on code emission pairs produces a "code-spewing automaton" that cannot engage in conversational engineering, cannot troubleshoot broken code, cannot explain its architectural choices, and has no grounding in real-world automation standards.

To build an enterprise-ready **Industrial Automation Co-Pilot & Engineering Assistant**, the training distribution must be diversified across six complementary dataset archetypes:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                      LUMINA MULTI-MODAL DATASET ECOSYSTEM                              │
│                                                                                        │
│  [Code Generation]          [Conversational AI]         [Diagnostic & Troubleshooting] │
│  Verified IEC-ST Blocks     Type 1: Technical Dialogue  Type 2: 3-Turn Debug Chains    │
│  (~503 Clean Datasets)      (1,500 - 2,000 Pairs)       (800 - 1,000 Chains)           │
│                                                                                        │
│  [Brownfield Engineering]   [Theory-to-Execution]       [Foundation Pre-Training]      │
│  Type 3: Code Modification  Type 4: Concept-to-Code     Type 5: Domain Text Corpora    │
│  (500 - 800 Tasks)          (600 - 800 Bridges)         (5 - 10 Million Tokens)        │
│                                                                                        │
│  [Functional Safety]                                                                   │
│  Type 6: Safety SIF Logic                                                              │
│  (200 - 300 Certified SIFs)                                                            │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Dataset Type 1: Technical Dialogues & Support Bot Q&A Pairs

### 2.1 Capability It Unlocks
Transforms the model into an interactive technical support agent and consultative automation peer. The model learns to answer *why* specific engineering decisions are made, analyze architectural trade-offs, and guide engineers through complex control loop commissioning without simply dumping unrequested code.

### 2.2 Target Volume & Specifications
- **Target Volume**: 1,500 – 2,000 multi-turn exchanges.
- **Turn Count**: 2 to 4 turns per conversation.
- **Response Depth**: $\ge 400$ words per assistant turn. Must include mathematical equations, standards citations, and structured Markdown tables/diagrams.
- **Target Topics**:
  - 2oo3 TMR vs. 1oo2/1oo3 safety and availability trade-offs under IEC 61511 SIL-2.
  - Tuning Model Predictive Control (MPC) $Q$ state penalty vs. $R$ actuator effort matrices.
  - Mitigating derivative kick and integral windup in high-inertia hydraulic and thermal loops.
  - Designing bumpless manual-to-automatic PID transfer functions.
  - Dynamic adaptation of discrepancy timers during mechanical machine transients.

### 2.3 Concrete Industrial Example: 2oo3 TMR Architecture in Hot Strip Mill AGC
```json
{
  "id": "dialogue_qa_steelmaking_tmr_agc_80ca812b",
  "dataset_type": "type_1_dialogue_qa",
  "topic": "TMR_HotStripMill_AGC",
  "sector": "steelmaking",
  "system": "6-High Cold Mill AGC Roll Force Control",
  "schema_version": "2.0",
  "messages": [
    {
      "role": "user",
      "content": "What is the engineering rationale for implementing a 2oo3 Triple Modular Redundancy (TMR) architecture on roll force load cells in a hot strip mill Automatic Gauge Control (AGC) system?"
    },
    {
      "role": "assistant",
      "content": "In a continuous hot strip mill Automatic Gauge Control (AGC) system, the 2-out-of-3 (2oo3) TMR architecture serves as the primary cyber-physical barrier against catastrophic roll bite failure.\n\n### 1. The Physical Hazard & Safety Context\nIn a 6-high finishing stand, the hydraulic roll gap cylinders exert between 35 to 55 Meganewtons (MN) of roll force on a steel strip moving at up to 1,800 m/min. The process response window is under 30 milliseconds. If a single load cell suffers an open-circuit failure or bridge drift while under load, a naive single-channel controller would interpret the sudden loss of force as a massive strip thickness drop. The controller would drive the hydraulic servo cylinders to maximum stroke in under 100 ms, causing severe roll bite freeze, work roll spalling, strip necking/fracture, and catastrophic mill stall.\n\n### 2. Comparative Reliability Architecture Analysis\n\n| Architecture | Trip Condition | Production Availability | Safety Integrity (IEC 61511) | Real-World Feasibility in Hot Rolling |\n|---|---|:---:|:---:|---|\n| **1oo1 (Single)** | Any failure blinds loop | Poor (Single point of failure) | Non-compliant (SIL-0) | Unacceptable risk of equipment destruction. |\n| **1oo2 (Dual)** | Either sensor trips system | Unacceptably low (Nuisance trips) | High (SIL-2 / SIL-3) | A transient noise spike trips a 24/7 continuous line. |\n| **1oo3 (Triplicate)**| All 3 must agree to trip | High availability | Dangerous (Blind to 1 rogue sensor) | Single frozen load cell prevents emergency trip. |\n| **2oo3 (TMR)** | 2 agreeing sensors govern | **Optimal (Continuous uptime)** | **SIL-2 Compliant (Low PFDavg)** | **Industrial Standard**: Discards 1 failed sensor seamlessly. |\n\n### 3. Voting Mechanics & Discrepancy Filtering\nThree independent load cell channels (ChA, ChB, ChC) measure simultaneous force. The voting algorithm executes in scan time (typically $T_s = 5\\text{ ms}$):\n1. Computes pairwise differences: $\\Delta_{AB} = |A - B|$, $\\Delta_{BC} = |B - C|$, $\\Delta_{CA} = |C - A|$.\n2. Selects the median channel value as the feedback signal.\n3. If any single channel deviates by more than the deviation threshold (typically $\\delta = \\pm 0.5\\text{ MN}$) for longer than the discrepancy persistence timer ($t_d = 25\\text{ ms}$), that channel is flagged as SUSPECT, latches an ISA-18.2 Warning alarm, and the voting degrades to a 1oo2 average of the remaining two healthy channels without disturbing the hydraulic valve position."
    },
    {
      "role": "user",
      "content": "During mill tail-out deceleration, the strip tail whips as it leaves the roll bite. Won't the mechanical vibration cause false discrepancy trips if the timer is fixed at 25 ms?"
    },
    {
      "role": "assistant",
      "content": "Yes, tail-out deceleration is the single greatest cause of nuisance trips in hot strip mills. When the strip tail leaves the roll bite, tension collapses instantaneously, generating an asymmetric 2–5 Hz mechanical whip with force oscillations of $\\pm 2.0\\text{ to } \\pm 3.5\\text{ MN}$. A static $25\\text{ ms}$ discrepancy filter calibrated for steady-state rolling ($\\\\pm 0.5\\text{ MN}$) will trip the mill on every coil.\n\n### The Architectural Fix: State-Dependent TMR Adaptation\nThe correct engineering solution is **FSM-State-Conditional TMR Adaptation**, where the Finite State Machine modifies the discrepancy threshold and filter time based on the active rolling stage:\n\n```iec-st\n(* State-Dependent TMR Adaptation during Tail-Out Deceleration *)\nIF State = STATE_TAILOUT_DECEL THEN\n    r_TMR_DiscrepancyThreshold := 3.5;    (* Widened from 0.5 MN to absorb tail whip *)\n    t_TMR_DiscrepancyTimer := T#120ms;    (* Extended from 25ms to bridge transient *)\n    b_TMR_AlarmSuppressed := TRUE;       (* Suppress nuisance alarms per ISA-18.2 *)\nELSE\n    r_TMR_DiscrepancyThreshold := 0.5;    (* Normal steady-state tolerance [MN] *)\n    t_TMR_DiscrepancyTimer := T#25ms;     (* Tight response for steady-state safety *)\n    b_TMR_AlarmSuppressed := FALSE;\nEND_IF;\n```\n\nThis architecture guarantees both zero false trips during mechanical tail whip and full SIL-2 safety integrity during steady-state production."
    }
  ]
}
```

### 2.4 Concrete Customer Example: Motorcycle Factory Robotic Frame Welding & Jig Clamping Dialogue
```json
{
  "id": "dialogue_qa_bike_frame_welding_91dc38a4",
  "dataset_type": "type_1_dialogue_qa",
  "topic": "Motorcycle_Frame_RoboticWeld_Thermal_Compensation",
  "sector": "automotive",
  "subsector": "bike_motorcycle_manufacturing",
  "system": "Robotic Motorcycle Tubular Frame Jig & Multi-Pass MIG Station",
  "schema_version": "2.0",
  "messages": [
    {
      "role": "user",
      "content": "In our motorcycle assembly plant, we are experiencing steering head tube distortion and angle variance (>0.35 deg) on our tubular chrome-moly bike frame line after robotic MIG welding. How should our PLC coordinator sequence the hydraulic clamping cylinders and torch progression to prevent frame warping?"
    },
    {
      "role": "assistant",
      "content": "Steering head angle tolerance on a high-speed motorcycle chassis must remain within $\\pm 0.10^\\circ$ to guarantee directional high-speed stability and prevent dangerous tank-slapper oscillations. Chrome-moly (25CrMo4) tubing experiences intense asymmetric thermal contraction when welded sequentially in a fixed rigid clamp.\n\n### 1. Root Cause of Frame Distortion\nWhen steering head tube seams are welded continuously from top to bottom, the heat-affected zone (HAZ) creates a progressive thermal moment about the chassis centerline. Rigid hydraulic clamping without thermal stress-relief sequencing traps tensile stresses up to $420\\text{ MPa}$. Upon hydraulic clamp de-energization, elastic spring-back pulls the steering head angle out of specification.\n\n### 2. Cyber-Physical Sequence Architecture\nTo eliminate frame distortion, the PLC must execute a **Symmetric Staggered Sequence with Adaptive Force-Controlled Clamping**:\n\n```mermaid\nflowchart TD\n    A[Clamp Engagement: Hydraulic Proportional Pressure 120 bar] --> B[Symmetric Tack Welding: 4-Point Opposed Micro-Tacks]\n    B --> C[Pass 1: Left Gusset Seam 50% Travel]\n    C --> D[Pass 2: Right Gusset Seam 50% Travel - Heat Balancing]\n    D --> E[Hydraulic Clamp Relieve to 35 bar Floating Holding State]\n    E --> F[Pass 3 & 4: Opposed Interrupted Bead Completion]\n    F --> G[Controlled Post-Weld Nitrogen Quench & Clamp Release]\n```\n\n### 3. Structured Text FSM Implementation\n```iec-st\n(* Motorcycle Frame Welding Jig Proportional Clamp State Control *)\nCASE eWeldSequence OF\n    WELD_SEQ_INITIAL_CLAMP:\n        r_HydraulicClamp_PressureSP := 120.0; (* Rigid lock for tacking [bar] *)\n        IF b_AllJigProximitySensors_OK AND (r_HydraulicClamp_ActualPressure >= 115.0) THEN\n            b_RobotWeld_Permissive := TRUE;\n            eWeldSequence := WELD_SEQ_OPPOSED_TACKING;\n        END_IF;\n\n    WELD_SEQ_THERMAL_FLOAT:\n        (* Relieve hydraulic clamping during main root pass to allow axial thermal expansion *)\n        r_HydraulicClamp_PressureSP := 35.0;  (* Floating retention pressure [bar] *)\n        IF (r_HeadTube_PyrometerTemp >= 380.0) THEN\n            (* Compensate weld travel speed dynamically based on heat buildup *)\n            r_RobotTravelSpeed_Setpoint := 8.5; (* Speed up travel [mm/s] to restrict heat input *)\n        END_IF;\nEND_CASE;\n```\nThis sequence reduces angular distortion below $\\pm 0.08^\\circ$ consistently across two-wheeler production shifts."
    }
  ]
}
```

---

## 3. Dataset Type 2: Code Debugging & Fault Diagnosis Chains

### 3.1 Capability It Unlocks
Empowers the model to serve as a **real-time diagnostic co-pilot**. In production, controls engineers spend $>60\%$ of their time troubleshooting existing malfunctioning code rather than writing greenfield programs. This dataset trains the model to identify subtle runtime failure modes (integral windup, derivative kick, valve spool cavitation, FSM deadlocks) and synthesize verified corrections.

### 3.2 Target Volume & Specifications
- **Target Volume**: 800 – 1,000 3-turn debug chains.
- **Structure**:
  - `Turn 1 (User)`: Operational symptom report + excerpt of broken Structured Text code.
  - `Turn 2 (Assistant)`: Detailed root-cause diagnosis identifying the compounding physical and algorithmic flaws.
  - `Turn 3 (User)`: Request for complete, corrected code.
  - `Turn 4 (Assistant)`: Fully verified Structured Text code with defensive clamps, rate limiters, and FSM transition guards.
- **Common Fault Archetypes**:
  1. *Integral Windup*: Unclamped accumulators during actuator saturation or workpiece approach phases.
  2. *Derivative Kick*: Unfiltered differentiation on setpoint steps causing output spikes.
  3. *Valve Slew Saturation*: Demanding step changes exceeding hydraulic spool bandwidth.
  4. *State Deadlocks*: `CASE` branches missing outgoing transitions when unexpected error conditions occur.
  5. *Matrix Inversion Singularities*: Ill-conditioned online matrix updates causing divide-by-zero traps.

### 3.3 Concrete Industrial Example: Press Force Overshoot & Die Cracking
```json
{
  "id": "debug_chain_heavy_machinery_press_overshoot_ff7381c3",
  "dataset_type": "type_2_debug_chain",
  "fault_type": "Integral_Windup_Press_Overshoot",
  "sector": "heavy_machinery",
  "system": "2,500-Ton Servo Stamping Press Coining Stage",
  "schema_version": "2.0",
  "messages": [
    {
      "role": "user",
      "content": "We are commissioning a 2,500-ton servo stamping press. During the coining stroke (FSM Stage 6), the press experiences a 14% force overshoot above the 22 MN setpoint before settling. This is causing micro-cracking in our automotive stamping dies. Here is our current Structured Text logic:\n\n```iec-st\n(* Stage 6: Coining Force Hold *)\n6: \n    r_ForceError := r_TargetCoinForce - r_MeasuredForce_TMR;\n    r_ForceIntegral := r_ForceIntegral + (r_ForceError * r_Ki * r_CycleTime);\n    r_ServoCmd := (r_ForceError * r_Kp) + r_ForceIntegral;\n    r_HydraulicValveOutput := r_ServoCmd;\n```\n\nWhat is causing this overshoot and how do we fix it?"
    },
    {
      "role": "assistant",
      "content": "I can identify **three compounding flaws** in this control loop that together explain the 14% force overshoot:\n\n### 1. Unbounded Integral Windup (Primary Root Cause)\nDuring the rapid ram approach (Stages 4 and 5), the workpiece has not yet been contacted. The force error ($r\\_TargetCoinForce - r\\_MeasuredForce$) remains massive (~22 MN) for over 400 milliseconds. Because `r_ForceIntegral` is unclamped, it accumulates an enormous value. When the tooling contacts the sheet metal, the force rises sharply, but the wound-up integral prevents the servo output from decreasing, driving the hydraulic cylinder to maximum force and causing the 14% die overshoot.\n\n### 2. Lack of Derivative Contact Anticipation\nContact between die and sheet metal is a discontinuous stiffness jump (from air to steel die stiffness in $<30\\text{ ms}$). A pure PI loop only reacts *after* error accumulates. A derivative term on force ($dF/dt$) is required to act as an immediate hydraulic brake the instant the rate-of-force rises.\n\n### 3. Missing Valve Slew Rate Limiter\nYour hydraulic proportional valve has a physical spool slew bandwidth limit (~150 bar/s). Driving `r_HydraulicValveOutput` directly from the raw PID step change forces the valve into saturation, inducing cavitation and secondary pressure resonance."
    },
    {
      "role": "user",
      "content": "Please rewrite the Stage 6 logic in IEC 61131-3 with all three issues corrected."
    },
    {
      "role": "assistant",
      "content": "```iec-st\n(* Stage 6: Coining Force Hold with Anti-Windup, Derivative Lead, and Slew-Limiter *)\n6: \n    r_ForceError := r_TargetCoinForce - r_MeasuredForce_TMR;\n    \n    (* FIX 1: Clamped Anti-Windup Integration *)\n    r_ForceIntegral := LIMIT(\n        -r_MaxIntegralClamp_MN,\n        r_ForceIntegral + (r_ForceError * r_Ki_Force * r_ScanTime_s),\n        r_MaxIntegralClamp_MN\n    );\n    \n    (* FIX 2: Contact Derivative Lead (dF/dt with 1st-order low-pass filter) *)\n    r_dF_dt_raw := (r_MeasuredForce_TMR - r_MeasuredForce_Prev) / r_ScanTime_s;\n    r_dF_dt_filtered := r_dF_dt_filtered + (r_ScanTime_s / (r_FilterTimeConst_s + r_ScanTime_s)) * (r_dF_dt_raw - r_dF_dt_filtered);\n    r_MeasuredForce_Prev := r_MeasuredForce_TMR;\n    \n    (* PID Output Synthesis with Derivative Subtraction *)\n    r_ServoCmd_Raw := (r_ForceError * r_Kp_Force) \n                    + r_ForceIntegral \n                    - (r_dF_dt_filtered * r_Kd_Force);\n    \n    (* FIX 3: Slew Rate Limiter to Protect Hydraulic Spool *)\n    r_ValveDelta := LIMIT(-r_MaxValveSlew_PerScan, r_ServoCmd_Raw - r_HydraulicValveOutput, r_MaxValveSlew_PerScan);\n    r_HydraulicValveOutput := r_HydraulicValveOutput + r_ValveDelta;\n    \n    (* Deterministic Coining Dwell Timer *)\n    IF r_MeasuredForce_TMR >= (r_TargetCoinForce * 0.985) THEN\n        ton_CoiningDwell(IN := TRUE, PT := t_CoiningDwellTime);\n        IF ton_CoiningDwell.Q THEN\n            ton_CoiningDwell(IN := FALSE);\n            State := 7; (* Advance to controlled hydraulic decompression *)\n        END_IF;\n    ELSE\n        ton_CoiningDwell(IN := FALSE);\n    END_IF;\n```"
    }
  ]
}
```

---

## 4. Dataset Type 3: Brownfield Incremental Code Modification

### 4.1 Capability It Unlocks
Enables the model to ingest an **existing Function Block stub** or legacy controller and modularly inject advanced capabilities (e.g., adding multi-cavity pressure balancing to injection molding, integrating thermal spindle compensation into a CNC mill) without rewriting or breaking the surrounding I/O structure.

### 4.2 Target Volume & Specifications
- **Target Volume**: 500 – 800 tasks.
- **Format**: User supplies existing baseline block + requested functional enhancement $\rightarrow$ Assistant provides modular insertion code with explicit integration comments and variable additions.
- **Target Volume**: 500 – 800 datasets.

---

## 5. Dataset Type 4: Theory-to-Code Concept Bridges

### 5.1 Capability It Unlocks
Teaches the model to bridge the gap between academic control theory (Laplace/Z-domain transfer functions, orthogonal polynomials, state observers) and real-time execution in deterministic scan cycles.

### 5.2 Target Volume & Specifications
- **Target Volume**: 600 – 800 tasks.
- **Structure**: Detailed mathematical derivation ($\ge 300$ words) $\rightarrow$ Numerical discretization (Tustin / Euler) $\rightarrow$ Full production-grade Structured Text implementation.
- **Target Systems**: Automatic Flatness Control (Legendre decomposition), Smith Predictor dead-time compensation, Kalman state observers, bumpless auto-tune algorithms.

---

## 6. Dataset Type 5: Domain Text Corpora for Language Modeling

### 6.1 Capability It Unlocks
Improves the model's fundamental comprehension of industrial engineering terminology, safety standards, and operating principles during **Stage A Continual Pre-Training (CPT)** before code fine-tuning.

### 6.2 Corpus Source Sizing & Availability

| Corpus Source | Content Type | Target Volume (Tokens) | Availability & Licensing |
|---|---|:---:|---|
| **IEC 61131-3 & IEC 61508 Summaries** | Language specifications & safety guidelines | ~250,000 | Public summaries / Open Standards |
| **ISA-18.2 Alarm Management Guides** | Alarm rationalization & deadband standards | ~350,000 | ISA membership / Public guidance |
| **Machine Builder OEM Manuals** | Commissioning & operational procedures (Siemens, Beckhoff) | ~2,000,000 | Public technical documentation |
| **Academic Industrial Automation Papers** | State-space, MPC, and factory automation papers (arXiv) | ~3,500,000 | Open Access (arXiv e-prints) |
| **Open-Source Industrial Code Prose** | Technical markdown & documentation (`tc-open`, `OSCAT`) | ~500,000 | MIT / LGPL open licenses |
| **Industrial Control Encyclopedic Data** | SCADA, DCS, PLC, sensor hardware wiki entries | ~1,000,000 | Creative Commons (CC-BY-SA) |
| **Total Pre-Training Domain Text** | **High-Density Industrial Engineering Text** | **~7,600,000 Tokens** | **Fully Obtainable & Public** |

### 6.3 Pre-Processing Pipeline
1. **Boilerplate Stripping**: Regex elimination of HTML headers, navigational sidebars, and copyright footers.
2. **Quality Filtering**: Minimum 150 words per document, English language classification, removal of duplicate pages.
3. **MinHash LSH Deduplication**: Clustering at $\theta = 0.85$ Jaccard similarity.
4. **Context Chunking**: Partitioning into 2,048-token to 4,096-token segments for Stage A packing.

---

## 7. Dataset Type 6: Safety Instrumented Function (SIF) Scenarios

### 7.1 Capability It Unlocks
Guarantees that the model understands functional safety engineering under **IEC 61511** (Process Industry Safety Systems) and **IEC 62061** (Machinery Safety). The model learns to generate certified de-energize-to-trip logic, NAMUR NE43 analog current diagnostic monitoring, PFDavg verification, and proof test sequencing.

### 7.2 Target Volume & Specifications
- **Target Volume**: 200 – 300 SIF scenarios.
- **Key Safety Mandates**:
  - Dual-channel 1oo2D or 2oo3 sensor architectures.
  - NAMUR NE43 loop supervision ($I < 3.6\text{ mA}$ wire break, $I > 21.0\text{ mA}$ short circuit).
  - De-energize-to-trip output design (`b_SafeOutput_DO := FALSE;`).
  - Supervised physical manual reset requiring process return to safe operating envelope.

---

## 8. Summary: Complete Dataset Production Matrix

| Type | Dataset Archetype | Primary Role in Fine-Tuning | Target Volume | Generation Pipeline Tool | Schema Tag |
|:---:|---|---|:---:|---|---|
| **Core** | Verified Code Blocks | Base Structured Text Code Emission (Stage B) | ~503 datasets | Swarm Core (`triage_corpus.py`) | `verified_code` |
| **Type 1**| Technical Dialogue Q&A | Conversational Engineering & Support Bot (Stage C) | 1,500–2,000 | `scripts/generate_type1_dialogue.py` | `type_1_dialogue_qa` |
| **Type 2**| 3-Turn Debug Chains | Interactive Code Troubleshooting & Repair (Stage C) | 800–1,000 | `scripts/generate_type2_debug.py` | `type_2_debug_chain` |
| **Type 3**| Incremental Modification | Brownfield Subsystem Extension (Stage C) | 500–800 | `scripts/generate_type3_incremental.py` | `type_3_incremental_modification` |
| **Type 4**| Concept-to-Code Bridges | Mathematical Theory to Scan-Time Code (Stage C) | 600–800 | `scripts/generate_type4_concept_code.py` | `type_4_concept_to_code` |
| **Type 5**| Domain Text Corpora | Continual Domain Pre-Training Saturation (Stage A) | 5–10M tokens | Standards & OEM Manual Scraper | `raw_domain_text` |
| **Type 6**| SIF Safety Scenarios | Certified SIL-2/SIL-3 Functional Safety (Stage C) | 200–300 | `scripts/generate_type6_safety.py` | `type_6_safety_sif` |

---

*This specification provides the foundational dataset blueprint to transform the Lumina fine-tuning corpus into a world-class, multi-modal industrial automation training asset.*
