import psycopg2
import os
import random
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

# ─────────────────────────────────────────
# TOOL 1 — Verify Customer
# ─────────────────────────────────────────
def verify_customer(full_name: str, card_number: str):
    """
    Step 1: Check if customer exists in database
    using their name and card number
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.customer_id, c.full_name, c.phone, a.card_number
        FROM customers c
        JOIN accounts a ON c.customer_id = a.customer_id
        WHERE LOWER(c.full_name) = LOWER(%s)
        AND a.card_number = %s
    """, (full_name, card_number))

    customer = cursor.fetchone()
    cursor.close()
    conn.close()

    if not customer:
        return {
            "verified": False,
            "message": "Sorry, I could not find your account. Please check your name and card number."
        }

    return {
        "verified": True,
        "customer_id": customer[0],
        "full_name":   customer[1],
        "phone":       customer[2],
        "message":     f"Thank you {customer[1]}! I found your account."
    }


def send_otp(phone: str):
    """
    Step 2: Generate and send OTP to customer phone
    For learning purposes OTP is always 1234
    """
    otp = "1234"  # simulated OTP
    print(f"📱 OTP sent to {phone}: {otp}")
    return {
        "otp":     otp,
        "message": f"I have sent a verification code to your phone number on file ending in {phone[-4:]}. Please provide the code."
    }


def verify_otp(entered_otp: str, real_otp: str):
    """
    Step 3: Verify the OTP customer provides
    """
    if entered_otp == real_otp:
        return {
            "verified": True,
            "message":  "✅ Identity verified successfully! How can I help you today?"
        }
    else:
        return {
            "verified": False,
            "message":  "❌ Incorrect code. Please try again."
        }


# ─────────────────────────────────────────
# TOOL 2 — Get Customer Transactions
# ─────────────────────────────────────────
def get_transactions(account_id: str):
    """
    Get last 10 transactions for customer account
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT transaction_id, amount, merchant, location, timestamp
        FROM transactions
        WHERE account_id = %s
        ORDER BY timestamp DESC
        LIMIT 10
    """, (account_id,))

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        return {
            "found": False,
            "message": "No transactions found for this account."
        }

    transactions = []
    for i, row in enumerate(rows):
        transactions.append({
            "number":         i + 1,
            "transaction_id": row[0],
            "amount":         row[1],
            "merchant":       row[2],
            "location":       row[3],
            "date":           str(row[4]),
        })

    return {
        "found":        True,
        "account_id":   account_id,
        "transactions": transactions,
        "message":      f"Here are your last {len(transactions)} transactions."
    }


# ─────────────────────────────────────────
# TOOL 3 — Submit Fraud Claim
# ─────────────────────────────────────────
def submit_fraud_claim(customer_id: str, account_id: str, transaction_ids: list):
    """
    Submit a fraud claim for disputed transactions
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Generate claim ID
    cursor.execute("SELECT COUNT(*) FROM fraud_claims")
    count    = cursor.fetchone()[0]
    claim_id = f"CLM-{str(count + 1).zfill(6)}"

    # Save fraud claim
    cursor.execute("""
        INSERT INTO fraud_claims 
        (claim_id, customer_id, account_id, transactions)
        VALUES (%s, %s, %s, %s)
    """, (
        claim_id,
        customer_id,
        account_id,
        ", ".join(transaction_ids)
    ))

    # Save claim status
    cursor.execute("""
        INSERT INTO claim_status (claim_id, status, update_note)
        VALUES (%s, %s, %s)
    """, (
        claim_id,
        "Under Investigation",
        "Your claim has been received and is being reviewed by our fraud team."
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "success":  True,
        "claim_id": claim_id,
        "message":  f"Your fraud claim {claim_id} has been submitted successfully. Our fraud team is investigating and will provide an update within 30 business days."
    }