#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║         DEATHROLL STUDIO  v30.0  —  TITAN EDITION           ║
║  Automated Mobile-First Game Factory  |  100% Free Stack    ║
║  OpenAI GPT-4o-mini  |  Auto-Delivery  |  Multi-Genre      ║
╚══════════════════════════════════════════════════════════════╝

WHAT THIS BOT DOES (every day at 6 AM UTC via GitHub Actions):
  1. Fetches real-time trends from Reddit r/gamedev & r/indiegaming
  2. Uses OpenAI gpt-4o-mini to generate unique mechanic + description
  3. Generates 512×512 game art via Pollinations.ai (free)
  4. Builds a COMPLETE, MOBILE-PLAYABLE HTML5 game
     — Full touch controls (joystick + tap buttons)
     — Portrait & landscape responsive
     — Works on any smartphone browser
  5. Packages Godot project + HTML5 + README as ZIP
  6. Posts to Telegram channel with viral hook + buy info
  7. Updates portfolio.json + index.html storefront
  8. Auto-delivers to buyers who've paid SOL (via /deliver command)
  9. Updates SAR self-learning system
 10. Commits everything back to GitHub → GitHub Pages goes live

SECRETS REQUIRED (GitHub → Settings → Secrets → Actions):
  TELEGRAM_BOT_TOKEN  — your bot token from @BotFather
  TELEGRAM_CHAT_ID    — your admin chat ID (get from @userinfobot)
  OPENAI_API_KEY      — from platform.openai.com (gpt-4o-mini is cheapest)
  GH_TOKEN            — GitHub Personal Access Token (repo scope)
  GAME_PRICE          — price in SOL (default: 7)
