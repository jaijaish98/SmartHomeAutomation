/**
 * Main App Component
 * Smart Home Camera Viewer Application
 */

import React, { useState, useEffect } from 'react';
import CameraSelector from './components/CameraSelector';
import CameraViewer from './components/CameraViewer';
import { getAvailableCameras } from './services/cameraService';
import './styles/App.css';

function App() {
  const [cameras, setCameras] = useState([]);
  const [selectedCamera, setSelectedCamera] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isStreaming, setIsStreaming] = useState(false);

  // Load available cameras on mount
  useEffect(() => {
    loadCameras();
  }, []);

  const loadCameras = async () => {
    setLoading(true);
    setError(null);

    try {
      const cameraList = await getAvailableCameras();
      setCameras(cameraList);
    } catch (err) {
      setError('Failed to load cameras: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCameraSelect = (camera) => {
    setSelectedCamera(camera);
  };

  const handleStreamingChange = (streaming) => {
    setIsStreaming(streaming);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">
            <span className="title-icon">🏠</span>
            Smart Home Camera Viewer
          </h1>
          <p className="app-subtitle">View and manage your cameras</p>
        </div>
      </header>

      <main className="app-main">
        {loading && (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Loading cameras...</p>
          </div>
        )}

        {error && (
          <div className="error-container">
            <p className="error-text">❌ {error}</p>
            <button className="btn btn-retry" onClick={loadCameras}>
              🔄 Retry
            </button>
          </div>
        )}

        {!loading && !error && (
          <div className="content-container">
            <div className="control-panel">
              <CameraSelector
                cameras={cameras}
                selectedCamera={selectedCamera}
                onCameraSelect={handleCameraSelect}
                disabled={loading}
                isStreaming={isStreaming}
              />
            </div>

            <div className="viewer-panel">
              <CameraViewer
                selectedCamera={selectedCamera}
                onStreamingChange={handleStreamingChange}
              />
            </div>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>Smart Home Automation © 2024</p>
        <p className="footer-info">
          {cameras.length} camera{cameras.length !== 1 ? 's' : ''} available
        </p>
      </footer>
    </div>
  );
}

export default App;

