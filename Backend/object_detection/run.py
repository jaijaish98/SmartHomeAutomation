#!/usr/bin/env python3
"""
One-Click YOLO Object Detection Launcher
Cross-platform launcher that handles everything automatically!
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(text)
    print("="*70 + "\n")


def print_step(emoji, text):
    """Print a step with emoji."""
    print(f"{emoji} {text}")


def run_command(cmd, cwd=None, capture=False):
    """Run a command and return success status."""
    try:
        if capture:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True
            )
            return result.returncode == 0, result.stdout
        else:
            result = subprocess.run(cmd, shell=True, cwd=cwd)
            return result.returncode == 0, None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, None


def main():
    """Main launcher function."""
    os.system('clear' if os.name != 'nt' else 'cls')
    
    print_header("🚀 YOLO Object Detection - One-Click Launcher")
    
    # Get script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Step 1: Check Python
    print_step("🔍", "Checking Python...")
    python_version = sys.version.split()[0]
    print(f"   ✅ Python {python_version}")
    print()
    
    # Step 2: Install dependencies
    print_step("📦", "Checking dependencies...")
    success, _ = run_command(
        f"{sys.executable} -m pip install -q -r requirements.txt",
        capture=True
    )
    if success:
        print("   ✅ Dependencies ready")
    else:
        print("   ⚠️  Some dependencies may need updating")
    print()
    
    # Step 3: Check model files
    model_path = script_dir / "models" / "yolov4-tiny.weights"
    
    if not model_path.exists():
        print_step("📥", "Downloading YOLO model (first time only, ~23 MB)...")
        success, _ = run_command(f"{sys.executable} scripts/download_models.py")
        if not success:
            print("\n❌ Failed to download model")
            return 1
        print()
    else:
        print_step("✅", "Model already downloaded")
        print()
    
    # Step 4: Run object detection
    print_header("🎬 Launching Object Detection...")
    
    print("📹 Controls:")
    print("   • Press 'q' or ESC to exit")
    print("   • Press 's' to save frame")
    print("   • Press 'i' to show model info")
    print("\n" + "="*70 + "\n")
    
    # Launch detector
    success, _ = run_command(f"{sys.executable} scripts/detect_objects.py")
    
    # Cleanup
    print_header("👋 Object detection stopped")
    
    return 0 if success else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("👋 Interrupted by user")
        print("="*70)
        sys.exit(0)

