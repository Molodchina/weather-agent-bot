import logging
from typing import Dict
from pydantic import Field

from langchain.tools import tool
from langchain_gigachat.tools.giga_tool import giga_tool

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_gigachat.chat_models import GigaChat
from langchain.schema import HumanMessage

from infrastructure.config import settings
from infrastructure.redis_client import redis_cache

from .few_shot_examples import *
from domain.services.weather_service import WeatherService


logger = logging.getLogger(__name__)

@giga_tool(few_shot_examples=get_current_weather_examples)
def get_current_weather_by_city_name(
    city: str = Field(description="Название города"),
) -> str:
    """
    Функция для получения текущей погоды в указанном городе.
    """
    if city == "none":
        return "Из какого вы города?"

    weather = redis_cache.get(city)
    logger.info(f"Weather for {city} {'not' * (not weather)} found in cache")
    
    if not weather:
        weather = WeatherService.get_current_weather_by_city_name(city, settings.WEATHER_API_KEY)
        logger.info(f"Weather for {city} fetched from API: {weather}")

        redis_cache.set(city, weather)

    return weather

@giga_tool(few_shot_examples=get_city_name_by_coords_examples)
def get_current_weather_by_coords(
    latitude: str = Field(description="Широта города"),
    longitude: str = Field(description="Долгота города")
) -> str:
    """
    Функция для получения текущей погоды в указанных координатах с учетом знака координат.
    """
    if latitude == "none" or longitude == "none":
        return "Из какого вы города?"

    city = f"{latitude},{longitude}"
    weather = redis_cache.get(city)
    logger.info(f"Weather for {city} {'not' * (not weather)} found in cache")

    if not weather:
        weather = WeatherService.get_current_weather_by_coords(latitude, longitude, settings.WEATHER_API_KEY)
        logger.info(f"Weather for {city} fetched from API: {weather}")
        redis_cache.set(city, weather)

    return weather


class GigaChainClient:
    SYSTEM_PROMPT = (
        "Вы дружелюбный специалист по прогнозированию погоды. "
        "Вы знаете, что пользователь, возможно, уже указывал свой город ранее. "
        "Если пользователь еще не указал город или это неясно, спросите его: 'Из какого вы города?' "
        "Если пользователю погода неинтересна, а он просто делится информацией, просто поблагодари его за информацию."
        "Как только у вас будет четкое название города, обратитесь к API погоды, чтобы узнать текущую погоду. "
        "После получения данных о погоде представьте их в сжатом, удобочитаемом формате. "
        "Если пользователь спросит что-то, не связанное с погодой, вежливо ответьте, что вы можете помочь только с погодой."
    )

    def __init__(self):
        self._config = lambda id: {"configurable": {"thread_id": id}}
        self._tools = [get_current_weather_by_city_name, get_current_weather_by_coords]

        self._model = GigaChat(
            credentials=settings.GIGACHAIN_API_KEY,
            model=settings.GIGACHAIN_MODEL_NAME,
            verify_ssl_certs=False
        )
        self._model = self._model.bind_functions(self._tools)
        self._agent = create_react_agent(
            self._model,
            tools=self._tools,
            checkpointer=MemorySaver(),
            prompt=GigaChainClient.SYSTEM_PROMPT
        )

    async def chat(self, id, text: str) -> Dict[str, str]:
        """
        Отправляет сообщение в GigaChat и возвращает ответ.
        """

        try:
            response = self._agent.invoke(
                {"messages": [HumanMessage(content=text)]}, self._config(id)
            )
            logger.info(f"GigaChainClient.chat response: {response}")

            return {"content": response["messages"][-1].content}
        
        except Exception as e:
            logger.exception(f"GigaChainClient.chat exception: {e}")
            raise
