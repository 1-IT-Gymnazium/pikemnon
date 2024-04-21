"""The main game loop for Pikemnon."""

import json
import random
import time
import pyglet
from pyglet.window import key
from pyglet.gl import *
from data.npc_data import get_npcs_data
from src.main_menu import create_menu_labels, draw_menu, get_selected_action, update_selection
from src.player import change_active_pikemnon, create_player, update_player, get_player_pikemnon, add_random_item
from src.entity import draw_entity
from src.camera import set_camera_target, set_camera_window_size, update_camera, begin_camera, end_camera
from src.mapp import create_map_sprites, load_tile_images, what_tile_is_player_on, set_current_map, get_current_map
from conf import SCALE, WINDOW_WIDTH, WINDOW_HEIGHT
import src.maps as mps
from src.npc import create_npc, update_npc
from src.fighting import fighting_screen, handle_item, npc_attack, player_attack, set_text_to_display
from src.game_state import get_fight_stat, get_fight_status, end_fight, get_main_menu, set_fight_stat, set_main_menu, start_fight
from src.settings_menu import adjust_volume, create_volume_labels, draw_settings, update_settings_selection
from src.inventory import draw_inventory, remove_selected_pikemnon, select_selected_pikemnon, kill_pikemnon

# Window dimensions
window_width = WINDOW_WIDTH*SCALE
window_height = WINDOW_HEIGHT*SCALE

last_fight_time = 0

# Create a window
window = pyglet.window.Window(window_width, window_height, "Pikemnon")

player = None

outside_npcs = None

map_sprites = None

fighting_menu_state = 'main'  # 'main' or 'attack'
selected_menu_option_index = 0
menu_options = ["Attack", "Item", "Run", "Swap"]
attack_options = None
inventory_options = None
menu_direction = None  # Default value indicating no direction
change_options = None

inventory = False
kill_inventory = False
kill_index = 0
inventory_index = 0

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

    :param symbol: The key symbol of the pressed key.
    :type symbol: int
    :param modifier: The modifier key pressed along with the symbol key.
    :type modifier: int
    :return: None

    :Global Variables: 
        * menu_direction (str): The direction of the currently selected menu option.
        * fighting_menu_state (str): The current state of the fighting menu.
        * selected_menu_option_index (int): The index of the currently selected menu option.
        * menu_options (list): A list of the main menu options.
        * attack_options (list): A list of the player's current pikemnon's moves.
        * player (dict): The player object, which is a dictionary that includes a 'sprite' key and a 'pikemnons' key.
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

    :param symbol: The key symbol of the pressed key.
    :type symbol: int
    :return: None

    :Global Variables: 
        * key_state (dict): A dictionary that maps directions ('up', 'down', 'left', 'right') to booleans indicating whether the corresponding key is pressed.
    """
    global inventory, inventory_index, kill_inventory, kill_index

    if not inventory:
        if symbol == key.W:
            key_state['up'] = True
        if symbol == key.S:
            key_state['down'] = True
        if symbol == key.A:
            key_state['left'] = True
        if symbol == key.D:
            key_state['right'] = True
    elif inventory and not kill_inventory:
        if symbol in [key.W, key.UP]:
            inventory_index = (inventory_index - 2) % 4
        elif symbol in [key.S, key.DOWN]:
            inventory_index = (inventory_index + 2) % 4
        elif symbol in [key.A, key.LEFT]:
            if inventory_index % 2 > 0:
                inventory_index -= 1
        elif symbol in [key.D, key.RIGHT]:
            if inventory_index % 2 < 2 - 1:
                inventory_index += 1
        elif symbol == key.SPACE:
            select_selected_pikemnon(player['pikemnons'], inventory_index)
            kill_inventory = True
    elif kill_inventory:
        if symbol == key.A:
            kill_index = 0
        elif symbol == key.D:
            kill_index = 1
        elif symbol == key.SPACE:
            if kill_index == 0:
                kill_pikemnon(player)
                inventory = False
                kill_inventory = False
                kill_index = 0
                inventory_index = 0
            else:
                kill_inventory = False
                kill_index = 0
                remove_selected_pikemnon()
    if symbol == key.I:
        if inventory:
            inventory = False
            remove_selected_pikemnon()
            inventory_index = 0
        elif not inventory:
            inventory = True

    wild_encounter()


def handle_fighting_key_press(symbol: int) -> None:
    """
    Handles the key press event in the fighting game state.

    This function takes the key symbol and modifies the selected menu option index and the fighting menu state
    based on the key pressed. It handles navigation and selection in the fighting menu.

    :param symbol: The key symbol of the pressed key.
    :type symbol: int
    :return: None

    :Global Variables: 
        * selected_menu_option_index (int): The index of the currently selected menu option.
        * fighting_menu_state (str): The current state of the fighting menu.
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
    """
    Processes the action when the space key is pressed during a fight.

    This function checks the current state of the fighting menu and calls the appropriate function to process the action.
    The fighting menu state can be one of the following: 'main', 'attack', 'inventory', or 'change'.

    :return: None

    :Global Variables: 
        * fighting_menu_state (str): The current state of the fighting menu.
        * selected_menu_option_index (int): The index of the currently selected menu option.
        * player (Player): The player object.
    """
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
    """
    Processes the action when the space key is pressed during a fight.

    This function checks the current state of the fighting menu and calls the appropriate function to process the action.
    The fighting menu state can be one of the following: 'main', 'attack', 'inventory', or 'change'.

    :return: None

    :Global Variables: 
        * fighting_menu_state (str): The current state of the fighting menu.
        * selected_menu_option_index (int): The index of the currently selected menu option.
        * player (Player): The player object.
    """
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
    """
    Processes the action when an attack option is selected from the attack menu during a fight.

    This function calls the player_attack function with the attack corresponding to the selected menu option.

    :param None
    :return: None

    :Global Variables: 
        * player (Player): The player object.
        * selected_menu_option_index (int): The index of the currently selected menu option.
    """
    global player
    player_attack(attack_options[selected_menu_option_index])


