"""Simple timer app with sound notifications."""

import os
import time
from pathlib import Path
from typing import List, Optional

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import typer

app = typer.Typer(help="Run a timer with optional sub-timer notifications.")

NOTIFICATION_SOUND = Path(__file__).parent / "assets" / "notification.mp3"


def parse_time(time_str: str) -> int:
    """Convert a time string of format MM:SS to total seconds."""
    minutes, seconds = map(int, time_str.split(":"))
    return minutes * 60 + seconds


def play_sound(file_path: str) -> None:
    """Play a sound file."""
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)


def run_timers(total: str, sub: Optional[List[str]] = None) -> None:
    """
    Run a timer for the total time, with optional sub-timer notifications.

    Print notifications are sent to terminal at the end of each timer. All subtimers must occur before the final timer
    """
    print(f"Time Started at {time.strftime('%H:%M:%S', time.localtime(time.time()))}")
    total_seconds = parse_time(total)
    subtimers = sorted(parse_time(s) for s in sub) if sub else []

    start_time = time.time()
    sub_index = 0

    while True:
        elapsed_time = time.time() - start_time

        if sub_index < len(subtimers) and elapsed_time >= subtimers[sub_index]:
            minutes, seconds = divmod(subtimers[sub_index], 60)
            print(
                f"Subtimer {minutes} minute(s) and {seconds} second(s) elapsed "
                f"at {time.strftime('%H:%M:%S', time.localtime(time.time()))}!"
            )
            play_sound(str(NOTIFICATION_SOUND))
            sub_index += 1

        if elapsed_time >= total_seconds:
            minutes, seconds = divmod(total_seconds, 60)
            print(
                f"Total time {minutes} minute(s) and {seconds} second(s) elapsed "
                f"at {time.strftime('%H:%M:%S', time.localtime(time.time()))}!"
            )
            play_sound(str(NOTIFICATION_SOUND))
            break

        time.sleep(1)


@app.command("start")
def start(
    total: str = typer.Option(..., help="Total time in minutes:seconds for the final timer."),
    sub: Optional[List[str]] = typer.Option(
        None, help="Space separated time intervals in minutes:seconds for timer to notify you at."
    ),
):
    """Start a timer, optionally notifying at sub-timer intervals along the way."""
    run_timers(total, sub)
