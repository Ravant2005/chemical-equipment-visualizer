#!/bin/bash

echo "🚀 Chemical Equipment Visualizer Setup Script"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Install system dependencies (requires sudo)
echo "📦 Installing system dependencies..."
echo "Note: You may need to run 'sudo apt update && sudo apt install -y python3-pip nodejs npm' manually if this fails"

# Backend setup
echo "🐍 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
echo "Would you like to create a superuser? (y/n)"
read -r create_superuser
if [ "$create_superuser" = "y" ]; then
    python manage.py createsuperuser
fi

cd ..

# Frontend setup
echo "⚛️ Setting up frontend..."
cd frontend

# Install Node dependencies
echo "Installing Node.js dependencies..."
npm install

# Create environment file
if [ ! -f ".env" ]; then
    echo "Creating environment file..."
    cp .env.example .env
fi

cd ..

# Desktop setup
echo "🖥️ Setting up desktop application..."
cd desktop

# Install desktop dependencies (using same venv)
source ../backend/venv/bin/activate
pip install -r requirements.txt

cd ..

echo "✅ Setup complete!"
echo ""
echo "🚀 To start the application:"
echo "1. Backend: cd backend && source venv/bin/activate && python manage.py runserver"
echo "2. Frontend: cd frontend && npm run dev"
echo "3. Desktop: cd desktop && source ../backend/venv/bin/activate && python main.py"
echo ""
echo "📖 Check README.md for detailed instructions and deployment guide"