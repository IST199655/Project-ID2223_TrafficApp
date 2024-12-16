import requests
from shapely.geometry import LineString
from keys import TOMTOM_API_KEY, TOMTOM_API_KEY2, TOMTOM_API_KEY3
from OpenStreetMapAPI import get_grid
import matplotlib.pyplot as plt

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
        midpoint = grid.pop()
        coordinates = midpoint.coords.xy[1][0],midpoint.coords.xy[0][0]
        response = get_traffic_flow(api_key,coordinates,zoom)

        try:
            flow_segment = response.json()['flowSegmentData']
            line = flow_segment['coordinates']['coordinate']
            line_coords = [(point['longitude'], point['latitude']) for point in line]
            line = LineString(line_coords)

            traffic_map.append(flow_segment)

            l_grid = len(grid)
            grid = [p for p in grid if line.distance(p) > 1e-6]
            if l_grid - len(grid) != 0:
                print('eliminated:',l_grid - len(grid))

            c +=1
            print(round(100* c/(c+len(grid))), end = '\r')
        except:
            print(response.json())
    print('num of requests:', c)

    return traffic_map

def get_grid_from_map(map):
    grid = []
    for flow_segment in map:
        line_coords = [(point['longitude'], point['latitude']) for point in flow_segment['coordinates']['coordinate']]
        line = LineString(line_coords)
        midpoint = line.interpolate(0.5 * line.length)
        grid.append(midpoint)

    return grid

import geopandas as gpd

def get_grid_from_map_alt(map):
    """
    Efficiently calculates midpoints of flow segments in map_data.
    
    Parameters:
        map_data (list): List of flow segments, where each segment contains
                         'coordinates' with 'coordinate' as a list of
                         longitude/latitude dictionaries.

    Returns:
        list: List of midpoints (as Shapely Points) in geographic coordinates (latitude/longitude).
    """
    # Step 1: Convert all LineStrings into a GeoDataFrame
    lines = [
        LineString([(point['longitude'], point['latitude']) for point in flow_segment['coordinates']['coordinate']])
        for flow_segment in map
    ]
    gdf = gpd.GeoDataFrame(geometry=lines, crs="EPSG:4326")  # Assume input is in WGS84
    
    # Step 2: Project to a metric CRS for accurate length and interpolation
    gdf_projected = gdf.to_crs(gdf.estimate_utm_crs())
    
    # Step 3: Calculate midpoints in the projected CRS
    midpoints_projected = gdf_projected.geometry.apply(lambda line: line.interpolate(0.5 * line.length))
    
    # Step 4: Reproject midpoints back to geographic coordinates
    midpoints = midpoints_projected.to_crs("EPSG:4326")
    
    return midpoints.tolist()  # Return list of Shapely Point objects


def get_traffic_map_from_grid(api_key,grid, zoom = 12):
    traffic_map = []
    c = 0

    for midpoint in grid:
        coordinates = midpoint.coords.xy[1][0],midpoint.coords.xy[0][0]
        response = get_traffic_flow(api_key,coordinates,zoom)

        try:
            flow_segment = response.json()['flowSegmentData']
            line = flow_segment['coordinates']['coordinate']
            line_coords = [(point['longitude'], point['latitude']) for point in line]
            line = LineString(line_coords)
            traffic_map.append(flow_segment)
        except:
            print(response.json())
        c +=1
        print(round(100* c/len(grid)), end = '\r')
    print('num of requests:', c)

    return traffic_map

def plot_traffic_map(traffic_map, name = 'figures/traffic_map.png'):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for traffic_info in traffic_map:
        line = traffic_info['coordinates']['coordinate']
        xs = []
        ys = []
        for x in line:
            ys.append(x['latitude'])
            xs.append(x['longitude'])
            
        plt.plot(xs,ys)

    ax.set_aspect('equal')

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    plt.savefig(name, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    import pickle

    coordinates = 59.34318, 18.05141 # Stockholm
    radius = 1000
    zoom = 20

    traffic_map = get_traffic_map(TOMTOM_API_KEY, coordinates, radius, zoom = zoom)

    print(len(traffic_map))
    traffic_map = set([str(s) for s in traffic_map])
    traffic_map = [eval(s) for s in list(traffic_map)]
    print(len(traffic_map))

    plot_traffic_map(traffic_map)

    grid = get_grid_from_map(traffic_map)
    traffic_map2 = get_traffic_map_from_grid(TOMTOM_API_KEY,grid, zoom = zoom)

    plot_traffic_map(traffic_map2, name = 'figures/traffic_map2.png')

    with open('variables/grid.pickle', 'wb') as file:
        # Serialize and write the variable to the file
        pickle.dump(grid, file)