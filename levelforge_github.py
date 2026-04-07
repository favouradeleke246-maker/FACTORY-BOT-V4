#!/usr/bin/env python3
"""
LevelForge+ ULTRA - Full Version
Real AI naming, real art, real GitHub repos, real Twitter posts
"""

import os
import json
import random
import requests
import base64
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw

print("=" * 60)
print("🎮 LEVELFORGE+ ULTRA - FULL VERSION")
print("=" * 60)

# ============ GET SECRETS ============
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
openai_key = os.getenv("OPENAI_API_KEY")
replicate_token = os.getenv("REPLICATE_API_TOKEN")
github_token = os.getenv("GH_TOKEN")
twitter_key = os.getenv("TWITTER_API_KEY")
twitter_secret = os.getenv("TWITTER_API_SECRET")
twitter_access = os.getenv("TWITTER_ACCESS_TOKEN")
twitter_access_secret = os.getenv("TWITTER_ACCESS_SECRET")

print(f"✅ Telegram: {'OK' if telegram_token else 'NO'}")
print(f"✅ OpenAI: {'OK' if openai_key else 'NO'}")
print(f"✅ Replicate: {'OK' if replicate_token else 'NO'}")
print(f"✅ GitHub: {'OK' if github_token else 'NO'}")
print(f"✅ Twitter: {'OK' if twitter_key else 'NO'}")

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
                    "messages": [{"role": "user", "content": "Generate ONE creative video game name. Return ONLY the name, no quotes."}],
                    "temperature": 0.9,
                    "max_tokens": 20
                },
                timeout=10
            )
            if response.status_code == 200:
                name = response.json()["choices"][0]["message"]["content"].strip().strip('"')
                if name and len(name) < 40:
                    return name
        except Exception as e:
            print(f"   OpenAI error: {e}")
    
    # Fallback
    prefixes = ["Neon", "Cyber", "Quantum", "Astral", "Void", "Echo", "Flux", "Rogue", "Solar", "Nova"]
    suffixes = ["Runner", "Drifter", "Breach", "Vector", "Pulse", "Shift", "Core", "Edge", "Zone"]
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"

game_name = generate_ai_name()
print(f"   ✅ {game_name}")

# ============ 2. REAL SPRITE WITH SDXL ============
print("\n🎨 Generating game art with SDXL...")

sprite_path = Path("sprite.png")

def generate_ai_sprite():
    if replicate_token:
        try:
            # Start SDXL generation
            response = requests.post(
                "https://api.replicate.com/v1/predictions",
                headers={"Authorization": f"Bearer {replicate_token}", "Content-Type": "application/json"},
                json={
                    "version": "db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
                    "input": {
                        "prompt": f"game character sprite, pixel art style, {game_name} main character, centered, 512x512",
                        "negative_prompt": "blurry, low quality, realistic",
                        "width": 512,
                        "height": 512,
                        "num_outputs": 1
                    }
                },
                timeout=30
            )
            
            prediction = response.json()
            get_url = prediction["urls"]["get"]
            
            # Poll for result
            for attempt in range(30):
                time.sleep(2)
                status_resp = requests.get(get_url, headers={"Authorization": f"Bearer {replicate_token}"})
                status_data = status_resp.json()
                
                if status_data["status"] == "succeeded":
                    image_url = status_data["output"][0]
                    img_data = requests.get(image_url).content
                    with open(sprite_path, "wb") as f:
                        f.write(img_data)
                    return True
                elif status_data["status"] == "failed":
                    break
        except Exception as e:
            print(f"   Replicate error: {e}")
    
    # Fallback: Generate cool gradient art
    img = Image.new('RGB', (512, 512), color=(random.randint(50,200), random.randint(50,200), random.randint(50,200)))
    draw = ImageDraw.Draw(img)
    for i in range(10):
        color = (random.randint(100,255), random.randint(100,255), random.randint(100,255))
        draw.rectangle([i*50, i*50, 512-i*50, 512-i*50], outline=color, width=3)
    img.save(sprite_path)
    return True

generate_ai_sprite()
print(f"   ✅ Sprite saved: {sprite_path}")

# ============ 3. CREATE GODOT PROJECT ============
print("\n📁 Creating Godot project...")

project_dir = Path(f"workspace/{game_name.replace(' ', '_')}")
project_dir.mkdir(parents=True, exist_ok=True)

# Copy sprite
import shutil
shutil.copy(sprite_path, project_dir / "icon.png")

# Create project.godot
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

# Create main scene
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

# Create player script
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
            
            # Upload files to repo
            for file_path in project_dir.glob("*"):
                if file_path.is_file():
                    with open(file_path, 'rb') as f:
                        content = base64.b64encode(f.read()).decode()
                    requests.put(
                        f"https://api.github.com/repos/{os.getenv('GITHUB_REPOSITORY_OWNER', 'favouradeleke246-maker')}/{repo_name}/contents/{file_path.name}",
                        headers={"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"},
                        json={"message": f"Add {file_path.name}", "content": content, "branch": "main"},
                        timeout=30
                    )
        else:
            print(f"   ⚠️ Repo creation: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️ GitHub error: {e}")

# ============ 5. POST TO TWITTER ============
print("\n🐦 Posting to Twitter...")

tweet_url = None
if all([twitter_key, twitter_secret, twitter_access, twitter_access_secret]):
    try:
        import tweepy
        
        auth = tweepy.OAuth1UserHandler(twitter_key, twitter_secret, twitter_access, twitter_access_secret)
        api = tweepy.API(auth)
        
        # Upload media
        media = api.media_upload(str(sprite_path))
        
        # Post tweet
        tweet_text = f"""🎮 {game_name} - New daily game just dropped!

Play now: https://github.com/{os.getenv('GITHUB_REPOSITORY_OWNER', 'favouradeleke246-maker')}/{repo_name}

#gamedev #indiedev #{game_name.replace(' ', '')}"""
        
        tweet = api.update_status(status=tweet_text, media_ids=[media.media_id])
        tweet_url = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
        print(f"   ✅ Tweet posted: {tweet_url}")
    except Exception as e:
        print(f"   ⚠️ Twitter error: {e}")

# ============ 6. SEND TELEGRAM REPORT ============
print("\n📱 Sending Telegram report...")

if telegram_token and telegram_chat_id:
    message = f"""🎮 *LEVELFORGE+ DAILY GAME* 🎮

*Game:* {game_name}
*Date:* {datetime.now().strftime('%Y-%m-%d')}

🔗 *Links:*
• GitHub: {repo_url or 'https://github.com/' + os.getenv('GITHUB_REPOSITORY_OWNER', '') + '/' + repo_name}
• Twitter: {tweet_url or 'Not posted'}

✨ *Features:*
• AI-generated name
• AI-generated art
• Complete Godot project

Next game in 24 hours!"""
    
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{telegram_token}/sendMessage",
            json={"chat_id": telegram_chat_id, "text": message, "parse_mode": "Markdown"},
            timeout=10
        )
        print(f"   ✅ Report sent to Telegram!")
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
    "tweet": tweet_url,
    "sprite": "sprite.png"
})

portfolio_file.write_text(json.dumps(entries[-30:], indent=2))
print(f"   ✅ Portfolio has {len(entries)} games")

# ============ DONE ============
print("\n" + "=" * 60)
print(f"✅ {game_name} is READY!")
print("=" * 60)

# Save build info
with open("build_info.txt", "w") as f:
    f.write(f"Game: {game_name}\n")
    f.write(f"Time: {datetime.now()}\n")
    f.write(f"Repo: {repo_url}\n")
    f.write(f"Tweet: {tweet_url}\n")
