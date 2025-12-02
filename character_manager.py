"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Jessica Springer

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""
#Used AI to debug code


"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Jessica Springer

AI Usage: Debugging + syntax fixes
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
# HELPER FUNCTIONS (you were calling these but never defined them!)
# ============================================================================

def _save_filename(character_name, save_directory):
    return os.path.join(save_directory, f"{character_name}_save.txt")

def _list_from_csv(value):
    if value.strip() == "":
        return []
    return [item.strip() for item in value.split(",")]


# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    """
    valid_char_class = ["Warrior", "Mage", "Rogue", "Cleric"]

    if character_class not in valid_char_class:
        raise InvalidCharacterClassError(f"{character_class} is not available. Enter correct class!")

    # Correct base_stats dictionary
    base_stats_lookup = {
        "Warrior": {"health": 120, "max_health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "max_health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "max_health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "max_health": 100, "strength": 10, "magic": 15}
    }

    base_stats = base_stats_lookup[character_class]

    return {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": base_stats["health"],
        "max_health": base_stats["max_health"],
        "strength": base_stats["strength"],
        "magic": base_stats["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": [],
    }


def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    """
    os.makedirs(save_directory, exist_ok=True)
    filepath = _save_filename(character["name"], save_directory)

    try:
        with open(filepath, "w") as f:
            for key, value in character.items():
                if isinstance(value, list):
                    value = ",".join(value)
                f.write(f"{key}:{value}\n")
        return True
    except Exception:
        raise SaveFileCorruptedError("Failed to save character.")


def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    """
    filename = _save_filename(character_name, save_directory)

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"Character save not found for '{character_name}'.")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f]
    except Exception as exc:
        raise SaveFileCorruptedError(f"Could not read save file: {exc}")

    data = {}

    for raw in lines:
        if ":" not in raw:
            raise SaveFileCorruptedError("Missing ':' in save file.")
        key, _, value = raw.partition(":")
        data[key.strip().upper()] = value.strip()

    required_keys = [
        "NAME", "CLASS", "LEVEL", "HEALTH", "MAX_HEALTH",
        "STRENGTH", "MAGIC", "EXPERIENCE", "GOLD",
        "INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"
    ]

    for rk in required_keys:
        if rk not in data:
            raise InvalidSaveDataError(f"Missing required field: {rk}")

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
            "inventory": _list_from_csv(data["INVENTORY"]),
            "active_quests": _list_from_csv(data["ACTIVE_QUESTS"]),
            "completed_quests": _list_from_csv(data["COMPLETED_QUESTS"]),
        }
    except ValueError as exc:
        raise InvalidSaveDataError(f"Invalid numeric value: {exc}")

    validate_character_data(character)
    return character


def list_saved_characters(save_directory="data/save_games"):
    if not os.path.exists(save_directory):
        return []
    files = os.listdir(save_directory)
    return [f.replace("_save.txt", "") for f in files if f.endswith("_save.txt")]


def delete_character(character_name, save_directory="data/save_games"):
    filename = _save_filename(character_name, save_directory)

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"Character {character_name} was not found.")

    os.remove(filename)
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    if character["health"] == 0:
        raise CharacterDeadError("Character is dead, cannot gain experience.")

    character["experience"] += xp_amount

    while character["experience"] >= character["level"] * 100:
        required_xp = character["level"] * 100
        character["experience"] -= required_xp
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]


def add_gold(character, amount):
    if not isinstance(amount, (int, float)):
        raise ValueError("Amount must be a number.")

    new_total = character["gold"] + int(amount)

    if new_total < 0:
        raise ValueError("Not enough gold.")

    character["gold"] = new_total
    return character["gold"]


def heal_character(character, amount):
    if amount <= 0:
        return 0

    max_h = character["max_health"]
    current = character["health"]

    healed = min(amount, max_h - current)
    character["health"] = current + healed

    return healed


def is_character_dead(character):
    return character["health"] <= 0


def revive_character(character):
    if not is_character_dead(character):
        return False

    revive_hp = max(1, character["max_health"] // 2)
    character["health"] = revive_hp
    return True


# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
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
        if not isinstance(value, expected_type):
            raise InvalidSaveDataError(f"Field '{field}' must be {expected_type.__name__}")

    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
