// Home screen elements
const homeScreen = document.getElementById('homeScreen');
const startButton = document.getElementById('startButton');

// Game variables
let scene, camera, renderer, player, bullets, enemies;
let gameStarted = false;

// Initialize the game
function initGame() {
    // Initialize scene, camera, and renderer
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    // Lighting
    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(10, 10, 10);
    scene.add(light);

    // Create player (a simple cube)
    const playerGeometry = new THREE.BoxGeometry(1, 1, 1);
    const playerMaterial = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    player = new THREE.Mesh(playerGeometry, playerMaterial);
    scene.add(player);
    player.position.z = -5;

    // Bullets array
    bullets = [];
    enemies = [];
}

// Start game function
function startGame() {
    homeScreen.style.display = 'none';
    gameStarted = true;
    
    // Only initialize game elements if not already done
    if (!scene) {
        initGame();
        animate();
    }
}

// Event listener for start button
startButton.addEventListener('click', startGame);

// Create an enemy (another cube)
function createEnemy() {
    const enemyGeometry = new THREE.BoxGeometry(1, 1, 1);
    const enemyMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });
    const enemy = new THREE.Mesh(enemyGeometry, enemyMaterial);
    enemy.position.x = (Math.random() - 0.5) * 10;
    enemy.position.y = (Math.random() - 0.5) * 10;
    enemy.position.z = -20;
    scene.add(enemy);
    return enemy;
}

function spawnEnemies() {
    if (Math.random() < 0.02) {
        enemies.push(createEnemy());
    }
}

// Bullet class
class Bullet {
    constructor(position) {
        const bulletGeometry = new THREE.SphereGeometry(0.1, 8, 8);
        const bulletMaterial = new THREE.MeshBasicMaterial({ color: 0xffff00 });
        this.mesh = new THREE.Mesh(bulletGeometry, bulletMaterial);
        this.mesh.position.copy(position);
        scene.add(this.mesh);
    }

    update() {
        this.mesh.position.z -= 0.2; // Move bullet forward
    }
}

// Basic controls using keyboard
const keys = {};
window.addEventListener('keydown', (e) => {
    keys[e.key] = true;
    
    // Prevent spacebar from scrolling the page
    if (e.key === ' ' && gameStarted) {
        e.preventDefault();
        shoot();
    }
});
window.addEventListener('keyup', (e) => {
    keys[e.key] = false;
});

// Player movement
function movePlayer() {
    if (keys['ArrowUp']) player.position.y += 0.1;
    if (keys['ArrowDown']) player.position.y -= 0.1;
    if (keys['ArrowLeft']) player.position.x -= 0.1;
    if (keys['ArrowRight']) player.position.x += 0.1;
}

// Shooting mechanics
function shoot() {
    if (!gameStarted) return;
    bullets.push(new Bullet(player.position.clone()));
}

// Enemy collision detection with bullets
function detectCollisions() {
    enemies.forEach((enemy, enemyIndex) => {
        bullets.forEach((bullet, bulletIndex) => {
            const distance = enemy.position.distanceTo(bullet.mesh.position);
            if (distance < 1) {
                scene.remove(enemy);
                scene.remove(bullet.mesh);
                enemies.splice(enemyIndex, 1); // Remove enemy
                bullets.splice(bulletIndex, 1); // Remove bullet
            }
        });
    });
}

// Game over condition (if enemy reaches player)
function checkGameOver() {
    enemies.forEach((enemy) => {
        if (enemy.position.distanceTo(player.position) < 1) {
            alert("Game Over!");
            location.reload();
        }
    });
}

// Game loop
function animate() {
    if (!gameStarted) return;
    
    requestAnimationFrame(animate);
    movePlayer();

    bullets.forEach((bullet, index) => {
        bullet.update();
        if (bullet.mesh.position.z < -50) {
            scene.remove(bullet.mesh); // Remove bullets that are far off screen
            bullets.splice(index, 1);
        }
    });

    enemies.forEach((enemy) => {
        enemy.position.z += 0.05; // Move enemies towards the player
    });

    spawnEnemies();
    detectCollisions();
    checkGameOver();

    renderer.render(scene, camera);
}

// Handle window resize
window.addEventListener('resize', () => {
    if (camera && renderer) {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }
});
