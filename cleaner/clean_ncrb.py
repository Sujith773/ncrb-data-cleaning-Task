import os
import camelot
import pandas as pd

# Function to extract tables from all PDF files for a given year
def extract_tables_from_pdfs(year):
    input_dir = f"raw/{year}"
    all_dfs = []  # List to hold all extracted dataframes

    # Go through each file in the year's folder
    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):  # Process only PDF files
            file_path = os.path.join(input_dir, file)
            print(f"Extracting from: {file_path}")

            # Read all tables from the PDF using Camelot (stream flavor is better for structured tables)
            tables = camelot.read_pdf(file_path, pages="all", flavor="stream")

            # Iterate over the extracted tables
            for table in tables:
                df = table.df
                # Check if this table contains the keyword "State/UT" to identify matching data
                if "State/UT" in df.to_string():
                    df["Year"] = year  # Add a 'Year' column for year-wise tracking
                    all_dfs.append(df)  # Add the DataFrame to the list

    return all_dfs  # Return all tables extracted from PDFs

if __name__ == "__main__":
    combined_dfs = []  # List to hold data from all years

    # Extract and collect data from both 2021 and 2022
    for year in [2021, 2022]:
        combined_dfs.extend(extract_tables_from_pdfs(year))

    # If any valid data was collected, merge and save it
    if combined_dfs:
        os.makedirs("processed", exist_ok=True)  # Make sure 'processed' folder exists
        final_df = pd.concat(combined_dfs, ignore_index=True)  # Combine all yearly data
        final_df.to_csv("processed/suicide_data_cleaned.csv", index=False)  # Save to single CSV file
        print("Final cleaned data saved to: processed/suicide_data_cleaned.csv")
