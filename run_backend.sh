#!/bin/bash
set -e

echo "Starting Django Backend..."

# Navigate to backend directory
cd backend || exit 1

# Create virtual environment if missing
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Export settings
export DJANGO_SETTINGS_MODULE=backend.settings

# Apply migrations
python manage.py migrate

# Collect static files (safe even in dev)
python manage.py collectstatic --noinput || true

# Run server (IMPORTANT)
python manage.py runserver 0.0.0.0:8000
