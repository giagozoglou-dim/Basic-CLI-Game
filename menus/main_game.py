import curses
from time import monotonic, sleep
from constants import colors
from constants.inventory_items import find_desc
from scripts.room_handling import populate_room
import scripts.battle_mechanics as battle

def room_screen(stdscr, width, y_center, i):
    """shows the room the player is in"""
    stdscr.clear()
    hint = f"You are currently in room {i}/6."
    if i == 5:
        hint2 = "1 room left until the boss room!"
    if i == 6:
        hint2 = "This is the boss room!"
    else:
        hint2 = f"{6-i} rooms left until the boss room!"

    color = colors.GREEN if i < 6 else colors.RED
    hint_center = (width - len(hint)) // 2
    hint2_center = (width - len(hint2)) // 2
    stdscr.addstr(y_center - 2, hint_center, hint)
    stdscr.refresh()
    sleep(1)
    stdscr.addstr(y_center, hint2_center, hint2, color)
    stdscr.refresh()
    sleep(2)

    if i == 6:
        hint = "You've been granted +4 DMG!"
        hint_center = (width - len(hint)) // 2
        stdscr.addstr(y_center, hint_center, hint, colors.YELLOW | curses.A_ITALIC)

def fight_enemy_screen(stdscr, width, height, y_center, stats: dict, room):
    """displays enemy and fighting options"""
    boss_room = room == 6
    if boss_room:
        stats["damage"] += 4
    j = 1
    player_damage = stats["damage"]

    for enemy, enemy_stats in populate_room(boss_room):
        enemy_health = float(enemy_stats["health"])
        max_enemy_health = enemy_stats['health']

        enemy_hint = f"You encounter a {enemy}!" if not (enemy.startswith("The") or boss_room) else f"You encounter {enemy}!"
        enemy_hint_center = (width - len(enemy_hint)) // 2
        stdscr.clear()
        stdscr.addstr(y_center, enemy_hint_center, enemy_hint, curses.A_UNDERLINE)
        stdscr.refresh()
        sleep(1)

        while stats["current_health"] > 0 and enemy_health > 0:
            action, stats["inventory"] = player_choice_screen(
                stdscr, width, height, y_center, stats, player_damage, enemy, enemy_health, enemy_stats, max_enemy_health, j)
            match action[0]:
                case "NONE":
                    continue
                case "HP":
                    stats["current_health"] = battle.add_hp(stats["current_health"], stats["max_health"], action[1])
                    healed_hint = f"Healed {action[1]} HP!"
                    healed_hint_center = (width - len(healed_hint)) // 2
                    stdscr.clear()
                    stdscr.addstr(y_center, healed_hint_center, healed_hint, colors.GREEN | curses.A_UNDERLINE)
                    stdscr.refresh()
                case "DMG":
                    player_damage += 2
                    dmg_hint = "+2 DMG for this room!"
                    dmg_hint_center = (width - len(dmg_hint)) // 2
                    stdscr.clear()
                    stdscr.addstr(y_center, dmg_hint_center, dmg_hint, colors.RED)
                    stdscr.refresh()
                case "KILL":
                    stdscr.clear()
                    if not boss_room:
                        killed_hint = "Enemy killed!"
                        enemy_health = 0
                    else:
                        ## 100 Dollar Bill fails on bosses
                        killed_hint = f"{enemy} was unfazed..."
                    killed_hint_center = (width - len(killed_hint)) // 2
                    stdscr.addstr(y_center, killed_hint_center, killed_hint, colors.RED)
                    stdscr.refresh()
                case "ATTACK":
                    enemy_health = attack_screen(stdscr, y_center, width, enemy_health, player_damage)
            sleep(1)
            if enemy_health > 0:
                enemy_attack(stdscr, width, y_center, stats, enemy_stats)
                if stats["current_health"] <= 0:
                    return game_lost_screen(stdscr, width, height, y_center, stats)
        j += 1

    return stats

def enemy_attack(stdscr, width, y_center, stats, enemy_stats):
    """the current enemy attacks the player"""
    stats["current_health"], actual_damage = battle.attack(stats["current_health"], enemy_stats["damage"])
    stdscr.clear()
    damage_hint = f"Got dealt {actual_damage} DMG!"
    damage_hint_center = (width - len(damage_hint)) // 2
    stdscr.addstr(y_center, damage_hint_center, damage_hint, curses.A_ITALIC | colors.RED)
    stdscr.refresh()
    sleep(1)

