import streamlit as st
import pandas as pd
import requests
import folium
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# ==========================================
# 1. PAGE SETUP
# ==========================================
st.set_page_config(page_title="Bengaluru EV Optimizer", layout="wide", page_icon="⚡")

st.title("⚡ Smart City EV Charging Station Optimizer")
st.markdown(
    "This application fetches **live EV charging station data** from OpenStreetMap "
    "and applies the **K-Means clustering algorithm** to locate optimal charging hubs across Bengaluru."
)

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
@st.cache_data
def fetch_live_ev_data():
    # Bounding box for Bengaluru
    overpass_query = """
    [out:json][timeout:25];
    (
      node["amenity"="charging_station"](12.75,77.40,13.15,77.80);
      way["amenity"="charging_station"](12.75,77.40,13.15,77.80);
      relation["amenity"="charging_station"](12.75,77.40,13.15,77.80);
    );
    out center;
    """
    headers = {'User-Agent': 'BengaluruEVOptimizer/1.0 (Student Portfolio Project)'}
    
    try:
        response = requests.get("https://overpass-api.de/api/interpreter", params={'data': overpass_query}, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        locations = []
        for element in data.get('elements', []):
            if element['type'] == 'node':
                locations.append({'Latitude': element['lat'], 'Longitude': element['lon']})
            elif 'center' in element:
                locations.append({'Latitude': element['center']['lat'], 'Longitude': element['center']['lon']})
                
        if not locations:
            return pd.DataFrame(), "No data found."
            
        return pd.DataFrame(locations), "Live API Data (OpenStreetMap)"
    except Exception as e:
        return pd.DataFrame(), f"Error fetching data: {e}"

@st.cache_data
def get_address(lat, lon):
    """Converts a latitude and longitude into a readable street/city address."""
    # We must provide a user agent to use the free OpenStreetMap geocoder
    geolocator = Nominatim(user_agent="BengaluruEVOptimizer")
    try:
        # Reverse geocode the exact coordinates
        location = geolocator.reverse((lat, lon), exactly_one=True, timeout=10)
        if location:
            # location.address returns the full street, suburb, city, and zip code
            return location.address
        else:
            return "Address not found"
    except GeocoderTimedOut:
        return "Geocoding service timed out"

# ==========================================
# 3. DATA FETCHING & K-MEANS
# ==========================================
with st.spinner("Fetching live EV data..."):
    df, data_source = fetch_live_ev_data()

if df.empty:
    st.error("Failed to load map data. Please try again later.")
    st.stop()

coordinates = df[['Latitude', 'Longitude']].dropna().values

st.sidebar.header("Model Settings")
k = st.sidebar.slider("Select Number of Clusters (k):", min_value=1, max_value=10, value=3)

# Run K-Means Clustering
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(coordinates)
centroids = kmeans.cluster_centers_

# Generate Addresses for the new Centroids
# We only do this for the optimal hubs so it runs instantly
hub_data = []
with st.spinner("Finding street addresses for proposed stations..."):
    for i, center in enumerate(centroids):
        lat, lon = center[0], center[1]
        address = get_address(lat, lon)
        hub_data.append({
            "Hub": f"Hub {i+1}",
            "Latitude": round(lat, 5),
            "Longitude": round(lon, 5),
            "Street Address": address
        })

results_df = pd.DataFrame(hub_data)

# ==========================================
# 4. VISUALIZATION & OUTPUT
# ==========================================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Geospatial Distribution Map")
    
    map_center = [df['Latitude'].mean(), df['Longitude'].mean()]
    google_map_tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'
    city_map = folium.Map(location=map_center, zoom_start=11, tiles=google_map_tiles, attr='Google')
    
    # Plot existing EV stations
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=4,
            color='#0078FF',
            fill=True,
            fill_opacity=0.5,
            popup="Existing Station"
        ).add_to(city_map)
        
    # Plot optimal hubs WITH real addresses
    for _, row in results_df.iterrows():
        popup_html = f"<b>{row['Hub']}</b><br><br>{row['Street Address']}"
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color='red', icon='star', prefix='fa')
        ).add_to(city_map)
        
    st_folium(city_map, width=720, height=520)

with col2:
    st.subheader("Proposed Locations")
    st.markdown("The algorithm identified the following physical addresses for new infrastructure:")
    
    # Display the table showing the new Street Address column
    st.dataframe(
        results_df[["Hub", "Street Address"]], 
        use_container_width=True, 
        hide_index=True
    )