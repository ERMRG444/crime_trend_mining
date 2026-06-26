import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_and_train():
    print("Generating synthetic data...")
    # 1. Random Forest Data (Area, Time Slot)
    # Let's say we have 5 areas, 24 hours.
    areas = ['North Sector', 'South Region', 'East Node', 'West Hub', 'Central District']
    data = []
    np.random.seed(42)
    for _ in range(2000):
        area = np.random.choice(areas)
        hour = np.random.randint(0, 24)
        # Higher crime in certain areas and at night
        prob = 0.2
        if area in ['North Sector', 'West Hub']:
            prob += 0.3
        if hour >= 20 or hour <= 4:
            prob += 0.4
        
        crime_occurred = np.random.rand() < prob
        data.append([area, hour, int(crime_occurred)])
        
    df = pd.DataFrame(data, columns=['Area', 'Hour', 'Crime'])
    
    # One-hot encode Area
    df_encoded = pd.get_dummies(df, columns=['Area'])
    
    X = df_encoded.drop('Crime', axis=1)
    y = df_encoded['Crime']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    import xgboost as xgb
    xgb_clf = xgb.XGBClassifier(n_estimators=100, random_state=42, use_label_encoder=False, eval_metric='logloss')
    xgb_clf.fit(X_train, y_train)
    
    acc = accuracy_score(y_test, xgb_clf.predict(X_test))
    print(f"XGBoost Accuracy: {acc:.2%}")
    
    # Save the model and columns
    model_data = {
        'model': xgb_clf,
        'columns': list(X.columns),
        'accuracy': acc
    }
    joblib.dump(model_data, os.path.join(BASE_DIR, 'xgb_model.joblib'))
    
    # 2. Daily Counts for ARIMA
    # Generate 30 days of data
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
    base_counts = np.linspace(100, 200, 30) + np.random.normal(0, 20, 30)
    counts_df = pd.DataFrame({'Date': dates, 'Count': base_counts.astype(int)})
    counts_df.to_csv(os.path.join(BASE_DIR, 'daily_counts.csv'), index=False)
    
    # 3. Incidents for DBSCAN (Lat, Lng)
    # Generate around 500 incidents in India
    # India bounding box roughly: lat 8 to 37, lng 68 to 97
    # Let's cluster them slightly around major cities to make DBSCAN interesting
    cities = [
        (28.6139, 77.2090), # Delhi
        (19.0760, 72.8777), # Mumbai
        (12.9716, 77.5946), # Bangalore
        (22.5726, 88.3639)  # Kolkata
    ]
    
    incidents = []
    for _ in range(400):
        city = cities[np.random.randint(0, len(cities))]
        lat = city[0] + np.random.normal(0, 0.5)
        lng = city[1] + np.random.normal(0, 0.5)
        incidents.append([lat, lng])
        
    for _ in range(100): # Noise
        lat = np.random.uniform(10, 35)
        lng = np.random.uniform(70, 90)
        incidents.append([lat, lng])
        
    incidents_df = pd.DataFrame(incidents, columns=['Lat', 'Lng'])
    incidents_df.to_csv(os.path.join(BASE_DIR, 'incidents.csv'), index=False)
    
    print("Done! Exported rf_model.joblib, daily_counts.csv, and incidents.csv.")

if __name__ == '__main__':
    generate_and_train()
