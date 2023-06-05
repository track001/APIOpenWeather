import os  # Provides access to operating system functionalities
import requests  # Allows sending HTTP requests and receiving responses
import datetime  # Provides classes for manipulating dates and times - standard is UTC
import pytz  # Provides time zone functionalities, including conversions to MST

# Retrieve the API key from the environment variable
api_key = os.environ.get('API_KEY')

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
  weather_description = data['weather'][0]['description']
  temperature_celsius = data['main']['temp']
  temperature_fahrenheit = (temperature_celsius * 9 / 5) + 32
  humidity = data['main']['humidity']
  air_pressure_hpa = data['main']['pressure']
  air_pressure_inhg = air_pressure_hpa * 0.02953
  rainfall_mm = data.get('rain', {}).get('1h', 0)
  rainfall_in = rainfall_mm * 0.03937
  wind_speed_mps = data['wind']['speed']
  wind_speed_mph = wind_speed_mps * 2.23694
  sunrise_timestamp = data['sys']['sunrise']
  sunset_timestamp = data['sys']['sunset']
  visibility_m = data['visibility']
  visibility_km = visibility_m / 1000
  visibility_mi = visibility_m / 1609

  # Convert sunrise and sunset timestamps to readable format in MST
  timezone = pytz.timezone('MST')
  sunrise_datetime = datetime.datetime.fromtimestamp(sunrise_timestamp,
                                                     timezone)
  sunset_datetime = datetime.datetime.fromtimestamp(sunset_timestamp, timezone)

  print(f"\nHere is the weather in {location}!")
  print(f"\nWeather Condition: {weather_condition}")
  print(f"Weather Description: {weather_description}")
  print(
    f"\nTemperature: {temperature_celsius:.2f}°C / {temperature_fahrenheit:.2f}°F"
  )
  print(f"Humidity: {humidity}%")
  print(
    f"Air Pressure: {air_pressure_hpa:.2f} hPa / {air_pressure_inhg:.2f} inHg")
  print(f"Rainfall (last 1 hour): {rainfall_mm:.2f} mm / {rainfall_in:.2f} in")
  print(f"Wind Speed: {wind_speed_mps:.2f} m/s / {wind_speed_mph:.2f} mph")
  print(f"Sunrise: {sunrise_datetime}")
  print(f"Sunset: {sunset_datetime}")
  print(f"Visibility: {visibility_km:.2f} km / {visibility_mi:.2f} mi")

  # Calculate and display the temperature conversion steps
  print("\nTemperature Conversion:")
  print(
    f"{temperature_celsius:.2f}°C = ({temperature_celsius:.2f} × 9/5) + 32")
  print(f"{temperature_celsius:.2f}°C = {temperature_fahrenheit:.2f}°F")

else:
  print('Request failed with status code:', response.status_code)
