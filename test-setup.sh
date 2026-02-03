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

# Test health (using production placeholder)
curl -s https://your-backend.railway.app/api/auth/login/ > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Backend is reachable (production placeholder)"
else
    echo "❌ Backend connection failed (check production URL or run local server)"
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