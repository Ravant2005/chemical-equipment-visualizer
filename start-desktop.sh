#!/bin/bash

echo "🖥️ Starting Chemical Equipment Visualizer Desktop App..."
echo "========================================================"

# Navigate to desktop directory
cd "$(dirname "$0")/desktop"

# Activate virtual environment (same as backend)
echo "📦 Activating virtual environment..."
source ../backend/venv/bin/activate

# Install desktop dependencies if needed
pip install -r requirements.txt > /dev/null 2>&1

# Start the desktop application
echo "🚀 Starting desktop application..."
echo ""
python main.py