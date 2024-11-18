import requests
from bs4 import BeautifulSoup

# Base URL for relative links
base_url = "https://www.segwayguidedtours.com"

def get_links(url, keywords=[]):
    """Scrapes all links from a given URL and filters by keywords."""
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page: {url}")
        return []
    
    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()  # Use a set to avoid duplicates
    
    # Extract and filter links
    for a_tag in soup.find_all('a', href=True):
        link = a_tag['href']
        # Ensure link is fully qualified
        if not link.startswith("http"):
            link = f"{base_url}/{link.lstrip('/')}"
        # Apply keyword filter if specified
        if any(keyword in link for keyword in keywords):
            links.add(link)  # Add to set to ensure uniqueness
    return list(links)  # Convert back to list for further processing if needed

# Step 1: Initial scrape to find only "State" or "Country" links
initial_links = get_links(f"{base_url}/browsetours.cfm", keywords=["State", "Country"])

# Step 2: Scrape each filtered link to get all links on each of those pages,
# only including those that have "Tour", "City", "State", or "Country" in the URL
all_links = set()  # Use a set to collect all unique links
for link in initial_links:
    print(f"Scraping links from: {link}")
    page_links = get_links(link, keywords=["Tour", "City", "State", "Country"])
    all_links.update(page_links)  # Add to set to ensure uniqueness

# Display all unique, filtered links
print("All unique filtered links from secondary pages:")
for link in sorted(all_links):
    print(link)
