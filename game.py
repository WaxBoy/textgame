import random

# =========================================
#             Global Variables
# =========================================

player = None
inventory = {}
game_over = False
unlocked_locations = ["Haunted Forest", "Enchanted Castle", "Bandit's Lair"]  # Starting locations
persistent_states = {}  # To remember states like trapped enemies
current_prompt = ""  # To store the last prompt for '?'
enemy_death_count = {}


# =========================================
#             Character Classes
# =========================================

class Character:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class
        self.level = 1
        self.experience = 0
        self.health = 100
        self.max_health = 100
        self.stats = self.set_stats()
        self.abilities = self.set_abilities()
        self.unlocked_abilities = []  # For new abilities unlocked later
        self.stealthed = False  # For Rogue class

    def set_stats(self):
        # Initialize stats based on character class
        if self.char_class == "Warrior":
            return {"Strength": 15, "Agility": 10, "Intelligence": 5}
        elif self.char_class == "Mage":
            return {"Strength": 5, "Agility": 10, "Intelligence": 15}
        elif self.char_class == "Rogue":
            return {"Strength": 10, "Agility": 15, "Intelligence": 5}
        elif self.char_class == "Paladin":
            return {"Strength": 12, "Agility": 8, "Intelligence": 10}
        elif self.char_class == "Ranger":
            return {"Strength": 10, "Agility": 15, "Intelligence": 5}
        elif self.char_class == "Necromancer":
            return {"Strength": 5, "Agility": 8, "Intelligence": 17}
        elif self.char_class == "Druid":
            return {"Strength": 8, "Agility": 10, "Intelligence": 12}
        elif self.char_class == "Monk":
            return {"Strength": 13, "Agility": 13, "Intelligence": 4}
        elif self.char_class == ", the Creator":
            return {"Strength": float('inf'), "Agility": float('inf'), "Intelligence": float('inf')}
        else:
            return {"Strength": 10, "Agility": 10, "Intelligence": 10}

    def set_abilities(self):
        # Assign initial abilities and potential unlockable abilities
        abilities_dict = {
            "Warrior": {
                "initial": ["Power Strike", "Shield Block"],
                "unlockable": ["Battle Cry", "Whirlwind", "Earth Shatter"],
                "descriptions": {
                    "Power Strike": "A strong attack dealing extra damage.",
                    "Shield Block": "Block incoming attacks, reducing damage.",
                    "Battle Cry": "Boost morale, increasing Strength.",
                    "Whirlwind": "Attack all enemies around you.",
                    "Earth Shatter": "Stun enemies with a ground slam."
                }
            },
            "Mage": {
                "initial": ["Fireball", "Ice Spike"],
                "unlockable": ["Teleport", "Lightning Bolt", "Meteor Shower"],
                "descriptions": {
                    "Fireball": "Cast a fireball to burn enemies.",
                    "Ice Spike": "Launch an ice spike to slow enemies.",
                    "Teleport": "Instantly move to a nearby location.",
                    "Lightning Bolt": "Strike an enemy with lightning.",
                    "Meteor Shower": "Summon meteors to damage all enemies."
                }
            },
            "Rogue": {
                "initial": ["Backstab", "Stealth"],
                "unlockable": ["Poison Blade", "Shadow Step", "Fan of Knives"],
                "descriptions": {
                    "Backstab": "Attack an enemy from behind for extra damage.",
                    "Stealth": "Become invisible to enemies temporarily.",
                    "Poison Blade": "Coat your weapon with poison.",
                    "Shadow Step": "Teleport behind an enemy.",
                    "Fan of Knives": "Throw knives at multiple enemies."
                }
            },
            "Paladin": {
                "initial": ["Holy Smite", "Heal"],
                "unlockable": ["Divine Shield", "Blessing", "Judgment"],
                "descriptions": {
                    "Holy Smite": "Deal holy damage to an enemy.",
                    "Heal": "Restore health to yourself or an ally.",
                    "Divine Shield": "Become immune to damage temporarily.",
                    "Blessing": "Increase ally's stats.",
                    "Judgment": "Judge an enemy, reducing their stats."
                }
            },
            "Ranger": {
                "initial": ["Arrow Shot", "Trap"],
                "unlockable": ["Multi-Shot", "Eagle Eye", "Rain of Arrows"],
                "descriptions": {
                    "Arrow Shot": "Shoot an arrow at an enemy.",
                    "Trap": "Set a trap to immobilize enemies.",
                    "Multi-Shot": "Shoot multiple arrows at once.",
                    "Eagle Eye": "Increase accuracy and critical chance.",
                    "Rain of Arrows": "Rain arrows down on all enemies."
                }
            },
            "Necromancer": {
                "initial": ["Life Drain", "Raise Undead"],
                "unlockable": ["Soul Harvest", "Death Coil", "Army of the Dead"],
                "descriptions": {
                    "Life Drain": "Drain life from an enemy.",
                    "Raise Undead": "Summon undead to fight for you.",
                    "Soul Harvest": "Steal souls to increase power.",
                    "Death Coil": "Throw a coil of death energy.",
                    "Army of the Dead": "Summon a horde of undead."
                }
            },
            "Druid": {
                "initial": ["Nature's Grasp", "Wild Shape"],
                "unlockable": ["Summon Animal", "Regrowth", "Hurricane"],
                "descriptions": {
                    "Nature's Grasp": "Entangle enemies with vines.",
                    "Wild Shape": "Transform into a beast.",
                    "Summon Animal": "Summon an animal ally.",
                    "Regrowth": "Heal over time.",
                    "Hurricane": "Summon a storm to damage enemies."
                }
            },
            "Monk": {
                "initial": ["Flurry of Blows", "Meditate"],
                "unlockable": ["Chi Blast", "Inner Peace", "Fists of Fury"],
                "descriptions": {
                    "Flurry of Blows": "Deliver rapid strikes.",
                    "Meditate": "Restore health and mana.",
                    "Chi Blast": "Project energy to damage enemies.",
                    "Inner Peace": "Boost defenses temporarily.",
                    "Fists of Fury": "Unleash a powerful combo attack."
                }
            },
            ", the Creator": {
                "initial": [],
                "unlockable": [],
                "descriptions": {}
            }
        }

        abilities_info = abilities_dict.get(self.char_class, {"initial": [], "unlockable": [], "descriptions": {}})
        self.ability_descriptions = abilities_info["descriptions"]
        self.unlocked_abilities = abilities_info["unlockable"]
        return abilities_info["initial"]

    def level_up(self):
        self.level += 1
        print(f"🎉 {self.name} leveled up to level {self.level}!")
        # Increase stats
        self.stats["Strength"] += 2
        self.stats["Agility"] += 2
        self.stats["Intelligence"] += 2
        self.max_health += 20
        self.health = self.max_health
        # Unlock abilities if any
        if self.unlocked_abilities:
            new_ability = self.unlocked_abilities.pop(0)
            self.abilities.append(new_ability)
            print(f"✨ {self.name} unlocked a new ability: {new_ability}!")
            # Provide description of the new ability
            print(f"Ability Description: {self.ability_descriptions.get(new_ability, 'No description available.')}")
        # Unlock new locations at level up
        if self.level == 2 and "Mystic River" not in unlocked_locations:
            unlocked_locations.append("Mystic River")
            print("A new location has been unlocked: Mystic River! 🌊")
        if self.level == 3 and "Forgotten Caves" not in unlocked_locations:
            unlocked_locations.append("Forgotten Caves")
            print("A new location has been unlocked: Forgotten Caves! 🕳️")
        if self.level == 4 and "Ancient Ruins" not in unlocked_locations:
            unlocked_locations.append("Ancient Ruins")
            print("A new location has been unlocked: Ancient Ruins! 🏛️")
        if self.level == 5 and "Dragon's Peak" not in unlocked_locations:
            unlocked_locations.append("Dragon's Peak")
            print("A new location has been unlocked: Dragon's Peak! 🐉")
        if self.level == 6 and "Matrix World" not in unlocked_locations:
            unlocked_locations.append("Matrix World")
            print("A new location has been unlocked: Matrix World! 🕶️")

    def attack(self, target):
        # Calculate attack power based on Strength and product of 2d10 rolls
        roll = random.randint(1, 10) * random.randint(1, 10)
        damage = ((self.stats["Strength"] + self.stats["Agility"] / 2) * roll) // 10  # Adjusted for balance
        target.health -= damage
        print(f"{self.name} attacks {target.name} for {damage} damage. ⚔️")

    def use_ability(self, ability, target):
        # Use an ability during combat
        roll = random.randint(1, 10) * random.randint(1, 10)
        if ability == "Power Strike":
            damage = ((self.stats["Strength"] + 5) * roll) // 10
            target.health -= damage
            print(f"{self.name} uses {ability} on {target.name} for {damage} damage. 💥")
        elif ability == "Shield Block":
            self.stats["Strength"] += 2
            print(f"{self.name} uses {ability} and increases Strength by 2! 🛡️")
        elif ability == "Fireball":
            damage = ((self.stats["Intelligence"] + 5) * roll) // 10
            target.health -= damage
            print(f"{self.name} casts {ability} on {target.name} for {damage} damage. 🔥")
        elif ability == "Ice Spike":
            damage = ((self.stats["Intelligence"] + 3) * roll) // 10
            target.health -= damage
            persistent_states[target.name] = {'slowed': True, 'turns': 2}
            print(f"{self.name} casts {ability}, dealing {damage} damage and slowing {target.name}. ❄️")
        elif ability == "Backstab":
            damage = ((self.stats["Agility"] + 5) * roll) // 10
            if target.unaware:
                damage *= 2
                print(f"Critical Hit! {self.name} backstabs {target.name} for {damage} damage. 🗡️")
            else:
                print(f"{self.name} performs {ability} on {target.name} for {damage} damage. 🗡️")
            target.health -= damage
        elif ability == "Stealth":
            self.stealthed = True
            print(f"{self.name} enters stealth mode. 🕵️")
        elif ability == "Holy Smite":
            damage = ((self.stats["Strength"] + self.stats["Intelligence"]) * roll) // 10
            target.health -= damage
            print(f"{self.name} uses {ability} on {target.name} for {damage} damage. ✨")
        elif ability == "Heal":
            heal_amount = (self.stats["Intelligence"] * roll) // 10
            actual_heal = min(heal_amount, self.max_health - self.health)
            self.health += actual_heal
            print(f"{self.name} heals for {actual_heal} health. 💖")
        elif ability == "Arrow Shot":
            damage = ((self.stats["Agility"] + 5) * roll) // 10
            target.health -= damage
            print(f"{self.name} shoots an arrow at {target.name} for {damage} damage. 🎯")
        elif ability == "Trap":
            print(f"{self.name} sets a trap. 🪤")
            persistent_states[target.name] = {'trapped': True, 'turns': 3}
        elif ability == "Raise Undead":
            damage = ((self.stats["Intelligence"] + 5) * roll) // 10
            target.health -= damage
            heal_amount = damage // 2
            actual_heal = min(heal_amount, self.max_health - self.health)
            self.health += actual_heal
            print(f"{self.name} uses {ability} on {target.name}, dealing {damage} damage and healing for {actual_heal}. 💀")
        elif ability == "Life Drain":
            damage = ((self.stats["Intelligence"] + 3) * roll) // 10
            target.health -= damage
            heal_amount = damage // 2
            actual_heal = min(heal_amount, self.max_health - self.health)
            self.health += actual_heal
            print(f"{self.name} drains life from {target.name} for {damage} damage and heals for {actual_heal}. 🩸")
        elif ability == "Nature's Grasp":
            damage = ((self.stats["Intelligence"] + 5) * roll) // 10
            target.health -= damage
            persistent_states[target.name] = {'rooted': True, 'turns': 2}
            print(f"Vines entangle {target.name}, dealing {damage} damage and rooting them. 🌿")
        elif ability == "Wild Shape":
            self.stats["Strength"] += 5
            self.stats["Agility"] += 5
            print(f"{self.name} transforms into a beast, increasing Strength and Agility! 🐾")
        elif ability == "Flurry of Blows":
            damage = ((self.stats["Strength"] + self.stats["Agility"]) * roll) // 10
            target.health -= damage
            print(f"{self.name} unleashes rapid strikes on {target.name} for {damage} damage. 👊")
        elif ability == "Meditate":
            actual_heal = min(30, self.max_health - self.health)
            self.health += actual_heal
            print(f"{self.name} meditates and restores {actual_heal} health. 🧘")
        elif ability == "Plasma Blast":
            damage = ((self.stats["Intelligence"] + 10) * roll) // 5
            target.health -= damage
            print(f"{self.name} fires a {ability} at {target.name} for {damage} damage. 💥")
        else:
            print("You don't have that ability.")

    def show_abilities(self):
        print(f"\n{self.name}'s Abilities:")
        for ability in self.abilities:
            description = self.ability_descriptions.get(ability, "No description available.")
            print(f"- {ability}: {description}")
        print("")

