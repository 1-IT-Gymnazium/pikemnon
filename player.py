import json
from entity import create_entity
import random


def create_player(image_file, x, y, speed=220):
    player = create_entity(image_file, x, y)
    player['speed'] = speed
    player['canMove'] = True
    with open('player.json') as f:
        data = json.load(f)
        player_pikemnons = data['inventory']['pikemnons']
        pikemnons = []
        with open('pokemon.json') as f:
            pokemon_data = json.load(f)
        for x, pikemnon in enumerate(player_pikemnons):
            pikemnon = pokemon_data[pikemnon['name']]
            pikemnon['current_health'] = pikemnon['health']
            pikemnon['stage'] = {}
            pikemnon['stage']['attack'] = 0
            pikemnon['name'] = player_pikemnons[x]['name']
            pikemnon['active'] = True if x == 0 else False
            pikemnons.append(pikemnon)
        player['pikemnons'] = pikemnons
        player['potion'] = 5
        player['pikeball'] = 5
        player['better pikeball'] = 0
        player['better potion'] = 0
    return player


def update_player(player: dict[str, any], dt: float, key_state: dict[str, bool]):
    if player['canMove']:
        dx = dy = 0
        if key_state['up']:
            dy += player['speed'] * dt
        if key_state['down']:
            dy -= player['speed'] * dt
        if key_state['left']:
            dx -= player['speed'] * dt
        if key_state['right']:
            dx += player['speed'] * dt

    # Normalize
        length = (dx**2 + dy**2)**0.5
        if length != 0:
            dx, dy = dx / length * player['speed'] * dt, dy / length * player['speed'] * dt

        player['sprite'].x += dx
        player['sprite'].y += dy


def change_move(player, can):
    player['canMove'] = can

def get_player_pikemnon(player_inventory):
    for pikemnon in player_inventory:
        if pikemnon['active'] == True:
            return pikemnon

def add_random_item(player):
    random_items = ['pikeball', 'better pikeball', 'potion', 'better potion']
    item = random.choice(random_items)
    player[item] += 1
    return item

def change_active_pikemnon(player: dict[str, any], pikemnon_name: str) -> dict[str, any]:
    for pikemnon in player['pikemnons']:
        if pikemnon['name'] == pikemnon_name:
            pikemnon['active'] = True
        else:
            pikemnon['active'] = False
    return player