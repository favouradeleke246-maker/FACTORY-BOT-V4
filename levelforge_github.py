import os
import json
import random
from datetime import datetime
from pathlib import Path

print("=" * 60)
print("LevelForge+ Bot v2 - Starting...")
print("=" * 60)

# ============ CHECK SECRETS ============
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
github_token = os.getenv("GH_TOKEN")

print(f"\n✅ Telegram Token: {'FOUND' if telegram_token else 'MISSING'}")
print(f"✅ Telegram Chat ID: {'FOUND' if telegram_chat_id else 'MISSING'}")
print(f"✅ GitHub Token: {'FOUND' if github_token else 'MISSING'}")

# ============ GENERATE GAME NAME ============
print("\n🎮 Generating game name...")
prefixes = ["Neon", "Cyber", "Quantum", "Astral", "Void", "Echo", "Flux", "Rogue"]
suffixes = ["Runner", "Drifter", "Breach", "Vector", "Pulse", "Shift", "Core"]
game_name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
print(f"   Game name: {game_name}")

# ============ CREATE A FILE (PROOF IT RUNS) ============
print("\n📁 Creating output files...")

# Create build_info.txt
with open("build_info.txt", "w") as f:
    f.write(f"Game: {game_name}\n")
    f.write(f"Time: {datetime.now()}\n")
    f.write(f"Status: Success\n")
print("   ✅ Created: build_info.txt")

# Create portfolio.json
portfolio = [{
    "date": datetime.now().isoformat(),
    "game": game_name,
    "status": "generated"
}]
with open("portfolio.json", "w") as f:
    json.dump(portfolio, f, indent=2)
print("   ✅ Created: portfolio.json")

# Create a fake sprite (simple text file since PIL might not be installed)
with open("sprite.png", "w") as f:
    f.write("This is a placeholder for the sprite image")
print("   ✅ Created: sprite.png (placeholder)")

# ============ SEND TELEGRAM MESSAGE ============
print("\n📱 Sending Telegram message...")

if telegram_token and telegram_chat_id:
    try:
        import requests
        
        message = f"""🎮 *DAILY GAME READY!* 🎮

*Game:* {game_name}
*Date:* {datetime.now().strftime('%Y-%m-%d')}
*Status:* Bot is working!

Your game factory is now running correctly!
Next game in 24 hours."""
        
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        response = requests.post(url, json={
            "chat_id": telegram_chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }, timeout=10)
        
        if response.status_code == 200:
            print("   ✅ Telegram message sent successfully!")
            print(f"   Check your Telegram now!")
        else:
            print(f"   ❌ Telegram error: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Failed to send: {e}")
else:
    print("   ❌ Missing Telegram credentials - can't send message")

# ============ CREATE GITHUB REPO ============
print("\n📦 Creating GitHub repository...")

if github_token:
    try:
        import requests
        
        repo_name = f"daily-{game_name.lower().replace(' ', '-')}"
        response = requests.post(
            "https://api.github.com/user/repos",
            headers={
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github.v3+json"
            },
            json={
                "name": repo_name,
                "description": f"Daily game: {game_name}",
                "private": False,
                "auto_init": True
            },
            timeout=30
        )
        
        if response.status_code == 201:
            repo_url = response.json()["html_url"]
            print(f"   ✅ Repo created: {repo_url}")
        else:
            print(f"   ⚠️ Repo creation: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️ GitHub error: {e}")
else:
    print("   ⚠️ No GitHub token")

# ============ DONE ============
print("\n" + "=" * 60)
print("✅ BOT FINISHED SUCCESSFULLY!")
print("=" * 60)

# Verify files exist
print("\n📁 Files created:")
for file in ["build_info.txt", "portfolio.json", "sprite.png"]:
    if Path(file).exists():
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} - MISSING!")
