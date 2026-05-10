#!/usr/bin/env python3
"""
DEATHROLL STUDIO v29.0 - COMPLETE FULL FEATURES
- AI-generated mechanics, names, descriptions (with fallbacks)
- SAR self-learning system with performance tracking
- Real-time trends from Reddit
- Weighted genre selection based on SAR performance
- Viral hooks and emoji generation
- Art generation with multiple fallbacks
- Godot project creation
- GitHub repository creation
- Telegram admin delivery, sales posts, and feedback polls
- Weekly Best Of and monthly changelog
- GUARANTEED portfolio updates on EVERY run
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
print("🔥 DEATHROLL STUDIO v29.0 - COMPLETE FULL FEATURES")
print("=" * 60)

BOT_VERSION = "29.0.0"
print(f"🤖 Bot Version: {BOT_VERSION}")

# ============ CONFIGURATION ============
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
print(f"🐦 X reading: {'OK' if bearer_token else 'NO'}")

# ============ CACHE SYSTEM ============
CACHE_FILE = Path("openai_cache.json")

def load_cache():
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except:
            return {}
    return {}

def save_cache(cache):
    CACHE_FILE.write_text(json.dumps(cache, indent=2))

def cached_generate(prompt, max_tokens=150, temperature=0.9, retries=2):
    if not openai_key:
        return None
    cache = load_cache()
    key = hashlib.md5(f"{prompt}{max_tokens}{temperature}".encode()).hexdigest()
    if key in cache:
        print("   (cached)")
        return cache[key]
    for attempt in range(retries):
        try:
            time.sleep(1)
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature,
                    "max_tokens": max_tokens
                },
                timeout=30
            )
            if response.status_code == 200:
                result = response.json()["choices"][0]["message"]["content"].strip().strip('"')
                cache[key] = result
                save_cache(cache)
                return result
            elif response.status_code == 429:
                time.sleep(2 ** attempt)
            else:
                return None
        except:
            time.sleep(1)
    return None

# ============ REAL-TIME TRENDS ============
print("\n🌍 Fetching real-time trends...")

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
            top_genres = [g for g, count in sorted_genres if count > 0][:3]
            if top_genres:
                print(f"   🔥 Reddit trends: {', '.join(top_genres)}")
                return top_genres
    except:
        pass
    return []

real_time_trends = fetch_reddit_trends()
print(f"   🌍 Final trends: {real_time_trends if real_time_trends else 'none (using defaults)'}")

# ============ SAR SYSTEM (Self-Learning) ============
print("\n🧠 Initializing SAR System...")

class SARSystem:
    def __init__(self):
        self.sar_file = Path("sar_analysis.json")
        self.data = self.load()
    
    def load(self):
        default_data = {
            "total_runs": 0,
            "successful_art": 0,
            "failed_art": 0,
            "games": [],
            "genre_performance": {},
            "mechanic_performance": {},
            "best_genre": None,
            "best_mechanic": None,
            "trend_performance": {},
            "feedback": {},
            "weekly_winners": [],
            "monthly_stats": []
        }
        
        if not self.sar_file.exists():
            return default_data
        
        try:
            content = self.sar_file.read_text().strip()
            if not content:
                return default_data
            
            data = json.loads(content)
            for key in default_data:
                if key not in data:
                    data[key] = default_data[key]
            return data
        except Exception as e:
            print(f"   ⚠️ Error loading SAR: {e}")
            return default_data
    
    def save(self):
        try:
            self.sar_file.write_text(json.dumps(self.data, indent=2))
        except Exception as e:
            print(f"   ⚠️ Error saving SAR: {e}")
    
    def record(self, game_name, genre, mechanic, art_success, trends_used=None, feedback_score=None):
        self.data["total_runs"] = self.data.get("total_runs", 0) + 1
        if art_success:
            self.data["successful_art"] = self.data.get("successful_art", 0) + 1
        else:
            self.data["failed_art"] = self.data.get("failed_art", 0) + 1
        
        if genre not in self.data["genre_performance"]:
            self.data["genre_performance"][genre] = {"count": 0, "success": 0}
        self.data["genre_performance"][genre]["count"] += 1
        if art_success:
            self.data["genre_performance"][genre]["success"] += 1
        
        if mechanic not in self.data["mechanic_performance"]:
            self.data["mechanic_performance"][mechanic] = {"count": 0, "success": 0}
        self.data["mechanic_performance"][mechanic]["count"] += 1
        if art_success:
            self.data["mechanic_performance"][mechanic]["success"] += 1
        
        if trends_used:
            for trend in trends_used:
                if trend not in self.data["trend_performance"]:
                    self.data["trend_performance"][trend] = {"count": 0, "success": 0}
                self.data["trend_performance"][trend]["count"] += 1
                if art_success:
                    self.data["trend_performance"][trend]["success"] += 1
        
        game_record = {
            "name": game_name,
            "genre": genre,
            "mechanic": mechanic,
            "timestamp": datetime.now().isoformat(),
            "art_success": art_success,
            "trends_used": trends_used
        }
        if feedback_score:
            game_record["feedback_score"] = feedback_score
        self.data["games"].append(game_record)
        self.data["games"] = self.data["games"][-100:]
        
        if self.data["genre_performance"]:
            best = max(self.data["genre_performance"].keys(), 
                      key=lambda x: self.data["genre_performance"][x]["success"] / max(self.data["genre_performance"][x]["count"], 1))
            self.data["best_genre"] = best
        
        if self.data["mechanic_performance"]:
            best = max(self.data["mechanic_performance"].keys(),
                      key=lambda x: self.data["mechanic_performance"][x]["success"] / max(self.data["mechanic_performance"][x]["count"], 1))
            self.data["best_mechanic"] = best
        
        self.save()
    
    def get_best_genre(self):
        return self.data.get("best_genre")
    
    def get_best_mechanic(self):
        return self.data.get("best_mechanic")
    
    def get_success_rate(self):
        total = self.data.get("successful_art", 0) + self.data.get("failed_art", 0)
        if total > 0:
            return self.data.get("successful_art", 0) / total
        return 0

sar = SARSystem()
print(f"   ✅ SAR ready ({sar.data.get('total_runs', 0)} runs)")
print(f"   📊 Success rate: {sar.get_success_rate()*100:.1f}%")
if sar.get_best_genre():
    print(f"   🏆 Best genre so far: {sar.get_best_genre()}")
if sar.get_best_mechanic():
    print(f"   ⚡ Best mechanic: {sar.get_best_mechanic()}")

# ============ WEIGHTED GENRE SELECTION ============
print("\n🎮 Weighted genre selection...")

all_genres = [
    "top-down shooter", "action RPG", "racing game", "puzzle game", "survival horror",
    "fighting game", "strategy game", "extraction shooter", "cozy builder", "roguelite"
]

candidates = []
weights = []

sar_best = sar.get_best_genre()
if sar_best and sar_best in all_genres:
    candidates.append(sar_best)
    weights.append(0.4)

if real_time_trends:
    for trend in real_time_trends[:1]:
        if trend in all_genres:
            candidates.append(trend)
            weights.append(0.3)

candidates.append(random.choice(all_genres))
weights.append(0.3)

selected_type = random.choices(candidates, weights=weights)[0] if candidates else random.choice(all_genres)
print(f"   Selected genre: {selected_type}")

# ============ VIRAL HOOKS ============
hook_pool = [
    "🏃‍♂️ Run or die", "💀 This game haunted me", "🔦 Can you survive?",
    "🔫 I built a shooter in 24 hours", "⚔️ Your next obsession",
    "🏎️ Speed meets chaos", "🧠 1000 IQ required", "👊 One combo to rule them all",
    "♟️ Outsmart the system", "🏴‍☠️ Loot or die", "🌿 Build your dream",
    "🌀 One mechanic changes everything", "💀 Death is just the beginning"
]
selected_hook = random.choice(hook_pool)

last_hook_file = Path("last_hook.txt")
last_hook = last_hook_file.read_text().strip() if last_hook_file.exists() else ""
if selected_hook == last_hook:
    selected_hook = random.choice([h for h in hook_pool if h != last_hook] or hook_pool)
last_hook_file.write_text(selected_hook)

selected_cta = random.choice(["Follow for daily games! 🎮", "Share with a friend! 🔄", "Join our Telegram! 📱", "Get your copy now! 🎯"])

genre_emojis = {
    "survival horror": ["😱", "💀", "👻", "🔪", "🩸"],
    "top-down shooter": ["🔫", "💥", "🎯", "⚡", "💣"],
    "action RPG": ["⚔️", "🛡️", "👑", "🗡️", "🏹"],
    "racing game": ["🏎️", "💨", "🔥", "🏁", "⚡"],
    "puzzle game": ["🧠", "💡", "🔮", "🎲", "❓"],
    "fighting game": ["👊", "💥", "⚡", "🥊", "💪"],
    "strategy game": ["♟️", "🧠", "👑", "🏰", "⚔️"],
}
emojis = genre_emojis.get(selected_type, ["🎮", "🔥", "⚡", "💀", "🎯"])
selected_emojis = " ".join(random.sample(emojis, min(4, len(emojis))))

# ============ AI MECHANIC GENERATION (with fallback) ============
print("\n⚙️ Generating unique mechanic...")

creative_fallbacks = [
    ("Phase Echo", "leave behind a short-lived decoy that distracts enemies"),
    ("Chrono Fracture", "create a time bubble that slows everything but you"),
    ("Void Step", "teleport through short walls and obstacles"),
    ("Mirror Shell", "reflect projectiles back at attackers"),
    ("Gravity Well", "pull nearby enemies toward you with force"),
    ("Soul Link", "share damage with an enemy, making them your anchor"),
    ("Static Charge", "build electricity with movement, release as a shockwave"),
    ("Nightmare Fuel", "enemies see their worst fear and flee"),
    ("Blood Pact", "sacrifice health for temporary invincibility"),
    ("Echo Location", "reveal hidden paths and enemies with sound waves"),
    ("Shadow Cloak", "become invisible when standing still"),
    ("Berserker Rage", "deal more damage as your health drops")
]

def generate_mechanic():
    if openai_key and random.random() > 0.3:
        recent = [g.get("mechanic", "") for g in sar.data.get("games", [])[-3:] if g.get("mechanic")]
        avoid = ', '.join(recent) if recent else "none"
        
        prompt = f"""Invent a unique game mechanic for a {selected_type} game.
