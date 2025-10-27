# 📡 Umuhuza API Documentation

Complete API reference for the Umuhuza marketplace platform.

**Base URL:** `http://127.0.0.1:8000/api` (Development)

**Production URL:** `https://api.umuhuza.com` (When deployed)

---

## 🆕 Recent Updates (January 2025)

### ✅ **Subscription-Based Listing System Implemented**

Major changes to align with monetization model:

- ✅ **Auto-Subscription**: New verified users automatically get Basic Plan (1 free listing)
- ✅ **Auto-Activation**: Listings are now automatically activated based on subscription quota
- ✅ **Quota Enforcement**: Users cannot create listings beyond their plan limit
- ✅ **Status Protection**: Users cannot manually change listing status to bypass subscription
- ✅ **Pricing Plans**: 3 tiers - Basic (free), Premium (20,000 BIF), Dealer (50,000 BIF)
- ✅ **Image Limits**: Enforced per plan (Basic: 5, Premium: 10, Dealer: 15)
- ✅ **User Role Upgrade**: First listing automatically sets `is_seller = True`

### 📝 **New/Updated Endpoints**

- `POST /listings/create/` - Now includes subscription enforcement and auto-activation
- `PATCH /listings/{id}/update-status/` - NEW: Safely change listing status (sold/hidden/active)
- `GET /subscription/current/` - Get user's active subscription details
- `PUT /listings/{id}/update/` - Now prevents status changes

### 🔧 **New Management Command**

```bash
python manage.py setup_pricing_plans
```

Creates/updates the 3 standard pricing plans (Basic, Premium, Dealer).

---

## 🔐 Authentication

All protected endpoints require a JWT Bearer token in the Authorization header.

### Get Token

**Endpoint:** `POST /auth/login/`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user": {
    "userid": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "user_role": "buyer"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### Use Token

Add to request headers:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Refresh Token

**Endpoint:** `POST /auth/token/refresh/`

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## 👤 User Management

### Register User

**Endpoint:** `POST /auth/register/`

**Request:**
```json
{
  "user_firstname": "John",
  "user_lastname": "Doe",
  "email": "john@example.com",
  "phone_number": "+25779123456",
  "password": "SecurePass123",
  "password_confirm": "SecurePass123"
}
```

**Response:** `201 Created`
```json
{
  "message": "Registration successful! Please verify your email and phone.",
  "user": {
    "userid": 1,
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone_number": "+25779123456",
    "is_verified": false,
    "email_verified": false,
    "phone_verified": false
  },
  "email_code": "123456",
  "phone_code": "654321"
}
```

### Verify Email

**Endpoint:** `POST /auth/verify-email/`

**Auth Required:** Yes

**Request:**
```json
{
  "code": "123456"
}
```

**Response:** `200 OK`
```json
{
  "message": "Email verified successfully"
}
```

### Verify Phone

**Endpoint:** `POST /auth/verify-phone/`

**Auth Required:** Yes

**Request:**
```json
{
  "code": "654321"
}
```

**Response:** `200 OK`
```json
{
  "message": "Phone verified successfully",
  "is_fully_verified": true
}
```

### Resend Verification Code

**Endpoint:** `POST /auth/resend-code/`

**Auth Required:** Yes

**Request:**
```json
{
  "code_type": "email"
}
```

**Response:** `200 OK`
```json
{
  "message": "Verification code sent to your email",
  "code": "789012"
}
```

### Get User Profile

**Endpoint:** `GET /auth/profile/`

**Auth Required:** Yes

**Response:** `200 OK`
```json
{
  "userid": 1,
  "user_firstname": "John",
  "user_lastname": "Doe",
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone_number": "+25779123456",
  "user_role": "seller",
  "profile_photo": "default-avatar.png",
  "is_verified": true,
  "email_verified": true,
  "phone_verified": true,
  "date_joined": "2025-01-15T10:30:00Z",
  "badges": [
    {
      "userbadge_id": 1,
      "badge_type": "verified",
      "issuedat": "2025-01-15T11:00:00Z",
      "is_active": true
    }
  ]
}
```

