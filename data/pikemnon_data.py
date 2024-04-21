def get_pikemnon_data():
    """
    Returns a dictionary representing the Pokemon's data.

    :return: A dictionary representing the Pokemon's data.
    :rtype: dict
    """
    return {
        "Bulbasaur": {
            "health": 45,
            "attack": 49,
            "defense": 49,
            "type": "grass",
            "moves": {
                "growl": {"power": 1, "move_type": "debuff", "type": "normal", "target_stat": "attack", "pp": 40},
                "tackle": {"power": 40, "move_type": "attack", "type": "normal", "pp": 35},
                "vine whip": {"power": 45, "move_type": "attack", "type": "grass", "pp": 25},
                "Growth": {"power": 1, "move_type": "buff", "type": "normal", "target_stat": "attack", "pp": 20}
            }
        },
        "Charmander": {
            "health": 39,
            "attack": 52,
            "defense": 43,
            "type": "fire",
            "moves": {
                "growl": {"power": 1, "move_type": "debuff", "type": "normal", "target_stat": "attack", "pp": 40},
                "scratch": {"power": 40, "move_type": "attack", "type": "normal", "pp": 35},
                "ember": {"power": 40, "move_type": "attack", "type": "fire", "pp": 25},
                "dragon breath": {"power": 60, "move_type": "attack", "type": "fire", "pp": 20}
            }
        },
        "Squirtle": {
            "health": 44,
            "attack": 48,
            "defense": 65,
            "type": "water",
            "moves": {
                "tackle": {"power": 40, "move_type": "attack", "type": "normal", "pp": 35},
                "tail whip": {"power": 1, "move_type": "debuff", "type": "normal", "target_stat": "defense", "pp": 30},
                "water gun": {"power": 40, "move_type": "attack", "type": "water", "pp": 25},
                "withdraw": {"power": 1, "move_type": "buff", "type": "water", "target_stat": "defense", "pp": 40}
            }
        },
        "Pikachu": {
            "health": 35,
            "attack": 55,
            "defense": 40,
            "type": "electric",
            "moves": {
                "growl": {"power": 1, "move_type": "debuff", "type": "normal", "target_stat": "attack", "pp": 40},
                "quick attack": {"power": 40, "move_type": "attack", "type": "normal", "pp": 30},
                "thunder shock": {"power": 40, "move_type": "attack", "type": "electric", "pp": 30},
                "electro ball": {"power": 60, "move_type": "attack", "type": "electric", "pp": 10}
            }
        },
        "Jigglypuff": {
            "health": 115,
            "attack": 45,
            "defense": 20,
            "type": "normal",
            "moves": {
                "sing": {"power": 1, "move_type": "debuff", "type": "normal", "target_stat": "sleep", "pp": 15},
                "pound": {"power": 40, "move_type": "attack", "type": "normal", "pp": 35},
                "disable": {"power": 1, "move_type": "debuff", "type": "normal", "target_stat": "move", "pp": 20},
                "double slap": {"power": 15, "move_type": "attack", "type": "normal", "pp": 10}
            }
        },
        "Psyduck": {
            "health": 50,
            "attack": 52,
            "defense": 48,
            "type": "water",
            "moves": {
                "scratch": {"power": 40, "move_type": "attack", "type": "normal", "pp": 35},
                "tail whip": {"power": 1, "move_type": "debuff", "type": "normal", "target_stat": "defense", "pp": 30},
                "water gun": {"power": 40, "move_type": "attack", "type": "water", "pp": 25},
                "confusion": {"power": 50, "move_type": "attack", "type": "psychic", "pp": 25}
            }
        },
        "Eevee": {
            "health": 55,
            "attack": 55,
            "defense": 50,
            "type": "normal",
            "moves": {
                "tackle": {"power": 40, "move_type": "attack", "type": "normal", "pp": 35},
                "tail whip": {"power": 1, "move_type": "debuff", "type": "normal", "target_stat": "defense", "pp": 30},
                "bite": {"power": 60, "move_type": "attack", "type": "dark", "pp": 25},
                "sand attack": {"power": 1, "move_type": "debuff", "type": "ground", "target_stat": "accuracy", "pp": 15}
            }
        }
    }