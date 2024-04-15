import json
import random
import time
import pyglet
from pyglet.window import key
from pyglet.gl import *
from player import create_player, update_player, get_player_pikemnon, add_random_item
from entity import draw_entity
from camera import set_camera_target, set_camera_window_size, update_camera, begin_camera, end_camera
from mapp import create_map_sprites, what_tile_is_player_on, set_current_map, get_current_map
from conf import SCALE, WINDOW_WIDTH, WINDOW_HEIGHT
import maps as mps
from npc import create_npc, update_npc
from fighting import fighting_screen, handle_item, player_attack, next_turn
from game_state import get_fight_status, end_fight, start_fight

# Window dimensions
window_width = WINDOW_WIDTH*SCALE
window_height = WINDOW_HEIGHT*SCALE

last_fight_time = 0

# Create a window
window = pyglet.window.Window(window_width, window_height, "Pikemnon")

player = create_player('assets/player.png', window.width//2, window.height//2)

with open('npcs.json') as f:
    data = json.load(f)

outside_npcs = []
for i, npc_data in enumerate(data):  # Generate a unique ID
    npc = create_npc(npc_data['image'], npc_data['x'], npc_data['y'], npc_data['direction'], npc_data['pikemnons'])
    outside_npcs.append(npc)

set_current_map(mps.starter_map)

map_sprites = create_map_sprites()

fighting_menu_state = 'main'  # 'main' or 'attack'
selected_menu_option_index = 0
menu_options = ["Attack", "Item", "Run", "Swap"]
attack_options = None
inventory_options = None
menu_direction = None  # Default value indicating no direction

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
    global menu_direction, fighting_menu_state, selected_menu_option_index, menu_options, attack_options, player
    fighton = get_fight_status()
    
    if not fighton:
        handle_non_fighting_key_press(symbol)
    else:
        handle_fighting_key_press(symbol)

def handle_non_fighting_key_press(symbol):
    # Ensure that each direction is evaluated independently
    if symbol == key.W:
        key_state['up'] = True
    if symbol == key.S:
        key_state['down'] = True
    if symbol == key.A:
        key_state['left'] = True
    if symbol == key.D:
        key_state['right'] = True
    wild_encounter()


def handle_fighting_key_press(symbol):
    global selected_menu_option_index, fighting_menu_state

    grid_columns = 2
    if symbol == key.SPACE:
        process_space_key()
    elif symbol in [key.W, key.UP]:
        selected_menu_option_index = (selected_menu_option_index - 2) % len(menu_options)
    elif symbol in [key.S, key.DOWN]:
        selected_menu_option_index = (selected_menu_option_index + 2) % len(menu_options)
    elif symbol in [key.A, key.LEFT]:
        if selected_menu_option_index % grid_columns > 0:
            selected_menu_option_index -= 1
    elif symbol in [key.D, key.RIGHT]:
        if selected_menu_option_index % grid_columns < grid_columns - 1:
            selected_menu_option_index += 1

def process_space_key():
    global fighting_menu_state, selected_menu_option_index

    if fighting_menu_state == 'main':
        if selected_menu_option_index == 0:
            fighting_menu_state = 'attack'
        elif selected_menu_option_index == 1:
            fighting_menu_state = 'inventory'
        selected_menu_option_index = 0
    elif fighting_menu_state == 'attack':
        player_atk = player_attack(attack_options[selected_menu_option_index])
        handle_attack_result(player_atk)
    elif fighting_menu_state == 'inventory':
        handle_item(inventory_options[selected_menu_option_index], player)
        player[inventory_options[selected_menu_option_index]] -= 1
        fighting_menu_state = 'main'

def handle_attack_result(player_atk):
    global fighting_menu_state, selected_menu_option_index

    if player_atk == "player":
        end_fight()
        random_item = add_random_item(player)
        print(f"Player won! You got a {random_item}")
        return
    fighting_menu_state = 'main'
    if player_atk == "no pp":
        fighting_menu_state = 'attack'
        return
    selected_menu_option_index = 0
    if player_atk != "no pp" and next_turn() == "npc":
        end_fight()

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


def wild_encounter():
    global last_fight_time
    figt_chance = 0.1
    playerTile = what_tile_is_player_on(player)
    if time.time() - last_fight_time > 5 and not get_fight_status() and playerTile == "Tall Grass" and random.random() < figt_chance:
        start_fight("wild")
        last_fight_time = time.time()


def update(dt):
    # Update the player
    old_x, old_y = player['sprite'].x, player['sprite'].y
    update_player(player, dt, key_state)

    current_map = get_current_map()
    if current_map == mps.outside_map:
        for npc in outside_npcs:
            update_npc(npc, player)

    playerTile = what_tile_is_player_on(player)
    global last_player_tile
    if playerTile:
        if playerTile == "Nothing":
            player['sprite'].x, player['sprite'].y = old_x, old_y
        if playerTile == "Door":
            set_current_map(mps.outside_map)
            global map_sprites, map_overlay, overlay_batch
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
        draw_entity(player)
        if current_map == mps.outside_map:
            for npc in outside_npcs:
                draw_entity(npc)
        
        
        end_camera()
    elif fighton:
        global menu_direction, attack_options, inventory_options
        inventory_options = ['pikeball', 'better pikeball', 'potion', 'better potion']
        attack_options = list(get_player_pikemnon(player['pikemnons'])['moves'].keys())
        
        menu_options_dict = {
            'attack': attack_options,
            'inventory': inventory_options,
            'main': menu_options
        }

        current_menu_options = menu_options_dict[fighting_menu_state]

        fighting_screen(window, player, menu_direction, current_menu_options, selected_menu_option_index, fighting_menu_state)
        menu_direction = None  # Reset after use to avoid unintended navigation


if __name__ == '__main__':
    pyglet.app.run()
