"""
Face recognition API routes.
Handles face enrollment, identification, and management.
"""

from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from pathlib import Path
from datetime import datetime

# Import face identification modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from face_identification import FaceEncoder, FaceIdentifier, FaceDatabase

# Create blueprint
faces_bp = Blueprint('faces', __name__)

# Initialize face recognition components
UPLOAD_FOLDER = Path(__file__).parent.parent.parent / 'face_recognition' / 'data' / 'photos'
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Global instances (will be initialized by camera_manager)
face_encoder = None
face_identifier = None
face_database = None
camera_manager_instance = None


def init_face_recognition():
    """Initialize face recognition components"""
    global face_encoder, face_identifier, face_database

    if face_database is None:
        face_database = FaceDatabase()

    if face_encoder is None:
        face_encoder = FaceEncoder(model='hog')  # Use 'cnn' for better accuracy with GPU

    if face_identifier is None:
        face_identifier = FaceIdentifier(face_database, tolerance=0.6)

    return face_encoder, face_identifier, face_database


def set_camera_manager(manager):
    """Set the camera manager instance"""
    global camera_manager_instance
    camera_manager_instance = manager


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@faces_bp.route('/api/faces/enroll', methods=['POST'])
def enroll_face():
    """
    Enroll a new person with uploaded image OR add photo to existing person.

    Request:
        - file: Image file (multipart/form-data)
        - name: Person's name (for new person)
        - person_id: Existing person ID (for adding photo to existing person)
        - notes: Optional notes

    Response:
        - person_id: ID of enrolled person
        - message: Success message
        - total_encodings: Total number of photos for this person
    """
    try:
        # Initialize components
        encoder, identifier, database = init_face_recognition()

        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif, bmp'}), 400

        # Check if adding to existing person or creating new
        person_id_str = request.form.get('person_id', '').strip()
        name = request.form.get('name', '').strip()
        notes = request.form.get('notes', '').strip()

        if person_id_str:
            # Adding photo to existing person
            person_id = int(person_id_str)
            person = database.get_person(person_id)
            if not person:
                return jsonify({'error': 'Person not found'}), 404
            name = person['name']
        else:
            # Creating new person
            if not name:
                return jsonify({'error': 'Person name is required'}), 400
            person_id = None

        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = UPLOAD_FOLDER / filename
        file.save(str(filepath))

        # Validate image quality
        is_valid, message = encoder.validate_image_quality(str(filepath))
        if not is_valid:
            os.remove(filepath)
            return jsonify({'error': message}), 400

        # Generate face encoding
        encoding, face_location = encoder.encode_face_from_file(str(filepath))

        if encoding is None:
            os.remove(filepath)
            return jsonify({'error': 'Could not detect face in image'}), 400

        # Enroll person in database
        if person_id:
            # Add encoding to existing person
            database.add_encoding_to_person(person_id, encoding, str(filepath))
        else:
            # Create new person
            person_id = database.enroll_person(name, encoding, str(filepath), notes)

        # Get total encodings for this person
        encodings = database.get_person_encodings(person_id)
        total_encodings = len(encodings)

        # Reload known faces in identifier
        identifier.reload_known_faces()

        return jsonify({
            'success': True,
            'person_id': person_id,
            'name': name,
            'message': f'Successfully enrolled {name}',
            'photo_path': str(filepath),
            'total_encodings': total_encodings
        }), 201

    except Exception as e:
        return jsonify({'error': f'Enrollment failed: {str(e)}'}), 500


@faces_bp.route('/api/faces/enroll/capture', methods=['POST'])
def enroll_face_from_capture():
    """
    Enroll a new person by capturing from active camera OR add photo to existing person.

    Request (JSON):
        - camera_id: ID of active camera
        - name: Person's name (for new person)
        - person_id: Existing person ID (for adding photo to existing person)
        - notes: Optional notes

    Response:
        - person_id: ID of enrolled person
        - message: Success message
        - total_encodings: Total number of photos for this person
    """
    try:
        # Initialize components
        encoder, identifier, database = init_face_recognition()

        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        camera_id = data.get('camera_id')
        person_id_val = data.get('person_id')
        name = data.get('name', '').strip()
        notes = data.get('notes', '').strip()

        if not camera_id:
            return jsonify({'error': 'Camera ID is required'}), 400

        # Check if adding to existing person or creating new
        if person_id_val:
            person_id = int(person_id_val)
            person = database.get_person(person_id)
            if not person:
                return jsonify({'error': 'Person not found'}), 404
            name = person['name']
        else:
            if not name:
                return jsonify({'error': 'Person name is required'}), 400
            person_id = None

        # Get frame from camera manager
        if camera_manager_instance is None:
            return jsonify({'error': 'Camera manager not initialized'}), 500

        frame = camera_manager_instance.capture_raw_frame(camera_id)

        if frame is None:
            return jsonify({'error': 'Could not capture frame from camera'}), 400

        # Generate face encoding from frame
        encoding, face_location = encoder.encode_face_from_frame(frame)

        if encoding is None:
            return jsonify({'error': 'Could not detect face in camera frame'}), 400

        # Save captured frame
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"capture_{timestamp}_{name.replace(' ', '_')}.jpg"
        filepath = UPLOAD_FOLDER / filename
        cv2.imwrite(str(filepath), frame)

        # Enroll person in database
        if person_id:
            # Add encoding to existing person
            database.add_encoding_to_person(person_id, encoding, str(filepath))
        else:
            # Create new person
            person_id = database.enroll_person(name, encoding, str(filepath), notes)

        # Get total encodings for this person
        encodings = database.get_person_encodings(person_id)
        total_encodings = len(encodings)

        # Reload known faces in identifier
        identifier.reload_known_faces()

        return jsonify({
            'success': True,
            'person_id': person_id,
            'name': name,
            'message': f'Successfully enrolled {name} from camera capture',
            'photo_path': str(filepath),
            'total_encodings': total_encodings
        }), 201

    except Exception as e:
        return jsonify({'error': f'Enrollment failed: {str(e)}'}), 500


