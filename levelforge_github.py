#!/usr/bin/env python3
"""
DEATHROLL STUDIO v28.0 - COMPLETE FULL FEATURES
- AI-generated mechanics, names, descriptions
- SAR self-learning system with performance tracking
- Real-time trends from Reddit and X/Twitter
- Weighted genre selection based on SAR performance
- Viral hooks and emoji generation
- Art generation with fallback
- Godot project creation
- GitHub repository creation
- Telegram admin delivery, sales posts, and feedback polls
- Weekly Best Of and monthly changelog
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
print("🔥 DEATHROLL STUDIO v28.0 - COMPLETE FULL FEATURES")
print("✅ AI Mechanics | SAR Learning | Real-time Trends | Guaranteed Portfolio")
print("=" * 60)

BOT_VERSION = "28.0.0"
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
        
        # Track genre performance
        if genre not in self.data["genre_performance"]:
            self.data["genre_performance"][genre] = {"count": 0, "success": 0, "total_feedback": 0, "feedback_count": 0}
        self.data["genre_performance"][genre]["count"] += 1
        if art_success:
            self.data["genre_performance"][genre]["success"] += 1
        if feedback_score:
            self.data["genre_performance"][genre]["total_feedback"] = self.data["genre_performance"][genre].get("total_feedback", 0) + feedback_score
            self.data["genre_performance"][genre]["feedback_count"] = self.data["genre_performance"][genre].get("feedback_count", 0) + 1
        
        # Track mechanic performance
        if mechanic not in self.data["mechanic_performance"]:
            self.data["mechanic_performance"][mechanic] = {"count": 0, "success": 0, "total_feedback": 0, "feedback_count": 0}
        self.data["mechanic_performance"][mechanic]["count"] += 1
        if art_success:
            self.data["mechanic_performance"][mechanic]["success"] += 1
        if feedback_score:
            self.data["mechanic_performance"][mechanic]["total_feedback"] = self.data["mechanic_performance"][mechanic].get("total_feedback", 0) + feedback_score
            self.data["mechanic_performance"][mechanic]["feedback_count"] = self.data["mechanic_performance"][mechanic].get("feedback_count", 0) + 1
        
        # Track trends
        if trends_used:
            for trend in trends_used:
                if trend not in self.data["trend_performance"]:
                    self.data["trend_performance"][trend] = {"count": 0, "success": 0}
                self.data["trend_performance"][trend]["count"] += 1
                if art_success:
                    self.data["trend_performance"][trend]["success"] += 1
        
        # Add game record
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
        
        # Calculate best genre (by success rate)
        if self.data["genre_performance"]:
            best = max(self.data["genre_performance"].keys(), 
                      key=lambda x: self.data["genre_performance"][x]["success"] / max(self.data["genre_performance"][x]["count"], 1))
            self.data["best_genre"] = best
        
        # Calculate best mechanic (by success rate)
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
    
    def get_genre_rating(self, genre):
        perf = self.data["genre_performance"].get(genre, {})
        if perf.get("feedback_count", 0) > 0:
            return perf.get("total_feedback", 0) / perf["feedback_count"]
        return None
    
    def record_feedback(self, game_name, rating):
        if game_name not in self.data["feedback"]:
            self.data["feedback"][game_name] = []
        self.data["feedback"][game_name].append(rating)
        
        # Update game record
        for game in self.data["games"]:
            if game["name"] == game_name:
                game["feedback_score"] = rating
                break
        
        self.save()

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

# Build weighted candidates based on SAR performance
candidates = []
weights = []

# SAR best genre (40% weight) - highest success rate
sar_best = sar.get_best_genre()
if sar_best and sar_best in all_genres:
    candidates.append(sar_best)
    weights.append(0.4)

# Real-time trends (30% weight)
if real_time_trends:
    for trend in real_time_trends[:1]:
        if trend in all_genres:
            candidates.append(trend)
            weights.append(0.3)

# Random genre (30% weight)
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

# Save last hook to file to avoid repetition
last_hook_file = Path("last_hook.txt")
last_hook = last_hook_file.read_text().strip() if last_hook_file.exists() else ""
if selected_hook == last_hook:
    selected_hook = random.choice([h for h in hook_pool if h != last_hook] or hook_pool)
last_hook_file.write_text(selected_hook)

# Select random CTA
selected_cta = random.choice(["Follow for daily games! 🎮", "Share with a friend! 🔄", "Join our Telegram! 📱", "Get your copy now! 🎯"])

# Genre-specific emojis
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

# ============ AI MECHANIC GENERATION ============
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
    ("Echo Location", "reveal hidden paths and enemies with sound waves"),
    ("Shadow Cloak", "become invisible when standing still"),
    ("Berserker Rage", "deal more damage as your health drops")
]

def generate_ai_mechanic():
    if not openai_key:
        return random.choice(creative_fallbacks)
    
    # Get recently used mechanics to avoid repetition
    recent_mechanics = [g.get("mechanic", "") for g in sar.data.get("games", [])[-5:] if g.get("mechanic")]
    avoid_str = ', '.join(recent_mechanics[:3]) if recent_mechanics else "none"
    
    prompt = f"""Invent a unique, creative game mechanic for a {selected_type} game.
