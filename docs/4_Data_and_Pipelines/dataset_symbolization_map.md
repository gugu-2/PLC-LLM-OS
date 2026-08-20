# Industrial Dataset Symbolization Map

To ensure the LLM understands exactly *what* it is coding, we must "symbolize" (classify) the dataset. Every generated pair maps to specific industrial verticals, machinery types, and engineering departments.

## 1. Dataset Origin (How we got it)
* **Tier 1 (Natural):** Mined autonomously from GitHub and open-source enterprise repositories via the `fast_tier_extractor.py` daemon.
* **Tier 2 (Synthetic Base):** Generated programmatically via Gemini API (`synthetic_50k_dataset.jsonl` - currently isolated due to low reasoning quality).
* **Tier 3 (Evol-Instruct):** Generated autonomously via the Antigravity Agent Swarm, utilizing deep reasoning, adversarial hardware-in-the-loop (HIL) logic, and IEC 62443 cybersecurity interlocks.

---

## 2. Industry & Machinery Taxonomy (The Swarm Batches)

### Batch 1: Heavy Duty Motor Control
* **Industry:** General Manufacturing, Mining, Oil & Gas.
* **Machinery:** 3-Phase Induction Motors, Variable Speed Drives (VSD), Star-Delta Starters.
* **Department:** Electrical Engineering, Low-Voltage (LV) MCC Control.
* **Status:** `[COMPLETED]`

### Batch 2: Discrete Manufacturing & Continuous Process
* **Industry:** Logistics, Pharmaceuticals, Food & Beverage, Automotive.
* **Machinery:** High-Speed Sortation Conveyors, Incline Conveyors, ISA-88 Liquid Mixers, Granulation Batch Processors, Servo Cam Followers.
* **Department:** Process Engineering, Motion Control, Packaging.
* **Status:** `[COMPLETED]`

### Batch 3: HVAC, Utilities, & Renewables *(Currently Deploying)*
* **Industry:** Building Automation (BMS), Utilities, Renewable Energy.
* **Machinery:** Chiller Plants, Air Handling Units (AHU), Industrial Boilers, Reverse Osmosis (RO) Water Treatment, Wind Turbine Yaw Control.
* **Department:** Facilities Management, Process Utilities, Environmental Engineering.
* **Status:** `[IN PROGRESS]`

### Batch 4: Advanced Robotics & CNC
* **Industry:** Automotive Assembly, Aerospace, Semiconductor.
* **Machinery:** 6-Axis Articulated Arms, CNC Spindle Control, Automated Guided Vehicles (AGV), Gantry Systems.
* **Department:** Robotics Engineering, Advanced Manufacturing.
* **Status:** `[QUEUED]`

---

## 3. The Autonomous Generation & Review Loop
Per your command, the Swarm will now run continuously without pausing for human permission. 
1. The Swarm Orchestrator deploys a batch of 5 autonomous subagents.
2. The Orchestrator waits for all 5 to complete.
3. The Orchestrator aggregates the data and performs a **Self-Review** of the generated code to ensure high-grade quality.
4. The Orchestrator immediately queues and deploys the next batch.
