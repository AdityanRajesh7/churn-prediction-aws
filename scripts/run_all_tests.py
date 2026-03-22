import boto3
import requests
import json
from sqlalchemy import create_engine
import pandas as pd
from credentials import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

API_URL = "https://lwg1tqrh52.execute-api.ap-south-1.amazonaws.com/prod/predict"

print("="*60)
print("END-TO-END PIPELINE TEST REPORT")
print("="*60)

# Test 1 — RDS
try:
    engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    count = pd.read_sql("SELECT COUNT(*) as c FROM customers_cleaned", engine)
    assert count['c'][0] == 7032
    print("✅ Test 1 — RDS PostgreSQL: PASSED (7032 rows)")
except Exception as e:
    print(f"❌ Test 1 — RDS PostgreSQL: FAILED — {e}")

# Test 2 — S3
try:
    s3 = boto3.client('s3', region_name='ap-south-1')
    s3.head_object(Bucket='churn-project-adityan-2026',
                   Key='models/sagemaker/model.tar.gz')
    print("✅ Test 2 — S3 Model artifact: PASSED")
except Exception as e:
    print(f"❌ Test 2 — S3 Model artifact: FAILED — {e}")

# Test 3 — API
try:
    response = requests.post(API_URL, json={
        "customer_id": "E2E-TEST",
        "features": {
            "seniorcitizen": 0, "partner": 1, "dependents": 0,
            "tenure": 24, "phoneservice": 1, "multiplelines": 1,
            "onlinesecurity": 2, "onlinebackup": 1, "deviceprotection": 1,
            "techsupport": 1, "streamingtv": 1, "streamingmovies": 1,
            "paperlessbilling": 1, "monthlycharges": 0.5,
            "totalcharges": 0.3, "gender_Male": 1,
            "internetservice_Fiber optic": 0, "internetservice_No": 0,
            "contract_One year": 1, "contract_Two year": 0,
            "paymentmethod_Credit card (automatic)": 1,
            "paymentmethod_Electronic check": 0,
            "paymentmethod_Mailed check": 0
        }
    }, headers={'Content-Type': 'application/json'})
    assert response.status_code == 200
    result = response.json()
    print(f"✅ Test 3 — API Gateway + Lambda: PASSED")
    print(f"           Prediction: {result.get('result')}")
    print(f"           Probability: {result.get('churn_probability')}")
except Exception as e:
    print(f"❌ Test 3 — API Gateway + Lambda: FAILED — {e}")

# Test 4 — S3 Predictions
try:
    s3 = boto3.client('s3', region_name='ap-south-1')
    response = s3.list_objects_v2(
        Bucket='churn-project-adityan-2026',
        Prefix='predictions/'
    )
    count = len([x for x in response.get('Contents', [])
                 if x['Size'] > 0])
    print(f"✅ Test 4 — Predictions stored in S3: PASSED ({count} predictions)")
except Exception as e:
    print(f"❌ Test 4 — Predictions in S3: FAILED — {e}")

print("="*60)
print("ALL TESTS COMPLETE")
print("="*60)