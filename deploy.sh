#!/bin/bash

echo "🚀 Chemical Equipment Visualizer - Deployment Setup"
echo "=================================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - Chemical Equipment Visualizer"
    echo "✅ Git repository initialized"
else
    echo "📦 Git repository already exists"
fi

# Check if remote origin exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo ""
    echo "🔗 GitHub Setup Required:"
    echo "1. Go to https://github.com"
    echo "2. Create new repository: 'chemical-equipment-visualizer'"
    echo "3. Make it public"
    echo "4. Don't initialize with README"
    echo ""
    read -p "Enter your GitHub username: " github_username
    
    if [ ! -z "$github_username" ]; then
        git remote add origin https://github.com/$github_username/chemical-equipment-visualizer.git
        git branch -M main
        echo "✅ Remote origin added"
        
        echo "📤 Pushing to GitHub..."
        git push -u origin main
        echo "✅ Code pushed to GitHub"
    fi
else
    echo "🔗 Remote origin already exists"
    echo "📤 Pushing latest changes..."
    git add .
    git commit -m "Update for deployment" || echo "No changes to commit"
    git push
fi

echo ""
echo "🎯 Next Steps:"
echo "1. Deploy Backend to Railway:"
echo "   - Go to https://railway.app"
echo "   - Sign up with GitHub"
echo "   - New Project → Deploy from GitHub"
echo "   - Select your repo → backend folder"
echo "   - Add PostgreSQL database"
echo "   - Set environment variables from backend/.env.production"
echo ""
echo "2. Deploy Frontend to Vercel:"
echo "   - Go to https://vercel.com"
echo "   - Sign up with GitHub"
echo "   - New Project → Import from GitHub"
echo "   - Root Directory: frontend"
echo "   - Set VITE_API_URL to your Railway backend URL"
echo ""
echo "3. Update URLs:"
echo "   - Update CORS_ALLOWED_ORIGINS in Railway with your Vercel URL"
echo "   - Test the deployed application"
echo ""
echo "📖 Full guide: DEPLOYMENT_GUIDE.md"