# Community Waste Reporting System - Quick Start Guide

## 🚀 Quick Start (5 minutes)

### Step 1: Start the Backend
```bash
cd backend
.venv\Scripts\Activate.ps1
python manage.py runserver
```
✓ Backend running at: `http://localhost:8000`

### Step 2: Start the Frontend
```bash
cd frontend
npm install  # (first time only)
npm run dev
```
✓ Frontend running at: `http://localhost:5173`

### Step 3: Access the System
- **Frontend**: http://localhost:5173
- **Django Admin**: http://localhost:8000/admin
- **Dashboard**: http://localhost:8000/api/dashboard/

---

## 📋 Initial Setup (First Time Only)

### Backend Setup

1. **Database Migrations**:
   ```bash
   cd backend
   python manage.py migrate
   ```

2. **Create Admin User**:
   ```bash
   python manage.py createsuperuser
   # Enter username, email, password
   ```

3. **Add Sample Data** (Optional):
   ```bash
   python manage.py shell
   ```
   Paste this code:
   ```python
   from prediction.models import Shehia, Bin
   
   # Create areas (Shehias)
   amani = Shehia.objects.create(name="Amani", description="Central area")
   makadara = Shehia.objects.create(name="Makadara", description="West area")
   kibera = Shehia.objects.create(name="Kibera", description="South area")
   
   # Create bins for Amani
   Bin.objects.create(shehia=amani, name="AmaniA", location="Market", bin_type="general", capacity=100)
   Bin.objects.create(shehia=amani, name="AmaniB", location="Park", bin_type="organic", capacity=80)
   
   # Create bins for Makadara
   Bin.objects.create(shehia=makadara, name="MakadaraA", location="Street", bin_type="recyclable", capacity=60)
   
   # Create bins for Kibera
   Bin.objects.create(shehia=kibera, name="KiberaA", location="Center", bin_type="general", capacity=100)
   
   exit()
   ```

4. **Verify Django Admin**:
   - Go to: http://localhost:8000/admin
   - Login with your superuser credentials
   - You should see: Shehias, Bins, and Waste Reports sections

---

## 🎯 How to Use

### For Citizens: Report Waste
1. Go to http://localhost:5173
2. Click **"Report Waste Now"** button
3. Select your **Shehia** (area)
4. Select the **Bin** location (dropdown auto-updates)
5. Set the **Timestamp** (when you saw the issue)
6. Add **Comments** (optional - describe the problem)
7. Click **"Submit Report"**
8. ✓ You'll see a success message

### For Administrators: Manage Data

#### Adding a New Shehia (Area)
1. Go to Django Admin: http://localhost:8000/admin
2. Click **"Shehias"**
3. Click **"Add Shehia"** button
4. Enter: Name (e.g., "Kamukunji") and Description (optional)
5. Click **"Save"**
6. ✓ New area appears on frontend immediately

#### Adding a New Bin
1. Go to Django Admin: http://localhost:8000/admin
2. Click **"Bins"**
3. Click **"Add Bin"** button
4. Fill in:
   - **Shehia**: Select from dropdown
   - **Name**: e.g., "KamukunjiA"
   - **Location**: e.g., "Downtown Market"
   - **Bin Type**: Choose (General/Organic/Recyclable/Hazardous)
   - **Capacity**: Enter in kg (e.g., 100)
5. Click **"Save"**
6. ✓ New bin appears in frontend dropdowns

#### Viewing & Deleting Reports
- **Dashboard**: http://localhost:8000/api/dashboard/
  - See all reports with stats
  - Click "Delete" to remove reports
  
- **Admin Panel**: http://localhost:8000/admin → "Waste Reports"
  - View detailed report information
  - Filter by Shehia, Bin, or Date
  - Delete individual reports

---

## 🌐 Frontend Pages

### Landing Page (Home)
- Shows system overview
- Big "Report Waste Now" button
- Features section (4 steps)
- Call-to-action section

### Report Page
- Shehia selector (loads all areas)
- Bin selector (dynamic based on Shehia)
- Timestamp picker
- Comment field
- Form validation and feedback

### About Page
- **Mission**: System overview
- **Laws & Regulations**: Environmental protection rules
- **Privacy & Data Protection**: How data is used and secured
- **Support**: Contact information

