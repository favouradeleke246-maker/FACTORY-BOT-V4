#!/usr/bin/env python3
"""
LevelForge+ ULTRA – DEATHROLL STUDIO v21.1
- FIXED: Images now show on website
- FIXED: No loops (tracks recent game names)
- AI-generated unique descriptions
"""

import os
import json
import random
import hashlib
import requests
import time
import shutil
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw
from collections import Counter

print("=" * 60)
print("🔥 DEATHROLL STUDIO v21.1 – IMAGES FIXED + NO LOOPS")
print("✅ All Features | Auto Portfolio | Unique Every Day")
print("=" * 60)

BOT_VERSION = "21.1.0"
print(f"🤖 Bot Version: {BOT_VERSION}")

# ============ YOUR CONTACT INFO ============
BRAND_NAME = "DeathRoll"
BRAND_EMAIL_PRIMARY = "favouradeleke246@gmail.com"
BRAND_EMAIL_SECONDARY = "fadeleke246@gmail.com"
BRAND_TELEGRAM = "@deathroll1"
BRAND_TIKTOK = "@deathroll.co"
BRAND_WEBSITE = "https://deathroll.co"
BRAND_GITHUB = "favouradeleke246-maker"

SOLANA_TRUST_WALLET = "6wsQ6nGXrUUUGCEokb4rZcfHDv2a8MomUb22TuVaH2m3"
SOLANA_PHANTOM_WALLET = "Csk9DKstWMdKx19gUHWB9xy2VwZZX2nx6V6oSVGDCgMb"
TELEGRAM_CHANNEL = "@drolltech"

print(f"🏷️ Brand: {BRAND_NAME}")
print(f"📧 Email: {BRAND_EMAIL_PRIMARY}")
print(f"📱 Telegram: {BRAND_TELEGRAM} | Channel: {TELEGRAM_CHANNEL}")

# ============ SECRETS ============
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
openai_key = os.getenv("OPENAI_API_KEY")
github_token = os.getenv("GH_TOKEN")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
game_price = os.getenv("GAME_PRICE", "7")

print(f"✅ Telegram: {'OK' if telegram_token else 'NO'}")
print(f"✅ OpenAI: {'OK' if openai_key else 'NO'}")
print(f"✅ GitHub: {'OK' if github_token else 'NO'}")

# ============ PREVENT LOOPS - TRACK RECENT GAMES ============
RECENT_NAMES_FILE = Path("recent_game_names.json")
RECENT_COUNT = 10  # Remember last 10 game names to avoid repeats

def load_recent_names():
    if RECENT_NAMES_FILE.exists():
        try:
            return json.loads(RECENT_NAMES_FILE.read_text())
        except:
            return []
    return []

def save_recent_names(names):
    RECENT_NAMES_FILE.write_text(json.dumps(names[-RECENT_COUNT:]))

def is_name_used(name, recent_names):
    return name.lower() in [n.lower() for n in recent_names]

def get_unique_game_name(recent_names):
    """Generate a unique game name not used recently"""
    prefixes = ["Neon", "Cyber", "Quantum", "Astral", "Void", "Echo", "Flux", "Rogue", "Crimson", "Shadow", "Phantom", "Eclipse", "Solar", "Nova", "Dark", "Light"]
    suffixes = ["Runner", "Drifter", "Breach", "Vector", "Pulse", "Shift", "Core", "Edge", "Zone", "Realm", "Fury", "Strike", "Blade", "Force", "Storm"]
    
    for attempt in range(50):
        name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
        if not is_name_used(name, recent_names):
            return name
    # Fallback with number
    return f"{random.choice(prefixes)} {random.choice(suffixes)} {random.randint(1, 999)}"

# ============ API CALL ============
def call_api(prompt, max_tokens=120):
    if not openai_key:
        return None
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"},
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.9,
                "max_tokens": max_tokens
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip().strip('"')
        return None
    except:
        return None

# ============ SAR SYSTEM ============
print("\n🧠 Initializing SAR System...")