### Update Profile

**Endpoint:** `PUT /auth/profile/update/`

**Auth Required:** Yes

**Request:**
```json
{
  "user_firstname": "John",
  "user_lastname": "Smith",
  "phone_number": "+25779123456"
}
```

**Response:** `200 OK`
```json
{
  "message": "Profile updated successfully",
  "user": { /* updated user object */ }
}
```

---

## 💼 Subscription System

### Overview

The platform uses a subscription-based monetization model. Users must have an active subscription with available quota to create listings.

### How It Works

1. **New User Registration** → User created with `is_verified=False`
2. **Email + Phone Verification** → `is_verified=True`
3. **Auto-Subscription Created** → Basic Plan (1 listing, 60 days, 5 images, 0 BIF)
4. **Create Listing** → Auto-activated if quota available
5. **Quota Exhausted** → Must upgrade to Premium or Dealer plan

### Pricing Plans

| Plan | Price | Listings | Duration | Images | Featured |
|------|-------|----------|----------|--------|----------|
| **Basic Plan** | 0 BIF | 1 | 60 days | 5 | ❌ No |
| **Premium Plan** | 20,000 BIF | 10 | 90 days | 10 | ✅ Yes |
| **Dealer Monthly** | 50,000 BIF | Unlimited | 30 days | 15 | ✅ Yes |

### Get Current Subscription

**Endpoint:** `GET /subscription/current/`

**Auth Required:** Yes

**Response:** `200 OK`
```json
{
  "has_subscription": true,
  "subscription": {
    "user_subscr_id": 1,
    "user": {
      "userid": 1,
      "full_name": "John Doe"
    },
    "plan": {
      "pricing_id": 1,
      "pricing_name": "Basic Plan",
      "plan_price": "0.00",
      "max_listings": 1,
      "max_images_per_listing": 5,
      "duration_days": 60,
      "is_featured": false
    },
    "subscription_status": "active",
    "starts_at": "2025-01-24T10:00:00Z",
    "expires_at": null,
    "listings_used": 0,
    "remaining_listings": 1,
    "auto_renew": false
  }
}
```

**No Subscription Response:**
```json
{
  "message": "No active subscription found",
  "has_subscription": false
}
```

### Quota Enforcement

**When Creating Listings:**
- ✅ Checks if user has active subscription
- ✅ Checks if `remaining_listings > 0`
- ✅ Returns 403 if quota exhausted
- ✅ Auto-increments `listings_used` on success

**When Marking as Sold/Hidden:**
- ✅ Decrements `listings_used` (frees quota)

**When Reactivating:**
- ✅ Checks quota availability first
- ✅ Increments `listings_used` if reactivated

---

## 📂 Categories

### List Categories

**Endpoint:** `GET /categories/`

**Auth Required:** No

**Response:** `200 OK`
```json
[
  {
    "cat_id": 1,
    "cat_name": "Real Estate - Houses",
    "slug": "real-estate-houses",
    "cat_description": "Houses for sale or rent"
  },
  {
    "cat_id": 2,
    "cat_name": "Vehicles - Cars",
    "slug": "vehicles-cars",
    "cat_description": "Cars for sale"
  }
]
```

### Get Category Detail

**Endpoint:** `GET /categories/{id}/`

**Auth Required:** No

**Response:** `200 OK`
```json
{
  "cat_id": 1,
  "cat_name": "Real Estate - Houses",
  "slug": "real-estate-houses",
  "cat_description": "Houses for sale or rent"
}
```

---

## 🏠 Listings

### List All Listings

**Endpoint:** `GET /listings/`

**Auth Required:** No

**Query Parameters:**
- `category` - Filter by category ID
- `min_price` - Minimum price
- `max_price` - Maximum price
- `location` - Filter by location (partial match)
- `search` - Search in title and description
- `is_featured` - Filter featured listings (true/false)
- `ordering` - Sort field (e.g., `-createdat`, `listing_price`)
- `page` - Page number
- `page_size` - Items per page (max 100)

