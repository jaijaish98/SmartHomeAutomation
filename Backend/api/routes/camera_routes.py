"""
Camera API Routes
Endpoints for camera discovery and control
"""

from flask import Blueprint, jsonify, request

# Create blueprint
bp = Blueprint('cameras', __name__, url_prefix='/api')

# Camera manager will be injected
camera_manager = None


def init_blueprint(manager):
    """Initialize blueprint with camera manager"""
    global camera_manager
    camera_manager = manager


@bp.route('/cameras', methods=['GET'])
def get_cameras():
    """
    GET /api/cameras
    Get list of all available cameras
    """
    try:
        cameras = camera_manager.get_all_cameras()
        return jsonify({
            'success': True,
            'count': len(cameras),
            'cameras': cameras
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/cameras/<int:camera_id>', methods=['GET'])
def get_camera(camera_id):
    """
    GET /api/cameras/:id
    Get specific camera information
    """
    try:
        camera = camera_manager.get_camera_by_id(camera_id)
        if camera:
            return jsonify({
                'success': True,
                'camera': camera,
                'active': camera_manager.is_camera_active(camera_id)
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Camera {camera_id} not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/cameras/<int:camera_id>/open', methods=['POST'])
def open_camera(camera_id):
    """
    POST /api/cameras/:id/open
    Open camera and start streaming
    """
    try:
        result = camera_manager.open_camera(camera_id)
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/cameras/<int:camera_id>/close', methods=['POST'])
def close_camera(camera_id):
    """
    POST /api/cameras/:id/close
    Close camera and stop streaming
    """
    try:
        result = camera_manager.close_camera(camera_id)
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/cameras/active', methods=['GET'])
def get_active_cameras():
    """
    GET /api/cameras/active
    Get list of currently active cameras
    """
    try:
        all_cameras = camera_manager.get_all_cameras()
        active_cameras = [
            cam for cam in all_cameras 
            if camera_manager.is_camera_active(cam['id'])
        ]
        return jsonify({
            'success': True,
            'count': len(active_cameras),
            'cameras': active_cameras
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

