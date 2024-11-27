import pygame
import random
import time

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
    pygame.Rect(50, 325, 200, 30),
    pygame.Rect(550, 325, 200, 30)
]

# Define Avatar class
class Avatar:
    def __init__(self, start_x, start_y, block_size):
        self.x = start_x
        self.y = start_y
        self.block_size = block_size
        self.blocks = []
        self.is_jumping = False
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_speed = -10
        self.grounded = True
        self.horizontal_speed = 5
        self.air_resistance = 0.95  # Slow down horizontal speed in the air
        self.invincible = False
        self.shrunk = False
        self.flight = False
        self.frozen = False

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
        if self.grounded:
            self.velocity_x = -self.horizontal_speed
        else:
            self.velocity_x = -self.horizontal_speed * 0.5

    def move_right(self):
        if self.grounded:
            self.velocity_x = self.horizontal_speed
        else:
            self.velocity_x = self.horizontal_speed * 0.5

    def start_jump(self):
        if not self.is_jumping and self.grounded:
            self.is_jumping = True
            self.velocity_y = self.jump_speed
            self.grounded = False

    def is_on_ground(self):
        for block in self.blocks:
            for obstacle in obstacles:
                if block.bottom == obstacle.top and block.colliderect(obstacle.inflate(0, 1)):
                    return True
        return False

    def collide_with_obstacles(self):
        for block in self.blocks:
            for obstacle in obstacles:
                if block.colliderect(obstacle):
                    if self.velocity_y < 0 and block.bottom <= obstacle.top:
                        continue
                    return True
        return False

    def apply_gravity_and_movement(self):
        if not self.is_on_ground():
            self.velocity_y += self.gravity
            self.y += self.velocity_y
            self.update_position()

            if self.collide_with_obstacles():
                self.y -= self.velocity_y
                self.velocity_y = 0
                self.grounded = True
                self.is_jumping = False
                self.update_position()
        else:
            self.grounded = True
            self.velocity_y = 0

        self.x += self.velocity_x
        self.update_position()

        if self.collide_with_obstacles():
            self.x -= self.velocity_x
            self.velocity_x = 0
            self.update_position()

        if self.y + self.block_size * 5 > HEIGHT:
            self.y = HEIGHT - self.block_size * 5
            self.velocity_y = 0
            self.grounded = True
            self.is_jumping = False
            self.update_position()

        if not self.grounded:
            self.velocity_x *= self.air_resistance

    def draw(self, surface):
        for block in self.blocks:
            pygame.draw.rect(surface, BLACK, block)
            pygame.draw.rect(surface, WHITE, block, 1)

# Define Ball class
class Ball:
    def __init__(self, x, y, radius, color, velocity_x, velocity_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.velocity_x = -self.velocity_x
        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.velocity_y = -self.velocity_y

        for obstacle in obstacles:
            if pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2).colliderect(obstacle):
                if abs(self.x - obstacle.left) < self.radius or abs(self.x - obstacle.right) < self.radius:
                    self.velocity_x = -self.velocity_x
                if abs(self.y - obstacle.top) < self.radius or abs(self.y - obstacle.bottom) < self.radius:
                    self.velocity_y = -self.velocity_y

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

# Function to check collision between a ball and the avatar
def check_ball_avatar_collision(ball, avatar):
    ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, ball.radius * 2, ball.radius * 2)
    for block in avatar.blocks:
        if ball_rect.colliderect(block):
            return True
    return False

# Function to spawn power-ups and power-downs
def spawn_power_up_or_down():
    power_type = random.choice(['power_up', 'power_down'])
    box_type = random.choice(['invincibility', 'shrink', 'flight', 'frozen', 'ball_speed_increase'])
    x = random.randint(0, WIDTH - 50)
    y = 0
    return {
        "type": power_type,
        "box_type": box_type,
        "rect": pygame.Rect(x, y, 20, 20),
        "fall_speed": 1.5
    }

