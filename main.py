import pyglet
from pyglet.gl import *
from pyglet.window import key
from player import Player

# Window dimensions
window_width = 800
window_height = 600

# Create a window
window = pyglet.window.Window(window_width, window_height, "Pikemnon")

player = Player('assets/player.png', window.width//2, window.height//2)

key_state = {
    'up': False,
    'down': False,
    'left': False,
    'right': False
}

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.W:
        key_state['up'] = True
    elif symbol == key.S:
        key_state['down'] = True
    elif symbol == key.A:
        key_state['left'] = True
    elif symbol == key.D:
        key_state['right'] = True

@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.W:
        key_state['up'] = False
    elif symbol == key.S:
        key_state['down'] = False
    elif symbol == key.A:
        key_state['left'] = False
    elif symbol == key.D:
        key_state['right'] = False

def update(dt):
    player.update(dt, key_state)

pyglet.clock.schedule_interval(update, 1/60.0)


@window.event
def on_draw():
    window.clear()
    player.draw()

if __name__ == '__main__':
    pyglet.app.run()
