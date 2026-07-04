import pygame

pygame.init()

# Screen size
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Tile size
TILE_SIZE = 100

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)

# Player
player_x, player_y = 0, 0
player_speed = 5

# Game loop
running = True
while running:
    screen.fill(WHITE)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  player_x -= player_speed
    if keys[pygame.K_RIGHT]: player_x += player_speed
    if keys[pygame.K_UP]:    player_y -= player_speed
    if keys[pygame.K_DOWN]:  player_y += player_speed

    # Wrap player position (infinite movement)
    player_x %= SCREEN_WIDTH
    player_y %= SCREEN_HEIGHT

    # Draw repeating tiles
    for i in range(-1, SCREEN_WIDTH // TILE_SIZE + 2):
        for j in range(-1, SCREEN_HEIGHT // TILE_SIZE + 2):
            tile_x = (i * TILE_SIZE - (player_x % TILE_SIZE))
            tile_y = (j * TILE_SIZE - (player_y % TILE_SIZE))
            pygame.draw.rect(screen, GREEN, (tile_x, tile_y, TILE_SIZE, TILE_SIZE), 1)

    # Draw player (centered in the screen)
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 25, 50, 50))

    pygame.display.update()
    pygame.time.delay(30)

pygame.quit()
