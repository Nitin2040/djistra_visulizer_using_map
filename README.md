# djistra_visulizer_using_map
This Streamlit app allows users to find and visualize the shortest driving route between two real-world addresses using:

Google Maps Directions API for real road data

Dijkstra's Algorithm for computing the shortest path

Folium for interactive map visualization


 # 🔧 Features
Enter any valid source and destination address.

Fetch driving steps from Google Maps.

Construct a graph from stepwise coordinates.

Use Dijkstra's algorithm to compute the shortest path.

Visualize the path on a Folium map.

Animated route display using folium.plugins.AntPath.

 # 📦 Requirements
Install dependencies using pip:

bash
Copy code
pip install streamlit googlemaps geopy folium streamlit-folium

 # 🚀 How to Run
Clone this repository:

bash
Copy code
git clone https://github.com/yourusername/shortest-path-finder.git
cd shortest-path-finder
Replace the placeholder API key in the script:

python
Copy code
API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"
Run the app:

bash
Copy code
streamlit run app.py
