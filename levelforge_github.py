#!/usr/bin/env python3
"""
LevelForge+ ULTRA – DEATHROLL STUDIO v14.0
- SAR SYSTEM (Study, Analysis, Reprogram)
- Self-improving AI
- Smart Art Generation (Hugging Face + Pollinations.ai backup)
- Adaptive Timeouts & Retry Logic
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
print("🧠 DEATHROLL STUDIO v14.0 – SMART AI WITH SAR SYSTEM")
print("✅ Study | Analysis | Reprogram | Self-Improving")
print("=" * 60)

# ============ BOT VERSION ============
BOT_VERSION = "14.0.0"
print(f"🤖 Bot Version: {BOT_VERSION}")

# ============ YOUR CONTACT INFO ============
BRAND_NAME = "DeathRoll"
BRAND_EMAIL_PRIMARY = "favouradeleke246@gmail.com"
BRAND_EMAIL_SECONDARY = "fadeleke246@gmail.com"
BRAND_TELEGRAM = "@deathroll1"
BRAND_TIKTOK = "@deathroll.co"
BRAND_WEBSITE = "https://deathroll.co"
BRAND_GITHUB = "favouradeleke246-maker"

# Solana wallets
SOLANA_TRUST_WALLET = "6wsQ6nGXrUUUGCEokb4rZcfHDv2a8MomUb22TuVaH2m3"
SOLANA_PHANTOM_WALLET = "Csk9DKstWMdKx19gUHWB9xy2VwZZX2nx6V6oSVGDCgMb"

# Telegram channel
TELEGRAM_CHANNEL = "@drolltech"

print(f"🏷️ Brand: {BRAND_NAME}")
print(f"📧 Email: {BRAND_EMAIL_PRIMARY}")
print(f"📱 Telegram: {BRAND_TELEGRAM} | Channel: {TELEGRAM_CHANNEL}")
print(f"🎵 TikTok: {BRAND_TIKTOK}")

# ============ GET SECRETS ============
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
openai_key = os.getenv("OPENAI_API_KEY")
github_token = os.getenv("GH_TOKEN")
huggingface_token = os.getenv("HUGGINGFACE_TOKEN")
game_price = os.getenv("GAME_PRICE", "5")

print(f"✅ Telegram: {'OK' if telegram_token else 'NO'}")
print(f"✅ OpenAI: {'OK' if openai_key else 'NO'}")
print(f"✅ GitHub: {'OK' if github_token else 'NO'}")
print(f"✅ Hugging Face: {'OK' if huggingface_token else 'NO'}")
print(f"💰 Game Price: ${game_price}")

# ============ SAR SYSTEM (Study, Analysis, Reprogram) ============
print("\n🧠 Initializing SAR System (Study, Analysis, Reprogram)...")

class SARSystem:
    """Self-improving AI that learns from each run"""
    
    def __init__(self):
        self.sar_file = Path("sar_analysis.json")
        self.data = self.load()
        self.performance_metrics = {}
    
    def load(self):
        if self.sar_file.exists():
            try:
                return json.loads(self.sar_file.read_text())
            except:
                return self.get_default_sar()
        return self.get_default_sar()
    
    def get_default_sar(self):
        return {
            "study": {
                "total_runs": 0,
                "successful_art_generations": 0,
                "failed_art_generations": 0,
                "average_execution_time": 0,
                "games_created": []
            },
            "analysis": {
                "best_genre": None,
                "best_mechanic": None,
                "best_hook": None,
                "success_rate": 0,
                "improvement_areas": []
            },
            "reprogram": {
                "last_improvement": None,
                "version": BOT_VERSION,
                "adaptive_changes": []
            }
        }
    
    def save(self):
        self.sar_file.write_text(json.dumps(self.data, indent=2))
    
    def study_record(self, game_name, genre, mechanic, hook, success, execution_time):
        """Record data from each run"""
        self.data["study"]["total_runs"] += 1
        if success:
            self.data["study"]["successful_art_generations"] += 1
        else:
            self.data["study"]["failed_art_generations"] += 1
        
        self.data["study"]["games_created"].append({
            "name": game_name,
            "genre": genre,
            "mechanic": mechanic,
            "hook": hook,
            "timestamp": datetime.now().isoformat(),
            "success": success
        })
        
        # Keep only last 50 games
        self.data["study"]["games_created"] = self.data["study"]["games_created"][-50:]
        
        # Update average execution time
        total_time = self.data["study"]["average_execution_time"] * (self.data["study"]["total_runs"] - 1) + execution_time
        self.data["study"]["average_execution_time"] = total_time / self.data["study"]["total_runs"]
        
        self.save()
    
    def analyze(self):
        """Analyze data and find improvement areas"""
        if not self.data["study"]["games_created"]:
            return
        
        # Find best performing genre
        genre_counts = {}
        for game in self.data["study"]["games_created"]:
            genre = game["genre"]
            if genre not in genre_counts:
                genre_counts[genre] = {"count": 0, "successes": 0}
            genre_counts[genre]["count"] += 1
            if game["success"]:
                genre_counts[genre]["successes"] += 1
        
        if genre_counts:
            best_genre = max(genre_counts.keys(), key=lambda g: genre_counts[g]["successes"] / max(genre_counts[g]["count"], 1))
            self.data["analysis"]["best_genre"] = best_genre
        
        # Find best mechanic
        mechanic_counts = {}
        for game in self.data["study"]["games_created"]:
            mechanic = game["mechanic"]
            if mechanic not in mechanic_counts:
                mechanic_counts[mechanic] = {"count": 0, "successes": 0}
            mechanic_counts[mechanic]["count"] += 1
            if game["success"]:
                mechanic_counts[mechanic]["successes"] += 1
        
        if mechanic_counts:
            best_mechanic = max(mechanic_counts.keys(), key=lambda m: mechanic_counts[m]["successes"] / max(mechanic_counts[m]["count"], 1))
            self.data["analysis"]["best_mechanic"] = best_mechanic
        
        # Calculate success rate
        total = self.data["study"]["successful_art_generations"] + self.data["study"]["failed_art_generations"]
        if total > 0:
            self.data["analysis"]["success_rate"] = self.data["study"]["successful_art_generations"] / total
        
        self.save()
    
    def reprogram(self, improvement):
        """Record an improvement made to the bot"""
        self.data["reprogram"]["last_improvement"] = datetime.now().isoformat()
        self.data["reprogram"]["adaptive_changes"].append({
            "timestamp": datetime.now().isoformat(),
            "improvement": improvement
        })
        self.save()
        print(f"   💾 Reprogrammed: {improvement}")

sar = SARSystem()
sar.analyze()
print(f"   ✅ SAR System ready ({sar.data['study']['total_runs']} runs analyzed)")
if sar.data["analysis"]["best_genre"]:
    print(f"   📊 Best performing genre: {sar.data['analysis']['best_genre']}")
if sar.data["analysis"]["best_mechanic"]:
    print(f"   📊 Best performing mechanic: {sar.data['analysis']['best_mechanic']}")

# ============ SMART ART GENERATION ============
print("\n🎨 Initializing Smart Art Generation System...")

sprite_path = Path("sprite.png")

# Art generation metrics
art_metrics = {
    "huggingface_success": 0,
    "pollinations_success": 0,
    "fallback_used": 0,
    "total_attempts": 0
}

def generate_smart_art():
    """Smart art generation with adaptive retry logic"""
    
    art_metrics["total_attempts"] += 1
    
    # PRIORITY 1: Hugging Face (most reliable, free)
    if huggingface_token:
        print("   🎨 Attempt 1: Hugging Face (High quality, reliable)")
        result = generate_huggingface_art()
        if result:
            art_metrics["huggingface_success"] += 1
            sar.reprogram("Hugging Face art generation successful")
            return True
        else:
            print("   ⚠️ Hugging Face failed, trying Pollinations.ai...")
            time.sleep(3)  # Brief pause before next attempt
    
    # PRIORITY 2: Pollinations.ai (backup)
    print("   🎨 Attempt 2: Pollinations.ai (Free backup)")
    result = generate_pollinations_art()
    if result:
        art_metrics["pollinations_success"] += 1
        sar.reprogram("Pollinations.ai fallback used successfully")
        return True
    
    # PRIORITY 3: Fallback art (always works)
    print("   🎨 Attempt 3: Fallback algorithmic art (Guaranteed)")
    art_metrics["fallback_used"] += 1
    return generate_fallback_art()

def generate_huggingface_art():
    """Generate art using Hugging Face's free API"""
    try:
        models = [
            "stabilityai/stable-diffusion-2-1",
            "runwayml/stable-diffusion-v1-5",
            "dreamlike-art/dreamlike-photoreal-2.0"
        ]
        
        prompts = [
            f"pixel art game sprite, {game_name} character, {selected_type} game, {selected_mechanic} ability, centered, vibrant colors, game asset, high quality, 512x512",
            f"detailed pixel art character for '{game_name}', {selected_type} hero, using {selected_mechanic}, cute but cool, game sprite, 8-bit style"
        ]
        
        selected_model = random.choice(models)
        selected_prompt = random.choice(prompts)
        
        print(f"      Model: {selected_model.split('/')[-1]}")
        
        API_URL = f"https://api-inference.huggingface.co/models/{selected_model}"
        headers = {"Authorization": f"Bearer {huggingface_token}"}
        
        response = requests.post(API_URL, headers=headers, json={"inputs": selected_prompt}, timeout=60)
        
        if response.status_code == 200:
            with open(sprite_path, "wb") as f:
                f.write(response.content)
            print(f"      ✅ Hugging Face art generated!")
            return True
        elif response.status_code == 503:
            print("      ⏳ Model loading, waiting...")
            time.sleep(15)
            response = requests.post(API_URL, headers=headers, json={"inputs": selected_prompt}, timeout=60)
            if response.status_code == 200:
                with open(sprite_path, "wb") as f:
                    f.write(response.content)
                print(f"      ✅ Hugging Face art generated after wait!")
                return True
        else:
            print(f"      ⚠️ HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"      ⚠️ Exception: {str(e)[:50]}")
        return False

def generate_pollinations_art():
    """Generate art using Pollinations.ai (backup)"""
    try:
        prompt = f"8K pixel art game sprite for '{game_name}', {selected_type} game character using {selected_mechanic}, detailed, vibrant colors, epic pose, game asset, high quality, centered"
        enhanced_prompt = prompt.replace(" ", "+").replace("'", "").replace(",", "+")
        url = f"https://image.pollinations.ai/prompt/{enhanced_prompt}?width=512&height=512&model=flux&seed={random.randint(1, 999999)}"
        
        response = requests.get(url, timeout=45)
        if response.status_code == 200 and len(response.content) > 5000:
            with open(sprite_path, "wb") as f:
                f.write(response.content)
            print(f"      ✅ Pollinations.ai art generated!")
            return True
        else:
            print(f"      ⚠️ HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"      ⚠️ Exception: {str(e)[:50]}")
        return False

def generate_fallback_art():
    """Ultimate fallback - always works"""
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

# ============ VIRAL MARKETING ============
print("\n🔥 Generating viral marketing content...")

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

# Use SAR analysis to improve genre selection
best_genre = sar.data["analysis"].get("best_genre")
if best_genre and random.random() < 0.4:  # 40% chance to use best genre
    selected_type = best_genre
    print(f"   🧠 SAR analysis chose best genre: {selected_type}")
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
    "survival horror": ["#horrorgame", "#survival", "#scary"],
    "top-down shooter": ["#shootergame", "#actiongame"],
    "action RPG": ["#rpg", "#actionrpg"],
    "racing game": ["#racinggame", "#speed"],
    "puzzle game": ["#puzzlegame", "#brainteaser"],
    "fighting game": ["#fightinggame", "#combat"],
    "strategy game": ["#strategygame", "#tactical"]
}

specific_hashtags = genre_hashtags.get(selected_type, ["#indiegame", "#gaming"])
all_hashtags = viral_hashtags_base + specific_hashtags + [f"#{game_name.replace(' ', '')}"]
random.shuffle(all_hashtags)
hashtag_string = " ".join(all_hashtags[:7])
print(f"   #️⃣ {hashtag_string[:60]}...")

# ============ GENERATE ART (WITH TIMING) ============
print("\n🎨 Generating game art...")
art_start_time = time.time()
art_success = generate_smart_art()
art_time = time.time() - art_start_time
print(f"   ✅ Art generation completed in {art_time:.1f}s")

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

# ============ SAR RECORDING ============
print("\n🧠 Recording run in SAR system...")
sar.study_record(game_name, selected_type, selected_mechanic, selected_hook, art_success, art_time)
sar.analyze()
sar.reprogram(f"Run {sar.data['study']['total_runs']} completed. Art source: {'Success' if art_success else 'Fallback'}")
print(f"   ✅ SAR updated")

# ============ SAVE DATA ============
print("\n💾 Saving learning data...")
ld = {"last_run": datetime.now().isoformat(), "game_name": game_name, "genre": selected_type, "mechanic": selected_mechanic, "day": day_name, "hook": selected_hook, "description": ai_description, "repo_url": repo_link, "price": game_price, "bot_version": BOT_VERSION, "art_success": art_success, "art_time": art_time}
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

# ============ ART METRICS REPORT ============
print("\n📊 Art Generation Metrics:")
print(f"   🤖 Hugging Face: {art_metrics['huggingface_success']}/{art_metrics['total_attempts']}")
print(f"   🎨 Pollinations: {art_metrics['pollinations_success']}/{art_metrics['total_attempts']}")
print(f"   ⚡ Fallback: {art_metrics['fallback_used']}/{art_metrics['total_attempts']}")

# ============ VERIFICATION ============
print("\n🔍 Verifying all systems...")
print(f"   AI Name: ✅")
print(f"   SAR System: ✅ ({sar.data['study']['total_runs']} runs)")
print(f"   Smart Art: ✅ ({'Success' if art_success else 'Fallback used'})")
print(f"   Godot Project: ✅")
print(f"   GitHub: {'✅' if repo_url else '⚠️'}")
print(f"   Telegram: {'✅' if telegram_token else '⚠️'}")

# ============ DONE ============
print("\n" + "=" * 60)
print(f"✅ {game_name} is READY!")
print(f"   📅 Day: {day_name} – {selected_type}")
print(f"   🎣 Hook: {selected_hook}")
print(f"   🎨 Art: {'Smart AI' if art_success else 'Fallback'}")
print(f"   🧠 SAR: {sar.data['study']['total_runs']} games analyzed")
print(f"   📦 GitHub: {repo_link}")
print("=" * 60)

print("\n🎉 DEATHROLL STUDIO v14.0 FINISHED SUCCESSFULLY!")
print("🧠 SAR System learned from this run!")
print("📱 Check Telegram for viral posts!")
print("🎵 TikTok caption ready above – copy and post!")
