import pyglet

# Global variables for settings
volume_settings = {
    'Music Volume': 50,  # Initial volume levels in percentage
    'SFX Volume': 50
}
volume_labels = []
selected_index = 0

def create_volume_labels(window):
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
    pyglet.gl.glClearColor(1, 1, 1, 1)  # Set the clear color to white
    window.clear()
    for i, label in enumerate(volume_labels):
        if i == selected_index:
            label.color = (255, 0, 0, 255)  # Highlight the selected setting in red
        else:
            label.color = (0, 0, 0, 255)  # Other settings in black
        label.draw()

def update_selection(direction):
    global selected_index
    if direction == 'up' and selected_index > 0:
        selected_index -= 1
    elif direction == 'down' and selected_index < len(volume_settings) - 1:
        selected_index += 1

def adjust_volume(direction):
    setting = list(volume_settings.keys())[selected_index]
    if direction == 'increase' and volume_settings[setting] < 100:
        volume_settings[setting] += 10  # Increase volume
    elif direction == 'decrease' and volume_settings[setting] > 0:
        volume_settings[setting] -= 10  # Decrease volume
    # Update label text
    volume_labels[selected_index].text = f"{setting}: {volume_settings[setting]}%"