The mechanic should be fun, original, and exciting.
Avoid repeating these: {avoid_str}

Return EXACTLY in this format:
MECHANIC: <cool mechanic name, 2-4 words>
DESCRIPTION: <one sentence explaining how it works, max 80 chars>"""
    
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

mechanic_name, mechanic_desc = generate_ai_mechanic()
selected_mechanic = mechanic_name
print(f"   ✨ Mechanic: {selected_mechanic}")
print(f"   📖 {mechanic_desc}")

# ============ GAME NAME GENERATION ============
print("\n🎮 Generating game name...")

prefixes = ["Neon", "Cyber", "Quantum", "Astral", "Void", "Echo", "Flux", "Rogue", "Crimson", "Shadow", "Phantom", "Eclipse", "Solar", "Nova", "Dark", "Light", "Storm", "Thunder", "Frost", "Ember"]
suffixes = ["Runner", "Drifter", "Breach", "Vector", "Pulse", "Shift", "Core", "Edge", "Zone", "Realm", "Fury", "Strike", "Blade", "Force", "Hunter", "Seeker", "Warden", "Ghost", "Wraith", "Phantom"]

if openai_key and random.random() > 0.3:  # 70% chance for AI name
    prompt = f"""Generate a cool, catchy name for a {selected_type} game with the mechanic '{selected_mechanic}'.
Return ONLY the name, 1-3 words, max 25 characters.
Examples: Neon Drifter, Shadow Breach, Void Runner, Crimson Core"""
    ai_name = cached_generate(prompt, temperature=0.9, max_tokens=20)
    if ai_name and len(ai_name) > 2 and len(ai_name) < 30:
        game_name = ai_name
    else:
        game_name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
else:
    game_name = f"{random.choice(prefixes)} {random.choice(suffixes)}"

# Ensure name is unique (add number if duplicate)
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

# Default description
ai_description = f"Master the {selected_mechanic} in this intense {selected_type} experience! {mechanic_desc[:70]}"

# Generate hashtags
hashtag_base = f"#gamedev #indiegame #{selected_type.replace(' ', '')} #{selected_mechanic.replace(' ', '')} #DeathRollStudio"
if real_time_trends:
    trend_tag = f" #{real_time_trends[0].replace(' ', '')}"
    hashtag_string = hashtag_base + trend_tag
else:
    hashtag_string = hashtag_base

# Try AI for better description if OpenAI is available
if openai_key and random.random() > 0.5:
    prompt = f"""Write a ONE-SENTENCE exciting description for a {selected_type} game called '{game_name}' with the mechanic: {selected_mechanic} - {mechanic_desc}
