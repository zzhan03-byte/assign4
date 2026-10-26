# Import necessary packages (Make sure to also include in "requirements.txt" in this repository.)
import streamlit as st
import pandas as pd

# Print Title for the App
st.title("Microsoft Stock Data Dashboard by Zihan Zhan")

# Read CSV file with stock data (CSV file must be in 'main' folder for your assignment 4 repository) 
df = pd.read_csv("msft.csv")

# Set up the 4 tabs on the Dashboard
tabs = st.tabs(["📋 Raw Data", "📈 Price Chart", "📊 Volume Chart", "Fun Tab"])

# Tab 1: Raw Data
with tabs[0]:
    st.subheader(f"Raw Data for MSFT")
    st.dataframe(df, use_container_width=True)

# Tab 2: Closing Price Chart
with tabs[1]:
    st.subheader(f"Closing Price for MSFT")
    st.line_chart(df['Close'])

# Tab 3: Volume Chart
with tabs[2]:
    st.subheader(f"Volume for MSFT")
    st.bar_chart(df['Volume'])

# Tab 4: New
with tabs[3]:
    st.subheader(f"🌦️ Weather Emoji Drawer")
    st.markdown("Enter a city to get its current weather and "
            "generate matching emojis! (Powered by **Open-Meteo**, no API key needed)")
    import streamlit as st
import requests

# Set up page configurations
st.set_page_config(
    page_title="Weather Emoji Drawer",
    page_icon="🌦️",
    layout="centered"
)

# Dictionary mapping Open-Meteo WMO weather codes to text and emojis
WEATHER_MAPPING = {
    0: {"desc": "Clear sky", "emoji": "🌞", "canvas": "☀️🕶️🌻🥤🌅"},
    1: {"desc": "Mainly clear", "emoji": "🌤️", "canvas": "🌤️🍃✨🌸🚶"},
    2: {"desc": "Partly cloudy", "emoji": "⛅", "canvas": "⛅🌥️🪁🍃🚶"},
    3: {"desc": "Overcast", "emoji": "☁️", "canvas": "☁️☁️🧱🛋️☕📚"},
    45: {"desc": "Fog", "emoji": "🌫️", "canvas": "🌫️👻🌲🚗🏮🌫️"},
    48: {"desc": "Depositing rime fog", "emoji": "🌫️", "canvas": "🌫️❄️🌲🏔️🥶"},
    51: {"desc": "Light drizzle", "emoji": "🌦️", "canvas": "🌦️🌱🐌🌾🚶🌱"},
    53: {"desc": "Moderate drizzle", "emoji": "🌦️", "canvas": "🌦️💧🌱🌂👟🍃"},
    55: {"desc": "Dense drizzle", "emoji": "🌧️", "canvas": "🌧️🌧️☔🐌🍃🦆"},
    56: {"desc": "Light freezing drizzle", "emoji": "🌧️", "canvas": "🌧️❄️🥶🧣🧊"},
    57: {"desc": "Dense freezing drizzle", "emoji": "🌧️", "canvas": "🌧️❄️⛸️🏂🧤🥶"},
    61: {"desc": "Slight rain", "emoji": "🌧️", "canvas": "🌧️💧☔🏃‍♂️🏡🌧️"},
    63: {"desc": "Moderate rain", "emoji": "🌧️", "canvas": "🌧️🌊☔💧🐸🛋️"},
    65: {"desc": "Heavy rain", "emoji": "🌧️", "canvas": "🌧️🌧️⛈️🌊⛈️☔🐸"},
    66: {"desc": "Light freezing rain", "emoji": "🌧️", "canvas": "🌧️❄️🧊🥶🚗⚠️"},
    67: {"desc": "Heavy freezing rain", "emoji": "🌧️", "canvas": "🌧️❄️⛈️🧊🥶⚠️🚗"},
    71: {"desc": "Slight snowfall", "emoji": "❄️", "canvas": "❄️⛄🎿☃️❄️🌲"},
    73: {"desc": "Moderate snowfall", "emoji": "❄️", "canvas": "❄️❄️⛄☃️🏡🏂❄️"},
    75: {"desc": "Heavy snowfall", "emoji": "❄️", "canvas": "❄️❄️❄️☃️🏔️⛷️🥶❄️"},
    77: {"desc": "Snow grains", "emoji": "❄️", "canvas": "❄️⚪🥶🧤🧣"},
    80: {"desc": "Slight rain showers", "emoji": "🌦️", "canvas": "🌦️🌦️🏃‍♀️🌈🌱🦆"},
    81: {"desc": "Moderate rain showers", "emoji": "🌧️", "canvas": "🌧️🌊☔💧🏃‍♂️🌂"},
    82: {"desc": "Violent rain showers", "emoji": "⛈️", "canvas": "⛈️🌧️⛈️🌊🛶⛈️"},
    85: {"desc": "Slight snow showers", "emoji": "❄️", "canvas": "❄️⛷️☃️🎿❄️"},
    86: {"desc": "Heavy snow showers", "emoji": "❄️", "canvas": "❄️❄️🏔️🏂🥶❄️"},
    95: {"desc": "Thunderstorm", "emoji": "⛈️", "canvas": "⛈️⚡🌩️🌪️🔌🏠⛈️"},
    96: {"desc": "Thunderstorm with slight hail", "emoji": "⛈️", "canvas": "⛈️⚡⚪🚙⚠️🌩️"},
    99: {"desc": "Thunderstorm with heavy hail", "emoji": "⛈️", "canvas": "⛈️⚡🚨⚪🏚️💥🌧️"}
}

