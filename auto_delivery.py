#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║       DEATHROLL STUDIO v30.0  —  AUTO-DELIVERY BOT          ║
║  24/7 Telegram bot that handles buyers automatically         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  HOW IT WORKS:                                               ║
║  1. Buyer sees game on Telegram channel                      ║
║  2. Buyer sends SOL to your wallet                           ║
║  3. YOU (admin) type:  /paid @username                       ║
║  4. Bot INSTANTLY sends buyer:                               ║
║       • Play link (browser, mobile-ready)                    ║
║       • Download link (Godot 4 source ZIP)                   ║
║       • License key                                          ║
║       • Thank you message                                    ║
║                                                              ║
║  ADMIN COMMANDS:                                             ║
║    /paid @username      — deliver latest game to buyer       ║
║    /deliver @username   — same as /paid                      ║
║    /status              — show stats & last game info        ║
║    /games               — list last 10 games                 ║
║    /price 9             — change price to 9 SOL              ║
║    /broadcast <msg>     — send message to all past buyers    ║
║    /sales               — show total sales count             ║
║                                                              ║
║  BUYER COMMANDS (anyone can use):                            ║
║    /start    — welcome message + latest game link            ║
║    /latest   — get the latest game                           ║
║    /catalog  — see all available games                       ║
║    /buy      — get payment instructions                      ║
║                                                              ║
║  SETUP:                                                      ║
║    1. pip install requests                                   ║
║    2. Set env vars (or edit CONFIG below)                    ║
║    3. python auto_delivery.py                                ║
║    4. Keep running 24/7 (use screen / pm2 / Railway.app)     ║
║                                                              ║
║  FREE HOSTING OPTIONS:                                       ║
║    • Railway.app (free tier, always on)                      ║
║    • Render.com  (free tier)                                 ║
║    • Your own VPS                                            ║
║    • GitHub Actions (run on schedule — see note below)       ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import json
import time
import requests
import hashlib
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════════════════
#  CONFIG  — set via environment variables or edit directly
# ═══════════════════════════════════════════════════════════
TG_TOKEN    = os.getenv("TELEGRAM_BOT_TOKEN",  "")
ADMIN_ID    = os.getenv("TELEGRAM_CHAT_ID",    "")   # your personal chat ID
CHANNEL     = os.getenv("TELEGRAM_CHANNEL",    "@drolltech")
GITHUB_USER = os.getenv("GITHUB_USER",         "favouradeleke246-maker")
GITHUB_REPO = os.getenv("GITHUB_REPO",         "FACTORY-BOT-V4")
PRICE_SOL   = os.getenv("GAME_PRICE",          "7")

SOLANA_TRUST   = "6wsQ6nGXrUUUGCEokb4rZcfHDv2a8MomUb22TuVaH2m3"
SOLANA_PHANTOM = "Csk9DKstWMdKx19gUHWB9xy2VwZZX2nx6V6oSVGDCgMb"
BRAND_NAME     = "DeathRoll Studio"
WEBSITE        = "https://deathroll.co"

BASE_URL  = f"https://{GITHUB_USER}.github.io/{GITHUB_REPO}"
RAW_URL   = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main"
STORE_URL = BASE_URL
ZIP_URL   = f"{RAW_URL}/workspace/latest_game.zip"

TG_API    = f"https://api.telegram.org/bot{TG_TOKEN}"

# ═══════════════════════════════════════════════════════════
#  LOCAL STATE  (persists across restarts)
# ═══════════════════════════════════════════════════════════
STATE_FILE   = Path("delivery_state.json")
BUYERS_FILE  = Path("buyers.json")

def load_state() -> dict:
    defaults = {
        "last_update_id": 0,
        "total_deliveries": 0,
        "total_sales_sol": 0.0,
        "price_sol": PRICE_SOL,
        "started": datetime.now().isoformat(),
    }
    if STATE_FILE.exists():
        try:
            d = json.loads(STATE_FILE.read_text())
            defaults.update(d)
        except: pass
    return defaults

def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2))

def load_buyers() -> list:
    if BUYERS_FILE.exists():
        try: return json.loads(BUYERS_FILE.read_text())
        except: pass
    return []

def save_buyers(buyers: list):
    BUYERS_FILE.write_text(json.dumps(buyers, indent=2))

def load_portfolio() -> list:
    """Load portfolio from local file or GitHub."""
    # Try local first (if running in same repo)
    local = Path("portfolio.json")
    if local.exists():
        try:
            data = json.loads(local.read_text())
            if isinstance(data, list) and data:
                return data
        except: pass
    # Fallback: fetch from GitHub
    try:
        r = requests.get(f"{RAW_URL}/portfolio.json", timeout=15)
        if r.status_code == 200:
            return r.json()
    except: pass
    return []

