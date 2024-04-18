import datetime
import logging
import os
import time
import warnings

import requests
from alive_progress import alive_bar
from notifypy import Notify

logging.getLogger("playsound").setLevel(logging.CRITICAL)
from playsound import playsound

_NOTIFICATION_ICON = str(os.path.join(os.path.dirname(__file__), "clidoro.png"))


def _playsound(sound: str, sound_dir: str, mode="pomodoro"):
    path = os.path.join(sound_dir, sound + ".mp3")
    if not os.path.exists(path):
        download_assets(
            f"https://kingjuno.github.io/data-server/files/clidoro/assets/{sound}.mp3",
            sound_dir,
        )
    playsound(path, block=False)
    notification = Notify()
    notification.title = "Clidoro"
    notification.icon = _NOTIFICATION_ICON
    notification.message = f"{'Good Job! Take a Break now.' if mode=='pomodoro' else 'Time to start working.'}"
    notification.send()


def _timer(mins, sound="simple-notification", sound_dir=None, mode="pomodoro"):
    try:
        with alive_bar(
            int(mins), spinner="waves", title="Clidoro >", stats="", elapsed=None
        ) as bar:
            for i in range(1, int(1 + 60 * mins)):
                time.sleep(1)
                if i % 60 == 0:
                    bar()
        if sound_dir:
            _playsound(sound, sound_dir, mode)
        return 1
    except KeyboardInterrupt:
        return -1


def date_str_to_datetime(date_str, format="%Y-%m-%d %H:%M:%S.%f"):
    """
    Convert a date string to a datetime object.

    Args:
    - date_str (str): The date string in the specified format.
    - format (str): The format of the date string (default is '%Y-%m-%d %H:%M:%S.%f').

    Returns:
    - datetime.datetime: The datetime object corresponding to the input date string.
    """
    try:
        datetime_obj = datetime.datetime.strptime(date_str, format)
        return datetime_obj
    except ValueError:
        print("Error: Invalid date string or format.")
        return None


def timestamp_to_datetime(timestamp):
    """
    Convert a Unix timestamp to a datetime object.

    Args:
    - timestamp (int): The Unix timestamp to convert.

    Returns:
    - datetime.datetime: The datetime object corresponding to the input timestamp.
    """
    try:
        datetime_obj = datetime.datetime.fromtimestamp(timestamp)
        return datetime_obj
    except ValueError:
        print("Error: Invalid timestamp.")
        return None


def download_assets(link, download_dir="."):
    os.makedirs(download_dir, exist_ok=True)
    filename = link.split("/")[-1]
    response = requests.get(link)
    if response.status_code == 200:
        file_path = os.path.join(download_dir, filename)
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded: {file_path}")
    else:
        print(f"Failed to download: {link}")
