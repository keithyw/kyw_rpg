from enum import Enum, auto

class GameState(Enum):
    MAIN_MENU = auto()
    CHARACTER_CREATION = auto()
    GAMEPLAY = auto()
    # Add other states as needed

class GameManager:
    def __init__(self):
        self.current_state = GameState.MAIN_MENU
        self.running = True
        self.data_loader = None
        self.screen_width = 1024
        self.screen_height = 768
        self.fps = 60

    def set_data_loader(self, data_loader):
        self.data_loader = data_loader

    def change_state(self, new_state: GameState):
        self.current_state = new_state
        print(f"State changed to: {self.current_state}")

    def quit_game(self):
        self.running = False
