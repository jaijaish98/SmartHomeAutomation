"""
Tapo RTSP Camera Handler
Handles connection to TP-Link Tapo IP cameras via RTSP streams.
"""

import cv2
import time
from typing import Tuple, Optional, Dict, Any
import numpy as np
from ..base import CameraSource


class TapoRTSPCamera(CameraSource):
    """Handles Tapo IP camera RTSP stream connection and frame capture."""
    
    def __init__(
        self,
        rtsp_url: str,
        reconnect_attempts: int = 3,
        reconnect_delay: int = 2,
        timeout: int = 10,
        buffer_size: int = 1
    ):
        """
        Initialize Tapo RTSP camera handler.
        
        Args:
            rtsp_url (str): RTSP stream URL (e.g., rtsp://user:pass@ip:port/stream1)
            reconnect_attempts (int): Number of reconnection attempts on failure
            reconnect_delay (int): Delay in seconds between reconnection attempts
            timeout (int): Connection timeout in seconds
            buffer_size (int): Frame buffer size (1 = latest frame only)
        """
        super().__init__()
        self.rtsp_url = rtsp_url
        self.reconnect_attempts = reconnect_attempts
        self.reconnect_delay = reconnect_delay
        self.timeout = timeout
        self.buffer_size = buffer_size
        self.capture = None
        self._last_frame = None
        self._frame_count = 0
        self._connection_errors = 0
        
    def initialize(self) -> bool:
        """
        Initialize the RTSP camera connection.
        
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"\n📹 Initializing Tapo RTSP camera...")
        print(f"   🔗 Connecting to RTSP stream...")
        
        # Extract camera info from URL (without showing credentials)
        try:
            # Parse URL to hide credentials in logs
            url_parts = self.rtsp_url.split('@')
            if len(url_parts) > 1:
                camera_address = url_parts[-1]
                print(f"   📍 Camera address: {camera_address}")
            else:
                print(f"   📍 Camera address: {self.rtsp_url}")
        except Exception:
            pass
        
        # Attempt to connect
        for attempt in range(1, self.reconnect_attempts + 1):
            try:
                print(f"   🔄 Connection attempt {attempt}/{self.reconnect_attempts}...")
                
                # Create VideoCapture with RTSP URL
                self.capture = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
                
                # Set buffer size (smaller = more recent frames, less lag)
                self.capture.set(cv2.CAP_PROP_BUFFERSIZE, self.buffer_size)
                
                # Set timeout
                self.capture.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, self.timeout * 1000)
                self.capture.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, self.timeout * 1000)
                
                # Check if connection is successful
                if not self.capture.isOpened():
                    raise IOError("Failed to open RTSP stream")
                
                # Try to read a test frame
                success, frame = self.capture.read()
                if not success or frame is None:
                    raise IOError("Failed to read frame from RTSP stream")
                
                # Get stream properties
                width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = int(self.capture.get(cv2.CAP_PROP_FPS))
                
                print(f"   ✅ RTSP connection established successfully")
                print(f"   📐 Resolution: {width}x{height}")
                print(f"   🎬 FPS: {fps if fps > 0 else 'Unknown'}")
                
                self.is_initialized = True
                self._connection_errors = 0
                return True
                
            except Exception as e:
                print(f"   ⚠️  Attempt {attempt} failed: {e}")
                
                if self.capture is not None:
                    self.capture.release()
                    self.capture = None
                
                if attempt < self.reconnect_attempts:
                    print(f"   ⏳ Waiting {self.reconnect_delay}s before retry...")
                    time.sleep(self.reconnect_delay)
                else:
                    print(f"   ❌ Failed to connect after {self.reconnect_attempts} attempts")
                    self._print_troubleshooting()
                    return False
        
        return False
    
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Read a frame from the RTSP stream.
        
        Returns:
            tuple: (success, frame) where success is bool and frame is numpy array
        """
        if not self.is_initialized or self.capture is None:
            return False, None
        
        try:
            success, frame = self.capture.read()
            
            if not success or frame is None:
                self._connection_errors += 1
                
                # Attempt reconnection if multiple consecutive errors
                if self._connection_errors >= 5:
                    print(f"\n   ⚠️  Multiple frame read failures detected")
                    print(f"   🔄 Attempting to reconnect...")
                    
                    self.release()
                    if self.initialize():
                        print(f"   ✅ Reconnection successful")
                        return self.capture.read()
                    else:
                        print(f"   ❌ Reconnection failed")
                        return False, None
                
                # Return last known good frame if available
                if self._last_frame is not None:
                    return True, self._last_frame.copy()
                
                return False, None
            
            # Reset error counter on successful read
            self._connection_errors = 0
            self._frame_count += 1

            # Store as last good frame (no flip for RTSP - already correct orientation)
            self._last_frame = frame.copy()

            return True, frame
            
        except Exception as e:
            print(f"   ❌ Error reading frame: {e}")
            self._connection_errors += 1
            
            # Return last known good frame if available
            if self._last_frame is not None:
                return True, self._last_frame.copy()
            
            return False, None
    
    def release(self) -> None:
        """Release RTSP camera resources."""
        if self.capture is not None:
            self.capture.release()
            self.capture = None
            self.is_initialized = False
            print("   📹 RTSP camera connection closed")
    
    def get_properties(self) -> Dict[str, Any]:
        """
        Get RTSP camera properties.
        
        Returns:
            dict: Camera properties
        """
        if not self.is_initialized or self.capture is None:
            return {}
        
        return {
            'width': int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': int(self.capture.get(cv2.CAP_PROP_FPS)),
            'frame_count': self._frame_count,
            'connection_errors': self._connection_errors,
            'backend': 'FFMPEG',
            'source_type': 'RTSP',
        }
    
    def _print_troubleshooting(self) -> None:
        """Print troubleshooting tips for RTSP connection issues."""
        print(f"\n   💡 Troubleshooting Tips:")
        print(f"      1. Verify camera is powered on and connected to network")
        print(f"      2. Check RTSP URL format: rtsp://username:password@ip:port/stream")
        print(f"      3. Verify credentials (username and password)")
        print(f"      4. Ensure camera IP address is correct and reachable")
        print(f"      5. Check if RTSP is enabled in camera settings")
        print(f"      6. Verify port (usually 554 for RTSP)")
        print(f"      7. Check firewall settings")
        print(f"      8. Try pinging the camera: ping <camera_ip>")
        print(f"      9. Test RTSP URL with VLC: Media → Open Network Stream")

