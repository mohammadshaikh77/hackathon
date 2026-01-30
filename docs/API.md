# Circular Economy Marketplace - API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication

All authenticated endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

Get your token by calling the login endpoint.

---

## Endpoints Overview

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

### Listings
- `POST /listings/` - Create a new listing
- `GET /listings/` - Get all listings (with filters)
- `GET /listings/{id}` - Get specific listing
- `PUT /listings/{id}` - Update listing
- `DELETE /listings/{id}` - Archive listing
- `GET /listings/{id}/provenance` - Get material provenance
- `GET /listings/{id}/price-recommendation` - Get price recommendation

### Matching
- `POST /matches/find` - Find matches for buyer
- `GET /matches/` - Get user's matches
- `GET /matches/{id}` - Get specific match

### Wallet
- `GET /wallet/balance` - Get wallet balance
- `POST /wallet/deposit` - Deposit funds
- `POST /wallet/withdraw` - Withdraw funds
- `POST /wallet/transfer` - Transfer to another user

### Notifications
- `GET /notifications/` - Get user notifications
- `PUT /notifications/{id}/read` - Mark as read

### Logistics
- `POST /logistics/` - Create logistics schedule
- `GET /logistics/` - Get all schedules
- `GET /logistics/{id}` - Get specific schedule
- `PUT /logistics/{id}/status` - Update status

### Analytics (Admin Only)
- `GET /analytics/dashboard` - Get dashboard data
- `GET /analytics/users/stats` - Get user statistics
- `GET /analytics/listings/stats` - Get listing statistics
- `GET /analytics/market/trends` - Get market trends

---

## Detailed Endpoint Documentation

### 1. Authentication

#### Register User
**POST** `/auth/register`

Request Body:
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword",
  "full_name": "John Doe",
  "role": "buyer",
  "company_name": "Acme Corp",
  "phone": "+1234567890",
  "address": "123 Main St, New York, NY",
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

Response: `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "role": "buyer",
  "is_active": true,
  "is_verified": false,
  "verification_score": 0.0,
  "wallet_balance": 0.0,
  "created_at": "2024-01-01T12:00:00"
}
```

#### Login
**POST** `/auth/login`

Content-Type: `application/x-www-form-urlencoded`

Request Body:
```
username=johndoe&password=securepassword
```

