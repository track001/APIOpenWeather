<h1>Climbing Forecast Program</h1>

<br>**Data Sources for Colorado Climbing Areas and Weather Forecasts**
<br>This program utilizes multiple data sources to provide accurate weather forecasts for various climbing areas in Colorado:
<br>*-OpenWeather API:* The weather data used in this program is sourced from the OpenWeather API, a reliable weather data provider. The API offers a comprehensive range of weather information, including current conditions, forecasts, and more. The weather data obtained from the OpenWeather API forms the basis for generating the climbing forecasts.
<br>*-Mountain Project:* The list of Colorado climbing areas used in this program is sourced from Mountain Project, a renowned platform for climbers. Mountain Project provides a vast collection of climbing locations, including their respective "crag" names. This ensures that the program covers a comprehensive list of climbing areas in Colorado.
<br>*-GeoDomain:* To ensure the accuracy of the climbing area locations, the GeoDomain database is utilized. The GeoDomain database provides the most precise ZIP codes associated with each climbing area. The ZIP code information is essential for retrieving accurate weather data from the OpenWeather API. By incorporating the ZIP code information from GeoDomain, the program ensures precise weather forecasts tailored to specific climbing areas.

<br> **Features** </br>
Get weather conditions for a specific location:
<br>A) Choose from a list of pre-existing Colorado climbing areas.
<br>B) Enter a city name or ZIP code.
<br>C) Enter coordinates (latitude and longitude).

<br> *Convert weather data to user-friendly units:* </br>
-Temperature is converted from Celsius to Fahrenheit.
<br>-Wind speed is converted from meters per second (m/s) to miles per hour (mph).
<br>-Rainfall is converted from millimeters (mm) to inches (in).
<br>-Timezone is converted from UTC to Mountain Standard Time (MST).
<br>-Determine climbing conditions based on user-defined temperature range, humidity, and wind speed.

**Program Objectives**
<br>-Display the current weather conditions and climbing conditions for the specified location.
<br>-Show a weekly climbing forecast for the next 7 days.

<br> *How to Use*
<br>-Run the script and follow the prompts to choose the location input option.
<br>-Enter the desired location (Colorado climbing area list, city name, ZIP code, or coordinates through longitude and latitude) when prompted.
<br>-Provide the minimum and maximum temperature range (in Fahrenheit) for good climbing conditions.
<br>The program will fetch the current weather conditions and determine the climbing conditions based on the specified range, humidity, and wind speed.
<br>The program will display the current weather conditions, climbing conditions, and any factors that make the conditions bad.
<br>Optionally, you can choose to see the weekly climbing conditions for the next 7 days.
<br>The program will output the weekly forecast, including weather conditions, temperatures, humidity, wind speed, rainfall, and climbing conditions.

**Dependencies**
<br>*-Python 3.x* requests (2.x.x) for making HTTP requests.
<br>-*pytz (2.x.x)* - for timezone conversion.
<br>To install the required dependencies, use the following command:
<br>```pip install requests pytz```
<br>*-API Key*
<br>To use the OpenWeather API and fetch weather data, you need to provide an API key. Instructions for obtaining an API key can be found on the OpenWeather website: https://openweathermap.org/appid.

<br>Once you have obtained your API key, replace the placeholder YOUR_API_KEY in the code with your actual API key:
<br>```API_KEY = "YOUR_API_KEY"```

**Credits**
<br>The Climbing Forecast Program was developed by Ti Schwarz and is based on the OpenWeather API. The program utilizes weather data from the OpenWeatherMap service to provide accurate and up-to-date climbing conditions for various locations.

**License**
<br>This project is licensed under the MIT License.

**Limitations**
<br>*-Accuracy and Coverage:* Weather forecasts are based on data collected from weather reporting towers located at specific geographic locations. The accuracy of the forecast for a particular location depends on the proximity of the weather reporting tower and the coverage of the network of weather stations. In some cases, the nearest weather reporting tower may not be in close proximity to the desired location, leading to potential discrepancies in the forecasted weather conditions.
<br>*-Regional Variations:* Weather conditions can vary significantly across different regions, even within a relatively small area. This means that a single weather reporting tower may not capture the microclimates or localized weather patterns that can occur within a specific location, such as Rocky Mountain National Park (RMNP) in Estes Park. Therefore, the forecasted weather conditions may not accurately represent the conditions within RMNP itself.
<br>*-Elevation Differences:* Elevation plays a crucial role in weather patterns and conditions. Weather reporting towers typically report weather conditions at their specific elevation. If your desired location within RMNP has a significantly different elevation than the weather reporting tower, the forecasted conditions may not align with the actual conditions at that specific location. It's important to consider the elevation differences and their potential impact on the accuracy of the forecast.
<br>*-Generalized Forecasts:* Weather forecasts are often generalized for larger areas, such as ZIP codes or city names. This means that a single forecast may apply to a broader region rather than a specific point within that region. In the case of RMNP, where multiple ZIP codes may span the area, relying solely on a ZIP code may not provide the most accurate forecast for a particular climbing spot within the park.

