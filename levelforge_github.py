#!/usr/bin/env python3
"""
DEATHROLL STUDIO v27.0 - SIMPLIFIED & GUARANTEED
- Portfolio saves FIRST
- No complex AI mechanic generation that breaks
- All error handling
"""

import os
import json
import random
import requests
import time
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw

print("=" * 60)
print("🔥 DEATHROLL STUDIO v27.0 - SIMPLIFIED & GUARANTEED")
print("=" * 60)

BOT_VERSION = "27.0.0"
print(f"🤖 Bot Version: {BOT_VERSION}")

# ============ CONFIGURATION ============
BRAND_GITHUB = "favouradeleke246-maker"
SOLANA_TRUST_WALLET = "6wsQ6nGXrUUUGCEokb4rZcfHDv2a8MomUb22TuVaH2m3"
SOLANA_PHANTOM_WALLET = "Csk9DKstWMdKx19gUHWB9xy2VwZZX2nx6V6oSVGDCgMb"
TELEGRAM_CHANNEL = "@drolltech"

# Get secrets
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
openai_key = os.getenv("OPENAI_API_KEY")
github_token = os.getenv("GH_TOKEN")
game_price = os.getenv("GAME_PRICE", "7")

print(f"✅ Telegram: {'OK' if telegram_token else 'NO'}")
print(f"✅ OpenAI: {'OK' if openai_key else 'NO'}")
print(f"✅ GitHub: {'OK' if github_token else 'NO'}")

# ============ GAME DATA GENERATION (NO AI COMPLEXITY) ============
print("\n🎮 Generating game data...")

# Simple game name
prefixes = ["Neon", "Cyber", "Quantum", "Astral", "Void", "Echo", "Flux", "Rogue", "Crimson", "Shadow"]
suffixes = ["Runner", "Drifter", "Breach", "Vector", "Pulse", "Shift", "Core", "Edge", "Zone", "Fury"]
game_name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
print(f"   Game: {game_name}")

# Genre
genres = ["top-down shooter", "action RPG", "racing game", "puzzle game", "survival horror", "roguelite"]
selected_type = random.choice(genres)
print(f"   Genre: {selected_type}")

# Mechanic (simple list, no AI)
mechanics = [
    "Phase Echo", "Mirror Shell", "Gravity Well", "Soul Link", 
    "Void Step", "Chrono Fracture", "Static Charge", "Blood Pact"
]
mechanic_name = random.choice(mechanics)
mechanic_desc = f"Use {mechanic_name} to gain an advantage in combat"
print(f"   Mechanic: {mechanic_name}")

# Description
description = f"Master the {mechanic_name} in this intense {selected_type} experience!"
hashtags = f"#gamedev #indiegame #{selected_type.replace(' ', '')}"

# Hook
hooks = ["🔥 Run or die", "💀 Can you survive?", "⚔️ Your next obsession", "🏎️ Speed meets chaos"]
selected_hook = random.choice(hooks)

# Emojis for the game
emojis = ["🎮", "🔥", "⚡", "💀", "🔫", "⚔️"]
selected_emojis = " ".join(random.sample(emojis, 3))

print(f"   Description: {description}")
print(f"   Hook: {selected_hook}")

# ============ 🚨 IMMEDIATE PORTFOLIO SAVE (BEFORE ANYTHING ELSE) 🚨 ============
print("\n" + "=" * 60)
print("💾 STEP 1: SAVING TO PORTFOLIO.JSON")
print("=" * 60)

portfolio_path = Path("portfolio.json")

# Load existing portfolio
existing_games = []
if portfolio_path.exists():
    try:
        content = portfolio_path.read_text()
        if content.strip():
            existing_games = json.loads(content)
            if not isinstance(existing_games, list):
                existing_games = []
        print(f"   Loaded {len(existing_games)} existing games")
    except Exception as e:
        print(f"   Starting fresh: {e}")
        existing_games = []

# Create game entry
image_url = f"https://raw.githubusercontent.com/{BRAND_GITHUB}/FACTORY-BOT-V4/main/workspace/{game_name.replace(' ', '_')}/icon.png"

new_game = {
    "date": datetime.now().isoformat(),
    "game": game_name,
    "genre": selected_type,
    "mechanic": mechanic_name,
    "description": description,
    "hook": selected_hook,
    "hashtags": hashtags,
    "price_sol": game_price,
    "image_url": image_url,
    "status": "saved"
}

existing_games.append(new_game)
existing_games = existing_games[-200:]

# Save portfolio.json
try:
    portfolio_path.write_text(json.dumps(existing_games, indent=2))
    print(f"   ✅ Portfolio saved! Total games: {len(existing_games)}")
    print(f"   ✅ Added: {game_name}")
