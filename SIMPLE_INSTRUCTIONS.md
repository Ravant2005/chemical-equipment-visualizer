# 🚀 SIMPLE INSTRUCTIONS - How to Run the Application

## Step 1: Start the Backend Server

Open a terminal and run:
```bash
cd /home/s-ravant-vignesh/Documents/chemicalequipment
./start-backend.sh
```

**What you should see:**
- "Starting Django server on http://localhost:8000"
- Keep this terminal open - DON'T CLOSE IT

## Step 2: Start the Frontend (Web Application)

Open a NEW terminal and run:
```bash
cd /home/s-ravant-vignesh/Documents/chemicalequipment
./start-frontend.sh
```

**What you should see:**
- "Starting React development server on http://localhost:5173"
- Your web browser should automatically open
- If not, go to: http://localhost:5173

## Step 3: Use the Web Application

1. **Register a new account:**
   - Click "Sign up"
   - Enter username: `testuser`
   - Enter email: `test@example.com`
   - Enter password: `testpass123`
   - Click "Create Account"

2. **Upload CSV file:**
   - Click "Upload CSV File"
   - Select the file: `backend/sample_equipment_data.csv`
   - Wait for upload to complete

3. **View the results:**
   - See charts and statistics
   - Click "Generate PDF Report" to download report
   - Click "History" to see uploaded files

## Step 4: Try Desktop Application (Optional)

Open a NEW terminal and run:
```bash
cd /home/s-ravant-vignesh/Documents/chemicalequipment
./start-desktop.sh
```

**Login with same credentials:**
- Username: `testuser`
- Password: `testpass123`

## 🛑 How to Stop the Servers

- In each terminal, press `Ctrl + C` to stop the servers
- Close the terminal windows

## 🆘 If Something Goes Wrong

1. **Backend won't start:**
   ```bash
   cd /home/s-ravant-vignesh/Documents/chemicalequipment/backend
   source venv/bin/activate
   python manage.py runserver 8000
   ```

2. **Frontend won't start:**
   ```bash
   cd /home/s-ravant-vignesh/Documents/chemicalequipment/frontend
   npm install
   npm run dev
   ```

3. **Can't login:**
   - Make sure backend is running first
   - Try creating a new account
   - Check that both servers are running

## 📱 What Each Part Does

- **Backend (Port 8000):** Handles data, authentication, file uploads
- **Frontend (Port 5173):** The website you see in your browser
- **Desktop App:** Same functionality but as a desktop program

## 🎯 Test Data

Use the sample file located at:
`/home/s-ravant-vignesh/Documents/chemicalequipment/backend/sample_equipment_data.csv`

This file contains sample chemical equipment data for testing.

---

**That's it! The application should now be running and ready to use! 🎉**