# MedAnnotate — Setup Guide

## Prerequisites

1. **Python 3.11+** — https://www.python.org/downloads/
   - ✅ Check "Add Python to PATH" during installation

2. **MongoDB Community Server** — https://www.mongodb.com/try/download/community
   - Install and start the service (default port 27017)

---

## Quick Start

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Start the Flask server
```bash
python app.py
```

### Step 3 — Create the admin account
In your browser, visit:
```
POST http://localhost:5000/api/admin/seed
```
Or just open: http://localhost:5000 — the server auto-seeds on first run.

### Step 4 — Open the platform
```
http://localhost:5000
```

---

## Default Admin Credentials
```
Email:    admin@medannotate.com
Password: Admin@1234
```

---

## Register Accounts

### Doctor Registration
1. Go to `/register`
2. Select "Doctor / Specialist"
3. Fill in name, email, specialty, license number, password
4. Admin must verify your account before you can start annotating

### AI Company Registration
1. Go to `/register`
2. Select "AI Company"
3. Fill in company name, email, password
4. Companies are auto-approved — you can upload immediately

---

## Workflow

```
Company uploads images (with AI dept detection + anonymization)
         ↓
System assigns images to matching specialist doctors
         ↓
Doctor annotates (bounding boxes, freehand, labels, notes)
         ↓
Doctor submits → QA assigned to second specialist
         ↓
QA doctor Approves or Rejects
         ↓
On Approval → Doctor earns $4.00 per image
         ↓
Admin marks payout as paid
         ↓
Company downloads Gold Standard data (COCO/VOC/YOLO)
```

---

## Environment Variables (Optional)

Create a `.env` file:
```
MONGO_URI=mongodb://localhost:27017/medannotate
JWT_SECRET_KEY=your-secret-key
HUGGINGFACE_API_KEY=your-hf-key  # optional, for AI dept detection
PAY_PER_IMAGE=4.0
```

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/auth/register` | POST | Register doctor or company |
| `/api/auth/login`    | POST | Login → returns JWT token |
| `/api/auth/me`       | GET  | Get current user profile |
| `/api/images/upload` | POST | Upload medical image (company) |
| `/api/images/`       | GET  | List images (role-filtered) |
| `/api/images/<id>/file` | GET | Serve image file |
| `/api/annotations/`  | POST | Save/update annotation |
| `/api/annotations/<id>/submit` | POST | Submit for QA |
| `/api/annotations/<id>/qa`    | POST | QA approve/reject |
| `/api/annotations/qa-queue`   | GET  | Doctor's QA queue |
| `/api/annotations/my-stats`   | GET  | Doctor stats & earnings |
| `/api/admin/stats`   | GET  | Platform statistics |
| `/api/admin/doctors/<id>/verify` | POST | Verify doctor |
| `/api/admin/payouts/<id>/pay`    | POST | Mark payout as paid |

---

## Project Structure

```
medical/
├── app.py              # Flask app entry point
├── config.py           # Settings, departments, labels
├── extensions.py       # MongoDB + JWT instances
├── requirements.txt    # Python dependencies
├── start.bat           # Windows quick-start script
│
├── routes/
│   ├── auth.py         # Login, register, me
│   ├── images.py       # Upload, serve, list
│   ├── annotations.py  # Save, submit, QA, stats
│   └── admin.py        # Admin management
│
├── utils/
│   ├── anonymize.py    # Strip EXIF/DICOM patient data
│   └── detect_department.py  # AI dept detection
│
└── frontend/
    ├── index.html      # Landing page
    ├── login.html      # Login
    ├── register.html   # Registration
    ├── doctor/
    │   ├── dashboard.html   # Doctor home + queue
    │   ├── annotate.html    # Fabric.js canvas
    │   └── earnings.html    # Earnings + QA review
    ├── company/
    │   ├── dashboard.html   # Company home
    │   ├── upload.html      # Batch upload
    │   └── batches.html     # Track & download
    ├── admin/
    │   └── dashboard.html   # Admin control panel
    ├── css/
    │   └── main.css         # Dark mode design system
    └── js/
        ├── api.js           # HTTP client + auth
        ├── annotate.js      # Fabric.js engine
        ├── doctor-dashboard.js
        ├── company-dashboard.js
        ├── admin-dashboard.js
        └── upload.js
```
"# MedAnnotate" 
"# MedAnnotate" 
