Supply Chain Analytics and Inventory Optimization Dashboard

An AI driven interactive web dashboard that combines Machine Learning demand forecasting with dynamic safety stock and Reorder Point (ROP) calculation logic.

Key Features
. ML Demand Forecasting: Predicts daily and monthly product demand using a trained Random Forest Regressor.
. Dynamic Risk Simulation: Allows interactive slider adjustments for Lead Time delays and safety buffers.
. Automated Reorder Point Alerts: Calculates exact inventory thresholds to prevent stockouts and reduce excess holding costs.
. Interactive Visualizations: Built-in dynamic Plotly charts for real-time trend analysis.

Tech Stack
. Language: Python
. Machine Learning: Scikit-Learn (Random Forest)
. Web Dashboard: Streamlit
. Data Processing and Visualization: Pandas, Plotly
. Deployment: Streamlit Cloud

How to Run Locally

Clone the repository:
git clone(https://supply-chain-analytics-dashboard-l84j3e6vwpjq3mbhkpbzyt.streamlit.app/)

Install required packages:
pip install -r requirements.txt

Launch the Streamlit app:
streamlit run app.py
