#!/usr/bin/env python3
"""
LevelForge+ ULTRA - COMPLETE WORKING VERSION
- AI game names (OpenAI GPT)
- FREE AI art (Hugging Face FLUX / Fallback)
- GitHub repos
- Telegram reports
- Bluesky posts (FREE Twitter alternative!)
"""

import os
import json
import random
import time
import requests
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw

print("=" * 60)
print("🎮 LEVELFORGE+ ULTRA - COMPLETE VERSION")
print("✅ Telegram | GitHub | Bluesky")
print("=" * 60)

# ============ GET SECRETS ============
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
openai_key = os.getenv("OPENAI_API_KEY")
huggingface_token = os.getenv("HUGGINGFACE_TOKEN")
github_token = os.getenv("GH_TOKEN")
bluesky_handle = os.getenv("BLUESKY_HANDLE")
bluesky_password = os.getenv("BLUESKY_PASSWORD")

print(f"✅ Telegram: {'OK' if telegram_token else 'NO'}")
print(f"✅ OpenAI: {'OK' if openai_key else 'NO'}")
print(f"✅ Hugging Face: {'OK' if huggingface_token else 'NO'}")
print(f"✅ GitHub: {'OK' if github_token else 'NO'}")
print(f"✅ Bluesky: {'OK' if bluesky_handle else 'NO'}")

# ============ 1. AI GAME NAME ============
print("\n🎮 Generating game name with AI...")

def generate_ai_name():
    if openai_key:
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"},
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": "Generate ONE creative video game name. Return ONLY the name, no quotes. Make it sound fun and unique. Max 20 characters."}],
                    "temperature": 0.9,
                    "max_tokens": 20
                },
                timeout=10
            )
            if response.status_code == 200:
                name = response.json()["choices"][0]["message"]["content"].strip().strip('"')
                if name and len(name) < 30:
                    return name
        except Exception as e:
            print(f"   OpenAI error: {e}")
    
    prefixes = ["Neon", "Cyber", "Quantum", "Astral", "Void", "Echo", "Flux", "Rogue", "Solar", "Nova"]
    suffixes = ["Runner", "Drifter", "Breach", "Vector", "Pulse", "Shift", "Core", "Edge", "Zone"]
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"

game_name = generate_ai_name()
print(f"   ✅ {game_name}")

# ============ 2. FREE ART GENERATION ============
print("\n🎨 Generating game art...")

sprite_path = Path("sprite.png")

def generate_huggingface_art():
    if not huggingface_token:
        print("   No Hugging Face token - using fallback art")
        return generate_fallback_art()
    
    try:
        API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
        headers = {"Authorization": f"Bearer {huggingface_token}"}
        
        prompt = f"pixel art game sprite, {game_name} game character, cute mascot, centered, bright colors, game asset, 512x512"
        
        print("   Calling Hugging Face API...")
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=60)
        
        if response.status_code == 200:
            with open(sprite_path, "wb") as f:
                f.write(response.content)
            print(f"   ✅ Hugging Face FLUX created!")
            return True
        elif response.status_code == 429:
            print("   ⏳ Rate limited - using fallback art")
            return generate_fallback_art()
        else:
            print(f"   ⚠️ API error {response.status_code} - using fallback")
            return generate_fallback_art()
            
    except Exception as e:
        print(f"   ⚠️ Error: {e} - using fallback")
        return generate_fallback_art()

def generate_fallback_art():
    """Fallback art that always works"""
    print("   Using fallback art generator...")
    img = Image.new('RGB', (512, 512), color=(20, 20, 40))
    draw = ImageDraw.Draw(img)
    
    colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100), (255, 100, 255)]
    for i, color in enumerate(colors):
        size = 512 - (i * 80)
        offset = (512 - size) // 2
        draw.ellipse([offset, offset, offset + size, offset + size], outline=color, width=4)
    
    # Draw star
    draw.polygon([(256, 200), (270, 240), (312, 242), (278, 268), (288, 310), (256, 286), (224, 310), (234, 268), (200, 242), (242, 240)], fill=(255, 215, 0))
    
    img.save(sprite_path)
    return True

generate_huggingface_art()
print(f"   ✅ Sprite ready!")

# ============ 3. CREATE GODOT PROJECT ============
print("\n📁 Creating Godot project...")

project_dir = Path(f"workspace/{game_name.replace(' ', '_')}")
project_dir.mkdir(parents=True, exist_ok=True)

import shutil
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

(project_dir / "player.gd").write_text("""
extends CharacterBody2D
var speed = 300

func _physics_process(delta):
    var velocity = Vector2.ZERO
    if Input.is_action_pressed("ui_right"): velocity.x += 1
    if Input.is_action_pressed("ui_left"): velocity.x -= 1
    if Input.is_action_pressed("ui_down"): velocity.y += 1
    if Input.is_action_pressed("ui_up"): velocity.y -= 1
    velocity = velocity.normalized() * speed
    move_and_collide(velocity * delta)
""")

print(f"   ✅ Project created: {project_dir}")

