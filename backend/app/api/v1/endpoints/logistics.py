from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.core.deps import get_current_active_user
from app.models.models import User, LogisticsSchedule
from app.schemas.schemas import LogisticsSchedule as LogisticsSchema, LogisticsScheduleCreate
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=LogisticsSchema)
def create_logistics_schedule(
    schedule_in: LogisticsScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a logistics schedule"""
    # Calculate estimated cost based on distance (simplified)
    estimated_cost = 50.0  # Base cost
    
    if schedule_in.pickup_latitude and schedule_in.delivery_latitude:
        from app.services.matching import calculate_distance
        distance = calculate_distance(
            schedule_in.pickup_latitude,
            schedule_in.pickup_longitude,
            schedule_in.delivery_latitude,
            schedule_in.delivery_longitude
        )
        estimated_cost += distance * 2.5  # $2.5 per km
    
    schedule = LogisticsSchedule(
        **schedule_in.dict(),
        estimated_cost=estimated_cost,
        status="pending"
    )
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    
    return schedule


@router.get("/", response_model=List[LogisticsSchema])
def get_logistics_schedules(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all logistics schedules"""
    schedules = db.query(LogisticsSchedule).offset(skip).limit(limit).all()
    return schedules


@router.get("/{schedule_id}", response_model=LogisticsSchema)
def get_logistics_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific logistics schedule"""
    schedule = db.query(LogisticsSchedule).filter(
        LogisticsSchedule.id == schedule_id
    ).first()
    
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    return schedule


@router.put("/{schedule_id}/status")
def update_logistics_status(
    schedule_id: int,
    status: str,
    tracking_number: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update logistics status"""
    schedule = db.query(LogisticsSchedule).filter(
        LogisticsSchedule.id == schedule_id
    ).first()
    
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    schedule.status = status
    if tracking_number:
        schedule.tracking_number = tracking_number
    
    db.commit()
    
    return {"message": "Status updated successfully"}
