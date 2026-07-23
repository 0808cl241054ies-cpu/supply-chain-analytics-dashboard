import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib

def generate_synthetic_data(samples=1000):
    np.random.seed(42)
    dates = pd.date_range(start="2024-01-01", periods=samples, freq="D")
    
    # Feature Engineering
    df = pd.DataFrame({'date': dates})
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    # Target: Base demand + seasonality + noise
    base_demand = 150
    seasonality = np.sin(df['month'] * (2 * np.pi / 12)) * 30
    weekend_spike = df['is_weekend'] * 20
    noise = np.random.normal(0, 10, samples)
    
    df['demand'] = (base_demand + seasonality + weekend_spike + noise).astype(int)
    return df

def train_and_save_model():
    df = generate_synthetic_data()
    X = df[['day_of_week', 'month', 'is_weekend']]
    y = df['demand']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    print(f"Model Trained Successfully!")
    print(f"R2 Score: {r2_score(y_test, preds):.2f}")
    print(f"RMSE: {np.sqrt(mean_squared_error(y_test, preds)):.2f}")
    
    # Save model artifact
    joblib.dump(model, 'demand_forecast_model.pkl')
    print("Model saved as 'demand_forecast_model.pkl'")

if __name__ == "__main__":
    train_and_save_model()