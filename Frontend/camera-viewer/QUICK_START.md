# 🚀 Camera Viewer - Quick Start

Get up and running in 2 minutes!

---

## ⚡ Super Quick Start

```bash
cd Frontend/camera-viewer
./start.sh
```

**That's it!** The app will open in your browser at http://localhost:3000

---

## 📋 What You Need

- **Node.js** (v14+) - [Download](https://nodejs.org/)
- **npm** (comes with Node.js)

Check if you have them:
```bash
node --version
npm --version
```

---

## 🎯 Three Ways to Start

### 1️⃣ Easiest - Use Start Script

```bash
cd Frontend/camera-viewer
./start.sh
```

### 2️⃣ Manual - Step by Step

```bash
cd Frontend/camera-viewer
npm install
npm start
```

### 3️⃣ Custom Port

```bash
cd Frontend/camera-viewer
PORT=3001 npm start
```

---

## 🎨 What You'll See

### 1. **Camera Selector**
- Dropdown with 3 cameras:
  - 🎥 FaceTime HD Camera
  - 🎥 USB Camera
  - 📹 Tapo Smart Camera

### 2. **Camera Controls**
- ▶️ **Open Camera** button (green)
- ⏹️ **Close Camera** button (red)

### 3. **Camera Display**
- Live status indicator
- Camera feed area
- Statistics panel

---

## 🎮 How to Use

1. **Select** a camera from dropdown
2. **Click** "Open Camera" button
3. **View** camera feed (placeholder)
4. **Click** "Close Camera" when done

---

## 🐛 Quick Fixes

### Port 3000 in use?
```bash
PORT=3001 npm start
```

### Dependencies won't install?
```bash
npm cache clean --force
rm -rf node_modules
npm install
```

### Browser won't open?
Manually go to: http://localhost:3000

---

## 📚 More Help

- **Full Setup Guide:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Complete Docs:** [README.md](README.md)
- **Project Overview:** [../../README.md](../../README.md)

---

## ✅ Success!

If you see the Camera Viewer interface with the dropdown and buttons, you're all set! 🎉

---

**Smart Home Automation © 2024**

