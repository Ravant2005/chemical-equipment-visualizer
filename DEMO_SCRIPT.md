```markdown
# 🎬 Demo Script - Chemical Equipment Visualizer

This script provides step-by-step instructions to demonstrate all features of the Chemical Equipment Visualizer.

## 🚀 Prerequisites

- Backend server running on `https://your-backend.railway.app`
- Frontend server running on `https://your-frontend.vercel.app`
- Desktop application ready to launch
- Sample CSV file available (`backend/sample_equipment_data.csv`)

## 📱 Web Application Demo

### Step 1: User Registration

1. **Open browser** and navigate to `https://your-frontend.vercel.app`
2. **Click "Sign up"** link on the login page
3. **Fill registration form**:
   - Username: `demo_user`
   - Email: `demo@example.com`
   - Password: `demo123456`
   - Confirm Password: `demo123456`
4. **Click "Create Account"**
5. **Verify**: You should be automatically logged in and redirected to dashboard

### Step 2: Dashboard Overview

1. **Observe the UI**:
   - Animated background with particles
   - Glassmorphism design elements
   - Smooth animations and transitions
   - Responsive navigation bar

2. **Note the features**:
   - Upload section prominently displayed
   - No data message (since no files uploaded yet)
   - Clean, modern interface

### Step 3: CSV File Upload

1. **Click "Upload CSV File"** button
2. **Select file**: Choose `backend/sample_equipment_data.csv`
3. **Watch the upload process**:
   - Button shows "Uploading..." state
   - Success toast notification appears
   - Dashboard updates with new data

### Step 4: Data Visualization

1. **Statistics Cards**: Observe the animated statistics cards showing:
   - Total Equipment: 15
   - Average Flowrate: ~125.33
   - Average Pressure: ~5.95
   - Average Temperature: ~118.67

2. **Charts Section**:
   - **Pie Chart**: Equipment type distribution
     - Pumps, Compressors, Valves, Heat Exchangers, etc.
     - Interactive hover effects
   - **Bar Chart**: Parameter comparison
     - Flowrate, Pressure, Temperature for each equipment
     - Animated bars with different colors

3. **Interactive Features**:
   - Hover over chart elements for tooltips
   - Smooth animations on load
   - Responsive design adapts to screen size

### Step 5: PDF Report Generation

1. **Click "Generate PDF Report"** button
2. **Wait for processing** (should be quick)
3. **Download starts automatically**
4. **Open the PDF** to verify contents:
   - Professional header and formatting
   - Summary statistics table
   - Equipment distribution table
   - Detailed equipment list
   - Timestamp and metadata

### Step 6: History Management

1. **Click "History"** in the navigation
2. **Observe the history page**:
   - Shows the uploaded dataset
   - Upload timestamp
   - Summary statistics
   - Equipment type distribution tags

3. **Test actions**:
   - **Download button**: Generates PDF report
   - **Delete button**: Removes dataset (confirm dialog)

### Step 7: Upload Additional Files

1. **Return to Dashboard**
2. **Upload the same file 4 more times** (to test history limit)
3. **Go to History page**
4. **Verify**: Only last 5 uploads are shown

### Step 8: Logout

1. **Click logout button** (red button in navbar)
2. **Verify**: Redirected to login page
3. **Try accessing dashboard directly**: Should redirect to login

## 🖥️ Desktop Application Demo

### Step 1: Launch Desktop App

1. **Open terminal** in desktop directory
2. **Run**: `python main.py`
3. **Observe**: Modern dark-themed login window opens

### Step 2: Login

1. **Enter credentials**:
   - Username: `demo_user`
   - Password: `demo123456`
2. **Click "Login"**
3. **Verify**: Main application window opens

### Step 3: Desktop Interface Overview

1. **Header section**: Shows app name and logged-in user
2. **Tabbed interface**: Dashboard and History tabs
3. **Upload section**: File selection and processing
4. **Statistics area**: Summary information
5. **Charts area**: Matplotlib visualizations
6. **Data table**: Equipment details

### Step 4: File Upload (Desktop)

1. **Click "Select File"**
2. **Choose**: `backend/sample_equipment_data.csv`
3. **Click "Upload & Process"**
4. **Watch the process**:
   - File uploads to server
   - Statistics update
   - Charts render
   - Table populates

### Step 5: Desktop Visualizations

1. **Pie Chart**: Equipment distribution with matplotlib styling
2. **Bar Chart**: Parameter comparison with grouped bars
3. **Data Table**: Scrollable table with all equipment details
4. **Statistics**: Formatted summary information

### Step 6: History Tab (Desktop)

1. **Click "History" tab**
2. **Click "Refresh History"**
3. **Observe**: Table shows all uploaded datasets
4. **Note**: Same data as web application (shared backend)

