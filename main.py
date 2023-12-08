import pyglet
from pyglet.gl import *
from pyglet.window import key

# Window dimensions
window_width = 800
window_height = 600

# Create a window
window = pyglet.window.Window(window_width, window_height, "Pikemnon")

image = pyglet.resource.image('player.png')

# Ensure the image scales pixel-perfectly
texture = image.get_texture()
glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameteri(texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

# Create a sprite and scale it up
sprite = pyglet.sprite.Sprite(img=image, x=window.width//2, y=window.height//2)
sprite.scale = 4

# Draw the sprite
@window.event
def on_draw():
    window.clear()
    sprite.draw()

if __name__ == '__main__':
    pyglet.app.run()
