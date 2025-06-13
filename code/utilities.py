import os
import sys
from typing import Dict, List

import pygame
from settings import GROUND_LEVEL


def _get_base_paths():
    """Determines the correct base and resource paths based on frozen status."""
    if getattr(sys, 'frozen', False):
        # We are running inside a PyInstaller bundle
        # sys._MEIPASS is the path to the temporary folder where PyInstaller extracted everything
        bundle_root = sys._MEIPASS
        # We configured PyInstaller with --add-data "resources:resources"
        # so the resources folder is directly under the bundle_root
        resource_dir = os.path.join(bundle_root, "resources")
        return bundle_root, resource_dir
    else:
        # We are running in a normal Python environment (e.g., from terminal)
        # Navigate up two levels from code/utilities.py to get to the project root
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        resource_dir = os.path.join(base_dir, "resources")
        return base_dir, resource_dir


BASE_GAME_PATH, RESOURCES_PATH = _get_base_paths()


def get_font(size: int) -> pygame.font.Font:
    return pygame.font.Font(
        os.path.join(RESOURCES_PATH, "fonts", "VCR_OSD_MONO_1.ttf"), size
    )


def flip_helper_vertical(
    frames: List[pygame.Surface], range: tuple[int, int]
) -> List[pygame.Surface]:
    return [
        pygame.transform.flip(frame, True, False)
        for frame in frames[range[0]: range[1]]
    ]


