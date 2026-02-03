# 🚀 Complete Deployment Guide

This guide provides step-by-step instructions to deploy the Chemical Equipment Visualizer on **free hosting services**.

## 📋 Deployment Overview

| Component | Free Hosting | URL Format |
|-----------|--------------|------------|
| Backend (API) | Railway | `https://your-app.railway.app` |
| Frontend (Web) | Vercel | `https://your-app.vercel.app` |
| Database | Railway PostgreSQL | Auto-provisioned |
| Desktop App | N/A | Standalone (not deployable) |

---

## 🗄️ Part 1: Database Setup (Railway PostgreSQL)

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Click "Sign Up" and register with GitHub
3. Authorize Railway to access your GitHub repositories

### Step 2: Provision PostgreSQL
1. Click "New Project" → "Provision PostgreSQL"
2. Wait for PostgreSQL to be created
3. Go to the "Variables" tab
4. Copy the `DATABASE_URL` value (format: `postgresql://user:pass@host:port/db`)

---

## 🐍 Part 2: Backend Deployment (Railway)

### Step 1: Push Code to GitHub
```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - ready for deployment"

# Create GitHub repository on GitHub.com, then:
git remote add origin https://github.com/YOURUSERNAME/YOURREPO.git
git push -u origin main
```

### Step 2: Deploy Backend to Railway
1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. **Important**: Set the root directory to `backend` or configure the start command

### Step 3: Configure Environment Variables
In Railway project settings, add these variables:

| Variable | Value | Notes |
|----------|-------|-------|
| `SECRET_KEY` | `django-insecure-xxxx...` | Generate with: `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `DEBUG` | `False` | Must be False for production |
| `ALLOWED_HOSTS` | `.railway.app` | Railway subdomain |
| `CORS_ALLOWED_ORIGINS` | `https://your-frontend.vercel.app` | Your Vercel URL (after deployment) |
| `DATABASE_URL` | (auto-filled) | From PostgreSQL service |

### Step 4: Verify Backend
After deployment, visit your Railway URL:
```
https://your-backend-project.railway.app/api/datasets/
```
You should see a 401 error (unauthorized) - this means the API is working!

---

## ⚛️ Part 3: Frontend Deployment (Vercel)

### Step 1: Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Click "Sign Up" and register with GitHub
3. Authorize Vercel to access your GitHub repositories

### Step 2: Import Project
1. Click "Add New" → "Project"
2. Import your GitHub repository
3. Configure these settings:

| Setting | Value |
|---------|-------|
| Framework Preset | `Vite` |
| Root Directory | `frontend` |
| Build Command | `npm run build` |
| Output Directory | `dist` |

### Step 3: Add Environment Variables
In Vercel project settings, add:

| Variable | Value |
|----------|-------|
| `VITE_API_URL` | `https://your-backend-project.railway.app` |

**Note**: Remove trailing slash from URL!

### Step 4: Deploy
Click "Deploy" and wait for the build to complete.

### Step 5: Verify Frontend
1. Visit your Vercel URL
2. Try to register/login
3. Upload a CSV file
4. Check that charts display correctly

---

## 🔗 Part 4: Connect Frontend to Backend

### Step 1: Update CORS Settings
After deploying frontend, go back to Railway and update `CORS_ALLOWED_ORIGINS`:

```
CORS_ALLOWED_ORIGINS = https://your-frontend.vercel.app,https://your-project-name.vercel.app
```

### Step 2: Redeploy Backend
In Railway, click "Redeploy" to apply the new CORS settings.

### Step 3: Test End-to-End
1. Open your Vercel frontend URL
2. Register a new user
3. Upload the sample CSV file
4. Verify charts and data display correctly
5. Check history page

---

## 🔧 Configuration Reference

### Backend Environment Variables

```env
# Required
SECRET_KEY=your-super-secret-key-minimum-50-characters
DEBUG=False
ALLOWED_HOSTS=.railway.app

# CORS - update with your frontend URL after deployment
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app

# Database - auto-provided by Railway
DATABASE_URL=postgresql://...
```

### Frontend Environment Variables

```env
# Your backend API URL (no trailing slash, no /api)
VITE_API_URL=https://your-backend.railway.app
```

---

## 📱 Desktop Application

The desktop application cannot be deployed to web hosting. It runs locally and connects to your deployed backend.

### Using with Deployed Backend

