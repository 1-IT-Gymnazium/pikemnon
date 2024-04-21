import random
import time
import pyglet
from conf import WINDOW_WIDTH, WINDOW_HEIGHT, SCALE
from pyglet.gl import glTexParameteri, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_NEAREST
from game_state import get_current_npc, get_fight_stat, set_display_text, set_fight_stat
from conf import FONT_NAME
from player import get_player_pikemnon

npc_pokemon = None
player_pokemon = None

selected_option_index = 0

window_width = WINDOW_WIDTH*SCALE
window_height = WINDOW_HEIGHT*SCALE

main_menu_options = ["Attack", "Item", "Run", "Swap"]
# attack_menu_options = None
current_menu = main_menu_options

turn = 0

current_player = None

text_to_display = ''

display_time = None

old_fight_stat = None

def calculate_damage(attack: int, defense: int, power: int, stage: int) -> int:
    """
    Calculate the damage inflicted during a Pokemon battle.

    This function uses the formula from the Pokemon games to calculate
    how much damage an attack will do. The formula takes into account
    the attack power of the attacking Pokemon, the defense of the
    defending Pokemon, and the power of the move being used.

    Parameters:
    attack (int): The attack power of the attacking Pokemon.
    defense (int): The defense power of the defending Pokemon.
    power (int): The power of the move being used.

    Returns:
    int: The calculated damage.
    """

    stage_multipliers = {
    -6: 0.25,
    -5: 0.29,
    -4: 0.33,
    -3: 0.4,
    -2: 0.5,
    -1: 0.67,
    0: 1,
    1: 1.5,
    2: 2,
    3: 2.5,
    4: 3,
    5: 3.5,
    6: 4
    }

    attack_stage = stage_multipliers[stage['attack']]
    
    return int(((2 * power * ((attack * attack_stage) / defense)) / 50) + 2)

def handle_attack(attack_name, attacking_pokemon, defending_pokemon):
    global text_to_display
    move = attacking_pokemon['moves'][attack_name]
    if move['move_type'] == "attack":
        damage = calculate_damage(attacking_pokemon['attack'], defending_pokemon['defense'], move['power'], attacking_pokemon['stage'])
        defending_pokemon['current_health'] -= damage
        text_to_display = f"{attacking_pokemon['name']} used {attack_name} and dealt {damage} damage."
    elif move['move_type'] == "buff":
        target_stat = move['target_stat']
        attacking_pokemon['stage'][target_stat] = min(attacking_pokemon['stage'][target_stat] + move['power'], 6)
    elif move['move_type'] == "debuff":
        target_stat = move['target_stat']
        defending_pokemon['stage'][target_stat] = max(defending_pokemon['stage'][target_stat] - move['power'], -6)

def player_attack(attack_name: str) -> str:
    global player_pokemon, text_to_display
    if player_pokemon['moves'][attack_name]['pp'] <= 0:
        text_to_display = "No PP left for this move."
        return "no pp"
    player_pokemon['moves'][attack_name]['pp'] -= 1
    handle_attack(attack_name, player_pokemon, npc_pokemon)
    set_fight_stat("attacked")

def handle_item(item: str, player: dict[str, any]) -> dict[str, any]:
    global player_pokemon, text_to_display
    if item == "potion":
        if player['potion'] <= 0:
            text_to_display = "No potions left."
            return player
        if player_pokemon['current_health'] == player_pokemon['health']:
            text_to_display = "Pokémon is already at full health."
            return player
        player_pokemon['current_health'] = min(player_pokemon['current_health'] + 10, player_pokemon['health'])
        text_to_display = "Healed 10 HP."
    if item == "pikeball":
        if player['pikeball'] <= 0:
            text_to_display = "No Pikeballs left."
            return player
        if "wild" in npc_pokemon:
            player = catch_pikemnon(player)
        else:
            text_to_display = "You can't catch this Pokémon."
    return player

def catch_pikemnon(player) -> dict[str, any]:
    global player_pokemon, npc_pokemon, text_to_display
    text_to_display = "You caught the Pokémon!"
    player['pikemnons'].append(npc_pokemon)
    return player
    

def draw_player_image():
    # Load the image
    image = pyglet.resource.image('assets/fight-player.png')

    # Apply nearest neighbor filtering to prevent blurring when scaling
    texture = image.get_texture()
    glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    # Create a sprite from the image
    sprite = pyglet.sprite.Sprite(img=image)
    sprite.scale = 7

    # Calculate the position to center the scaled sprite
    sprite.x = (window_width - sprite.width) // 2 - 150
    sprite.y = (window_height - sprite.height) // 2 - 0

    # Reset color to default (white) to ensure no unintended tint is applied
    pyglet.gl.glColor4f(1.0, 1.0, 1.0, 1.0)
    
    # Draw the scaled sprite
    sprite.draw()


