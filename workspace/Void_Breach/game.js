
const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    physics: { default: 'arcade', arcade: { debug: false } },
    scene: { preload: preload, create: create, update: update },
    scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH }
};

let player, cursors, enemies, bullets, powerups, scoreText, healthText, waveText;
let score = 0, health = 100, wave = 1, enemiesDefeated = 0;
let gameOver = false, bossActive = false;
let playerSpeed = 300;
let shootTimer = 0;

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

    this.physics.add.overlap(bullets, enemies, (bullet, enemy) => {
        bullet.destroy();
        enemy.destroy();
        score += 10;
        enemiesDefeated++;
        updateUI();
        if (enemiesDefeated % 10 === 0) {
            wave++;
            waveText.setText('Wave: ' + wave);
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

    this.input.keyboard.on('keydown-SPACE', shoot, this);
    this.input.on('pointerdown', shoot, this);

    // Spawn enemies every second
    this.time.addEvent({ delay: 1000, callback: spawnEnemy, callbackScope: this, loop: true });
    // Spawn powerups occasionally
    this.time.addEvent({ delay: 5000, callback: spawnPowerup, callbackScope: this, loop: true });
}

function update(time) {
    if (gameOver) return;
    // Movement
    let vx = 0, vy = 0;
    if (cursors.left.isDown) vx = -playerSpeed;
    else if (cursors.right.isDown) vx = playerSpeed;
    if (cursors.up.isDown) vy = -playerSpeed;
    else if (cursors.down.isDown) vy = playerSpeed;
    player.setVelocity(vx, vy);
    // Auto-shoot if holding space? We'll use keydown.
    // Boss logic
    if (bossActive) {
        const boss = enemies.getChildren().find(e => e.boss);
        if (boss) {
            // Move boss left-right
            boss.x += Math.sin(time/1000) * 2;
        }
    }
}

function spawnEnemy() {
    if (gameOver) return;
    if (bossActive) return; // No regular enemies during boss
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
    // Move down slowly
    boss.setVelocityY(20);
    // Boss health bar (we'll add later)
}

function spawnPowerup() {
    if (gameOver) return;
    const x = Phaser.Math.Between(50, 750);
    const y = Phaser.Math.Between(50, 550);
    const pw = powerups.create(x, y, 'powerup');
    pw.setScale(0.5);
}

function shoot() {
    if (gameOver) return;
    const bullet = bullets.create(player.x, player.y - 20, 'coin');
    bullet.setVelocityY(-400);
    bullet.setScale(0.2);
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
