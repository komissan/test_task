import time 
time.sleep(5)
from fastapi import FastAPI
import uvicorn
import requests
from key import API_KEY
import json
from pydantic import BaseModel
import sql
from sql import SessionLocal
import model
import create_db

db = SessionLocal()  

app = FastAPI()

@app.get('/weather/{city}') 
async def get_weather(city:str):
    params = {"q" : city, "appid": API_KEY, "units": "metric", "lang":"ru" }
    response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
    data = json.loads(response.text)
    new_weather_report=model.Item()
    if data['cod']==200:    
        new_weather_report.coord_lat=data['coord']['lat']
        new_weather_report.coord_long=data['coord']['lon'] 
        new_weather_report.weather_id=data['weather'][0]['id']
        new_weather_report.weather_main=data['weather'][0]['main']
        new_weather_report.weather_description=data['weather'][0]['description']
        new_weather_report.main_temp= data['main']['temp']
        new_weather_report.main_feels_like= data['main']['feels_like']
        new_weather_report.main_pressure= data['main']['pressure']
        new_weather_report.main_humidity= data['main']['humidity']
        new_weather_report.main_temp_min= data['main']['temp_min']
        new_weather_report.main_temp_max= data['main']['temp_max']
        if 'sea_level' in data['main'].keys():
            new_weather_report.main_sea_level= data['main']['sea_level']
        if 'grnd_level' in data['main'].keys():
            new_weather_report.main_grnd_level= data['main']['grnd_level']
        new_weather_report.visibility= data['visibility']
        new_weather_report.wind_speed= data['wind']['speed']
        new_weather_report.wind_deg= data['wind']['deg']
        if 'gust' in data['wind'].keys():
            new_weather_report.wind_gust= data['wind']['gust']
        new_weather_report.cloud_all= data['clouds']['all']
        if 'rain' in data.keys():   
            if '1h' in data['rain'].keys():
                new_weather_report.rain_1h= data['rain']['1h']
            if '3h' in data['rain'].keys():
                new_weather_report.rain_3h= data['rain']['3h']
        if 'snow' in data.keys():
            if '1h' in data['snow'].keys():
                new_weather_report.snow_1h= data['snow']['1h']
            if '3h' in data['snow'].keys():
                new_weather_report.snow_3h= data['snow']['3h']
        new_weather_report.dt= data['dt']
        new_weather_report.sys_country= data['sys']['country']
        new_weather_report.sys_sunrise= data['sys']['sunrise']
        new_weather_report.sys_sunset= data['sys']['sunset']
        new_weather_report.timezone= data['timezone']
        new_weather_report.cityname= data['name']
        new_weather_report.cod= data['cod']
        db.add(new_weather_report)
        db.commit()
    else:
        new_weather_report.sys_country= city
        new_weather_report.cod= data['cod']
        db.add(new_weather_report)
        db.commit()
        return ("Wrong city name or the service is unreachable", data['cod'])

    return (data['name'], 
    data['weather'][0]['main'],
    data['weather'][0]['description'],
    ["Temperature:", data['main']['temp']],
    "Wind speed:", data['wind']['speed'],
    )

