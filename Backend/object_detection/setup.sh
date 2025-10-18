#!/bin/bash

# YOLO Object Detection Setup Script
# Automates the setup process

echo "======================================================================"
echo "YOLO Object Detection - Setup Script"
echo "======================================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
echo "----------------------------------------------------------------------"
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✅ Dependencies installed successfully"
echo ""

# Test setup
echo "🧪 Testing setup..."
echo "----------------------------------------------------------------------"
python3 scripts/test_setup.py

if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  Some tests failed. Please check the output above."
    echo ""
    echo "💡 Common issues:"
    echo "   • Camera permission not granted (macOS)"
    echo "   • Model files not downloaded"
    echo ""
    echo "To download model files, run:"
    echo "   python3 scripts/download_models.py"
    exit 1
fi

echo ""
echo "======================================================================"
echo "✅ Setup completed successfully!"
echo "======================================================================"
echo ""
echo "Next steps:"
echo "   1. Download YOLO model: python3 scripts/download_models.py"
echo "   2. Run object detection: python3 scripts/detect_objects.py"
echo ""
echo "======================================================================"

