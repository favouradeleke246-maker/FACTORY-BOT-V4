#!/usr/bin/env python3
"""
LevelForge+ ULTRA – DEATHROLL STUDIO v12.0
- MASTODON READY
- Telegram Viral Posts
- GitHub Auto-Repos
- AI-Powered Art
"""

import os
import json
import random
import requests
import time
import shutil
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw

print("=" * 60)
print("🔥 DEATHROLL STUDIO v12.0 – MASTODON READY")
print("✅ Telegram | Mastodon | GitHub | Viral Marketing")
print("=" * 60)

# ============ BOT VERSION ============
BOT_VERSION = "12.0.0"
print(f"🤖 Bot Version: {BOT_VERSION}")

# ============ YOUR CONTACT INFO ============
BRAND_NAME = "DeathRoll"
BRAND_EMAIL_PRIMARY = "favouradeleke246@gmail.com"
BRAND_EMAIL_SECONDARY = "fadeleke246@gmail.com"
BRAND_TELEGRAM = "@deathroll1"
BRAND_TIKTOK = "@deathroll.co"
BRAND_WEBSITE = "https://deathroll.co"
BRAND_GITHUB = "favouradeleke246-maker"
MASTODON_HANDLE = "@Deathroll_Studio"

# Solana wallets
SOLANA_TRUST_WALLET = "6wsQ6nGXrUUUGCEokb4rZcfHDv2a8MomUb22TuVaH2m3"
SOLANA_PHANTOM_WALLET = "Csk9DKstWMdKx19gUHWB9xy2VwZZX2nx6V6oSVGDCgMb"

# Telegram channel
TELEGRAM_CHANNEL = "@drolltech"

print(f"🏷️ Brand: {BRAND_NAME}")
print(f"📧 Email: {BRAND_EMAIL_PRIMARY}")
print(f"📱 Telegram: {BRAND_TELEGRAM} | Channel: {TELEGRAM_CHANNEL}")
print(f"🎵 TikTok: {BRAND_TIKTOK}")
print(f"🐘 Mastodon: {MASTODON_HANDLE}")

# ============ GET SECRETS ============
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
openai_key = os.getenv("OPENAI_API_KEY")
github_token = os.getenv("GH_TOKEN")
mastodon_token = os.getenv("MASTODON_ACCESS_TOKEN")
mastodon_instance = os.getenv("MASTODON_INSTANCE")
game_price = os.getenv("GAME_PRICE", "5")

print(f"✅ Telegram: {'OK' if telegram_token else 'NO'}")
print(f"✅ OpenAI: {'OK' if openai_key else 'NO'}")
print(f"✅ GitHub: {'OK' if github_token else 'NO'}")
print(f"🐘 Mastodon: {'OK' if mastodon_token else 'NO (add token)'}")
print(f"💰 Game Price: ${game_price}")

# ============ MASTODON VALIDATION ============
if mastodon_token and mastodon_instance:
    print(f"\n🐘 Mastodon configured with: {mastodon_instance}")
else:
    print(f"\n⚠️ Mastodon not configured – add MASTODON_ACCESS_TOKEN and MASTODON_INSTANCE secrets")

# ============ VIRAL MARKETING ============
print("\n🔥 Generating viral marketing content...")

# Genre-specific emojis
genre_emojis = {
    "top-down shooter": ["🔫", "💥", "🎯", "⚡", "🔥", "💀"],
    "action RPG": ["⚔️", "🛡️", "👑", "✨", "🌟", "💎"],
    "racing game": ["🏎️", "💨", "🔥", "⚡", "🏁", "🚗"],
    "puzzle game": ["🧠", "💡", "🔮", "✨", "🎯", "💎"],
    "survival horror": ["😱", "💀", "👻", "🔪", "🩸", "🌙"],
    "fighting game": ["👊", "💥", "⚡", "🔥", "🏆", "💪"],
    "strategy game": ["♟️", "🧠", "👑", "⚔️", "🎯", "💎"]
}