# ═══════════════════════════════════════════════════════════
#  TELEGRAM HELPERS
# ═══════════════════════════════════════════════════════════
def tg_get(method: str, params: dict = {}) -> dict:
    try:
        r = requests.get(f"{TG_API}/{method}", params=params, timeout=15)
        return r.json() if r.status_code == 200 else {}
    except: return {}

def tg_post(method: str, data: dict = {}) -> dict:
    try:
        r = requests.post(f"{TG_API}/{method}", data=data, timeout=15)
        return r.json() if r.status_code == 200 else {}
    except: return {}

def send_msg(chat_id, text: str, parse_mode: str = "Markdown",
             reply_markup: dict = None) -> bool:
    data = {
        "chat_id":    str(chat_id),
        "text":       text,
        "parse_mode": parse_mode,
    }
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    return bool(tg_post("sendMessage", data).get("ok"))

def send_photo(chat_id, photo_url: str, caption: str) -> bool:
    return bool(tg_post("sendPhoto", {
        "chat_id":    str(chat_id),
        "photo":      photo_url,
        "caption":    caption,
        "parse_mode": "Markdown",
    }).get("ok"))

def get_updates(offset: int = 0) -> list:
    data = tg_get("getUpdates", {
        "offset":  offset,
        "timeout": 30,
        "limit":   50,
        "allowed_updates": json.dumps(["message","callback_query"]),
    })
    return data.get("result", [])

# ═══════════════════════════════════════════════════════════
#  GAME DATA HELPERS
# ═══════════════════════════════════════════════════════════
def get_latest_game(portfolio: list) -> dict | None:
    complete = [g for g in portfolio if g.get("status") == "complete"]
    return complete[-1] if complete else (portfolio[-1] if portfolio else None)

def get_game_by_name(portfolio: list, name: str) -> dict | None:
    name_lower = name.lower()
    for g in reversed(portfolio):
        if name_lower in g.get("game", "").lower():
            return g
    return None

def format_game_card(game: dict, price: str) -> str:
    name   = game.get("game", "Unknown")
    genre  = game.get("genre", "?")
    mech   = game.get("mechanic", "?")
    mdesc  = game.get("mech_desc", game.get("mechanic_description",""))
    desc   = game.get("description", "")
    play   = game.get("play_url", STORE_URL)
    date   = game.get("date", "")[:10]
    color_emojis = {
        "top-down shooter": "🔫", "action RPG": "⚔️",
        "racing game": "🏎️", "puzzle game": "🧩",
        "survival horror": "👻", "fighting game": "👊",
        "strategy game": "♟️", "roguelite": "🎲",
        "platformer": "🦘", "stealth game": "🕵️",
        "extraction shooter": "💰", "cozy builder": "🏡",
        "tower defense": "🏰", "metroidvania": "🗺️",
    }
    emoji = color_emojis.get(genre, "🎮")
    return (
        f"{emoji} *{name}*\n"
        f"_{genre.title()}_\n\n"
        f"{desc}\n\n"
        f"⚡ *Mechanic:* {mech}\n"
        f"_{mdesc[:80]}_\n\n"
        f"🕹️ [Play Free Now]({play})\n"
        f"💰 Full source: *{price} SOL*\n"
        f"📅 {date}"
    )

# ═══════════════════════════════════════════════════════════
#  DELIVERY SYSTEM
# ═══════════════════════════════════════════════════════════
def generate_license_key(username: str, game_name: str) -> str:
    seed = f"{username}{game_name}{SOLANA_TRUST}"
    return "DR-" + hashlib.md5(seed.encode()).hexdigest()[:16].upper()

