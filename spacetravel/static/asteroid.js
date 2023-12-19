import * as THREE from 'https://threejs.org/build/three.module.js';

// Constants
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const asteroidDistance = 5; // Distance from Earth

// Set up scene
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 0, 5);
const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
sceneContainer.appendChild(renderer.domElement);

// Create Earth
const earthGeometry = new THREE.SphereGeometry(1, 32, 32);
const earthTexture = new THREE.TextureLoader().load('../static/earth_daymap.jpg');
const earthMaterial = new THREE.MeshBasicMaterial({ map: earthTexture });
const earth = new THREE.Mesh(earthGeometry, earthMaterial);
scene.add(earth);

// Create Asteroid
const asteroidGeometry = new THREE.SphereGeometry(0.1, 16, 16);
const asteroidTexture = new THREE.TextureLoader().load('../static/Comet_from_331_m.png');
const asteroidMaterial = new THREE.MeshBasicMaterial({ map: asteroidTexture, transparent: true, opacity: 1, depthWrite: true });
const asteroid = new THREE.Mesh(asteroidGeometry, asteroidMaterial);
scene.add(asteroid);
asteroid.position.set(asteroidDistance, 0, 0);


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
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = - (event.clientY / window.innerHeight) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);

  // Calculate the point on the ray that is closest to the asteroid
  const closestPoint = new THREE.Vector3();
  raycaster.ray.closestPointToPoint(asteroid.position, closestPoint);

  // Check if the closest point is close to the asteroid's position
  const distanceToAsteroid = closestPoint.distanceTo(asteroid.position);

  if (distanceToAsteroid < asteroid.geometry.parameters.radius) {
    // Display popup with asteroid information
    const popupText = `Asteroid Information\nName: Asteroid 1\nDistance: ${asteroidDistance} km`;
    alert(popupText);
  }
});

// Start animation
animate();
