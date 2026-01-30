from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum


class UserRole(enum.Enum):
    ADMIN = "admin"
    SUPPLIER = "supplier"
    BUYER = "buyer"


class ListingStatus(enum.Enum):
    ACTIVE = "active"
    PENDING = "pending"
    SOLD = "sold"
    ARCHIVED = "archived"


class MaterialCategory(enum.Enum):
    METAL = "metal"
    PLASTIC = "plastic"
    WOOD = "wood"
    TEXTILE = "textile"
    ELECTRONIC = "electronic"
    GLASS = "glass"
    PAPER = "paper"
    OTHER = "other"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.BUYER)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_score = Column(Float, default=0.0)
    company_name = Column(String)
    phone = Column(String)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    wallet_balance = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    listings = relationship("Listing", back_populates="owner", foreign_keys="Listing.owner_id")
    provenance_records = relationship("ProvenanceRecord", back_populates="user")
    notifications = relationship("Notification", back_populates="user")


class Listing(Base):
    __tablename__ = "listings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    category = Column(SQLEnum(MaterialCategory), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    status = Column(SQLEnum(ListingStatus), default=ListingStatus.ACTIVE)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    quality_grade = Column(String)
    certification = Column(String)
    available_from = Column(DateTime(timezone=True))
    available_until = Column(DateTime(timezone=True))
    images = Column(Text)  # JSON array of image URLs
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Full-text search
    search_vector = Column(Text)  # For PostgreSQL full-text search
    
    # Relationships
    owner = relationship("User", back_populates="listings", foreign_keys=[owner_id])
    matches = relationship("Match", back_populates="listing", foreign_keys="Match.listing_id")
    provenance_records = relationship("ProvenanceRecord", back_populates="listing")
    
    __table_args__ = (
        Index('idx_listing_search', 'search_vector'),
        Index('idx_listing_location', 'latitude', 'longitude'),
    )


class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    match_score = Column(Float, nullable=False)
    distance_km = Column(Float)
    price_compatibility = Column(Float)
    category_match = Column(Boolean)
    quality_match = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    listing = relationship("Listing", back_populates="matches", foreign_keys=[listing_id])
    buyer = relationship("User", foreign_keys=[buyer_id])


class ProvenanceRecord(Base):
    __tablename__ = "provenance_records"
    
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String, nullable=False)  # created, transferred, processed, etc.
    description = Column(Text)
    metadata = Column(Text)  # JSON for additional data
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    listing = relationship("Listing", back_populates="provenance_records")
    user = relationship("User", back_populates="provenance_records")


class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String)  # match, transaction, system, etc.
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="notifications")


class LogisticsSchedule(Base):
    __tablename__ = "logistics_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    pickup_location = Column(String)
    pickup_latitude = Column(Float)
    pickup_longitude = Column(Float)
    delivery_location = Column(String)
    delivery_latitude = Column(Float)
    delivery_longitude = Column(Float)
    scheduled_date = Column(DateTime(timezone=True))
    estimated_cost = Column(Float)
    status = Column(String, default="pending")
    carrier = Column(String)
    tracking_number = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
