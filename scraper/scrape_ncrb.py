import os
import requests
from bs4 import BeautifulSoup

def download_pdf_links(year):
    base_url = f"https://ncrb.gov.in/accidental-deaths-suicides-in-india-table-content.html?year={year}&category="
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.find_all("a", href=True)
    os.makedirs(f"raw/{year}", exist_ok=True)

    for link in links:
        href = link['href']
        if "state-ut-city" in href and href.endswith(".pdf"):
            pdf_url = href if href.startswith("http") else "https://ncrb.gov.in" + href

            pdf_name = pdf_url.split("/")[-1]
            print(f"Downloading {pdf_name}...")
            pdf_response = requests.get(pdf_url)
            with open(f"raw/{year}/{pdf_name}", "wb") as f:
                f.write(pdf_response.content)

if __name__ == "__main__":
    for year in [2021, 2022]:
        download_pdf_links(year)
