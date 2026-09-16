"""for handler() and calculation of screen proportions"""
import curses
from constants.colors import init_colors
from menus import main_menu
from menus import main_game
import scripts.file_validity as valid
from scripts.save_file_management import file_save

def init_screen(stdscr):
    """initializes menu and provides with useful variables"""
    init_colors()
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.clear()
    stdscr.refresh()
    height: int
    width: int
    height, width = stdscr.getmaxyx()
    y_center = height // 2

    handler(stdscr, height, width, y_center)


def handler(stdscr, height, width, y_center):
    """menu controller function"""
    main_menu.main_menu(stdscr, height, width, y_center)
    main_menu.file_select(stdscr, height, width, y_center)

    from scripts.save_file_management import pull_stats
    file_name, stats = pull_stats()

    if stats is not None:
        for room in range(stats["current_room"], 7):
            ## handles room changes
            main_game.room_screen(stdscr, width, y_center, room)
            new_stats = main_game.fight_enemy_screen(stdscr, width, height, y_center, stats, room)
            if new_stats["game_status"] == 0:
                break
            file_save(new_stats, file_name) ## increases current_room count too
            if room != 6:
                stats["inventory"] = main_game.item_reward_screen(stdscr, width, height, y_center, stats["inventory"])
            else:
                ## game_lost_screen() is handled inside main_game.py
                main_game.game_won_screen(stdscr, width, height, y_center)
                stats["game_status"] = 2
                break
        file_save(new_stats, file_name) ## handles game lost/won scenarios
        quit()

if __name__ == "__main__":
    valid.ensure_enemy_validity()
    valid.ensure_character_validity()
    valid.ensure_boss_validity()

    curses.wrapper(init_screen)
