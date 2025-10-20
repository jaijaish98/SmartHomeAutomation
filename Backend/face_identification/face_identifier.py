"""
Face identification module.
Matches detected faces against enrolled face encodings.
"""

import face_recognition
import numpy as np
from typing import List, Tuple, Optional, Dict
from .database import FaceDatabase


class FaceIdentifier:
    """Handles face identification and matching"""
    
    def __init__(self, database: FaceDatabase, tolerance: float = 0.6):
        """
        Initialize face identifier.
        
        Args:
            database: FaceDatabase instance
            tolerance: Face matching tolerance (lower = more strict, default 0.6)
        """
        self.database = database
        self.tolerance = tolerance
        self.known_encodings = []
        self.known_person_ids = []
        self.known_person_names = []
        self._load_known_faces()
        
        print(f"👤 Face identifier initialized with {len(self.known_encodings)} known faces")
    
    def _load_known_faces(self):
        """Load all known face encodings from database"""
        encodings_data = self.database.get_all_encodings()
        
        self.known_encodings = []
        self.known_person_ids = []
        self.known_person_names = []
        
        for person_id, person_name, encoding in encodings_data:
            self.known_encodings.append(encoding)
            self.known_person_ids.append(person_id)
            self.known_person_names.append(person_name)
    
    def reload_known_faces(self):
        """Reload known faces from database (call after enrolling new faces)"""
        self._load_known_faces()
        print(f"🔄 Reloaded {len(self.known_encodings)} known faces")
    
    def identify_face(self, face_encoding: np.ndarray) -> Tuple[Optional[int], Optional[str], float]:
        """
        Identify a face by comparing against known encodings.
        
        Args:
            face_encoding: 128-dimensional face encoding to identify
            
        Returns:
            Tuple of (person_id, person_name, confidence) or (None, None, 0.0) if unknown
        """
        if len(self.known_encodings) == 0:
            return None, None, 0.0
        
        # Calculate face distances
        face_distances = face_recognition.face_distance(self.known_encodings, face_encoding)
        
        # Find the best match
        best_match_index = np.argmin(face_distances)
        best_distance = face_distances[best_match_index]
        
        # Check if match is within tolerance
        if best_distance <= self.tolerance:
            person_id = self.known_person_ids[best_match_index]
            person_name = self.known_person_names[best_match_index]
            
            # Convert distance to confidence (0-100%)
            # Distance of 0 = 100% confidence, distance of tolerance = 0% confidence
            confidence = max(0, (1 - (best_distance / self.tolerance)) * 100)
            
            return person_id, person_name, confidence
        
        return None, None, 0.0
    
    def identify_faces_in_frame(self, face_encodings: List[np.ndarray]) -> List[Dict]:
        """
        Identify multiple faces in a frame.
        
        Args:
            face_encodings: List of face encodings to identify
            
        Returns:
            List of dictionaries with identification results
        """
        results = []
        
        for encoding in face_encodings:
            person_id, person_name, confidence = self.identify_face(encoding)
            
            results.append({
                'person_id': person_id,
                'person_name': person_name if person_name else 'Unknown',
                'confidence': confidence,
                'is_known': person_id is not None
            })
        
        return results
    
    def compare_faces(self, encoding1: np.ndarray, encoding2: np.ndarray) -> Tuple[bool, float]:
        """
        Compare two face encodings.
        
        Args:
            encoding1: First face encoding
            encoding2: Second face encoding
            
        Returns:
            Tuple of (is_match, distance)
        """
        distance = face_recognition.face_distance([encoding1], encoding2)[0]
        is_match = distance <= self.tolerance
        
        return is_match, distance
    
    def get_all_matches(self, face_encoding: np.ndarray, 
                       max_distance: float = None) -> List[Tuple[int, str, float]]:
        """
        Get all matching faces within tolerance.
        
        Args:
            face_encoding: Face encoding to match
            max_distance: Maximum distance for matches (uses tolerance if None)
            
        Returns:
            List of tuples (person_id, person_name, distance) sorted by distance
        """
        if len(self.known_encodings) == 0:
            return []
        
        if max_distance is None:
            max_distance = self.tolerance
        
        # Calculate distances to all known faces
        face_distances = face_recognition.face_distance(self.known_encodings, face_encoding)
        
        # Find all matches within tolerance
        matches = []
        for i, distance in enumerate(face_distances):
            if distance <= max_distance:
                person_id = self.known_person_ids[i]
                person_name = self.known_person_names[i]
                matches.append((person_id, person_name, distance))
        
        # Sort by distance (best matches first)
        matches.sort(key=lambda x: x[2])
        
        return matches
    
    def set_tolerance(self, tolerance: float):
        """
        Update face matching tolerance.
        
        Args:
            tolerance: New tolerance value (0.0-1.0, lower = more strict)
        """
        self.tolerance = tolerance
        print(f"🎯 Face matching tolerance updated to {tolerance}")
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about enrolled faces.
        
        Returns:
            Dictionary with statistics
        """
        persons = self.database.get_all_persons()
        
        total_persons = len(persons)
        total_encodings = len(self.known_encodings)
        
        # Calculate average encodings per person
        avg_encodings = total_encodings / total_persons if total_persons > 0 else 0
        
        return {
            'total_persons': total_persons,
            'total_encodings': total_encodings,
            'average_encodings_per_person': round(avg_encodings, 2),
            'tolerance': self.tolerance
        }
    
    def verify_person(self, person_id: int, face_encoding: np.ndarray) -> Tuple[bool, float]:
        """
        Verify if a face encoding belongs to a specific person.
        
        Args:
            person_id: Person ID to verify against
            face_encoding: Face encoding to verify
            
        Returns:
            Tuple of (is_verified, confidence)
        """
        # Get all encodings for this person
        person_encodings = self.database.get_person_encodings(person_id)
        
        if not person_encodings:
            return False, 0.0
        
        # Compare against all encodings for this person
        best_distance = float('inf')
        
        for _, encoding, _ in person_encodings:
            distance = face_recognition.face_distance([encoding], face_encoding)[0]
            best_distance = min(best_distance, distance)
        
        # Check if verified
        is_verified = best_distance <= self.tolerance
        confidence = max(0, (1 - (best_distance / self.tolerance)) * 100) if is_verified else 0.0
        
        return is_verified, confidence

