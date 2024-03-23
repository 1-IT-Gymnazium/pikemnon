import pyglet
from conf import WINDOW_WIDTH, WINDOW_HEIGHT, SCALE
from pyglet.gl import glTexParameteri, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_NEAREST


player_pokemon = {'attack': 10, 'defense': 10, 'health': 100}
npc_pokemon = {'attack': 10, 'defense': 10, 'health': 100}
current_turn = 'player'
selected_option_index = 0

window_width = WINDOW_WIDTH*SCALE
window_height = WINDOW_HEIGHT*SCALE


def calculate_damage(attack, defense, power):
    """
    Simple damage calculation formula
    """
    return int(((2 * power * (attack / defense)) / 50) + 2)

def player_attack():
    global player_pokemon, npc_pokemon
    power = 50
    damage = calculate_damage(player_pokemon['attack'], npc_pokemon['defense'], power)
    npc_pokemon['health'] -= damage
    print(f"Player's Pokémon caused {damage} damage. NPC Pokémon health is now {npc_pokemon['health']}.")
    check_battle_end()


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
    power = 50
    damage = calculate_damage(npc_pokemon['attack'], player_pokemon['defense'], power)
    player_pokemon['health'] -= damage
    print(f"NPC's Pokémon caused {damage} damage. Player Pokémon health is now {player_pokemon['health']}.")
    check_battle_end()

def check_battle_end():
    global player_pokemon, npc_pokemon
    if player_pokemon['health'] <= 0:
        print("Player's Pokémon fainted. NPC wins!")
        return True
    elif npc_pokemon['health'] <= 0:
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

def draw_menu_options(window, selected):
    menu_box_x = 20
    menu_box_y = 20
    menu_box_width = 600
    menu_box_height = 150
    menu_options = ["Attack", "Item", "Run", "Swap"]

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

        # Check if the option is the selected one
        if option == selected:
            # Draw highlighted background
            pyglet.graphics.glColor4ub(*highlight_background_color)
            margin = 5  # Margin for the background rectangle
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [
                x_center - column_width / 2 + margin, y_center - row_height / 2 + margin,
                x_center + column_width / 2 - margin, y_center - row_height / 2 + margin,
                x_center + column_width / 2 - margin, y_center + row_height / 2 - margin,
                x_center - column_width / 2 + margin, y_center + row_height / 2 - margin,
            ]))

            # Set text color for highlighted option
            color = highlight_color
        else:
            color = default_color

        # Create and draw the label for the option
        option_label = pyglet.text.Label(option,
                                         font_name='Courier',
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

def fighting_screen(window, direction):
    pyglet.gl.glClearColor(1, 1, 1, 1)
    window.clear()

    # Define the box's coordinates, size, and border thickness
    player_box_x = 40  # Left edge of the window
    player_box_y = 450  # Bottom edge of the window
    player_box_width = 200
    player_box_height = 80
    enemy_box_x = 400  # Left edge of the window
    enemy_box_y = 200  # Bottom edge of the window
    enemy_box_width = 200
    enemy_box_height = 80
    menu_box_x = 20
    menu_box_y = 20
    menu_box_width = 600
    menu_box_height = 150
    border_thickness = 2

    
    pyglet.graphics.glColor4f(0, 0, 0, 1)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                         ('v2f', [player_box_x - border_thickness, player_box_y - border_thickness, 
                                  player_box_x + player_box_width + border_thickness, player_box_y - border_thickness, 
                                  player_box_x + player_box_width + border_thickness, player_box_y + player_box_height + border_thickness, 
                                  player_box_x - border_thickness, player_box_y + player_box_height + border_thickness])
                        )

    pyglet.graphics.glColor4f(1, 1, 1, 1)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                         ('v2f', [player_box_x, player_box_y, 
                                  player_box_x + player_box_width, player_box_y, 
                                  player_box_x + player_box_width, player_box_y + player_box_height, 
                                  player_box_x, player_box_y + player_box_height])
                        )

    pyglet.graphics.glColor4f(0, 0, 0, 1)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                         ('v2f', [enemy_box_x - border_thickness, enemy_box_y - border_thickness, 
                                  enemy_box_x + enemy_box_width + border_thickness, enemy_box_y - border_thickness, 
                                  enemy_box_x + enemy_box_width + border_thickness, enemy_box_y + enemy_box_height + border_thickness, 
                                  enemy_box_x - border_thickness, enemy_box_y + enemy_box_height + border_thickness])
                        )

    pyglet.graphics.glColor4f(1, 1, 1, 1)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                         ('v2f', [enemy_box_x, enemy_box_y, 
                                  enemy_box_x + enemy_box_width, enemy_box_y, 
                                  enemy_box_x + enemy_box_width, enemy_box_y + enemy_box_height, 
                                  enemy_box_x, enemy_box_y + enemy_box_height])
                        )

    pyglet.graphics.glColor4f(0, 0, 0, 1)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                         ('v2f', [menu_box_x - border_thickness, menu_box_y - border_thickness, 
                                  menu_box_x + menu_box_width + border_thickness, menu_box_y - border_thickness, 
                                  menu_box_x + menu_box_width + border_thickness, menu_box_y + menu_box_height + border_thickness, 
                                  menu_box_x - border_thickness, menu_box_y + menu_box_height + border_thickness])
                        )

    pyglet.graphics.glColor4f(1, 1, 1, 1)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                         ('v2f', [menu_box_x, menu_box_y, 
                                  menu_box_x + menu_box_width, menu_box_y, 
                                  menu_box_x + menu_box_width, menu_box_y + menu_box_height, 
                                  menu_box_x, menu_box_y + menu_box_height])
                        )

    player_label_x = player_box_x + 40
    player_label_y = player_box_y + player_box_height - 10

    enemy_label_x = enemy_box_x + 40
    enemy_label_y = enemy_box_y + enemy_box_height - 10


    player_label = pyglet.text.Label('Player',
                              font_name='Courier',
                              font_size=12,
                              color=(0, 0, 0, 255),
                              x=player_label_x, y=player_label_y,
                              anchor_x='center', anchor_y='center')
    player_label.draw()

    enemy_label = pyglet.text.Label('Enemy',
                              font_name='Courier',
                              font_size=12,
                              color=(0, 0, 0, 255),
                              x=enemy_label_x, y=enemy_label_y,
                              anchor_x='center', anchor_y='center')
    enemy_label.draw()

    menu_options = ["Attack", "Item", "Run", "Swap"]
    if direction:
        navigate_menu(direction)
    draw_menu_options(window, menu_options[selected_option_index])

    player_health_bar_x = player_label_x - 30
    player_health_bar_y = player_label_y - 25
    player_health_bar_width = 100
    player_health_bar_height = 10
    player_health_percentage = 1
    draw_health_bar(player_health_bar_x, player_health_bar_y, player_health_bar_width, player_health_bar_height, player_health_percentage)

    enemy_health_bar_x = enemy_label_x - 30
    enemy_health_bar_y = enemy_label_y - 25
    enemy_health_bar_width = 100
    enemy_health_bar_height = 10
    enemy_health_percentage = 0.1
    draw_health_bar(enemy_health_bar_x, enemy_health_bar_y, enemy_health_bar_width, enemy_health_bar_height, enemy_health_percentage)

    draw_player_image()