**Example Request:**
```
GET /listings/?category=1&min_price=50000000&max_price=100000000&location=Bujumbura&page=1
```

**Response:** `200 OK`
```json
{
  "count": 150,
  "next": "http://127.0.0.1:8000/api/listings/?page=2",
  "previous": null,
  "results": [
    {
      "listing_id": 1,
      "listing_title": "Beautiful House in Bujumbura",
      "list_description": "3 bedrooms, 2 bathrooms...",
      "listing_price": "75000000.00",
      "list_location": "Bujumbura, Rohero",
      "listing_status": "active",
      "views": 45,
      "is_featured": true,
      "createdat": "2025-01-15T10:30:00Z",
      "images": [
        {
          "listimage_id": 1,
          "image_url": "/media/listings/1/abc123.jpg",
          "is_primary": true,
          "display_order": 0
        }
      ],
      "category": {
        "cat_id": 1,
        "cat_name": "Real Estate - Houses"
      },
      "seller": {
        "userid": 2,
        "full_name": "Jane Smith",
        "profile_photo": "default-avatar.png",
        "is_verified": true
      }
    }
  ]
}
```

### Create Listing

**Endpoint:** `POST /listings/create/`

**Auth Required:** Yes

**⚠️ Requirements:**
- User must be verified (`is_verified = True`)
- User must have active subscription
- Subscription must have available quota (`remaining_listings > 0`)

**Request:**
```json
{
  "cat_id": 1,
  "listing_title": "Modern House in Bujumbura",
  "list_description": "Beautiful 3-bedroom house with garden. Modern kitchen, spacious living room.",
  "listing_price": 75000000,
  "list_location": "Bujumbura, Rohero"
}
```

**With Images (multipart/form-data):**
```
Form-Data:
  cat_id: 1
  listing_title: "Modern House in Bujumbura"
  list_description: "Beautiful 3-bedroom house..."
  listing_price: 75000000
  list_location: "Bujumbura, Rohero"
  images: [file1.jpg, file2.jpg, ...] (max based on plan)
```

**Success Response:** `201 Created`
```json
{
  "message": "Listing created and activated successfully!",
  "listing": {
    "listing_id": 5,
    "listing_title": "Modern House in Bujumbura",
    "listing_status": "active",
    "expiration_date": "2025-04-24T10:00:00Z",
    "is_featured": false,
    /* ... full listing object ... */
  },
  "images_uploaded": 3,
  "subscription_info": {
    "plan": "Basic Plan",
    "listings_used": 1,
    "listings_remaining": 0,
    "max_listings": 1
  }
}
```

**Error: Not Verified**
```json
{
  "error": "You must verify your email and phone before creating listings",
  "verification_required": true
}
```
Status: `403 Forbidden`

**Error: No Subscription**
```json
{
  "error": "No active subscription found. Please contact support.",
  "needs_subscription": true
}
```
Status: `403 Forbidden`

**Error: Quota Exceeded**
```json
{
  "error": "You have reached your listing limit (1 listings). Upgrade your plan to create more listings.",
  "quota_exceeded": true,
  "current_plan": "Basic Plan",
  "max_listings": 1,
  "listings_used": 1
}
```
Status: `403 Forbidden`

**⚡ Automatic Actions:**
- ✅ Listing status set to `active` (not pending!)
- ✅ `expiration_date` set based on plan duration
- ✅ `listings_used` incremented in subscription
- ✅ User's `is_seller` flag set to `True` (if first listing)
- ✅ Images limited to `max_images_per_listing` from plan

### Get Listing Detail

**Endpoint:** `GET /listings/{id}/`

**Auth Required:** No

**Response:** `200 OK`
```json
{
  "listing_id": 1,
  "listing_title": "Beautiful House in Bujumbura",
  "list_description": "Full description here...",
  "listing_price": "75000000.00",
  "list_location": "Bujumbura, Rohero",
  "listing_status": "active",
  "views": 46,
  "is_featured": true,
  "expiration_date": "2025-03-15T10:30:00Z",
  "createdat": "2025-01-15T10:30:00Z",
  "updatedat": "2025-01-15T10:30:00Z",
  "images": [ /* array of images */ ],
  "category": { /* category object */ },
  "seller": { /* seller object */ },
  "is_favorited": false
}
```

