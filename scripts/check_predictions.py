import boto3
import json

s3 = boto3.client('s3', region_name='ap-south-1')
BUCKET = 'churn-project-adityan-2026'

response = s3.list_objects_v2(Bucket=BUCKET, Prefix='predictions/')

if 'Contents' not in response:
    print("No predictions found yet")
else:
    print("="*55)
    print("PREDICTIONS STORED IN S3")
    print("="*55)

    valid = 0
    for obj in response['Contents']:
        try:
            data = s3.get_object(Bucket=BUCKET, Key=obj['Key'])
            body = data['Body'].read()
            if not body:  # skip empty files
                continue
            record = json.loads(body)
            result = "CHURN 🔴" if record['prediction'] == 1 else "STAY 🟢"
            print(f"Customer:    {record['customer_id']}")
            print(f"Result:      {result}")
            print(f"Probability: {record['churn_probability']}")
            print(f"Saved at:    {record['predicted_at']}")
            print(f"Model:       {record['model_version']}")
            print("-"*55)
            valid += 1
        except Exception as e:
            print(f"Skipping {obj['Key']} — {str(e)}")

    print(f"\nTotal valid predictions: {valid}")
    print("✅ S3 predictions verified!")