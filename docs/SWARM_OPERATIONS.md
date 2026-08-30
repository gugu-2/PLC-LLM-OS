# Swarm Operations & Orchestration

The Swarm generation loop is the core engine of the PLC-LLM-OS project. It allows the system to autonomously farm highly specialized IEC 61131-3 logic without constant human supervision.

---

## 1. The Swarm Pulse Mechanism

The orchestration is handled through Antigravity's background task management. A specific cron task (e.g., `task-8838`) is scheduled to run indefinitely:

**Cron Schedule:** `*/6 * * * *` (Every 6 minutes)

**Wakeup Prompt:** 
> "CRITICAL: Swarm Pulse. Invoke 3 new SyntheticDataEvolverV3 subagents with the 'pro' model tier. Assign them completely new and complex industrial domains. Instruct them to generate IEC 61131-3 ST code (>= 1500 chars) and save the JSON payload to isolated files in data/swarm_raw/ using python with uuid4 filenames to guarantee no collisions. Do NOT combine files."

### Why 6 Minutes?
Spawning 3 `pro`-tier agents simultaneously consumes a massive amount of token bandwidth. A 6-minute cooldown between pulses prevents API exhaustion (`429` errors) while allowing sufficient time for the agents to run Python file operations.

## 2. Prompt Engineering for the Evolver Agents

To guarantee high-quality synthetic data, the subagents must be strictly prompted. A standard invocation configuration looks like this:

```json
{
  "Model": "pro",
  "TypeName": "SyntheticDataEvolverV3",
  "Role": "Specific Domain Architect (e.g. Petrochemical Architect)",
  "Prompt": "..."
}
```

**Critical Prompt Elements:**
1. **Domain Specificity:** The domain cannot be generic (e.g., "Manufacturing"). It must be hyper-niche (e.g., "Fischer-Tropsch reactor catalyst cooling zones in a Power-to-Liquid plant").
2. **Length constraint:** Force the agent to write robust logic (`>= 1500 chars`).
3. **No conversational fluff:** Explicitly state: `DO NOT APOLOGIZE. DO NOT EXPLAIN.` Output must be strictly bounded by ` ```iec-st ` code fences.
4. **Isolated File I/O:** Provide the exact Python snippet to the agent to write its response via `uuid4()`.

## 3. Stopping and Restarting

The loop is designed to be infinite. It will only stop if:
1. The user explicitly requests to stop it (e.g., "Stop the synthetic data loop").
2. The IDE server crashes or is restarted.

**If the server restarts:** All background tasks, including the cron job, are killed. The user or the orchestrating agent must manually revive the loop by scheduling a new cron job with the identical wakeup prompt.

## 4. Recovering from Safety Rejections

Occasionally, a generated domain will trigger the LLM's safety filters (e.g., generating control code for a nuclear reactor, biological weapons facility, or Cobalt-60 irradiator). 

When a subagent reports a refusal:
1. **Acknowledge:** The orchestrator should acknowledge the dropped payload.
2. **Pivot:** In the next pulse, the orchestrator must dynamically pivot the domains to safer industrial sectors (Renewables, Food & Bev, Packaging, Textiles, Semiconductor) to maintain high data yield.
