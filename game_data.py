"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Jessica Springer

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# HELPERS
# ============================================================================

def _save_filename(character_name, save_directory):
    return os.path.join(save_directory, f"{character_name}_save.txt")

def _list_from_csv(csv_str):
    """Convert comma-separated string to list, trimming spaces. Empty -> []"""
    csv_str = csv_str.strip()
    if csv_str == "":
        return []
    return [item.strip() for item in csv_str.split(",") if item.strip()]

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class

    Valid classes: Warrior, Mage, Rogue, Cleric

    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests

    Raises: InvalidCharacterClassError if class is not valid
    """
    valid_char_class = ["Warrior", "Mage", "Rogue", "Cleric"]

    if character_class not in valid_char_class:
        raise InvalidCharacterClassError(f"{character_class} is not available. Enter correct class!")

    if character_class == "Warrior":
        base_stats = {"health": 120, "max_health": 120, "strength": 15, "magic": 5}
    elif character_class == "Mage":
        base_stats = {"health": 80, "max_health": 80, "strength": 8, "magic": 20}
    elif character_class == "Rogue":
        base_stats = {"health": 90, "max_health": 90, "strength": 12, "magic": 10}
    elif character_class == "Cleric":
        base_stats = {"health": 100, "max_health": 100, "strength": 10, "magic": 15}

    return {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": int(base_stats["health"]),
        "max_health": int(base_stats["max_health"]),
        "strength": int(base_stats["strength"]),
        "magic": int(base_stats["magic"]),
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": [],
    }


def save_character(character, save_directory="data/save_games"):
    """
    Save character to file using uppercase keys expected by loader.
    Returns True if successful, raises exceptions on I/O issues.
    """
    os.makedirs(save_directory, exist_ok=True)
    filepath = _save_filename(character["name"], save_directory)

    # Map character dict keys to the exact labels we want in file
    lines_map = {
        "NAME": character.get("name", ""),
        "CLASS": character.get("class", ""),
        "LEVEL": character.get("level", 0),
        "HEALTH": character.get("health", 0),
        "MAX_HEALTH": character.get("max_health", 0),
        "STRENGTH": character.get("strength", 0),
        "MAGIC": character.get("magic", 0),
        "EXPERIENCE": character.get("experience", 0),
        "GOLD": character.get("gold", 0),
        "INVENTORY": ",".join(character.get("inventory", [])),
        "ACTIVE_QUESTS": ",".join(character.get("active_quests", [])),
        "COMPLETED_QUESTS": ",".join(character.get("completed_quests", [])),
    }

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            for key in [
                "NAME","CLASS","LEVEL","HEALTH","MAX_HEALTH","STRENGTH","MAGIC",
                "EXPERIENCE","GOLD","INVENTORY","ACTIVE_QUESTS","COMPLETED_QUESTS"
            ]:
                f.write(f"{key}: {lines_map[key]}\n")
        return True
    except Exception:
        # Let caller decide how to handle logging; return False to indicate failure
        return False

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file

    Raises:
        CharacterNotFoundError, SaveFileCorruptedError, InvalidSaveDataError
    """
    filename = _save_filename(character_name, save_directory)
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"Character save not found for '{character_name}'.")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f]
    except Exception as exc:
        raise SaveFileCorruptedError(f"Could not read save file: {exc}")

    # Parse into dict (keys uppercased for consistency)
    data = {}
    for raw in lines:
        if ":" not in raw:
            continue
        key, _, value = raw.partition(":")
        data[key.strip().upper()] = value.strip()

    required_keys = [
        "NAME","CLASS","LEVEL","HEALTH","MAX_HEALTH","STRENGTH","MAGIC",
        "EXPERIENCE","GOLD","INVENTORY","ACTIVE_QUESTS","COMPLETED_QUESTS"
    ]
    for rk in required_keys:
        if rk not in data:
            raise InvalidSaveDataError(f"Missing required field in save: {rk}")

    try:
        character = {
            "name": data["NAME"],
            "class": data["CLASS"],
            "level": int(data["LEVEL"]),
            "health": int(data["HEALTH"]),
            "max_health": int(data["MAX_HEALTH"]),
            "strength": int(data["STRENGTH"]),
            "magic": int(data["MAGIC"]),
            "experience": int(data["EXPERIENCE"]),
            "gold": int(data["GOLD"]),
            "inventory": _list_from_csv(data.get("INVENTORY", "")),
            "active_quests": _list_from_csv(data.get("ACTIVE_QUESTS", "")),
            "completed_quests": _list_from_csv(data.get("COMPLETED_QUESTS", "")),
        }
    except ValueError as exc:
        raise InvalidSaveDataError(f"Invalid numeric value in save file: {exc}")

    # Validate loaded data
    validate_character_data(character)

    return character

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names (without suffix)
    """
    if not os.path.exists(save_directory):
        return []
    files = os.listdir(save_directory)
    return [f.replace("_save.txt", "") for f in files if f.endswith("_save.txt")]

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    """
    filename = _save_filename(character_name, save_directory)
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"Character {character_name} was not found.")
    os.remove(filename)
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups.
    Raises: CharacterDeadError if character health is 0
    """
    if character.get("health", 0) <= 0:
        raise CharacterDeadError("Character is dead, cannot gain experience.")

    if xp_amount <= 0:
        return

    character["experience"] = int(character.get("experience", 0)) + int(xp_amount)

    # Loop to allow multiple level-ups
    while character["experience"] >= character["level"] * 100:
        level_up_xp = character["level"] * 100
        character["experience"] -= level_up_xp
        character["level"] += 1
        character["max_health"] = int(character.get("max_health", 0)) + 10
        character["strength"] = int(character.get("strength", 0)) + 2
        character["magic"] = int(character.get("magic", 0)) + 2
        character["health"] = character["max_health"]

def add_gold(character, amount):
    """
    Add gold to character; raising ValueError if result would be negative.
    """
    if not isinstance(amount, (int, float)):
        raise ValueError("amount must be a number.")
    current = int(character.get("gold", 0))
    new_total = current + int(amount)
    if new_total < 0:
        raise ValueError("Not enough gold.")
    character["gold"] = new_total
    return character["gold"]

def heal_character(character, amount):
    """
    Heal character by specified amount; cannot exceed max_health.
    Returns actual amount healed.
    """
    if amount <= 0:
        return 0
    max_h = int(character.get("max_health", 0))
    current = int(character.get("health", 0))
    if current >= max_h:
        return 0
    healed = min(int(amount), max_h - current)
    character["health"] = current + healed
    return healed

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    """
    return int(character.get("health", 0)) <= 0

