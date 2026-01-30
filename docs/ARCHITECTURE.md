# Circular Economy Marketplace - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                            │
│                                                                 │
│  ┌──────────────────┐              ┌──────────────────────┐   │
│  │  React Frontend  │              │   Admin Dashboard    │   │
│  │  (Port 3000)     │              │    (React UI)        │   │
│  └────────┬─────────┘              └──────────┬───────────┘   │
└───────────┼────────────────────────────────────┼───────────────┘
            │                                    │
            │         HTTP/REST API              │
            └────────────────┬───────────────────┘
                             │
┌────────────────────────────┼───────────────────────────────────┐
│                    Application Layer                           │
│                                                                 │
│                  ┌──────────────────┐                          │
│                  │  FastAPI Server  │                          │
│                  │   (Port 8000)    │                          │
│                  └────────┬─────────┘                          │
│                           │                                     │
│      ┌────────────────────┼────────────────────┐              │
│      │                    │                    │              │
│ ┌────▼────┐         ┌────▼────┐         ┌────▼────┐          │
│ │  Auth   │         │Business │         │  API    │          │
│ │  Layer  │         │ Logic   │         │  Layer  │          │
│ │         │         │         │         │         │          │
│ │ - JWT   │         │-Matching│         │-REST v1 │          │
│ │ - RBAC  │         │-Pricing │         │-OpenAPI │          │
│ └─────────┘         │-Wallet  │         └─────────┘          │
│                     │-Logistics│                              │
│                     └─────────┘                               │
└─────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────┼───────────────────────────────────┐
│                     Data Layer                                 │
│                                                                 │
│    ┌────────────────┐            ┌──────────────┐             │
│    │   PostgreSQL   │            │    Redis     │             │
│    │   (Port 5432)  │            │  (Port 6379) │             │
│    │                │            │              │             │
│    │ - Users        │            │ - Cache      │             │
│    │ - Listings     │            │ - Sessions   │             │
│    │ - Matches      │            └──────────────┘             │
│    │ - Provenance   │                                         │
│    │ - Wallet       │                                         │
│    │ - Notifications│                                         │
│    │ - Logistics    │                                         │
│    └────────────────┘                                         │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### Backend (FastAPI)

```
backend/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/
│   │   │   ├── auth.py          # Authentication & user management
│   │   │   ├── listings.py      # CRUD for material listings
│   │   │   ├── matching.py      # Smart matching algorithm
│   │   │   ├── wallet.py        # Digital wallet simulation
│   │   │   ├── analytics.py     # Admin dashboard data
│   │   │   ├── notifications.py # User notifications
│   │   │   └── logistics.py     # Logistics scheduling
│   │   └── api.py               # API router aggregation
│   ├── core/
│   │   ├── config.py            # App configuration
│   │   ├── security.py          # JWT & password hashing
│   │   └── deps.py              # Dependency injection
│   ├── db/
│   │   └── base.py              # Database connection
│   ├── models/
│   │   └── models.py            # SQLAlchemy ORM models
│   ├── schemas/
│   │   └── schemas.py           # Pydantic validation schemas
│   ├── services/
│   │   ├── matching.py          # Matching algorithm logic
│   │   └── pricing.py           # Pricing recommendation engine
│   ├── utils/
│   │   └── cache.py             # Redis caching utilities
│   └── main.py                  # Application entry point
```

### Frontend (React)

```
frontend/
├── src/
│   ├── components/
│   │   └── Navbar.js            # Navigation component
│   ├── contexts/
│   │   └── AuthContext.js       # Authentication state
│   ├── pages/
│   │   ├── Login.js             # Login/Register page
│   │   ├── Marketplace.js       # Main marketplace view
│   │   └── AdminDashboard.js    # Analytics dashboard
│   ├── services/
│   │   └── api.js               # API client
│   ├── App.js                   # Main app component
│   └── index.js                 # Entry point
```

## Data Flow

### 1. User Registration & Authentication

