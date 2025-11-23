import streamlit as st
import requests
import os
from dotenv import load_dotenv
from PIL import Image

# Load API key
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Streamlit Page Configuration
st.set_page_config(
    page_title="Weather Forecast App",
    page_icon="🌦️",
    layout="wide"
)

# Custom CSS for styling + animations
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: white;
        }
        .big-title {
            font-size: 48px;
            font-weight: 800;
            text-align: center;
            color: #ffffff;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.4);
        }
        .sub {
            text-align: center;
            color: #cfe0ff;
            margin-bottom: 30px;
        }
        .card {
            background: rgba(255,255,255,0.15);
            padding: 20px;
            border-radius: 20px;
            backdrop-filter: blur(12px);
            transition: 0.3s;
        }
        .card:hover {
            transform: scale(1.02);
        }
        .weather-icon {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 120px;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("⚙️ Settings")
st.sidebar.info("Enter a city name and choose forecast type.")
forecast_type = st.sidebar.selectbox("Forecast Type", ["Current Weather", "5-Day Forecast"])

# Title
st.markdown("<h1 class='big-title'>🌦️ Weather Forecast App</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub'>Beautiful, Real-Time Weather Data</p>", unsafe_allow_html=True)

city = st.text_input("Enter city name")


# Function to call OpenWeather API
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

def get_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()


# Icon picker
def pick_icon(condition):
    condition = condition.lower()
    if "clear" in condition:
        return "assets/sunny.jpg"
    elif "cloud" in condition:
        return "assets/cloudy.jpg"
    elif "rain" in condition:
        return "assets/rain.jpg"
    elif "storm" in condition or "thunder" in condition:
        return "assets/storm.jpg"
    elif "snow" in condition:
        return "assets/snow.jpg"
    else:
        return "assets/mist.jpg"


# Main button
if st.button("Get Weather"):
    if not city:
        st.warning("Please enter a city name.")
    else:

        # CURRENT WEATHER
        if forecast_type == "Current Weather":
            data = get_weather(city)

            if data.get("cod") != 200:
                st.error("City not found.")
            else:
                condition = data["weather"][0]["description"].title()
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                wind = data["wind"]["speed"]

                icon_path = pick_icon(condition)
                img = Image.open(icon_path)

                st.markdown("### ☁️ Current Weather")
                st.image(img, width=150)

                # 3 Column layout
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.metric("Temperature", f"{temp} °C")
                    st.markdown("</div>", unsafe_allow_html=True)

                with col2:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.metric("Humidity", f"{humidity}%")
                    st.markdown("</div>", unsafe_allow_html=True)

                with col3:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.metric("Wind Speed", f"{wind} m/s")
                    st.markdown("</div>", unsafe_allow_html=True)

                st.success(f"Condition: {condition}")


        # 5-DAY FORECAST
        else:
            forecast = get_forecast(city)

            if forecast.get("cod") != "200":
                st.error("City not found.")
            else:
                st.markdown("## 📆 5-Day Forecast")

                # Forecast every 8 steps (24 hours)
                for x in range(0, 40, 8):
                    day = forecast["list"][x]
                    date = day["dt_txt"].split(" ")[0]
                    temp = day["main"]["temp"]
                    condition = day["weather"][0]["description"]

                    icon = pick_icon(condition)
                    img = Image.open(icon)

                    st.markdown(f"### 📅 {date}")
                    cols = st.columns([1,3])

                    with cols[0]:
                        st.image(img, width=100)

                    with cols[1]:
                        st.markdown("<div class='card'>", unsafe_allow_html=True)
                        st.write(f"**Temperature:** {temp} °C")
                        st.write(f"**Condition:** {condition.title()}")
                        st.markdown("</div>", unsafe_allow_html=True)
