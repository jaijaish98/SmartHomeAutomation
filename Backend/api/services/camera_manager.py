"""
Camera Manager Service
Manages camera instances, connections, and streaming
"""

import sys
from pathlib import Path
from typing import Dict, Optional, Any
import threading
import yaml
import cv2

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from device_connectivity.camera import CameraDiscovery
from device_connectivity.camera.webcam import WebcamCamera
from device_connectivity.camera.tapo.rtsp_camera import TapoRTSPCamera
from object_detection.src.detector import ObjectDetector
from object_detection.src.visualizer import Visualizer


class CameraManager:
    """Manages all camera instances and their states"""

    def __init__(self):
        self.available_cameras = []
        self.active_cameras = {}  # {camera_id: camera_instance}
        self.camera_locks = {}    # {camera_id: threading.Lock}
        self.detector = None
        self.visualizer = None
        self.object_detection_enabled = False
        self._discover_cameras()
        self._initialize_object_detection()
    
    def _load_config(self):
        """Load configuration from config.yaml and credentials.yaml"""
        config_dir = Path(__file__).parent.parent.parent / 'object_detection' / 'config'
        config_path = config_dir / 'config.yaml'
        credentials_path = config_dir / 'credentials.yaml'

        config = {}

        # Load main config
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
            except Exception as e:
                print(f"⚠️  Warning: Could not load config: {e}")
                return {}
        else:
            return {}

        # Load credentials and merge if RTSP URL is empty
        if not config.get('rtsp', {}).get('url'):
            if credentials_path.exists():
                try:
                    with open(credentials_path, 'r') as f:
                        credentials = yaml.safe_load(f)
                        if credentials and 'rtsp' in credentials:
                            if 'rtsp' not in config:
                                config['rtsp'] = {}
                            config['rtsp']['url'] = credentials['rtsp']['url']
                            print("   ✅ Loaded RTSP credentials from credentials.yaml")
                except Exception as e:
                    print(f"⚠️  Warning: Could not load credentials: {e}")

        return config

    def _discover_cameras(self):
        """Discover all available cameras"""
        print("🔍 Discovering cameras...")

        # Discover webcams
        webcams = CameraDiscovery.discover_webcams(max_cameras=5)

        # Load config for RTSP cameras
        config = self._load_config()

        # Load RTSP cameras from config
        rtsp_cameras = CameraDiscovery.load_rtsp_cameras(config) if config else []

        # Combine all cameras and assign IDs
        all_cameras = webcams + rtsp_cameras

        # Assign sequential IDs
        for idx, cam in enumerate(all_cameras, start=1):
            cam['id'] = idx
            # Store additional info for RTSP cameras
            if cam['type'] == 'rtsp':
                rtsp_config = config.get('rtsp', {})
                cam['rtsp_url'] = rtsp_config.get('url', '')
                cam['username'] = rtsp_config.get('username')
                cam['password'] = rtsp_config.get('password')

        self.available_cameras = all_cameras

        print(f"✅ Found {len(self.available_cameras)} camera(s)")
        for cam in self.available_cameras:
            print(f"   - {cam['name']} ({cam['type']})")

    def _initialize_object_detection(self):
        """Initialize YOLO object detection"""
        try:
            print("\n🤖 Initializing object detection...")

            # Load config
            config = self._load_config()
            if not config:
                print("   ⚠️  No config found, object detection disabled")
                return

            # Initialize detector
            self.detector = ObjectDetector(config)

            # Load YOLO model
            model_dir = Path(__file__).parent.parent.parent / 'object_detection' / 'models'
            weights_path = model_dir / 'yolov4-tiny.weights'
            config_path = model_dir / 'yolov4-tiny.cfg'
            names_path = model_dir / 'coco.names'

            if self.detector.load_model(str(weights_path), str(config_path), str(names_path)):
                # Initialize visualizer
                display_config = config.get('display', {})
                self.visualizer = Visualizer(display_config)
                self.object_detection_enabled = True
                print("   ✅ Object detection initialized successfully")
            else:
                print("   ⚠️  Failed to load YOLO model, object detection disabled")
                self.detector = None

        except Exception as e:
            print(f"   ⚠️  Error initializing object detection: {e}")
            self.detector = None
            self.visualizer = None
            self.object_detection_enabled = False

    def get_all_cameras(self) -> list:
        """Get list of all available cameras"""
        return self.available_cameras
    
    def get_camera_by_id(self, camera_id: int) -> Optional[Dict[str, Any]]:
        """Get camera info by ID"""
        for camera in self.available_cameras:
            if camera['id'] == camera_id:
                return camera
        return None
    
    def open_camera(self, camera_id: int) -> Dict[str, Any]:
        """Open a camera and start streaming"""
        # Check if camera exists
        camera_info = self.get_camera_by_id(camera_id)
        if not camera_info:
            return {
                'success': False,
                'error': f'Camera {camera_id} not found'
            }
        
        # Check if already open
        if camera_id in self.active_cameras:
            return {
                'success': True,
                'message': 'Camera already open',
                'camera': camera_info
            }
        
        try:
            # Create camera instance based on type
            if camera_info['type'] == 'webcam':
                camera = WebcamCamera(camera_info['index'])
            elif camera_info['type'] == 'rtsp':
                camera = TapoRTSPCamera(camera_info['rtsp_url'])
            else:
                return {
                    'success': False,
                    'error': f'Unknown camera type: {camera_info["type"]}'
                }
            
            # Initialize camera
            if not camera.initialize():
                return {
                    'success': False,
                    'error': 'Failed to initialize camera'
                }
            
            # Store camera instance and lock
            self.active_cameras[camera_id] = camera
            self.camera_locks[camera_id] = threading.Lock()
            
            print(f"✅ Opened camera {camera_id}: {camera_info['name']}")
            
            return {
                'success': True,
                'message': 'Camera opened successfully',
                'camera': camera_info,
                'stream_url': f'/stream/{camera_id}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error opening camera: {str(e)}'
            }
    
    def close_camera(self, camera_id: int) -> Dict[str, Any]:
        """Close a camera and stop streaming"""
        if camera_id not in self.active_cameras:
            return {
                'success': False,
                'error': f'Camera {camera_id} is not open'
            }
        
        try:
            # Get camera instance
            camera = self.active_cameras[camera_id]
            
            # Release camera
            camera.release()
            
            # Remove from active cameras
            del self.active_cameras[camera_id]
            del self.camera_locks[camera_id]
            
            camera_info = self.get_camera_by_id(camera_id)
            print(f"✅ Closed camera {camera_id}: {camera_info['name']}")
            
            return {
                'success': True,
                'message': 'Camera closed successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error closing camera: {str(e)}'
            }
    
    def get_camera_frame(self, camera_id: int):
        """Get current frame from camera with object detection"""
        if camera_id not in self.active_cameras:
            return None

        camera = self.active_cameras[camera_id]
        lock = self.camera_locks[camera_id]

        with lock:
            success, frame = camera.read_frame()
            if success and frame is not None:
                # Apply object detection if enabled
                if self.object_detection_enabled and self.detector and self.visualizer:
                    try:
                        # Detect objects
                        detections = self.detector.detect(frame)

                        # Draw detections on frame
                        if detections:
                            frame = self.visualizer.draw_detections(
                                frame,
                                detections,
                                self.detector.class_names
                            )
                    except Exception as e:
                        # If detection fails, just return original frame
                        print(f"⚠️  Detection error: {e}")
                        pass

                return frame

        return None
    
    def is_camera_active(self, camera_id: int) -> bool:
        """Check if camera is currently active"""
        return camera_id in self.active_cameras
    
    def close_all_cameras(self):
        """Close all active cameras"""
        camera_ids = list(self.active_cameras.keys())
        for camera_id in camera_ids:
            self.close_camera(camera_id)
        print("✅ All cameras closed")

