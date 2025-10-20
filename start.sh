#!/bin/bash

# Smart Home Automation - Startup Script
# This script starts both the backend API server and frontend React app

echo "======================================================================"
echo "🚀 Starting Smart Home Automation System"
echo "======================================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if Backend directory exists
if [ ! -d "$SCRIPT_DIR/Backend" ]; then
    echo "❌ Error: Backend directory not found!"
    exit 1
fi

# Check if Frontend directory exists
if [ ! -d "$SCRIPT_DIR/Frontend/camera-viewer" ]; then
    echo "❌ Error: Frontend directory not found!"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "======================================================================"
    echo "🛑 Stopping Smart Home Automation System"
    echo "======================================================================"
    
    # Kill backend process
    if [ ! -z "$BACKEND_PID" ]; then
        echo "Stopping backend server (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null
    fi
    
    # Kill frontend process
    if [ ! -z "$FRONTEND_PID" ]; then
        echo "Stopping frontend server (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null
    fi
    
    echo "✅ All servers stopped"
    exit 0
}

# Trap SIGINT (Ctrl+C) and SIGTERM
trap cleanup SIGINT SIGTERM

# Start Backend Server
echo "${BLUE}📡 Starting Backend API Server...${NC}"
cd "$SCRIPT_DIR/Backend/api"
python3 app.py > "$SCRIPT_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
echo "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"
echo "   Log file: backend.log"
echo ""

# Wait a moment for backend to initialize
sleep 3

# Start Frontend Server
echo "${BLUE}🎨 Starting Frontend React App...${NC}"
cd "$SCRIPT_DIR/Frontend/camera-viewer"
npm start > "$SCRIPT_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"
echo "   Log file: frontend.log"
echo ""

# Wait for frontend to compile
echo "${YELLOW}⏳ Waiting for frontend to compile...${NC}"
sleep 10

echo "======================================================================"
echo "${GREEN}✅ Smart Home Automation System Started Successfully!${NC}"
echo "======================================================================"
echo ""
echo "📡 Backend API:  http://localhost:5000"
echo "🎨 Frontend UI:  http://localhost:3000"
echo ""
echo "📋 Features Available:"
echo "   - 📹 Camera Viewer with Object Detection"
echo "   - 👤 Face Recognition & Enrollment"
echo "   - 🔄 Real-time Updates"
echo ""
echo "📝 Logs:"
echo "   - Backend:  $SCRIPT_DIR/backend.log"
echo "   - Frontend: $SCRIPT_DIR/frontend.log"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "======================================================================"
echo ""

# Keep script running and wait for processes
wait $BACKEND_PID $FRONTEND_PID

