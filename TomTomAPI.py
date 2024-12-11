import requests
from keys import TOMTOM_API_KEY
import itertools
import FetchingASync as fetchasync

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
    
def get_vector_flow(api_key, bounding_box, zoom=12):
    grid = 10
    divx = (bounding_box['max_lat'] - bounding_box['min_lat'])/grid
    coord_gridx = [bounding_box['min_lat'] + i*divx for i in range(grid)]
    divy = (bounding_box['max_lng'] - bounding_box['min_lng'])/grid
    coord_gridy = [bounding_box['min_lng'] + i*divy for i in range(grid)]
    
    base_url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/"
    endpoint = f"{zoom}/json"
    urls = []
    for x,y in itertools.product(coord_gridx,coord_gridy):
        params = {
            "key": api_key,
            "point": f"{x},{y}"
        }
        urls.append((f"{base_url}{endpoint}",params))
    
    responses = fetchasync.get(urls)
    responses = [r.json() for r in responses]
    return responses


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import json

    area_bounds = {
        'min_lat': 40.730610,  # Example latitude (bottom left)
        'min_lng': -73.935242, # Example longitude (bottom left)
        'max_lat': 40.748817,  # Example latitude (top right)
        'max_lng': -73.925242, # Example longitude (top right)
    }  # Example: Berlin, Germany

    # Fetch and decode traffic flow information
    traffic_info = get_vector_flow(TOMTOM_API_KEY, area_bounds, zoom = 12)
    coords = set()
    for x in traffic_info:
        coords.add(str(x['coordinates']['coordinate']))
    
    coords = [eval(x) for x in coords]
    print(len(traffic_info),len(coords))
    
    for line in coords:
        xs = []
        ys = []
        for x in line:
            xs.append(x['latitude'])
            ys.append(x['longitude'])
        
        plt.plot(xs,ys)
    plt.show()
    

