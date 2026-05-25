import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Load aggregated data
print("Loading aggregated data...")
df = pd.read_csv('/Users/poojasri/provider_aggregated.csv')

# Features for anomaly detection
features = ['total_records', 'total_patients', 'total_claims', 
            'total_paid', 'avg_paid_per_month', 'max_paid_single_month', 'active_months']

X = df[features].fillna(0)

# Scale features
print("Scaling features...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train Isolation Forest
print("Training Isolation Forest...")
model = IsolationForest(
    n_estimators=100,
    contamination=0.01,  # assume 1% of providers are anomalous
    random_state=42,
    n_jobs=-1
)
df['anomaly_score'] = model.fit_predict(X_scaled)
df['anomaly_probability'] = model.score_samples(X_scaled)

# Flag anomalies
df['is_anomaly'] = df['anomaly_score'] == -1

# Summary
print(f"\nTotal providers analyzed: {len(df):,}")
print(f"Flagged as anomalies: {df['is_anomaly'].sum():,}")
print(f"\nTop 10 most anomalous providers:")
top = df[df['is_anomaly']].sort_values('anomaly_probability').head(10)
print(top[['provider_id', 'billing_code', 'total_patients', 'total_paid', 'anomaly_probability']])

# Save results
df.to_csv('/Users/poojasri/anomaly_results.csv', index=False)
print("\nSaved to anomaly_results.csv")
