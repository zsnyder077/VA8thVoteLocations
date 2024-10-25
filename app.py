import streamlit as st
import folium
from geopy.geocoders import ArcGIS
import pandas as pd
from streamlit_folium import st_folium

# Load the CSV file
df = pd.read_csv('votingLocs.csv')
df.columns = df.columns.str.strip()  # Clean column names

# Display column names for debugging
st.write(df.columns)

# Create a base map
m = folium.Map(location=[38.826671, -77.120943], zoom_start=11.2)

# Add the markers for each row in the dataframe
for index, row in df.iterrows():
    latitude = row['Latitude']  # Use the actual column name for latitude
    longitude = row['Longitude']  # Use the actual column name for longitude
    column1_value = row['Name']  # Use the actual column name for Name
    column2_value = row['Address']  # Use the actual column name for Address
    
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

# Form to input address
st.sidebar.header("Enter Address")
address = st.sidebar.text_input("Address")

if address:
    add_address_marker(address, m)

# Display the map
st_folium(m, width=700, height=500)
