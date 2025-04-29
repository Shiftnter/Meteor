import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Step 1: Load the data
df = pd.read_csv("weather_forecast.csv")

# Step 2: Clean column names
df.columns = df.columns.str.strip().str.lower()

# Step 3: Rename for easier handling
df = df.rename(columns={
    "temperature (°c)": "temp",
    "humidity (%)": "humidity",
    "weather description": "description",
    "datetime": "date"
})

# Step 4: Drop duplicates
df = df.drop_duplicates()

# Step 5: Handle missing values
df['temp'] = df['temp'].fillna(df['temp'].mean())
df['humidity'] = df['humidity'].fillna(df['humidity'].mean())
df = df.dropna(subset=['city', 'date'])

# Step 6: Convert to datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.dropna(subset=['date'])

# 💡 Add dummy wind_speed column if it's not in the original data
if 'wind_speed' not in df.columns:
    df['wind_speed'] = 0  # or fetch it during data collection if needed

# ✅ Step 7: Normalize the numeric columns
numerical_cols = ['temp', 'humidity', 'wind_speed']
scaler = MinMaxScaler()
df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

# Step 8: Show result
print("Normalized Data:")
print(df.head())

# Optional: Save cleaned and normalized data
df.to_csv("weather_forecast_cleaned_normalized.csv", index=False)
