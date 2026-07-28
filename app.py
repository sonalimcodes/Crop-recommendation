import streamlit as st
import pandas as pd
import joblib

# Load model and scaler
model = joblib.load("crop_model.pkl")
scaler = joblib.load("scaler.pkl")

st.title(" 🌱 Crop Recommendation System")

st.write("Enter the soil and weather details below.")

N = st.number_input("Nitrogen (N)", value=90)
P = st.number_input("Phosphorous (P)", value=42)
K = st.number_input("Potassium (K)", value=43)
temperature = st.number_input("Temperature (°C)", value=20.8)
humidity = st.number_input("Humidity (%)", value=82.0)
ph = st.number_input("Soil pH", value=6.5)
rainfall = st.number_input("Rainfall (mm)", value=202.9)

if st.button("Predict Crop"):

    features = pd.DataFrame([{
        "N": N,
        "P": P,
        "K": K,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall
    }])

    features_scaled = scaler.transform(features)

    prediction = model.predict(features_scaled)

    st.success(f"Recommended Crop: **{prediction[0]}**")
