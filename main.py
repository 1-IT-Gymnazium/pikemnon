import pyglet
from pyglet.gl import *
from entity import Entity

# Window dimensions
window_width = 800
window_height = 600

# Create a window
window = pyglet.window.Window(window_width, window_height, "Pikemnon")

player = Entity('assets/player.png', window.width//2, window.height//2)

# Draw the sprite
@window.event
def on_draw():
    window.clear()
    player.draw()

if __name__ == '__main__':
    pyglet.app.run()
