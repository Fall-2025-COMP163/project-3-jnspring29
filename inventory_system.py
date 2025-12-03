"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module

Name: Jessica Springer

AI Usage: Implemented with ChatGPT assistance

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """Add an item to character's inventory"""
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")
    character["inventory"].append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    """Remove an item from character's inventory"""
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")
    character["inventory"].remove(item_id)
    return True

def has_item(character, item_id):
    """Check if character has a specific item"""
    return item_id in character["inventory"]

def count_item(character, item_id):
    """Count how many of a specific item the character has"""
    return character["inventory"].count(item_id)

def get_inventory_space_remaining(character):
    """Calculate how many more items can fit in inventory"""
    return MAX_INVENTORY_SIZE - len(character["inventory"])

def clear_inventory(character):
    """Remove all items from inventory"""
    removed = character["inventory"].copy()
    character["inventory"].clear()
    return removed

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """Use a consumable item from inventory"""
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not found.")
    if item_data["type"] != "consumable":
        raise InvalidItemTypeError("Only consumable items can be used.")

    stat, value = parse_item_effect(item_data["effect"])
    apply_stat_effect(character, stat, value)
    remove_item_from_inventory(character, item_id)

    return f"{character['name']} used {item_id} and gained {stat} +{value}."

def equip_weapon(character, item_id, item_data):
    """Equip a weapon"""
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not found.")
    if item_data["type"] != "weapon":
        raise InvalidItemTypeError("Item is not a weapon.")

    # Unequip current weapon
    if character.get("equipped_weapon"):
        unequip_weapon(character)

    stat, val = parse_item_effect(item_data["effect"])
    apply_stat_effect(character, stat, val)

    character["equipped_weapon"] = item_id
    character["equipped_weapon_effect"] = item_data["effect"]

    remove_item_from_inventory(character, item_id)
    return f"{character['name']} equipped weapon: {item_id} (+{val} {stat})"

def equip_armor(character, item_id, item_data):
    """Equip armor"""
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not found.")
    if item_data["type"] != "armor":
        raise InvalidItemTypeError("Item is not armor.")

    # Unequip current armor
    if character.get("equipped_armor"):
        unequip_armor(character)

    stat, val = parse_item_effect(item_data["effect"])
    apply_stat_effect(character, stat, val)

    character["equipped_armor"] = item_id
    character["equipped_armor_effect"] = item_data["effect"]

    remove_item_from_inventory(character, item_id)
    return f"{character['name']} equipped armor: {item_id} (+{val} {stat})"

def unequip_weapon(character):
    """Remove equipped weapon and return it to inventory"""
    item_id = character.get("equipped_weapon")
    if not item_id:
        return None
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("No space to unequip weapon.")

    stat, val = parse_item_effect(character["equipped_weapon_effect"])
    apply_stat_effect(character, stat, -val)

    add_item_to_inventory(character, item_id)
    character["equipped_weapon"] = None
    character["equipped_weapon_effect"] = None
    return item_id

def unequip_armor(character):
    """Remove equipped armor and return it to inventory"""
    item_id = character.get("equipped_armor")
    if not item_id:
        return None
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("No space to unequip armor.")

    stat, val = parse_item_effect(character["equipped_armor_effect"])
    apply_stat_effect(character, stat, -val)

    add_item_to_inventory(character, item_id)
    character["equipped_armor"] = None
    character["equipped_armor_effect"] = None
    return item_id

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """Purchase an item from a shop"""
    cost = item_data["cost"]
    if character["gold"] < cost:
        raise InsufficientResourcesError("Not enough gold.")
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Inventory is full.")

    character["gold"] -= cost
    add_item_to_inventory(character, item_id)
    return True

def sell_item(character, item_id, item_data):
    """Sell an item for half its purchase cost"""
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not found.")
    sell_value = item_data["cost"] // 2
    remove_item_from_inventory(character, item_id)
    character["gold"] += sell_value
    return sell_value

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """Parse item effect string into stat name and value"""
    try:
        stat, value = effect_string.split(":")
        return stat, int(value)
    except Exception:
        raise ValueError(f"Invalid item effect format: {effect_string}")

def apply_stat_effect(character, stat_name, value):
    """Apply a stat modification to character"""
    if stat_name not in character:
        raise KeyError(f"Unknown stat: {stat_name}")

    character[stat_name] += value
    if stat_name == "health":
        character["health"] = max(0, min(character["health"], character["max_health"]))

def display_inventory(character, item_data_dict):
    """Display character's inventory in formatted way"""
    print("\n=== INVENTORY ===")
    if not character["inventory"]:
        print("Inventory is empty.")
        return

    counted = {}
    for item_id in character["inventory"]:
        counted[item_id] = counted.get(item_id, 0) + 1

    for item_id in sorted(counted):
        item = item_data_dict.get(item_id, {"name": "Unknown", "type": "unknown"})
        print(f"{item['name']} (x{counted[item_id]}) - {item['type']}")

# ============================================================================
# CHARACTER INITIALIZATION HELPER
# ============================================================================

def initialize_character_inventory(character):
    """Ensure character has all inventory/equipment keys"""
    keys = [
        "inventory", "equipped_weapon", "equipped_weapon_effect",
        "equipped_armor", "equipped_armor_effect"
    ]
    for key in keys:
        if key not in character:
            character[key] = None if "equipped" in key else []

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    # Example test character
    char = {
        "name": "TestHero",
        "health": 100,
        "max_health": 100,
        "strength": 10,
        "magic": 5,
        "gold": 50
    }
    initialize_character_inventory(char)

    # Add items
    add_item_to_inventory(char, "health_potion")
    print(char["inventory"])

    # Equip weapon
    add_item_to_inventory(char, "iron_sword")
    print(equip_weapon(char, "iron_sword", {"type": "weapon", "effect": "strength:5"}))
    print(char["strength"])

    # Use consumable
    char["health"] = 50
    add_item_to_inventory(char, "health_potion")
    print(use_item(char, "health_potion", {"type": "consumable", "effect": "health:30"}))
    print(char["health"])
