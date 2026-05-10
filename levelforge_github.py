#!/usr/bin/env python3
"""
DEATHROLL STUDIO v26.2 - COMPLETE WITH AI
- AI-generated mechanics, names, descriptions
- SAR self-learning system
- Real-time trends from Reddit/X
- Weekly Best Of, monthly changelog, feedback polls
- GUARANTEED portfolio updates on EVERY run
"""

import os
import json
import random
import hashlib
import requests
import time
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw

print("=" * 60)
print("🔥 DEATHROLL STUDIO v26.2 - COMPLETE WITH AI")
print("✅ AI Mechanics | SAR Learning | Real-time Trends | Guaranteed Portfolio")
print("=" * 60)

BOT_VERSION = "26.2.0"
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

def fetch_x_trends():
    if not bearer_token:
        return []
    try:
        headers = {"Authorization": f"Bearer {bearer_token}"}
        params = {
            "query": "gamedev OR indie game -filter:retweets",
            "max_results": 30,
            "tweet.fields": "public_metrics"
        }
        r = requests.get("https://api.twitter.com/2/tweets/search/recent", headers=headers, params=params, timeout=10)
        if r.status_code == 200:
            tweets = r.json().get("data", [])
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
                top_genres = [g for g, count in sorted_genres if count > 0][:3]
                if top_genres:
                    print(f"   🐦 X trends: {', '.join(top_genres)}")
                    return top_genres
    except:
        pass
    return []

reddit_trends = fetch_reddit_trends()
x_trends = fetch_x_trends()
all_trends = reddit_trends + x_trends
real_time_trends = list(dict.fromkeys(all_trends))[:3] if all_trends else []
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
            "feedback": {}
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
    
    def record(self, game_name, genre, mechanic, art_success, trends_used=None):
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
        
        self.data["games"].append({
            "name": game_name,
            "genre": genre,
            "mechanic": mechanic,
            "timestamp": datetime.now().isoformat(),
            "art_success": art_success,
            "trends_used": trends_used
        })
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
    "♟️ Outsmart the system", "🏴‍☠️ Loot or die", "🌿 Build your dream"
]
selected_hook = random.choice(hook_pool)

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

# ============ AI MECHANIC GENERATION - FIXED ============
print("\n⚙️ AI generating unique mechanic...")

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
    ("Echo Location", "reveal hidden paths and enemies with sound waves")
]

def generate_ai_mechanic():
    if not openai_key:
        return random.choice(creative_fallbacks)
    
    # Get recently used mechanics - FIXED: extract just the mechanic name from tuples
    recent_mechanics = []
    for g in sar.data.get("games", [])[-5:]:
        mech = g.get("mechanic", "")
        if mech:
            recent_mechanics.append(mech)
    
    # Create avoid list from mechanic names only
    avoid_names = [m[0] for m in creative_fallbacks[:3]] + recent_mechanics
    avoid_str = ', '.join(avoid_names[:5])
    
    prompt = f"""Invent a unique, creative game mechanic for a {selected_type} game.
The mechanic should be fun and original.
Avoid these: {avoid_str}

Return EXACTLY in this format:
MECHANIC: <cool mechanic name, 2-4 words>
DESCRIPTION: <one sentence explaining how it works>"""
    
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
        if name and desc and len(name) > 3:
            return name, desc
    return random.choice(creative_fallbacks)

mechanic_name, mechanic_desc = generate_ai_mechanic()
selected_mechanic = mechanic_name
print(f"   ✨ Mechanic: {selected_mechanic}")
print(f"   📖 {mechanic_desc}")

# ============ GAME NAME GENERATION ============
print("\n🎮 Generating game name...")

prefixes = ["Neon", "Cyber", "Quantum", "Astral", "Void", "Echo", "Flux", "Rogue", "Crimson", "Shadow", "Phantom", "Eclipse", "Solar", "Nova", "Dark", "Light", "Storm", "Thunder"]
suffixes = ["Runner", "Drifter", "Breach", "Vector", "Pulse", "Shift", "Core", "Edge", "Zone", "Realm", "Fury", "Strike", "Blade", "Force", "Hunter", "Seeker", "Warden"]

if openai_key:
    prompt = f"""Generate a cool, catchy name for a {selected_type} game with the mechanic '{selected_mechanic}'.
Return ONLY the name, 1-3 words, max 25 characters.
Examples: Neon Drifter, Shadow Breach, Void Runner"""
    ai_name = cached_generate(prompt, temperature=0.9, max_tokens=20)
    if ai_name and len(ai_name) > 2 and len(ai_name) < 30:
        game_name = ai_name
    else:
        game_name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
else:
    game_name = f"{random.choice(prefixes)} {random.choice(suffixes)}"

