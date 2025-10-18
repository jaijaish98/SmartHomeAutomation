#!/usr/bin/env python3
"""
Real-time Face Detection using OpenCV
This script captures video from the system's default camera and detects faces in real-time.
"""

import cv2
import sys
import os


class FaceDetector:
    """Face detection class using OpenCV's Haar Cascade classifier."""
    
    def __init__(self, camera_index=0, scale_factor=1.1, min_neighbors=5, min_size=(30, 30)):
        """
        Initialize the face detector.
        
        Args:
            camera_index (int): Camera device index (default: 0 for default camera)
            scale_factor (float): Parameter specifying how much the image size is reduced at each image scale
            min_neighbors (int): Parameter specifying how many neighbors each candidate rectangle should have
            min_size (tuple): Minimum possible object size. Objects smaller than this are ignored
        """
        self.camera_index = camera_index
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.min_size = min_size
        self.video_capture = None
        self.face_cascade = None
        
    def load_cascade_classifier(self):
        """Load the Haar Cascade classifier for face detection."""
        try:
            # Load the pre-trained Haar Cascade classifier for face detection
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            
            if self.face_cascade.empty():
                raise IOError("Failed to load Haar Cascade classifier")
            
            print(f"✓ Haar Cascade classifier loaded successfully from: {cascade_path}")
            return True
        except Exception as e:
            print(f"✗ Error loading Haar Cascade classifier: {e}")
            return False
    
    def initialize_camera(self):
        """Initialize the video capture from the camera."""
        try:
            self.video_capture = cv2.VideoCapture(self.camera_index)
            
            if not self.video_capture.isOpened():
                raise IOError(f"Cannot access camera at index {self.camera_index}")
            
            # Get camera properties
            width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(self.video_capture.get(cv2.CAP_PROP_FPS))
            
            print(f"✓ Camera initialized successfully")
            print(f"  Resolution: {width}x{height}")
            print(f"  FPS: {fps if fps > 0 else 'Unknown'}")
            return True
        except Exception as e:
            print(f"✗ Error initializing camera: {e}")
            print(f"  Make sure your camera is connected and not being used by another application")
            return False
    
    def detect_faces(self, frame):
        """
        Detect faces in the given frame.
        
        Args:
            frame: Input image frame
            
        Returns:
            List of face rectangles (x, y, w, h)
        """
        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=self.scale_factor,
            minNeighbors=self.min_neighbors,
            minSize=self.min_size,
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        return faces
    
    def draw_face_boxes(self, frame, faces):
        """
        Draw bounding boxes around detected faces.
        
        Args:
            frame: Input image frame
            faces: List of face rectangles
            
        Returns:
            Frame with drawn bounding boxes
        """
        for (x, y, w, h) in faces:
            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Add label
            label = "Face"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            label_y = max(y - 10, label_size[1])
            cv2.putText(frame, label, (x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, (0, 255, 0), 1, cv2.LINE_AA)
        
        return frame
    
    def add_info_overlay(self, frame, num_faces, fps=0):
        """
        Add information overlay to the frame.
        
        Args:
            frame: Input image frame
            num_faces: Number of detected faces
            fps: Current frames per second
            
        Returns:
            Frame with information overlay
        """
        # Add face count
        face_text = f"Faces detected: {num_faces}"
        cv2.putText(frame, face_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, (0, 255, 0), 2, cv2.LINE_AA)
        
        # Add FPS if available
        if fps > 0:
            fps_text = f"FPS: {fps:.1f}"
            cv2.putText(frame, fps_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (0, 255, 0), 2, cv2.LINE_AA)
        
        # Add instructions
        instruction_text = "Press 'q' or ESC to exit"
        cv2.putText(frame, instruction_text, (10, frame.shape[0] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        
        return frame
    
    def run(self):
        """Main loop for face detection."""
        # Load cascade classifier
        if not self.load_cascade_classifier():
            return False
        
        # Initialize camera
        if not self.initialize_camera():
            return False
        
        print("\n" + "="*50)
        print("Starting face detection...")
        print("Press 'q' or ESC to exit")
        print("="*50 + "\n")
        
        # Variables for FPS calculation
        fps = 0
        frame_count = 0
        
        try:
            # Create a timer for FPS calculation
            timer = cv2.getTickCount()
            
            while True:
                # Capture frame-by-frame
                ret, frame = self.video_capture.read()
                
                if not ret:
                    print("✗ Error: Failed to capture frame from camera")
                    break
                
                # Detect faces
                faces = self.detect_faces(frame)
                
                # Draw bounding boxes around faces
                frame = self.draw_face_boxes(frame, faces)
                
                # Calculate FPS every 30 frames
                frame_count += 1
                if frame_count >= 30:
                    fps = 30 / ((cv2.getTickCount() - timer) / cv2.getTickFrequency())
                    timer = cv2.getTickCount()
                    frame_count = 0
                
                # Add information overlay
                frame = self.add_info_overlay(frame, len(faces), fps)
                
                # Display the resulting frame
                cv2.imshow('Face Detection - Real-time', frame)
                
                # Check for exit key
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # 'q' or ESC key
                    print("\n✓ Exiting face detection...")
                    break
                    
        except KeyboardInterrupt:
            print("\n✓ Interrupted by user")
        except Exception as e:
            print(f"\n✗ Error during face detection: {e}")
            return False
        finally:
            # Cleanup
            self.cleanup()
        
        return True
    
    def cleanup(self):
        """Release resources."""
        if self.video_capture is not None:
            self.video_capture.release()
        cv2.destroyAllWindows()
        print("✓ Resources released successfully")


def main():
    """Main function to run the face detector."""
    print("="*50)
    print("Real-time Face Detection using OpenCV")
    print("="*50 + "\n")
    
    # Create face detector instance
    detector = FaceDetector(
        camera_index=0,      # Default camera
        scale_factor=1.1,    # Image scale reduction
        min_neighbors=5,     # Minimum neighbors for detection
        min_size=(30, 30)    # Minimum face size
    )
    
    # Run face detection
    success = detector.run()
    
    if success:
        print("\n✓ Face detection completed successfully")
        return 0
    else:
        print("\n✗ Face detection failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

