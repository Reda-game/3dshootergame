// Scorebeheer en instellingen
let score = 0;
let highScore = localStorage.getItem('highScore') || 0;
let gameStarted = false;
let isGameOver = false;
let sensitivity = parseFloat(document.getElementById('sensitivity').value);

// HTML elementen ophalen
const scoreText = document.getElementById('score');
const gameOverBanner = document.getElementById('gameOverBanner');

// Toon/verberg instellingenmenu
document.getElementById('settingsToggle').addEventListener('click', () => {
  const controls = document.getElementById('controls');
  controls.style.display = (controls.style.display === 'block') ? 'none' : 'block';
});

// Gevoeligheid aanpassen
document.getElementById('sensitivity').addEventListener('input', (e) => {
  sensitivity = parseFloat(e.target.value);
});

// Reset highscore
function resetHighScore() {
  localStorage.setItem('highScore', 0);
  alert('High score reset.');
}

// Start de game
document.getElementById('startBtn').addEventListener('click', () => {
  document.getElementById('startScreen').style.display = 'none';
  gameStarted = true;
  animate();
});

// Three.js setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Lichtbron toevoegen
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(10, 10, 10);
scene.add(light);

// Spelerobject
const player = new THREE.Mesh(
  new THREE.BoxGeometry(1, 1, 1),
  new THREE.MeshBasicMaterial({ color: 0x00ff00 })
);
player.position.z = -5;
scene.add(player);

const bullets = [];
let enemies = [];

// Maak vijand aan
function createEnemy() {
  const enemy = new THREE.Mesh(
    new THREE.BoxGeometry(1, 1, 1),
    new THREE.MeshBasicMaterial({ color: 0xff0000 })
  );
  enemy.position.x = (Math.random() - 0.5) * 10;
  enemy.position.y = (Math.random() - 0.5) * 10;
  enemy.position.z = -20;
  scene.add(enemy);
  return enemy;
}

// Vijanden periodiek spawnen
function spawnEnemies() {
  if (Math.random() < 0.02) enemies.push(createEnemy());
}

// Klasse voor kogelobjecten
class Bullet {
  constructor(position) {
    this.mesh = new THREE.Mesh(
      new THREE.SphereGeometry(0.1, 8, 8),
      new THREE.MeshBasicMaterial({ color: 0xffff00 })
    );
    this.mesh.position.copy(position);
    scene.add(this.mesh);
  }

  update() {
    this.mesh.position.z -= 0.2;
  }
}

// Bewegingstoetsen bijhouden
const keys = {};
window.addEventListener('keydown', (e) => keys[e.key] = true);
window.addEventListener('keyup', (e) => keys[e.key] = false);

// Spelerbeweging op basis van pijltjestoetsen
function movePlayer() {
  if (keys['ArrowUp']) player.position.y += sensitivity;
  if (keys['ArrowDown']) player.position.y -= sensitivity;
  if (keys['ArrowLeft']) player.position.x -= sensitivity;
  if (keys['ArrowRight']) player.position.x += sensitivity;

  // Speler binnen grenzen houden
  player.position.x = THREE.MathUtils.clamp(player.position.x, -5, 5);
  player.position.y = THREE.MathUtils.clamp(player.position.y, -3.5, 3.5);
}

// Functie om te schieten
function shoot() {
  bullets.push(new Bullet(player.position.clone()));
}

// Spatiebalk om te schieten
window.addEventListener('keydown', (e) => {
  if (e.key === ' ') shoot();
});

// Detecteer botsingen tussen kogels en vijanden
function detectCollisions() {
  enemies.forEach((enemy, ei) => {
    bullets.forEach((bullet, bi) => {
      if (enemy.position.distanceTo(bullet.mesh.position) < 1) {
        scene.remove(enemy);
        scene.remove(bullet.mesh);
        enemies.splice(ei, 1);
        bullets.splice(bi, 1);
        score++;
        scoreText.textContent = `Score: ${score}`;
        if (score > highScore) {
          highScore = score;
          localStorage.setItem('highScore', highScore);
        }
      }
    });
  });
}

// Controleer of speler geraakt is
function checkGameOver() {
  if (isGameOver) return true;

  for (let enemy of enemies) {
    if (enemy.position.distanceTo(player.position) < 1) {
      isGameOver = true;
      gameOverBanner.style.display = 'block';
      setTimeout(() => location.reload(), 1000);
      return true;
    }
  }

  return false;
}

// Animatielus van het spel
function animate() {
  if (!gameStarted || isGameOver) return;

  requestAnimationFrame(animate);
  movePlayer();

  bullets.forEach((bullet, index) => {
    bullet.update();
    if (bullet.mesh.position.z < -50) {
      scene.remove(bullet.mesh);
      bullets.splice(index, 1);
    }
  });

  enemies.forEach((enemy) => enemy.position.z += 0.05);
  spawnEnemies();
  detectCollisions();
  if (checkGameOver()) return;

  renderer.render(scene, camera);
}
