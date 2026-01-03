import requests
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path("./.env"))
def geo_data():
    response = requests.get("https://api.geoapify.com/v1/ipinfo?&apiKey=%s" % (os.getenv("GEO_API_KEY")))
    if response.status_code == 200:
        r = response.json()
        return [r['location'].get('latitude'), r['location'].get('longitude')]
    return None 

def weather_data(lat, long):
    response = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&units=metric&appid=%s" %
        (lat, long, os.getenv("WEATHER_API_KEY")))

    if response.status_code == 200:
        r = response.json()
        return {
		  "id": r['weather'][0].get('id'),
		  "temp": r['main'].get('temp'),
		  "humidity": r['main'].get('humidity'),
		  "description": r['weather'][0].get('description'),
		  "windSpeed": r['wind'].get('speed'),
		}
    return None 