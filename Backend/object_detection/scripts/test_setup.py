#!/usr/bin/env python3
"""
Setup Test Script
Verifies that all dependencies and components are properly installed.
"""

import sys
from pathlib import Path


def test_imports():
    """Test if all required packages can be imported."""
    print("\n" + "="*70)
    print("Testing Package Imports")
    print("="*70)
    
    packages = {
        'cv2': 'OpenCV',
        'numpy': 'NumPy',
        'yaml': 'PyYAML',
    }
    
    all_ok = True
    for package, name in packages.items():
        try:
            __import__(package)
            if package == 'cv2':
                import cv2
                version = cv2.__version__
                print(f"   ✅ {name} (version {version})")
            else:
                print(f"   ✅ {name}")
        except ImportError as e:
            print(f"   ❌ {name} - NOT INSTALLED")
            all_ok = False
    
    return all_ok


def test_config():
    """Test if configuration file exists and is valid."""
    print("\n" + "="*70)
    print("Testing Configuration")
    print("="*70)
    
    project_root = Path(__file__).parent.parent
    config_path = project_root / "config" / "config.yaml"
    
    if not config_path.exists():
        print(f"   ❌ Config file not found: {config_path}")
        return False
    
    try:
        import yaml
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        print(f"   ✅ Config file loaded successfully")
        print(f"   📋 Model type: {config['model']['type']}")
        print(f"   📋 Camera index: {config['camera']['index']}")
        return True
    except Exception as e:
        print(f"   ❌ Error loading config: {e}")
        return False


def test_model_files():
    """Test if model files exist."""
    print("\n" + "="*70)
    print("Testing Model Files")
    print("="*70)
    
    project_root = Path(__file__).parent.parent
    
    try:
        import yaml
        config_path = project_root / "config" / "config.yaml"
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        model_type = config['model']['type']
        model_files = config['model_files'][model_type]
        
        print(f"   Checking files for model: {model_type}")
        
        all_exist = True
        for file_type in ['weights', 'config', 'names']:
            file_path = project_root / model_files[file_type]
            if file_path.exists():
                size_mb = file_path.stat().st_size / (1024 * 1024)
                print(f"   ✅ {file_type}: {file_path.name} ({size_mb:.1f} MB)")
            else:
                print(f"   ❌ {file_type}: NOT FOUND - {file_path.name}")
                all_exist = False
        
        if not all_exist:
            print(f"\n   💡 Download model files with:")
            print(f"      python scripts/download_models.py")
        
        return all_exist
        
    except Exception as e:
        print(f"   ❌ Error checking model files: {e}")
        return False


def test_camera():
    """Test camera access."""
    print("\n" + "="*70)
    print("Testing Camera Access")
    print("="*70)
    
    try:
        import cv2
        import platform
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("   ❌ Cannot access camera")
            
            if platform.system() == "Darwin":
                print("\n   💡 macOS Camera Permission Required:")
                print("      1. System Settings → Privacy & Security → Camera")
                print("      2. Enable camera access for Terminal/IDE")
                print("      3. Restart Terminal and try again")
            
            return False
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            print("   ❌ Camera opened but cannot read frames")
            return False
        
        print("   ✅ Camera is accessible")
        print(f"   📐 Frame shape: {frame.shape}")
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing camera: {e}")
        return False


def test_opencv_dnn():
    """Test OpenCV DNN module."""
    print("\n" + "="*70)
    print("Testing OpenCV DNN Module")
    print("="*70)
    
    try:
        import cv2
        
        # Check if DNN module is available
        if not hasattr(cv2, 'dnn'):
            print("   ❌ OpenCV DNN module not available")
            return False
        
        print("   ✅ OpenCV DNN module available")
        
        # Check CUDA support
        if cv2.cuda.getCudaEnabledDeviceCount() > 0:
            print("   ✅ CUDA support available")
            print(f"   🎮 CUDA devices: {cv2.cuda.getCudaEnabledDeviceCount()}")
        else:
            print("   ℹ️  CUDA not available (will use CPU)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing DNN: {e}")
        return False


def main():
    """Run all tests."""
    print("="*70)
    print("Object Detection Setup Test")
    print("="*70)
    
    results = {
        'Imports': test_imports(),
        'Configuration': test_config(),
        'Model Files': test_model_files(),
        'Camera': test_camera(),
        'OpenCV DNN': test_opencv_dnn(),
    }
    
    # Summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("✅ All tests passed! You're ready to run object detection.")
        print("\nNext step:")
        print("   python scripts/detect_objects.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        
        if not results['Model Files']:
            print("\n💡 To download model files:")
            print("   python scripts/download_models.py")
    print("="*70)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

