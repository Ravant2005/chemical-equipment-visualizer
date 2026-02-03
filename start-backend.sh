#!/bin/bash

echo "🚀 Starting Chemical Equipment Visualizer Backend..."
echo "=================================================="

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if migrations are needed
echo "🗄️ Checking database..."
python manage.py migrate

# Start the server
echo "🌐 Starting Django server (local: http://127.0.0.1:8001 — production: https://your-backend.railway.app)"
echo "Press Ctrl+C to stop the local server"
echo ""
python manage.py runserver 8001