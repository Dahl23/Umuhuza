# 🚀 Umuhuza Platform - Complete Setup Guide

Complete step-by-step guide to set up and run the Umuhuza listings platform.

---

## 📋 Prerequisites

- Python 3.12+
- Node.js 18+ and npm
- PostgreSQL 14+ (or SQLite for development)
- Git

---

## 🛠️ Backend Setup (Django)

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create `.env` file in `backend/` directory:
```env
# Database
DATABASE_URL=sqlite:///db.sqlite3  # Or PostgreSQL URL

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173

# JWT
ACCESS_TOKEN_LIFETIME=60  # minutes
REFRESH_TOKEN_LIFETIME=1440  # minutes (24 hours)

# Email (optional - for production)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 5. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Setup Initial Data (Categories & Pricing Plans)
```bash
python manage.py setup_database
```

This command creates:
- **8 predefined categories** (Houses, Land, Cars, Trucks, etc.)
- **3 pricing plans** (Basic Free, Premium 50K BIF, Dealer 150K BIF)

### 7. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 8. Start Backend Server
```bash
python manage.py runserver
```

Backend now running at: **http://localhost:8000**

---

## 🎨 Frontend Setup (React + Vite)

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Environment Configuration
Create `.env` file in `frontend/` directory:
```env
# Site Configuration
VITE_SITE_NAME=Umuhuza

# API Configuration
VITE_API_URL=http://localhost:8000/api

# Google Maps API Key (optional - for location autocomplete)
VITE_GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

### 4. Start Frontend Server
```bash
npm run dev
```

Frontend now running at: **http://localhost:5173**

---

## 🧪 Quick Test

### 1. Register a User
1. Navigate to http://localhost:5173
2. Click "Sign Up"
3. Fill registration form
4. Verify your account (check console logs for verification code in development)

### 2. Automatic Basic Plan
- Upon registration, users are **automatically subscribed** to the **Basic Plan** (free)
- Basic Plan allows: 1 listing, 5 images, 30 days

### 3. Create a Listing
1. Go to "Post Listing"
2. Fill in listing details (multi-step form)
3. Upload up to 5 images (auto-converted to optimized JPEGs)
4. Submit → Listing is **automatically activated**

### 4. Upgrade to Premium/Dealer
1. Go to "Pricing" page
2. Select Premium (50K BIF) or Dealer (150K BIF)
3. Complete payment (simulation in development)
4. Old Basic plan is **automatically cancelled**, new plan activated

---

## 📦 Database Setup Script

### Command Usage
```bash
python manage.py setup_database [--reset]
```

### Options
- **No flags**: Creates categories and plans if they don't exist
- **--reset**: Deletes existing data and recreates from scratch (⚠️ DESTRUCTIVE)

### What It Creates

#### Categories (8 total)
| Category | Description |
|----------|-------------|
| Houses & Apartments | Residential properties |
| Land & Plots | Empty land for sale |
| Commercial Properties | Office spaces, shops |
| Cars | Passenger vehicles |
| Trucks & Commercial Vehicles | Commercial vehicles |
| Motorcycles & Bikes | Two-wheelers |
| Buses & Minibuses | Passenger transport |
| Heavy Equipment | Construction equipment |

#### Pricing Plans (3 total)
| Plan | Price | Duration | Listings | Images | Featured |
|------|-------|----------|----------|--------|----------|
| Basic Plan | FREE | 30 days | 1 | 5 | ❌ |
| Premium Plan | 50,000 BIF | 30 days | 10 | 10 | ❌ |
| Dealer Monthly | 150,000 BIF | 30 days | Unlimited | 15 | ✅ |

---

## 🖼️ Image Upload System

### How It Works
1. User uploads images (PNG, JPG, WebP)
2. Backend processes with PIL:
   - Converts to RGB mode
   - Resizes if width > 1920px
   - Saves as optimized JPEG (85% quality)
3. **Only converted JPEG** is saved to disk
4. Original upload is **discarded** (exists only in memory)

### Storage Location
```
backend/media/listings/{listing_id}/{uuid}.jpg
```

### Key Features
- **No duplicates**: Original files never saved
- **Optimized**: Smaller file sizes, faster loading
- **Automatic cleanup**: PIL images closed after processing
- **Plan limits**: Basic=5, Premium=10, Dealer=15 images

---

## 🔑 Subscription & Listing Flow

### 1. User Registration
```
User signs up → Email verification → Basic Plan auto-created
```

### 2. Create Listing
```
Fill form → Upload images (plan limit enforced) → Submit → Listing auto-activated
```

### 3. Plan Upgrade
```
Select plan → Pay → Old plan cancelled → New plan activated → All benefits granted
```

### 4. Listing Status Management

**Users CAN:**
- Mark listing as "Sold"
- Mark listing as "Hidden"

**Users CANNOT:**
- Mark listing as "Active" (only subscription system can activate)

**Status Transition:**
```
active → sold/hidden (frees quota)
sold/hidden → active (NOT ALLOWED by user)
```

---

## 🎯 Key Features & Improvements

### ✅ Recently Fixed Issues

1. **Payment History Page** - Now displays plan details correctly
2. **Image Display** - Absolute URLs, images show on all pages
3. **Listing Status** - Users can mark as sold/hidden via dropdown menu
4. **Image Upload Limits** - Enforced based on subscription plan
5. **Price Limits** - Increased to support high-value properties (up to 9.9 trillion)
6. **Subscription Upgrades** - Old plans cancelled when upgrading
7. **Redundant Modal** - Plan selection no longer shown twice
8. **Description Layout** - Text wrapping fixed, no overflow
9. **Status Control** - Users cannot self-activate listings

### 🔐 Subscription Security

- **Auto-activation**: Only the system activates listings (when created with valid subscription)
- **Quota management**: Automatically tracked, enforced on creation
- **Plan cancellation**: Upgrading cancels old plan immediately
- **Listing deactivation**: Marking as sold/hidden frees quota

---

## 🚀 Production Deployment

### Environment Variables (Production)
```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com

# Use PostgreSQL
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Real email backend
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

# Media files (use S3 or similar)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_STORAGE_BUCKET_NAME=your-bucket
```

### Static Files
```bash
python manage.py collectstatic
```

### Media Files
Consider using **AWS S3** or **Cloudinary** for production (see `FILE_UPLOAD_ARCHITECTURE.md`)

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check migrations
python manage.py showmigrations

# Run migrations
python manage.py migrate
```

### Images not showing
```bash
# Check media directory exists
ls backend/media/

# Check permissions
chmod -R 755 backend/media/

# Verify MEDIA_URL in settings.py
```

### Database reset needed
```bash
# Delete database
rm backend/db.sqlite3

# Recreate
python manage.py migrate
python manage.py setup_database
```

---

## 📚 Additional Documentation

- **FILE_UPLOAD_ARCHITECTURE.md** - Image upload system details
- **API Documentation** - Available at http://localhost:8000/api/docs/ (if configured)
- **ROADMAP.md** - Future features and improvements

---

## 🤝 Support

For issues or questions:
1. Check existing documentation
2. Review backend logs: `backend/debug.log`
3. Check browser console for frontend errors
4. Verify environment variables are set correctly

---

**Last Updated:** 2025-01-25
**Platform Version:** 1.0.0
