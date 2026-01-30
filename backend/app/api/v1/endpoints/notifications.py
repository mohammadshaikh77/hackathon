from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.core.deps import get_current_active_user
from app.models.models import User, Notification
from app.schemas.schemas import Notification as NotificationSchema, NotificationCreate

router = APIRouter()


@router.post("/", response_model=NotificationSchema)
def create_notification(
    notification_in: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a notification (mock implementation)"""
    notification = Notification(**notification_in.dict())
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


@router.get("/", response_model=List[NotificationSchema])
def get_notifications(
    skip: int = 0,
    limit: int = 50,
    unread_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get notifications for current user"""
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    
    if unread_only:
        query = query.filter(Notification.is_read == False)
    
    notifications = query.order_by(
        Notification.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return notifications


@router.put("/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Mark notification as read"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    db.commit()
    
    return {"message": "Notification marked as read"}


@router.post("/send-match-notification")
def send_match_notification(
    buyer_id: int,
    listing_id: int,
    match_score: float,
    db: Session = Depends(get_db)
):
    """Send a match notification to a buyer (internal use)"""
    notification = Notification(
        user_id=buyer_id,
        title="New Match Found!",
        message=f"We found a listing that matches your preferences with a score of {match_score}%",
        type="match"
    )
    db.add(notification)
    db.commit()
    
    return {"message": "Notification sent"}
