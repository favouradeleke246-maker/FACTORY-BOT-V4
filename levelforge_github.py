#!/usr/bin/env python3
"""
DEATHROLL STUDIO v30.0 — COMPLETE GAME FACTORY (ALL 5 GENRES)
Generates a new mobile game every day with AI mechanics, modern UI, and beautiful art.
"""
import os, json, random, requests, shutil, zipfile, hashlib, math, html
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_OK = True
except ImportError:
    PIL_OK = False

# ---------- CONFIG ----------
BOT_VERSION = "30.0.0"
BRAND_GITHUB = "favouradeleke246-maker"
BRAND_REPO = "FACTORY-BOT-V4"
TELEGRAM_CHANNEL = "@drolltech"
SOLANA_TRUST = "6wsQ6nGXrUUUGCEokb4rZcfHDv2a8MomUb22TuVaH2m3"
SOLANA_PHANTOM = "Csk9DKstWMdKx19gUHWB9xy2VwZZX2nx6V6oSVGDCgMb"
GAME_PRICE = os.getenv("GAME_PRICE", "7")
TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TG_ADMIN = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GH_TOKEN = os.getenv("GH_TOKEN")
WHATSAPP_WEBHOOK_URL = os.getenv("WHATSAPP_WEBHOOK_URL", "")

BASE_URL = f"https://{BRAND_GITHUB}.github.io/{BRAND_REPO}"
RAW_URL = f"https://raw.githubusercontent.com/{BRAND_GITHUB}/{BRAND_REPO}/main"

# ---------- TELEGRAM HELPERS (safe HTML) ----------
def tg_send_photo(chat_id, photo_path, caption):
    if not TG_TOKEN: return False
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto"
    try:
        with open(photo_path, "rb") as f:
            files = {"photo": f}
            # Escape caption to avoid HTML injection but keep our tags
            safe_caption = caption.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            # But we need to allow <b>, <i>, <code> etc. We'll just send as is – we trust our own formatting.
            data = {
                "chat_id": chat_id,
                "caption": caption,
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            }
            r = requests.post(url, files=files, data=data, timeout=40)
        if r.status_code == 200:
            print(f"  ✅ Telegram photo sent to {chat_id}")
            return True
        else:
            print(f"  ❌ Telegram error {r.status_code}: {r.text[:200]}")
            return False
    except Exception as e:
        print(f"  ❌ Telegram exception: {e}")
        return False

def tg_send_doc(chat_id, doc_path, caption):
    if not TG_TOKEN: return False
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendDocument"
    try:
        with open(doc_path, "rb") as f:
            files = {"document": f}
            data = {"chat_id": chat_id, "caption": caption, "parse_mode": "HTML"}
            r = requests.post(url, files=files, data=data, timeout=90)
        if r.status_code == 200:
            print(f"  ✅ Document sent to {chat_id}")
            return True
        else:
            print(f"  ❌ Document error: {r.text[:200]}")
            return False
    except Exception as e:
        print(f"  ❌ Document exception: {e}")
        return False

def send_to_whatsapp(text, image_url=None):
    if not WHATSAPP_WEBHOOK_URL: return False
    try:
        r = requests.post(WHATSAPP_WEBHOOK_URL, json={"text": text, "image_url": image_url}, timeout=15)
        return r.status_code == 200
    except: return False

# ---------- OPENAI ----------
def call_openai(prompt, max_tokens=300, system=""):
    if not OPENAI_KEY: return None
    try:
        r = requests.post("https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_KEY}", "content-type": "application/json"},
            json={"model": "gpt-4o-mini", "max_tokens": max_tokens,
                  "messages": ([{"role":"system","content":system}] if system else []) + [{"role":"user","content":prompt}]},
            timeout=50)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip().strip('"')
    except Exception as e:
        print(f"  ⚠️  OpenAI error: {e}")
    return None

# ---------- GENRES & LISTS ----------
GENRES = {
    "top-down shooter":   {"emojis": ["🔫","💥","🎯"], "color": "#ff4444", "bg": "#0d0005"},
    "action RPG":         {"emojis": ["⚔️","🛡️","👑"], "color": "#ffd700", "bg": "#0a0800"},
    "racing game":        {"emojis": ["🏎️","💨","🔥"], "color": "#00cfff", "bg": "#000a10"},
    "puzzle game":        {"emojis": ["🧩","💡","🔮"], "color": "#b44fff", "bg": "#08000d"},
    "survival horror":    {"emojis": ["😱","💀","👻"], "color": "#33ff99", "bg": "#000d04"},
    "fighting game":      {"emojis": ["👊","💥","⚡"], "color": "#ff6600", "bg": "#0d0400"},
    "strategy game":      {"emojis": ["♟️","🧠","🏰"], "color": "#4488ff", "bg": "#00040d"},
    "roguelite":          {"emojis": ["🎲","⚡","💀"], "color": "#ff44aa", "bg": "#0d0008"},
    "platformer":         {"emojis": ["🦘","⭐","🎮"], "color": "#ffcc00", "bg": "#0a0800"},
    "stealth game":       {"emojis": ["🕵️","🌑","🔪"], "color": "#88ccff", "bg": "#000508"},
    "extraction shooter": {"emojis": ["🔫","💰","🚁"], "color": "#ff8800", "bg": "#0d0600"},
    "cozy builder":       {"emojis": ["🏡","🌸","✨"], "color": "#ff99cc", "bg": "#0a0006"},
    "tower defense":      {"emojis": ["🏰","💣","🛡️"], "color": "#44ffbb", "bg": "#000d07"},
    "metroidvania":       {"emojis": ["🗺️","🔑","⚔️"], "color": "#cc88ff", "bg": "#06000d"},
}

PREFIXES = ["Neon","Cyber","Quantum","Astral","Void","Echo","Flux","Rogue","Crimson","Shadow","Phantom","Eclipse","Solar","Nova","Iron","Dark","Storm","Hyper","Apex","Omega","Zenith","Vortex","Blaze","Frost","Titan","Ghost","Pulse","Arc","Rift","Chrome","Surge","Static","Aether","Binary","Carbon","Delta","Ember","Forge","Glitch","Helix","Inferno","Jade","Kinetic","Lunar","Magma","Nexus","Obsidian","Prism","Quasar","Radiant","Sonic","Turbo","Ultra","Vapor","Warp","Xenon","Amber","Blitz","Cobalt","Dusk","Enigma","Fractal","Glacial","Hex","Ionic","Jinx","Krypto","Lancer","Mirage","Null","Optic","Pixel","Quake","Reaper","Scarlet","Thorn","Umbra","Venom","Wraith","Xeno","Yearn","Zeal","Abyssal","Brutal","Caustic","Desolate","Eternal","Feral","Grim","Hollow","Ironskin","Jagged","Kel","Lethal","Molten"]
SUFFIXES = ["Runner","Drifter","Breach","Vector","Pulse","Shift","Core","Edge","Zone","Realm","Fury","Strike","Blade","Force","Maze","Hunt","War","Fall","Rise","Gate","Lab","Ops","Shard","Crash","Dash","Drive","Fight","Grid","Hook","Impact","Jump","Kill","Lock","March","Nexus","Orbit","Path","Quest","Race","Siege","Tank","Vault","Wing","Arena","Base","Chain","Dome","Echo","Field","Gloom","Haze","Isle","Jungle","Keep","Loop","Mire","Outpost","Peak","Ridge","Spire","Trail","Waste","Expanse","Abyss","Citadel","Den","Expanse","Front","Gulch","Hollow","Iris","Jaw","Knell","Lore","Mark","Night","Omen","Pyre","Ruin","Shroud","Tomb","Undertow","Vale","Wreck","Xenith","Yonder","Zenith","Deep"]
MECHANICS_FALLBACK = [
    ("Phase Echo", "Tap to leave a ghost clone — enemies attack it instead of you"),
    ("Chrono Fracture", "Hold to freeze all enemies in a 3-second time bubble"),
    ("Void Step", "Double-tap to teleport through any obstacle once per 4 seconds"),
    ("Mirror Shell", "Absorb one hit and reflect triple damage back at attacker"),
    ("Gravity Well", "Pull all enemies toward your cursor/finger with a singularity"),
    ("Soul Link", "Link to an enemy — you share health, so use them as a shield"),
    ("Signal Jam", "Disable all enemy projectiles for 3 seconds with an EMP burst"),
    ("Death Bloom", "Near-death triggers a massive radial shockwave instantly"),
    ("Echo Strike", "Every attack automatically repeats 0.8s later for free"),
    ("Fracture Line", "Draw a line — anything that crosses it takes 3x damage"),
    ("Null Field", "Drop a zone where no enemy abilities or bullets work"),
    ("Chain Spark", "Hit one enemy and lightning chains instantly to 4 others"),
    ("Bleed Aura", "Moving fast leaves a damage trail that hurts anything following"),
    ("Inverted Shield", "Your shield deals damage — the harder you're hit, the more you deal"),
    ("Time Anchor", "Mark your position; one button warps you back to it at any moment"),
    ("Overclock", "Speed boost so extreme enemies appear frozen — lasts 2 seconds"),
    ("Phantom Rush", "A ghost version of you rushes forward, triggering all traps safely"),
    ("Collapse Wave", "Every 10 kills trigger a screen-wide collapse dealing massive damage"),
]
HOOKS = ["This game will haunt you 🔥", "I built this in 24 hours", "Your next obsession just dropped", "Run. Or die trying", "1000 IQ moves only", "Speed meets absolute chaos", "One mechanic. Infinite depth", "Can you survive this?", "Most intense drop this week", "This one hits completely different", "No one is ready for this mechanic", "Built different. Plays different", "The game that broke my brain", "Indie gold just dropped", "You've never played anything like this"]

