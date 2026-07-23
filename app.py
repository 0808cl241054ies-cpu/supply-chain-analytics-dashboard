import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Page Config
st.set_page_config(page_title="Supply Chain Analytics Dashboard", layout="wide")

st.title("📦 Supply Chain Analytics & Demand Forecasting")

# Model Loading
@st.cache_resource
def load_model():
    return joblib.load("demand_forecast_model.pkl")

try:
    model = load_model()
    st.sidebar.success("ML Model Loaded Successfully!")
except Exception as e:
    st.sidebar.error("Model file not found. Run model_training.py first.")

# Sidebar Inputs for ML Prediction
st.sidebar.header("🔮 Demand Predictor Settings")
selected_day = st.sidebar.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
selected_month = st.sidebar.slider("Month", 1, 12, 6)

# Map day to integer (0=Monday, 6=Sunday)
day_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
day_num = day_map[selected_day]
is_weekend = 1 if day_num in [5, 6] else 0

# Predict Target Demand
input_features = np.array([[day_num, selected_month, is_weekend]])
predicted_demand = int(model.predict(input_features)[0])

# Dashboard Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Predicted Daily Demand", f"{predicted_demand} units")
col2.metric("Recommended Safety Stock", f"{int(predicted_demand * 0.2)} units")
col3.metric("Reorder Point (ROP)", f"{int(predicted_demand * 1.5)} units")

st.markdown("---")
st.subheader("📊 Forecast Summary")
st.write(f"Selected Day: **{selected_day}** | Month: **{selected_month}** | Weekend Status: **{'Yes' if is_weekend else 'No'}**")