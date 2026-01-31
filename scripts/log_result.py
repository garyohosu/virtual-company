import json
import sys
import os
from datetime import datetime

def log_result(repo_root, instructions_file, output_file, status, exit_code, duration):
    log_dir = os.path.join(repo_root, "results", "gemini")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, "execution_log.json")
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "instructions_file": instructions_file,
        "output_file": output_file,
        "status": status,
        "exit_code": int(exit_code),
        "duration_seconds": int(duration)
    }
    
    data = []
    if os.path.exists(log_file):
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = []
            
    data.append(entry)
    
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print("Usage: python log_result.py <repo_root> <instr_file> <out_file> <status> <exit_code> <duration>")
        sys.exit(1)
    log_result(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
