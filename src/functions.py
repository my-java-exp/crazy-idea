import pygame
from src.defaults import DEFAULT_REWARD

def collision_check(obj1: pygame.Rect, obj2: pygame.Rect):
    if obj1.colliderect(obj2):
        return DEFAULT_REWARD
    else:
        return 0