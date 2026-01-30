# Circular Economy Marketplace

A production-grade platform for sustainable material trading with full-stack implementation using FastAPI, PostgreSQL, Redis, and React.

## 🌟 Features

### Core Modules
- **Listings CRUD**: Complete management of material listings
- **Smart Matching**: AI-powered matching algorithm with match scores (0-100)
- **Material Provenance**: Append-only blockchain-style tracking of material history
- **Pricing Engine**: Rule-based recommendation system with market analysis
- **Digital Wallet**: Simulated wallet for transactions
- **Notifications**: Mock notification system for user alerts
- **Trust & Verification**: User verification scoring system
- **Logistics Scheduling**: Delivery and pickup management
- **Admin Analytics**: Comprehensive dashboard with charts and metrics
- **JWT Authentication**: Secure token-based auth with role-based access control

### Technical Features
- PostgreSQL full-text search for listings
- Redis caching for performance optimization
- Google Maps integration for location services
- RESTful API with OpenAPI documentation
- Clean architecture with separation of concerns
- Dockerized microservices
- Production-ready code structure

## 🏗️ Architecture

```
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Configuration & security
│   │   ├── db/          # Database configuration
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   └── utils/       # Utilities (cache, etc.)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── contexts/    # Context providers
│   │   ├── pages/       # Page components
│   │   └── services/    # API services
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml   # Docker orchestration
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Using Docker (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/mohammadshaikh77/hackathon.git
cd hackathon
```

2. **Set up environment variables**
```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env with your settings

# Frontend
cp frontend/.env.example frontend/.env
# Edit frontend/.env with your settings
```

3. **Start all services**
```bash
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- Redis cache on port 6379
- FastAPI backend on port 8000
- React frontend on port 3000

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative API Docs: http://localhost:8000/redoc

### Local Development (Without Docker)

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your database settings

# Run migrations (database will be created automatically)
# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment
cp .env.example .env

# Start development server
npm start
```

#### Database Setup (if running locally)

```bash
# Install PostgreSQL and Redis
# Create database
createdb circular_economy

# The application will create tables automatically on first run
```

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "password",
  "full_name": "Full Name",
  "role": "buyer"  // or "supplier" or "admin"
}
```

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=username&password=password
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### Get Current User
```http
GET /api/v1/auth/me
Authorization: Bearer {token}
```

### Listings Endpoints

#### Create Listing
```http
POST /api/v1/listings/
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Recycled Aluminum Sheets",
  "description": "High-quality recycled aluminum",
  "category": "metal",
  "quantity": 1000,
  "unit": "kg",
  "price_per_unit": 2.5,
  "location": "New York, NY",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "quality_grade": "A"
}
```

#### List All Listings
```http
GET /api/v1/listings/?category=metal&search=aluminum&limit=50
```

#### Get Listing Details
```http
GET /api/v1/listings/{id}
```

#### Update Listing
```http
PUT /api/v1/listings/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "price_per_unit": 3.0,
  "quantity": 800
}
```

#### Get Price Recommendation
```http
GET /api/v1/listings/{id}/price-recommendation
Authorization: Bearer {token}
```

Response:
```json
{
  "min_price": 42.5,
  "recommended_price": 50.0,
  "max_price": 60.0,
  "market_average": 48.5,
  "confidence": "high"
}
```

#### Get Provenance History
```http
GET /api/v1/listings/{id}/provenance
```

### Matching Endpoints

#### Find Matches
```http
POST /api/v1/matches/find
Authorization: Bearer {token}
Content-Type: application/json

{
  "max_price": 100,
  "preferred_categories": ["metal", "plastic"]
}
```

Response: Array of matches with scores
```json
[
  {
    "id": 1,
    "listing_id": 5,
    "buyer_id": 2,
    "match_score": 87.5,
    "distance_km": 15.3,
    "category_match": true,
    "quality_match": true
  }
]
```

#### Get My Matches
```http
GET /api/v1/matches/
Authorization: Bearer {token}
```

### Wallet Endpoints

#### Get Balance
```http
GET /api/v1/wallet/balance
Authorization: Bearer {token}
```

#### Deposit Funds
```http
POST /api/v1/wallet/deposit
Authorization: Bearer {token}
Content-Type: application/json

{
  "amount": 500.0,
  "description": "Initial deposit"
}
```

#### Transfer Funds
```http
POST /api/v1/wallet/transfer?recipient_id=5
Authorization: Bearer {token}
Content-Type: application/json

{
  "amount": 100.0,
  "description": "Payment for materials"
}
```

### Analytics Endpoints (Admin Only)

#### Get Dashboard Analytics
```http
GET /api/v1/analytics/dashboard
Authorization: Bearer {admin_token}
```

Response:
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
  "recent_activity": [...]
}
```

#### Get Market Trends
```http
GET /api/v1/analytics/market/trends
Authorization: Bearer {admin_token}
```

### Logistics Endpoints

