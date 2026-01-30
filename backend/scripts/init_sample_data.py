"""
Sample data initialization script
Run this to populate the database with sample data for testing
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import SessionLocal, engine, Base
from app.models.models import User, Listing, UserRole, ListingStatus, MaterialCategory
from app.core.security import get_password_hash
from datetime import datetime, timedelta

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Check if data already exists
    if db.query(User).count() > 0:
        print("⚠️  Database already contains data. Skipping initialization.")
        sys.exit(0)
    
    print("📝 Creating sample users...")
    
    # Create admin user
    admin = User(
        email="admin@circular.eco",
        username="admin",
        hashed_password=get_password_hash("admin123"),
        full_name="Admin User",
        role=UserRole.ADMIN,
        is_active=True,
        is_verified=True,
        verification_score=100.0,
        wallet_balance=10000.0,
        company_name="Circular Economy Platform"
    )
    db.add(admin)
    db.commit()
    
    print(f"✓ Created admin user")
    print("\n✅ Sample data initialization complete!")
    print("\n🔐 Login credentials:")
    print("   Admin: admin / admin123")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
    raise
finally:
    db.close()
