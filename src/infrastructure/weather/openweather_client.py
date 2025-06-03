import aiohttp
import logging
from infrastructure.config import settings

logger = logging.getLogger(__name__)

class OpenWeatherClient:
    BASE_URL = settings.WEATHER_API_URL
    API_KEY = settings.WEATHER_API_KEY

    @classmethod
    async def fetch(cls, city: str) -> dict:
        params = {
            "q": city,
            "appid": cls.API_KEY,
            "units": "metric",
            "lang": "en"
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(cls.BASE_URL, params=params, timeout=10) as resp:
                    if resp.status != 200:
                        text = await resp.text()
                        logger.error(f"OpenWeather API error {resp.status}: {text}")
                        raise Exception(f"Status {resp.status}")
                    return await resp.json()
            except Exception as e:
                logger.exception(f"Exception in OpenWeatherClient.fetch: {e}")
                raise