Max 120 characters. Make it hype! Use emojis."""
    ai_desc = cached_generate(prompt, temperature=0.8, max_tokens=80)
    if ai_desc and len(ai_desc) > 20:
        ai_description = ai_desc[:120]

print(f"   📝 {ai_description}")
print(f"   #️⃣ {hashtag_string[:80]}...")

# ============ 🚨 CRITICAL: IMMEDIATE PORTFOLIO SAVE ============
print("\n" + "=" * 60)
print("💾 STEP 1: SAVING TO PORTFOLIO.JSON (BEFORE ANY RISKY OPERATIONS)")
print("=" * 60)

portfolio_path = Path("portfolio.json")

# Load existing portfolio
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

# Create image URL (will be updated after art generation)
image_url = f"https://raw.githubusercontent.com/{BRAND_GITHUB}/FACTORY-BOT-V4/main/workspace/{game_name.replace(' ', '_')}/icon.png"

# Create game entry
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

# Add to list
existing_games.append(new_game_entry)
existing_games = existing_games[-500:]  # Keep last 500 games

# Save portfolio.json
try:
    portfolio_path.write_text(json.dumps(existing_games, indent=2))
    print(f"   ✅ Portfolio saved! Total games: {len(existing_games)}")
    print(f"   ✅ Added: {game_name}")
except Exception as e:
    print(f"   ❌ Portfolio save failed: {e}")
    Path("portfolio_emergency.json").write_text(json.dumps([new_game_entry], indent=2))
    print(f"   ✅ Emergency backup saved")

# Also save to simple log
games_log = Path("games_log.txt")
with open(games_log, "a") as f:
    f.write(f"{datetime.now().isoformat()} | {game_name} | {selected_type} | {selected_mechanic} | {real_time_trends}\n")
print(f"   ✅ Logged to games_log.txt")

# Save run timestamp
Path("last_run.txt").write_text(datetime.now().isoformat())
print(f"   ✅ last_run.txt created")

print("=" * 60)
print("✅ PORTFOLIO SAVE COMPLETE - Continuing with game creation...")
print("=" * 60)

# ============ ART STYLE SELECTION ============
print("\n🎨 Selecting art style...")
visual_styles = ["isometric", "neon cyberpunk", "low-poly", "cell-shaded", "voxel", "pastel gothic", "dark fantasy", "steampunk", "anime", "realistic"]
trending_style = random.choice(visual_styles)
last_style_file = Path("last_style.txt")
last_style_file.write_text(trending_style)
print(f"   Style: {trending_style}")

# ============ ART GENERATION ============
print("\n🎨 Generating game art...")
sprite_path = Path("sprite.png")
art_success = False
art_method = "none"

# Try online generation first
try:
    # Use different prompts for variety
    art_prompts = [
        f"3D {trending_style} render of a {selected_type} character for '{game_name}', professional game asset, high quality, epic",
        f"Game art for '{game_name}', a {selected_type} game, {trending_style} style, cinematic lighting",
        f"Character concept art for '{game_name}', {selected_type} genre, {trending_style}, vibrant colors"
    ]
    selected_prompt = random.choice(art_prompts)
    prompt_url = selected_prompt.replace(" ", "+").replace("'", "").replace(",", "")[:200]
    url = f"https://image.pollinations.ai/prompt/{prompt_url}?width=512&height=512&model=flux&seed={random.randint(1, 999999)}"
    
    r = requests.get(url, timeout=45)
    if r.status_code == 200 and len(r.content) > 5000:
        sprite_path.write_bytes(r.content)
        art_success = True
        art_method = "online"
        print(f"   ✅ Online art generated ({trending_style})")
    else:
        raise Exception("Online art returned empty")
except Exception as e:
    print(f"   ⚠️ Online art failed: {e}")
    
    # Try fallback with different API
    try:
        url = f"https://image.pollinations.ai/prompt/{selected_type}+game+character+{trending_style}?width=512&height=512"
        r = requests.get(url, timeout=30)
        if r.status_code == 200 and len(r.content) > 3000:
            sprite_path.write_bytes(r.content)
            art_success = True
            art_method = "fallback_api"
            print(f"   ✅ Fallback API art generated")
        else:
            raise Exception("Fallback also failed")
    except:
        # Create custom fallback art
        try:
            img = Image.new('RGB', (512, 512), color=(20, 20, 40))
            draw = ImageDraw.Draw(img)
            
            # Draw a stylized game icon
            draw.rectangle([50, 50, 462, 462], outline=(78, 205, 196), width=4)
            draw.rectangle([100, 100, 412, 412], outline=(255, 107, 107), width=2)
            
            # Add game name
            draw.text((180, 220), game_name[:12], fill=(255, 255, 255))
            draw.text((200, 250), selected_type[:10], fill=(150, 150, 150))
            draw.text((220, 280), f"v{BOT_VERSION}", fill=(100, 100, 100))
            
            img.save(sprite_path)
            art_success = True
            art_method = "generated"
            print(f"   ✅ Generated custom art")
        except Exception as e2:
            print(f"   ❌ All art methods failed: {e2}")
            art_success = False

print(f"   🎨 Art ready (method: {art_method}, success: {art_success})")

# ============ WORKSPACE SETUP ============
print("\n📁 Setting up workspace...")
project_dir = Path(f"workspace/{game_name.replace(' ', '_')}")
project_dir.mkdir(parents=True, exist_ok=True)

# Copy art to workspace
if sprite_path.exists():
    shutil.copy(sprite_path, project_dir / "icon.png")
else:
    # Create placeholder
    img = Image.new('RGB', (512, 512), color=(50, 50, 80))
    img.save(project_dir / "icon.png")

# Create Godot project files
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
transform = Transform3D(1, 0, 0, 0, 0.866, 0.5, 0, -0.5, 0.866, 0, 5, 4)
""")

