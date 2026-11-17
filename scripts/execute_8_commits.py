# scripts/execute_8_commits.py
import subprocess
import os
import sys

def run_git(cmd):
    print(f"Executing: git {' '.join(cmd)}")
    res = subprocess.run(["git"] + cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error: {res.stderr}")
        sys.exit(1)
    if res.stdout.strip():
        print(res.stdout.strip())
    return res.stdout.strip()

def main():
    # Verify status
    status = subprocess.check_output(["git", "status", "--porcelain"]).decode("utf-8")
    lines = status.splitlines()

    deleted_files = [l.split(maxsplit=1)[1] for l in lines if l.startswith(" D") or l.startswith("D ")]
    untracked_files = [l.split(maxsplit=1)[1] for l in lines if l.startswith("??")]
    modified_files = [l.split(maxsplit=1)[1] for l in lines if l.startswith(" M") or l.startswith("M ")]

    print(f"Total deleted: {len(deleted_files)}")
    print(f"Total untracked: {len(untracked_files)}")
    print(f"Total modified: {len(modified_files)}")

    raw_datasets = sorted([f for f in untracked_files if f.startswith("data/swarm_raw")])
    print(f"Total raw datasets untracked: {len(raw_datasets)}")

    # ----------------------------------------------------
    # COMMIT 1: Purge deleted files & quarantined datasets
    # ----------------------------------------------------
    print("\n=== STAGING COMMIT 1 ===")
    for df in deleted_files:
        run_git(["rm", "--cached", "-r", "--ignore-unmatch", df])
    # Also remove them from index
    run_git(["commit", "-m", "refactor(cleanup): purge legacy builder artifacts and quarantined flawed datasets [Commit 1/8]"])

    # ----------------------------------------------------
    # COMMIT 2: Core toolchain, validation scripts & st files
    # ----------------------------------------------------
    print("\n=== STAGING COMMIT 2 ===")
    toolchain_files = [
        "package_dataset.py",
        "save_and_validate_dataset.py",
        "save_dataset.py",
        "assemble_tape_reel.py",
        "assemble_trt.py",
        "build_and_save_dataset.py",
        "build_and_validate_dataset.py",
        "build_dataset.py",
        "build_gigapress_block.py",
        "build_gigapress_full.py",
        "find_comment.py",
        "generate_ecu_smt_fb.py",
        "generate_stamping_press.py",
        "save_and_validate_dyno.py",
        "scratch/check_progress.py",
        "scripts/check_agents.py",
        "scripts/execute_8_commits.py",
        "section0_and_1.py",
        "section2_physics.py",
        "section3_mpc.py",
        "section4_fsm.py",
        "section5_6_7.py",
        "test_script_creation.py",
        "test_var_block.py",
        "FB_Automotive_Gigacasting_4500Ton_HPDC_RealTimeShot.st",
        "FB_Electronics_AutomotiveECU_SMT_PickAndPlace_VisionMotion.st",
        "part1.st",
        "part2.st",
        "part3.st"
    ]
    for tf in toolchain_files:
        if os.path.exists(tf):
            run_git(["add", tf])
    run_git(["commit", "-m", "feat(toolchain): update core data evolution tooling, validation scripts, and assembly pipeline [Commit 2/8]"])

    # ----------------------------------------------------
    # COMMIT 3: Active subagent backlog documentation
    # ----------------------------------------------------
    print("\n=== STAGING COMMIT 3 ===")
    run_git(["add", "docs/ACTIVE_SUBAGENTS_BACKLOG.md"])
    run_git(["commit", "-m", "docs(backlog): preserve 8 active industrial subagent specifications for future sessions [Commit 3/8]"])

    # ----------------------------------------------------
    # COMMIT 4: Submodule references and latest agent file
    # ----------------------------------------------------
    print("\n=== STAGING COMMIT 4 ===")
    meta_files = ["data/repos/openplc", "data/repos/tcopen", "latest_agent_file.txt"]
    for mf in meta_files:
        if os.path.exists(mf):
            run_git(["add", mf])
    run_git(["commit", "-m", "chore(metadata): sync repository submodule pointers and agent tracking metadata [Commit 4/8]"])

    # ----------------------------------------------------
    # COMMITS 5-8: Datasets partitioned in 4 balanced batches
    # ----------------------------------------------------
    q1 = raw_datasets[:47]
    q2 = raw_datasets[47:94]
    q3 = raw_datasets[94:141]
    q4 = raw_datasets[141:]

    # COMMIT 5
    print("\n=== STAGING COMMIT 5 ===")
    for f in q1:
        run_git(["add", f])
    run_git(["commit", "-m", "feat(datasets): ingest commercial manufacturing datasets - automotive & heavy mobility [Commit 5/8]"])

    # COMMIT 6
    print("\n=== STAGING COMMIT 6 ===")
    for f in q2:
        run_git(["add", f])
    run_git(["commit", "-m", "feat(datasets): ingest commercial manufacturing datasets - semiconductor & electronics [Commit 6/8]"])

    # COMMIT 7
    print("\n=== STAGING COMMIT 7 ===")
    for f in q3:
        run_git(["add", f])
    run_git(["commit", "-m", "feat(datasets): ingest commercial manufacturing datasets - metallurgy & precision tooling [Commit 7/8]"])

    # COMMIT 8
    print("\n=== STAGING COMMIT 8 ===")
    for f in q4:
        run_git(["add", f])
    run_git(["commit", "-m", "feat(datasets): ingest commercial manufacturing datasets - polymers, plastics & aseptic packaging [Commit 8/8]"])

    print("\n=== ALL 8 COMMITS COMPLETED SUCCESSFULLY! ===")

if __name__ == "__main__":
    main()
