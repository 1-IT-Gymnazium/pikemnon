import pyglet

class Camera:
    def __init__(self, target, window_width, window_height):
        self.target = target
        self.window_width = window_width
        self.window_height = window_height
        self.offset_x = 0
        self.offset_y = 0

    def update(self):
        self.offset_x = self.window_width // 2 - self.target.sprite.x
        self.offset_y = self.window_height // 2 - self.target.sprite.y

    def begin(self):
        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(self.offset_x, self.offset_y, 0)

    def end(self):
        pyglet.gl.glPopMatrix()
