#!/usr/bin/env python3
"""
DEATHROLL STUDIO v33.0 - TELEGRAM FIXED + MOBILE TOUCH
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

BOT_VERSION = "33.0.0"

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
print("🔥 DEATHROLL STUDIO v33.0 - MOBILE + TELEGRAM FIXED")
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
# TELEGRAM SERVICE - FIXED
# ============================================================================

class Telegram:
    def __init__(self, token: Optional[str]):
        self.token = token
        self.enabled = bool(token)
    
    def send_photo(self, chat_id: str, photo: Path, caption: str) -> bool:
        if not self.enabled:
            return False
        try:
            with open(photo, "rb") as f:
                r = requests.post(
                    f"https://api.telegram.org/bot{self.token}/sendPhoto",
                    files={"photo": f},
                    data={"chat_id": chat_id, "caption": caption, "parse_mode": "Markdown"},
                    timeout=60
                )
            if r.status_code == 200:
                print(f"   ✅ Photo sent to {chat_id}")
                return True
            else:
                print(f"   ⚠️ Photo failed: {r.status_code}")
                return False
        except Exception as e:
            print(f"   ⚠️ Photo error: {e}")
            return False
    
    def send_message(self, chat_id: str, text: str) -> bool:
        if not self.enabled:
            return False
        try:
            r = requests.post(
                f"https://api.telegram.org/bot{self.token}/sendMessage",
                json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
                timeout=30
            )
            if r.status_code == 200:
                print(f"   ✅ Message sent to {chat_id}")
                return True
            else:
                print(f"   ⚠️ Message failed: {r.status_code}")
                return False
        except Exception as e:
            print(f"   ⚠️ Message error: {e}")
            return False
    
    def send_document(self, chat_id: str, doc: Path, caption: str) -> bool:
        if not self.enabled:
            return False
        try:
            with open(doc, "rb") as f:
                r = requests.post(
                    f"https://api.telegram.org/bot{self.token}/sendDocument",
                    files={"document": f},
                    data={"chat_id": chat_id, "caption": caption, "parse_mode": "Markdown"},
                    timeout=60
                )
            return r.status_code == 200
        except:
            return False

# ============================================================================
# HTML5 GAME GENERATOR - WITH TOUCH CONTROLS
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
        .wrapper {{ text-align:center; padding:10px; max-width:100%; }}
        .title {{
            font-size:1.5rem;
            color:{p};
            text-shadow: {'0 0 20px ' + p if theme['glow'] else 'none'};
            font-weight:bold;
        }}
        .genre {{ color:{s}; font-size:0.8rem; }}
        .mechanic {{ color:{a}; font-size:0.75rem; margin-top:3px; }}
        .canvas-wrapper {{
            position:relative;
            display:inline-block;
            width:100%;
            max-width:700px;
            margin:5px auto;
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
        /* Touch Controls */
        .touch-controls {{
            position:relative;
            width:100%;
            max-width:700px;
            margin:5px auto 0;
            display:flex;
            justify-content:space-between;
            align-items:center;
            padding:5px 10px;
            touch-action:none;
        }}
        .touch-joystick {{
            width:120px;
            height:120px;
            border-radius:50%;
            background:rgba(255,255,255,0.1);
            border:2px solid {p}44;
            position:relative;
            touch-action:none;
        }}
        .touch-joystick-inner {{
            width:50px;
            height:50px;
            border-radius:50%;
            background:{p};
            position:absolute;
            top:35px;
            left:35px;
            touch-action:none;
            box-shadow: 0 0 20px {p}44;
        }}
        .touch-btn {{
            width:70px;
            height:70px;
            border-radius:50%;
            background:{p}33;
            border:2px solid {p};
            color:#fff;
            font-size:0.7rem;
            font-weight:bold;
            display:flex;
            align-items:center;
            justify-content:center;
            touch-action:none;
            box-shadow: 0 0 20px {p}44;
            text-align:center;
            line-height:1.2;
            padding:5px;
        }}
        .touch-btn:active {{
            background:{p}66;
            transform:scale(0.95);
        }}
        .controls {{
            margin-top:5px;
            color:#888;
            font-size:0.7rem;
        }}
        .controls span {{
            display:inline-block;
            background:rgba(255,255,255,0.1);
            padding:2px 8px;
            border-radius:20px;
            margin:0 2px;
        }}
        @media (max-width:600px) {{
            .title {{ font-size:1.2rem; }}
            .touch-joystick {{ width:80px; height:80px; }}
            .touch-joystick-inner {{ width:35px; height:35px; top:22.5px; left:22.5px; }}
            .touch-btn {{ width:55px; height:55px; font-size:0.6rem; }}
        }}
        @media (max-width:400px) {{
            .touch-joystick {{ width:60px; height:60px; }}
            .touch-joystick-inner {{ width:25px; height:25px; top:17.5px; left:17.5px; }}
            .touch-btn {{ width:45px; height:45px; font-size:0.5rem; }}
        }}
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="title">{name}</div>
        <div class="genre">{genre}</div>
        <div class="mechanic">⚡ {mechanic}</div>
        <div class="canvas-wrapper">
            <canvas id="c" width="900" height="600"></canvas>
        </div>
        <div class="touch-controls">
            <div class="touch-joystick" id="joystick">
                <div class="touch-joystick-inner" id="joystickInner"></div>
            </div>
            <div class="touch-btn" id="mechanicBtn">⚡<br>{mechanic[:8]}</div>
        </div>
        <div class="controls"><span>WASD</span> or <span>←→↑↓</span> move | <span>SPACE</span> {mechanic}</div>
    </div>
    <script>
        const c=document.getElementById('c'),ctx=c.getContext('2d');
        const C={{p:'{p}',s:'{s}',a:'{a}',g:{glow}}};
        const state={{p:{{x:450,y:300,size:25,h:{hp},mh:{hp}}},e:[],parts:[],score:0,combo:0,go:false,started:false,cd:0,maxCd:90}};
        let keys={{}},touchX=0,touchY=0,touchActive=false;
        
        // Joystick
        const joystick=document.getElementById('joystick');
        const joystickInner=document.getElementById('joystickInner');
        let jActive=false,jX=0,jY=0;
        
        joystick.addEventListener('touchstart',function(e){{e.preventDefault();jActive=true;const r=this.getBoundingClientRect();const t=e.touches[0];jX=(t.clientX-r.left-40)/40;jY=(t.clientY-r.top-40)/40;updateJoystick();}});
        joystick.addEventListener('touchmove',function(e){{e.preventDefault();if(!jActive)return;const r=this.getBoundingClientRect();const t=e.touches[0];jX=(t.clientX-r.left-40)/40;jY=(t.clientY-r.top-40)/40;updateJoystick();}});
        joystick.addEventListener('touchend',function(e){{e.preventDefault();jActive=false;jX=0;jY=0;updateJoystick();}});
        
        function updateJoystick(){{const max=1;let x=Math.max(-max,Math.min(max,jX));let y=Math.max(-max,Math.min(max,jY));const d=Math.hypot(x,y);if(d>max){{x/=d;y/=d;}}jX=x;jY=y;joystickInner.style.transform=`translate(${{jX*20}}px,${{jY*20}}px)`;}}
        
        // Mechanic button
        document.getElementById('mechanicBtn').addEventListener('touchstart',function(e){{e.preventDefault();simulateKey(' ');}});
        document.getElementById('mechanicBtn').addEventListener('mousedown',function(e){{simulateKey(' ');}});
        
        function simulateKey(k){{const ev=new KeyboardEvent('keydown',{{key:k,code:k===' '?'Space':k}});document.dispatchEvent(ev);setTimeout(()=>{{const up=new KeyboardEvent('keyup',{{key:k,code:k===' '?'Space':k}});document.dispatchEvent(up);}},200);}}
        
        function spawn(){{const x=Math.random()*880+10,y=Math.random()*580+10;state.e.push({{x,y,size:25,hp:3,mh:3,speed:{speed}}});}}
        function useM(){{if(state.cd>0)return;state.cd=state.maxCd;state.e.forEach(e=>{{const dx=e.x-state.p.x,dy=e.y-state.p.y,d=Math.hypot(dx,dy);if(d<150){{const a=Math.atan2(dy,dx);e.x+=Math.cos(a)*80;e.y+=Math.sin(a)*80;e.hp-=2;}}}});addP(state.p.x,state.p.y,C.p,20);}}
        function addP(x,y,color,c){{for(let i=0;i<c;i++)state.parts.push({{x:x+(Math.random()-0.5)*20,y:y+(Math.random()-0.5)*20,vx:(Math.random()-0.5)*6,vy:(Math.random()-0.5)*6,life:30+Math.random()*20,maxLife:50,color,size:3+Math.random()*4}});}}
        
        function update(){{if(state.go||!state.started)return;let dx=0,dy=0,s=4.5;
        // Keyboard
        if(keys['w']||keys['ArrowUp'])dy=-s;if(keys['s']||keys['ArrowDown'])dy=s;if(keys['a']||keys['ArrowLeft'])dx=-s;if(keys['d']||keys['ArrowRight'])dx=s;
        // Touch
        if(jActive){{dx+=jX*s*0.7;dy+=jY*s*0.7;}}
        if(dx&&dy){{dx*=0.707;dy*=0.707;}}
        state.p.x=Math.max(20,Math.min(880,state.p.x+dx));state.p.y=Math.max(20,Math.min(580,state.p.y+dy));
        if(state.cd>0)state.cd--;if(Math.random()<0.02*{spawn})spawn();
        for(let i=0;i<state.e.length;i++){{const e=state.e[i],dx2=state.p.x-e.x,dy2=state.p.y-e.y,d=Math.hypot(dx2,dy2);if(d>0){{e.x+=(dx2/d)*e.speed;e.y+=(dy2/d)*e.speed;}}e.x=Math.max(10,Math.min(890,e.x));e.y=Math.max(10,Math.min(590,e.y));const cd=Math.hypot(state.p.x-e.x,state.p.y-e.y);if(cd<state.p.size/2+e.size/2){{state.p.h-=10;state.combo=0;if(state.p.h<=0){{state.p.h=0;state.go=true;return;}}}}if(e.hp<=0){{state.score+=10*(1+Math.floor(state.combo/10));state.combo++;addP(e.x,e.y,C.s,15);state.e.splice(i,1);i--;}}}}
        for(let i=0;i<state.parts.length;i++){{const p=state.parts[i];p.x+=p.vx;p.y+=p.vy;p.vx*=0.98;p.vy*=0.98;p.life--;if(p.life<=0){{state.parts.splice(i,1);i--;}}}}}}
        
        function draw(){{const g=ctx.createRadialGradient(450,300,100,450,300,500);g.addColorStop(0,'{bg1}');g.addColorStop(1,'{bg0}');ctx.fillStyle=g;ctx.fillRect(0,0,900,600);ctx.strokeStyle='rgba(255,255,255,0.03)';ctx.lineWidth=1;for(let i=0;i<900;i+=50){{ctx.beginPath();ctx.moveTo(i,0);ctx.lineTo(i,600);ctx.stroke();ctx.beginPath();ctx.moveTo(0,i);ctx.lineTo(900,i);ctx.stroke();}}
        state.e.forEach(e=>{{const g2=ctx.createRadialGradient(e.x-5,e.y-5,5,e.x,e.y,e.size);g2.addColorStop(0,C.s);g2.addColorStop(1,'#cc4444');ctx.fillStyle=g2;ctx.shadowColor=C.s;ctx.shadowBlur=10;ctx.beginPath();ctx.arc(e.x,e.y,e.size/2,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;const w=e.size;ctx.fillStyle='#444';ctx.fillRect(e.x-w/2,e.y-e.size/2-10,w,4);ctx.fillStyle='#4ecdc4';ctx.fillRect(e.x-w/2,e.y-e.size/2-10,w*(e.hp/e.mh),4);ctx.fillStyle='#fff';ctx.font='18px monospace';ctx.fillText('👾',e.x-12,e.y-8);}});
        const g3=ctx.createRadialGradient(state.p.x-8,state.p.y-8,5,state.p.x,state.p.y,state.p.size);g3.addColorStop(0,C.p);g3.addColorStop(1,'#2a7d8f');ctx.fillStyle=g3;ctx.shadowColor=C.p;ctx.shadowBlur=20;ctx.beginPath();ctx.arc(state.p.x,state.p.y,state.p.size/2,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;ctx.fillStyle='#fff';ctx.font='24px monospace';ctx.fillText('🎮',state.p.x-15,state.p.y-12);
        state.parts.forEach(p=>{{const a=p.life/p.maxLife;ctx.globalAlpha=a;ctx.fillStyle=p.color;ctx.shadowColor=p.color;ctx.shadowBlur=8;ctx.beginPath();ctx.arc(p.x,p.y,p.size*a,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;ctx.globalAlpha=1;}});
        ctx.shadowBlur=0;ctx.fillStyle='#fff';ctx.font='bold 22px monospace';ctx.fillText('SCORE: '+state.score,20,45);ctx.fillStyle='#ff4444';ctx.fillRect(20,65,200,14);ctx.fillStyle=C.p;ctx.fillRect(20,65,(state.p.h/state.p.mh)*200,14);
        if(state.combo>0){{ctx.fillStyle=C.a;ctx.font='bold 18px monospace';ctx.fillText('⚡ '+state.combo+'x COMBO!',20,120);}}
        if(state.cd>0){{ctx.fillStyle='rgba(255,255,255,0.2)';ctx.fillRect(20,150,state.cd*2,6);}}ctx.fillStyle='#888';ctx.font='12px monospace';ctx.fillText('⚡ {mechanic} (SPACE)',20,165);
        if(state.go){{ctx.fillStyle='rgba(0,0,0,0.7)';ctx.fillRect(0,0,900,600);ctx.fillStyle='#fff';ctx.font='bold 48px monospace';ctx.textAlign='center';ctx.fillText('GAME OVER',450,250);ctx.font='24px monospace';ctx.fillStyle=C.a;ctx.fillText('Score: '+state.score,450,320);ctx.font='16px monospace';ctx.fillStyle='#aaa';ctx.fillText('Press R to restart',450,370);ctx.textAlign='left';}}
        if(!state.started&&!state.go){{ctx.fillStyle='rgba(0,0,0,0.5)';ctx.fillRect(0,0,900,600);ctx.fillStyle='#fff';ctx.font='bold 36px monospace';ctx.textAlign='center';ctx.fillText('🎮 {name}',450,230);ctx.font='18px monospace';ctx.fillStyle=C.p;ctx.fillText('Press SPACE to start',450,320);ctx.textAlign='left';}}}}
        
        function loop(){{update();draw();requestAnimationFrame(loop);}}
        
        document.addEventListener('keydown',function(e){{const k=e.key.toLowerCase();keys[k]=true;if(e.key===' '){{e.preventDefault();if(!state.started){{state.started=true;for(let i=0;i<5;i++)spawn();}}else{{useM();}}}}if((e.key==='r'||e.key==='R')&&state.go){{state.p={{x:450,y:300,size:25,h:{hp},mh:{hp}}};state.e=[];state.parts=[];state.score=0;state.combo=0;state.go=false;state.cd=0;for(let i=0;i<5;i++)spawn();}}}});
        document.addEventListener('keyup',function(e){{keys[e.key.toLowerCase()]=false;}});
        
        // Click/tap to start
        c.addEventListener('click',function(){{if(!state.started&&!state.go){{state.started=true;for(let i=0;i<5;i++)spawn();}}}});
        c.addEventListener('touchstart',function(e){{e.preventDefault();if(!state.started&&!state.go){{state.started=true;for(let i=0;i<5;i++)spawn();}}}});
        
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
            self._send_telegram_fixed(game, license_key, html5_url)
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
    
    def _send_telegram_fixed(self, game: Dict, license_key: str, html5_url: str):
        """FIXED: Send proper game post to channel and DM"""
        
        channel = CONFIG["telegram"]["channel"]
        sprite = Path("sprite.png")
        
        # Build the game post
        post = f"""