```
Client                  Backend                Database
  │                       │                       │
  │──Register Request───> │                       │
  │    (POST /auth/       │                       │
  │     register)         │                       │
  │                       │──Create User─────────>│
  │                       │                       │
  │                       │<─User Created─────────│
  │<─User Object─────────│                       │
  │                       │                       │
  │──Login Request──────> │                       │
  │    (POST /auth/       │                       │
  │     login)            │                       │
  │                       │──Verify Password─────>│
  │                       │                       │
  │                       │<─User Data────────────│
  │<─JWT Token───────────│                       │
```

### 2. Listing Creation & Search

```
Client                  Backend                Cache      Database
  │                       │                       │           │
  │──Create Listing─────> │                       │           │
  │    (POST /listings)   │                       │           │
  │    [JWT Token]        │                       │           │
  │                       │──Validate Token───────────────────│
  │                       │                       │           │
  │                       │──Save Listing─────────────────────>│
  │                       │                       │           │
  │                       │──Create Provenance────────────────>│
  │                       │                       │           │
  │                       │──Clear Cache─────────>│           │
  │<─Listing Object──────│                       │           │
  │                       │                       │           │
  │──Search Listings────> │                       │           │
  │    (GET /listings)    │                       │           │
  │                       │──Check Cache────────>│           │
  │                       │                       │           │
  │                       │<─Cache Miss──────────│           │
  │                       │                       │           │
  │                       │──Query Database───────────────────>│
  │                       │                       │           │
  │                       │<─Results──────────────────────────│
  │                       │                       │           │
  │                       │──Cache Results──────>│           │
  │<─Listings Array──────│                       │           │
```

### 3. Smart Matching

```
Client                  Backend                Database
  │                       │                       │
  │──Find Matches───────> │                       │
  │    (POST /matches/    │                       │
  │     find)             │                       │
  │                       │──Get Buyer Info──────>│
  │                       │                       │
  │                       │──Get Active Listings─>│
  │                       │                       │
  │                       │<─Listings────────────│
  │                       │                       │
  │                       │  [Matching Algorithm] │
  │                       │  - Calculate Distance │
  │                       │  - Price Compatibility│
  │                       │  - Category Match     │
  │                       │  - Quality Score      │
  │                       │  - Verification Score │
  │                       │                       │
  │                       │──Save Matches────────>│
  │                       │                       │
  │<─Matches (sorted)────│                       │
```

### 4. Pricing Recommendation

```
Client                  Backend                Database
  │                       │                       │
  │──Get Price Rec.─────> │                       │
  │    (GET /listings/    │                       │
  │     {id}/price-rec)   │                       │
  │                       │                       │
  │                       │──Get Market Avg──────>│
  │                       │                       │
  │                       │<─Price Data──────────│
  │                       │                       │
  │                       │  [Pricing Engine]     │
  │                       │  - Base Price         │
  │                       │  - Quality Multiplier │
  │                       │  - Volume Discount    │
  │                       │  - Market Average     │
  │                       │  - Location Premium   │
  │                       │                       │
  │<─Price Recommendation│                       │
```

## Security Architecture

### Authentication Flow

```
1. User provides credentials
2. Backend validates against hashed password
3. JWT token generated with user info
4. Token includes:
   - User ID
   - Username
   - Role
   - Expiration (7 days)
5. Client stores token in localStorage
6. Token sent with all authenticated requests
7. Backend validates token on each request
8. Role-based access control enforced
```

### Role-Based Access Control

```
┌──────────┬───────────┬──────────┬────────────┐
│ Endpoint │   Buyer   │ Supplier │   Admin    │
├──────────┼───────────┼──────────┼────────────┤
│ /auth/*  │    ✓      │    ✓     │     ✓      │
│ /listings│    ✓      │    ✓     │     ✓      │
│ /matches │    ✓      │    ✗     │     ✓      │
│ /wallet  │    ✓      │    ✓     │     ✓      │
│ /analytics│   ✗      │    ✗     │     ✓      │
└──────────┴───────────┴──────────┴────────────┘
```

## Database Schema

### Entity Relationship Diagram

