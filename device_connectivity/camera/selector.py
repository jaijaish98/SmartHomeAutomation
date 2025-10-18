"""
Camera Selection Menu
Interactive menu for selecting camera source.
"""

import sys
from typing import Dict, Any, Optional, Tuple
from .discovery import CameraDiscovery
from .webcam import WebcamCamera
from .tapo import TapoRTSPCamera


class CameraSelector:
    """Interactive camera selection menu."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize camera selector.
        
        Args:
            config (dict): Configuration dictionary
        """
        self.config = config
        self.available_cameras = []
        
    def discover_cameras(self) -> None:
        """Discover all available cameras."""
        print("\n" + "="*70)
        print("🎥 Camera Discovery")
        print("="*70)
        
        self.available_cameras = CameraDiscovery.discover_all_cameras(
            config=self.config,
            max_webcams=10
        )
        
        if not self.available_cameras:
            print("\n❌ No cameras found!")
            print("\n💡 Troubleshooting:")
            print("   • Ensure cameras are connected")
            print("   • Check camera permissions (macOS: System Settings → Privacy → Camera)")
            print("   • Configure RTSP camera in config/credentials.yaml")
            sys.exit(1)
    
    def display_menu(self) -> None:
        """Display camera selection menu."""
        print("\n" + "="*70)
        print("📹 Available Cameras")
        print("="*70)
        
        for i, camera in enumerate(self.available_cameras, 1):
            camera_type = "📹 RTSP" if camera['type'] == 'rtsp' else "🎥 Webcam"
            print(f"\n{i}. {camera_type} - {camera['name']}")
            print(f"   Resolution: {camera['resolution']}")
            print(f"   FPS: {camera['fps']}")
            if camera['type'] == 'webcam':
                print(f"   Device Index: {camera['index']}")
        
        print("\n" + "="*70)
    
    def get_user_selection(self) -> Optional[Dict[str, Any]]:
        """
        Get user's camera selection.
        
        Returns:
            dict: Selected camera information or None if cancelled
        """
        while True:
            try:
                print(f"\n📌 Select a camera (1-{len(self.available_cameras)}) or 'q' to quit: ", end='')
                user_input = input().strip()
                
                if user_input.lower() == 'q':
                    print("\n✅ Cancelled by user")
                    return None
                
                selection = int(user_input)
                
                if 1 <= selection <= len(self.available_cameras):
                    selected_camera = self.available_cameras[selection - 1]
                    print(f"\n✅ Selected: {selected_camera['name']}")
                    return selected_camera
                else:
                    print(f"❌ Invalid selection. Please enter a number between 1 and {len(self.available_cameras)}")
                    
            except ValueError:
                print("❌ Invalid input. Please enter a number or 'q' to quit")
            except KeyboardInterrupt:
                print("\n\n✅ Cancelled by user")
                return None
    
    def create_camera_instance(self, camera_info: Dict[str, Any]):
        """
        Create camera instance based on selection.
        
        Args:
            camera_info (dict): Camera information dictionary
            
        Returns:
            CameraSource: Camera instance (WebcamCamera or TapoRTSPCamera)
        """
        if camera_info['type'] == 'rtsp':
            # Create RTSP camera
            rtsp_config = self.config.get('rtsp', {})
            return TapoRTSPCamera(
                rtsp_url=camera_info['url'],
                reconnect_attempts=rtsp_config.get('reconnect_attempts', 3),
                reconnect_delay=rtsp_config.get('reconnect_delay', 2),
                timeout=rtsp_config.get('timeout', 10),
                buffer_size=rtsp_config.get('buffer_size', 1)
            )
        else:
            # Create webcam camera
            webcam_config = self.config.get('webcam', {})
            return WebcamCamera(
                camera_index=camera_info['index'],
                width=webcam_config.get('width', 0),
                height=webcam_config.get('height', 0),
                fps=webcam_config.get('fps', 0)
            )
    
    def select_camera(self) -> Optional[Tuple[Any, Dict[str, Any]]]:
        """
        Run interactive camera selection.
        
        Returns:
            tuple: (camera_instance, camera_info) or (None, None) if cancelled
        """
        # Discover cameras
        self.discover_cameras()
        
        # Display menu
        self.display_menu()
        
        # Get user selection
        camera_info = self.get_user_selection()
        
        if camera_info is None:
            return None, None
        
        # Create camera instance
        camera_instance = self.create_camera_instance(camera_info)
        
        return camera_instance, camera_info


def select_camera_interactive(config: Dict[str, Any]) -> Optional[Tuple[Any, Dict[str, Any]]]:
    """
    Interactive camera selection helper function.
    
    Args:
        config (dict): Configuration dictionary
        
    Returns:
        tuple: (camera_instance, camera_info) or (None, None) if cancelled
    """
    selector = CameraSelector(config)
    return selector.select_camera()


if __name__ == "__main__":
    # Test camera selector
    import yaml
    from pathlib import Path
    
    # Load config
    config_path = Path(__file__).parent.parent.parent / 'object_detection' / 'config' / 'config.yaml'
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Try to load credentials
        credentials_path = config_path.parent / 'credentials.yaml'
        if credentials_path.exists():
            with open(credentials_path, 'r') as f:
                credentials = yaml.safe_load(f)
                if credentials and 'rtsp' in credentials:
                    config['rtsp']['url'] = credentials['rtsp']['url']
        
        # Run selector
        camera, info = select_camera_interactive(config)
        
        if camera:
            print(f"\n✅ Camera selected: {info['name']}")
        else:
            print("\n❌ No camera selected")
            
    except Exception as e:
        print(f"❌ Error: {e}")

