import requests
from keys import TOMTOM_API_KEY
from OpenStreetMapAPI import get_roads

def get_traffic_flow(api_key, coordinates, zoom=12):
    """
    Fetch traffic flow information for a specific location using TomTom Traffic API.

    :param api_key: Your TomTom API key.
    :param coordinates: Tuple containing latitude and longitude of the location (latitude, longitude).
    :param zoom: Zoom level for traffic data granularity (optional, default is 10).
    :return: JSON response containing traffic flow information or an error message.
    """
    base_url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/"
    endpoint = f"{zoom}/json"
    
    # Construct the full request URL
    params = {
        "key": api_key,
        "point": f"{coordinates[0]},{coordinates[1]}"
    }

    try:
        response = requests.get(f"{base_url}{endpoint}", params=params)
        return response
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_traffic_map(api_key, point, radius, zoom = 12):
    roads = get_roads(point,radius)

    # while i =
    traffic_map = None

    return traffic_map

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import json

    coordinates = (40.730610, -73.935242)

    # Fetch and decode traffic flow information
    traffic_info = get_traffic_flow(TOMTOM_API_KEY, coordinates, zoom = 12)
    traffic_info = traffic_info.json()['flowSegmentData']
    
    line = traffic_info['coordinates']['coordinate']
    xs = []
    ys = []
    for x in line:
        xs.append(x['latitude'])
        ys.append(x['longitude'])
        
    plt.plot(xs,ys)
    plt.show()
    

