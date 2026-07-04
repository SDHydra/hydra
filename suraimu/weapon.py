import os
import pygame as pg

class Weapon:
    def __init__(self, sprite_dir, frame_count=7, scale_factor=2, animation_speed=70):
        self.scale_factor = scale_factor
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = animation_speed
        self.attacking = False
        self.attacking_left = False
        self.hit_enemies = set()  # Track enemies hit during current attack

        # Load frames (right-facing and flipped for left)
        base_dir = os.path.dirname(__file__)
        full_dir = os.path.join(base_dir, sprite_dir)
        self.frames_right = []
        for i in range(1, frame_count + 1):
            path = os.path.join(full_dir, f"Sword_Fight_Animation{i}.png")
            image = pg.image.load(path).convert_alpha()
            image = pg.transform.scale(
                image,
                (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor))
            )
            self.frames_right.append(image)
        self.frames_left = [pg.transform.flip(f, True, False) for f in self.frames_right]

        self.image = self.frames_right[0]
        self.rect = self.image.get_rect()

    def attack(self, mouse_pos, player_rect, camera):
        if not self.attacking:
            self.attacking = True
            self.frame_index = 0
            self.animation_timer = 0
            self.attacking_left = mouse_pos[0] - camera.x < player_rect.centerx
            self.hit_enemies.clear()  # Reset hit enemies at the start of the attack

    def update(self, dt, player_rect, mouse_world_x, mouse_held):
        px, py = player_rect.center

        if not mouse_held:
            # Stop attacking if mouse released
            self.attacking = False
            self.frame_index = 0
            self.animation_timer = 0
            return

        # Update attack animation
        if self.attacking:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.frame_index += 1
                if self.frame_index >= len(self.frames_right):
                    if mouse_held:
                        self.frame_index = 0  # Loop attack if holding
                        self.hit_enemies.clear()  # Reset enemies for new swing
                    else:
                        self.attacking = False
                        self.frame_index = 0
                        self.hit_enemies.clear()

        # Position weapon
        if self.attacking:
            if self.attacking_left:
                base_image = self.frames_left[self.frame_index]
                weapon_x = px - int(35 * self.scale_factor)
            else:
                base_image = self.frames_right[self.frame_index]
                weapon_x = px + int(35 * self.scale_factor)
            weapon_y = py
            self.image = base_image
            self.rect = self.image.get_rect(center=(weapon_x, weapon_y))
        else:
            self.image = None
            self.rect = pg.Rect(0, 0, 0, 0)

    def draw(self, screen, camera):
        if self.attacking and self.image:
            screen.blit(self.image, (self.rect.x + camera.x, self.rect.y + camera.y))
