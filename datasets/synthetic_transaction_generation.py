# This dataset is fully synthetic and generated for educational and portfolio purposes.
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# -------- CONFIG --------
NUM_TRANSACTIONS = 25000
NUM_ACCOUNTS = 3000
OUTPUT_PATH = os.path.expanduser("~/Desktop/payment_dataset")

os.makedirs(OUTPUT_PATH, exist_ok=True)

# -------- HELPERS --------
payment_types = ["ACH", "Wire", "Card"]
statuses = ["completed", "failed", "pending"]

def random_date():
    start = datetime(2026, 2, 1)
    end = datetime(2026, 2, 28, 23, 59, 59)
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

# -------- ACCOUNTS --------
accounts = pd.DataFrame({
    "account_id": [f"A{i}" for i in range(1, NUM_ACCOUNTS+1)],
    "user_id": [f"U{random.randint(1, NUM_ACCOUNTS)}" for _ in range(NUM_ACCOUNTS)],
    "balance": np.round(np.random.uniform(100, 50000, NUM_ACCOUNTS), 2)
})

accounts.to_csv(f"{OUTPUT_PATH}/accounts.csv", index=False)

# -------- TRANSACTIONS --------
transactions = []

for i in range(NUM_TRANSACTIONS):
    t_id = f"T{i+1}"
    user = f"U{random.randint(1, NUM_ACCOUNTS)}"
    acc = random.choice(accounts["account_id"].values)
    p_type = random.choice(payment_types)
    amount = round(np.random.exponential(500), 2)
    
    status = np.random.choice(statuses, p=[0.85, 0.1, 0.05])
    ts = random_date()
    
    transactions.append([t_id, user, acc, p_type, amount, status, ts])

transactions_df = pd.DataFrame(transactions, columns=[
    "transaction_id","user_id","account_id","payment_type","amount","status","timestamp"
])

transactions_df.to_csv(f"{OUTPUT_PATH}/transactions.csv", index=False)

# -------- PAYMENTS LOG --------
logs = []

for _, row in transactions_df.iterrows():
    t_id = row["transaction_id"]
    base_time = row["timestamp"]
    
    logs.append([t_id, "initiated", base_time])
    
    if row["status"] == "completed":
        logs.append([t_id, "processed", base_time + timedelta(minutes=5)])
    elif row["status"] == "failed":
        logs.append([t_id, "failed", base_time + timedelta(minutes=3)])
    else:
        logs.append([t_id, "pending", base_time + timedelta(minutes=10)])

payments_log = pd.DataFrame(logs, columns=["transaction_id","event_type","timestamp"])
payments_log.to_csv(f"{OUTPUT_PATH}/payments_log.csv", index=False)

# -------- RECONCILIATION --------
recon = []

for _, row in transactions_df.iterrows():
    expected = row["amount"]
    
    if row["status"] == "failed":
        actual = 0
    elif random.random() < 0.05:
        actual = round(expected * random.uniform(0.5, 1.5), 2)
    else:
        actual = expected
    
    flag = expected != actual
    
    recon.append([row["transaction_id"], expected, actual, flag])

reconciliation = pd.DataFrame(recon, columns=[
    "transaction_id","expected_amount","actual_amount","discrepancy_flag"
])

reconciliation.to_csv(f"{OUTPUT_PATH}/reconciliation.csv", index=False)

# -------- SUPPORT CASES --------
cases = []

issue_types = ["failed_payment", "duplicate", "refund", "pending_payment"]

case_id = 1

for _, row in transactions_df.iterrows():
    if row["status"] == "failed" or random.random() < 0.05:
        issue = random.choice(issue_types)
        resolution = random.randint(1, 72) if row["status"] != "pending" else 0
        status = "resolved" if resolution > 0 else "open"
        
        cases.append([
            f"C{case_id}",
            row["transaction_id"],
            issue,
            status,
            resolution
        ])
        case_id += 1

support_cases = pd.DataFrame(cases, columns=[
    "case_id","transaction_id","issue_type","status","resolution_time_hours"
])

support_cases.to_csv(f"{OUTPUT_PATH}/support_cases.csv", index=False)

print("✅ Dataset created on Desktop in folder: payment_dataset")
