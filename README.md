# Text-Based RPG Adventure Game

Welcome to the Text-Based RPG Adventure Game! In this game, you create a character and embark on an adventure, making choices that affect the outcome of the story. You'll encounter various locations, enemies, and items as you progress.

## Table of Contents
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Available Commands](#available-commands)
- [Classes](#classes)
- [Abilities](#abilities)
- [Items](#items)
- [Locations](#locations)
- [Gameplay Tips](#gameplay-tips)

## Installation
No installation is required. Simply run the Python script to start the game.

## How to Play
Run the game script using Python:

```bash
python adventure_game.py
```

Follow the on-screen prompts to create your character and make choices throughout your adventure.

## Available Commands
At any time during the game, you can use the following commands:

- **`inventory`** or **`i`**: View your inventory.
- **`stats`** or **`s`**: View your character's stats.
- **`abilities`** or **`a`**: View your abilities.
- **`use item`** or **`u`**: Use an item from your inventory.
- **`discard item`** or **`d`**: Discard an item from your inventory.
- **`?`**: Repeat the last prompt or go back.
- **`help`** or **`h`**: Display the help message.

## Classes
### 1. Warrior
- **Description**: A strong melee fighter with high Strength.
- **Initial Abilities**:
  - Power Strike: A strong attack dealing extra damage.
  - Shield Block: Block incoming attacks, reducing damage.
- **Stats**:
  - Strength: High
  - Agility: Medium
  - Intelligence: Low

### 2. Mage
- **Description**: A master of elemental magic with high Intelligence.
- **Initial Abilities**:
  - Fireball: Cast a fireball to burn enemies.
  - Ice Spike: Launch an ice spike to slow enemies.
- **Stats**:
  - Strength: Low
  - Agility: Medium
  - Intelligence: High

### 3. Rogue
- **Description**: A stealthy assassin with high Agility.
- **Initial Abilities**:
  - Backstab: Attack an enemy from behind for extra damage.
  - Stealth: Become invisible to enemies temporarily.
- **Stats**:
  - Strength: Medium
  - Agility: High
  - Intelligence: Low

### 4. Paladin
- **Description**: A holy knight with balanced Strength and Intelligence.
- **Initial Abilities**:
  - Holy Smite: Deal holy damage to an enemy.
  - Heal: Restore health to yourself or an ally.
- **Stats**:
  - Strength: High
  - Agility: Low
  - Intelligence: Medium

### 5. Ranger
- **Description**: An agile archer skilled in ranged combat.
- **Initial Abilities**:
  - Arrow Shot: Shoot an arrow at an enemy.
  - Trap: Set a trap to immobilize enemies.
- **Stats**:
  - Strength: Medium
  - Agility: High
  - Intelligence: Low

### 6. Necromancer
- **Description**: A dark magician who manipulates life and death.
- **Initial Abilities**:
  - Life Drain: Drain life from an enemy.
  - Raise Undead: Summon undead to fight for you.
- **Stats**:
  - Strength: Low
  - Agility: Low
  - Intelligence: High

### 7. Druid
- **Description**: A guardian of nature with shapeshifting abilities.
- **Initial Abilities**:
  - Nature's Grasp: Entangle enemies with vines.
  - Wild Shape: Transform into a beast.
- **Stats**:
  - Strength: Medium
  - Agility: Medium
  - Intelligence: High

### 8. Monk
- **Description**: A martial artist with balanced Strength and Agility.
- **Initial Abilities**:
  - Flurry of Blows: Deliver rapid strikes.
  - Meditate: Restore health and mana.
- **Stats**:
  - Strength: High
  - Agility: High
  - Intelligence: Low

### 9. , the Creator (Secret Class)
- **Description**: Unlock infinite power by naming your character "Tyler".
- **Initial Abilities**: None
- **Stats**:
  - Strength: Infinite
  - Agility: Infinite
  - Intelligence: Infinite

## Abilities
- **Power Strike**: Deals extra damage based on Strength.
- **Shield Block**: Increases Strength temporarily, reducing incoming damage.
- **Fireball**: Deals damage based on Intelligence.
- **Ice Spike**: Deals damage and slows the enemy.
- **Backstab**: Deals extra damage, especially if the enemy is unaware.
- **Stealth**: Makes you invisible to enemies for a short time.
- **Holy Smite**: Deals holy damage combining Strength and Intelligence.
- **Heal**: Restores health based on Intelligence.
- **Arrow Shot**: Deals damage based on Agility.
- **Trap**: Immobilizes the enemy for several turns.
- **Life Drain**: Deals damage and heals you for a portion of the damage.
- **Raise Undead**: Summons undead to fight for you.
- **Nature's Grasp**: Roots the enemy and deals damage.
- **Wild Shape**: Increases Strength and Agility.
- **Flurry of Blows**: Deals damage based on both Strength and Agility.
- **Meditate**: Restores health.
- **Plasma Blast**: A powerful attack unlocked by equipping the Plasma Rifle.

## Items
- **Health Potion**: Restores 40-60 health.
- **Mana Potion**: Restores mana when you have mana-consuming abilities.
- **Healing Herb**: Restores 15-25 health.
- **Strength Elixir**: Increases Strength by 2.
- **Agility Potion**: Increases Agility by 2.
- **Intelligence Scroll**: Increases Intelligence by 2.
- **Troll's Club**: Equips to increase Strength by 5.
- **Guardian's Shield**: Equips to increase Defense.
- **Plasma Rifle**: Equips to unlock the "Plasma Blast" ability.
- **Enchanted Flower**: Can be given to the Enchantress in the Enchanted Castle.
- **Ancient Relic**: Can be offered to the dragon for a special outcome.
- **Bandit's Dagger**: Can be used during combat for extra damage.
- **Magic Amulet**: Enhances magical abilities when used in combat.
- **Spirit Essence**: Used in specific rituals at the Ancient Ruins.

## Locations
### Haunted Forest
- **Description**: An eerie forest filled with ghosts and hidden paths.
- **Activities**:
  - Explore deeper to encounter enemies or find treasures.
  - Collect herbs with both positive and negative outcomes.
  - Set up camp to rest or risk ambushes.
  - Confront the Forest Spirit for significant rewards.

### Enchanted Castle
- **Description**: A mystical castle with magical inhabitants.
- **Activities**:
  - Knock on the door to interact with wizards or face traps.
  - Sneak in through a window to find treasures or get caught.
  - Search the garden for rare items or enemies.
  - Speak with the Enchantress for blessings or quests.

### Bandit's Lair
- **Description**: A hideout of notorious bandits.
- **Activities**:
  - Attack the bandits to gain loot.
  - Try to negotiate for truce or trades.
  - Spy on them for valuable information.
  - Challenge the Bandit Leader for significant rewards.

### Mystic River
- **Description**: A river with mystical properties.
- **Activities**:
  - Fish to catch rare items or encounter river monsters.
  - Drink the water for healing or stat changes.
  - Meditate by the river for insights or disturbances.
  - Build a raft to explore new areas.

### Forgotten Caves
- **Description**: Ancient caves with hidden dangers and treasures.
- **Activities**:
  - Explore to encounter powerful enemies.
  - Look for treasure with the risk of traps.
  - Set up camp to rest or risk nighttime attacks.
  - Search for ancient writings to gain knowledge.

### Ancient Ruins
- **Description**: Ruins of a long-lost civilization.
- **Activities**:
  - Enter the temple to face guardians.
  - Search for artifacts with potential dangers.
  - Decode inscriptions for stat increases.
  - Perform rituals using special items.

### Dragon's Peak
- **Description**: The lair of a mighty dragon.
- **Activities**:
  - Seek the dragon for a final confrontation.
  - Search for dragon eggs with risks.
  - Collect rare herbs.
  - Build a shelter to rest.

### Matrix World
- **Description**: A digital realm with surreal challenges.
- **Activities**:
  - Explore the city and avoid detection.
  - Hide from robots.
  - Look for futuristic weapons.
  - Try to find an exit back to the real world.

## Gameplay Tips
- **Balance Risk and Reward**: Many choices have both positive and negative outcomes. Weigh your options carefully.
- **Manage Inventory**: Use and discard items strategically. Some items have specific uses in certain locations.
- **Level Up**: Gain experience to increase your stats and unlock new abilities and locations.
- **Prepare for the Dragon**: The dragon is a tough enemy. Consider visiting the Matrix World to obtain the Plasma Rifle before facing it.
- **Use Abilities Wisely**: Abilities can turn the tide in combat. Learn when to use them effectively.