**Option 1: Environment Variable**
```bash
# Linux/Mac
export CHEMVIZ_API_URL=https://your-backend.railway.app/api
python main.py

# Windows
set CHEMVIZ_API_URL=https://your-backend.railway.app/api
python main.py
```

**Option 2: In-App Configuration**
1. Launch the desktop app
2. Click "⚙️ Configure API URL" on the login screen
3. Enter your backend URL: `https://your-backend.railway.app`
4. Click OK

---

## 🧪 Testing Your Deployment

### 1. API Health Check
```bash
curl https://your-backend.railway.app/api/auth/login/
# Should return: {"detail":"Method \"GET\" not allowed."}
```

### 2. Frontend Access
- Visit `https://your-frontend.vercel.app`
- Check browser console for errors
- Verify no CORS errors

### 3. Full Workflow Test
1. Register a new user account
2. Login with credentials
3. Upload `backend/sample_equipment_data.csv`
4. Verify charts render correctly
5. Check History page
6. Generate PDF report

---

## 🚨 Troubleshooting

### CORS Errors
**Symptom**: "Access to XMLHttpRequest has been blocked by CORS policy"

**Solution**:
1. Go to Railway dashboard
2. Update `CORS_ALLOWED_ORIGINS` with your exact Vercel URL
3. Redeploy the backend service

### 500 Internal Server Error
**Symptom**: API returns 500 error

**Solutions**:
1. Check Railway logs for error details
2. Verify `SECRET_KEY` is set
3. Ensure `DATABASE_URL` is valid
4. Check migrations ran successfully

### Static Files Not Loading
**Symptom**: CSS/JS files return 404

**Solution**:
The `Procfile` includes `collectstatic` command. If issues persist:
1. Check `STATIC_ROOT` in settings.py
2. Verify whitenoise is in middleware

### Frontend Can't Reach API
**Symptom**: Network errors in browser console

**Solutions**:
1. Verify `VITE_API_URL` is correct in Vercel
2. Ensure no trailing slash in URL
3. Check backend is deployed and running
4. Verify CORS settings include your Vercel URL

### Database Connection Failed
**Symptom**: "django.db.utils.OperationalError"

**Solutions**:
1. Verify `DATABASE_URL` is set in Railway
2. Check PostgreSQL service is running
3. Ensure database migrations ran

---

## 📊 Performance Tips

### Frontend Optimization
- Vercel automatically optimizes static files
- Use production build: `npm run build`
- Enable GZIP compression (automatic on Vercel)

### Backend Optimization
- Use connection pooling (PostgreSQL default)
- Add Redis caching for frequent queries
- Enable database indexes on Equipment model

---

## 🔐 Security Best Practices

1. **Use Strong SECRET_KEY**: Generate with `python -c "import secrets; print(secrets.token_urlsafe(50))"`

2. **Keep DEBUG=False**: Never deploy with DEBUG=True

3. **Limit ALLOWED_HOSTS**: Only include necessary domains

4. **Secure CORS**: Only allow your frontend domains

5. **HTTPS Only**: Railway and Vercel provide automatic HTTPS

6. **Database Backups**: Railway provides automatic daily backups for PostgreSQL

---

## 💰 Free Tier Limits

### Railway (Backend)
- **Free**: $5 credit/month (enough for small projects)
- **Limits**: 500 hours execution, 1GB storage
- **PostgreSQL**: Free tier includes 1GB storage

### Vercel (Frontend)
- **Free**: 100GB bandwidth/month
- **Limits**: 100 hours build time, 6 sites
- **SSL**: Automatic free SSL certificates

---

## 🎯 Next Steps After Deployment

1. **Custom Domain** (Optional):
   - Railway: Add custom domain in project settings
   - Vercel: Add custom domain in project settings
   - Update DNS records as instructed

2. **Monitoring**:
   - Set up uptime monitoring (UptimeRobot - free)
   - Configure error tracking (Sentry - free tier)

3. **Backup**:
   - Railway provides automatic PostgreSQL backups
   - Enable additional backup retention if needed

4. **CI/CD**:
   - Pushes to GitHub automatically trigger redeploy
   - Configure branch protection for production

---

## 📞 Need Help?

1. **Check Logs First**:
   - Railway: View logs in dashboard
   - Vercel: View function logs in dashboard

2. **Common Solutions**:
   - Restart/redeploy the service
   - Check environment variables
   - Verify all required variables are set

3. **GitHub Issues**: Open an issue for bugs or questions

---

**🎉 Deployment Complete!**
Your Chemical Equipment Visualizer is now live and accessible worldwide!

