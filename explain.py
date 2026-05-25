import pandas as pd
import numpy as np

df = pd.read_csv('/Users/poojasri/anomaly_results.csv')
anomalies = df[df['is_anomaly'] == True].copy()

# Calculate national averages
avg_patients = df['total_patients'].mean()
avg_paid = df['total_paid'].mean()
avg_claims = df['total_claims'].mean()

def explain_anomaly(row):
    reasons = []
    
    if row['total_patients'] > avg_patients * 10:
        ratio = row['total_patients'] / avg_patients
        reasons.append(f"Serves {ratio:.1f}x more patients than national average")
    
    if row['total_paid'] > avg_paid * 10:
        ratio = row['total_paid'] / avg_paid
        reasons.append(f"Billed {ratio:.1f}x more than national average")
    
    if row['total_claims'] > avg_claims * 10:
        ratio = row['total_claims'] / avg_claims
        reasons.append(f"Filed {ratio:.1f}x more claims than national average")
    
    if pd.isna(row['provider_id']):
        reasons.append("No registered NPI number — anonymous billing entity")
    
    if row['max_paid_single_month'] > avg_paid * 50:
        reasons.append(f"Single month billing spike: ${row['max_paid_single_month']:,.0f}")
    
    return " | ".join(reasons) if reasons else "Statistical outlier across multiple dimensions"

print("Generating explanations...")
anomalies['explanation'] = anomalies.apply(explain_anomaly, axis=1)

# Show top 10
top10 = anomalies.sort_values('anomaly_probability').head(10)
for _, row in top10.iterrows():
    print(f"\nProvider: {row['provider_id']} | Code: {row['billing_code']}")
    print(f"Patients: {row['total_patients']:,.0f} | Total Paid: ${row['total_paid']:,.0f}")
    print(f"Reason: {row['explanation']}")

anomalies.to_csv('/Users/poojasri/anomalies_explained.csv', index=False)
print("\nSaved to anomalies_explained.csv")
