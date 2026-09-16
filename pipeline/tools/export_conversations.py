"""
Script: export_conversations.py
Purpose: Parses the complete conversation transcript and exports all exchanges 
into categorized Markdown files organized by work type in the `conversation/` directory.
"""

import json
import os
import re
from datetime import datetime

TRANSCRIPT_PATH = r"C:\Users\majip\.gemini\antigravity\brain\4a136880-690c-422e-88be-60ce46a1b230\.system_generated\logs\transcript.jsonl"
OUTPUT_DIR = r"C:\Users\majip\Downloads\LLM REASEARCH\conversation"

CATEGORIES = {
    "ARCHITECTURE": {
        "filename": "01_Architecture_and_System_Design.md",
        "title": "01. Architecture, UI & System Foundations",
        "desc": "Conversations on project scoping (PLC-LLM-OS), AV2 directory setup, Replicate getdesign system, UI dashboards, JEPA architecture concepts, and baseline LLM model evaluation.",
        "keywords": ["av2", "markup", "raga", "replicate", "getdesign", "frontend", "front end", "dashboard", "jepa", "architecture", "base model", "qwen", "infrastructure", "recommendation"]
    },
    "SCRAPING": {
        "filename": "02_Natural_Data_Mining_and_Web_Scraping.md",
        "title": "02. Natural Data Mining & Web Scraping",
        "desc": "Conversations on scraping real-world PLC code: Tier 1 open-source repositories, Siemens Open Library, OSCAT Basic Library, GitHub Gists, Hugging Face datasets, YouTube, Reddit, crawler speed optimization, anti-blocking, and bottleneck analysis.",
        "keywords": ["scrap", "scrapping", "natural data", "oscat", "siemens", "hugging face", "reddit", "youtube", "gist", "mining", "bottleneck", "crawler"]
    },
    "SYNTHETIC_SWARM": {
        "filename": "03_Cloud_Swarm_Synthetic_Data_Generation.md",
        "title": "03. Cloud Swarm Synthetic Data Generation",
        "desc": "Conversations on launching multi-agent synthetic generation swarms with Gemini Pro: Evol-Instruct prompt engineering, 80+ advanced manufacturing domains, continuous cron looping (task-11326), rate limit / 429 management, and massive dataset scaling.",
        "keywords": ["synthetic", "swarm", "loop", "agent", "subagent", "pulse", "evolve", "evolver", "generate", "spin up", "50,000", "batch", "resilience"]
    },
    "DATA_AUDIT_FIXES": {
        "filename": "04_Data_Quality_Audits_and_IEC_Validation.md",
        "title": "04. Dataset Quality Audits, Bug Fixes & IEC 61131-3 Validation",
        "desc": "Conversations on auditing synthetic data quality, discovering 4/10 initial scores, structural validation enforcement (FB, VAR_INPUT, VAR_OUTPUT, END_IF/CASE, END_FUNCTION_BLOCK), eliminating double FUNCTION_BLOCK hallucinations, SHA-256 deduplication, and master dataset compilation.",
        "keywords": ["audit", "corrupt", "quality", "iec", "iec-st", "reanalyze", "randomly 10", "random 10", "recheck", "retest", "score", "flaw", "syntax", "structure", "pass", "threshold", "dedup", "sha-256"]
    },
    "TRAINING_PIPELINE": {
        "filename": "05_AI_Model_Training_and_FineTuning.md",
        "title": "05. AI Model Training Pipeline & Fine-Tuning",
        "desc": "Conversations on designing train.py, train_plc_llm.py, PyTorch LoRA/QLoRA pipelines, hyperparameter tuning, context window limits, tokenization, training loss evaluation, and mock vs physical PLC hardware testing.",
        "keywords": ["train", "training", "pytorch", "lora", "qlora", "fine tuning", "fine-tuning", "context window", "loss", "eval", "unsloth", "epoch", "learning rate"]
    },
    "LOCAL_OFFLINE_RTX5050": {
        "filename": "06_Local_Offline_Inference_and_RTX5050.md",
        "title": "06. Local Offline Pipeline & RTX 5050 Optimization",
        "desc": "Conversations on running offline LLMs on the user's laptop (NVIDIA RTX 5050 8GB VRAM, 16GB RAM): comparing Qwen2.5-Coder-14B (Q4_K_M vs Q3_K_M) vs 7B, VRAM mathematics, Ollama swarm generator, and setup automation.",
        "keywords": ["rtx 5050", "5050", "qwen2.5-coder", "quantiz", "offline", "14b", "7b", "8gb vram", "8 gigabyte", "vram", "ollama", "local llm", "laptop"]
    },
    "GIT_AND_MAINTENANCE": {
        "filename": "07_Git_Maintenance_and_Codebase_Hygiene.md",
        "title": "07. Git Repository Sync & Codebase Hygiene",
        "desc": "Conversations on pushing to GitHub (upload-workspace-20260818 branch), fixing failed git pushes, managing access tokens, archiving 186 legacy duplicate scripts into archive/legacy_scripts/, and comprehensive documentation generation.",
        "keywords": ["github", "git", "upload", "push", "re upload", "commit", "archive", "clean", "branch", "pat", "failed push"]
    }
}

