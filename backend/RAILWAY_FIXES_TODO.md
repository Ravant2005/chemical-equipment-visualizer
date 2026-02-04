# Railway Healthcheck Fixes - TODO List

## Phase 1: Core File Fixes ✅
- [x] 1. Fix `backend/backend/wsgi.py` - Remove malformed code
- [x] 2. Fix `backend/core/views.py` - Ensure clean health_check function
- [x] 3. Fix `backend/core/urls.py` - Correct view reference

## Phase 2: URL & CSRF Configuration ✅
- [x] 4. Fix `backend/backend/urls.py` - Add CSRF exemption
- [x] 5. Fix `backend/backend/settings.py` - Fix CSRF_TRUSTED_ORIGINS, remove duplicate

## Phase 3: Railway Configuration ✅
- [x] 6. Fix `backend/railway.toml` - Add --timeout 120 for robustness
- [x] 7. Fix `backend/railway.json` - Add collectstatic, align with railway.toml

## Phase 4: Verification ✅
- [x] 8. Verify all changes are consistent
- [x] 9. Test healthcheck endpoint logic

---

## Summary of Fixes Applied:

### 1. backend/backend/wsgi.py
- Removed malformed code (health_check function that was appended incorrectly)

### 2. backend/core/views.py  
- Clean, minimal health_check function with docstring
- Returns HttpResponse("OK", status=200) - pure, fast, no dependencies

### 3. backend/core/urls.py
- Fixed to import `health_check` instead of non-existent `health_check_view`

### 4. backend/backend/urls.py
- Added `@csrf_exempt` decorator to health_check endpoint
- Ensures CSRF middleware won't block healthcheck requests

### 5. backend/backend/settings.py
- Added preview URLs to CSRF_TRUSTED_ORIGINS
- Removed duplicate SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE settings
- Cleaned up duplicate CORS_ALLOW_ALL_ORIGINS

### 6. backend/railway.toml
- Added --timeout 120 to gunicorn command
- Added healthcheckTimeout = 300
- Clean formatting and comments

### 7. backend/railway.json
- Added preDeployCommand with collectstatic
- Added --timeout 120 to gunicorn
- Aligned with railway.toml configuration

---

## Final Configuration Checklist:

✅ Healthcheck endpoint: `/api/health/`
✅ Response: "OK" (plain text)
✅ Status code: 200
✅ CSRF: Exempt
✅ Auth: None
✅ Database: Not queried
✅ Response time: <50ms expected
✅ Gunicorn binds: 0.0.0.0:$PORT
✅ Workers: 2
✅ Timeout: 120 seconds
✅ preDeployCommand: migrate + collectstatic
✅ Restart policy: ON_FAILURE, 10 retries

