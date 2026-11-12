import pandas as pd
from pathlib import Path

# Read the Snappy Parquet file
parquet_file = Path("data/parquet/ecommerce_snappy.parquet")

# Read all columns
df_full = pd.read_parquet(
    parquet_file,
    engine="pyarrow"
)

# Read only selected columns
selected_columns = ["order_id", "region", "sales"]

df_selected = pd.read_parquet(
    parquet_file,
    engine="pyarrow",
    columns=selected_columns
)

# Calculate memory usage
full_memory = df_full.memory_usage(
    deep=True
).sum()

selected_memory = df_selected.memory_usage(
    deep=True
).sum()

# Convert bytes to MB
full_memory_mb = full_memory / (1024 * 1024)
selected_memory_mb = selected_memory / (1024 * 1024)

# Calculate reduction
reduction = (
    (full_memory - selected_memory) / full_memory
) * 100

print("Column Pruning Demonstration")
print("----------------------------")

print("\nFull Dataset:")
print("Columns:", len(df_full.columns))
print(f"Memory Usage: {full_memory_mb:.2f} MB")

print("\nSelected Dataset:")
print("Columns:", len(df_selected.columns))
print("Selected Columns:", selected_columns)
print(f"Memory Usage: {selected_memory_mb:.2f} MB")

print(f"\nMemory Reduction: {reduction:.2f}%")

print("\nSelected Data Sample:")
print(df_selected.head())