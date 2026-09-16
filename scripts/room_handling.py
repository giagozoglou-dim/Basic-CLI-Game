import json
import random
from scripts.save_file_management import main_dir

def populate_room(boss_room):
    """fills room with enemies"""
    file_path = main_dir / "constants"
    enemies_file_path = file_path / "enemies.json"
    bosses_file_path = file_path / "bosses.json"
    if not boss_room:
        try:
            with open(enemies_file_path, "r", encoding = "utf-8") as f:
                enemies = json.load(f)
            chosen_enemies = random.choices(tuple(enemies), k = 4)
        except OSError:
            print('Critical Error: "enemies.json" not found.')
            quit()
        for i in range(3):
            yield chosen_enemies[i], enemies[chosen_enemies[i]]
    else:
        try:
            with open(bosses_file_path, "r", encoding = "utf-8") as f:
                bosses = json.load(f)
            chosen_boss = random.choice(tuple(bosses))
        except OSError:
            print('Critical Error: "bosses.json" not found.')
            quit()
        yield chosen_boss, bosses[chosen_boss]
