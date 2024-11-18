import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson
from datetime import datetime

def create_interactive_map(data):
    # Create a base map centered globally
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Prepare data for TimestampedGeoJson
    features = []
    for idx, row in data.iterrows():
        if pd.isna(row['Latitude']) or pd.isna(row['Longitude']):
            continue  # Skip if location data is missing

        # Use Date Added or Date Ended as the timestamp
        if not pd.isna(row['Date Added']) and row['Date Added'] != 'NaT':
            timestamp = row['Date Added']
        elif not pd.isna(row['Date Ended']) and row['Date Ended'] != 'NaT':
            timestamp = row['Date Ended']
        else:
            continue  # Skip if no date is available

        # Ensure timestamp is in ISO format
        if isinstance(timestamp, pd.Timestamp):
            timestamp = timestamp.isoformat()
        elif isinstance(timestamp, str):
            try:
                timestamp = pd.to_datetime(timestamp).isoformat()
            except:
                continue  # Skip invalid dates

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [row['Longitude'], row['Latitude']],
            },
            'properties': {
                'time': timestamp,
                'popup': f"Title: {row['Title']}",
                'icon': 'circle',
                'iconstyle': {
                    'fillColor': 'red',
                    'fillOpacity': 0.6,
                    'stroke': 'true',
                    'radius': 5  # Adjust radius as needed
                },
            }
        }
        features.append(feature)

    # Create a GeoJSON object
    geojson = {
        'type': 'FeatureCollection',
        'features': features,
    }

    # Add the TimestampedGeoJson layer
    TimestampedGeoJson(
        geojson,
        period='P1D',  # Time interval for the slider (1 Day)
        add_last_point=True,
        auto_play=True,
        loop=False,
        max_speed=1,
        loop_button=True,
        date_options='YYYY-MM-DD',
        time_slider_drag_update=True,
    ).add_to(m)

    # Save the map to an HTML file
    m.save('tours_map.html')
    print("Interactive map has been saved to 'tours_map.html'.")

def main():
    # Read the processed data from the CSV file
    data = pd.read_csv('processed_data.csv', parse_dates=['Date Added', 'Date Ended'], na_values=['NaT'])
    # Call the function to create the map
    create_interactive_map(data)

if __name__ == '__main__':
    main()
