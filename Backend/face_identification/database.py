"""
Database module for face recognition system.
Handles storage and retrieval of person data and face encodings.
"""

import sqlite3
import json
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class FaceDatabase:
    """Manages face recognition database operations"""
    
    def __init__(self, db_path: str = None):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file. If None, uses default location.
        """
        if db_path is None:
            # Default to Backend/face_recognition/data/faces.db
            db_dir = Path(__file__).parent / 'data'
            db_dir.mkdir(exist_ok=True)
            db_path = db_dir / 'faces.db'
        
        self.db_path = str(db_path)
        self.conn = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
    
    def _create_tables(self):
        """Create database tables if they don't exist"""
        cursor = self.conn.cursor()
        
        # Create persons table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS persons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                notes TEXT,
                enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create face_encodings table (supports multiple encodings per person)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS face_encodings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                encoding_data TEXT NOT NULL,
                photo_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE
            )
        ''')
        
        # Create index for faster lookups
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_person_id 
            ON face_encodings(person_id)
        ''')
        
        self.conn.commit()
    
    def enroll_person(self, name: str, encoding: np.ndarray, 
                     photo_path: str = None, notes: str = None) -> int:
        """
        Enroll a new person with their face encoding.
        
        Args:
            name: Person's name
            encoding: 128-dimensional face encoding
            photo_path: Path to the enrollment photo
            notes: Optional notes about the person
            
        Returns:
            int: Person ID
        """
        cursor = self.conn.cursor()
        
        # Insert person
        cursor.execute(
            'INSERT INTO persons (name, notes) VALUES (?, ?)',
            (name, notes)
        )
        person_id = cursor.lastrowid
        
        # Insert face encoding
        encoding_json = json.dumps(encoding.tolist())
        cursor.execute(
            'INSERT INTO face_encodings (person_id, encoding_data, photo_path) VALUES (?, ?, ?)',
            (person_id, encoding_json, photo_path)
        )
        
        self.conn.commit()
        return person_id
    
    def add_encoding_to_person(self, person_id: int, encoding: np.ndarray, 
                               photo_path: str = None) -> int:
        """
        Add an additional face encoding to an existing person.
        
        Args:
            person_id: ID of the person
            encoding: 128-dimensional face encoding
            photo_path: Path to the photo
            
        Returns:
            int: Encoding ID
        """
        cursor = self.conn.cursor()
        encoding_json = json.dumps(encoding.tolist())
        
        cursor.execute(
            'INSERT INTO face_encodings (person_id, encoding_data, photo_path) VALUES (?, ?, ?)',
            (person_id, encoding_json, photo_path)
        )
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_all_persons(self) -> List[Dict]:
        """
        Get all enrolled persons.
        
        Returns:
            List of person dictionaries
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT p.id, p.name, p.notes, p.enrolled_at, p.updated_at,
                   COUNT(fe.id) as encoding_count
            FROM persons p
            LEFT JOIN face_encodings fe ON p.id = fe.person_id
            GROUP BY p.id
            ORDER BY p.enrolled_at DESC
        ''')
        
        persons = []
        for row in cursor.fetchall():
            persons.append({
                'id': row['id'],
                'name': row['name'],
                'notes': row['notes'],
                'enrolled_at': row['enrolled_at'],
                'updated_at': row['updated_at'],
                'encoding_count': row['encoding_count']
            })
        
        return persons
    
    def get_person(self, person_id: int) -> Optional[Dict]:
        """
        Get a specific person by ID.
        
        Args:
            person_id: Person ID
            
        Returns:
            Person dictionary or None if not found
        """
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT * FROM persons WHERE id = ?',
            (person_id,)
        )
        
        row = cursor.fetchone()
        if row is None:
            return None
        
        return {
            'id': row['id'],
            'name': row['name'],
            'notes': row['notes'],
            'enrolled_at': row['enrolled_at'],
            'updated_at': row['updated_at']
        }
    
    def get_person_encodings(self, person_id: int) -> List[Tuple[int, np.ndarray, str]]:
        """
        Get all face encodings for a person.
        
        Args:
            person_id: Person ID
            
        Returns:
            List of tuples (encoding_id, encoding_array, photo_path)
        """
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT id, encoding_data, photo_path FROM face_encodings WHERE person_id = ?',
            (person_id,)
        )
        
        encodings = []
        for row in cursor.fetchall():
            encoding_array = np.array(json.loads(row['encoding_data']))
            encodings.append((row['id'], encoding_array, row['photo_path']))
        
        return encodings
    
    def get_all_encodings(self) -> List[Tuple[int, str, np.ndarray]]:
        """
        Get all face encodings with person information.
        
        Returns:
            List of tuples (person_id, person_name, encoding_array)
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT p.id, p.name, fe.encoding_data
            FROM persons p
            JOIN face_encodings fe ON p.id = fe.person_id
        ''')
        
        encodings = []
        for row in cursor.fetchall():
            encoding_array = np.array(json.loads(row['encoding_data']))
            encodings.append((row['id'], row['name'], encoding_array))
        
        return encodings
    
    def update_person(self, person_id: int, name: str = None, notes: str = None) -> bool:
        """
        Update person information.
        
        Args:
            person_id: Person ID
            name: New name (optional)
            notes: New notes (optional)
            
        Returns:
            bool: True if updated successfully
        """
        cursor = self.conn.cursor()
        
        updates = []
        params = []
        
        if name is not None:
            updates.append('name = ?')
            params.append(name)
        
        if notes is not None:
            updates.append('notes = ?')
            params.append(notes)
        
        if not updates:
            return False
        
        updates.append('updated_at = CURRENT_TIMESTAMP')
        params.append(person_id)
        
        query = f"UPDATE persons SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        self.conn.commit()
        
        return cursor.rowcount > 0
    
    def delete_person(self, person_id: int) -> bool:
        """
        Delete a person and all their face encodings.
        
        Args:
            person_id: Person ID
            
        Returns:
            bool: True if deleted successfully
        """
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM persons WHERE id = ?', (person_id,))
        self.conn.commit()
        
        return cursor.rowcount > 0
    
    def get_photo_path(self, person_id: int) -> Optional[str]:
        """
        Get the first photo path for a person.

        Args:
            person_id: Person ID

        Returns:
            Photo path or None
        """
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT photo_path FROM face_encodings WHERE person_id = ? LIMIT 1',
            (person_id,)
        )

        row = cursor.fetchone()
        return row['photo_path'] if row else None

    def get_statistics(self) -> Dict:
        """
        Get statistics about the face recognition database.

        Returns:
            Dictionary with statistics
        """
        cursor = self.conn.cursor()

        # Get total persons
        cursor.execute('SELECT COUNT(*) as count FROM persons')
        total_persons = cursor.fetchone()['count']

        # Get total encodings
        cursor.execute('SELECT COUNT(*) as count FROM face_encodings')
        total_encodings = cursor.fetchone()['count']

        # Calculate average encodings per person
        avg_encodings = total_encodings / total_persons if total_persons > 0 else 0

        return {
            'total_persons': total_persons,
            'total_encodings': total_encodings,
            'average_encodings_per_person': avg_encodings
        }

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def __del__(self):
        """Cleanup on deletion"""
        self.close()

