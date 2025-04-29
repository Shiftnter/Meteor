import pandas as pd

# Load the data
df = pd.read_csv("weather_forecast.csv")

# Optional: clean column names (remove whitespace, lowercase)
df.columns = df.columns.str.strip().str.lower()

# Check column names after cleaning
print("Column Names:", df.columns.tolist())

# Rename columns for consistency
df = df.rename(columns={
    "temperature (°c)": "temp",
    "humidity (%)": "humidity",
    "weather description": "description",
    "datetime": "date"
})

# Drop duplicate rows if any
df = df.drop_duplicates()

# Handle missing values
print("Missing values:\n", df.isnull().sum())

# Fill numeric NaNs with column mean
df['temp'] = df['temp'].fillna(df['temp'].mean())
df['humidity'] = df['humidity'].fillna(df['humidity'].mean())

# Drop rows where city or date is missing
df = df.dropna(subset=['city', 'date'])

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Drop rows with invalid dates
df = df.dropna(subset=['date'])

# Final cleaned preview
print("\n✅ Cleaned Data:")
print(df.head())

# Save the cleaned version if needed
df.to_csv("weather_forecast_cleaned.csv", index=False)
