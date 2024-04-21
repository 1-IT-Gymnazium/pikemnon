import json
import random
import time
import pyglet
from pyglet.window import key
from pyglet.gl import *
from main_menu import create_menu_labels, draw_menu, get_selected_action, update_selection
from player import change_active_pikemnon, create_player, update_player, get_player_pikemnon, add_random_item
from entity import draw_entity
from camera import set_camera_target, set_camera_window_size, update_camera, begin_camera, end_camera
from mapp import create_map_sprites, what_tile_is_player_on, set_current_map, get_current_map
from conf import SCALE, WINDOW_WIDTH, WINDOW_HEIGHT
import maps as mps
from npc import create_npc, update_npc
from fighting import fighting_screen, handle_item, npc_attack, player_attack, set_text_to_display
from game_state import get_display_text, get_fight_stat, get_fight_status, end_fight, get_main_menu, set_fight_stat, set_main_menu, start_fight
from settings_menu import adjust_volume, create_volume_labels, draw_settings, update_settings_selection

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

create_menu_labels(window)
create_volume_labels(window)

fighting_menu_state = 'main'  # 'main' or 'attack'
selected_menu_option_index = 0
menu_options = ["Attack", "Item", "Run", "Swap"]
attack_options = None
inventory_options = None
menu_direction = None  # Default value indicating no direction
change_options = None

set_camera_target(player)
set_camera_window_size(window_width, window_height)

key_state = {
    'up': False,
    'down': False,
    'left': False,
    'right': False
}

menu_direction = None

fight_status = None

@window.event
def on_key_press(symbol: int, modifier: int) -> None:
    """
    Handles the key press event in the game.

    This function takes the key symbol and modifier and modifies the game state based on the key pressed.
    It handles navigation and selection in the main menu and options menu, adjusts the volume,
    and handles key presses during fighting and non-fighting game states.

    Parameters:
    symbol (int): The key symbol of the pressed key.
    modifier (int): The modifier key pressed along with the symbol key.

    Returns:
    None
    """
    global menu_direction, fighting_menu_state, selected_menu_option_index, menu_options, attack_options, player
    if get_fight_stat() != "text":
        fighton = get_fight_status()
        main_menu = get_main_menu()
        if main_menu == "main":
            if symbol == key.W or symbol == key.UP:
                update_selection('up')
            elif symbol == key.S or symbol == key.DOWN:
                update_selection('down')
            elif symbol == key.SPACE:
                action = get_selected_action()
                if action == 'Start Game':
                    set_main_menu(None)
                elif action == "Options":
                    set_main_menu('options')
                elif action == 'Exit':
                    pyglet.app.exit()
        elif main_menu == "options":
            if symbol == pyglet.window.key.W:
                update_settings_selection('up')
            elif symbol == pyglet.window.key.S:
                update_settings_selection('down')
            elif symbol == pyglet.window.key.A:
                adjust_volume('decrease')
            elif symbol == pyglet.window.key.D:
                adjust_volume('increase')
            elif symbol == pyglet.window.key.Q:
                set_main_menu('main')
        elif not fighton:
            handle_non_fighting_key_press(symbol)
        else:
            handle_fighting_key_press(symbol)

def handle_non_fighting_key_press(symbol: int) -> None:
    """
    Handles the key press event in the non-fighting game state.

    This function takes the key symbol and modifies the key_state dictionary based on the key pressed.
    It handles navigation in the game world by setting the appropriate direction to True in the key_state dictionary.
    It also checks for wild encounters after each key press.

    Parameters:
    symbol (int): The key symbol of the pressed key.

    Returns:
    None
    """
    if symbol == key.W:
        key_state['up'] = True
    if symbol == key.S:
        key_state['down'] = True
    if symbol == key.A:
        key_state['left'] = True
    if symbol == key.D:
        key_state['right'] = True
    wild_encounter()


def handle_fighting_key_press(symbol: int) -> None:
    """
    Handles the key press event in the fighting game state.

    This function takes the key symbol and modifies the selected menu option index and the fighting menu state
    based on the key pressed. It handles navigation and selection in the fighting menu.

    Parameters:
    symbol (int): The key symbol of the pressed key.

    Returns:
    None
    """
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

def process_space_key() -> None:
    global fighting_menu_state, selected_menu_option_index, player

    if get_fight_stat() != "text":
        if fighting_menu_state == 'main':
            process_main_menu()
        elif fighting_menu_state == 'attack':
            process_attack_menu()
        elif fighting_menu_state == 'inventory':
            process_inventory_menu()
        elif fighting_menu_state == 'change':
            process_change_menu()

