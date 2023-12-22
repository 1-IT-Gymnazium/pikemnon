import pyglet

# Initialize variables
target = None
window_width = 0
window_height = 0
offset_x = 0
offset_y = 0

def set_camera_target(new_target):
    global target
    target = new_target
    print(target['sprite'].x)

def set_camera_window_size(new_window_width, new_window_height):
    global window_width, window_height
    window_width = new_window_width
    window_height = new_window_height

def update_camera():
    global offset_x, offset_y, window_width, window_height, target
    offset_x = window_width // 2 - target['sprite'].x
    offset_y = window_height // 2 - target['sprite'].y

def begin_camera():
    pyglet.gl.glPushMatrix()
    pyglet.gl.glTranslatef(offset_x, offset_y, 0)

def end_camera():
    pyglet.gl.glPopMatrix()