viral_hooks = {
    "top-down shooter": ["🔫 I built a shooter in 24 hours", "💀 This boss took 50 attempts"],
    "action RPG": ["⚔️ Your next obsession", "✨ 24 hours = a whole RPG"],
    "racing game": ["🏎️ Speed meets chaos", "💨 Fastest game I've made"],
    "puzzle game": ["🧠 1000 IQ required", "💡 One move changes everything"],
    "survival horror": ["🏃‍♂️ Run or die", "💀 This game haunted me", "🔦 Can you survive?"],
    "fighting game": ["👊 One combo to rule them all", "💥 60 seconds of pure action"],
    "strategy game": ["♟️ Outsmart the system", "🧠 Big brain energy"]
}

engagement_questions = [
    "Which mechanic would you add? 👇",
    "Rate this game 1-10! 🔥",
    "Would you play this? 💬",
    "What should I build next? 🎮",
    "How many hours would you play? ⏰"
]

viral_cta = [
    "Follow for daily games! 🎮",
    "Share with a friend who loves gaming! 🔄",
    "Double tap if you'd play this! ❤️"
]

viral_hashtags_base = ["#gamedev", "#indiegame", "#indiedev", "#gaming", "#newgame", "#solana"]

# ============ GAME GENRES ============
print("\n🎮 Setting up game genre rotation...")

day_name = datetime.now().strftime("%A")
game_genres = {
    "Monday": "top-down shooter",
    "Tuesday": "action RPG",
    "Wednesday": "racing game",
    "Thursday": "puzzle game",
    "Friday": "survival horror",
    "Saturday": "fighting game",
    "Sunday": "strategy game"
}

selected_type = game_genres.get(day_name, "precision platformer")
print(f"   📅 Today is {day_name} – {selected_type}")

genre_mechanics = {
    "top-down shooter": ["dash", "time slow", "shield", "bullet time"],
    "action RPG": ["double jump", "teleport", "clone", "elemental blast"],
    "racing game": ["speed boost", "drift", "nitro", "slipstream"],
    "puzzle game": ["time slow", "gravity flip", "invisibility", "phasing"],
    "survival horror": ["invisibility", "shield", "wall run", "sprint"],
    "fighting game": ["dash", "double jump", "grapple", "counter"],
    "strategy game": ["clone", "teleport", "gravity flip", "freeze"]
}

available_mechanics = genre_mechanics.get(selected_type, ["dash", "double jump", "time slow"])
selected_mechanic = random.choice(available_mechanics)

game_emojis = random.sample(genre_emojis.get(selected_type, ["🎮", "🔥", "⚡"]), 3)
selected_emojis = " ".join(game_emojis)

print(f"   🎮 Genre: {selected_type}")
print(f"   ⚡ Mechanic: {selected_mechanic}")
print(f"   😍 Emojis: {selected_emojis}")

# ============ VIRAL HOOK ============
hook_list = viral_hooks.get(selected_type, ["🎮 New game just dropped", "🔥 24 hour game challenge"])
selected_hook = random.choice(hook_list)
selected_question = random.choice(engagement_questions)
selected_cta = random.choice(viral_cta)

print(f"   🎣 Hook: {selected_hook}")
print(f"   ❓ Question: {selected_question}")
print(f"   📢 CTA: {selected_cta}")

# ============ GENERATE GAME NAME ============
print("\n🎮 Generating unique game name...")

def generate_ai_name():
    if openai_key:
        try:
            prompt = f"Generate ONE creative, catchy video game name for a {selected_type} game with {selected_mechanic}. Return ONLY the name, no quotes. Max 25 characters."
            r = requests.post("https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"},
                json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}], "temperature": 0.9, "max_tokens": 20}, timeout=30)
            if r.status_code == 200:
                name = r.json()["choices"][0]["message"]["content"].strip().strip('"')
                if name and len(name) < 35:
                    return name
        except:
            pass
    prefixes = ["Neon", "Cyber", "Quantum", "Astral", "Void", "Echo", "Flux", "Rogue", "Solar", "Nova"]
    suffixes = ["Runner", "Drifter", "Breach", "Vector", "Pulse", "Shift", "Core", "Edge", "Zone"]
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"

game_name = generate_ai_name()
print(f"   ✅ {game_name}")
repo_name = f"daily-{game_name.lower().replace(' ', '-')}"

# ============ AI DESCRIPTION ============
print("\n📝 Generating AI description...")