# =========================================
#             Enemy Classes
# =========================================

class Enemy:
    def __init__(self, name, health, strength, abilities, experience_given=50, agility=10, intelligence=5):
        self.name = name
        self.health = health
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.abilities = abilities
        self.experience_given = experience_given
        self.unaware = True  # For surprise attacks

    def attack(self, target):
        # Enemy attacks player
        state = persistent_states.get(self.name, {})
        if state.get('trapped'):
            print(f"{self.name} is trapped and cannot move! 😵")
            state['turns'] -= 1
            if state['turns'] <= 0:
                del persistent_states[self.name]
            else:
                persistent_states[self.name] = state
        elif state.get('rooted'):
            print(f"{self.name} is rooted and cannot move! 🌱")
            state['turns'] -= 1
            if state['turns'] <= 0:
                del persistent_states[self.name]
            else:
                persistent_states[self.name] = state
        elif state.get('slowed'):
            print(f"{self.name} is slowed and attacks less effectively. 🐌")
            roll = random.randint(1, 5) * random.randint(1, 5)
            damage = ((self.strength + random.randint(1, 5)) * roll) // 10
            target.health -= damage
            print(f"{self.name} sluggishly attacks {target.name} for {damage} damage. ⚔️")
            state['turns'] -= 1
            if state['turns'] <= 0:
                del persistent_states[self.name]
            else:
                persistent_states[self.name] = state
        elif getattr(target, 'stealthed', False):
            print(f"{self.name} can't see {target.name} and misses the attack! 👻")
            target.stealthed = False  # Stealth breaks after enemy's turn
        else:
            roll = random.randint(1, 10) * random.randint(1, 10)
            damage = ((self.strength + random.randint(1, 5)) * roll) // 10  # Adjusted for balance
            target.health -= damage
            print(f"{self.name} attacks {target.name} for {damage} damage. ⚔️")

# =========================================
#             Game Functions
# =========================================

def game_intro():
    print("Welcome to the Text-Based RPG Adventure Game!")
    print("Available commands at any time:")
    print("  'inventory' or 'i' - View your inventory")
    print("  'stats' or 's' - View your character's stats")
    print("  'use item' or 'u' - Use an item from your inventory")
    print("  'discard item' or 'd' - Discard an item from your inventory")
    print("  'abilities' or 'a' - View your abilities")
    print("  '?' - Repeat the last prompt or go back")
    print("  'help' or 'h' - Display this help message")
    print("Make choices by typing the number or command corresponding to your action.")
    print("Good luck on your journey!\n")

