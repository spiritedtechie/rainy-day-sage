# Rainy Day Sage
It rains a lot here in the UK. Why not let a friendly LLM be your sage? It can provide you with a wise 
and uplifting message if the weather forecast looks bad.

The LLM converts the weather forecast data from the MetOffice into a human readable form, and
quotes an uplifting message in case of bad weather.

Mostly just a way for me to mess around with LLMs.

## Running it
Copy the `.env.example` file to `.env` and fill in the properties.

```
pip install -r requirements.txt
python 1_main.py
```

## Result

The result from the LLM looks might look something like this:

```
On the 19th of August, the weather is as follows:

- Feels Like Temperature (C): 17
- Wind Gust (mph): 29
- Screen Relative Humidity (%): 79
- Temperature (C): 20
- Visibility: Good
- Wind Direction (compass): SW
- Wind Speed (mph): 16
- Max UV Index: 3
- Weather Type: Very Good
- Precipitation Probability (%): 7

The weather on the 19th of August is generally good, with a high temperature of 20°C and good visibility. However, there is a high wind gust of 29 mph and a relatively high humidity of 79%. 

In case the weather is bad, here's a wise and uplifting message to lighten the mood: "Storms may come and go, but they can never dampen the spirit within. Embrace the rain and let it wash away any worries. Remember, after every storm, there's a rainbow waiting to brighten your day."
```