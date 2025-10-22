# 🏠 Umuhuza - Real Estate & Vehicle Marketplace Platform

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Django 5.0+](https://img.shields.io/badge/django-5.0+-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL 15+](https://img.shields.io/badge/postgresql-15+-blue.svg)](https://www.postgresql.org/)

**Umuhuza** is a modern, secure marketplace platform connecting buyers and sellers of real estate and vehicles in Burundi. The platform eliminates middlemen, provides verified user accounts, and offers a seamless experience for property and vehicle transactions.

---

## 🌟 **Features**

### Core Features
- ✅ **User Authentication & Authorization** (JWT-based)
- ✅ **Email & Phone Verification** (OTP)
- ✅ **Multi-role System** (Buyer, Seller, Dealer)
- ✅ **Advanced Listing Management** with image uploads
- ✅ **Real-time Messaging** between buyers and sellers
- ✅ **Search & Filter** with full-text search
- ✅ **Favorites/Wishlist**
- ✅ **Ratings & Reviews**
- ✅ **In-app Notifications**
- ✅ **Payment Integration** (structure ready)
- ✅ **Dealer Applications** & verification
- ✅ **Report & Moderation System**
- ✅ **User Badges & Gamification**
- ✅ **Activity Logging** for security
- ✅ **Comprehensive Admin Panel**

### Security Features
- 🔐 JWT Token Authentication
- 🔐 Password Hashing (PBKDF2)
- 🔐 CORS Protection
- 🔐 Rate Limiting Ready
- 🔐 SQL Injection Protection
- 🔐 XSS Protection
- 🔐 CSRF Protection

---

## 📋 **Table of Contents**

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Database Setup](#database-setup)
5. [Running the Project](#running-the-project)
6. [API Documentation](#api-documentation)
7. [Testing](#testing)
8. [Project Structure](#project-structure)
9. [Contributing](#contributing)
10. [License](#license)

---

## 🔧 **Prerequisites**

Before you begin, ensure you have the following installed:

- **Python 3.12+** - [Download](https://www.python.org/downloads/)
- **PostgreSQL 15+** - [Download](https://www.postgresql.org/download/)
- **Git** - [Download](https://git-scm.com/downloads)
- **pip** (comes with Python)
- **virtualenv** (optional but recommended)

### System Requirements
- **OS:** Windows 10/11, macOS 10.15+, Ubuntu 20.04+, or WSL2
- **RAM:** Minimum 4GB (8GB recommended)
- **Storage:** At least 2GB free space

---

## 🚀 **Installation**

### 1. Clone the Repository

```bash
git clone https://github.com/Dahl23/Umuhuza.git
cd umuhuza/backend
```

### 2. Create Virtual Environment

**On Linux/macOS/WSL:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚙️ **Configuration**

### 1. Create Environment File

Create a `.env` file in the `backend` directory:

```bash
touch .env
```

### 2. Configure Environment Variables

Add the following to your `.env` file:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-super-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DATABASE_NAME=umuhuza
DATABASE_USER=umuhuza_admin
DATABASE_PASSWORD=umuhuza_admin_2025
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Email Configuration (Optional - for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password

# SMS Configuration (Optional - for production)
AFRICASTALKING_USERNAME=your-username
AFRICASTALKING_API_KEY=your-api-key

# Payment Gateway (Optional - for production)
LUMICASH_API_KEY=your-lumicash-api-key
LUMICASH_SECRET=your-lumicash-secret

# Redis (Optional - for Celery)
REDIS_URL=redis://localhost:6379/0
```

**⚠️ IMPORTANT:** Never commit your `.env` file to version control!

---

## 🗄️ **Database Setup**

### 1. Install PostgreSQL

**On Ubuntu/WSL:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo service postgresql start
```

**On macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**On Windows:**
Download and install from [PostgreSQL official website](https://www.postgresql.org/download/windows/)

### 2. Create Database and User

```bash
# Access PostgreSQL
sudo -u postgres psql

# Or on Windows/macOS
psql -U postgres
```

**Run these SQL commands:**

```sql
-- Create database
CREATE DATABASE umuhuza;

-- Create user
CREATE USER umuhuza_admin WITH PASSWORD 'umuhuza_admin_2025';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE umuhuza TO umuhuza_admin;

-- Connect to database
\c umuhuza

-- Grant schema privileges (PostgreSQL 15+)
GRANT ALL ON SCHEMA public TO umuhuza_admin;

-- Exit
\q
```

### 3. Test Database Connection

```bash
psql -U umuhuza_admin -d umuhuza -h localhost
# Enter password when prompted
# If successful, type \q to exit
```

---

## 🏃 **Running the Project**

### 1. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

**Enter the following when prompted:**
- Email address
- Phone number
- First name
- Last name
- Password (minimum 8 characters)

### 3. Load Sample Data (Optional)

```bash
python manage.py shell
```

**Paste and run:**

```python
from listings.models import Category, PricingPlan
from django.utils.text import slugify

# Create Categories
categories = [
    {"name": "Real Estate - Houses", "description": "Houses for sale or rent"},
    {"name": "Real Estate - Apartments", "description": "Apartments for sale or rent"},
    {"name": "Real Estate - Land & Plots", "description": "Land and plots for sale"},
    {"name": "Vehicles - Cars", "description": "Cars for sale"},
    {"name": "Vehicles - Motorcycles", "description": "Motorcycles for sale"},
]

for cat in categories:
    Category.objects.get_or_create(
        cat_name=cat["name"],
        defaults={
            "slug": slugify(cat["name"]),
            "cat_description": cat["description"]
        }
    )

# Create Pricing Plans
plans = [
    {"name": "Basic Plan", "description": "1 listing for 30 days", "price": 0, "duration": 30, "scope": "all", "max_listings": 1, "max_images": 3, "featured": False},
    {"name": "Premium Plan", "description": "Featured listing for 60 days", "price": 10000, "duration": 60, "scope": "all", "max_listings": 1, "max_images": 10, "featured": True},
    {"name": "Dealer Monthly", "description": "Unlimited listings for 30 days", "price": 50000, "duration": 30, "scope": "all", "max_listings": 999, "max_images": 10, "featured": True},
]

for plan in plans:
    PricingPlan.objects.get_or_create(
        pricing_name=plan["name"],
        defaults={
            "pricing_description": plan["description"],
            "plan_price": plan["price"],
            "duration_days": plan["duration"],
            "category_scope": plan["scope"],
            "max_listings": plan["max_listings"],
            "max_images_per_listing": plan["max_images"],
            "is_featured": plan["featured"]
        }
    )

print("✓ Sample data created!")
exit()
```

### 4. Run Development Server

```bash
python manage.py runserver
```

The API will be available at: **http://127.0.0.1:8000/**

### 5. Access Admin Panel

Navigate to: **http://127.0.0.1:8000/admin/**

Login with your superuser credentials.

---

## 📖 **API Documentation**

### Base URL
```
http://127.0.0.1:8000/api
```

### Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### Available Endpoints

#### **Authentication** (`/api/auth/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register/` | Register new user | No |
| POST | `/auth/login/` | Login user | No |
| POST | `/auth/logout/` | Logout user | Yes |
| POST | `/auth/token/refresh/` | Refresh JWT token | No |
| POST | `/auth/verify-email/` | Verify email with code | Yes |
| POST | `/auth/verify-phone/` | Verify phone with code | Yes |
| POST | `/auth/resend-code/` | Resend verification code | Yes |
| GET | `/auth/profile/` | Get current user profile | Yes |
| PUT | `/auth/profile/update/` | Update user profile | Yes |

#### **Categories** (`/api/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/categories/` | List all categories | No |
| GET | `/categories/{id}/` | Get category detail | No |

#### **Listings** (`/api/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/listings/` | List all listings (with filters) | No |
| POST | `/listings/create/` | Create new listing | Yes |
| GET | `/listings/{id}/` | Get listing detail | No |
| PUT | `/listings/{id}/update/` | Update listing | Yes (Owner) |
| DELETE | `/listings/{id}/delete/` | Delete listing | Yes (Owner) |
| GET | `/listings/my-listings/` | Get user's listings | Yes |
| GET | `/listings/featured/` | Get featured listings | No |
| GET | `/listings/{id}/similar/` | Get similar listings | No |
| POST | `/listings/{id}/upload-image/` | Upload listing image | Yes (Owner) |
| DELETE | `/listings/{listing_id}/images/{image_id}/` | Delete image | Yes (Owner) |
| PUT | `/listings/{listing_id}/images/{image_id}/set-primary/` | Set primary image | Yes (Owner) |

#### **Favorites** (`/api/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/favorites/` | Get user's favorites | Yes |
| POST | `/favorites/{listing_id}/toggle/` | Add/remove favorite | Yes |

#### **Reviews** (`/api/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/reviews/user/{user_id}/` | Get user reviews | No |
| POST | `/reviews/create/` | Create review | Yes |

#### **Messaging** (`/api/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/chats/` | List user's chats | Yes |
| POST | `/chats/create/` | Create/get chat | Yes |
| GET | `/chats/{id}/` | Get chat detail | Yes |
| GET | `/chats/{chat_id}/messages/` | Get chat messages | Yes |
| POST | `/chats/{chat_id}/messages/send/` | Send message | Yes |
| PUT | `/chats/{chat_id}/mark-read/` | Mark messages as read | Yes |
| DELETE | `/chats/{id}/archive/` | Archive chat | Yes |
| GET | `/chats/unread-count/` | Get unread count | Yes |

#### **Notifications** (`/api/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/notifications/` | List notifications | Yes |
| PUT | `/notifications/{id}/read/` | Mark as read | Yes |
| PUT | `/notifications/read-all/` | Mark all as read | Yes |
| DELETE | `/notifications/{id}/delete/` | Delete notification | Yes |
| DELETE | `/notifications/clear-all/` | Clear all read | Yes |
| GET | `/notifications/unread-count/` | Get unread count | Yes |

#### **Reports** (`/api/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/reports/create/` | Submit report | Yes |
| GET | `/reports/my-reports/` | Get user's reports | Yes |
| GET | `/reports/{id}/` | Get report detail | Yes (Owner) |

#### **Payments** (`/api/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/pricing-plans/` | List pricing plans | No |
| POST | `/payments/initiate/` | Initiate payment | Yes |
| POST | `/payments/verify/` | Verify payment | Yes |
| GET | `/payments/history/` | Payment history | Yes |
| GET | `/payments/{payment_id}/` | Payment detail | Yes |

#### **Dealer Applications** (`/api/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/dealer-applications/create/` | Submit application | Yes |
| GET | `/dealer-applications/status/` | Get application status | Yes |
| POST | `/dealer-applications/documents/` | Upload documents | Yes |

### Query Parameters

**Listings Filtering:**
```
GET /api/listings/?category=1&min_price=1000&max_price=50000&location=Bujumbura&search=house&ordering=-createdat
```

Supported filters:
- `category` - Filter by category ID
- `min_price` - Minimum price
- `max_price` - Maximum price
- `location` - Filter by location (partial match)
- `search` - Full-text search in title and description
- `ordering` - Sort by field (prefix with `-` for descending)
- `is_featured` - Filter featured listings (true/false)
- `page` - Page number for pagination
- `page_size` - Items per page (default: 20, max: 100)

---

## 🧪 **Testing**

### Run Automated Tests

```bash
python test_api.py
```

This will test all major endpoints and display results.

### Manual API Testing

#### Using cURL

**Register User:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_firstname": "John",
    "user_lastname": "Doe",
    "email": "john@test.com",
    "phone_number": "+25779123456",
    "password": "SecurePass123",
    "password_confirm": "SecurePass123"
  }'
```

**Login:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@test.com",
    "password": "SecurePass123"
  }'
```

**Get Listings:**
```bash
curl http://127.0.0.1:8000/api/listings/
```

#### Using Postman

1. Import the API collection (if provided)
2. Set base URL: `http://127.0.0.1:8000/api`
3. For authenticated requests, add header:
   - Key: `Authorization`
   - Value: `Bearer <your_token>`

---

## 📁 **Project Structure**

```
backend/
├── umuhuza_api/           # Main project folder
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI configuration
│   ├── middleware.py      # Custom middleware
│   └── __init__.py
│
├── users/                 # User management app
│   ├── models.py          # User, VerificationCode, UserBadge, ActivityLog
│   ├── serializers.py     # User serializers
│   ├── views.py           # Authentication views
│   ├── urls.py            # User URLs
│   ├── admin.py           # User admin
│   └── utils.py           # Helper functions
│
├── listings/              # Listings management app
│   ├── models.py          # Listing, Category, ListingImage, Review, Favorite, Report
│   ├── serializers.py     # Listing serializers
│   ├── views.py           # Listing views
│   ├── urls.py            # Listing URLs
│   └── admin.py           # Listing admin
│
├── messaging/             # Messaging app
│   ├── models.py          # Chat, Message
│   ├── serializers.py     # Messaging serializers
│   ├── views.py           # Messaging views
│   ├── urls.py            # Messaging URLs
│   └── admin.py           # Messaging admin
│
├── notifications/         # Notifications app
│   ├── models.py          # Notification
│   ├── serializers.py     # Notification serializers
│   ├── views.py           # Notification views
│   ├── urls.py            # Notification URLs
│   ├── utils.py           # Notification helpers
│   └── admin.py           # Notification admin
│
├── payments/              # Payments & Dealer app
│   ├── models.py          # Payment, DealerApplication, DealerDocument
│   ├── serializers.py     # Payment serializers
│   ├── views.py           # Payment views
│   ├── urls.py            # Payment URLs
│   └── admin.py           # Payment admin
│
├── media/                 # User uploaded files
│   ├── listings/          # Listing images
│   ├── profiles/          # Profile photos
│   └── documents/         # Dealer documents
│
├── staticfiles/           # Static files (CSS, JS)
├── templates/             # Email templates (optional)
├── requirements.txt       # Python dependencies
├── manage.py              # Django management script
├── test_api.py            # API test script
├── .env                   # Environment variables (not in git)
├── .gitignore             # Git ignore file
└── README.md              # This file
```

---

## 🔄 **Database Models**

### Core Models

1. **User** - Custom user model with roles
2. **VerificationCode** - Email/phone verification
3. **UserBadge** - User achievement badges
4. **ActivityLog** - User activity tracking
5. **Category** - Listing categories
6. **Listing** - Main listing model
7. **ListingImage** - Listing photos
8. **PricingPlan** - Pricing plans for featured listings
9. **Payment** - Payment transactions
10. **RatingReview** - User reviews
11. **Favorite** - User favorites/wishlist
12. **Chat** - Chat conversations
13. **Message** - Chat messages
14. **Notification** - User notifications
15. **ReportMisconduct** - Content reports
16. **DealerApplication** - Dealer applications
17. **DealerDocument** - Dealer verification documents

### Entity Relationship Diagram

```
User ──┬─< Listing ──┬─< ListingImage
       │             ├─< Favorite
       │             └─< RatingReview
       │
       ├─< VerificationCode
       ├─< UserBadge
       ├─< ActivityLog
       ├─< Notification
       ├─< Payment
       ├─< DealerApplication ──< DealerDocument
       ├─< Chat ──< Message
       └─< ReportMisconduct
```

---

## 🚀 **Deployment**

### Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Configure proper `SECRET_KEY`
- [ ] Set up production database (managed PostgreSQL)
- [ ] Configure email service (SendGrid/AWS SES)
- [ ] Configure SMS service (Africa's Talking)
- [ ] Set up file storage (AWS S3/Cloudflare R2)
- [ ] Configure payment gateway (Lumicash/Flutterwave)
- [ ] Set up SSL certificate
- [ ] Configure CORS for production domains
- [ ] Set up Redis for Celery (if using background tasks)
- [ ] Configure logging and monitoring
- [ ] Set up automated backups
- [ ] Configure rate limiting

### Recommended Hosting Platforms

- **Railway.app** - Easiest deployment
- **DigitalOcean App Platform** - Good balance
- **AWS EC2** - Full control
- **Render.com** - Free tier available

### Environment Variables for Production

```env
DEBUG=False
SECRET_KEY=<generate-strong-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,api.yourdomain.com

DATABASE_URL=postgresql://user:pass@host:5432/dbname

# File Storage
AWS_ACCESS_KEY_ID=<your-key>
AWS_SECRET_ACCESS_KEY=<your-secret>
AWS_STORAGE_BUCKET_NAME=<bucket-name>
AWS_S3_REGION_NAME=us-east-1

# Email
EMAIL_HOST=smtp.sendgrid.net
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=<sendgrid-api-key>

# SMS
AFRICASTALKING_USERNAME=<username>
AFRICASTALKING_API_KEY=<api-key>

# Payment
LUMICASH_API_KEY=<api-key>
LUMICASH_SECRET=<secret>
```

---

## 🤝 **Contributing**

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Write unit tests for new features
- Update documentation when adding features

---

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 **Authors**

- **Andy Miguel Habyarimana** - *Initial work* - [Go to page](https://github.com/miguelandy875)
- **Dahl Ndayisenga** - *Initial work* - [Go to page](https://github.com/Dahl23)

---

## 🙏 **Acknowledgments**

- Django Rest Framework for excellent API tools
- PostgreSQL for robust database
- All contributors and testers

---

## 📞 **Support**

For support, email support@umuhuza.bi.

---

## 🗺️ **Roadmap**

### Version 1.0 (Current)
- ✅ Core marketplace functionality
- ✅ User authentication & verification
- ✅ Messaging system
- ✅ Payment integration structure

### Version 1.1 (Planned)
- [ ] WebSocket for real-time messaging
- [ ] Advanced search with Elasticsearch
- [ ] Mobile app (React Native)
- [ ] Multi-language support (French, Kirundi)

### Version 2.0 (Future)
- [ ] AI-powered fraud detection
- [ ] Virtual property tours
- [ ] Escrow payment system
- [ ] Integration with banks for financing

---

## 📊 **API Response Examples**

### Successful Response
```json
{
  "message": "Listing created successfully",
  "listing": {
    "listing_id": 1,
    "listing_title": "Beautiful House in Bujumbura",
    "listing_price": 75000000,
    "listing_status": "pending",
    "createdat": "2025-01-15T10:30:00Z"
  }
}
```

### Error Response
```json
{
  "error": "Invalid credentials"
}
```

### Validation Error Response
```json
{
  "email": ["This field is required."],
  "password": ["Password must be at least 8 characters."]
}
```

---

**Made with ❤️ in Burundi 🇧🇮**
