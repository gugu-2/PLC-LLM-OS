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
        "feat(tooling): Add IEC 61131-3 swarm builders, state-space assemblers & validators [Part 1/12]",
        [
            "assemble_and_verify.py",
            "assemble_msfr.py",
            "assemble_st.py",
            "build_biopharma_tff.py",
            "build_dataset_entry.py",
            "build_full_script.py",
            "build_generator.py",
            "dataset_builder.py",
            "dataset_builder_fsm.py",
            "dataset_builder_logic1.py",
            "dataset_builder_logic2.py",
            "dataset_builder_logic3.py",
            "dataset_builder_part3.py",
            "generate_cryo_st.py",
            "generate_fb.py",
            "generate_full_system.py",
            "save_record.py",
            "scratch_builder.py",
            "scratch_build_cryo.py",
            "st_part1_declarations.py",
            "st_part2_logic_core.py",
            "st_part3_logic_mpc_fsm.py",
            "validate_agent.py",
            "validate_and_assemble.py",
            "validate_iec.py",
            "verify_dataset.py",
            "verify_parity.py",
            "verify_record.py",
            "scripts/",
            "msfr_sections/",
            "brain_scratch/",
            "scratch/"
        ]
    ),
    # Commit 2
    (
        "feat(synthetic): Add Cryogenic ASU Argon Purity & Superfluid Helium Transition ST blocks [Part 2/12]",
        [
            "data/swarm_raw/agent_ff3ffc7c.json",
            "data/swarm_raw/agent_3df981b7.json",
            "data/swarm_raw/agent_9e4d6601.json",
            "data/swarm_raw/agent_a9a21ee3.json"
        ]
    ),
    # Commit 3
    (
        "feat(synthetic): Add Quantum Gravity Gradiometer & Gravitational Wave Cryopump ST blocks [Part 3/12]",
        [
            "data/swarm_raw/agent_56be839b.json",
            "data/swarm_raw/agent_6ded3c55.json",
            "data/swarm_raw/agent_ea986904.json",
            "data/swarm_raw/agent_8efa91e3.json"
        ]
    ),
    # Commit 4
    (
        "feat(synthetic): Add SFR Secondary Sodium Loop & MCFR Lead-Bismuth Heat Exchanger ST blocks [Part 4/12]",
        [
            "data/swarm_raw/agent_30747251.json",
            "data/swarm_raw/agent_c11aff78.json",
            "data/swarm_raw/agent_d38d42c6.json",
            "data/swarm_raw/agent_1cee7622.json"
        ]
    ),
    # Commit 5
    (
        "feat(synthetic): Add Tokamak Divertor Plasma & Electric Arc Furnace Foaming Slag ST blocks [Part 5/12]",
        [
            "data/swarm_raw/agent_322bf100.json",
            "data/swarm_raw/agent_daaaecfb.json",
            "data/swarm_raw/agent_1e6e30c1.json"
        ]
    ),
    # Commit 6
    (
        "feat(synthetic): Add Subsea Twin-Screw Multiphase Pump & Hydrothermal Vent Cutter ST blocks [Part 6/12]",
        [
            "data/swarm_raw/agent_00510d8b.json",
            "data/swarm_raw/agent_557030a4.json",
            "data/swarm_raw/agent_153a32b5.json"
        ]
    ),
    # Commit 7
    (
        "feat(synthetic): Add Geothermal ESP Anti-Cavitation & Kalina Cycle Power ST blocks [Part 7/12]",
        [
            "data/swarm_raw/agent_1d114b46.json",
            "data/swarm_raw/agent_8dab41b4.json",
            "data/swarm_raw/agent_0e3b6aa4.json",
            "data/swarm_raw/agent_72350657.json"
        ]
    ),
    # Commit 8
    (
        "feat(synthetic): Add Biopharma Microfluidic LNP & Continuous Lyophilization ST blocks [Part 8/12]",
        [
            "data/swarm_raw/agent_c92e3968.json",
            "data/swarm_raw/agent_cdf3fa22.json",
            "data/swarm_raw/agent_1bf6e13b.json",
            "data/swarm_raw/agent_58f13bb6.json",
            "data/swarm_raw/agent_f2077216.json"
        ]
    ),
    # Commit 9
    (
        "feat(synthetic): Add Green Ammonia Synthesis & Direct Air Capture VTSA ST blocks [Part 9/12]",
        [
            "data/swarm_raw/agent_6b6033eb.json",
            "data/swarm_raw/agent_c318e360.json",
            "data/swarm_raw/agent_762193b0.json",
            "data/swarm_raw/agent_2619c642.json"
        ]
    ),
    # Commit 10
    (
        "feat(synthetic): Add High-Pressure Alkaline Electrolysis & Aviation Cryo-H2 Fuel Cell ST blocks [Part 10/12]",
        [
            "data/swarm_raw/agent_bb917707.json",
            "data/swarm_raw/agent_5026330a.json",
            "data/swarm_raw/agent_fcd0b533.json"
        ]
    ),
    # Commit 11
    (
        "feat(synthetic): Add Multi-Laser PBF & Hybrid DED-CNC Manufacturing ST blocks [Part 11/12]",
        [
            "data/swarm_raw/agent_e2fa40b2.json",
            "data/swarm_raw/agent_33ec9628.json",
            "data/swarm_raw/agent_e217271f.json",
            "data/swarm_raw/agent_aebe4d91.json",
            "data/swarm_raw/agent_742c21f9.json"
        ]
    ),
    # Commit 12
    (
        "feat(synthetic): Add High-Speed Maglev Launcher & Port AGV 4WID Navigation ST blocks [Part 12/12]",
        [
            "data/swarm_raw/agent_176a5ae4.json",
            "data/swarm_raw/agent_8ce43e1a.json",
            "data/swarm_raw/agent_fe440f90.json",
            "data/swarm_raw/agent_5d35d696.json",
            "data/swarm_raw/agent_622fc4c9.json",
            "data/swarm_raw/agent_b46bd182.json",
            "data/swarm_raw/agent_c103ad87.json",
            "data/repos/",
            "lumina/data/"
        ]
    )
]

print("Starting 12-Commit Sequence...")
for idx, (msg, targets) in enumerate(commits, 1):
    print(f"\n==========================================")
    print(f"PROCESSING COMMIT {idx}/12: {msg}")
    print(f"==========================================")
    for t in targets:
        if os.path.exists(t):
            run_cmd(f"git add -A \"{t}\"", check=False)
        else:
            # Handle deleted files
            run_cmd(f"git add -u \"{t}\"", check=False)
    
    # Check if anything staged
    diff_res = run_cmd("git diff --cached --name-only", check=False)
    staged = diff_res.stdout.strip()
    if not staged:
        print(f"Warning: No staged changes for commit {idx}.")
    else:
        print(f"Staged {len(staged.splitlines())} changes.")
    
    # Commit
    commit_res = subprocess.run(["git", "commit", "-m", msg], capture_output=True, text=True)
    print(commit_res.stdout.strip())
    if commit_res.returncode != 0 and "nothing to commit" not in commit_res.stdout:
        print("Commit error:", commit_res.stderr.strip())

print("\nAll 12 commits generated. Checking git log...")
run_cmd("git log -n 14 --oneline")
