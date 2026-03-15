"""Redis caching layer for research results."""
import json
import hashlib
import logging
from typing import Optional, Dict, Any
from datetime import timedelta

logger = logging.getLogger(__name__)

# Redis client (will be initialized if Redis is available)
redis_client = None
CACHE_ENABLED = False

def init_redis():
    """Initialize Redis connection if available."""
    global redis_client, CACHE_ENABLED
    
    try:
        import redis
        from config.settings import settings
        
        if not settings.redis_url or settings.redis_url == "redis://localhost:6379":
            logger.info("⏸️ Redis not configured, caching disabled")
            return
        
        redis_client = redis.from_url(
            settings.redis_url,
            decode_responses=True,
            socket_connect_timeout=2
        )
        
        # Test connection
        redis_client.ping()
        CACHE_ENABLED = True
        logger.info("✅ Redis cache initialized successfully")
        
    except Exception as e:
        logger.warning(f"⚠️ Redis unavailable: {e}. Caching disabled.")
        CACHE_ENABLED = False


def get_cache_key(topic: str, client_email: str = "") -> str:
    """
    Generate cache key from topic and email.
    
    Args:
        topic: Research topic
        client_email: Client email (optional)
        
    Returns:
        Cache key string
    """
    # Normalize topic (lowercase, strip whitespace)
    normalized_topic = topic.lower().strip()
    
    # Create hash of topic for consistent key
    topic_hash = hashlib.md5(normalized_topic.encode()).hexdigest()[:12]
    
    # Include email in key if provided (for personalized results)
    if client_email and client_email != "display@ui.local":
        email_hash = hashlib.md5(client_email.encode()).hexdigest()[:8]
        return f"research:{topic_hash}:{email_hash}"
    
    return f"research:{topic_hash}"


async def get_cached_research(topic: str, client_email: str = "") -> Optional[Dict[str, Any]]:
    """
    Get cached research results.
    
    Args:
        topic: Research topic
        client_email: Client email
        
    Returns:
        Cached research data or None
    """
    if not CACHE_ENABLED or not redis_client:
        return None
    
    try:
        cache_key = get_cache_key(topic, client_email)
        cached_data = redis_client.get(cache_key)
        
        if cached_data:
            logger.info(f"✅ Cache HIT for topic: {topic[:50]}...")
            return json.loads(cached_data)
        
        logger.info(f"❌ Cache MISS for topic: {topic[:50]}...")
        return None
        
    except Exception as e:
        logger.error(f"❌ Redis get error: {e}")
        return None


async def cache_research(
    topic: str,
    client_email: str,
    summary: str,
    citations: list,
    verified: bool,
    ttl_hours: int = 24
) -> bool:
    """
    Cache research results.
    
    Args:
        topic: Research topic
        client_email: Client email
        summary: Research summary
        citations: List of citations
        verified: Verification status
        ttl_hours: Time to live in hours (default 24)
        
    Returns:
        True if cached successfully
    """
    if not CACHE_ENABLED or not redis_client:
        return False
    
    try:
        cache_key = get_cache_key(topic, client_email)
        
        cache_data = {
            "topic": topic,
            "summary": summary,
            "citations": citations,
            "verified": verified,
            "cached_at": str(timedelta(hours=ttl_hours))
        }
        
        # Set with expiration
        redis_client.setex(
            cache_key,
            timedelta(hours=ttl_hours),
            json.dumps(cache_data)
        )
        
        logger.info(f"✅ Cached research for topic: {topic[:50]}... (TTL: {ttl_hours}h)")
        return True
        
    except Exception as e:
        logger.error(f"❌ Redis set error: {e}")
        return False


async def invalidate_cache(topic: str, client_email: str = "") -> bool:
    """
    Invalidate cached research.
    
    Args:
        topic: Research topic
        client_email: Client email
        
    Returns:
        True if invalidated successfully
    """
    if not CACHE_ENABLED or not redis_client:
        return False
    
    try:
        cache_key = get_cache_key(topic, client_email)
        redis_client.delete(cache_key)
        logger.info(f"✅ Invalidated cache for topic: {topic[:50]}...")
        return True
        
    except Exception as e:
        logger.error(f"❌ Redis delete error: {e}")
        return False


def get_cache_stats() -> Dict[str, Any]:
    """
    Get cache statistics.
    
    Returns:
        Dictionary with cache stats
    """
    if not CACHE_ENABLED or not redis_client:
        return {"enabled": False}
    
    try:
        info = redis_client.info("stats")
        
        return {
            "enabled": True,
            "total_keys": redis_client.dbsize(),
            "hits": info.get("keyspace_hits", 0),
            "misses": info.get("keyspace_misses", 0),
            "hit_rate": info.get("keyspace_hits", 0) / max(info.get("keyspace_hits", 0) + info.get("keyspace_misses", 0), 1)
        }
    except Exception as e:
        logger.error(f"❌ Redis stats error: {e}")
        return {"enabled": False, "error": str(e)}
