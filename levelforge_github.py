#!/usr/bin/env python3
"""
DEATHROLL STUDIO v38.1 – COMPLETE MULTI‑GAME ENGINE (FIXED)
All 7 game templates fully implemented, art‑matched, no missing variables.
"""

import os, json, random, requests, time, shutil, zipfile, uuid
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw
from typing import Dict, List, Optional

# ============================================================
# CONFIG
# ============================================================
BOT_VERSION = "38.1.0"
CONFIG = {
    "brand": {"name":"DeathRoll","email":"favouradeleke246@gmail.com","telegram":"@deathroll1",
              "tiktok":"@deathroll.co","website":"https://deathroll.co","github":"favouradeleke246-maker"},
    "wallets": {"trust":"6wsQ6nGXrUUUGCEokb4rZcfHDv2a8MomUb22TuVaH2m3",
                "phantom":"Csk9DKstWMdKx19gUHWB9xy2VwZZX2nx6V6oSVGDCgMb"},
    "telegram": {"channel":"@drolltech"},
    "price": {"min":2, "max":10, "default":5}
}
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GH_TOKEN")

print("═"*60); print("🔥 DEATHROLL STUDIO v38.1 – COMPLETE MULTI‑GAME ENGINE")
print(f"🤖 Version: {BOT_VERSION}") ; print(f"✅ Telegram: {'✅' if TELEGRAM_TOKEN else '❌'}")
print(f"✅ OpenAI: {'✅' if OPENAI_KEY else '❌'}") ; print(f"✅ GitHub: {'✅' if GITHUB_TOKEN else '❌'}")
print("═"*60)

# ============================================================
# ART DIRECTOR
# ============================================================
class ArtDirector:
    @staticmethod
    def generate(name, genre, style, template):
        sprite_path = Path("sprite.png")
        prompts = {
            "shooter": "action shooter with gun", "platformer": "character jumping",
            "puzzle": "puzzle pieces", "racer": "race car", "horror": "creepy monster",
            "strategy": "tower defense base", "roguelike": "adventurer with sword"
        }
        full_prompt = f"game art for '{name}', {genre}, {style}, {prompts.get(template,'')}"
        try:
            url = f"https://image.pollinations.ai/prompt/{full_prompt.replace(' ','+')}?width=512&height=512"
            r = requests.get(url, timeout=45)
            if r.status_code==200 and len(r.content)>5000:
                sprite_path.write_bytes(r.content); return sprite_path
        except: pass
        # fallback
        icons = {"shooter":"🔫","platformer":"🏃","puzzle":"🧩","racer":"🏎️","horror":"👻","strategy":"🏰","roguelike":"⚔️"}
        icon = icons.get(template, "🎮")
        img = Image.new('RGB',(512,512),color=(20,20,40))
        draw = ImageDraw.Draw(img)
        draw.text((200,200), icon, fill=(255,255,255))
        draw.text((180,400), name[:15], fill=(255,255,255))
        draw.text((200,430), genre[:12], fill=(200,200,200))
        img.save(sprite_path)
        return sprite_path

# ============================================================
# AI SERVICE (unchanged)
# ============================================================
class AIService:
    def __init__(self, key): self.key=key; self.enabled=bool(key)
    def generate(self, prompt, max_tokens=150, temp=0.8):
        if not self.enabled: return None
        try:
            r = requests.post("https://api.openai.com/v1/chat/completions",
                headers={"Authorization":f"Bearer {self.key}"},
                json={"model":"gpt-4o-mini","messages":[{"role":"user","content":prompt}],
                      "temperature":temp,"max_tokens":max_tokens}, timeout=30)
            if r.status_code==200: return r.json()["choices"][0]["message"]["content"].strip().strip('"')
        except: pass
        return None
    def generate_game_design(self, genre, previous):
        if not self.enabled: return self._fallback(genre)
        recent_m = [g.get("mechanic","") for g in previous[-5:] if g.get("mechanic")]
        recent_n = [g.get("name","") for g in previous[-5:] if g.get("name")]
        prompt = f"""Design a unique game:
Genre: {genre}
Avoid: {', '.join(recent_m[:3]) if recent_m else 'none'}
Avoid names: {', '.join(recent_n[:3]) if recent_n else 'none'}
Return JSON: {{"name":"...","mechanic":"...","mechanic_description":"...","hook":"...","visual_style":"neon/dark_fantasy/cartoon/pixel/minimalist","game_mode":"endless/waves/time_attack/boss_fight/survival","difficulty":"easy/medium/hard"}}"""
        result = self.generate(prompt, max_tokens=300, temp=1.0)
        if result:
            import re
            m = re.search(r'\{.*\}', result, re.DOTALL)
            if m:
                try: return json.loads(m.group())
                except: pass
        return self._fallback(genre)
    def _fallback(self, genre):
        names = [("Neon","Runner"),("Cyber","Drifter"),("Quantum","Breach"),("Astral","Vector"),("Void","Pulse")]
        mechanics = [("Phase Echo","summon a temporal duplicate"),("Chrono Fracture","slow time"),("Void Step","teleport")]
        hooks = ["Every second counts.","One mechanic changes everything.","Fight. Survive. Evolve."]
        styles = ["neon","dark_fantasy","cartoon","pixel","minimalist"]
        modes = ["endless","waves","time_attack","boss_fight","survival"]
        name = f"{random.choice(names)[0]} {random.choice(names)[1]}"
        mech = random.choice(mechanics)
        return {"name":name,"mechanic":mech[0],"mechanic_description":mech[1],"hook":random.choice(hooks),
                "visual_style":random.choice(styles),"game_mode":random.choice(modes),
                "difficulty":random.choice(["easy","medium","hard"])}
    def generate_description(self, game):
        if not self.enabled:
            return f"Step into {game['name']}, a {game['genre']} where {game['mechanic']} changes everything."
        prompt = f"Write a professional game description for:\nGame: {game['name']}\nGenre: {game['genre']}\nMechanic: {game['mechanic']} - {game['mechanic_description']}\nHook: {game['hook']}\nWrite 2-3 sentences. Professional tone, no emojis."
        result = self.generate(prompt, max_tokens=120, temp=0.7)
        return result if (result and len(result)>30) else f"Step into {game['name']}, a {game['genre']} where {game['mechanic']} changes everything."

# ============================================================
# GAME DESIGN SYSTEM
# ============================================================
class GameDesignSystem:
    GENRES = ["top-down shooter","action RPG","racing game","puzzle game","survival horror","fighting game","strategy game","platformer","tower defense","roguelite"]
    THEMES = {
        "neon": {"bg":["#0a0a2e","#1a1a3e"],"primary":"#4ecdc4","secondary":"#ff6b6b","accent":"#ffd93d","glow":True},
        "dark_fantasy": {"bg":["#0a0a0a","#1a0a0a"],"primary":"#8b0000","secondary":"#ff4444","accent":"#ffd700","glow":False},
        "cartoon": {"bg":["#1a2a3a","#2a4a5a"],"primary":"#ff6b35","secondary":"#f7c948","accent":"#4ecdc4","glow":False},
        "minimalist": {"bg":["#f5f5f5","#e8e8e8"],"primary":"#2c3e50","secondary":"#3498db","accent":"#2ecc71","glow":False},
        "pixel": {"bg":["#1a1a2e","#16213e"],"primary":"#00ff88","secondary":"#ff0066","accent":"#ffcc00","glow":True}
    }
    MODES = {"endless":"Endless","waves":"Wave Defense","time_attack":"Time Attack","boss_fight":"Boss Fight","survival":"Survival"}
    STYLES = {"shooter":{"enemy_speed":1.2,"spawn_rate":4,"player_health":50},
              "survival":{"enemy_speed":1.5,"spawn_rate":3,"player_health":100},
              "collector":{"enemy_speed":0.8,"spawn_rate":2,"player_health":75},
              "wave_defense":{"enemy_speed":1.8,"spawn_rate":5,"player_health":80}}
    def __init__(self, ai): self.ai=ai; self.sar=self._load_sar()
    def _load_sar(self):
        p=Path("sar_analysis.json")
        if p.exists():
            try: return json.loads(p.read_text())
            except: pass
        return {"study":{"games":[]},"analysis":{}}
    def select_genre(self):
        best = self.sar.get("analysis",{}).get("best_genre")
        if best and best in self.GENRES and random.random()<0.4: return best
        return random.choice(self.GENRES)
    def generate(self):
        genre = self.select_genre()
        prev = self.sar.get("study",{}).get("games",[])
        design = self.ai.generate_game_design(genre, prev)
        return {
            "genre": genre,
            "name": design.get("name", f"{random.choice(['Neon','Cyber','Quantum'])} {random.choice(['Runner','Drifter','Breach'])}"),
            "mechanic": design.get("mechanic", "Phase Echo"),
            "mechanic_description": design.get("mechanic_description", "summon a temporal duplicate"),
            "hook": design.get("hook", "Every second counts."),
            "visual_style": design.get("visual_style", random.choice(list(self.THEMES.keys()))),
            "game_mode": design.get("game_mode", random.choice(list(self.MODES.keys()))),
            "difficulty": design.get("difficulty", "medium"),
            "game_style": random.choice(list(self.STYLES.keys()))
        }

def generate_license(name):
    return f"DR-{''.join([w[0] for w in name.split()[:2]]).upper()}-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

