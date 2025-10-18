/**
 * Camera Selector Component
 * Dropdown to select from available cameras
 */

import React from 'react';
import '../styles/CameraSelector.css';

const CameraSelector = ({ cameras, selectedCamera, onCameraSelect, disabled }) => {
  const handleChange = (event) => {
    const cameraId = parseInt(event.target.value);
    const camera = cameras.find(cam => cam.id === cameraId);
    onCameraSelect(camera);
  };

  return (
    <div className="camera-selector">
      <label htmlFor="camera-dropdown" className="selector-label">
        📹 Select Camera:
      </label>
      <select
        id="camera-dropdown"
        className="camera-dropdown"
        value={selectedCamera?.id || ''}
        onChange={handleChange}
        disabled={disabled}
      >
        <option value="" disabled>
          -- Choose a camera --
        </option>
        {cameras.map((camera) => (
          <option key={camera.id} value={camera.id}>
            {camera.type === 'rtsp' ? '📹' : '🎥'} {camera.name} ({camera.resolution})
          </option>
        ))}
      </select>
      
      {selectedCamera && (
        <div className="camera-info">
          <div className="info-item">
            <span className="info-label">Type:</span>
            <span className="info-value">{selectedCamera.type === 'rtsp' ? 'RTSP Camera' : 'Webcam'}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Resolution:</span>
            <span className="info-value">{selectedCamera.resolution}</span>
          </div>
          <div className="info-item">
            <span className="info-label">FPS:</span>
            <span className="info-value">{selectedCamera.fps}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default CameraSelector;

