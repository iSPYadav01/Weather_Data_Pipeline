import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

# Set your OpenWeatherMap API key
API_KEY = "6e15cb2537dab4e2a83fd8dbb301e224"
CITIES = ["Gorakhpur", "Bengaluru"]  # Weather forecast for these cities

# Function to fetch weather data from the OpenWeatherMap API
def fetch_weather_data(city):
    """Fetch weather data from OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    # Check if the request was successful
    if data["cod"] == 200:
        weather_data = {
            "city": city,
            "temperature": data["main"]["temp"],
            "pressure": data["main"]["pressure"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "temp_min": data["main"]["temp_min"],  # Minimum temperature
            "temp_max": data["main"]["temp_max"],  # Maximum temperature
            "timestamp": datetime.now()
        }
        return weather_data
    else:
        print(f"Failed to retrieve data for {city}. Error: {data['message']}")
        return None

def save_data_to_csv(weather_data):
    """Appends weather data to a CSV file."""
    output_folder = "data"  # The data will be stored in the 'data' folder
    os.makedirs(output_folder, exist_ok=True)

    # Convert the data to DataFrame
    df = pd.DataFrame([weather_data])

    # Define the path for the CSV file
    file_path = os.path.join(output_folder, 'dataset.csv')

    # Append to CSV file or create a new one if it doesn't exist
    df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)

    print(f"Data for {weather_data['city']} saved to CSV: {file_path}")

def load_and_visualize_data():
    """Visualize weather data for comparison between cities."""
    df = pd.read_csv("data/dataset.csv")

    # Create timestamp for folder based on current 2-hour intervals
    current_time = datetime.now()
    interval_time = (current_time - timedelta(hours=current_time.hour % 2,
                                                minutes=current_time.minute,
                                                seconds=current_time.second,
                                                microseconds=current_time.microsecond))
    timestamp_str = interval_time.strftime("%Y-%m-%d_%H-%M")

    # Create output folder based on the timestamp
    output_folder = os.path.join("output", f"weather_data_{timestamp_str}")
    os.makedirs(output_folder, exist_ok=True)

    # Prepare the figure for combined view of both cities
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))

    # Plot temperature
    axes[0, 0].set_title("Temperature (°C)")
    for city in df['city'].unique():
        city_data = df[df['city'] == city]
        axes[0, 0].plot(city_data['timestamp'], city_data['temperature'], label=city)
    axes[0, 0].set_xlabel("Time")
    axes[0, 0].set_ylabel("Temperature (°C)")
    axes[0, 0].legend()

    # Plot humidity
    axes[0, 1].set_title("Humidity (%)")
    for city in df['city'].unique():
        city_data = df[df['city'] == city]
        axes[0, 1].plot(city_data['timestamp'], city_data['humidity'], label=city)
    axes[0, 1].set_xlabel("Time")
    axes[0, 1].set_ylabel("Humidity (%)")
    axes[0, 1].legend()

    # Plot wind speed
    axes[1, 0].set_title("Wind Speed (m/s)")
    for city in df['city'].unique():
        city_data = df[df['city'] == city]
        axes[1, 0].plot(city_data['timestamp'], city_data['wind_speed'], label=city)
    axes[1, 0].set_xlabel("Time")
    axes[1, 0].set_ylabel("Wind Speed (m/s)")
    axes[1, 0].legend()

    # Plot Min/Max temperatures
    axes[1, 1].set_title("Min & Max Temperature (°C)")
    for city in df['city'].unique():
        city_data = df[df['city'] == city]
        axes[1, 1].plot(city_data['timestamp'], city_data['temp_min'], label=f"{city} Min Temp", linestyle="--")
        axes[1, 1].plot(city_data['timestamp'], city_data['temp_max'], label=f"{city} Max Temp", linestyle="-.")
    axes[1, 1].set_xlabel("Time")
    axes[1, 1].set_ylabel("Temperature (°C)")
    axes[1, 1].legend()

    # Layout and save the plot
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, f"weather_comparison_{timestamp_str}.png"))
    plt.show()

def run_weather_pipeline():
    """Run the entire weather data pipeline."""
    # Fetch and save weather data for all cities
    for city in CITIES:
        weather_data = fetch_weather_data(city)
        if weather_data:
            save_data_to_csv(weather_data)

    # Generate visualizations based on the data
    load_and_visualize_data()

if __name__ == "__main__":
    run_weather_pipeline()
