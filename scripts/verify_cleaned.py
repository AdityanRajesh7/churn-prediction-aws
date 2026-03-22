import pandas as pd
from sqlalchemy import create_engine
from credentials import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
# Compare raw vs cleaned tables
raw_count = pd.read_sql("SELECT COUNT(*) as count FROM customers", engine)
clean_count = pd.read_sql("SELECT COUNT(*) as count FROM customers_cleaned", engine)
print(f"Raw table rows:     {raw_count['count'][0]}")
print(f"Cleaned table rows: {clean_count['count'][0]}")

# Verify churn is now 0/1
churn_check = pd.read_sql("""
    SELECT churn, COUNT(*) as count 
    FROM customers_cleaned 
    GROUP BY churn
""", engine)
print(f"\nChurn distribution (0=No, 1=Yes):\n{churn_check}")

# Verify no nulls in key columns
null_check = pd.read_sql("""
    SELECT 
        SUM(CASE WHEN totalcharges IS NULL THEN 1 ELSE 0 END) as null_totalcharges,
        SUM(CASE WHEN churn IS NULL THEN 1 ELSE 0 END) as null_churn,
        SUM(CASE WHEN customerid IS NULL THEN 1 ELSE 0 END) as null_customerid
    FROM customers_cleaned
""", engine)
print(f"\nNull check:\n{null_check}")

print("\n Pipeline verified — raw → Glue → cleaned → RDS complete!")