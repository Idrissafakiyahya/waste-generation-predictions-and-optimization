# Admin Management Guide

## Django Admin Panel Overview

The Django Admin Panel is the central hub for managing all data in the Waste Reporting System.

**Access**: http://localhost:8000/admin

---

## 🗂️ Main Sections

### 1. SHEHIAS (Areas/Divisions)

#### View All Shehias
1. Go to Django Admin
2. Click **"Shehias"** section
3. You'll see a list of all areas with:
   - Name
   - Creation date
   - Search functionality

#### Add a New Shehia
1. Click **"Add Shehia"** button
2. Fill in:
   - **Name** (required): E.g., "Kamukunji", "Westlands", "Downtown"
   - **Description** (optional): E.g., "Central business district"
3. Click **"Save"**

#### Edit a Shehia
1. Click on a Shehia name
2. Update the fields
3. Click **"Save"**

#### Delete a Shehia
1. Check the checkbox next to a Shehia
2. Select "Delete selected Shehias" from dropdown
3. Click **"Go"**
4. Confirm deletion
⚠️ **Warning**: Deleting will remove all associated bins and may delete related reports

#### Search Shehias
- Use the search box to find Shehias by name
- Useful when you have many areas

---

### 2. BINS (Waste Bins)

#### View All Bins
1. Click **"Bins"** section
2. You'll see all bins with:
   - Name
   - Shehia
   - Location
   - Type (General/Organic/Recyclable/Hazardous)
   - Capacity

#### Add a New Bin
1. Click **"Add Bin"** button
2. Fill in:
   - **Shehia** (required): Select from dropdown
   - **Name** (required): E.g., "AmaniA", "Downtown-1"
   - **Location** (required): E.g., "Market Street", "Park Entrance"
   - **Capacity** (required): Enter in kg (e.g., 100, 80, 60)
   - **Bin Type** (required): Choose one:
     - General Waste
     - Organic Waste
     - Recyclable
     - Hazardous
3. Click **"Save"**

#### Edit a Bin
1. Click on a bin name
2. Update the fields (especially capacity if needed)
3. Click **"Save"**

#### Delete a Bin
1. Check the checkbox next to a bin
2. Select "Delete selected Bins" from dropdown
3. Click **"Go"**
4. Confirm deletion

#### Filter Bins
- **By Shehia**: Click on a Shehia name in sidebar
- **By Type**: Click on a bin type in sidebar
- Use search for location

#### Sort Bins
- Click column headers to sort by:
  - Name
  - Shehia
  - Location
  - Type

---

### 3. WASTE REPORTS (Community Reports)

#### View All Reports
1. Click **"Waste Reports"** section
2. See all submitted reports with:
   - Report ID
   - Shehia
   - Bin
   - Timestamp (when issue observed)
   - Submit date/time
   - Filters available

#### View Report Details
1. Click on a report ID
2. See full details:
   - Shehia and Bin info
   - Timestamp when issue was observed
   - Full comment/description
   - When it was submitted
3. Cannot edit (to maintain data integrity)
4. Can only delete

#### Filter Reports
Available filters on the right sidebar:
- **By Shehia**: Select to see reports only from one area
- **By Bin**: Filter by specific waste bin
- **By Submitted Date**: Filter by submission date range

#### Search Reports
- Search by comment text
- Use quotes for exact phrases: "overflowing waste"

#### Delete Reports
1. Method A - Single Report:
   - Open the report
   - Click **"Delete"** button at bottom
   - Confirm

2. Method B - Multiple Reports:
   - Check boxes next to reports
   - Select "Delete selected Waste Reports" from dropdown
   - Click **"Go"**
   - Confirm

#### Sort Reports
- Click column headers to sort
- Most recent reports appear first by default

#### Export Reports
The default Django admin shows reports in table format. For larger data exports:
- Consider building custom export functionality
- Or use Django's data export features

---

## 📊 Dashboard View

For a real-time overview without Django Admin:

1. Go to: http://localhost:8000/api/dashboard/
2. See statistics:
   - Total Reports
   - This Month
   - This Week
   - Active Shehias
3. View report table with delete buttons
4. Auto-refreshes every 30 seconds

---

## 🔍 Monitoring & Analysis

### Find Problem Areas
1. Go to Waste Reports
2. Filter by Shehia
3. Sort by submission date
4. Look for patterns:
   - Multiple reports from same location
   - Reports at same time of day
   - Specific bin types causing issues

### Track Report Trends
1. Note dates of reports
2. Check if same bins reported multiple times
3. Use submission date filter to find peak times
4. Plan collection schedules accordingly

