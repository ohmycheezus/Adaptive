import requests
import pyowm
import os


owm = pyowm.OWM(os.environ.get('OPENW'))


def cityweather(city):
    your_city = city.strip()
    observation = owm.weather_at_place(your_city)
    w = observation.get_weather()
    return w.get_temperature(unit='celsius')['temp']
