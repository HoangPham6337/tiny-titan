import pygame
import os
from settings import WINDOW_WIDTH, WINDOW_HEIGHT
from ui import main_menu
from utilities import RESOURCES_PATH

pygame.init()
screen: pygame.Surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_background: pygame.Surface = pygame.image.load(
    os.path.join(RESOURCES_PATH, "background", "background_misty_rocks.png")
)
icon = pygame.transform.scale2x(
    pygame.image.load(os.path.join(RESOURCES_PATH, "icon", "title.png"))
)
pygame.display.set_icon(icon)
bg_music = pygame.mixer.Sound(
    os.path.join(RESOURCES_PATH, "audio", "alexander-nakarada-chase.mp3")
)
pygame.mixer.set_reserved(1)
bg_channel = pygame.mixer.Channel(0)
bg_channel.set_volume(0.1)
bg_channel.play(bg_music, loops=-1)
main_menu(screen, game_background, 0)
