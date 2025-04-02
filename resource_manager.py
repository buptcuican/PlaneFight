import pygame
import sys
import os

def get_scaled_image(relative_path, max_size):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    full_path = os.path.join(base_path, relative_path)
    original_image = pygame.image.load(full_path).convert_alpha()
    
    # 保持宽高比的缩放逻辑
    original_width, original_height = original_image.get_size()
    if original_width > original_height:
        new_width = max_size
        new_height = int(original_height * (max_size / original_width))
    else:
        new_height = max_size
        new_width = int(original_width * (max_size / original_height))
    
    return pygame.transform.smoothscale(original_image, (new_width, new_height))