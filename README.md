# Classic CRPG Project

A data-driven, turn-based CRPG system inspired by classic 80s and 90s titles.

---

## 1. Project Overview

The core philosophy of this project is **Data-Driven Design**.  
All game rules (Races, Classes, Skills, Items, etc.) are defined in human-readable JSON files inside the `data/` directory.

### Core Engine

pygame==2.5.2

### Data/Utility

Pydantic for schema validation later

### If using a specific version of Python, specify it here (e.g., python>=3.10)

---

### Key Directories

- **data/**  
  Contains all static game design files (`races.json`, `classes.json`, `skills.json`, etc.).

- **docs/**  
  Contains markdown files detailing the game's mechanics and design decisions (`character_generation.md`, `progression_mechanics.md`).

- **saved_games/**  
  Stores saved character files (`characters.json`) and future game state data. Will be created when the first character is saved if it does not exist.

- **rendering/**  
  Planned home for rendering and UI modules.

---

## 2. Setup (Getting Started)

### Prerequisites

- Python **3.8+**

### Installation Steps

#### 1. Clone the Repository

```bash
git clone https://github.com/keithyw/kyw_rpg.git
cd kyw_rpg
```
