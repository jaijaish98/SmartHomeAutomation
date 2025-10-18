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

### Start Backend API
```bash
cd Backend/api
python3 -m pip install Flask Flask-CORS
python3 app.py
```

### Start Frontend
```bash
cd Frontend/camera-viewer
npm install
npm start
```

### Access Application
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

### Web Interface
- ✅ Modern React UI
- ✅ Responsive design
- ✅ Camera dropdown selector
- ✅ Live video display
- ✅ Camera statistics

### API
- ✅ RESTful endpoints
- ✅ Camera discovery
- ✅ Stream control
- ✅ CORS enabled
- ✅ Health monitoring

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

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cameras` | List all cameras |
| POST | `/api/cameras/:id/open` | Open camera |
| POST | `/api/cameras/:id/close` | Close camera |
| GET | `/stream/:id` | Video stream |
| GET | `/health` | Health check |

See [API Documentation](Backend/api/README.md) for details.

---

**Smart Home Automation - Making homes smarter, one camera at a time** 🏠📹
