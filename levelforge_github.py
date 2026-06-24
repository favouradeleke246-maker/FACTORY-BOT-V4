#!/usr/bin/env python3
"""
DEATHROLL STUDIO v50.0 – COMPLETE PRODUCTION GAME ENGINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os, json, random, requests, time, shutil, zipfile, uuid, math
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw
from typing import Dict, List, Optional

# ============================================================
# CONFIG
# ============================================================
BOT_VERSION = "50.0.0"
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

print("═"*60); print("🔥 DEATHROLL STUDIO v50.0 – COMPLETE PRODUCTION ENGINE")
print(f"🤖 Version: {BOT_VERSION}") ; print(f"✅ Telegram: {'✅' if TELEGRAM_TOKEN else '❌'}")
print(f"✅ OpenAI: {'✅' if OPENAI_KEY else '❌'}") ; print(f"✅ GitHub: {'✅' if GITHUB_TOKEN else '❌'}")
print("═"*60)

# ============================================================
# AI SERVICE
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
Avoid mechanics: {', '.join(recent_m[:3]) if recent_m else 'none'}
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
# TEMPLATE SELECTOR
# ============================================================
def _select_template(genre):
    g = genre.lower()
    if "shooter" in g or "action" in g: return "shooter"
    if "platform" in g: return "platformer"
    if "puzzle" in g or "match" in g: return "puzzle"
    if "racing" in g or "driving" in g: return "racer"
    if "horror" in g or "survival" in g: return "horror"
    if "strategy" in g or "tower" in g or "defense" in g: return "strategy"
    if "rogue" in g or "dungeon" in g: return "roguelike"
    return "shooter"

# ============================================================
# ART DIRECTOR – creates genre-appropriate sprites
# ============================================================
class ArtDirector:
    @staticmethod
    def generate_all_assets(game_name, genre, style, template, folder: Path):
        assets = folder / "assets"
        assets.mkdir(exist_ok=True)

        # Try to use AI-generated sprite, otherwise create one
        main_sprite = Path("sprite.png")
        if main_sprite.exists() and main_sprite.stat().st_size > 100:
            shutil.copy(main_sprite, assets / "player.png")
        else:
            ArtDirector._create_player_sprite(assets / "player.png", template)

        ArtDirector._create_enemy_sprite(assets / "enemy.png", template)
        ArtDirector._create_coin_sprite(assets / "coin.png")
        ArtDirector._create_powerup_sprite(assets / "powerup.png", template)
        bg = ArtDirector._create_background(template)
        bg.save(assets / "bg.png")
        print(f"   🎨 Assets generated in {assets}")

    @staticmethod
    def _create_player_sprite(path, template):
        img = Image.new('RGBA', (64, 64), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        if template == "shooter":
            draw.polygon([(32, 2), (60, 62), (32, 48), (4, 62)], fill=(78,205,196))
            draw.polygon([(32, 8), (48, 56), (32, 44), (16, 56)], fill=(255,255,255))
        elif template == "platformer":
            draw.ellipse([12, 8, 52, 48], fill=(255,107,107))
            draw.rectangle([20, 40, 44, 64], fill=(255,107,107))
            draw.ellipse([20, 2, 44, 18], fill=(255,215,0))
        elif template == "racer":
            draw.rectangle([8, 20, 56, 60], fill=(255,68,68))
            draw.ellipse([12, 52, 28, 64], fill=(0,0,0))
            draw.ellipse([36, 52, 52, 64], fill=(0,0,0))
            draw.rectangle([20, 8, 44, 20], fill=(200,200,200))
        elif template == "horror":
            draw.ellipse([8, 8, 56, 56], fill=(139,0,0))
            draw.ellipse([20, 20, 28, 30], fill=(255,255,255))
            draw.ellipse([36, 20, 44, 30], fill=(255,255,255))
            draw.ellipse([24, 24, 26, 26], fill=(0,0,0))
            draw.ellipse([38, 24, 40, 26], fill=(0,0,0))
        elif template == "roguelike":
            draw.rectangle([12, 12, 52, 52], fill=(128,128,128))
            draw.rectangle([16, 16, 48, 48], fill=(200,200,200))
            draw.rectangle([24, 8, 40, 16], fill=(150,150,150))
            draw.polygon([(24, 8), (40, 8), (32, 0)], fill=(255,215,0))
        else:
            draw.ellipse([8, 8, 56, 56], fill=(78,205,196))
        img.save(path)

    @staticmethod
    def _create_enemy_sprite(path, template):
        img = Image.new('RGBA', (64, 64), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        if template == "shooter":
            draw.polygon([(32, 0), (64, 48), (32, 32), (0, 48)], fill=(255,68,68))
        elif template == "horror":
            draw.ellipse([8, 8, 56, 56], fill=(0,0,0))
            draw.ellipse([16, 16, 24, 24], fill=(255,0,0))
            draw.ellipse([40, 16, 48, 24], fill=(255,0,0))
        else:
            draw.ellipse([8, 8, 56, 56], fill=(255,68,68))
        img.save(path)

    @staticmethod
    def _create_coin_sprite(path):
        img = Image.new('RGBA', (32, 32), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([4, 4, 28, 28], fill=(255,215,0))
        draw.ellipse([12, 12, 20, 20], fill=(255,255,0))
        img.save(path)

    @staticmethod
    def _create_powerup_sprite(path, template):
        img = Image.new('RGBA', (32, 32), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([4, 4, 28, 28], fill=(0,255,136))
        draw.text((8, 4), "⚡", fill=(255,255,255), font=None)
        img.save(path)

    @staticmethod
    def _create_background(template):
        bg = Image.new('RGB', (800, 600), color=(20, 20, 40))
        draw = ImageDraw.Draw(bg)
        if template == "shooter":
            for _ in range(150):
                x = random.randint(0, 800); y = random.randint(0, 600)
                draw.point((x, y), fill=(255,255,255))
        elif template == "platformer":
            for i in range(0, 800, 100):
                draw.arc((i-50, 500, i+50, 600), 0, 180, fill=(50,100,50))
        elif template == "racer":
            draw.rectangle([300, 0, 500, 600], fill=(80,80,80))
            for y in range(0, 600, 60):
                draw.rectangle([390, y, 410, y+30], fill=(255,255,255))
        elif template == "horror":
            for _ in range(30):
                x = random.randint(0, 800); y = random.randint(0, 600)
                draw.polygon([(x, y), (x-20, y+40), (x+20, y+40)], fill=(30,30,30))
        elif template == "strategy":
            for x in range(0, 800, 40):
                draw.line([(x, 0), (x, 600)], fill=(40,40,40))
            for y in range(0, 600, 40):
                draw.line([(0, y), (800, y)], fill=(40,40,40))
        elif template == "roguelike":
            for x in range(0, 800, 80):
                for y in range(0, 600, 80):
                    draw.rectangle([x, y, x+80, y+80], outline=(60,60,60))
        return bg

# ============================================================
# GAME ENGINE – Complete Phaser 3 Games
# ============================================================
class GameEngine:
    @staticmethod
    def build(game_data, theme, style, template, folder: Path):
        if template == "shooter":
            js = GameEngine._shooter(game_data, theme, style)
        elif template == "platformer":
            js = GameEngine._platformer(game_data, theme, style)
        elif template == "puzzle":
            js = GameEngine._puzzle(game_data, theme, style)
        elif template == "racer":
            js = GameEngine._racer(game_data, theme, style)
        elif template == "horror":
            js = GameEngine._horror(game_data, theme, style)
        elif template == "strategy":
            js = GameEngine._strategy(game_data, theme, style)
        elif template == "roguelike":
            js = GameEngine._roguelike(game_data, theme, style)
        else:
            js = GameEngine._shooter(game_data, theme, style)

        index_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <title>{game_data['name']}</title>
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ background:#000; overflow:hidden; touch-action:none; }}
        canvas {{ display:block; margin:0 auto; }}
    </style>
</head>
<body>
    <script src="https://cdn.jsdelivr.net/npm/phaser@3.60.0/dist/phaser.min.js"></script>
    <script>
        {js}
    </script>
</body>
</html>'''
        (folder / "index.html").write_text(index_html)
        print(f"   🎮 {template.capitalize()} game built in {folder}")

    # ==================== SHOOTER ====================
    @staticmethod
    def _shooter(game_data, theme, style):
        p, s, a, bg0, bg1 = theme["primary"], theme["secondary"], theme["accent"], theme["bg"][0], theme["bg"][1]
        name, mechanic, hook, desc = game_data["name"], game_data["mechanic"], game_data["mechanic_description"], game_data["description"]
        return f'''
const config = {{
    type: Phaser.AUTO,
    width: 800, height: 600,
    physics: {{ default: 'arcade', arcade: {{ debug: false }} }},
    scene: {{
        preload: function() {{
            this.load.image('bg', 'assets/bg.png');
            this.load.image('player', 'assets/player.png');
            this.load.image('enemy', 'assets/enemy.png');
            this.load.image('coin', 'assets/coin.png');
            this.load.image('powerup', 'assets/powerup.png');
        }},
        create: function() {{
            if (this.textures.exists('bg')) this.add.image(400, 300, 'bg');
            else {{ const g = this.add.graphics(); g.fillStyle(0x1a1a2e).fillRect(0, 0, 800, 600); }}
            let player;
            if (this.textures.exists('player')) {{
                player = this.physics.add.sprite(400, 500, 'player');
            }} else {{
                player = this.add.circle(400, 500, 20, 0x4ecdc4);
                this.physics.add.existing(player);
                player.body.setCircle(20);
            }}
            player.setCollideWorldBounds(true);
            player.setScale(0.8);
            const cursors = this.input.keyboard.createCursorKeys();
            let state = {{
                score: 0, health: 100, wave: 1, enemiesDefeated: 0,
                gameOver: false, mechanicCooldown: 0,
                enemies: this.physics.add.group(),
                bullets: this.physics.add.group(),
                powerups: this.physics.add.group(),
                spawnTimer: 0, bossActive: false
            }};
            const scoreText = this.add.text(16, 16, 'Score: 0', {{ fontSize: '28px', fill: '#fff' }});
            const healthText = this.add.text(16, 56, 'HP: 100', {{ fontSize: '28px', fill: '#fff' }});
            const waveText = this.add.text(16, 96, 'Wave: 1', {{ fontSize: '28px', fill: '#fff' }});
            const mechanicText = this.add.text(16, 136, '⚡ {mechanic} (SPACE)', {{ fontSize: '20px', fill: '#ffd93d' }});

            function useMechanic() {{
                if (state.gameOver || state.mechanicCooldown > 0) return;
                state.mechanicCooldown = 120;
                state.enemies.children.iterate(e => {{
                    const dx = e.x - player.x, dy = e.y - player.y, d = Math.hypot(dx, dy);
                    if (d < 150) {{ e.x += dx * 0.5; e.y += dy * 0.5; }}
                }});
                this.cameras.main.shake(100);
                this.cameras.main.flash(100, 255, 255, 255);
            }}
            this.input.keyboard.on('keydown-SPACE', useMechanic, this);
            this.input.on('pointerdown', useMechanic, this);

            this.physics.add.overlap(state.bullets, state.enemies, (b, e) => {{
                b.destroy(); e.destroy();
                state.score += 10; state.enemiesDefeated++;
                scoreText.setText('Score: ' + state.score);
                if (state.enemiesDefeated % 10 === 0) {{
                    state.wave++;
                    waveText.setText('Wave: ' + state.wave);
                    if (state.wave % 3 === 0) {{
                        state.bossActive = true;
                        const boss = state.enemies.create(400, 50, 'enemy');
                        boss.setScale(2);
                        boss.hp = 20 + state.wave * 5;
                        boss.setVelocityX(100);
                        boss.setVelocityY(20);
                    }}
                }}
            }});
            this.physics.add.overlap(player, state.enemies, (p, e) => {{
                state.health = Math.max(0, state.health - 20);
                e.destroy();
                healthText.setText('HP: ' + state.health);
                if (state.health <= 0) {{ state.gameOver = true; showGameOver.call(this); }}
            }});
            this.physics.add.overlap(player, state.powerups, (p, pw) => {{
                pw.destroy();
                state.health = Math.min(100, state.health + 20);
                healthText.setText('HP: ' + state.health);
            }});

            function spawnEnemy() {{
                if (state.gameOver || state.bossActive) return;
                const x = Phaser.Math.Between(50, 750);
                const enemy = state.enemies.create(x, 0, 'enemy');
                enemy.setVelocityY(100 + state.wave * 20);
                enemy.setScale(0.6 + state.wave * 0.02);
            }}
            function spawnPowerup() {{
                if (state.gameOver) return;
                const x = Phaser.Math.Between(50, 750), y = Phaser.Math.Between(50, 550);
                const pw = state.powerups.create(x, y, 'powerup');
                pw.setScale(0.5);
            }}
            function shoot() {{
                if (state.gameOver) return;
                const bullet = state.bullets.create(player.x, player.y - 20, 'coin');
                bullet.setVelocityY(-400);
                bullet.setScale(0.2);
            }}
            this.input.keyboard.on('keydown-SPACE', shoot, this);
            this.input.on('pointerdown', shoot, this);

            this.time.addEvent({{ delay: 1000, callback: spawnEnemy, callbackScope: this, loop: true }});
            this.time.addEvent({{ delay: 5000, callback: spawnPowerup, callbackScope: this, loop: true }});

            function showGameOver() {{
                this.add.text(300, 250, 'GAME OVER', {{ fontSize: '64px', fill: '#ff0000' }});
                this.add.text(300, 320, 'Press R to restart', {{ fontSize: '32px', fill: '#fff' }});
                this.input.keyboard.on('keydown-R', () => {{ this.scene.restart(); }});
            }}
            this.update = function(time) {{
                if (state.gameOver) return;
                let vx = 0, vy = 0;
                if (cursors.left.isDown) vx = -300; else if (cursors.right.isDown) vx = 300;
                if (cursors.up.isDown) vy = -300; else if (cursors.down.isDown) vy = 300;
                player.setVelocity(vx, vy);
                if (state.mechanicCooldown > 0) state.mechanicCooldown--;
            }};
        }}
    }},
    scale: {{ mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH }}
}};
const game = new Phaser.Game(config);
'''

    # ==================== PLATFORMER ====================
    @staticmethod
    def _platformer(game_data, theme, style):
        p, s, a, bg0, bg1 = theme["primary"], theme["secondary"], theme["accent"], theme["bg"][0], theme["bg"][1]
        name, mechanic, hook, desc = game_data["name"], game_data["mechanic"], game_data["mechanic_description"], game_data["description"]
        return f'''
const config = {{
    type: Phaser.AUTO,
    width: 800, height: 600,
    physics: {{ default: 'arcade', arcade: {{ gravity: {{ y: 300 }}, debug: false }} }},
    scene: {{
        preload: function() {{
            this.load.image('bg', 'assets/bg.png');
            this.load.image('player', 'assets/player.png');
            this.load.image('enemy', 'assets/enemy.png');
            this.load.image('coin', 'assets/coin.png');
        }},
        create: function() {{
            if (this.textures.exists('bg')) this.add.image(400, 300, 'bg');
            else {{ const g = this.add.graphics(); g.fillStyle(0x1a1a2e).fillRect(0, 0, 800, 600); }}
            let player;
            if (this.textures.exists('player')) {{
                player = this.physics.add.sprite(100, 450, 'player');
            }} else {{
                player = this.add.circle(100, 450, 20, 0x4ecdc4);
                this.physics.add.existing(player);
                player.body.setCircle(20);
            }}
            player.setCollideWorldBounds(true);
            player.setBounce(0.1);
            const platforms = this.physics.add.staticGroup();
            platforms.create(400, 580, 'coin').setScale(10, 0.5).refreshBody();
            for(let i=0;i<8;i++) platforms.create(80+i*100,400-50*Math.sin(i*0.7),'coin').setScale(2.5,0.3).refreshBody();
            this.physics.add.collider(player, platforms);
            const coins = this.physics.add.staticGroup();
            for(let i=0;i<15;i++) coins.create(50+Math.random()*700,100+Math.random()*300,'coin');
            const enemies = this.physics.add.group();
            for(let i=0;i<3;i++){{
                const e=enemies.create(150+i*200,550,'enemy');
                e.setScale(0.6);
                e.body.allowGravity=false;
                e.setVelocityX(80*(i%2===0?1:-1));
            }}
            const cursors = this.input.keyboard.createCursorKeys();
            let state = {{ score:0, lives:3, gameOver:false, mechanicCooldown:0 }};
            const scoreText = this.add.text(16, 16, 'Score: 0', {{fontSize:'28px',fill:'#fff'}});
            const livesText = this.add.text(16, 56, 'Lives: 3', {{fontSize:'28px',fill:'#fff'}});
            const mechanicText = this.add.text(16, 96, '⚡ {mechanic} (SPACE) - double jump', {{fontSize:'20px',fill:'#ffd93d'}});

            this.physics.add.overlap(player, coins, (p,c)=>{{c.destroy(); state.score+=10; scoreText.setText('Score: '+state.score);}});
            this.physics.add.overlap(player, enemies, (p,e)=>{{state.lives--; livesText.setText('Lives: '+state.lives); if(state.lives<=0){{state.gameOver=true; showGameOver.call(this);}}}});

            function useMechanic() {{
                if(state.gameOver||state.mechanicCooldown>0)return;
                state.mechanicCooldown=120;
                player.setVelocityY(-500);
                this.cameras.main.flash(100,0,255,255);
            }}
            this.input.keyboard.on('keydown-SPACE', useMechanic, this);
            this.input.on('pointerdown', useMechanic, this);

            function showGameOver() {{
                this.add.text(300,250,'GAME OVER',{{fontSize:'64px',fill:'#ff0000'}});
                this.add.text(300,320,'Press R to restart',{{fontSize:'32px',fill:'#fff'}});
                this.input.keyboard.on('keydown-R',()=>{{this.scene.restart();}});
            }}
            this.update = function() {{
                if(state.gameOver)return;
                if(cursors.left.isDown) player.setVelocityX(-160);
                else if(cursors.right.isDown) player.setVelocityX(160);
                else player.setVelocityX(0);
                if(cursors.up.isDown && player.body.touching.down) player.setVelocityY(-400);
                enemies.children.iterate(e=>{{if(e.x<50||e.x>750)e.setVelocityX(-e.body.velocity.x);}});
                if(state.mechanicCooldown>0)state.mechanicCooldown--;
            }};
        }}
    }},
    scale: {{ mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH }}
}};
const game = new Phaser.Game(config);
'''

    # ==================== PUZZLE ====================
    @staticmethod
    def _puzzle(game_data, theme, style):
        p, s, a, bg0, bg1 = theme["primary"], theme["secondary"], theme["accent"], theme["bg"][0], theme["bg"][1]
        name, mechanic, hook, desc = game_data["name"], game_data["mechanic"], game_data["mechanic_description"], game_data["description"]
        return f'''
const config = {{
    type: Phaser.AUTO,
    width: 800, height: 600,
    scene: {{
        preload: function() {{
            this.load.image('bg', 'assets/bg.png');
            this.load.image('coin', 'assets/coin.png');
        }},
        create: function() {{
            if (this.textures.exists('bg')) this.add.image(400, 300, 'bg');
            else {{ const g = this.add.graphics(); g.fillStyle(0x1a1a2e).fillRect(0, 0, 800, 600); }}
            const emojis = ['🍎','🍌','🍇','🍉','🍓','🍒','🍑','🍊'];
            let deck = [...emojis, ...emojis];
            shuffle(deck);
            const cols=4, rows=4, w=120, h=120, gap=20;
            const startX=(800-cols*(w+gap)+gap)/2, startY=(600-rows*(h+gap)+gap)/2;
            let tiles=[], selected=[], matched=0;
            let score=0, moves=0, timer=0;
            let gameOver=false, mechanicCooldown=0;
            for (let r=0; r<rows; r++) {{
                for (let c=0; c<cols; c++) {{
                    const i=r*cols+c;
                    const x=startX+c*(w+gap), y=startY+r*(h+gap);
                    const tile = this.add.text(x+10, y+10, '?', {{ fontSize: '64px', color: '#fff', backgroundColor: '#333', padding: {{x:20, y:20}} }});
                    tile.setInteractive();
                    tile.value = deck[i];
                    tile.revealed = false;
                    tile.matched = false;
                    tile.x0=x; tile.y0=y;
                    tile.on('pointerdown', () => handleTileClick(tile, this));
                    tiles.push(tile);
                }}
            }}
            const scoreText = this.add.text(16, 16, 'Score: 0', {{ fontSize: '28px', fill: '#fff' }});
            const moveText = this.add.text(16, 56, 'Moves: 0', {{ fontSize: '28px', fill: '#fff' }});
            const timerText = this.add.text(16, 96, 'Time: 0s', {{ fontSize: '28px', fill: '#fff' }});
            const mechanicText = this.add.text(16, 136, '⚡ {mechanic} (SPACE) - shuffle', {{ fontSize: '20px', fill: '#ffd93d' }});

            function shuffle(arr){{ for(let i=arr.length-1;i>0;i--){{ const j=Math.floor(Math.random()*(i+1)); [arr[i],arr[j]]=[arr[j],arr[i]]; }} }}
            function handleTileClick(tile, scene) {{
                if (gameOver || tile.revealed || tile.matched || selected.length===2) return;
                tile.setText(tile.value);
                tile.revealed = true;
                selected.push(tile);
                if (selected.length===2) {{
                    moves++;
                    moveText.setText('Moves: '+moves);
                    const [t1,t2] = selected;
                    if (t1.value === t2.value) {{
                        t1.matched = true; t2.matched = true;
                        matched++;
                        score += 10;
                        scoreText.setText('Score: '+score);
                        selected = [];
                        if (matched === 8) {{
                            gameOver = true;
                            this.add.text(300, 250, 'YOU WIN!', {{ fontSize: '64px', fill: '#00ff00' }});
                            this.add.text(300, 320, 'Press R to restart', {{ fontSize: '32px', fill: '#fff' }});
                            this.input.keyboard.on('keydown-R', () => {{ this.scene.restart(); }});
                        }}
                    }} else {{
                        scene.time.delayedCall(500, () => {{
                            t1.setText('?'); t2.setText('?');
                            t1.revealed = false; t2.revealed = false;
                            selected = [];
                        }});
                    }}
                }}
            }}
            function useMechanic() {{
                if(gameOver||mechanicCooldown>0)return;
                mechanicCooldown=180;
                let unmatch = tiles.filter(t => !t.matched);
                let values = unmatch.map(t => t.value);
                shuffle(values);
                unmatch.forEach((t,i) => {{
                    t.value = values[i];
                    if (t.revealed) t.setText('?');
                    t.revealed = false;
                }});
                selected = [];
                this.cameras.main.flash(200,255,255,0);
            }}
            this.input.keyboard.on('keydown-SPACE', useMechanic, this);
            this.input.on('pointerdown', useMechanic, this);
            this.time.addEvent({{ delay: 1000, callback: () => {{ if (!gameOver) {{ timer++; timerText.setText('Time: '+timer+'s'); }} }}, loop: true }});
        }}
    }},
    scale: {{ mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH }}
}};
const game = new Phaser.Game(config);
'''

    # ==================== RACER ====================
    @staticmethod
    def _racer(game_data, theme, style):
        p, s, a, bg0, bg1 = theme["primary"], theme["secondary"], theme["accent"], theme["bg"][0], theme["bg"][1]
        name, mechanic, hook, desc = game_data["name"], game_data["mechanic"], game_data["mechanic_description"], game_data["description"]
        return f'''
const config = {{
    type: Phaser.AUTO,
    width: 800, height: 600,
    physics: {{ default: 'arcade', arcade: {{ debug: false }} }},
    scene: {{
        preload: function() {{
            this.load.image('bg', 'assets/bg.png');
            this.load.image('player', 'assets/player.png');
            this.load.image('enemy', 'assets/enemy.png');
            this.load.image('powerup', 'assets/powerup.png');
        }},
        create: function() {{
            if (this.textures.exists('bg')) this.add.image(400, 300, 'bg');
            else {{ const g = this.add.graphics(); g.fillStyle(0x1a1a2e).fillRect(0, 0, 800, 600); }}
            let player;
            if (this.textures.exists('player')) {{
                player = this.physics.add.sprite(400, 520, 'player');
            }} else {{
                player = this.add.circle(400, 520, 20, 0x4ecdc4);
                this.physics.add.existing(player);
                player.body.setCircle(20);
            }}
            player.setCollideWorldBounds(true);
            player.setScale(0.6);
            const cursors = this.input.keyboard.createCursorKeys();
            let obstacles = this.physics.add.group();
            let boost = this.physics.add.group();
            let state = {{ score:0, lives:3, speed:6, gameOver:false, mechanicCooldown:0 }};
            const scoreText = this.add.text(16, 16, 'Score: 0', {{ fontSize: '28px', fill: '#fff' }});
            const livesText = this.add.text(16, 56, 'Lives: 3', {{ fontSize: '28px', fill: '#fff' }});
            const mechanicText = this.add.text(16, 96, '⚡ {mechanic} (SPACE) - boost', {{ fontSize: '20px', fill: '#ffd93d' }});

            this.time.addEvent({{ delay: 700, callback: spawnObstacle, callbackScope: this, loop: true }});
            this.time.addEvent({{ delay: 3000, callback: spawnBoost, callbackScope: this, loop: true }});

            function spawnObstacle() {{
                const x = Phaser.Math.Between(40, 760);
                const ob = obstacles.create(x, -40, 'enemy');
                ob.setScale(0.5);
            }}
            function spawnBoost() {{
                const x = Phaser.Math.Between(100, 700);
                const b = boost.create(x, -30, 'powerup');
                b.setScale(0.4);
                b.setVelocityY(50);
            }}
            function useMechanic() {{
                if(state.gameOver||state.mechanicCooldown>0)return;
                state.mechanicCooldown=180;
                state.speed = Math.min(state.speed+4, 15);
                this.cameras.main.flash(100,255,255,100);
            }}
            this.input.keyboard.on('keydown-SPACE', useMechanic, this);
            this.input.on('pointerdown', useMechanic, this);
            this.physics.add.overlap(player, obstacles, (p, ob) => {{
                ob.destroy();
                state.lives--;
                livesText.setText('Lives: '+state.lives);
                if(state.lives<=0){{ state.gameOver=true; showGameOver.call(this); }}
            }});
            this.physics.add.overlap(player, boost, (p, b) => {{
                b.destroy();
                state.speed = Math.min(state.speed+2, 12);
            }});

            function showGameOver() {{
                this.add.text(300, 250, 'CRASH!', {{ fontSize: '64px', fill: '#ff0000' }});
                this.add.text(300, 320, 'Press R to restart', {{ fontSize: '32px', fill: '#fff' }});
                this.input.keyboard.on('keydown-R', () => {{ this.scene.restart(); }});
            }}
            this.update = function() {{
                if(state.gameOver)return;
                if(cursors.left.isDown) player.x -= 7;
                else if(cursors.right.isDown) player.x += 7;
                state.speed += 0.001;
                obstacles.children.iterate(ob => {{
                    ob.y += state.speed;
                    if (ob.y > 650) {{
                        ob.destroy();
                        state.score++;
                        scoreText.setText('Score: '+state.score);
                    }}
                }});
                if(state.mechanicCooldown>0)state.mechanicCooldown--;
            }};
        }}
    }},
    scale: {{ mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH }}
}};
const game = new Phaser.Game(config);
'''

    # ==================== HORROR ====================
    @staticmethod
    def _horror(game_data, theme, style):
        p, s, a, bg0, bg1 = theme["primary"], theme["secondary"], theme["accent"], theme["bg"][0], theme["bg"][1]
        name, mechanic, hook, desc = game_data["name"], game_data["mechanic"], game_data["mechanic_description"], game_data["description"]
        return f'''
const config = {{
    type: Phaser.AUTO,
    width: 800, height: 600,
    physics: {{ default: 'arcade', arcade: {{ debug: false }} }},
    scene: {{
        preload: function() {{
            this.load.image('bg', 'assets/bg.png');
            this.load.image('player', 'assets/player.png');
            this.load.image('enemy', 'assets/enemy.png');
            this.load.image('coin', 'assets/coin.png');
        }},
        create: function() {{
            if (this.textures.exists('bg')) this.add.image(400, 300, 'bg');
            else {{ const g = this.add.graphics(); g.fillStyle(0x0a0a0a).fillRect(0, 0, 800, 600); }}
            let player;
            if (this.textures.exists('player')) {{
                player = this.physics.add.sprite(400, 300, 'player');
            }} else {{
                player = this.add.circle(400, 300, 20, 0x4ecdc4);
                this.physics.add.existing(player);
                player.body.setCircle(20);
            }}
            player.setCollideWorldBounds(true);
            player.setScale(0.7);
            const cursors = this.input.keyboard.createCursorKeys();
            let monsters = this.physics.add.group();
            let keys = this.physics.add.staticGroup();
            let foundKeys = 0, totalKeys = 5;
            let stealth = 100;
            let gameOver = false, mechanicCooldown = 0;
            for (let i=0; i<totalKeys; i++) {{
                const x = Phaser.Math.Between(50, 750);
                const y = Phaser.Math.Between(50, 550);
                keys.create(x, y, 'coin');
            }}
            this.time.addEvent({{ delay: 1500, callback: spawnMonster, callbackScope: this, loop: true }});
            function spawnMonster() {{
                const x = Phaser.Math.Between(50, 750);
                const y = Phaser.Math.Between(50, 550);
                const mon = monsters.create(x, y, 'enemy');
                mon.setScale(0.7);
            }}
            this.physics.add.overlap(player, keys, (p, k) => {{
                k.destroy(); foundKeys++;
                this.children.list.forEach(c => {{ if (c.text && c.text.startsWith('Keys:')) c.setText('Keys: '+foundKeys+'/'+totalKeys); }});
                if (foundKeys === totalKeys) {{
                    gameOver = true;
                    this.add.text(300, 250, 'YOU ESCAPED!', {{ fontSize: '64px', fill: '#00ff00' }});
                    this.add.text(300, 320, 'Press R to restart', {{ fontSize: '32px', fill: '#fff' }});
                    this.input.keyboard.on('keydown-R', () => {{ this.scene.restart(); }});
                }}
            }});
            this.physics.add.overlap(player, monsters, (p, m) => {{
                gameOver = true;
                this.add.text(300, 250, 'CAUGHT!', {{ fontSize: '64px', fill: '#ff0000' }});
                this.add.text(300, 320, 'Press R to restart', {{ fontSize: '32px', fill: '#fff' }});
                this.input.keyboard.on('keydown-R', () => {{ this.scene.restart(); }});
            }});
            const stealthBar = this.add.graphics();
            function updateStealthBar() {{
                stealthBar.clear();
                const color = stealth > 50 ? 0x00ff00 : 0xff0000;
                stealthBar.fillStyle(color, 1);
                stealthBar.fillRect(20, 40, Math.max(0, stealth * 2), 20);
            }}
            this.add.text(20, 20, 'Stealth', {{ fontSize: '20px', fill: '#fff' }});
            this.add.text(20, 60, 'Keys: 0/'+totalKeys, {{ fontSize: '20px', fill: '#fff' }});
            this.add.text(20, 100, '⚡ {mechanic} (SPACE)', {{ fontSize: '18px', fill: '#ffd93d' }});
            function useMechanic() {{
                if(gameOver||mechanicCooldown>0)return;
                mechanicCooldown=180;
                stealth = Math.min(100, stealth + 30);
                updateStealthBar();
                monsters.children.iterate(mon => {{
                    const dx = mon.x - player.x, dy = mon.y - player.y;
                    const dist = Math.hypot(dx, dy);
                    if (dist < 200) {{
                        mon.x += dx * 0.8; mon.y += dy * 0.8;
                    }}
                }});
                this.cameras.main.flash(200, 0, 255, 0);
            }}
            this.input.keyboard.on('keydown-SPACE', useMechanic, this);
            this.input.on('pointerdown', useMechanic, this);
            this.update = function() {{
                if(gameOver)return;
                if(cursors.left.isDown) player.x -= 4;
                else if(cursors.right.isDown) player.x += 4;
                if(cursors.up.isDown) player.y -= 4;
                else if(cursors.down.isDown) player.y += 4;
                monsters.children.iterate(mon => {{
                    const dist = Phaser.Math.Distance.Between(player.x, player.y, mon.x, mon.y);
                    if (dist < 150) {{
                        stealth -= 0.5;
                        if (stealth < 0) {{
                            gameOver = true;
                            this.add.text(300, 250, 'CAUGHT!', {{ fontSize: '64px', fill: '#ff0000' }});
                            this.add.text(300, 320, 'Press R to restart', {{ fontSize: '32px', fill: '#fff' }});
                            this.input.keyboard.on('keydown-R', () => {{ this.scene.restart(); }});
                        }}
                        updateStealthBar();
                    }}
                }});
                if(mechanicCooldown>0)mechanicCooldown--;
            }};
        }}
    }},
    scale: {{ mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH }}
}};
const game = new Phaser.Game(config);
'''

    # ==================== STRATEGY ====================
    @staticmethod
    def _strategy(game_data, theme, style):
        p, s, a, bg0, bg1 = theme["primary"], theme["secondary"], theme["accent"], theme["bg"][0], theme["bg"][1]
        name, mechanic, hook, desc = game_data["name"], game_data["mechanic"], game_data["mechanic_description"], game_data["description"]
        return f'''
const config = {{
    type: Phaser.AUTO,
    width: 800, height: 600,
    physics: {{ default: 'arcade', arcade: {{ debug: false }} }},
    scene: {{
        preload: function() {{
            this.load.image('bg', 'assets/bg.png');
            this.load.image('player', 'assets/player.png');
            this.load.image('enemy', 'assets/enemy.png');
            this.load.image('coin', 'assets/coin.png');
        }},
        create: function() {{
            if (this.textures.exists('bg')) this.add.image(400, 300, 'bg');
            else {{ const g = this.add.graphics(); g.fillStyle(0x1a1a2e).fillRect(0, 0, 800, 600); }}
            const base = this.add.rectangle(400, 550, 100, 50, 0x4ecdc4);
            this.physics.add.existing(base, true);
            let enemies = this.physics.add.group();
            let towers = this.physics.add.group();
            let projectiles = this.physics.add.group();
            let state = {{ gold:50, baseHealth:100, wave:1, gameOver:false, mechanicCooldown:0 }};
            const goldText = this.add.text(20, 20, 'Gold: '+state.gold, {{ fontSize: '24px', fill: '#fff' }});
            const baseHealthText = this.add.text(20, 60, 'Base HP: '+state.baseHealth, {{ fontSize: '24px', fill: '#fff' }});
            const waveText = this.add.text(20, 100, 'Wave: '+state.wave, {{ fontSize: '24px', fill: '#fff' }});
            const mechanicText = this.add.text(20, 140, '⚡ {mechanic} (SPACE) - +20 gold', {{ fontSize: '18px', fill: '#ffd93d' }});

            this.time.addEvent({{ delay: 1500, callback: spawnEnemy, callbackScope: this, loop: true }});
            function spawnEnemy() {{
                const x = Phaser.Math.Between(50, 750);
                const enemy = enemies.create(x, 0, 'enemy');
                enemy.setScale(0.6);
            }}
            this.input.on('pointerdown', placeTower, this);
            function placeTower(pointer) {{
                if (state.gold < 30) return;
                state.gold -= 30;
                const tower = this.physics.add.sprite(pointer.x, pointer.y, 'player');
                tower.setScale(0.4);
                towers.add(tower);
                goldText.setText('Gold: '+state.gold);
            }}
            function useMechanic() {{
                if(state.gameOver||state.mechanicCooldown>0)return;
                state.mechanicCooldown=120;
                state.gold += 20;
                goldText.setText('Gold: '+state.gold);
                this.cameras.main.flash(100,255,215,0);
            }}
            this.input.keyboard.on('keydown-SPACE', useMechanic, this);
            this.input.on('pointerdown', useMechanic, this);
            this.update = function() {{
                if(state.gameOver)return;
                enemies.children.iterate(enemy => {{
                    enemy.y += 1 + state.wave * 0.5;
                    if (enemy.y > 580) {{
                        enemy.destroy();
                        state.baseHealth -= 10;
                        baseHealthText.setText('Base HP: '+state.baseHealth);
                        if (state.baseHealth <= 0) {{
                            state.gameOver = true;
                            this.add.text(300, 250, 'BASE DESTROYED', {{ fontSize: '64px', fill: '#ff0000' }});
                            this.add.text(300, 320, 'Press R to restart', {{ fontSize: '32px', fill: '#fff' }});
                            this.input.keyboard.on('keydown-R', () => {{ this.scene.restart(); }});
                        }}
                    }}
                }});
                towers.children.iterate(tower => {{
                    const closest = enemies.getChildren().reduce((a,b) => {{
                        const da = Phaser.Math.Distance.Between(tower.x, tower.y, a.x, a.y);
                        const db = Phaser.Math.Distance.Between(tower.x, tower.y, b.x, b.y);
                        return da < db ? a : b;
                    }});
                    if (closest && Phaser.Math.Distance.Between(tower.x, tower.y, closest.x, closest.y) < 200) {{
                        const proj = projectiles.create(tower.x, tower.y, 'coin');
                        proj.setScale(0.2);
                        this.physics.moveToObject(proj, closest, 200);
                        this.physics.add.overlap(proj, closest, (p, e) => {{
                            p.destroy(); e.destroy();
                            state.gold += 10;
                            goldText.setText('Gold: '+state.gold);
                        }});
                    }}
                }});
                if(state.mechanicCooldown>0)state.mechanicCooldown--;
            }};
        }}
    }},
    scale: {{ mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH }}
}};
const game = new Phaser.Game(config);
'''

    # ==================== ROGUELIKE ====================
    @staticmethod
    def _roguelike(game_data, theme, style):
        p, s, a, bg0, bg1 = theme["primary"], theme["secondary"], theme["accent"], theme["bg"][0], theme["bg"][1]
        name, mechanic, hook, desc = game_data["name"], game_data["mechanic"], game_data["mechanic_description"], game_data["description"]
        return f'''
const config = {{
    type: Phaser.AUTO,
    width: 800, height: 600,
    scene: {{
        preload: function() {{
            this.load.image('bg', 'assets/bg.png');
            this.load.image('player', 'assets/player.png');
            this.load.image('enemy', 'assets/enemy.png');
            this.load.image('coin', 'assets/coin.png');
        }},
        create: function() {{
            if (this.textures.exists('bg')) this.add.image(400, 300, 'bg');
            else {{ const g = this.add.graphics(); g.fillStyle(0x1a1a2e).fillRect(0, 0, 800, 600); }}
            let graphics = this.add.graphics();
            let dungeon = [], player = {{x:1, y:1}}, enemies = [];
            let turn = 0, hp = 10, maxHp = 10, gold = 0, gameOver = false;
            const size = 10;
            function generateDungeon() {{
                dungeon = [];
                for (let y=0; y<size; y++) {{
                    const row = [];
                    for (let x=0; x<size; x++) row.push(Math.random() < 0.25 ? 1 : 0);
                    dungeon.push(row);
                }}
                dungeon[1][1] = 0;
                dungeon[size-2][size-2] = 0;
                player = {{x:1, y:1}};
                enemies = [];
                for (let i=0; i<4; i++) {{
                    let ex, ey;
                    do {{ ex = Math.floor(Math.random()*size); ey = Math.floor(Math.random()*size); }}
                    while (dungeon[ey][ex] !== 0 || (ex===1 && ey===1));
                    enemies.push({{x:ex, y:ey, hp:3, maxHp:3}});
                }}
                let gx, gy;
                do {{ gx = Math.floor(Math.random()*size); gy = Math.floor(Math.random()*size); }}
                while (dungeon[gy][gx] !== 0 || (gx===1 && gy===1));
                enemies.push({{x:gx, y:gy, hp:0, gold:10}});
            }}
            function drawDungeon() {{
                graphics.clear();
                const cellSize = 60;
                const offsetX = (800 - size*cellSize)/2, offsetY = (600 - size*cellSize)/2;
                for (let y=0; y<size; y++) {{
                    for (let x=0; x<size; x++) {{
                        const px = offsetX + x*cellSize, py = offsetY + y*cellSize;
                        if (dungeon[y][x] === 1) {{
                            graphics.fillStyle(0x444444, 1);
                        }} else {{
                            graphics.fillStyle(0x2a2a4a, 1);
                        }}
                        graphics.fillRect(px, py, cellSize, cellSize);
                        graphics.lineStyle(1, 0x555555);
                        graphics.strokeRect(px, py, cellSize, cellSize);
                        enemies.forEach(e => {{
                            if (e.x === x && e.y === y) {{
                                if (e.hp > 0) {{
                                    graphics.fillStyle(0xff4444, 1);
                                    graphics.fillCircle(px+cellSize/2, py+cellSize/2, 15);
                                }} else {{
                                    graphics.fillStyle(0xffd93d, 1);
                                    graphics.fillCircle(px+cellSize/2, py+cellSize/2, 12);
                                }}
                            }}
                        }});
                        if (player.x === x && player.y === y) {{
                            graphics.fillStyle(0x4ecdc4, 1);
                            graphics.fillCircle(px+cellSize/2, py+cellSize/2, 20);
                        }}
                    }}
                }}
            }}
            generateDungeon();
            drawDungeon();
            const uiText = this.add.text(20, 20, 'HP: '+hp+'/'+maxHp+'  Gold: '+gold, {{ fontSize: '20px', fill: '#fff' }});
            this.add.text(20, 60, 'Turn: '+turn, {{ fontSize: '20px', fill: '#fff' }});
            const mechanicText = this.add.text(20, 100, '⚡ {mechanic} (SPACE) - heal +3', {{ fontSize: '18px', fill: '#ffd93d' }});

            function useMechanic() {{
                if(gameOver)return;
                hp = Math.min(maxHp, hp + 3);
                uiText.setText('HP: '+hp+'/'+maxHp+'  Gold: '+gold);
                this.cameras.main.flash(100, 0, 255, 0);
            }}
            this.input.keyboard.on('keydown-SPACE', useMechanic, this);
            this.input.on('pointerdown', useMechanic, this);

            function movePlayer(dx, dy) {{
                if(gameOver)return;
                const nx = player.x + dx, ny = player.y + dy;
                if (nx<0 || nx>=size || ny<0 || ny>=size) return;
                if (dungeon[ny][nx] === 1) return;
                let enemyHere = enemies.find(e => e.x === nx && e.y === ny);
                if (enemyHere) {{
                    if (enemyHere.hp > 0) {{
                        enemyHere.hp--;
                        if (enemyHere.hp <= 0) {{
                            gold += 5;
                            uiText.setText('HP: '+hp+'/'+maxHp+'  Gold: '+gold);
                            enemies = enemies.filter(e => e !== enemyHere);
                        }} else {{
                            hp--;
                            if (hp <= 0) {{
                                gameOver = true;
                                this.add.text(300, 250, 'GAME OVER', {{ fontSize: '64px', fill: '#ff0000' }});
                                this.add.text(300, 320, 'Press R to restart', {{ fontSize: '32px', fill: '#fff' }});
                                this.input.keyboard.on('keydown-R', () => {{ this.scene.restart(); }});
                            }}
                        }}
                    }} else {{
                        gold += enemyHere.gold || 10;
                        enemies = enemies.filter(e => e !== enemyHere);
                    }}
                    turn++;
                    uiText.setText('HP: '+hp+'/'+maxHp+'  Gold: '+gold);
                    drawDungeon();
                    return;
                }}
                player.x = nx; player.y = ny;
                turn++;
                enemies.forEach(e => {{
                    if (e.hp <= 0) return;
                    const dirs = [[1,0],[-1,0],[0,1],[0,-1]];
                    const shuffled = dirs.sort(() => Math.random() - 0.5);
                    for (let d of shuffled) {{
                        const ex = e.x + d[0], ey = e.y + d[1];
                        if (ex<0 || ex>=size || ey<0 || ey>=size) continue;
                        if (dungeon[ey][ex] === 1) continue;
                        if (ex === player.x && ey === player.y) {{
                            hp--;
                            if (hp <= 0) {{
                                gameOver = true;
                                this.add.text(300, 250, 'GAME OVER', {{ fontSize: '64px', fill: '#ff0000' }});
                                this.add.text(300, 320, 'Press R to restart', {{ fontSize: '32px', fill: '#fff' }});
                                this.input.keyboard.on('keydown-R', () => {{ this.scene.restart(); }});
                            }}
                            break;
                        }}
                        if (!enemies.some(oe => oe.x === ex && oe.y === ey)) {{
                            e.x = ex; e.y = ey;
                            break;
                        }}
                    }}
                }});
                uiText.setText('HP: '+hp+'/'+maxHp+'  Gold: '+gold);
                drawDungeon();
            }}
            this.input.keyboard.on('keydown-W', () => movePlayer(0,-1));
            this.input.keyboard.on('keydown-A', () => movePlayer(-1,0));
            this.input.keyboard.on('keydown-S', () => movePlayer(0,1));
            this.input.keyboard.on('keydown-D', () => movePlayer(1,0));
        }}
    }},
    scale: {{ mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH }}
}};
const game = new Phaser.Game(config);
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
        print("\n"+"═"*60); print("🎮 GENERATING NEW GAME (Production Engine)"); print("═"*60)
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

        folder = Path(f"workspace/{game['name'].replace(' ','_')}")
        folder.mkdir(parents=True, exist_ok=True)
        ArtDirector.generate_all_assets(game["name"], game["genre"], game["visual_style"], template, folder)
        GameEngine.build(game, self.design.THEMES[game["visual_style"]], self.design.STYLES[game["game_style"]], template, folder)

        zip_path = Path("workspace/latest_game.zip")
        try:
            if zip_path.exists(): zip_path.unlink()
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
                for f in folder.rglob("*"):
                    if f.is_file():
                        z.write(f, f.relative_to(folder.parent))
        except: pass

        html5_url = f"https://{CONFIG['brand']['github']}.github.io/FACTORY-BOT-V4/workspace/{game['name'].replace(' ','_')}/index.html"
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
            if sprite.exists():
                self.telegram.send_photo(channel, sprite, post)
            else:
                self.telegram.send_message(channel, post)
        if TELEGRAM_CHAT_ID:
            if sprite.exists():
                self.telegram.send_photo(TELEGRAM_CHAT_ID, sprite, post)
            else:
                self.telegram.send_message(TELEGRAM_CHAT_ID, post)
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
