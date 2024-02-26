from entity import create_entity, update_entity


def create_player(image_file, x, y, speed=220):
    player = create_entity(image_file, x, y)
    player['speed'] = speed
    return player


def update_player(player, dt, key_state):
    dx = dy = 0
    if key_state['up']:
        dy += player['speed'] * dt
    if key_state['down']:
        dy -= player['speed'] * dt
    if key_state['left']:
        dx -= player['speed'] * dt
    if key_state['right']:
        dx += player['speed'] * dt

    # Normalize
    length = (dx**2 + dy**2)**0.5
    if length != 0:
        dx, dy = dx / length * player['speed'] * dt, dy / length * player['speed'] * dt

    player['sprite'].x += dx
    player['sprite'].y += dy
    update_entity(player, dt)
