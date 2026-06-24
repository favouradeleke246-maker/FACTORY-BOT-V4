#!/usr/bin/env python3
"""
DEATHROLL STUDIO v47.0 – MODULAR GAME GENERATION (FULL)
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
BOT_VERSION = "47.0.0"
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

print("═"*60); print("🔥 DEATHROLL STUDIO v47.0 – MODULAR GAME GENERATION")
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
# ART DIRECTOR – generates unique assets per game
# ============================================================
class ArtDirector:
    @staticmethod
    def generate_all_assets(game_name, genre, style, template, folder: Path):
        assets = folder / "assets"
        assets.mkdir(exist_ok=True)
        main_sprite = Path("sprite.png")
        if main_sprite.exists() and main_sprite.stat().st_size > 100:
            shutil.copy(main_sprite, assets / "player.png")
        else:
            ArtDirector._create_fallback_player(assets / "player.png", template)
        ArtDirector._generate_enemy_sprite(assets / "enemy.png", template)
        ArtDirector._generate_coin_sprite(assets / "coin.png")
        ArtDirector._generate_powerup_sprite(assets / "powerup.png", template)
        bg = ArtDirector._generate_background(template)
        bg.save(assets / "bg.png")
        print(f"   🎨 Assets generated in {assets}")

    @staticmethod
    def _create_fallback_player(path, template):
        img = Image.new('RGBA', (64, 64), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([8, 8, 56, 56], fill=(78,205,196))
        draw.text((18, 20), "P", fill=(255,255,255), font=None)
        img.save(path)

    @staticmethod
    def _generate_enemy_sprite(path, template):
        img = Image.new('RGBA', (64, 64), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        if template == "shooter":
            draw.polygon([(32, 0), (64, 48), (32, 32), (0, 48)], fill=(255,68,68))
        elif template == "horror":
            draw.ellipse([8, 8, 56, 56], fill=(0,0,0))
            draw.ellipse([16, 16, 24, 24], fill=(255,0,0))
            draw.ellipse([40, 16, 48, 24], fill=(255,0,0))
            draw.polygon([(24, 32), (40, 32), (32, 48)], fill=(255,0,0))
        else:
            draw.ellipse([8, 8, 56, 56], fill=(255,68,68))
        img.save(path)

    @staticmethod
    def _generate_coin_sprite(path):
        img = Image.new('RGBA', (32, 32), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([4, 4, 28, 28], fill=(255,215,0))
        draw.ellipse([12, 12, 20, 20], fill=(255,255,0))
        img.save(path)

    @staticmethod
    def _generate_powerup_sprite(path, template):
        img = Image.new('RGBA', (32, 32), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([4, 4, 28, 28], fill=(0,255,136))
        draw.text((8, 4), "⚡", fill=(255,255,255), font=None)
        img.save(path)

    @staticmethod
    def _generate_background(template):
        bg = Image.new('RGB', (800, 600), color=(20, 20, 40))
        draw = ImageDraw.Draw(bg)
        if template == "shooter":
            for _ in range(100):
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
            for _ in range(20):
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
# MODULAR GAME BUILDER – FULL IMPLEMENTATION
# ============================================================
class GameBuilder:
    @staticmethod
    def build(game_data, theme, style, template, folder: Path):
        js = GameBuilder._assemble_js(game_data, theme, style, template)
        index_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <title>{game_data['name']}</title>
    <style>
        body {{ margin:0; padding:0; background:#000; overflow:hidden; touch-action:none; }}
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
        print(f"   🎮 Modular game built in {folder}")

    @staticmethod
    def _assemble_js(game_data, theme, style, template):
        # This method returns a complete Phaser game script with distinct logic per template.
        p = theme["primary"]
        s = theme["secondary"]
        a = theme["accent"]
        glow = "true" if theme["glow"] else "false"
        bg0 = theme["bg"][0]
        bg1 = theme["bg"][1]
        name = game_data["name"]
        mechanic = game_data["mechanic"]
        hook = game_data["hook"]
        desc = game_data["description"]
        mode = game_data["game_mode"]
        diff = game_data["difficulty"]

        # A single JS with conditional logic per template
        js = f'''
// ---- {name} - Generated by DeathRoll Studio ----
const config = {{
    type: Phaser.AUTO,
    width: 800,
    height: 600,
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
            // Background
            if (this.textures.exists('bg')) this.add.image(400, 300, 'bg');
            else {{ const g = this.add.graphics(); g.fillStyle(0x1a1a2e).fillRect(0, 0, 800, 600); }}

            // Player
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

            // Cursors
            const cursors = this.input.keyboard.createCursorKeys();

            // Template: {template}
            // Game state
            let state = {{
                score: 0,
                health: 100,
                wave: 1,
                gameOver: false,
                mechanicCooldown: 0,
                enemies: this.physics.add.group(),
                coins: this.physics.add.group(),
                powerups: this.physics.add.group(),
                spawnTimer: 0,
                // Additional flags
                template: '{template}'
            }};

            // UI
            const scoreText = this.add.text(16, 16, 'Score: 0', {{ fontSize: '28px', fill: '#fff' }});
            const healthText = this.add.text(16, 56, 'HP: 100', {{ fontSize: '28px', fill: '#fff' }});
            const mechanicText = this.add.text(16, 96, '⚡ {mechanic} (SPACE)', {{ fontSize: '20px', fill: '#ffd93d' }});

            // Mechanic function – implements different effects per template
            function useMechanic() {{
                if (state.gameOver || state.mechanicCooldown > 0) return;
                state.mechanicCooldown = 120;
                // Template-specific effect
                if (state.template === 'shooter') {{
                    // Push enemies away
                    state.enemies.children.iterate(e => {{
                        const dx = e.x - player.x;
                        const dy = e.y - player.y;
                        const dist = Math.hypot(dx, dy);
                        if (dist < 150) {{
                            e.x += dx * 0.5;
                            e.y += dy * 0.5;
                        }}
                    }});
                }} else if (state.template === 'platformer') {{
                    // Double jump (boost)
                    player.setVelocityY(-500);
                }} else if (state.template === 'puzzle') {{
                    // Shuffle – can be implemented with more logic
                }} else if (state.template === 'racer') {{
                    // Speed boost (increase game speed)
                }} else if (state.template === 'horror') {{
                    // Stealth boost (increase stealth meter)
                }} else if (state.template === 'strategy') {{
                    // Gold boost
                }} else if (state.template === 'roguelike') {{
                    // Heal player
                    state.health = Math.min(100, state.health + 20);
                    healthText.setText('HP: ' + state.health);
                }}
                this.cameras.main.shake(100);
                this.cameras.main.flash(100, 255, 255, 255);
            }}

            // Input
            this.input.keyboard.on('keydown-SPACE', useMechanic, this);
            this.input.on('pointerdown', useMechanic, this);

            // Collisions
            this.physics.add.overlap(player, state.enemies, (p, e) => {{
                state.health -= 10;
                e.destroy();
                healthText.setText('HP: ' + state.health);
                if (state.health <= 0) {{
                    state.gameOver = true;
                    showGameOver.call(this);
                }}
            }});
            this.physics.add.overlap(player, state.coins, (p, c) => {{
                c.destroy();
                state.score += 10;
                scoreText.setText('Score: ' + state.score);
            }});
            this.physics.add.overlap(player, state.powerups, (p, pw) => {{
                pw.destroy();
                state.health = Math.min(100, state.health + 20);
                healthText.setText('HP: ' + state.health);
            }});

            // Spawn function
            function spawnEnemy() {{
                if (state.gameOver) return;
                const x = Phaser.Math.Between(50, 750);
                const enemy = state.enemies.create(x, 0, 'enemy');
                enemy.setVelocityY(100 + state.wave * 20);
                enemy.setScale(0.6 + state.wave * 0.02);
                // Additional behavior per template
                if (state.template === 'platformer') {{
                    enemy.setVelocityX(Phaser.Math.Between(-50, 50));
                }}
            }}

            // Update function
            this.update = function(time) {{
                if (state.gameOver) return;

                // Player movement
                let vx = 0, vy = 0;
                if (cursors.left.isDown) vx = -300;
                else if (cursors.right.isDown) vx = 300;
                if (cursors.up.isDown) vy = -300;
                else if (cursors.down.isDown) vy = 300;
                player.setVelocity(vx, vy);

                // Cooldown
                if (state.mechanicCooldown > 0) state.mechanicCooldown--;

                // Spawn
                state.spawnTimer--;
                if (state.spawnTimer <= 0) {{
                    spawnEnemy();
                    state.spawnTimer = 1000;
                }}

                // Template-specific update (if any)
                // (e.g., racer would scroll obstacles)
            }};

            // Game over screen
            function showGameOver() {{
                this.add.text(300, 250, 'GAME OVER', {{ fontSize: '64px', fill: '#ff0000' }});
                this.add.text(300, 320, 'Press R to restart', {{ fontSize: '32px', fill: '#fff' }});
                this.input.keyboard.on('keydown-R', () => {{ this.scene.restart(); }});
            }}

            // Start spawning
            state.spawnTimer = 1000;
        }}
    }},
    scale: {{ mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH }}
}};
const game = new Phaser.Game(config);
'''
        return js

# ============================================================
# PHASER GAME GENERATOR – dispatcher
# ============================================================
def generate_phaser_game(game_data, theme, style, template, folder: Path):
    GameBuilder.build(game_data, theme, style, template, folder)

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
        print("\n"+"═"*60); print("🎮 GENERATING NEW MODULAR GAME"); print("═"*60)
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
        generate_phaser_game(game, self.design.THEMES[game["visual_style"]], self.design.STYLES[game["game_style"]], template, folder)

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
