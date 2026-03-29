import sys
import os
from pathlib import Path

# 1. I need to make sure 'common' is in the Python path
# I'll add the directory where THIS script lives to sys.path
script_dir = Path(__file__).resolve().parent
sys.path.append(str(script_dir))

try:
    # 2. I'll attempt to import my new path utility
    from common.project_paths import get_project_root
    
    # 3. I'll run my discovery logic
    PROJECT_ROOT = get_project_root()
    
    print("-" * 50)
    print("🏠 MY PROJECT ROOT DISCOVERY")
    print(f"Current File: {__file__}")
    print(f"Identified Root: {PROJECT_ROOT}")
    print("-" * 50)

    # 4. I'll verify my core directories exist
    required_dirs = ["docs/research", "docs/manuals", "common", "bin"]
    print("\n📁 FOLDER VERIFICATION:")
    for d in required_dirs:
        status = "✅ Found" if (PROJECT_ROOT / d).exists() else "❌ Missing"
        print(f" - {d:15} : {status}")

    # 5. I'll check for my sensitive credentials
    env_file = PROJECT_ROOT / ".env"
    print(f"\n🔑 CONFIG CHECK:")
    if env_file.exists():
        print(f" - .env file      : ✅ Detected (Safe in .gitignore)")
    else:
        print(f" - .env file      : ⚠️ Missing! (I should copy .env.example)")

except ImportError as e:
    print(f"❌ ERROR: Could not find my common utilities. {e}")
    print(f"I am currently looking in: {sys.path}")

print("-" * 50)