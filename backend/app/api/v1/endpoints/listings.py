from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List, Optional
from app.db.base import get_db
from app.core.deps import get_current_active_user
from app.models.models import Listing, User, ProvenanceRecord, ListingStatus
from app.schemas.schemas import (
    Listing as ListingSchema,
    ListingCreate,
    ListingUpdate,
    ProvenanceRecord as ProvenanceSchema
)
from app.services.pricing import PricingEngine
from app.utils.cache import cache

router = APIRouter()


@router.post("/", response_model=ListingSchema)
def create_listing(
    listing_in: ListingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new listing"""
    listing = Listing(
        **listing_in.dict(),
        owner_id=current_user.id,
        status=ListingStatus.ACTIVE
    )
    
    # Create full-text search vector
    search_text = f"{listing.title} {listing.description or ''} {listing.category.value}"
    listing.search_vector = search_text
    
    db.add(listing)
    db.commit()
    db.refresh(listing)
    
    # Create provenance record
    provenance = ProvenanceRecord(
        listing_id=listing.id,
        user_id=current_user.id,
        action="created",
        description=f"Listing created: {listing.title}"
    )
    db.add(provenance)
    db.commit()
    
    # Clear cache
    cache.clear_pattern("listings:*")
    
    return listing


@router.get("/", response_model=List[ListingSchema])
def list_listings(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all listings with optional filters"""
    # Try cache first
    cache_key = f"listings:{skip}:{limit}:{category}:{status}:{search}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    query = db.query(Listing)
    
    if category:
        query = query.filter(Listing.category == category)
    
    if status:
        query = query.filter(Listing.status == status)
    else:
        query = query.filter(Listing.status == ListingStatus.ACTIVE)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Listing.title.ilike(search_term),
                Listing.description.ilike(search_term),
                Listing.search_vector.ilike(search_term)
            )
        )
    
    listings = query.offset(skip).limit(limit).all()
    
    # Cache results
    cache.set(cache_key, [ListingSchema.from_orm(l).dict() for l in listings])
    
    return listings


@router.get("/{listing_id}", response_model=ListingSchema)
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    """Get a specific listing"""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing


@router.put("/{listing_id}", response_model=ListingSchema)
def update_listing(
    listing_id: int,
    listing_in: ListingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a listing"""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    if listing.owner_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Update fields
    update_data = listing_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(listing, field, value)
    
    # Update search vector if title or description changed
    if 'title' in update_data or 'description' in update_data:
        search_text = f"{listing.title} {listing.description or ''} {listing.category.value}"
        listing.search_vector = search_text
    
    db.commit()
    db.refresh(listing)
    
    # Create provenance record
    provenance = ProvenanceRecord(
        listing_id=listing.id,
        user_id=current_user.id,
        action="updated",
        description=f"Listing updated"
    )
    db.add(provenance)
    db.commit()
    
    # Clear cache
    cache.clear_pattern("listings:*")
    
    return listing


@router.delete("/{listing_id}")
def delete_listing(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a listing (soft delete by setting status to archived)"""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    if listing.owner_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    listing.status = ListingStatus.ARCHIVED
    db.commit()
    
    # Create provenance record
    provenance = ProvenanceRecord(
        listing_id=listing.id,
        user_id=current_user.id,
        action="archived",
        description=f"Listing archived"
    )
    db.add(provenance)
    db.commit()
    
    # Clear cache
    cache.clear_pattern("listings:*")
    
    return {"message": "Listing archived successfully"}


@router.get("/{listing_id}/provenance", response_model=List[ProvenanceSchema])
def get_listing_provenance(listing_id: int, db: Session = Depends(get_db)):
    """Get provenance history for a listing"""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    records = db.query(ProvenanceRecord).filter(
        ProvenanceRecord.listing_id == listing_id
    ).order_by(ProvenanceRecord.timestamp.desc()).all()
    
    return records


@router.get("/{listing_id}/price-recommendation")
def get_price_recommendation(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get price recommendation for a listing"""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    pricing_engine = PricingEngine(db)
    recommendation = pricing_engine.calculate_recommended_price(
        category=listing.category,
        quantity=listing.quantity,
        quality_grade=listing.quality_grade,
        certification=listing.certification
    )
    
    return recommendation