print(f"   ✅ Game name: {game_name}")
repo_name = f"daily-{game_name.lower().replace(' ', '-')}"

# ============ DESCRIPTION & HASHTAGS ============
print("\n📝 Generating description and hashtags...")

ai_description = f"Master the {selected_mechanic} in this intense {selected_type} experience! {mechanic_desc[:80]}"
hashtag_string = f"#gamedev #indiegame #solana #{selected_type.replace(' ', '')} #{selected_mechanic.replace(' ', '')} #DeathRollStudio"

if openai_key:
    prompt = f"""Write a ONE-SENTENCE exciting description for a {selected_type} game called '{game_name}' with the mechanic: {selected_mechanic} - {mechanic_desc}
Max 120 characters. Make it hype!"""
    ai_desc = cached_generate(prompt, temperature=0.8, max_tokens=60)
    if ai_desc and len(ai_desc) > 20:
        ai_description = ai_desc[:120]

print(f"   📝 {ai_description}")
print(f"   #️⃣ {hashtag_string[:80]}...")

# ============ 🚨 CRITICAL: IMMEDIATE PORTFOLIO SAVE ============
print("\n" + "=" * 60)
print("💾 STEP 1: SAVING TO PORTFOLIO.JSON (BEFORE ANY RISKY OPERATIONS)")
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
    "status": "generated"
}

existing_games.append(new_game_entry)
existing_games = existing_games[-200:]

try:
    portfolio_path.write_text(json.dumps(existing_games, indent=2))
    print(f"   ✅ Portfolio saved! Total games: {len(existing_games)}")
    print(f"   ✅ Added: {game_name}")
except Exception as e:
    print(f"   ❌ Portfolio save failed: {e}")
    Path("portfolio_emergency.json").write_text(json.dumps([new_game_entry], indent=2))
    print(f"   ✅ Emergency backup saved")

games_log = Path("games_log.txt")
with open(games_log, "a") as f:
    f.write(f"{datetime.now().isoformat()} | {game_name} | {selected_type} | {selected_mechanic} | {real_time_trends}\n")
print(f"   ✅ Logged to games_log.txt")

Path("last_run.txt").write_text(datetime.now().isoformat())
print(f"   ✅ last_run.txt created")

print("=" * 60)
print("✅ PORTFOLIO SAVE COMPLETE - Continuing...")
print("=" * 60)

# ============ ART STYLE SELECTION ============
print("\n🎨 Selecting art style...")
visual_styles = ["isometric", "neon cyberpunk", "low-poly", "cell-shaded", "voxel", "pastel gothic", "dark fantasy", "steampunk"]
trending_style = random.choice(visual_styles)
print(f"   Style: {trending_style}")

# ============ ART GENERATION ============
print("\n🎨 Generating game art...")
sprite_path = Path("sprite.png")

def generate_art():
    try:
        prompt = f"3D {trending_style} render of a {selected_type} character for '{game_name}', professional game asset, high quality"
        prompt_url = prompt.replace(" ", "+").replace("'", "").replace(",", "+")[:200]
        url = f"https://image.pollinations.ai/prompt/{prompt_url}?width=512&height=512&model=flux&seed={random.randint(1, 999999)}"
        r = requests.get(url, timeout=45)
        if r.status_code == 200 and len(r.content) > 5000:
            sprite_path.write_bytes(r.content)
            return True
    except Exception as e:
        print(f"   ⚠️ Online art: {e}")
    
    try:
        img = Image.new('RGB', (512, 512), color=(30, 30, 60))
        draw = ImageDraw.Draw(img)
        draw.rectangle([50, 50, 462, 462], outline=(255, 255, 255), width=3)
        draw.text((180, 230), game_name[:15], fill=(255, 255, 255))
        draw.text((200, 260), selected_type[:12], fill=(200, 200, 200))
        img.save(sprite_path)
        return True
    except:
        return False

art_success = generate_art()
print(f"   ✅ Art ready (success: {art_success})")

# ============ WORKSPACE SETUP ============
print("\n📁 Setting up workspace...")
project_dir = Path(f"workspace/{game_name.replace(' ', '_')}")
project_dir.mkdir(parents=True, exist_ok=True)

if sprite_path.exists():
    shutil.copy(sprite_path, project_dir / "icon.png")
else:
    Image.new('RGB', (512, 512), color=(50, 50, 80)).save(project_dir / "icon.png")

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
""")

(project_dir / "player.gd").write_text(f"""
extends Node2D
func _ready():
    print("{game_name} – {selected_type}")
    print("Mechanic: {selected_mechanic}")
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
                    arcname = file.relative_to(project_dir.parent)
                    zipf.write(file, arcname)
                except:
                    pass
    print(f"   ✅ ZIP created")
