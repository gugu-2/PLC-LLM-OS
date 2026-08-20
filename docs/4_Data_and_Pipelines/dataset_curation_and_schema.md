# Dataset Curation & DSL Schema Integrity

## 1. The Quality vs. Quantity Dilemma
In LLM training for industrial automation, quantity is dangerous. Scraping GitHub for random `.st` or `.l5x` files yields incredibly sloppy, unsafe, or non-compiling code. Lumina enforces strict quality gating.

## 2. Logic Density Heuristics (`clean_dataset.py`)
Before a scraped file is allowed into the training pipeline, it passes through the Dataset Cleaner.
- **AST Parsing:** If the file does not have a minimum density of assignment operators (`:=`) or branch logic (`IF`, `CASE`), it is immediately purged as "No-Op" junk.
- **Tag Validation:** If memory addresses are referenced without being formally typed (e.g., `INT`, `BOOL`), it is discarded.

## 3. The Strict JSON DSL Schema
The `train_dataset_formatter.py` guarantees that Qwen2.5-Coder only trains on structurally perfect data.
- **The Input Format:** The dataset uses an Intermediate Textual DSL.
- **Fields:** Every single record *must* contain a natural language `Specification`, an explicit array of `Required Interlocks`, and the compiled `ST Code`. 
- If a dataset example lacks safety interlock declarations, the `validate_st_dsl_schema()` function purges it to prevent the LLM from learning reckless coding behaviors.
