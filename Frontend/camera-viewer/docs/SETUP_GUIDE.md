# 📹 Camera Viewer - Setup Guide

Complete guide to setting up and running the Camera Viewer React application.

---

## 🎯 What is Camera Viewer?

Camera Viewer is a modern React.js web application that allows you to:

✅ **View all available cameras** - Automatically discovers cameras from backend
✅ **Select cameras easily** - Dropdown menu with camera details
✅ **Open/Close cameras** - Simple button controls
✅ **See camera info** - Type, resolution, FPS displayed
✅ **Responsive design** - Works on desktop, tablet, and mobile

---

## 📋 Prerequisites

Before you begin, make sure you have:

### Required
- **Node.js** (v14 or higher) - [Download here](https://nodejs.org/)
- **npm** (comes with Node.js)

### Optional
- **yarn** - Alternative package manager

### Check Your Installation

```bash
node --version   # Should show v14.x.x or higher
npm --version    # Should show 6.x.x or higher
```

---

## 🚀 Quick Start (Easiest Method)

### Option 1: Use the Start Script

```bash
cd Frontend/camera-viewer
./start.sh
```

That's it! The script will:
1. Check for Node.js
2. Install dependencies (if needed)
3. Start the development server
4. Open your browser automatically

---

## 📝 Manual Setup

### Step 1: Navigate to Directory

```bash
cd Frontend/camera-viewer
```

### Step 2: Install Dependencies

```bash
npm install
```

This will install:
- React 18
- React DOM
- React Scripts
- Axios (for API calls)

**First time installation may take 2-5 minutes.**

### Step 3: Start Development Server

```bash
npm start
```

### Step 4: Open Browser

The app should automatically open at:
```
http://localhost:3000
```

If it doesn't open automatically, manually navigate to that URL.

---

## 🎨 What You'll See

### 1. **Header**
- App title: "Smart Home Camera Viewer"
- Subtitle: "View and manage your cameras"

### 2. **Camera Selector**
- Dropdown menu showing all available cameras
- Camera details (type, resolution, FPS)

### 3. **Camera Viewer**
- "Open Camera" button (green)
- "Close Camera" button (red)
- Camera feed display area
- Live status indicator

### 4. **Footer**
- Copyright information
- Number of available cameras

---

## 📹 Available Cameras (Mock Data)

The app currently shows these cameras:

1. **🎥 FaceTime HD Camera**
   - Type: Webcam
   - Resolution: 1920x1080
   - FPS: 30

2. **🎥 USB Camera**
   - Type: Webcam
   - Resolution: 1920x1080
   - FPS: 30

3. **📹 Tapo Smart Camera**
   - Type: RTSP
   - Resolution: Variable
   - FPS: Variable

---

## 🎮 How to Use

### Step 1: Select a Camera
1. Click the dropdown menu
2. Choose a camera from the list
3. Camera details will appear below

### Step 2: Open Camera
1. Click the "▶️ Open Camera" button
2. Wait for the camera to initialize
3. Camera feed will appear (placeholder for now)

### Step 3: View Camera
- See the live status indicator (🔴 LIVE)
- View camera statistics at the bottom
- Camera name and type displayed

### Step 4: Close Camera
1. Click the "⏹️ Close Camera" button
2. Camera feed will stop
3. Ready to select another camera

---

## 🔧 Available Commands

### Development

```bash
npm start          # Start development server
npm test           # Run tests
npm run build      # Build for production
```

### Port Configuration

If port 3000 is already in use:

```bash
PORT=3001 npm start
```

Or create a `.env` file:
```
PORT=3001
```

---

## 🐛 Troubleshooting

### Problem: "npm: command not found"

**Solution:** Install Node.js from https://nodejs.org/

### Problem: "Port 3000 already in use"

**Solution:** 
```bash
# Option 1: Use different port
PORT=3001 npm start

# Option 2: Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### Problem: Dependencies won't install

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Problem: Browser doesn't open automatically

**Solution:** Manually open http://localhost:3000 in your browser

### Problem: Blank page in browser

**Solution:**
1. Check browser console for errors (F12)
2. Make sure all dependencies installed correctly
3. Try clearing browser cache
4. Restart the development server

---

## 🔌 Backend Integration (Future)

### Current Status
The app uses **mock data** for demonstration.

### To Connect to Real Backend

1. **Start the backend server** (from Backend directory)
2. **Update API URL** in `src/services/cameraService.js`:
   ```javascript
   const API_BASE_URL = 'http://localhost:5000/api';
   ```
3. **Enable CORS** on backend
4. **Restart React app**

### Required Backend Endpoints

- `GET /api/cameras` - List cameras
- `POST /api/cameras/:id/open` - Open camera
- `POST /api/cameras/:id/close` - Close camera
- `GET /stream/:id` - Video stream

---

## 📱 Responsive Design

The app works on all devices:

### Desktop (1200px+)
- Full layout with spacious panels
- Large buttons and text
- Side-by-side information

### Tablet (768px - 1199px)
- Optimized spacing
- Stacked layout
- Touch-friendly buttons

### Mobile (< 768px)
- Single column layout
- Full-width buttons
- Compact information display

---

## 🎨 Customization

### Change Colors

Edit `src/styles/App.css`:

```css
/* Primary gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Change to your colors */
background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
```

### Change Port

Create `.env` file:
```
PORT=3001
BROWSER=none  # Don't auto-open browser
```

### Add New Features

1. Create component in `src/components/`
2. Add styles in `src/styles/`
3. Import in `App.js`
4. Update documentation

---

## 📊 Project Structure

```
camera-viewer/
├── public/
│   └── index.html              # HTML template
│
├── src/
│   ├── components/
│   │   ├── CameraSelector.js   # Dropdown component
│   │   └── CameraViewer.js     # Viewer component
│   │
│   ├── services/
│   │   └── cameraService.js    # API service (mock data)
│   │
│   ├── styles/
│   │   ├── App.css             # Main styles
│   │   ├── CameraSelector.css  # Selector styles
│   │   ├── CameraViewer.css    # Viewer styles
│   │   └── index.css           # Global styles
│   │
│   ├── App.js                  # Main component
│   └── index.js                # Entry point
│
├── package.json                # Dependencies
├── README.md                   # Documentation
├── SETUP_GUIDE.md             # This file
└── start.sh                    # Quick start script
```

---

## 🚀 Next Steps

After getting the app running:

1. ✅ Explore the UI and test camera selection
2. ✅ Try opening and closing different cameras
3. ✅ Test on different screen sizes (resize browser)
4. ✅ Check browser console for any messages
5. 🚧 Connect to real backend (when ready)
6. 🚧 Implement real video streaming
7. 🚧 Add more features (recording, snapshots, etc.)

---

## 📚 Learn More

- [React Documentation](https://react.dev/)
- [Create React App Documentation](https://create-react-app.dev/)
- [Backend README](../../Backend/README.md)
- [Project Overview](../../README.md)

---

## 🤝 Need Help?

1. Check this guide first
2. Read the [README.md](README.md)
3. Check browser console for errors (F12)
4. Verify Node.js and npm are installed correctly
5. Make sure you're in the correct directory

---

## ✅ Success Checklist

- [ ] Node.js installed (v14+)
- [ ] npm installed
- [ ] Navigated to `Frontend/camera-viewer`
- [ ] Ran `npm install` successfully
- [ ] Ran `npm start` successfully
- [ ] Browser opened to http://localhost:3000
- [ ] Can see the Camera Viewer interface
- [ ] Can select cameras from dropdown
- [ ] Can click Open/Close buttons

---

**You're all set! Enjoy using Camera Viewer!** 🎉

**Smart Home Automation © 2024**

