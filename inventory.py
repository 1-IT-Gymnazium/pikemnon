import pyglet
from pyglet.gl import *
from conf import FONT_NAME

def draw_inventory(window, player_pikemnons, selected_index, camera_x, camera_y):
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
    # Set the color to white
    glColor3f(1.0, 1.0, 1.0)

    # Calculate the size of the blocks
    block_width = 150
    block_height = 150

    # Calculate the size of the grid
    grid_width = 2 * block_width
    grid_height = 2 * block_height

    # Calculate the position of the grid relative to the camera's position
    grid_x = camera_x - window.width // 2 + grid_width // 2
    grid_y = camera_y - window.height // 2 + grid_height // 2

    # Create a label for each Pokemon
    labels = [pyglet.text.Label(pikemnon['name'],
                                font_name=FONT_NAME,
                                font_size=12,
                                x=grid_x + (i % 2) * block_width + block_width // 2,
                                y=grid_y + (i // 2) * block_height + block_height // 2,
                                anchor_x='center', anchor_y='center',
                                color=(0, 0, 0, 255))  # Set the text color to black
              for i, pikemnon in enumerate(player_pikemnons)]

    # Draw the blocks and the labels
    for i, pikemnon in enumerate(player_pikemnons):
        block_x = grid_x + (i % 2) * block_width
        block_y = grid_y + (i // 2) * block_height

        # If this is the selected Pokemon, set the color to yellow
        if i == selected_index:
            glColor3f(1.0, 1.0, 0.0)
        else:
            glColor3f(1.0, 1.0, 1.0)

        pyglet.graphics.draw(4, GL_QUADS,
        ('v2i', (int(block_x), int(block_y), int(block_x + block_width), int(block_y), int(block_x + block_width), int(block_y + block_height), int(block_x), int(block_y + block_height)))
        )

        labels[i].draw()