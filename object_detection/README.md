# YOLO Real-time Object Detection

A professional, well-structured Python application for real-time object detection using YOLO (You Only Look Once) and OpenCV. Detects 80+ object types from your **webcam or RTSP IP camera** with high accuracy and performance.

**Note:** This system detects people (which includes faces), vehicles, animals, electronics, and many more objects - making it far more versatile than simple face-only detection systems.

**NEW:** Now supports RTSP IP cameras (Tapo, Hikvision, Dahua, etc.) in addition to webcams! See [RTSP Camera Setup Guide](RTSP_CAMERA_SETUP.md).

## 🎯 Features

- ✅ **80+ Object Types** - Detects people, vehicles, animals, everyday objects, and more
- ✅ **Interactive Camera Selection** - Automatically detects and lists all available cameras
- ✅ **Multiple Camera Sources** - Built-in webcam, external USB cameras, and RTSP IP cameras
- ✅ **Real-time Performance** - Fast detection with FPS monitoring
- ✅ **High Accuracy** - YOLO deep learning model (90-95% accuracy)
- ✅ **Color-coded Bounding Boxes** - Each object type has a unique color
- ✅ **Natural Mirror View** - Webcams are flipped for natural viewing (RTSP cameras show original orientation)
- ✅ **Auto-Reconnection** - RTSP streams automatically reconnect on failure
- ✅ **Confidence Scores** - Shows detection confidence for each object
- ✅ **Object Counting** - Real-time count of detected objects
- ✅ **Frame Saving** - Save detection results with one keypress
- ✅ **Configurable** - Easy YAML-based configuration
- ✅ **Modular Design** - Clean, professional code structure
- ✅ **Multiple YOLO Models** - Support for YOLOv3, YOLOv4, and tiny versions

## 📋 Detectable Objects (80 COCO Classes)

**People & Animals:**
- person (includes face detection as part of person detection), dog, cat, bird, horse, sheep, cow, elephant, bear, zebra, giraffe

**Vehicles:**
- bicycle, car, motorcycle, airplane, bus, train, truck, boat

**Everyday Objects:**
- cell phone, laptop, keyboard, mouse, remote, bottle, cup, fork, knife, spoon

**Furniture & Appliances:**
- chair, couch, bed, dining table, toilet, tv, microwave, oven, refrigerator

**Sports & Recreation:**
- frisbee, skis, snowboard, sports ball, kite, baseball bat, skateboard, surfboard

**And 40+ more objects!**

## 📁 Project Structure

```
object_detection/
├── config/
│   └── config.yaml           # Configuration file (camera, model, display settings)
├── models/                   # YOLO model files (auto-downloaded)
│   ├── yolov4-tiny.weights
│   ├── yolov4-tiny.cfg
│   └── coco.names
├── src/                      # Source code modules
│   ├── detector.py           # Core ObjectDetector class
│   ├── camera.py             # Camera handling utilities
│   └── visualizer.py         # Visualization utilities
├── scripts/                  # Executable scripts
│   ├── download_models.py    # Download YOLO models
│   ├── detect_objects.py     # Main detection application
│   └── test_setup.py         # Test installation
├── output/                   # Saved frames (auto-created)
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🚀 Quick Start

### ⚡ One-Click Launch (Easiest!)

**macOS/Linux:**
```bash
cd object_detection
./run.sh
```

**Or double-click** `START_OBJECT_DETECTION.command` in Finder (macOS)

**Windows:**
```bash
cd object_detection
run.bat
```

**Or use Python (cross-platform):**
```bash
cd object_detection
python run.py
```

That's it! The launcher automatically:
- ✅ Checks dependencies
- ✅ Downloads model (first time only)
- ✅ Shows camera selection menu
- ✅ Launches object detection

### 📹 Camera Selection

When you run the application, you'll see an interactive menu listing all available cameras:

```
======================================================================
📹 Available Cameras
======================================================================

