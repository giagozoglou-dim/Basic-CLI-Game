"""for dumping the correct json files"""
import json
from scripts.save_file_management import const_path

enemy_path = const_path / "enemies.json"
boss_path = const_path / "bosses.json"
char_path = const_path / "default_characters.json"

enemy_dict = {
    "Snake": {
        "health": 15,
        "damage": 7
    },
    "Skeleton": {
        "health": 55,
        "damage": 7
    },
    "The Fanatic": {
        "health": 40,
        "damage": 12
    },
    "Spider": {
        "health": 10,
        "damage": 7
    },
    "Mad Mosquito": {
        "health": 20,
        "damage": 14
    },
    "Kamikaze": {
        "health": 16,
        "damage": 25
    },
    "Headless Knight": {
        "health": 30,
        "damage": 10
    },
    "Bishop": {
        "health": 45,
        "damage": 10
    },
    "Phantom": {
        "health": 35,
        "damage": 7
    },
    "Minion": {
        "health": 25,
        "damage": 12
    },
    "Sewer Rat": {
        "health": 40,
        "damage": 12
    }
}
boss_dict = {
    "Jacob": {
        "health": 150,
        "damage": 17
    },
    "The Keeper": {
        "health": 120,
        "damage": 21
    },
    "Magdalene": {
        "health": 180,
        "damage": 16
    },
    "The Forlorn": {
        "health": 90,
        "damage": 32
    }
}

## for game_status:
## 0 signifies game lost, 1 game in progress, 2 game won
char_dict = {
  "Jax": {
    "name": "Jax",
    "current_health": 150,
    "max_health": 150,
    "damage": 15,
    "inventory": [
      "Bandage"
    ],
    "current_room": 1,
    "game_status": 1
  },
  "Casper": {
    "name": "Casper",
    "current_health": 100,
    "max_health": 100,
    "damage": 20,
    "inventory": [
      "Bandage"
    ],
    "current_room": 1,
    "game_status": 1
  },
  "Blitz": {
    "name": "Blitz",
    "current_health": 50,
    "max_health": 50,
    "damage": 35,
    "inventory": [
      "Painkiller"
    ],
    "current_room": 1,
    "game_status": 1
  }
}

def ensure_enemy_validity():
    """ensures enemies.json exists and contains the right defaults"""
    try:
        with open(enemy_path, "w", encoding = "utf-8") as f:
            json.dump(enemy_dict, f, indent = 2)
    except OSError:
        print(OSError)
        quit()

def ensure_boss_validity():
    """ensures bosses.json exists and contains the right defaults"""
    try:
        with open(boss_path, "w", encoding = "utf-8") as f:
            json.dump(boss_dict, f, indent = 2)
    except OSError:
        print(OSError)
        quit()

def ensure_character_validity():
    """ensures default_characters.json exists and contains the right defaults"""
    try:
        with open(char_path, "w", encoding = "utf-8") as f:
            json.dump(char_dict, f, indent = 2)
    except OSError:
        print(OSError)
        quit()
