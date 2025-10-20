"""
Face encoding module using face_recognition library.
Generates 128-dimensional face encodings from images.
"""

import face_recognition
import numpy as np
import cv2
from typing import List, Tuple, Optional
from pathlib import Path


class FaceEncoder:
    """Handles face detection and encoding generation"""
    
    def __init__(self, model: str = 'hog'):
        """
        Initialize face encoder.
        
        Args:
            model: Face detection model - 'hog' (faster, CPU) or 'cnn' (more accurate, GPU)
        """
        self.model = model
        print(f"🔍 Face encoder initialized with {model.upper()} model")
    
    def encode_face_from_file(self, image_path: str) -> Tuple[Optional[np.ndarray], Optional[Tuple]]:
        """
        Generate face encoding from an image file.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Tuple of (encoding, face_location) or (None, None) if no face found
        """
        try:
            # Load image
            image = face_recognition.load_image_file(image_path)
            
            # Detect faces
            face_locations = face_recognition.face_locations(image, model=self.model)
            
            if len(face_locations) == 0:
                print(f"⚠️  No face detected in {image_path}")
                return None, None
            
            if len(face_locations) > 1:
                print(f"⚠️  Multiple faces detected in {image_path}, using the first one")
            
            # Generate encoding for the first face
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            if len(face_encodings) == 0:
                print(f"⚠️  Could not generate encoding for {image_path}")
                return None, None
            
            return face_encodings[0], face_locations[0]
            
        except Exception as e:
            print(f"❌ Error encoding face from {image_path}: {e}")
            return None, None
    
    def encode_face_from_frame(self, frame: np.ndarray) -> Tuple[Optional[np.ndarray], Optional[Tuple]]:
        """
        Generate face encoding from a video frame.
        
        Args:
            frame: Video frame (BGR format from OpenCV)
            
        Returns:
            Tuple of (encoding, face_location) or (None, None) if no face found
        """
        try:
            # Convert BGR to RGB (face_recognition uses RGB)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect faces
            face_locations = face_recognition.face_locations(rgb_frame, model=self.model)
            
            if len(face_locations) == 0:
                print("⚠️  No face detected in frame")
                return None, None
            
            if len(face_locations) > 1:
                print(f"⚠️  Multiple faces detected in frame, using the first one")
            
            # Generate encoding for the first face
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            if len(face_encodings) == 0:
                print("⚠️  Could not generate encoding from frame")
                return None, None
            
            return face_encodings[0], face_locations[0]
            
        except Exception as e:
            print(f"❌ Error encoding face from frame: {e}")
            return None, None
    
    def detect_faces_in_frame(self, frame: np.ndarray) -> List[Tuple[np.ndarray, Tuple]]:
        """
        Detect all faces in a frame and generate encodings.
        
        Args:
            frame: Video frame (BGR format from OpenCV)
            
        Returns:
            List of tuples (encoding, face_location) for each detected face
        """
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect faces
            face_locations = face_recognition.face_locations(rgb_frame, model=self.model)
            
            if len(face_locations) == 0:
                return []
            
            # Generate encodings for all faces
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            # Combine encodings with locations
            results = list(zip(face_encodings, face_locations))
            
            return results
            
        except Exception as e:
            print(f"❌ Error detecting faces in frame: {e}")
            return []
    
    def get_face_landmarks(self, frame: np.ndarray, face_location: Tuple) -> Optional[dict]:
        """
        Get facial landmarks for a detected face.
        
        Args:
            frame: Video frame (BGR format)
            face_location: Face location tuple (top, right, bottom, left)
            
        Returns:
            Dictionary of facial landmarks or None
        """
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            landmarks = face_recognition.face_landmarks(rgb_frame, [face_location])
            
            if landmarks:
                return landmarks[0]
            return None
            
        except Exception as e:
            print(f"❌ Error getting face landmarks: {e}")
            return None
    
    def validate_image_quality(self, image_path: str) -> Tuple[bool, str]:
        """
        Validate if an image is suitable for face enrollment.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            # Load image
            image = face_recognition.load_image_file(image_path)
            
            # Check image size
            height, width = image.shape[:2]
            if width < 100 or height < 100:
                return False, "Image too small (minimum 100x100 pixels)"
            
            # Detect faces
            face_locations = face_recognition.face_locations(image, model=self.model)
            
            if len(face_locations) == 0:
                return False, "No face detected in image"
            
            if len(face_locations) > 1:
                return False, f"Multiple faces detected ({len(face_locations)}). Please use an image with only one face."
            
            # Check face size
            top, right, bottom, left = face_locations[0]
            face_width = right - left
            face_height = bottom - top
            
            if face_width < 50 or face_height < 50:
                return False, "Face too small in image. Please use a closer photo."
            
            # Check if face is too small relative to image
            face_area = face_width * face_height
            image_area = width * height
            face_ratio = face_area / image_area
            
            if face_ratio < 0.05:
                return False, "Face is too small relative to image size. Please use a closer photo."
            
            return True, "Image is suitable for enrollment"
            
        except Exception as e:
            return False, f"Error validating image: {str(e)}"
    
    def crop_face_from_image(self, image_path: str, output_path: str, 
                            padding: int = 50) -> bool:
        """
        Crop and save the face region from an image.
        
        Args:
            image_path: Path to input image
            output_path: Path to save cropped face
            padding: Pixels to add around face
            
        Returns:
            bool: True if successful
        """
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                return False
            
            # Convert to RGB for face detection
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Detect face
            face_locations = face_recognition.face_locations(rgb_image, model=self.model)
            
            if len(face_locations) == 0:
                return False
            
            # Get first face location
            top, right, bottom, left = face_locations[0]
            
            # Add padding
            height, width = image.shape[:2]
            top = max(0, top - padding)
            bottom = min(height, bottom + padding)
            left = max(0, left - padding)
            right = min(width, right + padding)
            
            # Crop face
            face_crop = image[top:bottom, left:right]
            
            # Save cropped face
            cv2.imwrite(output_path, face_crop)
            
            return True
            
        except Exception as e:
            print(f"❌ Error cropping face: {e}")
            return False