### Update Listing

**Endpoint:** `PUT /listings/{id}/update/` or `PATCH /listings/{id}/update/`

**Auth Required:** Yes (Owner only)

**⚠️ Important:**
- **Cannot change `listing_status` through this endpoint**
- Use `/listings/{id}/update-status/` instead
- Can only update: title, description, price, location, category

**Request:**
```json
{
  "listing_title": "Updated Title",
  "listing_price": 80000000,
  "list_description": "Updated description..."
}
```

**Response:** `200 OK`
```json
{
  "message": "Listing updated successfully",
  "listing": { /* updated listing object */ }
}
```

**Error: Attempted Status Change**
```json
{
  "error": "Cannot change listing status through this endpoint. Use /api/listings/{id}/update-status/ to mark as sold or hidden."
}
```
Status: `403 Forbidden`

---

### Update Listing Status

**Endpoint:** `PATCH /listings/{id}/update-status/`

**Auth Required:** Yes (Owner only)

**Purpose:** Safely change listing status with quota management

**Request:**
```json
{
  "status": "sold"
}
```

**Allowed Status Values:**
- `"sold"` - Mark listing as sold
- `"hidden"` - Hide listing from public view
- `"active"` - Reactivate a sold/hidden listing (requires quota)

**Success Response:** `200 OK`
```json
{
  "message": "Listing marked as sold",
  "listing": { /* updated listing object */ }
}
```

**Behavior:**
- **Marking as Sold/Hidden:**
  - ✅ Decrements `listings_used` (frees quota)
  - ✅ Allows creating new listing with freed quota

- **Reactivating (sold/hidden → active):**
  - ✅ Checks if quota available
  - ✅ Increments `listings_used`
  - ❌ Returns 403 if no quota

**Error: No Quota to Reactivate**
```json
{
  "error": "No available quota to reactivate listing. Please upgrade your plan.",
  "quota_exceeded": true
}
```
Status: `403 Forbidden`

**Error: Invalid Status**
```json
{
  "error": "Invalid status. Allowed: sold, hidden, active"
}
```
Status: `400 Bad Request`

### Delete Listing

**Endpoint:** `DELETE /listings/{id}/delete/`

**Auth Required:** Yes (Owner only)

**Response:** `204 No Content`
```json
{
  "message": "Listing deleted successfully"
}
```

### Get My Listings

**Endpoint:** `GET /listings/my-listings/`

**Auth Required:** Yes

**Response:** `200 OK`
```json
[
  { /* listing object */ },
  { /* listing object */ }
]
```

### Get Featured Listings

**Endpoint:** `GET /listings/featured/`

**Auth Required:** No

**Response:** `200 OK`
```json
[
  { /* featured listing */ },
  { /* featured listing */ }
]
```

### Get Similar Listings

**Endpoint:** `GET /listings/{id}/similar/`

**Auth Required:** No

**Response:** `200 OK`
```json
[
  { /* similar listing */ },
  { /* similar listing */ }
]
```

### Upload Listing Image

**Endpoint:** `POST /listings/{listing_id}/upload-image/`

**Auth Required:** Yes (Owner only)

**Content-Type:** `multipart/form-data`

**Request:**
```
Form-Data:
  image: (binary file)
```

**Response:** `201 Created`
```json
{
  "message": "Image uploaded successfully",
  "image": {
    "listimage_id": 10,
    "image_url": "/media/listings/5/xyz789.jpg",
    "is_primary": false,
    "display_order": 1
  }
}
```

### Delete Listing Image

**Endpoint:** `DELETE /listings/{listing_id}/images/{image_id}/`

**Auth Required:** Yes (Owner only)

**Response:** `204 No Content`
```json
{
  "message": "Image deleted successfully"
}
```

### Set Primary Image

**Endpoint:** `PUT /listings/{listing_id}/images/{image_id}/set-primary/`

**Auth Required:** Yes (Owner only)