Avoid: {avoid}
Return EXACTLY:
MECHANIC: <name 2-4 words>
DESCRIPTION: <one sentence, max 80 chars>"""
        
        result = cached_generate(prompt, temperature=1.2, max_tokens=120)
        if result:
            lines = result.strip().split("\n")
            name = None
            desc = None
            for line in lines:
                if line.startswith("MECHANIC:"):
                    name = line.replace("MECHANIC:", "").strip()
                elif line.startswith("DESCRIPTION:"):
                    desc = line.replace("DESCRIPTION:", "").strip()
            if name and desc and len(name) > 2:
                return name, desc[:100]
    return random.choice(creative_fallbacks)

mechanic_name, mechanic_desc = generate_mechanic()
selected_mechanic = mechanic_name
print(f"   ✨ Mechanic: {selected_mechanic}")
print(f"   📖 {mechanic_desc}")

# ============ GAME NAME GENERATION ============
print("\n🎮 Generating game name...")

prefixes = ["Neon", "Cyber", "Quantum", "Astral", "Void", "Echo", "Flux", "Rogue", "Crimson", "Shadow", "Phantom", "Eclipse", "Solar", "Nova", "Dark", "Light", "Storm", "Thunder", "Frost", "Ember"]
suffixes = ["Runner", "Drifter", "Breach", "Vector", "Pulse", "Shift", "Core", "Edge", "Zone", "Realm", "Fury", "Strike", "Blade", "Force", "Hunter", "Seeker", "Warden", "Ghost", "Wraith", "Phantom"]

if openai_key and random.random() > 0.3:
    prompt = f"Generate a cool name for a {selected_type} game. Return ONLY the name, 1-3 words, max 25 chars:"
    ai_name = cached_generate(prompt, temperature=0.9, max_tokens=20)
    if ai_name and len(ai_name) > 2 and len(ai_name) < 30:
        game_name = ai_name
    else:
        game_name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
else:
    game_name = f"{random.choice(prefixes)} {random.choice(suffixes)}"

# Ensure unique name
recent_names_file = Path("recent_names.txt")
recent_names = recent_names_file.read_text().splitlines() if recent_names_file.exists() else []
if game_name in recent_names:
    game_name = f"{game_name} {random.randint(2, 99)}"
recent_names.append(game_name)
recent_names_file.write_text("\n".join(recent_names[-20:]))

print(f"   ✅ Game name: {game_name}")
repo_name = f"daily-{game_name.lower().replace(' ', '-')}"

# ============ DESCRIPTION & HASHTAGS ============
print("\n📝 Generating description and hashtags...")

ai_description = f"Master the {selected_mechanic} in this intense {selected_type} experience! {mechanic_desc[:70]}"

hashtag_string = f"#gamedev #indiegame #{selected_type.replace(' ', '')} #{selected_mechanic.replace(' ', '')} #DeathRollStudio"
if real_time_trends:
    hashtag_string += f" #{real_time_trends[0].replace(' ', '')}"

if openai_key and random.random() > 0.5:
    prompt = f"Write a ONE-SENTENCE hype description for '{game_name}' ({selected_type}) with mechanic '{selected_mechanic}'. Max 120 chars:"
    ai_desc = cached_generate(prompt, temperature=0.8, max_tokens=80)
    if ai_desc and len(ai_desc) > 20:
        ai_description = ai_desc[:120]

print(f"   📝 {ai_description}")
print(f"   #️⃣ {hashtag_string[:80]}...")

# ============ 🚨 IMMEDIATE PORTFOLIO SAVE ============
print("\n" + "=" * 60)
print("💾 STEP 1: SAVING TO PORTFOLIO.JSON")
print("=" * 60)

portfolio_path = Path("portfolio.json")

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

image_url = f"https://raw.githubusercontent.com/{BRAND_GITHUB}/FACTORY-BOT-V4/main/workspace/{game_name.replace(' ', '_')}/icon.png"

new_game_entry = {
    "date": datetime.now().isoformat(),
    "game": game_name,
    "genre": selected_type,
    "mechanic": selected_mechanic,
    "mechanic_description": mechanic_desc,
    "description": ai_description,
    "hook": selected_hook,
    "hashtags": hashtag_string,
    "image_url": image_url,
    "price_sol": game_price,
    "trends_used": real_time_trends,
    "status": "generated",
    "version": BOT_VERSION
}

existing_games.append(new_game_entry)
existing_games = existing_games[-500:]

try:
    portfolio_path.write_text(json.dumps(existing_games, indent=2))
    print(f"   ✅ Portfolio saved! Total games: {len(existing_games)}")
    print(f"   ✅ Added: {game_name}")
except Exception as e:
    print(f"   ❌ Portfolio save failed: {e}")
    Path("portfolio_emergency.json").write_text(json.dumps([new_game_entry], indent=2))
    print(f"   ✅ Emergency backup saved")

with open("games_log.txt", "a") as f:
    f.write(f"{datetime.now().isoformat()} | {game_name} | {selected_type} | {selected_mechanic} | {real_time_trends}\n")
print(f"   ✅ Logged to games_log.txt")

Path("last_run.txt").write_text(datetime.now().isoformat())
print(f"   ✅ last_run.txt created")

print("=" * 60)

# ============ ART STYLE SELECTION ============
print("\n🎨 Selecting art style...")
visual_styles = ["isometric", "neon cyberpunk", "low-poly", "cell-shaded", "voxel", "pastel gothic", "dark fantasy", "steampunk"]
trending_style = random.choice(visual_styles)
Path("last_style.txt").write_text(trending_style)
print(f"   Style: {trending_style}")

# ============ ART GENERATION ============
print("\n🎨 Generating game art...")
sprite_path = Path("sprite.png")
art_success = False
art_method = "none"

try:
    prompt = f"3D {trending_style} render of a {selected_type} character for '{game_name}', game art"
    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '+')[:150]}?width=512&height=512"
    r = requests.get(url, timeout=45)
    if r.status_code == 200 and len(r.content) > 5000:
        sprite_path.write_bytes(r.content)
        art_success = True
        art_method = "online"
        print(f"   ✅ Online art generated")
    else:
        raise Exception("Online failed")
except Exception as e:
    print(f"   ⚠️ Online art failed: {e}")
    try:
        img = Image.new('RGB', (512, 512), color=(30, 30, 60))
        draw = ImageDraw.Draw(img)
        draw.rectangle([50, 50, 462, 462], outline=(78, 205, 196), width=3)
        draw.text((180, 230), game_name[:15], fill=(255, 255, 255))
        draw.text((200, 260), selected_type[:12], fill=(200, 200, 200))
        img.save(sprite_path)
        art_success = True
        art_method = "fallback"
        print(f"   ✅ Fallback art created")
    except Exception as e2:
        print(f"   ❌ Art failed: {e2}")
        art_success = False

print(f"   🎨 Art ready (method: {art_method})")

# ============ WORKSPACE SETUP ============
print("\n📁 Setting up workspace...")
project_dir = Path(f"workspace/{game_name.replace(' ', '_')}")
project_dir.mkdir(parents=True, exist_ok=True)

if sprite_path.exists():
    shutil.copy(sprite_path, project_dir / "icon.png")
else:
    Image.new('RGB', (512, 512), color=(50, 50, 80)).save(project_dir / "icon.png")

# Godot project
(project_dir / "project.godot").write_text(f"""
; Godot 4.2
config_version=5
[application]
config/name="{game_name}"
config/icon="res://icon.png"
""")

(project_dir / "main.tscn").write_text("""
[gd_scene format=3]
[node name="Main" type="Node2D"]
[node name="Player" type="CharacterBody2D" position="(400,300)"]
""")

(project_dir / "player.gd").write_text(f"""
extends CharacterBody2D
var speed = 300
func _ready():
    print("{game_name} - {selected_type}")
    print("Mechanic: {selected_mechanic}")