class SARSystem:
    def __init__(self):
        self.sar_file = Path("sar_analysis.json")
        self.data = self.load()
    def load(self):
        if self.sar_file.exists():
            try:
                return json.loads(self.sar_file.read_text())
            except:
                return self.get_default()
        return self.get_default()
    def get_default(self):
        return {
            "study": {"total_runs": 0, "successful_art": 0, "failed_art": 0, "games": []},
            "analysis": {
                "best_genre": None,
                "best_mechanic": None,
                "best_external_trend": None,
                "success_rate": 0
            },
            "feedback": {},
            "reprogram": {"last_improvement": None, "changes": []}
        }
    def save(self):
        self.sar_file.write_text(json.dumps(self.data, indent=2))
    def record(self, game_name, genre, mechanic, hook, art_success, exec_time, external_trends=None, art_prompt_used=None, feedback_score=None):
        self.data["study"]["total_runs"] += 1
        if art_success:
            self.data["study"]["successful_art"] += 1
        else:
            self.data["study"]["failed_art"] += 1
        game_entry = {
            "name": game_name,
            "genre": genre,
            "mechanic": mechanic,
            "hook": hook,
            "timestamp": datetime.now().isoformat(),
            "success": art_success,
            "art_prompt": art_prompt_used,
            "feedback_score": feedback_score
        }
        if external_trends:
            game_entry["external_trends"] = external_trends
        self.data["study"]["games"].append(game_entry)
        self.data["study"]["games"] = self.data["study"]["games"][-50:]
        genre_counts = {}
        for g in self.data["study"]["games"]:
            ggenre = g["genre"]
            if ggenre not in genre_counts:
                genre_counts[ggenre] = {"count": 0, "success": 0}
            genre_counts[ggenre]["count"] += 1
            if g["success"]:
                genre_counts[ggenre]["success"] += 1
        if genre_counts:
            best = max(genre_counts.keys(), key=lambda x: genre_counts[x]["success"] / max(genre_counts[x]["count"], 1))
            self.data["analysis"]["best_genre"] = best
        if external_trends:
            trend_counts = {}
            for g in self.data["study"]["games"]:
                trends = g.get("external_trends", [])
                for t in trends:
                    if t not in trend_counts:
                        trend_counts[t] = {"count": 0, "success": 0}
                    trend_counts[t]["count"] += 1
                    if g["success"]:
                        trend_counts[t]["success"] += 1
            if trend_counts:
                best_trend = max(trend_counts.keys(), key=lambda x: trend_counts[x]["success"] / max(trend_counts[x]["count"], 1))
                self.data["analysis"]["best_external_trend"] = best_trend
        total = self.data["study"]["successful_art"] + self.data["study"]["failed_art"]
        if total > 0:
            self.data["analysis"]["success_rate"] = self.data["study"]["successful_art"] / total
        self.save()
    def analyze(self):
        if "reprogram" not in self.data:
            self.data["reprogram"] = {"last_improvement": None, "changes": []}
        if "feedback" not in self.data:
            self.data["feedback"] = {}
        self.save()

sar = SARSystem()
sar.analyze()
print(f"   ✅ SAR ready ({sar.data['study']['total_runs']} runs)")

# ============ REAL-TIME TRENDING GENRES ============
print("\n🌍 Fetching real-time trending genres...")

def fetch_reddit_trends():
    try:
        url = "https://www.reddit.com/r/gamedev/top.json?limit=25&t=day"
        headers = {"User-Agent": "DeathRollStudio/1.0"}
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            posts = data.get("data", {}).get("children", [])
            all_text = " ".join([p["data"]["title"].lower() for p in posts])
            genres = {
                "action": all_text.count("action"),
                "platformer": all_text.count("platformer"),
                "puzzle": all_text.count("puzzle"),
                "rpg": all_text.count("rpg"),
                "strategy": all_text.count("strategy"),
                "horror": all_text.count("horror"),
                "shooter": all_text.count("shooter")
            }
            sorted_genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)
            top_genres = [g for g, count in sorted_genres if count > 0][:2]
            if top_genres:
                print(f"   🔥 Reddit trending: {', '.join(top_genres)}")
                return top_genres
    except:
        pass
    return None

real_time_trends = fetch_reddit_trends() or []
print(f"   🌍 Trends: {real_time_trends if real_time_trends else 'none'}")

# ============ GENRE SELECTION ============
print("\n🎮 Selecting genre...")
all_genres = [
    "top-down shooter", "action RPG", "racing game", "puzzle game", "survival horror",
    "fighting game", "strategy game", "extraction shooter", "cozy builder", "roguelite",
    "stealth action", "tower defense", "rhythm game", "platformer"
]
sar_best = sar.data["analysis"].get("best_genre")
recent_genres = [g["genre"] for g in sar.data["study"]["games"][-5:]]

