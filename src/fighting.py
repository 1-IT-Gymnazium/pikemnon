import json
import random
import time
import uuid
import pyglet
from config.conf import WINDOW_WIDTH, WINDOW_HEIGHT, SCALE
from pyglet.gl import glTexParameteri, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_NEAREST
from src.game_state import get_current_npc, get_fight_stat, set_display_text, set_fight_stat
from config.conf import FONT_NAME
from src.player import add_random_item, get_player_pikemnon

npc_pikemnon = None
player_pikemnon = None

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

def calculate_damage(attack: int, defense: int, power: int, stage: int, attack_type: str, defense_type: str) -> int:
    """
    Calculates the damage dealt by an attack in a Pikemnon battle.

    This function takes the attack and defense stats of the Pikemnon, the power and stage of the attack, and the types of the attack and defense. It calculates the base damage, applies a random factor to make the battles less predictable, and multiplies the result by the effectiveness of the attack type against the defense type.

    Parameters:
    attack (int): The attack stat of the attacking Pikemnon.
    defense (int): The defense stat of the defending Pikemnon.
    power (int): The power of the attack.
    stage (int): The stage of the attack.
    attack_type (str): The type of the attacking.
    defense_type (str): The type of the defense.

    Returns:
    int: The final damage dealt by the attack.
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
    type_effectiveness = load_type_effectiveness()

    effectiveness = type_effectiveness.get(attack_type, {}).get(defense_type, 1)

    base_damage = (power * (attack * attack_stage) / defense) / 50
    random_factor = random.uniform(0.5, 2.0) 
    final_damage = int(base_damage * effectiveness * random_factor) + 2
    
    
    return final_damage

def handle_attack(attack_name: str, attacking_pikemnon: dict[str, any], defending_pikemnon: dict[str, any]) -> None:
    """
    Handles the attack action in the game.

    This function takes the name of the attack, the attacking Pikemnon, and the defending Pikemnon as arguments.
    It calculates the damage based on the attack type and updates the health of the defending Pikemnon.
    It also updates the global variable `text_to_display` with the result of the attack.

    Parameters:
    attack_name (str): The name of the attack.
    attacking_pikemnon (dict): The dictionary representing the attacking Pikemnon.
    defending_pikemnon (dict): The dictionary representing the defending Pikemnon.

    Returns:
    None
    """
    global text_to_display
    move = attacking_pikemnon['moves'][attack_name]
    if move['move_type'] == "attack":
        damage = calculate_damage(attacking_pikemnon['attack'], defending_pikemnon['defense'], move['power'], attacking_pikemnon['stage'], attacking_pikemnon['type'], defending_pikemnon['type'])
        defending_pikemnon['current_health'] -= damage
        text_to_display = f"{attacking_pikemnon['name']} used {attack_name} and dealt {damage} damage."
    elif move['move_type'] == "buff":
        target_stat = move['target_stat']
        attacking_pikemnon['stage'][target_stat] = min(attacking_pikemnon['stage'][target_stat] + move['power'], 6)
        text_to_display = f"{attacking_pikemnon['name']} used {attack_name} and increased {target_stat}."
    elif move['move_type'] == "debuff":
        target_stat = move['target_stat']
        defending_pikemnon['stage'][target_stat] = max(defending_pikemnon['stage'][target_stat] - move['power'], -6)
        text_to_display = f"{attacking_pikemnon['name']} used {attack_name} and decreased {defending_pikemnon['name']}'s {target_stat}."

def load_type_effectiveness():
    with open('data/type_advantages.json') as f:
        return json.load(f)

def player_attack(attack_name: str) -> str:
    global player_pikemnon, text_to_display
    if get_fight_stat() != "text":
        if player_pikemnon['moves'][attack_name]['pp'] <= 0:
            text_to_display = "No PP left for this move."
            return "no pp"
        player_pikemnon['moves'][attack_name]['pp'] -= 1
        handle_attack(attack_name, player_pikemnon, npc_pikemnon)
        set_fight_stat("attacked")

def handle_item(item: str, player: dict[str, any]):
    global player_pikemnon, text_to_display
    if item == "potion" or item == "better potion":
        if player['potion'] <= 0 and item == "potion":
            text_to_display = "No potions left."
            return
        elif player['better potion'] == 0 and item == "better potion":
            text_to_display = "No Better Potions left."
            return
        elif player_pikemnon['current_health'] == player_pikemnon['health']:
            text_to_display = "Pokémon is already at full health."
            return
        if item == "potion":
            player_pikemnon['current_health'] = min(player_pikemnon['health'], player_pikemnon['current_health'] + 10)
            text_to_display = "Pokémon's health was restored by 10."
        elif item == "better potion":
            player_pikemnon['current_health'] = min(player_pikemnon['health'], player_pikemnon['current_health'] + 20)
            text_to_display = "Pokémon's health was restored by 20."
    if item == "pikeball" or item == "better pikeball":
        if player['pikeball'] <= 0 and item == "pikeball":
            text_to_display = "No Pikeballs left."
            return
        elif player['better pikeball'] == 0 and item == "better pikeball":
            text_to_display = "No Better Pikeballs left."
            return
        elif len(player['pikemnons']) == 4:
            text_to_display = "You can't catch this Pokémon. You already have 4 Pokémon."
        elif "wild" in npc_pikemnon:
            base_catch_rate = 0.3 if item == "pikeball" else 0.8
            health_percentage = npc_pikemnon['current_health'] / npc_pikemnon['health']
            catch_rate = base_catch_rate + (1 - health_percentage) * (1 - base_catch_rate)
            catch_rate = min(1, catch_rate)  # Ensure catch rate does not exceed 1
            random_factor = random.uniform(0.7, 1.0)  # Random factor between 0.7 and 1.0
            final_catch_probability = catch_rate * random_factor
            if random.random() < final_catch_probability:
                player = catch_pikemnon(player)
                text_to_display = "You caught the Pokémon!"
            else:
                text_to_display = "You didn't catch the Pokémon."
        else:
            text_to_display = "You can't catch this Pokémon."
    player[item] -= 1

def catch_pikemnon(player: dict[str, any]) -> dict[str, any]:
    global player_pikemnon, npc_pikemnon, text_to_display
    text_to_display = "You caught the Pokémon!"
    npc_pikemnon['id'] = str(uuid.uuid4())
    player['pikemnons'].append(npc_pikemnon)
    return player
    

def draw_player_image():
    # Load the image
    active_pikemnon = get_player_pikemnon(current_player['pikemnons'])
    image = pyglet.resource.image(f'assets/{active_pikemnon['name'].lower()}.png')

    # Apply nearest neighbor filtering to prevent blurring when scaling
    texture = image.get_texture()
    glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    # Create a sprite from the image
    sprite = pyglet.sprite.Sprite(img=image)
    sprite.scale = 7
    sprite.scale_x *= -1  # Flip the sprite horizontally

    # Calculate the position to center the scaled sprite
    sprite.x = (window_width - sprite.width) // 2 + 100
    sprite.y = (window_height - sprite.height) // 2 + 50

    # Reset color to default (white) to ensure no unintended tint is applied
    pyglet.gl.glColor4f(1.0, 1.0, 1.0, 1.0)
    
    # Draw the scaled sprite
    sprite.draw()

def draw_npc_image(img_path: str):
    image = pyglet.resource.image(img_path)

    texture = image.get_texture()
    glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    sprite = pyglet.sprite.Sprite(img=image)
    sprite.scale = 7

    sprite.x = (window_width - sprite.width) // 2 + 150
    sprite.y = (window_height - sprite.height) // 2 + 150

    pyglet.gl.glColor4f(1.0, 1.0, 1.0, 1.0)

    sprite.draw()


def npc_attack():
    global player_pikemnon, npc_pikemnon
    moves = npc_pikemnon['moves']

    attacks = {name: details for name, details in moves.items() if details['move_type'] == 'attack'}
    buffs_and_debuffs = {name: details for name, details in moves.items() if details['move_type'] in ['buff', 'debuff']}

    chance_list = []

    for attack in attacks:
        for _ in range(attacks[attack]['power']):
            if npc_pikemnon['moves'][attack]['pp'] > 0:
                chance_list.append(attack)
    
    if buffs_and_debuffs:
        for buff in buffs_and_debuffs:
            if npc_pikemnon['moves'][buff]['pp'] > 0:
                for _ in range(len(chance_list) // 2):
                    chance_list.append(buff)
    
        if turn % 2 == 0 and buffs_and_debuffs:
            for buff in buffs_and_debuffs:
                if npc_pikemnon['moves'][buff]['pp'] > 0:
                    for _ in range(len(chance_list) // 2):
                        chance_list.append(buff)
    
    attack_name = random.choice(chance_list)
    npc_pikemnon['moves'][attack_name]['pp'] -= 1

    handle_attack(attack_name, npc_pikemnon, player_pikemnon)

def check_battle_end() -> str:
    global player_pikemnon, npc_pikemnon, turn, text_to_display
    if get_fight_stat() == "end":
        return "end"
    if player_pikemnon['current_health'] <= 0:
        player_pikemnon['current_health'] = 0
        for pix in current_player['pikemnons']:
            if pix['current_health'] > 0:
                return "change"
        if not text_to_display and get_fight_stat() != "text":
            text_to_display = "Player's Pokémon fainted. NPC wins!"
            return "text"
        elif not text_to_display:
            return "npc"
    elif npc_pikemnon['current_health'] <= 0:
        current_npc = get_current_npc()
        if current_npc['pikemnon_index'] < len(current_npc['pikemnons']) - 1:
            current_npc['pikemnon_index'] += 1
            npc_pikemnon = current_npc['pikemnons'][current_npc['pikemnon_index']]
            text_to_display = f"NPC sent out {npc_pikemnon['name']}."
        else:
            npc_pikemnon['current_health'] = 0
            if not text_to_display and get_fight_stat() != "text":
                random_item = add_random_item(current_player)
                print(f"Player won! You got a {random_item}")
                text_to_display = "NPC's Pokémon fainted. Player wins!"
                return "text"
            elif not text_to_display:
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

def draw_menu_options(menu_options, selected_option_index, state):
    global current_menu 
    menu_box_x = 20
    menu_box_y = 20
    menu_box_width = 600
    menu_box_height = 150

    # Colors
    default_color = (0, 0, 0, 255)
    highlight_color = (255, 255, 255, 255)
    highlight_background_color = (0, 0, 255, 255)

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
                                         font_name=FONT_NAME,
                                         font_size=12,
                                         color=color,
                                         x=x_center,
                                         y=y_center,
                                         anchor_x='center', anchor_y='center')
        option_label.draw()

    # Reset color to default after drawing
    pyglet.graphics.glColor4ub(255, 255, 255, 255)

def attack_display_text(option):
    return f"{option} {player_pikemnon['moves'][option]['pp']}"

def inventory_display_text(option):
    return f"{option} {current_player[option]}"

def menu_display_text(option):
    return f"{option}"

def change_display_text(option):
    pikemn = 0
    for pikemnon in current_player['pikemnons']:
        if pikemnon['id'] == option:
            pikemn = pikemnon
    health_percentage = round(pikemn['current_health']/pikemn['health'] * 100, 2)
    return f"{pikemn['name']} {health_percentage}%"


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

    global npc_pikemnon, player_pikemnon, current_player, display_time, text_to_display, old_fight_stat
    current_npc = get_current_npc()
    npc_pikemnon = current_npc['pikemnons'][current_npc['pikemnon_index']]
    current_player = player

    player_pikemnon = get_player_pikemnon(player['pikemnons'])

    draw_box(40, 450, 200, 80)
    draw_box(400, 200, 200, 80)

    draw_box(20, 20, 600, 150)

    draw_label('Player', 40 + 10, 450 + 80 - 10)
    draw_label(player_pikemnon['name'], 40 + 10, 450 + 50)
    draw_label(npc_pikemnon['name'], 400 + 10, 200 + 80 - 10)

    draw_health_bar(40, 450 - 20, 200, 10, player_pikemnon['current_health']/player_pikemnon['health'])
    draw_health_bar(400, 200 - 20, 200, 10, npc_pikemnon['current_health']/npc_pikemnon['health'])

    if text_to_display:
        set_display_text(True)

    draw_label(text_to_display, 50, 150) if text_to_display else draw_menu_options(menu_options, selected_option_index, menu_state)

    if text_to_display and not display_time:
        display_time = time.time()
        old_fight_stat = get_fight_stat()
    elif display_time and time.time() - display_time >= 1:
        text_to_display = ''
        display_time = None
        set_fight_stat(old_fight_stat)
        old_fight_stat = None

    draw_player_image()
    draw_npc_image(f'assets/{npc_pikemnon['name'].lower()}.png')

    if direction:
        navigate_menu(direction)

    set_fight_stat(check_battle_end())

    if text_to_display:
        set_fight_stat("text")

def set_text_to_display(text: str) -> None:
    global text_to_display
    text_to_display = text
