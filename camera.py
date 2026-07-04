import pygame as pg

class Camera:
    def __init__(self, width, height, map_width, map_height):
        self.width = width  # The width of the camera view
        self.height = height  # The height of the camera view
        self.map_width = map_width # The width of the map
        self.map_height = map_height # The height of the map
        self.x = 0  # Initial camera position (x)
        self.y = 0  # Initial camera position (y)

    # Apply the camera offset to a given entity's rectangle
    def apply(self, target):
        if hasattr(target, "rect"):  # works for sprites
            return target.rect.move(self.x, self.y)
        return target.move(self.x, self.y)  # works for plain Rects

    # Update the camera to follow the target (player)
    def update(self, target):
        # Center the camera on the player
        self.x = -target.rect.centerx + int(self.width / 2)  # Update camera to follow player position (no negative sign)
        self.y = -target.rect.centery + int(self.height / 2)  # Same for the y-axis

        # Keep the camera inside the bounds of the map
        self.x = min(0, self.x)  # Prevent scrolling off the left of the world
        self.y = min(0, self.y)  # Prevent scrolling off the top of the world
        self.x = max(-(self.map_width - self.width), self.x)  # Don't scroll past the right side of the map
        self.y = max(-(self.map_height - self.height), self.y)  # Don't scroll past the bottom of the map
