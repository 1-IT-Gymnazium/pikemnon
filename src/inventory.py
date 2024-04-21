import pyglet
from pyglet.gl import *
from config.conf import FONT_NAME
from src.player import remove_pikemnon

selected_pikemnon = None

def draw_inventory(window, player_pikemnons, selected_index, player_x, player_y, kill_index=None):
    """
    Draws a 2x2 grid of blocks in the middle of the screen, with the names of the player's Pokemon.
    Highlights the selected Pokemon.

    Parameters:
    window (pyglet.window.Window): The window in which to draw the blocks.
    player_pikemnons (list): The list of the player's Pokemon.
    selected_index (int): The index of the selected Pokemon.
    camera_x (float): The x-coordinate of the camera's position.
    camera_y (float): The y-coordinate of the camera's position.

    Returns:
    None
    """
    if selected_pikemnon:
        # Set up the drawing for the selected Pokemon
        glColor3f(1.0, 1.0, 1.0)  # White background
        block_width = 400
        block_height = 300
        x = int(player_x - window.width // 2 + block_width // 2)
        y = int(player_y - window.height // 2 + block_height // 2)

        # Draw background rectangle
        pyglet.graphics.draw(4, GL_QUADS,
                             ('v2i', (x, y, x + block_width, y, x + block_width, y + block_height, x, y + block_height)),
                             ('c3B', (255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255)))

        # Draw the selected Pokemon's name and subtext
        label = pyglet.text.Label(selected_pikemnon['name'],
                                  font_name=FONT_NAME,
                                  font_size=24,
                                  x=x + block_width // 2,
                                  y=y + block_height - 30,
                                  anchor_x='center', anchor_y='center',
                                  color=(0, 0, 0, 255))
        label.draw()

        subtext = pyglet.text.Label("Do you want to kill this Pikemnon?",
                                    font_name=FONT_NAME,
                                    font_size=16,
                                    x=x + block_width // 2,
                                    y=y + block_height - 150,
                                    anchor_x='center', anchor_y='center',
                                    color=(0, 0, 0, 255))
        subtext.draw()

        # Draw "Yes" and "No" options with highlighting based on selection_index
        yes_color = (0, 255, 0, 255) if kill_index == 0 else (0, 0, 0, 255)
        no_color = (255, 0, 0, 255) if kill_index == 1 else (0, 0, 0, 255)

        yes_label = pyglet.text.Label("Yes",
                                      font_name=FONT_NAME,
                                      font_size=18,
                                      x=x + block_width // 2 - 60,
                                      y=y + block_height // 2 - 60,
                                      anchor_x='center', anchor_y='center',
                                      color=yes_color)
        yes_label.draw()

        no_label = pyglet.text.Label("No",
                                     font_name=FONT_NAME,
                                     font_size=18,
                                     x=x + block_width // 2 + 60,
                                     y=y + block_height // 2 - 60,
                                     anchor_x='center', anchor_y='center',
                                     color=no_color)
        no_label.draw()
    else:
        # Set the color to white
        glColor3f(1.0, 1.0, 1.0)

        # Calculate the size of the blocks
        block_width = 150
        block_height = 150

        # Calculate the size of the grid
        grid_width = 2 * block_width
        grid_height = 2 * block_height

        # Calculate the position of the grid relative to the camera's position
        grid_x = player_x - window.width // 2 + grid_width // 2
        grid_y = player_y - window.height // 2 + grid_height // 2

        # Create a label for each Pokemon
        labels = [pyglet.text.Label(pikemnon['name'],
                                    font_name=FONT_NAME,
                                    font_size=12,
                                    x=grid_x + (i % 2) * block_width + block_width // 2,
                                    y=grid_y + (i // 2) * block_height + block_height // 2,
                                    anchor_x='center', anchor_y='center',
                                    color=(0, 0, 0, 255))
                for i, pikemnon in enumerate(player_pikemnons)]

        for i, pikemnon in enumerate(player_pikemnons):
            block_x = grid_x + (i % 2) * block_width
            block_y = grid_y + (i // 2) * block_height

            if i == selected_index:
                glColor3f(1.0, 1.0, 0.0)
            else:
                glColor3f(1.0, 1.0, 1.0)

            pyglet.graphics.draw(4, GL_QUADS,
            ('v2i', (int(block_x), int(block_y), int(block_x + block_width), int(block_y), int(block_x + block_width), int(block_y + block_height), int(block_x), int(block_y + block_height)))
            )

            labels[i].draw()

def select_selected_pikemnon(player_pikemnons, selected_index):
    """
    Assigns the selected pikemnon to a global variable and prints its name.

    Parameters:
    player_pikemnons (list): The list of the player's pikemnons.
    selected_index (int): The index of the selected pikemnon.

    Returns:
    None
    """
    global selected_pikemnon
    if 0 <= selected_index < len(player_pikemnons):
        selected_pikemnon = player_pikemnons[selected_index]
        print(player_pikemnons[selected_index]['name'])
    else:
        print("Invalid index")

def remove_selected_pikemnon():
    """
    Removes the selected pikemnon from the global variable.

    Parameters:
    None

    Returns:
    None
    """
    global selected_pikemnon
    selected_pikemnon = None

def kill_pikemnon(player: dict[str, any]) -> dict[str, any]:
    """
    Kills the selected pikemnon.

    Parameters:
    None

    Returns:
    None
    """
    global selected_pikemnon
    if selected_pikemnon:
        remove_pikemnon(player, selected_pikemnon['id'])
        selected_pikemnon = None
    else:
        print("No pikemnon selected")