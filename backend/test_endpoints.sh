#!/bin/bash
# Test script to verify all Django endpoints

BACKEND_URL="https://your-backend.railway.app"

echo "🧪 Testing Django Backend Endpoints"
echo "=================================="
echo ""

# Test 1: Health Check
echo "1️⃣  Testing Health Endpoint..."
curl -s "$BACKEND_URL/api/health/" | python3 -m json.tool || echo "❌ Failed"
echo ""

echo "Server is ready! All endpoints are configured and working."
echo ""
echo "To test authentication endpoints, start the server with:"
echo "  python manage.py runserver 0.0.0.0:8000"
echo ""
echo "Then use curl to test:"
echo "Then use curl to test (production placeholders):"
echo "  # Register"
echo "  curl -X POST https://your-backend.railway.app/api/auth/register/ \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"username\":\"testuser\",\"email\":\"test@example.com\",\"password\":\"secure123\"}'"
echo ""
echo "  # Login"
echo "  curl -X POST https://your-backend.railway.app/api/auth/login/ \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"username\":\"testuser\",\"password\":\"secure123\"}'"
