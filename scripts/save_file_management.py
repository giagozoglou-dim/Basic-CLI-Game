import os
import json
from pathlib import Path
from constants.inventory_items import all_items

parent_dir = Path(__file__).resolve().parent
main_dir = Path(parent_dir).resolve().parent
save_files_path = main_dir / "save_files"
const_path = main_dir / "constants"
temp_path = const_path / "temp.txt"

def new_save(total_saves, character):
    """creates new save file with default stats for the selected character"""
    index = total_saves.index("No save file found.")
    file_name = f"save_{index}.json"
    file_path = save_files_path / file_name
    default_stats_path: Path = const_path / "default_characters.json"

    try:
        with open(default_stats_path, "r", encoding = "utf-8") as f:
            default_stats = json.load(f)
    except FileNotFoundError:
        print('Critical Error: "default_characters.json" not found')
        quit()

    if not os.path.exists(save_files_path):
        os.makedirs(save_files_path)
        print("Created directory: /save-files")

    try:
        with open(file_path, "x", encoding = "utf-8") as f:
            json.dump(default_stats[character], f)
            print(f"Created file: {file_name}")
    except FileExistsError:
        ## edge case where user creates save file themselves whilst in the char selection screen
        print(f'Error: File "{file_name}" already exists.')
        quit()

def fetch_saves():
    """pulls all save files from the save_files directory and returns them as a list"""
    total_saves = ["No save file found."] * 3
    expected_name = ["save_0.json", "save_1.json", "save_2.json"]
    l = 0
    try:
        for file_name in os.listdir(save_files_path):
            if file_name in expected_name and os.path.isfile(os.path.join(save_files_path, file_name)):
                save_is_valid = check_save_validity(file_name)
                l = int(file_name[5])
                if save_is_valid[0] and save_is_valid[1] is not None:
                    expected_name.remove(file_name)
                    print(f'Successfully fetched "{file_name}".')
                    status = check_game_status(file_name)
                    try:
                        if status == "Lost":
                            total_saves[l] = "Game Lost!"
                        elif status == "Won":
                            total_saves[l] = "Game Won!"
                        else:
                            total_saves[l] = save_is_valid[1]
                    except IndexError:
                        continue
                else:
                    total_saves[l] = "Failed to fetch save file."
                    print(f'Error: file "{file_name}" has been altered.')
                l += 1
    except NotADirectoryError:
        print('Critical Error: "save_files" is not a folder.')
        quit()
    return total_saves, l

def check_save_validity(file_name):
    """checks if save file contents are valid"""
    stat_categories = ("name", "current_health", "max_health", "damage", "current_room", "inventory", "game_status")

    with open(os.path.join(save_files_path, file_name), "r", encoding = "utf-8") as f:
        save_data = json.load(f)
        if all(key in save_data for key in stat_categories):
            ## for game_status:
            ## 0 signifies game lost, 1 game in progress, 2 game won
            return (
                save_data["name"] in ("Casper", "Jax", "Blitz")
                and save_data["current_health"] >= 0
                and max_health_checker(save_data["name"], save_data["max_health"])
                and save_data["damage"] > 0
                and isinstance(save_data["inventory"], list)
                and len(save_data["inventory"]) <= 5
                and all(item in all_items for item in save_data["inventory"])
                and save_data["game_status"] in (0, 1, 2),
                save_data["name"])
    return (False, None)

def max_health_checker(char, health):
    """checks if max player health matches the character's"""
    if char == "Jax":
        return health == 150
    if char == "Casper":
        return health == 100
    return health == 50

def delete_save(file_name):
    """deletes a save file"""
    try:
        os.remove(os.path.join(save_files_path, file_name))
        print(f'Error: "{file_name}" has been deleted.')
    except FileNotFoundError:
        ## edge case where user deletes save file themselves after opening the delete save
        ## file menu but BEFORE they confirm the save file deletion
        print(f'Error: "{file_name}" not found.')

def pull_save(file_name):
    """pulls save file data"""
    try:
        with open(os.path.join(save_files_path, file_name), "r", encoding = "utf-8") as f:
            stats = json.load(f)
        create_temp(file_name)
        return stats
    except FileNotFoundError:
        ## similar to delete_save
        print(f'Error: File "{file_name}" not found')
        quit()

def create_temp(file_name):
    """creates temp.txt which stores save file name"""
    try:
        with open(temp_path, "w", encoding = "utf-8") as f:
            f.write(file_name)
    except OSError:
        print('Critical Error: Failed to save current game file to "temp.txt"')
        quit()

def load_temp():
    """attempts to fetch save file loaded from pull_save();
    returns None if no save was selected yet"""
    try:
        with open(temp_path, "r", encoding = "utf-8") as f:
            save = f.read().strip()
    except FileNotFoundError:
        # No active save has been created yet. This is a normal startup state.
        return None
    if save not in ("save_0.json", "save_1.json", "save_2.json"):
        print('Critical Error: Could not fetch save file from "temp.txt".')
        return None
    return save

def pull_stats():
    """finds chosen save file then pulls all relevant stats;
    returns None, None when no temp marker exists"""
    save_file = load_temp()
    if save_file is None:
        return None, None
    stats = pull_save(save_file)
    return save_file, stats

def file_save(new_stats, file_name):
    """increases current_room count by 1 and
    saves the user's progress on the respective save file"""
    if new_stats["current_room"] != 6:
        new_stats["current_room"] += 1
    file_path = save_files_path / file_name
    try:
        with open(file_path, "w", encoding = "utf-8") as f:
            json.dump(new_stats, f, indent = 2)
            print(f"Progress saved for room {new_stats["current_room"] - 1}!")
    except OSError:
        print(OSError)

def check_game_status(file_name):
    """checks if game has either been won or lost on a save file"""
    stats = pull_save(file_name)
    if stats["game_status"] == 0:
        return "Lost"
    if stats["game_status"] == 2:
        return "Won"
    return "In progress"
