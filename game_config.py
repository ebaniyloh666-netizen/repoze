"""
Empire 3D Game Configuration
Central configuration file for all game settings and constants
"""

# ============================================================================
# SCREEN AND DISPLAY SETTINGS
# ============================================================================
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_FPS = 60
FULLSCREEN = False
VSYNC_ENABLED = True

# Display modes
DISPLAY_RESOLUTION_OPTIONS = [
    (1280, 720),
    (1600, 900),
    (1920, 1080),
    (2560, 1440),
]

# ============================================================================
# COLOR PALETTE
# ============================================================================
COLORS = {
    # Basic colors
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'YELLOW': (255, 255, 0),
    'CYAN': (0, 255, 255),
    'MAGENTA': (255, 0, 255),
    
    # Grayscale
    'DARK_GRAY': (64, 64, 64),
    'GRAY': (128, 128, 128),
    'LIGHT_GRAY': (192, 192, 192),
    
    # Team colors
    'TEAM_1': (30, 144, 255),      # Dodger Blue
    'TEAM_2': (220, 20, 60),       # Crimson Red
    'TEAM_3': (50, 205, 50),       # Lime Green
    'TEAM_4': (255, 140, 0),       # Dark Orange
    'NEUTRAL': (128, 128, 128),    # Gray
    
    # UI colors
    'UI_BACKGROUND': (20, 20, 30),
    'UI_PANEL': (40, 40, 60),
    'UI_BORDER': (100, 100, 150),
    'UI_HOVER': (150, 150, 200),
    'UI_ACTIVE': (100, 200, 255),
    
    # Resource colors
    'GOLD': (255, 215, 0),
    'WOOD': (139, 69, 19),
    'STONE': (169, 169, 169),
    'IRON': (70, 70, 70),
    'FOOD': (34, 139, 34),
    
    # Status colors
    'HEALTH_GOOD': (0, 255, 0),
    'HEALTH_WARNING': (255, 165, 0),
    'HEALTH_CRITICAL': (255, 0, 0),
}

# ============================================================================
# UNIT STATS AND CONFIGURATION
# ============================================================================
UNIT_TYPES = {
    'SOLDIER': {
        'name': 'Soldier',
        'health': 100,
        'attack': 15,
        'defense': 5,
        'speed': 5.0,
        'range': 1.0,
        'cost': {
            'gold': 50,
            'wood': 10,
            'food': 20,
        },
        'training_time': 30,  # seconds
        'armor': 2,
    },
    'ARCHER': {
        'name': 'Archer',
        'health': 60,
        'attack': 20,
        'defense': 3,
        'speed': 4.5,
        'range': 8.0,
        'cost': {
            'gold': 75,
            'wood': 30,
            'food': 15,
        },
        'training_time': 40,
        'armor': 1,
    },
    'CAVALRY': {
        'name': 'Cavalry',
        'health': 150,
        'attack': 25,
        'defense': 8,
        'speed': 7.5,
        'range': 1.0,
        'cost': {
            'gold': 150,
            'wood': 50,
            'food': 40,
        },
        'training_time': 60,
        'armor': 5,
    },
    'MAGE': {
        'name': 'Mage',
        'health': 50,
        'attack': 30,
        'defense': 2,
        'speed': 3.5,
        'range': 10.0,
        'cost': {
            'gold': 200,
            'wood': 20,
            'food': 10,
        },
        'training_time': 80,
        'armor': 0,
        'mana': 100,
    },
    'PALADIN': {
        'name': 'Paladin',
        'health': 200,
        'attack': 28,
        'defense': 12,
        'speed': 5.0,
        'range': 1.5,
        'cost': {
            'gold': 300,
            'wood': 60,
            'food': 50,
        },
        'training_time': 120,
        'armor': 8,
    },
    'SCOUT': {
        'name': 'Scout',
        'health': 30,
        'attack': 8,
        'defense': 1,
        'speed': 10.0,
        'range': 1.0,
        'cost': {
            'gold': 25,
            'wood': 5,
            'food': 10,
        },
        'training_time': 15,
        'armor': 0,
        'vision_range': 20.0,
    },
}

# Unit group limits
MAX_UNIT_GROUP_SIZE = 100
UNIT_FORMATION_TYPES = ['Line', 'Square', 'Column', 'Wedge', 'Circle']

