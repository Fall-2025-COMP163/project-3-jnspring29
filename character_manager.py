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
    # TODO: Implement character creation
    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    
    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]
    
    # Raise InvalidCharacterClassError if class not in valid list

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
    # TODO: Implement save functionality
    # Create save_directory if it doesn't exist
    # Handle any file I/O errors appropriately
    # Lists should be saved as comma-separated values
# Make sure the save directory exists
    os.makedirs(save_directory, exist_ok=True)

    # Build the save file path using character's name
    filepath = os.path.join(save_directory, f"{character['name']}_save.txt")

    try:
        with open(filepath, "w") as f:
            for key, value in character.items():
                # If the value is a list (like inventory or quests), join it as comma-separated
                if isinstance(value, list):
                    value = ",".join(value)
                # Write the line as key:value
                f.write(f"{key}:{value}\n")
        return True
    except Exception as e:
        # Could log e here if needed
        return False
    
def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # TODO: Implement load functionality
    # Check if file exists → CharacterNotFoundError
    # Try to read file → SaveFileCorruptedError
    # Validate data format → InvalidSaveDataError
    # Parse comma-separated lists back into Python lists
filename = _save_filename(character_name, save_directory)
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"Character save not found for '{character_name}'.")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f]
    except Exception as exc:
        raise SaveFileCorruptedError(f"Could not read save file: {exc}")

    # Parse lines into a mapping
    data = {}
    for raw in lines:
        if ":" not in raw:
            continue
        key, _, value = raw.partition(":")
        data[key.strip().upper()] = value.strip()

    # Required fields
    required_keys = [
        "NAME",
        "CLASS",
        "LEVEL",
        "HEALTH",
        "MAX_HEALTH",
        "STRENGTH",
        "MAGIC",
        "EXPERIENCE",
        "GOLD",
        "INVENTORY",
        "ACTIVE_QUESTS",
        "COMPLETED_QUESTS",
    ]
    for rk in required_keys:
        if rk not in data:
            raise InvalidSaveDataError(f"Missing required field in save: {rk}")

    # Convert and validate types
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

    # Final validation of the loaded character
    try:
        validate_character_data(character)
    except InvalidSaveDataError as exc:
        raise InvalidSaveDataError(f"Loaded save is invalid: {exc}")

    return character

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    # Return empty list if directory doesn't exist
    # Extract character names from filenames
    if not os.path.exists(save_directory):
        return []
    files = os.listdir(save_directory)
    return [f.replace("_save.txt", "") for f in files if f.endswith("_save.txt")]

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion
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
    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    # Add experience
    # Check for level up (can level up multiple times)
    # Update stats on level up
    if character["health"] == 0:
        raise CharacterDeadError("Character is dead, cannot gain experience.")

# The while loop keeps leveling up the character until the experience equals the level * 100
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
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold
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
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
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
    
    Returns: True if dead, False if alive
    """
    # TODO: Implement death check
        return int(character.get("health", 0)) <= 0

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    # TODO: Implement revival
    # Restore health to half of max_health
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
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists
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

