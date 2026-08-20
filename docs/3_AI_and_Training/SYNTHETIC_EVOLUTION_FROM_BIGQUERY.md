# Synthetic Data Evolution: Upgrading 50,000 Human Records via Local LLM

This document details the architectural strategy of using a massive, lower-quality human dataset (like 50,000 BigQuery GitHub records) as "seeds" to force a local LLM to generate a vastly superior, enterprise-grade synthetic dataset. 

This technique is known in AI research as **Evol-Instruct (Evolutionary Instruction Tuning)** combined with **Data Distillation**.

---

## 1. The Core Concept: Why do this?

When you scrape 50,000 files from GitHub, you get highly authentic syntax, but the engineering quality is often poor. You will find:
*   Uncommented code.
*   Poorly named variables (e.g., VAR1, 	emp2).
*   Missing safety interlocks and error handling.
*   Spaghetti logic written by junior engineers or students.

Your local 7B-8B parameter LLM (like Qwen2.5-Coder) might struggle to hallucinate a brilliant factory architecture from a blank screen. However, LLMs are **exceptional at refactoring**. If you hand the LLM a messy, poorly-written human script, it has the localized intelligence to clean it, optimize it, and upgrade it to enterprise standards.

**The Goal:** We feed 50,000 "dirty" human records into the local LLM, and it spits out 50,000 "Golden" records. The AI effectively acts as an ultra-strict Senior Automation Engineer rewriting junior code.

---

## 2. The Evolution Pipeline Architecture

To achieve this on your RTX 5050, we will modify the evol_orchestrator.py script to perform a specific loop:

### Step 1: The Seed Injection (RAG)
Instead of asking the AI to invent something from scratch, the Python script randomly selects 1 to 3 records from your 50,000 BigQuery dataset.

### Step 2: The Mutation Prompts
The orchestrator wraps the human code in a specific "Mutation Prompt". We randomly cycle through different mutations to create diverse data:

*   **Mutation A (Code Polish):** *"Here is a messy IEC 61131-3 function block written by a human. Refactor this code to industrial standards. Add comprehensive comments, rename variables to follow Hungarian notation, and ensure all edge cases are handled. Output the perfected code."*
*   **Mutation B (Complexity Deepening):** *"Here is a basic human-written motor control loop. Expand this code. Add a PID temperature monitoring system to it, and include safety shutdown logic if the temperature exceeds 80 degrees."*
*   **Mutation C (Translation/Standardization):** *"Here is some legacy Siemens SCL code. Rewrite it into pure, hardware-agnostic IEC 61131-3 Structured Text that can run on any PLC."*

### Step 3: The GPU Generation (Local Inference)
Your RTX 5050 processes the prompt and the messy code, and generates the new, upgraded code block.

### Step 4: The Mathematical Verification Gauntlet
The newly generated code is instantly piped into linter.py. 
*   If the LLM broke the syntax while trying to upgrade it, the linter fails, and the LLM is told to fix its mistake (The Reflection Loop).
*   If it passes, the new code is saved into the Golden Vault.

---

## 3. The Hardware Mathematics (RTX 5050)

Processing 50,000 records through a local 7B parameter model requires significant compute time. 

*   **Average Generation Time:** ~15 to 20 seconds per record (reading the prompt + generating the new code).
*   **Generations per Minute:** ~3 records.
*   **Generations per Hour:** ~180 records.
*   **Generations per Day (24/7):** ~4,300 records.

**Total Time to Evolve 50,000 Records:** 
It will take your laptop approximately **11 to 12 days running 24/7** to upgrade the entire BigQuery database into a pristine synthetic dataset.

Because it runs locally, this costs you **.00** in API fees. It only costs the electricity to run the laptop.

---

## 4. Why This Creates the Ultimate Dataset

By doing this, you achieve the "Holy Grail" of AI training data:
1.  **Volume:** You have 50,000 unique industrial scenarios (impossible to write by hand).
2.  **Authenticity:** The core logic concepts were grounded in real human engineering problems found on GitHub, avoiding AI "hallucination loops."
3.  **Perfection:** Every single record has been rewritten by a genius-level coding model to feature perfect commenting, perfect variable naming, and flawless syntax.

When you eventually fine-tune a model on this *distilled* dataset, the resulting AI will strictly output clean, enterprise-grade code, because that is the only formatting it has ever seen.
