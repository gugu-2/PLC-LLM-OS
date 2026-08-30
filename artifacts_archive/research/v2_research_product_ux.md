# Designing the Glass Box: Product UX and Interaction Design for Autonomous PLC Code Generation Systems

## Abstract

The advent of large language models (LLMs) and advanced code generation technologies has paved the way for autonomous generation of Programmable Logic Controller (PLC) code in industrial automation. While previous research has successfully demonstrated the technical feasibility and backend infrastructure of such systems, a critical gap remains: the user experience (UX) and product design necessary for widespread adoption. This paper introduces a comprehensive UX framework for the **Autonomous PLC Code Generator & Management System**, focusing on the pivotal "Trust Interface Problem." By defining distinct user personas, structured approval workflows, and intuitive natural language interfaces, we propose a "Glass Box" interaction model that fosters trust, enhances human-AI collaboration, and delivers measurable return on investment (ROI). Furthermore, we present a unified brand identity, *Lumina*, to encapsulate the product's vision.

---

## 1. Introduction: From Infrastructure to Interface

Industrial control systems govern machinery responsible for manufacturing, energy distribution, and critical infrastructure. The financial and safety stakes in these environments are astronomically high. Consequently, the primary barrier to adopting autonomous AI for PLC programming is not technical capability, but human trust. A system that can write code for a million-dollar robotic assembly line is useless if the plant manager refuses to turn it on.

This research shifts the focus from infrastructure to the end-user, exploring the UX design required to transform a theoretical capability into an indispensable industrial product.

---

## 2. Product Naming Strategy and Brand Identity

To anchor the UX design, we first establish a cohesive brand identity that conveys transparency, intelligence, and reliability.

### 2.1 Brand Name: **Lumina**
*Meaning:* Derived from "illumination," representing the shedding of light on previously opaque, black-box AI processes. Lumina signifies clarity, foresight, and enlightenment in industrial automation.

### 2.2 Brand Identity Concept
- **Color Palette:** 
  - *Primary:* Deep Industrial Slate (Trust, Stability, Structure).
  - *Secondary:* Electric Azure (Intelligence, Precision, Modernity).
  - *Accents:* Safety Amber & Critical Crimson (Alerts, Human-in-the-loop actions).
- **Typography:** Clean, sans-serif fonts (e.g., Inter or Roboto Mono for technical data) that prioritize legibility on harsh factory floors and high-glare environments.
- **Voice & Tone:** Authoritative, precise, and reassuring. The system never guesses; it calculates, simulates, and recommends with explicit confidence metrics.

---

## 3. The Trust Interface Problem: The "Glass Box" Design

The core UX challenge is mitigating the inherent apprehension associated with AI control. The "Glass Box" design paradigm mandates that every autonomous action is fully transparent and explainable.

### 3.1 Explainable Actions
Instead of simply executing a change, Lumina provides a causal narrative.
*Example UI Element:*
> **Action Proposed:** Reduce Servo T-04 deceleration timer from 500ms to 380ms.
> **Reasoning:** Predictive maintenance models detect a 12% vibration degradation trend over the last 30 days. The proposed timer adjustment reduces mechanical stress, extending servo lifespan by an estimated 4.2 months, without impacting the 60 PPM line throughput.
> **Confidence Score:** 98.4% (Based on 14 similar historical adjustments).

### 3.2 Visual Simulation and Diff Views
Before any code is deployed, the system presents a visual simulation of the mechanical impact alongside a semantic diff of the PLC code (e.g., Ladder Logic or Structured Text). The user sees the code change *and* a 3D or digital-twin representation of the physical outcome.

---

## 4. User Personas and Tailored Interfaces

An autonomous system serves multiple stakeholders, each requiring a distinct lens into the system's operations.

### 4.1 The Plant Manager (Non-Technical)
**Goal:** Maximize uptime, ensure safety, and manage overall plant health.
**Interface:** The "Factory Weather Forecast."
- **Visuals:** High-level dashboards with clear status indicators (Green/Yellow/Red).
- **Features:** 
  - **Uptime Prediction:** "Line 3 has a 92% probability of running without interruption for the next 72 hours."
  - **Action Queue:** A summarized list of AI recommendations awaiting engineering approval, highlighting the potential impact on throughput if delayed.

### 4.2 The Controls Engineer (The Co-Pilot)
**Goal:** Design complex logic, troubleshoot anomalies, and oversee AI operations.
**Interface:** The "Superpowered IDE."
- **Visuals:** Split-pane views combining traditional IEC 61131-3 editors with AI-assisted chat and simulation environments.
- **Features:** 
  - **Boilerplate Generation:** The engineer defines high-level state machines; Lumina generates the underlying I/O mapping and fault-handling logic.
  - **Semantic Search:** "Show me all interlocks affecting the Line 2 safety gate."
  - **Impact Analysis:** Real-time visualization of how a manual code change affects downstream processes.

