"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Fixed Version

Name: Jessica Springer

AI Usage: No AI used
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *
from inventory_system import ItemNotFoundError, InvalidItemTypeError, InventoryFullError, InsufficientResourcesError

# ============================================================================
# GAME STATE
# ============================================================================

current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    print("\n=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")
    while True:
        choice = input("Choose (1-3): ").strip()
        if choice in ("1", "2", "3"):
            return int(choice)
        print("Please enter 1, 2, or 3.")

def new_game():
    global current_character
    print("\n=== NEW GAME ===")
    name = input("Enter character name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    print("Choose class: Warrior, Mage, Rogue, Cleric")
    cls = input("Class: ").strip().title()

    try:
        char = character_manager.create_character(name, cls)
    except InvalidCharacterClassError as e:
        print(f"Invalid class: {e}")
        return

    try:
        character_manager.save_character(char)
    except Exception as e:
        print(f"Warning: could not auto-save character: {e}")

    current_character = char
    print(f"Welcome, {char['name']} the {char['class']}!")
    game_loop()

def load_game():
    global current_character
    print("\n=== LOAD GAME ===")

    saves = character_manager.list_saved_characters()
    if not saves:
        print("No saved characters found.")
        return

    print("Saved characters:")
    for i, name in enumerate(saves, start=1):
        print(f"{i}. {name}")

    while True:
        choice = input(f"Select (1-{len(saves)}) or 'c' to cancel: ").strip()
        if choice.lower() == 'c':
            return
        if choice.isdigit() and 1 <= int(choice) <= len(saves):
            sel = saves[int(choice) - 1]
            try:
                char = character_manager.load_character(sel)
                current_character = char
                print(f"Loaded {char['name']} the {char['class']}.")
                game_loop()
                return
            except CharacterNotFoundError:
                print("Save not found.")
                return
            except SaveFileCorruptedError:
                print("Save file appears corrupted.")
                return
            except InvalidSaveDataError as e:
                print(f"Invalid save data: {e}")
                return
        print("Invalid selection.")

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    global game_running, current_character
    game_running = True
    while game_running:
        if current_character is None:
            print("No active character. Returning to main menu.")
            return

        choice = game_menu()

        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
            if current_character is None:
                return
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Saved. Returning to main menu.")
            return
        else:
            print("Invalid selection.")

        try:
            save_game()
        except Exception as e:
            print(f"Auto-save failed: {e}")

def game_menu():
    print("\n=== GAME MENU ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")

    while True:
        choice = input("Choose (1-6): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= 6:
            return int(choice)
        print("Please enter a number from 1 to 6.")

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    global current_character
    c = current_character
    if c is None:
        print("No character loaded.")
        return

    print("\n=== CHARACTER STATS ===")
    print(f"Name: {c['name']}")
    print(f"Class: {c['class']}")
    print(f"Level: {c['level']}  XP: {c['experience']}")
    print(f"HP: {c['health']}/{c['max_health']}")
    print(f"STR: {c['strength']}  MAG: {c['magic']}")
    print(f"Gold: {c['gold']}")
    print(f"Inventory slots: {len(c['inventory'])}/20")  # placeholder
    total_quests = len(all_quests)
    completed = len(c['completed_quests'])
    active = len(c['active_quests'])
    print(f"Quests: {active} active, {completed} completed ({total_quests} total)")

def view_inventory():
    global current_character, all_items
    c = current_character
    if c is None:
        print("No character loaded.")
        return
    # Minimal stub: just print inventory
    print("\n=== INVENTORY ===")
    if not c['inventory']:
        print("Inventory is empty.")
    else:
        for item in c['inventory']:
            print(f"- {item}")

def quest_menu():
    global current_character, all_quests
    c = current_character
    if c is None:
        print("No character loaded.")
        return
    print("\nQuest menu stub (replace with real quest logic)")

def explore():
    global current_character
    c = current_character
    if c is None:
        print("No character loaded.")
        return
    print("\nExploring... You encounter a monster!")
    # Minimal combat stub
    print("You won! Gained 10 XP and 5 gold.")
    character_manager.gain_experience(c, 10)
    character_manager.add_gold(c, 5)

def shop():
    global current_character, all_items
    c = current_character
    if c is None:
        print("No character loaded.")
        return
    print("\nShop stub (replace with real shop logic)")

# ============================================================================
# HELPERS
# ============================================================================

def save_game():
    global current_character
    if current_character is None:
        raise ValueError("No character to save.")
    character_manager.save_character(current_character)

def load_game_data():
    global all_quests, all_items
    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except Exception:
        # Fallback minimal data
        all_quests = {"quest_001": {"name": "Test Quest"}}
        all_items = {"item_001": {"name": "Test Item", "type": "consumable", "cost": 5}}

def display_welcome():
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!\n")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    display_welcome()
    load_game_data()
    while True:
        choice = main_menu()
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
