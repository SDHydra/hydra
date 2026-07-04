import pygame as pg
import random
import math

CHUNK_SIZE = 64 # Size of each chunk (number of tiles in one dimension)

# Size of each chunk (number of tiles in one dimension)
TILES = {
    0: pg.Color('green'),  # Grass
    1: pg.Color('pink'),  # Pink flower
    2: pg.Color('blue'),  # Blue flower
    3: pg.Color('yellow'),  # Sunflower
}

class Chunk:  # Class to represent a chunk of tiles
    def __init__(self, chunk_x, chunk_y): # Initialize a chunk with given coordinates
        self.chunk_x = chunk_x # Coordinates of the chunk
        self.chunk_y = chunk_y # Coordinates of the chunk
        self.tiles = self.generate_chunk() # Generate the chunk of tiles
        print(f"Generating chunk at {self.chunk_x}, {self.chunk_y}")


    def generate_chunk(self):
        chunk = [[0 for _ in range(CHUNK_SIZE)] for _ in range(CHUNK_SIZE)]  # All grass

        for y in range(CHUNK_SIZE):
            for x in range(CHUNK_SIZE):
                rand = random.random()
                tile_type = None

                if rand < 0.1: # 1% chance to place two flowers
                    tile_type = 1  # Pink flower
                elif rand < 0.2: # 1% chance to place blue flowers
                    tile_type = 2  # Blue flower
                elif rand < 0.3: # 1% chance to place sunflowers
                    tile_type = 3  # Sunflower

                if tile_type:
                    spacing = random.randint(1, 4) # Random spacing between 1 and 4 tiles
                    can_place = True
                    # Check if the tile can be placed without overlapping with existing tiles
                    for ny in range(max(0, y - spacing), min(CHUNK_SIZE, y + spacing + 1)):
                        for nx in range(max(0, x - spacing), min(CHUNK_SIZE, x + spacing + 1)):
                            if chunk[ny][nx] == tile_type:
                                can_place = False
                                break

                        if not can_place: # If a tile of the same type is found in the vicinity, break out of the loop
                            break

                    if can_place: # Check if the tile can be placed
                        chunk[y][x] = tile_type # Place the tile

        return chunk # Return the generated chunk
    
class World: # Class to represent the game world
    def __init__(self, tile_size, grass_frames=None, two_flower_animation_frame=None, bf_frames=None, sunflower_frames=None): # Initialize the world with a given tile size
        self.tile_size = tile_size # Size of each tile
        self.chunks = {} # Dictionary to store chunks

        self.grass_frames = grass_frames # List of grass frames for animation
        self.two_flower_animation_frame = two_flower_animation_frame # List of flower frames for 
        self.bf_frames = bf_frames # List of blue flower frames for animation
        self.sunflower_frames = sunflower_frames # List of sunflower frames for animation


        self.grass_animation_frame = 0 # Current frame for grass animation
        self.flower_animation_frame = 0 # Current frame for flower animation
        self.bf_animation_frame = 0
        self.sunflower_animation_frame = 0 # Current frame for sunflower animation

        self.frame_tier = 0 # Timer for animation frames

        self.frame_delay = 350 # Delay between frames in milliseconds

    def update(self, dt): # Update the world state
        self.frame_tier += dt # Increment the frame timer
        if self.frame_tier >= self.frame_delay:
            self.frame_tier = 0 # Reset the frame timer
            if self.grass_frames:
                self.grass_animation_frame = (self.grass_animation_frame + 1) % len(self.grass_frames) # Update the grass animation frame
            if self.two_flower_animation_frame:
                self.flower_animation_frame = (self.flower_animation_frame + 1) % len(self.two_flower_animation_frame) # Update the flower animation frame
            if self.bf_frames:
                self.bf_animation_frame = (self.bf_animation_frame + 1) % len(self.bf_frames) # Update the blue flower animation frame
            if self.sunflower_frames:
                self.sunflower_animation_frame = (self.sunflower_animation_frame + 1) % len(self.sunflower_frames) # Update the sunflower animation frame
        
    def get_chunk_key(self, tile_x, tile_y): # Get the chunk coordinates based on tile coordinates
        return tile_x // CHUNK_SIZE, tile_y // CHUNK_SIZE # Get the chunk coordinates based on tile coordinates
    
    def get_tile(self, tile_x, tile_y): # Get the tile type at the given coordinates
        
        chunk_key = self.get_chunk_key(tile_x, tile_y) # Get the chunk coordinates
        if chunk_key not in self.chunks: # Check if the chunk exists
            self.chunks[chunk_key] = Chunk(*chunk_key) # Create a new chunk if it doesn't exist

        return self.chunks[chunk_key].tiles[tile_y % CHUNK_SIZE][tile_x % CHUNK_SIZE]


    def draw(self, screen, camera): # Draw the world to the screen
        screen_tiles_x = screen.get_width() // self.tile_size + 2 # Calculate the number of tiles that fit on the screen
        screen_tiles_y = screen.get_height() // self.tile_size + 2 # Calculate the number of tiles that fit on the screen

        start_tile_x = math.floor(-camera.x / self.tile_size) # Calculate the starting tile coordinates
        start_tile_y = math.floor(-camera.y / self.tile_size) # Calculate the starting tile coordinates

        for y in range(screen_tiles_y): # Loop through the visible tiles
            for x in range(screen_tiles_x): # Loop through the visible tiles

                tile_x = start_tile_x + x # Calculate the tile coordinates
                tile_y = start_tile_y + y # Calculate the tile coordinates

                tile_type = self.get_tile(tile_x, tile_y) # Get the tile type from the chunk
                draw_x = tile_x * self.tile_size + camera.x # Adjust for camera offset
                draw_y = tile_y * self.tile_size + camera.y # Adjust for camera offset

                if tile_type == 0 and self.grass_frames:
                    frame = pg.transform.scale(self.grass_frames[self.grass_animation_frame], (self.tile_size, self.tile_size)) # Get the current grass frames
                    screen.blit(frame, (draw_x, draw_y))

                elif tile_type == 1 and self.two_flower_animation_frame:
                    frame = pg.transform.scale(self.two_flower_animation_frame[self.flower_animation_frame], (self.tile_size, self.tile_size)) # Get the current flower frames
                    screen.blit(frame, (draw_x, draw_y))
                
                elif tile_type == 2 and self.bf_frames:
                    frame = pg.transform.scale(self.bf_frames[self.bf_animation_frame], (self.tile_size, self.tile_size))
                    screen.blit(frame, (draw_x, draw_y))
                
                elif tile_type == 3 and self.sunflower_frames:
                    frame = pg.transform.scale(self.sunflower_frames[self.sunflower_animation_frame], (self.tile_size, self.tile_size))
                    screen.blit(frame, (draw_x, draw_y))

                #pg.draw.rect(screen, (255, 0, 0), pg.Rect(draw_x, draw_y, self.tile_size, self.tile_size), 1