#!/bin/bash

echo "🧪 Testing Chemical Equipment Visualizer..."
echo "==========================================="

# Test backend
echo "📡 Testing backend connection..."
cd /home/s-ravant-vignesh/Documents/chemicalequipment/backend
source venv/bin/activate

# Start backend in background
python manage.py runserver 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Test API endpoints
echo "🔍 Testing API endpoints..."

# Test health
curl -s http://localhost:8000/api/auth/login/ > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Backend is running successfully"
else
    echo "❌ Backend connection failed"
fi

# Kill backend
kill $BACKEND_PID 2>/dev/null

echo ""
echo "🎯 Ready to start the application!"
echo "Run these commands in separate terminals:"
echo ""
echo "1. Backend:  ./start-backend.sh"
echo "2. Frontend: ./start-frontend.sh"
echo "3. Desktop:  ./start-desktop.sh"