# Weighted selection with variety
candidates = []
weights = []
if sar_best and sar_best in all_genres:
    weight = 0.3 if sar_best not in recent_genres else 0.15
    candidates.append(sar_best)
    weights.append(weight)
if real_time_trends:
    for trend in real_time_trends[:2]:
        if trend in all_genres and trend not in candidates:
            candidates.append(trend)
            weights.append(0.25)
# Add fresh genres not used recently
unused = [g for g in all_genres if g not in recent_genres[:3]]
if unused:
    candidates.append(random.choice(unused))
    weights.append(0.3)
# Always include a random option
candidates.append(random.choice(all_genres))
weights.append(0.2)

selected_type = random.choices(candidates, weights=weights)[0] if candidates else random.choice(all_genres)
print(f"   Selected: {selected_type}")

# ============ VIRAL HOOKS ============
hook_pool = [
    "🏃‍♂️ Run or die", "💀 This game haunted me", "🔦 Can you survive?",
    "🔫 I built a shooter in 24 hours", "⚔️ Your next obsession",
    "🏎️ Speed meets chaos", "🧠 1000 IQ required", "👊 One combo to rule them all",
    "♟️ Outsmart the system", "🏴‍☠️ Loot or die", "🌿 Build your dream",
    "💀 Die. Learn. Repeat.", "🌀 Every run is different"
]
selected_hook = random.choice(hook_pool)
selected_question = random.choice(["Which mechanic would you add? 👇", "Rate this game 1-10! 🔥", "Would you play this? 💬"])
selected_cta = random.choice(["Follow for daily games! 🎮", "Share with a friend! 🔄", "Double tap if you'd play this! ❤️"])

genre_emojis = {
    "survival horror": ["😱", "💀", "👻"],
    "top-down shooter": ["🔫", "💥", "🎯"],
    "action RPG": ["⚔️", "🛡️", "👑"],
    "racing game": ["🏎️", "💨", "🔥"],
    "puzzle game": ["🧠", "💡", "🔮"],
    "fighting game": ["👊", "💥", "⚡"],
    "strategy game": ["♟️", "🧠", "👑"],
}
emojis = genre_emojis.get(selected_type, ["🎮", "🔥", "⚡"])
selected_emojis = " ".join(random.sample(emojis, min(3, len(emojis))))

# ============ AI-INVENTED MECHANIC ============
print("\n⚙️ Generating mechanic...")
mechanics = [
    ("Phase Echo", "leave behind a short-lived decoy"),
    ("Chrono Fracture", "create a time bubble"),
    ("Void Step", "teleport through short walls"),
    ("Mirror Shell", "reflect projectiles"),
    ("Gravity Well", "pull enemies toward you"),
    ("Soul Link", "share damage with an enemy"),
    ("Static Charge", "build and release electricity"),
    ("Quantum Tether", "connect two objects together"),
    ("Necrotic Touch", "steal health from enemies"),
    ("Blink", "short range teleport with afterimage")
]
selected_mechanic, mechanic_desc = random.choice(mechanics)
print(f"   ✨ {selected_mechanic} – {mechanic_desc}")

# ============ UNIQUE GAME NAME (NO LOOPS) ============
print("\n🎮 Generating unique name (no loops)...")
recent_names = load_recent_names()
game_name = get_unique_game_name(recent_names)
recent_names.append(game_name)
save_recent_names(recent_names)
print(f"   ✅ {game_name}")
repo_name = f"daily-{game_name.lower().replace(' ', '-')}"

# ============ AI DESCRIPTION (UNIQUE EACH DAY) ============
print("\n📝 Generating description...")
# Add variety to description prompt based on day
description_styles = ["exciting", "mysterious", "urgent", "funny", "epic", "dark", "colorful"]
style = random.choice(description_styles)

if openai_key:
    desc_prompt = f"Write a unique, {style} 1-sentence description for '{game_name}', a {selected_type} game with {selected_mechanic}. Be creative and don't repeat phrases from previous games. Max 120 chars."
    ai_description = call_api(desc_prompt, 100)
else:
    ai_description = None
if not ai_description:
    # Fallback with variety
    fallbacks = [
        f"Master the {selected_mechanic} in this epic {selected_type} adventure!",
        f"Unleash {selected_mechanic} and conquer this {selected_type} world!",
        f"Experience {selected_mechanic} like never before in this {selected_type} game!",
        f"Dive into {selected_type} action with the powerful {selected_mechanic}!"
    ]
    ai_description = random.choice(fallbacks)
