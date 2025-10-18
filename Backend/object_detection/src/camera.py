"""
Camera Handler Module
Handles camera initialization, frame capture, and camera-related utilities.
"""

import cv2
import platform


class CameraHandler:
    """Manages camera operations and frame capture."""
    
    def __init__(self, camera_index=0, width=0, height=0, fps=0):
        """
        Initialize camera handler.
        
        Args:
            camera_index (int): Camera device index
            width (int): Desired frame width (0 for default)
            height (int): Desired frame height (0 for default)
            fps (int): Desired FPS (0 for default)
        """
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.fps = fps
        self.capture = None
        self.is_initialized = False
        
    def initialize(self):
        """
        Initialize the camera.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"\n🎥 Initializing camera (index: {self.camera_index})...")
            
            self.capture = cv2.VideoCapture(self.camera_index)
            
            if not self.capture.isOpened():
                raise IOError(f"Cannot access camera at index {self.camera_index}")
            
            # Set camera properties if specified
            if self.width > 0:
                self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            if self.height > 0:
                self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            if self.fps > 0:
                self.capture.set(cv2.CAP_PROP_FPS, self.fps)
            
            # Get actual camera properties
            actual_width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            actual_fps = int(self.capture.get(cv2.CAP_PROP_FPS))
            
            print(f"   ✅ Camera initialized successfully")
            print(f"   📐 Resolution: {actual_width}x{actual_height}")
            print(f"   🎬 FPS: {actual_fps if actual_fps > 0 else 'Unknown'}")
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            print(f"   ❌ Error initializing camera: {e}")
            
            if platform.system() == "Darwin":  # macOS
                print(f"\n   💡 macOS Camera Permission Required:")
                print(f"      1. Go to System Settings → Privacy & Security → Camera")
                print(f"      2. Enable camera access for Terminal (or your IDE)")
                print(f"      3. Restart Terminal and try again")
            
            return False
    
    def read_frame(self):
        """
        Read a frame from the camera.

        Returns:
            tuple: (success, frame) where success is bool and frame is numpy array
        """
        if not self.is_initialized or self.capture is None:
            return False, None

        success, frame = self.capture.read()

        # Flip frame horizontally to fix mirroring (makes it look natural like a mirror)
        if success and frame is not None:
            frame = cv2.flip(frame, 1)

        return success, frame
    
    def release(self):
        """Release camera resources."""
        if self.capture is not None:
            self.capture.release()
            self.is_initialized = False
            print("   🎥 Camera released")
    
    def get_properties(self):
        """
        Get current camera properties.
        
        Returns:
            dict: Camera properties
        """
        if not self.is_initialized:
            return {}
        
        return {
            'width': int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': int(self.capture.get(cv2.CAP_PROP_FPS)),
            'brightness': self.capture.get(cv2.CAP_PROP_BRIGHTNESS),
            'contrast': self.capture.get(cv2.CAP_PROP_CONTRAST),
        }
    
    def __enter__(self):
        """Context manager entry."""
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.release()

