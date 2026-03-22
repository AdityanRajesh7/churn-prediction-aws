import psycopg2

conn = psycopg2.connect(
    host="churn-db.cvkawco2szg1.ap-south-1.rds.amazonaws.com",
    port=5432,
    database="churndb",
    user="postgres",
    password="Adi20082004"  # replace with your password
)

print("✅ Connected to RDS PostgreSQL successfully!")
conn.close()