#!/bin/bash

# Camera Viewer - Quick Start Script
# This script installs dependencies and starts the React app

echo "======================================================================"
echo "📹 Camera Viewer - Quick Start"
echo "======================================================================"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed!"
    echo "   Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js found: $(node --version)"
echo "✅ npm found: $(npm --version)"
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    echo "   This may take a few minutes on first run..."
    echo ""
    npm install
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ Failed to install dependencies"
        exit 1
    fi
    
    echo ""
    echo "✅ Dependencies installed successfully!"
else
    echo "✅ Dependencies already installed"
fi

echo ""
echo "======================================================================"
echo "🚀 Starting Camera Viewer..."
echo "======================================================================"
echo ""
echo "📱 The app will open in your browser at http://localhost:3000"
echo ""
echo "⌨️  Press Ctrl+C to stop the server"
echo ""
echo "======================================================================"
echo ""

# Start the React app
npm start

