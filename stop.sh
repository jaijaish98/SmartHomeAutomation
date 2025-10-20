#!/bin/bash

# Smart Home Automation - Stop Script
# This script stops both the backend API server and frontend React app

echo "======================================================================"
echo "🛑 Stopping Smart Home Automation System"
echo "======================================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to kill process on port
kill_port() {
    local port=$1
    local name=$2
    
    echo "Checking for processes on port $port ($name)..."
    
    # Find process using the port
    PID=$(lsof -ti:$port)
    
    if [ ! -z "$PID" ]; then
        echo "${YELLOW}Found process $PID on port $port${NC}"
        kill -9 $PID 2>/dev/null
        echo "${GREEN}✅ Stopped $name (PID: $PID)${NC}"
    else
        echo "No process found on port $port"
    fi
}

# Stop Backend (port 5000)
kill_port 5000 "Backend API Server"
echo ""

# Stop Frontend (port 3000)
kill_port 3000 "Frontend React App"
echo ""

# Also kill any python app.py processes
echo "Checking for any remaining backend processes..."
BACKEND_PIDS=$(pgrep -f "python3 app.py")
if [ ! -z "$BACKEND_PIDS" ]; then
    echo "${YELLOW}Found backend processes: $BACKEND_PIDS${NC}"
    pkill -9 -f "python3 app.py"
    echo "${GREEN}✅ Stopped all backend processes${NC}"
else
    echo "No backend processes found"
fi
echo ""

# Also kill any npm start processes
echo "Checking for any remaining frontend processes..."
FRONTEND_PIDS=$(pgrep -f "react-scripts start")
if [ ! -z "$FRONTEND_PIDS" ]; then
    echo "${YELLOW}Found frontend processes: $FRONTEND_PIDS${NC}"
    pkill -9 -f "react-scripts start"
    echo "${GREEN}✅ Stopped all frontend processes${NC}"
else
    echo "No frontend processes found"
fi
echo ""

echo "======================================================================"
echo "${GREEN}✅ All servers stopped successfully!${NC}"
echo "======================================================================"