"""

import os, json, random, requests, shutil, zipfile, hashlib, time
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter
    PIL_OK = True
except ImportError:
    PIL_OK = False

# ═══════════════════════════════════════════════════════════
#  BRAND CONFIG
# ═══════════════════════════════════════════════════════════
BOT_VERSION       = "30.0.0"
BRAND_NAME        = "DeathRoll"
BRAND_GITHUB      = "favouradeleke246-maker"
BRAND_REPO        = "FACTORY-BOT-V4"
BRAND_WEBSITE     = "https://deathroll.co"
BRAND_TELEGRAM    = "@deathroll1"
BRAND_TIKTOK      = "@deathroll.co"
TELEGRAM_CHANNEL  = "@drolltech"
SOLANA_TRUST      = "6wsQ6nGXrUUUGCEokb4rZcfHDv2a8MomUb22TuVaH2m3"
SOLANA_PHANTOM    = "Csk9DKstWMdKx19gUHWB9xy2VwZZX2nx6V6oSVGDCgMb"

BASE_URL  = f"https://{BRAND_GITHUB}.github.io/{BRAND_REPO}"
RAW_URL   = f"https://raw.githubusercontent.com/{BRAND_GITHUB}/{BRAND_REPO}/main"

# ═══════════════════════════════════════════════════════════
#  ENVIRONMENT SECRETS
# ═══════════════════════════════════════════════════════════
TG_TOKEN   = os.getenv("TELEGRAM_BOT_TOKEN")
TG_ADMIN   = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GH_TOKEN   = os.getenv("GH_TOKEN")
GAME_PRICE = os.getenv("GAME_PRICE", "7")

print("╔══════════════════════════════════════════════════════╗")
print(f"║  DEATHROLL STUDIO v{BOT_VERSION}  —  TITAN EDITION     ║")
print("╚══════════════════════════════════════════════════════╝")
print(f"  Telegram : {'✅' if TG_TOKEN else '❌ MISSING'}")
print(f"  OpenAI   : {'✅' if OPENAI_KEY  else '⚠️  Using fallbacks'}")
print(f"  GitHub   : {'✅' if GH_TOKEN else '⚠️  No repo creation'}")
print(f"  Price    : {GAME_PRICE} SOL")
print()

# ═══════════════════════════════════════════════════════════
#  OPENAI  (gpt-4o-mini — cheapest + widely available)
# ═══════════════════════════════════════════════════════════
def call_openai(prompt: str, max_tokens: int = 200, system: str = "") -> str | None:
    if not OPENAI_KEY:
        return None
    payload: dict = {
        "model": "gpt-4o-mini",
        "max_tokens": max_tokens,
        "messages": ([{"role":"system","content":system}] if system else []) + [{"role":"user","content":prompt}],
    }
    try:
        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_KEY}",

                "content-type":      "application/json",
            },
            json=payload,
            timeout=40,
        )
        if r.status_code == 200:
            return r.json()["content"][0]["text"].strip().strip('"')
        print(f"  ⚠️  OpenAI {r.status_code}: {r.text[:120]}")
    except Exception as e:
        print(f"  ⚠️  OpenAI error: {e}")
    return None

# ═══════════════════════════════════════════════════════════
#  TELEGRAM HELPERS
# ═══════════════════════════════════════════════════════════
TG_BASE = f"https://api.telegram.org/bot{TG_TOKEN}" if TG_TOKEN else ""

def tg_send_photo(chat_id, photo_path, caption):
    if not TG_TOKEN: return False
    try:
        with open(photo_path, "rb") as f:
            r = requests.post(f"{TG_BASE}/sendPhoto",
                files={"photo": f},
                data={"chat_id": chat_id, "caption": caption,
                      "parse_mode": "Markdown"}, timeout=40)
        return r.status_code == 200
    except: return False

def tg_send_doc(chat_id, doc_path, caption):
    if not TG_TOKEN: return False
    try:
        with open(doc_path, "rb") as f:
            r = requests.post(f"{TG_BASE}/sendDocument",
                files={"document": f},
                data={"chat_id": chat_id, "caption": caption,
                      "parse_mode": "Markdown"}, timeout=90)
        return r.status_code == 200
    except: return False

def tg_send_message(chat_id, text):
    if not TG_TOKEN: return False
    try:
        r = requests.post(f"{TG_BASE}/sendMessage",
            data={"chat_id": chat_id, "text": text,
                  "parse_mode": "Markdown"}, timeout=20)
        return r.status_code == 200
    except: return False

# ═══════════════════════════════════════════════════════════
#  GENRE SYSTEM  (14 genres, smart emoji mapping)
# ═══════════════════════════════════════════════════════════
GENRES = {
    "top-down shooter":   {"emojis": ["🔫","💥","🎯"], "color": "#ff4444", "bg": "#0d0005"},
    "action RPG":         {"emojis": ["⚔️","🛡️","👑"],  "color": "#ffd700", "bg": "#0a0800"},
    "racing game":        {"emojis": ["🏎️","💨","🔥"],  "color": "#00cfff", "bg": "#000a10"},
    "puzzle game":        {"emojis": ["🧩","💡","🔮"],  "color": "#b44fff", "bg": "#08000d"},
    "survival horror":    {"emojis": ["😱","💀","👻"],  "color": "#33ff99", "bg": "#000d04"},
    "fighting game":      {"emojis": ["👊","💥","⚡"],  "color": "#ff6600", "bg": "#0d0400"},
    "strategy game":      {"emojis": ["♟️","🧠","🏰"],  "color": "#4488ff", "bg": "#00040d"},
    "roguelite":          {"emojis": ["🎲","⚡","💀"],  "color": "#ff44aa", "bg": "#0d0008"},
    "platformer":         {"emojis": ["🦘","⭐","🎮"],  "color": "#ffcc00", "bg": "#0a0800"},
    "stealth game":       {"emojis": ["🕵️","🌑","🔪"],  "color": "#88ccff", "bg": "#000508"},
    "extraction shooter": {"emojis": ["🔫","💰","🚁"],  "color": "#ff8800", "bg": "#0d0600"},
    "cozy builder":       {"emojis": ["🏡","🌸","✨"],  "color": "#ff99cc", "bg": "#0a0006"},
    "tower defense":      {"emojis": ["🏰","💣","🛡️"],  "color": "#44ffbb", "bg": "#000d07"},
    "metroidvania":       {"emojis": ["🗺️","🔑","⚔️"],  "color": "#cc88ff", "bg": "#06000d"},
}

# ═══════════════════════════════════════════════════════════
#  NAME POOL  (1200+ combinations)
# ═══════════════════════════════════════════════════════════
PREFIXES = [
    "Neon","Cyber","Quantum","Astral","Void","Echo","Flux","Rogue",
    "Crimson","Shadow","Phantom","Eclipse","Solar","Nova","Iron","Dark",
    "Storm","Hyper","Apex","Omega","Zenith","Vortex","Blaze","Frost",
    "Titan","Ghost","Pulse","Arc","Rift","Chrome","Surge","Static",
    "Aether","Binary","Carbon","Delta","Ember","Forge","Glitch","Helix",
    "Inferno","Jade","Kinetic","Lunar","Magma","Nexus","Obsidian","Prism",
    "Quasar","Radiant","Sonic","Turbo","Ultra","Vapor","Warp","Xenon",
    "Amber","Blitz","Cobalt","Dusk","Enigma","Fractal","Glacial","Hex",
    "Ionic","Jinx","Krypto","Lancer","Mirage","Null","Optic","Pixel",
    "Quake","Reaper","Scarlet","Thorn","Umbra","Venom","Wraith","Xeno",
    "Yearn","Zeal","Abyssal","Brutal","Caustic","Desolate","Eternal",
    "Feral","Grim","Hollow","Ironskin","Jagged","Kel","Lethal","Molten",
]

SUFFIXES = [
    "Runner","Drifter","Breach","Vector","Pulse","Shift","Core","Edge",
    "Zone","Realm","Fury","Strike","Blade","Force","Maze","Hunt",
    "War","Fall","Rise","Gate","Lab","Ops","Shard","Crash",
    "Dash","Drive","Fight","Grid","Hook","Impact","Jump","Kill",
    "Lock","March","Nexus","Orbit","Path","Quest","Race","Siege",
    "Tank","Vault","Wing","Arena","Base","Chain","Dome","Echo",
    "Field","Gloom","Haze","Isle","Jungle","Keep","Loop","Mire",
    "Outpost","Peak","Ridge","Spire","Trail","Waste","Expanse","Abyss",
    "Citadel","Den","Expanse","Front","Gulch","Hollow","Iris","Jaw",
    "Knell","Lore","Mark","Night","Omen","Pyre","Ruin","Shroud",
    "Tomb","Undertow","Vale","Wreck","Xenith","Yonder","Zenith","Deep",
]

MECHANICS_FALLBACK = [
    ("Phase Echo",       "Tap to leave a ghost clone — enemies attack it instead of you"),
    ("Chrono Fracture",  "Hold to freeze all enemies in a 3-second time bubble"),
    ("Void Step",        "Double-tap to teleport through any obstacle once per 4 seconds"),
    ("Mirror Shell",     "Absorb one hit and reflect triple damage back at attacker"),
    ("Gravity Well",     "Pull all enemies toward your cursor/finger with a singularity"),
    ("Soul Link",        "Link to an enemy — you share health, so use them as a shield"),
    ("Signal Jam",       "Disable all enemy projectiles for 3 seconds with an EMP burst"),
    ("Death Bloom",      "Near-death triggers a massive radial shockwave instantly"),
    ("Echo Strike",      "Every attack automatically repeats 0.8s later for free"),
    ("Fracture Line",    "Draw a line — anything that crosses it takes 3x damage"),
    ("Null Field",       "Drop a zone where no enemy abilities or bullets work"),
    ("Chain Spark",      "Hit one enemy and lightning chains instantly to 4 others"),
    ("Bleed Aura",       "Moving fast leaves a damage trail that hurts anything following"),
    ("Inverted Shield",  "Your shield deals damage — the harder you're hit, the more you deal"),
    ("Time Anchor",      "Mark your position; one button warps you back to it at any moment"),
    ("Overclock",        "Speed boost so extreme enemies appear frozen — lasts 2 seconds"),
    ("Phantom Rush",     "A ghost version of you rushes forward, triggering all traps safely"),
    ("Collapse Wave",    "Every 10 kills trigger a screen-wide collapse dealing massive damage"),
]

HOOKS = [
    "This game will haunt you 🔥",
    "I built this in 24 hours",
    "Your next obsession just dropped",
    "Run. Or die trying",
    "1000 IQ moves only",
    "Speed meets absolute chaos",
    "One mechanic. Infinite depth",
    "Can you survive this?",
    "Most intense drop this week",
    "This one hits completely different",
    "No one is ready for this mechanic",
    "Built different. Plays different",
    "The game that broke my brain",
    "Indie gold just dropped",
    "You've never played anything like this",
]

# ═══════════════════════════════════════════════════════════
#  SAR SYSTEM  (Study → Analyse → React)
# ═══════════════════════════════════════════════════════════
sar_path = Path("sar_analysis.json")
SAR: dict = {
    "study":    {"total_runs": 0, "art_ok": 0, "art_fail": 0, "sales": 0, "games": []},
    "analysis": {"best_genre": None, "best_mechanic": None, "rate": 0.0, "top_hooks": []},
    "feedback": {},
}
if sar_path.exists():
    try:
        d = json.loads(sar_path.read_text())
        for k in SAR: SAR[k].update(d.get(k, {}))
        print(f"  📊 SAR: {SAR['study']['total_runs']} runs | "
              f"{SAR['study']['sales']} sales | "
              f"best genre: {SAR['analysis']['best_genre'] or 'TBD'}")
    except: pass

# ═══════════════════════════════════════════════════════════
#  REAL-TIME TRENDS
# ═══════════════════════════════════════════════════════════
def fetch_trends() -> list[str]:
    found = []
    for sub in ["gamedev", "indiegaming"]:
        try:
            r = requests.get(
                f"https://www.reddit.com/r/{sub}/top.json?limit=30&t=day",
                headers={"User-Agent": "DeathRollStudio/3.0"}, timeout=10)
            if r.status_code == 200:
                posts = r.json().get("data", {}).get("children", [])
                text  = " ".join(p["data"]["title"].lower() for p in posts)
                kws   = ["action","platformer","puzzle","rpg","strategy","horror",
                         "shooter","roguelike","survival","racing","stealth","fighting"]
                for k in kws:
                    if k in text and k not in found:
                        found.append(k)
        except: pass
    return found[:3]

print("  🌍 Fetching trends...")
trends = fetch_trends()
print(f"  🔥 Trending: {trends or ['none — using SAR']}")

# ═══════════════════════════════════════════════════════════
#  GENRE SELECTION  (trend + SAR weighted)
# ═══════════════════════════════════════════════════════════
candidates = []
for t in trends:
    match = next((g for g in GENRES if t in g), None)
    if match: candidates.append(match)
if SAR["analysis"].get("best_genre"):
    candidates.append(SAR["analysis"]["best_genre"])
candidates.append(random.choice(list(GENRES.keys())))

GENRE     = random.choice(candidates)
G_COLOR   = GENRES[GENRE]["color"]
G_BG      = GENRES[GENRE]["bg"]
G_EMOJIS  = GENRES[GENRE]["emojis"]
EMOJI_STR = " ".join(random.sample(G_EMOJIS, len(G_EMOJIS)))
print(f"  🎮 Genre: {GENRE}  ({EMOJI_STR})")

# ═══════════════════════════════════════════════════════════
#  AI MECHANIC
# ═══════════════════════════════════════════════════════════
print("  ⚙️  Generating mechanic...")
def gen_mechanic() -> tuple[str, str]:
    if OPENAI_KEY:
        res = call_openai(
            f"Invent one UNIQUE, surprising game mechanic for a mobile {GENRE} game.\n"
            f"It must work well with TOUCH controls (tap, swipe, hold).\n"
            f"Reply EXACTLY:\nMECHANIC: <short name 2-4 words>\n"
            f"DESCRIPTION: <one punchy sentence max 18 words describing what it does>",
            max_tokens=100,
            system="You are a genius indie game designer. Be creative and unexpected."
        )
        if res:
            name = desc = None
            for line in res.splitlines():
                if line.startswith("MECHANIC:"):    name = line.split(":",1)[1].strip()
                elif line.startswith("DESCRIPTION:"): desc = line.split(":",1)[1].strip()
            if name and desc and 2 < len(name) < 40:
                return name, desc
    return random.choice(MECHANICS_FALLBACK)

MECHANIC, MECH_DESC = gen_mechanic()
print(f"  ✨ {MECHANIC} — {MECH_DESC}")

# ═══════════════════════════════════════════════════════════
#  GAME NAME  (1200+ combos, remembers last 50)
# ═══════════════════════════════════════════════════════════
names_file = Path("recent_game_names.json")
recent: list = []
if names_file.exists():
    try: recent = json.loads(names_file.read_text())
    except: pass

def unique_name() -> str:
    pool = {n.lower() for n in recent}
    for _ in range(300):
        n = f"{random.choice(PREFIXES)} {random.choice(SUFFIXES)}"
        if n.lower() not in pool: return n
    return f"{random.choice(PREFIXES)} {random.choice(SUFFIXES)} {random.randint(2,99)}"

GAME_NAME = unique_name()
recent.append(GAME_NAME)
names_file.write_text(json.dumps(recent[-50:]))
SAFE_NAME = GAME_NAME.replace(" ", "_")
PLAY_URL  = f"{BASE_URL}/workspace/{SAFE_NAME}/index.html"
IMG_URL   = f"{RAW_URL}/workspace/{SAFE_NAME}/icon.png"
ZIP_URL   = f"{RAW_URL}/workspace/latest_game.zip"
print(f"  🎯 Name: {GAME_NAME}")

# ═══════════════════════════════════════════════════════════
#  AI DESCRIPTION
# ═══════════════════════════════════════════════════════════
def gen_description() -> str:
    if OPENAI_KEY:
        res = call_openai(
            f"Write ONE thrilling sentence (max 110 chars) for a mobile {GENRE} "
            f"game called '{GAME_NAME}' featuring '{MECHANIC}'. "
            f"Sound exciting, edgy, like a trailer tagline. No quotes.",
            max_tokens=60,
            system="You write killer indie game marketing copy."
        )
        if res and len(res) > 15: return res[:120]
    return f"Master {MECHANIC} in this {GENRE} — no two sessions are the same."

DESCRIPTION = gen_description()
HOOK        = random.choice(HOOKS)
TAGS        = (f"#gamedev #indiegame #mobilegame #{GENRE.replace(' ','').replace('-','')}"
               f" #{MECHANIC.replace(' ','')} #DeathRollStudio #solanagaming #playtoearn")
print(f"  📝 {DESCRIPTION}")

# ═══════════════════════════════════════════════════════════
#  LICENSE KEY  (unique per game)
# ═══════════════════════════════════════════════════════════
seed = f"{GAME_NAME}{datetime.now().date()}{SOLANA_TRUST}"
LICENSE_KEY = "DR-" + hashlib.md5(seed.encode()).hexdigest()[:16].upper()

# ═══════════════════════════════════════════════════════════
#  PORTFOLIO  — save immediately
# ═══════════════════════════════════════════════════════════
port_path = Path("portfolio.json")
entries: list = []
if port_path.exists():
    try:
        raw = port_path.read_text().strip()
        if raw: entries = json.loads(raw)
        if not isinstance(entries, list): entries = []
    except: entries = []

entry = {
    "id":          f"game_{len(entries)+1:04d}",
    "date":        datetime.now().isoformat(),
    "game":        GAME_NAME,
    "genre":       GENRE,
    "mechanic":    MECHANIC,
    "mech_desc":   MECH_DESC,
    "description": DESCRIPTION,
    "hook":        HOOK,
    "hashtags":    TAGS,
    "image_url":   IMG_URL,
    "play_url":    PLAY_URL,
    "zip_url":     ZIP_URL,
    "price_sol":   GAME_PRICE,
    "license_key": LICENSE_KEY,
    "color":       G_COLOR,
    "sales":       0,
    "status":      "generating",
}
entries.append(entry)
entries = entries[-300:]
port_path.write_text(json.dumps(entries, indent=2))
print(f"  💾 Portfolio: {len(entries)} games")

with open("games_log.txt", "a") as f:
    f.write(f"{datetime.now().isoformat()} | {GAME_NAME} | {GENRE} | {MECHANIC}\n")

# ═══════════════════════════════════════════════════════════
#  ART GENERATION  (Pollinations free API)
# ═══════════════════════════════════════════════════════════
print("  🎨 Generating art...")
sprite = Path("sprite.png")
art_ok = False

styles = [
    "isometric 3D render with dramatic neon lighting",
    "dark cyberpunk concept art, ultra detailed",
    "low-poly 3D character, game-ready, moody lighting",
    "cell-shaded game art, bold outlines, vibrant",
    "dark fantasy concept art, cinematic",
    "retro-futuristic sci-fi illustration",
    "gritty noir game poster style",
    "hyper-detailed 3D render, unreal engine style",
]
style   = random.choice(styles)
art_pmt = (f"{style}, {GENRE} game character for '{GAME_NAME}', "
           f"professional game art, dark background, dramatic")

try:
    enc = art_pmt.replace(" ","+").replace(",","%2C").replace("'","%27")
    url = f"https://image.pollinations.ai/prompt/{enc}?width=512&height=512&seed={random.randint(1,999999)}&nologo=true"
    r   = requests.get(url, timeout=40)
    if r.status_code == 200 and len(r.content) > 8000:
        sprite.write_bytes(r.content)
        art_ok = True
        print(f"  ✅ Art: {style[:40]}...")
except Exception as e:
    print(f"  ⚠️  Pollinations: {e}")

if not art_ok and PIL_OK:
    from PIL import ImageFont
    img   = Image.new("RGB", (512, 512), (10, 5, 20))
    draw  = ImageDraw.Draw(img)
    # Scanline bg
    for y in range(0, 512, 4):
        alpha = int(40 * (1 - abs(y-256)/256))
        draw.line([(0,y),(512,y)], fill=(0, int(G_COLOR[3:5],16)//4,
                                         int(G_COLOR[5:7],16)//4))
    # Hexagonal grid pattern
    r_hex, cx, cy = 30, 256, 256
    for row in range(-6, 7):
        for col in range(-6, 7):
            hx = cx + col * r_hex * 1.732
            hy = cy + row * r_hex * 2 + (col % 2) * r_hex
            pts = [(hx + r_hex*0.8 * (0 if i%2==0 else 1) *
                    (1 if i<3 else -1), hy) for i in range(6)]
            # Simplified hex outline
            draw.regular_polygon(((hx, hy), r_hex-2), 6,
                                  outline=(*bytes.fromhex(G_COLOR[1:]), 60), fill=None)
    # Glow rings
    for rad in [180, 140, 100, 60]:
        clr = bytes.fromhex(G_COLOR[1:])
        draw.ellipse([cx-rad, cy-rad, cx+rad, cy+rad],
                     outline=(*clr, max(20, 80-(180-rad)//2)), width=2)
    # Center diamond
    pts = [(cx, cy-80),(cx+70, cy),(cx, cy+80),(cx-70, cy)]
    draw.polygon(pts, fill=(*bytes.fromhex(G_COLOR[1:]), 180))
    draw.polygon(pts, outline=(255,255,255,200), width=2)
    # Text
    draw.text((cx, cy-130), GAME_NAME, fill=(255,255,255), anchor="mm")
    draw.text((cx, cy+110), GENRE.upper(), fill=(*bytes.fromhex(G_COLOR[1:]),),
              anchor="mm")
    draw.text((cx, cy+140), f"⚡ {MECHANIC}", fill=(200,200,200), anchor="mm")
    draw.text((10, 500), "DeathRoll Studio", fill=(100,100,100))
    img.save(sprite)
    art_ok = True
    print("  ✅ Fallback art generated")

# ═══════════════════════════════════════════════════════════
#  HTML5 MOBILE GAME  — Full touch controls
#  Genre-adaptive gameplay:
#    shooter/horror/roguelite  → twin-stick shooter
#    racing                    → tilt/swipe racer
#    puzzle                    → sliding block puzzle
#    platformer/action RPG     → side-scroller
#    fighting/strategy         → wave-defense
#    default                   → arena shooter
# ═══════════════════════════════════════════════════════════
print("  🕹️  Building HTML5 mobile game...")

SHOOTER_GENRES = {"top-down shooter","survival horror","roguelite","extraction shooter","stealth game"}
RACER_GENRES   = {"racing game"}
PUZZLE_GENRES  = {"puzzle game","cozy builder"}
PLAT_GENRES    = {"platformer","metroidvania"}
WAVE_GENRES    = {"fighting game","strategy game","tower defense","action RPG"}

if   GENRE in SHOOTER_GENRES: GAME_TYPE = "shooter"
elif GENRE in RACER_GENRES:   GAME_TYPE = "racer"
elif GENRE in PUZZLE_GENRES:  GAME_TYPE = "puzzle"
elif GENRE in PLAT_GENRES:    GAME_TYPE = "platformer"
elif GENRE in WAVE_GENRES:    GAME_TYPE = "wave"
else:                          GAME_TYPE = "shooter"

print(f"  🎲 Game type: {GAME_TYPE}")

# ── Common CSS + Joystick JS shared by all game types ──────
SHARED_HEAD = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<title>{GAME_NAME}</title>
<style>
:root{{
  --acc:  {G_COLOR};
  --bg:   {G_BG};
  --dark: #050505;
  --txt:  #e8e8e8;
}}
*{{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}}
html,body{{width:100%;height:100%;overflow:hidden;background:var(--bg);}}
body{{display:flex;flex-direction:column;align-items:center;justify-content:center;
     font-family:'Courier New',monospace;color:var(--txt);touch-action:none;}}
#wrap{{position:relative;width:100%;max-width:480px;height:100vh;
       max-height:820px;overflow:hidden;display:flex;flex-direction:column;}}
#hud{{display:flex;justify-content:space-between;align-items:center;
      padding:8px 12px;background:rgba(0,0,0,.7);border-bottom:1px solid var(--acc);
      font-size:13px;gap:8px;flex-shrink:0;}}
.hud-val{{color:var(--acc);font-weight:bold;text-shadow:0 0 8px var(--acc);}}
canvas{{flex:1;width:100%;display:block;}}
/* Virtual joystick */
#joy-zone{{position:absolute;bottom:0;left:0;width:50%;height:44%;
           display:flex;align-items:center;justify-content:center;}}
#joy-outer{{width:90px;height:90px;border-radius:50%;
            border:2px solid rgba(255,255,255,.25);background:rgba(0,0,0,.35);
            position:relative;display:flex;align-items:center;justify-content:center;}}
#joy-inner{{width:38px;height:38px;border-radius:50%;
            background:var(--acc);opacity:.85;position:absolute;
            box-shadow:0 0 14px var(--acc);pointer-events:none;}}
/* Action buttons */
#btn-zone{{position:absolute;bottom:0;right:0;width:50%;height:44%;
           display:flex;align-items:center;justify-content:center;gap:18px;}}
.abtn{{width:56px;height:56px;border-radius:50%;border:2px solid var(--acc);
       background:rgba(0,0,0,.5);color:var(--acc);font-size:20px;
       display:flex;align-items:center;justify-content:center;
       box-shadow:0 0 12px var(--acc)44;cursor:pointer;user-select:none;
       -webkit-user-select:none;active:opacity:0.7;}}
.abtn:active{{background:var(--acc)33;transform:scale(.93);}}
/* Overlay screens */
.screen{{position:absolute;inset:0;display:flex;flex-direction:column;
          align-items:center;justify-content:center;
          background:rgba(0,0,0,.88);z-index:99;text-align:center;padding:24px;}}
.screen.hidden{{display:none;}}
.screen h1{{font-size:clamp(22px,6vw,36px);color:var(--acc);
            text-shadow:0 0 20px var(--acc);margin-bottom:10px;letter-spacing:2px;}}
.screen h2{{font-size:clamp(16px,4vw,24px);color:#fff;margin-bottom:8px;}}
.screen p{{font-size:13px;color:#aaa;margin:4px 0;line-height:1.5;}}
.screen .mechanic-pill{{margin:12px auto;padding:8px 18px;border:1px solid var(--acc);
  border-radius:20px;color:var(--acc);font-size:12px;max-width:280px;}}
.bigbtn{{margin-top:16px;padding:14px 36px;background:var(--acc);color:#000;
          font-family:inherit;font-size:16px;font-weight:bold;border:none;
          cursor:pointer;letter-spacing:2px;text-transform:uppercase;}}
.bigbtn:active{{opacity:.8;transform:scale(.97);}}
#score-ring{{width:72px;height:72px;border-radius:50%;border:3px solid var(--acc);
             display:flex;align-items:center;justify-content:center;flex-direction:column;}}
#score-ring .num{{font-size:20px;color:var(--acc);line-height:1;}}
#score-ring .lbl{{font-size:8px;color:#888;}}
#lives-row{{display:flex;gap:4px;}}
.life-pip{{width:10px;height:10px;border-radius:50%;background:var(--acc);
           box-shadow:0 0 6px var(--acc);}}
.life-pip.dead{{background:#333;box-shadow:none;}}
#special-bar{{flex:1;height:6px;background:#1a1a1a;border-radius:3px;overflow:hidden;}}
#special-fill{{height:100%;background:var(--acc);width:0%;
               transition:width .1s;box-shadow:0 0 4px var(--acc);}}
#brand-strip{{position:absolute;top:0;right:0;font-size:9px;color:#333;
              padding:3px 6px;letter-spacing:1px;}}
@media(orientation:landscape){{
  #wrap{{flex-direction:row;max-width:none;max-height:480px;height:100%;}}
  #hud{{flex-direction:column;width:80px;border-bottom:none;border-right:1px solid var(--acc);}}
  #joy-zone{{width:25%;height:100%;}}
  #btn-zone{{width:25%;height:100%;}}
}}
</style>
</head>"""

