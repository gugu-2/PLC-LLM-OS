#!/usr/bin/env python3
"""
Comprehensive Conversation History & Changelog Extractor with Full Secret Sanitization.
Parses transcript.jsonl from start to current turn (turns 1 to 306+),
documents all user requests, tools invoked, code/file changes made,
sanitizes any credentials/tokens to satisfy GitHub Push Protection,
and generates structured Markdown archives in conversation/.
"""

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

TRANSCRIPT_PATH = r"C:\Users\majip\.gemini\antigravity\brain\4a136880-690c-422e-88be-60ce46a1b230\.system_generated\logs\transcript.jsonl"
CONVERSATION_DIR = Path("conversation")
CONVERSATION_DIR.mkdir(parents=True, exist_ok=True)


def sanitize_all_secrets(text):
    """Aggressively redact API keys, personal access tokens, and credentials."""
    if not text:
        return text
    # GitHub Tokens
    text = re.sub(r'github_pat_[A-Za-z0-9_]{20,}', '[REDACTED_GITHUB_PAT]', text)
    text = re.sub(r'gh[pous]_[A-Za-z0-9_]{20,}', '[REDACTED_GITHUB_TOKEN]', text)
    # Google/GCP API Keys & OAuth Tokens
    text = re.sub(r'AIza[0-9A-Za-z\-_]{25,}', '[REDACTED_GCP_API_KEY]', text)
    text = re.sub(r'AQ\.[A-Za-z0-9_\-]+', '[REDACTED_GCP_TOKEN]', text)
    # OpenAI & Anthropic API Keys
    text = re.sub(r'sk-[A-Za-z0-9\-_]{20,}', '[REDACTED_OPENAI_KEY]', text)
    text = re.sub(r'sk-ant-[A-Za-z0-9\-_]{20,}', '[REDACTED_ANTHROPIC_KEY]', text)
    # Hugging Face Tokens
    text = re.sub(r'hf_[A-Za-z0-9]{20,}', '[REDACTED_HF_TOKEN]', text)
    # Private Keys & JWT
    text = re.sub(r'-----BEGIN [A-Z ]+ PRIVATE KEY-----.*?-----END [A-Z ]+ PRIVATE KEY-----', '[REDACTED_PRIVATE_KEY]', text, flags=re.DOTALL)
    text = re.sub(r'Bearer\s+[A-Za-z0-9\-_.]+', 'Bearer [REDACTED_BEARER_TOKEN]', text)
    # GCP Service Account private key fields
    text = re.sub(r'"private_key":\s*"[^"]+"', '"private_key": "[REDACTED_PRIVATE_KEY]"', text)
    return text


def clean_user_content(raw):
    """Strip <USER_REQUEST> tags and metadata and sanitize secrets."""
    if not raw:
        return ""
    text = re.sub(r"<USER_REQUEST>", "", raw)
    text = re.sub(r"</USER_REQUEST>.*", "", text, flags=re.DOTALL)
    text = re.sub(r"<ADDITIONAL_METADATA>.*?</ADDITIONAL_METADATA>", "", text, flags=re.DOTALL)
    return sanitize_all_secrets(text.strip())


def categorize_turn(turn):
    """Assign a domain category based on request content and actions."""
    u = turn["user_text"].lower()

    if any(k in u for k in ["commercial", "automotive", "smt", "injection", "bottling", "stamping", "cnc", "delta robot"]):
        return "COMMERCIAL_MANUFACTURING"
    if any(k in u for k in ["upload", "git", "commit", "push", "remote", "repository", "github", "pen drive", "copy folder"]):
        return "GIT_AND_MAINTENANCE"
    if any(k in u for k in ["rtx", "5050", "vram", "ollama", "offline", "quantization", "qwen2.5-coder-14b"]):
        return "LOCAL_OFFLINE_RTX5050"
    if any(k in u for k in ["train", "loss", "lora", "qlora", "fine-tuning", "finetuning", "hyperparameter", "eval"]):
        return "TRAINING_PIPELINE"
    if any(k in u for k in ["audit", "verify", "validation", "parities", "syntax", "iec-st", "function_block", "repair"]):
        return "DATA_AUDIT_FIXES"
    if any(k in u for k in ["scrap", "mining", "forum", "youtube", "reddit", "crawler", "github bulk"]):
        return "SCRAPING"
    if any(k in u for k in ["swarm", "subagent", "synthetic", "tokens", "eat all the tokens", "evol-instruct", "gemini"]):
        return "SYNTHETIC_SWARM"
    if any(k in u for k in ["project", "architecture", "folder", "design", "av2", "ui", "dashboard", "jepa"]):
        return "ARCHITECTURE"
    return "SYNTHETIC_SWARM"