def player_choice_screen(stdscr, width, height, y_center, stats, player_damage, enemy, enemy_health, enemy_stats, max_enemy_health, j):
    """Displays to the user a menu with the relevant attack/use item options.
    Returns a tuple with 2 items that directs fight_enemy_screen() to execute the chosen action."""
    ## Actions List:
    ## 1. NONE - user returns to menu after viewing inventory
    ## 2. ATTACK - user attacks enemy
    ## (next three concern remove_item())
    ## 3. HP - user consumes hp+ item
    ## 4. DMG - user consumes dmg+ item
    ## 5. KILL - user consumes instakill item

    player_health = stats["current_health"]
    max_player_health = stats["max_health"]

    stdscr.clear()
    a = f" ({j}/4)" if stats["current_room"] < 6 else ""
    hint = f"You are now fighting against {enemy}{a}."
    option1 = "1. Attack"
    option2 = "2. Use Item"
    p_hint = stats["name"] + ":"
    p_health_hint = f"{player_health:.2f}/{max_player_health} HP"
    p_dmg_hint = f"{player_damage} DMG"
    enemy1 = enemy + ":"
    en_health_hint = f"{enemy_health:.2f}/{max_enemy_health} HP"
    en_dmg_hint = f"{enemy_stats["damage"]} DMG"
    hint_center = (width - len(hint)) // 2

    if player_health < max_player_health * 0.3:
        p_health_color = colors.RED
    elif player_health < max_player_health * 0.85:
        p_health_color = colors.ORANGE
    else:
        p_health_color = colors.GREEN

    if enemy_health < max_enemy_health * 0.3:
        en_health_color = colors.RED
    elif enemy_health < max_enemy_health * 0.85:
        en_health_color = colors.ORANGE
    else:
        en_health_color = colors.GREEN

    stdscr.addstr(4, hint_center, hint, curses.A_ITALIC | colors.RED)

    stdscr.addstr(y_center + 8, 37, option1, curses.A_UNDERLINE)
    stdscr.addstr(y_center + 8, width - len(option2) - 37, option2, curses.A_UNDERLINE)

    stdscr.addstr(y_center + 10, 3, p_hint, curses.A_BOLD | colors.GREEN | curses.A_UNDERLINE)
    stdscr.addstr(y_center + 11, 3, p_health_hint, p_health_color)
    stdscr.addstr(y_center + 12, 3, p_dmg_hint, colors.ORANGE)

    stdscr.addstr(y_center + 10, width - len(enemy1) - 3, enemy1, colors.PURPLE | curses.A_UNDERLINE)
    stdscr.addstr(y_center + 11, width - len(en_health_hint) - 3, en_health_hint, en_health_color)
    stdscr.addstr(y_center + 12, width - len(en_dmg_hint) - 3, en_dmg_hint, colors.ORANGE)

    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord("1"):
            return ("ATTACK", enemy_health), stats["inventory"]
        if key == ord("2"):
            item = pick_from_inventory(stdscr, width, height, stats)
            if item is not None:
                ## also returns a tuple, refer to remove_item()
                return battle.remove_item(stats["inventory"], item)
            return ("NONE", 0), stats["inventory"]

def attack_screen(stdscr, y_center, width, enemy_health, player_damage):
    """handles player choosing to attack"""
    enemy_health, actual_damage = battle.attack(enemy_health, player_damage)
    stdscr.clear()
    damage_hint = f"Dealt {actual_damage} DMG!"
    damage_hint_center = (width - len(damage_hint)) // 2
    stdscr.addstr(y_center, damage_hint_center, damage_hint, curses.A_UNDERLINE | colors.RED)
    stdscr.refresh()
    return enemy_health

def pick_from_inventory(stdscr, width, height, stats):
    """renders all items in inventory and asks the player to pick one"""
    stdscr.clear()
    hint = "Pick an item from your inventory!"
    hint2 = "Press / to go back."
    hint_center = (width - len(hint)) // 2
    hint2_center = (width - len(hint2)) // 2
    stdscr.addstr(2, hint_center, hint, curses.A_ITALIC | colors.ORANGE)
    stdscr.addstr(height - 2, hint2_center, hint2, curses.A_ITALIC)

    valid_keys = [ord("/")]
    for i, item in enumerate(stats["inventory"]):
        item1 = f"{i + 1}. {item}"
        item1_center = (width - len(item1)) // 2
        color = colors.GREEN
        if battle.hp_change(item, stats["current_health"], stats["max_health"]):
            valid_keys.append(ord(str(i+1)))
        else:
            color = colors.RED
        stdscr.addstr(8 + i * 2, item1_center, item1, color | curses.A_UNDERLINE)
        desc = find_desc(item)
        if desc is not None:
            desc_center = (width - len(desc)) // 2
            stdscr.addstr(9 + i * 2, desc_center, desc, curses.A_ITALIC)
    for j in range(len(stats["inventory"]), 5):
        empty_hint = f"{j + 1}. Empty inventory slot"
        empty_hint_center = (width - len(empty_hint)) // 2
        stdscr.addstr(10 + j * 2, empty_hint_center, empty_hint, curses.A_UNDERLINE)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key in valid_keys:
            if key == ord("1"):
                return stats["inventory"][0]
            if key == ord("2"):
                return stats["inventory"][1]
            if key == ord("3"):
                return stats["inventory"][2]
            if key == ord("4"):
                return stats["inventory"][3]
            if key == ord("5"):
                return stats["inventory"][4]
            return None

