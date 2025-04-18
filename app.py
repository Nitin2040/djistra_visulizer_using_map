import streamlit as st
import googlemaps
import folium
from folium import plugins
from geopy.distance import geodesic
from streamlit_folium import folium_static
import heapq

API_KEY = "AIzaSyDLvSMi08dftL2BaumBRW1g6gkwKzI3Cuc"  
gmaps = googlemaps.Client(key=API_KEY)

# Dijkstra's Algorithm
def dijkstra(nodes, graph, start, end):
    queue = [(0, start)]
    distances = {node: float("inf") for node in nodes}
    distances[start] = 0
    previous = {node: None for node in nodes}

    while queue:
        dist, node = heapq.heappop(queue)
        if node == end:
            break

        for neighbor, cost in graph.get(node, {}).items():
            alt = dist + cost
            if alt < distances[neighbor]:
                distances[neighbor] = alt
                previous[neighbor] = node
                heapq.heappush(queue, (alt, neighbor))

    # Reconstruct path
    path = []
    current = end
    while current:
        path.insert(0, current)
        current = previous[current]

    return path, distances[end]

st.set_page_config(layout="wide")
st.title("🚗 Shortest Route Finder using Dijkstra + Google Maps Steps")

source = st.text_input("Enter Source Address")
destination = st.text_input("Enter Destination Address")
animate = st.checkbox("Animate Route", True)

if source and destination:
    with st.spinner("Fetching directions from Google Maps..."):
        try:
            directions = gmaps.directions(source, destination, mode="driving")
            steps = directions[0]["legs"][0]["steps"]
        except:
            st.error("Error fetching directions. Check API key or address.")
            st.stop()

        # Build nodes and edges
        nodes = []
        graph = {}
        coords = {}

        for i, step in enumerate(steps):
            start = step["start_location"]
            end = step["end_location"]
            start_node = f"n{i}"
            end_node = f"n{i+1}"

            start_coord = (start["lat"], start["lng"])
            end_coord = (end["lat"], end["lng"])

            coords[start_node] = start_coord
            coords[end_node] = end_coord

            dist = geodesic(start_coord, end_coord).km

            # Build undirected edge
            if start_node not in graph:
                graph[start_node] = {}
            if end_node not in graph:
                graph[end_node] = {}

            graph[start_node][end_node] = dist
            graph[end_node][start_node] = dist  
            nodes.extend([start_node, end_node])

        nodes = list(set(nodes))  # Remove duplicates
        start_node = "n0"
        end_node = f"n{len(steps)}"

        # Run Dijkstra
        path, total_dist = dijkstra(nodes, graph, start_node, end_node)

        # Display route info
        st.success(f"Shortest path found through {len(path)} points (Total: {total_dist:.2f} km)")

        # Visualize with Folium
        m = folium.Map(location=coords[start_node], zoom_start=13)

        path_coords = [coords[node] for node in path]
        for i, node in enumerate(path):
            folium.Marker(
                coords[node],
                popup=f"{node}",
                icon=folium.Icon(color="green" if i == 0 else "red" if i == len(path)-1 else "blue")
            ).add_to(m)

        folium.PolyLine(path_coords, color="blue", weight=5).add_to(m)

        if animate:
            plugins.AntPath(path_coords, color="orange", delay=800).add_to(m)

        st.subheader("📍 Path on Map")
        folium_static(m)

        st.subheader("🧭 Intermediate Nodes")
        for node in path[1:-1]:
            st.write(f"{node} - {coords[node]}")
