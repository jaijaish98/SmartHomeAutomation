#!/bin/bash

# One-Click YOLO Object Detection Launcher
# This script handles everything automatically!

clear

echo "======================================================================"
echo "🚀 YOLO Object Detection - One-Click Launcher"
echo "======================================================================"
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Step 1: Check Python
echo "🔍 Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.7+"
    exit 1
fi
echo "   ✅ Python found: $(python3 --version)"
echo ""

# Step 2: Install dependencies (silent)
echo "📦 Checking dependencies..."
pip3 install -q -r requirements.txt 2>&1 | grep -v "already satisfied" || true
echo "   ✅ Dependencies ready"
echo ""

# Step 3: Check if model exists, download if needed
if [ ! -f "models/yolov4-tiny.weights" ]; then
    echo "📥 Downloading YOLO model (first time only, ~23 MB)..."
    python3 scripts/download_models.py
    echo ""
else
    echo "✅ Model already downloaded"
    echo ""
fi

# Step 4: Run object detection
echo "======================================================================"
echo "🎬 Launching Object Detection..."
echo "======================================================================"
echo ""
echo "📹 Controls:"
echo "   • Press 'q' or ESC to exit"
echo "   • Press 's' to save frame"
echo "   • Press 'i' to show model info"
echo ""
echo "======================================================================"
echo ""

# Launch the detector
python3 scripts/detect_objects.py

# Cleanup message
echo ""
echo "======================================================================"
echo "👋 Object detection stopped"
echo "======================================================================"

