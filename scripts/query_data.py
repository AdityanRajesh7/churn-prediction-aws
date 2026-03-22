import pandas as pd
from sqlalchemy import create_engine
from credentials import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# 1. Basic check - first 5 rows
print("=== FIRST 5 ROWS ===")
df = pd.read_sql("SELECT * FROM customers LIMIT 5", engine)
print(df[['customerid', 'gender', 'tenure', 'monthlycharges', 'churn']])

# 2. How many churned vs not churned?
print("\n=== CHURN COUNTS ===")
result = pd.read_sql("SELECT churn, COUNT(*) as count FROM customers GROUP BY churn", engine)
print(result)

# 3. Average monthly charges by contract type
print("\n=== AVG CHARGES BY CONTRACT ===")
result = pd.read_sql("""
    SELECT contract, 
           ROUND(AVG(monthlycharges)::numeric, 2) as avg_monthly_charge,
           COUNT(*) as total_customers
    FROM customers 
    GROUP BY contract
    ORDER BY avg_monthly_charge DESC
""", engine)
print(result)

# 4. Churn rate by contract type
print("\n=== CHURN RATE BY CONTRACT ===")
result = pd.read_sql("""
    SELECT contract,
           COUNT(*) as total,
           SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) as churned,
           ROUND(100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) as churn_rate_pct
    FROM customers
    GROUP BY contract
    ORDER BY churn_rate_pct DESC
""", engine)
print(result)

# 5. Senior citizens churn rate
print("\n=== SENIOR CITIZEN CHURN ===")
result = pd.read_sql("""
    SELECT seniorcitizen,
           COUNT(*) as total,
           SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) as churned,
           ROUND(100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) as churn_rate_pct
    FROM customers
    GROUP BY seniorcitizen
    ORDER BY seniorcitizen
""", engine)
print(result)

print("\n✅ All queries ran successfully!")