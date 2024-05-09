import json
import random
from data.pikemnon_data import get_pikemnon_data
from src.entity import create_entity
from src.player import change_move
from src.game_state import start_fight

def create_npc(image_file, x, y, look, pikemnons: int):
    """
    Creates a Non-Player Character (NPC) with specified attributes and a set of Pikemnons.

    This function creates an NPC with a specified image, position, look direction, and number of Pikemnons.
    The Pikemnons are randomly chosen from a JSON file of available Pikemnons.

    :param image_file: The file path of the image for the NPC.
    :type image_file: str
    :param x: The x-coordinate of the NPC's position.
    :type x: int
    :param y: The y-coordinate of the NPC's position.
    :type y: int
    :param look: The direction the NPC is looking ('up', 'down', 'left', 'right').
    :type look: str
    :param pikemnons: The number of Pikemnons the NPC has.
    :type pikemnons: int
    :return: A dictionary representing the NPC, with keys for image, position, look direction, fight status, Pikemnons, and current Pikemnon.
    :rtype: dict
    """
    npc = create_entity(image_file, x, y)
    npc['look'] = look
    npc['fought'] = False
    npc['pikemnons'] = []
    npc['pikemnon_index'] = 0
    data = get_pikemnon_data()
    for _ in range(pikemnons):
        pikemnon = random.choice(list(data.keys()))
        pik = data[pikemnon]
        pik['name'] = pikemnon
        pik['current_health'] = pik['health']
        pik['stage'] = {}
        pik['stage']['attack'] = 0
        pik['stage']['defense'] = 0
        npc['pikemnons'].append(pik)
    return npc


def update_npc(npc, player):
    """
    Determines if the player is colliding with an empty tile.

    This function calculates the player's tile coordinates and checks all tiles the player is on. If the player is on an empty tile, it returns True. Otherwise, it returns False.

    :param player: The player.
    :type player: dict
    :return: Whether the player is colliding with an empty tile.
    :rtype: bool

    :Global Variables: 
        * current_map (list): The current map.
    """
    npcX = npc['sprite'].x
    npcY = npc['sprite'].y
    playerX = player['sprite'].x
    playerY = player['sprite'].y

    player_player = False

    for pik in player['pikemnons']:
        if pik['current_health'] > 0:
            player_player = True

    if not player_player:
        return

    xVal = npcX - playerX
    yVal = npcY - playerY

    lookDir = npc['look']
    if not npc['fought']:
        if lookDir == 'down':
            if xVal > -10 and xVal < 10 and yVal < 150 and yVal > 0:
                change_move(player, False)
                npc['sprite'].y -= 1
                if yVal < 30:
                    fighting(npc, player)
        elif lookDir == 'up':
            if xVal > -10 and xVal < 10 and yVal > -150 and yVal < 0:
                change_move(player, False)
                npc['sprite'].y += 1

                if yVal > -30:
                    fighting(npc, player)
        elif lookDir == 'right':
            if yVal > -10 and yVal < 10 and xVal > -150 and xVal < 0:
                change_move(player, False)
                npc['sprite'].x += 1

                if xVal > -30:
                    fighting(npc, player)
        elif lookDir == 'left':
            if yVal > -10 and yVal < 10 and xVal < 150 and xVal > 0:
                change_move(player, False)
                npc['sprite'].x -= 1

                if xVal < 30:
                    fighting(npc, player)

def fighting(npc, player):
    """
    Starts a fight between the NPC and the player.

    This function starts a fight with the NPC, sets the NPC's 'fought' status to True, and stops the player's movement.

    :param npc: The NPC to fight.
    :type npc: dict
    :param player: The player.
    :type player: dict
    :return: None

    :Global Variables: 
        * npc['fought'] (bool): Whether the NPC has fought the player.
        * player['sprite'] (pyglet.sprite.Sprite): The player's sprite.
    """
    start_fight(npc)
    npc['fought'] = True
    change_move(player, True)
