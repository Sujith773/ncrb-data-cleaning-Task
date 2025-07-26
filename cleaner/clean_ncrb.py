import os
import camelot
import pandas as pd

# Function to extract and reformat data from all PDF files for a given year
def extract_tables_from_pdfs(year):
    input_dir = f"raw/{year}"  # Define the folder path containing PDF files for the given year
    all_dfs = []  # Initialize list to hold extracted and formatted DataFrames

    # Loop through each PDF file in the year's folder
    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            file_path = os.path.join(input_dir, file)
            print(f"Extracting from: {file_path}")

            # Extract all tables from the PDF using Camelot (stream flavor preferred for structured data)
            tables = camelot.read_pdf(file_path, pages="all", flavor="stream")

            # Iterate over each extracted table
            for table in tables:
                df = table.df  # Get DataFrame from table
                if "State/UT" in df.to_string():  # Filter tables that contain relevant headers
                    df.columns = df.iloc[0]  # Use first row as column headers
                    df = df[1:]  # Remove header row from data
                    df.insert(0, "Year", year)  # Add a new 'Year' column to track the year of the data

                    # Convert wide format into long format if category columns exist
                    if 'State/UT' in df.columns:
                        id_vars = ["Year", "State/UT"]
                        value_vars = [col for col in df.columns if col not in id_vars]
                        melted = pd.melt(df, id_vars=id_vars, value_vars=value_vars,
                                         var_name="category", value_name="value")
                        melted.rename(columns={"State/UT": "state"}, inplace=True)  # Rename for consistency
                        all_dfs.append(melted)  # Append the cleaned table to the list

    return all_dfs  # Return all extracted and formatted DataFrames

if __name__ == "__main__":
    combined_dfs = []  # List to hold combined data across multiple years

    # Loop over each target year and extract tables
    for year in [2021, 2022]:
        combined_dfs.extend(extract_tables_from_pdfs(year))

    # If any data was extracted, merge and save it
    if combined_dfs:
        os.makedirs("processed", exist_ok=True)  # Ensure the processed folder exists
        final_df = pd.concat(combined_dfs, ignore_index=True)  # Merge all yearly data

        # Add 'unit' and 'note' columns with placeholder values (can be manually updated if needed)
        final_df["unit"] = ""
        final_df["note"] = ""

        # Reorder and rename columns to match final format
        final_df = final_df[["Year", "state", "category", "value", "unit", "note"]]
        final_df.columns = ["year", "state", "category", "value", "unit", "note"]

        # Save final cleaned and formatted data to CSV
        final_df.to_csv("processed/suicide_data_cleaned.csv", index=False)
        print("Final cleaned data saved to: processed/suicide_data_cleaned.csv")
