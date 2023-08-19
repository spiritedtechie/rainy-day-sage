# Rainy Day Sage
It rains a lot here in the UK. Why not let a friendly LLM be your sage? It can provide you with a wise 
and uplifting message if the weather forecast looks bad.

The LLM converts the weather forecast data from the MetOffice into a human readable form, and
quotes an uplifting message in case of bad weather.

Mostly just a way for me to mess around with LLMs.

## Running it
Copy the `.env.example` file to `.env` and fill in the properties.

```
# Do the following once
pip install -r requirements.txt
python pre-processing/1_vectorise_weather_api_document.py
python pre-processing/2_vectorise_weather_code_mapping.py
```

Then run as many times as you like:
```
python run_service.py
```

Or to spin up a Flask API:

```
flask --app api run -p 3001
curl http://127.0.0.1:3001
```

## Result

The result from the LLM looks might look something like this:

```
{
   "summary":"The weather forecast for today is a feels like temperature of 20°C with a maximum temperature of 22°C. The wind speed is 11 mph with gusts up to 25 mph. The screen relative humidity is 70%. The visibility is good, between 10-20 km. The wind direction is east-southeast. The UV index is 1, indicating low exposure. The weather type is partly cloudy with a 49% chance of precipitation.",
   "status":"Average",
   "inspiring-message":"Even though the weather may not be perfect, remember that every day is a new opportunity to make the most of what we have. Embrace the partly cloudy skies and enjoy the gentle breeze. Don't let a little rain dampen your spirits, instead see it as a chance to appreciate the beauty of nature. Remember, the sun will always shine again, and with it comes new possibilities. So go out there and make today a day to remember!"
}
```