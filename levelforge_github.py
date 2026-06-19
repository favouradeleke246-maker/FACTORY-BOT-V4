#!/usr/bin/env python3
"""
DEATHROLL STUDIO v34.0 - COMPREHENSIVE GAME + TELEGRAM FIXED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os
import json
import random
import requests
import time
import shutil
import zipfile
import uuid
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw
from typing import Dict, List, Optional

# ============================================================================
# CONFIGURATION
# ============================================================================

BOT_VERSION = "34.0.0"

CONFIG = {
    "brand": {
        "name": "DeathRoll",
        "email": "favouradeleke246@gmail.com",
        "telegram": "@deathroll1",
        "tiktok": "@deathroll.co",
        "website": "https://deathroll.co",
        "github": "favouradeleke246-maker"
    },
    "wallets": {
        "trust": "6wsQ6nGXrUUUGCEokb4rZcfHDv2a8MomUb22TuVaH2m3",
        "phantom": "Csk9DKstWMdKx19gUHWB9xy2VwZZX2nx6V6oSVGDCgMb"
    },
    "telegram": {
        "channel": "@drolltech"
    },
    "price": {
        "min": 2,
        "max": 10,
        "default": 5
    }
}

# ============================================================================
# ENVIRONMENT
# ============================================================================

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GH_TOKEN")

print("═" * 60)
print("🔥 DEATHROLL STUDIO v34.0 - COMPREHENSIVE GAME")
print("═" * 60)
print(f"🤖 Version: {BOT_VERSION}")
print(f"✅ Telegram: {'✅' if TELEGRAM_TOKEN else '❌'}")
print(f"✅ OpenAI: {'✅' if OPENAI_KEY else '❌'}")
print(f"✅ GitHub: {'✅' if GITHUB_TOKEN else '❌'}")
print(f"📢 Channel: {CONFIG['telegram']['channel']}")
print("═" * 60)

# ============================================================================
# ART DIRECTOR
# ============================================================================

class ArtDirector:
    @staticmethod
    def generate(name: str, genre: str, style: str) -> Path:
        sprite_path = Path("sprite.png")
        try:
            style_map = {
                "neon": "neon cyberpunk, glowing, futuristic",
                "dark_fantasy": "dark fantasy, gothic, dramatic",
                "cartoon": "cartoon style, colorful, playful",
                "minimalist": "minimalist, clean, modern",
                "pixel": "pixel art, retro, 8-bit"
            }
            style_desc = style_map.get(style, "neon cyberpunk")
            prompt = f"professional game character art for '{name}', {genre}, {style_desc}, high quality"
            url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '+')}?width=512&height=512"
            response = requests.get(url, timeout=45)
            if response.status_code == 200 and len(response.content) > 5000:
                sprite_path.write_bytes(response.content)
                return sprite_path
        except:
            pass
        img = Image.new('RGB', (512, 512), color=(20, 20, 40))
        draw = ImageDraw.Draw(img)
        draw.rectangle([50, 50, 462, 462], outline=(78, 205, 196), width=4)
        draw.text((180, 230), name[:15], fill=(255, 255, 255))
        draw.text((200, 260), genre[:12], fill=(200, 200, 200))
        img.save(sprite_path)
        return sprite_path

# ============================================================================
# AI SERVICE
# ============================================================================

class AIService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.enabled = bool(api_key)
    
    def generate(self, prompt: str, max_tokens: int = 150, temperature: float = 0.8) -> Optional[str]:
        if not self.enabled:
            return None
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature,
                    "max_tokens": max_tokens
                },
                timeout=30
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip().strip('"')
        except:
            pass
        return None
    
    def generate_game_design(self, genre: str, previous: List[Dict]) -> Dict:
        if not self.enabled:
            return self._fallback(genre)
        recent_mechanics = [g.get("mechanic", "") for g in previous[-5:] if g.get("mechanic")]
        recent_names = [g.get("name", "") for g in previous[-5:] if g.get("name")]
        prompt = f"""Design a unique game:
Genre: {genre}
Avoid: {', '.join(recent_mechanics[:3]) if recent_mechanics else 'none'}
Avoid names: {', '.join(recent_names[:3]) if recent_names else 'none'}

Return JSON:
{{"name":"creative name","mechanic":"unique mechanic","mechanic_description":"how it works","hook":"one-line hook","visual_style":"neon/dark_fantasy/cartoon/pixel/minimalist","game_mode":"endless/waves/time_attack/boss_fight/survival","difficulty":"easy/medium/hard"}}"""
        result = self.generate(prompt, max_tokens=300, temperature=1.0)
        if result:
            try:
                import re
                match = re.search(r'\{.*\}', result, re.DOTALL)
                if match:
                    return json.loads(match.group())
            except:
                pass
        return self._fallback(genre)
    
    def _fallback(self, genre: str) -> Dict:
        names = [("Neon", "Runner"), ("Cyber", "Drifter"), ("Quantum", "Breach"), ("Astral", "Vector"), ("Void", "Pulse")]
        mechanics = [("Phase Echo", "summon a temporal duplicate"), ("Chrono Fracture", "slow time"), ("Void Step", "teleport")]
        hooks = ["Every second counts.", "One mechanic changes everything.", "Fight. Survive. Evolve."]
        styles = ["neon", "dark_fantasy", "cartoon", "pixel", "minimalist"]
        modes = ["endless", "waves", "time_attack", "boss_fight", "survival"]
        name = f"{random.choice(names)[0]} {random.choice(names)[1]}"
        mechanic = random.choice(mechanics)
        return {
            "name": name,
            "mechanic": mechanic[0],
            "mechanic_description": mechanic[1],
            "hook": random.choice(hooks),
            "visual_style": random.choice(styles),
            "game_mode": random.choice(modes),
            "difficulty": random.choice(["easy", "medium", "hard"])
        }
    
    def generate_description(self, game_data: Dict) -> str:
        if not self.enabled:
            return f"Step into {game_data['name']}, a {game_data['genre']} where {game_data['mechanic']} changes everything."
        prompt = f"""Write a professional game description for:
