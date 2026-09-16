import curses
from textwrap import wrap
from time import sleep
from constants import colors
from scripts.save_file_management import fetch_saves, new_save, delete_save, pull_save

def main_menu(stdscr, height, width, y_center):
    """main menu"""
    main_title = "BASIC DUNGEON CRAWLER GAME"
    hint = "Press any key to continue!"
    hint_center = (width - len(hint)) // 2
    win_width = len(main_title) + 4
    win_center = (width - win_width) // 2
    stdscr.nodelay(True)

    title_window = curses.newwin(2, win_width, y_center - 8, win_center)
    title_window.clear()

    stdscr.addstr(height - 2, hint_center, hint)
    stdscr.refresh()

    color = colors.CYAN_MAGENTA
    while True:
        try:
            title_window.clear()
            title_window.addstr(1, 1, main_title, color | curses.A_UNDERLINE)
            title_window.refresh()
        except curses.error as e:
            stdscr.addstr(0, 0, f"Error: {str(e)}", curses.color_pair(2))
        sleep(1.5)
        if stdscr.getch() != -1:
            break
        color = colors.RED_GREEN if color != colors.RED_GREEN else colors.CYAN_MAGENTA

def file_select(stdscr, height, width, y_center):
    """allows user to select or delete a save file or create a new one"""
    hint = "///////Select a save file!///////"
    creation_prompt = "Press / to create a new save file!"
    deletion_prompt = "Press Q to delete a save file!"
    hint_center = (width - len(hint)) // 2
    creation_prompt_center = (width - len(creation_prompt)) // 2
    deletion_prompt_center = (width - len(deletion_prompt)) // 2
    stdscr.clear()
    stdscr.nodelay(False)

    window_width = 40
    save_file_list = curses.newwin(10, window_width, y_center - 2, (width - window_width) // 2)
    hints_window = curses.newwin(5, window_width, height - 6, (width - window_width) // 2)

    total_saves, l = fetch_saves()
    for i, save in enumerate(total_saves, start = 1):
        if save == "No save file found.":
            color = colors.WHITE
        elif save in ("Failed to fetch save file.", "Game Lost!"):
            color = colors.RED
        else:
            color = colors.GREEN
        save = f"{i}. {save}"
        save_file_center = max(0, (window_width - len(save)) // 2)
        save_file_list.addnstr(i * 2 + 2, save_file_center, save, window_width - save_file_center, color)

    stdscr.addstr(y_center - 10, hint_center, hint)

    creation_prompt_center = max(0, (window_width - len(creation_prompt)) // 2)
    deletion_prompt_center = max(0, (window_width - len(deletion_prompt)) // 2)

    if l == 0:
        hints_window.addnstr(2, creation_prompt_center, creation_prompt, window_width - creation_prompt_center, colors.ORANGE)
    elif l in (1, 2):
        hints_window.addnstr(2, creation_prompt_center, creation_prompt, window_width - creation_prompt_center, colors.ORANGE)
        hints_window.addnstr(4, deletion_prompt_center, deletion_prompt, window_width - deletion_prompt_center, colors.ORANGE)
    else:
        hints_window.addnstr(2, deletion_prompt_center, deletion_prompt, window_width - deletion_prompt_center, colors.ORANGE)

    stdscr.refresh()
    save_file_list.refresh()
    hints_window.refresh()

    status_tuple = ("No save file found.", "An error was encountered whilst fetching this save file.", "Game Lost!", "Game Won!")
    while True:
        key = stdscr.getch()
        if key == ord("/") and l < 3:
            character_picker(stdscr, height, width, y_center, total_saves)
            return file_select(stdscr, height, width, y_center)
        if key in (ord("q"), ord("Q")) and l > 0:
            return save_file_deletion(stdscr, hints_window, height, width, y_center)
        if key == 49 and total_saves[0] not in status_tuple: ## ord("1")
            return pull_save("save_0.json")
        if key == 50 and total_saves[1] not in status_tuple: ## ord("2")
            return pull_save("save_1.json")
        if key == 51 and total_saves[2] not in status_tuple: ## ord("3")
            return pull_save("save_2.json")

def character_picker(stdscr, height, width, y_center, total_saves):
    """asks user to pick a charcter for their new save file then creates it"""
    while True:
        ## allows user to pick a character
        stdscr.clear()

        prompt = "Pick a character:"
        prompt_center = (width - len(prompt)) // 2
        char1 = "Jax (1)"
        hp1 = "HP: 250"
        dmg1 = "DMG: 15"
        char2 = "Casper (2)"
        hp2 = "HP: 200"
        dmg2 = "DMG: 20"
        char3 = "Blitz (3)"
        hp3 = "HP: 150"
        dmg3 = "DMG: 25"
        selection_hint = "Pick your character by pressing their corresponding number. Press Esc to cancel."
        selection_hint_center = (width - len(selection_hint)) // 2

        window_height = 6
        window_width = 16
        window_y = y_center - window_height // 2
        window_gap = 8
        group_width = window_width * 3 + window_gap
        group_x = (width - group_width) // 2
        left_x = group_x
        center_x = left_x + window_width + window_gap
        right_x = center_x + window_width + window_gap

        char1_win = curses.newwin(window_height, window_width, window_y, left_x)
        char2_win = curses.newwin(window_height, window_width, window_y, center_x)
        char3_win = curses.newwin(window_height, window_width, window_y, right_x)

        char1_win.box()
        char2_win.box()
        char3_win.box()
        stdscr.addstr(2, prompt_center, prompt, curses.A_UNDERLINE)
        char1_win.addstr(1, 2, char1, colors.GREEN)
        char1_win.addstr(2, 2, hp1, colors.GREEN)
        char1_win.addstr(3, 2, dmg1, colors.GREEN)
        char2_win.addstr(1, 2, char2, colors.YELLOW)
        char2_win.addstr(2, 2, hp2, colors.YELLOW)
        char2_win.addstr(3, 2, dmg2, colors.YELLOW)
        char3_win.addstr(1, 2, char3, colors.RED)
        char3_win.addstr(2, 2, hp3, colors.RED)
        char3_win.addstr(3, 2, dmg3, colors.RED)
        stdscr.addstr(height - 2, selection_hint_center, selection_hint, curses.A_UNDERLINE)
        stdscr.refresh()
        char1_win.refresh()
        char2_win.refresh()
        char3_win.refresh()

        char_key = stdscr.getch()
        match char_key:
            case 49: ## ord("1")
                return new_save(total_saves, "Jax")
            case 50: ## ord("2")
                return new_save(total_saves, "Casper")
            case 51: ## ord("3")
                return new_save(total_saves, "Blitz")
            case 27: ## ord("Esc")
                return file_select(stdscr, height, width, y_center)

def save_file_deletion(stdscr, hints_window, height, width, y_center):
    """asks user to pick a save file for deletion"""
    proceed_prompt = "Pick the save file you wish to delete by pressing its corresponding number."
    cancel_prompt = "Press / to go back."
    confirmation_prompt = "THIS ACTION IS IRREVERSIBLE! Press D to confirm or / to cancel."
    window_width = 40

    hints_window.clear()

    proceed_lines = wrap(proceed_prompt, width=window_width)
    for row, line in enumerate(proceed_lines):
        line_center = max(0, (window_width - len(line)) // 2)
        hints_window.addnstr(row, line_center, line, window_width - line_center, curses.A_ITALIC)

    cancel_row = len(proceed_lines) + 1
    cancel_prompt_center = max(0, (window_width - len(cancel_prompt)) // 2)
    hints_window.addnstr(cancel_row, cancel_prompt_center, cancel_prompt, window_width - cancel_prompt_center)

    stdscr.refresh()
    hints_window.refresh()

    while True:
        if (key := stdscr.getch()) == ord("1"):
            file_name = "save_0.json"
            return confirm_deletion(stdscr, confirmation_prompt, width, y_center, height, file_name)
        if key == ord("2"):
            file_name = "save_1.json"
            return confirm_deletion(stdscr, confirmation_prompt, width, y_center, height, file_name)
        if key == ord("3"):
            file_name = "save_2.json"
            return confirm_deletion(stdscr, confirmation_prompt, width, y_center, height, file_name)
        if key == ord("/"):
            return file_select(stdscr, height, width, y_center)

def confirm_deletion(stdscr, confirmation_prompt, width, y_center, height, file_name):
    """confirms deletion of save file"""
    stdscr.clear()
    confirmation_lines = wrap(confirmation_prompt, width=width)
    first_row = y_center - len(confirmation_lines) // 2
    for row, line in enumerate(confirmation_lines):
        line_center = max(0, (width - len(line)) // 2)
        stdscr.addnstr(first_row + row, line_center, line, width - line_center, curses.A_UNDERLINE | colors.RED)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord("/"):
            return file_select(stdscr, height, width, y_center)
        if key in (ord("D"), ord("d")):
            delete_save(file_name)
            return file_select(stdscr, height, width, y_center)