```
┌─────────────────┐
│     Users       │
├─────────────────┤
│ id (PK)         │
│ email           │
│ username        │
│ password_hash   │
│ role            │
│ wallet_balance  │
│ latitude        │
│ longitude       │
│ verification_   │
│  score          │
└────────┬────────┘
         │
         │ 1:N
         │
         ▼
┌─────────────────┐        1:N        ┌─────────────────┐
│    Listings     │◄───────────────────│    Matches      │
├─────────────────┤                    ├─────────────────┤
│ id (PK)         │                    │ id (PK)         │
│ owner_id (FK)   │                    │ listing_id (FK) │
│ title           │                    │ buyer_id (FK)   │
│ category        │                    │ match_score     │
│ price_per_unit  │                    │ distance_km     │
│ quantity        │                    └─────────────────┘
│ status          │
│ quality_grade   │
│ latitude        │
│ longitude       │
└────────┬────────┘
         │
         │ 1:N
         │
         ▼
┌─────────────────┐
│ Provenance      │
│   Records       │
├─────────────────┤
│ id (PK)         │
│ listing_id (FK) │
│ user_id (FK)    │
│ action          │
│ timestamp       │
│ metadata        │
└─────────────────┘
```

## Matching Algorithm

### Score Calculation (0-100)

```python
match_score = (
    distance_score * 0.30 +      # 30% - proximity
    price_score * 0.25 +          # 25% - price compatibility
    category_score * 0.25 +       # 25% - category match
    quality_score * 0.10 +        # 10% - quality grade
    verification_score * 0.10     # 10% - supplier trust
)

# Distance scoring
distance_score = max(0, 100 - (distance_km / 100 * 100))

# Price scoring (if within budget)
if price <= max_price:
    price_score = 100
else:
    price_score = max(0, 100 - ((price - max_price) / max_price * 100))

# Category scoring
category_score = 100 if match else 30

# Quality scoring
quality_map = {'A': 100, 'B': 80, 'C': 60, 'D': 40}

# Verification scoring
verification_score = supplier.verification_score
```

## Deployment Architecture

### Docker Compose Setup

```
┌─────────────────────────────────────────────────────┐
│              Docker Host                             │
│                                                      │
│  ┌────────────────┐  ┌────────────────┐            │
│  │   Frontend     │  │    Backend     │            │
│  │   Container    │  │   Container    │            │
│  │                │  │                │            │
│  │  Node:18       │  │  Python:3.11   │            │
│  │  Port: 3000    │  │  Port: 8000    │            │
│  └────────────────┘  └────────┬───────┘            │
│                                │                     │
│         ┌──────────────────────┼─────────────┐      │
│         │                      │             │      │
│  ┌──────▼───────┐      ┌──────▼──────┐  ┌───▼───┐ │
│  │  PostgreSQL  │      │    Redis    │  │ Vols  │ │
│  │  Container   │      │  Container  │  │       │ │
│  │              │      │             │  │       │ │
│  │  Port: 5432  │      │ Port: 6379  │  │       │ │
│  └──────────────┘      └─────────────┘  └───────┘ │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## Performance Considerations

### Caching Strategy

- **Listing Queries**: 5-minute cache
- **User Sessions**: Redis-based
- **Cache Invalidation**: On create/update/delete operations

### Database Indexing

```sql
-- Primary indexes on all primary keys
-- Composite index on listing search
CREATE INDEX idx_listing_search ON listings(search_vector);

-- Geospatial index for location queries
CREATE INDEX idx_listing_location ON listings(latitude, longitude);

-- Index on foreign keys
CREATE INDEX idx_listing_owner ON listings(owner_id);
CREATE INDEX idx_match_buyer ON matches(buyer_id);
```

### Scalability

- **Horizontal Scaling**: Multiple backend instances behind load balancer
- **Database**: Read replicas for heavy read operations
- **Cache**: Redis cluster for distributed caching
- **Static Assets**: CDN for frontend

## API Rate Limits (Recommended for Production)

```
Standard User:
- 100 requests/minute
- 1000 requests/hour

Admin User:
- 500 requests/minute
- 5000 requests/hour
```

## Monitoring & Logging

### Recommended Tools

- **Application Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **APM**: New Relic or DataDog
- **Error Tracking**: Sentry
- **Uptime Monitoring**: Pingdom or UptimeRobot

### Key Metrics to Monitor

- API response times
- Database query performance
- Cache hit/miss ratio
- Error rates
- Active users
- Match generation rate
- Transaction volume
