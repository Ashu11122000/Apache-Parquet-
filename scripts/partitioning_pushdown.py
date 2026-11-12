import pandas as pd
import pyarrow.dataset as ds
from pathlib import Path
import shutil

# Input CSV dataset
input_file = Path("data/raw/ecommerce_data.csv")

# Partitioned output directory
output_dir = Path("data/partitioned/ecommerce_by_region")

# Load dataset
df = pd.read_csv(input_file)

print("Original Dataset")
print("----------------")
print("Total records:", len(df))

# Remove previous output if it exists
if output_dir.exists():
    shutil.rmtree(output_dir)

# Create partitioned Parquet dataset
df.to_parquet(
    output_dir,
    engine="pyarrow",
    compression="snappy",
    partition_cols=["region"],
    index=False
)

print("\nPartitioned Parquet dataset created!")

# Read partitioned dataset using PyArrow
dataset = ds.dataset(
    output_dir,
    format="parquet",
    partitioning="hive"
)

# Define filter conditions
filter_condition = (
    (ds.field("region") == "North") &
    (ds.field("year") == 2024)
)

# Identify matching data fragments
matching_fragments = list(
    dataset.get_fragments(
        filter=filter_condition
    )
)

print("\nPredicate Pushdown")
print("------------------")
print("Matching Parquet fragments:", len(matching_fragments))

for fragment in matching_fragments:
    print("Fragment:", fragment.path)

# Read only matching records and selected columns
table = dataset.to_table(
    columns=["order_id", "region", "year", "sales"],
    filter=filter_condition
)

# Convert result into pandas DataFrame
filtered_df = table.to_pandas()

print("\nFiltered Dataset")
print("----------------")
print("Selected region: North")
print("Selected year: 2024")
print("Matching records:", len(filtered_df))

print("\nSample filtered records:")
print(filtered_df.head())

print("\nPartitioned dataset saved at:")
print(output_dir)