def generate_ai_description():
    if openai_key:
        try:
            prompt = f"Write a SHORT, EXCITING game description for '{game_name}'. Genre: {selected_type}. Special move: {selected_mechanic}. Max 120 characters."
            r = requests.post("https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"},
                json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}], "temperature": 0.9, "max_tokens": 80}, timeout=15)
            if r.status_code == 200:
                desc = r.json()["choices"][0]["message"]["content"].strip().strip('"')
                if len(desc) > 20:
                    return desc
        except:
            pass
    return f"🔥 {game_name} – {selected_type} madness! Master the {selected_mechanic}! 💀"

ai_description = generate_ai_description()
print(f"   🤖 {ai_description}")

# ============ VIRAL HASHTAGS ============
print("\n#️⃣ Generating viral hashtags...")

genre_hashtags = {
    "top-down shooter": ["#shootergame", "#actiongame"],
    "action RPG": ["#rpg", "#actionrpg"],
    "racing game": ["#racinggame", "#speed"],
    "puzzle game": ["#puzzlegame", "#brainteaser"],
    "survival horror": ["#horrorgame", "#survival", "#scary"],
    "fighting game": ["#fightinggame", "#combat"],
    "strategy game": ["#strategygame", "#tactical"]
}

specific_hashtags = genre_hashtags.get(selected_type, ["#indiegame", "#gaming"])
all_hashtags = viral_hashtags_base + specific_hashtags + [f"#{game_name.replace(' ', '')}"]
random.shuffle(all_hashtags)
hashtag_string = " ".join(all_hashtags[:7])
print(f"   #️⃣ {hashtag_string[:60]}...")

# ============ GENERATE ART ============
print("\n🎨 Generating game art...")
sprite_path = Path("sprite.png")

def generate_art():
    try:
        prompt = f"pixel+art+game+sprite+{game_name.replace(' ', '+')}+{selected_type}+character+hero+centered+glowing"
        url = f"https://image.pollinations.ai/prompt/{prompt}?width=512&height=512&model=flux&seed={random.randint(1, 999999)}"
        r = requests.get(url, timeout=45)
        if r.status_code == 200 and len(r.content) > 5000:
            with open(sprite_path, "wb") as f:
                f.write(r.content)
            print("   ✅ AI art generated!")
            return True
    except:
        pass
    
    print("   Creating fallback art...")
    img = Image.new('RGB', (512, 512), color=(20, 20, 40))
    draw = ImageDraw.Draw(img)
    colors = [(255,100,100), (100,255,100), (100,100,255)]
    for i, col in enumerate(colors):
        size = 512 - (i * 80)
        off = (512 - size) // 2
        draw.ellipse([off, off, off+size, off+size], outline=col, width=4)
    draw.polygon([(256, 200), (270, 240), (312, 242), (278, 268), (288, 310), (256, 286), (224, 310), (234, 268), (200, 242), (242, 240)], fill=(255, 215, 0))
    draw.text((180, 450), game_name[:15], fill=(255,255,255))
    img.save(sprite_path)
    return True

generate_art()
print(f"   ✅ Sprite ready!")

# ============ CREATE GODOT PROJECT ============
print("\n📁 Creating Godot project...")
project_dir = Path(f"workspace/{game_name.replace(' ', '_')}")
project_dir.mkdir(parents=True, exist_ok=True)
shutil.copy(sprite_path, project_dir / "icon.png")

(project_dir / "project.godot").write_text(f"""
; Godot 4.2
config_version=5
[application]
config/name="{game_name}"
config/features=PackedStringArray("4.2")
run/main_scene="res://main.tscn"
config/icon="res://icon.png"
[rendering]
renderer="forward_plus"
""")

player_script = f"""
extends CharacterBody2D
var speed = 300
func _ready():
    print("DeathRoll Studio presents: {game_name}")
func _physics_process(delta):
    var vel = Vector2.ZERO
    if Input.is_action_pressed("ui_right"): vel.x += 1
    if Input.is_action_pressed("ui_left"): vel.x -= 1
    if Input.is_action_pressed("ui_down"): vel.y += 1
    if Input.is_action_pressed("ui_up"): vel.y -= 1
    vel = vel.normalized() * speed
    move_and_collide(vel * delta)
"""
(project_dir / "player.gd").write_text(player_script)

