import boto3

sns = boto3.client('sns', region_name='ap-south-1')

TOPIC_ARN = 'arn:aws:sns:ap-south-1:084384979234:churn-alerts'

def send_alert(churn_rate, threshold=0.35):
    if churn_rate > threshold:
        message = f"""
⚠️ CHURN RATE ALERT

Current churn rate:  {churn_rate:.1%}
Threshold:           {threshold:.1%}
Status:              ABOVE THRESHOLD 🔴

Action required: Review high-risk customers immediately.

Pipeline:  churn-prediction-api
Model:     sagemaker-rf-v1
        """
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject='🔴 Churn Rate Alert — Action Required',
            Message=message
        )
        print(f"✅ Alert sent! {churn_rate:.1%} exceeds threshold")
    else:
        print(f"✅ {churn_rate:.1%} is within range — no alert needed")

# Test 1 — within range (our actual churn rate)
send_alert(0.265)

# Test 2 — above threshold (triggers alert)
send_alert(0.42)