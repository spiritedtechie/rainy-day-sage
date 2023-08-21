## Description
Fetches forecast data from the UK MetOffice, and interacts with an LLM to 
produce a natural language summary.


## External services
The following are required and need to be configured in the `.env` file.

1. **MetOffice Datapoint** - API for UK weather data. Sign up [here](https://www.metoffice.gov.uk/services/data/datapoint/getting-started).
2. **OpenAI** - well known cloud-based LLM provider e.g. GPT-3 etc. Sign up [here](https://openai.com/).
3. **ActiveLoop DeepLake** - a cloud-based vector store with a free tier. Sign up [here](https://www.activeloop.ai/).

## Running locally

Copy the `.env.example` file to `.env` and fill in the properties.

Vectorise the reference data:
```
# Do the following once
pip install -r requirements.txt
python pre-processing/1_vectorise_weather_api_document.py
python pre-processing/2_vectorise_weather_code_mapping.py
```

Spin up the Flask API:

```
flask --app api run -p 3001
curl http://127.0.0.1:3001
```

## Result

The result from the api looks might look something like this:

```
{
   "summary":"The weather forecast for today is a feels like temperature of 20°C with a maximum temperature of 22°C. The wind speed is 11 mph with gusts up to 25 mph. The screen relative humidity is 70%. The visibility is good, between 10-20 km. The wind direction is east-southeast. The UV index is 1, indicating low exposure. The weather type is partly cloudy with a 49% chance of precipitation.",
   "status":"Average",
   "inspiring-message":"Even though the weather may not be perfect, remember that every day is a new opportunity to make the most of what we have. Embrace the partly cloudy skies and enjoy the gentle breeze. Don't let a little rain dampen your spirits, instead see it as a chance to appreciate the beauty of nature. Remember, the sun will always shine again, and with it comes new possibilities. So go out there and make today a day to remember!"
}
```