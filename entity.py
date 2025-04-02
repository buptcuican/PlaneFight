import pygame
import random
from pygame.math import Vector2


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction, damage):
        super().__init__()
        self.image = pygame.Surface((4, 8))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=position)
        self.speed = 10
        self.direction = direction
        self.damage = damage

    def update(self, *args):
        self.rect.y += self.direction * self.speed
        if self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height():
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_path, hp, speed, score):
        self.score = score
        super().__init__()
        from resource_manager import get_scaled_image
        self.image = get_scaled_image(image_path, 100)
        screen = pygame.display.get_surface()
        screen_width = screen.get_width()
        self.rect = self.image.get_rect(center=(random.randint(50, screen_width - 50), -50))
        self.hp = hp
        self.speed = speed
        self.last_shot = pygame.time.get_ticks()

    def take_damage(self, damage):
        self.hp -= damage
        return self.hp <= 0

    def update(self, *args):
        self.rect.y += self.speed
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()

class Meteor(Enemy):
    def __init__(self):
        super().__init__('resources/meteorite.png', 100, 3, 100)

class EnemyPlane(Enemy):
    def __init__(self):
        super().__init__('resources/enemy.png', 30, 5, 30)
        self.move_vector = Vector2(random.choice([-1, 0, 1]), 1).normalize()
        self.shoot_interval = 1500

    def update(self, *args):
        self.rect.x += int(self.move_vector.x * self.speed)
        self.rect.y += int(self.move_vector.y * self.speed)
        
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_interval:
            self.last_shot = now
            return Bullet(self.rect.center, 1, 10)
        
        if self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_width():
            self.kill()