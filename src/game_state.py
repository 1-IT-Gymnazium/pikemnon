import json
import random

from data.pikemnon_data import get_pikemnon_data


fighton = False
current_npc = None

fight_status = None

main_menu_status = "main"

display_text = False
def start_fight(npc: str) -> None:
    """
    Starts a fight with an NPC or a wild Pokemon.

    :param npc: The NPC to start a fight with. If "wild", a wild Pokemon is created for the fight.
    :type npc: str
    :return: None

    :Global Variables: 
        * fighton (bool): Whether a fight is currently on.
        * current_npc (str): The NPC currently in a fight with.
    """
    global fighton, current_npc
    fighton = True
    current_npc = npc if npc != "wild" else create_wild_pokemon()


def get_fight_status() -> bool:
    """
    Returns the current fight status.

    :return: Whether a fight is currently on.
    :rtype: bool

    :Global Variables: 
        * fighton (bool): Whether a fight is currently on.
    """
    return fighton


def set_fight_stat(value: str) -> None:
    """
    Sets the fight status.

    :param value: The value to set the fight status to.
    :type value: str
    :return: None

    :Global Variables: 
        * fight_status (str): The current fight status.
    """
    global fight_status
    fight_status = value


def get_fight_stat() -> str:
    """
    Returns the current fight status.

    :return: The current fight status.
    :rtype: str

    :Global Variables: 
        * fight_status (str): The current fight status.
    """
    return fight_status


def end_fight() -> None:
    """
    Ends the current fight.

    :return: None

    :Global Variables: 
        * fighton (bool): Whether a fight is currently on.
        * current_npc (str): The NPC currently in a fight with.
    """
    global fighton, current_npc
    fighton = False
    current_npc = None


def get_current_npc() -> str:
    """
    Returns the NPC currently in a fight with.

    :return: The NPC currently in a fight with.
    :rtype: str

    :Global Variables: 
        * current_npc (str): The NPC currently in a fight with.
    """
    return current_npc


def create_wild_pokemon():
    """
    Creates a wild Pokemon for a fight.

    This function randomly selects a Pokemon from the available Pokemon data, sets its current health to its maximum health, and adds it to the NPC's list of Pokemon.

    :return: A dictionary representing the NPC with the wild Pokemon.
    :rtype: dict

    :Global Variables: 
        * data (dict): The available Pokemon data.
    """
    npc = {}
    npc['pikemnons'] = []
    npc['pikemnon_index'] = 0
    data = get_pikemnon_data()
    pikemnon = random.choice(list(data.keys()))
    pik = data[pikemnon]
    pik['name'] = pikemnon
    pik['current_health'] = pik['health']
    pik['stage'] = {}
    pik['stage']['attack'] = 0
    pik['wild'] = True
    npc['pikemnons'].append(pik)
    return npc

def get_main_menu() -> bool:
    """
    Returns the current status of the main menu.

    :return: The current status of the main menu.
    :rtype: bool

    :Global Variables: 
        * main_menu_status (bool): The current status of the main menu.
    """
    return main_menu_status


def set_main_menu(value: bool) -> None:
    """
    Sets the status of the main menu.

    :param value: The value to set the main menu status to.
    :type value: bool
    :return: None

    :Global Variables: 
        * main_menu_status (bool): The current status of the main menu.
    """
    global main_menu_status
    main_menu_status = value


def get_display_text() -> str:
    """
    Returns the current display text.

    :return: The current display text.
    :rtype: str

    :Global Variables: 
        * display_text (str): The current display text.
    """
    return display_text


def set_display_text(value: str) -> None:
    """
    Sets the display text.

    :param value: The value to set the display text to.
    :type value: str
    :return: None

    :Global Variables: 
        * display_text (str): The current display text.
    """
    global display_text
    display_text = value