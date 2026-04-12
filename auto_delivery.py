#!/usr/bin/env python3
"""
Auto‑Delivery Bot – Monitors Solana wallet, reads memo, sends game file.
"""

import os
import json
import time
import requests
from pathlib import Path

# ============ CONFIG ============
WALLET = os.getenv("SOLANA_WALLET")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
GAME_ZIP_PATH = os.getenv("GAME_ZIP_PATH", "workspace/latest_game.zip")

PROCESSED_FILE = Path("delivered_tx.json")
EXPECTED_AMOUNT_SOL = 5.0

HELIUS_URL = f"https://api.helius.xyz/v0/addresses/{WALLET}/transactions?apiKey={HELIUS_API_KEY}"

def load_processed():
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_processed(processed_set):
    with open(PROCESSED_FILE, "w") as f:
        json.dump(list(processed_set), f)

def get_recent_transactions():
    try:
        response = requests.get(HELIUS_URL, timeout=15)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Helius error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return []

def extract_payment_and_memo(tx):
    # Check for SOL transfer to our wallet
    if "tokenTransfers" in tx:
        for transfer in tx["tokenTransfers"]:
            if (transfer.get("toUserAccount") == WALLET and
                transfer.get("amount") == EXPECTED_AMOUNT_SOL * 1e9):
                memo = tx.get("memo", "")
                if memo.startswith("@"):
                    return memo, tx["signature"]
    return None, None

def send_game_file(telegram_username, tx_signature):
    zip_file = Path(GAME_ZIP_PATH)
    if not zip_file.exists():
        print(f"Game ZIP not found at {GAME_ZIP_PATH}")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    with open(zip_file, "rb") as f:
        files = {"document": f}
        data = {"chat_id": telegram_username, "caption": f"✅ Payment confirmed! Here is your game.\nTX: {tx_signature}"}
        response = requests.post(url, files=files, data=data, timeout=30)
    return response.status_code == 200

def main():
    processed = load_processed()
    transactions = get_recent_transactions()

    for tx in transactions[:10]:
        sig = tx.get("signature")
        if sig in processed:
            continue

        username, tx_sig = extract_payment_and_memo(tx)
        if username and tx_sig:
            success = send_game_file(username, tx_sig)
            if success:
                processed.add(sig)
                print(f"✅ Delivered game to {username} for tx {sig}")
            else:
                print(f"❌ Failed to deliver to {username}")
        else:
            # No relevant payment or no memo
            pass

    save_processed(processed)

if __name__ == "__main__":
    main()
