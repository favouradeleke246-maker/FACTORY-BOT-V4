
const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    physics: { default: 'arcade', arcade: { debug: false } },
    scene: { preload: preload, create: create, update: update },
    scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH }
};

let player, monsters, keys, cursors, foundKeys = 0, totalKeys = 5;
let gameOver = false, stealth = 100;

function preload() {
    this.load.image('player', 'assets/player.png');
    this.load.image('enemy', 'assets/enemy.png');
    this.load.image('coin', 'assets/coin.png');
    this.load.image('bg', 'assets/bg.png');
}

function create() {
    this.add.image(400, 300, 'bg');
    player = this.physics.add.sprite(400, 300, 'player');
    player.setCollideWorldBounds(true);
    player.setScale(0.7);
    cursors = this.input.keyboard.createCursorKeys();

    monsters = this.physics.add.group();
    this.time.addEvent({ delay: 1500, callback: spawnMonster, callbackScope: this, loop: true });

    keys = this.physics.add.staticGroup();
    for (let i=0; i<totalKeys; i++) {
        const x = Phaser.Math.Between(50, 750);
        const y = Phaser.Math.Between(50, 550);
        keys.create(x, y, 'coin');
    }
    this.physics.add.overlap(player, keys, collectKey, null, this);
    this.physics.add.overlap(player, monsters, hitMonster, null, this);

    this.add.text(20, 20, 'Stealth', { fontSize: '20px', fill: '#fff' });
    this.add.text(20, 60, 'Keys: 0/'+totalKeys, { fontSize: '20px', fill: '#fff' });
    // Simple stealth bar (graphics)
    this.stealthBar = this.add.graphics();
    this.updateStealthBar();
}

function update() {
    if (gameOver) return;
    if (cursors.left.isDown) { player.x -= 4; }
    else if (cursors.right.isDown) { player.x += 4; }
    if (cursors.up.isDown) { player.y -= 4; }
    else if (cursors.down.isDown) { player.y += 4; }
    // Stealth decreases near monsters
    monsters.children.iterate(mon => {
        const dist = Phaser.Math.Distance.Between(player.x, player.y, mon.x, mon.y);
        if (dist < 150) {
            stealth -= 0.5;
            if (stealth < 0) {
                gameOver = true;
                this.add.text(300, 250, 'CAUGHT!', { fontSize: '64px', fill: '#ff0000' });
                this.add.text(300, 320, 'Press R to restart', { fontSize: '32px', fill: '#fff' });
                this.input.keyboard.on('keydown-R', () => { this.scene.restart(); });
            }
            this.updateStealthBar();
        }
    });
}

function spawnMonster() {
    const x = Phaser.Math.Between(50, 750);
    const y = Phaser.Math.Between(50, 550);
    const mon = monsters.create(x, y, 'enemy');
    mon.setScale(0.7);
}

function collectKey(player, key) {
    key.destroy();
    foundKeys++;
    this.children.list.forEach(c => {
        if (c.text && c.text.startsWith('Keys:')) c.setText('Keys: '+foundKeys+'/'+totalKeys);
    });
    if (foundKeys === totalKeys) {
        gameOver = true;
        this.add.text(300, 250, 'YOU ESCAPED!', { fontSize: '64px', fill: '#00ff00' });
        this.add.text(300, 320, 'Press R to restart', { fontSize: '32px', fill: '#fff' });
        this.input.keyboard.on('keydown-R', () => { this.scene.restart(); });
    }
}

function hitMonster(player, mon) {
    gameOver = true;
    this.add.text(300, 250, 'CAUGHT!', { fontSize: '64px', fill: '#ff0000' });
    this.add.text(300, 320, 'Press R to restart', { fontSize: '32px', fill: '#fff' });
    this.input.keyboard.on('keydown-R', () => { this.scene.restart(); });
}

function updateStealthBar() {
    this.stealthBar.clear();
    const color = stealth > 50 ? 0x00ff00 : 0xff0000;
    this.stealthBar.fillStyle(color, 1);
    this.stealthBar.fillRect(20, 40, Math.max(0, stealth * 2), 20);
}

const game = new Phaser.Game(config);
