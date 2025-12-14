"""
Game Map System
Handles terrain generation, tile management, pathfinding using A* algorithm,
and resource placement on the game map.
"""

import heapq
import random
from enum import Enum
from typing import List, Tuple, Optional, Dict, Set
from dataclasses import dataclass, field


class TileType(Enum):
    """Enumeration of different tile types in the game world."""
    GRASS = 1
    WATER = 2
    FOREST = 3
    MOUNTAIN = 4


class ResourceType(Enum):
    """Enumeration of different resource types."""
    WOOD = "wood"
    STONE = "stone"
    GOLD = "gold"
    FOOD = "food"


@dataclass
class Tile:
    """Represents a single tile on the game map."""
    x: int
    y: int
    tile_type: TileType
    resource: Optional[ResourceType] = None
    resource_amount: int = 0
    walkable: bool = True

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.x == other.x and self.y == other.y
        return False


@dataclass
class PathNode:
    """Node used for A* pathfinding."""
    tile: Tile
    g_cost: float = 0.0  # Cost from start
    h_cost: float = 0.0  # Heuristic cost to goal
    parent: Optional['PathNode'] = None

    @property
    def f_cost(self) -> float:
        """Total estimated cost."""
        return self.g_cost + self.h_cost

    def __lt__(self, other):
        return self.f_cost < other.f_cost

    def __eq__(self, other):
        if isinstance(other, PathNode):
            return self.tile == other.tile
        return False

    def __hash__(self):
        return hash(self.tile)


