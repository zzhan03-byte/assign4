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
import xml.etree.ElementTree as ET
import urllib.request
import re

# Set up page configurations
st.set_page_config(
    page_title="Temperature Emoji Drawer",
    page_icon="🌡️",
    layout="centered"
)

# Function to dynamically generate emojis based on temperature celsius ranges
def get_temperature_artwork(temp_c):
    if temp_c <= 0:
        return {"tier": "Freezing", "color": "#17a2b8", "emoji": "🥶", "canvas": "❄️🏔️⛷️🥶🧊⛸️☃️🧣"}
    elif 0 < temp_c <= 15:
        return {"tier": "Chilly / Cool", "color": "#4a90e2", "emoji": "🧥", "canvas": "🍁🍂🧥☕🌲🚶‍♂️🧦🍁"}
    elif 15 < temp_c <= 25:
        return {"tier": "Mild / Comfortable", "color": "#28a745", "emoji": "😎", "canvas": "🌸🍃😎🚶‍♀️🚲🌳🌼🌷"}
    elif 25 < temp_c <= 35:
        return {"tier": "Warm / Hot", "color": "#fd7e14", "emoji": "☀️", "canvas": "☀️🕶️🍦🌊🏊‍♂️🥤🏖️🍉"}
    else:
        return {"tier": "Scorching Hot", "color": "#dc3545", "emoji": "🥵", "canvas": "🥵🔥🌵🧴🍦🥵🥤🐪"}

# 1. User Input for Location
city_input = st.text_input("Enter a US city name:", value="Boston")

if city_input:
    try:
        # Format input city name for RSS search query
        formatted_city = city_input.strip().replace(" ", "%20")
        rss_url = f"https://weather.gov" 
        
        # Fallback to direct RSS data query text scanner via a secondary reliable public endpoint
        # For universal simplicity without key dependencies:
        wttr_url = f"https://wttr.in{formatted_city}?format=%t"
        
        req = urllib.request.Request(
            wttr_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            raw_text = response.read().decode('utf-8').strip()
            
            # Extract digits from string (e.g. "+12°C" or "55°F")
            temp_digits = re.findall(r'[-+]?\d+', raw_text)
            
            if temp_digits:
                temp_val = int(temp_digits[0])
                
                # Check if the text output implies Celsius or Fahrenheit to align logic
                if "F" in raw_text:
                    temp_f = temp_val
                    temp_c = (temp_f - 32) * 5/9
                else:
                    temp_c = temp_val
                    temp_f = (temp_c * 9/5) + 32
                
                art = get_temperature_artwork(temp_c)
                
                # Display metrics panel
                st.write(f"### Current Temperature in **{city_input.title()}**")
                
                col1, col2 = st.columns(2)
                col1.metric(label="Temperature", value=f"{temp_c:.1f}°C / {temp_f:.1f}°F")
                col2.metric(label="Temperature Feel", value=f"{art['emoji']} {art['tier']}")
                
                # 4. Canvas Section
                st.write("---")
                st.write("### 🎨 Your Temperature Emoji Canvas")
                
                st.markdown(f"<h1 style='text-align: center; font-size: 100px; margin: 0;'>{art['emoji']}</h1>", unsafe_allow_html=True)
                st.markdown(
                    f"<h3 style='text-align: center; letter-spacing: 12px; "
                    f"background-color: {art['color']}22; border: 2px solid {art['color']}; "
                    f"padding: 20px; border-radius: 10px;'>{art['canvas']}</h3>", 
                    unsafe_allow_html=True
                )
            else:
                st.error("Could not parse data for this location. Please try another city.")
                
    except Exception as e:
        st.error(f"Network error handling your request: {e}")






