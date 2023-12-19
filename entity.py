import pyglet
from pyglet.gl import *

class Entity:
    def __init__(self, image_file, x, y, health=100):
        self.image = pyglet.resource.image(image_file)

        texture = self.image.get_texture()
        glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        self.sprite = pyglet.sprite.Sprite(img=self.image, x=x, y=y)
        self.sprite.scale = 4

        self.health = health

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        pass
