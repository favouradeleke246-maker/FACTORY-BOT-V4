#!/usr/bin/env python3
"""
DEATHROLL STUDIO v30.0 — GAME FACTORY (AI + TRENDS + SAR)
Generates a new mobile game every day, posts to Telegram & WhatsApp.
"""
import os, json, random, requests, shutil, zipfile, hashlib
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image, ImageDraw
    PIL_OK = True
except ImportError:
    PIL_OK = False

# ---------- CONFIG ----------
BOT_VERSION = "30.0.0"
BRAND_GITHUB = "favouradeleke246-maker"
BRAND_REPO = "FACTORY-BOT-V4"
TELEGRAM_CHANNEL = "@drolltech"
WHATSAPP_WEBHOOK_URL = os.getenv("WHATSAPP_WEBHOOK_URL", "")  # Your WhatsApp API endpoint
SOLANA_TRUST = "6wsQ6nGXrUUUGCEokb4rZcfHDv2a8MomUb22TuVaH2m3"
SOLANA_PHANTOM = "Csk9DKstWMdKx19gUHWB9xy2VwZZX2nx6V6oSVGDCgMb"
GAME_PRICE = os.getenv("GAME_PRICE", "7")
TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TG_ADMIN = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GH_TOKEN = os.getenv("GH_TOKEN")

BASE_URL = f"https://{BRAND_GITHUB}.github.io/{BRAND_REPO}"
RAW_URL = f"https://raw.githubusercontent.com/{BRAND_GITHUB}/{BRAND_REPO}/main"

# ---------- TELEGRAM HELPERS ----------
def tg_send_photo(chat_id, photo_path, caption):
    if not TG_TOKEN: return False
    try:
        with open(photo_path, "rb") as f:
            r = requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto",
                files={"photo": f}, data={"chat_id": chat_id, "caption": caption,
                "parse_mode": "Markdown"}, timeout=40)
        return r.status_code == 200
    except: return False

def tg_send_doc(chat_id, doc_path, caption):
    if not TG_TOKEN: return False
    try:
        with open(doc_path, "rb") as f:
            r = requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendDocument",
                files={"document": f}, data={"chat_id": chat_id, "caption": caption,
                "parse_mode": "Markdown"}, timeout=90)
        return r.status_code == 200
    except: return False

# ---------- WHATSAPP HELPERS (placeholder) ----------
def send_to_whatsapp(text, image_url=None):
    """Send game info to WhatsApp channel via webhook.
       Replace with actual WhatsApp Business API call."""
    if not WHATSAPP_WEBHOOK_URL:
        print("  ⚠️  WhatsApp webhook not set. Skipping.")
        return False
    payload = {"text": text, "image_url": image_url}
    try:
        r = requests.post(WHATSAPP_WEBHOOK_URL, json=payload, timeout=15)
        return r.status_code == 200
    except Exception as e:
        print(f"  ⚠️  WhatsApp send error: {e}")
        return False

# ---------- OPENAI ----------
def call_openai(prompt, max_tokens=200, system=""):
    if not OPENAI_KEY: return None
    try:
        r = requests.post("https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_KEY}", "content-type": "application/json"},
            json={"model": "gpt-4o-mini", "max_tokens": max_tokens,
                  "messages": ([{"role":"system","content":system}] if system else []) + [{"role":"user","content":prompt}]},
            timeout=40)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip().strip('"')
    except: pass
    return None

# ---------- GENRES ----------
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
print(f"║  DEATHROLL STUDIO v{BOT_VERSION}  —  TITAN EDITION     ║")
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

# AI Mechanic
print("  ⚙️  Generating mechanic...")
def gen_mechanic():
    if OPENAI_KEY:
        res = call_openai(f"Invent one UNIQUE, surprising game mechanic for a mobile {GENRE} game.\nIt must work well with TOUCH controls (tap, swipe, hold).\nReply EXACTLY:\nMECHANIC: <short name 2-4 words>\nDESCRIPTION: <one punchy sentence max 18 words>", max_tokens=100, system="You are a genius indie game designer. Be creative and unexpected.")
        if res:
            name = desc = None
            for line in res.splitlines():
                if line.startswith("MECHANIC:"): name = line.split(":",1)[1].strip()
                elif line.startswith("DESCRIPTION:"): desc = line.split(":",1)[1].strip()
            if name and desc and 2 < len(name) < 40: return name, desc
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

# AI Description
def gen_description():
    if OPENAI_KEY:
        res = call_openai(f"Write ONE thrilling sentence (max 110 chars) for a mobile {GENRE} game called '{GAME_NAME}' featuring '{MECHANIC}'. Sound exciting, edgy, like a trailer tagline. No quotes.", max_tokens=60, system="You write killer indie game marketing copy.")
        if res and len(res) > 15: return res[:120]
    return f"Master {MECHANIC} in this {GENRE} — no two sessions are the same."
DESCRIPTION = gen_description()
HOOK = random.choice(HOOKS)
TAGS = f"#gamedev #indiegame #mobilegame #{GENRE.replace(' ','').replace('-','')} #{MECHANIC.replace(' ','')} #DeathRollStudio #solanagaming"
print(f"  📝 {DESCRIPTION}")

# License key
LICENSE_KEY = "DR-" + hashlib.md5(f"{GAME_NAME}{datetime.now().date()}{SOLANA_TRUST}".encode()).hexdigest()[:16].upper()

# Portfolio
port_path = Path("portfolio.json")
entries = []
if port_path.exists():
    try:
        raw = port_path.read_text().strip()
        if raw: entries = json.loads(raw)
        if not isinstance(entries, list): entries = []
    except: entries = []
entry = {"id": f"game_{len(entries)+1:04d}", "date": datetime.now().isoformat(), "game": GAME_NAME, "genre": GENRE, "mechanic": MECHANIC, "mech_desc": MECH_DESC, "description": DESCRIPTION, "hook": HOOK, "hashtags": TAGS, "image_url": IMG_URL, "play_url": PLAY_URL, "zip_url": ZIP_URL, "price_sol": GAME_PRICE, "license_key": LICENSE_KEY, "color": G_COLOR, "sales": 0, "status": "generating"}
entries.append(entry)
entries = entries[-300:]
port_path.write_text(json.dumps(entries, indent=2))
print(f"  💾 Portfolio: {len(entries)} games")

# Art generation
print("  🎨 Generating art...")
sprite = Path("sprite.png")
art_ok = False
style = random.choice(["isometric 3D render with dramatic neon lighting", "dark cyberpunk concept art, ultra detailed", "low-poly 3D character, game-ready", "cell-shaded game art, bold outlines", "dark fantasy concept art, cinematic", "retro-futuristic sci-fi illustration", "gritty noir game poster style", "hyper-detailed 3D render, unreal engine style"])
art_pmt = f"{style}, {GENRE} game character for '{GAME_NAME}', professional game art, dark background, dramatic"
try:
    enc = art_pmt.replace(" ","+").replace(",","%2C").replace("'","%27")
    url = f"https://image.pollinations.ai/prompt/{enc}?width=512&height=512&seed={random.randint(1,999999)}&nologo=true"
    r = requests.get(url, timeout=40)
    if r.status_code == 200 and len(r.content) > 8000:
        sprite.write_bytes(r.content)
        art_ok = True
        print(f"  ✅ Art: {style[:40]}...")
except Exception as e:
    print(f"  ⚠️  Pollinations: {e}")