# ── START SCREEN (shared) ──────────────────────────────────
def start_screen():
    return f"""
<div id="start-screen" class="screen">
  <h1>{GAME_NAME.upper()}</h1>
  <h2>{GENRE.upper()}</h2>
  <div class="mechanic-pill">⚡ {MECHANIC}: {MECH_DESC[:60]}{"..." if len(MECH_DESC)>60 else ""}</div>
  <p style="color:#666;font-size:11px;margin-top:8px;">
    🕹️ Joystick + buttons | Works on any device
  </p>
  <button class="bigbtn" onclick="startGame()">PLAY FREE</button>
  <p style="margin-top:20px;font-size:11px;color:#555;">
    {GENRE} · ${GAME_PRICE} SOL for full Godot source<br>
    <a href="https://t.me/{TELEGRAM_CHANNEL.lstrip('@')}" style="color:var(--acc);">{TELEGRAM_CHANNEL}</a>
  </p>
</div>
<div id="over-screen" class="screen hidden">
  <h1>GAME OVER</h1>
  <p style="font-size:28px;color:#fff;margin:10px 0;" id="final-score"></p>
  <div class="mechanic-pill">⚡ {MECHANIC}</div>
  <p style="margin-top:12px;font-size:12px;color:#666;">
    Get full Godot source for ${GAME_PRICE} SOL
  </p>
  <p style="font-size:11px;margin:4px 0;">
    <a href="https://t.me/{TELEGRAM_CHANNEL.lstrip('@')}" style="color:var(--acc);">{TELEGRAM_CHANNEL}</a>
  </p>
  <button class="bigbtn" onclick="restartGame()">PLAY AGAIN</button>
</div>"""

# ── JOYSTICK JS (shared) ───────────────────────────────────
JOYSTICK_JS = """
// ── Virtual Joystick ──────────────────────────────────────
const joyZone  = document.getElementById('joy-zone');
const joyOuter = document.getElementById('joy-outer');
const joyInner = document.getElementById('joy-inner');
const JOY = {x:0, y:0, active:false, id:-1,
             ox:0, oy:0, r:36};

function joyStart(e){
  if(JOY.active) return;
  const t  = e.changedTouches[0];
  const rc = joyOuter.getBoundingClientRect();
  JOY.active = true;
  JOY.id     = t.identifier;
  JOY.ox     = rc.left + rc.width/2;
  JOY.oy     = rc.top  + rc.height/2;
  joyMove(e);
}
function joyMove(e){
  if(!JOY.active) return;
  for(const t of e.changedTouches){
    if(t.identifier !== JOY.id) continue;
    const dx = t.clientX - JOY.ox;
    const dy = t.clientY - JOY.oy;
    const d  = Math.sqrt(dx*dx+dy*dy);
    const c  = Math.min(d, JOY.r);
    JOY.x    = (dx/Math.max(d,1))*c/JOY.r;
    JOY.y    = (dy/Math.max(d,1))*c/JOY.r;
    joyInner.style.transform =
      `translate(${JOY.x*JOY.r}px,${JOY.y*JOY.r}px)`;
  }
}
function joyEnd(e){
  for(const t of e.changedTouches){
    if(t.identifier === JOY.id){
      JOY.active = false; JOY.x = 0; JOY.y = 0; JOY.id = -1;
      joyInner.style.transform = 'translate(0,0)';
    }
  }
}
joyZone.addEventListener('touchstart', joyStart, {passive:false});
joyZone.addEventListener('touchmove',  joyMove,  {passive:false});
joyZone.addEventListener('touchend',   joyEnd,   {passive:false});

// ── Keyboard fallback ────────────────────────────────────
const KB = {};
document.addEventListener('keydown', e=>{KB[e.key]=true; e.preventDefault();});
document.addEventListener('keyup',   e=>{KB[e.key]=false;});
function kbJoy(){
  JOY.x = ((KB['ArrowRight']||KB['d'])?1:0) - ((KB['ArrowLeft']||KB['a'])?1:0);
  JOY.y = ((KB['ArrowDown'] ||KB['s'])?1:0) - ((KB['ArrowUp']  ||KB['w'])?1:0);
}
"""

# ═══════════════════════════════════════════════════════════
#  GAME IMPLEMENTATIONS
# ═══════════════════════════════════════════════════════════

