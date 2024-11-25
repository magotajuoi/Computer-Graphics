import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Obstacle Jumping Game")

# Define colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define obstacles dimensions (rectangles)
obstacles = [
    pygame.Rect(100, 548, 50, 50),
    pygame.Rect(250, 548, 50, 50),
    pygame.Rect(275, 496, 50, 50),
    pygame.Rect(300, 548, 50, 50),
    pygame.Rect(450, 548, 50, 50),
    pygame.Rect(500, 548, 50, 50),
    pygame.Rect(650, 548, 50, 50),
    pygame.Rect(675, 496, 50, 50),
    pygame.Rect(700, 548, 50, 50),
    pygame.Rect(150, 325, 200, 30),
    pygame.Rect(550, 325, 200, 30)
]

# Define Avatar class with realistic gravity and horizontal movement
class Avatar:
    def __init__(self, start_x, start_y, block_size):
        self.x = start_x
        self.y = start_y
        self.block_size = block_size
        self.blocks = []
        self.is_jumping = False
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 1
        self.jump_speed = -15
        self.grounded = False
        self.horizontal_speed = 5
        self.air_resistance = 0.95  # Slow down horizontal speed in the air

        avatar_structure = [
            [0, 1, 0, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
            [0, 1, 0, 1, 0],
            [1, 0, 0, 0, 1]
        ]

        for row_index, row in enumerate(avatar_structure):
            for col_index, cell in enumerate(row):
                if cell == 1:
                    x = self.x + col_index * block_size
                    y = self.y + row_index * block_size
                    self.blocks.append(pygame.Rect(x, y, block_size, block_size))

    def update_position(self):
        index = 0
        for row_index, row in enumerate([
            [0, 1, 0, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
            [0, 1, 0, 1, 0],
            [1, 0, 0, 0, 1]
        ]):
            for col_index, cell in enumerate(row):
                if cell == 1:
                    x = self.x + col_index * self.block_size
                    y = self.y + row_index * self.block_size
                    self.blocks[index].topleft = (x, y)
                    index += 1

    def move_left(self):
        if self.grounded:  # Apply full horizontal speed if grounded
            self.velocity_x = -self.horizontal_speed
        elif not self.grounded:  # Apply slower horizontal speed in the air
            self.velocity_x = -self.horizontal_speed * 0.5

    def move_right(self):
        if self.grounded:
            self.velocity_x = self.horizontal_speed
        elif not self.grounded:
            self.velocity_x = self.horizontal_speed * 0.5

    def start_jump(self):
        if not self.is_jumping and self.grounded:
            self.is_jumping = True
            self.velocity_y = self.jump_speed
            self.grounded = False

    def apply_gravity_and_movement(self):
        # Apply gravity and update vertical position
        if not self.grounded:
            self.velocity_y += self.gravity
            self.y += self.velocity_y
            self.update_position()

            # Decay horizontal speed in the air to simulate air resistance
            self.velocity_x *= self.air_resistance
            self.x += self.velocity_x
            self.update_position()

            # Collision check to see if we landed on an obstacle
            if self.collide_with_obstacles():
                self.y -= self.velocity_y  # Reset y position to "land"
                self.velocity_y = 0
                self.grounded = True
                self.is_jumping = False
                self.update_position()
        else:
            # Allow movement in both directions when grounded
            self.x += self.velocity_x
            self.update_position()

            # Reset horizontal velocity to zero when grounded to stop continuous movement
            self.velocity_x = 0

    def collide_with_obstacles(self):
        for block in self.blocks:
            for obstacle in obstacles:
                if block.colliderect(obstacle):
                    return True
        return False

    def draw(self, surface):
        for block in self.blocks:
            pygame.draw.rect(surface, BLACK, block)
            pygame.draw.rect(surface, WHITE, block, 1)

# Set parameters for the avatar
block_size = 17
avatar_x = WIDTH // 2 - block_size * 2
avatar_y = HEIGHT - 150
avatar = Avatar(avatar_x, avatar_y, block_size)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        avatar.move_left()
    if keys[pygame.K_RIGHT]:
        avatar.move_right()
    if keys[pygame.K_UP]:
        avatar.start_jump()

    # Update avatar's position with gravity and movement
    avatar.apply_gravity_and_movement()

    # Fill background
    window.fill(LIGHT_BLUE)

    # Draw obstacles
    for obstacle in obstacles:
        outline_rect = pygame.Rect(obstacle.x - 2, obstacle.y - 2, obstacle.width + 4, obstacle.height + 4)
        pygame.draw.rect(window, BLACK, outline_rect)
        pygame.draw.rect(window, WHITE, obstacle)

    # Draw the avatar
    avatar.draw(window)

    # Update display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(30)

# Quit Pygame
pygame.quit()