# 1. User Input for Location
city_input = st.text_input("Enter a city name:", value="Boston")

if city_input:
    try:
        # 2. Get Geocoding data (Lat/Lon) for the entered city name
        geo_url = f"https://open-meteo.com{city_input}&count=1&language=en&format=json"
        geo_response = requests.get(geo_url).json()
        
        if "results" in geo_response and len(geo_response["results"]) > 0:
            location_data = geo_response["results"][0]
            lat = location_data["latitude"]
            lon = location_data["longitude"]
            city_name = location_data["name"]
            country = location_data.get("country", "")
            
            # 3. Fetch real-time weather details using Lat/Lon
            weather_url = f"https://open-meteo.com{lat}&longitude={lon}&current=temperature_2m,weather_code"
            weather_data = requests.get(weather_url).json()
            
            current_weather = weather_data["current"]
            temp = current_weather["temperature_2m"]
            code = current_weather["weather_code"]
            
            # Get matching details from mapping, default fallback if unknown code
            weather_info = WEATHER_MAPPING.get(code, {"desc": "Unknown", "emoji": "❓", "canvas": "❓❓❓"})
            
            # Display metrics panel
            st.write(f"### Current Weather in **{city_name}, {country}**")
            
            col1, col2 = st.columns(2)
            col1.metric(label="Temperature", value=f"{temp}°C")
            col2.metric(label="Condition", value=f"{weather_info['emoji']} {weather_info['desc']}")
            
            # 4. Canvas Section: Drawing emojis according to today's weather
            st.write("---")
            st.write("### 🎨 Your Generated Weather Emoji Artwork")
            
            # Big featured icon
            st.markdown(f"<h1 style='text-align: center; font-size: 100px; margin: 0;'>{weather_info['emoji']}</h1>", unsafe_content_code=True)
            
            # Descriptive scenic row of emojis
            st.markdown(f"<h3 style='text-align: center; letter-spacing: 15px; background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>{weather_info['canvas']}</h3>", unsafe_content_code=True)
            
        else:
            st.error(f"Could not find a city named '{city_input}'. Please check your spelling and try again.")
            
    except Exception as e:
        st.error(f"An error occurred while fetching the data: {e}")