def deliver_game(username: str, game: dict, state: dict,
                 buyers: list, price: str) -> bool:
    """Send full game package to buyer."""
    username = username.lstrip("@")
    name     = game.get("game", "Latest Game")
    genre    = game.get("genre", "")
    mech     = game.get("mechanic", "")
    play_url = game.get("play_url", STORE_URL)
    key      = generate_license_key(username, name)

    delivery_msg = (
        f"🎮 *Your game is ready, @{username}!*\n\n"
        f"✨ *{name}*\n"
        f"_{genre.title()}_\n\n"
        f"⚡ *Mechanic:* {mech}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🕹️ *Play in browser (mobile-ready):*\n"
        f"{play_url}\n\n"
        f"📦 *Download Godot 4 source:*\n"
        f"{ZIP_URL}\n\n"
        f"🌐 *Full store:*\n"
        f"{STORE_URL}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🔑 *Your license key:*\n"
        f"`{key}`\n\n"
        f"📌 *Keep this key safe* — it proves your purchase.\n\n"
        f"Thanks for supporting DeathRoll Studio! 🔥\n"
        f"New game drops every day → {CHANNEL}\n\n"
        f"_Questions? DM @deathroll1_"
    )

    # Try sending to @username
    ok = send_msg(f"@{username}", delivery_msg)

    if ok:
        # Record buyer
        buyer_record = {
            "username":  username,
            "game":      name,
            "genre":     genre,
            "key":       key,
            "price_sol": price,
            "date":      datetime.now().isoformat(),
        }
        buyers.append(buyer_record)
        save_buyers(buyers)

        # Update portfolio sales count
        port_path = Path("portfolio.json")
        if port_path.exists():
            try:
                entries = json.loads(port_path.read_text())
                for e in entries:
                    if e.get("game") == name:
                        e["sales"] = e.get("sales", 0) + 1
                        break
                port_path.write_text(json.dumps(entries, indent=2))
            except: pass

        # Update state
        state["total_deliveries"] += 1
        state["total_sales_sol"]  = round(
            state.get("total_sales_sol", 0) + float(price), 2)
        save_state(state)

        log(f"✅ Delivered '{name}' to @{username} | Key: {key}")
        return True
    else:
        log(f"⚠️  Could not reach @{username} — they may need to /start the bot first")
        return False

# ═══════════════════════════════════════════════════════════
#  COMMAND HANDLERS
# ═══════════════════════════════════════════════════════════
def handle_admin_command(text: str, chat_id: str, state: dict,
                         buyers: list, portfolio: list) -> str | None:
    """Handle admin-only commands. Returns response string or None."""
    parts  = text.strip().split()
    cmd    = parts[0].lower() if parts else ""
    args   = parts[1:] if len(parts) > 1 else []
    price  = state.get("price_sol", PRICE_SOL)

    # ── /paid @username  OR  /deliver @username ────────────
    if cmd in ("/paid", "/deliver") and args:
        username = args[0].lstrip("@")
        game     = get_latest_game(portfolio)
        if not game:
            return "❌ No games in portfolio yet. Run the factory first."
        ok = deliver_game(username, game, state, buyers, price)
        if ok:
            return (
                f"✅ *Delivered to @{username}*\n\n"
                f"Game: *{game.get('game')}*\n"
                f"Price: *{price} SOL*\n"
                f"Total deliveries: *{state['total_deliveries']}*\n"
                f"Total SOL earned: *{state['total_sales_sol']} SOL*"
            )
        else:
            return (
                f"⚠️ *Could not reach @{username}*\n\n"
                f"They need to start the bot first:\n"
                f"Ask them to send `/start` to your bot.\n\n"
                f"Once they do, try `/paid @{username}` again."
            )

    # ── /status ────────────────────────────────────────────
    elif cmd == "/status":
        game = get_latest_game(portfolio)
        game_name = game.get("game", "None") if game else "None"
        game_genre = game.get("genre", "") if game else ""
        return (
            f"📊 *DeathRoll Studio Status*\n\n"
            f"🎮 Latest game: *{game_name}*\n"
            f"🏷️ Genre: _{game_genre}_\n"
            f"💰 Price: *{price} SOL*\n"
            f"📦 Games built: *{len(portfolio)}*\n"
            f"🛒 Total deliveries: *{state['total_deliveries']}*\n"
            f"💎 Total SOL earned: *{state['total_sales_sol']} SOL*\n"
            f"👥 Buyers: *{len(buyers)}*\n"
            f"🤖 Bot uptime since: _{state.get('started','?')[:16]}_\n\n"
            f"🌐 Store: {STORE_URL}"
        )

    # ── /games ─────────────────────────────────────────────
    elif cmd == "/games":
        if not portfolio:
            return "❌ No games yet."
        recent = list(reversed(portfolio[-10:]))
        lines  = ["📋 *Last 10 Games:*\n"]
        for i, g in enumerate(recent, 1):
            date  = g.get("date","")[:10]
            name  = g.get("game","?")
            genre = g.get("genre","?")
            play  = g.get("play_url","")
            lines.append(f"{i}. [{name}]({play}) — _{genre}_ ({date})")
        return "\n".join(lines)

    # ── /price <amount> ────────────────────────────────────
    elif cmd == "/price" and args:
        try:
            new_price = str(float(args[0]))
            state["price_sol"] = new_price
            save_state(state)
            return f"✅ Price updated to *{new_price} SOL*"
        except:
            return "❌ Invalid price. Example: `/price 9`"

    # ── /sales ─────────────────────────────────────────────
    elif cmd == "/sales":
        if not buyers:
            return "📊 No sales yet."
        lines = [f"💎 *Sales Report* — {len(buyers)} total\n"]
        for b in reversed(buyers[-15:]):
            lines.append(
                f"@{b.get('username','?')} → {b.get('game','?')} "
                f"({b.get('price_sol','?')} SOL) — {b.get('date','')[:10]}"
            )
        lines.append(f"\n💰 Total: *{state.get('total_sales_sol',0)} SOL*")
        return "\n".join(lines)

    # ── /broadcast <message> ──────────────────────────────
    elif cmd == "/broadcast" and args:
        msg_text  = " ".join(args)
        count     = 0
        failed    = 0
        for buyer in buyers:
            uname = buyer.get("username","")
            if not uname: continue
            ok = send_msg(f"@{uname}",
                f"📢 *DeathRoll Studio Update*\n\n{msg_text}\n\n"
                f"— {BRAND_NAME}")
            if ok: count += 1
            else:  failed += 1
            time.sleep(0.1)   # rate limit friendly
        return (
            f"✅ Broadcast sent\n"
            f"Delivered: *{count}*\n"
            f"Failed: *{failed}*"
        )

    # ── /help ─────────────────────────────────────────────
    elif cmd in ("/help", "/start") and str(chat_id) == str(ADMIN_ID):
        return (
            f"🤖 *DeathRoll Studio Bot — Admin Commands*\n\n"
            f"`/paid @username`    — deliver latest game\n"
            f"`/deliver @username` — same as /paid\n"
            f"`/status`            — bot stats\n"
            f"`/games`             — last 10 games\n"
            f"`/sales`             — sales report\n"
            f"`/price 9`           — change price\n"
            f"`/broadcast <msg>`   — message all buyers\n"
        )

    return None

