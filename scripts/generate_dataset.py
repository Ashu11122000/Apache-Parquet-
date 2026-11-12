import numpy as np
import pandas as pd
from pathlib import Path

# Reproducible random data
rng = np.random.default_rng(42)

# Number of records
ROWS = 500_000

# Generate order dates between 2022 and 2025
start_date = np.datetime64("2022-01-01")
end_date = np.datetime64("2026-01-01")

random_days = rng.integers(
    0,
    int((end_date - start_date) / np.timedelta64(1, "D")),
    size=ROWS
)

order_dates = start_date + random_days.astype("timedelta64[D]")

# Generate dataset
df = pd.DataFrame({
    "order_id": np.arange(1, ROWS + 1),
    "customer_id": rng.integers(1000, 50000, ROWS),
    "product": rng.choice(
        ["Laptop", "Mobile", "Tablet", "Monitor", "Keyboard"],
        ROWS
    ),
    "category": rng.choice(
        ["Electronics", "Accessories", "Computers"],
        ROWS
    ),
    "region": rng.choice(
        ["North", "South", "East", "West"],
        ROWS
    ),
    "order_date": pd.to_datetime(order_dates),
    "year": pd.to_datetime(order_dates).year,
    "quantity": rng.integers(1, 10, ROWS),
    "unit_price": np.round(rng.uniform(100, 50000, ROWS), 2)
})

# Calculate sales
df["sales"] = np.round(
    df["quantity"] * df["unit_price"], 2
)

# Save raw CSV dataset
output_path = Path("data/raw/ecommerce_data.csv")
df.to_csv(output_path, index=False)

print("Dataset generated successfully!")
print("----------------------------------")
print("Total records:", len(df))
print("Total columns:", len(df.columns))
print("Dataset shape:", df.shape)
print("\nSample records:")
print(df.head())

print("\nRegion distribution:")
print(df["region"].value_counts())

print("\nYear distribution:")
print(df["year"].value_counts().sort_index())

print("\nCSV file saved at:", output_path)