def parse_transcript():
    turns = []
    current_turn = None

    print(f"Reading transcript from {TRANSCRIPT_PATH}...")
    with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
        for line_idx, line in enumerate(f):
            if not line.strip():
                continue
            data = json.loads(line)
            stype = data.get("type")

            if stype == "USER_INPUT":
                if current_turn:
                    turns.append(current_turn)
                raw_content = data.get("content", "")
                clean_text = clean_user_content(raw_content)
                current_turn = {
                    "turn_number": len(turns) + 1,
                    "step_index": data.get("step_index", line_idx),
                    "created_at": data.get("created_at", ""),
                    "raw_user_content": raw_content,
                    "user_text": clean_text,
                    "tool_names": [],
                    "files_written": [],
                    "files_edited": [],
                    "commands_run": [],
                    "subagents_spawned": [],
                    "assistant_text_snippets": [],
                    "summary_of_changes": ""
                }
            elif current_turn:
                if stype == "PLANNER_RESPONSE":
                    text = data.get("content", "")
                    if text:
                        current_turn["assistant_text_snippets"].append(sanitize_all_secrets(text))
                    for tc in data.get("tool_calls", []):
                        name = tc.get("name", "")
                        args = tc.get("args", {})
                        current_turn["tool_names"].append(name)
                        if name == "write_file":
                            p = args.get("Path", "")
                            if p and p not in current_turn["files_written"]:
                                current_turn["files_written"].append(p)
                        elif name == "edit_file":
                            p = args.get("Path", "")
                            if p and p not in current_turn["files_edited"]:
                                current_turn["files_edited"].append(p)
                        elif name == "run_command":
                            cmd = sanitize_all_secrets(args.get("CommandLine", ""))
                            if cmd and cmd not in current_turn["commands_run"]:
                                current_turn["commands_run"].append(cmd)
                        elif name == "invoke_subagent":
                            role = args.get("Role") or args.get("TypeName") or "Subagent"
                            current_turn["subagents_spawned"].append(role)

    if current_turn:
        turns.append(current_turn)

    for t in turns:
        t["category"] = categorize_turn(t)
        changes = []
        if t["files_written"]:
            changes.append(f"Created/Wrote {len(t['files_written'])} files: " + ", ".join([Path(p).name for p in t["files_written"][:6]]))
            if len(t["files_written"]) > 6:
                changes[-1] += f" (+{len(t['files_written'])-6} more)"
        if t["files_edited"]:
            changes.append(f"Modified {len(t['files_edited'])} files: " + ", ".join([Path(p).name for p in t["files_edited"][:6]]))
        if t["commands_run"]:
            cmds_clean = [c.split()[0] if c.split() else c for c in t["commands_run"][:4]]
            changes.append(f"Executed {len(t['commands_run'])} CLI commands ({', '.join(set(cmds_clean))})")
        if t["subagents_spawned"]:
            changes.append(f"Orchestrated {len(t['subagents_spawned'])} subagents ({', '.join(t['subagents_spawned'][:4])})")
        if not changes:
            changes.append("Technical consultation, architecture analysis, mathematical proof & prompt formulation")
        t["summary_of_changes"] = " | ".join(changes)

    print(f"Total turns successfully extracted: {len(turns)}")
    return turns


