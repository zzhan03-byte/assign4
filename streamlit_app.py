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
    st.subheader(f"🌡️ Temperature Emoji Drawer")
    st.markdown("Enter a city to check today's current temperature and generate an emoji")

import streamlit as st
import requests

# Set up page configurations
st.set_page_config(
    page_title="Temperature Emoji Drawer",
    page_icon="🌡️",
    layout="centered"
)

# Function to dynamically generate emojis based on temperature celsius ranges
def get_temperature_artwork(temp_c):
    if temp_c <= 0:
        return {
            "tier": "Freezing",
            "color": "#17a2b8",
            "emoji": "🥶",
            "canvas": "❄️🏔️⛷️🥶🧊⛸️☃️🧣"
        }
    elif 0 < temp_c <= 15:
        return {
            "tier": "Chilly / Cool",
            "color": "#4a90e2",
            "emoji": "🧥",
            "canvas": "🍁🍂🧥☕🌲🚶‍♂️🧦🍁"
        }
    elif 15 < temp_c <= 25:
        return {
            "tier": "Mild / Comfortable",
            "color": "#28a745",
            "emoji": "😎",
            "canvas": "🌸🍃😎🚶‍♀️🚲🌳🌼🌷"
        }
    elif 25 < temp_c <= 35:
        return {
            "tier": "Warm / Hot",
            "color": "#fd7e14",
            "emoji": "☀️",
            "canvas": "☀️🕶️🍦🌊🏊‍♂️🥤🏖️🍉"
        }
    else:  # More than 35°C
        return {
            "tier": "Scorching Hot",
            "color": "#dc3545",
            "emoji": "🥵",
            "canvas": "🥵🔥🌵🧴🍦🥵🥤🐪"
        }

# 1. User Input for Location
city_input = st.text_input("Enter a city name:", value="Miami")

if city_input:
    try:
        # 2. Geocoding API Request
        geo_url = "https://open-meteo.com"
        geo_params = {
            "name": city_input,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        
        response = requests.get(geo_url, params=geo_params)
        
        if response.status_code == 200:
            geo_response = response.json()
            
            if "results" in geo_response and len(geo_response["results"]) > 0:
                # FIXED: Added [0] index to grab the first matching dict item inside the list array
                location_data = geo_response["results"][0]
                lat = location_data["latitude"]
                lon = location_data["longitude"]
                city_name = location_data["name"]
                country = location_data.get("country", "")
                
                # 3. Fetch real-time weather details using parsed coordinates
                weather_url = "https://open-meteo.com"
                weather_params = {
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m"
                }
                
                weather_res = requests.get(weather_url, params=weather_params)
                
                if weather_res.status_code == 200:
                    weather_data = weather_res.json()
                    current_weather = weather_data["current"]
                    temp_c = current_weather["temperature_2m"]
                    temp_f = (temp_c * 9/5) + 32
                    
                    # Determine styling and artwork values via temperature logic mapping
                    art = get_temperature_artwork(temp_c)
                    
                    # Display metrics panel
                    st.write(f"### Current Temperature in **{city_name}, {country}**")
                    
                    col1, col2 = st.columns(2)
                    col1.metric(label="Temperature", value=f"{temp_c}°C / {temp_f:.1f}°F")
                    col2.metric(label="Temperature Feel", value=f"{art['emoji']} {art['tier']}")
                    
                    # 4. Canvas Section: Drawing emojis according to today's temperature tier
                    st.write("---")
                    st.write("### 🎨 Your Temperature Emoji Canvas")
                    
                    # Central big emoji indicator
                    st.markdown(f"<h1 style='text-align: center; font-size: 100px; margin: 0;'>{art['emoji']}</h1>", unsafe_allow_html=True)
                    
                    # Row banner display 
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing: 12px; "
                        f"background-color: {art['color']}22; border: 2px solid {art['color']}; "
                        f"padding: 20px; border-radius: 10px;'>{art['canvas']}</h3>", 
                        unsafe_allow_html=True
                    )
                else:
                    st.error(f"Weather API returned error status: {weather_res.status_code}")
            else:
                st.error(f"Could not find a city named '{city_input}'. Please check your spelling and try again.")
        else:
            st.error(f"Geocoding API returned error status: {response.status_code}")
            
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")





