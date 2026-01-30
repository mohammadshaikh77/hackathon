from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.core.deps import get_current_active_user
from app.models.models import User, Match
from app.schemas.schemas import Match as MatchSchema
from app.services.matching import find_matches, get_buyer_matches

router = APIRouter()


@router.post("/find", response_model=List[MatchSchema])
def find_buyer_matches(
    preferences: dict = None,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Find matches for current buyer based on preferences"""
    matches = find_matches(
        db=db,
        buyer_id=current_user.id,
        buyer_preferences=preferences,
        limit=limit
    )
    return matches


@router.get("/", response_model=List[MatchSchema])
def get_my_matches(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get existing matches for current user"""
    matches = get_buyer_matches(db, current_user.id, limit)
    return matches


@router.get("/{match_id}", response_model=MatchSchema)
def get_match(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific match"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Ensure user has access to this match
    if match.buyer_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return match
