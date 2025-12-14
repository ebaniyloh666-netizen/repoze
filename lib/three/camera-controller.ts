import * as THREE from 'three';

/**
 * RTS Camera Controller
 * Provides camera controls typical for Real-Time Strategy games
 * Supports panning, zooming, and rotation
 */
export class RTSCameraController {
  private camera: THREE.PerspectiveCamera;
  private target: THREE.Vector3;
  private domElement: HTMLElement;
  
  // Camera movement
  private panSpeed: number = 30;
  private zoomSpeed: number = 5;
  private rotationSpeed: number = 0.01;
  
  // Camera constraints
  private minZoom: number = 10;
  private maxZoom: number = 200;
  private minPitch: number = 15; // degrees
  private maxPitch: number = 85; // degrees
  
  // Current state
  private distance: number = 50;
  private pitch: number = 45; // degrees
  private yaw: number = 0; // degrees
  private keysPressed: Set<string> = new Set();
  private mouseDown: boolean = false;
  private lastMouseX: number = 0;
  private lastMouseY: number = 0;

  constructor(
    camera: THREE.PerspectiveCamera,
    domElement: HTMLElement,
    initialTarget: THREE.Vector3 = new THREE.Vector3(0, 0, 0)
  ) {
    this.camera = camera;
    this.domElement = domElement;
    this.target = initialTarget.clone();
    
    this.setupEventListeners();
    this.updateCameraPosition();
  }

  /**
   * Setup all event listeners for keyboard and mouse input
   */
  private setupEventListeners(): void {
    // Keyboard events
    document.addEventListener('keydown', (e) => this.onKeyDown(e));
    document.addEventListener('keyup', (e) => this.onKeyUp(e));
    
    // Mouse events
    this.domElement.addEventListener('mousedown', (e) => this.onMouseDown(e));
    this.domElement.addEventListener('mousemove', (e) => this.onMouseMove(e));
    this.domElement.addEventListener('mouseup', (e) => this.onMouseUp(e));
    this.domElement.addEventListener('wheel', (e) => this.onMouseWheel(e));
    
    // Context menu prevention for right-click
    this.domElement.addEventListener('contextmenu', (e) => e.preventDefault());
  }

  /**
   * Handle keyboard down events
   */
  private onKeyDown(event: KeyboardEvent): void {
    this.keysPressed.add(event.key.toLowerCase());
  }

  /**
   * Handle keyboard up events
   */
  private onKeyUp(event: KeyboardEvent): void {
    this.keysPressed.delete(event.key.toLowerCase());
  }

  /**
   * Handle mouse down events
   */
  private onMouseDown(event: MouseEvent): void {
    this.mouseDown = true;
    this.lastMouseX = event.clientX;
    this.lastMouseY = event.clientY;
  }

  /**
   * Handle mouse move events
   */
  private onMouseMove(event: MouseEvent): void {
    if (this.mouseDown) {
      const deltaX = event.clientX - this.lastMouseX;
      const deltaY = event.clientY - this.lastMouseY;
      
      // Right-click drag for rotation
      if (event.buttons === 2) {
        this.yaw -= deltaX * this.rotationSpeed;
        this.pitch += deltaY * this.rotationSpeed;
        
        // Clamp pitch
        this.pitch = Math.max(
          this.minPitch,
          Math.min(this.maxPitch, this.pitch)
        );
      }
      // Middle-click or Shift+drag for panning
      else if (event.buttons === 4 || (event.buttons === 1 && event.shiftKey)) {
        this.panByPixels(deltaX, deltaY);
      }
    }
    
    this.lastMouseX = event.clientX;
    this.lastMouseY = event.clientY;
  }

  /**
   * Handle mouse up events
   */
  private onMouseUp(event: MouseEvent): void {
    this.mouseDown = false;
  }

  /**
   * Handle mouse wheel events for zooming
   */
  private onMouseWheel(event: WheelEvent): void {
    event.preventDefault();
    
    const scrollDelta = event.deltaY > 0 ? 1 : -1;
    this.distance += scrollDelta * this.zoomSpeed;
    this.distance = Math.max(
      this.minZoom,
      Math.min(this.maxZoom, this.distance)
    );
  }

  /**
   * Pan camera by pixel amounts
   */
  private panByPixels(deltaX: number, deltaY: number): void {
    const panAmount = (this.distance / 100) * this.panSpeed;
    
    // Get camera right and forward vectors
    const forward = new THREE.Vector3(
      Math.sin(this.yaw),
      0,
      Math.cos(this.yaw)
    ).normalize();
    
    const right = new THREE.Vector3(
      Math.cos(this.yaw),
      0,
      -Math.sin(this.yaw)
    ).normalize();
    
    // Apply pan
    this.target.addScaledVector(right, -deltaX * panAmount * 0.01);
    this.target.addScaledVector(forward, -deltaY * panAmount * 0.01);
  }

  /**
   * Update camera position based on current state
   */
  private updateCameraPosition(): void {
    const pitchRad = THREE.MathUtils.degToRad(this.pitch);
    const yawRad = this.yaw;
    
    // Calculate camera position
    const x = this.target.x + this.distance * Math.sin(yawRad) * Math.cos(pitchRad);
    const y = this.target.y + this.distance * Math.sin(pitchRad);
    const z = this.target.z + this.distance * Math.cos(yawRad) * Math.cos(pitchRad);
    
    this.camera.position.set(x, y, z);
    this.camera.lookAt(this.target);
  }

