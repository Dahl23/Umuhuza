#!/bin/bash

# Script to check and fix listing statuses

echo "============================================================"
echo "LISTING STATUS CHECKER AND FIXER"
echo "============================================================"
echo ""
echo "Activating virtual environment..."

# Activate virtual environment (adjust path if needed)
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d "../venv" ]; then
    source ../venv/bin/activate
elif [ -d "env" ]; then
    source env/bin/activate
else
    echo "⚠️  Virtual environment not found. Using system Python..."
fi

echo "Running diagnostic script..."
echo ""

# Run the fix script
python manage.py shell < fix_listing_status.py

echo ""
echo "✅ Done! Refresh your browser to see the changes."