### Identify High-Issue Areas
1. Filter reports by Shehia
2. Count reports per area
3. Prioritize resource allocation
4. Plan community outreach

---

## 🛠️ Data Management Tasks

### Weekly Tasks
- [ ] Review new reports
- [ ] Delete resolved issues
- [ ] Check for recurring problem locations
- [ ] Note any new areas needing bins

### Monthly Tasks
- [ ] Analyze report statistics (on dashboard)
- [ ] Add new areas if needed
- [ ] Add new bins in problem areas
- [ ] Review community feedback

### Adding Bins to Problem Areas
1. Identify area with high reports
2. Go to Bins section
3. Add new bins for that area
4. Test on frontend (new bins appear in dropdown)

### Updating Bin Capacity
1. Go to Bins section
2. Click on a bin
3. Update capacity if needed
4. Save changes

---

## 🚨 Important Notes

### Data Integrity
- Reports cannot be edited (only viewed/deleted)
- Deleting a bin may affect associated reports
- Always confirm before bulk deletions

### CORS & API
- Admin panel doesn't use API (direct database)
- Dashboard and frontend use API endpoints
- Reports appear immediately in admin after submission

### Backup
- Django SQLite database: `backend/db.sqlite3`
- Regular backups recommended for production

---

## 🔐 Admin Best Practices

1. **Regular Monitoring**
   - Check reports weekly
   - Look for patterns and issues
   - Act on repeated problems

2. **Data Clean-up**
   - Delete resolved/old reports
   - Keep database manageable
   - Maintain accuracy of data

3. **Proactive Support**
   - Add bins before citizens complain
   - Update descriptions for clarity
   - Respond to issue patterns

4. **Documentation**
   - Keep notes on problem areas
   - Track when bins were added
   - Monitor report patterns over time

---

## 🎯 Common Scenarios

### Scenario 1: Adding a New Area
1. **Citizen complaints about new area**
2. Go to Shehias → Add Shehia
3. Enter area name and description
4. Add bins for that area (2-3 to start)
5. Announce to public that area is now covered

### Scenario 2: Bin Overflowing Problem
1. **Receive multiple reports for same bin**
2. Go to Reports → Filter by bin
3. Increase capacity in Bins section
4. Or add additional bin nearby
5. Test new bin appears in frontend

### Scenario 3: Change Bin Location
1. **Area being renovated**
2. Go to Bins → Click on bin
3. Update location description
4. Inform public of new location
5. Consider adding nearby bin temporarily

### Scenario 4: Removing Resolved Issue
1. **Bin replaced or area cleaned**
2. Go to Waste Reports
3. Delete related reports (to keep dashboard clean)
4. Keep historical data by exporting first

---

## 📈 Reporting Insights

### What High Reports Mean
- **Same bin**: May need higher capacity or more frequent collection
- **Same area**: May need more bins or better community education
- **Time pattern**: May need adjusted collection schedule

### What Low Reports Mean
- **Good area management**: Keep current setup
- **Lack of awareness**: May need more publicity
- **Under-coverage**: Check if bin placement is convenient

---

## 🔧 Troubleshooting

### Can't see reports
- Check filters aren't too restrictive
- Verify reports were submitted on frontend
- Refresh the page

### Deleted wrong data
- Use Django's built-in admin actions to undo (if available)
- For SQLite: Restore from backup
- Always confirm before bulk deletes

### Bins not appearing on frontend
- Verify bins are created for selected Shehia
- Try refreshing frontend page
- Check browser console for errors
- Verify bin-Shehia association

### Report numbers not matching
- Dashboard auto-refreshes; may lag slightly
- Refresh dashboard page
- Check admin panel for definitive counts

---

## 📝 Checklist for New Admin

- [ ] Log in to Django Admin successfully
- [ ] Add 3-5 Shehias (test areas)
- [ ] Add 2-3 bins per Shehia
- [ ] Test frontend form with new data
- [ ] Submit test report from frontend
- [ ] Verify report appears in admin panel
- [ ] Delete test report
- [ ] View dashboard at /api/dashboard/
- [ ] Test search and filter functions
- [ ] Read full documentation

---

## 🆘 Need Help?

Refer to:
- **Full System Docs**: `WASTE_SYSTEM_README.md`
- **Quick Start**: `QUICK_START.md`
- **Django Documentation**: https://docs.djangoproject.com/
- **Models Overview**: See `backend/prediction/models.py`

---

**You're ready to manage the Waste Reporting System! ♻️**
