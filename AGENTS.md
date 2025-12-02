## 🤖 AGENTS.md: Classic CRPG Project Guide

### 1. 🎯 Project Overview & Vibe

- **Goal:** Build a modular, turn-based CRPG system inspired by classic 80s titles (Bard's Tale 3, Wizardry 6, Ultima 4-6, Might and Magic 2).
- **Engine:** Pygame (for rendering and main loop).
- **Core Principle:** **Data-Driven Design.** Game rules (Races, Classes, Items) must be defined primarily in easily editable **JSON files**, separating game design from Python logic. Python classes should read and apply this static data.
- **Target Party Size:** Up to 16 characters.
- **This Document:** Considered a living document. Game rules in the .json files will be updated too
  for balance reasons as well as for features.

---

### 2. 📁 Project File Structure

Format: `file_name: description. notes`

- main.py: Pygame Initialization & Main Game Loop. Entry point. Handles switching between major views (Map, Combat, Menu).
- game_manager.py: Game State Management. Handles saving/loading state, global variables, and game flow control.
- data_loader.py: Data Utility. Function to load all static data from the `data/` directory.
- character.py: Character Logic. Defines the **`Character` class** (used for both Players and Monsters).
- combat.py: Combat Engine. Logic for the **Turn-Based Combat** system.
- rendering/: UI and Rendering Modules. Specialized drawing functions for different views.
- data/: Static Game Data (JSON). All game design elements live here.

### 3. 💾 Data Definitions (JSON Schemas)

data/\*.json files are used as schemas to define the game data. These files will impose certain
rules/restrictions on things such a which classes a race can choose from or what skills a class
can use. There should be descriptions and other meta data to help the AI understand the function/usage
as well as flavor text where a key is used.

#### Core Attributes `data/core_attributes.json`

This file defines the attributes for characters and NPCs in this game. It's more of a description of
what the attributes are and how they are used in the game. At this stage, this file has no strict
rules on what they do.

- `STR`: Integer. Strength (Physical power and striking force).
- `DEX`: Integer. Dexterity (Hand-eye coordination, quickness, and manual skill).
- `SPD`: Integer. Speed (Reaction time and overall swiftness).
- `VIT`: Integer. Vitality (Hardiness, health, and resistance to physical ailments).
- `INT`: Integer. Intelligence (Mental acuity, memory, and arcane knowledge).
- `PER`: Integer. Personality (Charm, persuasion, and outward social grace).
- `WIL`: Integer. Willpower (Inner mental strength, devotion, and sheer stubbornness).

#### Races `data/races.json`

This file defines the races for characters and NPCs in this game. Races may have a subrace or have
a "default" race (e.g. a human). The subrace itself will have modifiers for attributes, skills and
limitations such as class picks.

- `name`: String. The race's name.
- `description`: String. A description of the race.
- `sub_races`: List. A list of sub-races available for this race.
  - `$subrace_name`: String. The sub-race's key.
  - `name`: String. The sub-race's fullname.
  - `base_minimums`: Dict. Minimum attribute scores required. The attributes are based on the core attributes.
  - `class_limits`: List. A list of class keys this race _cannot_ use nor multi/dual class into.
  - `hp_mod`: Int (need to correct some values). Bonus/penalty to HP
  - `resistances`: Dict. Resistances to damage types or debuffs. These values are percentage based and additive.
  - `skill_bonuses`: Dict. Characters choosing this race will start with these skills with the minimum level specified.
  - `innate_abilities`: List. A list of innate abilities which are spell-like and are either passive or can be activated.
  - `equipment_bonuses`: Dict. Bonus/penalty to equipment skills.

#### Classes `data/classes.json`

This file contains core classes for the game. Refer to docs/CHARACTER_CLASSES.md for more information on the structure
of the file.

#### Non-Combat Skills `data/noncombat_skills.json`

Contains a list of non-combat skills. These skills are used for skills checks and are not combat related.
Some examples of usage are: if a character can climb a mountain and their success rate (e.g. do they
fall off), some percentage rate for picking a lock. Some skills might produce an artifact such as
a weapon. The keys in the skills might change though.

- skill: dict
  - name: String. Fullname for skill to display
  - description: String. Flavor text description of the skill
  - primary_stat_key: String. The primary attribute that governs skill success (e.g., "DEX" for Lockpicking). Might change this aspect in the future.
  - mechanical_type: String. Defines how the skill is checked (e.g., "Wasteland" for % chance, "Wizardry" for hidden formula).
  - base_start_value: Int. The base value for the skill.

#### Combat Skills `data/combat_skills.json`

Contains a list of weapon and armor skills. This is not a list of equipment itself.

- skill type: dict (melee, ranged, defense)
  - skill: dict (key name of the skill)
    - name: String. Fullname for skill to display
    - description: String. Flavor text description of the skill
    - primary_stat_key: String. The primary attribute that governs skill success (e.g., "DEX" for Lockpicking). Might change this aspect in the future.
    - mechanical_type: String. Defines how the skill is checked (e.g., "Wasteland" for % chance, "Wizardry" for hidden formula). Will probably get rid of this.
    - base_start_value: Int. Probably will get rid of this. Instead, this value should be defined by race/class.

### Spell Schools `data/spell_schools.json`

Contains a list of spell schools. Classes may belong to zero or more spell schools. This
list only defines the schools and their properties as well as general description. This is not
a final list while spells themselves will be defined elsewhere. Currently, we have not defined
which classes belong to which schools.

- school: dict
  - name: String. Fullname for school to display
  - description: String. Flavor text description of the school
  - primary_stat_key: String. The primary attribute that governs school success (e.g., "INT" for Arcane Magic).
  - damage_type: String. The damage type associated with the school. Damage types should refer to the damage_types.json file for eligible values.

### Gear Slots `data/gear_slots.json`

This file contains the gear slots for the game. It defines the equipment slots, jewelry slots, and utility slots.

- equipment_slots: dict
  - "worn_slots": dict - armor slots and weapon slots that can be filled
    - key: string - slot name
    - value: dict
      - limit: int - number of items that can be worn in this slot. For main_hand/off_hand, the slot might be occupied by a two handed item like a weapon. When one is used, the off_hand slot becomes unavailable until the main_hand slot is changed.
      - type: list - types of items that can be worn in this slot
  - "jewelry_slots": dict - jewelry slots that can be filled
    - key: string - slot name
    - value: dict
      - limit: int - number of items that can be worn in this slot
      - type: list - types of items that can be worn in this slot
  - "utility_slots": dict - utility slots that can be filled
    - key: string - slot name
    - value: dict
      - limit: int - number of items that can be worn in this slot
      - type: list - types of items that can be worn in this slot

#### Gear Properties `data/gear_properties.json`

This file contains the materials that gear are made of. For instance, you can have a steel long sword.
These properties will influence attributes, weight, etc. Also, for crafting, when an item is decomposed,
it may break down into these materials for crafting. Or these materials might be used to create a new
item.

- material: dict
  - name: String. Fullname for material to display
  - description: String. Flavor text description of the material
  - tier: Int. The tier of the material. Tiers dictate the rarity, value and difficulty of obtaining the material.
  - weight: String. The weight of the material
  - default_resistance_mod: Dict. The default resistance modifiers for the material

### Damage Types `data/damage_types.json`

This file contains the damage types and effects (debuffs) for spells, weapons, monsters, etc.

- damage_type: dict

  - name: String. Fullname for damage type to display
  - description: String. Flavor text description of the damage type
  - elemental: Boolean. Whether the damage type is elemental
  - effect_key: String. The key for the effect associated with the damage type. This can be a debuff
    or something that causes a bonus like a critical hit. Refer to status_effects underneath.

- weapon_physical_damage_types: dict - Different damage types can have bonuses or penalties against armor, monsters and influence the type of an attack a character or NPC can perform during a round of combat.

  - damage_type: dict
    - name: String. Fullname for damage type to display
    - description: String. Flavor text description of the damage type

- status_effects: dict - Different status effects can have bonuses or penalties against armor, monsters and influence the type of an attack a character or NPC can perform during a round of combat.

  - status_effect: dict
    - name: String. Fullname for status effect to display
    - description: String. Flavor text description of the status effect

- damage_modifiers: dict - Different damage modifiers can have bonuses or penalties against armor, monsters and influence the type of an attack a character or NPC can perform during a round of combat.
  - damage_modifier: dict
    - name: String. Fullname for damage modifier to display
    - description: String. Flavor text description of the damage modifier

#### Character Schema `data/character_schema.json`

- `name`: String. The character's name.
- `sex`: String. The character's sex (M/F/O).
- `race_key`: String. The primary race identifier.
- `sub_race_key`: String. The sub-race identifier.
- `class_key`: String. The specific class identifier (sub_class key).
- `level`: Integer. Current character level.
- `base_attributes`: Dict. Unmodified attribute scores from roll and point buy.
- `final_attributes`: Dict. Calculated final attribute scores (Base + Racial Mods + Gear Mods).
- `skills`: Dict. All skill proficiencies (percentage values).
- `inventory`: List. Non-equipped items.
- `equipment`: Dict. Currently equipped gear, keyed by slot.
- `current_hp`: Integer. Current Health Points.
- `max_hp`: Integer. Maximum Health Points.

### Other Files for Agents

#### CHARACTER_CREATION_FLOW.md

This file contains how the character creation process will work.