class GameMap:
    """
    Manages the game map including terrain generation, tile management,
    pathfinding, and resource placement.
    """

    # Movement cost multipliers for different tile types
    TILE_COSTS = {
        TileType.GRASS: 1.0,
        TileType.FOREST: 1.5,
        TileType.MOUNTAIN: 2.0,
        TileType.WATER: float('inf'),  # Not walkable by default
    }

    # Resource spawn probabilities by tile type
    RESOURCE_SPAWN_RATES = {
        TileType.GRASS: {ResourceType.FOOD: 0.15},
        TileType.FOREST: {ResourceType.WOOD: 0.25, ResourceType.FOOD: 0.05},
        TileType.MOUNTAIN: {ResourceType.STONE: 0.20, ResourceType.GOLD: 0.10},
        TileType.WATER: {},
    }

    def __init__(self, width: int, height: int, seed: Optional[int] = None):
        """
        Initialize the game map.

        Args:
            width: Width of the map in tiles
            height: Height of the map in tiles
            seed: Random seed for terrain generation (optional)
        """
        self.width = width
        self.height = height
        self.tiles: Dict[Tuple[int, int], Tile] = {}
        self.resources_placed: Dict[Tuple[int, int], Tuple[ResourceType, int]] = {}

        if seed is not None:
            random.seed(seed)

        self._generate_terrain()

    def _generate_terrain(self) -> None:
        """Generate the initial terrain using noise-based generation."""
        # Initialize all tiles as grass
        for x in range(self.width):
            for y in range(self.height):
                self.tiles[(x, y)] = Tile(x, y, TileType.GRASS)

        # Add water bodies (simplified island generation)
        self._generate_water()

        # Add forests
        self._generate_forests()

        # Add mountains
        self._generate_mountains()

        # Place resources
        self._place_resources()

    def _generate_water(self) -> None:
        """Generate water bodies on the map."""
        # Create a few water clusters
        num_water_clusters = random.randint(3, 6)
        for _ in range(num_water_clusters):
            center_x = random.randint(0, self.width - 1)
            center_y = random.randint(0, self.height - 1)
            cluster_size = random.randint(5, 15)
            self._create_terrain_cluster(center_x, center_y, cluster_size, TileType.WATER)

    def _generate_forests(self) -> None:
        """Generate forest areas on the map."""
        num_forest_clusters = random.randint(5, 10)
        for _ in range(num_forest_clusters):
            center_x = random.randint(0, self.width - 1)
            center_y = random.randint(0, self.height - 1)
            cluster_size = random.randint(8, 20)
            self._create_terrain_cluster(center_x, center_y, cluster_size, TileType.FOREST)

    def _generate_mountains(self) -> None:
        """Generate mountain ranges on the map."""
        num_mountain_clusters = random.randint(3, 6)
        for _ in range(num_mountain_clusters):
            center_x = random.randint(0, self.width - 1)
            center_y = random.randint(0, self.height - 1)
            cluster_size = random.randint(6, 15)
            self._create_terrain_cluster(center_x, center_y, cluster_size, TileType.MOUNTAIN)

    def _create_terrain_cluster(self, center_x: int, center_y: int,
                                size: int, tile_type: TileType) -> None:
        """
        Create a cluster of terrain tiles.

        Args:
            center_x: X coordinate of cluster center
            center_y: Y coordinate of cluster center
            size: Size of the cluster
            tile_type: Type of terrain to create
        """
        created = 0
        queue = [(center_x, center_y)]
        visited = set()

        while queue and created < size:
            try:
                x, y = queue.pop(0)

                if (x, y) in visited:
                    continue
                if not (0 <= x < self.width and 0 <= y < self.height):
                    continue

                visited.add((x, y))

                # Don't overwrite water with other terrain (water is priority)
                if self.tiles[(x, y)].tile_type != TileType.WATER or tile_type == TileType.WATER:
                    self.tiles[(x, y)] = Tile(x, y, tile_type)
                    created += 1

                # Add neighboring tiles with some probability
                if random.random() < 0.6:
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if (nx, ny) not in visited:
                            queue.append((nx, ny))
            except (IndexError, KeyError):
                continue

    def _place_resources(self) -> None:
        """Place resources on the map based on tile types."""
        for tile in self.tiles.values():
            if tile.tile_type == TileType.WATER:
                continue

            spawn_rates = self.RESOURCE_SPAWN_RATES.get(tile.tile_type, {})
            for resource_type, spawn_rate in spawn_rates.items():
                if random.random() < spawn_rate:
                    amount = random.randint(5, 20)
                    self.place_resource(tile.x, tile.y, resource_type, amount)

    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """
        Get a tile at the specified coordinates.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Tile object or None if coordinates are out of bounds
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            return None
        return self.tiles.get((x, y))

    def set_tile(self, x: int, y: int, tile_type: TileType) -> bool:
        """
        Set a tile type at the specified coordinates.

        Args:
            x: X coordinate
            y: Y coordinate
            tile_type: Type of tile to set

        Returns:
            True if successful, False if coordinates are out of bounds
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        self.tiles[(x, y)] = Tile(x, y, tile_type)
        return True

    def place_resource(self, x: int, y: int, resource_type: ResourceType,
                       amount: int) -> bool:
        """
        Place a resource on a tile.

        Args:
            x: X coordinate
            y: Y coordinate
            resource_type: Type of resource to place
            amount: Amount of resource

        Returns:
            True if successful, False if tile doesn't exist or is water
        """
        tile = self.get_tile(x, y)
        if not tile or tile.tile_type == TileType.WATER:
            return False

        tile.resource = resource_type
        tile.resource_amount = amount
        self.resources_placed[(x, y)] = (resource_type, amount)
        return True

    def harvest_resource(self, x: int, y: int, amount: int) -> Optional[Tuple[ResourceType, int]]:
        """
        Harvest resources from a tile.

        Args:
            x: X coordinate
            y: Y coordinate
            amount: Amount to harvest

        Returns:
            Tuple of (ResourceType, amount harvested) or None if no resource
        """
        tile = self.get_tile(x, y)
        if not tile or not tile.resource:
            return None

        harvested = min(amount, tile.resource_amount)
        tile.resource_amount -= harvested

        if tile.resource_amount <= 0:
            tile.resource = None
            if (x, y) in self.resources_placed:
                del self.resources_placed[(x, y)]

        return (tile.resource, harvested)

    def get_neighbors(self, tile: Tile) -> List[Tile]:
        """
        Get all walkable neighboring tiles.

        Args:
            tile: The tile to get neighbors for

        Returns:
            List of neighboring Tile objects
        """
        neighbors = []
        # 8-directional movement (including diagonals)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                neighbor = self.get_tile(tile.x + dx, tile.y + dy)
                if neighbor and neighbor.walkable:
                    neighbors.append(neighbor)

        return neighbors

    def heuristic(self, tile1: Tile, tile2: Tile) -> float:
        """
        Calculate heuristic distance between two tiles (Euclidean distance).

        Args:
            tile1: First tile
            tile2: Second tile

        Returns:
            Estimated distance between tiles
        """
        dx = abs(tile1.x - tile2.x)
        dy = abs(tile1.y - tile2.y)
        return (dx ** 2 + dy ** 2) ** 0.5

    def get_movement_cost(self, from_tile: Tile, to_tile: Tile) -> float:
        """
        Calculate the movement cost between two adjacent tiles.

        Args:
            from_tile: Starting tile
            to_tile: Destination tile

        Returns:
            Movement cost
        """
        if not to_tile.walkable:
            return float('inf')

        # Diagonal movement costs more
        dx = abs(from_tile.x - to_tile.x)
        dy = abs(from_tile.y - to_tile.y)
        is_diagonal = dx == 1 and dy == 1

        base_cost = self.TILE_COSTS.get(to_tile.tile_type, 1.0)
        return base_cost * (1.414 if is_diagonal else 1.0)

    def find_path(self, start: Tile, goal: Tile) -> Optional[List[Tile]]:
        """
        Find the shortest path between two tiles using A* algorithm.

        Args:
            start: Starting tile
            goal: Goal tile

        Returns:
            List of tiles representing the path, or None if no path exists
        """
        if not start.walkable or not goal.walkable:
            return None

        open_set: List[PathNode] = []
        closed_set: Set[PathNode] = set()
        open_dict: Dict[Tuple[int, int], PathNode] = {}

        start_node = PathNode(start, 0.0, self.heuristic(start, goal))
        heapq.heappush(open_set, start_node)
        open_dict[(start.x, start.y)] = start_node

        while open_set:
            current_node = heapq.heappop(open_set)
            del open_dict[(current_node.tile.x, current_node.tile.y)]

            if current_node.tile == goal:
                # Reconstruct path
                path = []
                node = current_node
                while node is not None:
                    path.append(node.tile)
                    node = node.parent
                return list(reversed(path))

            closed_set.add(current_node)

            for neighbor in self.get_neighbors(current_node.tile):
                if any(n.tile == neighbor for n in closed_set):
                    continue

                move_cost = self.get_movement_cost(current_node.tile, neighbor)
                if move_cost == float('inf'):
                    continue

                new_g_cost = current_node.g_cost + move_cost
                neighbor_key = (neighbor.x, neighbor.y)

                # Check if we've found a better path
                if neighbor_key in open_dict:
                    existing_node = open_dict[neighbor_key]
                    if new_g_cost < existing_node.g_cost:
                        open_set.remove(existing_node)
                        heapq.heapify(open_set)
                        del open_dict[neighbor_key]
                    else:
                        continue

                new_h_cost = self.heuristic(neighbor, goal)
                new_node = PathNode(neighbor, new_g_cost, new_h_cost, current_node)
                heapq.heappush(open_set, new_node)
                open_dict[neighbor_key] = new_node

        return None  # No path found

    def get_map_info(self) -> Dict:
        """
        Get information about the map.

        Returns:
            Dictionary containing map statistics
        """
        tile_counts = {tile_type: 0 for tile_type in TileType}
        resource_counts = {resource_type: 0 for resource_type in ResourceType}

        for tile in self.tiles.values():
            tile_counts[tile.tile_type] += 1
            if tile.resource:
                resource_counts[tile.resource] += 1

        return {
            "width": self.width,
            "height": self.height,
            "total_tiles": len(self.tiles),
            "tile_distribution": {name.value: count for name, count in tile_counts.items()},
            "resources_placed": len(self.resources_placed),
            "resource_distribution": {name.value: count for name, count in resource_counts.items()},
        }

    def get_visible_area(self, center_x: int, center_y: int, radius: int) -> List[Tile]:
        """
        Get all tiles in a visible area around a center point.

        Args:
            center_x: X coordinate of center
            center_y: Y coordinate of center
            radius: Radius of visible area

        Returns:
            List of visible tiles
        """
        visible_tiles = []
        for x in range(max(0, center_x - radius), min(self.width, center_x + radius + 1)):
            for y in range(max(0, center_y - radius), min(self.height, center_y + radius + 1)):
                tile = self.get_tile(x, y)
                if tile:
                    visible_tiles.append(tile)
        return visible_tiles

    def __repr__(self) -> str:
        return f"GameMap(width={self.width}, height={self.height})"
