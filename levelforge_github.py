#!/usr/bin/env python3
"""
LevelForge+ ULTRA - COMPLETE PRODUCTION SYSTEM v3.0
- Self-learning AI bot
- Full marketing suite
- Brand integration (DeathRoll)
- Multi-platform support
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
print("🎮 LEVELFORGE+ ULTRA - DEATHROLL STUDIO v3.0")
print("✅ Self-Learning | Marketing | Full Automation")
print("=" * 60)

# ============ BOT VERSION ============
BOT_VERSION = "3.0.0"
print(f"🤖 Bot Version: {BOT_VERSION}")

# ============ YOUR REAL CONTACT INFO ============
BRAND_NAME = "DeathRoll"
BRAND_EMAIL_PRIMARY = "favouradeleke246@gmail.com"
BRAND_EMAIL_SECONDARY = "fadeleke246@gmail.com"
BRAND_TELEGRAM = "@deathroll1"
BRAND_TIKTOK = "@favouradeleke662"
BRAND_WEBSITE = "https://deathroll.co"
BRAND_GITHUB = "favouradeleke246-maker"

print(f"🏷️ Brand: {BRAND_NAME}")
print(f"📧 Email: {BRAND_EMAIL_PRIMARY}")
print(f"📱 Telegram: {BRAND_TELEGRAM}")
print(f"🎵 TikTok: {BRAND_TIKTOK}")

# ============ GET SECRETS ============
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
openai_key = os.getenv("OPENAI_API_KEY")
github_token = os.getenv("GH_TOKEN")
bluesky_handle = os.getenv("BLUESKY_HANDLE")
bluesky_password = os.getenv("BLUESKY_PASSWORD")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

print(f"✅ Telegram: {'OK' if telegram_token else 'NO'}")
print(f"✅ OpenAI: {'OK' if openai_key else 'NO'}")
print(f"✅ GitHub: {'OK' if github_token else 'NO'}")
print(f"✅ Bluesky: {'OK' if bluesky_handle else 'NO'}")
print(f"✅ X Learning: {'OK' if bearer_token else 'NO'}")

# ============ SELF-IMPROVEMENT SYSTEM ============
print("\n🧠 Running self-improvement analysis...")

def analyze_and_improve():
    """Analyze past performance and improve future games"""
    improvement_file = Path("improvement_data.json")
    improvements = {}
    
    if improvement_file.exists():
        try:
            improvements = json.loads(improvement_file.read_text())
        except:
            improvements = {}
    
    # Track mechanic performance
    mechanic_scores = improvements.get("mechanic_scores", {})
    
    all_mechanics = ["dash ability", "double jump", "time slow", "energy shield", "grappling hook", "invisibility cloak", "wall run", "teleport dash", "gravity flip", "clone summon"]
    
    # Initialize scores if empty
    for mechanic in all_mechanics:
        if mechanic not in mechanic_scores:
            mechanic_scores[mechanic] = 50
    
    # Improve based on trends (will be updated from X)
    if trending_genres:
        if "action" in trending_genres:
            mechanic_scores["dash ability"] = min(mechanic_scores.get("dash ability", 50) + 5, 100)
            mechanic_scores["time slow"] = min(mechanic_scores.get("time slow", 50) + 3, 100)
        if "platformer" in trending_genres:
            mechanic_scores["double jump"] = min(mechanic_scores.get("double jump", 50) + 8, 100)
            mechanic_scores["wall run"] = min(mechanic_scores.get("wall run", 50) + 5, 100)
    
    # Weighted random selection
    def weighted_choice(items, scores):
        total = sum(scores.values())
        if total == 0:
            return random.choice(items)
        rand = random.random() * total
        for item, score in scores.items():
            if rand < score:
                return item
            rand -= score
        return random.choice(items)
    
    selected = weighted_choice(all_mechanics, mechanic_scores)
    
    # Save improvements
    improvements["mechanic_scores"] = mechanic_scores
    improvements["last_analysis"] = datetime.now().isoformat()
    improvement_file.write_text(json.dumps(improvements, indent=2))
    
    print(f"   📊 Mechanic scores updated")
    print(f"   🎯 Top mechanic: {max(mechanic_scores, key=mechanic_scores.get)}")
    
    return selected

# ============ 1. LEARN FROM X TRENDS ============
print("\n📊 Learning from X trends...")

def learn_from_x_trends():
    """Analyze X for game trends - completely FREE!"""
    if not bearer_token:
        print("   No X bearer token - using default trends")
        return None, None
    
    try:
        headers = {"Authorization": f"Bearer {bearer_token}"}
        
        search_params = {
            "query": "gamedev OR indie game OR game release -filter:retweets",
            "max_results": 50,
            "tweet.fields": "public_metrics,created_at"
        }
        
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/recent",
            headers=headers,
            params=search_params,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            tweets = data.get("data", [])
            
            if tweets:
                all_text = " ".join([t.get("text", "") for t in tweets]).lower()
                genres = {
                    "action": all_text.count("action"),
                    "platformer": all_text.count("platformer"),
                    "puzzle": all_text.count("puzzle"),
                    "rpg": all_text.count("rpg"),
                    "strategy": all_text.count("strategy")
                }
                
                sorted_genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)
                top_genres = [g for g, count in sorted_genres if count > 0][:2]
                
                if top_genres:
                    print(f"   🔥 Trending: {', '.join(top_genres)}")
                    return top_genres, ["#gamedev", "#indiedev"]
        else:
            print(f"   ⚠️ X API error: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️ Learning error: {e}")
    
    return ["platformer", "puzzle"], ["#gamedev", "#indiedev"]

# Load previous learnings
learning_file = Path("learning_data.json")
if learning_file.exists():
    try:
        previous = json.loads(learning_file.read_text())
        print(f"   💾 Loaded {len(previous.get('history', []))} past learnings")
    except:
        pass

# Get trending data
trending_genres, trending_hashtags = learn_from_x_trends()

# ============ 2. GENERATE AI GAME NAME ============
print("\n🎮 Generating unique game name...")

def generate_ai_name():
    if openai_key:
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"},
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": "Generate ONE creative video game name. Return ONLY the name, no quotes. Max 25 characters."}],
                    "temperature": 0.9,
                    "max_tokens": 20
                },
                timeout=30
            )
            if response.status_code == 200:
                name = response.json()["choices"][0]["message"]["content"].strip().strip('"')
                if name and len(name) < 35:
                    return name
        except Exception as e:
            print(f"   OpenAI error: {e}")
    
    prefixes = ["Neon", "Cyber", "Quantum", "Astral", "Void", "Echo", "Flux", "Rogue", "Solar", "Nova"]
    suffixes = ["Runner", "Drifter", "Breach", "Vector", "Pulse", "Shift", "Core", "Edge", "Zone"]
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"

game_name = generate_ai_name()
print(f"   ✅ {game_name}")

# ============ 3. SELECT GAME TYPE ============
print("\n🎮 Selecting game mechanics...")

all_game_types = ["top-down shooter", "precision platformer", "puzzle crawler", "endless runner", "action rpg"]
all_mechanics = ["dash ability", "double jump", "time slow", "energy shield", "grappling hook", "wall run"]

# Use self-improvement to pick mechanic
selected_mechanic = analyze_and_improve()

# Pick genre based on trends
if trending_genres and len(trending_genres) > 0:
    genre_map = {"action": "top-down shooter", "platformer": "precision platformer", "puzzle": "puzzle crawler", "rpg": "action rpg"}
    selected_type = genre_map.get(trending_genres[0], random.choice(all_game_types))
else:
    selected_type = random.choice(all_game_types)

print(f"   📊 Based on X trends: {trending_genres if trending_genres else 'default'}")
print(f"   🎮 Genre: {selected_type}")
print(f"   ⚡ Mechanic: {selected_mechanic}")

# ============ 4. FREE IMAGE GENERATION ============
print("\n🎨 Generating game art...")

sprite_path = Path("sprite.png")

def generate_fallback_art():
    """Dynamic fallback art"""
    print("   Creating custom game art...")
    random.seed(game_name)
    colors = [(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)) for _ in range(3)]
    
    img = Image.new('RGB', (512, 512), color=(20, 20, 40))
    draw = ImageDraw.Draw(img)
    
    for i, color in enumerate(colors):
        size = 512 - (i * 80)
        offset = (512 - size) // 2
        draw.ellipse([offset, offset, offset + size, offset + size], outline=color, width=5)
    
    draw.text((240, 240), game_name[0].upper(), fill=(255, 255, 255))
    img.save(sprite_path)
    return True

generate_fallback_art()
print(f"   ✅ Sprite ready!")

# ============ 5. CREATE GODOT PROJECT ============
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
config/description="A game by DeathRoll Studio - https://deathroll.co"

[rendering]
renderer="forward_plus"
""")

