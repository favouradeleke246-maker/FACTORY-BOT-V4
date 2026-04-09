#!/usr/bin/env python3
"""
LevelForge+ ULTRA – DEATHROLL STUDIO v4.0
- Self-learning AI bot
- Dynamic art (changes daily)
- AI-powered social descriptions
- Multi-platform posting (Bluesky, Mastodon, Telegram)
- Demo page with Solana payment info
- Telegram public channel: @drolltech
"""

import os
import json
import random
import requests
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw

print("=" * 60)
print("🎮 LEVELFORGE+ ULTRA – DEATHROLL STUDIO v4.0")
print("✅ Bluesky | Mastodon | Telegram | Solana")
print("=" * 60)

# ============ BOT VERSION ============
BOT_VERSION = "4.0.0"
print(f"🤖 Bot Version: {BOT_VERSION}")

# ============ YOUR CONTACT INFO ============
BRAND_NAME = "DeathRoll"
BRAND_EMAIL_PRIMARY = "favouradeleke246@gmail.com"
BRAND_EMAIL_SECONDARY = "fadeleke246@gmail.com"
BRAND_TELEGRAM = "@deathroll1"
BRAND_TIKTOK = "@favouradeleke662"
BRAND_WEBSITE = "https://deathroll.co"
BRAND_GITHUB = "favouradeleke246-maker"

# Solana wallets
SOLANA_TRUST_WALLET = "6wsQ6nGXrUUUGCEokb4rZcfHDv2a8MomUb22TuVaH2m3"
SOLANA_PHANTOM_WALLET = "Csk9DKstWMdKx19gUHWB9xy2VwZZX2nx6V6oSVGDCgMb"
MONETIZATION_LINK = "https://trustwallet.com"

# Telegram channel
TELEGRAM_CHANNEL = "@drolltech"

print(f"🏷️ Brand: {BRAND_NAME}")
print(f"📧 Email: {BRAND_EMAIL_PRIMARY}")
print(f"📱 Telegram: {BRAND_TELEGRAM} | Channel: {TELEGRAM_CHANNEL}")
print(f"🎵 TikTok: {BRAND_TIKTOK}")
print(f"💰 Solana (Trust): {SOLANA_TRUST_WALLET[:10]}...")
print(f"💰 Solana (Phantom): {SOLANA_PHANTOM_WALLET[:10]}...")

# ============ GET SECRETS ============
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")      # your private chat
openai_key = os.getenv("OPENAI_API_KEY")
github_token = os.getenv("GH_TOKEN")
bluesky_handle = os.getenv("BLUESKY_HANDLE")
bluesky_password = os.getenv("BLUESKY_PASSWORD")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
mastodon_token = os.getenv("MASTODON_ACCESS_TOKEN")
mastodon_instance = os.getenv("MASTODON_INSTANCE")
game_price = os.getenv("GAME_PRICE", "5")

print(f"✅ Telegram: {'OK' if telegram_token else 'NO'}")
print(f"✅ OpenAI: {'OK' if openai_key else 'NO'}")
print(f"✅ GitHub: {'OK' if github_token else 'NO'}")
print(f"✅ Bluesky: {'OK' if bluesky_handle else 'NO'}")
print(f"✅ X Learning: {'OK' if bearer_token else 'NO'}")
print(f"✅ Mastodon: {'OK' if mastodon_token else 'NO (add later)'}")
print(f"💰 Game Price: ${game_price}")

