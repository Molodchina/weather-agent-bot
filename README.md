# Telegram-бот, подсказывающий погоду, на основе GigaChat-агента 

## 🔗 Ссылка на бота

[Перейти к Telegram-боту](https://t.me/gigachat_weather_agent_bot)

---

## 🚀 Запуск бота
1. **Клонируйте репозиторий**  
   ```bash
   git clone git@github.com:Molodchina/weather-agent-bot.git
   cd telegram-weather-bot
   ```
2. **Подготовьте файл окружения**
	- Скопируйте шаблон:
```
cp .env.example .env
```
	- Откройте `.env` и заполните необходимые переменные:
```
TELEGRAM_TOKEN=<ваш_токен_бота>
OPENWEATHER_API_KEY=<ключ_OpenWeatherMap>
REDIS_URL=redis://redis:6379/0
GIGACHAIN_API_KEY=<ключ_GigaChain>
```
	- Убедитесь, что все переменные (особенно пароли и ключи) указаны правильно.

3. **Запуск через Docker Compose**
Убедитесь, что у вас установлены Docker и Docker Compose (версия ≥ 1.29).
```
docker-compose up --build
```
	При первом запуске Docker соберёт образы и запустит два контейнера:
	- redis (хранилище для контекста памяти)
	- bot (сам бот, подключается к Telegram API)

---

## 📝 Основные факты о репозитории

- 🤖 **Telegram-бот, отвечающий на запросы о погоде без явных команд**  
  Бот запоминает город и контекст диалога: достаточно написать «Какая погода?» без повторения города, и бот ответит корректно.

- 🧠 **Контекстная память**  
  • Каждому пользователю хранится своя история диалога (до 20 последних реплик).  
  • Сообщения разделяются по пользователям, чтобы исключить «скрещивание» контекстов.

- 📦 **DDD-архитектура (Domain-Driven Design)**  
  - `domain/` – хэндлеры для сообщений Telegram-бота.  
  - `application/` – бизнес-логика: `AgentService`, `WeatherService`.  
  - `infrastructure/` – технические детали: Redis, GigaChain (LangChain), OpenWeather, логгирование.

- 🤖 **AI-агент на базе GigaChain (LangChain)**  
  • В качестве system-prompt используется:
  	`Вы дружелюбный специалист по прогнозированию погоды...`.
  • Агент умеет приводить названия городов к корректному виду (даже если пользователь сделал опечатку или сократил название) и работать с координатами.

- ☁️ **Интеграция с OpenWeatherMap**  
  - Метод `WeatherService.get_current_weather(city)` возвращает прогноз погоды:
    `city`, `temp`, `feels_like`, `desc`, `humidity`, `wind_speed`.
  - Обработка ошибок (404, 5xx) и вежливые ответы пользователю при недоступности сервиса.

- 📊 **Логирование и трассировка**  
  Все этапы работы (приём сообщений, вызовы LLM/OpenWeather) логируются в формате: `[timestamp][LEVEL][module] <сообщение>`.

- 🧩 **aiogram 3.x**  
- Используется единый хэндлер `@router.message()`: принимает любые текстовые сообщения и передаёт их в `AgentService`.  
- При непредвиденных ошибках бот отсылает generic-ответ: «Произошла ошибка сервера...».

- 🔒 **Безопасность**  
- Все ключи и секреты хранятся в файле `.env` (никаких хардкодов в коде).  
- Экранирование пользовательского ввода, таймауты на запросы, retry-механизмы, валидация промптов для LLM.

- 📦 **Контейнеризация и масштабирование**  
- В проекте есть `Dockerfile` (multi-stage build) и `docker-compose.yml` с тремя сервисами:
  - `postgres`
  - `redis`
  - `bot`

- 🧹 **Профессиональные принципы**  
- Чистый код (соблюдение PEP8, использование аннотаций типов).  
- Чёткое разделение слоёв приложения для быстрой замены компонентов.  
- CI/CD-готовность (есть инструкции для GitHub Actions или GitLab CI).

---

## 📁 Структура репозитория (пример)
```
.
├── docker-compose.yml
├── Dockerfile
├── .env
├── example.env
├── .gitignore
├── README.md
├── requirements.txt
└── src
    ├── application
    │   ├── handlers.py
    │   ├── __init__.py
    │   └── texts.py
    ├── domain
    │   └── services
    │       ├── agent_service.py
    │       └── weather_service.py
    ├── infrastructure
    │   ├── ai
    │   │   ├── few_shot_examples.py
    │   │   ├── gigachain_client.py
    │   │   └── __init__.py
    │   ├── config.py
    │   ├── __init__.py
    │   ├── logging_config.py
    │   ├── redis_client.py
    │   └── weather
    │       ├── __init__.py
    │       └── openweather_client.py
    └── main.py
```