  /**
   * Handle keyboard-based camera movement
   */
  private handleKeyboardInput(): void {
    const moveAmount = this.panSpeed * 0.016; // Assume 60fps
    const forward = new THREE.Vector3(
      Math.sin(this.yaw),
      0,
      Math.cos(this.yaw)
    ).normalize();
    
    const right = new THREE.Vector3(
      Math.cos(this.yaw),
      0,
      -Math.sin(this.yaw)
    ).normalize();
    
    // WASD movement
    if (this.keysPressed.has('w')) {
      this.target.addScaledVector(forward, moveAmount);
    }
    if (this.keysPressed.has('s')) {
      this.target.addScaledVector(forward, -moveAmount);
    }
    if (this.keysPressed.has('a')) {
      this.target.addScaledVector(right, -moveAmount);
    }
    if (this.keysPressed.has('d')) {
      this.target.addScaledVector(right, moveAmount);
    }
    
    // Q/E for rotation
    if (this.keysPressed.has('q')) {
      this.yaw -= this.rotationSpeed * 2;
    }
    if (this.keysPressed.has('e')) {
      this.yaw += this.rotationSpeed * 2;
    }
    
    // Z/X for zoom
    if (this.keysPressed.has('z')) {
      this.distance -= this.zoomSpeed;
      this.distance = Math.max(this.minZoom, this.distance);
    }
    if (this.keysPressed.has('x')) {
      this.distance += this.zoomSpeed;
      this.distance = Math.min(this.maxZoom, this.distance);
    }
  }

  /**
   * Update the camera (should be called in the animation loop)
   */
  public update(): void {
    this.handleKeyboardInput();
    this.updateCameraPosition();
  }

  /**
   * Set the camera focus point
   */
  public setTarget(position: THREE.Vector3): void {
    this.target.copy(position);
  }

  /**
   * Get the current camera target
   */
  public getTarget(): THREE.Vector3 {
    return this.target.clone();
  }

  /**
   * Set zoom level (1 = min zoom, 0 = max zoom as a normalized value)
   */
  public setZoom(normalizedZoom: number): void {
    normalizedZoom = Math.max(0, Math.min(1, normalizedZoom));
    this.distance = this.minZoom + (this.maxZoom - this.minZoom) * (1 - normalizedZoom);
  }

  /**
   * Get current zoom as normalized value
   */
  public getZoom(): number {
    return 1 - (this.distance - this.minZoom) / (this.maxZoom - this.minZoom);
  }

  /**
   * Set camera pitch (in degrees)
   */
  public setPitch(degrees: number): void {
    this.pitch = Math.max(this.minPitch, Math.min(this.maxPitch, degrees));
  }

  /**
   * Get current pitch (in degrees)
   */
  public getPitch(): number {
    return this.pitch;
  }

  /**
   * Set camera yaw (in radians)
   */
  public setYaw(radians: number): void {
    this.yaw = radians;
  }

  /**
   * Get current yaw (in radians)
   */
  public getYaw(): number {
    return this.yaw;
  }

  /**
   * Configure camera constraints
   */
  public setConstraints(options: {
    minZoom?: number;
    maxZoom?: number;
    minPitch?: number;
    maxPitch?: number;
  }): void {
    if (options.minZoom !== undefined) this.minZoom = options.minZoom;
    if (options.maxZoom !== undefined) this.maxZoom = options.maxZoom;
    if (options.minPitch !== undefined) this.minPitch = options.minPitch;
    if (options.maxPitch !== undefined) this.maxPitch = options.maxPitch;
  }

  /**
   * Configure movement speeds
   */
  public setSpeeds(options: {
    panSpeed?: number;
    zoomSpeed?: number;
    rotationSpeed?: number;
  }): void {
    if (options.panSpeed !== undefined) this.panSpeed = options.panSpeed;
    if (options.zoomSpeed !== undefined) this.zoomSpeed = options.zoomSpeed;
    if (options.rotationSpeed !== undefined) this.rotationSpeed = options.rotationSpeed;
  }

  /**
   * Reset camera to initial state
   */
  public reset(target?: THREE.Vector3): void {
    if (target) {
      this.target.copy(target);
    }
    this.distance = 50;
    this.pitch = 45;
    this.yaw = 0;
    this.keysPressed.clear();
    this.updateCameraPosition();
  }

  /**
   * Dispose of event listeners
   */
  public dispose(): void {
    document.removeEventListener('keydown', (e) => this.onKeyDown(e));
    document.removeEventListener('keyup', (e) => this.onKeyUp(e));
    this.domElement.removeEventListener('mousedown', (e) => this.onMouseDown(e));
    this.domElement.removeEventListener('mousemove', (e) => this.onMouseMove(e));
    this.domElement.removeEventListener('mouseup', (e) => this.onMouseUp(e));
    this.domElement.removeEventListener('wheel', (e) => this.onMouseWheel(e));
  }
}
