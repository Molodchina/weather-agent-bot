WELCOME_MESSAGE = """
Привет! Я ваш дружелюбный бот-прогнозист погоды.
Я могу предоставить вам информацию о текущих погодных условиях для любого города, который вы укажете.

Также я запоинмаю историю диалога и отвечаю на основе предыдущих реплик.
Более того, если Вы поделитесь своим родным городом, то я смогу предоставлять прогноз погоды для него по умолчанию.

Я здесь для того, чтобы помочь вам быть в курсе погоды!
"""

HELP_MESSAGE = """
Сейчас я действую автономно на основе агента на базе GigaChat и API open-meteo.com.
К сожалению, я был создан в качестве демо-версии, поэтому умею выполнять только узкий набор функционала.

Для предложений или замечаний пишите: @amolodchina!
"""

WEATHER_MESSAGE = """
Current weather in {city}:
Temperature: {temperature}°C
Description: {description}
Humidity: {humidity}%
Wind Speed: {wind_speed} m/s
"""

FORECAST_MESSAGE = """
5-day weather forecast for {city}:
"""

FORECAST_DAY_MESSAGE = """
Date: {date}
Temperature: {temperature}°C
Description: {description}
"""

CITY_NOT_FOUND_MESSAGE = """
Sorry, I couldn't find the weather information for "{city}".
Please make sure you spelled the city name correctly.
"""

ERROR_MESSAGE = """
An error occurred while fetching the weather information.
Please try again later.
"""

INVALID_COMMAND_MESSAGE = """
I didn't understand that command.
Please provide a city name to get the current weather, or a city name followed by 'forecast' for the 5-day forecast.
"""