**Response:** `200 OK`
```json
{
  "message": "Primary image updated"
}
```

---

## ⭐ Favorites

### Get Favorites

**Endpoint:** `GET /favorites/`

**Auth Required:** Yes

**Response:** `200 OK`
```json
[
  {
    "fav_id": 1,
    "listing": { /* full listing object */ },
    "createdat": "2025-01-15T12:00:00Z"
  }
]
```

### Toggle Favorite

**Endpoint:** `POST /favorites/{listing_id}/toggle/`

**Auth Required:** Yes

**Response:** `201 Created` or `200 OK`
```json
{
  "message": "Added to favorites",
  "is_favorited": true
}
```

---

## ⭐ Reviews

### Get User Reviews

**Endpoint:** `GET /reviews/user/{user_id}/`

**Auth Required:** No

**Response:** `200 OK`
```json
{
  "average_rating": 4.5,
  "total_reviews": 12,
  "reviews": [
    {
      "ratingrev_id": 1,
      "reviewer": {
        "userid": 3,
        "full_name": "Alice Johnson"
      },
      "rating": 5,
      "comment": "Excellent seller! Very professional.",
      "createdat": "2025-01-10T14:00:00Z"
    }
  ]
}
```

### Create Review

**Endpoint:** `POST /reviews/create/`

**Auth Required:** Yes

**Request:**
```json
{
  "reviewed_userid": 2,
  "listing_id": 5,
  "rating": 5,
  "comment": "Great experience! Highly recommended."
}
```

**Response:** `201 Created`
```json
{
  "message": "Review posted successfully",
  "review": { /* review object */ }
}
```

---

## 💬 Messaging

### Get All Chats

**Endpoint:** `GET /chats/`

**Auth Required:** Yes

**Response:** `200 OK`
```json
[
  {
    "chat_id": 1,
    "buyer": { /* user object */ },
    "seller": { /* user object */ },
    "listing": { /* listing object */ },
    "last_message_at": "2025-01-15T15:30:00Z",
    "createdat": "2025-01-15T10:00:00Z",
    "last_message": {
      "message_id": 5,
      "sender": { /* user object */ },
      "content": "When can I view the property?",
      "sentat": "2025-01-15T15:30:00Z"
    },
    "unread_count": 2
  }
]
```

### Create Chat

**Endpoint:** `POST /chats/create/`

**Auth Required:** Yes

**Request:**
```json
{
  "listing_id": 1
}
```

**Response:** `201 Created` or `200 OK`
```json
{
  "message": "Chat created",
  "chat": { /* chat object */ }
}
```

### Get Chat Messages

**Endpoint:** `GET /chats/{chat_id}/messages/`

**Auth Required:** Yes

**Response:** `200 OK`
```json
[
  {
    "message_id": 1,
    "sender": { /* user object */ },
    "content": "Hi! Is this property still available?",
    "message_type": "text",
    "is_read": true,
    "sentat": "2025-01-15T10:15:00Z",
    "read_at": "2025-01-15T10:20:00Z"
  },
  {
    "message_id": 2,
    "sender": { /* user object */ },
    "content": "Yes, it's still available. Would you like to schedule a viewing?",
    "message_type": "text",
    "is_read": false,
    "sentat": "2025-01-15T10:25:00Z",
    "read_at": null
  }
]
```

### Send Message

**Endpoint:** `POST /chats/{chat_id}/messages/send/`

**Auth Required:** Yes

**Request:**
```json
{
  "content": "When can I view the property?",
  "message_type": "text"
}
```

**Response:** `201 Created`
```json
{
  "message": "Message sent successfully",
  "data": { /* message object */ }
}
```

### Mark Messages as Read

**Endpoint:** `PUT /chats/{chat_id}/mark-read/`

**Auth Required:** Yes

**Response:** `200 OK`
```json
{
  "message": "3 messages marked as read"
}
```

### Get Unread Count

**Endpoint:** `GET /chats/unread-count/`

**Auth Required:** Yes

**Response:** `200 OK`
```json
{
  "unread_count": 5
}
```

---

## 🔔 Notifications

