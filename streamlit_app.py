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
    st.subheader(f"Outfit Emoji Suggestion")
    st.markdown("Answer 3 simple questions on a scale of 1 to 10 to draw your customized daily wearing suggestions!")


import streamlit as st

# Set up page configurations
st.set_page_config(
    page_title="Outfit Emoji Planner",
    page_icon="🧥",
    layout="centered"
)

st.write("---")
st.subheader("📋 Quick Questions")

# 1. First Question: Temperature Feel
q_temp = st.slider(
    "1. What do you feel about today's weather?",
    min_value=1,
    max_value=10,
    value=5,
    help="1 is Cold, 10 is Hot"
)

# 2. Second Question: Sky/Weather Conditions
q_sky = st.slider(
    "2. How does today's weather look like?",
    min_value=1,
    max_value=10,
    value=5,
    help="1 is Raining/Cloudy, 10 is Sunny"
)

# 3. Third Question: Transit / Activity Mode
q_transit = st.slider(
    "3. What is your plan for going out?",
    min_value=1,
    max_value=10,
    value=5,
    help="1 is Walking, 10 is in Transportation"
)

# --- Logic to generate recommendations based on the 1-10 scales ---
outfit_canvas = []
footwear = "👟"  # Default
accessory = "🎒" # Default

# Temperature clothing layer logic
if q_temp <= 3:
    # Cold weather clothing layers
    clothing_tier = "Heavy Winter Wear"
    theme_color = "#17a2b8"
    outfit_canvas.extend(["🥶", "🥶", "🧥", "🧣", "🧤", "👖", "🧦"])
    footwear = "🥾"  # Heavy winter boots
elif 4 <= q_temp <= 6:
    # Mild/Cool layers
    clothing_tier = "Comfortable Layers"
    theme_color = "#28a745"
    outfit_canvas.extend(["😎", "🧥", "👕", "👖"])
    footwear = "👟"  # Sneakers
else:
    # Hot weather minimal clothing
    clothing_tier = "Light Summer Clothes"
    theme_color = "#fd7e14"
    outfit_canvas.extend(["☀️", "🥵", "🕶️", "👕", "🩳"])
    footwear = "🩴"  # Sandals/Slippers

# Sky / Weather condition protection logic
if q_sky <= 3:
    # Rainy / Stormy gear adjustments
    outfit_canvas.append("☔")
    if q_temp <= 6:
        outfit_canvas.append("🧥")  # Rain coat protection
else:
    # Sunny protection gear
    if q_temp >= 5:
        outfit_canvas.append("🧢")  # Sun cap
    if q_sky >= 8:
        outfit_canvas.append("🕶️")  # Sunglasses

# Walking vs. Transportation footwear and baggage logic
if q_transit <= 4:
    # Heavy active walking means priority on athletic comfort
    if footwear != "🩴" and footwear != "🥾":
        footwear = "👟"  # Force comfortable running shoes
    accessory = "🎒"    # Backpack for supplies while walking
else:
    # Transportation means formal / luxury footwear or light bags are fine
    if q_temp >= 7:
        footwear = "🥿"  # Flats / Loafers
    else:
        footwear = "👞"  # Dress shoes / Boots
    accessory = "💼"    # Briefcase or handheld purse

# Combine the contextual items into the finalized dynamic array string
outfit_canvas.append(footwear)
outfit_canvas.append(accessory)
canvas_string = "".join(outfit_canvas)

# --- Render Results Canvas UI ---
st.write("---")
st.write("### 🎨 Your Suggested Wearing")

# The main mood indicator block
st.markdown(
    f"<div style='text-align: center; border: 2px dashed {theme_color}; "
    f"background-color: {theme_color}11; padding: 25px; border-radius: 12px; margin-top: 15px;'>"
    f"<p style='font-size: 16px; margin: 0; color: #555; font-weight: bold;'>RECOMMENDED STYLE STYLE: {clothing_tier.upper()}</p>"
    f"<h1 style='font-size: 60px; letter-spacing: 15px; margin: 15px 0;'>{canvas_string}</h1>"
    f"</div>", 
    unsafe_allow_html=True
)

# Text description details block
st.write("#### 📝 Breakdowns for Today:")
st.markdown(f"- **Top & Bottom Layer Basics:** Look out for items matching {canvas_string[2:5] if len(canvas_string) > 4 else '👕'}")
st.markdown(f"- **Footwear Focus:** Highly optimized for your choice of locomotion ({footwear})")
st.markdown(f"- **Weather Safeguard:** Environmental protection check items ({'☔ Umbrella/Raincoat active' if q_sky <= 3 else '🧢/🕶️ Sun shield accessories ready'})")








