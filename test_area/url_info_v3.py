import requests
from bs4 import BeautifulSoup
import csv

def scrape_tour_info(url):
    try:
        # Send a GET request to the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the title of the tour
        title = soup.find('h1').get_text(strip=True) if soup.find('h1') else "Title not found"

        # Extract location using the correct class name
        location = soup.find('span', class_='item-location').get_text(strip=True) if soup.find('span', class_='item-location') else "Location not found"

        # Extract date added using the correct class name
        date_added = soup.find('span', class_='date').get_text(strip=True) if soup.find('span', class_='date') else "Date added not found"

        # Extract date updated using the correct class name
        date_updated = soup.find('span', class_='date hidden-xs').get_text(strip=True) if soup.find('span', class_='date hidden-xs') else "Date updated not found"

        # Extract company name
        company = soup.select_one('aside p:nth-of-type(1)').get_text(strip=True) if soup.select_one('aside p:nth-of-type(1)') else "Company not found"

        # Extract phone number
        phone = soup.select_one('aside ul li:nth-of-type(1)').get_text(strip=True) if soup.select_one('aside ul li:nth-of-type(1)') else "Phone not found"

        # Extract website URL of the tour/business being listed
        website_element = soup.select_one('aside ul li:nth-of-type(2)')
        website = website_element.get_text(strip=True) if website_element else "Website not found"

        # Return the extracted information
        return {
            "Title": title,
            "Location": location,
            "Date Added": date_added,
            "Date Updated": date_updated,
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
            # Read the input CSV file
            csv_reader = csv.reader(infile)
            # Skip the header
            next(csv_reader, None)

            # Write the output CSV file
            csv_writer = csv.DictWriter(outfile, fieldnames=[
                "Title", "Location", "Date Added", "Date Updated", "Company", "Phone", "Website", "Error"
            ])
            csv_writer.writeheader()

            # Process each URL
            for row in csv_reader:
                url = row[0]  # Assuming the URL is in the first column
                print(f"Scraping URL: {url}")
                data = scrape_tour_info(url)
                csv_writer.writerow(data)

        print(f"Scraping completed. Results saved to {output_csv}")

    except FileNotFoundError:
        print(f"File {input_csv} not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {e}")

# File paths (adjust as needed)
input_csv = input("Please provice the path of the csv containing all the tour links: ")
output_csv = 'scraped_tour_info.csv'  # Replace with your desired output CSV file

# Call the function to scrape and save the data
scrape_links_from_csv(input_csv, output_csv)