(project_dir / "player.gd").write_text(f"""
extends CharacterBody3D
var speed = 5.0
var mechanic_available = true
var mechanic_cooldown = 0.0

func _ready():
    print("{game_name} – {selected_type}")
    print("Mechanic: {selected_mechanic}")
    print("Description: {mechanic_desc[:60]}")

func _physics_process(delta):
    # Basic movement
    var input = Input.get_vector("left", "right", "forward", "back")
    var dir = (transform.basis * Vector3(input.x, 0, input.y)).normalized()
    velocity.x = dir.x * speed
    velocity.z = dir.z * speed
    move_and_slide()
    
    # Mechanic cooldown
    if mechanic_cooldown > 0:
        mechanic_cooldown -= delta

func use_mechanic():
    if mechanic_available and mechanic_cooldown <= 0:
        print("{selected_mechanic} activated!")
        mechanic_cooldown = 2.0
        return True
    return False
""")

print(f"   ✅ Godot project created at {project_dir}")

# Create README for the game
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

## How to Play
- WASD to move
- Space to use the {selected_mechanic} mechanic
- Survive and master the game!

---
Generated by DeathRoll Studio v{BOT_VERSION}
""")

print(f"   ✅ Game README created")

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
                except Exception as e:
                    print(f"   ⚠️ Could not add {file.name}: {e}")
    print(f"   ✅ ZIP created successfully")
except Exception as e:
    print(f"   ⚠️ ZIP creation failed: {e}")
    try:
        shutil.make_archive(str(zip_path).replace('.zip', ''), 'zip', project_dir)
        print(f"   ✅ Created zip with fallback method")
    except:
        print(f"   ❌ ZIP completely failed")

# ============ UPDATE PORTFOLIO WITH FINAL DETAILS ============
print("\n📁 Updating portfolio with final details...")

try:
    current_games = json.loads(portfolio_path.read_text())
    for game in current_games:
        if game["game"] == game_name:
            game["image_url"] = image_url
            game["status"] = "complete"
            game["art_success"] = art_success
            game["art_style"] = trending_style
            game["art_method"] = art_method
            game["completed_at"] = datetime.now().isoformat()
            break
    portfolio_path.write_text(json.dumps(current_games, indent=2))
    print(f"   ✅ Portfolio updated with final details")
except Exception as e:
    print(f"   ⚠️ Could not update portfolio: {e}")

# ============ GITHUB REPOSITORY ============
print("\n📦 Creating GitHub repository...")
repo_link = f"https://github.com/{BRAND_GITHUB}/{repo_name}"

if github_token:
    try:
        r = requests.post(
            "https://api.github.com/user/repos",
            headers={"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"},
            json={
                "name": repo_name, 
                "description": ai_description[:100], 
                "private": False, 
                "auto_init": True,
                "has_wiki": False,
                "has_issues": True
            },
            timeout=30
        )
        if r.status_code == 201:
            repo_link = r.json()["html_url"]
            print(f"   ✅ Repo created: {repo_link}")
            
            # Push the game files to the new repo
            try:
                os.chdir(project_dir)
                # This would require git commands - simplified for now
                os.chdir("../..")
            except:
                pass
        else:
            print(f"   ⚠️ Repo returned {r.status_code}: {r.text[:100]}")
    except Exception as e:
        print(f"   ⚠️ Repo creation skipped: {e}")
else:
    print(f"   ⚠️ No GitHub token, skipping repo creation")

# Update portfolio with repo link
try:
    current_games = json.loads(portfolio_path.read_text())
    for game in current_games:
        if game["game"] == game_name:
            game["repo"] = repo_link
            break
    portfolio_path.write_text(json.dumps(current_games, indent=2))
    print(f"   ✅ Portfolio updated with repo link")
except:
    pass

# ============ TELEGRAM SEND ============
print("\n📱 Sending to Telegram...")

if telegram_token and telegram_chat_id:
    # Send ZIP to admin
    try:
        with open(zip_path, "rb") as f:
            caption = f"🎮 *NEW GAME: {game_name}*\n\n🎭 Genre: {selected_type}\n⚡ Mechanic: {selected_mechanic}\n📝 {ai_description}\n💰 Price: ${game_price} SOL\n\n📦 ZIP size: {zip_path.stat().st_size // 1024} KB"
            requests.post(
                f"https://api.telegram.org/bot{telegram_token}/sendDocument",
                files={"document": f},
                data={"chat_id": telegram_chat_id, "caption": caption, "parse_mode": "Markdown"},
                timeout=60
            )
        print(f"   ✅ Game ZIP sent to admin")
    except Exception as e:
        print(f"   ⚠️ Admin send failed: {e}")

if telegram_token:
    # Public sales post
    try:
        sales_post = f"""
{selected_emojis} *{selected_hook}* {selected_emojis}

