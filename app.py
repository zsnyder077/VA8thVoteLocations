import streamlit as st
import folium
from geopy.geocoders import ArcGIS
import pandas as pd
from streamlit_folium import st_folium

df = pd.read_csv("votingLocs.csv")

st.image('dBeyer.jpg', use_column_width=True)

# Initialize map
m = folium.Map(location=[38.82667174903602, -77.12094362224809], zoom_start=10.5)

last_red_marker = None

# Function to add address marker
def add_address_marker(address, map_obj):
    global last_red_marker
    geolocator = ArcGIS()

    try:
        location = geolocator.geocode(address, timeout=10)

        if location:
            latitude = location.latitude
            longitude = location.longitude

            popup = folium.Popup(f"<div style='width: 75px;'><strong>{'Your Location'}</strong></div>", max_width=250)

            if last_red_marker:
                map_obj.remove_child(last_red_marker)

            # Add red marker for input location
            last_red_marker = folium.Marker(
                location=[latitude, longitude],
                icon=folium.Icon(icon='star', color='red'),
                popup=popup
            )
            map_obj.add_child(last_red_marker)

        else:
            st.error(f"Address not found: {address}")
    except Exception as e:
        st.error(f"Geocoding error: {e}")

# Add circle markers from data
for index, row in df.iterrows():
    latitude = row[3]
    longitude = row[4]
    column1_value = row[0]
    column2_value = row[1]

    popup_content = f'''
    <div style="width: 200px;">
    <strong>{column1_value}</strong><br>
    {column2_value}
    </div>
    '''

    folium.CircleMarker(
        location=[latitude, longitude],
        radius=4,
        color='dodgerblue',
        fill=True,
        fill_color='lightblue',
        fill_opacity=0.4,
        popup=popup_content
    ).add_to(m)

# Streamlit app UI
st.markdown("<h1 style='text-align: center;'>Find Your Closest Polling Destination!</h1>", unsafe_allow_html=True)

address = st.text_input("Your Address:")

if address:
    add_address_marker(address, m)

# Display the map using streamlit_folium
st_folium(m, width=750, height=500)