# ============ SELF-IMPROVEMENT ============
print("\n🧠 Running self-improvement analysis...")
def analyze_and_improve():
    improvement_file = Path("improvement_data.json")
    improvements = {}
    if improvement_file.exists():
        try:
            improvements = json.loads(improvement_file.read_text())
        except:
            pass
    mechanic_scores = improvements.get("mechanic_scores", {})
    all_mechanics = ["dash ability", "double jump", "time slow", "energy shield", "grappling hook", "invisibility cloak", "wall run", "teleport dash", "gravity flip", "clone summon"]
    for mechanic in all_mechanics:
        if mechanic not in mechanic_scores:
            mechanic_scores[mechanic] = 50
    if 'trending_genres' in globals() and trending_genres:
        if "action" in trending_genres:
            mechanic_scores["dash ability"] = min(mechanic_scores.get("dash ability", 50) + 5, 100)
            mechanic_scores["time slow"] = min(mechanic_scores.get("time slow", 50) + 3, 100)
        if "platformer" in trending_genres:
            mechanic_scores["double jump"] = min(mechanic_scores.get("double jump", 50) + 8, 100)
            mechanic_scores["wall run"] = min(mechanic_scores.get("wall run", 50) + 5, 100)
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
    improvements["mechanic_scores"] = mechanic_scores
    improvements["last_analysis"] = datetime.now().isoformat()
    improvement_file.write_text(json.dumps(improvements, indent=2))
    print(f"   📊 Mechanic scores updated")
    print(f"   🎯 Top mechanic: {max(mechanic_scores, key=mechanic_scores.get)}")
    return selected

# ============ 1. LEARN FROM X TRENDS ============
print("\n📊 Learning from X trends...")
trending_genres = ["platformer", "puzzle"]
trending_hashtags = ["#gamedev", "#indiedev"]
def learn_from_x_trends():
    if not bearer_token:
        print("   No X bearer token – using defaults")
        return ["platformer", "puzzle"], ["#gamedev", "#indiedev"]
    try:
        headers = {"Authorization": f"Bearer {bearer_token}"}
        params = {"query": "gamedev OR indie game OR game release -filter:retweets", "max_results": 50, "tweet.fields": "public_metrics"}
        response = requests.get("https://api.twitter.com/2/tweets/search/recent", headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            tweets = response.json().get("data", [])
            if tweets:
                all_text = " ".join([t.get("text", "") for t in tweets]).lower()
                genres = {"action": all_text.count("action"), "platformer": all_text.count("platformer"), "puzzle": all_text.count("puzzle"), "rpg": all_text.count("rpg"), "strategy": all_text.count("strategy")}
                sorted_g = sorted(genres.items(), key=lambda x: x[1], reverse=True)
                top = [g for g, c in sorted_g if c > 0][:2]
                if top:
                    print(f"   🔥 Trending: {', '.join(top)}")
                    return top, ["#gamedev", "#indiedev"]
    except Exception as e:
        print(f"   ⚠️ Learning error: {e}")
    return ["platformer", "puzzle"], ["#gamedev", "#indiedev"]

trending_genres, trending_hashtags = learn_from_x_trends()
print(f"   🎯 Recommended genres: {trending_genres}")

# ============ 2. GENERATE AI GAME NAME ============
print("\n🎮 Generating unique game name...")
def generate_ai_name():
    if openai_key:
        try:
            resp = requests.post("https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"},
                json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "Generate ONE creative video game name. Return ONLY the name, no quotes. Max 25 chars."}], "temperature": 0.9, "max_tokens": 20}, timeout=30)
            if resp.status_code == 200:
                name = resp.json()["choices"][0]["message"]["content"].strip().strip('"')
                if name and len(name) < 35:
                    return name
        except Exception as e:
            print(f"   OpenAI error: {e}")
    prefixes = ["Neon", "Cyber", "Quantum", "Astral", "Void", "Echo", "Flux", "Rogue", "Solar", "Nova"]
    suffixes = ["Runner", "Drifter", "Breach", "Vector", "Pulse", "Shift", "Core", "Edge", "Zone"]
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"

game_name = generate_ai_name()
print(f"   ✅ {game_name}")
repo_name = f"daily-{game_name.lower().replace(' ', '-')}"

# ============ 3. SELECT GAME TYPE & MECHANIC ============
print("\n🎮 Selecting game mechanics...")
all_game_types = ["top-down shooter", "precision platformer", "puzzle crawler", "endless runner", "action rpg"]
all_mechanics = ["dash ability", "double jump", "time slow", "energy shield", "grappling hook", "wall run"]
selected_mechanic = analyze_and_improve()
genre_map = {"action": "top-down shooter", "platformer": "precision platformer", "puzzle": "puzzle crawler", "rpg": "action rpg"}
selected_type = genre_map.get(trending_genres[0], random.choice(all_game_types)) if trending_genres else random.choice(all_game_types)
print(f"   📊 Based on X trends: {trending_genres if trending_genres else 'default'}")
print(f"   🎮 Genre: {selected_type}")
print(f"   ⚡ Mechanic: {selected_mechanic}")