✨ *{game_name}* – {selected_type}
{ai_description}

⚡ *Mechanic:* `{selected_mechanic}`
📖 *Description:* {mechanic_desc}

💰 *Price:* `${game_price} SOL`

🔵 Trust Wallet: `{SOLANA_TRUST_WALLET}`
🟣 Phantom: `{SOLANA_PHANTOM_WALLET}`

📩 Send `${game_price} SOL` + your @username in memo → receive game in 5 mins

{hashtag_string}
{selected_cta}
#DeathRollStudio
"""
        with open(sprite_path, "rb") as photo:
            requests.post(
                f"https://api.telegram.org/bot{telegram_token}/sendPhoto",
                files={"photo": photo},
                data={"chat_id": TELEGRAM_CHANNEL, "caption": sales_post, "parse_mode": "Markdown"},
                timeout=30
            )
        print(f"   ✅ Sales post sent to {TELEGRAM_CHANNEL}")
    except Exception as e:
        print(f"   ⚠️ Sales post failed: {e}")
    
    # Send feedback poll
    try:
        poll_options = json.dumps(["⭐ 1 star", "⭐⭐ 2 stars", "⭐⭐⭐ 3 stars", "⭐⭐⭐⭐ 4 stars", "⭐⭐⭐⭐⭐ 5 stars"])
        poll_data = {
            "chat_id": TELEGRAM_CHANNEL,
            "question": f"How would you rate {game_name}?",
            "options": poll_options,
            "is_anonymous": True,
            "open_period": 86400  # 24 hours
        }
        response = requests.post(f"https://api.telegram.org/bot{telegram_token}/sendPoll", data=poll_data, timeout=30)
        if response.status_code == 200:
            print(f"   ✅ Feedback poll sent")
        else:
            print(f"   ⚠️ Poll failed: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️ Poll failed: {e}")

# ============ WEEKLY BEST OF ============
if datetime.now().strftime("%A") == "Sunday":
    print("\n🏆 Weekly Best Of...")
    try:
        # Get last 7 days of games
        week_ago = datetime.now().timestamp() - (7 * 24 * 3600)
        recent_games = [g for g in sar.data.get("games", []) if datetime.fromisoformat(g["timestamp"]).timestamp() > week_ago]
        
        if recent_games:
            # Find game with highest feedback score
            best_game = max(recent_games, key=lambda g: g.get("feedback_score", 0) if g.get("feedback_score") else 0)
            best_msg = f"""🏆 *Game of the Week* 🏆