class Portfolio:
    def __init__(self): self.path=Path("portfolio.json"); self._ensure()
    def _ensure(self):
        if not self.path.exists(): self.path.write_text("[]")
    def add(self, entry):
        data=self._load(); data.append(entry); self._save(data[-200:]); return len(data)
    def _load(self):
        try: return json.loads(self.path.read_text())
        except: return []
    def _save(self, data): self.path.write_text(json.dumps(data, indent=2))

class Telegram:
    def __init__(self, token):
        self.token=token; self.enabled=bool(token); self.bot_url=f"https://api.telegram.org/bot{token}" if token else ""
    def send_photo(self, chat_id, photo, caption):
        if not self.enabled: return False
        try:
            with open(photo,"rb") as f:
                r = requests.post(f"{self.bot_url}/sendPhoto", files={"photo":f},
                                  data={"chat_id":chat_id,"caption":caption[:1000],"parse_mode":"HTML"}, timeout=60)
                if r.status_code==200: return True
                r = requests.post(f"{self.bot_url}/sendPhoto", files={"photo":f},
                                  data={"chat_id":chat_id,"caption":caption[:1000]}, timeout=60)
                return r.status_code==200
        except: return False
    def send_message(self, chat_id, text):
        if not self.enabled: return False
        try:
            r = requests.post(f"{self.bot_url}/sendMessage", json={"chat_id":chat_id,"text":text[:1000],"parse_mode":"HTML"}, timeout=30)
            if r.status_code==200: return True
            r = requests.post(f"{self.bot_url}/sendMessage", json={"chat_id":chat_id,"text":text[:1000]}, timeout=30)
            return r.status_code==200
        except: return False
    def send_document(self, chat_id, doc, caption):
        if not self.enabled: return False
        try:
            with open(doc,"rb") as f:
                r = requests.post(f"{self.bot_url}/sendDocument", files={"document":f},
                                  data={"chat_id":chat_id,"caption":caption[:200]}, timeout=60)
            return r.status_code==200
        except: return False

# ============================================================
# HTML5 GAME ENGINE – FULLY IMPLEMENTED, ALL VARIABLES DEFINED
# ============================================================
def _select_template(genre):
    mapping = {"shooter":"shooter","action rpg":"shooter","platformer":"platformer","puzzle":"puzzle",
               "racing":"racer","horror":"horror","survival horror":"horror","strategy":"strategy",
               "tower defense":"strategy","roguelite":"roguelike"}
    for k,v in mapping.items():
        if k in genre.lower(): return v
    return "shooter"

def generate_html5(game, theme, style, sprite_rel="icon.png"):
    p, s, a = theme["primary"], theme["secondary"], theme["accent"]
    glow = "true" if theme["glow"] else "false"
    bg0, bg1 = theme["bg"][0], theme["bg"][1]
    hp = style["player_health"]; speed = style["enemy_speed"]; spawn = style["spawn_rate"]
    name, genre, mechanic, hook = game["name"], game["genre"], game["mechanic"], game["hook"]
    mode = game["game_mode"]; time_limit = 60 if mode=="time_attack" else 0
    template = _select_template(genre)

    # ----- Build the JavaScript engine for the selected template -----
    # We'll build a string with all needed values interpolated.
    if template == "shooter":
        game_js = _build_shooter_js(hp, speed, spawn, mechanic, mode, time_limit, bg0, bg1, name, genre, hook, p, s, a)
    elif template == "platformer":
        game_js = _build_platformer_js(hp, mechanic, bg0, bg1, name, genre, hook, p, s, a)
    elif template == "puzzle":
        game_js = _build_puzzle_js(mechanic, bg0, bg1, name, genre, hook, p, s, a)
    elif template == "racer":
        game_js = _build_racer_js(speed, mechanic, bg0, bg1, name, genre, hook, p, s, a)
    elif template == "horror":
        game_js = _build_horror_js(mechanic, bg0, bg1, name, genre, hook, p, s, a)
    elif template == "strategy":
        game_js = _build_strategy_js(mechanic, bg0, bg1, name, genre, hook, p, s, a)
    elif template == "roguelike":
        game_js = _build_roguelike_js(mechanic, bg0, bg1, name, genre, hook, p, s, a)
    else:
        game_js = _build_shooter_js(hp, speed, spawn, mechanic, mode, time_limit, bg0, bg1, name, genre, hook, p, s, a)

    # Common HTML shell with player image and theme
    return f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>{name}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{background:linear-gradient(135deg,{bg0},{bg1});min-height:100vh;display:flex;justify-content:center;align-items:center;font-family:'Segoe UI',sans-serif;touch-action:none;overflow:hidden;user-select:none}}
