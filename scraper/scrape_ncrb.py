import os
import requests
from bs4 import BeautifulSoup

# Function to download PDF links for a given year

def download_pdf_links(year):
    # Construct the URL for the selected year's NCRB suicide data
    base_url = f"https://ncrb.gov.in/accidental-deaths-suicides-in-india-table-content.html?year={year}&category="
    # Sends HTTP GET request to fetch the webpage content
    response = requests.get(base_url)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    # Extract all anchor tags with href attributes
    links = soup.find_all("a", href=True)
    # Create directory to store raw PDF files for the year (if it doesn't exist)
    os.makedirs(f"raw/{year}", exist_ok=True)

    for link in links:
        href = link['href']
        # Check for PDF files with "state-ut-city" in filename
        if "state-ut-city" in href and href.endswith(".pdf"):
            pdf_url = href if href.startswith("http") else "https://ncrb.gov.in" + href
# Extracts the PDF file name from the URL
            pdf_name = pdf_url.split("/")[-1]
            print(f"Downloading {pdf_name}...")
            # Send request to download the PDF file
            pdf_response = requests.get(pdf_url)
            # Save the PDF file to the corresponding raw folder
            with open(f"raw/{year}/{pdf_name}", "wb") as f:
                f.write(pdf_response.content)

if __name__ == "__main__":
    # collects simalarly every year
    for year in [2021, 2022]:
        download_pdf_links(year)
