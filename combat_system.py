"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Jessica Springer

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward
    enemies = {
        "goblin": {
            "name": "Goblin",
            "type": "Goblin",
            "health": 30,
            "max_health": 30,
            "strength": 5,
            "magic": 0,
            "xp_reward": 10,
            "gold_reward": 5
        },
        "orc": {
            "name": "Orc",
            "type": "Orc",
            "health": 50,
            "max_health": 50,
            "strength": 12,
            "magic": 2,
            "xp_reward": 20,
            "gold_reward": 12
        }
    }

    enemy_type = enemy_type.lower()  # normalize input

    if enemy_type not in enemies:
        raise InvalidTargetError(f"Unknown enemy: {enemy_type}")

    # Return a new dictionary so modifications in battle don't affect template
    e = enemies[enemy_type]
    return {
        "name": e["name"],
        "type": e["type"],
        "health": e["health"],
        "max_health": e["max_health"],
        "strength": e["strength"],
        "magic": e["magic"],
        "xp_reward": e["xp_reward"],
        "gold_reward": e["gold_reward"]
    }

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    if character_level <= 2:
        enemy_type = "goblin"
    elif 3 <= character_level <= 5:
        enemy_type = "orc"
    else:
        enemy_type = "dragon"
    
    # Create and return the enemy
    return create_enemy(enemy_type)


# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # Store both participants
        self.character = character
        self.enemy = enemy

        # Combat is active when battle starts
        self.combat_active = True

        # Track turns (character = odd turns, enemy = even turns, if needed)
        self.turn_count = 1
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        def start_battle(self):
    """
    Start the combat loop
    
    Returns: Dictionary with battle results:
            {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
    
    Raises: CharacterDeadError if character is already dead
    """
    # Check if character is already dead
    if self.character["health"] <= 0:
        raise CharacterDeadError("Character cannot fight because they are dead.")

    # Extract needed stats
    player = self.character
    enemy = self.enemy

    # Main combat loop
    while self.combat_active:

        # --- Player Turn ---
        enemy["health"] -= player["strength"]

        if enemy["health"] <= 0:
            # Player won
            xp = enemy.get("xp_reward", 0)
            gold = enemy.get("gold_reward", 0)

            # Award rewards
            player["experience"] += xp
            player["gold"] += gold

            self.combat_active = False

            return {
                "winner": "player",
                "xp_gained": xp,
                "gold_gained": gold
            }

        # --- Enemy Turn ---
        player["health"] -= enemy

    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        if not self.combat_active:
        raise CombatNotActiveError("Cannot act because combat is not active.")

    player = self.character
    enemy = self.enemy

    print("\n=== PLAYER TURN ===")
    print(f"Enemy HP: {enemy['health']}")
    print("1. Basic Attack")
    print("2. Special Ability")
    print("3. Run Away")

    choice = input("Choose an action (1-3): ").strip()

    # -------------------------
    # ATTACK 1: BASIC ATTACK
    # -------------------------
    if choice == "1":
        damage = player["strength"]
        enemy["health"] -= damage
        print(f"You strike the {enemy['type']} for {damage} damage!")

        if enemy["health"] <= 0:
            print("Enemy defeated!")

        return "attack"
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        if not self.combat_active:
        raise CombatNotActiveError("Cannot act because combat is not active.")

    enemy = self.enemy
    player = self.character

    # Enemy attack
    damage = enemy.get("strength", 0)
    player["health"] -= damage

    print(f"The {enemy.get('type', 'enemy')} attacks you for {damage} damage!")

    # Check if player is dead
    if player["health"] <= 0:
        print("You have been defeated!")
        self.combat_active = False

    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        # Get attacker and defender strength, default to 0 if missing
    atk = attacker.get("strength", 0)
    defn = defender.get("strength", 0)

    # Calculate damage
    damage = atk - (defn // 4)

    # Ensure minimum damage is 1
    if damage < 1:
        damage = 1

    return damage
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
         if not isinstance(damage, (int, float)) or damage < 0:
        raise ValueError("Damage must be a non-negative number.")

    current_hp = target.get("health", 0)
    new_hp = max(0, current_hp - int(damage))  # Prevent negative health
    target["health"] = new_hp

    return new_hp
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        if self.enemy.get("health", 0) <= 0:
        self.combat_active = False
        return "player"
    elif self.character.get("health", 0) <= 0:
        self.combat_active = False
        return "enemy"
    else:
        return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
         if not self.combat_active:
        return False  # Cannot escape if battle is already inactive

    success = random.random() < 0.5  # 50% chance

    if success:
        print("You successfully escaped the battle!")
        self.combat_active = False
    else:
        print("Escape failed! The battle continues.")

    return success

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    char_class = character.get("class", "").lower()
    result_msg = ""
    
    if char_class == "warrior":
        damage = character.get("strength", 0) * 2
        enemy["health"] = max(0, enemy.get("health", 0) - damage)
        result_msg = f"Warrior uses Power Strike! Deals {damage} damage to {enemy.get('type','enemy')}."

    elif char_class == "mage":
        damage = character.get("magic", 0) * 2
        enemy["health"] = max(0, enemy.get("health", 0) - damage)
        result_msg = f"Mage casts Fireball! Deals {damage} damage to {enemy.get('type','enemy')}."

    elif char_class == "rogue":
        if random.random() < 0.5:  # 50% chance
            damage = character.get("strength", 0) * 3
            enemy["health"] = max(0, enemy.get("health", 0) - damage)
            result_msg = f"Rogue lands a Critical Strike! Deals {damage} damage."
        else:
            damage = 0
            result_msg = "Rogue's Critical Strike missed!"

    elif char_class == "cleric":
        heal_amount = 30
        max_health = character.get("max_health", 0)
        current_health = character.get("health", 0)
        actual_heal = min(heal_amount, max_health - current_health)
        character["health"] = current_health + actual_heal
        result_msg = f"Cleric casts Heal! Restores {actual_heal} health."

    else:
        result_msg = "No special ability available for this class."

    return result_msg


def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    # Calculate damage
    damage = character.get("strength", 0) * 2
    
    # Apply damage to enemy
    enemy["health"] = max(0, enemy.get("health", 0) - damage)
    
    return f"Warrior uses Power Strike! Deals {damage} damage to {enemy.get('type','enemy')}."

def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
        # Calculate damage
    damage = character.get("magic", 0) * 2
    
    # Apply damage to enemy
    enemy["health"] = max(0, enemy.get("health", 0) - damage)
    
    return f"Mage casts Fireball! Deals {damage} damage to {enemy.get('type','enemy')}."


def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    if random.random() < 0.5:  # 50% chance to hit
        damage = character.get("strength", 0) * 3
        enemy["health"] = max(0, enemy.get("health", 0) - damage)
        return f"Rogue lands a Critical Strike! Deals {damage} damage to {enemy.get('type','enemy')}."
    else:
        return "Rogue's Critical Strike missed!"


def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    heal_amount = 30
    max_health = character.get("max_health", 0)
    current_health = character.get("health", 0)
    
    # Calculate actual healing without exceeding max_health
    actual_heal = min(heal_amount, max_health - current_health)
    character["health"] = current_health + actual_heal
    
    return f"Cleric casts Heal! Restores {actual_heal} health."


# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    # Ensure character has 'health' and 'in_battle' keys
    health = character.get("health", 0)
    in_battle = character.get("in_battle", False)
    
    return health > 0 and not in_battle

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    xp = enemy.get("xp_reward", 0)
    gold = enemy.get("gold_reward", 0)
    
    return {"xp": xp, "gold": gold}

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print("\n=== COMBAT STATUS ===")
    print(f"{character.get('name','Character')}: HP {character.get('health',0)}/{character.get('max_health',0)} | "
          f"STR {character.get('strength',0)} | MAG {character.get('magic',0)} | GOLD {character.get('gold',0)}")
    
    print(f"{enemy.get('name', enemy.get('type','Enemy'))}: HP {enemy.get('health',0)}/{enemy.get('max_health',0)} | "
          f"STR {enemy.get('strength',0)} | MAG {enemy.get('magic',0)}")
    print("====================\n")

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")
# Example: Create an enemy manually (replace with create_enemy if implemented)
    goblin = {
        "name": "Goblin Grunt",
        "type": "goblin",
        "health": 50,
        "max_health": 50,
        "strength": 8,
        "magic": 0,
        "xp_reward": 20,
        "gold_reward": 15
    }
    print(f"Created enemy: {goblin['name']} (HP: {goblin['health']})\n")
    
    # Example test character
    test_char = {
        "name": "Hero",
        "class": "Warrior",
        "health": 120,
        "max_health": 120,
        "strength": 15,
        "magic": 5,
        "experience": 0,
        "gold": 100
    }
    
    # Initialize battle
    battle = SimpleBattle(test_char, goblin)
    
    # Start battle and handle results
    try:
        result = battle.start_battle()
        print(f"\n=== BATTLE RESULT ===")
        print(f"Winner: {result['winner']}")
        print(f"XP Gained: {result['xp_gained']}")
        print(f"Gold Gained: {result['gold_gained']}")
        print(f"{test_char['name']} HP Remaining: {test_char['health']}")
    except CharacterDeadError:
        print("Character is dead and cannot fight!")