.wrapper{{text-align:center;padding:5px;max-width:100%}}.header{{display:flex;justify-content:space-between;align-items:center;padding:0 5px;margin-bottom:3px}}
.title{{font-size:1.1rem;color:{p};text-shadow:{'0 0 15px '+p if theme['glow'] else 'none'};font-weight:bold}}
.stats{{display:flex;gap:8px;color:#aaa;font-size:0.65rem}}.stats span{{background:rgba(0,0,0,0.3);padding:2px 8px;border-radius:10px}}
.canvas-wrapper{{position:relative;display:inline-block;width:100%;max-width:700px}}
canvas{{border:3px solid {p};border-radius:12px;box-shadow:{'0 0 30px '+p if theme['glow'] else '0 0 15px rgba(0,0,0,0.5)'};width:100%;height:auto;background:{bg0};display:block;touch-action:none;cursor:pointer}}
.touch-controls{{width:100%;max-width:700px;margin:3px auto 0;display:flex;justify-content:space-between;align-items:center;padding:3px 8px}}
.touch-joystick{{width:70px;height:70px;border-radius:50%;background:rgba(255,255,255,0.08);border:2px solid {p}44;position:relative}}
.touch-joystick-inner{{width:25px;height:25px;border-radius:50%;background:{p};position:absolute;top:22px;left:22px;box-shadow:0 0 15px {p}44}}
.touch-btn{{width:55px;height:55px;border-radius:50%;background:{p}33;border:2px solid {p};color:#fff;font-size:0.55rem;font-weight:bold;display:flex;align-items:center;justify-content:center;text-align:center;line-height:1.1;padding:4px;box-shadow:0 0 15px {p}44}}
.touch-btn:active{{background:{p}66;transform:scale(0.9)}}
.controls{{color:#666;font-size:0.55rem;margin-top:2px}}
@media(max-width:500px){{.title{{font-size:0.9rem}}.touch-joystick{{width:55px;height:55px}}.touch-joystick-inner{{width:18px;height:18px;top:18px;left:18px}}.touch-btn{{width:40px;height:40px;font-size:0.45rem}}}}
</style>
</head><body>
<div class="wrapper">
<div class="header"><div class="title">{name}</div><div class="stats"><span id="w">🌊 1</span><span id="e">👾 0</span><span id="mode">⚡ {mode[:6]}</span></div></div>
<div class="canvas-wrapper"><canvas id="c" width="900" height="600"></canvas></div>
<div class="touch-controls">
<div class="touch-joystick" id="joystick"><div class="touch-joystick-inner" id="ji"></div></div>
<div class="touch-btn" id="mb">⚡<br>{mechanic[:6]}</div>
</div>
<div class="controls">WASD / Joystick • SPACE / Button for {mechanic}</div>
</div>
<script>
const playerImg = new Image(); playerImg.src = '{sprite_rel}';
const C = {{p:'{p}',s:'{s}',a:'{a}',g:{glow}}};
const canvas = document.getElementById('c'), ctx = canvas.getContext('2d');

// ========== GAME ENGINE ==========
{game_js}

// ========== COMMON CONTROLS ==========
let keys={{}}, jActive=false, jX=0, jY=0;
const j=document.getElementById('joystick'), ji=document.getElementById('ji');
j.addEventListener('touchstart',e=>{{e.preventDefault();jActive=true;updateJoy(e);}});
j.addEventListener('touchmove',e=>{{e.preventDefault();if(jActive)updateJoy(e);}});
j.addEventListener('touchend',e=>{{e.preventDefault();jActive=false;jX=0;jY=0;ji.style.transform='translate(0,0)';}});
function updateJoy(e){{const r=j.getBoundingClientRect(),t=e.touches[0];let x=(t.clientX-r.left-22)/22,y=(t.clientY-r.top-22)/22;const d=Math.hypot(x,y);if(d>1){{x/=d;y/=d;}}jX=x;jY=y;ji.style.transform=`translate(${{x*12}}px,${{y*12}}px)`;}}
document.getElementById('mb').addEventListener('touchstart',e=>{{e.preventDefault();simulateKey(' ');}});
document.getElementById('mb').addEventListener('mousedown',()=>simulateKey(' '));
function simulateKey(k){{const ev=new KeyboardEvent('keydown',{{key:k}});document.dispatchEvent(ev);setTimeout(()=>{{document.dispatchEvent(new KeyboardEvent('keyup',{{key:k}}));}},150);}}
function restartGame(){{ G.p = {{x:450,y:300,size:22,h:100,mh:100}}; G.enemies=[]; G.particles=[]; G.powerups=[]; G.projectiles=[]; G.score=0; G.combo=0; G.maxCombo=0; G.wave=1; G.kills=0; G.gameOver=false; G.started=true; G.cd=0; G.bossActive=false; G.shieldActive=false; G.shieldTimer=0; G.spawnTimer=30; G.difficulty=1; if(G.mode==='time_attack')G.time={time_limit}; if(G.mode==='boss_fight')G.bossActive=false; }}
document.addEventListener('keydown',function(e){{const k=e.key.toLowerCase();keys[k]=true;if(e.key===' '){{e.preventDefault();if(!G.started){{G.started=true;G.spawnTimer=30;}}else useMechanic();}} if((e.key==='r'||e.key==='R')&&G.gameOver)restartGame();}});
document.addEventListener('keyup',function(e){{keys[e.key.toLowerCase()]=false;}});
canvas.addEventListener('click',function(){{if(!G.started&&!G.gameOver){{G.started=true;G.spawnTimer=30;}}}});
canvas.addEventListener('touchstart',function(e){{e.preventDefault();if(!G.started&&!G.gameOver){{G.started=true;G.spawnTimer=30;}}}});
function loop(){{update();draw();requestAnimationFrame(loop);}}
loop();
</script>
</body></html>'''

# ----- Builder functions for each template (all variables passed) -----
def _build_shooter_js(hp, speed, spawn, mechanic, mode, time_limit, bg0, bg1, name, genre, hook, p, s, a):
    return f'''
const G = {{
    p:{{x:450,y:300,size:22,h:{hp},mh:{hp}}},
    enemies:[], particles:[], powerups:[], projectiles:[],
    score:0, combo:0, maxCombo:0, wave:1, kills:0,
    gameOver:false, started:false, cd:0, maxCd:90,
    bossActive:false, bossHealth:0, bossMaxHealth:0,
    shieldActive:false, shieldTimer:0, spawnTimer:0, difficulty:1,
    mode:'{mode}', time:{time_limit}, maxTime:{time_limit}
}};
function spawnEnemy(){{const side=Math.floor(Math.random()*4); let x,y; switch(side){{case 0:x=Math.random()*900;y=-20;break;case 1:x=920;y=Math.random()*600;break;case 2:x=Math.random()*900;y=620;break;case 3:x=-20;y=Math.random()*600;break;}} const hp2=1+Math.floor(G.wave/4); const size=18+Math.min(G.wave,5); G.enemies.push({{x,y,size,hp:hp2,maxHp:hp2,speed:1.2+G.wave*0.06,type:Math.random()>0.75?'fast':'normal',damage:8+Math.floor(G.wave/2)}});}}
function useMechanic(){{if(G.cd>0)return;G.cd=G.maxCd; G.enemies.forEach(e=>{{const dx=e.x-G.p.x,dy=e.y-G.p.y,d=Math.hypot(dx,dy);if(d<180){{const ang=Math.atan2(dy,dx);e.x+=Math.cos(ang)*100;e.y+=Math.sin(ang)*100;e.hp-=2;addParticles(e.x,e.y,C.s,5);}}}}); for(let i=0;i<8;i++){{const ang=(i/8)*Math.PI*2; G.projectiles.push({{x:G.p.x,y:G.p.y,vx:Math.cos(ang)*8,vy:Math.sin(ang)*8,life:60}});}} addParticles(G.p.x,G.p.y,C.p,30); if(G.p.h<G.p.mh*0.3){{G.shieldActive=true;G.shieldTimer=90;}}}}
function addParticles(x,y,color,c){{for(let i=0;i<c;i++)G.particles.push({{x:x+(Math.random()-0.5)*20,y:y+(Math.random()-0.5)*20,vx:(Math.random()-0.5)*8,vy:(Math.random()-0.5)*8,life:20+Math.random()*30,maxLife:50,color,size:2+Math.random()*5}});}}
function update(){{if(G.gameOver||!G.started)return; if(G.mode==='time_attack'&&G.maxTime>0){{G.time-=1/60; if(G.time<=0){{G.gameOver=true;return;}}}} let dx=0,dy=0,speed=4.5+G.difficulty*0.2; if(keys['w']||keys['ArrowUp'])dy=-speed; if(keys['s']||keys['ArrowDown'])dy=speed; if(keys['a']||keys['ArrowLeft'])dx=-speed; if(keys['d']||keys['ArrowRight'])dx=speed; if(jActive){{dx+=jX*speed*0.6;dy+=jY*speed*0.6;}} if(dx&&dy){{dx*=0.707;dy*=0.707;}} G.p.x=Math.max(20,Math.min(880,G.p.x+dx)); G.p.y=Math.max(20,Math.min(580,G.p.y+dy)); if(G.cd>0)G.cd--; if(G.shieldActive){{G.shieldTimer--; if(G.shieldTimer<=0)G.shieldActive=false;}} G.spawnTimer--; if(G.spawnTimer<=0){{const count=1+Math.floor(G.wave/4); for(let i=0;i<count;i++)spawnEnemy(); G.spawnTimer=Math.max(20,60-G.wave*2);}} if(G.mode==='boss_fight'&&G.wave%3===0&&!G.bossActive&&G.enemies.length===0){{G.bossActive=true;G.bossMaxHealth=30+G.wave*15;G.bossHealth=G.bossMaxHealth; G.enemies.push({{x:450,y:50,size:55,hp:G.bossMaxHealth,maxHp:G.bossMaxHealth,speed:1.0+G.wave*0.04,type:'boss',damage:15}});}} for(let i=G.enemies.length-1;i>=0;i--){{const e=G.enemies[i]; const dx2=G.p.x-e.x,dy2=G.p.y-e.y,d=Math.hypot(dx2,dy2); if(d>0){{const spd=e.type==='fast'?e.speed*1.6:e.speed; e.x+=(dx2/d)*spd; e.y+=(dy2/d)*spd;}} e.x=Math.max(10,Math.min(890,e.x)); e.y=Math.max(10,Math.min(590,e.y)); const cd=Math.hypot(G.p.x-e.x,G.p.y-e.y); if(cd<G.p.size/2+e.size/2){{if(G.shieldActive){{const ang=Math.atan2(e.y-G.p.y,e.x-G.p.x); e.x+=Math.cos(ang)*60;e.y+=Math.sin(ang)*60;e.hp-=3;addParticles(e.x,e.y,C.p,10);}}else{{G.p.h-=e.damage; G.combo=0; addParticles(G.p.x,G.p.y,C.s,15); if(G.p.h<=0){{G.p.h=0;G.gameOver=true;return;}}}}}} if(e.hp<=0){{G.score+=10*(1+Math.floor(G.combo/10)); G.combo++; G.kills++; if(G.combo>G.maxCombo)G.maxCombo=G.combo; spawnPowerup(e.x,e.y); addParticles(e.x,e.y,C.s,20); G.enemies.splice(i,1); if(G.enemies.length===0&&!G.bossActive){{G.wave++; G.difficulty=1+G.wave*0.1; G.spawnTimer=20;}}}}}}
for(let i=G.projectiles.length-1;i>=0;i--){{const b=G.projectiles[i]; b.x+=b.vx;b.y+=b.vy;b.life--; if(b.life<=0||b.x<0||b.x>900||b.y<0||b.y>600){{G.projectiles.splice(i,1);continue;}} for(let j=G.enemies.length-1;j>=0;j--){{const e=G.enemies[j]; if(Math.hypot(b.x-e.x,b.y-e.y)<e.size/2+5){{e.hp-=2; addParticles(b.x,b.y,C.a,8); G.projectiles.splice(i,1); break;}}}}}}
for(let i=G.powerups.length-1;i>=0;i--){{const pw=G.powerups[i]; pw.life--; if(pw.life<=0){{G.powerups.splice(i,1);continue;}} const d=Math.hypot(G.p.x-pw.x,G.p.y-pw.y); if(d<G.p.size/2+pw.size/2){{if(pw.type==='health')G.p.h=Math.min(G.p.mh,G.p.h+30); else if(pw.type==='shield'){{G.shieldActive=true;G.shieldTimer=120;}} else if(pw.type==='score')G.score+=50; addParticles(pw.x,pw.y,C.a,15); G.powerups.splice(i,1);}}}}
for(let i=G.particles.length-1;i>=0;i--){{const p=G.particles[i]; p.x+=p.vx;p.y+=p.vy; p.vx*=0.97;p.vy*=0.97; p.life--; if(p.life<=0)G.particles.splice(i,1);}}
document.getElementById('w').textContent='🌊 '+G.wave; document.getElementById('e').textContent='👾 '+G.enemies.length;
}}
function draw(){{const grad=ctx.createRadialGradient(450,300,100,450,300,500); grad.addColorStop(0,'{bg1}'); grad.addColorStop(1,'{bg0}'); ctx.fillStyle=grad; ctx.fillRect(0,0,900,600); ctx.strokeStyle='rgba(255,255,255,0.03)'; ctx.lineWidth=1; for(let i=0;i<900;i+=50){{ctx.beginPath();ctx.moveTo(i,0);ctx.lineTo(i,600);ctx.stroke();ctx.beginPath();ctx.moveTo(0,i);ctx.lineTo(900,i);ctx.stroke();}} G.powerups.forEach(pw=>{{ctx.fillStyle=pw.type==='health'?'#ff4444':pw.type==='shield'?'#4ecdc4':'#ffd93d'; ctx.shadowColor=ctx.fillStyle; ctx.shadowBlur=15; ctx.beginPath(); ctx.arc(pw.x,pw.y,pw.size/2,0,Math.PI*2); ctx.fill(); ctx.shadowBlur=0; ctx.fillStyle='#fff'; ctx.font='12px monospace'; ctx.fillText(pw.type==='health'?'❤️':pw.type==='shield'?'🛡️':'⭐',pw.x-8,pw.y-8);}}); G.projectiles.forEach(b=>{{ctx.fillStyle=C.a; ctx.shadowColor=C.a; ctx.shadowBlur=10; ctx.beginPath(); ctx.arc(b.x,b.y,4,0,Math.PI*2); ctx.fill(); ctx.shadowBlur=0;}}); G.enemies.forEach(e=>{{const grad2=ctx.createRadialGradient(e.x-5,e.y-5,5,e.x,e.y,e.size); grad2.addColorStop(0,e.type==='boss'?'#ff0044':C.s); grad2.addColorStop(1,e.type==='boss'?'#cc0033':'#cc4444'); ctx.fillStyle=grad2; ctx.shadowColor=e.type==='boss'?'#ff0000':C.s; ctx.shadowBlur=e.type==='boss'?30:10; ctx.beginPath(); ctx.arc(e.x,e.y,e.size/2,0,Math.PI*2); ctx.fill(); ctx.shadowBlur=0; const w=e.type==='boss'?80:e.size; ctx.fillStyle='#444'; ctx.fillRect(e.x-w/2,e.y-e.size/2-10,w,4); ctx.fillStyle=e.type==='boss'?'#ff0044':'#4ecdc4'; ctx.fillRect(e.x-w/2,e.y-e.size/2-10,w*(e.hp/e.maxHp),4); ctx.fillStyle='#fff'; ctx.font=e.type==='boss'?'30px monospace':'18px monospace'; ctx.fillText(e.type==='boss'?'👹':'👾',e.x-12,e.y-8); if(e.type==='boss'){{ctx.fillStyle='#ff0044'; ctx.font='bold 14px monospace'; ctx.fillText('BOSS',e.x-20,e.y-e.size/2-18);}}}}); if(playerImg.complete&&playerImg.naturalWidth){{const px=G.p.x-30,py=G.p.y-30; ctx.drawImage(playerImg,px,py,60,60);}}else{{const grad3=ctx.createRadialGradient(G.p.x-8,G.p.y-8,5,G.p.x,G.p.y,G.p.size); grad3.addColorStop(0,G.shieldActive?'#4ecdc4':C.p); grad3.addColorStop(1,G.shieldActive?'#2a9d8f':'#2a7d8f'); ctx.fillStyle=grad3; ctx.shadowColor=G.shieldActive?'#4ecdc4':C.p; ctx.shadowBlur=G.shieldActive?40:20; ctx.beginPath(); ctx.arc(G.p.x,G.p.y,G.p.size/2,0,Math.PI*2); ctx.fill(); ctx.shadowBlur=0; if(G.shieldActive){{ctx.strokeStyle=C.p; ctx.lineWidth=3; ctx.shadowColor=C.p; ctx.shadowBlur=30; ctx.beginPath(); ctx.arc(G.p.x,G.p.y,G.p.size/2+8,0,Math.PI*2); ctx.stroke(); ctx.shadowBlur=0;}} ctx.fillStyle='#fff'; ctx.font='22px monospace'; ctx.fillText('🎮',G.p.x-14,G.p.y-10);}} G.particles.forEach(p=>{{const a=p.life/p.maxLife; ctx.globalAlpha=a; ctx.fillStyle=p.color; ctx.shadowColor=p.color; ctx.shadowBlur=8; ctx.beginPath(); ctx.arc(p.x,p.y,p.size*a,0,Math.PI*2); ctx.fill(); ctx.shadowBlur=0; ctx.globalAlpha=1;}}); ctx.shadowBlur=0; ctx.fillStyle='#fff'; ctx.font='bold 22px monospace'; ctx.fillText('SCORE: '+G.score,20,40); ctx.fillStyle='#ff4444'; ctx.fillRect(20,55,200,12); ctx.fillStyle=C.p; ctx.fillRect(20,55,(G.p.h/G.p.mh)*200,12); ctx.fillStyle='#fff'; ctx.font='10px monospace'; ctx.fillText('HP: '+Math.round(G.p.h)+'/'+G.p.mh,25,67); if(G.combo>0){{ctx.fillStyle=C.a; ctx.font='bold 16px monospace'; ctx.fillText('⚡ '+G.combo+'x',20,110);}} if(G.mode==='time_attack'&&G.maxTime>0){{ctx.fillStyle=G.time<10?'#ff4444':'#fff'; ctx.font='bold 18px monospace'; ctx.fillText('⏱️ '+Math.ceil(G.time)+'s',20,145);}} if(G.cd>0){{ctx.fillStyle='rgba(255,255,255,0.2)'; ctx.fillRect(20,165,G.cd*2,6);}} ctx.fillStyle='#888'; ctx.font='10px monospace'; ctx.fillText('⚡ '+G.cd+'/'+G.maxCd,20,183); if(G.gameOver){{ctx.fillStyle='rgba(0,0,0,0.8)'; ctx.fillRect(0,0,900,600); ctx.fillStyle='#fff'; ctx.font='bold 48px monospace'; ctx.textAlign='center'; ctx.fillText('GAME OVER',450,230); ctx.font='24px monospace'; ctx.fillStyle=C.a; ctx.fillText('Score: '+G.score,450,290); ctx.font='18px monospace'; ctx.fillStyle='#aaa'; ctx.fillText('Wave: '+G.wave+' • Combo: '+G.maxCombo+' • Kills: '+G.kills,450,340); ctx.font='16px monospace'; ctx.fillStyle='#888'; ctx.fillText('Press R to restart',450,400); ctx.textAlign='left');}} if(!G.started&&!G.gameOver){{ctx.fillStyle='rgba(0,0,0,0.7)'; ctx.fillRect(0,0,900,600); ctx.fillStyle='#fff'; ctx.font='bold 36px monospace'; ctx.textAlign='center'; ctx.fillText('🎮 {name}',450,200); ctx.font='18px monospace'; ctx.fillStyle=C.p; ctx.fillText('Genre: {genre}',450,255); ctx.font='16px monospace'; ctx.fillStyle=C.s; ctx.fillText('Mechanic: {mechanic}',450,290); ctx.font='14px monospace'; ctx.fillStyle=C.a; ctx.fillText('"{hook}"',450,325); ctx.font='16px monospace'; ctx.fillStyle='#fff'; ctx.fillText('Press SPACE / Tap to Start',450,385); ctx.textAlign='left');}}}}
function spawnPowerup(x,y){{if(Math.random()>0.12)return; const types=['health','shield','score']; G.powerups.push({{x:x,y:y,size:14,type:types[Math.floor(Math.random()*types.length)],life:300}});}}
'''

def _build_platformer_js(hp, mechanic, bg0, bg1, name, genre, hook, p, s, a):
    return f'''
const G = {{p:{{x:100,y:400,size:20,h:{hp},mh:{hp},vy:0,onGround:false}}, platforms:[], enemies:[], coins:[], particles:[], score:0, gameOver:false, started:false, cd:0, maxCd:60}};
function initPlatforms(){{for(let i=0;i<12;i++){{let x=i*80, y=350+Math.sin(i*0.8)*60; G.platforms.push({{x,y,w:70,h:12}});}}}}
function useMechanic(){{if(G.cd>0)return; G.cd=G.maxCd; G.p.vy=-15; addParticles(G.p.x,G.p.y,C.p,20);}}
function addParticles(x,y,c,count){{for(let i=0;i<count;i++)G.particles.push({{x:x+(Math.random()-0.5)*20,y:y+(Math.random()-0.5)*20,vx:(Math.random()-0.5)*6,vy:(Math.random()-0.5)*6,life:20+Math.random()*20,maxLife:40,color:c,size:2+Math.random()*4}});}}
function update(){{if(G.gameOver||!G.started)return; let dx=0,speed=4; if(keys['a']||keys['ArrowLeft'])dx=-speed; if(keys['d']||keys['ArrowRight'])dx=speed; if(jActive){{dx+=jX*speed*0.6;}} G.p.x+=dx; G.p.x=Math.max(10,Math.min(890,G.p.x)); G.p.vy+=0.6; G.p.y+=G.p.vy; G.p.onGround=false; G.platforms.forEach(p=>{{if(G.p.x+10>p.x&&G.p.x-10<p.x+p.w&&G.p.y+10>p.y&&G.p.y-10<p.y+p.h){{if(G.p.vy>0){{G.p.y=p.y-10; G.p.vy=0; G.p.onGround=true;}}}}}}); if(G.p.y>650){{G.gameOver=true;return;}} if(G.cd>0)G.cd--; if(keys['w']||keys['ArrowUp']){{if(G.p.onGround){{G.p.vy=-8;}}}} G.coins.forEach((c,i)=>{{if(Math.hypot(G.p.x-c.x,G.p.y-c.y)<20){{G.score+=10; G.coins.splice(i,1);}}}}); G.enemies.forEach((e,i)=>{{e.x+=e.vx; if(e.x<10||e.x>890)e.vx*=-1; if(Math.hypot(G.p.x-e.x,G.p.y-e.y)<25){{if(G.p.vy>0){{G.score+=20; G.enemies.splice(i,1); G.p.vy=-8;}}else{{G.gameOver=true;}}}}}}); for(let i=G.particles.length-1;i>=0;i--){{const p=G.particles[i]; p.x+=p.vx;p.y+=p.vy; p.vy+=0.1; p.life--; if(p.life<=0)G.particles.splice(i,1);}}
document.getElementById('w').textContent='🏆 '+G.score; document.getElementById('e').textContent='🪙 '+G.coins.length;
}}
function draw(){{ctx.fillStyle='{bg0}'; ctx.fillRect(0,0,900,600); G.platforms.forEach(p=>{{ctx.fillStyle=C.p; ctx.fillRect(p.x,p.y,p.w,p.h);}}); G.coins.forEach(c=>{{ctx.fillStyle='#ffd93d'; ctx.shadowColor='#ffd93d'; ctx.shadowBlur=15; ctx.beginPath(); ctx.arc(c.x,c.y,10,0,Math.PI*2); ctx.fill(); ctx.shadowBlur=0;}}); G.enemies.forEach(e=>{{ctx.fillStyle=C.s; ctx.beginPath(); ctx.arc(e.x,e.y,15,0,Math.PI*2); ctx.fill(); ctx.fillStyle='#fff'; ctx.font='20px monospace'; ctx.fillText('👾',e.x-12,e.y-10);}}); if(playerImg.complete&&playerImg.naturalWidth){{ctx.drawImage(playerImg,G.p.x-25,G.p.y-25,50,50);}}else{{ctx.fillStyle=C.p; ctx.beginPath(); ctx.arc(G.p.x,G.p.y,15,0,Math.PI*2); ctx.fill();}} G.particles.forEach(p=>{{const a=p.life/p.maxLife; ctx.globalAlpha=a; ctx.fillStyle=p.color; ctx.beginPath(); ctx.arc(p.x,p.y,p.size*a,0,Math.PI*2); ctx.fill(); ctx.globalAlpha=1;}}); ctx.fillStyle='#fff'; ctx.font='bold 20px monospace'; ctx.fillText('SCORE: '+G.score,20,40); if(G.gameOver){{ctx.fillStyle='rgba(0,0,0,0.7)'; ctx.fillRect(0,0,900,600); ctx.fillStyle='#fff'; ctx.font='bold 48px monospace'; ctx.textAlign='center'; ctx.fillText('GAME OVER',450,250); ctx.font='24px monospace'; ctx.fillStyle=C.a; ctx.fillText('Score: '+G.score,450,310); ctx.font='18px monospace'; ctx.fillStyle='#aaa'; ctx.fillText('Press R to restart',450,370); ctx.textAlign='left');}} if(!G.started&&!G.gameOver){{ctx.fillStyle='rgba(0,0,0,0.7)'; ctx.fillRect(0,0,900,600); ctx.fillStyle='#fff'; ctx.font='bold 36px monospace'; ctx.textAlign='center'; ctx.fillText('🎮 {name}',450,220); ctx.font='18px monospace'; ctx.fillStyle=C.p; ctx.fillText('Genre: {genre}',450,280); ctx.font='16px monospace'; ctx.fillStyle=C.s; ctx.fillText('Press SPACE / Tap to Start',450,340); ctx.textAlign='left');}}}}
function restartGame(){{G.p={{x:100,y:400,h:{hp},mh:{hp},vy:0,onGround:false}}; G.enemies=[]; G.coins=[]; G.particles=[]; G.score=0; G.gameOver=false; G.started=true; G.cd=0; initPlatforms(); for(let i=0;i<5;i++){{G.enemies.push({{x:100+Math.random()*700,y:300+Math.random()*100,vx:(Math.random()>0.5?1:-1)*1.5}});}} for(let i=0;i<20;i++){{G.coins.push({{x:50+Math.random()*800,y:100+Math.random()*400}});}}}}
initPlatforms(); for(let i=0;i<5;i++){{G.enemies.push({{x:100+Math.random()*700,y:300+Math.random()*100,vx:(Math.random()>0.5?1:-1)*1.5}});}} for(let i=0;i<20;i++){{G.coins.push({{x:50+Math.random()*800,y:100+Math.random()*400}});}}
'''

def _build_puzzle_js(mechanic, bg0, bg1, name, genre, hook, p, s, a):
    return '''
const G = {tiles:[], selected:[], matched:0, pairs:6, score:0, moves:0, gameOver:false, started:false};
const emojis = ['🍎','🍌','🍇','🍉','🍓','🍒'];
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];} return a;}
function initPuzzle(){ let arr=[...emojis,...emojis]; shuffle(arr); G.tiles=arr.map((v,i)=>({id:i,value:v,revealed:false,matched:false})); G.matched=0; G.score=0; G.moves=0; }
function useMechanic(){ G.tiles.forEach(t=>{t.revealed=false;}); G.selected=[]; }
function update(){ if(G.gameOver||!G.started)return; }
function draw(){ ctx.fillStyle='#1a1a3a'; ctx.fillRect(0,0,900,600); const cols=4, rows=3, w=120, h=120, gap=20; const startX=(900-(cols*(w+gap)-gap))/2, startY=(600-(rows*(h+gap)-gap))/2; G.tiles.forEach((t,i)=>{ const col=i%cols, row=Math.floor(i/cols); const x=startX+col*(w+gap), y=startY+row*(h+gap); if(t.matched){ ctx.fillStyle='rgba(0,255,0,0.1)'; }else if(t.revealed){ ctx.fillStyle='#2a2a5a'; ctx.shadowColor=C.p; ctx.shadowBlur=15; ctx.fillRect(x,y,w,h); ctx.shadowBlur=0; ctx.fillStyle='#fff'; ctx.font='48px sans-serif'; ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText(t.value,x+w/2,y+h/2); }else{ ctx.fillStyle='#4a4a7a'; ctx.fillRect(x,y,w,h); ctx.fillStyle='#666'; ctx.font='30px sans-serif'; ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText('❓',x+w/2,y+h/2); } }); ctx.textAlign='left'; ctx.textBaseline='top'; ctx.fillStyle='#fff'; ctx.font='bold 20px monospace'; ctx.fillText('Score: '+G.score,20,40); ctx.fillText('Moves: '+G.moves,20,80); if(G.matched===G.pairs){ G.gameOver=true; ctx.fillStyle='rgba(0,0,0,0.7)'; ctx.fillRect(0,0,900,600); ctx.fillStyle='#fff'; ctx.font='bold 48px monospace'; ctx.textAlign='center'; ctx.fillText('YOU WIN!',450,250); ctx.font='24px monospace'; ctx.fillStyle=C.a; ctx.fillText('Score: '+G.score,450,310); ctx.font='18px monospace'; ctx.fillStyle='#aaa'; ctx.fillText('Press R to restart',450,370); ctx.textAlign='left'; } if(!G.started&&!G.gameOver){ ctx.fillStyle='rgba(0,0,0,0.7)'; ctx.fillRect(0,0,900,600); ctx.fillStyle='#fff'; ctx.font='bold 36px monospace'; ctx.textAlign='center'; ctx.fillText('🧩 MEMORY PUZZLE',450,220); ctx.font='18px monospace'; ctx.fillStyle=C.p; ctx.fillText('Click tiles to match pairs',450,280); ctx.font='16px monospace'; ctx.fillStyle=C.s; ctx.fillText('Press SPACE / Tap to Start',450,340); ctx.textAlign='left'; } }
function handlePuzzleClick(ex,ey){ if(G.gameOver||!G.started)return; const cols=4, rows=3, w=120, h=120, gap=20; const startX=(900-(cols*(w+gap)-gap))/2, startY=(600-(rows*(h+gap)-gap))/2; for(let i=0;i<G.tiles.length;i++){ const t=G.tiles[i]; if(t.matched)continue; const col=i%cols, row=Math.floor(i/cols); const x=startX+col*(w+gap), y=startY+row*(h+gap); if(ex>=x&&ex<=x+w&&ey>=y&&ey<=y+h){ if(G.selected.length===2)return; if(t.revealed)return; t.revealed=true; G.selected.push(i); if(G.selected.length===2){ G.moves++; const idx1=G.selected[0], idx2=G.selected[1]; if(G.tiles[idx1].value===G.tiles[idx2].value){ G.tiles[idx1].matched=true; G.tiles[idx2].matched=true; G.matched++; G.score+=10; G.selected=[]; }else{ setTimeout(()=>{ G.tiles[idx1].revealed=false; G.tiles[idx2].revealed=false; G.selected=[]; },600); } } break; } } }
canvas.addEventListener('click',function(e){ const rect=canvas.getBoundingClientRect(); const scaleX=canvas.width/rect.width, scaleY=canvas.height/rect.height; const ex=(e.clientX-rect.left)*scaleX, ey=(e.clientY-rect.top)*scaleY; if(!G.started){ G.started=true; initPuzzle(); }else{ handlePuzzleClick(ex,ey); } });
canvas.addEventListener('touchstart',function(e){ e.preventDefault(); const rect=canvas.getBoundingClientRect(); const scaleX=canvas.width/rect.width, scaleY=canvas.height/rect.height; const touch=e.touches[0]; const ex=(touch.clientX-rect.left)*scaleX, ey=(touch.clientY-rect.top)*scaleY; if(!G.started){ G.started=true; initPuzzle(); }else{ handlePuzzleClick(ex,ey); } });
function restartGame(){ initPuzzle(); G.gameOver=false; G.started=true; }
initPuzzle();
'''

def _build_racer_js(speed, mechanic, bg0, bg1, name, genre, hook, p, s, a):
    return f'''