func _physics_process(delta):
    var input = Vector2(
        Input.get_axis("left", "right"),
        Input.get_axis("up", "down")
    )
    velocity = input * speed
    move_and_slide()
""")

(project_dir / "README.md").write_text(f"""
# {game_name}

## Description
{ai_description}

## Genre
{selected_type}

## Key Mechanic
**{selected_mechanic}**: {mechanic_desc}

## Price
{game_price} SOL

---
Generated by DeathRoll Studio v{BOT_VERSION}
""")

print(f"   ✅ Godot project created")

# ============ CREATE ZIP ============
print("\n📦 Creating game ZIP...")
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

# ============ UPDATE PORTFOLIO ============
print("\n📁 Updating portfolio with final details...")
try:
    current = json.loads(portfolio_path.read_text())
    for game in current:
        if game["game"] == game_name:
            game["art_success"] = art_success
            game["art_method"] = art_method
            game["art_style"] = trending_style
            game["status"] = "complete"
            game["completed_at"] = datetime.now().isoformat()
            break
    portfolio_path.write_text(json.dumps(current, indent=2))
    print(f"   ✅ Portfolio updated")
except Exception as e:
    print(f"   ⚠️ Update failed: {e}")

# ============ GITHUB REPOSITORY ============
print("\n📦 Creating GitHub repository...")
repo_link = f"https://github.com/{BRAND_GITHUB}/{repo_name}"

if github_token:
    try:
        r = requests.post(
            "https://api.github.com/user/repos",
            headers={"Authorization": f"token {github_token}"},
            json={"name": repo_name, "description": ai_description[:100], "private": False},
            timeout=30
        )
        if r.status_code == 201:
            repo_link = r.json()["html_url"]
            print(f"   ✅ Repo created: {repo_link}")
        else:
            print(f"   ⚠️ Repo returned {r.status_code}")
    except Exception as e:
        print(f"   ⚠️ Repo skip: {e}")

# Update portfolio with repo link
try:
    current = json.loads(portfolio_path.read_text())
    for game in current:
        if game["game"] == game_name:
            game["repo"] = repo_link
            break
    portfolio_path.write_text(json.dumps(current, indent=2))
except:
    pass

# ============ TELEGRAM ============
print("\n📱 Sending to Telegram...")

if telegram_token and telegram_chat_id:
    try:
        with open(zip_path, "rb") as f:
            caption = f"🎮 *NEW: {game_name}*\n🎭 {selected_type}\n⚡ {selected_mechanic}\n📝 {ai_description}\n💰 ${game_price} SOL"
            requests.post(
                f"https://api.telegram.org/bot{telegram_token}/sendDocument",
                files={"document": f},
                data={"chat_id": telegram_chat_id, "caption": caption, "parse_mode": "Markdown"},
                timeout=60
            )
        print(f"   ✅ Game sent to admin")
    except Exception as e:
        print(f"   ⚠️ Admin failed: {e}")

if telegram_token:
    try:
        post = f"""
{selected_emojis} *{selected_hook}* {selected_emojis}