def clean_text(t):
    if not t:
        return ""
    t = re.sub(r"<ADDITIONAL_METADATA>.*?</ADDITIONAL_METADATA>", "", t, flags=re.DOTALL)
    t = re.sub(r"<USER_SETTINGS_CHANGE>.*?</USER_SETTINGS_CHANGE>", "", t, flags=re.DOTALL)
    return t.strip()

def classify_turn(req_text):
    text = req_text.lower()
    if any(k in text for k in CATEGORIES["LOCAL_OFFLINE_RTX5050"]["keywords"]):
        return "LOCAL_OFFLINE_RTX5050"
    if any(k in text for k in ["github", "re upload", "upload the entire", "push", "failed push", "git"]):
        return "GIT_AND_MAINTENANCE"
    if any(k in text for k in ["pytorch", "train.py", "train_plc_llm", "fine tuning", "fine-tuning", "context window", "unsloth"]):
        return "TRAINING_PIPELINE"
    if any(k in text for k in ["audit", "corrupt", "reanalyze", "randomly 10", "random 10", "recheck", "retest", "score", "flaw", "iec 61131"]):
        return "DATA_AUDIT_FIXES"
    if any(k in text for k in ["scrap", "scrapping", "natural data", "oscat", "siemens", "hugging face", "reddit", "youtube", "gist"]):
        return "SCRAPING"
    if any(k in text for k in ["synthetic", "swarm", "loop", "agent", "subagent", "pulse", "evolve", "generate", "batch"]):
        return "SYNTHETIC_SWARM"
    return "ARCHITECTURE"

def parse_transcript():
    turns = []
    current_turn = None
    current_assistant_msgs = []
    current_tool_calls = []

    print(f"Reading transcript: {TRANSCRIPT_PATH}")
    with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f):
            try:
                d = json.loads(line)
                stype = d.get("type")
                if stype == "USER_INPUT":
                    content = d.get("content", "")
                    if "<USER_REQUEST>" in content:
                        if current_turn is not None:
                            current_turn["assistant_responses"] = current_assistant_msgs
                            current_turn["tool_calls"] = current_tool_calls
                            turns.append(current_turn)

                        start = content.find("<USER_REQUEST>") + len("<USER_REQUEST>")
                        end = content.find("</USER_REQUEST>")
                        req_text = content[start:end].strip() if end != -1 else content[start:].strip()
                        req_text = clean_text(req_text)

                        current_turn = {
                            "turn_num": len(turns) + 1,
                            "created_at": d.get("created_at", ""),
                            "request": req_text,
                            "category": classify_turn(req_text)
                        }
                        current_assistant_msgs = []
                        current_tool_calls = []
                elif stype == "PLANNER_RESPONSE":
                    if current_turn is not None:
                        txt = d.get("content", "")
                        if txt:
                            current_assistant_msgs.append(txt.strip())
                        tcalls = d.get("tool_calls", [])
                        for tc in tcalls:
                            if isinstance(tc, dict):
                                summ = tc.get("toolSummary") or tc.get("toolAction")
                                if summ and summ not in current_tool_calls:
                                    current_tool_calls.append(summ)
            except Exception as e:
                pass

    if current_turn is not None:
        current_turn["assistant_responses"] = current_assistant_msgs
        current_turn["tool_calls"] = current_tool_calls
        turns.append(current_turn)

    print(f"Parsed {len(turns)} total conversation turns.")
    return turns

