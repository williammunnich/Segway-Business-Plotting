import requests
from datetime import datetime

def get_wayback_snapshots(url):
    # Wayback Machine CDX API endpoint
    cdx_api_url = f"http://web.archive.org/cdx/search/cdx?url={url}&output=json&fl=timestamp&collapse=digest"

    try:
        # Send a request to the CDX API
        response = requests.get(cdx_api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the response JSON
        data = response.json()
        
        # Check if snapshots are available
        if len(data) > 1:
            # Exclude the header row and extract timestamps
            timestamps = [entry[0] for entry in data[1:]]
            
            # Convert and print each timestamp as a readable date and time
            print(f"Snapshots for {url}:")
            for ts in timestamps:
                snapshot_date = datetime.strptime(ts, "%Y%m%d%H%M%S")
                print(snapshot_date.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            print("No snapshots found on the Wayback Machine.")

    except requests.RequestException as e:
        print(f"Error accessing Wayback Machine API: {e}")

# Example usage
get_wayback_snapshots("www.ActionSegwayTours.com")
