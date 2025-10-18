# 📡 Smart Home Camera API

Flask REST API for camera management and video streaming.

---

## 🎯 Overview

This API provides endpoints for:
- **Camera Discovery** - Automatically detect available cameras
- **Camera Control** - Open and close cameras
- **Video Streaming** - MJPEG streaming from cameras
- **Camera Management** - Track active camera sessions

---

## 🚀 Quick Start

### **Install Dependencies**

```bash
pip install Flask Flask-CORS
```

### **Start Server**

```bash
python3 app.py
```

**Server will start on:** http://localhost:5000

---

## 📋 API Endpoints

### **Camera Management**

#### **GET /api/cameras**
List all available cameras

**Response:**
```json
{
  "success": true,
  "count": 2,
  "cameras": [
    {
      "id": 1,
      "name": "FaceTime HD Camera",
      "type": "webcam",
      "index": 0,
      "resolution": "1920x1080",
      "fps": 30,
      "available": true
    },
    {
      "id": 2,
      "name": "USB Camera",
      "type": "webcam",
      "index": 1,
      "resolution": "1920x1080",
      "fps": 30,
      "available": true
    }
  ]
}
```

#### **POST /api/cameras/:id/open**
Open camera and start streaming

**Response:**
```json
{
  "success": true,
  "message": "Camera opened successfully",
  "camera": { ... },
  "stream_url": "/stream/1"
}
```

#### **POST /api/cameras/:id/close**
Close camera and stop streaming

**Response:**
```json
{
  "success": true,
  "message": "Camera closed successfully"
}
```

### **Video Streaming**

#### **GET /stream/:id**
MJPEG video stream from camera

**Content-Type:** `multipart/x-mixed-replace; boundary=frame`

**Usage:**
```html
<img src="http://localhost:5000/stream/1" />
```

#### **GET /stream/:id/snapshot**
Get single frame snapshot

**Content-Type:** `image/jpeg`

---

## 🏗️ Architecture

### **Components**

```
app.py
├── CameraManager (services/camera_manager.py)
│   ├── Camera Discovery
│   ├── Camera Instances
│   └── Frame Management
│
├── Camera Routes (routes/camera_routes.py)
│   ├── GET /api/cameras
│   ├── POST /api/cameras/:id/open
│   └── POST /api/cameras/:id/close
│
└── Stream Routes (routes/stream_routes.py)
    ├── GET /stream/:id
    └── GET /stream/:id/snapshot
```

### **Camera Manager**

Manages camera lifecycle:
- Discovers available cameras
- Opens/closes camera connections
- Provides thread-safe frame access
- Tracks active camera sessions

---

## 🔧 Configuration

### **CORS Settings**

Edit `app.py`:
```python
CORS(app, resources={
    r"/api/*": {"origins": ["http://localhost:3000"]},
    r"/stream/*": {"origins": ["http://localhost:3000"]}
})
```

### **Server Settings**

```python
app.run(
    host='0.0.0.0',  # Listen on all interfaces
    port=5000,        # Port number
    debug=True,       # Debug mode
    threaded=True     # Multi-threaded
)
```

---

## 📊 Camera Types

### **Webcam**
- Built-in laptop cameras
- USB cameras
- Accessed via OpenCV VideoCapture

### **RTSP**
- IP cameras (Tapo, etc.)
- Network cameras
- Accessed via RTSP URL

---

## 🔒 Security

### **Current (Development)**
- No authentication
- CORS enabled for localhost
- Debug mode enabled

### **Production Recommendations**
- Add API key authentication
- Use HTTPS
- Restrict CORS origins
- Disable debug mode
- Use production WSGI server (gunicorn)
- Rate limiting
- Input validation

---

## 🐛 Error Handling

All endpoints return consistent error format:

```json
{
  "success": false,
  "error": "Error message here"
}
```

**HTTP Status Codes:**
- `200` - Success
- `400` - Bad request
- `404` - Not found
- `500` - Server error

---

## 📝 Example Usage

### **Python**

```python
import requests

# List cameras
response = requests.get('http://localhost:5000/api/cameras')
cameras = response.json()['cameras']

# Open camera
response = requests.post('http://localhost:5000/api/cameras/1/open')
print(response.json())

# Close camera
response = requests.post('http://localhost:5000/api/cameras/1/close')
```

### **JavaScript**

```javascript
// List cameras
const response = await fetch('http://localhost:5000/api/cameras');
const data = await response.json();
console.log(data.cameras);

// Open camera
await fetch('http://localhost:5000/api/cameras/1/open', {
  method: 'POST'
});

// Display stream
<img src="http://localhost:5000/stream/1" />
```

### **curl**

```bash
# List cameras
curl http://localhost:5000/api/cameras

# Open camera
curl -X POST http://localhost:5000/api/cameras/1/open

# Close camera
curl -X POST http://localhost:5000/api/cameras/1/close
```

---

## 🔍 Debugging

### **Enable Verbose Logging**

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### **Check Active Cameras**

```bash
curl http://localhost:5000/api/cameras/active
```

### **Health Check**

```bash
curl http://localhost:5000/health
```

---

## 📦 Dependencies

```
Flask==3.0.0
Flask-CORS==4.0.0
opencv-python==4.8.1.78
numpy==1.24.3
PyYAML==6.0.1
```

---

## 🚀 Deployment

### **Development**

```bash
python3 app.py
```

### **Production (gunicorn)**

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📚 Related Documentation

- [Full Stack Setup Guide](../../FULL_STACK_SETUP.md)
- [Frontend Documentation](../../Frontend/camera-viewer/README.md)
- [Camera Discovery](../device_connectivity/camera/discovery.py)

---

**Smart Home Camera API - Ready to serve!** 🚀

