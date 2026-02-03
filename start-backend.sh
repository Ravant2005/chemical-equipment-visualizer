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
echo "🌐 Starting Django server on http://localhost:8001"
echo "Press Ctrl+C to stop the server"
echo ""
python manage.py runserver 8001