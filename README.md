# ChemViz Pro - Chemical Equipment Analytics

ChemViz Pro is a full-stack analytics platform for chemical equipment data. It includes a Django REST API, a Vite + React web dashboard, and a PyQt5 + Matplotlib desktop app. Users can upload CSV data, visualize equipment metrics, view history, and download PDF reports.

**Live Web App**
```text
https://chemical-equipment-visualizer-chi.vercel.app
```

**Features**
- Secure JWT authentication (register/login)
- CSV upload with validation
- Interactive charts for distribution and parameter comparison
- Upload history and dataset management
- PDF report generation
- Desktop client with the same visualizations

**Tech Stack**
- Backend: Django, Django REST Framework, PostgreSQL, Gunicorn
- Frontend: React, Vite, TailwindCSS, Chart.js
- Desktop: PyQt5, Matplotlib, Requests

**Project Structure**
- `backend/` Django API
- `frontend/` React web app
- `desktop/` PyQt5 desktop app
- `.github/workflows/` CI for desktop builds

---

## Local Development

**Backend (Django)**
1. `cd backend`
2. `python3 -m venv venv`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. Create `backend/.env` with at least: `SECRET_KEY=your-dev-secret`, `DEBUG=True`, `DATABASE_URL=` (optional for local SQLite), `FRONTEND_URL=http://localhost:5173`
6. `python manage.py migrate`
7. `python manage.py runserver 0.0.0.0:8000`

You can also use the helper script: `./run_backend.sh`

**Frontend (Vite + React)**
1. `cd frontend`
2. `npm install`
3. Create `frontend/.env` with `VITE_API_URL=http://127.0.0.1:8000/api`
4. `npm run dev`

You can also use the helper script: `./run_frontend.sh`

**Desktop (PyQt5)**
1. `cd desktop`
2. Optional: `export CHEMVIZ_API_URL=http://127.0.0.1:8000/api`
3. `python main.py`

---

## Environment Variables

**Backend (Render / production)**
- `SECRET_KEY` = strong random string
- `DEBUG` = `False`
- `DATABASE_URL` = Render PostgreSQL connection string
- `FRONTEND_URL` = your Vercel URL (example: `https://your-app.vercel.app`)

**Frontend (Vercel)**
- `VITE_API_URL` = `https://your-backend.onrender.com/api`
- `VITE_DESKTOP_WINDOWS_URL` = Windows download URL
- `VITE_DESKTOP_MAC_URL` = macOS download URL
- `VITE_DESKTOP_LINUX_URL` = Linux download URL

**Desktop**
- `CHEMVIZ_API_URL` = backend API URL

---

## CSV Format

Your CSV must include these headers:
- `Equipment Name`
- `Type`
- `Flowrate`
- `Pressure`
- `Temperature`

---

## API Endpoints (Core)

- `POST /api/accounts/auth/register/`
- `POST /api/accounts/auth/login/`
- `GET /api/accounts/auth/user/`
- `POST /api/equipments/datasets/upload/`
- `GET /api/equipments/datasets/history/`
- `GET /api/equipments/datasets/{id}/`
- `GET /api/equipments/datasets/{id}/generate_report/`

---

## Production Deployment

**Backend on Render**
1. Create a Render Web Service from this repo.
2. Use the start command from `Procfile`:
   - `gunicorn backend.wsgi:application --chdir backend --bind 0.0.0.0:$PORT --workers 4 --timeout 120`
3. Create a Render PostgreSQL database and set `DATABASE_URL`.
4. Set `SECRET_KEY`, `DEBUG=False`, and `FRONTEND_URL`.

**Frontend on Vercel**
1. Import the `frontend/` directory into Vercel.
2. Set `VITE_API_URL` to your Render API URL.
3. Set `VITE_DESKTOP_*` URLs to your desktop release assets.
4. Redeploy.

---

## Desktop Builds

**Local build**
1. `cd desktop`
2. `./build-desktop.sh`
3. Find output in `desktop/dist/`

**Automated build (recommended)**
1. Push to GitHub.
2. Tag a release and push it:
   - `git tag v1.0.0`
   - `git push origin v1.0.0`
3. GitHub Actions builds Windows, macOS, and Linux.
4. Release assets are attached automatically.

**Download URLs for the web button**
- `https://github.com/<owner>/<repo>/releases/latest/download/ChemVizPro-Windows.exe`
- `https://github.com/<owner>/<repo>/releases/latest/download/ChemVizPro-macOS.zip`
- `https://github.com/<owner>/<repo>/releases/latest/download/ChemVizPro-Linux.tar.gz`

---

## Notes

- PDF reports are generated from `/api/equipments/datasets/{id}/generate_report/`.
- Desktop and web apps both use JWT tokens.
- If a download button does not appear, check Vercel env vars and redeploy.
