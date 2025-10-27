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

# Print header
echo -e "${PURPLE}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║        🔧 UMUHUZA PLATFORM - DEV MODE 🔧               ║"
echo "║         (Live Output in Separate Terminals)           ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

echo -e "${CYAN}This script will open servers in separate terminal windows${NC}"
echo -e "${CYAN}so you can see live output, errors, and verification codes.${NC}\n"

# Detect terminal emulator
if command -v gnome-terminal &> /dev/null; then
    TERM_CMD="gnome-terminal"
elif command -v xterm &> /dev/null; then
    TERM_CMD="xterm"
elif command -v konsole &> /dev/null; then
    TERM_CMD="konsole"
elif command -v terminator &> /dev/null; then
    TERM_CMD="terminator"
elif command -v bash &> /dev/null; then
    TERM_CMD="bash"
else
    echo -e "${RED}❌ Error: No supported terminal emulator found${NC}"
    echo -e "${YELLOW}💡 Available options: gnome-terminal, xterm, konsole, terminator${NC}"
    echo -e "${YELLOW}💡 Fallback: Use ./start.sh and then ./logs.sh in a separate terminal${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Detected terminal: $TERM_CMD${NC}\n"

# Check if virtual environment exists
if [ ! -d "$BACKEND_DIR/venv" ]; then
    echo -e "${RED}❌ Error: Virtual environment not found${NC}"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo -e "${YELLOW}⚠️  Installing frontend dependencies...${NC}"
    cd "$FRONTEND_DIR" && npm install
fi

echo -e "${BLUE}┌─────────────────────────────────────────────────────┐${NC}"
echo -e "${BLUE}│  Opening Backend Server in New Terminal Window     │${NC}"
echo -e "${BLUE}└─────────────────────────────────────────────────────┘${NC}\n"

# Start backend in new terminal
if [ "$TERM_CMD" = "gnome-terminal" ]; then
    gnome-terminal --title="Backend - Django Server" -- bash -c "
        cd '$BACKEND_DIR'
        source venv/bin/activate
        echo -e '\033[0;32m'
        echo '╔════════════════════════════════════════════════════════╗'
        echo '║           🐍 DJANGO BACKEND SERVER 🐍                  ║'
        echo '║              http://localhost:8000                     ║'
        echo '╚════════════════════════════════════════════════════════╝'
        echo -e '\033[0m\n'
        echo -e '\033[0;36m📌 You will see verification codes here!\033[0m'
        echo -e '\033[0;33m⚠️  Keep this window open - Press Ctrl+C to stop\033[0m\n'
        python manage.py migrate --no-input
        python manage.py runserver
        read -p 'Press Enter to close...'
    " &
elif [ "$TERM_CMD" = "xterm" ]; then
    xterm -title "Backend - Django Server" -hold -e "
        cd '$BACKEND_DIR'
        source venv/bin/activate
        echo '🐍 DJANGO BACKEND SERVER - http://localhost:8000'
        python manage.py migrate --no-input
        python manage.py runserver
    " &
elif [ "$TERM_CMD" = "konsole" ]; then
    konsole --new-tab --title "Backend Server" -e bash -c "
        cd '$BACKEND_DIR'
        source venv/bin/activate
        echo '🐍 DJANGO BACKEND SERVER - http://localhost:8000'
        python manage.py migrate --no-input
        python manage.py runserver
        read -p 'Press Enter to close...'
    " &
elif [ "$TERM_CMD" = "terminator" ]; then
    terminator -T "Backend Server" -e "bash -c '
        cd $BACKEND_DIR
        source venv/bin/activate
        echo \"🐍 DJANGO BACKEND SERVER - http://localhost:8000\"
        python manage.py migrate --no-input
        python manage.py runserver
        read -p \"Press Enter to close...\"
    '" &
fi

sleep 2

echo -e "${BLUE}┌─────────────────────────────────────────────────────┐${NC}"
echo -e "${BLUE}│  Opening Frontend Server in New Terminal Window    │${NC}"
echo -e "${BLUE}└─────────────────────────────────────────────────────┘${NC}\n"

# Start frontend in new terminal
if [ "$TERM_CMD" = "gnome-terminal" ]; then
    gnome-terminal --title="Frontend - React (Vite)" -- bash -c "
        cd '$FRONTEND_DIR'
        echo -e '\033[0;32m'
        echo '╔════════════════════════════════════════════════════════╗'
        echo '║           ⚛️  REACT FRONTEND SERVER ⚛️                  ║'
        echo '║              http://localhost:5173                     ║'
        echo '╚════════════════════════════════════════════════════════╝'
        echo -e '\033[0m\n'
        echo -e '\033[0;33m⚠️  Keep this window open - Press Ctrl+C to stop\033[0m\n'
        npm run dev
        read -p 'Press Enter to close...'
    " &
elif [ "$TERM_CMD" = "xterm" ]; then
    xterm -title "Frontend - React (Vite)" -hold -e "
        cd '$FRONTEND_DIR'
        echo '⚛️  REACT FRONTEND SERVER - http://localhost:5173'
        npm run dev
    " &
elif [ "$TERM_CMD" = "konsole" ]; then
    konsole --new-tab --title "Frontend Server" -e bash -c "
        cd '$FRONTEND_DIR'
        echo '⚛️  REACT FRONTEND SERVER - http://localhost:5173'
        npm run dev
        read -p 'Press Enter to close...'
    " &
elif [ "$TERM_CMD" = "terminator" ]; then
    terminator -T "Frontend Server" -e "bash -c '
        cd $FRONTEND_DIR
        echo \"⚛️  REACT FRONTEND SERVER - http://localhost:5173\"
        npm run dev
        read -p \"Press Enter to close...\"
    '" &
fi

sleep 2

echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║        ✅ DEV MODE SERVERS STARTED SUCCESSFULLY ✅      ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

echo -e "${CYAN}📍 Server URLs:${NC}"
echo -e "   ${PURPLE}Frontend:${NC} http://localhost:5173"
echo -e "   ${PURPLE}Backend:${NC}  http://localhost:8000"
echo -e "   ${PURPLE}Admin:${NC}    http://localhost:8000/admin\n"

echo -e "${YELLOW}📝 Live Output:${NC}"
echo -e "   ${CYAN}Check the newly opened terminal windows!${NC}"
echo -e "   ${CYAN}You'll see all logs, errors, and verification codes there.${NC}\n"

echo -e "${GREEN}✨ To stop servers:${NC}"
echo -e "   ${CYAN}Press Ctrl+C in each terminal window${NC}"
echo -e "   ${CYAN}or run: ./stop.sh${NC}\n"

echo -e "${BLUE}💡 Tip: Keep the terminal windows visible while developing!${NC}\n"
