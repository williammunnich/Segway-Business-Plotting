import csv
import pandas as pd
from geopy.geocoders import Nominatim

def process_csv(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    total_rows = len(df)
    geolocator = Nominatim(user_agent="myGeocoder")

    for index, row in df.iterrows():
        title = row['Title']
        location = row['Location']
        date_added = None  # Set Date Added to None
        date_ended_field = str(row['Date Ended']).strip()
        # Parse Date Ended
        date_ended = pd.to_datetime(date_ended_field, errors='coerce')

        # Geocode location
        try:
            location_geo = geolocator.geocode(location)
            if location_geo:
                latitude = location_geo.latitude
                longitude = location_geo.longitude
            else:
                latitude = None
                longitude = None
        except Exception as e:
            latitude = None
            longitude = None

        # Prepare output dictionary
        output = {
            'Title': title,
            'Latitude': latitude,
            'Longitude': longitude,
            'Date Added': date_added,
            'Date Ended': date_ended
        }

        print(output)
        print(f"Number completed: {index + 1}/{total_rows}")

# Example usage:
process_csv('scraped_data/scraped_tour_info_20241117_212053.csv')
