import * as THREE from 'three';

/**
 * Terrain Generator - Creates procedurally generated terrain with grass and trees
 */

interface TerrainConfig {
  width: number;
  height: number;
  widthSegments: number;
  heightSegments: number;
  scale: number;
  maxHeight: number;
}

interface TreeConfig {
  trunkRadius: number;
  trunkHeight: number;
  foliageRadius: number;
  foliageHeight: number;
}

/**
 * Perlin-like noise function for terrain generation
 */
function perlinNoise(x: number, y: number, seed: number = 0): number {
  const n = Math.sin(x * 12.9898 + y * 78.233 + seed) * 43758.5453;
  return n - Math.floor(n);
}

/**
 * Improved Perlin noise with multiple octaves for more natural terrain
 */
function improvedPerlinNoise(
  x: number,
  y: number,
  octaves: number = 4,
  persistence: number = 0.5,
  lacunarity: number = 2.0,
  seed: number = 0
): number {
  let value = 0;
  let amplitude = 1;
  let frequency = 1;
  let maxValue = 0;

  for (let i = 0; i < octaves; i++) {
    value += perlinNoise(x * frequency, y * frequency, seed + i) * amplitude;
    maxValue += amplitude;
    amplitude *= persistence;
    frequency *= lacunarity;
  }

  return value / maxValue;
}

/**
 * Create a procedural terrain with grass material
 */
function createTerrain(config: TerrainConfig): THREE.Mesh {
  const geometry = new THREE.PlaneGeometry(
    config.width,
    config.height,
    config.widthSegments,
    config.heightSegments
  );

  // Deform the terrain using noise
  const positionAttribute = geometry.getAttribute('position');
  const positions = positionAttribute.array as Float32Array;

  for (let i = 0; i < positions.length; i += 3) {
    const x = positions[i];
    const y = positions[i + 1];
    const z = improvedPerlinNoise(
      x / config.scale,
      y / config.scale,
      4,
      0.5,
      2.0,
      42
    ) * config.maxHeight;
    positions[i + 2] = z;
  }

  positionAttribute.needsUpdate = true;
  geometry.computeVertexNormals();

  // Create grass material
  const grassMaterial = new THREE.MeshPhongMaterial({
    color: 0x2d5016,
    emissive: 0x1a3009,
    shininess: 10,
    wireframe: false,
    flatShading: false,
  });

  const terrain = new THREE.Mesh(geometry, grassMaterial);
  terrain.castShadow = true;
  terrain.receiveShadow = true;
  terrain.rotation.x = -Math.PI / 2;

  return terrain;
}

/**
 * Create a single tree
 */
function createTree(position: THREE.Vector3, treeConfig: TreeConfig): THREE.Group {
  const tree = new THREE.Group();

  // Trunk
  const trunkGeometry = new THREE.CylinderGeometry(
    treeConfig.trunkRadius,
    treeConfig.trunkRadius * 1.2,
    treeConfig.trunkHeight,
    8
  );
  const trunkMaterial = new THREE.MeshPhongMaterial({
    color: 0x6d4c41,
    emissive: 0x3d2c21,
  });
  const trunk = new THREE.Mesh(trunkGeometry, trunkMaterial);
  trunk.position.y = treeConfig.trunkHeight / 2;
  trunk.castShadow = true;
  trunk.receiveShadow = true;
  tree.add(trunk);

  // Foliage (multiple spheres for natural look)
  const foliageMaterial = new THREE.MeshPhongMaterial({
    color: 0x228b22,
    emissive: 0x114411,
    shininess: 20,
  });

  // Main foliage sphere
  const foliageGeometry = new THREE.SphereGeometry(
    treeConfig.foliageRadius,
    8,
    8
  );
  const mainFoliage = new THREE.Mesh(foliageGeometry, foliageMaterial);
  mainFoliage.position.y = treeConfig.trunkHeight + treeConfig.foliageHeight * 0.3;
  mainFoliage.castShadow = true;
  mainFoliage.receiveShadow = true;
  tree.add(mainFoliage);

  // Upper foliage for variety
  const upperFoliage = new THREE.Mesh(
    new THREE.SphereGeometry(treeConfig.foliageRadius * 0.7, 8, 8),
    foliageMaterial
  );
  upperFoliage.position.y = treeConfig.trunkHeight + treeConfig.foliageHeight * 0.9;
  upperFoliage.castShadow = true;
  upperFoliage.receiveShadow = true;
  tree.add(upperFoliage);

  // Side foliage for fullness
  const sideFoliage = new THREE.Mesh(
    new THREE.SphereGeometry(treeConfig.foliageRadius * 0.6, 8, 8),
    foliageMaterial
  );
  sideFoliage.position.set(
    treeConfig.foliageRadius * 0.4,
    treeConfig.trunkHeight + treeConfig.foliageHeight * 0.5,
    0
  );
  sideFoliage.castShadow = true;
  sideFoliage.receiveShadow = true;
  tree.add(sideFoliage);

  tree.position.copy(position);
  return tree;
}

