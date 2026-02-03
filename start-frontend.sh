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
echo "🌐 Starting React development server (local: http://127.0.0.1:5173 — production: https://your-frontend.vercel.app)"
echo "Press Ctrl+C to stop the local server"
echo ""
npm run dev