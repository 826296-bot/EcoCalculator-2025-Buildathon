import requests
import streamlit as st
import os
API_KEY = "Klh7ZZpwQYHhEOmG7Hd2"
BASE_URL = "https://api.electricitymaps.com/v3"

def get_electricity_emissions(zone="US", electricity_kwh=0):
    try:
        url = f"{BASE_URL}/carbon-intensity/latest?zone={zone}"
        headers = {"auth-token": API_KEY}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            intensity_g = data.get("carbonIntensity")
            if intensity_g is None:
                st.error("No carbon intensity value in response.")
                return None
            emissions_kg = electricity_kwh * (intensity_g / 1000.0)
            return {"emissions_kg": emissions_kg, "intensity_gCO2_per_kWh": intensity_g}
        else:
            st.error(f"Electricity Maps API error {resp.status_code}: {resp.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Network error with Electricity Maps API: {e}")
        return None
