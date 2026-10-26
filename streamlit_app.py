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
import random

# 设置页面配置
st.set_page_config(
    page_title="Temperature Emoji Drawer",
    page_icon="🌡️",
    layout="centered"
)

# 应用标题
st.title("🌡️ Temperature Emoji Drawer")
st.markdown("由于当前部署环境限制了外网连接，我们为你开启了 **Google 天气模拟器模式**！")

# 气温区间与 Emoji 艺术画的映射函数
def get_temperature_artwork(temp_c):
    if temp_c <= 0:
        return {"tier": "极寒 / Freezing", "color": "#17a2b8", "emoji": "🥶", "canvas": "❄️🏔️⛷️🥶🧊⛸️☃️🧣"}
    elif 0 < temp_c <= 15:
        return {"tier": "寒冷 / Chilly", "color": "#4a90e2", "emoji": "🧥", "canvas": "🍁🍂🧥☕🌲🚶‍♂️🧦🍁"}
    elif 15 < temp_c <= 25:
        return {"tier": "舒适 / Mild", "color": "#28a745", "emoji": "😎", "canvas": "🌸🍃😎🚶‍♀️🚲🌳🌼🌷"}
    elif 25 < temp_c <= 35:
        return {"tier": "炎热 / Warm", "color": "#fd7e14", "emoji": "☀️", "canvas": "☀️🕶️🍦🌊🏊‍♂️🥤🏖️🍉"}
    else:
        return {"tier": "酷暑 / Scorching", "color": "#dc3545", "emoji": "🥵", "canvas": "🥵🔥🌵🧴🍦🥵🥤🐪"}

# 1. 用户输入城市
city_input = st.text_input("输入城市名称 (如 Boston, Miami):", value="Boston")

if city_input:
    # 2. 模拟 Google 天气的数据生成（离线运行，永不报错）
    # 使用城市名字的长度和首字母作为随机种子，确保同一个城市每次生成的温度是固定的，模拟真实天气效果
    seed = sum(ord(char) for char in city_input)
    random.seed(seed)
    
    # 随机生成一个合理的温度 (-5 到 38°C 之间)
    simulated_temp_c = random.randint(-5, 38)
    simulated_temp_f = (simulated_temp_c * 9/5) + 32
    
    # 获取对应的 Emoji 艺术画
    art = get_temperature_artwork(simulated_temp_c)
    
    # 3. 模拟 Google 天气的 UI 展示
    st.write(f"### 🔍 Google Weather (模拟预估) 结果： **{city_input.title()}**")
    
    col1, col2 = st.columns(2)
    col1.metric(label="当前温度", value=f"{simulated_temp_c}°C / {simulated_temp_f:.1f}°F")
    col2.metric(label="体感状态", value=f"{art['emoji']} {art['tier']}")
    
    # 4. Canvas 画布区域
    st.write("---")
    st.write("### 🎨 根据今日气温生成的 Emoji 画布")
    
    # 中央超大 Emoji
    st.markdown(f"<h1 style='text-align: center; font-size: 100px; margin: 0;'>{art['emoji']}</h1>", unsafe_allow_html=True)
    
    # 动态背景边框条
    st.markdown(
        f"<h3 style='text-align: center; letter-spacing: 12px; "
        f"background-color: {art['color']}22; border: 2px solid {art['color']}; "
        f"padding: 20px; border-radius: 10px;'>{art['canvas']}</h3>", 
        unsafe_allow_html=True
    )
    
    # 提供一个手动微调滑块，增强趣味性
    st.write("---")
    st.caption("💡 想要测试其他气温？在下方手动调整温度，画布会实时变化：")
    user_temp = st.slider("微调实时温度 (°C)", min_value=-20, max_value=45, value=int(simulated_temp_c))
    
    # 如果用户拖动了滑块，实时更新下方的画布
    if user_temp != simulated_temp_c:
        custom_art = get_temperature_artwork(user_temp)
        st.markdown(f"<h4 style='text-align: center; color:{custom_art['color']};'>{user_temp}°C 对应的画布形态：</h4>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; letter-spacing: 12px; background-color: {custom_art['color']}22; border: 1px dashed {custom_art['color']}; padding: 15px; border-radius: 10px;'>{custom_art['canvas']}</h3>", unsafe_allow_html=True)







