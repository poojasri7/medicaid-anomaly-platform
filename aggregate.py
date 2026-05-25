import duckdb
con = duckdb.connect()

print("Aggregating provider stats...")
df = con.execute("""
    SELECT 
        SERVICING_PROVIDER_NPI_NUM as provider_id,
        HCPCS_CODE as billing_code,
        COUNT(*) as total_records,
        SUM(TOTAL_PATIENTS) as total_patients,
        SUM(TOTAL_CLAIM_LINES) as total_claims,
        SUM(TOTAL_PAID) as total_paid,
        AVG(TOTAL_PAID) as avg_paid_per_month,
        MAX(TOTAL_PAID) as max_paid_single_month,
        COUNT(DISTINCT CLAIM_FROM_MONTH) as active_months
    FROM read_csv_auto('/Users/poojasri/Downloads/medicaid-provider-spending.csv')
    GROUP BY SERVICING_PROVIDER_NPI_NUM, HCPCS_CODE
""").df()

print(f"Aggregated shape: {df.shape}")
print(df.describe())
df.to_csv('/Users/poojasri/provider_aggregated.csv', index=False)
print("\nSaved to provider_aggregated.csv")
