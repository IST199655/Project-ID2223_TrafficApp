import requests
from shapely.geometry import LineString
from keys import TOMTOM_API_KEY
from OpenStreetMapAPI import get_grid

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
    grid = get_grid(point,radius)
    traffic_map = []
    c = 0

    while len(grid) > 0:
        coordinates = grid.pop().coords.xy
        coordinates = coordinates[1][0],coordinates[0][0]
        response = get_traffic_flow(api_key,coordinates,zoom)

        flow_segment = response.json()['flowSegmentData']
        traffic_map.append(flow_segment)

        line = flow_segment['coordinates']['coordinate']
        line_coords = [(point['longitude'], point['latitude']) for point in line]
        line = LineString(line_coords)
        l_grid = len(grid)
        grid = [p for p in grid if line.distance(p) > 1e-6]
        if l_grid - len(grid) != 0:
            print('eliminated:',l_grid - len(grid))

        c +=1
        print(c, end = '\r')

    return traffic_map

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    coordinates = 59.34318, 18.05141 # Stockholm
    radius = 1000

    traffic_map = get_traffic_map(TOMTOM_API_KEY, coordinates, radius)

    for traffic_info in traffic_map:
        line = traffic_info['coordinates']['coordinate']
        xs = []
        ys = []
        for x in line:
            xs.append(x['latitude'])
            ys.append(x['longitude'])
            
        plt.plot(xs,ys)
    plt.show()

    # # Fetch and decode traffic flow information
    # traffic_info = get_traffic_flow(TOMTOM_API_KEY, coordinates, zoom = 12)
    # traffic_info = traffic_info.json()['flowSegmentData']
    
    # line = traffic_info['coordinates']['coordinate']
    # xs = []
    # ys = []
    # for x in line:
    #     xs.append(x['latitude'])
    #     ys.append(x['longitude'])
        
    # plt.plot(xs,ys)
    # plt.show()
    

