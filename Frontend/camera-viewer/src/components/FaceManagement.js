import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './FaceManagement.css';

const API_BASE_URL = 'http://localhost:5000';

const FaceManagement = () => {
  const [enrolledFaces, setEnrolledFaces] = useState([]);
  const [cameras, setCameras] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  // Enrollment form state
  const [enrollmentMode, setEnrollmentMode] = useState('upload'); // 'upload' or 'capture'
  const [personMode, setPersonMode] = useState('new'); // 'new' or 'existing'
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [personName, setPersonName] = useState('');
  const [personNotes, setPersonNotes] = useState('');
  const [selectedCamera, setSelectedCamera] = useState(null);
  const [selectedExistingPerson, setSelectedExistingPerson] = useState(null);

  // Camera preview state
  const [showCameraPreview, setShowCameraPreview] = useState(false);
  const [countdown, setCountdown] = useState(null);
  const [capturedImage, setCapturedImage] = useState(null);

  useEffect(() => {
    fetchEnrolledFaces();
    fetchCameras();
    fetchStats();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchEnrolledFaces = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/faces`);
      if (response.data.success) {
        setEnrolledFaces(response.data.persons);
      }
    } catch (error) {
      console.error('Error fetching enrolled faces:', error);
      showMessage('error', 'Failed to load enrolled faces');
    }
  };

  const fetchCameras = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/cameras`);
      if (response.data.success) {
        setCameras(response.data.cameras);
        if (response.data.cameras.length > 0) {
          setSelectedCamera(response.data.cameras[0].id);
        }
      }
    } catch (error) {
      console.error('Error fetching cameras:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/faces/stats`);
      if (response.data.success) {
        setStats(response.data.statistics);
      }
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const showMessage = (type, text) => {
    setMessage({ type, text });
    setTimeout(() => setMessage({ type: '', text: '' }), 5000);
  };

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Validate file type
      const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/bmp'];
      if (!validTypes.includes(file.type)) {
        showMessage('error', 'Please select a valid image file (PNG, JPG, GIF, BMP)');
        return;
      }

      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        showMessage('error', 'File size must be less than 10MB');
        return;
      }

      setSelectedFile(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const reloadFaceRecognition = async () => {
    try {
      await axios.post(`${API_BASE_URL}/api/faces/reload`);
      console.log('Face recognition reloaded successfully');
    } catch (error) {
      console.error('Error reloading face recognition:', error);
    }
  };

  const handleEnrollWithUpload = async (e) => {
    e.preventDefault();

    if (!selectedFile) {
      showMessage('error', 'Please select an image file');
      return;
    }

    // Validate based on person mode
    if (personMode === 'new') {
      if (!personName.trim()) {
        showMessage('error', 'Please enter a name');
        return;
      }
    } else {
      if (!selectedExistingPerson) {
        showMessage('error', 'Please select an existing person');
        return;
      }
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('notes', personNotes.trim());

      if (personMode === 'new') {
        formData.append('name', personName.trim());
      } else {
        formData.append('person_id', selectedExistingPerson);
      }

      const response = await axios.post(`${API_BASE_URL}/api/faces/enroll`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        const enrolledName = personMode === 'new' ? personName : enrolledFaces.find(p => p.id === selectedExistingPerson)?.name;
        const photoCount = response.data.total_encodings || 1;
        showMessage('success', `Successfully enrolled ${enrolledName}! Total photos: ${photoCount}`);
        resetForm();
        fetchEnrolledFaces();
        fetchStats();

        // Trigger real-time reload of face recognition
        await reloadFaceRecognition();
      }
    } catch (error) {
      const errorMsg = error.response?.data?.error || 'Failed to enroll face';
      showMessage('error', errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const startCameraPreview = () => {
    if (!selectedCamera) {
      showMessage('error', 'Please select a camera');
      return;
    }

    // Simply show the preview - the stream URL will handle opening the camera
    setShowCameraPreview(true);
  };

  const stopCameraPreview = () => {
    setShowCameraPreview(false);
    setCapturedImage(null);
    setCountdown(null);
  };

  const startCountdown = () => {
    let count = 3;
    setCountdown(count);

    const countdownInterval = setInterval(() => {
      count--;
      if (count > 0) {
        setCountdown(count);
      } else {
        clearInterval(countdownInterval);
        setCountdown('📸');
        setTimeout(() => {
          captureFrame();
        }, 500);
      }
    }, 1000);
  };

  const captureFrame = () => {
    // Set a timestamp to force image refresh
    setCapturedImage(`${API_BASE_URL}/stream/${selectedCamera}?t=${Date.now()}`);
    setCountdown(null);
    setShowCameraPreview(false);
  };

  const handleEnrollWithCapture = async (e) => {
    e.preventDefault();

    // Validate based on person mode
    if (personMode === 'new') {
      if (!personName.trim()) {
        showMessage('error', 'Please enter a name');
        return;
      }
    } else {
      if (!selectedExistingPerson) {
        showMessage('error', 'Please select an existing person');
        return;
      }
    }

    if (!selectedCamera) {
      showMessage('error', 'Please select a camera');
      return;
    }

    setLoading(true);

    try {
      // Ensure camera is open before capturing
      const camerasResponse = await axios.get(`${API_BASE_URL}/api/cameras`);
      const camera = camerasResponse.data.cameras.find(c => c.id === selectedCamera);

      if (!camera.is_active) {
        await axios.post(`${API_BASE_URL}/api/cameras/${selectedCamera}/open`);
        // Wait a moment for camera to initialize
        await new Promise(resolve => setTimeout(resolve, 1000));
      }

      const payload = {
        camera_id: selectedCamera,
        notes: personNotes.trim(),
      };

      if (personMode === 'new') {
        payload.name = personName.trim();
      } else {
        payload.person_id = selectedExistingPerson;
      }

      const response = await axios.post(`${API_BASE_URL}/api/faces/enroll/capture`, payload);

      if (response.data.success) {
        const enrolledName = personMode === 'new' ? personName : enrolledFaces.find(p => p.id === selectedExistingPerson)?.name;
        const photoCount = response.data.total_encodings || 1;
        showMessage('success', `Successfully enrolled ${enrolledName}! Total photos: ${photoCount}`);
        resetForm();
        fetchEnrolledFaces();
        fetchStats();

        // Trigger real-time reload of face recognition
        await reloadFaceRecognition();
      }
    } catch (error) {
      const errorMsg = error.response?.data?.error || 'Failed to enroll face from camera';
      showMessage('error', errorMsg);
    } finally {
      setLoading(false);
      stopCameraPreview();
    }
  };

  const handleDeleteFace = async (personId, personName) => {
    if (!window.confirm(`Are you sure you want to delete ${personName}?`)) {
      return;
    }

    try {
      const response = await axios.delete(`${API_BASE_URL}/api/faces/${personId}`);
      
      if (response.data.success) {
        showMessage('success', `Successfully deleted ${personName}`);
        fetchEnrolledFaces();
        fetchStats();
      }
    } catch (error) {
      const errorMsg = error.response?.data?.error || 'Failed to delete face';
      showMessage('error', errorMsg);
    }
  };

  const resetForm = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setPersonName('');
    setPersonNotes('');
    setCapturedImage(null);
    setShowCameraPreview(false);
    setCountdown(null);
    if (personMode === 'new') {
      setSelectedExistingPerson(null);
    }
  };

  return (
    <div className="face-management">
      <div className="face-management-header">
        <h1>👤 Face Recognition Management</h1>
        <p>Enroll and manage people for face identification</p>
      </div>

      {/* Message Display */}
      {message.text && (
        <div className={`message message-${message.type}`}>
          {message.type === 'success' ? '✅' : '❌'} {message.text}
        </div>
      )}

      {/* Statistics */}
      {stats && (
        <div className="stats-panel">
          <div className="stat-card">
            <div className="stat-value">{stats.total_persons}</div>
            <div className="stat-label">Enrolled Persons</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.total_encodings}</div>
            <div className="stat-label">Face Encodings</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.average_encodings_per_person.toFixed(1)}</div>
            <div className="stat-label">Avg Encodings/Person</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{(stats.tolerance * 100).toFixed(0)}%</div>
            <div className="stat-label">Match Tolerance</div>
          </div>
        </div>
      )}

      {/* Enrollment Section */}
      <div className="enrollment-section">
        <h2>📸 Enroll Face</h2>

        {/* Person Mode Selection */}
        <div className="person-mode-selector">
          <label className="mode-label">
            <input
              type="radio"
              value="new"
              checked={personMode === 'new'}
              onChange={(e) => setPersonMode(e.target.value)}
            />
            <span>➕ New Person</span>
          </label>
          <label className="mode-label">
            <input
              type="radio"
              value="existing"
              checked={personMode === 'existing'}
              onChange={(e) => setPersonMode(e.target.value)}
            />
            <span>📸 Add Photo to Existing Person</span>
          </label>
        </div>

        {/* Enrollment Method Selection */}
        <div className="mode-selector">
          <button
            className={`mode-btn ${enrollmentMode === 'upload' ? 'active' : ''}`}
            onClick={() => setEnrollmentMode('upload')}
          >
            📁 Upload Photo
          </button>
          <button
            className={`mode-btn ${enrollmentMode === 'capture' ? 'active' : ''}`}
            onClick={() => setEnrollmentMode('capture')}
          >
            📷 Capture from Camera
          </button>
        </div>

        <p className="help-text">
          💡 Tip: Enroll multiple photos from different angles for better recognition accuracy
        </p>

        {/* Upload Mode */}
        {enrollmentMode === 'upload' && (
          <form onSubmit={handleEnrollWithUpload} className="enrollment-form">
            {personMode === 'existing' && (
              <div className="form-group">
                <label>Select Person *</label>
                <select
                  value={selectedExistingPerson || ''}
                  onChange={(e) => setSelectedExistingPerson(parseInt(e.target.value))}
                  disabled={loading}
                  required
                >
                  <option value="">-- Select a person --</option>
                  {enrolledFaces.map((person) => (
                    <option key={person.id} value={person.id}>
                      {person.name} ({person.encoding_count} photo{person.encoding_count !== 1 ? 's' : ''})
                    </option>
                  ))}
                </select>
              </div>
            )}

            {personMode === 'new' && (
              <div className="form-group">
                <label>Name *</label>
                <input
                  type="text"
                  value={personName}
                  onChange={(e) => setPersonName(e.target.value)}
                  placeholder="Enter person's name"
                  disabled={loading}
                  required
                />
              </div>
            )}

            <div className="form-group">
              <label>Photo Upload</label>
              <input
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                disabled={loading}
              />
              {previewUrl && (
                <div className="image-preview">
                  <img src={previewUrl} alt="Preview" />
                </div>
              )}
            </div>

            <div className="form-group">
              <label>Notes (Optional)</label>
              <textarea
                value={personNotes}
                onChange={(e) => setPersonNotes(e.target.value)}
                placeholder="Add any notes about this photo (e.g., 'front view', 'with glasses')"
                disabled={loading}
                rows="3"
              />
            </div>

            <button type="submit" className="btn-primary" disabled={loading || !selectedFile}>
              {loading ? '⏳ Enrolling...' : '✅ Enroll Photo'}
            </button>
          </form>
        )}

        {/* Capture Mode */}
        {enrollmentMode === 'capture' && (
          <form onSubmit={handleEnrollWithCapture} className="enrollment-form">
            {personMode === 'existing' && (
              <div className="form-group">
                <label>Select Person *</label>
                <select
                  value={selectedExistingPerson || ''}
                  onChange={(e) => setSelectedExistingPerson(parseInt(e.target.value))}
                  disabled={loading}
                  required
                >
                  <option value="">-- Select a person --</option>
                  {enrolledFaces.map((person) => (
                    <option key={person.id} value={person.id}>
                      {person.name} ({person.encoding_count} photo{person.encoding_count !== 1 ? 's' : ''})
                    </option>
                  ))}
                </select>
              </div>
            )}

            {personMode === 'new' && (
              <div className="form-group">
                <label>Name *</label>
                <input
                  type="text"
                  value={personName}
                  onChange={(e) => setPersonName(e.target.value)}
                  placeholder="Enter person's name"
                  disabled={loading}
                  required
                />
              </div>
            )}

            <div className="form-group">
              <label>Select Camera</label>
              <select
                value={selectedCamera || ''}
                onChange={(e) => setSelectedCamera(parseInt(e.target.value))}
                disabled={loading}
              >
                {cameras.map((camera) => (
                  <option key={camera.id} value={camera.id}>
                    {camera.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Camera Preview */}
            {!showCameraPreview && !capturedImage && (
              <div className="form-group">
                <button
                  type="button"
                  className="btn-secondary"
                  onClick={startCameraPreview}
                  disabled={loading || !selectedCamera}
                >
                  🎥 Start Camera Preview
                </button>
                <p className="help-text">
                  💡 Start the camera preview to position yourself before capturing
                </p>
              </div>
            )}

            {showCameraPreview && (
              <div className="camera-preview-container">
                <div className="camera-preview">
                  <img
                    src={`${API_BASE_URL}/stream/${selectedCamera}`}
                    alt="Camera Preview"
                    className="preview-stream"
                  />
                  {countdown && (
                    <div className="countdown-overlay">
                      <div className="countdown-number">{countdown}</div>
                    </div>
                  )}
                </div>
                <div className="preview-controls">
                  <button
                    type="button"
                    className="btn-primary"
                    onClick={startCountdown}
                    disabled={countdown !== null}
                  >
                    {countdown ? '⏱️ Capturing...' : '📸 Start Countdown (3s)'}
                  </button>
                  <button
                    type="button"
                    className="btn-secondary"
                    onClick={stopCameraPreview}
                    disabled={countdown !== null}
                  >
                    ❌ Cancel
                  </button>
                </div>
              </div>
            )}

            {capturedImage && (
              <div className="captured-image-container">
                <div className="image-preview">
                  <img src={capturedImage} alt="Captured" />
                </div>
                <div className="preview-controls">
                  <button
                    type="button"
                    className="btn-secondary"
                    onClick={() => {
                      setCapturedImage(null);
                      startCameraPreview();
                    }}
                  >
                    🔄 Retake
                  </button>
                </div>
              </div>
            )}

            <div className="form-group">
              <label>Notes (Optional)</label>
              <textarea
                value={personNotes}
                onChange={(e) => setPersonNotes(e.target.value)}
                placeholder="Add any notes about this photo (e.g., 'front view', 'with glasses')"
                disabled={loading}
                rows="3"
              />
            </div>

            <button type="submit" className="btn-primary" disabled={loading || !capturedImage}>
              {loading ? '⏳ Enrolling...' : '✅ Enroll Photo'}
            </button>
          </form>
        )}
      </div>

      {/* Enrolled Faces List */}
      <div className="enrolled-faces-section">
        <h2>👥 Enrolled Persons ({enrolledFaces.length})</h2>
        
        {enrolledFaces.length === 0 ? (
          <div className="empty-state">
            <p>No persons enrolled yet. Start by enrolling someone above!</p>
          </div>
        ) : (
          <div className="faces-grid">
            {enrolledFaces.map((person) => (
              <div key={person.id} className="face-card">
                <div className="face-photo">
                  {person.photo_url ? (
                    <img src={`${API_BASE_URL}${person.photo_url}`} alt={person.name} />
                  ) : (
                    <div className="no-photo">👤</div>
                  )}
                </div>
                <div className="face-info">
                  <h3>{person.name}</h3>
                  {person.notes && <p className="notes">{person.notes}</p>}
                  <div className="face-meta">
                    <span>📸 {person.encoding_count} photo{person.encoding_count !== 1 ? 's' : ''}</span>
                    <span>📅 {new Date(person.enrolled_at).toLocaleDateString()}</span>
                  </div>
                </div>
                <div className="face-actions">
                  <button
                    className="btn-delete"
                    onClick={() => handleDeleteFace(person.id, person.name)}
                  >
                    🗑️ Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default FaceManagement;

