# Lumina Frontend: UI/UX & AR Diagnostics Guide

## 1. Architectural Philosophy
The Lumina frontend (`index.html` + standard vanilla JS) is built on a **Zero-Build, Edge-Native** philosophy. 
Because Lumina operates in harsh industrial environments (often air-gapped without internet access), the frontend is entirely self-contained. There is no Webpack, no React, and no complex node-modules required to serve the dashboard. It is a lightweight, ultra-fast UI served directly by FastAPI.

## 2. The 9-Tab Dashboard Architecture
The interface is decoupled into 9 discrete operational views, allowing engineers to monitor the entire plant stack from a single pane of glass:
1. **System Overview:** Global status, active PLCs, and high-level health.
2. **Telemetry Stream:** Raw, real-time JSON polling from the `UnidirectionalDiodeRX`.
3. **Cybersecurity:** Activity logs from the Golden Master Vault and tag proxy blocks.
4. **Knowledge Base (RAG):** AI chat interface to query OEM manuals.
5. **Generative Code:** The workspace to prompt the Qwen2.5-Coder model to generate PLC logic.
6. **Hardware (PAL):** Configuration for physical PLC connections (Snap7, PyComm3, PyModbus).
7. **Simulation:** The Kinematic Digital Twin visualizer (Oscilloscope / HTML5 Canvas).
8. **Formal Verification:** Readout from the Microsoft Z3 SMT prover.
9. **AR Diagnostics:** A mobile-first Augmented Reality overlay for field technicians.

## 3. AR Diagnostics & Mobile UX
The **AR Diagnostics (Tab 9)** feature represents a paradigm shift in how field technicians interact with physical machinery.

### Implementation Details:
- **Device Orientation API:** Utilizes standard HTML5 APIs to map the technician's mobile device gyroscope to a digital viewport.
- **Bounding Box Telemetry:** Real-time UDP telemetry is mapped to absolute `(x, y)` HTML `<div>` coordinates. When the technician points their iPad/Tablet at the physical "Rotary Capper", the live PLC tags (e.g., `Torque_Nm`) hover perfectly over the machine on their screen.
- **Responsive Fluidity:** CSS Grid and Flexbox ensure that the 9-tab interface collapses into a thumb-friendly bottom-sheet on mobile devices, ensuring field workers can navigate the complex AI tools while wearing PPE gloves.
