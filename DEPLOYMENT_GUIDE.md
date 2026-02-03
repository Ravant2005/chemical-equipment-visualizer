# 🚀 DEPLOYMENT GUIDE - Chemical Equipment Visualizer

## Step 1: Push to GitHub

### 1.1 Initialize Git Repository
```bash
cd /home/s-ravant-vignesh/Documents/chemicalequipment
git init
git add .
git commit -m "Initial commit - Chemical Equipment Visualizer"
```

### 1.2 Create GitHub Repository
1. Go to [github.com](https://github.com)
2. Click "New repository"
3. Name: `chemical-equipment-visualizer`
4. Make it Public
5. Don't initialize with README (we already have one)
6. Click "Create repository"

### 1.3 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/chemical-equipment-visualizer.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy Backend (Railway - Free)

### 2.1 Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Select "backend" folder

### 2.2 Configure Environment Variables
In Railway dashboard, go to Variables tab and add:
```
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DEBUG=False
ALLOWED_HOSTS=.railway.app
CORS_ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
DATABASE_URL=postgresql://user:pass@host:port/db
```

### 2.3 Add Database
1. Click "New" → "Database" → "PostgreSQL"
2. Copy the DATABASE_URL from Variables tab

## Step 3: Deploy Frontend (Vercel - Free)

### 3.1 Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Click "New Project"
4. Import your GitHub repository
5. Set Root Directory to `frontend`
6. Framework Preset: Vite
7. Build Command: `npm run build`
8. Output Directory: `dist`

### 3.2 Add Environment Variable
In Vercel project settings → Environment Variables:
```
VITE_API_URL=https://your-backend.railway.app/api
```

## Step 4: Update Backend for Production

### 4.1 Update CORS Settings
Update your Railway backend environment variables:
```
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-custom-domain.com
```

## Step 5: Test Deployment

1. **Backend Test**: Visit `https://your-backend.railway.app/api/`
2. **Frontend Test**: Visit `https://your-frontend.vercel.app`
3. **Full Test**: Register, login, upload CSV, generate PDF

## Alternative Free Hosting Options

### Backend Alternatives:
- **Render**: Similar to Railway, free tier available
- **Heroku**: Free tier discontinued, but still popular
- **PythonAnywhere**: Free tier with limitations

### Frontend Alternatives:
- **Netlify**: Similar to Vercel, drag-and-drop deployment
- **GitHub Pages**: For static sites only
- **Surge.sh**: Simple static hosting

## Quick Commands Summary

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/chemical-equipment-visualizer.git
git push -u origin main

# 2. Deploy Backend to Railway
# - Connect GitHub repo
# - Select backend folder
# - Add environment variables
# - Add PostgreSQL database

# 3. Deploy Frontend to Vercel
# - Connect GitHub repo
# - Set root directory to frontend
# - Add VITE_API_URL environment variable

# 4. Update URLs
# - Update CORS_ALLOWED_ORIGINS in Railway
# - Update VITE_API_URL in Vercel
```

## Troubleshooting

### Common Issues:
1. **CORS Error**: Update CORS_ALLOWED_ORIGINS with exact frontend URL
2. **Database Error**: Check DATABASE_URL format
3. **Build Error**: Ensure all dependencies are in requirements.txt/package.json
4. **Static Files**: Railway handles this automatically
5. **Environment Variables**: Double-check all variables are set correctly

### Logs:
- **Railway**: Check deployment logs in dashboard
- **Vercel**: Check function logs in dashboard

## Custom Domain (Optional)

### For Vercel:
1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

### For Railway:
1. Go to Settings → Domains
2. Add custom domain
3. Update DNS records

## Cost Breakdown (Free Tiers)

- **Railway**: 500 hours/month free
- **Vercel**: Unlimited static sites, 100GB bandwidth
- **PostgreSQL**: Included with Railway
- **Custom Domain**: $10-15/year (optional)

Your app will be live at:
- Backend: `https://your-app.railway.app`
- Frontend: `https://your-app.vercel.app`