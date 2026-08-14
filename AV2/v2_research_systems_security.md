# Securing Autonomous PLC Code Generation: A Defense-in-Depth Architecture for Next-Generation ICS

## Abstract
The integration of Large Language Models (LLMs) into Industrial Control Systems (ICS) for autonomous Programmable Logic Controller (PLC) code generation presents unprecedented operational efficiencies and equally unprecedented cyber-physical risks. Previous architectures relied on flawed assumptions, such as utilizing memory-constrained secure enclaves (e.g., Intel SGX) for large models, assuming universal "atomic" code handoffs, and granting direct PLC write access to Level 3 AI agents. This paper proposes a robust, structurally sound security architecture designed from first principles. It introduces AMD SEV-SNP Confidential VMs for secure LLM execution, a hardware-enforced deployment proxy, a comprehensive model supply chain security framework, and strict constraints on autonomous actions. Furthermore, we outline an incident response plan specifically tailored to AI-induced operational failures, modeled against the MITRE ATT&CK for ICS framework.

---

## 1. Introduction
Autonomous generation and deployment of PLC code by AI agents represents a paradigm shift in manufacturing and critical infrastructure. However, the cyber-physical nature of ICS means that logical errors—whether maliciously injected or accidentally generated—can result in catastrophic physical damage. Early theoretical models for securing these systems suffered from critical technical misunderstandings. This research establishes a realistic, defense-in-depth architecture that assumes compromise at the AI layer and builds hardware and protocol-level safeguards to contain it.

---

## 2. Secure Execution: Moving Beyond Enclave Limitations
A fundamental flaw in early AI-ICS security designs was the proposition of running multi-billion parameter LLMs (requiring 4GB to 80GB of RAM) inside technologies like Intel SGX, which historically offered a severely limited Enclave Page Cache (EPC).

### 2.1 The AMD SEV-SNP Confidential VM Solution
Instead of process-level enclaves, the autonomous LLM agent must be hosted within a **Confidential Virtual Machine (CVM)** utilizing technologies such as **AMD SEV-SNP (Secure Encrypted Virtualization-Secure Nested Paging)** or Intel TDX. 
- **Memory Capacity:** CVMs support hundreds of gigabytes of encrypted RAM, accommodating state-of-the-art LLMs with large context windows.
- **Hardware-Rooted Trust:** SEV-SNP encrypts the entire VM's memory and state, isolating it even from a compromised hypervisor.
- **Attestation:** Before the ICS network accepts any generated code, the CVM provides cryptographic attestation proving that the expected, untampered model and inference engine are running.

---

## 3. Network Architecture: Hardware-Enforced Proxies
Placing an autonomous AI agent at Level 3 of the Purdue Model with direct write access to Level 1 PLCs creates the ultimate pivot point for an advanced persistent threat (APT). 

### 3.1 The One-Way Downward Pipeline
The AI must have **zero direct network routes** to the PLC layer. The architecture relies on a **Hardware-Enforced Proxy** equipped with a Formal Policy Engine.
1. **Telemetry Ingress:** The AI receives plant telemetry (Level 1 to Level 3) via a physical **Unidirectional Data Diode**, ensuring attackers cannot use the telemetry channel to traverse downward.
2. **Code Deployment Proxy:** When the AI generates new logic, it submits it to a heavily hardened, air-gapped-equivalent proxy server. 
3. **Formal Policy Engine:** The proxy does not merely pass the code; it analyzes it using formal verification (e.g., bounded model checking). The engine verifies that the new logic does not violate predefined safety invariants (e.g., "Valve A and Valve B must never be open simultaneously"). Only if the formal proof passes is the code allowed to proceed to the Level 1 engineering workstation for deployment.

---

## 4. Realistic Mechanisms of Code Deployment
The concept of a universal "atomic handoff" (where new code is loaded into a standby bank and switched instantly) is a dangerous oversimplification of PLC architectures.

### 4.1 Vendor-Specific Deployment Realities
- **Siemens (TIA Portal / S7-1500):** Deployment often requires compiling a block and downloading it in RUN mode. Care must be taken with Data Blocks (DBs). The AI deployment proxy must explicitly manage Reinitialization of DBs to prevent state loss during the transition.
- **Rockwell Automation (ControlLogix):** Uses a mechanism of "Online Edits." Rungs are inserted, tested, and assembled. The proxy must manage the transition via Controller Tags and handle the `Test` phase before `Assemble`.
- **Constraint:** The AI proxy is strictly forbidden from initiating a full "Download in STOP" mode without human multi-factor authentication (MFA), as this halts the process.

