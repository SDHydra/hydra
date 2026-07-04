import pygame as pg
import sys
from camera import Camera
from player import Player
from world import World  # You'll create this
from inventory import Inventory
from projectile import BallProjectile  # You'll create this
from utils.enemy_spawner import spawn_enemy_near_player
from enemy.plague_slime import Plague_Slime
import os

def get_button_rect(screen):
    screen_width, screen_height = screen.get_size()

    # Calculate button rectangle based on screen size
    x_start = int(screen_width * 0.2917) # 0.2917 is 0.2917 * 1920 = 560
    y_start = int(screen_height * 0.5306) # 0.2917 is 0.2917 * 1920 = 560, 0.5306 is 0.5306 * 1080 = 573
    x_end = int(screen_width * 0.7086) # 0.7086 is 0.7086 * 1920 = 1368
    y_end = int(screen_height * 0.725) # 0.725 is 0.725 * 1080 = 783

    return pg.Rect(x_start, y_start, x_end - x_start, y_end - y_start) # Rectangle for the start button

def show_start_screen(screen):
    global is_fullscreen

    start_screen_path = os.path.join(os.path.dirname(__file__), 'art', 'start_screen', 'start_screen.png') # Path to the start screen image
    start_image = pg.image.load(start_screen_path).convert() # Load the start screen image
    start_image = pg.transform.scale(start_image, screen.get_size()) # Scale the image to fit the screen

    font = pg.font.Font(None, 36)

    button_rect = get_button_rect(screen) # Get the button rectangle for the start button

    waiting = True # Flag to control the waiting state
    while waiting: # Wait for user input
        screen.blit(start_image, (0, 0))
        
        # Debug mouse position
        mouse_x, mouse_y = pg.mouse.get_pos()
        text_surface = font.render(f"Mouse: {mouse_x}, {mouse_y}", True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        pg.display.flip() # Update the display

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_F11:
                    is_fullscreen = not is_fullscreen
                    screen = pg.display.set_mode(
                        FULL_SCREEN if is_fullscreen else WINDOW_SIZE,
                        pg.FULLSCREEN if is_fullscreen else 0
                    )
                    start_image = pg.transform.scale(start_image, screen.get_size())
                    button_rect = get_button_rect(screen) # Update button rectangle for new screen size
            elif event.type == pg.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos): # Check if the button is clicked
                    waiting = False # Exit the waiting loop if the button is clicked