/**
 * Generate procedural tree positions based on terrain noise
 */
function generateTreePositions(
  terrain: THREE.Mesh,
  gridSize: number,
  density: number = 0.1,
  seed: number = 123
): THREE.Vector3[] {
  const positions: THREE.Vector3[] = [];
  const step = 1 / (density * 10);

  for (let x = -gridSize / 2; x < gridSize / 2; x += step) {
    for (let z = -gridSize / 2; z < gridSize / 2; z += step) {
      // Use noise to determine if a tree should be placed
      const noise = improvedPerlinNoise(x / 5, z / 5, 3, 0.5, 2.0, seed);

      // Only place trees where noise is above a threshold
      if (noise > 0.6) {
        // Sample height from terrain
        const raycaster = new THREE.Raycaster(
          new THREE.Vector3(x, 100, z),
          new THREE.Vector3(0, -1, 0)
        );
        const intersects = raycaster.intersectObject(terrain);

        if (intersects.length > 0) {
          const height = intersects[0].point.y + 0.5;
          positions.push(new THREE.Vector3(x, height, z));
        }
      }
    }
  }

  return positions;
}

/**
 * Main terrain generator class
 */
export class TerrainGenerator {
  private terrain: THREE.Mesh;
  private trees: THREE.Group = new THREE.Group();
  private config: TerrainConfig;
  private treeConfig: TreeConfig;

  constructor(
    terrainConfig: TerrainConfig = {
      width: 100,
      height: 100,
      widthSegments: 64,
      heightSegments: 64,
      scale: 15,
      maxHeight: 15,
    },
    treeConfig: TreeConfig = {
      trunkRadius: 0.3,
      trunkHeight: 2,
      foliageRadius: 1.5,
      foliageHeight: 2.5,
    }
  ) {
    this.config = terrainConfig;
    this.treeConfig = treeConfig;
    this.terrain = createTerrain(terrainConfig);
  }

  /**
   * Generate the complete scene with terrain and trees
   */
  public generate(treeCount?: number): THREE.Group {
    const scene = new THREE.Group();

    // Add terrain
    scene.add(this.terrain);

    // Generate and add trees
    const treePositions = generateTreePositions(
      this.terrain,
      Math.min(this.config.width, this.config.height),
      treeCount ? treeCount / (this.config.width * this.config.height) : 0.05
    );

    treePositions.forEach((position) => {
      const tree = createTree(position, this.treeConfig);
      this.trees.add(tree);
    });

    scene.add(this.trees);

    return scene;
  }

  /**
   * Get the terrain mesh
   */
  public getTerrain(): THREE.Mesh {
    return this.terrain;
  }

  /**
   * Get the trees group
   */
  public getTrees(): THREE.Group {
    return this.trees;
  }

  /**
   * Regenerate terrain and trees with new seed
   */
  public regenerate(seed: number = Math.random() * 1000): THREE.Group {
    // Clear existing trees
    this.trees.clear();

    // Recreate terrain with same config
    this.terrain = createTerrain(this.config);

    // Regenerate and add new trees
    const treePositions = generateTreePositions(
      this.terrain,
      Math.min(this.config.width, this.config.height),
      0.05,
      seed
    );

    treePositions.forEach((position) => {
      const tree = createTree(position, this.treeConfig);
      this.trees.add(tree);
    });

    const scene = new THREE.Group();
    scene.add(this.terrain);
    scene.add(this.trees);

    return scene;
  }

  /**
   * Get terrain statistics
   */
  public getStats(): {
    terrainVertices: number;
    treeCount: number;
    terrainSize: { width: number; height: number };
  } {
    const positionAttribute = this.terrain.geometry.getAttribute('position');
    return {
      terrainVertices: (positionAttribute.array as Float32Array).length / 3,
      treeCount: this.trees.children.length,
      terrainSize: {
        width: this.config.width,
        height: this.config.height,
      },
    };
  }
}

export { TerrainConfig, TreeConfig };
