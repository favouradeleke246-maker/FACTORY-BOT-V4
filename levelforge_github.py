#!/usr/bin/env python3
"""
DEATHROLL STUDIO v31.0 - PROFESSIONAL AI GAME FACTORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI-Powered Game Generation | No Loops | Clean Architecture
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os
import json
import random
import hashlib
import requests
import time
import shutil
import zipfile
import uuid
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw
from typing import Dict, List, Optional, Tuple, Any

# ============================================================================
# CONFIGURATION
# ============================================================================

BOT_VERSION = "31.0.0"

CONFIG = {
    "brand": {
        "name": "DeathRoll",
        "email_primary": "favouradeleke246@gmail.com",
        "email_secondary": "fadeleke246@gmail.com",
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
        "default": 7,
        "min": 2,
        "max": 10
    }
}

# ============================================================================
# ENVIRONMENT
# ============================================================================

def get_env(key: str, default: Any = None) -> Any:
    return os.getenv(key, default)

TELEGRAM_TOKEN = get_env("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = get_env("TELEGRAM_CHAT_ID")
OPENAI_KEY = get_env("OPENAI_API_KEY")
GITHUB_TOKEN = get_env("GH_TOKEN")
GAME_PRICE = get_env("GAME_PRICE", "7")

print("═" * 60)
print("🔥 DEATHROLL STUDIO v31.0 - PROFESSIONAL AI GAME FACTORY")
print("═" * 60)
print(f"🤖 Version: {BOT_VERSION}")
print(f"🏷️ Brand: {CONFIG['brand']['name']}")
print(f"📧 Email: {CONFIG['brand']['email_primary']}")
print(f"✅ Telegram: {'OK' if TELEGRAM_TOKEN else 'NO'}")
print(f"✅ OpenAI: {'OK' if OPENAI_KEY else 'NO'}")
print(f"✅ GitHub: {'OK' if GITHUB_TOKEN else 'NO'}")
print("═" * 60)

# ============================================================================
# AI SERVICE
# ============================================================================

class AIService:
    """Handles all AI interactions with clean error handling"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.enabled = bool(api_key)
    
    def generate(self, prompt: str, max_tokens: int = 150, temperature: float = 0.8) -> Optional[str]:
        """Generate text using OpenAI API"""
        if not self.enabled:
            return None
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
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
    
    def generate_game_design(self, genre: str, previous_games: List[Dict]) -> Dict:
        """Generate a complete game design using AI"""
        
        if not self.enabled:
            return self._fallback_design(genre)
        
        # Build context from previous games
        recent_mechanics = [g.get("mechanic", "") for g in previous_games[-5:] if g.get("mechanic")]
        recent_names = [g.get("name", "") for g in previous_games[-5:] if g.get("name")]
        
        prompt = f"""Design a unique game with these requirements:

Genre: {genre}
Avoid these mechanics: {', '.join(recent_mechanics[:3]) if recent_mechanics else 'none'}
Avoid these names: {', '.join(recent_names[:3]) if recent_names else 'none'}

Return EXACTLY this JSON format:
{{
    "name": "creative game name (2-3 words)",
    "mechanic": "unique mechanic name (2-3 words)",
    "mechanic_description": "how the mechanic works (one sentence)",
    "hook": "one-line hook to sell the game",
    "visual_style": "art style (neon, dark, cartoon, pixel, minimalist)",
    "game_mode": "game mode (endless, waves, time_attack, boss_fight, survival)",
    "difficulty": "easy, medium, hard"
}}

Make it creative and different from typical games."""

        result = self.generate(prompt, max_tokens=300, temperature=1.0)
        
        if result:
            try:
                # Extract JSON from response
                import re
                json_match = re.search(r'\{.*\}', result, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except:
                pass
        
        return self._fallback_design(genre)
    
    def _fallback_design(self, genre: str) -> Dict:
        """Fallback design when AI fails"""
        mechanics = [
            ("Phase Echo", "summon a temporal duplicate"),
            ("Chrono Fracture", "slow time around you"),
            ("Void Step", "teleport through obstacles"),
            ("Mirror Shell", "reflect projectiles"),
            ("Gravity Well", "pull enemies together"),
            ("Soul Link", "share damage with enemies"),
            ("Shadow Cloak", "become invisible when still"),
            ("Berserker Rage", "gain power as health drops")
        ]
        hooks = [
            "Every second counts. Master the unknown.",
            "Death is temporary. Glory is forever.",
            "One mechanic changes everything.",
            "Fight. Survive. Evolve.",
            "Darkness awaits. Are you ready?"
        ]
        styles = ["neon", "dark_fantasy", "cartoon", "pixel", "minimalist"]
        modes = ["endless", "waves", "time_attack", "boss_fight", "survival"]
        
        name_prefixes = ["Neon", "Cyber", "Quantum", "Astral", "Void", "Echo", "Flux", "Rogue", "Crimson", "Shadow"]
        name_suffixes = ["Runner", "Drifter", "Breach", "Vector", "Pulse", "Shift", "Core", "Edge", "Zone", "Fury"]
        
        mechanic = random.choice(mechanics)
        
        return {
            "name": f"{random.choice(name_prefixes)} {random.choice(name_suffixes)}",
            "mechanic": mechanic[0],
            "mechanic_description": mechanic[1],
            "hook": random.choice(hooks),
            "visual_style": random.choice(styles),
            "game_mode": random.choice(modes),
            "difficulty": random.choice(["easy", "medium", "hard"])
        }
    
    def generate_description(self, game_data: Dict) -> str:
        """Generate a professional game description"""
        
        if not self.enabled:
            return self._fallback_description(game_data)
        
        prompt = f"""Write a professional, compelling game description for:

Game: {game_data['name']}
Genre: {game_data['genre']}
Mechanic: {game_data['mechanic']} - {game_data['mechanic_description']}
Hook: {game_data['hook']}

Write 2-3 sentences that would make someone want to play. Professional tone, no emojis.
Make it sound like a real game store description."""

        result = self.generate(prompt, max_tokens=120, temperature=0.7)
        if result and len(result) > 30:
            return result
        
        return self._fallback_description(game_data)
    
    def _fallback_description(self, game_data: Dict) -> str:
        """Fallback description"""
        templates = [
            f"Step into {game_data['name']}, a {game_data['genre']} where {game_data['mechanic']} changes everything. {game_data['mechanic_description']}. Experience thrilling gameplay in this unique adventure.",
            f"Welcome to {game_data['name']}. This {game_data['genre']} challenges you to master {game_data['mechanic']}. {game_data['mechanic_description']}. Can you survive the challenge?",
            f"{game_data['name']} redefines the {game_data['genre']} genre with {game_data['mechanic']}. {game_data['mechanic_description']}. Prepare for an unforgettable gaming experience."
        ]
        return random.choice(templates)


# ============================================================================
# GAME DESIGN SYSTEM
# ============================================================================

class GameDesignSystem:
    """Manages game design and generation"""
    
    GENRES = [
        "top-down shooter", "action RPG", "racing game", "puzzle game",
        "survival horror", "fighting game", "strategy game",
        "extraction shooter", "cozy builder", "roguelite",
        "platformer", "tower defense", "battle royale"
    ]
    
    VISUAL_THEMES = {
        "neon": {
            "bg": ["#0a0a2e", "#1a1a3e", "#0f0f1a"],
            "primary": "#4ecdc4",
            "secondary": "#ff6b6b",
            "accent": "#ffd93d",
            "glow": True
        },
        "dark_fantasy": {
            "bg": ["#0a0a0a", "#1a0a0a", "#0a0a0f"],
            "primary": "#8b0000",
            "secondary": "#ff4444",
            "accent": "#ffd700",
            "glow": False
        },
        "cartoon": {
            "bg": ["#1a2a3a", "#2a4a5a", "#0a1a2a"],
            "primary": "#ff6b35",
            "secondary": "#f7c948",
            "accent": "#4ecdc4",
            "glow": False
        },
        "minimalist": {
            "bg": ["#f5f5f5", "#e8e8e8", "#ffffff"],
            "primary": "#2c3e50",
            "secondary": "#3498db",
            "accent": "#2ecc71",
            "glow": False
        },
        "pixel": {
            "bg": ["#1a1a2e", "#16213e", "#0f0f23"],
            "primary": "#00ff88",
            "secondary": "#ff0066",
            "accent": "#ffcc00",
            "glow": True
        }
    }
    
    GAME_MODES = {
        "endless": {"name": "Endless", "description": "Keep going until you fall"},
        "waves": {"name": "Wave Defense", "description": "Survive wave after wave"},
        "time_attack": {"name": "Time Attack", "description": "Score as much as possible in 60s"},
        "boss_fight": {"name": "Boss Fight", "description": "Defeat the massive boss"},
        "survival": {"name": "Survival", "description": "Survive as long as possible"}
    }
    
    GAME_STYLES = {
        "shooter": {"enemy_speed": 1.2, "spawn_rate": 4, "player_health": 50, "mechanic_effect": "shoot"},
        "platformer": {"enemy_speed": 1.0, "spawn_rate": 3, "player_health": 60, "mechanic_effect": "double_jump"},
        "survival": {"enemy_speed": 1.5, "spawn_rate": 3, "player_health": 100, "mechanic_effect": "push"},
        "collector": {"enemy_speed": 0.8, "spawn_rate": 2, "player_health": 75, "mechanic_effect": "speed_boost"},
        "wave_defense": {"enemy_speed": 1.8, "spawn_rate": 5, "player_health": 80, "mechanic_effect": "shield"}
    }
    
    def __init__(self, ai_service: AIService):
        self.ai = ai_service
        self.sar_data = self._load_sar()
    
    def _load_sar(self) -> Dict:
        """Load SAR data for learning"""
        sar_path = Path("sar_analysis.json")
        if sar_path.exists():
            try:
                return json.loads(sar_path.read_text())
            except:
                pass
        return {"study": {"games": []}, "analysis": {}}
    
    def _save_sar(self):
        """Save SAR data"""
        Path("sar_analysis.json").write_text(json.dumps(self.sar_data, indent=2))
    
    def select_genre(self) -> str:
        """Select genre with SAR weighting"""
        sar_best = self.sar_data.get("analysis", {}).get("best_genre")
        candidates = []
        weights = []
        
        if sar_best and sar_best in self.GENRES:
            candidates.append(sar_best)
            weights.append(0.4)
        
        # Random from genres
        candidates.append(random.choice(self.GENRES))
        weights.append(0.6)
        
        return random.choices(candidates, weights=weights)[0]
    
    def generate_game(self) -> Dict:
        """Generate a complete game design"""
        
        # Select genre
        genre = self.select_genre()
        
        # Get AI design
        previous_games = self.sar_data.get("study", {}).get("games", [])
        design = self.ai.generate_game_design(genre, previous_games)
        
        # Merge with system data
        game_data = {
            "genre": genre,
            "name": design.get("name", f"{random.choice(['Neon','Cyber','Quantum'])} {random.choice(['Runner','Drifter','Breach'])}"),
            "mechanic": design.get("mechanic", "Phase Echo"),
            "mechanic_description": design.get("mechanic_description", "summon a temporal duplicate"),
            "hook": design.get("hook", "Every second counts. Master the unknown."),
            "visual_style": design.get("visual_style", random.choice(list(self.VISUAL_THEMES.keys()))),
            "game_mode": design.get("game_mode", random.choice(list(self.GAME_MODES.keys()))),
            "difficulty": design.get("difficulty", "medium"),
            "game_style": random.choice(list(self.GAME_STYLES.keys()))
        }
        
        # Generate description via AI
        game_data["description"] = self.ai.generate_description(game_data)
        
        return game_data


# ============================================================================
# LICENSE SYSTEM
# ============================================================================

class LicenseSystem:
    """Manages license key generation and verification"""
    
    @staticmethod
    def generate(game_name: str, buyer_username: Optional[str] = None) -> str:
        """Generate a unique license key"""
        timestamp = datetime.now().strftime("%Y%m%d")
        unique_id = str(uuid.uuid4())[:8].upper()
        game_code = ''.join([w[0] for w in game_name.split()[:2]]).upper()
        
        if buyer_username:
            clean = buyer_username.replace('@', '').upper()[:6]
            return f"DR-{game_code}-{timestamp}-{unique_id}-{clean}"
        return f"DR-{game_code}-{timestamp}-{unique_id}"
    
    @staticmethod
    def verify(key: str) -> bool:
        """Verify a license key format"""
        parts = key.split('-')
        if len(parts) < 4:
            return False
        if not parts[0] == "DR":
            return False
        return True


# ============================================================================
# PORTFOLIO SYSTEM
# ============================================================================

class PortfolioSystem:
    """Manages the game portfolio"""
    
    def __init__(self, path: Path = Path("portfolio.json")):
        self.path = path
        self._ensure_exists()
    
    def _ensure_exists(self):
        if not self.path.exists():
            self.path.write_text("[]")
    
    def load(self) -> List[Dict]:
        try:
            data = json.loads(self.path.read_text())
            return data if isinstance(data, list) else []
        except:
            return []
    
    def save(self, games: List[Dict]):
        self.path.write_text(json.dumps(games, indent=2))
    
    def add_game(self, game_data: Dict):
        games = self.load()
        games.append(game_data)
        self.save(games[-200:])  # Keep last 200
        return len(games)


# ============================================================================
# TELEGRAM SERVICE
# ============================================================================

class TelegramService:
    """Handles Telegram messaging"""
    
    def __init__(self, token: Optional[str], channel: str):
        self.token = token
        self.channel = channel
        self.enabled = bool(token)
    
    def send(self, chat_id: str, text: str, parse_mode: str = "Markdown") -> bool:
        if not self.enabled:
            return False
        try:
            response = requests.post(
                f"https://api.telegram.org/bot{self.token}/sendMessage",
                json={"chat_id": chat_id, "text": text, "parse_mode": parse_mode},
                timeout=30
            )
            return response.status_code == 200
        except:
            return False
    
    def send_photo(self, chat_id: str, photo_path: Path, caption: str) -> bool:
        if not self.enabled:
            return False
        try:
            with open(photo_path, "rb") as f:
                response = requests.post(
                    f"https://api.telegram.org/bot{self.token}/sendPhoto",
                    files={"photo": f},
                    data={"chat_id": chat_id, "caption": caption, "parse_mode": "Markdown"},
                    timeout=60
                )
            return response.status_code == 200
        except:
            return False
    
    def send_document(self, chat_id: str, doc_path: Path, caption: str) -> bool:
        if not self.enabled:
            return False
        try:
            with open(doc_path, "rb") as f:
                response = requests.post(
                    f"https://api.telegram.org/bot{self.token}/sendDocument",
                    files={"document": f},
                    data={"chat_id": chat_id, "caption": caption, "parse_mode": "Markdown"},
                    timeout=60
                )
            return response.status_code == 200
        except:
            return False
    
    def send_game_post(self, game_data: Dict, license_key: str, html5_url: str) -> bool:
        """Send the full game sales post"""
        
        theme = GameDesignSystem.VISUAL_THEMES.get(game_data["visual_style"], {})
        emojis = ["🎮", "🔥", "⚡", "💀", "🎯"]
        selected_emojis = " ".join(random.sample(emojis, 3))
        
        post = f"""
{selected_emojis} *{game_data['hook']}* {selected_emojis}

✨ *{game_data['name']}*
*Genre:* {game_data['genre']}
*Mechanic:* `{game_data['mechanic']}`
*Difficulty:* {game_data['difficulty']}

{game_data['description']}

━━━━━━━━━━━━━━━━━━━━━
🎮 *PLAY INSTANTLY (HTML5)*
{html5_url}

🔑 *License Key:* `{license_key}`
💰 *Price:* ${game_data.get('price', 7)} SOL
━━━━━━━━━━━━━━━━━━━━━

🔵 Trust: `{CONFIG['wallets']['trust']}`
🟣 Phantom: `{CONFIG['wallets']['phantom']}`

Send ${game_data.get('price', 7)} SOL + your @username → receive full game

#gamedev #indiegame #{game_data['genre'].replace(' ', '')} #DeathRollStudio
"""
        return self.send_photo(self.channel, Path("sprite.png"), post)


# ============================================================================
# MAIN BOT
# ============================================================================

class DeathRollStudio:
    """Main bot class"""
    
    def __init__(self):
        self.ai = AIService(OPENAI_KEY)
        self.design_system = GameDesignSystem(self.ai)
        self.portfolio = PortfolioSystem()
        self.telegram = TelegramService(TELEGRAM_TOKEN, CONFIG["telegram"]["channel"])
        self.license_system = LicenseSystem()
        
        self.config = CONFIG
        self.version = BOT_VERSION
    
    def run(self):
        """Run the game factory"""
        
        print("\n" + "═" * 60)
        print("🎮 GENERATING NEW GAME")
        print("═" * 60)
        
        # 1. Design the game
        game_data = self.design_system.generate_game()
        print(f"   📝 Game: {game_data['name']}")
        print(f"   🎭 Genre: {game_data['genre']}")
        print(f"   ⚡ Mechanic: {game_data['mechanic']}")
        print(f"   🎨 Style: {game_data['visual_style']}")
        print(f"   🏆 Mode: {game_data['game_mode']}")
        
        # 2. Calculate price
        price = self._calculate_price(game_data)
        game_data["price"] = price
        print(f"   💰 Price: ${price} SOL")
        
        # 3. Generate description (if not already)
        if "description" not in game_data or not game_data["description"]:
            game_data["description"] = self.ai.generate_description(game_data)
        print(f"   📝 {game_data['description'][:100]}...")
        
        # 4. Generate license key
        license_key = self.license_system.generate(game_data["name"])
        print(f"   🔑 License: {license_key}")
        
        # 5. Generate art
        art_url = self._generate_art(game_data)
        print(f"   🎨 Art: {'Success' if art_url else 'Fallback'}")
        
        # 6. Build game files
        html5_url = self._build_game(game_data, license_key)
        print(f"   🌐 HTML5: {html5_url}")
        
        # 7. Update portfolio
        portfolio_entry = self._create_portfolio_entry(game_data, license_key, art_url, html5_url)
        total_games = self.portfolio.add_game(portfolio_entry)
        print(f"   📊 Portfolio: {total_games} games")
        
        # 8. Send to Telegram
        if self.telegram.enabled:
            self.telegram.send_game_post(game_data, license_key, html5_url)
            print(f"   📱 Telegram: Posted")
        
        # 9. Update SAR
        self._update_sar(game_data)
        print(f"   🧠 SAR: Updated")
        
        # 10. Final verification
        print("\n" + "═" * 60)
        print("✅ GAME COMPLETE")
        print("═" * 60)
        print(f"   Game: {game_data['name']}")
        print(f"   License: {license_key}")
        print(f"   HTML5: {html5_url}")
        print(f"   Portfolio: {total_games} games")
        print("═" * 60)
    
    def _calculate_price(self, game_data: Dict) -> int:
        """Calculate dynamic price"""
        base = 3
        
        # Art quality bonus
        if game_data.get("visual_style") in ["neon", "pixel"]:
            base += 1
        
        # Difficulty bonus
        if game_data.get("difficulty") == "hard":
            base += 2
        elif game_data.get("difficulty") == "medium":
            base += 1
        
        # Mode bonus
        if game_data.get("game_mode") == "boss_fight":
            base += 2
        
        return min(max(base, CONFIG["price"]["min"]), CONFIG["price"]["max"])
    
    def _generate_art(self, game_data: Dict) -> Optional[str]:
        """Generate game art"""
        sprite_path = Path("sprite.png")
        
        try:
            style = game_data.get("visual_style", "neon")
            prompt = f"3D {style} render of a {game_data['genre']} character for '{game_data['name']}'"
            url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '+')}?width=512&height=512"
            response = requests.get(url, timeout=45)
            if response.status_code == 200 and len(response.content) > 5000:
                sprite_path.write_bytes(response.content)
                return f"https://raw.githubusercontent.com/{CONFIG['brand']['github']}/FACTORY-BOT-V4/main/sprite.png"
        except:
            pass
        
        # Fallback art
        try:
            img = Image.new('RGB', (512, 512), color=(30, 30, 60))
            draw = ImageDraw.Draw(img)
            draw.rectangle([50, 50, 462, 462], outline=(78, 205, 196), width=4)
            draw.text((180, 230), game_data['name'][:15], fill=(255, 255, 255))
            img.save(sprite_path)
            return None
        except:
            return None
    
    def _build_game(self, game_data: Dict, license_key: str) -> str:
        """Build HTML5 game files"""
        
        # Get theme and mode
        visual_theme = GameDesignSystem.VISUAL_THEMES.get(
            game_data["visual_style"], 
            GameDesignSystem.VISUAL_THEMES["neon"]
        )
        game_mode = GameDesignSystem.GAME_MODES.get(
            game_data["game_mode"],
            GameDesignSystem.GAME_MODES["endless"]
        )
        game_style = GameDesignSystem.GAME_STYLES.get(
            game_data.get("game_style", "survival"),
            GameDesignSystem.GAME_STYLES["survival"]
        )
        
        # Create workspace
        project_dir = Path(f"workspace/{game_data['name'].replace(' ', '_')}")
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy art
        sprite_path = Path("sprite.png")
        if sprite_path.exists():
            shutil.copy(sprite_path, project_dir / "icon.png")
        
        # Generate HTML5 game
        html_content = self._generate_html5_game(game_data, visual_theme, game_mode, game_style)
        (project_dir / "index.html").write_text(html_content)
        
        # Create license file
        (project_dir / "LICENSE.txt").write_text(f"""
╔══════════════════════════════════════════════════════════╗
║              DEATHROLL STUDIO - GAME LICENSE             ║
╠══════════════════════════════════════════════════════════╣
║  Game: {game_data['name']:<47} ║
║  License Key: {license_key:<44} ║
║  Price: {game_data.get('price', 7)} SOL{' ' * 44}║
║  Date: {datetime.now().strftime('%Y-%m-%d'):<44} ║
╠══════════════════════════════════════════════════════════╣
║  ✓ Personal, non-commercial use                          ║
║  ✓ Access to all future updates                          ║
║  ✓ Play on any device you own                           ║
╠══════════════════════════════════════════════════════════╣
║  Support: @deathroll1                                    ║
║  Website: deathroll.co                                   ║
╚══════════════════════════════════════════════════════════╝
""")
        
        # Create README
        (project_dir / "README.md").write_text(f"""
# {game_data['name']}

## Description
{game_data['description']}

## Genre
{game_data['genre']}

## Key Mechanic
**{game_data['mechanic']}**: {game_data['mechanic_description']}

## How to Play
- **HTML5**: Open `index.html` in any browser
- **Controls**: WASD or Arrow Keys to move, SPACE for {game_data['mechanic']}

## License
{license_key}

## Price
{game_data.get('price', 7)} SOL

---
Generated by DeathRoll Studio v{BOT_VERSION}
""")
        
        # Create ZIP
        zip_path = Path("workspace/latest_game.zip")
        try:
            if zip_path.exists():
                zip_path.unlink()
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in project_dir.rglob("*"):
                    if file.is_file():
                        zipf.write(file, file.relative_to(project_dir.parent))
        except:
            pass
        
        return f"https://{CONFIG['brand']['github']}.github.io/FACTORY-BOT-V4/workspace/{game_data['name'].replace(' ', '_')}/index.html"
    
    def _generate_html5_game(self, game_data: Dict, visual_theme: Dict, game_mode: Dict, game_style: Dict) -> str:
        """Generate clean HTML5 game with proper variable handling"""
        
        theme = visual_theme
        mode = game_mode
        style = game_style
        theme_primary = theme["primary"]
        theme_secondary = theme["secondary"]
        theme_accent = theme["accent"]
        theme_glow = "true" if theme["glow"] else "false"
        theme_bg0 = theme["bg"][0]
        theme_bg1 = theme["bg"][1]
        
        player_health = style["player_health"]
        enemy_speed = style["enemy_speed"]
        spawn_rate = style["spawn_rate"]
        game_style_id = style.get("id", "survival")
        
        mode_name = mode["name"]
        time_limit = 60 if mode_name == "Time Attack" else 0
        
        game_name = game_data["name"]
        game_genre = game_data["genre"]
        game_mechanic = game_data["mechanic"]
        game_hook = game_data.get("hook", "Master the unknown.")
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{game_name} - DeathRoll Studio</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: linear-gradient(135deg, {theme_bg0}, {theme_bg1});
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }}
        .game-wrapper {{ text-align: center; padding: 15px; }}
        .game-title {{
            font-size: 2rem;
            color: {theme_primary};
            text-shadow: {'0 0 20px ' + theme_primary if theme['glow'] else 'none'};
            font-weight: bold;
        }}
        .game-genre {{ color: {theme_secondary}; font-size: 0.9rem; }}
        .game-mechanic {{ color: {theme_accent}; font-size: 0.85rem; margin-top: 5px; }}
        canvas {{
            border: 3px solid {theme_primary};
            border-radius: 15px;
            box-shadow: {'0 0 40px ' + theme_primary if theme['glow'] else '0 0 20px rgba(0,0,0,0.5)'};
            max-width: 100%;
            background: {theme_bg0};
            display: block;
            margin: 0 auto;
        }}
        .controls {{ margin-top: 15px; color: #aaa; font-size: 0.8rem; }}
        .controls span {{
            display: inline-block;
            background: rgba(255,255,255,0.1);
            padding: 4px 10px;
            border-radius: 20px;
            margin: 0 3px;
        }}
        @media (max-width: 768px) {{
            .game-title {{ font-size: 1.3rem; }}
            canvas {{ width: 100%; height: auto; }}
        }}
    </style>
</head>
<body>
    <div class="game-wrapper">
        <div class="game-title">{game_name}</div>
        <div class="game-genre">{game_genre}</div>
        <div class="game-mechanic">⚡ {game_mechanic}</div>
        <canvas id="gameCanvas" width="900" height="600"></canvas>
        <div class="controls">
            <span>WASD</span> or <span>← → ↑ ↓</span> move &nbsp;|&nbsp; <span>SPACE</span> {game_mechanic}
        </div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        // Theme colors
        const COLORS = {{
            primary: '{theme_primary}',
            secondary: '{theme_secondary}',
            accent: '{theme_accent}',
            glow: {theme_glow}
        }};
        
        // Game state
        const state = {{
            player: {{ x: 450, y: 300, size: 25, health: {player_health}, maxHealth: {player_health} }},
            enemies: [],
            particles: [],
            bullets: [],
            score: 0,
            combo: 0,
            wave: 1,
            gameOver: false,
            started: false,
            mechanicCooldown: 0,
            maxCooldown: 90
        }};
        
        let keys = {{}};
        
        function spawnEnemy() {{
            const x = Math.random() * 880 + 10;
            const y = Math.random() * 580 + 10;
            state.enemies.push({{
                x: x, y: y,
                size: 25,
                hp: 3,
                maxHp: 3,
                speed: {enemy_speed} * (1 + state.wave * 0.1)
            }});
        }}
        
        function useMechanic() {{
            if (state.mechanicCooldown > 0) return;
            state.mechanicCooldown = state.maxCooldown;
            
            state.enemies.forEach(e => {{
                const dx = e.x - state.player.x;
                const dy = e.y - state.player.y;
                const dist = Math.hypot(dx, dy);
                if(dist < 150) {{
                    const angle = Math.atan2(dy, dx);
                    e.x += Math.cos(angle) * 80;
                    e.y += Math.sin(angle) * 80;
                    e.hp -= 2;
                }}
            }});
            addParticles(state.player.x, state.player.y, COLORS.primary, 20);
        }}
        
        function addParticles(x, y, color, count) {{
            for(let i = 0; i < count; i++) {{
                state.particles.push({{
                    x: x + (Math.random() - 0.5) * 20,
                    y: y + (Math.random() - 0.5) * 20,
                    vx: (Math.random() - 0.5) * 6,
                    vy: (Math.random() - 0.5) * 6,
                    life: 30 + Math.random() * 20,
                    maxLife: 50,
                    color: color,
                    size: 3 + Math.random() * 4
                }});
            }}
        }}
        
        function update() {{
            if (state.gameOver || !state.started) return;
            
            // Player movement
            let dx = 0, dy = 0, speed = 4.5;
            if(keys['w'] || keys['ArrowUp']) dy = -speed;
            if(keys['s'] || keys['ArrowDown']) dy = speed;
            if(keys['a'] || keys['ArrowLeft']) dx = -speed;
            if(keys['d'] || keys['ArrowRight']) dx = speed;
            if(dx && dy) {{ dx *= 0.707; dy *= 0.707; }}
            state.player.x = Math.max(20, Math.min(880, state.player.x + dx));
            state.player.y = Math.max(20, Math.min(580, state.player.y + dy));
            
            // Cooldowns
            if(state.mechanicCooldown > 0) state.mechanicCooldown--;
            
            // Spawn enemies
            if(Math.random() < 0.02 * {spawn_rate}) spawnEnemy();
            
            // Update enemies
            for(let i = 0; i < state.enemies.length; i++) {{
                const e = state.enemies[i];
                const dx2 = state.player.x - e.x;
                const dy2 = state.player.y - e.y;
                const dist = Math.hypot(dx2, dy2);
                if(dist > 0) {{
                    e.x += (dx2 / dist) * e.speed;
                    e.y += (dy2 / dist) * e.speed;
                }}
                e.x = Math.max(10, Math.min(890, e.x));
                e.y = Math.max(10, Math.min(590, e.y));
                
                // Collision
                const cd = Math.hypot(state.player.x - e.x, state.player.y - e.y);
                if(cd < state.player.size/2 + e.size/2) {{
                    state.player.health -= 10;
                    state.combo = 0;
                    if(state.player.health <= 0) {{
                        state.player.health = 0;
                        state.gameOver = true;
                        return;
                    }}
                }}
                
                // Enemy death
                if(e.hp <= 0) {{
                    state.score += 10 * (1 + Math.floor(state.combo / 10));
                    state.combo++;
                    addParticles(e.x, e.y, COLORS.secondary, 15);
                    state.enemies.splice(i,1);
                    i--;
                }}
            }}
            
            // Update particles
            for(let i = 0; i < state.particles.length; i++) {{
                const p = state.particles[i];
                p.x += p.vx; p.y += p.vy;
                p.vx *= 0.98; p.vy *= 0.98;
                p.life--;
                if(p.life <= 0) {{
                    state.particles.splice(i,1);
                    i--;
                }}
            }}
        }}
        
        function draw() {{
            // Background
            const grad = ctx.createRadialGradient(450, 300, 100, 450, 300, 500);
            grad.addColorStop(0, '{theme_bg1}');
            grad.addColorStop(1, '{theme_bg0}');
            ctx.fillStyle = grad;
            ctx.fillRect(0, 0, 900, 600);
            
            // Grid
            ctx.strokeStyle = 'rgba(255,255,255,0.03)';
            ctx.lineWidth = 1;
            for(let i = 0; i < 900; i += 50) {{
                ctx.beginPath();
                ctx.moveTo(i, 0); ctx.lineTo(i, 600);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(0, i); ctx.lineTo(900, i);
                ctx.stroke();
            }}
            
            // Draw enemies
            state.enemies.forEach(e => {{
                const grad2 = ctx.createRadialGradient(e.x-5, e.y-5, 5, e.x, e.y, e.size);
                grad2.addColorStop(0, COLORS.secondary);
                grad2.addColorStop(1, '#cc4444');
                ctx.fillStyle = grad2;
                ctx.shadowColor = COLORS.secondary;
                ctx.shadowBlur = 10;
                ctx.beginPath();
                ctx.arc(e.x, e.y, e.size/2, 0, Math.PI * 2);
                ctx.fill();
                ctx.shadowBlur = 0;
                
                // Health bar
                const hpWidth = e.size;
                ctx.fillStyle = '#444';
                ctx.fillRect(e.x - hpWidth/2, e.y - e.size/2 - 10, hpWidth, 4);
                ctx.fillStyle = '#4ecdc4';
                ctx.fillRect(e.x - hpWidth/2, e.y - e.size/2 - 10, hpWidth * (e.hp/e.maxHp), 4);
                
                ctx.fillStyle = '#fff';
                ctx.font = '18px monospace';
                ctx.fillText('👾', e.x-12, e.y-8);
            }});
            
            // Draw player
            const grad3 = ctx.createRadialGradient(state.player.x-8, state.player.y-8, 5, state.player.x, state.player.y, state.player.size);
            grad3.addColorStop(0, COLORS.primary);
            grad3.addColorStop(1, '#2a7d8f');
            ctx.fillStyle = grad3;
            ctx.shadowColor = COLORS.primary;
            ctx.shadowBlur = 20;
            ctx.beginPath();
            ctx.arc(state.player.x, state.player.y, state.player.size/2, 0, Math.PI * 2);
            ctx.fill();
            ctx.shadowBlur = 0;
            ctx.fillStyle = '#fff';
            ctx.font = '24px monospace';
            ctx.fillText('🎮', state.player.x-15, state.player.y-12);
            
            // Particles
            state.particles.forEach(p => {{
                const alpha = p.life / p.maxLife;
                ctx.globalAlpha = alpha;
                ctx.fillStyle = p.color;
                ctx.shadowColor = p.color;
                ctx.shadowBlur = 8;
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size * alpha, 0, Math.PI * 2);
                ctx.fill();
                ctx.shadowBlur = 0;
                ctx.globalAlpha = 1;
            }});
            
            // UI
            ctx.shadowBlur = 0;
            ctx.fillStyle = '#fff';
            ctx.font = 'bold 22px monospace';
            ctx.fillText('SCORE: ' + state.score, 20, 45);
            
            ctx.fillStyle = '#ff4444';
            ctx.fillRect(20, 65, 200, 14);
            ctx.fillStyle = COLORS.primary;
            ctx.fillRect(20, 65, (state.player.health / state.player.maxHealth) * 200, 14);
            
            if(state.combo > 0) {{
                ctx.fillStyle = COLORS.accent;
                ctx.font = 'bold 18px monospace';
                ctx.fillText('⚡ ' + state.combo + 'x COMBO!', 20, 120);
            }}
            
            if(state.mechanicCooldown > 0) {{
                ctx.fillStyle = 'rgba(255,255,255,0.2)';
                ctx.fillRect(20, 150, state.mechanicCooldown * 2, 6);
            }}
            ctx.fillStyle = '#888';
            ctx.font = '12px monospace';
            ctx.fillText('⚡ {game_mechanic} (SPACE)', 20, 165);
            
            // Game Over
            if(state.gameOver) {{
                ctx.fillStyle = 'rgba(0,0,0,0.7)';
                ctx.fillRect(0, 0, 900, 600);
                ctx.fillStyle = '#fff';
                ctx.font = 'bold 48px monospace';
                ctx.textAlign = 'center';
                ctx.fillText('GAME OVER', 450, 250);
                ctx.font = '24px monospace';
                ctx.fillStyle = COLORS.accent;
                ctx.fillText('Score: ' + state.score, 450, 320);
                ctx.font = '16px monospace';
                ctx.fillStyle = '#aaa';
                ctx.fillText('Press R to restart', 450, 370);
                ctx.textAlign = 'left';
            }}
            
            // Start
            if(!state.started && !state.gameOver) {{
                ctx.fillStyle = 'rgba(0,0,0,0.5)';
                ctx.fillRect(0, 0, 900, 600);
                ctx.fillStyle = '#fff';
                ctx.font = 'bold 36px monospace';
                ctx.textAlign = 'center';
                ctx.fillText('🎮 {game_name}', 450, 230);
                ctx.font = '18px monospace';
                ctx.fillStyle = COLORS.primary;
                ctx.fillText('Press SPACE to start', 450, 320);
                ctx.textAlign = 'left';
            }}
        }}
        
        function gameLoop() {{
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }}
        
        // Controls
        document.addEventListener('keydown', function(e) {{
            const key = e.key.toLowerCase();
            keys[key] = true;
            if(e.key === ' ') {{
                e.preventDefault();
                if(!state.started) {{
                    state.started = true;
                    for(let i = 0; i < 5; i++) spawnEnemy();
                }} else {{
                    useMechanic();
                }}
            }}
            if((e.key === 'r' || e.key === 'R') && state.gameOver) {{
                state.player = {{ x: 450, y: 300, size: 25, health: {player_health}, maxHealth: {player_health} }};
                state.enemies = [];
                state.particles = [];
                state.bullets = [];
                state.score = 0;
                state.combo = 0;
                state.wave = 1;
                state.gameOver = false;
                state.mechanicCooldown = 0;
                for(let i = 0; i < 5; i++) spawnEnemy();
            }}
        }});
        document.addEventListener('keyup', function(e) {{
            keys[e.key.toLowerCase()] = false;
        }});
        
        gameLoop();
    </script>
</body>
</html>'''
    
    def _create_portfolio_entry(self, game_data: Dict, license_key: str, art_url: Optional[str], html5_url: str) -> Dict:
        """Create portfolio entry"""
        return {
            "date": datetime.now().isoformat(),
            "game": game_data["name"],
            "genre": game_data["genre"],
            "mechanic": game_data["mechanic"],
            "mechanic_description": game_data.get("mechanic_description", ""),
            "description": game_data.get("description", ""),
            "hook": game_data.get("hook", ""),
            "visual_style": game_data.get("visual_style", "neon"),
            "game_mode": game_data.get("game_mode", "endless"),
            "difficulty": game_data.get("difficulty", "medium"),
            "price": game_data.get("price", 7),
            "license_key": license_key,
            "image_url": art_url or "",
            "html5_url": html5_url,
            "version": self.version,
            "status": "complete"
        }
    
    def _update_sar(self, game_data: Dict):
        """Update SAR learning system"""
        sar_path = Path("sar_analysis.json")
        
        if sar_path.exists():
            try:
                sar_data = json.loads(sar_path.read_text())
            except:
                sar_data = {"study": {"games": []}, "analysis": {}}
        else:
            sar_data = {"study": {"games": []}, "analysis": {}}
        
        # Add game
        if "study" not in sar_data:
            sar_data["study"] = {"games": []}
        if "games" not in sar_data["study"]:
            sar_data["study"]["games"] = []
        
        sar_data["study"]["games"].append({
            "name": game_data["name"],
            "genre": game_data["genre"],
            "mechanic": game_data["mechanic"],
            "visual_style": game_data.get("visual_style"),
            "game_mode": game_data.get("game_mode"),
            "timestamp": datetime.now().isoformat(),
            "price": game_data.get("price", 7)
        })
        
        # Keep last 100
        sar_data["study"]["games"] = sar_data["study"]["games"][-100:]
        
        # Update best genre
        genre_counts = {}
        for g in sar_data["study"]["games"]:
            genre = g.get("genre")
            if genre:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
        
        if genre_counts:
            sar_data["analysis"]["best_genre"] = max(genre_counts, key=genre_counts.get)
        
        # Update average price
        total_price = sum(g.get("price", 0) for g in sar_data["study"]["games"])
        if sar_data["study"]["games"]:
            sar_data["analysis"]["avg_price"] = total_price / len(sar_data["study"]["games"])
        
        sar_path.write_text(json.dumps(sar_data, indent=2))


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    bot = DeathRollStudio()
    bot.run()
