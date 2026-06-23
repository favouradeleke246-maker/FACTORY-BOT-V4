
const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    physics: { default: 'arcade', arcade: { debug: false } },
    scene: { preload: preload, create: create, update: update },
    scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH }
};

let player, cursors, enemies, bullets, powerups, scoreText, healthText, waveText, mechanicText;
let score = 0, health = 100, wave = 1, enemiesDefeated = 0;
let gameOver = false, bossActive = false;
let mechanicCooldown = 0;

function preload() {
    this.load.image('player', 'assets/player.png');
    this.load.image('enemy', 'assets/enemy.png');
    this.load.image('coin', 'assets/coin.png');
    this.load.image('powerup', 'assets/powerup.png');
    this.load.image('bg', 'assets/bg.png');
}

function create() {
    this.add.image(400, 300, 'bg');
    player = this.physics.add.sprite(400, 500, 'player');
    player.setCollideWorldBounds(true);
    player.setScale(0.8);
    cursors = this.input.keyboard.createCursorKeys();
    enemies = this.physics.add.group();
    bullets = this.physics.add.group();
    powerups = this.physics.add.group();

    this.input.keyboard.on('keydown-SPACE', useMechanic, this);
    this.input.on('pointerdown', useMechanic, this);

    this.physics.add.overlap(bullets, enemies, (bullet, enemy) => {
        bullet.destroy();
        enemy.destroy();
        score += 10;
        enemiesDefeated++;
        updateUI();
        if (enemiesDefeated % 10 === 0) {
            wave++;
            if (wave % 3 === 0) spawnBoss.call(this);
        }
    });
    this.physics.add.overlap(player, enemies, (p, enemy) => {
        health -= 20;
        enemy.destroy();
        updateUI();
        if (health <= 0) { gameOver = true; showGameOver.call(this); }
    });
    this.physics.add.overlap(player, powerups, (p, pw) => {
        pw.destroy();
        health = Math.min(health + 20, 100);
        updateUI();
    });

    scoreText = this.add.text(16, 16, 'Score: 0', { fontSize: '28px', fill: '#fff' });
    healthText = this.add.text(16, 56, 'HP: 100', { fontSize: '28px', fill: '#fff' });
    waveText = this.add.text(16, 96, 'Wave: 1', { fontSize: '28px', fill: '#fff' });
    mechanicText = this.add.text(16, 136, '⚡ Void Step (SPACE)', { fontSize: '20px', fill: '#ffd93d' });

    this.time.addEvent({ delay: 1000, callback: spawnEnemy, callbackScope: this, loop: true });
    this.time.addEvent({ delay: 5000, callback: spawnPowerup, callbackScope: this, loop: true });
}

function update(time) {
    if (gameOver) return;
    let vx = 0, vy = 0;
    if (cursors.left.isDown) vx = -300;
    else if (cursors.right.isDown) vx = 300;
    if (cursors.up.isDown) vy = -300;
    else if (cursors.down.isDown) vy = 300;
    player.setVelocity(vx, vy);
    if (mechanicCooldown > 0) mechanicCooldown--;
    if (bossActive) {
        const boss = enemies.getChildren().find(e => e.boss);
        if (boss) boss.x += Math.sin(time/1000) * 2;
    }
}

function useMechanic() {
    if (gameOver || mechanicCooldown > 0) return;
    mechanicCooldown = 120;
    enemies.children.iterate(e => {
        e.setVelocityY(e.body.velocity.y * 0.3);
        const dx = e.x - player.x;
        const dy = e.y - player.y;
        const dist = Math.hypot(dx, dy);
        if (dist < 150) {
            e.x += dx * 0.5;
            e.y += dy * 0.5;
        }
    });
    this.cameras.main.shake(100);
    this.cameras.main.flash(100, 255, 255, 255);
}

function spawnEnemy() {
    if (gameOver || bossActive) return;
    const x = Phaser.Math.Between(50, 750);
    const enemy = enemies.create(x, 0, 'enemy');
    enemy.setVelocityY(100 + wave * 20);
    enemy.setScale(0.6 + wave * 0.02);
}

function spawnBoss() {
    bossActive = true;
    const boss = enemies.create(400, 50, 'enemy');
    boss.setScale(2);
    boss.boss = true;
    boss.hp = 20 + wave * 5;
    boss.setVelocityX(100);
    boss.setVelocityY(20);
}

function spawnPowerup() {
    if (gameOver) return;
    const x = Phaser.Math.Between(50, 750);
    const y = Phaser.Math.Between(50, 550);
    const pw = powerups.create(x, y, 'powerup');
    pw.setScale(0.5);
}

function updateUI() {
    scoreText.setText('Score: ' + score);
    healthText.setText('HP: ' + health);
    waveText.setText('Wave: ' + wave);
}

function showGameOver() {
    this.add.text(300, 250, 'GAME OVER', { fontSize: '64px', fill: '#ff0000' });
    this.add.text(300, 320, 'Press R to restart', { fontSize: '32px', fill: '#fff' });
    this.input.keyboard.on('keydown-R', () => { this.scene.restart(); });
}

const game = new Phaser.Game(config);
