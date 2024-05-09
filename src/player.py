import json
from data.pikemnon_data import get_pikemnon_data
from data.player_data import get_player_data
from src.entity import create_entity
import random
import uuid


def create_player(x, y, speed=220):
    """
    Creates a player entity at the specified coordinates with the specified speed.

    :param x: The x-coordinate of the player.
    :type x: int
    :param y: The y-coordinate of the player.
    :type y: int
    :param speed: The speed of the player, defaults to 220.
    :type speed: int, optional
    :return: The player entity.
    :rtype: dict
    """
    player = create_entity("assets/player.png", x, y)
    player['speed'] = speed
    player['canMove'] = True
    data = get_player_data()
    player_pikemnons = data['inventory']['pikemnons']
    pikemnons = []
    pokemon_data = get_pikemnon_data()
    for x, pikemnon in enumerate(player_pikemnons):
        pikemnon = pokemon_data[pikemnon['name']]
        pikemnon['current_health'] = pikemnon['health']
        pikemnon['stage'] = {}
        pikemnon['stage']['attack'] = 0
        pikemnon['stage']['defense'] = 0
        pikemnon['name'] = player_pikemnons[x]['name']
        pikemnon['active'] = True if x == 0 else False
        pikemnon['id'] = str(uuid.uuid4())
        pikemnons.append(pikemnon)
    player['pikemnons'] = pikemnons
    player['potion'] = 5
    player['pikeball'] = 5
    player['better pikeball'] = 5
    player['better potion'] = 0
    return player


def update_player(player: dict[str, any], dt: float, key_state: dict[str, bool]):
    """
    Updates the player's position based on the current key state.

    :param player: The player entity.
    :type player: dict
    :param dt: The time delta.
    :type dt: float
    :param key_state: The current key state.
    :type key_state: dict
    :return: None
    """
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
    """
    Changes the player's movement status.

    :param player: The player entity.
    :type player: dict
    :param can: Whether the player can move.
    :type can: bool
    :return: None
    """
    player['canMove'] = can

def get_player_pikemnon(player_inventory):
    """
    Returns the active Pikemnon from the player's inventory.

    :param player_inventory: The player's inventory.
    :type player_inventory: list
    :return: The active Pikemnon.
    :rtype: dict
    """
    for pikemnon in player_inventory:
        if pikemnon['active'] == True:
            return pikemnon

def add_random_item(player):
    """
    Adds a random item to the player's inventory.

    :param player: The player entity.
    :type player: dict
    :return: The added item.
    :rtype: str
    """
    random_items = ['pikeball', 'better pikeball', 'potion', 'better potion']
    probabilities = [0.4, 0.1, 0.4, 0.1]
    cumulative_probabilities = [sum(probabilities[:i+1]) for i in range(len(probabilities))]

    rand = random.random()
    for i, cumulative_probability in enumerate(cumulative_probabilities):
        if rand < cumulative_probability:
            item = random_items[i]
            break

    player[item] += 1
    return item

def change_active_pikemnon(player: dict[str, any], pikemnon_id: str) -> dict[str, any]:
    """
    Changes the active Pikemnon in the player's inventory.

    :param player: The player entity.
    :type player: dict
    :param pikemnon_id: The ID of the Pikemnon to activate.
    :type pikemnon_id: str
    :return: The updated player entity.
    :rtype: dict
    """
    
    for pikemnon in player['pikemnons']:
        if pikemnon['id'] == pikemnon_id:
            pikemnon['active'] = True
        else:
            pikemnon['active'] = False
    return player

def remove_pikemnon(player: dict[str, any], pikemnon_id: str) -> dict[str, any]:
    """
    Removes a Pikemnon from the player's inventory.

    :param player: The player entity.
    :type player: dict
    :param pikemnon_id: The ID of the Pikemnon to remove.
    :type pikemnon_id: str
    :return: The updated player entity.
    :rtype: dict
    """
    for pikemnon in player['pikemnons']:
        if pikemnon['id'] == pikemnon_id:
            player['pikemnons'].remove(pikemnon)
            break