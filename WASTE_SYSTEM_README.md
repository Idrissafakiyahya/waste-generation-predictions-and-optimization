# Community Waste Reporting System

A web-based system for reporting and managing community waste issues. This system includes a React-based frontend for citizens to report waste problems and a Django backend with an admin interface for managing reports, waste bins, and locations.

## Features

### Frontend
- **Landing Page**: Welcome page with information about the system
- **About Page**: Regulations, laws, and privacy policy information
- **Report Form**: Easy-to-use form for citizens to report waste issues
  - Location selection (Shehia)
  - Bin selection (automatically filtered by Shehia)
  - Timestamp selection
  - Comment/details field
  - Real-time validation and feedback

### Backend
- **RESTful API**: Endpoints for Shehias, Bins, and Waste Reports
- **Admin Dashboard**: Web interface for viewing all waste reports
- **Admin Panel**: Django admin interface for managing:
  - Shehias (administrative divisions)
  - Waste Bins (with types and capacities)
  - Waste Reports (with full details)

## Project Structure

```
waste system/
├── frontend/                 # React frontend
│   └── src/
│       ├── components/
│       │   ├── Header.jsx
│       │   ├── LandingPage.jsx
│       │   ├── About.jsx
│       │   ├── ReportForm.jsx
│       │   └── *.css files
│       ├── App.jsx
│       └── index.css
├── backend/                  # Django backend
│   ├── prediction/
│   │   ├── models.py         # Shehia, Bin, WasteReport models
│   │   ├── views.py          # API endpoints
│   │   ├── admin.py          # Admin customization
│   │   └── urls.py
│   ├── templates/
│   │   └── prediction/
│   │       ├── admin_dashboard.html
│   │       └── react_report_page.html
│   └── waste_project/        # Project settings
└── README.md
```

## Setup Instructions

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Activate virtual environment**:
   ```bash
   .venv\Scripts\Activate.ps1  # Windows PowerShell
   # or
   source .venv/bin/activate   # Mac/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. **Add sample data** (Shehias and Bins):
   ```bash
   python manage.py shell
   ```
   Then in the shell:
   ```python
   from prediction.models import Shehia, Bin
   
   # Create Shehias
   shehi_amani = Shehia.objects.create(name="Amani", description="Central district")
   shehi_makadara = Shehia.objects.create(name="Makadara", description="Western district")
   shehi_kibera = Shehia.objects.create(name="Kibera", description="Southern district")
   
   # Create Bins
   Bin.objects.create(shehia=shehi_amani, name="AmaniA", location="Amani Market", bin_type="general", capacity=100)
   Bin.objects.create(shehia=shehi_amani, name="AmaniB", location="Amani Park", bin_type="organic", capacity=80)
   Bin.objects.create(shehia=shehi_makadara, name="MakadaraA", location="Makadara Street", bin_type="recyclable", capacity=60)
   Bin.objects.create(shehia=shehi_kibera, name="KiberaA", location="Kibera Center", bin_type="general", capacity=100)
   
   exit()
   ```

7. **Run development server**:
   ```bash
   python manage.py runserver
   ```
   Backend will be available at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```
   Frontend will be available at: `http://localhost:5173`

## API Endpoints

### Public Endpoints (CORS enabled)

#### Get all Shehias
```
GET /api/shehias/
Response:
{
  "success": true,
  "data": [
    {"id": 1, "name": "Amani", "description": "Central district"},
    ...
  ]
}
```

#### Get Bins for a Shehia
```
GET /api/bins/?shehia_id=1
Response:
{
  "success": true,
  "data": [
    {"id": 1, "name": "AmaniA", "location": "Amani Market", "bin_type": "general"},
    ...
  ]
}
```

#### Submit Waste Report
```
POST /api/reports/
Body:
{
  "shehia_id": 1,
  "bin_id": 1,
  "timestamp": "2026-07-02T10:30:00",
  "comment": "Bin is overflowing with trash"
}
Response:
{
  "success": true,
  "message": "Report submitted successfully",
  "report_id": 5
}
```

#### Get All Waste Reports
```
GET /api/reports/list/
Response:
{
  "success": true,
  "data": [
    {
      "id": 5,
      "shehia__name": "Amani",
      "bin__name": "AmaniA",
      "bin__location": "Amani Market",
      "timestamp": "2026-07-02T10:30:00",
      "comment": "Bin is overflowing with trash",
      "submitted_at": "2026-07-02T10:35:00"
    },
    ...
  ],
  "count": 5
}
```