def item_reward_screen(stdscr, width, height, y_center, inventory):
    """presents player with a choice between two items after clearing a room"""
    chosen_items = battle.pick_items()
    stdscr.clear()
    for i, item in enumerate(chosen_items, start = 1):
        if item in ("Bandage", "Serum", "Painkiller"):
            color = colors.GREEN
        elif item == "Meat":
            color = colors.RED
        else:
            color = colors.YELLOW
        item_hint = f"{i}. {item}"
        a = 3 if i == 1 else width - len(item_hint) - 3
        stdscr.addstr(y_center - 3, a, item_hint, color)

        desc = find_desc(item)
        if desc is not None:
            b = 3 if i == 1 else width - len(desc) - 3
            stdscr.addstr(y_center - 2, b, desc, curses.A_ITALIC)

    hint1 = "Pick one of the item below!"
    hint1_center = (width - len(hint1)) // 2
    hint2 = "Press / to skip."
    hint2_center = (width - len(hint2)) // 2
    stdscr.addstr(2, hint1_center, hint1, curses.A_UNDERLINE | colors.ORANGE)
    stdscr.addstr(height - 2, hint2_center, hint2, curses.A_ITALIC | colors.RED)
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord("/"):
            pass
        if len(inventory) != 5:
            if key == ord("1"):
                inventory.append(chosen_items[0])
            if key == ord("2"):
                inventory.append(chosen_items[1])
        else:
            item = item_removal_screen(stdscr, width, height, y_center, inventory)
            if item is None:
                return item_reward_screen(stdscr, width, height, y_center, inventory)
            _, inventory = battle.remove_item(inventory, item)
            inventory.append(item)
        return inventory

def item_removal_screen(stdscr, width, height, y_center, inventory):
    """prompts the player to delete an item
    if their inventory is full"""
    stdscr.clear()
    hint = "Select an item to remove:"
    hint_center = (width - len(hint)) // 2
    stdscr.addstr(2, hint_center, hint, curses.A_ITALIC)
    for i, item in enumerate(inventory, start = 1):
        item_hint = f"{i}. {item}"
        item_hint_center = (width - len(item_hint)) // 2

        if item in ("Bandage", "Serum", "Painkiller"):
            color = colors.GREEN
        elif item == "Meat":
            color = colors.RED
        else:
            color = colors.YELLOW

        stdscr.addstr(y_center + 2 + i, item_hint_center, item_hint, curses.A_UNDERLINE | color)
    hint2 = "Press / to go back."
    hint2_center = (width - len(hint2)) // 2
    stdscr.addstr(height - 2, hint2_center, hint2, curses.A_ITALIC)
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord("/"):
            return None
        if key == ord("1"):
            return inventory[0]
        if key == ord("2"):
            return inventory[1]
        if key == ord("3"):
            return inventory[2]
        if key == ord("4"):
            return inventory[3]
        if key == ord("5"):
            return inventory[4]

def game_won_screen(stdscr, width, height, y_center):
    """renders game won screen"""
    stdscr.clear()
    message_window = curses.newwin(height - 2, width, 0, 0)
    input_window = curses.newwin(2, width, height - 2, 0)
    input_window.nodelay(True)

    hint = "You won!"
    hint_center = (width - len(hint)) // 2
    message_window.addstr(y_center, hint_center, hint, colors.GREEN | curses.A_ITALIC)

    for i in range(10, 0, -1):
        hint2 = f"You'll exit the game automatically in {i:02d} seconds."
        hint2_center = (width - len(hint2)) // 2
        message_window.addstr(height - 3, hint2_center, hint2, curses.A_ITALIC)
        message_window.refresh()

        input_window.clear()
        hint3 = "Press any key to quit instantly."
        hint3_center = (width - len(hint3)) // 2
        input_window.addstr(0, hint3_center, hint3, curses.A_ITALIC)
        input_window.refresh()

        next_update = monotonic() + 1
        while monotonic() < next_update:
            key = input_window.getch()
            if key != -1:
                return
            sleep(0.05)

    return

def game_lost_screen(stdscr, width, height, y_center, stats):
    """renders game lost screen"""
    stats["game_status"] = 0
    stdscr.clear()
    message_window = curses.newwin(height - 2, width, 0, 0)
    input_window = curses.newwin(2, width, height - 2, 0)
    input_window.nodelay(True)

    hint = "You died!"
    hint_center = (width - len(hint)) // 2
    message_window.addstr(y_center, hint_center, hint, colors.RED | curses.A_ITALIC)

    for i in range(10, 0, -1):
        hint2 = f"You'll exit the game automatically in {i} seconds."
        hint2_center = (width - len(hint2)) // 2
        message_window.addstr(height - 3, hint2_center, hint2, curses.A_ITALIC)
        message_window.refresh()

        input_window.clear()
        hint3 = "Press any key to quit instantly."
        hint3_center = (width - len(hint3)) // 2
        input_window.addstr(0, hint3_center, hint3, curses.A_ITALIC)
        input_window.refresh()

        next_update = monotonic() + 1
        while monotonic() < next_update:
            key = input_window.getch()
            if key != -1:
                return stats
            sleep(0.05)

    return stats
