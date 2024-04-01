import pyglet
from conf import WINDOW_WIDTH, WINDOW_HEIGHT, SCALE
from pyglet.gl import glTexParameteri, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_NEAREST
from game_state import get_current_npc
from conf import FONT_NAME
from player import get_player_pikemnon

npc_pokemon = None
player_pokemon = None

current_turn = 'player'
selected_option_index = 0

window_width = WINDOW_WIDTH*SCALE
window_height = WINDOW_HEIGHT*SCALE

main_menu_options = ["Attack", "Item", "Run", "Swap"]
# attack_menu_options = None
current_menu = main_menu_options
menu_state = 'main'


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

    damage = ((2 * power * ((attack * attack_stage) / defense)) / 50) + 2
    print(damage)
    print(attack * attack_stage)
    print(int(damage))
    
    return int(((2 * power * ((attack * attack_stage) / defense)) / 50) + 2)

def handle_attack(attack_name, attacking_pokemon, defending_pokemon):
    move = attacking_pokemon['moves'][attack_name]
    if move['move_type'] == "attack":
        damage = calculate_damage(attacking_pokemon['attack'], defending_pokemon['defense'], move['power'], attacking_pokemon['stage'])
        defending_pokemon['health'] -= damage
        print(f"used {attack_name} and caused {damage} damage.")
    elif move['move_type'] == "buff":
        target_stat = move['target_stat']
        print(min(attacking_pokemon['stage'][target_stat] + move['power'], 6))
        attacking_pokemon['stage'][target_stat] = min(attacking_pokemon['stage'][target_stat] + move['power'], 6)
    elif move['move_type'] == "debuff":
        target_stat = move['target_stat']
        defending_pokemon['stage'][target_stat] = max(defending_pokemon['stage'][target_stat] - move['power'], -6)

def player_attack(attack_name: str):
    global player_pokemon
    handle_attack(attack_name, player_pokemon, npc_pokemon)
    return check_battle_end()


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
    damage = calculate_damage(npc_pokemon['attack'], player_pokemon['defense'], npc_pokemon['attack'])
    player_pokemon['health'] -= damage
    print(f"NPC's Pokémon caused {damage} damage. Player Pokémon health is now {player_pokemon['health']}.")
    return check_battle_end()

def check_battle_end():
    global player_pokemon, npc_pokemon
    if player_pokemon['health'] <= 0:
        player_pokemon['health'] = 0
        print("Player's Pokémon fainted. NPC wins!")
        return True
    elif npc_pokemon['health'] <= 0:
        current_npc = get_current_npc()
        if current_npc['pikemnon_index'] < len(current_npc['pikemnons']) - 1:
            current_npc['pikemnon_index'] += 1
            npc_pokemon = current_npc['pikemnons'][current_npc['pikemnon_index']]
            print("NPC sends out another Pokémon.")
        else:
            npc_pokemon['health'] = 0
            print("NPC's Pokémon fainted. Player wins!")
            return True
    return False

def next_turn():
    global current_turn
    if current_turn == 'player':
        current_turn = 'npc'
        npc_attack()
    else:
        current_turn = 'player'



def draw_health_bar(x, y, width, height, health_percentage):
    # Draw the health bar background (e.g., gray for depleted health)
    pyglet.graphics.glColor4f(0.5, 0.5, 0.5, 1)  # Gray color
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [x, y, x + width, y, x + width, y + height, x, y + height]))
    
    # Draw the current health (e.g., green for current health)
    pyglet.graphics.glColor4f(0, 1, 0, 1)  # Green color
    current_health_width = width * health_percentage
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [x, y, x + current_health_width, y, x + current_health_width, y + height, x, y + height]))

def draw_menu_options(window, menu_options, selected_option_index):
    global current_menu  # Assuming current_menu holds the current state of menu options
    menu_box_x = 20
    menu_box_y = 20
    menu_box_width = 600
    menu_box_height = 150

    # No need to determine current_menu here if menu_options is directly passed as an argument
    # menu_options = current_menu

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

        # Create and draw the label for the option
        option_label = pyglet.text.Label(option,
                                         font_name=FONT_NAME,
                                         font_size=12,
                                         color=color,
                                         x=x_center,
                                         y=y_center,
                                         anchor_x='center', anchor_y='center')
        option_label.draw()

    # Reset color to default after drawing
    pyglet.graphics.glColor4ub(255, 255, 255, 255)


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
    label = pyglet.text.Label(text, font_name=FONT_NAME, font_size=font_size, color=color, x=x, y=y, anchor_x='center', anchor_y='center')
    label.draw()

def draw_health_bar(x, y, width, height, percentage):
    # Background
    pyglet.graphics.glColor4f(0.5, 0.5, 0.5, 1)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [x, y, x + width, y, x + width, y + height, x, y + height]))
    # Health
    pyglet.graphics.glColor4f(0, 1, 0, 1)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [x, y, x + width * percentage, y, x + width * percentage, y + height, x, y + height]))

def fighting_screen(window, player, direction, menu_options, selected_option_index):
    clear_screen(window)

    global npc_pokemon, player_pokemon
    current_npc = get_current_npc()
    npc_pokemon = current_npc['pikemnons'][current_npc['pikemnon_index']]


    if not player_pokemon or player_pokemon['health'] <= 0:
        player_pokemon = get_player_pikemnon(player['pikemnons'])
        # attack_menu_options = list(player_pokemon['moves'].keys())

    draw_box(40, 450, 200, 80)
    draw_box(400, 200, 200, 80)

    draw_box(20, 20, 600, 150)

    draw_label('Player', 40 + 40, 450 + 80 - 10)
    draw_label(npc_pokemon['name'], 400 + 70, 200 + 80 - 10)

    draw_health_bar(40, 450 - 20, 200, 10, player_pokemon['health']/player_pokemon['current_health'])
    draw_health_bar(400, 200 - 20, 200, 10, npc_pokemon['health']/npc_pokemon['current_health'])

    draw_menu_options(window, menu_options, selected_option_index)

    draw_player_image()

    if direction:
        navigate_menu(direction)