const G = {{player:{{x:450,y:550,w:40,h:60}}, obstacles:[], score:0, speed:{speed}, gameOver:false, started:false}};
function useMechanic(){{G.speed+=2;}}
function update(){{if(G.gameOver||!G.started)return; let dx=0; if(keys['a']||keys['ArrowLeft'])dx=-5; if(keys['d']||keys['ArrowRight'])dx=5; if(jActive)dx+=jX*3; G.player.x=Math.max(20,Math.min(880,G.player.x+dx)); G.speed=Math.min(8,G.speed+0.01); if(Math.random()<0.03){{G.obstacles.push({{x:Math.random()*860+20,y:-30,w:40+Math.random()*30,h:40+Math.random()*30}});}} for(let i=G.obstacles.length-1;i>=0;i--){{const o=G.obstacles[i]; o.y+=G.speed; if(o.y>650){{G.obstacles.splice(i,1); G.score++; continue;}} if(o.x<G.player.x+G.player.w/2&&o.x+o.w>G.player.x-G.player.w/2&&o.y<G.player.y+G.player.h/2&&o.y+o.h>G.player.y-G.player.h/2){{G.gameOver=true;}}}} document.getElementById('w').textContent='🏎️ '+G.score; document.getElementById('e').textContent='🚗 '+G.obstacles.length;
}}
function draw(){{ctx.fillStyle='{bg0}'; ctx.fillRect(0,0,900,600); ctx.strokeStyle='#444'; ctx.lineWidth=2; for(let i=0;i<600;i+=40){{ctx.beginPath(); ctx.moveTo(450,i+ (Date.now()/100)%40 -40); ctx.lineTo(450,i+ (Date.now()/100)%40); ctx.stroke();}} G.obstacles.forEach(o=>{{ctx.fillStyle=C.s; ctx.fillRect(o.x,o.y,o.w,o.h); ctx.fillStyle='#fff'; ctx.font='20px monospace'; ctx.fillText('🚗',o.x,o.y+20);}}); if(playerImg.complete&&playerImg.naturalWidth){{ctx.drawImage(playerImg,G.player.x-20,G.player.y-30,40,60);}}else{{ctx.fillStyle=C.p; ctx.fillRect(G.player.x-20,G.player.y-30,40,60);}} ctx.fillStyle='#fff'; ctx.font='bold 20px monospace'; ctx.fillText('Score: '+G.score,20,40); if(G.gameOver){{ctx.fillStyle='rgba(0,0,0,0.7)'; ctx.fillRect(0,0,900,600); ctx.fillStyle='#fff'; ctx.font='bold 48px monospace'; ctx.textAlign='center'; ctx.fillText('CRASH!',450,250); ctx.font='24px monospace'; ctx.fillStyle=C.a; ctx.fillText('Score: '+G.score,450,310); ctx.font='18px monospace'; ctx.fillStyle='#aaa'; ctx.fillText('Press R to restart',450,370); ctx.textAlign='left');}} if(!G.started&&!G.gameOver){{ctx.fillStyle='rgba(0,0,0,0.7)'; ctx.fillRect(0,0,900,600); ctx.fillStyle='#fff'; ctx.font='bold 36px monospace'; ctx.textAlign='center'; ctx.fillText('🏎️ RACER',450,220); ctx.font='18px monospace'; ctx.fillStyle=C.p; ctx.fillText('Avoid the cars!',450,280); ctx.font='16px monospace'; ctx.fillStyle=C.s; ctx.fillText('Press SPACE / Tap to Start',450,340); ctx.textAlign='left');}}}}
function restartGame(){{G.player={{x:450,y:550,w:40,h:60}}; G.obstacles=[]; G.score=0; G.speed={speed}; G.gameOver=false; G.started=true;}}
'''

def _build_horror_js(mechanic, bg0, bg1, name, genre, hook, p, s, a):
    return '''
