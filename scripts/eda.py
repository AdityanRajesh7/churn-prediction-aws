import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sqlalchemy import create_engine
from credentials import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

# Create connection
engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# ── OUTPUT DIRECTORY SETUP ─────────────────────────────
output_dir = r"C:\Users\user\churn-project\plots"
os.makedirs(output_dir, exist_ok=True)

def save_plot(filename):
    plt.savefig(
        os.path.join(output_dir, filename),
        dpi=300,
        bbox_inches='tight'
    )
    print(f"✅ Saved: {filename}")


# ── LOAD DATA ──────────────────────────────────────────
df = pd.read_sql("SELECT * FROM customers_cleaned", engine)
print(f"Shape: {df.shape}")
print(df.describe())

# ── PLOT 1: Overall Churn Distribution ─────────────────
plt.figure(figsize=(6, 4))
df['churn'].value_counts().plot(kind='bar', color=['steelblue', 'tomato'])
plt.title('Churn Distribution (0=No, 1=Yes)')
plt.xlabel('Churn')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.tight_layout()
save_plot('plot1_churn_distribution.png')
plt.show()

# ── PLOT 2: Churn Rate by Contract Type ────────────────
plt.figure(figsize=(8, 5))
contract_churn = df.groupby('contract')['churn'].mean() * 100
contract_churn.plot(kind='bar', color=['steelblue', 'orange', 'tomato'])
plt.title('Churn Rate by Contract Type (%)')
plt.xlabel('Contract')
plt.ylabel('Churn Rate (%)')
plt.xticks(rotation=0)
plt.tight_layout()
save_plot('plot2_churn_by_contract.png')
plt.show()

# ── PLOT 3: Tenure vs Churn ────────────────────────────
plt.figure(figsize=(7, 5))
sns.boxplot(x='churn', y='tenure', data=df, palette=['steelblue', 'tomato'])
plt.title('Tenure Distribution by Churn')
plt.xlabel('Churn (0=No, 1=Yes)')
plt.ylabel('Tenure (months)')
plt.tight_layout()
save_plot('plot3_tenure_vs_churn.png')
plt.show()

# ── PLOT 4: Monthly Charges vs Churn ───────────────────
plt.figure(figsize=(7, 5))
sns.boxplot(x='churn', y='monthlycharges', data=df, palette=['steelblue', 'tomato'])
plt.title('Monthly Charges by Churn')
plt.xlabel('Churn (0=No, 1=Yes)')
plt.ylabel('Monthly Charges ($)')
plt.tight_layout()
save_plot('plot4_monthlycharges_vs_churn.png')
plt.show()

# ── PLOT 5: Churn by Internet Service ──────────────────
plt.figure(figsize=(8, 5))
internet_churn = df.groupby('internetservice')['churn'].mean() * 100
internet_churn.plot(kind='bar', color=['steelblue', 'orange', 'tomato'])
plt.title('Churn Rate by Internet Service (%)')
plt.xlabel('Internet Service')
plt.ylabel('Churn Rate (%)')
plt.xticks(rotation=0)
plt.tight_layout()
save_plot('plot5_churn_by_internet.png')
plt.show()

# ── PLOT 6: Correlation Heatmap ────────────────────────
plt.figure(figsize=(8, 6))
numeric_cols = df[['tenure', 'monthlycharges', 'totalcharges', 'churn']]
sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap')
plt.tight_layout()
save_plot('plot6_correlation_heatmap.png')
plt.show()

print("\n✅ EDA complete — 6 plots saved in /plots folder!")