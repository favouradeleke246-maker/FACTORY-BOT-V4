
const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    physics: { default: 'arcade', arcade: { debug: false } },
    scene: { preload: preload, create: create, update: update },
    scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH }
};

let player, monsters, keys, cursors, stealthBar, foundKeys = 0, totalKeys = 5;
let gameOver = false, escaped = false;

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
    cursors = this.input.keyboard.createCursorKeys();

    monsters = this.physics.add.group();
    this.time.addEvent({ delay: 2000, callback: spawnMonster, callbackScope: this, loop: true });

    keys = this.physics.add.staticGroup();
    for (let i=0; i<totalKeys; i++) {
        const x = Phaser.Math.Between(50, 750);
        const y = Phaser.Math.Between(50, 550);
        keys.create(x, y, 'coin');
    }
    this.physics.add.overlap(player, keys, collectKey, null, this);
    this.physics.add.overlap(player, monsters, hitMonster, null, this);

    stealthBar = this.add.graphics();
    stealthBar.fillStyle(0x00ff00, 1);
    stealthBar.fillRect(20, 60, 200, 20);

    this.add.text(20, 20, 'Stealth', { fontSize: '20px', fill: '#fff' });
    this.add.text(20, 100, 'Keys: 0/'+totalKeys, { fontSize: '20px', fill: '#fff' });
}

function update() {
    if (gameOver) return;
    if (cursors.left.isDown) { player.x -= 4; }
    else if (cursors.right.isDown) { player.x += 4; }
    if (cursors.up.isDown) { player.y -= 4; }
    else if (cursors.down.isDown) { player.y += 4; }
    // Reduce stealth if monsters are near
    monsters.children.iterate(mon => {
        const dist = Phaser.Math.Distance.Between(player.x, player.y, mon.x, mon.y);
        if (dist < 150) {
            // decrease stealth bar (simulate)
            // For demo, just check if too close -> game over
            if (dist < 50) {
                gameOver = true;
                this.add.text(300, 250, 'CAUGHT!', { fontSize: '64px', fill: '#ff0000' });
            }
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
    this.add.text(20, 130, 'Keys: '+foundKeys+'/'+totalKeys, { fontSize: '20px', fill: '#fff' }).setDepth(1);
    if (foundKeys === totalKeys) {
        escaped = true;
        gameOver = true;
        this.add.text(300, 250, 'YOU ESCAPED!', { fontSize: '64px', fill: '#00ff00' });
    }
}

function hitMonster(player, mon) {
    // Flash effect, but not immediate game over – we use proximity logic above.
    // For simplicity, we also trigger game over on direct collision.
    gameOver = true;
    this.add.text(300, 250, 'CAUGHT!', { fontSize: '64px', fill: '#ff0000' });
}

const game = new Phaser.Game(config);
