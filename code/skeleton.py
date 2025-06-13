import pygame
import os
import random
from settings import GROUND_LEVEL
from timer_counter import Timer
from player import Player
from typing import Dict, List, Optional
from utilities import RESOURCES_PATH, extract_frames_skeleton, get_current_direction
from settings import EnemyStates


class Skeleton(pygame.sprite.Sprite):
    def __init__(
        self,
        position: tuple[int, int],
        health: int,
        group: pygame.sprite.Group,
        player_position: pygame.math.Vector2,
        speed: Optional[float] = None,
    ):
        super().__init__(group)
        enemy_sprite_path = os.path.join(RESOURCES_PATH, "enemies", "skeleton.png")
        enemy_sprite_sheet = pygame.image.load(enemy_sprite_path)
        self.frames: Dict[str, List[pygame.Surface]] = extract_frames_skeleton(
            enemy_sprite_sheet, 32, 32, 5
        )

        self.channel = pygame.mixer.Channel(3)
        self.state: str = EnemyStates.MOVE_LEFT.value
        self.current_direction: str = get_current_direction(self.state)
        self.current_frame = 0
        self.image: pygame.Surface = self.frames[self.state][self.current_frame]
        self.rect: pygame.Rect = self.image.get_rect(center=position)
        self.possible_speed = [50, 70, 100, 150]
        self.speed: float = (
            speed
            if speed is not None
            else self.possible_speed[round(random.uniform(0, 3))]
        )
        self.world_position = pygame.math.Vector2(position)
        self.player_position = player_position

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
        number_of_sprites = len(self.frames[self.state])

        # Accumulative fraction value
        self.current_frame += number_of_sprites * delta_time  # type: ignore
        if self.current_frame > number_of_sprites:
            self.current_frame = 0
        try:
            self.image = self.frames[self.state][int(self.current_frame)]
            # Account for the differences in surface size
            self.rect = self.image.get_rect(center=self.rect.center)
        except IndexError:
            print(f"Frame missed: {self.current_frame}\nPlayer state: {self.state}")
        except KeyError:
            print(f"Critical error. No frame found. Missing: {self.state}")

    def change_status(self, player_position: pygame.math.Vector2) -> None:
        if not self.timers["hit_timer"].active:
            if player_position.x < self.world_position.x:
                self.current_direction = "left"
            else:
                self.current_direction = "right"
            self.state = f"move_{self.current_direction}"

    def damage_player_if_close(self, player: Player):
        distance = pygame.math.Vector2(self.rect.center).distance_to(player.rect.center)
        if distance < 20: 
            if not self.timers["damage_timer"].active and not self.timers["hit_timer"].active:
                self.channel.set_volume(0.5)
                self.channel.play(pygame.mixer.Sound(os.path.join(RESOURCES_PATH, "audio", "hurt.mp3")))
                player.health -= 20
                player.timers["shake_timer"].activate()
                self.timers["damage_timer"].activate()
                
    def take_damage(self, amount: int):
        if self.timers["death_timer"].active:
            return
        if not self.timers["hit_timer"].active:
            print("take damage")
            self.health -= amount
            print(self.health)
            self.state = EnemyStates.HIT_RIGHT.value
            self.timers["hit_timer"].activate()
        if self.health <= 0 and not self.timers["death_timer"].active:
            self.timers["death_timer"].activate()
            direction = get_current_direction(self.state)
            self.state = f"death_{direction}"

    def position_calculator(
        self,
        delta_time: float,
        player_position: pygame.math.Vector2,
        player_state: str,
    ):
        # Calculate direction vector toward the player
        direction_vector = pygame.math.Vector2(player_position) - self.world_position

        distance_to_player = direction_vector.length()
        if distance_to_player < 20:
            return
        # Normalize the vector to ensure consistent movement speed
        if direction_vector.length() != 0:
            direction_vector = direction_vector.normalize()

        speed_multiplier = 0.5 if get_current_direction(player_state) == "left" else 1.0

        # Move the enemy
        if not self.timers["hit_timer"].active or not self.timers["death_timer"].active:
            self.world_position.x += (
                direction_vector.x * self.speed * delta_time * speed_multiplier
            )
            self.rect.center = self.world_position  # type: ignore

    def die(self) -> None:
        self.kill()
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"points": 10}))

    def update_timer(self) -> None:
        for timer in self.timers.values():
            timer.update()

    def update(
        self, player_movement: pygame.math.Vector2, player_state: str, delta_time: float
    ):
        # self.rect.x -= round(player_movement)
        self.position_calculator(
            delta_time, self.player_position, player_state
        )
        self.animate(delta_time)
        self.change_status(player_movement)
        self.update_timer()

        if (
            not self.timers["death_timer"].active
            and self.state.split("_")[0] == "death"
        ):
            self.die()
