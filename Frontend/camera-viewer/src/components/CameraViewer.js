/**
 * Camera Viewer Component
 * Displays camera feed with open/close controls
 */

import React, { useState } from 'react';
import { openCamera, closeCamera, getCameraStreamUrl } from '../services/cameraService';
import '../styles/CameraViewer.css';

const CameraViewer = ({ selectedCamera }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [streamUrl, setStreamUrl] = useState(null);

  const handleOpenCamera = async () => {
    if (!selectedCamera) {
      setError('Please select a camera first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await openCamera(selectedCamera.id);
      
      if (response.success) {
        setStreamUrl(getCameraStreamUrl(selectedCamera.id));
        setIsOpen(true);
      } else {
        setError('Failed to open camera');
      }
    } catch (err) {
      setError('Error opening camera: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCloseCamera = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await closeCamera(selectedCamera.id);
      
      if (response.success) {
        setStreamUrl(null);
        setIsOpen(false);
      } else {
        setError('Failed to close camera');
      }
    } catch (err) {
      setError('Error closing camera: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="camera-viewer">
      <div className="viewer-controls">
        <button
          className="btn btn-open"
          onClick={handleOpenCamera}
          disabled={!selectedCamera || isOpen || loading}
        >
          {loading && !isOpen ? '⏳ Opening...' : '▶️ Open Camera'}
        </button>
        
        <button
          className="btn btn-close"
          onClick={handleCloseCamera}
          disabled={!isOpen || loading}
        >
          {loading && isOpen ? '⏳ Closing...' : '⏹️ Close Camera'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          ❌ {error}
        </div>
      )}

      <div className="viewer-container">
        {!selectedCamera && (
          <div className="placeholder">
            <div className="placeholder-icon">📹</div>
            <p>Select a camera from the dropdown above</p>
          </div>
        )}

        {selectedCamera && !isOpen && (
          <div className="placeholder">
            <div className="placeholder-icon">🎥</div>
            <p>Camera: {selectedCamera.name}</p>
            <p className="placeholder-hint">Click "Open Camera" to start viewing</p>
          </div>
        )}

        {isOpen && streamUrl && (
          <div className="stream-container">
            <div className="stream-header">
              <span className="stream-status">🔴 LIVE</span>
              <span className="stream-name">{selectedCamera.name}</span>
            </div>

            {/* Real camera stream */}
            <div className="stream-video">
              <img
                src={streamUrl}
                alt={`${selectedCamera.name} stream`}
                className="video-stream"
              />
              <div className="video-overlay">
                <div className="recording-indicator">● REC</div>
                <div className="camera-label">{selectedCamera.name}</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {isOpen && (
        <div className="viewer-stats">
          <div className="stat-item">
            <span className="stat-label">Status:</span>
            <span className="stat-value status-active">● Active</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Camera:</span>
            <span className="stat-value">{selectedCamera.name}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Type:</span>
            <span className="stat-value">{selectedCamera.type.toUpperCase()}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default CameraViewer;

