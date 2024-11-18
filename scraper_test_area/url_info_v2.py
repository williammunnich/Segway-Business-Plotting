import requests
from datetime import datetime
from bs4 import BeautifulSoup

def fetch_wayback_data(url):
    wayback_api_url = f"http://archive.org/wayback/available"
    
    # Fetch earliest snapshot
    earliest_response = requests.get(wayback_api_url, params={"url": url, "timestamp": "19960101"})
    earliest_snapshot = earliest_response.json().get('archived_snapshots', {}).get('closest', {})
    
    # Fetch latest snapshot
    latest_response = requests.get(wayback_api_url, params={"url": url})
    latest_snapshot = latest_response.json().get('archived_snapshots', {}).get('closest', {})
    
    return {
        "earliest": earliest_snapshot.get('timestamp'),
        "latest": latest_snapshot.get('timestamp'),
    }

def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y%m%d%H%M%S").strftime("%m/%d/%Y")
    except (ValueError, TypeError):
        return None

def check_site_status(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return False, "Site Down"
        
        """# Parse HTML to check if it's populated
        soup = BeautifulSoup(response.text, 'html.parser')
        if not soup.body or len(soup.body.get_text(strip=True)) < 10:  # Adjust content length threshold as needed
            return False, "Blank or Parked"
        """
        return True, "Populated"
    except requests.RequestException:
        return False, "Site Unreachable"

def main(site_url):
    wayback_data = fetch_wayback_data(site_url)
    earliest_date = format_date(wayback_data.get("earliest"))
    latest_date = format_date(wayback_data.get("latest"))
    
    # Check if site is still up and populated
    is_up, status = check_site_status(site_url)
    
    if is_up and status == "Populated":
        return {
            {"Still Up"},
        }
    else:
        return {
            latest_date,
        }

# Example usage
if __name__ == "__main__":
    site = "www.CitySegwayTours.com"
    result = main(site)
    print(result)