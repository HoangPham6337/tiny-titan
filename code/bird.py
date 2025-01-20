import pygame
import os
import random
from settings import GROUND_LEVEL
from timer_counter import Timer
from player import Player
from typing import Dict, List, Optional
from utilities import construct_dir, get_current_direction, extract_frames
from settings import EnemyStates


RESOURCES = construct_dir()[1]


class Bird(pygame.sprite.Sprite):
    def __init__(
        self,
        position: tuple[int, int],
        health: int,
        group: pygame.sprite.Group,
        speed: Optional[float] = None,
    ):
        super().__init__(group)
        enemy_sprite_path = os.path.join(RESOURCES, "enemies", "bird.png")
        enemy_sprite_sheet = pygame.image.load(enemy_sprite_path)
        self.frames: List[pygame.Surface] = extract_frames(enemy_sprite_sheet, 68, 68, 3)

        self.channel = pygame.mixer.Channel(4)
        self.state: str = EnemyStates.MOVE_LEFT.value
        self.current_frame = 0
        self.image: pygame.Surface = self.frames[self.current_frame]
        self.rect: pygame.Rect = self.image.get_rect(center=position)
        self.possible_speed = [90, 110, 130, 170]
        self.speed: float = (
            speed
            if speed is not None
            else self.possible_speed[round(random.uniform(0, 3))]
        )
        self.world_position = pygame.math.Vector2(position)
        self.health: int = health
        self.timers = {
            "hit_timer": Timer(1300),
            "death_timer": Timer(900),
            "damage_timer": Timer(1200)
        }

    def animate(self, delta_time: float) -> None:
        """
        Animate player player based on delta_time.
        """
        number_of_sprites = len(self.frames)

        # Accumulative fraction value
        self.current_frame += number_of_sprites * delta_time  # type: ignore
        if self.current_frame > number_of_sprites:
            self.current_frame = 0
        try:
            self.image = self.frames[int(self.current_frame)]
            # Account for the differences in surface size
            self.rect = self.image.get_rect(center=self.rect.center)
        except IndexError:
            print(f"Frame missed: {self.current_frame}\nPlayer state: {self.state}")
        except KeyError:
            print(f"Critical error. No frame found. Missing: {self.state}")

    def change_status(self) -> None:
        if not self.timers["hit_timer"].active:
            self.state = f"move_left"
        if self.world_position.x < -10:
            self.state = "death_left"
        if self.health <= 0:
            direction = get_current_direction(self.state)
            self.state = f"death_{direction}"

    def damage_player_if_close(self, player: Player):
        distance = pygame.math.Vector2(self.rect.center).distance_to(player.rect.center)
        if distance < 40: 
            if not self.timers["damage_timer"].active and not self.timers["hit_timer"].active:
                player.health -= 5
                player.timers["shake_timer"].activate()
                self.timers["damage_timer"].activate()
                self.channel.set_volume(0.5)
                self.channel.play(pygame.mixer.Sound(os.path.join(RESOURCES, "audio", "hurt.mp3")))
                
    def take_damage(self, amount: int):
        if self.timers["death_timer"].active:
            return
        if not self.timers["hit_timer"].active:
            self.health -= amount
            self.state = EnemyStates.HIT_RIGHT.value
            self.timers["hit_timer"].activate()

    def position_calculator(
        self,
        delta_time: float,
        player_state: str,
    ):

        speed_multiplier = 0.5 if get_current_direction(player_state) == "left" else 1.0

        # Move the enemy
        self.world_position.x -= (self.speed * delta_time * speed_multiplier)
        self.rect.center = self.world_position  # type: ignore

    def die(self) -> None:
        self.kill()
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"points": 5}))

    def update_timer(self) -> None:
        for timer in self.timers.values():
            timer.update()

    def update(
        self, player_state: str, delta_time: float
    ):
        
        self.position_calculator(delta_time, player_state)
        self.animate(delta_time)
        self.change_status()
        self.update_timer()

        if self.state.split("_")[0] == "death":
            self.die()
