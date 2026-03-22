import pandas as pd
from sqlalchemy import create_engine
from credentials import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
# Load cleaned CSV
df = pd.read_csv(r"C:\Users\user\churn-project\data\telco-churn-cleaned.csv")

print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
print(df.head())
print(f"\nData types:\n{df.dtypes}")
print(f"\nNull values:\n{df.isnull().sum()}")

# Load into new table in PostgreSQL
df.to_sql('customers_cleaned', engine, if_exists='replace', index=False)

print(f"\n {len(df)} rows loaded into PostgreSQL table 'customers_cleaned'!")