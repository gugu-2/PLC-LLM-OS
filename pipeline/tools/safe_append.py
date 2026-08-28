import sys
import json
import os

def append_json_safely(json_string, filepath):
    try:
        # Validate it's a real JSON object first
        data = json.loads(json_string)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Open in append mode with a file lock
        with open(filepath, 'a', encoding='utf-8') as f:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(f, fcntl.LOCK_EX)
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
                fcntl.flock(f, fcntl.LOCK_UN)
                
        print(f"SUCCESS: Safely appended to {filepath}")
    except Exception as e:
        print(f"ERROR appending data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python safe_append.py '<json_string>' '<filepath>'")
        sys.exit(1)
        
    append_json_safely(sys.argv[1], sys.argv[2])
