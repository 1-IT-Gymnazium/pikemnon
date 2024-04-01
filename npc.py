import json
from entity import create_entity
from player import change_move
from game_state import start_fight

def create_npc(image_file, x, y, look, pikemnons):
    npc = create_entity(image_file, x, y)
    npc['look'] = look
    npc['fought'] = False
    npc['id'] = id
    npc['pikemnons'] = []
    npc['pikemnon_index'] = 0
    with open('pokemon.json') as f:
        data = json.load(f)
    for pikemnon in pikemnons:
        if pikemnon in data:
            pik = data[pikemnon]
            pik['name'] = pikemnon
            pik['current_health'] = pik['health']
            pik['stage'] = {}
            pik['stage']['attack'] = 0
            npc['pikemnons'].append(pik)
    return npc


def update_npc(npc, player):
    npcX = npc['sprite'].x
    npcY = npc['sprite'].y
    playerX = player['sprite'].x
    playerY = player['sprite'].y

    xVal = npcX - playerX
    yVal = npcY - playerY

    lookDir = npc['look']
    if not npc['fought']:
        if lookDir == 'down':
            if xVal > -10 and xVal < 10 and yVal < 300 and yVal > 0:
                change_move(player, False)
                npc['sprite'].y -= 1
                if yVal < 30:
                    fighting(npc, player)
        elif lookDir == 'up':
            if xVal > -10 and xVal < 10 and yVal > -300 and yVal < 0:
                change_move(player, False)
                npc['sprite'].y += 1

                if yVal > -30:
                    fighting(npc, player)
        elif lookDir == 'right':
            if yVal > -10 and yVal < 10 and xVal > -300 and xVal < 0:
                change_move(player, False)
                npc['sprite'].x += 1

                if xVal > -30:
                    fighting(npc, player)
        elif lookDir == 'left':
            if yVal > -10 and yVal < 10 and xVal < 300 and xVal > 0:
                change_move(player, False)
                npc['sprite'].x -= 1

                if xVal < 30:
                    fighting(npc, player)

def fighting(npc, player):
    start_fight(npc)
    npc['fought'] = True
    change_move(player, True)
