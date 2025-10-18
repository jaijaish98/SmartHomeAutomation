"""
Video Streaming Routes
Endpoints for camera video streaming
"""

from flask import Blueprint, Response, jsonify
import cv2
import time

# Create blueprint
bp = Blueprint('stream', __name__, url_prefix='/stream')

# Camera manager will be injected
camera_manager = None


def init_blueprint(manager):
    """Initialize blueprint with camera manager"""
    global camera_manager
    camera_manager = manager


def generate_frames(camera_id):
    """
    Generator function to yield video frames
    Used for MJPEG streaming
    """
    while True:
        # Check if camera is still active
        if not camera_manager.is_camera_active(camera_id):
            break
        
        # Get frame from camera
        frame = camera_manager.get_camera_frame(camera_id)
        
        if frame is None:
            time.sleep(0.1)
            continue
        
        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        
        # Convert to bytes
        frame_bytes = buffer.tobytes()
        
        # Yield frame in multipart format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        # Small delay to control frame rate
        time.sleep(0.033)  # ~30 FPS


@bp.route('/<int:camera_id>')
def stream_camera(camera_id):
    """
    GET /stream/:id
    Stream video from camera as MJPEG
    """
    # Check if camera exists
    camera = camera_manager.get_camera_by_id(camera_id)
    if not camera:
        return jsonify({
            'success': False,
            'error': f'Camera {camera_id} not found'
        }), 404
    
    # Check if camera is active
    if not camera_manager.is_camera_active(camera_id):
        return jsonify({
            'success': False,
            'error': f'Camera {camera_id} is not open. Please open it first.'
        }), 400
    
    # Return MJPEG stream
    return Response(
        generate_frames(camera_id),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@bp.route('/<int:camera_id>/snapshot')
def get_snapshot(camera_id):
    """
    GET /stream/:id/snapshot
    Get a single frame snapshot from camera
    """
    # Check if camera exists
    camera = camera_manager.get_camera_by_id(camera_id)
    if not camera:
        return jsonify({
            'success': False,
            'error': f'Camera {camera_id} not found'
        }), 404
    
    # Check if camera is active
    if not camera_manager.is_camera_active(camera_id):
        return jsonify({
            'success': False,
            'error': f'Camera {camera_id} is not open'
        }), 400
    
    # Get single frame
    frame = camera_manager.get_camera_frame(camera_id)
    
    if frame is None:
        return jsonify({
            'success': False,
            'error': 'Failed to capture frame'
        }), 500
    
    # Encode as JPEG
    ret, buffer = cv2.imencode('.jpg', frame)
    if not ret:
        return jsonify({
            'success': False,
            'error': 'Failed to encode frame'
        }), 500
    
    # Return image
    return Response(
        buffer.tobytes(),
        mimetype='image/jpeg'
    )