Game: {game_data['name']}
Genre: {game_data['genre']}
Mechanic: {game_data['mechanic']} - {game_data['mechanic_description']}
Hook: {game_data['hook']}
Write 2-3 sentences. Professional tone, no emojis."""
        result = self.generate(prompt, max_tokens=120, temperature=0.7)
        return result if result and len(result) > 30 else self._fallback_description(game_data)
    
    def _fallback_description(self, game_data: Dict) -> str:
        return f"Step into {game_data['name']}, a {game_data['genre']} where {game_data['mechanic']} changes everything. {game_data['mechanic_description']}. Can you survive the challenge?"

# ============================================================================
# GAME DESIGN SYSTEM
# ============================================================================

class GameDesignSystem:
    GENRES = ["top-down shooter", "action RPG", "racing game", "puzzle game", "survival horror", "fighting game", "strategy game", "platformer", "tower defense", "roguelite"]
    THEMES = {
        "neon": {"bg": ["#0a0a2e", "#1a1a3e"], "primary": "#4ecdc4", "secondary": "#ff6b6b", "accent": "#ffd93d", "glow": True},
        "dark_fantasy": {"bg": ["#0a0a0a", "#1a0a0a"], "primary": "#8b0000", "secondary": "#ff4444", "accent": "#ffd700", "glow": False},
        "cartoon": {"bg": ["#1a2a3a", "#2a4a5a"], "primary": "#ff6b35", "secondary": "#f7c948", "accent": "#4ecdc4", "glow": False},
        "minimalist": {"bg": ["#f5f5f5", "#e8e8e8"], "primary": "#2c3e50", "secondary": "#3498db", "accent": "#2ecc71", "glow": False},
        "pixel": {"bg": ["#1a1a2e", "#16213e"], "primary": "#00ff88", "secondary": "#ff0066", "accent": "#ffcc00", "glow": True}
    }
    MODES = {"endless": "Endless", "waves": "Wave Defense", "time_attack": "Time Attack", "boss_fight": "Boss Fight", "survival": "Survival"}
    STYLES = {"shooter": {"enemy_speed": 1.2, "spawn_rate": 4, "player_health": 50}, "survival": {"enemy_speed": 1.5, "spawn_rate": 3, "player_health": 100}, "collector": {"enemy_speed": 0.8, "spawn_rate": 2, "player_health": 75}, "wave_defense": {"enemy_speed": 1.8, "spawn_rate": 5, "player_health": 80}}
    
    def __init__(self, ai: AIService):
        self.ai = ai
        self.sar = self._load_sar()
    
    def _load_sar(self) -> Dict:
        path = Path("sar_analysis.json")
        if path.exists():
            try:
                return json.loads(path.read_text())
            except:
                pass
        return {"study": {"games": []}, "analysis": {}}
    
    def select_genre(self) -> str:
        best = self.sar.get("analysis", {}).get("best_genre")
        if best and best in self.GENRES and random.random() < 0.4:
            return best
        return random.choice(self.GENRES)
    
    def generate(self) -> Dict:
        genre = self.select_genre()
        previous = self.sar.get("study", {}).get("games", [])
        design = self.ai.generate_game_design(genre, previous)
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

# ============================================================================
# LICENSE SYSTEM
# ============================================================================

def generate_license(game_name: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d")
    unique = str(uuid.uuid4())[:8].upper()
    code = ''.join([w[0] for w in game_name.split()[:2]]).upper()
    return f"DR-{code}-{timestamp}-{unique}"

# ============================================================================
# PORTFOLIO SYSTEM
# ============================================================================

class Portfolio:
    def __init__(self):
        self.path = Path("portfolio.json")
        self._ensure()
    def _ensure(self):
        if not self.path.exists():
            self.path.write_text("[]")
    def add(self, entry: Dict) -> int:
        data = self._load()
        data.append(entry)
        self._save(data[-200:])
        return len(data)
    def _load(self) -> List[Dict]:
        try:
            data = json.loads(self.path.read_text())
            return data if isinstance(data, list) else []
        except:
            return []
    def _save(self, data: List[Dict]):
        self.path.write_text(json.dumps(data, indent=2))

# ============================================================================
# TELEGRAM SERVICE - FIXED (shorter messages, better formatting)
# ============================================================================

class Telegram:
    def __init__(self, token: Optional[str]):
        self.token = token
        self.enabled = bool(token)
    
    def send_photo(self, chat_id: str, photo: Path, caption: str) -> bool:
        if not self.enabled:
            return False
        # Truncate caption if too long (Telegram limit ~1024 chars)
        if len(caption) > 900:
            caption = caption[:900] + "..."
        try:
            with open(photo, "rb") as f:
                r = requests.post(
                    f"https://api.telegram.org/bot{self.token}/sendPhoto",
                    files={"photo": f},
                    data={"chat_id": chat_id, "caption": caption, "parse_mode": "Markdown"},
                    timeout=60
                )
            if r.status_code == 200:
                return True
            else:
                # If Markdown fails, try without
                r = requests.post(
                    f"https://api.telegram.org/bot{self.token}/sendPhoto",
                    files={"photo": f},
                    data={"chat_id": chat_id, "caption": caption.replace('*', '').replace('`', '')},
                    timeout=60
                )
                return r.status_code == 200
        except:
            return False
    
    def send_message(self, chat_id: str, text: str) -> bool:
        if not self.enabled:
            return False
        if len(text) > 900:
            text = text[:900] + "..."
        try:
            r = requests.post(
                f"https://api.telegram.org/bot{self.token}/sendMessage",
                json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
                timeout=30
            )
            if r.status_code == 200:
                return True
            else:
                # Try without Markdown
                r = requests.post(
                    f"https://api.telegram.org/bot{self.token}/sendMessage",
                    json={"chat_id": chat_id, "text": text.replace('*', '').replace('`', '')},
                    timeout=30
                )
                return r.status_code == 200
        except:
            return False
    
    def send_document(self, chat_id: str, doc: Path, caption: str) -> bool:
        if not self.enabled:
            return False
        try:
            with open(doc, "rb") as f:
                r = requests.post(
                    f"https://api.telegram.org/bot{self.token}/sendDocument",
                    files={"document": f},
                    data={"chat_id": chat_id, "caption": caption[:200], "parse_mode": "Markdown"},
                    timeout=60
                )
            return r.status_code == 200
        except:
            return False

# ============================================================================
# HTML5 GAME GENERATOR - COMPREHENSIVE VERSION
# ============================================================================

def generate_html5(game_data: Dict, theme: Dict, style: Dict) -> str:
    p = theme["primary"]
    s = theme["secondary"]
    a = theme["accent"]
    glow = "true" if theme["glow"] else "false"
    bg0 = theme["bg"][0]
    bg1 = theme["bg"][1]
    
    hp = style["player_health"]
    speed = style["enemy_speed"]
    spawn = style["spawn_rate"]
    
    name = game_data["name"]
    genre = game_data["genre"]
    mechanic = game_data["mechanic"]
    hook = game_data.get("hook", "Every second counts.")
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{name}</title>
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{
            background: linear-gradient(135deg, {bg0}, {bg1});
            min-height:100vh;
            display:flex;
            justify-content:center;
            align-items:center;
            font-family:'Segoe UI',sans-serif;
            touch-action:none;
            overflow:hidden;
            user-select:none;
            -webkit-user-select:none;
        }}
        .wrapper {{ text-align:center; padding:5px; max-width:100%; }}
        .header {{
            display:flex;
            justify-content:space-between;
            align-items:center;
            padding:0 5px;
            margin-bottom:3px;
        }}
        .title {{
            font-size:1.2rem;
            color:{p};
            text-shadow: {'0 0 15px ' + p if theme['glow'] else 'none'};
            font-weight:bold;
        }}
        .stats {{
            display:flex;
            gap:10px;
            color:#aaa;
            font-size:0.7rem;
        }}
        .stats span {{ background:rgba(0,0,0,0.3); padding:2px 8px; border-radius:10px; }}
        .canvas-wrapper {{
            position:relative;
            display:inline-block;
            width:100%;
            max-width:700px;
        }}
        canvas {{
            border:3px solid {p};
            border-radius:12px;
            box-shadow: {'0 0 30px ' + p if theme['glow'] else '0 0 15px rgba(0,0,0,0.5)'};
            width:100%;
            height:auto;
            background:{bg0};
            display:block;
            touch-action:none;
            cursor:pointer;
        }}
        .touch-controls {{
            width:100%;
            max-width:700px;
            margin:3px auto 0;
            display:flex;
            justify-content:space-between;
            align-items:center;
            padding:3px 8px;
            touch-action:none;
        }}
        .touch-joystick {{
            width:80px;
            height:80px;
            border-radius:50%;
            background:rgba(255,255,255,0.08);
            border:2px solid {p}44;
            position:relative;
            touch-action:none;
        }}
        .touch-joystick-inner {{
            width:30px;
            height:30px;
            border-radius:50%;
            background:{p};
            position:absolute;
            top:25px;
            left:25px;
            touch-action:none;
            box-shadow: 0 0 15px {p}44;
        }}
        .touch-btn {{
            width:60px;
            height:60px;
            border-radius:50%;
            background:{p}33;
            border:2px solid {p};
            color:#fff;
            font-size:0.6rem;
            font-weight:bold;
            display:flex;
            align-items:center;
            justify-content:center;
            touch-action:none;
            text-align:center;
            line-height:1.1;
            padding:4px;
            box-shadow: 0 0 15px {p}44;
        }}
        .touch-btn:active {{ background:{p}66; transform:scale(0.9); }}
        .controls {{ color:#666; font-size:0.6rem; margin-top:2px; }}
        @media (max-width:500px) {{
            .title {{ font-size:1rem; }}
            .touch-joystick {{ width:60px; height:60px; }}
            .touch-joystick-inner {{ width:22px; height:22px; top:19px; left:19px; }}
            .touch-btn {{ width:45px; height:45px; font-size:0.5rem; }}
        }}
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="header">
            <div class="title">{name}</div>
            <div class="stats">
                <span id="waveDisplay">🌊 1</span>
                <span id="enemyCount">👾 0</span>
            </div>
        </div>
        <div class="canvas-wrapper">
            <canvas id="c" width="900" height="600"></canvas>
        </div>
        <div class="touch-controls">
            <div class="touch-joystick" id="joystick">
                <div class="touch-joystick-inner" id="joystickInner"></div>
            </div>
            <div class="touch-btn" id="mechanicBtn">⚡<br>{mechanic[:6]}</div>
        </div>
        <div class="controls">WASD / Joystick • SPACE / Button for {mechanic}</div>
    </div>
    <script>
        const c=document.getElementById('c'),ctx=c.getContext('2d');
        const C={{p:'{p}',s:'{s}',a:'{a}',g:{glow}}};
        
        // Full game state
        const G = {{
            p: {{x:450,y:300,size:22,h:{hp},mh:{hp}}},
            enemies: [],
            particles: [],
            powerups: [],
            bullets: [],
            score: 0,
            combo: 0,
            maxCombo: 0,
            wave: 1,
            enemiesKilled: 0,
            gameOver: false,
            started: false,
            cd: 0,
            maxCd: 90,
            bossActive: false,
            bossHealth: 0,
            bossMaxHealth: 0,
            shieldActive: false,
            shieldTimer: 0,
            spawnTimer: 0,
            difficulty: 1
        }};
        
        let keys={{}}, jActive=false, jX=0, jY=0;
        
        // Joystick
        const j=document.getElementById('joystick'), ji=document.getElementById('joystickInner');
        j.addEventListener('touchstart',e=>{{e.preventDefault();jActive=true;updateJoy(e);}});
        j.addEventListener('touchmove',e=>{{e.preventDefault();if(jActive)updateJoy(e);}});
        j.addEventListener('touchend',e=>{{e.preventDefault();jActive=false;jX=0;jY=0;ji.style.transform='translate(0,0)';}});
        function updateJoy(e){{const r=j.getBoundingClientRect(),t=e.touches[0];let x=(t.clientX-r.left-30)/30,y=(t.clientY-r.top-30)/30;const d=Math.hypot(x,y);if(d>1){{x/=d;y/=d;}}jX=x;jY=y;ji.style.transform=`translate(${{x*15}}px,${{y*15}}px)`;}}
        
        // Mechanic button
        document.getElementById('mechanicBtn').addEventListener('touchstart',e=>{{e.preventDefault();simulateKey(' ');}});
        document.getElementById('mechanicBtn').addEventListener('mousedown',()=>simulateKey(' '));
        function simulateKey(k){{const ev=new KeyboardEvent('keydown',{{key:k}});document.dispatchEvent(ev);setTimeout(()=>{{document.dispatchEvent(new KeyboardEvent('keyup',{{key:k}}));}},150);}}
        
        // Enemies
        function spawnEnemy() {{
            const side=Math.floor(Math.random()*4);
            let x,y;
            switch(side){{case 0:x=Math.random()*900;y=-20;break;case 1:x=920;y=Math.random()*600;break;case 2:x=Math.random()*900;y=620;break;case 3:x=-20;y=Math.random()*600;break;}}
            const hp=1+Math.floor(G.wave/3);
            const size=20+Math.min(G.wave,5);
            G.enemies.push({{
                x,y,size,
                hp:hp, maxHp:hp,
                speed:1.5+G.wave*0.08,
                type:Math.random()>0.7?'fast':'normal',
                damage:10+Math.floor(G.wave/2)
            }});
        }}
        
        // Powerups
        function spawnPowerup(x,y) {{
            if(Math.random()>0.15)return;
            const types=['health','shield','score'];
            G.powerups.push({{
                x:x,y:y,size:15,
                type:types[Math.floor(Math.random()*types.length)],
                life:300
            }});
        }}
        
        // Particles
        function addParticles(x,y,color,count) {{
            for(let i=0;i<count;i++)G.particles.push({{
                x:x+(Math.random()-0.5)*20,y:y+(Math.random()-0.5)*20,
                vx:(Math.random()-0.5)*8,vy:(Math.random()-0.5)*8,
                life:30+Math.random()*30,maxLife:60,
                color:color,size:2+Math.random()*5
            }});
        }}
        
        // Mechanic
        function useMechanic() {{
            if(G.cd>0)return;G.cd=G.maxCd;
            // Push enemies + damage
            G.enemies.forEach(e=>{{
                const dx=e.x-G.p.x,dy=e.y-G.p.y,d=Math.hypot(dx,dy);
                if(d<180){{
                    const ang=Math.atan2(dy,dx);
                    e.x+=Math.cos(ang)*100;
                    e.y+=Math.sin(ang)*100;
                    e.hp-=2;
                    addParticles(e.x,e.y,C.s,5);
                }}
            }});
            addParticles(G.p.x,G.p.y,C.p,30);
            // Shield if low health
            if(G.p.h<G.p.mh*0.3){{G.shieldActive=true;G.shieldTimer=120;}}
        }}
        
        // Update
        function update() {{
            if(G.gameOver||!G.started)return;
            
            // Player movement
            let dx=0,dy=0,speed=4.5+G.difficulty*0.2;
            if(keys['w']||keys['ArrowUp'])dy=-speed;
            if(keys['s']||keys['ArrowDown'])dy=speed;
            if(keys['a']||keys['ArrowLeft'])dx=-speed;
            if(keys['d']||keys['ArrowRight'])dx=speed;
            if(jActive){{dx+=jX*speed*0.6;dy+=jY*speed*0.6;}}
            if(dx&&dy){{dx*=0.707;dy*=0.707;}}
            G.p.x=Math.max(20,Math.min(880,G.p.x+dx));
            G.p.y=Math.max(20,Math.min(580,G.p.y+dy));
            
            // Cooldowns
            if(G.cd>0)G.cd--;
            if(G.shieldActive){{G.shieldTimer--;if(G.shieldTimer<=0)G.shieldActive=false;}}
            
            // Spawn enemies
            G.spawnTimer--;
            if(G.spawnTimer<=0){{
                const count=1+Math.floor(G.wave/3);
                for(let i=0;i<count;i++)spawnEnemy();
                G.spawnTimer=Math.max(20,60-G.wave*2);
            }}
            
            // Boss every 5 waves
            if(G.wave%5===0&&!G.bossActive&&G.enemies.length===0){{
                G.bossActive=true;
                G.bossMaxHealth=50+G.wave*10;
                G.bossHealth=G.bossMaxHealth;
                G.enemies.push({{
                    x:450,y:50,size:60,
                    hp:G.bossMaxHealth,maxHp:G.bossMaxHealth,
                    speed:1.2+G.wave*0.05,
                    type:'boss',
                    damage:20
                }});
            }}
            
            // Update enemies
            for(let i=G.enemies.length-1;i>=0;i--){{
                const e=G.enemies[i];
                const dx=G.p.x-e.x,dy=G.p.y-e.y,d=Math.hypot(dx,dy);
                if(d>0){{
                    const spd=e.type==='fast'?e.speed*1.5:e.speed;
                    e.x+=(dx/d)*spd;
                    e.y+=(dy/d)*spd;
                }}
                e.x=Math.max(10,Math.min(890,e.x));
                e.y=Math.max(10,Math.min(590,e.y));
                
                // Collision
                const cd=Math.hypot(G.p.x-e.x,G.p.y-e.y);
                if(cd<G.p.size/2+e.size/2){{
                    if(G.shieldActive){{
                        const ang=Math.atan2(e.y-G.p.y,e.x-G.p.x);
                        e.x+=Math.cos(ang)*60;e.y+=Math.sin(ang)*60;
                        e.hp-=3;
                        addParticles(e.x,e.y,C.p,10);
                    }}else{{
                        G.p.h-=e.damage;
                        G.combo=0;
                        addParticles(G.p.x,G.p.y,C.s,15);
                        if(G.p.h<=0){{G.p.h=0;G.gameOver=true;return;}}
                    }}
                }}
                
                // Enemy death
                if(e.hp<=0){{
                    G.score+=10*(1+Math.floor(G.combo/10));
                    G.combo++;G.enemiesKilled++;
                    if(G.combo>G.maxCombo)G.maxCombo=G.combo;
                    spawnPowerup(e.x,e.y);
                    addParticles(e.x,e.y,C.s,20);
                    G.enemies.splice(i,1);
                    
                    // Wave progress
                    if(G.enemies.length===0&&!G.bossActive){{
                        G.wave++;
                        G.difficulty=1+G.wave*0.1;
                        G.spawnTimer=30;
                    }}
                }}
            }}
            
            // Update powerups
            for(let i=G.powerups.length-1;i>=0;i--){{
                const pw=G.powerups[i];
                pw.life--;
                if(pw.life<=0){{G.powerups.splice(i,1);continue;}}
                const d=Math.hypot(G.p.x-pw.x,G.p.y-pw.y);
                if(d<G.p.size/2+pw.size/2){{
                    if(pw.type==='health'){{G.p.h=Math.min(G.p.mh,G.p.h+25);}}
                    else if(pw.type==='shield'){{G.shieldActive=true;G.shieldTimer=90;}}
                    else if(pw.type==='score'){{G.score+=50;}}
                    addParticles(pw.x,pw.y,C.a,15);
                    G.powerups.splice(i,1);
                }}
            }}
            
            // Update particles
            for(let i=G.particles.length-1;i>=0;i--){{
                const p=G.particles[i];
                p.x+=p.vx;p.y+=p.vy;
                p.vx*=0.97;p.vy*=0.97;
                p.life--;
                if(p.life<=0)G.particles.splice(i,1);
            }}
            
            // Update UI
            document.getElementById('waveDisplay').textContent='🌊 '+G.wave;
            document.getElementById('enemyCount').textContent='👾 '+G.enemies.length;
        }}
        
        // Draw
        function draw() {{
            const grad=ctx.createRadialGradient(450,300,100,450,300,500);
            grad.addColorStop(0,'{bg1}');grad.addColorStop(1,'{bg0}');
            ctx.fillStyle=grad;ctx.fillRect(0,0,900,600);
            
            // Grid
            ctx.strokeStyle='rgba(255,255,255,0.03)';ctx.lineWidth=1;
            for(let i=0;i<900;i+=50){{ctx.beginPath();ctx.moveTo(i,0);ctx.lineTo(i,600);ctx.stroke();ctx.beginPath();ctx.moveTo(0,i);ctx.lineTo(900,i);ctx.stroke();}}
            
            // Powerups
            G.powerups.forEach(pw=>{{
                ctx.fillStyle=pw.type==='health'?'#ff4444':pw.type==='shield'?'#4ecdc4':'#ffd93d';
                ctx.shadowColor=ctx.fillStyle;ctx.shadowBlur=15;
                ctx.beginPath();ctx.arc(pw.x,pw.y,pw.size/2,0,Math.PI*2);ctx.fill();
                ctx.shadowBlur=0;
                ctx.fillStyle='#fff';ctx.font='12px monospace';
                ctx.fillText(pw.type==='health'?'❤️':pw.type==='shield'?'🛡️':'⭐',pw.x-8,pw.y-8);
            }});
            
            // Enemies
            G.enemies.forEach(e=>{{
                const grad2=ctx.createRadialGradient(e.x-5,e.y-5,5,e.x,e.y,e.size);
                grad2.addColorStop(0,e.type==='boss'?'#ff0044':C.s);
                grad2.addColorStop(1,e.type==='boss'?'#cc0033':'#cc4444');
                ctx.fillStyle=grad2;
                ctx.shadowColor=e.type==='boss'?'#ff0000':C.s;
                ctx.shadowBlur=e.type==='boss'?30:10;
                ctx.beginPath();ctx.arc(e.x,e.y,e.size/2,0,Math.PI*2);ctx.fill();
                ctx.shadowBlur=0;
                
                // Health bar
                const w=e.type==='boss'?80:e.size;
                ctx.fillStyle='#444';
                ctx.fillRect(e.x-w/2,e.y-e.size/2-10,w,4);
                ctx.fillStyle=e.type==='boss'?'#ff0044':'#4ecdc4';
                ctx.fillRect(e.x-w/2,e.y-e.size/2-10,w*(e.hp/e.maxHp),4);
                
                ctx.fillStyle='#fff';
                ctx.font=e.type==='boss'?'30px monospace':'18px monospace';
                ctx.fillText(e.type==='boss'?'👹':'👾',e.x-12,e.y-8);
                if(e.type==='boss'){{
                    ctx.fillStyle='#ff0044';ctx.font='bold 14px monospace';
                    ctx.fillText('BOSS',e.x-20,e.y-e.size/2-18);
                }}
            }});
            
            // Player
            const grad3=ctx.createRadialGradient(G.p.x-8,G.p.y-8,5,G.p.x,G.p.y,G.p.size);
            grad3.addColorStop(0,G.shieldActive?'#4ecdc4':C.p);
            grad3.addColorStop(1,G.shieldActive?'#2a9d8f':'#2a7d8f');
            ctx.fillStyle=grad3;
            ctx.shadowColor=G.shieldActive?'#4ecdc4':C.p;
            ctx.shadowBlur=G.shieldActive?40:20;
            ctx.beginPath();ctx.arc(G.p.x,G.p.y,G.p.size/2,0,Math.PI*2);ctx.fill();
            ctx.shadowBlur=0;
            if(G.shieldActive){{
                ctx.strokeStyle=C.p;ctx.lineWidth=3;ctx.shadowColor=C.p;ctx.shadowBlur=30;
                ctx.beginPath();ctx.arc(G.p.x,G.p.y,G.p.size/2+8,0,Math.PI*2);ctx.stroke();
                ctx.shadowBlur=0;
            }}
            ctx.fillStyle='#fff';ctx.font='22px monospace';
            ctx.fillText('🎮',G.p.x-14,G.p.y-10);
            
            // Particles
            G.particles.forEach(p=>{{
                const a=p.life/p.maxLife;
                ctx.globalAlpha=a;ctx.fillStyle=p.color;
                ctx.shadowColor=p.color;ctx.shadowBlur=8;
                ctx.beginPath();ctx.arc(p.x,p.y,p.size*a,0,Math.PI*2);ctx.fill();
                ctx.shadowBlur=0;ctx.globalAlpha=1;
            }});
            
            // UI
            ctx.shadowBlur=0;
            ctx.fillStyle='#fff';ctx.font='bold 22px monospace';
            ctx.fillText('SCORE: '+G.score,20,40);
            ctx.fillStyle='#ff4444';ctx.fillRect(20,55,200,12);
            ctx.fillStyle=C.p;ctx.fillRect(20,55,(G.p.h/G.p.mh)*200,12);
            ctx.fillStyle='#fff';ctx.font='10px monospace';
            ctx.fillText('HP: '+Math.round(G.p.h)+'/'+G.p.mh,25,67);
            
            if(G.combo>0){{
                ctx.fillStyle=C.a;ctx.font='bold 16px monospace';
                ctx.fillText('⚡ '+G.combo+'x',20,110);
            }}
            if(G.cd>0){{
                ctx.fillStyle='rgba(255,255,255,0.2)';
                ctx.fillRect(20,130,G.cd*2,6);
            }}
            ctx.fillStyle='#888';ctx.font='11px monospace';
            ctx.fillText('⚡ '+G.cd+'/'+G.maxCd,20,148);
            
            // Game Over
            if(G.gameOver){{
                ctx.fillStyle='rgba(0,0,0,0.75)';ctx.fillRect(0,0,900,600);
                ctx.fillStyle='#fff';ctx.font='bold 48px monospace';ctx.textAlign='center';
                ctx.fillText('GAME OVER',450,230);
                ctx.font='24px monospace';ctx.fillStyle=C.a;
                ctx.fillText('Score: '+G.score,450,290);
                ctx.font='18px monospace';ctx.fillStyle='#aaa';
                ctx.fillText('Wave: '+G.wave+' • Combo: '+G.maxCombo,450,340);
                ctx.font='16px monospace';ctx.fillStyle='#888';
                ctx.fillText('Press R to restart',450,400);
                ctx.textAlign='left';
            }}
            
            // Start
            if(!G.started&&!G.gameOver){{
                ctx.fillStyle='rgba(0,0,0,0.6)';ctx.fillRect(0,0,900,600);
                ctx.fillStyle='#fff';ctx.font='bold 40px monospace';ctx.textAlign='center';
                ctx.fillText('🎮 {name}',450,220);
                ctx.font='18px monospace';ctx.fillStyle=C.p;
                ctx.fillText('Genre: {genre}',450,270);
                ctx.font='16px monospace';ctx.fillStyle=C.s;
                ctx.fillText('Mechanic: {mechanic}',450,305);
                ctx.font='16px monospace';ctx.fillStyle=C.a;
                ctx.fillText('"{hook}"',450,345);
                ctx.font='18px monospace';ctx.fillStyle='#fff';
                ctx.fillText('Press SPACE / Tap to Start',450,400);
                ctx.textAlign='left';
            }}
        }}
        
        function loop(){{update();draw();requestAnimationFrame(loop);}}
        
        // Controls
        document.addEventListener('keydown',function(e){{
            const k=e.key.toLowerCase();keys[k]=true;
            if(e.key===' '){{e.preventDefault();
                if(!G.started){{G.started=true;G.spawnTimer=30;}}
                else useMechanic();
            }}
            if((e.key==='r'||e.key==='R')&&G.gameOver){{
                Object.assign(G,{{
                    p:{{x:450,y:300,size:22,h:{hp},mh:{hp}}},
                    enemies:[],particles:[],powerups:[],bullets:[],
                    score:0,combo:0,maxCombo:0,wave:1,enemiesKilled:0,
                    gameOver:false,started:true,cd:0,maxCd:90,
                    bossActive:false,shieldActive:false,shieldTimer:0,
                    spawnTimer:30,difficulty:1
                }});
            }}
        }});
        document.addEventListener('keyup',function(e){{keys[e.key.toLowerCase()]=false;}});
        
        // Click to start
        c.addEventListener('click',function(){{
            if(!G.started&&!G.gameOver){{G.started=true;G.spawnTimer=30;}}
        }});
        c.addEventListener('touchstart',function(e){{
            e.preventDefault();
            if(!G.started&&!G.gameOver){{G.started=true;G.spawnTimer=30;}}
        }});
        
        loop();
    </script>
</body>
</html>'''

# ============================================================================
# MAIN BOT
# ============================================================================

class DeathRollStudio:
    def __init__(self):
        self.ai = AIService(OPENAI_KEY)
        self.design = GameDesignSystem(self.ai)
        self.portfolio = Portfolio()
        self.telegram = Telegram(TELEGRAM_TOKEN)
    
    def run(self):
        print("\n" + "═" * 60)
        print("🎮 GENERATING NEW GAME")
        print("═" * 60)
        
        # 1. Design
        game = self.design.generate()
        print(f"   📝 Name: {game['name']}")
        print(f"   🎭 Genre: {game['genre']}")
        print(f"   ⚡ Mechanic: {game['mechanic']}")
        print(f"   🎨 Style: {game['visual_style']}")
        
        # 2. Price
        price = self._price(game)
        game["price"] = price
        print(f"   💰 Price: ${price} SOL")
        
        # 3. Description
        if "description" not in game:
            game["description"] = self.ai.generate_description(game)
        print(f"   📝 {game['description'][:80]}...")
        
        # 4. License
        license_key = generate_license(game["name"])
        print(f"   🔑 License: {license_key}")
        
        # 5. Art
        ArtDirector.generate(game["name"], game["genre"], game["visual_style"])
        print(f"   🎨 Art: Generated")
        
        # 6. Build game
        html5_url = self._build(game, license_key)
        print(f"   🌐 HTML5: {html5_url}")
        
        # 7. Portfolio
        entry = {
            "date": datetime.now().isoformat(),
            "game": game["name"],
            "genre": game["genre"],
            "mechanic": game["mechanic"],
            "description": game["description"],
            "hook": game["hook"],
            "visual_style": game["visual_style"],
            "game_mode": game["game_mode"],
            "price": price,
            "license_key": license_key,
            "html5_url": html5_url,
            "version": BOT_VERSION
        }
        total = self.portfolio.add(entry)
        print(f"   📊 Portfolio: {total} games")
        
        # 8. Telegram - FIXED
        print(f"   📱 Sending to Telegram...")
        if self.telegram.enabled:
            self._send_telegram(game, license_key, html5_url)
        else:
            print("   ⚠️ Telegram token missing")
        
        # 9. SAR
        self._update_sar(game)
        print(f"   🧠 SAR: Updated")
        
        # 10. Done
        print("\n" + "═" * 60)
        print("✅ GAME COMPLETE")
        print("═" * 60)
        print(f"   Game: {game['name']}")
        print(f"   License: {license_key}")
        print(f"   HTML5: {html5_url}")
        print(f"   Portfolio: {total} games")
        print("═" * 60)
    
    def _price(self, game: Dict) -> int:
        base = 3
        if game["visual_style"] in ["neon", "pixel"]:
            base += 1
        if game["difficulty"] == "hard":
            base += 2
        elif game["difficulty"] == "medium":
            base += 1
        if game["game_mode"] == "boss_fight":
            base += 2
        return min(max(base, CONFIG["price"]["min"]), CONFIG["price"]["max"])
    
    def _build(self, game: Dict, license_key: str) -> str:
        theme = GameDesignSystem.THEMES.get(game["visual_style"], GameDesignSystem.THEMES["neon"])
        style = GameDesignSystem.STYLES.get(game["game_style"], GameDesignSystem.STYLES["survival"])
        
        folder = Path(f"workspace/{game['name'].replace(' ', '_')}")
        folder.mkdir(parents=True, exist_ok=True)
        
        sprite = Path("sprite.png")
        if sprite.exists():
            shutil.copy(sprite, folder / "icon.png")
        
        html = generate_html5(game, theme, style)
        (folder / "index.html").write_text(html)
        
        (folder / "LICENSE.txt").write_text(f"""
