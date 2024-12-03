Tour Scraping and Visualization Project

This repository contains a set of tools for scraping tour information, processing the data, and visualizing it on an interactive map. The project includes a working professional file (index.html) that is ready to use, featuring a polished interface with an embedded map for showcasing tour data dynamically.

The project is divided into three main components:
	1.	Data Collection: Scraping initial and detailed data from a website.
	2.	Data Processing: Producing comprehensive information from the scraped data.
	3.	Visualization: Creating an interactive map to display the tour data dynamically.

Table of Contents

	•	Working Professional File
	•	Getting Started
	•	Workflow
	•	Scripts Overview
	•	Data Collection
	•	Data Processing
	•	Data Visualization
	•	Output
	•	Dependencies
	•	License
	•	Future Enhancements

Working Professional File

The project includes a ready-to-use index.html file designed for a polished user experience. It features:
	•	A professional layout.
	•	An embedded interactive map (tours_map.html) displayed seamlessly using an iframe.
	•	Clean design and user-friendly presentation.

You can open index.html directly in your browser to explore the functionality without additional setup. This file is ideal for showcasing the results of your scraping and visualization efforts.

Getting Started

To begin working with the project, clone this repository and ensure you have the necessary dependencies installed. The project uses Python for data collection and processing, and HTML/CSS for visualization.

git clone [repository-url]
cd [repository-directory]

Workflow

	1.	Run link_scraper_v2.py:
	•	Gathers initial tour links and generates a CSV file containing valid links.
	2.	Run comprehensive_scrape_v1.py:
	•	Uses the CSV generated in the previous step to perform a detailed scrape and outputs a comprehensive CSV with additional metadata.
	3.	Run map_plot.py:
	•	Processes the data and generates an interactive HTML map (tours_map.html).
	4.	Use index.html:
	•	The final polished file that embeds the generated tours_map.html for seamless visualization.

Scripts Overview

1. Data Collection

File: scraper/link_scraper_v2.py
	•	Purpose: Scrapes valid links from a base URL by iterating through a range of IDs.
	•	Input: None.
	•	Output: A CSV file prefixed with scraped_tour_info_ followed by the current timestamp (e.g., scraped_tour_info_20241203_120000.csv).

How to Run:

python scraper/link_scraper_v2.py

2. Data Processing

File: scraper/comprehensive_scrape_v1.py
	•	Purpose: Reads the CSV generated by link_scraper_v2.py, performs detailed scraping of each link, and extracts metadata such as title, location, company, website, and date information.
	•	Input: The CSV file generated in the previous step.
	•	Output: A detailed CSV file with comprehensive tour information.

How to Run:

python scraper/comprehensive_scrape_v1.py

You will be prompted to provide the input CSV file’s path.

3. Data Visualization

File: plotting_test_area/map_plot.py
	•	Purpose: Generates an interactive map of the tours using the processed data.
	•	Input: The processed CSV file (processed_data.csv).
	•	Output: An HTML file (tours_map.html) displaying the tours on a dynamic map with a timestamp slider.

How to Run:

python plotting_test_area/map_plot.py

Output

	•	tours_map.html: An interactive map showing tour locations with dynamic timestamps. Includes features like a boomerang effect on the time slider.
	•	index.html: A professional website template embedding tours_map.html in an iframe for improved presentation. This file is ready to use immediately.

Dependencies

Ensure you have the following Python libraries installed:
	•	requests
	•	beautifulsoup4
	•	pandas
	•	folium
	•	concurrent.futures
	•	datetime

You can install the dependencies using:

pip install -r requirements.txt

License

This project is licensed under the MIT License, which permits anyone to use, modify, and distribute the software, subject to the conditions outlined in the LICENSE file.

As the original author, I retain the following rights:
	1.	To maintain a copy of the code for personal use and future development.
	2.	To publish a version of this code publicly on my GitHub, scrubbed of any proprietary or identifying information related to private collaborations or usage.

No ongoing support or updates are implied or provided unless explicitly agreed.

For questions or clarifications, contact williammunnich@gmail.com.

Future Enhancements

	•	Add error handling for scraping scripts to better manage network issues.
	•	Automate the integration of tours_map.html into index.html.
	•	Include additional metadata for richer visualization on the map.