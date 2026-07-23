import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="Supply Chain & Inventory Optimization",
    page_icon="📦",
    layout="wide"
)

# Title & Description
st.title("📦 Smart Supply Chain Analytics & Forecasting Engine")
st.markdown("""
This end-to-end Data Science application predicts daily product demand using **Random Forest ML**, 
calculates dynamic **Reorder Points (ROP)**, and performs **What-If Risk Analysis** for supply chain optimization.
""")

st.markdown("---")

# 1. Model Loading
@st.cache_resource
def load_model():
    return joblib.load("demand_forecast_model.pkl")

try:
    model = load_model()
    st.sidebar.success("✅ Random Forest Model Loaded")
except Exception as e:
    st.sidebar.error("❌ Model file not found. Run model_training.py first.")
    st.stop()

# Sidebar Configuration
st.sidebar.header("⚙️ Simulation Controls")

selected_day = st.sidebar.selectbox(
    "Select Day of Week", 
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)
selected_month = st.sidebar.slider("Select Month", 1, 12, 6)
lead_time_days = st.sidebar.slider("Supplier Lead Time (Days)", 1, 14, 7)
supplier_delay_risk = st.sidebar.slider("Supplier Delay Buffer (%)", 0, 50, 10)

# Feature Encoding
day_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
day_num = day_map[selected_day]
is_weekend = 1 if day_num in [5, 6] else 0

# ML Prediction
input_features = np.array([[day_num, selected_month, is_weekend]])
predicted_demand = int(model.predict(input_features)[0])

# Inventory Calculation Logic
adjusted_lead_time = lead_time_days * (1 + (supplier_delay_risk / 100))
safety_stock = int(predicted_demand * 0.25 * (1 + supplier_delay_risk / 100))
reorder_point = int((predicted_demand * adjusted_lead_time) + safety_stock)

# Top Metrics Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Predicted Daily Demand", f"{predicted_demand} units")
col2.metric("Effective Lead Time", f"{adjusted_lead_time:.1f} days", f"+{supplier_delay_risk}% Delay Risk")
col3.metric("Safety Stock Buffer", f"{safety_stock} units")
col4.metric("Reorder Point (ROP)", f"{reorder_point} units")

st.markdown("---")

# 2. Visualization & Analytics Section
col_chart, col_details = st.columns([2, 1])

with col_chart:
    st.subheader("📈 7-Day Demand Forecast Trend")
    
    # Generate 7-day projection starting from selected day
    days_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    start_idx = day_map[selected_day]
    forecast_days = [days_list[(start_idx + i) % 7] for i in range(7)]
    
    features_7d = []
    for d in forecast_days:
        d_num = day_map[d]
        features_7d.append([d_num, selected_month, 1 if d_num in [5, 6] else 0])
        
    preds_7d = model.predict(features_7d)
    
    chart_df = pd.DataFrame({
        "Day": forecast_days,
        "Predicted Demand": preds_7d
    })
    
    fig = px.line(
        chart_df, x="Day", y="Predicted Demand", markers=True,
        title="Projected Demand Across Next 7 Days",
        line_shape="spline"
    )
    fig.update_traces(line_color="#2E86C1", line_width=3, marker_size=8)
    st.plotly_chart(fig, use_container_width=True)

with col_details:
    st.subheader("🔍 What-If Analysis")
    st.info(f"""
    **Current Operational Status:**
    - **Base Lead Time:** {lead_time_days} days
    - **Risk Factor:** {supplier_delay_risk}% supplier delay expected
    
    **Action Items:**
    - Trigger purchase order when inventory drops to **{reorder_point} units**.
    - Maintain minimum **{safety_stock} units** to prevent stockouts during supply spikes.
    """)