def generate_master_changelog(turns):
    """Create 09_Full_Project_Lifetime_Chat_History_and_Changelog.md with redacted credentials."""
    out_path = CONVERSATION_DIR / "09_Full_Project_Lifetime_Chat_History_and_Changelog.md"
    print(f"Writing master changelog to {out_path}...")

    now_str = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    lines = [
        "# Complete Project Lifetime Chat History & Engineering Changelog",
        "",
        f"**Project:** Lumina PLC-LLM-OS  ",
        f"**Extraction Timestamp:** {now_str} UTC  ",
        f"**Total Conversation Turns Recorded:** {len(turns)}  ",
        f"**Scope:** Complete chronological audit of all user prompts, engineering actions, file mutations, and dataset milestones from Turn #1 to Turn #{len(turns)}.",
        "",
        "---",
        "",
        "## Executive Summary of Project Evolution",
        "- **Phase 1 (Turns 1-45): Foundations & Architecture Scoping** - Evaluated baseline PLC repositories, setup `AV2/` architecture, integrated Replicate design system, benchmarked Qwen2.5-Coder as base LLM.",
        "- **Phase 2 (Turns 46-110): Natural Web Scraping & Mining** - Built web scrapers across GitHub, Siemens Open Library, OSCAT, Hugging Face, Reddit, and YouTube transcripts; handled bot blocking.",
        "- **Phase 3 (Turns 111-190): Cloud Swarm & Synthetic Evol-Instruct** - Launched Gemini Pro multi-agent swarms across 80+ extreme cyber-physical domains; configured automated background crons.",
        "- **Phase 4 (Turns 191-230): Quality Audits & Parity Enforcement** - Diagnosed syntax anomalies, instituted strict AST parity validation, fixed double `FUNCTION_BLOCK` bugs, and conducted SHA-256 deduplication.",
        "- **Phase 5 (Turns 231-259): Edge Inference Optimization & Code Cleanup** - Benchmarked RTX 5050 (8GB VRAM) for offline Qwen2.5-Coder-14B inference; archived 186 legacy scripts.",
        "- **Phase 6 (Turns 260-290): The 12-Commit Sequence & Dataset Repository Partitioning** - Partitioned synthetic datasets into 12 thematic commits (`[Part 1/12]` to `[Part 12/12]`); created dedicated `PLC-DATA-EXTRACT` standalone repository.",
        "- **Phase 7 (Turns 291-306): Computer Migration, Commercial Focus & Swarm Lifecycle** - Established 1-Agent = 1-Dataset lifecycle; shifted domain catalog exclusively to billion-dollar commercial manufacturing (Automotive EV, SMT, Heavy Press, Plastics, Aseptic Bottling); engineered self-healing USB setup scripts.",
        "",
        "---",
        "",
        "## Complete Turn-by-Turn Chat Audit & Changelog",
        ""
    ]

    for t in turns:
        t_num = t["turn_number"]
        t_time = t["created_at"].replace("T", " ").replace("Z", "")
        cat = t["category"]
        user_prompt = t["user_text"] or "(Empty / System Action)"
        changes = t["summary_of_changes"]

        lines.append(f"### Turn #{t_num} - [{cat}] ({t_time} UTC)")
        lines.append(f"**Step Index:** `{t['step_index']}`  ")
        lines.append(f"**User Request / Prompt:**")
        lines.append(f"> {user_prompt}")
        lines.append("")
        lines.append(f"**Changes Performed:**")
        lines.append(f"- **Summary:** {changes}")

        if t["files_written"]:
            lines.append("- **Files Created / Written:**")
            for f in t["files_written"][:8]:
                lines.append(f"  - `{f}`")
            if len(t["files_written"]) > 8:
                lines.append(f"  - *(+{len(t['files_written'])-8} additional files)*")

        if t["files_edited"]:
            lines.append("- **Files Modified:**")
            for f in t["files_edited"][:8]:
                lines.append(f"  - `{f}`")

        if t["commands_run"]:
            lines.append("- **Commands Executed:**")
            for c in t["commands_run"][:5]:
                clean_cmd = c.strip().replace("\n", " ")
                lines.append(f"  - `{clean_cmd[:100]}`")

        if t["subagents_spawned"]:
            lines.append(f"- **Subagents Spawned:** {', '.join(set(t['subagents_spawned']))}")

        if t["assistant_text_snippets"]:
            first_resp = t["assistant_text_snippets"][0].strip()
            preview = first_resp.split("\n\n")[0][:300].replace("\n", " ")
            lines.append(f"- **Outcome & Guidance:** {preview}...")

        lines.append("")
        lines.append("---")
        lines.append("")

    full_text = sanitize_all_secrets("\n".join(lines))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"Master changelog saved: {out_path} ({os.path.getsize(out_path)/(1024*1024):.2f} MB)")