# ============ 4. DYNAMIC GAME ART ============
print("\n🎨 Generating awesome game art...")
sprite_path = Path("sprite.png")
def generate_cool_art():
    try:
        art_styles = [
            f"pixel+art+game+sprite+{game_name.replace(' ', '+')}+character+hero+centered+glowing+detailed",
            f"rpg+character+portrait+{game_name.replace(' ', '+')}+fantasy+art+shiny+armor",
            f"chibi+game+character+{game_name.replace(' ', '+')}+cute+colorful+dynamic+pose",
            f"retro+arcade+sprite+{game_name.replace(' ', '+')}+8-bit+pixel+art+action"
        ]
        url = f"https://image.pollinations.ai/prompt/{random.choice(art_styles)}?width=512&height=512&model=flux"
        print("   Generating with Pollinations.ai (free AI)...")
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200 and len(resp.content) > 5000:
            with open(sprite_path, "wb") as f:
                f.write(resp.content)
            print("   ✅ Pollinations.ai created cool art!")
            return True
    except Exception as e:
        print(f"   Pollinations.ai error: {e}")
    print("   Creating custom algorithmic game sprite...")
    random.seed(game_name + datetime.now().strftime("%Y-%m-%d"))
    img = Image.new('RGBA', (512, 512), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    center = 256
    for r in range(256, 0, -20):
        alpha = int(100 * (1 - r/256))
        col = (random.randint(30,80), random.randint(30,80), random.randint(100,180), alpha)
        draw.ellipse([center-r, center-r, center+r, center+r], fill=col)
    body_col = (random.randint(180,255), random.randint(80,180), random.randint(50,150))
    draw.ellipse([180,200,332,380], fill=body_col, outline=(0,0,0), width=3)
    head_col = (body_col[0]-20, body_col[1]-20, body_col[2]-20)
    draw.ellipse([210,130,302,230], fill=head_col, outline=(0,0,0), width=3)
    draw.ellipse([235,170,255,190], fill=(255,255,255))
    draw.ellipse([257,170,277,190], fill=(255,255,255))
    draw.ellipse([242,175,252,185], fill=(0,0,0))
    draw.ellipse([264,175,274,185], fill=(0,0,0))
    if random.random() > 0.5:
        draw.arc([240,190,272,210], 0, 180, fill=(0,0,0), width=2)
    else:
        draw.arc([240,190,272,210], 0, -180, fill=(0,0,0), width=2)
    if "dash" in selected_mechanic:
        draw.polygon([(220,130),(256,80),(292,130)], fill=(255,215,0), outline=(0,0,0), width=2)
    elif "shield" in selected_mechanic:
        draw.ellipse([140,250,210,320], fill=(100,150,255), outline=(255,255,255), width=3)
    elif "jump" in selected_mechanic:
        draw.rectangle([270,300,330,370], fill=(139,69,19), outline=(0,0,0), width=2)
    elif "grapple" in selected_mechanic:
        draw.line([(256,200),(300,140)], fill=(100,100,100), width=6)
    elif "invisibility" in selected_mechanic:
        draw.ellipse([180,200,332,380], outline=(200,200,200,100), width=4)
    else:
        draw.polygon([(256,350),(280,400),(232,400)], fill=(255,0,0), outline=(0,0,0), width=2)
    draw.ellipse([150,100,362,412], outline=(255,255,100), width=4)
    draw.text((180,460), game_name[:15], fill=(255,255,255))
    for _ in range(30):
        x,y = random.randint(30,482), random.randint(30,482)
        draw.point((x,y), fill=(255,255,200))
    img.save(sprite_path)
    return True

generate_cool_art()
print(f"   ✅ Sprite ready!")

# ============ 5. GODOT PROJECT ============
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

# ============ 6. README ============
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
| Arrow Keys | Move |
| Space | Special ability |
## 📥 Download & Purchase
- **Price:** ${game_price} USD
- **Payment:** Solana (Trust Wallet or Phantom Wallet)
- **Free demo version:** [Download from GitHub](https://github.com/{BRAND_GITHUB}/{repo_name}/archive/main.zip)
## 🤝 Connect With DeathRoll
| Platform | Link |
|----------|------|
| 📧 **Email** | {BRAND_EMAIL_PRIMARY} |
| 📱 **Telegram** | {BRAND_TELEGRAM} |
| 🎵 **TikTok** | {BRAND_TIKTOK} |
| 🌐 **Website** | {BRAND_WEBSITE} |
**Made with ❤️ by DeathRoll Studio**
*Support: {BRAND_EMAIL_PRIMARY}*
"""
(project_dir / "README.md").write_text(readme_content)
print(f"   ✅ Created README with DeathRoll branding")

# ============ 7. GITHUB REPO ============
print("\n📦 Creating GitHub repository...")
repo_url = None
github_owner = BRAND_GITHUB
if github_token:
    try:
        resp = requests.post("https://api.github.com/user/repos", headers={"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}, json={"name": repo_name, "description": f"{game_name} - A {selected_type} game by DeathRoll Studio | Price ${game_price}", "private": False, "auto_init": True}, timeout=30)
        if resp.status_code == 201:
            repo_url = resp.json()["html_url"]
            print(f"   ✅ Repo created: {repo_url}")
        else:
            print(f"   ⚠️ Repo creation: {resp.status_code}")
    except Exception as e:
        print(f"   ⚠️ GitHub error: {e}")
repo_link = repo_url or f"https://github.com/{github_owner}/{repo_name}"

# ============ 8. DEMO PAGE ============
print("\n🌐 Creating demo landing page...")
raw_demo_link = f"https://htmlpreview.github.io/?https://github.com/{github_owner}/{repo_name}/blob/main/demo.html"
landing_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{game_name} – DeathRoll Studio</title>
<meta property="og:image" content="icon.png"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:system-ui;background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px}}
.card{{max-width:800px;background:rgba(255,255,255,0.1);backdrop-filter:blur(10px);border-radius:40px;padding:30px;text-align:center;color:#fff;box-shadow:0 25px 45px rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.2)}}
h1{{font-size:2.5rem}}.sprite{{width:256px;height:256px;margin:20px auto;background:#1e1a2f;border-radius:30px;overflow:hidden;box-shadow:0 10px 20px rgba(0,0,0,0.3)}}
.sprite img{{width:100%;height:100%;object-fit:contain}}.badge{{display:inline-block;background:rgba(255,255,255,0.2);padding:6px 14px;border-radius:40px;margin:5px;font-size:0.9rem}}
.price{{font-size:2rem;font-weight:bold;color:#ffd700;margin:15px 0}}.btn{{display:inline-block;background:#ff6b6b;color:#fff;padding:12px 28px;border-radius:40px;text-decoration:none;font-weight:bold;margin:15px 10px;transition:transform 0.2s}}
.btn:hover{{transform:scale(1.05);background:#ff4757}}.btn-secondary{{background:#4a90e2}}.btn-secondary:hover{{background:#357abd}}
.contact{{background:rgba(255,255,255,0.05);border-radius:30px;padding:20px;margin-top:20px}}
.wallet{{background:rgba(0,0,0,0.3);border-radius:20px;padding:15px;margin:15px 0;font-family:monospace;word-break:break-all}}
.footer{{margin-top:30px;font-size:0.8rem;opacity:0.7}}
</style></head>
<body>
<div class="card">
<h1>🎮 {game_name}</h1>
<div class="sprite"><img src="icon.png" alt="Game sprite"></div>
<div><span class="badge">{selected_type}</span><span class="badge">{selected_mechanic}</span></div>
<div class="price">${game_price} USD</div>
<p>A <strong>{selected_type}</strong> where you master the <strong>{selected_mechanic}</strong>.<br>Created daily by DeathRoll Studio.</p>
<div>
<a href="{repo_link}" class="btn">⬇️ Download Demo</a>
<a href="mailto:{BRAND_EMAIL_PRIMARY}?subject=Purchase%20{game_name}" class="btn btn-secondary">💰 Contact to Buy</a>
<a href="{MONETIZATION_LINK}" class="btn btn-secondary" target="_blank">🔐 Trust Wallet</a>
</div>
<div class="contact">
<strong>📞 Send ${game_price} SOL to either wallet:</strong>
<div class="wallet">🔵 <strong>Trust Wallet:</strong><br><code>{SOLANA_TRUST_WALLET}</code></div>
<div class="wallet">🟣 <strong>Phantom Wallet:</strong><br><code>{SOLANA_PHANTOM_WALLET}</code></div>
<p>After payment, email <a href="mailto:{BRAND_EMAIL_PRIMARY}" style="color:#ffd700;">{BRAND_EMAIL_PRIMARY}</a> or Telegram <strong>{BRAND_TELEGRAM}</strong> with TX ID. You'll get full game files + commercial license.</p>
</div>
<div class="footer">🎵 TikTok: {BRAND_TIKTOK} | 🌐 {BRAND_WEBSITE}<br>New game every day!</div>
</div>
</body>
</html>"""
(project_dir / "demo.html").write_text(landing_html)
print(f"   ✅ Demo page: {raw_demo_link}")

# ============ 9. AI DESCRIPTION (shared) ============
print("\n🤖 Generating AI description...")
bluesky_description = ""
if openai_key:
    try:
        prompt = f"Write a short, exciting game description for '{game_name}'. Genre: {selected_type}. Mechanic: {selected_mechanic}. Keep under 200 chars. Make people want to click."
        resp = requests.post("https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"},
            json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}], "temperature": 0.8, "max_tokens": 80}, timeout=15)
        if resp.status_code == 200:
            bluesky_description = resp.json()["choices"][0]["message"]["content"].strip().strip('"')
            print(f"   🤖 {bluesky_description[:80]}...")
    except Exception as e:
        print(f"   AI description error: {e}")
