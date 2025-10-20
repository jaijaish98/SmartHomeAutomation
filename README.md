# 🏠 Smart Home Automation

A comprehensive smart home automation system with real-time camera management, video streaming, and AI-powered object detection capabilities.

---

## 🎯 Overview

This project provides a full-stack solution for smart home camera monitoring with:
- **Real-time Video Streaming** - View multiple cameras simultaneously
- **AI Object Detection** - YOLO-based object recognition
- **Multi-Camera Support** - Webcams and RTSP/IP cameras
- **Web Interface** - Modern React-based UI
- **REST API** - Flask backend for camera control

---

## 🏗️ Architecture

```
SmartHomeAutomation/
├── Backend/              # Python backend services
│   ├── api/             # Flask REST API server
│   ├── device_connectivity/  # Camera drivers
│   ├── object_detection/     # YOLO detection
│   └── docs/            # Backend documentation
│
└── Frontend/            # React frontend application
    └── camera-viewer/   # Camera viewer web app
        └── docs/        # Frontend documentation
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 14+
- npm 6+

### Option 1: Using Shell Scripts (Recommended ⭐)

**Start the application:**
```bash
./start.sh
```

This will:
- Start the backend API server on http://localhost:5000
- Start the frontend React app on http://localhost:3000
- Create log files (backend.log and frontend.log)
- Automatically open the application in your browser

**Stop the application:**
```bash
./stop.sh
```

Or use the **🛑 Stop App** button in the UI.

### Option 2: Manual Start

**Start Backend API:**
```bash
cd Backend/api
python3 -m pip install Flask Flask-CORS
python3 app.py
```

**Start Frontend:**
```bash
cd Frontend/camera-viewer
npm install
npm start
```

**Access Application:**
Open browser to: **http://localhost:3000**

---

## 📚 Documentation Index

### 🎯 Getting Started
- **[Full Stack Setup Guide](Backend/docs/FULL_STACK_SETUP.md)** - Complete installation and setup
- **[Quick Start Guide](Frontend/camera-viewer/docs/QUICK_START.md)** - Get running in 5 minutes
- **[Frontend Setup Guide](Frontend/camera-viewer/docs/SETUP_GUIDE.md)** - Detailed frontend setup

### 🔧 Backend Documentation
- **[Backend README](Backend/README.md)** - Backend overview
- **[API Documentation](Backend/api/README.md)** - REST API reference
- **[Camera Selection Guide](Backend/docs/CAMERA_SELECTION_GUIDE.md)** - Camera configuration
- **[RTSP Integration](Backend/docs/RTSP_INTEGRATION_SUMMARY.md)** - IP camera setup
- **[Changelog](Backend/docs/CHANGELOG.md)** - Version history

### 🎨 Frontend Documentation
- **[Frontend README](Frontend/camera-viewer/README.md)** - Frontend overview
- **[Camera Viewer Summary](Backend/docs/CAMERA_VIEWER_SUMMARY.md)** - Feature overview

### 🤖 Computer Vision
- **[Computer Vision Projects](Backend/docs/COMPUTER_VISION_PROJECTS.md)** - CV capabilities
- **[Object Detection Guide](Backend/object_detection/README.md)** - YOLO setup

### 📝 Project Documentation
- **[Restructure Summary](Backend/docs/RESTRUCTURE_SUMMARY.md)** - Project organization

---

## 🎥 Features

### Camera Management
- ✅ Auto-discovery of webcams
- ✅ RTSP/IP camera support (Tapo, etc.)
- ✅ Real camera name detection (macOS)
- ✅ Multi-camera switching
- ✅ Live video streaming (MJPEG)

### Object Detection
- ✅ YOLO v3/v4 support
- ✅ Real-time object recognition
- ✅ Bounding box visualization
- ✅ Confidence scoring
- ✅ Custom object filtering

### Face Recognition 👤 (NEW!)
- ✅ Face enrollment with upload or camera capture
- ✅ Live camera preview with countdown timer
- ✅ Multiple photos per person for better accuracy
- ✅ Real-time face recognition without restart
- ✅ Person management (add, update, delete)
- ✅ Face recognition statistics

### Web Interface
- ✅ Modern React UI
- ✅ Responsive design
- ✅ Camera dropdown selector
- ✅ Live video display
- ✅ Camera statistics
- ✅ Face management interface
- ✅ Stop application button

### API
- ✅ RESTful endpoints
- ✅ Camera discovery
- ✅ Stream control
- ✅ Face recognition endpoints
- ✅ CORS enabled
- ✅ Health monitoring
- ✅ Shutdown endpoint

---

## 🛠️ Technology Stack

### Backend
- **Python 3.9+** - Core language
- **Flask** - Web framework
- **OpenCV** - Computer vision
- **YOLO** - Object detection
- **NumPy** - Numerical computing

### Frontend
- **React 18** - UI framework
- **Axios** - HTTP client
- **CSS3** - Styling
- **Webpack** - Bundling

---

## 📖 API Reference

### Camera Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cameras` | List all cameras |
| POST | `/api/cameras/:id/open` | Open camera |
| POST | `/api/cameras/:id/close` | Close camera |
| GET | `/stream/:id` | Video stream |

### Face Recognition Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/faces` | List all enrolled persons |
| POST | `/api/faces/enroll` | Enroll face from upload |
| POST | `/api/faces/enroll/capture` | Enroll face from camera |
| GET | `/api/faces/:id` | Get person details |
| PUT | `/api/faces/:id` | Update person info |
| DELETE | `/api/faces/:id` | Delete person |
| POST | `/api/faces/reload` | Reload face recognition |
| GET | `/api/faces/stats` | Get statistics |

### System Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/shutdown` | Shutdown server |

See [API Documentation](Backend/api/README.md) for details.

---

**Smart Home Automation - Making homes smarter, one camera at a time** 🏠📹