const G = {player:{x:450,y:300,size:20,stealth:100}, monsters:[], keys:[], foundKeys:0, totalKeys:5, gameOver:false, started:false, cd:0, maxCd:60};
function useMechanic(){ if(G.cd>0)return; G.cd=G.maxCd; G.player.stealth=Math.min(100,G.player.stealth+20); }
function update(){ if(G.gameOver||!G.started)return; let dx=0,dy=0,s=3; if(keys['w']||keys['ArrowUp'])dy=-s; if(keys['s']||keys['ArrowDown'])dy=s; if(keys['a']||keys['ArrowLeft'])dx=-s; if(keys['d']||keys['ArrowRight'])dx=s; if(jActive){dx+=jX*s*0.6;dy+=jY*s*0.6;} if(dx&&dy){dx*=0.707;dy*=0.707;} G.player.x=Math.max(20,Math.min(880,G.player.x+dx)); G.player.y=Math.max(20,Math.min(580,G.player.y+dy)); if(G.cd>0)G.cd--; G.player.stealth=Math.min(100,G.player.stealth+0.1); if(Math.random()<0.01){ G.monsters.push({x:Math.random()*880+10,y:Math.random()*580+10}); } G.monsters.forEach(m=>{ const d=Math.hypot(G.player.x-m.x,G.player.y-m.y); if(d<100){ const s2=(100-d)/100; G.player.stealth-=s2*0.5; if(G.player.stealth<=0){ G.gameOver=true; } } }); if(G.keys.length<G.totalKeys&&Math.random()<0.005){ G.keys.push({x:Math.random()*880+10,y:Math.random()*580+10}); } G.keys.forEach((k,i)=>{ if(Math.hypot(G.player.x-k.x,G.player.y-k.y)<20){ G.foundKeys++; G.keys.splice(i,1); } }); if(G.foundKeys>=G.totalKeys){ G.gameOver=true; } document.getElementById('w').textContent='🔑 '+G.foundKeys+'/'+G.totalKeys; document.getElementById('e').textContent='👻 '+G.monsters.length; }
function draw(){ ctx.fillStyle='#0a0a0a'; ctx.fillRect(0,0,900,600); const grad=ctx.createRadialGradient(G.player.x,G.player.y,50,G.player.x,G.player.y,250); grad.addColorStop(0,'rgba(255,255,255,0.05)'); grad.addColorStop(1,'rgba(0,0,0,0.9)'); ctx.fillStyle=grad; ctx.fillRect(0,0,900,600); G.keys.forEach(k=>{ ctx.fillStyle='#ffd93d'; ctx.shadowColor='#ffd93d'; ctx.shadowBlur=20; ctx.beginPath(); ctx.arc(k.x,k.y,12,0,Math.PI*2); ctx.fill(); ctx.shadowBlur=0; ctx.fillStyle='#000'; ctx.font='16px monospace'; ctx.fillText('🔑',k.x-8,k.y-8); }); G.monsters.forEach(m=>{ ctx.fillStyle='#ff4444'; ctx.shadowColor='#ff4444'; ctx.shadowBlur=20; ctx.beginPath(); ctx.arc(m.x,m.y,20,0,Math.PI*2); ctx.fill(); ctx.shadowBlur=0; ctx.fillStyle='#fff'; ctx.font='30px monospace'; ctx.fillText('👻',m.x-15,m.y-12); }); if(playerImg.complete&&playerImg.naturalWidth){ ctx.drawImage(playerImg,G.player.x-20,G.player.y-20,40,40); }else{ ctx.fillStyle='#4ecdc4'; ctx.beginPath(); ctx.arc(G.player.x,G.player.y,15,0,Math.PI*2); ctx.fill(); } ctx.fillStyle='#444'; ctx.fillRect(20,55,200,12); ctx.fillStyle=G.player.stealth>50?'#4ecdc4':'#ff4444'; ctx.fillRect(20,55,G.player.stealth*2,12); ctx.fillStyle='#fff'; ctx.font='10px monospace'; ctx.fillText('Stealth',25,67); ctx.fillStyle='#fff'; ctx.font='bold 20px monospace'; ctx.fillText('🔑 '+G.foundKeys+'/'+G.totalKeys,20,40); if(G.gameOver){ ctx.fillStyle='rgba(0,0,0,0.8)'; ctx.fillRect(0,0,900,600); ctx.fillStyle='#fff'; ctx.font='bold 48px monospace'; ctx.textAlign='center'; if(G.foundKeys>=G.totalKeys){ ctx.fillText('YOU ESCAPED!',450,230); ctx.fillStyle=C.a; ctx.fillText('All keys collected!',450,300); }else{ ctx.fillText('CAUGHT!',450,230); } ctx.font='18px monospace'; ctx.fillStyle='#aaa'; ctx.fillText('Press R to restart',450,370); ctx.textAlign='left'; } if(!G.started&&!G.gameOver){ ctx.fillStyle='rgba(0,0,0,0.8)'; ctx.fillRect(0,0,900,600); ctx.fillStyle='#fff'; ctx.font='bold 36px monospace'; ctx.textAlign='center'; ctx.fillText('👻 HORROR',450,220); ctx.font='18px monospace'; ctx.fillStyle=C.p; ctx.fillText('Find all keys without being caught',450,280); ctx.font='16px monospace'; ctx.fillStyle=C.s; ctx.fillText('Press SPACE / Tap to Start',450,340); ctx.textAlign='left'; } }}
function restartGame(){ G.player={x:450,y:300,stealth:100}; G.monsters=[]; G.keys=[]; G.foundKeys=0; G.gameOver=false; G.started=true; G.cd=0; }
'''

def _build_strategy_js(mechanic, bg0, bg1, name, genre, hook, p, s, a):
    return '''