---

## 📊 API Endpoints

All endpoints are at: `http://localhost:8000/api/`

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/shehias/` | Get all areas |
| GET | `/bins/?shehia_id=1` | Get bins for area |
| POST | `/reports/` | Submit waste report |
| GET | `/reports/list/` | Get all reports |
| DELETE | `/reports/{id}/delete/` | Delete a report |
| GET | `/dashboard/` | View dashboard |

---

## 🎨 Green Theme Colors

- **Primary**: `#10b981` (Emerald Green)
- **Dark**: `#059669` (Forest Green)
- **Light**: `#d1fae5` (Mint Green)

Used throughout:
- Navigation header
- Buttons and links
- Form borders and highlights
- Badges and status indicators

---

## 🔧 Troubleshooting

### Frontend shows "Loading..." forever
- ✓ Check backend is running on port 8000
- ✓ Check browser console for errors
- ✓ Try `npm run dev` again

### Bins dropdown is empty
- ✓ Make sure you created bins in Django Admin
- ✓ Verify bins are assigned to selected Shehia
- ✓ Refresh the page

### Can't login to Django Admin
- ✓ Check you created a superuser: `python manage.py createsuperuser`
- ✓ Use correct username/password
- ✓ Try http://localhost:8000/admin/login/

### Reports not appearing in dashboard
- ✓ Check that reports were submitted on frontend
- ✓ Verify database connection
- ✓ Try refreshing the dashboard page
- ✓ Check Django logs for errors

### "CORS ERROR" or connection refused
- ✓ Backend must be running on `http://localhost:8000`
- ✓ Frontend must be running on `http://localhost:5173`
- ✓ Check CORS settings in `backend/waste_project/settings.py`

---

## 📁 File Structure

```
waste system/
├── frontend/src/
│   ├── components/
│   │   ├── Header.jsx + Header.css         # Navigation
│   │   ├── LandingPage.jsx + .css          # Home page
│   │   ├── About.jsx + About.css           # Info page
│   │   └── ReportForm.jsx + .css           # Report form
│   ├── App.jsx                             # Main app
│   └── index.css                           # Global styles
├── backend/
│   ├── prediction/
│   │   ├── models.py                       # Database models
│   │   ├── views.py                        # API endpoints
│   │   ├── admin.py                        # Admin config
│   │   └── urls.py                         # URL routing
│   ├── templates/prediction/
│   │   └── admin_dashboard.html            # Dashboard UI
│   └── manage.py                           # Django CLI
└── WASTE_SYSTEM_README.md                  # Full documentation
```

---

## 🎓 Example Workflow

### Citizen Flow:
1. **Visit** http://localhost:5173
2. **See** landing page with features
3. **Click** "Report Waste Now"
4. **Select** "Amani" → Choose "AmaniA" (Market) → Set time → Add comment
5. **Submit** → See success message
6. **Report** appears in admin dashboard

### Admin Flow:
1. **Visit** http://localhost:8000/admin
2. **Add** new Shehia (e.g., "Kamukunji")
3. **Add** new Bin for Kamukunji (e.g., "KamukunjiA")
4. **Visit** http://localhost:5173
5. **See** new area/bin in dropdown (auto-updated)
6. **Check** http://localhost:8000/api/dashboard/ for submissions

---

## ✅ What's Included

✓ **Frontend**
- React 19 with Vite
- React Router for navigation
- 4 pages (Home, Report, About)
- Green theme styling
- Form validation
- API integration

✓ **Backend**
- Django REST API
- 3 models (Shehia, Bin, WasteReport)
- Admin interface
- CORS enabled
- Dashboard HTML interface
- Delete functionality

✓ **Documentation**
- Full README
- API documentation
- Admin guide
- This quick start

---

## 🚀 Next Steps

1. ✓ Start backend and frontend
2. ✓ Add your first Shehia in Admin
3. ✓ Add some bins for that Shehia
4. ✓ Submit a test report from frontend
5. ✓ View it in the dashboard
6. ✓ Start collecting real community reports!

---

## 📞 Support

- Check full docs: `WASTE_SYSTEM_README.md`
- Django Admin help: http://localhost:8000/admin
- API errors show in browser console
- Backend errors visible in terminal output

---

**Happy reporting! ♻️**
