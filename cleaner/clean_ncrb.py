import os
import camelot
import pandas as pd

def extract_and_clean_pdf_tables(year):
    input_dir = f"raw/{year}"
    debug_dir = "debug_tables"
    os.makedirs(debug_dir, exist_ok=True)

    all_cleaned_rows = []

    for file in os.listdir(input_dir):
        if file.endswith(".pdf") and "Table 1.3" in file:
            file_path = os.path.join(input_dir, file)
            print(f" Extracting tables from: {file_path}")
            tables = camelot.read_pdf(file_path, pages="all", flavor="stream")

            for i, table in enumerate(tables):
                df = table.df

                # Save raw table for debugging
                debug_file = os.path.join(debug_dir, f"debug_{year}_{file.replace('.pdf', '')}_table{i}.csv")
                df.to_csv(debug_file, index=False)
                print(f"Saved debug table to: {debug_file}")

                # Assign fixed headers manually if structure is known
                expected_columns = [
                    "index",
                    "state",
                    "2020_suicides", "2021_suicides", "suicides_variation",
                    "2020_percent", "2021_percent", "percent_variation",
                    "2020_population", "2021_population", "population_variation"
                ]

                if df.shape[1] >= len(expected_columns):
                    df.columns = expected_columns[:df.shape[1]]
                else:
                    print(f"Skipping {file} table {i} - Unexpected number of columns")
                    continue

                # Remove total/all rows
                df = df[~df["state"].str.contains("total|all", case=False, na=False)]

                for _, row in df.iterrows():
                    state = str(row["state"]).strip()

                    try:
                        suicides = float(str(row["2021_suicides"]).replace(",", ""))
                        population = float(str(row["2021_population"]).replace(",", ""))
                        rate = round(suicides / population, 2) if population > 0 else ""
                    except:
                        rate = ""

                    all_cleaned_rows.extend([
                        {"year": year, "state": state, "category": "Number of Suicides", "value": row["2021_suicides"], "unit": "value in Absolute number", "note": ""},
                        {"year": year, "state": state, "category": "Percentage Share in Total", "value": row["2021_percent"], "unit": "value in Percentage", "note": ""},
                        {"year": year, "state": state, "category": "Projected Mid Year Population", "value": row["2021_population"], "unit": "value in Lakh", "note": ""},
                        {"year": year, "state": state, "category": "Rate of Suicides", "value": rate, "unit": "value in Ratio", "note": "calculated as suicides/population"}
                    ])

    return all_cleaned_rows

if __name__ == "__main__":
    all_years = [2021, 2022]
    all_data = []

    for year in all_years:
        all_data.extend(extract_and_clean_pdf_tables(year))

    final_df = pd.DataFrame(all_data)

    if not final_df.empty:
        os.makedirs("processed", exist_ok=True)
        final_df.to_csv("processed/suicide_data_cleaned.csv", index=False)
        print(" Final cleaned data saved to: processed/suicide_data_cleaned.csv")
    else:
        print(" Final cleaned data is empty. Please check debug tables.")
