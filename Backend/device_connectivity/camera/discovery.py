"""
Camera Discovery Utility
Discovers and lists all available cameras on the system.
"""

import cv2
import platform
import subprocess
import re
from typing import List, Dict, Any, Optional


class CameraDiscovery:
    """Utility class for discovering available cameras."""

    @staticmethod
    def _get_macos_camera_names() -> Dict[int, str]:
        """
        Get camera names from macOS system_profiler.

        Returns:
            dict: Mapping of camera index to camera name
        """
        camera_names = {}

        try:
            # Run system_profiler to get camera information
            result = subprocess.run(
                ['system_profiler', 'SPCameraDataType'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                output = result.stdout

                # Parse camera names from output
                # Format: "    Camera Name:\n      Model ID: ..."
                camera_sections = re.split(r'\n\s{4}(?=[A-Z])', output)

                temp_names = []
                for section in camera_sections:
                    # Look for camera name (first line of section)
                    lines = section.strip().split('\n')
                    if lines and ':' in lines[0]:
                        camera_name = lines[0].split(':')[0].strip()

                        # Clean up the name
                        if camera_name and camera_name != 'Camera':
                            temp_names.append(camera_name)

                # IMPORTANT: On macOS, system_profiler returns cameras in different order
                # than OpenCV indices. Testing shows we need to reverse the list.
                # system_profiler: ['FaceTime HD Camera', 'USB Camera']
                # OpenCV actual:   index 0 = USB Camera, index 1 = FaceTime HD Camera
                temp_names.reverse()

                # Map to indices
                for index, name in enumerate(temp_names):
                    camera_names[index] = name

        except Exception as e:
            # If system_profiler fails, return empty dict
            pass

        return camera_names

    @staticmethod
    def _get_camera_name(index: int, system_names: Dict[int, str]) -> str:
        """
        Get camera name for a given index.

        Args:
            index (int): Camera index
            system_names (dict): Mapping of index to system camera names

        Returns:
            str: Camera name
        """
        # Try to get name from system
        if index in system_names:
            return system_names[index]

        # Fallback names
        if index == 0:
            return "Built-in Camera (Default)"
        else:
            return f"External Camera {index}"

    @staticmethod
    def discover_webcams(max_cameras: int = 10) -> List[Dict[str, Any]]:
        """
        Discover all available webcams/USB cameras on the system.

        Args:
            max_cameras (int): Maximum number of camera indices to check

        Returns:
            list: List of dictionaries containing camera information
        """
        available_cameras = []

        print("\n🔍 Scanning for available cameras...")

        # Get camera names from system (macOS only)
        system_names = {}
        if platform.system() == 'Darwin':
            system_names = CameraDiscovery._get_macos_camera_names()

        for index in range(max_cameras):
            try:
                # Try to open camera
                cap = cv2.VideoCapture(index)

                if cap.isOpened():
                    # Try to read a frame to verify camera works
                    ret, frame = cap.read()

                    if ret and frame is not None:
                        # Get camera properties
                        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        fps = int(cap.get(cv2.CAP_PROP_FPS))

                        # Get camera name from system or use fallback
                        camera_name = CameraDiscovery._get_camera_name(index, system_names)

                        camera_info = {
                            'index': index,
                            'name': camera_name,
                            'type': 'webcam',
                            'resolution': f"{width}x{height}",
                            'fps': fps if fps > 0 else 'Unknown',
                            'available': True
                        }

                        available_cameras.append(camera_info)
                        print(f"   ✅ Found: {camera_name} - {width}x{height}")

                    cap.release()

            except Exception:
                # Camera not available or error accessing it
                pass
        
        if not available_cameras:
            print("   ⚠️  No webcams found")
        
        return available_cameras
    
    @staticmethod
    def load_rtsp_cameras(config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Load RTSP camera configurations.

        Args:
            config (dict): Configuration dictionary containing RTSP settings

        Returns:
            list: List of dictionaries containing RTSP camera information
        """
        rtsp_cameras = []

        # Check if RTSP is configured
        rtsp_config = config.get('rtsp', {})
        rtsp_url = rtsp_config.get('url', '')

        if rtsp_url:
            # Use "Tapo Smart Camera" as the name
            camera_name = "Tapo Smart Camera"

            camera_info = {
                'index': -1,  # Special index for RTSP
                'name': camera_name,
                'type': 'rtsp',
                'url': rtsp_url,
                'resolution': 'Variable',
                'fps': 'Variable',
                'available': True
            }

            rtsp_cameras.append(camera_info)
            print(f"   ✅ Found: {camera_name} (RTSP)")

        return rtsp_cameras
    
    @staticmethod
    def discover_all_cameras(config: Dict[str, Any] = None, max_webcams: int = 10) -> List[Dict[str, Any]]:
        """
        Discover all available cameras (webcams and RTSP).
        
        Args:
            config (dict): Configuration dictionary
            max_webcams (int): Maximum number of webcam indices to check
            
        Returns:
            list: List of all available cameras
        """
        all_cameras = []
        
        # Discover webcams
        webcams = CameraDiscovery.discover_webcams(max_webcams)
        all_cameras.extend(webcams)
        
        # Load RTSP cameras if config provided
        if config:
            rtsp_cameras = CameraDiscovery.load_rtsp_cameras(config)
            all_cameras.extend(rtsp_cameras)
        
        return all_cameras
    
    @staticmethod
    def print_camera_list(cameras: List[Dict[str, Any]]) -> None:
        """
        Print a formatted list of cameras.
        
        Args:
            cameras (list): List of camera dictionaries
        """
        if not cameras:
            print("\n❌ No cameras found")
            return
        
        print("\n" + "="*70)
        print("Available Cameras:")
        print("="*70)
        
        for i, camera in enumerate(cameras, 1):
            camera_type = "📹 RTSP" if camera['type'] == 'rtsp' else "🎥 Webcam"
            print(f"\n{i}. {camera_type} - {camera['name']}")
            print(f"   Resolution: {camera['resolution']}")
            print(f"   FPS: {camera['fps']}")
            if camera['type'] == 'webcam':
                print(f"   Device Index: {camera['index']}")
        
        print("\n" + "="*70)
    
    @staticmethod
    def get_camera_info(cameras: List[Dict[str, Any]], selection: int) -> Dict[str, Any]:
        """
        Get camera information by selection number.
        
        Args:
            cameras (list): List of camera dictionaries
            selection (int): Selection number (1-based)
            
        Returns:
            dict: Camera information or None if invalid selection
        """
        if 1 <= selection <= len(cameras):
            return cameras[selection - 1]
        return None


def test_camera_discovery():
    """Test camera discovery functionality."""
    print("\n" + "="*70)
    print("Camera Discovery Test")
    print("="*70)
    
    # Discover webcams
    cameras = CameraDiscovery.discover_webcams(max_cameras=5)
    
    # Print results
    CameraDiscovery.print_camera_list(cameras)
    
    print(f"\n✅ Found {len(cameras)} camera(s)")


if __name__ == "__main__":
    test_camera_discovery()