### 4.3 The C-Suite / Owner
**Goal:** Maximize ROI, reduce operational costs, and justify capital expenditures.
**Interface:** The "Financial Command Center."
- **Visuals:** Executive summaries, trend graphs, and financial metrics.
- **Features:**
  - **Real-time ROI Tracking:** "Lumina optimizations have saved $42,000 in energy costs and prevented 14 hours of unplanned downtime this quarter."
  - **Capital Expenditure Forecasting:** Predictions on when physical hardware will need replacement based on AI-monitored wear and tear.

---

## 5. The Structured Approval Workflow

To ensure safety and compliance, Lumina employs a tiered, risk-based approval workflow.

| Risk Level | Type of Change | Approval Requirement | Example |
| :--- | :--- | :--- | :--- |
| **Tier 1 (Low)** | Parameter optimization, minor timer tuning within safety limits. | Auto-approved (Notified in digest). | Adjusting PID loop tuning by < 5%. |
| **Tier 2 (Medium)** | Logic sequence modification, new standard I/O mapping. | Single Controls Engineer signature. | Adding a new proximity sensor to an existing sequence. |
| **Tier 3 (High)** | Safety interlock changes, high-speed motion profile alterations. | Dual signatures (Lead Engineer + Plant Manager) & Mandatory 24h virtual simulation. | Bypassing a redundant safety gate logic block. |

*UI Implementation:* Tier 3 changes trigger an escalation notification to mobile devices, requiring biometric authentication (e.g., FaceID) to sign off.

---

## 6. Natural Language Interface (NLI)

The NLI is the primary interaction paradigm for reactive maintenance and troubleshooting.

### 6.1 Conversational Workflow
1. **User Input:** Engineer speaks into a tablet: *"The bottle labeler on Line 3 is 5mm off center. Fix it."*
2. **Intent Parsing:** Lumina identifies the machine (Line 3 Labeler), the issue (5mm offset), and the goal (re-center).
3. **Investigation & Proposal:** Lumina analyzes the current encoder values and servo logic.
4. **System Response:** *"I found the issue. The registration mark sensor has drifted. I have generated a corrective offset of -500 encoder counts to the servo homing routine. Do you want to simulate this change?"*
5. **Simulation & Approval:** The engineer views the digital twin simulation. The code diff is shown. The engineer clicks "Approve & Deploy."

---

## 7. The Onboarding Experience: Commissioning Wizard

Deploying an AI system into an existing, often chaotic, factory environment is daunting. The onboarding experience must be frictionless.

### 7.1 Step-by-Step Commissioning
1. **Network Discovery:** Lumina scans the industrial network (Profinet, EtherNet/IP) and auto-identifies connected PLCs, drives, and HMIs.
2. **Digital Twin Mapping:** The wizard prompts the user to upload existing CAD files or P&ID diagrams. Lumina correlates the network nodes to physical assets.
3. **Baseline Monitoring:** Before proposing any changes, Lumina enters a mandatory "Listening Mode" (e.g., 14 days) to learn normal operating baselines and build the predictive model.
4. **First Value Delivery:** The system identifies a low-risk, high-value optimization (e.g., a motor running unnecessarily during idle periods) to build initial user trust.

---

## 8. The Mobile Experience

Industrial professionals are rarely tethered to desks. The UX must be mobile-first for operational tasks.

### 8.1 Mobile-First Capabilities
- **Push Alerts with Context:** Not just "Fault 404," but "Fault 404 on Line 2 Infeed. AI suggests clearing sensor cache and resetting the drive. Tap to execute."
- **Approval on the Go:** Managers can review Tier 2 changes with a quick summary of the "Why" and "Impact," swiping right to approve via the mobile app.
- **Augmented Reality (AR) Overlay:** Using the tablet camera, an engineer can look at a physical cabinet, and Lumina overlays the real-time PLC variable states on the physical I/O cards.

---

## 9. The Affordability of UX: Thin Client Architecture

Previous research proposed heavy edge computing, which is cost-prohibitive. Lumina adopts a "Thin Client" architecture.

### 9.1 Architecture Model
- **Centralized Brain:** All LLM inference, heavy simulation, and data aggregation occur on a centralized secure server (on-premise cluster or isolated cloud VPC).
- **Edge Data Collectors:** Lightweight, inexpensive DIN-rail mounted gateways simply stream OPC UA data to the brain.
- **Thin Client Interfaces:** The entire UX (Dashboards, IDE, Mobile App) is delivered via responsive web technologies (e.g., React/WebSockets).
- **Hardware Agnostic:** A Plant Manager can access the full power of Lumina using a standard $200 ruggedized Android tablet and a web browser. No expensive, dedicated HMIs are required for the AI interface.

---

## 10. Conclusion

The success of an Autonomous PLC Code Generator hinges not on its ability to write code, but on its ability to communicate its intent, respect industrial hierarchies, and prove its reliability. By implementing the "Glass Box" interface, structured workflows, and role-specific views within a thin-client architecture, Lumina bridges the gap between advanced artificial intelligence and the pragmatic realities of the factory floor. This UX framework transforms the AI from a perceived threat into an indispensable, trusted co-pilot.
