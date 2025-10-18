#!/bin/bash

# Face Detection Launcher Script
# This script helps with camera permissions on macOS

echo "=================================================="
echo "Face Detection - Camera Permission Helper"
echo "=================================================="
echo ""

# Check if running on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "⚠️  macOS detected - Camera permissions required"
    echo ""
    echo "If you see a camera permission error:"
    echo "1. Go to System Settings → Privacy & Security → Camera"
    echo "2. Enable camera access for Terminal (or your terminal app)"
    echo "3. Restart Terminal and run this script again"
    echo ""
    echo "Press Enter to continue..."
    read
fi

# Run the face detector
python3 face_detector.py

echo ""
echo "Script execution completed."

