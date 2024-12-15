import datetime
import requests
from keys import CALENDAR_API_KEY

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

if __name__ == '__main__':
    print(is_holiday())