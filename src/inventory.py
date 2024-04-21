import pyglet
from pyglet.gl import *
from conf import FONT_NAME
from src.player import remove_pikemnon

selected_pikemnon = None

def draw_inventory(window, player_pikemnons, selected_index, player_x, player_y, kill_index=None):
    """
    Draws the player's inventory on the screen.

    This function draws a grid of the player's Pokemon, highlighting the currently selected one. If a Pokemon is selected, it draws a detailed view of that Pokemon with the option to kill it.

    :param window: The window to draw on.
    :type window: pyglet.window.Window
    :param player_pikemnons: The player's list of Pokemon.
    :type player_pikemnons: list
    :param selected_index: The index of the currently selected Pokemon.
    :type selected_index: int
    :param player_x: The x-coordinate of the player's position.
    :type player_x: float
    :param player_y: The y-coordinate of the player's position.
    :type player_y: float
    :param kill_index: The index of the kill option, if a Pokemon is selected. Defaults to None.
    :type kill_index: int, optional
    :return: None
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

    :param player_pikemnons: The list of the player's pikemnons.
    :type player_pikemnons: list
    :param selected_index: The index of the selected pikemnon.
    :type selected_index: int
    :return: None
    :rtype: None
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

    :param: None
    :return: None
    """
    global selected_pikemnon
    selected_pikemnon = None

def kill_pikemnon(player: dict[str, any]) -> dict[str, any]:
    """
    Kills the selected pikemnon.

    :param player: The player's dictionary.
    :type player: dict[str, any]
    :return: The modified player's dictionary.
    :rtype: dict[str, any]
    """
    global selected_pikemnon
    if selected_pikemnon:
        remove_pikemnon(player, selected_pikemnon['id'])
        selected_pikemnon = None
    else:
        print("No pikemnon selected")