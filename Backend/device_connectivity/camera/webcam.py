"""
Webcam Camera Handler
Handles connection to local webcams/USB cameras.
"""

import cv2
import platform
from typing import Tuple, Optional, Dict, Any
import numpy as np
from .base import CameraSource


class WebcamCamera(CameraSource):
    """Handles local webcam/USB camera connection and frame capture."""
    
    def __init__(
        self,
        camera_index: int = 0,
        width: int = 0,
        height: int = 0,
        fps: int = 0
    ):
        """
        Initialize webcam camera handler.
        
        Args:
            camera_index (int): Camera device index (0 for default camera)
            width (int): Desired frame width (0 for default)
            height (int): Desired frame height (0 for default)
            fps (int): Desired FPS (0 for default)
        """
        super().__init__()
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.fps = fps
        self.capture = None
        
    def initialize(self) -> bool:
        """
        Initialize the webcam.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"\n🎥 Initializing webcam (index: {self.camera_index})...")
            
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
            
            print(f"   ✅ Webcam initialized successfully")
            print(f"   📐 Resolution: {actual_width}x{actual_height}")
            print(f"   🎬 FPS: {actual_fps if actual_fps > 0 else 'Unknown'}")
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            print(f"   ❌ Error initializing webcam: {e}")
            
            if platform.system() == "Darwin":  # macOS
                print(f"\n   💡 macOS Camera Permission Required:")
                print(f"      1. Go to System Settings → Privacy & Security → Camera")
                print(f"      2. Enable camera access for Terminal (or your IDE)")
                print(f"      3. Restart Terminal and try again")
            
            return False
    
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Read a frame from the webcam.
        
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
    
    def release(self) -> None:
        """Release webcam resources."""
        if self.capture is not None:
            self.capture.release()
            self.is_initialized = False
            print("   🎥 Webcam released")
    
    def get_properties(self) -> Dict[str, Any]:
        """
        Get webcam properties.
        
        Returns:
            dict: Camera properties
        """
        if not self.is_initialized or self.capture is None:
            return {}
        
        return {
            'width': int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': int(self.capture.get(cv2.CAP_PROP_FPS)),
            'brightness': self.capture.get(cv2.CAP_PROP_BRIGHTNESS),
            'contrast': self.capture.get(cv2.CAP_PROP_CONTRAST),
            'source_type': 'Webcam',
        }