except Exception as e:
    print(f"   ❌ Portfolio save failed: {e}")
    Path("portfolio_emergency.json").write_text(json.dumps([new_game], indent=2))
    print(f"   ✅ Emergency backup saved")

# Also log to simple text file
games_log = Path("games_log.txt")
with open(games_log, "a") as f:
    f.write(f"{datetime.now().isoformat()} | {game_name} | {selected_type} | {mechanic_name}\n")
print(f"   ✅ Logged to games_log.txt")

# Create run timestamp
Path("last_run.txt").write_text(datetime.now().isoformat())
print(f"   ✅ last_run.txt created")

print("=" * 60)

# ============ ART GENERATION ============
print("\n🎨 STEP 2: Generating art...")
sprite_path = Path("sprite.png")
art_success = False

# Try online art
try:
    style = random.choice(["isometric", "neon cyberpunk", "low-poly", "cell-shaded"])
    prompt = f"3D {style} render of a {selected_type} character for '{game_name}', game asset"
    prompt_url = prompt.replace(" ", "+").replace("'", "")[:150]
    url = f"https://image.pollinations.ai/prompt/{prompt_url}?width=512&height=512"
    r = requests.get(url, timeout=30)
    if r.status_code == 200 and len(r.content) > 5000:
        sprite_path.write_bytes(r.content)
        art_success = True
        print(f"   ✅ Online art generated")
    else:
        raise Exception("Online art failed")
except Exception as e:
    print(f"   ⚠️ Online art failed: {e}")
    # Fallback art
    try:
        img = Image.new('RGB', (512, 512), color=(30, 30, 60))
        draw = ImageDraw.Draw(img)
        draw.rectangle([50, 50, 462, 462], outline=(255, 255, 255), width=3)
        draw.text((180, 230), game_name[:15], fill=(255, 255, 255))
        img.save(sprite_path)
        art_success = True
        print(f"   ✅ Fallback art created")
    except Exception as e2:
        print(f"   ❌ Art failed: {e2}")

# ============ WORKSPACE ============
print("\n📁 STEP 3: Setting up workspace...")
project_dir = Path(f"workspace/{game_name.replace(' ', '_')}")
project_dir.mkdir(parents=True, exist_ok=True)

if sprite_path.exists():
    shutil.copy(sprite_path, project_dir / "icon.png")
else:
    Image.new('RGB', (512, 512), color=(50, 50, 80)).save(project_dir / "icon.png")

# Create Godot files
(project_dir / "project.godot").write_text(f"""[application]
config/name="{game_name}"
config/icon="res://icon.png"
""")

(project_dir / "main.tscn").write_text("""[gd_scene format=3]
[node name="Main" type="Node2D"]""")

(project_dir / "player.gd").write_text(f"""extends Node2D
func _ready():
    print("{game_name} is ready!")""")

print(f"   ✅ Workspace created")

# ============ ZIP ============
print("\n📦 STEP 4: Creating ZIP...")
zip_path = Path("workspace/latest_game.zip")
try:
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in project_dir.rglob("*"):
            if file.is_file():
                try:
                    zipf.write(file, file.relative_to(project_dir.parent))
                except:
                    pass
    print(f"   ✅ ZIP created")
except Exception as e:
    print(f"   ⚠️ ZIP failed: {e}")

# ============ UPDATE PORTFOLIO WITH ART URL ============
print("\n📁 STEP 5: Updating portfolio with final details...")
try:
    current_games = json.loads(portfolio_path.read_text())
    for game in current_games:
        if game["game"] == game_name:
            game["art_success"] = art_success
            game["status"] = "complete"
            break
    portfolio_path.write_text(json.dumps(current_games, indent=2))
    print(f"   ✅ Portfolio updated")
except Exception as e:
    print(f"   ⚠️ Could not update: {e}")

# ============ GITHUB ============
print("\n📦 STEP 6: Creating GitHub repository...")
repo_name = f"daily-{game_name.lower().replace(' ', '-')}"
repo_link = f"https://github.com/{BRAND_GITHUB}/{repo_name}"

if github_token:
    try:
        r = requests.post(
            "https://api.github.com/user/repos",
            headers={"Authorization": f"token {github_token}"},
            json={"name": repo_name, "description": description[:100], "private": False},
            timeout=30
        )
        if r.status_code == 201:
            repo_link = r.json()["html_url"]
            print(f"   ✅ Repo created")
    except Exception as e:
        print(f"   ⚠️ Repo skip: {e}")

# ============ TELEGRAM ============
print("\n📱 STEP 7: Sending to Telegram...")

