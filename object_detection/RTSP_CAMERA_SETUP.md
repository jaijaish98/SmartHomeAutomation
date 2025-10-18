# RTSP Camera Setup Guide

This guide explains how to integrate your Tapo IP camera (or any RTSP-compatible camera) with the YOLO object detection system.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Configuration](#configuration)
5. [Troubleshooting](#troubleshooting)
6. [Security Best Practices](#security-best-practices)

---

## 🎯 Overview

The object detection system now supports two camera sources:
- **Webcam** - Local USB/built-in cameras
- **RTSP** - IP cameras via RTSP streams (Tapo, Hikvision, Dahua, etc.)

---

## ✅ Prerequisites

### 1. Camera Requirements
- IP camera with RTSP support (e.g., TP-Link Tapo)
- Camera connected to the same network
- RTSP enabled in camera settings
- Camera credentials (username and password)

### 2. Network Requirements
- Camera and computer on the same network (or accessible network)
- Know the camera's IP address
- RTSP port accessible (usually 554)

### 3. Software Requirements
- Python 3.7+
- OpenCV with FFMPEG support (auto-installed)
- All dependencies from `requirements.txt`

---

## 🚀 Quick Start

### Step 1: Find Your Camera's RTSP URL

**For Tapo Cameras:**
```
rtsp://username:password@camera_ip:554/stream1
```

**Example:**
```
rtsp://admin:MyPassword123@192.168.0.233:554/stream1
```

**Stream Options:**
- `/stream1` - High quality (1080p)
- `/stream2` - Low quality (360p, faster)

### Step 2: Configure Credentials

**Option A: Using credentials.yaml (Recommended)**

1. Copy the example file:
   ```bash
   cd object_detection/config
   cp credentials.yaml.example credentials.yaml
   ```

2. Edit `credentials.yaml`:
   ```yaml
   rtsp:
     url: "rtsp://your-username:your-password@192.168.0.233:554/stream1"
   ```

3. Save and close

**Option B: Direct in config.yaml (Not Recommended)**

Edit `config/config.yaml`:
```yaml
rtsp:
  url: "rtsp://username:password@192.168.0.233:554/stream1"
```

⚠️ **Warning:** Don't commit credentials to git!

### Step 3: Select RTSP as Camera Source

Edit `config/config.yaml`:
```yaml
camera_source:
  type: "rtsp"  # Change from "webcam" to "rtsp"
```

### Step 4: Run Object Detection

```bash
cd object_detection
./run.sh
```

Or:
```bash
python scripts/detect_objects.py
```

---

## ⚙️ Configuration

### Camera Source Selection

In `config/config.yaml`:

```yaml
camera_source:
  type: "webcam"  # Options: "webcam" or "rtsp"
```

### Webcam Settings

```yaml
webcam:
  index: 0        # Camera device index (0 for default)
  width: 640      # Frame width (0 for default)
  height: 480     # Frame height (0 for default)
  fps: 30         # Target FPS (0 for default)
```

### RTSP Settings

```yaml
rtsp:
  url: ""                     # RTSP URL (leave empty to load from credentials.yaml)
  reconnect_attempts: 3       # Number of reconnection attempts
  reconnect_delay: 2          # Delay between reconnections (seconds)
  timeout: 10                 # Connection timeout (seconds)
  buffer_size: 1              # Frame buffer (1 = latest frame, reduces lag)
```

### Advanced RTSP Configuration

**Reduce Lag:**
```yaml
rtsp:
  buffer_size: 1              # Use only latest frame
```

**Increase Reliability:**
```yaml
rtsp:
  reconnect_attempts: 5       # More retry attempts
  reconnect_delay: 3          # Longer delay between retries
  timeout: 15                 # Longer timeout
```

---

## 🔧 Troubleshooting

### Connection Failed

**Problem:** Cannot connect to RTSP stream

**Solutions:**
1. **Verify camera is on and connected:**
   ```bash
   ping 192.168.0.233
   ```

2. **Test RTSP URL with VLC:**
   - Open VLC Media Player
   - Media → Open Network Stream
   - Paste your RTSP URL
   - If it works in VLC, the URL is correct

3. **Check credentials:**
   - Verify username and password
   - Special characters in password may need URL encoding

4. **Verify RTSP is enabled:**
   - Check camera settings/app
   - Enable RTSP streaming

5. **Check firewall:**
   - Ensure port 554 is not blocked
   - Disable firewall temporarily to test

### Authentication Failed

**Problem:** "401 Unauthorized" or authentication errors

**Solutions:**
1. Double-check username and password
2. Reset camera password if forgotten
3. Check for special characters in password (may need encoding)

### Stream Lag or Freezing

**Problem:** Video is laggy or freezes

**Solutions:**
1. **Use lower quality stream:**
   ```yaml
   rtsp:
     url: "rtsp://user:pass@ip:554/stream2"  # Use stream2 instead of stream1
   ```

2. **Reduce buffer size:**
   ```yaml
   rtsp:
     buffer_size: 1  # Already set to minimum
   ```

3. **Check network:**
   - Use wired connection instead of WiFi
   - Ensure good WiFi signal
   - Reduce network congestion

4. **Lower camera resolution:**
   - Configure in camera settings/app

### Reconnection Issues

**Problem:** Stream drops and doesn't reconnect

**Solutions:**
1. **Increase reconnection attempts:**
   ```yaml
   rtsp:
     reconnect_attempts: 5
     reconnect_delay: 3
   ```

2. **Check camera stability:**
   - Ensure camera has stable power
   - Check camera firmware is up to date

### URL Encoding for Special Characters

If your password contains special characters, encode them:

| Character | Encoded |
|-----------|---------|
| @ | %40 |
| : | %3A |
| / | %2F |
| ? | %3F |
| # | %23 |
| [ | %5B |
| ] | %5D |
| ! | %21 |
| $ | %24 |
| & | %26 |
| ' | %27 |
| ( | %28 |
| ) | %29 |
| * | %2A |
| + | %2B |
| , | %2C |
| ; | %3B |
| = | %3D |

**Example:**
- Password: `MyPass@123!`
- Encoded: `MyPass%40123%21`
- URL: `rtsp://admin:MyPass%40123%21@192.168.0.233:554/stream1`

---

## 🔒 Security Best Practices

### 1. Never Commit Credentials

✅ **DO:**
- Use `credentials.yaml` (in `.gitignore`)
- Use environment variables
- Use separate config files for production

❌ **DON'T:**
- Commit passwords to git
- Share credentials in code
- Use default passwords

### 2. Secure Your Credentials File

```bash
# Set restrictive permissions (Linux/macOS)
chmod 600 object_detection/config/credentials.yaml
```

### 3. Use Strong Passwords

- Minimum 12 characters
- Mix of letters, numbers, symbols
- Avoid common words
- Change default camera passwords

### 4. Network Security

- Use VPN for remote access
- Keep camera firmware updated
- Disable unused camera features
- Use separate VLAN for cameras (advanced)

---

## 📚 Camera-Specific RTSP URLs

### TP-Link Tapo
```
rtsp://username:password@ip:554/stream1  # High quality
rtsp://username:password@ip:554/stream2  # Low quality
```

### Hikvision
```
rtsp://username:password@ip:554/Streaming/Channels/101
rtsp://username:password@ip:554/Streaming/Channels/102  # Sub-stream
```

### Dahua
```
rtsp://username:password@ip:554/cam/realmonitor?channel=1&subtype=0  # Main
rtsp://username:password@ip:554/cam/realmonitor?channel=1&subtype=1  # Sub
```

### Reolink
```
rtsp://username:password@ip:554/h264Preview_01_main  # Main
rtsp://username:password@ip:554/h264Preview_01_sub   # Sub
```

### Amcrest
```
rtsp://username:password@ip:554/cam/realmonitor?channel=1&subtype=0
```

### Generic ONVIF
```
rtsp://username:password@ip:554/live
rtsp://username:password@ip:554/stream
```

---

## 🎯 Switching Between Webcam and RTSP

### Use Webcam

Edit `config/config.yaml`:
```yaml
camera_source:
  type: "webcam"
```

Run:
```bash
./run.sh
```

### Use RTSP Camera

Edit `config/config.yaml`:
```yaml
camera_source:
  type: "rtsp"
```

Ensure `credentials.yaml` has your RTSP URL, then run:
```bash
./run.sh
```

---

## 💡 Tips

1. **Test RTSP URL first** - Use VLC to verify URL works
2. **Start with stream2** - Lower quality = faster, more reliable
3. **Use wired connection** - More stable than WiFi
4. **Monitor network usage** - RTSP can use significant bandwidth
5. **Keep camera firmware updated** - Improves stability and security

---

## 🆘 Getting Help

If you're still having issues:

1. Check camera documentation for RTSP URL format
2. Test with VLC Media Player first
3. Check camera app/settings for RTSP configuration
4. Verify network connectivity with `ping`
5. Check firewall and router settings

---

**Ready to detect objects from your IP camera!** 🎉

