import * as THREE from 'https://threejs.org/build/three.module.js';

// Constants
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

let factor = null;
let asteroids = null;

// Set up scene
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 0, 5);
const renderer = new THREE.WebGLRenderer({
  alpha: true
});
renderer.setSize(window.innerWidth, window.innerHeight);
sceneContainer.appendChild(renderer.domElement);

// Create Earth
const earthGeometry = new THREE.SphereGeometry(1, 32, 32);
const earthTexture = new THREE.TextureLoader().load('../static/earth_daymap.jpg');
const earthMaterial = new THREE.MeshBasicMaterial({
  map: earthTexture,
  transparent: true,
  opacity: 0.6
});
const earth = new THREE.Mesh(earthGeometry, earthMaterial);
scene.add(earth);

// Create Asteroid Style
const asteroidTexture = new THREE.TextureLoader().load('../static/Comet_from_331_m.png');
const asteroidMaterial = new THREE.MeshBasicMaterial({
  map: asteroidTexture,
  transparent: true,
  opacity: 1,
  depthWrite: true
});
const asteroidsMesh = [];


// Animation
const animate = () => {
  requestAnimationFrame(animate);

  // Rotate Earth
  earth.rotation.y += 0.005;

  renderer.render(scene, camera);
}

// Handle window resize
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// Handle mouse click
window.addEventListener('click', (event) => {
  if (document.getElementById("filterForm").style.display == "none") {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);

    // Store the closest asteroid and its distance
    let closestAsteroid = null;
    let closestDistance = Infinity;
    let closestAsteroidIndex = -1

    asteroidsMesh.forEach((asteroid, index) => {
      const closestPoint = new THREE.Vector3();
      raycaster.ray.closestPointToPoint(asteroid.position, closestPoint);

      // Calculate distance to the asteroid
      const distanceToAsteroid = closestPoint.distanceTo(asteroid.position);

      // Check if the distance is less than the asteroid's radius
      if (distanceToAsteroid < asteroid.geometry.parameters.radius && distanceToAsteroid < closestDistance) {
        closestAsteroid = asteroid;
        closestAsteroidIndex = index;
        closestDistance = distanceToAsteroid;
      }
    });

    // If an asteroid is clicked, display its information
    if (closestAsteroid) {
      const popupText = `Asteroid Information\n
        Name: ${asteroids[closestAsteroidIndex].name}
        Type: ${asteroids[closestAsteroidIndex].type}
        Next closest approach: ${asteroids[closestAsteroidIndex].close}
        Distance: ${closestDistance.toFixed(2)*factor} km`;
      alert(popupText);
    }
  }
});

// Function to create an asteroid
function createAsteroid(asteroidData) {
  //console.log(asteroidData)
  const asteroidGeometry = new THREE.SphereGeometry(0.1, 16, 16);
  const asteroid = new THREE.Mesh(asteroidGeometry, asteroidMaterial.clone());
  //const asteroidDistance = 5; // Distance from Earth
  const position = asteroidData.position.map(coord => coord * ((1 / factor)))
  asteroid.position.set(position[0], position[1], position[2]);
  return asteroid;
}

// Start animation
animate();


// Function to import data into the module
export function importAsteroidModule(asteroidsData, newFactor) {
  asteroids = asteroidsData;
  factor = newFactor;
  //console.log('Asteroids data:', asteroids);
  //console.log('Factor:', factor);

  asteroids.forEach(asteroid => {
    //console.log('Asteroid Name:', asteroidData.name);
    const newAsteroid = createAsteroid(asteroid);
    asteroidsMesh.push(newAsteroid)
    scene.add(newAsteroid);
  });
}