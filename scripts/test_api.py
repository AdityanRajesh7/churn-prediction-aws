import requests
import json

API_URL = "https://lwg1tqrh52.execute-api.ap-south-1.amazonaws.com/prod/predict"

# ── HIGH RISK customer ───────────────────────────────────
# Senior, month-to-month, fiber optic, electronic check
high_risk = {
    "customer_id": "TEST-HIGH-RISK",
    "features": {
        "seniorcitizen": 1,
        "partner": 0,
        "dependents": 0,
        "tenure": 2,
        "phoneservice": 1,
        "multiplelines": 2,
        "onlinesecurity": 1,
        "onlinebackup": 1,
        "deviceprotection": 1,
        "techsupport": 1,
        "streamingtv": 2,
        "streamingmovies": 2,
        "paperlessbilling": 1,
        "monthlycharges": 1.5,
        "totalcharges": -0.8,
        "gender_Male": 1,
        "internetservice_Fiber optic": 1,
        "internetservice_No": 0,
        "contract_One year": 0,
        "contract_Two year": 0,
        "paymentmethod_Credit card (automatic)": 0,
        "paymentmethod_Electronic check": 1,
        "paymentmethod_Mailed check": 0
    }
}

# ── LOW RISK customer ────────────────────────────────────
# Two-year contract, long tenure, bank transfer
low_risk = {
    "customer_id": "TEST-LOW-RISK",
    "features": {
        "seniorcitizen": 0,
        "partner": 1,
        "dependents": 1,
        "tenure": 60,
        "phoneservice": 1,
        "multiplelines": 0,
        "onlinesecurity": 2,
        "onlinebackup": 2,
        "deviceprotection": 2,
        "techsupport": 2,
        "streamingtv": 0,
        "streamingmovies": 0,
        "paperlessbilling": 0,
        "monthlycharges": -0.8,
        "totalcharges": 1.2,
        "gender_Male": 0,
        "internetservice_Fiber optic": 0,
        "internetservice_No": 0,
        "contract_One year": 0,
        "contract_Two year": 1,
        "paymentmethod_Credit card (automatic)": 1,
        "paymentmethod_Electronic check": 0,
        "paymentmethod_Mailed check": 0
    }
}

# ── Test both ────────────────────────────────────────────
print("="*55)
print("TESTING CHURN PREDICTION API")
print("="*55)

for customer in [high_risk, low_risk]:
    print(f"\nCustomer: {customer['customer_id']}")
    print("-"*40)

    response = requests.post(
        API_URL,
        json=customer,
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 200:
        result = response.json()
        # Handle both direct and wrapped responses
        if 'body' in result:
            result = json.loads(result['body'])

        print(f"Status:      {response.status_code} ✅")
        print(f"Prediction:  {result.get('result')}")
        print(f"Probability: {result.get('churn_probability')}")
        print(f"Risk Level:  {result.get('risk_level')}")
        print(f"Model:       {result.get('model_version')}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

print("\n" + "="*55)
print("✅ API test complete!")