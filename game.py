import pygame

# Initialize Pygame
pygame.init()

# Set up the game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Crossy Road")

# Load assets
player_image = pygame.image.load("assets/player.png")
player_image = pygame.transform.scale(player_image, (50, 50))
road_image = pygame.image.load("assets/road.png")
road_image = pygame.transform.scale(road_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Set up player
player_rect = player_image.get_rect()
player_rect.topleft = (0, SCREEN_HEIGHT // 2 - player_rect.height // 2)

# Define train track boundaries
track_rects = [
    # Vertical train tracks
    pygame.Rect(80, 0, 100, 600),    # Left vertical track
    pygame.Rect(360, 0, 100, 600),   # Center vertical track
    pygame.Rect(640, 0, 100, 600),   # Right vertical track

    # Horizontal train tracks
    pygame.Rect(0, 180, 800, 120),   # Top horizontal track
    pygame.Rect(0, 420, 800, 120),   # Bottom horizontal track
]

# Function to calculate dynamic rectangles for scrolling
def calculate_dynamic_rects(base_rects, road_offset):
    return [
        pygame.Rect(rect.left + road_offset, rect.top, rect.width, rect.height)
        for rect in base_rects
    ]

# Function to check if player is within valid boundaries
def is_within_boundaries(new_rect, boundaries):
    for rect in boundaries:
        if new_rect.colliderect(rect):
            return True
    return False

# Main game loop
running = True
road_x = 0
road_speed_x = 1  # Scrolling speed

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update scrolling
    road_x -= road_speed_x
    if road_x <= -SCREEN_WIDTH:
        road_x = 0  # Reset scrolling

    # Calculate dynamic boundaries
    dynamic_rects = calculate_dynamic_rects(track_rects, road_x)

    # Update player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        new_rect = player_rect.move(-5, 0)
        if is_within_boundaries(new_rect, dynamic_rects):
            player_rect = new_rect
    if keys[pygame.K_RIGHT]:
        new_rect = player_rect.move(5, 0)
        if is_within_boundaries(new_rect, dynamic_rects):
            player_rect = new_rect
    if keys[pygame.K_UP]:
        new_rect = player_rect.move(0, -5)
        if is_within_boundaries(new_rect, dynamic_rects):
            player_rect = new_rect
    if keys[pygame.K_DOWN]:
        new_rect = player_rect.move(0, 5)
        if is_within_boundaries(new_rect, dynamic_rects):
            player_rect = new_rect

    # Draw the road
    screen.blit(road_image, (road_x, 0))
    screen.blit(road_image, (road_x + SCREEN_WIDTH, 0))  # Seamless scrolling

    # Draw the player
    screen.blit(player_image, player_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
