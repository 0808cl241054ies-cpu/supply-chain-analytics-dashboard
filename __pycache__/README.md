# 📦 Smart Supply Chain Analytics & Demand Forecasting Engine

An end-to-end Machine Learning and Supply Chain Optimization Web Application built with **Python**, **Streamlit**, and **Scikit-learn**.

![Streamlit Status](https://img.shields.io/badge/Streamlit-Live_Dashboard-FF4B4B?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)
![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn)

---

## 📌 Executive Summary
Supply chain disruptions and stockouts directly impact profitability. This project solves inventory management challenges by combining **Predictive Machine Learning** (Demand Forecasting) with **Operations Research Principles** (Dynamic Reorder Point & Safety Stock Buffer Calculations).

---

## 🔥 Key Features
* **Machine Learning Forecasting:** Trained Random Forest Regressor to predict daily product demand based on calendar seasonality and weekend spikes.
* **Dynamic Safety Stock & ROP:** Real-time calculation of Safety Stock and Reorder Points incorporating customizable supplier lead times and delay risk buffers.
* **Interactive What-If Scenario Analysis:** Sliders to simulate supplier delays (0–50%) and observe inventory buffer impacts live.
* **Interactive Data Visualization:** Dynamic 7-day demand trend projections rendered via **Plotly Splines**.

---

## 🛠️ Tech Stack
* **Language:** Python
* **Frontend / Web Framework:** Streamlit
* **Machine Learning:** Scikit-learn (Random Forest), Joblib
* **Data Manipulation & Visualization:** Pandas, NumPy, Plotly Express
* **Deployment:** Streamlit Cloud with Continuous Deployment via GitHub

---

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/mayank-lovanshi/supply-chain-analytics-dashboard.git](https://github.com/mayank-lovanshi/supply-chain-analytics-dashboard.git)
   cd supply-chain-analytics-dashboard