# ── SHOOTER (top-down twin-stick) ─────────────────────────
def build_shooter_game() -> str:
    return f"""{SHARED_HEAD}
<body>
<div id="wrap">
  <div id="hud">
    <div id="score-ring"><div class="num" id="sc">0</div><div class="lbl">SCORE</div></div>
    <div style="flex:1;display:flex;flex-direction:column;gap:6px;padding:0 8px;">
      <div id="lives-row">
        <div class="life-pip" id="lp0"></div>
        <div class="life-pip" id="lp1"></div>
        <div class="life-pip" id="lp2"></div>
      </div>
      <div id="special-bar"><div id="special-fill"></div></div>
      <div style="font-size:9px;color:#555;">⚡ {MECHANIC.upper()}</div>
    </div>
    <div style="font-size:11px;color:#666;text-align:right;">
      {GAME_NAME}<br><span style="color:var(--acc);font-size:9px;">WAVE <span id="wv">1</span></span>
    </div>
  </div>
  <canvas id="c"></canvas>
  {start_screen()}
  <div id="joy-zone">
    <div id="joy-outer"><div id="joy-inner"></div></div>
  </div>
  <div id="btn-zone">
    <div class="abtn" id="btn-special" ontouchstart="activateSpecial()">⚡</div>
    <div class="abtn" id="btn-fire" ontouchstart="rapidFire=true" ontouchend="rapidFire=false">🔥</div>
  </div>
  <div id="brand-strip">DeathRoll</div>
</div>
<script>
{JOYSTICK_JS}
const C   = document.getElementById('c');
const ctx = C.getContext('2d');
let W, H;

function resize(){{
  const wrap = document.getElementById('wrap');
  const hud  = document.getElementById('hud');
  C.width  = W = wrap.offsetWidth;
  C.height = H = wrap.offsetHeight - hud.offsetHeight;
}}
window.addEventListener('resize', resize);
resize();

// ── State ──────────────────────────────────────────────
let player, bullets, enemies, particles, score, lives;
let wave, frame, running, specialCharge, rapidFire=false;
let shootTimer=0, enemySpawnTimer=0;

function R(a,b){{return Math.random()*(b-a)+a;}}
function dist(a,b){{return Math.hypot(a.x-b.x,a.y-b.y);}}

function mkParticles(x,y,color,n=8){{
  for(let i=0;i<n;i++){{
    const angle = R(0,Math.PI*2);
    const speed = R(1,5);
    particles.push({{x,y,vx:Math.cos(angle)*speed,vy:Math.sin(angle)*speed,
                     life:R(20,40),color,r:R(2,5)}});
  }}
}}

function startGame(){{
  document.getElementById('start-screen').classList.add('hidden');
  init();
}}
function restartGame(){{
  document.getElementById('over-screen').classList.add('hidden');
  init();
}}

function init(){{
  player={{x:W/2,y:H*0.75,r:14,speed:3.8,angle:0,
           shield:false,shieldT:0,invincible:0}};
  bullets=[]; enemies=[]; particles=[];
  score=0; lives=3; wave=1; frame=0; running=true;
  specialCharge=0; shootTimer=0; enemySpawnTimer=0;
  updateHUD();
  loop();
}}

function updateHUD(){{
  document.getElementById('sc').textContent=score;
  document.getElementById('wv').textContent=wave;
  document.getElementById('special-fill').style.width=(specialCharge/300*100)+'%';
  for(let i=0;i<3;i++){{
    const pip=document.getElementById('lp'+i);
    if(pip) pip.className='life-pip'+(i>=lives?' dead':'');
  }}
}}

function spawnEnemy(){{
  const side=Math.floor(R(0,4));
  let x,y;
  if(side===0){{x=R(0,W);y=-25;}}
  else if(side===1){{x=W+25;y=R(0,H);}}
  else if(side===2){{x=R(0,W);y=H+25;}}
  else{{x=-25;y=R(0,H);}}
  const hp  = 1+Math.floor(score/300);
  const spd = R(0.9,1.8+wave*0.15);
  enemies.push({{x,y,r:14+hp*2,hp,maxHp:hp,speed:spd,
                 color:`hsl(${{R(0,360)}},70%,55%)`,angle:0,shoot:hp>3}});
}}

function activateSpecial(){{
  if(specialCharge < 300) return;
  // {MECHANIC} — mirror shell: 3s invincibility + damage pulse
  player.shield    = true;
  player.shieldT   = 180;
  player.invincible= 180;
  specialCharge    = 0;
  mkParticles(player.x,player.y,'{G_COLOR}',20);
  // Shockwave
  enemies.forEach(e=>{{
    const d=dist(player,e);
    if(d<160){{e.hp-=3; mkParticles(e.x,e.y,e.color,6);}}
  }});
  enemies=enemies.filter(e=>e.hp>0);
}}

document.getElementById('btn-special')
  .addEventListener('touchstart',e=>{{e.preventDefault();activateSpecial();}},{{passive:false}});

function loop(){{
  if(!running) return;
  requestAnimationFrame(loop);
  frame++;
  kbJoy();

  // ── Move player ──────────────────────────────────────
  const spd = player.speed;
  player.x  = Math.max(player.r, Math.min(W-player.r, player.x+JOY.x*spd));
  player.y  = Math.max(player.r, Math.min(H-player.r, player.y+JOY.y*spd));
  if(player.shieldT>0){{player.shieldT--;if(player.shieldT===0)player.shield=false;}}
  if(player.invincible>0) player.invincible--;

  // ── Auto/rapid shoot toward nearest enemy ────────────
  shootTimer++;
  const rate = rapidFire ? 8 : 18;
  if(shootTimer>=rate && enemies.length){{
    shootTimer=0;
    let nearest=enemies.reduce((a,b)=>dist(player,a)<dist(player,b)?a:b);
    const ang=Math.atan2(nearest.y-player.y,nearest.x-player.x);
    bullets.push({{x:player.x,y:player.y,vx:Math.cos(ang)*9,vy:Math.sin(ang)*9,r:5}});
    if(rapidFire){{
      bullets.push({{x:player.x,y:player.y,
                    vx:Math.cos(ang+0.2)*9,vy:Math.sin(ang+0.2)*9,r:4}});
    }}
  }}

  // ── Spawn enemies ─────────────────────────────────────
  enemySpawnTimer++;
  const spawnRate=Math.max(35,90-wave*8);
  if(enemySpawnTimer>=spawnRate){{enemySpawnTimer=0;spawnEnemy();
    if(wave>3 && Math.random()<0.3) spawnEnemy();
  }}
  if(score>0 && score%500===0 && frame%60===0) wave=Math.min(20,1+Math.floor(score/500));

  // ── Move enemies toward player ────────────────────────
  enemies.forEach(e=>{{
    const ang=Math.atan2(player.y-e.y,player.x-e.x);
    e.x+=Math.cos(ang)*e.speed;
    e.y+=Math.sin(ang)*e.speed;
  }});

  // ── Collisions: bullet→enemy ──────────────────────────
  bullets=bullets.filter(b=>b.x>-20&&b.x<W+20&&b.y>-20&&b.y<H+20);
  for(let bi=bullets.length-1;bi>=0;bi--){{
    for(let ei=enemies.length-1;ei>=0;ei--){{
      if(dist(bullets[bi],enemies[ei])<enemies[ei].r+bullets[bi].r){{
        enemies[ei].hp--;
        mkParticles(enemies[ei].x,enemies[ei].y,enemies[ei].color,4);
        bullets.splice(bi,1);
        if(enemies[ei].hp<=0){{
          score+=10+wave*2;
          specialCharge=Math.min(300,specialCharge+20);
          mkParticles(enemies[ei].x,enemies[ei].y,enemies[ei].color,12);
          enemies.splice(ei,1);
          updateHUD();
        }}
        break;
      }}
    }}
  }}

  // ── Collisions: enemy→player ─────────────────────────
  if(player.invincible===0){{
    for(let ei=enemies.length-1;ei>=0;ei--){{
      if(dist(player,enemies[ei])<player.r+enemies[ei].r-4){{
        lives--;
        player.invincible=90;
        mkParticles(player.x,player.y,'#ff3344',16);
        enemies.splice(ei,1);
        updateHUD();
        if(lives<=0){{running=false;gameOver();return;}}
      }}
    }}
  }}

  // ── Draw ─────────────────────────────────────────────
  ctx.fillStyle='{G_BG}';
  ctx.fillRect(0,0,W,H);

  // Grid
  ctx.strokeStyle='rgba(255,255,255,0.04)';
  ctx.lineWidth=1;
  const gs=40;
  for(let x=0;x<W;x+=gs){{ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke();}}
  for(let y=0;y<H;y+=gs){{ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}}

  // Particles
  particles.forEach((p,i)=>{{
    p.x+=p.vx; p.y+=p.vy; p.vx*=0.92; p.vy*=0.92; p.life--;
    ctx.globalAlpha=p.life/40;
    ctx.fillStyle=p.color;
    ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2); ctx.fill();
  }});
  ctx.globalAlpha=1;
  particles=particles.filter(p=>p.life>0);

  // Enemies
  enemies.forEach(e=>{{
    ctx.save();
    ctx.shadowColor=e.color; ctx.shadowBlur=10;
    ctx.fillStyle=e.color;
    ctx.beginPath(); ctx.arc(e.x,e.y,e.r,0,Math.PI*2); ctx.fill();
    // HP bar
    if(e.maxHp>1){{
      ctx.fillStyle='#111';
      ctx.fillRect(e.x-e.r,e.y-e.r-8,e.r*2,4);
      ctx.fillStyle=e.color;
      ctx.fillRect(e.x-e.r,e.y-e.r-8,e.r*2*(e.hp/e.maxHp),4);
    }}
    ctx.restore();
  }});

  // Bullets
  bullets.forEach(b=>{{
    b.x+=b.vx; b.y+=b.vy;
    ctx.save();
    ctx.shadowColor='{G_COLOR}'; ctx.shadowBlur=12;
    ctx.fillStyle='{G_COLOR}';
    ctx.beginPath(); ctx.arc(b.x,b.y,b.r,0,Math.PI*2); ctx.fill();
    ctx.restore();
  }});

  // Player
  ctx.save();
  if(player.shield){{
    ctx.shadowColor='{G_COLOR}'; ctx.shadowBlur=24;
    ctx.strokeStyle='{G_COLOR}'; ctx.lineWidth=3;
    ctx.beginPath(); ctx.arc(player.x,player.y,player.r+10,0,Math.PI*2); ctx.stroke();
  }}
  if(player.invincible>0 && Math.floor(frame/4)%2===0){{
    ctx.restore(); return;
  }}
  ctx.shadowColor='#fff'; ctx.shadowBlur=8;
  ctx.fillStyle='#ffffff';
  ctx.translate(player.x,player.y);
  ctx.beginPath();
  ctx.moveTo(0,-player.r);
  ctx.lineTo(player.r*0.7,player.r*0.8);
  ctx.lineTo(-player.r*0.7,player.r*0.8);
  ctx.closePath(); ctx.fill();
  ctx.restore();
}}

function gameOver(){{
  document.getElementById('final-score').textContent='SCORE: '+score;
  document.getElementById('over-screen').classList.remove('hidden');
}}
</script>
</body></html>"""

# ── WAVE DEFENSE (fighting/strategy/tower defense) ────────
def build_wave_game() -> str:
    return f"""{SHARED_HEAD}
<body>
<div id="wrap">
  <div id="hud">
    <div id="score-ring"><div class="num" id="sc">0</div><div class="lbl">SCORE</div></div>
    <div style="flex:1;display:flex;flex-direction:column;gap:6px;padding:0 8px;">
      <div id="lives-row">
        <div class="life-pip" id="lp0"></div><div class="life-pip" id="lp1"></div>
        <div class="life-pip" id="lp2"></div><div class="life-pip" id="lp3"></div>
        <div class="life-pip" id="lp4"></div>
      </div>
      <div id="special-bar"><div id="special-fill"></div></div>
    </div>
    <div style="font-size:11px;color:#666;text-align:right;">
      {GAME_NAME}<br><span style="color:var(--acc);font-size:9px;">WAVE <span id="wv">1</span></span>
    </div>
  </div>
  <canvas id="c"></canvas>
  {start_screen()}
  <div id="joy-zone"><div id="joy-outer"><div id="joy-inner"></div></div></div>
  <div id="btn-zone">
    <div class="abtn" ontouchstart="activateSpecial()">⚡</div>
    <div class="abtn" ontouchstart="slash()">⚔️</div>
  </div>
  <div id="brand-strip">DeathRoll</div>
</div>
<script>
{JOYSTICK_JS}
const C=document.getElementById('c'),ctx=C.getContext('2d');
let W,H;
function resize(){{const wrap=document.getElementById('wrap'),hud=document.getElementById('hud');C.width=W=wrap.offsetWidth;C.height=H=wrap.offsetHeight-hud.offsetHeight;}}
window.addEventListener('resize',resize);resize();

let player,enemies,particles,slashes,score,lives,wave,frame,running,charge,waveTimer,waveActive;

function R(a,b){{return Math.random()*(b-a)+a;}}
function dist(a,b){{return Math.hypot(a.x-b.x,a.y-b.y);}}
function mkP(x,y,c,n=8){{for(let i=0;i<n;i++){{const a=R(0,Math.PI*2),s=R(2,6);particles.push({{x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,life:R(25,45),color:c,r:R(2,5)}});}}}}

function startGame(){{document.getElementById('start-screen').classList.add('hidden');init();}}
function restartGame(){{document.getElementById('over-screen').classList.add('hidden');init();}}

function init(){{
  player={{x:W/2,y:H/2,r:16,speed:3.5,invincible:0,facingAngle:0}};
  enemies=[];particles=[];slashes=[];
  score=0;lives=5;wave=1;frame=0;running=true;charge=0;
  waveTimer=120;waveActive=false;
  updateHUD();loop();
}}
function updateHUD(){{
  document.getElementById('sc').textContent=score;
  document.getElementById('wv').textContent=wave;
  document.getElementById('special-fill').style.width=(charge/300*100)+'%';
  for(let i=0;i<5;i++){{const p=document.getElementById('lp'+i);if(p)p.className='life-pip'+(i>=lives?' dead':'');}}
}}
function spawnWave(){{
  const count=3+wave*2;
  for(let i=0;i<count;i++){{
    const ang=R(0,Math.PI*2),d=Math.max(W,H)*0.6;
    const hp=1+Math.floor(wave/2);
    enemies.push({{x:W/2+Math.cos(ang)*d,y:H/2+Math.sin(ang)*d,
                   r:12+hp*3,hp,maxHp:hp,speed:R(1,1.8+wave*0.1),
                   color:`hsl(${{R(0,360)}},70%,55%)`,invincible:0}});
  }}
  waveActive=true;
}}
function slash(){{
  // Melee attack in facing direction
  const range=70;
  slashes.push({{x:player.x,y:player.y,angle:player.facingAngle,life:14,range}});
  enemies.forEach((e,i)=>{{
    const ang=Math.atan2(e.y-player.y,e.x-player.x);
    const diff=Math.abs(ang-player.facingAngle);
    if(dist(player,e)<range+e.r && diff<1.1){{
      e.hp--;charge=Math.min(300,charge+30);
      mkP(e.x,e.y,e.color,6);
      if(e.hp<=0){{score+=15+wave*3;mkP(e.x,e.y,e.color,14);enemies.splice(i,1);}}
    }}
  }});
  updateHUD();
}}
function activateSpecial(){{
  if(charge<300)return;
  charge=0;
  // Massive area clear
  enemies.forEach((e,i)=>{{if(dist(player,e)<200){{mkP(e.x,e.y,e.color,12);score+=10;enemies.splice(i,1);}}}});
  mkP(player.x,player.y,'{G_COLOR}',30);
  player.invincible=120;
  updateHUD();
}}
document.getElementById('btn-zone').querySelectorAll('.abtn')[0]
  .addEventListener('touchstart',e=>{{e.preventDefault();activateSpecial();}},{{passive:false}});
document.getElementById('btn-zone').querySelectorAll('.abtn')[1]
  .addEventListener('touchstart',e=>{{e.preventDefault();slash();}},{{passive:false}});
document.addEventListener('keydown',e=>{{if(e.key===' ')activateSpecial();if(e.key==='z'||e.key==='x')slash();}});

function loop(){{
  if(!running)return;
  requestAnimationFrame(loop);
  frame++;kbJoy();
  player.x=Math.max(player.r,Math.min(W-player.r,player.x+JOY.x*player.speed));
  player.y=Math.max(player.r,Math.min(H-player.r,player.y+JOY.y*player.speed));
  if(JOY.x!==0||JOY.y!==0) player.facingAngle=Math.atan2(JOY.y,JOY.x);
  if(player.invincible>0)player.invincible--;

  if(!waveActive){{
    waveTimer--;
    if(waveTimer<=0){{spawnWave();waveTimer=0;}}
  }}
  if(waveActive && enemies.length===0){{
    wave++;waveTimer=90;waveActive=false;score+=wave*20;updateHUD();
  }}

  enemies.forEach(e=>{{
    if(e.invincible>0){{e.invincible--;return;}}
    const ang=Math.atan2(player.y-e.y,player.x-e.x);
    e.x+=Math.cos(ang)*e.speed;e.y+=Math.sin(ang)*e.speed;
  }});

  if(player.invincible===0){{
    enemies.forEach((e,i)=>{{
      if(dist(player,e)<player.r+e.r-4){{
        lives--;player.invincible=80;mkP(player.x,player.y,'#ff3344',12);
        enemies.splice(i,1);updateHUD();
        if(lives<=0){{running=false;gameOver();}}
      }}
    }});
  }}

  // Draw
  ctx.fillStyle='{G_BG}';ctx.fillRect(0,0,W,H);
  // Radial bg glow
  const grd=ctx.createRadialGradient(W/2,H/2,30,W/2,H/2,H*0.7);
  grd.addColorStop(0,'{G_COLOR}11');grd.addColorStop(1,'transparent');
  ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);

  particles.forEach(p=>{{p.x+=p.vx;p.y+=p.vy;p.vx*=0.9;p.vy*=0.9;p.life--;
    ctx.globalAlpha=p.life/45;ctx.fillStyle=p.color;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();}});
  ctx.globalAlpha=1;particles=particles.filter(p=>p.life>0);

  slashes.forEach(s=>{{
    s.life--;ctx.save();ctx.globalAlpha=s.life/14;ctx.strokeStyle='{G_COLOR}';
    ctx.lineWidth=4;ctx.shadowColor='{G_COLOR}';ctx.shadowBlur=20;
    ctx.beginPath();ctx.moveTo(s.x,s.y);
    ctx.lineTo(s.x+Math.cos(s.angle)*s.range,s.y+Math.sin(s.angle)*s.range);
    ctx.stroke();ctx.restore();
  }});
  slashes=slashes.filter(s=>s.life>0);

  enemies.forEach(e=>{{
    ctx.save();ctx.shadowColor=e.color;ctx.shadowBlur=8;ctx.fillStyle=e.color;
    ctx.beginPath();ctx.arc(e.x,e.y,e.r,0,Math.PI*2);ctx.fill();
    if(e.maxHp>1){{ctx.fillStyle='#111';ctx.fillRect(e.x-e.r,e.y-e.r-8,e.r*2,4);
      ctx.fillStyle=e.color;ctx.fillRect(e.x-e.r,e.y-e.r-8,e.r*2*(e.hp/e.maxHp),4);}}
    ctx.restore();
  }});

  // Player
  ctx.save();
  if(player.invincible>0&&Math.floor(frame/5)%2===0){{ctx.restore();}}
  else{{
    ctx.shadowColor='{G_COLOR}';ctx.shadowBlur=14;ctx.fillStyle='{G_COLOR}';
    ctx.translate(player.x,player.y);ctx.rotate(player.facingAngle+Math.PI/2);
    ctx.beginPath();ctx.moveTo(0,-16);ctx.lineTo(12,10);ctx.lineTo(-12,10);ctx.closePath();ctx.fill();
    ctx.restore();
  }}

  if(!waveActive&&waveTimer>0){{
    ctx.fillStyle='rgba(0,0,0,.5)';ctx.fillRect(W/2-100,H/2-20,200,40);
    ctx.fillStyle='{G_COLOR}';ctx.font='bold 14px Courier New';ctx.textAlign='center';
    ctx.fillText(`WAVE ${{wave}} IN ${{Math.ceil(waveTimer/30)}}s`,W/2,H/2+5);ctx.textAlign='left';
  }}
}}
function gameOver(){{
  document.getElementById('final-score').textContent='SCORE: '+score;
  document.getElementById('over-screen').classList.remove('hidden');
}}
</script>
</body></html>"""

