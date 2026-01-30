from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from app.models.models import UserRole, ListingStatus, MaterialCategory


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.BUYER
    company_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class User(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    verification_score: float
    wallet_balance: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Listing Schemas
class ListingBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: MaterialCategory
    quantity: float
    unit: str
    price_per_unit: float
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    quality_grade: Optional[str] = None
    certification: Optional[str] = None
    available_from: Optional[datetime] = None
    available_until: Optional[datetime] = None
    images: Optional[str] = None


class ListingCreate(ListingBase):
    pass


class ListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[float] = None
    price_per_unit: Optional[float] = None
    status: Optional[ListingStatus] = None
    quality_grade: Optional[str] = None


class Listing(ListingBase):
    id: int
    status: ListingStatus
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Match Schema
class MatchBase(BaseModel):
    listing_id: int
    buyer_id: int
    match_score: float
    distance_km: Optional[float] = None
    price_compatibility: Optional[float] = None
    category_match: Optional[bool] = None
    quality_match: Optional[bool] = None


class Match(MatchBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Provenance Schema
class ProvenanceRecordCreate(BaseModel):
    listing_id: int
    action: str
    description: Optional[str] = None
    record_metadata: Optional[str] = None


class ProvenanceRecord(ProvenanceRecordCreate):
    id: int
    user_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


# Notification Schema
class NotificationCreate(BaseModel):
    user_id: int
    title: str
    message: str
    type: Optional[str] = None


class Notification(NotificationCreate):
    id: int
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Logistics Schema
class LogisticsScheduleCreate(BaseModel):
    listing_id: int
    pickup_location: str
    pickup_latitude: Optional[float] = None
    pickup_longitude: Optional[float] = None
    delivery_location: str
    delivery_latitude: Optional[float] = None
    delivery_longitude: Optional[float] = None
    scheduled_date: Optional[datetime] = None


class LogisticsSchedule(LogisticsScheduleCreate):
    id: int
    estimated_cost: Optional[float] = None
    status: str
    carrier: Optional[str] = None
    tracking_number: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Wallet Schema
class WalletTransaction(BaseModel):
    amount: float
    description: str


# Analytics Schema
class AnalyticsResponse(BaseModel):
    total_users: int
    total_listings: int
    active_listings: int
    total_matches: int
    total_transactions_value: float
    avg_match_score: float
    top_categories: List[dict]
    recent_activity: List[dict]