### Get Notifications

**Endpoint:** `GET /notifications/`

**Auth Required:** Yes

**Response:** `200 OK`
```json
{
  "unread_count": 3,
  "unread": [
    {
      "notif_id": 1,
      "notif_title": "New Message",
      "notif_message": "Jane Smith sent you a message",
      "notif_type": "chat",
      "link_url": "/chats/1",
      "is_read": false,
      "createdat": "2025-01-15T15:30:00Z"
    }
  ],
  "read": [ /* array of read notifications */ ]
}
```

### Mark Notification as Read

**Endpoint:** `PUT /notifications/{id}/read/`

**Auth Required:** Yes

**Response:** `200 OK`
```json
{
  "message": "Notification marked as read"
}
```

### Mark All as Read

**Endpoint:** `PUT /notifications/read-all/`

**Auth Required:** Yes

**Response:** `200 OK`
```json
{
  "message": "15 notifications marked as read"
}
```

### Get Unread Count

**Endpoint:** `GET /notifications/unread-count/`

**Auth Required:** Yes

**Response:** `200 OK`
```json
{
  "unread_count": 3
}
```

---

## 🚨 Reports

### Submit Report

**Endpoint:** `POST /reports/create/`

**Auth Required:** Yes

**Request:**
```json
{
  "listing_id": 5,
  "report_type": "spam",
  "report_reason": "This listing appears to be a duplicate"
}
```

**Response:** `201 Created`
```json
{
  "message": "Report submitted successfully. We will review it shortly.",
  "report": { /* report object */ }
}
```

### Get My Reports

**Endpoint:** `GET /reports/my-reports/`

**Auth Required:** Yes

**Response:** `200 OK`
```json
[
  {
    "reportmiscond_id": 1,
    "reporter": { /* user object */ },
    "listing_id": 5,
    "report_type": "spam",
    "report_status": "pending",
    "createdat": "2025-01-15T16:00:00Z"
  }
]
```

---

## 💳 Payments & Pricing

### Get Pricing Plans

**Endpoint:** `GET /pricing-plans/`

**Auth Required:** No

**Response:** `200 OK`
```json
[
  {
    "pricing_id": 1,
    "pricing_name": "Basic Plan",
    "pricing_description": "Perfect for occasional sellers",
    "plan_price": "0.00",
    "duration_days": 60,
    "category_scope": "all",
    "max_listings": 1,
    "max_images_per_listing": 5,
    "is_featured": false,
    "is_active": true
  },
  {
    "pricing_id": 2,
    "pricing_name": "Premium Plan",
    "pricing_description": "Boost your listings with featured placement",
    "plan_price": "20000.00",
    "duration_days": 90,
    "category_scope": "all",
    "max_listings": 10,
    "max_images_per_listing": 10,
    "is_featured": true,
    "is_active": true
  },
  {
    "pricing_id": 3,
    "pricing_name": "Dealer Monthly",
    "pricing_description": "Unlimited listings for professional dealers",
    "plan_price": "50000.00",
    "duration_days": 30,
    "category_scope": "all",
    "max_listings": 999999,
    "max_images_per_listing": 15,
    "is_featured": true,
    "is_active": true
  }
]
```

**📝 Note:** Run `python manage.py setup_pricing_plans` to create/update these plans.

### Initiate Payment

**Endpoint:** `POST /payments/initiate/`

**Auth Required:** Yes

**Request:**
```json
{
  "pricing_id": 2,
  "listing_id": 5,
  "payment_method": "mobile_money",
  "phone_number": "+25779123456"
}
```

**Response:** `201 Created`
```json
{
  "payment_id": "550e8400-e29b-41d4-a716-446655440000",
  "payment_ref": "UMH-ABC123XYZ",
  "amount": 10000.0,
  "message": "Check your phone for payment prompt",
  "status": "pending"
}
```

### Verify Payment

**Endpoint:** `POST /payments/verify/`

**Auth Required:** Yes

**Request:**
```json
{
  "payment_ref": "UMH-ABC123XYZ"
}
```

