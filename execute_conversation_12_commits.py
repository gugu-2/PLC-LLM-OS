#!/usr/bin/env python3
"""
Executes the 12-Commit Sequence for the Complete Conversation History & Changelog
Commits each extracted conversation archive and changelog into 12 structured parts,
then pushes cleanly to origin/main on GitHub.
"""

import subprocess
import os
import sys

def run_cmd(cmd, check=True):
    print(f">> Running: {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr:
        print("STDERR:", res.stderr.strip())
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed with code {res.returncode}: {cmd}")
    return res

commits = [
    # Commit 1
    (
        "feat(tooling): Add automated conversation transcript & changelog extractor [Part 1/12]",
        ["scripts/extract_conversation_history.py"]
    ),
    # Commit 2
    (
        "docs(archive): Update master chronology and turn index covering 306 interactions [Part 2/12]",
        ["conversation/00_Master_Chronology_and_Index.md"]
    ),
    # Commit 3
    (
        "docs(archive): Ingest recent turns for system architecture and AV2 scoping [Part 3/12]",
        ["conversation/01_Architecture_and_System_Design.md"]
    ),
    # Commit 4
    (
        "docs(archive): Audit natural data mining and web scraping history [Part 4/12]",
        ["conversation/02_Natural_Data_Mining_and_Web_Scraping.md"]
    ),
    # Commit 5
    (
        "docs(archive): Expand cloud swarm generation archive with commercial factory domains [Part 5/12]",
        ["conversation/03_Cloud_Swarm_Synthetic_Data_Generation.md"]
    ),
    # Commit 6
    (
        "docs(archive): Complete IEC 61131-3 verification and dataset quality audit archive [Part 6/12]",
        ["conversation/04_Data_Quality_Audits_and_IEC_Validation.md"]
    ),
    # Commit 7
    (
        "docs(archive): Audit AI model training, LoRA fine-tuning, and loss metrics [Part 7/12]",
        ["conversation/05_AI_Model_Training_and_FineTuning.md"]
    ),
    # Commit 8
    (
        "docs(archive): Update local offline inference and RTX 5050 VRAM analysis [Part 8/12]",
        ["conversation/06_Local_Offline_Inference_and_RTX5050.md"]
    ),
    # Commit 9
    (
        "docs(archive): Update git maintenance, multi-part commit, and migration logs [Part 9/12]",
        ["conversation/07_Git_Maintenance_and_Codebase_Hygiene.md"]
    ),
    # Commit 10
    (
        "docs(archive): Extend complete chronological transcript archive to Turn 306 [Part 10/12]",
        ["conversation/08_Complete_Chronological_Archive.md"]
    ),
    # Commit 11
    (
        "docs(changelog): Ingest complete 306-turn project lifetime engineering changelog [Part 11/12]",
        ["conversation/09_Full_Project_Lifetime_Chat_History_and_Changelog.md"]
    ),
    # Commit 12
    (
        "docs(manifest): Synchronize migration playbook and documentation with 306-turn audit [Part 12/12]",
        ["HOW_TO_PROMPT_AGENT_ON_NEW_COMPUTER.md", "execute_conversation_12_commits.py"]
    )
]

print("==================================================")
print(">>> STARTING 12-COMMIT CONVERSATION ARCHIVE SEQUENCE")
print("==================================================")

for idx, (msg, targets) in enumerate(commits, 1):
    print(f"\n--------------------------------------------------")
    print(f"PROCESSING COMMIT {idx}/12: {msg}")
    print(f"--------------------------------------------------")
    for t in targets:
        if os.path.exists(t):
            run_cmd(f"git add -A \"{t}\"", check=False)
        else:
            run_cmd(f"git add -u \"{t}\"", check=False)
    
    diff_res = run_cmd("git diff --cached --name-only", check=False)
    staged = diff_res.stdout.strip()
    if not staged:
        print(f"Notice: No staged changes for commit {idx}.")
    else:
        print(f"Staged {len(staged.splitlines())} files.")
        commit_res = subprocess.run(["git", "commit", "-m", msg], capture_output=True, text=True)
        if commit_res.stdout:
            print(commit_res.stdout.strip())
        if commit_res.returncode != 0:
            print("Commit info:", commit_res.stderr.strip())

print("\n==================================================")
print("PUSHING ALL 12 COMMITS TO GITHUB (ORIGIN MAIN)...")
print("==================================================")
push_res = run_cmd("git push origin main")
print(push_res.stdout.strip())

print("\nRecent 14 Commits on origin/main:")
run_cmd("git log -n 14 --oneline")
print("\n[OK] All 12 commits generated and pushed to GitHub successfully!")
