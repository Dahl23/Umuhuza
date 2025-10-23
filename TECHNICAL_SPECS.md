# 🔧 Umuhuza Platform - Technical Specifications

**Version 1.0 | Last Updated: January 2025**

This document provides comprehensive technical specifications for developers and AI systems working on the Umuhuza marketplace platform. It details the architecture, data flow, component interactions, and implementation details.

---

## 📋 Table of Contents

1. [System Architecture](#system-architecture)
2. [Technology Stack](#technology-stack)
3. [Database Schema](#database-schema)
4. [API Endpoints](#api-endpoints)
5. [Authentication & Authorization](#authentication--authorization)
6. [Component Architecture](#component-architecture)
7. [Data Flow Diagrams](#data-flow-diagrams)
8. [Integration Points](#integration-points)
9. [Security Specifications](#security-specifications)
10. [Performance Requirements](#performance-requirements)
11. [Deployment Architecture](#deployment-architecture)

---

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Browser    │  │  Mobile App  │  │   PWA        │  │
│  │   (React)    │  │  (Future)    │  │  (Future)    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                    HTTPS/REST API
                          │
┌─────────────────────────────────────────────────────────┐
│                  APPLICATION LAYER                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │          Express.js REST API Server              │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │  │
│  │  │  Auth    │ │  Listing │ │   Messaging      │ │  │
│  │  │ Service  │ │  Service │ │   Service        │ │  │
│  │  └──────────┘ └──────────┘ └──────────────────┘ │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │  │
│  │  │ Payment  │ │  User    │ │   Notification   │ │  │
│  │  │ Service  │ │ Service  │ │   Service        │ │  │
│  │  └──────────┘ └──────────┘ └──────────────────┘ │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                    DATA LAYER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   MySQL      │  │    Redis     │  │   File       │  │
│  │  Database    │  │   Cache      │  │  Storage     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│              EXTERNAL SERVICES LAYER                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Email      │  │     SMS      │  │   Payment    │  │
│  │   (SMTP)     │  │   (Twilio)   │  │  Gateway     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Architectural Principles

- **Separation of Concerns**: Frontend (React) completely decoupled from backend (Express)
- **RESTful API**: Stateless communication via JSON
- **Token-Based Auth**: JWT for authentication
- **Microservices-Ready**: Modular service design for future scaling
- **Database-First**: MySQL as single source of truth

---

## 2. Technology Stack

### 2.1 Frontend Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Framework | React | 18+ | UI framework |
| Language | TypeScript | 5+ | Type safety |
| Routing | React Router | 6+ | Client-side routing |
| State Management | React Query + Context | 5+ | Server & local state |
| Styling | Tailwind CSS | 3+ | Utility-first CSS |
| Forms | React Hook Form | 7+ | Form management |
| HTTP Client | Axios | 1+ | API requests |
| Icons | Lucide React | Latest | Icon library |

**File Structure:**
```
frontend/
├── src/
│   ├── api/           # API client & endpoints
│   ├── components/    # Reusable components
│   ├── context/       # React Context providers
│   ├── hooks/         # Custom React hooks
│   ├── pages/         # Page components
│   ├── types/         # TypeScript types
│   └── utils/         # Utility functions
├── public/            # Static assets
└── package.json
```

### 2.2 Backend Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Runtime | Node.js | 18+ | JavaScript runtime |
| Framework | Express.js | 4+ | Web framework |
| Language | JavaScript | ES6+ | Server-side language |
| Database | MySQL | 8+ | Relational database |
| ORM | Raw SQL | - | Database queries |
| Auth | JWT | Latest | Token-based auth |
| File Upload | Multer | 1+ | Handle file uploads |
| Email | Nodemailer | 6+ | Email service |
| SMS | Twilio | Latest | SMS notifications |
| Validation | Express Validator | 7+ | Input validation |

**File Structure:**
```
backend/
├── config/            # Configuration files
├── middleware/        # Express middleware
├── routes/            # API route handlers
├── controllers/       # Business logic
├── models/            # Database queries
├── utils/             # Utility functions
├── uploads/           # Uploaded files
└── server.js          # Entry point
```

### 2.3 Database

- **Primary Database**: MySQL 8.0+
- **Cache Layer**: Redis (future)
- **File Storage**: Local filesystem (future: AWS S3/DigitalOcean Spaces)

---

## 3. Database Schema

### 3.1 Core Tables

#### **users** (User Accounts)
```sql
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    user_type ENUM('individual', 'dealer') DEFAULT 'individual',
    email_verified BOOLEAN DEFAULT FALSE,
    phone_verified BOOLEAN DEFAULT FALSE,
    profile_picture VARCHAR(255),
    bio TEXT,
    location VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_phone (phone),
    INDEX idx_user_type (user_type)
);
```

**Relationships:**
- One user → Many listings
- One user → Many messages sent
- One user → Many messages received
- One user → Many favorites
- One user → Many reviews given
- One user → Many reviews received

#### **categories** (Listing Categories)
```sql
CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    slug VARCHAR(50) NOT NULL UNIQUE,
    icon VARCHAR(50),
    description TEXT,
    parent_category_id INT,
    is_active BOOLEAN DEFAULT TRUE,
    display_order INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_category_id) REFERENCES categories(category_id),
    INDEX idx_parent (parent_category_id),
    INDEX idx_slug (slug)
);
```

**Categories Structure:**
- Real Estate (parent)
  - Land (child)
  - Houses (child)
  - Apartments (child)
  - Commercial (child)
- Vehicles (parent)
  - Cars (child)
  - Motorcycles (child)
  - Trucks (child)

#### **listings** (Property & Vehicle Listings)
```sql
CREATE TABLE listings (
    listing_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(15,2) NOT NULL,
    location VARCHAR(100) NOT NULL,
    status ENUM('active', 'sold', 'pending', 'inactive') DEFAULT 'active',
    listing_type ENUM('sale', 'rent') DEFAULT 'sale',
    is_featured BOOLEAN DEFAULT FALSE,
    featured_until TIMESTAMP NULL,
    views INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    INDEX idx_user (user_id),
    INDEX idx_category (category_id),
    INDEX idx_status (status),
    INDEX idx_price (price),
    INDEX idx_created (created_at),
    FULLTEXT idx_search (title, description, location)
);
```

**Business Rules:**
- Free users: 3 active listings max
- Premium users: 10 active listings max
- Dealers: Unlimited listings
- Featured listings: Require payment

#### **listing_images** (Listing Photos)
```sql
CREATE TABLE listing_images (
    image_id INT PRIMARY KEY AUTO_INCREMENT,
    listing_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    display_order INT DEFAULT 0,
    is_primary BOOLEAN DEFAULT FALSE,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (listing_id) REFERENCES listings(listing_id) ON DELETE CASCADE,
    INDEX idx_listing (listing_id)
);
```

**Constraints:**
- Max 10 images per listing
- At least 1 image required
- First image is primary by default

#### **listing_details** (Category-Specific Attributes)
```sql
CREATE TABLE listing_details (
    detail_id INT PRIMARY KEY AUTO_INCREMENT,
    listing_id INT NOT NULL,
    attribute_name VARCHAR(50) NOT NULL,
    attribute_value VARCHAR(255) NOT NULL,
    FOREIGN KEY (listing_id) REFERENCES listings(listing_id) ON DELETE CASCADE,
    INDEX idx_listing (listing_id),
    INDEX idx_attribute (attribute_name)
);
```

**Real Estate Attributes:**
- bedrooms, bathrooms, square_meters, land_size, year_built

**Vehicle Attributes:**
- make, model, year, mileage, fuel_type, transmission, condition

#### **conversations** (Message Threads)
```sql
CREATE TABLE conversations (
    conversation_id INT PRIMARY KEY AUTO_INCREMENT,
    listing_id INT NOT NULL,
    buyer_id INT NOT NULL,
    seller_id INT NOT NULL,
    last_message_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    buyer_unread_count INT DEFAULT 0,
    seller_unread_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (listing_id) REFERENCES listings(listing_id) ON DELETE CASCADE,
    FOREIGN KEY (buyer_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (seller_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_conversation (listing_id, buyer_id, seller_id),
    INDEX idx_buyer (buyer_id),
    INDEX idx_seller (seller_id),
    INDEX idx_last_message (last_message_at)
);
```

#### **messages** (Individual Messages)
```sql
CREATE TABLE messages (
    message_id INT PRIMARY KEY AUTO_INCREMENT,
    conversation_id INT NOT NULL,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    message_text TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_conversation (conversation_id),
    INDEX idx_created (created_at)
);
```

**Message Flow:**
1. Buyer clicks "Contact Seller" on listing
2. System creates conversation (if doesn't exist)
3. Message saved with conversation_id
4. Unread count incremented for receiver
5. Real-time notification sent

#### **favorites** (Saved Listings)
```sql
CREATE TABLE favorites (
    favorite_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    listing_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (listing_id) REFERENCES listings(listing_id) ON DELETE CASCADE,
    UNIQUE KEY unique_favorite (user_id, listing_id),
    INDEX idx_user (user_id)
);
```

#### **reviews** (User Ratings)
```sql
CREATE TABLE reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    reviewer_id INT NOT NULL,
    reviewed_user_id INT NOT NULL,
    listing_id INT,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (reviewer_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (listing_id) REFERENCES listings(listing_id) ON DELETE SET NULL,
    UNIQUE KEY unique_review (reviewer_id, reviewed_user_id, listing_id),
    INDEX idx_reviewed_user (reviewed_user_id)
);
```

**Review Rules:**
- Can only review after transaction
- One review per user per listing
- Rating: 1-5 stars
- Cannot review yourself

#### **subscriptions** (Premium Plans)
```sql
CREATE TABLE subscriptions (
    subscription_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    plan_type ENUM('basic', 'premium', 'dealer') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status ENUM('active', 'expired', 'cancelled') DEFAULT 'active',
    amount_paid DECIMAL(10,2),
    payment_method VARCHAR(50),
    auto_renew BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_status (status),
    INDEX idx_end_date (end_date)
);
```

**Plan Types:**
- Basic: Free (3 listings)
- Premium: 20,000 BIF/month (10 listings)
- Dealer: 50,000 BIF/month (unlimited)

#### **transactions** (Payment History)
```sql
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    listing_id INT,
    transaction_type ENUM('listing_fee', 'featured', 'subscription', 'boost') NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'BIF',
    payment_method VARCHAR(50),
    payment_status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    payment_reference VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (listing_id) REFERENCES listings(listing_id) ON DELETE SET NULL,
    INDEX idx_user (user_id),
    INDEX idx_status (payment_status),
    INDEX idx_created (created_at)
);
```

#### **dealer_applications** (Dealer Verification)
```sql
CREATE TABLE dealer_applications (
    application_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    business_name VARCHAR(200) NOT NULL,
    business_type VARCHAR(100),
    registration_number VARCHAR(100),
    tax_id VARCHAR(100),
    address TEXT,
    phone VARCHAR(20),
    website VARCHAR(200),
    description TEXT,
    documents_url VARCHAR(255),
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    reviewed_by INT,
    review_notes TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_by) REFERENCES users(user_id),
    INDEX idx_user (user_id),
    INDEX idx_status (status)
);
```

#### **notifications** (User Notifications)
```sql
CREATE TABLE notifications (
    notification_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    related_id INT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_created (user_id, created_at),
    INDEX idx_is_read (is_read)
);
```

**Notification Types:**
- new_message, listing_sold, listing_expired, review_received, application_status

#### **reports** (User-Generated Reports)
```sql
CREATE TABLE reports (
    report_id INT PRIMARY KEY AUTO_INCREMENT,
    reporter_id INT NOT NULL,
    reported_user_id INT,
    reported_listing_id INT,
    report_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    status ENUM('pending', 'reviewing', 'resolved', 'dismissed') DEFAULT 'pending',
    admin_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    FOREIGN KEY (reporter_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (reported_user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (reported_listing_id) REFERENCES listings(listing_id) ON DELETE CASCADE,
    INDEX idx_status (status),
    INDEX idx_created (created_at)
);
```

### 3.2 Database Optimization

**Indexes:**
- All foreign keys indexed
- Search fields (title, location) have FULLTEXT indexes
- Frequently filtered fields (status, created_at) indexed

**Query Optimization:**
- Use prepared statements for SQL injection prevention
- Implement pagination (LIMIT/OFFSET)
- Use JOIN efficiently (avoid N+1 queries)
- Cache frequently accessed data (Redis)

---

## 4. API Endpoints

### 4.1 Base URL

```
Development: http://localhost:5000/api
Production: https://api.umuhuza.bi/api
```

### 4.2 Authentication Endpoints

#### POST `/auth/register`
Register new user account.

**Request:**
```json
{
  "full_name": "Jean Dupont",
  "email": "jean@example.com",
  "phone": "+25779123456",
  "password": "SecurePass123!",
  "user_type": "individual"
}
```

**Response (201):**
```json
{
  "message": "Registration successful. Please verify your email.",
  "user": {
    "user_id": 1,
    "full_name": "Jean Dupont",
    "email": "jean@example.com",
    "user_type": "individual"
  }
}
```

#### POST `/auth/login`
User login.

**Request:**
```json
{
  "email": "jean@example.com",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "user_id": 1,
    "full_name": "Jean Dupont",
    "email": "jean@example.com",
    "user_type": "individual",
    "email_verified": true
  }
}
```

#### POST `/auth/verify-email`
Verify email with token sent via email.

**Request:**
```json
{
  "token": "abc123xyz789"
}
```

#### POST `/auth/reset-password`
Request password reset.

**Request:**
```json
{
  "email": "jean@example.com"
}
```

### 4.3 Listing Endpoints

#### GET `/listings`
Get all listings with filters.

**Query Parameters:**
- `category_id` (optional): Filter by category
- `location` (optional): Filter by location
- `min_price` (optional): Minimum price
- `max_price` (optional): Maximum price
- `listing_type` (optional): 'sale' or 'rent'
- `search` (optional): Search in title/description
- `page` (default: 1): Page number
- `limit` (default: 20): Items per page

**Response (200):**
```json
{
  "listings": [
    {
      "listing_id": 1,
      "title": "Beautiful 3BR House in Bujumbura",
      "description": "...",
      "price": 150000000,
      "location": "Rohero",
      "status": "active",
      "images": [
        {"image_url": "/uploads/...", "is_primary": true}
      ],
      "user": {
        "user_id": 5,
        "full_name": "Seller Name",
        "profile_picture": "..."
      },
      "category": {
        "category_id": 2,
        "name": "Houses"
      },
      "created_at": "2025-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

#### GET `/listings/:id`
Get single listing details.

**Response (200):**
```json
{
  "listing_id": 1,
  "title": "Beautiful 3BR House",
  "description": "...",
  "price": 150000000,
  "location": "Rohero",
  "listing_type": "sale",
  "status": "active",
  "views": 245,
  "images": [...],
  "details": {
    "bedrooms": "3",
    "bathrooms": "2",
    "square_meters": "200"
  },
  "user": {
    "user_id": 5,
    "full_name": "Seller Name",
    "user_type": "dealer",
    "rating": 4.8,
    "total_reviews": 12
  },
  "created_at": "2025-01-15T10:30:00Z"
}
```

#### POST `/listings`
Create new listing (requires authentication).

**Headers:**
```
Authorization: Bearer <token>
```

**Request (multipart/form-data):**
```
title: "Beautiful 3BR House"
description: "..."
price: 150000000
location: "Rohero"
category_id: 2
listing_type: "sale"
bedrooms: 3
bathrooms: 2
images: [File, File, File]
```

**Response (201):**
```json
{
  "message": "Listing created successfully",
  "listing_id": 1
}
```

#### PUT `/listings/:id`
Update listing (must be owner).

#### DELETE `/listings/:id`
Delete listing (must be owner).

#### PUT `/listings/:id/views`
Increment view count.

### 4.4 Messaging Endpoints

#### GET `/conversations`
Get user's conversations (requires auth).

**Response (200):**
```json
{
  "conversations": [
    {
      "conversation_id": 1,
      "listing": {
        "listing_id": 5,
        "title": "Toyota Camry 2020",
        "primary_image": "..."
      },
      "other_user": {
        "user_id": 10,
        "full_name": "Buyer Name",
        "profile_picture": "..."
      },
      "last_message": {
        "message_text": "Is it still available?",
        "created_at": "2025-01-20T14:30:00Z"
      },
      "unread_count": 2
    }
  ]
}
```

#### GET `/conversations/:id/messages`
Get messages in conversation.

**Response (200):**
```json
{
  "messages": [
    {
      "message_id": 1,
      "sender_id": 5,
      "message_text": "Hello, is this still available?",
      "is_read": true,
      "created_at": "2025-01-20T10:00:00Z"
    },
    {
      "message_id": 2,
      "sender_id": 10,
      "message_text": "Yes, it's available!",
      "is_read": false,
      "created_at": "2025-01-20T10:05:00Z"
    }
  ]
}
```

#### POST `/conversations`
Create conversation / send first message.

**Request:**
```json
{
  "listing_id": 5,
  "message_text": "Is this still available?"
}
```

#### POST `/conversations/:id/messages`
Send message in existing conversation.

**Request:**
```json
{
  "message_text": "Can we meet tomorrow?"
}
```

#### PUT `/messages/:id/read`
Mark message as read.

### 4.5 User Endpoints

#### GET `/users/profile`
Get current user profile (requires auth).

#### PUT `/users/profile`
Update user profile.

**Request:**
```json
{
  "full_name": "Jean Dupont",
  "bio": "Experienced property investor",
  "location": "Bujumbura"
}
```

#### GET `/users/:id`
Get public user profile.

**Response (200):**
```json
{
  "user_id": 5,
  "full_name": "Jean Dupont",
  "user_type": "dealer",
  "bio": "...",
  "location": "Bujumbura",
  "rating": 4.8,
  "total_reviews": 25,
  "active_listings": 12,
  "member_since": "2024-06-15"
}
```

#### GET `/users/:id/listings`
Get user's public listings.

#### GET `/users/:id/reviews`
Get user's reviews.

### 4.6 Favorite Endpoints

#### GET `/favorites`
Get user's saved listings.

#### POST `/favorites`
Add listing to favorites.

**Request:**
```json
{
  "listing_id": 5
}
```

#### DELETE `/favorites/:listing_id`
Remove from favorites.

### 4.7 Review Endpoints

#### POST `/reviews`
Create review.

**Request:**
```json
{
  "reviewed_user_id": 10,
  "listing_id": 5,
  "rating": 5,
  "comment": "Great seller, smooth transaction!"
}
```

#### GET `/reviews/user/:user_id`
Get reviews for a user.

### 4.8 Payment Endpoints

#### POST `/payments/initiate`
Initiate payment for featured listing or subscription.

**Request:**
```json
{
  "listing_id": 5,
  "payment_type": "featured",
  "duration_days": 30
}
```

#### POST `/payments/verify`
Verify payment status.

### 4.9 Dealer Endpoints

#### POST `/dealer/apply`
Submit dealer application.

**Request (multipart/form-data):**
```
business_name: "ABC Real Estate"
business_type: "Real Estate Agency"
registration_number: "123456"
documents: [File]
```

#### GET `/dealer/applications/:id`
Get application status.

### 4.10 Admin Endpoints

#### GET `/admin/reports`
Get all reports (admin only).

#### PUT `/admin/reports/:id`
Update report status.

#### GET `/admin/dealer-applications`
Get pending applications.

#### PUT `/admin/dealer-applications/:id`
Approve/reject application.

---

## 5. Authentication & Authorization

### 5.1 JWT Token Structure

**Token Payload:**
```json
{
  "user_id": 1,
  "email": "jean@example.com",
  "user_type": "individual",
  "iat": 1643723400,
  "exp": 1643809800
}
```

**Token Expiration:**
- Access Token: 24 hours
- Refresh Token: 30 days (future)

### 5.2 Middleware Chain

```javascript
// Example protected route
router.post('/listings', 
  authMiddleware.verifyToken,      // 1. Verify JWT
  authMiddleware.requireVerified,  // 2. Check email verified
  listingValidation,                // 3. Validate input
  listingController.create          // 4. Execute
);
```

### 5.3 Permission Levels

| Action | Visitor | Registered | Verified | Premium | Dealer |
|--------|---------|------------|----------|---------|--------|
| View listings | ✅ | ✅ | ✅ | ✅ | ✅ |
| Contact seller | ❌ | ✅ | ✅ | ✅ | ✅ |
| Create listing | ❌ | ❌ | ✅ | ✅ | ✅ |
| Edit own listing | ❌ | ❌ | ✅ | ✅ | ✅ |
| Delete own listing | ❌ | ❌ | ✅ | ✅ | ✅ |
| Featured listing | ❌ | ❌ | 💰 | 💰 | ✅ |
| Unlimited listings | ❌ | ❌ | ❌ (3) | ❌ (10) | ✅ |

### 5.4 Security Measures

- **Password Hashing**: bcrypt with salt rounds = 10
- **SQL Injection**: Parameterized queries
- **XSS Protection**: Input sanitization
- **CSRF**: Token validation (future)
- **Rate Limiting**: 100 requests/15 minutes per IP
- **File Upload**: Whitelist extensions, max 5MB per image

---

## 6. Component Architecture

### 6.1 Frontend Component Hierarchy

```
App
├── Router
│   ├── PublicRoutes
│   │   ├── HomePage
│   │   │   ├── Hero
│   │   │   ├── SearchBar
│   │   │   ├── CategoryGrid
│   │   │   ├── FeaturedListings
│   │   │   └── StatsSection
│   │   ├── ListingsPage
│   │   │   ├── FilterSidebar
│   │   │   ├── ListingGrid
│   │   │   └── Pagination
│   │   ├── ListingDetailPage
│   │   │   ├── ImageGallery
│   │   │   ├── ListingInfo
│   │   │   ├── SellerCard
│   │   │   ├── ContactButton
│   │   │   └── SimilarListings
│   │   ├── LoginPage
│   │   └── RegisterPage
│   └── ProtectedRoutes (requires auth)
│       ├── CreateListingPage
│       │   ├── ListingForm
│       │   ├── ImageUploader
│       │   └── PricingInfo
│       ├── MessagesPage
│       │   ├── ConversationList
│       │   ├── ChatWindow
│       │   └── MessageInput
│       ├── ProfilePage
│       │   ├── ProfileHeader
│       │   ├── UserListings
│       │   └── ReviewsList
│       ├── FavoritesPage
│       ├── SettingsPage
│       └── DealerApplicationPage
└── Shared Components
    ├── Header (Navbar)
    ├── Footer
    ├── Modal
    ├── Toast
    ├── Spinner
    └── ErrorBoundary
```

### 6.2 State Management Strategy

**React Context Providers:**
```typescript
// AuthContext - Current user & authentication
{
  user: User | null,
  token: string | null,
  login: (email, password) => Promise<void>,
  logout: () => void,
  isAuthenticated: boolean
}

// NotificationContext - Real-time notifications
{
  unreadCount: number,
  notifications: Notification[],
  markAsRead: (id) => void
}
```

**React Query (Server State):**
- Listings data
- User profiles
- Messages
- Reviews
- Caching & automatic refetching

### 6.3 React Component Patterns

**Composition Pattern:**
```typescript
// ListingCard is reusable
<FeaturedListings>
  {listings.map(listing => (
    <ListingCard 
      key={listing.id} 
      listing={listing}
      featured={true}
    />
  ))}
</FeaturedListings>
```

**Custom Hooks:**
```typescript
// useAuth hook
const { user, login, logout } = useAuth();

// useListings hook
const { listings, isLoading, error } = useListings(filters);

// useMessages hook
const { conversations, sendMessage } = useMessages();
```

---

## 7. Data Flow Diagrams

### 7.1 User Registration Flow

```
[Browser] → POST /auth/register → [Express API]
                                        ↓
                                   Validate Input
                                        ↓
                                   Hash Password
                                        ↓
                                   Insert to DB
                                        ↓
                              Generate Email Token
                                        ↓
                            [Nodemailer] → Send Email
                                        ↓
                          ← Response (201 Created)
                                        ↓
[Browser] ← Display "Check Email"
```

### 7.2 Listing Creation Flow

```
[Browser] → Form Submit → Image Upload
                              ↓
                    POST /listings (multipart)
                              ↓
                        [Express API]
                              ↓
                      Verify JWT Token
                              ↓
                    Check Email Verified
                              ↓
                    Check Listing Limit
                              ↓
                      Validate Form Data
                              ↓
                Save Images to /uploads
                              ↓
              INSERT INTO listings + details
                              ↓
              INSERT INTO listing_images
                              ↓
            ← Response (listing_id)
                              ↓
[Browser] ← Redirect to Listing Detail
```

### 7.3 Messaging Flow

```
[Buyer Browser] → Click "Contact Seller"
                              ↓
                  POST /conversations
                  {listing_id, message}
                              ↓
                        [Express API]
                              ↓
             Check if conversation exists
                              ↓
                  Create if not exists
                              ↓
                INSERT INTO messages
                              ↓
        UPDATE conversations.last_message_at
        INCREMENT seller_unread_count
                              ↓
    [Notification Service] → Send SMS/Email
                              ↓
            ← Response (conversation_id)
                              ↓
[Buyer] ← Redirect to Messages Page

[Seller] → GET /conversations (polling every 10s)
                              ↓
         ← {unread_count: 1}
                              ↓
         Display notification badge
```

### 7.4 Search & Filter Flow

```
[Browser] → Enter search "apartment bujumbura"
                              ↓
        Select filters: price_range, bedrooms
                              ↓
    GET /listings?search=apartment+bujumbura
                 &location=Bujumbura
                 &min_price=50000000
                 &max_price=100000000
                 &bedrooms=2
                              ↓
                        [Express API]
                              ↓
        Build SQL Query with WHERE clauses
                              ↓
              Execute with FULLTEXT search
              + JOIN categories
              + JOIN users
              + JOIN listing_images
                              ↓
            Apply pagination (LIMIT 20)
                              ↓
    ← Response {listings[], pagination{}}
                              ↓
[Browser] ← Render ListingGrid
```

---

## 8. Integration Points

### 8.1 Email Service (Nodemailer)

**Configuration:**
```javascript
const transporter = nodemailer.createTransport({
  host: "smtp.gmail.com",
  port: 587,
  secure: false,
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASSWORD
  }
});
```

**Email Templates:**
- Welcome email (registration)
- Email verification
- Password reset
- New message notification
- Listing status updates
- Dealer application status

### 8.2 SMS Service (Twilio)

**Configuration:**
```javascript
const twilio = require('twilio');
const client = twilio(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);
```

**SMS Triggers:**
- Phone verification (OTP)
- New message alerts
- Listing sold confirmation
- Payment confirmations

### 8.3 Payment Gateway Integration (Future)

**Providers:**
- Mobile Money (Lumicash, Ecocash)
- Bank transfer
- Credit card (Stripe)

**Payment Flow:**
1. User initiates payment
2. Create transaction record (status: pending)
3. Redirect to payment gateway
4. Receive callback/webhook
5. Update transaction status
6. Activate feature (featured/subscription)

### 8.4 Cloud Storage (Future)

**Migration from local to AWS S3:**
- Image uploads
- User documents
- Backup database

---

## 9. Security Specifications

### 9.1 Input Validation

**Backend Validation (Express Validator):**
```javascript
// Example for listing creation
body('title').trim().isLength({min: 10, max: 200}),
body('price').isFloat({min: 0}),
body('phone').matches(/^\+257[0-9]{8}$/),
body('email').isEmail().normalizeEmail()
```

**Frontend Validation:**
- Real-time form validation
- Custom error messages
- Prevent double submission

### 9.2 File Upload Security

**Allowed Extensions:**
- Images: .jpg, .jpeg, .png, .webp
- Documents: .pdf

**Security Checks:**
```javascript
const fileFilter = (req, file, cb) => {
  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
  if (allowedTypes.includes(file.mimetype)) {
    cb(null, true);
  } else {
    cb(new Error('Invalid file type'), false);
  }
};
```

**File Size Limits:**
- Images: 5MB per file, 50MB total
- Documents: 10MB

### 9.3 Rate Limiting

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: 'Too many requests, please try again later'
});

app.use('/api/', limiter);
```

### 9.4 CORS Configuration

```javascript
const cors = require('cors');

app.use(cors({
  origin: process.env.FRONTEND_URL,
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
```

---

## 10. Performance Requirements

### 10.1 Response Time Targets

| Endpoint Type | Target | Maximum |
|---------------|--------|---------|
| Static pages | <100ms | 200ms |
| API (simple) | <200ms | 500ms |
| API (complex) | <500ms | 1000ms |
| Search queries | <300ms | 800ms |
| Image loading | <1s | 2s |

### 10.2 Scalability Requirements

**Current (MVP):**
- 1,000 concurrent users
- 50,000 listings
- 100,000 messages/day

**Year 1:**
- 10,000 concurrent users
- 500,000 listings
- 1M messages/day

### 10.3 Caching Strategy

**Browser Caching:**
- Static assets: 7 days
- Images: 30 days
- API responses: No cache

**Redis Caching (Future):**
- Category list: 24 hours
- User sessions: 24 hours
- Featured listings: 1 hour
- Search results: 5 minutes

### 10.4 Database Performance

**Query Optimization:**
- Use indexes on all foreign keys
- Implement pagination (never load all records)
- Use SELECT specific columns (not SELECT *)
- Optimize JOIN queries

**Connection Pooling:**
```javascript
const pool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  connectionLimit: 10,
  queueLimit: 0
});
```

---

## 11. Deployment Architecture

### 11.1 Development Environment

```
Local Machine
├── Frontend: localhost:5173 (Vite dev server)
├── Backend: localhost:5000 (Express)
└── Database: localhost:3306 (MySQL)
```

### 11.2 Production Environment (Recommended)

```
┌─────────────────────────────────────┐
│        Domain: umuhuza.bi           │
├─────────────────────────────────────┤
│         Cloudflare CDN              │
│       (SSL, DDoS Protection)        │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│      Load Balancer (Nginx)          │
└─────────────────────────────────────┘
         ↓              ↓
┌─────────────┐  ┌─────────────┐
│ Frontend    │  │   Backend   │
│ (React)     │  │  (Express)  │
│ Port 3000   │  │  Port 5000  │
└─────────────┘  └─────────────┘
                        ↓
                ┌─────────────┐
                │   MySQL     │
                │   Port 3306 │
                └─────────────┘
```

### 11.3 Hosting Options

**Option 1: VPS (Recommended for MVP)**
- Provider: DigitalOcean / Linode / Vultr
- Plan: $20-40/month
- Specs: 2 CPU, 4GB RAM, 80GB SSD
- OS: Ubuntu 24.04 LTS

**Option 2: Managed Services**
- Frontend: Vercel / Netlify (Free tier)
- Backend: Heroku / Railway ($10-20/month)
- Database: PlanetScale / AWS RDS ($15-30/month)

### 11.4 Deployment Process

**Backend Deployment:**
```bash
# 1. Clone repository
git clone https://github.com/yourusername/umuhuza-backend.git

# 2. Install dependencies
npm install

# 3. Set environment variables
cp .env.example .env
nano .env

# 4. Start with PM2
pm2 start server.js --name umuhuza-api

# 5. Setup Nginx reverse proxy
sudo nano /etc/nginx/sites-available/umuhuza
```

**Frontend Deployment:**
```bash
# 1. Build for production
npm run build

# 2. Deploy to Vercel
vercel --prod

# Or serve with Nginx
sudo cp -r dist/* /var/www/umuhuza/
```

### 11.5 Environment Variables

**Backend (.env):**
```env
NODE_ENV=production
PORT=5000
DB_HOST=localhost
DB_USER=umuhuza_user
DB_PASSWORD=secure_password
DB_NAME=umuhuza_db
JWT_SECRET=your_jwt_secret_key_here
EMAIL_USER=noreply@umuhuza.bi
EMAIL_PASSWORD=email_app_password
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=+1234567890
FRONTEND_URL=https://umuhuza.bi
```

**Frontend (.env):**
```env
VITE_API_URL=https://api.umuhuza.bi/api
VITE_APP_NAME=Umuhuza
```

### 11.6 Monitoring & Logging

**Tools:**
- **Error Tracking**: Sentry
- **Performance**: New Relic / Datadog
- **Uptime**: UptimeRobot
- **Logs**: PM2 logs / CloudWatch

**Health Check Endpoint:**
```javascript
app.get('/health', (req, res) => {
  res.json({
    status: 'OK',
    timestamp: new Date(),
    uptime: process.uptime(),
    environment: process.env.NODE_ENV
  });
});
```

---

## 12. Development Guidelines

### 12.1 Code Style

**Backend (JavaScript):**
- Use ES6+ features
- Async/await for promises
- Consistent error handling
- JSDoc comments for functions

**Frontend (TypeScript):**
- Strict TypeScript mode
- Functional components with hooks
- Named exports for components
- PropTypes or TypeScript interfaces

### 12.2 Git Workflow

**Branch Strategy:**
```
main (production)
├── develop (staging)
│   ├── feature/user-authentication
│   ├── feature/messaging-system
│   ├── bugfix/image-upload
│   └── hotfix/login-error
```

**Commit Messages:**
```
feat: Add messaging system
fix: Resolve image upload bug
refactor: Improve listing query performance
docs: Update API documentation
```

### 12.3 Testing Strategy

- **Unit Tests**: Jest (backend), Vitest (frontend)
- **Integration Tests**: Supertest (API)
- **E2E Tests**: Cypress / Playwright
- **Manual Testing**: See TESTING_GUIDE.md

---

## 13. Future Enhancements

### 13.1 Technical Debt & Improvements

**Phase 2 (Q2 2025):**
- Implement Redis caching
- Add WebSocket for real-time messaging
- Migrate to AWS S3 for file storage
- Implement search with Elasticsearch

**Phase 3 (Q3 2025):**
- Microservices architecture
- GraphQL API
- Mobile app (React Native)
- AI-powered recommendations

### 13.2 API Versioning

Future API structure:
```
/api/v1/listings  (current)
/api/v2/listings  (with breaking changes)
```

---

**END OF TECHNICAL SPECIFICATIONS**

*For user experience details, see USER_EXPERIENCE_GUIDE.md*  
*For testing procedures, see TESTING_GUIDE.md*  
*For monetization details, see MONETIZATION_MODEL.md*