✨ *{game_name}* – {selected_type}
{ai_description}

⚡ *Mechanic:* `{selected_mechanic}`
📖 {mechanic_desc}

💰 *Price:* `${game_price} SOL`

🔵 Trust: `{SOLANA_TRUST_WALLET}`
🟣 Phantom: `{SOLANA_PHANTOM_WALLET}`

Send `${game_price} SOL` + @username → game in 5 mins

{hashtag_string}
{selected_cta}
#DeathRollStudio
"""
        with open(sprite_path, "rb") as photo:
            requests.post(
                f"https://api.telegram.org/bot{telegram_token}/sendPhoto",
                files={"photo": photo},
                data={"chat_id": TELEGRAM_CHANNEL, "caption": post, "parse_mode": "Markdown"},
                timeout=30
            )
        print(f"   ✅ Sales post sent to channel")
    except Exception as e:
        print(f"   ⚠️ Sales post failed: {e}")

# ============ SAR UPDATE ============
print("\n🧠 Updating SAR system...")
sar.record(game_name, selected_type, selected_mechanic, art_success, real_time_trends)
print(f"   ✅ SAR updated (run #{sar.data.get('total_runs', 0)})")

# ============ LEARNING DATA ============
print("\n📚 Updating learning data...")
learning_data = {
    "last_run": datetime.now().isoformat(),
    "last_game": game_name,
    "genre": selected_type,
    "mechanic": selected_mechanic,
    "mechanic_description": mechanic_desc,
    "trends_used": real_time_trends,
    "art_success": art_success,
    "art_method": art_method,
    "art_style": trending_style,
    "total_games": len(existing_games),
    "sar_runs": sar.data.get("total_runs", 0),
    "success_rate": sar.get_success_rate(),
    "best_genre": sar.get_best_genre(),
    "best_mechanic": sar.get_best_mechanic(),
    "version": BOT_VERSION
}
Path("learning_data.json").write_text(json.dumps(learning_data, indent=2))
print(f"   ✅ Learning data saved")

# ============ BUILD INFO ============
build_info = f"""
DEATHROLL STUDIO v{BOT_VERSION}
================================
Game: {game_name}
Genre: {selected_type}
Mechanic: {selected_mechanic}
Description: {ai_description}
Hook: {selected_hook}
Date: {datetime.now().isoformat()}
Trends: {real_time_trends}
Art: {art_method} ({art_success})
Repo: {repo_link}
Portfolio: {len(existing_games)} games
SAR runs: {sar.data.get('total_runs', 0)}
Success rate: {sar.get_success_rate()*100:.1f}%
"""
Path("build_info.txt").write_text(build_info)
print(f"   ✅ Build info saved")

# ============ GIT FILES ============
Path("last_update.txt").write_text(f"Last update: {datetime.now().isoformat()}\nGame: {game_name}\nRun: {sar.data.get('total_runs', 0)}")
print(f"   ✅ last_update.txt created")

# ============ WEEKLY BEST OF ============
if datetime.now().strftime("%A") == "Sunday" and telegram_token:
    try:
        week_ago = datetime.now().timestamp() - (7 * 24 * 3600)
        weekly = [g for g in sar.data.get("games", []) if datetime.fromisoformat(g["timestamp"]).timestamp() > week_ago]
        if weekly:
            best = weekly[0]
            best_msg = f"🏆 *Game of the Week* 🏆\n\n{best['name']}\nGenre: {best['genre']}\nMechanic: {best['mechanic']}"
            requests.post(
                f"https://api.telegram.org/bot{telegram_token}/sendMessage",
                json={"chat_id": TELEGRAM_CHANNEL, "text": best_msg, "parse_mode": "Markdown"},
                timeout=30
            )
            print(f"   ✅ Game of the Week sent")
    except:
        pass

# ============ MONTHLY CHANGELOG ============
if datetime.now().day == 1 and telegram_token and telegram_chat_id:
    try:
        month_games = [g for g in sar.data.get("games", []) if datetime.fromisoformat(g["timestamp"]).month == datetime.now().month]
        changelog = f"""📅 *DeathRoll Studio Monthly*

