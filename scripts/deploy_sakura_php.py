import os
import subprocess
import sys
from pathlib import Path

# Configuration
REMOTE_HOST = "garyo@garyo.sakura.ne.jp"
REMOTE_DIR = "www/magicboxai"
LOCAL_PHP_DIR = Path(__file__).parent.parent / "magicboxai" / "php"

def run_command(cmd_list):
    print(f"Executing: {' '.join(str(c) for c in cmd_list)}")
    result = subprocess.run(cmd_list, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    if result.stdout:
        print(result.stdout)
    return True

def deploy():
    if not LOCAL_PHP_DIR.exists():
        print(f"Error: Local PHP directory {LOCAL_PHP_DIR} not found.")
        sys.exit(1)

    print(f"🚀 Deploying MagicBoxAI PHP to {REMOTE_HOST}:{REMOTE_DIR}...")

    # Upload files
    # index.php
    run_command(["scp", str(LOCAL_PHP_DIR / "index.php"), f"{REMOTE_HOST}:{REMOTE_DIR}/index.php"])
    # cron_cleanup.php
    run_command(["scp", str(LOCAL_PHP_DIR / "cron_cleanup.php"), f"{REMOTE_HOST}:{REMOTE_DIR}/cron_cleanup.php"])
    # .htaccess
    run_command(["scp", str(LOCAL_PHP_DIR / ".htaccess"), f"{REMOTE_HOST}:{REMOTE_DIR}/.htaccess"])
    # pages/home.php
    run_command(["scp", str(LOCAL_PHP_DIR / "pages" / "home.php"), f"{REMOTE_HOST}:{REMOTE_DIR}/pages/home.php"])

    # Ensure permissions
    remote_chmod = f"chmod 644 {REMOTE_DIR}/index.php {REMOTE_DIR}/cron_cleanup.php {REMOTE_DIR}/.htaccess {REMOTE_DIR}/pages/home.php"
    run_command(["ssh", REMOTE_HOST, remote_chmod])
    
    print("✅ Deployment complete.")

if __name__ == "__main__":
    deploy()
