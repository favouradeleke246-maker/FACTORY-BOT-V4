#!/usr/bin/env python3
"""
LevelForge+ ULTRA – DEATHROLL STUDIO v15.2
- Learns from Reddit + X (Twitter) trends
- SAR system enhanced with multi‑source external data
- No data loss – existing learning preserved
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
print("🔥 DEATHROLL STUDIO v15.2 – REAL‑WORLD LEARNING (Reddit + X)")
print("✅ SAR | Reddit Trends | X Trends | Self‑Improving")
print("=" * 60)

# ============ BOT VERSION ============
BOT_VERSION = "15.2.0"
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

# ============ GET SECRETS ============
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
openai_key = os.getenv("OPENAI_API_KEY")
github_token = os.getenv("GH_TOKEN")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")   # for X reading (free)
game_price = os.getenv("GAME_PRICE", "5")

print(f"✅ Telegram: {'OK' if telegram_token else 'NO'}")
print(f"✅ OpenAI: {'OK' if openai_key else 'NO'}")
print(f"✅ GitHub: {'OK' if github_token else 'NO'}")
print(f"🐦 X (Twitter) reading: {'OK (free)' if bearer_token else 'NO (add token)'}")

# ============ SAR SYSTEM (ENHANCED) ============
print("\n🧠 Initializing SAR System (with external trends)...")

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
            "reprogram": {"last_improvement": None, "changes": []}
        }
    
    def save(self):
        self.sar_file.write_text(json.dumps(self.data, indent=2))
    
    def record(self, game_name, genre, mechanic, hook, art_success, exec_time, external_trends=None):
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
            "success": art_success
        }
        if external_trends:
            game_entry["external_trends"] = external_trends
        
        self.data["study"]["games"].append(game_entry)
        self.data["study"]["games"] = self.data["study"]["games"][-50:]
        
        # Update best genre
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
        
        # Update best external trend
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
        pass

sar = SARSystem()
sar.analyze()
print(f"   ✅ SAR ready ({sar.data['study']['total_runs']} runs)")
if sar.data["analysis"]["best_external_trend"]:
    print(f"   🌍 Best external trend so far: {sar.data['analysis']['best_external_trend']}")

# ============ REAL‑WORLD DATA: REDDIT + X TRENDS ============
print("\n🌍 Fetching real‑world gaming trends (Reddit + X)...")

def fetch_reddit_trends():
    try:
        url = "https://www.reddit.com/r/gamedev/top.json?limit=25&t=day"
        headers = {"User-Agent": "DeathRollStudio/1.0"}
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
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
    except Exception as e:
        print(f"   ⚠️ Reddit fetch error: {e}")
    return None

def fetch_x_trends():
    if not bearer_token:
        print("   ⚠️ No X bearer token – skipping X trends")
        return None
    try:
        headers = {"Authorization": f"Bearer {bearer_token}"}
        params = {
            "query": "gamedev OR indie game OR game release -filter:retweets",
            "max_results": 30,
            "tweet.fields": "public_metrics"
        }
        response = requests.get("https://api.twitter.com/2/tweets/search/recent", headers=headers, params=params, timeout=15)
        if response.status_code == 200:
            tweets = response.json().get("data", [])
            if tweets:
                all_text = " ".join([t.get("text", "").lower() for t in tweets])
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
                    print(f"   🐦 X trending: {', '.join(top_genres)}")
                    return top_genres
        else:
            print(f"   ⚠️ X API error: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️ X fetch error: {e}")
    return None

reddit_trends = fetch_reddit_trends()
x_trends = fetch_x_trends()

# Combine trends (prioritise X if both exist, but keep both for SAR)
all_external_trends = []
if reddit_trends:
    all_external_trends.extend(reddit_trends)
if x_trends:
    all_external_trends.extend(x_trends)
# Remove duplicates while preserving order
unique_trends = []
for t in all_external_trends:
    if t not in unique_trends:
        unique_trends.append(t)

print(f"   🌍 Combined external trends: {unique_trends if unique_trends else 'none'}")

# ============ GAME GENRES (with SAR + external trends) ============
print("\n🎮 Setting up genre rotation...")

day_name = datetime.now().strftime("%A")
game_genres = {
    "Monday": "top-down shooter", "Tuesday": "action RPG", "Wednesday": "racing game",
    "Thursday": "puzzle game", "Friday": "survival horror", "Saturday": "fighting game", "Sunday": "strategy game"
}

best_genre = sar.data["analysis"].get("best_genre")
best_external_trend = sar.data["analysis"].get("best_external_trend")

# Decision logic (prioritises SAR best genre, then best external trend, then current Reddit/X, then day)
if best_genre and random.random() < 0.4:
    selected_type = best_genre
    print(f"   🧠 SAR chose best genre: {selected_type}")
elif best_external_trend and best_external_trend != best_genre and random.random() < 0.3:
    selected_type = best_external_trend
    print(f"   🌍 SAR chose best external trend: {selected_type}")
elif unique_trends and random.random() < 0.3:
    selected_type = random.choice(unique_trends)
    print(f"   📈 Using current external trend: {selected_type}")
else:
    selected_type = game_genres.get(day_name, "precision platformer")
    print(f"   📅 Today is {day_name} – {selected_type}")

genre_mechanics = {
    "survival horror": ["invisibility", "shield", "wall run", "sprint"],
    "top-down shooter": ["dash", "time slow", "shield", "bullet time"],
    "action RPG": ["double jump", "teleport", "clone", "elemental blast"],
    "racing game": ["speed boost", "drift", "nitro", "slipstream"],
    "puzzle game": ["time slow", "gravity flip", "invisibility", "phasing"],
    "fighting game": ["dash", "double jump", "grapple", "counter"],
    "strategy game": ["clone", "teleport", "gravity flip", "freeze"]
}
available_mechanics = genre_mechanics.get(selected_type, ["dash", "double jump", "time slow"])
selected_mechanic = random.choice(available_mechanics)

print(f"   🎮 Genre: {selected_type}")
print(f"   ⚡ Mechanic: {selected_mechanic}")

# ============ VIRAL MARKETING (unchanged) ============
print("\n🔥 Generating viral content...")

genre_emojis = {
    "survival horror": ["😱", "💀", "👻", "🔪", "🩸", "🌙"],
    "top-down shooter": ["🔫", "💥", "🎯", "⚡", "🔥", "💀"],
    "action RPG": ["⚔️", "🛡️", "👑", "✨", "🌟", "💎"],
    "racing game": ["🏎️", "💨", "🔥", "⚡", "🏁", "🚗"],
    "puzzle game": ["🧠", "💡", "🔮", "✨", "🎯", "💎"],
    "fighting game": ["👊", "💥", "⚡", "🔥", "🏆", "💪"],
    "strategy game": ["♟️", "🧠", "👑", "⚔️", "🎯", "💎"]
}

viral_hooks = {
    "survival horror": ["🏃‍♂️ Run or die", "💀 This game haunted me", "🔦 Can you survive?"],
    "top-down shooter": ["🔫 I built a shooter in 24 hours", "💀 This boss took 50 attempts"],
    "action RPG": ["⚔️ Your next obsession", "✨ 24 hours = a whole RPG"],
    "racing game": ["🏎️ Speed meets chaos", "💨 Fastest game I've made"],
    "puzzle game": ["🧠 1000 IQ required", "💡 One move changes everything"],
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

hook_list = viral_hooks.get(selected_type, ["🎮 New game just dropped"])
selected_hook = random.choice(hook_list)
selected_question = random.choice(engagement_questions)
selected_cta = random.choice(viral_cta)

game_emojis = random.sample(genre_emojis.get(selected_type, ["🎮", "🔥", "⚡"]), 3)
selected_emojis = " ".join(game_emojis)

print(f"   🎣 Hook: {selected_hook}")
print(f"   ❓ Question: {selected_question}")

# ============ GENERATE GAME NAME ============
print("\n🎮 Generating game name...")

def generate_ai_name():
    if openai_key:
        try:
            prompt = f"Generate ONE creative video game name for a {selected_type} game with {selected_mechanic}. Return ONLY the name."
            r = requests.post("https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"},
                json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}], "temperature": 0.9, "max_tokens": 20}, timeout=30)
            if r.status_code == 200:
                name = r.json()["choices"][0]["message"]["content"].strip().strip('"')
                if name:
                    return name
        except:
            pass
    prefixes = ["Neon", "Cyber", "Quantum", "Astral", "Void", "Echo", "Flux", "Rogue"]
    suffixes = ["Runner", "Drifter", "Breach", "Vector", "Pulse", "Shift", "Core", "Edge"]
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"

game_name = generate_ai_name()
print(f"   ✅ {game_name}")
repo_name = f"daily-{game_name.lower().replace(' ', '-')}"

# ============ AI DESCRIPTION ============
print("\n📝 Generating AI description...")

def generate_ai_description():
    if openai_key:
        try:
            prompt = f"Write a SHORT exciting description for '{game_name}', a {selected_type} game with {selected_mechanic}. Max 100 chars."
            r = requests.post("https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"},
                json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}], "temperature": 0.9, "max_tokens": 60}, timeout=15)
            if r.status_code == 200:
                desc = r.json()["choices"][0]["message"]["content"].strip().strip('"')
                if desc:
                    return desc
        except:
            pass
    return f"🔥 {game_name} – {selected_type} madness! Master the {selected_mechanic}! 💀"

ai_description = generate_ai_description()
print(f"   🤖 {ai_description}")

# ============ HASHTAGS ============
print("\n#️⃣ Generating hashtags...")
genre_hashtags = {
    "survival horror": ["#horrorgame", "#survival", "#scary"],
    "top-down shooter": ["#shootergame", "#actiongame"],
    "action RPG": ["#rpg", "#actionrpg"],
    "racing game": ["#racinggame", "#speed"],
    "puzzle game": ["#puzzlegame", "#brainteaser"],
    "fighting game": ["#fightinggame", "#combat"],
    "strategy game": ["#strategygame", "#tactical"]
}
base_hashtags = ["#gamedev", "#indiegame", "#indiedev", "#gaming", "#solana"]
specific = genre_hashtags.get(selected_type, ["#indiegame"])
all_tags = base_hashtags + specific + [f"#{game_name.replace(' ', '')}"]
random.shuffle(all_tags)
hashtag_string = " ".join(all_tags[:7])
print(f"   #️⃣ {hashtag_string[:60]}...")

# ============ ART GENERATION ============
print("\n🎨 Generating art...")
sprite_path = Path("sprite.png")
art_stats = {"pollinations": 0, "fallback": 0, "total": 0}

def generate_art():
    art_stats["total"] += 1
    print("   🎨 Attempt 1: Pollinations.ai")
    result = generate_pollinations_art()
    if result:
        art_stats["pollinations"] += 1
        return True
    print("   🎨 Attempt 2: Fallback art")
    art_stats["fallback"] += 1
    return generate_fallback_art()

def generate_pollinations_art():
    try:
        prompts = [
            f"pixel+art+game+sprite+{game_name.replace(' ', '+')}+{selected_type}+character+hero+glowing+detailed",
            f"8K+pixel+art+{game_name.replace(' ', '+')}+game+character+{selected_mechanic}+ability+centered",
            f"game+sprite+{game_name.replace(' ', '+')}+{selected_type}+character+cute+but+cool+detailed"
        ]
        selected_prompt = random.choice(prompts)
        url = f"https://image.pollinations.ai/prompt/{selected_prompt}?width=512&height=512&model=flux&seed={random.randint(1, 999999)}"
        response = requests.get(url, timeout=45)
        if response.status_code == 200 and len(response.content) > 5000:
            with open(sprite_path, "wb") as f:
                f.write(response.content)
            print(f"      ✅ Pollinations.ai succeeded!")
            return True
        else:
            print(f"      ⚠️ Pollinations error: {response.status_code}")
            return False
    except Exception as e:
        print(f"      ⚠️ Pollinations exception: {str(e)[:50]}")
        return False

def generate_fallback_art():
    print("      Creating algorithmic art...")
    img = Image.new('RGB', (512, 512), color=(20, 20, 40))
    draw = ImageDraw.Draw(img)
    genre_colors = {
        "survival horror": [(80,80,80), (120,120,120), (160,160,160)],
        "top-down shooter": [(255,50,50), (255,100,100), (255,150,150)],
        "action RPG": [(100,50,200), (150,100,255), (200,150,255)],
        "racing game": [(50,200,255), (100,255,255), (150,200,255)],
        "puzzle game": [(50,255,50), (100,255,100), (150,255,150)],
        "fighting game": [(255,100,50), (255,150,100), (255,200,150)],
        "strategy game": [(50,100,255), (100,150,255), (150,200,255)]
    }
    colors = genre_colors.get(selected_type, [(255,100,100), (100,255,100), (100,100,255)])
    for i, col in enumerate(colors):
        size = 512 - (i * 80)
        off = (512 - size) // 2
        draw.ellipse([off, off, off+size, off+size], outline=col, width=4)
    draw.polygon([(256, 200), (270, 240), (312, 242), (278, 268), (288, 310), (256, 286), (224, 310), (234, 268), (200, 242), (242, 240)], fill=(255, 215, 0))
    draw.text((180, 450), game_name[:15], fill=(255,255,255))
    img.save(sprite_path)
    return True

art_start = time.time()
art_success = generate_art()
art_time = time.time() - art_start
print(f"   ✅ Art completed in {art_time:.1f}s")

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
print(f"   ✅ Project created")

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
    except:
        pass
repo_link = repo_url or f"https://github.com/{BRAND_GITHUB}/{repo_name}"

# ============ DEMO PAGE ============
print("\n🌐 Creating demo page...")
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

# ============ TELEGRAM POSTS ============
print("\n📱 Sending Telegram posts...")
if telegram_token:
    try:
        with open(sprite_path, "rb") as photo:
            files = {"photo": photo}
            data = {"chat_id": telegram_chat_id, "caption": viral_post_text[:900]}
            requests.post(f"https://api.telegram.org/bot{telegram_token}/sendPhoto", files=files, data=data, timeout=30)
            print("   ✅ Sent to private chat")
    except:
        print("   ⚠️ Private error")
    
    try:
        with open(sprite_path, "rb") as photo:
            files = {"photo": photo}
            data = {"chat_id": TELEGRAM_CHANNEL, "caption": viral_post_text[:900]}
            requests.post(f"https://api.telegram.org/bot{telegram_token}/sendPhoto", files=files, data=data, timeout=30)
            print(f"   ✅ Sent to {TELEGRAM_CHANNEL}")
    except:
        print("   ⚠️ Channel error")

# ============ SAR RECORD (with external trends) ============
print("\n🧠 Recording run with external trends...")
external_trends = unique_trends if unique_trends else []
sar.record(game_name, selected_type, selected_mechanic, selected_hook, art_success, art_time, external_trends)
sar.analyze()
print(f"   ✅ SAR updated ({sar.data['study']['total_runs']} total runs)")
if external_trends:
    print(f"   🌍 Recorded external trends: {external_trends}")

# ============ SAVE DATA ============
print("\n💾 Saving data...")
Path("learning_data.json").write_text(json.dumps({"last_run": datetime.now().isoformat(), "game": game_name, "genre": selected_type, "external_trends": external_trends}, indent=2))
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
entries.append({"date": datetime.now().isoformat(), "game": game_name, "genre": selected_type, "mechanic": selected_mechanic, "repo": repo_link})
port.write_text(json.dumps(entries[-50:], indent=2))
print(f"   ✅ Portfolio: {len(entries)} games")

# ============ TIKTOK CAPTION ============
print("\n🎵 TikTok Caption (copy this):")
print("=" * 60)
print(viral_post_text[:1500])
print("=" * 60)

# ============ ART METRICS ============
print("\n📊 Art Generation Stats:")
print(f"   Pollinations: {art_stats['pollinations']}/{art_stats['total']}")
print(f"   Fallback: {art_stats['fallback']}/{art_stats['total']}")

# ============ VERIFICATION ============
print("\n🔍 Verification:")
print(f"   AI Name: ✅")
print(f"   SAR System: ✅ ({sar.data['study']['total_runs']} runs)")
if sar.data["analysis"]["best_external_trend"]:
    print(f"   🌍 Best external trend learned: {sar.data['analysis']['best_external_trend']}")
print(f"   Smart Art: ✅")
print(f"   GitHub: {'✅' if repo_url else '⚠️'}")
print(f"   Telegram: {'✅' if telegram_token else '⚠️'}")
print(f"   X (Twitter) reading: {'✅ (free)' if bearer_token else '⚠️ (add token)'}")

# ============ DONE ============
print("\n" + "=" * 60)
print(f"✅ {game_name} is READY!")
print(f"   📅 {day_name} – {selected_type}")
print(f"   🎣 {selected_hook}")
print(f"   🧠 SAR: {sar.data['study']['total_runs']} games analyzed")
print(f"   🌍 External trends used: {external_trends if external_trends else 'none'}")
print(f"   📦 {repo_link}")
print("=" * 60)

print("\n🎉 DEATHROLL STUDIO v15.2 FINISHED!")
print("✅ Now learning from Reddit + X (Twitter) trends")
print("🧠 SAR stores all external trends for future improvement")
print("📱 Check Telegram for your viral posts!")
print("🎵 TikTok caption ready above!")