def process_inventory_menu() -> None:
    """
    Processes the action when an attack option is selected from the attack menu during a fight.

    This function calls the player_attack function with the attack corresponding to the selected menu option.

    :param None
    :return: None

    :Global Variables: 
        * player (Player): The player object.
        * selected_menu_option_index (int): The index of the currently selected menu option.
    """
    global fighting_menu_state, player, selected_menu_option_index
    player_pikemnons = len(player['pikemnons'])
    handle_item(inventory_options[selected_menu_option_index], player)
    new_player_pikemnons = len(player['pikemnons'])
    fighting_menu_state = 'main'
    if new_player_pikemnons > player_pikemnons:
        selected_menu_option_index = 0
        set_fight_stat('end')

def process_change_menu() -> None:
    """
    Processes the action when a pikemnon is selected from the change menu during a fight.

    This function changes the active pikemnon to the one corresponding to the selected menu option, if it is valid and has more than 0 health.
    After changing the active pikemnon, it resets the selected menu option index and changes the fighting menu state to 'main'.

    :param None:
    :return: None

    :Global Variables: 
        * fighting_menu_state (str): The current state of the fighting menu.
        * player (dict): The player object, which is a dictionary that includes a 'pikemnons' key.
        * selected_menu_option_index (int): The index of the currently selected menu option.
    """
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
    """
    Handles the result of an attack during a fight.

    This function checks the current fight status and performs the appropriate action.
    If the fight status is 'continue', 'change', or 'text', it returns without doing anything.
    If the fight status is 'attacked', it calls the npc_attack function and sets the fight status to 'continue'.
    If the fight status is 'player', it ends the fight and resets the fighting menu state to 'main'.
    If the fight status is 'no pp', it changes the fighting menu state to 'attack'.
    If the fight status is 'npc', it checks if there is a pikemnon with more than 0 health and changes the fighting menu state to 'change' if there is one, or ends the fight if there isn't.
    If the fight status is 'change', it changes the fighting menu state to 'change'.
    If the fight status is 'end', it ends the fight.

    :param None:
    :return: None

    :Global Variables: 
        * fighting_menu_state (str): The current state of the fighting menu.
        * player (dict): The player object, which is a dictionary that includes a 'pikemnons' key.
        * selected_menu_option_index (int): The index of the currently selected menu option.
    """
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
def on_key_release(symbol: int, _: int) -> None:
    """
    Checks if a wild encounter should occur and starts a fight if necessary.

    This function checks if the player is on a "Tall Grass" tile, if at least 5 seconds have passed since the last fight, 
    if there is not currently a fight ongoing, and if a random number is less than the fight chance (0.1).
    If all these conditions are met, it starts a wild fight and updates the last fight time.

    :param None:
    :return: None

    :Global Variables: 
        * last_fight_time (float): The time when the last fight occurred.
        * player (dict): The player object, which is a dictionary that includes a 'position' key.
    """
    if symbol == key.W:
        key_state['up'] = False
    elif symbol == key.S:
        key_state['down'] = False
    elif symbol == key.A:
        key_state['left'] = False
    elif symbol == key.D:
        key_state['right'] = False


