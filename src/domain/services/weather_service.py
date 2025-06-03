import logging
import requests


logger = logging.getLogger(__name__)

class WeatherService:
    """
    Сервис для получения прогноза погоды через OpenWeatherMap.
    """

    def handle_request(city: str, base_url: str, params: dict, timeout: int = 10) -> str:
        try:
            with requests.get(base_url, params=params, timeout=timeout) as resp:
                data = resp.json()
                if data["cod"] != "404":
                    return f"Текущая погода в городе {data['name']}: {data['weather'][0]['description']}, " \
                           f"температура {data['main']['temp']}°C, ощущается как {data['main']['feels_like']}°C, " \
                           f"влажность {data['main']['humidity']}%, ветер {data['wind']['speed']} м/с"
                
                logger.error(f"Ошибка OpenWeather API: статус {data['cod']}, тело = {data}")
                raise Exception(f"Failed to get weather for {city}: status {data['cod']}")
            
        except Exception as e:
            logger.exception(f"Exception in WeatherService.get_current_weather: {e}")
            raise
    
    @classmethod
    def get_current_weather_by_city_name(cls, city: str, appid: str) -> str:
        """
        Функция для получения текущей погоды в указанном городе.
        """
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": appid,
            "units": "metric",
            "lang": "ru"
        }
        return cls.handle_request(city, base_url, params)
        
    @classmethod
    def get_current_weather_by_coords(cls, lat: str, lon: str, appid: str) -> str:
        """
        Функция для получения текущей погоды в указанных координатах с учетом знака координат.
        """
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": appid,
            "units": "metric",
            "lang": "ru"
        }
        city = "lat={lat},lon={lon}"
        return cls.handle_request(city, base_url, params)
