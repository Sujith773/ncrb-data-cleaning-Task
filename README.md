 NCRB Data Cleaning Task

This project scrapes NCRB suicide data from PDF files and cleans it into structured CSV files.

Project Structure

NCRB_Cleaning_Task/
│
├── scraper/
│ └── scrape_ncrb.py # For scraping PDFs
│
├── cleaner/
│ └── clean_ncrb.py # For cleaning data
│
├── raw/
│ ├── 2021/
│ └── 2022/ # Raw PDF files
│
├── processed/
│ ├── suicide_data_2021.csv
│ └── suicide_data_2022.csv # Cleaned CSVs
│
├── requirements.txt
└── README.md

Setup & Execution

1. Clone the repository

git clone https://github.com/Sujith773/ncrb-data-cleaning-Task.git
cd ncrb-data-cleaning-Task

2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate  # For Windows

3. Install required packages
pip install -r requirements.txt

4. Run the scraper (if raw PDFs are not already present)
python scraper/scrape_ncrb.py

5. Run the data cleaner
python cleaner/clean_ncrb.py

Output
Cleaned CSV files will be generated inside the processed/ directory.