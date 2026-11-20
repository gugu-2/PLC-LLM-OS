import subprocess
import sys
import os

def run_git(args):
    print(f">> git {' '.join(args)}")
    res = subprocess.run(['git'] + args, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error: {res.stderr}")
        sys.exit(1)
    if res.stdout.strip():
        print(res.stdout.strip())
    return res.stdout.strip()

# Check starting status
status = run_git(['status', '--porcelain'])
print(f"Initial dirty paths count: {len(status.splitlines())}")

# Commit 1: Tooling and scripts
commit1_files = [
    'build_dataset.py',
    'build_full_agent.py',
    'build_full_code.py',
    'build_full_dataset.py',
    'build_iec_mill.py',
    'build_massive_dataset.py',
    'builder.py',
    'builder_can_seamer.py',
    'builder_ev_dispense.py',
    'execute_9_commits.py',
    'gen_part1.py',
    'gen_part2.py',
    'gen_part3.py',
    'gen_part4.py',
    'gen_part5.py',
    'gen_part6.py',
    'gen_part7.py',
    'gen_part8.py',
    'gen_phase1.py',
    'gen_phase2.py',
    'gen_phase5.py',
    'gen_phase6.py',
    'generate_bonder.py',
    'generate_code.py',
    'generate_dataset.py',
    'generate_fuel_tank_dataset.py',
    'generate_full_bonder.py',
    'generate_full_dataset.py',
    'generate_massive_dataset.py',
    'last_validated_agent.txt',
    'make_builder.py',
    'make_code.py',
    'package_and_validate.py',
    'part1.st',
    'part2.st',
    'part3.st',
    'part4.st',
    'part5.st',
    'part6.st',
    'part7.st',
    'scratch/build_hairpin.py',
    'scratch/gen_st_parts.py',
    'scratch/generate_dataset.py',
    'scratch_builder.py',
    'scripts/generate_gear_grinding.py'
]

print("\n--- Executing Commit 1/9 ---")
for f in commit1_files:
    if os.path.exists(f):
        run_git(['add', f])
    else:
        # File might be deleted
        run_git(['rm', '--ignore-unmatch', f])

run_git(['commit', '-m', 'chore(tools): add modular synthesis builders, parity validation tooling and clean obsolete scripts [Commit 1/9]'])

# Commit 2: Backlog documentation
print("\n--- Executing Commit 2/9 ---")
run_git(['add', 'docs/ACTIVE_SUBAGENTS_BACKLOG.md'])
run_git(['commit', '-m', 'docs(fleet): update active subagent backlog and sync cumulative 870 datasets [Commit 2/9]'])

# Commit 3: Automotive Powertrain & Chassis
commit3_datasets = [
    'data/swarm_raw/agent_18c9a3b4.json',
    'data/swarm_raw/agent_20986c69.json',
    'data/swarm_raw/agent_29f81a4d.json',
    'data/swarm_raw/agent_31fa9c04.json',
    'data/swarm_raw/agent_5b8dc74d.json',
    'data/swarm_raw/agent_81c6bf04.json',
    'data/swarm_raw/agent_ddc093c2.json'
]
print(f"\n--- Executing Commit 3/9 ({len(commit3_datasets)} files) ---")
for f in commit3_datasets:
    run_git(['add', f])
run_git(['commit', '-m', 'feat(datasets): ingest commercial manufacturing datasets - automotive powertrain, chassis & dyno testing [Commit 3/9]'])

# Commit 4: Automotive EV Battery, BIW & Paint
commit4_datasets = [
    'data/swarm_raw/agent_1f489b2c.json',
    'data/swarm_raw/agent_41d8e20b.json',
    'data/swarm_raw/agent_71a82b3d.json',
    'data/swarm_raw/agent_74b62d3a.json',
    'data/swarm_raw/agent_75599a7a.json',
    'data/swarm_raw/agent_75b91ca3.json',
    'data/swarm_raw/agent_7c81a29d.json',
    'data/swarm_raw/agent_82d19ca5.json',
    'data/swarm_raw/agent_906a7734.json',
    'data/swarm_raw/agent_aeabef2a.json',
    'data/swarm_raw/agent_dbfcd869.json'
]
print(f"\n--- Executing Commit 4/9 ({len(commit4_datasets)} files) ---")
for f in commit4_datasets:
    run_git(['add', f])
run_git(['commit', '-m', 'feat(datasets): ingest commercial manufacturing datasets - automotive EV battery, BIW & paint systems [Commit 4/9]'])

# Commit 5: Electronics SMT & Inspection
commit5_datasets = [
    'data/swarm_raw/agent_02b4d411.json',
    'data/swarm_raw/agent_15ae720d.json',
    'data/swarm_raw/agent_52d9a10c.json',
    'data/swarm_raw/agent_82223f85.json',
    'data/swarm_raw/agent_93b71ca2.json'
]
print(f"\n--- Executing Commit 5/9 ({len(commit5_datasets)} files) ---")
for f in commit5_datasets:
    run_git(['add', f])
run_git(['commit', '-m', 'feat(datasets): ingest commercial manufacturing datasets - electronics assembly, SMT & 3D inspection [Commit 5/9]'])

# Commit 6: Semiconductor & Power Modules
commit6_datasets = [
    'data/swarm_raw/agent_05bc92ba.json',
    'data/swarm_raw/agent_19c84e1b.json',
    'data/swarm_raw/agent_27ab42c4.json',
    'data/swarm_raw/agent_61d9a20b.json',
    'data/swarm_raw/agent_74b12df8.json',
    'data/swarm_raw/agent_88b17ce2.json',
    'data/swarm_raw/agent_c836f42a.json'
]
print(f"\n--- Executing Commit 6/9 ({len(commit6_datasets)} files) ---")
for f in commit6_datasets:
    run_git(['add', f])
run_git(['commit', '-m', 'feat(datasets): ingest commercial manufacturing datasets - semiconductor wafer fab & power packaging [Commit 6/9]'])

# Commit 7: Metallurgy & Continuous Rolling
commit7_datasets = [
    'data/swarm_raw/agent_1129ef79.json',
    'data/swarm_raw/agent_64ca39b8.json',
    'data/swarm_raw/agent_8a391cb4.json',
    'data/swarm_raw/agent_cdc2db65.json'
]
print(f"\n--- Executing Commit 7/9 ({len(commit7_datasets)} files) ---")
for f in commit7_datasets:
    run_git(['add', f])
run_git(['commit', '-m', 'feat(datasets): ingest commercial manufacturing datasets - metallurgy, continuous casting & cold/hot strip mills [Commit 7/9]'])

# Commit 8: Heavy Machinery, Forging & CNC
commit8_datasets = [
    'data/swarm_raw/agent_3a719ce2.json',
    'data/swarm_raw/agent_3a812df0.json',
    'data/swarm_raw/agent_42b81ce9.json',
    'data/swarm_raw/agent_53a91cb4.json',
    'data/swarm_raw/agent_68d19ce2.json',
    'data/swarm_raw/agent_6c18f3a2.json',
    'data/swarm_raw/agent_9e1b0d57.json',
    'data/swarm_raw/agent_d7730511.json',
    'data/swarm_raw/agent_ee3c325b.json'
]
print(f"\n--- Executing Commit 8/9 ({len(commit8_datasets)} files) ---")
for f in commit8_datasets:
    run_git(['add', f])
run_git(['commit', '-m', 'feat(datasets): ingest commercial manufacturing datasets - heavy hydraulic/servo presses, forging & CNC machining [Commit 8/9]'])

# Commit 9: Plastics & Food/Beverage Packaging
commit9_datasets = [
    'data/swarm_raw/agent_16c80f6f.json',
    'data/swarm_raw/agent_2b984fa1.json',
    'data/swarm_raw/agent_2f409da1.json',
    'data/swarm_raw/agent_33e19cb4.json',
    'data/swarm_raw/agent_45a19cb2.json',
    'data/swarm_raw/agent_4da82d22.json',
    'data/swarm_raw/agent_4e29ba17.json',
    'data/swarm_raw/agent_4e891b2c.json',
    'data/swarm_raw/agent_50b1b638.json',
    'data/swarm_raw/agent_51c08e7a.json',
    'data/swarm_raw/agent_58b29ca1.json',
    'data/swarm_raw/agent_6d92a10e.json',
    'data/swarm_raw/agent_79d11a84.json',
    'data/swarm_raw/agent_7a391e4d.json',
    'data/swarm_raw/agent_84f12de9.json',
    'data/swarm_raw/agent_9753f0d2.json',
    'data/swarm_raw/agent_9b5821ea.json',
    'data/swarm_raw/agent_b9f27c10.json',
    'data/swarm_raw/agent_c22c5f4d.json',
    'data/swarm_raw/agent_c70cf145.json'
]
print(f"\n--- Executing Commit 9/9 ({len(commit9_datasets)} files) ---")
for f in commit9_datasets:
    run_git(['add', f])
run_git(['commit', '-m', 'feat(datasets): ingest commercial manufacturing datasets - plastics extrusion, blow molding & food/beverage packaging [Commit 9/9]'])

print("\n--- Final Status Check ---")
final_status = run_git(['status', '--porcelain'])
if not final_status:
    print("WORKING DIRECTORY IS 100% CLEAN! ALL 9 COMMITS CREATED SUCCESSFULLY!")
else:
    print(f"Warning: Untracked/modified files remaining:\n{final_status}")
