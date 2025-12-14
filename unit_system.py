"""
Unit Management System
Comprehensive system for handling unit creation, movement, combat, abilities, and state management.
"""

from enum import Enum
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import uuid
from datetime import datetime


class UnitType(Enum):
    """Enumeration of unit types."""
    SOLDIER = "soldier"
    KNIGHT = "knight"
    ARCHER = "archer"
    MAGE = "mage"
    HEALER = "healer"
    TANK = "tank"


class UnitState(Enum):
    """Enumeration of unit states."""
    IDLE = "idle"
    MOVING = "moving"
    IN_COMBAT = "in_combat"
    CASTING = "casting"
    STUNNED = "stunned"
    DEAD = "dead"
    RECOVERING = "recovering"


class AbilityType(Enum):
    """Enumeration of ability types."""
    ATTACK = "attack"
    DEFEND = "defend"
    HEAL = "heal"
    SPELL = "spell"
    BUFF = "buff"
    DEBUFF = "debuff"
    SUMMON = "summon"


@dataclass
class Position:
    """Represents a position in 2D space."""
    x: float
    y: float

    def distance_to(self, other: "Position") -> float:
        """Calculate Euclidean distance to another position."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def move_towards(self, target: "Position", distance: float) -> "Position":
        """Move towards a target position by a given distance."""
        current_distance = self.distance_to(target)
        if current_distance <= distance:
            return Position(target.x, target.y)
        
        ratio = distance / current_distance
        new_x = self.x + (target.x - self.x) * ratio
        new_y = self.y + (target.y - self.y) * ratio
        return Position(new_x, new_y)

    def __eq__(self, other) -> bool:
        """Check if two positions are equal."""
        return self.x == other.x and self.y == other.y


@dataclass
class Ability:
    """Represents a unit ability."""
    ability_id: str
    name: str
    ability_type: AbilityType
    damage: float = 0
    healing: float = 0
    cooldown: float = 0
    range: float = 10
    cost: float = 0  # Resource cost (mana, stamina, etc.)
    description: str = ""

    def __post_init__(self):
        """Initialize ability with unique ID if not provided."""
        if not self.ability_id:
            self.ability_id = str(uuid.uuid4())


@dataclass
class UnitStats:
    """Represents unit statistics."""
    health: float
    max_health: float
    mana: float
    max_mana: float
    stamina: float
    max_stamina: float
    attack_power: float
    defense: float
    speed: float
    accuracy: float
    level: int = 1
    experience: int = 0

    def take_damage(self, damage: float) -> float:
        """Reduce health by damage amount and return actual damage taken."""
        actual_damage = min(damage, self.health)
        self.health = max(0, self.health - damage)
        return actual_damage

    def heal(self, amount: float) -> float:
        """Increase health and return actual healing done."""
        actual_healing = min(amount, self.max_health - self.health)
        self.health = min(self.max_health, self.health + amount)
        return actual_healing

    def restore_resource(self, resource_type: str, amount: float) -> float:
        """Restore mana or stamina and return actual amount restored."""
        if resource_type == "mana":
            actual_restore = min(amount, self.max_mana - self.mana)
            self.mana = min(self.max_mana, self.mana + amount)
            return actual_restore
        elif resource_type == "stamina":
            actual_restore = min(amount, self.max_stamina - self.stamina)
            self.stamina = min(self.max_stamina, self.stamina + amount)
            return actual_restore
        return 0

    def is_alive(self) -> bool:
        """Check if unit is alive."""
        return self.health > 0


class Unit:
    """Represents a single unit in the game."""

    def __init__(
        self,
        unit_id: str,
        name: str,
        unit_type: UnitType,
        stats: UnitStats,
        position: Position,
        team_id: str = ""
    ):
        """Initialize a unit."""
        self.unit_id = unit_id or str(uuid.uuid4())
        self.name = name
        self.unit_type = unit_type
        self.stats = stats
        self.position = position
        self.team_id = team_id
        self.state = UnitState.IDLE
        self.abilities: Dict[str, Ability] = {}
        self.active_effects: List[Dict] = []
        self.target_unit: Optional["Unit"] = None
        self.movement_target: Optional[Position] = None
        self.last_action_time = datetime.utcnow()
        self.action_cooldown = 0.5  # seconds

    def add_ability(self, ability: Ability) -> None:
        """Add an ability to the unit."""
        self.abilities[ability.ability_id] = ability

    def remove_ability(self, ability_id: str) -> bool:
        """Remove an ability from the unit."""
        if ability_id in self.abilities:
            del self.abilities[ability_id]
            return True
        return False

    def get_ability(self, ability_id: str) -> Optional[Ability]:
        """Get an ability by ID."""
        return self.abilities.get(ability_id)

    def can_use_ability(self, ability: Ability) -> bool:
        """Check if unit can use an ability."""
        if not self.stats.is_alive():
            return False
        if ability.cost > self.stats.mana:
            return False
        return True

    def use_ability(self, ability: Ability, target: Optional["Unit"] = None) -> bool:
        """Use an ability."""
        if not self.can_use_ability(ability):
            return False

        # Deduct resource cost
        self.stats.mana = max(0, self.stats.mana - ability.cost)

        # Apply ability effects
        if ability.ability_type == AbilityType.ATTACK and target:
            damage = ability.damage + self.stats.attack_power * 0.5
            target.stats.take_damage(damage)
            self.add_effect("attack", 0.1)
            return True

        elif ability.ability_type == AbilityType.HEAL and target:
            healing = ability.healing
            target.stats.heal(healing)
            self.add_effect("heal", 0.1)
            return True

        elif ability.ability_type == AbilityType.DEFEND:
            self.add_effect("defend", 5.0, {"defense_bonus": ability.damage})
            self.state = UnitState.IDLE
            return True

        elif ability.ability_type == AbilityType.SPELL and target:
            damage = ability.damage
            target.stats.take_damage(damage)
            self.add_effect("spell_cast", 1.0)
            return True

        return False

    def add_effect(self, effect_name: str, duration: float, data: Dict = None) -> None:
        """Add a temporary effect to the unit."""
        effect = {
            "name": effect_name,
            "duration": duration,
            "start_time": datetime.utcnow(),
            "data": data or {}
        }
        self.active_effects.append(effect)

    def remove_effect(self, effect_name: str) -> bool:
        """Remove an active effect."""
        self.active_effects = [e for e in self.active_effects if e["name"] != effect_name]
        return True

    def get_active_effects(self) -> List[Dict]:
        """Get all active effects."""
        now = datetime.utcnow()
        self.active_effects = [
            e for e in self.active_effects
            if (now - e["start_time"]).total_seconds() < e["duration"]
        ]
        return self.active_effects

    def move_to(self, target_position: Position) -> None:
        """Set movement target."""
        self.movement_target = target_position
        self.state = UnitState.MOVING

    def update_position(self, distance: float) -> None:
        """Update unit position based on movement."""
        if self.movement_target and self.state == UnitState.MOVING:
            self.position = self.position.move_towards(self.movement_target, distance)
            
            if self.position == self.movement_target:
                self.movement_target = None
                self.state = UnitState.IDLE

    def attack(self, target: "Unit") -> bool:
        """Attack a target unit."""
        if not self.stats.is_alive() or not target.stats.is_alive():
            return False

        distance = self.position.distance_to(target.position)
        
        # Default attack range
        attack_range = 2.0
        if distance > attack_range:
            return False

        damage = self.stats.attack_power
        target.stats.take_damage(damage)
        self.state = UnitState.IN_COMBAT
        target.state = UnitState.IN_COMBAT

        return True

    def take_damage(self, damage: float) -> bool:
        """Take damage and check if unit dies."""
        self.stats.take_damage(damage)
        if not self.stats.is_alive():
            self.state = UnitState.DEAD
            return True
        return False

    def heal(self, amount: float) -> None:
        """Heal the unit."""
        self.stats.heal(amount)

    def apply_status_effect(self, effect_name: str, duration: float) -> None:
        """Apply a status effect to the unit."""
        if effect_name == "stun":
            self.state = UnitState.STUNNED
            self.add_effect("stun", duration)
        elif effect_name == "slow":
            self.add_effect("slow", duration, {"speed_reduction": 0.5})

    def reset_state(self) -> None:
        """Reset unit state to idle."""
        if self.state not in [UnitState.DEAD, UnitState.STUNNED]:
            self.state = UnitState.IDLE
            self.target_unit = None

    def get_info(self) -> Dict:
        """Get unit information."""
        return {
            "unit_id": self.unit_id,
            "name": self.name,
            "type": self.unit_type.value,
            "state": self.state.value,
            "position": {"x": self.position.x, "y": self.position.y},
            "health": self.stats.health,
            "max_health": self.stats.max_health,
            "mana": self.stats.mana,
            "level": self.stats.level,
            "team_id": self.team_id
        }


class UnitGroup:
    """Represents a group of units."""

    def __init__(self, group_id: str, name: str, team_id: str = ""):
        """Initialize a unit group."""
        self.group_id = group_id or str(uuid.uuid4())
        self.name = name
        self.team_id = team_id
        self.units: Dict[str, Unit] = {}
        self.formation: str = "line"  # formation type
        self.created_at = datetime.utcnow()

    def add_unit(self, unit: Unit) -> bool:
        """Add a unit to the group."""
        if unit.unit_id in self.units:
            return False
        self.units[unit.unit_id] = unit
        return True

    def remove_unit(self, unit_id: str) -> bool:
        """Remove a unit from the group."""
        if unit_id in self.units:
            del self.units[unit_id]
            return True
        return False

    def get_unit(self, unit_id: str) -> Optional[Unit]:
        """Get a unit by ID."""
        return self.units.get(unit_id)

    def get_all_units(self) -> List[Unit]:
        """Get all units in the group."""
        return list(self.units.values())

    def get_alive_units(self) -> List[Unit]:
        """Get all alive units in the group."""
        return [u for u in self.units.values() if u.stats.is_alive()]

    def get_unit_count(self) -> int:
        """Get the number of units in the group."""
        return len(self.units)

    def get_alive_count(self) -> int:
        """Get the number of alive units."""
        return len(self.get_alive_units())

    def set_formation(self, formation: str) -> None:
        """Set the formation of the group."""
        valid_formations = ["line", "column", "square", "circle"]
        if formation in valid_formations:
            self.formation = formation

    def move_group(self, target_position: Position) -> None:
        """Move all units in the group to a target position."""
        for unit in self.units.values():
            if unit.stats.is_alive():
                unit.move_to(target_position)

    def attack_target(self, target: Unit) -> int:
        """Have all alive units in the group attack a target."""
        successful_attacks = 0
        for unit in self.get_alive_units():
            if unit.attack(target):
                successful_attacks += 1
        return successful_attacks

    def heal_group(self, amount: float) -> None:
        """Heal all units in the group."""
        for unit in self.units.values():
            if unit.stats.is_alive():
                unit.heal(amount)

    def get_total_health(self) -> float:
        """Get total health of all units."""
        return sum(u.stats.health for u in self.units.values())

    def get_total_max_health(self) -> float:
        """Get total max health of all units."""
        return sum(u.stats.max_health for u in self.units.values())

    def get_group_info(self) -> Dict:
        """Get group information."""
        return {
            "group_id": self.group_id,
            "name": self.name,
            "team_id": self.team_id,
            "formation": self.formation,
            "total_units": self.get_unit_count(),
            "alive_units": self.get_alive_count(),
            "total_health": self.get_total_health(),
            "total_max_health": self.get_total_max_health(),
            "created_at": self.created_at.isoformat()
        }


class UnitManager:
    """Manages all units and groups in the system."""

    def __init__(self):
        """Initialize the unit manager."""
        self.units: Dict[str, Unit] = {}
        self.groups: Dict[str, UnitGroup] = {}
        self.teams: Dict[str, List[str]] = {}  # team_id -> list of unit_ids
        self.update_log: List[Dict] = []

    def create_unit(
        self,
        name: str,
        unit_type: UnitType,
        position: Position,
        team_id: str = "",
        stats: Optional[UnitStats] = None
    ) -> Unit:
        """Create a new unit."""
        if stats is None:
            stats = self._get_default_stats(unit_type)

        unit = Unit(
            unit_id=str(uuid.uuid4()),
            name=name,
            unit_type=unit_type,
            stats=stats,
            position=position,
            team_id=team_id
        )

        self.units[unit.unit_id] = unit

        # Add to team tracking
        if team_id:
            if team_id not in self.teams:
                self.teams[team_id] = []
            self.teams[team_id].append(unit.unit_id)

        # Add default abilities
        self._add_default_abilities(unit)

        self.log_action(f"Unit created: {unit.name} ({unit.unit_type.value})")
        return unit

    def create_group(self, name: str, team_id: str = "") -> UnitGroup:
        """Create a new unit group."""
        group = UnitGroup(group_id=str(uuid.uuid4()), name=name, team_id=team_id)
        self.groups[group.group_id] = group
        self.log_action(f"Group created: {name}")
        return group

    def delete_unit(self, unit_id: str) -> bool:
        """Delete a unit."""
        if unit_id not in self.units:
            return False

        unit = self.units[unit_id]
        
        # Remove from team tracking
        if unit.team_id in self.teams:
            self.teams[unit.team_id].remove(unit_id)

        # Remove from groups
        for group in self.groups.values():
            group.remove_unit(unit_id)

        del self.units[unit_id]
        self.log_action(f"Unit deleted: {unit.name}")
        return True

    def delete_group(self, group_id: str) -> bool:
        """Delete a unit group."""
        if group_id not in self.groups:
            return False

        group = self.groups[group_id]
        self.log_action(f"Group deleted: {group.name}")
        del self.groups[group_id]
        return True

    def get_unit(self, unit_id: str) -> Optional[Unit]:
        """Get a unit by ID."""
        return self.units.get(unit_id)

    def get_group(self, group_id: str) -> Optional[UnitGroup]:
        """Get a group by ID."""
        return self.groups.get(group_id)

    def get_team_units(self, team_id: str) -> List[Unit]:
        """Get all units in a team."""
        unit_ids = self.teams.get(team_id, [])
        return [self.units[uid] for uid in unit_ids if uid in self.units]

    def get_alive_team_units(self, team_id: str) -> List[Unit]:
        """Get all alive units in a team."""
        return [u for u in self.get_team_units(team_id) if u.stats.is_alive()]

    def get_units_in_range(self, position: Position, radius: float) -> List[Unit]:
        """Get all units within a certain range of a position."""
        return [
            u for u in self.units.values()
            if u.position.distance_to(position) <= radius
        ]

    def get_enemy_units(self, unit_id: str) -> List[Unit]:
        """Get all enemy units relative to a unit."""
        unit = self.get_unit(unit_id)
        if not unit:
            return []

        return [
            u for u in self.units.values()
            if u.team_id != unit.team_id and u.stats.is_alive()
        ]

    def add_unit_to_group(self, unit_id: str, group_id: str) -> bool:
        """Add a unit to a group."""
        unit = self.get_unit(unit_id)
        group = self.get_group(group_id)

        if not unit or not group:
            return False

        return group.add_unit(unit)

    def remove_unit_from_group(self, unit_id: str, group_id: str) -> bool:
        """Remove a unit from a group."""
        group = self.get_group(group_id)
        if not group:
            return False

        return group.remove_unit(unit_id)

    def update_all_units(self, delta_time: float) -> None:
        """Update all units (called each frame/tick)."""
        for unit in self.units.values():
            if unit.stats.is_alive():
                # Update position
                unit.update_position(unit.stats.speed * delta_time)
                
                # Update effects
                unit.get_active_effects()
                
                # Restore resources over time
                unit.stats.restore_resource("mana", unit.stats.max_mana * 0.01 * delta_time)
                unit.stats.restore_resource("stamina", unit.stats.max_stamina * 0.02 * delta_time)

    def get_system_stats(self) -> Dict:
        """Get overall system statistics."""
        total_units = len(self.units)
        alive_units = sum(1 for u in self.units.values() if u.stats.is_alive())
        dead_units = total_units - alive_units

        return {
            "total_units": total_units,
            "alive_units": alive_units,
            "dead_units": dead_units,
            "total_groups": len(self.groups),
            "total_teams": len(self.teams),
            "actions_logged": len(self.update_log)
        }

    def get_all_units_info(self) -> List[Dict]:
        """Get information about all units."""
        return [u.get_info() for u in self.units.values()]

    def get_all_groups_info(self) -> List[Dict]:
        """Get information about all groups."""
        return [g.get_group_info() for g in self.groups.values()]

    def log_action(self, action: str) -> None:
        """Log a system action."""
        self.update_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "action": action
        })

    def get_action_log(self, limit: int = 100) -> List[Dict]:
        """Get the action log."""
        return self.update_log[-limit:]

    def clear_action_log(self) -> None:
        """Clear the action log."""
        self.update_log.clear()

    @staticmethod
    def _get_default_stats(unit_type: UnitType) -> UnitStats:
        """Get default stats for a unit type."""
        stats_map = {
            UnitType.SOLDIER: UnitStats(
                health=100, max_health=100,
                mana=20, max_mana=20,
                stamina=50, max_stamina=50,
                attack_power=15, defense=5, speed=5.0, accuracy=0.8
            ),
            UnitType.KNIGHT: UnitStats(
                health=150, max_health=150,
                mana=10, max_mana=10,
                stamina=60, max_stamina=60,
                attack_power=20, defense=15, speed=4.0, accuracy=0.7
            ),
            UnitType.ARCHER: UnitStats(
                health=60, max_health=60,
                mana=30, max_mana=30,
                stamina=70, max_stamina=70,
                attack_power=18, defense=2, speed=6.5, accuracy=0.95
            ),
            UnitType.MAGE: UnitStats(
                health=50, max_health=50,
                mana=100, max_mana=100,
                stamina=30, max_stamina=30,
                attack_power=5, defense=1, speed=4.5, accuracy=0.85
            ),
            UnitType.HEALER: UnitStats(
                health=70, max_health=70,
                mana=80, max_mana=80,
                stamina=40, max_stamina=40,
                attack_power=8, defense=3, speed=4.0, accuracy=0.8
            ),
            UnitType.TANK: UnitStats(
                health=200, max_health=200,
                mana=15, max_mana=15,
                stamina=50, max_stamina=50,
                attack_power=12, defense=20, speed=3.0, accuracy=0.6
            ),
        }
        return stats_map.get(unit_type, stats_map[UnitType.SOLDIER])

    @staticmethod
    def _add_default_abilities(unit: Unit) -> None:
        """Add default abilities to a unit based on type."""
        if unit.unit_type == UnitType.SOLDIER:
            unit.add_ability(Ability(
                ability_id=str(uuid.uuid4()),
                name="Slash",
                ability_type=AbilityType.ATTACK,
                damage=20,
                range=2,
                cost=10,
                description="Basic melee attack"
            ))
        elif unit.unit_type == UnitType.HEALER:
            unit.add_ability(Ability(
                ability_id=str(uuid.uuid4()),
                name="Heal",
                ability_type=AbilityType.HEAL,
                healing=50,
                range=5,
                cost=30,
                description="Restore health to a target"
            ))
        elif unit.unit_type == UnitType.MAGE:
            unit.add_ability(Ability(
                ability_id=str(uuid.uuid4()),
                name="Fireball",
                ability_type=AbilityType.SPELL,
                damage=40,
                range=8,
                cost=40,
                description="Powerful fire spell"
            ))
        elif unit.unit_type == UnitType.ARCHER:
            unit.add_ability(Ability(
                ability_id=str(uuid.uuid4()),
                name="Arrow Shot",
                ability_type=AbilityType.ATTACK,
                damage=25,
                range=10,
                cost=15,
                description="Ranged arrow attack"
            ))
        elif unit.unit_type == UnitType.TANK:
            unit.add_ability(Ability(
                ability_id=str(uuid.uuid4()),
                name="Shield Bash",
                ability_type=AbilityType.DEFEND,
                damage=10,
                range=2,
                cost=20,
                description="Defensive ability that reduces incoming damage"
            ))


# Example usage
if __name__ == "__main__":
    # Create manager
    manager = UnitManager()

    # Create some units
    soldier1 = manager.create_unit(
        name="Soldier1",
        unit_type=UnitType.SOLDIER,
        position=Position(0, 0),
        team_id="team_a"
    )

    soldier2 = manager.create_unit(
        name="Soldier2",
        unit_type=UnitType.SOLDIER,
        position=Position(5, 5),
        team_id="team_b"
    )

    mage = manager.create_unit(
        name="FireMage",
        unit_type=UnitType.MAGE,
        position=Position(10, 10),
        team_id="team_a"
    )

    healer = manager.create_unit(
        name="Healer1",
        unit_type=UnitType.HEALER,
        position=Position(2, 2),
        team_id="team_a"
    )

    # Create a group and add units
    group_a = manager.create_group(name="Squad A", team_id="team_a")
    manager.add_unit_to_group(soldier1.unit_id, group_a.group_id)
    manager.add_unit_to_group(mage.unit_id, group_a.group_id)
    manager.add_unit_to_group(healer.unit_id, group_a.group_id)

    # Test abilities
    fireball = mage.get_ability(list(mage.abilities.keys())[0])
    if fireball:
        mage.use_ability(fireball, soldier2)

    # Test movement
    soldier1.move_to(Position(5, 5))

    # Test group operations
    print("Group Info:", group_a.get_group_info())
    print("System Stats:", manager.get_system_stats())
    print("Action Log:", manager.get_action_log())