# ---------- SAR ----------
sar_path = Path("sar_analysis.json")
SAR = {"study": {"total_runs": 0, "art_ok": 0, "art_fail": 0, "games": []}, "analysis": {"best_genre": None, "rate": 0.0}}
if sar_path.exists():
    try:
        d = json.loads(sar_path.read_text())
        for k in SAR: SAR[k].update(d.get(k, {}))
    except: pass

# ---------- TRENDS ----------
def fetch_trends():
    found = []
    for sub in ["gamedev", "indiegaming"]:
        try:
            r = requests.get(f"https://www.reddit.com/r/{sub}/top.json?limit=30&t=day", headers={"User-Agent": "DeathRollStudio/3.0"}, timeout=10)
            if r.status_code == 200:
                posts = r.json().get("data", {}).get("children", [])
                text = " ".join(p["data"]["title"].lower() for p in posts)
                kws = ["action","platformer","puzzle","rpg","strategy","horror","shooter","roguelike","survival","racing","stealth","fighting"]
                for k in kws:
                    if k in text and k not in found: found.append(k)
        except: pass
    return found[:3]

# ---------- MAIN ----------
print("╔══════════════════════════════════════════════════════╗")
print(f"║  DEATHROLL STUDIO v{BOT_VERSION}  —  UPGRADED UI     ║")
print("╚══════════════════════════════════════════════════════╝")

trends = fetch_trends()
print(f"  🔥 Trending: {trends or ['none — using SAR']}")

# Genre selection
candidates = []
for t in trends:
    match = next((g for g in GENRES if t in g), None)
    if match: candidates.append(match)
if SAR["analysis"].get("best_genre"): candidates.append(SAR["analysis"]["best_genre"])
candidates.append(random.choice(list(GENRES.keys())))
GENRE = random.choice(candidates)
G_COLOR = GENRES[GENRE]["color"]
G_BG = GENRES[GENRE]["bg"]
G_EMOJIS = GENRES[GENRE]["emojis"]
EMOJI_STR = " ".join(random.sample(G_EMOJIS, len(G_EMOJIS)))
print(f"  🎮 Genre: {GENRE}  ({EMOJI_STR})")

# AI Mechanic & Description
print("  ⚙️  Generating mechanic...")
def gen_mechanic():
    if OPENAI_KEY:
        res = call_openai(f"Invent one UNIQUE, surprising game mechanic for a mobile {GENRE} game.\nIt must work well with TOUCH controls.\nReply EXACTLY:\nMECHANIC: <short name 2-4 words>\nDESCRIPTION: <one punchy sentence max 18 words>", max_tokens=100, system="You are a genius indie game designer.")
        if res:
            name = desc = None
            for line in res.splitlines():
                if line.startswith("MECHANIC:"): name = line.split(":",1)[1].strip()
                elif line.startswith("DESCRIPTION:"): desc = line.split(":",1)[1].strip()
            if name and desc: return name, desc
    return random.choice(MECHANICS_FALLBACK)

MECHANIC, MECH_DESC = gen_mechanic()
print(f"  ✨ {MECHANIC} — {MECH_DESC}")

# Game name
names_file = Path("recent_game_names.json")
recent = []
if names_file.exists():
    try: recent = json.loads(names_file.read_text())
    except: pass
def unique_name():
    pool = {n.lower() for n in recent}
    for _ in range(300):
        n = f"{random.choice(PREFIXES)} {random.choice(SUFFIXES)}"
        if n.lower() not in pool: return n
    return f"{random.choice(PREFIXES)} {random.choice(SUFFIXES)} {random.randint(2,99)}"
GAME_NAME = unique_name()
recent.append(GAME_NAME)
names_file.write_text(json.dumps(recent[-50:]))
SAFE_NAME = GAME_NAME.replace(" ", "_")
PLAY_URL = f"{BASE_URL}/workspace/{SAFE_NAME}/index.html"
IMG_URL = f"{RAW_URL}/workspace/{SAFE_NAME}/icon.png"
ZIP_URL = f"{RAW_URL}/workspace/latest_game.zip"
print(f"  🎯 Name: {GAME_NAME}")

# Short description
def gen_short_desc():
    if OPENAI_KEY:
        res = call_openai(f"Write ONE thrilling sentence (max 110 chars) for a mobile {GENRE} game called '{GAME_NAME}' featuring '{MECHANIC}'. No quotes.", max_tokens=60, system="You write killer indie game marketing copy.")
        if res and len(res) > 15: return res[:120]
    return f"Master {MECHANIC} in this {GENRE} — no two sessions are the same."
DESCRIPTION = gen_short_desc()
HOOK = random.choice(HOOKS)
TAGS = f"#gamedev #indiegame #mobilegame #{GENRE.replace(' ','').replace('-','')} #{MECHANIC.replace(' ','')} #DeathRollStudio"
print(f"  📝 {DESCRIPTION}")

# AI art prompt
def gen_art_prompt():
    if OPENAI_KEY:
        prompt = f"Write a detailed, vivid image generation prompt for a {GENRE} mobile game called '{GAME_NAME}' whose main mechanic is '{MECHANIC}'. The art should be stunning, game‑ready, suitable for a 512x512 icon. Include style, lighting, mood. Max 150 words."
        res = call_openai(prompt, max_tokens=200, system="You are a concept artist. Output only the prompt.")
        if res and len(res) > 20: return res
    return f"isometric 3D render, {GENRE} game character for '{GAME_NAME}', mechanic: {MECHANIC}, professional game art, dark background, dramatic lighting, high detail"
ART_PROMPT = gen_art_prompt()
print(f"  🖌️  Art prompt: {ART_PROMPT[:80]}...")

LICENSE_KEY = "DR-" + hashlib.md5(f"{GAME_NAME}{datetime.now().date()}{SOLANA_TRUST}".encode()).hexdigest()[:16].upper()

# Portfolio
port_path = Path("portfolio.json")
entries = []
if port_path.exists():
    try: entries = json.loads(port_path.read_text())
    except: entries = []
entry = {"id": f"game_{len(entries)+1:04d}", "date": datetime.now().isoformat(), "game": GAME_NAME, "genre": GENRE, "mechanic": MECHANIC, "mech_desc": MECH_DESC, "description": DESCRIPTION, "hook": HOOK, "hashtags": TAGS, "image_url": IMG_URL, "play_url": PLAY_URL, "zip_url": ZIP_URL, "price_sol": GAME_PRICE, "license_key": LICENSE_KEY, "color": G_COLOR, "sales": 0, "status": "generating"}
entries.append(entry)
entries = entries[-300:]
port_path.write_text(json.dumps(entries, indent=2))
print(f"  💾 Portfolio: {len(entries)} games")

# ---------- ART GENERATION (with modern fallback) ----------
print("  🎨 Generating game art...")
sprite = Path("sprite.png")
art_ok = False

