import pygame as pg
import os
from weapon import Weapon

class Player:
    def __init__(self, start_x, start_y, speed, sprite_dir, scale_factor=None, world_width=None, world_height=None):
        self.speed = speed # Player speed
        self.world_width = world_width # World dimensions Width
        self.world_height =  world_height # World dimensions Height
        self.scale_factor = scale_factor # Scale factor for the sprite
        self.direction = 'idle'  # Default direction

        # Initialize the weapon
        self.weapon = Weapon("art/weapon_objects")

        # Initialize animation variables
        self.frame_index = 0 # Current frame index
        self.animation_timer = 0  # Timer for animation frames
        self.animation_speed = 300  # Animation speed in milliseconds

        # Load the sprites for each direction
        self.sprites = {
            "up": self.load_animation(sprite_dir, "slime_top", 3),
            "down": self.load_animation(sprite_dir, "slime_down", 3),
            "left": self.load_animation(sprite_dir, "slime_left", 3),
            "right": self.load_animation(sprite_dir, "slime_right", 3),
            "idle": [pg.image.load(os.path.join(sprite_dir, "slime.png")).convert_alpha()]
        }
        
        # Set the initial image to the idle sprite
        first_frame = self.sprites[self.direction][0] # self.sprites[self.direction] → gives a list of frames (images), e.g. [slime_down1.png, slime_down2.png, slime_down3.png].
                                                      # You cannot call .get_width() on a list. Need to call it on the first frame of the list, which is slime_down1.png.
        self.image = pg.transform.scale(
            first_frame,
            (
                int(first_frame.get_width() * self.scale_factor),
                int(first_frame.get_height() * self.scale_factor)
            )
        )  # Scale the sprite to the desired size
        
        # Set the initial position of the player
        self.rect = self.image.get_rect() # Get the rectangle of the image
        self.rect.center = (start_x, start_y)  # Start at the given position (e.g., screen center)

    def load_animation(self, sprite_dir, base_filename, frame_count):
        frames = []
        for i in range(1, frame_count + 1): # frame_count is the number of sprites 3, the 1 infront is the first sprite the + 1 in the end is for 4 which stops there
            path = os.path.join(sprite_dir, f"{base_filename}{i}.png")
            image = pg.image.load(path).convert_alpha()
            frames.append(image)
        return frames

    # Update the sprite based on the direction
    def update_sprite(self, dt):
        frames = self.sprites[self.direction]

        if self.direction != "idle": # != "idle" means the player is moving ! means not with = it means not equal
            self.animation_timer += dt # Increment the animation timer
            if self.animation_timer >= self.animation_speed: # Check if it's time to switch frames
                self.animation_timer = 0 # Reset the timer
                self.frame_index = (self.frame_index + 1) % len(frames) # Move to the next frame in the animation sequence.
                # The % len(frames) part ensures that after the last frame, it loops back to the first frame smoothly.
                # % calculates division ramainder, example: 5 % 3 = 2 remainder 2, 6 % 3 = 0 remainder 0
                # Means go to the next frame, if the next frame is 3 then go back to 0
                # If you have 3 frames (indexes 0,1,2), and self.frame_index is 2 (last frame), adding 1 gives 3, but 3 % 3 is 0 — so it loops back to the first frame smoothly.
                # len returns the number of elements in the list, so if you have 3 frames, len(frames) = 3
        else:
            self.frame_index = 0  # Reset to first frame when idle

        sprite = frames[self.frame_index] # Get the current frame sprite
        self.image = pg.transform.scale( # Scale the sprite to the desired size
            sprite,
            (
                int(sprite.get_width() * self.scale_factor),
                int(sprite.get_height() * self.scale_factor)
            )
        )

    # Handle player movement and key events
    def handle_keys(self, dt, camera):
        keys = pg.key.get_pressed()
        movement = self.speed * dt  # Multiply speed by delta time to make it frame rate independent

        moved = False # Initialize moved to False

        # Check for key presses and move the player accordingly
        if keys[pg.K_a]:
            self.rect.x -= movement
            self.direction = 'left'
            moved = True
        elif keys[pg.K_d]:
            self.rect.x += movement
            self.direction = 'right'
            moved = True
        elif keys[pg.K_w]:
            self.rect.y -= movement
            self.direction = 'up'
            moved = True
        elif keys[pg.K_s]:
            self.rect.y += movement
            self.direction = 'down'
            moved = True
        else:
            self.direction = 'idle'

        self.update_sprite(dt) # Update the sprite based on the direction

        mouse_pos = pg.mouse.get_pos() # Get current mouse position
        mouse_held = pg.mouse.get_pressed()[0] # Check if left mouse button is held
        mouse_world_x = mouse_pos[0] + camera.x # Convert mouse x to world coordinates

        # If mouse is held, attack with the weapon
        if mouse_held:
            self.weapon.attack(mouse_pos, self.rect, camera)
        # Update the weapon
        self.weapon.update(dt, self.rect, mouse_world_x, mouse_held)
    
        # Keep player within world bounds (rect is player's rectangle)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.world_width:
            self.rect.right = self.world_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.world_height:
            self.rect.bottom = self.world_height
    
    # Clamp player to camera view
    def clamp_player_to_camera_view(self, camera):
    # Clamp player inside camera view boundaries
        if self.rect.left < -camera.x:
            self.rect.left = -camera.x
        if self.rect.right > -camera.x + camera.width:
            self.rect.right = -camera.x + camera.width
        if self.rect.top < -camera.y:
            self.rect.top = -camera.y
        if self.rect.bottom > -camera.y + camera.height:
            self.rect.bottom = -camera.y + camera.height

    # Draw the player on the screen
    def draw(self, screen, camera):
        # Apply camera transformation and draw player
        screen.blit(self.image, camera.apply(self))
        self.weapon.draw(screen, camera)