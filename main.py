import pyglet
from pyglet.window import key
from pyglet.gl import *
from player import create_player, update_player
from entity import draw_entity
from camera import set_camera_target, set_camera_window_size, update_camera, begin_camera, end_camera
from mapp import create_map_sprites, what_tile_is_player_on, set_current_map, get_current_map
from conf import SCALE, WINDOW_WIDTH, WINDOW_HEIGHT
import maps as mps
from npc import create_npc, update_npc
from fighting import fighting_screen
from game_state import get_fight_status

# Window dimensions
window_width = WINDOW_WIDTH*SCALE
window_height = WINDOW_HEIGHT*SCALE

# Create a window
window = pyglet.window.Window(window_width, window_height, "Pikemnon")

player = create_player('assets/player.png', window.width//2, window.height//2)
out_npc = create_npc('assets/player.png', 500, 300, 'left')
outside_npcs = [out_npc]

set_current_map(mps.starter_map)

map_sprites = create_map_sprites()

set_camera_target(player)
set_camera_window_size(window_width, window_height)

key_state = {
    'up': False,
    'down': False,
    'left': False,
    'right': False
}

menu_direction = None

@window.event
def on_key_press(symbol, modifiers):
    fighton = get_fight_status()
    if not fighton:
        if symbol == key.W:
            key_state['up'] = True
        elif symbol == key.S:
            key_state['down'] = True
        elif symbol == key.A:
            key_state['left'] = True
        elif symbol == key.D:
            key_state['right'] = True
    elif fighton:
        global menu_direction
        if symbol == key.W:
            menu_direction = "up"
        elif symbol == key.S:
            menu_direction = "down"
        elif symbol == key.A:
            menu_direction = "left"
        elif symbol == key.D:
            menu_direction = "right"


@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.W:
        key_state['up'] = False
    elif symbol == key.S:
        key_state['down'] = False
    elif symbol == key.A:
        key_state['left'] = False
    elif symbol == key.D:
        key_state['right'] = False


def update(dt):
    # Update the player
    old_x, old_y = player['sprite'].x, player['sprite'].y
    update_player(player, dt, key_state)

    current_map = get_current_map()
    if current_map == mps.outside_map:
        for npc in outside_npcs:
            update_npc(npc, player)

    playerTile = what_tile_is_player_on(player)
    if playerTile:
        if playerTile == "Nothing":
            player['sprite'].x, player['sprite'].y = old_x, old_y
        if playerTile == "Door":
            set_current_map(mps.outside_map)
            global map_sprites
            map_sprites = create_map_sprites()

    update_camera()

pyglet.clock.schedule_interval(update, 1/60.0)


@window.event
def on_draw():
    window.clear()
    fighton = get_fight_status()
    if not fighton:
        begin_camera()
        for sprite in map_sprites:
            sprite.draw()
        current_map = get_current_map()
        if current_map == mps.outside_map:
            for npc in outside_npcs:
                draw_entity(npc)
        draw_entity(player)
        end_camera()
    elif fighton:
        global menu_direction
        fighting_screen(window, menu_direction)
        menu_direction = None


if __name__ == '__main__':
    pyglet.app.run()
