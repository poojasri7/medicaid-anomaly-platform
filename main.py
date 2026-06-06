import pandas as pd
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import io

app = FastAPI(title="Medicaid Anomaly Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load precomputed anomalies
df = pd.read_csv('anomalies_explained.csv')
df = df[df['is_anomaly'] == True].fillna('Unknown')

@app.get("/")
def root():
    return {"message": "Medicaid Anomaly Detection API", "total_anomalies": len(df)}

@app.get("/anomalies")
def get_anomalies(limit: int = 50, min_paid: float = 0):
    filtered = df[df['total_paid'] >= min_paid]
    filtered = filtered.sort_values('anomaly_probability').head(limit)
    return filtered[['provider_id', 'billing_code', 'total_patients', 
                      'total_paid', 'anomaly_probability', 'explanation']].to_dict(orient='records')

@app.get("/anomalies/{provider_id}")
def get_provider(provider_id: str):
    result = df[df['provider_id'].astype(str) == provider_id]
    if result.empty:
        return {"error": "Provider not found"}
    return result.to_dict(orient='records')

@app.get("/stats")
def get_stats():
    return {
        "total_anomalies": len(df),
        "unknown_providers": int((df['provider_id'] == 'Unknown').sum()),
        "total_paid_flagged": float(df['total_paid'].sum()),
        "avg_patients_flagged": float(df['total_patients'].mean()),
        "top_billing_codes": df['billing_code'].value_counts().head(5).to_dict()
    }

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    uploaded_df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    return {
        "filename": file.filename,
        "rows": len(uploaded_df),
        "columns": list(uploaded_df.columns),
        "message": "File received. Anomaly detection would run here."
    }
