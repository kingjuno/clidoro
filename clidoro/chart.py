import io
import sqlite3
from contextlib import redirect_stdout
from datetime import date, datetime, timedelta

from clidoro._utils import date_str_to_datetime
from clidoro.termgraph.module import Args, BarChart, Colors, Data

GREEN_COLOR = "\033[92m"
RED_COLOR = "\033[91m"
RESET_COLOR = "\033[0m"


def history_all(cache_dir):
    try:
        conn = sqlite3.connect(f"{cache_dir}/clidoro.sqlite")
        cursor = conn.cursor()
        cursor.execute("SELECT date, amount FROM random_data")
        rows = cursor.fetchall()
        conn.close()
        dates = [list(row) for row in rows]
        if len(dates) == 0:
            raise
    except:
        return f"{RED_COLOR}No data found.{RESET_COLOR}\n"

    todays_date = date.today()
    todays_times = [
        row[1]
        for row in dates
        if datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f").date() == todays_date
    ]
    times = [time[1] for time in dates]

    # Calculate this week's statistics starting from Sunday
    today_weekday = todays_date.weekday()  # 0 for Monday, 6 for Sunday
    start_of_week = todays_date - timedelta(days=today_weekday)
    this_week = [
        time[1]
        for time in dates
        if start_of_week
        <= datetime.strptime(time[0], "%Y-%m-%d %H:%M:%S.%f").date()
        <= todays_date
    ]
    week_stats = (
        f"\n{GREEN_COLOR}Pomodoros This Week: {RED_COLOR}{len(this_week)}{RESET_COLOR}\n"
        + f"{GREEN_COLOR}Hours This Week: {RED_COLOR}{sum(this_week)/60:.2f}{RESET_COLOR}\n"
    )

    first_day = min(
        datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f").date() for row in dates
    )

    days_since_start = (todays_date - first_day).days
    if days_since_start > 0:
        daily_avg = sum(times) / days_since_start
        avg_stats = f"\n{GREEN_COLOR}Daily Average: {RED_COLOR}{daily_avg/60:.2f}{RESET_COLOR} hours\n"
    else:
        avg_stats = ""

    stats = (
        f"{GREEN_COLOR}Pomodoros Today: {RED_COLOR}{len(todays_times)}{RESET_COLOR}\n"
        + f"{GREEN_COLOR}Hours Today: {RED_COLOR}{sum(todays_times)/60:.2f}{RESET_COLOR}\n"
    )

    stats += (
        f"\n{GREEN_COLOR}Pomodoros Total: {RED_COLOR}{len(times)}{RESET_COLOR}\n"
        f"{GREEN_COLOR}Hours Total: {RED_COLOR}{sum(times)/60:.2f}{RESET_COLOR}\n"
    )

    stats += week_stats + avg_stats
    return stats


def history(cache_dir):
    try:
        conn = sqlite3.connect(f"{cache_dir}/clidoro.sqlite")
        cursor = conn.cursor()
        cursor.execute("SELECT date, amount FROM random_data")
        rows = cursor.fetchall()
        conn.close()
        dates = [list(row) for row in rows]
        if len(dates) == 0:
            raise
    except:
        return f"{RED_COLOR}No data found.{RESET_COLOR}\n"

    timers = set([timer[-1] for timer in dates])
    if len(dates) == 0:
        return f"{RED_COLOR}No data found.{RESET_COLOR}\n"
    current_week = datetime.now().isocalendar()[1]
    weekly_stats = {
        "Monday": {timer: 0 for timer in timers},
        "Tuesday": {timer: 0 for timer in timers},
        "Wednesday": {timer: 0 for timer in timers},
        "Thursday": {timer: 0 for timer in timers},
        "Friday": {timer: 0 for timer in timers},
        "Saturday": {timer: 0 for timer in timers},
        "Sunday": {timer: 0 for timer in timers},
    }
    for date, timer in dates:
        date = date_str_to_datetime(date)
        weekday = date.strftime("%A")
        weekly_stats[weekday][timer] += 1

    week_data = [[sum([i[j] for j in i])] for i in weekly_stats.values()]
    data = Data(week_data, list(weekly_stats.keys()), ["Pomodoros by Week Day"])
    chart = BarChart(
        data,
        Args(
            title=None,
            colors=[Colors.Red, Colors.Magenta, Colors.Blue],
            format="{:0.0f}",
        ),
    )
    f = io.StringIO()
    with redirect_stdout(f):
        chart.draw()
    return f.getvalue()