def revive_character(character):
    """
    Revive a dead character with 50% health (minimum 1).
    """
    if not is_character_dead(character):
        return False
    max_h = int(character.get("max_health", 0))
    revive_hp = max(1, max_h // 2)
    character["health"] = revive_hp
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields and types.
    Raises InvalidSaveDataError if invalid.
    """
    required_fields = {
        "name": str,
        "class": str,
        "level": int,
        "health": int,
        "max_health": int,
        "strength": int,
        "magic": int,
        "experience": int,
        "gold": int,
        "inventory": list,
        "active_quests": list,
        "completed_quests": list
    }

    for field, expected_type in required_fields.items():
        if field not in character:
            raise InvalidSaveDataError(f"Missing required field: {field}")
        value = character[field]
        # For ints accept values that are int-like (but prefer strict)
        if expected_type is int:
            if not isinstance(value, int):
                raise InvalidSaveDataError(f"Field '{field}' must be of type int")
        elif expected_type is list:
            if not isinstance(value, list):
                raise InvalidSaveDataError(f"Field '{field}' must be of type list")
        else:
            if not isinstance(value, expected_type):
                raise InvalidSaveDataError(f"Field '{field}' must be of type {expected_type.__name__}")

    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    try:
        char = create_character("TestHero", "Warrior")
        print(f"Created: {char['name']} the {char['class']}")
        print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
        save_character(char)
        print("Saved TestHero.")
        loaded = load_character("TestHero")
        print("Loaded:", loaded["name"], loaded["level"])
        gain_experience(loaded, 250)  # should trigger at least two level-ups
        print("After XP:", loaded["level"], "HP:", loaded["health"], "EXP:", loaded["experience"])
    except Exception as e:
        print("Error during test:", e)
