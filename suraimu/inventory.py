import pygame as pg
import os

class Inventory:
    def __init__(self, sprite_path, scale_factor=1):
        if not os.path.exists(sprite_path):
            raise FileNotFoundError(f"Inventory sprite not found: {sprite_path}")

        self.scale_factor = scale_factor
        self.original_image = pg.image.load(sprite_path).convert_alpha()
        self.image = None # Will be set in _update_scale
        self.rect = self.original_image.get_rect()
        self._last_screen_size = None # To track last screen size

    # Only a safety measure for future changes
    def _update_scale(self, screen):
        """Rescale image to fit the current screen size."""
        screen_w, screen_h = screen.get_size()
        orig_w, orig_h = self.original_image.get_size()

        # Calculate new dimensions
        new_w = (orig_w * self.scale_factor)
        new_h = (orig_h * self.scale_factor)

        # Ensures the Inventory does not scale beyond what is needed
        print("Before limit:", new_w, new_h)
        if new_w > screen_w * 0.35:
            new_w = int(screen_w * 0.35)
        if new_h > screen_h * 0.09:
            new_h = int(screen_h * 0.09)
        print("After limit:", new_w, new_h)

        self.image = pg.transform.smoothscale(self.original_image, (new_w, new_h)) # Rescale the image
        self.rect = self.image.get_rect() # Get new rect after scaling
        self._last_screen_size = (screen_w, screen_h) # Store last screen size

    # Cheks if re scaling is needed (!= means not equal), if None or if the last screen size is different from the current one. That is why we need this code
    def draw(self, screen, fullscreen=False):
        if self.image is None or screen.get_size() != self._last_screen_size:
            self._update_scale(screen)                                        
        screen_w, screen_h = screen.get_size() # Get current screen size

        # Adjust bottom position depending on fullscreen
        if fullscreen:
            # Stick to bottom in fullscreen mode
            self.rect.midbottom = (screen_w // 2, screen_h)
        else:
            # Move up slightly in windowed mode (e.g., 19% of inventory height)
            offset = int(self.rect.height * 0.19)
            self.rect.midbottom = (screen_w // 2, screen_h - offset)

        screen.blit(self.image, self.rect)