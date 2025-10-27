#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${PURPLE}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║           📝 UMUHUZA PLATFORM - LIVE LOGS 📝           ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

# Check if log files exist
if [ ! -f "$SCRIPT_DIR/backend.log" ] && [ ! -f "$SCRIPT_DIR/frontend.log" ]; then
    echo -e "${YELLOW}⚠️  No log files found. Are the servers running?${NC}"
    echo -e "${CYAN}💡 Run ./start.sh first, then run this script${NC}\n"
    exit 1
fi

# Check which logs to show
case "${1:-both}" in
    backend|back|be)
        echo -e "${CYAN}📊 Showing BACKEND logs only (Ctrl+C to exit)${NC}"
        echo -e "${YELLOW}Location: $SCRIPT_DIR/backend.log${NC}\n"
        tail -f "$SCRIPT_DIR/backend.log"
        ;;
    frontend|front|fe)
        echo -e "${CYAN}📊 Showing FRONTEND logs only (Ctrl+C to exit)${NC}"
        echo -e "${YELLOW}Location: $SCRIPT_DIR/frontend.log${NC}\n"
        tail -f "$SCRIPT_DIR/frontend.log"
        ;;
    both|*)
        echo -e "${CYAN}📊 Showing BOTH logs (Ctrl+C to exit)${NC}"
        echo -e "${GREEN}Backend:${NC}  $SCRIPT_DIR/backend.log"
        echo -e "${GREEN}Frontend:${NC} $SCRIPT_DIR/frontend.log\n"
        echo -e "${YELLOW}════════════════════════════════════════════════════════${NC}\n"

        # Use multitail if available, otherwise use tail with labels
        if command -v multitail &> /dev/null; then
            multitail -s 2 -l "tail -f $SCRIPT_DIR/backend.log" -l "tail -f $SCRIPT_DIR/frontend.log"
        else
            # Fallback: show both with tail
            tail -f "$SCRIPT_DIR/backend.log" "$SCRIPT_DIR/frontend.log"
        fi
        ;;
esac
