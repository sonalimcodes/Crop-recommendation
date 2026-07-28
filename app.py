import streamlit as st
import pandas as pd
import joblib

import database
from auth import register_user, login_user

# Load model and scaler
model = joblib.load("crop_model.pkl")
scaler = joblib.load("scaler.pkl")

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# -----------------------------
# LOGIN / REGISTER
# -----------------------------
if not st.session_state.logged_in:

    st.title("🌱 Crop Recommendation System")

    menu = ["Login", "Create Account"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Create Account":

        st.subheader("Create Account")

        new_user = st.text_input("Username")

        new_password = st.text_input("Password", type="password")

        if st.button("Create Account"):

            if register_user(new_user, new_password):
                st.success("Account created successfully!")
                st.info("Please login.")

            else:
                st.error("Username already exists.")

    elif choice == "Login":

        st.subheader("Login")

        username = st.text_input("Username")

        password = st.text_input("Password", type="password")

        if st.button("Login"):

            user = login_user(username, password)

            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()

            else:
                st.error("Invalid username or password.")

# -----------------------------
# MAIN APPLICATION
# -----------------------------
else:

    st.title("🌱 Crop Recommendation System")

    st.success(f"Welcome, {st.session_state.username}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

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

        st.success(f"🌾 Recommended Crop: **{prediction[0]}**")