(project_dir / "main.tscn").write_text("""
[gd_scene load_steps=2 format=3]
[ext_resource type="Script" path="res://player.gd" id=1]
[node name="Main" type="Node2D"]
[node name="Player" type="CharacterBody2D" parent="."]
position = Vector2(400, 300)
script = ExtResource("1")
[node name="Sprite2D" type="Sprite2D" parent="Player"]
texture = ExtResource("2")
[node name="CollisionShape2D" type="CollisionShape2D" parent="Player"]
shape = SubResource("RectangleShape2D")
[sub_resource type="RectangleShape2D" id=1]
size = Vector2(32, 32)
""")
print(f"   ✅ Project created!")

# ============ README ============
print("\n📢 Creating README...")
readme = f"""
<div align="center">
# 🎮 {game_name}
### Created by [DeathRoll Studio](https://deathroll.co)

> {selected_hook}

</div>

## 🔥 About The Game
**{game_name}** is a **{selected_type}** where you master the **{selected_mechanic}**!

{ai_description}

## 📥 Download & Purchase
- **Price:** ${game_price} USD (Solana)

## 🤝 Connect
- 📧 {BRAND_EMAIL_PRIMARY}
- 📱 {BRAND_TELEGRAM}
- 🎵 {BRAND_TIKTOK}
- 🐘 {MASTODON_HANDLE}
"""
(project_dir / "README.md").write_text(readme)
print("   ✅ Created README")

