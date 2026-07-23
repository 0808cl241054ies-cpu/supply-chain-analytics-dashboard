import pandas as pd
import numpy as np
import scipy.stats as stats
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus

# 1. Data Generation & Preprocessing
def load_and_clean_data():
    """Supply chain data simulate karta hai."""
    np.random.seed(42)
    n_records = 1000
    
    data = {
        'SKU': np.random.choice(['SKU_Alpha', 'SKU_Beta', 'SKU_Gamma'], n_records),
        'Supplier_Name': np.random.choice(['Supplier_A', 'Supplier_B'], n_records),
        'Carrier': np.random.choice(['Carrier_X', 'Carrier_Y', 'Carrier_Z'], n_records),
        'Units_Sold': np.random.poisson(lam=45, size=n_records),
        'Stock_Level': np.random.randint(50, 500, size=n_records),
        'Lead_Time_Days': np.random.normal(loc=7, scale=2, size=n_records).clip(1, 20),
        'Manufacturing_Cost': np.random.uniform(10, 50, size=n_records),
        'Shipping_Cost': np.random.uniform(2, 15, size=n_records),
        'Revenue': np.random.uniform(100, 500, size=n_records),
        'Late_Delivery_Risk': np.random.choice([0, 1], p=[0.8, 0.2], size=n_records)
    }
    
    df = pd.DataFrame(data)
    df['Total_Cost'] = df['Manufacturing_Cost'] + df['Shipping_Cost']
    df['Profit'] = df['Revenue'] - df['Total_Cost']
    return df


# 2. Inventory Metrics (Safety Stock & Reorder Point)
def calculate_inventory_metrics(df, service_level=0.95):
    """Safety Stock aur Reorder Point (ROP) calculate karta hai."""
    z_score = stats.norm.ppf(service_level)
    
    metrics = []
    for sku, group in df.groupby('SKU'):
        avg_demand = group['Units_Sold'].mean()
        std_demand = group['Units_Sold'].std()
        
        avg_lead_time = group['Lead_Time_Days'].mean()
        std_lead_time = group['Lead_Time_Days'].std()
        
        safety_stock = z_score * np.sqrt((avg_lead_time * (std_demand**2)) + ((avg_demand**2) * (std_lead_time**2)))
        reorder_point = (avg_demand * avg_lead_time) + safety_stock
        
        metrics.append({
            'SKU': sku,
            'Avg_Daily_Demand': round(avg_demand, 2),
            'Avg_Lead_Time': round(avg_lead_time, 2),
            'Safety_Stock': int(np.ceil(safety_stock)),
            'Reorder_Point_ROP': int(np.ceil(reorder_point))
        })
        
    return pd.DataFrame(metrics)


# 3. Optimization Function (Linear Programming)
def optimize_carrier_allocation(demand_target=800):
    """Linear Programming se shipping cost minimize karta hai."""
    carriers = ['Carrier_X', 'Carrier_Y', 'Carrier_Z']
    costs = {'Carrier_X': 5.0, 'Carrier_Y': 3.5, 'Carrier_Z': 4.2}
    capacities = {'Carrier_X': 500, 'Carrier_Y': 400, 'Carrier_Z': 600}
    
    prob = LpProblem("Supply_Chain_Cost_Minimization", LpMinimize)
    ship_vars = LpVariable.dicts("Units", carriers, lowBound=0, cat='Continuous')
    
    # Objective Function
    prob += lpSum([costs[c] * ship_vars[c] for c in carriers])
    
    # Constraints
    prob += lpSum([ship_vars[c] for c in carriers]) >= demand_target, "Demand_Constraint"
    for c in carriers:
        prob += ship_vars[c] <= capacities[c], f"Capacity_Constraint_{c}"
        
    prob.solve()
    
    allocation = {c: ship_vars[c].varValue for c in carriers}
    total_cost = prob.objective.value()
    
    return allocation, total_cost, LpStatus[prob.status]


if __name__ == "__main__":
    df = load_and_clean_data()
    print("Backend script working correctly!")