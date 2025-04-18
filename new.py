import googlemaps
from geopy.distance import geodesic
import folium

# Set your Google Maps API key
API_KEY = "AIzaSyDLvSMi08dftL2BaumBRW1g6gkwKzI3Cuc"

# Initialize the Google Maps client
gmaps = googlemaps.Client(key=API_KEY)

def get_lat_lon(address):
    """
    Get latitude and longitude of a location.
    """
    geocode_result = gmaps.geocode(address)
    lat_lon = geocode_result[0]["geometry"]["location"]
    return lat_lon["lat"], lat_lon["lng"]

def get_directions(origin, destination):
    """
    Get directions from origin to destination using Dijkstra's algorithm.
    """
    directions_result = gmaps.directions(origin, destination, mode="driving")
    route = directions_result[0]["legs"][0]["steps"]
    return route

def visualize_route(route):
    """
    Visualize the route on a map.
    """
    # Create a map centered on the first point of the route
    start_point = (route[0]["start_location"]["lat"], route[0]["start_location"]["lng"])
    map_obj = folium.Map(location=start_point, zoom_start=13)

    # Add route points to the map
    for step in route:
        start = (step["start_location"]["lat"], step["start_location"]["lng"])
        end = (step["end_location"]["lat"], step["end_location"]["lng"])
        folium.Marker(start).add_to(map_obj)
        folium.Marker(end).add_to(map_obj)
        folium.PolyLine([start, end], color="blue").add_to(map_obj)

    # Display the map
    map_obj.save("route_map.html")
    print("Route map saved as 'route_map.html'.")

if __name__ == "__main__":
    # Input source and destination
    source = input("Enter source address: ")
    destination = input("Enter destination address: ")

    # Get route
    route = get_directions(source, destination)

    # Visualize route
    visualize_route(route)