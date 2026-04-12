#!/usr/bin/env python3
"""
Auto‑Delivery Bot – Monitors Solana wallet and sends game file on payment.
"""

import os
import json
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path

# ============ CONFIG ============
WALLET = os.getenv("SOLANA_WALLET")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
GAME_ZIP_PATH = os.getenv("GAME_ZIP_PATH", "workspace/latest_game.zip")

# File to store already‑processed transaction signatures
PROCESSED_FILE = Path("delivered_tx.json")
EXPECTED_AMOUNT_SOL = 5.0   # $5 SOL

# ============ HELIUS RPC (free) ============
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
    """Fetch last 10 transactions from Helius."""
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

def extract_payment(tx):
    """Check if transaction is an incoming SOL transfer of exactly $5."""
    # Helius transaction structure may vary – simplified example
    # You may need to adjust based on actual response.
    if "tokenTransfers" in tx:
        for transfer in tx["tokenTransfers"]:
            if (transfer.get("toUserAccount") == WALLET and
                transfer.get("amount") == EXPECTED_AMOUNT_SOL * 1e9):  # SOL has 9 decimals
                return transfer["fromUserAccount"], tx["signature"]
    return None, None

def send_game_file(telegram_user_id, tx_signature):
    """Send the game ZIP file to the buyer's Telegram chat."""
    zip_file = Path(GAME_ZIP_PATH)
    if not zip_file.exists():
        print(f"Game ZIP not found at {GAME_ZIP_PATH}")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    with open(zip_file, "rb") as f:
        files = {"document": f}
        data = {"chat_id": telegram_user_id, "caption": f"✅ Payment confirmed! Here is your game.\nTX: {tx_signature}"}
        response = requests.post(url, files=files, data=data, timeout=30)
    return response.status_code == 200

def main():
    processed = load_processed()
    transactions = get_recent_transactions()

    for tx in transactions[:10]:  # limit to recent 10
        sig = tx.get("signature")
        if sig in processed:
            continue

        sender, tx_sig = extract_payment(tx)
        if sender and tx_sig:
            # We have a valid payment. Now we need the buyer's Telegram handle.
            # Option A: Use transaction memo (if buyer included @username)
            # Option B: Ask buyer to message the bot first, then match by amount + time.
            # For simplicity, this example uses a memo.
            memo = tx.get("memo", "")
            if memo.startswith("@") and len(memo) > 1:
                buyer_username = memo
                # Convert username to chat_id (you need to know it or use sendMessage to username)
                # Actually you can send to username directly: "@username"
                success = send_game_file(buyer_username, tx_sig)
                if success:
                    processed.add(sig)
                    print(f"✅ Delivered game to {buyer_username} for tx {sig}")
                else:
                    print(f"❌ Failed to deliver to {buyer_username}")
            else:
                print(f"⚠️ Payment from {sender} but no Telegram memo. Skipping.")
        else:
            # Not a relevant transfer
            pass

    save_processed(processed)

if __name__ == "__main__":
    main()
