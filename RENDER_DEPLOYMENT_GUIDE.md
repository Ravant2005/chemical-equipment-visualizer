# Django Backend Production Deployment - Render

## 🔍 Audit Summary

### What Was Missing:
1. **ALLOWED_HOSTS** - Only had `localhost` and `127.0.0.1`, missing Render's `.onrender.com` domains
2. **CSRF_TRUSTED_ORIGINS** - Missing Vercel frontend domains
3. **CORS_ALLOWED_ORIGINS** - Missing Vercel frontend domains
4. **WhiteNoise Middleware** - Not included in MIDDLEWARE list
5. **DATABASE Configuration** - Only SQLite, no PostgreSQL via `DATABASE_URL`
6. **SECURITY Settings** - Missing production security headers
7. **DEBUG Setting** - Hardcoded to `True`, no environment-based detection
8. **Procfile** - Missing `--chdir backend` and `$PORT` for Render
9. **Frontend API** - Hardcoded localhost, won't work with Vercel deployment

### Why It Caused Deployment Issues:
- Render services use dynamic subdomains (e.g., `myapp.onrender.com`)
- Vercel frontend makes cross-origin requests requiring CORS/CSRF configuration
- PostgreSQL requires `DATABASE_URL` connection string
- Gunicorn needs `$PORT` from Render's environment
- Static files need WhiteNoise for production serving

---

## ✏️ Exact Code Changes

### 1. `backend/backend/settings.py`

**Lines Added/Modified:**

```python
# At the top - import dj_database_url
import dj_database_url

# DEBUG: Auto-detect production vs development
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes')

# ALLOWED_HOSTS: Configure for Render + localhost + Vercel frontend
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.onrender.com',  # All Render services
]

# CSRF trusted origins for cross-origin requests
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://*.vercel.app',  # Vercel frontend deployments
]
```

```python
# MIDDLEWARE - Added WhiteNoise (after SecurityMiddleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files serving
    # ... rest of middleware
]
```

```python
# DATABASES - PostgreSQL via DATABASE_URL with SQLite fallback
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PostgreSQL configuration for Render
db_from_env = dj_database_url.config(conn_max_age=500, ssl_require=True)
DATABASES['default'] = dj_database_url.config(default=None, conn_max_age=500)
if not DATABASES['default']:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
```

```python
# Static Files & Security
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings (only when DEBUG=False)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
```

```python
# CORS - Added Vercel support
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://*.vercel.app",  # Vercel frontend deployments
]
CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
```

### 2. `Procfile` (root directory)

**Complete Replacement:**
```
web: gunicorn backend.wsgi:application --chdir backend --bind 0.0.0.0:$PORT --workers 4 --timeout 120 --access-logfile - --error-logfile -
```

### 3. `frontend/src/services/api.js`

**Lines Added/Modified:**
```javascript
// Dynamic API URL detection
const getApiBaseUrl = () => {
  // Check for environment variable (production on Vercel)
  const envUrl = import.meta.env.VITE_API_URL || import.meta.env.VITE_BACKEND_URL;
  
  if (envUrl) {
    return envUrl;
  }
  
  // Fallback to localhost for local development
  return 'http://127.0.0.1:8000/api';
};
```

---

## ⚙️ Render Configuration

### Start Command
```
gunicorn backend.wsgi:application --chdir backend --bind 0.0.0.0:$PORT --workers 4 --timeout 120
```

### Required Environment Variables

| Variable | Value | Required | Description |
|----------|-------|----------|-------------|
| `DATABASE_URL` | `postgres://user:pass@host:5432/db` | **YES** | Render PostgreSQL connection string |
| `SECRET_KEY` | `<strong-random-string>` | **YES** | Django secret key (minimum 50 chars) |
| `DEBUG` | `False` | **YES** | Must be `False` for production |
| `ALLOWED_HOSTS` | `.onrender.com,localhost` | NO | Already configured in settings.py |
| `CSRF_TRUSTED_ORIGINS` | `https://*.vercel.app` | NO | Already configured in settings.py |
| `VITE_API_URL` | `https://your-backend.onrender.com/api` | Optional | For Vercel frontend |

### Database Connection Instructions

1. **Create PostgreSQL Database on Render:**
   - Go to Render Dashboard → New → PostgreSQL
   - Note the `DATABASE_URL` from the connection details
   - Wait for the database to be provisioned (green status)

2. **Add Environment Variable:**
   - Go to your Web Service → Environment
   - Add `DATABASE_URL` with the value from step 1
   - Add `SECRET_KEY` with a strong random value
   - Set `DEBUG` to `False`

---

## ✅ Verification Checklist

### 1. Health Check Verification
```bash
curl https://your-backend.onrender.com/api/health/
```
**Expected Response:** `OK` (HTTP 200)

### 2. CSRF/CORS Testing
```bash
# Test with Vercel origin (simulated)
curl -X POST https://your-backend.onrender.com/api/accounts/auth/login/ \
  -H "Content-Type: application/json" \
  -H "Origin: https://your-frontend.vercel.app" \
  -d '{"username":"test","password":"test"}' \
  -v
```
**Expected:** No CORS errors in response headers

### 3. Frontend ↔ Backend Integration Test
1. Deploy frontend to Vercel with `VITE_API_URL` env var set to your Render backend URL
2. Test login/register from Vercel domain
3. Verify JWT tokens are stored and sent correctly
4. Test equipment API endpoints

### 4. Deployment Success Indicators
- [ ] Health check returns HTTP 200
- [ ] `python manage.py migrate` runs successfully
- [ ] `collectstatic` completes without errors
- [ ] Login/Register endpoints work from frontend
- [ ] No CORS errors in browser console
- [ ] Static files load correctly (admin, DRF browsable API)

### 5. Local Development Verification
```bash
cd backend
python manage.py migrate
python manage.py runserver
```
**Expected:** Everything works as before (SQLite, localhost)

---

## 🧠 Production Notes

### What NOT to Change Later:
1. ❌ Don't modify `ALLOWED_HOSTS` to remove `.onrender.com`
2. ❌ Don't set `DEBUG=True` in production
3. ❌ Don't hardcode secrets in `settings.py`
4. ❌ Don't remove `CSRF_TRUSTED_ORIGINS` Vercel entries
5. ❌ Don't change the auth strategy (JWT is working)

### Future-Proofing Suggestions:
1. **Add logging:** Configure `LOGGING` for production error tracking
2. **Rate limiting:** Add `django-ratelimit` for API protection
3. **Caching:** Add Redis cache backend for sessions/API responses
4. **Monitoring:** Integrate Sentry or similar for error tracking
5. **Database backups:** Enable Render's automatic backups for PostgreSQL

### Performance Considerations:
- Workers: Start with 4 (as in Procfile), adjust based on Render's plan
- Timeout: 120 seconds is generous; can reduce to 60
- Connection pooling: `conn_max_age=500` (5 minutes) is optimal for PostgreSQL
- Static files: WhiteNoise compression reduces file size by ~70%

---

## 📋 Quick Reference

### Files Modified:
1. ✅ `backend/backend/settings.py` - Production configuration
2. ✅ `Procfile` - Render deployment command
3. ✅ `frontend/src/services/api.js` - Dynamic API URL

### Files NOT Modified (intentionally):
- `backend/backend/urls.py` - Health endpoint already exists
- `backend/core/views.py` - Health check already working
- `backend/requirements.txt` - All dependencies already present
- Any models, serializers, or business logic

