import pandas as pd
from sqlalchemy import create_engine
from credentials import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

# Create connection
engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Load CSV
df = pd.read_csv("../data/telco-churn-raw.csv")

# Clean column names
df.columns = df.columns.str.lower().str.replace(' ', '_')

print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
print(df.head())

# Push to PostgreSQL
df.to_sql('customers', engine, if_exists='replace', index=False)

print(f"✅ {len(df)} rows loaded into PostgreSQL table 'customers'!")