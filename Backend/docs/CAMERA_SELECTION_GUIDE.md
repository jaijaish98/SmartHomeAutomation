# Camera Selection Guide

## 🎥 Interactive Camera Selection

The YOLO object detection system now features **automatic camera discovery** and an **interactive selection menu** that makes it easy to choose between multiple cameras.

---

## ✨ What's New

### **Before (Manual Configuration)**
```yaml
# Had to manually edit config.yaml
camera_source:
  type: "webcam"  # or "rtsp"
```

### **After (Interactive Selection)**
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

**Just enter the number!** No more manual configuration needed.

---

## 🎯 Features

### **Automatic Camera Discovery**

The system automatically detects:

1. **🎥 Built-in Webcam** - Your laptop's integrated camera
2. **🎥 External USB Cameras** - Any USB cameras connected to your computer
3. **📹 RTSP IP Cameras** - Network cameras configured in `credentials.yaml`

### **Camera Information Display**

For each camera, you'll see:
- **Name** - Descriptive name (Built-in, External, Tapo, etc.)
- **Type** - Webcam or RTSP
- **Resolution** - Frame dimensions
- **FPS** - Frames per second
- **Device Index** - For webcams only

### **Smart Mirroring**

- **Webcams** - Horizontally flipped for natural mirror view (like looking in a mirror)
- **RTSP Cameras** - Original orientation (no flip, as IP cameras are usually mounted)

---

## 🚀 How to Use

### **1. Run the Application**

```bash
cd object_detection
./run.sh
```

Or:
```bash
python scripts/detect_objects.py
```

### **2. Select Your Camera**

When the menu appears, enter the number of the camera you want to use:

```
📌 Select a camera (1-3) or 'q' to quit: 2
```

Press **Enter**.

### **3. Start Detecting!**

The application will:
- ✅ Initialize the selected camera
- ✅ Start object detection
- ✅ Display real-time results

---

## ⚙️ Configuration Modes

### **Interactive Mode (Default - Recommended)**

Shows the camera selection menu every time:

```yaml
# config/config.yaml
camera_source:
  mode: "interactive"
```

**Pros:**
- ✅ Easy to switch between cameras
- ✅ See all available cameras
- ✅ No manual configuration needed

**Cons:**
- ⚠️ Requires user input each time

---

### **Auto Mode (Skip Menu)**

Automatically uses a specific camera type:

```yaml
# config/config.yaml
camera_source:
  mode: "auto"
  type: "webcam"  # or "rtsp"
```

**Pros:**
- ✅ No user input required
- ✅ Faster startup
- ✅ Good for automation/scripts

**Cons:**
- ⚠️ Can't easily switch cameras
- ⚠️ Need to edit config to change camera

---

## 📹 Camera Types

### **1. Built-in Webcam**

**Typical Specs:**
- Resolution: 1280x720 or 1920x1080
- FPS: 30
- Device Index: 0

**Best For:**
- Quick testing
- Personal use
- Portable setups

---

### **2. External USB Camera**

**Typical Specs:**
- Resolution: 1920x1080 or higher
- FPS: 15-60
- Device Index: 1, 2, 3, etc.

**Best For:**
- Better image quality
- Adjustable positioning
- Multiple camera setups

---

### **3. RTSP IP Camera (Tapo, Hikvision, etc.)**

**Typical Specs:**
- Resolution: 1280x720 to 3840x2160 (4K)
- FPS: 15-30
- Network-based

**Best For:**
- Fixed installations
- Remote monitoring
- Professional setups
- Outdoor use

**Setup Required:**
1. Configure RTSP URL in `config/credentials.yaml`
2. Ensure camera is on the same network
3. Enable RTSP in camera settings

See [RTSP_CAMERA_SETUP.md](object_detection/RTSP_CAMERA_SETUP.md) for details.

---

## 🔧 Troubleshooting

### **No Cameras Found**

**Problem:**
```
❌ No cameras found!
```

**Solutions:**

1. **Check Camera Connections**
   - Ensure webcams are plugged in
   - Check USB connections
   - Verify RTSP camera is powered on

2. **Check Permissions (macOS)**
   - Go to: System Settings → Privacy & Security → Camera
   - Enable camera access for Terminal/Python

3. **Check RTSP Configuration**
   - Verify `credentials.yaml` has correct RTSP URL
   - Test RTSP URL in VLC player
   - Ensure camera is on the network

---

### **Camera Not Detected**

**Problem:**
Camera is connected but not showing in the list.

**Solutions:**

1. **Webcam:**
   - Try unplugging and replugging
   - Check if another app is using the camera
   - Restart your computer

2. **RTSP Camera:**
   - Verify RTSP is enabled in camera settings
   - Check network connectivity: `ping <camera-ip>`
   - Test URL in VLC: Media → Open Network Stream

---

### **Camera Initialization Failed**

**Problem:**
```
❌ Failed to initialize camera
```

**Solutions:**

1. **Close Other Apps**
   - Close Zoom, Skype, FaceTime, etc.
   - Only one app can use a webcam at a time

2. **Check Camera Settings**
   - Verify resolution and FPS are supported
   - Try default settings (width=0, height=0, fps=0)

3. **RTSP Issues**
   - Check credentials are correct
   - Verify network connection
   - Try increasing timeout in config.yaml

---

## 💡 Tips & Best Practices

### **Choosing the Right Camera**

**For Testing:**
- Use built-in webcam (fastest setup)

**For Better Quality:**
- Use external USB camera (better resolution/FPS)

**For Fixed Installation:**
- Use RTSP IP camera (professional, remote access)

---

### **Performance Optimization**

**Webcam:**
- Lower resolution = faster processing
- 640x480 is good for real-time detection
- 1920x1080 for better quality (slower)

**RTSP:**
- Use `stream2` for lower quality/faster speed
- Set `buffer_size: 1` to reduce lag
- Ensure good network connection

---

### **Multiple Cameras**

**Switching Cameras:**
1. Press 'q' to exit current session
2. Run the application again
3. Select a different camera

**Using Multiple Cameras Simultaneously:**
- Currently not supported
- Run multiple instances with different configs
- Set `mode: "auto"` and different `type` for each

---

## 📚 Related Documentation

- **[README.md](object_detection/README.md)** - Main project documentation
- **[RTSP_CAMERA_SETUP.md](object_detection/RTSP_CAMERA_SETUP.md)** - RTSP camera setup guide
- **[device_connectivity/README.md](device_connectivity/README.md)** - Camera module documentation

---

## 🎉 Summary

**Camera Selection Features:**

✅ **Automatic Discovery** - Finds all available cameras
✅ **Interactive Menu** - Easy selection with numbered list
✅ **Multiple Camera Types** - Webcam, USB, and RTSP support
✅ **Camera Information** - Shows resolution, FPS, and device info
✅ **Smart Mirroring** - Webcams flipped, RTSP original orientation
✅ **Flexible Modes** - Interactive or auto mode
✅ **Easy Switching** - Change cameras without editing config

**No more manual configuration - just select and detect!** 🚀

