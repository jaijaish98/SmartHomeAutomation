/**
 * Camera Selector Component
 * Side panel to select from available cameras with auto-switching
 */

import React from 'react';
import '../styles/CameraSelector.css';

const CameraSelector = ({ cameras, selectedCamera, onCameraSelect, disabled, isStreaming }) => {
  const handleCameraClick = (camera) => {
    if (!disabled) {
      onCameraSelect(camera);
    }
  };

  return (
    <div className="camera-selector-panel">
      <div className="panel-header">
        <h3 className="panel-title">📹 Cameras</h3>
        <span className="camera-count">{cameras.length} available</span>
      </div>

      <div className="camera-list">
        {cameras.map((camera) => (
          <div
            key={camera.id}
            className={`camera-item ${selectedCamera?.id === camera.id ? 'active' : ''} ${disabled ? 'disabled' : ''}`}
            onClick={() => handleCameraClick(camera)}
          >
            <div className="camera-item-header">
              <span className="camera-icon">
                {camera.type === 'rtsp' ? '📹' : '🎥'}
              </span>
              <span className="camera-name">{camera.name}</span>
              {selectedCamera?.id === camera.id && isStreaming && (
                <span className="streaming-badge">🔴 LIVE</span>
              )}
            </div>
            <div className="camera-item-details">
              <span className="detail-badge">{camera.type === 'rtsp' ? 'RTSP' : 'Webcam'}</span>
              <span className="detail-text">{camera.resolution}</span>
              <span className="detail-text">{camera.fps} FPS</span>
            </div>
          </div>
        ))}
      </div>

      {selectedCamera && (
        <div className="selected-camera-info">
          <div className="info-header">Selected Camera</div>
          <div className="info-content">
            <div className="info-row">
              <span className="info-label">Name:</span>
              <span className="info-value">{selectedCamera.name}</span>
            </div>
            <div className="info-row">
              <span className="info-label">Type:</span>
              <span className="info-value">{selectedCamera.type === 'rtsp' ? 'RTSP Camera' : 'Webcam'}</span>
            </div>
            <div className="info-row">
              <span className="info-label">Resolution:</span>
              <span className="info-value">{selectedCamera.resolution}</span>
            </div>
            <div className="info-row">
              <span className="info-label">FPS:</span>
              <span className="info-value">{selectedCamera.fps}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CameraSelector;