def handle_public_command(text: str, chat_id: str,
                          portfolio: list, state: dict) -> bool:
    """Handle public commands anyone can use. Returns True if handled."""
    parts = text.strip().split()
    cmd   = parts[0].lower().split("@")[0] if parts else ""
    price = state.get("price_sol", PRICE_SOL)

    # ── /start ─────────────────────────────────────────────
    if cmd == "/start":
        game = get_latest_game(portfolio)
        play = game.get("play_url", STORE_URL) if game else STORE_URL
        name = game.get("game", "our latest game") if game else "our latest game"
        send_msg(chat_id,
            f"🎮 *Welcome to DeathRoll Studio!*\n\n"
            f"We drop a brand new mobile game *every single day*.\n"
            f"All games are *free to play* in your browser.\n"
            f"Buy the full Godot 4 source for just *{price} SOL*.\n\n"
            f"🕹️ *Latest game:* [{name}]({play})\n\n"
            f"Use /latest for today's game\n"
            f"Use /catalog to browse all games\n"
            f"Use /buy to purchase source code\n\n"
            f"📺 Follow us: {CHANNEL}"
        )
        return True

    # ── /latest ────────────────────────────────────────────
    elif cmd == "/latest":
        game = get_latest_game(portfolio)
        if not game:
            send_msg(chat_id, "🎮 No games yet — check back soon!")
            return True
        card = format_game_card(game, price)
        img  = game.get("image_url","")
        if img:
            ok = send_photo(chat_id, img, card)
            if not ok: send_msg(chat_id, card)
        else:
            send_msg(chat_id, card)
        return True

    # ── /catalog ───────────────────────────────────────────
    elif cmd == "/catalog":
        if not portfolio:
            send_msg(chat_id, "📋 No games yet!")
            return True
        recent = list(reversed(portfolio[-12:]))
        lines  = [f"📋 *DeathRoll Studio — Game Catalog*\n_{len(portfolio)} games total_\n"]
        for g in recent:
            name  = g.get("game","?")
            genre = g.get("genre","?")
            play  = g.get("play_url", STORE_URL)
            lines.append(f"▸ [{name}]({play}) — _{genre}_")
        lines.append(f"\n🌐 Full store: {STORE_URL}")
        send_msg(chat_id, "\n".join(lines))
        return True

    # ── /buy ───────────────────────────────────────────────
    elif cmd == "/buy":
        game = get_latest_game(portfolio)
        name = game.get("game","latest game") if game else "latest game"
        send_msg(chat_id,
            f"💰 *How to Buy — DeathRoll Studio*\n\n"
            f"*Step 1:* Play the game free first\n"
            f"_Make sure you love it before buying!_\n\n"
            f"*Step 2:* Send *{price} SOL* to either wallet:\n\n"
            f"🔵 *Trust Wallet (Solana):*\n"
            f"`{SOLANA_TRUST}`\n\n"
            f"🟣 *Phantom Wallet (Solana):*\n"
            f"`{SOLANA_PHANTOM}`\n\n"
            f"*Step 3:* Send proof + your @username to:\n"
            f"👉 @deathroll1\n\n"
            f"*What you receive:*\n"
            f"✅ Full Godot 4 source code\n"
            f"✅ HTML5 build (deploy anywhere)\n"
            f"✅ License key\n"
            f"✅ Instant delivery\n\n"
            f"Current game: *{name}*\n"
            f"Price: *{price} SOL*"
        )
        return True

    return False

