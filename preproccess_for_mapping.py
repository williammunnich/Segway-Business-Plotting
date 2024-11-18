import csv
import pandas as pd
from geopy.geocoders import Nominatim

def process_csv(input_file_path, output_file_path):
    # Read the CSV file
    df = pd.read_csv(input_file_path)
    total_rows = len(df)
    geolocator = Nominatim(user_agent="myGeocoder")

    # List to hold output dictionaries
    output_list = []

    for index, row in df.iterrows():
        title = row['Title']
        location = row['Location']

        # Parse Date Added
        date_added_field = str(row['Date Added']).strip()
        # Extract the date part from 'Added: 3/1/04'
        date_added_str = date_added_field.replace('Added:', '').strip()
        date_added = pd.to_datetime(date_added_str, errors='coerce', dayfirst=False)

        # Parse Date Ended
        date_ended_field = str(row['Date Ended']).strip()
        date_ended = pd.to_datetime(date_ended_field, errors='coerce', dayfirst=False)

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

        output_list.append(output)

        print(f"Number completed: {index + 1}/{total_rows}")

    # Write output to CSV file
    output_df = pd.DataFrame(output_list)

    # Convert dates to strings for CSV output
    output_df['Date Added'] = output_df['Date Added'].dt.strftime('%Y-%m-%d')
    output_df['Date Ended'] = output_df['Date Ended'].dt.strftime('%Y-%m-%d')

    # Replace 'NaT' with 'NaT' string
    output_df['Date Added'] = output_df['Date Added'].fillna('NaT')
    output_df['Date Ended'] = output_df['Date Ended'].fillna('NaT')

    # Write to CSV without index and only the specified columns
    output_df.to_csv(output_file_path, index=False, columns=['Title', 'Latitude', 'Longitude', 'Date Added', 'Date Ended'])

# Example usage:
process_csv('scraped_data/scraped_tour_info_20241117_212053.csv', 'processed_data.csv')
