import pygame
import os
import random
from typing import List, Dict
from timer_counter import Timer
from settings import (
    GROUND_LEVEL, 
    JUMP_FORCE, 
    GRAVITY_ACCELERATION, 
    PlayerStates
)
from utilities import (
    RESOURCES_PATH,
    extract_frames_character,
    extract_frames_tool,
    get_current_direction,
    is_on_ground
)


class Player(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], group: pygame.sprite.Group):
        super().__init__(group)
        self.channel = pygame.mixer.Channel(1)
        self.channel.set_volume(1)
        # Set up resources
        player_sprite_path = os.path.join(RESOURCES_PATH, "player", "player.png")
        player_sprite_sheet = pygame.image.load(player_sprite_path).convert_alpha()

        self.frames: Dict[str, List[pygame.Surface]] = extract_frames_character(
            player_sprite_sheet, 32, 32, 5
        )
        if len(self.frames) < 4:
            raise Exception("Critical Error. Failed to extract sprite.")

        actions_sprite_path = os.path.join(RESOURCES_PATH, "player", "player_actions.png")
        action_sprite_sheet = pygame.image.load(actions_sprite_path).convert_alpha()
        self.action_frames: Dict[str, List[pygame.Surface]] = extract_frames_tool(
            action_sprite_sheet, 48, 48, 4.7
        )

        # Set up player
        self.state: str = PlayerStates.IDLE_RIGHT.value  # Default state
        self.current_frame: int = 0
        self.image: pygame.Surface = self.frames[self.state][self.current_frame]
        self.rect: pygame.Rect = self.image.get_rect(center=position)
        self.health: int = 100

        # Player movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.on_ground: bool = is_on_ground(self.pos.y)
        self.speed: int = 200
        self.last_update_time: int = pygame.time.get_ticks()
        self.gravity: float = 0

        # Player tools
        self.possible_tools: List[str] = list(
            {key.split("_")[0] for key in self.action_frames.keys()}
        )
        self.possible_tools.sort()
        self.tool_index: int = 0
        self.selected_tool: str = self.possible_tools[self.tool_index]
        self.tool_damage = {
            "pickaxe": 30,
            "axe": 40,
            "shovel": 30,
            "sword": 60
        }

        self.tool_range = {
            "pickaxe": 80,  
            "axe": 70,
            "shovel": 100,
            "sword": 50
        }

        self.tool_sound = {
            "pickaxe": pygame.mixer.Sound(os.path.join(RESOURCES_PATH, "audio", "axe.mp3")),
            "axe": pygame.mixer.Sound(os.path.join(RESOURCES_PATH, "audio", "axe.mp3")),
            "shovel": pygame.mixer.Sound(os.path.join(RESOURCES_PATH, "audio", "shovel.mp3")),
            "sword": pygame.mixer.Sound(os.path.join(RESOURCES_PATH, "audio", "sword.mp3"))
        }

        # Timer
        self.timers: Dict[str, Timer] = {
            "tool_use": Timer(1100),
            "weapon_use": Timer(500),
            "item_switch": Timer(1200),
            "weapon_switch": Timer(500),
            "shake_timer": Timer(300)
        }

        self.shake_offset = pygame.math.Vector2(0, 0)

    def animate(self, delta_time: float) -> None:
        """
        Animate player player based on delta_time.
        """
        isToolUsed = self.state.split("_")[0] in self.possible_tools

        number_of_sprites = (
            len(self.action_frames[self.state])
            if isToolUsed
            else len(self.frames[self.state])
        )

        # Accumulative fraction value
        self.current_frame += number_of_sprites * delta_time  # type: ignore
        if self.current_frame > number_of_sprites:
            self.current_frame = 0
        try:
            if isToolUsed:
                self.image = self.action_frames[self.state][int(self.current_frame)]
            else:
                self.image = self.frames[self.state][int(self.current_frame)]
            # Account for the differences in surface size
            self.rect = self.image.get_rect(center=self.rect.center)
        except IndexError:
            print(f"Frame missed: {self.current_frame}\nPlayer state: {self.state}")
        except KeyError:
            print(f"Critical error. No frame found. Missing: {self.state}")

    def change_status(self) -> None:
        """
        Match player current status with the next status.
        """

        # Movement
        if self.direction.x == 0 and self.direction.y == 0 and is_on_ground(self.pos.y):
            # Check last status
            idle_mapping = {
                PlayerStates.JUMP_RIGHT.value: PlayerStates.IDLE_RIGHT.value,
                PlayerStates.JUMP_LEFT.value: PlayerStates.IDLE_LEFT.value,
                PlayerStates.MOVE_RIGHT.value: PlayerStates.IDLE_RIGHT.value,
                PlayerStates.MOVE_LEFT.value: PlayerStates.IDLE_LEFT.value
            }
            self.state = idle_mapping.get(self.state, self.state)

        current_item = self.state.split("_")[0]
        current_direction = get_current_direction(self.state)
        if self.timers["tool_use"].active:
            self.state = "_".join([self.selected_tool, current_direction])
        elif self.timers["weapon_use"].active:
            self.state = "_".join([current_item, current_direction])
        else:
            # Change the player status to idle to prevent unlimited action duration
            if current_item in self.possible_tools or current_item in "sword":
                self.state = "_".join(["idle", current_direction])

    def input_handler(self):
        """
        Handle player input.
        """
        keys = pygame.key.get_pressed()

        if not self.timers["tool_use"].active and not self.timers["weapon_use"].active:
            self.handle_movement(keys)
            self.handle_tool_switch(keys)

        self.handle_weapon_use(keys)
        self.handle_tool_use(keys)

    def handle_movement(self, keys: pygame.key.ScancodeWrapper):
        # on_ground: bool = is_on_ground(self.pos.y)
        if keys[pygame.K_SPACE] and self.on_ground:
            self.gravity = JUMP_FORCE
            if self.state == PlayerStates.MOVE_LEFT.value or self.state == PlayerStates.IDLE_LEFT.value:
                self.state = PlayerStates.JUMP_LEFT.value
            elif self.state == PlayerStates.MOVE_RIGHT.value or self.state == PlayerStates.IDLE_RIGHT.value:
                self.state = PlayerStates.JUMP_RIGHT.value

        # Horizontal
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.state = PlayerStates.MOVE_LEFT.value if self.on_ground else PlayerStates.JUMP_LEFT.value
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.state = PlayerStates.MOVE_RIGHT.value if self.on_ground else PlayerStates.JUMP_RIGHT.value
        else:
            self.direction.x = 0

    def handle_tool_use(self, keys):
        # Tool use
        if keys[pygame.K_f] and not self.timers["tool_use"].active:
            self.timers["tool_use"].activate()
            self.channel.play(self.tool_sound[self.selected_tool])
            if self.on_ground:
                self.direction = pygame.math.Vector2()
            self.current_frame = 0

    def handle_tool_switch(self, keys):
        """
        Handle the use of tool. Player cannot move when use tool.
        """
        # Change tool
        tool_keys = [
            pygame.K_1,
            pygame.K_2,
            pygame.K_3,
        ]

        for key in tool_keys:
            if keys[key]:
                self.tool_index = tool_keys.index(key)
                self.selected_tool = self.possible_tools[self.tool_index]
                break

    def handle_weapon_use(self, keys):
        """
        Handle the use of sword. Player cannot move when use sword.
        """
        if keys[pygame.K_r] and not self.timers["weapon_use"].active:
            self.timers["weapon_use"].activate()
            self.channel.play(self.tool_sound["sword"])
            self.state = "_".join(["sword", get_current_direction(self.state)])
            if self.on_ground:
                self.direction = pygame.math.Vector2()
            self.current_frame = 0

    def position_calculator(self, delta_time: float):
        self.on_ground = is_on_ground(self.pos.y)
        # Normalize the direction vector to ensure consistent speed
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        self.gravity += GRAVITY_ACCELERATION * delta_time
        self.pos.y += self.gravity
        if self.pos.y >= GROUND_LEVEL:
            self.pos.y = GROUND_LEVEL

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * delta_time
        if self.pos.x < 60:
            self.pos.x = 60
        if self.pos.x > 1300:
            self.pos.x = 1300
        self.rect.centerx = round(self.pos.x) # type: ignore
        
        # vertical movement
        self.rect.centery = round(self.pos.y) # type: ignore 
        self.rect.centerx += round(self.shake_offset.x)
        self.rect.centery += round(self.shake_offset.y)
        # print(self.pos.x)
        # print("pos_y:" + str(self.pos.y))
        # print("rect_y:" + str(self.rect.centery))
        # print("gravity:" + str(self.gravity))

    def deal_damage(self, enemies: pygame.sprite.Group):
        if self.state.split("_")[0] == "sword":
            current_tool = "sword"
        else:
            current_tool = self.selected_tool
        # print(current_tool)
        damage: int = self.tool_damage.get(current_tool, 0)
        weapon_range: int = self.tool_range.get(current_tool, 0)
        for enemy in enemies:
            distance = pygame.math.Vector2(self.rect.center).distance_to(enemy.rect.center)
            if distance <= weapon_range:
                pygame.mixer.Channel(2).play(pygame.mixer.Sound(os.path.join(RESOURCES_PATH, "audio", "hit.mp3")))

                enemy.take_damage(damage)

    def apply_shake(self):
        if self.timers["shake_timer"].active:
            self.shake_offset.x = random.randint(-5, 5)  # Random x offset
            self.shake_offset.y = random.randint(-5, 5)  # Random y offset
        else:
            self.shake_offset.x = 0
            self.shake_offset.y = 0

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, delta_time: float):
        """
        Main game update method. Called every frame to update the player.
        """
        self.input_handler()
        self.position_calculator(delta_time)
        self.change_status()
        self.apply_shake()
        self.update_timers()
        self.animate(delta_time)