# ── PLATFORMER ────────────────────────────────────────────
def build_platformer_game() -> str:
    return f"""{SHARED_HEAD}
<body>
<div id="wrap">
  <div id="hud">
    <div id="score-ring"><div class="num" id="sc">0</div><div class="lbl">SCORE</div></div>
    <div style="flex:1;display:flex;flex-direction:column;gap:6px;padding:0 8px;">
      <div id="lives-row">
        <div class="life-pip" id="lp0"></div>
        <div class="life-pip" id="lp1"></div>
        <div class="life-pip" id="lp2"></div>
      </div>
      <div id="special-bar"><div id="special-fill"></div></div>
    </div>
    <div style="font-size:11px;color:#666;">{GAME_NAME}</div>
  </div>
  <canvas id="c"></canvas>
  {start_screen()}
  <div id="joy-zone"><div id="joy-outer"><div id="joy-inner"></div></div></div>
  <div id="btn-zone">
    <div class="abtn" ontouchstart="doJump()">↑</div>
    <div class="abtn" ontouchstart="activateSpecial()">⚡</div>
  </div>
  <div id="brand-strip">DeathRoll</div>
</div>
<script>
{JOYSTICK_JS}
const C=document.getElementById('c'),ctx=C.getContext('2d');
let W,H;
function resize(){{const wrap=document.getElementById('wrap'),hud=document.getElementById('hud');C.width=W=wrap.offsetWidth;C.height=H=wrap.offsetHeight-hud.offsetHeight;}}
window.addEventListener('resize',resize);resize();

let player,platforms,coins,enemies,particles,score,lives,frame,running,charge,camY;
const GRAV=0.45,JUMP=-10;

function R(a,b){{return Math.random()*(b-a)+a;}}
function mkP(x,y,c,n=6){{for(let i=0;i<n;i++){{const a=R(0,Math.PI*2),s=R(1,4);particles.push({{x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,life:R(20,35),color:c,r:R(1,4)}});}}}}

function startGame(){{document.getElementById('start-screen').classList.add('hidden');init();}}
function restartGame(){{document.getElementById('over-screen').classList.add('hidden');init();}}

function doJump(){{if(player&&player.onGround){{player.vy=JUMP;player.onGround=false;mkP(player.x,player.y+player.h,'{G_COLOR}',6);}}}}
function activateSpecial(){{
  if(charge<300)return;charge=0;
  player.vy=JUMP*1.6;player.invincible=120;
  mkP(player.x,player.y,'{G_COLOR}',20);
  enemies.forEach((e,i)=>{{if(Math.hypot(e.x-player.x,e.y-player.y)<120){{mkP(e.x,e.y,e.color,8);enemies.splice(i,1);score+=20;}}}});
  updateHUD();
}}
document.addEventListener('keydown',e=>{{
  if(e.key===' '||e.key==='ArrowUp'||e.key==='w')doJump();
  if(e.key==='z')activateSpecial();
}});

function buildLevel(startY){{
  const plats=[];
  plats.push({{x:0,y:startY+H-20,w:W,h:20,color:'#333'}});
  for(let i=1;i<30;i++){{
    const y=startY+H-20-i*85+R(-20,20);
    const w=R(60,140);
    const x=R(10,W-w-10);
    plats.push({{x,y,w,h:14,color:`hsl(${{R(180,280)}},60%,35%)`}});
  }}
  return plats;
}}
function buildCoins(plats){{
  return plats.slice(1).map(p=>{{
    if(Math.random()<0.6) return {{x:p.x+p.w/2,y:p.y-18,r:7,collected:false}};
    return null;
  }}).filter(Boolean);
}}
function buildEnemies(plats){{
  return plats.slice(5).filter(()=>Math.random()<0.35).map(p=>{{
    return {{x:p.x+p.w/2,y:p.y-20,r:12,dx:1.2,plat:p,color:`hsl(${{R(0,60)}},80%,55%)`,invincible:0}};
  }});
}}

function init(){{
  camY=0;
  player={{x:W/2-12,y:H-100,w:24,h:28,vx:0,vy:0,onGround:false,invincible:0}};
  platforms=buildLevel(0);
  coins=buildCoins(platforms);
  enemies=buildEnemies(platforms);
  particles=[];score=0;lives=3;frame=0;running=true;charge=0;
  updateHUD();loop();
}}
function updateHUD(){{
  document.getElementById('sc').textContent=score;
  document.getElementById('special-fill').style.width=(charge/300*100)+'%';
  for(let i=0;i<3;i++){{const p=document.getElementById('lp'+i);if(p)p.className='life-pip'+(i>=lives?' dead':'');}}
}}

function loop(){{
  if(!running)return;
  requestAnimationFrame(loop);
  frame++;kbJoy();

  player.vx=JOY.x*4;
  player.vy+=GRAV;
  player.x+=player.vx;
  player.y+=player.vy;
  player.onGround=false;
  player.x=Math.max(0,Math.min(W-player.w,player.x));
  if(player.invincible>0)player.invincible--;

  platforms.forEach(p=>{{
    if(player.vx>=0||true){{
      if(player.x<p.x+p.w&&player.x+player.w>p.x&&
         player.y+player.h>p.y&&player.y+player.h<p.y+p.h+Math.abs(player.vy)+2&&player.vy>=0){{
        player.y=p.y-player.h;player.vy=0;player.onGround=true;
      }}
    }}
  }});

  // Scroll camera
  const targetY=player.y-H*0.5;
  if(targetY<camY) camY+=(targetY-camY)*0.08;

  // Collect coins
  coins.forEach(coin=>{{
    if(!coin.collected&&Math.hypot(player.x+12-coin.x,player.y+14-coin.y)<coin.r+14){{
      coin.collected=true;score+=5;charge=Math.min(300,charge+25);
      mkP(coin.x,coin.y,'{G_COLOR}',8);updateHUD();
    }}
  }});

  // Enemy movement
  enemies.forEach(e=>{{
    e.x+=e.dx;
    if(e.x<e.plat.x||e.x>e.plat.x+e.plat.w) e.dx*=-1;
    // Player stomps enemy
    if(player.invincible===0&&Math.hypot(player.x+12-e.x,player.y+14-e.y)<e.r+14){{
      if(player.vy>0&&player.y+player.h<e.y+4){{
        score+=15;charge=Math.min(300,charge+50);
        mkP(e.x,e.y,e.color,12);
        enemies=enemies.filter(en=>en!==e);player.vy=JUMP*0.6;updateHUD();
      }} else if(player.invincible===0){{
        lives--;player.invincible=90;player.vy=JUMP*0.7;
        mkP(player.x,player.y,'#ff3344',12);updateHUD();
        if(lives<=0){{running=false;gameOver();}}
      }}
    }}
  }});

  if(player.y-camY>H+100){{running=false;gameOver();}}

  // Fall off bottom
  if(player.y>10000){{running=false;gameOver();}}

  // Draw
  ctx.fillStyle='{G_BG}';ctx.fillRect(0,0,W,H);
  ctx.save();ctx.translate(0,-camY);

  platforms.forEach(p=>{{
    ctx.fillStyle=p.color;ctx.fillRect(p.x,p.y,p.w,p.h);
    ctx.fillStyle='rgba(255,255,255,0.06)';ctx.fillRect(p.x,p.y,p.w,4);
  }});

  coins.forEach(c=>{{
    if(c.collected)return;
    ctx.save();ctx.shadowColor='{G_COLOR}';ctx.shadowBlur=10;
    ctx.fillStyle='{G_COLOR}';ctx.beginPath();ctx.arc(c.x,c.y,c.r,0,Math.PI*2);ctx.fill();
    ctx.restore();
  }});

  enemies.forEach(e=>{{
    ctx.save();ctx.shadowColor=e.color;ctx.shadowBlur=8;ctx.fillStyle=e.color;
    ctx.beginPath();ctx.arc(e.x,e.y,e.r,0,Math.PI*2);ctx.fill();ctx.restore();
  }});

  particles.forEach(p=>{{
    p.x+=p.vx;p.y+=p.vy;p.vy+=0.15;p.life--;
    ctx.globalAlpha=p.life/35;ctx.fillStyle=p.color;
    ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();
  }});
  ctx.globalAlpha=1;particles=particles.filter(p=>p.life>0);

  // Player
  if(!(player.invincible>0&&Math.floor(frame/5)%2===0)){{
    ctx.fillStyle='{G_COLOR}';ctx.shadowColor='{G_COLOR}';ctx.shadowBlur=10;
    ctx.fillRect(player.x,player.y,player.w,player.h);
    ctx.fillStyle='rgba(255,255,255,.5)';ctx.fillRect(player.x+6,player.y+6,6,6);
  }}
  ctx.restore();
}}
function gameOver(){{
  document.getElementById('final-score').textContent='SCORE: '+score;
  document.getElementById('over-screen').classList.remove('hidden');
}}
</script>
</body></html>"""

