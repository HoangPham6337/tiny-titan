import pygame
import os
import sys
from button import Button
from settings import CENTER_SCREEN, COLOR_PALETTE, MAX_FRAME_RATE, WINDOW_HEIGHT
from utilities import get_font, load_high_score, save_high_score, RESOURCES_PATH
from scene import Scene
from player import Player

button_background: pygame.Surface = pygame.image.load(
os.path.join(RESOURCES_PATH, "button", "button_background.png")
)
button_background = pygame.transform.scale_by(button_background, 0.4)

def play(screen: pygame.Surface, background: pygame.Surface, score: int) -> None:
    clock = pygame.time.Clock()
    scene = Scene(score)
    while True:
        delta_time = clock.tick(MAX_FRAME_RATE) / 1000
        mouse_pos = pygame.mouse.get_pos()
        pygame.display.set_caption("Tiny Titan")
        screen.fill("black")


        scene.run(delta_time)
        button_background: pygame.Surface = pygame.image.load(
            os.path.join(RESOURCES_PATH, "button", "button_background.png")
        )
        button_background = pygame.transform.scale_by(button_background, 0.2)
        play_back = Button(
            button_background, (1285, 50), "BACK", get_font(40), "White", "Red", False
        )
        play_back.changeColor(mouse_pos)
        play_back.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_back.check_input(mouse_pos):
                    save_high_score(scene.high_score)
                    main_menu(screen, background, scene.score)
            if event.type == pygame.USEREVENT:
                scene.score += event.points
        if scene.player.health <= 0:
            save_high_score(scene.high_score)
            main_menu(screen, background, scene.score)
        pygame.display.update()


def main_menu(screen: pygame.Surface, background: pygame.Surface, score: int) -> None:
    high_score = load_high_score()
    high_score = max(high_score, score)  # Update high score if the current score is higher
    while True:
        pygame.display.set_caption("Tiny Titan")
        screen.blit(background, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        menu_font = pygame.font.Font(
            os.path.join(RESOURCES_PATH, "fonts", "gumball.ttf"), 100
        )
        menu_text = menu_font.render("TINY TITAN", False, COLOR_PALETTE[5])
        menu_rect = menu_text.get_rect(center=(CENTER_SCREEN[0], 100))
        
        score_text = get_font(50).render(f"High Score: {high_score}", False, COLOR_PALETTE[4])
        score_rect = score_text.get_rect(center=(CENTER_SCREEN[0], 200))


        play_button = Button(
            button_background,
            (683, 350),
            "PLAY",
            get_font(75),
            "White",
            COLOR_PALETTE[4],
            False,
        )

        quit_button = Button(
            button_background,
            (683, 520),
            "QUIT",
            get_font(75),
            "White",
            COLOR_PALETTE[4],
            False,
        )

        screen.blit(menu_text, menu_rect)
        screen.blit(score_text, score_rect)

        for button in [play_button, quit_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_input(mouse_pos):
                    play(screen, background, score)
                if quit_button.check_input(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
