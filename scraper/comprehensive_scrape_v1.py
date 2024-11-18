import requests
from bs4 import BeautifulSoup
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import time

def fetch_wayback_data(url, retries=3):
    wayback_api_url = f"http://archive.org/wayback/available"
    for attempt in range(retries):
        try:
            # Fetch earliest snapshot
            earliest_response = requests.get(wayback_api_url, params={"url": url, "timestamp": "19960101"}, timeout=10)
            earliest_snapshot = earliest_response.json().get('archived_snapshots', {}).get('closest', {})

            # Fetch latest snapshot
            latest_response = requests.get(wayback_api_url, params={"url": url}, timeout=10)
            latest_snapshot = latest_response.json().get('archived_snapshots', {}).get('closest', {})

            return {
                "earliest": earliest_snapshot.get('timestamp'),
                "latest": latest_snapshot.get('timestamp'),
            }
        except requests.RequestException as e:
            print(f"Error fetching Wayback data (attempt {attempt + 1}): {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
    return {"earliest": None, "latest": None}


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
        return {"Closed":"Still Up"}
    else:
        return {"Closed":latest_date}


def scrape_tour_info(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('h1').get_text(strip=True) if soup.find('h1') else "Title not found"
        location = soup.find('span', class_='item-location').get_text(strip=True) if soup.find('span', class_='item-location') else "Location not found"
        date_added = soup.find('span', class_='date').get_text(strip=True) if soup.find('span', class_='date') else "Date added not found"
        date_updated = soup.find('span', class_='date hidden-xs').get_text(strip=True) if soup.find('span', class_='date hidden-xs') else "Date updated not found"
        company = soup.select_one('aside p:nth-of-type(1)').get_text(strip=True) if soup.select_one('aside p:nth-of-type(1)') else "Company not found"
        phone = soup.select_one('aside ul li:nth-of-type(1)').get_text(strip=True) if soup.select_one('aside ul li:nth-of-type(1)') else "Phone not found"
        website_element = soup.select_one('aside ul li:nth-of-type(2)')
        website = website_element.get_text(strip=True) if website_element else "Website not found"

        end_date = main(website)

        return {
            "Indexed URL": url,
            "Title": title,
            "Location": location,
            "Date Added": date_added,
            "Date Ended": end_date,
            "Company": company,
            "Phone": phone,
            "Website": website
        }

    except requests.RequestException as e:
        return {"Error": f"Request error: {e}"}
    except Exception as e:
        return {"Error": f"Parsing error: {e}"}


def scrape_links_from_csv(input_csv, output_csv):
    try:
        with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
            csv_reader = csv.reader(infile)
            next(csv_reader, None)  # Skip header row

            csv_writer = csv.DictWriter(outfile, fieldnames=[
                "Indexed URL", "Title", "Location", "Date Added", "Date Ended", "Company", "Phone", "Website", "Error"
            ])
            csv_writer.writeheader()

            urls = [row[0] for row in csv_reader]
            results = []

            print("Starting multithreaded scraping...")

            # Use ThreadPoolExecutor for multithreading
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(scrape_tour_info, url): url for url in urls}

                for future in as_completed(futures):
                    url = futures[future]
                    try:
                        data = future.result()
                        results.append(data)
                        csv_writer.writerow(data)
                        print(f"Completed: {url}")
                    except Exception as e:
                        print(f"Error scraping {url}: {e}")
                        csv_writer.writerow({"Error": str(e)})

            print(f"Scraping completed. Results saved to {output_csv}")

    except FileNotFoundError:
        print(f"File {input_csv} not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {e}")


# File paths (adjust as needed)
input_csv = input("Please provide the path of the CSV containing all the tour links: ")
output_csv = 'scraped_tour_info_' + str(datetime.now().strftime("%Y%m%d_%H%M%S")) + '.csv'

# Run the scraper
scrape_links_from_csv(input_csv, output_csv)