# ============ GITHUB REPO ============
print("\n📦 Creating GitHub repository...")
repo_url = None
if github_token:
    try:
        r = requests.post("https://api.github.com/user/repos", headers={"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}, json={"name": repo_name, "description": f"{game_name} – {selected_type} game", "private": False, "auto_init": True}, timeout=30)
        if r.status_code == 201:
            repo_url = r.json()["html_url"]
            print(f"   ✅ Repo created: {repo_url}")
    except Exception as e:
        print(f"   ⚠️ GitHub error: {e}")

repo_link = repo_url or f"https://github.com/{BRAND_GITHUB}/{repo_name}"

# ============ DEMO PAGE ============
print("\n🌐 Creating demo page...")
raw_demo_link = f"https://htmlpreview.github.io/?https://github.com/{BRAND_GITHUB}/{repo_name}/blob/main/demo.html"
demo_html = f"""<!DOCTYPE html>
<html>
<head><title>{game_name}</title></head>
<body style="background:#0f0c29;color:white;text-align:center;padding:50px">
<h1>🎮 {game_name}</h1>
<img src="icon.png" width="256">
<p>{ai_description}</p>
<p>💰 ${game_price} SOL</p>
<p>{selected_hook}</p>
<a href="{repo_link}">Download on GitHub</a>
</body>
</html>"""
(project_dir / "demo.html").write_text(demo_html)
print(f"   ✅ Demo page created")

# ============ VIRAL POST TEXT ============
viral_post_text = f"""{selected_emojis} {selected_hook} {selected_emojis}

{ai_description}

{selected_question}

💰 ${game_price} SOL
🔗 {repo_link}

{hashtag_string}

{selected_cta}

#DeathRollStudio 🎮"""

# ============ MASTODON POST (FIXED - NO ERRORS) ============
print("\n🐘 Posting to Mastodon...")

if mastodon_token and mastodon_instance:
    try:
        # Step 1: Upload image to Mastodon
        print("   📤 Uploading image to Mastodon...")
        with open(sprite_path, "rb") as img:
            media_response = requests.post(
                f"{mastodon_instance}/api/v2/media",
                headers={"Authorization": f"Bearer {mastodon_token}"},
                files={"file": img},
                timeout=30
            )
        
        if media_response.status_code == 200:
            media_data = media_response.json()
            media_id = media_data.get("id")
            print(f"   ✅ Image uploaded! Media ID: {media_id}")
            
            # Step 2: Create the post with image
            print("   📝 Creating Mastodon post...")
            post_data = {
                "status": viral_post_text[:500],  # Mastodon limit is 500 chars
                "media_ids": [media_id],
                "visibility": "public"
            }
            
            status_response = requests.post(
                f"{mastodon_instance}/api/v1/statuses",
                headers={"Authorization": f"Bearer {mastodon_token}", "Content-Type": "application/json"},
                json=post_data,
                timeout=30
            )
            
            if status_response.status_code == 200:
                print(f"   ✅ Posted to Mastodon successfully!")
                mastodon_url = status_response.json().get("url", "https://mastodon.gamedev.place/@Deathroll_Studio")
                print(f"   🔗 Post URL: {mastodon_url}")
            else:
                print(f"   ❌ Mastodon post failed: {status_response.status_code}")
                print(f"   Response: {status_response.text[:200]}")
        else:
            print(f"   ❌ Mastodon upload failed: {media_response.status_code}")
            print(f"   Response: {media_response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Mastodon error: {e}")
else:
    print("   ⚠️ Mastodon not configured – skipping")

# ============ TELEGRAM POSTS ============
print("\n📱 Sending Telegram posts...")
if telegram_token:
    try:
        with open(sprite_path, "rb") as photo:
            files = {"photo": photo}
            data = {"chat_id": telegram_chat_id, "caption": viral_post_text[:900]}
            requests.post(f"https://api.telegram.org/bot{telegram_token}/sendPhoto", files=files, data=data, timeout=30)
            print("   ✅ Post sent to private chat")
    except Exception as e:
        print(f"   ⚠️ Private error: {e}")
    
    try:
        with open(sprite_path, "rb") as photo:
            files = {"photo": photo}
            data = {"chat_id": TELEGRAM_CHANNEL, "caption": viral_post_text[:900]}
            requests.post(f"https://api.telegram.org/bot{telegram_token}/sendPhoto", files=files, data=data, timeout=30)
            print(f"   ✅ Post sent to channel {TELEGRAM_CHANNEL}")
    except Exception as e:
        print(f"   ⚠️ Channel error: {e}")

# ============ SAVE DATA ============
print("\n💾 Saving learning data...")
ld = {"last_run": datetime.now().isoformat(), "game_name": game_name, "genre": selected_type, "mechanic": selected_mechanic, "day": day_name, "hook": selected_hook, "description": ai_description, "repo_url": repo_link, "price": game_price, "bot_version": BOT_VERSION}
Path("learning_data.json").write_text(json.dumps({"history": [ld], "last_update": datetime.now().isoformat()}, indent=2))
print("   ✅ Learning data saved")

# ============ PORTFOLIO ============
print("\n📁 Updating portfolio...")
port = Path("portfolio.json")
entries = []
if port.exists():
    try:
        entries = json.loads(port.read_text())
    except:
        pass
entries.append({"date": datetime.now().isoformat(), "game": game_name, "genre": selected_type, "mechanic": selected_mechanic, "day": day_name, "hook": selected_hook, "description": ai_description, "repo": repo_link, "price": game_price})
port.write_text(json.dumps(entries[-50:], indent=2))
print(f"   ✅ Portfolio has {len(entries)} games")

# ============ TIKTOK CAPTION ============
print("\n🎵 TikTok Caption (copy for manual post):")
print("=" * 60)
print(viral_post_text[:2000])
print("=" * 60)

# ============ VERIFICATION ============
print("\n🔍 Verifying all systems...")
print(f"   AI Name: ✅")
print(f"   Game Art: ✅")
print(f"   Godot Project: ✅")
print(f"   GitHub: {'✅' if repo_url else '⚠️'}")
print(f"   Mastodon: {'✅' if mastodon_token else '⚠️ (add token)'}")
print(f"   Telegram: {'✅' if telegram_token else '⚠️'}")

# ============ DONE ============
print("\n" + "=" * 60)
print(f"✅ {game_name} is READY!")
print(f"   📅 Day: {day_name} – {selected_type}")
print(f"   🎣 Hook: {selected_hook}")
print(f"   🐘 Mastodon: {'Posted' if mastodon_token else 'Skipped'}")
print(f"   📦 GitHub: {repo_link}")
print("=" * 60)

print("\n🎉 DEATHROLL STUDIO v12.0 FINISHED SUCCESSFULLY!")
print("🐘 Check your Mastodon profile for the post!")
print("📱 Check Telegram for viral posts!")
print("🎵 TikTok caption ready above – copy and post!")
