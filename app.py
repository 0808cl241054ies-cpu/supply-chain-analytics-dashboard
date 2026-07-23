import streamlit as st
import pandas as pd
import plotly.express as px

# Backend script se functions import kar rahe hain
from supply_chain_analysis import (
    load_and_clean_data, 
    calculate_inventory_metrics, 
    optimize_carrier_allocation
)

# Page configuration
st.set_page_config(
    page_title="Supply Chain Analytics Dashboard",
    page_icon="📦",
    layout="wide"
)

# Title & Description
st.title("📦 End-to-End Supply Chain Analytics & Optimization")
st.markdown("Automated Inventory Planning, Risk Analysis, and Route Cost Minimization.")

# Data load kar rahe hain
@st.cache_data
def get_data():
    return load_and_clean_data()

df = get_data()

# ==========================================
# SIDEBAR CONTROLS
# ==========================================
st.sidebar.header("⚙️ Configuration Panel")
st.sidebar.subheader("Inventory Policy Settings")

service_level = st.sidebar.slider(
    "Target Service Level (Z-Score)", 
    min_value=0.80, 
    max_value=0.99, 
    value=0.95, 
    step=0.01,
    help="Higher service level means more buffer stock to avoid stockouts."
)

st.sidebar.subheader("Carrier Allocation Settings")
target_demand = st.sidebar.number_input(
    "Target Shipment Volume (Units)", 
    min_value=100, 
    max_value=1500, 
    value=800,
    step=50
)

# ==========================================
# DASHBOARD TABS
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "📊 Executive Overview", 
    "🎯 Inventory Control (ROP)", 
    "⚡ Route Optimization (PuLP)"
])

# ------------------------------------------
# TAB 1: EXECUTIVE OVERVIEW
# ------------------------------------------
with tab1:
    st.subheader("Key Performance Indicators (KPIs)")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${df['Revenue'].sum():,.2f}")
    col2.metric("Total Profit", f"${df['Profit'].sum():,.2f}")
    col3.metric("Avg Lead Time", f"{df['Lead_Time_Days'].mean():.1f} Days")
    col4.metric("Late Delivery Risk", f"{(df['Late_Delivery_Risk'].mean()*100):.1f}%")
    
    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Revenue vs Total Cost by Supplier")
        fig_supplier = px.histogram(
            df, 
            x="Supplier_Name", 
            y="Revenue", 
            color="SKU", 
            barmode="group",
            title="Revenue Distribution Across Suppliers"
        )
        st.plotly_chart(fig_supplier, use_container_width=True)
        
    with col_chart2:
        st.subheader("Profitability by Carrier")
        fig_carrier = px.box(
            df, 
            x="Carrier", 
            y="Profit", 
            color="Carrier",
            title="Profit Margin Distribution per Carrier"
        )
        st.plotly_chart(fig_carrier, use_container_width=True)

# ------------------------------------------
# TAB 2: INVENTORY CONTROL (ROP & SAFETY STOCK)
# ------------------------------------------
with tab2:
    st.subheader("Safety Stock & Reorder Point (ROP) Analysis")
    st.info(f"Currently calculating buffers for a **{int(service_level*100)}% Service Level**.")
    
    inv_df = calculate_inventory_metrics(df, service_level=service_level)
    
    # Table display
    st.dataframe(inv_df, use_container_width=True)
    
    # Visual Chart
    fig_rop = px.bar(
        inv_df, 
        x="SKU", 
        y=["Safety_Stock", "Reorder_Point_ROP"],
        title="Safety Stock vs Total Reorder Point per SKU",
        barmode="group",
        labels={"value": "Units", "variable": "Metric"}
    )
    st.plotly_chart(fig_rop, use_container_width=True)

# ------------------------------------------
# TAB 3: ROUTE OPTIMIZATION
# ------------------------------------------
with tab3:
    st.subheader("Linear Programming Cost Minimization")
    
    alloc, min_cost, status = optimize_carrier_allocation(demand_target=target_demand)
    
    col_opt1, col_opt2 = st.columns(2)
    
    with col_opt1:
        st.success(f"Optimization Solver Status: **{status}**")
        st.metric("Total Minimum Transportation Cost", f"${min_cost:,.2f}")
        
        alloc_df = pd.DataFrame(list(alloc.items()), columns=['Carrier', 'Assigned_Units'])
        st.subheader("Optimal Unit Distribution")
        st.table(alloc_df)
        
    with col_opt2:
        fig_pie = px.pie(
            alloc_df, 
            values='Assigned_Units', 
            names='Carrier', 
            title=f"Carrier Capacity Allocation for {target_demand} Units"
        )
        st.plotly_chart(fig_pie, use_container_width=True)