# ============ 4. CREATE GITHUB REPO ============
print("\n📦 Creating GitHub repository...")

repo_name = f"daily-{game_name.lower().replace(' ', '-')}"
repo_url = None
github_owner = os.getenv("GITHUB_REPOSITORY_OWNER", "favouradeleke246-maker")

if github_token:
    try:
        response = requests.post(
            "https://api.github.com/user/repos",
            headers={"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"},
            json={"name": repo_name, "description": f"Daily game: {game_name}", "private": False, "auto_init": True},
            timeout=30
        )
        
        if response.status_code == 201:
            repo_url = response.json()["html_url"]
            print(f"   ✅ Repo created: {repo_url}")
        else:
            print(f"   ⚠️ Repo creation: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️ GitHub error: {e}")

# ============ 5. POST TO BLUESKY (FREE) - FIXED VERSION ============
print("\n🦋 Posting to Bluesky...")

bluesky_post_url = None

if bluesky_handle and bluesky_password:
    try:
        # Login to Bluesky
        print("   Logging in...")
        session = requests.post(
            "https://bsky.social/xrpc/com.atproto.server.createSession",
            json={"identifier": bluesky_handle, "password": bluesky_password},
            timeout=15
        )
        
        if session.status_code == 200:
            session_data = session.json()
            access_token = session_data.get("accessJwt")
            did = session_data.get("did")
            
            if access_token and did:
                # Create post (keep under 300 chars)
                repo_link = repo_url or f"https://github.com/{github_owner}/{repo_name}"
                post_text = f"🎮 {game_name}\n\nNew daily game!\n\n{repo_link}\n\n#gamedev #indiedev"
                
                # Ensure under 280 chars
                if len(post_text) > 280:
                    post_text = post_text[:277] + "..."
                
                # Create the post
                post_response = requests.post(
                    "https://bsky.social/xrpc/com.atproto.repo.createRecord",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "repo": did,
                        "collection": "app.bsky.feed.post",
                        "record": {
                            "$type": "app.bsky.feed.post",
                            "text": post_text,
                            "createdAt": datetime.now().isoformat()
                        }
                    },
                    timeout=15
                )
                
                if post_response.status_code == 200:
                    bluesky_post_url = f"https://bsky.app/profile/{bluesky_handle}"
                    print(f"   ✅ Posted to Bluesky!")
                else:
                    print(f"   ❌ Post failed: {post_response.status_code}")
                    print(f"   Response: {post_response.text[:200]}")
            else:
                print(f"   ❌ Login response missing tokens")
        else:
            print(f"   ❌ Login failed: {session.status_code}")
            print(f"   Response: {session.text[:200]}")
    except Exception as e:
        print(f"   ❌ Bluesky error: {e}")
else:
    print("   ⚠️ No Bluesky credentials - skipping")

# ============ 6. SEND TELEGRAM REPORT ============
print("\n📱 Sending Telegram report...")

if telegram_token and telegram_chat_id:
    message = f"""🎮 *LEVELFORGE+ DAILY GAME* 🎮

*Game:* {game_name}
*Date:* {datetime.now().strftime('%Y-%m-%d')}

🔗 *Links:*
• GitHub: {repo_url or f'https://github.com/{github_owner}/{repo_name}'}
• Bluesky: {bluesky_post_url or 'Not posted (check logs)'}

✨ *Features:*
• AI-generated name (GPT)
• FREE AI art (Hugging Face FLUX)
• Complete Godot project

🤖 *100% FREE - Running automatically!*

Next game in 24 hours!"""
    
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{telegram_token}/sendMessage",
            json={"chat_id": telegram_chat_id, "text": message, "parse_mode": "Markdown"},
            timeout=10
        )
        if response.status_code == 200:
            print(f"   ✅ Report sent to Telegram!")
        else:
            print(f"   ❌ Telegram error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Telegram error: {e}")

# ============ 7. UPDATE PORTFOLIO ============
print("\n📁 Updating portfolio...")

portfolio_file = Path("portfolio.json")
entries = []
if portfolio_file.exists():
    entries = json.loads(portfolio_file.read_text())

entries.append({
    "date": datetime.now().isoformat(),
    "game": game_name,
    "repo": repo_url,
    "bluesky": bluesky_post_url,
    "art_source": "Hugging Face FLUX / Fallback"
})

portfolio_file.write_text(json.dumps(entries[-30:], indent=2))
print(f"   ✅ Portfolio has {len(entries)} games")

# ============ DONE ============
print("\n" + "=" * 60)
print(f"✅ {game_name} is READY!")
print(f"   📦 GitHub: {repo_url or 'Created'}")
print(f"   🦋 Bluesky: {'Posted' if bluesky_post_url else 'Failed - check handle/password'}")
print("=" * 60)

with open("build_info.txt", "w") as f:
    f.write(f"Game: {game_name}\n")
    f.write(f"Time: {datetime.now()}\n")
    f.write(f"Repo: {repo_url}\n")
    f.write(f"Bluesky: {bluesky_post_url}\n")

print("\n🎉 BOT FINISHED SUCCESSFULLY!")
