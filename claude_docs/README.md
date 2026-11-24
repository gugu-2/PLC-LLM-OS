# Claude Documentation Archive — Lumina Industrial Automation AI Engine

This directory houses the technical documentation, forensic architecture audits, fine-tuning blueprints, and dataset specifications authored during the research, evolution, and audit phases of the **Lumina Cyber-Physical Industrial PLC-LLM** platform.

---

## 📑 Complete Document Index

### 1. The Core 6-Part Technical Architecture & Fine-Tuning Series

| Document | Title & Focus | Scope & Contents |
| :--- | :--- | :--- |
| **[`DOC_01_Critical_Path_Problems_And_Defects.md`](./DOC_01_Critical_Path_Problems_And_Defects.md)** | **Critical Path Forensic Post-Mortem & Corpus Pathology** | Comprehensive audit of historical project defects, non-manufacturing domain contamination, dataset size variance, syntax vs. semantic gaps, and prompt homogeneity. |
| **[`DOC_02_Architectural_Improvement_Roadmap.md`](./DOC_02_Architectural_Improvement_Roadmap.md)** | **Architectural Flaws & Systemic Remediation Blueprint** | Multi-layer engineering roadmap: Corpus Governance Schema v2.0, 3-Stage Semantic Validation Pipeline, Continuous Swarm Orchestration, and CI/CD Quality Gates. |
| **[`DOC_03_Fine_Tuning_Strategy_And_Best_Practices.md`](./DOC_03_Fine_Tuning_Strategy_And_Best_Practices.md)** | **Master Fine-Tuning Strategy & Industrial ML Engineering** | Base model selection (Qwen2.5-Coder-32B vs. DeepSeek), 4-stage fine-tuning recipe (Domain CPT, Heavy SFT, Multi-Format SFT, DPO/ORPO alignment), loss masking, and 32k-131k YaRN context scaling. |
| **[`DOC_04_Supplementary_Dataset_Design_Specification.md`](./DOC_04_Supplementary_Dataset_Design_Specification.md)** | **Structural & Task-Specific Dataset Engineering Specification** | Design blueprints for the 6 supplementary dataset archetypes: Dialogue Q&A, 3-Turn Debug Chains, Brownfield Code Modification, Theory-to-Code Bridges, Domain Text Corpora, and Safety SIF Logic. |
| **[`DOC_05_Data_Pipeline_And_Corpus_Processing_Guide.md`](./DOC_05_Data_Pipeline_And_Corpus_Processing_Guide.md)** | **Data Pipeline & Corpus Processing Implementation Guide** | Code-level implementations for the 5-stage corpus processing pipeline (`validate_domain.py`, `validate_iec.py`, `validate_semantic.py`, `size_gate.py`, MinHash LSH deduplication, and corpus indexing). |
| **[`DOC_06_Evaluation_Benchmarking_And_Deployment_Guide.md`](./DOC_06_Evaluation_Benchmarking_And_Deployment_Guide.md)** | **Evaluation Framework, Benchmarking & Production Deployment** | Quantitative industrial evaluation metrics (IEC-PR, DCA, ESCS, HR, IDR), 31-task held-out benchmark suite across unseen manufacturing plants, vLLM serving, and deployment gating. |

---

### 2. Comprehensive Deep Technical Audits

| Document | Title & Focus | Scope & Contents |
| :--- | :--- | :--- |
| **[`AUDIT_MASTER_EXECUTIVE_SUMMARY.md`](./AUDIT_MASTER_EXECUTIVE_SUMMARY.md)** | **Master Codebase & Architecture Audit Summary** | High-level synthesis of code, test, pipeline, and dataset audits with prioritized remediation roadmap. |
| **[`AUDIT_ARCHITECTURE_AND_PIPELINE_FLAWS.md`](./AUDIT_ARCHITECTURE_AND_PIPELINE_FLAWS.md)** | **System Architecture & Pipeline Fragmentation Audit** | In-depth analysis of module boundary defects, data pipeline disconnects, and environment isolation issues. |
| **[`AUDIT_CODE_BUGS_AND_TEST_FAILURES.md`](./AUDIT_CODE_BUGS_AND_TEST_FAILURES.md)** | **Code Bugs, Test Failures & Environment Defects** | Detailed findings on syntax parsing bugs, failing unit tests, import errors, and packaging mismatches. |
| **[`AUDIT_DATASET_ERRORS_AND_ANOMALIES.md`](./AUDIT_DATASET_ERRORS_AND_ANOMALIES.md)** | **Dataset Parity, Syntax Errors & Schema Anomalies** | Line-by-line validation audit of historical synthetic datasets across `data/swarm_raw/` and `data/master/`. |

---

### 3. Specifications, Backlogs & Sector Rankings

| Document | Title & Focus | Scope & Contents |
| :--- | :--- | :--- |
| **[`TOP_100_PLC_INDUSTRIAL_SECTORS_RANKED.md`](./TOP_100_PLC_INDUSTRIAL_SECTORS_RANKED.md)** | **Top 100 Commercial PLC Manufacturing Sectors** | Definitive commercial ranking of industrial automation sectors across Automotive, Semiconductor, Heavy Machinery, Plastics, and Food/Beverage. |
| **[`SYNTHETIC_DATASET_CATALOG.md`](./SYNTHETIC_DATASET_CATALOG.md)** | **Synthetic Dataset Catalog & Metadata Index** | Inventory of Function Blocks, domains, character counts, and cyber-physical control tags across generated datasets. |
| **[`ACTIVE_SUBAGENTS_BACKLOG.md`](./ACTIVE_SUBAGENTS_BACKLOG.md)** | **Active Subagent Swarm Backlog** | System tasks, sector assignments, and prompt templates for autonomous generation agents. |
| **[`ARCHITECTURE.md`](./ARCHITECTURE.md)** | **Platform Architecture Overview** | Overview of Lumina PLC-LLM platform components and runtime layers. |
| **[`DATA_PIPELINE.md`](./DATA_PIPELINE.md)** | **Data Pipeline Specification** | Data ingestion, validation, and serialization pipeline design. |
| **[`SWARM_OPERATIONS.md`](./SWARM_OPERATIONS.md)** | **Swarm Operations Guide** | Operating procedures for running parallel generation swarms and monitoring agents. |