def extract_frames(
    sprite_sheet: pygame.Surface,
    frame_width: int,
    frame_height: int,
    resize_factor: float = 1,
) -> List[pygame.Surface]:
    sheet_width, sheet_height = sprite_sheet.get_size()
    frames: List[pygame.Surface] = []
    temp = sheet_width // frame_width
    for row in range(sheet_height // frame_height):
        for col in range(sheet_width // frame_width):
            x = col * frame_width
            y = row * frame_height
            frame = sprite_sheet.subsurface(
                pygame.Rect(x, y, frame_width, frame_height)
            )
            if resize_factor > 1:
                frame = pygame.transform.scale_by(frame, resize_factor)
            frames.append(frame)
    return frames


def get_high_score_path():
    if getattr(sys, "frozen", False):
        return os.path.join(os.path.dirname(sys.executable))
    else:
        return os.path.join(construct_dir()[1], "high_score.txt")


def load_high_score():
    high_score_file = os.path.join(construct_dir()[1], "high_score.txt")
    if getattr(sys, 'frozen', False):
        high_score_file = os.path.join(os.path.dirname(sys.executable), "high_score.txt")
    else:
        high_score_file = os.path.join(RESOURCES_PATH, "high_score.txt")

    if os.path.exists(high_score_file):
        with open(high_score_file, "r") as file:
            try:
                return int(file.read().strip())
            except ValueError:
                return 0
    return 0


def save_high_score(high_score):
    if getattr(sys, 'frozen', False):
        high_score_file = os.path.join(os.path.dirname(sys.executable), "high_score.txt")
    else:
        high_score_file = os.path.join(RESOURCES_PATH, "high_score.txt")
    with open(high_score_file, "w") as file:
        file.write(str(high_score))


def construct_dir() -> List[str]:
    """
    Return the absolute path of:
    - code
    - resources

    Return value: List[base_dir, resource_dir]
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    resource_dir = os.path.join(base_dir, "resources")
    return [base_dir, resource_dir]


def extract_frames_character(
    sprite_sheet: pygame.Surface,
    frame_width: int,
    frame_height: int,
    resize_factor: float = 1,
) -> Dict[str, List[pygame.Surface]]:
    """
    This function will extract the individual sprite from an asset of multiple sprites.
    """
    frames: List[pygame.Surface] = extract_frames(
        sprite_sheet, frame_width, frame_height, resize_factor
    )
    jump = pygame.image.load(os.path.join(RESOURCES_PATH, "player", "jump.png"))
    jump = pygame.transform.scale_by(jump, resize_factor)
    animation_frames: Dict[str, List[pygame.Surface]] = {
        "idle_right": frames[6:12],
        "idle_left": flip_helper_vertical(frames, (6, 12)),
        "move_right": frames[24:30],
        "move_left": flip_helper_vertical(frames, (24, 30)),
        "sword_right": frames[42:46],
        "sword_left": flip_helper_vertical(frames, (42, 46)),
        "jump_right": [jump] * 6,
        "jump_left": flip_helper_vertical([jump] * 6, (0, 5)),
        "fall_down_right": frames[54:58],
        "fall_down_left": flip_helper_vertical(frames, (54, 58)),
    }

    return animation_frames


def extract_frames_skeleton(
    sprite_sheet: pygame.Surface,
    frame_width: int,
    frame_height: int,
    resize_factor: float = 1,
) -> Dict[str, List[pygame.Surface]]:
    """
    This function will extract the individual sprite from an asset of multiple sprites.
    """
    frames: List[pygame.Surface] = extract_frames(
        sprite_sheet, frame_width, frame_height, resize_factor
    )
    jump = pygame.image.load(os.path.join(RESOURCES_PATH, "player", "jump.png"))
    jump = pygame.transform.scale_by(jump, resize_factor)
    animation_frames: Dict[str, List[pygame.Surface]] = {
        "idle_right": frames[6:12],
        "idle_left": flip_helper_vertical(frames, (6, 12)),
        "move_right": frames[24:30],
        "move_left": flip_helper_vertical(frames, (24, 30)),
        "death_right": frames[36:40],
        "death_left": flip_helper_vertical(frames, (36, 42)),
        "hit_right": frames[48:52],
        "hit_left": flip_helper_vertical(frames, (48, 52)),
    }

    return animation_frames


def get_current_direction(status: str) -> str:
    """
    This function return the current direction of a character:
    up, down, left, right.
    """
    return status.split("_")[1]


def extract_frames_tool(
    sprite_sheet: pygame.Surface,
    frame_width: int,
    frame_height: int,
    resize_factor: float = 1,
) -> Dict[str, List[pygame.Surface]]:
    """
    This function will extract the individual sprite from an asset of multiple sprites.
    """
    frames: List[pygame.Surface] = extract_frames(
        sprite_sheet, frame_width, frame_height, resize_factor
    )

    animation_frames: Dict[str, List[pygame.Surface]] = {
        "pickaxe_right": frames[0:6],
        "pickaxe_left": flip_helper_vertical(frames, (0, 6)),
        "axe_right": frames[18:24],
        "axe_left": flip_helper_vertical(frames, (18, 24)),
        "shovel_right": frames[36:42],
        "shovel_left": flip_helper_vertical(frames, (36, 42)),
    }

    return animation_frames


def extract_overlay_tool(
    frame_width: int,
    frame_height: int,
    resize_factor: float = 1,
) -> Dict[str, pygame.Surface]:
    """
    This function will extract the individual sprite from an asset of multiple sprites.
    """
    overlay_sprite_path = os.path.join(RESOURCES_PATH, "overlay", "tools.png")
    overlay_sprite_sheet = pygame.image.load(
        overlay_sprite_path).convert_alpha()
    tool_frames: List[pygame.Surface] = extract_frames(
        overlay_sprite_sheet, frame_width, frame_height, resize_factor
    )
    health_frame_path = os.path.join(RESOURCES_PATH, "overlay", "health.png")
    overlay_sprite_sheet = pygame.image.load(health_frame_path).convert_alpha()
    health_frames: List[pygame.Surface] = extract_frames(
        overlay_sprite_sheet, 32, 32, 4
    )

    overlay_surfaces: Dict[str, pygame.Surface] = {
        "pickaxe": tool_frames[2],
        "axe": tool_frames[3],
        "sword": tool_frames[4],
        "shovel": tool_frames[5],
        "health": health_frames[2],
    }
    return overlay_surfaces


def is_on_ground(y: float) -> bool:
    return abs(y - GROUND_LEVEL) < 1e-3

