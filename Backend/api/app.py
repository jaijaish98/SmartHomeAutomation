"""
Flask API Server for Smart Home Camera System
Provides REST API endpoints for camera management and video streaming
"""

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import sys
import os
import signal
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from device_connectivity.camera import CameraDiscovery
from api.services.camera_manager import CameraManager
from api.routes import camera_routes, stream_routes
from api.routes.faces import faces_bp

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend access
CORS(app, resources={
    r"/api/*": {"origins": ["http://localhost:3000", "http://localhost:3001"]},
    r"/stream/*": {"origins": ["http://localhost:3000", "http://localhost:3001"]}
})

# Initialize camera manager
camera_manager = CameraManager()

# Initialize blueprints with camera manager
camera_routes.init_blueprint(camera_manager)
stream_routes.init_blueprint(camera_manager)

# Import and initialize faces blueprint with camera manager
from api.routes import faces
faces.set_camera_manager(camera_manager)

# Register blueprints
app.register_blueprint(camera_routes.bp)
app.register_blueprint(stream_routes.bp)
app.register_blueprint(faces_bp)

@app.route('/')
def index():
    """API root endpoint"""
    return jsonify({
        'name': 'Smart Home Camera API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'cameras': '/api/cameras',
            'open_camera': '/api/cameras/:id/open',
            'close_camera': '/api/cameras/:id/close',
            'stream': '/stream/:id',
            'faces': '/api/faces',
            'enroll_face': '/api/faces/enroll',
            'face_stats': '/api/faces/stats'
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'active_cameras': len(camera_manager.active_cameras)
    })

@app.route('/api/shutdown', methods=['POST'])
def shutdown():
    """Shutdown the server"""
    try:
        # Close all active cameras
        for camera_id in list(camera_manager.active_cameras.keys()):
            camera_manager.close_camera(camera_id)

        # Send response before shutting down
        response = jsonify({
            'status': 'shutting down',
            'message': 'Server is shutting down...'
        })

        # Schedule shutdown after response is sent
        def shutdown_server():
            import time
            time.sleep(1)  # Give time for response to be sent
            os.kill(os.getpid(), signal.SIGINT)

        import threading
        threading.Thread(target=shutdown_server).start()

        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 Smart Home Camera API Server")
    print("=" * 70)
    print(f"📡 Server starting on http://localhost:5000")
    print(f"📹 Camera API: http://localhost:5000/api/cameras")
    print(f"🎥 Stream API: http://localhost:5000/stream/:id")
    print(f"💚 Health Check: http://localhost:5000/health")
    print("=" * 70)
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