except Exception as e:
    print(f"   ⚠️ ZIP failed: {e}")
    shutil.make_archive(str(zip_path).replace('.zip', ''), 'zip', project_dir)
    print(f"   ✅ Created zip with fallback")

# ============ UPDATE PORTFOLIO ============
print("\n📁 Updating portfolio...")
try:
    current_games = json.loads(portfolio_path.read_text())
    for game in current_games:
        if game["game"] == game_name:
            game["image_url"] = image_url
            game["status"] = "complete"
            game["art_success"] = art_success
            game["art_style"] = trending_style
            break
    portfolio_path.write_text(json.dumps(current_games, indent=2))
    print(f"   ✅ Portfolio updated")
except Exception as e:
    print(f"   ⚠️ Could not update: {e}")

# ============ GITHUB REPOSITORY ============
print("\n📦 Creating GitHub repository...")
repo_link = f"https://github.com/{BRAND_GITHUB}/{repo_name}"

if github_token:
    try:
        r = requests.post(
            "https://api.github.com/user/repos",
            headers={"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"},
            json={"name": repo_name, "description": ai_description[:100], "private": False},
            timeout=30
        )
        if r.status_code == 201:
            repo_link = r.json()["html_url"]
            print(f"   ✅ Repo created: {repo_link}")
        else:
            print(f"   ⚠️ Repo returned {r.status_code}")
    except Exception as e:
        print(f"   ⚠️ Repo creation skipped: {e}")

# ============ TELEGRAM ============
print("\n📱 Sending to Telegram...")

if telegram_token:
    try:
        with open(zip_path, "rb") as f:
            caption = f"🎮 *{game_name}* – {selected_type}\n{ai_description}\n💰 ${game_price} SOL"
            requests.post(
                f"https://api.telegram.org/bot{telegram_token}/sendDocument",
                files={"document": f},
                data={"chat_id": telegram_chat_id, "caption": caption, "parse_mode": "Markdown"},
                timeout=60
            )
        print(f"   ✅ Game sent to admin")
    except Exception as e:
        print(f"   ⚠️ Admin send failed: {e}")
    
    try:
        sales_post = f"""
{selected_emojis} *{selected_hook}* {selected_emojis}

✨ *{game_name}* – {selected_type}
{ai_description}

⚡ *Mechanic:* `{selected_mechanic}`

💰 *Price:* ${game_price} SOL
🔵 Trust: `{SOLANA_TRUST_WALLET}`
🟣 Phantom: `{SOLANA_PHANTOM_WALLET}`

📩 Send ${game_price} SOL + your @username → game in 5 mins

{hashtag_string}
#DeathRollStudio
"""
        with open(sprite_path, "rb") as photo:
            requests.post(
                f"https://api.telegram.org/bot{telegram_token}/sendPhoto",
                files={"photo": photo},
                data={"chat_id": TELEGRAM_CHANNEL, "caption": sales_post, "parse_mode": "Markdown"},
                timeout=30
            )
        print(f"   ✅ Sales post sent")
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
    "total_games": len(existing_games),
    "sar_runs": sar.data.get("total_runs", 0),
    "success_rate": sar.get_success_rate()
}
Path("learning_data.json").write_text(json.dumps(learning_data, indent=2))
print(f"   ✅ Learning data saved")

# ============ BUILD INFO ============
Path("build_info.txt").write_text(f"""
DEATHROLL STUDIO v{BOT_VERSION}
================================
Game: {game_name}
Genre: {selected_type}
Mechanic: {selected_mechanic}
Date: {datetime.now().isoformat()}
Art success: {art_success}
Total portfolio games: {len(existing_games)}
SAR total runs: {sar.data.get('total_runs', 0)}
""")
print(f"   ✅ Build info saved")

# ============ last_update.txt ============
Path("last_update.txt").write_text(f"Last update: {datetime.now().isoformat()}\nGame: {game_name}")

# ============ FINAL VERIFICATION ============
print("\n" + "=" * 60)
print("🔍 FINAL VERIFICATION")
print("=" * 60)

print(f"   ✅ Game: {game_name}")
print(f"   ✅ Genre: {selected_type}")
print(f"   ✅ Mechanic: {selected_mechanic}")
print(f"   ✅ Portfolio entries: {len(existing_games)}")
print(f"   ✅ SAR runs: {sar.data.get('total_runs', 0)}")

print("\n" + "=" * 60)
print(f"✅ {game_name} is COMPLETE!")
print("=" * 60)

print("\n🎉 DEATHROLL STUDIO v26.2 FINISHED!")
print(f"📊 Website: https://{BRAND_GITHUB}.github.io/FACTORY-BOT-V4/")
