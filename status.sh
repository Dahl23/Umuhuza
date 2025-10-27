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
PIDS_FILE="$SCRIPT_DIR/.server_pids"

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║        UMUHUZA PLATFORM - SERVER STATUS               ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

# Check if servers are running
BACKEND_RUNNING=false
FRONTEND_RUNNING=false

# Check for Django process
if pgrep -f "manage.py runserver" > /dev/null; then
    BACKEND_RUNNING=true
    BACKEND_PID=$(pgrep -f "manage.py runserver")
fi

# Check for Vite process
if pgrep -f "vite" > /dev/null; then
    FRONTEND_RUNNING=true
    FRONTEND_PID=$(pgrep -f "vite")
fi

# Display status
echo -e "${CYAN}Backend (Django):${NC}"
if [ "$BACKEND_RUNNING" = true ]; then
    echo -e "  Status: ${GREEN}● RUNNING${NC} (PID: $BACKEND_PID)"
    echo -e "  URL:    http://localhost:8000"
else
    echo -e "  Status: ${RED}○ STOPPED${NC}"
fi

echo ""

echo -e "${CYAN}Frontend (React):${NC}"
if [ "$FRONTEND_RUNNING" = true ]; then
    echo -e "  Status: ${GREEN}● RUNNING${NC} (PID: $FRONTEND_PID)"
    echo -e "  URL:    http://localhost:5173"
else
    echo -e "  Status: ${RED}○ STOPPED${NC}"
fi

echo ""

# Check port availability
echo -e "${CYAN}Port Status:${NC}"
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "  Port 8000: ${GREEN}IN USE${NC} (Backend)"
else
    echo -e "  Port 8000: ${YELLOW}AVAILABLE${NC}"
fi

if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "  Port 5173: ${GREEN}IN USE${NC} (Frontend)"
else
    echo -e "  Port 5173: ${YELLOW}AVAILABLE${NC}"
fi

echo ""

# Overall status
if [ "$BACKEND_RUNNING" = true ] && [ "$FRONTEND_RUNNING" = true ]; then
    echo -e "${GREEN}✅ All servers are running${NC}"
elif [ "$BACKEND_RUNNING" = true ] || [ "$FRONTEND_RUNNING" = true ]; then
    echo -e "${YELLOW}⚠️  Some servers are running${NC}"
else
    echo -e "${RED}❌ No servers are running${NC}"
    echo -e "${CYAN}💡 Run ./start.sh to start servers${NC}"
fi

echo ""
