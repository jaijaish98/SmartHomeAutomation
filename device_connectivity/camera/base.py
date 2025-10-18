"""
Base Camera Source Interface
Abstract base class for all camera sources (webcam, RTSP, etc.)
"""

from abc import ABC, abstractmethod
from typing import Tuple, Optional, Dict, Any
import numpy as np


class CameraSource(ABC):
    """Abstract base class for camera sources."""
    
    def __init__(self):
        """Initialize camera source."""
        self.is_initialized = False
        self._properties = {}
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the camera source.
        
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Read a frame from the camera source.
        
        Returns:
            tuple: (success, frame) where success is bool and frame is numpy array
        """
        pass
    
    @abstractmethod
    def release(self) -> None:
        """Release camera resources."""
        pass
    
    @abstractmethod
    def get_properties(self) -> Dict[str, Any]:
        """
        Get camera properties.
        
        Returns:
            dict: Camera properties (width, height, fps, etc.)
        """
        pass
    
    def is_ready(self) -> bool:
        """
        Check if camera is ready to capture frames.
        
        Returns:
            bool: True if ready, False otherwise
        """
        return self.is_initialized
    
    def __enter__(self):
        """Context manager entry."""
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.release()

