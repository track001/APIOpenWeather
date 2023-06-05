import os
import requests
import pytz
import datetime
import csv


# Retrieve the API key from the environment variable
api_key = os.environ.get('API_KEY')


# Function to display the list of Colorado climbing areas
def display_climbing_areas():
    with open('colorado_climbing_areas.csv', 'r') as file:
        reader = csv.reader(file)
        climbing_areas = list(reader)
        
    print("List of Colorado Climbing Areas:")
    for i, area in enumerate(climbing_areas):
        print(f"{i+1}. {area[0]}")

    choice = input("\nEnter the number corresponding to the climbing area you want to check the forecast for (or enter 'Q' to quit): ")
    
    if choice.lower() == 'q':
        return None
    
    try:
        index = int(choice) - 1
        if index >= 0 and index < len(climbing_areas):
            return climbing_areas[index][1]
        else:
            print("Invalid choice.")
            return display_climbing_areas()
    except ValueError:
        print("Invalid choice.")
        return display_climbing_areas()


# Prompt the user for the desired location option
location_option = input("Choose an option:\nA) List of Colorado Climbing Areas\nB) Enter City Name or ZIP code\n")

if location_option.lower() == 'a':
    # Display the list of Colorado climbing areas and get the chosen ZIP code
    location = display_climbing_areas()
    if location is None:
        print("\nThank you for using the weather service. Have a great day!")
        exit()
elif location_option.lower() == 'b':
    # Prompt the user to enter the city name or ZIP code
    location = input("Enter the city name or ZIP code: ")
else:
    print("Invalid option. Exiting...")
    exit()


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

    # Define the timezone for MST (Mountain Standard Time)
    timezone = pytz.timezone("MST")

    # Convert sunrise and sunset times from UTC to MST
    sunrise_utc = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
    sunset_utc = datetime.datetime.fromtimestamp(data['sys']['sunset'])

    sunrise_mst = sunrise_utc.astimezone(timezone).strftime('%Y-%m-%d %H:%M:%S')
    sunset_mst = sunset_utc.astimezone(timezone).strftime('%Y-%m-%d %H:%M:%S')

    # Extract and display weather information
    weather_condition = data['weather'][0]['main']
    weather_description = data['weather'][0]['description']
    temperature_celsius = data['main']['temp']
    temperature_fahrenheit = (temperature_celsius * 9 / 5) + 32
    humidity = data['main']['humidity']
    rainfall_mm = data.get('rain', {}).get('1h', 0)
    rainfall_inches = rainfall_mm * 0.03937
    wind_speed = data['wind']['speed']

    print("\nCurrent Weather Conditions:")
    print(f"Location: {location}")
    print(f"Weather: {weather_condition} ({weather_description})")
    print(f"Temperature: {temperature_celsius:.2f} °C / {temperature_fahrenheit:.2f} °F")
    print(f"Humidity: {humidity}%")
    print(f"Rainfall: {rainfall_mm:.2f} mm / {rainfall_inches:.2f} in")
    print(f"Wind Speed: {wind_speed} m/s")

    # Prompt the user for the minimum and maximum temperature in Fahrenheit
    min_temp_fahrenheit = float(input("\nEnter the minimum temperature (in Fahrenheit) for good climbing conditions: "))
    max_temp_fahrenheit = float(input("Enter the maximum temperature (in Fahrenheit) for good climbing conditions: "))

    # Define the climbing condition thresholds
    min_temp_celsius = (min_temp_fahrenheit - 32) * 5 / 9
    max_temp_celsius = (max_temp_fahrenheit - 32) * 5 / 9
    min_humidity = 35
    max_humidity = 60
    max_wind_speed = 20

    # Check if the climbing conditions are good
    climbing_conditions = True

    if temperature_celsius < min_temp_celsius or temperature_celsius > max_temp_celsius:
        climbing_conditions = False

    if humidity < min_humidity or humidity > max_humidity:
        climbing_conditions = False

    if wind_speed > max_wind_speed:
        climbing_conditions = False

    if climbing_conditions:
        print("\nClimbing Conditions: Good")
    else:
        print("\nClimbing Conditions: Bad")

    choice = input("\nWould you like to see the weekly climbing conditions for the next 7 days? (yes/no): ")

    if choice.lower() == "yes" or choice.lower() == "y":
        # Check if the climbing conditions are good for each day in the weekly forecast
        forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric'
        forecast_response = requests.get(forecast_url)

        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            weekly_forecast = forecast_data['list']
            print("\nWeekly Climbing Forecast:")
            print("\nDay | Weather | Temperature (°C) | Temperature (°F) | Humidity (%) | Wind Speed (m/s) | Climbing Conditions | Rainfall (mm) | Rainfall (in)")
            print("------------------------------------------------------------------------------------------------------------------------")
            forecast_days = set()
            for forecast in weekly_forecast:
                forecast_time = datetime.datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')
                forecast_day = forecast_time.astimezone(timezone).strftime('%A')
                if forecast_day not in forecast_days:
                    forecast_days.add(forecast_day)
                    forecast_weather = forecast['weather'][0]['main']
                    forecast_description = forecast['weather'][0]['description']
                    forecast_temperature = forecast['main']['temp']
                    forecast_temperature_fahrenheit = (forecast_temperature * 9 / 5) + 32
                    forecast_humidity = forecast['main']['humidity']
                    forecast_wind_speed = forecast['wind']['speed']
                    forecast_rainfall_mm = forecast.get('rain', {}).get('3h', 0)
                    forecast_rainfall_inches = forecast_rainfall_mm * 0.03937
                    forecast_climbing_conditions = "Good" if min_temp_celsius <= forecast_temperature <= max_temp_celsius and min_humidity <= forecast_humidity <= max_humidity and forecast_wind_speed <= max_wind_speed else "Bad"
                    print(f"{forecast_day} | {forecast_description} | {forecast_temperature:.2f} | {forecast_temperature_fahrenheit:.2f} | {forecast_humidity} | {forecast_wind_speed} | {forecast_climbing_conditions} | {forecast_rainfall_mm:.2f} | {forecast_rainfall_inches:.2f}")
        else:
            print('Failed to retrieve weekly forecast:', forecast_response.status_code)

    else:
        print("\nThank you for using the weather service. Have a great day!")

else:
    print('Request failed with status code:', response.status_code)
