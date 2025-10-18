/**
 * Camera Viewer Component
 * Displays camera feed with automatic switching
 */

import React, { useState, useEffect, useRef } from 'react';
import { openCamera, closeCamera, getCameraStreamUrl } from '../services/cameraService';
import '../styles/CameraViewer.css';

const CameraViewer = ({ selectedCamera, onStreamingChange }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [streamUrl, setStreamUrl] = useState(null);
  const currentCameraIdRef = useRef(null);

  // Auto-switch camera when selection changes
  useEffect(() => {
    const switchCamera = async () => {
      // If no camera selected, close current camera
      if (!selectedCamera) {
        if (currentCameraIdRef.current !== null) {
          await handleCloseCamera(currentCameraIdRef.current);
        }
        return;
      }

      // If same camera, do nothing
      if (selectedCamera.id === currentCameraIdRef.current) {
        return;
      }

      // Close current camera if open
      if (currentCameraIdRef.current !== null) {
        await handleCloseCamera(currentCameraIdRef.current);
      }

      // Open new camera
      await handleOpenCamera(selectedCamera);
    };

    switchCamera();
  }, [selectedCamera]);

  const handleOpenCamera = async (camera) => {
    if (!camera) {
      setError('No camera selected');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await openCamera(camera.id);

      if (response.success) {
        setStreamUrl(getCameraStreamUrl(camera.id));
        setIsOpen(true);
        currentCameraIdRef.current = camera.id;
        if (onStreamingChange) {
          onStreamingChange(true);
        }
      } else {
        setError('Failed to open camera');
      }
    } catch (err) {
      setError('Error opening camera: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCloseCamera = async (cameraId) => {
    setLoading(true);
    setError(null);

    try {
      const response = await closeCamera(cameraId);

      if (response.success) {
        setStreamUrl(null);
        setIsOpen(false);
        currentCameraIdRef.current = null;
        if (onStreamingChange) {
          onStreamingChange(false);
        }
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
      {loading && (
        <div className="loading-overlay">
          <div className="loading-spinner"></div>
          <p>Switching camera...</p>
        </div>
      )}

      {error && (
        <div className="error-message">
          ❌ {error}
        </div>
      )}

      <div className="viewer-container">
        {!selectedCamera && (
          <div className="placeholder">
            <div className="placeholder-icon">📹</div>
            <p>Select a camera from the side panel</p>
          </div>
        )}

        {selectedCamera && !isOpen && !loading && (
          <div className="placeholder">
            <div className="placeholder-icon">🎥</div>
            <p>Camera: {selectedCamera.name}</p>
            <p className="placeholder-hint">Opening camera...</p>
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