#### Create Logistics Schedule
```http
POST /api/v1/logistics/
Authorization: Bearer {token}
Content-Type: application/json

{
  "listing_id": 5,
  "pickup_location": "123 Main St",
  "pickup_latitude": 40.7128,
  "pickup_longitude": -74.0060,
  "delivery_location": "456 Oak Ave",
  "delivery_latitude": 40.7580,
  "delivery_longitude": -73.9855
}
```

#### Update Logistics Status
```http
PUT /api/v1/logistics/{id}/status?status=in_transit&tracking_number=TRACK123
Authorization: Bearer {token}
```

## 🧮 Matching Algorithm

The smart matching system uses a weighted scoring algorithm:

- **Distance (30%)**: Proximity between buyer and supplier
- **Price (25%)**: Price compatibility with buyer preferences
- **Category (25%)**: Category match with buyer interests
- **Quality (10%)**: Quality grade of materials
- **Verification (10%)**: Supplier verification score

Match scores range from 0-100, with scores above 50 considered viable matches.

## 💰 Pricing Engine

The pricing recommendation engine uses:

1. **Base Prices**: Category-specific baseline prices
2. **Quality Multipliers**: Premium for higher grades
3. **Market Analysis**: Real-time market average calculation
4. **Volume Discounts**: Bulk quantity adjustments
5. **Demand Prediction**: Simple supply/demand analysis

## 🔐 Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- Role-based access control (Admin, Supplier, Buyer)
- CORS protection
- Environment-based configuration
- SQL injection protection via SQLAlchemy ORM

## 🗄️ Database Schema

### Users Table
- Authentication and profile information
- Role-based permissions
- Wallet balance
- Verification score
- Location coordinates

### Listings Table
- Material details and pricing
- Status tracking
- Full-text search vector
- Owner relationship
- Location data

### Matches Table
- Listing-buyer relationships
- Match scores and metrics
- Distance calculations

### Provenance Records Table
- Append-only audit trail
- Material lifecycle tracking
- Timestamp-based ordering

### Notifications Table
- User alerts
- Read status tracking

### Logistics Schedules Table
- Pickup/delivery coordination
- Cost estimation
- Tracking integration

## 📊 Testing

Access the interactive API documentation to test endpoints:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Sample Test Flow

1. Register a new user (role: buyer)
2. Register another user (role: supplier)
3. Login as supplier and create listings
4. Login as buyer and find matches
5. View match scores and details
6. Check provenance history
7. Access admin dashboard (if admin user)

## 🔧 Configuration

### Backend Environment Variables

See `backend/.env.example` for all available options:
- Database connection
- Redis configuration
- JWT settings
- CORS origins
- Google Maps API key

### Frontend Environment Variables

See `frontend/.env.example`:
- API URL
- Google Maps API key

## 📈 Performance Optimization

- **Redis Caching**: Listing queries are cached for 5 minutes
- **Database Indexing**: Full-text search and location indexes
- **Connection Pooling**: PostgreSQL connection pool
- **Lazy Loading**: Frontend components load on demand

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
docker-compose ps

# View logs
docker-compose logs postgres
```

### Backend Issues
```bash
# View backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

### Frontend Issues
```bash
# Clear npm cache and rebuild
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 📝 API Rate Limits

Currently no rate limiting is implemented. For production deployment, consider adding:
- Rate limiting middleware
- Request throttling
- API key management

## 🚀 Production Deployment

### Recommendations

1. **Change default secrets** in environment files
2. **Use managed PostgreSQL** (AWS RDS, Google Cloud SQL)
3. **Use managed Redis** (AWS ElastiCache, Redis Cloud)
4. **Enable HTTPS** with SSL certificates
5. **Set up monitoring** (Prometheus, Grafana)
6. **Configure logging** (ELK stack, CloudWatch)
7. **Add backup strategy** for database
8. **Implement API rate limiting**
9. **Use CDN** for frontend assets
10. **Add health checks** for load balancers

### Environment-Specific Settings

```bash
# Production
SECRET_KEY=<long-random-string>
POSTGRES_SERVER=<production-db-host>
REDIS_HOST=<production-redis-host>
```

## 🤝 Contributing

This is a hackathon project. For production use:
1. Add comprehensive tests
2. Implement additional validation
3. Add more error handling
4. Enhance security measures
5. Add monitoring and logging

## 📄 License

This project is created for the hackathon. See repository for license details.

## 🆘 Support

For issues and questions:
- Check the API documentation at `/docs`
- Review the code comments
- Check Docker logs for errors

## 🎯 Future Enhancements

- Real-time notifications with WebSockets
- Advanced ML-based pricing predictions
- Blockchain integration for provenance
- Mobile application
- Payment gateway integration
- Advanced analytics and reporting
- Multi-language support
- Real Google Maps integration
- File upload for listing images
- Email notifications
- SMS notifications for logistics
- Advanced search filters
- Saved searches and alerts
