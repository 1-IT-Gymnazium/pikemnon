import pyglet

# Initialize global variables for menu state
menu_items = ['Start Game', 'Options', 'Exit']
menu_labels = []
selected_index = 0
game_title_label = None  # Initialize a variable for the game title label

def create_menu_labels(window):
    global menu_labels, game_title_label
    # Create the game title label
    game_title_label = pyglet.text.Label('Pikemnon',
                                         font_name='Times New Roman',
                                         font_size=48,
                                         x=window.width // 2,
                                         y=window.height - 100,
                                         anchor_x='center',
                                         anchor_y='center',
                                         color=(0, 0, 0, 255))  # Black color for the title

    # Adjust the menu items to be lower on the screen
    menu_labels = [pyglet.text.Label(text=item,
                                     font_name='Times New Roman',
                                     font_size=36,
                                     x=window.width // 2,
                                     y=window.height // 2 - 50 * i - 50,  # Offset by an additional 50 pixels
                                     anchor_x='center',
                                     anchor_y='center')
                   for i, item in enumerate(menu_items)]

def draw_menu(window):
    pyglet.gl.glClearColor(1, 1, 1, 1)  # Set the clear color to white
    window.clear()
    game_title_label.draw()  # Draw the game title
    for i, label in enumerate(menu_labels):
        if i == selected_index:
            label.color = (255, 0, 0, 255)  # Highlight the selected item in red
        else:
            label.color = (0, 0, 0, 255)  # Change other items to black for better contrast
        label.draw()

def update_selection(direction):
    global selected_index
    if direction == 'up' and selected_index > 0:
        selected_index -= 1
    elif direction == 'down' and selected_index < len(menu_items) - 1:
        selected_index += 1

def get_selected_action():
    return menu_items[selected_index]
