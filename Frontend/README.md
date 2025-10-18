# Frontend - Smart Home Automation

This directory contains the frontend applications for the Smart Home Automation system.

---

## 📁 Applications

### 📹 Camera Viewer (`camera-viewer/`)

A modern React.js web application for viewing and managing multiple cameras.

**Features:**
- ✅ Camera discovery and listing
- ✅ Dropdown selection for easy camera switching
- ✅ Open/Close camera controls
- ✅ Live camera feed display (ready for backend integration)
- ✅ Camera information (type, resolution, FPS)
- ✅ Responsive design for all devices
- ✅ Beautiful modern UI with animations

**Quick Start:**
```bash
cd camera-viewer
npm install
npm start
```

**Documentation:** See [camera-viewer/README.md](camera-viewer/README.md)

---

## 🚀 Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Running the Camera Viewer

1. Navigate to the application directory:
   ```bash
   cd camera-viewer
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open your browser to `http://localhost:3000`

---

## 🔌 Backend Integration

The frontend applications are designed to work with the backend services located in the `Backend/` directory.

### API Endpoints (Planned)

- `GET /api/cameras` - List all available cameras
- `POST /api/cameras/:id/open` - Open camera stream
- `POST /api/cameras/:id/close` - Close camera stream
- `GET /stream/:id` - Camera video stream

### Current Status

The camera-viewer app currently uses **mock data** for demonstration. Backend API integration is planned for future updates.

---

## 📱 Applications Overview

| Application | Status | Description |
|------------|--------|-------------|
| **camera-viewer** | ✅ Ready | View and manage cameras with dropdown selection |
| **dashboard** | 🚧 Planned | Multi-camera dashboard with object detection |
| **settings** | 🚧 Planned | System configuration and camera settings |

---

## 🛠️ Technology Stack

- **React 18** - UI framework
- **React Scripts** - Build tooling
- **Axios** - HTTP client for API calls
- **CSS3** - Modern styling with gradients and animations
- **ES6+** - Modern JavaScript features

---

## 📁 Project Structure

```
Frontend/
├── camera-viewer/          # Camera viewer application ✅
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API services
│   │   └── styles/        # CSS files
│   ├── public/            # Static files
│   └── package.json       # Dependencies
│
└── README.md              # This file
```

---

## 🚧 Future Applications

### Planned Features

- [ ] Multi-camera dashboard with grid view
- [ ] Real-time object detection visualization
- [ ] Motion detection alerts
- [ ] Recording and playback interface
- [ ] User authentication and settings
- [ ] Camera configuration panel
- [ ] Mobile app (React Native)

---

## 📚 Documentation

- [Camera Viewer Documentation](camera-viewer/README.md)
- [Backend API Documentation](../Backend/README.md)
- [Project Overview](../README.md)

---

## 🤝 Contributing

To contribute to the frontend applications:

1. Choose or create an application directory
2. Make your changes
3. Test thoroughly with `npm start`
4. Update documentation
5. Follow React best practices

---

**Smart Home Automation © 2024**

