import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.tools import tool
from tools.fraud_tools import (
    verify_customer,
    send_otp,
    verify_otp,
    get_transactions,
    submit_fraud_claim
)

load_dotenv()

# ─────────────────────────────────────────
# STEP 1 — Wrap tools for LangChain
# ─────────────────────────────────────────
@tool
def tool_verify_customer(full_name: str, card_number: str) -> str:
    """
    Verify customer identity using their full name and card number.
    Use this first when customer calls.
    """
    return str(verify_customer(full_name, card_number))

@tool
def tool_send_otp(phone: str) -> str:
    """
    Send OTP verification code to customer phone number.
    Use this after verifying customer name and card number.
    """
    return str(send_otp(phone))

@tool
def tool_verify_otp(entered_otp: str, real_otp: str) -> str:
    """
    Verify the OTP code provided by the customer.
    Use this after sending OTP to customer.
    """
    return str(verify_otp(entered_otp, real_otp))

@tool
def tool_get_transactions(account_id: str) -> str:
    """
    Get last 10 transactions for customer account.
    Use this after customer is verified.
    """
    return str(get_transactions(account_id))

@tool
def tool_submit_fraud_claim(customer_id: str, account_id: str, transaction_ids: str) -> str:
    """
    Submit a fraud claim for disputed transactions.
    transaction_ids should be comma separated.
    """
    txn_list = [t.strip() for t in transaction_ids.split(",")]
    return str(submit_fraud_claim(customer_id, account_id, txn_list))


# ─────────────────────────────────────────
# STEP 2 — System Prompt
# ─────────────────────────────────────────
SYSTEM_PROMPT = """
You are a professional banking fraud detection agent.
Your job is to help customers report unauthorized transactions.

## Follow these steps in order:
1. Greet the customer professionally
2. Ask for their full name and card number
3. Use tool_verify_customer to verify their identity
4. If verified, thank them and ask for their phone number
5. Use tool_send_otp to send OTP to their phone
6. Ask customer to provide the OTP they received
7. Use tool_verify_otp to confirm the OTP
8. If OTP is correct, show their last 10 transactions using tool_get_transactions
9. Ask which transactions they did not authorize
10. Ask: what is the amount? what is the merchant name? did you authorize this payment?
11. Use tool_submit_fraud_claim to submit the claim
12. Tell customer their claim ID and that fraud team will contact them within 30 business days

## Important rules:
- Always be professional and polite
- Never skip verification steps
- Always confirm claim submission with claim ID
- If customer is not verified do not proceed
"""

# ─────────────────────────────────────────
# STEP 3 — Build the Agent
# ─────────────────────────────────────────
def build_agent():
    llm = AzureChatOpenAI(
        azure_endpoint   = os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key          = os.getenv("AZURE_OPENAI_API_KEY"),
        azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version      = os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature      = 0,
    )

    tools = [
        tool_verify_customer,
        tool_send_otp,
        tool_verify_otp,
        tool_get_transactions,
        tool_submit_fraud_claim,
    ]

    return llm.bind_tools(tools), tools


# ─────────────────────────────────────────
# STEP 4 — Chat with Agent in Terminal
# ─────────────────────────────────────────
def chat():
    llm_with_tools, tools = build_agent()
    tools_map = {t.name: t for t in tools}
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    print("\n" + "="*55)
    print("  🏦 Banking Fraud Detection Agent")
    print("  Type 'quit' to exit")
    print("="*55 + "\n")

    # Agent greets first
    messages.append({"role": "user", "content": "Hello"})
    response = llm_with_tools.invoke(messages)
    messages.append({"role": "assistant", "content": response.content})
    print(f"Agent: {response.content}\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("Agent: Thank you for calling. Goodbye!")
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        response = llm_with_tools.invoke(messages)

        # Handle tool calls
        while response.tool_calls:
            messages.append(response)
            for tool_call in response.tool_calls:
                tool_name   = tool_call["name"]
                tool_args   = tool_call["args"]
                tool_result = tools_map[tool_name].invoke(tool_args)
                messages.append({
                    "role":         "tool",
                    "tool_call_id": tool_call["id"],
                    "content":      str(tool_result)
                })
            response = llm_with_tools.invoke(messages)

        messages.append({"role": "assistant", "content": response.content})
        print(f"\nAgent: {response.content}\n")


if __name__ == "__main__":
    chat()