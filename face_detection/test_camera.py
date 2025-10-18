#!/usr/bin/env python3
"""
Camera Test Script
Quick diagnostic tool to check camera accessibility and permissions.
"""

import cv2
import sys
import platform


def test_camera_access(camera_index=0):
    """Test if camera is accessible."""
    print("="*60)
    print("Camera Access Test")
    print("="*60)
    print(f"\nSystem: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"OpenCV: {cv2.__version__}")
    print(f"\nTesting camera at index {camera_index}...")
    print("-"*60)
    
    try:
        # Try to open camera
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print("❌ FAILED: Cannot open camera")
            print("\n🔍 Possible reasons:")
            
            if platform.system() == "Darwin":  # macOS
                print("   • Camera permission not granted (most common on macOS)")
                print("   • Go to: System Settings → Privacy & Security → Camera")
                print("   • Enable camera access for Terminal or your IDE")
                print("   • Restart your terminal/IDE after granting permission")
            
            print("   • Camera is being used by another application")
            print("   • Camera is not connected or not working")
            print("   • Wrong camera index (try 0, 1, 2, etc.)")
            return False
        
        # Try to read a frame
        ret, frame = cap.read()
        
        if not ret:
            print("❌ FAILED: Camera opened but cannot read frames")
            cap.release()
            return False
        
        # Get camera properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        print("✅ SUCCESS: Camera is accessible!")
        print(f"\n📹 Camera Properties:")
        print(f"   • Resolution: {width}x{height}")
        print(f"   • FPS: {fps if fps > 0 else 'Unknown'}")
        print(f"   • Frame shape: {frame.shape}")
        
        # Test display
        print(f"\n🖼️  Testing display window...")
        cv2.imshow('Camera Test - Press any key to close', frame)
        print("   • A window should appear with your camera feed")
        print("   • Press any key in the window to close it")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        cap.release()
        
        print("\n✅ All tests passed! Your camera is working correctly.")
        print("   You can now run face_detector.py")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    """Main function."""
    success = test_camera_access(camera_index=0)
    
    print("\n" + "="*60)
    if success:
        print("✅ Camera test completed successfully")
        print("\nNext step: Run the face detector")
        print("   python face_detector.py")
    else:
        print("❌ Camera test failed")
        print("\nPlease fix the camera access issue before running face_detector.py")
    print("="*60)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

