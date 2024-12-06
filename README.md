# Obstacle Jumping Game & Simple Wave Ripple Simulator

This is a simple obstacle jumping game built using Pygame. The player controls an avatar that can jump, move left, and move right to avoid obstacles and collect power-ups. 

There is also a simple wave ripple simulator that when a user clicks the mouse the waves appear.

## Features

- Control an avatar to jump and move left or right.
- Avoid obstacles and collect power-ups.
- Power-ups include invincibility, shrink, flight, and ball speed increase.
- Power-downs include frozen state.
- Two balls move around the screen and can collide with the avatar.
- Win the game by reaching the golden hoop.
- Game over if the avatar collides with a ball.

## Controls

- `Left Arrow`: Move left
- `Right Arrow`: Move right
- `Up Arrow`: Jump
- `S`: Start the game
- `R`: Restart the game
- `Q`: Quit the game

## Installation

1. Install Python:
    - Download and install Python from the official website: [python.org](https://www.python.org/downloads/)
    - Make sure to add Python to your system PATH during installation.

2. Clone the repository:
    ```sh
    git clone https://github.com/magotajuoi/Obstacle-jumping-Game.git
    cd Obstacle-Jumping-Game-Wave-Ripple-Project
    ```

3. Install the required dependencies:
    ```sh
    pip install pygame
    ```

4. Run the game:
    ```sh
    python jumping_game.py
    ```

5. Run the WebGL file:
    ```sh
    start RippleWaves.html
    ```

## File Structure

- `jumping_game.py`: Main game logic and implementation.
- `README.md`: Project documentation.
- `RippleWaves.html`: WebGL ripple effect implementation.

## Dependencies

- Python 3.x
- Pygame


## Acknowledgements

- Pygame library for game development.
- Sound effects from [freesound.org](https://freesound.org).

