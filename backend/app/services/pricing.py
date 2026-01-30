from typing import Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Listing, MaterialCategory
import numpy as np


class PricingEngine:
    """Rule-based pricing recommendation engine"""
    
    # Base prices per unit (kg) for different material categories
    BASE_PRICES = {
        MaterialCategory.METAL: 50.0,
        MaterialCategory.PLASTIC: 15.0,
        MaterialCategory.WOOD: 20.0,
        MaterialCategory.TEXTILE: 10.0,
        MaterialCategory.ELECTRONIC: 100.0,
        MaterialCategory.GLASS: 8.0,
        MaterialCategory.PAPER: 5.0,
        MaterialCategory.OTHER: 12.0,
    }
    
    # Quality multipliers
    QUALITY_MULTIPLIERS = {
        'A': 1.5,   # Premium quality
        'B': 1.2,   # Good quality
        'C': 1.0,   # Standard quality
        'D': 0.7,   # Lower quality
    }
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_recommended_price(
        self,
        category: MaterialCategory,
        quantity: float,
        quality_grade: Optional[str] = None,
        certification: Optional[str] = None,
        location_premium: float = 0.0
    ) -> Dict[str, float]:
        """
        Calculate recommended price based on category, quality, and market data
        Returns dict with min, recommended, and max prices
        """
        # Get base price for category
        base_price = self.BASE_PRICES.get(category, 15.0)
        
        # Apply quality multiplier
        quality_mult = 1.0
        if quality_grade in self.QUALITY_MULTIPLIERS:
            quality_mult = self.QUALITY_MULTIPLIERS[quality_grade]
        
        # Apply certification premium
        cert_premium = 1.1 if certification else 1.0
        
        # Volume discount (larger quantities get slight discount)
        volume_discount = 1.0
        if quantity > 1000:
            volume_discount = 0.95
        elif quantity > 5000:
            volume_discount = 0.90
        
        # Calculate market average from recent listings
        market_avg = self._get_market_average(category)
        
        # Combine factors
        calculated_price = base_price * quality_mult * cert_premium * volume_discount
        
        # Adjust based on market data if available
        if market_avg:
            # Weighted average: 60% calculated, 40% market
            recommended_price = (calculated_price * 0.6) + (market_avg * 0.4)
        else:
            recommended_price = calculated_price
        
        # Apply location premium
        recommended_price *= (1 + location_premium)
        
        return {
            'min_price': round(recommended_price * 0.85, 2),
            'recommended_price': round(recommended_price, 2),
            'max_price': round(recommended_price * 1.20, 2),
            'market_average': round(market_avg, 2) if market_avg else None,
            'confidence': 'high' if market_avg else 'medium'
        }
    
    def _get_market_average(self, category: MaterialCategory) -> Optional[float]:
        """Get average price from recent listings in the same category"""
        result = self.db.query(
            func.avg(Listing.price_per_unit)
        ).filter(
            Listing.category == category,
            Listing.status == 'active'
        ).scalar()
        
        return float(result) if result else None
    
    def predict_demand(self, category: MaterialCategory) -> Dict[str, any]:
        """Simple demand prediction based on active listings and matches"""
        active_count = self.db.query(Listing).filter(
            Listing.category == category,
            Listing.status == 'active'
        ).count()
        
        # Simple heuristic: low supply = high demand
        if active_count < 5:
            demand_level = "high"
            price_trend = "increasing"
        elif active_count < 15:
            demand_level = "medium"
            price_trend = "stable"
        else:
            demand_level = "low"
            price_trend = "decreasing"
        
        return {
            'category': category.value,
            'demand_level': demand_level,
            'price_trend': price_trend,
            'active_listings': active_count
        }
