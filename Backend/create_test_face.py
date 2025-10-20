#!/usr/bin/env python3
"""
Create a simple test face image using OpenCV
This creates a basic face-like pattern for testing
"""

import cv2
import numpy as np

def create_test_face_image(output_path="test_face.jpg"):
    """Create a simple test face image"""
    
    # Create a blank image (480x640, RGB)
    img = np.ones((480, 640, 3), dtype=np.uint8) * 200  # Light gray background
    
    # Draw a face-like pattern
    # Face oval
    cv2.ellipse(img, (320, 240), (120, 160), 0, 0, 360, (220, 180, 150), -1)
    
    # Eyes
    cv2.circle(img, (280, 200), 20, (50, 50, 50), -1)  # Left eye
    cv2.circle(img, (360, 200), 20, (50, 50, 50), -1)  # Right eye
    cv2.circle(img, (280, 200), 8, (255, 255, 255), -1)  # Left eye highlight
    cv2.circle(img, (360, 200), 8, (255, 255, 255), -1)  # Right eye highlight
    
    # Eyebrows
    cv2.ellipse(img, (280, 170), (30, 10), 0, 0, 180, (80, 60, 40), 3)
    cv2.ellipse(img, (360, 170), (30, 10), 0, 0, 180, (80, 60, 40), 3)
    
    # Nose
    pts = np.array([[320, 220], [310, 260], [330, 260]], np.int32)
    cv2.polylines(img, [pts], True, (180, 140, 120), 2)
    
    # Mouth
    cv2.ellipse(img, (320, 300), (40, 20), 0, 0, 180, (150, 80, 80), 3)
    
    # Hair
    cv2.ellipse(img, (320, 140), (130, 80), 0, 0, 180, (60, 40, 20), -1)
    
    # Save the image
    cv2.imwrite(output_path, img)
    print(f"✅ Test face image created: {output_path}")
    print(f"   Image size: {img.shape}")
    
    return output_path

if __name__ == "__main__":
    create_test_face_image()