DEATHROLL STUDIO LICENSE
Game: {game['name']}
License: {license_key}
Price: {game['price']} SOL
Date: {datetime.now().strftime('%Y-%m-%d')}
""")
        
        zip_path = Path("workspace/latest_game.zip")
        try:
            if zip_path.exists():
                zip_path.unlink()
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
                for f in folder.rglob("*"):
                    if f.is_file():
                        z.write(f, f.relative_to(folder.parent))
        except:
            pass
        
        return f"https://{CONFIG['brand']['github']}.github.io/FACTORY-BOT-V4/workspace/{game['name'].replace(' ', '_')}/index.html"
    
    def _send_telegram(self, game: Dict, license_key: str, html5_url: str):
        """Send game post - short and clean"""
        
        channel = CONFIG["telegram"]["channel"]
        sprite = Path("sprite.png")
        
        # Short, clean post (no Markdown issues)
        post = f"""🎮 {game['name']} — {game['genre']}
⚡ {game['mechanic']}

{game['description'][:120]}

🌐 Play FREE: {html5_url}

💰 Full Game: ${game['price']} SOL
🔑 License: {license_key}

Send ${game['price']} SOL + @username to:
Trust: {CONFIG['wallets']['trust']}
Phantom: {CONFIG['wallets']['phantom']}

