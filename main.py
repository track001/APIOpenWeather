import os
import requests

# Retrieve the API key from the environment variable
api_key = os.environ.get('API_KEY')

# Print the API key for verification
print(f"API Key: {api_key}")

# Prompt the user for the desired city
city = input("Enter the city name: ")

# Set up the API endpoint URL
url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

# Send the GET request to the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Extract and display the weather information
    weather_condition = data['weather'][0]['main']
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    print(f"Weather in {city}:")
    print(f"Weather Condition: {weather_condition}")
    print(f"Temperature: {temperature}°C")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")
else:
    print('Request failed with status code:', response.status_code)
