from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    listings,
    matching,
    notifications,
    logistics,
    wallet,
    analytics
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(listings.router, prefix="/listings", tags=["Listings"])
api_router.include_router(matching.router, prefix="/matches", tags=["Matching"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(logistics.router, prefix="/logistics", tags=["Logistics"])
api_router.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