# ── PUZZLE (sliding tiles) ─────────────────────────────────
def build_puzzle_game() -> str:
    return f"""{SHARED_HEAD}
<body>
<div id="wrap">
  <div id="hud">
    <div id="score-ring"><div class="num" id="sc">0</div><div class="lbl">MOVES</div></div>
    <div style="flex:1;display:flex;flex-direction:column;gap:6px;padding:0 8px;">
      <div style="font-size:11px;color:var(--acc);">Best: <span id="best">—</span></div>
      <div id="special-bar"><div id="special-fill"></div></div>
      <div style="font-size:9px;color:#555;">⚡ {MECHANIC.upper()}</div>
    </div>
    <div style="font-size:11px;color:#666;">{GAME_NAME}</div>
  </div>
  <canvas id="c"></canvas>
  {start_screen()}
  <div id="brand-strip">DeathRoll</div>
</div>
<script>
const C=document.getElementById('c'),ctx=C.getContext('2d');
let W,H;
function resize(){{const wrap=document.getElementById('wrap'),hud=document.getElementById('hud');C.width=W=wrap.offsetWidth;C.height=H=wrap.offsetHeight-hud.offsetHeight;}}
window.addEventListener('resize',resize);resize();

const N=4;
let board,blank,moves,best,running,animTile,frame,charge;

function startGame(){{document.getElementById('start-screen').classList.add('hidden');init();}}
function restartGame(){{document.getElementById('over-screen').classList.add('hidden');init();}}

function init(){{
  // Build solved board
  board=[];
  for(let i=0;i<N*N-1;i++) board.push(i+1);
  board.push(0);
  blank={{r:N-1,c:N-1}};
  // Shuffle with valid moves
  for(let i=0;i<300;i++) doMove(random_move());
  moves=0;charge=0;running=true;animTile=null;frame=0;
  updateHUD();loop();
}}
function getBest(){{return localStorage?localStorage.getItem('dr_puzzle_best')||null:null;}}
function setBest(v){{if(localStorage)localStorage.setItem('dr_puzzle_best',v);}}
function updateHUD(){{
  document.getElementById('sc').textContent=moves;
  const b=getBest();
  document.getElementById('best').textContent=b||'—';
  document.getElementById('special-fill').style.width=(charge/300*100)+'%';
}}
function idx(r,c){{return r*N+c;}}
function random_move(){{
  const dirs=[[-1,0],[1,0],[0,-1],[0,1]];
  const valid=dirs.filter(([dr,dc])=>{{
    const nr=blank.r+dr,nc=blank.c+dc;
    return nr>=0&&nr<N&&nc>=0&&nc<N;
  }});
  return valid[Math.floor(Math.random()*valid.length)];
}}
function doMove([dr,dc]){{
  const nr=blank.r+dr,nc=blank.c+dc;
  if(nr<0||nr>=N||nc<0||nc>=N) return false;
  board[idx(blank.r,blank.c)]=board[idx(nr,nc)];
  board[idx(nr,nc)]=0;
  blank={{r:nr,c:nc}};
  return true;
}}
function isSolved(){{
  for(let i=0;i<N*N-1;i++) if(board[i]!==i+1) return false;
  return board[N*N-1]===0;
}}

C.addEventListener('click',handleClick);
C.addEventListener('touchend',e=>{{e.preventDefault();const t=e.changedTouches[0];handleClick({{clientX:t.clientX,clientY:t.clientY}});}},{{passive:false}});

function handleClick(e){{
  if(!running) return;
  const rect=C.getBoundingClientRect();
  const mx=e.clientX-rect.left,my=e.clientY-rect.top;
  const tw=W/N,th=H/N;
  const cc=Math.floor(mx/tw),cr=Math.floor(my/th);
  if(cr<0||cr>=N||cc<0||cc>=N) return;
  const dr=cr-blank.r,dc=cc-blank.c;
  if((Math.abs(dr)+Math.abs(dc))===1){{
    doMove([dr,dc]);moves++;
    charge=Math.min(300,charge+10);
    updateHUD();
    if(isSolved()){{
      running=false;
      const b=getBest();
      if(!b||moves<parseInt(b)) setBest(moves);
      setTimeout(()=>{{
        document.getElementById('final-score').textContent=`Solved in ${{moves}} moves!`;
        document.getElementById('over-screen').classList.remove('hidden');
      }},500);
    }}
  }}
}}

function loop(){{
  requestAnimationFrame(loop);frame++;
  ctx.fillStyle='{G_BG}';ctx.fillRect(0,0,W,H);
  const tw=W/N,th=H/N,gap=4;
  for(let r=0;r<N;r++){{
    for(let c=0;c<N;c++){{
      const v=board[idx(r,c)];
      if(v===0) continue;
      const x=c*tw+gap/2,y=r*th+gap/2,bw=tw-gap,bh=th-gap;
      // Tile bg
      const hue=((v-1)/(N*N-1))*280+20;
      ctx.fillStyle=`hsl(${{hue}},60%,18%)`;
      ctx.fillRect(x,y,bw,bh);
      ctx.strokeStyle=`hsl(${{hue}},70%,45%)`;
      ctx.lineWidth=2;ctx.strokeRect(x+1,y+1,bw-2,bh-2);
      // Number
      ctx.fillStyle=`hsl(${{hue}},80%,70%)`;
      ctx.font=`bold ${{Math.floor(tw*0.38)}}px Courier New`;
      ctx.textAlign='center';ctx.textBaseline='middle';
      ctx.shadowColor=`hsl(${{hue}},80%,60%)`;ctx.shadowBlur=8;
      ctx.fillText(v,x+bw/2,y+bh/2);
      ctx.shadowBlur=0;
    }}
  }}
  ctx.textAlign='left';ctx.textBaseline='alphabetic';
  // Grid lines
  ctx.strokeStyle='rgba(255,255,255,0.05)';ctx.lineWidth=1;
  for(let i=1;i<N;i++){{
    ctx.beginPath();ctx.moveTo(i*tw,0);ctx.lineTo(i*tw,H);ctx.stroke();
    ctx.beginPath();ctx.moveTo(0,i*th);ctx.lineTo(W,i*th);ctx.stroke();
  }}
}}
function gameOver(){{}}
</script>
</body></html>"""

# ── RACER ─────────────────────────────────────────────────
def build_racer_game() -> str:
    return f"""{SHARED_HEAD}
<body>
<div id="wrap">
  <div id="hud">
    <div id="score-ring"><div class="num" id="sc">0</div><div class="lbl">DIST</div></div>
    <div style="flex:1;display:flex;flex-direction:column;gap:6px;padding:0 8px;">
      <div style="font-size:11px;color:var(--acc);">SPEED: <span id="spd">0</span></div>
      <div id="special-bar"><div id="special-fill"></div></div>
    </div>
    <div style="font-size:11px;color:#666;">{GAME_NAME}</div>
  </div>
  <canvas id="c"></canvas>
  {start_screen()}
  <div id="joy-zone"><div id="joy-outer"><div id="joy-inner"></div></div></div>
  <div id="btn-zone">
    <div class="abtn" ontouchstart="activateBoost()">🚀</div>
  </div>
  <div id="brand-strip">DeathRoll</div>
</div>
<script>
{JOYSTICK_JS}
const C=document.getElementById('c'),ctx=C.getContext('2d');
let W,H;
function resize(){{const wrap=document.getElementById('wrap'),hud=document.getElementById('hud');C.width=W=wrap.offsetWidth;C.height=H=wrap.offsetHeight-hud.offsetHeight;}}
window.addEventListener('resize',resize);resize();

let car,obstacles,coins,particles,score,frame,running,speed,boost,charge,lines;
function R(a,b){{return Math.random()*(b-a)+a;}}
function mkP(x,y,c,n=8){{for(let i=0;i<n;i++){{const a=R(0,Math.PI*2),s=R(2,6);particles.push({{x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,life:R(20,35),color:c,r:R(2,4)}});}}}}

function startGame(){{document.getElementById('start-screen').classList.add('hidden');init();}}
function restartGame(){{document.getElementById('over-screen').classList.add('hidden');init();}}
function activateBoost(){{
  if(charge<300)return;charge=0;boost=180;
  mkP(car.x,car.y+30,'{G_COLOR}',20);updateHUD();
}}
document.addEventListener('keydown',e=>{{if(e.key===' ')activateBoost();}});

function init(){{
  car={{x:W/2,y:H*0.75,w:28,h:44,invincible:0}};
  obstacles=[];coins=[];particles=[];lines=[];
  score=0;frame=0;running=true;speed=3;boost=0;charge=0;
  for(let i=0;i<15;i++) lines.push({{x:W/2,y:i*(H/7),speed:0}});
  updateHUD();loop();
}}
function updateHUD(){{
  document.getElementById('sc').textContent=Math.floor(score);
  document.getElementById('spd').textContent=Math.floor(speed*10);
  document.getElementById('special-fill').style.width=(charge/300*100)+'%';
}}

function loop(){{
  if(!running)return;
  requestAnimationFrame(loop);
  frame++;kbJoy();

  const effectiveSpeed=speed+(boost>0?5:0);
  if(boost>0)boost--;
  speed=Math.min(12,3+frame/600);
  car.x=Math.max(car.w/2+20,Math.min(W-car.w/2-20,car.x+JOY.x*5));
  if(car.invincible>0)car.invincible--;
  score+=effectiveSpeed*0.1;

  // Road lines scroll
  lines.forEach(l=>{{l.y+=effectiveSpeed*2;if(l.y>H){{l.y-=H;l.x=W/2+R(-20,20);}}}}); 

  // Spawn obstacles
  if(frame%Math.max(30,60-Math.floor(speed*4))===0){{
    const cols=[W*0.2,W*0.4,W*0.6,W*0.8];
    const col=cols[Math.floor(R(0,cols.length))];
    obstacles.push({{x:col,y:-30,w:R(30,50),h:R(30,50),color:`hsl(${{R(0,360)}},70%,50%)`}});
  }}
  if(frame%45===0) coins.push({{x:R(40,W-40),y:-20,r:10,collected:false}});

  obstacles.forEach(o=>o.y+=effectiveSpeed*1.8);
  coins.forEach(c=>c.y+=effectiveSpeed*1.8);
  obstacles=obstacles.filter(o=>o.y<H+60);
  coins=coins.filter(c=>c.y<H+30&&!c.collected);

  // Collect coins
  coins.forEach(c=>{{
    if(!c.collected&&Math.hypot(car.x-c.x,car.y-c.y)<c.r+18){{
      c.collected=true;score+=20;charge=Math.min(300,charge+40);
      mkP(c.x,c.y,'{G_COLOR}',8);updateHUD();
    }}
  }});

  // Crash
  if(car.invincible===0){{
    obstacles.forEach((o,i)=>{{
      if(car.x-car.w/2<o.x+o.w/2&&car.x+car.w/2>o.x-o.w/2&&
         car.y-car.h/2<o.y+o.h/2&&car.y+car.h/2>o.y-o.h/2){{
        mkP(car.x,car.y,'#ff4444',20);
        running=false;gameOver();
      }}
    }});
  }}

  // Draw
  // Road
  ctx.fillStyle='#111';ctx.fillRect(0,0,W,H);
  ctx.fillStyle='#1a1a1a';ctx.fillRect(W*0.1,0,W*0.8,H);
  // Kerb
  ctx.fillStyle='#ff3300';
  for(let y=0;y<H;y+=80){{ctx.fillRect(W*0.1-8,y,8,40);ctx.fillRect(W*0.9,y,8,40);}}
  // Road lines
  lines.forEach(l=>{{
    ctx.fillStyle='rgba(255,255,100,0.6)';ctx.fillRect(l.x-2,l.y,4,30);
  }});
  // Particles
  particles.forEach(p=>{{p.x+=p.vx;p.y+=p.vy;p.vx*=0.9;p.vy*=0.9;p.life--;
    ctx.globalAlpha=p.life/35;ctx.fillStyle=p.color;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();}});
  ctx.globalAlpha=1;particles=particles.filter(p=>p.life>0);
  // Obstacles
  obstacles.forEach(o=>{{
    ctx.fillStyle=o.color;ctx.shadowColor=o.color;ctx.shadowBlur=8;
    ctx.fillRect(o.x-o.w/2,o.y-o.h/2,o.w,o.h);ctx.shadowBlur=0;
  }});
  // Coins
  coins.forEach(c=>{{
    if(c.collected)return;
    ctx.save();ctx.shadowColor='{G_COLOR}';ctx.shadowBlur=10;
    ctx.fillStyle='{G_COLOR}';ctx.beginPath();ctx.arc(c.x,c.y,c.r,0,Math.PI*2);ctx.fill();ctx.restore();
  }});
  // Car
  ctx.save();
  if(boost>0){{ctx.shadowColor='{G_COLOR}';ctx.shadowBlur=20;}}
  ctx.fillStyle=boost>0?'{G_COLOR}':'#ffffff';
  ctx.fillRect(car.x-car.w/2,car.y-car.h/2,car.w,car.h);
  // Windows
  ctx.fillStyle='rgba(0,200,255,.4)';
  ctx.fillRect(car.x-car.w/2+4,car.y-car.h/2+6,car.w-8,14);
  // Exhaust if boost
  if(boost>0){{
    for(let i=0;i<3;i++) mkP(car.x+R(-8,8),car.y+car.h/2+5,'{G_COLOR}',1);
  }}
  ctx.restore();
  updateHUD();
}}
function gameOver(){{
  document.getElementById('final-score').textContent='DISTANCE: '+Math.floor(score);
  document.getElementById('over-screen').classList.remove('hidden');
}}
</script>
</body></html>"""

