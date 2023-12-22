import pyglet
from pyglet.gl import *

def create_entity(image_file, x, y, health=100):
    image = pyglet.resource.image(image_file)

    texture = image.get_texture()
    glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    sprite = pyglet.sprite.Sprite(img=image, x=x, y=y)
    sprite.scale = 4

    return {'image': image, 'sprite': sprite, 'health': health}

def draw_entity(entity):
    entity['sprite'].draw()

def update_entity(entity, dt):
    pass
