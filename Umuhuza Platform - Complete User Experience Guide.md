# 🧭 Umuhuza Platform - Complete User Experience Guide

**Version 1.0 | Last Updated: January 2025**

This comprehensive guide explains how users interact with the Umuhuza marketplace platform from their first visit to advanced features. It covers all user journeys, restricted features, and gated content.

---

## 📋 Table of Contents

1. [Platform Overview](#platform-overview)
2. [User Roles & Capabilities](#user-roles--capabilities)
3. [First-Time Visitor Experience](#first-time-visitor-experience)
4. [Account Creation & Verification](#account-creation--verification)
5. [Browsing & Searching](#browsing--searching)
6. [Viewing Listings](#viewing-listings)
7. [Creating Listings](#creating-listings)
8. [Communication System](#communication-system)
9. [Favorites & Saved Items](#favorites--saved-items)
10. [User Profiles](#user-profiles)
11. [Ratings & Reviews](#ratings--reviews)
12. [Payments & Pricing](#payments--pricing)
13. [Dealer Applications](#dealer-applications)
14. [Notifications](#notifications)
15. [Reports & Moderation](#reports--moderation)
16. [Gated Features Matrix](#gated-features-matrix)

---

## 1. Platform Overview

### What is Umuhuza?

Umuhuza is a peer-to-peer marketplace connecting buyers and sellers of real estate and vehicles in Burundi. The platform eliminates middlemen, allowing direct transactions between users.

### Core Value Propositions

- **No Middlemen**: Direct contact between buyers and sellers
- **Verified Users**: All users must verify email and phone
- **Trust & Safety**: Rating system, verified badges, and reporting
- **Fair Pricing**: Lower fees than traditional brokers (1-2% vs 5-10%)
- **Easy to Use**: Simple listing creation and search

### Platform Categories

1. **Real Estate**
   - Houses (sale/rent)
   - Apartments (sale/rent)
   - Land & Plots

2. **Vehicles**
   - Cars
   - Motorcycles
   - Commercial vehicles

---

## 2. User Roles & Capabilities

### 2.1 Anonymous Visitor (Not Logged In)

**Can Access:**
- ✅ Homepage
- ✅ Browse all active listings
- ✅ Search and filter listings
- ✅ View listing details
- ✅ View seller public profiles
- ✅ View categories
- ✅ Read about pages (About Us, How It Works, FAQ)

**Cannot Access:**
- ❌ Contact sellers (messaging)
- ❌ Save favorites
- ❌ Create listings
- ❌ Leave reviews
- ❌ View notifications
- ❌ Apply as dealer
- ❌ Make payments

**Call-to-Action**: Prompted to register/login when attempting restricted actions

---

### 2.2 Registered Buyer (Unverified)

**Status**: Email registered, account created, but not verified

**Can Access:**
- ✅ All visitor features
- ✅ Access to verification page
- ✅ Receive verification codes

**Cannot Access:**
- ❌ Contact sellers
- ❌ Create listings
- ❌ All other authenticated features

**Steps to take**: Must verify email AND phone to unlock full features

---

### 2.3 Verified Buyer

**Status**: Email and phone verified, full account access

**Can Access:**
- ✅ All visitor features
- ✅ Contact sellers via messaging
- ✅ Save listings to favorites
- ✅ Leave ratings and reviews
- ✅ Receive notifications
- ✅ Report listings/users
- ✅ View own profile and settings
- ✅ Switch to seller role

**Cannot Access:**
- ❌ Create listings (must switch to seller role first)
- ❌ Dealer-only features

**Badge**: ✓ Verified badge on profile

---

### 2.4 Verified Seller

**Status**: Verified user who has created at least one listing

**Can Access:**
- ✅ All buyer features
- ✅ Create listings (up to free tier limit)
- ✅ Edit/delete own listings
- ✅ Upload listing images
- ✅ Respond to buyer messages
- ✅ View listing analytics (views, favorites)
- ✅ Purchase pricing plans for featured listings
- ✅ Receive buyer inquiries

**Limitations:**
- 📊 Basic Plan: 1 free listing, 3 images, 30 days
- 📊 Must upgrade for more listings or features

**Badge**: ✓ Verified Seller (after 5+ listings and 4+ star rating)

---

### 2.5 Dealer

**Status**: Business user with approved dealer application

**Requirements to Apply:**
- ✅ Verified email and phone
- ✅ Business documentation uploaded
- ✅ Tax ID number
- ✅ Business license (optional but recommended)
- ✅ Admin approval

**Can Access:**
- ✅ All seller features
- ✅ Unlimited listings (with dealer subscription)
- ✅ Bulk listing upload
- ✅ Advanced analytics dashboard
- ✅ Business profile page
- ✅ Priority customer support
- ✅ Featured listing slots included

**Pricing:**
- 💰 Monthly subscription: 50,000 BIF
- 💰 Yearly subscription: 500,000 BIF (2 months free)

**Badge**: ⭐ Top Dealer badge

---

### 2.6 Administrator (Internal)

**Status**: Platform staff/admin (managed via Django admin panel)

**Can Access:**
- ✅ Django admin panel
- ✅ View all users and listings
- ✅ Approve/reject dealer applications
- ✅ Review reported content
- ✅ Ban/suspend users
- ✅ Moderate reviews
- ✅ View platform analytics
- ✅ Manage categories and pricing plans
- ✅ View payment history

**Not Public-Facing**: Admins do not have accounts on the public site

---

## 3. First-Time Visitor Experience

### 3.1 Landing on Homepage

**What Users See:**

1. **Hero Section**
   - Large headline: "Find Your Dream Property or Vehicle"
   - Search bar (can search without login)
   - Quick category buttons (Real Estate, Vehicles)

2. **Value Propositions**
   - "Verified Users" - Trust and safety
   - "Direct Contact" - No middlemen
   - "Easy Listing" - Post in minutes

3. **Statistics**
   - Active listings count
   - Verified users count
   - Daily visits
   - Deals closed

4. **Call-to-Action**
   - "Sign Up Free" button
   - "Browse Listings" button

5. **Navigation Bar**
   - Logo (home link)
   - "Browse Listings"
   - "Login" button
   - "Sign Up" button

**User Actions Available:**
- Click search to explore
- Browse categories
- Click "Sign Up" to register
- Click "Login" if returning user
- Scroll to learn more about platform

---

### 3.2 Browsing Without Account

**Flow:**
1. User clicks "Browse Listings" or searches from homepage
2. Redirected to `/listings` page
3. Can see all active listings in grid format
4. Can filter by:
   - Category
   - Price range
   - Location
   - Search keywords
   - Sort order

**Listing Cards Show:**
- Primary image
- Title
- Price (formatted in BIF)
- Location
- Views count
- Category tag
- Seller name
- Verified badge (if seller verified)

**Actions Available:**
- Click listing to view details
- Use filters and search
- Paginate through results

**Actions Restricted:**
- ❌ Heart icon shows but clicking prompts login
- ❌ Cannot contact seller

---

### 3.3 Viewing Listing Detail (No Login)

**Flow:**
1. User clicks on a listing card
2. Redirected to `/listings/{id}` page
3. Full listing details displayed

**What Users See:**

**Left Section (Main Content):**
- Image gallery with navigation arrows
- Thumbnail strip below main image
- Full title and description
- Price (large, prominent)
- Location with map pin icon
- View count
- Date posted
- Category badge
- Detailed description (formatted text)

**Right Section (Sidebar):**
- Action buttons (favorite, share, report)
- **"Contact Seller" button** (prompts login)
- Seller information card:
  - Profile photo/initial
  - Full name
  - Verified status
  - Role (buyer/seller/dealer)
  - Phone number (visible)
  - Email (visible)
- Safety tips card

**Bottom Section:**
- Similar listings (4 cards)

**User Actions:**
- Navigate through images
- Read full description
- See seller contact info
- Click "Contact Seller" → **Redirected to /login**
- Click favorite icon → **Redirected to /login**
- Click share → Can share (no login required)
- Click report → **Redirected to /login**
- View similar listings

**Key Insight**: Users can see EVERYTHING except they cannot initiate contact or save favorites without registering.

---

## 4. Account Creation & Verification

### 4.1 Registration Process

**Flow:**

**Step 1: Click "Sign Up"**
- Redirected to `/register`
- Registration form displayed

**Step 2: Fill Registration Form**

Required fields:
- First Name
- Last Name
- Email Address
- Phone Number (format: +25779XXXXXXX)
- Password (min 8 characters)
- Confirm Password
- Terms & Conditions checkbox (required)

**Validation:**
- Email must be unique and valid format
- Phone must match Burundi format (+257 + 8 digits)
- Passwords must match
- All fields required

**Step 3: Submit**
- Click "Create Account" button
- Backend creates user account
- User automatically logged in
- Generates verification codes:
  - 6-digit email code (valid 15 minutes)
  - 6-digit SMS code (valid 10 minutes)

**Step 4: Redirect to Verification**
- User redirected to `/verify`
- Codes displayed in terminal (dev mode) or sent via email/SMS (production)

---

### 4.2 Verification Process

**Two-Step Verification Required:**

**Email Verification:**
1. User receives 6-digit code via email
2. Enters code in "Email Verification" section
3. Clicks verify or submits form
4. Backend validates code
5. If valid: `email_verified = True`
6. If expired/invalid: Error message shown
7. "Resend code" option available

**Phone Verification:**
1. User receives 6-digit code via SMS
2. Enters code in "Phone Verification" section
3. Clicks verify or submits form
4. Backend validates code
5. If valid: `phone_verified = True`
6. If expired/invalid: Error message shown
7. "Resend code" option available

**Completion:**
- When BOTH verified: `is_verified = True`
- User receives "Verified" badge
- Notification: "Account fully verified! 🎉"
- Redirected to homepage
- Can now access all buyer features

**What If User Skips?**
- Can log out and come back
- On next login, if not verified → redirected to `/verify`
- Cannot access messaging until verified
- Can still browse and view listings

---

### 4.3 Login Process

**Flow:**

**Step 1: Click "Login"**
- Redirected to `/login`
- Login form displayed

**Step 2: Enter Credentials**
- Email address
- Password
- "Remember me" checkbox (optional)
- "Forgot password?" link

**Step 3: Submit**
- Click "Sign In" button
- Backend validates credentials
- If valid:
  - JWT tokens generated (access + refresh)
  - Tokens stored in localStorage
  - User state updated in Zustand store
  - `last_login` timestamp updated
  - Redirected to homepage or previous page

**Step 4: Check Verification Status**
- If `email_verified = False` OR `phone_verified = False`
  - Redirected to `/verify`
  - Must complete verification
- If fully verified
  - Full access granted

**Failed Login:**
- Error: "Invalid email or password"
- No indication which field is wrong (security)
- User can try again or reset password

**Account Deactivated:**
- Error: "Account is deactivated"
- Contact support message shown

---

### 4.4 Password Reset (Future Feature)

**Flow:**
1. Click "Forgot password?" on login page
2. Enter email address
3. Receive reset link via email
4. Click link → redirected to reset page
5. Enter new password (twice)
6. Submit → password updated
7. Redirected to login page

*Status: Backend structure ready, frontend pending*

---

## 5. Browsing & Searching

### 5.1 Listings Page (/listings)

**Layout:**
- Search bar with filters at top
- Filters button (mobile: collapsible)
- Result count displayed
- Listings grid (responsive: 1/2/3/4 columns)
- Pagination at bottom

**Search Functionality:**

**Quick Search:**
- Type keywords in search bar
- Press Enter or click Search button
- Searches in: title + description
- Real-time results

**Advanced Filters:**

Click "Filters" button to expand:

1. **Category Dropdown**
   - All Categories
   - Real Estate - Houses
   - Real Estate - Apartments
   - Real Estate - Land & Plots
   - Vehicles - Cars
   - Vehicles - Motorcycles

2. **Price Range**
   - Min Price (BIF)
   - Max Price (BIF)
   - Can enter specific amounts

3. **Location**
   - Text input
   - Searches partial matches
   - Examples: "Bujumbura", "Rohero", "Ngagara"

4. **Sort By**
   - Newest First (default)
   - Oldest First
   - Price: Low to High
   - Price: High to Low
   - Most Viewed

**Filter Application:**
- Click "Apply Filters" to search
- Click "Clear" to reset all filters
- Active filters shown with count badge
- URL updates with filter parameters

**Results Display:**
- Loading spinner while fetching
- Grid of listing cards
- 12 listings per page (default)
- Pagination controls if >12 results

**Empty State:**
- "No listings found"
- Suggestion to adjust filters
- "Clear Filters" button

---

### 5.2 Category Pages

**Future Enhancement:**
- Dedicated pages for each category
- `/listings/real-estate` or `/categories/houses`
- Pre-filtered results
- Category-specific features

*Currently: All categories browsed from main listings page with filters*

---

### 5.3 Search Best Practices (User Tips)

**For Buyers:**
1. Start broad, then narrow
2. Use location filters effectively
3. Sort by newest to see fresh listings
4. Save searches (future feature)
5. Set price alerts (future feature)

**Common Search Patterns:**
- "House Bujumbura" + price filter
- "Toyota" + vehicles category
- "Land" + location + price range
- Featured listings first (sort option)

---

## 6. Viewing Listings

### 6.1 Listing Detail Page Anatomy

**URL Structure:** `/listings/{id}`

**Page Sections:**

**1. Image Gallery (Top Left)**
- Main large image (16:9 ratio, 600px height)
- Navigation arrows (left/right)
- Image counter (e.g., "3 / 8")
- Thumbnail strip below (5 visible)
- Click thumbnail to jump to image
- Featured badge (if applicable)
- Zoom capability (future)

**2. Listing Information (Below Gallery)**
- **Title**: Large, bold (H1)
- **Metadata Row**:
  - Location with pin icon
  - View count with eye icon
  - Date posted (formatted)
- **Price**: Extra large, primary color
- **Category**: Badge/pill style
- **Description**: 
  - "Description" heading
  - Full text, preserves line breaks
  - Can be long-form content

**3. Action Buttons (Top Right Sidebar)**
- **Favorite**: Heart icon
  - Filled red if favorited
  - Outline if not
  - Click to toggle
  - Shows login prompt if not authenticated
  
- **Share**: Share icon
  - Opens native share dialog if available
  - Otherwise copies link to clipboard
  - Toast notification: "Link copied!"
  
- **Report**: Flag icon
  - Opens report modal
  - Requires login

**4. Primary CTA (Sidebar)**
- Large **"Contact Seller"** button
  - If not logged in → redirects to `/login`
  - If logged in → opens chat or redirects to messages
  - If own listing → shows "Edit Listing" instead

**5. Seller Information Card (Sidebar)**
- Profile picture (or initial circle)
- Full name (clickable to user profile)
- Verified badge if applicable
- User role (buyer/seller/dealer)
- Contact details:
  - Phone number (clickable tel: link)
  - Email (clickable mailto: link)
- Member since date

**6. Safety Tips Card (Sidebar)**
- Yellow background
- Important reminders:
  - Meet in public place
  - Check item before payment
  - Don't pay in advance
  - Report suspicious listings

**7. Similar Listings (Bottom)**
- "Similar Listings" heading
- 4 listing cards in a row
- Based on same category + similar price
- Links to other listing detail pages

**User Actions Available:**
- Navigate images
- Read description
- View seller profile (click name)
- Call seller (click phone)
- Email seller (click email)
- Contact via messaging (button)
- Add to favorites
- Share listing
- Report listing
- View similar listings
- Navigate back to search results

---

### 6.2 View Counter

**How It Works:**
- Each page visit increments view count
- Same user visiting again = new view (no deduplication yet)
- Owner's views don't count
- Anonymous views counted
- Displayed on listing card and detail page

**Purpose:**
- Social proof for sellers
- Popularity indicator for buyers
- Analytics for platform

---

## 7. Creating Listings

### 7.1 Eligibility & Access

**Requirements to Create Listing:**
- ✅ Must be logged in
- ✅ Email verified
- ✅ Phone verified
- ✅ Can be buyer or seller role

**Access Point:**
- Click "Post Listing" in header
- Or navigate to `/listings/create`

**Role Automatic Upgrade:**
- If user is "buyer" and creates first listing
- Role automatically changes to "seller"
- No manual role selection needed

---

### 7.2 Create Listing Flow

**Step 1: Access Form**
- Click "Post Listing" in navigation
- Redirected to `/listings/create`
- Multi-step form displayed

**Step 2: Basic Information**

Form fields:
1. **Category** (dropdown, required)
   - Select from available categories
   - Determines listing type

2. **Title** (text, required)
   - Max 255 characters
   - Clear, descriptive
   - Example: "Modern 3-Bedroom House in Rohero"

3. **Description** (textarea, required)
   - Multi-line text
   - Min 50 characters recommended
   - Supports line breaks
   - Example structure:
     ```
     Beautiful house features:
     - 3 bedrooms
     - 2 bathrooms
     - Modern kitchen
     
     Located in quiet neighborhood...
     ```

4. **Price** (number, required)
   - In Burundian Francs (BIF)
   - Positive number only
   - Example: 75000000

5. **Location** (text, required)
   - City, neighborhood
   - Example: "Bujumbura, Rohero"
   - Format: "City, Area" recommended

**Step 3: Image Upload**

- **Upload Area**: Drag-and-drop or click to browse
- **Limits**:
  - Basic plan: 3 images max
  - Premium plans: Up to 10 images
- **Supported Formats**: JPG, JPEG, PNG, WebP
- **Max Size**: 5MB per image
- **Processing**:
  - Auto-resize to max 1920px width
  - Compressed to 85% quality
  - Converted to JPEG
  - Maintains aspect ratio

**Image Management:**
- First image = primary (by default)
- Drag to reorder (future feature)
- Click X to remove
- Preview before upload

**Step 4: Review & Submit**

Preview shows:
- All entered information
- Uploaded images
- How listing will appear

Actions:
- **"Go Back"** - Edit information
- **"Submit Listing"** - Create listing

**Step 5: Processing**

After submit:
1. Form data sent to backend
2. Images uploaded to server/S3
3. Listing created with status = "pending"
4. Admin notification sent (for review)
5. User redirected to success page or listing detail

**Success Message:**
- "Listing created successfully!"
- "Your listing is pending approval"
- Link to view listing
- Link to create another listing

---

### 7.3 Listing Status Flow

**Pending** (initial status)
- Just created by user
- Under review by admin
- Not visible in public search
- Visible to owner in "My Listings"
- Message: "Your listing is being reviewed"

**Active** (approved)
- Admin approved or auto-approved
- Visible in public search
- Can receive views and messages
- Counts toward user's active listings

**Sold** (manually set by owner)
- User marks as sold
- No longer in search results
- Visible in seller's history
- Badge: "SOLD" on listing card

**Expired** (automatic)
- Listing duration exceeded (30/60/90 days based on plan)
- Removed from active search
- Owner notified
- Can be renewed with payment

**Hidden** (by owner)
- Temporarily hidden from search
- Owner can unhide anytime
- Useful for "not ready to sell yet"

---

### 7.4 Managing Listings

**My Listings Dashboard** (`/my-listings`)

View of all own listings:
- Tabs: All, Active, Pending, Sold, Expired
- Grid or list view
- Search own listings
- Sort by date, views, status

**Each Listing Shows:**
- Thumbnail image
- Title
- Price
- Status badge
- Views count
- Created date
- Actions: Edit, Delete, Mark as Sold

**Edit Listing:**
- Click "Edit" button
- Redirected to `/listings/{id}/edit`
- Same form as create, pre-filled
- Can update: title, description, price, location
- Can add/remove images
- Can change status
- Save changes

**Delete Listing:**
- Click "Delete" button
- Confirmation modal: "Are you sure?"
- If confirmed → listing permanently deleted
- All images removed
- Associated messages remain (for history)

**Mark as Sold:**
- Click "Mark as Sold" button
- Status changes to "sold"
- Removed from active search
- Badge added to listing

---

## 8. Communication System

### 8.1 Messaging Overview

**Purpose**: Allow buyers and sellers to communicate about listings

**Access**: Protected - requires login and verification

**Architecture**: HTTP-based messaging (not real-time WebSocket yet)

---

### 8.2 Starting a Conversation

**Buyer Initiates:**

**Flow:**
1. Buyer views listing detail page
2. Clicks "Contact Seller" button
3. If not logged in → redirected to login
4. If logged in:
   - Backend creates or retrieves existing chat
   - Buyer redirected to `/messages?listing={id}`
   - Chat interface opens with seller

**Chat Creation Logic:**
- One chat per listing per buyer-seller pair
- If chat exists → open existing
- If new → create new chat record
- Seller = listing owner
- Buyer = current logged-in user

**Seller Receives:**
- Notification: "New message about your listing"
- Chat appears in their messages inbox

---

### 8.3 Messages Page (/messages)

**Layout:**

**Left Sidebar (30%):**
- List of all conversations
- Each chat shows:
  - Other user's name and photo
  - Listing thumbnail and title
  - Last message preview
  - Timestamp of last message
  - Unread badge (count)
- Sorted by most recent activity
- Click to open conversation

**Right Panel (70%):**
- Selected conversation thread
- Header shows:
  - Other user's name
  - Listing title (clickable link)
  - Online status (future)
- Message history (scrollable)
- Each message shows:
  - Sender's name/initial
  - Message content
  - Timestamp
  - Read status (checkmarks)
- Input box at bottom
- Send button

**Mobile View:**
- Chat list full screen
- Clicking chat opens conversation full screen
- Back button to return to list

---

### 8.4 Sending Messages

**Composing:**
1. Type message in input box
2. Press Enter or click Send button
3. Message sent to backend
4. Appears in conversation immediately (optimistic UI)
5. Marked as "sending" until confirmed
6. Other user's chat updates
7. `last_message_at` timestamp updated

**Message Types:**
- **Text** (current): Plain text messages
- **Images** (future): Share photos
- **Files** (future): Share documents

**Character Limits:**
- No strict limit
- Recommended: Keep messages concise
- Very long messages may be truncated in preview

**Restrictions:**
- Cannot message yourself
- Cannot message on inactive listings
- Cannot message banned users

---

### 8.5 Message Notifications

**When You Receive a Message:**

**In-App:**
- Red badge on "Messages" in navigation (unread count)
- Browser notification (if permitted)
- Sound alert (future)

**Email Notification:**
- If user enables email notifications
- Summary: "You have a new message about [listing]"
- CTA: "View Message" button

**SMS Notification** (future premium feature):
- For urgent messages
- Opt-in only

**Push Notifications** (future mobile app):
- Real-time alerts
- Actionable: Reply directly from notification

---

### 8.6 Read Receipts

**How It Works:**
- When user opens a chat, all unread messages marked as read
- `is_read` flag set to True
- `read_at` timestamp recorded
- Sender sees checkmarks change from gray (sent) to blue (read)

**Display:**
- Single checkmark = sent
- Double checkmarks = delivered
- Blue checkmarks = read

---

### 8.7 Chat Management

**Archive Chat:**
- Click menu → Archive
- Chat hidden from main list
- Can access in "Archived" folder
- Messages preserved

**Delete Chat:**
- Click menu → Delete
- Confirmation required
- Chat permanently removed for you
- Other user retains their copy

**Block User** (future):
- Prevents further messages
- Hides existing conversation
- User notified they're blocked

**Report User:**
- If receiving spam or abuse
- Opens report form
- Admin reviews
- May result in user ban

---

## 9. Favorites & Saved Items

### 9.1 Adding to Favorites

**Purpose**: Save listings for later viewing

**How To:**
1. Click heart icon on listing card or detail page
2. If not logged in → prompted to login
3. If logged in → listing added to favorites
4. Heart icon fills with red color
5. Toast notification: "Added to favorites"

**Removing from Favorites:**
1. Click heart icon again
2. Heart outline restored
3. Listing removed from favorites
4. Toast: "Removed from favorites"

**Where Heart Icons Appear:**
- Listing cards in grid
- Listing detail page (top right)
- My favorites page

---

### 9.2 Favorites Page (/favorites)

**Access**: Protected - requires login

**Layout:**
- Grid of favorited listings
- Same format as main listings page
- Shows all saved items
- Most recently added first

**Each Listing Shows:**
- Full listing card (same as browse view)
- Date added to favorites
- Current listing status
- Quick remove button

**Actions:**
- Click listing → view details
- Click heart → remove from favorites
- Share listing
- Contact seller

**Empty State:**
- "No favorites yet"
- Suggestion: "Browse listings to save your favorites"
- "Browse Listings" CTA button

**Management:**
- No folders/categories (yet)
- No bulk actions (yet)
- Simple list of favorited items

---

### 9.3 Favorite Notifications (Future)

**Price Drop Alert:**
- If favorited listing price decreases
- Email: "Price dropped on your saved listing!"

**Status Change:**
- If listing sold
- Notification: "A listing you saved was sold"

**New Similar Listings:**
- Based on favorite patterns
- Weekly digest: "New listings you might like"

---

## 10. User Profiles

### 10.1 Public Profile View

**URL**: `/users/{userid}`

**What Anyone Can See:**
- Profile photo or initial
- Full name
- User role (buyer/seller/dealer)
- Verified badge (if verified)
- Member since date
- Location (if provided)
- Bio (if provided)
- Badges earned (verified, trusted seller, etc.)

**Seller-Specific:**
- Active listings count
- Total listings count
- Average rating (stars)
- Reviews count
- Link to view all listings by this seller

**Dealer-Specific:**
- Business name
- Business description
- Contact information
- Active listings
- Business hours (future)

**Cannot See:**
- Email address (unless on listing detail)
- Phone number (unless on listing detail)
- Personal settings
- Messages
- Favorites
- Payment history

**Actions Available:**
- View seller's active listings
- Read reviews
- Send message (requires login)
- Report user (requires login)

---

### 10.2 Own Profile (/profile)

**Access**: Protected - must be logged in

**View:**
- All public information (as others see it)
- Private information:
  - Email
  - Phone number
  - Account settings
  - Privacy preferences
  - Notification settings

**Profile Sections:**

**1. Profile Information**
- Edit name
- Upload/change profile photo
- Add bio (about me)
- Add location
- Social media links (future)

**2. Account Settings**
- Change password
- Email preferences
- SMS preferences
- Language preference (future)
- Currency preference (future)

**3. Privacy Settings**
- Show phone on listings (yes/no)
- Show email on listings (yes/no)
- Profile visibility (public/private)
- Activity status (online/offline)

**4. Notification Preferences**
- Email notifications (on/off)
- Message notifications (on/off)
- Listing updates (on/off)
- Marketing emails (on/off)
- SMS notifications (on/off, premium)

**5. Account Statistics**
- Total listings created
- Active listings
- Total views
- Messages sent/received
- Deals completed
- Account age

**6. Verification Status**
- Email verification status (✓ or ✗)
- Phone verification status (✓ or ✗)
- ID verification status (future)
- Badges earned

**7. Actions**
- Edit profile
- Change password
- Delete account (with confirmation)
- Download data (GDPR compliance)
- Contact support

---

### 10.3 Profile Badges

**System of Achievement Badges:**

**Verified** 
- ✓ Green checkmark
- Earned: Email + phone verified
- Shows: User is authenticated

**Trusted Seller**
- ⭐ Gold star
- Earned: 5+ listings, 4+ average rating
- Valid: 1 year, renewable
- Shows: Reliable seller

**Top Dealer**
- 💼 Briefcase icon
- Earned: Dealer status + 10+ active listings
- Valid: While dealer subscription active
- Shows: Professional business

**Power Buyer**
- 🔥 Fire icon
- Earned: 10+ purchases/deals completed
- Valid: Lifetime
- Shows: Active buyer

---

### 10.4 Editing Profile

**Update Information:**
1. Click "Edit Profile" button
2. Form opens with current info pre-filled
3. Change fields:
   - First name
   - Last name
   - Phone number (must verify if changed)
   - Bio
   - Location
4. Upload new profile photo:
   - Click photo area
   - Select image (JPG, PNG)
   - Max 2MB
   - Auto-crops to square
   - Compressed and saved
5. Click "Save Changes"
6. Success message shown
7. Profile updated

**Change Password:**
1. Navigate to "Security" section
2. Enter current password
3. Enter new password
4. Confirm new password
5. Submit
6. Password updated
7. All sessions except current logged out
8. Email notification sent

**Delete Account:**
1. Click "Delete Account" in settings
2. Warning modal appears
3. Must enter password to confirm
4. Confirmation: "Are you sure? This cannot be undone."
5. If confirmed:
   - Account deactivated
   - Listings hidden
   - Messages preserved (anonymized)
   - Can reactivate within 30 days
   - After 30 days: permanently deleted

---

## 11. Ratings & Reviews

### 11.1 Leaving a Review

**Requirements:**
- Must be logged in and verified
- Must have had interaction with reviewed user
- Can review after completing a deal
- One review per transaction

**Flow:**
1. After successful transaction, option to review appears
2. Click "Leave Review" button
3. Review form opens:
   - Star rating (1-5, required)
   - Written comment (optional, 500 char max)
   - Transaction reference (auto-filled)
4. Submit review
5. Review visible on seller's profile
6. Buyer notified

**What Can Be Reviewed:**
- Seller communication
- Item accuracy
- Transaction smoothness
- Would recommend (yes/no)

**Edit Review:**
- Can edit within 48 hours
- After that, review locked
- Contact support to remove

---

### 11.2 Receiving Reviews

**Notification:**
- Email: "You received a new review!"
- In-app notification
- Link to view review

**Display:**
- Reviews shown on public profile
- Most recent first
- Average rating calculated
- Star rating visible
- Comment visible (unless hidden by admin)

**Respond to Review:**
- Seller can respond once per review
- Response shown below review
- Limited to 300 characters
- Professional tone required

**Report Review:**
- If review is abusive or fake
- Click "Report" on review
- Admin investigates
- May be removed if violates rules

---

### 11.3 Trust Score System

**Calculated Based On:**
- Average rating (weighted 40%)
- Number of reviews (weighted 20%)
- Verification status (weighted 20%)
- Account age (weighted 10%)
- Response time (weighted 10%)

**Display:**
- Overall score: 1-5 stars
- Breakdown available on profile
- Badge thresholds:
  - 4.5+ stars = Trusted Seller badge
  - 4.0-4.4 = No special badge
  - Below 4.0 = Warning indicator

**Impact:**
- Higher scores rank better in search
- Featured on "Top Sellers" page
- More buyer trust
- Eligibility for dealer status

---

## 12. Payments & Pricing

### 12.1 Free Tier (Basic Plan)

**What's Included:**
- ✅ Create account (free forever)
- ✅ Browse unlimited listings
- ✅ Message sellers
- ✅ 1 free listing per month
- ✅ 30 days listing duration
- ✅ 3 images per listing
- ✅ Basic support

**Limitations:**
- ❌ No featured placement
- ❌ Cannot create multiple active listings
- ❌ Standard support (24-48hr response)

**Target Audience:** Individual sellers, occasional users

---

### 12.2 Premium Plans

**Premium Plan** (10,000 BIF)
- ✅ 1 featured listing
- ✅ 60 days duration
- ✅ 10 images
- ✅ Priority placement in search
- ✅ Featured badge
- ✅ Analytics dashboard
- ✅ Priority support

**Purpose:** Boost single important listing

---

**Dealer Monthly** (50,000 BIF/month)
- ✅ Unlimited listings
- ✅ All listings featured
- ✅ 10 images per listing
- ✅ Advanced analytics
- ✅ Bulk upload
- ✅ Business profile page
- ✅ Priority support
- ✅ Top Dealer badge

**Purpose:** Professional businesses, agencies

---

**Dealer Yearly** (500,000 BIF/year)
- ✅ All monthly features
- ✅ 2 months free
- ✅ Annual discount (17% off)
- ✅ Dedicated account manager
- ✅ Custom branding (future)

**Purpose:** Committed businesses

---

### 12.3 Payment Process

**Selecting a Plan:**
1. Navigate to "Pricing" page
2. View all plans comparison
3. Click "Upgrade" on desired plan
4. If not logged in → prompted to login

**Payment Flow:**
1. Plan selection confirmed
2. Redirected to payment page
3. Choose payment method:
   - Mobile Money (Lumicash, Ecocash)
   - Credit/Debit Card
   - Wallet balance (future)

**Mobile Money (Primary):**
1. Select "Mobile Money"
2. Enter phone number
3. Click "Pay Now"
4. Backend initiates payment with Lumicash/Ecocash
5. User receives USSD push on phone
6. Enter PIN to approve
7. Payment confirmed
8. Webhook updates platform
9. Benefits applied immediately

**Card Payment:**
1. Select "Card"
2. Enter card details
3. 3D Secure verification
4. Payment processed
5. Confirmation sent

**Payment Confirmation:**
- Email receipt sent
- In-app notification
- Transaction ID provided
- Invoice available (PDF)

**Payment History:**
- View all transactions in `/payments/history`
- Download invoices
- See plan expiry dates

---

### 12.4 Applying Plan Benefits

**After Successful Payment:**

**For Featured Listings:**
1. User selects which listing to feature
2. Listing status: `is_featured = True`
3. Listing duration extended
4. Featured badge appears
5. Listing boosted in search results

**For Dealer Subscriptions:**
1. User role upgraded to "dealer"
2. All current listings featured
3. Unlimited listing creation enabled
4. Analytics dashboard unlocked
5. Top Dealer badge awarded

**Expiration:**
- Email reminder 7 days before expiry
- Email reminder 1 day before expiry
- After expiry:
  - Featured status removed
  - Listings return to regular status
  - Still visible, just not featured

**Renewal:**
- Auto-renewal option available
- Manual renewal via Pricing page
- Grace period: 3 days

---

## 13. Dealer Applications

### 13.1 Eligibility

**Requirements to Apply:**
- ✅ Verified email and phone
- ✅ Active account in good standing
- ✅ No policy violations
- ✅ Business documentation available

**Who Should Apply:**
- Real estate agencies
- Car dealerships
- Property developers
- Vehicle importers
- Professional brokers

---

### 13.2 Application Process

**Step 1: Start Application**
- Navigate to "Become a Dealer"
- Click "Apply Now"
- Application form opens

**Step 2: Business Information**

Required fields:
- Business name
- Business type (real estate / vehicle / both)
- Business address (physical location)
- Business phone number
- Business email
- Tax ID number (NIF)
- Business license number (if available)

**Step 3: Document Upload**

Required documents:
1. Business license (photo/scan)
2. Tax certificate (NIF document)
3. ID of business owner
4. Proof of address (optional)

Supported formats:
- PDF, JPG, PNG
- Max 5MB per file

**Step 4: Review & Submit**
- Preview application
- Confirm accuracy
- Accept dealer terms
- Submit

**Step 5: Confirmation**
- Success message displayed
- Application ID provided
- Estimated review time: 3-5 business days
- Email confirmation sent

---

### 13.3 Application Review

**Admin Review Process:**
1. Admin notified of new application
2. Reviews business information
3. Verifies documents
4. Checks business legitimacy
5. Makes decision:
   - **Approved**: Dealer status granted
   - **Rejected**: Reason provided
   - **More Info Needed**: Requests clarification

**If Approved:**
- Email notification sent
- Account upgraded to dealer
- Subscription payment required
- Access to dealer features unlocked

**If Rejected:**
- Email with rejection reason
- Opportunity to re-apply
- Can appeal decision

**If More Info Needed:**
- Email specifying requirements
- User can respond with additional info
- Application re-reviewed

---

### 13.4 Application Status Tracking

**Check Status:**
- Navigate to "Dealer Application Status"
- Shows current state:
  - Submitted
  - Under Review
  - Approved
  - Rejected
  - Pending Documents

**Updates:**
- Email updates at each stage
- In-app notifications
- Admin notes visible (if any)

---

## 14. Notifications

### 14.1 Notification Types

**System Notifications:**
- Account verified
- Welcome message
- Policy updates
- Maintenance alerts

**Chat Notifications:**
- New message received
- User replied to your message
- Chat archived

**Listing Notifications:**
- Listing approved
- Listing expired
- Listing featured
- Someone favorited your listing (future)

**Payment Notifications:**
- Payment successful
- Payment failed
- Subscription expiring
- Invoice available

**Review Notifications:**
- New review received
- Someone responded to your review

**Report Notifications:**
- Your report submitted
- Your report reviewed
- Action taken on report

**Verification Notifications:**
- Verification code sent
- Account fully verified
- Additional verification required

---

### 14.2 Notification Center (/notifications)

**Access**: Protected - requires login

**Layout:**
- List of all notifications
- Tabs: Unread (default), All
- Most recent first
- Unread count badge in navigation

**Each Notification Shows:**
- Icon (based on type)
- Title
- Message preview
- Timestamp (relative: "2 hours ago")
- Unread indicator (blue dot)
- Action button (if applicable)

**Actions:**
- Click notification → marks as read + follows link
- Mark as read (without opening)
- Mark all as read
- Delete notification
- Clear all read

**Empty State:**
- "No notifications"
- Encouragement: "We'll notify you of important updates"

---

### 14.3 Notification Settings

**Configure in Profile:**

**Email Notifications:**
- All notifications (on/off)
- Messages only
- Listings updates only
- Payments only
- Marketing emails (on/off)

**Browser Notifications:**
- Enable/disable in browser
- Requires permission

**Mobile Push** (future):
- All notifications
- Important only
- Off

**Frequency:**
- Real-time
- Daily digest
- Weekly summary

---

## 15. Reports & Moderation

### 15.1 Reporting Content

**What Can Be Reported:**
- Listings (spam, fraud, inappropriate)
- Users (harassment, fake account)
- Messages (abuse, spam)
- Reviews (fake, offensive)

**How to Report:**

**Listing Report:**
1. Click "Report" flag icon on listing
2. Report form opens:
   - Select reason:
     * Spam
     * Fraud/Scam
     * Inappropriate content
     * Duplicate listing
     * Other
   - Provide detailed explanation (required)
   - Optional: Upload evidence (screenshots)
3. Submit report
4. Confirmation message
5. Report ID provided

**User Report:**
1. Visit user profile
2. Click "Report User"
3. Same form as listing report
4. Additional fields:
   - Specific interaction reference
   - Severity level
5. Submit

---

### 15.2 After Reporting

**Immediate Actions:**
- Report logged in system
- Report ID assigned
- Confirmation email sent
- Status: "Pending Review"

**Admin Review:**
- Admin receives notification
- Reviews report details
- Investigates reported content/user
- Views evidence
- Checks violation history
- Makes decision

**Possible Outcomes:**

**Warning:**
- User warned
- Content remains
- User notified of violation

**Content Removal:**
- Listing removed/hidden
- User notified
- Refund issued if applicable

**User Suspension:**
- Temporary account suspension (7-30 days)
- Cannot login
- All listings hidden
- Can appeal

**User Ban:**
- Permanent account termination
- All content removed
- IP blocked
- Cannot register new account

**No Action:**
- Report reviewed but no violation found
- Reporter notified
- No consequences

---

### 15.3 Report Status Tracking

**Check Status:**
- Navigate to "My Reports" in profile
- See all submitted reports
- Status indicators:
  - Pending (orange)
  - Under Review (blue)
  - Resolved (green)
  - Rejected (red)

**Updates:**
- Email when status changes
- In-app notification
- Admin notes visible

**Resolution Details:**
- Action taken (if any)
- Reason for decision
- Thank you for reporting (if helpful)

---

### 15.4 Community Guidelines

**Zero Tolerance Policies:**
- Fraud or scams
- Illegal items/services
- Hate speech
- Harassment
- Child exploitation
- Violence threats

**Prohibited Listings:**
- Stolen items
- Counterfeit goods
- Weapons
- Drugs or illegal substances
- Adult content
- Services violating law

**Expected Behavior:**
- Respectful communication
- Accurate descriptions
- Fair pricing
- Honoring commitments
- Prompt responses

**Consequences:**
- 1st violation: Warning
- 2nd violation: Suspension
- 3rd violation: Permanent ban
- Severe violations: Immediate ban

---

## 16. Gated Features Matrix

### 16.1 Complete Access Control Table

| Feature | Anonymous | Registered (Unverified) | Verified Buyer | Verified Seller | Dealer | Admin |
|---------|-----------|------------------------|----------------|-----------------|--------|-------|
| **Browse Listings** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Search & Filter** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **View Listing Detail** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **View User Profiles** | ✅ (public only) | ✅ (public only) | ✅ (public only) | ✅ (public only) | ✅ (public only) | ✅ (all) |
| **Register Account** | ✅ | N/A | N/A | N/A | N/A | N/A |
| **Login** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Email Verification** | ❌ | ✅ | ✅ (completed) | ✅ (completed) | ✅ (completed) | N/A |
| **Phone Verification** | ❌ | ✅ | ✅ (completed) | ✅ (completed) | ✅ (completed) | N/A |
| **Contact Sellers** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Messaging** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Save Favorites** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **View Favorites** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Create Listings** | ❌ | ❌ | ❌ | ✅ (1 free) | ✅ (unlimited) | ✅ |
| **Edit Own Listings** | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Delete Own Listings** | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Upload Images** | ❌ | ❌ | ❌ | ✅ (3 max) | ✅ (10 max) | ✅ |
| **Feature Listings** | ❌ | ❌ | ❌ | ✅ (paid) | ✅ (included) | ✅ |
| **View Analytics** | ❌ | ❌ | ❌ | ✅ (basic) | ✅ (advanced) | ✅ |
| **Leave Reviews** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Respond to Reviews** | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Report Content** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Submit Dealer Application** | ❌ | ❌ | ✅ | ✅ | N/A | N/A |
| **Make Payments** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **View Payment History** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Bulk Upload** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Business Profile** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **View All Users** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Approve Listings** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Review Reports** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Ban Users** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Approve Dealers** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **View Analytics Dashboard** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

### 16.2 Feature Progression Path

**Visitor → Registered → Verified → Seller → Dealer**

**Path 1: Casual Buyer**
1. Browse as visitor
2. Find interesting listing
3. Try to contact → prompted to register
4. Register account
5. Verify email & phone
6. Can now message, save favorites
7. Complete purchase
8. Leave review

**Path 2: Individual Seller**
1. Browse as visitor
2. Decide to sell item
3. Click "Post Listing" → prompted to register
4. Register & verify
5. Create first listing (free)
6. Respond to buyer messages
7. Complete sale
8. Upgrade to premium for more listings

**Path 3: Professional Dealer**
1. Register as individual
2. Verify account
3. Create a few test listings
4. Apply for dealer status
5. Submit business documents
6. Get approved
7. Subscribe to dealer plan
8. Unlimited featured listings

---

## 17. Mobile Experience

### 17.1 Responsive Design

**Breakpoints:**
- Mobile: <640px
- Tablet: 640px - 1024px
- Desktop: >1024px

**Mobile Optimizations:**
- Touch-friendly buttons (min 44x44px)
- Collapsible navigation menu
- Single-column layouts
- Larger form inputs
- Swipe gestures for image galleries
- Bottom navigation (future)

---

### 17.2 Progressive Web App (PWA) Features (Future)

- Install as app
- Offline browsing of cached listings
- Push notifications
- App-like navigation
- Fast loading

---

## 18. Support & Help

### 18.1 Help Center

**Access**: `/help` or `/faq`

**Categories:**
- Getting Started
- Buying Guide
- Selling Guide
- Payments & Pricing
- Safety Tips
- Account Management
- Technical Support

**Format:**
- Searchable knowledge base
- Common questions
- Step-by-step guides
- Video tutorials (future)

---

### 18.2 Contact Support

**Methods:**
- Email: support@umuhuza.com
- Contact form on website
- Phone: +257 79 123 456 (business hours)
- Live chat (future)

**Response Time:**
- Free users: 24-48 hours
- Premium/Dealers: 12-24 hours
- Urgent issues: 4-6 hours

---

## 19. Terms & Policies

### 19.1 User Agreement

**Key Points:**
- Platform is a facilitator, not a party to transactions
- Users responsible for their own due diligence
- Platform not liable for deals gone wrong
- Users must be 18+ years old
- Accurate information required

### 19.2 Privacy Policy

**Data Collection:**
- Personal info (name, email, phone)
- Usage data (browsing, searches)
- Device info (IP, browser)
- Cookies for authentication

**Data Usage:**
- Provide and improve service
- Communication with users
- Security and fraud prevention
- Analytics (anonymized)

**Data Sharing:**
- Never sold to third parties
- Shared with service providers (email, SMS, payments)
- Law enforcement if required

**User Rights:**
- Access your data
- Correct inaccurate data
- Delete account and data
- Export data (GDPR)

### 19.3 Prohibited Activities

- Fraud or scams
- Misrepresentation
- Spamming
- Harassment
- Illegal items
- Price manipulation
- Multiple accounts for abuse
- Circumventing fees

---

## 20. Future Features Roadmap

### Coming Soon (Q2 2025)
- Map-based search
- Saved searches with alerts
- Real-time messaging (WebSocket)
- Mobile app (iOS & Android)

### Planned (Q3-Q4 2025)
- Virtual property tours (360°)
- Video uploads
- Mortgage calculator
- Property comparison tool
- Multi-language (Kirundi, French)

### Long-term Vision
- AI-powered recommendations
- Blockchain property records
- Escrow payment system
- Integration with banks
- Franchise opportunities

---

**END OF USER EXPERIENCE GUIDE**

*For technical specifications, see TECHNICAL_SPECS.md*  
*For testing procedures, see TESTING_GUIDE.md*  
*For monetization details, see MONETIZATION_MODEL.md*