**Response:** `200 OK`
```json
{
  "message": "Payment verified successfully",
  "payment": {
    "payment_id": "550e8400-e29b-41d4-a716-446655440000",
    "payment_status": "successful",
    "confirmed_at": "2025-01-15T17:00:00Z"
  }
}
```

### Get Payment History

**Endpoint:** `GET /payments/history/`

**Auth Required:** Yes

**Response:** `200 OK`
```json
[
  {
    "payment_id": "550e8400-e29b-41d4-a716-446655440000",
    "payment_amount": "10000.00",
    "payment_method": "mobile_money",
    "payment_status": "successful",
    "createdat": "2025-01-15T16:55:00Z",
    "confirmed_at": "2025-01-15T17:00:00Z"
  }
]
```

---

## 👔 Dealer Applications

### Submit Application

**Endpoint:** `POST /dealer-applications/create/`

**Auth Required:** Yes

**Request:**
```json
{
  "business_name": "Premium Real Estate",
  "business_type": "real_estate",
  "business_address": "123 Main Street, Bujumbura",
  "business_phone": "+25779111222",
  "business_email": "contact@premiumre.bi",
  "tax_id": "TIN123456789"
}
```

**Response:** `201 Created`
```json
{
  "message": "Dealer application submitted successfully",
  "application": { /* application object */ }
}
```

### Get Application Status

**Endpoint:** `GET /dealer-applications/status/`

**Auth Required:** Yes

**Response:** `200 OK`
```json
{
  "dealerapp_id": 1,
  "business_name": "Premium Real Estate",
  "business_type": "real_estate",
  "appli_status": "pending",
  "createdat": "2025-01-15T18:00:00Z",
  "documents": [ /* array of uploaded documents */ ]
}
```

---

## ⚠️ Error Responses

### 400 Bad Request
```json
{
  "error": "Validation failed",
  "details": {
    "email": ["This field is required."],
    "password": ["Password must be at least 8 characters."]
  }
}
```

### 401 Unauthorized
```json
{
  "error": "Authentication credentials were not provided"
}
```

### 403 Forbidden
```json
{
  "error": "You do not have permission to perform this action"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "An internal server error occurred"
}
```

---

## 📊 Rate Limiting

- **Public endpoints:** 100 requests per minute
- **Authenticated endpoints:** 1000 requests per minute
- **File uploads:** 10 uploads per minute

Rate limit headers included in response:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642345678
```

---

## 🔄 Pagination

All list endpoints support pagination:

**Query Parameters:**
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 20, max: 100)

**Response Format:**
```json
{
  "count": 150,
  "next": "http://api.example.com/endpoint/?page=2",
  "previous": null,
  "results": [ /* array of items */ ]
}
```

---

## 🔍 Filtering & Search

**Available Filters:**
- Exact match: `?field=value`
- Range: `?min_field=value&max_field=value`
- Search: `?search=keyword`
- Ordering: `?ordering=field` or `?ordering=-field` (descending)

**Example:**
```
GET /listings/?category=1&min_price=50000000&search=house&ordering=-createdat
```

---

## 🔧 Backend Architecture Changes

### New Features Implemented (January 2025)

#### 1. **Auto-Subscription System**

**File:** `backend/users/signals.py`

**How it works:**
- Django signal (`post_save`) on User model
- Triggers when `is_verified` changes to `True`
- Automatically creates Basic Plan subscription
- User gets 1 free listing immediately

**Code Location:** `assign_free_tier_to_new_user` function

---

#### 2. **Subscription-Based Listing Creation**

**File:** `backend/listings/views.py` - `listing_create` function

**Checks Performed:**
1. ✅ User verification status
2. ✅ Active subscription exists
3. ✅ Quota availability (`has_quota` property)
4. ✅ Image count vs plan limit

**Auto-Actions:**
1. ✅ Set status to `active`
2. ✅ Set `expiration_date`
3. ✅ Increment `listings_used`
4. ✅ Set `is_seller = True`

---

#### 3. **Status Protection System**

**Files:**
- `backend/listings/views.py` - `listing_update` (blocks status changes)
- `backend/listings/views.py` - `listing_update_status` (new endpoint)

**Security:**
- Users cannot bypass subscription by manually setting `listing_status='active'`
- Separate endpoint for status changes with quota checks
- Prevents fraud and abuse

---

#### 4. **Quota Management**

**Model:** `UserSubscription` (backend/listings/models.py)

**Properties:**
- `remaining_listings` - Computed property: `max_listings - listings_used`
- `has_quota` - Boolean: `remaining_listings > 0`
- `is_active` - Checks if subscription is active and not expired

**Behavior:**
- Creating listing → Increments `listings_used`
- Marking as sold/hidden → Decrements `listings_used`
- Reactivating → Checks quota first

---

### Management Commands

#### Setup Pricing Plans

**Command:** `python manage.py setup_pricing_plans`

**What it does:**
- Creates/updates 3 standard pricing plans
- Safe to run multiple times (uses `update_or_create`)
- Plans: Basic (0 BIF), Premium (20,000 BIF), Dealer (50,000 BIF)

**Location:** `backend/listings/management/commands/setup_pricing_plans.py`

**Usage:**
```bash
cd backend
source venv/bin/activate
python manage.py setup_pricing_plans
```

**Output:**
```
✓ Created: Basic Plan
✓ Created: Premium Plan
✓ Created: Dealer Monthly