const G = {towers:[], enemies:[], projectiles:[], baseHealth:100, gold:50, wave:1, gameOver:false, started:false, spawnTimer:0};
function useMechanic(){ G.gold+=20; }
function update(){ if(G.gameOver||!G.started)return; G.spawnTimer--; if(G.spawnTimer<=0){ const count=2+G.wave; for(let i=0;i<count;i++){ G.enemies.push({x:Math.random()*880+10,y:0,hp:3+G.wave, speed:1+G.wave*0.2}); } G.spawnTimer=60-G.wave*2; if(G.spawnTimer<20)G.spawnTimer=20; } for(let i=G.enemies.length-1;i>=0;i--){ const e=G.enemies[i]; e.y+=e.speed; if(e.y>600){ G.baseHealth-=10; G.enemies.splice(i,1); if(G.baseHealth<=0){ G.gameOver=true; return; } continue; } G.towers.forEach(t=>{ if(Math.hypot(t.x-e.x,t.y-e.y)<150){ G.projectiles.push({x:t.x,y:t.y,target:i}); } }); } for(let i=G.projectiles.length-1;i>=0;i--){ const p=G.projectiles[i]; const e=G.enemies[p.target]; if(!e){ G.projectiles.splice(i,1); continue; } const dx=e.x-p.x, dy=e.y-p.y, d=Math.hypot(dx,dy); if(d<5){ e.hp-=2; G.projectiles.splice(i,1); if(e.hp<=0){ G.gold+=5; G.enemies.splice(p.target,1); } }else{ p.x+=dx/d*5; p.y+=dy/d*5; } } if(G.enemies.length===0){ G.wave++; G.spawnTimer=20; } document.getElementById('w').textContent='🌊 '+G.wave; document.getElementById('e').textContent='👾 '+G.enemies.length; }
function draw(){ ctx.fillStyle='#1a1a3a'; ctx.fillRect(0,0,900,600); ctx.fillStyle='#4ecdc4'; ctx.fillRect(400,550,100,50); ctx.fillStyle='#fff'; ctx.font='14px monospace'; ctx.fillText('🏰 BASE',420,580); G.towers.forEach(t=>{ ctx.fillStyle=C.p; ctx.fillRect(t.x-15,t.y-15,30,30); }); G.enemies.forEach(e=>{ ctx.fillStyle=C.s; ctx.beginPath(); ctx.arc(e.x,e.y,15,0,Math.PI*2); ctx.fill(); ctx.fillStyle='#fff'; ctx.fillText('👾',e.x-12,e.y-10); }); G.projectiles.forEach(p=>{ ctx.fillStyle=C.a; ctx.beginPath(); ctx.arc(p.x,p.y,5,0,Math.PI*2); ctx.fill(); }); ctx.fillStyle='#fff'; ctx.font='bold 20px monospace'; ctx.fillText('Gold: '+G.gold,20,40); ctx.fillText('Base: '+G.baseHealth,20,80); if(G.gameOver){ ctx.fillStyle='rgba(0,0,0,0.7)'; ctx.fillRect(0,0,900,600); ctx.fillStyle='#fff'; ctx.font='bold 48px monospace'; ctx.textAlign='center'; ctx.fillText('BASE DESTROYED',450,250); ctx.font='24px monospace'; ctx.fillStyle=C.a; ctx.fillText('Wave: '+G.wave,450,310); ctx.font='18px monospace'; ctx.fillStyle='#aaa'; ctx.fillText('Press R to restart',450,370); ctx.textAlign='left'; } if(!G.started&&!G.gameOver){ ctx.fillStyle='rgba(0,0,0,0.7)'; ctx.fillRect(0,0,900,600); ctx.fillStyle='#fff'; ctx.font='bold 36px monospace'; ctx.textAlign='center'; ctx.fillText('🏰 TOWER DEFENSE',450,220); ctx.font='18px monospace'; ctx.fillStyle=C.p; ctx.fillText('Click to place towers',450,280); ctx.font='16px monospace'; ctx.fillStyle=C.s; ctx.fillText('Press SPACE / Tap to Start',450,340); ctx.textAlign='left'; } }
canvas.addEventListener('click',function(e){ if(!G.started||G.gameOver)return; const rect=canvas.getBoundingClientRect(); const scaleX=canvas.width/rect.width, scaleY=canvas.height/rect.height; const ex=(e.clientX-rect.left)*scaleX, ey=(e.clientY-rect.top)*scaleY; if(G.gold>=30){ G.towers.push({x:ex,y:ey}); G.gold-=30; } });
canvas.addEventListener('touchstart',function(e){ e.preventDefault(); if(!G.started||G.gameOver)return; const rect=canvas.getBoundingClientRect(); const scaleX=canvas.width/rect.width, scaleY=canvas.height/rect.height; const touch=e.touches[0]; const ex=(touch.clientX-rect.left)*scaleX, ey=(touch.clientY-rect.top)*scaleY; if(G.gold>=30){ G.towers.push({x:ex,y:ey}); G.gold-=30; } });
function restartGame(){ G.towers=[]; G.enemies=[]; G.projectiles=[]; G.baseHealth=100; G.gold=50; G.wave=1; G.gameOver=false; G.started=true; G.spawnTimer=30; }
'''

def _build_roguelike_js(mechanic, bg0, bg1, name, genre, hook, p, s, a):
    return '''
