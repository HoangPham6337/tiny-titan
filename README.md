# Tiny Titan

Tiny Titan is a side-scrolling action game where players control a hero battling waves of enemies while striving to achieve the highest score. The game features a dynamic environment, various tools, and challenging enemies.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Controls](#controls)
- [Dependencies](#dependencies)
- [Development](#development)
- [Credits](#credits)
- [License](#license)

---

## Features
- **Player Abilities**: Jump, attack, and switch between multiple tools (pickaxe, axe, shovel, sword).
- **Enemies**:
  - **Skeletons**: Ground enemies with different movement speeds.
  - **Birds**: Flying enemies with unique patterns.
- **Scoring System**: Earn points for defeating enemies and aim to beat the high score.
- **Dynamic Backgrounds**: Layered parallax scrolling for immersive gameplay.
- **Customizable Sound**: Background music and sound effects enhance the gaming experience.

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Ensure you have Python 3.8 or higher installed.
3. Install the required dependencies:
   ```bash
   pip install pygame
   ```
4. Run the game:
   ```bash
   python code/main.py
   ```

---

## How to Play

1. Launch the game and select "PLAY" from the main menu.
2. Navigate the environment, defeat enemies, and avoid taking damage.
3. Use tools strategically to maximize damage and maintain health.
4. Aim for the highest score and compete with yourself or others.

---

## Controls
- **Arrow Keys**: Move left/right.
- **Space**: Jump.
- **F**: Use the selected tool.
- **R**: Use the sword.
- **1, 2, 3**: Switch tools (pickaxe, axe, shovel).

---

## Dependencies
- Python 3.8 or higher
- Pygame (installed via `pip install pygame`)

---

## Development

### Directory 

```
./
│
├── code/
│
└── resources/
    │
    ├── audio/
    │
    ├── background/
    │
    ├── button/
    │
    ├── enemies/
    │
    ├── fonts/
    │
    ├── icon/
    │
    ├── overlay/
    │
    └── player/
```


### File Structure
- **main.py**: Game entry point.
- **player.py**: Player class and mechanics.
- **skeleton.py**: Skeleton enemy logic.
- **bird.py**: Bird enemy logic.
- **scene.py**: Game scene and background management.
- **ui.py**: User interface components (menu, buttons).
- **utilities.py**: Helper functions (e.g., loading assets, handling scores).

### Resources
Assets (sprites, audio) are located in the `resources` directory and are dynamically loaded during runtime.

---

## Credits

Special thanks to my girlfriend for her invaluable support during the development process, helping with artistic choices and thoroughly playtesting the game.

---

## License
This project is open-source and available under the MIT License. Feel free to contribute, modify, or distribute the game as per the license terms.
