import streamlit as st
import folium
from geopy.geocoders import ArcGIS
import pandas as pd
from streamlit_folium import st_folium

# Load data
df = pd.read_csv("votingLocs.csv")

# Display the image
st.image('dBeyer.jpg', use_column_width=True)

# Initialize map
m = folium.Map(location=[38.82667174903602, -77.12094362224809], zoom_start=11.2)

# Function to add address marker
def add_address_marker(address, map_obj):
    geolocator = ArcGIS()

    try:
        location = geolocator.geocode(address, timeout=10)

        if location:
            latitude = location.latitude
            longitude = location.longitude

            # Popup message for the marker
            popup = folium.Popup(f"<div style='width: 75px;'><strong>{'Your Location'}</strong></div>", max_width=250)

            # Add or update the red marker for the input location
            if 'last_red_marker' in st.session_state:
                # Remove the last marker if it exists
                map_obj.remove_child(st.session_state.last_red_marker)

            # Create a new marker
            red_marker = folium.Marker(
                location=[latitude, longitude],
                icon=folium.Icon(icon='star', color='red'),
                popup=popup
            )
            map_obj.add_child(red_marker)
            # Save the marker in session state for future updates
            st.session_state.last_red_marker = red_marker

        else:
            st.error(f"Address not found: {address}")
    except Exception as e:
        st.error(f"Geocoding error: {e}")

# Add circle markers from data
for index, row in df.iterrows():
    latitude = row[3]  # Use the column index for latitude
    longitude = row[4]  # Use the column index for longitude
    column1_value = row[0]  # Assuming there's a column named 'Name'
    column2_value = row[1]  # Assuming there's a column named 'Description'

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

# Display the map using streamlit_folium
st_folium(m, width=750, height=500)

# Input for address
address = st.text_input("Address:")

if address:
    add_address_marker(address, m)
