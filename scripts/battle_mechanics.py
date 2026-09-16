import random
from constants.inventory_items import all_items

def attack(attacked_health, attacker_damage):
    """randomly picks how much damage the attacker deals based on their base dmg,
    then subtracts the hp from the attacked party"""
    dmg_multipliers = [0.5, 1, 1.25]
    weights = [0.3, 0.5, 0.2]
    choice = random.choices(dmg_multipliers, weights = weights, k = 1)
    actual_damage = choice[0] * attacker_damage
    new = attacked_health - actual_damage
    attacked_health = new if new > 0 else 0
    return attacked_health, actual_damage

def remove_item(inventory, item):
    """removes given inventory item and returns appropriate boost"""
    inventory.remove(item)
    if item == "Bandage":
        return ("HP", 20), inventory
    if item == "Painkiller":
        return ("HP", 35), inventory
    if item == "Serum":
        return ("HP", 50), inventory
    if item == "Meat":
        return ("DMG", 2), inventory
    return ("KILL", 0), inventory ## 100 dollar bill insta kills current enemy

def hp_change(item, current_health, max_health):
    """checks if item is hp up and if hp change is possible SIMULTANEOUSLY"""
    if item in ("100 Dollar Bill", "Meat"):
        return True
    if item == "Bandage":
        new = 20
    elif item == "Painkiller":
        new = 35
    else:
        new = 50
    if current_health == max_health:
        return False
    if current_health + new <= max_health:
        return True
    return True

def add_hp(current_health, max_health, new):
    """adds new hp to player"""
    result = current_health + new
    return result if result <= max_health else max_health

def pick_items():
    """selects 2 items at random among which at least one hp+"""
    chosen_items = []
    health_items = all_items[0:2]
    weights = [0.6, 0.4]
    health_item = random.choices(health_items, weights = weights, k = 1)
    chosen_items.append(health_item[0])
    other_items = all_items[2:5]
    weights = [0.45, 0.35, 0.2]
    other_item = random.choices(other_items, weights = weights, k = 1)
    chosen_items.append(other_item[0])
    return chosen_items