# Function to handle power-up effects
def apply_power_up_or_down(power_box, avatar, balls):
    global power_text, power_text_start_time
    # Set the text and start time for display
    power_text = power_box["box_type"]
    power_text_start_time = pygame.time.get_ticks()

    if power_box["type"] == "power_up":
        if power_box["box_type"] == "invincibility":
            avatar.invincible = True
            pygame.time.set_timer(pygame.USEREVENT + 1, 10000)  # 10 seconds
        elif power_box["box_type"] == "shrink":
            avatar.block_size -= 10
            avatar.shrunk = True
            pygame.time.set_timer(pygame.USEREVENT + 2, 5000)  # 5 seconds
        elif power_box["box_type"] == "flight":
            avatar.flight = True
            pygame.time.set_timer(pygame.USEREVENT + 3, 10000)  # 10 seconds
    elif power_box["type"] == "power_down":
        if power_box["box_type"] == "frozen":
            avatar.frozen = True
            pygame.time.set_timer(pygame.USEREVENT + 4, 5000)  # 5 seconds
        elif power_box["box_type"] == "ball_speed_increase":
            for ball in balls:
                ball.velocity_x *= 1.5
                ball.velocity_y *= 1.5
            pygame.time.set_timer(pygame.USEREVENT + 5, 5000)  # 5 seconds

# Helper function to display power-up or power-down text
font = pygame.font.Font(None, 36)
def display_power_text(surface, text):
    if text:
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        surface.blit(text_surface, text_rect)

# Initialize game objects
avatar = Avatar(100, 400, 20)
ball = Ball(400, 300, 25, RED, 3, 3)
ball2 = Ball(200, 100, 25, RED, -3, 3)
power_boxes = []

# Power-up/down display variables
power_text = ""
power_text_start_time = None

# Main game loop
running = True
spawn_timer = pygame.time.get_ticks()
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT + 1:
            avatar.invincible = False
        if event.type == pygame.USEREVENT + 2:
            avatar.block_size += 10
            avatar.shrunk = False
        if event.type == pygame.USEREVENT + 3:
            avatar.flight = False
        if event.type == pygame.USEREVENT + 4:
            avatar.frozen = False
        if event.type == pygame.USEREVENT + 5:
            ball.velocity_x /= 1.5
            ball.velocity_y /= 1.5
            ball2.velocity_x /= 1.5
            ball2.velocity_y /= 1.5

    # Clear power_text after 2 seconds
    if power_text and power_text_start_time and current_time - power_text_start_time > 2000:
        power_text = ""

    # Spawn power-ups and power-downs at intervals
    if current_time - spawn_timer > 5000:
        power_boxes.append(spawn_power_up_or_down())
        spawn_timer = current_time

    keys = pygame.key.get_pressed()
    if not avatar.frozen:
        if keys[pygame.K_LEFT]:
            avatar.move_left()
        if keys[pygame.K_RIGHT]:
            avatar.move_right()
        if keys[pygame.K_UP]:
            avatar.start_jump()

    avatar.apply_gravity_and_movement()
    ball.move()
    ball2.move()

    # Check for collision with the avatar
    if check_ball_avatar_collision(ball, avatar) or check_ball_avatar_collision(ball2, avatar):
        if not avatar.invincible:
            print("Game Over!")
            running = False

    # Check for power-up/power-down collision with avatar
    for power_box in power_boxes[:]:
        power_box["rect"].y += power_box["fall_speed"]
        if power_box["rect"].colliderect(avatar.blocks[0]):  # Avatar's top-left block for collision detection
            apply_power_up_or_down(power_box, avatar, [ball, ball2])
            power_boxes.remove(power_box)

    # Draw everything
    window.fill(LIGHT_BLUE)

    for obstacle in obstacles:
        outline_rect = pygame.Rect(obstacle.x - 2, obstacle.y - 2, obstacle.width + 4, obstacle.height + 4)
        pygame.draw.rect(window, BLACK, outline_rect)
        pygame.draw.rect(window, WHITE, obstacle)

    avatar.draw(window)
    ball.draw(window)
    ball2.draw(window)

    for power_box in power_boxes:
        color = YELLOW if power_box["type"] == "power_up" else RED
        pygame.draw.rect(window, color, power_box["rect"])

    # Display power-up/power-down name
    display_power_text(window, power_text)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
