import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, classification_report,
                             roc_auc_score, confusion_matrix)
import matplotlib.pyplot as plt
import seaborn as sns

# Load feature engineered data
df = pd.read_csv(r'C:\Users\user\churn-project\data\churn_features.csv')

output_dir = r"C:\Users\user\churn-project\plots"
os.makedirs(output_dir, exist_ok=True)

def save_plot(filename):
    plt.savefig(
        os.path.join(output_dir, filename),
        dpi=300,
        bbox_inches='tight'
    )
# ── STEP 1: Split features and target ────────────────────
X = df.drop(columns=['churn'])
y = df['churn']
print(f"Features: {X.shape[1]} columns")
print(f"Target distribution:\n{y.value_counts()}")

# ── STEP 2: Train/test split ──────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nTrain size: {X_train.shape[0]} rows")
print(f"Test size:  {X_test.shape[0]} rows")

# ── STEP 3: Train Random Forest ───────────────────────────
print("\nTraining Random Forest...")
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    class_weight='balanced'  # handles imbalanced churn data
)
rf_model.fit(X_train, y_train)
print("✅ Model trained!")

# ── STEP 4: Evaluate ──────────────────────────────────────
y_pred = rf_model.predict(X_test)
y_prob = rf_model.predict_proba(X_test)[:, 1]

print(f"\n{'='*40}")
print(f"MODEL EVALUATION")
print(f"{'='*40}")
print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
print(f"ROC-AUC:   {roc_auc_score(y_test, y_prob):.4f}")
print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")

# ── PLOT 1: Confusion Matrix ──────────────────────────────
plt.figure(figsize=(6, 5))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['No Churn', 'Churn'],
            yticklabels=['No Churn', 'Churn'])
plt.title('Confusion Matrix — Random Forest')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.tight_layout()
save_plot('plot7_confusion_matrix.png')
plt.show()
print("✅ Confusion matrix saved")

# ── PLOT 2: Feature Importance ────────────────────────────
feat_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False).head(15)

plt.figure(figsize=(10, 6))
sns.barplot(x='importance', y='feature', data=feat_importance, palette='viridis')
plt.title('Top 15 Most Important Features')
plt.tight_layout()
save_plot('plot8_feature_importance.png')
plt.show()
print("✅ Feature importance plot saved")

# ── STEP 5: Save model locally ────────────────────────────
joblib.dump(rf_model, r'C:/Users/user/churn-project/models/churn_model_rf.pkl')
print(f"\n✅ Model saved as churn_model_rf.pkl")
print(f"Model size: {round(__import__('os').path.getsize(r'C:/Users/user/churn-project/models/churn_model_rf.pkl')/1024, 1)} KB")