import datetime
import requests
from keys import CALENDAR_API_KEY
import pandas as pd

import openmeteo_requests
import requests_cache
from retry_requests import retry

def is_holiday():
    base_url = "https://calendarific.com/api/v2/holidays"
    today = datetime.datetime.now()
    params = {'api_key': CALENDAR_API_KEY,
              'country': 'se',
              'day': today.day,
              'month': today.month,
              'year': today.year}
    encoder = {'Clock change/Daylight Saving Time': 1,
               'Christian': 2,
               'Public holiday': 3,
               'De facto holiday': 4,
               'Season': 5,
               'De facto and Bank holiday': 6,
               'Observance': 7,
               'De facto half holiday': 8}
    
    response = requests.get(base_url, params=params)
    holiday = response.json()['response']['holidays']
    if len(holiday) == 0:
        return 0
    else:
        return encoder[holiday[0]['primary_type']]

def get_weather(coordinates):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    latitude,longitude = coordinates
    today = datetime.datetime.now().date().isoformat()
    features = ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "wind_speed_10m_max", "wind_direction_10m_dominant"]

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "start_date": today,
        "end_date": today,
        "latitude": latitude,
        "longitude": longitude,
        "daily": features
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    daily = response.Daily()

    df = pd.DataFrame([], columns=features)
    date = pd.to_datetime(daily.Time(), unit="s")
    now = datetime.datetime.now()
    date = date.replace(second=0, microsecond=0, minute=0, hour=now.hour) + datetime.timedelta(hours=now.minute//30)
    
    df.loc[date] = [daily.Variables(i).ValuesAsNumpy()[0] for i in range(len(features))]

    return df

if __name__ == '__main__':
    coordinates = 59.34318, 18.05141

    print(get_weather(coordinates))
    print(is_holiday())