Response: `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Get Current User
**GET** `/auth/me`

Headers: `Authorization: Bearer <token>`

Response: `200 OK` - Returns user object

---

### 2. Listings

#### Create Listing
**POST** `/listings/`

Headers: `Authorization: Bearer <token>`

Request Body:
```json
{
  "title": "Recycled Aluminum Sheets",
  "description": "High-quality recycled aluminum suitable for construction",
  "category": "metal",
  "quantity": 1000,
  "unit": "kg",
  "price_per_unit": 2.5,
  "location": "New York, NY",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "quality_grade": "A",
  "certification": "ISO-14001",
  "available_from": "2024-01-01T00:00:00",
  "available_until": "2024-12-31T23:59:59"
}
```

Categories: `metal`, `plastic`, `wood`, `textile`, `electronic`, `glass`, `paper`, `other`

Quality Grades: `A` (Premium), `B` (Good), `C` (Standard), `D` (Lower)

Response: `200 OK` - Returns created listing object

#### List Listings
**GET** `/listings/`

Query Parameters:
- `skip` (int, default: 0): Pagination offset
- `limit` (int, default: 100): Max results
- `category` (string): Filter by category
- `status` (string): Filter by status (active, pending, sold, archived)
- `search` (string): Full-text search in title/description

Example:
```
GET /listings/?category=metal&search=aluminum&limit=20
```

Response: `200 OK` - Array of listing objects

#### Get Listing
**GET** `/listings/{id}`

Response: `200 OK` - Listing object

#### Update Listing
**PUT** `/listings/{id}`

Headers: `Authorization: Bearer <token>`

Request Body (all fields optional):
```json
{
  "title": "Updated Title",
  "description": "Updated description",
  "quantity": 900,
  "price_per_unit": 3.0,
  "status": "active"
}
```

Response: `200 OK` - Updated listing object

#### Get Price Recommendation
**GET** `/listings/{id}/price-recommendation`

Headers: `Authorization: Bearer <token>`

Response: `200 OK`
```json
{
  "min_price": 42.5,
  "recommended_price": 50.0,
  "max_price": 60.0,
  "market_average": 48.5,
  "confidence": "high"
}
```

#### Get Provenance
**GET** `/listings/{id}/provenance`

Response: `200 OK`
```json
[
  {
    "id": 1,
    "listing_id": 5,
    "user_id": 2,
    "action": "created",
    "description": "Listing created: Recycled Aluminum",
    "timestamp": "2024-01-01T12:00:00"
  },
  {
    "id": 2,
    "listing_id": 5,
    "user_id": 2,
    "action": "updated",
    "description": "Price updated",
    "timestamp": "2024-01-02T14:30:00"
  }
]
```

---

### 3. Matching

#### Find Matches
**POST** `/matches/find`

Headers: `Authorization: Bearer <token>`

Query Parameters:
- `limit` (int, default: 20): Max number of matches

Request Body (optional preferences):
```json
{
  "max_price": 100,
  "preferred_categories": ["metal", "plastic"]
}
```

Response: `200 OK`
```json
[
  {
    "id": 1,
    "listing_id": 5,
    "buyer_id": 2,
    "match_score": 87.5,
    "distance_km": 15.3,
    "price_compatibility": 0.95,
    "category_match": true,
    "quality_match": true,
    "created_at": "2024-01-01T12:00:00"
  }
]
```

Match Score Breakdown:
- 0-50: Poor match
- 50-70: Fair match
- 70-85: Good match
- 85-100: Excellent match

#### Get My Matches
**GET** `/matches/`

Headers: `Authorization: Bearer <token>`

Query Parameters:
- `limit` (int, default: 20): Max results

Response: `200 OK` - Array of match objects

---

### 4. Wallet

#### Get Balance
**GET** `/wallet/balance`

Headers: `Authorization: Bearer <token>`

Response: `200 OK`
```json
{
  "balance": 1500.50,
  "currency": "USD"
}
```

#### Deposit
**POST** `/wallet/deposit`

Headers: `Authorization: Bearer <token>`

Request Body:
```json
{
  "amount": 500.0,
  "description": "Initial deposit"
}
```

Response: `200 OK`
```json
{
  "message": "Deposit successful",
  "new_balance": 2000.50,
  "transaction": "Initial deposit"
}
```

#### Withdraw
**POST** `/wallet/withdraw`

Headers: `Authorization: Bearer <token>`

Request Body:
```json
{
  "amount": 200.0,
  "description": "Withdrawal to bank"
}
```

Response: `200 OK`
```json
{
  "message": "Withdrawal successful",
  "new_balance": 1800.50,
  "transaction": "Withdrawal to bank"
}
```

#### Transfer
**POST** `/wallet/transfer?recipient_id=5`

Headers: `Authorization: Bearer <token>`

Request Body:
```json
{
  "amount": 100.0,
  "description": "Payment for materials"
}
```

Response: `200 OK`
```json
{
  "message": "Transfer successful",
  "new_balance": 1700.50,
  "recipient": "supplier_user",
  "amount": 100.0
}
```

---

### 5. Notifications

#### Get Notifications
**GET** `/notifications/`

Headers: `Authorization: Bearer <token>`

Query Parameters:
- `skip` (int, default: 0): Pagination offset
- `limit` (int, default: 50): Max results
- `unread_only` (bool, default: false): Show only unread

Response: `200 OK`
```json
[
  {
    "id": 1,
    "user_id": 2,
    "title": "New Match Found!",
    "message": "We found a listing that matches your preferences with a score of 87.5%",
    "type": "match",
    "is_read": false,
    "created_at": "2024-01-01T12:00:00"
  }
]
```

#### Mark as Read
**PUT** `/notifications/{id}/read`

Headers: `Authorization: Bearer <token>`

Response: `200 OK`
```json
{
  "message": "Notification marked as read"
}
```

---

### 6. Logistics

#### Create Schedule
**POST** `/logistics/`

Headers: `Authorization: Bearer <token>`

Request Body:
```json
{
  "listing_id": 5,
  "pickup_location": "123 Main St, NY",
  "pickup_latitude": 40.7128,
  "pickup_longitude": -74.0060,
  "delivery_location": "456 Oak Ave, NJ",
  "delivery_latitude": 40.7580,
  "delivery_longitude": -73.9855,
  "scheduled_date": "2024-02-01T10:00:00"
}
```

Response: `200 OK`
```json
{
  "id": 1,
  "listing_id": 5,
  "pickup_location": "123 Main St, NY",
  "delivery_location": "456 Oak Ave, NJ",
  "estimated_cost": 88.25,
  "status": "pending",
  "created_at": "2024-01-01T12:00:00"
}
```

Cost Calculation: Base $50 + ($2.5 per km)

#### Update Status
**PUT** `/logistics/{id}/status?status=in_transit&tracking_number=TRACK123`

Headers: `Authorization: Bearer <token>`

Status Options: `pending`, `confirmed`, `in_transit`, `delivered`, `cancelled`

Response: `200 OK`
```json
{
  "message": "Status updated successfully"
}
```

---

### 7. Analytics (Admin Only)

#### Dashboard
**GET** `/analytics/dashboard`

Headers: `Authorization: Bearer <admin_token>`

Response: `200 OK`
```json
{
  "total_users": 150,
  "total_listings": 450,
  "active_listings": 280,
  "total_matches": 1240,
  "total_transactions_value": 125000.0,
  "avg_match_score": 76.3,
  "top_categories": [
    {"category": "metal", "count": 120},
    {"category": "plastic", "count": 95}
  ],
  "recent_activity": [
    {
      "type": "listing_created",
      "title": "Recycled Steel",
      "category": "metal",
      "created_at": "2024-01-01T12:00:00"
    }
  ]
}
```

#### Market Trends
**GET** `/analytics/market/trends`

Headers: `Authorization: Bearer <admin_token>`

Response: `200 OK`
```json
{
  "market_trends": [
    {
      "category": "metal",
      "demand_level": "high",
      "price_trend": "increasing",
      "active_listings": 4
    },
    {
      "category": "plastic",
      "demand_level": "medium",
      "price_trend": "stable",
      "active_listings": 12
    }
  ]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Rate Limiting

Currently no rate limiting implemented. Recommended for production:
- 100 requests per minute per IP
- 1000 requests per hour per user

---

## Pagination

List endpoints support pagination:
- `skip`: Number of records to skip (default: 0)
- `limit`: Max records to return (default: varies by endpoint)

Example:
```
GET /listings/?skip=20&limit=10
```

---

## Full-Text Search

The listings endpoint supports full-text search:
```
GET /listings/?search=recycled+aluminum
```

Searches in: title, description, category

---

## Interactive Documentation

Visit these URLs when the backend is running:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/api/v1/openapi.json
