import os
import requests

# Retrieve the API key from the environment variable
api_key = os.environ.get('API_KEY')

# Print the API key for verification
# print(f"API Key: {api_key}")

# Prompt the user for the desired location (city or ZIP code)
location = input("Enter the city name or ZIP code: ")

# Determine if the location is a ZIP code or city
if location.isdigit():
    # If the location is a ZIP code
    url = f'https://api.openweathermap.org/data/2.5/weather?zip={location}&appid={api_key}&units=metric'
else:
    # If the location is a city name
    url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'

# Send the GET request to the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Extract and display weather information
    weather_condition = data['weather'][0]['main']
    temperature_celsius = data['main']['temp']
    temperature_fahrenheit = (temperature_celsius * 9/5) + 32
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    print(f"Weather in {location}:")
    print(f"Weather Condition: {weather_condition}")
    print(f"Temperature: {temperature_celsius}°C / {temperature_fahrenheit}°F")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")
else:
    print('Request failed with status code:', response.status_code)
