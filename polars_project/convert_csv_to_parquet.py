import polars as pl
import os

# Define root-level directories
root_dir = os.getcwd()
data_dir = os.path.join(root_dir, "data")
parquet_dir = os.path.join(root_dir, "parquet")

# Create output folder if it doesn't exist
os.makedirs(parquet_dir, exist_ok=True)

# Loop through all files in the data folder
for filename in os.listdir(data_dir):
    # Process only CSV files
    if filename.endswith(".csv"):
        csv_path = os.path.join(data_dir, filename)

        # Create corresponding .parquet file name
        base_name = os.path.splitext(filename)[0]  # removes ".csv"
        parquet_path = os.path.join(parquet_dir, base_name + ".parquet")

        # Read CSV using Polars
        df = pl.read_csv(csv_path)

        # Write to Parquet in the output folder
        df.write_parquet(parquet_path)

        # Print confirmation
        print(f"Converted: {csv_path} → {parquet_path}")
