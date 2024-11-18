import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Base URL
base_url = "https://www.segwayguidedtours.com/tour.cfm?Tour="

# Range for suffixes
start, end = 0, 2000

# List to store valid links
valid_links = []

# Function to check each URL
def check_url(i):
    url = f"{base_url}{i}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"Valid link: {url}")
            return url  # Return valid link
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
    return None  # Return None if invalid

# Use ThreadPoolExecutor for multithreading
with ThreadPoolExecutor(max_workers=10) as executor:
    # Schedule the execution of each URL check
    future_to_url = {executor.submit(check_url, i): i for i in range(start, end + 1)}
    
    # Collect results as they complete
    for future in as_completed(future_to_url):
        url = future_to_url[future]
        try:
            result = future.result()
            if result:  # Only add if the result is a valid link
                valid_links.append(result)
        except Exception as exc:
            print(f"Generated an exception: {exc}")

# Save valid links to a text file with the current date and time
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"valid_links_{timestamp}.txt"
with open(filename, "w") as file:
    for link in valid_links:
        file.write(link + "\n")

print(f"\nAll valid links have been saved to {filename}")
