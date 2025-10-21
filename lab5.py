# lab5.py
import streamlit as st
import requests
from openai import OpenAI

st.title("🌤️ Lab 5 — What to Wear Bot")


# Weather function 
def get_current_weather(location: str, api_key: str):
    """
    Calls OpenWeatherMap API and returns weather info for a location.
    Extracts temperatures in Celsius and humidity.
    """
    if "," in location:  # handle "Syracuse, NY"
        location = location.split(",")[0].strip()

    urlbase = "https://api.openweathermap.org/data/2.5/"
    urlweather = f"weather?q={location}&appid={api_key}"
    url = urlbase + urlweather

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or "main" not in data:
        return None

    # Convert Kelvin → Celsius
    temp = data['main']['temp'] - 273.15
    feels_like = data['main']['feels_like'] - 273.15
    temp_min = data['main']['temp_min'] - 273.15
    temp_max = data['main']['temp_max'] - 273.15
    humidity = data['main']['humidity']
    description = data['weather'][0]['description']

    return {
        "location": location,
        "temperature": round(temp, 2),
        "feels_like": round(feels_like, 2),
        "temp_min": round(temp_min, 2),
        "temp_max": round(temp_max, 2),
        "humidity": round(humidity, 2),
        "description": description,
    }


# Keys from secrets
OPENWEATHER_API_KEY = st.secrets["OPENWEATHER_API_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

# User input
city = st.text_input("Enter a city:", value="Syracuse, NY")

if st.button("Get Outfit Suggestion"):
    weather = get_current_weather(city, OPENWEATHER_API_KEY)

    if not weather:
        st.error("⚠️ Could not fetch weather. Check city name or API key.")
    else:
        st.write(f"**Weather in {weather['location']}**")
        st.write(
            f"{weather['description'].capitalize()}, "
            f"{weather['temperature']}°C (feels like {weather['feels_like']}°C). "
            f"Humidity: {weather['humidity']}%."
        )

        # Call LLM for clothing + picnic suggestion
        prompt = (
            f"The current weather in {weather['location']} is {weather['description']} "
            f"with a temperature of {weather['temperature']}°C (feels like {weather['feels_like']}°C), "
            f"humidity {weather['humidity']}%. "
            "Suggest appropriate clothes to wear today and say if it’s a good day for a picnic."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
            )
            suggestion = response.choices[0].message.content
            st.subheader("👕 Clothing & Picnic Suggestion")
            st.write(suggestion)
        except Exception as e:
            st.error(f"Error with OpenAI: {e}")