# ── SELECT AND BUILD THE RIGHT GAME ───────────────────────
if   GAME_TYPE == "shooter":    html5_game = build_shooter_game()
elif GAME_TYPE == "wave":       html5_game = build_wave_game()
elif GAME_TYPE == "platformer": html5_game = build_platformer_game()
elif GAME_TYPE == "puzzle":     html5_game = build_puzzle_game()
elif GAME_TYPE == "racer":      html5_game = build_racer_game()
else:                            html5_game = build_shooter_game()

print(f"  ✅ HTML5 game built ({GAME_TYPE}, {len(html5_game)//1024}KB)")

# ═══════════════════════════════════════════════════════════
#  WORKSPACE & GODOT PROJECT
# ═══════════════════════════════════════════════════════════
print("  📁 Building workspace...")
proj_dir = Path(f"workspace/{SAFE_NAME}")
proj_dir.mkdir(parents=True, exist_ok=True)

(proj_dir / "index.html").write_text(html5_game, encoding="utf-8")
if sprite.exists(): shutil.copy(sprite, proj_dir / "icon.png")

(proj_dir / "project.godot").write_text(
    f'[application]\nconfig/name="{GAME_NAME}"\nconfig/icon="res://icon.png"\n'
    f'[display]\nwindow/size/viewport_width=480\nwindow/size/viewport_height=854\n'
)
(proj_dir / "main.tscn").write_text(
    '[gd_scene format=3]\n[node name="Main" type="Node2D"]\n'
    '[node name="Player" type="CharacterBody2D" parent="."]\n'
)
(proj_dir / "player.gd").write_text(
    f'extends CharacterBody2D\n\n'
    f'const SPEED = 200.0\n\n'
    f'func _ready():\n'
    f'\tprint("{GAME_NAME} - {GENRE}")\n'
    f'\tprint("Mechanic: {MECHANIC}")\n\n'
    f'func _physics_process(delta):\n'
    f'\tvar dir = Input.get_vector("ui_left","ui_right","ui_up","ui_down")\n'
    f'\tvelocity = dir * SPEED\n'
    f'\tmove_and_slide()\n'
)
(proj_dir / "README.md").write_text(
    f"# {GAME_NAME}\n\n"
    f"**Studio:** DeathRoll  \n"
    f"**Genre:** {GENRE}  \n"
    f"**Mechanic:** {MECHANIC}  \n"
    f"**Description:** {MECH_DESC}  \n\n"
    f"> {DESCRIPTION}\n\n"
    f"## Play\n🌐 [Play in browser]({PLAY_URL})\n\n"
    f"## Buy Full Source\n"
    f"💰 ${GAME_PRICE} SOL  \n"
    f"Telegram: {BRAND_TELEGRAM}  \n"
    f"Channel: {TELEGRAM_CHANNEL}  \n\n"
    f"## License Key\n`{LICENSE_KEY}`\n\n"
    f"---\n"
    f"Built automatically by [DeathRoll Studio]({BRAND_WEBSITE})\n"
)

# ═══════════════════════════════════════════════════════════
#  ZIP
# ═══════════════════════════════════════════════════════════
zip_path = Path("workspace/latest_game.zip")
try:
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in proj_dir.rglob("*"):
            if f.is_file(): zf.write(f, f.relative_to(proj_dir.parent))
    print(f"  ✅ ZIP: {zip_path.stat().st_size//1024}KB")
except Exception as e:
    print(f"  ⚠️  ZIP failed: {e}")

# ═══════════════════════════════════════════════════════════
#  UPDATE PORTFOLIO WITH FINAL STATUS
# ═══════════════════════════════════════════════════════════
try:
    cur = json.loads(port_path.read_text())
    for g in cur:
        if g["game"] == GAME_NAME:
            g["art_success"] = art_ok
            g["status"]      = "complete"
            g["game_type"]   = GAME_TYPE
    port_path.write_text(json.dumps(cur, indent=2))
except: pass

# ═══════════════════════════════════════════════════════════
#  GENERATE STOREFRONT  index.html  (updates every run)
# ═══════════════════════════════════════════════════════════
print("  🌐 Regenerating storefront...")

def build_storefront(entries: list) -> str:
    recent_entries = list(reversed(entries[-20:]))
    cards_html = ""
    for e in recent_entries:
        gname   = e.get("game","?")
        ggenre  = e.get("genre","?")
        gdesc   = e.get("description","")[:80]
        gmech   = e.get("mechanic","?")
        gimg    = e.get("image_url","")
        gplay   = e.get("play_url","#")
        gprice  = e.get("price_sol","7")
        gcolor  = e.get("color","#4ecdbc")
        gdate   = e.get("date","")[:10]
        cards_html += f"""
        <div class="card" style="--c:{gcolor}">
          <div class="card-img" style="background:url('{gimg}') center/cover no-repeat,#111;">
            <div class="card-badge">{ggenre.upper()}</div>
          </div>
          <div class="card-body">
            <h3>{gname}</h3>
            <p class="desc">{gdesc}</p>
            <div class="mech">⚡ {gmech}</div>
            <div class="card-foot">
              <span class="price">{gprice} SOL</span>
              <a href="{gplay}" class="play-btn" target="_blank">▶ PLAY FREE</a>
            </div>
            <div class="card-date">{gdate}</div>
          </div>
        </div>"""

    total = len(entries)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>DeathRoll Studio — Daily Mobile Games</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
