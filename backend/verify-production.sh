#!/bin/bash
# Railway Production Verification Script
# Replace YOUR_RAILWAY_URL with your actual Railway deployment URL

set -e

# Set your Railway backend URL here
BACKEND_URL="https://your-railway-app.railway.app"

echo "🔍 Testing Railway Production Deployment..."
echo "Backend URL: $BACKEND_URL"
echo ""

# Test 1: Health Check (CRITICAL - Railway depends on this)
echo "1. Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s -w "%{http_code}" "$BACKEND_URL/api/health/")
HTTP_CODE="${HEALTH_RESPONSE: -3}"
RESPONSE_BODY="${HEALTH_RESPONSE%???}"

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Health check: $HTTP_CODE"
    echo "   Response: $RESPONSE_BODY"
else
    echo "❌ Health check failed: $HTTP_CODE"
    echo "   Response: $RESPONSE_BODY"
    exit 1
fi

# Test 2: Django Admin
echo ""
echo "2. Testing Django admin..."
ADMIN_RESPONSE=$(curl -s -w "%{http_code}" "$BACKEND_URL/admin/")
ADMIN_CODE="${ADMIN_RESPONSE: -3}"

if [ "$ADMIN_CODE" = "200" ] || [ "$ADMIN_CODE" = "302" ]; then
    echo "✅ Django admin: $ADMIN_CODE"
else
    echo "❌ Django admin failed: $ADMIN_CODE"
fi

# Test 3: Auth Registration Endpoint
echo ""
echo "3. Testing auth registration endpoint..."
REG_RESPONSE=$(curl -s -w "%{http_code}" -X POST "$BACKEND_URL/api/auth/register/" \
    -H "Content-Type: application/json" \
    -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}')
REG_CODE="${REG_RESPONSE: -3}"

if [ "$REG_CODE" = "201" ] || [ "$REG_CODE" = "400" ]; then
    echo "✅ Auth registration endpoint: $REG_CODE"
else
    echo "❌ Auth registration failed: $REG_CODE"
fi

# Test 4: CORS Headers
echo ""
echo "4. Testing CORS headers..."
CORS_RESPONSE=$(curl -s -I -H "Origin: https://your-frontend.vercel.app" "$BACKEND_URL/api/health/")
if echo "$CORS_RESPONSE" | grep -q "Access-Control-Allow-Origin"; then
    echo "✅ CORS headers present"
else
    echo "⚠️  CORS headers missing - check CORS_ALLOWED_ORIGINS"
fi

echo ""
echo "🎉 Production verification complete!"
echo ""
echo "Expected Results:"
echo "✅ Health check: 200 with {\"status\":\"ok\"}"
echo "✅ Django admin: 200 or 302 (redirect to login)"
echo "✅ Auth endpoints: 201 (success) or 400 (validation error)"
echo "✅ CORS headers: Present for configured origins"