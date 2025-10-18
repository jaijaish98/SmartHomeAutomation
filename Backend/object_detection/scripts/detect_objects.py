#!/usr/bin/env python3
"""
Real-time Object Detection using YOLO
Main application script for detecting objects from webcam or RTSP camera feed.
"""

import sys
import cv2
import yaml
import time
from pathlib import Path
from datetime import datetime

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# Add device_connectivity to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from detector import ObjectDetector
from visualizer import Visualizer
from device_connectivity.camera import WebcamCamera, TapoRTSPCamera, select_camera_interactive


class ObjectDetectionApp:
    """Main application for real-time object detection."""
    
    def __init__(self, config_path="config/config.yaml"):
        """Initialize the application."""
        self.project_root = Path(__file__).parent.parent
        self.config_path = self.project_root / config_path
        self.config = self.load_config()
        
        self.detector = None
        self.camera = None
        self.visualizer = None
        self.output_dir = self.project_root / "output"
        self.output_dir.mkdir(exist_ok=True)
        
    def load_config(self):
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)

            # Load credentials if using RTSP and URL is empty
            if config.get('camera_source', {}).get('type') == 'rtsp':
                if not config.get('rtsp', {}).get('url'):
                    credentials_path = self.project_root / 'config' / 'credentials.yaml'
                    if credentials_path.exists():
                        with open(credentials_path, 'r') as f:
                            credentials = yaml.safe_load(f)
                            if credentials and 'rtsp' in credentials:
                                config['rtsp']['url'] = credentials['rtsp']['url']
                                print("   ✅ Loaded RTSP credentials from credentials.yaml")
                    else:
                        print(f"   ⚠️  Warning: credentials.yaml not found")
                        print(f"   💡 Copy credentials.yaml.example to credentials.yaml and add your RTSP URL")

            return config
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            sys.exit(1)
    
    def initialize(self):
        """Initialize all components."""
        print("="*70)
        print("YOLO Real-time Object Detection")
        print("="*70)
        
        # Initialize detector
        self.detector = ObjectDetector(self.config)
        
        # Get model file paths
        model_type = self.config['model']['type']
        model_files = self.config['model_files'][model_type]
        
        weights_path = self.project_root / model_files['weights']
        config_path = self.project_root / model_files['config']
        names_path = self.project_root / model_files['names']
        
        # Load model
        if not self.detector.load_model(weights_path, config_path, names_path):
            print("\n❌ Failed to load model")
            print("\n💡 Did you download the model files?")
            print("   Run: python scripts/download_models.py")
            return False
        
        # Initialize camera based on mode
        camera_source_config = self.config.get('camera_source', {})
        camera_mode = camera_source_config.get('mode', 'auto')

        if camera_mode == 'interactive':
            # Interactive camera selection
            print("\n")
            camera, camera_info = select_camera_interactive(self.config)

            if camera is None:
                print("\n❌ No camera selected")
                return False

            self.camera = camera

            # Initialize the selected camera
            if not self.camera.initialize():
                print("\n❌ Failed to initialize camera")
                return False
        else:
            # Auto mode - use configured camera type
            camera_source_type = camera_source_config.get('type', 'webcam')

            if camera_source_type == 'rtsp':
                # Initialize RTSP camera
                rtsp_config = self.config.get('rtsp', {})
                rtsp_url = rtsp_config.get('url', '')

                if not rtsp_url:
                    print("\n❌ RTSP URL not configured")
                    print("   💡 Set rtsp.url in config.yaml or credentials.yaml")
                    return False

                self.camera = TapoRTSPCamera(
                    rtsp_url=rtsp_url,
                    reconnect_attempts=rtsp_config.get('reconnect_attempts', 3),
                    reconnect_delay=rtsp_config.get('reconnect_delay', 2),
                    timeout=rtsp_config.get('timeout', 10),
                    buffer_size=rtsp_config.get('buffer_size', 1)
                )
            else:
                # Initialize webcam
                webcam_config = self.config.get('webcam', {})
                self.camera = WebcamCamera(
                    camera_index=webcam_config.get('index', 0),
                    width=webcam_config.get('width', 0),
                    height=webcam_config.get('height', 0),
                    fps=webcam_config.get('fps', 0)
                )

            if not self.camera.initialize():
                print("\n❌ Failed to initialize camera")
                return False
        
        # Initialize visualizer
        self.visualizer = Visualizer(self.config['display'])
        
        print("\n✅ All components initialized successfully")
        return True
    
    def save_frame(self, frame, detections):
        """Save current frame with detections."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"detection_{timestamp}.jpg"
        filepath = self.output_dir / filename
        
        cv2.imwrite(str(filepath), frame)
        
        # Also save detection info
        info_file = self.output_dir / f"detection_{timestamp}.txt"
        with open(info_file, 'w') as f:
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Total detections: {len(detections)}\n\n")
            for detection in detections:
                class_id, class_name, confidence, x, y, w, h = detection
                f.write(f"{class_name}: {confidence:.2f} at ({x}, {y}, {w}, {h})\n")
        
        print(f"\n📸 Frame saved: {filename}")
        return filepath
    
    def run(self):
        """Main detection loop."""
        if not self.initialize():
            return False
        
        print("\n" + "="*70)
        print("Starting object detection...")
        print("="*70)
        print("\n📹 Controls:")
        print("   • Press 'q' or ESC to exit")
        print("   • Press 's' to save current frame")
        print("   • Press 'i' to show model info")
        print("\n" + "="*70 + "\n")
        
        # FPS calculation variables
        fps = 0
        frame_count = 0
        start_time = time.time()
        
        try:
            while True:
                # Read frame
                ret, frame = self.camera.read_frame()
                
                if not ret:
                    print("❌ Failed to capture frame")
                    break
                
                # Detect objects
                detections = self.detector.detect(frame)
                
                # Draw detections
                frame = self.visualizer.draw_detections(
                    frame,
                    detections,
                    self.detector.get_class_names()
                )
                
                # Calculate FPS
                frame_count += 1
                if frame_count >= 30:
                    end_time = time.time()
                    fps = 30 / (end_time - start_time)
                    start_time = time.time()
                    frame_count = 0
                
                # Draw info overlay
                frame = self.visualizer.draw_info_overlay(frame, detections, fps)
                
                # Display frame
                cv2.imshow('YOLO Object Detection', frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == 27:  # 'q' or ESC
                    print("\n✅ Exiting...")
                    break
                elif key == ord('s'):  # Save frame
                    self.save_frame(frame, detections)
                elif key == ord('i'):  # Show info
                    self.print_model_info()
                    
        except KeyboardInterrupt:
            print("\n✅ Interrupted by user")
        except Exception as e:
            print(f"\n❌ Error during detection: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.cleanup()
        
        return True
    
    def print_model_info(self):
        """Print model information to console."""
        info = self.detector.get_model_info()
        print("\n" + "="*70)
        print("Model Information:")
        print("-"*70)
        for key, value in info.items():
            print(f"   {key}: {value}")
        print("="*70 + "\n")
    
    def cleanup(self):
        """Clean up resources."""
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()
        print("✅ Resources released")


def main():
    """Main entry point."""
    app = ObjectDetectionApp()
    success = app.run()
    
    if success:
        print("\n" + "="*70)
        print("✅ Object detection completed successfully")
        print("="*70)
        return 0
    else:
        print("\n" + "="*70)
        print("❌ Object detection failed")
        print("="*70)
        return 1


if __name__ == "__main__":
    sys.exit(main())

