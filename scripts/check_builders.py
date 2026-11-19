import os
import glob

print("Checking builder directories:")
for d in sorted(glob.glob("*_builder")):
    files = os.listdir(d)
    py_files = [f for f in files if f.endswith(".py")]
    json_files = [f for f in files if f.endswith(".json")]
    total_size = sum(os.path.getsize(os.path.join(d, f)) for f in files if os.path.isfile(os.path.join(d, f)))
    print(f"  {d:<30}: {len(py_files)} py files, {len(json_files)} json files, total size={total_size:,} bytes")
    for f in sorted(files):
        p = os.path.join(d, f)
        if os.path.isfile(p):
            print(f"    - {f:<30} ({os.path.getsize(p):,} bytes)")

print("\nChecking latest files in data/swarm_raw:")
raw_files = sorted(glob.glob("data/swarm_raw/*.json"), key=os.path.getmtime, reverse=True)
for f in raw_files[:10]:
    mtime = os.path.getmtime(f)
    print(f"  {f} ({os.path.getsize(f):,} bytes, mtime={mtime})")
