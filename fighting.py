import pyglet

def calculate_damage(attack, defense, power):
    """
    Simple damage calculation formula
    """
    return int(((2 * power * (attack / defense)) / 50) + 2)

class Battle:
    def __init__(self, player_pokemon, npc_pokemon):
        self.player_pokemon = player_pokemon
        self.npc_pokemon = npc_pokemon
        self.current_turn = 'player'

    def player_attack(self):
        """
        Handle player's attack
        """
        power = 50
        damage = calculate_damage(self.player_pokemon['attack'], self.npc_pokemon['defense'], power)
        self.npc_pokemon['health'] -= damage
        print(f"Player's Pokémon caused {damage} damage. NPC Pokémon health is now {self.npc_pokemon['health']}.")
        self.check_battle_end()

    def npc_attack(self):
        """
        Handle NPC's attack
        """
        power = 50
        damage = calculate_damage(self.npc_pokemon['attack'], self.player_pokemon['defense'], power)
        self.player_pokemon['health'] -= damage
        print(f"NPC's Pokémon caused {damage} damage. Player Pokémon health is now {self.player_pokemon['health']}.")
        self.check_battle_end()

    def check_battle_end(self):
        """
        Check if the battle has ended
        """
        if self.player_pokemon['health'] <= 0:
            print("Player's Pokémon fainted. NPC wins!")
            return True
        elif self.npc_pokemon['health'] <= 0:
            print("NPC's Pokémon fainted. Player wins!")
            return True
        return False

    def next_turn(self):
        """
        Progress to the next turn
        """
        if self.current_turn == 'player':
            self.current_turn = 'npc'
            self.npc_attack()
        else:
            self.current_turn = 'player'


def draw_health_bar(x, y, width, height, health_percentage):
    # Draw the health bar background (e.g., gray for depleted health)
    pyglet.graphics.glColor4f(0.5, 0.5, 0.5, 1)  # Gray color
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [x, y, x + width, y, x + width, y + height, x, y + height]))
    
    # Draw the current health (e.g., green for current health)
    pyglet.graphics.glColor4f(0, 1, 0, 1)  # Green color
    current_health_width = width * health_percentage
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [x, y, x + current_health_width, y, x + current_health_width, y + height, x, y + height]))

def fighting_screen(window):
    pyglet.gl.glClearColor(1, 1, 1, 1)
    window.clear()

    # Define the box's coordinates, size, and border thickness
    player_box_x = 40  # Left edge of the window
    player_box_y = 450  # Bottom edge of the window
    player_box_width = 200
    player_box_height = 80
    enemy_box_x = 400  # Left edge of the window
    enemy_box_y = 30  # Bottom edge of the window
    enemy_box_width = 200
    enemy_box_height = 80
    border_thickness = 2

    # Draw black border
    pyglet.graphics.glColor4f(0, 0, 0, 1)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                         ('v2f', [player_box_x - border_thickness, player_box_y - border_thickness, 
                                  player_box_x + player_box_width + border_thickness, player_box_y - border_thickness, 
                                  player_box_x + player_box_width + border_thickness, player_box_y + player_box_height + border_thickness, 
                                  player_box_x - border_thickness, player_box_y + player_box_height + border_thickness])
                        )

    pyglet.graphics.glColor4f(1, 1, 1, 1)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                         ('v2f', [player_box_x, player_box_y, 
                                  player_box_x + player_box_width, player_box_y, 
                                  player_box_x + player_box_width, player_box_y + player_box_height, 
                                  player_box_x, player_box_y + player_box_height])
                        )

    pyglet.graphics.glColor4f(0, 0, 0, 1)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                         ('v2f', [enemy_box_x - border_thickness, enemy_box_y - border_thickness, 
                                  enemy_box_x + enemy_box_width + border_thickness, enemy_box_y - border_thickness, 
                                  enemy_box_x + enemy_box_width + border_thickness, enemy_box_y + enemy_box_height + border_thickness, 
                                  enemy_box_x - border_thickness, enemy_box_y + enemy_box_height + border_thickness])
                        )

    pyglet.graphics.glColor4f(1, 1, 1, 1)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                         ('v2f', [enemy_box_x, enemy_box_y, 
                                  enemy_box_x + enemy_box_width, enemy_box_y, 
                                  enemy_box_x + enemy_box_width, enemy_box_y + enemy_box_height, 
                                  enemy_box_x, enemy_box_y + enemy_box_height])
                        )

    player_label_x = player_box_x + 40
    player_label_y = player_box_y + player_box_height - 10

    enemy_label_x = enemy_box_x + 40
    enemy_label_y = enemy_box_y + enemy_box_height - 10


    player_label = pyglet.text.Label('Player',
                              font_name='Courier',
                              font_size=12,
                              color=(0, 0, 0, 255),
                              x=player_label_x, y=player_label_y,
                              anchor_x='center', anchor_y='center')
    player_label.draw()

    enemy_label = pyglet.text.Label('Enemy',
                              font_name='Courier',
                              font_size=12,
                              color=(0, 0, 0, 255),
                              x=enemy_label_x, y=enemy_label_y,
                              anchor_x='center', anchor_y='center')
    enemy_label.draw()

    player_health_bar_x = player_label_x - 30
    player_health_bar_y = player_label_y - 25
    player_health_bar_width = 100
    player_health_bar_height = 10
    player_health_percentage = 0.1
    draw_health_bar(player_health_bar_x, player_health_bar_y, player_health_bar_width, player_health_bar_height, player_health_percentage)

    enemy_health_bar_x = enemy_label_x - 30
    enemy_health_bar_y = enemy_label_y - 25
    enemy_health_bar_width = 100
    enemy_health_bar_height = 10
    enemy_health_percentage = 0.1
    draw_health_bar(enemy_health_bar_x, enemy_health_bar_y, enemy_health_bar_width, enemy_health_bar_height, enemy_health_percentage)