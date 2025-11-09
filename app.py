import streamlit as st
import pandas as pd
from carbon_api import get_electricity_emissions

st.set_page_config(page_title="EcoCalculator 🌱", page_icon="🌍", layout="centered")
st.title("🔋 EcoCalculator: Your Daily Energy Impact Calculator")
st.write("Estimate your daily power usage and CO₂ footprint, then compare with your region!")

st.header("⚙️ Daily Usage")
computer_hours = st.slider("💻 Computer usage (hours/day)", 0, 12, 4)
light_bulbs = st.number_input("💡 Number of light bulbs used", 0, 10, 3)
ac_hours = st.slider("❄️ Air conditioner usage (hours/day)", 0, 12, 2)

computer_energy = 0.1 * computer_hours
lights_energy = 0.06 * light_bulbs * 4
ac_energy = 1.0 * ac_hours
total_daily_kwh = computer_energy + lights_energy + ac_energy
daily_co2_kg = total_daily_kwh * 0.42

st.header("📊 Your Daily Results")
st.metric("⚡ Total Energy", f"{total_daily_kwh:.2f} kWh/day")
st.metric("🌍 CO₂ Emissions", f"{daily_co2_kg:.2f} kg/day")

energy_data = pd.DataFrame({
    "Device": ["Computer", "Lights", "AC"],
    "kWh": [computer_energy, lights_energy, ac_energy]
})
st.bar_chart(energy_data.set_index("Device"))

if daily_co2_kg < 1.5:
    st.success("Great job! You're very energy-efficient 🌿")
elif daily_co2_kg < 3:
    st.warning("Not bad! You could save more with LED bulbs 💡")
else:
    st.error("High usage ⚠️ Try turning off devices when not in use!")

st.subheader("🌍 Compare Monthly CO₂ with Your Region")
monthly_kwh = total_daily_kwh * 30

region = st.selectbox(
    "Select your region for comparison:",
    ["United States", "Canada", "United Kingdom", "Germany", "India"]
)

country_codes = {
    "United States": "US",
    "Canada": "CA",
    "United Kingdom": "GB",
    "Germany": "DE",
    "India": "IN"
}
country = country_codes[region]

st.write("🔄 Fetching emissions data...")

user_data = get_electricity_emissions(zone=country, electricity_kwh=monthly_kwh)
avg_kwh_values = {
    "US": 400,
    "CA": 350,
    "GB": 300,
    "DE": 320,
    "IN": 250
}
avg_data = get_electricity_emissions(zone=country, electricity_kwh=avg_kwh_values[country])

if user_data and avg_data:
    try:
        user_co2 = user_data.get("emissions_kg", monthly_kwh * 0.42)
        avg_co2 = avg_data.get("emissions_kg", avg_kwh_values[country] * 0.42)
        percent_better = (1 - (user_co2 / avg_co2)) * 100

        st.divider()
        st.metric("Your Monthly CO₂", f"{user_co2:.2f} kg CO₂ / month")
        st.metric("Regional Average", f"{avg_co2:.2f} kg CO₂ / month")

        if percent_better >= 0:
            st.success(f"🌱 You emit {percent_better:.1f}% less CO₂ than the average in {region}")
        else:
            st.warning(f"⚠️ You emit {abs(percent_better):.1f}% more CO₂ than the average in {region}")

        comparison_df = pd.DataFrame({
            "Your Emissions": [user_co2],
            f"{region} Average": [avg_co2]
        })
        st.bar_chart(comparison_df)

    except Exception as e:
        st.error("Error processing Electricity Maps API data.")
        st.text(e)
else:
    st.error("Could not fetch emissions data. Please try again later.")

st.caption("Data provided by Electricity Maps. Made with ❤️ using Streamlit | Hackathon 2025 Entry")
