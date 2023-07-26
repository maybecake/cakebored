import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { STLExporter } from "three/addons/exporters/STLExporter.js";

function createPerspectiveCamera() {
  return new THREE.PerspectiveCamera(
    60,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
}

function createOrthoCamera() {
  const width = 10;
  const height = (window.innerHeight / window.innerWidth) * width;
  return new THREE.OrthographicCamera(
    width / -2,
    width / 2,
    height / 2,
    height / -2,
    0.1,
    1000
  );
}

const scene = new THREE.Scene();
const camera = createPerspectiveCamera();

const renderer = new THREE.WebGLRenderer({
  antialias: true,
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);

function createPlane(size: number) {
  const loader = new THREE.TextureLoader();
  const texture = loader.load("checker.png");
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.magFilter = THREE.NearestFilter;
  const repeats = size;
  texture.repeat.set(repeats, repeats);

  const planeGeo = new THREE.PlaneGeometry(size, size);
  const planeMat = new THREE.MeshPhongMaterial({
    map: texture,
    side: THREE.DoubleSide,
  });
  const mesh = new THREE.Mesh(planeGeo, planeMat);
  mesh.receiveShadow = true;
  mesh.rotation.x = Math.PI * -0.5;
  mesh.position.y = -0.1;
  return mesh;
}

function createCube() {
  const geometry = new THREE.BoxGeometry(1, 1, 1);
  const material = new THREE.MeshStandardMaterial({
    color: 0x306050,
    // flatShading: true,
    polygonOffset: true,
    polygonOffsetFactor: 1, // positive value pushes polygon further away
    polygonOffsetUnits: 1,
  });
  const cube = new THREE.Mesh(geometry, material);
  cube.castShadow = true;
  cube.receiveShadow = true;
  return cube;
}

function createWireframe() {
  const geo = new THREE.EdgesGeometry(cube.geometry); // or WireframeGeometry
  const mat = new THREE.LineBasicMaterial({
    color: 0xffffff,
    linewidth: 2,
  });
  const wireframe = new THREE.LineSegments(geo, mat);
  return wireframe;
}

function positionObjects(objs: Array<THREE.Object3D>, pos: THREE.Vector3) {
  for (const o of objs) {
    o.position.copy(pos);
  }
}

function rotateObjects(
  objs: Array<THREE.Object3D>,
  x: number,
  y: number,
  z: number
) {
  for (const o of objs) {
    o.rotateX(x);
    o.rotateY(y);
    o.rotateZ(z);
  }
}

scene.add(createPlane(12));
const cube = createCube();
scene.add(cube);
const wireframe = createWireframe();
scene.add(wireframe);

positionObjects([cube, wireframe], new THREE.Vector3(0.6, 0.6, 0.6));

scene.add(new THREE.AxesHelper(2));

camera.position.set(2, 2, 5);
const orbitControls = new OrbitControls(camera, renderer.domElement);
orbitControls.target.copy(cube.position);

scene.add(new THREE.AmbientLight(0x404040)); // soft white light

const color = 0xffffff;
const intensity = 1;
const light = new THREE.DirectionalLight(color, intensity);
light.castShadow = true;
light.position.set(0, 10, 0);
light.target.position.copy(cube.position);
light.shadow.mapSize.width = 2048;
light.shadow.mapSize.height = 2048;
scene.add(light);
scene.add(light.target);

function animate() {
  requestAnimationFrame(animate);
  rotateObjects([cube, wireframe], 0.01, 0.02, 0.03);
  renderer.render(scene, camera);
}

animate();

// const link = document.createElement("a");
// link.style.display = "none";
// document.body.appendChild(link);

// function save(blob, filename) {
//   link.href = URL.createObjectURL(blob);
//   link.download = filename;
//   link.click();
// }

// function saveArrayBuffer(buffer, filename) {
//   save(new Blob([buffer], { type: "application/octet-stream" }), filename);
// }

// const exporter = new STLExporter();
// const result = exporter.parse(cube, { binary: true });
// saveArrayBuffer(result, "box.stl");