import pygame

class UIRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.SysFont("Arial", 32)
        self.font_medium = pygame.font.SysFont("Arial", 24)
        self.font_small = pygame.font.SysFont("Arial", 18)
        self.colors = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "gray": (100, 100, 100),
            "light_gray": (200, 200, 200),
            "red": (255, 50, 50),
            "green": (50, 255, 50),
            "blue": (50, 50, 255),
            "yellow": (255, 255, 0)
        }

    def draw_text(self, text, x, y, font_size="medium", color="white", center=False):
        font = self.font_medium
        if font_size == "large":
            font = self.font_large
        elif font_size == "small":
            font = self.font_small
        
        text_surface = font.render(str(text), True, self.colors.get(color, self.colors["white"]))
        rect = text_surface.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        
        self.screen.blit(text_surface, rect)
        return rect

    def draw_button(self, text, rect, is_hovered=False, is_selected=False):
        color = self.colors["gray"]
        if is_selected:
            color = self.colors["green"]
        elif is_hovered:
            color = self.colors["light_gray"]
        
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, self.colors["white"], rect, 2) # Border
        
        self.draw_text(text, rect.centerx, rect.centery, color="black", center=True)
        return rect
