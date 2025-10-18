# Device Connectivity Module

This module provides connectivity to various devices including cameras, sensors, and smart home devices.

## 📁 Structure

```
device_connectivity/
├── camera/                  # Camera connectivity
│   ├── base.py             # Abstract base class for camera sources
│   ├── webcam.py           # Webcam/USB camera handler
│   ├── tapo/               # Tapo IP camera support
│   │   └── rtsp_camera.py  # RTSP stream handler
│   └── __init__.py
└── __init__.py
```

## 🎥 Camera Module

### Supported Camera Types

1. **Webcam** - Local USB/built-in cameras
2. **RTSP** - IP cameras via RTSP streams (Tapo, Hikvision, Dahua, etc.)

### Usage

#### Webcam

```python
from device_connectivity.camera import WebcamCamera

# Initialize webcam
camera = WebcamCamera(camera_index=0, width=640, height=480, fps=30)

# Initialize and read frames
if camera.initialize():
    success, frame = camera.read_frame()
    if success:
        # Process frame
        pass
    camera.release()
```

#### RTSP Camera

```python
from device_connectivity.camera import TapoRTSPCamera

# Initialize RTSP camera
camera = TapoRTSPCamera(
    rtsp_url="rtsp://username:password@192.168.0.233:554/stream1",
    reconnect_attempts=3,
    reconnect_delay=2,
    timeout=10,
    buffer_size=1
)

# Initialize and read frames
if camera.initialize():
    success, frame = camera.read_frame()
    if success:
        # Process frame
        pass
    camera.release()
```

#### Using Context Manager

```python
from device_connectivity.camera import WebcamCamera

# Automatically handles initialization and cleanup
with WebcamCamera(camera_index=0) as camera:
    success, frame = camera.read_frame()
    if success:
        # Process frame
        pass
```

### Camera Source Interface

All camera sources implement the `CameraSource` abstract base class:

**Methods:**
- `initialize()` - Initialize the camera
- `read_frame()` - Read a frame from the camera
- `release()` - Release camera resources
- `get_properties()` - Get camera properties (width, height, fps, etc.)
- `is_ready()` - Check if camera is ready

### Features

- **Unified Interface** - All camera types use the same interface
- **Auto-Reconnection** - RTSP cameras automatically reconnect on failure
- **Mirror View** - Frames are horizontally flipped for natural viewing
- **Error Handling** - Comprehensive error handling and troubleshooting
- **Context Manager** - Support for `with` statement
- **Configurable** - Flexible configuration options

## 🔧 Integration with Object Detection

The camera module is integrated with the YOLO object detection system in `object_detection/`.

See `object_detection/scripts/detect_objects.py` for usage example.

## 📚 Documentation

- [RTSP Camera Setup Guide](../object_detection/RTSP_CAMERA_SETUP.md) - Detailed RTSP setup instructions
- [Object Detection README](../object_detection/README.md) - Main project documentation

## 🚀 Future Enhancements

Potential additions:
- Support for more camera types (USB cameras, ONVIF, etc.)
- Video file input
- Network camera discovery
- Camera calibration utilities
- Multi-camera support

## 📄 License

Part of the Smart Home Automation project.

