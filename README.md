# 🏦 Agentic AI Fraud Detection System

An AI-powered banking fraud detection agent built with **Azure OpenAI (GPT-4o)**, **LangChain**, and **Azure PostgreSQL**. The agent handles real customer fraud claims through a conversational terminal interface.

---

## 🎯 Project Overview

This project simulates a real banking fraud detection workflow where an AI agent:
1. Verifies customer identity using name and card number
2. Sends OTP verification code to customer phone
3. Retrieves customer's recent transactions from database
4. Accepts customer's report of unauthorized transactions
5. Submits a fraud claim to Azure PostgreSQL database
6. Confirms claim ID and informs customer of 30 business day resolution

---

## 🏗️ Architecture
Customer (Terminal)
↓
LangChain Agent (GPT-4o)
↓
Agent Tools (Python)
↓
Azure PostgreSQL Database
---

## 🗄️ Database Schema

5 tables designed to simulate a real banking database:

| Table | Purpose |
|---|---|
| `customers` | Customer profiles (name, phone, email) |
| `accounts` | Bank accounts and card details |
| `transactions` | 2,500+ real banking transactions from Kaggle |
| `fraud_claims` | Submitted fraud claims |
| `claim_status` | Claim investigation status |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| AI Model | Azure OpenAI GPT-4o |
| Agent Framework | LangChain |
| Database | Azure PostgreSQL |
| Dataset | Kaggle Banking Fraud Dataset (2,512 transactions) |
| Language | Python 3.14 |
| Cloud | Microsoft Azure |
| Version Control | GitHub |

---

## 📁 Project Structure
```
fraud-ai-agent/
├── agents/
│   └── fraud_agent.py       ← AI agent brain
├── tools/
│   └── fraud_tools.py       ← Agent tools (verify, OTP, claim)
├── db/
│   ├── schema.sql           ← Database table definitions
│   ├── database.py          ← Database connection
│   └── run_schema.py        ← Creates tables in Azure
├── scripts/
│   ├── load_data.py         ← Loads Kaggle CSV into Azure
│   └── generate_customers.py← Generates fake customer data
├── data/
│   └── raw/                 ← Kaggle dataset (git-ignored)
├── .env.template            ← Environment variables template
├── requirements.txt         ← Python dependencies
└── README.md

```
---

## 🚀 Setup Guide

### 1 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/fraud-ai-agent.git
cd fraud-ai-agent
```

### 2 — Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3 — Install dependencies
```bash
pip3 install -r requirements.txt
```

### 4 — Configure environment variables
```bash
cp .env.template .env
# Fill in your Azure credentials
```

### 5 — Initialize database
```bash
python3 db/run_schema.py
```

### 6 — Load dataset
```bash
python3 scripts/load_data.py
```

### 7 — Generate test customers
```bash
python3 scripts/generate_customers.py
```

### 8 — Run the agent
```bash
python3 agents/fraud_agent.py
```

---

## 💬 Example Conversation