if telegram_token and telegram_chat_id:
    try:
        with open(zip_path, "rb") as f:
            caption = f"🎮 *{game_name}* – {selected_type}\n{description}\n💰 ${game_price} SOL"
            requests.post(
                f"https://api.telegram.org/bot{telegram_token}/sendDocument",
                files={"document": f},
                data={"chat_id": telegram_chat_id, "caption": caption, "parse_mode": "Markdown"},
                timeout=60
            )
        print(f"   ✅ Game sent to admin")
    except Exception as e:
        print(f"   ⚠️ Admin send failed: {e}")

if telegram_token:
    try:
        post = f"""
{selected_emojis} *{selected_hook}* {selected_emojis}

✨ *{game_name}* – {selected_type}
{description}

⚡ *Mechanic:* `{mechanic_name}`

💰 *Price:* ${game_price} SOL
🔵 Trust: `{SOLANA_TRUST_WALLET}`
🟣 Phantom: `{SOLANA_PHANTOM_WALLET}`

Send ${game_price} SOL + your @username → game in 5 mins

{hashtags}
#DeathRollStudio
"""
        with open(sprite_path, "rb") as photo:
            requests.post(
                f"https://api.telegram.org/bot{telegram_token}/sendPhoto",
                files={"photo": photo},
                data={"chat_id": TELEGRAM_CHANNEL, "caption": post, "parse_mode": "Markdown"},
                timeout=30
            )
        print(f"   ✅ Sales post sent")
    except Exception as e:
        print(f"   ⚠️ Sales post failed: {e}")

# ============ SAR SYSTEM (Simple) ============
print("\n🧠 STEP 8: Updating SAR system...")
sar_path = Path("sar_analysis.json")

sar_data = {"total_runs": 0, "games": []}
if sar_path.exists():
    try:
        sar_data = json.loads(sar_path.read_text())
    except:
        pass

sar_data["total_runs"] = sar_data.get("total_runs", 0) + 1
sar_data["last_game"] = game_name
sar_data["last_run"] = datetime.now().isoformat()
sar_data["games"].append({
    "name": game_name,
    "genre": selected_type,
    "mechanic": mechanic_name,
    "timestamp": datetime.now().isoformat()
})
sar_data["games"] = sar_data["games"][-100:]

sar_path.write_text(json.dumps(sar_data, indent=2))
print(f"   ✅ SAR updated (run #{sar_data['total_runs']})")

# ============ LEARNING DATA ============
print("\n📚 STEP 9: Updating learning data...")
learning_data = {
    "last_run": datetime.now().isoformat(),
    "last_game": game_name,
    "genre": selected_type,
    "mechanic": mechanic_name,
    "art_success": art_success,
    "total_games": len(existing_games)
}
Path("learning_data.json").write_text(json.dumps(learning_data, indent=2))
print(f"   ✅ Learning data saved")

# ============ BUILD INFO ============
Path("build_info.txt").write_text(f"""
DEATHROLL STUDIO v{BOT_VERSION}
Game: {game_name}
Genre: {selected_type}
Mechanic: {mechanic_name}
Date: {datetime.now().isoformat()}
Art success: {art_success}
Total games: {len(existing_games)}
""")
print(f"   ✅ Build info saved")

# ============ last_update.txt ============
Path("last_update.txt").write_text(f"Last update: {datetime.now().isoformat()}\nGame: {game_name}")
print(f"   ✅ last_update.txt created")

# ============ FINAL VERIFICATION ============
print("\n" + "=" * 60)
print("🔍 FINAL VERIFICATION")
print("=" * 60)

print(f"   Game: {game_name}")
print(f"   Genre: {selected_type}")
print(f"   Portfolio entries: {len(existing_games)}")
print(f"   SAR runs: {sar_data['total_runs']}")

# Verify portfolio.json
try:
    verify = portfolio_path.read_text()
    if game_name in verify:
        print(f"   ✅ VERIFIED: {game_name} is in portfolio.json")
    else:
        print(f"   ❌ ERROR: Game NOT in portfolio.json!")
        # Emergency: add it again
        current = json.loads(verify) if verify.strip() else []
        current.append(new_game)
        portfolio_path.write_text(json.dumps(current[-200:], indent=2))
        print(f"   🔄 Emergency re-save attempted")
except Exception as e:
    print(f"   ⚠️ Verification error: {e}")

print("\n" + "=" * 60)
print(f"✅ {game_name} is COMPLETE!")
print("=" * 60)

print("\n🎉 DEATHROLL STUDIO v27.0 FINISHED!")
print(f"📊 Website: https://{BRAND_GITHUB}.github.io/FACTORY-BOT-V4/")
