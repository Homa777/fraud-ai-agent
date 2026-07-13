import psycopg2
import os
import random
from dotenv import load_dotenv
from faker import Faker

load_dotenv()
fake = Faker()

def generate_customers():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()

    # Get all unique account IDs from transactions
    cursor.execute("SELECT DISTINCT account_id FROM transactions")
    accounts = cursor.fetchall()
    print(f"📂 Found {len(accounts)} unique accounts")

    inserted = 0

    for account in accounts:
        account_id = account[0]
        customer_id = "CX-" + account_id

        # Generate fake customer data
        name        = fake.name()
        phone       = fake.numerify("416-###-####")
        email       = fake.email()
        card_number = fake.numerify("#### #### #### ####")
        card_type   = random.choice(["debit", "credit"])
        balance     = round(random.uniform(100, 10000), 2)

        # Insert into customers table
        cursor.execute("""
            INSERT INTO customers (customer_id, full_name, phone, email)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (customer_id) DO NOTHING
        """, (customer_id, name, phone, email))

        # Insert into accounts table
        cursor.execute("""
            INSERT INTO accounts (account_id, customer_id, card_number, card_type, balance)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (account_id) DO NOTHING
        """, (account_id, customer_id, card_number, card_type, balance))

        inserted += 1

    conn.commit()
    cursor.close()
    conn.close()

    print(f"✅ Created {inserted} customers and accounts!")

if __name__ == "__main__":
    generate_customers()