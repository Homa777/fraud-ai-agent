import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def load_transactions():
    # Read CSV file
    df = pd.read_csv('data/raw/bank_transactions_data_2.csv')
    print(f"📂 Found {len(df)} transactions in CSV")

    # Connect to Azure PostgreSQL
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()

    inserted = 0
    skipped = 0

    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO transactions 
                (transaction_id, account_id, amount, merchant, location, timestamp, is_flagged)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (transaction_id) DO NOTHING
            """, (
                str(row['TransactionID']),
                str(row['AccountID']),
                float(row['TransactionAmount']),
                str(row['MerchantID']),
                str(row['Location']),
                str(row['TransactionDate']),
                False
            ))
            inserted += 1
        except Exception as e:
            skipped += 1

    conn.commit()
    cursor.close()
    conn.close()

    print(f"✅ Inserted: {inserted} transactions")
    print(f"⚠️  Skipped: {skipped} transactions")

if __name__ == "__main__":
    load_transactions()