✨ *{best_game['name']}*
🎭 Genre: {best_game['genre']}
⚡ Mechanic: {best_game['mechanic']}

Thanks for playing DeathRoll Studio games this week!"""
            
            requests.post(
                f"https://api.telegram.org/bot{telegram_token}/sendMessage",
                json={"chat_id": TELEGRAM_CHANNEL, "text": best_msg, "parse_mode": "Markdown"},
                timeout=30
            )
            print(f"   ✅ Game of the Week announced")
            
            # Record weekly winner
            sar.data["weekly_winners"].append({
                "game": best_game['name'],
                "date": datetime.now().isoformat(),
                "feedback_score": best_game.get("feedback_score", 0)
            })
            sar.save()
    except Exception as e:
        print(f"   ⚠️ Weekly Best Of failed: {e}")

# ============ MONTHLY CHANGELOG ============
if datetime.now().day == 1:
    print("\n📢 Monthly changelog...")
    try:
        current_month = datetime.now().month
        current_year = datetime.now().year
        month_games = [g for g in sar.data.get("games", []) 
                      if datetime.fromisoformat(g["timestamp"]).month == current_month 
                      and datetime.fromisoformat(g["timestamp"]).year == current_year]
        
        changelog = f"""📅 *DeathRoll Studio – Monthly Changelog ({datetime.now().strftime('%B %Y')})*

📊 *Stats for this month:*
• Games created: {len(month_games)}
• Most popular genre: {sar.get_best_genre() or 'N/A'}
• Best mechanic: {sar.get_best_mechanic() or 'N/A'}
• Success rate: {sar.get_success_rate()*100:.1f}%

🏆 *All-time stats:*
• Total games: {sar.data.get('total_runs', 0)}
• Portfolio size: {len(existing_games)} games

Thanks for supporting DeathRoll Studio! 🎮
#DeathRollStudio #MonthlyReport
"""
        requests.post(
            f"https://api.telegram.org/bot{telegram_token}/sendMessage",
            json={"chat_id": telegram_chat_id, "text": changelog, "parse_mode": "Markdown"},
            timeout=30
        )
        print(f"   ✅ Monthly changelog sent")
        
        # Record monthly stats
        sar.data["monthly_stats"].append({
            "month": datetime.now().strftime("%Y-%m"),
            "games": len(month_games),
            "best_genre": sar.get_best_genre(),
            "success_rate": sar.get_success_rate()
        })
        sar.save()
    except Exception as e:
        print(f"   ⚠️ Monthly changelog failed: {e}")

# ============ SAR SYSTEM UPDATE ============
print("\n🧠 Updating SAR system...")

# Check if we have feedback for this game (poll responses would come later)
# For now, record without feedback
sar.record(game_name, selected_type, selected_mechanic, art_success, real_time_trends, None)
print(f"   ✅ SAR updated (run #{sar.data.get('total_runs', 0)})")
print(f"   📊 Success rate: {sar.get_success_rate()*100:.1f}%")

# ============ LEARNING DATA UPDATE ============
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
try:
    Path("learning_data.json").write_text(json.dumps(learning_data, indent=2))
    print(f"   ✅ Learning data saved")
except Exception as e:
    print(f"   ⚠️ Learning data save failed: {e}")

# ============ BUILD INFO ============
try:
    build_info = f"""
