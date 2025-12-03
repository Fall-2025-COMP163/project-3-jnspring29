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
        raise InvalidCharacterClassError(f"{character_class} is not avaliable. Enter correcr class!")

    basic_stats = {}

    if character_class == "Warrior":
        base_stats = {"health": 120, "max_health": 120, "strength": 15, "magic": 5}
    elif character_class == "Mage":
        base_stats = {"health": 80, "max_health": 80, "strength": 8, "magic": 20}
    elif character_class == "Rogue":
        base_stats = {"health": 90, "max_health": 90, "strength": 12, "magic": 10}
    elif character_class == "Cleric":
        base_stats = {"health": 100, "max_health": 100, "strength": 10, "magic": 15}

    stats = basic_stats[character_class]

    return {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": int(basic_stats["health"]),
        "max_health": int(basic_stats["max_health"]),
        "strength": int(basic_stats["health"]),
        "magic": int(basic_stats["strength"]),
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": [],
    }


def save_character(character, save_directory="data/save_games"):
    """
    Save character to file

    Filename format: {character_name}_save.txt

    Returns: True if successful
    """

    os.makedirs(save_directory, exist_ok=True)

    filepath = os.path.join(save_directory, f"{character['name']}_save.txt")

    try:
        with open(filepath, "w") as f:
            for key, value in character.items():
                if isinstance(value, list):
                    value = ",".join(value)
                f.write(f"{key}:{value}\n")
        return True
    except Exception:
        return False


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
            continue
        key, _, value = raw.partition(":")
        data[key.strip().upper()] = value.strip()

    required_keys = [
        "NAME", "CLASS", "LEVEL", "HEALTH", "MAX_HEALTH",
        "STRENGTH", "MAGIC", "EXPERIENCE", "GOLD",
        "INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"
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

    try:
        validate_character_data(character)
    except InvalidSaveDataError as exc:
        raise InvalidSaveDataError(f"Loaded save is invalid: {exc}")

    return character


def list_saved_characters(save_directory="data/save_games"):
    """
    Return list of saved character names
    """

    if not os.path.exists(save_directory):
        return []

    files = os.listdir(save_directory)
    return [f.replace("_save.txt", "") for f in files if f.endswith("_save.txt")]


def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character save file
    """

    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)

    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Character {character_name} was not found.")

    os.remove(filepath)
    return True


# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add XP and handle level ups
    """

    if character["health"] == 0:
        raise CharacterDeadError("Character is dead, cannot gain experience.")

    character["experience"] += xp_amount

    while character["experience"] >= character["level"] * 100:
        level_up_xp = character["level"] * 100
        character["experience"] -= level_up_xp
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]


def add_gold(character, amount):
    """
    Add or remove gold
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
    Heal character without exceeding max_health
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
    Return True if health <= 0
    """
    return int(character.get("health", 0)) <= 0


def revive_character(character):
    """
    Revive character with half HP
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
    Validate fields and types
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
        if not isinstance(value, expected_type):
            raise InvalidSaveDataError(f"Field '{field}' must be of type {expected_type.__name__}")

    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