const G = {player:{x:1,y:1,hp:10,maxHp:10}, dungeon:[], visible:[], monsters:[], turn:0, gameOver:false, started:false, cd:0, maxCd:60};
function generateDungeon(){ const size=8; G.dungeon=[]; for(let y=0;y<size;y++){ const row=[]; for(let x=0;x<size;x++){ row.push(Math.random()<0.25?1:0); } G.dungeon.push(row); } G.dungeon[1][1]=0; G.dungeon[size-2][size-2]=0; G.player={x:1,y:1,hp:10,maxHp:10}; G.monsters=[]; for(let i=0;i<4;i++){ let mx,my; do{mx=Math.floor(Math.random()*size); my=Math.floor(Math.random()*size);}while(G.dungeon[my][mx]!==0||(mx===1&&my===1)); G.monsters.push({x:mx,y:my,hp:3}); } }
function useMechanic(){ if(G.cd>0)return; G.cd=G.maxCd; G.player.hp=Math.min(G.player.maxHp,G.player.hp+3); }
function update(){ if(G.gameOver||!G.started)return; }
function draw(){ const size=8; const cellSize=90; const offsetX=(900-size*cellSize)/2, offsetY=(600-size*cellSize)/2; ctx.fillStyle='#1a1a3a'; ctx.fillRect(0,0,900,600); for(let y=0;y<size;y++){ for(let x=0;x<size;x++){ const px=offsetX+x*cellSize, py=offsetY+y*cellSize; if(G.dungeon[y][x]===1){ ctx.fillStyle='#444'; }else{ ctx.fillStyle='#2a2a4a'; } ctx.fillRect(px,py,cellSize,cellSize); ctx.strokeStyle='#555'; ctx.strokeRect(px,py,cellSize,cellSize); G.monsters.forEach(m=>{ if(m.x===x&&m.y===y){ ctx.fillStyle='#ff4444'; ctx.beginPath(); ctx.arc(px+cellSize/2,py+cellSize/2,15,0,Math.PI*2); ctx.fill(); ctx.fillStyle='#fff'; ctx.font='20px monospace'; ctx.fillText('👾',px+cellSize/2-10,py+cellSize/2-8); } }); if(G.player.x===x&&G.player.y===y){ if(playerImg.complete&&playerImg.naturalWidth){ ctx.drawImage(playerImg,px+10,py+10,cellSize-20,cellSize-20); }else{ ctx.fillStyle=C.p; ctx.beginPath(); ctx.arc(px+cellSize/2,py+cellSize/2,20,0,Math.PI*2); ctx.fill(); ctx.fillStyle='#fff'; ctx.font='24px monospace'; ctx.fillText('🎮',px+cellSize/2-12,py+cellSize/2-10); } } } } ctx.fillStyle='#fff'; ctx.font='bold 20px monospace'; ctx.fillText('HP: '+G.player.hp+'/'+G.player.maxHp,20,40); ctx.fillText('Turn: '+G.turn,20,80); if(G.gameOver){ ctx.fillStyle='rgba(0,0,0,0.7)'; ctx.fillRect(0,0,900,600); ctx.fillStyle='#fff'; ctx.font='bold 48px monospace'; ctx.textAlign='center'; ctx.fillText('GAME OVER',450,250); ctx.font='24px monospace'; ctx.fillStyle=C.a; ctx.fillText('Survived '+G.turn+' turns',450,310); ctx.font='18px monospace'; ctx.fillStyle='#aaa'; ctx.fillText('Press R to restart',450,370); ctx.textAlign='left'; } if(!G.started&&!G.gameOver){ ctx.fillStyle='rgba(0,0,0,0.7)'; ctx.fillRect(0,0,900,600); ctx.fillStyle='#fff'; ctx.font='bold 36px monospace'; ctx.textAlign='center'; ctx.fillText('⚔️ ROGUELIKE',450,220); ctx.font='18px monospace'; ctx.fillStyle=C.p; ctx.fillText('Explore the dungeon!',450,280); ctx.font='16px monospace'; ctx.fillStyle=C.s; ctx.fillText('Press SPACE / Tap to Start',450,340); ctx.textAlign='left'; } }
function movePlayer(dx,dy){ if(G.gameOver||!G.started)return; const nx=G.player.x+dx, ny=G.player.y+dy; const size=8; if(nx<0||nx>=size||ny<0||ny>=size)return; if(G.dungeon[ny][nx]===1)return; let monsterHit=false; G.monsters.forEach(m=>{ if(m.x===nx&&m.y===ny){ G.player.hp-=2; monsterHit=true; if(G.player.hp<=0){ G.gameOver=true; return; } } }); if(monsterHit)return; G.player.x=nx; G.player.y=ny; G.turn++; G.monsters.forEach(m=>{ const dirs=[[1,0],[-1,0],[0,1],[0,-1]]; const shuffled=dirs.sort(()=>Math.random()-0.5); for(let d of shuffled){ const mnx=m.x+d[0], mny=m.y+d[1]; if(mnx<0||mnx>=size||mny<0||mny>=size)continue; if(G.dungeon[mny][mnx]===1)continue; if(mnx===G.player.x&&mny===G.player.y){ G.player.hp-=2; if(G.player.hp<=0){ G.gameOver=true; } break; } if(!G.monsters.some(mm=>mm.x===mnx&&mm.y===mny)){ m.x=mnx; m.y=mny; break; } } }); G.monsters=G.monsters.filter(m=>m.hp>0); }
document.addEventListener('keydown',function(e){ const k=e.key; if(k==='w'||k==='ArrowUp'){movePlayer(0,-1);} if(k==='s'||k==='ArrowDown'){movePlayer(0,1);} if(k==='a'||k==='ArrowLeft'){movePlayer(-1,0);} if(k==='d'||k==='ArrowRight'){movePlayer(1,0);} });
let touchStartX=0, touchStartY=0; canvas.addEventListener('touchstart',function(e){ const t=e.touches[0]; touchStartX=t.clientX; touchStartY=t.clientY; }); canvas.addEventListener('touchend',function(e){ const dx=touchStartX-e.changedTouches[0].clientX; const dy=touchStartY-e.changedTouches[0].clientY; if(Math.abs(dx)>20||Math.abs(dy)>20){ if(Math.abs(dx)>Math.abs(dy)){ movePlayer(dx>0?-1:1,0); }else{ movePlayer(0,dy>0?-1:1); } } });
function restartGame(){ generateDungeon(); G.turn=0; G.gameOver=false; G.started=true; G.cd=0; }
generateDungeon();
'''

# ============================================================
# MAIN BOT
# ============================================================
class DeathRollStudio:
    def __init__(self):
        self.ai = AIService(OPENAI_KEY)
        self.design = GameDesignSystem(self.ai)
        self.portfolio = Portfolio()
        self.telegram = Telegram(TELEGRAM_TOKEN)

    def run(self):
        print("\n"+"═"*60); print("🎮 GENERATING NEW GAME"); print("═"*60)
        game = self.design.generate()
        template = _select_template(game["genre"])
        print(f"   📝 Name: {game['name']}")
        print(f"   🎭 Genre: {game['genre']} → Template: {template}")
        print(f"   ⚡ Mechanic: {game['mechanic']}")
        print(f"   🎨 Style: {game['visual_style']}")

        price = self._price(game); game["price"] = price
        print(f"   💰 Price: ${price} SOL")
        if "description" not in game:
            game["description"] = self.ai.generate_description(game)
        print(f"   📝 {game['description'][:80]}...")
        license_key = generate_license(game["name"])
        print(f"   🔑 License: {license_key}")

        ArtDirector.generate(game["name"], game["genre"], game["visual_style"], template)
        print(f"   🎨 Art: Generated")

        html5_url = self._build(game, license_key, template)
        print(f"   🌐 HTML5: {html5_url}")

        entry = {
            "date": datetime.now().isoformat(),
            "game": game["name"], "genre": game["genre"], "mechanic": game["mechanic"],
            "description": game["description"], "hook": game["hook"],
            "visual_style": game["visual_style"], "game_mode": game["game_mode"],
            "price": price, "license_key": license_key, "html5_url": html5_url,
            "version": BOT_VERSION
        }
        total = self.portfolio.add(entry)
        print(f"   📊 Portfolio: {total} games")
        if self.telegram.enabled:
            self._send_telegram(game, license_key, html5_url)
        else:
            print("   ⚠️ Telegram token missing")
        self._update_sar(game)
        print(f"   🧠 SAR: Updated")
        print("\n"+"═"*60); print("✅ GAME COMPLETE"); print("═"*60)
        print(f"   Game: {game['name']}\n   License: {license_key}\n   HTML5: {html5_url}\n   Portfolio: {total} games")
        print("═"*60)

    def _price(self, game):
        base = 3
        if game["visual_style"] in ["neon","pixel"]: base += 1
        if game["difficulty"] == "hard": base += 2
        elif game["difficulty"] == "medium": base += 1
        if game["game_mode"] == "boss_fight": base += 2
        return min(max(base, CONFIG["price"]["min"]), CONFIG["price"]["max"])

    def _build(self, game, license_key, template):
        theme = GameDesignSystem.THEMES.get(game["visual_style"], GameDesignSystem.THEMES["neon"])
        style = GameDesignSystem.STYLES.get(game["game_style"], GameDesignSystem.STYLES["survival"])
        folder = Path(f"workspace/{game['name'].replace(' ','_')}")
        folder.mkdir(parents=True, exist_ok=True)
        sprite = Path("sprite.png")
        if sprite.exists(): shutil.copy(sprite, folder / "icon.png")
        # Extract color from sprite
        try:
            img = Image.open(sprite)
            avg = img.resize((1,1)).getpixel((0,0))
            theme["primary"] = '#{:02x}{:02x}{:02x}'.format(avg[0], avg[1], avg[2])
        except: pass
        html = generate_html5(game, theme, style, "icon.png")
        (folder / "index.html").write_text(html)
        (folder / "LICENSE.txt").write_text(f"""DEATHROLL STUDIO LICENSE
Game: {game['name']}
License: {license_key}
Price: {game['price']} SOL
Date: {datetime.now().strftime('%Y-%m-%d')}""")
        zip_path = Path("workspace/latest_game.zip")
        try:
            if zip_path.exists(): zip_path.unlink()
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
                for f in folder.rglob("*"):
                    if f.is_file(): z.write(f, f.relative_to(folder.parent))
        except: pass
        return f"https://{CONFIG['brand']['github']}.github.io/FACTORY-BOT-V4/workspace/{game['name'].replace(' ','_')}/index.html"

    def _send_telegram(self, game, license_key, html5_url):
        channel = CONFIG["telegram"]["channel"]
        sprite = Path("sprite.png")
        post = f"""<b>🎮 {game['name']}</b> — {game['genre']}
<b>⚡ {game['mechanic']}</b>
{game['description'][:120]}
🌐 <a href="{html5_url}">Play FREE (HTML5)</a>
💰 <b>Full Game: ${game['price']} SOL</b>
🔑 License: {license_key}
Send ${game['price']} SOL + @username to:
Trust: <code>{CONFIG['wallets']['trust']}</code>
Phantom: <code>{CONFIG['wallets']['phantom']}</code>
#gamedev #{game['genre'].replace(' ','')} #DeathRollStudio"""
        if channel:
            if sprite.exists(): self.telegram.send_photo(channel, sprite, post)
            else: self.telegram.send_message(channel, post)
        if TELEGRAM_CHAT_ID:
            if sprite.exists(): self.telegram.send_photo(TELEGRAM_CHAT_ID, sprite, post)
            else: self.telegram.send_message(TELEGRAM_CHAT_ID, post)
            zip_path = Path("workspace/latest_game.zip")
            if zip_path.exists():
                self.telegram.send_document(TELEGRAM_CHAT_ID, zip_path, f"🎮 {game['name']}\n🔑 {license_key}")

    def _update_sar(self, game):
        path = Path("sar_analysis.json")
        if path.exists():
            try: data = json.loads(path.read_text())
            except: data = {"study":{"games":[]},"analysis":{}}
        else: data = {"study":{"games":[]},"analysis":{}}
        data["study"]["games"].append({
            "name": game["name"], "genre": game["genre"], "mechanic": game["mechanic"],
            "game_mode": game.get("game_mode"), "timestamp": datetime.now().isoformat(),
            "price": game["price"]
        })
        data["study"]["games"] = data["study"]["games"][-100:]
        genre_counts = {}
        for g in data["study"]["games"]:
            genre = g.get("genre")
            if genre: genre_counts[genre] = genre_counts.get(genre,0)+1
        if genre_counts: data["analysis"]["best_genre"] = max(genre_counts, key=genre_counts.get)
        path.write_text(json.dumps(data, indent=2))

if __name__ == "__main__":
    bot = DeathRollStudio()
    bot.run()
