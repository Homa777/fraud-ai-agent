import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def create_tables():
    conn = None
    cursor = None
    try:
        # Connect to Azure PostgreSQL
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cursor = conn.cursor()

        # Read your SQL file
        with open("db/schema.sql", "r") as f:
            sql = f.read()

        # Send SQL to Azure and create tables
        cursor.execute(sql)
        conn.commit()

        print("✅ All 5 tables created in Azure PostgreSQL!")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    create_tables()