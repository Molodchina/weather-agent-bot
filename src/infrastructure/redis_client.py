import logging
import redis

from infrastructure.config import settings


logger = logging.getLogger(__name__)

redis_cache = redis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True
)
