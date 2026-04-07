#!/usr/bin/env python3
"""
LevelForge+ SIMPLE - Guaranteed to work version
"""

import os
import json
import random
import requests
from datetime import datetime
from pathlib import Path

# ============ READ SECRETS ============
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USER = os.getenv("GITHUB_USERNAME", "favouradeleke246-maker")

print("=" * 50)
print("LevelForge+ Bot Starting...")
print(f"Telegram configured: {'YES' if TELEGRAM_TOKEN else 'NO'}")
print(f"GitHub configured: {'YES' if GITHUB_TOKEN else 'NO'}")
print("=" * 50)

# ============ 1. GENERATE GAME NAME ============
print("\n🎮 Generating game name...")

# Simple random name generator (no API needed)
prefixes = ["Neon", "Cyber", "Quantum", "Astral", "Void", "Echo", "Flux", "Rogue", "Solar", "Nova", "Dark", "Light", "Swift", "Brave", "Epic"]
suffixes = ["Runner", "Drifter", "Breach", "Vector", "Pulse", "Shift", "Core", "Edge", "Zone", "Drift", "Quest", "Rush", "Blade", "Fury", "Star"]

game_name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
print(f"✅ Game name: {game_name}")

# ============ 2. CREATE SIMPLE ART ============
print("\n🎨 Creating game art...")

# Create a simple colored image
from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGB', (512, 512), color=(random.randint(50,200), random.randint(50,200), random.randint(50,200)))
draw = ImageDraw.Draw(img)

# Draw a circle
center = 256
draw.ellipse([100, 100, 412, 412], outline=(255,255,255), width=5)
draw.rectangle([200, 200, 312, 312], fill=(255,255,255))

# Add text
try:
    draw.text((180, 420), game_name[:15], fill=(255,255,255))
except:
    pass

# Save image
sprite_path = Path("sprite.png")
img.save(sprite_path)
print(f"✅ Art saved: {sprite_path}")

# ============ 3. CREATE GITHUB REPO ============
print("\n📦 Creating GitHub repository...")

repo_name = f"daily-{game_name.lower().replace(' ', '-')}"
repo_url = f"https://github.com/{GITHUB_USER}/{repo_name}"

if GITHUB_TOKEN:
    try:
        # Create repo using GitHub API
        response = requests.post(
            "https://api.github.com/user/repos",
            headers={
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            },
            json={
                "name": repo_name,
                "description": f"Daily game: {game_name} - {datetime.now().strftime('%Y-%m-%d')}",
                "private": False,
                "auto_init": True
            },
            timeout=30
        )
        
        if response.status_code == 201:
            print(f"✅ Repo created: {repo_url}")
        else:
            print(f"⚠️ Repo creation: {response.status_code} - {response.text[:100]}")
    except Exception as e:
        print(f"⚠️ GitHub error: {e}")
else:
    print(f"⚠️ No GitHub token - would create: {repo_url}")

# ============ 4. SEND TELEGRAM MESSAGE ============
print("\n📱 Sending Telegram report...")

if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
    message = f"""
🌄 *LevelForge+ Daily Report*

📅 {datetime.now().strftime('%Y-%m-%d')}

🎮 *Game:* {game_name}

🔗 *Links:*
• Repo: {repo_url}
• Demo: (coming soon)

📊 *Status:* Bot is working!

✅ Next build in 24 hours
"""
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        response = requests.post(
            url,
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Telegram message sent!")
            print(f"   Check your Telegram app: {TELEGRAM_CHAT_ID}")
        else:
            print(f"❌ Telegram error: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Telegram exception: {e}")
else:
    print("⚠️ Missing Telegram credentials")
    print(f"   Token present: {bool(TELEGRAM_TOKEN)}")
    print(f"   Chat ID present: {bool(TELEGRAM_CHAT_ID)}")

# ============ 5. UPDATE PORTFOLIO ============
print("\n📁 Updating portfolio...")

portfolio = Path("portfolio.json")
entries = []
if portfolio.exists():
    entries = json.loads(portfolio.read_text())

entries.append({
    "date": datetime.now().isoformat(),
    "game": game_name,
    "repo": repo_url
})

portfolio.write_text(json.dumps(entries[-30:], indent=2))
print(f"✅ Portfolio has {len(entries)} games")

# ============ DONE ============
print("\n" + "=" * 50)
print("✅ Bot finished successfully!")
print("=" * 50)

# Save build info
with open("build_info.txt", "w") as f:
    f.write(f"Game: {game_name}\n")
    f.write(f"Time: {datetime.now()}\n")
    f.write(f"Repo: {repo_url}\n")