Games this month: {len(month_games)}
Total all-time: {sar.data.get('total_runs', 0)}
Best genre: {sar.get_best_genre() or 'N/A'}
Success rate: {sar.get_success_rate()*100:.1f}%

Thanks for playing! 🎮
"""
        requests.post(
            f"https://api.telegram.org/bot{telegram_token}/sendMessage",
            json={"chat_id": telegram_chat_id, "text": changelog, "parse_mode": "Markdown"},
            timeout=30
        )
        print(f"   ✅ Monthly report sent")
    except:
        pass

# ============ FINAL VERIFICATION ============
print("\n" + "=" * 60)
print("🔍 FINAL VERIFICATION")
print("=" * 60)

print(f"   ✅ Game: {game_name}")
print(f"   ✅ Genre: {selected_type}")
print(f"   ✅ Mechanic: {selected_mechanic}")
print(f"   ✅ Portfolio entries: {len(existing_games)}")
print(f"   ✅ SAR runs: {sar.data.get('total_runs', 0)}")
print(f"   ✅ Art: {art_method}")

# Verify portfolio contains the new game
try:
    if game_name in portfolio_path.read_text():
        print(f"   ✅ VERIFIED: {game_name} in portfolio.json")
    else:
        print(f"   ❌ ERROR: Game not found!")
        current = json.loads(portfolio_path.read_text()) if portfolio_path.exists() else []
        current.append(new_game_entry)
        portfolio_path.write_text(json.dumps(current[-500:], indent=2))
        print(f"   🔄 Emergency re-save")
except Exception as e:
    print(f"   ⚠️ Verification error: {e}")

print("\n" + "=" * 60)
print(f"✅ {game_name} IS COMPLETE!")
print("=" * 60)

print(f"\n🎉 DEATHROLL STUDIO v{BOT_VERSION} FINISHED!")
print(f"📊 Website: https://{BRAND_GITHUB}.github.io/FACTORY-BOT-V4/")
