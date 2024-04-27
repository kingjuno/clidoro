import time
from pathlib import Path

from simple_term_menu import TerminalMenu

from clidoro._utils import _timer, timestamp_to_datetime
from clidoro.chart import history, history_all
from clidoro.data import clear_db, save_to_db

TITLE = """        _   _     _                 
       | | (_)   | |                
   ___ | |  _  __| | ___  _ __ ___  
  / __|| | | |/ _` |/ _ \| '__/ _ \ 
 | (__ | | | | (_| | (_) | | | (_) |
  \___||_| |_|\__,_|\___/|_|  \___/ 
  
  author:kingjuno
"""
CACHE_DIR = Path.home() / ".cache" / "clidoro"


def timer(menu, _save=False):
    """
    pomodoro
    index
    0-5: ["20 mins", "25 mins", "30 mins", "45 mins", "1  hour", "back"]
    prograssable terminal time option
    """
    times = [int(item.split(" ")[0]) for item in menu._menu_entries[:-1]]
    start_time = timestamp_to_datetime(time.time())
    while True:
        menu_entry_index = menu.show()
        if menu_entry_index == len(menu._menu_entries) - 1:
            break
        else:
            _time = times[menu_entry_index]
            start_time = timestamp_to_datetime(time.time())
            stats = _timer(
                _time, "simple-notification", CACHE_DIR, "pomodoro" if _save else "break"
            )
        if _save and stats > 0:
            save_to_db([[start_time, _time]], CACHE_DIR)


def history_menu(menu):
    while True:
        menu_entry_index = menu.show()
        if menu_entry_index == len(menu._menu_entries) - 1:
            break
        elif menu_entry_index == 0:
            _history = history(CACHE_DIR).replace("\n\n", "\n")
        elif menu_entry_index == 1:
            _history = history_all(CACHE_DIR)
        elif menu_entry_index == 2:
            delete_menu = TerminalMenu(
                ["accept", "exit"],
                accept_keys=("enter", "alt-d"),
                menu_highlight_style=("bg_black", "fg_green"),
            )
            delete_index = delete_menu.show()
            if delete_index == 0:
                clear_db(CACHE_DIR)
            return
        print(TITLE, _history, sep="\n")
        terminal_menu = TerminalMenu(
            ["exit"],
            accept_keys=("enter", "alt-d"),
            menu_highlight_style=("bg_black", "fg_green"),
        )
        terminal_menu.show()


def main():
    cli_options = ["start", "break", "history", "exit"]
    pomodoro_options = ["20 mins", "25 mins", "30 mins", "45 mins", "60 mins", "back"]
    break_options = ["5 mins", "10 mins", "15 mins", "30 mins", "back"]
    history_options = ["Pomodoros by weekdays", "Stats", "clear DB", "exit"]
    terminal_menu = TerminalMenu(
        cli_options,
        title=TITLE,
        accept_keys=("enter", "alt-d"),
        clear_screen=True,
        menu_highlight_style=("bg_black", "fg_green"),
    )
    pomodoro_menu = TerminalMenu(
        pomodoro_options,
        title=TITLE,
        accept_keys=("enter", "alt-d"),
        clear_screen=True,
        menu_highlight_style=("bg_black", "fg_green"),
    )
    break_menu = TerminalMenu(
        break_options,
        title=TITLE,
        accept_keys=("enter", "alt-d"),
        clear_screen=True,
        menu_highlight_style=("bg_black", "fg_green"),
    )
    hist_menu = TerminalMenu(
        history_options,
        title=TITLE,
        accept_keys=("enter", "alt-d"),
        clear_screen=True,
        menu_highlight_style=("bg_black", "fg_green"),
    )
    while not False:
        menu_entry_index = terminal_menu.show()
        if menu_entry_index == 0:
            timer(pomodoro_menu, _save=True)
        elif menu_entry_index == 1:
            timer(break_menu)
        elif menu_entry_index == 2:
            history_menu(hist_menu)
        if menu_entry_index == 3:
            break


if __name__ == "__main__":
    main()
