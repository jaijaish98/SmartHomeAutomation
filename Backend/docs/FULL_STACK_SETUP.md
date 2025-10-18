# 🚀 Full Stack Camera Viewer - Complete Setup Guide

Complete guide to running the Smart Home Camera Viewer with Backend API and Frontend React app.

---

## 🎯 System Overview

### **Architecture**

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│                  http://localhost:3000                   │
│  - Camera selection dropdown                             │
│  - Open/Close camera controls                            │
│  - Live video streaming display                          │
└──────────────────┬──────────────────────────────────────┘
                   │ REST API Calls
                   │ (axios)
┌──────────────────▼──────────────────────────────────────┐
│                 Backend API (Flask)                      │
│                  http://localhost:5000                   │
│  - GET /api/cameras - List cameras                       │
│  - POST /api/cameras/:id/open - Open camera              │
│  - POST /api/cameras/:id/close - Close camera            │
│  - GET /stream/:id - MJPEG video stream                  │
└──────────────────┬──────────────────────────────────────┘
                   │ Camera Access
                   │ (OpenCV)
┌──────────────────▼──────────────────────────────────────┐
│                    Cameras                               │
│  - FaceTime HD Camera (Webcam)                           │
│  - USB Camera (Webcam)                                   │
│  - Tapo Smart Camera (RTSP)                              │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Prerequisites

### **Required Software**

