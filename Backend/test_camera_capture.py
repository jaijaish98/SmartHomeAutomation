#!/usr/bin/env python3
"""
Test script to capture and save an image from the camera
"""

import cv2
import sys

def test_camera_capture(camera_index=0):
    """Test capturing from camera and save image"""
    print(f"Opening camera {camera_index}...")
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"❌ Failed to open camera {camera_index}")
        return False
    
    print("✅ Camera opened successfully")
    print("📸 Warming up camera (reading 10 frames)...")
    
    # Read a few frames to let camera adjust
    for i in range(10):
        ret, frame = cap.read()
        if ret:
            print(f"  Frame {i+1}/10 captured: {frame.shape}")
    
    print("\n📸 Capturing final frame...")
    ret, frame = cap.read()
    
    if ret and frame is not None:
        print(f"✅ Frame captured successfully: {frame.shape}")
        
        # Save the frame
        output_path = "test_capture.jpg"
        cv2.imwrite(output_path, frame)
        print(f"💾 Image saved to: {output_path}")
        
        # Test face detection
        print("\n🔍 Testing face detection...")
        try:
            import face_recognition
            
            # Detect faces
            face_locations = face_recognition.face_locations(frame)
            print(f"Found {len(face_locations)} face(s)")
            
            if face_locations:
                for i, (top, right, bottom, left) in enumerate(face_locations):
                    print(f"  Face {i+1}: top={top}, right={right}, bottom={bottom}, left={left}")
                    # Draw rectangle on face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                
                # Save image with face boxes
                output_with_faces = "test_capture_with_faces.jpg"
                cv2.imwrite(output_with_faces, frame)
                print(f"💾 Image with face boxes saved to: {output_with_faces}")
            else:
                print("⚠️  No faces detected in the image")
                print("   Make sure you're in front of the camera with good lighting")
        
        except Exception as e:
            print(f"❌ Face detection error: {e}")
    
    else:
        print("❌ Failed to capture frame")
    
    cap.release()
    print("\n✅ Camera released")
    return ret

if __name__ == "__main__":
    camera_index = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    test_camera_capture(camera_index)

