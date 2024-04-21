import pyglet

# Global variables for settings
volume_settings = {
    'Music Volume': 50,  # Initial volume levels in percentage
    'SFX Volume': 50
}
volume_labels = []
selected_index = 0

def create_volume_labels(window):
    """
    Changes the active Pikemnon in the player's inventory.

    :param player: The player entity.
    :type player: dict
    :param pikemnon_id: The ID of the Pikemnon to activate.
    :type pikemnon_id: str
    :return: The updated player entity.
    :rtype: dict
    """
    global volume_labels
    # Create labels for each volume setting
    volume_labels = [pyglet.text.Label(f"{setting}: {volume_settings[setting]}%",
                                       font_name='Times New Roman',
                                       font_size=24,
                                       x=window.width // 2,
                                       y=window.height // 2 + 50 * (1 - i),
                                       anchor_x='center',
                                       anchor_y='center')
                     for i, setting in enumerate(volume_settings)]

def draw_settings(window):
    """
    Draws the settings on the window.

    :param window: The window to draw the settings on.
    :type window: pyglet.window.Window
    :return: None

    :Global Variables: 
        * volume_labels (list): The list of volume setting labels.
        * selected_index (int): The index of the currently selected setting.
    """
    pyglet.gl.glClearColor(1, 1, 1, 1)  # Set the clear color to white
    window.clear()
    for i, label in enumerate(volume_labels):
        if i == selected_index:
            label.color = (255, 0, 0, 255)  # Highlight the selected setting in red
        else:
            label.color = (0, 0, 0, 255)  # Other settings in black
        label.draw()

def update_selection(direction):
    """
    Updates the selected setting based on the input direction.

    :param direction: The direction to move the selection. Possible values are "up" and "down".
    :type direction: str
    :return: None

    :Global Variables: 
        * selected_index (int): The index of the currently selected setting.
        * volume_settings (dict): The dictionary of volume settings.
    """
    global selected_index
    if direction == 'up' and selected_index > 0:
        selected_index -= 1
    elif direction == 'down' and selected_index < len(volume_settings) - 1:
        selected_index += 1

def adjust_volume(direction):
    """
    Adjusts the volume of the selected setting based on the input direction.

    :param direction: The direction to adjust the volume. Possible values are "increase" and "decrease".
    :type direction: str
    :return: None

    :Global Variables: 
        * selected_index (int): The index of the currently selected setting.
        * volume_settings (dict): The dictionary of volume settings.
        * volume_labels (list): The list of volume setting labels.
    """
    setting = list(volume_settings.keys())[selected_index]
    if direction == 'increase' and volume_settings[setting] < 100:
        volume_settings[setting] += 10  # Increase volume
    elif direction == 'decrease' and volume_settings[setting] > 0:
        volume_settings[setting] -= 10  # Decrease volume
    # Update label text
    volume_labels[selected_index].text = f"{setting}: {volume_settings[setting]}%"

def update_settings_selection(direction):
    """
    Updates the selected setting based on the input direction.

    :param direction: The direction to move the selection. Possible values are "up" and "down".
    :type direction: str
    :return: None

    :Global Variables: 
        * selected_index (int): The index of the currently selected setting.
        * volume_settings (dict): The dictionary of volume settings.
    """
    global selected_index
    if direction == 'up' and selected_index > 0:
        selected_index -= 1
    elif direction == 'down' and selected_index < len(volume_settings) - 1:
        selected_index += 1
