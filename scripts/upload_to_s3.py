import boto3
import os

s3 = boto3.client('s3', region_name='ap-south-1')

BUCKET = 'churn-project-adityan-2026'

# Upload feature engineered data to S3
s3.upload_file(r'C:\Users\user\churn-project\data\churn_features.csv',
    BUCKET,
    'processed-data/churn_features.csv'
)
print("✅ churn_features.csv uploaded to S3 processed-data/")

# Upload both models too
s3.upload_file(
    '../models/churn_model_rf.pkl',
    BUCKET,
    'models/churn_model_rf.pkl'
)
print("✅ churn_model_rf.pkl uploaded to S3 models/")

s3.upload_file(
    '../models/churn_model_xgb.pkl',
    BUCKET,
    'models/churn_model_xgb.pkl'
)
print("✅ churn_model_xgb.pkl uploaded to S3 models/")

print("\n✅ All files uploaded to S3 successfully!")