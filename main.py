import os  # For file operations
import requests  # For making HTTP requests
import pytz  # For timezone conversion
import datetime  # For date and time manipulation
import csv  # For working with CSV files

# Retrieve the API key from the environment variable
api_key = os.environ.get('API_KEY')

print("**************************************")
print("*    Welcome to the Climbing Forecast Program!    *")
print("**************************************")

print(
  "Choose from a list of Colorado Climbing areas, \nenter the city name or zip code (anywhere in the world), \nor enter the exact coordinates to your bouldering problem/sport climb."
)


# Function to display the list of Colorado climbing areas and retrieve the ZIP code
def display_climbing_areas():
  with open('colorado_climbing_areas.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    climbing_areas = list(reader)

  print("List of Colorado Climbing Areas:")
  for i, area in enumerate(climbing_areas):
    print(f"{i + 1}. {area[0]}")

  choice = input(
    "\nEnter the number corresponding to the climbing area you want to check the forecast for (or enter 'Q' to quit): "
  )

  if choice.lower() == 'q':
    return None

  try:
    index = int(choice) - 1
    if index >= 0 and index < len(climbing_areas):
      return climbing_areas[index][
        1]  # Return the ZIP code instead of the area name
    else:
      print("Invalid choice.")
      return display_climbing_areas()
  except ValueError:
    print("Invalid choice.")
    return display_climbing_areas()


# Prompt the user for the desired location option
location_option = input(
  "\n\nChoose an option:\nA) List of Colorado Climbing Areas\nB) Enter City Name or ZIP code\nC) Enter Longitude and Latitude\n"
)

if location_option.lower() == 'a':
  # Display the list of Colorado climbing areas and get the chosen climbing area's ZIP code
  location = display_climbing_areas()
  if location is None:
    print("\nThank you for using the weather service. Have a great day!")
    exit()
elif location_option.lower() == 'b':
  # Prompt the user to enter the city name or ZIP code
  location = input("Enter the city name or ZIP code: ")
elif location_option.lower() == 'c':
  # Prompt the user to enter the latitude and longitude
  latitude = input("Enter the latitude: ")
  longitude = input("Enter the longitude: ")
  location = latitude + "," + longitude
else:
  print("Invalid option. Exiting...")
  exit()

# Determine if the location is a ZIP code or city
if location.isdigit():
  # If the location is a ZIP code, no change is required
  url = f'https://api.openweathermap.org/data/2.5/weather?zip={location}&appid={api_key}&units=metric'
elif location_option.lower() == 'c':
  # If the location option is longitude and latitude
  url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric'
else:
  # If the location is a city name, retrieve the ZIP code from the CSV file
  with open('colorado_climbing_areas.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
      if row[0].lower() == location.lower():
        location = row[1]  # Use the ZIP code from the CSV file
        break
  url = f'https://api.openweathermap.org/data/2.5/weather?zip={location}&appid={api_key}&units=metric'

# Determine if the location is a ZIP code or city
if location.isdigit():
  # If the location is a ZIP code, no change is required
  url = f'https://api.openweathermap.org/data/2.5/weather?zip={location}&appid={api_key}&units=metric'
elif location_option.lower() == 'c':
  # If the location option is longitude and latitude
  url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric'
else:
  # If the location is a city name, retrieve the ZIP code from the CSV file
  with open('colorado_climbing_areas.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
      if row[0].lower() == location.lower():
        location = row[1]  # Use the ZIP code from the CSV file
        break
  url = f'https://api.openweathermap.org/data/2.5/weather?zip={location}&appid={api_key}&units=metric'

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

  # Extract high and low temperatures
  temperature_max_celsius = data['main']['temp_max']
  temperature_min_celsius = data['main']['temp_min']

  # Convert temperatures to Fahrenheit
  temperature_max_fahrenheit = (temperature_max_celsius * 9 / 5) + 32
  temperature_min_fahrenheit = (temperature_min_celsius * 9 / 5) + 32

  # Calculate "feels like" temperature using wind chill formula
  wind_speed_kmph = data['wind']['speed'] * 3.6  # Convert m/s to km/h
  feels_like_fahrenheit = 35.74 + 0.6215 * temperature_fahrenheit - 35.75 * wind_speed_kmph**0.16 + 0.4275 * temperature_fahrenheit * wind_speed_kmph**0.16

  print("\nCurrent Weather Conditions:")
  print(f"Location: {location}")
  print(f"Weather: {weather_condition} ({weather_description})")
  print(
    f"Temperature: {temperature_celsius:.2f} °C / {temperature_fahrenheit:.2f} °F"
  )
  print(
    f"High Temperature: {temperature_max_celsius:.2f} °C / {temperature_max_fahrenheit:.2f} °F"
  )
  print(
    f"Low Temperature: {temperature_min_celsius:.2f} °C / {temperature_min_fahrenheit:.2f} °F"
  )
  print(f"Feels Like: {feels_like_fahrenheit:.2f} °F")
  print(f"Humidity: {humidity}%")
  print(f"Wind Speed: {wind_speed:.2f} mph")
  print(f"Rainfall: {rainfall_mm:.2f} mm / {rainfall_in:.2f} in")
  print(f"Sunrise: {sunrise_mst}")
  print(f"Sunset: {sunset_mst}\n")

  min_temp_fahrenheit = float(
    input(
      "Enter the minimum temperature (in Fahrenheit) for good climbing conditions: "
    ))
  max_temp_fahrenheit = float(
    input(
      "Enter the maximum temperature (in Fahrenheit) for good climbing conditions: "
    ))

  climbing_conditions = "Good"

  if not (min_temp_fahrenheit <= temperature_fahrenheit <=
          max_temp_fahrenheit):
    climbing_conditions = "Bad"

  if not (35 <= humidity <= 60):
    climbing_conditions = "Bad"

  if wind_speed > 20:
    climbing_conditions = "Bad"

  print("\nYour ideal climbing conditions are related to temperature", end="")
  print(f" ({min_temp_fahrenheit}°F & {max_temp_fahrenheit}°F),", end="")
  print(
    " humidity should be between 35-60%, and wind should be less than 20 mph.")

  if climbing_conditions == "Bad":
    print("\nHere is what is making the conditions bad:")
    if temperature_fahrenheit < min_temp_fahrenheit:
      print(
        f"Temperature ({temperature_fahrenheit}°F) is below the minimum threshold."
      )
    elif temperature_fahrenheit > max_temp_fahrenheit:
      print(
        f"Temperature ({temperature_fahrenheit}°F) is above the maximum threshold."
      )
    if humidity < 35 or humidity > 60:
      print(f"Humidity ({humidity}%) is outside the ideal range.")
    if wind_speed > 20:
      print(f"Wind speed ({wind_speed} mph) exceeds the maximum limit.")

  choice = input(
    "\nWould you like to see the weekly climbing conditions for the next 7 days? (yes/no): "
  )

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
      print(
        "\nDay       | Weather | Temperature (°C) | Temperature (°F) | Humidity (%) | Wind Speed (mph) | Climbing Conditions | Rainfall (mm) | Rainfall (in)"
      )
      print(
        "------------------------------------------------------------------------------------------------------------------------"
      )
      forecast_days = set()
      for forecast in weekly_forecast:
        forecast_time = datetime.datetime.strptime(forecast['dt_txt'],
                                                   '%Y-%m-%d %H:%M:%S')
        forecast_day = forecast_time.strftime('%A')
        if forecast_day not in forecast_days:
          forecast_days.add(forecast_day)
          forecast_weather_condition = forecast['weather'][0]['main']
          forecast_weather_description = forecast['weather'][0]['description']
          forecast_temperature_celsius = forecast['main']['temp']
          forecast_temperature_fahrenheit = (forecast_temperature_celsius * 9 /
                                             5) + 32
          forecast_humidity = forecast['main']['humidity']
          forecast_wind_speed = forecast['wind'][
            'speed'] * 2.237  # Convert m/s to mph
          forecast_rainfall_mm = forecast.get('rain', {}).get('3h', 0)
          forecast_rainfall_in = forecast_rainfall_mm / 25.4

          forecast_climbing_conditions = "Good"

          if not (min_temp_celsius <= forecast_temperature_celsius <=
                  max_temp_celsius):
            forecast_climbing_conditions = "Bad"

          if not (35 <= forecast_humidity <= 60):
            forecast_climbing_conditions = "Bad"

          if forecast_wind_speed > 20:
            forecast_climbing_conditions = "Bad"

          print(
            f"{forecast_day:<10} | {forecast_weather_condition:<7} | {forecast_temperature_celsius:<15.2f} | {forecast_temperature_fahrenheit:<15.2f} | {forecast_humidity:<13} | {forecast_wind_speed:<16.2f} | {forecast_climbing_conditions:<18} | {forecast_rainfall_mm:<14.2f} | {forecast_rainfall_in:<14.2f}"
          )
    else:
      print("Failed to retrieve the weekly forecast.")
  else:
    print("\nThank you for using the weather service. Have a great day!")

  # Save the output to a file
  filename = input("\nEnter the filename to save the output: ")
  with open(filename, 'w') as file:
    file.write("\nCurrent Weather Conditions:\n")
    file.write(f"Location: {location}\n")
    file.write(f"Weather: {weather_condition} ({weather_description})\n")
    file.write(
      f"Temperature: {temperature_celsius:.2f} °C / {temperature_fahrenheit:.2f} °F\n"
    )
    file.write(f"Humidity: {humidity}%\n")
    file.write(f"Wind Speed: {wind_speed:.2f} mph\n")
    file.write(f"Rainfall: {rainfall_mm:.2f} mm / {rainfall_in:.2f} in\n")
    file.write(f"Sunrise: {sunrise_mst}\n")
    file.write(f"Sunset: {sunset_mst}\n\n")
    file.write("Your ideal climbing conditions are related to temperature")
    file.write(f" ({min_temp_fahrenheit}°F & {max_temp_fahrenheit}°F),")
    file.write(
      " humidity should be between 35-60%, and wind should be less than 20 mph.\n"
    )
    file.write(f"Climbing Conditions: {climbing_conditions}\n")

    if climbing_conditions == "Bad":
      file.write("\nHere is what is making the conditions bad:\n")
      if temperature_fahrenheit < min_temp_fahrenheit:
        file.write(
          f"Temperature ({temperature_fahrenheit}°F) is below the minimum threshold.\n"
        )
      elif temperature_fahrenheit > max_temp_fahrenheit:
        file.write(
          f"Temperature ({temperature_fahrenheit}°F) is above the maximum threshold.\n"
        )
      if humidity < 35 or humidity > 60:
        file.write(f"Humidity ({humidity}%) is outside the ideal range.\n")
      if wind_speed > 20:
        file.write(
          f"Wind speed ({wind_speed} mph) exceeds the maximum limit.\n")

    file.write("\nWeekly Climbing Forecast:\n")
    file.write(
      "\nDay       | Weather | Temperature (°C) | Temperature (°F) | Humidity (%) | Wind Speed (mph) | Climbing Conditions | Rainfall (mm) | Rainfall (in)\n"
    )
    file.write(
      "------------------------------------------------------------------------------------------------------------------------\n"
    )

    forecast_days = set()
    for forecast in weekly_forecast:
      forecast_time = datetime.datetime.strptime(forecast['dt_txt'],
                                                 '%Y-%m-%d %H:%M:%S')
      forecast_day = forecast_time.strftime('%A')
      if forecast_day not in forecast_days:
        forecast_days.add(forecast_day)
        forecast_weather_condition = forecast['weather'][0]['main']
        forecast_weather_description = forecast['weather'][0]['description']
        forecast_temperature_celsius = forecast['main']['temp']
        forecast_temperature_fahrenheit = (forecast_temperature_celsius * 9 /
                                           5) + 32
        forecast_humidity = forecast['main']['humidity']
        forecast_wind_speed = forecast['wind'][
          'speed'] * 2.237  # Convert m/s to mph
        forecast_rainfall_mm = forecast.get('rain', {}).get('3h', 0)
        forecast_rainfall_in = forecast_rainfall_mm / 25.4

        forecast_climbing_conditions = "Good"

        if not (min_temp_celsius <= forecast_temperature_celsius <=
                max_temp_celsius):
          forecast_climbing_conditions = "Bad"

        if not (35 <= forecast_humidity <= 60):
          forecast_climbing_conditions = "Bad"

        if forecast_wind_speed > 20:
          forecast_climbing_conditions = "Bad"

        file.write(
          f"{forecast_day:<10} | {forecast_weather_condition:<7} | {forecast_temperature_celsius:<15.2f} | {forecast_temperature_fahrenheit:<15.2f} | {forecast_humidity:<13} | {forecast_wind_speed:<16.2f} | {forecast_climbing_conditions:<18} | {forecast_rainfall_mm:<14.2f} | {forecast_rainfall_in:<14.2f}\n"
        )
    file.close()

else:
  print("Failed to retrieve weather information. Please try again later.")