#### Delete Waste Report
```
DELETE /api/reports/{report_id}/delete/
Response:
{
  "success": true,
  "message": "Report deleted successfully"
}
```

## Admin Interfaces

### Django Admin Panel
- URL: `http://localhost:8000/admin`
- Login with superuser credentials
- Manage Shehias, Bins, and Waste Reports
- View report statistics and details

### Waste Reports Dashboard
- URL: `http://localhost:8000/api/dashboard/`
- Real-time view of all waste reports
- Statistics: Total reports, monthly, weekly, active Shehias
- View, filter, and delete reports

## Data Management

### Adding New Shehias (via Admin Panel)
1. Go to Django Admin (`/admin`)
2. Click on "Shehias"
3. Click "Add Shehia"
4. Enter name and description
5. Save

### Adding New Bins (via Admin Panel)
1. Go to Django Admin (`/admin`)
2. Click on "Bins"
3. Click "Add Bin"
4. Select Shehia
5. Enter bin details (name, location, capacity, type)
6. Save
7. **New bin will immediately appear in frontend dropdowns**

### Viewing Reports
- **Frontend**: `/report` - Submit reports
- **Dashboard**: `/api/dashboard/` - View all reports
- **Admin Panel**: `/admin` - Detailed report management

## Green Theme

The system uses a professional green color scheme:
- **Primary Green**: `#10b981`
- **Dark Green**: `#059669`
- **Light Green**: `#d1fae5`

Colors are used throughout for:
- Header and navigation
- Buttons and interactive elements
- Form highlights and borders
- Badges and status indicators

## Database Schema

### Shehia Model
```
- id: Integer (Primary Key)
- name: String (Unique)
- description: Text (Optional)
- created_at: DateTime (Auto)
```

### Bin Model
```
- id: Integer (Primary Key)
- shehia: Foreign Key (Shehia)
- name: String
- location: String
- capacity: Integer (kg)
- bin_type: Choice (general, organic, recyclable, hazardous)
- created_at: DateTime (Auto)
- updated_at: DateTime (Auto)
```

### WasteReport Model
```
- id: Integer (Primary Key)
- shehia: Foreign Key (Shehia)
- bin: Foreign Key (Bin)
- timestamp: DateTime (when issue was observed)
- comment: Text (Optional)
- submitted_at: DateTime (Auto)
```

## CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:5173` (frontend dev server)
- `http://localhost:3000` (alternative frontend)
- All origins (for development)

Update `CORS_ALLOWED_ORIGINS` in `backend/waste_project/settings.py` for production.

## Features & Workflow

### For Citizens
1. Visit the frontend site
2. Click "Report Waste" button
3. Select their Shehia (area)
4. Select the specific bin location
5. Set the timestamp when issue was observed
6. Add optional comments
7. Submit the report
8. Receive confirmation

### For Administrators
1. Access Django Admin (`/admin`)
2. Add or update Shehias and Bins
3. View all waste reports
4. Filter reports by location, date, or bin type
5. Delete resolved issues
6. Use dashboard for statistics and monitoring
7. Track problem areas and patterns

## Customization

### Adding New Bin Types
Edit `backend/prediction/models.py`:
```python
bin_type = models.CharField(
    max_length=50,
    choices=[
        ('general', 'General Waste'),
        ('organic', 'Organic Waste'),
        ('recyclable', 'Recyclable'),
        ('hazardous', 'Hazardous'),
        # Add new types here
    ],
    default='general'
)
```

### Modifying Form Fields
Edit `frontend/src/components/ReportForm.jsx` to add/remove fields and update the API payload.

### Changing Colors
Update CSS variables in:
- `frontend/src/components/*.css`
- `backend/static/css/custom_admin.css`

## Troubleshooting

### Frontend can't connect to backend
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in Django
- Clear browser cache

### Bins not appearing in dropdown
- Ensure bins are created for the selected Shehia
- Check that bins are in the database via Admin panel
- Refresh the browser

### Admin panel not loading
- Clear Django cache: `python manage.py clear_cache`
- Check migrations: `python manage.py migrate`
- Restart Django server

## Support

For issues or improvements:
1. Check the admin panel for data consistency
2. Review API responses in browser console
3. Check Django logs for backend errors
4. Verify database connectivity

## License

Community Waste Reporting System v1.0 - 2026