def main():
    global is_fullscreen, FULL_SCREEN, WINDOW_SIZE, FPS, TILE_SIZE, player_speed

    pg.init()

    FULL_SCREEN = (1920, 1080)  # Fullscreen resolution
    WINDOW_SIZE = (1920, 1020)  # Windowed resolution
    FPS = 120  # Frames per second
    TILE_SIZE = 70 # Size of each tile in pixels
    player_speed = 0.3 # Speed of the player in pixels per millisecond

    is_fullscreen = True  # Set to True for fullscreen mode
    screen = pg.display.set_mode(FULL_SCREEN, pg.FULLSCREEN if is_fullscreen else 0) # Set the display mode
    show_start_screen(screen)  # Just pass the screen; image loading is handled inside

    clock = pg.time.Clock() # Create a clock to manage the frame rate

    current_dir = os.path.dirname(__file__)

    # Load player sprite
    player_sprite_dir = os.path.join(current_dir, 'art', 'main_slime')

    # Load enemy sprites
    enemies = pg.sprite.Group()
    enemy_spawn_timer = 0
    enemy_spawn_delay = 3000  # Spawn an enemy every 3000 milliseconds

    plague_slime_sprite_dir = os.path.join(current_dir, "art", "enemy_objects", "plague slime")

    # Load projectile sprite
    ball_projectile_path = os.path.join(current_dir, 'art', 'projectile_object', 'ball.png') # Path to the projectile image
    ball_projectile = pg.image.load(ball_projectile_path).convert_alpha() # Load the projectile image
    ball_projectile = pg.transform.scale(ball_projectile, (16, 16))  # Scale the projectile image

    # Load Inventory sprite
    inventory_sprite_path = os.path.join(current_dir, 'art', 'inventory_objects', 'inventory.png')
    
    # Load grass Sprite sheets
    grass_path = os.path.join(current_dir, 'art', 'world_objects')

    grass_frames = []
    for i in range(1, 4):
        path = os.path.join(grass_path, f'grass{i}.png')
        image_grass = pg.image.load(path).convert_alpha()
        grass_frames.append(image_grass)
    
    flower_path = os.path.join(current_dir, 'art', 'world_objects')

    two_flower_frames = []
    for i in range(1, 4): 
        path = os.path.join(flower_path, f'two_flower{i}.png')
        image_flower = pg.image.load(path).convert_alpha()
        two_flower_frames.append(image_flower)

    blue_flower_path = os.path.join(current_dir, 'art', 'world_objects')

    blue_two_flower_frames = []
    for i in range(1, 6):
        path = os.path.join(blue_flower_path, f'blue_flower{i}.png')
        image_blue_flower = pg.image.load(path).convert_alpha()
        blue_two_flower_frames.append(image_blue_flower)
    
    sunflower_path = os.path.join(current_dir, 'art', 'world_objects')

    sunflower_frames = []
    for i in range(1, 3):
        path = os.path.join(sunflower_path, f'sunflower{i}.png')
        image_sunflower = pg.image.load(path).convert_alpha()
        sunflower_frames.append(image_sunflower)

    # World dimensions
    world_width = 4970 # fits with tile size
    world_height = 2940 # fits with tile size

    # Calculate the starting position of the player
    start_x = world_width // 2
    start_y = world_height // 2

    scale_factor = 2.8 # Scale factor for the player sprite, adjust as needed

    # Initialize player and camera
    camera_width, camera_height = FULL_SCREEN  # Camera sizew
    player = Player(start_x, start_y, player_speed, player_sprite_dir, scale_factor=scale_factor, world_width=world_width, world_height=world_height) # Player starts at (0, 0)
    camera = Camera(camera_width, camera_height, world_width, world_height)  # Camera size
    world = World(TILE_SIZE, grass_frames, two_flower_frames, blue_two_flower_frames, sunflower_frames) # Initialize world with tile size
    inventory = Inventory(inventory_sprite_path, scale_factor=10)  # Initialize inventory
    projectiles = pg.sprite.Group()  # Group to hold all projectiles

    font = pg.font.Font(None, 36)

    running = True # Main game loop flag
    # Main game loop
    while running:
        dt = clock.tick(FPS) # Convert milliseconds to seconds
        enemy_spawn_timer += dt # Increment enemy spawn timer
        if enemy_spawn_timer >= enemy_spawn_delay: # Check if it's time to spawn a new enemy
            enemy_spawn_timer = 0
            spawn_enemy_near_player(player, plague_slime_sprite_dir, enemies) # Spawn a new enemy near the player

        # Ensure the weapon has a hit_enemies set
        if not hasattr(player.weapon, 'hit_enemies'):
            player.weapon.hit_enemies = set()
        # Collision detection every frame while attacking
        if player.weapon.attacking:
            for enemy in enemies:
                if player.weapon.rect.colliderect(enemy.rect):
                    if enemy not in player.weapon.hit_enemies:
                        enemy.take_damage(1)
                        player.weapon.hit_enemies.add(enemy)
            if player.weapon.frame_index == 0 and player.weapon.attacking:
                player.weapon.hit_enemies.clear()
                # check if collision with enemies and amount of damage

        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_F11:  # Toggle fullscreen
                    is_fullscreen = not is_fullscreen  # Toggle fullscreen mode
                    if is_fullscreen: # Fullscreen mode
                        screen = pg.display.set_mode(FULL_SCREEN, pg.FULLSCREEN) # Set fullscreen mode
                        camera.width, camera.height = FULL_SCREEN  # Update camera size
                    else:
                        screen = pg.display.set_mode(WINDOW_SIZE) # Set windowed mode
                        camera.width, camera.height = WINDOW_SIZE # Update camera size

                elif event.key == pg.K_SPACE:  # Fire projectile
                    spawn_pos = pg.Vector2(player.rect.center)
                    mouse_pos = pg.Vector2(pg.mouse.get_pos())
                    mouse_world = mouse_pos - pg.Vector2(camera.x, camera.y)
                    direction = mouse_world - spawn_pos

                    if direction.length() != 0:
                        direction = direction.normalize()
                        ball = BallProjectile(spawn_pos, direction, ball_projectile, speed=0.5)
                        projectiles.add(ball)
        

        # Debug mouse position
        mouse_x, mouse_y = pg.mouse.get_pos()
        text_surface = font.render(f"Mouse: {mouse_x}, {mouse_y}", True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        # Update game state
        player.handle_keys(dt, camera)
        
        world.update(dt)

        projectiles.update(dt)

        for enemy in enemies:
            enemy.update(player, dt)

        camera.update(player)

        player.clamp_player_to_camera_view(camera)

        # Clear screen
        screen.fill((0, 0, 0))

        # Draw world to screen using camera offset
        world.draw(screen, camera)

        # Draw inventory
        inventory.draw(screen, fullscreen=is_fullscreen)

        # Draw player (offset by camera)
        player.draw(screen, camera)

        # Draw projectiles
        for projectile in projectiles:
            screen.blit(projectile.image, camera.apply(projectile))

        # Draw enemies
                # Draw enemies
        for enemy in enemies:
            screen.blit(enemy.image, camera.apply(enemy))

        pg.display.flip()

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()