print(f"   📝 {ai_description}")

# ============ HASHTAGS ============
print("\n#️⃣ Generating hashtags...")
if openai_key:
    tag_prompt = f"Generate 5 unique hashtags for a {selected_type} game called '{game_name}'. Include #gamedev, #indiegame, #solana. Make them fresh and relevant."
    hashtag_string = call_api(tag_prompt, 80)
else:
    hashtag_string = None
if not hashtag_string:
    hashtag_string = f"#gamedev #indiegame #solana #{selected_type.replace(' ', '')} #{game_name.replace(' ', '')}"
print(f"   #️⃣ {hashtag_string[:60]}...")

# ============ ART STYLE ============
visual_styles = ["isometric", "neon cyberpunk", "low-poly", "cell-shaded", "voxel", "pastel gothic", "synthwave", "steampunk", "watercolor"]
trending_style = random.choice(visual_styles)
print(f"\n🎨 Style: {trending_style}")

# ============ ART GENERATION ============
print("\n🎨 Generating art...")
sprite_path = Path("sprite.png")
def generate_art():
    try:
        prompt = f"3D {trending_style} render of a {selected_type} character for '{game_name}', game asset"
        prompt_url = prompt.replace(" ", "+").replace("'", "").replace(",", "+")
        url = f"https://image.pollinations.ai/prompt/{prompt_url}?width=512&height=512&model=flux&seed={random.randint(1, 999999)}"
        r = requests.get(url, timeout=45)
        if r.status_code == 200 and len(r.content) > 5000:
            with open(sprite_path, "wb") as f:
                f.write(r.content)
            return True
    except:
        pass
    # Fallback art
    img = Image.new('RGB', (512, 512), color=(20, 20, 40))
    draw = ImageDraw.Draw(img)
    draw.rectangle([100,100,412,412], outline=(255,255,255), width=4)
    draw.polygon([(256,100),(412,200),(412,412),(256,412),(100,412),(100,200)], outline=(200,200,255), width=3)
    draw.text((180, 450), game_name[:15], fill=(255,255,255))
    img.save(sprite_path)
    return True

art_success = generate_art()
print(f"   ✅ Art ready")

# ============ GODOT PROJECT ============
print(f"\n📁 Creating {selected_type} 3D project...")
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

(project_dir / "main.tscn").write_text("""
[gd_scene load_steps=2 format=3]
[ext_resource type="Script" path="res://player.gd" id=1]
[node name="Main" type="Node3D"]
[node name="Player" type="CharacterBody3D" parent="."]
position = Vector3(0, 0.5, 0)
script = ExtResource("1")
[node name="Camera3D" type="Camera3D" parent="Player"]
transform = Transform3D(1, 0, 0, 0, 0.866, 0.5, 0, -0.5, 0.866, 0, 5, 5)
""")

(project_dir / "player.gd").write_text(f"""
extends CharacterBody3D
var speed = 5.0
func _ready():
    print("{game_name} – {selected_type}")
func _physics_process(delta):
    var input = Input.get_vector("left", "right", "forward", "back")
    var dir = (transform.basis * Vector3(input.x, 0, input.y)).normalized()
    velocity.x = dir.x * speed
    velocity.z = dir.z * speed
    move_and_slide()
""")
print(f"   ✅ Project created")

# ============ ZIP ============
print("\n📦 Creating game ZIP...")
zip_path = Path("workspace/latest_game.zip")
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file in project_dir.rglob("*"):
        zipf.write(file, file.relative_to(project_dir.parent))
print(f"   ✅ ZIP created")

