import logging
from langgraph.checkpoint.memory import MemorySaver


from infrastructure.config import settings
from infrastructure.ai.gigachain_client import GigaChainClient


logger = logging.getLogger(__name__)

class AgentService:
    """
    Главный сервис‑агент, который:
    1. Собирает историю диалога (из Redis и/или PostgreSQL),
    2. Формирует запрос к GigaChain,
    3. Обрабатывает ответ: если нужно спросить город/дату, возвращает соответствующий текст;
       если нужен прогноз — вызывает WeatherService, формирует финальный ответ линейкой LLM.
    4. Сохраняет всё в MessageRepository и кеширует последние сообщения в Redis.
    """

    def __init__(
        self,
        llm_client: GigaChainClient
    ):
        self.llm = llm_client
        self.max_history = settings.MAX_HISTORY_LENGTH

    async def handle_user_message(self, telegram_id: int, text: str) -> str:
        try:
            llm_response = await self.llm.chat(telegram_id, text)

        except Exception as e:
            logger.exception(f"GigaChain error: {e}")
            return "Извините, не удалось получить ответ от AI. Попробуйте чуть позже."

        bot_answer = llm_response.get("content", "")
        logger.info(f"LLM preliminary answer: {bot_answer}")
        return bot_answer
