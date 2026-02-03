# 🔬 Chemical Equipment Visualizer

A full-stack hybrid application for analyzing and visualizing chemical equipment data with both web and desktop interfaces.

![React](https://img.shields.io/badge/React-18.2-blue?style=for-the-badge&logo=react)
![Django](https://img.shields.io/badge/Django-4.2-green?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

## ✨ Features

- **📊 CSV Upload & Processing**: Upload equipment data in CSV format
- **📈 Real-time Analytics**: Calculate averages, distributions, and statistics
- **🎨 Interactive Visualizations**: 
  - Web: Chart.js powered charts with advanced animations
  - Desktop: Matplotlib powered charts
- **📜 History Management**: Automatically stores last 5 uploaded datasets
- **📄 PDF Report Generation**: Create professional PDF reports
- **🔐 Authentication**: Secure user authentication with token-based auth
- **💻 Dual Interface**: Access from web browser or desktop application
- **🎯 Advanced UI**: Glassmorphism design with smooth animations

## 🏗️ Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend (Web)** | React.js + Chart.js | Show table + charts |
| **Frontend (Desktop)** | PyQt5 + Matplotlib | Same visualization in desktop |
| **Backend** | Python Django + DRF | Common backend API |
| **Data Handling** | Pandas | Reading CSV & analytics |
| **Database** | SQLite | Store last 5 uploaded datasets (auto-upgrades to PostgreSQL in production) |
| **Version Control** | Git & GitHub | Collaboration & submission |
| **Sample Data** | sample_equipment_data.csv | Sample CSV for testing |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/chemical-equipment-visualizer.git
cd chemical-equipment-visualizer

# Run automated setup
chmod +x setup.sh
./setup.sh
```

### Manual Setup

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend (new terminal)
cd frontend
npm install
npm run dev

# Desktop (new terminal)
cd desktop
pip install -r requirements.txt
python main.py
```

## 📁 Project Structure

```
chemical-equipment-visualizer/
├── backend/                 # Django REST API
│   ├── backend/            # Django settings
│   ├── equipment_api/      # Main API app
│   ├── manage.py
│   ├── requirements.txt
│   ├── railway.json        # Railway deployment config
│   ├── runtime.txt         # Python version
│   └── sample_equipment_data.csv
├── frontend/               # React Web Application
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   └── utils/         # Utility functions
│   ├── package.json
│   └── vite.config.js
├── desktop/               # PyQt5 Desktop Application
│   ├── main.py
│   └── requirements.txt
├── .env.example           # Environment variables template
├── Procfile              # Heroku deployment
└── README.md
```

## 🌍 Deployment Guide (Free Hosting)

### Backend Deployment (Railway - Recommended)

Railway provides free PostgreSQL and Python hosting with easy deployment.

#### Step 1: Prepare Your Repository

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit"
```

#### Step 2: Deploy to Railway

1. **Create Railway Account**: Go to [railway.app](https://railway.app) and sign up with GitHub
2. **Create New Project**: Click "New Project" → "Deploy from GitHub repo"
3. **Select Repository**: Choose your repository
4. **Configure Root Directory**: Set to `backend` (or deploy entire repo and use root directory)
5. **Add Environment Variables**: Go to Variables tab and add:

   ```
   SECRET_KEY=your-super-secret-key-here (generate with: python -c "import secrets; print(secrets.token_urlsafe(50))")
   DEBUG=False
   ALLOWED_HOSTS=.railway.app
   CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
   DATABASE_URL= (auto-provided by Railway PostgreSQL)
   ```

6. **Deploy**: Click "Deploy"

#### Step 3: Get Your Backend URL

After deployment, Railway will provide a URL like:
```
https://your-backend-project.railway.app
```

### Frontend Deployment (Vercel - Recommended)

Vercel provides free static site hosting with excellent performance.

#### Step 1: Connect to Vercel

1. **Create Vercel Account**: Go to [vercel.com](https://vercel.com) and sign up with GitHub
2. **Import Project**: Click "Add New" → "Project" → Import your GitHub repository
3. **Configure**:
   - Framework Preset: `Vite`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

#### Step 2: Add Environment Variables

In Vercel project settings, add:
```
VITE_API_URL=https://your-backend-project.railway.app
```

#### Step 3: Deploy

Click "Deploy" and Vercel will automatically build and deploy your frontend.

### Alternative: Render Deployment

#### Backend (Render)

1. Create account at [render.com](https://render.com)
2. Create Web Service → Connect GitHub repo
3. Configure:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn backend.wsgi:application`
4. Add Environment Variables (same as Railway)
5. Create PostgreSQL database in Render and connect via `DATABASE_URL`

#### Frontend (Netlify)

1. Create account at [netlify.com](https://netlify.com)
2. Connect GitHub repository
3. Configure:
   - Base Directory: `frontend`
   - Build Command: `npm run build`
   - Publish Directory: `dist`
4. Add Environment Variable: `VITE_API_URL=https://your-backend.render.com`

## 🔧 API Configuration

### Frontend API URL Setup

The frontend needs to know your backend API URL. Set this in two places:

1. **Vercel Environment Variable**:
   ```
   VITE_API_URL=https://your-backend.railway.app
   ```

2. **Frontend Code** (for local development):
   Create `.env` file in `frontend/` directory:
   ```
   VITE_API_URL=http://localhost:8000
   ```

### Desktop App API URL

The desktop app can connect to your deployed backend:

1. **Using Environment Variable**:
   ```bash
   export CHEMVIZ_API_URL=https://your-backend.railway.app/api
   python main.py
   ```

2. **In-App Configuration**: Click "⚙️ Configure API URL" on the login screen

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login and get token |
| POST | `/api/auth/logout/` | Logout (invalidate token) |
| GET | `/api/auth/user/` | Get current user info |

### Datasets
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/datasets/upload/` | Upload CSV file |
| GET | `/api/datasets/` | List all datasets |
| GET | `/api/datasets/{id}/` | Get dataset details |
| GET | `/api/datasets/{id}/summary/` | Get dataset summary |
| GET | `/api/datasets/{id}/generate_report/` | Download PDF report |
| GET | `/api/datasets/history/` | Get last 5 uploads |
| DELETE | `/api/datasets/{id}/` | Delete dataset |

## 📝 CSV Format

Your CSV file should have the following columns:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Compressor-1,Compressor,95,8.4,95
Heat-Exchanger-1,Heat Exchanger,85,6.1,150
...
```

Sample file: `backend/sample_equipment_data.csv`

## 🛠️ Development

### Running Locally

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
python manage.py runserver

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Desktop
cd desktop
source ../backend/venv/bin/activate
python main.py
```

### Access Points
- **Web App**: http://localhost:5173
- **API**: http://localhost:8000
- **Admin**: http://localhost:8000/admin (create superuser first)

## 🧪 Testing

```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test
```

## 📦 Building for Production

### Frontend Build
```bash
cd frontend
npm run build
# Output in dist/ folder
```

### Desktop Build (Executable)
```bash
cd desktop
pip install pyinstaller
pyinstaller --onefile --windowed main.py
# Output in dist/ folder
```

## 🔐 Security Checklist for Production

- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY` (50+ characters)
- [ ] Configure `ALLOWED_HOSTS` with production domains
- [ ] Set up HTTPS (automatic on Railway/Vercel)
- [ ] Configure `CORS_ALLOWED_ORIGINS`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up regular database backups

## 📊 Monitoring & Logs

### Railway Logs
View logs in Railway dashboard under the service's logs tab.

### Vercel Logs
View function logs in Vercel dashboard under the deployment details.

## 🐛 Troubleshooting

### CORS Errors
```python
# In backend/settings.py, add your frontend URL:
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend.vercel.app",
]
```

### Database Migrations
```bash
cd backend
python manage.py migrate
```

### Static Files Not Loading
```bash
cd backend
python manage.py collectstatic --noinput
```

### Port Already in Use
```bash
# Backend
python manage.py runserver 8001

# Frontend
npm run dev -- --port 3001
```

## 📈 Performance Optimization

### Backend
- Enable database connection pooling
- Use Redis for caching (optional)
- Optimize database queries

### Frontend
- Enable code splitting
- Optimize images and assets
- Use CDN for static files

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Sample data provided by the internship program
- Icons from Lucide React
- UI inspiration from modern dashboard designs
- Glassmorphism effects inspired by modern design trends

## 📧 Support

For questions or issues, please open a GitHub issue or contact: your.email@example.com

---

Made with ❤️ for Chemical Equipment Analysis