def npc_attack():
    global player_pokemon, npc_pokemon
    moves = npc_pokemon['moves']

    attacks = {name: details for name, details in moves.items() if details['move_type'] == 'attack'}
    buffs_and_debuffs = {name: details for name, details in moves.items() if details['move_type'] in ['buff', 'debuff']}

    chance_list = []

    for attack in attacks:
        for _ in range(attacks[attack]['power']):
            if npc_pokemon['moves'][attack]['pp'] > 0:
                chance_list.append(attack)
    
    if buffs_and_debuffs:
        for buff in buffs_and_debuffs:
            if npc_pokemon['moves'][buff]['pp'] > 0:
              chance_list.append([buff] * (len(chance_list) // 2))
    
        if turn % 2 == 0 and buffs_and_debuffs:
            for buff in buffs_and_debuffs:
                if npc_pokemon['moves'][buff]['pp'] > 0:
                    chance_list.append([buff] * (len(chance_list) // 2))
    
    attack_name = random.choice(chance_list)
    npc_pokemon['moves'][attack_name]['pp'] -= 1

    handle_attack(attack_name, npc_pokemon, player_pokemon)

def check_battle_end() -> str:
    global player_pokemon, npc_pokemon, turn, text_to_display
    if player_pokemon['current_health'] <= 0:
        player_pokemon['current_health'] = 0
        for pix in current_player['pikemnons']:
            if pix['current_health'] > 0:
                return "change"
        if not text_to_display and get_fight_stat() != "text":
            text_to_display = "Player's Pokémon fainted. NPC wins!"
            return "text"
        elif text_to_display:
            return "text"
        elif not text_to_display:
            return "npc"
    elif npc_pokemon['current_health'] <= 0:
        current_npc = get_current_npc()
        if current_npc['pikemnon_index'] < len(current_npc['pikemnons']) - 1:
            current_npc['pikemnon_index'] += 1
            npc_pokemon = current_npc['pikemnons'][current_npc['pikemnon_index']]
            print("NPC sends out another Pokémon.")
        else:
            npc_pokemon['current_health'] = 0
            print("NPC's Pokémon fainted. Player wins!")
            turn = 0
            return "player"
    return "continue" if get_fight_stat() != "attacked" else "attacked"


def draw_health_bar(x, y, width, height, health_percentage):
    # Draw the health bar background (e.g., gray for depleted health)
    pyglet.graphics.glColor4f(0.5, 0.5, 0.5, 1)  # Gray color
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [x, y, x + width, y, x + width, y + height, x, y + height]))
    
    # Draw the current health
    pyglet.graphics.glColor4f(0, 1, 0, 1)  # Green color
    current_health_width = width * health_percentage
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [x, y, x + current_health_width, y, x + current_health_width, y + height, x, y + height]))

def draw_menu_options(window, menu_options, selected_option_index, state, player_pokemon):
    global current_menu  # Assuming current_menu holds the current state of menu options
    menu_box_x = 20
    menu_box_y = 20
    menu_box_width = 600
    menu_box_height = 150

    # Colors
    default_color = (0, 0, 0, 255)  # Black for unselected options
    highlight_color = (255, 255, 255, 255)  # White for the selected option text
    highlight_background_color = (0, 0, 255, 255)  # Blue background for selected option

    grid_columns = 2
    grid_rows = 2
    column_width = menu_box_width / grid_columns
    row_height = menu_box_height / grid_rows

    for i, option in enumerate(menu_options):
        column = i % grid_columns
        row = i // grid_columns

        x_center = menu_box_x + (column * column_width) + (column_width / 2)
        y_center = menu_box_y + (menu_box_height - (row * row_height)) - (row_height / 2)

        display_text_functions = {
            'attack': attack_display_text,
            'inventory': inventory_display_text,
            'menu': menu_display_text,
            'change': change_display_text
        }

        display_text_function = display_text_functions.get(state, display_text_functions['menu'])

        display_text = display_text_function(option)

        # Use index to check if the option is the selected one
        if i == selected_option_index:
            # Draw highlighted background
            pyglet.graphics.glColor4ub(*highlight_background_color)
            margin = 5  # Margin for the background rectangle
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [
                x_center - column_width / 2 + margin, y_center - row_height / 2 + margin,
                x_center + column_width / 2 - margin, y_center - row_height / 2 + margin,
                x_center + column_width / 2 - margin, y_center + row_height / 2 - margin,
                x_center - column_width / 2 + margin, y_center + row_height / 2 - margin,
            ]))

            color = highlight_color
        else:
            color = default_color

        # Create and draw the label for the option with the number appended
        option_label = pyglet.text.Label(display_text,
                                         font_name='Arial',  # Adjust FONT_NAME to 'Arial' if not previously defined
                                         font_size=12,
                                         color=color,
                                         x=x_center,
                                         y=y_center,
                                         anchor_x='center', anchor_y='center')
        option_label.draw()

    # Reset color to default after drawing
    pyglet.graphics.glColor4ub(255, 255, 255, 255)