1. **Python 3.9+** - [Download](https://www.python.org/)
2. **Node.js 14+** - [Download](https://nodejs.org/)
3. **npm** (comes with Node.js)

### **Check Installation**

```bash
python3 --version   # Should be 3.9 or higher
node --version      # Should be 14 or higher
npm --version       # Should be 6 or higher
```

---

## 🚀 Quick Start (Two Terminals)

### **Terminal 1: Start Backend API**

```bash
cd Backend/api
python3 -m pip install Flask Flask-CORS
python3 app.py
```

**Expected Output:**
```
🚀 Smart Home Camera API Server
📡 Server starting on http://localhost:5000
✅ Found 2 camera(s)
   - FaceTime HD Camera (webcam)
   - USB Camera (webcam)
```

### **Terminal 2: Start Frontend**

```bash
cd Frontend/camera-viewer
npm start
```

**Expected Output:**
```
Compiled successfully!
You can now view camera-viewer in the browser.
  Local: http://localhost:3000
```

### **Access the Application**

Open browser to: **http://localhost:3000**

---

## 📁 Project Structure

```
SmartHomeAutomation/
├── Backend/
│   ├── api/                          # Flask API Server
│   │   ├── app.py                    # Main Flask app
│   │   ├── routes/
│   │   │   ├── camera_routes.py      # Camera API endpoints
│   │   │   └── stream_routes.py      # Video streaming endpoints
│   │   ├── services/
│   │   │   └── camera_manager.py     # Camera management service
│   │   ├── requirements.txt          # Python dependencies
│   │   └── start_api.sh              # Start script
│   │
│   ├── device_connectivity/          # Camera connectivity modules
│   │   └── camera/
│   │       ├── discovery.py          # Camera discovery
│   │       ├── webcam.py             # Webcam handler
│   │       └── tapo/
│   │           └── rtsp_camera.py    # RTSP camera handler
│   │
│   └── object_detection/             # YOLO object detection
│       └── config/
│           └── config.yaml           # Configuration
│
└── Frontend/
    └── camera-viewer/                # React application
        ├── src/
        │   ├── components/
        │   │   ├── CameraSelector.js # Dropdown component
        │   │   └── CameraViewer.js   # Viewer component
        │   ├── services/
        │   │   └── cameraService.js  # API service
        │   └── App.js                # Main app
        ├── package.json              # Dependencies
        └── start.sh                  # Start script
```

---

## 🔌 API Endpoints

### **Camera Management**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cameras` | List all available cameras |
| GET | `/api/cameras/:id` | Get specific camera info |
| POST | `/api/cameras/:id/open` | Open camera and start streaming |
| POST | `/api/cameras/:id/close` | Close camera and stop streaming |
| GET | `/api/cameras/active` | List currently active cameras |

### **Video Streaming**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/stream/:id` | MJPEG video stream |
| GET | `/stream/:id/snapshot` | Single frame snapshot |

### **System**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |

---

## 🎮 How to Use

### **Step 1: Start Both Servers**

1. Start backend API (Terminal 1)
2. Start frontend React app (Terminal 2)

### **Step 2: Open Application**

Navigate to http://localhost:3000 in your browser

### **Step 3: Select Camera**

1. Click the dropdown menu
2. Choose a camera (FaceTime HD, USB Camera, etc.)
3. Camera details will appear below

### **Step 4: Open Camera**

1. Click the "▶️ Open Camera" button
2. Wait for camera to initialize
3. Live video stream will appear

### **Step 5: View Stream**

- See live video feed
- 🔴 LIVE indicator shows active status
- Camera statistics displayed below

### **Step 6: Close Camera**

1. Click the "⏹️ Close Camera" button
2. Stream will stop
3. Ready to select another camera

---

## 🔧 Configuration

### **Backend Configuration**

Edit `Backend/object_detection/config/config.yaml`:

```yaml
camera:
  mode: 'interactive'  # or 'auto'
  default_index: 0

rtsp:
  url: 'rtsp://192.168.0.233:554/stream1'
  username: 'your_username'
  password: 'your_password'
```

### **Frontend Configuration**

Edit `Frontend/camera-viewer/src/services/cameraService.js`:

```javascript
const API_BASE_URL = 'http://localhost:5000/api';
const STREAM_BASE_URL = 'http://localhost:5000/stream';
```

---

## 🐛 Troubleshooting

### **Backend Issues**

#### Problem: "Module not found: Flask"
**Solution:**
```bash
cd Backend/api
python3 -m pip install Flask Flask-CORS
```

#### Problem: "Port 5000 already in use"
**Solution:**
```bash
# Find and kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

#### Problem: "No cameras found"
**Solution:**
- Check camera permissions
- Verify cameras are connected
- Check config.yaml for RTSP settings

### **Frontend Issues**

#### Problem: "Cannot connect to backend"
**Solution:**
- Verify backend is running on port 5000
- Check browser console for CORS errors
- Ensure both servers are running

#### Problem: "Video stream not displaying"
**Solution:**
- Open camera first using "Open Camera" button
- Check browser console for errors
- Verify camera is active in backend

---

## 📊 Testing the API

### **Using curl**

```bash
# List cameras
curl http://localhost:5000/api/cameras

# Open camera 1
curl -X POST http://localhost:5000/api/cameras/1/open

# Check health
curl http://localhost:5000/health

# Close camera 1
curl -X POST http://localhost:5000/api/cameras/1/close
```

### **Using Browser**

- API Root: http://localhost:5000
- Camera List: http://localhost:5000/api/cameras
- Health Check: http://localhost:5000/health

---

## 🔒 Security Notes

### **Development Mode**

- Backend runs in debug mode (not for production)
- CORS enabled for localhost only
- No authentication required

### **Production Deployment**

For production, you should:
1. Disable Flask debug mode
2. Use production WSGI server (gunicorn, uwsgi)
3. Add authentication/authorization
4. Use HTTPS
5. Restrict CORS origins
6. Secure credentials in environment variables

---

## 🚀 Advanced Usage

### **Running on Different Ports**

**Backend:**
```python
# Edit Backend/api/app.py
app.run(host='0.0.0.0', port=8000, debug=True)
```

**Frontend:**
```bash
PORT=3001 npm start
```

### **Adding More Cameras**

1. Connect camera to device
2. Restart backend API
3. Camera will auto-discover
4. Refresh frontend to see new camera

---

## 📚 Documentation

- [Backend API README](Backend/api/README.md)
- [Frontend README](Frontend/camera-viewer/README.md)
- [Camera Setup Guide](Frontend/camera-viewer/SETUP_GUIDE.md)
- [Quick Start](Frontend/camera-viewer/QUICK_START.md)

---

## ✅ Success Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 14+ installed
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Backend running on port 5000
- [ ] Frontend running on port 3000
- [ ] Can access http://localhost:3000
- [ ] Can see camera list in dropdown
- [ ] Can open camera successfully
- [ ] Can see live video stream
- [ ] Can close camera successfully

---

## 🎉 You're All Set!

**Both servers are running:**
- ✅ Backend API: http://localhost:5000
- ✅ Frontend App: http://localhost:3000

**Try it now:**
1. Open http://localhost:3000
2. Select a camera
3. Click "Open Camera"
4. Watch the live stream!

---

**Smart Home Automation © 2024**

