import os, json, hashlib
from datetime import datetime
from flask import Flask, request, jsonify
import requests

# ---------- CONFIG ----------
TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = os.getenv("TELEGRAM_CHAT_ID")
PRICE_SOL = os.getenv("GAME_PRICE", "7")
SOLANA_TRUST = "6wsQ6nGXrUUUGCEokb4rZcfHDv2a8MomUb22TuVaH2m3"
SOLANA_PHANTOM = "Csk9DKstWMdKx19gUHWB9xy2VwZZX2nx6V6oSVGDCgMb"
GITHUB_USER = "favouradeleke246-maker"
GITHUB_REPO = "FACTORY-BOT-V4"
RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main"
ZIP_URL = f"{RAW_URL}/workspace/latest_game.zip"

STATE_FILE = "delivery_state.json"
BUYERS_FILE = "buyers.json"

def load_state():
    default = {"total_deliveries": 0, "total_sales_sol": 0.0, "price_sol": PRICE_SOL}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return {**default, **json.load(f)}
    return default

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def load_buyers():
    if os.path.exists(BUYERS_FILE):
        with open(BUYERS_FILE) as f:
            return json.load(f)
    return []

def save_buyers(buyers):
    with open(BUYERS_FILE, "w") as f:
        json.dump(buyers, f, indent=2)

state = load_state()
buyers = load_buyers()

def send_message(chat_id, text):
    if not TG_TOKEN:
        return False
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}, timeout=10)
        return r.ok
    except:
        return False

def get_latest_game():
    try:
        r = requests.get(f"{RAW_URL}/portfolio.json", timeout=10)
        games = r.json()
        for g in reversed(games):
            if g.get("status") == "complete":
                return g
        return games[-1] if games else None
    except:
        return None

def deliver(username):
    username = username.lstrip("@")
    game = get_latest_game()
    if not game:
        return False, "No game available. Wait for next daily drop."
    key = "DR-" + hashlib.md5(f"{username}{game['game']}{SOLANA_TRUST}".encode()).hexdigest()[:16].upper()
    msg = (
        f"🎮 *Your game is ready, @{username}!*\n\n"
        f"✨ *{game['game']}* — {game['genre']}\n"
        f"⚡ {game['mechanic']}\n\n"
        f"🕹️ *Play:* {game['play_url']}\n"
        f"📦 *Source:* {ZIP_URL}\n"
        f"🔑 *License:* `{key}`\n\nThanks for supporting DeathRoll Studio!"
    )
    if not send_message(f"@{username}", msg):
        return False, f"Could not reach @{username}. They must /start first."
    buyers.append({
        "username": username,
        "game": game["game"],
        "key": key,
        "price_sol": state["price_sol"],
        "date": datetime.now().isoformat()
    })
    save_buyers(buyers)
    state["total_deliveries"] += 1
    state["total_sales_sol"] += float(state["price_sol"])
    save_state(state)
    return True, f"✅ Delivered {game['game']} to @{username}"

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    if not update or "message" not in update:
        return jsonify({"ok": True})
    msg = update["message"]
    chat_id = str(msg["chat"]["id"])
    text = msg.get("text", "").strip()
    if chat_id == ADMIN_ID:
        if text.startswith(("/paid", "/deliver")):
            parts = text.split()
            if len(parts) > 1:
                ok, reply = deliver(parts[1])
                send_message(ADMIN_ID, reply)
        elif text == "/status":
            game = get_latest_game()
            send_message(ADMIN_ID, f"Deliveries: {state['total_deliveries']}\nRevenue: {state['total_sales_sol']} SOL\nLatest: {game['game'] if game else 'None'}")
        elif text.startswith("/broadcast "):
            count = sum(1 for b in buyers if send_message(f"@{b['username']}", f"📢 Announcement\n{text[11:]}"))
            send_message(ADMIN_ID, f"Broadcast to {count} buyers.")
    else:
        if text == "/start":
            send_message(chat_id, f"Welcome! Latest game: https://{GITHUB_USER}.github.io/{GITHUB_REPO}\n/buy to purchase")
        elif text == "/buy":
            send_message(chat_id, f"Send {state['price_sol']} SOL to:\n`{SOLANA_TRUST}`\nor `{SOLANA_PHANTOM}`\nThen DM @deathroll1 with proof.")
        elif text == "/latest":
            game = get_latest_game()
            send_message(chat_id, f"{game['game'] if game else 'No game yet'}")
    return jsonify({"ok": True})

@app.route("/health")
def health():
    return jsonify({"status": "alive", "deliveries": state["total_deliveries"]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