1. 🎥 Webcam - FaceTime HD Camera
   Resolution: 1920x1080
   FPS: 30
   Device Index: 0

2. 🎥 Webcam - USB Camera
   Resolution: 1920x1080
   FPS: 30
   Device Index: 1

3. 📹 RTSP - Tapo Smart Camera
   Resolution: Variable
   FPS: Variable

======================================================================

📌 Select a camera (1-3) or 'q' to quit:
```

**Simply enter the number of the camera you want to use!**

The system automatically detects:
- 🎥 **Built-in webcams** (laptop camera)
- 🎥 **External USB cameras** (connected via USB)
- 📹 **RTSP IP cameras** (configured in credentials.yaml)

---

### 📋 Manual Setup (Advanced)

If you prefer step-by-step:

**1. Install Dependencies**
```bash
cd object_detection
pip install -r requirements.txt
```

**2. Download YOLO Model**
```bash
python scripts/download_models.py
```

**3. Test Setup (Optional)**
```bash
python scripts/test_setup.py
```

**4. Run Object Detection**
```bash
python scripts/detect_objects.py
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| **q** or **ESC** | Exit the application |
| **s** | Save current frame with detections |
| **i** | Show model information in console |

## ⚙️ Configuration

Edit `config/config.yaml` to customize settings:

### Camera Source Selection

**Interactive Mode (Default - Recommended):**

The application will automatically detect and list all available cameras:

```yaml
camera_source:
  mode: "interactive"    # Shows camera selection menu
```

**Auto Mode (Skip Menu):**

Automatically use a specific camera type:

```yaml
camera_source:
  mode: "auto"           # Skip menu, use type below
  type: "webcam"         # Options: "webcam" or "rtsp"
```

### Webcam Settings

```yaml
webcam:
  index: 0          # Camera device (0 = default)
  width: 640        # Frame width (0 = default)
  height: 480       # Frame height (0 = default)
  fps: 30           # Target FPS (0 = default)
```

### RTSP Camera Settings

For IP cameras (Tapo, Hikvision, etc.):

```yaml
rtsp:
  url: ""                     # RTSP URL (or use credentials.yaml)
  reconnect_attempts: 3       # Reconnection attempts
  reconnect_delay: 2          # Delay between reconnections (seconds)
  timeout: 10                 # Connection timeout (seconds)
  buffer_size: 1              # Frame buffer (1 = latest frame)
```

**📖 See [RTSP Camera Setup Guide](RTSP_CAMERA_SETUP.md) for detailed instructions**

### Model Settings
```yaml
model:
  type: "yolov4-tiny"           # yolov3, yolov3-tiny, yolov4, yolov4-tiny
  confidence_threshold: 0.5     # Min confidence (0.0-1.0)
  nms_threshold: 0.4            # Non-max suppression
  input_size: 416               # YOLO input size (320, 416, 608)
```

### Display Settings
```yaml
display:
  show_fps: true                # Show FPS counter
  show_count: true              # Show object count
  show_confidence: true         # Show confidence scores
  box_thickness: 2              # Bounding box thickness
```

### Object Filtering (Optional)
```yaml
filter:
  enabled: true                 # Enable filtering
  classes:                      # Only detect these
    - person
    - car
    - dog
    - cell phone
```

## 🎨 Available YOLO Models

| Model | Size | Speed | Accuracy | Best For |
|-------|------|-------|----------|----------|
| **yolov4-tiny** | ~23 MB | ⚡⚡⚡ Very Fast | ⭐⭐⭐ Good | Real-time, CPU |
| **yolov3-tiny** | ~34 MB | ⚡⚡⚡ Very Fast | ⭐⭐ OK | Real-time, CPU |
| **yolov4** | ~245 MB | ⚡⚡ Medium | ⭐⭐⭐⭐⭐ Excellent | High accuracy |
| **yolov3** | ~236 MB | ⚡⚡ Medium | ⭐⭐⭐⭐ Great | Balanced |

**Recommendation:** Start with `yolov4-tiny` for best speed/accuracy balance on CPU.

