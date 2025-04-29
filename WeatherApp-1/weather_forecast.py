import requests
import csv
import os
from datetime import datetime

API_KEY = "f4c24f4ea4a8df0d1bb397c1ed7966cf"
CSV_FILE = "weather_forecast.csv"

def fetch_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        print(f"❌ Error fetching data for {city}: {data.get('message', 'Unknown error')}")
        return []

    forecast_data = []
    for entry in data["list"]:
        dt = datetime.fromtimestamp(entry["dt"]).strftime('%Y-%m-%d %H:%M')
        temp = entry["main"]["temp"]
        humidity = entry["main"]["humidity"]
        description = entry["weather"][0]["description"]
        forecast_data.append([city.title(), dt, temp, humidity, description])
    
    return forecast_data

def save_to_csv(forecast):
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["City", "Datetime", "Temperature (°C)", "Humidity (%)", "Weather Description"])
        writer.writerows(forecast)

def main():
    cities = input("Enter cities (comma-separated): ").split(",")
    for city in cities:
        city = city.strip()
        forecast = fetch_forecast(city)
        if forecast:
            save_to_csv(forecast)
            print(f" Data for {city.title()} added to {CSV_FILE}")

if __name__ == "__main__":
    main()
