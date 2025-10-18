# Real-time Face Detection with OpenCV

A Python application that performs real-time face detection using OpenCV's Haar Cascade classifier. The application captures video from your system's default camera and detects faces in real-time, drawing bounding boxes around detected faces.

## Features

- ✅ Real-time face detection from webcam/camera feed
- ✅ Uses OpenCV's Haar Cascade classifier for accurate face detection
- ✅ Draws bounding boxes around detected faces
- ✅ Displays face count and FPS information
- ✅ Error handling for camera access issues
- ✅ Easy exit with 'q' or ESC key

## Requirements

- Python 3.7 or higher
- Webcam/camera connected to your system
- OpenCV library

## Installation

1. Navigate to the `face_detection` directory:
   ```bash
   cd face_detection
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Step 1: Test Camera Access (Recommended First Step)

Before running the face detector, test if your camera is accessible:

```bash
python test_camera.py
```

This will help diagnose any camera permission or access issues.

### Step 2: Run Face Detection

Run the face detection script:

```bash
python face_detector.py
```

Or use the launcher script (macOS):

```bash
./run_face_detector.sh
```

### Controls

- **Press 'q' or ESC**: Exit the application
- **Ctrl+C**: Force quit (if needed)

### What to Expect

When you run the script, you should see:
1. Initialization messages confirming the camera and classifier are loaded
2. A window titled "Face Detection - Real-time" showing your camera feed
3. Green bounding boxes around detected faces
4. Information overlay showing:
   - Number of faces detected
   - Current FPS (frames per second)
   - Exit instructions

## How It Works

1. **Initialization**: The script loads OpenCV's pre-trained Haar Cascade classifier for frontal face detection
2. **Camera Access**: Opens the default camera (index 0)
3. **Frame Processing**: 
   - Captures frames from the camera
   - Converts each frame to grayscale
   - Applies the Haar Cascade classifier to detect faces
   - Draws bounding boxes around detected faces
4. **Display**: Shows the processed video feed with face detection overlays
5. **Cleanup**: Releases camera resources when exiting

## Troubleshooting

### Camera Not Accessible (macOS)

**Error: "OpenCV: not authorized to capture video" or "camera failed to properly initialize"**

This is a macOS privacy/security issue. Follow these steps:

1. **Grant Camera Permission to Terminal:**
   - Open **System Settings** (or System Preferences)
   - Go to **Privacy & Security** → **Camera**
   - Find **Terminal** (or **iTerm2**, **VS Code**, etc.) in the list
   - Check the box to enable camera access
   - If your terminal app isn't listed, run the script again and it should appear

2. **Restart Your Terminal:**
   - Completely close and reopen your Terminal application
   - Navigate back to the project directory
   - Run the script again

3. **Alternative - Use Python IDE:**
   - Run the script from PyCharm, VS Code, or another IDE
   - Grant camera permission to the IDE instead

### Camera Not Accessible (General)

If you see other camera access errors:
- Make sure your camera is connected and working
- Close any other applications using the camera (Zoom, Skype, etc.)
- Try changing the camera index in the code (0, 1, 2, etc.)
- Test your camera with another application first

### Poor Detection Performance

If faces are not being detected well:
- Ensure good lighting conditions
- Face the camera directly
- Adjust the `scale_factor` and `min_neighbors` parameters in the code for better accuracy

### Low FPS

If the video feed is slow:
- Close other resource-intensive applications
- Reduce the camera resolution
- Ensure your system meets the minimum requirements

## Configuration

You can customize the face detection parameters by modifying the `FaceDetector` initialization in `face_detector.py`:

```python
detector = FaceDetector(
    camera_index=0,      # Camera device index (0 for default)
    scale_factor=1.1,    # Detection scale factor (1.05-1.4)
    min_neighbors=5,     # Minimum neighbors (3-6 recommended)
    min_size=(30, 30)    # Minimum face size in pixels
)
```

## Technical Details

- **Haar Cascade Classifier**: Uses `haarcascade_frontalface_default.xml` for face detection
- **Detection Method**: Multi-scale detection with configurable parameters
- **Video Processing**: Real-time frame-by-frame processing
- **Performance**: FPS calculation and display for monitoring performance

## License

This project is open-source and available for educational and personal use.

## Credits

Built with OpenCV - Open Source Computer Vision Library

