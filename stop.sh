#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PIDS_FILE="$SCRIPT_DIR/.server_pids"

echo -e "${YELLOW}🛑 Stopping Umuhuza Platform servers...${NC}\n"

# Stop processes from PID file
if [ -f "$PIDS_FILE" ]; then
    while read pid; do
        if ps -p $pid > /dev/null 2>&1; then
            echo -e "${CYAN}  Stopping process $pid${NC}"
            kill $pid 2>/dev/null
            sleep 1

            # Force kill if still running
            if ps -p $pid > /dev/null 2>&1; then
                kill -9 $pid 2>/dev/null
            fi
        fi
    done < "$PIDS_FILE"
    rm -f "$PIDS_FILE"
fi

# Kill any remaining processes
echo -e "${CYAN}  Cleaning up remaining processes...${NC}"
pkill -f "manage.py runserver" 2>/dev/null
pkill -f "vite" 2>/dev/null

# Remove log files
if [ -f "$SCRIPT_DIR/backend.log" ]; then
    rm -f "$SCRIPT_DIR/backend.log"
fi

if [ -f "$SCRIPT_DIR/frontend.log" ]; then
    rm -f "$SCRIPT_DIR/frontend.log"
fi

echo -e "\n${GREEN}✅ All servers stopped successfully${NC}"
