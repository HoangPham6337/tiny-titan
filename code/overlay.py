import pygame
import os
from typing import (
    Dict
)
from utilities import (
    construct_dir,
    extract_overlay_tool,
    get_font
)
from settings import (
    OVERLAY_POSITIONS,
)
from player import Player

class Overlay:
    def __init__(self, player: Player):
        self.display_surface: pygame.Surface = pygame.display.get_surface()
        self.overlay_item_surf = extract_overlay_tool(16, 16, 6)

        self.player = player

    def display(self) -> None:
        tool_surf = self.overlay_item_surf[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(center=OVERLAY_POSITIONS["tool"])
        health_surf = self.overlay_item_surf["health"]
        health_rect = health_surf.get_rect(center=OVERLAY_POSITIONS["health"])
        menu_text = get_font(50).render(str(self.player.health), False, "White")
        menu_rect = menu_text.get_rect(center=OVERLAY_POSITIONS["health_num"])
        self.display_surface.blit(tool_surf, tool_rect)
        self.display_surface.blit(health_surf, health_rect)
        self.display_surface.blit(menu_text, menu_rect)