
const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    scene: { preload: preload, create: create, update: update },
    scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH }
};

let player, enemies, dungeon = [], turn = 0, hp = 10, maxHp = 10, gold = 0;
let gameOver = false, mechanicCooldown = 0;
let graphics, uiText, mechanicText;

function preload() {
    this.load.image('player', 'assets/player.png');
    this.load.image('enemy', 'assets/enemy.png');
    this.load.image('coin', 'assets/coin.png');
    this.load.image('bg', 'assets/bg.png');
}

function create() {
    if (this.textures.exists('bg')) {
        this.add.image(400, 300, 'bg');
    } else {
        const g = this.add.graphics();
        g.fillStyle(0x1a1a2e).fillRect(0, 0, 800, 600);
    }
    graphics = this.add.graphics();
    generateDungeon();
    drawDungeon();

    uiText = this.add.text(20, 20, 'HP: '+hp+'/'+maxHp+'  Gold: '+gold, { fontSize: '20px', fill: '#fff' });
    this.add.text(20, 60, 'Turn: '+turn, { fontSize: '20px', fill: '#fff' });
    mechanicText = this.add.text(20, 100, '⚡ Void Step (SPACE) - heal +3', { fontSize: '18px', fill: '#ffd93d' });

    this.input.keyboard.on('keydown-W', () => movePlayer(0,-1));
    this.input.keyboard.on('keydown-A', () => movePlayer(-1,0));
    this.input.keyboard.on('keydown-S', () => movePlayer(0,1));
    this.input.keyboard.on('keydown-D', () => movePlayer(1,0));
    this.input.keyboard.on('keydown-SPACE', useMechanic, this);
}

function generateDungeon() {
    const size = 10;
    dungeon = [];
    for (let y=0; y<size; y++) {
        const row = [];
        for (let x=0; x<size; x++) row.push(Math.random() < 0.25 ? 1 : 0);
        dungeon.push(row);
    }
    dungeon[1][1] = 0;
    dungeon[size-2][size-2] = 0;
    player = {x:1, y:1};
    enemies = [];
    for (let i=0; i<4; i++) {
        let ex, ey;
        do { ex = Math.floor(Math.random()*size); ey = Math.floor(Math.random()*size); }
        while (dungeon[ey][ex] !== 0 || (ex===1 && ey===1));
        enemies.push({x:ex, y:ey, hp:3, maxHp:3});
    }
    // Gold chest
    let gx, gy;
    do { gx = Math.floor(Math.random()*size); gy = Math.floor(Math.random()*size); }
    while (dungeon[gy][gx] !== 0 || (gx===1 && gy===1));
    enemies.push({x:gx, y:gy, hp:0, gold:10});
}

function drawDungeon() {
    graphics.clear();
    const size = 10, cellSize = 60;
    const offsetX = (800 - size*cellSize)/2, offsetY = (600 - size*cellSize)/2;
    for (let y=0; y<size; y++) {
        for (let x=0; x<size; x++) {
            const px = offsetX + x*cellSize, py = offsetY + y*cellSize;
            if (dungeon[y][x] === 1) {
                graphics.fillStyle(0x444444, 1);
            } else {
                graphics.fillStyle(0x2a2a4a, 1);
            }
            graphics.fillRect(px, py, cellSize, cellSize);
            graphics.lineStyle(1, 0x555555);
            graphics.strokeRect(px, py, cellSize, cellSize);
            enemies.forEach(e => {
                if (e.x === x && e.y === y) {
                    if (e.hp > 0) {
                        graphics.fillStyle(0xff4444, 1);
                        graphics.fillCircle(px+cellSize/2, py+cellSize/2, 15);
                    } else {
                        graphics.fillStyle(0xffd93d, 1);
                        graphics.fillCircle(px+cellSize/2, py+cellSize/2, 12);
                    }
                }
            });
            if (player.x === x && player.y === y) {
                graphics.fillStyle(0x4ecdc4, 1);
                graphics.fillCircle(px+cellSize/2, py+cellSize/2, 20);
            }
        }
    }
}

function useMechanic() {
    if (gameOver || mechanicCooldown > 0) return;
    mechanicCooldown = 60;
    hp = Math.min(maxHp, hp + 3);
    uiText.setText('HP: '+hp+'/'+maxHp+'  Gold: '+gold);
    this.cameras.main.flash(100, 0, 255, 0);
}

function movePlayer(dx, dy) {
    if (gameOver) return;
    const nx = player.x + dx, ny = player.y + dy;
    if (nx<0 || nx>=10 || ny<0 || ny>=10) return;
    if (dungeon[ny][nx] === 1) return;
    let enemyHere = enemies.find(e => e.x === nx && e.y === ny);
    if (enemyHere) {
        if (enemyHere.hp > 0) {
            enemyHere.hp--;
            if (enemyHere.hp <= 0) {
                gold += 5;
                uiText.setText('HP: '+hp+'/'+maxHp+'  Gold: '+gold);
                enemies = enemies.filter(e => e !== enemyHere);
            } else {
                hp--;
                if (hp <= 0) {
                    gameOver = true;
                    this.add.text(300, 250, 'GAME OVER', { fontSize: '64px', fill: '#ff0000' });
                    this.add.text(300, 320, 'Press R to restart', { fontSize: '32px', fill: '#fff' });
                    this.input.keyboard.on('keydown-R', () => { this.scene.restart(); });
                }
            }
        } else {
            gold += enemyHere.gold || 10;
            enemies = enemies.filter(e => e !== enemyHere);
        }
        turn++;
        uiText.setText('HP: '+hp+'/'+maxHp+'  Gold: '+gold);
        drawDungeon();
        return;
    }
    player.x = nx; player.y = ny;
    turn++;
    enemies.forEach(e => {
        if (e.hp <= 0) return;
        const dirs = [[1,0],[-1,0],[0,1],[0,-1]];
        const shuffled = dirs.sort(() => Math.random() - 0.5);
        for (let d of shuffled) {
            const ex = e.x + d[0], ey = e.y + d[1];
            if (ex<0 || ex>=10 || ey<0 || ey>=10) continue;
            if (dungeon[ey][ex] === 1) continue;
            if (ex === player.x && ey === player.y) {
                hp--;
                if (hp <= 0) {
                    gameOver = true;
                    this.add.text(300, 250, 'GAME OVER', { fontSize: '64px', fill: '#ff0000' });
                    this.add.text(300, 320, 'Press R to restart', { fontSize: '32px', fill: '#fff' });
                    this.input.keyboard.on('keydown-R', () => { this.scene.restart(); });
                }
                break;
            }
            if (!enemies.some(oe => oe.x === ex && oe.y === ey)) {
                e.x = ex; e.y = ey;
                break;
            }
        }
    });
    uiText.setText('HP: '+hp+'/'+maxHp+'  Gold: '+gold);
    drawDungeon();
}

const game = new Phaser.Game(config);
