import pyglet
from pyglet.gl import *
from conf import SCALE

current_map = None

tile_images = {}

# Load the tile images
def load_tile_images():
    """
    Returns the action associated with the currently selected menu item.

    :return: The action associated with the currently selected menu item.
    :rtype: str

    :Global Variables: 
        * selected_index (int): The index of the currently selected menu item.
        * menu_items (list): The list of menu items.
    """
    global tile_images
    tile_images = {
        0: pyglet.resource.image('assets/empty.png'),
        1: pyglet.resource.image('assets/floor.png'),
        2: pyglet.resource.image('assets/door_2.png'),
        3: pyglet.resource.image('assets/grass.png'),
        4: pyglet.resource.image('assets/tall-grass-tl.png'),
        5: pyglet.resource.image('assets/tall-grass-tr.png'),
        6: pyglet.resource.image('assets/tall-grass-bl.png'),
        7: pyglet.resource.image('assets/tall-grass-br.png'),
    }

# Define a list to hold the map sprites
map_sprites = []


# Define a function to create the map sprites
def create_map_sprites():
    """
    Returns the action associated with the currently selected menu item.

    :return: The action associated with the currently selected menu item.
    :rtype: str

    :Global Variables: 
        * selected_index (int): The index of the currently selected menu item.
        * menu_items (list): The list of menu items.
    """

    for y, row in enumerate(current_map):
        for x, tile in enumerate(row):
            image = tile_images[tile]
            texture = image.get_texture()
            glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            sprite = pyglet.sprite.Sprite(img=image, x=x*image.width*4,
                                          y=y*image.height*4)
            sprite.scale = 4
            if map and tile == 0:
                sprite.opacity = 0
            map_sprites.append(sprite)
    return map_sprites


def set_current_map(cr_map):
    """
    Returns the action associated with the currently selected menu item.

    :return: The action associated with the currently selected menu item.
    :rtype: str

    :Global Variables: 
        * selected_index (int): The index of the currently selected menu item.
        * menu_items (list): The list of menu items.
    """
    global current_map
    current_map = cr_map


def get_current_map():
    """
    Returns the current map.

    :return: The current map.
    :rtype: list

    :Global Variables: 
        * current_map (list): The current map.
    """
    return current_map


TILE_WIDTH = 8
TILE_HEIGHT = 8


def what_tile_is_player_on(player):
    """
    Determines what type of tile the player is currently on.

    This function calculates the player's tile coordinates and checks all tiles the player is on. It returns a string representing the type of tile the player is on.

    :param player: The player.
    :type player: dict
    :return: The type of tile the player is on.
    :rtype: str

    :Global Variables: 
        * current_map (list): The current map.
    """
    # Calculate the player's tile coordinates
    player_tile_x = int(player['sprite'].x // (TILE_WIDTH * SCALE))
    player_tile_y = int((player['sprite'].y) // (TILE_HEIGHT * SCALE))

    # Calculate the number of tiles the player spans
    player_tiles_x = (player['sprite'].width // (TILE_WIDTH * SCALE)) + 1
    player_tiles_y = (player['sprite'].height // (TILE_HEIGHT * SCALE))

    # Check all tiles the player is on
    for y in range(player_tile_y, player_tile_y + player_tiles_y):
        for x in range(player_tile_x, player_tile_x + player_tiles_x):
            player_in_map = 0 <= len(current_map) and 0 <= x < len(current_map[0])

            if player_in_map:
                if current_map[y][x] == 0:
                    return "Nothing"
                elif current_map[y][x] == 2:
                    return "Door"
                elif current_map[y][x] == 3:
                    return "Grass"
                if current_map[y][x] in [4, 5, 6, 7]:
                    return "Tall Grass"
    return None


def is_player_colliding_with_empty(player):
    """
    Determines if the player is colliding with an empty tile.

    This function calculates the player's tile coordinates and checks all tiles the player is on. If the player is on an empty tile, it returns True. Otherwise, it returns False.

    :param player: The player.
    :type player: dict
    :return: Whether the player is colliding with an empty tile.
    :rtype: bool

    :Global Variables: 
        * current_map (list): The current map.
    """
    # Calculate the player's tile coordinates
    player_tile_x = int(player['sprite'].x // (TILE_WIDTH * SCALE))
    player_tile_y = int(player['sprite'].y // (TILE_HEIGHT * SCALE))

    # Calculate the number of tiles the player spans
    player_tiles_x = (player['sprite'].width // (TILE_WIDTH * SCALE)) + 1
    player_tiles_y = (player['sprite'].height // (TILE_HEIGHT * SCALE)) + 1

    # Check all tiles the player is on
    for y in range(player_tile_y, player_tile_y + player_tiles_y):
        for x in range(player_tile_x, player_tile_x + player_tiles_x):
            # If the tile is an empty tile, there's a collision
            if (0 <= y < len(current_map) and 0 <= x < len(current_map[0]) and current_map[y][x] == 0):
                return True

    # No collision
    return False
