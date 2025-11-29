import pygame
import random
import json
import os
from enum import Enum, auto

class CreationStep(Enum):
    GENDER = auto()
    RACE = auto()
    SUBRACE = auto()
    CLASS_ARCHETYPE = auto() # Added archetype selection step
    SUBCLASS = auto()
    ROLL_STATS = auto()
    DISTRIBUTE_STATS = auto() # Added distribution step
    SKILLS = auto() # Simplified for now
    PORTRAIT = auto()
    NAME = auto()
    CONFIRM = auto()

class CharacterCreator:
    def __init__(self, game_manager):
        self.gm = game_manager
        self.data = game_manager.data_loader
        self.current_step = CreationStep.GENDER
        
        # Character Data
        self.char_data = {
            "name": "",
            "sex": "",
            "race_key": "",
            "sub_race_key": "",
            "class_key": "", # This will be the subclass key
            "archetype_key": "",
            "level": 1,
            "base_attributes": {},
            "final_attributes": {},
            "skills": {},
            "inventory": [],
            "equipment": {},
            "current_hp": 0,
            "max_hp": 0
        }
        
        # UI State
        self.selected_index = 0
        self.options = []
        self.message = ""
        
        # Temporary data for rolls
        self.base_rolls = {}
        self.bonus_roll = 0
        self.points_remaining = 0
        
        self._init_step()

    def _init_step(self):
        self.selected_index = 0
        self.message = ""
        
        if self.current_step == CreationStep.GENDER:
            self.options = ["Male", "Female", "Other"]
            
        elif self.current_step == CreationStep.RACE:
            self.options = [r.title() for r in self.data.get_races().keys()] + ["Previous"]
            
        elif self.current_step == CreationStep.SUBRACE:
            race_key = self.char_data["race_key"].lower()
            self.options = [s.title() for s in self.data.get_races()[race_key]["sub_races"].keys()] + ["Previous"]
            
        elif self.current_step == CreationStep.CLASS_ARCHETYPE:
            self.options = [c.title() for c in self.data.get_classes().keys()] + ["Previous"]

        elif self.current_step == CreationStep.SUBCLASS:
            archetype = self.char_data["archetype_key"].lower()
            # Filter subclasses based on race restrictions
            all_subclasses = self.data.get_classes()[archetype]["sub_classes"]
            valid_subclasses = []
            race_key = self.char_data["race_key"].lower()
            subrace_key = self.char_data["sub_race_key"].lower()
            
            # Get race data to check for class limits
            race_data = self.data.get_races()[race_key]["sub_races"][subrace_key]
            class_limits = race_data.get("class_limits", [])

            for key, val in all_subclasses.items():
                # Check if class is allowed for this race
                allowed_races = val.get("allowed_races", [])
                
                # Check if race is specifically allowed (simple check for now)
                # The data has "human", "dwarf" etc. logic. 
                # We need to match race_key or subrace_key? 
                # Usually allowed_races lists the main race key.
                
                is_allowed = False
                if "all" in allowed_races:
                    is_allowed = True
                elif race_key in allowed_races:
                    is_allowed = True
                
                # Also check class_limits from race
                if key in class_limits:
                    is_allowed = False
                    
                if is_allowed:
                    valid_subclasses.append(key)
            
            self.options = [v.title() for v in valid_subclasses] + ["Previous"]
            if len(self.options) == 1: # Only Previous
                self.message = "No valid classes for this race! Go back."

        elif self.current_step == CreationStep.ROLL_STATS:
            self.options = ["Reroll", "Accept"]
            self._roll_stats()

        elif self.current_step == CreationStep.DISTRIBUTE_STATS:
            self.options = list(self.char_data["final_attributes"].keys()) + ["Done"]
            self.selected_index = 0

        elif self.current_step == CreationStep.SKILLS:
            self.options = ["Continue"] # Placeholder
            
        elif self.current_step == CreationStep.PORTRAIT:
            self.options = ["Portrait 1", "Portrait 2"] # Placeholder
            
        elif self.current_step == CreationStep.NAME:
            self.options = [] # Text input
            
        elif self.current_step == CreationStep.CONFIRM:
            self.options = ["Save Character", "Discard"]

    def _roll_stats(self):
        # 1. Base rolls (let's say 3d6 for now, or just random 1-20 as per doc?)
        # Doc says: "Attributes are based on a 1-20 point scale... race/subrace will determine the minimum base score."
        # "An additional roll that adds 1-6 points to the base score will be given after a class is selected."
        
        race_data = self.data.get_races()[self.char_data["race_key"].lower()]["sub_races"][self.char_data["sub_race_key"].lower()]
        base_mins = race_data.get("base_minimums", {})
        
        # Initialize with base mins
        self.char_data["base_attributes"] = base_mins.copy()
        
        # Add 1d6 to each? Doc says "An additional roll that adds 1-6 points to the base score will be given after a class is selected."
        # It implies this is added to the base minimums.
        
        for attr in self.char_data["base_attributes"]:
            roll = random.randint(1, 6)
            self.char_data["base_attributes"][attr] += roll
            
        # Calculate final attributes (Base + Modifiers)
        modifiers = race_data.get("stat_modifiers", {})
        self.char_data["final_attributes"] = {}
        for attr, val in self.char_data["base_attributes"].items():
            mod = modifiers.get(attr, 0)
            self.char_data["final_attributes"][attr] = val + mod

        # Bonus roll
        self.bonus_roll = random.randint(1, 10) # Arbitrary bonus points
        self.points_remaining = self.bonus_roll

    def _adjust_stat(self, amount):
        if self.selected_index >= len(self.char_data["final_attributes"]):
            return # "Done" selected
        
        attr_keys = list(self.char_data["final_attributes"].keys())
        attr = attr_keys[self.selected_index]
        
        if amount > 0 and self.points_remaining > 0:
            self.char_data["final_attributes"][attr] += 1
            self.points_remaining -= 1
        elif amount < 0:
            # Check if we can decrease (don't go below rolled value)
            # For simplicity, let's just allow decreasing back to base? 
            # We need to track original rolled values to prevent exploiting.
            # For now, just allow decreasing if > 0, but we need to track "points spent".
            # Let's just allow decreasing freely for now as long as we give back points, 
            # but ideally we should cap it at the rolled value.
            # Simplified: Just allow +/- for now.
            if self.char_data["final_attributes"][attr] > 0:
                 self.char_data["final_attributes"][attr] -= 1
                 self.points_remaining += 1

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = max(0, self.selected_index - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_index = min(len(self.options) - 1, self.selected_index + 1)
            elif event.key == pygame.K_RETURN:
                self._confirm_selection()
            elif event.key == pygame.K_RIGHT and self.current_step == CreationStep.DISTRIBUTE_STATS:
                self._adjust_stat(1)
            elif event.key == pygame.K_LEFT:
                if self.current_step == CreationStep.DISTRIBUTE_STATS:
                    self._adjust_stat(-1)
                elif self.current_step != CreationStep.GENDER and self.current_step != CreationStep.NAME:
                     self._go_back()
            elif event.key == pygame.K_BACKSPACE:
                if self.current_step == CreationStep.NAME:
                    self.char_data["name"] = self.char_data["name"][:-1]
            elif self.current_step == CreationStep.NAME:
                if event.unicode.isprintable():
                    self.char_data["name"] += event.unicode
            
            # Hotkeys
            if self.current_step == CreationStep.GENDER:
                if event.key == pygame.K_m:
                    self._select_option("Male")
                elif event.key == pygame.K_f:
                    self._select_option("Female")
                elif event.key == pygame.K_o:
                    self._select_option("Other")
            elif self.current_step == CreationStep.CLASS_ARCHETYPE:
                if event.key == pygame.K_m:
                    self._select_option("Melee")
                elif event.key == pygame.K_h:
                    self._select_option("Holy")
                elif event.key == pygame.K_a:
                    self._select_option("Arcane")
                elif event.key == pygame.K_s:
                    self._select_option("Stealth")

    def _select_option(self, option_text):
        for i, opt in enumerate(self.options):
            if opt == option_text:
                self.selected_index = i
                self._confirm_selection()
                break

    def _go_back(self):
        if self.current_step == CreationStep.RACE:
            self.current_step = CreationStep.GENDER
        elif self.current_step == CreationStep.SUBRACE:
            self.current_step = CreationStep.RACE
        elif self.current_step == CreationStep.CLASS_ARCHETYPE:
            self.current_step = CreationStep.SUBRACE
        elif self.current_step == CreationStep.SUBCLASS:
            self.current_step = CreationStep.CLASS_ARCHETYPE
        elif self.current_step == CreationStep.ROLL_STATS:
            self.current_step = CreationStep.SUBCLASS
        elif self.current_step == CreationStep.DISTRIBUTE_STATS:
            self.current_step = CreationStep.ROLL_STATS
        elif self.current_step == CreationStep.SKILLS:
            self.current_step = CreationStep.DISTRIBUTE_STATS
        elif self.current_step == CreationStep.PORTRAIT:
            self.current_step = CreationStep.SKILLS
        elif self.current_step == CreationStep.NAME:
            self.current_step = CreationStep.PORTRAIT
        elif self.current_step == CreationStep.CONFIRM:
            self.current_step = CreationStep.NAME
            
        self._init_step()

    def _confirm_selection(self):
        if self.options and self.options[self.selected_index] == "Previous":
            self._go_back()
            return

        if self.current_step == CreationStep.GENDER:
            self.char_data["sex"] = self.options[self.selected_index]
            self.current_step = CreationStep.RACE
            
        elif self.current_step == CreationStep.RACE:
            self.char_data["race_key"] = self.options[self.selected_index]
            self.current_step = CreationStep.SUBRACE
            
        elif self.current_step == CreationStep.SUBRACE:
            self.char_data["sub_race_key"] = self.options[self.selected_index]
            self.current_step = CreationStep.CLASS_ARCHETYPE
            
        elif self.current_step == CreationStep.CLASS_ARCHETYPE:
            self.char_data["archetype_key"] = self.options[self.selected_index]
            self.current_step = CreationStep.SUBCLASS

        elif self.current_step == CreationStep.SUBCLASS:
            if self.options:
                self.char_data["class_key"] = self.options[self.selected_index]
                self.current_step = CreationStep.ROLL_STATS
            else:
                # Go back if no options
                self.current_step = CreationStep.CLASS_ARCHETYPE
                
        elif self.current_step == CreationStep.ROLL_STATS:
            if self.options[self.selected_index] == "Reroll":
                self._roll_stats()
                return # Stay on this step
            else:
                self.current_step = CreationStep.DISTRIBUTE_STATS
        
        elif self.current_step == CreationStep.DISTRIBUTE_STATS:
            if self.options[self.selected_index] == "Done":
                self.current_step = CreationStep.SKILLS
                
        elif self.current_step == CreationStep.SKILLS:
            self.current_step = CreationStep.PORTRAIT
            
        elif self.current_step == CreationStep.PORTRAIT:
            # Placeholder for portrait selection
            self.current_step = CreationStep.NAME
            
        elif self.current_step == CreationStep.NAME:
            if len(self.char_data["name"]) > 0:
                self.current_step = CreationStep.CONFIRM
                
        elif self.current_step == CreationStep.CONFIRM:
            if self.options[self.selected_index] == "Save Character":
                self._save_character()
                from game_manager import GameState
                self.gm.change_state(GameState.MAIN_MENU)
            else:
                from game_manager import GameState
                self.gm.change_state(GameState.MAIN_MENU)

        self._init_step()

    def _save_character(self):
        save_dir = "saved_games"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # Load existing characters or create new list
        char_file = os.path.join(save_dir, "characters.json")
        characters = []
        if os.path.exists(char_file):
            try:
                with open(char_file, 'r') as f:
                    characters = json.load(f)
            except:
                pass
        
        # Calculate derived stats (HP)
        # HP Mod from race
        race_hp_mod = self.data.get_races()[self.char_data["race_key"]]["sub_races"][self.char_data["sub_race_key"]].get("hp_mod", 1.0)
        
        # Base HP Die from class archetype
        archetype_data = self.data.get_classes()[self.char_data["archetype_key"]]["archetype_data"]
        hp_die_str = archetype_data.get("base_hp_die", "d10")
        hp_die = int(hp_die_str[1:]) # "d10" -> 10
        
        # Roll HP (max at level 1 usually, but let's roll for now or take max)
        # Let's take max for level 1
        base_hp = hp_die 
        
        # Apply VIT mod (simple rule: VIT/2 or something? Doc doesn't specify formula, just "Primary modifier for HP")
        # Let's assume VIT is the HP for now or VIT + Die. 
        # Let's use a simple formula: HP = (Base Die + VIT_MOD) * Race_Mod
        # VIT 10 = 0 mod? Let's just use VIT value directly for now as per "VIT: Primary modifier".
        # Actually, let's just set max_hp = VIT + Base Die for now.
        
        vit = self.char_data["final_attributes"].get("VIT", 10)
        self.char_data["max_hp"] = int((base_hp + vit) * race_hp_mod)
        self.char_data["current_hp"] = self.char_data["max_hp"]

        characters.append(self.char_data)
        
        with open(char_file, 'w') as f:
            json.dump(characters, f, indent=2)
        print(f"Character {self.char_data['name']} saved!")

    def draw(self, screen, renderer):
        screen.fill((0, 0, 0))
        
        # Step Name Formatting
        step_name = self.current_step.name.replace("_", " ").title()
        renderer.draw_text(f"Character Creation - Step: {step_name}", 20, 20, "large")
        
        y = 80
        
        # Breadcrumb Navigation
        # Order: Gender, Race, Class
        # Format: Race / Subrace, Archetype / Class
        parts = []
        if self.char_data["sex"]:
            parts.append(self.char_data["sex"])
        
        if self.char_data["race_key"]:
            race_str = self.char_data["race_key"].title()
            if self.char_data["sub_race_key"]:
                race_str += f" / {self.char_data['sub_race_key'].title()}"
            parts.append(race_str)
            
        if self.char_data["archetype_key"]:
            class_str = self.char_data["archetype_key"].title()
            if self.char_data["class_key"]:
                class_str += f" / {self.char_data['class_key'].title()}"
            parts.append(class_str)
            
        summary = " | ".join(parts)
        if summary:
            renderer.draw_text(summary, 20, y, "small", "gray")
        y += 40

        if self.message:
            renderer.draw_text(self.message, 20, y, "medium", "red")
            y += 40

        # Draw Options
        if self.current_step == CreationStep.NAME:
            renderer.draw_text("Enter Name: " + self.char_data["name"] + "_", 20, y)
            renderer.draw_text("Press Enter to Confirm", 20, y + 40, "small", "gray")
            
        elif self.current_step == CreationStep.DISTRIBUTE_STATS:
            renderer.draw_text(f"Distribute Points (Remaining: {self.points_remaining})", 20, y, "medium", "yellow")
            y += 40
            renderer.draw_text("Use Left/Right arrows to adjust, Enter on Done", 20, y, "small", "gray")
            y += 30
            
            for i, option in enumerate(self.options):
                color = "green" if i == self.selected_index else "white"
                text = option
                if option != "Done":
                    val = self.char_data["final_attributes"][option]
                    text = f"{option}: {val}"
                
                renderer.draw_text(f"> {text}" if i == self.selected_index else f"  {text}", 20, y, "medium", color)
                y += 30

        elif self.current_step == CreationStep.ROLL_STATS:
            # Show stats
            stat_y = y
            renderer.draw_text("Attributes:", 300, stat_y, "medium", "yellow")
            stat_y += 30
            for attr, val in self.char_data["final_attributes"].items():
                renderer.draw_text(f"{attr}: {val}", 300, stat_y)
                stat_y += 25
            
            # Show options (Reroll/Accept)
            for i, option in enumerate(self.options):
                color = "green" if i == self.selected_index else "white"
                renderer.draw_text(f"> {option}" if i == self.selected_index else f"  {option}", 20, y, "medium", color)
                y += 30
                
        else:
            for i, option in enumerate(self.options):
                color = "green" if i == self.selected_index else "white"
                renderer.draw_text(f"> {option}" if i == self.selected_index else f"  {option}", 20, y, "medium", color)
                y += 30