✅ Pricing plans setup complete!
Total plans: 3
```

---

### Database Models

#### Key Models

**UserSubscription** (`backend/listings/models.py`)
```python
class UserSubscription(models.Model):
    userid = ForeignKey(User)
    pricing_id = ForeignKey(PricingPlan)
    subscription_status = CharField  # active, expired, cancelled
    starts_at = DateTimeField
    expires_at = DateTimeField
    listings_used = IntegerField
    auto_renew = BooleanField

    @property
    def remaining_listings(self):
        return self.pricing_id.max_listings - self.listings_used

    @property
    def has_quota(self):
        return self.remaining_listings > 0

    @property
    def is_active(self):
        # Check status and expiration
```

**PricingPlan** (`backend/listings/models.py`)
```python
class PricingPlan(models.Model):
    pricing_name = CharField
    plan_price = DecimalField
    duration_days = IntegerField
    max_listings = IntegerField
    max_images_per_listing = IntegerField
    is_featured = BooleanField
    is_active = BooleanField
```

**Listing** (`backend/listings/models.py`)
```python
class Listing(models.Model):
    listing_status = CharField  # active, pending, sold, hidden, expired
    expiration_date = DateTimeField
    is_featured = BooleanField
    views = IntegerField
    # ... other fields
```

---

### API Endpoint Summary

#### New Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/subscription/current/` | GET | Get user's active subscription |
| `/listings/{id}/update-status/` | PATCH | Change listing status safely |

#### Modified Endpoints

| Endpoint | Changes |
|----------|---------|
| `/listings/create/` | ✅ Quota enforcement<br>✅ Auto-activation<br>✅ Subscription checks |
| `/listings/{id}/update/` | ❌ Status changes blocked |

---

### Testing

```bash
# 1. Start servers
./dev.sh

# 2. Register & verify user
# 3. Check subscription created
# 4. Create listing → Auto-activated
# 5. Try 2nd listing → Blocked
# 6. Upgrade to Premium
# 7. Create more listings → Success
```

---

### Future Improvements

**For Production:**

1. **Cron Jobs:**
   - Expire subscriptions automatically
   - Expire listings past `expiration_date`
   - Send renewal reminders

2. **Payment Integration:**
   - Replace simulated payment with real gateway
   - Add manual payment proof upload (Phase 1 MVP)
   - Webhook handlers for payment verification

3. **Admin Features:**
   - Manual subscription management
   - Listing approval system (optional)
   - Fraud detection

4. **Analytics:**
   - Subscription metrics
   - Revenue tracking
   - Listing performance

---

## 📚 Additional Documentation

- **Frontend API Usage:** See `frontend/src/api/` directory
- **Quick Start:** `QUICKSTART.md` for getting started

---

