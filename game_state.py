import json
import random


fighton = False
current_npc = None

def start_fight(npc):
    global fighton, current_npc
    fighton = True
    current_npc = npc if npc != "wild" else create_wild_pokemon()

def get_fight_status():
    return fighton

def end_fight():
    global fighton, current_npc
    fighton = False
    current_npc = None

def get_current_npc():
    return current_npc


def create_wild_pokemon():
    npc = {}
    npc['pikemnons'] = []
    npc['pikemnon_index'] = 0
    with open('pokemon.json') as f:
        data = json.load(f)
    pikemnon = random.choice(list(data.keys()))
    pik = data[pikemnon]
    pik['name'] = pikemnon
    pik['current_health'] = pik['health']
    pik['stage'] = {}
    pik['stage']['attack'] = 0
    npc['pikemnons'].append(pik)
    return npc