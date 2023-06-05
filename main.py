import os  # Provides functions for interacting with the operating system, such as accessing environment variables.
import requests  # Allows making HTTP requests to the weather API to retrieve weather data.
import pytz  # Provides timezone information and allows converting between different timezones (MST).
import datetime  # Provides classes and functions for working with dates and times.
import csv  # Allows reading and writing CSV files, which is used to retrieve the list of climbing areas in Colorado.



# Retrieve the API key from the environment variable
api_key = os.environ.get('API_KEY')


# Function to display the list of Colorado climbing areas
def display_climbing_areas():
    with open('colorado_climbing_areas.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
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
            return climbing_areas[index][0]
        else:
            print("Invalid choice.")
            return display_climbing_areas()
    except ValueError:
        print("Invalid choice.")
        return display_climbing_areas()


# Prompt the user for the desired location option
location_option = input("Choose an option:\nA) List of Colorado Climbing Areas\nB) Enter City Name or ZIP code\n")

if location_option.lower() == 'a':
    # Display the list of Colorado climbing areas and get the chosen climbing area
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
    wind_speed = data['wind']['speed'] * 2.237  # Convert m/s to mph
    rainfall_mm = data.get('rain', {}).get('1h', 0)
    rainfall_in = rainfall_mm / 25.4

    print("\nCurrent Weather Conditions:")
    print(f"Location: {location}")
    print(f"Weather: {weather_condition} ({weather_description})")
    print(f"Temperature: {temperature_celsius:.2f} °C / {temperature_fahrenheit:.2f} °F")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed:.2f} mph")
    print(f"Rainfall: {rainfall_mm:.2f} mm / {rainfall_in:.2f} in")
    print(f"Sunrise: {sunrise_mst}")
    print(f"Sunset: {sunset_mst}\n")

    min_temp_fahrenheit = float(input("Enter the minimum temperature (in Fahrenheit) for good climbing conditions: "))
    max_temp_fahrenheit = float(input("Enter the maximum temperature (in Fahrenheit) for good climbing conditions: "))

    climbing_conditions = "Good"

    if not (min_temp_fahrenheit <= temperature_fahrenheit <= max_temp_fahrenheit):
        climbing_conditions = "Bad"

    if not (35 <= humidity <= 60):
        climbing_conditions = "Bad"

    if wind_speed > 20:
        climbing_conditions = "Bad"

    print("\nYour ideal climbing conditions are related to temperature", end="")
    print(f" ({min_temp_fahrenheit}°F & {max_temp_fahrenheit}°F),", end="")
    print(" humidity should be between 35-60%, and wind should be less than 20 mph.")

    if climbing_conditions == "Bad":
        print("\nHere is what is making the conditions bad:")
        if temperature_fahrenheit < min_temp_fahrenheit:
            print(f"Temperature ({temperature_fahrenheit}°F) is below the minimum threshold.")
        elif temperature_fahrenheit > max_temp_fahrenheit:
            print(f"Temperature ({temperature_fahrenheit}°F) is above the maximum threshold.")
        if humidity < 35 or humidity > 60:
            print(f"Humidity ({humidity}%) is outside the ideal range.")
        if wind_speed > 20:
            print(f"Wind speed ({wind_speed} mph) exceeds the maximum limit.")

    choice = input("\nWould you like to see the weekly climbing conditions for the next 7 days? (yes/no): ")

    if choice.lower() == "yes" or choice.lower() == "y":
        # Check if the climbing conditions are good
        min_temp_celsius = (min_temp_fahrenheit - 32) * 5 / 9
        max_temp_celsius = (max_temp_fahrenheit - 32) * 5 / 9

        # Get the weekly forecast for climbing conditions
        forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric'
        forecast_response = requests.get(forecast_url)

        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            weekly_forecast = forecast_data['list']
            print("\nWeekly Climbing Forecast:")
            print("\nDay       | Weather | Temperature (°C) | Temperature (°F) | Humidity (%) | Wind Speed (mph) | Climbing Conditions | Rainfall (mm) | Rainfall (in)")
            print("------------------------------------------------------------------------------------------------------------------------")
            forecast_days = set()
            for forecast in weekly_forecast:
                forecast_time = datetime.datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')
                forecast_day = forecast_time.strftime('%A')
                if forecast_day not in forecast_days:
                    forecast_days.add(forecast_day)
                    forecast_weather_condition = forecast['weather'][0]['main']
                    forecast_weather_description = forecast['weather'][0]['description']
                    forecast_temperature_celsius = forecast['main']['temp']
                    forecast_temperature_fahrenheit = (forecast_temperature_celsius * 9 / 5) + 32
                    forecast_humidity = forecast['main']['humidity']
                    forecast_wind_speed = forecast['wind']['speed'] * 2.237  # Convert m/s to mph
                    forecast_rainfall_mm = forecast.get('rain', {}).get('3h', 0)
                    forecast_rainfall_in = forecast_rainfall_mm / 25.4

                    forecast_climbing_conditions = "Good"

                    if not (min_temp_celsius <= forecast_temperature_celsius <= max_temp_celsius):
                        forecast_climbing_conditions = "Bad"

                    if not (35 <= forecast_humidity <= 60):
                        forecast_climbing_conditions = "Bad"

                    if forecast_wind_speed > 20:
                        forecast_climbing_conditions = "Bad"

                    print(f"{forecast_day:<9} | {forecast_weather_condition:<7} | {forecast_temperature_celsius:<16.2f} | {forecast_temperature_fahrenheit:<16.2f} | {forecast_humidity:<13} | {forecast_wind_speed:<16.2f} | {forecast_climbing_conditions:<19} | {forecast_rainfall_mm:<14.2f} | {forecast_rainfall_in:<14.2f}")
        else:
            print("Failed to retrieve the weekly forecast.")
    else:
        print("\nThanks for using the weather service. Have a great day!")
else:
    print("Failed to retrieve weather data. Please try again later.")
