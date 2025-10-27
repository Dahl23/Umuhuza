# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Umuhuza is a full-stack marketplace platform for real estate and vehicle listings in Burundi. The platform eliminates middlemen by connecting buyers and sellers directly, featuring verified accounts, real-time messaging, and integrated payment systems.

**Stack:**
- Backend: Django 5.2+ with Django REST Framework
- Frontend: React 19 with TypeScript, Vite, TailwindCSS 4
- Database: PostgreSQL 15+
- State Management: Zustand with persistence
- Authentication: JWT (djangorestframework-simplejwt)

## Development Setup

### Backend (Django)

**Working directory:** Always run backend commands from `/backend/`

```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # Linux/macOS/WSL
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Database setup
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run API tests
python test_api.py
```

### Frontend (React/TypeScript)

**Working directory:** Always run frontend commands from `/frontend/`

```bash
cd frontend

# Install dependencies
npm install

# Run development server (http://localhost:5173)
npm run dev

# Build for production
npm run build

# Lint code
npm run lint

# Preview production build
npm preview
```

## Architecture

### Backend Structure

**Django Apps (5 core apps):**

1. **users** - Custom user authentication and management
   - Custom User model extending AbstractBaseUser with multi-role support (buyer/seller/dealer)
   - Role flags: `is_seller` (auto-set on first listing), `is_dealer` (admin-approved)
   - Models: User, VerificationCode, UserBadge, ActivityLog
   - JWT authentication with access/refresh token rotation

2. **listings** - Core marketplace functionality
   - Models: Listing, Category, ListingImage, RatingReview, Favorite, ReportMisconduct, PricingPlan
   - Signal: Auto-promotes users to seller role on first listing creation (signals.py)
   - Full-text search with django-filter integration
   - Image uploads with validation (max 5MB per image)

3. **messaging** - Real-time chat system
   - Models: Chat, Message
   - One-to-one chats between buyer and seller per listing
   - Unread message tracking and notification integration

4. **notifications** - In-app notification system
   - Model: Notification
   - Helper functions in utils.py for common notification patterns
   - Types: chat, listing, review, payment, verification, system

5. **payments** - Payment processing and dealer management
   - Models: Payment, DealerApplication, DealerDocument, PricingPlan
   - Structure ready for Lumicash/Flutterwave integration
   - Dealer verification workflow with document upload

**Key Middleware:**
- `ActivityLogMiddleware` (umuhuza_api/middleware.py) - Logs user actions (login, registration, listings, payments, reports) with IP and user agent tracking

**Settings Configuration:**
- Environment variables via python-decouple (.env file)
- JWT tokens: 1-hour access, 7-day refresh with rotation
- CORS configured for React frontend (ports 3000, 5173)
- Timezone: Africa/Bujumbura
- File upload limit: 5MB

### Frontend Structure

**Directory organization:**
- `src/api/` - Axios-based API client modules
- `src/components/` - Organized by feature (common, layout, listings, messaging, notifications)
- `src/pages/` - Route-level page components
- `src/store/` - Zustand stores (authStore.ts for JWT auth state)
- `src/types/` - TypeScript type definitions
- `src/hooks/` - Custom React hooks (e.g., useRequireVerification)

**State Management:**
- Zustand with localStorage persistence for auth state
- JWT tokens stored in localStorage (access_token, refresh_token)
- TanStack Query for server state management

**Key Patterns:**
- ProtectedRoute component for authenticated routes
- VerificationBanner for prompting email/phone verification
- ReportModal for content moderation
- Custom form validation with react-hook-form + yup

## Important Implementation Details

### User Roles and Permissions

Users have **overlapping roles** (not mutually exclusive):
- All users start as buyers
- Creating a listing automatically sets `is_seller = True` via Django signal
- Dealer status requires application approval and sets `is_dealer = True`
- Legacy `user_role` field maintained for backward compatibility

**Key Signal:** `listings/signals.py` - `set_user_as_seller()` automatically promotes users when they create their first listing.

### Authentication Flow

1. Register → User created with `email_verified=False`, `phone_verified=False`
2. Login → Returns JWT access + refresh tokens
3. Token stored in localStorage (frontend) and used in Authorization header
4. Refresh token rotation enabled (new refresh token issued on refresh)
5. `SIMPLE_JWT` config uses `userid` field as USER_ID_FIELD

### API URL Structure