#gamedev #{game['genre'].replace(' ', '')} #DeathRollStudio"""
        
        # Send to channel
        if channel:
            print(f"   📢 Channel: {channel}")
            if sprite.exists():
                self.telegram.send_photo(channel, sprite, post)
            else:
                self.telegram.send_message(channel, post)
        
        # Send to admin DM
        if TELEGRAM_CHAT_ID:
            print(f"   📨 Admin DM: {TELEGRAM_CHAT_ID}")
            if sprite.exists():
                self.telegram.send_photo(TELEGRAM_CHAT_ID, sprite, post)
            else:
                self.telegram.send_message(TELEGRAM_CHAT_ID, post)
            
            zip_path = Path("workspace/latest_game.zip")
            if zip_path.exists():
                self.telegram.send_document(
                    TELEGRAM_CHAT_ID,
                    zip_path,
                    f"🎮 {game['name']}\n🔑 {license_key}"
                )
                print(f"   ✅ ZIP sent")
    
    def _update_sar(self, game: Dict):
        path = Path("sar_analysis.json")
        if path.exists():
            try:
                data = json.loads(path.read_text())
            except:
                data = {"study": {"games": []}, "analysis": {}}
        else:
            data = {"study": {"games": []}, "analysis": {}}
        
        data["study"]["games"].append({
            "name": game["name"],
            "genre": game["genre"],
            "mechanic": game["mechanic"],
            "timestamp": datetime.now().isoformat(),
            "price": game["price"]
        })
        data["study"]["games"] = data["study"]["games"][-100:]
        
        genre_counts = {}
        for g in data["study"]["games"]:
            genre = g.get("genre")
            if genre:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
        if genre_counts:
            data["analysis"]["best_genre"] = max(genre_counts, key=genre_counts.get)
        
        path.write_text(json.dumps(data, indent=2))

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    bot = DeathRollStudio()
    bot.run()