## 🧪 API Testing (Optional)

### Using curl or Postman

1. **Register a new user**:
```bash
curl -X POST https://your-backend.railway.app/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"api_user","email":"api@example.com","password":"api123456"}'
```

2. **Login and get token**:
```bash
curl -X POST https://your-backend.railway.app/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"api_user","password":"api123456"}'
```

3. **Upload CSV file**:
```bash
curl -X POST https://your-backend.railway.app/api/datasets/upload/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -F "file=@backend/sample_equipment_data.csv"
```

4. **Get history**:
```bash
curl -X GET https://your-backend.railway.app/api/datasets/history/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## 🎯 Feature Demonstration Checklist

### ✅ Authentication
- [ ] User registration works
- [ ] User login works
- [ ] Token-based authentication
- [ ] Logout functionality
- [ ] Protected routes

### ✅ File Upload
- [ ] CSV file validation
- [ ] File size limits
- [ ] Error handling for invalid files
- [ ] Success feedback

### ✅ Data Processing
- [ ] CSV parsing with Pandas
- [ ] Statistics calculation
- [ ] Equipment type distribution
- [ ] Data validation

### ✅ Visualizations
- [ ] Interactive pie chart
- [ ] Animated bar chart
- [ ] Responsive design
- [ ] Chart tooltips and hover effects

### ✅ PDF Reports
- [ ] Professional formatting
- [ ] Complete data inclusion
- [ ] Download functionality
- [ ] Proper file naming

### ✅ History Management
- [ ] Last 5 uploads stored
- [ ] Automatic cleanup
- [ ] Delete functionality
- [ ] Summary information

### ✅ UI/UX
- [ ] Glassmorphism design
- [ ] Smooth animations
- [ ] Responsive layout
- [ ] Loading states
- [ ] Error handling
- [ ] Toast notifications

### ✅ Desktop Application
- [ ] PyQt5 interface
- [ ] Matplotlib charts
- [ ] Data table display
- [ ] API integration
- [ ] Cross-platform compatibility

## 🐛 Common Issues and Solutions

### Backend Issues

1. **Server not starting**:
   - Check if port 8000 is available
   - Verify virtual environment is activated
   - Check for missing dependencies

2. **Database errors**:
   - Run migrations: `python manage.py migrate`
   - Check database file permissions

3. **CORS errors**:
   - Verify CORS_ALLOWED_ORIGINS in settings
   - Check frontend URL matches exactly

### Frontend Issues

1. **Build errors**:
   - Clear node_modules and reinstall
   - Check Node.js version compatibility

2. **API connection issues**:
   - Verify VITE_API_URL in .env file
   - Check backend server is running

3. **Chart not displaying**:
   - Check browser console for errors
   - Verify Chart.js dependencies

### Desktop Issues

1. **PyQt5 import errors**:
   - Install PyQt5: `pip install PyQt5`
   - Check Python version compatibility

2. **Matplotlib issues**:
   - Install matplotlib: `pip install matplotlib`
   - Check display settings on Linux

## 📊 Performance Notes

- **File Upload**: Handles files up to 10MB
- **Chart Rendering**: Optimized for up to 1000 data points
- **History Limit**: Automatically maintains last 5 uploads
- **PDF Generation**: Typically completes in 1-2 seconds

## 🎉 Demo Completion

Congratulations! You've successfully demonstrated all features of the Chemical Equipment Visualizer:

1. ✅ User authentication and authorization
2. ✅ CSV file upload and processing
3. ✅ Real-time data visualization
4. ✅ PDF report generation
5. ✅ History management
6. ✅ Both web and desktop interfaces
7. ✅ Modern UI with animations
8. ✅ API functionality

## 📝 Next Steps

1. **Customize the application** for specific use cases
2. **Deploy to production** using the deployment guide
3. **Add more chart types** or analysis features
4. **Implement additional file formats** (Excel, JSON)
5. **Add user roles and permissions**
6. **Integrate with external APIs**

---

**Demo Complete!** 🎊
The Chemical Equipment Visualizer is fully functional and ready for production use.
```\n\nThis script provides step-by-step instructions to demonstrate all features of the Chemical Equipment Visualizer.\n\n## 🚀 Prerequisites\n\n- Backend server running on `http://localhost:8000`\n- Frontend server running on `http://localhost:5173`\n- Desktop application ready to launch\n- Sample CSV file available (`backend/sample_equipment_data.csv`)\n\n## 📱 Web Application Demo\n\n### Step 1: User Registration\n\n1. **Open browser** and navigate to `http://localhost:5173`\n2. **Click \"Sign up\"** link on the login page\n3. **Fill registration form**:\n   - Username: `demo_user`\n   - Email: `demo@example.com`\n   - Password: `demo123456`\n   - Confirm Password: `demo123456`\n4. **Click \"Create Account\"**\n5. **Verify**: You should be automatically logged in and redirected to dashboard\n\n### Step 2: Dashboard Overview\n\n1. **Observe the UI**:\n   - Animated background with particles\n   - Glassmorphism design elements\n   - Smooth animations and transitions\n   - Responsive navigation bar\n\n2. **Note the features**:\n   - Upload section prominently displayed\n   - No data message (since no files uploaded yet)\n   - Clean, modern interface\n\n### Step 3: CSV File Upload\n\n1. **Click \"Upload CSV File\"** button\n2. **Select file**: Choose `backend/sample_equipment_data.csv`\n3. **Watch the upload process**:\n   - Button shows \"Uploading...\" state\n   - Success toast notification appears\n   - Dashboard updates with new data\n\n### Step 4: Data Visualization\n\n1. **Statistics Cards**: Observe the animated statistics cards showing:\n   - Total Equipment: 15\n   - Average Flowrate: ~125.33\n   - Average Pressure: ~5.95\n   - Average Temperature: ~118.67\n\n2. **Charts Section**:\n   - **Pie Chart**: Equipment type distribution\n     - Pumps, Compressors, Valves, Heat Exchangers, etc.\n     - Interactive hover effects\n   - **Bar Chart**: Parameter comparison\n     - Flowrate, Pressure, Temperature for each equipment\n     - Animated bars with different colors\n\n3. **Interactive Features**:\n   - Hover over chart elements for tooltips\n   - Smooth animations on load\n   - Responsive design adapts to screen size\n\n### Step 5: PDF Report Generation\n\n1. **Click \"Generate PDF Report\"** button\n2. **Wait for processing** (should be quick)\n3. **Download starts automatically**\n4. **Open the PDF** to verify contents:\n   - Professional header and formatting\n   - Summary statistics table\n   - Equipment distribution table\n   - Detailed equipment list\n   - Timestamp and metadata\n\n### Step 6: History Management\n\n1. **Click \"History\"** in the navigation\n2. **Observe the history page**:\n   - Shows the uploaded dataset\n   - Upload timestamp\n   - Summary statistics\n   - Equipment type distribution tags\n\n3. **Test actions**:\n   - **Download button**: Generates PDF report\n   - **Delete button**: Removes dataset (confirm dialog)\n\n### Step 7: Upload Additional Files\n\n1. **Return to Dashboard**\n2. **Upload the same file 4 more times** (to test history limit)\n3. **Go to History page**\n4. **Verify**: Only last 5 uploads are shown\n\n### Step 8: Logout\n\n1. **Click logout button** (red button in navbar)\n2. **Verify**: Redirected to login page\n3. **Try accessing dashboard directly**: Should redirect to login\n\n## 🖥️ Desktop Application Demo\n\n### Step 1: Launch Desktop App\n\n1. **Open terminal** in desktop directory\n2. **Run**: `python main.py`\n3. **Observe**: Modern dark-themed login window opens\n\n### Step 2: Login\n\n1. **Enter credentials**:\n   - Username: `demo_user`\n   - Password: `demo123456`\n2. **Click \"Login\"**\n3. **Verify**: Main application window opens\n\n### Step 3: Desktop Interface Overview\n\n1. **Header section**: Shows app name and logged-in user\n2. **Tabbed interface**: Dashboard and History tabs\n3. **Upload section**: File selection and processing\n4. **Statistics area**: Summary information\n5. **Charts area**: Matplotlib visualizations\n6. **Data table**: Equipment details\n\n### Step 4: File Upload (Desktop)\n\n1. **Click \"Select File\"**\n2. **Choose**: `backend/sample_equipment_data.csv`\n3. **Click \"Upload & Process\"**\n4. **Watch the process**:\n   - File uploads to server\n   - Statistics update\n   - Charts render\n   - Table populates\n\n### Step 5: Desktop Visualizations\n\n1. **Pie Chart**: Equipment distribution with matplotlib styling\n2. **Bar Chart**: Parameter comparison with grouped bars\n3. **Data Table**: Scrollable table with all equipment details\n4. **Statistics**: Formatted summary information\n\n### Step 6: History Tab (Desktop)\n\n1. **Click \"History\" tab**\n2. **Click \"Refresh History\"**\n3. **Observe**: Table shows all uploaded datasets\n4. **Note**: Same data as web application (shared backend)\n\n## 🧪 API Testing (Optional)\n\n### Using curl or Postman\n\n1. **Register a new user**:\n```bash\ncurl -X POST http://localhost:8000/api/auth/register/ \\\n  -H \"Content-Type: application/json\" \\\n  -d '{\"username\":\"api_user\",\"email\":\"api@example.com\",\"password\":\"api123456\"}'\n```\n\n2. **Login and get token**:\n```bash\ncurl -X POST http://localhost:8000/api/auth/login/ \\\n  -H \"Content-Type: application/json\" \\\n  -d '{\"username\":\"api_user\",\"password\":\"api123456\"}'\n```\n\n3. **Upload CSV file**:\n```bash\ncurl -X POST http://localhost:8000/api/datasets/upload/ \\\n  -H \"Authorization: Token YOUR_TOKEN_HERE\" \\\n  -F \"file=@backend/sample_equipment_data.csv\"\n```\n\n4. **Get history**:\n```bash\ncurl -X GET http://localhost:8000/api/datasets/history/ \\\n  -H \"Authorization: Token YOUR_TOKEN_HERE\"\n```\n\n## 🎯 Feature Demonstration Checklist\n\n### ✅ Authentication\n- [ ] User registration works\n- [ ] User login works\n- [ ] Token-based authentication\n- [ ] Logout functionality\n- [ ] Protected routes\n\n### ✅ File Upload\n- [ ] CSV file validation\n- [ ] File size limits\n- [ ] Error handling for invalid files\n- [ ] Success feedback\n\n### ✅ Data Processing\n- [ ] CSV parsing with Pandas\n- [ ] Statistics calculation\n- [ ] Equipment type distribution\n- [ ] Data validation\n\n### ✅ Visualizations\n- [ ] Interactive pie chart\n- [ ] Animated bar chart\n- [ ] Responsive design\n- [ ] Chart tooltips and hover effects\n\n### ✅ PDF Reports\n- [ ] Professional formatting\n- [ ] Complete data inclusion\n- [ ] Download functionality\n- [ ] Proper file naming\n\n### ✅ History Management\n- [ ] Last 5 uploads stored\n- [ ] Automatic cleanup\n- [ ] Delete functionality\n- [ ] Summary information\n\n### ✅ UI/UX\n- [ ] Glassmorphism design\n- [ ] Smooth animations\n- [ ] Responsive layout\n- [ ] Loading states\n- [ ] Error handling\n- [ ] Toast notifications\n\n### ✅ Desktop Application\n- [ ] PyQt5 interface\n- [ ] Matplotlib charts\n- [ ] Data table display\n- [ ] API integration\n- [ ] Cross-platform compatibility\n\n## 🐛 Common Issues and Solutions\n\n### Backend Issues\n\n1. **Server not starting**:\n   - Check if port 8000 is available\n   - Verify virtual environment is activated\n   - Check for missing dependencies\n\n2. **Database errors**:\n   - Run migrations: `python manage.py migrate`\n   - Check database file permissions\n\n3. **CORS errors**:\n   - Verify CORS_ALLOWED_ORIGINS in settings\n   - Check frontend URL matches exactly\n\n### Frontend Issues\n\n1. **Build errors**:\n   - Clear node_modules and reinstall\n   - Check Node.js version compatibility\n\n2. **API connection issues**:\n   - Verify VITE_API_URL in .env file\n   - Check backend server is running\n\n3. **Chart not displaying**:\n   - Check browser console for errors\n   - Verify Chart.js dependencies\n\n### Desktop Issues\n\n1. **PyQt5 import errors**:\n   - Install PyQt5: `pip install PyQt5`\n   - Check Python version compatibility\n\n2. **Matplotlib issues**:\n   - Install matplotlib: `pip install matplotlib`\n   - Check display settings on Linux\n\n## 📊 Performance Notes\n\n- **File Upload**: Handles files up to 10MB\n- **Chart Rendering**: Optimized for up to 1000 data points\n- **History Limit**: Automatically maintains last 5 uploads\n- **PDF Generation**: Typically completes in 1-2 seconds\n\n## 🎉 Demo Completion\n\nCongratulations! You've successfully demonstrated all features of the Chemical Equipment Visualizer:\n\n1. ✅ User authentication and authorization\n2. ✅ CSV file upload and processing\n3. ✅ Real-time data visualization\n4. ✅ PDF report generation\n5. ✅ History management\n6. ✅ Both web and desktop interfaces\n7. ✅ Modern UI with animations\n8. ✅ API functionality\n\n## 📝 Next Steps\n\n1. **Customize the application** for specific use cases\n2. **Deploy to production** using the deployment guide\n3. **Add more chart types** or analysis features\n4. **Implement additional file formats** (Excel, JSON)\n5. **Add user roles and permissions**\n6. **Integrate with external APIs**\n\n---\n\n**Demo Complete!** 🎊\nThe Chemical Equipment Visualizer is fully functional and ready for production use.