import json
import os
from typing import Dict, Any

class DataLoader:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.races = {}
        self.classes = {}
        self.core_attributes = {}
        self.spell_schools = {}
        self.combat_skills = {}
        self.noncombat_skills = {}
        self.damage_types = {}
        self.gear_slots = {}
        self.gear_properties = {}
        self.character_schema = {}

    def load_all_data(self):
        self.races = self._load_json("races.json")
        self.classes = self._load_json("classes.json")
        self.core_attributes = self._load_json("core_attributes.json")
        self.spell_schools = self._load_json("spell_schools.json")
        self.combat_skills = self._load_json("combat_skills.json")
        self.noncombat_skills = self._load_json("noncombat_skills.json")
        self.damage_types = self._load_json("damage_types.json")
        self.gear_slots = self._load_json("gear_slots.json")
        self.gear_properties = self._load_json("gear_properties.json")
        self.character_schema = self._load_json("character_schema.json")
        print("All data loaded successfully.")

    def _load_json(self, filename: str) -> Dict[str, Any]:
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: File {filename} not found in {self.data_dir}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode {filename}: {e}")
            return {}

    def get_races(self):
        return self.races

    def get_classes(self):
        return self.classes
    
    def get_core_attributes(self):
        return self.core_attributes

    def get_flat_subclasses(self) -> Dict[str, Any]:
        """Returns a flat dictionary of all subclasses keyed by their ID."""
        flat_subclasses = {}
        for archetype, data in self.classes.items():
            if "sub_classes" in data:
                for sub_key, sub_data in data["sub_classes"].items():
                    # Inject archetype info if needed, or just return the sub_data
                    sub_data["archetype"] = archetype
                    flat_subclasses[sub_key] = sub_data
        return flat_subclasses
