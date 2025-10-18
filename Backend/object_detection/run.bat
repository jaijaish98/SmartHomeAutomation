@echo off
REM Windows One-Click Launcher for YOLO Object Detection

cls
echo ======================================================================
echo 🚀 YOLO Object Detection - One-Click Launcher
echo ======================================================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check Python
echo 🔍 Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.7+
    pause
    exit /b 1
)
python --version
echo.

REM Install dependencies
echo 📦 Checking dependencies...
python -m pip install -q -r requirements.txt >nul 2>&1
echo    ✅ Dependencies ready
echo.

REM Check model files
if not exist "models\yolov4-tiny.weights" (
    echo 📥 Downloading YOLO model (first time only, ~23 MB)...
    python scripts\download_models.py
    echo.
) else (
    echo ✅ Model already downloaded
    echo.
)

REM Run object detection
echo ======================================================================
echo 🎬 Launching Object Detection...
echo ======================================================================
echo.
echo 📹 Controls:
echo    • Press 'q' or ESC to exit
echo    • Press 's' to save frame
echo    • Press 'i' to show model info
echo.
echo ======================================================================
echo.

python scripts\detect_objects.py

echo.
echo ======================================================================
echo 👋 Object detection stopped
echo ======================================================================
pause

