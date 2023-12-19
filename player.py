import pyglet
from entity import Entity

class Player(Entity):
    def __init__(self, image_file, x, y):
        super().__init__(image_file, x, y)
        self.speed = 200

    def update(self, dt, key_state):
        dx = dy = 0
        if key_state['up']:
            dy += self.speed * dt
        if key_state['down']:
            dy -= self.speed * dt
        if key_state['left']:
            dx -= self.speed * dt
        if key_state['right']:
            dx += self.speed * dt
        
        # Normalize
        length = (dx**2 + dy**2)**0.5
        if length != 0:
            dx, dy = dx / length * self.speed * dt, dy / length * self.speed * dt

        self.sprite.x += dx
        self.sprite.y += dy
        super().update(dt)