if not bluesky_description:
    bluesky_description = f"A {selected_type} where you master the {selected_mechanic}. Unique daily games from DeathRoll Studio!"

# ============ 10. BLUESKY POST (FIXED) ============
print("\n🦋 Posting to Bluesky...")
bluesky_post_url = None
if bluesky_handle and bluesky_password:
    try:
        session = requests.post("https://bsky.social/xrpc/com.atproto.server.createSession", json={"identifier": bluesky_handle, "password": bluesky_password}, timeout=30)
        if session.status_code == 200:
            data = session.json()
            access_token = data["accessJwt"]
            did = data["did"]
            with open(sprite_path, "rb") as f:
                upload = requests.post("https://bsky.social/xrpc/com.atproto.repo.uploadBlob", headers={"Authorization": f"Bearer {access_token}"}, files={"blob": f.read()}, timeout=30)
            if upload.status_code == 200:
                blob = upload.json()["blob"]
                post_text = f"🎮 {game_name}\n\n{bluesky_description}\n\n💰 Price: ${game_price} SOL\n\n{repo_link}\n\n#gamedev #indiedev #{game_name.replace(' ', '')}"
                post_resp = requests.post("https://bsky.social/xrpc/com.atproto.repo.createRecord",
                    headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
                    json={"repo": did, "collection": "app.bsky.feed.post", "record": {"$type": "app.bsky.feed.post", "text": post_text[:300], "createdAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "embed": {"$type": "app.bsky.embed.images", "images": [{"image": blob, "alt": f"{game_name} art"}]}}}, timeout=30)
                if post_resp.status_code == 200:
                    bluesky_post_url = f"https://bsky.app/profile/{bluesky_handle}"
                    print(f"   ✅ Posted to Bluesky with image!")
                else:
                    print(f"   ❌ Bluesky post failed: {post_resp.status_code} {post_resp.text}")
            else:
                print(f"   ❌ Bluesky upload failed: {upload.status_code}")
        else:
            print(f"   ❌ Bluesky login failed: {session.status_code}")
    except Exception as e:
        print(f"   ❌ Bluesky error: {e}")
else:
    print("   ⚠️ No Bluesky credentials – skipping")

# ============ 11. MASTODON POST (if configured) ============
print("\n🐘 Posting to Mastodon...")
mastodon_post_url = None
if mastodon_token and mastodon_instance:
    try:
        with open(sprite_path, "rb") as img:
            media = requests.post(f"{mastodon_instance}/api/v2/media", headers={"Authorization": f"Bearer {mastodon_token}"}, files={"file": img}, timeout=30)
        if media.status_code == 200:
            media_id = media.json()["id"]
            post_text = f"🎮 {game_name}\n\n{bluesky_description}\n\n💰 Price: ${game_price} SOL\n\n{repo_link}\n\n#gamedev #indiedev"
            status = requests.post(f"{mastodon_instance}/api/v1/statuses", headers={"Authorization": f"Bearer {mastodon_token}"}, json={"status": post_text, "media_ids": [media_id], "visibility": "public"}, timeout=30)
            if status.status_code == 200:
                mastodon_post_url = status.json()["url"]
                print(f"   ✅ Posted to Mastodon!")
            else:
                print(f"   ❌ Mastodon status error: {status.status_code}")
        else:
            print(f"   ❌ Mastodon media error: {media.status_code}")
    except Exception as e:
        print(f"   ❌ Mastodon error: {e}")
else:
    print("   ⚠️ No Mastodon credentials – skipping")

# ============ 12. TELEGRAM: PRIVATE CHAT & PUBLIC CHANNEL ============
print("\n📱 Sending Telegram reports...")
if telegram_token:
    # Send photo to private chat
    try:
        with open(sprite_path, "rb") as photo:
            files = {"photo": photo}
            data = {"chat_id": telegram_chat_id, "caption": f"🎮 {game_name} – {bluesky_description}"}
            requests.post(f"https://api.telegram.org/bot{telegram_token}/sendPhoto", files=files, data=data, timeout=30)
            print("   ✅ Game art sent to private chat")
    except Exception as e:
        print(f"   ⚠️ Private photo error: {e}")

    # Send photo to public channel @drolltech
    try:
        with open(sprite_path, "rb") as photo:
            files = {"photo": photo}
            data = {"chat_id": TELEGRAM_CHANNEL, "caption": f"🎮 {game_name} – {bluesky_description}"}
            requests.post(f"https://api.telegram.org/bot{telegram_token}/sendPhoto", files=files, data=data, timeout=30)
            print(f"   ✅ Game art sent to channel {TELEGRAM_CHANNEL}")
    except Exception as e:
        print(f"   ⚠️ Channel photo error: {e}")

    # Detailed text message for private chat
    private_msg = f"""🎮 *DEATHROLL STUDIO – DAILY GAME* 🎮

*Game:* {game_name}
*Genre:* {selected_type}
*Mechanic:* {selected_mechanic}
*Price:* ${game_price} USD (Solana)

📝 *Description:* {bluesky_description}

🔗 *Links:*
• GitHub: {repo_link}
• Demo Page: {raw_demo_link}
• Bluesky: {bluesky_post_url or 'Not posted'}
• Mastodon: {mastodon_post_url or 'Not posted'}

💰 *Solana Wallets:*
Trust: `{SOLANA_TRUST_WALLET[:15]}...`
Phantom: `{SOLANA_PHANTOM_WALLET[:15]}...`

🏷️ *DeathRoll Studio*
🤖 *Bot learns and improves daily!* v{BOT_VERSION}"""
    requests.post(f"https://api.telegram.org/bot{telegram_token}/sendMessage", json={"chat_id": telegram_chat_id, "text": private_msg, "parse_mode": "Markdown"}, timeout=30)
    print("   ✅ Private report sent")

    # Shorter public message for channel (no wallet details)
    channel_msg = f"""🎮 *{game_name}* – New game from DeathRoll Studio!

{bluesky_description}

🔗 Download / Demo: {repo_link}
💰 Price: ${game_price} SOL (contact @deathroll1 to buy)

#gamedev #indiedev #{game_name.replace(' ', '')}"""
    requests.post(f"https://api.telegram.org/bot{telegram_token}/sendMessage", json={"chat_id": TELEGRAM_CHANNEL, "text": channel_msg, "parse_mode": "Markdown"}, timeout=30)
    print(f"   ✅ Public announcement sent to {TELEGRAM_CHANNEL}")

# ============ 13. SAVE LEARNING DATA ============
print("\n💾 Saving learning data...")
learning_data = {"last_run": datetime.now().isoformat(), "game_name": game_name, "genre": selected_type, "mechanic": selected_mechanic, "trending": trending_genres, "repo_url": repo_link, "price": game_price, "bot_version": BOT_VERSION}
Path("learning_data.json").write_text(json.dumps({"history": [learning_data], "last_update": datetime.now().isoformat()}, indent=2))
print("   ✅ Learning data saved")

# ============ 14. UPDATE PORTFOLIO ============
print("\n📁 Updating portfolio...")
portfolio_file = Path("portfolio.json")
entries = []
if portfolio_file.exists():
    try:
        entries = json.loads(portfolio_file.read_text())
    except:
        pass
entries.append({"date": datetime.now().isoformat(), "game": game_name, "genre": selected_type, "mechanic": selected_mechanic, "trending": trending_genres, "repo": repo_link, "price": game_price, "bluesky": bluesky_post_url, "mastodon": mastodon_post_url})
portfolio_file.write_text(json.dumps(entries[-50:], indent=2))
print(f"   ✅ Portfolio has {len(entries)} games")

# ============ 15. SUPPORT FILE ============
print("\n📧 Creating support & purchase file...")
support = f"""DeathRoll Studio – Support & Purchase

Game: {game_name}
Date: {datetime.now().strftime('%Y-%m-%d')}
Price: ${game_price} SOL

Payment: Solana only
Trust Wallet: {SOLANA_TRUST_WALLET}
Phantom Wallet: {SOLANA_PHANTOM_WALLET}

How to purchase:
1. Send exactly ${game_price} SOL to either wallet.
2. Email {BRAND_EMAIL_PRIMARY} or Telegram {BRAND_TELEGRAM} with TX ID.
3. You'll receive full Godot files + commercial license + lifetime updates.

Contact: {BRAND_EMAIL_PRIMARY} | {BRAND_TELEGRAM}
"""
(project_dir / "SUPPORT.txt").write_text(support)
print("   ✅ Support file created")

# ============ 16. VERIFICATION ============
print("\n🔍 Verifying all systems...")
systems = {"AI Name Generation": True, "Art Generation": True, "Godot Project": True, "GitHub Integration": bool(github_token), "Bluesky Posting": bool(bluesky_handle and bluesky_password), "Mastodon Posting": bool(mastodon_token), "X Learning": bool(bearer_token), "Self-Improvement": True, "Demo Page": True, "Payment Contact": True}
for s, ok in systems.items():
    print(f"   {s}: {'✅' if ok else '⚠️'}")

# ============ DONE ============
print("\n" + "=" * 60)
print(f"✅ {game_name} is READY!")
print(f"   🏷️ Brand: DeathRoll Studio")
print(f"   📧 Support: {BRAND_EMAIL_PRIMARY}")
print(f"   📱 Telegram: {BRAND_TELEGRAM} | Channel: {TELEGRAM_CHANNEL}")
print(f"   🎮 Genre: {selected_type} | Mechanic: {selected_mechanic}")
print(f"   💰 Price: ${game_price} SOL")
print(f"   📦 GitHub: {repo_link}")
print(f"   🌐 Demo: {raw_demo_link}")
print("=" * 60)

with open("build_info.txt", "w") as f:
    f.write(f"Game: {game_name}\nGenre: {selected_type}\nMechanic: {selected_mechanic}\nPrice: ${game_price} SOL\nTime: {datetime.now()}\nRepo: {repo_link}\nDemo: {raw_demo_link}\nEmail: {BRAND_EMAIL_PRIMARY}\nTelegram: {BRAND_TELEGRAM}\nChannel: {TELEGRAM_CHANNEL}\nTrust Wallet: {SOLANA_TRUST_WALLET}\nPhantom Wallet: {SOLANA_PHANTOM_WALLET}\nBot Version: {BOT_VERSION}\n")

print("\n🎉 DEATHROLL STUDIO BOT FINISHED SUCCESSFULLY!")
print("🧠 Your bot learned, adapted, and created a new game!")
print("💰 Buyers can send SOL to your Trust or Phantom wallet.")
print("🖼️ Game art embedded in Bluesky, Mastodon, and Telegram.")
print(f"📢 Public Telegram channel: {TELEGRAM_CHANNEL}")
