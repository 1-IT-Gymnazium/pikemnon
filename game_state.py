fighton = False
current_npc = None

def start_fight(npc):
    global fighton, current_npc
    fighton = True
    current_npc = npc

def get_fight_status():
    return fighton

def end_fight():
    global fighton, current_npc
    fighton = False
    current_npc = None

def get_current_npc():
    return current_npc