All endpoints prefixed with `/api/`:
- `/api/auth/*` - Authentication (users app)
- `/api/listings/*` - Listings CRUD
- `/api/categories/*` - Category listing
- `/api/chats/*` - Messaging
- `/api/notifications/*` - Notifications
- `/api/payments/*` - Payments and pricing plans
- `/api/dealer-applications/*` - Dealer applications
- `/api/reports/*` - Content reporting

See README.md for complete endpoint documentation.

### Database Conventions

- Custom column names use UPPERCASE (e.g., `db_column='USERID'`)
- Primary keys: `userid`, `listing_id`, `chat_id`, etc. (not Django's default `id`)
- Timestamps: `createdat`, `updatedat` (lowercase, single word)
- Foreign keys use `userid` pattern (e.g., `userid = ForeignKey(User)`)

### Notification Integration

Always use helper functions from `notifications/utils.py`:
- `notify_new_message()` - When message sent
- `notify_listing_status()` - When listing approved/rejected
- `notify_new_review()` - When review posted
- `notify_payment_success()` - After successful payment
- `notify_verification_complete()` - When email+phone verified

### File Uploads

**Listing images:**
- Handled via `ListingImage` model with foreign key to `Listing`
- Upload endpoint: `/api/listings/{id}/upload-image/`
- Max 5MB per image, validated in backend
- Can set primary image via `/api/listings/{listing_id}/images/{image_id}/set-primary/`

**Media storage:**
- Development: Local filesystem in `backend/media/`
- Production: Configure django-storages with S3/R2 (settings ready)

## Common Tasks

### Run Tests

```bash
# Backend API tests
cd backend
python test_api.py

# Frontend linting
cd frontend
npm run lint
```

### Database Migrations

```bash
cd backend
python manage.py makemigrations
python manage.py migrate

# Check migration status
python manage.py showmigrations

# Create empty migration for custom SQL
python manage.py makemigrations --empty <app_name>
```

### Django Shell

```bash
cd backend
python manage.py shell

# Example: Create categories
from listings.models import Category
from django.utils.text import slugify

Category.objects.create(
    cat_name="Real Estate - Houses",
    slug=slugify("Real Estate - Houses"),
    cat_description="Houses for sale or rent"
)
```

### Add New API Endpoint

1. Add view function/class to `<app>/views.py`
2. Add URL pattern to `<app>/urls.py`
3. Add serializer to `<app>/serializers.py` if needed
4. Update frontend API client in `frontend/src/api/`
5. Update this documentation if it's a major feature

### Environment Variables

**Required in backend/.env:**
- `DEBUG` - True/False
- `SECRET_KEY` - Django secret key
- `ALLOWED_HOSTS` - Comma-separated hostnames
- `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_HOST`, `DATABASE_PORT`

**Optional (for production):**
- Email: `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`
- SMS: `AFRICASTALKING_USERNAME`, `AFRICASTALKING_API_KEY`
- Payment: `LUMICASH_API_KEY`, `LUMICASH_SECRET`
- Storage: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`

## Git Workflow

Main branch: `main`

Recent work includes:
- Notification system UI implementation
- Report functionality for platform safety
- Platform UX improvements

When creating commits, follow the existing style visible in recent commits (action verb + concise description).

## Deployment Notes

Backend deployment checklist:
- Set `DEBUG=False`
- Configure production database (managed PostgreSQL)
- Set up email service (SendGrid/AWS SES)
- Configure SMS service (Africa's Talking)
- Set up file storage (AWS S3/Cloudflare R2)
- Configure payment gateway (Lumicash/Flutterwave)
- Enable SSL and security middleware
- Configure Celery with Redis for background tasks

Frontend deployment:
- Run `npm run build` in frontend directory
- Serve from `frontend/dist/`
- Configure CORS in backend for production domain

## Key Dependencies

**Backend:**
- Django 5.2.7 + djangorestframework 3.16.1
- psycopg2-binary 2.9.11 (PostgreSQL adapter)
- djangorestframework-simplejwt 5.5.1 (JWT auth)
- Pillow 12.0.0 + django-imagekit 6.0.0 (image processing)
- celery 5.5.3 + redis 6.4.0 (background tasks - optional)
- django-storages 1.14.2 + boto3 (cloud storage - optional)

**Frontend:**
- React 19.1.1 with TypeScript 5.9.3
- Vite 7.1.7 + @vitejs/plugin-react
- TailwindCSS 4.1.14
- Zustand 5.0.8 (state management)
- TanStack Query 5.90.5 (server state)
- axios 1.12.2 (HTTP client)
- react-hook-form 7.65.0 + yup 1.7.1 (forms)
- framer-motion 12.23.24 (animations)
