#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

# PID file to track background processes
PIDS_FILE="$SCRIPT_DIR/.server_pids"

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down servers...${NC}"

    if [ -f "$PIDS_FILE" ]; then
        while read pid; do
            if ps -p $pid > /dev/null 2>&1; then
                echo -e "${CYAN}  Stopping process $pid${NC}"
                kill $pid 2>/dev/null
            fi
        done < "$PIDS_FILE"
        rm -f "$PIDS_FILE"
    fi

    # Kill any remaining Django/npm processes
    pkill -f "manage.py runserver" 2>/dev/null
    pkill -f "vite" 2>/dev/null

    echo -e "${GREEN}✅ All servers stopped${NC}"
    exit 0
}

# Set up trap for cleanup
trap cleanup SIGINT SIGTERM EXIT

# Print header
echo -e "${PURPLE}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║          🚀 UMUHUZA PLATFORM STARTUP SCRIPT 🚀         ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

# Check if backend directory exists
if [ ! -d "$BACKEND_DIR" ]; then
    echo -e "${RED}❌ Error: Backend directory not found at $BACKEND_DIR${NC}"
    exit 1
fi

# Check if frontend directory exists
if [ ! -d "$FRONTEND_DIR" ]; then
    echo -e "${RED}❌ Error: Frontend directory not found at $FRONTEND_DIR${NC}"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "$BACKEND_DIR/venv" ]; then
    echo -e "${RED}❌ Error: Virtual environment not found at $BACKEND_DIR/venv${NC}"
    echo -e "${YELLOW}💡 Tip: Create it with: cd backend && python3 -m venv venv${NC}"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo -e "${YELLOW}⚠️  Warning: node_modules not found. Installing dependencies...${NC}"
    cd "$FRONTEND_DIR"
    npm install
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Error: Failed to install frontend dependencies${NC}"
        exit 1
    fi
fi

# Clear PID file
> "$PIDS_FILE"

echo -e "${BLUE}┌─────────────────────────────────────────────────────┐${NC}"
echo -e "${BLUE}│  STEP 1: Starting Backend (Django)                 │${NC}"
echo -e "${BLUE}└─────────────────────────────────────────────────────┘${NC}\n"

# Start Django backend
cd "$BACKEND_DIR"
source venv/bin/activate

# Check if Django is installed
python -c "import django" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error: Django not installed in virtual environment${NC}"
    exit 1
fi

# Run migrations if needed
echo -e "${CYAN}🔄 Checking for pending migrations...${NC}"
python manage.py migrate --check 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Applying migrations...${NC}"
    python manage.py migrate
fi

# Start Django server in background
echo -e "${CYAN}🐍 Starting Django server on http://localhost:8000${NC}"
python manage.py runserver 0.0.0.0:8000 > "$SCRIPT_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID >> "$PIDS_FILE"

# Wait for backend to be ready
sleep 3

# Check if backend is running
if ps -p $BACKEND_PID > /dev/null; then
    echo -e "${GREEN}✅ Backend server started successfully (PID: $BACKEND_PID)${NC}\n"
else
    echo -e "${RED}❌ Failed to start backend server${NC}"
    echo -e "${YELLOW}Check backend.log for details${NC}"
    exit 1
fi

echo -e "${BLUE}┌─────────────────────────────────────────────────────┐${NC}"
echo -e "${BLUE}│  STEP 2: Starting Frontend (React + Vite)          │${NC}"
echo -e "${BLUE}└─────────────────────────────────────────────────────┘${NC}\n"

# Start Frontend
cd "$FRONTEND_DIR"

echo -e "${CYAN}⚛️  Starting Vite dev server on http://localhost:5173${NC}"
npm run dev > "$SCRIPT_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID >> "$PIDS_FILE"

# Wait for frontend to be ready
sleep 5

# Check if frontend is running
if ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${GREEN}✅ Frontend server started successfully (PID: $FRONTEND_PID)${NC}\n"
else
    echo -e "${RED}❌ Failed to start frontend server${NC}"
    echo -e "${YELLOW}Check frontend.log for details${NC}"
    cleanup
    exit 1
fi

# Print success message
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║           ✅ ALL SERVERS RUNNING SUCCESSFULLY ✅        ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

echo -e "${CYAN}📍 Server URLs:${NC}"
echo -e "   ${PURPLE}Frontend:${NC} http://localhost:5173"
echo -e "   ${PURPLE}Backend:${NC}  http://localhost:8000"
echo -e "   ${PURPLE}Admin:${NC}    http://localhost:8000/admin"
echo -e "   ${PURPLE}API:${NC}      http://localhost:8000/api\n"

echo -e "${CYAN}📝 Logs:${NC}"
echo -e "   ${PURPLE}Backend:${NC}  tail -f $SCRIPT_DIR/backend.log"
echo -e "   ${PURPLE}Frontend:${NC} tail -f $SCRIPT_DIR/frontend.log\n"

echo -e "${YELLOW}⚠️  Press Ctrl+C to stop all servers${NC}\n"

# Keep script running and monitor processes
while true; do
    # Check if backend is still running
    if ! ps -p $BACKEND_PID > /dev/null; then
        echo -e "${RED}❌ Backend server stopped unexpectedly${NC}"
        cleanup
        exit 1
    fi

    # Check if frontend is still running
    if ! ps -p $FRONTEND_PID > /dev/null; then
        echo -e "${RED}❌ Frontend server stopped unexpectedly${NC}"
        cleanup
        exit 1
    fi

    sleep 5
done