def update_master_index(turns):
    """Update 00_Master_Chronology_and_Index.md with turns 1 to 306."""
    out_path = CONVERSATION_DIR / "00_Master_Chronology_and_Index.md"
    print(f"Updating master index at {out_path}...")

    cats = {}
    for t in turns:
        c = t["category"]
        cats[c] = cats.get(c, 0) + 1

    now_str = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    lines = [
        "# PLC-LLM-OS: Complete Conversation Archive & Master Index",
        "",
        f"**Generated / Updated:** {now_str} UTC  ",
        f"**Total Conversation Turns:** {len(turns)}  ",
        f"**Workspace:** `C:\\Users\\majip\\Downloads\\LLM REASEARCH`  ",
        "",
        "## 1. Executive Project Summary",
        "This archive preserves the complete engineering history, architectural debates, agent swarm designs, dataset curation loops, hardware benchmarks, computer migration scripts, and commercial manufacturing focus for the **PLC-LLM-OS (Lumina AI)** autonomous code generation project.",
        "",
        "## 2. Thematic Work Breakdown Files",
        "",
        "| File | Category | Total Turns | Key Topics & Scope |",
        "| :--- | :--- | :---: | :--- |",
        f"| [01_Architecture_and_System_Design.md](./01_Architecture_and_System_Design.md) | `ARCHITECTURE` | **{cats.get('ARCHITECTURE', 0)}** | Scoping, AV2 directory setup, Replicate design system, UI dashboards, JEPA concepts, and baseline LLM model evaluation. |",
        f"| [02_Natural_Data_Mining_and_Web_Scraping.md](./02_Natural_Data_Mining_and_Web_Scraping.md) | `SCRAPING` | **{cats.get('SCRAPING', 0)}** | Scraping real-world PLC code: Tier 1 open-source repositories, Siemens Open Library, OSCAT, GitHub Gists, Hugging Face, YouTube, Reddit, crawler speed optimization. |",
        f"| [03_Cloud_Swarm_Synthetic_Data_Generation.md](./03_Cloud_Swarm_Synthetic_Data_Generation.md) | `SYNTHETIC_SWARM` | **{cats.get('SYNTHETIC_SWARM', 0) + cats.get('COMMERCIAL_MANUFACTURING', 0)}** | Multi-agent synthetic generation swarms with Gemini Pro: Evol-Instruct prompt engineering, 80+ advanced manufacturing domains, continuous cron looping, rate limit management. |",
        f"| [04_Data_Quality_Audits_and_IEC_Validation.md](./04_Data_Quality_Audits_and_IEC_Validation.md) | `DATA_AUDIT_FIXES` | **{cats.get('DATA_AUDIT_FIXES', 0)}** | Auditing synthetic data quality, structural validation enforcement, eliminating double FUNCTION_BLOCK hallucinations, SHA-256 deduplication, and master dataset compilation. |",
        f"| [05_AI_Model_Training_and_FineTuning.md](./05_AI_Model_Training_and_FineTuning.md) | `TRAINING_PIPELINE` | **{cats.get('TRAINING_PIPELINE', 0)}** | Designing train.py, PyTorch LoRA/QLoRA pipelines, hyperparameter tuning, context window limits, tokenization, training loss evaluation. |",
        f"| [06_Local_Offline_Inference_and_RTX5050.md](./06_Local_Offline_Inference_and_RTX5050.md) | `LOCAL_OFFLINE_RTX5050` | **{cats.get('LOCAL_OFFLINE_RTX5050', 0)}** | Running offline LLMs on RTX 5050 8GB VRAM: Qwen2.5-Coder-14B (Q4_K_M vs Q3_K_M) vs 7B, VRAM mathematics, Ollama swarm generator, and setup automation. |",
        f"| [07_Git_Maintenance_and_Codebase_Hygiene.md](./07_Git_Maintenance_and_Codebase_Hygiene.md) | `GIT_AND_MAINTENANCE` | **{cats.get('GIT_AND_MAINTENANCE', 0)}** | Pushing to GitHub, managing access tokens, executing the 12-commit sequence, computer migration playbooks (`setup_new_computer.ps1`), pen drive transfers. |",
        f"| [08_Complete_Chronological_Archive.md](./08_Complete_Chronological_Archive.md) | `ALL` | **{len(turns)}** | Complete sequential transcript archive of all turns from start to current. |",
        f"| [09_Full_Project_Lifetime_Chat_History_and_Changelog.md](./09_Full_Project_Lifetime_Chat_History_and_Changelog.md) | `FULL_LIFETIME` | **{len(turns)}** | Master chronological audit of every turn, user prompt, and exact file changes from Day 1 to current. |",
        "",
        "## 3. Master Chronological Index of All Turns (1 to " + str(len(turns)) + ")",
        "",
        "| # | Date / Time | Category | User Request Preview | Changes Summary |",
        "| :---: | :--- | :--- | :--- | :--- |"
    ]

    for t in turns:
        t_num = t["turn_number"]
        t_time = t["created_at"][:16].replace("T", " ")
        cat = t["category"]
        u_prev = (t["user_text"] or "(System prompt)").replace("\n", " ")[:60].replace("|", "/")
        c_prev = t["summary_of_changes"][:65].replace("|", "/")
        lines.append(f"| {t_num} | `{t_time}` | `{cat}` | {u_prev}... | {c_prev}... |")

    full_text = sanitize_all_secrets("\n".join(lines))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"Master index updated: {out_path}")


def sanitize_existing_files():
    """Sanitize all files in conversation directory to guarantee zero secret scanning triggers."""
    print("Sanitizing all existing files in conversation/...")
    for fpath in CONVERSATION_DIR.glob("*.md"):
        content = fpath.read_text(encoding="utf-8")
        sanitized = sanitize_all_secrets(content)
        if sanitized != content:
            fpath.write_text(sanitized, encoding="utf-8")
            print(f"Sanitized secrets in: {fpath.name}")


def main():
    turns = parse_transcript()
    generate_master_changelog(turns)
    update_master_index(turns)
    sanitize_existing_files()
    print("\n[OK] All conversation extraction, changelog generation, and secret sanitization complete!")


if __name__ == "__main__":
    main()
