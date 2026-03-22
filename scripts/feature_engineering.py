import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.preprocessing import LabelEncoder, StandardScaler
from credentials import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

# Create connection
engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",pool_pre_ping=True,
    pool_recycle=300
)


# Pull cleaned data
df = pd.read_sql("SELECT * FROM customers_cleaned", engine)
print(f"Original shape: {df.shape}")

# ── STEP 1: Drop customerid (not useful for ML) ──────────
df = df.drop(columns=['customerid'])

# ── STEP 2: Encode binary columns (Yes/No → 1/0) ─────────
binary_cols = [
    'partner', 'dependents', 'phoneservice', 'paperlessbilling',
    'seniorcitizen'
]
for col in binary_cols:
    df[col] = df[col].map({'Yes': 1, 'No': 0})

# ── STEP 3: Encode columns with 3 values ─────────────────
# (No phone service / No / Yes) → map to 0, 1, 2
three_val_cols = [
    'multiplelines', 'onlinesecurity', 'onlinebackup',
    'deviceprotection', 'techsupport', 'streamingtv', 'streamingmovies'
]
for col in three_val_cols:
    df[col] = df[col].map({
        'No internet service': 0,
        'No phone service': 0,
        'No': 1,
        'Yes': 2
    })

# ── STEP 4: One-hot encode multi-category columns ─────────
df = pd.get_dummies(df, columns=['gender', 'internetservice',
                                  'contract', 'paymentmethod'],
                    drop_first=True)

# ── STEP 5: Convert boolean columns to int ────────────────
bool_cols = df.select_dtypes(include='bool').columns
df[bool_cols] = df[bool_cols].astype(int)

# ── STEP 6: Scale numeric columns ────────────────────────
scaler = StandardScaler()
numeric_cols = ['tenure', 'monthlycharges', 'totalcharges']
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

print(f"Engineered shape: {df.shape}")
print(f"\nColumns: {list(df.columns)}")
print(f"\nSample:\n{df.head(3)}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nNull values: {df.isnull().sum().sum()}")

# ── STEP 7: Save to PostgreSQL ────────────────────────────
from sqlalchemy import text

# Dispose old engine and create fresh one
engine.dispose()
engine2 = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_pre_ping=True,
    pool_recycle=300,
    isolation_level="AUTOCOMMIT"
)

# Drop table first then write
with engine2.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS customers_features"))

df.to_sql('customers_features', engine2, if_exists='replace', index=False)
print(f"\n✅ Feature engineered data saved to PostgreSQL table 'customers_features'!")