def create_character():
    global player  # Declare global variable at the beginning
    # Allow player to create a character
    name = input("Enter your character's name: ")

    if name == "Tyler":
        char_class = ", the Creator"
        player = Character(name, char_class)
        player.stats = {"Strength": float('inf'), "Agility": float('inf'), "Intelligence": float('inf')}
        player.abilities = []
        print(f"Welcome, {player.name}{player.char_class}!")
        print("You have unlocked infinite power! 💪")
        return

    print("Choose a class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    print("4. Paladin")
    print("5. Ranger")
    print("6. Necromancer")
    print("7. Druid")
    print("8. Monk")
    class_choice = input("Enter the number of your choice: ")

    class_dict = {
        "1": "Warrior",
        "2": "Mage",
        "3": "Rogue",
        "4": "Paladin",
        "5": "Ranger",
        "6": "Necromancer",
        "7": "Druid",
        "8": "Monk"
    }

    char_class = class_dict.get(class_choice, "Warrior")

    player = Character(name, char_class)
    print(f"Welcome, {player.name} the {player.char_class}!")

    # Include class description
    class_descriptions = {
        "Warrior": "A strong melee fighter with high Strength.",
        "Mage": "A master of elemental magic with high Intelligence.",
        "Rogue": "A stealthy assassin with high Agility.",
        "Paladin": "A holy knight with balanced Strength and Intelligence.",
        "Ranger": "An agile archer skilled in ranged combat.",
        "Necromancer": "A dark magician who manipulates life and death.",
        "Druid": "A guardian of nature with shapeshifting abilities.",
        "Monk": "A martial artist with balanced Strength and Agility."
    }

    print(class_descriptions.get(char_class, "A mysterious adventurer."))

def show_inventory():
    # Display player's inventory with quantities
    if inventory:
        print("Your inventory contains:")
        for item, quantity in inventory.items():
            print(f"- {item} x{quantity}")
    else:
        print("Your inventory is empty.")

def show_stats():
    # Display player's stats
    print(f"\n{player.name} the {player.char_class}")
    print(f"Level: {player.level}")
    print(f"Health: {player.health}/{player.max_health}")
    print("Stats:")
    for stat, value in player.stats.items():
        print(f"  {stat}: {value}")
    print("")

def use_item():
    # Use an item from inventory
    if not inventory:
        print("You have no items to use.")
        return False  # Indicate that no action was taken

    while True:
        print("Choose an item to use:")
        items = list(inventory.keys())
        for idx, item in enumerate(items):
            print(f"{idx + 1}. {item} x{inventory[item]}")
        choice = input("Enter the number of the item (or 'back' to cancel): ").lower()
        if choice in ['?', 'back', 'b']:
            return False  # Indicate that no action was taken

        try:
            item = items[int(choice) - 1]
            if item == "Health Potion":
                heal_amount = random.randint(40, 60)
                actual_heal = min(heal_amount, player.max_health - player.health)
                player.health += actual_heal
                inventory[item] -= 1
                if inventory[item] == 0:
                    del inventory[item]
                print(f"{player.name} used a Health Potion and restored {actual_heal} health. 🍶")
                return True  # Action was taken
            elif item == "Mana Potion":
                print("Mana Potions restore mana when you have mana-consuming abilities.")
                print("Use it when you acquire such abilities.")
                continue  # Re-prompt the player
            elif item == "Healing Herb":
                heal_amount = random.randint(15, 25)
                actual_heal = min(heal_amount, player.max_health - player.health)
                player.health += actual_heal
                inventory[item] -= 1
                if inventory[item] == 0:
                    del inventory[item]
                print(f"{player.name} used a Healing Herb and restored {actual_heal} health. 🌿")
                return True  # Action was taken
            elif item == "Strength Elixir":
                player.stats["Strength"] += 2
                inventory[item] -= 1
                if inventory[item] == 0:
                    del inventory[item]
                print(f"{player.name} drank a Strength Elixir. Strength increased by 2! 💪")
                return True  # Action was taken
            elif item == "Agility Potion":
                player.stats["Agility"] += 2
                inventory[item] -= 1
                if inventory[item] == 0:
                    del inventory[item]
                print(f"{player.name} drank an Agility Potion. Agility increased by 2! 🏃")
                return True  # Action was taken
            elif item == "Intelligence Scroll":
                player.stats["Intelligence"] += 2
                inventory[item] -= 1
                if inventory[item] == 0:
                    del inventory[item]
                print(f"{player.name} read an Intelligence Scroll. Intelligence increased by 2! 🧠")
                return True  # Action was taken
            elif item == "Troll's Club":
                print(f"{player.name} equips the Troll's Club, increasing Strength by 5! 🪓")
                player.stats["Strength"] += 5
                inventory[item] -= 1
                if inventory[item] == 0:
                    del inventory[item]
                return True  # Action was taken
            elif item == "Guardian's Shield":
                print(f"{player.name} equips the Guardian's Shield, increasing Defense! 🛡️")
                # Implement defense mechanism if desired
                inventory[item] -= 1
                if inventory[item] == 0:
                    del inventory[item]
                return True  # Action was taken
            elif item == "Plasma Rifle":
                print(f"{player.name} equips the Plasma Rifle, unlocking powerful attacks! 🔫")
                if "Plasma Blast" not in player.abilities:
                    player.abilities.append("Plasma Blast")
                    player.ability_descriptions["Plasma Blast"] = "A devastating energy attack."
                inventory[item] -= 1
                if inventory[item] == 0:
                    del inventory[item]
                return True  # Action was taken
            else:
                if item == "Enchanted Flower":
                    print("The Enchanted Flower can be given to the Enchantress in the Enchanted Castle.")
                elif item == "Ancient Relic":
                    print("The Ancient Relic can be offered to the dragon for a special outcome.")
                elif item == "Bandit's Dagger":
                    print("The Bandit's Dagger can be used during combat for extra damage.")
                elif item == "Magic Amulet":
                    print("The Magic Amulet enhances magical abilities when used in combat.")
                elif item == "Spirit Essence":
                    print("Spirit Essence can be used in specific rituals at the Ancient Ruins.")
                else:
                    print(f"The {item} can't be used right now.")
                continue  # Re-prompt the player
        except (IndexError, ValueError):
            print("That's not a valid choice.")
            continue  # Re-prompt the player

def discard_item():
    # Discard an item from inventory
    if not inventory:
        print("You have no items to discard.")
        return

    while True:
        print("Choose an item to discard:")
        items = list(inventory.keys())
        for idx, item in enumerate(items):
            print(f"{idx + 1}. {item} x{inventory[item]}")
        choice = input("Enter the number of the item (or 'back' to cancel): ").lower()
        if choice in ['?', 'back', 'b']:
            return

        try:
            item = items[int(choice) - 1]
            inventory[item] -= 1
            if inventory[item] == 0:
                del inventory[item]
            print(f"You have discarded {item}.")
            return
        except (IndexError, ValueError):
            print("That's not a valid choice.")
            continue  # Re-prompt the player

def get_player_input(prompt, valid_choices):
    global current_prompt
    current_prompt = prompt
    while True:
        user_input = input(prompt)
        user_input = user_input.strip().lower()
        if user_input in ['inventory', 'i']:
            show_inventory()
        elif user_input in ['stats', 's']:
            show_stats()
        elif user_input in ['abilities', 'a']:
            player.show_abilities()
        elif user_input in ['use item', 'u']:
            use_item()
        elif user_input in ['discard item', 'd']:
            discard_item()
        elif user_input in ['?', 'back', 'b']:
            return '?'
        elif user_input in ['help', 'h']:
            print("Available commands: 'inventory'/'i', 'stats'/'s', 'abilities'/'a', 'use item'/'u', 'discard item'/'d', '?'/'back'/'b', 'help'/'h'")
        elif user_input in valid_choices:
            return user_input
        else:
            print("That's not a valid choice. Type 'help' for available commands.")

def combat(enemy):
    global game_over  # Declare global variable
    # Determine who attacks first based on Agility
    if player.stats["Agility"] >= enemy.agility:
        turn_order = [player, enemy]
    else:
        turn_order = [enemy, player]
    print(f"A wild {enemy.name} appears! 😈")
    enemy.unaware = False  # Enemy is now aware of the player
    while enemy.health > 0 and player.health > 0:
        for entity in turn_order:
            if enemy.health <= 0 or player.health <= 0:
                break
            if entity == player:
                print(f"\n{player.name}'s Health: {player.health}")
                print(f"{enemy.name} Health: {enemy.health}")
                print("Choose an action:")
                print("1. Attack")
                choices = ['1']

                if player.abilities:
                    print("2. Use Ability")
                    choices.append('2')

                print("3. Use Item")
                choices.append('3')

                print("4. Flee")
                choices.append('4')

                action = get_player_input("Enter the number of your action: ", choices)
                if action == '?':
                    continue
                print()  # Add a blank line between choice and output

                if action == "1":
                    player.attack(enemy)
                    if enemy.health <= 0:
                        print(f"{enemy.name} has been defeated!")
                        break  # Enemy is defeated, end combat
                elif action == "2":
                    if not player.abilities:
                        print("You have no abilities to use.")
                        continue  # Re-prompt the player
                    print("Choose an ability:")
                    for idx, ability in enumerate(player.abilities):
                        print(f"{idx + 1}. {ability}")
                    ability_choices = [str(i+1) for i in range(len(player.abilities))]
                    ability_choice = get_player_input("Enter the number of the ability (or 'back' to cancel): ", ability_choices)
                    if ability_choice == '?':
                        continue
                    print()
                    try:
                        ability = player.abilities[int(ability_choice) - 1]
                        player.use_ability(ability, enemy)
                        if enemy.health <= 0:
                            print(f"{enemy.name} has been defeated!")
                            break  # Enemy is defeated, end combat
                    except (IndexError, ValueError):
                        print("Invalid ability choice.")
                        continue
                elif action == "3":
                    if use_item():
                        pass  # Item used successfully; proceed to enemy's turn
                    else:
                        continue  # No action taken; re-prompt the player
                elif action == "4":
                    flee_chance = random.randint(1, 36) + player.stats["Agility"] // 5
                    if flee_chance < 35:  # Ensure it's never 100% chance
                        print(f"{player.name} failed to flee! The battle continues.")
                    else:
                        print(f"{player.name} successfully fled the battle! 🏃")
                        return
                else:
                    print("That's not a valid action.")
                    continue
            else:
                if enemy.health > 0:
                    enemy.attack(player)
                    if player.health <= 0:
                        break  # Player is defeated
    if player.health <= 0:
        print(f"{player.name} has been defeated! 💀")
        print(f"{enemy.name}'s remaining health: {enemy.health}, Str: {enemy.strength}, Agi: {enemy.agility}, Int: {enemy.intelligence}")
        game_over = True
    else:
        print(f"{player.name} defeated {enemy.name}! 🎉")
        # Update enemy death count
        enemy_death_count[enemy.name] = enemy_death_count.get(enemy.name, 0) + 1
        # Adjust experience given based on death count
        death_multiplier = 0.85 ** (enemy_death_count[enemy.name] - 1)
        adjusted_experience = int(-(-enemy.experience_given * death_multiplier) // 1)  # Round up
        player.experience += adjusted_experience
        print(f"{player.name} gains {adjusted_experience} experience points! 🏅")
        # Check for level up
        experience_needed = player.level * 100
        if player.experience >= experience_needed:
            player.experience -= experience_needed
            player.level_up()
        # Random chance to get an item
        loot_chance = random.randint(1, 10)
        if loot_chance > 5:
            item_found = random.choice(["Health Potion", "Mana Potion", "Gold Coin", "Strength Elixir", "Agility Potion", "Intelligence Scroll"])
            inventory[item_found] = inventory.get(item_found, 0) + 1
            print(f"{player.name} found a {item_found}! 🎁")



def random_encounter():
    global game_over
    print("\nYou encounter a wandering traveler. 🚶")
    print("Options:")
    print("1. Talk to the traveler")
    print("2. Attack the traveler")
    print("3. Ignore and move on")
    choices = ['1', '2', '3']
    choice = get_player_input("What do you want to do? ", choices)
    if choice == '?':
        return random_encounter()
    print()

    if choice == '1':
        event = random.choice(["trade", "quest", "information", "hostile"])
        if event == "trade":
            print("The traveler offers to trade items with you. 💱")
            if inventory:
                print("Your items:")
                items = list(inventory.keys())
                for idx, item in enumerate(items):
                    print(f"{idx + 1}. {item} x{inventory[item]}")
                trade_choice = input("Choose an item to trade or type 'cancel' to decline: ")
                if trade_choice.lower() != 'cancel':
                    try:
                        item = items[int(trade_choice) - 1]
                        inventory[item] -= 1
                        if inventory[item] == 0:
                            del inventory[item]
                        new_item = random.choice(["Health Potion", "Agility Potion", "Strength Elixir"])
                        inventory[new_item] = inventory.get(new_item, 0) + 1
                        print(f"You traded {item} for {new_item}! 🤝")
                    except (IndexError, ValueError):
                        print("Invalid choice.")
                else:
                    print("You decided not to trade.")
            else:
                print("You have nothing to trade.")
        elif event == "quest":
            print("The traveler gives you a quest to find a lost artifact. 🗺️")
            # Simple quest: find an item in the next location
            inventory["Quest Item"] = inventory.get("Quest Item", 0) + 1
            print("You received a Quest Item!")
        elif event == "information":
            print("The traveler shares valuable information with you. 💡")
            stat_increase = random.choice(["Strength", "Agility", "Intelligence"])
            player.stats[stat_increase] += 1
            print(f"{player.name}'s {stat_increase} increased by 1!")
        elif event == "hostile":
            print("The traveler turns out to be a bandit in disguise! 😈")
            enemy = Enemy("Bandit", 100, 15, ["Slash"], experience_given=80, agility=12, intelligence=8)
            enemy.unaware = False  # Enemy is now aware
            combat(enemy)
            if game_over:
                return
            inventory["Gold Coin"] = inventory.get("Gold Coin", 0) + 1
            print(f"{player.name} obtained a Gold Coin! 💰")
        else:
            print("The traveler has nothing to offer.")
    elif choice == '2':
        # If the traveler was secretly hostile, attacking them now gives an advantage
        event = random.choice(["hostile", "innocent"])
        if event == "hostile":
            print(f"{player.name} catches the traveler off-guard! 🗡️")
            enemy = Enemy("Bandit", 100, 15, ["Slash"], experience_given=80, agility=12, intelligence=8)
            enemy.unaware = True
            combat(enemy)
            if game_over:
                return
            inventory["Gold Coin"] = inventory.get("Gold Coin", 0) + 1
            print(f"{player.name} obtained a Gold Coin! 💰")
        else:
            print(f"{player.name} attacks an innocent traveler! 😱")
            enemy = Enemy("Innocent Traveler", 80, 10, ["Defend"], experience_given=50, agility=8, intelligence=5)
            enemy.unaware = False
            combat(enemy)
            if game_over:
                return
            print(f"{player.name} feels a pang of guilt.")
    elif choice == '3':
        print("You continue on your journey. 🛤️")
    else:
        print("That's not a valid choice.")

def choose_location():
    print("\nWhere would you like to go?")
    for idx, location in enumerate(unlocked_locations):
        print(f"{idx + 1}. {location}")
    choices = [str(i+1) for i in range(len(unlocked_locations))]
    choice = get_player_input("Enter the number of your destination: ", choices)
    if choice == '?':
        return choose_location()

    location_functions = {
        "Haunted Forest": haunted_forest,
        "Enchanted Castle": enchanted_castle,
        "Bandit's Lair": bandits_lair,
        "Mystic River": mystic_river,
        "Forgotten Caves": forgotten_caves,
        "Ancient Ruins": ancient_ruins,
        "Dragon's Peak": dragons_peak,
        "Matrix World": matrix_world
    }

    if choice in choices:
        location_name = unlocked_locations[int(choice) - 1]
        location_function = location_functions.get(location_name)
        if location_function:
            location_function()
        else:
            print("That's not a valid location.")
    else:
        print("That's not a valid choice.")

# =========================================
#        Location Functions (Updated)
# =========================================

def haunted_forest():
    global game_over
    while True:
        # Random encounter chance
        if random.randint(1, 100) <= 30:
            random_encounter()
            if game_over:
                return
        # Scenario: The Haunted Forest
        print("\n🌲 You are in the Haunted Forest.")
        print("An eerie silence surrounds you.")
        print("Options:")
        print("1. Explore deeper")
        print("2. Collect herbs")
        print("3. Set up camp")
        print("4. Search for hidden paths")
        print("5. Confront the Forest Spirit")
        print("6. Leave the forest")
        choices = ['1', '2', '3', '4', '5', '6']
        choice = get_player_input("What do you want to do? ", choices)
        if choice == '?':
            continue
        print()  # Add a blank line between choice and output

        if choice == "1":
            event = random.choice(["enemy", "treasure", "stat_increase", "nothing"])
            if event == "enemy":
                enemy = Enemy("Ghost", 80, 10, ["Haunt"], experience_given=70, agility=12, intelligence=15)
                combat(enemy)
                if game_over:
                    return
                inventory["Magic Amulet"] = inventory.get("Magic Amulet", 0) + 1
                print(f"{player.name} found a Magic Amulet! ✨")
            elif event == "treasure":
                print("You found an old chest! 📦")
                inventory["Health Potion"] = inventory.get("Health Potion", 0) + 1
                print(f"{player.name} obtained a Health Potion! 🍶")
            elif event == "stat_increase":
                player.stats["Agility"] += 1
                print(f"{player.name}'s Agility increased by 1! 🏃")
            else:
                print("You wander but find nothing of interest.")
        elif choice == "2":
            event = random.choice(["found_herbs", "poison_ivy", "nothing"])
            if event == "found_herbs":
                print("You collect rare herbs. 🌿")
                inventory["Healing Herb"] = inventory.get("Healing Herb", 0) + 1
                print(f"{player.name} obtained a Healing Herb!")
            elif event == "poison_ivy":
                print("You accidentally touch poison ivy and get a rash! 🌿")
                player.health -= 10
                print(f"{player.name} loses 10 health.")
                if player.health <= 0:
                    print(f"{player.name} didn't survive.")
                    game_over = True
                    return
            else:
                print("You search but find nothing.")
        elif choice == "3":
            event = random.choice(["heal", "ambush", "dream", "nothing"])
            if event == "heal":
                print("You set up camp and rest. 🏕️")
                heal_amount = 20 + player.stats["Intelligence"] // 2
                actual_heal = min(heal_amount, player.max_health - player.health)
                player.health += actual_heal
                print(f"{player.name}'s health is restored by {actual_heal} points.")
            elif event == "ambush":
                print("You are ambushed by forest bandits during your rest! 😱")
                enemy = Enemy("Forest Bandit", 90, 12, ["Quick Shot"], experience_given=80, agility=14, intelligence=10)
                combat(enemy)
                if game_over:
                    return
            elif event == "dream":
                event_outcome = random.choice(["good_dream", "nightmare"])
                if event_outcome == "good_dream":
                    print("You have a prophetic dream, gaining insight. 💤")
                    player.stats["Intelligence"] += 1
                    print(f"{player.name}'s Intelligence increased by 1!")
                else:
                    print("You have a nightmare and wake up in a cold sweat. 😰")
                    player.health -= 10
                    print(f"{player.name} loses 10 health.")
                    if player.health <= 0:
                        print(f"{player.name} didn't survive the shock.")
                        game_over = True
                        return
            else:
                print("Your rest is uneventful.")
        elif choice == "4":
            event = random.choice(["find path", "get lost", "hidden treasure", "nothing"])
            if event == "find path":
                print("You discover a hidden path leading out of the forest! 🗺️")
                inventory["Forest Map"] = inventory.get("Forest Map", 0) + 1
                print(f"{player.name} obtained a Forest Map!")
            elif event == "get lost":
                print("You get lost and wander for hours. 😓")
                player.health -= 10
                print(f"{player.name} loses 10 health due to exhaustion.")
                if player.health <= 0:
                    print(f"{player.name} has succumbed to exhaustion.")
                    game_over = True
            elif event == "hidden treasure":
                print("You find a hidden stash left by previous travelers.")
                inventory["Agility Potion"] = inventory.get("Agility Potion", 0) + 1
                print(f"{player.name} obtained an Agility Potion!")
            else:
                print("You search but find nothing.")
        elif choice == "5":
            print("You decide to confront the Forest Spirit.")
            enemy = Enemy("Forest Spirit", 150, 20, ["Nature's Wrath"], experience_given=120, agility=20, intelligence=25)
            combat(enemy)
            if game_over:
                return
            inventory["Spirit Essence"] = inventory.get("Spirit Essence", 0) + 1
            print(f"{player.name} obtained Spirit Essence!")
        elif choice == "6":
            print("You decide to leave the Haunted Forest.")
            return  # Exit the function
        else:
            print("That's not a valid choice.")

def enchanted_castle():
    global game_over
    while True:
        # Random encounter chance
        if random.randint(1, 100) <= 30:
            random_encounter()
            if game_over:
                return
        # Scenario: The Enchanted Castle
        print("\n🏰 You are at the Enchanted Castle.")
        print("Options:")
        print("1. Knock on the door")
        print("2. Sneak in through a window")
        print("3. Search the garden")
        print("4. Look for secret entrances")
        print("5. Speak with the Enchantress")
        print("6. Leave the castle")
        choices = ['1', '2', '3', '4', '5', '6']
        choice = get_player_input("What do you want to do? ", choices)
        if choice == '?':
            continue
        print()

        if choice == "1":
            event = random.choice(["wizard", "butler", "no_answer", "trap"])
            if event == "wizard":
                print("A friendly wizard greets you and offers a quest. 🧙")
                quest_choice = get_player_input("Do you accept the quest? (yes/no) ", ['yes', 'no'])
                if quest_choice == '?':
                    continue
                print()
                if quest_choice == "yes":
                    print("The wizard asks you to retrieve a lost scroll from the basement.")
                    enemy = Enemy("Animated Armor", 120, 15, ["Shield Bash"], experience_given=80, agility=10, intelligence=10)
                    combat(enemy)
                    if game_over:
                        return
                    print("You retrieve the scroll and return it to the wizard.")
                    inventory["Wizard's Staff"] = inventory.get("Wizard's Staff", 0) + 1
                    print(f"The wizard gives {player.name} a Wizard's Staff! ✨")
                else:
                    print("You decline the quest and leave the castle.")
            elif event == "butler":
                print("The castle's butler answers and offers you tea. ☕")
                actual_heal = min(10, player.max_health - player.health)
                player.health += actual_heal
                print(f"{player.name}'s health is restored by {actual_heal} points.")
            elif event == "no_answer":
                print("No one answers the door. It's eerily quiet.")
            elif event == "trap":
                print("The door was trapped! You take damage. 💥")
                trap_damage = random.randint(10, 20)
                player.health -= trap_damage
                print(f"{player.name} loses {trap_damage} health.")
                if player.health <= 0:
                    print(f"{player.name} didn't survive the trap.")
                    game_over = True
            else:
                print("Nothing happens.")
        elif choice == "2":
            event = random.choice(["trap", "success", "caught", "treasure"])
            if event == "trap":
                print("You sneak in but trigger a trap! 💥")
                trap_damage = random.randint(20, 40)
                player.health -= trap_damage
                if player.health <= 0:
                    print(f"{player.name} succumbed to the trap's damage.")
                    game_over = True
                    return
                print(f"You manage to escape the trap but are injured for {trap_damage} damage.")
            elif event == "success":
                print("You successfully sneak in and find a treasure room! 💰")
                inventory["Bag of Gems"] = inventory.get("Bag of Gems", 0) + 1
                print(f"{player.name} obtained a Bag of Gems!")
            elif event == "caught":
                print("You are caught by the guards and thrown out! 🚪")
                player.health -= 10
                print(f"{player.name} loses 10 health.")
                if player.health <= 0:
                    print(f"{player.name} didn't survive the rough handling.")
                    game_over = True
            elif event == "treasure":
                print("You find a hidden stash inside the castle.")
                inventory["Intelligence Scroll"] = inventory.get("Intelligence Scroll", 0) + 1
                print(f"{player.name} obtained an Intelligence Scroll!")
            else:
                print("Nothing happens.")
        elif choice == "3":
            event = random.choice(["flower", "stat_increase", "enemy", "nothing"])
            if event == "flower":
                print("You find a mysterious flower in the garden. 🌺")
                inventory["Enchanted Flower"] = inventory.get("Enchanted Flower", 0) + 1
                print(f"{player.name} obtained an Enchanted Flower!")
            elif event == "stat_increase":
                event_outcome = random.choice(["positive", "negative"])
                if event_outcome == "positive":
                    print("You find a serene spot and meditate. 🧘")
                    player.stats["Intelligence"] += 1
                    print(f"{player.name}'s Intelligence increased by 1!")
                else:
                    print("You are bitten by a venomous insect! 🐝")
                    player.health -= 15
                    print(f"{player.name} loses 15 health.")
                    if player.health <= 0:
                        print(f"{player.name} didn't survive the venom.")
                        game_over = True
                        return
            elif event == "enemy":
                print("A garden golem awakens and attacks! 🗿")
                enemy = Enemy("Garden Golem", 130, 18, ["Stomp"], experience_given=90, agility=8, intelligence=5)
                combat(enemy)
                if game_over:
                    return
            else:
                print("You enjoy the beauty of the garden.")
        elif choice == "4":
            event = random.choice(["hidden_door", "nothing", "secret_passage", "trap"])
            if event == "hidden_door":
                print("You find a hidden door leading to the castle's library. 📚")
                inventory["Ancient Tome"] = inventory.get("Ancient Tome", 0) + 1
                print(f"{player.name} obtained an Ancient Tome!")
            elif event == "secret_passage":
                event_outcome = random.choice(["positive", "negative"])
                if event_outcome == "positive":
                    print("You discover a secret passage that boosts your agility! 🏃")
                    player.stats["Agility"] += 1
                    print(f"{player.name}'s Agility increased by 1!")
                else:
                    print("You fall into a hidden pit! 💀")
                    player.health -= 20
                    print(f"{player.name} loses 20 health.")
                    if player.health <= 0:
                        print(f"{player.name} didn't survive the fall.")
                        game_over = True
                        return
            elif event == "trap":
                print("You trigger a trap! 💥")
                trap_damage = random.randint(10, 20)
                player.health -= trap_damage
                print(f"{player.name} loses {trap_damage} health.")
                if player.health <= 0:
                    print(f"{player.name} didn't survive the trap.")
                    game_over = True
            else:
                print("You search but find nothing.")
        elif choice == "5":
            print("You seek out the Enchantress.")
            event = random.choice(["blessing", "curse", "quest"])
            if event == "blessing":
                print("The Enchantress blesses you, increasing your Intelligence! ✨")
                player.stats["Intelligence"] += 2
                print(f"{player.name}'s Intelligence increased by 2!")
            elif event == "curse":
                print("The Enchantress curses you for trespassing! 😈")
                player.stats["Strength"] -= 2
                print(f"{player.name}'s Strength decreased by 2!")
            elif event == "quest":
                print("The Enchantress asks for the Enchanted Flower.")
                if "Enchanted Flower" in inventory:
                    print("You give her the Enchanted Flower.")
                    inventory["Enchanted Flower"] -= 1
                    if inventory["Enchanted Flower"] == 0:
                        del inventory["Enchanted Flower"]
                    print("She rewards you with a Magic Ring!")
                    inventory["Magic Ring"] = inventory.get("Magic Ring", 0) + 1
                else:
                    print("You don't have the Enchanted Flower.")
            else:
                print("She has nothing for you.")
        elif choice == "6":
            print("You decide to leave the Enchanted Castle.")
            return
        else:
            print("That's not a valid choice.")

def bandits_lair():
    global game_over
    while True:
        # Random encounter chance
        if random.randint(1, 100) <= 30:
            random_encounter()
            if game_over:
                return
        # Scenario: The Bandit's Lair
        print("\n🏴‍☠️ You are at the Bandit's Lair.")
        print("Options:")
        print("1. Attack the bandits")
        print("2. Try to negotiate")
        print("3. Spy on them")
        print("4. Set traps around their camp")
        print("5. Challenge the Bandit Leader")
        print("6. Leave the lair")
        choices = ['1', '2', '3', '4', '5', '6']
        choice = get_player_input("What do you want to do? ", choices)
        if choice == '?':
            continue
        print()

        if choice == "1":
            enemy = Enemy("Bandit", 100, 15, ["Quick Slash"], experience_given=80, agility=14, intelligence=10)
            combat(enemy)
            if game_over:
                return
            print("You defeated a bandit and found loot!")
            inventory["Gold Coin"] = inventory.get("Gold Coin", 0) + 1
            print(f"{player.name} obtained a Gold Coin! 💰")
        elif choice == "2":
            event = random.choice(["truce", "betrayal", "trade", "nothing"])
            if event == "truce":
                print("The bandits agree to a truce and offer you a share of their loot. 🤝")
                inventory["Bandit's Dagger"] = inventory.get("Bandit's Dagger", 0) + 1
                print(f"{player.name} received a Bandit's Dagger!")
            elif event == "betrayal":
                print("The bandits betray you and attack! 😈")
                enemy = Enemy("Bandit Ambusher", 120, 18, ["Quick Slash"], experience_given=90, agility=14, intelligence=10)
                combat(enemy)
                if game_over:
                    return
            elif event == "trade":
                print("The bandits are willing to trade stolen goods.")
                inventory["Stolen Jewelry"] = inventory.get("Stolen Jewelry", 0) + 1
                print(f"{player.name} obtained Stolen Jewelry!")
            else:
                print("The bandits are not interested in negotiating.")
        elif choice == "3":
            event = random.choice(["learn_info", "caught", "nothing"])
            if event == "learn_info":
                print("You spy on the bandits and learn valuable information. 🕵️")
                inventory["Bandit Map"] = inventory.get("Bandit Map", 0) + 1
                print(f"{player.name} obtained a Bandit Map!")
            elif event == "caught":
                print("You are caught spying and have to flee! 🏃")
                player.health -= 15
                print(f"{player.name} loses 15 health during the escape.")
                if player.health <= 0:
                    print(f"{player.name} didn't survive the escape.")
                    game_over = True
            else:
                print("You observe but gain no useful information.")
        elif choice == "4":
            print("You set traps around their camp. 🪤")
            success = random.choice([True, False])
            if success:
                print("Your traps incapacitate some bandits! 🎉")
                inventory["Trap Components"] = inventory.get("Trap Components", 0) + 1
                print(f"{player.name} collected Trap Components.")
            else:
                print("You were caught setting traps! 😱")
                enemy = Enemy("Bandit Scout", 100, 15, ["Quick Shot"], experience_given=70, agility=13, intelligence=9)
                combat(enemy)
                if game_over:
                    return
        elif choice == "5":
            print("You challenge the Bandit Leader to a duel.")
            enemy = Enemy("Bandit Leader", 150, 20, ["Power Attack"], experience_given=100, agility=15, intelligence=12)
            combat(enemy)
            if game_over:
                return
            print("You defeated the Bandit Leader and found treasure!")
            inventory["Bag of Gold"] = inventory.get("Bag of Gold", 0) + 1
            print(f"{player.name} obtained a Bag of Gold! 💰")
        elif choice == "6":
            print("You decide to leave the Bandit's Lair.")
            return
        else:
            print("That's not a valid choice.")

def mystic_river():
    global game_over
    while True:
        # Random encounter chance
        if random.randint(1, 100) <= 30:
            random_encounter()
            if game_over:
                return
        # Scenario: The Mystic River
        print("\n🌊 You are at the Mystic River.")
        print("Options:")
        print("1. Fish in the river")
        print("2. Drink the water")
        print("3. Meditate by the river")
        print("4. Build a raft")
        print("5. Search for river spirits")
        print("6. Leave the river")
        choices = ['1', '2', '3', '4', '5', '6']
        choice = get_player_input("What do you want to do? ", choices)
        if choice == '?':
            continue
        print()

        if choice == "1":
            event = random.choice(["catch_fish", "nothing", "monster", "treasure"])
            if event == "catch_fish":
                print("You catch a strange fish. 🐟")
                inventory["Mystic Fish"] = inventory.get("Mystic Fish", 0) + 1
                print(f"{player.name} obtained a Mystic Fish!")
            elif event == "nothing":
                print("You spend hours but catch nothing.")
            elif event == "monster":
                print("A river monster emerges and attacks! 🐉")
                enemy = Enemy("River Serpent", 140, 22, ["Tail Whip"], experience_given=110, agility=16, intelligence=12)
                combat(enemy)
                if game_over:
                    return
            elif event == "treasure":
                print("You reel in a sunken treasure chest! 💎")
                inventory["Gold Coin"] = inventory.get("Gold Coin", 0) + 1
                print(f"{player.name} obtained a Gold Coin!")
            else:
                print("Nothing happens.")
        elif choice == "2":
            event = random.choice(["heal", "poison", "stat_increase", "nothing"])
            if event == "heal":
                print("You drink the water and feel rejuvenated. 💧")
                player.health = player.max_health
                print(f"{player.name}'s health is fully restored!")
            elif event == "poison":
                print("The water is poisoned! ☠️")
                player.health -= 20
                print(f"{player.name} loses 20 health.")
                if player.health <= 0:
                    print(f"{player.name} has succumbed to the poison.")
                    game_over = True
            elif event == "stat_increase":
                print("The magical water enhances your abilities!")
                stat_increase = random.choice(["Strength", "Agility", "Intelligence"])
                player.stats[stat_increase] += 2
                print(f"{player.name}'s {stat_increase} increased by 2!")
            else:
                print("You drink the water but feel no different.")
        elif choice == "3":
            event = random.choice(["gain_insight", "disturbed", "nothing"])
            if event == "gain_insight":
                print("You meditate and gain insights. 🧘")
                stat_increase = random.choice(["Strength", "Agility", "Intelligence"])
                player.stats[stat_increase] += 1
                print(f"{player.name}'s {stat_increase} increased by 1!")
            elif event == "disturbed":
                print("Your meditation is disturbed by unsettling visions. 😱")
                player.stats["Intelligence"] -= 1
                print(f"{player.name}'s Intelligence decreased by 1!")
            else:
                print("You meditate but feel no different.")
        elif choice == "4":
            print("You build a raft and sail downstream. 🚣")
            event = random.choice(["waterfall", "safe", "treasure", "storm"])
            if event == "waterfall":
                print("You fall over a waterfall and take damage! 🌊")
                player.health -= 30
                if player.health <= 0:
                    print(f"{player.name} didn't survive the fall.")
                    game_over = True
                    return
                print(f"{player.name} survives but is injured.")
            elif event == "safe":
                print("You safely reach a new location.")
                if "Ancient Ruins" not in unlocked_locations:
                    unlocked_locations.append("Ancient Ruins")
                    print("A new location has been unlocked: Ancient Ruins! 🏛️")
                ancient_ruins()
                return
            elif event == "treasure":
                print("You find a floating chest in the river! 🎁")
                inventory["Gold Coin"] = inventory.get("Gold Coin", 0) + 1
                print(f"{player.name} obtained a Gold Coin!")
            elif event == "storm":
                print("A sudden storm capsizes your raft! ⛈️")
                player.health -= 20
                if player.health <= 0:
                    print(f"{player.name} didn't survive the storm.")
                    game_over = True
                    return
                print(f"{player.name} manages to swim to shore, injured.")
            else:
                print("Nothing happens.")
        elif choice == "5":
            event = random.choice(["spirit_blessing", "spirit_curse", "nothing"])
            if event == "spirit_blessing":
                print("A river spirit blesses you! ✨")
                player.stats["Agility"] += 2
                print(f"{player.name}'s Agility increased by 2!")
            elif event == "spirit_curse":
                print("A river spirit curses you! 😈")
                player.stats["Strength"] -= 2
                print(f"{player.name}'s Strength decreased by 2!")
            else:
                print("You find no spirits today.")
        elif choice == "6":
            print("You decide to leave the Mystic River.")
            return
        else:
            print("That's not a valid choice.")

def forgotten_caves():
    global game_over
    while True:
        # Random encounter chance
        if random.randint(1, 100) <= 30:
            random_encounter()
            if game_over:
                return
        # Scenario: The Forgotten Caves
        print("\n🕳️ You are in the Forgotten Caves.")
        print("Options:")
        print("1. Explore the caves")
        print("2. Look for treasure")
        print("3. Set up camp")
        print("4. Search for ancient writings")
        print("5. Face the Cave Beast")
        print("6. Leave the caves")
        choices = ['1', '2', '3', '4', '5', '6']
        choice = get_player_input("What do you want to do? ", choices)
        if choice == '?':
            continue
        print()

        if choice == "1":
            enemy = Enemy("Cave Troll", 180, 25, ["Smash"], experience_given=120, agility=12, intelligence=6)
            combat(enemy)
            if game_over:
                return
            print("You defeated the Cave Troll!")
            inventory["Troll's Club"] = inventory.get("Troll's Club", 0) + 1
            print(f"{player.name} obtained a Troll's Club! 🪓")
        elif choice == "2":
            event = random.choice(["find_relic", "trap", "nothing", "stat_increase"])
            if event == "find_relic":
                print("You search for treasure and find an ancient relic. 🗿")
                inventory["Ancient Relic"] = inventory.get("Ancient Relic", 0) + 1
                print(f"{player.name} obtained an Ancient Relic!")
            elif event == "trap":
                print("You trigger a trap and take damage! 💥")
                trap_damage = random.randint(15, 30)
                player.health -= trap_damage
                print(f"{player.name} loses {trap_damage} health.")
                if player.health <= 0:
                    print(f"{player.name} didn't survive the trap.")
                    game_over = True
            elif event == "stat_increase":
                print("You find a hidden training ground! 🏋️")
                player.stats["Strength"] += 1
                print(f"{player.name}'s Strength increased by 1!")
            else:
                print("You search but find nothing.")
        elif choice == "3":
            event = random.choice(["heal", "enemy", "dream", "nothing"])
            if event == "heal":
                print("You rest peacefully and restore health. 😴")
                heal_amount = 30 + player.stats["Intelligence"] // 2
                actual_heal = min(heal_amount, player.max_health - player.health)
                player.health += actual_heal
                print(f"{player.name}'s health is restored by {actual_heal} points.")
            elif event == "enemy":
                print("You are attacked by cave bats during your rest! 🦇")
                enemy = Enemy("Bat Swarm", 60, 10, ["Bite"], experience_given=50, agility=15, intelligence=5)
                combat(enemy)
                if game_over:
                    return
            elif event == "dream":
                event_outcome = random.choice(["good_dream", "nightmare"])
                if event_outcome == "good_dream":
                    print("You have a vivid dream, unlocking new potential. 💫")
                    player.stats["Intelligence"] += 1
                    print(f"{player.name}'s Intelligence increased by 1!")
                else:
                    print("You have a nightmare and wake up in a panic. 😱")
                    player.health -= 10
                    print(f"{player.name} loses 10 health.")
                    if player.health <= 0:
                        print(f"{player.name} didn't survive the shock.")
                        game_over = True
                        return
            else:
                print("Your rest is uneventful.")
        elif choice == "4":
            event = random.choice(["knowledge", "nothing", "trap", "enemy"])
            if event == "knowledge":
                print("You find ancient writings that grant knowledge. 📜")
                stat_increase = random.choice(["Strength", "Agility", "Intelligence"])
                player.stats[stat_increase] += 2
                print(f"{player.name}'s {stat_increase} increased by 2!")
            elif event == "trap":
                print("A trap triggers and you are injured! 💥")
                trap_damage = random.randint(10, 25)
                player.health -= trap_damage
                print(f"{player.name} loses {trap_damage} health.")
                if player.health <= 0:
                    print(f"{player.name} didn't survive the trap.")
                    game_over = True
            elif event == "enemy":
                print("An ancient guardian attacks you! 🛡️")
                enemy = Enemy("Stone Guardian", 150, 20, ["Smash"], experience_given=100, agility=10, intelligence=8)
                combat(enemy)
                if game_over:
                    return
            else:
                print("You find nothing of interest.")
        elif choice == "5":
            print("You decide to face the Cave Beast.")
            enemy = Enemy("Cave Beast", 200, 30, ["Roar"], experience_given=150, agility=15, intelligence=10)
            combat(enemy)
            if game_over:
                return
            inventory["Beast Claw"] = inventory.get("Beast Claw", 0) + 1
            print(f"{player.name} obtained a Beast Claw!")
        elif choice == "6":
            print("You decide to leave the Forgotten Caves.")
            return
        else:
            print("That's not a valid choice.")

def ancient_ruins():
    global game_over
    while True:
        # Random encounter chance
        if random.randint(1, 100) <= 30:
            random_encounter()
            if game_over:
                return
        # Scenario: The Ancient Ruins
        print("\n🏛️ You are at the Ancient Ruins.")
        print("Options:")
        print("1. Enter the temple")
        print("2. Search for artifacts")
        print("3. Decode inscriptions")
        print("4. Set up camp")
        print("5. Perform a ritual")
        print("6. Leave the ruins")
        choices = ['1', '2', '3', '4', '5', '6']
        choice = get_player_input("What do you want to do? ", choices)
        if choice == '?':
            continue
        print()

        if choice == "1":
            enemy = Enemy("Ancient Guardian", 200, 30, ["Blast"], experience_given=150, agility=15, intelligence=20)
            combat(enemy)
            if game_over:
                return
            inventory["Guardian's Shield"] = inventory.get("Guardian's Shield", 0) + 1
            print(f"{player.name} obtained the Guardian's Shield! 🛡️")
        elif choice == "2":
            event = random.choice(["find_artifact", "trap", "nothing", "enemy"])
            if event == "find_artifact":
                print("You find rare artifacts. 💎")
                inventory["Golden Idol"] = inventory.get("Golden Idol", 0) + 1
                print(f"{player.name} obtained a Golden Idol!")
            elif event == "trap":
                print("A trap triggers and you are injured! 💥")
                trap_damage = random.randint(20, 35)
                player.health -= trap_damage
                print(f"{player.name} loses {trap_damage} health.")
                if player.health <= 0:
                    print(f"{player.name} didn't survive the trap.")
                    game_over = True
            elif event == "enemy":
                print("A cursed spirit attacks you! 👻")
                enemy = Enemy("Cursed Spirit", 160, 25, ["Curse"], experience_given=130, agility=18, intelligence=22)
                combat(enemy)
                if game_over:
                    return
            else:
                print("You search but find nothing.")
        elif choice == "3":
            event = random.choice(["wisdom", "nothing", "trap", "enemy"])
            if event == "wisdom":
                print("You decode inscriptions and gain wisdom. 🧠")
                player.stats["Intelligence"] += 2
                print(f"{player.name}'s Intelligence increased by 2!")
            elif event == "trap":
                print("A magical trap saps your energy! 💫")
                player.stats["Strength"] -= 1
                player.stats["Agility"] -= 1
                print(f"{player.name}'s Strength and Agility decreased by 1!")
            elif event == "enemy":
                print("An ancient mage's spirit attacks you! 🔮")
                enemy = Enemy("Ancient Mage", 170, 28, ["Arcane Blast"], experience_given=140, agility=16, intelligence=25)
                combat(enemy)
                if game_over:
                    return
            else:
                print("You cannot decipher the inscriptions.")
        elif choice == "4":
            event = random.choice(["heal", "enemy", "dream", "nothing"])
            if event == "heal":
                print("You set up camp and rest. 🏕️")
                heal_amount = 40 + player.stats["Intelligence"] // 2
                actual_heal = min(heal_amount, player.max_health - player.health)
                player.health += actual_heal
                print(f"{player.name}'s health is restored by {actual_heal} points.")
            elif event == "enemy":
                print("You are attacked by ruins guardians during your rest! 🛡️")
                enemy = Enemy("Ruins Guardian", 160, 22, ["Smash"], experience_given=120, agility=12, intelligence=10)
                combat(enemy)
                if game_over:
                    return
            elif event == "dream":
                event_outcome = random.choice(["good_dream", "nightmare"])
                if event_outcome == "good_dream":
                    print("You have a prophetic dream about the dragon. 🐉")
                    print(f"{player.name} gains insight about the dragon!")
                else:
                    print("You have a nightmare and wake up unsettled. 😰")
                    player.stats["Intelligence"] -= 1
                    print(f"{player.name}'s Intelligence decreased by 1!")
            else:
                print("Your rest is uneventful.")
        elif choice == "5":
            if "Spirit Essence" in inventory:
                print("You perform a ritual using the Spirit Essence.")
                inventory["Spirit Essence"] -= 1
                if inventory["Spirit Essence"] == 0:
                    del inventory["Spirit Essence"]
                print("The ritual enhances your abilities! ✨")
                player.stats["Strength"] += 2
                player.stats["Agility"] += 2
                player.stats["Intelligence"] += 2
                print(f"{player.name}'s stats have increased!")
            else:
                print("You don't have the necessary items for a ritual.")
        elif choice == "6":
            print("You decide to leave the Ancient Ruins.")
            return
        else:
            print("That's not a valid choice.")

def dragons_peak():
    global game_over
    while True:
        # Random encounter chance
        if random.randint(1, 100) <= 20:
            random_encounter()
            if game_over:
                return
        # Scenario: Dragon's Peak
        print("\n⛰️ You are at Dragon's Peak.")
        print("Options:")
        print("1. Seek the dragon")
        print("2. Search for dragon eggs")
        print("3. Collect rare herbs")
        print("4. Build a shelter")
        print("5. Leave Dragon's Peak")
        choices = ['1', '2', '3', '4', '5']
        choice = get_player_input("What do you want to do? ", choices)
        if choice == '?':
            continue
        print()

        if choice == "1":
            final_decision()
            if game_over:
                return
        elif choice == "2":
            event = random.choice(["found", "caught", "nothing"])
            if event == "found":
                inventory["Dragon Egg"] = inventory.get("Dragon Egg", 0) + 1
                print(f"{player.name} found a Dragon Egg! 🥚")
            elif event == "caught":
                print("The dragon catches you! 😱")
                final_decision()
                if game_over:
                    return
            else:
                print("You search but find no eggs.")
        elif choice == "3":
            event = random.choice(["found_herbs", "poisonous_herb", "nothing"])
            if event == "found_herbs":
                print("You collect rare mountain herbs. 🌿")
                inventory["Mountain Herb"] = inventory.get("Mountain Herb", 0) + 1
                print(f"{player.name} obtained a Mountain Herb!")
            elif event == "poisonous_herb":
                print("You accidentally collect poisonous herbs! ☠️")
                player.health -= 20
                print(f"{player.name} loses 20 health.")
                if player.health <= 0:
                    print(f"{player.name} didn't survive the poison.")
                    game_over = True
            else:
                print("You find nothing of interest.")
        elif choice == "4":
            event = random.choice(["heal", "storm", "nothing"])
            if event == "heal":
                print("You build a shelter and rest. 🏕️")
                heal_amount = 30 + player.stats["Intelligence"] // 2
                actual_heal = min(heal_amount, player.max_health - player.health)
                player.health += actual_heal
                print(f"{player.name}'s health is restored by {actual_heal} points.")
            elif event == "storm":
                print("A storm damages your shelter! ⛈️")
                player.health -= 20
                print(f"{player.name} loses 20 health.")
                if player.health <= 0:
                    print(f"{player.name} didn't survive the storm.")
                    game_over = True
            else:
                print("Your rest is uneventful.")
        elif choice == "5":
            print("You decide to leave Dragon's Peak.")
            return
        else:
            print("That's not a valid choice.")

def matrix_world():
    global game_over
    # Scenario: Matrix World
    print("\n🕶️ You have stumbled into the Matrix World.")
    print("Everything seems digital and surreal.")
    print("Options:")
    print("1. Explore the city")
    print("2. Hide from the robots")
    print("3. Look for weapons")
    print("4. Try to find an exit")
    choices = ['1', '2', '3', '4']
    choice = get_player_input("What do you want to do? ", choices)
    if choice == '?':
        return matrix_world()
    print()

    if choice == "1":
        event = random.choice(["agent", "resistance", "nothing"])
        if event == "agent":
            print("An Agent spots you! 🤖")
            enemy = Enemy("Agent", 1000, 100, ["Gunshot"], experience_given=0, agility=50, intelligence=50)
            combat(enemy)
            if game_over:
                return
        elif event == "resistance":
            print("You meet the resistance who help you find an exit. 🕳️")
            if "Neo's Sunglasses" not in inventory:
                inventory["Neo's Sunglasses"] = inventory.get("Neo's Sunglasses", 0) + 1
                print(f"{player.name} obtained Neo's Sunglasses! 🕶️")
            print("You safely return to the real world.")
        else:
            print("You wander the city unnoticed.")
    elif choice == "2":
        success = random.randint(1, 36) + player.stats["Agility"] // 2
        if success > 30:
            print("You successfully hide from the robots. 🤫")
        else:
            print("The robots find you! ⚠️")
            enemy = Enemy("Sentinel", 800, 80, ["Laser Beam"], experience_given=0, agility=40, intelligence=40)
            combat(enemy)
            if game_over:
                return
    elif choice == "3":
        print("You search for weapons.")
        event = random.choice(["find_weapon", "ambush", "nothing"])
        if event == "find_weapon":
            print("You find a futuristic weapon with unimaginable power! 🔫")
            inventory["Plasma Rifle"] = inventory.get("Plasma Rifle", 0) + 1
            print(f"{player.name} obtained a Plasma Rifle!")
        elif event == "ambush":
            print("Robots ambush you while searching! ⚠️")
            enemy = Enemy("Drone", 600, 60, ["Shock"], experience_given=0, agility=35, intelligence=35)
            combat(enemy)
            if game_over:
                return
        else:
            print("You find nothing.")
    elif choice == "4":
        print("You try to find an exit.")
        success = random.randint(1, 36) + player.stats["Intelligence"] // 2
        if success > 30:
            print("You find a portal and escape the Matrix World! 🌐")
            print("You return to your world with newfound knowledge.")
        else:
            print("You can't find an exit and are stuck!")
            game_over = True
            print("Ending: Trapped in the Matrix")
    else:
        print("That's not a valid choice.")

def final_decision():
    global game_over
    # Final decision leading to different endings
    print("\n🔥 After your long journey, you encounter the dragon.")
    print("Options:")
    print("1. Fight the dragon")
    print("2. Use a special item")
    print("3. Attempt to communicate")
    choices = ['1', '2', '3']
    choice = get_player_input("Enter the number of your choice: ", choices)
    if choice == '?':
        return final_decision()
    print()  # Add a blank line between choice and output

    if choice == "1":
        enemy = Enemy("Dragon", 1000, 80, ["Fire Breath", "Tail Swipe", "Roar"], experience_given=500, agility=35, intelligence=40)
        combat(enemy)
        if game_over:
            return
        if enemy.health <= 0:
            print(f"{player.name} slayed the dragon and became a legend! 🏆🐲")
            print("Ending: Dragon Slayer")
            game_over = True
        else:
            print("You managed to escape from the dragon!")
            # Allow the player to continue the game
    elif choice == "2":
        if "Dragon Egg" in inventory:
            print(f"{player.name} presents the Dragon Egg.")
            print("The dragon is pleased and grants you a wish. 🌠")
            print("Ending: Wish Granted")
            game_over = True
        elif "Golden Idol" in inventory:
            print(f"{player.name} offers the Golden Idol.")
            print("The dragon accepts the tribute and allows you to leave. 🛡️")
            print("Ending: Peaceful Resolution")
            game_over = True
        else:
            print("You have no special item to use.")
            print("The dragon becomes enraged! 😠")
            enemy = Enemy("Enraged Dragon", 1000, 90, ["Firestorm"], experience_given=500, agility=38, intelligence=45)
            combat(enemy)
            if game_over:
                return
            if enemy.health <= 0:
                print(f"{player.name} slayed the dragon and became a legend! 🏆🐲")
                print("Ending: Dragon Slayer")
                game_over = True
            else:
                print("You managed to escape from the enraged dragon!")
    elif choice == "3":
        success = random.randint(1, 10) + player.stats["Intelligence"] // 2
        if success > 12:
            print(f"{player.name} communicates with the dragon and forms an alliance! 🤝")
            print("Ending: Dragon Ally")
            game_over = True
        else:
            print("The dragon rejects your attempt and attacks! 🐉")
            enemy = Enemy("Dragon", 1000, 80, ["Fire Breath", "Tail Swipe", "Roar"], experience_given=500, agility=35, intelligence=40)
            combat(enemy)
            if game_over:
                return
            if enemy.health <= 0:
                print(f"{player.name} slayed the dragon and became a legend! 🏆🐲")
                print("Ending: Dragon Slayer")
                game_over = True
            else:
                print("You managed to escape from the dragon!")
    else:
        print("That's not a valid choice.")

# =========================================
#             Game Loop
# =========================================

def main():
    game_intro()
    create_character()

    while not game_over:
        choose_location()
        if game_over:
            break

    if not game_over:
        final_decision()
        if game_over:
            print("Game Over.")
        else:
            print("Congratulations! You've completed your adventure.")

if __name__ == "__main__":
    main()