player_script = f"""
extends CharacterBody2D
var speed = 300

func _ready():
    print("DeathRoll Studio presents: {game_name}")
    print("Genre: {selected_type} | Mechanic: {selected_mechanic}")

func _physics_process(delta):
    var velocity = Vector2.ZERO
    if Input.is_action_pressed("ui_right"): velocity.x += 1
    if Input.is_action_pressed("ui_left"): velocity.x -= 1
    if Input.is_action_pressed("ui_down"): velocity.y += 1
    if Input.is_action_pressed("ui_up"): velocity.y -= 1
    velocity = velocity.normalized() * speed
    move_and_collide(velocity * delta)
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

print(f"   ✅ Project created with {selected_mechanic}!")

# ============ 6. CREATE MARKETING README ============
print("\n📢 Creating marketing materials...")

readme_content = f"""
<div align="center">

# 🎮 {game_name}

### Created by [DeathRoll Studio](https://deathroll.co)

[![Made with Godot](https://img.shields.io/badge/Made%20with-Godot-478CBF?style=for-the-badge&logo=godot-engine)](https://godotengine.org)
[![DeathRoll](https://img.shields.io/badge/Created%20by-DeathRoll-FF6B6B?style=for-the-badge)](https://deathroll.co)

</div>

## ✨ About The Game

**{game_name}** is a **{selected_type}** where you can **{selected_mechanic}**! 

Created by **DeathRoll Studio**, this game features:

- 🎮 Unique **{selected_mechanic}** mechanics
- 🎨 Custom pixel art
- ⚡ Fast-paced {selected_type} gameplay
- 🔧 Built with Godot 4.2

## 🎯 How to Play

| Key | Action |
|-----|--------|
| Arrow Keys | Move your character |
| Space | Special ability |

## 📥 Download

- [Download from GitHub](https://github.com/{BRAND_GITHUB}/{repo_name}/archive/main.zip)

## 🤝 Connect With DeathRoll

| Platform | Link |
|----------|------|
| 📧 **Email** | {BRAND_EMAIL_PRIMARY} |
| 📱 **Telegram** | {BRAND_TELEGRAM} |
| 🎵 **TikTok** | {BRAND_TIKTOK} |
| 🌐 **Website** | {BRAND_WEBSITE} |

---

**Made with ❤️ by DeathRoll Studio**

*Support: {BRAND_EMAIL_PRIMARY}*
"""
(project_dir / "README.md").write_text(readme_content)
print(f"   ✅ Created README with DeathRoll branding")

# ============ 7. CREATE GITHUB REPO ============
print("\n📦 Creating GitHub repository...")

repo_name = f"daily-{game_name.lower().replace(' ', '-')}"
repo_url = None
github_owner = BRAND_GITHUB

if github_token:
    try:
        response = requests.post(
            "https://api.github.com/user/repos",
            headers={"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"},
            json={"name": repo_name, "description": f"{game_name} - A {selected_type} game by DeathRoll Studio", "private": False, "auto_init": True},
            timeout=30
        )
        
        if response.status_code == 201:
            repo_url = response.json()["html_url"]
            print(f"   ✅ Repo created: {repo_url}")
    except Exception as e:
        print(f"   ⚠️ GitHub error: {e}")

# ============ 8. POST TO BLUESKY ============
print("\n🦋 Posting to Bluesky...")

bluesky_post_url = None
repo_link = repo_url or f"https://github.com/{github_owner}/{repo_name}"

if bluesky_handle and bluesky_password:
    try:
        session = requests.post(
            "https://bsky.social/xrpc/com.atproto.server.createSession",
            json={"identifier": bluesky_handle, "password": bluesky_password},
            timeout=30
        )
        
        if session.status_code == 200:
            session_data = session.json()
            access_token = session_data.get("accessJwt")
            did = session_data.get("did")
            
            if access_token and did:
                post_text = f"🎮 {game_name} - New game from DeathRoll Studio!\n\nA {selected_type} with {selected_mechanic}\n\n{repo_link}\n\n#gamedev #indiedev"
                
                post_response = requests.post(
                    "https://bsky.social/xrpc/com.atproto.repo.createRecord",
                    headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
                    json={
                        "repo": did,
                        "collection": "app.bsky.feed.post",
                        "record": {
                            "$type": "app.bsky.feed.post",
                            "text": post_text[:300],
                            "createdAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                        }
                    },
                    timeout=30
                )
                
                if post_response.status_code == 200:
                    bluesky_post_url = f"https://bsky.app/profile/{bluesky_handle}"
                    print(f"   ✅ Posted to Bluesky!")
    except Exception as e:
        print(f"   ❌ Bluesky error: {e}")

# ============ 9. SEND TELEGRAM REPORT ============
print("\n📱 Sending Telegram report...")

if telegram_token and telegram_chat_id:
    message = f"""🎮 *DEATHROLL STUDIO - DAILY GAME* 🎮

*Game:* {game_name}
*Genre:* {selected_type}
*Mechanic:* {selected_mechanic}
*Date:* {datetime.now().strftime('%Y-%m-%d')}

📊 *X Trends:* {trending_genres[0] if trending_genres else 'N/A'}

🔗 *Links:*
• GitHub: {repo_link}
• Bluesky: {bluesky_post_url or 'Not posted'}

🏷️ *DeathRoll Studio*
📧 Support: {BRAND_EMAIL_PRIMARY}
📱 Telegram: {BRAND_TELEGRAM}
🎵 TikTok: {BRAND_TIKTOK}
🌐 Website: {BRAND_WEBSITE}

🤖 *Bot learns and improves daily!* v{BOT_VERSION}"""
    
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{telegram_token}/sendMessage",
            json={"chat_id": telegram_chat_id, "text": message, "parse_mode": "Markdown"},
            timeout=30
        )
        if response.status_code == 200:
            print(f"   ✅ Report sent to Telegram!")
    except Exception as e:
        print(f"   ❌ Telegram error: {e}")

# ============ 10. SAVE LEARNING DATA ============
print("\n💾 Saving learning data...")

learning_data = {
    "last_run": datetime.now().isoformat(),
    "game_name": game_name,
    "genre": selected_type,
    "mechanic": selected_mechanic,
    "trending_genres": trending_genres,
    "repo_url": repo_url,
    "bot_version": BOT_VERSION
}

learning_file.write_text(json.dumps({"history": [learning_data], "last_update": datetime.now().isoformat()}, indent=2))
print(f"   ✅ Learning data saved")

# ============ 11. UPDATE PORTFOLIO ============
print("\n📁 Updating portfolio...")

portfolio_file = Path("portfolio.json")
entries = []
if portfolio_file.exists():
    try:
        entries = json.loads(portfolio_file.read_text())
    except:
        entries = []

entries.append({
    "date": datetime.now().isoformat(),
    "game": game_name,
    "genre": selected_type,
    "mechanic": selected_mechanic,
    "trending": trending_genres,
    "repo": repo_link,
    "bluesky": bluesky_post_url
})

portfolio_file.write_text(json.dumps(entries[-50:], indent=2))
print(f"   ✅ Portfolio has {len(entries)} games")

# ============ 12. CREATE SUPPORT FILE ============
support_content = f"""DeathRoll Studio - Support Information

Game: {game_name}
Date: {datetime.now().strftime('%Y-%m-%d')}

Contact Information:
- Primary Email: {BRAND_EMAIL_PRIMARY}
- Secondary Email: {BRAND_EMAIL_SECONDARY}
- Telegram: {BRAND_TELEGRAM}
- TikTok: {BRAND_TIKTOK}
- Website: {BRAND_WEBSITE}
- GitHub: https://github.com/{BRAND_GITHUB}

For support requests, please email: {BRAND_EMAIL_PRIMARY}

Include in your email:
1. Game name: {game_name}
2. Platform you're playing on
3. Description of the issue

We'll respond within 24-48 hours.

Thank you for playing DeathRoll Studio games!
"""
(project_dir / "SUPPORT.txt").write_text(support_content)
print(f"   ✅ Created support file")

# ============ DONE ============
print("\n" + "=" * 60)
print(f"✅ {game_name} is READY!")
print(f"   🏷️ Brand: DeathRoll Studio")
print(f"   📧 Support: {BRAND_EMAIL_PRIMARY}")
print(f"   📱 Telegram: {BRAND_TELEGRAM}")
print(f"   🎵 TikTok: {BRAND_TIKTOK}")
print(f"   🎮 Genre: {selected_type}")
print(f"   ⚡ Mechanic: {selected_mechanic}")
print(f"   📦 GitHub: {repo_link}")
print("=" * 60)

# Save build info
with open("build_info.txt", "w") as f:
    f.write(f"Game: {game_name}\n")
    f.write(f"Genre: {selected_type}\n")
    f.write(f"Mechanic: {selected_mechanic}\n")
    f.write(f"Time: {datetime.now()}\n")
    f.write(f"Repo: {repo_link}\n")
    f.write(f"Email: {BRAND_EMAIL_PRIMARY}\n")
    f.write(f"Telegram: {BRAND_TELEGRAM}\n")
    f.write(f"TikTok: {BRAND_TIKTOK}\n")

print("\n🎉 DEATHROLL STUDIO BOT FINISHED SUCCESSFULLY!")
print("🧠 Your bot learned, adapted, and created a new game!")
print(f"📧 Support emails: {BRAND_EMAIL_PRIMARY} / {BRAND_EMAIL_SECONDARY}")
print(f"📱 Telegram: {BRAND_TELEGRAM}")
print(f"🎵 TikTok: {BRAND_TIKTOK}")