# ============================================================================
# BUILDING TYPES AND CONFIGURATION
# ============================================================================
BUILDING_TYPES = {
    'BARRACKS': {
        'name': 'Barracks',
        'health': 500,
        'defense': 10,
        'width': 3,
        'height': 3,
        'cost': {
            'gold': 200,
            'wood': 500,
            'stone': 300,
        },
        'construction_time': 120,  # seconds
        'unit_production': ['SOLDIER', 'ARCHER', 'SCOUT'],
        'capacity': 30,  # max units training
    },
    'STABLE': {
        'name': 'Stable',
        'health': 400,
        'defense': 8,
        'width': 3,
        'height': 3,
        'cost': {
            'gold': 300,
            'wood': 400,
            'stone': 200,
        },
        'construction_time': 150,
        'unit_production': ['CAVALRY', 'PALADIN'],
        'capacity': 20,
    },
    'MAGE_TOWER': {
        'name': 'Mage Tower',
        'health': 300,
        'defense': 5,
        'width': 2,
        'height': 2,
        'cost': {
            'gold': 500,
            'wood': 200,
            'stone': 400,
        },
        'construction_time': 180,
        'unit_production': ['MAGE'],
        'capacity': 10,
    },
    'WALL': {
        'name': 'Wall',
        'health': 800,
        'defense': 20,
        'width': 1,
        'height': 1,
        'cost': {
            'gold': 50,
            'wood': 100,
            'stone': 500,
        },
        'construction_time': 60,
        'unit_production': [],
    },
    'TOWER': {
        'name': 'Defense Tower',
        'health': 600,
        'defense': 15,
        'width': 2,
        'height': 2,
        'cost': {
            'gold': 300,
            'wood': 200,
            'stone': 400,
        },
        'construction_time': 120,
        'attack': 25,
        'attack_range': 12.0,
        'unit_production': [],
    },
    'RESOURCE_GATHERER': {
        'name': 'Resource Gatherer',
        'health': 200,
        'defense': 3,
        'width': 2,
        'height': 2,
        'cost': {
            'gold': 100,
            'wood': 300,
            'stone': 100,
        },
        'construction_time': 90,
        'unit_production': [],
        'gather_rate': 0.5,  # resources per second
    },
    'WAREHOUSE': {
        'name': 'Warehouse',
        'health': 400,
        'defense': 5,
        'width': 3,
        'height': 3,
        'cost': {
            'gold': 100,
            'wood': 400,
            'stone': 200,
        },
        'construction_time': 100,
        'storage_capacity': 5000,
        'unit_production': [],
    },
    'TOWNHALL': {
        'name': 'Town Hall',
        'health': 1000,
        'defense': 20,
        'width': 4,
        'height': 4,
        'cost': {
            'gold': 500,
            'wood': 800,
            'stone': 600,
        },
        'construction_time': 300,
        'unit_production': [],
        'special': 'faction_center',
    },
}

# ============================================================================
# MAP SETTINGS
# ============================================================================
MAP_SETTINGS = {
    'MAP_WIDTH': 256,
    'MAP_HEIGHT': 256,
    'TILE_SIZE': 32,  # pixels
    'MAX_PLAYERS': 4,
    'MIN_PLAYERS': 2,
    'STARTING_RESOURCES': {
        'gold': 500,
        'wood': 500,
        'stone': 300,
        'iron': 200,
        'food': 400,
    },
    'TERRAIN_TYPES': ['grass', 'forest', 'mountain', 'water', 'desert', 'swamp'],
    'RESOURCE_SPAWN_RATE': 0.1,  # percentage of tiles
    'FOG_OF_WAR_ENABLED': True,
}

# ============================================================================
# GAME BALANCE PARAMETERS
# ============================================================================
BALANCE = {
    # Economy
    'RESOURCE_GENERATION_RATE': 1.0,  # multiplier
    'BUILD_COST_MULTIPLIER': 1.0,
    'UNIT_COST_MULTIPLIER': 1.0,
    
    # Combat
    'DAMAGE_MULTIPLIER': 1.0,
    'DEFENSE_REDUCTION': 0.1,  # defense reduces X% of damage
    'ARMOR_EFFECTIVENESS': 0.5,  # armor reduces X% of damage per point
    'CRITICAL_CHANCE': 0.05,  # 5% base critical chance
    'CRITICAL_MULTIPLIER': 1.5,  # critical does 1.5x damage
    
    # Health and Healing
    'BASE_HEALING_RATE': 0.1,  # HP per second
    'UNIT_RESPAWN_TIME': 30,  # seconds
    
    # Speed and Movement
    'MOVEMENT_SPEED_MULTIPLIER': 1.0,
    'ACCELERATION_TIME': 0.5,  # seconds to reach max speed
    
    # Building
    'BUILD_TIME_MULTIPLIER': 1.0,
    'BUILDING_PLACEMENT_RANGE': 10.0,  # distance units can build from
    
    # Experience and Leveling
    'EXPERIENCE_GAIN_MULTIPLIER': 1.0,
    'LEVEL_UP_THRESHOLD': 100,
    'STAT_INCREASE_PER_LEVEL': {
        'health': 10,
        'attack': 2,
        'defense': 1,
    },
    
    # Vision and Detection
    'BASE_VISION_RANGE': 12.0,
    'STEALTH_DETECTION_RANGE': 5.0,
    
    # Time
    'GAME_SPEED': 1.0,  # 1.0 = normal speed
    'DAY_NIGHT_CYCLE_DURATION': 600,  # seconds (10 minutes)
}

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================
ABILITIES = {
    'CHARGE': {
        'name': 'Charge',
        'unit_types': ['CAVALRY', 'PALADIN'],
        'cooldown': 10,  # seconds
        'duration': 3,
        'speed_multiplier': 2.0,
        'damage_multiplier': 1.5,
        'mana_cost': 30,
    },
    'FIREBALL': {
        'name': 'Fireball',
        'unit_types': ['MAGE'],
        'cooldown': 8,
        'range': 15.0,
        'radius': 5.0,
        'damage': 50,
        'mana_cost': 50,
    },
    'SHIELD_BASH': {
        'name': 'Shield Bash',
        'unit_types': ['PALADIN', 'SOLDIER'],
        'cooldown': 12,
        'stun_duration': 2,
        'range': 3.0,
        'mana_cost': 20,
    },
    'VOLLEY': {
        'name': 'Volley',
        'unit_types': ['ARCHER'],
        'cooldown': 6,
        'projectiles': 5,
        'spread_angle': 30,
        'mana_cost': 25,
    },
}

