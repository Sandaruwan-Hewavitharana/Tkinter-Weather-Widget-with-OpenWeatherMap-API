import tkinter as tk
from tkinter import font, ttk
from PIL import Image, ImageTk
import requests

# OpenWeatherMap API details
API_KEY = "ENTER_API"
CURRENT_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

# Predefined list of cities with their names and coordinates
cities = {
    "New York": "New York",
    "Los Angeles": "Los Angeles",
    "London": "London",
    "Tokyo": "Tokyo",
    "Paris": "Paris",
    "Sydney": "Sydney",
    "Moscow": "Moscow",
    "Rio de Janeiro": "Rio de Janeiro",
    "Mumbai": "Mumbai",
    "Cape Town": "Cape Town",
}

# Function to fetch current weather data
def fetch_current_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(CURRENT_WEATHER_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to fetch 6-day weather forecast
def fetch_forecast(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(FORECAST_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to update the weather information in the GUI
def update_weather():
    city = city_combobox.get()
    current_data = fetch_current_weather(city)
    forecast_data = fetch_forecast(city)
    
    if current_data and forecast_data:
        # Update today's weather
        temp_label.config(text=f"{current_data['main']['temp']}°C")
        condition_label.config(text=current_data['weather'][0]['description'].capitalize())
        icon_code = current_data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_image = ImageTk.PhotoImage(Image.open(requests.get(icon_url, stream=True).raw))
        icon_label.config(image=icon_image)
        icon_label.image = icon_image  # Keep a reference to avoid garbage collection

        # Update the 6-day forecast
        for i in range(6):
            forecast_day = forecast_data['list'][i * 8]  # Get the weather at noon for each day
            day_temp = forecast_day['main']['temp']
            day_condition = forecast_day['weather'][0]['description'].capitalize()
            day_icon_code = forecast_day['weather'][0]['icon']
            day_icon_url = f"http://openweathermap.org/img/wn/{day_icon_code}.png"
            day_icon_image = ImageTk.PhotoImage(Image.open(requests.get(day_icon_url, stream=True).raw))

            forecast_labels[i]['temp'].config(text=f"{day_temp}°C")
            forecast_labels[i]['condition'].config(text=day_condition)
            forecast_labels[i]['icon'].config(image=day_icon_image)
            forecast_labels[i]['icon'].image = day_icon_image
    else:
        temp_label.config(text="N/A")
        condition_label.config(text="Error fetching data")

# Set up the main application window
root = tk.Tk()
root.title("Weather Widget")
root.geometry("400x600")  # Size suitable for a desktop widget
root.configure(bg='#1E1E1E')  # Dark background

# Load Poppins font (requires font installation on the system)
poppins = font.Font(family="Poppins", size=12)

# City selection dropdown (combobox)
city_combobox = ttk.Combobox(root, values=list(cities.keys()), font=poppins)
city_combobox.pack(pady=10)
city_combobox.set("Select a city")  # Default placeholder

# Fetch Weather button
fetch_button = tk.Button(root, text="Get Weather", command=update_weather, font=poppins, bg='#4CAF50', fg='white')
fetch_button.pack(pady=5)

# Weather icon
icon_label = tk.Label(root, bg='#1E1E1E')
icon_label.pack(pady=10)

# Today's Temperature display
temp_label = tk.Label(root, text="Temperature", font=poppins, fg='white', bg='#1E1E1E')
temp_label.pack()

# Today's Condition display
condition_label = tk.Label(root, text="Condition", font=poppins, fg='white', bg='#1E1E1E')
condition_label.pack()

# Frame for the 6-day forecast
forecast_frame = tk.Frame(root, bg='#1E1E1E')
forecast_frame.pack(pady=10, fill=tk.BOTH, expand=True)

forecast_labels = []
for i in range(6):
    day_frame = tk.Frame(forecast_frame, bg='#2E2E2E')
    day_frame.pack(pady=5, padx=10, fill=tk.X)

    icon = tk.Label(day_frame, bg='#2E2E2E')
    icon.pack(side=tk.LEFT, padx=10)

    temp = tk.Label(day_frame, text="Temp", font=poppins, fg='white', bg='#2E2E2E')
    temp.pack(side=tk.LEFT, padx=10)

    condition = tk.Label(day_frame, text="Condition", font=poppins, fg='white', bg='#2E2E2E')
    condition.pack(side=tk.LEFT, padx=10)

    forecast_labels.append({'icon': icon, 'temp': temp, 'condition': condition})

# Start the application
root.mainloop()
