# 🧪 Umuhuza Platform - Testing & Quality Assurance Guide

**Version 1.0 | Last Updated: January 2025**

This comprehensive testing guide ensures every feature of the Umuhuza marketplace platform functions correctly. It includes manual test cases, automated test strategies, and quality assurance procedures.

---

## 📋 Table of Contents

1. [Testing Philosophy](#testing-philosophy)
2. [Testing Environment Setup](#testing-environment-setup)
3. [Manual Testing Checklist](#manual-testing-checklist)
4. [Automated Testing Strategy](#automated-testing-strategy)
5. [Feature-by-Feature Test Cases](#feature-by-feature-test-cases)
6. [Performance Testing](#performance-testing)
7. [Security Testing](#security-testing)
8. [Browser & Device Testing](#browser--device-testing)
9. [Bug Reporting Process](#bug-reporting-process)
10. [Test Data & Fixtures](#test-data--fixtures)

---

## 1. Testing Philosophy

### 1.1 Testing Pyramid

```
        /\
       /  \        E2E Tests (10%)
      /____\       - Critical user flows
     /      \      
    /________\     Integration Tests (30%)
   /          \    - API endpoints
  /____________\   - Database operations
 /              \  
/________________\ Unit Tests (60%)
                   - Functions, components
                   - Business logic
```

### 1.2 Testing Principles

- **Test Early, Test Often**: Write tests alongside features
- **Test User Behavior**: Focus on what users do, not implementation
- **Automate Repetitive Tests**: Manual testing for exploratory only
- **Test in Production-Like Environment**: Use staging server
- **Document Failures**: Every bug should have a test case

### 1.3 Quality Gates

**Before Deployment:**
- ✅ All automated tests pass
- ✅ Manual smoke tests completed
- ✅ No critical/high bugs
- ✅ Performance benchmarks met
- ✅ Security scan passed

---

## 2. Testing Environment Setup

### 2.1 Test Environments

| Environment | Purpose | URL | Database |
|-------------|---------|-----|----------|
| **Local** | Development | localhost:5173 | Local MySQL |
| **Staging** | Pre-production testing | staging.umuhuza.bi | Staging DB |
| **Production** | Live site | umuhuza.bi | Production DB |

### 2.2 Test User Accounts

Create the following test accounts in staging:

| Role | Email | Password | Purpose |
|------|-------|----------|---------|
| Visitor | - | - | Unregistered browsing |
| Basic User | test.user@example.com | Test123! | Basic functionality |
| Verified User | verified.user@example.com | Test123! | Verified features |
| Premium User | premium.user@example.com | Test123! | Premium features |
| Dealer | dealer.test@example.com | Test123! | Dealer features |
| Admin | admin.test@example.com | Test123! | Admin panel |

### 2.3 Test Data Setup

**SQL Script to Create Test Data:**
```sql
-- Create test categories
INSERT INTO categories (name, slug, parent_category_id) VALUES
('Real Estate', 'real-estate', NULL),
('Land', 'land', 1),
('Houses', 'houses', 1),
('Vehicles', 'vehicles', NULL),
('Cars', 'cars', 4);

-- Create test listings
INSERT INTO listings (user_id, category_id, title, description, price, location, status) VALUES
(2, 3, 'Beautiful 3BR House in Rohero', 'Spacious house with garden', 150000000, 'Rohero', 'active'),
(2, 5, 'Toyota Camry 2020', 'Well maintained sedan', 35000000, 'Bujumbura', 'active'),
(3, 2, 'Prime Land in Kabondo', '500sqm residential land', 25000000, 'Kabondo', 'active');
```

### 2.4 Testing Tools

**Backend Testing:**
- **Jest**: Unit tests
- **Supertest**: API integration tests
- **Artillery**: Load testing

**Frontend Testing:**
- **Vitest**: Unit tests
- **React Testing Library**: Component tests
- **Cypress**: E2E tests

**Manual Testing:**
- **Browser DevTools**: Network, console inspection
- **Postman**: API testing
- **Lighthouse**: Performance audits

---

## 3. Manual Testing Checklist

### 3.1 Pre-Release Smoke Test (30 minutes)

Execute these critical tests before every deployment:

**✅ Homepage**
- [ ] Page loads without errors
- [ ] Search bar is functional
- [ ] Categories display correctly
- [ ] Featured listings appear
- [ ] Footer links work

**✅ User Authentication**
- [ ] Can register new account
- [ ] Verification email sent
- [ ] Can log in with correct credentials
- [ ] Cannot log in with wrong password
- [ ] Logout works properly

**✅ Listing Creation**
- [ ] Create listing form loads
- [ ] Can upload images (test 1, 5, 10 images)
- [ ] Form validation works
- [ ] Listing appears after creation
- [ ] Can edit own listing
- [ ] Can delete own listing

**✅ Messaging**
- [ ] Can send message to seller
- [ ] Message appears in conversation
- [ ] Unread count updates
- [ ] Can receive reply
- [ ] Message notifications work

**✅ Search & Browse**
- [ ] Can search by keyword
- [ ] Can filter by category
- [ ] Can filter by price range
- [ ] Can sort results
- [ ] Pagination works

**✅ Payments** (if implemented)
- [ ] Can initiate payment
- [ ] Payment gateway redirects correctly
- [ ] Featured listing activates after payment

---

## 4. Automated Testing Strategy

### 4.1 Backend Unit Tests

**File: `backend/tests/unit/auth.test.js`**
```javascript
const { hashPassword, comparePassword } = require('../../utils/auth');

describe('Authentication Utils', () => {
  test('should hash password correctly', async () => {
    const password = 'SecurePass123!';
    const hashed = await hashPassword(password);
    expect(hashed).not.toBe(password);
    expect(hashed.length).toBeGreaterThan(50);
  });

  test('should verify correct password', async () => {
    const password = 'SecurePass123!';
    const hashed = await hashPassword(password);
    const isValid = await comparePassword(password, hashed);
    expect(isValid).toBe(true);
  });

  test('should reject incorrect password', async () => {
    const password = 'SecurePass123!';
    const hashed = await hashPassword(password);
    const isValid = await comparePassword('WrongPassword', hashed);
    expect(isValid).toBe(false);
  });
});
```

**Run Tests:**
```bash
cd backend
npm test
```

### 4.2 Backend Integration Tests

**File: `backend/tests/integration/listings.test.js`**
```javascript
const request = require('supertest');
const app = require('../../server');

describe('Listings API', () => {
  let authToken;

  beforeAll(async () => {
    // Login to get token
    const response = await request(app)
      .post('/api/auth/login')
      .send({
        email: 'test@example.com',
        password: 'Test123!'
      });
    authToken = response.body.token;
  });

  test('GET /api/listings should return listings', async () => {
    const response = await request(app)
      .get('/api/listings')
      .expect(200);

    expect(response.body.listings).toBeInstanceOf(Array);
    expect(response.body.pagination).toBeDefined();
  });

  test('GET /api/listings/:id should return single listing', async () => {
    const response = await request(app)
      .get('/api/listings/1')
      .expect(200);

    expect(response.body.listing_id).toBe(1);
    expect(response.body.title).toBeDefined();
  });

  test('POST /api/listings should create listing with auth', async () => {
    const newListing = {
      category_id: 2,
      title: 'Test Listing',
      description: 'This is a test listing',
      price: 100000,
      location: 'Test Location'
    };

    const response = await request(app)
      .post('/api/listings')
      .set('Authorization', `Bearer ${authToken}`)
      .send(newListing)
      .expect(201);

    expect(response.body.listing_id).toBeDefined();
  });

  test('POST /api/listings should fail without auth', async () => {
    const newListing = {
      category_id: 2,
      title: 'Test Listing',
      price: 100000
    };

    await request(app)
      .post('/api/listings')
      .send(newListing)
      .expect(401);
  });

  test('GET /api/listings should support filtering', async () => {
    const response = await request(app)
      .get('/api/listings')
      .query({
        category_id: 2,
        min_price: 50000,
        max_price: 200000
      })
      .expect(200);

    expect(response.body.listings).toBeInstanceOf(Array);
  });
});
```

### 4.3 Frontend Component Tests

**File: `frontend/src/components/__tests__/ListingCard.test.tsx`**
```typescript
import { render, screen } from '@testing-library/react';
import { ListingCard } from '../ListingCard';

const mockListing = {
  listing_id: 1,
  title: 'Beautiful House',
  price: 150000000,
  location: 'Rohero',
  images: [{ image_url: '/test.jpg', is_primary: true }],
  created_at: '2025-01-15T10:00:00Z'
};

describe('ListingCard', () => {
  test('renders listing title', () => {
    render(<ListingCard listing={mockListing} />);
    expect(screen.getByText('Beautiful House')).toBeInTheDocument();
  });

  test('displays formatted price', () => {
    render(<ListingCard listing={mockListing} />);
    expect(screen.getByText(/150,000,000 BIF/)).toBeInTheDocument();
  });

  test('shows location', () => {
    render(<ListingCard listing={mockListing} />);
    expect(screen.getByText('Rohero')).toBeInTheDocument();
  });

  test('renders primary image', () => {
    render(<ListingCard listing={mockListing} />);
    const image = screen.getByRole('img');
    expect(image).toHaveAttribute('src', expect.stringContaining('test.jpg'));
  });
});
```

### 4.4 E2E Tests with Cypress

**File: `cypress/e2e/user-flow.cy.js`**
```javascript
describe('Complete User Flow', () => {
  
  it('should allow visitor to browse and register', () => {
    // Visit homepage
    cy.visit('/');
    cy.contains('Find Your Perfect Property').should('be.visible');

    // Search for listings
    cy.get('input[placeholder*="Search"]').type('house');
    cy.get('button[type="submit"]').click();
    
    // View results
    cy.url().should('include', '/listings');
    cy.get('[data-testid="listing-card"]').should('have.length.at.least', 1);

    // Click on a listing
    cy.get('[data-testid="listing-card"]').first().click();
    cy.url().should('include', '/listings/');

    // Try to contact seller (should redirect to login)
    cy.contains('Contact Seller').click();
    cy.url().should('include', '/login');

    // Register new account
    cy.contains('Sign Up').click();
    cy.url().should('include', '/register');
    
    cy.get('input[name="full_name"]').type('Test User');
    cy.get('input[name="email"]').type(`test${Date.now()}@example.com`);
    cy.get('input[name="phone"]').type('+25779123456');
    cy.get('input[name="password"]').type('Test123!');
    cy.get('button[type="submit"]').click();

    // Should redirect to verification page
    cy.contains('Verify Your Email').should('be.visible');
  });

  it('should allow verified user to create listing', () => {
    // Login
    cy.visit('/login');
    cy.get('input[name="email"]').type('verified.user@example.com');
    cy.get('input[name="password"]').type('Test123!');
    cy.get('button[type="submit"]').click();

    // Navigate to create listing
    cy.contains('Post Listing').click();
    cy.url().should('include', '/create-listing');

    // Fill form
    cy.get('select[name="category_id"]').select('Houses');
    cy.get('input[name="title"]').type('Test Listing from Cypress');
    cy.get('textarea[name="description"]').type('This is a test listing created by automated test');
    cy.get('input[name="price"]').type('100000000');
    cy.get('input[name="location"]').type('Bujumbura');

    // Upload image
    cy.get('input[type="file"]').attachFile('test-house.jpg');

    // Submit
    cy.get('button[type="submit"]').click();

    // Should redirect to listing detail
    cy.contains('Test Listing from Cypress').should('be.visible');
  });

  it('should allow messaging between users', () => {
    // Login as buyer
    cy.visit('/login');
    cy.get('input[name="email"]').type('test.user@example.com');
    cy.get('input[name="password"]').type('Test123!');
    cy.get('button[type="submit"]').click();

    // Find a listing
    cy.visit('/listings/1');
    
    // Contact seller
    cy.contains('Contact Seller').click();
    cy.get('textarea').type('Hi, is this still available?');
    cy.contains('Send Message').click();

    // Should see message in conversation
    cy.contains('Hi, is this still available?').should('be.visible');

    // Logout and login as seller
    cy.contains('Logout').click();
    cy.visit('/login');
    cy.get('input[name="email"]').type('verified.user@example.com');
    cy.get('input[name="password"]').type('Test123!');
    cy.get('button[type="submit"]').click();

    // Check messages
    cy.contains('Messages').click();
    cy.get('[data-testid="unread-badge"]').should('contain', '1');
    
    // Reply
    cy.get('[data-testid="conversation"]').first().click();
    cy.contains('Hi, is this still available?').should('be.visible');
    cy.get('textarea').type('Yes, it is! Would you like to schedule a viewing?');
    cy.contains('Send').click();
  });
});
```

**Run E2E Tests:**
```bash
npx cypress open  # Interactive mode
npx cypress run   # Headless mode
```

---

## 5. Feature-by-Feature Test Cases

### 5.1 User Registration

| Test Case ID | Description | Steps | Expected Result | Priority |
|-------------|-------------|-------|-----------------|----------|
| REG-001 | Register with valid data | 1. Go to /register<br>2. Fill all fields correctly<br>3. Submit | Account created, verification email sent | High |
| REG-002 | Register with existing email | 1. Use email already in DB<br>2. Submit | Error: "Email already registered" | High |
| REG-003 | Register with invalid email | 1. Enter "notanemail"<br>2. Submit | Error: "Invalid email format" | Medium |
| REG-004 | Register with weak password | 1. Enter password "123"<br>2. Submit | Error: "Password must be at least 8 characters" | Medium |
| REG-005 | Register with invalid phone | 1. Enter phone "12345"<br>2. Submit | Error: "Invalid phone format" | Medium |
| REG-006 | Leave required fields empty | 1. Submit empty form | Validation errors shown | High |
| REG-007 | Password visibility toggle | 1. Click eye icon | Password shown/hidden | Low |

**Test Data:**
```json
{
  "valid": {
    "full_name": "Jean Dupont",
    "email": "jean.test@example.com",
    "phone": "+25779123456",
    "password": "SecurePass123!"
  },
  "invalid_email": {
    "email": "notanemail"
  },
  "weak_password": {
    "password": "123"
  }
}
```

### 5.2 User Login

| Test Case ID | Description | Steps | Expected Result | Priority |
|-------------|-------------|-------|-----------------|----------|
| LOGIN-001 | Login with correct credentials | 1. Enter valid email/password<br>2. Submit | Logged in, redirected to homepage | High |
| LOGIN-002 | Login with wrong password | 1. Enter valid email, wrong password<br>2. Submit | Error: "Invalid credentials" | High |
| LOGIN-003 | Login with non-existent email | 1. Enter email not in DB<br>2. Submit | Error: "Invalid credentials" | High |
| LOGIN-004 | Login with unverified email | 1. Login before verifying<br>2. Submit | Warning: "Please verify your email" | High |
| LOGIN-005 | "Remember me" functionality | 1. Check "Remember me"<br>2. Login<br>3. Close browser<br>4. Return | Still logged in | Medium |
| LOGIN-006 | Logout | 1. Click Logout | Logged out, redirected to homepage | High |

### 5.3 Email Verification

| Test Case ID | Description | Steps | Expected Result | Priority |
|-------------|-------------|-------|-----------------|----------|
| VERIFY-001 | Verify with valid token | 1. Click email link<br>2. Submit token | Email verified, can access features | High |
| VERIFY-002 | Verify with expired token | 1. Use token > 24hrs old<br>2. Submit | Error: "Token expired", option to resend | Medium |
| VERIFY-003 | Verify with invalid token | 1. Use random token<br>2. Submit | Error: "Invalid token" | Medium |
| VERIFY-004 | Resend verification email | 1. Click "Resend"<br>2. Check email | New verification email received | Medium |
| VERIFY-005 | Verify already verified account | 1. Use valid token twice | Message: "Already verified" | Low |

### 5.4 Listing Creation

| Test Case ID | Description | Steps | Expected Result | Priority |
|-------------|-------------|-------|-----------------|----------|
| LIST-001 | Create listing with all fields | 1. Fill complete form<br>2. Upload 5 images<br>3. Submit | Listing created successfully | High |
| LIST-002 | Create listing with minimum fields | 1. Fill only required fields<br>2. Upload 1 image<br>3. Submit | Listing created | High |
| LIST-003 | Create listing without images | 1. Fill form, no images<br>2. Submit | Error: "At least 1 image required" | High |
| LIST-004 | Upload 11 images | 1. Try to upload 11 images | Error: "Maximum 10 images" | Medium |
| LIST-005 | Upload invalid file type | 1. Try to upload .txt file | Error: "Only images allowed" | Medium |
| LIST-006 | Upload oversized image | 1. Upload image > 5MB | Error: "File too large" | Medium |
| LIST-007 | Create listing as unverified user | 1. Login unverified<br>2. Try to create listing | Redirected to verification page | High |
| LIST-008 | Exceed free listing limit | 1. Create 4th listing as free user | Error: "Upgrade to create more" | High |
| LIST-009 | Special characters in title | 1. Use é, à, ç in title<br>2. Submit | Listing created with correct characters | Medium |
| LIST-010 | Price validation | 1. Enter negative price<br>2. Submit | Error: "Price must be positive" | High |

**Test Data:**
```json
{
  "valid_listing": {
    "category_id": 3,
    "title": "Beautiful 3BR House in Rohero",
    "description": "Spacious house with modern amenities, 3 bedrooms, 2 bathrooms, large garden",
    "price": 150000000,
    "location": "Rohero, Bujumbura",
    "listing_type": "sale",
    "bedrooms": 3,
    "bathrooms": 2,
    "square_meters": 200
  },
  "minimum_listing": {
    "category_id": 5,
    "title": "Toyota Camry 2020",
    "description": "Well maintained sedan, single owner",
    "price": 35000000,
    "location": "Bujumbura"
  }
}
```

### 5.5 Listing Viewing & Details

| Test Case ID | Description | Steps | Expected Result | Priority |
|-------------|-------------|-------|-----------------|----------|
| VIEW-001 | View listing detail page | 1. Click on listing card | Detail page loads with all info | High |
| VIEW-002 | View listing images | 1. Open detail page<br>2. Click images | Gallery modal opens, can navigate | High |
| VIEW-003 | View count increments | 1. View listing<br>2. Check count<br>3. Refresh<br>4. Check again | Count increased by 1 | Medium |
| VIEW-004 | Share listing | 1. Click share button | Share modal with social options | Low |
| VIEW-005 | Print listing | 1. Click print | Print-friendly version | Low |
| VIEW-006 | View similar listings | 1. Scroll to bottom | Similar listings displayed | Medium |
| VIEW-007 | View seller profile from listing | 1. Click seller name | Seller profile page loads | Medium |
| VIEW-008 | View listing when inactive | 1. Access inactive listing URL | 404 or "Listing no longer available" | High |

### 5.6 Listing Search & Filters

| Test Case ID | Description | Steps | Expected Result | Priority |
|-------------|-------------|-------|-----------------|----------|
| SEARCH-001 | Search by keyword | 1. Enter "house"<br>2. Submit | Results contain "house" in title/description | High |
| SEARCH-002 | Filter by category | 1. Select "Cars"<br>2. Apply | Only car listings shown | High |
| SEARCH-003 | Filter by price range | 1. Set min: 50M, max: 100M<br>2. Apply | Listings within range | High |
| SEARCH-004 | Filter by location | 1. Select "Rohero"<br>2. Apply | Only Rohero listings | High |
| SEARCH-005 | Combined filters | 1. Category + Price + Location<br>2. Apply | Listings match all filters | High |
| SEARCH-006 | Sort by price (low to high) | 1. Select sort option | Listings ordered by price ascending | Medium |
| SEARCH-007 | Sort by date (newest first) | 1. Select sort option | Newest listings first | Medium |
| SEARCH-008 | Search with no results | 1. Search "xyzabc123"<br>2. Submit | "No listings found" message | Medium |
| SEARCH-009 | Clear all filters | 1. Apply filters<br>2. Click "Clear All" | All filters reset | Medium |
| SEARCH-010 | Pagination | 1. Go to page 2<br>2. Check results | Different listings shown | High |

### 5.7 Messaging System

| Test Case ID | Description | Steps | Expected Result | Priority |
|-------------|-------------|-------|-----------------|----------|
| MSG-001 | Send first message to seller | 1. Click "Contact Seller"<br>2. Type message<br>3. Send | Conversation created, message sent | High |
| MSG-002 | Reply to message | 1. Open conversation<br>2. Type reply<br>3. Send | Reply appears in conversation | High |
| MSG-003 | Unread message badge | 1. Receive new message<br>2. Check badge | Badge shows "1" | High |
| MSG-004 | Mark message as read | 1. Open conversation with unread | Badge count decreases | High |
| MSG-005 | Empty message | 1. Try to send empty message | Error or button disabled | Medium |
| MSG-006 | Very long message | 1. Type 10,000 characters<br>2. Send | Error: "Message too long" | Medium |
| MSG-007 | Multiple conversations | 1. Message 3 different sellers | 3 separate conversations created | High |
| MSG-008 | Delete conversation | 1. Click delete<br>2. Confirm | Conversation removed from list | Low |
| MSG-009 | Search conversations | 1. Type in search<br>2. Enter | Filtered conversations shown | Low |
| MSG-010 | Real-time message receipt | 1. Send from User A<br>2. Check User B's messages (open) | Message appears immediately | High |

### 5.8 Favorites

| Test Case ID | Description | Steps | Expected Result | Priority |
|-------------|-------------|-------|-----------------|----------|
| FAV-001 | Add listing to favorites | 1. Click heart icon<br>2. Check | Icon filled, added to favorites | High |
| FAV-002 | Remove from favorites | 1. Click filled heart<br>2. Check | Icon unfilled, removed | High |
| FAV-003 | View favorites page | 1. Go to /favorites | All saved listings displayed | High |
| FAV-004 | Favorite as visitor | 1. Try to favorite<br>2. Not logged in | Redirected to login | High |
| FAV-005 | Empty favorites page | 1. No favorites<br>2. Visit page | "No favorites yet" message | Low |
| FAV-006 | Favorite deleted listing | 1. Listing deleted<br>2. Check favorites | Listing removed from favorites | Medium |

### 5.9 User Profile

| Test Case ID | Description | Steps | Expected Result | Priority |
|-------------|-------------|-------|-----------------|----------|
| PROF-001 | View own profile | 1. Click profile icon | Profile page loads with info | High |
| PROF-002 | Edit profile | 1. Click "Edit Profile"<br>2. Change name<br>3. Save | Changes saved successfully | High |
| PROF-003 | Upload profile picture | 1. Choose file<br>2. Upload | Picture displayed in header | Medium |
| PROF-004 | Update bio | 1. Edit bio<br>2. Save | Bio updated on profile | Medium |
| PROF-005 | Change password | 1. Enter old + new password<br>2. Submit | Password changed, can login with new | High |
| PROF-006 | View public profile | 1. Click seller name<br>2. View profile | Public info shown (no email/phone) | High |
| PROF-007 | View user's listings | 1. On profile page<br>2. Check listings tab | User's active listings shown | High |
| PROF-008 | View user's reviews | 1. On profile page<br>2. Check reviews tab | Received reviews shown | Medium |

### 5.10 Reviews & Ratings

| Test Case ID | Description | Steps | Expected Result | Priority |
|-------------|-------------|-------|-----------------|----------|
| REV-001 | Leave review | 1. After transaction<br>2. Rate 5 stars<br>3. Write comment<br>4. Submit | Review saved and visible | High |
| REV-002 | Review without transaction | 1. Try to review random user | Error: "No transaction found" | High |
| REV-003 | Duplicate review | 1. Try to review same listing twice | Error: "Already reviewed" | Medium |
| REV-004 | Review self | 1. Try to review own listing | Error: "Cannot review yourself" | Medium |
| REV-005 | View user rating | 1. Check seller profile | Average rating and count shown | High |
| REV-006 | Edit review | 1. Edit existing review<br>2. Save | Review updated | Medium |
| REV-007 | Delete review | 1. Delete review<br>2. Confirm | Review removed | Low |

### 5.11 Payments & Subscriptions

| Test Case ID | Description | Steps | Expected Result | Priority |
|-------------|-------------|-------|-----------------|----------|
| PAY-001 | Upgrade to premium | 1. Click "Upgrade"<br>2. Select plan<br>3. Complete payment | Account upgraded | High |
| PAY-002 | Purchase featured listing | 1. Select listing<br>2. Choose duration<br>3. Pay | Listing featured | High |
| PAY-003 | Payment failure | 1. Use declined card<br>2. Try to pay | Error message, no charge | High |
| PAY-004 | Payment success | 1. Complete payment<br>2. Check status | Transaction recorded, feature activated | High |
| PAY-005 | View payment history | 1. Go to settings<br>2. Check payments | All transactions listed | Medium |
| PAY-006 | Auto-renewal | 1. Subscription expires<br>2. Auto-renew enabled | Automatically renewed | Medium |
| PAY-007 | Cancel subscription | 1. Click "Cancel"<br>2. Confirm | Subscription cancelled, expires at end of period | Medium |

### 5.12 Dealer Applications

| Test Case ID | Description | Steps | Expected Result | Priority |
|-------------|-------------|-------|-----------------|----------|
| DEAL-001 | Submit dealer application | 1. Fill form<br>2. Upload docs<br>3. Submit | Application submitted, status "pending" | High |
| DEAL-002 | Incomplete application | 1. Leave required fields empty<br>2. Submit | Error: validation failures | High |
| DEAL-003 | Check application status | 1. Go to applications page | Current status shown | High |
| DEAL-004 | Approve application (admin) | 1. Admin reviews<br>2. Approve | User upgraded to dealer | High |
| DEAL-005 | Reject application (admin) | 1. Admin reviews<br>2. Reject with note | User notified, can reapply | Medium |
| DEAL-006 | Reapply after rejection | 1. Submit new application | New application created | Medium |

### 5.13 Admin Panel

| Test Case ID | Description | Steps | Expected Result | Priority |
|-------------|-------------|-------|-----------------|----------|
| ADM-001 | Access admin panel | 1. Login as admin<br>2. Navigate to /admin | Admin dashboard loads | High |
| ADM-002 | View all listings | 1. Go to listings management | All listings with filters | High |
| ADM-003 | Moderate listing | 1. Review flagged listing<br>2. Approve/reject | Status updated | High |
| ADM-004 | View reports | 1. Go to reports section | Pending reports listed | High |
| ADM-005 | Ban user | 1. Select user<br>2. Ban with reason | User account suspended | High |
| ADM-006 | View statistics | 1. Check dashboard | Accurate metrics shown | Medium |

### 5.14 Notifications

| Test Case ID | Description | Steps | Expected Result | Priority |
|-------------|-------------|-------|-----------------|----------|
| NOT-001 | Receive email notification | 1. New message sent<br>2. Check email | Email notification received | High |
| NOT-002 | Receive SMS notification | 1. Important event<br>2. Check phone | SMS received | Medium |
| NOT-003 | In-app notification | 1. Event occurs<br>2. Check notification bell | Notification badge shown | High |
| NOT-004 | Mark notification as read | 1. Click notification | Badge count decreases | Medium |
| NOT-005 | Notification preferences | 1. Go to settings<br>2. Toggle email/SMS | Preferences saved | Medium |

---

## 6. Performance Testing

### 6.1 Page Load Times

**Using Lighthouse in Chrome DevTools:**

| Page | Target Load Time | Acceptable | Actions if Slow |
|------|------------------|------------|-----------------|
| Homepage | < 2s | < 3s | Optimize images, reduce JS |
| Listings page | < 2.5s | < 4s | Implement pagination, lazy loading |
| Listing detail | < 2s | < 3s | Compress images, cache data |
| Dashboard | < 2s | < 3s | Optimize queries |

**Test Command:**
```bash
lighthouse https://umuhuza.bi --view
```

### 6.2 API Response Times

**Using Artillery:**

Create `load-test.yml`:
```yaml
config:
  target: "https://api.umuhuza.bi"
  phases:
    - duration: 60
      arrivalRate: 10
      name: "Warm up"
    - duration: 120
      arrivalRate: 50
      name: "Sustained load"
  
scenarios:
  - name: "Get listings"
    flow:
      - get:
          url: "/api/listings"
      - think: 2
      - get:
          url: "/api/listings/1"
```

**Run Load Test:**
```bash
artillery run load-test.yml
```

**Performance Targets:**
- **p95 response time**: < 500ms
- **p99 response time**: < 1000ms
- **Error rate**: < 1%

### 6.3 Database Performance

**Slow Query Monitoring:**
```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1; -- 1 second

-- Check slow queries
SELECT * FROM mysql.slow_log ORDER BY query_time DESC LIMIT 10;
```

**Index Usage Check:**
```sql
-- Listings query should use indexes
EXPLAIN SELECT * FROM listings 
WHERE category_id = 2 
AND price BETWEEN 50000000 AND 100000000 
AND status = 'active';
```

---

## 7. Security Testing

### 7.1 Authentication Security

| Test | Description | How to Test | Expected |
|------|-------------|-------------|----------|
| **SQL Injection** | Try SQL in login form | Email: `' OR '1'='1` | Rejected, no login |
| **XSS** | Try script in bio | Bio: `<script>alert('XSS')</script>` | Escaped, not executed |
| **CSRF** | Submit form without token | Use Postman without CSRF token | 403 Forbidden |
| **Brute Force** | Multiple failed logins | Try 20 wrong passwords | Account locked/rate limited |
| **JWT Expiry** | Use expired token | Wait 25 hours, make request | 401 Unauthorized |
| **Password Strength** | Try weak passwords | Password: "123" | Rejected with error |

### 7.2 File Upload Security

| Test | Description | Expected |
|------|-------------|----------|
| **Malicious file upload** | Upload .exe file | Rejected: "Invalid file type" |
| **Oversized file** | Upload 20MB image | Rejected: "File too large" |
| **Script in filename** | Upload `<script>.jpg` | Filename sanitized |
| **Path traversal** | Filename: `../../etc/passwd.jpg` | Path sanitized |

### 7.3 Authorization Testing

| Test | Description | Expected |
|------|-------------|----------|
| **Access other user's listing** | Edit listing_id=1 as user_id=2 | 403 Forbidden |
| **Admin endpoints as regular user** | GET /api/admin/reports | 403 Forbidden |
| **Unverified user creates listing** | Try without email verification | Rejected |

### 7.4 Security Scan

**Using OWASP ZAP:**
```bash
# Run automated security scan
zap-cli quick-scan https://umuhuza.bi
```

**Check for:**
- SSL/TLS configuration
- Security headers (CSP, X-Frame-Options)
- Known vulnerabilities
- Exposed sensitive data

---

## 8. Browser & Device Testing

### 8.1 Browser Compatibility

**Desktop Browsers:**
| Browser | Version | Priority | Status |
|---------|---------|----------|--------|
| Chrome | Latest | High | ✅ |
| Firefox | Latest | High | ✅ |
| Safari | Latest | Medium | ⚠️ Test on Mac |
| Edge | Latest | Medium | ✅ |
| IE11 | - | Low | ❌ Not supported |

**Mobile Browsers:**
| Browser | Platform | Priority | Status |
|---------|----------|----------|--------|
| Chrome | Android | High | ✅ |
| Safari | iOS | High | ⚠️ Test on iPhone |
| Samsung Internet | Android | Medium | ✅ |

### 8.2 Responsive Design Testing

**Test Viewports:**
- **Mobile**: 375x667 (iPhone SE)
- **Tablet**: 768x1024 (iPad)
- **Desktop**: 1920x1080 (HD)

**Using Chrome DevTools:**
1. Open DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Test each viewport

**Check:**
- [ ] Navigation menu collapses on mobile
- [ ] Images scale properly
- [ ] Forms are usable on mobile
- [ ] No horizontal scrolling
- [ ] Touch targets are 44x44px minimum

### 8.3 Device Testing

**Physical Device Testing (Recommended):**
- iPhone 12/13/14
- Samsung Galaxy S21/S22
- iPad Air
- Low-end Android (< 2GB RAM)

**Cloud Testing Services:**
- BrowserStack
- LambdaTest
- Sauce Labs

---

## 9. Bug Reporting Process

### 9.1 Bug Report Template

```markdown
**Bug ID**: BUG-001
**Title**: Cannot upload more than 3 images on mobile
**Priority**: High
**Severity**: Major
**Environment**: Staging, iOS Safari 16.0
**Reported By**: Test Team
**Date**: 2025-01-20

**Description**:
When creating a listing on iPhone Safari, the file upload 
only allows selecting up to 3 images, even though the limit is 10.

**Steps to Reproduce**:
1. Open Safari on iPhone
2. Go to /create-listing
3. Click "Upload Images"
4. Try to select 5 images
5. Only 3 are selected

**Expected Result**:
Should allow selecting up to 10 images

**Actual Result**:
Only 3 images can be selected

**Screenshots**:
[Attach screenshot]

**Additional Info**:
- Works fine on Chrome Android
- Works fine on desktop Safari
```

### 9.2 Bug Priority Levels

| Priority | Description | Response Time | Example |
|----------|-------------|---------------|---------|
| **Critical** | System down, no workaround | < 4 hours | Site completely inaccessible |
| **High** | Major feature broken | < 24 hours | Cannot create listings |
| **Medium** | Feature partially broken | < 3 days | Search filters not working |
| **Low** | Minor issue, cosmetic | < 7 days | Typo in footer |

### 9.3 Bug Tracking

**Use GitHub Issues or Trello:**

**GitHub Labels:**
- `bug` - Confirmed bug
- `enhancement` - Feature request
- `documentation` - Docs issue
- `high-priority` - Urgent
- `needs-testing` - Fix needs verification

---

## 10. Test Data & Fixtures

### 10.1 SQL Test Data Script

**File: `test-data.sql`**
```sql
-- Reset database
DROP DATABASE IF EXISTS umuhuza_test;
CREATE DATABASE umuhuza_test;
USE umuhuza_test;

-- Create tables (same as production schema)
-- ... (all CREATE TABLE statements)

-- Insert test categories
INSERT INTO categories (name, slug, parent_category_id) VALUES
('Real Estate', 'real-estate', NULL),
('Land', 'land', 1),
('Houses', 'houses', 1),
('Apartments', 'apartments', 1),
('Vehicles', 'vehicles', NULL),
('Cars', 'cars', 5),
('Motorcycles', 'motorcycles', 5);

-- Insert test users
INSERT INTO users (full_name, email, phone, password_hash, user_type, email_verified) VALUES
('Test User', 'test@example.com', '+25779100001', '$2b$10$hashedpassword', 'individual', TRUE),
('Verified User', 'verified@example.com', '+25779100002', '$2b$10$hashedpassword', 'individual', TRUE),
('Premium User', 'premium@example.com', '+25779100003', '$2b$10$hashedpassword', 'individual', TRUE),
('Dealer User', 'dealer@example.com', '+25779100004', '$2b$10$hashedpassword', 'dealer', TRUE),
('Admin User', 'admin@example.com', '+25779100005', '$2b$10$hashedpassword', 'individual', TRUE);

-- Insert test listings
INSERT INTO listings (user_id, category_id, title, description, price, location, status) VALUES
(2, 3, 'Beautiful 3BR House in Rohero', 'Spacious house with modern amenities', 150000000, 'Rohero', 'active'),
(2, 6, 'Toyota Camry 2020', 'Well maintained sedan', 35000000, 'Bujumbura', 'active'),
(3, 2, 'Prime Land in Kabondo', '500sqm residential land', 25000000, 'Kabondo', 'active'),
(4, 4, 'Luxury Apartment Downtown', '2BR apartment with city view', 80000000, 'Centre Ville', 'active');

-- Add more test data...
```

### 10.2 Automated Test Fixtures

**File: `backend/tests/fixtures/users.js`**
```javascript
module.exports = {
  testUsers: [
    {
      full_name: "Test User",
      email: "test@example.com",
      phone: "+25779100001",
      password: "Test123!",
      user_type: "individual"
    },
    {
      full_name: "Premium User",
      email: "premium@example.com",
      phone: "+25779100003",
      password: "Test123!",
      user_type: "individual"
    }
  ],
  testListings: [
    {
      category_id: 3,
      title: "Test House",
      description: "Test description",
      price: 100000000,
      location: "Test Location"
    }
  ]
};
```

---

## 11. Continuous Testing

### 11.1 Pre-Commit Checks

**Git Hook: `.git/hooks/pre-commit`**
```bash
#!/bin/sh
# Run linter
npm run lint || exit 1

# Run unit tests
npm test || exit 1

echo "✅ All pre-commit checks passed"
```

### 11.2 CI/CD Pipeline

**GitHub Actions: `.github/workflows/test.yml`**
```yaml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm install
      
      - name: Run unit tests
        run: npm test
      
      - name: Run E2E tests
        run: npm run test:e2e
      
      - name: Run security scan
        run: npm audit
```

---

## 12. Testing Checklist

### 12.1 Pre-Deployment Checklist

**Before deploying to production:**

**Functionality:**
- [ ] All critical paths tested manually
- [ ] All automated tests passing
- [ ] No console errors in browser
- [ ] All API endpoints responding correctly

**Performance:**
- [ ] Lighthouse score > 80
- [ ] Page load times < 3s
- [ ] API response times < 500ms
- [ ] No memory leaks

**Security:**
- [ ] No critical vulnerabilities (npm audit)
- [ ] SSL certificate valid
- [ ] Environment variables secured
- [ ] Rate limiting configured

**UX:**
- [ ] Tested on mobile devices
- [ ] Tested on 3+ browsers
- [ ] Forms validated correctly
- [ ] Error messages clear

**Data:**
- [ ] Database backup created
- [ ] Migration scripts tested
- [ ] Test data cleaned

---

**END OF TESTING GUIDE**

*For technical specifications, see TECHNICAL_SPECS.md*  
*For user experience details, see USER_EXPERIENCE_GUIDE.md*  
*For monetization details, see MONETIZATION_MODEL.md*