def wild_encounter() -> None:
    """
    Checks if a wild encounter should occur and starts a fight if so.

    This function checks if the player is on a "Tall Grass" tile, if at least 5 seconds have passed since the last fight, 
    if there is not currently a fight ongoing, and if a random number is less than the fight chance (0.1).
    If all these conditions are met, it starts a wild fight and updates the last fight time.

    :param None:
    :return: None

    :Global Variables: 
        * last_fight_time (float): The time when the last fight occurred.
        * player (dict): The player object, which is a dictionary that includes a 'position' key.
    """
    global last_fight_time
    figt_chance = 0.1
    playerTile = what_tile_is_player_on(player)
    if time.time() - last_fight_time > 5 and not get_fight_status() and playerTile == "Tall Grass" and random.random() < figt_chance:
        start_fight("wild")
        last_fight_time = time.time()


def update(dt: float) -> None:
    """
    Updates the game state based on the elapsed time since the last frame.

    This function updates the player's position based on the current key state, updates the NPCs if the current map is the outside map, 
    checks the tile the player is on and performs the appropriate action (e.g., prevents the player from moving onto a "Nothing" tile, 
    changes the current map to the outside map if the player is on a "Door" tile), and updates the camera.

    :param dt: The time elapsed since the last frame.
    :type dt: float

    :global player: The player object, which is a dictionary that includes a 'sprite' key.
    :global key_state: A dictionary that maps directions ('up', 'down', 'left', 'right') to booleans indicating whether the corresponding key is pressed.
    :global last_player_tile: The type of the tile the player was on in the last frame.
    :global map_sprites: A list of sprite objects for the current map.
    :global map_overlay: A list of overlay objects for the current map.
    :global overlay_batch: A batch of graphics to be drawn over the map.

    :return: None
    """
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


@window.event
def on_draw() -> None:
    """
    Handles the drawing of the game window.

    This function clears the window and then draws the appropriate screen based on the current game state.
    If the main menu is open, it draws the main menu or the options menu, depending on the current menu state.
    If a fight is not ongoing, it draws the current map, the player, any NPCs on the map, and the inventory if it is open.
    If a fight is ongoing, it draws the fighting screen.

    :param None:
    :return: None

    :global window: The game window.
    :global map_sprites: A list of sprite objects for the current map.
    :global player: The player object, which is a dictionary that includes a 'sprite' key and a 'pikemnons' key.
    :global outside_npcs: A list of NPC objects for the outside map.
    :global inventory: A boolean indicating whether the inventory is open.
    :global inventory_index: The index of the currently selected inventory item.
    :global kill_index: The index of the pikemnon to be removed from the player's pikemnons.
    :global menu_direction: The direction of the currently selected menu option.
    :global attack_options: A list of the player's current pikemnon's moves.
    :global inventory_options: A list of the player's inventory items.
    :global change_options: A list of the player's pikemnons.
    :global menu_options: A list of the main menu options.
    :global fighting_menu_state: The current state of the fighting menu.
    :global selected_menu_option_index: The index of the currently selected menu option.
    """
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
        if inventory:
            draw_inventory(window, player['pikemnons'], inventory_index, player['sprite'].x, player['sprite'].y, kill_index)
        
        
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

def start_game():
    global window, player, outside_npcs, map_sprites
    player = create_player(window.width//2, window.height//2)
    load_tile_images()
    set_current_map(mps.starter_map)
    data = get_npcs_data()
    outside_npcs = []
    for i, npc_data in enumerate(data):  # Generate a unique ID
        npc = create_npc(npc_data['image'], npc_data['x'], npc_data['y'], npc_data['direction'], npc_data['pikemnons'])
        outside_npcs.append(npc)

    map_sprites = create_map_sprites()

    create_menu_labels(window)
    create_volume_labels(window)

    set_camera_target(player)
    set_camera_window_size(window_width, window_height)

    pyglet.clock.schedule_interval(update, 1/60.0)

    pyglet.app.run()

if __name__ == "__main__":
    start_game()