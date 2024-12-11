import requests
from keys import TOMTOM_API_KEY

def get_traffic_flow(api_key, coordinates, zoom=10):
    """
    Fetch traffic flow information for a specific location using TomTom Traffic API.

    :param api_key: Your TomTom API key.
    :param coordinates: Tuple containing latitude and longitude of the location (latitude, longitude).
    :param zoom: Zoom level for traffic data granularity (optional, default is 10).
    :return: JSON response containing traffic flow information or an error message.
    """
    base_url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/"
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

if __name__ == "__main__":
    # Replace with your TomTom API Key
    TOMTOM_API_KEY = "zJT5UBCDtRKSWwsbGp6LWjcQcIi0IcdV"

    # Coordinates for the location (latitude, longitude)
    location_coordinates = (52.5200, 13.4050)  # Example: Berlin, Germany

    # Fetch traffic flow information
    response = get_traffic_flow(TOMTOM_API_KEY, location_coordinates)

    # Display the result
    if "error" in response:
        print(f"Error fetching traffic data: {response['error']}")
    else:
        print("Traffic Flow Information:")
        print(response)
        response.raise_for_status()  # Raise HTTPError for bad responses
        traffic_data = response.json()
        print(traffic_data)