To change models:
1. Edit `config/config.yaml` and set `model.type`
2. Run `python scripts/download_models.py` to download the new model

## 🔧 Troubleshooting

### Camera Not Accessible (macOS)

**Error:** "OpenCV: not authorized to capture video"

**Solution:**
1. Open **System Settings** → **Privacy & Security** → **Camera**
2. Enable camera access for **Terminal** (or your IDE)
3. Restart Terminal and try again

### Model Files Not Found

**Error:** "Failed to load model"

**Solution:**
```bash
python scripts/download_models.py
```

### Low FPS / Slow Performance

**Solutions:**
- Use `yolov4-tiny` or `yolov3-tiny` (faster models)
- Reduce `input_size` in config (e.g., 320 instead of 416)
- Lower camera resolution in config
- Close other resource-intensive applications

### Import Errors

**Error:** "ModuleNotFoundError: No module named 'cv2'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Detection Not Accurate

**Solutions:**
- Increase `confidence_threshold` (fewer false positives)
- Decrease `confidence_threshold` (more detections)
- Use a larger model (yolov4 instead of yolov4-tiny)
- Ensure good lighting conditions
- Increase `input_size` for better accuracy

## 📊 Performance Tips

1. **For Maximum Speed:**
   - Use `yolov4-tiny`
   - Set `input_size: 320`
   - Reduce camera resolution

2. **For Maximum Accuracy:**
   - Use `yolov4`
   - Set `input_size: 608`
   - Increase camera resolution

3. **For Balanced Performance:**
   - Use `yolov4-tiny` (default)
   - Set `input_size: 416`
   - Use default camera resolution

## 🎓 How It Works

1. **Model Loading:** Loads pre-trained YOLO model (trained on COCO dataset)
2. **Frame Capture:** Captures video frames from webcam
3. **Preprocessing:** Resizes and normalizes frames for YOLO input
4. **Detection:** Runs YOLO neural network to detect objects
5. **Post-processing:** Applies Non-Maximum Suppression to remove duplicates
6. **Visualization:** Draws bounding boxes and labels on frame
7. **Display:** Shows processed frame with detections

## 🆚 Comparison with Face Detection

| Feature | Face Detection (Haar) | Object Detection (YOLO) |
|---------|----------------------|------------------------|
| **Objects** | Only faces | 80+ types |
| **Accuracy** | 70-80% | 90-95% |
| **Technology** | Classical ML (2001) | Deep Learning (2015+) |
| **Speed** | Very Fast | Fast |
| **Model Size** | <1 MB | 23-245 MB |
| **Use Case** | Face-specific | General purpose |

## 📝 Code Architecture

### Modular Design

- **`detector.py`** - Core YOLO detection logic
- **`camera.py`** - Camera initialization and frame capture
- **`visualizer.py`** - Drawing bounding boxes and overlays
- **`detect_objects.py`** - Main application orchestration

### Benefits

- ✅ **Separation of Concerns** - Each module has a single responsibility
- ✅ **Reusability** - Modules can be used independently
- ✅ **Testability** - Easy to test individual components
- ✅ **Maintainability** - Clean, organized code structure
- ✅ **Extensibility** - Easy to add new features

## 🔮 Future Enhancements

Potential additions:
- Video file input (not just webcam)
- Object tracking across frames
- Custom object training
- Multi-camera support
- Web interface
- Mobile app integration

## 📚 Resources

- [YOLO Official Paper](https://arxiv.org/abs/1506.02640)
- [OpenCV Documentation](https://docs.opencv.org/)
- [COCO Dataset](https://cocodataset.org/)

## 📄 License

This project is open-source and available for educational and personal use.

## 🙏 Credits

- **YOLO** - Joseph Redmon et al.
- **OpenCV** - Open Source Computer Vision Library
- **COCO Dataset** - Microsoft COCO: Common Objects in Context

---

**Built with ❤️ using YOLO and OpenCV**

