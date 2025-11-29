import pygame
import sys
from game_manager import GameManager, GameState
from data_loader import DataLoader
from rendering.ui_renderer import UIRenderer
from character_creation import CharacterCreator

def main():
    pygame.init()
    
    # Setup Window
    screen_width = 1024
    screen_height = 768
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Classic CRPG")
    clock = pygame.time.Clock()
    
    # Initialize Systems
    data_loader = DataLoader()
    data_loader.load_all_data()
    
    game_manager = GameManager()
    game_manager.set_data_loader(data_loader)
    
    renderer = UIRenderer(screen)
    
    # Character Creator instance
    char_creator = None

    # Main Loop
    while game_manager.running:
        # Event Handling
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_manager.quit_game()
            
            # Pass events to active controller
            if game_manager.current_state == GameState.MAIN_MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        game_manager.change_state(GameState.CHARACTER_CREATION)
                        char_creator = CharacterCreator(game_manager) # Reset/Init creator
                    elif event.key == pygame.K_q:
                        game_manager.quit_game()
                        
            elif game_manager.current_state == GameState.CHARACTER_CREATION:
                if char_creator:
                    char_creator.handle_input(event)

        # Rendering
        screen.fill((0, 0, 0))
        
        if game_manager.current_state == GameState.MAIN_MENU:
            renderer.draw_text("Classic CRPG Title Screen", screen_width//2, 100, "large", "yellow", center=True)
            renderer.draw_text("(C)reate Character", screen_width//2, 300, "medium", "white", center=True)
            renderer.draw_text("(Q)uit", screen_width//2, 350, "medium", "white", center=True)
            
        elif game_manager.current_state == GameState.CHARACTER_CREATION:
            if char_creator:
                char_creator.draw(screen, renderer)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()