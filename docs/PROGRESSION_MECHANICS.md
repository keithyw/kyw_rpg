### Unified Points-Based Progression System

This system uses a single pool of points, derived from a starting Character Creation Budget and earned through experience (XP), to purchase all forms of advancement: acquiring new classes, unlocking specialized kits, and improving skills.

### Class Tiers and Acquisition Cost

Classes are organized into tiers based on their specialization and power level. Acquisition uses the Progression Points (PP) pool.

| Class Tier              | Example (Concept)                     | PP Cost to Acquire     | Description                                                                                                                                                                                 |
| ----------------------- | ------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tier 1: Generic         | Fighter, Cleric, Rogue, Mage          | 10                     | Core, versatile classes with broad skill access and lower attribute requirements. Suitable for multiclassing foundations.                                                                   |
| Tier 2: Specialized     | Paladin, Ranger, Bard, Assassin       | 20                     | Focused classes requiring higher attributes and providing access to more potent, restricted skill sets (e.g., Divine Magic, Stealth Attack).                                                |
| Tier 3: Kits / Prestige | Undead Hunter, Archmage, Shadowdancer | 40                     | Highly specialized paths that provide unique mechanics, often overriding or modifying core class features. Kits usually require an existing Tier 1 or 2 class (e.g., Ranger -> Archer Kit). |
| Tier 4: Ascended        | Avatar, Demigod, Archlich             | 80 (Unlock Multiplier) | Reserved for late-game progression, often requiring high total XP or completing a specific quest (unlock condition).                                                                        |

### Multiclassing Rule

A character may acquire any number of classes, provided they meet the class's minimum attribute requirements and pay the PP Cost.

- Balance Mechanism: The system is balanced by the finite pool of starting PP and the high cost of maintaining too many disparate skill sets (since skills must also be purchased with PP).

### Skill Acquisition and Improvement

Skills (both combat and non-combat) are also purchased using the Progression Points (PP) pool.

| Advancement Type  | PP Cost Formula      | Notes                                                                                                                                                      |
| ----------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Skill Acquisition | 2 PP (Initial)       | The cost to acquire a skill and gain its Starting Base Value (derived from the controlling attribute, as defined in `data/*_skills.json`).                 |
| Skill Improvement | 1 PP per 5% increase | Cost to raise a skill's percentage proficiency above its starting value. This cost may increase exponentially at very high skill levels (e.g., above 90%). |

### Experience and Progression Point Gain

Characters do not gain "levels" in the traditional sense. Instead, XP is converted directly into Progression Points (PP).

- XP Conversion: Every [TBD] points of XP earned yields 1 PP.
- XP Distribution: XP is awarded for defeating enemies, completing quests, and successfully using non-combat skills. The total XP is distributed among active party members.

### Class XP Debt (Suggested)

To prevent extreme over-multiclassing, acquiring a new class could incur an XP Debt multiplier.

- Example: A 3rd class imposes a 1.2x multiplier on all future XP earned before it is converted to PP. This makes further specialization more expensive over time.

### Party Management and Recruitment

#### Party Slots

The party capacity is 16 total slots.

- Initial Slots: The player begins with 6 available slots.
- Acquisition: Additional slots (up to 16) are acquired through:
  - PP Purchase: 50 PP per additional slot.
  - Quests: Certain major quests may unlock a new slot.
- Recruitment: Recruitable NPCs automatically occupy an available party slot. Once recruited, they are fully customizable PCs, consuming a slot until dismissed.
