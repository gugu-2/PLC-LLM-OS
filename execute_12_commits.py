import os
import glob
import subprocess
import sys

def run_cmd(cmd):
    print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    res = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr:
        print("STDERR:", res.stderr.strip())
    if res.returncode != 0:
        print(f"FAILED with exit code {res.returncode}")
        sys.exit(res.returncode)
    return res.stdout

def main():
    # 1. Collect all untracked raw json files
    all_json = sorted(glob.glob("data/swarm_raw/*.json"))
    print(f"Total raw json datasets found: {len(all_json)}")
    
    # We want exactly 12 batches:
    # 6 batches of 7 (42) and 6 batches of 8 (48) = 90 files
    chunks = []
    idx = 0
    for b in range(1, 13):
        chunk_size = 7 if b <= 6 else 8
        chunk = all_json[idx:idx + chunk_size]
        chunks.append(chunk)
        idx += chunk_size
        print(f"Batch {b:02d}: {len(chunk)} files")
    
    # Commit 1: Stage deletions, modified engine scripts, brain_scratch, and Batch 1
    print("\n--- STAGING COMMIT 1 of 12 ---")
    run_cmd(["git", "add", "-u"])  # stages all tracked deletions & modifications (generate_agent_data.py, etc.)
    if os.path.exists("data/swarm_raw/script.py"):
        run_cmd(["git", "add", "data/swarm_raw/script.py"])
    if os.path.exists("brain_scratch"):
        run_cmd(["git", "add", "brain_scratch"])
    for f in chunks[0]:
        run_cmd(["git", "add", f])
    run_cmd(["git", "commit", "-m", "feat: Add massive V7 God-Tier synthetic data and engine updates - Batch 1 of 12"])
    
    # Commits 2 through 11
    for b in range(2, 12):
        print(f"\n--- STAGING COMMIT {b} of 12 ---")
        for f in chunks[b - 1]:
            run_cmd(["git", "add", f])
        run_cmd(["git", "commit", "-m", f"feat: Add massive V7 God-Tier synthetic data - Batch {b} of 12"])
    
    # Commit 12: Stage final batch and any remaining untracked items
    print("\n--- STAGING COMMIT 12 of 12 ---")
    for f in chunks[11]:
        run_cmd(["git", "add", f])
    run_cmd(["git", "add", "-A"])
    # Check if there is anything to commit for #12
    status = subprocess.run(["git", "status", "--porcelain", "--ignore-submodules"], capture_output=True, text=True).stdout
    if status.strip():
        run_cmd(["git", "commit", "-m", "feat: Add massive V7 God-Tier synthetic data - Batch 12 of 12"])
    else:
        print("Commit 12 already staged or no diff.")

    print("\n--- VERIFYING GIT LOG (LAST 14 COMMITS) ---")
    run_cmd(["git", "log", "-n", "14", "--oneline"])
    
    print("\n--- VERIFYING GIT STATUS ---")
    run_cmd(["git", "status", "--short", "--ignore-submodules"])

if __name__ == "__main__":
    main()
