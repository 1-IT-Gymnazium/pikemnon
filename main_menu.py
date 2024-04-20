import pyglet

# Initialize global variables for menu state
menu_items = ['Start Game', 'Options', 'Exit']
menu_labels = []
selected_index = 0

def create_menu_labels(window):
    global menu_labels
    menu_labels = [pyglet.text.Label(text=item,
                                     font_name='Times New Roman',
                                     font_size=36,
                                     x=window.width // 2,
                                     y=window.height // 2 - 50 * i,
                                     anchor_x='center',
                                     anchor_y='center')
                   for i, item in enumerate(menu_items)]

def draw_menu(window):
    window.clear()
    for i, label in enumerate(menu_labels):
        if i == selected_index:
            label.color = (255, 0, 0, 255)  # Highlight the selected item in red
        else:
            label.color = (255, 255, 255, 255)  # Other items in white
        label.draw()

def update_selection(direction):
    global selected_index
    if direction == 'up' and selected_index > 0:
        selected_index -= 1
    elif direction == 'down' and selected_index < len(menu_items) - 1:
        selected_index += 1

def get_selected_action():
    return menu_items[selected_index]
