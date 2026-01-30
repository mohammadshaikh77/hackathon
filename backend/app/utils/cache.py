from redis import Redis
from app.core.config import settings
from typing import Optional
import json


class RedisCache:
    def __init__(self):
        self.redis_client: Optional[Redis] = None
    
    def connect(self):
        """Connect to Redis"""
        try:
            self.redis_client = Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                decode_responses=True
            )
            self.redis_client.ping()
        except Exception as e:
            print(f"Redis connection failed: {e}")
            self.redis_client = None
    
    def get(self, key: str) -> Optional[dict]:
        """Get value from cache"""
        if not self.redis_client:
            return None
        try:
            value = self.redis_client.get(key)
            return json.loads(value) if value else None
        except Exception:
            return None
    
    def set(self, key: str, value: dict, expire: int = 300):
        """Set value in cache with expiration (default 5 minutes)"""
        if not self.redis_client:
            return
        try:
            self.redis_client.setex(key, expire, json.dumps(value))
        except Exception:
            pass
    
    def delete(self, key: str):
        """Delete key from cache"""
        if not self.redis_client:
            return
        try:
            self.redis_client.delete(key)
        except Exception:
            pass
    
    def clear_pattern(self, pattern: str):
        """Clear all keys matching pattern"""
        if not self.redis_client:
            return
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
        except Exception:
            pass


# Global cache instance
cache = RedisCache()
