#!/bin/bash

# Backend API Server - Start Script

echo "======================================================================"
echo "🚀 Smart Home Camera API - Starting Server"
echo "======================================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "   Please install Python 3 from https://www.python.org/"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo ""

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

echo "======================================================================"
echo "🎬 Starting API Server..."
echo "======================================================================"
echo ""
echo "📡 API will be available at:"
echo "   - http://localhost:5000"
echo "   - http://localhost:5000/api/cameras"
echo "   - http://localhost:5000/stream/:id"
echo ""
echo "⌨️  Press Ctrl+C to stop the server"
echo ""
echo "======================================================================"
echo ""

# Start the Flask app
python3 app.py

