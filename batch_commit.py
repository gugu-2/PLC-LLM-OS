import subprocess
import math

result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
lines = result.stdout.strip().split('\n')
files = []
for line in lines:
    if line:
        filepath = line[3:]
        if filepath.startswith('"') and filepath.endswith('"'):
            filepath = filepath[1:-1]
        files.append(filepath)

filtered_files = []
for f in files:
    if 'cloned_repos' not in f and 'data/repos/' not in f:
        filtered_files.append(f)

print(f'Total files to process: {len(filtered_files)}')
if len(filtered_files) == 0:
    print("Nothing to commit")
    exit(0)
    
num_chunks = 8
chunk_size = math.ceil(len(filtered_files) / num_chunks)

for i in range(num_chunks):
    start = i * chunk_size
    end = start + chunk_size
    chunk = filtered_files[start:end]
    if not chunk: continue
    
    for f in chunk:
        subprocess.run(['git', 'add', f])
    
    msg = f'feat: Add massive V4 synthetic data and engine updates - Batch {i+1} of 8'
    subprocess.run(['git', 'commit', '-m', msg])
    print(f'Committed batch {i+1}')

print('Pushing to GitHub...')
push_res = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
print(push_res.stdout)
print(push_res.stderr)