def format_turn_markdown(turn):
    md = []
    created_at = turn["created_at"]
    try:
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        dt_str = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except:
        dt_str = created_at

    md.append(f"### Turn #{turn['turn_num']} — `{dt_str}`\n")
    md.append(f"> **User Request:**\n> {turn['request'].replace(chr(10), chr(10) + '> ')}\n")
    
    if turn["tool_calls"]:
        md.append("**Actions & Tools Executed:**")
        for tc in turn["tool_calls"][:10]:
            md.append(f"- `{tc}`")
        if len(turn["tool_calls"]) > 10:
            md.append(f"- *...and {len(turn['tool_calls']) - 10} more tool operations.*")
        md.append("")

    if turn["assistant_responses"]:
        md.append("**Assistant Response:**\n")
        resp_text = "\n\n---\n\n".join(turn["assistant_responses"])
        md.append(resp_text)
        md.append("\n")
    else:
        md.append("*No text response recorded (command/tool execution turn).*\n")

    md.append("---\n")
    return "\n".join(md)

def export_all():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    turns = parse_transcript()

    categorized_turns = {cat: [] for cat in CATEGORIES}
    for turn in turns:
        cat = turn["category"]
        categorized_turns[cat].append(turn)

    # 1. Generate Thematic Files
    for cat_key, cat_meta in CATEGORIES.items():
        cat_turns = categorized_turns[cat_key]
        filepath = os.path.join(OUTPUT_DIR, cat_meta["filename"])
        print(f"Writing {cat_meta['filename']} ({len(cat_turns)} turns)...")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {cat_meta['title']}\n\n")
            f.write(f"**Category Identifier:** `{cat_key}`  \n")
            f.write(f"**Total Documented Exchanges:** {len(cat_turns)}  \n")
            if cat_turns:
                first_time = cat_turns[0]["created_at"][:10]
                last_time = cat_turns[-1]["created_at"][:10]
                f.write(f"**Timeline Covered:** {first_time} to {last_time}  \n\n")
            else:
                f.write("**Timeline Covered:** N/A  \n\n")

            f.write("## 1. Domain Overview & Purpose\n")
            f.write(f"{cat_meta['desc']}\n\n")
            f.write("---\n\n")
            f.write("## 2. Conversation Trajectory\n\n")

            if not cat_turns:
                f.write("*No specific turns recorded under this category.*\n")
            else:
                for turn in cat_turns:
                    f.write(format_turn_markdown(turn))

    # 2. Generate Master Chronology & Index
    index_path = os.path.join(OUTPUT_DIR, "00_Master_Chronology_and_Index.md")
    print("Writing 00_Master_Chronology_and_Index.md...")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("# PLC-LLM-OS: Complete Conversation Archive & Master Index\n\n")
        f.write(f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}  \n")
        f.write(f"**Total Conversation Turns:** {len(turns)}  \n")
        f.write(f"**Workspace:** `C:\\Users\\majip\\Downloads\\LLM REASEARCH`  \n\n")

        f.write("## 1. Executive Project Summary\n")
        f.write("This archive preserves the complete engineering history, architectural debates, ")
        f.write("agent swarm designs, dataset curation loops, hardware benchmarks, and training pipeline development ")
        f.write("for the **PLC-LLM-OS (Lumina AI)** autonomous code generation project.\n\n")

        f.write("## 2. Thematic Work Breakdown Files\n\n")
        f.write("| File | Category | Total Turns | Key Topics & Scope |\n")
        f.write("| :--- | :--- | :---: | :--- |\n")
        for cat_key, cat_meta in CATEGORIES.items():
            count = len(categorized_turns[cat_key])
            f.write(f"| [{cat_meta['filename']}](./{cat_meta['filename']}) | `{cat_key}` | **{count}** | {cat_meta['desc']} |\n")
        f.write(f"| [08_Complete_Chronological_Archive.md](./08_Complete_Chronological_Archive.md) | `ALL` | **{len(turns)}** | Complete sequential record of all turns from start to finish. |\n\n")

        f.write("## 3. High-Level Project Evolution Milestones\n")
        f.write("- **Milestone 1 (Aug 14-16): Foundations & AV2** — Reviewed initial codebases (`markup`, `raga`), established `AV2/` architecture, integrated Replicate design system, selected Qwen2.5-Coder as foundational base LLM.\n")
        f.write("- **Milestone 2 (Aug 16-20): Natural Data Mining** — Designed scrapers for Siemens Open Library, OSCAT, Hugging Face, GitHub Gists, Reddit, and YouTube; tackled bot detection and dynamic scraping bottlenecks.\n")
        f.write("- **Milestone 3 (Aug 20-31): Synthetic Swarm Launch** — Orchestrated Gemini Pro multi-agent Evol-Instruct swarms across 80+ manufacturing domains; established background cron scheduling.\n")
        f.write("- **Milestone 4 (Aug 31 - Sep 3): Quality Reform & IEC 61131-3 Standard** — Audited synthetic data discovering a 4/10 baseline; enforced 5 mandatory structural syntax lines; fixed double `FUNCTION_BLOCK` bug; implemented SHA-256 deduplication.\n")
        f.write("- **Milestone 5 (Sep 11): Codebase Cleanup & Master Dataset Build** — Archived 186 duplicate legacy scripts into `archive/legacy_scripts/`; compiled clean 1,459-record master dataset; pushed to GitHub.\n")
        f.write("- **Milestone 6 (Sep 11): Offline Edge Pipeline (RTX 5050)** — Evaluated Qwen2.5-Coder-14B (Q4_K_M vs Q3_K_M) vs 7B on 8GB VRAM; provided mathematical proof of VRAM constraints; deployed offline Ollama pipeline.\n")
        f.write("- **Milestone 7 (Sep 11-12): Autonomous Continuous Flywheel** — Restarted 6-minute background cron swarm (`task-11326`), producing verified, ultra-complex industrial structured text.\n\n")

        f.write("## 4. Master Chronological Index of All Turns\n\n")
        f.write("| # | Date / Time | Category | User Request Preview | Target Document |\n")
        f.write("| :---: | :--- | :--- | :--- | :--- |\n")
        for turn in turns:
            cat = turn["category"]
            cat_file = CATEGORIES[cat]["filename"]
            preview = (turn["request"][:70] + "...") if len(turn["request"]) > 70 else turn["request"]
            preview = preview.replace("|", "\\|").replace("\n", " ")
            t_str = turn["created_at"][:16].replace("T", " ")
            f.write(f"| {turn['turn_num']} | `{t_str}` | `{cat}` | {preview} | [{cat_file}](./{cat_file}) |\n")

    # 3. Generate Complete Chronological Archive
    chrono_path = os.path.join(OUTPUT_DIR, "08_Complete_Chronological_Archive.md")
    print("Writing 08_Complete_Chronological_Archive.md...")
    with open(chrono_path, "w", encoding="utf-8") as f:
        f.write("# Complete Chronological Conversation Archive\n\n")
        f.write(f"**Total Documented Turns:** {len(turns)}  \n")
        f.write(f"**Timeline:** {turns[0]['created_at'][:10]} to {turns[-1]['created_at'][:10]}  \n\n")
        f.write("This document is the complete, unbroken, chronological transcription of every single exchange in this project.\n\n")
        f.write("---\n\n")
        for turn in turns:
            f.write(format_turn_markdown(turn))

    print(f"\nSUCCESS! All conversation files created in: {OUTPUT_DIR}")

if __name__ == "__main__":
    export_all()
