import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson
from datetime import datetime
from branca.element import Element

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

    # Add the TimestampedGeoJson layer with adjusted options
    timestamped_geojson = TimestampedGeoJson(
        data=geojson,
        period='P1D',  # Time interval for the slider (1 Day)
        add_last_point=True,
        auto_play=True,
        loop=False,  # We'll handle looping in custom JavaScript
        max_speed=3000,  # Increase max_speed for faster playback
        loop_button=True,
        date_options='YYYY-MM-DD',
        time_slider_drag_update=True,
        transition_time=3000,  # Decrease transition time for faster animation
    )

    # Add the layer to the map
    timestamped_geojson.add_to(m)

    # Add custom JavaScript to implement the boomerang effect
    boomerang_js = """
    <script>
    var td_player = document.getElementsByClassName('leaflet-control-timecontrol')[0].td_player;
    var originalNextTime = td_player._getNextTime.bind(td_player);
    var originalPrevTime = td_player._getPrevTime.bind(td_player);
    var direction = 'forward';

    td_player._step = function() {
        if (!this._timeDimension) {
            return;
        }

        var currentTime = this._timeDimension.getCurrentTimeIndex();
        var maxTime = this._timeDimension.getAvailableTimes().length - 1;

        if (direction === 'forward') {
            var nextTime = originalNextTime(1);
            if (nextTime > maxTime) {
                direction = 'backward';
                nextTime = originalPrevTime(1);
            }
        } else {
            var nextTime = originalPrevTime(1);
            if (nextTime < 0) {
                direction = 'forward';
                nextTime = originalNextTime(1);
            }
        }

        this._timeDimension.setCurrentTimeIndex(nextTime);
    };
    </script>
    """
    m.get_root().html.add_child(Element(boomerang_js))

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
