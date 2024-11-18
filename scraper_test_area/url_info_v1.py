import whois
import requests
from datetime import datetime

# Domain to check
domain = "boyne.com"

# WHOIS lookup
try:
    domain_info = whois.whois(domain)
    creation_date = domain_info.creation_date
    expiration_date = domain_info.expiration_date
    print(f"Domain creation date: {creation_date}")
    print(f"Domain expiration date: {expiration_date}")
except Exception as e:
    print(f"Error retrieving WHOIS data: {e}")

# Wayback Machine API endpoint to get the list of snapshots
wayback_cdx_url = f"http://web.archive.org/cdx/search/cdx?url={domain}&output=json&fl=timestamp&collapse=digest"

def get_all_snapshots(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1:
                timestamps = [entry[0] for entry in data[1:]]  # Exclude the header row
                snapshots = sorted([datetime.strptime(ts, "%Y%m%d%H%M%S") for ts in timestamps])
                return snapshots
        else:
            print(f"Error accessing Wayback Machine CDX API: Status code {response.status_code}")
    except Exception as e:
        print(f"Error accessing Wayback Machine CDX API: {e}")
    return []

# Retrieve all snapshots and determine first and last snapshots
snapshots = get_all_snapshots(wayback_cdx_url)

if snapshots:
    first_snapshot_date = snapshots[0]
    last_snapshot_date = snapshots[-1]  # Last entry after sorting
    print(f"First Wayback Machine snapshot: {first_snapshot_date}")
    print(f"Last Wayback Machine snapshot: {last_snapshot_date}")
else:
    print("No snapshots found on the Wayback Machine.")