@faces_bp.route('/api/faces', methods=['GET'])
def get_all_faces():
    """
    Get all enrolled persons.
    
    Response:
        - persons: List of enrolled persons
    """
    try:
        encoder, identifier, database = init_face_recognition()
        
        persons = database.get_all_persons()
        
        # Add photo URLs
        for person in persons:
            photo_path = database.get_photo_path(person['id'])
            if photo_path:
                person['photo_url'] = f"/api/faces/{person['id']}/photo"
            else:
                person['photo_url'] = None
        
        return jsonify({
            'success': True,
            'persons': persons,
            'count': len(persons)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve persons: {str(e)}'}), 500


@faces_bp.route('/api/faces/<int:person_id>', methods=['GET'])
def get_face(person_id):
    """
    Get details of a specific person.
    
    Response:
        - person: Person details
    """
    try:
        encoder, identifier, database = init_face_recognition()
        
        person = database.get_person(person_id)
        
        if person is None:
            return jsonify({'error': 'Person not found'}), 404
        
        # Add photo URL
        photo_path = database.get_photo_path(person_id)
        if photo_path:
            person['photo_url'] = f"/api/faces/{person_id}/photo"
        else:
            person['photo_url'] = None
        
        # Add encoding count
        encodings = database.get_person_encodings(person_id)
        person['encoding_count'] = len(encodings)
        
        return jsonify({
            'success': True,
            'person': person
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve person: {str(e)}'}), 500


@faces_bp.route('/api/faces/<int:person_id>', methods=['PUT'])
def update_face(person_id):
    """
    Update person details.
    
    Request (JSON):
        - name: New name (optional)
        - notes: New notes (optional)
    
    Response:
        - message: Success message
    """
    try:
        encoder, identifier, database = init_face_recognition()
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        name = data.get('name')
        notes = data.get('notes')
        
        success = database.update_person(person_id, name, notes)
        
        if not success:
            return jsonify({'error': 'Person not found or no changes made'}), 404
        
        # Reload known faces if name changed
        if name:
            identifier.reload_known_faces()
        
        return jsonify({
            'success': True,
            'message': 'Person updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to update person: {str(e)}'}), 500


@faces_bp.route('/api/faces/<int:person_id>', methods=['DELETE'])
def delete_face(person_id):
    """
    Delete an enrolled person.
    
    Response:
        - message: Success message
    """
    try:
        encoder, identifier, database = init_face_recognition()
        
        # Get photo path before deletion
        photo_path = database.get_photo_path(person_id)
        
        # Delete from database
        success = database.delete_person(person_id)
        
        if not success:
            return jsonify({'error': 'Person not found'}), 404
        
        # Delete photo file if exists
        if photo_path and os.path.exists(photo_path):
            try:
                os.remove(photo_path)
            except Exception as e:
                print(f"⚠️  Could not delete photo file: {e}")
        
        # Reload known faces
        identifier.reload_known_faces()
        
        return jsonify({
            'success': True,
            'message': 'Person deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to delete person: {str(e)}'}), 500


@faces_bp.route('/api/faces/<int:person_id>/photo', methods=['GET'])
def get_person_photo(person_id):
    """
    Get the photo of an enrolled person.

    Response:
        - Image file
    """
    try:
        encoder, identifier, database = init_face_recognition()

        photo_path = database.get_photo_path(person_id)

        if not photo_path or not os.path.exists(photo_path):
            return jsonify({'error': 'Photo not found'}), 404

        return send_file(photo_path, mimetype='image/jpeg')

    except Exception as e:
        return jsonify({'error': f'Failed to retrieve photo: {str(e)}'}), 500


@faces_bp.route('/api/faces/reload', methods=['POST'])
def reload_face_recognition():
    """
    Reload face recognition encodings from database.
    This allows real-time updates without restarting the application.

    Response:
        - success: Boolean
        - message: Status message
        - total_faces: Number of faces loaded
    """
    try:
        encoder, identifier, database = init_face_recognition()

        # Reload known faces in identifier
        identifier.reload_known_faces()

        # Get statistics
        stats = database.get_statistics()

        return jsonify({
            'success': True,
            'message': 'Face recognition reloaded successfully',
            'total_faces': stats['total_persons']
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to reload face recognition: {str(e)}'}), 500


@faces_bp.route('/api/faces/stats', methods=['GET'])
def get_face_stats():
    """
    Get face recognition statistics.
    
    Response:
        - statistics: Face recognition stats
    """
    try:
        encoder, identifier, database = init_face_recognition()
        
        stats = identifier.get_statistics()
        
        return jsonify({
            'success': True,
            'statistics': stats
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve statistics: {str(e)}'}), 500

