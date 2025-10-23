# Payment Feature & "Promote to Featured" Guide

## Issue: Star Button Not Showing

If you can't see the star (⭐) button on your listings to promote them to featured, here's why:

### When the Star Button Shows

The "Promote to Featured" star button only appears when **BOTH** conditions are met:

1. ✅ **Listing is NOT already featured**: `is_featured === false`
2. ✅ **Listing status is 'active'**: `listing_status === 'active'`

### Common Issue: Pending Listings

**The most common reason** the star button doesn't show is because new listings default to `'pending'` status (waiting for admin approval).

### Quick Fix

Run this command to check and fix listing statuses:

```bash
cd backend
python manage.py shell < fix_listing_status.py
```

This script will:
- Show all your listings with their current status
- Identify which listings can show the star button
- Automatically update 'pending' listings to 'active' for testing
- Display before/after status

### Manual Fix (Alternative)

If you prefer to manually update listings in Django admin or shell:

```python
# Django shell
python manage.py shell

from listings.models import Listing

# Update all pending listings to active
Listing.objects.filter(listing_status='pending').update(listing_status='active')

# Or update a specific listing
listing = Listing.objects.get(listing_id=1)
listing.listing_status = 'active'
listing.save()
```

## How the Payment Feature Works

### 1. Promote to Featured Button

Located on: **My Listings page** (`/my-listings`)

- Shows as a star (⭐) icon button
- Only visible on active, non-featured listings
- Opens the Payment Modal when clicked

### 2. Payment Modal

Shows when you click the star button:

**Features:**
- Grid of pricing plans (only featured plans shown)
- Plan details: price, duration, features
- Visual selection with checkmark
- Payment method selection (Mobile Money / Card)
- Phone number input for mobile money
- Summary and confirmation

**Available Plans** (from your test data):
- Featured 7 Days: 25,000 BIF
- Featured 15 Days: 45,000 BIF
- Featured 30 Days: 75,000 BIF
- Featured Premium: 150,000 BIF
- Real Estate Featured: 100,000 BIF (30 days)
- Vehicle Featured: 85,000 BIF (30 days)

### 3. Payment Flow

```
My Listings → Click Star → Select Plan → Enter Phone → Confirm
    ↓
Payment Initiated → Redirected to Verification Page
    ↓
Auto-verify after 3 seconds → Success/Failure
    ↓
Listing becomes featured (if successful)
```

### 4. Payment Verification Page

Route: `/payment/verify?ref={payment_ref}`

**Three States:**
1. **Pending**: Loading spinner, auto-verifies after 3 seconds
2. **Success**: ✅ Checkmark, success message, navigation options
3. **Failed**: ❌ Error message, retry button

### 5. Payment History

Route: `/payments/history`

Access from: **Profile page** → "Payment History" button

**Shows:**
- All past payments
- Status badges (successful, pending, failed, refunded)
- Plan details
- Amounts and dates
- Summary statistics

## Database Schema

### Listings Table
```sql
LISTING_STATUS: 'active' | 'pending' | 'sold' | 'expired' | 'hidden'
IS_FEATURED: boolean (default: false)
```

### Payments Table
```sql
PAYMENT_STATUS: 'pending' | 'successful' | 'failed' | 'refunded'
PAYMENT_METHOD: 'mobile_money' | 'card' | 'wallet'
```

## Testing Workflow

### Step 1: Create Test Pricing Plans

Run this in Django shell:

```python
from listings.models import PricingPlan
from decimal import Decimal

# Featured 7 Days
PricingPlan.objects.create(
    pricing_name="Featured 7 Days",
    pricing_description="Get your listing featured for 7 days",
    plan_price=Decimal("25000.00"),
    duration_days=7,
    category_scope="all",
    max_listings=1,
    max_images_per_listing=10,
    is_featured=True,
    is_active=True
)

# Add more plans as needed...
```

### Step 2: Create Test Listings

1. Login to your account
2. Go to "Create Listing" page
3. Fill out the form with images
4. Submit

### Step 3: Activate Listings

```bash
cd backend
python manage.py shell < fix_listing_status.py
```

### Step 4: Promote to Featured

1. Go to "My Listings" page
2. You should now see ⭐ star button on active listings
3. Click star → Select plan → Enter phone → Confirm
4. Follow payment flow

## Troubleshooting

### Star button still not showing?

**Check 1: Listing Status**
```python
from listings.models import Listing
for l in Listing.objects.all():
    print(f"{l.listing_title}: status={l.listing_status}, featured={l.is_featured}")
```

Expected: `status='active'`, `featured=False`

**Check 2: Frontend Console**
Open browser DevTools (F12) → Console tab
Look for errors related to API calls or rendering

**Check 3: Network Tab**
1. Open DevTools → Network tab
2. Refresh My Listings page
3. Find request to `/api/listings/my-listings/`
4. Check response data - should include `is_featured` and `listing_status`

**Check 4: Pricing Plans**
```python
from listings.models import PricingPlan
print(f"Featured plans: {PricingPlan.objects.filter(is_featured=True, is_active=True).count()}")
```

Should return > 0 (you need at least one featured pricing plan)

### Payment Modal is empty?

**Issue:** No pricing plans showing in modal

**Fix:** Create pricing plans with `is_featured=True` and `is_active=True`

### Payment always fails?

**Expected:** Payments are simulated in development

Backend randomly returns success (70%) or failure (30%) for testing purposes. In production, you'll integrate with real payment gateway (Lumicash, EcoCash, etc.)

## Backend API Endpoints

```
GET  /api/pricing-plans/              - List all active pricing plans
POST /api/payments/initiate/          - Initiate payment
POST /api/payments/verify/            - Verify payment status
GET  /api/payments/history/           - User's payment history
GET  /api/payments/{id}/              - Get specific payment
```

## Frontend Routes

```
/my-listings              - View user's listings (star button here)
/payment/verify           - Payment verification page
/payments/history         - Payment history dashboard
```

## Production Considerations

1. **Payment Gateway**: Replace simulated payment with real Lumicash/EcoCash integration
2. **Listing Approval**: Implement admin approval workflow for 'pending' → 'active'
3. **Featured Expiration**: Add cron job to expire featured listings after duration
4. **Payment Webhooks**: Implement webhook handlers for payment status updates
5. **Security**: Add payment amount verification, prevent replay attacks

## Files Modified

### Frontend
- `frontend/src/pages/MyListingsPage.tsx` - Added star button
- `frontend/src/components/payments/PaymentModal.tsx` - Payment modal
- `frontend/src/pages/PaymentVerifyPage.tsx` - Verification flow
- `frontend/src/pages/PaymentHistoryPage.tsx` - History dashboard
- `frontend/src/api/payments.ts` - Payment API client

### Backend
- `backend/listings/models.py` - Has `is_featured` field
- `backend/listings/serializers.py` - Returns `is_featured`
- `backend/listings/views.py` - `my_listings()` endpoint

### Database
- `LISTINGS` table has `IS_FEATURED` column (boolean)
- `PAYMENTS` table for payment records
- `PRICING_PLANS` table for plan definitions

## Summary

The star button shows only on **active** listings that are **not already featured**. Most likely, your listings are in 'pending' status. Run the fix script to activate them, and you'll see the star buttons appear!