---

## 5. Model Supply Chain and Integrity Framework
The LLM itself is a supply chain vector. A maliciously fine-tuned model (Data Poisoning) might generate logic that operates normally 99% of the time but subtly alters a PID loop tuning parameter during a specific, rare operational state.

### 5.1 Securing the Provenance
Relying on a "Sheep Dip Kiosk" for USB scanning is insufficient, as modern threats evade static AV.
- **Cryptographic Attestation and Reproducible Builds:** The model weights must be signed. The inference container must be built via a reproducible build pipeline. The AMD SEV-SNP attestation report verifies the hash of the running container against the signed hash of the authorized model.
- **Behavioral Red-Teaming (Pre-Deployment):** Before a new model version is authorized for the ICS environment, it must pass a rigorous, automated red-team simulation where it is subjected to edge-case telemetry to ensure it does not hallucinate dangerous logic.

---

## 6. The Principle of Minimum Viable Autonomous Action
To limit the blast radius of an AI failure, the system must enforce strict boundaries on what the AI is permitted to modify.

### 6.1 Safety Functions are Air-Gapped from AI
The AI is structurally prevented from interacting with **Safety Instrumented Systems (SIS)** or Safety PLCs (e.g., Siemens fail-safe CPUs, Rockwell GuardLogix). 
- Safety Logic (SIL 2/3 requirements) relies on fixed, deterministic, certified code. The formal policy engine outright rejects any AI attempt to write to memory addresses or tags designated for safety functions.
- The AI may optimize process variables (e.g., throughput, energy usage) but can never override safety interlocks.

---

## 7. AI Behavioral Monitoring and Anomaly Detection
Beyond monitoring the physical process, the system must monitor the AI's *cognitive* output.

### 7.1 Meta-Monitoring the AI
An independent, deterministic heuristic engine monitors the AI agent's actions:
- **Frequency Analysis:** If the AI attempts to deploy code changes 50 times a minute when the baseline is twice a day, the connection is severed.
- **Semantic Drift Detection:** If the AI starts generating logic that interacts with hardware modules unrelated to its assigned optimization task (e.g., an HVAC AI suddenly querying the physical access control PLCs), an alarm is triggered, and the AI's write privileges are revoked.

---

## 8. Threat Modeling (MITRE ATT&CK for ICS)
This architecture defends against specific ICS attack vectors:

| Tactic | Technique (ATT&CK for ICS) | Mitigation |
| :--- | :--- | :--- |
| **Execution** | Execution through API (T0871) | Hardware proxy rejects unauthorized API calls; Formal Policy Engine restricts executable logic. |
| **Persistence** | Modify Control Logic (T0833) | Cryptographic attestation of the LLM prevents poisoned models from injecting backdoors. |
| **Evasion** | Indicator Removal on Host (T0872) | AI runs in a CVM; logs are written to an immutable append-only ledger outside the VM. |
| **Impact** | Manipulation of Control (T0831) | Minimum Viable Autonomous Action prohibits modification of safety PLCs. |

---

## 9. Incident Response and Recovery Plan
When the AI deploys faulty code that halts a production line, the response must be immediate and structured.

### 9.1 Step-by-Step AI Incident Recovery
1. **Containment (Automated):** The plant's Level 1 anomalies trip a hardware interlock, safely halting the physical process. The AI proxy automatically severs the connection to the CVM upon detecting the Level 1 fault.
2. **Eradication (Manual):** The Incident Response (IR) team physically disconnects the AI proxy. The AI CVM is suspended, and its RAM state is dumped for forensics.
3. **Recovery (Deterministic Rollback):** 
    - Operators utilize the Level 1 Engineering Workstation to initiate a "Golden Master" rollback. 
    - The PLC is flashed with the last known-good configuration from a read-only hardware vault.
4. **Post-Incident Analysis:** IR analysts review the AI's prompts, context window, and generated code in the immutable log to determine if the failure was a hallucination, a data poisoning trigger, or a logic flaw in the Formal Policy Engine.

---

## 10. Conclusion
Deploying autonomous AI for PLC code generation introduces extreme risks that cannot be mitigated by traditional IT security paradigms. By discarding flawed concepts like LLM enclaves and atomic handoffs, and replacing them with Confidential VMs, hardware-enforced proxies, formal policy engines, and strict boundaries on autonomous action, organizations can harness the efficiency of AI without compromising the safety and integrity of critical infrastructure.
