import pygame as pg

class BallProjectile(pg.sprite.Sprite):
    def __init__(self, pos, direction, image, speed=0.5):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.pos = pg.Vector2(pos)
        self.direction = pg.Vector2(direction).normalize() # Normalize the direction vector
        self.speed = speed # pixel per millisecond

    def update(self, dt):
        self.pos += self.direction * self.speed * dt # Move the projectile in the direction at the specified speed
        self.rect.center = self.pos # Update the rectangle position based on the new position

        # Check if the projectile is out of bounds and remove it
        if (self.rect.right < 0 or self.rect.left > 5000 or 
            self.rect.bottom < 0 or self.rect.top > 3000):
            self.kill()