def process_main_menu() -> None:
    global fighting_menu_state, selected_menu_option_index
    menu_actions = {
        0: 'attack',
        1: 'inventory',
        2: 'run',
        3: 'change'
    }
    fighting_menu_state = menu_actions.get(selected_menu_option_index, fighting_menu_state)
    if fighting_menu_state == 'run':
        set_text_to_display("You ran away!")
        set_fight_stat('end')
        selected_menu_option_index = 0
        fighting_menu_state = 'main'
    selected_menu_option_index = 0

def process_attack_menu() -> None:
    global player
    player_attack(attack_options[selected_menu_option_index])


def process_inventory_menu() -> None:
    global fighting_menu_state, player, selected_menu_option_index
    player_pikemnons = len(player['pikemnons'])
    handle_item(inventory_options[selected_menu_option_index], player)
    new_player_pikemnons = len(player['pikemnons'])
    fighting_menu_state = 'main'
    if new_player_pikemnons > player_pikemnons:
        selected_menu_option_index = 0
        set_fight_stat('end')

def process_change_menu() -> None:
    global fighting_menu_state, selected_menu_option_index, player
    # Retrieve the UUID of the selected Pikemnon from the menu options
    pikemnon_uuid = change_options[selected_menu_option_index]

    # Find the Pikemnon with the matching UUID
    pikemnon = next((p for p in player['pikemnons'] if p['id'] == pikemnon_uuid), None)
    
    # If no Pikemnon was found or the selected Pikemnon has 0 health, exit the function
    if pikemnon is None or pikemnon['current_health'] <= 0:
        return

    # Change the active Pikemnon to the selected one using its UUID
    player = change_active_pikemnon(player, pikemnon_uuid)
    
    # Reset the state and selection index
    fighting_menu_state = 'main'
    selected_menu_option_index = 0



def handle_attack_result() -> None:
    global fighting_menu_state, selected_menu_option_index

    fight_stat = get_fight_stat()

    if fight_stat == 'continue' or fighting_menu_state == 'change' or fight_stat == "text":
        return
    elif fight_stat == "attacked":
        npc_attack()
        set_fight_stat('continue')
    elif fight_stat == "player":
        end_fight()
        fighting_menu_state = 'main'
        return
    fighting_menu_state = 'main'
    if fight_stat == "no pp":
        fighting_menu_state = 'attack'
        return
    selected_menu_option_index = 0
    if fight_stat == "npc":
        for pikemnon in player['pikemnons']:
            if pikemnon['current_health'] > 0:
                fighting_menu_state = 'change'
                set_fight_stat('continue')
                return
        set_fight_stat(None)
        end_fight()
        fighting_menu_state = 'main'
    elif fight_stat == "change":
        fighting_menu_state = 'change'
        set_fight_stat('continue')
    elif fight_stat == "end":
        end_fight()
        set_fight_stat(None)

@window.event
def on_key_release(symbol: int, _) -> None:
    if symbol == key.W:
        key_state['up'] = False
    elif symbol == key.S:
        key_state['down'] = False
    elif symbol == key.A:
        key_state['left'] = False
    elif symbol == key.D:
        key_state['right'] = False


def wild_encounter() -> None:
    global last_fight_time
    figt_chance = 0.1
    playerTile = what_tile_is_player_on(player)
    if time.time() - last_fight_time > 5 and not get_fight_status() and playerTile == "Tall Grass" and random.random() < figt_chance:
        start_fight("wild")
        last_fight_time = time.time()


def update(dt: float) -> None:
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
def on_draw() -> None:
    pyglet.gl.glClearColor(0, 0, 0, 1)
    window.clear()
    fighton = get_fight_status()
    main_menu = get_main_menu()
    if main_menu == 'main':
        draw_menu(window)
    elif main_menu == 'options':
        draw_settings(window)
    elif not fighton:
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
        global menu_direction, attack_options, inventory_options, change_options
        inventory_options = ['pikeball', 'better pikeball', 'potion', 'better potion']
        attack_options = list(get_player_pikemnon(player['pikemnons'])['moves'].keys())
        change_options = list(pikemnon['id'] for pikemnon in player['pikemnons'])
        
        menu_options_dict = {
            'attack': attack_options,
            'inventory': inventory_options,
            'main': menu_options,
            "change": change_options
        }

        current_menu_options = menu_options_dict[fighting_menu_state]

        fighting_screen(window, player, menu_direction, current_menu_options, selected_menu_option_index, fighting_menu_state)
        menu_direction = None  # Reset after use to avoid unintended navigation

        handle_attack_result()


if __name__ == '__main__':
    pyglet.app.run()
