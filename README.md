# Smart Home Automation

A comprehensive smart home automation system with computer vision capabilities and IoT device integration.

---

## 📁 Project Structure

```
SmartHomeAutomation/
├── Backend/                    # Backend services and computer vision
│   ├── object_detection/       # YOLO object detection system
│   ├── device_connectivity/    # Device connectivity modules
│   └── *.md                    # Backend documentation
│
└── Frontend/                   # Frontend application (coming soon)
```

---

## 🎯 Features

### **Backend**

- ✅ **YOLO Object Detection** - Real-time object detection with 80+ object types
- ✅ **Multi-Camera Support** - Webcam, USB cameras, and RTSP IP cameras
- ✅ **Interactive Camera Selection** - Automatic camera discovery and selection
- ✅ **Device Connectivity** - Modular device integration framework
- ✅ **Smart Camera Integration** - Tapo IP camera support via RTSP

### **Frontend**

- 🚧 **Coming Soon** - Web interface for smart home control

---

## 🚀 Quick Start

### **Backend - Object Detection**

```bash
cd Backend/object_detection
./run.sh
```

This will:
1. Install dependencies
2. Download YOLO model
3. Show camera selection menu
4. Start real-time object detection

**See [Backend/README.md](Backend/README.md) for detailed documentation.**

---

## 📚 Documentation

### **Backend Documentation**

| Document | Description |
|----------|-------------|
| [Backend/README.md](Backend/README.md) | Backend overview |
| [Backend/object_detection/README.md](Backend/object_detection/README.md) | Object detection system |
| [Backend/CAMERA_SELECTION_GUIDE.md](Backend/CAMERA_SELECTION_GUIDE.md) | Camera selection guide |
| [Backend/RTSP_INTEGRATION_SUMMARY.md](Backend/RTSP_INTEGRATION_SUMMARY.md) | RTSP camera integration |
| [Backend/device_connectivity/README.md](Backend/device_connectivity/README.md) | Device connectivity module |

### **Frontend Documentation**

- 🚧 Coming soon

---

## 🛠️ Technology Stack

### **Backend**

- **Python 3.x** - Core programming language
- **OpenCV** - Computer vision library
- **YOLO (YOLOv4-tiny)** - Object detection model
- **RTSP** - IP camera streaming protocol

### **Frontend**

- 🚧 To be determined

---

## 📋 Requirements

### **Backend**

- Python 3.7+
- OpenCV (cv2)
- NumPy
- PyYAML
- Webcam or IP camera

**See [Backend/object_detection/requirements.txt](Backend/object_detection/requirements.txt) for complete list.**

---

## 🎥 Camera Support

The system supports multiple camera types:

1. **Built-in Webcam** - Laptop/desktop camera (e.g., FaceTime HD Camera)
2. **External USB Camera** - USB-connected cameras
3. **RTSP IP Cameras** - Network cameras (Tapo, Hikvision, Dahua, etc.)

**Interactive camera selection automatically detects all available cameras.**

---

## 🔧 Configuration

### **Backend Configuration**

Main configuration file: `Backend/object_detection/config/config.yaml`

**Camera Selection Mode:**
```yaml
camera_source:
  mode: "interactive"    # Shows camera selection menu
```

**See [Backend/object_detection/README.md](Backend/object_detection/README.md) for detailed configuration.**

---

## 📖 Getting Started

### **1. Clone the Repository**

```bash
git clone <repository-url>
cd SmartHomeAutomation
```

### **2. Run Backend Object Detection**

```bash
cd Backend/object_detection
./run.sh
```

### **3. Select Your Camera**

Choose from the interactive menu:
- FaceTime HD Camera (built-in)
- USB Camera (external)
- Tapo Smart Camera (RTSP)

### **4. Start Detecting Objects**

The system will detect 80+ object types in real-time!

---

## 🎯 Use Cases

- **Home Security** - Detect people and objects
- **Smart Home Automation** - Trigger actions based on detected objects
- **Pet Monitoring** - Detect cats, dogs, and other animals
- **Package Detection** - Detect deliveries
- **Vehicle Detection** - Monitor cars, bicycles, motorcycles
- **Activity Monitoring** - Track daily activities

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- **YOLO** - You Only Look Once object detection
- **OpenCV** - Open Source Computer Vision Library
- **Tapo** - TP-Link smart camera integration

---

## 📞 Support

For issues and questions:
- Check the documentation in `Backend/` folder
- Review troubleshooting guides
- Open an issue on GitHub

---

**Built with ❤️ for Smart Home Automation**

