import pyglet
from pyglet.gl import *


def create_entity(image_file, x, y, health=100):
    """
    Creates an entity with specified attributes.

    This function creates an entity with a specified image, position, and health.
    The image is scaled up by a factor of 4.

    :param image_file: The file path of the image for the entity.
    :type image_file: str
    :param x: The x-coordinate of the entity's position.
    :type x: int
    :param y: The y-coordinate of the entity's position.
    :type y: int
    :param health: The health of the entity. Default is 100.
    :type health: int
    :return: A dictionary representing the entity, with keys for image, sprite, and health.
    :rtype: dict
    """
    image = pyglet.resource.image(image_file)

    texture = image.get_texture()
    glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    sprite = pyglet.sprite.Sprite(img=image, x=x, y=y)
    sprite.scale = 4

    return {'image': image, 'sprite': sprite, 'health': health}


def draw_entity(entity):
    """
    Draws the entity on the screen.

    This function calls the draw method on the entity's sprite.

    :param entity: The entity to be drawn. The entity should be a dictionary with a 'sprite' key.
    :type entity: dict
    :return: None
    """
    entity['sprite'].draw()