🎮 *{game['name']}* — {game['genre']}
⚡ *Mechanic:* `{game['mechanic']}`

{game['description']}

🌐 *Play FREE:* {html5_url}

━━━━━━━━━━━━━━━━━━━━━
💰 *Full Game:* ${game['price']} SOL

🔵 *Trust Wallet:*
`{CONFIG['wallets']['trust']}`

🟣 *Phantom Wallet:*
`{CONFIG['wallets']['phantom']}`

📩 Send ${game['price']} SOL + @username → receive full game + license key

🔑 *License:* `{license_key}`

#gamedev #indiegame #{game['genre'].replace(' ', '')} #DeathRollStudio
"""
        
        # Send to channel
        if channel:
            print(f"   📢 Sending to channel: {channel}")
            if sprite.exists():
                sent = self.telegram.send_photo(channel, sprite, post)
                if not sent:
                    self.telegram.send_message(channel, post)
            else:
                self.telegram.send_message(channel, post)
            print(f"   ✅ Channel post sent")
        
        # Send to admin DM
        if TELEGRAM_CHAT_ID:
            print(f"   📨 Sending to admin DM: {TELEGRAM_CHAT_ID}")
            if sprite.exists():
                sent = self.telegram.send_photo(TELEGRAM_CHAT_ID, sprite, post)
                if not sent:
                    self.telegram.send_message(TELEGRAM_CHAT_ID, post)
            else:
                self.telegram.send_message(TELEGRAM_CHAT_ID, post)
            print(f"   ✅ DM sent")
            
            # Send ZIP
            zip_path = Path("workspace/latest_game.zip")
            if zip_path.exists():
                self.telegram.send_document(
                    TELEGRAM_CHAT_ID,
                    zip_path,
                    f"🎮 {game['name']}\n🔑 {license_key}\n🌐 {html5_url}"
                )
                print(f"   ✅ ZIP sent to DM")
    
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