def attack_display_text(option):
    return f"{option} {player_pokemon['moves'][option]['pp']}"

def inventory_display_text(option):
    return f"{option} {current_player[option]}"

def menu_display_text(option):
    return f"{option}"

def change_display_text(option):
    pikemn = 0
    for pikemnon in current_player['pikemnons']:
        if pikemnon['name'] == option:
            pikemn = pikemnon
    return f"{option} {pikemn['current_health']/pikemn['health'] * 100}%"

def navigate_menu(direction):
    global selected_option_index
    if direction == 'up' and selected_option_index >= 2:
        selected_option_index -= 2
    elif direction == 'down' and selected_option_index < 2:
        selected_option_index += 2
    elif direction == 'left' and selected_option_index % 2 == 1:
        selected_option_index -= 1
    elif direction == 'right' and selected_option_index % 2 == 0:
        selected_option_index += 1

def clear_screen(window):
    pyglet.gl.glClearColor(1, 1, 1, 1)
    window.clear()

def draw_box(x, y, width, height, border_thickness=2):
    # Draw border
    pyglet.graphics.glColor4f(0, 0, 0, 1)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [
        x - border_thickness, y - border_thickness,
        x + width + border_thickness, y - border_thickness,
        x + width + border_thickness, y + height + border_thickness,
        x - border_thickness, y + height + border_thickness]))
    # Fill
    pyglet.graphics.glColor4f(1, 1, 1, 1)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [
        x, y, x + width, y, x + width, y + height, x, y + height]))

def draw_label(text, x, y, font_size=12, color=(0, 0, 0, 255)):
    label = pyglet.text.Label(text, font_name=FONT_NAME, font_size=font_size, color=color, x=x, y=y, anchor_x='left', anchor_y='center')
    label.draw()

def draw_health_bar(x, y, width, height, percentage):
    # Background
    pyglet.graphics.glColor4f(0.5, 0.5, 0.5, 1)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [x, y, x + width, y, x + width, y + height, x, y + height]))
    # Health
    pyglet.graphics.glColor4f(0, 1, 0, 1)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [x, y, x + width * percentage, y, x + width * percentage, y + height, x, y + height]))

def fighting_screen(window, player, direction, menu_options, selected_option_index, menu_state):
    clear_screen(window)

    global npc_pokemon, player_pokemon, current_player, display_time, text_to_display, old_fight_stat
    current_npc = get_current_npc()
    npc_pokemon = current_npc['pikemnons'][current_npc['pikemnon_index']]
    current_player = player

    player_pokemon = get_player_pikemnon(player['pikemnons'])

    draw_box(40, 450, 200, 80)
    draw_box(400, 200, 200, 80)

    draw_box(20, 20, 600, 150)

    draw_label('Player', 40 + 40, 450 + 80 - 10)
    draw_label(player_pokemon['name'], 40 + 50, 450 + 50)
    draw_label(npc_pokemon['name'], 400 + 70, 200 + 80 - 10)

    draw_health_bar(40, 450 - 20, 200, 10, player_pokemon['current_health']/player_pokemon['health'])
    draw_health_bar(400, 200 - 20, 200, 10, npc_pokemon['current_health']/npc_pokemon['health'])

    if text_to_display:
        set_display_text(True)

    draw_label(text_to_display, 50, 150, font_size=16) if text_to_display else draw_menu_options(window, menu_options, selected_option_index, menu_state, player_pokemon)

    if text_to_display and not display_time:
        display_time = time.time()
        old_fight_stat = get_fight_stat()
    elif display_time and time.time() - display_time >= 1:
        text_to_display = ''
        display_time = None
        set_fight_stat(old_fight_stat)
        old_fight_stat = None

    if text_to_display:
        set_fight_stat("text")

    draw_player_image()

    if direction:
        navigate_menu(direction)

    set_fight_stat(check_battle_end())




