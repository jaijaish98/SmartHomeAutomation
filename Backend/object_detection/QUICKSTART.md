# Quick Start Guide

Get started with YOLO object detection in **ONE CLICK**! 🚀

## ⚡ One-Click Launch

### macOS/Linux
```bash
cd object_detection
./run.sh
```

### macOS (Double-Click)
Just **double-click** `START_OBJECT_DETECTION.command` in Finder!

### Windows
```bash
cd object_detection
run.bat
```

### Cross-Platform (Python)
```bash
cd object_detection
python run.py
```

**That's it!** 🎉 The launcher does everything automatically!

---

## 📋 What the Launcher Does

1. ✅ Checks Python installation
2. ✅ Installs dependencies (if needed)
3. ✅ Downloads YOLO model (first time only, ~23 MB)
4. ✅ Launches object detection

**No manual setup required!**

## 🎮 Using the Application

Once running, you'll see a window with your webcam feed and detected objects highlighted with colored bounding boxes.

**Controls:**
- Press **'q'** or **ESC** to quit
- Press **'s'** to save the current frame
- Press **'i'** to show model info

## 📸 What You'll See

- **Colored boxes** around detected objects
- **Labels** showing object type and confidence
- **Object count** in the top-left corner
- **FPS counter** showing performance

## 🎯 Example Detections

The system can detect:
- 👤 **People** in the frame
- 📱 **Cell phones** and laptops
- 🐕 **Pets** (dogs, cats, birds)
- 🚗 **Vehicles** (cars, bikes, trucks)
- 🪑 **Furniture** (chairs, tables, couches)
- And **70+ more objects!**

## ⚙️ Quick Configuration

Edit `config/config.yaml` to customize:

**Change detection sensitivity:**
```yaml
model:
  confidence_threshold: 0.5  # Lower = more detections, Higher = fewer false positives
```

**Filter specific objects only:**
```yaml
filter:
  enabled: true
  classes:
    - person
    - dog
    - cell phone
```

**Change camera:**
```yaml
camera:
  index: 0  # Try 0, 1, 2 for different cameras
```

## 🔧 Troubleshooting

### Camera Permission (macOS)
If you see "not authorized to capture video":
1. System Settings → Privacy & Security → Camera
2. Enable for Terminal
3. Restart Terminal

### Model Not Found
If you see "Failed to load model":
```bash
python scripts/download_models.py
```

### Slow Performance
Try the faster tiny model in `config/config.yaml`:
```yaml
model:
  type: "yolov4-tiny"
```

## 📚 Learn More

See [README.md](README.md) for complete documentation.

## 🎓 Next Steps

1. **Experiment** with different objects
2. **Adjust** confidence threshold for better results
3. **Try** different YOLO models (yolov3, yolov4)
4. **Save** interesting detections with 's' key
5. **Filter** to detect only specific objects

Happy detecting! 🎉

