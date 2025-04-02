import pygame
import sys
import os
import random
from pygame.locals import *
from entity import Bullet, EnemyPlane, Meteor

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        from resource_manager import get_scaled_image
        self.image = get_scaled_image('resources/player.png', 100)
        screen = pygame.display.get_surface()
        screen_width, screen_height = screen.get_size()
        self.rect = self.image.get_rect(midbottom=(screen_width // 2, screen_height))
        screen_rect = pygame.display.get_surface().get_rect()
        self.speed = 8
        self.hp = 100
        self.last_shot = pygame.time.get_ticks()

    def update(self, keys):
        screen_rect = pygame.display.get_surface().get_rect()
        
        # 使用浮点数坐标提升移动精度
        dx, dy = 0, 0
        if keys[K_LEFT]: dx -= self.speed
        if keys[K_RIGHT]: dx += self.speed
        if keys[K_UP]: dy -= self.speed
        if keys[K_DOWN]: dy += self.speed
        
        # 临时浮点坐标计算
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy
        
        # 应用边界约束
        self.rect.x = max(screen_rect.left, min(new_x, screen_rect.right - self.rect.width))
        self.rect.y = max(screen_rect.top, min(new_y, screen_rect.bottom - self.rect.height))

def main():
    pygame.init()
    # 获取显示器原生分辨率
    screen = pygame.display.set_mode(pygame.display.list_modes()[0], pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    player = Player()
    score = 0
    all_sprites = pygame.sprite.Group(player)
    enemy_group = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    ENEMY_SPAWN = pygame.USEREVENT + 1
    pygame.time.set_timer(ENEMY_SPAWN, 1500)

    running = True
    # 在主游戏循环中找到背景填充代码并修改
    while running:
        screen.fill((30, 30, 40))
        keys = pygame.key.get_pressed()
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == QUIT or keys[K_ESCAPE]:
                running = False
            if event.type == ENEMY_SPAWN:
                enemy = Meteor() if random.random() < 0.7 else EnemyPlane()
                all_sprites.add(enemy)
                enemy_group.add(enemy)

        # 玩家自动射击
        now = pygame.time.get_ticks()
        if now - player.last_shot > 300:
            player.last_shot = now
            new_bullet = Bullet((player.rect.centerx, player.rect.top - 10), -1, 20)
            player_bullets.add(new_bullet)
            all_sprites.add(new_bullet)

        # 处理事件
        for event in pygame.event.get():
            if event.type == ENEMY_SPAWN:
                enemy = Meteor() if random.random() < 0.5 else EnemyPlane()
                all_sprites.add(enemy)
                enemy_group.add(enemy)

        # 碰撞检测
        # 子弹与敌人的碰撞
        collisions = pygame.sprite.groupcollide(player_bullets, enemy_group, True, False)
        for bullet, enemies in collisions.items():
            for enemy in enemies:
                if enemy.take_damage(bullet.damage):
                    score += enemy.score
                    enemy.kill()

        # 玩家与敌人的碰撞
        for enemy in pygame.sprite.spritecollide(player, enemy_group, False):
            player.hp -= 20
            enemy.kill()

        # 更新游戏状态
        if player.hp <= 0:
            running = False

        all_sprites.update(keys)
        screen.fill((30, 30, 40))
        screen_width, screen_height = screen.get_size()
        border_rect = pygame.Rect(10, 10, screen_width - 20, screen_height - 20)
        pygame.draw.rect(screen, (255, 255, 0), border_rect, 5)
        all_sprites.draw(screen)

        # 绘制HP
        font = pygame.font.Font(None, 36)
        hp_text = font.render(f'HP: {player.hp}  Score: {score}', True, (255, 255, 255))
        screen.blit(hp_text, (20, 20))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


class Game:
    def __init__(self):
        from resource_manager import get_scaled_image
        self.player_img = get_scaled_image('resources/player.png', 100)
        self.enemy_img = get_scaled_image('resources/enemy.png', 100)
        self.meteorite_img = get_scaled_image('resources/meteorite.png', 100)
import sys
import os