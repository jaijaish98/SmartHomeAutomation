/**
 * Main App Component
 * Smart Home Camera Viewer Application
 */

import React, { useState, useEffect } from 'react';
import CameraSelector from './components/CameraSelector';
import CameraViewer from './components/CameraViewer';
import FaceManagement from './components/FaceManagement';
import { getAvailableCameras } from './services/cameraService';
import axios from 'axios';
import './styles/App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [cameras, setCameras] = useState([]);
  const [selectedCamera, setSelectedCamera] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const [currentView, setCurrentView] = useState('cameras'); // 'cameras' or 'faces'
  const [stopping, setStopping] = useState(false);

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

  const handleStopApplication = async () => {
    if (!window.confirm('Are you sure you want to stop the application? This will shut down both the backend and frontend servers.')) {
      return;
    }

    setStopping(true);

    try {
      // Call backend shutdown endpoint
      await axios.post(`${API_BASE_URL}/api/shutdown`, {}, { timeout: 2000 });
    } catch (error) {
      // Ignore errors as the server will be shutting down
      console.log('Server shutdown initiated');
    }

    // Show message to user
    alert('Application is shutting down. Please close this browser tab.');

    // Optionally close the window (may not work in all browsers)
    setTimeout(() => {
      window.close();
    }, 1000);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">
            <span className="title-icon">🏠</span>
            Smart Home Automation
          </h1>
          <p className="app-subtitle">Camera Viewer & Face Recognition</p>
        </div>

        {/* Navigation */}
        <nav className="app-nav">
          <button
            className={`nav-btn ${currentView === 'cameras' ? 'active' : ''}`}
            onClick={() => setCurrentView('cameras')}
          >
            📹 Cameras
          </button>
          <button
            className={`nav-btn ${currentView === 'faces' ? 'active' : ''}`}
            onClick={() => setCurrentView('faces')}
          >
            👤 Face Recognition
          </button>
          <button
            className="nav-btn stop-btn"
            onClick={handleStopApplication}
            disabled={stopping}
            title="Stop the application"
          >
            {stopping ? '⏳ Stopping...' : '🛑 Stop App'}
          </button>
        </nav>
      </header>

      <main className="app-main">
        {/* Camera View */}
        {currentView === 'cameras' && (
          <>
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
          </>
        )}

        {/* Face Recognition View */}
        {currentView === 'faces' && (
          <FaceManagement />
        )}
      </main>

      <footer className="app-footer">
        <p>Smart Home Automation © 2024</p>
        <p className="footer-info">
          {currentView === 'cameras'
            ? `${cameras.length} camera${cameras.length !== 1 ? 's' : ''} available`
            : 'Face Recognition Management'
          }
        </p>
      </footer>
    </div>
  );
}

export default App;

