import json
import random


fighton = False
current_npc = None

fight_status = None

main_menu_status = "main"

display_text = False

def start_fight(npc):
    global fighton, current_npc
    fighton = True
    current_npc = npc if npc != "wild" else create_wild_pokemon()

def get_fight_status():
    return fighton

def set_fight_stat(value):
    global fight_status
    fight_status = value

def get_fight_stat():
    return fight_status

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
    with open('data/pokemon.json') as f:
        data = json.load(f)
    pikemnon = random.choice(list(data.keys()))
    pik = data[pikemnon]
    pik['name'] = pikemnon
    pik['current_health'] = pik['health']
    pik['stage'] = {}
    pik['stage']['attack'] = 0
    pik['wild'] = True
    npc['pikemnons'].append(pik)
    return npc

def get_main_menu():
    return main_menu_status

def set_main_menu(value):
    global main_menu_status
    main_menu_status = value

def get_display_text():
    return display_text

def set_display_text(value):
    global display_text
    display_text = value