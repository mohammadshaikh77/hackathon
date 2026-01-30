import math
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.models import Listing, User, Match
from app.schemas.schemas import Match as MatchSchema


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates using Haversine formula (in km)"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c


def calculate_match_score(
    listing: Listing,
    buyer: User,
    buyer_preferences: Dict = None
) -> float:
    """
    Calculate match score between a listing and a buyer
    Score is 0-100, higher is better
    """
    score = 0.0
    weights = {
        'distance': 0.3,
        'price': 0.25,
        'category': 0.25,
        'quality': 0.1,
        'verification': 0.1
    }
    
    # Distance score (closer is better)
    if listing.latitude and listing.longitude and buyer.latitude and buyer.longitude:
        distance = calculate_distance(
            listing.latitude, listing.longitude,
            buyer.latitude, buyer.longitude
        )
        # Score decreases with distance (max 100km for full score)
        distance_score = max(0, 100 - (distance / 100 * 100))
        score += distance_score * weights['distance']
    else:
        score += 50 * weights['distance']  # Neutral score if location unknown
    
    # Price score (based on buyer preferences or market average)
    if buyer_preferences and 'max_price' in buyer_preferences:
        max_price = buyer_preferences['max_price']
        if listing.price_per_unit <= max_price:
            price_score = 100
        else:
            price_score = max(0, 100 - ((listing.price_per_unit - max_price) / max_price * 100))
        score += price_score * weights['price']
    else:
        score += 70 * weights['price']  # Default score
    
    # Category match
    if buyer_preferences and 'preferred_categories' in buyer_preferences:
        if listing.category.value in buyer_preferences['preferred_categories']:
            score += 100 * weights['category']
        else:
            score += 30 * weights['category']
    else:
        score += 70 * weights['category']
    
    # Quality score
    quality_scores = {'A': 100, 'B': 80, 'C': 60, 'D': 40}
    if listing.quality_grade in quality_scores:
        score += quality_scores[listing.quality_grade] * weights['quality']
    else:
        score += 70 * weights['quality']
    
    # Verification score
    if hasattr(listing, 'owner') and listing.owner:
        score += listing.owner.verification_score * weights['verification']
    else:
        score += 50 * weights['verification']
    
    return round(score, 2)


def find_matches(
    db: Session,
    buyer_id: int,
    buyer_preferences: Dict = None,
    limit: int = 20
) -> List[Match]:
    """Find matching listings for a buyer"""
    buyer = db.query(User).filter(User.id == buyer_id).first()
    if not buyer:
        return []
    
    # Get active listings
    listings = db.query(Listing).filter(
        Listing.status == "active",
        Listing.owner_id != buyer_id  # Don't match own listings
    ).all()
    
    matches = []
    for listing in listings:
        match_score = calculate_match_score(listing, buyer, buyer_preferences)
        
        # Only create matches with score > 50
        if match_score > 50:
            distance = None
            if listing.latitude and listing.longitude and buyer.latitude and buyer.longitude:
                distance = calculate_distance(
                    listing.latitude, listing.longitude,
                    buyer.latitude, buyer.longitude
                )
            
            match = Match(
                listing_id=listing.id,
                buyer_id=buyer_id,
                match_score=match_score,
                distance_km=distance,
                category_match=True,
                quality_match=bool(listing.quality_grade)
            )
            db.add(match)
            matches.append(match)
    
    db.commit()
    
    # Return top matches sorted by score
    matches.sort(key=lambda x: x.match_score, reverse=True)
    return matches[:limit]


def get_buyer_matches(db: Session, buyer_id: int, limit: int = 20) -> List[Match]:
    """Get existing matches for a buyer"""
    matches = db.query(Match).filter(
        Match.buyer_id == buyer_id
    ).order_by(Match.match_score.desc()).limit(limit).all()
    
    return matches
