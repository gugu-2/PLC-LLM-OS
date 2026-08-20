# BigQuery Data Analysis: Yield, Sources, and Authenticity

This document outlines the expected results if we activate billing on Google Cloud and run the BigQuery extraction across the GitHub mirror.

## 1. How Much Data Can We Get?
The Google BigQuery public dataset (igquery-public-data.github_repos) contains a snapshot of **every public repository on GitHub** (over 3 million repositories).

Our SQL query is designed to pull up to **75,000 files** matching PLC extensions (.st, .scl, .tcpou, etc.).

**Expected Pipeline Yield:**
*   **Raw files pulled:** ~50,000 - 75,000
*   **Failed linter / too short:** ~40% drop-off
*   **Duplicates removed:** ~10-20% drop-off
*   **Final Verified Records:** **~20,000 to ~35,000 unique ChatML pairs.**

This would expand our current dataset (5,928) by about 500% in a single run.

## 2. What Are the Data Sources?
The data comes from a massive, unfiltered cross-section of the global automation community on GitHub.

Unlike our manual cloner (which targets 62 hand-picked "best-of" repositories), BigQuery searches **everything**.
*   **Vendors:** Siemens (TIA Portal .scl), Beckhoff (TwinCAT .tcpou), Codesys (.st).
*   **Demographics:** German automotive engineers, American integrators, university students, hobbyists.
*   **Project Types:** Everything from massive open-source frameworks (like TcOpen) to random one-off university assignments.

## 3. How Authentic is the Data?
**Structural Authenticity: 100%**
Because every file is passed through our Z3/AST Linter, we mathematically guarantee that the data contains zero syntax errors, perfectly closed FUNCTION_BLOCKs, and valid variable declarations.

**Engineering Quality: Variable**
Because BigQuery pulls from *every* repository, the quality of the logic varies wildly:
*   **The Good:** Highly optimized, production-grade logic from professional automation firms who open-sourced their core libraries.
*   **The Bad:** Student homework assignments (e.g., "traffic light controllers") that are syntactically perfect but logically simple or poorly named.

**The Verdict for AI Training:**
For training an LLM, this variability is actually **highly desirable**. To learn a language deeply, the AI needs to see millions of tokens of diverse, messy, real-world syntax, not just perfect textbook examples. BigQuery provides the raw volume of human-written syntax required to teach the model the "grammar" of IEC 61131-3, which we then refine with our ultra-high-quality Evol-Instruct synthetic data.