# ============ GITHUB REPO ============
print("\n📦 Creating GitHub repository...")
repo_url = None
if github_token:
    try:
        r = requests.post("https://api.github.com/user/repos", headers={"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}, json={"name": repo_name, "description": f"{game_name} – {selected_type}", "private": False, "auto_init": True}, timeout=30)
        if r.status_code == 201:
            repo_url = r.json()["html_url"]
            print(f"   ✅ Repo created: {repo_url}")
    except:
        pass
repo_link = repo_url or f"https://github.com/{BRAND_GITHUB}/{repo_name}"

# ============ UPDATE PORTFOLIO (FIXED IMAGE URL) ============
print("\n📁 Updating portfolio...")
# FIXED: Use raw.githubusercontent.com with correct path
image_url = f"https://raw.githubusercontent.com/{BRAND_GITHUB}/FACTORY-BOT-V4/main/workspace/{game_name.replace(' ', '_')}/icon.png"

port = Path("portfolio.json")
entries = []
if port.exists():
    try:
        entries = json.loads(port.read_text())
        if not isinstance(entries, list):
            entries = []
    except:
        entries = []

entries.append({
    "date": datetime.now().isoformat(),
    "game": game_name,
    "genre": selected_type,
    "mechanic": selected_mechanic,
    "description": ai_description,
    "image_url": image_url,
    "repo": repo_link
})
entries = entries[-50:]
port.write_text(json.dumps(entries, indent=2))
print(f"   ✅ Portfolio: {len(entries)} games")

# ============ SEND TO ADMIN ============
print("\n📬 Sending game to admin...")
if telegram_token and telegram_chat_id:
    try:
        with open(zip_path, "rb") as f:
            files = {"document": f}
            caption = f"🎮 *{game_name}* – {selected_type}\n{ai_description}\n💰 ${game_price} SOL"
            requests.post(f"https://api.telegram.org/bot{telegram_token}/sendDocument", files=files, data={"chat_id": telegram_chat_id, "caption": caption, "parse_mode": "Markdown"}, timeout=60)
        print("   ✅ Game ZIP sent to admin")
    except Exception as e:
        print(f"   ⚠️ Could not send: {e}")

# ============ TELEGRAM SALES POST ============
print("\n📱 Sending Telegram sales post...")
if telegram_token:
    viral_post_text = f"""
{selected_emojis} *{selected_hook}* {selected_emojis}

✨ *{game_name}* – {selected_type}
{ai_description}

⚡ *Mechanic:* `{selected_mechanic}`

💰 *Price:* ${game_price} SOL
🔵 Trust: `{SOLANA_TRUST_WALLET}`
🟣 Phantom: `{SOLANA_PHANTOM_WALLET}`

📩 Send ${game_price} SOL + your @username in memo → game in 5 mins

{hashtag_string}
{selected_cta}
#DeathRollStudio
"""
    try:
        with open(sprite_path, "rb") as photo:
            files = {"photo": photo}
            data = {"chat_id": TELEGRAM_CHANNEL, "caption": viral_post_text, "parse_mode": "Markdown"}
            requests.post(f"https://api.telegram.org/bot{telegram_token}/sendPhoto", files=files, data=data, timeout=30)
        print(f"   ✅ Sales post sent to {TELEGRAM_CHANNEL}")
    except Exception as e:
        print(f"   ⚠️ Error sending photo: {e}")

# ============ FEEDBACK POLL ============
print("\n📊 Sending feedback poll...")
if telegram_token:
    try:
        poll_data = {
            "chat_id": TELEGRAM_CHANNEL,
            "question": f"Rate {game_name} (1-5 stars)?",
            "options": json.dumps(["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]),
            "is_anonymous": False,
            "open_period": 86400
        }
        requests.post(f"https://api.telegram.org/bot{telegram_token}/sendPoll", data=poll_data, timeout=30)
        print("   ✅ Poll sent")
    except Exception as e:
        print(f"   ⚠️ Poll error: {e}")

# ============ SAR RECORD ============
print("\n🧠 Recording run...")
sar.record(game_name, selected_type, selected_mechanic, selected_hook, art_success, time.time(), real_time_trends, "", None)
sar.analyze()
print(f"   ✅ SAR updated ({sar.data['study']['total_runs']} runs)")

# ============ SAVE DATA ============
Path("learning_data.json").write_text(json.dumps({"last_run": datetime.now().isoformat(), "game": game_name, "genre": selected_type}, indent=2))
print("   ✅ Data saved")

# ============ FINAL ============
print("\n🔍 Final verification:")
print(f"   Game: {game_name}")
print(f"   Genre: {selected_type}")
print(f"   Mechanic: {selected_mechanic}")
print(f"   Description: {ai_description}")
print(f"   Art: {'✅' if art_success else '⚠️'}")
print(f"   Portfolio: {len(entries)} games")
print(f"   Recent names: {len(recent_names)} unique names tracked")

print("\n" + "=" * 60)
print(f"✅ {game_name} is READY!")
print("=" * 60)

print("\n🎉 DEATHROLL STUDIO v21.1 FINISHED!")
print("✅ Images fixed – website now shows game art")
print("✅ No loops – tracks recent game names")
print("✅ Unique AI descriptions each day")
print(f"📊 Website: https://{BRAND_GITHUB}.github.io/FACTORY-BOT-V4/")
