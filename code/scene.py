import pygame
import os
import random
from player import Player
from typing import List
from settings import GROUND_LEVEL, MAX_FRAME_RATE
from overlay import Overlay
from skeleton import Skeleton
from bird import Bird
from timer_counter import Timer
from utilities import construct_dir, get_font, load_high_score
from settings import COLOR_PALETTE

RESOURCE = construct_dir()[1]


class Scene:

    def __init__(self, score: int):
        self.screen: pygame.Surface = pygame.display.get_surface()
        self.all_sprites: pygame.sprite.Group = pygame.sprite.Group()
        self.skeletons: pygame.sprite.Group = pygame.sprite.Group()
        self.birds: pygame.sprite.Group = pygame.sprite.Group()
        self.enemy_spawn_timer: Timer = Timer(4000)
        self.max_enemies: int = 4
        self.score = 0
        self.high_score = load_high_score()
        self.backgrounds: List[pygame.Surface] = []
        self.background_positions: List[float] = []
        for i in range(4):
            bg_image = pygame.image.load(
                os.path.join(RESOURCE, "background", f"BG-{i}.png")
            ).convert_alpha()
            if i != 0:
                bg_image = pygame.transform.scale_by(bg_image, 0.5).convert_alpha()
            if i == 3:
                bg_image = pygame.transform.scale(bg_image, (1366, 768))

            self.backgrounds.append(bg_image)
            self.background_positions.append(0)
        self.background_width: int = self.backgrounds[0].get_width()
        self.setup()

    def setup(self) -> None:
        self.player = Player((300, GROUND_LEVEL), self.all_sprites)
        self.overlay: Overlay = Overlay(self.player)

    def draw_background(self) -> float:
        player_movement = self.player.direction.x * self.player.speed / MAX_FRAME_RATE
        if self.player.pos.x <= 300 or self.player.pos.x >= 1300:
            player_movement = 0

        scroll_speeds: List[float] = [0.1, 0.5, 0.8, 1]  # Farthest to closest layers

        for i, image in enumerate(self.backgrounds):
            self.background_positions[i] -= player_movement * scroll_speeds[i]

            if self.background_positions[i] <= -self.background_width:
                self.background_positions[i] += self.background_width
            elif self.background_positions[i] >= self.background_width:
                self.background_positions[i] -= self.background_width

            if i == 0:
                self.screen.blit(image, (self.background_positions[i], 0))
                self.screen.blit(
                    pygame.transform.flip(image, True, False),
                    (self.background_positions[i] + self.background_width, 0),
                )
            elif i != 3:
                self.screen.blit(image, (self.background_positions[i], 0))
                self.screen.blit(
                    image, (self.background_positions[i] + self.background_width, 0)
                )
            else:
                self.screen.blit(
                    image, (self.background_positions[i], GROUND_LEVEL + 30)
                )
                self.screen.blit(
                    image,
                    (
                        self.background_positions[i] + self.background_width,
                        GROUND_LEVEL + 30,
                    ),
                )
        return player_movement

    def spawn_enemy(self):
        if len(self.skeletons) < self.max_enemies:
            # Spawn enemy off-screen to the right
            spawn_x = random.randint(
                self.screen.get_width() + 50, self.screen.get_width() + 150
            )
            Skeleton((spawn_x, GROUND_LEVEL), 100, self.skeletons, self.player.pos)

        if len(self.birds) < 2:
            spawn_x = random.randint(
                self.screen.get_width() + 50, self.screen.get_width() + 150
            )
            Bird((spawn_x, GROUND_LEVEL - 100), 10, self.birds)
            print("bird")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.score += event.points

    def check_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score

    def display_score(self):
        font = pygame.font.Font(None, 36)
        score_text = get_font(50).render(f"Score:{self.score}", True, "White")
        high_score_text = get_font(50).render(
            f"High Score:{self.high_score}", True, COLOR_PALETTE[6]
        )
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 70))

    def update(
        self,
        player_position: pygame.math.Vector2,
        player_direction: str,
        delta_time: float,
        player: Player,
    ):
        # Update enemies
        for skeleton in self.skeletons:
            skeleton.update(player_position, player_direction, delta_time)
            skeleton.damage_player_if_close(player)

        for bird in self.birds:
            bird.update(self.player.state, delta_time)
            bird.damage_player_if_close(player)

        # Spawn new enemies if necessary
        self.enemy_spawn_timer.update()
        if not self.enemy_spawn_timer.active:
            self.enemy_spawn_timer.activate()
            self.spawn_enemy()

        # Draw everything
        self.skeletons.draw(self.screen)
        self.birds.draw(self.screen)

    def run(self, delta_time: float) -> None:
        # Background
        self.draw_background()
        # Adjust enemy position
        self.update(self.player.pos, self.player.state, delta_time, self.player)
        # Draw sprites on screen
        self.all_sprites.draw(self.screen)
        self.skeletons.draw(self.screen)
        # Update
        self.all_sprites.update(delta_time)
        # self.handle_events()
        self.check_high_score()
        self.display_score()
        self.overlay.display()
        # Handle attack
        if (
            self.player.timers["tool_use"].active
            or self.player.timers["weapon_use"].active
        ):
            self.player.deal_damage(self.skeletons)
            self.player.deal_damage(self.birds)
