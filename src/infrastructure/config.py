import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Telegram
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "")
    
    # GigaChain
    GIGACHAIN_API_KEY: str = os.getenv("GIGACHAIN_API_KEY", "")
    GIGACHAIN_MODEL_NAME: str = os.getenv("GIGACHAIN_MODEL_NAME", "GigaChat-Lite")
    GIGACHAIN_API_URL: str = os.getenv("GIGACHAIN_API_URL", "https://api.gigachain.ai/v1/chat")

    # Weather
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")
    WEATHER_API_URL: str = os.getenv("WEATHER_API_URL", "http://api.openweathermap.org/data/2.5/weather")

    # PostgreSQL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    # POSTGRES_USER: str = os.getenv("POSTGRES_USER", "botuser")
    # POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "botpassword")
    # POSTGRES_DB: str = os.getenv("POSTGRES_DB", "weatherbot")
    # POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    # POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "")
    # REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    # REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))

    # Общие
    MAX_HISTORY_LENGTH: int = int(os.getenv("MAX_HISTORY_LENGTH", 20))

settings = Settings()
