import pyglet

# Initialize variables
target = None
window_width = 0
window_height = 0
offset_x = 0
offset_y = 0

def set_camera_target(new_target):
    """
    Sets the target for the camera.

    This function updates the global target variable to the new target object.

    :param new_target: The new target object for the camera.
    :type new_target: object
    :return: None

    :Global Variables: 
        * target (object): The current target of the camera.
    """
    global target
    target = new_target

def set_camera_window_size(new_window_width, new_window_height):
    """
    Sets the target for the camera.

    This function updates the global target variable to the new target object.

    :param new_target: The new target object for the camera.
    :type new_target: object
    :return: None

    :Global Variables: 
        * target (object): The current target of the camera.
    """
    global window_width, window_height
    window_width = new_window_width
    window_height = new_window_height

def update_camera():
    """
    Updates the camera's position based on the target's position.

    This function calculates the new offsets for the camera based on the target's position and the window size.
    The camera is always centered on the target.

    :return: None

    :Global Variables: 
        * offset_x (int): The current x-offset of the camera.
        * offset_y (int): The current y-offset of the camera.
        * window_width (int): The current width of the camera window.
        * window_height (int): The current height of the camera window.
        * target (dict): The current target of the camera, which is a dictionary containing a 'sprite' key.
    """
    global offset_x, offset_y, window_width, window_height, target
    offset_x = window_width // 2 - target['sprite'].x
    offset_y = window_height // 2 - target['sprite'].y

def begin_camera():
    """
    Begins the camera transformation.

    This function pushes the current matrix stack down by one, duplicating the current matrix.
    Then it applies a translation transformation to the matrix using the current camera offsets.

    :return: None

    :Global Variables: 
        * offset_x (int): The current x-offset of the camera.
        * offset_y (int): The current y-offset of the camera.
    """
    pyglet.gl.glPushMatrix()
    pyglet.gl.glTranslatef(offset_x, offset_y, 0)

def end_camera():
    """
    Ends the camera transformation.

    This function pops the current matrix stack up by one, removing the current matrix.

    :return: None
    """
    pyglet.gl.glPopMatrix()