if ART_PROMPT:
    try:
        enc = ART_PROMPT.replace(" ", "+").replace(",", "%2C").replace("'", "%27").replace("\n", " ")[:500]
        url = f"https://image.pollinations.ai/prompt/{enc}?width=512&height=512&seed={random.randint(1,999999)}&nologo=true"
        print(f"  🖼️  Trying Pollinations...")
        r = requests.get(url, timeout=60)
        if r.status_code == 200 and r.headers.get('content-type', '').startswith('image'):
            sprite.write_bytes(r.content)
            art_ok = True
            print("  ✅ AI‑generated art from custom prompt")
        else:
            print(f"  ⚠️  Pollinations returned {r.status_code}")
    except Exception as e:
        print(f"  ⚠️  Pollinations error: {e}")

    if not art_ok:
        simple_prompt = f"{GENRE} game {GAME_NAME} {MECHANIC} character art, dark cyberpunk style, 512x512 game icon"
        try:
            enc = simple_prompt.replace(" ", "+")
            url = f"https://image.pollinations.ai/prompt/{enc}?width=512&height=512&seed={random.randint(1,999999)}&nologo=true"
            r = requests.get(url, timeout=60)
            if r.status_code == 200 and r.headers.get('content-type', '').startswith('image'):
                sprite.write_bytes(r.content)
                art_ok = True
                print("  ✅ AI‑generated art (simple prompt)")
        except Exception as e:
            print(f"  ⚠️  Simple Pollinations error: {e}")