# ============================================================================
# GAME RULES AND MECHANICS
# ============================================================================
GAME_RULES = {
    'FRIENDLY_FIRE_ENABLED': False,
    'BUILDING_OVERLAP_ALLOWED': False,
    'UNIT_COLLISION_ENABLED': True,
    'PATHING_ENABLED': True,
    'RETREAT_ENABLED': True,
    'SURRENDER_ENABLED': True,
    'DIPLOMACY_ENABLED': True,
    'DIPLOMACY_ACTIONS': ['ally', 'enemy', 'neutral', 'trade'],
    'VICTORY_CONDITIONS': ['elimination', 'control_points', 'time_limit'],
    'TIME_LIMIT_MINUTES': 60,
    'CONTROL_POINT_THRESHOLD': 3,  # points needed to win
}

# ============================================================================
# UI CONFIGURATION
# ============================================================================
UI_CONFIG = {
    'MINIMAP_SCALE': 0.2,
    'MINIMAP_UPDATE_RATE': 0.5,  # seconds
    'TOOLTIP_DELAY': 0.5,  # seconds
    'MENU_ANIMATION_SPEED': 0.3,  # seconds
    'BUTTON_SIZE': (150, 40),
    'DEFAULT_FONT_SIZE': 14,
    'TITLE_FONT_SIZE': 28,
    'HUD_OPACITY': 0.8,
    'SELECTION_BOX_COLOR': (100, 200, 255),
    'SELECTION_BOX_WIDTH': 2,
}

# ============================================================================
# AUDIO CONFIGURATION
# ============================================================================
AUDIO_CONFIG = {
    'MASTER_VOLUME': 1.0,
    'MUSIC_VOLUME': 0.7,
    'SFX_VOLUME': 0.8,
    'VOICE_VOLUME': 0.9,
    'AMBIENT_VOLUME': 0.5,
    'AUDIO_ENABLED': True,
    'MUSIC_ENABLED': True,
}

# ============================================================================
# NETWORK AND MULTIPLAYER
# ============================================================================
NETWORK_CONFIG = {
    'SERVER_IP': 'localhost',
    'SERVER_PORT': 5000,
    'TIMEOUT_SECONDS': 30,
    'MAX_RECONNECT_ATTEMPTS': 5,
    'RECONNECT_DELAY': 3,  # seconds
    'PLAYER_NAME_MAX_LENGTH': 20,
    'CHAT_MESSAGE_MAX_LENGTH': 200,
    'UPDATE_RATE': 30,  # hz
    'USE_COMPRESSION': True,
}

# ============================================================================
# DIFFICULTY SETTINGS
# ============================================================================
DIFFICULTY_SETTINGS = {
    'EASY': {
        'resource_multiplier': 1.5,
        'enemy_damage_multiplier': 0.7,
        'ai_reaction_time': 2.0,
    },
    'NORMAL': {
        'resource_multiplier': 1.0,
        'enemy_damage_multiplier': 1.0,
        'ai_reaction_time': 1.0,
    },
    'HARD': {
        'resource_multiplier': 0.8,
        'enemy_damage_multiplier': 1.3,
        'ai_reaction_time': 0.5,
    },
    'INSANE': {
        'resource_multiplier': 0.6,
        'enemy_damage_multiplier': 1.5,
        'ai_reaction_time': 0.2,
    },
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_unit_stats(unit_type):
    """Get stats for a specific unit type"""
    return UNIT_TYPES.get(unit_type, None)

def get_building_stats(building_type):
    """Get stats for a specific building type"""
    return BUILDING_TYPES.get(building_type, None)

def get_ability_stats(ability_name):
    """Get stats for a specific ability"""
    return ABILITIES.get(ability_name, None)

def get_difficulty_settings(difficulty):
    """Get difficulty settings"""
    return DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS['NORMAL'])

def calculate_total_cost(cost_dict, multiplier=1.0):
    """Calculate total cost with multiplier"""
    return {resource: int(amount * multiplier) 
            for resource, amount in cost_dict.items()}
