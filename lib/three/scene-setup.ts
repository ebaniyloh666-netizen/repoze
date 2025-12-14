import * as THREE from 'three';

/**
 * Three.js Scene Setup for 3D RTS Game
 * Initializes camera, renderer, and lighting for a real-time strategy game environment
 */

interface SceneSetupConfig {
  canvas?: HTMLCanvasElement;
  width?: number;
  height?: number;
  pixelRatio?: number;
  antialias?: boolean;
  shadowMap?: boolean;
  shadowMapSize?: number;
}

export class RTSSceneSetup {
  scene: THREE.Scene;
  camera: THREE.PerspectiveCamera;
  renderer: THREE.WebGLRenderer;
  lights: {
    ambientLight: THREE.AmbientLight;
    directionalLight: THREE.DirectionalLight;
    pointLights: THREE.PointLight[];
  };

  constructor(config: SceneSetupConfig = {}) {
    const {
      canvas,
      width = window.innerWidth,
      height = window.innerHeight,
      pixelRatio = window.devicePixelRatio || 1,
      antialias = true,
      shadowMap = true,
      shadowMapSize = 2048,
    } = config;

    // Initialize Scene
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x1a1a2e);
    this.scene.fog = new THREE.Fog(0x1a1a2e, 500, 2000);

    // Initialize Camera
    this.camera = new THREE.PerspectiveCamera(
      45,
      width / height,
      0.1,
      10000
    );
    this.camera.position.set(100, 150, 100);
    this.camera.lookAt(0, 0, 0);

    // Initialize Renderer
    this.renderer = new THREE.WebGLRenderer({
      canvas,
      antialias,
      alpha: false,
      preserveDrawingBuffer: false,
    });
    this.renderer.setSize(width, height);
    this.renderer.setPixelRatio(pixelRatio);
    this.renderer.shadowMap.enabled = shadowMap;
    this.renderer.shadowMap.type = THREE.PCFShadowShadowMap;
    this.renderer.shadowMap.autoUpdate = true;

    // Configure shadow map size for better quality
    if (shadowMap) {
      this.renderer.shadowMap.mapSize.width = shadowMapSize;
      this.renderer.shadowMap.mapSize.height = shadowMapSize;
    }

    // Initialize Lights
    this.lights = this.setupLights();

    // Add lights to scene
    this.scene.add(this.lights.ambientLight);
    this.scene.add(this.lights.directionalLight);
    this.lights.pointLights.forEach(light => this.scene.add(light));

    // Handle window resize
    window.addEventListener('resize', () => this.onWindowResize(width, height));
  }

  /**
   * Setup lighting for RTS game environment
   */
  private setupLights() {
    // Ambient light for overall scene illumination
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);

    // Directional light (simulating sun)
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(200, 300, 200);
    directionalLight.castShadow = true;

    // Configure shadow camera for directional light
    directionalLight.shadow.camera.left = -500;
    directionalLight.shadow.camera.right = 500;
    directionalLight.shadow.camera.top = 500;
    directionalLight.shadow.camera.bottom = -500;
    directionalLight.shadow.camera.near = 0.5;
    directionalLight.shadow.camera.far = 3000;
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    directionalLight.shadow.bias = -0.0001;

    // Point lights for strategic locations (bases, structures)
    const pointLights: THREE.PointLight[] = [];
    const pointLightPositions = [
      { pos: [100, 50, 100], color: 0x00ff00, intensity: 0.5 },
      { pos: [-100, 50, 100], color: 0xff0000, intensity: 0.5 },
      { pos: [100, 50, -100], color: 0x0000ff, intensity: 0.5 },
      { pos: [-100, 50, -100], color: 0xffff00, intensity: 0.5 },
    ];

    pointLightPositions.forEach(({ pos, color, intensity }) => {
      const pointLight = new THREE.PointLight(color, intensity, 300);
      pointLight.position.set(...(pos as [number, number, number]));
      pointLight.castShadow = true;
      pointLight.shadow.mapSize.width = 1024;
      pointLight.shadow.mapSize.height = 1024;
      pointLights.push(pointLight);
    });

    return { ambientLight, directionalLight, pointLights };
  }

  /**
   * Handle window resize events
   */
  private onWindowResize(baseWidth: number, baseHeight: number) {
    const width = window.innerWidth;
    const height = window.innerHeight;

    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  }

  /**
   * Get the renderer's DOM element
   */
  getDOMElement(): HTMLCanvasElement {
    return this.renderer.domElement;
  }

  /**
   * Update scene (for animation loop)
   */
  update(deltaTime: number) {
    // Update point lights with slight rotation for atmospheric effect
    this.lights.pointLights.forEach((light, index) => {
      const angle = (Date.now() * 0.0001 + index) % (Math.PI * 2);
      light.intensity = 0.3 + 0.2 * Math.sin(angle);
    });
  }

  /**
   * Render the scene
   */
  render() {
    this.renderer.render(this.scene, this.camera);
  }

  /**
   * Get camera for external manipulation
   */
  getCamera(): THREE.PerspectiveCamera {
    return this.camera;
  }

  /**
   * Get scene for adding objects
   */
  getScene(): THREE.Scene {
    return this.scene;
  }

  /**
   * Get renderer for external configuration
   */
  getRenderer(): THREE.WebGLRenderer {
    return this.renderer;
  }

  /**
   * Dispose of resources
   */
  dispose() {
    this.renderer.dispose();
    this.scene.clear();
  }

  /**
   * Set camera position for RTS isometric/top-down view
   */
  setCameraRTSView(distance: number = 200, height: number = 150, angle: number = 45) {
    const rad = (angle * Math.PI) / 180;
    this.camera.position.set(
      Math.cos(rad) * distance,
      height,
      Math.sin(rad) * distance
    );
    this.camera.lookAt(0, 0, 0);
  }

  /**
   * Update shadow map resolution
   */
  setShadowMapSize(size: number) {
    this.renderer.shadowMap.mapSize.width = size;
    this.renderer.shadowMap.mapSize.height = size;
    this.lights.directionalLight.shadow.mapSize.width = size;
    this.lights.directionalLight.shadow.mapSize.height = size;
  }
}

/**
 * Factory function for quick scene setup
 */
export function createRTSScene(config?: SceneSetupConfig): RTSSceneSetup {
  return new RTSSceneSetup(config);
}
