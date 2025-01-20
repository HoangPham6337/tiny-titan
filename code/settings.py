from enum import Enum
import os

MAX_FRAME_RATE = 60
WINDOW_WIDTH: int = 1366
WINDOW_HEIGHT: int = 768
GROUND_LEVEL: int = 500
OVERLAY_POSITIONS = {
    "tool": (60, WINDOW_HEIGHT - 60),
    "health_num": (WINDOW_WIDTH - 162, WINDOW_HEIGHT - 60),
    "health": (WINDOW_WIDTH - 60, WINDOW_HEIGHT - 60)
}
JUMP_FORCE = -8
GRAVITY_ACCELERATION = 15
CENTER_SCREEN: tuple[int, int] = (683, 384)
COLOR_PALETTE: tuple[str, str, str, str, str, str, str, str] = (
    "#91A281",
    "#5A201D",
    "#451315",
    "#A5B48F",
    "#A1654A",
    "#FECE74",  # Light Yellow
    "#FFDE00",  # Yellow
    "#D2001A",  # Red
)


class PlayerStates(Enum):
    IDLE_RIGHT = "idle_right"
    IDLE_LEFT = "idle_left"
    JUMP_RIGHT = "jump_right"
    JUMP_LEFT = "jump_left"
    MOVE_RIGHT = "move_right"
    MOVE_LEFT = "move_left"
    PICKAXE_RIGHT = "pickaxe_right"
    PICKAXE_LEFT = "pickaxe_left"
    AXE_RIGHT = "axe_right"
    AXE_LEFT = "axe_left"
    SHOVEL_RIGHT = "shovel_right"
    SHOVEL_LEFT = "shovel_left"
    SWORD_RIGHT = "sword_right"
    SWORD_LEFT = "sword_left"

class EnemyStates(Enum):
    MOVE_RIGHT = "move_right"
    MOVE_LEFT = "move_left"
    ATTACK_RIGHT = "attack_right"
    ATTACK_LEFT = "attack_left"
    HIT_RIGHT = "hit_right"
    HIT_LEFT = "hit_left"
    DEATH_RIGHT = "death_right"
    DEATH_LEFT = "death_left"
