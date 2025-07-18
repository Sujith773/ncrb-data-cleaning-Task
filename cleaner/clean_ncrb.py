import os
import camelot
import pandas as pd

def extract_tables_from_pdfs(year):
    input_dir = f"raw/{year}"
    output_dir = f"processed/"
    os.makedirs(output_dir, exist_ok=True)
    all_dfs = []

    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            file_path = os.path.join(input_dir, file)
            print(f"Extracting from: {file_path}")

            tables = camelot.read_pdf(file_path, pages="all", flavor="stream")

            for table in tables:
                df = table.df
                if "State/UT" in df.to_string():
                    all_dfs.append(df)

    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        combined_df.to_csv(f"{output_dir}suicide_data_{year}.csv", index=False)
        print(f"Saved cleaned data to: {output_dir}suicide_data_{year}.csv")

if __name__ == "__main__":
    for year in [2021, 2022]:
        extract_tables_from_pdfs(year)