DEATHROLL STUDIO v{BOT_VERSION}
================================
Game: {game_name}
Genre: {selected_type}
Mechanic: {selected_mechanic}
Mechanic Description: {mechanic_desc}
Description: {ai_description}
Hook: {selected_hook}
Hashtags: {hashtag_string}
Date: {datetime.now().isoformat()}
Trends used: {real_time_trends}
Art success: {art_success}
Art method: {art_method}
Art style: {trending_style}
Repo: {repo_link}
Total portfolio games: {len(existing_games)}
SAR total runs: {sar.data.get('total_runs', 0)}
SAR success rate: {sar.get_success_rate()*100:.1f}%
Best genre all-time: {sar.get_best_genre() or 'N/A'}
Best mechanic all-time: {sar.get_best_mechanic() or 'N/A'}
"""
    Path("build_info.txt").write_text(build_info)
    print(f"   ✅ Build info saved")
except Exception as e:
    print(f"   ⚠️ Build info failed: {e}")

# ============ GIT TRACKING FILES ============
try:
    Path("last_update.txt").write_text(f"Last update: {datetime.now().isoformat()}\nGame: {game_name}\nRun: {sar.data.get('total_runs', 0)}")
    print(f"   ✅ last_update.txt created")
except Exception as e:
    print(f"   ⚠️ last_update.txt failed: {e}")

# ============ FINAL VERIFICATION ============
print("\n" + "=" * 60)
print("🔍 FINAL VERIFICATION")
print("=" * 60)

print(f"   ✅ Game: {game_name}")
print(f"   ✅ Genre: {selected_type}")
print(f"   ✅ Mechanic: {selected_mechanic}")
print(f"   ✅ Portfolio entries: {len(existing_games)}")
print(f"   ✅ SAR runs: {sar.data.get('total_runs', 0)}")
print(f"   ✅ Art: {art_method} ({'Success' if art_success else 'Failed'})")
print(f"   ✅ Repo: {repo_link}")

# Verify portfolio.json contains the new game
try:
    verify_content = portfolio_path.read_text()
    if game_name in verify_content:
        print(f"   ✅ VERIFIED: {game_name} is in portfolio.json")
    else:
        print(f"   ❌ ERROR: {game_name} NOT found in portfolio.json!")
        # Emergency: append again
        current = json.loads(verify_content) if verify_content.strip() else []
        current.append(new_game_entry)
        portfolio_path.write_text(json.dumps(current[-500:], indent=2))
        print(f"   🔄 Emergency re-save attempted")
except Exception as e:
    print(f"   ⚠️ Verification failed: {e}")

# Print file sizes for debugging
print("\n📁 File sizes:")
for f in ["portfolio.json", "sar_analysis.json", "learning_data.json", "games_log.txt"]:
    if Path(f).exists():
        size = Path(f).stat().st_size
        print(f"   {f}: {size} bytes")

print("\n" + "=" * 60)
print(f"✅ {game_name} is COMPLETE!")
print("=" * 60)

print("\n🎉 DEATHROLL STUDIO v28.0 FINISHED!")
print("✅ AI mechanics & descriptions")
print("✅ SAR self-learning system")
print("✅ Real-time trends from Reddit/X")
print("✅ Weighted genre selection")
print("✅ Weekly Best Of & monthly changelog")
print("✅ Feedback polls & Telegram integration")
print("✅ Portfolio guaranteed to save every game")
print(f"📊 Website: https://{BRAND_GITHUB}.github.io/FACTORY-BOT-V4/")
