import pyglet
from pyglet.gl import *
from conf import SCALE

current_map = None

# Load the tile images
tile_images = {
    0: pyglet.resource.image('assets/empty.png'),
    1: pyglet.resource.image('assets/floor.png'),
    2: pyglet.resource.image('assets/door_2.png'),
    3: pyglet.resource.image('assets/grass.png')
}

# Define a list to hold the map sprites
map_sprites = []


# Define a function to create the map sprites
def create_map_sprites():
    for y, row in enumerate(current_map):
        for x, tile in enumerate(row):
            image = tile_images[tile]
            texture = image.get_texture()
            glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            sprite = pyglet.sprite.Sprite(img=image, x=x*image.width*4,
                                          y=y*image.height*4)
            sprite.scale = 4
            map_sprites.append(sprite)
    return map_sprites


def set_current_map(cr_map):
    global current_map
    current_map = cr_map


TILE_WIDTH = 8
TILE_HEIGHT = 8


def what_tile_is_player_on(player):
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
    return None


def is_player_colliding_with_empty(player):
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
