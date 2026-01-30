from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.base import get_db
from app.core.deps import require_admin
from app.models.models import User, Listing, Match, ListingStatus
from app.schemas.schemas import AnalyticsResponse
from app.services.pricing import PricingEngine

router = APIRouter()


@router.get("/dashboard", response_model=AnalyticsResponse)
def get_analytics_dashboard(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Get admin analytics dashboard data"""
    
    # Total counts
    total_users = db.query(func.count(User.id)).scalar()
    total_listings = db.query(func.count(Listing.id)).scalar()
    active_listings = db.query(func.count(Listing.id)).filter(
        Listing.status == ListingStatus.ACTIVE
    ).scalar()
    total_matches = db.query(func.count(Match.id)).scalar()
    
    # Average match score
    avg_match_score = db.query(func.avg(Match.match_score)).scalar() or 0.0
    
    # Total transaction value (sum of active listing values)
    total_value = db.query(
        func.sum(Listing.quantity * Listing.price_per_unit)
    ).filter(Listing.status == ListingStatus.ACTIVE).scalar() or 0.0
    
    # Top categories
    top_categories = db.query(
        Listing.category,
        func.count(Listing.id).label('count')
    ).group_by(Listing.category).order_by(func.count(Listing.id).desc()).limit(5).all()
    
    top_categories_list = [
        {"category": cat.value, "count": count}
        for cat, count in top_categories
    ]
    
    # Recent activity (last 10 listings)
    recent_listings = db.query(Listing).order_by(
        Listing.created_at.desc()
    ).limit(10).all()
    
    recent_activity = [
        {
            "type": "listing_created",
            "title": listing.title,
            "category": listing.category.value,
            "created_at": listing.created_at.isoformat()
        }
        for listing in recent_listings
    ]
    
    return AnalyticsResponse(
        total_users=total_users,
        total_listings=total_listings,
        active_listings=active_listings,
        total_matches=total_matches,
        total_transactions_value=float(total_value),
        avg_match_score=float(avg_match_score),
        top_categories=top_categories_list,
        recent_activity=recent_activity
    )


@router.get("/users/stats")
def get_user_stats(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Get user statistics"""
    total_users = db.query(func.count(User.id)).scalar()
    verified_users = db.query(func.count(User.id)).filter(User.is_verified == True).scalar()
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()
    
    # Users by role
    users_by_role = db.query(
        User.role,
        func.count(User.id).label('count')
    ).group_by(User.role).all()
    
    role_distribution = {role.value: count for role, count in users_by_role}
    
    return {
        "total_users": total_users,
        "verified_users": verified_users,
        "active_users": active_users,
        "role_distribution": role_distribution
    }


@router.get("/listings/stats")
def get_listing_stats(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Get listing statistics"""
    # Listings by status
    listings_by_status = db.query(
        Listing.status,
        func.count(Listing.id).label('count')
    ).group_by(Listing.status).all()
    
    status_distribution = {status.value: count for status, count in listings_by_status}
    
    # Average price by category
    avg_prices = db.query(
        Listing.category,
        func.avg(Listing.price_per_unit).label('avg_price')
    ).group_by(Listing.category).all()
    
    avg_price_by_category = {
        cat.value: float(price) for cat, price in avg_prices
    }
    
    return {
        "status_distribution": status_distribution,
        "avg_price_by_category": avg_price_by_category
    }


@router.get("/market/trends")
def get_market_trends(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Get market trends and demand predictions"""
    from app.models.models import MaterialCategory
    
    pricing_engine = PricingEngine(db)
    trends = []
    
    for category in MaterialCategory:
        demand_info = pricing_engine.predict_demand(category)
        trends.append(demand_info)
    
    return {"market_trends": trends}
