import pygame
from src.defaults import DEFAULT_REWARD, DEFAULT_K
from src.game_objects import StrappedObject

def collision_check(obj1: pygame.Rect, obj2: pygame.Rect):
    if obj1.colliderect(obj2):
        return DEFAULT_REWARD
    else:
        return 0

def check_best(network_list: list[StrappedObject], k: int=DEFAULT_K):

    #START

    # Only store 2 values(e.g 2 objects, 2 idx, 2 rewards)
    best_networks: dict[int, StrappedObject] = {} 
    best_networks_list = []
    best_rewards = [0, 0] 

    #END
    
    for idx, net in enumerate(network_list):

        for idx, reward in enumerate(best_rewards):
            if net.collected_rewards > reward:
                best_rewards[idx] = net.collected_rewards
                best_networks[idx] = net
                best_networks_list.append(net)
            

def spread_inheritance(network_list: list[StrappedObject]): ...