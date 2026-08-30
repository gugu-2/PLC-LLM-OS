# Zero Trust Security & Data Diode Architecture

## 1. The Operational Technology (OT) Threat Model
Connecting an AI to physical industrial machinery represents an extreme security risk (Stuxnet, ransomware, hallucinated logic causing physical destruction). The Lumina OS is designed around a **Zero Trust** architecture, assuming the AI is inherently compromised or prone to hallucinations.

## 2. Unidirectional Data Diode (Layer 1 Air-Gap)
Physical data diodes are hardware devices that only allow data to flow in one direction (usually via a severed TX/RX fiber optic cable). Lumina simulates this in software via `lumina_diode.py`.
- **`UnidirectionalDiodeTX` (The Plant):** Broadcasts high-frequency telemetry via UDP to a specific port. It does not listen for TCP handshakes.
- **`UnidirectionalDiodeRX` (The Server):** Listens to the UDP stream.
- **Why?** By strictly using connectionless UDP streaming for telemetry, it is impossible for a compromised server to send malicious data *back down* the telemetry pipe. The only way data flows back to the PLC is through the highly restrictive PAL verification gauntlet.

## 3. Cognitive Meta-Monitor & Burst Limiting
The `lumina_security.py` module acts as a strict firewall between the AI and the PLC.
- **Tag Prefix Filtering:** The AI is strictly limited to writing to specific memory tags. For example, if it attempts to write to a tag outside the allowed `["Cmd_", "SP_"]` prefixes (e.g., trying to overwrite a raw sensor input `Sens_`), the proxy blocks the payload immediately.
- **Burst Rate Limiting:** The `AdaptiveBurstRateLimiter` prevents the AI (or a malicious actor) from flooding the PLC with write commands, preventing Denial of Service (DoS) attacks on the PLC's limited CPU cycle time.

## 4. The Golden Master Vault
Before any new AI-generated code is deployed, a cryptographic SHA-256 hash of the known-good, human-verified PLC logic is stored in the `GoldenMasterVault`. 
If the AI deploys logic that violates safety protocols or causes an anomaly, the Cognitive Meta-Monitor can instantly trigger a rollback, rewriting the original Golden Master code back to the PLC to restore safe operational status.
