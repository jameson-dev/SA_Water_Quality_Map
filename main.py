import folium
import pandas as pd
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster

# Read Excel file
filename = 'datasets\\water-quality-performance-2024.xlsx'
data = pd.read_excel(filename)
print(f"Reading file: {filename}")

# Show the first few rows to confirm the column names
print("Printing a few rows to confirm headers")
print(data.head())

# Geocoding function for SA Water System Names to coords
geolocator = Nominatim(user_agent="geoapiExcercises")


def geocode_location(location):
    if pd.isna(location) or location.strip() == "":  # Check for NaN or empty locations
        print(f"Skipping geocoding for empty or NaN location: {location}")
        return None, None

    print(f"Geocoding {location}")
    try:
        loc = geolocator.geocode(location)
        if loc:
            print(f"Lat: {loc.latitude}, Long: {loc.longitude}")
            return loc.latitude, loc.longitude
        else:
            print(f"Geocoding failed for {location}: No location found")
            return None, None
    except Exception as e:
        print(f"Error geocoding {location}: {e}")
        return None, None


# Clean System Name rows by removing any parentheses
data['Cleaned System Name'] = data[' System Name'].str.replace(r"\s*\(.*?\)", "", regex=True)

# Remove duplicates based on the cleaned system name
unique_locations = data[['Cleaned System Name']].drop_duplicates()

# Apply geocoding to unique locations
unique_locations[['latitude', 'longitude']] = unique_locations['Cleaned System Name'].apply(
    lambda loc: pd.Series(geocode_location(loc))
)

# Merge the geocoded data with the original data based on the cleaned system name
data = data.merge(unique_locations, on='Cleaned System Name', how='left')

# Add coordinates to DataFrame (No need to re-run geocoding for duplicates)
print("Adding Lat/Long coordinates to DataFrame...")
data[['Latitude', 'Longitude']] = pd.DataFrame(data[['latitude', 'longitude']].values, index=data.index)

# Group data by "System Name" and aggregate parameters
print("Aggregating data")
grouped_data = data.groupby(' System Name').agg(
    parameters=('Parameter', lambda x: '<br>'.join(f"{param}: {value}" for param, value in zip(x, data.loc[x.index, 'Average Value']))),
    latitude=('Latitude', 'first'),
    longitude=('Longitude', 'first')
).reset_index()

# Set map center coordinates
map_center = [-30.5344, 135.6300]

# Generate map
print("Generating map")
m = folium.Map(location=map_center, zoom_start=6)

# Cluster markers for ease and performance
marker_center = MarkerCluster().add_to(m)

print("Adding markers to map")
for _, row in grouped_data.iterrows():

    # Skip rows with NaN coordinates
    if pd.isna(row['latitude']) or pd.isna(row['longitude']):
        print(f"Skipping marker for {row[' System Name']} due to missing coordinates")
        continue

    folium.Marker(
        location=(row['latitude'], row['longitude']),
        popup=row['parameters'],
        icon=folium.Icon(color='blue')
    ).add_to(marker_center)

# Save the map to HTML file
html_file = "index.html"

print(f"Saving HTML file: {html_file}")
m.save(html_file)
