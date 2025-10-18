# 📹 Camera Viewer - React Application

A modern React.js web application for viewing and managing multiple cameras in the Smart Home Automation system.

---

## 🎯 Features

✅ **Camera Discovery** - Automatically lists all available cameras
✅ **Dropdown Selection** - Easy camera selection from dropdown menu
✅ **Open/Close Controls** - Simple buttons to start and stop camera streams
✅ **Camera Information** - Display camera type, resolution, and FPS
✅ **Live Status** - Real-time camera status indicators
✅ **Responsive Design** - Works on desktop, tablet, and mobile
✅ **Modern UI** - Beautiful gradient design with smooth animations

---

## 📁 Project Structure

```
camera-viewer/
├── public/
│   └── index.html              # HTML template
├── src/
│   ├── components/
│   │   ├── CameraSelector.js   # Camera dropdown component
│   │   └── CameraViewer.js     # Camera viewer component
│   ├── services/
│   │   └── cameraService.js    # API service for camera operations
│   ├── styles/
│   │   ├── App.css             # Main app styles
│   │   ├── CameraSelector.css  # Selector styles
│   │   ├── CameraViewer.css    # Viewer styles
│   │   └── index.css           # Global styles
│   ├── App.js                  # Main app component
│   └── index.js                # Entry point
├── package.json                # Dependencies
└── README.md                   # This file
```

---

## 🚀 Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. **Navigate to the camera-viewer directory:**
   ```bash
   cd Frontend/camera-viewer
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Open your browser:**
   ```
   http://localhost:3000
   ```

---

## 📋 Available Scripts

### `npm start`
Runs the app in development mode.
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

### `npm run build`
Builds the app for production to the `build` folder.
The build is minified and optimized for best performance.

### `npm test`
Launches the test runner in interactive watch mode.

---

## 🎨 Components

### **CameraSelector**
Dropdown component for selecting cameras.

**Props:**
- `cameras` - Array of camera objects
- `selectedCamera` - Currently selected camera
- `onCameraSelect` - Callback when camera is selected
- `disabled` - Disable the dropdown

**Features:**
- Lists all available cameras
- Shows camera type icon (🎥 for webcam, 📹 for RTSP)
- Displays camera information (resolution, FPS, type)

### **CameraViewer**
Component for viewing camera feed with controls.

**Props:**
- `selectedCamera` - Camera object to display

**Features:**
- Open/Close camera buttons
- Live status indicator
- Stream placeholder
- Camera statistics
- Error handling

---

## 🔌 API Integration

### Current Status
The app currently uses **mock data** for demonstration purposes.

### Camera Service (`src/services/cameraService.js`)

**Functions:**
- `getAvailableCameras()` - Fetch list of available cameras
- `openCamera(cameraId)` - Open camera stream
- `closeCamera(cameraId)` - Close camera stream
- `getCameraStreamUrl(cameraId)` - Get stream URL

### Backend Integration (TODO)

To connect to the actual backend:

1. **Update API endpoints** in `cameraService.js`:
   ```javascript
   const API_BASE_URL = 'http://localhost:5000/api';
   ```

2. **Implement backend API** with these endpoints:
   - `GET /api/cameras` - List all cameras
   - `POST /api/cameras/:id/open` - Open camera
   - `POST /api/cameras/:id/close` - Close camera
   - `GET /stream/:id` - Camera stream

3. **Enable CORS** on backend for frontend access

---

## 📱 Responsive Design

The application is fully responsive and works on:

- 🖥️ **Desktop** - Full layout with side-by-side panels
- 📱 **Tablet** - Stacked layout with optimized spacing
- 📱 **Mobile** - Single column layout with touch-friendly buttons

---

## 🎨 Styling

### Color Scheme
- **Primary Gradient:** Purple to Blue (`#667eea` → `#764ba2`)
- **Secondary Gradient:** Pink to Red (`#f093fb` → `#f5576c`)
- **Background:** White with subtle shadows
- **Text:** Dark gray (`#333`) with lighter variants

### Animations
- Button hover effects with lift animation
- Smooth transitions on all interactive elements
- Pulsing "LIVE" indicator
- Loading spinner

---

## 🔧 Configuration

### Camera Data Format

```javascript
{
  id: 1,                    // Unique camera ID
  index: 0,                 // Device index (for webcams)
  name: 'FaceTime HD Camera', // Camera name
  type: 'webcam',           // 'webcam' or 'rtsp'
  resolution: '1920x1080',  // Resolution
  fps: 30,                  // Frames per second
  available: true           // Availability status
}
```

---

## 🚧 Future Enhancements

### Planned Features
- [ ] Real-time video streaming integration
- [ ] Multiple camera view (grid layout)
- [ ] Camera settings panel
- [ ] Recording functionality
- [ ] Snapshot capture
- [ ] Motion detection alerts
- [ ] Camera health monitoring
- [ ] User authentication
- [ ] Camera presets and favorites

---

## 🐛 Troubleshooting

### Port Already in Use
If port 3000 is already in use:
```bash
PORT=3001 npm start
```

### Dependencies Not Installing
Clear npm cache and reinstall:
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Build Errors
Make sure you're using a compatible Node.js version:
```bash
node --version  # Should be v14 or higher
```

---

## 📚 Technologies Used

- **React 18** - UI framework
- **React Scripts** - Build tooling
- **Axios** - HTTP client (for future API calls)
- **CSS3** - Styling with gradients and animations
- **ES6+** - Modern JavaScript

---

## 🤝 Contributing

This is part of the Smart Home Automation project. To contribute:

1. Make changes in the `Frontend/camera-viewer` directory
2. Test thoroughly with `npm start`
3. Build for production with `npm run build`
4. Update this README if adding new features

---

## 📄 License

Part of the Smart Home Automation project.

---

## 📞 Support

For issues or questions:
1. Check the console for error messages
2. Verify all dependencies are installed
3. Ensure backend API is running (when integrated)
4. Check browser compatibility (Chrome, Firefox, Safari, Edge)

---

## 🎉 Quick Start Summary

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

**That's it! Your camera viewer is ready!** 🚀

---

**Smart Home Automation © 2024**

