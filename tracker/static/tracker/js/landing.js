const container = document.getElementById('globeContainer');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);

// Lighting
const light = new THREE.PointLight(0xffffff, 1);
light.position.set(5, 5, 5);
scene.add(light);

// Earth - Closest & Bigger
const earthGeometry = new THREE.SphereGeometry(1, 64, 64);
const earthMaterial = new THREE.MeshStandardMaterial({
    color: 0x4da8da,
    wireframe: true
});
const earth = new THREE.Mesh(earthGeometry, earthMaterial);
earth.position.z = 2;
scene.add(earth);

// Other Planets (no labels)
const planetObjects = [];

// Example planet data (required if used)
const planets = [
    { name: "Mars", size: 0.5, color: 0xff4500, x: 2.5 },
    { name: "Venus", size: 0.6, color: 0xffcc00, x: -3 },
    { name: "Jupiter", size: 0.8, color: 0xffa07a, x: 4 }
];

planets.forEach(planet => {
    const geometry = new THREE.SphereGeometry(planet.size, 32, 32);
    const material = new THREE.MeshStandardMaterial({
        color: planet.color,
        wireframe: true
    });
    const sphere = new THREE.Mesh(geometry, material);
    sphere.position.x = planet.x;
    scene.add(sphere);
    planetObjects.push(sphere);
});

camera.position.z = 5;

// Rotation Targets
let targetRotationX = 0;
let targetRotationY = 0;

// Animation
function animate() {
    requestAnimationFrame(animate);

    // Smooth rotation
    scene.rotation.x += (targetRotationX - scene.rotation.x) * 0.05;
    scene.rotation.y += (targetRotationY - scene.rotation.y) * 0.05;

    renderer.render(scene, camera);
}
animate();

// Mouse Movement for Rotation
container.addEventListener('mousemove', (event) => {
    const x = (event.clientX / container.clientWidth) * 2 - 1;
    const y = (event.clientY / container.clientHeight) * 2 - 1;

    targetRotationY = x * Math.PI * 0.3;
    targetRotationX = y * Math.PI * 0.3;
});

// Hover Effect for Earth
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let hovered = false;

container.addEventListener('mousemove', (event) => {
    mouse.x = (event.clientX / container.clientWidth) * 2 - 1;
    mouse.y = -(event.clientY / container.clientHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObject(earth);

    if (intersects.length > 0) {
        if (!hovered) {
            earth.scale.set(1.2, 1.2, 1.2);
            container.style.cursor = 'pointer';
            hovered = true;
        }
    } else {
        if (hovered) {
            earth.scale.set(1, 1, 1);
            container.style.cursor = 'default';
            hovered = false;
        }
    }
});

// Earth Click → Home Page
container.addEventListener('click', () => {
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObject(earth);
    if (intersects.length > 0) {
        window.location.href = '/home';
    }
});

// Handle Resize
window.addEventListener('resize', () => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
});
