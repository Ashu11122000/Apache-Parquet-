import pandas as pd
from pathlib import Path

# Input CSV file
input_file = Path("data/raw/ecommerce_data.csv")

# Output directory
output_dir = Path("data/parquet")
output_dir.mkdir(parents=True, exist_ok=True)

# Load CSV dataset
df = pd.read_csv(input_file)

print("Dataset loaded successfully!")
print("Records:", len(df))

# Save using Snappy compression
snappy_file = output_dir / "ecommerce_snappy.parquet"

df.to_parquet(
    snappy_file,
    engine="pyarrow",
    compression="snappy",
    index=False
)

# Save using Gzip compression
gzip_file = output_dir / "ecommerce_gzip.parquet"

df.to_parquet(
    gzip_file,
    engine="pyarrow",
    compression="gzip",
    index=False
)

# Calculate file sizes
snappy_size = snappy_file.stat().st_size
gzip_size = gzip_file.stat().st_size

# Convert bytes to MB
snappy_mb = snappy_size / (1024 * 1024)
gzip_mb = gzip_size / (1024 * 1024)

# Display comparison
print("\nCompression Comparison")
print("----------------------")

print(f"Snappy Size: {snappy_mb:.2f} MB")
print(f"Gzip Size:   {gzip_mb:.2f} MB")

if snappy_size > gzip_size:
    difference = (
        (snappy_size - gzip_size) / snappy_size
    ) * 100

    print(f"\nGzip is {difference:.2f}% smaller than Snappy.")

elif gzip_size > snappy_size:
    difference = (
        (gzip_size - snappy_size) / gzip_size
    ) * 100

    print(f"\nSnappy is {difference:.2f}% smaller than Gzip.")

else:
    print("\nBoth files have the same size.")

print("\nParquet files created successfully!")