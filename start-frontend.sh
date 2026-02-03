#!/bin/bash

echo "⚛️ Starting Chemical Equipment Visualizer Frontend..."
echo "===================================================="

# Navigate to frontend directory
cd "$(dirname "$0")/frontend"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start the development server
echo "🌐 Starting React development server on http://localhost:5173"
echo "Press Ctrl+C to stop the server"
echo ""
npm run dev