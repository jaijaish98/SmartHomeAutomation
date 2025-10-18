# 🚀 How to Run Object Detection

## ⚡ EASIEST WAY - One Click!

### Option 1: Shell Script (macOS/Linux)
```bash
cd object_detection
./run.sh
```

### Option 2: Double-Click (macOS)
1. Open Finder
2. Navigate to `object_detection` folder
3. **Double-click** `START_OBJECT_DETECTION.command`
4. Done! 🎉

### Option 3: Python Script (All Platforms)
```bash
cd object_detection
python run.py
```

### Option 4: Windows Batch File
```bash
cd object_detection
run.bat
```

---

## 🎯 What Happens Automatically

When you run any launcher above:

1. ✅ **Checks Python** - Verifies Python 3 is installed
2. ✅ **Installs packages** - Installs OpenCV, NumPy, PyYAML (if needed)
3. ✅ **Downloads model** - Downloads YOLOv4-tiny (~23 MB) on first run only
4. ✅ **Starts detection** - Opens camera and starts detecting objects

**No manual setup needed!**

---

## 📹 Using the Application

Once running, you'll see a window with your webcam feed.

### Controls
- **'q'** or **ESC** - Quit
- **'s'** - Save current frame
- **'i'** - Show model info

### What You'll See
- 🎨 Colored boxes around detected objects
- 🏷️ Labels with object names
- 📊 Confidence scores (e.g., "person: 95%")
- 📈 FPS counter
- 🔢 Object count

---

## 🎯 Try Detecting

Point your camera at:
- 👤 Yourself (person)
- 📱 Your phone (cell phone)
- 💻 Your laptop (laptop)
- ⌨️ Keyboard
- 🖱️ Mouse
- 🍎 Food items
- 🪑 Furniture
- 🐕 Pets

---

## 🛑 To Stop

Press **'q'** or **ESC** in the detection window

---

## 📁 File Overview

| File | Purpose | How to Use |
|------|---------|------------|
| `run.sh` | Shell launcher | `./run.sh` |
| `run.py` | Python launcher | `python run.py` |
| `run.bat` | Windows launcher | `run.bat` |
| `START_OBJECT_DETECTION.command` | macOS double-click | Double-click in Finder |

**All do the same thing - pick your favorite!**

---

## 💡 Tips

### First Time Running
- Model download takes ~30 seconds (23 MB)
- Only happens once
- Subsequent runs start instantly

### Camera Permission (macOS)
If you see "not authorized to capture video":
1. System Settings → Privacy & Security → Camera
2. Enable for Terminal
3. Restart Terminal
4. Run again

### Performance
- Default model (YOLOv4-tiny) runs at 20-40 FPS on CPU
- Good lighting improves accuracy
- Hold objects steady for better detection

---

## 🔧 Troubleshooting

### "Python not found"
Install Python 3.7+ from [python.org](https://python.org)

### "Camera not accessible"
- Check camera permissions (macOS)
- Close other apps using camera
- Try different camera index in `config/config.yaml`

### "Model download failed"
- Check internet connection
- Run manually: `python scripts/download_models.py`

### Slow performance
- Use YOLOv4-tiny (default)
- Close other applications
- Reduce camera resolution in config

---

## 📚 More Information

- [README.md](README.md) - Full documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [config/config.yaml](config/config.yaml) - Configuration options

---

## 🎉 Summary

**Simplest way to run:**
```bash
./run.sh
```

**That's it!** Everything else is automatic! 🚀

