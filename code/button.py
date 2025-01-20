import pygame
from typing import Optional

class Button:
    def __init__(
        self,
        image: Optional[pygame.Surface],
        position: tuple[int, int],
        text_input: str,
        font: pygame.font.Font,
        base_color,
        hovering_color,
        antialias: bool
    ):
        self.image = image
        self.x_pos = position[0]
        self.y_pos = position[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.aa = antialias
        self.text_input = text_input
        self.text = self.font.render(self.text_input, self.aa, self.base_color)
        if self.image is None:
            self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        else:
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen: pygame.Surface):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_input(self, position: tuple[int, int]):
        isInVertical: bool = position[0] in range(self.rect.left, self.rect.right)
        isInHorizontal: bool = position[1] in range(self.rect.top, self.rect.bottom)
        return True if (isInVertical and isInHorizontal) else False

    def changeColor(self, position: tuple[int, int]):
        if self.check_input(position):
            self.text = self.font.render(self.text_input, self.aa, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, self.aa, self.base_color)
    
    