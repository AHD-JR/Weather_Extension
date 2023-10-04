from fastapi import FastAPI, Request, Query, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import requests
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

# Configure CORS to allow all origins (for development purposes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.environ.get('WEATHER_API_KEY')

@app.get('/weather')
def get_user_current_weather(req: Request = None):
    try:
        city_name = get_user_location(req)
        if city_name is None:
            return {"error": "Unable to fetch user location and no city_name provided"}
        
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
        data = fetch_api(api_url)

        return weather_data_serializer(data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

@app.get('/weather/{city_name}')
def get_current_weather(city_name: str):
    try:
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
        data = fetch_api(api_url)

        return weather_data_serializer(data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
def fetch_api(api_url):
    response = requests.get(api_url)
    return response.json()
    
    
def get_user_location(req: Request):
    #user_ip = req.client.host
    user_ip = "157.240.22.35"
    res = requests.get(f"https://ipinfo.io/{user_ip}/json")

    if res.status_code == 200:
        location_data = res.json()
        return location_data['city']
    else:
        return None
    

def weather_data_serializer(data):
    return {
        "City": data["name"],
        "Country": data["sys"]["country"],
        "Description": data["weather"][0]["description"],
        "Temp": data["main"]["temp"],
        "Min_temp": data["main"]["temp_min"],
        "Max_temp": data["main"]["temp_max"],
        "Pressure": data["main"]["pressure"],
        "Humidity": data["main"]["humidity"],
        "Visibility": data["visibility"],
        "Wind": data["wind"]
    }