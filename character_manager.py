"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Jessica Springer]

AI Usage: AI used for debugging

This module handles character creation, loading, and saving.
"""
import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError 
    CharacterDeadError
)

# =============================================================================

# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

VALID_CLASSES = {
    "Warrior": {"health": 120, "strength": 15, "magic": 5},
    "Mage": {"health": 80, "strength": 8, "magic": 20},
    "Rogue": {"health": 90, "strength": 12, "magic": 10},
    "Cleric": {"health": 100, "strength": 10, "magic": 15},
}

def create_character(name, character_class):
    if character_class not in VALID_CLASSES:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    base = VALID_CLASSES[character_class]
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    valid_classes = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15},
    }

    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")

    base = valid_classes[character_class]

    character = {
        "name": name,
        "class": character_class,
@@ -46,62 +60,133 @@
        "active_quests": [],
        "completed_quests": []
    }

    return character

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    

    filename = os.path.join(save_directory, f"{character['name']}_save.txt")
    

    try:
        with open(filename, "w", encoding="utf-8") as f:
            for key in ["name", "class", "level", "health", "max_health", "strength", "magic", "experience", "gold"]:
                f.write(f"{key.upper()}: {character[key]}\n")
            # Save lists as comma-separated
            for key in ["inventory", "active_quests", "completed_quests"]:
                f.write(f"{key.upper()}: {','.join(character[key])}\n")
        return True
        with open(filename, "w") as file:
            file.write(f"NAME: {character['name']}\n")
            file.write(f"CLASS: {character['class']}\n")
            file.write(f"LEVEL: {character['level']}\n")
            file.write(f"HEALTH: {character['health']}\n")
            file.write(f"MAX_HEALTH: {character['max_health']}\n")
            file.write(f"STRENGTH: {character['strength']}\n")
            file.write(f"MAGIC: {character['magic']}\n")
            file.write(f"EXPERIENCE: {character['experience']}\n")
            file.write(f"GOLD: {character['gold']}\n")
            file.write(f"INVENTORY: {','.join(character['inventory']) if character['inventory'] else ''}\n")
            file.write(f"ACTIVE_QUESTS: {','.join(character['active_quests']) if character['active_quests'] else ''}\n")
            file.write(f"COMPLETED_QUESTS: {','.join(character['completed_quests']) if character['completed_quests'] else ''}\n")
    except Exception as e:
        raise e

    return True

def load_character(character_name, save_directory="data/save_games"):
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"{character_name} save file not found")
    
        raise CharacterNotFoundError(f"No save file found for {character_name}")

    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except:
        raise SaveFileCorruptedError(f"Could not read save file for {character_name}")

    character = {}

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if ": " not in line:
                    continue
                key, value = line.strip().split(": ", 1)
                key = key.lower()
                if key in ["level", "health", "max_health", "strength", "magic", "experience", "gold"]:
                    character[key] = int(value)
                elif key in ["inventory", "active_quests", "completed_quests"]:
                    character[key] = value.split(",") if value else []
                else:
                    character[key] = value
    except Exception as e:
        raise SaveFileCorruptedError(f"Failed to read save file: {e}")
    
    if not validate_character_data(character):
        raise InvalidSaveDataError("Save file data is invalid")
    
        for line in lines:
            line = line.strip()
            if not line:
                continue

            if ":" not in line:
                raise InvalidSaveDataError("Missing ':' in save data")

            # --- Safe split (fixes your failing test) ---
            if ": " in line:
                key, value = line.split(": ", 1)
            else:
                key, value = line.split(":", 1)
                value = value.lstrip()
            # --------------------------------------------

            # Lists
            if key in ("INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"):
                character[key.lower()] = value.split(",") if value else []

            # Integers
            elif key in ("LEVEL", "HEALTH", "MAX_HEALTH", "STRENGTH", "MAGIC", "EXPERIENCE", "GOLD"):
                character[key.lower()] = int(value)

            # Strings
            else:
                character[key.lower()] = value

    except Exception:
        raise InvalidSaveDataError("Save file format incorrect")

    validate_character_data(character)
    return character

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    if not os.path.exists(save_directory):
        return []
    files = [f[:-9] for f in os.listdir(save_directory) if f.endswith("_save.txt")]
    return files

    names = []
    for filename in os.listdir(save_directory):
        if filename.endswith("_save.txt"):
            names.append(filename.replace("_save.txt", ""))

    return names

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"{character_name} save file not found")
        raise CharacterNotFoundError(f"No save file for {character_name}")

    os.remove(filename)
    return True

@@ -110,39 +195,74 @@
# ============================================================================

def gain_experience(character, xp_amount):
    if is_character_dead(character):
        raise CharacterDeadError(f"{character['name']} is dead and cannot gain XP")
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    if character["health"] <= 0:
        raise CharacterDeadError("Character is dead and cannot gain XP.")

    character["experience"] += xp_amount
    # Level up while experience >= level * 100

    leveled_up = False

    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]
        leveled_up = True

    return leveled_up

def add_gold(character, amount):
    new_gold = character["gold"] + amount
    if new_gold < 0:
        raise ValueError("Gold cannot be negative")
    character["gold"] = new_gold
    return new_gold
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    new_total = character["gold"] + amount
    if new_total < 0:
        raise ValueError("Gold cannot be negative.")
    character["gold"] = new_total
    return character["gold"]

def heal_character(character, amount):
    if amount < 0:
        return 0
    healed = min(amount, character["max_health"] - character["health"])
    character["health"] += healed
    return healed

    old_health = character["health"]
    character["health"] = min(character["health"] + amount, character["max_health"])
    return character["health"] - old_health

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    return character["health"] <= 0

def revive_character(character):
    if not is_character_dead(character):
        return False

    character["health"] = character["max_health"] // 2
    return True

@@ -151,32 +271,55 @@
# ============================================================================

def validate_character_data(character):
    required_keys = [
    required = {
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]
    for key in required_keys:
        if key not in character:
            raise InvalidSaveDataError(f"Missing key: {key}")
    
    for key in ["level", "health", "max_health", "strength", "magic", "experience", "gold"]:
        if not isinstance(character[key], int):
            raise InvalidSaveDataError(f"{key} must be an integer")
    
    for key in ["inventory", "active_quests", "completed_quests"]:
        if not isinstance(character[key], list):
            raise InvalidSaveDataError(f"{key} must be a list")
    
    }

    for field in required:
        if field not in character:
            raise InvalidSaveDataError(f"Missing field: {field}")

    numeric_fields = ["level", "health", "max_health", "strength", "magic", "experience", "gold"]
    for field in numeric_fields:
        if not isinstance(character[field], int):
            raise InvalidSaveDataError(f"{field} must be an integer")

    list_fields = ["inventory", "active_quests", "completed_quests"]
    for field in list_fields:
        if not isinstance(character[field], list):
            raise InvalidSaveDataError(f"{field} must be a list")

    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    char = create_character("TestHero", "Warrior")
    print(f"Created: {char['name']} the {char['class']}")
    save_character(char)
    loaded = load_character("TestHero")
    print(f"Loaded: {loaded['name']} HP={loaded['health']}")
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")