if not art_ok and PIL_OK:
    img = Image.new("RGB", (512, 512), (10,5,20))
    draw = ImageDraw.Draw(img)
    for y in range(0,512,4): draw.line([(0,y),(512,y)], fill=(0,int(G_COLOR[3:5],16)//4,int(G_COLOR[5:7],16)//4))
    cx,cy = 256,256
    for rad in [180,140,100,60]:
        clr = bytes.fromhex(G_COLOR[1:])
        draw.ellipse([cx-rad,cy-rad,cx+rad,cy+rad], outline=(*clr, max(20,80-(180-rad)//2)), width=2)
    pts = [(cx,cy-80),(cx+70,cy),(cx,cy+80),(cx-70,cy)]
    draw.polygon(pts, fill=(*bytes.fromhex(G_COLOR[1:]),180))
    draw.polygon(pts, outline=(255,255,255,200), width=2)
    draw.text((cx,cy-130), GAME_NAME, fill=(255,255,255), anchor="mm")
    draw.text((cx,cy+110), GENRE.upper(), fill=(*bytes.fromhex(G_COLOR[1:]),), anchor="mm")
    draw.text((cx,cy+140), f"⚡ {MECHANIC}", fill=(200,200,200), anchor="mm")
    img.save(sprite)
    art_ok = True
    print("  ✅ Fallback art generated")

# ---------- SHARED HTML5 COMPONENTS ----------
SHARED_HEAD = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<title>{GAME_NAME}</title>
<style>
:root{{--acc:{G_COLOR};--bg:{G_BG};}}
*{{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}}
html,body{{width:100%;height:100%;overflow:hidden;background:var(--bg);}}
body{{display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Courier New',monospace;color:#e8e8e8;touch-action:none;}}
#wrap{{position:relative;width:100%;max-width:480px;height:100vh;max-height:820px;overflow:hidden;display:flex;flex-direction:column;}}
#hud{{display:flex;justify-content:space-between;align-items:center;padding:8px 12px;background:rgba(0,0,0,.7);border-bottom:1px solid var(--acc);font-size:13px;gap:8px;flex-shrink:0;}}
canvas{{flex:1;width:100%;display:block;}}
#joy-zone{{position:absolute;bottom:0;left:0;width:50%;height:44%;display:flex;align-items:center;justify-content:center;}}
#joy-outer{{width:90px;height:90px;border-radius:50%;border:2px solid rgba(255,255,255,.25);background:rgba(0,0,0,.35);position:relative;display:flex;align-items:center;justify-content:center;}}
#joy-inner{{width:38px;height:38px;border-radius:50%;background:var(--acc);opacity:.85;position:absolute;box-shadow:0 0 14px var(--acc);pointer-events:none;}}
#btn-zone{{position:absolute;bottom:0;right:0;width:50%;height:44%;display:flex;align-items:center;justify-content:center;gap:18px;}}
.abtn{{width:56px;height:56px;border-radius:50%;border:2px solid var(--acc);background:rgba(0,0,0,.5);color:var(--acc);font-size:20px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 12px var(--acc)44;cursor:pointer;user-select:none;}}
.abtn:active{{background:var(--acc)33;transform:scale(.93);}}
.screen{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(0,0,0,.88);z-index:99;text-align:center;padding:24px;}}
.screen.hidden{{display:none;}}
.screen h1{{font-size:clamp(22px,6vw,36px);color:var(--acc);text-shadow:0 0 20px var(--acc);margin-bottom:10px;letter-spacing:2px;}}
.screen h2{{font-size:clamp(16px,4vw,24px);color:#fff;margin-bottom:8px;}}
.screen p{{font-size:13px;color:#aaa;margin:4px 0;line-height:1.5;}}
.screen .mechanic-pill{{margin:12px auto;padding:8px 18px;border:1px solid var(--acc);border-radius:20px;color:var(--acc);font-size:12px;max-width:280px;}}
.bigbtn{{margin-top:16px;padding:14px 36px;background:var(--acc);color:#000;font-family:inherit;font-size:16px;font-weight:bold;border:none;cursor:pointer;text-transform:uppercase;}}
.bigbtn:active{{opacity:.8;transform:scale(.97);}}
#score-ring{{width:72px;height:72px;border-radius:50%;border:3px solid var(--acc);display:flex;align-items:center;justify-content:center;flex-direction:column;}}
#score-ring .num{{font-size:20px;color:var(--acc);line-height:1;}}
#score-ring .lbl{{font-size:8px;color:#888;}}
#lives-row{{display:flex;gap:4px;}}
.life-pip{{width:10px;height:10px;border-radius:50%;background:var(--acc);box-shadow:0 0 6px var(--acc);}}
.life-pip.dead{{background:#333;box-shadow:none;}}
#special-bar{{flex:1;height:6px;background:#1a1a1a;border-radius:3px;overflow:hidden;}}
#special-fill{{height:100%;background:var(--acc);width:0%;transition:width .1s;box-shadow:0 0 4px var(--acc);}}
#brand-strip{{position:absolute;top:0;right:0;font-size:9px;color:#333;padding:3px 6px;letter-spacing:1px;}}
@media(orientation:landscape){{
  #wrap{{flex-direction:row;max-width:none;max-height:480px;height:100%;}}
  #hud{{flex-direction:column;width:80px;border-bottom:none;border-right:1px solid var(--acc);}}
  #joy-zone{{width:25%;height:100%;}}
  #btn-zone{{width:25%;height:100%;}}
}}
</style>
</head>"""

def start_screen():
    return f"""
<div id="start-screen" class="screen">
  <h1>{GAME_NAME.upper()}</h1>
  <h2>{GENRE.upper()}</h2>
  <div class="mechanic-pill">⚡ {MECHANIC}: {MECH_DESC[:60]}{"..." if len(MECH_DESC)>60 else ""}</div>
  <p style="color:#666;font-size:11px;margin-top:8px;">🕹️ Joystick + buttons | Works on any device</p>
  <button class="bigbtn" onclick="startGame()">PLAY FREE</button>
  <p style="margin-top:20px;font-size:11px;color:#555;">{GENRE} · ${GAME_PRICE} SOL for full Godot source<br><a href="https://t.me/{TELEGRAM_CHANNEL.lstrip('@')}" style="color:var(--acc);">{TELEGRAM_CHANNEL}</a></p>
</div>
<div id="over-screen" class="screen hidden">
  <h1>GAME OVER</h1>
  <p style="font-size:28px;color:#fff;margin:10px 0;" id="final-score"></p>
  <div class="mechanic-pill">⚡ {MECHANIC}</div>
  <p style="margin-top:12px;font-size:12px;color:#666;">Get full Godot source for ${GAME_PRICE} SOL</p>
  <button class="bigbtn" onclick="restartGame()">PLAY AGAIN</button>
</div>"""

JOYSTICK_JS = """
const joyZone=document.getElementById('joy-zone'),joyOuter=document.getElementById('joy-outer'),joyInner=document.getElementById('joy-inner');
const JOY={x:0,y:0,active:false,id:-1,ox:0,oy:0,r:36};
function joyStart(e){if(JOY.active)return;const t=e.changedTouches[0],rc=joyOuter.getBoundingClientRect();JOY.active=true;JOY.id=t.identifier;JOY.ox=rc.left+rc.width/2;JOY.oy=rc.top+rc.height/2;joyMove(e);}
function joyMove(e){if(!JOY.active)return;for(const t of e.changedTouches){if(t.identifier!==JOY.id)continue;const dx=t.clientX-JOY.ox,dy=t.clientY-JOY.oy,d=Math.sqrt(dx*dx+dy*dy),c=Math.min(d,JOY.r);JOY.x=(dx/Math.max(d,1))*c/JOY.r;JOY.y=(dy/Math.max(d,1))*c/JOY.r;joyInner.style.transform=`translate(${JOY.x*JOY.r}px,${JOY.y*JOY.r}px)`;}}
function joyEnd(e){for(const t of e.changedTouches){if(t.identifier===JOY.id){JOY.active=false;JOY.x=0;JOY.y=0;JOY.id=-1;joyInner.style.transform='translate(0,0)';}}}
joyZone.addEventListener('touchstart',joyStart,{passive:false});joyZone.addEventListener('touchmove',joyMove,{passive:false});joyZone.addEventListener('touchend',joyEnd,{passive:false});
const KB={};document.addEventListener('keydown',e=>{KB[e.key]=true;e.preventDefault();});document.addEventListener('keyup',e=>{KB[e.key]=false;});
function kbJoy(){JOY.x=((KB['ArrowRight']||KB['d'])?1:0)-((KB['ArrowLeft']||KB['a'])?1:0);JOY.y=((KB['ArrowDown']||KB['s'])?1:0)-((KB['ArrowUp']||KB['w'])?1:0);}
"""

# ---------- GAME BUILDERS (FULL, NO F-STRING ERRORS) ----------

def build_shooter_game():
    return SHARED_HEAD + """
<body>
<div id="wrap">
  <div id="hud">
    <div id="score-ring"><div class="num" id="sc">0</div><div class="lbl">SCORE</div></div>
    <div style="flex:1;display:flex;flex-direction:column;gap:6px;padding:0 8px;">
      <div id="lives-row"><div class="life-pip" id="lp0"></div><div class="life-pip" id="lp1"></div><div class="life-pip" id="lp2"></div></div>
      <div id="special-bar"><div id="special-fill"></div></div>
      <div style="font-size:9px;color:#555;">⚡ """ + MECHANIC.upper() + """</div>
    </div>
    <div style="font-size:11px;color:#666;text-align:right;">""" + GAME_NAME + """<br><span style="color:var(--acc);font-size:9px;">WAVE <span id="wv">1</span></span></div>
  </div>
  <canvas id="c"></canvas>
  """ + start_screen() + """
  <div id="joy-zone"><div id="joy-outer"><div id="joy-inner"></div></div></div>
  <div id="btn-zone"><div class="abtn" id="btn-special" ontouchstart="activateSpecial()">⚡</div><div class="abtn" id="btn-fire" ontouchstart="rapidFire=true" ontouchend="rapidFire=false">🔥</div></div>
  <div id="brand-strip">DeathRoll</div>
</div>
<script>
""" + JOYSTICK_JS + """
const C=document.getElementById('c'),ctx=C.getContext('2d'); let W,H;
function resize(){{const wrap=document.getElementById('wrap'),hud=document.getElementById('hud');C.width=W=wrap.offsetWidth;C.height=H=wrap.offsetHeight-hud.offsetHeight;}}
window.addEventListener('resize',resize); resize();
let player,bullets,enemies,particles,score,lives,wave,frame,running,specialCharge,rapidFire=false;
function R(a,b){{return Math.random()*(b-a)+a;}}
function dist(a,b){{return Math.hypot(a.x-b.x,a.y-b.y);}}
function mkParticles(x,y,color,n=8){{for(let i=0;i<n;i++){{const a=R(0,Math.PI*2),s=R(1,5);particles.push({{x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,life:R(20,40),color,r:R(2,5)}});}}}}
function startGame(){{document.getElementById('start-screen').classList.add('hidden');init();}}
function restartGame(){{document.getElementById('over-screen').classList.add('hidden');init();}}
function init(){{
  player={{x:W/2,y:H*0.75,r:14,speed:3.8,invincible:0}};
  bullets=[]; enemies=[]; particles=[]; score=0; lives=3; wave=1; frame=0; running=true; specialCharge=0; updateHUD(); loop();
}}
function updateHUD(){{
  document.getElementById('sc').textContent=score;
  document.getElementById('wv').textContent=wave;
  document.getElementById('special-fill').style.width=(specialCharge/300*100)+'%';
  for(let i=0;i<3;i++){{const p=document.getElementById('lp'+i);if(p)p.className='life-pip'+(i>=lives?' dead':'');}}
}}
function spawnEnemy(){{
  const side=Math.floor(R(0,4)); let x,y;
  if(side===0){{x=R(0,W);y=-25;}}else if(side===1){{x=W+25;y=R(0,H);}}else if(side===2){{x=R(0,W);y=H+25;}}else{{x=-25;y=R(0,H);}}
  const hp=1+Math.floor(score/300),spd=R(0.9,1.8+wave*0.15);
  enemies.push({{x,y,r:14+hp*2,hp,maxHp:hp,speed:spd,color:`hsl(${R(0,360)},70%,55%)`}});
}}
function activateSpecial(){{
  if(specialCharge<300)return;
  player.invincible=180; specialCharge=0;
  mkParticles(player.x,player.y,'""" + G_COLOR + """',20);
  enemies.forEach(e=>{{if(dist(player,e)<160){{e.hp-=3; mkParticles(e.x,e.y,e.color,6);}}}});
  enemies=enemies.filter(e=>e.hp>0);
}}
document.getElementById('btn-special').addEventListener('touchstart',e=>{{e.preventDefault();activateSpecial();}},{{passive:false}});
function loop(){{
  if(!running)return; requestAnimationFrame(loop); frame++; kbJoy();
  const spd=player.speed; player.x=Math.max(player.r,Math.min(W-player.r,player.x+JOY.x*spd)); player.y=Math.max(player.r,Math.min(H-player.r,player.y+JOY.y*spd));
  if(player.invincible>0)player.invincible--;
  if(frame%18==0 && enemies.length){{
    let nearest=enemies.reduce((a,b)=>dist(player,a)<dist(player,b)?a:b);
    const ang=Math.atan2(nearest.y-player.y,nearest.x-player.x);
    bullets.push({{x:player.x,y:player.y,vx:Math.cos(ang)*9,vy:Math.sin(ang)*9,r:5}});
    if(rapidFire) bullets.push({{x:player.x,y:player.y,vx:Math.cos(ang+0.2)*9,vy:Math.sin(ang+0.2)*9,r:4}});
  }}
  if(frame%Math.max(35,90-wave*8)==0){{spawnEnemy(); if(wave>3&&Math.random()<0.3) spawnEnemy();}}
  if(score>0&&score%500===0&&frame%60===0) wave=Math.min(20,1+Math.floor(score/500));
  enemies.forEach(e=>{{const ang=Math.atan2(player.y-e.y,player.x-e.x); e.x+=Math.cos(ang)*e.speed; e.y+=Math.sin(ang)*e.speed;}});
  bullets=bullets.filter(b=>b.x>-20&&b.x<W+20&&b.y>-20&&b.y<H+20);
  for(let bi=bullets.length-1;bi>=0;bi--) for(let ei=enemies.length-1;ei>=0;ei--) if(dist(bullets[bi],enemies[ei])<enemies[ei].r+bullets[bi].r){{
    enemies[ei].hp--; mkParticles(enemies[ei].x,enemies[ei].y,enemies[ei].color,4); bullets.splice(bi,1);
    if(enemies[ei].hp<=0){{score+=10+wave*2; specialCharge=Math.min(300,specialCharge+20); mkParticles(enemies[ei].x,enemies[ei].y,enemies[ei].color,12); enemies.splice(ei,1); updateHUD();}}
    break;
  }}
  if(player.invincible===0) for(let ei=enemies.length-1;ei>=0;ei--) if(dist(player,enemies[ei])<player.r+enemies[ei].r-4){{
    lives--; player.invincible=90; mkParticles(player.x,player.y,'#ff3344',16); enemies.splice(ei,1); updateHUD();
    if(lives<=0){{running=false; document.getElementById('final-score').textContent='SCORE: '+score; document.getElementById('over-screen').classList.remove('hidden'); return;}}
  }}
  ctx.fillStyle='""" + G_BG + """'; ctx.fillRect(0,0,W,H);
  ctx.strokeStyle='rgba(255,255,255,0.04)'; for(let x=0;x<W;x+=40){{ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke();}} for(let y=0;y<H;y+=40){{ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}}
  particles=particles.filter(p=>{{p.x+=p.vx;p.y+=p.vy;p.vx*=0.92;p.vy*=0.92;p.life--; ctx.globalAlpha=p.life/40; ctx.fillStyle=p.color; ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill(); return p.life>0;}});
  ctx.globalAlpha=1;
  enemies.forEach(e=>{{ctx.save();ctx.shadowColor=e.color;ctx.shadowBlur=10;ctx.fillStyle=e.color;ctx.beginPath();ctx.arc(e.x,e.y,e.r,0,Math.PI*2);ctx.fill();if(e.maxHp>1){{ctx.fillStyle='#111';ctx.fillRect(e.x-e.r,e.y-e.r-8,e.r*2,4);ctx.fillStyle=e.color;ctx.fillRect(e.x-e.r,e.y-e.r-8,e.r*2*(e.hp/e.maxHp),4);}}ctx.restore();}});
  bullets.forEach(b=>{{b.x+=b.vx;b.y+=b.vy;ctx.save();ctx.shadowColor='""" + G_COLOR + """';ctx.shadowBlur=12;ctx.fillStyle='""" + G_COLOR + """';ctx.beginPath();ctx.arc(b.x,b.y,b.r,0,Math.PI*2);ctx.fill();ctx.restore();}});
  ctx.save(); if(player.invincible>0&&Math.floor(frame/4)%2===0){{ctx.restore();return;}} ctx.shadowColor='#fff';ctx.shadowBlur=8;ctx.fillStyle='#ffffff';ctx.translate(player.x,player.y);ctx.beginPath();ctx.moveTo(0,-player.r);ctx.lineTo(player.r*0.7,player.r*0.8);ctx.lineTo(-player.r*0.7,player.r*0.8);ctx.closePath();ctx.fill();ctx.restore();
}}
</script>
</body></html>"""

def build_wave_game():
    return SHARED_HEAD + """
<body>
<div id="wrap">
  <div id="hud">
    <div id="score-ring"><div class="num" id="sc">0</div><div class="lbl">SCORE</div></div>
    <div style="flex:1;display:flex;flex-direction:column;gap:6px;padding:0 8px;"><div id="lives-row"><div class="life-pip" id="lp0"></div><div class="life-pip" id="lp1"></div><div class="life-pip" id="lp2"></div><div class="life-pip" id="lp3"></div><div class="life-pip" id="lp4"></div></div><div id="special-bar"><div id="special-fill"></div></div></div>
    <div style="font-size:11px;color:#666;text-align:right;">""" + GAME_NAME + """<br><span style="color:var(--acc);font-size:9px;">WAVE <span id="wv">1</span></span></div>
  </div>
  <canvas id="c"></canvas>
  """ + start_screen() + """
  <div id="joy-zone"><div id="joy-outer"><div id="joy-inner"></div></div></div>
  <div id="btn-zone"><div class="abtn" ontouchstart="activateSpecial()">⚡</div><div class="abtn" ontouchstart="slash()">⚔️</div></div>
  <div id="brand-strip">DeathRoll</div>
</div>
<script>
""" + JOYSTICK_JS + """
const C=document.getElementById('c'),ctx=C.getContext('2d'); let W,H;
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
  enemies=[];particles=[];slashes=[];score=0;lives=5;wave=1;frame=0;running=true;charge=0;waveTimer=120;waveActive=false;
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
    enemies.push({{x:W/2+Math.cos(ang)*d,y:H/2+Math.sin(ang)*d,r:12+hp*3,hp,maxHp:hp,speed:R(1,1.8+wave*0.1),color:`hsl(${R(0,360)},70%,55%)`,invincible:0}});
  }}
  waveActive=true;
}}
function slash(){{
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
  enemies.forEach((e,i)=>{{if(dist(player,e)<200){{mkP(e.x,e.y,e.color,12);score+=10;enemies.splice(i,1);}}}});
  mkP(player.x,player.y,'""" + G_COLOR + """',30);
  player.invincible=120;
  updateHUD();
}}
document.getElementById('btn-zone').querySelectorAll('.abtn')[0].addEventListener('touchstart',e=>{{e.preventDefault();activateSpecial();}},{{passive:false}});
document.getElementById('btn-zone').querySelectorAll('.abtn')[1].addEventListener('touchstart',e=>{{e.preventDefault();slash();}},{{passive:false}});
document.addEventListener('keydown',e=>{{if(e.key===' ')activateSpecial();if(e.key==='z'||e.key==='x')slash();}});
function loop(){{
  if(!running)return; requestAnimationFrame(loop); frame++;kbJoy();
  player.x=Math.max(player.r,Math.min(W-player.r,player.x+JOY.x*player.speed));
  player.y=Math.max(player.r,Math.min(H-player.r,player.y+JOY.y*player.speed));
  if(JOY.x!==0||JOY.y!==0) player.facingAngle=Math.atan2(JOY.y,JOY.x);
  if(player.invincible>0)player.invincible--;
  if(!waveActive){{waveTimer--;if(waveTimer<=0){{spawnWave();waveTimer=0;}}}}
  if(waveActive && enemies.length===0){{wave++;waveTimer=90;waveActive=false;score+=wave*20;updateHUD();}}
  enemies.forEach(e=>{{if(e.invincible>0)e.invincible--;const ang=Math.atan2(player.y-e.y,player.x-e.x);e.x+=Math.cos(ang)*e.speed;e.y+=Math.sin(ang)*e.speed;}});
  if(player.invincible===0) enemies.forEach((e,i)=>{{if(dist(player,e)<player.r+e.r-4){{lives--;player.invincible=80;mkP(player.x,player.y,'#ff3344',12);enemies.splice(i,1);updateHUD();if(lives<=0){{running=false;gameOver();}}}}}});
  ctx.fillStyle='""" + G_BG + """';ctx.fillRect(0,0,W,H);
  const grd=ctx.createRadialGradient(W/2,H/2,30,W/2,H/2,H*0.7);grd.addColorStop(0,'""" + G_COLOR + """11');grd.addColorStop(1,'transparent');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
  particles=particles.filter(p=>{{p.x+=p.vx;p.y+=p.vy;p.vx*=0.9;p.vy*=0.9;p.life--;ctx.globalAlpha=p.life/45;ctx.fillStyle=p.color;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();return p.life>0;}});
  ctx.globalAlpha=1;
  slashes.forEach(s=>{{s.life--;ctx.save();ctx.globalAlpha=s.life/14;ctx.strokeStyle='""" + G_COLOR + """';ctx.lineWidth=4;ctx.shadowColor='""" + G_COLOR + """';ctx.shadowBlur=20;ctx.beginPath();ctx.moveTo(s.x,s.y);ctx.lineTo(s.x+Math.cos(s.angle)*s.range,s.y+Math.sin(s.angle)*s.range);ctx.stroke();ctx.restore();}});
  slashes=slashes.filter(s=>s.life>0);
  enemies.forEach(e=>{{ctx.save();ctx.shadowColor=e.color;ctx.shadowBlur=8;ctx.fillStyle=e.color;ctx.beginPath();ctx.arc(e.x,e.y,e.r,0,Math.PI*2);ctx.fill();if(e.maxHp>1){{ctx.fillStyle='#111';ctx.fillRect(e.x-e.r,e.y-e.r-8,e.r*2,4);ctx.fillStyle=e.color;ctx.fillRect(e.x-e.r,e.y-e.r-8,e.r*2*(e.hp/e.maxHp),4);}}ctx.restore();}});
  ctx.save();if(player.invincible>0&&Math.floor(frame/5)%2===0){{ctx.restore();}}else{{ctx.shadowColor='""" + G_COLOR + """';ctx.shadowBlur=14;ctx.fillStyle='""" + G_COLOR + """';ctx.translate(player.x,player.y);ctx.rotate(player.facingAngle+Math.PI/2);ctx.beginPath();ctx.moveTo(0,-16);ctx.lineTo(12,10);ctx.lineTo(-12,10);ctx.closePath();ctx.fill();ctx.restore();}}
  if(!waveActive&&waveTimer>0){{ctx.fillStyle='rgba(0,0,0,.5)';ctx.fillRect(W/2-100,H/2-20,200,40);ctx.fillStyle='""" + G_COLOR + """';ctx.font='bold 14px Courier New';ctx.textAlign='center';ctx.fillText(`WAVE ${wave} IN ${Math.ceil(waveTimer/30)}s`,W/2,H/2+5);ctx.textAlign='left';}}
}}
function gameOver(){{document.getElementById('final-score').textContent='SCORE: '+score;document.getElementById('over-screen').classList.remove('hidden');}}
</script>
</body></html>"""

def build_platformer_game():
    return SHARED_HEAD + """
<body>
<div id="wrap">
  <div id="hud">
    <div id="score-ring"><div class="num" id="sc">0</div><div class="lbl">SCORE</div></div>
    <div style="flex:1;display:flex;flex-direction:column;gap:6px;padding:0 8px;"><div id="lives-row"><div class="life-pip" id="lp0"></div><div class="life-pip" id="lp1"></div><div class="life-pip" id="lp2"></div></div><div id="special-bar"><div id="special-fill"></div></div></div>
    <div style="font-size:11px;color:#666;">""" + GAME_NAME + """</div>
  </div>
  <canvas id="c"></canvas>
  """ + start_screen() + """
  <div id="joy-zone"><div id="joy-outer"><div id="joy-inner"></div></div></div>
  <div id="btn-zone"><div class="abtn" ontouchstart="doJump()">↑</div><div class="abtn" ontouchstart="activateSpecial()">⚡</div></div>
  <div id="brand-strip">DeathRoll</div>
</div>
<script>
""" + JOYSTICK_JS + """
const C=document.getElementById('c'),ctx=C.getContext('2d'); let W,H;
function resize(){{const wrap=document.getElementById('wrap'),hud=document.getElementById('hud');C.width=W=wrap.offsetWidth;C.height=H=wrap.offsetHeight-hud.offsetHeight;}}
window.addEventListener('resize',resize);resize();
let player,platforms,coins,enemies,particles,score,lives,frame,running,charge,camY;
const GRAV=0.45,JUMP=-10;
function R(a,b){{return Math.random()*(b-a)+a;}}
function mkP(x,y,c,n=6){{for(let i=0;i<n;i++){{const a=R(0,Math.PI*2),s=R(1,4);particles.push({{x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,life:R(20,35),color:c,r:R(1,4)}});}}}}
function startGame(){{document.getElementById('start-screen').classList.add('hidden');init();}}
function restartGame(){{document.getElementById('over-screen').classList.add('hidden');init();}}
function doJump(){{if(player&&player.onGround){{player.vy=JUMP;player.onGround=false;mkP(player.x,player.y+player.h,'""" + G_COLOR + """',6);}}}}
function activateSpecial(){{
  if(charge<300)return;charge=0;
  player.vy=JUMP*1.6;player.invincible=120;
  mkP(player.x,player.y,'""" + G_COLOR + """',20);
  enemies.forEach((e,i)=>{{if(Math.hypot(e.x-player.x,e.y-player.y)<120){{mkP(e.x,e.y,e.color,8);enemies.splice(i,1);score+=20;}}}});
  updateHUD();
}}
document.addEventListener('keydown',e=>{{if(e.key===' '||e.key==='ArrowUp'||e.key==='w')doJump();if(e.key==='z')activateSpecial();}});
function buildLevel(startY){{
  const plats=[];plats.push({{x:0,y:startY+H-20,w:W,h:20,color:'#333'}});
  for(let i=1;i<30;i++){{const y=startY+H-20-i*85+R(-20,20);const w=R(60,140);const x=R(10,W-w-10);plats.push({{x,y,w,h:14,color:`hsl(${R(180,280)},60%,35%)`}});}}
  return plats;
}}
function buildCoins(plats){{return plats.slice(1).map(p=>Math.random()<0.6?{{x:p.x+p.w/2,y:p.y-18,r:7,collected:false}}:null).filter(Boolean);}}
function buildEnemies(plats){{return plats.slice(5).filter(()=>Math.random()<0.35).map(p=>{{return{{x:p.x+p.w/2,y:p.y-20,r:12,dx:1.2,plat:p,color:`hsl(${R(0,60)},80%,55%)`,invincible:0}};}});}}
function init(){{
  camY=0;player={{x:W/2-12,y:H-100,w:24,h:28,vx:0,vy:0,onGround:false,invincible:0}};
  platforms=buildLevel(0);coins=buildCoins(platforms);enemies=buildEnemies(platforms);
  particles=[];score=0;lives=3;frame=0;running=true;charge=0;updateHUD();loop();
}}
function updateHUD(){{
  document.getElementById('sc').textContent=score;
  document.getElementById('special-fill').style.width=(charge/300*100)+'%';
  for(let i=0;i<3;i++){{const p=document.getElementById('lp'+i);if(p)p.className='life-pip'+(i>=lives?' dead':'');}}
}}
function loop(){{
  if(!running)return; requestAnimationFrame(loop); frame++;kbJoy();
  player.vx=JOY.x*4;player.vy+=GRAV;player.x+=player.vx;player.y+=player.vy;player.onGround=false;
  player.x=Math.max(0,Math.min(W-player.w,player.x));
  if(player.invincible>0)player.invincible--;
  platforms.forEach(p=>{{if(player.x<p.x+p.w&&player.x+player.w>p.x&&player.y+player.h>p.y&&player.y+player.h<p.y+p.h+Math.abs(player.vy)+2&&player.vy>=0){{player.y=p.y-player.h;player.vy=0;player.onGround=true;}}}});
  const targetY=player.y-H*0.5;if(targetY<camY)camY+=(targetY-camY)*0.08;
  coins.forEach(coin=>{{if(!coin.collected&&Math.hypot(player.x+12-coin.x,player.y+14-coin.y)<coin.r+14){{coin.collected=true;score+=5;charge=Math.min(300,charge+25);mkP(coin.x,coin.y,'""" + G_COLOR + """',8);updateHUD();}}}});
  enemies.forEach(e=>{{e.x+=e.dx;if(e.x<e.plat.x||e.x>e.plat.x+e.plat.w)e.dx*=-1;if(player.invincible===0&&Math.hypot(player.x+12-e.x,player.y+14-e.y)<e.r+14){{if(player.vy>0&&player.y+player.h<e.y+4){{score+=15;charge=Math.min(300,charge+50);mkP(e.x,e.y,e.color,12);enemies=enemies.filter(en=>en!==e);player.vy=JUMP*0.6;updateHUD();}}else{{lives--;player.invincible=90;player.vy=JUMP*0.7;mkP(player.x,player.y,'#ff3344',12);updateHUD();if(lives<=0){{running=false;gameOver();}}}}}}}});
  if(player.y-camY>H+100||player.y>10000){{running=false;gameOver();}}
  ctx.fillStyle='""" + G_BG + """';ctx.fillRect(0,0,W,H);ctx.save();ctx.translate(0,-camY);
  platforms.forEach(p=>{{ctx.fillStyle=p.color;ctx.fillRect(p.x,p.y,p.w,p.h);ctx.fillStyle='rgba(255,255,255,0.06)';ctx.fillRect(p.x,p.y,p.w,4);}});
  coins.forEach(c=>{{if(c.collected)return;ctx.save();ctx.shadowColor='""" + G_COLOR + """';ctx.shadowBlur=10;ctx.fillStyle='""" + G_COLOR + """';ctx.beginPath();ctx.arc(c.x,c.y,c.r,0,Math.PI*2);ctx.fill();ctx.restore();}});
  enemies.forEach(e=>{{ctx.save();ctx.shadowColor=e.color;ctx.shadowBlur=8;ctx.fillStyle=e.color;ctx.beginPath();ctx.arc(e.x,e.y,e.r,0,Math.PI*2);ctx.fill();ctx.restore();}});
  particles=particles.filter(p=>{{p.x+=p.vx;p.y+=p.vy;p.vy+=0.15;p.life--;ctx.globalAlpha=p.life/35;ctx.fillStyle=p.color;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();return p.life>0;}});
  ctx.globalAlpha=1;
  if(!(player.invincible>0&&Math.floor(frame/5)%2===0)){{ctx.fillStyle='""" + G_COLOR + """';ctx.shadowColor='""" + G_COLOR + """';ctx.shadowBlur=10;ctx.fillRect(player.x,player.y,player.w,player.h);ctx.fillStyle='rgba(255,255,255,.5)';ctx.fillRect(player.x+6,player.y+6,6,6);}}
  ctx.restore();
}}
function gameOver(){{document.getElementById('final-score').textContent='SCORE: '+score;document.getElementById('over-screen').classList.remove('hidden');}}
</script>
</body></html>"""

def build_puzzle_game():
    return SHARED_HEAD + """
<body>
<div id="wrap">
  <div id="hud">
    <div id="score-ring"><div class="num" id="sc">0</div><div class="lbl">MOVES</div></div>
    <div style="flex:1;display:flex;flex-direction:column;gap:6px;padding:0 8px;"><div style="font-size:11px;color:var(--acc);">Best: <span id="best">—</span></div><div id="special-bar"><div id="special-fill"></div></div><div style="font-size:9px;color:#555;">⚡ """ + MECHANIC.upper() + """</div></div>
    <div style="font-size:11px;color:#666;">""" + GAME_NAME + """</div>
  </div>
  <canvas id="c"></canvas>
  """ + start_screen() + """
  <div id="brand-strip">DeathRoll</div>
</div>
<script>
const C=document.getElementById('c'),ctx=C.getContext('2d'); let W,H;
function resize(){{const wrap=document.getElementById('wrap'),hud=document.getElementById('hud');C.width=W=wrap.offsetWidth;C.height=H=wrap.offsetHeight-hud.offsetHeight;}}
window.addEventListener('resize',resize);resize();
const N=4; let board,blank,moves,best,running,animTile,frame,charge;
function startGame(){{document.getElementById('start-screen').classList.add('hidden');init();}}
function restartGame(){{document.getElementById('over-screen').classList.add('hidden');init();}}
function init(){{
  board=[];for(let i=0;i<N*N-1;i++)board.push(i+1);board.push(0);blank={{r:N-1,c:N-1}};
  for(let i=0;i<300;i++)doMove(random_move());
  moves=0;charge=0;running=true;animTile=null;frame=0;updateHUD();loop();
}}
function getBest(){{return localStorage?localStorage.getItem('dr_puzzle_best')||null:null;}}
function setBest(v){{if(localStorage)localStorage.setItem('dr_puzzle_best',v);}}
function updateHUD(){{document.getElementById('sc').textContent=moves;const b=getBest();document.getElementById('best').textContent=b||'—';document.getElementById('special-fill').style.width=(charge/300*100)+'%';}}
function idx(r,c){{return r*N+c;}}
function random_move(){{const dirs=[[-1,0],[1,0],[0,-1],[0,1]];const valid=dirs.filter(([dr,dc])=>{{const nr=blank.r+dr,nc=blank.c+dc;return nr>=0&&nr<N&&nc>=0&&nc<N;}});return valid[Math.floor(Math.random()*valid.length)];}}
function doMove([dr,dc]){{const nr=blank.r+dr,nc=blank.c+dc;if(nr<0||nr>=N||nc<0||nc>=N)return false;board[idx(blank.r,blank.c)]=board[idx(nr,nc)];board[idx(nr,nc)]=0;blank={{r:nr,c:nc}};return true;}}
function isSolved(){{for(let i=0;i<N*N-1;i++)if(board[i]!==i+1)return false;return board[N*N-1]===0;}}
C.addEventListener('click',handleClick);C.addEventListener('touchend',e=>{{e.preventDefault();const t=e.changedTouches[0];handleClick({{clientX:t.clientX,clientY:t.clientY}});}},{{passive:false}});
function handleClick(e){{if(!running)return;const rect=C.getBoundingClientRect();const mx=e.clientX-rect.left,my=e.clientY-rect.top;const tw=W/N,th=H/N;const cc=Math.floor(mx/tw),cr=Math.floor(my/th);if(cr<0||cr>=N||cc<0||cc>=N)return;const dr=cr-blank.r,dc=cc-blank.c;if((Math.abs(dr)+Math.abs(dc))===1){{doMove([dr,dc]);moves++;charge=Math.min(300,charge+10);updateHUD();if(isSolved()){{running=false;const b=getBest();if(!b||moves<parseInt(b))setBest(moves);setTimeout(()=>{{document.getElementById('final-score').textContent=`Solved in ${moves} moves!`;document.getElementById('over-screen').classList.remove('hidden');}},500);}}}}}}
function loop(){{requestAnimationFrame(loop);frame++;ctx.fillStyle='""" + G_BG + """';ctx.fillRect(0,0,W,H);const tw=W/N,th=H/N,gap=4;for(let r=0;r<N;r++){{for(let c=0;c<N;c++){{const v=board[idx(r,c)];if(v===0)continue;const x=c*tw+gap/2,y=r*th+gap/2,bw=tw-gap,bh=th-gap;const hue=((v-1)/(N*N-1))*280+20;ctx.fillStyle=`hsl(${hue},60%,18%)`;ctx.fillRect(x,y,bw,bh);ctx.strokeStyle=`hsl(${hue},70%,45%)`;ctx.lineWidth=2;ctx.strokeRect(x+1,y+1,bw-2,bh-2);ctx.fillStyle=`hsl(${hue},80%,70%)`;ctx.font=`bold ${Math.floor(tw*0.38)}px Courier New`;ctx.textAlign='center';ctx.textBaseline='middle';ctx.shadowColor=`hsl(${hue},80%,60%)`;ctx.shadowBlur=8;ctx.fillText(v,x+bw/2,y+bh/2);ctx.shadowBlur=0;}}}
  ctx.textAlign='left';ctx.strokeStyle='rgba(255,255,255,0.05)';ctx.lineWidth=1;for(let i=1;i<N;i++){{ctx.beginPath();ctx.moveTo(i*tw,0);ctx.lineTo(i*tw,H);ctx.stroke();ctx.beginPath();ctx.moveTo(0,i*th);ctx.lineTo(W,i*th);ctx.stroke();}}
}}
function gameOver(){{}}
</script>
</body></html>"""

def build_racer_game():
    return SHARED_HEAD + """
<body>
<div id="wrap">
  <div id="hud">
    <div id="score-ring"><div class="num" id="sc">0</div><div class="lbl">DIST</div></div>
    <div style="flex:1;display:flex;flex-direction:column;gap:6px;padding:0 8px;"><div style="font-size:11px;color:var(--acc);">SPEED: <span id="spd">0</span></div><div id="special-bar"><div id="special-fill"></div></div></div>
    <div style="font-size:11px;color:#666;">""" + GAME_NAME + """</div>
  </div>
  <canvas id="c"></canvas>
  """ + start_screen() + """
  <div id="joy-zone"><div id="joy-outer"><div id="joy-inner"></div></div></div>
  <div id="btn-zone"><div class="abtn" ontouchstart="activateBoost()">🚀</div></div>
  <div id="brand-strip">DeathRoll</div>
</div>
<script>
""" + JOYSTICK_JS + """
const C=document.getElementById('c'),ctx=C.getContext('2d'); let W,H;
function resize(){{const wrap=document.getElementById('wrap'),hud=document.getElementById('hud');C.width=W=wrap.offsetWidth;C.height=H=wrap.offsetHeight-hud.offsetHeight;}}
window.addEventListener('resize',resize);resize();
let car,obstacles,coins,particles,score,frame,running,speed,boost,charge,lines;
function R(a,b){{return Math.random()*(b-a)+a;}}
function mkP(x,y,c,n=8){{for(let i=0;i<n;i++){{const a=R(0,Math.PI*2),s=R(2,6);particles.push({{x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,life:R(20,35),color:c,r:R(2,4)}});}}}}
function startGame(){{document.getElementById('start-screen').classList.add('hidden');init();}}
function restartGame(){{document.getElementById('over-screen').classList.add('hidden');init();}}
function activateBoost(){{if(charge<300)return;charge=0;boost=180;mkP(car.x,car.y+30,'""" + G_COLOR + """',20);updateHUD();}}
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
  if(!running)return; requestAnimationFrame(loop); frame++;kbJoy();
  const effectiveSpeed=speed+(boost>0?5:0);
  if(boost>0)boost--;
  speed=Math.min(12,3+frame/600);
  car.x=Math.max(car.w/2+20,Math.min(W-car.w/2-20,car.x+JOY.x*5));
  if(car.invincible>0)car.invincible--;
  score+=effectiveSpeed*0.1;
  lines.forEach(l=>{{l.y+=effectiveSpeed*2;if(l.y>H){{l.y-=H;l.x=W/2+R(-20,20);}}}});
  if(frame%Math.max(30,60-Math.floor(speed*4))===0){{const cols=[W*0.2,W*0.4,W*0.6,W*0.8];const col=cols[Math.floor(R(0,cols.length))];obstacles.push({{x:col,y:-30,w:R(30,50),h:R(30,50),color:`hsl(${R(0,360)},70%,50%)`}});}}
  if(frame%45===0) coins.push({{x:R(40,W-40),y:-20,r:10,collected:false}});
  obstacles.forEach(o=>o.y+=effectiveSpeed*1.8);
  coins.forEach(c=>c.y+=effectiveSpeed*1.8);
  obstacles=obstacles.filter(o=>o.y<H+60);
  coins=coins.filter(c=>c.y<H+30&&!c.collected);
  coins.forEach(c=>{{if(!c.collected&&Math.hypot(car.x-c.x,car.y-c.y)<c.r+18){{c.collected=true;score+=20;charge=Math.min(300,charge+40);mkP(c.x,c.y,'""" + G_COLOR + """',8);updateHUD();}}}});
  if(car.invincible===0) obstacles.forEach((o,i)=>{{if(car.x-car.w/2<o.x+o.w/2&&car.x+car.w/2>o.x-o.w/2&&car.y-car.h/2<o.y+o.h/2&&car.y+car.h/2>o.y-o.h/2){{mkP(car.x,car.y,'#ff4444',20);running=false;gameOver();}}}});
  ctx.fillStyle='#111';ctx.fillRect(0,0,W,H);
  ctx.fillStyle='#1a1a1a';ctx.fillRect(W*0.1,0,W*0.8,H);
  ctx.fillStyle='#ff3300';for(let y=0;y<H;y+=80){{ctx.fillRect(W*0.1-8,y,8,40);ctx.fillRect(W*0.9,y,8,40);}}
  lines.forEach(l=>{{ctx.fillStyle='rgba(255,255,100,0.6)';ctx.fillRect(l.x-2,l.y,4,30);}});
  particles=particles.filter(p=>{{p.x+=p.vx;p.y+=p.vy;p.vx*=0.9;p.vy*=0.9;p.life--;ctx.globalAlpha=p.life/35;ctx.fillStyle=p.color;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();return p.life>0;}});
  ctx.globalAlpha=1;
  obstacles.forEach(o=>{{ctx.fillStyle=o.color;ctx.shadowColor=o.color;ctx.shadowBlur=8;ctx.fillRect(o.x-o.w/2,o.y-o.h/2,o.w,o.h);ctx.shadowBlur=0;}});
  coins.forEach(c=>{{if(c.collected)return;ctx.save();ctx.shadowColor='""" + G_COLOR + """';ctx.shadowBlur=10;ctx.fillStyle='""" + G_COLOR + """';ctx.beginPath();ctx.arc(c.x,c.y,c.r,0,Math.PI*2);ctx.fill();ctx.restore();}});
  ctx.save();if(boost>0){{ctx.shadowColor='""" + G_COLOR + """';ctx.shadowBlur=20;}}ctx.fillStyle=boost>0?'""" + G_COLOR + """':'#ffffff';ctx.fillRect(car.x-car.w/2,car.y-car.h/2,car.w,car.h);ctx.fillStyle='rgba(0,200,255,.4)';ctx.fillRect(car.x-car.w/2+4,car.y-car.h/2+6,car.w-8,14);if(boost>0){{for(let i=0;i<3;i++) mkP(car.x+R(-8,8),car.y+car.h/2+5,'""" + G_COLOR + """',1);}}ctx.restore();
  updateHUD();
}}
function gameOver(){{document.getElementById('final-score').textContent='DISTANCE: '+Math.floor(score);document.getElementById('over-screen').classList.remove('hidden');}}
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

# ---------- CREATE WORKSPACE ----------
proj_dir = Path(f"workspace/{SAFE_NAME}")
proj_dir.mkdir(parents=True, exist_ok=True)
(proj_dir / "index.html").write_text(html5_game, encoding="utf-8")
if sprite.exists(): shutil.copy(sprite, proj_dir / "icon.png")
(proj_dir / "project.godot").write_text(f'[application]\nconfig/name="{GAME_NAME}"\nconfig/icon="res://icon.png"\n')
(proj_dir / "README.md").write_text(f"# {GAME_NAME}\n\n**Studio:** DeathRoll\n**Genre:** {GENRE}\n**Mechanic:** {MECHANIC}\n\n{DESCRIPTION}\n\nPlay: {PLAY_URL}\nSource: {ZIP_URL}\nLicense: {LICENSE_KEY}")

# ---------- ZIP ----------
zip_path = Path("workspace/latest_game.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in proj_dir.rglob("*"):
        if f.is_file(): zf.write(f, f.relative_to(proj_dir.parent))
print(f"  ✅ ZIP: {zip_path.stat().st_size//1024}KB")

# ---------- UPDATE PORTFOLIO STATUS ----------
cur = json.loads(port_path.read_text())
for g in cur:
    if g["game"] == GAME_NAME:
        g["art_success"] = art_ok
        g["status"] = "complete"
        g["game_type"] = GAME_TYPE
port_path.write_text(json.dumps(cur, indent=2))

# ---------- STOREFRONT ----------
print("  🌐 Generating storefront...")
storefront_html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
<title>DeathRoll Studio – Daily AI Games</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  :root {
    --bg: #04040c;
    --surface: #0a0a18;
    --card: #0f0f20;
    --border: rgba(255,255,255,0.05);
    --accent: #00ffcc;
    --accent2: #ff2d55;
    --text: #d0d0f0;
    --muted: #6a6a8a;
    --success: #00cc88;
  }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Share Tech Mono', monospace;
    overflow-x: hidden;
  }
  body::before {
    content: '';
    position: fixed; inset: 0;
    background-image: linear-gradient(rgba(0,255,204,0.015) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(0,255,204,0.015) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
  }
  .container { position: relative; z-index: 1; max-width: 1400px; margin: 0 auto; padding: 20px; }
  header { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; padding: 20px 0; border-bottom: 1px solid var(--border); margin-bottom: 32px; }
  .logo { font-family: 'Orbitron', sans-serif; font-size: 1.8rem; font-weight: 900; background: linear-gradient(135deg, #fff, var(--accent)); -webkit-background-clip: text; background-clip: text; color: transparent; letter-spacing: 2px; }
  .logo span { color: var(--accent); background: none; -webkit-background-clip: unset; background-clip: unset; }
  .nav a { color: var(--muted); text-decoration: none; margin-left: 24px; font-size: 0.8rem; letter-spacing: 1px; transition: color 0.2s; }
  .nav a:hover { color: var(--accent); }
  .live-badge { background: rgba(0,255,204,0.1); border: 1px solid var(--accent); color: var(--accent); padding: 4px 12px; border-radius: 20px; font-size: 0.7rem; letter-spacing: 1px; }
  .hero { text-align: center; padding: 60px 20px; background: radial-gradient(ellipse 70% 40% at 50% 0%, rgba(0,255,204,0.08), transparent); border-radius: 32px; margin-bottom: 40px; }
  .hero h1 { font-family: 'Orbitron', sans-serif; font-size: clamp(2rem, 8vw, 4rem); font-weight: 900; background: linear-gradient(135deg, #fff, var(--accent)); -webkit-background-clip: text; background-clip: text; color: transparent; margin-bottom: 16px; }
  .hero p { color: var(--muted); max-width: 600px; margin: 0 auto 24px; line-height: 1.6; }
  .stats { display: flex; justify-content: center; gap: 32px; flex-wrap: wrap; margin: 32px 0; }
  .stat-card { background: rgba(255,255,255,0.02); backdrop-filter: blur(4px); border: 1px solid var(--border); border-radius: 16px; padding: 20px 32px; text-align: center; }
  .stat-number { font-family: 'Orbitron', sans-serif; font-size: 2.5rem; font-weight: 900; color: var(--accent); }
  .stat-label { font-size: 0.7rem; letter-spacing: 2px; color: var(--muted); margin-top: 4px; }
  .games-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 24px; margin: 40px 0; }
  .game-card { background: var(--card); border: 1px solid var(--border); border-radius: 16px; overflow: hidden; transition: transform 0.2s, border-color 0.2s; }
  .game-card:hover { transform: translateY(-4px); border-color: var(--accent); }
  .game-image { height: 180px; background-size: cover; background-position: center; position: relative; }
  .game-badge { position: absolute; top: 12px; left: 12px; background: rgba(0,0,0,0.7); backdrop-filter: blur(4px); padding: 4px 12px; border-radius: 20px; font-size: 0.7rem; color: var(--accent); border: 1px solid var(--accent); }
  .game-info { padding: 20px; }
  .game-name { font-family: 'Orbitron', sans-serif; font-size: 1.2rem; margin-bottom: 4px; }
  .game-genre { color: var(--accent); font-size: 0.7rem; letter-spacing: 1px; margin-bottom: 12px; text-transform: uppercase; }
  .game-mechanic { background: rgba(0,255,204,0.1); display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.7rem; margin-bottom: 12px; }
  .game-desc { font-size: 0.8rem; color: var(--muted); line-height: 1.5; margin-bottom: 16px; }
  .price { font-size: 1.2rem; color: var(--accent); font-weight: bold; }
  .game-date { font-size: 0.6rem; color: #444; margin-top: 12px; }
  .buy-section { background: var(--surface); border-radius: 24px; padding: 40px; margin: 40px 0; text-align: center; border: 1px solid var(--border); }
  .buy-section h2 { font-family: 'Orbitron', sans-serif; font-size: 1.6rem; margin-bottom: 24px; }
  .wallet-box { background: rgba(0,0,0,0.4); border-radius: 16px; padding: 20px; margin: 20px auto; max-width: 500px; word-break: break-all; font-family: monospace; font-size: 0.7rem; }
  .wallet-row { display: flex; gap: 12px; align-items: center; justify-content: center; margin: 12px 0; }
  .btn { display: inline-block; background: var(--accent); color: #000; padding: 12px 28px; border-radius: 40px; text-decoration: none; font-weight: bold; letter-spacing: 1px; transition: opacity 0.2s; margin-top: 16px; }
  .btn:hover { opacity: 0.8; }
  footer { text-align: center; padding: 32px 0; border-top: 1px solid var(--border); margin-top: 40px; font-size: 0.7rem; color: var(--muted); }
  @media (max-width: 768px) { .nav { display: none; } .stats { gap: 16px; } .stat-card { padding: 12px 20px; } }
</style>
</head>
<body>
<div class="container">
  <header>
    <div class="logo">DEATH<span>ROLL</span></div>
    <div class="nav">
      <a href="#games">GAMES</a>
      <a href="#buy">BUY</a>
      <a href="https://t.me/drolltech" target="_blank">TELEGRAM</a>
    </div>
    <div class="live-badge">● LIVE DAILY</div>
  </header>

  <div class="hero">
    <h1>NEW MOBILE GAME<br>EVERY DAY</h1>
    <p>AI‑generated mechanics, unique art, and full source code – all playable in your browser.<br>Own the game for <span id="priceDisplay">7</span> SOL.</p>
    <div class="stats" id="stats">
      <div class="stat-card"><div class="stat-number" id="totalGames">-</div><div class="stat-label">GAMES</div></div>
      <div class="stat-card"><div class="stat-number" id="totalGenres">-</div><div class="stat-label">GENRES</div></div>
      <div class="stat-card"><div class="stat-number" id="latestDate">-</div><div class="stat-label">LATEST</div></div>
    </div>
  </div>

  <div class="games-grid" id="gamesGrid"><div class="stat-card">Loading games...</div></div>

  <div class="buy-section" id="buy">
    <h2>⚡ GET FULL SOURCE CODE</h2>
    <p>Send <strong id="buyPrice">7</strong> SOL to either wallet below, then DM <strong>@deathroll1</strong> with your @username.<br>You'll receive the complete Godot 4 project + HTML5 build + license key instantly.</p>
    <div class="wallet-box">
      <div class="wallet-row">🔵 <strong>Trust Wallet (Solana)</strong><br><code id="trustAddr">6wsQ6nGXrUUUGCEokb4rZcfHDv2a8MomUb22TuVaH2m3</code></div>
      <div class="wallet-row">🟣 <strong>Phantom Wallet (Solana)</strong><br><code id="phantomAddr">Csk9DKstWMdKx19gUHWB9xy2VwZZX2nx6V6oSVGDCgMb</code></div>
    </div>
    <a href="https://t.me/deathroll1" class="btn" target="_blank">📩 DM @deathroll1</a>
  </div>

  <footer>
    <p>© 2025 DeathRoll Studio — Automated Game Factory v30.0</p>
    <p>Built with AI & Solana | <a href="https://t.me/drolltech" style="color:var(--accent);">Join Telegram</a></p>
  </footer>
</div>

<script>
  async function loadGames() {
    try {
      const res = await fetch('portfolio.json?t='+Date.now());
      if (!res.ok) throw new Error();
      let games = await res.json();
      if (!Array.isArray(games)) games = [];
      games.sort((a,b) => new Date(b.date) - new Date(a.date));
      const total = games.length;
      const genres = new Set(games.map(g => g.genre)).size;
      const latest = games[0] ? new Date(games[0].date).toLocaleDateString() : '-';
      document.getElementById('totalGames').innerText = total;
      document.getElementById('totalGenres').innerText = genres;
      document.getElementById('latestDate').innerText = latest;
      const price = games[0]?.price_sol || '7';
      document.getElementById('priceDisplay').innerText = price;
      document.getElementById('buyPrice').innerText = price;
      document.getElementById('trustAddr').innerText = '6wsQ6nGXrUUUGCEokb4rZcfHDv2a8MomUb22TuVaH2m3';
      document.getElementById('phantomAddr').innerText = 'Csk9DKstWMdKx19gUHWB9xy2VwZZX2nx6V6oSVGDCgMb';
      const grid = document.getElementById('gamesGrid');
      grid.innerHTML = games.slice(0, 20).map(g => `
        <div class="game-card">
          <div class="game-image" style="background-image: url('${g.image_url || ''}'); background-color:#111;">
            <div class="game-badge">${escapeHtml(g.genre || '?')}</div>
          </div>
          <div class="game-info">
            <div class="game-name">${escapeHtml(g.game)}</div>
            <div class="game-genre">${escapeHtml(g.genre)}</div>
            <div class="game-mechanic">⚡ ${escapeHtml(g.mechanic)}</div>
            <div class="game-desc">${escapeHtml(g.description || g.mech_desc || '')}</div>
            <div class="price">💰 ${g.price_sol || price} SOL</div>
            <div class="game-date">📅 ${new Date(g.date).toLocaleDateString()}</div>
            <a href="${g.play_url || '#'}" target="_blank" style="display:inline-block; margin-top:12px; color:var(--accent); font-size:0.7rem;">▶ Play Free</a>
          </div>
        </div>
      `).join('');
      if (!games.length) grid.innerHTML = '<div class="stat-card">No games yet. First game will appear at 6AM UTC tomorrow.</div>';
    } catch(e) {
      document.getElementById('gamesGrid').innerHTML = '<div class="stat-card">⚠️ Error loading games. Check back soon.</div>';
    }
  }
  function escapeHtml(str) { if(!str) return ''; return str.replace(/[&<>]/g, function(m){if(m==='&') return '&amp;'; if(m==='<') return '&lt;'; if(m==='>') return '&gt;'; return m;}); }
  loadGames();
  setInterval(loadGames, 60000);
</script>
</body>
</html>'''
Path("index.html").write_text(storefront_html, encoding="utf-8")
print(f"  ✅ Storefront updated")

# ---------- TELEGRAM POSTS ----------
sales_post = f"{EMOJI_STR} *{HOOK}* {EMOJI_STR}\n\n✨ *{GAME_NAME}* — {GENRE}\n_{DESCRIPTION}_\n\n⚡ *Mechanic:* `{MECHANIC}`\n🕹️ *Play FREE:* {PLAY_URL}\n\n💰 *Full source:* ${GAME_PRICE} SOL\n🔵 Trust: `{SOLANA_TRUST}`\n🟣 Phantom: `{SOLANA_PHANTOM}`\n\nSend ${GAME_PRICE} SOL + @username → instant delivery\n\n{TAGS}"
if TG_TOKEN and sprite.exists():
    tg_send_photo(TELEGRAM_CHANNEL, sprite, sales_post)
    print("  ✅ Channel post sent")
if TG_TOKEN and TG_ADMIN and zip_path.exists():
    tg_send_doc(TG_ADMIN, zip_path, f"🎮 {GAME_NAME} — {GAME_TYPE}\nGenre: {GENRE}\nMechanic: {MECHANIC}\nArt: {'✅' if art_ok else '⚠️'}\nKey: `{LICENSE_KEY}`")
    print("  ✅ Admin bundle sent")

# ---------- WHATSAPP POST ----------
whatsapp_text = f"🎮 *NEW GAME*: {GAME_NAME} ({GENRE})\n\n{MECHANIC}: {MECH_DESC}\n{DESCRIPTION}\n\nPlay free: {PLAY_URL}\nFull source: {GAME_PRICE} SOL\n\n#DeathRollStudio"
if sprite.exists():
    send_to_whatsapp(whatsapp_text, image_url=IMG_URL)
    print("  ✅ WhatsApp post sent (if webhook configured)")

# ---------- SAR UPDATE ----------
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

# ---------- LOGS ----------
Path("learning_data.json").write_text(json.dumps({"ts": datetime.now().isoformat(), "game": GAME_NAME, "genre": GENRE, "mechanic": MECHANIC, "art_ok": art_ok, "total_games": len(entries)}, indent=2))
Path("last_run.txt").write_text(datetime.now().isoformat())

print("\n╔══════════════════════════════════════════════════════╗")
print("║  ✅  DEATHROLL STUDIO v30.0  —  COMPLETE            ║")
print(f"║  Game    : {GAME_NAME:<41}║")
print(f"║  Genre   : {GENRE:<41}║")
print(f"║  Mechanic: {MECHANIC:<41}║")
print("╚══════════════════════════════════════════════════════╝")
print(f"  🌐 {BASE_URL}/")
print(f"  📱 https://t.me/{TELEGRAM_CHANNEL.lstrip('@')}")