:root{{
  --acc:#4ecdbc;--bg:#06060e;--card:#0d0d18;--border:#1e1e30;
  --txt:#e0e0e0;--dim:#888;
}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html{{scroll-behavior:smooth;}}
body{{background:var(--bg);color:var(--txt);font-family:'Share Tech Mono',monospace;
     min-height:100vh;overflow-x:hidden;}}
/* ── Header ── */
header{{
  position:sticky;top:0;z-index:100;
  background:rgba(6,6,14,.95);
  border-bottom:1px solid var(--border);
  backdrop-filter:blur(12px);
  padding:12px 20px;
  display:flex;align-items:center;justify-content:space-between;
  gap:12px;flex-wrap:wrap;
}}
.logo{{
  font-family:'Orbitron',sans-serif;font-weight:900;
  font-size:clamp(18px,4vw,26px);
  color:var(--acc);text-shadow:0 0 20px var(--acc);
  letter-spacing:2px;text-decoration:none;
}}
.logo span{{color:#fff;}}
nav{{display:flex;gap:16px;flex-wrap:wrap;}}
nav a{{color:var(--dim);font-size:12px;text-decoration:none;letter-spacing:1px;
       transition:color .2s;}}
nav a:hover{{color:var(--acc);}}
.live-badge{{
  background:rgba(255,50,50,.15);border:1px solid #ff3232;
  color:#ff5555;font-size:10px;padding:3px 8px;border-radius:3px;
  animation:pulse-badge 2s infinite;letter-spacing:2px;
}}
@keyframes pulse-badge{{0%,100%{{opacity:1}}50%{{opacity:.5}}}}
/* ── Hero ── */
.hero{{
  padding:60px 20px 40px;text-align:center;
  background:radial-gradient(ellipse 70% 40% at 50% 0%,
    rgba(78,205,188,.08) 0%,transparent 70%);
  position:relative;overflow:hidden;
}}
.hero::before{{
  content:'';position:absolute;inset:0;
  background:repeating-linear-gradient(0deg,transparent,transparent 39px,
    rgba(255,255,255,.02) 40px),
    repeating-linear-gradient(90deg,transparent,transparent 39px,
    rgba(255,255,255,.02) 40px);
}}
.hero h1{{
  font-family:'Orbitron',sans-serif;
  font-size:clamp(28px,8vw,64px);font-weight:900;
  line-height:1.05;position:relative;
  background:linear-gradient(135deg,#fff 30%,var(--acc));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
}}
.hero p{{color:var(--dim);font-size:14px;margin:14px auto;max-width:480px;line-height:1.7;}}
.stats-row{{
  display:flex;justify-content:center;gap:32px;flex-wrap:wrap;
  margin:28px auto;max-width:500px;
}}
.stat{{text-align:center;}}
.stat .n{{font-family:'Orbitron',sans-serif;font-size:clamp(24px,5vw,36px);
           color:var(--acc);text-shadow:0 0 16px var(--acc);}}
.stat .l{{font-size:10px;color:var(--dim);letter-spacing:2px;margin-top:2px;}}
.cta-row{{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:20px;}}
.cta{{padding:12px 28px;font-family:inherit;font-size:13px;letter-spacing:2px;
       cursor:pointer;text-decoration:none;display:inline-block;}}
.cta-primary{{background:var(--acc);color:#000;font-weight:bold;}}
.cta-primary:hover{{background:#fff;}}
.cta-secondary{{border:1px solid var(--acc);color:var(--acc);background:transparent;}}
.cta-secondary:hover{{background:rgba(78,205,188,.1);}}
/* ── Game grid ── */
.section{{padding:32px 16px;max-width:1100px;margin:0 auto;}}
.section-title{{
  font-family:'Orbitron',sans-serif;font-size:16px;color:var(--acc);
  letter-spacing:3px;margin-bottom:20px;display:flex;align-items:center;gap:10px;
}}
.section-title::after{{content:'';flex:1;height:1px;background:var(--border);}}
.grid{{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(min(100%,280px),1fr));
  gap:16px;
}}
.card{{
  background:var(--card);border:1px solid var(--border);
  transition:transform .25s,border-color .25s,box-shadow .25s;
  position:relative;overflow:hidden;
}}
.card:hover{{
  transform:translateY(-4px);
  border-color:var(--c,var(--acc));
  box-shadow:0 8px 32px rgba(0,0,0,.5),0 0 0 1px var(--c,var(--acc))44;
}}
.card-img{{
  height:180px;position:relative;
  background:#111;
}}
.card-img::after{{
  content:'';position:absolute;inset:0;
  background:linear-gradient(to bottom,transparent 60%,var(--card));
}}
.card-badge{{
  position:absolute;top:10px;left:10px;z-index:1;
  background:rgba(0,0,0,.75);border:1px solid var(--c,var(--acc));
  color:var(--c,var(--acc));font-size:9px;padding:3px 8px;letter-spacing:1.5px;
}}
.card-body{{padding:14px;}}
.card-body h3{{font-family:'Orbitron',sans-serif;font-size:14px;
               color:#fff;margin-bottom:6px;}}
.desc{{font-size:11px;color:var(--dim);line-height:1.5;margin-bottom:8px;min-height:32px;}}
.mech{{font-size:10px;color:var(--c,var(--acc));margin-bottom:10px;}}
.card-foot{{display:flex;align-items:center;justify-content:space-between;}}
.price{{font-size:13px;color:#fff;font-family:'Orbitron',sans-serif;}}
.play-btn{{
  background:var(--c,var(--acc));color:#000;font-family:inherit;
  font-size:11px;padding:7px 14px;letter-spacing:1px;
  text-decoration:none;font-weight:bold;transition:opacity .2s;
}}
.play-btn:hover{{opacity:.8;}}
.card-date{{font-size:9px;color:#444;margin-top:8px;}}
/* ── How to Buy ── */
.buy-section{{
  padding:40px 20px;max-width:700px;margin:0 auto;text-align:center;
}}
.buy-section h2{{font-family:'Orbitron',sans-serif;font-size:18px;
                  color:var(--acc);margin-bottom:24px;letter-spacing:2px;}}
.steps{{display:flex;flex-direction:column;gap:16px;text-align:left;}}
.step{{display:flex;gap:16px;align-items:flex-start;padding:16px;
        border:1px solid var(--border);background:var(--card);}}
.step-num{{font-family:'Orbitron',sans-serif;font-size:22px;color:var(--acc);
            min-width:32px;line-height:1;}}
.step h4{{font-size:13px;color:#fff;margin-bottom:4px;}}
.step p{{font-size:11px;color:var(--dim);line-height:1.5;}}
/* ── Wallets ── */
.wallet-box{{
  margin:28px 0;padding:20px;background:var(--card);
  border:1px solid var(--border);word-break:break-all;
}}
.wallet-row{{display:flex;align-items:flex-start;gap:10px;margin:8px 0;font-size:11px;}}
.wallet-ico{{font-size:16px;flex-shrink:0;}}
.wallet-addr{{color:var(--acc);font-size:10px;margin-top:2px;}}
/* ── Footer ── */
footer{{
  border-top:1px solid var(--border);padding:28px 20px;
  text-align:center;font-size:11px;color:var(--dim);
}}
footer a{{color:var(--acc);text-decoration:none;}}
footer .links{{display:flex;justify-content:center;gap:20px;flex-wrap:wrap;margin-bottom:12px;}}
/* ── Ticker ── */
.ticker{{
  background:#0a0a14;border-top:1px solid var(--border);
  border-bottom:1px solid var(--border);overflow:hidden;
  height:32px;display:flex;align-items:center;
}}
.ticker-inner{{
  white-space:nowrap;font-size:11px;color:var(--dim);
  animation:ticker-scroll 30s linear infinite;padding-left:100%;
}}
.ticker-inner span{{color:var(--acc);margin-right:4px;}}
@keyframes ticker-scroll{{from{{transform:translateX(0)}}to{{transform:translateX(-100%)}}}}
/* Responsive */
@media(max-width:480px){{
  .hero h1{{font-size:32px;}}
  .stats-row{{gap:20px;}}
  .stat .n{{font-size:28px;}}
}}
</style>
</head>
<body>

<header>
  <a href="#" class="logo">DEATH<span>ROLL</span></a>
  <nav>
    <a href="#games">GAMES</a>
    <a href="#buy">BUY</a>
    <a href="https://t.me/{TELEGRAM_CHANNEL.lstrip('@')}" target="_blank">TELEGRAM</a>
    <a href="https://tiktok.com/@deathroll.co" target="_blank">TIKTOK</a>
  </nav>
  <div class="live-badge">● LIVE DAILY</div>
</header>

<div class="ticker">
  <div class="ticker-inner">
    {''.join(f'<span>⚡</span>{e["game"]} [{e["genre"]}] — ' for e in recent_entries[:8])}
    NEW GAME EVERY DAY AT 6AM UTC &nbsp;&nbsp;&nbsp;
  </div>
</div>

<section class="hero">
  <h1>DAILY MOBILE<br>GAME FACTORY</h1>
  <p>A new playable mobile game drops every single day — free to play in your browser, 
     full Godot source for just {GAME_PRICE} SOL.</p>
  <div class="stats-row">
    <div class="stat"><div class="n">{total}</div><div class="l">GAMES BUILT</div></div>
    <div class="stat"><div class="n">{GAME_PRICE}</div><div class="l">SOL PER GAME</div></div>
    <div class="stat"><div class="n">∞</div><div class="l">PLAYABLE FREE</div></div>
  </div>
  <div class="cta-row">
    <a href="#games" class="cta cta-primary">BROWSE GAMES</a>
    <a href="https://t.me/{TELEGRAM_CHANNEL.lstrip('@')}" class="cta cta-secondary" target="_blank">TELEGRAM CHANNEL</a>
  </div>
</section>

<section id="games" class="section">
  <div class="section-title">LATEST GAMES</div>
  <div class="grid">
    {cards_html}
  </div>
</section>

<section id="buy" class="buy-section">
  <h2>HOW TO BUY</h2>
  <div class="steps">
    <div class="step">
      <div class="step-num">01</div>
      <div><h4>Play any game for free</h4>
      <p>Every game is 100% free to play in your mobile browser — no download needed.</p></div>
    </div>
    <div class="step">
      <div class="step-num">02</div>
      <div><h4>Send {GAME_PRICE} SOL + your @username</h4>
      <p>Use Trust Wallet or Phantom to send SOL to either address below.</p></div>
    </div>
    <div class="step">
      <div class="step-num">03</div>
      <div><h4>Receive instantly</h4>
      <p>Get the full Godot 4 source code, HTML5 build, and license key — delivered to your Telegram.</p></div>
    </div>
  </div>

  <div class="wallet-box">
    <div class="wallet-row">
      <div class="wallet-ico">🔵</div>
      <div><div style="font-size:11px;color:#aaa;">Trust Wallet (Solana)</div>
      <div class="wallet-addr">{SOLANA_TRUST}</div></div>
    </div>
    <div class="wallet-row">
      <div class="wallet-ico">🟣</div>
      <div><div style="font-size:11px;color:#aaa;">Phantom Wallet (Solana)</div>
      <div class="wallet-addr">{SOLANA_PHANTOM}</div></div>
    </div>
  </div>

  <a href="https://t.me/{BRAND_TELEGRAM.lstrip('@')}" class="cta cta-primary" target="_blank">
    DM {BRAND_TELEGRAM} ON TELEGRAM
  </a>
</section>

<footer>
  <div class="links">
    <a href="https://t.me/{TELEGRAM_CHANNEL.lstrip('@')}" target="_blank">Telegram Channel</a>
    <a href="https://t.me/{BRAND_TELEGRAM.lstrip('@')}" target="_blank">Direct DM</a>
    <a href="https://tiktok.com/@deathroll.co" target="_blank">TikTok</a>
    <a href="mailto:favouradeleke246@gmail.com">Email</a>
    <a href="https://github.com/{BRAND_GITHUB}" target="_blank">GitHub</a>
  </div>
  <p>© {datetime.now().year} DeathRoll Studio — {total} games and counting.</p>
  <p style="margin-top:6px;font-size:10px;color:#333;">
    Automated by DeathRoll Studio v{BOT_VERSION} — New game daily at 6AM UTC
  </p>
</footer>

</body>
</html>"""

# Write storefront
storefront_html = build_storefront(entries)
Path("index.html").write_text(storefront_html, encoding="utf-8")
print(f"  ✅ Storefront updated ({len(storefront_html)//1024}KB)")

# ═══════════════════════════════════════════════════════════
#  TELEGRAM  — Sales post + admin bundle
# ═══════════════════════════════════════════════════════════
print("  📱 Sending Telegram posts...")

sales_post = (
    f"{EMOJI_STR} *{HOOK}* {EMOJI_STR}\n\n"
    f"✨ *{GAME_NAME}* — {GENRE}\n"
    f"_{DESCRIPTION}_\n\n"
    f"⚡ *Mechanic:* `{MECHANIC}`\n"
    f"📱 _Mobile-first, plays in any browser_\n\n"
    f"🕹️ *Play FREE:* {PLAY_URL}\n\n"
    f"💰 *Full source:* ${GAME_PRICE} SOL\n"
    f"🔵 Trust: `{SOLANA_TRUST}`\n"
    f"🟣 Phantom: `{SOLANA_PHANTOM}`\n\n"
    f"Send ${GAME_PRICE} SOL + @username → instant delivery\n\n"
    f"{TAGS}"
)

if TG_TOKEN and sprite.exists():
    ok = tg_send_photo(TELEGRAM_CHANNEL, sprite, sales_post)
    print(f"  {'✅' if ok else '⚠️ '} Channel post")

if TG_TOKEN and TG_ADMIN and zip_path.exists():
    admin_caption = (
        f"🎮 *{GAME_NAME}* — {GAME_TYPE}\n"
        f"Genre: {GENRE}\nMechanic: {MECHANIC}\n"
        f"Art: {'✅' if art_ok else '⚠️'}\n"
        f"Games: {len(entries)}\nKey: `{LICENSE_KEY}`\n"
        f"Play: {PLAY_URL}"
    )
    ok = tg_send_doc(TG_ADMIN, zip_path, admin_caption)
    print(f"  {'✅' if ok else '⚠️ '} Admin bundle")

# ═══════════════════════════════════════════════════════════
#  AUTO-DELIVERY  — /deliver @username command
# ═══════════════════════════════════════════════════════════
print("  🤖 Processing delivery queue...")

def send_to_buyer(username: str):
    msg = (
        f"🎮 *Your game is ready!*\n\n"
        f"✨ *{GAME_NAME}* — {GENRE}\n"
        f"⚡ Mechanic: {MECHANIC}\n"
        f"_{DESCRIPTION}_\n\n"
        f"🕹️ *Play in browser:*\n{PLAY_URL}\n\n"
        f"📦 *Download source (Godot 4):*\n{ZIP_URL}\n\n"
        f"🔑 *License:* `{LICENSE_KEY}`\n\n"
        f"Thanks for supporting DeathRoll Studio! 🔥\n"
        f"New game every day → {TELEGRAM_CHANNEL}"
    )
    tg_send_message(f"@{username.lstrip('@')}", msg)

def process_queue():
    if not (TG_TOKEN and TG_ADMIN): return
    try:
        r = requests.get(f"{TG_BASE}/getUpdates",
                         params={"limit":50,"timeout":3}, timeout=12)
        if r.status_code != 200: return
        updates = r.json().get("result",[])
        last_id = 0
        for upd in updates:
            uid  = upd.get("update_id",0)
            last_id = max(last_id, uid)
            msg  = upd.get("message",{})
            text = msg.get("text","").strip()
            cid  = str(msg.get("chat",{}).get("id",""))
            if cid != str(TG_ADMIN): continue
            for prefix in ["/deliver ","/DELIVER ","DELIVER ","deliver "]:
                if text.startswith(prefix):
                    uname = text[len(prefix):].strip().lstrip("@")
                    send_to_buyer(uname)
                    tg_send_message(TG_ADMIN, f"✅ Delivered {GAME_NAME} to @{uname}")
                    print(f"  ✅ Delivered to @{uname}")
        # Acknowledge updates so they don't replay
        if last_id:
            requests.get(f"{TG_BASE}/getUpdates",
                         params={"offset":last_id+1,"limit":1,"timeout":1}, timeout=5)
    except Exception as e:
        print(f"  ⚠️  Queue: {e}")

process_queue()

# ═══════════════════════════════════════════════════════════
#  GITHUB  — Create per-game repo
# ═══════════════════════════════════════════════════════════
if GH_TOKEN:
    try:
        r = requests.post("https://api.github.com/user/repos",
            headers={"Authorization":f"token {GH_TOKEN}","Accept":"application/vnd.github.v3+json"},
            json={"name":f"dr-{SAFE_NAME.lower()}",
                  "description":f"{DESCRIPTION[:100]} | DeathRoll Studio",
                  "private":False,"has_pages":True},
            timeout=30)
        if r.status_code == 201:
            print(f"  ✅ Repo: {r.json()['html_url']}")
    except Exception as e:
        print(f"  ⚠️  Repo: {e}")

# ═══════════════════════════════════════════════════════════
#  SAR UPDATE
# ═══════════════════════════════════════════════════════════
SAR["study"]["total_runs"] += 1
if art_ok: SAR["study"]["art_ok"] += 1
else:       SAR["study"]["art_fail"] += 1

SAR["study"]["games"].append({
    "name":game_name,"genre":GENRE,"mechanic":MECHANIC,
    "hook":HOOK,"ts":datetime.now().isoformat(),"art":art_ok,
    "game_type":GAME_TYPE
})
SAR["study"]["games"] = SAR["study"]["games"][-100:]

# Analyse
gs: dict = {}
for g in SAR["study"]["games"]:
    gn = g["genre"]
    if gn not in gs: gs[gn]={"count":0,"art":0}
    gs[gn]["count"]+=1
    if g.get("art"): gs[gn]["art"]+=1

if gs:
    SAR["analysis"]["best_genre"] = max(gs,key=lambda x:gs[x]["art"]/max(gs[x]["count"],1))
    SAR["analysis"]["rate"] = round(SAR["study"]["art_ok"]/max(SAR["study"]["total_runs"],1),3)

sar_path.write_text(json.dumps(SAR,indent=2))

# ═══════════════════════════════════════════════════════════
#  METADATA
# ═══════════════════════════════════════════════════════════
Path("learning_data.json").write_text(json.dumps({
    "ts":datetime.now().isoformat(),"game":GAME_NAME,"genre":GENRE,
    "mechanic":MECHANIC,"art_ok":art_ok,"game_type":GAME_TYPE,
    "play_url":PLAY_URL,"total":len(entries),"sar_runs":SAR["study"]["total_runs"],
},indent=2))
Path("build_info.txt").write_text(
    f"DEATHROLL STUDIO v{BOT_VERSION}\n"
    f"Game     : {GAME_NAME}\nGenre    : {GENRE}\n"
    f"Type     : {GAME_TYPE}\nMechanic : {MECHANIC}\n"
    f"Art      : {'OK' if art_ok else 'FALLBACK'}\n"
    f"Date     : {datetime.now().isoformat()}\n"
    f"Portfolio: {len(entries)}\nSAR runs : {SAR['study']['total_runs']}\n"
    f"Play     : {PLAY_URL}\n"
)
Path("last_run.txt").write_text(datetime.now().isoformat())
Path("last_update.txt").write_text(datetime.now().isoformat())

# ═══════════════════════════════════════════════════════════
#  FINAL REPORT
# ═══════════════════════════════════════════════════════════
print()
print("╔══════════════════════════════════════════════════════╗")
print("║  ✅  DEATHROLL STUDIO v30.0  —  COMPLETE            ║")
print("╠══════════════════════════════════════════════════════╣")
print(f"║  Game    : {GAME_NAME:<41}║")
print(f"║  Genre   : {GENRE:<41}║")
print(f"║  Type    : {GAME_TYPE:<41}║")
print(f"║  Mechanic: {MECHANIC:<41}║")
print(f"║  Art     : {'✅ Online' if art_ok else '✅ Fallback':<41}║")
print(f"║  Games   : {str(len(entries))+' in portfolio':<41}║")
print(f"║  SAR     : Run #{str(SAR['study']['total_runs'])+', '+str(SAR['analysis']['rate']*100)[:4]+'% art rate':<37}║")
print("╚══════════════════════════════════════════════════════╝")
print(f"  🌐 {BASE_URL}/")
print(f"  📱 https://t.me/{TELEGRAM_CHANNEL.lstrip('@')}")