# Beautiful game cover fallback
if not art_ok and PIL_OK:
    print("  🎨 Generating modern game cover art...")
    img = Image.new("RGB", (512, 512), G_BG)
    draw = ImageDraw.Draw(img)

    # Gradient background
    for y in range(512):
        factor = y / 512
        r_val = int(10 + factor * 30)
        g_val = int(5 + factor * 20)
        b_val = int(20 + factor * 40)
        draw.line([(0, y), (512, y)], fill=(r_val, g_val, b_val))

    # Glowing concentric rings
    cx, cy = 256, 256
    for rad in range(200, 40, -20):
        alpha = max(20, 80 - rad//3)
        draw.ellipse([cx-rad, cy-rad, cx+rad, cy+rad], outline=(*bytes.fromhex(G_COLOR[1:]), alpha), width=3)

    # Diagonal scanlines
    for i in range(-512, 512, 20):
        draw.line([(i, 0), (i+512, 512)], fill=(*bytes.fromhex(G_COLOR[1:]), 15), width=1)
        draw.line([(0, i), (512, i+512)], fill=(*bytes.fromhex(G_COLOR[1:]), 15), width=1)

    # Hex grid overlay
    hex_size = 45
    for x in range(-hex_size, 512+hex_size, hex_size):
        for y in range(-hex_size, 512+hex_size, int(hex_size*0.86)):
            xc = x + (y % (hex_size*2)) * 0.5
            pts = []
            for i in range(6):
                ang = math.radians(60*i - 30)
                px = xc + hex_size * 0.6 * math.cos(ang)
                py = y + hex_size * 0.6 * math.sin(ang)
                pts.append((px, py))
            draw.polygon(pts, outline=(*bytes.fromhex(G_COLOR[1:]), 35), width=1)

    # Game title with outline
    try:
        font = ImageFont.load_default()
        title = GAME_NAME[:18]
        for offset in range(-2, 3):
            for oy in range(-2, 3):
                draw.text((cx-150+offset, cy-60+oy), title, fill=(0,0,0), anchor="mm", font=font)
        draw.text((cx-150, cy-60), title, fill=G_COLOR, anchor="mm", font=font)
    except:
        draw.text((cx-150, cy-60), GAME_NAME[:18], fill=G_COLOR, anchor="mm")

    # Genre badge
    genre_text = GENRE.upper()
    bbox = draw.textbbox((0,0), genre_text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    badge_x = cx - tw//2 - 10
    badge_y = cy + 10
    draw.rectangle([badge_x, badge_y, badge_x+tw+20, badge_y+th+8], fill=(*bytes.fromhex(G_COLOR[1:]), 60), outline=G_COLOR, width=1)
    draw.text((cx, cy+15), genre_text, fill=G_COLOR, anchor="mm", font=font)

    # Mechanic text
    mech_text = f"⚡ {MECHANIC}"
    draw.text((cx, cy+50), mech_text, fill=(200,200,200), anchor="mm", font=font)

    # Watermark
    draw.text((10, 480), "DeathRoll Studio", fill=(80,80,100))

    img.save(sprite)
    art_ok = True
    print("  ✅ Modern game cover art generated")

if not art_ok:
    img = Image.new("RGB", (512,512), G_BG)
    draw = ImageDraw.Draw(img)
    draw.text((256,256), GAME_NAME, fill=G_COLOR, anchor="mm")
    img.save(sprite)
    art_ok = True
    print("  ✅ Basic fallback art generated")

# ---------- MODERN UI FOR HTML5 GAMES (shared components) ----------
SHARED_HEAD = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>{GAME_NAME}</title>
<style>
  *{{margin:0;padding:0;box-sizing:border-box;user-select:none;-webkit-tap-highlight-color:transparent;}}
  body{{
    background: radial-gradient(circle at 20% 30%, #0a0a1a, #03030a);
    display:flex; align-items:center; justify-content:center;
    font-family:'Segoe UI','Poppins',system-ui,sans-serif;
    min-height:100vh;
  }}
  #game-container{{
    width:100%; max-width:480px; height:100vh;
    background: rgba(10,10,20,0.7);
    backdrop-filter: blur(2px);
    border-radius: 32px;
    overflow: hidden;
    box-shadow: 0 0 40px rgba(0,255,204,0.1);
    display: flex; flex-direction: column;
    border: 1px solid rgba(0,255,204,0.2);
  }}
  .hud{{
    display: flex; justify-content: space-between;
    padding: 16px 20px;
    background: rgba(0,0,0,0.5);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid rgba(0,255,204,0.3);
    font-weight: bold;
    color: #0ff;
    text-shadow: 0 0 5px #0ff;
    letter-spacing: 1px;
  }}
  .hud div{{
    background: rgba(0,0,0,0.6);
    padding: 6px 12px;
    border-radius: 40px;
    font-size: 14px;
  }}
  canvas{{
    flex: 1;
    width: 100%;
    display: block;
    background: #05050a;
  }}
  .joystick-area{{
    position: absolute; bottom: 20px; left: 20px;
    width: 130px; height: 130px;
    border-radius: 50%;
    background: rgba(0,0,0,0.4);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(0,255,204,0.4);
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .joystick-base{{
    width: 100px; height: 100px;
    border-radius: 50%;
    background: rgba(0,0,0,0.6);
    border: 1px solid #0ff;
    position: relative;
  }}
  .joystick-thumb{{
    width: 45px; height: 45px;
    border-radius: 50%;
    background: #0ff;
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 15px #0ff;
    transition: transform 0.05s linear;
  }}
  .action-buttons{{
    position: absolute; bottom: 20px; right: 20px;
    display: flex; gap: 15px;
  }}
  .action-btn{{
    width: 70px; height: 70px;
    border-radius: 50%;
    background: rgba(0,0,0,0.6);
    backdrop-filter: blur(8px);
    border: 1px solid #0ff;
    color: #0ff;
    font-size: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: 0.05s linear;
    box-shadow: 0 0 10px rgba(0,255,204,0.3);
  }}
  .action-btn:active{{
    transform: scale(0.92);
    background: rgba(0,255,204,0.2);
  }}
  .screen{{
    position: absolute; inset: 0;
    background: rgba(0,0,0,0.85);
    backdrop-filter: blur(10px);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 10;
    border-radius: 32px;
  }}
  .screen.hidden{{display: none;}}
  .screen h1{{
    font-size: 32px; color: #0ff; text-shadow: 0 0 20px #0ff;
    margin-bottom: 10px;
  }}
  .screen button{{
    background: #0ff; color: #000; border: none;
    padding: 12px 28px; border-radius: 40px;
    font-weight: bold; font-size: 18px;
    margin-top: 20px;
    cursor: pointer;
    box-shadow: 0 0 15px #0ff;
  }}
  @media (max-width: 500px){{
    .action-btn{{ width: 60px; height: 60px; font-size: 24px; }}
    .joystick-area{{ width: 110px; height: 110px; }}
    .joystick-base{{ width: 80px; height: 80px; }}
  }}
</style>
</head>"""

def start_screen():
    return f"""
<div id="startScreen" class="screen">
  <h1>{GAME_NAME}</h1>
  <p style="color:#ccc; margin-bottom:8px;">{GENRE}</p>
  <div style="background:#0ff22; padding:6px 12px; border-radius:20px; border:1px solid #0ff; margin:12px;">
    ⚡ {MECHANIC}
  </div>
  <p style="font-size:14px; color:#aaa;">{MECH_DESC[:80]}</p>
  <button onclick="startGame()">▶ PLAY FREE</button>
</div>
<div id="gameOverScreen" class="screen hidden">
  <h1>GAME OVER</h1>
  <p id="finalScore" style="font-size:24px; color:#0ff;">Score: 0</p>
  <button onclick="restartGame()">🔄 RESTART</button>
</div>"""

JOYSTICK_JS = """
const joyArea = document.querySelector('.joystick-area');
const joyBase = document.querySelector('.joystick-base');
const joyThumb = document.querySelector('.joystick-thumb');
let joyActive = false, joyId = -1, joyX = 0, joyY = 0, joyCenter = {x:0,y:0}, joyRadius = 40;
joyArea.addEventListener('touchstart', (e) => {
  e.preventDefault();
  const touch = e.touches[0];
  const rect = joyBase.getBoundingClientRect();
  joyActive = true;
  joyId = touch.identifier;
  joyCenter.x = rect.left + rect.width/2;
  joyCenter.y = rect.top + rect.height/2;
  updateJoy(touch);
});
joyArea.addEventListener('touchmove', (e) => {
  for(let t of e.touches) if(t.identifier === joyId) updateJoy(t);
});
joyArea.addEventListener('touchend', (e) => {
  joyActive = false;
  joyX = 0; joyY = 0;
  joyThumb.style.transform = 'translate(-50%, -50%)';
});
function updateJoy(touch) {
  const dx = touch.clientX - joyCenter.x;
  const dy = touch.clientY - joyCenter.y;
  const dist = Math.hypot(dx, dy);
  const angle = Math.atan2(dy, dx);
  const mag = Math.min(dist, joyRadius);
  joyX = (mag / joyRadius) * Math.cos(angle);
  joyY = (mag / joyRadius) * Math.sin(angle);
  joyThumb.style.transform = `translate(calc(-50% + ${joyX*joyRadius}px), calc(-50% + ${joyY*joyRadius}px))`;
}
const keyState = {};
document.addEventListener('keydown', e => { keyState[e.key] = true; e.preventDefault(); });
document.addEventListener('keyup', e => { keyState[e.key] = false; });
function getJoyFromKeys() {
  let x = 0, y = 0;
  if (keyState['ArrowRight']||keyState['d']) x = 1;
  if (keyState['ArrowLeft']||keyState['a']) x = -1;
  if (keyState['ArrowDown']||keyState['s']) y = 1;
  if (keyState['ArrowUp']||keyState['w']) y = -1;
  return {x, y};
}
"""

# ---------- FULL UPGRADED GAME BUILDERS (modern UI) ----------
def build_shooter_game():
    return SHARED_HEAD + """
<body>
<div id="game-container">
  <div class="hud"><div>💥 SCORE <span id="score">0</span></div><div>❤️ LIVES <span id="lives">3</span></div><div>🌊 WAVE <span id="wave">1</span></div></div>
  <canvas id="gameCanvas"></canvas>
  """ + start_screen() + """
  <div class="joystick-area"><div class="joystick-base"><div class="joystick-thumb"></div></div></div>
  <div class="action-buttons"><div class="action-btn" id="shootBtn">🔫</div><div class="action-btn" id="specialBtn">💥</div></div>
</div>
<script>
""" + JOYSTICK_JS + """
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
let W, H, player, enemies, bullets, score, lives, wave, frame, specialCharge, gameRunning;
function resize() {
  const container = document.getElementById('game-container');
  const hud = document.querySelector('.hud');
  canvas.width = W = container.clientWidth;
  canvas.height = H = container.clientHeight - hud.clientHeight;
}
window.addEventListener('resize', resize);
resize();
function init() {
  player = { x: W/2, y: H-80, r: 15, speed: 5, invincible: 0 };
  enemies = []; bullets = []; score = 0; lives = 3; wave = 1; frame = 0; specialCharge = 0;
  gameRunning = true;
  updateUI();
  requestAnimationFrame(gameLoop);
}
function startGame() { document.getElementById('startScreen').classList.add('hidden'); init(); }
function restartGame() { document.getElementById('gameOverScreen').classList.add('hidden'); init(); }
function updateUI() {
  document.getElementById('score').innerText = score;
  document.getElementById('lives').innerText = lives;
  document.getElementById('wave').innerText = wave;
}
function spawnEnemy() {
  let side = Math.floor(Math.random()*4);
  let x, y;
  if(side===0){ x=Math.random()*W; y=-20; }
  else if(side===1){ x=W+20; y=Math.random()*H; }
  else if(side===2){ x=Math.random()*W; y=H+20; }
  else{ x=-20; y=Math.random()*H; }
  enemies.push({ x:x, y:y, r:15, hp: 1+Math.floor(wave/3) });
}
function shoot() {
  let ang = Math.atan2(player.y+10 - player.y, player.x+10 - player.x);
  bullets.push({ x:player.x, y:player.y-10, dx:Math.cos(ang)*8, dy:Math.sin(ang)*8, r:4 });
}
function special() { if(specialCharge>=100){ specialCharge=0; enemies.forEach(e=>e.hp-=2); } }
document.getElementById('shootBtn').onclick = () => { if(gameRunning) shoot(); };
document.getElementById('specialBtn').onclick = () => { if(gameRunning) special(); };
function gameLoop() {
  if(!gameRunning) return;
  requestAnimationFrame(gameLoop);
  frame++;
  let joy = joyActive ? {x:joyX, y:joyY} : getJoyFromKeys();
  if(player.invincible>0) player.invincible--;
  player.x += joy.x * player.speed;
  player.y += joy.y * player.speed;
  player.x = Math.max(player.r, Math.min(W-player.r, player.x));
  player.y = Math.max(player.r, Math.min(H-player.r, player.y));
  if(frame%20===0 && enemies.length<10+wave) spawnEnemy();
  if(frame%15===0) shoot();
  specialCharge = Math.min(100, specialCharge+0.5);
  for(let e of enemies) {
    let ang = Math.atan2(player.y-e.y, player.x-e.x);
    e.x += Math.cos(ang)*2;
    e.y += Math.sin(ang)*2;
  }
  for(let i=0;i<bullets.length;i++) {
    bullets[i].x += bullets[i].dx;
    bullets[i].y += bullets[i].dy;
    if(bullets[i].x<-50||bullets[i].x>W+50||bullets[i].y<-50||bullets[i].y>H+50) bullets.splice(i,1), i--;
  }
  for(let i=0;i<bullets.length;i++) {
    for(let j=0;j<enemies.length;j++) {
      if(Math.hypot(bullets[i].x-enemies[j].x, bullets[i].y-enemies[j].y) < enemies[j].r+bullets[i].r) {
        enemies[j].hp--;
        bullets.splice(i,1); i--;
        if(enemies[j].hp<=0) { score+=10; enemies.splice(j,1); j--; }
        break;
      }
    }
  }
  for(let j=0;j<enemies.length;j++) {
    if(player.invincible===0 && Math.hypot(player.x-enemies[j].x, player.y-enemies[j].y) < player.r+enemies[j].r) {
      lives--;
      player.invincible = 60;
      enemies.splice(j,1); j--;
      updateUI();
      if(lives<=0) { gameRunning=false; document.getElementById('finalScore').innerText='Score: '+score; document.getElementById('gameOverScreen').classList.remove('hidden'); return; }
    }
  }
  if(score>0 && score%500<20) wave = Math.min(10, 1+Math.floor(score/500));
  ctx.fillStyle = '#05050a'; ctx.fillRect(0,0,W,H);
  ctx.fillStyle = '#0ff'; ctx.beginPath(); ctx.arc(player.x, player.y, player.r, 0, Math.PI*2); ctx.fill();
  for(let e of enemies) { ctx.fillStyle = '#f44'; ctx.beginPath(); ctx.arc(e.x,e.y,e.r,0,Math.PI*2); ctx.fill(); }
  for(let b of bullets) { ctx.fillStyle = '#ff0'; ctx.beginPath(); ctx.arc(b.x,b.y,b.r,0,Math.PI*2); ctx.fill(); }
  updateUI();
}
</script>
</body></html>"""

def build_wave_game():
    return SHARED_HEAD + """
<body>
<div id="game-container">
  <div class="hud"><div>💥 SCORE <span id="score">0</span></div><div>❤️ LIVES <span id="lives">5</span></div><div>🌊 WAVE <span id="wave">1</span></div></div>
  <canvas id="gameCanvas"></canvas>
  """ + start_screen() + """
  <div class="joystick-area"><div class="joystick-base"><div class="joystick-thumb"></div></div></div>
  <div class="action-buttons"><div class="action-btn" id="attackBtn">⚔️</div><div class="action-btn" id="specialBtn">💥</div></div>
</div>
<script>
""" + JOYSTICK_JS + """
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
let W, H, player, enemies, score, lives, wave, frame, specialCharge, gameRunning;
function resize() {
  const container = document.getElementById('game-container');
  const hud = document.querySelector('.hud');
  canvas.width = W = container.clientWidth;
  canvas.height = H = container.clientHeight - hud.clientHeight;
}
window.addEventListener('resize', resize);
resize();
function init() {
  player = { x: W/2, y: H/2, r: 18, speed: 4, invincible: 0, attackTimer: 0 };
  enemies = []; score = 0; lives = 5; wave = 1; frame = 0; specialCharge = 0;
  gameRunning = true;
  updateUI();
  requestAnimationFrame(gameLoop);
}
function startGame() { document.getElementById('startScreen').classList.add('hidden'); init(); }
function restartGame() { document.getElementById('gameOverScreen').classList.add('hidden'); init(); }
function updateUI() {
  document.getElementById('score').innerText = score;
  document.getElementById('lives').innerText = lives;
  document.getElementById('wave').innerText = wave;
}
function spawnWave() {
  let count = 3 + wave;
  for(let i=0;i<count;i++) {
    let ang = Math.random() * Math.PI * 2;
    let dist = Math.max(W,H) * 0.6;
    enemies.push({ x: W/2 + Math.cos(ang)*dist, y: H/2 + Math.sin(ang)*dist, r: 15+wave, hp: 1+Math.floor(wave/2), speed: 1+wave*0.1 });
  }
}
function attack() {
  if(player.attackTimer<=0) {
    player.attackTimer = 10;
    let range = 70;
    for(let i=0;i<enemies.length;i++) {
      if(Math.hypot(enemies[i].x-player.x, enemies[i].y-player.y) < range) {
        enemies[i].hp--;
        specialCharge = Math.min(100, specialCharge+10);
        if(enemies[i].hp<=0) { score+=10; enemies.splice(i,1); i--; }
      }
    }
    updateUI();
  }
}
function special() { if(specialCharge>=100){ specialCharge=0; enemies.forEach(e=>e.hp-=3); } }
document.getElementById('attackBtn').onclick = () => { if(gameRunning) attack(); };
document.getElementById('specialBtn').onclick = () => { if(gameRunning) special(); };
function gameLoop() {
  if(!gameRunning) return;
  requestAnimationFrame(gameLoop);
  frame++;
  if(player.attackTimer>0) player.attackTimer--;
  if(player.invincible>0) player.invincible--;
  let joy = joyActive ? {x:joyX, y:joyY} : getJoyFromKeys();
  player.x += joy.x * player.speed;
  player.y += joy.y * player.speed;
  player.x = Math.max(player.r, Math.min(W-player.r, player.x));
  player.y = Math.max(player.r, Math.min(H-player.r, player.y));
  if(enemies.length === 0) { wave++; spawnWave(); updateUI(); }
  specialCharge = Math.min(100, specialCharge+0.3);
  for(let e of enemies) {
    let ang = Math.atan2(player.y-e.y, player.x-e.x);
    e.x += Math.cos(ang) * e.speed;
    e.y += Math.sin(ang) * e.speed;
  }
  for(let j=0;j<enemies.length;j++) {
    if(player.invincible===0 && Math.hypot(player.x-enemies[j].x, player.y-enemies[j].y) < player.r+enemies[j].r) {
      lives--;
      player.invincible = 60;
      enemies.splice(j,1); j--;
      updateUI();
      if(lives<=0) { gameRunning=false; document.getElementById('finalScore').innerText='Score: '+score; document.getElementById('gameOverScreen').classList.remove('hidden'); return; }
    }
  }
  ctx.fillStyle = '#05050a'; ctx.fillRect(0,0,W,H);
  ctx.fillStyle = '#0ff'; ctx.beginPath(); ctx.arc(player.x, player.y, player.r, 0, Math.PI*2); ctx.fill();
  for(let e of enemies) { ctx.fillStyle = '#f44'; ctx.beginPath(); ctx.arc(e.x,e.y,e.r,0,Math.PI*2); ctx.fill(); }
  if(player.attackTimer>0) { ctx.strokeStyle = '#ff0'; ctx.lineWidth=3; ctx.beginPath(); ctx.arc(player.x,player.y,50,0,Math.PI*2); ctx.stroke(); }
  updateUI();
}
</script>
</body></html>"""

def build_platformer_game():
    return SHARED_HEAD + """
<body>
<div id="game-container">
  <div class="hud"><div>💥 SCORE <span id="score">0</span></div><div>❤️ LIVES <span id="lives">3</span></div><div>🪙 COINS</div></div>
  <canvas id="gameCanvas"></canvas>
  """ + start_screen() + """
  <div class="joystick-area"><div class="joystick-base"><div class="joystick-thumb"></div></div></div>
  <div class="action-buttons"><div class="action-btn" id="jumpBtn">⬆️</div><div class="action-btn" id="specialBtn">⚡</div></div>
</div>
<script>
""" + JOYSTICK_JS + """
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
let W, H, player, platforms, coins, score, lives, frame, gameRunning, specialCharge, cameraY;
const GRAV = 0.5, JUMP = -9;
function resize() {
  const container = document.getElementById('game-container');
  const hud = document.querySelector('.hud');
  canvas.width = W = container.clientWidth;
  canvas.height = H = container.clientHeight - hud.clientHeight;
}
window.addEventListener('resize', resize);
resize();
function init() {
  player = { x: W/2-15, y: H-100, w:30, h:30, vx:0, vy:0, onGround:false, invincible:0 };
  platforms = [{ x:0, y:H-20, w:W, h:20 }];
  for(let i=1;i<15;i++) {
    let y = H-20 - i*80 + Math.random()*30;
    let w = 80 + Math.random()*100;
    let x = Math.random() * (W-w);
    platforms.push({ x:x, y:y, w:w, h:15 });
  }
  coins = [];
  for(let p of platforms) {
    if(Math.random()<0.6) coins.push({ x:p.x+p.w/2, y:p.y-10, r:8, collected:false });
  }
  score = 0; lives = 3; frame = 0; specialCharge = 0; cameraY = 0;
  gameRunning = true;
  updateUI();
  requestAnimationFrame(gameLoop);
}
function startGame() { document.getElementById('startScreen').classList.add('hidden'); init(); }
function restartGame() { document.getElementById('gameOverScreen').classList.add('hidden'); init(); }
function updateUI() {
  document.getElementById('score').innerText = score;
  document.getElementById('lives').innerText = lives;
}
function jump() { if(player.onGround){ player.vy = JUMP; player.onGround = false; } }
function special() { if(specialCharge>=100){ specialCharge=0; player.vy = JUMP*1.5; player.invincible=60; } }
document.getElementById('jumpBtn').onclick = () => { if(gameRunning) jump(); };
document.getElementById('specialBtn').onclick = () => { if(gameRunning) special(); };
function gameLoop() {
  if(!gameRunning) return;
  requestAnimationFrame(gameLoop);
  frame++;
  if(player.invincible>0) player.invincible--;
  let joy = joyActive ? {x:joyX, y:joyY} : getJoyFromKeys();
  player.vx = joy.x * 4;
  player.vy += GRAV;
  player.x += player.vx;
  player.y += player.vy;
  player.onGround = false;
  player.x = Math.max(0, Math.min(W-player.w, player.x));
  for(let p of platforms) {
    if(player.x < p.x+p.w && player.x+player.w > p.x && player.y+player.h > p.y && player.y+player.h < p.y+p.h+Math.abs(player.vy) && player.vy >= 0) {
      player.y = p.y - player.h;
      player.vy = 0;
      player.onGround = true;
    }
  }
  if(player.y > H+200) {
    lives--;
    if(lives<=0) { gameRunning=false; document.getElementById('finalScore').innerText='Score: '+score; document.getElementById('gameOverScreen').classList.remove('hidden'); return; }
    player.x = W/2; player.y = H-100; player.vy = 0; player.invincible = 60;
    updateUI();
  }
  for(let i=0;i<coins.length;i++) {
    if(!coins[i].collected && Math.hypot(player.x+player.w/2 - coins[i].x, player.y+player.h/2 - coins[i].y) < coins[i].r+15) {
      coins[i].collected = true;
      score += 5;
      specialCharge = Math.min(100, specialCharge+10);
      updateUI();
    }
  }
  specialCharge = Math.min(100, specialCharge+0.2);
  cameraY = Math.max(0, player.y - H/2);
  ctx.fillStyle = '#05050a'; ctx.fillRect(0,0,W,H);
  ctx.save(); ctx.translate(0, -cameraY);
  for(let p of platforms) { ctx.fillStyle = '#888'; ctx.fillRect(p.x, p.y, p.w, p.h); }
  for(let c of coins) { if(!c.collected) { ctx.fillStyle = '#ff0'; ctx.beginPath(); ctx.arc(c.x,c.y,c.r,0,Math.PI*2); ctx.fill(); } }
  ctx.fillStyle = '#0ff'; ctx.fillRect(player.x, player.y, player.w, player.h);
  ctx.restore();
  updateUI();
}
</script>
</body></html>"""

def build_puzzle_game():
    return SHARED_HEAD + """
<body>
<div id="game-container">
  <div class="hud"><div>🔢 MOVES <span id="moves">0</span></div><div>🏆 BEST <span id="best">-</span></div></div>
  <canvas id="gameCanvas"></canvas>
  """ + start_screen() + """
</div>
<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
let W, H, N=4, board, blank, moves, best, gameRunning;
function resize() {
  const container = document.getElementById('game-container');
  const hud = document.querySelector('.hud');
  canvas.width = W = container.clientWidth;
  canvas.height = H = container.clientHeight - hud.clientHeight;
  if(gameRunning) draw();
}
window.addEventListener('resize', resize);
function init() {
  board = []; for(let i=0;i<N*N-1;i++) board.push(i+1); board.push(0);
  blank = { r: N-1, c: N-1 };
  moves = 0; best = localStorage.getItem('puzzleBest') || null;
  document.getElementById('best').innerText = best || '-';
  gameRunning = true;
  shuffle(200);
  draw();
}
function shuffle(step) {
  for(let i=0;i<step;i++) {
    let dirs = [[-1,0],[1,0],[0,-1],[0,1]];
    let valid = [];
    for(let d of dirs) {
      let nr = blank.r + d[0], nc = blank.c + d[1];
      if(nr>=0 && nr<N && nc>=0 && nc<N) valid.push(d);
    }
    if(valid.length) {
      let d = valid[Math.floor(Math.random()*valid.length)];
      move(d[0], d[1]);
    }
  }
  moves = 0; updateUI();
}
function move(dr, dc) {
  let nr = blank.r + dr, nc = blank.c + dc;
  if(nr<0 || nr>=N || nc<0 || nc>=N) return false;
  let idx1 = blank.r*N + blank.c, idx2 = nr*N + nc;
  [board[idx1], board[idx2]] = [board[idx2], board[idx1]];
  blank = { r: nr, c: nc };
  moves++;
  updateUI();
  return true;
}
function updateUI() { document.getElementById('moves').innerText = moves; }
function isSolved() {
  for(let i=0;i<N*N-1;i++) if(board[i] !== i+1) return false;
  return true;
}
function draw() {
  ctx.fillStyle = '#05050a'; ctx.fillRect(0,0,W,H);
  let tw = W/N, th = H/N;
  for(let r=0;r<N;r++) {
    for(let c=0;c<N;c++) {
      let val = board[r*N + c];
      if(val === 0) continue;
      let x = c*tw+2, y = r*th+2, w = tw-4, h = th-4;
      ctx.fillStyle = '#1a1a2e'; ctx.fillRect(x,y,w,h);
      ctx.fillStyle = '#0ff'; ctx.font = `bold ${Math.floor(tw*0.4)}px monospace`;
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(val, x+w/2, y+h/2);
    }
  }
}
canvas.addEventListener('click', (e) => {
  if(!gameRunning) return;
  let rect = canvas.getBoundingClientRect();
  let mx = (e.clientX - rect.left) * W / rect.width;
  let my = (e.clientY - rect.top) * H / rect.height;
  let c = Math.floor(mx / (W/N)), r = Math.floor(my / (H/N));
  let dr = r - blank.r, dc = c - blank.c;
  if((Math.abs(dr)+Math.abs(dc))===1) {
    move(dr, dc);
    draw();
    if(isSolved()) {
      gameRunning = false;
      if(!best || moves < parseInt(best)) localStorage.setItem('puzzleBest', moves);
      alert('Solved!');
      document.getElementById('finalScore').innerText = 'Solved in ' + moves + ' moves';
      document.getElementById('gameOverScreen').classList.remove('hidden');
    }
  }
});
canvas.addEventListener('touchstart', (e) => {
  e.preventDefault();
  let rect = canvas.getBoundingClientRect();
  let touch = e.touches[0];
  let mx = (touch.clientX - rect.left) * W / rect.width;
  let my = (touch.clientY - rect.top) * H / rect.height;
  let c = Math.floor(mx / (W/N)), r = Math.floor(my / (H/N));
  let dr = r - blank.r, dc = c - blank.c;
  if((Math.abs(dr)+Math.abs(dc))===1) {
    move(dr, dc);
    draw();
    if(isSolved()) {
      gameRunning = false;
      if(!best || moves < parseInt(best)) localStorage.setItem('puzzleBest', moves);
      alert('Solved!');
      document.getElementById('finalScore').innerText = 'Solved in ' + moves + ' moves';
      document.getElementById('gameOverScreen').classList.remove('hidden');
    }
  }
});
function startGame() { document.getElementById('startScreen').classList.add('hidden'); init(); }
function restartGame() { document.getElementById('gameOverScreen').classList.add('hidden'); init(); }
</script>
</body></html>"""

def build_racer_game():
    return SHARED_HEAD + """
<body>
<div id="game-container">
  <div class="hud"><div>🏁 DIST <span id="distance">0</span></div><div>💨 SPEED <span id="speed">0</span></div></div>
  <canvas id="gameCanvas"></canvas>
  """ + start_screen() + """
  <div class="joystick-area"><div class="joystick-base"><div class="joystick-thumb"></div></div></div>
  <div class="action-buttons"><div class="action-btn" id="boostBtn">🚀</div></div>
</div>
<script>
""" + JOYSTICK_JS + """
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
let W, H, car, obstacles, score, speed, boost, frame, gameRunning;
function resize() {
  const container = document.getElementById('game-container');
  const hud = document.querySelector('.hud');
  canvas.width = W = container.clientWidth;
  canvas.height = H = container.clientHeight - hud.clientHeight;
}
window.addEventListener('resize', resize);
resize();
function init() {
  car = { x: W/2, y: H-80, w:30, h:40 };
  obstacles = [];
  score = 0; speed = 3; boost = 0; frame = 0;
  gameRunning = true;
  updateUI();
  requestAnimationFrame(gameLoop);
}
function startGame() { document.getElementById('startScreen').classList.add('hidden'); init(); }
function restartGame() { document.getElementById('gameOverScreen').classList.add('hidden'); init(); }
function updateUI() {
  document.getElementById('distance').innerText = Math.floor(score);
  document.getElementById('speed').innerText = Math.floor(speed*10);
}
function boostFunc() { if(boost<=0) boost = 60; }
document.getElementById('boostBtn').onclick = () => { if(gameRunning) boostFunc(); };
function gameLoop() {
  if(!gameRunning) return;
  requestAnimationFrame(gameLoop);
  frame++;
  let joy = joyActive ? {x:joyX, y:joyY} : getJoyFromKeys();
  let effSpeed = speed + (boost>0 ? 5 : 0);
  if(boost>0) boost--;
  car.x += joy.x * 5;
  car.x = Math.max(car.w/2+20, Math.min(W-car.w/2-20, car.x));
  score += effSpeed * 0.1;
  speed = Math.min(12, 3 + frame/600);
  if(frame % Math.max(30, 60-Math.floor(speed*4)) === 0) {
    let x = Math.random() * (W-60) + 30;
    obstacles.push({ x:x, y:-30, w:40, h:40 });
  }
  for(let o of obstacles) o.y += effSpeed * 2;
  obstacles = obstacles.filter(o => o.y < H+50);
  for(let o of obstacles) {
    if(car.x < o.x+o.w && car.x+car.w > o.x && car.y < o.y+o.h && car.y+car.h > o.y) {
      gameRunning = false;
      document.getElementById('finalScore').innerText = 'Distance: '+Math.floor(score);
      document.getElementById('gameOverScreen').classList.remove('hidden');
    }
  }
  ctx.fillStyle = '#05050a'; ctx.fillRect(0,0,W,H);
  ctx.fillStyle = '#1a1a2e'; ctx.fillRect(W*0.2, 0, W*0.6, H);
  for(let i=0; i<H/50; i++) {
    ctx.fillStyle = '#0ff';
    ctx.fillRect(W/2-5, (i*50 + frame*effSpeed) % H, 10, 30);
  }
  ctx.fillStyle = '#0ff'; ctx.fillRect(car.x, car.y, car.w, car.h);
  for(let o of obstacles) { ctx.fillStyle = '#f44'; ctx.fillRect(o.x, o.y, o.w, o.h); }
  updateUI();
}
</script>
</body></html>"""

# ---------- DETERMINE GAME TYPE ----------
shooter_set = {"top-down shooter","survival horror","roguelite","extraction shooter","stealth game"}
racer_set = {"racing game"}
puzzle_set = {"puzzle game","cozy builder"}
plat_set = {"platformer","metroidvania"}
wave_set = {"fighting game","strategy game","tower defense","action RPG"}
if GENRE in shooter_set: GAME_TYPE = "shooter"
elif GENRE in racer_set: GAME_TYPE = "racer"
elif GENRE in puzzle_set: GAME_TYPE = "puzzle"
elif GENRE in plat_set: GAME_TYPE = "platformer"
elif GENRE in wave_set: GAME_TYPE = "wave"
else: GAME_TYPE = "shooter"

html5_game = eval(f"build_{GAME_TYPE}_game()")
print(f"  ✅ HTML5 game built ({GAME_TYPE}, {len(html5_game)//1024}KB)")

# ---------- WORKSPACE & ZIP ----------
proj_dir = Path(f"workspace/{SAFE_NAME}")
proj_dir.mkdir(parents=True, exist_ok=True)
(proj_dir / "index.html").write_text(html5_game, encoding="utf-8")
if sprite.exists(): shutil.copy(sprite, proj_dir / "icon.png")
(proj_dir / "project.godot").write_text(f'[application]\nconfig/name="{GAME_NAME}"\nconfig/icon="res://icon.png"\n')
(proj_dir / "README.md").write_text(f"# {GAME_NAME}\n\n**Genre:** {GENRE}\n**Mechanic:** {MECHANIC}\n\n{DESCRIPTION}\n\nPlay: {PLAY_URL}\nSource: {ZIP_URL}")
zip_path = Path("workspace/latest_game.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in proj_dir.rglob("*"):
        if f.is_file(): zf.write(f, f.relative_to(proj_dir.parent))
print(f"  ✅ ZIP: {zip_path.stat().st_size//1024}KB")

# Update portfolio status
cur = json.loads(port_path.read_text())
for g in cur:
    if g["game"] == GAME_NAME:
        g["art_success"] = art_ok
        g["status"] = "complete"
        g["game_type"] = GAME_TYPE
port_path.write_text(json.dumps(cur, indent=2))

# ---------- STOREFRONT (upgraded) ----------
print("  🌐 Generating upgraded storefront...")
storefront_html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DeathRoll Studio – Daily AI Games</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
  *{margin:0;padding:0;box-sizing:border-box;}
  body{background:#04040c;color:#d0d0f0;font-family:'Share Tech Mono',monospace;overflow-x:hidden;}
  body::before{content:'';position:fixed;inset:0;background-image:linear-gradient(rgba(0,255,204,0.015) 1px,transparent 1px),linear-gradient(90deg,rgba(0,255,204,0.015) 1px,transparent 1px);background-size:40px 40px;pointer-events:none;z-index:0;}
  .container{position:relative;z-index:1;max-width:1400px;margin:0 auto;padding:20px;}
  header{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;padding:20px 0;border-bottom:1px solid rgba(255,255,255,0.05);margin-bottom:32px;}
  .logo{font-family:'Orbitron',sans-serif;font-size:1.8rem;font-weight:900;background:linear-gradient(135deg,#fff,#00ffcc);-webkit-background-clip:text;background-clip:text;color:transparent;}
  .logo span{color:#00ffcc;background:none;}
  .nav a{color:#6a6a8a;text-decoration:none;margin-left:24px;font-size:0.8rem;letter-spacing:1px;transition:color 0.2s;}
  .nav a:hover{color:#00ffcc;}
  .live-badge{background:rgba(0,255,204,0.1);border:1px solid #00ffcc;color:#00ffcc;padding:4px 12px;border-radius:20px;font-size:0.7rem;}
  .hero{text-align:center;padding:60px 20px;background:radial-gradient(ellipse 70% 40% at 50% 0%,rgba(0,255,204,0.08),transparent);border-radius:32px;margin-bottom:40px;}
  .hero h1{font-family:'Orbitron',sans-serif;font-size:clamp(2rem,8vw,4rem);font-weight:900;background:linear-gradient(135deg,#fff,#00ffcc);-webkit-background-clip:text;background-clip:text;color:transparent;margin-bottom:16px;}
  .hero p{color:#6a6a8a;max-width:600px;margin:0 auto 24px;}
  .stats{display:flex;justify-content:center;gap:32px;flex-wrap:wrap;margin:32px 0;}
  .stat-card{background:rgba(255,255,255,0.02);backdrop-filter:blur(4px);border:1px solid rgba(255,255,255,0.05);border-radius:16px;padding:20px 32px;text-align:center;}
  .stat-number{font-family:'Orbitron',sans-serif;font-size:2.5rem;font-weight:900;color:#00ffcc;}
  .stat-label{font-size:0.7rem;letter-spacing:2px;color:#6a6a8a;}
  .games-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:24px;margin:40px 0;}
  .game-card{background:#0f0f20;border:1px solid rgba(255,255,255,0.05);border-radius:16px;overflow:hidden;transition:transform 0.2s,border-color 0.2s;}
  .game-card:hover{transform:translateY(-4px);border-color:#00ffcc;}
  .game-image{height:180px;background-size:cover;background-position:center;position:relative;}
  .game-badge{position:absolute;top:12px;left:12px;background:rgba(0,0,0,0.7);backdrop-filter:blur(4px);padding:4px 12px;border-radius:20px;font-size:0.7rem;color:#00ffcc;border:1px solid #00ffcc;}
  .game-info{padding:20px;}
  .game-name{font-family:'Orbitron',sans-serif;font-size:1.2rem;margin-bottom:4px;}
  .game-genre{color:#00ffcc;font-size:0.7rem;letter-spacing:1px;margin-bottom:12px;text-transform:uppercase;}
  .game-mechanic{background:rgba(0,255,204,0.1);display:inline-block;padding:4px 12px;border-radius:20px;font-size:0.7rem;margin-bottom:12px;}
  .game-desc{font-size:0.8rem;color:#6a6a8a;line-height:1.5;margin-bottom:16px;}
  .price{font-size:1.2rem;color:#00ffcc;font-weight:bold;}
  .game-date{font-size:0.6rem;color:#444;margin-top:12px;}
  .buy-section{background:#0a0a18;border-radius:24px;padding:40px;margin:40px 0;text-align:center;border:1px solid rgba(255,255,255,0.05);}
  .buy-section h2{font-family:'Orbitron',sans-serif;font-size:1.6rem;margin-bottom:24px;}
  .wallet-box{background:rgba(0,0,0,0.4);border-radius:16px;padding:20px;margin:20px auto;max-width:500px;word-break:break-all;font-family:monospace;font-size:0.7rem;}
  .wallet-row{display:flex;gap:12px;align-items:center;justify-content:center;margin:12px 0;}
  .btn{display:inline-block;background:#00ffcc;color:#000;padding:12px 28px;border-radius:40px;text-decoration:none;font-weight:bold;letter-spacing:1px;transition:opacity 0.2s;margin-top:16px;}
  .btn:hover{opacity:0.8;}
  footer{text-align:center;padding:32px 0;border-top:1px solid rgba(255,255,255,0.05);margin-top:40px;font-size:0.7rem;color:#6a6a8a;}
  @media(max-width:768px){.nav{display:none;}.stats{gap:16px;}.stat-card{padding:12px 20px;}}
</style>
</head>
<body>
<div class="container">
  <header>
    <div class="logo">DEATH<span>ROLL</span></div>
    <div class="nav"><a href="#games">GAMES</a><a href="#buy">BUY</a><a href="https://t.me/drolltech" target="_blank">TELEGRAM</a></div>
    <div class="live-badge">● LIVE DAILY</div>
  </header>
  <div class="hero">
    <h1>NEW MOBILE GAME<br>EVERY DAY</h1>
    <p>AI‑generated mechanics, unique art, and full source code – all playable in your browser.<br>Own the game for <span id="priceDisplay">7</span> SOL.</p>
    <div class="stats" id="stats"><div class="stat-card"><div class="stat-number" id="totalGames">-</div><div class="stat-label">GAMES</div></div><div class="stat-card"><div class="stat-number" id="totalGenres">-</div><div class="stat-label">GENRES</div></div><div class="stat-card"><div class="stat-number" id="latestDate">-</div><div class="stat-label">LATEST</div></div></div>
  </div>
  <div class="games-grid" id="gamesGrid"><div class="stat-card">Loading games...</div></div>
  <div class="buy-section" id="buy"><h2>⚡ GET FULL SOURCE CODE</h2><p>Send <strong id="buyPrice">7</strong> SOL to either wallet below, then DM <strong>@deathroll1</strong> with your @username.<br>You'll receive the complete Godot 4 project + HTML5 build + license key instantly.</p>
  <div class="wallet-box"><div class="wallet-row">🔵 <strong>Trust Wallet (Solana)</strong><br><code>6wsQ6nGXrUUUGCEokb4rZcfHDv2a8MomUb22TuVaH2m3</code></div><div class="wallet-row">🟣 <strong>Phantom Wallet (Solana)</strong><br><code>Csk9DKstWMdKx19gUHWB9xy2VwZZX2nx6V6oSVGDCgMb</code></div></div>
  <a href="https://t.me/deathroll1" class="btn" target="_blank">📩 DM @deathroll1</a></div>
  <footer><p>© 2025 DeathRoll Studio — Automated Game Factory v30.0</p><p>Built with AI & Solana | <a href="https://t.me/drolltech" style="color:#00ffcc;">Join Telegram</a></p></footer>
</div>
<script>
async function loadGames(){try{const res=await fetch('portfolio.json?t='+Date.now());if(!res.ok)throw new Error();let games=await res.json();if(!Array.isArray(games))games=[];games.sort((a,b)=>new Date(b.date)-new Date(a.date));document.getElementById('totalGames').innerText=games.length;document.getElementById('totalGenres').innerText=new Set(games.map(g=>g.genre)).size;document.getElementById('latestDate').innerText=games[0]?new Date(games[0].date).toLocaleDateString():'-';const price=games[0]?.price_sol||'7';document.getElementById('priceDisplay').innerText=price;document.getElementById('buyPrice').innerText=price;const grid=document.getElementById('gamesGrid');grid.innerHTML=games.slice(0,20).map(g=>`<div class="game-card"><div class="game-image" style="background-image:url('${g.image_url||''}');background-color:#111;"><div class="game-badge">${escapeHtml(g.genre||'?')}</div></div><div class="game-info"><div class="game-name">${escapeHtml(g.game)}</div><div class="game-genre">${escapeHtml(g.genre)}</div><div class="game-mechanic">⚡ ${escapeHtml(g.mechanic)}</div><div class="game-desc">${escapeHtml(g.description||g.mech_desc||'')}</div><div class="price">💰 ${g.price_sol||price} SOL</div><div class="game-date">📅 ${new Date(g.date).toLocaleDateString()}</div><a href="${g.play_url||'#'}" target="_blank" style="display:inline-block;margin-top:12px;color:#00ffcc;font-size:0.7rem;">▶ Play Free</a></div></div>`).join('');if(!games.length)grid.innerHTML='<div class="stat-card">No games yet. First game will appear at 6AM UTC tomorrow.</div>';}catch(e){document.getElementById('gamesGrid').innerHTML='<div class="stat-card">⚠️ Error loading games. Check back soon.</div>';}}
function escapeHtml(str){if(!str)return '';return str.replace(/[&<>]/g,m=>{if(m==='&')return '&amp;';if(m==='<')return '&lt;';if(m==='>')return '&gt;';return m;});}
loadGames();setInterval(loadGames,60000);
</script>
</body>
</html>'''
Path("index.html").write_text(storefront_html, encoding="utf-8")
print("  ✅ Storefront updated")

# ---------- TELEGRAM POST (safe HTML) ----------
sales_post = f"""
<b>{EMOJI_STR} {HOOK} {EMOJI_STR}</b>

✨ <b>{GAME_NAME}</b> — {GENRE}
<i>{DESCRIPTION}</i>

⚡ <b>Mechanic:</b> <code>{MECHANIC}</code>
🕹️ <b>Play FREE:</b> {PLAY_URL}

💰 <b>Full source:</b> ${GAME_PRICE} SOL
🔵 Trust: <code>{SOLANA_TRUST}</code>
🟣 Phantom: <code>{SOLANA_PHANTOM}</code>

Send ${GAME_PRICE} SOL + @username → instant delivery

{TAGS}
""".strip()

if TG_TOKEN and sprite.exists():
    print(f"  📤 Sending to channel {TELEGRAM_CHANNEL}...")
    ok = tg_send_photo(TELEGRAM_CHANNEL, sprite, sales_post)
    if ok:
        print("  ✅ Channel post sent")
    else:
        print("  ❌ Channel post failed. Ensure bot is admin in channel.")
else:
    print("  ⚠️  Missing TG_TOKEN or sprite.png")

if TG_TOKEN and TG_ADMIN and zip_path.exists():
    admin_caption = f"<b>🎮 {GAME_NAME}</b> — {GAME_TYPE}<br>Genre: {GENRE}<br>Mechanic: {MECHANIC}<br>Art: {'✅' if art_ok else '⚠️'}<br>Key: <code>{LICENSE_KEY}</code>"
    tg_send_doc(TG_ADMIN, zip_path, admin_caption)
    print("  ✅ Admin bundle sent")

if WHATSAPP_WEBHOOK_URL:
    send_to_whatsapp(f"🎮 NEW GAME: {GAME_NAME} ({GENRE})\n{MECHANIC}\n{DESCRIPTION}\nPlay: {PLAY_URL}\n{GAME_PRICE} SOL", IMG_URL)
    print("  ✅ WhatsApp sent")

# ---------- SAR ----------
SAR["study"]["total_runs"] += 1
if art_ok: SAR["study"]["art_ok"] += 1
else: SAR["study"]["art_fail"] += 1
SAR["study"]["games"].append({"name": GAME_NAME, "genre": GENRE, "mechanic": MECHANIC, "art": art_ok, "ts": datetime.now().isoformat()})
SAR["study"]["games"] = SAR["study"]["games"][-100:]
genre_stats = {}
for g in SAR["study"]["games"]:
    gn = g["genre"]
    genre_stats.setdefault(gn, {"count":0, "art":0})
    genre_stats[gn]["count"] += 1
    if g.get("art"): genre_stats[gn]["art"] += 1
if genre_stats:
    SAR["analysis"]["best_genre"] = max(genre_stats, key=lambda x: genre_stats[x]["art"]/max(genre_stats[x]["count"],1))
    SAR["analysis"]["rate"] = round(SAR["study"]["art_ok"]/max(SAR["study"]["total_runs"],1),3)
sar_path.write_text(json.dumps(SAR, indent=2))
Path("learning_data.json").write_text(json.dumps({"ts": datetime.now().isoformat(), "game": GAME_NAME, "genre": GENRE, "mechanic": MECHANIC, "art_ok": art_ok, "total_games": len(entries)}))
Path("last_run.txt").write_text(datetime.now().isoformat())

print("\n╔══════════════════════════════════════════════════════╗")
print("║  ✅  DEATHROLL STUDIO v30.0  —  COMPLETE            ║")
print(f"║  Game    : {GAME_NAME:<41}║")
print(f"║  Genre   : {GENRE:<41}║")
print(f"║  Mechanic: {MECHANIC:<41}║")
print("╚══════════════════════════════════════════════════════╝")
print(f"  🌐 {BASE_URL}/")
print(f"  📱 https://t.me/{TELEGRAM_CHANNEL.lstrip('@')}")