# ═══════════════════════════════════════════════════════════
#  LOGGING
# ═══════════════════════════════════════════════════════════
def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line      = f"[{timestamp}] {msg}"
    print(line)
    with open("delivery_log.txt", "a") as f:
        f.write(line + "\n")

# ═══════════════════════════════════════════════════════════
#  MAIN POLLING LOOP
# ═══════════════════════════════════════════════════════════
def main():
    if not TG_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not set. Add it as environment variable.")
        return
    if not ADMIN_ID:
        print("⚠️  TELEGRAM_CHAT_ID not set — admin commands won't be restricted.")

    state   = load_state()
    buyers  = load_buyers()

    log(f"🤖 DeathRoll Studio Delivery Bot starting...")
    log(f"   Admin ID    : {ADMIN_ID or 'NOT SET'}")
    log(f"   Channel     : {CHANNEL}")
    log(f"   Price       : {state.get('price_sol', PRICE_SOL)} SOL")
    log(f"   Deliveries  : {state['total_deliveries']}")
    log(f"   Buyers      : {len(buyers)}")

    # Announce startup to admin
    if ADMIN_ID:
        send_msg(ADMIN_ID,
            f"🤖 *DeathRoll Bot Online*\n\n"
            f"Deliveries: *{state['total_deliveries']}*\n"
            f"Buyers: *{len(buyers)}*\n"
            f"SOL earned: *{state.get('total_sales_sol',0)}*\n\n"
            f"Send `/help` for commands."
        )

    offset       = state.get("last_update_id", 0) + 1
    portfolio    = load_portfolio()
    port_refresh = 0   # refresh portfolio every 10 minutes

    log("✅ Bot running — polling for messages...")

    while True:
        try:
            # Refresh portfolio periodically
            port_refresh += 1
            if port_refresh >= 20:   # every ~10 min at 30s poll
                portfolio    = load_portfolio()
                port_refresh = 0

            updates = get_updates(offset)

            for update in updates:
                uid    = update.get("update_id", 0)
                offset = uid + 1
                state["last_update_id"] = uid
                save_state(state)

                # ── Handle regular messages ─────────────────
                msg     = update.get("message", {})
                text    = msg.get("text", "").strip()
                chat_id = str(msg.get("chat", {}).get("id", ""))
                user    = msg.get("from", {})
                uname   = user.get("username", "")
                fname   = user.get("first_name", "")

                if not text or not chat_id:
                    continue

                is_admin = (chat_id == str(ADMIN_ID))

                log(f"📨 [{fname or uname or chat_id}]: {text[:60]}")

                # ── Admin commands ──────────────────────────
                if is_admin:
                    response = handle_admin_command(
                        text, chat_id, state, buyers, portfolio)
                    if response:
                        send_msg(chat_id, response)
                        continue

                # ── Public commands (anyone) ─────────────────
                handled = handle_public_command(
                    text, chat_id, portfolio, state)
                if handled:
                    continue

                # ── Unknown command fallback ─────────────────
                if text.startswith("/"):
                    if is_admin:
                        send_msg(chat_id,
                            "❓ Unknown command. Send `/help` for the list.")
                    else:
                        send_msg(chat_id,
                            "👋 Try:\n/start — welcome\n/latest — today's game\n"
                            "/catalog — all games\n/buy — purchase info")

            # Small sleep to avoid hammering Telegram
            time.sleep(1)

        except KeyboardInterrupt:
            log("🛑 Bot stopped by user.")
            break
        except requests.exceptions.ConnectionError:
            log("⚠️  Connection lost — retrying in 10s...")
            time.sleep(10)
        except requests.exceptions.Timeout:
            log("⚠️  Timeout — retrying...")
            time.sleep(3)
        except Exception as e:
            log(f"❌ Unexpected error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
